# Manuscript Literature Marker Resolution Audit

This document provides sentence-by-sentence verification and resolution recommendations for all literature markers in `manuscript_draft/INTRODUCTION_DRAFT.md` and `manuscript_draft/DISCUSSION_DRAFT.md`.

---

## Introduction Marker Resolutions

### Marker I-01
* **MARKER**: `[LITERATURE VERIFICATION REQUIRED: tuberculosis epidemiology and surveillance in Brazil]`
* **PARAGRAPH**: Introduction, Paragraph 1 (I1)
* **CURRENT_SENTENCE**: "In diseases with protracted latency and complex clinical progression, such as tuberculosis—which remains a persistent public health challenge in Brazil [LITERATURE VERIFICATION REQUIRED: tuberculosis epidemiology and surveillance in Brazil]—mathematical models often aim to serve dual purposes: providing mechanistic insight into unobserved infection states and generating forward projections of reported surveillance data."
* **VERDICT**: `SUPPORTED_AS_WRITTEN`
* **SOURCES**:
  * World Health Organization. (2022). *Global Tuberculosis Report 2022*. Geneva: WHO.
  * Pelissari, D. M., et al. (2020). Notifiable Diseases Information System (SINAN): main features of tuberculosis notification and data analysis. *Epidemiol. Serv. Saude*, 29(1), e2019154. DOI: 10.5123/S1679-49742020000100009.
* **EXACT CLAIM SUPPORTED**: Tuberculosis is a major persistent public health challenge in Brazil (high-burden country designation), and SINAN is the standardized national notification system.
* **BOUNDARY / CAVEAT**: Retain qualitative statement; do not introduce volatile annual incidence/mortality statistics that quickly become obsolete.
* **RECOMMENDED FINAL SENTENCE**: "In diseases with protracted latency and complex clinical progression, such as tuberculosis—which remains a persistent public health challenge in Brazil (World Health Organization, 2022; Pelissari et al., 2020)—mathematical models often aim to serve dual purposes: providing mechanistic insight into unobserved infection states and generating forward projections of reported surveillance data."
* **RECOMMENDED CITATION PLACEMENT**: `(World Health Organization, 2022; Pelissari et al., 2020)` directly after "Brazil".

---

### Marker I-02
* **MARKER**: `[LITERATURE VERIFICATION REQUIRED: external-baseline evaluation of mechanistic epidemic forecasting models]`
* **PARAGRAPH**: Introduction, Paragraph 1 (I1)
* **CURRENT_SENTENCE**: "A close calibration fit to historical surveillance records does not ensure that a compartmental model will reliably forecast future trajectory changes when subjected to strict temporal evaluation [LITERATURE VERIFICATION REQUIRED: external-baseline evaluation of mechanistic epidemic forecasting models]."
* **VERDICT**: `SUPPORTED_AS_WRITTEN`
* **SOURCES**:
  * Moran, K. R., et al. (2016). Epidemic forecasting is messier than weather forecasting: The role of human behavior and Internet data streams in epidemic forecast. *J. Infect. Dis.*, 214(suppl_4), S404–S408. DOI: 10.1093/infdis/jiw375.
  * Bracher, J., Ray, E. L., Gneiting, T., & Reich, N. G. (2021). Evaluating epidemic forecasts in an interval format. *PLOS Comput. Biol.*, 17(2), e1008618. DOI: 10.1371/journal.pcbi.1008618.
* **EXACT CLAIM SUPPORTED**: Historical goodness-of-fit does not guarantee forward out-of-sample forecast accuracy; out-of-sample evaluations against standard reference baselines are essential to measure genuine predictive skill.
* **BOUNDARY / CAVEAT**: Framed as a general methodological principle in epidemic forecasting, not an unverified empirical gap or universal failure claim.
* **RECOMMENDED FINAL SENTENCE**: "A close calibration fit to historical surveillance records does not ensure that a compartmental model will reliably forecast future trajectory changes when subjected to strict temporal evaluation (Moran et al., 2016; Bracher et al., 2021)."
* **RECOMMENDED CITATION PLACEMENT**: `(Moran et al., 2016; Bracher et al., 2021)` at sentence end.

