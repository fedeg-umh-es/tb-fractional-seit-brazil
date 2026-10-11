# Evidence Freeze Report

## 1. Freeze status

RESULT_SET_STATUS = FROZEN_WITH_DOCUMENTED_LIMITATIONS. Canonical HEAD before freeze: `cfec12a`.
This is an evidence-packaging exercise: no new scientific experiments, no recalibration, no
model-selection reruns, no seed changes, no bound changes, no DM tests, no optimal control, no
manuscript rewriting.

## 2. Canonical source provenance

`data/raw/tb_mes.xlsx` (SHA-256 `93e75138...ea662b`) and
`manuscript/source/BIOMATEMATICA_UNICAMP.docx` (SHA-256 `10e65262...f64fa4ac88`) re-verified
unchanged immediately before this freeze. REPRODUCTION_MODE = INDEPENDENT_REIMPLEMENTATION;
historical manuscript numerical results remain REFERENCE_ONLY_NOT_EVIDENCE, superseded by this
evidence set.

## 3. Model-contract status

Fractional-order SEIT (Caputo), observed reported cases modeled as an incidence flow associated
with the E->I transition (not the infectious stock I(t)). Free parameters beta, sigma, gamma, d,
alpha. `results_canonical/01_model_contract/table_model_contract_status.csv`.

## 4. Identifiability evidence

PARAMETER_IDENTIFIABILITY = WEAK (beta/gamma/d individually not reportable as precise rates).
PREDICTIVE_IDENTIFIABILITY = ROBUST. R0_FUNCTIONAL_IDENTIFIABILITY = ROBUST.
ALPHA_IDENTIFIABILITY = ROBUST. `IDENTIFIABILITY_AUDIT_REPORT.md`;
`results_canonical/02_identifiability/table_full_profile_diagnostic.csv` (full 33-solution pool,
diagnostic only, 2 of 33 with R0<1 -- never generalized to "R0>1 throughout").

## 5. R0/stability evidence

Primary mechanistic evidence uses ONLY the near-equivalent admissible set (delta calibration
RMSE <=1%, n=25): R0 in [1.1542, 1.1892], median 1.1735, IQR [1.1682, 1.1770]. Disease-free
equilibrium: 0 stable, 25 unstable, 0 ambiguous, under the commensurate Caputo/Matignon
criterion. `results_canonical/03_R0_stability/table_R0_stability_summary.csv`. The common
positive reference-time scaling factor was proved to cancel exactly from the next-generation
matrix (`R0_STABILITY_ANALYSIS_NOTE.md`).

## 6. Long-open-loop evidence

Single-origin stress test (calibration through 2020-12, continuous open-loop through 2022-12):
fractional RMSE=1117.960/MAE=953.230/bias=-851.150; integer RMSE=1759.538/MAE=1588.649/
bias=-1588.649. `results_canonical/04_long_open_loop/table_long_open_loop.csv`. Kept explicitly
separate from rolling-origin evidence throughout.

## 7. Rolling-origin forecasting evidence

13 expanding-window origins (2020-12..2021-12), h=1..12, 5 models, 780 leakage-audited forecasts
(0 duplicates, 0 temporal violations). Each SEIT model fit exactly once per origin; the same fit
generated all 12 horizons. SARIMA order frozen before evaluation
(`docs/SARIMA_BASELINE_CONTRACT.md`: SARIMA(0,1,2)(1,1,1,12)).
`results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv` (60 rows, never
collapsed across horizons).

## 8. Baseline-relative skill

`results_canonical/05_rolling_origin/table_skill_by_horizon.csv` /
`table_horizon_summary.csv`:

- vs integer: fractional lower error at every horizon (within-model-family only).
- vs persistence: negative skill at every horizon (H_relax=0, H_strict_from_h1=0).
- vs SARIMA: negative skill at every horizon (H_relax=0, H_strict_from_h1=0).
- vs seasonal_naive_12: positive skill h=1-7, negative h=8-12 (H_relax=7, H_strict_from_h1=7).

## 9. Claim-support audit

`results_canonical/07_claim_support/claim_support_table.csv`, 11 claims (C01-C11): each maps to
a supporting artifact with allowed/forbidden wording. No claim of general forecasting
superiority, statistical significance, or biological memory survives this audit.

## 10. Known inferential limitations

Rolling-origin skill values and horizon summaries are descriptive only; no DM test performed;
serial dependence of rolling-origin horizon-specific loss differentials not yet formally
characterized (long-open-loop residual autocorrelation was characterized separately and is not a
substitute). `results_canonical/KNOWN_LIMITATIONS.md` L09-L11;
`results_canonical/RESULT_SET_FREEZE.md` "Forecast-error dependence and future inference".

## 11. Deferred analyses

`DM_TESTS=DEFERRED_NOT_PREREGISTERED`, `OPTIMAL_CONTROL=DEFERRED_NOT_VERIFIED`,
`HISTORICAL_48_PERCENT_CLAIM=NOT_VERIFIED`, `MANUSCRIPT_REWRITE=NEXT_STAGE_AFTER_FREEZE`,
`LATEX=BLOCKED_UNTIL_MANUSCRIPT_EVIDENCE_UPDATE`.

## 12. Reopening policy

Reopen only for: numerical inconsistency; reproducibility failure; evidence required for a
central manuscript claim; an explicitly authorized future inferential analysis; or an explicit
author decision to change the scientific question. Never reopen merely because a baseline
performed better or a more favorable result might be achievable.
`results_canonical/RESULT_SET_FREEZE.md`.

## 13. Next manuscript stage

Prepare evidence-first manuscript architecture from this frozen result set (see
`results_canonical/00_manifest/CANONICAL_EVIDENCE_MANIFEST.csv` for the artifact index each
section should cite). Do not run additional experiments unless required by a central manuscript
claim.

---

"The fractional-order SEIT formulation consistently reduced forecast error relative to its
independently refitted integer-order counterpart. However, under rolling-origin evaluation it
showed negative observed skill relative to persistence and SARIMA at every evaluated horizon,
while positive skill relative to seasonal naive was limited to horizons 1-7. Separately,
individual epidemiological rate parameters were weakly identifiable, whereas the derived R0
functional remained stable and above unity across the near-equivalent admissible solution set,
for which the disease-free equilibrium was locally unstable. These mechanistic results do not
constitute evidence of operational forecasting superiority."
