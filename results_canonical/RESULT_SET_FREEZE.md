# Result Set Freeze

RESULT_SET_STATUS = **FROZEN_WITH_DOCUMENTED_LIMITATIONS**

## Canonical HEAD before freeze

`cfec12a` (analysis: evaluate TB SEIT rolling-origin forecast skill)

## Canonical source hashes

- `data/raw/tb_mes.xlsx`: `93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b`
- `manuscript/source/BIOMATEMATICA_UNICAMP.docx`: `10e652628a7786460243fd47201bbfef498356fcee9766ce3fab48f64fa4ac88`

Both re-verified unchanged immediately before this freeze.

## Canonical tables

- `results_canonical/01_model_contract/table_model_contract_status.csv`
- `results_canonical/02_identifiability/table_full_profile_diagnostic.csv`
- `results_canonical/03_R0_stability/table_R0_stability_summary.csv`
- `results_canonical/04_long_open_loop/table_long_open_loop.csv`
- `results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv`
- `results_canonical/05_rolling_origin/table_skill_by_horizon.csv`
- `results_canonical/05_rolling_origin/table_horizon_summary.csv`
- `results_canonical/07_claim_support/claim_support_table.csv`
- `results_canonical/00_manifest/CANONICAL_EVIDENCE_MANIFEST.csv`

## Canonical figures

- `results_canonical/06_figures/F1_rmse_vs_horizon.png`
- `results_canonical/06_figures/F2a_skill_rmse_vs_horizon.png`
- `results_canonical/06_figures/F2b_skill_mae_vs_horizon.png`
- `results_canonical/06_figures/F3_R0_near_equivalent_envelope.png`
- `results_canonical/06_figures/F4_bias_vs_horizon.png`

## Canonical claims

See `results_canonical/07_claim_support/claim_support_table.csv` (C01-C11): 1
SUPPORTED_WITHIN_MODEL_FAMILY, 2 SUPPORTED, 1 SUPPORTED_ONLY_VS_SEASONAL_NAIVE, 5 NOT_SUPPORTED
(C02, C03, C05, C06, C09), 1 NOT_VERIFIED, 1 NOT_TESTED.

## Known limitations

See `results_canonical/KNOWN_LIMITATIONS.md` (L01-L12).

## Deferred analyses

See "Deferred items" below.

---

## Forecast-error dependence and future inference

The current rolling-origin forecasting evidence is descriptive and baseline-relative. No
statistical-superiority claim is made.

Residual autocorrelation was previously detected in the separate LONG_OPEN_LOOP_STRESS_TEST, but
serial dependence of the rolling-origin forecast errors and horizon-specific loss differentials
has not yet been formally characterized.

Therefore, the current RMSE/MAE skill values and horizon summaries are frozen as descriptive
results only.

If inferential comparison is added later, including Diebold-Mariano or a related
forecast-comparison test, the protocol must be specified before execution and must:

- operate separately by forecast horizon and explicit baseline;
- use horizon-specific loss-differential series;
- define the loss function before analysis;
- account for serial dependence and overlapping multi-step forecasts with an appropriate
  HAC/dependence-robust variance estimator;
- account explicitly for the small number of forecast origins;
- define any multiple-comparison correction before testing.

No iid confidence interval or independence-based test should be applied without first
demonstrating that its assumptions are appropriate.

STATUS:

KNOWN_INFERENCE_LIMITATION
DOES_NOT_REOPEN_FROZEN_DESCRIPTIVE_RESULTS

---

## Deferred items

```
DM_TESTS                    = DEFERRED_NOT_PREREGISTERED
OPTIMAL_CONTROL              = DEFERRED_NOT_VERIFIED
HISTORICAL_48_PERCENT_CLAIM  = NOT_VERIFIED
MANUSCRIPT_REWRITE           = NEXT_STAGE_AFTER_FREEZE
LATEX                        = BLOCKED_UNTIL_MANUSCRIPT_EVIDENCE_UPDATE
```

## Reopening policy

After this freeze, scientific experiments may be reopened ONLY for:

1. numerical inconsistency;
2. reproducibility failure;
3. evidence required for a CENTRAL manuscript claim;
4. an explicitly authorized future inferential analysis;
5. an explicit author decision to change the scientific question.

They must NOT be reopened simply because: persistence performs better; SARIMA performs better;
skill is negative; a more favorable result might be achievable; or the historical manuscript
reported stronger results.
