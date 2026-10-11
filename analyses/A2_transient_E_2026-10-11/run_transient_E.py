"""Step 4 (Plan A continuation): transient of E(t) with the frozen S1 parameter vectors.

Protocol: PROTOCOL.md in this folder (committed before this script was run). No fitting.
"""

import csv
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np
import pandas as pd
from scipy.special import gammaln

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
from tb_seit import constants, data, model, population  # noqa: E402

OUT = Path(__file__).resolve().parent
S1 = REPO / "evidence_S1" / "TB_SEIT_EVIDENCE_FREEZE_2026-10-10"
PARAMS = S1 / "phase1/tb_global_refit_phase1/results_global_primary/global_refit_parameters.csv"
PRED_DIR = S1 / "phase1/tb_global_refit_phase1/results_global_primary"
H = 1.0
N_MONTHS = 264
N_CAL = 240
FLOW_TOL = 1e-6
ML_Z_MAX = 5.0
RHO_NEGLIGIBLE = 0.10
REL_TOL = 0.10


def ordinary_monthly_flow(e: np.ndarray, sigma: float) -> np.ndarray:
    """Same quadrature as run_global_refit.py: composite trapezoid of sigma*E per month (h = 1)."""
    return (0.5 * sigma * H * (e[:-1] + e[1:])).reshape(N_MONTHS, int(round(1 / H))).sum(axis=1)


def mittag_leffler(alpha: float, z: np.ndarray) -> np.ndarray:
    """Power series sum_k z^k / Gamma(alpha k + 1); valid here because |z| <= ML_Z_MAX."""
    k = np.arange(0, 400)
    coef = np.exp(-gammaln(alpha * k + 1.0))
    return (z[:, None] ** k[None, :] * coef[None, :]).sum(axis=1)


