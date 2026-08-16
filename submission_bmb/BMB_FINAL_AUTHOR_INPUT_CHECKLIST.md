# Bulletin of Mathematical Biology — Final Author Input Checklist

This document provides a single, consolidated checklist of all human author decisions and metadata inputs required from **fedeg** prior to final submission to the *Bulletin of Mathematical Biology* (Springer Nature).

---

## 1. Metadata & Submission Input Matrix

| Category | Status | Missing Human Input | Action Required from fedeg |
| :--- | :---: | :--- | :--- |
| **AUTHORSHIP** | `AUTHOR_INPUT_REQUIRED` | Confirmation of complete author list (sole author vs. coauthors). | Confirm author list for manuscript title page and Springer Editorial Manager portal. |
| **AFFILIATIONS** | `AUTHOR_INPUT_REQUIRED` | Institutional department, institution name, city, and country. | Provide exact affiliation text to replace placeholder `[AUTHOR INPUT REQUIRED: Department / Institution...]`. |
| **CORRESPONDING AUTHOR** | `AUTHOR_INPUT_REQUIRED` | Primary corresponding email address. | Provide official corresponding email address. |
| **ORCID** | `AUTHOR_INPUT_REQUIRED` | ORCID identifier(s). | Provide 16-digit ORCID iD (e.g., `0000-000X-XXXX-XXXX`). |
| **CRediT ROLES** | `AUTHOR_INPUT_REQUIRED` | Confirmation of formal contributor roles. | Confirm or adjust proposed CRediT roles in `BMB_DECLARATIONS.md`. |
| **FUNDING** | `AUTHOR_INPUT_REQUIRED` | Specific grant/funding statement. | Confirm if funded (provide agency and grant number) or confirm explicit text: *"The author(s) received no specific funding for this work."* |
| **ETHICS** | `AUTHOR_CONFIRMATION_REQUIRED` | Final author sign-off on public data exemption statement. | Confirm ethics statement: *"Not applicable. Analyzes publicly available, anonymous, aggregate national surveillance data."* |
| **COMPETING INTERESTS** | `AUTHOR_CONFIRMATION_REQUIRED` | Formal conflict-of-interest sign-off. | Confirm declaration: *"The author(s) declare no competing interests."* |
| **DATA AVAILABILITY** | `VERIFIED_READY` | None (SINAN / DATASUS provenance fully documented). | Ready for submission. |
| **CODE AVAILABILITY** | `VERIFIED_READY` | None for initial submission (repository commit `13015847a6f364505391d4f6e24d9c4c994669ff` documented). | Ready. (Zenodo archive recommended upon manuscript acceptance). |
| **AI DISCLOSURE** | `VERIFIED_READY` | None (Springer Nature LLM policy compliant statement drafted). | Ready for submission. |
| **TITLE** | `APPROVED` | None (`Within-Family Error Reduction Versus External Forecasting Skill...`). | Ready for submission. |
| **ABSTRACT** | `APPROVED` | None (243 words, turning-point control sentence locked). | Ready for submission. |
| **COVER LETTER** | `AUTHOR_INPUT_REQUIRED` | Affiliation, email, and signature details in footer. | Fill affiliation and email in `BMB_COVER_LETTER.md`. |

---

## 2. Unresolved Human Decision Blockers Summary

The following exact items must be provided by **fedeg** to transition the package to `READY_FOR_BMB_SUBMISSION = YES`:

1. **Author Name & Affiliation**: Exact institutional affiliation for title page.
2. **Email Address**: Institutional corresponding author email.
3. **ORCID ID**: Author ORCID profile link.
4. **Funding Disclosure**: Grant details or confirmation of unfunded status.
5. **Coauthor Confirmation**: Confirmation whether manuscript has any additional coauthors or is sole-authored.

---

## 3. Submission Package Gate Status

```text
REPOSITORY_AUTHOR = fedeg
SCIENTIFIC_EVIDENCE_STATUS = FROZEN_AND_LOCKED
BMB_EDITORIAL_PACKAGING = COMPLETE
CODE_PUBLIC = NO (Local reproducible Git repository)
ARCHIVAL_DOI = ABSENT (To be minted upon acceptance)
ZENODO_ARCHIVE_RECOMMENDED = YES
READY_FOR_BMB_SUBMISSION = NO (Awaiting explicit human author metadata above)
FINAL_GATE_STATUS = BMB_PACKAGE_AWAITING_AUTHOR_INPUT
```
