#!/usr/bin/env python3
"""Build the submission tables for the BMB manuscript from frozen files (standard library only).

Presentation only. Values are read from `results_canonical/`, from the frozen
`outputs/calibration/` and `outputs/identifiability/` files, and from the canonical
series `data/raw/tb_mes.xlsx`. Nothing is recomputed except display quantities that
are checked against the frozen summaries (the script aborts if a check fails):
  * the pooled 33-solution profile pool must reproduce `table_full_profile_diagnostic.csv`;
  * its <=1% subset must reproduce `table_R0_stability_summary.csv` (n, min, max);
  * annual totals from the xlsx must equal the observed series stored in `outputs/`.

Writes `submission_bmb/tables/*.md` (one file per table, caption included) and the
assembled `submission_bmb/BMB_SUPPLEMENTARY_INFORMATION.md`.
"""
import csv
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "results_canonical"
OUTS = ROOT / "outputs"
TAB = ROOT / "submission_bmb" / "tables"
TAB.mkdir(parents=True, exist_ok=True)

MODELS = ["fractional", "integer", "persistence", "seasonal_naive_12", "SARIMA"]
LABEL = {
    "fractional": "Fractional",
    "integer": "Integer",
    "persistence": "Persistence",
    "seasonal_naive_12": "Seasonal naive",
    "SARIMA": "SARIMA",
}
BASELINES = ["persistence", "seasonal_naive_12", "SARIMA"]
HORIZONS = list(range(1, 13))


def read(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def md(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] + ["---:"] * (len(headers) - 1)) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def write(name, caption, body, note=None):
    text = f"**{caption}**\n\n{body}\n"
    if note:
        text += f"\n{note}\n"
    (TAB / f"{name}.md").write_text(text)
    return text


# --------------------------------------------------------------------------- Table 1
hs = read(CANON / "05_rolling_origin" / "table_horizon_summary.csv")
rows = [
    [LABEL[r["baseline"]], r["metric"], r["H_relax"], r["H_strict_from_h1"], r["longest_positive_run_if_available"]]
    for r in hs
]
T1 = write(
    "table1",
    "Table 1. Empirical skill-horizon descriptors of the fractional SEIT model relative to each external baseline "
    "in the 13-origin expanding-window evaluation ($h = 1,\\dots,12$ months).",
    md(["Baseline", "Metric", "$H_{\\text{relax}}$", "$H_{\\text{strict-from-h1}}$", "Longest positive run"], rows),
    "$H_{\\text{relax}}$ is the largest horizon with positive observed skill; $H_{\\text{strict-from-h1}}$ is the largest $h$ "
    "such that skill is positive at every horizon from $h = 1$ to $h$; the last column is the longest run of consecutive "
    "positive-skill horizons. They describe this dataset and protocol only. They are not universal predictability limits, "
    "and no predictive-accuracy test was applied.",
)

# --------------------------------------------------------------------------- Table 2
s = read(CANON / "03_R0_stability" / "table_R0_stability_summary.csv")[0]
f4 = lambda k: f"{float(s[k]):.4f}"
T2 = write(
    "table2",
    "Table 2. Practical-identifiability envelope of the derived basic reproduction number $R_0$ and local stability of the "
    "Disease-Free Equilibrium (DFE) under Matignon's criterion for the predefined near-equivalent admissible set "
    "($n = 25$, $\\Delta\\mathrm{RMSE}_{\\mathrm{cal}} \\le 1.0\\%$).",
    md(
        ["$n$", "Min", "Q1", "Median", "Q3", "Max", "DFE stable", "DFE unstable", "DFE ambiguous"],
        [[s["n_solutions"], f4("R0_min"), f4("R0_Q1"), f4("R0_median"), f4("R0_Q3"), f4("R0_max"),
          s["DFE_stable"], s["DFE_unstable"], s["DFE_ambiguous"]]],
    ),
    "The range is an empirical envelope over calibration-equivalent solutions, not a confidence or credible interval. "
    "In all 25 solutions the latent-progression rate $\\sigma$ lay within about 2% of its lower search bound, so the envelope "
    "is conditional on that boundary value and on the single-compartment latent structure. The DFE classification follows "
    "from $R_0 > 1$ in every solution; it is not an independent result and not an assertion about real-world transmission.",
)

