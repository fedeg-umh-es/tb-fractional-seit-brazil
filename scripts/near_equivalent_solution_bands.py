"""Phase 5 of the identifiability audit: descriptive near-equivalent-objective bands.

Pools all multiseed solutions (outputs/identifiability/multiseed_functionals.csv, 5 rows) and
all profile-objective solutions (outputs/identifiability/profile_objective.csv, 28 rows) into a
single set of (beta, sigma, gamma, d, alpha, R0_diagnostic, calibration_rmse) tuples, then
reports the range of each quantity within descriptive objective bands relative to the canonical
primary-seed calibration RMSE (605.048881003205). These are descriptive bands, NOT significance
thresholds, and are fixed in advance (<=0.1%, <=0.5%, <=1.0%, <=2.0%) rather than chosen after
inspecting the data.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

CANONICAL_RMSE = 605.048881003205
BANDS_PCT = [0.1, 0.5, 1.0, 2.0]

OUT_PATH = REPO_ROOT / "outputs/identifiability/near_equivalent_solution_bands.csv"


def load_pool() -> list[dict]:
    pool = []
    with (REPO_ROOT / "outputs/identifiability/multiseed_functionals.csv").open() as f:
        for r in csv.DictReader(f):
            pool.append(
                {
                    "beta": float(r["beta"]), "sigma": float(r["sigma"]),
                    "gamma": float(r["gamma"]), "d": float(r["d"]), "alpha": float(r["alpha"]),
                    "R0_diagnostic": float(r["R0_diagnostic"]),
                    "calibration_rmse": float(r["calibration_rmse"]),
                    "source": f"multiseed:{r['seed']}",
                }
            )
    with (REPO_ROOT / "outputs/identifiability/profile_objective.csv").open() as f:
        for r in csv.DictReader(f):
            pool.append(
                {
                    "beta": float(r["optimized_beta"]), "sigma": float(r["optimized_sigma"]),
                    "gamma": float(r["optimized_gamma"]), "d": float(r["optimized_d"]),
                    "alpha": float(r["optimized_alpha"]),
                    "R0_diagnostic": float(r["R0_diagnostic"]),
                    "calibration_rmse": float(r["calibration_rmse"]),
                    "source": f"profile:{r['profile_parameter']}={r['fixed_value']}",
                }
            )
    return pool


def main() -> None:
    pool = load_pool()

    rows = []
    for band_pct in BANDS_PCT:
        threshold = CANONICAL_RMSE * (1.0 + band_pct / 100.0)
        within = [p for p in pool if p["calibration_rmse"] <= threshold]
        row = {"band_pct_over_canonical": band_pct, "threshold_rmse": threshold, "n_solutions": len(within)}
        for key in ["beta", "sigma", "gamma", "d", "alpha", "R0_diagnostic"]:
            values = [p[key] for p in within]
            row[f"{key}_min"] = min(values) if values else float("nan")
            row[f"{key}_max"] = max(values) if values else float("nan")
        rows.append(row)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with OUT_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {OUT_PATH.relative_to(REPO_ROOT)} (pool size = {len(pool)})")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
