# Bulletin of Mathematical Biology — Data and Code Availability Statements

This document provides formal, transparent statements regarding the provenance, accessibility, and archival status of all empirical datasets and computational code supporting the manuscript.

---

## 1. Data Availability Statement

### Formal Statement for Manuscript
The empirical epidemiological data analyzed in this study comprise aggregate monthly tuberculosis notification records for Brazil covering the period January 2001 through December 2022 ($N = 264$ consecutive monthly counts). The raw surveillance records originate from Brazil's National System for Notifiable Diseases (Sistema de Informação de Agravos de Notificação, SINAN), maintained by the Ministry of Health of Brazil and accessible via the DATASUS portal (https://datasus.saude.gov.br/). The curated, quality-controlled monthly time-series file utilized for all calibration and validation runs is provided within the project repository (`data/monthly_cases.csv`). All processed numerical artifacts generated during the analysis are stored in the canonical results repository directory (`results_canonical/`).

### Provenance Details
* **Source Agency**: Ministry of Health of Brazil / DATASUS / SINAN
* **Spatial Resolution**: National aggregate (Brazil)
* **Temporal Resolution**: Monthly ($2001\text{-}01$ to $2022\text{-}12$, $N = 264$)
* **Data Nature**: Public aggregate disease surveillance statistics (no individual patient records)
* **Completeness**: $100\%$ temporal continuity (0 missing observations, 0 duplicate months)

---

## 2. Code Availability Statement

### Formal Statement for Manuscript
The computational code implementing the Caputo fractional-order numerical integrator, Differential Evolution calibration routines, profile-likelihood practical-identifiability analysis, equilibrium stability evaluations under Matignon's criterion, and expanding-window rolling-origin forecasting benchmarks was developed by **fedeg** in Python (utilizing NumPy, SciPy, Pandas, Statsmodels, and Pytest). 

The complete codebase, configuration files, and automated test suite are maintained in a version-controlled repository (Git commit `13015847a6f364505391d4f6e24d9c4c994669ff`). The repository is structured for deterministic reproduction of all reported tables, figures, and numerical envelopes. Upon manuscript acceptance, a permanent, citable digital object identifier (DOI) will be minted via Zenodo. During peer review, the complete reproducible repository bundle or private repository access will be made available to editors and reviewers upon request.

---

## 3. Archival and Submission Metadata

```text
REPOSITORY_AUTHOR = fedeg
REPOSITORY_CURRENT_STATUS = LOCAL_REPRODUCIBLE_GIT_REPOSITORY
CANONICAL_COMMIT_HASH = 13015847a6f364505391d4f6e24d9c4c994669ff
DATA_RESTRICTIONS = NONE (Public aggregate surveillance data)
PUBLIC_ARCHIVAL_DOI_EXISTS_NOW = NO (Will be minted upon acceptance)
ZENODO_ARCHIVE_RECOMMENDED = YES (Prior to final publication)
CODE_ARCHIVE_REQUIRED_BEFORE_SUBMISSION = NO (Reviewer package / Git bundle sufficient for initial submission)
```
