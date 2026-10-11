"""Controlled phase-3 audit. No repository source or previous output is modified."""
from __future__ import annotations
import hashlib
import json
import platform
import subprocess
import sys
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
from scipy.optimize import differential_evolution

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
P1 = REPO / 'audits/observation_operator_refit_phase1_2026-10-08'
P2 = REPO / 'audits/observation_operator_rolling_origin_phase2_2026-10-08'
FITDIR = P1 / 'tb_global_refit_phase1/results_global_primary'
sys.path.insert(0, str(REPO / 'src'))
sys.path.insert(0, str(P1 / 'tb_global_refit_phase1'))
from tb_seit import calibration, constants, data, model, population, r0, seeds
from run_global_refit import ordinary_monthly_flow

PARAMS = ['beta', 'sigma', 'gamma', 'd', 'alpha']
BOUNDS = dict(zip(PARAMS, [(0.01,1.),(.01,.5),(.05,.30),(.0001,.05),(.5,1.)]))
STEPS = (1., .5, .25)
BANDS = (.001, .005, .01, .02, .05)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_json(name, payload):
    (HERE / name).write_text(json.dumps(payload, indent=2, allow_nan=False) + '\n')


def save_csv(name, rows):
    pd.DataFrame(rows).to_csv(HERE / name, index=False, float_format='%.17g')


def metric(obs, pred):
    err = pred - obs
    return dict(rmse=float(np.sqrt(np.mean(err**2))), mae=float(np.mean(abs(err))), bias=float(np.mean(err)))


def primary_parameters():
    row = pd.read_csv(FITDIR / 'global_refit_parameters.csv', float_precision='round_trip').set_index('model').loc['fractional']
    return {k: float(row[k]) for k in PARAMS}


def profile_grid(param, primary):
    lo, hi = BOUNDS[param]
    value = primary[param]
    grid = [value] + [value-f*(value-lo) for f in (.1,.3,.6)] + [value+f*(hi-value) for f in (.1,.3,.6)]
    if param == 'alpha':
        grid += [.5,.505,.51,.52,.55,.60,.65,.70,.75,.80,.85,.90,.95,1.]
    return sorted(set(grid))


def context(ds):
    # Objective context contains only calibration cases/population. Validation values are
    # not stored, referenced or scored here. Full population forcing extrapolates train only.
    series, trend = population.build_population_exogenous_series(ds)
    mc = constants.compute_model_constants(ds.calibration.population)
    return dict(obs=ds.calibration.cases.to_numpy(float).copy(), mc=mc,
                N_of_t=population.make_N_of_t(series), series=series, trend=trend,
                N0=float(ds.calibration.population.iloc[0]), flow0=float(ds.calibration.cases.iloc[0]),
                train_sha256=hashlib.sha256(ds.calibration.to_csv(index=False, float_format='%.17g').encode()).hexdigest())


def prediction(values, ctx, months=240, step=1.):
    p = model.SeitParameters(**values)
    sim = model.simulate(p, ctx['mc'].lambda_, ctx['mc'].mu, ctx['N_of_t'], ctx['N0'], ctx['flow0'], months, step)
    if sim.solver.status != 'ok':
        raise RuntimeError(f"STOP: final solver {sim.solver.status}")
    pred = ordinary_monthly_flow(sim.solver, p.sigma, months, step)
    if not np.all(np.isfinite(pred)) or np.any(pred < 0):
        raise RuntimeError('STOP: invalid final ordinary prediction')
    return pred


def objective(values, ctx):
    return metric(ctx['obs'], prediction(values, ctx))['rmse']


