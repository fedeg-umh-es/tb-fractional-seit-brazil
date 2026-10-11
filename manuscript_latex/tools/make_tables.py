"""Generate the LaTeX tables of the manuscript from the analysis outputs (no numbers typed by hand).

Run from the repository root:  python manuscript_latex/tools/make_tables.py
Inputs : analyses/A1_*, analyses/A2_tables_*, analyses/A3_*, evidence_S1 phase 1 (read-only)
Outputs: manuscript_latex/tables/*.tex
"""
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
from tb_seit.r0 import r0_diagnostic  # noqa: E402

OUT = REPO / "manuscript_latex" / "tables"
A1 = REPO / "analyses" / "A1_bound_sensitivity_2026-10-11"
A2 = REPO / "analyses" / "A2_tables_2026-10-11"
A3 = REPO / "analyses" / "A3_sarima_coefficients_2026-10-11"
P1 = REPO / "evidence_S1/TB_SEIT_EVIDENCE_FREEZE_2026-10-10/phase1/tb_global_refit_phase1/results_global_primary"
MU = 1 / 888


def tex_table(caption, label, header, rows, colspec, size="scriptsize", tabcolsep="3pt"):
    r"""Same pattern as Tables 1-5 of the manuscript (sn-jnl redefines table/tabular: no \resizebox, no \parbox)."""
    lines = [r"\begin{table}[htbp]", r"\centering", rf"\{size}", rf"\caption{{{caption}}}", rf"\label{{{label}}}",
             rf"\begingroup\setlength{{\tabcolsep}}{{{tabcolsep}}}", rf"\begin{{tabular}}{{{colspec}}}", r"\toprule",
             " & ".join(header) + r" \\", r"\midrule"]
    lines += [" & ".join(r) + r" \\" for r in rows]
    lines += [r"\bottomrule", r"\end{tabular}", r"\endgroup", r"\end{table}", ""]
    return "\n".join(lines)


def fmt_change(x):
    """Relative change as LaTeX, with a real minus sign."""
    v = 100 * x
    return f"({'$-$' if v < 0 else '+'}{abs(v):.1f}\\%)"


def sensitivity():
    f1 = pd.read_csv(A1 / "fit_parameters.csv", float_precision="round_trip").set_index("id")
    f2 = pd.read_csv(A1 / "fit_parameters_continuation.csv", float_precision="round_trip").set_index("id")
    f3 = pd.read_csv(A1 / "fit_parameters_I-b.csv", float_precision="round_trip").set_index("id")
    p = pd.read_csv(P1 / "global_refit_parameters.csv", float_precision="round_trip").set_index("model")
    m = pd.read_csv(P1 / "global_refit_metrics.csv", float_precision="round_trip")
    i0 = p.loc["integer"]
    r0_i0 = r0_diagnostic(i0.beta, i0.sigma, i0.gamma, i0.d, MU)
    tr_i0 = float(m[(m.model == "integer") & (m.split == "calibration")].rmse.iloc[0])
    va_i0 = float(m[(m.model == "integer") & (m.split == "validation_open_loop")].rmse.iloc[0])
    rows_src = [
        ("F-0", "0.5--1", "0.01--0.5", f2.loc["F-0"], None),
        ("F-a$^{\\dagger}$", "0.2--1", "0.01--0.5", f1.loc["F-a"], True),
        ("F-b", "0.5--1", "0.001--0.5", f2.loc["F-b"], True),
        ("F-c$^{\\dagger}$", "0.2--1", "0.001--0.5", f2.loc["F-c"], True),
    ]
    rows = []
    for name, ab, sb, r, flag in rows_src:
        chg = "--" if flag is None else fmt_change(r.train_rmse_rel_change_vs_S1_primary)
        rows.append([name, ab, sb, f"{r.alpha:.4f}", f"{r.sigma:.4f}", f"{r.d:.4f}", f"{r.train_rmse:.1f}", chg, f"{r.val_rmse:.1f}", f"{r.R0_reference:.3f}"])
    rows.append(["I-0", "1", "0.01--0.5", "1", f"{i0.sigma:.4f}", f"{i0.d:.4f}", f"{tr_i0:.1f}", "--", f"{va_i0:.1f}", f"{r0_i0:.3f}$^{{\\ddagger}}$"])
    r = f3.loc["I-b"]
    rows.append(["I-b", "1", "0.001--0.5", "1", f"{r.sigma:.4f}", f"{r.d:.4f}", f"{r.train_rmse:.1f}", fmt_change(r.train_rmse_rel_change_vs_S1_primary), f"{r.val_rmse:.1f}", f"{r.R0_reference:.3f}"])
    hdr = ["Fit", r"$\alpha$ range", r"$\sigma$ range", r"$\hat\alpha$", r"$\hat\sigma$", r"$\hat d$", "Train RMSE", "Change", "Valid. RMSE", r"$R_0^{\mathrm{ref}}$"]
    cap = ("Sensitivity of the global fits to the lower bounds of $\\alpha$ and $\\sigma$. F-0, F-a, F-b and F-c are fractional fits; I-0 and I-b are integer fits (F-0 and I-0 are the primary fits). "
           "Ranges are the search bounds; $\\hat\\alpha$, $\\hat\\sigma$ and $\\hat d$ are the fitted values (month$^{-1}$ for $\\sigma$ and $d$). "
           "Change is the relative change of the training RMSE against the primary fit of the same model. Valid. RMSE is the open-loop RMSE for 2021--2022. "
           "One differential-evolution run per fit (seed 20260815), calibration 2001--2020, ordinary monthly observation operator; bounds of $\\beta$, $\\gamma$ and $d$ unchanged. "
           "No rolling-origin evaluation was run with the wider bounds. "
           "$^\\dagger$ The maximum pointwise relative change between steps of 1 and 0.25 months was 1.01\\% (above the 1\\% threshold); changes in RMSE, MAE and bias were below 0.07\\%. "
           "$^\\ddagger$ Computed for this table with the same function as for the fractional fits; not part of the main diagnostics.")
    (OUT / "table_sensitivity.tex").write_text(tex_table(cap, "tab:sens", hdr, rows, "@{}lllrrrrrrr@{}", tabcolsep="2pt"))


