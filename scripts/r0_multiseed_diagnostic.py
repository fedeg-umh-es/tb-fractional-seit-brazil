"""Phase 3 of the identifiability audit: R0 diagnostic functional stability across the 5
already-computed fractional multiseed solutions (outputs/identifiability/multiseed_functionals.csv).

Reports continuous statistics only -- no identifiability threshold is applied here; that
classification happens in IDENTIFIABILITY_AUDIT_REPORT.md after all phases' evidence is in.
"""

from __future__ import annotations

import csv
import statistics
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

IN_PATH = REPO_ROOT / "outputs/identifiability/multiseed_functionals.csv"
OUT_PATH = REPO_ROOT / "outputs/identifiability/R0_multiseed_diagnostic.csv"


def main() -> None:
    with IN_PATH.open() as f:
        rows = list(csv.DictReader(f))
    values = [float(r["R0_diagnostic"]) for r in rows]

    mean = statistics.fmean(values)
    median = statistics.median(values)
    std = statistics.pstdev(values)
    cv = std / mean if mean else float("nan")
    vmin, vmax = min(values), max(values)
    value_range = vmax - vmin
    relative_range = value_range / mean if mean else float("nan")

    out_row = {
        "n_seeds": len(values),
        "mean": mean,
        "median": median,
        "std": std,
        "cv": cv,
        "min": vmin,
        "max": vmax,
        "range": value_range,
        "relative_range": relative_range,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_row.keys()))
        writer.writeheader()
        writer.writerow(out_row)

    print(f"Wrote {OUT_PATH.relative_to(REPO_ROOT)}")
    print(out_row)


if __name__ == "__main__":
    main()
