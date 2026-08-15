"""Rolling-origin forecasting evaluation primitives, per FORECASTING_EVALUATION_REPORT.md.

Origins: 2020-12 through 2021-12 (13 monthly origins), chosen deterministically so that every
origin's full h=1..12 horizon set has targets falling entirely within the primary evaluation
window 2021-01..2022-12 and entirely within the available dataset (<=2022-12) -- a fully-crossed
origin x horizon grid with no partial-horizon origins.

Leakage rule: every quantity used to produce a forecast at a given origin (training data,
population extrapolation, Lambda, DE-estimated parameters, SARIMA coefficients) is built using
ONLY observations with date <= origin. mu is the sole exception -- it is an externally fixed
demographic constant (life-expectancy-derived), not data-derived, so it is identical at every
origin by construction, not "leaked" from the future.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .data import CALIBRATION_START, load_canonical_dataset, month_index
from .model import SeitParameters, initial_conditions, seit_rhs
from .solver import solve_caputo_fde

ORIGINS = pd.date_range("2020-12-01", "2021-12-01", freq="MS")
HORIZONS = list(range(1, 13))
PRIMARY_H = 1.0


@dataclass(frozen=True)
class OriginTrainingSet:
    origin: pd.Timestamp
    train_dates: pd.Series
    train_cases: np.ndarray
    train_population: np.ndarray
    n_train: int


def build_training_set(origin: pd.Timestamp) -> OriginTrainingSet:
    dataset = load_canonical_dataset()
    train_df = dataset.full[dataset.full["date"] <= origin].reset_index(drop=True)
    return OriginTrainingSet(
        origin=origin,
        train_dates=train_df["date"],
        train_cases=train_df["cases"].to_numpy(dtype=float),
        train_population=train_df["population"].to_numpy(dtype=float),
        n_train=len(train_df),
    )


@dataclass(frozen=True)
class OriginPopulationTrend:
    intercept: float
    slope: float

    def predict(self, t_months) -> np.ndarray:
        t_months = np.asarray(t_months, dtype=float)
        return np.exp(self.intercept + self.slope * t_months)


def fit_origin_population_trend(training: OriginTrainingSet) -> OriginPopulationTrend:
    """Log-linear trend fit EXCLUSIVELY on population values with date <= origin."""
    t = month_index(training.train_dates).to_numpy(dtype=float)
    ln_n = np.log(training.train_population)
    slope, intercept = np.polyfit(t, ln_n, deg=1)
    return OriginPopulationTrend(intercept=float(intercept), slope=float(slope))


def make_origin_N_of_t(training: OriginTrainingSet, trend: OriginPopulationTrend):
    """N(t): observed population for t within the training window (linear interpolation over
    the training grid), log-linear extrapolation (fit on training data only) beyond it."""
    t_grid = month_index(training.train_dates).to_numpy(dtype=float)
    n_grid = training.train_population
    t_max = t_grid.max()

    def N_of_t(t: float) -> float:
        if t <= t_max:
            return float(np.interp(t, t_grid, n_grid))
        return float(trend.predict(t))

    return N_of_t


def origin_month_index(origin: pd.Timestamp) -> int:
    return int(month_index(pd.Series([origin]), origin=CALIBRATION_START).iloc[0])


def simulate_forecast(
    params: SeitParameters,
    lambda_: float,
    mu: float,
    N_of_t,
    N0: float,
    flow0: float,
    n_train_months: int,
    n_horizon_months: int,
    h: float = PRIMARY_H,
) -> np.ndarray:
    """Integrate from t=0 (2001-01) through n_train_months + n_horizon_months, return the
    monthly flow for the n_horizon_months AFTER the training window (i.e. the h=1..H forecast).
    """
    y0 = initial_conditions(params, mu, N0, flow0)

    def f(t: float, y: np.ndarray) -> np.ndarray:
        return seit_rhs(t, y, params, lambda_, mu, N_of_t)

    total_months = n_train_months + n_horizon_months
    result = solve_caputo_fde(f, y0, t_end=float(total_months), h=h, alpha=params.alpha)
    if result.status != "ok":
        return np.full(n_horizon_months, np.nan)

    steps_per_month = int(round(1.0 / h))
    c_at_month = result.y[:: steps_per_month, 4]  # C_IDX
    monthly_flow = np.diff(c_at_month)
    return monthly_flow[n_train_months : n_train_months + n_horizon_months]


def persistence_forecast(training: OriginTrainingSet, n_horizon: int) -> np.ndarray:
    last_value = training.train_cases[-1]
    return np.full(n_horizon, last_value)


def seasonal_naive_forecast(training: OriginTrainingSet, n_horizon: int, season: int = 12) -> np.ndarray:
    """y_hat(origin+h) = y(origin+h-season), using only training-window observations
    (origin+h-season <= origin for all h<=season, so always within history)."""
    n = training.n_train
    out = np.empty(n_horizon)
    for h in range(1, n_horizon + 1):
        idx = n - season + (h - 1)  # index into train_cases for date origin+h-season
        out[h - 1] = training.train_cases[idx]
    return out
