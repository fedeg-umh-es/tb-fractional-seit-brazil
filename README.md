# tb-fractional-seit-brazil

> **Current status (2026-10-11).** The evidence of record is the S1 freeze, `evidence_S1/TB_SEIT_EVIDENCE_FREEZE_2026-10-10/` (ordinary monthly observation operator; commit `53eae1091f652ec0393707f4e0ae7b2ec4b43acb`).
> The manuscript source is in `manuscript_latex/`, the submission documents in `submission_final/`, decisions in `docs/decisions/`. `results_canonical/` and `outputs/` hold historical evidence of the retired operator.
> The text below describes the project at its initialisation (2026-08) and is kept as history.
> **Licences:** MIT for code, CC BY 4.0 for data, results and documents (`LICENSES.md`). **Cite:** `CITATION.cff`.

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
