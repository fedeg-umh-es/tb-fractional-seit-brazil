# Bulletin of Mathematical Biology — Desk-Reject Simulation Audit

This document records a bounded editorial-risk assessment after Gate 2 closure, manuscript repair, and cover-letter reframing. It is not a prediction of editorial outcome.

---

## Seven-Gate Assessment

| Gate | Status | Current reading |
|---|:---:|---|
| Formal | HOLD | Scientific package is assembled, but final author metadata, declarations, and compiled submission formatting remain incomplete. |
| Policy | HOLD | AI disclosure is documented in Methods; final authorship, funding, competing-interest and ethics-applicability confirmations remain pending. |
| Scope | PLAUSIBLE | Mathematical epidemiology, fractional differential equations, identifiability and forecast evaluation are within BMB's mathematical-biology remit. Scope match alone is not sufficient for acceptance. |
| Contribution threshold | LOW-TO-MODERATE RISK AFTER FRAMING REPAIR | The work does not introduce new fractional theory or a new forecasting algorithm. The cover letter now leads with the field-level methodological question and states the practical implication before the TB case details. |
| Evidence | PASS FOR BOUNDED CLAIM | 13 rolling origins, 12 horizons, independently refitted integer comparator, three external baselines, frozen canonical evidence, and bounded identifiability analysis support the manuscript's stated claims. |
| Problem/framing | PASS AFTER REPAIR | Historical-absence language is removed. Discussion and cover letter frame the contribution as a change in scientific interpretation when the benchmark set expands beyond the model family. |
| Execution/context | PASS WITH HUMAN QA PENDING | Main numerical and methodological boundaries are explicit; final bibliographic, author and production review remains required. |

---

## Principal Desk-Reject Risk

The main remaining editorial risk is **contribution threshold**, not raw scope, missing evidence, or novelty overclaim.

The cover letter now makes the transferable question visible before the application details:

> when a fractional epidemic model reduces error relative to its integer-order counterpart, does that within-family improvement constitute evidence of forecasting skill against external references under genuine temporal out-of-sample evaluation?

The manuscript's bounded methodological implication is also explicit in the Discussion: within-family error reduction is not sufficient, by itself, to establish predictive utility; forecasting claims should be tested against appropriate external baselines under an explicit temporal out-of-sample protocol.

The cover letter additionally anchors journal fit in two relevant BMB precedents: Angstmann, Henry, and McGann (2016) on principled versus ad hoc fractional epidemiological modeling, and Simpson & Maclaren (2024) on prediction with poorly identified mathematical models. This is used as evidence of editorial continuity, not as a novelty claim.

---

## Current Risk Classification

```text
DESK_REJECT_RISK = LOW_TO_MODERATE
PRIMARY_RISK_GATE = CONTRIBUTION_THRESHOLD
SCOPE_RISK = LOW_TO_MODERATE
EVIDENCE_RISK_FOR_CURRENT_CLAIMS = LOW
NOVELTY_OVERCLAIM_RISK_AFTER_GATE_2_REPAIR = LOW
PROBLEM_FRAMING_RISK_AFTER_COVER_LETTER_REPAIR = LOW
FORMAL_POLICY_RISK_BEFORE_METADATA_COMPLETION = ACTIVE
NEW_EXPERIMENT_REQUIRED = NO
```

This classification remains a qualitative editorial-risk assessment. It does not imply that a cover letter can eliminate desk-reject risk or guarantee external review.
