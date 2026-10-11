"""Phases 1-2 of the practical-identifiability audit (IDENTIFIABILITY_AUDIT_REPORT.md).

Phase 1: for every one of the 5 already-calibrated fractional multiseed solutions (none
discarded), compute the R0 diagnostic functional and full-span (2001-01..2022-12) open-loop
predictions, then report calibration RMSE (re-derived from the same predictions, as a
consistency check against the recorded DE objective) and validation RMSE/MAE/bias ->
outputs/identifiability/multiseed_functionals.csv.

Phase 2: across those 5 solutions' monthly predictions, compute per-month mean/std/min/max/CV,
separated into calibration and validation windows -> outputs/identifiability/prediction_dispersion.csv.

Uses only already-frozen calibration parameters (outputs/calibration/fractional_multiseed.csv);
does not re-run any optimization and does not select or discard any seed.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import data, metrics, model, population, r0  # noqa: E402

PRIMARY_H = 1.0
CALIBRATION_MONTHS = 240
TOTAL_MONTHS = 264

MULTISEED_CSV = REPO_ROOT / "outputs/calibration/fractional_multiseed.csv"
CONSTANTS_JSON = REPO_ROOT / "outputs/model_constants.json"

OUT_FUNCTIONALS = REPO_ROOT / "outputs/identifiability/multiseed_functionals.csv"
OUT_DISPERSION = REPO_ROOT / "outputs/identifiability/prediction_dispersion.csv"


def load_seed_rows() -> list[dict]:
    with MULTISEED_CSV.open() as f:
        return list(csv.DictReader(f))


def main() -> None:
    dataset = data.load_canonical_dataset()
    series, _trend = population.build_population_exogenous_series(dataset)
    N_of_t = population.make_N_of_t(series)
    constants_payload = json.loads(CONSTANTS_JSON.read_text())
    mu = constants_payload["mu"]["value"]
    lambda_ = constants_payload["lambda"]["value"]

    N0 = float(dataset.calibration["population"].iloc[0])
    flow0 = float(dataset.calibration["cases"].iloc[0])
    observed_full = dataset.full["cases"].to_numpy(dtype=float)
    observed_cal = observed_full[:CALIBRATION_MONTHS]
    observed_val = observed_full[CALIBRATION_MONTHS:]

    seed_rows = load_seed_rows()
    assert len(seed_rows) == 5, f"expected 5 fractional seeds, found {len(seed_rows)}"

    functional_rows = []
    predictions_by_seed: dict[int, np.ndarray] = {}

    for row in seed_rows:
        seed = int(row["seed"])
        params = model.SeitParameters(
            beta=float(row["beta"]), sigma=float(row["sigma"]),
            gamma=float(row["gamma"]), d=float(row["d"]), alpha=float(row["alpha"]),
        )
        sim = model.simulate(
            params, lambda_, mu, N_of_t, N0, flow0, n_months=TOTAL_MONTHS, h=PRIMARY_H
        )
        if sim.solver.status != "ok":
            raise RuntimeError(f"seed {seed}: solver status={sim.solver.status}")

        predictions_by_seed[seed] = sim.monthly_flow

        pred_cal = sim.monthly_flow[:CALIBRATION_MONTHS]
        pred_val = sim.monthly_flow[CALIBRATION_MONTHS:]

        r0_diag = r0.r0_diagnostic(params.beta, params.sigma, params.gamma, params.d, mu)

        functional_rows.append(
            {
                "seed": seed,
                "beta": params.beta,
                "sigma": params.sigma,
                "gamma": params.gamma,
                "d": params.d,
                "alpha": params.alpha,
                "calibration_rmse": metrics.rmse(observed_cal, pred_cal),
                "R0_diagnostic": r0_diag,
                "validation_rmse": metrics.rmse(observed_val, pred_val),
                "validation_mae": metrics.mae(observed_val, pred_val),
                "validation_bias": metrics.bias(observed_val, pred_val),
            }
        )

    OUT_FUNCTIONALS.parent.mkdir(parents=True, exist_ok=True)
    with OUT_FUNCTIONALS.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "seed", "beta", "sigma", "gamma", "d", "alpha",
                "calibration_rmse", "R0_diagnostic",
                "validation_rmse", "validation_mae", "validation_bias",
            ],
        )
        writer.writeheader()
        writer.writerows(functional_rows)
    print(f"Wrote {OUT_FUNCTIONALS.relative_to(REPO_ROOT)}")

    # Phase 2: per-month dispersion across the 5 solutions' full-span predictions.
    seeds_sorted = sorted(predictions_by_seed)
    stacked = np.vstack([predictions_by_seed[s] for s in seeds_sorted])  # (5, 264)

    dates = dataset.full["date"].tolist()
    dispersion_rows = []
    for month_idx in range(TOTAL_MONTHS):
        values = stacked[:, month_idx]
        mean = float(np.mean(values))
        std = float(np.std(values, ddof=0))
        cv = (std / mean) if mean != 0 else float("nan")
        split = "calibration" if month_idx < CALIBRATION_MONTHS else "validation"
        dispersion_rows.append(
            {
                "date": dates[month_idx].date(),
                "split": split,
                "mean_prediction": mean,
                "std_prediction": std,
                "min_prediction": float(np.min(values)),
                "max_prediction": float(np.max(values)),
                "cv_prediction": cv,
            }
        )

    with OUT_DISPERSION.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "date", "split", "mean_prediction", "std_prediction",
                "min_prediction", "max_prediction", "cv_prediction",
            ],
        )
        writer.writeheader()
        writer.writerows(dispersion_rows)
    print(f"Wrote {OUT_DISPERSION.relative_to(REPO_ROOT)}")

    cal_cv = [r["cv_prediction"] for r in dispersion_rows if r["split"] == "calibration"]
    val_cv = [r["cv_prediction"] for r in dispersion_rows if r["split"] == "validation"]
    print(f"Calibration mean monthly CV: {np.nanmean(cal_cv):.6f}")
    print(f"Validation mean monthly CV:  {np.nanmean(val_cv):.6f}")


if __name__ == "__main__":
    main()
