# Manuscript Assembly Audit

This document provides a comprehensive structural, textual, and claim consistency audit for `manuscript_package/MASTER_MANUSCRIPT.md`, confirming that the assembled text matches the frozen section drafts exactly without alteration of scientific prose.

---

## Assembly Status Summary

```text
REPOSITORY_AUTHOR = fedeg
ASSEMBLY_MODE = STRICT_SECTION_CONCATENATION
PROSE_ALTERATIONS_DETECTED = NO
FROZEN_CLAIMS_PRESERVED = YES
ALL_SECTIONS_PRESENT = YES
REFERENCES_LIST_INCLUDED = YES
```

---

## Section-by-Section Verification

| Section Number & Title | Source Draft File | Status | Hash / Commit of Source | Prose Integrity |
| :--- | :--- | :---: | :---: | :---: |
| **Title Placeholder** | Standardized Title | FROZEN | `6663204d` | Verified placeholder |
| **Abstract** | `manuscript_draft/ABSTRACT_DRAFT.md` | FROZEN | `6663204d` | Exact match (268 words prose) |
| **1. Introduction** | `manuscript_draft/INTRODUCTION_DRAFT.md` | FROZEN | `6590bf5e` | Exact match (5 paragraphs) |
| **2. Methods** | `manuscript_draft/METHODS_DRAFT.md` | FROZEN | `b5d755d1` | Exact match (12 subsections) |
| **3. Results** | `manuscript_draft/RESULTS_DRAFT.md` | FROZEN | `eb87b21d` | Exact match (3 subsections) |
| **4. Discussion** | `manuscript_draft/DISCUSSION_DRAFT.md` | FROZEN | `6590bf5e` | Exact match (7 paragraphs) |
| **5. Conclusion** | `manuscript_draft/CONCLUSION_DRAFT.md` | FROZEN | `9ab89605` | Exact match (2 paragraphs) |
| **References** | `literature_verification/VERIFIED_REFERENCES_USED.md` | FROZEN | `6590bf5e` | Exact match (11 verified refs) |

---

## Core Scientific Story & Turning Point Audit

1. **Within-Family Structural Comparison**:
   * Fractional SEIT achieves lower RMSE/MAE than independently refitted integer SEIT across 24-month long open-loop stress test and all 12 rolling-origin horizons ($h = 1 \dots 12$).
   * Preserved in Abstract, Results §3.1, Discussion §4 (D1–D2), Conclusion §5.

2. **External Statistical Benchmarking (Central Turning Point)**:
   * Persistence (random walk) and SARIMA achieve lower error than Fractional SEIT across all 12 horizons ($H_{\text{relax}} = 0$, $H_{\text{strict-from-h1}} = 0$).
   * Preserved in Abstract, Results §3.2, Discussion §4 (D1–D2), Conclusion §5.

3. **Seasonal Naive Bounded Horizon Exception**:
   * Fractional SEIT achieves positive skill only for $h = 1 \dots 7\text{ months}$ ($H_{\text{relax}} = 7$, $H_{\text{strict-from-h1}} = 7$); negative skill for $h = 8 \dots 12$.
   * Preserved as a baseline-specific empirical sample descriptor in Abstract, Results §3.2, Discussion §4 (D3), Conclusion §5.

4. **Mechanistic Identifiability vs. Predictive Stability**:
   * Individual kinetic parameters $\beta, \gamma, d$ vary widely ($\text{CV} \approx 58\%\dots 82\%$) across near-equivalent calibrations ($\text{CV}_{\text{cal}} \approx 0.35\%$), while predictions remain highly stable ($\text{CV} \approx 0.19\%\dots 0.58\%$).
   * Preserved in Abstract, Results §3.3, Discussion §4 (D4), Conclusion §5.

5. **Functional Robustness of $R_0$ Envelope & DFE Dynamics**:
   * Derived $R_0 \in [1.1542, 1.1892]$ (median $1.1735$, IQR $1.1682$–$1.1770$) across $n = 25$ admissible set ($\Delta \text{RMSE}_{\text{cal}} \le 1.0\%$).
   * DFE is locally asymptotically unstable under Matignon's criterion in $25/25$ admissible solutions, dynamically consistent with $R_0 > 1$.
   * Stated strictly as mathematical properties over the admissible set; no population confidence intervals, no empirical claims about real-world transmission in Brazil.
   * Preserved in Abstract, Results §3.3, Discussion §4 (D5–D6), Conclusion §5.

6. **Statistical Boundary Guardrail**:
   * Descriptive sample comparison across 13 origins; no claims of formal inferential superiority or statistical significance.
   * Preserved in Abstract, Methods §2.12, Results §3.2, Discussion §4 (D7), Conclusion §5.

---

## Assembly Conclusion

The master manuscript document is fully assembled, internally consistent, and ready for figure/table integration and journal-fit assessment.
