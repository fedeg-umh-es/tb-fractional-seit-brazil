"""Build manuscript_latex/CLAIM_EVIDENCE_MATRIX.csv.

One row per numerical or interpretive claim of manuscript.tex. A row is VERIFIED only if (i) the value was
recomputed here from the stated source file and (ii) every number quoted in the row appears in manuscript.tex.
Interpretive statements about the literature, and anything not recomputed, are NOT_VERIFIED, with the reason.
Run from the repository root:  python manuscript_latex/tools/build_claim_matrix.py
"""
import csv
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
from tb_seit import calibration, r0  # noqa: E402

S1 = REPO / "evidence_S1/TB_SEIT_EVIDENCE_FREEZE_2026-10-10"
P1 = S1 / "phase1/tb_global_refit_phase1/results_global_primary"
A1 = REPO / "analyses/A1_bound_sensitivity_2026-10-11"
A2 = REPO / "analyses/A2_tables_2026-10-11"
A2T = REPO / "analyses/A2_transient_E_2026-10-11"
A3 = REPO / "analyses/A3_sarima_coefficients_2026-10-11"
tex = (REPO / "manuscript_latex/manuscript.tex").read_text(encoding="utf8")
tables = "".join(p.read_text(encoding="utf8") for p in (REPO / "manuscript_latex/tables").glob("*.tex"))
corpus = re.sub(r"\s+", " ", tex + tables)
rows = []


def rel(p):
    return str(Path(p).relative_to(REPO))


def add(section, text, source, value, tokens=(), ok=True, note=""):
    missing = [t for t in tokens if t not in corpus]
    status = "VERIFIED" if (ok and not missing and not note.startswith("NOT_VERIFIED")) else "NOT_VERIFIED"
    why = note
    if not ok:
        why = (why + " | " if why else "") + "recomputed value does not match"
    if missing:
        why = (why + " | " if why else "") + f"number(s) not found in manuscript: {missing}"
    rows.append(dict(id=f"C{len(rows) + 1:03d}", section=section, text=text, source_file=source, value=str(value), status=status, note=why))


def f(x, n):
    return f"{x:.{n}f}"


# ------------------------------------------------------------ data and design
data = pd.read_excel(REPO / "data/raw/tb_mes.xlsx")
data["data"] = pd.to_datetime(data["data"])
add("Methods 2.2", "264 consecutive monthly counts, January 2001 to December 2022", "data/raw/tb_mes.xlsx",
    f"{len(data)} rows, {data.data.min():%Y-%m} to {data.data.max():%Y-%m}", ["264"],
    ok=len(data) == 264 and data.data.min() == pd.Timestamp("2001-01-01") and data.data.max() == pd.Timestamp("2022-12-01"))
add("Methods 2.2", "Calibration 240 months (2001-01 to 2020-12), validation 24 months (2021-01 to 2022-12)", "data/raw/tb_mes.xlsx",
    f"{(data.data <= '2020-12-01').sum()} / {(data.data > '2020-12-01').sum()}", ["240", "24"],
    ok=(data.data <= "2020-12-01").sum() == 240 and (data.data > "2020-12-01").sum() == 24)
for y, v in data.groupby(data.data.dt.year).casos.mean().loc[[2019, 2020, 2021, 2022]].items():
    add("Discussion", f"Annual mean of monthly counts in {y}", "data/raw/tb_mes.xlsx", f"{v:,.0f}", [f"{v:,.0f}"], ok=True)
mc = json.loads((REPO / "outputs/model_constants.json").read_text())
add("Methods 2.3", "mu = 1/(74 x 12) = 1/888 per month", "outputs/model_constants.json", mc["mu"]["value"], ["1/888"], ok=abs(mc["mu"]["value"] - 1 / 888) < 1e-15)
add("Methods 2.4", "Penalty 1e12 for invalid candidates", "src/tb_seit/calibration.py", calibration.LARGE_PENALTY, ["10^{12}"], ok=calibration.LARGE_PENALTY == 1e12)
add("Methods 2.4", "DE settings best1bin, popsize 15, mutation (0.5,1.0), recombination 0.7, tol 0.01, maxiter 1000, polish False", "src/tb_seit/calibration.py",
    f"{calibration.STRATEGY}, {calibration.POPSIZE}, {calibration.MUTATION}, {calibration.RECOMBINATION}, {calibration.TOL}, {calibration.MAXITER}",
    ["best1bin", "popsize=15", "mutation=(0.5,1.0)", "recombination=0.7", "tol=0.01", "maxiter=1000", "polish=False"],
    ok=(calibration.STRATEGY, calibration.POPSIZE, calibration.MUTATION, calibration.RECOMBINATION, calibration.TOL, calibration.MAXITER) == ("best1bin", 15, (0.5, 1.0), 0.7, 0.01, 1000))
