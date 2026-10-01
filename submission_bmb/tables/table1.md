**Table 1. Empirical skill-horizon descriptors of the fractional SEIT model relative to each external baseline in the 13-origin expanding-window evaluation ($h = 1,\dots,12$ months).**

| Baseline | Metric | $H_{\text{relax}}$ | $H_{\text{strict-from-h1}}$ | Longest positive run |
|---|---:|---:|---:|---:|
| Persistence | RMSE | 0 | 0 | 0 |
| Persistence | MAE | 0 | 0 | 0 |
| Seasonal naive | RMSE | 7 | 7 | 7 |
| Seasonal naive | MAE | 7 | 7 | 7 |
| SARIMA | RMSE | 0 | 0 | 0 |
| SARIMA | MAE | 0 | 0 | 0 |

$H_{\text{relax}}$ is the largest horizon with positive observed skill; $H_{\text{strict-from-h1}}$ is the largest $h$ such that skill is positive at every horizon from $h = 1$ to $h$; the last column is the longest run of consecutive positive-skill horizons. They describe this dataset and protocol only. They are not universal predictability limits, and no predictive-accuracy test was applied.
