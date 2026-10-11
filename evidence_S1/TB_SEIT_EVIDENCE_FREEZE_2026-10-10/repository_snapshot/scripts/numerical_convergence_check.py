"""Write outputs/audits/numerical_convergence.csv.

Deterministic step-size convergence check at a FIXED, ARBITRARY parameter vector (bounds
midpoint of the primary contract bounds -- never a fitted/optimized value), per
docs/MODEL_CONTRACT.md Sections 7/12.1. This determines/confirms the primary time step h purely
on numerical-accuracy grounds; it must NOT be, and is not, selected on validation RMSE.

Runs both the fractional model (alpha=0.75, an arbitrary in-bounds midpoint) and the integer
comparator (alpha=1.0) at h in {1, 1/2, 1/4} months over the full 240-month calibration window,
and reports each finer step against the coarsest (h=1) as the reference.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import constants, data, model, population  # noqa: E402

OUTPUT_CSV = REPO_ROOT / "outputs" / "audits" / "numerical_convergence.csv"

STEPS = [1.0, 0.5, 0.25]
N_MONTHS = 240  # full calibration window

REFERENCE_PARAMS_FRACTIONAL = model.SeitParameters(
    beta=(0.01 + 1.00) / 2,
    sigma=(0.01 + 0.50) / 2,
    gamma=(0.05 + 0.30) / 2,
    d=(0.0001 + 0.05) / 2,
    alpha=(0.50 + 1.00) / 2,  # arbitrary in-bounds midpoint, alpha=0.75
)
REFERENCE_PARAMS_INTEGER = model.SeitParameters(
    beta=REFERENCE_PARAMS_FRACTIONAL.beta,
    sigma=REFERENCE_PARAMS_FRACTIONAL.sigma,
    gamma=REFERENCE_PARAMS_FRACTIONAL.gamma,
    d=REFERENCE_PARAMS_FRACTIONAL.d,
    alpha=1.0,
)


def run_model(params: model.SeitParameters, label: str) -> list[dict]:
    dataset = data.load_canonical_dataset()
    series, _trend = population.build_population_exogenous_series(dataset)
    N_of_t = population.make_N_of_t(series)
    mc = constants.compute_model_constants(dataset.calibration["population"])

    N0 = float(dataset.calibration["population"].iloc[0])
    flow0 = float(dataset.calibration["cases"].iloc[0])
    observed = dataset.calibration["cases"].to_numpy(dtype=float)

    rows = []
    reference_flow = None
    for h in STEPS:
        sim = model.simulate(
            params, mc.lambda_, mc.mu, N_of_t, N0, flow0, n_months=N_MONTHS, h=h
        )
        calibration_rmse = (
            float(np.sqrt(np.mean((observed - sim.monthly_flow) ** 2)))
            if sim.solver.status == "ok"
            else float("nan")
        )
        if h == STEPS[0]:
            reference_flow = sim.monthly_flow
            max_abs_diff = 0.0
            rel_diff = 0.0
        elif sim.solver.status == "ok" and reference_flow is not None:
            diff = sim.monthly_flow - reference_flow
            max_abs_diff = float(np.max(np.abs(diff)))
            denom = float(np.max(np.abs(reference_flow))) or 1.0
            rel_diff = max_abs_diff / denom
        else:
            max_abs_diff = float("nan")
            rel_diff = float("nan")

        rows.append(
            {
                "model": label,
                "step": h,
                "calibration_rmse": calibration_rmse,
                "max_absolute_prediction_difference": max_abs_diff,
                "relative_prediction_difference": rel_diff,
                "solver_status": sim.solver.status,
            }
        )
    return rows


def main() -> None:
    rows = run_model(REFERENCE_PARAMS_FRACTIONAL, "fractional_alpha_0.75_reference") + run_model(
        REFERENCE_PARAMS_INTEGER, "integer_alpha_1.0_reference"
    )

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "model",
                "step",
                "calibration_rmse",
                "max_absolute_prediction_difference",
                "relative_prediction_difference",
                "solver_status",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {OUTPUT_CSV.relative_to(REPO_ROOT)}")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
