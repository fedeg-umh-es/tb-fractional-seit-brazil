# A1 — Sensitivity to the lower bounds of alpha and sigma: protocol (written before execution)

Date: 2026-10-11. Plan A continuation, step 5. Responds to Amaury's request A1.
Authorisation: step 5 of Plan A (fedeg). Evaluation in rolling origin is **not** authorised here.

## Why this fit is justified

In the S1 global fits, alpha (0.5022, bound 0.50) and sigma (0.01000, bound 0.01) sit at their
lower bounds. This analysis asks whether those two values are determined by the bounds or by the
calibration data. It does not look for a better model and does not change the S1 evidence.

## Fits (all on calibration 2001-01 to 2020-12, 240 months)

Common settings, identical to S1 phase 1 (`run_global_refit.py`): ordinary composite-trapezoid
observation operator; solver h = 1 month; initial state E(0) = y0/sigma, I(0) =
sigma*E(0)/(gamma+mu+d), T(0) = 0; mu = 1/888; Lambda and N(t) as in S1; objective = calibration
RMSE; `scipy.optimize.differential_evolution` with strategy best1bin, popsize 15,
mutation (0.5, 1), recombination 0.7, tol 0.01, maxiter 1000, polish False, seed 20260815, single
process. Unchanged bounds: beta [0.01, 1.00], gamma [0.05, 0.30], d [0.0001, 0.05].

| Id | Model | alpha bounds | sigma bounds |
|---|---|---|---|
| F-0 (control) | fractional | [0.50, 1.00] | [0.01, 0.50] |
| F-a | fractional | [0.20, 1.00] | [0.01, 0.50] |
| F-b | fractional | [0.50, 1.00] | [0.001, 0.50] |
| F-c | fractional | [0.20, 1.00] | [0.001, 0.50] |
| I-b | integer (alpha = 1) | fixed | [0.001, 0.50] |

The sigma lower bound 0.001 month^-1 (mean E-to-I progression time of about 83 years) was
proposed in the plan and accepted by fedeg on 2026-10-11. F-0 repeats the S1 primary
configuration; it exists only as a control of this script.

## Controls before interpreting (decided in advance)

1. **Script fidelity.** The objective evaluated at the S1 primary vectors (fractional and integer,
   `phase1/.../global_refit_parameters.csv`) equals the stored `objective_train_rmse` within 1e-8;
   F-0 reproduces the S1 fractional primary objective (619.3187514936859) within 1e-6 and its
   parameters within 1e-6 (relative).
2. **Numerical resolution of every new vector** (F-a, F-b, F-c, I-b), same criterion as S1
   phase 2 and 3 (`numerical_check`): predictions with h = 1, 0.5 and 0.25 months; pass if the
   maximum pointwise relative change between h = 1 and h = 0.25 <= 1%, relative changes of RMSE and
   MAE <= 1%, change in bias <= 1% of the observed mean, and the h = 0.5-vs-0.25 difference does
   not exceed the h = 1-vs-0.5 difference (tolerance 1e-9). Alpha near 0.2 may fail; if it does,
   stop and report (no other grid is tried).

## Outputs per fit

Parameters, calibration RMSE (objective), optimizer success/iterations/evaluations, calibration
MAE and bias, open-loop validation RMSE/MAE/bias for 2021-2022 (264-month continuous simulation,
population extrapolated from training only, as S1 phase 1), R0 reference via
`tb_seit.r0.r0_diagnostic` (the function of phase 3), and a comparison table against the S1
primary of phase 1 (relative change of the training objective and of the validation RMSE).

## Interpretation criteria (fixed before running)

- **Boundary rule.** A fitted alpha is "determined by the boundary" if it lies within 0.01 of its
  lower bound (absolute distance, as in the plan). A fitted sigma is "determined by the boundary"
  if sigma < 1.1 x its lower bound (relative distance of 10%). The plan states a common absolute
  0.01 for both; for sigma, whose range spans two orders of magnitude, that would label as
  boundary-driven any value up to 0.011 even with a bound at 0.001. The relative rule was chosen
  by fedeg on 2026-10-11 and is a deliberate departure from the literal text of the plan. For
  F-0 and F-a (sigma bound 0.01) both rules give the same result.
- Boundary-driven: write that the value is set by the bound, not by the data. Interior: report the
  value and the relative change of the training objective against the S1 primary.
- Other parameters (beta, gamma, d) are only checked for closeness to either of their bounds with
  the same rules (absolute 0.01 is not meaningful for them, so the relative 10% of the range
  width is used) and reported. The bound of d is **not** widened.
- A relative training-RMSE change within 1% is inside the near-equivalence band used in S1 phase
  3 and is not a material improvement. A single seed is used, so differences between fits mix the
  effect of the bound with search variability; this is a stated limit, not corrected here.

## Mandatory stops (no further step, no phase 2/3 redo)

Report and stop if any of the following occurs; evaluation in rolling origin would require a
separate authorisation from fedeg and Amaury:

- the calibration RMSE of any fit is more than 1% lower than the S1 primary of the same model
  (619.3187514936859 fractional, 776.0408518 integer);
- the ranking of fractional against integer in validation inverts: any fractional fit (F-a, F-b,
  F-c) has an open-loop 2021-2022 RMSE >= that of I-b or >= that of the S1 integer primary;
- the optimizer does not report success, or returns an invalid or penalised objective;
- a control above fails; a hash or the S1 verifier fails; a test fails.

## Outputs

`fit_parameters.csv`, `comparison_with_S1_primary.csv`, `numerical_controls.csv`,
`predictions_<id>.csv` (calibration and validation), `REPORT.md`, and the script `run_bounds.py`.
