# Reproducibility status

Live tracking table. Update statuses as work progresses; never mark an item COMPLETE or
VERIFIED without a corresponding, checkable artifact in this repository.

| Item                                   | Status       |
|-----------------------------------------|--------------|
| Dataset integrity                       | VERIFIED     |
| Original source preservation            | COMPLETE     |
| Original code recovered                 | NO           |
| Exact reproduction                      | NOT_POSSIBLE |
| Independent reimplementation            | COMPLETE_WITH_DOCUMENTED_LIMITATIONS |
| Method specification                    | COMPLETE     |
| Base-model implementation (code)        | COMPLETE     |
| Numerical solver verification           | VERIFIED     |
| Numerical convergence (h selection)     | VERIFIED     |
| Population exogenous series (leakage-safe) | COMPLETE |
| Model constants (mu, Lambda)            | COMPLETE     |
| Optimization contract (DE hyperparameters + seeds) | COMPLETE — seeds frozen D024 |
| Fractional model calibration (primary seed 20260815) | COMPLETE  |
| Integer model calibration (primary seed 20260815) | COMPLETE  |
| Multi-seed robustness diagnostics       | COMPLETE — weak individual identifiability documented |
| Alpha-bound sensitivity ([0.70,1.00] vs [0.50,1.00]) | COMPLETE — alpha materially unchanged |
| Strict 2021-2022 validation             | COMPLETE — fractional RMSE 1117.96 < integer RMSE 1759.54 |
| Individual-parameter identifiability (beta, gamma, d) | WEAK — CV 58-82% across seeds despite stable objective |
| Fractional model reproduction           | NOT_APPLICABLE — original numerical reproduction impossible; independent reimplementation is canonical |
| Integer model reproduction              | NOT_APPLICABLE — original numerical reproduction impossible; independent refit is canonical comparator |
| Predictive validation                   | COMPLETE — single-origin and rolling-origin evidence frozen |
| Practical-identifiability analysis      | COMPLETE — profile-objective + multiseed evidence |
| R0                                      | COMPLETE_WITH_SCOPE_BOUNDARY — admissible-set envelope 1.1542-1.1892 (n=25), not a confidence interval |
| Stability                               | COMPLETE_WITH_SCOPE_BOUNDARY — 25/25 admissible solutions unstable under Matignon criterion |
| Rolling-origin external benchmarking    | COMPLETE — persistence, seasonal naive, SARIMA; h=1..12 |
| Additional sensitivity analysis         | DEFERRED_NOT_REQUIRED_FOR_FROZEN_CLAIMS |
| Optimal control                         | DEFERRED_OUTSIDE_CURRENT_PAPER |
| Historical 48% claim                    | NOT_VERIFIED_AND_NOT_USED |
| Canonical result set                    | FROZEN_WITH_DOCUMENTED_LIMITATIONS |
| Manuscript revision                     | IN_PROGRESS — controlled pre-submission repair only |
| BMB production / LaTeX                  | BLOCKED_UNTIL_MANUSCRIPT_AND_HUMAN_METADATA_GATES_PASS |

## Current gate (2026-09-05)

The scientific evidence and result set are frozen. The project is now in controlled pre-submission repair. No new experiment is authorized merely to improve narrative strength, journal fit, or cosmetic completeness. Reopening is restricted to the conditions recorded in `results_canonical/RESULT_SET_FREEZE.md`.

The active work is limited to documentary truth, manuscript structure, claim precision, prose, BMB packaging, and final human-author metadata/review.

## Dataset integrity evidence

Confirmed by `scripts/audit_dataset.py` -> `outputs/audits/dataset_integrity.json`:
TOTAL_MONTHS = 264, CALIBRATION_MONTHS = 240, VALIDATION_MONTHS = 24, DUPLICATE_DATES = 0,
MISSING_MONTHS = 0, MISSING_VALUES = 0. Re-run on 2026-08-15 against canonical commit 419f1ca;
output unchanged (`git diff` empty). No missing observations exist in the canonical dataset;
this status must not be described otherwise absent a new reproducible audit that disagrees.

The canonical observational file used by the pipeline is `data/raw/tb_mes.xlsx`. Its SHA-256 and acquisition record are documented in `DATA_PROVENANCE.md`. The repository does not independently record the original governmental download URL or acquisition path, so no specific external provenance route should be represented as repository-verified unless later documented by the authors.

## Historical progression and evidence record

