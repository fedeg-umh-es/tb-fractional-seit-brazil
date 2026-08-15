# Reproducibility status

Live tracking table. Update statuses as work progresses; never mark an item COMPLETE or
VERIFIED without a corresponding, checkable artifact in this repository.

| Item                                 | Status    |
|---------------------------------------|-----------|
| Dataset integrity                     | PENDING   |
| Original source preservation          | COMPLETE  |
| Original code recovered               | UNKNOWN   |
| Numerical solver specification        | UNKNOWN   |
| Initial conditions                    | UNKNOWN   |
| Differential Evolution configuration  | UNKNOWN   |
| Fractional model reproduction         | NOT_STARTED |
| Integer model reproduction            | NOT_STARTED |
| Predictive validation                 | NOT_STARTED |
| R0                                    | NOT_STARTED |
| Stability                             | NOT_STARTED |
| Sensitivity                           | NOT_STARTED |
| Optimal control                       | NOT_STARTED |
| 48% claim                             | NOT_VERIFIED |
| Manuscript revision                   | BLOCKED   |
| LaTeX conversion                      | BLOCKED   |

## Next gate

Dataset integrity moves to COMPLETE once `scripts/audit_dataset.py` has been run and its output
(`outputs/audits/dataset_integrity.json`) reviewed with no unresolved anomalies.

All modeling-related rows (fractional/integer reproduction onward) are blocked on recovering
Amaury de Souza's original computational code or configuration (see `PROJECT_CANON.md`,
"Next scientific gate"). Absent that, subsequent work must be labelled
INDEPENDENT_REIMPLEMENTATION rather than EXACT_REPRODUCTION.