def fit(ctx, seed, primary, fixed=None):
    free = [k for k in PARAMS if fixed is None or k != fixed[0]]
    rejected = 0
    def cost(x):
        nonlocal rejected
        values = dict(zip(free, map(float, x)))
        if fixed is not None:
            values[fixed[0]] = fixed[1]
        try:
            result = objective(values, ctx)
            if not np.isfinite(result):
                rejected += 1
                return calibration.LARGE_PENALTY
            return result
        except (FloatingPointError, ValueError, OverflowError, RuntimeError):
            rejected += 1
            return calibration.LARGE_PENALTY
    started = time.monotonic()
    result = differential_evolution(cost, bounds=[BOUNDS[k] for k in free], seed=seed,
        strategy=calibration.STRATEGY, popsize=calibration.POPSIZE, mutation=calibration.MUTATION,
        recombination=calibration.RECOMBINATION, tol=calibration.TOL, maxiter=calibration.MAXITER, polish=False)
    if not result.success or not np.isfinite(result.fun) or result.fun >= calibration.LARGE_PENALTY:
        raise RuntimeError(f'STOP: optimization failure seed={seed}, fixed={fixed}: {result.message}')
    values = dict(zip(free, map(float, result.x)))
    if fixed is not None:
        values[fixed[0]] = fixed[1]
    checked = objective(values, ctx)
    if abs(checked - float(result.fun)) > 1e-8:
        raise RuntimeError('STOP: DE objective reproduction discrepancy')
    record = dict(solution_id=f'multiseed_{seed}' if fixed is None else f'profile_{fixed[0]}_{fixed[1]:.17g}',
        source='diagnostic_multiseed' if fixed is None else 'reoptimized_profile', seed=int(seed),
        profile_parameter='' if fixed is None else fixed[0], fixed_value=None if fixed is None else fixed[1],
        **values, calibration_rmse=float(result.fun), delta_rmse=float(result.fun)-objective(primary, ctx),
        optimizer_success=True, optimizer_message=str(result.message), nit=int(result.nit), nfev=int(result.nfev),
        rejected_candidates=rejected, seconds=time.monotonic()-started, train_sha256=ctx['train_sha256'])
    return record


def jacobian(values, mu, q=1.):
    b, s, g, d = [values[k] for k in PARAMS[:4]]
    return np.array([[-mu,0.,-b*q,0.],[0.,-(s+mu),b*q,0.],
                     [0.,s,-(g+mu+d),0.],[0.,0.,g,-mu]])


def next_generation(values, mu, q=1., scale=1.):
    b, s, g, d = [values[k] for k in PARAMS[:4]]
    F = scale*np.array([[0.,b*q],[0.,0.]])
    V = scale*np.array([[s+mu,0.],[-s,g+mu+d]])
    return F @ np.linalg.inv(V)


def stability(values, mu, q=1.):
    eig = np.linalg.eigvals(jacobian(values, mu, q)).astype(complex)
    threshold = values['alpha']*np.pi/2
    zero = np.abs(eig) < 1e-12
    margins = np.abs(np.angle(eig))-threshold
    if np.any(zero) or np.any(np.abs(margins)<1e-12):
        classification = 'NONHYPERBOLIC_OR_SECTOR_BOUNDARY'
    elif np.all(margins>0):
        classification = 'ASYMPTOTICALLY_STABLE_AUTONOMOUS_REFERENCE'
    else:
        classification = 'UNSTABLE_AUTONOMOUS_REFERENCE'
    return classification, eig, margins


def verify_inputs():
    head = subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()
    if head != 'b3ad21bb059eb5357742693a4d5072107dc0df63':
        raise RuntimeError('STOP: repository HEAD discrepancy')
    if subprocess.run(['git','-C',str(REPO),'diff','--quiet']).returncode:
        raise RuntimeError('STOP: tracked modification')
    tracked = json.loads((P1/'integrity_before.json').read_text())
    for path, digest in tracked.items():
        if sha(REPO/path) != digest:
            raise RuntimeError(f'STOP: tracked integrity {path}')
    for folder in (P1, P2):
        for path, digest in json.loads((folder/'artifact_manifest.json').read_text()).items():
            if sha(folder/path) != digest:
                raise RuntimeError(f'STOP: previous phase integrity {folder/path}')
    controls = json.loads((P1/'control_worktrees_before.json').read_text())
    for base, record in controls.items():
        if subprocess.check_output(['git','-C',base,'rev-parse','HEAD'],text=True).strip() != record['head']:
            raise RuntimeError('STOP: control worktree HEAD discrepancy')
        if subprocess.check_output(['git','-C',base,'status','--short'],text=True) != record['status']:
            raise RuntimeError('STOP: control worktree status discrepancy')
        if any(sha(Path(base)/p)!=h for p,h in record['sha256'].items()):
            raise RuntimeError('STOP: control worktree file discrepancy')
    return tracked


