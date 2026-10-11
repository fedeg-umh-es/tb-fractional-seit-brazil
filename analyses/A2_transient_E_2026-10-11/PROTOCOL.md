# A2 — Transient of E(t) under the frozen S1 parameters: protocol (written before execution)

Date: 2026-10-11. Plan A continuation, step 4. Responds to Amaury's request A2 and is needed
before drafting the texts B2 and B5. Simulation only: **nothing is fitted or re-fitted.**

## Question

Does the exposed compartment E(t) of the fitted models behave like a slowly draining reservoir
(the wording proposed in B2), or is it sustained by the inflow beta*S*I/N?

## Inputs (read-only)

- Parameter vectors: `evidence_S1/TB_SEIT_EVIDENCE_FREEZE_2026-10-10/phase1/tb_global_refit_phase1/results_global_primary/global_refit_parameters.csv`
  (rows `fractional` and `integer`, seed 20260815).
- Simulator, population series and constants: `tb_seit.model.simulate`,
  `tb_seit.population.build_population_exogenous_series` / `make_N_of_t`,
  `tb_seit.constants.compute_model_constants`, exactly as called in `run_global_refit.py`
  (S1 phase 1 runner): solver step h = 1 month, 264 months, E(0) = y0/sigma with y0 the observed
  case count of 2001-01, I(0) = sigma*E(0)/(gamma+mu+d), T(0) = 0, S(0) = N(0)-E(0)-I(0)-T(0).
  mu = 1/888 month^-1 (`outputs/model_constants.json`).
- Environment: venv from `phase1/requirements_frozen.txt`, single process.

## Quantities saved (solver grid, t = 0..264 months, 265 nodes)

S, E, I, T, N(t); ordinary monthly flow (trapezoid of sigma*E per month, 264 values); inflow
`beta*S*I/N`; outflow `(sigma+mu)*E`; ratio `rho(t) = inflow / outflow`.

## Control before interpreting (decided in advance)

The simulated ordinary monthly flow must reproduce the archived `fractional_predictions.csv` and
`integer_predictions.csv` of S1 phase 1 (264 rows each) with maximum absolute difference
<= 1e-6 cases/month. If it does not, stop and report; do not interpret the diagnostics.

## Diagnostics (decided in advance)

Calibration segment = grid nodes t = 0..240 (months 2001-01 to 2020-12 boundary).

1. **Integer model.** Ordinary least squares of log E(t_j) on t_j over the calibration segment.
   Report the slope b, its ratio to the pure-decay rate -(sigma+mu) (with sigma from the integer
   vector), and the R^2 of the log-linear fit.
2. **Fractional model.** Compare E(t)/E(0) with the Mittag-Leffler function
   `E_alpha(-(sigma+mu) t^alpha)` (alpha, sigma from the fractional vector), the solution of the
   linear part without inflow. Evaluate by the power series `sum_k z^k / Gamma(alpha k + 1)`,
   `z = -(sigma+mu) t^alpha`, accepted only if |z| <= 5 over the evaluated range (otherwise stop
   and report). Report max and mean of |E/E(0) - E_alpha| / E_alpha over the calibration segment
   and over the full 264 months. The exponential-decay hypothesis is not applied to the
   fractional model because alpha is about 0.5.
3. **Both models.** Report rho(t) at t = 0, 60, 120, 180, 240, 264, and its minimum, maximum and
   mean over the calibration segment.

## Interpretation rules (conventions fixed here; the thresholds are not derived from theory)

- The inflow is called **negligible** if max rho(t) <= 0.10 over the calibration segment.
- A model is called **consistent with a draining reservoir** only if (i) the inflow is negligible
  and (ii) for the integer model |b/(-(sigma+mu)) - 1| <= 0.10, or for the fractional model the
  maximum relative difference to E_alpha over the calibration segment is <= 0.10.
- If the inflow is not negligible, the comparison with pure decay can be reported but only
  partially interpreted, and the text must say so. In that case the phrase "slowly draining
  exposed reservoir" is not used for that model.
- Whatever the outcome, results are reported as obtained. No parameter, bound, grid or threshold
  is changed after seeing them. The diagnostics describe the fitted trajectory of the model; they
  do not say anything about tuberculosis biology.

## Stopping conditions

Control above fails; the ML series condition fails; any simulation returns solver status other
than "ok"; non-finite values; any hash or the S1 verifier fails.

## Outputs

`trajectories_fractional.csv`, `trajectories_integer.csv`, `diagnostics.json`, `REPORT.md`,
`transient_E.png`, plus `run_transient_E.py`.
