# Base Model Reimplementation Report

Stage: first reproducible computational stage of the tb-fractional-seit-brazil independent
reimplementation (canonical data preparation, fractional SEIT + integer comparator
implementation, calibration/validation/sensitivity harness). No AIC, R0, stability,
sensitivity-index, or optimal-control work was attempted, per scope. Manuscript and LaTeX
untouched.

## 1. Executive verdict

**IMPLEMENTATION_BLOCKED** (partial — data preparation, numerical infrastructure, and solver
verification are COMPLETE and PASSING; calibration and everything downstream of it are blocked
on a genuine, pre-existing gap in the governing contract, not on any defect found in the model
itself).

Two preconditions were checked before implementation began, per this task's own instructions:

- **Worktree cleanliness**: the tree was NOT clean at the start (see Section 14/D023 in
  `docs/METHOD_DECISION_LOG.md`) — it held uncommitted, already-reviewed documentation from the
  two immediately preceding methodology-review turns of this same collaboration
  (`docs/MODEL_CONTRACT.md`, `docs/EXTERNAL_PARAMETER_CONTRACT.md`). These were committed as a
  separate, documentation-only prerequisite commit rather than halting the task outright; the
  reported `CURRENT CANONICAL HEAD` (`5d1d63b`) also did not match the actual HEAD (`e683c93`,
  due to an external amend) — both discrepancies are logged, not silently absorbed.
- **Optimization contract completeness**: `docs/MODEL_CONTRACT.md` Section 8 fixes the DE
  hyperparameter *policy* (strategy, popsize, mutation, recombination, tol, maxiter=1000) but
  never states literal seed integers (one canonical + four diagnostic). Per this task's explicit
  instruction ("Do not invent them" / "STOP rather than selecting arbitrary values"), calibration
  was not executed. `tb_seit.calibration.run_differential_evolution` enforces this structurally:
  `seed` has no default and raises `SeedNotSpecifiedError` if passed `None`.

## 2. Data contract

`data/raw/tb_mes.xlsx`, 264 monthly observations, 2001-01 to 2022-12. Calibration = 2001-01 to
2020-12 (N=240); validation = 2021-01 to 2022-12 (N=24); no overlap. Implemented in
`src/tb_seit/data.py`, verified in `tests/test_seit_model.py`
(`test_calibration_validation_split_sizes`, `test_calibration_validation_no_overlap`,
`test_calibration_validation_boundary`) and the pre-existing
`tests/test_repository_integrity.py`. The pre-existing dataset-integrity audit
(`outputs/audits/dataset_integrity.json`) was not re-run in this stage (unchanged since the
prior specification stage; still 264/240/24, 0 anomalies).

## 3. Population/exogenous-information handling

`src/tb_seit/population.py`, executed via `scripts/build_population_exogenous_series.py` ->
`outputs/audits/population_exogenous_series.csv` (+ `..._trend.json`). Calibration months use
the dataset's own `populacao` column directly (`source_type=OBSERVED_TRAIN`). Validation months
use a log-linear trend fitted **exclusively** on 2001-01..2020-12
(`ln(N(t)) = 18.9923934417 + 0.0008140043 * t_months`), extrapolated forward
(`source_type=TRAIN_ONLY_EXTRAPOLATION`); the dataset's own 2021-2022 `populacao` values are
recorded for audit only and never fed to the model, per `docs/EXTERNAL_PARAMETER_CONTRACT.md`
Sections 2-3 (`PROVENANCE_REQUIRED`). Verified: extrapolated validation-window population differs
materially from the dataset's own values (e.g. Dec-2022: 219.4M extrapolated vs. 214.7M in the
dataset), confirming no leakage; `test_population_trend_is_fit_on_training_data_only` confirms
corrupting the dataset's validation-period population does not change the fitted trend. The
compartment total `S+E+I+T` is not constrained to equal `N_external(t)`
(`model.state_population_discrepancy`, diagnostic-only, never used to recalibrate).

## 4. Observation model

