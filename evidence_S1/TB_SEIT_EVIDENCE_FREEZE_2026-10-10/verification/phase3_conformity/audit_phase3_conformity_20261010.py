"""Conformity audit of EXISTING tables: no optimizer, solver, or scientific rerun."""
from pathlib import Path
import ast
import csv
import hashlib
import json
import re
import shutil
import subprocess
import numpy as np
import pandas as pd

BASE=Path('/Users/fede/Documents/Codex/2026-10-08/files-pasted-by-the-user-diagn')
REPO=BASE/'work/tb-global-refit-phase1'
P1=REPO/'audits/observation_operator_refit_phase1_2026-10-08'
P2=REPO/'audits/observation_operator_rolling_origin_phase2_2026-10-08'
P3=REPO/'audits/observation_operator_phase3_identifiability_2026-10-08'
OUT=BASE/'outputs/TB_SEIT_PHASE3_CONFORMITY_AUDIT_2026-10-10'
PARAMS=['beta','sigma','gamma','d','alpha']
CHECKS=[]

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def check(label,valid,detail=None):
    CHECKS.append(dict(check=label,status='PASS' if bool(valid) else 'FAIL',detail=detail))
    if not valid:
        raise RuntimeError('Scientific conformity discrepancy: '+label)

def close(a,b,atol=1e-8,rtol=1e-12):
    return bool(np.allclose(a,b,atol=atol,rtol=rtol))

def read(name):
    return pd.read_csv(P3/name,float_precision='round_trip')

def metric(obs,pred):
    err=np.asarray(pred)-np.asarray(obs)
    return dict(rmse=float(np.sqrt(np.mean(err**2))),mae=float(np.mean(abs(err))),bias=float(np.mean(err)))

def chronology():
    session=Path('/Users/fede/.codex/sessions/2026/10/08/rollout-2026-10-08T18-08-54-01a11c46-59b9-7523-be14-f505ed10eb83.jsonl')
    events=[]
    fragments=[]
    for index,line in enumerate(session.open(),1):
        obj=json.loads(line)
        p=obj.get('payload',{})
        if obj.get('timestamp','')>='2026-10-09' or p.get('type')!='custom_tool_call':
            continue
        code=p.get('input','')
        if 'observation_operator_phase3_identifiability_2026-10-08' not in code:
            continue
        if 'tools.apply_patch' in code:
            for match in re.finditer(r'tools\.apply_patch\(("(?:\\.|[^"\\])*")\)',code):
                patch=json.loads(match.group(1))
                lines=patch.splitlines()
                for start,s in enumerate(lines):
                    if s.startswith('*** Add File:') and (s.endswith('/PROTOCOL_DECISION.md') or s.endswith('/run_phase3.py')):
                        text=[]
                        for part in lines[start+1:]:
                            if part.startswith('***'):break
                            if part.startswith('+'):text.append(part[1:])
                        name=s.rsplit('/',1)[1]
                        digest=hashlib.sha256(('\n'.join(text)+'\n').encode()).hexdigest()
                        events.append(dict(event='write_'+name,timestamp_utc=obj['timestamp'],session_line=index,
                            recovered_content_sha256=digest,current_content_sha256=sha(P3/name),same_bytes=digest==sha(P3/name)))
                        fragments.append(line)
        if '/run_phase3.py > ' in code:
            events.append(dict(event='launch_phase3',timestamp_utc=obj['timestamp'],session_line=index))
            fragments.append(line)
    return events,fragments

