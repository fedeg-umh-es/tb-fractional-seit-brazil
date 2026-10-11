"""Mandatory phase-2 gate. Frozen phase-1 parameters only; NO calibration."""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import scipy

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PHASE1 = REPO/'audits/observation_operator_refit_phase1_2026-10-08'
FITDIR = PHASE1/'tb_global_refit_phase1/results_global_primary'
STEPS = (1., .5, .25)
REL_TOL = .01
REPRO_ATOL = 1e-6
REPRO_RTOL = 1e-10


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def metrics(obs, pred):
    err = pred-obs
    return dict(rmse=float(np.sqrt(np.mean(err**2))), mae=float(np.mean(abs(err))), bias=float(np.mean(err)))


def main():
    assert subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip()=='b3ad21bb059eb5357742693a4d5072107dc0df63'
    assert subprocess.run(['git','-C',str(REPO),'diff','--quiet']).returncode==0
    tracked=json.loads((PHASE1/'integrity_before.json').read_text())
    manifest=json.loads((PHASE1/'artifact_manifest.json').read_text())
    assert all(sha(REPO/p)==h for p,h in tracked.items()), 'Tracked integrity failure'
    assert all(sha(PHASE1/p)==h for p,h in manifest.items()), 'Phase-1 artifact integrity failure'
    package=json.loads((PHASE1/'package_provenance.json').read_text())
    assert sha(PHASE1/'tb_global_refit_phase1/run_global_refit.py')==package['executed_script_sha256']
    controls=json.loads((PHASE1/'control_worktrees_before.json').read_text())
    for base,record in controls.items():
        assert all(sha(Path(base)/p)==h for p,h in record['sha256'].items())
        assert subprocess.check_output(['git','-C',base,'rev-parse','HEAD'],text=True).strip()==record['head']
        assert subprocess.check_output(['git','-C',base,'status','--short'],text=True)==record['status']
    preservation={str(p.relative_to(REPO)):sha(p) for p in PHASE1.rglob('*') if p.is_file()}
    (HERE/'preserve_phase1_sha256.json').write_text(json.dumps(preservation,indent=2)+'\n')
    (HERE/'tracked_before_sha256.json').write_text(json.dumps(tracked,indent=2)+'\n')

    command=[sys.executable,'-m','pytest','-q','-p','no:cacheprovider',str(PHASE1/'tb_global_refit_phase1/test_global_refit.py')]
    test=subprocess.run(command,capture_output=True,text=True)
    (HERE/'phase1_tests_reverified.json').write_text(json.dumps(dict(command=command,exit_code=test.returncode,stdout=test.stdout,stderr=test.stderr),indent=2)+'\n')
    assert test.returncode==0, 'Supplied phase-1 tests failed'
    sys.path.insert(0,str(PHASE1/'tb_global_refit_phase1'))
    from run_global_refit import ordinary_monthly_flow
    sys.path.insert(0,str(REPO/'src'))
    from tb_seit import constants,data,model,population
    ds=data.load_canonical_dataset()
    series,trend=population.build_population_exogenous_series(ds)
    N_of_t=population.make_N_of_t(series)
    mc=constants.compute_model_constants(ds.calibration.population)
    N0,flow0=float(ds.calibration.population.iloc[0]),float(ds.calibration.cases.iloc[0])
    obs=ds.full.cases.to_numpy(float)
    fits=pd.read_csv(FITDIR/'global_refit_parameters.csv').set_index('model')
    assert fits.success.all() and fits.seed.eq(20260815).all()
    phase1_metrics=pd.read_csv(FITDIR/'global_refit_metrics.csv')
    numerical, predictions, reproduction, quadrature=[],[],[],[]
    sims={}
    for label in ('fractional','integer'):
        p=model.SeitParameters(**{k:float(fits.loc[label,k]) for k in ['beta','sigma','gamma','d','alpha']})
        for h in STEPS:
            sim=model.simulate(p,mc.lambda_,mc.mu,N_of_t,N0,flow0,264,h)
            assert sim.solver.status=='ok', f'{label}/h={h}: {sim.solver.status}'
            assert np.allclose(np.diff(sim.solver.t),h,atol=1e-12,rtol=0)
            before=hashlib.sha256(sim.solver.y.tobytes()).hexdigest()
            pred=ordinary_monthly_flow(sim.solver,p.sigma,264,h)
            assert np.all(np.isfinite(pred)) and np.all(pred>0)
            assert hashlib.sha256(sim.solver.y.tobytes()).hexdigest()==before
            # Independent use of actual t spacings, not the quadrature h argument.
            E=sim.solver.y[:,1]
            reference=(p.sigma*(E[:-1]+E[1:])/2*np.diff(sim.solver.t)).reshape(264,int(1/h)).sum(axis=1)
            assert np.max(abs(pred-reference))<1e-9
            for f in ('constant','linear'):
                y=sim.solver.y.copy()
                y[:,1]=1234. if f=='constant' else 1234.+3*sim.solver.t
                from types import SimpleNamespace
                expected=p.sigma*(np.full(264,1234.) if f=='constant' else 1234.+3*(np.arange(264)+.5))
                error=float(np.max(abs(ordinary_monthly_flow(SimpleNamespace(status='ok',y=y),p.sigma,264,h)-expected)))
                assert error<1e-9
                quadrature.append(dict(model=label,step=h,test=f,error=error,tolerance=1e-9,status='PASS'))
            sims[(label,h)]=pred
            for date,observed,predicted in zip(ds.full.date,obs,pred):
                predictions.append(dict(model=label,step=h,date=str(date.date()),observed=observed,predicted=predicted))
            if h==1.:
                saved=pd.read_csv(FITDIR/f'{label}_predictions.csv')
                assert np.array_equal(saved.observed.to_numpy(float),obs)
                assert np.array_equal(pd.to_datetime(saved.date).to_numpy(),ds.full.date.to_numpy())
                assert np.allclose(pred,saved.predicted,atol=REPRO_ATOL,rtol=REPRO_RTOL)
                reproduction.append(dict(model=label,max_prediction_delta=float(np.max(abs(pred-saved.predicted))),status='PASS'))
                for split,sl in [('calibration',slice(0,240)),('validation_open_loop',slice(240,264))]:
                    m=metrics(obs[sl],pred[sl]); old=phase1_metrics[(phase1_metrics.model==label)&(phase1_metrics.split==split)].iloc[0]
                    assert all(np.isclose(m[k],float(old[k]),atol=REPRO_ATOL,rtol=REPRO_RTOL) for k in m)
                    assert np.isclose(m['rmse'],float(fits.loc[label,'objective_train_rmse']),atol=REPRO_ATOL,rtol=REPRO_RTOL) if split=='calibration' else True
        for split,sl in [('calibration',slice(0,240)),('validation_open_loop',slice(240,264))]:
            coarse,middle,fine=[sims[(label,h)][sl] for h in STEPS]
            max_change=float(np.max(abs(coarse-fine)))
            max_rel=float(np.max(abs(coarse-fine)/np.maximum(abs(fine),1.)))
            d1=float(np.max(abs(coarse-middle))); d2=float(np.max(abs(middle-fine)))
            m0,mf=metrics(obs[sl],coarse),metrics(obs[sl],fine)
            metric_change={k:abs(m0[k]-mf[k])/max(abs(mf[k]),1.) for k in ('rmse','mae')}
            bias_change=abs(m0['bias']-mf['bias'])/float(np.mean(obs[sl]))
            passed=max_rel<=REL_TOL and all(v<=REL_TOL for v in metric_change.values()) and bias_change<=REL_TOL and d2<=d1+1e-9
            numerical.append(dict(model=label,alpha=p.alpha,split=split,max_prediction_change=max_change,
                max_pointwise_relative_change=max_rel,coarse_half_max_difference=d1,half_quarter_max_difference=d2,
                rmse_h1=m0['rmse'],rmse_hquarter=mf['rmse'],rmse_relative_change=metric_change['rmse'],
                mae_h1=m0['mae'],mae_hquarter=mf['mae'],mae_relative_change=metric_change['mae'],
                bias_relative_to_mean_observed_change=bias_change,tolerance=REL_TOL,status='PASS' if passed else 'FAIL'))
    pd.DataFrame(numerical).to_csv(HERE/'numerical_convergence.csv',index=False,float_format='%.17g')
    pd.DataFrame(predictions).to_csv(HERE/'frozen_parameter_step_predictions.csv',index=False,float_format='%.17g')
    pd.DataFrame(quadrature).to_csv(HERE/'quadrature_checks.csv',index=False,float_format='%.17g')
    assert all(sha(REPO/p)==h for p,h in tracked.items()) and all(sha(REPO/p)==h for p,h in preservation.items())
    passed=all(row['status']=='PASS' for row in numerical)
    report=dict(status='PASS' if passed else 'STOP_NUMERICAL_GATE_FAILURE',phase1_hashes_verified=True,
        phase1_untracked_files_preserved=True,tracked_file_count=len(tracked),tests_reverified=test.stdout,
        operator='Composite trapezoids of sigma*E corrected grid, independent ordinary integral; fractional dynamics unchanged',
        steps=list(STEPS),relative_tolerance_declared_before_execution=REL_TOL,
        rules='Max pointwise h1 vs h.25 relative difference <=1%; RMSE/MAE changes <=1%; bias change <=1% observed mean; h.5 to h.25 max change must decrease. Empirical resolution check, not proof of exact continuum error.',
        frozen_parameters=fits.reset_index().to_dict(orient='records'),reproduction=reproduction,numerical=numerical,
        python=sys.version,numpy=np.__version__,scipy=scipy.__version__,recalibrations_performed=0)
    (HERE/'numerical_gate_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(pd.DataFrame(numerical).to_string(index=False))
    print('NUMERICAL_GATE =',report['status'])
    if not passed:
        raise SystemExit(2)


if __name__=='__main__':
    main()