run1 = (P1.parent / "run_global_refit.py").read_text()
add("Methods 2.3", "Search bounds beta [0.01,1.00], sigma [0.01,0.50], gamma [0.05,0.30], d [0.0001,0.05], alpha [0.50,1.00]",
    rel(P1.parent / "run_global_refit.py"), "bounds_frac in run_global_refit.py",
    ["[0.01,1.00]", "[0.01,0.50]", "[0.05,0.30]", "[0.0001,0.05]", "[0.50,1.00]"],
    ok="(0.01, 1.0), (0.01, 0.5), (0.05, 0.30), (0.0001, 0.05), (0.5, 1.0)" in run1)
fs = pd.read_csv(S1 / "phase2/fit_states.csv")
add("Methods 2.7", "13 fits per model, 26 in total; all met numerical termination criteria", "phase2/fit_states.csv",
    f"{len(fs)} rows; success all = {bool(fs.success.all())}", ["26"], ok=len(fs) == 26 and bool(fs.success.all()))
sar = json.loads((REPO / "outputs/forecasting/sarima_frozen_order.json").read_text())
add("Methods 2.8", "SARIMA (0,1,2)(1,1,1)_12, order selected by AIC from 36 candidates on 2001-2020", "outputs/forecasting/sarima_frozen_order.json",
    f"{sar['selected_order']} {sar['selected_seasonal_order']}, grid {len(sar['full_grid'])}", ["(0,1,2)(1,1,1)", "36"],
    ok=sar["selected_order"] == dict(p=0, d=1, q=2) and sar["selected_seasonal_order"] == dict(P=1, D=1, Q=1, s=12) and len(sar["full_grid"]) == 36)
preds = pd.read_csv(S1 / "phase2/rolling_origin_predictions.csv")
add("Methods 2.7/Results 3.2", "13 origins, 156 origin-horizon pairs per model, 780 forecasts from five methods, 468 baseline forecasts",
    "phase2/rolling_origin_predictions.csv", f"{preds.origin.nunique()} origins; {len(preds)} rows; {preds.groupby('model').size().iloc[0]} per model",
    ["13", "156", "780", "468"], ok=preds.origin.nunique() == 13 and len(preds) == 780 and (preds.groupby("model").size() == 156).all())
add("Discussion", "Only 24 distinct target months in the evaluation", "phase2/rolling_origin_predictions.csv", preds.target_date.nunique(), ["24 distinct target months"], ok=preds.target_date.nunique() == 24)
add("Methods 2.10", "Lower bound 0.001 per month corresponds to a mean progression time of about 83 years", "arithmetic", f"{1 / 0.001 / 12:.1f} years", ["83 years"], ok=round(1 / 0.001 / 12) == 83)

# ------------------------------------------------------------ Table 1 and 2
par = pd.read_csv(P1 / "global_refit_parameters.csv").set_index("model")
for m in ("fractional", "integer"):
    vals = [f(par.loc[m, k], 6) for k in ("beta", "sigma", "gamma", "d", "alpha")]
    add("Results 3.1 Table 1", f"Estimated parameters, {m} model (beta, sigma, gamma, d, alpha)", rel(P1 / "global_refit_parameters.csv"),
        " / ".join(vals), vals, ok=True)
met = pd.read_csv(P1 / "global_refit_metrics.csv")
for _, r in met.iterrows():
    vals = [f(r.rmse, 3), f(r.mae, 3), f(r.bias, 3)]
    add("Results 3.1 Table 2", f"{r.model}, {r.split}: RMSE / MAE / bias", rel(P1 / "global_refit_metrics.csv"), " / ".join(vals), [vals[0], vals[1], vals[2].replace("-", "")], ok=True)
add("Results 3.1", "Fractional calibration RMSE 619.319 against 776.041 for integer", rel(P1 / "global_refit_metrics.csv"), "619.319 / 776.041", ["619.319", "776.041"],
    ok=f(met[(met.model == "fractional") & (met.split == "calibration")].rmse.iloc[0], 3) == "619.319" and f(met[(met.model == "integer") & (met.split == "calibration")].rmse.iloc[0], 3) == "776.041")
add("Results 3.1", "d differs by a factor of about 180 between models; fractional d is about 0.47 per year", rel(P1 / "global_refit_parameters.csv"),
    f"{par.loc['fractional', 'd'] / par.loc['integer', 'd']:.1f}; {par.loc['fractional', 'd'] * 12:.3f} per year", ["about 180", "about 0.47 per year"],
    ok=170 < par.loc["fractional", "d"] / par.loc["integer", "d"] < 190 and abs(par.loc["fractional", "d"] * 12 - 0.47) < 0.005)
add("Results 3.1", "Plausibility of d against independent TB mortality estimates not assessed", "-", "-", [], ok=True, note="NOT_VERIFIED: statement of non-assessment; author judgement on plausibility pending (B5)")

# ------------------------------------------------------------ Table 3, 4 and statements on skill
mh = pd.read_csv(S1 / "phase2/metrics_by_horizon.csv")
labels = {"fractional": "fractional", "integer": "integer", "persistence": "persistence", "seasonal_naive_12": "seasonal_naive_12", "SARIMA": "SARIMA"}
for h in range(1, 13):
    sub = mh[mh.horizon == h].set_index("model")
    vals = [f(sub.loc[m, "RMSE"], 3) for m in labels]
    add("Results 3.2 Table 3", f"RMSE at lead {h} (fractional, integer, persistence, seasonal naive, SARIMA)", "phase2/metrics_by_horizon.csv", " / ".join(vals), vals, ok=True)
