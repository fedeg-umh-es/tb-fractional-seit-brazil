"""Primary calibration + multi-seed robustness, per docs/MODEL_CONTRACT.md Sections 8/9/12.

NOT EXECUTED as part of the current implementation stage: docs/MODEL_CONTRACT.md documents the
DE hyperparameter POLICY (strategy, popsize, mutation, recombination, tol, maxiter=1000) but
never fixes literal seed values (one canonical + four diagnostic). Per this task's own
instruction ("If seeds are not explicitly defined: STOP rather than selecting arbitrary
values"), this script requires seeds to be supplied explicitly and will refuse to run with
made-up ones -- see tb_seit.calibration.SeedNotSpecifiedError.

Usage (once the canonical seed set is defined in docs/MODEL_CONTRACT.md and passed here):
    python scripts/run_calibration_multiseed.py \
        --canonical-seed <int> --diagnostic-seeds <int> <int> <int> <int>
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import calibration, constants, data, model, population  # noqa: E402

PRIMARY_H = 1.0  # months; frozen by outputs/audits/numerical_convergence.csv (<1% relative diff)

BOUNDS_FRACTIONAL = [
    (0.01, 1.00),  # beta
    (0.01, 0.50),  # sigma
    (0.05, 0.30),  # gamma (primary; see docs/EXTERNAL_PARAMETER_CONTRACT.md)
    (0.0001, 0.05),  # d
    (0.50, 1.00),  # alpha (primary)
]
BOUNDS_INTEGER = BOUNDS_FRACTIONAL[:4]

MULTISEED_FIELDS = [
    "seed", "objective", "beta", "sigma", "gamma", "d", "alpha",
    "success", "iterations", "function_evaluations",
]


def _setup():
    dataset = data.load_canonical_dataset()
    series, _trend = population.build_population_exogenous_series(dataset)
    N_of_t = population.make_N_of_t(series)
    mc = constants.compute_model_constants(dataset.calibration["population"])
    N0 = float(dataset.calibration["population"].iloc[0])
    flow0 = float(dataset.calibration["cases"].iloc[0])
    observed = dataset.calibration["cases"].to_numpy(dtype=float)
    return dataset, N_of_t, mc, N0, flow0, observed


def run_all_seeds(canonical_seed: int, diagnostic_seeds: list[int]) -> None:
    dataset, N_of_t, mc, N0, flow0, observed = _setup()
    seeds = [canonical_seed] + list(diagnostic_seeds)

    for label, bounds, fixed_alpha, out_multiseed, out_params, out_pred in [
        (
            "fractional", BOUNDS_FRACTIONAL, None,
            REPO_ROOT / "outputs/calibration/fractional_multiseed.csv",
            REPO_ROOT / "outputs/calibration/fractional_parameters.csv",
            REPO_ROOT / "outputs/calibration/fractional_predictions.csv",
        ),
        (
            "integer", BOUNDS_INTEGER, 1.0,
            REPO_ROOT / "outputs/calibration/integer_multiseed.csv",
            REPO_ROOT / "outputs/calibration/integer_parameters.csv",
            REPO_ROOT / "outputs/calibration/integer_predictions.csv",
        ),
    ]:
        runs = []
        for seed in seeds:
            run = calibration.run_differential_evolution(
                observed_flow=observed,
                lambda_=mc.lambda_,
                mu=mc.mu,
                N_of_t=N_of_t,
                N0=N0,
                flow0=flow0,
                h=PRIMARY_H,
                bounds=bounds,
                fixed_alpha=fixed_alpha,
                seed=seed,
            )
            runs.append(run)

        out_multiseed.parent.mkdir(parents=True, exist_ok=True)
        with out_multiseed.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=MULTISEED_FIELDS)
            writer.writeheader()
            for run in runs:
                writer.writerow({k: getattr(run, k) for k in MULTISEED_FIELDS})

        primary = runs[0]
        with out_params.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["parameter", "value"])
            for k in ["beta", "sigma", "gamma", "d", "alpha"]:
                writer.writerow([k, getattr(primary, k)])

        params = model.SeitParameters(
            beta=primary.beta, sigma=primary.sigma, gamma=primary.gamma,
            d=primary.d, alpha=primary.alpha,
        )
        sim = model.simulate(
            params, mc.lambda_, mc.mu, N_of_t, N0, flow0,
            n_months=len(observed), h=PRIMARY_H,
        )
        with out_pred.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "observed", "predicted", "residual"])
            for date, obs, pred in zip(dataset.calibration["date"], observed, sim.monthly_flow):
                writer.writerow([date.date(), obs, pred, pred - obs])

        print(f"{label}: wrote {out_multiseed.name}, {out_params.name}, {out_pred.name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical-seed", type=int, required=True)
    parser.add_argument("--diagnostic-seeds", type=int, nargs=4, required=True)
    args = parser.parse_args()
    run_all_seeds(args.canonical_seed, args.diagnostic_seeds)


if __name__ == "__main__":
    main()