Implemented exactly as `docs/MODEL_CONTRACT.md` Section 6 specifies — **no
OBSERVATION_MODEL_AMBIGUOUS stop was needed**, the document resolves this unambiguously: an
auxiliary Caputo accumulator `C(t)` with `cD^alpha_t C = sigma*E(t)`, and
`flow_model(t_k) = C(t_{k+1}) - C(t_k)`, i.e. the **time-integrated** flow over each month, not
`sigma*E(t)` sampled instantaneously. `tests/test_seit_model.py::
test_observation_model_is_time_integrated_flow_not_instantaneous_sample` confirms both that the
implementation matches `diff(C)` exactly and that it differs from the naive instantaneous sample.

## 5. Numerical solver

Diethelm-Ford-Freed fractional Adams-Bashforth-Moulton predictor-corrector (PECE),
`src/tb_seit/solver.py`. Deterministic, vector-state, finite-value and negative-state checks
(`SolverResult.status`), `N_external(t)` supplied as a callable evaluated at each grid node,
dense-numpy CPU-only implementation (no CUDA assumption). **Verified against two independent
analytic references**, not just internal self-consistency:

- alpha=1.0, `D y = -y`: matches `exp(-t)` to <2e-4 absolute error (h=0.05).
- alpha=0.75, `D^alpha y = -y`: matches the Mittag-Leffler function `E_alpha(-t^alpha)` to
  <7e-5 absolute error (h=0.01).

Both models (fractional, alpha<1, and the integer comparator, alpha=1) share this single code
path, satisfying `docs/MODEL_CONTRACT.md`'s requirement that the two differ only in fractional
order.

## 6. Calibration

**Not executed** (`OPTIMIZATION_CONTRACT_INCOMPLETE`, see Section 1). Fully implemented in
`scripts/run_calibration_multiseed.py` and `src/tb_seit/calibration.py`: bounds
beta∈[0.01,1.00], sigma∈[0.01,0.50], gamma∈[0.05,0.30] (primary), d∈[0.0001,0.05],
alpha∈[0.50,1.00] (primary); DE strategy=best1bin, popsize=15, mutation=(0.5,1.0),
recombination=0.7, tol=0.01, maxiter=1000 (all confirmed against `docs/MODEL_CONTRACT.md` in
`test_de_hyperparameters_match_model_contract` and `test_primary_bounds_match_contract`);
objective = calibration-only RMSE of the flow observation model; initial conditions recomputed
per candidate via `model.initial_conditions` (never free parameters).

## 7. Multi-seed robustness

**Not executed**, same blocker. `scripts/run_calibration_multiseed.py` requires
`--canonical-seed` and `--diagnostic-seeds` (4 values) as mandatory CLI arguments with no
defaults; writes `outputs/calibration/fractional_multiseed.csv` /
`integer_multiseed.csv` with columns `seed, objective, beta, sigma, gamma, d, alpha, success,
iterations, function_evaluations` once seeds are supplied.

## 8. Integer comparator

**Not executed**, same blocker. Implemented to independently re-estimate beta, sigma, gamma, d
under `alpha` fixed at exactly `1.0` (never reusing fractional-model parameters), same
observation equation, calibration interval, initial-condition logic, numerical grid, DE
configuration, and objective. `test_integer_comparator_alpha_is_exactly_one` confirms
`fixed_alpha=1.0` forces `CalibrationRun.alpha == 1.0` exactly (verified with a cheap synthetic
fixture, not the canonical seed).

## 9. Strict 2021-2022 validation

**Not executed**, same blocker (depends on calibration output). Implemented in
`scripts/run_validation.py`: single continuous open-loop simulation 2001-01..2022-12 using
frozen calibration parameters; the last 24 months are compared against observed cases; no
refitting, reinitialization, or use of validation outcomes anywhere in the pipeline.

## 10. Alpha-bound sensitivity

