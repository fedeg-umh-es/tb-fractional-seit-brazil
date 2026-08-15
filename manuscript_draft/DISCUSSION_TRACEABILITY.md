# Discussion Traceability and Argument Audit

This document provides complete paragraph-by-paragraph audit traceability for `manuscript_draft/DISCUSSION_DRAFT.md`, linking every interpretive argument, boundary condition, and methodological qualification directly to Results findings, canonical evidence, and approved architecture specifications.

---

## Global Discussion Audit Checklist

```text
CENTRAL_TURNING_POINT_LEADS_DISCUSSION = YES
RESULTS_REPEATED_EXCESSIVELY = NO
NEW_EMPIRICAL_RESULT_INTRODUCED = NO
CAUSAL_EXPLANATION_INVENTED = NO
LITERATURE_CLAIM_INVENTED = NO
NOVELTY_CLAIM_INVENTED = NO
SIGNIFICANCE_LANGUAGE_INCLUDED = NO
FORECASTING_MECHANISTIC_CONFLATION = NO
R0_ENVELOPE_BOUNDARY_RESPECTED = YES
DFE_MODEL_PROPERTY_GUARDRAIL_RESPECTED = YES
OPTIMAL_CONTROL_USED_AS_EVIDENCE = NO
```

---

## Paragraph-by-Paragraph Traceability Matrix

### D1 — Integrated main finding and turning point (Paragraph 1)

* **PARAGRAPH_ID**: D1
* **ARGUMENTATIVE_ROLE**: Establish the manuscript's primary turning point: fractional SEIT consistently improves over the independently refitted integer SEIT comparator, but this within-family advantage does not translate into positive forecast skill against persistence or SARIMA at any horizon.
* **RESULTS_FINDINGS_USED**: R1 (within-family error reduction), R2 (negative skill vs. persistence and SARIMA across $h = 1, \dots, 12$).
* **CLAIM_IDS**: C01 (`SUPPORTED_WITHIN_MODEL_FAMILY`), C02 (`NOT_SUPPORTED`), C03 (`NOT_SUPPORTED`), C05 (`NOT_SUPPORTED`).
* **CANONICAL_EVIDENCE**: `results_canonical/04_long_open_loop/table_long_open_loop.csv`, `results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv`, `table_skill_by_horizon.csv`, `table_horizon_summary.csv`.
* **INTERPRETATION_ALLOWED**: Internal ablations against simpler nested variants of the same model family can produce a misleading impression of forecasting efficacy if external baselines are omitted.
* **INTERPRETATION_FORBIDDEN**: Do not claim "fractional models are generally ineffective" or "statistical models are universally superior"; do not claim general forecasting superiority.
* **LIMITATION_USED**: Single national dataset, 13 rolling origins, specific model parameterizations.
* **LITERATURE_VERIFICATION_MARKER**: `[LITERATURE VERIFICATION REQUIRED: benchmark selection and internal ablations in epidemic forecasting]`
* **FORECASTING_MECHANISTIC_BOUNDARY_RISK**: Kept strictly focused on empirical forecast accuracy comparisons.
* **INFERENCE_BOUNDARY**: Descriptive sample comparison over the evaluated origins.

---

### D2 — Methodological role of external baselines (Paragraph 2)

* **PARAGRAPH_ID**: D2
* **ARGUMENTATIVE_ROLE**: Explain why external baselines (persistence, SARIMA) are necessary to distinguish mathematical flexibility from genuine operational forecasting utility.
* **RESULTS_FINDINGS_USED**: R1 vs. R2 contrast.
* **CLAIM_IDS**: C01, C02, C03, C05.
* **CANONICAL_EVIDENCE**: `table_skill_by_horizon.csv`, `table_horizon_summary.csv`.
* **INTERPRETATION_ALLOWED**: Outperforming an integer comparator is a structural ablation test; outperforming statistical baselines is an external forecasting test. These two questions must be evaluated with separate benchmarks.
* **INTERPRETATION_FORBIDDEN**: No invented causal explanations for why SARIMA/persistence performed better (e.g. asserting specific unproven COVID regime shifts or structural breaks as facts).
* **LIMITATION_USED**: One purpose-built statistical model (frozen SARIMA order) and simple naive benchmarks.
* **LITERATURE_VERIFICATION_MARKER**: `[LITERATURE VERIFICATION REQUIRED: comparison of mechanistic and phenomenological epidemiological models]`
* **FORECASTING_MECHANISTIC_BOUNDARY_RISK**: No mechanistic properties invoked to explain forecasting gaps.
* **INFERENCE_BOUNDARY**: Descriptive comparison; no significance claims.

