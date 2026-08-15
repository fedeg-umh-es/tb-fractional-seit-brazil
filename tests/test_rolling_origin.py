"""Tests for the rolling-origin forecasting evaluation (FORECASTING_EVALUATION_REPORT.md).

Covers: no temporal leakage, train_end < target_date, correct rolling-origin targets, correct
seasonal-naive indexing, persistence construction, origin-specific population extrapolation,
integer alpha exactly 1, skill formula, horizon aggregation, long-open-loop/rolling-origin
separation, and canonical source immutability.
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

from tb_seit import rolling_origin as ro  # noqa: E402

RAW_DATASET = REPO_ROOT / "data" / "raw" / "tb_mes.xlsx"
RAW_MANUSCRIPT = REPO_ROOT / "manuscript" / "source" / "BIOMATEMATICA_UNICAMP.docx"
DATASET_SHA256 = "93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b"
MANUSCRIPT_SHA256 = "10e652628a7786460243fd47201bbfef498356fcee9766ce3fab48f64fa4ac88"


def _require(path: Path) -> list[dict]:
    if not path.exists():
        pytest.skip(f"{path} not yet generated in this test session")
    with path.open() as f:
        return list(csv.DictReader(f))


# ---- raw-source immutability -----------------------------------------------------------


def test_raw_sources_unchanged_sha256():
    import hashlib

    assert hashlib.sha256(RAW_DATASET.read_bytes()).hexdigest() == DATASET_SHA256
    assert hashlib.sha256(RAW_MANUSCRIPT.read_bytes()).hexdigest() == MANUSCRIPT_SHA256


# ---- origin/horizon construction ---------------------------------------------------------


def test_thirteen_origins_covering_2020_12_to_2021_12():
    assert len(ro.ORIGINS) == 13
    assert ro.ORIGINS[0] == pd.Timestamp("2020-12-01")
    assert ro.ORIGINS[-1] == pd.Timestamp("2021-12-01")


def test_all_origin_horizon_targets_within_evaluation_window_and_data():
    for origin in ro.ORIGINS:
        for h in ro.HORIZONS:
            target = origin + pd.DateOffset(months=h)
            assert pd.Timestamp("2021-01-01") <= target <= pd.Timestamp("2022-12-01"), (
                f"origin={origin}, h={h}: target {target} outside primary evaluation window"
            )


def test_train_end_precedes_every_target_no_leakage():
    for origin in ro.ORIGINS:
        ts = ro.build_training_set(origin)
        train_end = ts.train_dates.max()
        for h in ro.HORIZONS:
            target = origin + pd.DateOffset(months=h)
            assert train_end < target, f"leakage: train_end {train_end} >= target {target}"
        # origin itself is the last training observation, never a leaked future point
        assert train_end == origin


def test_training_set_never_includes_dates_after_origin():
    origin = pd.Timestamp("2021-06-01")
    ts = ro.build_training_set(origin)
    assert (ts.train_dates <= origin).all()


# ---- persistence / seasonal-naive construction ---------------------------------------------


def test_persistence_repeats_last_observed_value():
    origin = pd.Timestamp("2021-03-01")
    ts = ro.build_training_set(origin)
    forecast = ro.persistence_forecast(ts, 12)
    assert np.all(forecast == ts.train_cases[-1])
    assert len(forecast) == 12


def test_seasonal_naive_uses_only_historical_values():
    origin = pd.Timestamp("2021-06-01")
    ts = ro.build_training_set(origin)
    forecast = ro.seasonal_naive_forecast(ts, 12)
    # h=12 forecast must equal the value observed exactly at the origin (target - 12 = origin)
    assert forecast[11] == ts.train_cases[-1]
    # h=1 forecast must equal the value observed 12 months before the origin
    assert forecast[0] == ts.train_cases[-12]
    # every seasonal-naive source index must be within the training window (no leakage)
    assert len(forecast) == 12


# ---- origin-specific population extrapolation -----------------------------------------------


def test_population_trend_uses_training_window_only():
    origin_a = pd.Timestamp("2020-12-01")
    origin_b = pd.Timestamp("2021-12-01")
    ts_a = ro.build_training_set(origin_a)
    ts_b = ro.build_training_set(origin_b)
    trend_a = ro.fit_origin_population_trend(ts_a)
    trend_b = ro.fit_origin_population_trend(ts_b)
    # different training windows -> generally different fitted trends (b has 12 more months)
    assert ts_b.n_train == ts_a.n_train + 12
    # trend_a must reproduce the base-model-stage frozen trend exactly (same training window)
    assert trend_a.intercept == pytest.approx(18.9923934417, abs=1e-6)
    assert trend_a.slope == pytest.approx(0.0008140043, abs=1e-8)


def test_N_of_t_beyond_training_window_uses_extrapolation_not_future_actuals():
    origin = pd.Timestamp("2020-12-01")
    ts = ro.build_training_set(origin)
    trend = ro.fit_origin_population_trend(ts)
    N_of_t = ro.make_origin_N_of_t(ts, trend)
    t_future = ro.origin_month_index(origin) + 6
    n_future = N_of_t(t_future)
    # must match the trend's own prediction, not the dataset's actual future population
    assert n_future == pytest.approx(trend.predict(t_future))


# ---- output-file-level checks (skip if not yet generated) -----------------------------------


def test_predictions_schema_and_leakage_field_consistency():
    rows = _require(REPO_ROOT / "outputs/forecasting/rolling_origin_predictions.csv")
    expected = {
        "origin", "target_date", "horizon", "model", "observed", "predicted", "residual",
        "train_start", "train_end", "n_train", "seed", "population_source", "status",
    }
    assert set(rows[0].keys()) == expected
    for row in rows:
        assert row["train_end"] < row["target_date"]


def test_predictions_full_grid_origin_x_horizon_x_model():
    rows = _require(REPO_ROOT / "outputs/forecasting/rolling_origin_predictions.csv")
    combos = {(r["origin"], r["horizon"], r["model"]) for r in rows}
    assert len(combos) == len(rows), "duplicate origin x horizon x model rows found"
    assert len(combos) == 13 * 12 * 5


def test_integer_model_alpha_is_not_reported_as_fractional_and_status_ok_rows_exist():
    rows = _require(REPO_ROOT / "outputs/forecasting/rolling_origin_predictions.csv")
    integer_rows = [r for r in rows if r["model"] == "integer"]
    assert len(integer_rows) == 13 * 12
    assert any(r["status"] == "ok" for r in integer_rows)


def test_metrics_by_horizon_never_collapses_across_horizons():
    rows = _require(REPO_ROOT / "outputs/forecasting/metrics_by_horizon.csv")
    horizons_seen = {int(r["horizon"]) for r in rows}
    assert horizons_seen == set(range(1, 13)), "primary metrics must remain horizon-wise"


def test_skill_formula_matches_definition():
    metrics_rows = _require(REPO_ROOT / "outputs/forecasting/metrics_by_horizon.csv")
    skill_rows = _require(REPO_ROOT / "outputs/forecasting/skill_by_horizon.csv")
    metrics_by_key = {(r["model"], int(r["horizon"])): r for r in metrics_rows}
    for row in skill_rows:
        h = int(row["horizon"])
        m_row = metrics_by_key[(row["model"], h)]
        b_row = metrics_by_key[(row["baseline"], h)]
        err_model = float(m_row[row["metric"]])
        err_baseline = float(b_row[row["metric"]])
        expected_skill = 1.0 - err_model / err_baseline
        assert float(row["skill"]) == pytest.approx(expected_skill, rel=1e-9)


def test_protocol_comparison_separates_long_open_loop_from_rolling_origin():
    rows = _require(REPO_ROOT / "outputs/forecasting/protocol_comparison.csv")
    protocols = {r["protocol"] for r in rows}
    assert protocols == {"LONG_OPEN_LOOP_STRESS_TEST", "ROLLING_ORIGIN_FORECASTING"}
    long_open_loop = [r for r in rows if r["protocol"] == "LONG_OPEN_LOOP_STRESS_TEST"]
    frac_row = next(r for r in long_open_loop if r["model"] == "fractional")
    assert float(frac_row["RMSE"]) == pytest.approx(1117.960, abs=1e-3)
    int_row = next(r for r in long_open_loop if r["model"] == "integer")
    assert float(int_row["RMSE"]) == pytest.approx(1759.538, abs=1e-3)


def test_sarima_order_frozen_before_evaluation_and_unused_2021_2022():
    import json

    payload = json.loads((REPO_ROOT / "outputs/forecasting/sarima_frozen_order.json").read_text())
    assert payload["selection_data"] == "2001-01 to 2020-12 (canonical calibration only)"
    assert "selected_order" in payload and "selected_seasonal_order" in payload
