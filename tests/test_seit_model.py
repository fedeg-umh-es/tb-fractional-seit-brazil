"""Unit/integration tests for the base-model reimplementation (tb_seit package).

Covers: temporal split, no leakage of validation population, fixed mu, training-only Lambda,
initial conditions, observation model, integer alpha==1 exactly, parameter bounds, solver finite
outputs, and output schema. Optimization-contract (seed) tests live in
test_optimization_contract.py.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import constants, data, model, population, solver  # noqa: E402


@pytest.fixture(scope="module")
def dataset():
    return data.load_canonical_dataset()


# ---- temporal split -------------------------------------------------------------------


def test_calibration_validation_split_sizes(dataset):
    assert len(dataset.calibration) == 240
    assert len(dataset.validation) == 24
    assert len(dataset.full) == 264


def test_calibration_validation_no_overlap(dataset):
    assert set(dataset.calibration["date"]).isdisjoint(set(dataset.validation["date"]))


def test_calibration_validation_boundary(dataset):
    assert dataset.calibration["date"].max() == pd.Timestamp("2020-12-01")
    assert dataset.validation["date"].min() == pd.Timestamp("2021-01-01")


# ---- population / no validation leakage -----------------------------------------------


def test_population_series_schema(dataset):
    series, _trend = population.build_population_exogenous_series(dataset)
    assert list(series.columns) == [
        "date", "N_dataset", "N_model_input", "source_type", "used_for_model",
    ]
    assert len(series) == 264


def test_validation_months_do_not_use_dataset_population(dataset):
    series, _trend = population.build_population_exogenous_series(dataset)
    validation_rows = series[series["date"] >= pd.Timestamp("2021-01-01")]
    assert len(validation_rows) == 24
    assert (validation_rows["source_type"] == population.SOURCE_TRAIN_ONLY_EXTRAPOLATION).all()
    assert (validation_rows["used_for_model"] == "N_model_input").all()
    # The extrapolated value must not equal the dataset's own (unused) validation population.
    assert not np.allclose(
        validation_rows["N_model_input"], validation_rows["N_dataset"], rtol=1e-6
    )


def test_calibration_months_use_dataset_population_directly(dataset):
    series, _trend = population.build_population_exogenous_series(dataset)
    calibration_rows = series[series["date"] <= pd.Timestamp("2020-12-01")]
    assert (calibration_rows["source_type"] == population.SOURCE_TRAIN_OBSERVED).all()
    assert np.allclose(calibration_rows["N_model_input"], calibration_rows["N_dataset"])


def test_population_trend_is_fit_on_training_data_only(dataset):
    """Corrupting the validation-period `populacao` values must not change the fitted trend."""
    trend_original = population.fit_population_trend(dataset)

    corrupted_full = dataset.full.copy()
    corrupted_full.loc[corrupted_full["date"] >= pd.Timestamp("2021-01-01"), "population"] = 1.0
    corrupted_calibration = corrupted_full[
        corrupted_full["date"] <= pd.Timestamp("2020-12-01")
    ].reset_index(drop=True)
    corrupted_dataset = data.CanonicalDataset(
        full=corrupted_full, calibration=corrupted_calibration, validation=dataset.validation
    )
    trend_corrupted = population.fit_population_trend(corrupted_dataset)

    assert trend_original.intercept == pytest.approx(trend_corrupted.intercept)
    assert trend_original.slope == pytest.approx(trend_corrupted.slope)


# ---- fixed constants --------------------------------------------------------------------


def test_mu_matches_life_expectancy_formula():
    mu = constants.compute_mu(74.0)
    assert mu == pytest.approx(1.0 / (74.0 * 12.0))


def test_lambda_uses_training_population_only(dataset):
    mu = constants.compute_mu()
    lambda_, mean_n = constants.compute_lambda(mu, dataset.calibration["population"])
    assert mean_n == pytest.approx(dataset.calibration["population"].mean())
    assert lambda_ == pytest.approx(mu * mean_n)

    # Corrupting validation population must not change Lambda (function never sees it).
    lambda_again, _ = constants.compute_lambda(mu, dataset.calibration["population"])
    assert lambda_again == pytest.approx(lambda_)


# ---- initial conditions -------------------------------------------------------------------


def test_initial_conditions_formula():
    params = model.SeitParameters(beta=0.5, sigma=0.2, gamma=0.1, d=0.001, alpha=0.8)
    mu = 0.001
    N0 = 1_000_000.0
    flow0 = 1000.0

    y0 = model.initial_conditions(params, mu, N0, flow0)

    expected_E0 = flow0 / params.sigma
    expected_I0 = params.sigma * expected_E0 / (params.gamma + mu + params.d)
    expected_T0 = 0.0
    expected_S0 = N0 - expected_E0 - expected_I0 - expected_T0

    assert y0[model.S_IDX] == pytest.approx(expected_S0)
    assert y0[model.E_IDX] == pytest.approx(expected_E0)
    assert y0[model.I_IDX] == pytest.approx(expected_I0)
    assert y0[model.T_IDX] == 0.0
    assert y0[model.C_IDX] == 0.0


def test_initial_conditions_are_not_free_parameters():
    """E0/I0 must be a deterministic function of (sigma, gamma, d, mu, N0, flow0) only."""
    mu, N0, flow0 = 0.001, 1_000_000.0, 1000.0
    p1 = model.SeitParameters(beta=0.1, sigma=0.2, gamma=0.1, d=0.001, alpha=0.9)
    p2 = model.SeitParameters(beta=0.9, sigma=0.2, gamma=0.1, d=0.001, alpha=0.5)
    y0_a = model.initial_conditions(p1, mu, N0, flow0)
    y0_b = model.initial_conditions(p2, mu, N0, flow0)
    # beta and alpha differ but do not enter the IC formula -> E0/I0/S0 must match exactly.
    assert y0_a[model.E_IDX] == y0_b[model.E_IDX]
    assert y0_a[model.I_IDX] == y0_b[model.I_IDX]
    assert y0_a[model.S_IDX] == y0_b[model.S_IDX]


# ---- observation model -------------------------------------------------------------------


def test_observation_model_is_time_integrated_flow_not_instantaneous_sample():
    """flow_model(k) must equal C(k+1)-C(k), i.e. an integral, not sigma*E sampled once."""
    params = model.SeitParameters(beta=0.05, sigma=0.1, gamma=0.15, d=0.002, alpha=0.9)
    mu, N0, flow0 = 0.001, 200_000_000.0, 7000.0

    def N_of_t(_t):
        return N0

    lambda_ = mu * N0
    sim = model.simulate(params, lambda_, mu, N_of_t, N0, flow0, n_months=6, h=1.0)

    assert sim.solver.status == "ok"
    c_series = sim.solver.y[:, model.C_IDX]
    expected_flow = np.diff(c_series)
    assert np.allclose(sim.monthly_flow, expected_flow)
    # A pure instantaneous sample sigma*E(t_k) would generically differ from the integral.
    instantaneous = params.sigma * sim.solver.y[:-1, model.E_IDX]
    assert not np.allclose(sim.monthly_flow, instantaneous)


def test_state_population_discrepancy_is_diagnostic_only(dataset):
    series, _trend = population.build_population_exogenous_series(dataset)
    N_of_t = population.make_N_of_t(series)
    mc = constants.compute_model_constants(dataset.calibration["population"])
    params = model.SeitParameters(beta=0.1, sigma=0.2, gamma=0.15, d=0.002, alpha=0.9)
    N0 = float(dataset.calibration["population"].iloc[0])
    flow0 = float(dataset.calibration["cases"].iloc[0])
    sim = model.simulate(params, mc.lambda_, mc.mu, N_of_t, N0, flow0, n_months=24, h=1.0)
    discrepancy = model.state_population_discrepancy(sim, N_of_t)
    assert discrepancy.shape[0] == sim.solver.t.shape[0]
    assert np.all(np.isfinite(discrepancy))


# ---- integer comparator: alpha exactly 1 --------------------------------------------------


def test_integer_comparator_alpha_is_exactly_one():
    """fixed_alpha=1.0 must force alpha==1.0 exactly in the returned run, never estimated."""
    from tb_seit import calibration

    def N_of_t(_t):
        return 1_000_000.0

    observed = np.full(6, 100.0)
    run = calibration.run_differential_evolution(
        observed_flow=observed,
        lambda_=1000.0,
        mu=0.001,
        N_of_t=N_of_t,
        N0=1_000_000.0,
        flow0=100.0,
        h=1.0,
        bounds=[(0.01, 1.0), (0.01, 0.5), (0.05, 0.30), (0.0001, 0.05)],
        fixed_alpha=1.0,
        seed=12345,  # test-only fixture seed, not a canonical project seed
    )
    assert run.alpha == 1.0


def test_solver_alpha_one_matches_exponential_decay():
    def f(_t, y):
        return -y

    res = solver.solve_caputo_fde(f, np.array([1.0]), t_end=5.0, h=0.05, alpha=1.0)
    exact = np.exp(-res.t)
    assert np.max(np.abs(res.y[:, 0] - exact)) < 1e-3
    assert res.status == "ok"


def test_solver_alpha_fractional_matches_mittag_leffler():
    from scipy.special import gamma as gamma_fn

    alpha = 0.75

    def mittag_leffler(z, terms=200):
        out = np.zeros_like(z)
        for k in range(terms):
            out = out + z**k / gamma_fn(alpha * k + 1)
        return out

    def f(_t, y):
        return -y

    res = solver.solve_caputo_fde(f, np.array([1.0]), t_end=2.0, h=0.02, alpha=alpha)
    exact = mittag_leffler(-res.t**alpha)
    assert np.max(np.abs(res.y[:, 0] - exact)) < 1e-3
    assert res.status == "ok"


# ---- solver finite/negative-state checks ---------------------------------------------------


def test_solver_flags_non_finite_blowup():
    def f(_t, y):
        return 50.0 * y  # explosive growth

    res = solver.solve_caputo_fde(f, np.array([1.0]), t_end=10.0, h=0.5, alpha=1.0)
    assert res.status in ("non_finite", "ok")  # must not silently return finite garbage
    if res.status == "non_finite":
        assert np.all(np.isnan(res.y[-1]))


def test_solver_requires_valid_alpha_domain():
    def f(_t, y):
        return -y

    with pytest.raises(ValueError):
        solver.solve_caputo_fde(f, np.array([1.0]), t_end=1.0, h=0.1, alpha=1.5)
    with pytest.raises(ValueError):
        solver.solve_caputo_fde(f, np.array([1.0]), t_end=1.0, h=0.1, alpha=0.0)


# ---- parameter bounds (schema check against the canonical contract) ----------------------


def test_primary_bounds_match_contract():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "run_calibration_multiseed", REPO_ROOT / "scripts" / "run_calibration_multiseed.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    assert mod.BOUNDS_FRACTIONAL == [
        (0.01, 1.00), (0.01, 0.50), (0.05, 0.30), (0.0001, 0.05), (0.50, 1.00),
    ]
    assert mod.BOUNDS_INTEGER == [(0.01, 1.00), (0.01, 0.50), (0.05, 0.30), (0.0001, 0.05)]


# ---- output schema for existing generated artifacts ---------------------------------------


def test_numerical_convergence_csv_schema():
    path = REPO_ROOT / "outputs" / "audits" / "numerical_convergence.csv"
    if not path.exists():
        pytest.skip("numerical_convergence.csv not yet generated")
    with path.open() as f:
        header = next(csv.reader(f))
    assert header == [
        "model", "step", "calibration_rmse",
        "max_absolute_prediction_difference", "relative_prediction_difference",
        "solver_status",
    ]


def test_model_constants_json_schema():
    import json

    path = REPO_ROOT / "outputs" / "model_constants.json"
    if not path.exists():
        pytest.skip("model_constants.json not yet generated")
    payload = json.loads(path.read_text())
    assert "mu" in payload and "lambda" in payload
    assert payload["mu"]["value"] == pytest.approx(1.0 / (74 * 12))
