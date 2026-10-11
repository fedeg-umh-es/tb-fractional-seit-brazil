"""Exogenous population forcing N(t), per docs/EXTERNAL_PARAMETER_CONTRACT.md Sections 2-3.

Calibration months (2001-01..2020-12) use the dataset's own `populacao` column directly.
Validation months (2021-01..2022-12) use a log-linear trend fitted EXCLUSIVELY on the
calibration-period population series, extrapolated forward. The dataset's own 2021-2022
`populacao` values are recorded for audit purposes only and are never fed to the model
(PROVENANCE_REQUIRED; no leakage of information not knowable by 2020-12).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .data import CanonicalDataset, month_index

SOURCE_TRAIN_OBSERVED = "OBSERVED_TRAIN"
SOURCE_TRAIN_ONLY_EXTRAPOLATION = "TRAIN_ONLY_EXTRAPOLATION"


@dataclass(frozen=True)
class PopulationTrend:
    """ln(N(t)) = intercept + slope * t, t in months since 2001-01, fit on 2001-01..2020-12 only."""

    intercept: float
    slope: float

    def predict(self, t_months) -> np.ndarray:
        t_months = np.asarray(t_months, dtype=float)
        return np.exp(self.intercept + self.slope * t_months)

    def equation_string(self) -> str:
        return f"ln(N(t)) = {self.intercept:.10f} + {self.slope:.10f} * t_months"


def fit_population_trend(dataset: CanonicalDataset) -> PopulationTrend:
    t = month_index(dataset.calibration["date"]).to_numpy(dtype=float)
    ln_n = np.log(dataset.calibration["population"].to_numpy(dtype=float))
    slope, intercept = np.polyfit(t, ln_n, deg=1)
    return PopulationTrend(intercept=float(intercept), slope=float(slope))


def build_population_exogenous_series(dataset: CanonicalDataset) -> tuple[pd.DataFrame, PopulationTrend]:
    trend = fit_population_trend(dataset)

    rows = []
    for _, row in dataset.calibration.iterrows():
        rows.append(
            {
                "date": row["date"],
                "N_dataset": float(row["population"]),
                "N_model_input": float(row["population"]),
                "source_type": SOURCE_TRAIN_OBSERVED,
                "used_for_model": "N_dataset",
            }
        )

    validation_t = month_index(dataset.validation["date"]).to_numpy(dtype=float)
    extrapolated = trend.predict(validation_t)
    for (_, row), n_model in zip(dataset.validation.iterrows(), extrapolated):
        rows.append(
            {
                "date": row["date"],
                "N_dataset": float(row["population"]),
                "N_model_input": float(n_model),
                "source_type": SOURCE_TRAIN_ONLY_EXTRAPOLATION,
                "used_for_model": "N_model_input",
            }
        )

    series = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    return series, trend


def make_N_of_t(series: pd.DataFrame, origin=None) -> callable:
    """Continuous N(t) via linear interpolation over N_model_input on the monthly grid.

    t is measured in months since the calibration origin (2001-01), consistent with
    tb_seit.data.month_index.
    """
    from .data import CALIBRATION_START

    origin = origin or CALIBRATION_START
    t_grid = month_index(series["date"], origin=origin).to_numpy(dtype=float)
    n_grid = series["N_model_input"].to_numpy(dtype=float)

    def N_of_t(t: float) -> float:
        return float(np.interp(t, t_grid, n_grid))

    return N_of_t
