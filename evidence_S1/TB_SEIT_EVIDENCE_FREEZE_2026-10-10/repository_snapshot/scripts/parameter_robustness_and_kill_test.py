"""Identifiability diagnostics + fractional-memory kill-condition audit.

Per docs/MODEL_CONTRACT.md Sections 11/15 and the task's "IDENTIFIABILITY / PARAMETER
ROBUSTNESS" / "KILL CONDITION AUDIT" sections. NOT EXECUTED -- requires
outputs/calibration/fractional_multiseed.csv, outputs/calibration/integer_multiseed.csv, and
outputs/validation/validation_metrics.csv, none of which exist because calibration is blocked
(undefined canonical seed set). No numeric threshold for PARAMETER_INSTABILITY is invented here:
docs/MODEL_CONTRACT.md does not define one, so this script reports continuous diagnostics
(mean/std/min/max/CV, objective-function spread) and leaves classification to the accompanying
prose report, per explicit task instruction.
"""

from __future__ import annotations

import csv
import statistics
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

FRACTIONAL_MULTISEED = REPO_ROOT / "outputs/calibration/fractional_multiseed.csv"
INTEGER_MULTISEED = REPO_ROOT / "outputs/calibration/integer_multiseed.csv"
VALIDATION_METRICS = REPO_ROOT / "outputs/validation/validation_metrics.csv"
ALPHA_SENSITIVITY = REPO_ROOT / "outputs/sensitivity/alpha_bound_sensitivity.csv"

OUT_ROBUSTNESS = REPO_ROOT / "outputs/audits/parameter_robustness.csv"
OUT_KILL_TEST = REPO_ROOT / "outputs/audits/fractional_memory_kill_test.md"

PARAM_FIELDS = ["beta", "sigma", "gamma", "d", "alpha"]


def _require(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found -- multi-seed calibration has not been run "
            "(blocked: canonical + diagnostic seeds undefined, see "
            "OPTIMIZATION_CONTRACT_INCOMPLETE)."
        )


def _read_rows(path: Path) -> list[dict]:
    with path.open() as f:
        return list(csv.DictReader(f))


def parameter_robustness() -> None:
    _require(FRACTIONAL_MULTISEED)
    rows = _read_rows(FRACTIONAL_MULTISEED)

    out_rows = []
    for field in PARAM_FIELDS + ["objective"]:
        values = [float(r[field]) for r in rows]
        mean = statistics.fmean(values)
        std = statistics.pstdev(values) if len(values) > 1 else 0.0
        cv = (std / mean) if mean not in (0, None) and field != "objective" else float("nan")
        out_rows.append(
            {
                "quantity": field,
                "mean": mean,
                "std": std,
                "min": min(values),
                "max": max(values),
                "cv": cv,
                "n_seeds": len(values),
            }
        )

    OUT_ROBUSTNESS.parent.mkdir(parents=True, exist_ok=True)
    with OUT_ROBUSTNESS.open("w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["quantity", "mean", "std", "min", "max", "cv", "n_seeds"]
        )
        writer.writeheader()
        writer.writerows(out_rows)
    print(f"Wrote {OUT_ROBUSTNESS.relative_to(REPO_ROOT)}")


def kill_condition_audit() -> None:
    _require(FRACTIONAL_MULTISEED)
    _require(INTEGER_MULTISEED)
    _require(VALIDATION_METRICS)

    fractional_rows = _read_rows(FRACTIONAL_MULTISEED)
    validation_rows = {r["model"]: r for r in _read_rows(VALIDATION_METRICS)}

    # Component A: parameter stability vs. objective spread.
    objectives = [float(r["objective"]) for r in fractional_rows]
    obj_cv = (
        statistics.pstdev(objectives) / statistics.fmean(objectives)
        if statistics.fmean(objectives) else float("nan")
    )
    param_cvs = {}
    for field in PARAM_FIELDS:
        values = [float(r[field]) for r in fractional_rows]
        mean = statistics.fmean(values)
        param_cvs[field] = (statistics.pstdev(values) / mean) if mean else float("nan")

    # Component B: alpha boundary behavior.
    alphas = [float(r["alpha"]) for r in fractional_rows]

    # Component C: integer vs fractional out-of-sample.
    frac_val_rmse = float(validation_rows["fractional"]["rmse"])
    int_val_rmse = float(validation_rows["integer"]["rmse"])

    lines = [
        "# Fractional-memory kill-condition audit",
        "",
        "Per docs/MODEL_CONTRACT.md Section 15. Evidence-based only; no configuration was",
        "adjusted to avoid any outcome below.",
        "",
        f"## A. Parameter stability across seeds vs. objective spread",
        f"Objective (calibration RMSE) coefficient of variation across seeds: {obj_cv:.4f}",
        f"Per-parameter CV across seeds: {param_cvs}",
        "Classification: SURVIVES / WEAKENS / FAILS -- see prose in "
        "BASE_MODEL_REIMPLEMENTATION_REPORT.md Section 12/13 (no undocumented binary threshold "
        "applied here; continuous diagnostics only).",
        "",
        f"## B. Alpha boundary behavior",
        f"Fitted alpha across seeds: {alphas}",
        f"Primary bound: [0.50, 1.00]",
        "",
        f"## C. Integer comparator vs. fractional model, 2021-2022 holdout",
        f"Fractional validation RMSE: {frac_val_rmse}",
        f"Integer validation RMSE:    {int_val_rmse}",
        f"Fractional better: {frac_val_rmse < int_val_rmse}",
    ]
    OUT_KILL_TEST.write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_KILL_TEST.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    parameter_robustness()
    kill_condition_audit()
