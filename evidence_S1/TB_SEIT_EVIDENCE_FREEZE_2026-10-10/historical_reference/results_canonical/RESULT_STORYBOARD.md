# Result Storyboard

## Question

Does the fractional-order SEIT formulation provide useful predictive advantage for monthly
tuberculosis forecasting when evaluated against both its integer-order counterpart and explicit
forecasting baselines?

## Design

Independent reproducible implementation. Rolling-origin evaluation. 13 origins. h=1..12.
Fractional SEIT, integer SEIT, persistence, seasonal naive, SARIMA. Strict train-only
information flow (`FORECASTING_EVALUATION_REPORT.md` Sec 2-4; leakage audit: 0 violations across
780 forecasts).

## Result 1

Within the SEIT family, the fractional formulation consistently reduced forecast error relative
to the integer-order counterpart, at every one of the 12 evaluated horizons
(`results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv`).

## Result 2

This within-family improvement did not translate into operational skill against stronger
external forecasting baselines.

## Turning point

Persistence and SARIMA produced lower RMSE than the fractional SEIT model at every evaluated
horizon (`results_canonical/05_rolling_origin/table_skill_by_horizon.csv`: `Skill_RMSE` and
`Skill_MAE` negative for h=1..12 against both baselines).

## Result 3

Against seasonal naive only, fractional RMSE skill remained positive through h=7
(`results_canonical/05_rolling_origin/table_horizon_summary.csv`: `H_relax=7`,
`H_strict_from_h1=7`), and turned negative for h=8..12.

## Result 4

Mechanistically, individual epidemiological rate parameters (beta, gamma, d) were weakly
identified (5.4x, 5.3x, and >100x spread respectively across near-equivalent solutions despite
near-identical calibration fit), but the R0 functional was comparatively stable across
near-equivalent solutions (`IDENTIFIABILITY_AUDIT_REPORT.md`).

## Result 5

Across all 25 near-equivalent admissible solutions, R0 exceeded one (range 1.1542-1.1892,
median 1.1735) and the disease-free equilibrium was locally unstable under the implemented
Caputo/Matignon criterion (`results_canonical/03_R0_stability/table_R0_stability_summary.csv`).

## Boundary

The fractional formulation is numerically reproducible, dimensionally coherent, and superior to
the corresponding integer-order SEIT within the model family, but the evidence does **not**
support general operational forecasting superiority over persistence or SARIMA.

No novelty claims are made here. No causal biological-memory claim is made. R0/stability
evidence is not treated as evidence of forecasting accuracy -- these are two separate evidence
layers, reported separately throughout (`results_canonical/00_manifest/CANONICAL_EVIDENCE_MANIFEST.csv`).
