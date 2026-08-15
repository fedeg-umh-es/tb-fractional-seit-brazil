"""Differential Evolution calibration harness, per docs/MODEL_CONTRACT.md Section 8.

IMPORTANT -- seed contract: docs/MODEL_CONTRACT.md documents the POLICY that one literal,
documented primary seed plus four literal diagnostic seeds must be fixed and recorded, but it
never states the actual integer values (see BASE_MODEL_REIMPLEMENTATION run,
OPTIMIZATION_CONTRACT_INCOMPLETE). `run_differential_evolution` therefore takes `seed` as a
required keyword argument with NO default: calling it without an explicit seed raises
SeedNotSpecifiedError rather than silently inventing one. This is a deliberate structural guard,
not an oversight.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

import numpy as np
from scipy.optimize import differential_evolution

from .metrics import bias, mae, rmse
from .model import SeitParameters, simulate

# DE hyperparameters fixed by docs/MODEL_CONTRACT.md Section 8 (not seed-dependent).
STRATEGY = "best1bin"
POPSIZE = 15
MUTATION = (0.5, 1.0)
RECOMBINATION = 0.7
TOL = 0.01
MAXITER = 1000

LARGE_PENALTY = 1.0e12


class SeedNotSpecifiedError(RuntimeError):
    """Raised when a DE run is attempted without an explicit, documented literal seed.

    Per the BASE_MODEL_REIMPLEMENTATION task's own optimization contract: 'If maxiter or
    primary seed remains unspecified: STOP with OPTIMIZATION_CONTRACT_INCOMPLETE. Do not invent
    them.' No seed value may be chosen inside this function.
    """


@dataclass(frozen=True)
class CalibrationRun:
    seed: int
    objective: float
    beta: float
    sigma: float
    gamma: float
    d: float
    alpha: float
    success: bool
    iterations: int
    function_evaluations: int
    calibration_rmse: float
    calibration_mae: float
    calibration_bias: float


def run_differential_evolution(
    *,
    observed_flow: np.ndarray,
    lambda_: float,
    mu: float,
    N_of_t: Callable[[float], float],
    N0: float,
    flow0: float,
    h: float,
    bounds: Sequence[tuple[float, float]],
    fixed_alpha: float | None,
    seed: int,
) -> CalibrationRun:
    if seed is None:
        raise SeedNotSpecifiedError(
            "run_differential_evolution requires an explicit literal seed; none was given. "
            "The canonical seed set is not yet defined in docs/MODEL_CONTRACT.md -- see "
            "BASE_MODEL_REIMPLEMENTATION_REPORT.md, OPTIMIZATION_CONTRACT_INCOMPLETE."
        )

    n_months = len(observed_flow)

    def objective(x: np.ndarray) -> float:
        if fixed_alpha is None:
            beta, sigma, gamma, d, alpha = x
        else:
            beta, sigma, gamma, d = x
            alpha = fixed_alpha

        if sigma <= 0 or gamma < 0 or d < 0:
            return LARGE_PENALTY

        params = SeitParameters(beta=beta, sigma=sigma, gamma=gamma, d=d, alpha=alpha)
        try:
            sim = simulate(
                params, lambda_=lambda_, mu=mu, N_of_t=N_of_t,
                N0=N0, flow0=flow0, n_months=n_months, h=h,
            )
        except Exception:
            return LARGE_PENALTY

        if sim.solver.status != "ok" or not np.all(np.isfinite(sim.monthly_flow)):
            return LARGE_PENALTY

        return rmse(observed_flow, sim.monthly_flow)

    result = differential_evolution(
        objective,
        bounds=list(bounds),
        strategy=STRATEGY,
        popsize=POPSIZE,
        mutation=MUTATION,
        recombination=RECOMBINATION,
        tol=TOL,
        maxiter=MAXITER,
        seed=seed,
        polish=False,
    )

    if fixed_alpha is None:
        beta, sigma, gamma, d, alpha = result.x
    else:
        beta, sigma, gamma, d = result.x
        alpha = fixed_alpha

    params = SeitParameters(beta=beta, sigma=sigma, gamma=gamma, d=d, alpha=alpha)
    sim = simulate(
        params, lambda_=lambda_, mu=mu, N_of_t=N_of_t, N0=N0, flow0=flow0,
        n_months=n_months, h=h,
    )

    return CalibrationRun(
        seed=seed,
        objective=float(result.fun),
        beta=float(beta),
        sigma=float(sigma),
        gamma=float(gamma),
        d=float(d),
        alpha=float(alpha),
        success=bool(result.success),
        iterations=int(result.nit),
        function_evaluations=int(result.nfev),
        calibration_rmse=rmse(observed_flow, sim.monthly_flow),
        calibration_mae=mae(observed_flow, sim.monthly_flow),
        calibration_bias=bias(observed_flow, sim.monthly_flow),
    )
