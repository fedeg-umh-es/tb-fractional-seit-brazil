# Bulletin of Mathematical Biology — Data and Code Availability Statements

This document provides formal, transparent statements regarding the provenance, accessibility, and archival status of the empirical dataset and computational code supporting the manuscript.

---

## 1. Data Availability Statement

### Formal Statement for Manuscript
The empirical dataset analyzed in this study comprises aggregate monthly tuberculosis notification counts for Brazil covering January 2001 through December 2022 ($N = 264$ consecutive monthly observations). The canonical observational file used directly by the computational pipeline is `data/raw/tb_mes.xlsx`, preserved unchanged in the project repository exactly as supplied by Amaury de Souza for this collaboration. Repository provenance records the original filename, file hash, structure, and ingestion history in `DATA_PROVENANCE.md` and `outputs/audits/source_manifest.csv`.

The 2001–2020 population denominator has been traced to the 2013 revision of the IBGE national population projection. For `casos`, four prespecified national DATASUS/SINAN TabNet configurations were audited against all 264 supplied monthly counts. None matched exactly; the closest, C1, differed in 99 months. Thus the exact original extraction configuration was not recovered. The supplied series remains unchanged and no audited TabNet query is represented as its verified acquisition route. The source file, audit record, and processed numerical evidence are held in the private repository. [AUTHOR CONFIRMATION REQUIRED BEFORE SUBMISSION: specify how the canonical observational file and reproducibility bundle can be accessed, and any conditions for reuse.]

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
The computational codebase implements the Caputo fractional-order numerical integrator, Differential Evolution calibration routines, profile-objective practical-identifiability analysis, equilibrium stability evaluations under Matignon's criterion, and expanding-window rolling-origin forecasting benchmarks in Python using NumPy, SciPy, Pandas, Statsmodels, and Pytest.

The complete codebase, configuration files, and automated test suite are maintained in a private version-controlled repository. The frozen computational state supporting the reported numerical evidence is Git commit `13015847a6f364505391d4f6e24d9c4c994669ff`; later editorial and documentation commits do not redefine the canonical computational evidence. During peer review, a reproducible repository bundle or private repository access can be provided to editors and reviewers. No public archival DOI currently exists. Any future public archival release or DOI must be created only after explicit author approval and must correspond to a verified reproducible release.

---

## 3. Archival and Submission Metadata

```text
REPOSITORY_OWNER = fedeg
REPOSITORY_CURRENT_STATUS = PRIVATE_VERSION_CONTROLLED_REPOSITORY
CANONICAL_COMPUTATIONAL_COMMIT = 13015847a6f364505391d4f6e24d9c4c994669ff
CANONICAL_DATA_FILE = data/raw/tb_mes.xlsx
CANONICAL_DATA_SHA256 = 93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b
POPULACAO_PROVENANCE = RESOLVED
CASOS_PROVENANCE = NO_EXACT_MATCH
CANDIDATE_SET_EXHAUSTED = YES
ORIGINAL_EXTERNAL_DATA_URL_VERIFIED = NO
PUBLIC_ARCHIVAL_DOI_EXISTS_NOW = NO
PEER_REVIEW_ACCESS = PENDING_AUTHOR_CONFIRMATION_OF_ROUTE_AND_REUSE_CONDITIONS
PUBLIC_RELEASE = REQUIRES_EXPLICIT_AUTHOR_DECISION
```
