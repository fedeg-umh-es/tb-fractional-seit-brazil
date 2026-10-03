"""Submission-quality figures and tables for the BMB package.

Reads ONLY frozen artifacts (results_canonical/ tables and the identifiability CSVs that
the canonical F3 was already built from). Writes to submission_bmb/figures and
submission_bmb/tables. It never writes to results_canonical/ and computes no new
evidence: every plotted value is a frozen value or an order statistic of frozen values,
and the script asserts agreement with the frozen summary tables.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "results_canonical"
FIG = ROOT / "submission_bmb/figures"
TAB = ROOT / "submission_bmb/tables"

LABEL = {
    "fractional": "Fractional SEIT",
    "integer": "Integer SEIT (refitted)",
    "persistence": "Persistence",
    "seasonal_naive_12": "Seasonal naive (lag 12)",
    "SARIMA": "SARIMA(0,1,2)(1,1,1)$_{12}$",
}
# Okabe-Ito palette; within-family models solid, external baselines dashed.
STYLE = {
    "fractional": dict(color="#0072B2", ls="-", marker="o"),
    "integer": dict(color="#D55E00", ls="-", marker="s"),
    "persistence": dict(color="#555555", ls="--", marker="^"),
    "seasonal_naive_12": dict(color="#009E73", ls="--", marker="D"),
    "SARIMA": dict(color="#CC79A7", ls="--", marker="v"),
}
BASELINES = ["persistence", "seasonal_naive_12", "SARIMA"]

plt.rcParams.update({
    "font.size": 9, "axes.labelsize": 9, "axes.titlesize": 9, "legend.fontsize": 8,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "axes.spines.top": False,
    "axes.spines.right": False, "mathtext.default": "regular",
})


def save(fig, name):
    fig.savefig(FIG / f"{name}.png", dpi=600, bbox_inches="tight")
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def metric_vs_horizon(ax, df, col, ylabel):
    for m, st in STYLE.items():
        s = df[df.model == m].sort_values("horizon")
        assert len(s) == 12 and (s.n_forecasts == 13).all()
        ax.plot(s.horizon, s[col], label=LABEL[m], lw=1.4, ms=4, **st)
    ax.set_xticks(range(1, 13))
    ax.set_xlabel("Forecast horizon $h$ (months)")
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", lw=0.3, alpha=0.6)


def fig1(fc):
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    metric_vs_horizon(ax, fc, "RMSE", "RMSE (notified cases per month)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3, frameon=False)
    save(fig, "Figure1_rmse_vs_horizon")


def fig2(sk):
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6), sharey=True)
    lo = 0.0
    for ax, metric, tag in zip(axes, ["RMSE", "MAE"], ["A", "B"]):
        for b in BASELINES:
            s = sk[(sk.model == "fractional") & (sk.baseline == b) & (sk.metric == metric)].sort_values("horizon")
            assert len(s) == 12
            ax.plot(s.horizon, s.skill, label=f"vs {LABEL[b]}", lw=1.4, ms=4, **STYLE[b])
            lo = min(lo, s.skill.min())
        ax.axhline(0, color="black", lw=0.8)
        ax.set_xticks(range(1, 13))
        ax.set_xlabel("Forecast horizon $h$ (months)")
        ax.set_title(f"({tag}) {metric}-based skill", loc="left", fontweight="bold")
        ax.grid(axis="y", lw=0.3, alpha=0.6)
    axes[0].set_ylabel("Skill = 1 $-$ error$_{fractional}$ / error$_{baseline}$")
    axes[0].set_ylim(lo - 0.05, None)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.04))
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    save(fig, "Figure2_skill_vs_horizon")


def r0_admissible():
    p = pd.read_csv(ROOT / "outputs/identifiability/profile_objective.csv")
    m = pd.read_csv(ROOT / "outputs/identifiability/multiseed_functionals.csv")
    thr = 1.01 * 605.048881003205  # canonical primary-seed calibration RMSE x 1.01
    r = np.concatenate([p[p.calibration_rmse <= thr].R0_diagnostic.values, m.R0_diagnostic.values])
    s = pd.read_csv(CANON / "03_R0_stability/table_R0_stability_summary.csv").iloc[0]
    assert len(r) == int(s.n_solutions) == 25
    for v, k in [(r.min(), "R0_min"), (np.percentile(r, 25), "R0_Q1"), (np.median(r), "R0_median"),
                 (np.percentile(r, 75), "R0_Q3"), (r.max(), "R0_max")]:
        assert abs(v - s[k]) < 1e-9, (k, v, s[k])
    return np.sort(r), s


def fig3():
    r, s = r0_admissible()
    fig, ax = plt.subplots(figsize=(6.2, 2.4))
    # deterministic vertical offsets so that overlapping dots stay visible
    y = -0.30 + 0.06 * (np.arange(len(r)) % 5)
    ax.hlines(0.12, s.R0_min, s.R0_max, color="#0072B2", lw=1.2, zorder=1)
    ax.add_patch(plt.Rectangle((s.R0_Q1, 0.05), s.R0_Q3 - s.R0_Q1, 0.14, fc="#9ecae1",
                               ec="#0072B2", lw=1, zorder=2))
    ax.vlines(s.R0_median, 0.05, 0.19, color="#003f66", lw=2, zorder=3)
    ax.scatter(r, y, s=14, color="#0072B2", alpha=0.85, zorder=4)
    ax.axvline(1, color="black", ls="--", lw=0.9)
    ax.text(1.002, 0.38, "$R_0 = 1$", ha="left", va="center")
    ax.text(s.R0_max, 0.27, f"min\u2013max: {s.R0_min:.4f}\u2013{s.R0_max:.4f}", ha="right", va="bottom")
    ax.set_xlim(0.995, 1.20)
    ax.set_ylim(-0.45, 0.5)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Derived basic reproduction number $R_0$")
    save(fig, "Figure3_R0_envelope")


def figS1(fc):
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    metric_vs_horizon(ax, fc, "bias", "Mean forecast bias, $\\hat{y}-y$ (cases per month)")
    ax.axhline(0, color="black", lw=0.8)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3, frameon=False)
    save(fig, "FigureS1_bias_vs_horizon")


def tables():
    hs = pd.read_csv(CANON / "05_rolling_origin/table_horizon_summary.csv")
    names = {"persistence": "Persistence", "seasonal_naive_12": "Seasonal naive (lag 12)", "SARIMA": "SARIMA"}
    wide = hs.pivot(index="baseline", columns="metric", values=["H_relax", "H_strict_from_h1"])
    t1 = pd.DataFrame({
        "Baseline": [names[b] for b in BASELINES],
        "H_relax (RMSE)": [int(wide.loc[b, ("H_relax", "RMSE")]) for b in BASELINES],
        "H_relax (MAE)": [int(wide.loc[b, ("H_relax", "MAE")]) for b in BASELINES],
        "H_strict-from-h1 (RMSE)": [int(wide.loc[b, ("H_strict_from_h1", "RMSE")]) for b in BASELINES],
        "H_strict-from-h1 (MAE)": [int(wide.loc[b, ("H_strict_from_h1", "MAE")]) for b in BASELINES],
    })
    t1.to_csv(TAB / "Table1_horizon_descriptors.csv", index=False)
    (TAB / "Table1_horizon_descriptors.md").write_text(t1.to_markdown(index=False) + "\n")

    s = pd.read_csv(CANON / "03_R0_stability/table_R0_stability_summary.csv").iloc[0]
    t2 = pd.DataFrame({
        "Quantity": ["Admissible solutions (n)", "R0 minimum", "R0 first quartile", "R0 median",
                     "R0 third quartile", "R0 maximum", "DFE locally unstable (Matignon)",
                     "DFE locally stable", "DFE ambiguous"],
        "Value": [int(s.n_solutions), f"{s.R0_min:.4f}", f"{s.R0_Q1:.4f}", f"{s.R0_median:.4f}",
                  f"{s.R0_Q3:.4f}", f"{s.R0_max:.4f}", f"{int(s.DFE_unstable)}/25",
                  f"{int(s.DFE_stable)}/25", f"{int(s.DFE_ambiguous)}/25"],
    })
    t2.to_csv(TAB / "Table2_R0_envelope_DFE.csv", index=False)
    (TAB / "Table2_R0_envelope_DFE.md").write_text(t2.to_markdown(index=False) + "\n")
    print(t1.to_string(index=False)); print(t2.to_string(index=False))


def main():
    FIG.mkdir(parents=True, exist_ok=True); TAB.mkdir(parents=True, exist_ok=True)
    fc = pd.read_csv(CANON / "05_rolling_origin/table_forecasting_by_horizon.csv")
    sk = pd.read_csv(CANON / "05_rolling_origin/table_skill_by_horizon.csv")
    fig1(fc); fig2(sk); fig3(); figS1(fc); tables()


if __name__ == "__main__":
    main()
