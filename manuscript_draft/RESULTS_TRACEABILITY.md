# Results Traceability and Evidence Audit

This document provides complete paragraph-by-paragraph audit traceability for `manuscript_draft/RESULTS_DRAFT.md`, linking every reported finding, empirical comparison, numerical value, and boundary condition directly to frozen canonical artifacts in `results_canonical/` and approved architecture specifications in `manuscript_architecture/`.

---

## Paragraph-by-Paragraph Traceability Matrix

### P1 — Protocol orientation (Section 3.1, Paragraph 1)

* **PARAGRAPH_ID**: P1
* **FINDING**: Definition and separation of the two evaluation protocols: (1) 24-month single-origin long open-loop stress test (2021–2022) following 2001–2020 calibration ($N_{\text{cal}} = 240$), and (2) 13-origin expanding-window rolling-origin forecasting evaluation ($h = 1, \dots, 12$).
* **CLAIM_IDS**: M04 (methodological/descriptive)
* **CANONICAL_ARTIFACTS**:
  * `results_canonical/04_long_open_loop/table_long_open_loop.csv`
  * `results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv`
  * `FORECASTING_EVALUATION_REPORT.md` (Section 12)
* **EXACT ROWS/SUBSETS**: Protocol definitions and metadata; $N_{\text{cal}} = 240$, $N_{\text{val}} = 24$, 13 origins $\times$ 12 horizons.
* **EXACT NUMBERS USED**: $N_{\text{cal}} = 240$ months, 24-month validation period (2021-01 to 2022-12), 13 origins (2020-12 to 2021-12), 12 horizons ($h = 1, \dots, 12$).
* **PERMITTED_INTERPRETATION**: Procedural orientation explaining why single-origin stress testing and multi-origin rolling forecasting are structurally distinct and must not be numerically combined.
* **FORBIDDEN_INTERPRETATION**: No performance claims or numerical error comparisons in P1.
* **FIGURE/TABLE REFERENCES**: `table_long_open_loop.csv`, `table_forecasting_by_horizon.csv`
* **INFERENCE_BOUNDARY**: Descriptive protocol specification only.

---

### P2 / R1 — Fractional SEIT versus independently refitted integer SEIT (Section 3.1, Paragraph 2)

* **PARAGRAPH_ID**: P2 (R1)
* **FINDING**: The fractional SEIT formulation achieved lower observed errors than the independently refitted integer-order SEIT comparator across both evaluation protocols and at every evaluated rolling-origin horizon.
* **CLAIM_IDS**: C01 (`SUPPORTED_WITHIN_MODEL_FAMILY`)
* **CANONICAL_ARTIFACTS**:
  * `results_canonical/04_long_open_loop/table_long_open_loop.csv`
  * `results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv`
* **EXACT ROWS/SUBSETS**:
  * `table_long_open_loop.csv`: rows for `model=fractional` and `model=integer`.
  * `table_forecasting_by_horizon.csv`: fractional and integer rows across all 12 horizons.
* **EXACT NUMBERS USED**:
  * Long open-loop: fractional RMSE $= 1117.960$, MAE $= 953.230$, bias $= -851.150$; integer RMSE $= 1759.538$, MAE $= 1588.649$, bias $= -1588.649$.
  * Rolling-origin representative points:
    * $h = 1$: fractional RMSE $= 688.858$ vs. integer RMSE $= 1185.796$
    * $h = 6$: fractional RMSE $= 1138.323$ vs. integer RMSE $= 1770.697$
    * $h = 12$: fractional RMSE $= 1355.984$ vs. integer RMSE $= 2022.492$
* **PERMITTED_INTERPRETATION**: Consistent error reduction within the SEIT model family under fair, independent re-estimation of the integer comparator.
* **FORBIDDEN_INTERPRETATION**: Must not be described as "general forecasting superiority" or operational forecasting efficacy.
* **FIGURE/TABLE REFERENCES**: `table_long_open_loop.csv`, `table_forecasting_by_horizon.csv`, Figure F1.
* **INFERENCE_BOUNDARY**: Descriptive sample comparison over the evaluated origins/window.

