# Introduction Traceability and Audit

This document provides complete paragraph-by-paragraph audit traceability for `manuscript_draft/INTRODUCTION_DRAFT.md`, mapping rhetorical roles, study facts, literature markers, and guardrails directly to the approved manuscript architecture in `manuscript_architecture/INTRODUCTION_REQUIREMENTS.md` and `manuscript_architecture/MANUSCRIPT_EVIDENCE_ARCHITECTURE.md`.

---

## Global Introduction Audit Checklist

```text
INTRODUCTION_FUNNEL_COHERENT = YES
DOMINANT_QUESTION_PRESERVED = YES
MECHANISTIC_AXIS_SUBORDINATE = YES
RESULTS_PREEMPTED = NO
UNVERIFIED_GAP_ASSERTED_AS_FACT = NO
NOVELTY_CLAIM_INVENTED = NO
LITERATURE_REFERENCE_INVENTED = NO
FORECASTING_SUPERIORITY_PROMISED = NO
PARAMETER_PRECISION_PROMISED = NO
R0_POPULATION_INFERENCE_PROMISED = NO
```

---

## Consolidated Literature Verification Markers (4 Total)

1. `[LITERATURE VERIFICATION REQUIRED: tuberculosis epidemiology and surveillance in Brazil]` (Paragraph 1)
2. `[LITERATURE VERIFICATION REQUIRED: external-baseline evaluation of mechanistic epidemic forecasting models]` (Paragraph 1)
3. `[LITERATURE VERIFICATION REQUIRED: fractional-order compartmental models in infectious-disease modelling]` (Paragraph 2)
4. `[LITERATURE VERIFICATION REQUIRED: parameter and functional identifiability in epidemiological compartmental models]` (Paragraph 3)

---

## Paragraph-by-Paragraph Traceability Matrix

### I1 — Scientific stakes and compartmental epidemic models (Paragraph 1)

* **PARAGRAPH_ID**: I1
* **RHETORICAL_ROLE**: Funnel top: Introduce the role of mechanistic compartmental models in representing transmission and latent processes, establish the application context of tuberculosis in Brazil, and introduce the distinction between historical goodness-of-fit and out-of-sample forecast accuracy.
* **STUDY_FACTS_USED**: Application context of Brazilian tuberculosis monthly surveillance records (2001–2022).
* **GENERAL_SCIENTIFIC_CLAIMS**: Compartmental models represent transmission and latent dynamics; TB is a public health challenge in Brazil; calibration fit does not guarantee forward forecast accuracy.
* **LITERATURE_VERIFICATION_MARKERS**:
  * `[LITERATURE VERIFICATION REQUIRED: tuberculosis epidemiology and surveillance in Brazil]`
  * `[LITERATURE VERIFICATION REQUIRED: external-baseline evaluation of mechanistic epidemic forecasting models]`
* **STUDY_QUESTION_SUPPORTED**: Motivates questions 1 and 2 (forecasting evaluation).
* **PROMISE_TO_RESULTS**: Promises a rigorous out-of-sample forecast evaluation distinguishing fit from forward projection.
* **OVERCLAIM_RISK**: None; no claims of model superiority or performance outcomes.
* **NOVELTY_RISK**: None; functional framing without encylopedic generalizations.
* **GENERALIZATION_RISK**: Kept to general mathematical epidemiological principles.

---

### I2 — Fractional-order extensions and the evaluation problem (Paragraph 2)

* **PARAGRAPH_ID**: I2
* **RHETORICAL_ROLE**: Funnel step 2: Introduce fractional-order operators as extensions introducing power-law temporal dependence, and identify the methodological problem of evaluating models solely against internal/nested integer-order ablations rather than external baselines.
* **STUDY_FACTS_USED**: SEIT model family includes both fractional-order and integer-order formulations.
* **GENERAL_SCIENTIFIC_CLAIMS**: Fractional operators introduce power-law dependence; internal ablations demonstrate within-family flexibility but do not evaluate external predictive utility.
* **LITERATURE_VERIFICATION_MARKERS**:
  * `[LITERATURE VERIFICATION REQUIRED: fractional-order compartmental models in infectious-disease modelling]`
* **STUDY_QUESTION_SUPPORTED**: Sets up Sub-question 1 (fractional vs. integer) and Sub-question 2 (external baselines).
* **PROMISE_TO_RESULTS**: Promises comparative evaluation against both integer-order SEIT and external baselines.
* **OVERCLAIM_RISK**: None; does not promise that fractional models are superior.
* **NOVELTY_RISK**: Avoids asserting an unverified universal gap in the field; framed as a logical evaluation requirement.
* **GENERALIZATION_RISK**: Bounded to the evaluation logic of mathematical models.

