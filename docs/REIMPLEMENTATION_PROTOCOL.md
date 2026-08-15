# Independent Reimplementation Protocol

Status: SPECIFICATION (no model code has been written or executed under this protocol).

This document defines the non-negotiable experimental contract governing all future
computational work on this project. It does not itself perform, calibrate, or validate any
model. See `PROJECT_CANON.md` for project-level status and `docs/ASSUMPTIONS_REGISTER.md` for
the itemized list of open methodological decisions this protocol depends on.

REPRODUCTION_MODE = INDEPENDENT_REIMPLEMENTATION
EXACT_REPRODUCTION = IMPOSSIBLE_FROM_AVAILABLE_MATERIAL

Reason: original computational code and complete numerical specification are unavailable.
Amaury de Souza has confirmed that no original source code, scripts, or computational
configuration remain from the work reported in the manuscript. Only the manuscript text and the
observational dataset (`data/raw/tb_mes.xlsx`) are available to this project.

## 1. Data

Observed period:
2001-01 to 2022-12 (N = 264 monthly observations).

Calibration:
2001-01 to 2020-12 (N = 240).

Validation:
2021-01 to 2022-12 only (N = 24).

Validation 2001-01? **NO.** The 2001-01 to 2020-12 observations are calibration data;
the validation window is exclusively 2021-01 through 2022-12.

This is the entire definitive observational period as confirmed by the collaborator. The
manuscript source text describes an incorrect period of "2001 to 2027" and a validation window
of "2021-2027"; no observations exist in the supplied dataset beyond 2022-12, and no synthetic
2023-2027 data may ever be generated or treated as validation data. Every analysis in the
manuscript that depended on the incorrect 2001-2027 / 2021-2027 framing must be recalculated
under the canonical 2001-01 to 2022-12 / 2021-01 to 2022-12 split before its result can be
treated as valid.

No information from 2021-2022 may influence:
- parameter estimation;
- the fractional order alpha;
- solver choice selected from performance;
- parameter bounds selected from performance;
- hyperparameter tuning;
- model selection.

Validation data remain untouched (not inspected, plotted against candidate fits, or used to
tune any choice) until the model structure, calibration procedure, comparator definition, and
validation pipeline itself are frozen under this protocol. See Section 5.

## 2. Scientific models

Primary model:
Fractional-order SEIT model using Caputo derivatives, as structurally specified in the
manuscript (Section 2.3):

```
cD^alpha_t S(t) = Lambda - beta * S(t) I(t) / N(t) - mu S(t)
cD^alpha_t E(t) = beta * S(t) I(t) / N(t) - (sigma + mu) E(t)
cD^alpha_t I(t) = sigma E(t) - (gamma + mu + d) I(t)
cD^alpha_t T(t) = gamma I(t) - mu T(t)
```

Comparator model:
The same SEIT system with alpha = 1 (integer-order), as stated in the manuscript
(Section 3.6): "The integer-order model was obtained by setting the fractional parameter equal
to unity."

The comparator must differ from the primary model only in fractional vs. integer order wherever
mathematically possible (same compartments, same parameter set S/E/I/T, Lambda, beta, sigma,
gamma, mu, d, same initial-condition treatment, same observational mapping, same optimization
procedure and loss). Any other difference between the two models must be recorded as an explicit
decision in `docs/METHOD_DECISION_LOG.md`, not introduced silently.

## 3. Evidence hierarchy

LEVEL A: directly regenerated numerical artifacts (e.g., a parameter vector produced by running
an independently specified and version-controlled optimization procedure against the canonical
calibration data, with the run's configuration and output both committed to the repository).

LEVEL B: analytical results derived from independently regenerated LEVEL A parameters (e.g., R0,
stability classification, sensitivity indices computed from a LEVEL A parameter vector using an
explicit, documented formula).

LEVEL C: interpretive claims based on LEVEL A and/or LEVEL B evidence (e.g., narrative statements
about epidemiological persistence or memory effects).

Historical manuscript values (all numbers currently listed under "Manuscript-reported results —
status NOT_VERIFIED" in `PROJECT_CANON.md`) are:
REFERENCE_ONLY_NOT_EVIDENCE.

They may be displayed alongside independently regenerated results for post-hoc comparison. They
may never be used to select, tune, or validate a method, nor cited as an established finding of
this project.

## 4. Result replacement rule

Every manuscript number must eventually be classified as exactly one of:

- CONFIRMED_BY_REIMPLEMENTATION — independently regenerated under this protocol and found to
  match the manuscript value within a pre-declared, documented tolerance.
- REPLACED_BY_REIMPLEMENTATION — independently regenerated under this protocol and found to
  differ from the manuscript value; the regenerated value supersedes it.
- NOT_REPRODUCIBLE — an independent, methodologically defensible attempt was made and did not
  converge to a stable, defensible result under the canonical data split.
- REMOVED — the claim depended on the incorrect 2001-2027 / 2021-2027 period, or on an
  assumption that cannot be defensibly reconstructed, and is dropped rather than replaced.

No manuscript number may remain classified as NOT_VERIFIED once independent reimplementation
work begins on it; NOT_VERIFIED is a holding state for numbers not yet attempted.

## 5. Validation

Validation data (2021-01 to 2022-12) remain untouched until model structure, calibration
procedure, comparator definition, and the validation pipeline itself are frozen. "Frozen" means:
committed to the repository, described in `docs/METHOD_DECISION_LOG.md`, and not subsequently
altered in response to validation-period performance. Any change made after validation data have
been examined must be treated as a new, separately logged methodological decision, and the
validation run that motivated it must be disclosed alongside the result rather than silently
superseded.

## 6. Optimal control

Optimal control (Section 2.6 of the manuscript: intensified diagnosis, treatment adherence,
contact tracing, and the associated objective functional) must not be implemented until the
uncontrolled SEIT model, parameter estimation procedure, integer-order comparator, and
predictive-validation pipeline have each independently passed their own reproducibility gates
under this protocol (i.e., produced LEVEL A/B evidence and been logged in
`docs/METHOD_DECISION_LOG.md`).

The historical approximately 48% cumulative-case/peak reduction value must not influence control
weights, objective-function parameters, intervention bounds, or any other optimization choice in
the eventual optimal-control work. Per `PROJECT_CANON.md`, this figure must be discarded
entirely if it is not independently supported by regenerated evidence produced under this
protocol.