def numerical_check(solution_id, values, ctx, months=240, observed=None):
    obs = ctx['obs'] if observed is None else observed
    predictions = {h:prediction(values,ctx,months,h) for h in STEPS}
    m0, mf = metric(obs,predictions[1.]),metric(obs,predictions[.25])
    d1 = float(np.max(abs(predictions[1.]-predictions[.5])))
    d2 = float(np.max(abs(predictions[.5]-predictions[.25])))
    rel = float(np.max(abs(predictions[1.]-predictions[.25])/np.maximum(abs(predictions[.25]),1.)))
    rmse_rel = abs(m0['rmse']-mf['rmse'])/max(abs(mf['rmse']),1.)
    mae_rel = abs(m0['mae']-mf['mae'])/max(abs(mf['mae']),1.)
    bias_rel = abs(m0['bias']-mf['bias'])/float(np.mean(obs))
    passed = rel <= .01 and rmse_rel <= .01 and mae_rel <= .01 and bias_rel <= .01 and d2<=d1+1e-9
    row = dict(solution_id=solution_id, months=months, alpha=values['alpha'], max_pointwise_relative_change=rel,
        max_absolute_change=float(np.max(abs(predictions[1.]-predictions[.25]))), half_difference=d1, quarter_difference=d2,
        rmse_h1=m0['rmse'], rmse_hquarter=mf['rmse'], rmse_relative_change=rmse_rel,
        mae_relative_change=mae_rel, bias_change_relative_observed_mean=bias_rel, status='PASS' if passed else 'FAIL')
    return row, predictions


def append_checkpoint(name, row):
    with (HERE/name).open('a') as stream:
        stream.write(json.dumps(row, allow_nan=False)+'\n')


