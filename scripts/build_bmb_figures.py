#!/usr/bin/env python3
"""Typeset submission figures for the BMB manuscript from frozen canonical CSVs.

Presentation only. No model is run and no metric is recomputed: every plotted
series is read from `results_canonical/` (Figures 1, 2, S1; summary of Figure 3)
or from the frozen `outputs/identifiability/` files (the 25 individual R0 values
of Figure 3, which are checked against the frozen summary table).

The canonical PNGs in `results_canonical/06_figures/` are not modified. Output goes
to `submission_bmb/figures/` as vector PDF and 600-dpi PNG.

Every plotted line is read back from the Matplotlib artists and compared with the
CSV values; the script aborts on any mismatch.
"""
import csv
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "results_canonical"
OUT = ROOT / "submission_bmb" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update(
    {
        "font.size": 8,
        "axes.labelsize": 8.5,
        "axes.titlesize": 8.5,
        "legend.fontsize": 7,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "savefig.dpi": 600,
    }
)

# Okabe-Ito palette; marker and line style also differ so the figures stay legible in grayscale.
STYLE = {
    "fractional": dict(label="Fractional SEIT", color="#0072B2", marker="o", ls="-", lw=1.8, ms=4.5, zorder=5),
    "integer": dict(label="Integer SEIT (refitted)", color="#56B4E9", marker="s", ls="--", lw=1.4, ms=4, zorder=4),
    "persistence": dict(label="Persistence", color="#000000", marker="^", ls=":", lw=1.4, ms=4.5, zorder=3),
    "seasonal_naive_12": dict(label="Seasonal naive (lag 12)", color="#009E73", marker="D", ls="-.", lw=1.4, ms=3.5, zorder=3),
    "SARIMA": dict(label="SARIMA(0,1,2)(1,1,1)$_{12}$", color="#CC79A7", marker="v", ls="--", lw=1.4, ms=4.5, zorder=3),
}
WITHIN = ["fractional", "integer"]
EXTERNAL = ["persistence", "seasonal_naive_12", "SARIMA"]
HORIZONS = list(range(1, 13))
CHECKS = []


def read(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def by_horizon(rows, metric):
    out = {}
    for r in rows:
        out.setdefault(r["model"], {})[int(r["horizon"])] = float(r[metric])
    return {m: [v[h] for h in HORIZONS] for m, v in out.items()}


def plot_series(ax, model, y):
    s = dict(STYLE[model])
    line, = ax.plot(HORIZONS, y, label=s.pop("label"), **s)
    CHECKS.append((line, y, model))
    return line


def verify():
    bad = 0
    for line, expected, tag in CHECKS:
        got = np.asarray(line.get_ydata(), dtype=float)
        if not np.allclose(got, np.asarray(expected, dtype=float), rtol=0, atol=1e-12):
            print("MISMATCH", tag)
            bad += 1
    if bad:
        sys.exit("figure data do not match the frozen CSVs")
    print(f"verified {len(CHECKS)} plotted series against frozen CSVs")


def grouped_legend(ax, loc, anchor=None):
    handles = [Line2D([], [], linestyle="none", label=r"$\bf{Within\ family}$")]
    handles += [Line2D([], [], **{k: v for k, v in STYLE[m].items() if k not in ("zorder",)}) for m in WITHIN]
    handles += [Line2D([], [], linestyle="none", label=r"$\bf{External\ baselines}$")]
    handles += [Line2D([], [], **{k: v for k, v in STYLE[m].items() if k not in ("zorder",)}) for m in EXTERNAL]
    ax.legend(handles=handles, loc=loc, bbox_to_anchor=anchor, frameon=False, handlelength=2.6, labelspacing=0.35)


def style_axes(ax, ylabel):
    ax.set_xticks(HORIZONS)
    ax.set_xlabel("Forecast horizon $h$ (months)")
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.5)
    ax.set_axisbelow(True)


def save(fig, name):
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"{name}.{ext}", bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------------------- Figure 1
fc = read(CANON / "05_rolling_origin" / "table_forecasting_by_horizon.csv")
rmse = by_horizon(fc, "RMSE")
fig, ax = plt.subplots(figsize=(6.8, 3.6))
for m in WITHIN + EXTERNAL:
    plot_series(ax, m, rmse[m])
style_axes(ax, "RMSE (notifications per month)")
ax.set_ylim(250, 2200)
grouped_legend(ax, "lower right")
save(fig, "Fig1_rmse_by_horizon")

# --------------------------------------------------------------------------- Figure 2
sk = read(CANON / "05_rolling_origin" / "table_skill_by_horizon.csv")


def skill(metric):
    out = {}
    for r in sk:
        if r["model"] == "fractional" and r["metric"] == metric:
            out.setdefault(r["baseline"], {})[int(r["horizon"])] = float(r["skill"])
    return {b: [v[h] for h in HORIZONS] for b, v in out.items()}


fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.3), sharey=False)
for ax, metric, tag, ylab in (
    (axes[0], "RMSE", "A", r"Skill$_{\mathrm{RMSE}} = 1-\mathrm{RMSE}_M/\mathrm{RMSE}_B$"),
    (axes[1], "MAE", "B", r"Skill$_{\mathrm{MAE}} = 1-\mathrm{MAE}_M/\mathrm{MAE}_B$"),
):
    s = skill(metric)
    for b in EXTERNAL:
        plot_series(ax, b, s[b])
    ax.axhline(0, color="#444444", linewidth=0.8, linestyle="-", zorder=1)
    style_axes(ax, ylab)
    ax.text(-0.17, 1.04, tag, transform=ax.transAxes, fontsize=10, fontweight="bold")
handles = [Line2D([], [], **{k: v for k, v in STYLE[m].items() if k != "zorder"}) for m in EXTERNAL]
fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, handlelength=2.6, bbox_to_anchor=(0.5, 0.0))
fig.tight_layout(rect=(0, 0.07, 1, 1))
save(fig, "Fig2_skill_by_horizon")

# --------------------------------------------------------------------------- Figure 3
summ = read(CANON / "03_R0_stability" / "table_R0_stability_summary.csv")[0]
frozen = {k: float(summ[k]) for k in ("R0_min", "R0_Q1", "R0_median", "R0_Q3", "R0_max")}
base_rmse = float(read(ROOT / "outputs" / "calibration" / "fractional_multiseed.csv")[0]["objective"])
seeds = [float(r["R0_diagnostic"]) for r in read(ROOT / "outputs" / "identifiability" / "multiseed_functionals.csv")]
prof = [
    float(r["R0_diagnostic"])
    for r in read(ROOT / "outputs" / "identifiability" / "profile_objective.csv")
    if float(r["calibration_rmse"]) / base_rmse - 1.0 <= 0.01
]
allv = np.array(sorted(seeds + prof))
rebuilt = dict(
    R0_min=allv.min(), R0_Q1=np.quantile(allv, 0.25), R0_median=np.median(allv), R0_Q3=np.quantile(allv, 0.75), R0_max=allv.max()
)
assert len(allv) == int(summ["n_solutions"]) == 25, "admissible set size differs from the frozen table"
for k, v in frozen.items():
    assert abs(rebuilt[k] - v) < 1e-12, f"{k}: rebuilt {rebuilt[k]} vs frozen {v}"
print("Figure 3: 25 individual R0 values reproduce the frozen summary exactly")

fig, ax = plt.subplots(figsize=(6.8, 1.9))
ax.plot([frozen["R0_min"], frozen["R0_max"]], [0, 0], color="#9ECAE1", lw=9, solid_capstyle="butt", zorder=1)
ax.plot([frozen["R0_Q1"], frozen["R0_Q3"]], [0, 0], color="#0072B2", lw=9, solid_capstyle="butt", zorder=2)
ax.plot([frozen["R0_median"]], [0], marker="D", color="white", mec="black", ms=5, zorder=4, ls="none")
rng = np.random.default_rng(20260815)  # fixed seed: vertical jitter only
ax.plot(seeds, rng.uniform(0.18, 0.34, len(seeds)), "o", color="#D55E00", ms=4, zorder=5, ls="none")
ax.plot(prof, rng.uniform(-0.34, -0.18, len(prof)), "o", mfc="white", mec="#D55E00", ms=4, zorder=5, ls="none")
ax.axvline(1.0, color="#444444", linestyle="--", linewidth=1)
ax.text(1.003, 0.52, "$R_0 = 1$", fontsize=7.5, va="top")
ax.set_xlim(0.98, 1.22)
ax.set_ylim(-0.6, 0.6)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.set_xlabel(r"$R_0$ diagnostic functional $\beta\sigma/[(\sigma+\mu)(\gamma+\mu+d)]$")
handles = [
    Line2D([], [], color="#9ECAE1", lw=6, label="Range of the 25 solutions"),
    Line2D([], [], color="#0072B2", lw=6, label="Interquartile range"),
    Line2D([], [], marker="D", color="white", mec="black", ms=5, ls="none", label="Median"),
    Line2D([], [], marker="o", color="#D55E00", ms=4, ls="none", label="Multiseed solutions ($n=5$)"),
    Line2D([], [], marker="o", mfc="white", mec="#D55E00", ms=4, ls="none", label="Profile-objective solutions ($n=20$)"),
]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.42), ncol=3, frameon=False, handlelength=1.8)
save(fig, "Fig3_R0_envelope")

# --------------------------------------------------------------------------- Figure S1
bias = by_horizon(fc, "bias")
fig, ax = plt.subplots(figsize=(6.8, 3.6))
for m in WITHIN + EXTERNAL:
    plot_series(ax, m, bias[m])
ax.axhline(0, color="#444444", linewidth=0.8, zorder=1)
style_axes(ax, r"Mean bias $\hat{y}-y$ (notifications per month)")
ax.set_ylim(-2150, 150)
grouped_legend(ax, "upper right", anchor=(1.0, 0.93))
save(fig, "FigS1_bias_by_horizon")

verify()