---

### P3 / R2 — TURNING POINT: No positive skill versus persistence or SARIMA (Section 3.2, Paragraph 1)

* **PARAGRAPH_ID**: P3 (R2 / Turning Point)
* **FINDING**: Observed forecast skill of the fractional SEIT model was negative across all 12 evaluated lead horizons relative to persistence (random walk) and SARIMA ($H_{\text{relax}} = 0$, $H_{\text{strict-from-h1}} = 0$).
* **CLAIM_IDS**: C02 (`NOT_SUPPORTED`), C03 (`NOT_SUPPORTED`), C05 (`NOT_SUPPORTED`)
* **CANONICAL_ARTIFACTS**:
  * `results_canonical/05_rolling_origin/table_skill_by_horizon.csv`
  * `results_canonical/05_rolling_origin/table_horizon_summary.csv`
  * `results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv`
* **EXACT ROWS/SUBSETS**:
  * `table_skill_by_horizon.csv`: rows for `model=fractional` vs. `baseline=persistence` and `baseline=SARIMA` across $h = 1, \dots, 12$ (RMSE and MAE).
  * `table_horizon_summary.csv`: persistence and SARIMA rows ($H_{\text{relax}} = 0$, $H_{\text{strict-from-h1}} = 0$).
* **EXACT NUMBERS USED**:
  * $H_{\text{relax}} = 0$, $H_{\text{strict-from-h1}} = 0$ for persistence and SARIMA (both RMSE and MAE).
  * Representative RMSE values:
    * $h = 1$: fractional $688.858$ vs. persistence $389.702$ vs. SARIMA $535.547$
    * $h = 6$: fractional $1138.323$ vs. persistence $845.856$ vs. SARIMA $1022.421$
    * $h = 12$: fractional $1355.984$ vs. persistence $1152.958$ vs. SARIMA $1283.583$
* **PERMITTED_INTERPRETATION**: The within-family improvement does not generalize to persistence or SARIMA; both external baselines achieved lower error at every evaluated horizon.
* **FORBIDDEN_INTERPRETATION**: Never use "statistically significant"; never state fractional is "comparable" when skill is negative; never soften the turning point.
* **FIGURE/TABLE REFERENCES**: `table_skill_by_horizon.csv`, `table_horizon_summary.csv`, Figures F1, F2a, F2b.
* **INFERENCE_BOUNDARY**: Descriptive sample comparison over the 13 evaluated origins; formal inferential testing deferred.

---

### P4 / R3 — Bounded skill versus seasonal naive (Section 3.2, Paragraph 2)

* **PARAGRAPH_ID**: P4 (R3)
* **FINDING**: Observed forecast skill of the fractional SEIT model relative to seasonal naive ($\text{lag } 12$) was positive for lead times $h = 1, \dots, 7$ and negative for $h = 8, \dots, 12$ ($H_{\text{relax}} = 7$, $H_{\text{strict-from-h1}} = 7$).
* **CLAIM_IDS**: C04 (`SUPPORTED_ONLY_VS_SEASONAL_NAIVE`)
* **CANONICAL_ARTIFACTS**:
  * `results_canonical/05_rolling_origin/table_skill_by_horizon.csv`
  * `results_canonical/05_rolling_origin/table_horizon_summary.csv`
  * `results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv`
* **EXACT ROWS/SUBSETS**:
  * `table_skill_by_horizon.csv`: rows for `model=fractional` vs. `baseline=seasonal_naive_12` across $h = 1, \dots, 12$.
  * `table_horizon_summary.csv`: seasonal_naive_12 rows.
