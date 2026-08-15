# Project identity

External collaboration:
Amaury de Souza / Federico García Crespo

Manuscript:
Fractional-Order SEIT Modeling, Predictive Validation, and Optimal Control of Tuberculosis
Dynamics in Brazil

Target journal mentioned by collaborator:
Biomatemática (UNICAMP)

Submission deadline communicated by collaborator:
30 September 2026 — **COLLABORATOR_REPORTED**, not independently verified.

This project is independent from, and must not be mixed with, any other project (including but
not limited to any internally labelled P1, P2, P3, or P4). No artifacts, methods, results, or
repositories are to be shared across projects.

# Canonical data

Period:
2001-01 to 2022-12

N:
264 monthly observations

Calibration:
2001-01 to 2020-12
N = 240

Validation:
2021-01 to 2022-12
N = 24

# Evidence policy

All current manuscript numerical results are provisional until independently reproduced.

Never preserve a result because it appears in the manuscript.

No observations after December 2022 exist in the supplied canonical dataset.

Never generate synthetic 2023–2027 observations and call them validation data.

## Manuscript-reported results — status NOT_VERIFIED

Parameters:
- alpha = 0.9581
- beta = 0.0112
- sigma = 0.0335
- gamma = 0.0100
- d = 0.0001
- R0 = 1.0963

Integer model fit:
- RMSE = 245.3
- MAE = 198.7
- AIC = 1342

Fractional model fit:
- RMSE = 171.5
- MAE = 132.4
- AIC = 1187

Optimal-control reduction:
- approximately 48%

None of the above may be assumed correct, cited as established, or reused in derived work
without independent reproduction.

# Current stage

INDEPENDENT_REIMPLEMENTATION_SPECIFICATION

EXACT_REPRODUCTION = NOT_POSSIBLE
INDEPENDENT_REIMPLEMENTATION = REQUIRED

Reason: original computational code and complete numerical specification are unavailable.
Amaury de Souza has confirmed no original source code, scripts, or computational configuration
remain. Only the manuscript and the observational dataset are available.

Permitted:
- source preservation
- provenance
- environment setup
- non-destructive dataset integrity inspection
- methodological inventory
- assumption/decision documentation
- methodological specification (this document set)

Not yet permitted:
- model calibration
- parameter estimation
- Differential Evolution execution
- optimal-control simulation
- computing alpha, R0, RMSE, MAE, AIC, stability, sensitivity, or optimal-control results
- manuscript rewriting
- LaTeX preparation
- attempting to reproduce the old numerical values as a target

# Collaborator-confirmed constraints (2026-08-15)

- No original source code remains.
- No scripts remain.
- No original computational configuration remains.
- Only the manuscript and observational dataset are available.
- Definitive observational period: 2001-01 through 2022-12.
- Calibration must use 2001-01 through 2020-12.
- Independent validation must use 2021-01 through 2022-12.
- All analyses affected by the previous incorrect 2001-2027 period (as it appears in the
  manuscript source) must be recalculated.
- Old manuscript values must be retained only if independently regenerated.
- The approximately 48% optimal-control reduction must be discarded if not independently
  supported by regenerated evidence.

# Evidence policy

- All numerical results currently appearing in the manuscript remain NOT_VERIFIED.
- No old numerical result is a target value.
- Old results may be used only for post-hoc comparison after independent computation.
- Implementation choices must be selected for methodological defensibility, not for numerical
  agreement with the manuscript.

# Next scientific gate

Perform a focused methodological review to select and justify the Caputo solver, state
initialization, observational mapping, parameter treatment, and Differential Evolution
configuration (see `docs/ASSUMPTIONS_REGISTER.md`) before writing any model code.

All modeling work proceeds under:
**INDEPENDENT_REIMPLEMENTATION**

not:
EXACT_REPRODUCTION
