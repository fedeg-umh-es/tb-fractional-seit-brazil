"""Read-only phase-2 ZIP verification; frozen simulations only, no fitting."""
import ast
import hashlib
import io
import json
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath
import numpy as np
import pandas as pd
import scipy.optimize

BASE=Path('/Users/fede/Documents/Codex/2026-10-08/files-pasted-by-the-user-diagn')
REPO=BASE/'work/tb-global-refit-phase1'
ARCHIVE=BASE/'outputs/TB_SEIT_rolling_ordinary_phase2_2026-10-08.zip'
OUT=BASE/'outputs/PHASE2_ZIP_VERIFICATION_2026-10-10'
checks=[]
def forbid(*args,**kwargs):
    raise RuntimeError('New calibration explicitly prohibited during this verification')
scipy.optimize.differential_evolution=forbid
scipy.optimize.minimize=forbid

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def check(name, condition, details=None):
    checks.append(dict(check=name,status='PASS' if condition else 'FAIL',details=details))
    if not condition:
        raise RuntimeError('Verification failed: '+name)
def close(actual,expected,atol=1e-7,rtol=1e-10):
    return bool(np.allclose(actual,expected,atol=atol,rtol=rtol))
def metric(obs,pred):
    err=np.asarray(pred)-np.asarray(obs)
    return dict(RMSE=float(np.sqrt(np.mean(err**2))),MAE=float(np.mean(abs(err))),bias=float(np.mean(err)))

