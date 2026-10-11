# A3 — SARIMA coefficients per origin: report (2026-10-11)

Protocol: `PROTOCOL.md`, committed as `bf1e72efd5505100abcaf4872b53117b8ad07063` before execution.
Script: `run_sarima_coefficients.py`. Environment: statsmodels 0.15.0, numpy 2.5.3, scipy 1.18.1
(frozen requirements), single process.

## Result of the reproduction control

**Passed.** The 156 regenerated forecasts (13 origins x 12 horizons) differ from the archived SARIMA
predictions in `phase2/rolling_origin_predictions.csv` by at most 9.2e-9 in relative terms
(tolerance 1e-6). All 13 fits reported optimizer convergence, with no warnings and no non-finite
values. The AIC of the 2020-12 origin, 3194.7051, equals the AIC recorded when the order was frozen
(`outputs/forecasting/sarima_frozen_order.json`, 3194.7051183611375), as expected because both fits
use the same 240 observations. The archived predictions were not modified.

## Coefficients (SARIMA(0,1,2)(1,1,1)12, expanding window)

Full table with standard errors, log-likelihood, AIC and n: `sarima_coefficients_by_origin.csv`.
Summary over the 13 origins:

| Parameter | Range of estimates | Typical SE |
|---|---|---|
| MA(1) | -0.846 to -0.794 | 0.044-0.046 |
| MA(2) | 0.045 to 0.089 | 0.060-0.065 |
| Seasonal AR(12) | 0.116 to 0.142 | 0.067-0.071 |
| Seasonal MA(12) | -0.9986 to -0.9948 | 1.2-2.6 |
| sigma^2 | 169,517 to 178,538 | 193,000-426,000 |

## Points to state when these results are used

- **Fact.** The seasonal MA coefficient is at -0.995 to -0.999, practically on the unit boundary.
  The model was fitted with `enforce_invertibility=False`, the same option as in the archived
  forecasts, so that estimate is allowed to sit there. A coefficient this close to -1 is the usual
  signature of seasonal differencing being applied to a seasonal pattern that is nearly
  deterministic.
- **Fact.** The default (outer-product) standard errors of the seasonal MA term (1.2-2.6) and of
  sigma^2 are very large relative to the estimates. They are numerically produced by statsmodels
  but should not be read as precision: at the boundary the quadratic approximation behind them is
  unreliable. They are reported for completeness and should not be used to construct intervals for
  those two parameters.
- **Inference (not tested).** MA(1) and the seasonal AR term look stable across origins, and MA(2)
  stays small, which is consistent with the order having been chosen on 2001-2020 data and not
  being sensitive to the 12 extra months. This is a visual reading of 13 overlapping fits, not a test.
- **Not claimed.** The coefficients are not epidemiological quantities and the order is not
  re-selected here. Nothing in this step bears on the fractional-versus-baseline comparison beyond
  documenting the SARIMA baseline that was evaluated.

## Pending

Whether to mention the boundary seasonal MA estimate in the manuscript's limitations is an author
decision. If included, the sentence should say that the seasonal MA estimate lies at the
invertibility boundary and its standard error is not informative.