def main() -> int:
    ds = data.load_canonical_dataset()
    series, _ = population.build_population_exogenous_series(ds)
    N_of_t = population.make_N_of_t(series)
    mc = constants.compute_model_constants(ds.calibration["population"])
    N0 = float(ds.calibration["population"].iloc[0])
    flow0 = float(ds.calibration["cases"].iloc[0])
    pars = pd.read_csv(PARAMS).set_index("model")

    diag, stop = {"flow0": flow0, "N0": N0, "mu": mc.mu, "lambda": mc.lambda_}, False
    t = np.arange(N_MONTHS + 1) * H
    for label in ("fractional", "integer"):
        r = pars.loc[label]
        p = model.SeitParameters(beta=r.beta, sigma=r.sigma, gamma=r.gamma, d=r.d, alpha=r.alpha)
        sim = model.simulate(p, mc.lambda_, mc.mu, N_of_t, N0, flow0, N_MONTHS, H)
        if sim.solver.status != "ok" or not np.all(np.isfinite(sim.solver.y)):
            print(f"STOP: {label} solver status {sim.solver.status}", file=sys.stderr)
            return 1
        S, E, I, T, _C = sim.solver.y.T
        N = np.array([N_of_t(x) for x in t])
        flow = ordinary_monthly_flow(E, p.sigma)
        inflow = p.beta * S * I / N
        outflow = (p.sigma + mc.mu) * E
        rho = inflow / outflow

        # --- control: reproduce archived S1 phase-1 predictions
        arch = pd.read_csv(PRED_DIR / f"{label}_predictions.csv")["predicted"].to_numpy()
        assert len(arch) == N_MONTHS
        ctrl = float(np.max(np.abs(flow - arch)))
        d = {"params": {k: float(r[k]) for k in ("beta", "sigma", "gamma", "d", "alpha")},
             "control_max_abs_flow_diff": ctrl, "control_tol": FLOW_TOL,
             "control_pass": ctrl <= FLOW_TOL}
        if not d["control_pass"]:
            diag[label] = d
            (OUT / "diagnostics.json").write_text(json.dumps(diag, indent=2) + "\n")
            print(f"STOP: {label} reproduction control failed ({ctrl})", file=sys.stderr)
            return 1

        pd.DataFrame({"t_month": t, "S": S, "E": E, "I": I, "T": T, "N": N,
                      "inflow_beta_S_I_over_N": inflow, "outflow_sigma_plus_mu_E": outflow,
                      "rho_inflow_over_outflow": rho,
                      "ordinary_monthly_flow": np.append(flow, np.nan)}
                     ).to_csv(OUT / f"trajectories_{label}.csv", index=False, float_format="%.12g")

        lam = p.sigma + mc.mu
        cal = slice(0, N_CAL + 1)
        # --- rho summary (both models)
        d["rho"] = {f"t={k}": float(rho[k]) for k in (0, 60, 120, 180, 240, 264)}
        d["rho_calibration"] = {"min": float(rho[cal].min()), "max": float(rho[cal].max()),
                                "mean": float(rho[cal].mean())}
        d["inflow_negligible"] = bool(rho[cal].max() <= RHO_NEGLIGIBLE)
        d["E0"] = float(E[0]); d["E_240"] = float(E[240]); d["E_264"] = float(E[264])
        d["E_ratio_240_over_0"] = float(E[240] / E[0])
        d["S_over_N_0"] = float(S[0] / N[0])

        if label == "integer":
            logE = np.log(E[cal])
            slope, icpt = np.polyfit(t[cal], logE, 1)
            pred = icpt + slope * t[cal]
            r2 = 1 - np.sum((logE - pred) ** 2) / np.sum((logE - logE.mean()) ** 2)
            ratio = slope / (-lam)
            d["loglinear"] = {"slope": float(slope), "pure_decay_rate": float(-lam),
                              "slope_over_pure_decay": float(ratio), "R2": float(r2)}
            d["slope_within_10pct"] = bool(abs(ratio - 1) <= REL_TOL)
            d["consistent_with_draining_reservoir"] = bool(d["inflow_negligible"] and d["slope_within_10pct"])
        else:
            z = -lam * t ** p.alpha
            if np.max(np.abs(z)) > ML_Z_MAX:
                print("STOP: |z| exceeds the Mittag-Leffler series range", file=sys.stderr)
                return 1
            ml = mittag_leffler(p.alpha, z)
            rel = np.abs(E / E[0] - ml) / ml
            d["mittag_leffler"] = {"max_abs_z": float(np.max(np.abs(z))),
                                   "ML_240": float(ml[240]), "E_ratio_240": float(E[240] / E[0]),
                                   "ML_264": float(ml[264]), "E_ratio_264": float(E[264] / E[0]),
                                   "calibration": {"max_rel_diff": float(rel[cal].max()),
                                                   "mean_rel_diff": float(rel[cal].mean())},
                                   "full_264": {"max_rel_diff": float(rel.max()),
                                                "mean_rel_diff": float(rel.mean())}}
            d["ml_within_10pct"] = bool(rel[cal].max() <= REL_TOL)
            d["consistent_with_draining_reservoir"] = bool(d["inflow_negligible"] and d["ml_within_10pct"])
            pd.DataFrame({"t_month": t, "E_over_E0": E / E[0], "MittagLeffler": ml}
                         ).to_csv(OUT / "fractional_E_vs_mittag_leffler.csv", index=False, float_format="%.12g")
        diag[label] = d

    (OUT / "diagnostics.json").write_text(json.dumps(diag, indent=2) + "\n")
    print(json.dumps(diag, indent=2))

    # figure
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    tr = {k: pd.read_csv(OUT / f"trajectories_{k}.csv") for k in ("fractional", "integer")}
    ml = pd.read_csv(OUT / "fractional_E_vs_mittag_leffler.csv")
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
    for k, c in (("fractional", "tab:blue"), ("integer", "tab:orange")):
        ax[0].plot(tr[k].t_month, tr[k].E / tr[k].E.iloc[0], c=c, label=f"{k} E(t)/E(0)")
        ax[2].plot(tr[k].t_month, tr[k].rho_inflow_over_outflow, c=c, label=k)
    lam_i = pars.loc["integer"].sigma + mc.mu
    ax[0].plot(tr["integer"].t_month, np.exp(-lam_i * tr["integer"].t_month), "k:", label="integer pure decay")
    ax[0].plot(ml.t_month, ml.MittagLeffler, "k--", label="fractional Mittag-Leffler")
    ax[1].plot(tr["integer"].t_month, tr["integer"].E / 1e3, c="tab:orange", label="integer E (x1e3)")
    ax[1].plot(tr["fractional"].t_month, tr["fractional"].E / 1e3, c="tab:blue", label="fractional E (x1e3)")
    ax[2].axhline(RHO_NEGLIGIBLE, c="gray", ls=":"); ax[2].axhline(1.0, c="gray", ls="-", lw=0.5)
    for a, tt in zip(ax, ("E(t)/E(0) vs pure decay", "E(t) (thousands)", "inflow / outflow")):
        a.axvline(N_CAL, c="gray", lw=0.5); a.set_title(tt, fontsize=10); a.set_xlabel("months since 2001-01")
        a.legend(fontsize=7)
    fig.tight_layout(); fig.savefig(OUT / "transient_E.png", dpi=150)
    return 0


if __name__ == "__main__":
    sys.exit(main())
