# Methods Traceability and Precedence Audit

This document provides subsection-by-subsection audit traceability for `manuscript_draft/METHODS_DRAFT.md`, linking every methodological description, mathematical formulation, configuration parameter, and constraint directly to canonical artifacts, contracts, and source code in the repository.

---

## Global Documentary Precedence Record

```text
DOCUMENTARY_PRECEDENCE_NOTE:
docs/MODEL_CONTRACT.md contains earlier/placeholder values for demographic mortality mu (1/(75*12))
and gamma bounds ([0.01, 0.50]).

Canonical drafting values are taken from:
docs/EXTERNAL_PARAMETER_CONTRACT.md
+ src/tb_seit/constants.py
+ scripts/run_calibration_multiseed.py
+ results_canonical/01_model_contract/table_model_contract_status.csv

Specifically:
- mu = 1 / (74 * 12) ≈ 0.001126 month^-1 (IBGE life expectancy anchor ~74 years)
- gamma bounds = [0.05, 0.30] month^-1 (primary search range anchored to WHO 6-month regimen + Brazilian diagnostic delays)

This discrepancy is a documented superseded-document issue (SUPERSEDED_DOCUMENTATION) and does not represent an inconsistency in the frozen evidence or scientific code.
```

---

## Subsection-by-Subsection Traceability

### 2.1 Study design and independent-reimplementation scope

* **SUBSECTION**: 2.1 Study design and independent-reimplementation scope
* **PURPOSE**: State study objectives, define the scope as an independent reimplementation and methodological audit, declare unrecoverability of historical code, articulate the two-tier dominant research question, and establish boundaries regarding optimal control.
* **SOURCE FILES**:
  * `PROJECT_CANON.md` (Sections 1–3)
  * `REPRODUCIBILITY_STATUS.md` (Stage summary)
  * `manuscript_architecture/MANUSCRIPT_EVIDENCE_ARCHITECTURE.md` (Sections 1, 2, 4.1)
  * `docs/METHOD_DECISION_LOG.md` (D001–D007, D032)
* **IMPLEMENTATION FILES CHECKED**:
  * `src/tb_seit/__init__.py`
  * `results_canonical/01_model_contract/table_model_contract_status.csv`
* **KEY CONFIGURATION VALUES USED**:
  * `REPRODUCTION_MODE = INDEPENDENT_REIMPLEMENTATION`
  * `historical manuscript = REFERENCE_ONLY_NOT_EVIDENCE`
  * `OPTIMAL_CONTROL = DEFERRED_NOT_VERIFIED`
* **ASSUMPTIONS**:
  * Historical manuscript cannot be reproduced numerically without unverified post-hoc reverse engineering; independent specification is required.
* **DOCUMENTATION GAPS**:
  * BLOCKING: None.
  * NON_BLOCKING: Exact historical compiler / solver environment remains permanently unrecoverable (declared by design).
* **CLAIM-BOUNDARY RISKS**:
  * Must not claim exact replication of historical findings.
  * Must not imply historical ~48% optimal control reduction is verified.
* **PRECEDENCE NOTES**: None.

---

### 2.2 Data and observation mapping

* **SUBSECTION**: 2.2 Data and observation mapping
* **PURPOSE**: Document the empirical data series, temporal partitioning, population denominator handling, and the critical flow-based observation model mapping.
* **SOURCE FILES**:
  * `DATA_PROVENANCE.md`
  * `docs/MODEL_CONTRACT.md` (Sections 1, 2, 6)
  * `docs/EXTERNAL_PARAMETER_CONTRACT.md` (Sections 2, 3)
  * `docs/METHOD_DECISION_LOG.md` (D001, D002, D009, D016)
  * `results_canonical/01_model_contract/table_model_contract_status.csv`
* **IMPLEMENTATION FILES CHECKED**:
  * `src/tb_seit/data.py` (`load_canonical_dataset`, date range assertions)
  * `src/tb_seit/population.py` (`build_population_exogenous_series`, `fit_population_trend`)
  * `src/tb_seit/model.py` (`simulate`, `flow_model = diff(C)`)
  * `tests/test_repository_integrity.py`
