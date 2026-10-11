import numpy as np
import pandas as pd
import pytest
import run_phase3 as a


@pytest.fixture
def inputs():
    ds=a.data.load_canonical_dataset()
    return ds,a.context(ds),a.primary_parameters()


def test_primary_reproduces_phase1_objective(inputs):
    _,ctx,primary=inputs
    assert a.objective(primary,ctx)==pytest.approx(619.3187514936859,abs=1e-7)


def test_validation_perturbation_cannot_change_cost_or_population(inputs):
    ds,ctx,primary=inputs
    full=ds.full.copy()
    full.loc[full.date>a.data.CALIBRATION_END,['cases','population']]*=1000
    changed=a.data.CanonicalDataset(full,ds.calibration.copy(),full.iloc[240:].reset_index(drop=True))
    other=a.context(changed)
    assert ctx['train_sha256']==other['train_sha256']
    assert np.array_equal(ctx['obs'],other['obs'])
    assert a.objective(primary,ctx)==a.objective(primary,other)
    assert np.array_equal([ctx['N_of_t'](t) for t in [0,120,239,240,264]],
                          [other['N_of_t'](t) for t in [0,120,239,240,264]])


def test_grids_preserve_bounds_and_cover_alpha_endpoints(inputs):
    _,_,p=inputs
    for k in ['beta','gamma','d','alpha']:
        grid=a.profile_grid(k,p)
        lo,hi=a.BOUNDS[k]
        assert all(lo<=v<=hi for v in grid)
        assert p[k] in grid and grid==sorted(set(grid))
        assert len(grid)==(21 if k=='alpha' else 7)
    assert a.profile_grid('alpha',p)[0]==.5
    assert a.profile_grid('alpha',p)[-1]==1.


def test_dfe_solves_epidemiological_rhs_at_all_forcing_times(inputs):
    _,ctx,p=inputs
    equilibrium=np.array([ctx['mc'].lambda_/ctx['mc'].mu,0,0,0,0])
    for t in [0.,120.,239.,264.]:
        rhs=a.model.seit_rhs(t,equilibrium,a.model.SeitParameters(**p),ctx['mc'].lambda_,ctx['mc'].mu,ctx['N_of_t'])
        assert np.allclose(rhs,0,atol=1e-10,rtol=0)


def test_full_jacobian_matches_independent_central_differences(inputs):
    _,ctx,p=inputs
    equilibrium=np.array([ctx['mc'].lambda_/ctx['mc'].mu,0,0,0,0])
    for t in [0.,120.,239.]:
        columns=[]
        for index in range(4):
            delta=np.zeros(5)
            delta[index]=1.
            high=a.model.seit_rhs(t,equilibrium+delta,a.model.SeitParameters(**p),ctx['mc'].lambda_,ctx['mc'].mu,ctx['N_of_t'])
            low=a.model.seit_rhs(t,equilibrium-delta,a.model.SeitParameters(**p),ctx['mc'].lambda_,ctx['mc'].mu,ctx['N_of_t'])
            columns.append((high[:4]-low[:4])/2)
        finite=np.array(columns).T
        q=equilibrium[0]/ctx['N_of_t'](t)
        assert np.allclose(finite,a.jacobian(p,ctx['mc'].mu,q),atol=1e-10,rtol=1e-9)
        assert finite[3,2]==pytest.approx(p['gamma'])


def test_next_generation_spectral_radius_and_scale_cancellation(inputs):
    _,ctx,p=inputs
    mu=ctx['mc'].mu
    r0=a.r0.r0_diagnostic(p['beta'],p['sigma'],p['gamma'],p['d'],mu)
    for q in [.8,1.,1.2]:
        for scale in [.1,1.,10.]:
            radius=np.max(abs(np.linalg.eigvals(a.next_generation(p,mu,q,scale))))
            assert radius==pytest.approx(q*r0,rel=1e-13)


def test_real_eigenvalue_threshold_and_matignon_cases(inputs):
    _,ctx,p=inputs
    mu=ctx['mc'].mu
    critical=(p['sigma']+mu)*(p['gamma']+mu+p['d'])/p['sigma']
    for alpha in [.5,p['alpha'],1.]:
        for factor,wanted in [(.8,'ASYMPTOTICALLY_STABLE_AUTONOMOUS_REFERENCE'),
                              (1.,'NONHYPERBOLIC_OR_SECTOR_BOUNDARY'),
                              (1.2,'UNSTABLE_AUTONOMOUS_REFERENCE')]:
            pp={**p,'alpha':alpha,'beta':critical*factor}
            cls,eig,_=a.stability(pp,mu)
            assert cls==wanted and np.max(abs(eig.imag))==0


def test_auxiliary_observation_zero_eigenvalue_is_not_epidemiological_instability(inputs):
    _,ctx,p=inputs
    J=a.jacobian(p,ctx['mc'].mu)
    augmented=np.zeros((5,5))
    augmented[:4,:4]=J
    augmented[4,1]=p['sigma']
    assert min(abs(np.linalg.eigvals(augmented)))==0
    assert min(abs(np.linalg.eigvals(J)))>0
    assert a.stability(p,ctx['mc'].mu)[0]=='ASYMPTOTICALLY_STABLE_AUTONOMOUS_REFERENCE'


def test_constant_matignon_matrix_differs_from_time_varying_implementation(inputs):
    _,ctx,p=inputs
    sstar=ctx['mc'].lambda_/ctx['mc'].mu
    first=a.jacobian(p,ctx['mc'].mu,sstar/ctx['N_of_t'](0))
    last=a.jacobian(p,ctx['mc'].mu,sstar/ctx['N_of_t'](239))
    assert first[1,2]!=last[1,2]
    assert first[3,2]==last[3,2]==p['gamma']