**Not executed**, same blocker. `scripts/run_alpha_sensitivity.py` re-runs calibration+validation
with `alpha` bound at `[0.70, 1.00]` (the manuscript's original bound) using the same canonical
seed and otherwise identical configuration as the primary `[0.50, 1.00]` run, strictly for
comparison.

## 11. Numerical convergence

**Executed** (`outputs/audits/numerical_convergence.csv`). Fixed, arbitrary bounds-midpoint
parameter vector (never a fitted value): beta=0.505, sigma=0.255, gamma=0.175, d=0.02505,
alpha=0.75 (fractional) / alpha=1.0 (integer). Step sizes h∈{1, 1/2, 1/4} months over the full
240-month calibration window, referenced against h=1:

| model | step | max abs diff | relative diff |
|---|---|---|---|
| fractional (alpha=0.75) | 0.5 | 5181.2 | 0.39% |
| fractional (alpha=0.75) | 0.25 | 6732.1 | 0.51% |
| integer (alpha=1.0) | 0.5 | 14173.7 | 0.31% |
| integer (alpha=1.0) | 0.25 | 17828.5 | 0.38% |

All relative differences are well under a 1% threshold. **Primary step h=1 month is frozen**
(also the most CPU-efficient choice for the Mac mini M2 CPU-only target). This determination was
made entirely independently of any fitted parameter or validation outcome.

## 12. Identifiability diagnostics

**Not executed**, same blocker (requires multi-seed calibration results).
`scripts/parameter_robustness_and_kill_test.py` (function `parameter_robustness`) will report
mean/std/min/max/CV per parameter and objective-function spread once seeds are defined. No
undocumented binary `PARAMETER_INSTABILITY` threshold is hardcoded — `docs/MODEL_CONTRACT.md`
does not define one, so the script emits continuous diagnostics only, per explicit task
instruction; classification is left to prose review once real numbers exist.

## 13. Fractional-memory kill test

**Not executed**, same blocker (requires multi-seed calibration and validation results).
`scripts/parameter_robustness_and_kill_test.py` (function `kill_condition_audit`) is implemented
to evaluate all three canonical components (A: parameter stability vs. objective spread; B:
alpha boundary behavior; C: integer comparator vs. fractional model on the 2021-2022 holdout)
exactly as specified in `docs/MODEL_CONTRACT.md` Section 15, with no configuration manipulation
to avoid any outcome. It has not run, so it does not yet classify SURVIVES/WEAKENS/FAILS for any
component — there is no evidence yet to classify.

## 14. Limitations

- Seed contract incompleteness (Section 1) blocks every result downstream of calibration; this
  is a limitation of the governing contract, not of the implementation.
- The worktree was not clean at task start; resolved via a logged prerequisite commit
  (`docs/METHOD_DECISION_LOG.md` D023), not a silent override.
- The `numpy.polyfit`-based log-linear population trend is a simple, defensible but not the only
  possible extrapolation choice; `docs/EXTERNAL_PARAMETER_CONTRACT.md` recommended log-linear
  specifically, so no further judgment call was introduced here.
- The Diethelm-Ford-Freed solver here is a direct O(n²) implementation (no FFT acceleration);
  adequate at the problem's scale (≤264-1056 steps) but would need revisiting before any much
  finer-grained or longer-horizon future use.

## 15. Evidence manifest

See `outputs/EVIDENCE_MANIFEST.csv` for the complete artifact-by-artifact status
(COMPLETE/BLOCKED) with generating script and parameter source for each. 6 artifacts COMPLETE,
13 BLOCKED (all and only the ones depending on an actual DE run).

## 16. Next permitted scientific step

**Resolve implementation blocker**: define the canonical primary seed and the four diagnostic
seeds as an explicit, logged methodological decision (they are not scientific parameters —
any fixed, documented integers satisfy reproducibility; the requirement is that they be chosen
deliberately and recorded, not selected post hoc for a favorable result). Once logged in
`docs/MODEL_CONTRACT.md`/`docs/METHOD_DECISION_LOG.md`, re-run in sequence:
`scripts/run_calibration_multiseed.py` -> `scripts/run_validation.py` ->
`scripts/run_alpha_sensitivity.py` -> `scripts/parameter_robustness_and_kill_test.py`. Only after
those produce real evidence should the identifiability and kill-condition classifications, and
the next-stage choice among "proceed to analytical R0/stability," "investigate identifiability
failure," or "abandon the fractional-memory claim," be made.
