"""Step 5 (Plan A continuation): sensitivity to the lower bounds of alpha and sigma.

Protocol: PROTOCOL.md in this folder (committed before this script was run).
Objective, solver, observation operator and DE settings replicate S1 phase 1
(evidence_S1/.../phase1/tb_global_refit_phase1/run_global_refit.py). Evidence is read-only.
"""

import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
from tb_seit import calibration, constants, data, model, population, r0, seeds  # noqa: E402

OUT = Path(__file__).resolve().parent
S1 = REPO / "evidence_S1" / "TB_SEIT_EVIDENCE_FREEZE_2026-10-10"
P1 = S1 / "phase1/tb_global_refit_phase1/results_global_primary"
NAMES = ["beta", "sigma", "gamma", "d", "alpha"]
BASE = {"beta": (0.01, 1.0), "sigma": (0.01, 0.5), "gamma": (0.05, 0.30), "d": (0.0001, 0.05), "alpha": (0.5, 1.0)}
FITS = {  # id: (integer?, overrides)
    "F-0": (False, {}),
    "F-a": (False, {"alpha": (0.20, 1.0)}),
    "F-b": (False, {"sigma": (0.001, 0.5)}),
    "F-c": (False, {"alpha": (0.20, 1.0), "sigma": (0.001, 0.5)}),
    "I-b": (True, {"sigma": (0.001, 0.5)}),
}
H = 1.0
# Optional CLI: fit ids to run (continuation after the mandatory stop, see PROTOCOL_ADDENDUM).
IDS = sys.argv[1:] or list(FITS)
SUFFIX = "_continuation" if sys.argv[1:] else ""


def ordinary_monthly_flow(e, sigma, n_months, h):
    steps = int(round(1.0 / h))
    return (0.5 * sigma * h * (e[:-1] + e[1:])).reshape(n_months, steps).sum(axis=1)


class Ctx:
    def __init__(self):
        ds = data.load_canonical_dataset()
        series, _ = population.build_population_exogenous_series(ds)
        self.N_of_t = population.make_N_of_t(series)
        self.mc = constants.compute_model_constants(ds.calibration["population"])
        self.N0 = float(ds.calibration["population"].iloc[0])
        self.flow0 = float(ds.calibration["cases"].iloc[0])
        self.obs_train = ds.calibration["cases"].to_numpy(float)
        self.obs_val = ds.validation["cases"].to_numpy(float)
        self.dates = pd.concat([ds.calibration["date"], ds.validation["date"]]).reset_index(drop=True)

    def predict(self, values, months, h=H):
        p = model.SeitParameters(**values)
        sim = model.simulate(p, self.mc.lambda_, self.mc.mu, self.N_of_t, self.N0, self.flow0, months, h)
        if sim.solver.status != "ok":
            return None
        pred = ordinary_monthly_flow(np.asarray(sim.solver.y[:, 1], float), p.sigma, months, h)
        return pred if np.all(np.isfinite(pred)) else None


def rmse(o, p): return float(np.sqrt(np.mean((p - o) ** 2)))
def mae(o, p): return float(np.mean(np.abs(p - o)))
def bias(o, p): return float(np.mean(p - o))


def numerical_check(values, ctx, months=240):
    pr = {h: ctx.predict(values, months, h) for h in (1.0, 0.5, 0.25)}
    if any(v is None for v in pr.values()):
        return dict(status="FAIL", reason="solver failure")
    o = ctx.obs_train
    d1 = float(np.max(np.abs(pr[1.0] - pr[0.5])))
    d2 = float(np.max(np.abs(pr[0.5] - pr[0.25])))
    rel = float(np.max(np.abs(pr[1.0] - pr[0.25]) / np.maximum(np.abs(pr[0.25]), 1.0)))
    rr = abs(rmse(o, pr[1.0]) - rmse(o, pr[0.25])) / max(abs(rmse(o, pr[0.25])), 1.0)
    mr = abs(mae(o, pr[1.0]) - mae(o, pr[0.25])) / max(abs(mae(o, pr[0.25])), 1.0)
    br = abs(bias(o, pr[1.0]) - bias(o, pr[0.25])) / float(np.mean(o))
    ok = rel <= .01 and rr <= .01 and mr <= .01 and br <= .01 and d2 <= d1 + 1e-9
    return dict(max_pointwise_relative_change=rel, rmse_relative_change=rr, mae_relative_change=mr,
                bias_change_relative_observed_mean=br, half_difference=d1, quarter_difference=d2,
                status="PASS" if ok else "FAIL")


