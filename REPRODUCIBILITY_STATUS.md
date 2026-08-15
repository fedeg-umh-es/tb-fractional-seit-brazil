# Reproducibility status

Live tracking table. Update statuses as work progresses; never mark an item COMPLETE or
VERIFIED without a corresponding, checkable artifact in this repository.

| Item                                   | Status       |
|-----------------------------------------|--------------|
| Dataset integrity                       | VERIFIED     |
| Original source preservation            | COMPLETE     |
| Original code recovered                 | NO           |
| Exact reproduction                      | NOT_POSSIBLE |
| Independent reimplementation            | REQUIRED     |
| Method specification                    | COMPLETE (base-model scope only) |
| Base-model implementation (code)        | COMPLETE    |
| Numerical solver verification           | VERIFIED    |
| Numerical convergence (h selection)     | VERIFIED    |
| Population exogenous series (leakage-safe) | COMPLETE |
| Model constants (mu, Lambda)            | COMPLETE    |
| Optimization contract (DE hyperparameters + seeds) | COMPLETE — seeds frozen D024 |
| Fractional model calibration (primary seed 20260815) | COMPLETE  |
| Integer model calibration (primary seed 20260815) | COMPLETE  |
| Multi-seed robustness diagnostics       | COMPLETE — see identifiability caveat below |
| Alpha-bound sensitivity ([0.70,1.00] vs [0.50,1.00]) | COMPLETE — alpha materially unchanged |
| Strict 2021-2022 validation             | COMPLETE — fractional RMSE 1117.96 < integer RMSE 1759.54 |
| Individual-parameter identifiability (beta, gamma, d) | WEAKENS — CV 58-82% across seeds despite stable objective (CV 0.35%); see BASE_MODEL_REIMPLEMENTATION_REPORT.md Sec 12 |
| Fractional model reproduction           | NOT_STARTED (exact reproduction of manuscript values is NOT_POSSIBLE; independent values above are the reimplementation result) |
| Integer model reproduction              | NOT_STARTED (same) |
| Predictive validation                   | COMPLETE (see strict validation row above) |
| R0                                      | NOT_STARTED — see next-gate note (identifiability caveat applies) |
| Stability                               | NOT_STARTED  |
| Sensitivity                             | NOT_STARTED  |
| Optimal control                         | NOT_STARTED  |
| 48% claim                               | NOT_VERIFIED |
| Manuscript revision                     | BLOCKED      |
| LaTeX conversion                        | BLOCKED      |

## Dataset integrity evidence

Confirmed by `scripts/audit_dataset.py` -> `outputs/audits/dataset_integrity.json`:
TOTAL_MONTHS = 264, CALIBRATION_MONTHS = 240, VALIDATION_MONTHS = 24, DUPLICATE_DATES = 0,
MISSING_MONTHS = 0, MISSING_VALUES = 0. Re-run on 2026-08-15 against canonical commit 419f1ca;
output unchanged (`git diff` empty). No missing observations exist in the canonical dataset;
this status must not be described otherwise absent a new reproducible audit that disagrees.

## Next gate

Original computational code/configuration has been confirmed unavailable by the collaborator
(Amaury de Souza). Exact reproduction of the manuscript's numerical results is therefore not
possible. All modeling-related rows (fractional/integer reproduction onward) proceed only under
INDEPENDENT_REIMPLEMENTATION, governed by `docs/REIMPLEMENTATION_PROTOCOL.md`, and are blocked
until the outstanding methodological assumptions in `docs/ASSUMPTIONS_REGISTER.md` are resolved
(status PENDING_METHOD_SELECTION or UNKNOWN) via independent, documented, and auditable
methodological choices — never by reverse-engineering the manuscript's reported values.

## Base-model implementation stage (2026-08-15)

See `BASE_MODEL_REIMPLEMENTATION_REPORT.md` for the full account. The base-model codebase
(`src/tb_seit/`), canonical data split, leakage-safe population exogenous series, fixed
demographic constants, the Diethelm-Ford-Freed fractional solver, the flow-based observation
model, and the numerical convergence check were implemented and tested first
(`tests/test_seit_model.py`, `tests/test_optimization_contract.py`), while calibration was
blocked on an undefined seed contract (`OPTIMIZATION_CONTRACT_INCOMPLETE`).

## Base-model evidence pipeline execution (2026-08-15, continuation)

The seed contract was frozen (`docs/METHOD_DECISION_LOG.md` D024: `PRIMARY_SEED=20260815`,
`DIAGNOSTIC_SEEDS=[20260816..20260819]`) before any DE result existed under it, resolving the
blocker. The full pipeline was then executed: 5-seed x 2-model calibration, primary-seed
integer comparator (independently re-estimated, never reusing fractional parameters), strict
open-loop 2021-2022 validation, alpha-bound sensitivity ([0.70,1.00] vs. primary [0.50,1.00]),
multi-seed identifiability diagnostics, and the fractional-memory kill-condition audit. All 48
tests pass (`tests/test_seed_contract.py` added). Overall verdict:
`BASE_MODEL_REIMPLEMENTATION_VALID_WITH_LIMITATIONS` -- valid, reproducible pipeline; material
limitation is weak individual identifiability of beta/gamma/d (see table above and
`BASE_MODEL_REIMPLEMENTATION_REPORT.md` Sec 12-13). No AIC, R0, stability, sensitivity-index, or
optimal-control work was attempted, per scope; R0/stability work, when it begins, must carry the
identifiability caveat forward rather than treat the primary-seed beta/gamma point estimates as
precise.
