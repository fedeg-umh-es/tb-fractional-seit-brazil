"""Alpha-bound sensitivity, per docs/MODEL_CONTRACT.md Section 12.3 / task Section "ALPHA BOUND
SENSITIVITY". NOT EXECUTED -- requires the canonical seed (see run_calibration_multiseed.py).

Runs calibration + validation with alpha in [0.70, 1.00] (the manuscript's original bound) using
the SAME canonical seed and otherwise identical configuration as the primary [0.50, 1.00] run,
strictly for comparison -- never to redefine the primary bounds.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import calibration, constants, data, metrics, model, population  # noqa: E402

PRIMARY_H = 1.0
TOTAL_MONTHS = 264
CALIBRATION_MONTHS = 240

BOUNDS_SENSITIVITY = [
    (0.01, 1.00),
    (0.01, 0.50),
    (0.05, 0.30),
    (0.0001, 0.05),
    (0.70, 1.00),  # manuscript's original alpha bound
]


def main(canonical_seed: int) -> None:
    dataset = data.load_canonical_dataset()
    series, _trend = population.build_population_exogenous_series(dataset)
    N_of_t = population.make_N_of_t(series)
    mc = constants.compute_model_constants(dataset.calibration["population"])
    N0 = float(dataset.calibration["population"].iloc[0])
    flow0 = float(dataset.calibration["cases"].iloc[0])
    observed_cal = dataset.calibration["cases"].to_numpy(dtype=float)
    observed_val = dataset.validation["cases"].to_numpy(dtype=float)

    run = calibration.run_differential_evolution(
        observed_flow=observed_cal,
        lambda_=mc.lambda_,
        mu=mc.mu,
        N_of_t=N_of_t,
        N0=N0,
        flow0=flow0,
        h=PRIMARY_H,
        bounds=BOUNDS_SENSITIVITY,
        fixed_alpha=None,
        seed=canonical_seed,
    )

    params = model.SeitParameters(
        beta=run.beta, sigma=run.sigma, gamma=run.gamma, d=run.d, alpha=run.alpha
    )
    sim = model.simulate(
        params, mc.lambda_, mc.mu, N_of_t, N0, flow0, n_months=TOTAL_MONTHS, h=PRIMARY_H
    )
    validation_flow = sim.monthly_flow[CALIBRATION_MONTHS:]

    out_path = REPO_ROOT / "outputs/sensitivity/alpha_bound_sensitivity.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "alpha_lower_bound", "beta", "sigma", "gamma", "d", "alpha",
                "calibration_rmse", "validation_rmse", "validation_mae", "validation_bias",
            ]
        )
        writer.writerow(
            [
                0.70, run.beta, run.sigma, run.gamma, run.d, run.alpha,
                run.calibration_rmse,
                metrics.rmse(observed_val, validation_flow),
                metrics.mae(observed_val, validation_flow),
                metrics.bias(observed_val, validation_flow),
            ]
        )
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical-seed", type=int, required=True)
    args = parser.parse_args()
    main(args.canonical_seed)
