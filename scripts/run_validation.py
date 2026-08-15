"""Strict open-loop 2021-2022 validation, per docs/MODEL_CONTRACT.md Sections 9-10.

NOT EXECUTED in this implementation stage -- requires outputs/calibration/{fractional,
integer}_parameters.csv, which do not exist because calibration itself is blocked on the
undefined seed contract (see run_calibration_multiseed.py). Reads frozen calibration parameters
only; performs a single continuous open-loop simulation 2001-01..2022-12 and compares the last
24 months against observed cases. No refitting, no reinitialization, no use of validation data
in any decision.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import constants, data, metrics, model, population  # noqa: E402

PRIMARY_H = 1.0
TOTAL_MONTHS = 264  # full 2001-01..2022-12 span
CALIBRATION_MONTHS = 240


def _read_params(path: Path) -> model.SeitParameters:
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found -- calibration has not been run "
            "(blocked: canonical seed set undefined, see OPTIMIZATION_CONTRACT_INCOMPLETE)."
        )
    values = {}
    with path.open() as f:
        reader = csv.reader(f)
        next(reader)
        for k, v in reader:
            values[k] = float(v)
    return model.SeitParameters(**values)


def run_one(label: str, params_path: Path, out_path: Path) -> None:
    dataset = data.load_canonical_dataset()
    series, _trend = population.build_population_exogenous_series(dataset)
    N_of_t = population.make_N_of_t(series)
    mc = constants.compute_model_constants(dataset.calibration["population"])
    N0 = float(dataset.calibration["population"].iloc[0])
    flow0 = float(dataset.calibration["cases"].iloc[0])

    params = _read_params(params_path)
    sim = model.simulate(
        params, mc.lambda_, mc.mu, N_of_t, N0, flow0,
        n_months=TOTAL_MONTHS, h=PRIMARY_H,
    )
    if sim.solver.status != "ok":
        raise RuntimeError(f"{label}: solver status={sim.solver.status} over full 264-month span")

    validation_flow = sim.monthly_flow[CALIBRATION_MONTHS:]
    observed = dataset.validation["cases"].to_numpy(dtype=float)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "observed", "predicted", "residual", "split"])
        for date, obs, pred in zip(dataset.validation["date"], observed, validation_flow):
            writer.writerow([date.date(), obs, pred, pred - obs, "validation"])

    return {
        "model": label,
        "rmse": metrics.rmse(observed, validation_flow),
        "mae": metrics.mae(observed, validation_flow),
        "bias": metrics.bias(observed, validation_flow),
    }


def main() -> None:
    rows = [
        run_one(
            "fractional",
            REPO_ROOT / "outputs/calibration/fractional_parameters.csv",
            REPO_ROOT / "outputs/validation/fractional_predictions.csv",
        ),
        run_one(
            "integer",
            REPO_ROOT / "outputs/calibration/integer_parameters.csv",
            REPO_ROOT / "outputs/validation/integer_predictions.csv",
        ),
    ]
    out_metrics = REPO_ROOT / "outputs/validation/validation_metrics.csv"
    with out_metrics.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["model", "rmse", "mae", "bias"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {out_metrics.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