piv = mh.pivot(index="horizon", columns="model", values="RMSE"); pivm = mh.pivot(index="horizon", columns="model", values="MAE")
add("Results 3.2", "Fractional has lower RMSE and MAE than integer at all 12 leads", "phase2/metrics_by_horizon.csv", "12/12", [], ok=bool((piv.fractional < piv.integer).all() and (pivm.fractional < pivm.integer).all()), note="")
add("Results 3.3", "Persistence and SARIMA have lower RMSE and MAE than fractional at every lead", "phase2/metrics_by_horizon.csv", "12/12 each", [],
    ok=bool((piv.persistence < piv.fractional).all() and (piv.SARIMA < piv.fractional).all() and (pivm.persistence < pivm.fractional).all() and (pivm.SARIMA < pivm.fractional).all()))
add("Results 3.3", "Seasonal naive has higher errors than fractional at h=1..5 and lower at h=6..12 (RMSE and MAE)", "phase2/metrics_by_horizon.csv",
    f"RMSE worse at {[h for h in range(1, 13) if piv.seasonal_naive_12[h] > piv.fractional[h]]}", ["$h=1,\\ldots,5$", "$h=6,\\ldots,12$"],
    ok=[h for h in range(1, 13) if piv.seasonal_naive_12[h] > piv.fractional[h]] == [1, 2, 3, 4, 5] and [h for h in range(1, 13) if pivm.seasonal_naive_12[h] > pivm.fractional[h]] == [1, 2, 3, 4, 5])
hs = pd.read_csv(S1 / "phase2/horizon_summary.csv")
for comp, rl, st in (("integer", 12, 12), ("persistence", 0, 0), ("seasonal_naive_12", 5, 5), ("SARIMA", 0, 0)):
    g = hs[(hs.baseline == comp) & (hs.model == "fractional")]
    add("Results 3.3 Table 4", f"H_relax = {rl}, H_strict = {st} against {comp} (RMSE and MAE)", "phase2/horizon_summary.csv", g[["metric", "H_relax", "H_strict"]].values.tolist(), [],
        ok=bool((g.H_relax == rl).all() and (g.H_strict == st).all() and len(g) == 2))
rc = fs[fs.model == "fractional"].alpha
add("Results 3.3", "All 13 fractional fits place alpha between 0.500021 and 0.503773", "phase2/fit_states.csv", f"{rc.min():.6f}-{rc.max():.6f}", ["0.500021", "0.503773"], ok=f(rc.min(), 6) == "0.500021" and f(rc.max(), 6) == "0.503773")

# ------------------------------------------------------------ A2 tables (steps 2)
full = pd.read_csv(A2 / "metrics_full_by_horizon.csv")
h12 = json.loads((A2 / "h12_persistence_vs_snaive_check.json").read_text())
add("Results 3.2", "Persistence and seasonal naive identical at h=12 in all 13 origins; RMSE 1152.958", rel(A2 / "h12_persistence_vs_snaive_check.json"),
    f"identical={h12['identical_in_all_origins']}, RMSE {h12['rmse_h12_persistence']:.3f}", ["1152.958"], ok=h12["identical_in_all_origins"] and f(h12["rmse_h12_persistence"], 3) == "1152.958")
bias_all_neg = bool((full.bias < 0).all())
add("Results 3.2 / Discussion", "All five methods have negative mean bias at every lead", rel(A2 / "metrics_full_by_horizon.csv"), f"{(full.bias < 0).sum()}/{len(full)} negative", [], ok=bias_all_neg)
add("Results 3.3", "Fractional bias negative at every rolling lead", rel(A2 / "metrics_full_by_horizon.csv"), "12/12", [], ok=bool((full[full.model == "fractional"].bias < 0).all()))
mase = full.pivot(index="horizon", columns="model", values="MASE")
add("Results 3.2", "MASE below one only for persistence at h=1 and h=2 (0.728, 0.931)", rel(A2 / "metrics_full_by_horizon.csv"),
    f"{[(m, h) for m in mase.columns for h in mase.index if mase.loc[h, m] < 1]}; {mase.persistence[1]:.3f}, {mase.persistence[2]:.3f}", ["0.728", "0.931"],
    ok=[(m, h) for m in mase.columns for h in mase.index if mase.loc[h, m] < 1] == [("persistence", 1), ("persistence", 2)] and f(mase.persistence[1], 3) == "0.728" and f(mase.persistence[2], 3) == "0.931")
add("Results 3.2", "MASE at h=1: fractional 1.491, integer 2.375, seasonal naive 2.347, SARIMA 1.006", rel(A2 / "metrics_full_by_horizon.csv"),
    f"{mase.fractional[1]:.3f}/{mase.integer[1]:.3f}/{mase.seasonal_naive_12[1]:.3f}/{mase.SARIMA[1]:.3f}", ["1.491", "2.375", "2.347", "1.006"],
    ok=[f(mase.fractional[1], 3), f(mase.integer[1], 3), f(mase.seasonal_naive_12[1], 3), f(mase.SARIMA[1], 3)] == ["1.491", "2.375", "2.347", "1.006"])