* **KEY CONFIGURATION VALUES USED**:
  * $N = 264$ monthly observations (2001-01 to 2022-12)
  * Calibration window: 2001-01 to 2020-12 ($N_{\text{cal}} = 240$)
  * Validation window: 2021-01 to 2022-12 ($N_{\text{val}} = 24$)
  * Population $N(t)$: Observed for 2001–2020; log-linear extrapolation for 2021–2022.
  * Observation equation: $\hat{y}_k = C(t_{k+1}) - C(t_k)$ with $^C D_t^\alpha C = \tau_0^{1-\alpha} \sigma E(t)$.
* **ASSUMPTIONS**:
  * Monthly SINAN notifications represent incidence flow ($E \to I$), not the standing stock $I(t)$.
  * Validation population extrapolation eliminates post-2022 census retrospective leakage risk.
* **DOCUMENTATION GAPS**:
  * BLOCKING: None.
  * NON_BLOCKING: Exact IBGE table provenance of the original `populacao` column is unrecorded in `DATA_PROVENANCE.md`, but fully neutralized by the log-linear train-only extrapolation rule (`PROVENANCE_REQUIRED` fallback).
* **CLAIM-BOUNDARY RISKS**:
  * Guard against stating monthly cases observe $I(t)$ directly.
* **PRECEDENCE NOTES**:
  * Supersedes any naive stock-interpretation assumption.

---

### 2.3 Fractional SEIT formulation

* **SUBSECTION**: 2.3 Fractional SEIT formulation
* **PURPOSE**: State the complete mathematical system of fractional differential equations, Caputo derivative operator, reference-time scaling, state definitions, non-free initial condition derivations, and parameter bounds.
* **SOURCE FILES**:
  * `docs/MODEL_CONTRACT.md` (Sections 3–5)
  * `docs/EXTERNAL_PARAMETER_CONTRACT.md` (Sections 2, 4)
  * `docs/FRACTIONAL_DIMENSIONAL_CONSISTENCY.md` (Phases 1–5)
  * `docs/METHOD_DECISION_LOG.md` (D010, D012, D014, D015, D017, D018, D019, D028)
* **IMPLEMENTATION FILES CHECKED**:
  * `src/tb_seit/model.py` (`SeitParameters`, `initial_conditions`, `seit_rhs`)
  * `src/tb_seit/constants.py` (`compute_mu`, `compute_lambda`, `ModelConstants`)
  * `src/tb_seit/dimensional_audit.py`
  * `tests/test_dimensional_audit.py`
  * `tests/test_seit_model.py`
* **KEY CONFIGURATION VALUES USED**:
  * Reference timescale: $\tau_0 = 1.0\text{ month}$ ($\tau_0^{1-\alpha} = 1.0$)
  * Demographic mortality: $\mu = 1/(74 \times 12) \approx 0.001126\text{ month}^{-1}$
  * Demographic recruitment: $\Lambda = \mu \bar{N}_{\text{cal}}$
  * Parameter search bounds:
    * $\beta \in [0.01, 1.00]\text{ month}^{-1}$
    * $\sigma \in [0.01, 0.50]\text{ month}^{-1}$
    * $\gamma \in [0.05, 0.30]\text{ month}^{-1}$ (primary; $[0.01, 0.50]$ sensitivity)
    * $d \in [0.0001, 0.05]\text{ month}^{-1}$
    * $\alpha \in [0.50, 1.00]$ (primary; $[0.70, 1.00]$ sensitivity)
  * Initial conditions: $E(0) = y_0/\sigma$, $I(0) = y_0/(\gamma+\mu+d)$, $T(0) = 0$, $S(0) = N(t_0) - E(0) - I(0)$, $C(0) = 0$.
* **ASSUMPTIONS**:
  * Exponential residence times within compartments; single-compartment $E$ represents a simplified average progression.
  * T-compartment is defined as completed/removed.
* **DOCUMENTATION GAPS**:
  * BLOCKING: None.
  * NON_BLOCKING: Single-compartment $E$ cannot simultaneously fit fast and slow TB progression pathways (`STRUCTURAL_LIMITATION_TO_DECLARE`).
