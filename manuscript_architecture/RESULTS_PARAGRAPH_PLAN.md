# Results Paragraph Plan

No Results prose is drafted here. Each planned paragraph is specified by its Point, Evidence,
Explanation allowed, and Resolution/bridge (PIER used as paragraph anatomy, not a sentence
template), plus the canonical artifacts and claim IDs it draws on.

## P1 -- Protocol orientation (precedes R1)

- **Point**: Two independent evaluation protocols (long open-loop stress test; 13-origin
  rolling-origin evaluation) are reported separately and never numerically mixed.
- **Evidence**: `results_canonical/04_long_open_loop/table_long_open_loop.csv`;
  `results_canonical/05_rolling_origin/*`; `FORECASTING_EVALUATION_REPORT.md` Sec 12.
- **Explanation allowed**: Why two protocols exist (single-origin stress test vs. genuine
  multi-origin generalization check) and why they must stay separate (a single origin cannot
  establish forecasting skill against baselines; only the multi-origin protocol includes
  baselines at all).
- **Resolution/bridge**: Sets up R1 to report both protocols' fractional-vs-integer result
  together without conflating them with baseline comparisons yet to come.
- **Canonical artifacts**: `table_long_open_loop.csv`, `FORECASTING_EVALUATION_REPORT.md`.
- **Claim IDs**: M04 (methodological).

## P2 -- R1: fractional beats integer, both protocols

- **Point**: The fractional SEIT has lower RMSE/MAE than the independently re-estimated integer
  SEIT in both the long open-loop stress test and at every rolling-origin horizon.
- **Evidence**: `table_long_open_loop.csv` (RMSE 1117.960 vs 1759.538); `table_forecasting_by_horizon.csv`
  (fractional/integer rows, all h=1-12).
- **Explanation allowed**: That the integer comparator was independently re-estimated (not the
  fractional fit with alpha forced to 1), so this is a fair within-family comparison; state
  explicitly this is a within-model-family result.
- **Resolution/bridge**: "This raises the question of whether the improvement is forecasting-
  relevant beyond the SEIT family itself."
- **Canonical artifacts**: `table_long_open_loop.csv`, `table_forecasting_by_horizon.csv`, F1.
- **Claim IDs**: C01.

## P3 -- R2: no skill vs persistence or SARIMA (turning point)

- **Point**: Skill against persistence and against SARIMA is negative at every one of the 12
  evaluated horizons.
- **Evidence**: `table_skill_by_horizon.csv` (fractional vs persistence, fractional vs SARIMA,
  all rows negative); `table_horizon_summary.csv` (H_relax=0, H_strict_from_h1=0 for both).
- **Explanation allowed**: What "skill<0" means concretely (the baseline's RMSE/MAE is lower);
  representative values at h=1, h=6, h=12 already tabulated may be cited directly from the CSV,
  not re-derived; state this is descriptive, not a significance-tested result.
- **Resolution/bridge**: "This is the paper's central turning point: a consistent within-family
  improvement (P2) does not generalize to two of the three external baselines evaluated."
- **Canonical artifacts**: `table_skill_by_horizon.csv`, `table_horizon_summary.csv`, F1, F2a, F2b.
- **Claim IDs**: C02, C03, C05.

## P4 -- R3: bounded positive skill vs seasonal-naive

- **Point**: Against seasonal-naive specifically, skill is positive for h=1-7 and negative for
  h=8-12.
- **Evidence**: `table_skill_by_horizon.csv` (seasonal_naive_12 rows); `table_horizon_summary.csv`
  (H_relax=7, H_strict_from_h1=7).
- **Explanation allowed**: Why this one baseline differs qualitatively from the other two
  (descriptive contrast only -- no causal mechanism should be asserted); explicit statement that
  H=7 is a descriptor of this dataset/protocol, not a general predictability limit.
- **Resolution/bridge**: "Having established the full predictive picture (P2-P4), we turn to
  what the calibration itself can and cannot support mechanistically."
- **Canonical artifacts**: `table_skill_by_horizon.csv`, `table_horizon_summary.csv`, F2a, F2b.
- **Claim IDs**: C04.

## P5 -- R4a: individual parameters weakly identified

- **Point**: beta, gamma, and d vary by roughly 5x, 5x, and >100x respectively across
  near-equivalent calibration solutions, despite near-identical calibration fit.
- **Evidence**: `IDENTIFIABILITY_AUDIT_REPORT.md` (multiseed + profile-objective evidence);
  calibration RMSE CV~0.35% vs. parameter CVs of 58%/60%/82% (from the audit; no new
  computation).
- **Explanation allowed**: Why this matters (these three parameters cannot be reported as point
  estimates of biological rates); explicitly forbid stating any specific beta/gamma/d value as a
  finding.
- **Resolution/bridge**: "Despite this, predictions and the derived R0 functional remain
  strikingly stable across the same solution set."
- **Canonical artifacts**: `IDENTIFIABILITY_AUDIT_REPORT.md` (no results_canonical table needed;
  this is process-level identifiability evidence, cited to the audit report directly).
- **Claim IDs**: C09.

## P6 -- R4b: predictive and R0-functional robustness

- **Point**: Predictions vary by only 0.19%/0.58% CV (calibration/validation) and R0 remains in
  [1.1542, 1.1892] (IQR [1.1682, 1.1770]) across the same 25-member near-equivalent set.
- **Evidence**: `IDENTIFIABILITY_AUDIT_REPORT.md` (prediction dispersion);
  `results_canonical/03_R0_stability/table_R0_stability_summary.csv`.
- **Explanation allowed**: The distinction between parameter identifiability and
  predictive/functional identifiability (Sec 19 of the architecture task); explicit statement
  that this range is a "practical-identifiability envelope," never a confidence interval.
- **Resolution/bridge**: "Given a robust R0, the implied equilibrium behavior can be assessed
  consistently across the admissible set."
- **Canonical artifacts**: `table_R0_stability_summary.csv`, F3.
- **Claim IDs**: C07; M03 (methodological).

## P7 -- R5: DFE instability across the admissible set

- **Point**: The disease-free equilibrium is locally unstable in 25 of 25 near-equivalent
  admissible solutions under the commensurate Caputo/Matignon criterion.
- **Evidence**: `table_R0_stability_summary.csv` (DFE_stable=0, DFE_unstable=25, DFE_ambiguous=0).
- **Explanation allowed**: One sentence on what "locally unstable DFE" means epidemiologically
  (persistent transmission is dynamically consistent with R0>1, not a new independent fact);
  explicit statement that this is restricted to the admissible set and does not generalize to
  the full 33-solution diagnostic pool (2 of which are stable).
- **Resolution/bridge**: Closes Results; hands off to Discussion's explicit separation of
  mechanistic findings (R4/R5) from forecasting findings (R1-R3).
- **Canonical artifacts**: `table_R0_stability_summary.csv`, `table_full_profile_diagnostic.csv`
  (negative-space citation).
- **Claim IDs**: C08.
