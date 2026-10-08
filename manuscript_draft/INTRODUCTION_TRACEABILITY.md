# Introduction Traceability and Audit

This document provides complete paragraph-by-paragraph audit traceability for `manuscript_draft/INTRODUCTION_DRAFT.md`, mapping rhetorical roles, study facts, verified literature citations, and guardrails directly to the approved manuscript architecture in `manuscript_architecture/INTRODUCTION_REQUIREMENTS.md` and `manuscript_architecture/MANUSCRIPT_EVIDENCE_ARCHITECTURE.md`.

---

## Global Introduction Audit Checklist

```text
INTRODUCTION_FUNNEL_COHERENT = YES
DOMINANT_QUESTION_PRESERVED = YES
MECHANISTIC_AXIS_SUBORDINATE = YES
RESULTS_PREEMPTED = NO
ALL_LITERATURE_MARKERS_RESOLVED = YES
UNVERIFIED_GAP_ASSERTED_AS_FACT = NO
NOVELTY_CLAIM_INVENTED = NO
LITERATURE_REFERENCE_INVENTED = NO
FORECASTING_SUPERIORITY_PROMISED = NO
PARAMETER_PRECISION_PROMISED = NO
R0_POPULATION_INFERENCE_PROMISED = NO
```

---

## Resolved Literature Verification Markers

1. `[LITERATURE VERIFICATION REQUIRED: tuberculosis epidemiology and surveillance in Brazil]`
   * **STATUS**: RESOLVED
   * **SOURCES**: REF-01 (World Health Organization, 2022), REF-02 (Rocha et al., 2020)
   * **CITATION_INSERTED**: `(World Health Organization, 2022; Rocha et al., 2020)`
   * **CLAIM_SUPPORTED**: Tuberculosis is a persistent public health challenge in Brazil, monitored via standardized national surveillance notifications.
   * **WORDING_CHANGED**: NO
   * **NOVELTY_IMPLICATION**: NONE

2. `[LITERATURE VERIFICATION REQUIRED: external-baseline evaluation of mechanistic epidemic forecasting models]`
   * **STATUS**: RESOLVED
   * **SOURCES**: REF-03 (Moran et al., 2016). Bracher et al. (2021) was removed on 2026-10-08: it concerns the weighted interval score for probabilistic forecasts and does not address this claim.
   * **CITATION_INSERTED**: `(Moran et al., 2016)`
   * **CLAIM_SUPPORTED**: Cited claim (Moran et al., 2016, abstract level): epidemic forecasting must contend with incomplete and inaccurate data and with changes in human behavior. The statement that a close fit does not ensure reliable forecasts under strict temporal evaluation is the authors' own framing and carries no citation.
   * **WORDING_CHANGED**: NO
   * **NOVELTY_IMPLICATION**: NONE

3. `[LITERATURE VERIFICATION REQUIRED: fractional-order compartmental models in infectious-disease modelling]`
   * **STATUS**: RESOLVED
   * **SOURCES**: REF-06 (Diethelm, 2013), REF-07 (Area et al., 2015)
   * **CITATION_INSERTED**: `(Diethelm, 2013; Area et al., 2015)`
   * **CLAIM_SUPPORTED**: Fractional-order derivatives replace integer rates with non-local operators that introduce power-law temporal dependence in compartmental epidemic models.
   * **WORDING_CHANGED**: NO
   * **NOVELTY_IMPLICATION**: NONE

4. `[LITERATURE VERIFICATION REQUIRED: parameter and functional identifiability in epidemiological compartmental models]`
   * **STATUS**: RESOLVED
   * **SOURCES**: REF-08 (Tuncer & Le, 2018), REF-09 (Roosa & Chowell, 2019). Meshkat et al. (2014) was removed from this sentence on 2026-10-08 because it addresses structural identifiability.
   * **CITATION_INSERTED**: `(Tuncer & Le, 2018; Roosa & Chowell, 2019)`
   * **CLAIM_SUPPORTED**: Fitting compartmental models to aggregate notifications frequently leads to practical non-identifiability, where disparate parameter combinations yield near-equivalent fits, while specific composite parameter combinations can remain identifiable.
   * **WORDING_CHANGED**: NO
   * **TERMINOLOGY_BOUNDARY**: Aligned with standard literature terms ("identifiable parameter combinations" and "practical robustness of derived quantities").
   * **NOVELTY_IMPLICATION**: NONE


