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
| Optimization contract (DE hyperparameters) | PARTIAL — seeds undefined |
| Fractional model calibration            | BLOCKED — OPTIMIZATION_CONTRACT_INCOMPLETE |
| Integer model calibration               | BLOCKED — OPTIMIZATION_CONTRACT_INCOMPLETE |
| Multi-seed robustness diagnostics       | BLOCKED — OPTIMIZATION_CONTRACT_INCOMPLETE |
| Alpha-bound sensitivity                 | BLOCKED — OPTIMIZATION_CONTRACT_INCOMPLETE |
| Fractional model reproduction           | NOT_STARTED  |
| Integer model reproduction              | NOT_STARTED  |
| Predictive validation                   | NOT_STARTED  |
| R0                                      | NOT_STARTED  |
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

See `BASE_MODEL_REIMPLEMENTATION_REPORT.md` for the full account. Summary: the base-model
codebase (`src/tb_seit/`), canonical data split, leakage-safe population exogenous series,
fixed demographic constants, the Diethelm-Ford-Freed fractional solver, the flow-based
observation model, and the numerical convergence check are all implemented, executed, and
tested (`tests/test_seit_model.py`, `tests/test_optimization_contract.py`). Calibration,
multi-seed robustness, validation, alpha-bound sensitivity, and the kill-condition audit are
implemented as code but **not executed**: `docs/MODEL_CONTRACT.md` documents the Differential
Evolution hyperparameter policy but never fixes literal seed values (one canonical + four
diagnostic), and this implementation stage's own instructions require stopping rather than
inventing them (`OPTIMIZATION_CONTRACT_INCOMPLETE`). No AIC, R0, stability, sensitivity-index,
or optimal-control work was attempted, per scope.
