# Bulletin of Mathematical Biology — Figure and Table Submission Package

This document specifies the inventory and claim-safe captions for the main-text and supplementary figures and tables prepared for submission to the *Bulletin of Mathematical Biology*. No canonical figure, table, numerical result, or plotting code is changed here.

---

## 1. Package Inventory Summary

```text
MAIN_FIGURES_COUNT = 3
MAIN_TABLES_COUNT = 2
SUPPLEMENTARY_FIGURES_COUNT = 1
SUPPLEMENTARY_TABLES_COUNT = 3
REDUNDANT_ITEMS_COUNT = 0
TOTAL_ITEMS = 9
FIGURE_TABLE_STATUS = CONTENT_COMPLETE_CAPTIONS_CLAIM_AUDITED
```

---

## 2. Figures Specification

### Figure 1 (FIG-01)
* **ID**: FIG-01
* **MAIN_OR_SUPPLEMENTARY**: MAIN
* **FILE_NAME**: `F1_rmse_vs_horizon.png`
* **CANONICAL_PATH**: `results_canonical/06_figures/F1_rmse_vs_horizon.png`
* **SCIENTIFIC_ROLE**: Multi-model rolling-origin RMSE trajectories across lead horizons $h = 1,\dots,12$ months.
* **CLAIMS_SUPPORTED**: C01 (fractional SEIT has lower observed error than independently refitted integer SEIT); C02/C03 (fractional SEIT has higher observed error than persistence and SARIMA at every evaluated horizon); C04 (fractional versus seasonal-naive crossover between $h=7$ and $h=8$).
* **CLAIM-SAFE CAPTION**: **Figure 1.** Root Mean Squared Error (RMSE) across 12 monthly forecast horizons in the 13-origin expanding-window evaluation. Fractional SEIT and independently refitted Integer SEIT form the within-family mechanistic comparison; Persistence, Seasonal Naive ($\mathrm{lag}\,12$), and SARIMA are external forecasting baselines. The fractional model has lower observed RMSE than the integer comparator at every horizon, while Persistence and SARIMA have lower observed RMSE than the fractional model throughout. Seasonal Naive has higher observed RMSE than the fractional model through $h=7$ and lower observed RMSE from $h=8$ onward. Comparisons are descriptive sample results for the evaluated origins; no inferential superiority is claimed.
* **FILE_AVAILABLE**: YES
* **RESOLUTION_VERIFIED**: YES
* **FORMAT_VERIFIED**: YES
* **ACTION_REQUIRED**: Include as Figure 1 in Main Manuscript.

---

### Figure 2 (FIG-02A & FIG-02B)
* **ID**: FIG-02A / FIG-02B (Paired Panel Figure)
* **MAIN_OR_SUPPLEMENTARY**: MAIN
* **FILE_NAME**: `F2a_skill_rmse_vs_horizon.png` & `F2b_skill_mae_vs_horizon.png`
* **CANONICAL_PATH**: `results_canonical/06_figures/F2a_skill_rmse_vs_horizon.png`, `results_canonical/06_figures/F2b_skill_mae_vs_horizon.png`
* **SCIENTIFIC_ROLE**: Relative forecasting skill of fractional SEIT against the three external baselines under RMSE (Panel A) and MAE (Panel B), with zero as the no-skill reference.
* **CLAIMS_SUPPORTED**: C02/C03 (negative observed skill versus persistence and SARIMA throughout); C04 (positive observed skill versus seasonal naive only for $h=1,\dots,7$); C11 boundary (descriptive, not inferential).
* **CLAIM-SAFE CAPTION**: **Figure 2.** Observed relative forecasting skill of Fractional SEIT against external baselines across 12 monthly lead horizons in the 13-origin expanding-window evaluation: (A) RMSE-based skill and (B) MAE-based skill. Skill above zero denotes lower observed error for Fractional SEIT than the named baseline; skill below zero denotes lower observed error for the baseline. Observed skill is negative relative to Persistence and SARIMA at all horizons and positive relative to Seasonal Naive only from $h=1$ through $h=7$. These are descriptive sample skill values; no predictive-accuracy significance test was prespecified or applied.
* **FILE_AVAILABLE**: YES
* **RESOLUTION_VERIFIED**: YES
* **FORMAT_VERIFIED**: YES
* **ACTION_REQUIRED**: Include as Figure 2 (two-panel figure) in Main Manuscript.

