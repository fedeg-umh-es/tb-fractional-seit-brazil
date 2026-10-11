"""Tests for the deliberate seed-contract guard in tb_seit.calibration.

docs/MODEL_CONTRACT.md documents the POLICY that one literal canonical seed and four literal
diagnostic seeds must be fixed, but never states the actual integers. Per this task's own
instruction ("If seeds are not explicitly defined: STOP rather than selecting arbitrary
values"), tb_seit.calibration.run_differential_evolution must refuse to run without an explicit
seed, and must never silently substitute a default.
"""

from __future__ import annotations

import inspect
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import calibration  # noqa: E402


def _dummy_kwargs(seed):
    return dict(
        observed_flow=[100.0] * 6,
        lambda_=1000.0,
        mu=0.001,
        N_of_t=lambda _t: 1_000_000.0,
        N0=1_000_000.0,
        flow0=100.0,
        h=1.0,
        bounds=[(0.01, 1.0), (0.01, 0.5), (0.05, 0.30), (0.0001, 0.05)],
        fixed_alpha=1.0,
        seed=seed,
    )


def test_seed_has_no_default_value():
    signature = inspect.signature(calibration.run_differential_evolution)
    assert signature.parameters["seed"].default is inspect.Parameter.empty


def test_missing_seed_argument_raises_type_error():
    kwargs = _dummy_kwargs(seed=0)
    del kwargs["seed"]
    with pytest.raises(TypeError):
        calibration.run_differential_evolution(**kwargs)


def test_explicit_none_seed_raises_seed_not_specified_error():
    with pytest.raises(calibration.SeedNotSpecifiedError):
        calibration.run_differential_evolution(**_dummy_kwargs(seed=None))


def test_de_hyperparameters_match_model_contract():
    assert calibration.STRATEGY == "best1bin"
    assert calibration.POPSIZE == 15
    assert calibration.MUTATION == (0.5, 1.0)
    assert calibration.RECOMBINATION == 0.7
    assert calibration.TOL == 0.01
    assert calibration.MAXITER == 1000


def test_explicit_integer_seed_runs_deterministically():
    """Same explicit seed -> identical result (reproducibility), using a cheap fixture."""
    run_a = calibration.run_differential_evolution(**_dummy_kwargs(seed=42))
    run_b = calibration.run_differential_evolution(**_dummy_kwargs(seed=42))
    assert run_a.beta == run_b.beta
    assert run_a.sigma == run_b.sigma
    assert run_a.gamma == run_b.gamma
    assert run_a.d == run_b.d
    assert run_a.objective == run_b.objective
