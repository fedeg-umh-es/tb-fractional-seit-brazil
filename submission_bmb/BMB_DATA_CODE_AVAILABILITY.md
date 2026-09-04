# Bulletin of Mathematical Biology — Data and Code Availability Statements

This document provides formal, transparent statements regarding the provenance, accessibility, and archival status of all empirical datasets and computational code supporting the manuscript.

---

## 1. Data Availability Statement

### Formal Statement for Manuscript
The empirical epidemiological data analyzed in this study comprise aggregate monthly tuberculosis notification records for Brazil covering the period January 2001 through December 2022 ($N = 264$ consecutive monthly counts). The raw surveillance records originate from Brazil's National System for Notifiable Diseases (Sistema de Informação de Agravos de Notificação, SINAN), maintained by the Ministry of Health of Brazil and publicly accessible via the DATASUS portal (https://datasus.saude.gov.br/). The curated monthly time series and processing scripts are hosted in the project GitHub repository, which will be made public prior to submission [FEDEG_INPUT_REQUIRED: insert repository URL once public].

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

The complete codebase, configuration files, and automated test suite are hosted in a Git repository that will be made public on GitHub prior to submission [FEDEG_INPUT_REQUIRED: insert repository URL once public]. The repository is structured for deterministic reproduction of all reported tables, figures, and numerical envelopes. Upon manuscript acceptance, a permanent, citable digital object identifier (DOI) will be minted via Zenodo.

---

## 3. Archival and Submission Metadata

```text
REPOSITORY_AUTHOR = fedeg
GITHUB_VISIBILITY = PUBLIC (to be made public)
REPO_VISIBILITY_ACTION = NOT_EXECUTED_AWAITING_EXPLICIT_GO
DATA_RESTRICTIONS = NONE (Public aggregate surveillance data)
PUBLIC_ARCHIVAL_DOI_EXISTS_NOW = NO (Deferred to post-acceptance)
ZENODO_ARCHIVE_RECOMMENDED = YES (Prior to final publication)
CODE_ARCHIVE_REQUIRED_BEFORE_SUBMISSION = NO (Public GitHub repository sufficient for submission)
```
