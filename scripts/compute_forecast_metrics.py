"""Horizon-wise metrics, baseline-relative skill, and horizon summary, from
outputs/forecasting/rolling_origin_predictions.csv.

Writes:
  outputs/forecasting/metrics_by_horizon.csv
  outputs/forecasting/skill_by_horizon.csv
  outputs/forecasting/horizon_summary.csv
  outputs/forecasting/residual_diagnostics_by_horizon.csv
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import metrics  # noqa: E402

IN_PATH = REPO_ROOT / "outputs/forecasting/rolling_origin_predictions.csv"
OUT_METRICS = REPO_ROOT / "outputs/forecasting/metrics_by_horizon.csv"
OUT_SKILL = REPO_ROOT / "outputs/forecasting/skill_by_horizon.csv"
OUT_SUMMARY = REPO_ROOT / "outputs/forecasting/horizon_summary.csv"
OUT_RESIDUAL = REPO_ROOT / "outputs/forecasting/residual_diagnostics_by_horizon.csv"

MODELS = ["fractional", "integer", "persistence", "seasonal_naive_12", "SARIMA"]
FOCAL_MODELS = ["fractional", "integer"]
BASELINES = ["persistence", "seasonal_naive_12", "SARIMA"]
HORIZONS = list(range(1, 13))


def load() -> pd.DataFrame:
    df = pd.read_csv(IN_PATH)
    df = df[df["status"].isin(["ok"])].copy()
    df["observed"] = df["observed"].astype(float)
    df["predicted"] = df["predicted"].astype(float)
    df = df[np.isfinite(df["predicted"])]
    return df


def compute_metrics_by_horizon(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for model_label in MODELS:
        for h in HORIZONS:
            sub = df[(df["model"] == model_label) & (df["horizon"] == h)]
            if len(sub) == 0:
                continue
            rows.append(
                {
                    "model": model_label,
                    "horizon": h,
                    "n_forecasts": len(sub),
                    "RMSE": metrics.rmse(sub["observed"], sub["predicted"]),
                    "MAE": metrics.mae(sub["observed"], sub["predicted"]),
                    "bias": metrics.bias(sub["observed"], sub["predicted"]),
                }
            )
    return pd.DataFrame(rows)


def compute_skill(metrics_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for model_label in FOCAL_MODELS:
        for baseline in BASELINES:
            for h in HORIZONS:
                m_row = metrics_df[(metrics_df["model"] == model_label) & (metrics_df["horizon"] == h)]
                b_row = metrics_df[(metrics_df["model"] == baseline) & (metrics_df["horizon"] == h)]
                if len(m_row) == 0 or len(b_row) == 0:
                    continue
                for metric_name in ["RMSE", "MAE"]:
                    err_model = float(m_row[metric_name].iloc[0])
                    err_baseline = float(b_row[metric_name].iloc[0])
                    skill = 1.0 - err_model / err_baseline if err_baseline != 0 else float("nan")
                    rows.append(
                        {
                            "model": model_label,
                            "baseline": baseline,
                            "horizon": h,
                            "metric": metric_name,
                            "error_model": err_model,
                            "error_baseline": err_baseline,
                            "skill": skill,
                            "n_forecasts": int(m_row["n_forecasts"].iloc[0]),
                        }
                    )
    return pd.DataFrame(rows)


def longest_run_from_h1(positive_flags: list[bool]) -> int:
    count = 0
    for flag in positive_flags:
        if flag:
            count += 1
        else:
            break
    return count


def last_horizon_positive(horizons: list[int], positive_flags: list[bool]) -> int:
    last = 0
    for h, flag in zip(horizons, positive_flags):
        if flag:
            last = h
    return last


def compute_horizon_summary(skill_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for baseline in BASELINES:
        for metric_name in ["RMSE", "MAE"]:
            sub = skill_df[
                (skill_df["model"] == "fractional")
                & (skill_df["baseline"] == baseline)
                & (skill_df["metric"] == metric_name)
            ].sort_values("horizon")
            if len(sub) == 0:
                continue
            horizons = sub["horizon"].tolist()
            flags = (sub["skill"] > 0).tolist()
            rows.append(
                {
                    "baseline": baseline,
                    "metric": metric_name,
                    "H_relax_last_horizon_positive_skill": last_horizon_positive(horizons, flags),
                    "H_strict_from_h1_longest_contiguous_run": longest_run_from_h1(flags),
                    "n_horizons_evaluated": len(sub),
                }
            )
    return pd.DataFrame(rows)


def compute_residual_diagnostics(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for model_label in MODELS:
        for h in HORIZONS:
            sub = df[(df["model"] == model_label) & (df["horizon"] == h)]
            if len(sub) == 0:
                continue
            residuals = (sub["predicted"] - sub["observed"]).to_numpy()
            rows.append(
                {
                    "model": model_label,
                    "horizon": h,
                    "n": len(residuals),
                    "bias": float(np.mean(residuals)),
                    "fraction_positive": float(np.mean(residuals > 0)),
                    "fraction_negative": float(np.mean(residuals < 0)),
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    df = load()

    metrics_df = compute_metrics_by_horizon(df)
    OUT_METRICS.parent.mkdir(parents=True, exist_ok=True)
    metrics_df.to_csv(OUT_METRICS, index=False)
    print(f"Wrote {OUT_METRICS.relative_to(REPO_ROOT)}")

    skill_df = compute_skill(metrics_df)
    skill_df.to_csv(OUT_SKILL, index=False)
    print(f"Wrote {OUT_SKILL.relative_to(REPO_ROOT)}")

    summary_df = compute_horizon_summary(skill_df)
    summary_df.to_csv(OUT_SUMMARY, index=False)
    print(f"Wrote {OUT_SUMMARY.relative_to(REPO_ROOT)}")
    print(summary_df.to_string())

    residual_df = compute_residual_diagnostics(df)
    residual_df.to_csv(OUT_RESIDUAL, index=False)
    print(f"Wrote {OUT_RESIDUAL.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