def sarima():
    d = pd.read_csv(A3 / "sarima_coefficients_by_origin.csv")
    cols = [("ma.L1", r"MA(1)"), ("ma.L2", r"MA(2)"), ("ar.S.L12", r"SAR(12)"), ("ma.S.L12", r"SMA(12)")]
    rows = []
    for _, r in d.iterrows():
        rows.append([r["origin"][:7], str(int(r["n_train"]))] + [f"{r[c]:.3f} ({r[c + '_se']:.3f})".replace("-", "$-$") for c, _ in cols] + [f"{r['aic']:.1f}"])
    hdr = ["Origin", "$n$"] + [lab for _, lab in cols] + ["AIC"]
    cap = (r"Origin-specific SARIMA coefficients for the 13 rolling origins: estimate (standard error). Order $(0,1,2)(1,1,1)_{12}$, expanding training window, fitted with "
           r"\texttt{enforce\_stationarity=False} and \texttt{enforce\_invertibility=False}, as in the archived forecasts. "
           r"The seasonal MA estimate lies at the invertibility boundary, and its standard error (1.2--2.6) is not informative there. "
           r"Regenerated forecasts reproduce the archived ones with a maximum relative error of $9.2\times10^{-9}$.")
    (OUT / "table_sarima.tex").write_text(tex_table(cap, "tab:sarima", hdr, rows, "@{}lrccccr@{}", tabcolsep="3pt"))


def metric_tables():
    full = pd.read_csv(A2 / "metrics_full_by_horizon.csv")
    methods = ["fractional", "integer", "persistence", "seasonal_naive_12", "SARIMA"]
    heads = ["Fractional", "Integer", "Persistence", "Seasonal naive", "SARIMA"]
    spec = {"MAE": (1, "Mean absolute error (cases per month) by lead and method, rolling origin (13 origins).", "tab:mae_h"),
            "bias": (1, "Mean bias, mean(predicted $-$ observed) (cases per month), by lead and method. Negative values indicate under-prediction.", "tab:bias_h"),
            "MASE": (3, "Mean absolute scaled error by lead and method. The scale is the in-sample MAE of the seasonal naive ($m=12$) on each origin's training window; values are averaged over the 13 origins.", "tab:mase_h")}
    for metric, (nd, cap, lab) in spec.items():
        wide = full.pivot(index="horizon", columns="model", values=metric)
        rows = [[str(h)] + [f"{wide.loc[h, m]:.{nd}f}".replace("-", "$-$") for m in methods] for h in wide.index]
        (OUT / f"table_{metric}.tex").write_text(tex_table(cap, lab, ["Lead (months)"] + heads, rows, "@{}lrrrrr@{}", size="small", tabcolsep="6pt"))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    sensitivity(); sarima(); metric_tables()
    print("ok")