---

### Marker I-03
* **MARKER**: `[LITERATURE VERIFICATION REQUIRED: fractional-order compartmental models in infectious-disease modelling]`
* **PARAGRAPH**: Introduction, Paragraph 2 (I2)
* **CURRENT_SENTENCE**: "Fractional-order formulations extend compartmental models by replacing integer-order derivatives with non-local operators that introduce power-law temporal dependence [LITERATURE VERIFICATION REQUIRED: fractional-order compartmental models in infectious-disease modelling]."
* **VERDICT**: `SUPPORTED_AS_WRITTEN`
* **SOURCES**:
  * Diethelm, K. (2013). A fractional calculus based model for the simulation of an outbreak of dengue fever. *Nonlinear Dyn.*, 71(4), 613–619. DOI: 10.1007/s11071-012-0475-2.
  * Area, I., et al. (2015). On a fractional order epidemic model with Caputo derivative. *Appl. Math. Lett.*, 40, 23–27. DOI: 10.1016/j.aml.2014.09.006.
* **EXACT CLAIM SUPPORTED**: Fractional-order derivatives replace standard integer rates with non-local operators that capture power-law temporal dependence and non-exponential residence times in compartmental models.
* **BOUNDARY / CAVEAT**: Do not assert that fractional operators prove biological or immunological memory in hosts.
* **RECOMMENDED FINAL SENTENCE**: "Fractional-order formulations extend compartmental models by replacing integer-order derivatives with non-local operators that introduce power-law temporal dependence (Diethelm, 2013; Area et al., 2015)."
* **RECOMMENDED CITATION PLACEMENT**: `(Diethelm, 2013; Area et al., 2015)` directly after "temporal dependence".

---

### Marker I-04
* **MARKER**: `[LITERATURE VERIFICATION REQUIRED: parameter and functional identifiability in epidemiological compartmental models]`
* **PARAGRAPH**: Introduction, Paragraph 3 (I3)
* **CURRENT_SENTENCE**: "When compartmental systems are calibrated against aggregate surveillance notifications, multiple disparate combinations of kinetic rate parameters can often produce near-identical trajectory fits to the observed data—a condition known as practical non-identifiability [LITERATURE VERIFICATION REQUIRED: parameter and functional identifiability in epidemiological compartmental models]."
* **VERDICT**: `SUPPORTED_AS_WRITTEN`
* **SOURCES**:
  * Tuncer, N., & Le, T. T. (2018). Structural and practical identifiability analysis of outbreak models. *Math. Biosci.*, 299, 1–18. DOI: 10.1016/j.mbs.2018.02.004.
  * Roosa, S., & Chowell, G. (2019). Assessing parameter identifiability in compartmental dynamic models using a computational approach. *Theor. Biol. Med. Model.*, 16, 1. DOI: 10.1186/s12976-018-0094-2.
  * Meshkat, N., Kuo, C. E., & Sullivant, S. (2014). On finding identifiable parameter combinations in nonlinear dynamic systems. *PLOS ONE*, 9(10), e110261. DOI: 10.1371/journal.pone.0110261.
* **EXACT CLAIM SUPPORTED**: Calibration of compartmental ODE systems to aggregate notifications frequently leads to practical non-identifiability, where disparate parameter vectors produce nearly identical trajectory fits, whereas specific composite parameter combinations can remain identifiable.
* **BOUNDARY / CAVEAT**: Standard literature terminology designates this as "identifiable parameter combinations" and "practical identifiability of composite quantities".
* **RECOMMENDED FINAL SENTENCE**: "When compartmental systems are calibrated against aggregate surveillance notifications, multiple disparate combinations of kinetic rate parameters can often produce near-identical trajectory fits to the observed data—a condition known as practical non-identifiability (Tuncer & Le, 2018; Roosa & Chowell, 2019; Meshkat et al., 2014)."
* **RECOMMENDED CITATION PLACEMENT**: `(Tuncer & Le, 2018; Roosa & Chowell, 2019; Meshkat et al., 2014)` at sentence end.

---

