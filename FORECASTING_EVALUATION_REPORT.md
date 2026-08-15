# Forecasting Evaluation Report

Primary predictive-evidence stage for tb-fractional-seit-brazil. Dimensional consistency, R0
derivation, stability, and the identifiability audit are **frozen** and not reopened here
(`R0_STABILITY_ANALYSIS_NOTE.md`, `docs/FRACTIONAL_DIMENSIONAL_CONSISTENCY.md`,
`IDENTIFIABILITY_AUDIT_REPORT.md`). No optimal control, no DM tests, no manuscript/LaTeX work.

## 1. Scientific forecasting question

Does the fractional-order SEIT model retain predictive skill against explicit forecasting
baselines (persistence, seasonal-naive, SARIMA) and against the honestly re-fit integer-order
comparator, as the forecast horizon increases from 1 to 12 months?

## 2. Rolling-origin protocol

Expanding-window rolling-origin evaluation, 13 origins (`src/tb_seit/rolling_origin.py`,
`ORIGINS = 2020-12 .. 2021-12`), chosen deterministically so every origin's full `h=1..12`
horizon set falls entirely within the primary evaluation window (2021-01..2022-12) and entirely
within available data -- a fully-crossed origin x horizon grid, 13 x 12 = 156 forecasts per
model. At each origin: fractional SEIT and integer SEIT (`alpha=1` exactly) are each **fit
exactly once** (Differential Evolution, `PRIMARY_SEED=20260815`, frozen bounds/DE policy from
`docs/MODEL_CONTRACT.md`, unchanged) on the training data available up to that origin, and a
single continuous simulation from that one fit produces all 12 horizons at once (verified
structurally: `scripts/run_rolling_origin_forecast.py::fit_mechanistic` calls
`run_differential_evolution` once and `rolling_origin.simulate_forecast(..., n_horizon_months=12)`
once per origin per model -- 13 origins x 2 models = 26 fits total, confirmed against the run log
and `tests/test_predictions_full_grid_origin_x_horizon_x_model`).

## 3. Baselines

- **B1 persistence**: last observed value at the origin, repeated for all 12 horizons.
- **B2 seasonal_naive_12**: `y_hat(origin+h) = y(origin+h-12)`, using only historical
  observations (always `<= origin` for `h<=12`).
- **B3 SARIMA**: order frozen BEFORE evaluation via `docs/SARIMA_BASELINE_CONTRACT.md` (grid
  search, AIC-minimizing, on 2001-2020 data only, never inspecting 2021-2022) ->
  `SARIMA(0,1,2)(1,1,1,12)`, AIC=3194.705 on the selection data
  (`outputs/forecasting/sarima_frozen_order.json`). At each rolling origin, this frozen order's
  *coefficients* are refit on that origin's own training data (exactly analogous to the
  mechanistic models' per-origin refitting); the order itself is never re-selected.

## 4. Leakage audit

Programmatic post-run integrity gate (all checks passed): 780/780 rows (13 origins x 12
horizons x 5 models), 0 duplicate origin x horizon x model combinations, every origin has all
12 horizons for all 5 models, `train_end < target_date` in all 780 rows (0 violations),
population extrapolation fit separately per origin on that origin's own training window only
(`tests/test_population_trend_uses_training_window_only`,
`test_N_of_t_beyond_training_window_uses_extrapolation_not_future_actuals`), SARIMA refit on
training-only data per origin, and each origin's mechanistic fit reused unchanged across all 12
horizons (constant `n_train`/`seed` per origin x model group). No 2021-2022 observation entered
any fit, extrapolation, or model-order selection.

## 5. RMSE by horizon

`outputs/forecasting/metrics_by_horizon.csv` (n=13 per cell). RMSE rises with horizon for every
model. Fractional consistently and substantially below integer at every horizon (e.g. h=1:
688.9 vs 1185.8; h=12: 1356.0 vs 2022.5). Fractional is **above** (worse than) persistence and
SARIMA at every one of the 12 horizons. Fractional is below (better than) seasonal_naive_12 for
h=1-7 and above it for h=8-12.

## 6. MAE by horizon

Same qualitative pattern as RMSE (see CSV for exact values); fractional < integer at every
horizon; fractional > persistence and > SARIMA at every horizon; fractional < seasonal_naive_12
for h=1-7, > for h=8-12.

## 7. Bias by horizon

All five models show negative bias (underprediction) that grows with horizon in every case
(strongest evidence: fractional bias goes from -409.6 at h=1 to -1234.95 at h=12; note the
fractional bias equals `-MAE` exactly from h=6 onward, meaning **every** fractional residual at
those horizons is negative -- 100% underprediction, not merely on-average). Persistence and
SARIMA also underpredict growing TB incidence but less severely at short horizons.

## 8. Skill vs persistence

`Skill_RMSE(h)` and `Skill_MAE(h)` for fractional vs persistence are **negative at every one of
the 12 horizons** (range roughly -0.77 at h=1 to -0.17 at h=12 for RMSE) -- persistence
outperforms the fractional model at every horizon in this evaluation. Positive values would mean
skill; none occur here, so no positive-skill language is used.

