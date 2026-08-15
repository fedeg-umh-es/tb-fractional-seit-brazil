"""Phase 6 of the identifiability audit: deterministic pairwise scatter plots among the pooled
multiseed + profile-objective solutions. Descriptive only -- no causal relationships are
inferred here; see IDENTIFIABILITY_AUDIT_REPORT.md for interpretation.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

OUT_DIR = REPO_ROOT / "outputs/figures/identifiability"

PAIRS = [
    ("beta", "gamma"),
    ("beta", "d"),
    ("gamma", "d"),
    ("beta", "R0_diagnostic"),
    ("gamma", "R0_diagnostic"),
]


def load_pool() -> list[dict]:
    pool = []
    with (REPO_ROOT / "outputs/identifiability/multiseed_functionals.csv").open() as f:
        for r in csv.DictReader(f):
            pool.append(
                {
                    "beta": float(r["beta"]), "sigma": float(r["sigma"]),
                    "gamma": float(r["gamma"]), "d": float(r["d"]), "alpha": float(r["alpha"]),
                    "R0_diagnostic": float(r["R0_diagnostic"]), "group": "multiseed",
                }
            )
    with (REPO_ROOT / "outputs/identifiability/profile_objective.csv").open() as f:
        for r in csv.DictReader(f):
            pool.append(
                {
                    "beta": float(r["optimized_beta"]), "sigma": float(r["optimized_sigma"]),
                    "gamma": float(r["optimized_gamma"]), "d": float(r["optimized_d"]),
                    "alpha": float(r["optimized_alpha"]),
                    "R0_diagnostic": float(r["R0_diagnostic"]), "group": "profile",
                }
            )
    return pool


def main() -> None:
    pool = load_pool()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for x_key, y_key in PAIRS:
        fig, ax = plt.subplots(figsize=(5, 4))
        for group, marker, color in [("multiseed", "o", "tab:blue"), ("profile", "^", "tab:orange")]:
            xs = [p[x_key] for p in pool if p["group"] == group]
            ys = [p[y_key] for p in pool if p["group"] == group]
            ax.scatter(xs, ys, marker=marker, color=color, label=group, alpha=0.75)
        ax.set_xlabel(x_key)
        ax.set_ylabel(y_key)
        ax.set_title(f"{x_key} vs {y_key} (descriptive; no causal inference)")
        ax.legend()
        fig.tight_layout()
        out_path = OUT_DIR / f"{x_key}_vs_{y_key}.png"
        fig.savefig(out_path, dpi=120)
        plt.close(fig)
        print(f"Wrote {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
