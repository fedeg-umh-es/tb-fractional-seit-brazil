# Abstract Traceability and Sentence-by-Sentence Audit

This document provides complete sentence-by-sentence audit traceability for `manuscript_draft/ABSTRACT_DRAFT.md`, mapping each sentence's rhetorical role, source manuscript section, claim IDs, canonical evidence, numbers used, and guardrails.

---

## Global Abstract Audit Checklist

```text
TURNING_POINT_VISIBLE = YES
WITHIN_FAMILY_BOUNDARY_RESPECTED = YES
EXTERNAL_BASELINE_RESULT_EXPLICIT = YES
SEASONAL_NAIVE_BOUNDARY_RESPECTED = YES
PARAMETER_IDENTIFIABILITY_BOUNDARY_RESPECTED = YES
R0_ENVELOPE_BOUNDARY_RESPECTED = YES
DFE_MODEL_PROPERTY_GUARDRAIL_RESPECTED = YES
NEW_RESULT_INTRODUCED = NO
NEW_LITERATURE_CLAIM_INTRODUCED = NO
NOVELTY_CLAIM_INTRODUCED = NO
SIGNIFICANCE_LANGUAGE_INCLUDED = NO
FORECASTING_MECHANISTIC_CONFLATION = NO
```

---

## Sentence-by-Sentence Traceability Matrix

### S1 — Problem Formulation (Sentence 1)

* **SENTENCE_ID**: S1
* **RHETORICAL_ROLE**: Background / Problem: Establish the methodological evaluation problem (evaluating fractional models requires testing beyond internal/nested ablations).
* **SOURCE_SECTION**: Introduction (§1 / I1–I2)
* **CLAIM_IDS**: M04
* **CANONICAL_EVIDENCE**: `manuscript_architecture/MANUSCRIPT_EVIDENCE_ARCHITECTURE.md` (Dominant Question Tier 1)
* **NUMBERS_USED**: None
* **PERMITTED_INTERPRETATION**: Problem framing motivating external benchmark evaluation.
* **FORBIDDEN_INTERPRETATION**: Do not claim fractional models are universally flawed or that past literature failed.
* **GENERALIZATION_BOUNDARY**: General methodological principle.

---

### S2 — Study Design and Scope (Sentence 2)

* **SENTENCE_ID**: S2
* **RHETORICAL_ROLE**: Methods / Study Scope: Define the independent reimplementation, data source (Brazil 2001–2022), Caputo derivative formulation, and corrected incidence-flow observation mapping.
* **SOURCE_SECTION**: Introduction (§1 / I5), Methods (§2.1–2.4)
* **CLAIM_IDS**: M01, M02
* **CANONICAL_EVIDENCE**: `data/brazil_tb_monthly.csv`, `docs/MODEL_CONTRACT.md`
* **NUMBERS_USED**: 2001–2022 (surveillance period)
* **PERMITTED_INTERPRETATION**: Procedural description of the independent reimplementation and observation mapping correction.
* **FORBIDDEN_INTERPRETATION**: No novelty or priority claims.
* **GENERALIZATION_BOUNDARY**: Bounded to the evaluated dataset and model formulation.

---

### S3 — Predictive Findings & Central Turning Point (Sentences 3–5)