5. `[GATE 2: neighboring evaluation designs and direct-precedent check]`
   * **STATUS**: RESOLVED
   * **SOURCES**: Chishtie et al. (2026), Alzahrani et al. (2024), Kalizhanova et al. (2024)
   * **CLAIM_SUPPORTED**: Neighboring studies report a fractional-versus-integer comparison on Canadian COVID-19 data with, separately, rolling-origin validation (Chishtie et al., 2026; abstract only, full text not read); a fractional SEIR model fitting influenza data better than ARIMA, as a comparison of fit rather than held-out forecasts (Alzahrani et al., 2024); and SARIMA outperforming a basic SIR model on tuberculosis data with different training and evaluation windows and a single partition (Kalizhanova et al., 2024). These precedents support framing the paper around the inferential change produced by benchmark expansion rather than around a universal absence claim.
   * **NOVELTY_IMPLICATION**: No `first`, `never evaluated`, or universal-absence claim is permitted.

---

## Paragraph-by-Paragraph Traceability Matrix

### I1 — Scientific stakes and compartmental epidemic models (Paragraph 1)

* **PARAGRAPH_ID**: I1
* **RHETORICAL_ROLE**: Funnel top: establish the mathematical-epidemiology context, the Brazilian TB application, and the distinction between historical fit and forward forecasting.
* **STUDY_FACTS_USED**: Brazilian national monthly TB surveillance context (2001–2022).
* **GENERAL_SCIENTIFIC_CLAIMS**: Compartmental models represent transmission and latent dynamics; TB remains a public-health challenge in Brazil; calibration fit does not guarantee forward forecast accuracy.
* **VERIFIED_CITATIONS**: (World Health Organization, 2022; Rocha et al., 2020), (Moran et al., 2016).
* **STUDY_QUESTION_SUPPORTED**: Motivates Q1 and Q2.
* **PROMISE_TO_RESULTS**: Rigorous out-of-sample evaluation separating fit from forward predictive performance.
* **OVERCLAIM_RISK**: None.
* **NOVELTY_RISK**: None.

---

### I2 — Fractional-order extension and within-family evidence (Paragraph 2)

* **PARAGRAPH_ID**: I2
* **RHETORICAL_ROLE**: Introduce fractional-order flexibility and establish that fractional-versus-integer improvement is still a within-family comparison.
* **STUDY_FACTS_USED**: Fractional and integer SEIT formulations belong to the same mechanistic family.
* **GENERAL_SCIENTIFIC_CLAIMS**: Fractional operators introduce non-local temporal dependence; lower within-family error does not by itself establish forecasting value beyond that family.
* **VERIFIED_CITATIONS**: (Diethelm, 2013; Area et al., 2015).
* **STUDY_QUESTION_SUPPORTED**: Sets up Q1 and creates the need for Q2.
* **PROMISE_TO_RESULTS**: Separate within-family comparison from external predictive utility.
* **OVERCLAIM_RISK**: None.
* **NOVELTY_RISK**: No generic fractional superiority claim.

---

### I3 — Central evaluation friction and neighboring precedents (Paragraph 3)

