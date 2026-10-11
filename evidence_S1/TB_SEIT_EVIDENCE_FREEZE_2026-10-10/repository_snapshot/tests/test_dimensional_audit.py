"""Tests for the FRACTIONAL_R0_PARAMETERIZATION_CONFLICT resolution
(docs/FRACTIONAL_DIMENSIONAL_CONSISTENCY.md, R0_STABILITY_ANALYSIS_NOTE.md Phase 8).

Covers: reference-time scaling dimensions/units, tau0=1 month numerical equivalence, uniform
scaling applied to every RHS equation, R0 invariance under a general positive scaling factor,
Jacobian eigenvalue-argument invariance, separation of the full diagnostic pool from the
near-equivalent admissible set, absence of a false "all R0>1" claim over the full pool, and
canonical source immutability.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import dimensional_audit, model, r0  # noqa: E402

RAW_DATASET = REPO_ROOT / "data" / "raw" / "tb_mes.xlsx"
RAW_MANUSCRIPT = REPO_ROOT / "manuscript" / "source" / "BIOMATEMATICA_UNICAMP.docx"
DATASET_SHA256 = "93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b"
MANUSCRIPT_SHA256 = "10e652628a7786460243fd47201bbfef498356fcee9766ce3fab48f64fa4ac88"


def _require(path: Path) -> list[dict]:
    if not path.exists():
        pytest.skip(f"{path} not yet generated in this test session")
    with path.open() as f:
        return list(csv.DictReader(f))


# ---- raw-source immutability ------------------------------------------------------------


def test_raw_sources_unchanged_sha256():
    import hashlib

    assert hashlib.sha256(RAW_DATASET.read_bytes()).hexdigest() == DATASET_SHA256
    assert hashlib.sha256(RAW_MANUSCRIPT.read_bytes()).hexdigest() == MANUSCRIPT_SHA256


# ---- reference-time scaling dimensions / tau0=1 numerical equivalence -------------------


def test_scaling_factor_is_exactly_one_for_tau0_one_month_any_alpha():
    for alpha in [0.50, 0.75, 0.9640110362133341, 1.0]:
        c = dimensional_audit.reference_time_scaling_factor(alpha, tau0=1.0)
        assert c == 1.0


def test_scaling_factor_not_one_for_other_tau0_and_alpha():
    """Sanity: the factor is only trivially 1 because tau0=1 in this project's month-based
    time axis -- confirm it is NOT a tautology by checking a non-unit tau0 changes it."""
    c = dimensional_audit.reference_time_scaling_factor(alpha=0.9, tau0=2.0)
    assert c != 1.0
    assert c == pytest.approx(2.0 ** 0.1)


def test_scaled_rhs_equals_unscaled_rhs_when_tau0_is_one():
    """The scaled vector field must be numerically identical (not merely close) to the
    production tb_seit.model.seit_rhs when tau0=1 month, for every state component -- i.e. the
    uniform scaling is applied to the ENTIRE vector field (S,E,I,T,C), not selected terms."""
    params = model.SeitParameters(beta=0.076, sigma=0.010, gamma=0.057, d=0.0003, alpha=0.964)
    mu, lambda_ = 0.001126, 220201.0
    y = np.array([1.7e8, 3e4, 4e4, 1e3, 5e4])

    def N_of_t(_t):
        return 1.75e8

    unscaled = model.seit_rhs(0.0, y, params, lambda_, mu, N_of_t)
    scaled = dimensional_audit.seit_rhs_reference_time_scaled(
        0.0, y, params, lambda_, mu, N_of_t, tau0=1.0
    )
    assert np.array_equal(unscaled, scaled), "scaling by exactly 1.0 must be a numeric no-op"


def test_numerical_equivalence_report_shows_zero_difference():
    rows = _require(REPO_ROOT / "outputs/audits/dimensional_scaling_numerical_equivalence.csv")
    for row in rows:
        assert float(row["max_absolute_difference"]) == 0.0
        assert float(row["max_relative_difference"]) == 0.0
        assert float(row["rmse_difference"]) == 0.0
        assert float(row["scaling_factor_c"]) == 1.0


# ---- R0 invariance under general positive scaling (Phase 4) -----------------------------


@pytest.mark.parametrize("c", [1.0, 0.3, 2.5, 10.0])
def test_r0_invariant_under_uniform_positive_scaling(c):
    beta, sigma, gamma, d, mu = 0.076, 0.010, 0.057, 0.0003, 0.00113
    r0_base = r0.r0_diagnostic(beta, sigma, gamma, d, mu)

    f_mat, v_mat = dimensional_audit.f_v_matrices(beta, sigma, gamma, d, mu)
    f_scaled, v_scaled = c * f_mat, c * v_mat
    ngm_scaled = f_scaled @ np.linalg.inv(v_scaled)
    r0_scaled = float(np.max(np.abs(np.linalg.eigvals(ngm_scaled))))

    assert r0_scaled == pytest.approx(r0_base, rel=1e-9)


def test_r0_from_ngm_matches_diagnostic_formula():
    beta, sigma, gamma, d, mu = 0.076, 0.010, 0.057, 0.0003, 0.00113
    assert dimensional_audit.r0_from_ngm(beta, sigma, gamma, d, mu) == pytest.approx(
        r0.r0_diagnostic(beta, sigma, gamma, d, mu), rel=1e-9
    )


# ---- Jacobian eigenvalue-argument invariance (Phase 5) -----------------------------------


@pytest.mark.parametrize("c", [1.0, 0.5, 3.0, 7.7])
def test_eigenvalue_argument_invariant_under_positive_scaling(c):
    j = dimensional_audit.j_ei(beta=0.076, sigma=0.010, gamma=0.057, d=0.0003, mu=0.00113)
    args_base = np.sort(dimensional_audit.eigenvalue_arguments(j))
    args_scaled = np.sort(dimensional_audit.eigenvalue_arguments(c * j))
    assert np.allclose(args_base, args_scaled, atol=1e-10)


def test_matignon_margin_matches_manual_computation_for_r0_above_one():
    """For R0>1, one eigenvalue of J_EI is real positive (arg=0); margin should be exactly
    -alpha*pi/2 (the binding eigenvalue)."""
    beta, sigma, gamma, d, mu, alpha = 0.076, 0.010, 0.057, 0.0003, 0.00113, 0.964
    j = dimensional_audit.j_ei(beta, sigma, gamma, d, mu)
    margin = dimensional_audit.matignon_margin(j, alpha)
    assert margin == pytest.approx(-alpha * np.pi / 2, abs=1e-6)


# ---- evidence-set separation (Phase 6) ---------------------------------------------------


def test_full_pool_and_admissible_set_are_reported_separately():
    rows = _require(REPO_ROOT / "outputs/identifiability/R0_evidence_set_classification.csv")
    sets = {r["set"] for r in rows}
    assert sets == {"FULL_PROFILE_DIAGNOSTIC_POOL", "NEAR_EQUIVALENT_ADMISSIBLE_SET"}
    full = next(r for r in rows if r["set"] == "FULL_PROFILE_DIAGNOSTIC_POOL")
    admissible = next(r for r in rows if r["set"] == "NEAR_EQUIVALENT_ADMISSIBLE_SET")
    assert int(full["n"]) == 33
    assert int(admissible["n"]) == 25


def test_full_pool_does_not_have_uniform_R0_above_1():
    """Regression guard for the corrected false claim: the full 33-solution pool DOES contain
    R0<1 points (deliberately poor-fit profile probes) -- it must never be reported as
    uniformly R0>1."""
    rows = _require(REPO_ROOT / "outputs/identifiability/R0_evidence_set_classification.csv")
    full = next(r for r in rows if r["set"] == "FULL_PROFILE_DIAGNOSTIC_POOL")
    assert int(full["n_R0_below_1"]) > 0
    assert float(full["R0_min"]) < 1.0


def test_admissible_set_R0_all_above_1():
    rows = _require(REPO_ROOT / "outputs/identifiability/R0_evidence_set_classification.csv")
    admissible = next(r for r in rows if r["set"] == "NEAR_EQUIVALENT_ADMISSIBLE_SET")
    assert int(admissible["n_R0_below_1"]) == 0
    assert float(admissible["R0_min"]) > 1.0


def test_stability_by_evidence_set_schema_and_counts():
    rows = _require(REPO_ROOT / "outputs/audits/dfe_stability_by_evidence_set.csv")
    admissible = next(r for r in rows if r["set"] == "NEAR_EQUIVALENT_ADMISSIBLE_SET")
    assert int(admissible["n"]) == 25
    assert int(admissible["n_stable"]) + int(admissible["n_unstable"]) + int(
        admissible["n_ambiguous"]
    ) == 25

    full_row = next(r for r in rows if r["set"].startswith("FULL_PROFILE_DIAGNOSTIC_POOL"))
    assert "PROFILE_DIAGNOSTIC_ONLY" in full_row["set"]
    assert int(full_row["n_stable"]) > 0, (
        "full pool must show its 2 stable (R0<1) diagnostic-only points, distinct from the "
        "admissible set which has none"
    )


# ---- no false claim in the corrected note --------------------------------------------------


def test_note_does_not_claim_full_pool_uniformly_above_one():
    """The false claim may be quoted once (inside the explicit correction, as the thing being
    refuted); it must not appear as a bare, unqualified assertion anywhere else, and the note
    must explicitly document that 2 of 33 full-pool solutions have R0<1."""
    text = (REPO_ROOT / "R0_STABILITY_ANALYSIS_NOTE.md").read_text()
    assert text.count("R0 stayed above 1 throughout") <= 1
    assert "That reading is false" in text
    assert "2 solutions with R0<1" in text or "n(R0<1) = 2" in text


def test_note_states_admissible_set_result_correctly():
    text = (REPO_ROOT / "R0_STABILITY_ANALYSIS_NOTE.md").read_text()
    assert "n(R0<1) = 0" in text or "0 of 33" in text or "n_stable = 0" in text
