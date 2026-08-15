"""Evidence-packaging only (no new experiments). Deterministically aggregates already-frozen
canonical artifacts into results_canonical/, per the CANONICAL EVIDENCE FREEZE task. Every
number here is read from an existing repo artifact, never hand-typed.
"""

from __future__ import annotations

import csv
import json
import shutil
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

OUT = REPO_ROOT / "results_canonical"


def table_forecasting_by_horizon() -> None:
    df = pd.read_csv(REPO_ROOT / "outputs/forecasting/metrics_by_horizon.csv")
    df = df.rename(columns={"n_forecasts": "n_forecasts", "RMSE": "RMSE", "MAE": "MAE", "bias": "bias"})
    df = df[["horizon", "model", "n_forecasts", "RMSE", "MAE", "bias"]].sort_values(["horizon", "model"])
    assert len(df) == 60, f"expected 60 rows (5 models x 12 horizons), got {len(df)}"
    out_path = OUT / "05_rolling_origin/table_forecasting_by_horizon.csv"
    df.to_csv(out_path, index=False)
    print(f"Wrote {out_path.relative_to(REPO_ROOT)} ({len(df)} rows)")


def table_skill_by_horizon() -> None:
    df = pd.read_csv(REPO_ROOT / "outputs/forecasting/skill_by_horizon.csv")
    df = df[["model", "baseline", "horizon", "metric", "error_model", "error_baseline", "skill", "n_forecasts"]]
    out_path = OUT / "05_rolling_origin/table_skill_by_horizon.csv"
    df.to_csv(out_path, index=False)
    print(f"Wrote {out_path.relative_to(REPO_ROOT)} ({len(df)} rows)")


def table_horizon_summary() -> None:
    df = pd.read_csv(REPO_ROOT / "outputs/forecasting/horizon_summary.csv")
    rows = []
    for _, r in df.iterrows():
        rows.append(
            {
                "model": "fractional",
                "baseline": r["baseline"],
                "metric": r["metric"],
                "H_relax": int(r["H_relax_last_horizon_positive_skill"]),
                "H_strict_from_h1": int(r["H_strict_from_h1_longest_contiguous_run"]),
                "longest_positive_run_if_available": int(r["H_strict_from_h1_longest_contiguous_run"]),
                "notes": "descriptor of this dataset/protocol only, not a universal predictability limit",
            }
        )
    out_df = pd.DataFrame(rows)

    # Verification against the task's stated expected values (must match exactly, or STOP).
    def _get(baseline, metric, field):
        return int(out_df[(out_df.baseline == baseline) & (out_df.metric == metric)][field].iloc[0])

    checks = [
        (_get("persistence", "RMSE", "H_relax") == 0),
        (_get("persistence", "RMSE", "H_strict_from_h1") == 0),
        (_get("SARIMA", "RMSE", "H_relax") == 0),
        (_get("SARIMA", "RMSE", "H_strict_from_h1") == 0),
        (_get("seasonal_naive_12", "RMSE", "H_relax") == 7),
        (_get("seasonal_naive_12", "RMSE", "H_strict_from_h1") == 7),
    ]
    if not all(checks):
        raise SystemExit("CONFLICT: horizon_summary values do not match the task's stated canonical values")

    out_path = OUT / "05_rolling_origin/table_horizon_summary.csv"
    out_df.to_csv(out_path, index=False)
    print(f"Wrote {out_path.relative_to(REPO_ROOT)} ({len(out_df)} rows)")