def run():
    if (HERE/'execution_provenance.json').exists():
        raise RuntimeError('STOP: refusing to overwrite a phase-3 execution')
    tracked = verify_inputs()
    prior = {str(p.relative_to(REPO)):sha(p) for f in (P1,P2) for p in f.rglob('*') if p.is_file()}
    save_json('preserve_previous_phases_sha256.json',prior)
    save_json('tracked_before_sha256.json',tracked)
    primary = primary_parameters()
    ds = data.load_canonical_dataset()
    ctx = context(ds)
    primary_cost = objective(primary,ctx)
    original = pd.read_csv(FITDIR/'global_refit_parameters.csv',float_precision='round_trip').set_index('model').loc['fractional']
    if abs(primary_cost-float(original.objective_train_rmse))>1e-7:
        raise RuntimeError('STOP: phase-1 primary objective discrepancy')
    assert seeds.ALL_SEEDS == [20260815,20260816,20260817,20260818,20260819]
    assert len(ctx['obs'])==240 and calibration.MAXITER==1000 and calibration.POPSIZE==15
    grids={k:profile_grid(k,primary) for k in ['beta','gamma','d','alpha']}
    save_json('execution_provenance.json',dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),
        head=subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip(),
        repository=str(REPO),python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,
        bounds=BOUNDS,primary_seed=seeds.PRIMARY_SEED,diagnostic_seeds=seeds.DIAGNOSTIC_SEEDS,
        primary_parameters=primary,primary_rmse=primary_cost,profile_grids=grids,train_sha256=ctx['train_sha256'],
        calibration_months=240,validation_months=24,validation_used_in_fit=False,solver_steps=list(STEPS),
        constants=dict(mu=ctx['mc'].mu,lambda_=ctx['mc'].lambda_,N0=ctx['N0'],flow0=ctx['flow0']),
        de=dict(strategy=calibration.STRATEGY,popsize=calibration.POPSIZE,mutation=calibration.MUTATION,
                recombination=calibration.RECOMBINATION,tol=calibration.TOL,maxiter=calibration.MAXITER,polish=False),
        protocol_sha256=sha(HERE/'PROTOCOL_DECISION.md'),executed_script_sha256=sha(__file__)))
    pool=[dict(solution_id='primary_20260815',source='reused_phase1_primary',seed=20260815,
        profile_parameter='',fixed_value=None,**primary,calibration_rmse=primary_cost,delta_rmse=0.,
        optimizer_success=bool(original.success),optimizer_message='Reused accepted phase-1 fit; no recalibration',
        nit=int(original.iterations),nfev=int(original.function_evaluations),rejected_candidates=0,seconds=0.,train_sha256=ctx['train_sha256'])]
    fixed_rows=[]
    numeric=[]
    primary_check,_=numerical_check(pool[0]['solution_id'],primary,ctx)
    numeric.append(primary_check)
    if primary_check['status']!='PASS':
        raise RuntimeError('STOP: primary numerical gate')
    # Fixed section is kept separate from the reoptimized profile and envelope pool.
    for alpha in grids['alpha']:
        values={**primary,'alpha':alpha}
        cost=objective(values,ctx)
        check,_=numerical_check(f'fixed_alpha_{alpha:.17g}',values,ctx)
        numeric.append(check)
        append_checkpoint('numerical_checkpoint.jsonl',check)
        if check['status']!='PASS':
            raise RuntimeError(f'STOP: fixed-alpha numerical gate at {alpha}')
        fixed_rows.append(dict(alpha=alpha,**{k:values[k] for k in PARAMS[:4]},calibration_rmse=cost,
                               delta_rmse=cost-primary_cost,other_parameters='FIXED_PHASE1_PRIMARY'))
    save_csv('alpha_fixed_section.csv',fixed_rows)
    for seed in seeds.DIAGNOSTIC_SEEDS:
        row=fit(ctx,seed,primary)
        check,_=numerical_check(row['solution_id'],{k:row[k] for k in PARAMS},ctx)
        numeric.append(check)
        append_checkpoint('numerical_checkpoint.jsonl',check)
        append_checkpoint('fit_checkpoint.jsonl',row)
        if check['status']!='PASS':
            raise RuntimeError(f"STOP: numerical gate {row['solution_id']}")
        pool.append(row)
        print(f"{row['solution_id']}: RMSE={row['calibration_rmse']:.6f}, alpha={row['alpha']:.6f}, success=True",flush=True)
    for param,grid in grids.items():
        for value in grid:
            row=fit(ctx,seeds.PRIMARY_SEED,primary,(param,value))
            check,_=numerical_check(row['solution_id'],{k:row[k] for k in PARAMS},ctx)
            numeric.append(check)
            append_checkpoint('numerical_checkpoint.jsonl',check)
            append_checkpoint('fit_checkpoint.jsonl',row)
            if check['status']!='PASS':
                raise RuntimeError(f"STOP: numerical gate {row['solution_id']}")
            pool.append(row)
            print(f"{row['solution_id']}: RMSE={row['calibration_rmse']:.6f}, alpha={row['alpha']:.6f}, success=True",flush=True)
    # Only now access validation case values, after all calibrations have finished.
    observed=ds.full.cases.to_numpy(float)
    prediction_rows=[]
    state_rows=[]
    stability_rows=[]
    eigen_rows=[]
    frozen_rows=[]
    for row in pool:
        values={k:row[k] for k in PARAMS}
        row['R0_reference']=r0.r0_diagnostic(values['beta'],values['sigma'],values['gamma'],values['d'],ctx['mc'].mu)
        row['relative_cost_above_primary']=row['calibration_rmse']/primary_cost-1
        row['admissible_1pct']=row['relative_cost_above_primary']<=.01+1e-12
        row['parameter_bounds_satisfied']=all(BOUNDS[k][0]<=values[k]<=BOUNDS[k][1] for k in PARAMS)
        check,preds=numerical_check(row['solution_id'],values,ctx,264,observed)
        numeric.append(check)
        append_checkpoint('numerical_checkpoint.jsonl',check)
        if check['status']!='PASS':
            raise RuntimeError(f"STOP: full-span numerical gate {row['solution_id']}")
        pred=preds[1.]
        row.update({f'validation_{k}':v for k,v in metric(observed[240:],pred[240:]).items()})
        row['calibration_rmse_hquarter']=metric(observed[:240],preds[.25][:240])['rmse']
        row['admissible_1pct_hquarter_primary_reference']=row['calibration_rmse_hquarter']<=primary_check['rmse_hquarter']*1.01+1e-10
        for date,actual,estimate in zip(ds.full.date,observed,pred):
            prediction_rows.append(dict(solution_id=row['solution_id'],source=row['source'],date=str(date.date()),
                split='calibration' if date<=data.CALIBRATION_END else 'validation_open_loop',observed=float(actual),predicted=float(estimate)))
        y0=model.initial_conditions(model.SeitParameters(**values),ctx['mc'].mu,ctx['N0'],ctx['flow0'])
        state_rows.append(dict(solution_id=row['solution_id'],**dict(zip(['S0','E0','I0','T0','C0'],map(float,y0))),
                               train_sha256=ctx['train_sha256'],validation_used_in_optimization=False))
        cls,eig,margins=stability(values,ctx['mc'].mu)
        stability_rows.append(dict(solution_id=row['solution_id'],alpha=values['alpha'],R0_reference=row['R0_reference'],
            admissible_1pct=row['admissible_1pct'],classification=cls,max_eigenvalue_real=float(max(eig.real)),
            min_matignon_margin=float(min(margins)),N_reference=ctx['mc'].lambda_/ctx['mc'].mu,
            theory_scope='AUTONOMOUS_CONSTANT_N_REFERENCE_ONLY'))
        for idx,(ev,margin) in enumerate(zip(eig,margins)):
            eigen_rows.append(dict(solution_id=row['solution_id'],eigenvalue_index=idx,real=float(ev.real),imag=float(ev.imag),
                argument_abs=float(abs(np.angle(ev))),alpha=values['alpha'],threshold=values['alpha']*np.pi/2,
                margin=float(margin),criterion_satisfied=bool(margin>0 and abs(ev)>1e-12)))
        for _,nrow in ctx['series'].iterrows():
            q=(ctx['mc'].lambda_/ctx['mc'].mu)/float(nrow.N_model_input)
            cl,ev,ma=stability(values,ctx['mc'].mu,q)
            frozen_rows.append(dict(solution_id=row['solution_id'],date=str(nrow.date.date()),q=q,
                R0_frozen_time=q*row['R0_reference'],max_eigenvalue_real=float(max(ev.real)),
                min_matignon_margin=float(min(ma)),classification=cl.replace('AUTONOMOUS_REFERENCE','FROZEN_TIME_ONLY'),
                nonautonomous_stability_proof=False))
    save_csv('solution_pool.csv',pool)
    save_csv('multiseed_functionals.csv',[r for r in pool if r['source']!='reoptimized_profile'])
    save_csv('profile_objective.csv',[r for r in pool if r['source']=='reoptimized_profile'])
    alpha=[]
    for fr in fixed_rows:
        row=next(r for r in pool if r['profile_parameter']=='alpha' and r['fixed_value']==fr['alpha'])
        alpha.append(dict(alpha=fr['alpha'],fixed_section_rmse=fr['calibration_rmse'],de_profile_rmse=row['calibration_rmse'],
            feasible_cost_upper_bound=min(fr['calibration_rmse'],row['calibration_rmse']),
            de_minus_fixed_rmse=row['calibration_rmse']-fr['calibration_rmse'],
            optimizer_success=row['optimizer_success'],**{f'profiled_{k}':row[k] for k in PARAMS[:4]},
            R0_profile_reference=row['R0_reference'],admissible_1pct=row['admissible_1pct']))
    save_csv('alpha_profile_comparison.csv',alpha)
    save_csv('global_solution_predictions.csv',prediction_rows)
    save_csv('initial_states_and_leakage.csv',state_rows)
    save_csv('numerical_resolution_checks.csv',numeric)
    save_csv('dfe_stability.csv',stability_rows)
    save_csv('dfe_eigenvalues.csv',eigen_rows)
    save_csv('dfe_frozen_time_diagnostics.csv',frozen_rows)
    envelopes=[]
    stats=[]
    for label,subset in [('FULL_DIAGNOSTIC_POOL',pool)]+[(f'NEAR_EQUIVALENT_{100*band:g}_PCT',[r for r in pool if r['calibration_rmse']<=primary_cost*(1+band)+1e-10]) for band in BANDS]:
        rr=np.array([r['R0_reference'] for r in subset])
        envelopes.append(dict(set=label,n=len(subset),minimum=float(rr.min()),maximum=float(rr.max()),median=float(np.median(rr)),
            q25=float(np.quantile(rr,.25)),q75=float(np.quantile(rr,.75)),n_below_1=int(sum(rr<1)),n_above_1=int(sum(rr>1)),
            primary_rmse_reference=primary_cost,interpretation='FINITE_EXPLORED_SET_DESCRIPTIVE_ENVELOPE_NOT_CONFIDENCE_INTERVAL'))
        for param in PARAMS+['R0_reference']:
            v=np.array([r[param] for r in subset])
            stats.append(dict(set=label,parameter=param,n=len(subset),minimum=float(v.min()),maximum=float(v.max()),
                mean=float(v.mean()),std_population=float(v.std()),cv=float(v.std()/abs(v.mean()))))
    save_csv('R0_practical_envelopes.csv',envelopes)
    save_csv('parameter_dispersion.csv',stats)
    predictions=pd.DataFrame(prediction_rows)
    dispersions=[]
    for label,ids in [('FIVE_ORIGINAL_SEEDS',[r['solution_id'] for r in pool if r['source']!='reoptimized_profile']),
                       ('NEAR_EQUIVALENT_1_PCT',[r['solution_id'] for r in pool if r['admissible_1pct']])]:
        for (date,split),frame in predictions[predictions.solution_id.isin(ids)].groupby(['date','split']):
            v=frame.predicted.to_numpy(float)
            dispersions.append(dict(set=label,date=date,split=split,n=len(v),mean=float(v.mean()),std_population=float(v.std()),
                minimum=float(v.min()),maximum=float(v.max()),cv=float(v.std()/abs(v.mean()))))
    save_csv('prediction_dispersion.csv',dispersions)
    verify_inputs()
    if any(sha(REPO/p)!=h for p,h in prior.items()):
        raise RuntimeError('STOP: previous phase file changed')
    save_json('phase3_report.json',dict(status='COMPLETED_REQUIRES_AUTHOR_REVIEW',primary_parameters=primary,
        primary_calibration_rmse=primary_cost,primary_R0_reference=pool[0]['R0_reference'],
        primary_DFE_reference=stability_rows[0],pool_size=len(pool),new_fits=len(pool)-1,
        all_optimizer_success=all(r['optimizer_success'] for r in pool),all_numerical_checks_pass=True,
        near_equivalent_envelopes=envelopes,alpha_fixed_vs_profile=alpha,
        seeds=seeds.ALL_SEEDS,primary_never_replaced=True,validation_not_used_in_fit=True,
        historical_R0_interval_suspended=True,nonautonomous_matignon_claim_not_established=True,
        phase2_evidence_status='PROVISIONALLY_ACCEPTED_NOT_FROZEN',tracked_files_preserved=len(tracked),
        previous_phase_files_preserved=len(prior),rejected_candidates=sum(r['rejected_candidates'] for r in pool)))
    print('PHASE_3_COMPLETE',json.dumps(dict(pool=len(pool),new_fits=len(pool)-1,primary_R0=pool[0]['R0_reference'],envelopes=envelopes)),flush=True)


if __name__=='__main__':
    try:
        run()
    except Exception as exc:
        save_json('STOP_REPORT.json',dict(status='STOP',reason=str(exc),timestamp_utc=datetime.now(timezone.utc).isoformat()))
        raise