---

### D3 — Seasonal-naive result as a bounded exception (Paragraph 3)

* **PARAGRAPH_ID**: D3
* **ARGUMENTATIVE_ROLE**: Contextualize the positive skill observed against seasonal naive for $h = 1 \dots 7$ as a baseline-specific, bounded exception that does not overturn the general persistence/SARIMA result.
* **RESULTS_FINDINGS_USED**: R3 (positive skill vs. seasonal naive for $h = 1 \dots 7$, negative for $h = 8 \dots 12$, $H_{\text{relax}} = 7$, $H_{\text{strict-from-h1}} = 7$).
* **CLAIM_IDS**: C04 (`SUPPORTED_ONLY_VS_SEASONAL_NAIVE`).
* **CANONICAL_EVIDENCE**: `table_skill_by_horizon.csv`, `table_horizon_summary.csv`.
* **INTERPRETATION_ALLOWED**: Forecast skill is inherently comparator- and horizon-dependent. $H = 7$ is an empirical sample descriptor for this specific series and protocol.
* **INTERPRETATION_FORBIDDEN**: Do NOT claim "the model has a seven-month useful forecasting horizon" without qualifying the baseline; do NOT treat $H = 7$ as an intrinsic biological predictability horizon; do NOT generalize to persistence or SARIMA.
* **LIMITATION_USED**: 13 origins per horizon cell; single seasonal naive baseline.
* **LITERATURE_VERIFICATION_MARKER**: None required.
* **FORECASTING_MECHANISTIC_BOUNDARY_RISK**: Bounded strictly to empirical horizon descriptions.
* **INFERENCE_BOUNDARY**: Descriptive sample summary index.

---

### D4 — Parameter non-identifiability versus predictive stability (Paragraph 4)

* **PARAGRAPH_ID**: D4
* **ARGUMENTATIVE_ROLE**: Address the finding that high predictive stability coexists with severe practical non-identifiability of individual rate parameters $\beta$, $\gamma$, and $d$, and establish that $\alpha < 1$ is not proof of biological memory.
* **RESULTS_FINDINGS_USED**: R4a (wide parameter dispersion at $\text{CV}_{\text{cal}} \approx 0.35\%$; stable predictions $\text{CV} \approx 0.19\% / 0.58\%$; stable $\alpha$).
* **CLAIM_IDS**: C06 (`NOT_SUPPORTED`: biological memory), C09 (`NOT_SUPPORTED`: parameters as precise rates).
* **CANONICAL_EVIDENCE**: `IDENTIFIABILITY_AUDIT_REPORT.md`, `outputs/calibration/fractional_multiseed.csv`, `outputs/identifiability/profile_objective.csv`.
* **INTERPRETATION_ALLOWED**: Low calibration RMSE and predictive stability do not guarantee unique parameter recovery; $\beta, \gamma, d$ cannot be reported as point estimates of biological rates. $\alpha < 1$ represents fitted power-law kernel dynamics, not proof of biological memory.
* **INTERPRETATION_FORBIDDEN**: Never cite a single $(\beta, \gamma, d)$ point estimate as a biological finding; never claim $\alpha < 1$ proves immunological/biological memory.
* **LIMITATION_USED**: Identifiability assessed practically via multiseed and profile sweeps, not full algebraic structural identifiability.
* **LITERATURE_VERIFICATION_MARKER**: `[LITERATURE VERIFICATION REQUIRED: structural and practical identifiability in epidemiological models]`
* **FORECASTING_MECHANISTIC_BOUNDARY_RISK**: Clarifies that good predictive fit does not equal parameter identifiability.
* **INFERENCE_BOUNDARY**: Practical-identifiability analysis on the calibration objective surface.

---

### D5 — Functional robustness of the basic reproduction number (Paragraph 5)

