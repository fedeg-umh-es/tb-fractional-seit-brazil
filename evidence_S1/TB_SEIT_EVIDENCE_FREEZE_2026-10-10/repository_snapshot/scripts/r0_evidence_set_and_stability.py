"""Phases 6-7 of the dimensional-consistency audit.

Phase 6: split the pooled 33-solution set (5 multiseed + 28 profile) into
FULL_PROFILE_DIAGNOSTIC_POOL (n=33, no filtering) and NEAR_EQUIVALENT_ADMISSIBLE_SET
(delta calibration RMSE <= 1% over the canonical primary-seed RMSE -- the same, already
pre-registered practical-identifiability tolerance from IDENTIFIABILITY_AUDIT_REPORT.md Sec 5,
not a newly invented threshold), and report R0 descriptive statistics for each separately.

Phase 7: for every solution in each set, using ITS OWN fitted alpha (not a fixed alpha),
evaluate the commensurate Caputo/Matignon stability criterion |arg(lambda_i)| > alpha*pi/2 for
the (E,I) Jacobian at the disease-free equilibrium, and classify stable/unstable/ambiguous.
"""

from __future__ import annotations

import csv
import statistics
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import dimensional_audit  # noqa: E402

CANONICAL_RMSE = 605.048881003205
ADMISSIBLE_BAND_PCT = 1.0  # pre-registered in IDENTIFIABILITY_AUDIT_REPORT.md Sec 5; unchanged

OUT_EVIDENCE = REPO_ROOT / "outputs/identifiability/R0_evidence_set_classification.csv"
OUT_STABILITY = REPO_ROOT / "outputs/audits/dfe_stability_by_evidence_set.csv"


def load_pool() -> list[dict]:
    pool = []
    with (REPO_ROOT / "outputs/identifiability/multiseed_functionals.csv").open() as f:
        for r in csv.DictReader(f):
            pool.append(
                {
                    "beta": float(r["beta"]), "sigma": float(r["sigma"]),
                    "gamma": float(r["gamma"]), "d": float(r["d"]), "alpha": float(r["alpha"]),
                    "R0": float(r["R0_diagnostic"]), "rmse": float(r["calibration_rmse"]),
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
                    "R0": float(r["R0_diagnostic"]), "rmse": float(r["calibration_rmse"]),
                    "source": f"profile:{r['profile_parameter']}={r['fixed_value']}",
                }
            )
    return pool


def summarize(label: str, solutions: list[dict]) -> dict:
    r0_values = np.array([s["R0"] for s in solutions])
    q1, q3 = np.percentile(r0_values, [25, 75])
    return {
        "set": label,
        "n": len(solutions),
        "R0_min": float(r0_values.min()),
        "R0_max": float(r0_values.max()),
        "R0_median": float(np.median(r0_values)),
        "R0_iqr_q1": float(q1),
        "R0_iqr_q3": float(q3),
        "n_R0_below_1": int(np.sum(r0_values < 1.0)),
        "n_R0_above_1": int(np.sum(r0_values > 1.0)),
    }


def main() -> None:
    import json

    mu = json.loads((REPO_ROOT / "outputs/model_constants.json").read_text())["mu"]["value"]

    pool = load_pool()
    delta_pct = np.array([(s["rmse"] - CANONICAL_RMSE) / CANONICAL_RMSE * 100.0 for s in pool])
    admissible = [s for s, d in zip(pool, delta_pct) if d <= ADMISSIBLE_BAND_PCT]

    evidence_rows = [
        summarize("FULL_PROFILE_DIAGNOSTIC_POOL", pool),
        summarize("NEAR_EQUIVALENT_ADMISSIBLE_SET", admissible),
    ]
    OUT_EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    with OUT_EVIDENCE.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(evidence_rows[0].keys()))
        writer.writeheader()
        writer.writerows(evidence_rows)
    print(f"Wrote {OUT_EVIDENCE.relative_to(REPO_ROOT)}")
    for row in evidence_rows:
        print(row)

    def classify(solutions: list[dict], label: str) -> dict:
        stable = unstable = ambiguous = 0
        margins = []
        for s in solutions:
            j = dimensional_audit.j_ei(s["beta"], s["sigma"], s["gamma"], s["d"], mu)
            margin = dimensional_audit.matignon_margin(j, s["alpha"])
            margins.append(margin)
            if margin > 0:
                stable += 1
            elif margin < 0:
                unstable += 1
            else:
                ambiguous += 1
        return {
            "set": label,
            "n": len(solutions),
            "n_stable": stable,
            "n_unstable": unstable,
            "n_ambiguous": ambiguous,
            "min_angular_margin_rad": min(margins) if margins else float("nan"),
            "max_angular_margin_rad": max(margins) if margins else float("nan"),
        }

    stability_rows = [
        classify(admissible, "NEAR_EQUIVALENT_ADMISSIBLE_SET"),
        classify(pool, "FULL_PROFILE_DIAGNOSTIC_POOL (PROFILE_DIAGNOSTIC_ONLY -- not the primary conclusion)"),
    ]
    with OUT_STABILITY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(stability_rows[0].keys()))
        writer.writeheader()
        writer.writerows(stability_rows)
    print(f"Wrote {OUT_STABILITY.relative_to(REPO_ROOT)}")
    for row in stability_rows:
        print(row)


if __name__ == "__main__":
    main()
