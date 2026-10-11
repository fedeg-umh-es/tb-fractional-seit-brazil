"""Phase 7 of the identifiability audit: verify the residual sign convention and count
positive/negative/zero residuals for the primary-seed fractional and integer validation runs.

Residual convention (per src/tb_seit/model.py and scripts/run_validation.py, unchanged here):
    residual = predicted - observed
so a negative residual means underprediction, positive means overprediction. This matches
outputs/validation/{fractional,integer}_predictions.csv's own "residual" column exactly.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

OUT_PATH = REPO_ROOT / "outputs/audits/validation_residual_signs.csv"


def audit_one(label: str, path: Path) -> dict:
    with path.open() as f:
        rows = list(csv.DictReader(f))

    positive = negative = zero = 0
    mismatches = 0
    for row in rows:
        residual = float(row["residual"])
        recomputed = float(row["predicted"]) - float(row["observed"])
        if abs(residual - recomputed) > 1e-6:
            mismatches += 1
        if residual > 0:
            positive += 1
        elif residual < 0:
            negative += 1
        else:
            zero += 1

    return {
        "model": label,
        "n_months": len(rows),
        "residuals_positive": positive,
        "residuals_negative": negative,
        "residuals_zero": zero,
        "convention_mismatches": mismatches,
        "convention": "residual = predicted - observed",
    }


def main() -> None:
    rows = [
        audit_one("fractional", REPO_ROOT / "outputs/validation/fractional_predictions.csv"),
        audit_one("integer", REPO_ROOT / "outputs/validation/integer_predictions.csv"),
    ]

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