# --------------------------------------------------------------------------- Table S1A / S1B
ol = read(CANON / "04_long_open_loop" / "table_long_open_loop.csv")
S1A = write(
    "tableS1A",
    "Table S1A. Single-origin 24-month long open-loop stress test (calibration through 2020-12; continuous open-loop "
    "simulation for 2021-01 to 2022-12).",
    md(["Model", "RMSE", "MAE", "Bias"],
       [[r["model"].capitalize(), f"{float(r['RMSE']):.1f}", f"{float(r['MAE']):.1f}", f"{float(r['bias']):.1f}"] for r in ol]),
    "This is a stress test from one origin, not a forecasting-skill evaluation. Its values must not be compared with, "
    "or merged into, the 13-origin rolling-origin metrics in Table S1B. Bias is forecast minus observation "
    "(negative: under-prediction).",
)

fc = read(CANON / "05_rolling_origin" / "table_forecasting_by_horizon.csv")
g = {(int(r["horizon"]), r["model"]): r for r in fc}
blocks = []
for metric, title in (("RMSE", "RMSE"), ("MAE", "MAE"), ("bias", "Mean bias (forecast minus observation)")):
    body = md(
        ["$h$"] + [LABEL[m] for m in MODELS],
        [[h] + [f"{float(g[h, m][metric]):.1f}" for m in MODELS] for h in HORIZONS],
    )
    blocks.append(f"*{title}*\n\n{body}")
S1B = write(
    "tableS1B",
    "Table S1B. Rolling-origin evaluation (13 expanding-window origins, 2020-12 to 2021-12): horizon-specific RMSE, MAE "
    "and mean bias for each model and baseline ($n = 13$ forecasts per cell).",
    "\n\n".join(blocks),
    "Values are notifications per month. Persistence and seasonal naive coincide at $h = 12$ by construction. "
    "These values underlie Figure 1 and Figure S1. They are descriptive sample metrics.",
)

# --------------------------------------------------------------------------- Table S2
sk = read(CANON / "05_rolling_origin" / "table_skill_by_horizon.csv")
sg = {(r["model"], r["baseline"], r["metric"], int(r["horizon"])): float(r["skill"]) for r in sk}
blocks = []
for model in ("fractional", "integer"):
    heads = ["$h$"]
    for b in BASELINES:
        heads += [f"{LABEL[b]} (RMSE)", f"{LABEL[b]} (MAE)"]
    body = md(heads, [[h] + [f"{sg[model, b, m, h]:.3f}" for b in BASELINES for m in ("RMSE", "MAE")] for h in HORIZONS])
    blocks.append(f"*{LABEL[model]} SEIT relative to each external baseline*\n\n{body}")
S2 = write(
    "tableS2",
    "Table S2. Observed relative forecasting skill by horizon, $1 - \\mathrm{Error}_M(h)/\\mathrm{Error}_B(h)$, for the "
    "fractional and integer SEIT models against each external baseline (13 origins).",
    "\n\n".join(blocks),
    "Positive values indicate lower observed error for the SEIT model than for the baseline. These are descriptive sample "
    "comparisons; they were not subjected to a prespecified predictive-accuracy significance test. At $h = 12$ the "
    "persistence and seasonal-naive columns coincide by construction.",
)

# --------------------------------------------------------------------------- Table S3
base = float(read(OUTS / "calibration" / "fractional_multiseed.csv")[0]["objective"])
pool = []
for r in read(OUTS / "identifiability" / "multiseed_functionals.csv"):
    pool.append(("Multiseed, seed " + r["seed"], r["beta"], r["sigma"], r["gamma"], r["d"], r["alpha"],
                 r["calibration_rmse"], r["R0_diagnostic"]))
for r in read(OUTS / "identifiability" / "profile_objective.csv"):
    name = f"Profile, {r['profile_parameter'].replace('beta', 'β').replace('gamma', 'γ').replace('alpha', 'α')} fixed at {float(r['fixed_value']):.5g}"
    pool.append((name, r["optimized_beta"], r["optimized_sigma"], r["optimized_gamma"], r["optimized_d"],
                 r["optimized_alpha"], r["calibration_rmse"], r["R0_diagnostic"]))