* **CLAIM-BOUNDARY RISKS**:
  * Reference-time scaling must be presented as mathematical dimensional consistency, not a post-hoc tuning factor.
  * $\alpha < 1$ must not be equated to proof of biological memory.
* **PRECEDENCE NOTES**:
  * `DOCUMENTARY_PRECEDENCE_NOTE`: $\mu = 1/(74 \times 12)$ and $\gamma \in [0.05, 0.30]$ supersede `docs/MODEL_CONTRACT.md` placeholders per `docs/EXTERNAL_PARAMETER_CONTRACT.md`.

---

### 2.4 Numerical solution and calibration

* **SUBSECTION**: 2.4 Numerical solution and calibration
* **PURPOSE**: Describe the Diethelm–Ford–Freed PECE solver, integration step size $h$, Differential Evolution calibration configuration, objective function, and random seed protocol.
* **SOURCE FILES**:
  * `docs/MODEL_CONTRACT.md` (Sections 7, 8)
  * `docs/METHOD_DECISION_LOG.md` (D020, D021, D024)
* **IMPLEMENTATION FILES CHECKED**:
  * `src/tb_seit/solver.py` (`solve_caputo_fde`)
  * `src/tb_seit/calibration.py` (`run_differential_evolution`, `STRATEGY`, `POPSIZE`, `MUTATION`, `RECOMBINATION`, `TOL`, `MAXITER`)
  * `src/tb_seit/seeds.py` (`PRIMARY_SEED`, `DIAGNOSTIC_SEEDS`)
  * `scripts/run_calibration_multiseed.py`
  * `tests/test_optimization_contract.py`
  * `tests/test_seed_contract.py`
* **KEY CONFIGURATION VALUES USED**:
  * Solver: Diethelm–Ford–Freed fractional Adams–Bashforth–Moulton PECE
  * Step size: $h = 1.0\text{ month}$
  * DE strategy: `best1bin`, popsize=15, mutation=(0.5, 1.0), recombination=0.7, tol=0.01, maxiter=1000, polish=False
  * Calibration objective: Calibration-window flow RMSE
  * Primary seed: `20260815`
  * Diagnostic seeds: `20260816`, `20260817`, `20260818`, `20260819`
* **ASSUMPTIONS**:
  * Step size $h=1.0$ provides sufficient accuracy based on pre-calibration convergence audit (<0.51% relative error vs $h=0.25$).
* **DOCUMENTATION GAPS**:
  * BLOCKING: None.
  * NON_BLOCKING: None.
* **CLAIM-BOUNDARY RISKS**:
  * No calibration outcome numbers (e.g. fitted RMSE or parameters) in Methods.
* **PRECEDENCE NOTES**: None.

---

### 2.5 Integer-order comparator

* **SUBSECTION**: 2.5 Integer-order comparator
* **PURPOSE**: Specify the integer-order SEIT benchmark ($\alpha = 1.0$) and establish the principle of fair independent re-estimation.
* **SOURCE FILES**:
  * `docs/MODEL_CONTRACT.md` (Section 9)
  * `docs/METHOD_DECISION_LOG.md` (D011)
  * `manuscript_architecture/MANUSCRIPT_EVIDENCE_ARCHITECTURE.md` (Section 4.1)
* **IMPLEMENTATION FILES CHECKED**:
  * `src/tb_seit/calibration.py` (`fixed_alpha=1.0`)
  * `scripts/run_calibration_multiseed.py` (`BOUNDS_INTEGER`)
  * `tests/test_seit_model.py`
* **KEY CONFIGURATION VALUES USED**:
  * $\alpha \equiv 1.0$
  * Free parameters: $(\beta, \sigma, \gamma, d)$
  * Identical DE configuration, bounds, and calibration objective
* **ASSUMPTIONS**:
  * Fair comparison requires independent re-estimation of integer parameters rather than reusing fractional parameters.
* **DOCUMENTATION GAPS**:
  * BLOCKING: None.
  * NON_BLOCKING: None.
* **CLAIM-BOUNDARY RISKS**:
  * Prevent describing the integer model as the fractional model with $\alpha$ set to 1 without refitting.
* **PRECEDENCE NOTES**: None.

---

### 2.6 Practical-identifiability analysis

