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
| Method specification                    | IN_PROGRESS  |
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
