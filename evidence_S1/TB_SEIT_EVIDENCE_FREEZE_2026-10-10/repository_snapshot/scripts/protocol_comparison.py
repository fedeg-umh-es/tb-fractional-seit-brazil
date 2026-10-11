"""Writes outputs/forecasting/protocol_comparison.csv, clearly separating the preserved
LONG_OPEN_LOOP_STRESS_TEST (2001-2020 -> 2021-2022, single origin, existing frozen numbers --
NOT recomputed here) from ROLLING_ORIGIN_FORECASTING (this task's primary evidence, pooled here
ONLY as a secondary cross-protocol comparison aggregate -- the primary evidence remains
horizon-wise in metrics_by_horizon.csv, never collapsed there).
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import metrics  # noqa: E402

OUT_PATH = REPO_ROOT / "outputs/forecasting/protocol_comparison.csv"

# Existing, frozen, NOT recomputed here -- see outputs/validation/validation_metrics.csv
LONG_OPEN_LOOP = {
    "fractional": {"RMSE": 1117.960, "MAE": 953.230, "bias": -851.150, "n": 24},
    "integer": {"RMSE": 1759.538, "MAE": 1588.649, "bias": -1588.649, "n": 24},
}


def main() -> None:
    rows = []
    for model_label, m in LONG_OPEN_LOOP.items():
        rows.append(
            {
                "protocol": "LONG_OPEN_LOOP_STRESS_TEST",
                "model": model_label,
                "RMSE": m["RMSE"], "MAE": m["MAE"], "bias": m["bias"], "n": m["n"],
                "notes": "single origin (2020-12), open-loop through 2022-12; preserved from "
                         "the base-model stage, not recomputed or mixed with rolling-origin.",
            }
        )

    df = pd.read_csv(REPO_ROOT / "outputs/forecasting/rolling_origin_predictions.csv")
    df = df[df["status"] == "ok"]
    df["observed"] = df["observed"].astype(float)
    df["predicted"] = df["predicted"].astype(float)

    for model_label in ["fractional", "integer", "persistence", "seasonal_naive_12", "SARIMA"]:
        sub = df[df["model"] == model_label]
        if len(sub) == 0:
            continue
        rows.append(
            {
                "protocol": "ROLLING_ORIGIN_FORECASTING",
                "model": model_label,
                "RMSE": metrics.rmse(sub["observed"], sub["predicted"]),
                "MAE": metrics.mae(sub["observed"], sub["predicted"]),
                "bias": metrics.bias(sub["observed"], sub["predicted"]),
                "n": len(sub),
                "notes": "SECONDARY AGGREGATE ONLY: pooled across all 13 origins x h=1..12 for "
                         "cross-protocol comparison. Primary rolling-origin evidence is "
                         "horizon-wise in metrics_by_horizon.csv -- never use this row as the "
                         "primary forecasting result.",
            }
        )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {OUT_PATH.relative_to(REPO_ROOT)}")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