---

### Figure 3 (FIG-03)
* **ID**: FIG-03
* **MAIN_OR_SUPPLEMENTARY**: MAIN
* **FILE_NAME**: `F3_R0_near_equivalent_envelope.png`
* **CANONICAL_PATH**: `results_canonical/06_figures/F3_R0_near_equivalent_envelope.png`
* **SCIENTIFIC_ROLE**: Practical-identifiability envelope of the derived basic reproduction number $R_0$ across the $n=25$ near-equivalent admissible calibration solutions.
* **CLAIM_SUPPORTED**: C07 ($R_0 \in [1.1542,1.1892]$ and $R_0>1$ for all 25 admissible solutions).
* **CLAIM-SAFE CAPTION**: **Figure 3.** Practical-identifiability envelope of the derived basic reproduction number $R_0$ across the predefined near-equivalent admissible set ($n=25$, $\Delta\mathrm{RMSE}_{\mathrm{cal}}\le1.0\%$), shown relative to the threshold $R_0=1$. The observed admissible-set range is $1.1542$–$1.1892$. The displayed range is an empirical practical-identifiability envelope over calibration-equivalent solutions, **not** a confidence interval or Bayesian credible interval, and it does not describe the broader 33-member diagnostic pool.
* **FILE_AVAILABLE**: YES
* **RESOLUTION_VERIFIED**: YES
* **FORMAT_VERIFIED**: YES
* **ACTION_REQUIRED**: Include as Figure 3 in Main Manuscript.

---

### Figure S1 (FIG-04)
* **ID**: FIG-04
* **MAIN_OR_SUPPLEMENTARY**: SUPPLEMENTARY
* **FILE_NAME**: `F4_bias_vs_horizon.png`
* **CANONICAL_PATH**: `results_canonical/06_figures/F4_bias_vs_horizon.png`
* **SCIENTIFIC_ROLE**: Directional mean forecast bias across lead horizons $h=1,\dots,12$.
* **CLAIM_SUPPORTED**: Diagnostic context only; no independent paper-level claim.
* **CLAIM-SAFE CAPTION**: **Figure S1.** Mean directional forecast bias ($\hat y-y$) across 13 rolling origins as a function of monthly lead horizon. Negative values indicate underprediction. The figure provides diagnostic context for the shared tendency of evaluated models to under-track the surveillance trajectory and is not used as evidence of model-specific causal failure or forecasting superiority.
* **FILE_AVAILABLE**: YES
* **RESOLUTION_VERIFIED**: YES
* **FORMAT_VERIFIED**: YES
* **ACTION_REQUIRED**: Place in Supplementary Material as Figure S1.

---

## 3. Tables Specification

### Table 1 (TAB-02)
* **ID**: TAB-02
* **MAIN_OR_SUPPLEMENTARY**: MAIN
* **FILE_NAME**: `table_horizon_summary.csv`
* **CANONICAL_PATH**: `results_canonical/05_rolling_origin/table_horizon_summary.csv`
* **SCIENTIFIC_ROLE**: Empirical horizon summary metrics ($H_{\text{relax}}$, $H_{\text{strict-from-h1}}$, mean RMSE/MAE) across evaluated models/baselines.
* **CLAIMS_SUPPORTED**: C01-C04 and the negative-space boundary C05.
* **CLAIM-SAFE CAPTION**: **Table 1.** Summary of out-of-sample forecast errors and empirical skill-horizon descriptors across the 13 expanding rolling origins and $h=1,\dots,12$ months. $H_{\text{relax}}$ and $H_{\text{strict-from-h1}}$ are baseline-specific descriptive indices for this evaluation and must not be interpreted as intrinsic or biological predictability limits.
* **FILE_AVAILABLE**: YES
* **FORMAT_VERIFIED**: YES
* **ACTION_REQUIRED**: Embed as Table 1 in Main Manuscript.

---

