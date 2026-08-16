# Bulletin of Mathematical Biology — Figure and Table Submission Package

This document specifies the complete inventory of main text and supplementary figures and tables prepared for submission to the *Bulletin of Mathematical Biology*, verifying scientific roles, claim support, editorial relevance, formatting readiness, and file locations.

---

## 1. Package Inventory Summary

```text
MAIN_FIGURES_COUNT = 3
MAIN_TABLES_COUNT = 2
SUPPLEMENTARY_FIGURES_COUNT = 1
SUPPLEMENTARY_TABLES_COUNT = 3
REDUNDANT_ITEMS_COUNT = 0
TOTAL_ITEMS = 9
FIGURE_TABLE_STATUS = COMPLETE_AND_VERIFIED
```

---

## 2. Figures Specification

### Figure 1 (FIG-01)
* **ID**: FIG-01
* **MAIN_OR_SUPPLEMENTARY**: MAIN
* **FILE_NAME**: `F1_rmse_vs_horizon.png`
* **CANONICAL_PATH**: `results_canonical/06_figures/F1_rmse_vs_horizon.png`
* **SCIENTIFIC_ROLE**: Multi-model forecast error trajectory across lead horizons $h = 1 \dots 12\text{ months}$.
* **CLAIM_SUPPORTED**: C01 (fractional < integer), C02 (fractional > persistence), C03 (fractional > SARIMA), C04 (seasonal naive crossover).
* **BMB_RELEVANCE**: Direct graphical proof of within-family reduction versus external baseline underperformance.
* **CAPTION_READY**: YES ("Root Mean Squared Error (RMSE) across 12 forecast horizons for Fractional SEIT, Integer SEIT, Persistence, Seasonal Naive, and SARIMA models across 13 rolling origins...")
* **FILE_AVAILABLE**: YES
* **RESOLUTION_VERIFIED**: YES (High DPI PNG, clear vector-like line distinctions).
* **FORMAT_VERIFIED**: YES (PNG, RGB, standard Springer format compatible; EPS/PDF exportable).
* **ACTION_REQUIRED**: Include as Figure 1 in Main Manuscript.

---

### Figure 2 (FIG-02A & FIG-02B)
* **ID**: FIG-02A / FIG-02B (Paired Panel Figure)
* **MAIN_OR_SUPPLEMENTARY**: MAIN
* **FILE_NAME**: `F2a_skill_rmse_vs_horizon.png` & `F2b_skill_mae_vs_horizon.png`
* **CANONICAL_PATH**: `results_canonical/06_figures/F2a_skill_rmse_vs_horizon.png`, `F2b_skill_mae_vs_horizon.png`
* **SCIENTIFIC_ROLE**: Relative forecasting skill index across horizons under RMSE (Panel A) and MAE (Panel B) relative to zero-skill baseline floor.
* **CLAIM_SUPPORTED**: C02, C03 (negative skill throughout), C04 (positive skill only $h=1\dots 7$), C05 (loss function robustness).
* **BMB_RELEVANCE**: Essential visual demonstration of the central turning point: negative skill against persistence and SARIMA, with bounded seasonal naive exception.
* **CAPTION_READY**: YES ("Out-of-sample relative forecasting skill of the Fractional SEIT model against external statistical baselines across 12 monthly lead horizons. (A) Skill under RMSE metric. (B) Skill under MAE metric...")
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
* **SCIENTIFIC_ROLE**: Practical-identifiability distribution of derived basic reproduction number $R_0$ across the $n=25$ near-equivalent calibration solutions.
* **CLAIM_SUPPORTED**: C07 ($R_0 \in [1.1542, 1.1892] > 1.0$ over admissible set).
* **BMB_RELEVANCE**: Visualizes functional parameter compensation where weak individual parameter identifiability yields a tight dynamical threshold envelope.
* **CAPTION_READY**: YES ("Practical-identifiability envelope of the derived basic reproduction number $R_0$ across the $n = 25$ near-equivalent calibration solutions ($\Delta\text{RMSE}_{\text{cal}} \le 1.0\%$) relative to the epidemic threshold $R_0 = 1.0$...")
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
* **SCIENTIFIC_ROLE**: Directional mean forecast bias evolution across lead horizons $h = 1 \dots 12$.
* **CLAIM_SUPPORTED**: Diagnostic context for post-2020 surveillance trajectory underestimation.
* **BMB_RELEVANCE**: Provides diagnostic completeness for model validation behavior.
* **CAPTION_READY**: YES ("Mean directional forecast bias ($\hat{y} - y$) as a function of lead horizon $h$ across 13 rolling origins...")
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
* **SCIENTIFIC_ROLE**: Comprehensive empirical horizon summary metrics ($H_{\text{relax}}$, $H_{\text{strict-from-h1}}$, mean RMSE/MAE) across all evaluated models.
* **CLAIM_SUPPORTED**: C01, C02, C03, C04, C05.
* **BMB_RELEVANCE**: Core quantitative table summarizing multi-horizon forecasting behavior across all comparative models.
* **CAPTION_READY**: YES ("Summary of out-of-sample forecast accuracy and empirical skill horizons across 13 expanding rolling origins ($h = 1 \dots 12\text{ months}$)...")
* **FILE_AVAILABLE**: YES
* **RESOLUTION_VERIFIED**: N/A (Text / CSV)
* **FORMAT_VERIFIED**: YES (Clean markdown / LaTeX table ready).
* **ACTION_REQUIRED**: Embed as Table 1 in Main Manuscript.

