# Base Model Reimplementation Report

Stage: first reproducible computational stage of the tb-fractional-seit-brazil independent
reimplementation (canonical data preparation, fractional SEIT + integer comparator
implementation, calibration/validation/sensitivity/robustness evidence pipeline). No AIC, R0,
stability, sensitivity-index, or optimal-control work was attempted, per scope. Manuscript and
LaTeX untouched.

## 1. Executive verdict

**BASE_MODEL_REIMPLEMENTATION_VALID_WITH_LIMITATIONS**

The full pipeline (data preparation, solver, calibration, integer comparator, strict
out-of-sample validation, alpha-bound sensitivity, multi-seed robustness, kill-condition audit)
is implemented, executed, and passing its test suite (48/48). The fractional model produces a
stable, reproducible calibration objective and outperforms the honestly re-fit integer
comparator on the true 2021-2022 holdout. The material limitation: three of five estimated
parameters (beta, gamma, d) are weakly identified from this single national monthly series --
widely different values fit the calibration data almost equally well (Section 12) -- while sigma
and alpha are stably and reproducibly identified. This does not invalidate the base-model
pipeline itself, but it must condition any future use of the individual beta/gamma/d point
estimates (in particular, R0 = beta*sigma/[(sigma+mu)(gamma+mu+d)] depends directly on the two
weakest-identified quantities).

Preconditions checked before this run (Phase 0):
- Worktree clean at start; HEAD matched the expected `1f53e60`.
- Canonical source hashes verified byte-identical to the recorded values (Section "Canonical
  source integrity" below); no diff in either file since `5d1d63b`. No
  `CANONICAL_SOURCE_MUTATION_DETECTED`.
- Seed contract frozen in `docs/METHOD_DECISION_LOG.md` D024 (`PRIMARY_SEED=20260815`,
  `DIAGNOSTIC_SEEDS=[20260816..20260819]`) **before** any DE result existed under it -- resolving
  the sole blocker from the prior run of this pipeline.

### Canonical source integrity / benchmark disclosure

`data/raw/tb_mes.xlsx` SHA-256 = `93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b`
and `manuscript/source/BIOMATEMATICA_UNICAMP.docx` SHA-256 =
`10e652628a7786460243fd47201bbfef498356fcee9766ce3fab48f64fa4ac88`, both re-verified at the start
and end of this run, byte-identical to the recorded values; `git diff 5d1d63b..HEAD` for both
paths is empty.

Prior to this run, a single-seed (20260815) timing benchmark was executed manually to estimate
runtime before committing to the full 5-seed x 2-model run. It printed
`RMSE=605.049, alpha=0.964` to the terminal only -- it wrote **no file** and produced **no
tracked artifact**; there is nothing to reclassify as `NON_CANONICAL_BENCHMARK_ARTIFACT`. Those
numbers happen to numerically match the canonical primary-seed result in Section 6 below (as
expected, since the same seed with the same code deterministically reproduces the same result --
confirmed generally by `tests/test_optimization_contract.py::
test_explicit_integer_seed_runs_deterministically`), but every number cited anywhere in this
report is sourced from the regenerated canonical pipeline outputs listed in
`outputs/EVIDENCE_MANIFEST.csv`, never from that earlier manual observation.

## 2. Data contract

`data/raw/tb_mes.xlsx`, 264 monthly observations, 2001-01 to 2022-12. Calibration = 2001-01 to
2020-12 (N=240); validation = 2021-01 to 2022-12 (N=24); no overlap. Unchanged from the prior
implementation stage; re-verified (`tests/test_seit_model.py`, `tests/test_repository_integrity.py`).

## 3. Population/exogenous-information handling

Unchanged from the prior stage: calibration months use the dataset's own `populacao` column;
validation months use a log-linear trend fit exclusively on 2001-2020
(`ln(N(t)) = 18.9923934417 + 0.0008140043 * t_months`), never the dataset's own 2021-2022 values.
Re-used as-is for this run's calibration/validation/sensitivity executions (no re-fit needed,
nothing changed upstream of it).

## 4. Observation model

Unchanged: `flow_model(t_k) = C(t_{k+1}) - C(t_k)` via the auxiliary Caputo accumulator, per
`docs/MODEL_CONTRACT.md` Section 6. Used identically for calibration, validation, and sensitivity
runs in this stage.

## 5. Numerical solver

Unchanged: Diethelm-Ford-Freed PECE, verified against `exp(-t)` and the Mittag-Leffler function
(Section 11 below re-confirms convergence at the actual primary step used for all runs in this
stage, h=1 month).

