"""Tests for the practical-identifiability audit (IDENTIFIABILITY_AUDIT_REPORT.md).

Covers: R0 diagnostic formula, all five canonical seeds present, primary seed unchanged,
profile-objective calibration-only data usage, no validation leakage into optimization, raw
source immutability, residual-sign accounting, and output schemas for the audit's CSV artifacts.
"""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import r0, seeds  # noqa: E402

RAW_DATASET = REPO_ROOT / "data" / "raw" / "tb_mes.xlsx"
RAW_MANUSCRIPT = REPO_ROOT / "manuscript" / "source" / "BIOMATEMATICA_UNICAMP.docx"
DATASET_SHA256 = "93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b"
MANUSCRIPT_SHA256 = "10e652628a7786460243fd47201bbfef498356fcee9766ce3fab48f64fa4ac88"


def _load_module(name: str, relpath: str):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / relpath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---- R0 diagnostic formula --------------------------------------------------------------


def test_r0_diagnostic_formula():
    beta, sigma, gamma, d, mu = 0.1, 0.02, 0.1, 0.001, 0.001
    expected = (beta * sigma) / ((sigma + mu) * (gamma + mu + d))
    assert r0.r0_diagnostic(beta, sigma, gamma, d, mu) == pytest.approx(expected)


def test_r0_diagnostic_matches_canonical_primary_estimate():
    """Sanity check against the canonical fractional primary-seed parameters."""
    import json

    mu = json.loads((REPO_ROOT / "outputs/model_constants.json").read_text())["mu"]["value"]
    value = r0.r0_diagnostic(
        beta=0.07616353626040417, sigma=0.010022023505992378,
        gamma=0.05680581295281048, d=0.0003095189898615, mu=mu,
    )
    assert value == pytest.approx(1.1756214159263434, rel=1e-6)


# ---- raw-source immutability --------------------------------------------------------------


def test_raw_sources_unchanged_sha256():
    import hashlib

    assert hashlib.sha256(RAW_DATASET.read_bytes()).hexdigest() == DATASET_SHA256
    assert hashlib.sha256(RAW_MANUSCRIPT.read_bytes()).hexdigest() == MANUSCRIPT_SHA256


# ---- multiseed functionals: all seeds present, primary unchanged --------------------------


def _require(path: Path) -> list[dict]:
    if not path.exists():
        pytest.skip(f"{path} not yet generated in this test session")
    with path.open() as f:
        return list(csv.DictReader(f))


def test_multiseed_functionals_includes_all_five_canonical_seeds():
    rows = _require(REPO_ROOT / "outputs/identifiability/multiseed_functionals.csv")
    found = sorted(int(r["seed"]) for r in rows)
    assert found == sorted(seeds.ALL_SEEDS)


def test_multiseed_functionals_primary_seed_matches_canonical_values():
    rows = _require(REPO_ROOT / "outputs/identifiability/multiseed_functionals.csv")
    primary = next(r for r in rows if int(r["seed"]) == seeds.PRIMARY_SEED)
    assert float(primary["beta"]) == pytest.approx(0.07616353626040417)
    assert float(primary["sigma"]) == pytest.approx(0.010022023505992378)
    assert float(primary["gamma"]) == pytest.approx(0.05680581295281048)
    assert float(primary["d"]) == pytest.approx(0.0003095189898615)
    assert float(primary["alpha"]) == pytest.approx(0.9640110362133341)


def test_multiseed_functionals_schema():
    rows = _require(REPO_ROOT / "outputs/identifiability/multiseed_functionals.csv")
    expected = {
        "seed", "beta", "sigma", "gamma", "d", "alpha", "calibration_rmse",
        "R0_diagnostic", "validation_rmse", "validation_mae", "validation_bias",
    }
    assert set(rows[0].keys()) == expected


# ---- prediction dispersion schema ----------------------------------------------------------


def test_prediction_dispersion_schema_and_split_coverage():
    rows = _require(REPO_ROOT / "outputs/identifiability/prediction_dispersion.csv")
    expected = {
        "date", "split", "mean_prediction", "std_prediction",
        "min_prediction", "max_prediction", "cv_prediction",
    }
    assert set(rows[0].keys()) == expected
    assert len(rows) == 264
    assert sum(1 for r in rows if r["split"] == "calibration") == 240
    assert sum(1 for r in rows if r["split"] == "validation") == 24


# ---- R0 multiseed diagnostic schema --------------------------------------------------------


def test_r0_multiseed_diagnostic_schema():
    rows = _require(REPO_ROOT / "outputs/identifiability/R0_multiseed_diagnostic.csv")
    assert len(rows) == 1
    expected = {"n_seeds", "mean", "median", "std", "cv", "min", "max", "range", "relative_range"}
    assert set(rows[0].keys()) == expected
    assert int(rows[0]["n_seeds"]) == 5


# ---- profile objective: calibration-only, no validation leakage ---------------------------


def test_profile_objective_uses_calibration_months_only():
    mod = _load_module("profile_objective", "scripts/profile_objective.py")
    assert mod.CALIBRATION_MONTHS == 240


def test_profile_objective_grid_never_touches_bounds_exactly():
    mod = _load_module("profile_objective", "scripts/profile_objective.py")
    for param in mod.PROFILE_PARAMETERS:
        lo, hi = mod.BOUNDS[param]
        grid = mod.build_grid(param)
        assert len(grid) == 7
        for value in grid:
            assert lo < value < hi, f"{param} grid point {value} touches or exceeds its bound"


def test_profile_objective_schema():
    rows = _require(REPO_ROOT / "outputs/identifiability/profile_objective.csv")
    expected = {
        "profile_parameter", "fixed_value", "optimized_beta", "optimized_sigma",
        "optimized_gamma", "optimized_d", "optimized_alpha", "calibration_rmse",
        "delta_rmse", "R0_diagnostic", "optimizer_success",
    }
    assert set(rows[0].keys()) == expected
    assert len(rows) == 4 * 7  # 4 profiled parameters x 7 grid points each


# ---- validation residual-sign accounting ---------------------------------------------------


def test_residual_sign_audit_convention_and_counts():
    rows = _require(REPO_ROOT / "outputs/audits/validation_residual_signs.csv")
    by_model = {r["model"]: r for r in rows}
    for label in ["fractional", "integer"]:
        row = by_model[label]
        assert int(row["convention_mismatches"]) == 0
        total = (
            int(row["residuals_positive"])
            + int(row["residuals_negative"])
            + int(row["residuals_zero"])
        )
        assert total == int(row["n_months"]) == 24

    # Integer model's reported bias == -MAE, which is only possible if every residual
    # shares the same sign -- confirm the sign audit actually shows this.
    assert int(by_model["integer"]["residuals_negative"]) == 24
    assert int(by_model["integer"]["residuals_positive"]) == 0
