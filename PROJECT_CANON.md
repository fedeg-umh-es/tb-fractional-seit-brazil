# Project Canon — TB Fractional SEIT Brazil

Last operational update: 2026-09-24

## Project identity

External collaboration:
Amaury de Souza / Federico García Crespo

Repository:
`tb-fractional-seit-brazil`

Scientific owner and decision-maker:
fedeg

Working manuscript:
Fractional-order SEIT modelling and methodological evaluation of tuberculosis dynamics in Brazil

Primary editorial target:
**Bulletin of Mathematical Biology**

Editorial route:
Hybrid/subscription route required; avoid mandatory-APC venues.

This project is independent from, and must not be mixed with, the separate asthma manuscript or
with any other research project. No results, claims, artifacts, or project state may be silently
transferred across projects.

---

## Dominant scientific question

> Does improvement of a fractional-order mechanistic epidemic model over its independently
> refitted integer-order counterpart translate into forecasting skill beyond the model family?

This is the dominant question. Practical parameter identifiability is a secondary interpretive
axis, not the novelty claim.

---

## Canonical data and evaluation frame

Observational period:
2001-01 to 2022-12

N:
264 monthly observations

Original calibration / validation split:
- calibration: 2001-01 to 2020-12 (N = 240)
- validation: 2021-01 to 2022-12 (N = 24)

Primary forecasting evaluation:
- expanding-window rolling origin
- 13 origins
- forecast horizons h = 1..12 months
- fractional SEIT and independently refitted integer-order SEIT
- external baselines: persistence, seasonal naive (12 months), SARIMA

All availability and train-only constraints remain binding.

---

## Frozen scientific anchor

The current evidence supports the following bounded conclusions:

1. The fractional SEIT model improves over the independently refitted integer-order SEIT
   comparator within the model family.
2. The fractional model has no positive observed RMSE/MAE skill relative to persistence at any
   evaluated horizon h = 1..12.
3. The fractional model has no positive observed RMSE/MAE skill relative to SARIMA at any
   evaluated horizon h = 1..12.
4. Positive observed skill relative to the seasonal-naive baseline is limited to h = 1..7 and
   becomes negative at h = 8..12.
5. beta, gamma, and d are weakly identifiable individually under the current calibration problem.
6. Observable predictions are comparatively stable across near-equivalent parameter solutions.
7. The practical-identifiability envelope for the derived R0 diagnostic functional in the
   <=1% calibration-RMSE band is 1.1542-1.1892.

These are empirical findings for this dataset, model, and evaluation protocol. They are not
universal claims about fractional epidemic models.

Canonical numerical results remain frozen under
`results_canonical/RESULT_SET_FREEZE.md`.

---

## Novelty and claim discipline

Gate 2 external verification is closed.

```text
GATE_2_EXTERNAL_VERIFICATION = CLOSED
PORTFOLIO_DECISION = ABSORB
NEW_EXPERIMENT_REQUIRED = NO
FIRST_STUDY_CLAIM = PROHIBITED
UNIVERSAL_ABSENCE_CLAIM = PROHIBITED
```

The novelty is not an exact-combination or historical-priority claim.

The defensible contribution is the scientific friction exposed when the benchmark set is
expanded beyond the fractional/integer model family under a common temporal multi-horizon
forecasting protocol: a favorable within-family result does not imply external forecasting
skill.

Do not claim:
- generic fractional superiority;
- biological memory inferred from alpha < 1;
- precise estimation of beta, gamma, or d;
- universal forecasting skill;
- "first study", "never evaluated", "unprecedented", or equivalent priority language;
- theoretical novelty not supported by the work.

Practical identifiability remains a secondary interpretive axis.

---

## Current operational state

```text
PAPER = TUBERCULOSIS_BRAZIL_FRACTIONAL_SEIT
SCIENCE = FROZEN
PROVENANCE_AUDIT = CLOSED
NOVELTY_GATE_2 = CLOSED
MANUSCRIPT = CONSOLIDATION_PRODUCTION
TARGET = BULLETIN_OF_MATHEMATICAL_BIOLOGY
AMAURY_REVIEW = DEFERRED_UNTIL_RETURN
WORK_CONTINUES_DURING_ABSENCE = YES
NEW_EXPERIMENTS = NO
READY_FOR_SUBMISSION = NO
```

Amaury has asked that work continue while he is away, with final manuscript review after his
return. His absence is therefore not a project-wide freeze.

---

## Permitted work before Amaury's final review

The active front is editorial production and quality assurance:

- internal consistency of the manuscript;
- traceability of numerical statements to frozen evidence;
- reference verification and bibliography cleanup;
- figure/table consistency and packaging;
- declarations and submission metadata preparation;
- provisional CRediT preparation;
- Bulletin of Mathematical Biology formatting and submission-package preparation;
- PDF / manuscript QA;
- cover-letter consolidation;
- correction of documentary or reproducibility defects that do not reopen scientific results.

This work must preserve the frozen evidence and dominant question.

---

## Locked unless a genuine scientific blocker is demonstrated

Do not reopen experiments or recalculate canonical results for narrative, cosmetic, or favorable
result-seeking reasons.

Scientific work may be reopened only under the documented reopening policy, including a genuine
numerical inconsistency, reproducibility failure, evidence required for a central claim, an
explicitly authorized future inferential analysis, or an explicit author decision to change the
scientific question.

In particular, do not add experiments merely to improve the editorial story.

---

## Human gate reserved for Amaury / authors

The following remain pending final human closure:

- final scientific review of the complete manuscript;
- final wording of any provenance limitation requiring coauthor confirmation;
- definitive CRediT/contribution statements;
- final author list, order, and affiliations;
- funding, ethics, competing-interest, and corresponding-author metadata where human confirmation
  is required;
- authorization to submit.

AI tools are execution and review assistants, not authors or scientific decision-makers.

---

## Continuation rule

Resume from **manuscript consolidation / production**.

Do not return to model development, novelty hunting, or new experiments unless a documented
scientific blocker activates the reopening policy.

The next operational objective is to leave the Bulletin of Mathematical Biology submission
package essentially complete, with only the final human gate reserved for Amaury and the authors.
