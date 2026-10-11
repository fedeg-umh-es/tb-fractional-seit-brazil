# A1 — Sensitivity to the lower bounds of alpha and sigma: report (2026-10-11)

**Status: STOPPED by the protocol after the first new fit (F-a).** Only F-0 (control) and F-a were
run; F-b, F-c and I-b were not run. Protocol: `PROTOCOL.md`, commit
`46be6493fd63aa5561fb33d23f996ade8cd4d1b4`, written before execution. Script: `run_bounds.py`.
Nothing in `evidence_S1/`, `results_canonical/` or `outputs/` was touched, and neither phase 2 nor
phase 3 was redone.

## Controls

- Script fidelity (objective at the S1 primary vectors): passed (differences 2.3e-13 and 0).
- F-0 (S1 configuration refitted): passed. It reproduces the S1 fractional primary,
  objective 619.318751, alpha 0.502203, sigma 0.010004.

## Why it stopped (two independent stop conditions, both met by F-a)

1. **Mandatory stop: training RMSE improves by more than 1%.** F-a (alpha in [0.20, 1.00], sigma
   in [0.01, 0.50]) reaches 589.307 against 619.319 for the S1 primary, a change of -4.85%.
2. **Numerical-resolution control failed, narrowly.** The maximum pointwise relative change between
   h = 1 and h = 0.25 is 1.0095% against a 1% threshold. The other criteria pass by a wide margin:
   RMSE change 0.016%, MAE change 0.070%, bias change 0.004% of the observed mean, and the
   refinement is monotone (0.5-vs-0.25 difference 24.4 against 54.9 for 1-vs-0.5). The threshold
   was fixed in advance and is not relaxed; no other grid was tried.

## What F-a shows (descriptive; single seed, single fit)

| | S1 primary (F-0) | F-a |
|---|---|---|
| alpha | 0.5022 | **0.2024** (new bound 0.20) |
| sigma | 0.010004 (bound 0.01) | 0.034974 (interior) |
| beta, gamma, d | 0.1200, 0.2613, 0.0391 | 0.0117, 0.2490, 0.0310 |
| Training RMSE | 619.32 | 589.31 (-4.85%) |
| Validation RMSE 2021-2022, open loop | 1216.54 | 1086.82 (-10.66%) |
| Reference R0 (phase-3 function) | 0.3578 | 0.0405 |

**Facts.**

- With the lower bound of alpha lowered to 0.20, the optimizer returns alpha = 0.2024, again within
  0.01 of the lower bound. By the boundary rule fixed in the protocol, alpha is determined by the
  boundary in F-a as it was in F-0. The training objective keeps decreasing as alpha moves down.
- sigma moves away from 0.01 to 0.035 in this fit. In F-a its bound was not changed, so this
  says nothing about sigma at 0.001 (F-b, F-c and I-b would have addressed that).
- beta = 0.0117 lies within 10% of the range width of its lower bound (0.01); the script
  flagged it.
- The validation RMSE of F-a is below that of the S1 integer primary (1759.54), so the ranking
  against the S1 integer primary does not invert. The ranking against I-b was not evaluated
  because I-b was not run.

**Inference (not tested).** In this single fit alpha is not pinned at 0.50 by the data: relaxing
the bound moves it to the next bound. That supports describing alpha as a bound artefact, which is
what Amaury's request A1 anticipated. It also means the S1 primary vector is not the best fit of the
fractional model under wider bounds, and quantities that depend on it (alpha 0.502, R0 0.34-0.59,
fractional-model skill) are conditional on the 0.50 bound. A single DE seed mixes the effect of the
bound with search variability, but a 4.85% change is well outside the 1% near-equivalence band used
in S1 phase 3.

**Not claimed.** That alpha = 0.20 is a better or more plausible value; that the fractional
model forecasts better with wider bounds (no rolling-origin evaluation was run); that sigma is or
is not at its bound at 0.001.

## Consequence for the manuscript and decisions that belong to the authors

This result may force a change to a central claim (Plan A, rule 3): the S1 evidence presents
alpha = 0.502 and the R0 envelope as conditional on a lower bound of 0.50, and the within-family
comparison could change in size under wider bounds. Nothing in the manuscript has been written yet.
Pending decisions:

1. Whether to run F-b, F-c and I-b under this same protocol (about one minute each). The stop
   clause halts this step, so I have not run them without your authorisation.
2. Whether the numerical-control miss (1.0095% against 1%) is accepted as a documented
   limitation or treated as a failure. The protocol treats it as a failure; changing it requires a
   decision, not a new grid chosen after seeing the result.
3. Whether a rolling-origin re-evaluation with widened bounds is warranted. It needs separate
   authorisation from fedeg and Amaury and is not part of Plan A.
4. How B5 and B2 are worded: the manuscript can say that alpha lies at its bound and that, when the
   bound is lowered to 0.20, the fit moves to the new bound with a lower training RMSE (-4.85%) and
   a lower validation RMSE; it cannot present alpha = 0.502 as an estimate.

Steps 6 to 10 were not started: step 8 depends on this step, and the plan requires stopping when a
result may change a central claim.
