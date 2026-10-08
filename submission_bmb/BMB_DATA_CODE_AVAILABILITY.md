# Bulletin of Mathematical Biology — Data and Code Availability Statements

This document provides formal, transparent statements regarding the provenance, accessibility, and archival status of the empirical dataset and computational code supporting the manuscript.

---

## 1. Data Availability Statement

### Formal Statement for Manuscript
The canonical observational dataset analyzed in this study is the aggregate monthly Brazil tuberculosis series stored as `data/raw/tb_mes.xlsx`, covering January 2001 through December 2022 ($N=264$). The file is preserved unchanged as supplied by Amaury de Souza for this collaboration and is used directly by the computational pipeline. It is distributed in the public repository https://github.com/fedeg-umh-es/tb-fractional-seit-brazil. Repository provenance, including the source-file hash and structural audit, is recorded in `DATA_PROVENANCE.md` and `outputs/audits/source_manifest.csv`.

The 2001–2020 population denominator is traced to the 2013 revision of the IBGE national population projection. During a reproducibility audit, we attempted to reconstruct the supplied monthly case series through four prespecified DATASUS/SINAN TabNet configurations. None reproduced all 264 monthly values exactly; the closest differed in 99 months. The original extraction settings could therefore not be recovered. No specific DATASUS/SINAN query is presented as the verified source of the canonical case series. The workbook and reproducibility bundle are accessible through the public repository. The project software and documentation carry the MIT License; the license does not independently establish rights to redistribute the externally supplied workbook or resolve its unrecovered original extraction configuration.

### Access decision before submission
The [BMB submission guidelines](https://link.springer.com/journal/11538/submission-guidelines) require a Data Availability Statement explaining how supporting data can be accessed and any conditions for reuse. The authors must confirm a concrete access arrangement for the supplied file and bundle before removing the placeholder above. Public deposition is encouraged, not established here as mandatory for this aggregate series.

### Provenance Details
* **Repository source file**: `data/raw/tb_mes.xlsx`
* **Supplied by**: Amaury de Souza, for this collaboration
* **SHA-256**: `93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b`
* **Spatial Resolution**: National aggregate (Brazil)
* **Temporal Resolution**: Monthly ($2001\text{-}01$ to $2022\text{-}12$, $N = 264$)
* **Data Nature**: Aggregate monthly series; no individual-level or identifiable patient fields are present in the canonical observational file
* **Completeness**: 264 consecutive monthly rows; repository integrity audit reports 0 missing months and 0 duplicate dates
* **Population source (2001–2020)**: IBGE 2013 national population projection; see `DATA_PROVENANCE.md`
* **`casos` audit**: C1–C4 all `NO_EXACT_MATCH`; C1 closest (99/264 discrepant months); see `provenance/datasus/DATASUS_QUERY.md` and access logs
* **Original `casos` extraction settings/URL**: Not recovered or independently verified

---

## 2. Code Availability Statement

### Formal Statement for Manuscript
The computational code implementing the numerical fractional differential equation solver, Differential Evolution calibration, profile-objective practical-identifiability analysis, equilibrium stability analysis, and rolling-origin forecasting benchmarks is tied to canonical evidence-freeze commit `5617559bb0bf43d7223a7bb2491ab1e41fa4a084`. Editorial/documentation commits after this freeze do not modify canonical numerical evidence. The code, the canonical result tables and the supplied observational file are publicly available in the GitHub repository https://github.com/fedeg-umh-es/tb-fractional-seit-brazil. No archival DOI (e.g., Zenodo) currently exists for the repository. The MIT License applies to project-developed software and documentation, not by implication to the original supplied dataset or historical manuscript.

---

## 3. Archival and Submission Metadata

```text
REPOSITORY_OWNER = fedeg
REPOSITORY_CURRENT_STATUS = PUBLIC_VERSION_CONTROLLED_REPOSITORY
CANONICAL_EVIDENCE_FREEZE_COMMIT = 5617559bb0bf43d7223a7bb2491ab1e41fa4a084
CANONICAL_DATA_FILE = data/raw/tb_mes.xlsx
CANONICAL_DATA_SHA256 = 93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b
POPULACAO_PROVENANCE = RESOLVED
CASOS_PROVENANCE = NO_EXACT_MATCH
CANDIDATE_SET_EXHAUSTED = YES
ORIGINAL_EXTERNAL_DATA_URL_VERIFIED = NO
PUBLIC_ARCHIVAL_DOI_EXISTS_NOW = NO
PEER_REVIEW_ACCESS = PUBLIC_REPOSITORY_AVAILABLE
REUSE_CONDITIONS = MIT_FOR_PROJECT_SOFTWARE_AND_DOCUMENTATION; DATA_SOURCE_TERMS_NOT_INDEPENDENTLY_VERIFIED
```
