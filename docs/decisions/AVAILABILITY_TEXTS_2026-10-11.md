# Code and Data Availability texts for the manuscript (draft, 2026-10-11)

Plan A, step 9. Draft texts with placeholders. They replace, at step 8, the statements in
`submission_bmb/BMB_DATA_CODE_AVAILABILITY.md`, which still cite the historical freeze commit
`5617559` (retired operator) and state that no DOI exists. The deposit on Zenodo is created by
fedeg; nothing was deposited here.

Placeholders: `10.5281/zenodo.23298329` (DOI of the deposit) and `v1.0.0` (tag of the released
version, see deposit notes).

## Code Availability

> The code implementing the fractional differential equation solver, the Differential Evolution
> calibration, the ordinary monthly observation operator, the practical-identifiability analysis,
> the stability analysis and the rolling-origin forecasting benchmarks, together with the numerical
> results supporting this article, is archived at Zenodo (https://doi.org/10.5281/zenodo.23298329; release
> v1.0.0) and is publicly available in the GitHub repository
> https://github.com/fedeg-umh-es/tb-fractional-seit-brazil. The evidence on which the results are
> based is the frozen package `evidence_S1/TB_SEIT_EVIDENCE_FREEZE_2026-10-10/` (branch
> `evidence/s1-freeze-2026-10-10`, commit `53eae1091f652ec0393707f4e0ae7b2ec4b43acb`), whose
> integrity can be checked with the verification script included in the package. Results obtained
> with an earlier observation operator are kept in the repository as historical evidence and are not
> used in this article.

## Data Availability

> The monthly aggregate series of tuberculosis cases in Brazil analysed here (January 2001 to
> December 2022, N = 264) is distributed in the repository at `data/raw/tb_mes.xlsx` (SHA-256
> `93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b`) and in the Zenodo deposit
> (https://doi.org/10.5281/zenodo.23298329). The file contains aggregate national counts and no individual-level
> fields. It is used as supplied by the second author; an audit of four DATASUS/SINAN TabNet
> configurations did not reproduce all 264 monthly values (the closest differed in 99 months), so the
> original extraction route could not be recovered. The population denominator for 2001-2020 is
> traced to the 2013 revision of the IBGE national projection. [AUTHOR CONFIRMATION REQUIRED:
> reuse conditions of the supplied file.]

## Notes

- The repository is public (HTTP 200 without authentication on 2026-10-11).
- Licences decided by the authors on 2026-10-11: CC BY 4.0 for the data and MIT for the code (`LICENSES.md`).
- The sentence about the second author refers to the current repository wording ("supplied by
  Amaury de Souza for this collaboration"); confirm it with him.
