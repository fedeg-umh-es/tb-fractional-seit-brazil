"""Repository-state tests for the INDEPENDENT_REIMPLEMENTATION_SPECIFICATION stage.

These tests check documentation/state bookkeeping only: that the canon documents declare the
correct stage and split, that the required protocol documents exist and are populated, and that
no scientific result artifacts have been generated yet. They do not compute or assert any
epidemiological model result.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_CANON = REPO_ROOT / "PROJECT_CANON.md"
REPRODUCIBILITY_STATUS = REPO_ROOT / "REPRODUCIBILITY_STATUS.md"
PROTOCOL = REPO_ROOT / "docs" / "REIMPLEMENTATION_PROTOCOL.md"
ASSUMPTIONS = REPO_ROOT / "docs" / "ASSUMPTIONS_REGISTER.md"
DECISION_LOG = REPO_ROOT / "docs" / "METHOD_DECISION_LOG.md"
OUTPUTS_DIR = REPO_ROOT / "outputs"

ASSUMPTION_IDS = [f"A{n:02d}" for n in range(1, 46)]


def test_project_canon_declares_reimplementation_stage():
    text = PROJECT_CANON.read_text(encoding="utf-8")
    assert "INDEPENDENT_REIMPLEMENTATION_SPECIFICATION" in text
    assert "EXACT_REPRODUCTION = NOT_POSSIBLE" in text
    assert "INDEPENDENT_REIMPLEMENTATION = REQUIRED" in text


def test_project_canon_declares_canonical_split():
    text = PROJECT_CANON.read_text(encoding="utf-8")
    assert "2001-01 to 2022-12" in text
    assert "264 monthly observations" in text
    assert "2001-01 to 2020-12" in text
    assert "N = 240" in text
    assert "2021-01 to 2022-12" in text
    assert "N = 24" in text


def test_reproducibility_status_reflects_reimplementation_state():
    text = REPRODUCIBILITY_STATUS.read_text(encoding="utf-8")
    assert "VERIFIED" in text  # dataset integrity
    assert "NOT_POSSIBLE" in text  # exact reproduction
    assert "REQUIRED" in text  # independent reimplementation
    assert "OPTIMIZATION_CONTRACT_INCOMPLETE" in text  # base-model calibration gate (2026-08-15)
    for row in [
        "Fractional model reproduction",
        "Integer model reproduction",
        "Predictive validation",
        "R0",
        "Stability",
        "Sensitivity",
        "Optimal control",
    ]:
        assert row in text
    assert "NOT_STARTED" in text
    assert "NOT_VERIFIED" in text
    assert "BLOCKED" in text


def test_protocol_document_exists_and_defines_contract():
    assert PROTOCOL.is_file()
    text = PROTOCOL.read_text(encoding="utf-8")
    assert "REPRODUCTION_MODE = INDEPENDENT_REIMPLEMENTATION" in text
    assert "EXACT_REPRODUCTION = IMPOSSIBLE_FROM_AVAILABLE_MATERIAL" in text
    assert "REFERENCE_ONLY_NOT_EVIDENCE" in text
    for label in [
        "CONFIRMED_BY_REIMPLEMENTATION",
        "REPLACED_BY_REIMPLEMENTATION",
        "NOT_REPRODUCIBLE",
        "REMOVED",
    ]:
        assert label in text


def test_assumptions_register_covers_all_items():
    assert ASSUMPTIONS.is_file()
    text = ASSUMPTIONS.read_text(encoding="utf-8")
    for assumption_id in ASSUMPTION_IDS:
        assert re.search(rf"\b{assumption_id}\b", text), f"{assumption_id} missing from register"
    for status in ["KNOWN_FROM_MANUSCRIPT", "PARTIALLY_SPECIFIED", "UNKNOWN"]:
        assert status in text


def test_decision_log_exists_with_initial_entries():
    assert DECISION_LOG.is_file()
    text = DECISION_LOG.read_text(encoding="utf-8")
    for entry in ["D001", "D002", "D003", "D004", "D005", "D006"]:
        assert entry in text


def test_no_out_of_scope_analyses_generated():
    """Superseded gate (2026-08-15, D024 and the identifiability-audit stage): the seed
    contract is frozen and both the base-model pipeline and the practical-identifiability audit
    (IDENTIFIABILITY_AUDIT_REPORT.md) have been executed, so outputs/calibration/*,
    outputs/validation/*, outputs/sensitivity/*, outputs/identifiability/* (including the R0
    DIAGNOSTIC functional artifacts -- explicitly not a final R0 estimate, per that report's
    Section 1/7) and the kill-test audits are now expected and permitted. What must still be
    absent is anything from the explicitly out-of-scope analyses for this stage: AIC, a final
    R0 point estimate/stability analysis, R0 sensitivity-index (dR0/dp), and optimal control.
    """
    forbidden_name_fragments = [
        "aic",
        "optimal_control",
        "optimal-control",
        "r0_estimate",
        "r0estimate",
        "final_r0",
        "reproduction_number",
        "stability_analysis",
        "sensitivity_index",
    ]
    if not OUTPUTS_DIR.is_dir():
        return
    all_files = [p for p in OUTPUTS_DIR.rglob("*") if p.is_file()]
    for path in all_files:
        lowered = path.name.lower()
        for fragment in forbidden_name_fragments:
            assert fragment not in lowered, (
                f"unexpected out-of-scope artifact present at this stage: {path}"
            )
