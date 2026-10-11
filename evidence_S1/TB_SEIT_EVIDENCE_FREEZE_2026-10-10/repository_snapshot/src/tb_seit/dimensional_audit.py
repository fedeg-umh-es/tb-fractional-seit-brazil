"""Reference-time dimensional-consistency audit helpers, per
docs/FRACTIONAL_DIMENSIONAL_CONSISTENCY.md.

This module is AUDIT-ONLY: it does not modify, wrap, or get imported by the production
forecasting pipeline (src/tb_seit/model.py, solver.py, calibration.py are untouched). It exists
solely to (a) numerically verify that introducing the explicit tau0^(1-alpha) reference-time
scaling factor leaves existing predictions unchanged when tau0=1 month (Phase 2), and (b) verify
the algebraic invariance of R0 and the Matignon stability classification under a general
positive scaling factor c (Phases 4-5), including a non-trivial c far from 1 as a stronger test
than the trivial c=1 case relevant to this project's actual units.
"""

from __future__ import annotations

from typing import Callable

import numpy as np

from .model import SeitParameters, seit_rhs
from .solver import SolverResult, solve_caputo_fde

TAU0_MONTHS = 1.0  # the reference timescale used throughout this project's time axis


def reference_time_scaling_factor(alpha: float, tau0: float = TAU0_MONTHS) -> float:
    """c = tau0^(1-alpha). Dimensionally [time]^(1-alpha); numerically 1.0 for tau0=1 exactly,
    for ANY alpha, since 1**x == 1."""
    return tau0 ** (1.0 - alpha)


def seit_rhs_reference_time_scaled(
    t: float,
    y: np.ndarray,
    params: SeitParameters,
    lambda_: float,
    mu: float,
    N_of_t: Callable[[float], float],
    tau0: float = TAU0_MONTHS,
) -> np.ndarray:
    """C D_t^alpha X = tau0^(1-alpha) * F(X; theta), per
    docs/FRACTIONAL_DIMENSIONAL_CONSISTENCY.md. F is the UNCHANGED production vector field
    (tb_seit.model.seit_rhs); only the explicit scalar conversion factor is added here,
    multiplying the entire vector field uniformly."""
    c = reference_time_scaling_factor(params.alpha, tau0)
    return c * seit_rhs(t, y, params, lambda_, mu, N_of_t)


def solve_reference_time_scaled(
    params: SeitParameters,
    lambda_: float,
    mu: float,
    N_of_t: Callable[[float], float],
    y0: np.ndarray,
    t_end: float,
    h: float,
    tau0: float = TAU0_MONTHS,
) -> SolverResult:
    def f(t: float, y: np.ndarray) -> np.ndarray:
        return seit_rhs_reference_time_scaled(t, y, params, lambda_, mu, N_of_t, tau0)

    return solve_caputo_fde(f, y0, t_end=t_end, h=h, alpha=params.alpha)


# ---- Phase 4/5: NGM and Jacobian scaling invariance ----------------------------------------


def j_ei(beta: float, sigma: float, gamma: float, d: float, mu: float) -> np.ndarray:
    """Jacobian of the (E,I) infected subsystem at the DFE (S*/N*=1), per
    R0_STABILITY_ANALYSIS_NOTE.md Step 4."""
    return np.array([[-(sigma + mu), beta], [sigma, -(gamma + mu + d)]])


def f_v_matrices(beta: float, sigma: float, gamma: float, d: float, mu: float) -> tuple[np.ndarray, np.ndarray]:
    f_mat = np.array([[0.0, beta], [0.0, 0.0]])
    v_mat = np.array([[sigma + mu, 0.0], [-sigma, gamma + mu + d]])
    return f_mat, v_mat


def r0_from_ngm(beta: float, sigma: float, gamma: float, d: float, mu: float) -> float:
    f_mat, v_mat = f_v_matrices(beta, sigma, gamma, d, mu)
    ngm = f_mat @ np.linalg.inv(v_mat)
    eigenvalues = np.linalg.eigvals(ngm)
    return float(np.max(np.abs(eigenvalues)))


def eigenvalue_arguments(j: np.ndarray) -> np.ndarray:
    return np.angle(np.linalg.eigvals(j))


def matignon_margin(j: np.ndarray, alpha: float) -> float:
    """min_i (|arg(lambda_i)| - alpha*pi/2). Negative => unstable (per Matignon); the
    magnitude away from zero indicates how far from the boundary. Uses the eigenvalue with the
    SMALLEST |arg| (closest to instability / most binding for the stability check)."""
    args = np.abs(eigenvalue_arguments(j))
    return float(np.min(args) - alpha * np.pi / 2.0)
