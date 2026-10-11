# TB-SEIT: first authorized global refit (ordinary observation)

**Human authorization:** 2026-10-08, Fedeg, phase 1 only. This package is an execution harness; it does **not** contain new scientific results. It has **not** run against the original dataset in this environment.

## Preconditions

Run in a clean *new local worktree*, based on the audited commit `b3ad21bb059eb5357742693a4d5072107dc0df63`. The earlier diagnostic was performed in `codex/observation-operator-ablation-20261008`. Preserve that worktree and the main branch. No edits to `results_canonical/`, manuscript, calibration or validation outputs. The raw `data/raw/tb_mes.xlsx` must exist in the worktree. Keep the original audit as the scientific motivation for this experiment.

## Running

Copy `run_global_refit.py` and `test_global_refit.py` into a NEW untracked directory under the worktree, e.g. `audits/observation_operator_refit_2026-10-08/`. Or keep them outside the repo and pass `--repo /path/to/worktree` to the script.

```sh
python -m pip install -e /path/to/tb-fractional-seit-brazil
python -m pytest -q /path/to/test_global_refit.py
python /path/to/run_global_refit.py --repo /path/to/worktree --preflight-only
python /path/to/run_global_refit.py --repo /path/to/worktree
```

The full run fits both models using SciPy differential evolution: `best1bin`, popsize=15, mutation=(0.5,1), recombination=0.7, tol=0.01, maxiter=1000, polish=False and **primary seed 20260815**. Bounds are the original model bounds; alpha is fixed to 1 in the integer run. Initialization and population extrapolation follow the canonical code. The objective is train RMSE for the **ordinary integral** of sigma*E over each month using corrected E states and composite trapezoids. Validation uses a single continuous simulation for 264 months, with no fitting or decisions based on 2021-2022 observations.

The mandatory preflight reproduces the October 8 frozen-theta operator audit to within 0.001 RMSE before any fitting. A mismatch stops the run. The run writes only under an untracked `results_global_primary/` directory next to the script; it refuses nonempty output or paths inside protected canonical directories. It hashes all tracked files before and after execution.

## Deliverables

- `global_refit_parameters.csv`: independently fitted vectors and optimizer diagnostics, primary seed only
- `global_refit_metrics.csv`: train/validation RMSE, MAE and bias for both models
- `fractional_predictions.csv` and `integer_predictions.csv`: 264 monthly predictions each
- `phase1_report.json`: source HEAD, raw-data hash, full method contract, preflight check, contrast, and file-integrity assertion

**Interpretation gate:** A fitted fractional-vs-integer difference in open-loop validation does **not** establish rolling-origin superiority, forecasting skill against benchmarks, or robustness of identifiability/R0. If the optimizer fails, the preflight fails, or the data or hashes do not match, STOP and report the issue. No second phase, extra seeds, parameter profiles, figures, manuscript updates, commit or push without the author's explicit next decision.

## Scientific claim guard

Do not infer biological memory from alpha less than one. A material improvement under the ordinary observation operator is not a general fractional superiority claim. The global comparison answers whether the original within-family advantage can persist under common physical observation after each model is independently fitted. A later rolling-origin reassessment would require a separate authorization and full train-only fit at each origin.
