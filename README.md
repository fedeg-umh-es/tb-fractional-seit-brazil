# tb-fractional-seit-brazil

## Scientific purpose

Independent reproducibility audit — and possible subsequent revision — of the manuscript
*"Fractional-Order SEIT Modeling, Predictive Validation, and Optimal Control of Tuberculosis
Dynamics in Brazil"*, an external collaboration with Amaury de Souza.

This is a standalone project. It is not related to, and must not be mixed with, any other
project's artifacts, methods, results, or repositories.

## Repository status

**Current stage: reproducibility preparation (repository initialization).**

No model calibration, parameter estimation, optimal-control simulation, or new scientific
claims have been produced in this repository. All numerical results currently reported in the
supplied manuscript (parameter estimates, R0, RMSE/MAE/AIC, the ~48% optimal-control reduction)
are **NOT YET VALIDATED** and must be treated as provisional until independently reproduced.
See `REPRODUCIBILITY_STATUS.md` for the live tracking table.

## Observational data

- Canonical period: **2001-01 through 2022-12** (264 monthly observations)
- Calibration split (future work): 2001-01 to 2020-12 (N = 240)
- Independent validation split (future work): 2021-01 to 2022-12 (N = 24)

See `DATA_PROVENANCE.md` and `PROJECT_CANON.md` for full detail.

## Directory map

```
data/raw/          immutable copy of the supplied dataset
data/processed/    derived/cleaned data (generated, not immutable)
manuscript/source/ immutable copy of the supplied manuscript
src/               reusable project code (none yet)
scripts/           standalone scripts (e.g. dataset integrity audit)
tests/             automated tests
outputs/tables/    generated tables
outputs/figures/   generated figures
outputs/audits/    machine-readable audit/provenance artifacts
docs/              supporting documentation
```

## Immutability rule

Files under `data/raw/` and `manuscript/source/` are the original, supplied source artifacts.
**They must never be modified, only read.** Any transformation must write its output elsewhere
(e.g. `data/processed/`, `outputs/`).
