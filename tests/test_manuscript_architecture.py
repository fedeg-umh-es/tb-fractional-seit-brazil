"""Lightweight consistency checks for manuscript_architecture/ (evidence-first manuscript
architecture, built from the frozen canonical evidence set). Does NOT touch scientific
computation, results_canonical/, or canonical figures/tables -- documentation-structure checks
only.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

ARCH = REPO_ROOT / "manuscript_architecture"

RAW_DATASET = REPO_ROOT / "data" / "raw" / "tb_mes.xlsx"
RAW_MANUSCRIPT = REPO_ROOT / "manuscript" / "source" / "BIOMATEMATICA_UNICAMP.docx"
DATASET_SHA256 = "93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b"
MANUSCRIPT_SHA256 = "10e652628a7786460243fd47201bbfef498356fcee9766ce3fab48f64fa4ac88"

REQUIRED_FILES = [
    "MANUSCRIPT_EVIDENCE_ARCHITECTURE.md",
    "CLAIM_TRACEABILITY_MATRIX.csv",
    "FIGURE_TABLE_ROLE_MAP.md",
    "RESULTS_PARAGRAPH_PLAN.md",
    "DISCUSSION_ARGUMENT_MAP.md",
    "INTRODUCTION_REQUIREMENTS.md",
    "MANUSCRIPT_ARCHITECTURE_AUDIT.md",
]

BETA_GAMMA_D_PRECISE_PATTERN = re.compile(r"\b(beta|gamma|d)\s*=\s*0\.\d+", re.IGNORECASE)


def test_raw_sources_unchanged_sha256():
    import hashlib

    assert hashlib.sha256(RAW_DATASET.read_bytes()).hexdigest() == DATASET_SHA256
    assert hashlib.sha256(RAW_MANUSCRIPT.read_bytes()).hexdigest() == MANUSCRIPT_SHA256


def test_all_required_architecture_files_exist():
    for name in REQUIRED_FILES:
        assert (ARCH / name).is_file(), f"missing required architecture file: {name}"


def test_claim_traceability_matrix_covers_all_canonical_claims():
    with (ARCH / "CLAIM_TRACEABILITY_MATRIX.csv").open() as f:
        rows = list(csv.DictReader(f))
    claim_ids = {r["claim_id"] for r in rows}
    expected = {f"C{n:02d}" for n in range(1, 12)}
    assert expected.issubset(claim_ids), f"missing claim IDs: {expected - claim_ids}"


def test_claim_traceability_matrix_matches_canonical_claim_support_table():
    canon_path = REPO_ROOT / "results_canonical/07_claim_support/claim_support_table.csv"
    with canon_path.open() as f:
        canon_status = {r["claim_id"]: r["status"] for r in csv.DictReader(f)}
    with (ARCH / "CLAIM_TRACEABILITY_MATRIX.csv").open() as f:
        arch_rows = {r["claim_id"]: r for r in csv.DictReader(f) if r["claim_id"] in canon_status}
    for claim_id, status in canon_status.items():
        assert claim_id in arch_rows, f"{claim_id} missing from architecture matrix"
        assert arch_rows[claim_id]["canonical_status"] == status, (
            f"{claim_id} status mismatch: canonical={status}, "
            f"architecture={arch_rows[claim_id]['canonical_status']}"
        )


def test_no_precise_beta_gamma_d_values_in_architecture_docs():
    for path in ARCH.glob("*.md"):
        text = path.read_text()
        assert not BETA_GAMMA_D_PRECISE_PATTERN.search(text), (
            f"{path.name} names a precise beta/gamma/d value"
        )


def test_no_asserted_statistical_significance_claim():
    """'statistically significant' etc. may appear only inside forbidden-wording specs or
    reviewer-objection quotes, never as a positive assertion. Heuristic: every line containing
    the phrase must also contain a quote mark, 'forbidden', 'never', 'no ', or 'not' nearby,
    OR appear in the CLAIM_TRACEABILITY_MATRIX's forbidden_wording column context."""
    phrases = ["statistically significant", "statistically superior", "statistically inferior"]
    guard_words = ["forbidden", "never", "not ", "no ", '"', "objection"]
    for path in list(ARCH.glob("*.md")) + list(ARCH.glob("*.csv")):
        text = path.read_text().lower()
        for phrase in phrases:
            idx = text.find(phrase)
            while idx != -1:
                window = text[max(0, idx - 80) : idx + 80]
                assert any(g in window for g in guard_words), (
                    f"{path.name}: unguarded occurrence of {phrase!r} near: {window!r}"
                )
                idx = text.find(phrase, idx + 1)


def test_result_set_status_still_frozen_with_documented_limitations():
    text = (REPO_ROOT / "results_canonical/RESULT_SET_FREEZE.md").read_text()
    assert "FROZEN_WITH_DOCUMENTED_LIMITATIONS" in text


def test_audit_declares_ready_verdict():
    text = (ARCH / "MANUSCRIPT_ARCHITECTURE_AUDIT.md").read_text()
    assert "MANUSCRIPT_ARCHITECTURE_READY_FROM_FROZEN_EVIDENCE" in text
    assert "NEW_EXPERIMENTS_RUN                            = NO" in text
    assert "CANONICAL_RESULTS_MODIFIED                     = NO" in text
