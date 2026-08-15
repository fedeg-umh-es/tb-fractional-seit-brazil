# Method decision log

Chronological, append-only record of methodological decisions governing this project. Every
decision that affects data handling, model structure, parameter treatment, or evidence status
must be logged here at the time it is made, with a reason. Do not edit or delete prior entries;
append corrections as new entries that reference the one they supersede.

---

## D001

Date: 2026-08-15

Decision:
Observational period fixed at 2001-01 through 2022-12 (N = 264 monthly observations).

Reason:
Only supplied observational data are available through December 2022. The manuscript source
text describes an incorrect period ("2001 to 2027"); no data exist beyond 2022-12 in the
supplied dataset, and none may be fabricated.

---

## D002

Date: 2026-08-15

Decision:
Calibration set to 2001-01 through 2020-12 (N = 240); independent validation set to 2021-01
through 2022-12 (N = 24).

Reason:
Collaborator-approved (Amaury de Souza) strict temporal split, superseding the manuscript's
stated "2021-2027" validation window, which cannot exist given the true observational period.

---

## D003

Date: 2026-08-15

Decision:
Exact reproduction of the manuscript's numerical results is abandoned as a project goal.

Reason:
Original source code, scripts, and computational configuration are unavailable, as confirmed
by the collaborator. Exact reproduction is not possible from the available material.

---

## D004

Date: 2026-08-15

Decision:
Proceed as an independent reimplementation (REPRODUCTION_MODE = INDEPENDENT_REIMPLEMENTATION).

Reason:
Scientific results must be regenerated from explicit, auditable methodological choices rather
than assumed equivalent to the original (unrecoverable) computational pipeline.

---

## D005

Date: 2026-08-15

Decision:
Old manuscript numbers are not optimization targets, tuning references, or model-selection
criteria at any stage of independent reimplementation.

Reason:
Avoid reverse-engineering methodological assumptions (bounds, solver choice, initial conditions,
control weights, etc.) in order to reproduce expected values. Doing so would defeat the purpose
of an independent reimplementation and manufacture false confidence in the original result.

---

## D006

Date: 2026-08-15

Decision:
Manuscript revision and LaTeX conversion remain BLOCKED until evidence is frozen.

Reason:
No manuscript number can be reported as CONFIRMED_BY_REIMPLEMENTATION, REPLACED_BY_REIMPLEMENTATION,
NOT_REPRODUCIBLE, or REMOVED (see `docs/REIMPLEMENTATION_PROTOCOL.md`, Section 4) until it has
actually been independently regenerated or explicitly abandoned. Editing manuscript prose or
LaTeX before that point risks encoding NOT_VERIFIED values as if they were established.

---

## D007

Date: 2026-08-15

Decision:
Repository transitioned from stage REPOSITORY_INITIALIZATION to
INDEPENDENT_REIMPLEMENTATION_SPECIFICATION. `docs/REIMPLEMENTATION_PROTOCOL.md` and
`docs/ASSUMPTIONS_REGISTER.md` created; `PROJECT_CANON.md` and `REPRODUCIBILITY_STATUS.md`
updated accordingly. No model calibration, parameter estimation, Differential Evolution run, or
computation of alpha, R0, RMSE, MAE, AIC, stability, sensitivity, or optimal-control results was
performed as part of this transition; this entry documents a methodological-specification stage
change only.

Reason:
Formalizes the collaborator-confirmed constraints (no original code/scripts/configuration
recoverable; canonical 2001-01/2022-12 period; 2001-01/2020-12 calibration; 2021-01/2022-12
independent validation) into the repository's canonical documents before any numerical work
begins, per task scope.