rows, inside = [], []
for name, b, sg_, ga, d, a, rm, r0 in pool:
    delta = (float(rm) / base - 1.0) * 100.0
    adm = delta <= 1.0
    if adm:
        inside.append(float(r0))
    rows.append([name, f"{float(b):.4f}", f"{float(sg_):.5f}", f"{float(ga):.4f}", f"{float(d):.5f}", f"{float(a):.4f}",
                 f"{float(rm):.3f}", f"{delta:+.2f}", f"{float(r0):.4f}", "yes" if adm else "no"])
allr0 = [float(p[7]) for p in pool]
fp = read(CANON / "02_identifiability" / "table_full_profile_diagnostic.csv")[0]
assert len(pool) == int(fp["n"]) == 33
assert abs(min(allr0) - float(fp["R0_min"])) < 1e-12 and abs(max(allr0) - float(fp["R0_max"])) < 1e-12
assert sum(x < 1 for x in allr0) == int(fp["n_R0_lt_1"]) == 2 and sum(x > 1 for x in allr0) == int(fp["n_R0_gt_1"]) == 31
assert len(inside) == int(s["n_solutions"]) == 25
assert abs(min(inside) - float(s["R0_min"])) < 1e-12 and abs(max(inside) - float(s["R0_max"])) < 1e-12
print("Table S3: 33-solution pool and 25-solution admissible subset reproduce the frozen summaries")
S3 = write(
    "tableS3",
    "Table S3. Profile-objective diagnostic exploration: parameter values, calibration RMSE and $R_0$ for the 33 solutions "
    "pooled from the five multiseed fits and the 28 one-dimensional profile-objective fits.",
    md(["Solution", "$\\beta$", "$\\sigma$", "$\\gamma$", "$d$", "$\\alpha$", "Cal. RMSE", "$\\Delta$RMSE (%)", "$R_0$",
        "Admissible"], rows),
    "Each profile fit fixes one parameter at a grid value (seven points per parameter, never touching a bound) and "
    "re-optimizes the other four with the canonical seed (20260815) on the calibration window only. This is a "
    "profile-objective diagnostic exploration, not a formal profile-likelihood confidence analysis. $\\Delta$RMSE is "
    f"relative to the primary optimum ({base:.3f}). The 25 solutions with $\\Delta$RMSE $\\le 1.0\\%$ form the admissible set used "
    "for the primary $R_0$ and DFE statements; the remaining eight include deliberately poor-fit probes and do not support "
    "those statements. Two solutions in the pool have $R_0 < 1$ (β fixed at 0.0365 and 0.0563), so $R_0 > 1$ must not be "
    "stated for the whole pool. The profile grids reach at most 60% of the distance from the canonical value to each bound.",
)

# --------------------------------------------------------------------------- Table S4
BOUNDS = {"beta": (0.01, 1.0), "sigma": (0.01, 0.5), "gamma": (0.05, 0.30), "d": (0.0001, 0.05), "alpha": (0.5, 1.0)}


def near_bound(par, v):
    lo, hi = BOUNDS[par]
    return abs(v - lo) <= 0.02 * abs(lo) or abs(v - hi) <= 0.02 * abs(hi)


def fmt(par, v):
    txt = {"beta": f"{v:.4f}", "sigma": f"{v:.5f}", "gamma": f"{v:.4f}", "d": f"{v:.5f}", "alpha": f"{v:.4f}"}[par]
    return f"**{txt}**" if near_bound(par, v) else txt


rows = []
for model in ("fractional", "integer"):
    for r in read(OUTS / "calibration" / f"{model}_multiseed.csv"):
        v = {k: float(r[k]) for k in BOUNDS}
        rows.append([LABEL[model], r["seed"]] + [fmt(k, v[k]) if not (model == "integer" and k == "alpha") else "1 (fixed)" for k in BOUNDS]
                    + [f"{float(r['objective']):.3f}"])
S4 = write(
    "tableS4",
    "Table S4. Calibration results of the five optimizer seeds for the fractional and integer SEIT models under the frozen "
    "primary bounds (monthly units).",
    md(["Model", "Seed", "$\\beta$", "$\\sigma$", "$\\gamma$", "$d$", "$\\alpha$", "Cal. RMSE"], rows),
    "Primary bounds: $\\beta \\in [0.01, 1.00]$, $\\sigma \\in [0.01, 0.50]$, $\\gamma \\in [0.05, 0.30]$, "
    "$d \\in [0.0001, 0.05]$, $\\alpha \\in [0.50, 1.00]$ (fractional) or $\\alpha = 1$ (integer). Values within 2% of a bound "
    "are in bold. The primary calibration is seed 20260815; the other seeds are diagnostic. All ten fits reported "
    "convergence.",
)

