# Figure and Table Audit

This document provides a comprehensive audit of all canonical figures and tables in `results_canonical/` according to `manuscript_architecture/FIGURE_TABLE_ROLE_MAP.md`, specifying their scientific role, claims supported, manuscript placement, redundancy status, legibility, and caption readiness.

---

## Master Figure and Table Inventory

### Figures

#### FIG-01: F1_rmse_vs_horizon.png
* **ID**: FIG-01
* **FILE_NAME**: `F1_rmse_vs_horizon.png`
* **CANONICAL_SOURCE**: `results_canonical/06_figures/F1_rmse_vs_horizon.png`
* **ROLE**: Primary multi-model error evolution figure (Main Text).
* **SCIENTIFIC_QUESTION**: How does forecast RMSE evolve with lead horizon ($h = 1 \dots 12$) across all five evaluated models simultaneously?
* **CLAIM_SUPPORTED**: C01 (fractional < integer), C02 (fractional > persistence), C03 (fractional > SARIMA), C04 (fractional vs. seasonal naive crossover).
* **USED_IN_MANUSCRIPT**: Main Text, Results §3.1 and §3.2.
* **REDUNDANT**: NO
* **LEGIBILITY_ISSUE**: NO (high-contrast curves, distinct line styles, clear horizon axis).
* **CAPTION_READY**: YES (Distinguishes within-family comparison vs. integer from external statistical benchmarks).
* **ACTION_REQUIRED**: Embed in final formatted manuscript / supplementary bundle with explicit caption.

#### FIG-02A: F2a_skill_rmse_vs_horizon.png
* **ID**: FIG-02A
* **FILE_NAME**: `F2a_skill_rmse_vs_horizon.png`
* **CANONICAL_SOURCE**: `results_canonical/06_figures/F2a_skill_rmse_vs_horizon.png`
* **ROLE**: Primary forecast skill figure (RMSE metric) with skill=0 reference floor (Main Text).
* **SCIENTIFIC_QUESTION**: At which lead horizons does the fractional SEIT model exhibit positive vs. negative forecasting skill relative to persistence, seasonal naive, and SARIMA under RMSE?
* **CLAIM_SUPPORTED**: C02, C03 (negative throughout), C04 (positive $h=1\dots 7$, negative $h=8\dots 12$).
* **USED_IN_MANUSCRIPT**: Main Text, Results §3.2.
* **REDUNDANT**: NO (pairs with FIG-02B).
* **LEGIBILITY_ISSUE**: NO (prominent zero-skill baseline, clear legend, color-coded baselines).
* **CAPTION_READY**: YES (Clarifies descriptive nature of skill index and baseline-specific $h=7$ boundary).
* **ACTION_REQUIRED**: Include in main text alongside FIG-02B.

#### FIG-02B: F2b_skill_mae_vs_horizon.png
* **ID**: FIG-02B
* **FILE_NAME**: `F2b_skill_mae_vs_horizon.png`
* **CANONICAL_SOURCE**: `results_canonical/06_figures/F2b_skill_mae_vs_horizon.png`
* **ROLE**: Primary forecast skill figure (MAE metric) with skill=0 reference floor (Main Text).
* **SCIENTIFIC_QUESTION**: Does the relative forecasting skill pattern observed under RMSE replicate under Mean Absolute Error (MAE)?
* **CLAIM_SUPPORTED**: C02, C03, C04 (confirming metric concordance across RMSE and MAE).
* **USED_IN_MANUSCRIPT**: Main Text, Results §3.2.
* **REDUNDANT**: NO (demonstrates loss-function robustness).
* **LEGIBILITY_ISSUE**: NO.
* **CAPTION_READY**: YES.
* **ACTION_REQUIRED**: Include in main text paired as Figure 2 (panels A and B).

