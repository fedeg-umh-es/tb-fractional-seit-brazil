"""Tests for the R0/stability continuation (R0_STABILITY_ANALYSIS_NOTE.md).

Covers: the R0 diagnostic formula's algebraic consistency with the next-generation-matrix
derivation (det(J_EI) = det(V)*(1-R0), the identity underlying the Matignon-stability proof),
the near-equivalent solution envelope (descriptive, not a confidence interval), and the
hand-rolled ACF/Ljung-Box implementation (validated against synthetic white-noise and AR(1)
series where the answer is known analytically).
"""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import r0  # noqa: E402


def _load_module(name: str, relpath: str):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / relpath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---- NGM algebraic identity: det(J_EI) = (sigma+mu)(gamma+mu+d) * (1 - R0) ------------------


@pytest.mark.parametrize(
    "beta,sigma,gamma,d,mu",
    [
        (0.076, 0.010, 0.057, 0.0003, 0.00113),
        (0.4, 0.05, 0.2, 0.01, 0.001),
        (0.01, 0.5, 0.3, 0.05, 0.002),
        (1.0, 0.01, 0.05, 0.0001, 0.0005),
    ],
)
def test_r0_matches_next_generation_matrix_determinant_identity(beta, sigma, gamma, d, mu):
    """J_EI = [[-(sigma+mu), beta], [sigma, -(gamma+mu+d)]] at the DFE (S*/N*=1).
    Its determinant must equal (sigma+mu)(gamma+mu+d) * (1 - R0) exactly, per the
    next-generation-matrix derivation in R0_STABILITY_ANALYSIS_NOTE.md."""
    r0_value = r0.r0_diagnostic(beta, sigma, gamma, d, mu)
    j_ei = np.array([[-(sigma + mu), beta], [sigma, -(gamma + mu + d)]])
    det_j = np.linalg.det(j_ei)
    expected = (sigma + mu) * (gamma + mu + d) * (1 - r0_value)
    assert det_j == pytest.approx(expected, rel=1e-9)


@pytest.mark.parametrize(
    "beta,sigma,gamma,d,mu",
    [
        (0.076, 0.010, 0.057, 0.0003, 0.00113),  # canonical-ish, R0>1
        (0.005, 0.010, 0.057, 0.0003, 0.00113),  # small beta, R0<1
    ],
)
def test_trace_always_negative(beta, sigma, gamma, d, mu):
    """trace(J_EI) = -(sigma+mu) - (gamma+mu+d) < 0 always -- required for the R0<1 => both
    eigenvalues Re<0 argument (Routh-Hurwitz for a 2x2 system) used in the stability proof."""
    trace = -(sigma + mu) - (gamma + mu + d)
    assert trace < 0


def test_r0_below_one_implies_positive_determinant_and_above_one_implies_negative():
    mu = 0.00113
    # R0 < 1 case (weak transmission)
    r0_low = r0.r0_diagnostic(beta=0.005, sigma=0.010, gamma=0.057, d=0.0003, mu=mu)
    assert r0_low < 1
    j_low = np.array([[-(0.010 + mu), 0.005], [0.010, -(0.057 + mu + 0.0003)]])
    assert np.linalg.det(j_low) > 0

    # R0 > 1 case (canonical-ish)
    r0_high = r0.r0_diagnostic(beta=0.076, sigma=0.010, gamma=0.057, d=0.0003, mu=mu)
    assert r0_high > 1
    j_high = np.array([[-(0.010 + mu), 0.076], [0.010, -(0.057 + mu + 0.0003)]])
    assert np.linalg.det(j_high) < 0


# ---- R0 near-equivalent envelope (descriptive, not a CI) -----------------------------------


def _require(path: Path) -> list[dict]:
    if not path.exists():
        pytest.skip(f"{path} not yet generated in this test session")
    with path.open() as f:
        return list(csv.DictReader(f))


def test_r0_envelope_uses_full_33_solution_pool():
    rows = _require(REPO_ROOT / "outputs/identifiability/R0_near_equivalent_solution_envelope.csv")
    assert int(rows[0]["n_solutions"]) == 33


def test_r0_envelope_reports_descriptive_stats_not_ci_language():
    """The envelope file's own fieldnames must not use confidence-interval terminology."""
    rows = _require(REPO_ROOT / "outputs/identifiability/R0_near_equivalent_solution_envelope.csv")
    fieldnames = " ".join(rows[0].keys()).lower()
    for forbidden in ["confidence_interval", "ci_lower", "ci_upper", "95%", "sampling_uncertainty"]:
        assert forbidden not in fieldnames


def test_r0_envelope_iqr_narrower_than_full_range():
    """The IQR (bulk of near-equivalent solutions) should be much narrower than the full
    min-max range, which is dominated by deliberately poor-fit profile probe points."""
    rows = _require(REPO_ROOT / "outputs/identifiability/R0_near_equivalent_solution_envelope.csv")
    row = rows[0]
    iqr = float(row["iqr"])
    full_range = float(row["max"]) - float(row["min"])
    assert iqr < full_range


# ---- ACF / Ljung-Box implementation (validated against known synthetic cases) --------------


def test_acf_and_ljung_box_on_white_noise_not_significant():
    mod = _load_module("r0_diag", "scripts/r0_envelope_and_residual_diagnostics.py")
    rng = np.random.default_rng(0)
    white_noise = rng.normal(size=500)
    q_stat, p_value = mod.ljung_box(white_noise, max_lag=10)
    assert p_value > 0.01, "white noise should not show significant autocorrelation"


def test_acf_and_ljung_box_on_strong_ar1_is_significant():
    mod = _load_module("r0_diag", "scripts/r0_envelope_and_residual_diagnostics.py")
    rng = np.random.default_rng(1)
    n = 200
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = 0.8 * x[t - 1] + rng.normal()
    q_stat, p_value = mod.ljung_box(x, max_lag=10)
    assert p_value < 1e-6, "strongly autocorrelated AR(1) series should be flagged significant"
    acf_vals = mod.acf(x, max_lag=1)
    assert acf_vals[0] > 0.5


def test_residual_diagnostics_schema_and_validation_reliability_note():
    rows = _require(REPO_ROOT / "outputs/audits/residual_autocorrelation_diagnostics.csv")
    expected = {
        "model", "split", "n", "max_lag_tested", "acf_lag1", "acf_lag2", "acf_lag3",
        "ljung_box_Q", "ljung_box_p_value", "significant_at_0.05", "reliability_note",
    }
    assert set(rows[0].keys()) == expected
    validation_rows = [r for r in rows if r["split"] == "validation"]
    assert len(validation_rows) == 2
    for row in validation_rows:
        assert "LOW POWER" in row["reliability_note"]
        assert int(row["n"]) == 24
