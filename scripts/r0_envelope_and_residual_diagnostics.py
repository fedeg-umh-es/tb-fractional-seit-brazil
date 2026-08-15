"""R0/stability continuation, Parts A and B only (per the user's checkpoint superseding the
original CI-construction step -- see R0_STABILITY_ANALYSIS_NOTE.md for Part C and the resulting
STOP).

Part A: R0_NEAR_EQUIVALENT_SOLUTION_ENVELOPE over the full ~33-solution profile+multiseed pool
(all points, not RMSE-filtered) -- an identifiability/sensitivity envelope, explicitly NOT a
confidence interval, NOT sampling uncertainty. Also reports the relationship between R0
deviation and calibration-RMSE degradation.

Part B: ACF and Ljung-Box diagnostics on calibration and validation residuals, for both the
fractional and integer models, computed WITHOUT external dependencies (statsmodels is not
installed and was not added -- pip install was declined). Implemented directly with numpy/scipy
(scipy.stats.chi2 for the Ljung-Box p-value only; ACF/Ljung-Box statistic computed by hand,
standard textbook formulas). Diagnostic only -- does NOT determine any R0 uncertainty interval
(per the user's explicit instruction, a separate future experiment would be required for that).
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
from scipy import stats

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

CANONICAL_RMSE = 605.048881003205
RMSE_BANDS_PCT = [0.1, 0.5, 1.0, 2.0, 5.0]

OUT_ENVELOPE = REPO_ROOT / "outputs/identifiability/R0_near_equivalent_solution_envelope.csv"
OUT_RESIDUAL_DIAG = REPO_ROOT / "outputs/audits/residual_autocorrelation_diagnostics.csv"


def load_pool() -> list[dict]:
    pool = []
    with (REPO_ROOT / "outputs/identifiability/multiseed_functionals.csv").open() as f:
        for r in csv.DictReader(f):
            pool.append(
                {"R0": float(r["R0_diagnostic"]), "rmse": float(r["calibration_rmse"]),
                 "source": f"multiseed:{r['seed']}"}
            )
    with (REPO_ROOT / "outputs/identifiability/profile_objective.csv").open() as f:
        for r in csv.DictReader(f):
            pool.append(
                {"R0": float(r["R0_diagnostic"]), "rmse": float(r["calibration_rmse"]),
                 "source": f"profile:{r['profile_parameter']}={r['fixed_value']}"}
            )
    return pool


def part_a_envelope() -> None:
    pool = load_pool()
    r0 = np.array([p["R0"] for p in pool])
    rmse = np.array([p["rmse"] for p in pool])
    delta_pct = (rmse - CANONICAL_RMSE) / CANONICAL_RMSE * 100.0

    q1, q3 = np.percentile(r0, [25, 75])
    summary = {
        "n_solutions": len(r0),
        "median": float(np.median(r0)),
        "mean": float(np.mean(r0)),
        "min": float(np.min(r0)),
        "max": float(np.max(r0)),
        "iqr_q1": float(q1),
        "iqr_q3": float(q3),
        "iqr": float(q3 - q1),
        "full_relative_range_pct": float((r0.max() - r0.min()) / r0.mean() * 100.0),
        "pearson_corr_deltaRMSEpct_vs_absR0dev_from_mean": float(
            np.corrcoef(delta_pct, np.abs(r0 - r0.mean()))[0, 1]
        ),
    }
    for band in RMSE_BANDS_PCT:
        mask = delta_pct <= band
        sub = r0[mask]
        summary[f"band_le_{band}pct_n"] = int(mask.sum())
        summary[f"band_le_{band}pct_R0_min"] = float(sub.min())
        summary[f"band_le_{band}pct_R0_max"] = float(sub.max())

    OUT_ENVELOPE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_ENVELOPE.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)
    print(f"Wrote {OUT_ENVELOPE.relative_to(REPO_ROOT)}")
    print(summary)


def acf(x: np.ndarray, max_lag: int) -> np.ndarray:
    n = len(x)
    x = x - x.mean()
    c0 = np.dot(x, x) / n
    return np.array([np.dot(x[: n - k], x[k:]) / n / c0 for k in range(1, max_lag + 1)])


def ljung_box(x: np.ndarray, max_lag: int) -> tuple[float, float]:
    n = len(x)
    r = acf(x, max_lag)
    q_stat = n * (n + 2) * np.sum((r**2) / (n - np.arange(1, max_lag + 1)))
    p_value = float(stats.chi2.sf(q_stat, df=max_lag))
    return float(q_stat), p_value


def part_b_residual_diagnostics() -> None:
    sources = [
        ("fractional", "calibration", REPO_ROOT / "outputs/calibration/fractional_predictions.csv", 20),
        ("integer", "calibration", REPO_ROOT / "outputs/calibration/integer_predictions.csv", 20),
        ("fractional", "validation", REPO_ROOT / "outputs/validation/fractional_predictions.csv", 6),
        ("integer", "validation", REPO_ROOT / "outputs/validation/integer_predictions.csv", 6),
    ]

    rows = []
    for model_label, split, path, max_lag in sources:
        with path.open() as f:
            residuals = np.array([float(r["residual"]) for r in csv.DictReader(f)])
        n = len(residuals)
        acf_vals = acf(residuals, max_lag)
        q_stat, p_value = ljung_box(residuals, max_lag)
        rows.append(
            {
                "model": model_label,
                "split": split,
                "n": n,
                "max_lag_tested": max_lag,
                "acf_lag1": acf_vals[0],
                "acf_lag2": acf_vals[1] if max_lag >= 2 else float("nan"),
                "acf_lag3": acf_vals[2] if max_lag >= 3 else float("nan"),
                "ljung_box_Q": q_stat,
                "ljung_box_p_value": p_value,
                "significant_at_0.05": p_value < 0.05,
                "reliability_note": (
                    "LOW POWER: n=24 validation segment, few effective lags -- non-significance "
                    "here is not strong evidence of independence" if split == "validation" else
                    "adequate n for the tested lag count"
                ),
            }
        )

    OUT_RESIDUAL_DIAG.parent.mkdir(parents=True, exist_ok=True)
    with OUT_RESIDUAL_DIAG.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {OUT_RESIDUAL_DIAG.relative_to(REPO_ROOT)}")
    for row in rows:
        print(row)


if __name__ == "__main__":
    part_a_envelope()
    part_b_residual_diagnostics()
