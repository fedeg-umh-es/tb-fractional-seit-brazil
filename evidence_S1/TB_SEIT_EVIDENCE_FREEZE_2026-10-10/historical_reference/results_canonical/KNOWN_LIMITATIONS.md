# Known Limitations

**L01.** Original historical code/configuration unavailable. Study is an independent
reimplementation (`docs/REIMPLEMENTATION_PROTOCOL.md`); exact reproduction of the manuscript's
numerical results is impossible.

**L02.** beta, gamma, and d are weakly identifiable individually (`IDENTIFIABILITY_AUDIT_REPORT.md`:
5.4x, 5.3x, and >100x spread respectively across near-equivalent solutions, despite
calibration-RMSE CV of only 0.35%).

**L03.** The R0 range `[1.1542, 1.1892]` is a practical-identifiability envelope (near-equivalent
admissible solution range), not a confidence interval, not a sampling-uncertainty interval.

**L04.** Only one national monthly incidence series is available (no subnational, no independent
replication series).

**L05.** The SEIT latent-process structure is necessarily simplified relative to TB natural
history (e.g. a single exposed compartment cannot separately represent fast vs. slow
progression pathways).

**L06.** Validation/forecast period is limited to 2021-2022 (24 months), the only period held out
of calibration under the canonical data split.

**L07.** Rolling-origin evaluation has only 13 origins for the common h=1..12 comparison
(`FORECASTING_EVALUATION_REPORT.md` Sec 2), a small sample for horizon-wise metrics.

**L08.** Persistence and SARIMA outperform the fractional model descriptively at all evaluated
horizons (`results_canonical/05_rolling_origin/table_skill_by_horizon.csv`).

**L09.** Long-open-loop residuals showed significant serial autocorrelation
(`outputs/audits/residual_autocorrelation_diagnostics.csv`: Ljung-Box p<0.001 in all four series
-- fractional/integer x calibration/validation).

**L10.** Serial dependence of rolling-origin horizon-specific loss differentials has not yet
been formally characterized. Autocorrelation was checked for the separate long-open-loop
residuals only (L09); the rolling-origin forecast errors and, critically, the horizon-specific
loss differentials against each baseline have not undergone the equivalent diagnostic.

**L11.** No inferential forecast-comparison test (e.g. Diebold-Mariano) has been performed. All
rolling-origin skill values and horizon summaries are descriptive results only.

**L12.** Historical optimal-control results, including the approximately 48% reduction, remain
`NOT_VERIFIED` (`PROJECT_CANON.md`) -- optimal control was never implemented in this
reimplementation.