* **PARAGRAPH_ID**: I3
* **RHETORICAL_ROLE**: State the dominant forecasting question and show that the scientific issue is benchmark expansion, not an asserted absence of prior comparisons.
* **STUDY_FACTS_USED**: External benchmarking against independently re-estimated integer SEIT plus forecasting baselines across lead horizons.
* **GENERAL_SCIENTIFIC_CLAIMS**: A model can improve within-family while remaining uncompetitive against purpose-built predictive baselines.
* **VERIFIED_CITATIONS**: Chishtie et al. (2026), Alzahrani et al. (2024), Kalizhanova et al. (2024).
* **STUDY_QUESTION_SUPPORTED**: Q2 is stated as the paper-level dominant question while preserving Q1 as its prerequisite comparison.
* **PROMISE_TO_RESULTS**: Test whether the within-family conclusion survives benchmark expansion under temporal out-of-sample assessment.
* **OVERCLAIM_RISK**: Controlled.
* **NOVELTY_RISK**: `FIRST_STUDY_CLAIM` and universal-absence wording remain prohibited.

---

### I4 — Practical identifiability as a secondary interpretive axis (Paragraph 4)

* **PARAGRAPH_ID**: I4
* **RHETORICAL_ROLE**: Introduce the secondary mechanistic-interpretation problem without competing with the forecasting spine.
* **STUDY_FACTS_USED**: Calibration from aggregate monthly incidence and evaluation of parameter, predictive, and derived-functional stability.
* **GENERAL_SCIENTIFIC_CLAIMS**: Near-equivalent fits can coexist with substantial individual-parameter dispersion.
* **VERIFIED_CITATIONS**: (Tuncer & Le, 2018; Roosa & Chowell, 2019).
* **STUDY_QUESTION_SUPPORTED**: Q3.
* **PROMISE_TO_RESULTS**: Bound which mechanistic quantities remain interpretable under practical non-identifiability.
* **OVERCLAIM_RISK**: None.
* **NOVELTY_RISK**: Identifiability remains a secondary interpretive axis, not the novelty claim.

---

### I5 — Study response and explicit question hierarchy (Paragraph 5)

* **PARAGRAPH_ID**: I5
* **RHETORICAL_ROLE**: Present the study before its protocol and separate the two forecasting questions explicitly.
* **STUDY_FACTS_USED**:
  * Independent reimplementation and methodological audit of fractional SEIT.
  * Brazil monthly surveillance data, 2001–2022.
  * Independently re-estimated integer-order comparator.
  * External baselines: persistence, seasonal naive, and SARIMA.
  * Secondary practical-identifiability analysis.
* **GENERAL_SCIENTIFIC_CLAIMS**: None; study-design statements only.
* **VERIFIED_CITATIONS**: None required.
* **STUDY_QUESTION_SUPPORTED**: Q1 is tested first; Q2 asks whether any within-family improvement translates to external observed skill; Q3 remains explicitly secondary.
* **PROMISE_TO_RESULTS**: Preserves the result hierarchy without pre-empting the answer to Q1 or Q2.
* **OVERCLAIM_RISK**: None.
* **NOVELTY_RISK**: No theoretical novelty or historical-priority claim.

---

### I6 — Evaluation protocol and bounded contribution (Paragraph 6)

* **PARAGRAPH_ID**: I6
* **RHETORICAL_ROLE**: Summarize how the questions are evaluated and close with the bounded methodological/empirical contribution.
* **STUDY_FACTS_USED**:
  * 24-month single-origin long open-loop stress test.
  * 13-origin expanding-window rolling-origin evaluation across 12 lead horizons.
  * Parameter identifiability, predictive stability, $R_0$ practical-identifiability envelope, and Matignon DFE stability over the predefined admissible set.
* **GENERAL_SCIENTIFIC_CLAIMS**: None beyond the stated study contribution.
* **VERIFIED_CITATIONS**: None required.
* **STUDY_QUESTION_SUPPORTED**: Operationalizes Q1–Q3 after the question hierarchy has been stated.
* **PROMISE_TO_RESULTS**: Connects directly to Methods and the frozen Results sequence.
* **OVERCLAIM_RISK**: Low; contribution is explicitly methodological and empirical rather than theoretical.
* **NOVELTY_RISK**: Contribution rests on the common temporal protocol and the inference obtained by separating within-family improvement from external skill.