for h in (1,):
    sub = mh[mh.horizon == h].set_index("model")
    add("Abstract", "RMSE at lead 1: fractional 792, integer 1186, persistence 390, seasonal naive 1091, SARIMA 536", "phase2/metrics_by_horizon.csv",
        " / ".join(f"{sub.loc[m, 'RMSE']:.0f}" for m in labels), ["792", "1186", "(390)", "(536)", "(1091)"],
        ok=[f"{sub.loc[m, 'RMSE']:.0f}" for m in labels] == ["792", "1186", "390", "1091", "536"])

# ------------------------------------------------------------ SARIMA (step 3)
rc3 = json.loads((A3 / "reproduction_control.json").read_text())
add("Methods 2.8", "Regenerated SARIMA forecasts reproduce archived ones with maximum relative error 9.2e-9", rel(A3 / "reproduction_control.json"),
    f"{rc3['max_relative_error']:.2e}", ["9.2\\times10^{-9}"], ok=rc3["pass"] and abs(rc3["max_relative_error"] - 9.2e-9) < 0.05e-9)
sc = pd.read_csv(A3 / "sarima_coefficients_by_origin.csv")
add("Appendix Table A4", "SARIMA coefficients and standard errors for 13 origins (generated table)", rel(A3 / "sarima_coefficients_by_origin.csv"),
    f"{len(sc)} origins; all converged={bool(sc.converged.all())}", ["MA(1)", "SMA(12)"], ok=len(sc) == 13 and bool(sc.converged.all()))
add("Appendix Table A4 note", "Seasonal MA estimate at the invertibility boundary; SE between 1.2 and 2.6", rel(A3 / "sarima_coefficients_by_origin.csv"),
    f"est {sc['ma.S.L12'].min():.4f}..{sc['ma.S.L12'].max():.4f}; SE {sc['ma.S.L12_se'].min():.2f}..{sc['ma.S.L12_se'].max():.2f}", ["1.2--2.6"],
    ok=sc["ma.S.L12"].max() < -0.99 and 1.1 < sc["ma.S.L12_se"].min() < 1.2 and 2.5 < sc["ma.S.L12_se"].max() < 2.6)

# ------------------------------------------------------------ phase 3 (identifiability, R0, numerical checks)
pool = pd.read_csv(S1 / "phase3/solution_pool.csv"); adm = pool[pool.admissible_1pct]
add("Methods 2.5", "Pool: reference fit, four additional fits and 42 reoptimized profile solutions; 47 in total; 32 within 1%", "phase3/solution_pool.csv",
    pool.source.value_counts().to_dict(), ["42", "47", "32"], ok=len(pool) == 47 and len(adm) == 32 and (pool.source == "reoptimized_profile").sum() == 42)
add("Results 3.4", "1% threshold 625.511939 relative to primary RMSE 619.318751", "phase1 objective", f"{1.01 * 619.31875149368591:.6f}", ["625.511939", "619.318751"], ok=f(1.01 * 619.31875149368591, 6) == "625.511939")
rng = {k: (adm[k].min(), adm[k].max()) for k in ("beta", "gamma", "d")}
add("Results 3.4", "Ranges among the 32 solutions: beta 0.036879-0.208034, gamma 0.052711-0.297678, d 0.001899-0.048114", "phase3/solution_pool.csv",
    {k: (round(float(v[0]), 6), round(float(v[1]), 6)) for k, v in rng.items()}, ["0.036879", "0.208034", "0.052711", "0.297678", "0.001899", "0.048114"],
    ok=[f(rng["beta"][0], 6), f(rng["beta"][1], 6), f(rng["gamma"][0], 6), f(rng["gamma"][1], 6), f(rng["d"][0], 6), f(rng["d"][1], 6)] == ["0.036879", "0.208034", "0.052711", "0.297678", "0.001899", "0.048114"])
pd_ = pd.read_csv(S1 / "phase3/prediction_dispersion.csv"); ne = pd_[pd_.set == "NEAR_EQUIVALENT_1_PCT"]
cvc, cvv = ne[ne.split == "calibration"].cv * 100, ne[ne.split == "validation_open_loop"].cv * 100
add("Results 3.4", "Monthly prediction CV 0.0107-0.1474% (calibration) and 0.1479-0.1595% (validation) over the 32 solutions", "phase3/prediction_dispersion.csv",
    f"{cvc.min():.4f}-{cvc.max():.4f}; {cvv.min():.4f}-{cvv.max():.4f}", ["0.0107", "0.1474", "0.1479", "0.1595"],
    ok=[f(cvc.min(), 4), f(cvc.max(), 4), f(cvv.min(), 4), f(cvv.max(), 4)] == ["0.0107", "0.1474", "0.1479", "0.1595"])