def main():
    if OUT.exists():raise RuntimeError('Refusing to overwrite audit deliverable')
    before={str(p.relative_to(P3)):sha(p) for p in P3.rglob('*') if p.is_file()}
    prov=json.loads((P3/'execution_provenance.json').read_text())
    report=json.loads((P3/'phase3_report.json').read_text())
    check('adopted_protocol_hash',sha(P3/'PROTOCOL_DECISION.md')==prov['protocol_sha256']=='58d4bed36871f9c63cd93e4c199d5c9890f006ccaf96ede85362480dee91469b')
    check('executed_script_hash',sha(P3/'run_phase3.py')==prov['executed_script_sha256'])
    tracked=json.loads((P3/'tracked_before_sha256.json').read_text())
    previous=json.loads((P3/'preserve_previous_phases_sha256.json').read_text())
    check('239_versioned_files_unchanged',len(tracked)==239 and all(sha(REPO/p)==h for p,h in tracked.items()))
    check('61_previous_phase_files_unchanged',len(previous)==61 and all(sha(REPO/p)==h for p,h in previous.items()))
    reconciliation=BASE/'outputs/PHASE3_PROTOCOL_RECONCILIATION_2026-10-10/source_evidence_sha256.json'
    check('previous_reconciliation_hashes_preserved',all(sha(Path(p))==h for p,h in json.loads(reconciliation.read_text()).items()))
    events,fragments=chronology()
    creation=next(e for e in events if e['event']=='write_PROTOCOL_DECISION.md')
    script_creation=next(e for e in events if e['event']=='write_run_phase3.py')
    launch=next(e for e in events if e['event']=='launch_phase3')
    check('protocol_exact_bytes_precede_execution',creation['same_bytes'] and creation['timestamp_utc']<launch['timestamp_utc'],events)
    check('executor_exact_bytes_precede_execution',script_creation['same_bytes'] and script_creation['timestamp_utc']<launch['timestamp_utc'])
    p1report=json.loads((P1/'tb_global_refit_phase1/results_global_primary/phase1_report.json').read_text())
    p1package=json.loads((P1/'package_provenance.json').read_text())
    primary=next(r for r in p1report['parameters'] if r['model']=='fractional')
    integer=next(r for r in p1report['parameters'] if r['model']=='integer')
    p1code=P1/'tb_global_refit_phase1/run_global_refit.py'
    check('phase1_executor_integrity',sha(p1code)==p1package['executed_script_sha256'])
    ast1=ast.parse(p1code.read_text())
    operator=next(x for x in ast1.body if isinstance(x,ast.FunctionDef) and x.name=='ordinary_monthly_flow')
    opsource=ast.get_source_segment(p1code.read_text(),operator)
    check('S1_ordinary_corrected_E_quadrature',all(s in opsource for s in ['solver.y[:, 1]','0.5 * sigma * h * (e[:-1] + e[1:])','reshape(n_months, steps).sum(axis=1)']) and '[:, 4]' not in opsource)
    model_source=(REPO/'src/tb_seit/model.py').read_text()
    check('observable_C_no_feedback_and_T_derivative',all(s in model_source for s in ['force_of_infection = params.beta * S * I / N','dE = force_of_infection - (params.sigma + mu) * E','dI = params.sigma * E - (params.gamma + mu + params.d) * I','dT = params.gamma * I - mu * T','dC = params.sigma * E']))
    de_call=next(n for n in ast.walk(ast1) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='differential_evolution')
    check('global_fit_no_old_x0_population',not {'x0','init'}.intersection(k.arg for k in de_call.keywords))
    check('primary_exact_phase1_reuse',all(primary[k]==prov['primary_parameters'][k] for k in PARAMS))
    check('primary_calibration_precedes_phase3_protocol',p1report['timestamp_utc']<creation['timestamp_utc'])
    pool=read('solution_pool.csv').set_index('solution_id',drop=False)
    predictions=read('global_solution_predictions.csv')
    num=read('numerical_resolution_checks.csv').set_index(['solution_id','months'])
    fixed=read('alpha_fixed_section.csv')
    profiles=read('profile_objective.csv')
    alpha=read('alpha_profile_comparison.csv')
    envelopes=read('R0_practical_envelopes.csv').set_index('set')
    states=read('initial_states_and_leakage.csv').set_index('solution_id')
    eigen=read('dfe_eigenvalues.csv')
    stability=read('dfe_stability.csv').set_index('solution_id')
    frozen=read('dfe_frozen_time_diagnostics.csv')
    check('47_all_solutions_no_filtering',len(pool)==47 and pool.index.is_unique and pool.source.value_counts().to_dict()=={'reoptimized_profile':42,'diagnostic_multiseed':4,'reused_phase1_primary':1})
    check('primary_not_replaced',close(pool.loc['primary_20260815',PARAMS].to_numpy(float),[primary[k] for k in PARAMS],atol=0,rtol=0))
    check('optimizer_seed_budget_bounds',pool.optimizer_success.all() and all(pool[k].between(*prov['bounds'][k]).all() for k in PARAMS))
    diag=pool[pool.source=='diagnostic_multiseed']
    check('four_declared_diagnostic_seeds_and_primary_profiles',set(diag.seed)=={20260816,20260817,20260818,20260819} and profiles.seed.eq(20260815).all())
    for r in pool.itertuples():
        free=4 if r.source=='reoptimized_profile' else 5
        assert r.nfev==15*free*(r.nit+1) and r.nit<=1000 and 0<=r.rejected_candidates<=r.nfev
    check('all_DE_evaluation_counts_match_dimension_and_iterations',True)
    check('DE_frozen_contract',prov['de']==dict(strategy='best1bin',popsize=15,mutation=[.5,1.],recombination=.7,tol=.01,maxiter=1000,polish=False))
    for param,grid in prov['profile_grids'].items():
        sub=profiles[profiles.profile_parameter==param].sort_values('fixed_value')
        assert np.array_equal(sub.fixed_value.to_numpy(float),np.array(grid))
        assert np.array_equal(sub[param].to_numpy(float),np.array(grid))
    check('all_recorded_profile_grids_executed_exactly',True,dict(alpha=21,beta=7,gamma=7,d=7))
    grid=prov['profile_grids']['alpha']
    check('fixed_and_profile_alpha_same_21_points',np.array_equal(fixed.alpha.to_numpy(float),grid) and np.array_equal(alpha.alpha.to_numpy(float),grid))
    check('fixed_section_four_parameters_unchanged',all(fixed[k].eq(primary[k]).all() for k in PARAMS[:4]))
    for r in alpha.itertuples():
        fit=profiles[(profiles.profile_parameter=='alpha')&(profiles.fixed_value==r.alpha)].iloc[0]
        f=fixed[fixed.alpha==r.alpha].iloc[0]
        assert close([r.fixed_section_rmse,r.de_profile_rmse,r.feasible_cost_upper_bound,r.de_minus_fixed_rmse],
                     [f.calibration_rmse,fit.calibration_rmse,min(f.calibration_rmse,fit.calibration_rmse),fit.calibration_rmse-f.calibration_rmse])
        assert all(getattr(r,'profiled_'+k)==fit[k] for k in PARAMS[:4])
    check('alpha_fixed_vs_reoptimized_columns_not_mixed',True)
    alpha_one=profiles[(profiles.profile_parameter=='alpha')&(profiles.fixed_value==1)].iloc[0]
    check('alpha1_profile_recovers_independent_phase1_integer',all(alpha_one[k]==integer[k] for k in PARAMS) and close(alpha_one.calibration_rmse,integer['objective_train_rmse']))
    checkpoints=[json.loads(s) for s in (P3/'fit_checkpoint.jsonl').read_text().splitlines()]
    check('46_fit_checkpoints_complete',len(checkpoints)==46 and {r['solution_id'] for r in checkpoints}==set(pool.index)-{'primary_20260815'})
    for r in checkpoints:
        saved=pool.loc[r['solution_id']]
        assert all(saved[k]==r[k] for k in PARAMS+['seed','calibration_rmse','nfev','nit'])
    check('all_checkpoint_parameters_objectives_budgets_agree',True)
    dataset=pd.read_excel(REPO/'data/raw/tb_mes.xlsx')[['data','casos','populacao']].rename(columns={'data':'date','casos':'cases','populacao':'population'}).sort_values('date').reset_index(drop=True)
    train=dataset.iloc[:240]
    train_hash=hashlib.sha256(train.to_csv(index=False,float_format='%.17g').encode()).hexdigest()
    check('train_hash_and_no_validation_objective',train_hash==prov['train_sha256'] and pool.train_sha256.eq(train_hash).all() and states.train_sha256.eq(train_hash).all() and not states.validation_used_in_optimization.any())
    check('47_global_curves_complete_264_months',len(predictions)==47*264 and not predictions.duplicated(['solution_id','date']).any() and set(predictions.solution_id)==set(pool.index))
    for sid,frame in predictions.groupby('solution_id'):
        frame=frame.sort_values('date')
        assert np.array_equal(pd.to_datetime(frame.date).to_numpy(),dataset.date.to_numpy())
        assert np.array_equal(frame.observed.to_numpy(float),dataset.cases.to_numpy(float))
        assert frame.iloc[:240].split.eq('calibration').all() and frame.iloc[240:].split.eq('validation_open_loop').all()
        cost=metric(frame.observed.iloc[:240],frame.predicted.iloc[:240])['rmse']
        assert close(cost,pool.loc[sid,'calibration_rmse'])
        for k,v in metric(frame.observed.iloc[240:],frame.predicted.iloc[240:]).items():
            assert close(v,pool.loc[sid,'validation_'+k])
    check('all47_training_and_validation_metrics_from_saved_predictions',True)
    mu=prov['constants']['mu'];lam=prov['constants']['lambda_'];N0=prov['constants']['N0'];flow0=prov['constants']['flow0']
    check('mu_one_over_888',mu==1/888)
    for sid,r in pool.iterrows():
        E0=flow0/r.sigma;I0=flow0/(r.gamma+mu+r.d)
        assert close(states.loc[sid,['S0','E0','I0','T0','C0']].to_numpy(float),[N0-E0-I0,E0,I0,0,0],atol=1e-7,rtol=1e-13)
    check('all47_analytic_initial_states',True)
    primary_rmse=float(primary['objective_train_rmse']);threshold=primary_rmse*1.01
    admissible=pool.calibration_rmse.le(threshold+1e-10)
    check('1pct_membership_primary_reference',np.array_equal(admissible,pool.admissible_1pct) and close(pool.delta_rmse,pool.calibration_rmse-primary_rmse) and close(pool.relative_cost_above_primary,pool.calibration_rmse/primary_rmse-1))
    check('115_numeric_controls_all_contract_rules',len(num)==115 and num.index.is_unique and num.status.eq('PASS').all() and
        num.max_pointwise_relative_change.le(.01).all() and num.rmse_relative_change.le(.01).all() and num.mae_relative_change.le(.01).all() and num.bias_change_relative_observed_mean.le(.01).all() and (num.quarter_difference<=num.half_difference+1e-9).all())
    for sid,r in pool.iterrows():
        assert close(num.loc[(sid,240),'rmse_h1'],r.calibration_rmse)
        assert close(num.loc[(sid,240),'rmse_hquarter'],r.calibration_rmse_hquarter)
    for r in fixed.itertuples():
        sid=f'fixed_alpha_{r.alpha:.17g}'
        assert close(num.loc[(sid,240),'rmse_h1'],r.calibration_rmse)
    check('numeric_controls_match_pool_and_fixed_section_costs',True)
    quarter_primary=float(num.loc[('primary_20260815',240),'rmse_hquarter'])
    quarter_admissible=pool.calibration_rmse_hquarter.le(quarter_primary*1.01+1e-10)
    check('1pct_membership_stable_on_saved_quarter_grid',np.array_equal(quarter_admissible,pool.admissible_1pct_hquarter_primary_reference) and np.array_equal(quarter_admissible,admissible))
    numeric_checkpoint=[json.loads(s) for s in (P3/'numerical_checkpoint.jsonl').read_text().splitlines()]
    check('114_numeric_checkpoints_complete',len(numeric_checkpoint)==114 and {(r['solution_id'],r['months']) for r in numeric_checkpoint}==set(num.index)-{('primary_20260815',240)})
    for r in numeric_checkpoint:
        n=num.loc[(r['solution_id'],r['months'])]
        assert all(close(n[k],r[k]) for k in ['rmse_h1','rmse_hquarter','max_pointwise_relative_change','max_absolute_change'])
    check('numeric_checkpoint_tables_agree',True)
    # Independent arithmetic identities on the saved parameter table, not a new R0/DFE experiment.
    derived_r0=pool.beta*pool.sigma/((pool.sigma+mu)*(pool.gamma+mu+pool.d))
    check('R0_saved_formula_identity_all47',close(derived_r0,pool.R0_reference,atol=1e-13,rtol=1e-13))
    for label,row in envelopes.iterrows():
        if label=='FULL_DIAGNOSTIC_POOL':sub=pool
        else:
            band=float(label.split('_')[-2])/100
            sub=pool[pool.calibration_rmse<=primary_rmse*(1+band)+1e-10]
        rr=sub.R0_reference.to_numpy(float)
        assert int(row.n)==len(sub)
        assert close([row.minimum,row.maximum,row['median'],row.q25,row.q75],[rr.min(),rr.max(),np.median(rr),np.quantile(rr,.25),np.quantile(rr,.75)])
        assert int(row.n_below_1)==int(sum(rr<1)) and int(row.n_above_1)==int(sum(rr>1))
    check('all6_R0_envelopes_primary_band_complete_pool_separated',True)
    check('fixed_sections_excluded_from_R0_envelope',all(not sid.startswith('fixed_alpha_') for sid in pool.index))
    check('188_eigenvalues_and47_classifications_complete',len(eigen)==188 and len(stability)==47 and not eigen.duplicated(['solution_id','eigenvalue_index']).any())
    for sid,r in pool.iterrows():
        a=r.sigma+mu;b=r.gamma+mu+r.d
        root=np.sqrt((a-b)**2+4*r.beta*r.sigma)
        expected=np.array([-mu,-mu,(-a-b-root)/2,(-a-b+root)/2])
        ev=eigen[eigen.solution_id==sid]
        assert close(np.sort(ev.real),np.sort(expected),atol=1e-13,rtol=1e-12) and ev.imag.eq(0).all()
        argument=np.where(ev.real.to_numpy(float)<0,np.pi,0.)
        margin=argument-r.alpha*np.pi/2
        assert close(ev.argument_abs,argument) and close(ev.threshold,r.alpha*np.pi/2) and close(ev.margin,margin)
        assert np.array_equal(ev.criterion_satisfied.to_numpy(bool),margin>0)
        cls='ASYMPTOTICALLY_STABLE_AUTONOMOUS_REFERENCE' if r.R0_reference<1 else 'UNSTABLE_AUTONOMOUS_REFERENCE'
        st=stability.loc[sid]
        assert st.classification==cls and close(st.max_eigenvalue_real,max(expected)) and close(st.min_matignon_margin,min(margin))
        assert st.admissible_1pct==r.admissible_1pct and st.theory_scope=='AUTONOMOUS_CONSTANT_N_REFERENCE_ONLY'
    check('closed_form_J4_spectrum_matches_saved_DFE_all47',True)
    check('32_admissible_all_stable_reference_44_full_stable3_unstable',int(admissible.sum())==32 and stability.loc[admissible,'classification'].eq('ASYMPTOTICALLY_STABLE_AUTONOMOUS_REFERENCE').all() and stability.classification.value_counts().to_dict()=={'ASYMPTOTICALLY_STABLE_AUTONOMOUS_REFERENCE':44,'UNSTABLE_AUTONOMOUS_REFERENCE':3})
    check('frozen_time_diagnostics_no_nonautonomous_proof',len(frozen)==47*264 and not frozen.duplicated(['solution_id','date']).any() and not frozen.nonautonomous_stability_proof.any())
    trend=p1report['population_trend']
    N=np.concatenate([train.population.to_numpy(float),np.exp(trend['intercept']+trend['slope']*np.arange(240,264))])
    expected_q=(lam/mu)/N
    for sid,frame in frozen.groupby('solution_id'):
        frame=frame.sort_values('date');r=pool.loc[sid]
        assert close(frame.q,expected_q,atol=1e-13,rtol=1e-13)
        assert close(frame.R0_frozen_time,frame.q*r.R0_reference,atol=1e-13,rtol=1e-13)
        a=r.sigma+mu;b=r.gamma+mu+r.d
        root=np.sqrt((a-b)**2+4*r.beta*r.sigma*frame.q.to_numpy(float))
        lambda_plus=(-a-b+root)/2
        assert close(frame.max_eigenvalue_real,np.maximum(-mu,lambda_plus),atol=1e-13,rtol=1e-12)
        minangle=np.where(lambda_plus<0,np.pi,0.)
        assert close(frame.min_matignon_margin,minangle-r.alpha*np.pi/2)
        classes=np.where(lambda_plus<0,'ASYMPTOTICALLY_STABLE_FROZEN_TIME_ONLY','UNSTABLE_FROZEN_TIME_ONLY')
        assert np.array_equal(frame.classification.to_numpy(),classes)
    check('all12408_frozen_time_rows_match_saved_forcing_and_analytic_identity',True)
    params=read('parameter_dispersion.csv')
    for label,frame in params.groupby('set'):
        if label=='FULL_DIAGNOSTIC_POOL':sub=pool
        else:sub=pool[pool.calibration_rmse<=primary_rmse*(1+float(label.split('_')[-2])/100)+1e-10]
        for r in frame.itertuples():
            values=sub[r.parameter].to_numpy(float)
            assert r.n==len(values)
            assert close([r.minimum,r.maximum,r.mean,r.std_population,r.cv],[values.min(),values.max(),values.mean(),values.std(),values.std()/abs(values.mean())])
    check('parameter_dispersion_reconstructed',True)
    dispersion=read('prediction_dispersion.csv')
    for label,frame in dispersion.groupby('set'):
        ids=set(pool[pool.source!='reoptimized_profile'].index) if label=='FIVE_ORIGINAL_SEEDS' else set(pool[admissible].index)
        for r in frame.itertuples():
            values=predictions[(predictions.solution_id.isin(ids))&(predictions.date==r.date)].predicted.to_numpy(float)
            assert r.n==len(values)
            assert close([r.minimum,r.maximum,r.mean,r.std_population,r.cv],[values.min(),values.max(),values.mean(),values.std(),values.std()/abs(values.mean())])
    check('prediction_dispersion_reconstructed',True)
    trace=(P3/'execution.log').read_text()
    check('execution_completion_and_report_consistent',trace.count('success=True')==46 and 'PHASE_3_COMPLETE' in trace and report['pool_size']==47 and report['new_fits']==46 and report['rejected_candidates']==int(pool.rejected_candidates.sum()))
    check('all_source_artifacts_unchanged_during_audit',all(sha(P3/p)==h for p,h in before.items()))
    best=pool.loc[pool.calibration_rmse.idxmin()]
    alpha_eligible=alpha[alpha.admissible_1pct]
    summary=dict(verdict='PHASE3_PASS_WITH_DOCUMENTED_LIMITATIONS',primary_R0_reference=float(pool.loc['primary_20260815','R0_reference']),
        admissible_solutions=int(admissible.sum()),admissible_R0_min=float(pool.loc[admissible,'R0_reference'].min()),admissible_R0_max=float(pool.loc[admissible,'R0_reference'].max()),
        full_pool_solutions=len(pool),full_R0_min=float(pool.R0_reference.min()),full_R0_max=float(pool.R0_reference.max()),
        primary_RMSE_reference=primary_rmse,threshold_1pct=threshold,best_explored_RMSE=float(best.calibration_rmse),
        primary_minus_best=float(primary_rmse-best.calibration_rmse),primary_minus_best_percent=float(100*(primary_rmse-best.calibration_rmse)/primary_rmse),
        alpha_admissible_sampled_range=[float(alpha_eligible.alpha.min()),float(alpha_eligible.alpha.max())],
        alpha_next_sampled_excluded=float(alpha[~alpha.admissible_1pct].alpha.min()),admissibility_unchanged_hquarter=True,
        max_saved_step_relative_difference=float(num.max_pointwise_relative_change.max()),
        theory_scope='Autonomous constant-N reference; no proved stability of time-varying N(t) model',
        protocol_decisions_recorded_before_phase3_execution=True,protocol_decisions_before_phase1_or_phase2=False,
        author_adoption_of_available_protocol='2026-10-10; retrospective documentary adoption',
        original_protocol_search_closed=True,global_calibration_reused=True,original_protocol_equivalence_asserted=False,
        new_optimizations=0,new_solver_simulations=0,new_R0_DFE_experiments=0,
        verification_method='Static source inspection and arithmetic reconstruction of existing tables; no execution of scientific runner',
        raw_fine_grid_state_arrays_saved=False,
        limitations=['Local session chronology is not independently timestamp-certified; predates phase3 run, not prior phase1/2 results.',
        'DE profiles approximate minima; optimizer convergence does not establish uniqueness or exhaustive identification.',
        'Near-boundary alpha and sparse gap .52-.55 do not locate a continuous confidence or identifiability interval.',
        'R0 envelope covers 32 finite explored solutions; not a confidence interval or exhaustive admissible-set bound.',
        'DFE reference stability does not prove nonautonomous stability with N(t); frozen-time spectra are descriptive.',
        'Full fine-grid state arrays are not archived; 115 controls are supported by checkpoints and reproducible source, not an independent solver rerun in this audit.',
        'No full phase3 output manifest sealed before this audit; previous source/pool hashes and redundant tables/checkpoints are verified.'])
    OUT.mkdir()
    (OUT/'audit_evidence.json').write_text(json.dumps(dict(summary=summary,checks=CHECKS,chronology=events),indent=2)+'\n')
    (OUT/'source_sha256_at_audit.json').write_text(json.dumps(before,indent=2)+'\n')
    (OUT/'chronology_fragments.jsonl').write_text(''.join(fragments))
    shutil.copy2(__file__,OUT/Path(__file__).name)
    source_copy=OUT/'existing_phase3_evidence';source_copy.mkdir()
    for rel in before:
        target=source_copy/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P3/rel,target)
        assert sha(target)==before[rel]
    with (OUT/'conformity_checks.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['check','status','detail'])
        for row in CHECKS:writer.writerow([row['check'],row['status'],json.dumps(row['detail']) if row['detail'] is not None else ''])
    (OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    main()