Original computational code/configuration was confirmed unavailable by the collaborator
(Amaury de Souza). Exact reproduction of the manuscript's numerical results was therefore not
possible. Modeling proceeded under INDEPENDENT_REIMPLEMENTATION governed by
`docs/REIMPLEMENTATION_PROTOCOL.md`, using independently documented methodological choices rather than reverse-engineering reported values.

### Base-model implementation and evidence pipeline (2026-08-15)

See `BASE_MODEL_REIMPLEMENTATION_REPORT.md` for the full account. The base-model codebase
(`src/tb_seit/`), canonical data split, leakage-safe population exogenous series, fixed
demographic constants, the Diethelm-Ford-Freed fractional solver, the flow-based observation
model, and the numerical convergence check were implemented and tested. The optimization seed
contract was frozen in `docs/METHOD_DECISION_LOG.md` D024 before execution of the final evidence pipeline.

The pipeline then executed 5-seed x 2-model calibration, the independently re-estimated integer comparator, strict open-loop 2021-2022 validation, alpha-bound sensitivity, multiseed identifiability diagnostics, and the fractional-memory kill-condition audit. Overall verdict:
`BASE_MODEL_REIMPLEMENTATION_VALID_WITH_LIMITATIONS`. The material limitation is weak individual identifiability of beta/gamma/d; this limitation is retained explicitly in the manuscript interpretation.

### Practical-identifiability audit

See `IDENTIFIABILITY_AUDIT_REPORT.md`. The audit separates parameter, predictive, and R0-functional practical identifiability using the 5-seed ensemble and profile-objective analysis. Findings: beta/gamma/d are weakly identifiable; predictions are comparatively stable; alpha is tightly constrained in the implemented profile-objective analysis. The analysis is practical/numerical identifiability, not a structural-identifiability proof and not a formal profile-likelihood analysis.

### R0 and stability

See `R0_STABILITY_ANALYSIS_NOTE.md`, `docs/FRACTIONAL_DIMENSIONAL_CONSISTENCY.md`, and `docs/METHOD_DECISION_LOG.md` D027-D028. An initial dimensional-consistency conflict was explicitly stopped and subsequently resolved by the documented common reference-time scaling (`tau0=1 month`), without recalibration and without changing trajectories, R0, or the stability classification.

The full 33-solution diagnostic pool contains poor-fit probes and is not uniformly above R0=1. The manuscript-relevant `NEAR_EQUIVALENT_ADMISSIBLE_SET` is defined by calibration RMSE degradation <=1% (n=25). Across this admissible set, the practical-identifiability R0 envelope is 1.1542-1.1892 and 25/25 solutions are classified unstable under the commensurate Matignon criterion. The R0 envelope is not a confidence interval.

### Rolling-origin forecasting evaluation

See `FORECASTING_EVALUATION_REPORT.md` and `docs/METHOD_DECISION_LOG.md` D029. The leakage-audited expanding-window rolling-origin evaluation uses 13 origins, horizons h=1..12, and three external baselines: persistence, seasonal naive lag 12, and SARIMA with order fixed from the initial calibration period and coefficients re-estimated at each origin.

Observed fractional-model errors are lower than the independently refitted integer comparator at every evaluated horizon. Observed skill is negative versus persistence and SARIMA at h=1..12, and positive versus seasonal naive only through h=7. These comparisons are descriptive; post-hoc significance testing was not added because an inferential dependence protocol had not been pre-specified.

### Canonical evidence freeze

See `results_canonical/EVIDENCE_FREEZE_REPORT.md`, `results_canonical/RESULT_SET_FREEZE.md`, and
`docs/METHOD_DECISION_LOG.md` D030. `RESULT_SET_STATUS = FROZEN_WITH_DOCUMENTED_LIMITATIONS`.
Canonical tables, figures, and the claim-support audit were built deterministically from the frozen artifacts and reconciled before manuscript architecture work. Reopening remains restricted by the explicit policy in `results_canonical/RESULT_SET_FREEZE.md`.

## Current operational rule

```text
SCIENCE = FROZEN
NEW_EXPERIMENTS = NO_UNLESS_GENUINE_BLOCKER
DOCUMENTARY_REPAIR = ACTIVE
MANUSCRIPT_STRUCTURAL_REPAIR = ACTIVE
BMB_PRODUCTION = PENDING
READY_FOR_SUBMISSION = NO
```
