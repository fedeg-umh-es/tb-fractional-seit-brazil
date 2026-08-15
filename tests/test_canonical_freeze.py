"""Integrity tests for the CANONICAL EVIDENCE FREEZE (results_canonical/).

Covers: canonical source hashes, forecasting table row counts, rolling-origin raw prediction
row count/no-duplicates/no-leakage, skill-formula reproduction, directional skill checks vs
each baseline, R0 evidence-set separation, absence of precise beta/gamma/d claims and
unsupported-superiority/significance language in canonical summaries, and the historical ~48%
claim status.
"""

from __future__ import annotations

import csv
import hashlib
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

RAW_DATASET = REPO_ROOT / "data" / "raw" / "tb_mes.xlsx"
RAW_MANUSCRIPT = REPO_ROOT / "manuscript" / "source" / "BIOMATEMATICA_UNICAMP.docx"
DATASET_SHA256 = "93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b"
MANUSCRIPT_SHA256 = "10e652628a7786460243fd47201bbfef498356fcee9766ce3fab48f64fa4ac88"

CANON = REPO_ROOT / "results_canonical"


def _rows(path: Path) -> list[dict]:
    with path.open() as f:
        return list(csv.DictReader(f))


# ---- canonical source hashes ----------------------------------------------------------------


def test_canonical_source_hashes_unchanged():
    assert hashlib.sha256(RAW_DATASET.read_bytes()).hexdigest() == DATASET_SHA256
    assert hashlib.sha256(RAW_MANUSCRIPT.read_bytes()).hexdigest() == MANUSCRIPT_SHA256


# ---- forecasting table structure -------------------------------------------------------------


def test_forecasting_table_has_exactly_60_rows():
    rows = _rows(CANON / "05_rolling_origin/table_forecasting_by_horizon.csv")
    assert len(rows) == 60
    models = {r["model"] for r in rows}
    assert models == {"fractional", "integer", "persistence", "seasonal_naive_12", "SARIMA"}
    horizons = {int(r["horizon"]) for r in rows}
    assert horizons == set(range(1, 13))


def test_rolling_origin_raw_predictions_780_rows_no_duplicates():
    rows = _rows(REPO_ROOT / "outputs/forecasting/rolling_origin_predictions.csv")
    assert len(rows) == 780
    combos = {(r["origin"], r["horizon"], r["model"]) for r in rows}
    assert len(combos) == 780


def test_rolling_origin_no_temporal_leakage():
    rows = _rows(REPO_ROOT / "outputs/forecasting/rolling_origin_predictions.csv")
    for r in rows:
        assert r["train_end"] < r["target_date"], f"leakage: {r}"


# ---- skill formula and directional checks ----------------------------------------------------


def test_skill_formula_matches_canonical_metrics():
    metrics_rows = _rows(CANON / "05_rolling_origin/table_forecasting_by_horizon.csv")
    skill_rows = _rows(CANON / "05_rolling_origin/table_skill_by_horizon.csv")
    by_key = {(r["model"], int(r["horizon"])): r for r in metrics_rows}
    for row in skill_rows:
        h = int(row["horizon"])
        err_model = float(by_key[(row["model"], h)][row["metric"]])
        err_baseline = float(by_key[(row["baseline"], h)][row["metric"]])
        expected = 1.0 - err_model / err_baseline
        assert float(row["skill"]) == pytest.approx(expected, rel=1e-9)


def test_fractional_skill_vs_persistence_negative_all_horizons():
    rows = _rows(CANON / "05_rolling_origin/table_skill_by_horizon.csv")
    sub = [r for r in rows if r["model"] == "fractional" and r["baseline"] == "persistence"]
    assert len(sub) == 24  # 12 horizons x 2 metrics
    assert all(float(r["skill"]) < 0 for r in sub)


def test_fractional_skill_vs_sarima_negative_all_horizons():
    rows = _rows(CANON / "05_rolling_origin/table_skill_by_horizon.csv")
    sub = [r for r in rows if r["model"] == "fractional" and r["baseline"] == "SARIMA"]
    assert len(sub) == 24
    assert all(float(r["skill"]) < 0 for r in sub)


def test_fractional_rmse_skill_vs_seasonal_naive_positive_h1_7_negative_h8_12():
    rows = _rows(CANON / "05_rolling_origin/table_skill_by_horizon.csv")
    sub = {
        int(r["horizon"]): float(r["skill"])
        for r in rows
        if r["model"] == "fractional" and r["baseline"] == "seasonal_naive_12" and r["metric"] == "RMSE"
    }
    for h in range(1, 8):
        assert sub[h] > 0, f"h={h} expected positive skill vs seasonal_naive_12"
    for h in range(8, 13):
        assert sub[h] < 0, f"h={h} expected negative skill vs seasonal_naive_12"