# --------------------------------------------------------------------------- Table S5
def read_xlsx(path):
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path) as z:
        sheet = [n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml", n)][0]
        root = ET.fromstring(z.read(sheet))
    out = []
    for row in root.iter("{%s}row" % ns["m"]):
        cells = {}
        for c in row.findall("m:c", ns):
            v = c.find("m:v", ns)
            if v is not None and c.get("t") in (None, "n"):
                cells[re.match(r"[A-Z]+", c.get("r")).group()] = float(v.text)
        out.append(cells)
    return out


x = read_xlsx(ROOT / "data" / "raw" / "tb_mes.xlsx")
tot = {}
n_rows = 0
for cells in x:
    if "B" in cells and "D" in cells and 2001 <= cells["B"] <= 2022:
        tot[int(cells["B"])] = tot.get(int(cells["B"]), 0) + cells["D"]
        n_rows += 1
assert n_rows == 264, n_rows
obs = {}
for p in (OUTS / "calibration" / "fractional_predictions.csv", OUTS / "validation" / "fractional_predictions.csv"):
    for r in read(p):
        obs[r["date"][:7]] = float(r["observed"])
tot2 = {}
for k, v in obs.items():
    tot2[int(k[:4])] = tot2.get(int(k[:4]), 0) + v
assert tot == tot2, "annual totals from the xlsx differ from the observed series in outputs/"
print("Table S5: annual totals from tb_mes.xlsx equal the observed series stored in outputs/")
rows = []
for y in range(2001, 2023):
    ch = "" if y == 2001 else f"{(tot[y] / tot[y - 1] - 1) * 100:+.1f}"
    rows.append([y, f"{int(tot[y]):,}", ch])
S5 = write(
    "tableS5",
    "Table S5. Annual totals of monthly tuberculosis notifications in the canonical series (`data/raw/tb_mes.xlsx`, "
    "$N = 264$ months).",
    md(["Year", "Notifications", "Change vs previous year (%)"], rows),
    "Totals are sums of the 12 monthly values of each calendar year. The 2021–2022 evaluation window follows the 2020 "
    "decline and covers the subsequent rebound.",
)

# --------------------------------------------------------------------------- Supplementary Information
FIGS1 = (
    "**Figure S1.** Mean directional forecast bias ($\\hat{y} - y$) of each model and baseline across the 13 rolling origins "
    "as a function of forecast horizon. Negative values indicate under-prediction. All five methods under-predicted on "
    "average at every horizon. The evaluation window follows a 10.2% fall in annual notifications in 2020 and a rebound in "
    "2021–2022 (Table S5), so the shared negative bias is conditional on that level shift. The figure is diagnostic context; "
    "it is not evidence of model-specific causal failure or of forecasting superiority."
)
SI = f"""# Supplementary Information

**Fractional-order SEIT modelling and methodological evaluation of tuberculosis dynamics in Brazil**

This file collects the supplementary figure and tables cited in the main text. All values are read from frozen files:
`results_canonical/` for Tables S1, S2 and S3 (summary), and `outputs/calibration/` and `outputs/identifiability/` for
Tables S3 and S4. Table S5 is computed from the canonical series `data/raw/tb_mes.xlsx`. Nothing was recalculated. The
tables are regenerated with `python scripts/build_bmb_tables.py` and the figures with `python scripts/build_bmb_figures.py`;
both scripts check the displayed values against the frozen summaries.

---

![Figure S1](figures/FigS1_bias_by_horizon.png)

{FIGS1}

---

{S1A}
---

{S1B}
---

{S2}
---

{S3}
---

{S4}
---

{S5}"""
(ROOT / "submission_bmb" / "BMB_SUPPLEMENTARY_INFORMATION.md").write_text(SI)
print("wrote", len(list(TAB.glob("*.md"))), "table files and BMB_SUPPLEMENTARY_INFORMATION.md")
