# Bulletin of Mathematical Biology — Final Author Input Checklist

This document tracks all human author decisions and metadata inputs required from **fedeg** prior to final submission to the *Bulletin of Mathematical Biology* (Springer Nature).

---

## 1. Item-by-Item Status & Action Required

### AUTHORSHIP
* **STATUS**: `BLOCKED`
* **MISSING INPUT**: Complete human-confirmed author list (`FINAL_AUTHOR_LIST`, `AUTHOR_ORDER`, `AUTHOR_1_FULL_NAME`, `ADDITIONAL_AUTHORS`).
* **ACTION REQUIRED**: fedeg to supply the exact author list and author order. Sole authorship cannot be assumed automatically without explicit confirmation.

### AFFILIATIONS
* **STATUS**: `BLOCKED`
* **MISSING INPUT**: Institutional affiliations (`AUTHOR_1_AFFILIATION`, `ADDITIONAL_AUTHOR_AFFILIATIONS`).
* **ACTION REQUIRED**: fedeg to provide department, institution/university, city, and country for each author.

### CORRESPONDING AUTHOR
* **STATUS**: `BLOCKED`
* **MISSING INPUT**: Designated corresponding author and official institutional email (`CORRESPONDING_AUTHOR`, `AUTHOR_1_EMAIL`).
* **ACTION REQUIRED**: fedeg to specify corresponding author name and active institutional contact email.

### ORCID
* **STATUS**: `AUTHOR_CONFIRMATION_REQUIRED`
* **MISSING INPUT**: 16-digit ORCID identifier(s) (`AUTHOR_1_ORCID`, `ADDITIONAL_AUTHOR_ORCIDS`).
* **ACTION REQUIRED**: fedeg to provide ORCID identifier or confirm omitted/not available.

### CRediT AUTHOR CONTRIBUTIONS
* **STATUS**: `AUTHOR_CONFIRMATION_REQUIRED`
* **MISSING INPUT**: Formal contributor role taxonomy mapping for all confirmed authors.
* **ACTION REQUIRED**: fedeg to confirm or adjust formal CRediT roles once author list is finalized.

### FUNDING
* **STATUS**: `AUTHOR_INPUT_REQUIRED`
* **MISSING INPUT**: Explicit funding declaration (`FUNDING`).
* **ACTION REQUIRED**: fedeg to provide funder name, grant numbers, and recipients, or confirm an explicit no-specific-funding statement consistent with the journal requirements.

### ETHICS
* **STATUS**: `AUTHOR_OR_INSTITUTIONAL_CONFIRMATION_REQUIRED`
* **MISSING INPUT**: Formal confirmation of the ethics position appropriate to the actual aggregate observational dataset and institutional requirements.
* **ACTION REQUIRED**: fedeg to confirm that the analyzed canonical file contains only aggregate national monthly observations and no individual-level or identifiable patient data, and to confirm the appropriate ethics/consent wording. The repository does not independently establish the original governmental acquisition route for the supplied file.

### COMPETING INTERESTS
* **STATUS**: `AUTHOR_CONFIRMATION_REQUIRED`
* **MISSING INPUT**: Formal conflict-of-interest declaration (`COMPETING_INTERESTS`).
* **ACTION REQUIRED**: fedeg to confirm no competing interests or provide specific disclosures.

### DATA AVAILABILITY
* **STATUS**: `DOCUMENTARY_REPAIR_COMPLETE_AUTHOR_PROVENANCE_CONFIRMATION_OPTIONAL`
* **MISSING INPUT**: No missing computational artifact. Optional author input remains if a verified original public acquisition URL/source record exists outside the repository.
* **ACTION REQUIRED**: Current statement is restricted to repository-verifiable facts: canonical file `data/raw/tb_mes.xlsx`, 264 monthly observations, supplied by Amaury de Souza, preserved hash/provenance, and peer-review access through the private reproducible repository/bundle. Do not restore a SINAN/DATASUS acquisition claim unless independently documented by the authors.

### CODE AVAILABILITY
* **STATUS**: `RESOLVED_FOR_PRE_SUBMISSION`
* **MISSING INPUT**: None for peer-review availability wording.
* **ACTION REQUIRED**: Maintain frozen computational commit `13015847a6f364505391d4f6e24d9c4c994669ff`, private-review access wording, and `profile-objective` terminology. No public DOI currently exists.

### AI DISCLOSURE
* **STATUS**: `RESOLVED_FOR_PRE_SUBMISSION`
* **MISSING INPUT**: None pending final author review.
* **ACTION REQUIRED**: Maintain human-author responsibility and disclosed AI assistance in Methods.

### TITLE
* **STATUS**: `PROVISIONALLY_FROZEN_PENDING_FINAL_MANUSCRIPT_PASS`
* **MISSING INPUT**: None.
* **ACTION REQUIRED**: Reassess only after structural/prose repair; do not alter scientific identity for journal fit.

### ABSTRACT
* **STATUS**: `PENDING_FINAL_INSIDE_OUT_SYNC`
* **MISSING INPUT**: None scientific.
* **ACTION REQUIRED**: Rewrite/polish only after Results, Discussion, Conclusion, and Introduction are structurally closed; retain BMB word-limit compliance and the turning-point result.

### COVER LETTER
* **STATUS**: `AUTHOR_INPUT_REQUIRED`
* **MISSING INPUT**: Sign-off metadata plus final manuscript wording.
* **ACTION REQUIRED**: Insert confirmed author contact details only after the manuscript pre-submission draft passes scientific and editorial QA.

---

## 2. Hard Human Blockers Summary

The following human decisions remain pending before the package can be marked `READY_FOR_BMB_SUBMISSION = YES`:

1. **Author identities and order**
2. **Institutional affiliations**
3. **Corresponding-author contact**
4. **Funding declaration**
5. **Ethics position**
6. **Competing-interest declaration**
7. **Final human scientific review of the repaired manuscript**

A verified original public-source acquisition record for the canonical dataset may also be supplied if available, but its absence must not be filled by assumption.

---

## 3. Package Gate Status

```text
REPOSITORY_OWNER = fedeg
SCIENTIFIC_EVIDENCE_STATUS = FROZEN_AND_LOCKED
DOCUMENTARY_TRUTH_REPAIR = IN_PROGRESS
MANUSCRIPT_STRUCTURAL_REPAIR = NEXT
CODE_PUBLIC = NO
ARCHIVAL_DOI = ABSENT
READY_FOR_BMB_SUBMISSION = NO
FINAL_GATE_STATUS = CONTROLLED_PRE_SUBMISSION_REPAIR
```