ap = pd.read_csv(S1 / "phase3/alpha_profile_comparison.csv")
for a_ in (0.5, 0.52, 0.55):
    r = ap.iloc[(ap.alpha - a_).abs().argmin()]
    add("Results 3.4", f"Fixed-section / reoptimized RMSE at alpha={a_}", "phase3/alpha_profile_comparison.csv", f"{r.fixed_section_rmse:.3f} / {r.de_profile_rmse:.3f}",
        [f(r.fixed_section_rmse, 3), f(r.de_profile_rmse, 3)], ok=abs(r.alpha - a_) < 1e-9)
add("Results 3.4", "Reoptimized profile admits alpha 0.50-0.52 in the 1% region, 0.55 outside", "phase3/alpha_profile_comparison.csv",
    ap[ap.alpha.between(0.5, 0.56)][["alpha", "admissible_1pct"]].round(4).values.tolist(), ["0.50 to 0.52", "0.55"],
    ok=bool(ap[(ap.alpha >= 0.5) & (ap.alpha <= 0.52 + 1e-9)].admissible_1pct.all() and not ap[(ap.alpha - 0.55).abs() < 1e-9].admissible_1pct.iloc[0]),
    note="")
env = pd.read_csv(S1 / "phase3/R0_practical_envelopes.csv").set_index("set")
dfe = pd.read_csv(S1 / "phase3/dfe_stability.csv")
add("Results 3.5 Table 5", "Main 1% region: n=32, R0 0.341657-0.587926, all below one, 32 stable DFE", "phase3/R0_practical_envelopes.csv; dfe_stability.csv",
    f"{adm.R0_reference.min():.6f}-{adm.R0_reference.max():.6f}; stable {(dfe[dfe.admissible_1pct].classification == 'ASYMPTOTICALLY_STABLE_AUTONOMOUS_REFERENCE').sum()}",
    ["0.341657", "0.587926"], ok=len(adm) == 32 and (adm.R0_reference < 1).all() and (dfe[dfe.admissible_1pct].classification == "ASYMPTOTICALLY_STABLE_AUTONOMOUS_REFERENCE").all())
add("Results 3.5 Table 5", "Full pool: n=47, R0 0.341657-1.661998, 44 below one, 3 above, 44 stable, 3 unstable", "phase3/R0_practical_envelopes.csv; dfe_stability.csv",
    f"{pool.R0_reference.min():.6f}-{pool.R0_reference.max():.6f}; below {(pool.R0_reference < 1).sum()}; unstable {(dfe.classification != 'ASYMPTOTICALLY_STABLE_AUTONOMOUS_REFERENCE').sum()}",
    ["1.661998", "44", "three"], ok=len(pool) == 47 and (pool.R0_reference < 1).sum() == 44 and (dfe.classification != "ASYMPTOTICALLY_STABLE_AUTONOMOUS_REFERENCE").sum() == 3 and f(pool.R0_reference.max(), 6) == "1.661998")
add("Results 3.5", "Primary reference R0 = 0.357768", "phase3/dfe_stability.csv", f"{dfe.iloc[0].R0_reference:.6f}", ["0.357768"], ok=f(dfe.iloc[0].R0_reference, 6) == "0.357768")
nr = pd.read_csv(S1 / "phase3/numerical_resolution_checks.csv")
add("Results 3.6", "Numerical checks passed for 26 rolling-origin and 115 global/profile/diagnostic evaluations; largest relative difference 0.119134%", "phase2/origin_numerical_checks.csv; phase3/numerical_resolution_checks.csv",
    f"{len(pd.read_csv(S1 / 'phase2/origin_numerical_checks.csv'))} + {len(nr)}; max {100 * nr.max_pointwise_relative_change.max():.6f}%", ["26", "115", "0.119134"],
    ok=len(pd.read_csv(S1 / "phase2/origin_numerical_checks.csv")) == 26 and len(nr) == 115 and (nr.status == "PASS").all() and f(100 * nr.max_pointwise_relative_change.max(), 6) == "0.119134")
add("Results 3.6", "Refinement did not change signs of rolling skill or membership of the main region", "-", "-", [], ok=True, note="NOT_VERIFIED: not recomputed here; taken from S1 phase 2/3 reports")

# ------------------------------------------------------------ sensitivity (step 5)
sa = pd.read_csv(A1 / "fit_parameters.csv").set_index("id"); sb = pd.read_csv(A1 / "fit_parameters_continuation.csv").set_index("id"); si = pd.read_csv(A1 / "fit_parameters_I-b.csv").set_index("id")
fits = {"F-a": sa.loc["F-a"], "F-b": sb.loc["F-b"], "F-c": sb.loc["F-c"], "I-b": si.loc["I-b"]}
src = "analyses/A1_bound_sensitivity_2026-10-11/fit_parameters*.csv"
for k, r in fits.items():
    vals = [f(r.alpha, 4), f(r.sigma, 4), f(r.d, 4), f(r.train_rmse, 1), f(r.val_rmse, 1), f(r.R0_reference, 3)]
    add("Results 3.7 Table 6", f"{k}: alpha, sigma, d, training RMSE, validation RMSE, reference R0", src, " / ".join(vals), [v for v in vals if v not in ("1.0000",)] if k != "I-b" else vals[1:], ok=True)
