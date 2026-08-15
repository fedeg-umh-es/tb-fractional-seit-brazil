"""Reduced fractional SEIT model, per docs/MODEL_CONTRACT.md Sections 4-9.

State vector y = [S, E, I, T, C] (5 states):
    C D_t^alpha S = Lambda - beta*S*I/N(t) - mu*S
    C D_t^alpha E = beta*S*I/N(t) - (sigma + mu)*E
    C D_t^alpha I = sigma*E - (gamma + mu + d)*I
    C D_t^alpha T = gamma*I - mu*T                     (decoupled; bookkeeping only)
    C D_t^alpha C = sigma*E                            (auxiliary cumulative-incidence
                                                          accumulator, per MODEL_CONTRACT Sec. 6)

Observation model (MODEL_CONTRACT.md Section 6): the model-implied monthly case count for
calendar month k is the TIME-INTEGRATED flow over that month, obtained as
    flow_model(k) = C(t_{k+1}) - C(t_k)
i.e. the integral of sigma*E(t) over the month via the fractional accumulator C -- NOT sigma*E(t)
sampled instantaneously at a single point. This is the specification actually given in
docs/MODEL_CONTRACT.md; no ambiguity requiring an OBSERVATION_MODEL_AMBIGUOUS stop.

Initial conditions (MODEL_CONTRACT.md Section 5), no free dimensions:
    E0 = flow(t0) / sigma
    I0 = sigma * E0 / (gamma + mu + d)
    T0 = 0
    S0 = N(t0) - E0 - I0 - T0
    C0 = 0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np

from .solver import SolverResult, solve_caputo_fde

N_STATES = 5  # S, E, I, T, C
S_IDX, E_IDX, I_IDX, T_IDX, C_IDX = range(N_STATES)


@dataclass(frozen=True)
class SeitParameters:
    beta: float
    sigma: float
    gamma: float
    d: float
    alpha: float


def initial_conditions(
    params: SeitParameters, mu: float, N0: float, flow0: float
) -> np.ndarray:
    """Analytic, non-free initial state, per MODEL_CONTRACT.md Section 5.

    Recomputed from whichever (sigma, gamma, d) is currently being evaluated -- never a free
    DE dimension. T0 is fixed at 0 (T is decoupled from S/E/I; see module docstring).
    """
    E0 = flow0 / params.sigma
    I0 = params.sigma * E0 / (params.gamma + mu + params.d)
    T0 = 0.0
    S0 = N0 - E0 - I0 - T0
    return np.array([S0, E0, I0, T0, 0.0], dtype=float)


def seit_rhs(
    t: float, y: np.ndarray, params: SeitParameters, lambda_: float, mu: float, N_of_t: Callable[[float], float]
) -> np.ndarray:
    S, E, I, T, C = y
    N = N_of_t(t)
    force_of_infection = params.beta * S * I / N
    dS = lambda_ - force_of_infection - mu * S
    dE = force_of_infection - (params.sigma + mu) * E
    dI = params.sigma * E - (params.gamma + mu + params.d) * I
    dT = params.gamma * I - mu * T
    dC = params.sigma * E
    return np.array([dS, dE, dI, dT, dC], dtype=float)


@dataclass
class SimulationResult:
    solver: SolverResult
    monthly_flow: np.ndarray  # length = n_months, flow_model(k) = C(k+1)-C(k)
    initial_state: np.ndarray


def simulate(
    params: SeitParameters,
    lambda_: float,
    mu: float,
    N_of_t: Callable[[float], float],
    N0: float,
    flow0: float,
    n_months: int,
    h: float,
) -> SimulationResult:
    """Integrate the SEIT+accumulator system for n_months, on a step h (months) grid.

    n_months must be reachable as an integer multiple of h from t=0.
    """
    y0 = initial_conditions(params, mu, N0, flow0)

    def f(t: float, y: np.ndarray) -> np.ndarray:
        return seit_rhs(t, y, params, lambda_, mu, N_of_t)

    result = solve_caputo_fde(f, y0, t_end=float(n_months), h=h, alpha=params.alpha)

    if result.status != "ok":
        monthly_flow = np.full(n_months, np.nan)
        return SimulationResult(solver=result, monthly_flow=monthly_flow, initial_state=y0)

    steps_per_month = int(round(1.0 / h))
    c_at_month = result.y[:: steps_per_month, C_IDX]
    if len(c_at_month) != n_months + 1:
        raise RuntimeError(
            "monthly grid extraction mismatch: check that 1/h is an integer"
        )
    monthly_flow = np.diff(c_at_month)

    return SimulationResult(solver=result, monthly_flow=monthly_flow, initial_state=y0)


def state_population_discrepancy(result: SimulationResult, N_of_t: Callable[[float], float]) -> np.ndarray:
    """Diagnostic only: S+E+I+T - N(t) at every solver grid point. Never used to recalibrate."""
    y = result.solver.y
    t = result.solver.t
    compartment_total = y[:, S_IDX] + y[:, E_IDX] + y[:, I_IDX] + y[:, T_IDX]
    n_vals = np.array([N_of_t(ti) for ti in t])
    return compartment_total - n_vals
