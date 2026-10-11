"""Diethelm-Ford-Freed fractional Adams-Bashforth-Moulton predictor-corrector (PECE) solver.

Implements the standard method for Caputo-fractional initial value problems:
    C D_t^alpha y(t) = f(t, y(t)),   y(0) = y0,   0 < alpha <= 1

Reference: Diethelm, K., Ford, N.J., Freed, A.D. (2002), "A predictor-corrector approach for
the numerical solution of fractional differential equations", Nonlinear Dynamics 29, 3-22.
Coefficient formulas as summarized in Diethelm (2010) and Garrappa (2018).

At alpha=1 this reduces to a first-order-consistent Adams-Bashforth-Moulton predictor-corrector
for an ordinary differential equation, so the fractional model (alpha<1) and the integer
comparator (alpha=1) share exactly this code path, per docs/MODEL_CONTRACT.md Section 7/9.

Design notes (per BASE_MODEL_REIMPLEMENTATION task, "FRACTIONAL NUMERICAL SOLVER"):
- deterministic (no randomness);
- vector state support (arbitrary number of compartments);
- finite-value and negative-state checks after every step, surfaced in SolverResult.status;
- N_external(t) is supplied as a callable, evaluated at each (possibly sub-monthly) grid node;
- CPU-only, dense numpy arrays, O(n_steps^2) direct convolution (no FFT) -- appropriate for the
  problem size here (at most a few thousand steps), conservative on memory (single float64
  buffer per state).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy.special import gamma as gamma_fn

RHS = Callable[[float, np.ndarray], np.ndarray]


@dataclass
class SolverResult:
    t: np.ndarray  # shape (n_steps+1,)
    y: np.ndarray  # shape (n_steps+1, n_states)
    status: str  # "ok", "non_finite", "negative_state"
    alpha: float
    h: float


def solve_caputo_fde(
    f: RHS,
    y0: np.ndarray,
    t_end: float,
    h: float,
    alpha: float,
    negative_state_tolerance: float = -1e-6,
) -> SolverResult:
    """Solve a vector Caputo-FDE system on [0, t_end] with fixed step h.

    t_end / h must be (numerically) an integer number of steps.
    """
    if not (0.0 < alpha <= 1.0):
        raise ValueError(f"alpha must satisfy 0 < alpha <= 1, got {alpha}")
    if h <= 0:
        raise ValueError("h must be positive")

    n_steps = int(round(t_end / h))
    if abs(n_steps * h - t_end) > 1e-6:
        raise ValueError("t_end must be an integer multiple of h")

    y0 = np.asarray(y0, dtype=float)
    n_states = y0.shape[0]

    t = np.array([j * h for j in range(n_steps + 1)], dtype=float)
    y = np.zeros((n_steps + 1, n_states), dtype=float)
    fvals = np.zeros((n_steps + 1, n_states), dtype=float)

    y[0] = y0
    fvals[0] = f(t[0], y[0])

    h_alpha_ab1 = h**alpha / gamma_fn(alpha + 1.0)
    h_alpha_am2 = h**alpha / gamma_fn(alpha + 2.0)

    status = "ok"

    for n in range(n_steps):
        j = np.arange(0, n + 1, dtype=float)
        b_coeff = (n + 1 - j) ** alpha - (n - j) ** alpha
        predictor_sum = (b_coeff[:, None] * fvals[: n + 1]).sum(axis=0)
        y_pred = y0 + h_alpha_ab1 * predictor_sum

        f_pred = f(t[n + 1], y_pred)

        # General formula for j=0 (Diethelm, Ford & Freed 2002, eq. for a_{0,n+1}); valid at
        # n=0 too since 0**(alpha+1) == 0 for alpha > 0 (no special-casing required/desired).
        a0 = float(n) ** (alpha + 1.0) - (n - alpha) * (n + 1.0) ** alpha
        a_coeff = np.empty(n + 1, dtype=float)
        a_coeff[0] = a0
        if n >= 1:
            jj = np.arange(1, n + 1, dtype=float)
            a_coeff[1:] = (
                (n - jj + 2.0) ** (alpha + 1.0)
                + (n - jj) ** (alpha + 1.0)
                - 2.0 * (n - jj + 1.0) ** (alpha + 1.0)
            )
        corrector_sum = (a_coeff[:, None] * fvals[: n + 1]).sum(axis=0)
        y_next = y0 + h_alpha_am2 * (f_pred + corrector_sum)

        y[n + 1] = y_next
        fvals[n + 1] = f(t[n + 1], y_next)

        if not np.all(np.isfinite(y_next)):
            status = "non_finite"
            y[n + 2 :] = np.nan
            break
        if np.any(y_next < negative_state_tolerance):
            status = "negative_state" if status == "ok" else status

    return SolverResult(t=t, y=y, status=status, alpha=alpha, h=h)