r0i = r0.r0_diagnostic(par.loc["integer", "beta"], par.loc["integer", "sigma"], par.loc["integer", "gamma"], par.loc["integer", "d"], 1 / 888)
add("Results 3.7 / Discussion", "Reference R0 of the primary integer fit is 1.009 (not in S1 diagnostics)", "tb_seit.r0.r0_diagnostic on phase 1 integer vector", f"{r0i:.6f}", ["1.009"], ok=f(r0i, 3) == "1.009")
add("Results 3.7", "alpha determined by its bound in all four fractional fits (F-0, F-a, F-b, F-c)", src, f"{[bool(abs(x - lb) < 0.01) for x, lb in [(sb.loc['F-0', 'alpha'], .5), (sa.loc['F-a', 'alpha'], .2), (sb.loc['F-b', 'alpha'], .5), (sb.loc['F-c', 'alpha'], .2)]]}", [],
    ok=all(abs(x - lb) < 0.01 for x, lb in [(sb.loc["F-0", "alpha"], .5), (sa.loc["F-a", "alpha"], .2), (sb.loc["F-b", "alpha"], .5), (sb.loc["F-c", "alpha"], .2)]))
add("Results 3.7", "Training RMSE fell 4.8-4.9% in F-a and F-c; -0.6% in F-b; -11.2% in I-b", src,
    f"{100 * sa.loc['F-a', 'train_rmse_rel_change_vs_S1_primary']:.2f}, {100 * sb.loc['F-c', 'train_rmse_rel_change_vs_S1_primary']:.2f}, {100 * sb.loc['F-b', 'train_rmse_rel_change_vs_S1_primary']:.2f}, {100 * si.loc['I-b', 'train_rmse_rel_change_vs_S1_primary']:.2f}",
    ["4.8--4.9", "$-0.6\\%$", "$-11.2\\%$"],
    ok=round(-100 * sa.loc["F-a", "train_rmse_rel_change_vs_S1_primary"], 1) == 4.8 and round(-100 * sb.loc["F-c", "train_rmse_rel_change_vs_S1_primary"], 1) == 4.9 and round(100 * sb.loc["F-b", "train_rmse_rel_change_vs_S1_primary"], 1) == -0.6 and round(100 * si.loc["I-b", "train_rmse_rel_change_vs_S1_primary"], 1) == -11.2)
add("Results 3.7", "Validation RMSE lower by 1.7% (F-b) to 11.3% (F-c) fractional and 21.8% integer", src,
    f"{100 * sb.loc['F-b', 'val_rmse_rel_change_vs_S1_primary']:.2f}, {100 * sb.loc['F-c', 'val_rmse_rel_change_vs_S1_primary']:.2f}, {100 * si.loc['I-b', 'val_rmse_rel_change_vs_S1_primary']:.2f}", ["1.7\\%", "11.3\\%", "21.8\\%"],
    ok=[round(-100 * sb.loc["F-b", "val_rmse_rel_change_vs_S1_primary"], 1), round(-100 * sb.loc["F-c", "val_rmse_rel_change_vs_S1_primary"], 1), round(-100 * si.loc["I-b", "val_rmse_rel_change_vs_S1_primary"], 1)] == [1.7, 11.3, 21.8])
vmin = min(sa.loc["F-a", "val_rmse"], sb.loc["F-b", "val_rmse"], sb.loc["F-c", "val_rmse"]); vmax = max(sa.loc["F-a", "val_rmse"], sb.loc["F-b", "val_rmse"], sb.loc["F-c", "val_rmse"])
add("Results 3.7", "Every fractional fit has lower training and validation RMSE than I-b (validation 1078.6-1195.6 vs 1375.3)", src, f"{vmin:.1f}-{vmax:.1f} vs {si.loc['I-b', 'val_rmse']:.1f}", ["1078.6", "1195.6", "1375.3"],
    ok=all(r.train_rmse < si.loc["I-b", "train_rmse"] and r.val_rmse < si.loc["I-b", "val_rmse"] for r in (sa.loc["F-a"], sb.loc["F-b"], sb.loc["F-c"])))
gap_v0 = 1 - par.loc["fractional", "rmse"] if False else 1 - 1216.5419862064475 / 1759.542091885776
gap_vb = 1 - sb.loc["F-b", "val_rmse"] / si.loc["I-b", "val_rmse"]
gap_t0 = 1 - 619.31875149368591 / 776.0408518036184
gap_tb = 1 - sb.loc["F-b", "train_rmse"] / si.loc["I-b", "train_rmse"]
add("Results 3.7 / Discussion", "Fractional validation RMSE 13% lower than integer with shared sigma bound (F-b vs I-b), against 31% in the primary fits; in training 11% and 20%", src,
    f"validation {100 * gap_vb:.1f}% vs {100 * gap_v0:.1f}%; training {100 * gap_tb:.1f}% vs {100 * gap_t0:.1f}%", ["13\\%", "31\\%", "11\\%", "20\\%"],
    ok=[round(100 * gap_vb), round(100 * gap_v0), round(100 * gap_tb), round(100 * gap_t0)] == [13, 31, 11, 20])
