# Conclusion Traceability and Audit

This document provides complete paragraph-by-paragraph audit traceability for `manuscript_draft/CONCLUSION_DRAFT.md`, linking every synthesized finding, empirical boundary, and final scientific takeaway directly to the frozen Methods, Results, Discussion, and canonical artifacts.

---

## Global Conclusion Audit Checklist

```text
WITHIN_FAMILY_BOUNDARY_RESPECTED = YES
EXTERNAL_BASELINE_TURNING_POINT_PRESERVED = YES
SEASONAL_NAIVE_BOUNDARY_RESPECTED = YES
IDENTIFIABILITY_BOUNDARY_RESPECTED = YES
R0_ENVELOPE_BOUNDARY_RESPECTED = YES
DFE_MODEL_PROPERTY_GUARDRAIL_RESPECTED = YES
NEW_EMPIRICAL_RESULT_INTRODUCED = NO
NEW_LITERATURE_CLAIM_INTRODUCED = NO
SIGNIFICANCE_LANGUAGE_INCLUDED = NO
OPTIMAL_CONTROL_USED_AS_EVIDENCE = NO
FORECASTING_MECHANISTIC_CONFLATION = NO
```

---

## Paragraph-by-Paragraph Traceability Matrix

### C_P1 — Predictive synthesis: within-family gain vs. external baseline boundaries (Paragraph 1)

* **PARAGRAPH_ID**: C_P1
* **ARGUMENTATIVE_ROLE**: Summarize the core forecasting findings: fractional SEIT provides a consistent within-family improvement over the independently refitted integer SEIT comparator, but fails to achieve positive skill against persistence or SARIMA at any horizon, while positive skill against seasonal naive is confined to $h = 1 \dots 7$.
* **RESULTS_FINDINGS_USED**: R1 (fractional < integer error across long open-loop and rolling-origin horizons), R2 (negative skill vs. persistence and SARIMA across $h = 1 \dots 12$), R3 (positive skill vs. seasonal naive for $h = 1 \dots 7$, negative for $h = 8 \dots 12$).
* **CLAIM_IDS**: C01 (`SUPPORTED_WITHIN_MODEL_FAMILY`), C02 (`NOT_SUPPORTED`), C03 (`NOT_SUPPORTED`), C04 (`SUPPORTED_ONLY_VS_SEASONAL_NAIVE`), C05 (`NOT_SUPPORTED`).
* **CANONICAL_EVIDENCE**: `results_canonical/04_long_open_loop/table_long_open_loop.csv`, `results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv`, `table_skill_by_horizon.csv`, `table_horizon_summary.csv`.
* **PERMITTED_WORDING**: "consistent within-family improvement", "independently re-estimated integer-order SEIT comparator", "did not translate into positive observed forecast skill against standard statistical baselines", "positive observed forecast skill relative to seasonal naive was confined to lead times $h=1$ through $h=7$ months", "empirical sample descriptor".
* **FORBIDDEN_WORDING**: Do NOT state "fractional models are superior", "fractional forecasting superiority", "proved forecasting efficacy", "useful forecasting horizon" (without seasonal naive qualifier), or "statistically significant".
* **GENERALIZATION_BOUNDARY**: Specific to the Brazilian national surveillance series, evaluated 13 rolling origins, and evaluated model implementations.
* **INFERENCE_BOUNDARY**: Descriptive sample metrics; no statistical significance claims.
* **FORECASTING_MECHANISTIC_BOUNDARY**: Strictly addresses out-of-sample predictive performance.

---

### C_P2 — Mechanistic synthesis: parameter non-identifiability, functional robustness, and bounded takeaway (Paragraph 2)

* **PARAGRAPH_ID**: C_P2
* **ARGUMENTATIVE_ROLE**: Synthesize the mechanistic axis: weak practical identifiability of individual kinetic rate parameters ($\beta, \gamma, d$) limits point estimation, while derived dynamical functionals ($R_0 \in [1.1542, 1.1892]$) and DFE local instability under Matignon's criterion are robust across the admissible set, closing with the overall bounded scientific contribution.
* **RESULTS_FINDINGS_USED**: R4a (parameter non-identifiability at tight calibration fit), R4b ($R_0$ practical envelope over $n = 25$ admissible set), R5 ($25/25$ DFE local instability).
* **CLAIM_IDS**: C06 (`NOT_SUPPORTED`: biological memory), C07 (`SUPPORTED`), C08 (`SUPPORTED`), C09 (`NOT_SUPPORTED`: parameters as precise rates), M03 (`METHODOLOGICAL/DESCRIPTIVE`).
* **CANONICAL_EVIDENCE**: `results_canonical/03_R0_stability/table_R0_stability_summary.csv`, `results_canonical/02_identifiability/table_full_profile_diagnostic.csv`, `IDENTIFIABILITY_AUDIT_REPORT.md`.
* **PERMITTED_WORDING**: "practical non-identifiability of individual kinetic rate parameters", "precluding their interpretation as precise biological rates", "functionally robust across the predefined near-equivalent admissible set ($n=25$ solutions with $\Delta\text{RMSE}_{\text{cal}} \le 1.0\%$)", "practical-identifiability envelope", "uniform local instability of the Disease-Free Equilibrium under Matignon's criterion", "mathematical property of fitted model".
* **FORBIDDEN_WORDING**: Do NOT call the $R_0$ range a confidence interval or credible interval; do NOT claim DFE instability proves real-world persistent transmission; do NOT use mechanistic robustness as evidence of forecasting skill; do NOT include unverified historical optimal-control claims.
* **GENERALIZATION_BOUNDARY**: Restrained to the $n = 25$ near-equivalent admissible set; does not extend to the broader $n = 33$ exploratory diagnostic pool.
* **INFERENCE_BOUNDARY**: Mathematical and functional evaluation over the admissible solution set.
* **FORECASTING_MECHANISTIC_BOUNDARY**: Enforces the explicit separation: mechanistic flexibility and derived functional robustness are distinct from operational forecasting capability.
