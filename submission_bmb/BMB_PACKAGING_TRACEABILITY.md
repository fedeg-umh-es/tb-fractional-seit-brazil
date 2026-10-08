# Bulletin of Mathematical Biology — Packaging Traceability

This document retains historical packaging decisions. The canonical manuscript is `submission_bmb/BMB_MANUSCRIPT.md`; `manuscript_package/MASTER_MANUSCRIPT.md` is a superseded text-copy pointer. The current abstract is reproduced verbatim in `submission_bmb/BMB_ABSTRACT.md` (208 whitespace tokens). Historical section counts below are not a current readiness certification.

---

## 1. Packaging Metadata & Commit Traceability

```text
REPOSITORY_AUTHOR = fedeg
TARGET_JOURNAL = Bulletin of Mathematical Biology (BMB)
PUBLISHER = Springer Nature / Society for Mathematical Biology
CANONICAL_EVIDENCE_FREEZE_COMMIT = 5617559bb0bf43d7223a7bb2491ab1e41fa4a084
FREEZE_DOCUMENTATION_CORRECTION_COMMIT = 8ba6ea2bac741ae17b05e9b397af4057585929dc
CURRENT_ABSTRACT_SOURCE = submission_bmb/BMB_MANUSCRIPT.md
CURRENT_ABSTRACT_WHITESPACE_TOKENS = 208
ADAPTATION_PRINCIPLE = PACKAGING_ONLY_WITHOUT_ALTERING_SCIENCE
```

---

## 2. Historical Section Adaptation Decisions

### Title Adaptation
* **Source**: `manuscript_package/MASTER_MANUSCRIPT.md` (Placeholder)
* **BMB Selected Title**: `Within-Family Improvement Versus External Forecast Skill in a Fractional SEIT Tuberculosis Model`
* **Editorial Rationale**: Eliminates any ambiguity regarding "fractional superiority" by immediately pairing within-family reduction with external forecasting benchmarking in mathematical epidemiology.

### Abstract Adaptation
* **Source**: `manuscript_package/MASTER_MANUSCRIPT.md` (268 words)
* **BMB Adaptation**: Compressed to 243 words in `submission_bmb/BMB_ABSTRACT.md`.
* **Changes**: Trimmed minor descriptive qualifiers and consolidated phrasing while preserving the verbatim desk-review control sentence, all numerical bounds ($h=1\dots 12$, $H_{\text{relax}} = 0$, $H_{\text{relax}} = 7$, $R_0 \in [1.1542, 1.1892]$), and the seven-step narrative arc.
* **ABSTRACT_LIMIT_VERIFIED**: YES (243 $\le 250$ words).

### Introduction Audit
* **INTRODUCTION_BMB_CHANGE = LOCAL_STRUCTURAL_REVISION**
* **Audit Findings**: The canonical Introduction now presents the study/question hierarchy before the evaluation protocol, explicitly separates Q1 (fractional vs. independently re-estimated integer SEIT) from Q2 (external forecasting skill), preserves practical identifiability as a secondary axis, and retains the verified neighboring precedents that prevent a universal-absence novelty claim. No scientific result, numerical evidence, or claim boundary was changed.

### Methods Audit
* **METHODS_BMB_CHANGE = NONE**
* **Audit Findings**: The frozen Methods section (2431 words) completely specifies: Caputo fractional calculus with reference-time scaling ($\tau_0^{1-\alpha}$), incidence flow accumulator mapping ($C(t)$), Differential Evolution calibration contracts, independent integer-order re-estimation, 13-origin rolling-origin cross-validation, external baseline formulations (persistence, seasonal naive, SARIMA), Next-Generation Matrix derivation of $R_0$, and Matignon's DFE local asymptotic stability criterion.

### Results Audit
* **RESULTS_BMB_CHANGE = NONE**
* **Audit Findings**: The frozen Results section (1017 words) accurately presents the canonical evidence across R1 (within-family reduction), R2 (negative skill vs. persistence/SARIMA), Turning Point (within-family $\ne$ external skill), R3 (seasonal naive bounded $h=1\dots 7$ exception), R4 (weak parameter identifiability + stable predictions), and R5 (narrow $R_0$ envelope + $25/25$ Matignon DFE instability).

### Discussion Audit
* **DISCUSSION_BMB_CHANGE = NONE**
* **Audit Findings**: The frozen Discussion section (878 words) thoroughly contextualizes the empirical divergence, explains why within-family improvement is insufficient for operational forecasting, analyzes parameter compensation and $R_0$ functional robustness, details Matignon stability properties, and transparently bounds all conclusions (descriptive sample comparisons, no unverified control assertions).

### Conclusion Audit
* **CONCLUSION_BMB_CHANGE = NONE**
* **Audit Findings**: The frozen Conclusion section (243 words) cleanly and accurately summarizes the dual findings of the manuscript.

---

## 3. Historical Word Count Audit (superseded for the current abstract)

| Manuscript Section | Source Word Count | BMB Package Word Count | Change / Status |
| :--- | :---: | :---: | :---: |
| **Title** | 13 | 12 | Selected Primary Title |
| **Abstract** | 268 | 243 | Compressed ($\le 250$ words) |
| **1. Introduction** | 585 | — | Local structural revision; current text in `submission_bmb/BMB_MANUSCRIPT.md` |
| **2. Methods** | 2431 | 2431 | Unchanged (`NONE`) |
| **3. Results** | 1017 | 1017 | Unchanged (`NONE`) |
| **4. Discussion** | 878 | 878 | Unchanged (`NONE`) |
| **5. Conclusion** | 243 | 243 | Unchanged (`NONE`) |
| **Total Main Text (1–5)** | 5154 | — | Historical count superseded after local Introduction revision; scientific evidence unchanged |

---

## 4. Scientific Guardrail Compliance Verification

```text
NEW_SCIENTIFIC_CLAIM_INTRODUCED = NO
NEW_EXPERIMENT_RUN = NO
SCIENTIFIC_RESULTS_MODIFIED = NO
CANONICAL_EVIDENCE_MODIFIED = NO
STATISTICAL_BOUNDARY_PRESERVED = YES
DFE_MATIGNON_STABILITY_BOUNDED = YES
R0_ENVELOPE_INTERPRETATION_BOUNDED = YES
```