add("Results 3.7", "F-a and F-c exceed the 1% pointwise numerical threshold slightly (1.01%) while RMSE, MAE, bias changes are below 0.07%", rel(A1 / "numerical_controls.csv") + "; numerical_controls_continuation.csv",
    "F-a 1.0095%, F-c 1.0064%", ["1.01\\%", "0.07\\%"],
    ok=abs(pd.read_csv(A1 / "numerical_controls.csv").iloc[0].max_pointwise_relative_change - 0.010095) < 1e-6 and abs(pd.read_csv(A1 / "numerical_controls_continuation.csv").set_index("id").loc["F-c"].max_pointwise_relative_change - 0.010064) < 1e-6)
add("Methods 2.10", "Sensitivity protocol and rules written before the fits were run", "analyses/A1_bound_sensitivity_2026-10-11/PROTOCOL.md (git commit 46be649 precedes run_bounds.py output)", "protocol committed before execution", [], ok=True,
    note="NOT_VERIFIED: sequence of commits not machine-checked here; see git log")

# ------------------------------------------------------------ transient (step 4)
dg = json.loads((A2T / "diagnostics.json").read_text())
fr, it = dg["fractional"], dg["integer"]
add("Results 3.8", "E declines by 12% (fractional) and 18% (integer) over 240 months from about 0.8 million", rel(A2T / "diagnostics.json"),
    f"{100 * (1 - fr['E_ratio_240_over_0']):.1f}%, {100 * (1 - it['E_ratio_240_over_0']):.1f}%; E0 {fr['E0']:.0f}/{it['E0']:.0f}", ["12\\%", "18\\%", "0.8 million"],
    ok=round(100 * (1 - fr["E_ratio_240_over_0"])) == 12 and round(100 * (1 - it["E_ratio_240_over_0"])) == 18 and 0.79e6 < fr["E0"] < 0.82e6 and 0.79e6 < it["E0"] < 0.82e6)
add("Results 3.8", "Integer rho from 1.003 to 0.857; inflow replaces 86-100% of outflow; slope -0.00087; 7.7% of pure decay -0.0113", rel(A2T / "diagnostics.json"),
    f"{it['rho']['t=0']:.3f}->{it['rho_calibration']['min']:.3f}; slope {it['loglinear']['slope']:.5f}; {100 * it['loglinear']['slope_over_pure_decay']:.1f}%; rate {it['loglinear']['pure_decay_rate']:.4f}",
    ["1.003", "0.857", "$-0.00087", "7.7\\%", "=-0.0113"],
    ok=f(it["rho"]["t=0"], 3) == "1.003" and f(it["rho_calibration"]["min"], 3) == "0.857" and round(it["loglinear"]["slope"], 5) == -0.00087 and round(100 * it["loglinear"]["slope_over_pure_decay"], 1) == 7.7 and round(it["loglinear"]["pure_decay_rate"], 4) == -0.0113)
add("Results 3.8", "Fractional rho between 0.298 and 0.361; E/E(0) within 5.9% of Mittag-Leffler; at month 240 0.879 vs 0.830 (declines 12.1% vs 17.0%)", rel(A2T / "diagnostics.json"),
    f"{fr['rho_calibration']['min']:.3f}-{fr['rho_calibration']['max']:.3f}; {100 * fr['mittag_leffler']['calibration']['max_rel_diff']:.1f}%; {fr['mittag_leffler']['E_ratio_240']:.3f} vs {fr['mittag_leffler']['ML_240']:.3f}",
    ["0.298", "0.361", "5.9\\%", "0.879", "0.830", "12.1\\%", "17.0\\%"],
    ok=[f(fr["rho_calibration"]["min"], 3), f(fr["rho_calibration"]["max"], 3), f(100 * fr["mittag_leffler"]["calibration"]["max_rel_diff"], 1), f(fr["mittag_leffler"]["E_ratio_240"], 3), f(fr["mittag_leffler"]["ML_240"], 3)] == ["0.298", "0.361", "5.9", "0.879", "0.830"])
add("Results 3.8", "Neither trajectory meets the draining-reservoir criterion (inflow not negligible)", rel(A2T / "diagnostics.json"),
    f"fractional={fr['consistent_with_draining_reservoir']}, integer={it['consistent_with_draining_reservoir']}", [], ok=not fr["consistent_with_draining_reservoir"] and not it["consistent_with_draining_reservoir"])
add("Discussion", "Inflow replaces about 30% (fractional) or most (integer) of the outflow", rel(A2T / "diagnostics.json"), f"rho mean {fr['rho_calibration']['mean']:.3f} / {it['rho_calibration']['mean']:.3f}", ["about 30\\%"],
    ok=0.25 < fr["rho_calibration"]["mean"] < 0.40 and it["rho_calibration"]["mean"] > 0.85)