def near_bound(name, value, lo, hi, is_primary_rule):
    """Boundary rules fixed in PROTOCOL.md."""
    if name == "alpha":
        return abs(value - lo) < 0.01
    if name == "sigma":
        return value < 1.1 * lo
    return (value - lo) < 0.10 * (hi - lo) or (hi - value) < 0.10 * (hi - lo)


def stop(msg, rows, code=2):
    pd.DataFrame(rows).to_csv(OUT / f"fit_parameters{SUFFIX}.csv", index=False, float_format="%.12g")
    (OUT / f"STOP{SUFFIX}.txt").write_text(msg + "\n")
    print("STOP:", msg, file=sys.stderr)
    return code


def main():
    assert seeds.PRIMARY_SEED == 20260815 and calibration.MAXITER == 1000 and calibration.POPSIZE == 15
    ctx = Ctx()
    n_tr = len(ctx.obs_train)
    n_all = n_tr + len(ctx.obs_val)
    s1 = pd.read_csv(P1 / "global_refit_parameters.csv", float_precision="round_trip").set_index("model")
    s1m = pd.read_csv(P1 / "global_refit_metrics.csv", float_precision="round_trip")
    prim = {m: {"train": float(s1m[(s1m.model == m) & (s1m.split == "calibration")].rmse.iloc[0]),
                "val": float(s1m[(s1m.model == m) & (s1m.split == "validation_open_loop")].rmse.iloc[0])}
            for m in ("fractional", "integer")}

    # control 1: objective at the S1 primary vectors
    c1 = {}
    for m in ("fractional", "integer"):
        v = {k: float(s1.loc[m, k]) for k in NAMES}
        c1[m] = abs(rmse(ctx.obs_train, ctx.predict(v, n_tr)) - float(s1.loc[m, "objective_train_rmse"]))
    if max(c1.values()) > 1e-8:
        return stop(f"script fidelity control failed: {c1}", [])
    print("control 1 (objective at S1 primary) passed:", c1, flush=True)

    rows, ncs, preds = [], [], {}
    for fid in IDS:
        integer, over = FITS[fid]
        bounds = {**BASE, **over}
        free = NAMES[:4] if integer else NAMES

        def cost(x, free=free, integer=integer):
            try:
                vals = dict(zip(free, map(float, x)))
                if integer:
                    vals["alpha"] = 1.0
                pr = ctx.predict(vals, n_tr)
                return calibration.LARGE_PENALTY if pr is None else rmse(ctx.obs_train, pr)
            except (FloatingPointError, ValueError, OverflowError, RuntimeError):
                return calibration.LARGE_PENALTY

        t0 = time.monotonic()
        res = differential_evolution(cost, bounds=[bounds[k] for k in free], strategy=calibration.STRATEGY,
                                     popsize=calibration.POPSIZE, mutation=calibration.MUTATION,
                                     recombination=calibration.RECOMBINATION, tol=calibration.TOL,
                                     maxiter=calibration.MAXITER, seed=seeds.PRIMARY_SEED, polish=False)
        vals = dict(zip(free, map(float, res.x)))
        if integer:
            vals["alpha"] = 1.0
        ok_fit = bool(res.success) and np.isfinite(res.fun) and res.fun < calibration.LARGE_PENALTY
        pred_all = ctx.predict(vals, n_all)
        row = {"id": fid, "model": "integer" if integer else "fractional", **vals,
               **{f"lb_{k}": bounds[k][0] for k in ("alpha", "sigma")},
               "objective_train_rmse": float(res.fun), "success": bool(res.success), "message": str(res.message),
               "nit": int(res.nit), "nfev": int(res.nfev), "seconds": time.monotonic() - t0}
        print(f"{fid}: obj={res.fun:.6f} alpha={vals['alpha']:.5f} sigma={vals['sigma']:.6f} success={res.success}", flush=True)
        if not ok_fit or pred_all is None:
            rows.append(row)
            return stop(f"{fid}: optimizer did not succeed or invalid prediction ({res.message})", rows)
        tr, va = pred_all[:n_tr], pred_all[n_tr:]
        row.update(train_rmse=rmse(ctx.obs_train, tr), train_mae=mae(ctx.obs_train, tr), train_bias=bias(ctx.obs_train, tr),
                   val_rmse=rmse(ctx.obs_val, va), val_mae=mae(ctx.obs_val, va), val_bias=bias(ctx.obs_val, va),
                   R0_reference=r0.r0_diagnostic(vals["beta"], vals["sigma"], vals["gamma"], vals["d"], ctx.mc.mu))
        for k in ("alpha", "sigma"):
            row[f"{k}_determined_by_boundary"] = bool(near_bound(k, vals[k], bounds[k][0], bounds[k][1], True))
        row["other_params_near_a_bound"] = ";".join(
            k for k in ("beta", "gamma", "d") if near_bound(k, vals[k], *bounds[k], True))
        base = prim[row["model"]]
        row["train_rmse_rel_change_vs_S1_primary"] = (row["train_rmse"] - base["train"]) / base["train"]
        row["val_rmse_rel_change_vs_S1_primary"] = (row["val_rmse"] - base["val"]) / base["val"]
        rows.append(row)
        pd.DataFrame({"date": ctx.dates.astype(str), "split": ["calibration"] * n_tr + ["validation_open_loop"] * (n_all - n_tr),
                      "observed": np.concatenate([ctx.obs_train, ctx.obs_val]), "predicted": pred_all}
                     ).to_csv(OUT / f"predictions_{fid}{SUFFIX}.csv", index=False, float_format="%.12g")
        preds[fid] = row
        pd.DataFrame(rows).to_csv(OUT / f"fit_parameters{SUFFIX}.csv", index=False, float_format="%.12g")

        if fid == "F-0":  # control 2: script reproduces the S1 fractional primary
            dif = max(abs(vals[k] - float(s1.loc["fractional", k])) / abs(float(s1.loc["fractional", k])) for k in NAMES)
            if abs(res.fun - prim["fractional"]["train"]) > 1e-6 or dif > 1e-6:
                return stop(f"F-0 does not reproduce S1 primary (obj diff {res.fun - prim['fractional']['train']}, max rel param diff {dif})", rows)
            print("control 2 (F-0 reproduces S1 primary) passed", flush=True)
            continue

        nc = {"id": fid, **numerical_check(vals, ctx)}
        ncs.append(nc)
        pd.DataFrame(ncs).to_csv(OUT / f"numerical_controls{SUFFIX}.csv", index=False, float_format="%.12g")
        if nc["status"] != "PASS":
            return stop(f"{fid}: numerical resolution control failed: {nc}", rows)
        if row["train_rmse_rel_change_vs_S1_primary"] < -0.01:
            return stop(f"{fid}: training RMSE improves {100 * row['train_rmse_rel_change_vs_S1_primary']:.3f}% (> 1%) over the S1 primary", rows)

    # F-a was run (and stopped) in the original run: take its recorded values
    if "F-a" not in preds:
        fa = pd.read_csv(OUT / "fit_parameters.csv", float_precision="round_trip").set_index("id").loc["F-a"].to_dict()
        fa["id"] = "F-a"
        preds["F-a"] = fa
    # ranking in validation
    ib = preds["I-b"]["val_rmse"]
    inverted = [f for f in ("F-a", "F-b", "F-c")
                if preds[f]["val_rmse"] >= ib or preds[f]["val_rmse"] >= prim["integer"]["val"]]
    comp = []
    for fid, r in preds.items():
        m = r["model"]
        comp.append({"id": fid, "model": m, "alpha": r["alpha"], "sigma": r["sigma"],
                     "train_rmse": r["train_rmse"], "train_rmse_S1_primary": prim[m]["train"],
                     "train_rel_change_pct": 100 * r["train_rmse_rel_change_vs_S1_primary"],
                     "val_rmse": r["val_rmse"], "val_rmse_S1_primary": prim[m]["val"],
                     "val_rel_change_pct": 100 * r["val_rmse_rel_change_vs_S1_primary"],
                     "R0_reference": r["R0_reference"],
                     "alpha_boundary": r["alpha_determined_by_boundary"], "sigma_boundary": r["sigma_determined_by_boundary"],
                     "note": "F-a: recorded values from the stopped run; failed numerical control and 1% stop" if fid == "F-a" else ""})
    pd.DataFrame(comp).to_csv(OUT / f"comparison_with_S1_primary{SUFFIX}.csv", index=False, float_format="%.12g")
    if inverted:
        return stop(f"validation ranking fractional vs integer inverted for {inverted}", list(preds.values()))
    print(json.dumps({"status": "completed_no_stop", "validation_ranking_inverted": inverted}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