def table_R0_stability_summary() -> None:
    r0_df = pd.read_csv(REPO_ROOT / "outputs/identifiability/R0_evidence_set_classification.csv")
    stab_df = pd.read_csv(REPO_ROOT / "outputs/audits/dfe_stability_by_evidence_set.csv")

    r0_row = r0_df[r0_df["set"] == "NEAR_EQUIVALENT_ADMISSIBLE_SET"].iloc[0]
    stab_row = stab_df[stab_df["set"] == "NEAR_EQUIVALENT_ADMISSIBLE_SET"].iloc[0]

    assert int(r0_row["n"]) == 25
    assert round(float(r0_row["R0_min"]), 4) == 1.1542
    assert round(float(r0_row["R0_max"]), 4) == 1.1892
    assert round(float(r0_row["R0_median"]), 4) == 1.1735
    assert round(float(r0_row["R0_iqr_q1"]), 4) == 1.1682
    assert round(float(r0_row["R0_iqr_q3"]), 4) == 1.1770
    assert int(stab_row["n_stable"]) == 0
    assert int(stab_row["n_unstable"]) == 25
    assert int(stab_row["n_ambiguous"]) == 0

    row = {
        "admissible_set_definition": "delta calibration RMSE <= 1% over the canonical primary-seed RMSE (practical-identifiability tolerance, pre-registered in IDENTIFIABILITY_AUDIT_REPORT.md Sec 5)",
        "n_solutions": int(r0_row["n"]),
        "R0_min": float(r0_row["R0_min"]),
        "R0_Q1": float(r0_row["R0_iqr_q1"]),
        "R0_median": float(r0_row["R0_median"]),
        "R0_Q3": float(r0_row["R0_iqr_q3"]),
        "R0_max": float(r0_row["R0_max"]),
        "DFE_stable": int(stab_row["n_stable"]),
        "DFE_unstable": int(stab_row["n_unstable"]),
        "DFE_ambiguous": int(stab_row["n_ambiguous"]),
        "dimensional_status": "REFERENCE_TIME_SCALING_RESOLVES_CONFLICT (docs/FRACTIONAL_DIMENSIONAL_CONSISTENCY.md)",
        "notes": "R0 functional and DFE stability only; beta/gamma/d are NOT individually reported here (WEAK parameter identifiability, IDENTIFIABILITY_AUDIT_REPORT.md).",
    }
    out_path = OUT / "03_R0_stability/table_R0_stability_summary.csv"
    with out_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        w.writeheader()
        w.writerow(row)
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")


def table_full_profile_diagnostic() -> None:
    r0_df = pd.read_csv(REPO_ROOT / "outputs/identifiability/R0_evidence_set_classification.csv")
    row_src = r0_df[r0_df["set"] == "FULL_PROFILE_DIAGNOSTIC_POOL"].iloc[0]

    assert int(row_src["n"]) == 33
    assert round(float(row_src["R0_min"]), 4) == 0.6393
    assert round(float(row_src["R0_max"]), 4) == 1.6149
    assert int(row_src["n_R0_below_1"]) == 2
    assert int(row_src["n_R0_above_1"]) == 31

    row = {
        "label": "PROFILE_DIAGNOSTIC_ONLY",
        "n": int(row_src["n"]),
        "R0_min": float(row_src["R0_min"]),
        "R0_max": float(row_src["R0_max"]),
        "n_R0_lt_1": int(row_src["n_R0_below_1"]),
        "n_R0_gt_1": int(row_src["n_R0_above_1"]),
        "purpose": "Prevents accidental future claims that R0 exceeded one across the entire profile pool. "
                   "Includes deliberately poor-fit profile probes. Never the primary mechanistic evidence "
                   "-- see table_R0_stability_summary.csv (NEAR_EQUIVALENT_ADMISSIBLE_SET) for that.",
    }
    out_path = OUT / "02_identifiability/table_full_profile_diagnostic.csv"
    with out_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        w.writeheader()
        w.writerow(row)
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")