# ---- R0 evidence-set separation ---------------------------------------------------------------


def test_R0_primary_summary_uses_only_admissible_set():
    rows = _rows(CANON / "03_R0_stability/table_R0_stability_summary.csv")
    assert len(rows) == 1
    row = rows[0]
    assert int(row["n_solutions"]) == 25
    assert "delta calibration RMSE <= 1%" in row["admissible_set_definition"]
    assert round(float(row["R0_min"]), 4) == 1.1542
    assert round(float(row["R0_max"]), 4) == 1.1892
    assert int(row["DFE_stable"]) == 0
    assert int(row["DFE_unstable"]) == 25


def test_full_profile_diagnostic_pool_remains_separate():
    rows = _rows(CANON / "02_identifiability/table_full_profile_diagnostic.csv")
    assert len(rows) == 1
    row = rows[0]
    assert row["label"] == "PROFILE_DIAGNOSTIC_ONLY"
    assert int(row["n"]) == 33
    assert int(row["n_R0_lt_1"]) == 2
    assert int(row["n_R0_gt_1"]) == 31


# ---- no unsupported claims in canonical summaries ----------------------------------------------


BETA_GAMMA_D_PRECISE_PATTERN = re.compile(
    r"\b(beta|gamma|d)\s*=\s*0\.\d+", re.IGNORECASE
)
FORBIDDEN_SUPERIORITY_PHRASES = [
    "generally superior", "operationally superior", "statistically superior",
    "statistically significant", "significantly outperformed", "statistically inferior",
]

SUMMARY_DOCS = [
    CANON / "RESULT_STORYBOARD.md",
    CANON / "RESULT_SET_FREEZE.md",
    CANON / "EVIDENCE_FREEZE_REPORT.md",
    CANON / "KNOWN_LIMITATIONS.md",
]


def test_result_set_freeze_claim_status_counts_match_claim_support_table():
    """Regression guard: RESULT_SET_FREEZE.md's prose claim-status tally must sum to 11 and
    match the actual per-claim status counts in claim_support_table.csv (caught a documentation
    drift where NOT_SUPPORTED was mistyped as 4 instead of 5)."""
    rows = _rows(CANON / "07_claim_support/claim_support_table.csv")
    assert len(rows) == 11
    from collections import Counter

    counts = Counter(r["status"] for r in rows)
    assert counts["NOT_SUPPORTED"] == 5
    assert sum(counts.values()) == 11

    text = (CANON / "RESULT_SET_FREEZE.md").read_text()
    assert f"{counts['NOT_SUPPORTED']} NOT_SUPPORTED" in text
    assert f"{counts['SUPPORTED']} SUPPORTED," in text
    assert f"{counts['NOT_VERIFIED']} NOT_VERIFIED" in text
    assert f"{counts['NOT_TESTED']} NOT_TESTED" in text


def test_no_precise_beta_gamma_d_values_in_canonical_summaries():
    for path in SUMMARY_DOCS:
        text = path.read_text()
        assert not BETA_GAMMA_D_PRECISE_PATTERN.search(text), f"{path} names a precise beta/gamma/d value"
    r0_summary = (CANON / "03_R0_stability/table_R0_stability_summary.csv").read_text()
    assert not BETA_GAMMA_D_PRECISE_PATTERN.search(r0_summary), (
        "R0 stability summary must not name a precise beta/gamma/d value (mentioning that they "
        "are excluded, as a disclosure, is fine)"
    )


def test_no_forbidden_superiority_or_significance_language_in_summaries():
    for path in SUMMARY_DOCS:
        text = path.read_text().lower()
        for phrase in FORBIDDEN_SUPERIORITY_PHRASES:
            assert phrase not in text, f"{path} contains forbidden phrase: {phrase!r}"


def test_claim_support_table_forbids_significance_language_for_untested_claims():
    rows = _rows(CANON / "07_claim_support/claim_support_table.csv")
    c11 = next(r for r in rows if r["claim_id"] == "C11")
    assert c11["status"] == "NOT_TESTED"
    assert "statistically significant" in c11["forbidden_wording"].lower()


def test_historical_48_percent_claim_not_presented_as_verified():
    rows = _rows(CANON / "07_claim_support/claim_support_table.csv")
    c10 = next(r for r in rows if r["claim_id"] == "C10")
    assert c10["status"] == "NOT_VERIFIED"
    freeze_text = (CANON / "RESULT_SET_FREEZE.md").read_text()
    assert "HISTORICAL_48_PERCENT_CLAIM  = NOT_VERIFIED" in freeze_text or "NOT_VERIFIED" in freeze_text
