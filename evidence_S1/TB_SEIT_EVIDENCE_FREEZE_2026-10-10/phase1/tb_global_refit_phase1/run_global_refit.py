#!/usr/bin/env python3
"""Controlled global refit, ordinary monthly observation, both SEIT variants.

Runs only frozen primary seed; does not write into canonical repository outputs.
Place this file under an untracked audits directory or pass --repo /path/to/repo.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

AUDIT_FIXED_OPERATOR_EXPECTED = {
    "fractional": {
        "original_calibration_rmse": 605.048881,
        "original_validation_rmse": 1117.960028,
        "ordinary_calibration_rmse": 1620.116037,
        "ordinary_validation_rmse": 1178.733666,
    },
    "integer": {
        "original_calibration_rmse": 776.058253,
        "original_validation_rmse": 1759.538401,
        "ordinary_calibration_rmse": 776.040852,
        "ordinary_validation_rmse": 1759.542092,
    },
}


def find_repo(path: Path | None) -> Path:
    if path is not None:
        root = path.resolve()
        if not (root / "src/tb_seit/model.py").is_file():
            raise RuntimeError(f"Not a TB-SEIT repository: {root}")
        return root
    for candidate in (Path.cwd(), *Path(__file__).resolve().parents):
        if (candidate / "src/tb_seit/model.py").is_file():
            return candidate
    raise RuntimeError("Repository not found; use --repo /absolute/path/to/worktree")


def ordinary_monthly_flow(solver, sigma: float, n_months: int, h: float) -> np.ndarray:
    """Composite trapezoids on corrected E states; no fractional C increments."""
    if solver.status != "ok":
        return np.full(n_months, np.nan, dtype=float)
    steps = int(round(1.0 / h))
    if steps < 1 or not np.isclose(steps * h, 1.0, atol=1e-12, rtol=0):
        raise ValueError("h must divide one month exactly")
    e = np.asarray(solver.y[:, 1], dtype=float)  # S,E,I,T,C; E index 1
    if len(e) != n_months * steps + 1:
        raise ValueError("solver state length is inconsistent with n_months and h")
    intervals = (0.5 * sigma * h * (e[:-1] + e[1:]))
    return intervals.reshape(n_months, steps).sum(axis=1)


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tracked_hashes(root: Path) -> dict[str, str]:
    out = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"])
    paths = [p.decode("utf8") for p in out.split(b"\x00") if p]
    return {p: file_hash(root / p) for p in paths if (root / p).is_file()}


def read_params(path, model):
    with path.open(newline="") as stream:
        values = {r["parameter"]: float(r["value"]) for r in csv.DictReader(stream)}
    return model.SeitParameters(**values)


def metric_row(label, split, obs, pred, metrics):
    return {
        "model": label, "split": split, "n": len(obs),
        "rmse": metrics.rmse(obs, pred), "mae": metrics.mae(obs, pred),
        "bias": metrics.bias(obs, pred),
    }


def write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run(args):
    root = find_repo(args.repo)
    output = (args.output or (Path(__file__).resolve().parent / "results_global_primary")).resolve()
    protected = [root / p for p in ("results_canonical", "outputs", "src", "scripts", "data", "submission_bmb")]
    if any(output == p or p in output.parents for p in protected):
        raise RuntimeError("Output path overlaps a protected canonical directory")
    sys.path.insert(0, str(root / "src"))
    import scipy
    from scipy.optimize import differential_evolution
    from tb_seit import calibration, constants, data, metrics, model, population, seeds

    if seeds.PRIMARY_SEED != 20260815:
        raise RuntimeError("Unexpected change in the canonical primary seed")
    if calibration.MAXITER != 1000 or calibration.POPSIZE != 15:
        raise RuntimeError("Unexpected change in frozen DE budget")

    ds = data.load_canonical_dataset()
    n_train = len(ds.calibration)
    n_val = len(ds.validation)
    if n_train != 240 or n_val != 24:
        raise RuntimeError("Unexpected 240/24 split")
    observed_train = ds.calibration["cases"].to_numpy(dtype=float)
    observed_val = ds.validation["cases"].to_numpy(dtype=float)
    n_months = n_train + n_val
    series, trend = population.build_population_exogenous_series(ds)
    N_of_t = population.make_N_of_t(series)
    mc = constants.compute_model_constants(ds.calibration["population"])
    N0 = float(ds.calibration["population"].iloc[0])
    flow0 = float(observed_train[0])
    h = 1.0  # canonical solver grid
    tracked_before = tracked_hashes(root)

    def simulate_with_operator(p, months):
        sim = model.simulate(p, mc.lambda_, mc.mu, N_of_t, N0, flow0, months, h)
        pred_o = ordinary_monthly_flow(sim.solver, p.sigma, months, h)
        return sim, pred_o

    # Mandatory preflight: the fixed-theta ablation must reproduce independently.
    preflight = []
    for label in ("fractional", "integer"):
        p = read_params(root / f"outputs/calibration/{label}_parameters.csv", model)
        sim, observed_ordinary = simulate_with_operator(p, n_months)
        if sim.solver.status != "ok" or not np.all(np.isfinite(observed_ordinary)):
            raise RuntimeError(f"Preflight {label}: invalid solver result")
        old = sim.monthly_flow
        actual = {
            "original_calibration_rmse": metrics.rmse(observed_train, old[:n_train]),
            "original_validation_rmse": metrics.rmse(observed_val, old[n_train:]),
            "ordinary_calibration_rmse": metrics.rmse(observed_train, observed_ordinary[:n_train]),
            "ordinary_validation_rmse": metrics.rmse(observed_val, observed_ordinary[n_train:]),
        }
        for k, expected in AUDIT_FIXED_OPERATOR_EXPECTED[label].items():
            if abs(actual[k] - expected) > 0.001:
                raise RuntimeError(
                    f"Preflight mismatch {label}/{k}: {actual[k]:.9f} vs audit {expected:.9f}"
                )
        preflight.append({"model": label, "pass": True, **actual})

    if args.preflight_only:
        print(json.dumps({"stage": "preflight-only", "preflight": preflight}, indent=2))
        return

    if output.exists() and any(output.iterdir()):
        raise RuntimeError(f"Refusing to overwrite nonempty output directory: {output}")
    output.mkdir(parents=True, exist_ok=True)

    bounds_frac = [(0.01, 1.0), (0.01, 0.5), (0.05, 0.30), (0.0001, 0.05), (0.5, 1.0)]
    bounds_int = bounds_frac[:4]
    all_fit = []
    all_metrics = []
    for label, bounds, integer in [
        ("fractional", bounds_frac, False), ("integer", bounds_int, True)
    ]:
        def objective(x):
            try:
                p = model.SeitParameters(*map(float, x), **({"alpha": 1.0} if integer else {}))
                sim, flow_o = simulate_with_operator(p, n_train)
                if sim.solver.status != "ok" or not np.all(np.isfinite(flow_o)):
                    return calibration.LARGE_PENALTY
                return metrics.rmse(observed_train, flow_o)
            except (FloatingPointError, ValueError, OverflowError, RuntimeError):
                return calibration.LARGE_PENALTY

        result = differential_evolution(
            objective, bounds=bounds,
            strategy=calibration.STRATEGY,
            popsize=calibration.POPSIZE,
            mutation=calibration.MUTATION,
            recombination=calibration.RECOMBINATION,
            tol=calibration.TOL,
            maxiter=calibration.MAXITER,
            seed=seeds.PRIMARY_SEED,
            polish=False,
        )
        if not result.success:
            raise RuntimeError(f"STOP: {label} optimization failed: {result.message}")
        if not np.isfinite(result.fun) or result.fun >= calibration.LARGE_PENALTY:
            raise RuntimeError(f"STOP: {label} optimization returned an invalid objective")
        p = model.SeitParameters(*map(float, result.x), **({"alpha": 1.0} if integer else {}))
        sim, pred = simulate_with_operator(p, n_months)
        if sim.solver.status != "ok" or not np.all(np.isfinite(pred)):
            raise RuntimeError(f"{label}: global refit produced invalid 264-month validation")

        # Full continuous simulation and train-only fit: do not tune against validation.
        train_metrics = metric_row(label, "calibration", observed_train, pred[:n_train], metrics)
        val_metrics = metric_row(label, "validation_open_loop", observed_val, pred[n_train:], metrics)
        all_metrics.extend([train_metrics, val_metrics])
        fit_row = {
            "model": label, "operator": "ordinary_composite_trapezoid", "seed": seeds.PRIMARY_SEED,
            "beta": p.beta, "sigma": p.sigma, "gamma": p.gamma, "d": p.d, "alpha": p.alpha,
            "objective_train_rmse": float(result.fun), "success": bool(result.success),
            "iterations": int(result.nit), "function_evaluations": int(result.nfev),
        }
        all_fit.append(fit_row)
        pred_rows = []
        for split, frame, yobs, ypred in (
            ("calibration", ds.calibration, observed_train, pred[:n_train]),
            ("validation_open_loop", ds.validation, observed_val, pred[n_train:]),
        ):
            for date, obs, prediction in zip(frame["date"], yobs, ypred):
                pred_rows.append({
                    "date": str(date.date()), "split": split, "observed": float(obs),
                    "predicted": float(prediction), "residual": float(prediction - obs)
                })
        write_csv(output / f"{label}_predictions.csv",
                  ["date", "split", "observed", "predicted", "residual"], pred_rows)
        print(f"{label}: train RMSE={train_metrics['rmse']:.6f}, "
              f"open-loop validation RMSE={val_metrics['rmse']:.6f}, "
              f"optimizer_success={result.success}", flush=True)

    write_csv(output / "global_refit_parameters.csv", list(all_fit[0]), all_fit)
    write_csv(output / "global_refit_metrics.csv", list(all_metrics[0]), all_metrics)
    difference = {}
    for split in ("calibration", "validation_open_loop"):
        a = next(r for r in all_metrics if r["model"] == "fractional" and r["split"] == split)
        b = next(r for r in all_metrics if r["model"] == "integer" and r["split"] == split)
        difference[split] = {
            "rmse_fractional_minus_integer": a["rmse"] - b["rmse"],
            "mae_fractional_minus_integer": a["mae"] - b["mae"],
            "bias_fractional_minus_integer": a["bias"] - b["bias"],
        }
    hashes_after = tracked_hashes(root)
    if tracked_before != hashes_after:
        raise RuntimeError("STOP: tracked repository files changed during the experiment")
    audit = {
        "analysis": "GLOBAL_REFIT_ORDINARY_OBSERVATION_PHASE_1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "repository_path": str(root),
        "repository_head": subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip(),
        "raw_data_sha256": file_hash(root / "data/raw/tb_mes.xlsx"),
        "tracked_files_unchanged": True,
        "tracked_file_count": len(tracked_before),
        "primary_seed": seeds.PRIMARY_SEED,
        "solver_h_months": h,
        "train_months": n_train,
        "validation_months": n_val,
        "observation_operator": "sum of trapezoidal sigma*E over corrected states on each monthly interval",
        "population_trend": {"intercept": trend.intercept, "slope": trend.slope},
        "constants": {"mu": mc.mu, "lambda": mc.lambda_, "N0": N0, "flow0": flow0},
        "de_contract": {
            "strategy": calibration.STRATEGY, "popsize": calibration.POPSIZE,
            "mutation": calibration.MUTATION, "recombination": calibration.RECOMBINATION,
            "tol": calibration.TOL, "maxiter": calibration.MAXITER, "polish": False,
        },
        "python_version": platform.python_version(), "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "preflight_fixed_theta": preflight,
        "parameters": all_fit,
        "metrics": all_metrics,
        "contrasts": difference,
        "rolling_origin_evaluated": False,
        "decision": "REQUIRES_AUTHOR_SCIENTIFIC_REVIEW_BEFORE_ANY_ROLLING_ORIGIN",
    }
    (output / "phase1_report.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf8")
    print(f"Saved phase 1 in {output}")
    print("STOP: no rolling-origin, no manuscript edits, no commit or push")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=None, help="path to the exact audited worktree")
    parser.add_argument("--output", type=Path, default=None, help="fresh, noncanonical output directory")
    parser.add_argument("--preflight-only", action="store_true", help="verify frozen-theta audit before refitting")
    run(parser.parse_args())


if __name__ == "__main__":
    main()