---

### I3 — The parameter identifiability problem in calibration (Paragraph 3)

* **PARAGRAPH_ID**: I3
* **RHETORICAL_ROLE**: Funnel step 3: Establish the mechanistic challenge: aggregate incidence data frequently lead to practical non-identifiability of individual kinetic rate parameters despite low calibration errors and stable trajectory fits, motivating our analytical separation of evidence levels.
* **STUDY_FACTS_USED**: Calibration against aggregate monthly incidence series; estimation of kinetic parameters and derived $R_0$.
* **GENERAL_SCIENTIFIC_CLAIMS**: Practical non-identifiability is common when calibrating compartmental models from single aggregate streams; trajectory stability can coexist with parameter indeterminacy.
* **LITERATURE_VERIFICATION_MARKERS**:
  * `[LITERATURE VERIFICATION REQUIRED: parameter and functional identifiability in epidemiological compartmental models]`
* **STUDY_QUESTION_SUPPORTED**: Sets up Sub-question 3 (mechanistic interpretability under non-identifiability).
* **PROMISE_TO_RESULTS**: Promises an identifiability audit distinguishing parameter, predictive, and functional stability.
* **OVERCLAIM_RISK**: None; does not report specific parameter or $R_0$ numerical ranges.
* **NOVELTY_RISK**: Does not claim this is the first study to document non-identifiability.
* **GENERALIZATION_RISK**: Framed as study analytical framework.

---

### I4 — Specific methodological framework (Paragraph 4)

* **PARAGRAPH_ID**: I4
* **RHETORICAL_ROLE**: Funnel narrow: Articulate the study's specific evaluation framework that explicitly separates within-family flexibility from external forecasting competitiveness, and individual parameter recovery from derived functional stability.
* **STUDY_FACTS_USED**: Study evaluates (i) integer vs fractional comparison, (ii) external multi-horizon baselines, and (iii) parameter vs functional identifiability.
* **GENERAL_SCIENTIFIC_CLAIMS**: Stated as study evaluation requirements.
* **LITERATURE_VERIFICATION_MARKERS**: None (analytical synthesis).
* **STUDY_QUESTION_SUPPORTED**: Integrates all three study sub-questions.
* **PROMISE_TO_RESULTS**: Establishes the exact dual-axis evaluation structure reported in Results.
* **OVERCLAIM_RISK**: None.
* **NOVELTY_RISK**: None; states study objectives analytically without normative claims.
* **GENERALIZATION_RISK**: None.

---

### I5 — Study response, questions, and evaluation design (Paragraph 5)

* **PARAGRAPH_ID**: I5
* **RHETORICAL_ROLE**: Study specification: Introduce the independent reimplementation of the fractional SEIT model for Brazil (2001–2022), the corrected incidence observation mapping, state the 3 explicit sub-questions, and summarize the evaluation protocols without revealing numerical results.
* **STUDY_FACTS_USED**:
  * Independent reimplementation of fractional SEIT model for Brazil (2001–2022).
  * Reference-time-consistent Caputo derivative formulation.
  * Corrected observation process mapping notifications to $E \to I$ incidence flow.
  * Three explicit study sub-questions verbatim from `INTRODUCTION_REQUIREMENTS.md`.
  * Two forecasting protocols: 24-month long open-loop stress test and 13-origin rolling-origin cross-validation ($h=1\dots 12$).
  * External baselines: persistence, seasonal naive ($\text{lag } 12$), SARIMA.
  * Mechanistic audits: multiseed optimization, profile-objective identifiability, $R_0$ practical-identifiability envelope, Matignon DFE local stability analysis.
* **GENERAL_SCIENTIFIC_CLAIMS**: None (strictly study design facts).
* **LITERATURE_VERIFICATION_MARKERS**: None.
* **STUDY_QUESTION_SUPPORTED**: Directly articulates all three sub-questions.
* **PROMISE_TO_RESULTS**: Sets up Methods (§2) and Results (§3) precisely without pre-empting numerical outcomes or announcing the turning point.
* **OVERCLAIM_RISK**: Zero; no outcome results or performance claims mentioned.
* **NOVELTY_RISK**: Framed strictly as an independent reimplementation and audit.
* **GENERALIZATION_RISK**: Bounded to the evaluated dataset and protocols.