* **SUBSECTION**: 2.6 Practical-identifiability analysis
* **PURPOSE**: Detail the protocol for evaluating parameter, predictive, and functional identifiability, including the multiseed ensemble, profile-objective sweeps, and definition of the near-equivalent admissible set.
* **SOURCE FILES**:
  * `IDENTIFIABILITY_AUDIT_REPORT.md` (Sections 1–6)
  * `docs/METHOD_DECISION_LOG.md` (D025, D026)
  * `results_canonical/02_identifiability/table_full_profile_diagnostic.csv`
* **IMPLEMENTATION FILES CHECKED**:
  * `scripts/parameter_robustness_and_kill_test.py`
  * `tests/test_identifiability.py`
* **KEY CONFIGURATION VALUES USED**:
  * Near-equivalent admissibility condition: $\Delta \text{RMSE}_{\text{cal}} \le 1.0\%$
  * Multiseed set: 5 seeds
  * Profile grid: 28 profile evaluations across $\beta, \gamma, d, \alpha$
  * Total explored profile pool: $n = 33$ solutions ($n = 25$ admissible)
* **ASSUMPTIONS**:
  * A 1% calibration RMSE degradation threshold captures the practical flatness of the objective surface.
* **DOCUMENTATION GAPS**:
  * BLOCKING: None.
  * NON_BLOCKING: None.
* **CLAIM-BOUNDARY RISKS**:
  * The admissible set must NOT be described as a confidence interval, credible interval, or formal uncertainty region.
  * No numerical parameter dispersion or $R_0$ outcome numbers reported in Methods.
* **PRECEDENCE NOTES**: None.

---

### 2.7 Basic reproduction number and local stability

* **SUBSECTION**: 2.7 Basic reproduction number and local stability
* **PURPOSE**: Present the Next-Generation Matrix derivation of $R_0$, prove dimensional and $\alpha$-invariance under reference-time scaling, and define the fractional Matignon local stability condition for the DFE.
* **SOURCE FILES**:
  * `R0_STABILITY_ANALYSIS_NOTE.md` (Parts A, C)
  * `docs/FRACTIONAL_DIMENSIONAL_CONSISTENCY.md` (Phases 3–5)
  * `docs/METHOD_DECISION_LOG.md` (D027, D028)
  * `results_canonical/03_R0_stability/table_R0_stability_summary.csv`
* **IMPLEMENTATION FILES CHECKED**:
  * `src/tb_seit/r0.py` (`r0_diagnostic`)
  * `src/tb_seit/dimensional_audit.py` (`r0_scaling_invariance`, `matignon_stability`)
  * `tests/test_r0_stability.py`
* **KEY CONFIGURATION VALUES USED**:
  * $R_0 = \frac{\beta \sigma}{(\sigma + \mu)(\gamma + \mu + d)}$
  * Matignon condition: $|\arg(\lambda_i)| > \alpha \frac{\pi}{2}$ evaluated at DFE with individual fitted $\alpha$
* **ASSUMPTIONS**:
  * Standard DFE linearization; standard Caputo fractional stability criteria apply.
* **DOCUMENTATION GAPS**:
  * BLOCKING: None.
  * NON_BLOCKING: None.
* **CLAIM-BOUNDARY RISKS**:
  * Do not state the empirical 25/25 DFE instability result here (belongs in Results R5).
  * Stability must be formulated as a mathematical property of the model over the admissible set, not a direct epidemiological assertion about Brazil.
* **PRECEDENCE NOTES**: None.

---

### 2.8 Long open-loop stress test

* **SUBSECTION**: 2.8 Long open-loop stress test
* **PURPOSE**: Specify the single-origin 24-month continuous open-loop simulation protocol on the validation period.
* **SOURCE FILES**:
  * `docs/MODEL_CONTRACT.md` (Section 10)
  * `docs/METHOD_DECISION_LOG.md` (D013, D025)
  * `results_canonical/04_long_open_loop/table_long_open_loop.csv`
* **IMPLEMENTATION FILES CHECKED**:
  * `scripts/run_validation.py`
  * `tests/test_seit_model.py`
