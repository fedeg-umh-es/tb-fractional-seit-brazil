"""Primary rolling-origin forecasting evaluation. Writes
outputs/forecasting/rolling_origin_predictions.csv: one row per origin x horizon x model.

Models: fractional SEIT (M1), integer SEIT (M2, alpha=1 exactly, independently re-estimated),
persistence (B1), seasonal_naive_12 (B2), SARIMA (B3, frozen order from
docs/SARIMA_BASELINE_CONTRACT.md / outputs/forecasting/sarima_frozen_order.json).

Leakage rule (enforced structurally, not just by convention): every input to every forecast at
origin O is built from tb_seit.rolling_origin.build_training_set(O), which filters the dataset
to date <= O before anything else touches it.
"""

from __future__ import annotations

import csv
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from tb_seit import calibration, data, model, rolling_origin as ro, seeds  # noqa: E402

OUT_PATH = REPO_ROOT / "outputs/forecasting/rolling_origin_predictions.csv"

BOUNDS_FRACTIONAL = [(0.01, 1.00), (0.01, 0.50), (0.05, 0.30), (0.0001, 0.05), (0.50, 1.00)]
BOUNDS_INTEGER = BOUNDS_FRACTIONAL[:4]

FIELDS = [
    "origin", "target_date", "horizon", "model", "observed", "predicted", "residual",
    "train_start", "train_end", "n_train", "seed", "population_source", "status",
]


def _mu() -> float:
    return json.loads((REPO_ROOT / "outputs/model_constants.json").read_text())["mu"]["value"]


def observed_targets(origin: pd.Timestamp) -> np.ndarray:
    dataset = data.load_canonical_dataset()
    full = dataset.full.set_index("date")["cases"]
    targets = [origin + pd.DateOffset(months=h) for h in ro.HORIZONS]
    return np.array([float(full.loc[t]) for t in targets])


def fit_mechanistic(origin: pd.Timestamp, ts: ro.OriginTrainingSet, fixed_alpha: float | None) -> dict:
    mu = _mu()
    lambda_ = mu * ts.train_population.mean()
    N0 = float(ts.train_population[0])
    flow0 = float(ts.train_cases[0])
    trend = ro.fit_origin_population_trend(ts)
    N_of_t = ro.make_origin_N_of_t(ts, trend)

    bounds = BOUNDS_INTEGER if fixed_alpha is not None else BOUNDS_FRACTIONAL
    run = calibration.run_differential_evolution(
        observed_flow=ts.train_cases, lambda_=lambda_, mu=mu, N_of_t=N_of_t,
        N0=N0, flow0=flow0, h=ro.PRIMARY_H, bounds=bounds, fixed_alpha=fixed_alpha,
        seed=seeds.PRIMARY_SEED,
    )
    params = model.SeitParameters(
        beta=run.beta, sigma=run.sigma, gamma=run.gamma, d=run.d, alpha=run.alpha
    )
    forecast = ro.simulate_forecast(
        params, lambda_, mu, N_of_t, N0, flow0,
        n_train_months=ts.n_train, n_horizon_months=12, h=ro.PRIMARY_H,
    )
    return {"forecast": forecast, "run": run, "status": "ok" if run.success else "de_not_success"}


def fit_sarima(ts: ro.OriginTrainingSet, order: dict, seasonal_order: dict) -> np.ndarray:
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            m = SARIMAX(
                ts.train_cases,
                order=(order["p"], order["d"], order["q"]),
                seasonal_order=(
                    seasonal_order["P"], seasonal_order["D"], seasonal_order["Q"], seasonal_order["s"]
                ),
                enforce_stationarity=False, enforce_invertibility=False,
            )
            fit = m.fit(disp=False)
        forecast = np.asarray(fit.get_forecast(12).predicted_mean, dtype=float)
        status = "ok"
    except Exception:  # noqa: BLE001
        forecast = np.full(12, np.nan)
        status = "sarima_fit_failed"
    return forecast, status


def main() -> None:
    sarima_meta = json.loads((REPO_ROOT / "outputs/forecasting/sarima_frozen_order.json").read_text())
    order = sarima_meta["selected_order"]
    seasonal_order = sarima_meta["selected_seasonal_order"]

    rows = []
    for origin in ro.ORIGINS:
        ts = ro.build_training_set(origin)
        targets = [origin + pd.DateOffset(months=h) for h in ro.HORIZONS]
        observed = observed_targets(origin)

        assert ts.train_dates.max() < targets[0], "leakage guard: train_end must precede first target"

        fractional = fit_mechanistic(origin, ts, fixed_alpha=None)
        integer = fit_mechanistic(origin, ts, fixed_alpha=1.0)
        persistence = ro.persistence_forecast(ts, 12)
        seasonal = ro.seasonal_naive_forecast(ts, 12)
        sarima_fc, sarima_status = fit_sarima(ts, order, seasonal_order)

        model_forecasts = {
            "fractional": (fractional["forecast"], seeds.PRIMARY_SEED, fractional["status"]),
            "integer": (integer["forecast"], seeds.PRIMARY_SEED, integer["status"]),
            "persistence": (persistence, "N/A", "ok"),
            "seasonal_naive_12": (seasonal, "N/A", "ok"),
            "SARIMA": (sarima_fc, "N/A", sarima_status),
        }

        for label, (forecast, seed_val, status) in model_forecasts.items():
            for h, target, obs, pred in zip(ro.HORIZONS, targets, observed, forecast):
                pop_source = (
                    "TRAIN_ONLY_EXTRAPOLATION" if target > ts.train_dates.max() else "OBSERVED_TRAIN"
                ) if label in ("fractional", "integer") else "N/A"
                rows.append(
                    {
                        "origin": origin.date(),
                        "target_date": target.date(),
                        "horizon": h,
                        "model": label,
                        "observed": obs,
                        "predicted": pred,
                        "residual": (pred - obs) if np.isfinite(pred) else "",
                        "train_start": ts.train_dates.iloc[0].date(),
                        "train_end": ts.train_dates.iloc[-1].date(),
                        "n_train": ts.n_train,
                        "seed": seed_val,
                        "population_source": pop_source,
                        "status": status,
                    }
                )
        print(f"origin {origin.date()} done "
              f"(fractional rmse={fractional['run'].calibration_rmse:.2f}, "
              f"integer rmse={integer['run'].calibration_rmse:.2f}, sarima={sarima_status})")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {OUT_PATH.relative_to(REPO_ROOT)} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
