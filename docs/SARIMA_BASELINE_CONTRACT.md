# SARIMA Baseline Contract

No SARIMA specification existed in this repository before this task. Per the task's own
instruction ("If no SARIMA contract exists: STOP with SARIMA_BASELINE_CONTRACT_REQUIRED and
define it before running forecasting experiments"), this document defines the order-selection
procedure and the resulting frozen order BEFORE any rolling-origin forecasting evaluation is
run, and without ever inspecting 2021-2022 forecasting performance.

## Order-selection procedure (defined before evaluation)

1. Use ONLY the canonical calibration data, 2001-01 to 2020-12 (N=240, the same fixed window
   already used for the base-model fractional/integer primary calibration) -- never any
   2021-2022 observation.
2. Fit `statsmodels.tsa.statespace.sarimax.SARIMAX` with seasonal period `s=12` (monthly data,
   annual seasonality -- the manuscript's own STL decomposition, Sec 2.2, already establishes a
   seasonal component) over a small, deterministic grid:
   - non-seasonal `(p, d, q)`: `p in {0,1,2}`, `d = 1` (fixed; the manuscript's own ADF test,
     Sec 2.2, is invoked to argue for nonstationarity, so first-differencing is the standard,
     non-cherry-picked default rather than searching `d` too), `q in {0,1,2}`
   - seasonal `(P, D, Q, 12)`: `P in {0,1}`, `D = 1` (fixed; standard default for a single
     dominant annual cycle), `Q in {0,1}`
   - Total grid: `3 x 3 x 2 x 2 = 36` candidate orders.
3. Select the order minimizing AIC on this fixed 2001-2020 fit. Ties broken by lowest total
   parameter count `(p+q+P+Q)`, then by lowest `p`.
4. Freeze the selected `(p,d,q)(P,D,Q,12)` order. It is used, unchanged, for every rolling-origin
   refit in the forecasting evaluation (Phase: PRIMARY PROTOCOL) -- the order itself is selected
   once, on train-only data, before evaluation; only the SARIMAX *coefficients* are re-estimated
   at each rolling origin (on that origin's own expanding training window), exactly analogous to
   how the fractional/integer models' parameters are re-estimated per origin while their
   structure (bounds, DE policy) stays fixed.

## Execution and result

Executed by `scripts/select_sarima_order.py`, output frozen to
`outputs/forecasting/sarima_frozen_order.json` (order + AIC table for full transparency/audit).
This selection is performed once, in this task, before the rolling-origin evaluation script is
run, and is never revisited based on forecasting performance.