* **KEY CONFIGURATION VALUES USED**:
  * Calibration: 2001-01 to 2020-12 ($N_{\text{cal}} = 240$)
  * Validation: 2021-01 to 2022-12 ($N_{\text{val}} = 24$)
  * Continuous integration without resetting or data assimilation
* **ASSUMPTIONS**:
  * Serves as a single-origin long-horizon stability stress test; distinct from rolling-origin forecasting.
* **DOCUMENTATION GAPS**:
  * BLOCKING: None.
  * NON_BLOCKING: None.
* **CLAIM-BOUNDARY RISKS**:
  * Do not mix single-origin long open-loop metrics with rolling-origin metrics.
  * No numerical outcomes in Methods.
* **PRECEDENCE NOTES**: None.

---

### 2.9 Rolling-origin forecasting evaluation

* **SUBSECTION**: 2.9 Rolling-origin forecasting evaluation
* **PURPOSE**: Define the expanding-window rolling-origin cross-validation protocol, origins, horizons, SEIT recalibration policy, and strict leakage prevention rules.
* **SOURCE FILES**:
  * `FORECASTING_EVALUATION_REPORT.md` (Sections 1–4)
  * `docs/METHOD_DECISION_LOG.md` (D029)
  * `results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv`
* **IMPLEMENTATION FILES CHECKED**:
  * `src/tb_seit/rolling_origin.py` (`ORIGINS`, `HORIZONS`, `build_training_set`, `fit_origin_population_trend`, `simulate_forecast`)
  * `scripts/run_rolling_origin_evaluation.py`
  * `tests/test_rolling_origin.py`
* **KEY CONFIGURATION VALUES USED**:
  * 13 monthly origins: 2020-12 through 2021-12
  * Lead horizons: $h = 1, 2, \dots, 12$ months
  * Fully crossed grid: $13 \times 12 = 156$ targets (780 model-horizon predictions across 5 models)
  * SEIT fit policy: 1 DE fit per origin per model family (13 fractional + 13 integer = 26 fits); 12 horizons generated in open loop from each origin fit
  * Primary seed: `20260815`
* **ASSUMPTIONS**:
  * Expanding window mirrors real-time surveillance operations.
* **DOCUMENTATION GAPS**:
  * BLOCKING: None.
  * NON_BLOCKING: None.
* **CLAIM-BOUNDARY RISKS**:
  * Leakage controls must be described procedurally, not as an empirical result.
* **PRECEDENCE NOTES**: None.

---

### 2.10 External forecasting baselines

* **SUBSECTION**: 2.10 External forecasting baselines
* **PURPOSE**: Define the mathematical formulation of the three external forecasting benchmarks: Persistence, Seasonal Naive (lag 12), and SARIMA, including the train-only a priori SARIMA order selection.
* **SOURCE FILES**:
  * `docs/SARIMA_BASELINE_CONTRACT.md`
  * `FORECASTING_EVALUATION_REPORT.md` (Section 3)
  * `docs/METHOD_DECISION_LOG.md` (D029)
* **IMPLEMENTATION FILES CHECKED**:
  * `src/tb_seit/rolling_origin.py` (`persistence_forecast`, `seasonal_naive_forecast`)
  * `scripts/select_sarima_order.py`
  * `outputs/forecasting/sarima_frozen_order.json`
  * `tests/test_rolling_origin.py`
* **KEY CONFIGURATION VALUES USED**:
  * Persistence: $\hat{y}_{t_{\text{orig}}+h} = y_{t_{\text{orig}}}$
  * Seasonal Naive: $\hat{y}_{t_{\text{orig}}+h} = y_{t_{\text{orig}}+h-12}$
  * SARIMA frozen order: $\text{SARIMA}(0, 1, 2)(1, 1, 1)_{12}$ (selected via 36-model AIC grid on 2001–2020 data only; coefficients refitted per origin)
* **ASSUMPTIONS**:
  * SARIMA order selection on train-only data prevents lookahead bias.
* **DOCUMENTATION GAPS**:
  * BLOCKING: None.
  * NON_BLOCKING: None.
* **CLAIM-BOUNDARY RISKS**:
  * SARIMA order must not be re-tuned on validation data.
* **PRECEDENCE NOTES**: None.

---

