# Fractional-memory kill-condition audit

Per docs/MODEL_CONTRACT.md Section 15. Evidence-based only; no configuration was
adjusted to avoid any outcome below.

## A. Parameter stability across seeds vs. objective spread
Objective (calibration RMSE) coefficient of variation across seeds: 0.0035
Per-parameter CV across seeds: {'beta': 0.5799560130787418, 'sigma': 0.005234634805455617, 'gamma': 0.5985018135472373, 'd': 0.8221783517959707, 'alpha': 0.0008328185164861827}
Classification: SURVIVES / WEAKENS / FAILS -- see prose in BASE_MODEL_REIMPLEMENTATION_REPORT.md Section 12/13 (no undocumented binary threshold applied here; continuous diagnostics only).

## B. Alpha boundary behavior
Fitted alpha across seeds: [0.9640110362133341, 0.9635474177364491, 0.9619756595044474, 0.9622398765493891, 0.9623532255827466]
Primary bound: [0.50, 1.00]

## C. Integer comparator vs. fractional model, 2021-2022 holdout
Fractional validation RMSE: 1117.9600278444248
Integer validation RMSE:    1759.538400545304
Fractional better: True