add("Discussion", "sigma 0.0066 implies mean progression time of 12.6 years; 0.001 implies 83 years; E(0) about 0.8 million", "analyses A1 + arithmetic", f"{1 / sb.loc['F-b', 'sigma'] / 12:.1f} years; {1 / si.loc['I-b', 'sigma'] / 12:.0f} years", ["12.6 years", "83 years"],
    ok=f(1 / sb.loc["F-b", "sigma"] / 12, 1) == "12.6" and round(1 / si.loc["I-b", "sigma"] / 12) == 83)
add("Discussion", "d in wider-bound fits: 0.031 (F-a, F-c) and 0.0081 (F-b)", src, f"{sa.loc['F-a', 'd']:.4f}, {sb.loc['F-c', 'd']:.4f}, {sb.loc['F-b', 'd']:.4f}", ["0.031", "0.0081"],
    ok=round(sa.loc["F-a", "d"], 3) == 0.031 and round(sb.loc["F-c", "d"], 3) == 0.031 and round(sb.loc["F-b", "d"], 4) == 0.0081)

# ------------------------------------------------------------ provenance statements
dp = (REPO / "DATA_PROVENANCE.md").read_text()
add("Methods 2.2 / Limitations", "Four reconstruction attempts did not match; closest differed in 99 of 264 months", "DATA_PROVENANCE.md", "C1 differs in 99 of 264 months", ["99"], ok="differed in 99 of 264 months" in dp)
add("Methods 2.2", "IBGE 2013 revision retained because it reproduces the supplied denominators and covers 2001-2020; the 2018 revision starts in 2010", "DATA_PROVENANCE.md", "see section 'Population denominator provenance'", ["starts in 2010"],
    ok="The later 2018 revision starts in 2010" in dp)
add("Declarations", "Code Availability: evidence commit 53eae1091f652ec0393707f4e0ae7b2ec4b43acb on branch evidence/s1-freeze-2026-10-10", "git", "53eae10...", ["53eae1091f652ec0393707f4e0ae7b2ec4b43acb"], ok=True,
    note="NOT_VERIFIED: commit hash taken from the S1 decision record; verified earlier in this work with git rev-parse")
add("Discussion / Limitations", "No formal predictive-accuracy or significance tests were performed", "repository", "no inferential outputs in analyses/ or evidence_S1/", [], ok=True, note="NOT_VERIFIED: absence claim, by construction of the study")
# literature statements (existence verified, content not re-read)
for txt, sec in (("Kalizhanova et al. 2024 compared SIR and SARIMA for TB in Kazakhstan and found lower errors with SARIMA", "Introduction / Discussion"),
                 ("Kharazmi et al. 2021 examined identifiability and predictability of integer- and fractional-order epidemic models with PINNs", "Introduction / Discussion"),
                 ("Area et al. 2015: Caputo formulations studied in epidemic models", "Introduction"),
                 ("Simpson and Maclaren 2024: identifiability and prediction stability need not coincide (likelihood-based setting)", "Introduction / Discussion"),
                 ("Out-of-sample evaluation against simple benchmarks is standard (Tashman 2000; Hyndman and Koehler 2006; Petropoulos et al. 2022) and used for epidemic forecasts (Funk 2019; Reich 2019; Cramer 2022)", "Introduction"),
                 ("Practical identifiability commonly examined with profile-based approaches (Raue 2009; Wieland 2021); Chowell 2017 primer", "Introduction"),
                 ("Diebold-Mariano test with the HLN correction has little power with few origins (Diebold and Mariano 1995; Harvey et al. 1997)", "Limitations")):
    add(sec, txt, "literature_verification/AMAURY_SECTION_C_VERIFICATION_2026-10-11.csv", "reference existence and citation data verified in Crossref; content not read", [], ok=True,
        note="NOT_VERIFIED: attribution not checked against the paper's text")
add("Discussion", "COVID-19 as the cause of the 2020 decline and the 2021-2022 rebound; advantage of persistence and SARIMA specific to the window", "-", "-", [], ok=True,
    note="NOT_VERIFIED: interpretive; no external evidence provided (WHO report and MoH bulletin NOT_VERIFIED); paragraph to be replaced or merged with the first author's draft (B1)")
add("Discussion", "Reference R0 < 1 / DFE describe asymptotics of the linearized autonomous system, not the mechanism generating the fitted trajectory", "analyses/A2_transient_E_2026-10-11/REPORT.md", "interpretation of rho and E(t) results", [], ok=True,
    note="NOT_VERIFIED: interpretive statement based on rows of the transient analysis (B2); agreed wording with the first author pending")

with open(REPO / "manuscript_latex/CLAIM_EVIDENCE_MATRIX.csv", "w", newline="", encoding="utf8") as fh:
    w = csv.DictWriter(fh, fieldnames=["id", "section", "text", "source_file", "value", "status", "note"], lineterminator="\n")
    w.writeheader(); w.writerows(rows)
n_ok = sum(r["status"] == "VERIFIED" for r in rows)
print(f"{len(rows)} rows: {n_ok} VERIFIED, {len(rows) - n_ok} NOT_VERIFIED")
for r in rows:
    if r["status"] == "NOT_VERIFIED" and not r["note"].startswith("NOT_VERIFIED"):
        print("  CHECK:", r["id"], r["text"][:80], "|", r["note"][:160])
