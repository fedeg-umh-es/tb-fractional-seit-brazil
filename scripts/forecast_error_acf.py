"""ACF of forecast errors (fixed horizon, across the 13 origins) where enough observations
exist. Diagnostic only -- per instruction, NOT used as an automatic significance test.
Reuses the hand-rolled ACF from scripts/r0_envelope_and_residual_diagnostics.py (no new
dependency needed for this piece; SARIMA needed statsmodels, this does not).
"""

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

OUT_PATH = REPO_ROOT / "outputs/forecasting/forecast_error_acf.csv"
MIN_N_FOR_ACF = 8  # with 13 origins per horizon, require a reasonable minimum for a meaningful ACF


def _load_acf_fn():
    spec = importlib.util.spec_from_file_location(
        "r0_diag", REPO_ROOT / "scripts" / "r0_envelope_and_residual_diagnostics.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.acf


def main() -> None:
    acf_fn = _load_acf_fn()
    df = pd.read_csv(REPO_ROOT / "outputs/forecasting/rolling_origin_predictions.csv")
    df = df[df["status"] == "ok"]
    df["error"] = df["predicted"].astype(float) - df["observed"].astype(float)

    rows = []
    for model_label in ["fractional", "integer", "persistence", "seasonal_naive_12", "SARIMA"]:
        for h in range(1, 13):
            sub = df[(df["model"] == model_label) & (df["horizon"] == h)].sort_values("origin")
            n = len(sub)
            if n < MIN_N_FOR_ACF:
                rows.append(
                    {"model": model_label, "horizon": h, "n": n, "acf_lag1": "",
                     "note": f"n<{MIN_N_FOR_ACF}, ACF not computed (too few origins)"}
                )
                continue
            errors = sub["error"].to_numpy()
            acf_vals = acf_fn(errors, max_lag=min(3, n - 2))
            rows.append(
                {"model": model_label, "horizon": h, "n": n,
                 "acf_lag1": float(acf_vals[0]), "note": "diagnostic only, not a significance test"}
            )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["model", "horizon", "n", "acf_lag1", "note"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {OUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