---

### Table 2 (TAB-03)
* **ID**: TAB-03
* **MAIN_OR_SUPPLEMENTARY**: MAIN
* **FILE_NAME**: `table_R0_stability_summary.csv`
* **CANONICAL_PATH**: `results_canonical/03_R0_stability/table_R0_stability_summary.csv`
* **SCIENTIFIC_ROLE**: Quantitative distribution of derived basic reproduction number $R_0$ and Disease-Free Equilibrium stability classification across admissible set.
* **CLAIM_SUPPORTED**: C07, C08.
* **BMB_RELEVANCE**: Quantitative confirmation of functional robustness and Matignon equilibrium instability ($25/25$ unstable).
* **CAPTION_READY**: YES ("Summary of derived basic reproduction number $R_0$ and Disease-Free Equilibrium (DFE) local stability under Matignon's criterion across the near-equivalent admissible calibration set ($n = 25$)...")
* **FILE_AVAILABLE**: YES
* **RESOLUTION_VERIFIED**: N/A (Text / CSV)
* **FORMAT_VERIFIED**: YES (Clean markdown / LaTeX table ready).
* **ACTION_REQUIRED**: Embed as Table 2 in Main Manuscript.

---

### Table S1 (TAB-01 & Rolling Origin Detail)
* **ID**: TAB-01 / Rolling Detail
* **MAIN_OR_SUPPLEMENTARY**: SUPPLEMENTARY
* **FILE_NAME**: `table_long_open_loop.csv` & `table_forecasting_by_horizon.csv`
* **CANONICAL_PATH**: `results_canonical/04_long_open_loop/table_long_open_loop.csv`, `results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv`
* **SCIENTIFIC_ROLE**: Full horizon-by-horizon numerical RMSE, MAE, and bias values for all 5 models across all 12 lead times, plus 24-month long open-loop stress test results.
* **CLAIM_SUPPORTED**: Full numerical disclosure underlying Figure 1.
* **BMB_RELEVANCE**: Methodological transparency for replication.
* **CAPTION_READY**: YES
* **FILE_AVAILABLE**: YES
* **RESOLUTION_VERIFIED**: N/A
* **FORMAT_VERIFIED**: YES
* **ACTION_REQUIRED**: Include as Table S1 in Supplementary Material.

---

### Table S2 (Detailed Skill Data)
* **ID**: Detailed Skill Data
* **MAIN_OR_SUPPLEMENTARY**: SUPPLEMENTARY
* **FILE_NAME**: `table_skill_by_horizon.csv`
* **CANONICAL_PATH**: `results_canonical/05_rolling_origin/table_skill_by_horizon.csv`
* **SCIENTIFIC_ROLE**: Detailed horizon-by-horizon numerical skill values under RMSE and MAE across all comparators.
* **CLAIM_SUPPORTED**: Full numerical disclosure underlying Figure 2.
* **BMB_RELEVANCE**: Methodological transparency.
* **CAPTION_READY**: YES
* **FILE_AVAILABLE**: YES
* **RESOLUTION_VERIFIED**: N/A
* **FORMAT_VERIFIED**: YES
* **ACTION_REQUIRED**: Include as Table S2 in Supplementary Material.

---

### Table S3 (TAB-05)
* **ID**: TAB-05
* **MAIN_OR_SUPPLEMENTARY**: SUPPLEMENTARY
* **FILE_NAME**: `table_full_profile_diagnostic.csv`
* **CANONICAL_PATH**: `results_canonical/02_identifiability/table_full_profile_diagnostic.csv`
* **SCIENTIFIC_ROLE**: Complete parameter values, calibration error, $R_0$, and DFE stability across all 33 profile diagnostic exploration points.
* **CLAIM_SUPPORTED**: Parameter non-identifiability negative space and boundary analysis.
* **BMB_RELEVANCE**: Provides full mathematical audit of optimization landscape and profile likelihood sweeps.
* **CAPTION_READY**: YES
* **FILE_AVAILABLE**: YES
* **RESOLUTION_VERIFIED**: N/A
* **FORMAT_VERIFIED**: YES
* **ACTION_REQUIRED**: Include as Table S3 in Supplementary Material.