### 2.11 Forecast metrics, relative skill, and horizon descriptors

* **SUBSECTION**: 2.11 Forecast metrics, relative skill, and horizon descriptors
* **PURPOSE**: Provide explicit mathematical definitions for RMSE, MAE, Bias, baseline-relative skill scores, and the empirical horizon descriptors $H_{\text{relax}}$ and $H_{\text{strict-from-h1}}$.
* **SOURCE FILES**:
  * `docs/MODEL_CONTRACT.md` (Section 3)
  * `FORECASTING_EVALUATION_REPORT.md` (Sections 5, 6)
  * `results_canonical/05_rolling_origin/table_skill_by_horizon.csv`
  * `results_canonical/05_rolling_origin/table_horizon_summary.csv`
* **IMPLEMENTATION FILES CHECKED**:
  * `src/tb_seit/metrics.py` (`rmse`, `mae`, `bias`)
  * `tests/test_rolling_origin.py`
* **KEY CONFIGURATION VALUES USED**:
  * $\text{Skill}_{\text{Metric}}(M, B, h) = 1 - \frac{\text{Metric}_M(h)}{\text{Metric}_B(h)}$
  * $H_{\text{relax}} = \max \{h \mid \text{Skill}(h) > 0\}$
  * $H_{\text{strict-from-h1}} = \max \{h \mid \forall h' \le h, \text{Skill}(h') > 0\}$
* **ASSUMPTIONS**:
  * Horizon indices are empirical summary descriptors of this specific evaluation grid.
* **DOCUMENTATION GAPS**:
  * BLOCKING: None.
  * NON_BLOCKING: None.
* **CLAIM-BOUNDARY RISKS**:
  * Avoid labeling $H$ indices as intrinsic predictability horizons or physical bounds.
  * No numerical skill outcomes or $H$ values reported in Methods.
* **PRECEDENCE NOTES**: None.

---

### 2.12 Statistical interpretation boundary

* **SUBSECTION**: 2.12 Statistical interpretation boundary
* **PURPOSE**: State clearly the descriptive nature of rolling-origin metrics, explain why formal inferential tests (e.g. Diebold–Mariano) are deferred, and establish strict language boundaries prohibiting claims of statistical significance.
* **SOURCE FILES**:
  * `manuscript_architecture/MANUSCRIPT_EVIDENCE_ARCHITECTURE.md` (Sections 4.1, 7)
  * `results_canonical/KNOWN_LIMITATIONS.md` (L10, L11)
  * `results_canonical/07_claim_support/claim_support_table.csv` (C11)
  * `docs/METHOD_DECISION_LOG.md` (D030)
* **IMPLEMENTATION FILES CHECKED**:
  * `tests/test_canonical_freeze.py`
  * `tests/test_manuscript_architecture.py`
* **KEY CONFIGURATION VALUES USED**:
  * `DM_TESTS = DEFERRED_NOT_PREREGISTERED`
  * `INFERENCE_STATUS = DESCRIPTIVE_ONLY`
* **ASSUMPTIONS**:
  * Multi-step rolling forecast error differentials exhibit serial and cross-origin dependence requiring pre-registered HAC modeling.
* **DOCUMENTATION GAPS**:
  * BLOCKING: None.
  * NON_BLOCKING: Formal HAC / DM inferential testing deferred to future work.
* **CLAIM-BOUNDARY RISKS**:
  * Strictly forbid terms like "statistically significant", "significantly outperforms", or "confirmed superiority".
* **PRECEDENCE NOTES**: None.

---

## Discrepancy Classification Audit

* `docs/MODEL_CONTRACT.md` ($\mu = 1/(75 \times 12)$, $\gamma \in [0.01, 0.50]$):
  * **Classification**: `SUPERSEDED_DOCUMENTATION`
  * **Status**: Resolved by canonical precedence rule (`EXTERNAL_PARAMETER_CONTRACT` + frozen implementation). No code or frozen evidence modification required.
* All other verified parameters and protocols:
  * **Classification**: Exact match across contracts, code, and canonical results.
  * **Frozen evidence inconsistencies**: **ZERO** (`FROZEN_EVIDENCE_INCONSISTENCY = NONE`).