## 6. Calibration (executed)

`scripts/run_calibration_multiseed.py --canonical-seed 20260815 --diagnostic-seeds 20260816
20260817 20260818 20260819`. Executable contract verified programmatically before running
(Phase 2; `test_de_hyperparameters_match_model_contract`, `test_primary_bounds_match_contract`):
strategy=best1bin, popsize=15, mutation=(0.5,1.0), recombination=0.7, tol=0.01, maxiter=1000;
bounds beta∈[0.01,1.00], sigma∈[0.01,0.50], gamma∈[0.05,0.30] (primary), d∈[0.0001,0.05],
alpha∈[0.50,1.00] (primary). None of these were changed after seeing any result.

**Fractional multi-seed table** (`outputs/calibration/fractional_multiseed.csv`):

| seed | objective (RMSE) | beta | sigma | gamma | d | alpha | success | iters |
|---|---|---|---|---|---|---|---|---|
| **20260815 (primary)** | **605.049** | **0.07616** | **0.01002** | **0.05681** | **0.000310** | **0.96401** | True | 104 |
| 20260816 | 610.388 | 0.41305 | 0.01012 | 0.28185 | 0.036521 | 0.96355 | True | 70 |
| 20260817 | 606.273 | 0.08519 | 0.01015 | 0.05414 | 0.009352 | 0.96198 | True | 102 |
| 20260818 | 609.571 | 0.27806 | 0.01014 | 0.17386 | 0.038580 | 0.96224 | True | 73 |
| 20260819 | 609.874 | 0.38557 | 0.01004 | 0.28478 | 0.009994 | 0.96235 | True | 77 |

**Integer multi-seed table** (`outputs/calibration/integer_multiseed.csv`, alpha fixed = 1.0
exactly in every row):

| seed | objective (RMSE) | beta | sigma | gamma | d | success | iters |
|---|---|---|---|---|---|---|---|
| **20260815 (primary)** | **776.058** | **0.06117** | **0.01017** | **0.05325** | **0.000213** | True | 52 |
| 20260816 | 776.099 | 0.06566 | 0.01008 | 0.05452 | 0.002840 | True | 63 |
| 20260817 | 773.341 | 0.05901 | 0.01001 | 0.05043 | 0.000937 | True | 80 |
| 20260818 | 782.877 | 0.11334 | 0.01000 | 0.05303 | 0.046437 | True | 50 |
| 20260819 | 780.246 | 0.08533 | 0.01012 | 0.05761 | 0.016936 | True | 44 |

All 10 runs (5 seeds x 2 models) succeeded (`success=True`); nothing was filtered. The primary
row for each model is the `seed==20260815` row **by construction** (the script writes it
directly, never `argmin(objective)`) -- confirmed by
`tests/test_seed_contract.py::test_primary_result_selection_uses_seed_not_min_objective`. Note
this is not merely a formality here: for the integer model, seed 20260817 has a strictly *lower*
objective (773.34 < 776.06) than the primary seed, and it was **not** substituted, per D024.

`outputs/calibration/calibration_metrics.csv`:

| model | RMSE | MAE | bias |
|---|---|---|---|
| fractional | 605.049 | 486.505 | -3.811 |
| integer | 776.058 | 616.156 | 171.238 |

## 7. Multi-seed robustness (executed)

See Section 12 (Identifiability diagnostics) for the full analysis; raw per-seed values are in
Section 6's tables and `outputs/calibration/{fractional,integer}_multiseed.csv`.

## 8. Integer comparator (executed)

