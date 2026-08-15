"""Fixed demographic constants mu, Lambda, per docs/EXTERNAL_PARAMETER_CONTRACT.md Section 2/4.

mu = 1 / (74 * 12) per month, from an approximate 2001-2020-average Brazilian life expectancy
at birth of ~74 years (IBGE anchors; see docs/EXTERNAL_PARAMETER_CONTRACT.md, mu row and D015).
Lambda = mu * mean(N(t)) over the calibration window only (2001-01..2020-12), i.e. demographic
closure using training-period population exclusively -- never validation-period population.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

LIFE_EXPECTANCY_YEARS = 74.0
MONTHS_PER_YEAR = 12


@dataclass(frozen=True)
class ModelConstants:
    mu: float
    life_expectancy_years: float
    lambda_: float
    mean_training_population: float


def compute_mu(life_expectancy_years: float = LIFE_EXPECTANCY_YEARS) -> float:
    return 1.0 / (life_expectancy_years * MONTHS_PER_YEAR)


def compute_lambda(mu: float, training_population: pd.Series) -> tuple[float, float]:
    mean_n = float(training_population.mean())
    return mu * mean_n, mean_n


def compute_model_constants(training_population: pd.Series) -> ModelConstants:
    mu = compute_mu()
    lambda_, mean_n = compute_lambda(mu, training_population)
    return ModelConstants(
        mu=mu,
        life_expectancy_years=LIFE_EXPECTANCY_YEARS,
        lambda_=lambda_,
        mean_training_population=mean_n,
    )