#### FIG-03: F3_R0_near_equivalent_envelope.png
* **ID**: FIG-03
* **FILE_NAME**: `F3_R0_near_equivalent_envelope.png`
* **CANONICAL_SOURCE**: `results_canonical/06_figures/F3_R0_near_equivalent_envelope.png`
* **ROLE**: Mechanistic practical-identifiability distribution figure (Main Text).
* **SCIENTIFIC_QUESTION**: What is the distribution and dispersion of the derived basic reproduction number $R_0$ across the $n=25$ near-equivalent calibration solutions relative to the epidemic threshold $R_0 = 1$?
* **CLAIM_SUPPORTED**: C07 ($R_0 \in [1.1542, 1.1892] > 1$ over admissible set).
* **USED_IN_MANUSCRIPT**: Main Text, Results §3.3.
* **REDUNDANT**: NO (essential visual evidence for mechanistic identifiability separation).
* **LEGIBILITY_ISSUE**: NO (clear threshold line at $R_0 = 1.0$, boxplot/points indicating median and IQR).
* **CAPTION_READY**: YES (Explicitly labels envelope as practical-identifiability range, not a confidence interval).
* **ACTION_REQUIRED**: Include in main text Results §3.3.

#### FIG-04: F4_bias_vs_horizon.png
* **ID**: FIG-04
* **FILE_NAME**: `F4_bias_vs_horizon.png`
* **CANONICAL_SOURCE**: `results_canonical/06_figures/F4_bias_vs_horizon.png`
* **ROLE**: Supplementary forecast bias diagnostic figure (Supplementary Material).
* **SCIENTIFIC_QUESTION**: Do the evaluated models exhibit systematic directional forecast bias, and does bias worsen across lead horizons?
* **CLAIM_SUPPORTED**: Methodological diagnostic context (all models underpredict during the post-2020 validation rise).
* **USED_IN_MANUSCRIPT**: Supplementary Material (cited in Methods §2.11 and Results §3.1).
* **REDUNDANT**: NO (provides explanatory diagnostic context).
* **LEGIBILITY_ISSUE**: NO.
* **CAPTION_READY**: YES.
* **ACTION_REQUIRED**: Place in Supplementary Material as Figure S1.

---

### Tables

#### TAB-01: table_long_open_loop.csv
* **ID**: TAB-01
* **CANONICAL_SOURCE**: `results_canonical/04_long_open_loop/table_long_open_loop.csv`
* **ROLE**: Main Text Summary Table (Results §3.1).
* **SCIENTIFIC_QUESTION**: What are the 24-month continuous open-loop simulation errors for fractional vs. integer SEIT?
* **CLAIM_SUPPORTED**: C01 (long open-loop half of within-family evidence).
* **USED_IN_MANUSCRIPT**: Results §3.1 (values reported in text; compact table candidate).
* **REDUNDANT**: NO.
* **LEGIBILITY_ISSUE**: NO (single clean comparison row).
* **CAPTION_READY**: YES (Must carry explicit `LONG_OPEN_LOOP_STRESS_TEST, single origin` label).
* **ACTION_REQUIRED**: Retain for main text table or in-text summary.

#### TAB-02: table_horizon_summary.csv
* **ID**: TAB-02
* **CANONICAL_SOURCE**: `results_canonical/05_rolling_origin/table_horizon_summary.csv`
* **ROLE**: Main Text Horizon Summary Table (Results §3.2).
* **SCIENTIFIC_QUESTION**: What are the empirical horizon summary metrics ($H_{\text{relax}}$, $H_{\text{strict-from-h1}}$) across all comparators?
* **CLAIM_SUPPORTED**: C01, C02, C03, C04, C05.
* **USED_IN_MANUSCRIPT**: Results §3.2 (values reported in text; 6-row compact table).
* **REDUNDANT**: NO.
* **LEGIBILITY_ISSUE**: NO.
* **CAPTION_READY**: YES.
* **ACTION_REQUIRED**: Include as Table 1 in main text.