* **EXACT NUMBERS USED**:
  * $H_{\text{relax}} = 7$, $H_{\text{strict-from-h1}} = 7$ (for both RMSE and MAE).
  * Representative RMSE values:
    * $h = 1$: fractional $688.858$ vs. seasonal naive $1090.638$ (skill positive)
    * $h = 7$: fractional $1203.452$ vs. seasonal naive $1237.408$ (skill positive)
    * $h = 8$: fractional $1351.227$ vs. seasonal naive $1258.413$ (skill negative)
* **PERMITTED_INTERPRETATION**: Bounded positive skill against seasonal naive specifically for lead times up to 7 months in this evaluation.
* **FORBIDDEN_INTERPRETATION**: Do NOT state "the useful forecasting horizon is seven months" without baseline qualification; do NOT generalize to persistence or SARIMA.
* **FIGURE/TABLE REFERENCES**: `table_skill_by_horizon.csv`, `table_horizon_summary.csv`, Figures F2a, F2b.
* **INFERENCE_BOUNDARY**: Descriptive sample descriptor for this specific baseline/dataset/protocol.

---

### P5 / R4a — Weak individual parameter identifiability (Section 3.3, Paragraph 1)

* **PARAGRAPH_ID**: P5 (R4a)
* **FINDING**: Calibration solutions achieving near-identical calibration RMSE exhibit pronounced dispersion across individual kinetic rate parameters $\beta$, $\gamma$, and $d$, whereas fractional order $\alpha$ is sharply identified.
* **CLAIM_IDS**: C09 (`NOT_SUPPORTED`: parameters are precise rates)
* **CANONICAL_ARTIFACTS**:
  * `IDENTIFIABILITY_AUDIT_REPORT.md` (Sections 2–5)
  * `outputs/calibration/fractional_multiseed.csv`
  * `outputs/identifiability/profile_objective.csv`
* **EXACT ROWS/SUBSETS**: Multiseed ensemble (5 seeds) and 28 profile-objective runs across $\beta, \gamma, d, \alpha$.
* **EXACT NUMBERS USED**:
  * Calibration RMSE spread: $605.049$ to $610.388$ ($\text{CV} \approx 0.35\%$).
  * Parameter variations:
    * $\beta$ spread $\approx 5.4\times$ ($\text{CV} \approx 58.0\%$)
    * $\gamma$ spread $\approx 5.3\times$ ($\text{CV} \approx 59.9\%$)
    * $d$ spread $> 100\times$ ($\text{CV} \approx 82.2\%$)
    * $\alpha$ spread: range $0.9620$–$0.9640$ ($\text{CV} \approx 0.08\%$)
* **PERMITTED_INTERPRETATION**: Individual parameter estimates are weakly identified and must not be cited as precise epidemiological rates.
* **FORBIDDEN_INTERPRETATION**: Never report a single fitted $(\beta, \gamma, d)$ point estimate as a substantive epidemiological finding.
* **FIGURE/TABLE REFERENCES**: `IDENTIFIABILITY_AUDIT_REPORT.md`
* **INFERENCE_BOUNDARY**: Practical-identifiability analysis of the optimization surface over the calibration window.

---

### P6 / R4b — Predictive and R0-functional robustness (Section 3.3, Paragraph 2)

* **PARAGRAPH_ID**: P6 (R4b)
* **FINDING**: Weak individual parameter identifiability coexists with stable model predictions and a narrow, strictly above-unity practical-identifiability envelope for the composite derived functional $R_0$.
* **CLAIM_IDS**: C07 (`SUPPORTED`), M03 (`METHODOLOGICAL/DESCRIPTIVE`)
* **CANONICAL_ARTIFACTS**:
  * `results_canonical/03_R0_stability/table_R0_stability_summary.csv`
  * `IDENTIFIABILITY_AUDIT_REPORT.md` (Sections 4, 6)
  * `results_canonical/02_identifiability/table_full_profile_diagnostic.csv`