### Table 2 (TAB-03)
* **ID**: TAB-03
* **MAIN_OR_SUPPLEMENTARY**: MAIN
* **FILE_NAME**: `table_R0_stability_summary.csv`
* **CANONICAL_PATH**: `results_canonical/03_R0_stability/table_R0_stability_summary.csv`
* **SCIENTIFIC_ROLE**: Derived $R_0$ distribution and Disease-Free Equilibrium local-stability classification across the predefined admissible set.
* **CLAIMS_SUPPORTED**: C07 and C08.
* **CLAIM-SAFE CAPTION**: **Table 2.** Derived $R_0$ practical-identifiability envelope and Disease-Free Equilibrium local-stability classification under Matignon's criterion for the predefined near-equivalent admissible set ($n=25$). The $R_0$ range is an empirical admissible-set envelope rather than a statistical uncertainty interval; the DFE classification is a property of the fitted dynamical systems in this set, not an empirical assertion about persistence of real-world tuberculosis transmission.
* **FILE_AVAILABLE**: YES
* **FORMAT_VERIFIED**: YES
* **ACTION_REQUIRED**: Embed as Table 2 in Main Manuscript.

---

### Table S1 (TAB-01 & Rolling Origin Detail)
* **ID**: TAB-01 / Rolling Detail
* **MAIN_OR_SUPPLEMENTARY**: SUPPLEMENTARY
* **FILE_NAME**: `table_long_open_loop.csv` & `table_forecasting_by_horizon.csv`
* **CANONICAL_PATH**: `results_canonical/04_long_open_loop/table_long_open_loop.csv`, `results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv`
* **SCIENTIFIC_ROLE**: Full horizon-specific RMSE, MAE, and bias values plus the separate 24-month long open-loop stress-test results.
* **CLAIM_SUPPORTED**: Numerical disclosure underlying C01 and Figure 1.
* **CAPTION REQUIREMENT**: Label the long-open-loop values explicitly as a **single-origin stress test** and keep them distinct from the 13-origin rolling-origin metrics.
* **FILE_AVAILABLE**: YES
* **FORMAT_VERIFIED**: YES
* **ACTION_REQUIRED**: Include as Table S1 in Supplementary Material without merging the two evaluation protocols into one metric block.

---

### Table S2 (Detailed Skill Data)
* **ID**: Detailed Skill Data
* **MAIN_OR_SUPPLEMENTARY**: SUPPLEMENTARY
* **FILE_NAME**: `table_skill_by_horizon.csv`
* **CANONICAL_PATH**: `results_canonical/05_rolling_origin/table_skill_by_horizon.csv`
* **SCIENTIFIC_ROLE**: Horizon-by-horizon observed skill values under RMSE and MAE across external comparators.
* **CLAIMS_SUPPORTED**: C02-C04; C11 boundary applies.
* **CAPTION REQUIREMENT**: State explicitly that skill values are descriptive sample comparisons and were not subjected to a prespecified predictive-accuracy significance test.
* **FILE_AVAILABLE**: YES
* **FORMAT_VERIFIED**: YES
* **ACTION_REQUIRED**: Include as Table S2 in Supplementary Material.

---

### Table S3 (TAB-05)
* **ID**: TAB-05
* **MAIN_OR_SUPPLEMENTARY**: SUPPLEMENTARY
* **FILE_NAME**: `table_full_profile_diagnostic.csv`
* **CANONICAL_PATH**: `results_canonical/02_identifiability/table_full_profile_diagnostic.csv`
* **SCIENTIFIC_ROLE**: Parameter values, calibration error, $R_0$, and DFE stability across all 33 points in the broader profile-objective diagnostic exploration.
* **CLAIM_SUPPORTED**: Boundary evidence for practical non-identifiability and for restricting C07/C08 to the 25-member admissible set.
* **CAPTION REQUIREMENT**: Describe this as a **profile-objective diagnostic exploration**, not a formal profile-likelihood confidence analysis. Explicitly distinguish the full 33-member diagnostic pool from the 25-member admissible set used for the primary $R_0$/DFE claims.
* **FILE_AVAILABLE**: YES
* **FORMAT_VERIFIED**: YES
* **ACTION_REQUIRED**: Include as Table S3 in Supplementary Material.

---

## 4. Claim-safety gate

```text
WITHIN_FAMILY_VS_EXTERNAL_LABELING = PASS
DESCRIPTIVE_VS_INFERENTIAL_SKILL_LABELING = PASS
HORIZON_DESCRIPTOR_BOUNDARY = PASS
R0_ENVELOPE_NOT_CI = PASS
DFE_MODEL_PROPERTY_BOUNDARY = PASS
PROFILE_OBJECTIVE_TERMINOLOGY = PASS
FIGURE_REGENERATION_REQUIRED = NO
TABLE_REGENERATION_REQUIRED = NO
```