def table_long_open_loop() -> None:
    df = pd.read_csv(REPO_ROOT / "outputs/validation/validation_metrics.csv")
    rows = []
    for _, r in df.iterrows():
        rows.append(
            {
                "protocol": "LONG_OPEN_LOOP_STRESS_TEST",
                "model": r["model"],
                "evaluation_period": "2021-01 to 2022-12 (single origin: calibration through 2020-12, continuous open-loop)",
                "RMSE": float(r["rmse"]),
                "MAE": float(r["mae"]),
                "bias": float(r["bias"]),
                "interpretation": (
                    "Fractional formulation performed better than the independently refitted "
                    "integer-order formulation under this single-origin stress test. Does NOT "
                    "establish operational forecasting skill -- see 05_rolling_origin/ for that."
                    if r["model"] == "fractional" else
                    "Independently refitted integer-order (alpha=1) comparator; higher error than "
                    "the fractional formulation under this single-origin stress test."
                ),
            }
        )
    frac = next(r for r in rows if r["model"] == "fractional")
    assert round(frac["RMSE"], 3) == 1117.960
    assert round(frac["MAE"], 3) == 953.230
    assert round(frac["bias"], 3) == -851.150

    out_df = pd.DataFrame(rows)
    out_path = OUT / "04_long_open_loop/table_long_open_loop.csv"
    out_df.to_csv(out_path, index=False)
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")


def copy_figures() -> None:
    figs = {
        "F1_rmse_vs_horizon.png": REPO_ROOT / "outputs/figures/forecasting/rmse_vs_horizon.png",
        "F2a_skill_rmse_vs_horizon.png": REPO_ROOT / "outputs/figures/forecasting/skill_rmse_vs_horizon.png",
        "F2b_skill_mae_vs_horizon.png": REPO_ROOT / "outputs/figures/forecasting/skill_mae_vs_horizon.png",
        "F4_bias_vs_horizon.png": REPO_ROOT / "outputs/figures/forecasting/bias_vs_horizon.png",
    }
    for name, src in figs.items():
        dst = OUT / "06_figures" / name
        shutil.copy2(src, dst)
        print(f"Copied {src.relative_to(REPO_ROOT)} -> {dst.relative_to(REPO_ROOT)}")


def figure_F3_r0_envelope() -> None:
    """F3: R0 practical-identifiability envelope for the near-equivalent admissible set.
    New figure (not previously generated) -- built here from already-frozen data only."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    r0_df = pd.read_csv(REPO_ROOT / "outputs/identifiability/R0_evidence_set_classification.csv")
    row = r0_df[r0_df["set"] == "NEAR_EQUIVALENT_ADMISSIBLE_SET"].iloc[0]

    fig, ax = plt.subplots(figsize=(6, 2.2))
    ax.hlines(1, row["R0_min"] - 0.02, row["R0_max"] + 0.02, color="lightgray", linewidth=1)
    ax.plot([row["R0_min"], row["R0_max"]], [1, 1], color="tab:blue", linewidth=6, alpha=0.4,
            solid_capstyle="butt", label="near-equivalent solution range")
    ax.plot([row["R0_iqr_q1"], row["R0_iqr_q3"]], [1, 1], color="tab:blue", linewidth=12,
            solid_capstyle="butt", label="IQR")
    ax.scatter([row["R0_median"]], [1], color="black", zorder=5, label="median")
    ax.axvline(1.0, color="red", linestyle="--", linewidth=1, label="R0=1 threshold")
    ax.set_yticks([])
    ax.set_xlabel("R0 diagnostic functional")
    ax.set_title(f"R0 practical-identifiability envelope (near-equivalent admissible set, n={int(row['n'])})")
    ax.legend(fontsize=7, loc="upper left", bbox_to_anchor=(0, -0.4), ncol=2)
    fig.tight_layout()
    out_path = OUT / "06_figures/F3_R0_near_equivalent_envelope.png"
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")


def main() -> None:
    table_forecasting_by_horizon()
    table_skill_by_horizon()
    table_horizon_summary()
    table_R0_stability_summary()
    table_full_profile_diagnostic()
    table_long_open_loop()
    copy_figures()
    figure_F3_r0_envelope()
    print("\nAll deterministic canonical tables/figures generated and cross-checked against source artifacts.")


if __name__ == "__main__":
    main()
