"""Protocol tests before any authorized phase-2 optimization."""
import numpy as np
import pandas as pd
import pytest
from run_rolling_ordinary import training,audit_support,derive_tables,ORIGINS,HORIZONS,LABELS
from tb_seit import data,rolling_origin as ro


@pytest.mark.parametrize('origin',[ORIGINS[0],ORIGINS[6],ORIGINS[-1]])
def test_future_cases_and_population_cannot_change_training_inputs(origin):
    full=data.load_canonical_dataset().full
    changed=full.copy()
    changed.loc[changed.date>origin,['cases','population']]*=10
    a,b=training(full,origin),training(changed,origin)
    np.testing.assert_array_equal(a.train_cases,b.train_cases)
    np.testing.assert_array_equal(a.train_population,b.train_population)
    x,y=ro.fit_origin_population_trend(a),ro.fit_origin_population_trend(b)
    assert x==y
    N1,N2=ro.make_origin_N_of_t(a,x),ro.make_origin_N_of_t(b,y)
    t=np.arange(a.n_train+13)*.5
    np.testing.assert_array_equal([N1(v) for v in t],[N2(v) for v in t])


def saved():
    return pd.read_csv(data.REPO_ROOT/'outputs/forecasting/rolling_origin_predictions.csv',float_precision='round_trip')


def test_historical_support_is_exactly_156_pairs_per_model():
    df=saved();full=data.load_canonical_dataset().full
    audit_support(df,full)
    assert df.groupby('model').size().eq(156).all()


def test_support_rejects_missing_or_duplicate_pairs():
    full=data.load_canonical_dataset().full;df=saved()
    with pytest.raises(AssertionError): audit_support(df.iloc[1:],full)
    duplicate=pd.concat([df.iloc[:-1],df.iloc[[0]]],ignore_index=True)
    with pytest.raises(AssertionError): audit_support(duplicate,full)


def test_support_rejects_wrong_target_and_leaking_train_end():
    full=data.load_canonical_dataset().full;df=saved()
    df.loc[0,'target_date']='2020-12-01'
    with pytest.raises(AssertionError): audit_support(df,full)
    df=saved();df.loc[0,'train_end']='2021-01-01'
    with pytest.raises(AssertionError): audit_support(df,full)


def test_skill_and_horizons_keep_noncontiguous_positive_results_separate():
    rows=[]
    for label in LABELS:
        for h in HORIZONS:
            # Baseline error 10; fractional error 5 at h1,h3 and 15 otherwise.
            error=(5 if h in (1,3) else 15) if label=='fractional' else 10
            rows.extend(dict(model=label,horizon=h,observed=100,predicted=100+error) for _ in range(13))
    metrics,skill,horizons=derive_tables(pd.DataFrame(rows))
    sub=horizons[(horizons.model=='fractional')&(horizons.baseline=='persistence')]
    assert sub.H_relax.eq(3).all() and sub.H_strict.eq(1).all()
    assert skill[(skill.model=='fractional')&(skill.horizon==2)].skill.lt(0).all()
    assert metrics.n_forecasts.eq(13).all()
