# A3 — SARIMA coefficients per origin: protocol (written before execution)

Date: 2026-10-11. Plan A continuation, step 3. Responds to Amaury's request A4b.

## Purpose

Report the SARIMA coefficients, standard errors, log-likelihood, AIC and convergence status for
each of the 13 rolling origins. This is the reproduction of a deterministic fit that already
exists; it is not a new model and it changes no archived prediction.

## Specification (fixed; nothing is selected or tuned here)

- Order (0,1,2)(1,1,1)12, read from `outputs/forecasting/sarima_frozen_order.json`
  (`selected_order`, `selected_seasonal_order`).
- Estimator and options exactly as `fit_sarima` in `scripts/run_rolling_origin_forecast.py`:
  `statsmodels.tsa.statespace.sarimax.SARIMAX(train_cases, order, seasonal_order,
  enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)`; default optimizer
  and default covariance type; 12-step `get_forecast(12).predicted_mean`.
- Training data: `tb_seit.rolling_origin.build_training_set(origin)`, i.e. observations with
  date <= origin only (2001-01 to the origin month, n_train = 240..252).
- Origins: 2020-12-01 to 2021-12-01 (13 origins).
- Software: the venv installed from `phase1/requirements_frozen.txt` (statsmodels 0.15.0,
  numpy 2.5.3, scipy 1.18.1). Single process, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1`.
- No random seed is involved (the fit is deterministic).

## Quantities saved per origin

`ma.L1`, `ma.L2`, `ma.S.L12`... as named by statsmodels (`param_names`): coefficient and standard
error for each of the 4 parameters (ma1, ma2, seasonal ar1, seasonal ma1) plus sigma2; `llf`,
`aic`, `nobs`, `nobs_effective` as reported by statsmodels; `mle_retvals["converged"]` and the
optimizer warnings flag.

## Reproduction control (decided in advance)

The 12 regenerated forecasts of each origin are compared with the archived SARIMA predictions in
`evidence_S1/TB_SEIT_EVIDENCE_FREEZE_2026-10-10/phase2/rolling_origin_predictions.csv`.
Criterion: maximum over the 156 forecasts of |regenerated - archived| / |archived| <= 1e-6.

## Stopping conditions

Stop and report, without trying variants, if: the criterion above is not met; any fit does not
report convergence; any fit raises an exception or returns non-finite values; a hash or the
S1 verifier fails. If the control fails, the archived predictions are not replaced and the
coefficient tables are not offered as the coefficients behind them.

## Interpretation

The coefficients describe the baseline that was evaluated; they are not a model-selection result
and not a claim about tuberculosis dynamics. The order was fixed once on 2001-2020 data
(`docs/SARIMA_BASELINE_CONTRACT.md`) and is not revisited.

## Outputs

`sarima_coefficients_by_origin.csv`, `reproduction_control.json`, `REPORT.md`, plus the script
`run_sarima_coefficients.py`.
