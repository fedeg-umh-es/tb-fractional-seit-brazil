"""Phase 4 of the identifiability audit: local profile-objective analysis for beta, gamma, d
(required) and alpha (negative-control/comparison, since alpha was stable across multiseed).

GRID POLICY (documented here BEFORE execution, per task instruction -- no repository-wide grid
policy pre-existed to reuse):

For each profiled parameter p with frozen primary bound [lo, hi] (unchanged from
docs/MODEL_CONTRACT.md / this task's canonical status) and canonical primary-seed (20260815)
value p0:
    offset fractions f in {0.10, 0.30, 0.60}, applied on BOTH sides of p0:
        grid point (lower side)  = p0 - f * (p0 - lo)
        grid point (upper side)  = p0 + f * (hi - p0)
    plus p0 itself (f=0).
This gives 7 deterministic grid points per parameter (1 + 3 + 3): denser near the canonical
estimate (f=0.10) and sparser toward each bound (f=0.60), fully symmetric in relative terms,
without ever exactly touching a bound (avoiding degenerate boundary DE bounds).

At each grid point, the target parameter is FIXED at that value; the remaining 4 parameters
(always including sigma) are re-optimized via the same Differential Evolution policy used for
primary calibration (strategy=best1bin, popsize=15, mutation=(0.5,1.0), recombination=0.7,
tol=0.01, maxiter=1000), same seed (PRIMARY_SEED=20260815), same calibration-only data
(2001-01..2020-12), same observation model, same bounds for the free parameters. Validation data
never enters this optimization.

Output: outputs/identifiability/profile_objective.csv
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import calibration, data, metrics, model, population, r0, seeds  # noqa: E402

PRIMARY_H = 1.0
CALIBRATION_MONTHS = 240

BOUNDS = {
    "beta": (0.01, 1.00),
    "sigma": (0.01, 0.50),
    "gamma": (0.05, 0.30),
    "d": (0.0001, 0.05),
    "alpha": (0.50, 1.00),
}
PARAM_ORDER = ["beta", "sigma", "gamma", "d", "alpha"]

CANONICAL = {
    "beta": 0.07616353626040417,
    "sigma": 0.010022023505992378,
    "gamma": 0.05680581295281048,
    "d": 0.0003095189898615,
    "alpha": 0.9640110362133341,
}

OFFSET_FRACS = [0.10, 0.30, 0.60]
PROFILE_PARAMETERS = ["beta", "gamma", "d", "alpha"]  # alpha = negative control

OUT_PATH = REPO_ROOT / "outputs/identifiability/profile_objective.csv"


def build_grid(param: str) -> list[float]:
    lo, hi = BOUNDS[param]
    p0 = CANONICAL[param]
    points = [p0]
    for f in OFFSET_FRACS:
        points.append(p0 - f * (p0 - lo))
    for f in OFFSET_FRACS:
        points.append(p0 + f * (hi - p0))
    return sorted(points)


def profile_one_point(
    fixed_param: str,
    fixed_value: float,
    observed_cal: np.ndarray,
    lambda_: float,
    mu: float,
    N_of_t,
    N0: float,
    flow0: float,
) -> dict:
    free_params = [p for p in PARAM_ORDER if p != fixed_param]
    free_bounds = [BOUNDS[p] for p in free_params]

    def objective(x: np.ndarray) -> float:
        values = dict(zip(free_params, x))
        values[fixed_param] = fixed_value
        if values["sigma"] <= 0 or values["gamma"] < 0 or values["d"] < 0:
            return calibration.LARGE_PENALTY
        params = model.SeitParameters(**values)
        try:
            sim = model.simulate(
                params, lambda_, mu, N_of_t, N0, flow0,
                n_months=CALIBRATION_MONTHS, h=PRIMARY_H,
            )
        except Exception:
            return calibration.LARGE_PENALTY
        if sim.solver.status != "ok" or not np.all(np.isfinite(sim.monthly_flow)):
            return calibration.LARGE_PENALTY
        return metrics.rmse(observed_cal, sim.monthly_flow)

    result = differential_evolution(
        objective,
        bounds=free_bounds,
        strategy=calibration.STRATEGY,
        popsize=calibration.POPSIZE,
        mutation=calibration.MUTATION,
        recombination=calibration.RECOMBINATION,
        tol=calibration.TOL,
        maxiter=calibration.MAXITER,
        seed=seeds.PRIMARY_SEED,
        polish=False,
    )

    optimized = dict(zip(free_params, result.x))
    optimized[fixed_param] = fixed_value

    return {
        "profile_parameter": fixed_param,
        "fixed_value": fixed_value,
        "optimized_beta": optimized["beta"],
        "optimized_sigma": optimized["sigma"],
        "optimized_gamma": optimized["gamma"],
        "optimized_d": optimized["d"],
        "optimized_alpha": optimized["alpha"],
        "calibration_rmse": float(result.fun),
        "R0_diagnostic": r0.r0_diagnostic(
            optimized["beta"], optimized["sigma"], optimized["gamma"], optimized["d"], mu
        ),
        "optimizer_success": bool(result.success),
    }


def main() -> None:
    dataset = data.load_canonical_dataset()
    series, _trend = population.build_population_exogenous_series(dataset)
    N_of_t = population.make_N_of_t(series)
    constants_payload = json.loads((REPO_ROOT / "outputs/model_constants.json").read_text())
    mu = constants_payload["mu"]["value"]
    lambda_ = constants_payload["lambda"]["value"]
    N0 = float(dataset.calibration["population"].iloc[0])
    flow0 = float(dataset.calibration["cases"].iloc[0])
    observed_cal = dataset.calibration["cases"].to_numpy(dtype=float)

    canonical_rmse = 605.048881003205  # seed=20260815 fractional primary, for delta_rmse

    rows = []
    for param in PROFILE_PARAMETERS:
        grid = build_grid(param)
        for value in grid:
            row = profile_one_point(param, value, observed_cal, lambda_, mu, N_of_t, N0, flow0)
            row["delta_rmse"] = row["calibration_rmse"] - canonical_rmse
            rows.append(row)
            print(f"{param}={value:.6f} -> rmse={row['calibration_rmse']:.4f} "
                  f"(delta={row['delta_rmse']:+.4f}) R0={row['R0_diagnostic']:.4f}")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "profile_parameter", "fixed_value",
                "optimized_beta", "optimized_sigma", "optimized_gamma",
                "optimized_d", "optimized_alpha",
                "calibration_rmse", "delta_rmse", "R0_diagnostic", "optimizer_success",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {OUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