## 9. Skill vs seasonal naive

`Skill_RMSE(h)` for fractional vs seasonal_naive_12 is **positive for h=1-7** (0.368 at h=1,
declining to 0.027 at h=7) and **negative for h=8-12** (-0.074 to -0.176). Same pattern for MAE.
This is a genuine, if partial and horizon-limited, positive skill result -- reported as such,
not as statistically significant (no DM test performed, per scope).

## 10. Skill vs SARIMA

`Skill_RMSE(h)` and `Skill_MAE(h)` for fractional vs SARIMA are **negative at every one of the
12 horizons** (range roughly -0.34 to -0.06). SARIMA outperforms the fractional model at every
horizon evaluated.

## 11. Horizon summary

`outputs/forecasting/horizon_summary.csv` (fractional model only, per instruction):

| baseline | metric | H_relax (last h with positive skill) | H_strict_from_h1 (longest run from h=1) |
|---|---|---|---|
| persistence | RMSE | 0 | 0 |
| persistence | MAE | 0 | 0 |
| seasonal_naive_12 | RMSE | 7 | 7 |
| seasonal_naive_12 | MAE | 7 | 7 |
| SARIMA | RMSE | 0 | 0 |
| SARIMA | MAE | 0 | 0 |

These are descriptors of this dataset and this rolling-origin protocol only -- not universal
predictability limits, per instruction.

## 12. Long-open-loop comparison

`outputs/forecasting/protocol_comparison.csv`, explicitly separated and never mixed:

- **LONG_OPEN_LOOP_STRESS_TEST** (single origin 2020-12, preserved unchanged, not recomputed):
  fractional RMSE=1117.960/MAE=953.230/bias=-851.150; integer RMSE=1759.538/MAE=1588.649/
  bias=-1588.649.
- **ROLLING_ORIGIN_FORECASTING** (13 origins x h=1..12 pooled -- SECONDARY AGGREGATE ONLY, not
  primary evidence, which stays horizon-wise in Sections 5-7): fractional RMSE=1165.5/
  MAE=1031.3/bias=-987.5; integer RMSE=1780.3/MAE=1666.9/bias=-1666.9; persistence
  RMSE=924.4/MAE=744.7; seasonal_naive_12 RMSE=1189.1/MAE=1102.9; SARIMA RMSE=1028.4/MAE=888.5.

Reading: the long-open-loop single-origin result (RMSE=1117.96, better than the rolling-origin
pooled average of 1165.5) was evaluated at only one specific origin (2020-12); the rolling-origin
protocol's 13-origin evidence shows that result was not unusually favorable, but it also was not
the best case either -- origin-level variation exists (`outputs/figures/forecasting/
origin_horizon_error_map_fractional.png`). Critically, the single-origin stress test alone
could not have revealed that persistence and SARIMA outperform the fractional model at every
horizon -- that finding required the baseline comparisons only available in the rolling-origin
protocol.

## 13. Limitations

- 13 origins is a small sample for horizon-wise metrics (n=13 per model x horizon cell); no
  significance testing was performed (DM tests explicitly out of scope for this task).
- The SARIMA order was frozen on 2001-2020 data only; a different order might perform
  differently, but re-selecting it now would violate the train-only contract.
- Rolling-origin re-estimation reuses the same frozen bounds/DE policy/seed at every origin; it
  does not re-litigate any of the frozen mechanistic/dimensional/identifiability findings.
- Forecast-error ACF (`outputs/forecasting/forecast_error_acf.csv`) was computed per
  model/horizon across the 13 origins but is diagnostic only, per instruction, not used to
  determine any uncertainty interval or significance claim here.
- Beta, gamma, and d are not reinterpreted as precise rates anywhere in this report; alpha's
  stability (frozen evidence) is not treated as proof of epidemiological memory.

## 14. Forecasting verdict

**FRACTIONAL_ADVANTAGE_ONLY_VS_INTEGER**

The fractional model shows a clear, consistent, horizon-wide advantage over the integer-order
comparator (lower RMSE/MAE at all 12 horizons, by a substantial margin). It does **not** show
that advantage against the two more informative baselines: it underperforms persistence and
SARIMA at every one of the 12 horizons tested, and only partially/temporarily outperforms
seasonal_naive_12 (h=1-7 of 12). The fractional model's predictive advantage documented in this
evaluation is specific to the integer-order comparison, not a general forecasting-skill result.

## 15. Next permitted step

Given no baseline-relative skill beyond the integer comparator and a partial, horizon-limited
result against seasonal-naive, the responsible next step is to report these results as-is
(already done here) rather than proceed to claims of general predictive skill. Formal
significance testing (Diebold-Mariano) against persistence/SARIMA/seasonal-naive, if pursued
later, would need to be pre-registered (metric, horizon set, correction for multiple horizons)
before being run, following this project's established pattern of freezing methodology before
looking at results.
