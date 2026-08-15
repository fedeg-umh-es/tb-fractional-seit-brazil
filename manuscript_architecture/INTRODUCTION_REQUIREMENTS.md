# Introduction Requirements

Not drafted. Requirements only, so the Introduction (written last, per the Inside-Out order) is
constrained to exactly the question this study's frozen evidence answers -- no more.

## What the Introduction must establish

1. Tuberculosis remains a public-health burden in Brazil (background fact, requires a citable
   source -- `REQUIRES_LITERATURE_VERIFICATION`).
2. Mechanistic epidemic models, including fractional-order variants, are used to study TB
   transmission (background fact, requires citation --
   `REQUIRES_LITERATURE_VERIFICATION`).
3. A methodological gap in how such models are typically evaluated: improvements are often
   demonstrated only against a simpler/nested variant of the same model family (e.g.
   integer-order vs. fractional-order), without comparison to external, purpose-built or naive
   forecasting baselines. **This specific framing must not be asserted as a documented literature
   gap without a supporting citation search** -- mark as `REQUIRES_LITERATURE_VERIFICATION`
   until checked; it may currently be stated only as the motivating structure of this study's own
   design, not as an established fact about the field.
4. A parallel methodological concern: individual epidemiological rate parameters in such models
   may be poorly identified from a single aggregate incidence series, even when the model fits
   well and derived quantities (like R0) behave robustly -- this is stated as the identifiability
   problem this study investigates, not as a claim about the literature.
5. The precise research question this study answers (see below), stated as three explicit,
   non-conflated sub-questions.
6. The study design in one paragraph: independent reimplementation (original code unavailable),
   fractional/integer SEIT comparison, long-open-loop stress test, 13-origin rolling-origin
   evaluation against persistence/seasonal-naive/SARIMA, identifiability audit, R0/stability
   analysis.

## Precise study questions supported by the frozen design

These three, and only these three, in this order (mirrors Sec 3 of the architecture task and
Sec 1 of `MANUSCRIPT_EVIDENCE_ARCHITECTURE.md`):

1. Does the fractional-order formulation improve upon the corresponding integer-order SEIT
   formulation? (Answered: yes, within-family -- C01.)
2. Does that within-family improvement translate into forecasting skill against external
   forecasting baselines? (Answered: no, against persistence and SARIMA; bounded yes against
   seasonal-naive through h=7 -- C02, C03, C04, C05.)
3. Which mechanistic quantities remain scientifically interpretable given
   parameter-identifiability limitations? (Answered: R0 and predictions are robust; beta, gamma,
   d are not individually interpretable -- C07, C08, C09.)

## Prohibited novelty statements (unless independently verified against the literature later)

- Any claim that this is "the first" study to compare a fractional epidemic model against
  external forecasting baselines.
- Any claim that individual-parameter non-identifiability in fractional TB models is previously
  undocumented in the literature.
- Any claim characterizing the field's typical evaluation practice (e.g. "most fractional-model
  studies only compare against integer-order variants") without a citation-backed literature
  survey.
- Any implied superiority claim about fractional calculus in epidemiology generally (this study
  supports a within-family, dataset-specific finding only, C01).

All of the above, if used, must be tagged `REQUIRES_LITERATURE_VERIFICATION` in the drafting
notes and resolved (cited or removed) before submission. No web/literature search was performed
as part of this architecture task.

## What the Introduction must NOT pre-empt

- It must not state the forecasting result (R2/R3) as a foregone negative, nor imply the paper's
  contribution is primarily a cautionary tale -- the Introduction sets up the question; Results
  and Discussion carry the finding and its interpretation.
- It must not reference the historical manuscript's reported values (R0=1.0963, RMSE/MAE/AIC
  figures, the ~48% optimal-control reduction) as established background -- these are
  REFERENCE_ONLY_NOT_EVIDENCE throughout this project and may only be mentioned, if at all, as
  "a prior report, not independently verified here," never as a benchmark this study replicates
  or improves upon.
