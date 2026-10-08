# Bulletin of Mathematical Biology — Manuscript Declarations

This document tracks declaration text that still requires final human confirmation before submission.

---

## 1. Funding
This research received no external funding.

---

## 2. Competing Interests
The authors declare that they have no competing financial or non-financial interests.

---

## 3. Author Contributions
Amaury de Souza: Resources; Data curation; Conceptualization; Writing – review and editing. Federico García Crespi: Methodology; Software; Formal analysis; Validation; Visualization; Writing – original draft; Writing – review and editing. Both authors: review and approval of the final manuscript.

---

## 4. Ethics Approval and Consent to Participate
Ethics approval and consent to participate: Not applicable. This study analyzes publicly available, aggregate tuberculosis surveillance data without individual-level or identifiable records; no human participants were recruited or contacted. The canonical monthly series was supplied by a collaborator, and its exact original extraction settings could not be independently reconstructed.

---

## 5. Consent for Publication
Not applicable unless the final manuscript includes identifiable individual material, which the present manuscript does not.

---

## 6. Data Availability
The canonical observational dataset analyzed in this study is the aggregate monthly Brazil tuberculosis series stored as `data/raw/tb_mes.xlsx`, covering January 2001 through December 2022 ($N=264$). The file is preserved unchanged as supplied by Amaury de Souza for this collaboration and is used directly by the computational pipeline. It is distributed in the public repository https://github.com/fedeg-umh-es/tb-fractional-seit-brazil. Repository provenance, including the source-file hash and structural audit, is recorded in `DATA_PROVENANCE.md` and `outputs/audits/source_manifest.csv`.

The 2001–2020 population denominator is traced to the 2013 revision of the IBGE national population projection. During a reproducibility audit, we attempted to reconstruct the supplied monthly case series through four prespecified DATASUS/SINAN TabNet configurations. None reproduced all 264 monthly values exactly; the closest differed in 99 months. The original extraction settings could therefore not be recovered. No specific DATASUS/SINAN query is presented as the verified source of the canonical case series. The dataset file and reproducibility bundle are accessible through the public repository linked above. The original supplier's authorization for further redistribution and the applicable reuse conditions have not been documented and require corresponding-author confirmation before submission.

---

## 7. Code Availability
The computational code implementing the numerical fractional differential equation solver, Differential Evolution calibration, profile-objective practical-identifiability analysis, equilibrium stability analysis, and rolling-origin forecasting benchmarks is tied to canonical evidence-freeze commit `5617559bb0bf43d7223a7bb2491ab1e41fa4a084`. Editorial/documentation commits after this freeze do not modify canonical numerical evidence. The code, the canonical result tables and the supplied observational file are publicly available in the GitHub repository https://github.com/fedeg-umh-es/tb-fractional-seit-brazil. No archival DOI (e.g., Zenodo) currently exists for the repository.

---

## 8. AI Assistance Disclosure
Use of Large Language Model and AI-assisted tools is documented in Methods §2.13 of `submission_bmb/BMB_MANUSCRIPT.md` in accordance with the journal's current submission guidance.

AI tools were used under human oversight for drafting assistance, language editing, reference-format checks, structural review, and code-execution scripting. They were not treated as authors or scientific decision-makers and were not used as a source of empirical data or canonical numerical results. All AI-assisted text and code suggestions were reviewed against repository evidence. Final scientific responsibility remains with the confirmed human authors.
