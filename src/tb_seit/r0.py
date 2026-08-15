"""R0 diagnostic functional, per docs/ASSUMPTIONS_REGISTER.md A35 (formula explicitly given in
the manuscript, Sec 2.5) and IDENTIFIABILITY_AUDIT_REPORT.md.

R0_diagnostic(beta, sigma, gamma, d, mu) = (beta*sigma) / ((sigma+mu)*(gamma+mu+d))

IMPORTANT: this is a diagnostic functional used to assess whether R0 is more or less stable
than its individual component parameters across near-equivalent calibration solutions. It is
NOT a manuscript R0 estimate, NOT a final epidemiological result, and must not be reported as
such -- see IDENTIFIABILITY_AUDIT_REPORT.md for the governing distinction between parameter,
predictive, and functional identifiability.
"""

from __future__ import annotations


def r0_diagnostic(beta: float, sigma: float, gamma: float, d: float, mu: float) -> float:
    return (beta * sigma) / ((sigma + mu) * (gamma + mu + d))