Independently re-estimated beta, sigma, gamma, d with alpha fixed at exactly `1.0` (never
reusing the fractional model's parameters), same observation equation, calibration interval,
initial-condition logic, numerical grid (h=1 month), DE configuration, and objective as the
fractional model. `tests/test_seit_model.py::test_integer_comparator_alpha_is_exactly_one` and
`tests/test_seed_contract.py::test_integer_multiseed_alpha_always_exactly_one` both confirm
alpha==1.0 exactly in every one of the 5 integer runs (`outputs/calibration/integer_multiseed.csv`).

Notable pattern (see Section 12/13-C): the integer model's gamma sits within 0.0004-0.008 of its
lower bound (0.05) in **all five** seeds (0.0504-0.0576), unlike the fractional model's gamma,
which ranges much more widely (0.054-0.285). This asymmetry is reported as evidence, not
interpreted further here (no stability/R0 analysis in this stage).

## 9. Strict 2021-2022 validation (executed)

`scripts/run_validation.py`, primary-seed (20260815) parameters only, frozen after calibration.
Single continuous open-loop simulation 2001-01..2022-12; last 24 months compared to observed
cases. No refitting, no reinitialization from observed validation cases, no monthly correction,
and (per Section 3) no use of the dataset's own 2021-2022 population values.

`outputs/validation/validation_metrics.csv`:

| model | RMSE | MAE | bias |
|---|---|---|---|
| fractional | 1117.960 | 953.230 | -851.150 |
| integer | 1759.538 | 1588.649 | -1588.649 |

**Delta_RMSE = RMSE_fractional - RMSE_integer = 1117.960 - 1759.538 = -641.578** (negative favors
fractional). **Delta_MAE = 953.230 - 1588.649 = -635.419** (negative favors fractional). Both
models underpredict on average (negative bias); the integer model's underprediction is
substantially larger and grows over the validation window (row-level residuals in
`outputs/validation/integer_predictions.csv` trend from -346 in 2021-01 to -1376 in 2022-12,
consistent with its near-lower-bound gamma producing an overly persistent decline).

## 10. Alpha-bound sensitivity (executed)

`scripts/run_alpha_sensitivity.py --canonical-seed 20260815`, alpha restricted to `[0.70, 1.00]`
(the manuscript's original bound), all other configuration identical to the primary run.

`outputs/sensitivity/alpha_bound_sensitivity.csv`:

| alpha_lower_bound | beta | sigma | gamma | d | alpha | calibration_rmse | validation_rmse | validation_mae | validation_bias |
|---|---|---|---|---|---|---|---|---|---|
| 0.70 | 0.26801 | 0.01003 | 0.19467 | 0.010226 | 0.96228 | 609.782 | 1160.801 | 990.616 | -904.796 |

Fitted alpha under the restricted bound (0.9623) is essentially identical to the primary-bound
result (0.9640, a 0.18% relative difference) -- **alpha does not materially change under the
narrower, manuscript-original bound**, and it does not sit at either the 0.70 or 1.00 boundary.
Calibration RMSE is 0.78% higher and validation RMSE 3.8% higher under the restricted bound, both
small effects. Per instruction, this comparison did not redefine the primary [0.50,1.00] bound.

## 11. Numerical convergence

Unchanged from the prior stage (re-confirmed, not re-run): h=1 month frozen, max relative
difference vs. h=1/4 is 0.51% (fractional reference) / 0.38% (integer reference), both under the
1% threshold (`outputs/audits/numerical_convergence.csv`).

## 12. Identifiability diagnostics (executed)

`scripts/parameter_robustness_and_kill_test.py` -> `outputs/audits/parameter_robustness.csv`:

| quantity | mean | std | min | max | CV |
|---|---|---|---|---|---|
| beta | 0.2476 | 0.1436 | 0.0762 | 0.4130 | **57.996%** |
| sigma | 0.010093 | 0.0000528 | 0.010022 | 0.010151 | **0.523%** |
| gamma | 0.1703 | 0.1019 | 0.0541 | 0.2848 | **59.850%** |
| d | 0.018951 | 0.015581 | 0.000310 | 0.038580 | **82.218%** |
| alpha | 0.96283 | 0.000802 | 0.96198 | 0.96401 | **0.083%** |
| objective (RMSE) | 608.231 | 2.150 | 605.049 | 610.388 | 0.353% |

No binary threshold is invented here (`docs/MODEL_CONTRACT.md` defines none); the classification
below is a prose judgment over these continuous diagnostics, per explicit instruction.

**Reading**: the calibration objective is extremely stable across all 5 seeds (0.35% CV, a
605-610 range) -- the optimizer reliably finds equally-good fits. But it reaches those
equally-good fits via **materially different** (beta, gamma, d) combinations: beta ranges 5.4x
(0.076-0.413), gamma ranges 5.3x and **spans virtually its entire allowed prior range**
(0.054-0.285 against bounds [0.05,0.30]), and d ranges >100x (0.00031-0.0386, also close to
spanning its full [0.0001,0.05] bound). This is the textbook signature of practical
non-identifiability ("sloppiness") for these three parameters from a single aggregate monthly
series -- exactly the risk flagged in advance in `docs/MODEL_CONTRACT.md` Section 11
(MODERATE identifiability risk). By contrast, sigma and alpha are tightly and reproducibly
identified (CV well under 1%) regardless of which of the other three parameters the optimizer
happened to land on.

**parameter_identifiability = WEAKENS.** Not `FAILS`: the objective surface itself is stable and
reproducible, and 2 of 5 parameters (sigma, alpha) are well-identified. Not `SURVIVES`: 3 of 5
parameters (beta, gamma, d), including the single most epidemiologically central one (beta,
transmission rate), are not individually identifiable from this data under this model structure
-- their point estimates from any single seed (including the primary one) should not be cited as
precise values without disclosing this range.

## 13. Fractional-memory kill test

`outputs/audits/fractional_memory_kill_test.md` (raw); classified here per
`docs/MODEL_CONTRACT.md` Section 15 and this task's explicit worked examples.

**A. parameter_identifiability = WEAKENS** (Section 12).

**B. alpha_behavior = SURVIVES.** Alpha across all 5 primary-bound seeds: 0.9620-0.9640 (CV
0.083%) -- reproducible and seed-independent. It does **not** sit at either bound (distance from
lower bound [0.50]: ~0.46; distance from upper bound [1.00]: ~0.036-0.038 -- close-ish to but not
stuck at the upper bound). Under the restricted [0.70,1.00] sensitivity bound it barely moves
(0.9623 vs. 0.9640, Section 10) -- not an artifact of the wider primary bound being available.
Per the task's own worked examples ("if alpha is unstable across seeds... WEAKENS or FAILS"; "if
alpha repeatedly sticks at a bound... WEAKENS"), neither condition is met, so this axis SURVIVES.
**This is not interpreted as proof of epidemiological memory** -- it only means the alpha
estimate itself is a stable, reproducible, non-boundary feature of the fit, which is a
precondition for (not evidence of) any future memory-effect claim.

**C. integer_comparator = SURVIVES.** Fractional validation RMSE (1117.96) is lower than
integer's (1759.54); Delta_RMSE = -641.58, Delta_MAE = -635.42 (Section 9) -- the integer model
does not match or outperform the fractional model on the true holdout, so this axis does not
FAIL per the task's worked example. Caveat carried forward from Section 8: the integer model's
own gamma sits near its lower bound in all 5 seeds, a pattern of its own worth noting rather than
treating this comparison as a clean, fully-controlled structural test -- both models' gamma
estimates are affected by the same underlying weak identifiability documented in Section 12.

**Overall interpretation**: the base-model pipeline produces a reproducible, stable calibration
objective and a fractional model that outperforms the integer comparator out-of-sample, but the
individual-parameter identifiability weakness (beta, gamma, d) is real, material, and must be
disclosed alongside any future point estimate derived from these parameters -- most importantly
R0, which is a direct function of exactly beta and gamma. No configuration (seeds, bounds,
solver, initialization) was changed in response to any of these findings.

## 14. Limitations

- beta, gamma, d are weakly identified from this single national monthly aggregate series
  (Section 12); any future R0/stability derivation must carry this caveat rather than treat the
  primary-seed point estimate as precise.
- gamma's manuscript-original lower bound region and d's full range are both reached by the
  optimizer at different seeds, reinforcing the `PENDING` external-literature-check flag already
  recorded for these bounds in `docs/EXTERNAL_PARAMETER_CONTRACT.md`.
- The integer comparator's gamma boundary-clustering (Section 8) is a related, separate
  observation that has not been further investigated in this stage (out of scope).
- The `numpy.polyfit`-based log-linear population trend and the direct O(n^2) DFF solver
  carry over unchanged from the prior stage's limitations.

## 15. Evidence manifest

`outputs/EVIDENCE_MANIFEST.csv`: all 19 tracked artifacts are now `COMPLETE` (up from 6
COMPLETE / 13 BLOCKED in the prior stage). Every number reported in this document is sourced
from one of those artifacts, generated by a named script, with the parameter source explicit
(either "seed=20260815 row of `*_multiseed.csv`" or a downstream file built from that row) --
none from the earlier standalone timing benchmark (Section "Canonical source integrity /
benchmark disclosure" below).

## 16. Next permitted scientific step

Given the WEAKENS classification for parameter_identifiability in Section 12/13, and that R0 is
a direct function of exactly the two weakest-identified parameters (beta, gamma), the
responsible next step is **investigate identifiability failure** -- specifically, characterize
why beta/gamma/d trade off (e.g. examine the multiseed parameter vectors for a compensating
relationship, and/or narrow gamma/d's bounds using the `PENDING` external literature check
already flagged in `docs/EXTERNAL_PARAMETER_CONTRACT.md`) -- **before** any R0/stability
derivation is attempted, so that a future R0 value is not reported as a precise point estimate
built on parameters already shown here to be individually unidentifiable.
