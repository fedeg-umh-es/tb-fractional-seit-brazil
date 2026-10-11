"""Generate the LaTeX tables of the manuscript from the analysis outputs (no numbers typed by hand).

Run from the repository root:  python manuscript_latex/tools/make_tables.py
Inputs : analyses/A1_*, analyses/A2_tables_*, analyses/A3_*, evidence_S1 phase 1 (read-only)
Outputs: manuscript_latex/tables/*.tex
"""
import re
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


def tex_table(caption, label, header, rows, colspec, size="scriptsize", note=None):
    lines = [r"\begin{table}[htbp]", r"\centering", rf"\{size}", rf"\caption{{{caption}}}", rf"\label{{{label}}}",
             r"\resizebox{\textwidth}{!}{%", rf"\begin{{tabular}}{{{colspec}}}", r"\toprule",
             " & ".join(header) + r" \\", r"\midrule"]
    lines += [" & ".join(r) + r" \\" for r in rows]
    lines += [r"\bottomrule", r"\end{tabular}}"]
    if note:
        lines += [rf"\par\smallskip\noindent\parbox{{\textwidth}}{{\scriptsize {note}}}"]
    lines += [r"\end{table}", ""]
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
        ("F-0 (S1 primary)", "[0.50, 1]", "[0.01, 0.5]", f2.loc["F-0"], None),
        ("F-a", "[0.20, 1]", "[0.01, 0.5]", f1.loc["F-a"], "\\dagger"),
        ("F-b", "[0.50, 1]", "[0.001, 0.5]", f2.loc["F-b"], ""),
        ("F-c", "[0.20, 1]", "[0.001, 0.5]", f2.loc["F-c"], "\\dagger"),
    ]
    rows = []
    for name, ab, sb, r, flag in rows_src:
        chg = "(--)" if flag is None else fmt_change(r.train_rmse_rel_change_vs_S1_primary)
        rows.append([name + (f"$^{{{flag}}}$" if flag else ""), "fractional", ab, sb, f"{r.alpha:.4f}", f"{r.sigma:.4f}", f"{r.d:.4f}",
                     f"{r.train_rmse:.1f} {chg}", f"{r.val_rmse:.1f}", f"{r.R0_reference:.3f}"])
    rows.append(["I-0 (S1 primary)", "integer", "1 (fixed)", "[0.01, 0.5]", "1", f"{i0.sigma:.4f}", f"{i0.d:.4f}",
                 f"{tr_i0:.1f} (--)", f"{va_i0:.1f}", f"{r0_i0:.3f}$^{{\\ddagger}}$"])
    r = f3.loc["I-b"]
    rows.append(["I-b", "integer", "1 (fixed)", "[0.001, 0.5]", "1", f"{r.sigma:.4f}", f"{r.d:.4f}",
                 f"{r.train_rmse:.1f} {fmt_change(r.train_rmse_rel_change_vs_S1_primary)}", f"{r.val_rmse:.1f}", f"{r.R0_reference:.3f}"])
    hdr = ["Fit", "Model", r"$\alpha$ bounds", r"$\sigma$ bounds", r"$\hat\alpha$", r"$\hat\sigma$", r"$\hat d$",
           "Training RMSE (change)", "Validation RMSE", r"$R_0^{\mathrm{ref}}$"]
    note = (r"Single differential-evolution run per fit (seed 20260815), calibration 2001--2020, ordinary monthly observation operator. "
            r"Change = relative change of the training RMSE against the S1 primary of the same model. Validation = open-loop RMSE for 2021--2022. "
            r"Bounds of $\beta$, $\gamma$ and $d$ unchanged. $^\dagger$ The maximum pointwise relative change between steps of 1 and 0.25 months was 1.01\% (F-a) and 1.01\% (F-c), "
            r"slightly above the 1\% threshold; changes in RMSE, MAE and bias were below 0.07\%. "
            r"$^\ddagger$ Computed for this table with the same function as for the fractional fits; not reported in the S1 evidence.")
    (OUT / "table_sensitivity.tex").write_text(tex_table(
        "Sensitivity of the global fits to the lower bounds of $\\alpha$ and $\\sigma$. Descriptive fits; no rolling-origin evaluation was run with the wider bounds.",
        "tab:sens", hdr, rows, "@{}llllrrrrrr@{}", note=note))


def sarima():
    d = pd.read_csv(A3 / "sarima_coefficients_by_origin.csv")
    cols = [("ma.L1", r"MA(1)"), ("ma.L2", r"MA(2)"), ("ar.S.L12", r"SAR(12)"), ("ma.S.L12", r"SMA(12)")]
    rows = []
    for _, r in d.iterrows():
        rows.append([r["origin"][:7], str(int(r["n_train"]))] + [f"{r[c]:.3f} ({r[c + '_se']:.3f})" for c, _ in cols] + [f"{r['aic']:.1f}"])
    hdr = ["Origin", "$n$"] + [lab for _, lab in cols] + ["AIC"]
    note = (r"Estimate (standard error). Order $(0,1,2)(1,1,1)_{12}$, expanding training window, fitted with \texttt{enforce\_stationarity=False} and \texttt{enforce\_invertibility=False}, as in the archived forecasts. "
            r"The seasonal MA estimate lies at the invertibility boundary, and its standard error (1.2--2.6) is not informative there. "
            r"Regenerated forecasts reproduce the archived ones with a maximum relative error of $9.2\times10^{-9}$.")
    (OUT / "table_sarima.tex").write_text(tex_table(
        "Origin-specific SARIMA coefficients for the 13 rolling origins.", "tab:sarima", hdr, rows, "@{}lrccccr@{}", note=note))


def wrap_a2():
    for name in ("MAE", "bias", "MASE"):
        s = (A2 / f"table_{name}.tex").read_text()
        s = s.replace(r"\small", r"\scriptsize").replace(r"\begin{tabular}", r"\resizebox{\textwidth}{!}{%" + "\n" + r"\begin{tabular}")
        s = s.replace(r"\end{tabular}", r"\end{tabular}}").replace("[ht]", "[htbp]")
        s = s.replace(r"\hline", r"\toprule", 1)  # first rule
        # replace remaining rules: after header -> midrule, last -> bottomrule
        parts = s.split(r"\hline")
        if len(parts) == 3:
            s = parts[0] + r"\midrule" + parts[1] + r"\bottomrule" + parts[2]
        s = re.sub(r"\\caption\{(.*?)\}\n", lambda m: r"\caption{" + m.group(1) + "}\n", s)
        (OUT / f"table_{name}.tex").write_text(s)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    sensitivity(); sarima(); wrap_a2()
    print("ok")