#### TAB-03: table_R0_stability_summary.csv
* **ID**: TAB-03
* **CANONICAL_SOURCE**: `results_canonical/03_R0_stability/table_R0_stability_summary.csv`
* **ROLE**: Main Text Mechanistic Stability Summary Table (Results §3.3).
* **SCIENTIFIC_QUESTION**: What are the quantitative quantiles (Min, Q1, Median, Q3, Max) of $R_0$ and DFE stability classification across the admissible set?
* **CLAIM_SUPPORTED**: C07, C08.
* **USED_IN_MANUSCRIPT**: Results §3.3.
* **REDUNDANT**: NO.
* **LEGIBILITY_ISSUE**: NO.
* **CAPTION_READY**: YES.
* **ACTION_REQUIRED**: Include as Table 2 in main text (pairs with FIG-03).

#### TAB-04: table_forecasting_by_horizon.csv & table_skill_by_horizon.csv
* **ID**: TAB-04
* **CANONICAL_SOURCE**: `results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv`, `table_skill_by_horizon.csv`
* **ROLE**: Supplementary Data Tables (60 rows and 144 rows).
* **SCIENTIFIC_QUESTION**: What are the full horizon-by-horizon numerical RMSE, MAE, and skill values for all models across all 12 lead times?
* **CLAIM_SUPPORTED**: Underlying numerical data for FIG-01, FIG-02A, FIG-02B.
* **USED_IN_MANUSCRIPT**: Supplementary Material (cited in Results §3.1–3.2).
* **REDUNDANT**: NO (essential full numerical disclosure).
* **LEGIBILITY_ISSUE**: NO.
* **CAPTION_READY**: YES.
* **ACTION_REQUIRED**: Place in Supplementary Material as Tables S1 and S2.

#### TAB-05: table_full_profile_diagnostic.csv
* **ID**: TAB-05
* **CANONICAL_SOURCE**: `results_canonical/02_identifiability/table_full_profile_diagnostic.csv`
* **ROLE**: Supplementary Identifiability Diagnostic Table (33 solutions).
* **SCIENTIFIC_QUESTION**: What are the parameter values, calibration errors, $R_0$ values, and DFE stability for all 33 diagnostic profile probe points?
* **CLAIM_SUPPORTED**: Negative-space boundary support for C07 and C08 (defines non-admissible probe points).
* **USED_IN_MANUSCRIPT**: Supplementary Material (cited in Methods §2.6, Results §3.3, Discussion §4).
* **REDUNDANT**: NO.
* **LEGIBILITY_ISSUE**: NO.
* **CAPTION_READY**: YES.
* **ACTION_REQUIRED**: Place in Supplementary Material as Table S3.

#### TAB-06: table_model_contract_status.csv
* **ID**: TAB-06
* **CANONICAL_SOURCE**: `results_canonical/01_model_contract/table_model_contract_status.csv`
* **ROLE**: Internal Audit Reference Table.
* **SCIENTIFIC_QUESTION**: What fixed parameter bounds, initial condition definitions, and solver settings define the reproducible model contract?
* **CLAIM_SUPPORTED**: M01, M02.
* **USED_IN_MANUSCRIPT**: Fully articulated in Methods §2.2–2.4 text.
* **REDUNDANT**: NO (internal provenance artifact).
* **LEGIBILITY_ISSUE**: NO.
* **CAPTION_READY**: N/A.
* **ACTION_REQUIRED**: Preserve in repository for provenance audit; optional supplementary listing.

---

## Figure and Table Audit Summary

* **Main Text Figures**: 3 figures (Figure 1: FIG-01; Figure 2: FIG-02A/B; Figure 3: FIG-03).
* **Main Text Tables**: 2 tables (Table 1: TAB-02; Table 2: TAB-03).
* **Supplementary Figures**: 1 figure (Figure S1: FIG-04).
* **Supplementary Tables**: 3 tables (Table S1: TAB-01 / detailed rolling-origin; Table S2: detailed skill; Table S3: TAB-05 full profile).
* **Redundancy Count**: 0.
* **Blockers Found**: 0.
