"""Phase 2 of the dimensional-consistency audit: verify programmatically that introducing the
explicit tau0^(1-alpha) reference-time scaling factor (tau0=1 month) leaves the existing
fractional and integer trajectories unchanged, for the primary-seed (20260815) parameters, over
the full 264-month span (calibration + validation segments reported separately).

Writes outputs/audits/dimensional_scaling_numerical_equivalence.csv.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import data, dimensional_audit, metrics, model, population  # noqa: E402

PRIMARY_H = 1.0
CALIBRATION_MONTHS = 240
TOTAL_MONTHS = 264

OUT_PATH = REPO_ROOT / "outputs/audits/dimensional_scaling_numerical_equivalence.csv"


def _read_params(path: Path, keys: list[str]) -> dict:
    with path.open() as f:
        reader = csv.reader(f)
        next(reader)
        return {k: float(v) for k, v in reader if k in keys}


def compare_one(label: str, params_path: Path) -> list[dict]:
    dataset = data.load_canonical_dataset()
    series, _trend = population.build_population_exogenous_series(dataset)
    N_of_t = population.make_N_of_t(series)
    constants_payload = json.loads((REPO_ROOT / "outputs/model_constants.json").read_text())
    mu = constants_payload["mu"]["value"]
    lambda_ = constants_payload["lambda"]["value"]
    N0 = float(dataset.calibration["population"].iloc[0])
    flow0 = float(dataset.calibration["cases"].iloc[0])

    values = _read_params(params_path, ["beta", "sigma", "gamma", "d", "alpha"])
    params = model.SeitParameters(**values)

    y0 = model.initial_conditions(params, mu, N0, flow0)

    baseline = model.simulate(
        params, lambda_, mu, N_of_t, N0, flow0, n_months=TOTAL_MONTHS, h=PRIMARY_H
    )

    scaled_solver_result = dimensional_audit.solve_reference_time_scaled(
        params, lambda_, mu, N_of_t, y0, t_end=float(TOTAL_MONTHS), h=PRIMARY_H, tau0=1.0
    )
    steps_per_month = int(round(1.0 / PRIMARY_H))
    c_scaled = scaled_solver_result.y[:: steps_per_month, model.C_IDX]
    scaled_flow = np.diff(c_scaled)

    rows = []
    for split, sl in [("calibration", slice(0, CALIBRATION_MONTHS)), ("validation", slice(CALIBRATION_MONTHS, TOTAL_MONTHS))]:
        base = baseline.monthly_flow[sl]
        scal = scaled_flow[sl]
        abs_diff = np.abs(base - scal)
        rel_diff = abs_diff / np.maximum(np.abs(base), 1e-12)
        rows.append(
            {
                "model": label,
                "split": split,
                "scaling_factor_c": dimensional_audit.reference_time_scaling_factor(params.alpha),
                "max_absolute_difference": float(np.max(abs_diff)),
                "max_relative_difference": float(np.max(rel_diff)),
                "rmse_difference": metrics.rmse(base, scal),
            }
        )
    return rows


def main() -> None:
    rows = []
    rows += compare_one("fractional", REPO_ROOT / "outputs/calibration/fractional_parameters.csv")
    rows += compare_one("integer", REPO_ROOT / "outputs/calibration/integer_parameters.csv")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "model", "split", "scaling_factor_c",
                "max_absolute_difference", "max_relative_difference", "rmse_difference",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {OUT_PATH.relative_to(REPO_ROOT)}")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
