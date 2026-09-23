# Bulletin of Mathematical Biology — Manuscript Declarations

This document tracks declaration text that still requires final human confirmation before submission.

---

## 1. Funding
[AUTHOR INPUT REQUIRED: State funding sources and grant numbers, or confirm an explicit no-funding statement consistent with the journal requirements.]

---

## 2. Competing Interests
[AUTHOR CONFIRMATION REQUIRED: Confirm that all final authors have no relevant financial or non-financial interests, or provide the required disclosures.]

---

## 3. Author Contributions
[AUTHOR INPUT REQUIRED: Final contribution statement for every confirmed author. CRediT taxonomy may be used, but no contribution roles are assumed until the final author list is confirmed.]

---

## 4. Ethics Approval and Consent to Participate
[AUTHOR CONFIRMATION REQUIRED: Confirm that the analysis uses only aggregate national monthly notification counts with no individual-level or identifiable patient data. If confirmed, state the applicable ethics/consent position in wording consistent with institutional and journal requirements. The repository does not independently establish the original public acquisition route for the supplied observational file.]

---

## 5. Consent for Publication
Not applicable unless the final manuscript includes identifiable individual material, which the present manuscript does not.

---

## 6. Data Availability
The canonical observational dataset analyzed in this study is the aggregate monthly Brazil tuberculosis series stored as `data/raw/tb_mes.xlsx`, covering January 2001 through December 2022 ($N=264$). The file is preserved unchanged as supplied by Amaury de Souza for this collaboration and is used directly by the computational pipeline. Repository provenance, including the source-file hash and structural audit, is recorded in `DATA_PROVENANCE.md` and `outputs/audits/source_manifest.csv`.

The 2001–2020 population denominator is traced to the IBGE 2013 projection. A four-configuration DATASUS/SINAN TabNet audit did not exactly reconstruct the supplied case series; the closest configuration differed in 99 of 264 months. The original case-extraction settings therefore remain unrecovered. [AUTHOR CONFIRMATION REQUIRED BEFORE SUBMISSION: state the permitted access route for the canonical file and bundle, with any reuse conditions.]

See `submission_bmb/BMB_DATA_CODE_AVAILABILITY.md` for full provenance and release planning.

---

## 7. Code Availability
The computational code implementing the numerical fractional differential equation solver, Differential Evolution calibration, profile-objective practical-identifiability analysis, equilibrium stability analysis, and rolling-origin forecasting benchmarks is tied to frozen computational commit `13015847a6f364505391d4f6e24d9c4c994669ff`.

Editorial/documentation commits after this freeze do not modify canonical numerical evidence. The repository is private; a reproducible repository bundle or private access can be supplied during peer review. No public archival DOI currently exists.

---

## 8. AI Assistance Disclosure
Use of Large Language Model and AI-assisted tools is documented in Methods §2.13 of `submission_bmb/BMB_MANUSCRIPT.md` in accordance with the journal's current submission guidance.

AI tools were used under human oversight for drafting assistance, language editing, reference-format checks, structural review, and code-execution scripting. They were not treated as authors or scientific decision-makers and were not used as a source of empirical data or canonical numerical results. All AI-assisted text and code suggestions were reviewed against repository evidence. Final scientific responsibility remains with the confirmed human authors.