def run():
    with zipfile.ZipFile(ARCHIVE) as archive_zip:
        names=archive_zip.namelist()
        check('ZIP_CRC',archive_zip.testzip() is None)
        check('ZIP_unique_safe_members',len(names)==len(set(names)) and all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names))
        prefix=names[0].split('/')[0]+'/'
        check('ZIP_one_root',all(n.startswith(prefix) for n in names))
        files={n[len(prefix):]:archive_zip.read(n) for n in names if not n.endswith('/')}
    J=lambda n:json.loads(files[n])
    D=lambda n:pd.read_csv(io.BytesIO(files[n]),float_precision='round_trip')
    manifest=J('artifact_manifest.json')
    check('all_manifest_members_present',set(manifest).issubset(files))
    check('all_payload_files_covered',set(files)==set(manifest)|{'artifact_manifest.json'},dict(files=len(files),manifest_entries=len(manifest)))
    check('all_payload_SHA256',all(hashlib.sha256(files[p]).hexdigest()==h for p,h in manifest.items()))
    local=BASE/'outputs/TB_SEIT_rolling_ordinary_phase2_2026-10-08'
    check('ZIP_matches_original_deliverable',all((local/p).is_file() and sha(local/p)==hashlib.sha256(content).hexdigest() for p,content in files.items()))
    audit=REPO/'audits/observation_operator_rolling_origin_phase2_2026-10-08'
    check('ZIP_matches_worktree_audit',all(sha(audit/p)==hashlib.sha256(content).hexdigest() for p,content in files.items()))
    tracked=J('tracked_before_sha256.json')
    check('tracked_239_SHA256',len(tracked)==239 and all(sha(REPO/p)==h for p,h in tracked.items()))
    preserve=J('preserve_phase1_sha256.json')
    check('phase1_24_files_preserved',len(preserve)==24 and all(sha(REPO/p)==h for p,h in preserve.items()))
    check('repository_exact_commit',subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()=='b3ad21bb059eb5357742693a4d5072107dc0df63')
    check('versioned_source_unmodified',subprocess.check_output(['git','-C',str(REPO),'status','--short'],text=True)=='?? audits/\n')
    provenance=J('execution_provenance.json')
    check('pre_execution_code_and_protocol_hashes',all(hashlib.sha256(files[p]).hexdigest()==h for p,h in provenance['pre_run_sha256'].items()))
    check('original_process_success',provenance['exit_code']==0 and provenance['status']=='COMPLETED')
    contract=provenance['de_contract']
    check('DE_seed_and_bounds_original',contract==dict(strategy='best1bin',popsize=15,mutation=[.5,1.],recombination=.7,tol=.01,maxiter=1000,polish=False,seed=20260815,alpha_bounds=[.5,1.],integer_alpha=1.))
    report=J('phase2_report.json')
    check('reported_grid_and_step',report['fits']==26 and report['predictions']==780 and report['common_pairs_per_model']==156 and report['origins']==13 and report['horizons']==list(range(1,13)) and report['h_solver']==1. and report['baseline_fits_executed']==0)
    code=files['run_rolling_ordinary.py'].decode()
    check('source_training_only_and_independent_fits',all(s in code for s in ["df=full[full.date<=origin]", "for label in ['fractional','integer']:", "n_train,H)", "mvalues(ts.train_cases,pred)['RMSE']",'result=differential_evolution(objective',"seed=SEED,polish=False)","for label,pred in origin_forecasts:"]))
    check('source_operator_ordinary',"ordinary_monthly_flow(sim.solver,p.sigma,months,h)" in code and "from run_global_refit import ordinary_monthly_flow" in code)
    p1=REPO/'audits/observation_operator_refit_phase1_2026-10-08'
    p1_provenance=json.loads((p1/'package_provenance.json').read_text())
    op_path=p1/'tb_global_refit_phase1/run_global_refit.py'
    check('ordinary_operator_dependency_hash',sha(op_path)==p1_provenance['executed_script_sha256'])
    op_tree=ast.parse(op_path.read_text())
    op_function=next(n for n in op_tree.body if isinstance(n,ast.FunctionDef) and n.name=='ordinary_monthly_flow')
    op_ast=ast.Module(body=[op_function],type_ignores=[])
    namespace={'np':np}
    # Execute only the already hash-verified quadrature function, never a run or optimizer.
    exec(compile(op_ast,str(op_path),'exec'),namespace)
    original_operator=namespace['ordinary_monthly_flow']
    check('S1_corrected_E_trapezoids',all(s in ast.get_source_segment(op_path.read_text(),op_function) for s in ['solver.y[:, 1]','0.5 * sigma * h * (e[:-1] + e[1:])','reshape(n_months, steps).sum(axis=1)']))
    sys.path.insert(0,str(REPO/'src'))
    from tb_seit import data,model,rolling_origin as ro
    full=data.load_canonical_dataset().full
    observed_by_date=full.set_index('date').cases
    origins=pd.date_range('2020-12-01','2021-12-01',freq='MS')
    labels={'fractional','integer','persistence','seasonal_naive_12','SARIMA'}
    pairs={(str(o.date()),h) for o in origins for h in range(1,13)}
    pred=D('rolling_origin_predictions.csv')
    check('780_complete_unique_common_support',len(pred)==780 and not pred.duplicated(['model','origin','horizon']).any() and set(pred.model)==labels and all(len(sub)==156 and set(zip(sub.origin,sub.horizon))==pairs for _,sub in pred.groupby('model')))
    check('finite_successful_forecasts',np.isfinite(pred[['observed','predicted','residual']]).all().all() and pred.status.eq('ok').all())
    check('residual_identity',close(pred.predicted-pred.observed,pred.residual,atol=1e-8,rtol=0))
    for row in pred.itertuples():
        origin=pd.Timestamp(row.origin)
        target=origin+pd.DateOffset(months=int(row.horizon))
        assert pd.Timestamp(row.target_date)==target and row.observed==observed_by_date.loc[target]
        assert row.train_start=='2001-01-01' and row.train_end==row.origin and row.n_train==len(full[full.date<=origin])
    check('all_dates_targets_observations_training_ends',True)
    common=D('common_support.csv')
    check('common_support_artifact_156',len(common)==156 and set(zip(common.origin,common.horizon))==pairs)
    fits=D('fit_states.csv')
    expected_fits={(str(o.date()),m) for o in origins for m in ['fractional','integer']}
    check('26_distinct_successful_primary_seed_fits',len(fits)==26 and set(zip(fits.origin,fits.model))==expected_fits and not fits.duplicated(['origin','model']).any() and fits.success.all() and fits.seed.eq(20260815).all() and fits.h_solver.eq(1).all())
    bounds=[(.01,1),(.01,.5),(.05,.30),(.0001,.05),(.5,1)]
    check('all_parameters_original_bounds',all(fits[k].between(lo,hi).all() for k,(lo,hi) in zip(['beta','sigma','gamma','d','alpha'],bounds)) and fits[fits.model=='integer'].alpha.eq(1).all())
    check('recorded_DE_budgets_consistent',all(r.function_evaluations==15*(4 if r.model=='integer' else 5)*(r.iterations+1) and r.iterations<=1000 and 0<=r.rejected_candidates<=r.function_evaluations for r in fits.itertuples()))
    leakage=D('leakage_checks.csv')
    check('26_leakage_records',len(leakage)==26 and set(zip(leakage.origin,leakage.model))==expected_fits and leakage.status.eq('PASS').all() and not leakage.target_values_used_in_objective.any())
    steps=D('origin_step_forecasts.csv')
    check('936_frozen_step_forecasts',len(steps)==936 and set(steps.h_solver)=={1.,.5,.25} and not steps.duplicated(['origin','model','horizon','h_solver']).any())
    numerical=D('origin_numerical_checks.csv').set_index(['origin','model'])
    check('26_numeric_gate_records',len(numerical)==26 and numerical.status.eq('PASS').all() and numerical.tolerance.eq(.01).all())
    replay=[]
    max_replay_error=0.
    max_relative_change=0.
    for row in fits.itertuples():
        origin=pd.Timestamp(row.origin)
        frame=full[full.date<=origin].reset_index(drop=True)
        ts=ro.OriginTrainingSet(origin,frame.date,frame.cases.to_numpy(float),frame.population.to_numpy(float),len(frame))
        train_hash=hashlib.sha256(ts.train_cases.tobytes()+ts.train_population.tobytes()).hexdigest()
        assert row.n_train==len(frame) and row.train_sha256==train_hash
        trend=ro.fit_origin_population_trend(ts)
        assert close([trend.intercept,trend.slope],[row.population_trend_intercept,row.population_trend_slope],atol=1e-13,rtol=1e-13)
        assert row.mu==1/(74*12) and close(row.Lambda,row.mu*ts.train_population.mean(),atol=1e-9,rtol=1e-13)
        assert row.N0==ts.train_population[0] and row.flow0==ts.train_cases[0]
        p=model.SeitParameters(row.beta,row.sigma,row.gamma,row.d,row.alpha)
        assert close(model.initial_conditions(p,row.mu,row.N0,row.flow0),json.loads(row.initial_state),atol=1e-8,rtol=1e-13)
        leak=leakage[(leakage.origin==row.origin)&(leakage.model==row.model)].iloc[0]
        assert leak.training_hash==train_hash and leak.train_end==row.origin and leak.population_fit_max_date==row.origin and leak.Lambda_max_date==row.origin
        # Future-case/population perturbation leaves every origin-specific input unchanged.
        changed=full.copy()
        changed.loc[changed.date>origin,['cases','population']]*=100
        changed_frame=changed[changed.date<=origin].reset_index(drop=True)
        assert changed_frame.equals(frame)
        N=ro.make_origin_N_of_t(ts,trend)
        curves=[]
        obs=np.concatenate([ts.train_cases,np.array([observed_by_date.loc[origin+pd.DateOffset(months=h)] for h in range(1,13)])])
        for step in [1.,.5,.25]:
            sim=model.simulate(p,row.Lambda,row.mu,N,row.N0,row.flow0,ts.n_train+12,step)
            assert sim.solver.status=='ok' and np.isfinite(sim.solver.y).all()
            # Independent ordinary integration using the solver's actual corrected time grid.
            E=sim.solver.y[:,1]
            intervals=p.sigma*.5*(E[:-1]+E[1:])*np.diff(sim.solver.t)
            ordinary=intervals.reshape(ts.n_train+12,int(round(1/step))).sum(axis=1)
            assert close(ordinary,original_operator(sim.solver,p.sigma,ts.n_train+12,step),atol=1e-8,rtol=1e-13)
            assert np.all(ordinary>0)
            curves.append(ordinary)
            saved=steps[(steps.origin==row.origin)&(steps.model==row.model)&(steps.h_solver==step)].sort_values('horizon').predicted.to_numpy(float)
            error=float(np.max(abs(ordinary[ts.n_train:]-saved)))
            max_replay_error=max(max_replay_error,error)
            assert close(ordinary[ts.n_train:],saved,atol=1e-6,rtol=1e-10)
            if step==1.:
                assert close(metric(ts.train_cases,ordinary[:ts.n_train])['RMSE'],row.objective_train_RMSE,atol=1e-6,rtol=1e-10)
                main_pred=pred[(pred.origin==row.origin)&(pred.model==row.model)].sort_values('horizon').predicted.to_numpy(float)
                assert close(ordinary[ts.n_train:],main_pred,atol=1e-6,rtol=1e-10)
        coarse,half,quarter=curves
        rel=float(np.max(abs(coarse-quarter)/np.maximum(abs(quarter),1)))
        d1=float(np.max(abs(coarse-half)));d2=float(np.max(abs(half-quarter)))
        m0,mf=metric(ts.train_cases,coarse[:ts.n_train]),metric(ts.train_cases,quarter[:ts.n_train])
        metric_rel=max(abs(m0[k]-mf[k])/max(abs(mf[k]),1) for k in ['RMSE','MAE'])
        bias_rel=abs(m0['bias']-mf['bias'])/float(np.mean(ts.train_cases))
        assert rel<=.01 and metric_rel<=.01 and bias_rel<=.01 and d2<=d1+1e-9
        n=numerical.loc[(row.origin,row.model)]
        assert close([rel,d1,d2,metric_rel],[n.max_relative_change,n.half_difference,n.quarter_difference,n.train_metric_relative_change],atol=1e-7,rtol=1e-8)
        max_relative_change=max(max_relative_change,rel)
        replay.append(dict(origin=row.origin,model=row.model,status='PASS',train_hash=train_hash,
            max_relative_step_change=rel,bias_relative_training_change=bias_rel))
        print('frozen-replay PASS',row.origin,row.model,flush=True)
    check('all_26_frozen_replays_and_training_costs',True,dict(max_prediction_difference=max_replay_error,max_relative_step_change=max_relative_change))
    check('all_26_no_leakage_and_initialization_checks',True)
    baseline=J('baseline_reuse_verification.json')
    check('baseline_provenance_hashes',all(sha(REPO/p)==h for p,h in baseline['input_sha256'].items()))
    old=pd.read_csv(REPO/'outputs/forecasting/rolling_origin_predictions.csv',float_precision='round_trip')
    key=['origin','model','horizon']
    newb=pred[pred.model.isin(['persistence','seasonal_naive_12','SARIMA'])].sort_values(key)
    oldb=old[old.model.isin(['persistence','seasonal_naive_12','SARIMA'])].sort_values(key)
    check('468_baselines_exact_saved_float_reuse',len(newb)==468 and np.array_equal(newb.predicted.to_numpy(float),oldb.predicted.to_numpy(float)) and np.array_equal(newb.observed.to_numpy(float),oldb.observed.to_numpy(float)))
    for origin in origins:
        train=full[full.date<=origin].cases.to_numpy(float)
        pp=newb[(newb.origin==str(origin.date()))&(newb.model=='persistence')].sort_values('horizon').predicted.to_numpy(float)
        ss=newb[(newb.origin==str(origin.date()))&(newb.model=='seasonal_naive_12')].sort_values('horizon').predicted.to_numpy(float)
        assert np.array_equal(pp,np.full(12,train[-1])) and np.array_equal(ss,train[-12:])
    check('persistence_seasonal_definitions',True)
    sarima=json.loads((REPO/'outputs/forecasting/sarima_frozen_order.json').read_text())
    check('SARIMA_selection_training_only_fixed_order',sarima['selection_data']=='2001-01 to 2020-12 (canonical calibration only)' and sarima['selected_order']==dict(p=0,d=1,q=2) and sarima['selected_seasonal_order']==dict(P=1,D=1,Q=1,s=12))
    computed=[]
    for (name,horizon),frame in pred.groupby(['model','horizon']):
        assert len(frame)==13
        computed.append(dict(model=name,horizon=horizon,**metric(frame.observed,frame.predicted)))
    metrics=pd.DataFrame(computed).set_index(['model','horizon'])
    saved_metrics=D('metrics_by_horizon.csv').set_index(['model','horizon'])
    check('all_60_metric_rows_reconstructed',len(metrics)==60 and all(close(metrics[k],saved_metrics.reindex(metrics.index)[k],atol=1e-8,rtol=1e-12) for k in ['RMSE','MAE','bias']))
    skill=D('skill_by_horizon.csv')
    assert len(skill)==168 and not skill.duplicated(['model','baseline','horizon','metric']).any()
    for r in skill.itertuples():
        a=metrics.loc[(r.model,r.horizon),r.metric];b=metrics.loc[(r.baseline,r.horizon),r.metric]
        assert close([a,b,1-a/b],[r.error_model,r.error_baseline,r.skill],atol=1e-9,rtol=1e-12)
    check('all_168_skill_rows_reconstructed',True)
    summary=D('horizon_summary.csv').set_index(['model','baseline','metric'])
    for key,sub in skill.groupby(['model','baseline','metric']):
        flags=sub.sort_values('horizon').skill.to_numpy()>0
        relax=max((h for h,flag in enumerate(flags,1) if flag),default=0)
        strict=next((i for i,flag in enumerate(flags) if not flag),12)
        assert summary.loc[key,'H_relax']==relax and summary.loc[key,'H_strict']==strict
    check('all_14_horizon_summaries_reconstructed',len(summary)==14)
    # Recompute skill signs for all saved frozen steps, no new predictions/optimizations.
    main_sign=skill.set_index(['model','baseline','horizon','metric']).skill.gt(0)
    for step in [1.,.5,.25]:
        derived=metrics.copy()
        for (label,h),frame in steps[steps.h_solver==step].groupby(['model','horizon']):
            target=pred[(pred.model==label)&(pred.horizon==h)].sort_values('origin')
            vals=frame.sort_values('origin').predicted
            for k,v in metric(target.observed.to_numpy(float),vals.to_numpy(float)).items():
                derived.loc[(label,h),k]=v
        for r in skill.itertuples():
            sign=(1-derived.loc[(r.model,r.horizon),r.metric]/derived.loc[(r.baseline,r.horizon),r.metric])>0
            assert sign==main_sign.loc[(r.model,r.baseline,r.horizon,r.metric)]
    check('skill_signs_and_horizons_stable_on_three_steps',True)
    # Crosscheck archived historical comparisons, without fitting or generating baselines.
    comparison=D('historical_metrics_comparison.csv')
    for r in comparison.itertuples():
        oldframe=old[(old.model==r.model)&(old.horizon==r.horizon)]
        historical=metric(oldframe.observed,oldframe.predicted)
        for k in ['RMSE','MAE','bias']:
            assert close(historical[k],getattr(r,k+'_historical'),atol=1e-8,rtol=1e-12)
            assert close(metrics.loc[(r.model,r.horizon),k],getattr(r,k+'_ordinary'),atol=1e-8,rtol=1e-12)
            assert close(getattr(r,k+'_ordinary')-getattr(r,k+'_historical'),getattr(r,'delta_'+k),atol=1e-8,rtol=1e-12)
    check('historical_comparison_reconstructed',True)
    check('source_and_prior_artifacts_still_preserved',all(sha(REPO/p)==h for p,h in tracked.items()) and all(sha(REPO/p)==h for p,h in preserve.items()))
    OUT.mkdir(parents=True,exist_ok=False)
    payload=dict(status='PASS',decision='BLOCKED_MISSING_PHASE2_ARTIFACTS_CAN_BE_LIFTED',
        verification_date='2026-10-10',zip_sha256=sha(ARCHIVE),zip_files=len(files),payload_sha256_entries=len(manifest),
        predictions=780,pairs_per_model=156,fits_recorded=26,new_calibrations=0,frozen_simulations=78,
        source_operator='Ordinary monthly integral of sigma*E; composite trapezoids of corrected E, independent of fractional C',
        max_replay_prediction_difference=max_replay_error,max_relative_step_change=max_relative_change,
        sarima_limitation='Per-origin fitted coefficients not saved; exact reuse and immutable code/data/order provenance checked; no refit',
        remaining_blocks=['Scientific review/acceptance of phase-3 identifiability including alpha boundary/profile, R0 envelope and DFE scope',
                          'Reconcile claims and author decision to freeze phase-2 evidence',
                          'PR #3 remains draft / DO NOT MERGE; manuscript and compilation not authorized until scientific closure'],
        manuscript_changes=0,checks=checks)
    (OUT/'verification_report.json').write_text(json.dumps(payload,indent=2)+'\n')
    pd.DataFrame(replay).to_csv(OUT/'frozen_replay_checks.csv',index=False,float_format='%.17g')
    (OUT/'VERIFY_RESULT.md').write_text('Puede levantarse `BLOCKED_MISSING_PHASE2_ARTIFACTS`.\n\n'
        'El ZIP original supera CRC y los 36 hashes SHA-256 de sus 37 archivos. Se verifican el operador ordinario S1, el protocolo registrado, los 26 ajustes guardados y las 780 predicciones sobre soporte común (156 por modelo). Se reprodujeron 78 simulaciones con parámetros congelados, en h=1,0.5,0.25, sin recalibración; costes, métricas y skill coinciden.\n\n'
        'Permanecen pendientes la revisión y aceptación científica de Fase 3 (identificabilidad/α, R₀, DFE), la reconciliación de claims y la decisión del autor de congelar Fase 2. PR #3 sigue en borrador y bloqueado para merge; manuscrito y compilación no quedan liberados por esta verificación.\n\n'
        'Limitación SARIMA: se acredita reutilización exacta y procedencia del código, datos, orden y soporte; no se reconstruyeron los coeficientes por origen, que no están archivados.\n\n'
        f'SHA-256 del ZIP: `{sha(ARCHIVE)}`.\n')
    inventory={p.name:sha(p) for p in OUT.iterdir() if p.is_file()}
    (OUT/'artifact_manifest.json').write_text(json.dumps(inventory,indent=2)+'\n')
    print(json.dumps({k:v for k,v in payload.items() if k!='checks'},indent=2))

if __name__=='__main__':
    run()
