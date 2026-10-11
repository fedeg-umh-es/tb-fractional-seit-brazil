"""Write outputs/calibration/calibration_metrics.csv from the already-saved primary-seed
(20260815) calibration predictions, per docs/MODEL_CONTRACT.md Section 3 (RMSE/MAE/bias; no
AIC). Requires outputs/calibration/{fractional,integer}_predictions.csv to already exist
(produced by scripts/run_calibration_multiseed.py for the primary seed only).
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import metrics  # noqa: E402

MODELS = [
    ("fractional", REPO_ROOT / "outputs/calibration/fractional_predictions.csv"),
    ("integer", REPO_ROOT / "outputs/calibration/integer_predictions.csv"),
]
OUTPUT = REPO_ROOT / "outputs/calibration/calibration_metrics.csv"


def main() -> None:
    rows = []
    for label, path in MODELS:
        if not path.exists():
            raise FileNotFoundError(
                f"{path} not found -- run scripts/run_calibration_multiseed.py first"
            )
        df = pd.read_csv(path)
        rows.append(
            {
                "model": label,
                "rmse": metrics.rmse(df["observed"], df["predicted"]),
                "mae": metrics.mae(df["observed"], df["predicted"]),
                "bias": metrics.bias(df["observed"], df["predicted"]),
            }
        )

    with OUTPUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["model", "rmse", "mae", "bias"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)}")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
