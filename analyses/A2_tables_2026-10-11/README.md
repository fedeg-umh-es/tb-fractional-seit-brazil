# A2 tables — MAE, bias and MASE from the frozen S1 predictions (2026-10-11)

Plan A, step 2. Arithmetic only: no model was fitted or simulated. The input is
`evidence_S1/TB_SEIT_EVIDENCE_FREEZE_2026-10-10/phase2/rolling_origin_predictions.csv`
(780 rows = 5 methods x 12 horizons x 13 origins, 2020-12 to 2021-12) and the canonical series
`data/raw/tb_mes.xlsx` (`casos`). Reproduce with `python -I analyses/A2_tables_2026-10-11/make_tables.py`.

## Definitions

- Error: `e = predicted - observed`.
- RMSE(h) = sqrt(mean(e^2)); MAE(h) = mean(|e|); bias(h) = mean(e) (negative = under-prediction).
  All means are over the 13 origins.
- **MASE** (Hyndman and Koehler, 2006):
  - *Scale* for origin `o`: the in-sample MAE of the seasonal naive with m = 12, computed on the
    training window of that origin, 2001-01 to the origin month inclusive:
    `s_o = mean_{t=13..n_o} |y_t - y_{t-12}|` (n_o = 240 for the 2020-12 origin, 252 for 2021-12).
    Values are in `mase_scale_by_origin.csv`.
  - *Aggregation*: `MASE(h) = mean over the 13 origins of |e_{o,h}| / s_o`.
  - Because each origin has its own scale, MASE(h) is not MAE(h) divided by a single constant.
  - Interpretation: values below 1 indicate a smaller absolute error than the in-sample one-year-ago
    seasonal naive on the same training window. This is a descriptive scaling, not a test.

## Checks (both passed)

1. **Reconciliation with the frozen table.** RMSE, MAE and bias recomputed from the 780 predictions
   match `phase2/metrics_by_horizon.csv` for all 60 method-horizon rows. Maximum absolute difference:
   RMSE 4.5e-13, MAE 6.8e-13, bias 6.8e-13 (tolerance 1e-9 on RMSE). See `rmse_reconciliation.json`.
   The `observed` column also equals the canonical series exactly.
2. **Persistence vs seasonal naive at h = 12.** The two predictions are identical in all 13 origins
   (maximum absolute difference 0.0), so their metrics coincide at h = 12 (RMSE 1152.958, MAE 1016.2,
   bias -880.5, MASE 2.330). This holds because the forecast for origin month T + 12 is y_T under both
   methods. See `h12_persistence_vs_snaive_check.json`.

## A4a (re-running the baselines)

Not needed. Persistence, seasonal naive and SARIMA predictions are the archived ones, reused in S1
after support and provenance checks (`phase2/baseline_reuse_checks.csv`), and they are identical to
the historical set.

## Files

| File | Content |
|---|---|
| `metrics_full_by_horizon.csv` | RMSE, MAE, bias, MASE, n for 5 methods x 12 horizons |
| `table_MAE.{csv,tex}`, `table_bias.{csv,tex}`, `table_MASE.{csv,tex}` | wide tables for the manuscript |
| `mase_scale_by_origin.csv` | MASE scale per origin |
| `rmse_reconciliation.json`, `h12_persistence_vs_snaive_check.json` | check outputs |

## Reading limits

13 origins with overlapping multi-step errors over a 2021-2022 window: these are descriptive
summaries. The uniformly negative bias of all methods is consistent with an upward level shift in
the observed series over the evaluation window; the tables do not identify its cause.