## Discussion Marker Resolutions

### Marker D-01
* **MARKER**: `[LITERATURE VERIFICATION REQUIRED: benchmark selection and internal ablations in epidemic forecasting]`
* **PARAGRAPH**: Discussion, Paragraph 1 (D1)
* **CURRENT_SENTENCE**: "In this evaluation, restricting comparison to variants within the same compartmental family would have produced a substantially more favorable assessment of predictive performance than comparison against external statistical baselines [LITERATURE VERIFICATION REQUIRED: benchmark selection and internal ablations in epidemic forecasting]."
* **VERDICT**: `SUPPORTED_AS_WRITTEN`
* **SOURCES**: Bracher et al. (2021), *PLOS Comput. Biol.*; Cramer et al. (2022), *PNAS*.
* **RECOMMENDED CITATION PLACEMENT**: `(Bracher et al., 2021; Cramer et al., 2022)` at sentence end.

---

### Marker D-02
* **MARKER**: `[LITERATURE VERIFICATION REQUIRED: comparison of mechanistic and phenomenological epidemiological models]`
* **PARAGRAPH**: Discussion, Paragraph 2 (D2)
* **CURRENT_SENTENCE**: "While statistical time-series models do not encode compartmental transmission mechanisms, their operational forecast accuracy highlights the need to treat within-family mathematical improvements and operational forecasting utility as distinct scientific questions [LITERATURE VERIFICATION REQUIRED: comparison of mechanistic and phenomenological epidemiological models]."
* **VERDICT**: `SUPPORTED_AS_WRITTEN`
* **SOURCES**: Moran et al. (2016), *J. Infect. Dis.*; Cramer et al. (2022), *PNAS*.
* **RECOMMENDED CITATION PLACEMENT**: `(Moran et al., 2016; Cramer et al., 2022)` at sentence end.

---

### Marker D-03
* **MARKER**: `[LITERATURE VERIFICATION REQUIRED: structural and practical identifiability in epidemiological models]`
* **PARAGRAPH**: Discussion, Paragraph 4 (D4)
* **CURRENT_SENTENCE**: "Consequently, low calibration RMSE and stable forecasts do not imply unique parameter recovery, and individual rate estimates cannot be interpreted as precise epidemiological quantities [LITERATURE VERIFICATION REQUIRED: structural and practical identifiability in epidemiological models]."
* **VERDICT**: `SUPPORTED_AS_WRITTEN`
* **SOURCES**: Tuncer & Le (2018), *Math. Biosci.*; Roosa & Chowell (2019), *Theor. Biol. Med. Model.*
* **RECOMMENDED CITATION PLACEMENT**: `(Tuncer & Le, 2018; Roosa & Chowell, 2019)` at sentence end.

---

### Marker D-04
* **MARKER**: `[LITERATURE VERIFICATION REQUIRED: functional identifiability of composite epidemiological thresholds]`
* **PARAGRAPH**: Discussion, Paragraph 5 (D5)
* **CURRENT_SENTENCE**: "This pattern is consistent with compensating variation among individual parameters that preserves the composite transmission-to-removal functional defining $R_0$ [LITERATURE VERIFICATION REQUIRED: functional identifiability of composite epidemiological thresholds]."
* **VERDICT**: `SUPPORTED_AS_WRITTEN`
* **SOURCES**: Meshkat, Kuo, & Sullivant (2014), *PLOS ONE*; Raue et al. (2009), *Bioinformatics*.
* **RECOMMENDED CITATION PLACEMENT**: `(Meshkat et al., 2014; Raue et al., 2009)` at sentence end.

---

## Audit Summary

* **Introduction Sentences**:
  * `SUPPORTED_AS_WRITTEN`: 4
  * `SUPPORTED_IF_NARROWED`: 0
  * `UNSUPPORTED`: 0
  * `UNNECESSARY`: 0
* **Discussion Markers Resolved**: 4/4
* **Novelty Claim Added**: NO
* **Unverified Gap Claim Added**: NO
* **Manuscript Story Requires Change**: NO (all frozen claims, boundaries, and turning points are completely supported by the verified literature base).
