"""Authorized phase-2 ordinary-observation rolling-origin. All writes beside this file.

Run --check-baselines-only first; full run requires numerical_gate_report.json PASS.
No SARIMA fitting, alpha/bound search, additional seeds, or canonical writes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import scipy
from scipy.optimize import differential_evolution

OUT=Path(__file__).resolve().parent
REPO=OUT.parents[1]
sys.path.insert(0,str(REPO/'src'))
sys.path.insert(0,str(REPO/'audits/observation_operator_refit_phase1_2026-10-08/tb_global_refit_phase1'))
from tb_seit import calibration, data, model, rolling_origin as ro, seeds
from run_global_refit import ordinary_monthly_flow

ORIGINS=pd.date_range('2020-12-01','2021-12-01',freq='MS')
HORIZONS=list(range(1,13))
LABELS=['fractional','integer','persistence','seasonal_naive_12','SARIMA']
BASELINES=LABELS[2:]
BOUNDS_F=[(.01,1.),(.01,.5),(.05,.30),(.0001,.05),(.5,1.)]
SEED=20260815
H=1.
REL_TOL=.01


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def csv(name,rows):
    pd.DataFrame(rows).to_csv(OUT/name,index=False,float_format='%.17g')


def mvalues(obs,pred):
    error=np.asarray(pred)-np.asarray(obs)
    return dict(RMSE=float(np.sqrt(np.mean(error**2))),MAE=float(np.mean(abs(error))),bias=float(np.mean(error)))


def training(full,origin):
    df=full[full.date<=origin].copy().reset_index(drop=True)
    assert len(df)==240+(origin.year-2020)*12+origin.month-12
    assert df.date.max()==origin and df.date.min()==pd.Timestamp('2001-01-01')
    return ro.OriginTrainingSet(origin,df.date,df.cases.to_numpy(float),df.population.to_numpy(float),len(df))


def audit_support(df,full):
    assert len(df)==780 and not df.duplicated(['origin','horizon','model']).any()
    assert set(df.model)==set(LABELS)
    expected={(str(o.date()),h) for o in ORIGINS for h in HORIZONS}
    for label in LABELS:
        sub=df[df.model==label]
        assert len(sub)==156 and set(zip(sub.origin,sub.horizon))==expected
    assert np.isfinite(df[['observed','predicted','residual']].to_numpy(float)).all()
    assert df.status.eq('ok').all()
    assert np.allclose(df.predicted-df.observed,df.residual,atol=1e-8,rtol=0)
    for row in df.itertuples():
        origin=pd.Timestamp(row.origin); target=origin+pd.DateOffset(months=row.horizon)
        assert pd.Timestamp(row.target_date)==target
        assert row.observed==float(full.set_index('date').loc[target,'cases'])
        assert pd.Timestamp(row.train_start)==pd.Timestamp('2001-01-01')
        assert pd.Timestamp(row.train_end)==origin and int(row.n_train)==len(full[full.date<=origin])


def verify_baselines(full):
    path=REPO/'outputs/forecasting/rolling_origin_predictions.csv'
    original=pd.read_csv(path,float_precision='round_trip')
    audit_support(original,full)
    checks=[]
    for origin in ORIGINS:
        ts=training(full,origin)
        for label in BASELINES:
            sub=original[(original.origin==str(origin.date()))&(original.model==label)].sort_values('horizon')
            if label=='persistence': assert np.array_equal(sub.predicted.to_numpy(float),np.full(12,ts.train_cases[-1]))
            if label=='seasonal_naive_12': assert np.array_equal(sub.predicted.to_numpy(float),ts.train_cases[-12:])
            checks.append(dict(model=label,origin=str(origin.date()),n_forecasts=12,dates_support_observations='PASS',
                source_status='ok',protocol='Expanding train ending at origin; fixed original baseline definition',reuse=True))
    metadata=json.loads((REPO/'outputs/forecasting/sarima_frozen_order.json').read_text())
    assert metadata['selection_data']=='2001-01 to 2020-12 (canonical calibration only)'
    assert metadata['selected_order']==dict(p=0,d=1,q=2)
    assert metadata['selected_seasonal_order']==dict(P=1,D=1,Q=1,s=12)
    report=dict(status='PASS',source=str(path),source_sha256=sha(path),rows_reused=468,
        models_reused=BASELINES,source_commit='b3ad21bb059eb5357742693a4d5072107dc0df63',
        original_code_protocol='scripts/run_rolling_origin_forecast.py fits SARIMA on ts.train_cases from date<=origin, frozen order; persistence and seasonal naive use only ts.train_cases',
        evidence_manifest='outputs/EVIDENCE_MANIFEST.csv; canonical EV16/EV17/EV18 attest this source/protocol',
        sarima_order=metadata['selected_order'],sarima_seasonal_order=metadata['selected_seasonal_order'],
        sarima_limitation='Saved SARIMA coefficients per origin unavailable; provenance verified by immutable original code, data, recorded training dates, frozen order and archived prediction artifact. No new SARIMA fit or independent coefficient reconstruction.',
        checks=checks,input_sha256={p:sha(REPO/p) for p in ['outputs/forecasting/rolling_origin_predictions.csv',
            'outputs/forecasting/sarima_frozen_order.json','docs/SARIMA_BASELINE_CONTRACT.md',
            'scripts/run_rolling_origin_forecast.py','src/tb_seit/rolling_origin.py','data/raw/tb_mes.xlsx',
            'outputs/EVIDENCE_MANIFEST.csv','results_canonical/00_manifest/CANONICAL_EVIDENCE_MANIFEST.csv']})
    (OUT/'baseline_reuse_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    csv('baseline_reuse_checks.csv',checks)
    return original,original[original.model.isin(BASELINES)].copy(),report


def check_integrity():
    tracked=json.loads((OUT/'tracked_before_sha256.json').read_text())
    phase1=json.loads((OUT/'preserve_phase1_sha256.json').read_text())
    assert all(sha(REPO/p)==h for p,h in tracked.items()), 'Tracked file changed'
    assert all(sha(REPO/p)==h for p,h in phase1.items()), 'Phase-1 artifact changed'


def derive_tables(df):
    values=[]
    for label in LABELS:
        for h in HORIZONS:
            sub=df[(df.model==label)&(df.horizon==h)]
            assert len(sub)==13
            values.append(dict(model=label,horizon=h,n_forecasts=13,**mvalues(sub.observed,sub.predicted)))
    metric=pd.DataFrame(values)
    skill=[]
    for label in ['fractional','integer']:
        references=BASELINES+(['integer'] if label=='fractional' else [])
        for baseline in references:
            for h in HORIZONS:
                a=metric[(metric.model==label)&(metric.horizon==h)].iloc[0]
                b=metric[(metric.model==baseline)&(metric.horizon==h)].iloc[0]
                for name in ['RMSE','MAE']:
                    assert b[name]>0
                    skill.append(dict(model=label,baseline=baseline,horizon=h,metric=name,
                        error_model=a[name],error_baseline=b[name],skill=1-a[name]/b[name],n_forecasts=13))
    skill=pd.DataFrame(skill)
    horizon=[]
    for (label,baseline,name),sub in skill.groupby(['model','baseline','metric']):
        sub=sub.sort_values('horizon'); flags=(sub.skill.to_numpy()>0)
        hrelax=max((h for h,flag in zip(HORIZONS,flags) if flag),default=0)
        hstrict=0
        for flag in flags:
            if not flag: break
            hstrict+=1
        horizon.append(dict(model=label,baseline=baseline,metric=name,H_relax=hrelax,H_strict=hstrict))
    return metric,skill,pd.DataFrame(horizon)


def run(full):
    assert json.loads((OUT/'numerical_gate_report.json').read_text())['status']=='PASS'
    check_integrity()
    assert seeds.PRIMARY_SEED==SEED and ro.PRIMARY_H==H
    assert calibration.STRATEGY=='best1bin' and calibration.POPSIZE==15 and calibration.MAXITER==1000
    assert calibration.MUTATION==(.5,1.) and calibration.RECOMBINATION==.7 and calibration.TOL==.01
    assert not (OUT/'rolling_origin_predictions.csv').exists() and not (OUT/'fit_states.csv').exists(), 'Refusing duplicate execution'
    original,baselines,reuse=verify_baselines(full)
    mu=json.loads((REPO/'outputs/model_constants.json').read_text())['mu']['value']
    rows=baselines.to_dict(orient='records')
    for row in rows:
        row.update(observation_operator='baseline_original_saved',prediction_source_sha256=reuse['source_sha256'])
    fitrows,leakage,numchecks,stepforecasts=[],[],[],[]
    for origin in ORIGINS:
        ts=training(full,origin)
        trend=ro.fit_origin_population_trend(ts)
        N_of_t=ro.make_origin_N_of_t(ts,trend)
        lam=mu*ts.train_population.mean()
        N0,flow0=float(ts.train_population[0]),float(ts.train_cases[0])
        train_hash=hashlib.sha256(ts.train_cases.tobytes()+ts.train_population.tobytes()).hexdigest()
        origin_forecasts=[]
        for label in ['fractional','integer']:
            integer=label=='integer'
            def parameters(x):
                return model.SeitParameters(*map(float,x),**({'alpha':1.} if integer else {}))
            def simulate(p,months,h):
                sim=model.simulate(p,lam,mu,N_of_t,N0,flow0,months,h)
                return sim,ordinary_monthly_flow(sim.solver,p.sigma,months,h)
            invalid_candidates=0
            def objective(x):
                nonlocal invalid_candidates
                try:
                    sim,pred=simulate(parameters(x),ts.n_train,H)
                    if sim.solver.status!='ok' or not np.all(np.isfinite(pred)):
                        invalid_candidates+=1
                        return calibration.LARGE_PENALTY
                    return mvalues(ts.train_cases,pred)['RMSE']
                except (FloatingPointError,ValueError,OverflowError,RuntimeError):
                    invalid_candidates+=1
                    return calibration.LARGE_PENALTY
            result=differential_evolution(objective,bounds=BOUNDS_F[:4] if integer else BOUNDS_F,
                strategy=calibration.STRATEGY,popsize=calibration.POPSIZE,mutation=calibration.MUTATION,
                recombination=calibration.RECOMBINATION,tol=calibration.TOL,maxiter=calibration.MAXITER,
                seed=SEED,polish=False)
            fit=dict(origin=str(origin.date()),model=label,seed=SEED,**vars(parameters(result.x)),
                success=bool(result.success),message=str(result.message),iterations=int(result.nit),
                function_evaluations=int(result.nfev),objective_train_RMSE=float(result.fun),
                rejected_candidates=invalid_candidates,n_train=ts.n_train,train_sha256=train_hash,
                mu=mu,Lambda=float(lam),N0=N0,flow0=flow0,population_trend_intercept=trend.intercept,
                population_trend_slope=trend.slope,h_solver=H)
            fitrows.append(fit);csv('fit_states.csv',fitrows)
            if not result.success or not np.isfinite(result.fun) or result.fun>=calibration.LARGE_PENALTY:
                raise RuntimeError(f'STOP optimization failure: {origin.date()}/{label}: {result.message}')
            p=parameters(result.x)
            fit['initial_state']=json.dumps(model.initial_conditions(p,mu,N0,flow0).tolist())
            curves=[]
            for h in (1.,.5,.25):
                sim,pred=simulate(p,ts.n_train+12,h)
                if sim.solver.status!='ok' or not np.all(np.isfinite(pred)) or not np.all(pred>0):
                    raise RuntimeError(f'STOP numerical failure: {origin.date()}/{label}/step={h}')
                if h==1.:
                    assert np.isclose(mvalues(ts.train_cases,pred[:ts.n_train])['RMSE'],result.fun,atol=1e-6,rtol=1e-10)
                curves.append(pred)
                for horizon,val in zip(HORIZONS,pred[ts.n_train:]):
                    stepforecasts.append(dict(origin=str(origin.date()),model=label,horizon=horizon,h_solver=h,predicted=val))
            a,b,c=curves
            max_rel=float(np.max(abs(a-c)/np.maximum(abs(c),1.)))
            d1=float(np.max(abs(a-b))); d2=float(np.max(abs(b-c)))
            mae0=mvalues(ts.train_cases,a[:ts.n_train]);maef=mvalues(ts.train_cases,c[:ts.n_train])
            metric_rel=max(abs(mae0[k]-maef[k])/max(abs(maef[k]),1.) for k in ['RMSE','MAE'])
            passed=max_rel<=REL_TOL and metric_rel<=REL_TOL and d2<=d1+1e-9
            numchecks.append(dict(origin=str(origin.date()),model=label,alpha=p.alpha,
                max_relative_change=max_rel,max_absolute_change=float(np.max(abs(a-c))),
                half_difference=d1,quarter_difference=d2,train_metric_relative_change=metric_rel,tolerance=REL_TOL,status='PASS' if passed else 'FAIL'))
            csv('origin_numerical_checks.csv',numchecks)
            csv('origin_step_forecasts.csv',stepforecasts)
            if not passed: raise RuntimeError(f'STOP fitted-origin numerical gate: {origin.date()}/{label}')
            origin_forecasts.append((label,a[ts.n_train:]))
            leakage.append(dict(origin=str(origin.date()),model=label,train_start=str(ts.train_dates.min().date()),
                train_end=str(ts.train_dates.max().date()),n_train=ts.n_train,training_hash=train_hash,
                population_fit_max_date=str(ts.train_dates.max().date()),Lambda_max_date=str(ts.train_dates.max().date()),
                initial_condition_source_date=str(ts.train_dates.min().date()),target_values_used_in_objective=False,
                seed=SEED,observation_operator='ordinary_composite_trapezoid',status='PASS'))
            csv('fit_states.csv',fitrows);csv('leakage_checks.csv',leakage)
            check_integrity()
            print(f'{origin.date()} {label}: success=True; alpha={p.alpha:.9f}; train RMSE={result.fun:.6f}; iterations={result.nit}; nfev={result.nfev}; numerical_gate=PASS',flush=True)
        # Target observations are retrieved only after both models' fits/forecasts exist.
        for label,pred in origin_forecasts:
            for horizon,value in zip(HORIZONS,pred):
                target=origin+pd.DateOffset(months=horizon)
                observed=float(full.set_index('date').loc[target,'cases'])
                rows.append(dict(origin=str(origin.date()),target_date=str(target.date()),horizon=horizon,model=label,
                    observed=observed,predicted=float(value),residual=float(value-observed),
                    train_start=str(ts.train_dates.min().date()),train_end=str(ts.train_dates.max().date()),n_train=ts.n_train,
                    seed=SEED,population_source='TRAIN_ONLY_EXTRAPOLATION',status='ok',
                    observation_operator='ordinary_composite_trapezoid',prediction_source_sha256='NEW_PHASE2_FIT'))
        csv('predictions_checkpoint.csv',rows)
    predictions=pd.DataFrame(rows).sort_values(['origin','model','horizon']).reset_index(drop=True)
    audit_support(predictions,full)
    assert len(fitrows)==26 and len(leakage)==26 and len(numchecks)==26
    predictions.to_csv(OUT/'rolling_origin_predictions.csv',index=False,float_format='%.17g')
    metric,skill,summary=derive_tables(predictions)
    metric.to_csv(OUT/'metrics_by_horizon.csv',index=False,float_format='%.17g')
    skill.to_csv(OUT/'skill_by_horizon.csv',index=False,float_format='%.17g')
    summary.to_csv(OUT/'horizon_summary.csv',index=False)
    historical_metric, historical_skill,historical_summary=derive_tables(original)
    comparison=metric.merge(historical_metric,on=['model','horizon','n_forecasts'],suffixes=('_ordinary','_historical'))
    for k in ['RMSE','MAE','bias']: comparison[f'delta_{k}']=comparison[f'{k}_ordinary']-comparison[f'{k}_historical']
    comparison.to_csv(OUT/'historical_metrics_comparison.csv',index=False,float_format='%.17g')
    sk=skill.merge(historical_skill,on=['model','baseline','horizon','metric','n_forecasts'],suffixes=('_ordinary','_historical'))
    sk['delta_skill']=sk.skill_ordinary-sk.skill_historical
    sk['positive_sign_changed']=(sk.skill_ordinary>0)!=(sk.skill_historical>0)
    sk.to_csv(OUT/'historical_skill_comparison.csv',index=False,float_format='%.17g')
    summary.merge(historical_summary,on=['model','baseline','metric'],suffixes=('_ordinary','_historical')).to_csv(OUT/'historical_horizon_comparison.csv',index=False)
    # Check that independent derivation recovers the immutable canonical metric tables.
    canonical=pd.read_csv(REPO/'results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv').set_index(['model','horizon'])
    reconstructed=historical_metric.set_index(['model','horizon'])
    for k in ['RMSE','MAE','bias']: assert np.allclose(reconstructed[k],canonical.reindex(reconstructed.index)[k],atol=1e-8,rtol=1e-10)
    check_integrity()
    report=dict(status='COMPLETED_PHASE_2_PENDING_AUTHOR_REVIEW',commit='b3ad21bb059eb5357742693a4d5072107dc0df63',
        branch=subprocess.check_output(['git','-C',str(REPO),'branch','--show-current'],text=True).strip(),
        repository=str(REPO),predictions=780,common_pairs_per_model=156,origins=13,horizons=HORIZONS,
        fits=26,all_fits_success=True,all_fitted_origin_numeric_gates_passed=True,seed=SEED,bounds=BOUNDS_F,
        h_solver=H,observation='Ordinary sigma*E corrected-grid composite trapezoids',baseline_fits_executed=0,
        baseline_reuse_verification='baseline_reuse_verification.json',leakage_checks='leakage_checks.csv',
        parameters_saved='fit_states.csv',alpha_min=float(min(r['alpha'] for r in fitrows if r['model']=='fractional')),
        alpha_max=float(max(r['alpha'] for r in fitrows if r['model']=='fractional')),
        numerical_gate='numerical_gate_report.json',python=sys.version,numpy=np.__version__,scipy=scipy.__version__,
        integrity='All tracked and phase1 files unchanged',inference='DESCRIPTIVE_ONLY',
        R0_identifiability_DFE_recomputed=False,manuscript_updated=False,PR3_updated=False,
        decision='AUTHOR_REVIEW_REQUIRED; PR3_AND_COMPILATION_REMAIN_BLOCKED')
    (OUT/'phase2_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(summary.to_string(index=False))
    print('PHASE_2 = COMPLETE; 780 predictions; no manuscript/PR edits, commit, push or merge',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-baselines-only',action='store_true')
    args=parser.parse_args()
    full=data.load_canonical_dataset().full
    if args.check_baselines_only:
        verify_baselines(full);print('BASELINE_REUSE_GATE = PASS; 468 saved forecasts, same support/protocol')
    else:
        run(full)
