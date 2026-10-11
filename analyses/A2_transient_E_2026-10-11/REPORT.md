# A2 — Transient of E(t) under the frozen S1 parameters: report (2026-10-11)

Protocol: `PROTOCOL.md`, committed as `c52891100e98e5f3f1085e1a85d46bb04cbefaa3` before execution.
Script: `run_transient_E.py`. Environment: frozen requirements, single process. Nothing was fitted.

## Control

Passed. The simulated ordinary monthly flow reproduces the archived S1 phase-1 predictions
(264 months per model) with a maximum absolute difference of 4.5e-11 (fractional) and 1.0e-11
(integer) cases per month; tolerance 1e-6. The Mittag-Leffler series condition held (|z| <= 0.183).

## Result against the pre-specified criteria

**Neither model meets the criterion for a "draining reservoir".** The inflow beta*S*I/N is not
negligible in either model (rho = inflow/outflow, threshold 0.10), so the phrase "slowly draining
exposed reservoir" in B2 is not supported by these diagnostics for either model and should not be
used as written.

| | Fractional (alpha = 0.502) | Integer (alpha = 1) |
|---|---|---|
| rho(t) at t = 0 / 120 / 240 / 264 | 0.356 / 0.324 / 0.298 / 0.293 | 1.003 / 0.916 / 0.857 / 0.846 |
| rho over calibration, min-max (mean) | 0.298-0.361 (0.328) | 0.857-1.004 (0.925) |
| Inflow negligible (rho <= 0.10)? | No | No |
| E(240)/E(0); E(264)/E(0) | 0.879; 0.873 | 0.817; 0.791 |
| Diagnostic | ML: max rel. difference 5.9% (calibration) | log-linear slope -0.00087 month^-1, i.e. 7.7% of the pure-decay rate -(sigma+mu) = -0.01130; R^2 = 0.95 |
| Meets 10% criterion on its own? | Yes (5.9% <= 10%) | No (slope 7.7% of pure decay) |
| Consistent with a draining reservoir? | No (inflow not negligible) | No |

## Reading

**Facts.**

- E(t) falls slowly in both models: by 12% (fractional) and 18% (integer) between t = 0 and t = 240
  months, from a starting reservoir of about 0.8 million exposed individuals (E(0) = y0/sigma with
  y0 = 8,088 cases in 2001-01).
- In the **integer** model the inflow almost balances the outflow (rho between 0.86 and 1.00). The
  decline of log E is about one thirteenth of what pure decay would give. The exposed compartment
  is therefore close to a quasi-balance sustained by new exposure, not a reservoir emptying at rate
  sigma + mu. The trajectory is also not log-linear in a mechanical sense: E is flat at first and the
  decline accelerates later (figure, middle panel).
- In the **fractional** model rho is about 0.3, so roughly a third of the outflow is replaced by
  inflow. The ratio E(t)/E(0) stays within 5.9% of the Mittag-Leffler solution of the linear part
  without inflow. That agreement is lenient, because the total decline is small: the observed decline
  at t = 240 is 12.1% against 17.0% predicted by the inflow-free Mittag-Leffler (the model declines
  about 29% less than pure decay). This last comparison was not in the protocol and is a descriptive
  reading of the same output, not a criterion.
- By construction of the initial condition (I(0) = sigma*E(0)/(gamma + mu + d)), rho(0) equals
  R0 * S(0)/N(0). The fractional rho(0) = 0.356 is consistent with the primary reference R0 = 0.3578
  of the S1 phase 3 (0.3578 x 0.9953 = 0.3561). The integer rho(0) = 1.003 corresponds to an
  integer-model reference R0 of about 1.0, a quantity that S1 did not report for the integer model
  and that should not be quoted without its own calculation (pending).

**Inference (not tested).** The fitted fractional trajectory is a slow transient from a large
E(0), kept up by a partial inflow, and the same holds, with a stronger inflow, for the integer
model. This describes the model's fitted trajectory under its initialisation; it does not describe
tuberculosis biology, and it does not turn R0_ref < 1 into a statement about elimination.

**Not claimed.** That E "drains" at rate sigma + mu; that the fractional kernel produces the slow
decline (the integer model also declines slowly, for a different reason: near-balance).

## Consequence for the texts B2 and B5

- B2: drop "slowly draining exposed reservoir". Candidate wording, to be agreed with Amaury:
  "In the fitted trajectories the exposed compartment declines slowly (by about 12% in the
  fractional and 18% in the integer model over the 240 calibration months), with the inflow
  beta*S*I/N replacing about one third (fractional) or most (integer) of the outflow
  (sigma + mu)*E; the reference R0 < 1 of the autonomous linearised system therefore describes the
  asymptote of that system, not the mechanism generating the fitted trajectory."
- B5 depends on step 5 and is not drafted here.

## Pending

The reference R0 of the integer model is not in the S1 evidence. If the manuscript quotes rho(0)
or compares reference R0 across models, it needs a separate, explicit calculation with the phase-3
function; none was run here.
