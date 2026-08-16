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
* **ACTION REQUIRED**: fedeg to provide ORCID identifier (e.g., `0000-000X-XXXX-XXXX`) or confirm omitted/not available.

### CRediT AUTHOR CONTRIBUTIONS
* **STATUS**: `AUTHOR_CONFIRMATION_REQUIRED`
* **MISSING INPUT**: Formal contributor role taxonomy mapping for all confirmed authors.
* **ACTION REQUIRED**: fedeg to confirm or adjust formal CRediT roles once author list is finalized.

### FUNDING
* **STATUS**: `AUTHOR_INPUT_REQUIRED`
* **MISSING INPUT**: Explicit funding declaration (`FUNDING`).
* **ACTION REQUIRED**: fedeg to provide funder name, grant numbers, and recipients, or confirm explicit text: *"The author(s) received no specific funding for this work."*

### ETHICS
* **STATUS**: `AUTHOR_OR_INSTITUTIONAL_CONFIRMATION_REQUIRED`
* **MISSING INPUT**: Formal confirmation of aggregate public surveillance data exemption (`ETHICS_CONFIRMATION`).
* **ACTION REQUIRED**: fedeg to confirm factual statement: study analyzed strictly publicly accessible, aggregated national notification counts (SINAN/DATASUS) with zero individual-level or identifiable patient data.

### COMPETING INTERESTS
* **STATUS**: `AUTHOR_CONFIRMATION_REQUIRED`
* **MISSING INPUT**: Formal conflict-of-interest declaration (`COMPETING_INTERESTS`).
* **ACTION REQUIRED**: fedeg to confirm *"The authors declare no competing interests."* or provide specific disclosures.

### DATA AVAILABILITY
* **STATUS**: `RESOLVED`
* **MISSING INPUT**: None.
* **ACTION REQUIRED**: Maintained as verified (SINAN/DATASUS aggregate monthly notification data 2001–2022, $N=264$).

### CODE AVAILABILITY
* **STATUS**: `RESOLVED`
* **MISSING INPUT**: None.
* **ACTION REQUIRED**: Publication-safe statement maintained for local reproducible Git repository (commit `13015847a6f364505391d4f6e24d9c4c994669ff`), with Zenodo archival release scheduled upon acceptance.

### AI DISCLOSURE
* **STATUS**: `RESOLVED`
* **MISSING INPUT**: None.
* **ACTION REQUIRED**: Springer Nature LLM policy compliant statement maintained (human author sole responsibility, AI assistance disclosed).

### TITLE
* **STATUS**: `RESOLVED`
* **MISSING INPUT**: None.
* **ACTION REQUIRED**: Title approved: *"Within-Family Error Reduction Versus External Forecasting Skill in Fractional-Order Compartmental Models: A Methodological Investigation of SEIT Tuberculosis Dynamics"*.

### ABSTRACT
* **STATUS**: `RESOLVED`
* **MISSING INPUT**: None.
* **ACTION REQUIRED**: Abstract approved (243 words, turning-point sentence locked).

### COVER LETTER
* **STATUS**: `AUTHOR_INPUT_REQUIRED`
* **MISSING INPUT**: Sign-off metadata (author name, affiliation, institutional email in signature block).
* **ACTION REQUIRED**: Insert confirmed author contact details into `submission_bmb/BMB_COVER_LETTER.md` upon receipt of metadata.

---

## 2. Hard Human Blockers Summary

The following human decisions remain pending before the package can be marked `READY_FOR_BMB_SUBMISSION = YES`:

1. **Author Identities and Order** (`FINAL_AUTHOR_LIST`)
2. **Institutional Affiliations** (`AUTHOR_1_AFFILIATION`, etc.)
3. **Corresponding Author Contact** (`AUTHOR_1_EMAIL`)
4. **Funding Declaration** (`FUNDING`)
5. **Ethics & Competing Interest Confirmations** (`ETHICS_CONFIRMATION`, `COMPETING_INTERESTS`)

---

## 3. Package Gate Status

```text
REPOSITORY_AUTHOR = fedeg
SCIENTIFIC_EVIDENCE_STATUS = FROZEN_AND_LOCKED
BMB_EDITORIAL_PACKAGING = COMPLETE
CODE_PUBLIC = NO (Local reproducible Git repository)
ARCHIVAL_DOI = ABSENT (To be minted upon acceptance)
ZENODO_ARCHIVE_RECOMMENDED = YES
READY_FOR_BMB_SUBMISSION = NO (Awaiting explicit human author metadata above)
FINAL_GATE_STATUS = BMB_PACKAGE_STILL_AWAITING_AUTHOR_INPUT
```