* **EXACT ROWS/SUBSETS**: `table_R0_stability_summary.csv` (`NEAR_EQUIVALENT_ADMISSIBLE_SET`, $n = 25$ solutions with $\Delta \text{RMSE}_{\text{cal}} \le 1.0\%$).
* **EXACT NUMBERS USED**:
  * Mean prediction CV: calibration $\approx 0.19\%$, validation $\approx 0.58\%$.
  * Admissible set: $n = 25$ solutions.
  * $R_0$ distribution: $\min = 1.1542$, $Q_1 = 1.1682$, $\text{median} = 1.1735$, $Q_3 = 1.1770$, $\max = 1.1892$ ($\text{IQR} = [1.1682, 1.1770]$).
* **PERMITTED_INTERPRETATION**: $R_0$ is functionally identifiable and robustly exceeds unity across near-equivalent solutions despite component parameter non-uniqueness.
* **FORBIDDEN_INTERPRETATION**: Never label the $R_0$ range as a confidence interval, credible interval, or population uncertainty interval. Do not conflate the 25-solution admissible set with the 33-solution diagnostic pool (which includes 2 probe points with $R_0 < 1$).
* **FIGURE/TABLE REFERENCES**: `table_R0_stability_summary.csv`, Figure F3, `table_full_profile_diagnostic.csv` (diagnostic negative reference).
* **INFERENCE_BOUNDARY**: Mathematical evaluation of the composite derived functional over the admissible solution set.

---

### P7 / R5 — DFE local instability across the admissible set (Section 3.3, Paragraph 3)

* **PARAGRAPH_ID**: P7 (R5)
* **FINDING**: The Disease-Free Equilibrium (DFE) is locally asymptotically unstable in all 25 solutions within the near-equivalent admissible set under the commensurate Caputo fractional Matignon criterion.
* **CLAIM_IDS**: C08 (`SUPPORTED`)
* **CANONICAL_ARTIFACTS**:
  * `results_canonical/03_R0_stability/table_R0_stability_summary.csv`
  * `results_canonical/02_identifiability/table_full_profile_diagnostic.csv`
* **EXACT ROWS/SUBSETS**: `table_R0_stability_summary.csv` row 2 (`NEAR_EQUIVALENT_ADMISSIBLE_SET`, $n = 25$).
* **EXACT NUMBERS USED**: $\text{DFE\_stable} = 0$, $\text{DFE\_unstable} = 25$, $\text{DFE\_ambiguous} = 0$ ($n = 25$).
* **PERMITTED_INTERPRETATION**: Mathematical property of the fitted dynamical model across the admissible set, dynamically consistent with $R_0 > 1$.
* **FORBIDDEN_INTERPRETATION**: Must NOT be stated as an empirical proof of real-world persistent transmission in Brazil; must NOT be generalized to the full 33-solution diagnostic pool; must NOT be linked to forecasting performance.
* **FIGURE/TABLE REFERENCES**: `table_R0_stability_summary.csv`, `table_full_profile_diagnostic.csv` (negative reference).
* **INFERENCE_BOUNDARY**: Mathematical stability classification of the linearized fractional dynamical system at the DFE.

---

## Quality Gate Verification Summary

1. **P3 is visibly the central turning point**: Confirmed.
2. **C01 is always bounded to within-family comparison**: Confirmed.
3. **Negative skill vs persistence/SARIMA is stated directly**: Confirmed.
4. **Seasonal-naive skill is bounded to $h = 1 \dots 7$**: Confirmed.
5. **$\beta, \gamma, d$ are never presented as precise epidemiological rates**: Confirmed.
6. **$R_0$ range is never called a CI / credible interval**: Confirmed (designated "practical-identifiability envelope").
7. **$n = 25$ admissible set is never mixed with $n = 33$ diagnostic pool**: Confirmed.
8. **DFE result remains a model property**: Confirmed (not asserted as an empirical truth about Brazil).
9. **No statistical significance language appears**: Confirmed (all metrics descriptive).
10. **No Discussion-level causal explanations**: Confirmed.
11. **No external unverified literature claims**: Confirmed.
12. **No historical ~48% optimal control claims**: Confirmed.