* **SENTENCE_ID**: S3
* **RHETORICAL_ROLE**: Results (Forecasting): Report within-family error reduction alongside the central turning point (negative skill vs persistence/SARIMA at all horizons, positive skill vs seasonal naive bounded to $h=1\dots 7$).
* **SOURCE_SECTION**: Results (§3.1–3.2 / P2–P4), Discussion (§4 / D1–D3)
* **CLAIM_IDS**: C01 (`SUPPORTED_WITHIN_MODEL_FAMILY`), C02 (`NOT_SUPPORTED`), C03 (`NOT_SUPPORTED`), C04 (`SUPPORTED_ONLY_VS_SEASONAL_NAIVE`), C05 (`NOT_SUPPORTED`)
* **CANONICAL_EVIDENCE**: `results_canonical/04_long_open_loop/table_long_open_loop.csv`, `results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv`, `table_skill_by_horizon.csv`, `table_horizon_summary.csv`
* **NUMBERS_USED**: 24-month long open-loop, 13 rolling origins, 12 monthly horizons, $H_{\text{relax}} = 0$ (persistence/SARIMA), $H_{\text{relax}} = 7$ ($h=1\dots 7$, seasonal naive).
* **PERMITTED_INTERPRETATION**: Fractional SEIT outperforms integer SEIT within-family under independent re-estimation, but trails persistence and SARIMA across all evaluated horizons; positive skill vs seasonal naive is bounded to $h \le 7$ as a baseline-specific empirical descriptor.
* **FORBIDDEN_INTERPRETATION**: Must NOT claim general forecasting superiority; must NOT call $h=7$ an intrinsic disease predictability limit; no statistical significance claims.
* **GENERALIZATION_BOUNDARY**: Descriptive sample comparison over the evaluated 13 origins and dataset.

---

### S4 — Mechanistic Identifiability, R0 Envelope & DFE Dynamics (Sentences 6–7)

* **SENTENCE_ID**: S4
* **RHETORICAL_ROLE**: Results (Mechanistic): Report practical non-identifiability of individual kinetic rate parameters ($\beta, \gamma, d$), functional robustness of $R_0 \in [1.1542, 1.1892]$, and uniform DFE local instability ($25/25$) across the admissible set.
* **SOURCE_SECTION**: Results (§3.3 / P5–P7), Discussion (§4 / D4–D6)
* **CLAIM_IDS**: C06 (`NOT_SUPPORTED`: biological memory), C07 (`SUPPORTED`), C08 (`SUPPORTED`), C09 (`NOT_SUPPORTED`: parameters as precise rates), M03 (`METHODOLOGICAL/DESCRIPTIVE`)
* **CANONICAL_EVIDENCE**: `results_canonical/03_R0_stability/table_R0_stability_summary.csv`, `results_canonical/02_identifiability/table_full_profile_diagnostic.csv`, `IDENTIFIABILITY_AUDIT_REPORT.md`
* **NUMBERS_USED**: $n=25$ admissible set ($\Delta \text{RMSE}_{\text{cal}} \le 1.0\%$), $R_0 \in [1.1542, 1.1892]$, $25/25$ DFE unstable.
* **PERMITTED_INTERPRETATION**: Individual rates are practically non-identifiable and cannot be cited as precise biological values; derived composite threshold $R_0$ is robustly bounded above unity; DFE instability is a mathematical property of the fitted model over the admissible set.
* **FORBIDDEN_INTERPRETATION**: Never call $R_0$ range a confidence interval or credible interval; do not claim DFE instability proves real-world persistent transmission in Brazil; do not use mechanistic robustness as evidence of forecasting skill.
* **GENERALIZATION_BOUNDARY**: Restricted to the $n=25$ near-equivalent admissible set.

---

### S5 — Bounded Scientific Contribution (Sentence 8)

* **SENTENCE_ID**: S5
* **RHETORICAL_ROLE**: Conclusion / Implication: Synthesize the study-level takeaway (within-family structural gain, external forecasting boundaries, parameter non-identifiability coexisting with robust derived quantities).
* **SOURCE_SECTION**: Conclusion (§5 / P2), Discussion (§4 / D7)
* **CLAIM_IDS**: C01, C02, C03, C04, C07, C08, C09
* **CANONICAL_EVIDENCE**: `manuscript_architecture/MANUSCRIPT_EVIDENCE_ARCHITECTURE.md`, `results_canonical/KNOWN_LIMITATIONS.md`
* **NUMBERS_USED**: None
* **PERMITTED_INTERPRETATION**: Fractional differentiation improves compartmental flexibility within-family, external baselines delineate forecasting utility, and parameter indeterminacy coexists with robust derived functional properties.
* **FORBIDDEN_INTERPRETATION**: No universal claims about all fractional epidemic models; no unverified optimal-control claims.
* **GENERALIZATION_BOUNDARY**: Bounded strictly to this study, dataset, and model family.