* **PARAGRAPH_ID**: D5
* **ARGUMENTATIVE_ROLE**: Explain why composite threshold functional $R_0$ remains robustly identified ($1.1542$–$1.1892$, median $1.1735$) across the admissible set despite weak identifiability of individual component parameters.
* **RESULTS_FINDINGS_USED**: R4b ($R_0$ practical-identifiability envelope over $n = 25$ admissible set).
* **CLAIM_IDS**: C07 (`SUPPORTED`), M03 (`METHODOLOGICAL/DESCRIPTIVE`).
* **CANONICAL_EVIDENCE**: `results_canonical/03_R0_stability/table_R0_stability_summary.csv`, `results_canonical/02_identifiability/table_full_profile_diagnostic.csv`, `IDENTIFIABILITY_AUDIT_REPORT.md`.
* **INTERPRETATION_ALLOWED**: Composite combinations of weakly identified parameters can be robust due to compensating parameter correlations in the objective landscape.
* **INTERPRETATION_FORBIDDEN**: Never describe the $R_0$ range as a confidence interval, credible interval, or population uncertainty interval. Do not generalize to the full 33-solution profile diagnostic pool.
* **LIMITATION_USED**: Empirical envelope over a predefined 1% RMSE admissibility tolerance.
* **LITERATURE_VERIFICATION_MARKER**: `[LITERATURE VERIFICATION REQUIRED: functional identifiability of composite epidemiological thresholds]`
* **FORECASTING_MECHANISTIC_BOUNDARY_RISK**: Functional stability is a mechanistic property, not evidence of forecast skill.
* **INFERENCE_BOUNDARY**: Derived functional evaluation over the admissible solution set.

---

### D6 — DFE stability result and mechanistic/forecasting separation (Paragraph 6)

* **PARAGRAPH_ID**: D6
* **ARGUMENTATIVE_ROLE**: Interpret the $25/25$ DFE local instability finding under the fractional Matignon criterion as mathematical self-consistency with $R_0 > 1$, while enforcing the separation between mechanistic coherence and forecasting capability.
* **RESULTS_FINDINGS_USED**: R5 ($25/25$ DFE unstable across admissible set).
* **CLAIM_IDS**: C08 (`SUPPORTED`).
* **CANONICAL_EVIDENCE**: `table_R0_stability_summary.csv`, `table_full_profile_diagnostic.csv`.
* **INTERPRETATION_ALLOWED**: DFE instability is a robust mathematical property of the calibrated dynamical system across the admissible set.
* **INTERPRETATION_FORBIDDEN**: Must NOT be stated as empirical proof of persistent TB transmission in Brazil; must NOT be generalized to the 33-member diagnostic pool; must NOT be presented as evidence of forecasting efficacy.
* **LIMITATION_USED**: Restricted to the 25-member admissible set; linearized local stability at DFE.
* **LITERATURE_VERIFICATION_MARKER**: None required.
* **FORECASTING_MECHANISTIC_BOUNDARY_RISK**: Explicitly states that mechanistic dynamical consistency does not imply external predictive accuracy.
* **INFERENCE_BOUNDARY**: Mathematical stability classification of the linearized model.

---

### D7 — Limitations and bounded contribution (Paragraph 7)

* **PARAGRAPH_ID**: D7
* **ARGUMENTATIVE_ROLE**: Synthesize all study limitations into a coherent scientific boundary and summarize the exact bounded contribution of the research.
* **RESULTS_FINDINGS_USED**: R1–R5 collectively, plus project scope constraints.
* **CLAIM_IDS**: C01, C02, C03, C04, C05, C07, C08, C09, C10 (`NOT_VERIFIED`), C11 (`NOT_TESTED`).
* **CANONICAL_EVIDENCE**: `results_canonical/KNOWN_LIMITATIONS.md` (L01–L12), `PROJECT_CANON.md`.
* **INTERPRETATION_ALLOWED**: Clear synthesis of what the evidence supports: fractional order improves the SEIT formulation within-family; external baselines expose the limits of interpreting that as operational forecasting skill; and parameter non-identifiability coexists with robust derived functional and stability properties.
* **INTERPRETATION_FORBIDDEN**: No unverified historical optimal-control claims; no statistical significance claims; no claims of universal fractional superiority.
* **LIMITATION_USED**: Complete list of pre-declared limitations (independent reimplementation, single national series, weak parameter identifiability, operational admissibility threshold, 13 origins descriptive sample, deferred DM tests, deferred optimal control).
* **LITERATURE_VERIFICATION_MARKER**: None required.
* **FORECASTING_MECHANISTIC_BOUNDARY_RISK**: Full synthesis respecting the dual-axis structure.
* **INFERENCE_BOUNDARY**: Explicit statement that forecast evaluations are descriptive and inferential tests were deferred.
