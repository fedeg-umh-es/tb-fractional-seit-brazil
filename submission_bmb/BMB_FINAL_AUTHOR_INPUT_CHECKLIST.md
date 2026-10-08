# Bulletin of Mathematical Biology — Final Author Input Checklist

This document tracks confirmed author instructions, independently verified contact metadata, and declarations still needing explicit confirmation before submission to the *Bulletin of Mathematical Biology*.

The author has now instructed: **Amaury de Souza** as first and corresponding author, and **Federico García Crespi** as second author; no external funding. These editorial decisions replace the earlier unconfirmed metadata placeholders. Author contributions, conflicts, ethics determinations and dataset reuse permissions are not inferred.

---

## 1. Scientific/Editorial State Before Human Input

```text
SCIENTIFIC_EVIDENCE = FROZEN
DOCUMENTARY_TRUTH_REPAIR = COMPLETE_WITH_CASES_PROVENANCE_LIMITATION
STRUCTURAL_REPAIR = COMPLETE
CLAIM_PRECISION_AUDIT = PASS
CONTROLLED_PROSE_PASS = COMPLETE
CANONICAL_MANUSCRIPT_SYNC = COMPLETE
BMB_REQUIREMENTS_VERIFIED = 2026-09-23
CASOS_PROVENANCE = NO_EXACT_MATCH
CANDIDATE_SET_EXHAUSTED = YES
READY_FOR_AUTHOR_SCIENTIFIC_REVIEW = YES
READY_FOR_SUBMISSION = NO
```

No new experiment is required or authorized by the remaining items below.

---

## 2. Final scientific review requested from Amaury

Review the consolidated `submission_bmb/BMB_MANUSCRIPT.md` for the research question and
rationale, interpretation of the central within-family versus external-baseline finding,
limitations, Data Availability and the cases-provenance qualification, conclusion, and whether
the text reflects both researchers' scientific interpretation. Record requested changes or
explicit approval before final production. The four-candidate audit is closed; this review does
not itself authorize new filters, microdata, or model recalibration.

## 3. Required Human Decisions

### AUTHORSHIP AND ORDER
* **STATUS**: `CONFIRMED_BY_USER_FOR_DRAFT`
* **ORDER**: 1. Amaury de Souza; 2. Federico García Crespi.

### AFFILIATIONS
* **STATUS**: `PUBLIC_RECORD_VERIFIED_FOR_DRAFT; VERIFY_AT_FINAL_AUTHOR_PROOF`
* **Amaury**: Institute of Physics, Federal University of Mato Grosso do Sul, Campo Grande, Brazil.
* **Federico**: Department of Computer Engineering, Universidad Miguel Hernández de Elche, Elche, Spain.
* **RULE**: public-profile information may be used as a candidate for checking but must not replace author confirmation.

### CORRESPONDING AUTHOR
* **STATUS**: `IDENTITY_CONFIRMED_BY_USER; EMAIL_FROM_PUBLIC_PUBLICATION`
* **NAME**: Amaury de Souza.
* **EMAIL**: amaury.souza@ufms.br (verify current delivery before submission).

### ORCID
* **STATUS**: `AMAURY_VERIFIED; FEDERICO_OPTIONAL`
* **Amaury**: https://orcid.org/0000-0001-8168-1482.
* **Federico**: omit until the identifier is supplied/verified.

### AUTHOR CONTRIBUTIONS
* **STATUS**: `BLOCKED_HUMAN_DECISION`
* **REQUIRED INPUT**: contribution statement for every final author; CRediT may be used.
* **RULE**: AI must not infer contribution roles from repository commits or conversation history.

### FUNDING
* **STATUS**: `CONFIRMED_BY_USER`
* **STATEMENT**: This research received no external funding.

### COMPETING INTERESTS
* **STATUS**: `BLOCKED_HUMAN_CONFIRMATION`
* **REQUIRED INPUT**: financial and non-financial competing-interest disclosure for all final authors, or confirmation that none apply.

### ETHICS / CONSENT
* **STATUS**: `BLOCKED_HUMAN_OR_INSTITUTIONAL_CONFIRMATION`
* **REPOSITORY FACT**: the canonical observational file contains aggregate monthly national observations and no individual-level or directly identifiable patient fields.
* **REQUIRED INPUT**: confirm the appropriate ethics/consent statement under the authors' institutional requirements and the journal policy.
* **RULE**: the absence of individual-level data does not authorize AI to declare an institutional ethics exemption on the authors' behalf.

### DATA PROVENANCE AND ACCESS
* **STATUS**: `BLOCKED_FOR_FINAL_AUTHOR_ACCESS_DECISION`
* **REPOSITORY FACTS**:
  - canonical file: `data/raw/tb_mes.xlsx`;
  - 264 monthly observations, January 2001–December 2022;
  - supplied by Amaury de Souza for this collaboration;
  - hash/provenance recorded;
  - 2001–2020 population provenance is resolved to the IBGE 2013 projection;
  - the closed C1–C4 DATASUS/SINAN audit did not exactly reconstruct the supplied `casos` series (C1 closest: 99/264 discrepant months);
  - original case-extraction settings were not recovered;
  - project repository is public; dataset reuse conditions remain pending author confirmation.
* **REQUIRED INPUT**: confirm how editors and reviewers can access the canonical file and reproducibility bundle, whether public release is permitted, and any conditions for reuse. An original acquisition record may be documented if the authors already possess one; it does not reopen the closed candidate search.
* **RULE**: do not attribute the canonical case series to an audited SINAN/DATASUS extraction configuration without evidence of an exact match or an independently verified original record.

---

## 4. Items Already Closed

### CODE AVAILABILITY
* **STATUS**: `DRAFT_COMPLETE`
* Canonical evidence-freeze commit: `5617559bb0bf43d7223a7bb2491ab1e41fa4a084`.
* Repository public; canonical file and reproducibility bundle reuse conditions remain pending author confirmation.
* No public archival DOI currently exists.
* Use `profile-objective`, not `profile-likelihood`.

### AI DISCLOSURE
* **STATUS**: `DRAFT_COMPLETE`
* Methods §2.13 records generative AI/LLM assistance and preserves human accountability.

### TITLE
* **STATUS**: `READY_FOR_HUMAN_APPROVAL`
* Current title is claim-safe; no scientific reframe is recommended.

### ABSTRACT
* **STATUS**: `READY_FOR_HUMAN_APPROVAL`
* Approximately 208 words; BMB requirement verified as 150–250 words.

### COVER LETTER
* **STATUS**: `SCIENTIFIC_TEXT_COMPLETE_METADATA_PENDING`
* Contribution is bounded to the case-study evidence; corresponding-author sign-off remains pending.

---

## 5. Minimal Human Input Block

To unlock final production, the authors need to return one consolidated block containing:

```text
FINAL_AUTHOR_LIST_AND_ORDER = Amaury de Souza; Federico García Crespi
AFFILIATION_EACH_AUTHOR = UFMS Institute of Physics; UMH Department of Computer Engineering (verify final editorial forms)
CORRESPONDING_AUTHOR = Amaury de Souza
CORRESPONDING_EMAIL = amaury.souza@ufms.br (verify active)
ORCID_EACH_AUTHOR = Amaury 0000-0001-8168-1482; Federico optional/unconfirmed
AUTHOR_CONTRIBUTIONS = pending confirmation
FUNDING = No external funding
COMPETING_INTERESTS =
ETHICS_CONSENT_POSITION =
DATA_PROVENANCE_ACCESS_DECISION =
FINAL_SCIENTIFIC_REVIEW = APPROVE / CHANGES_REQUIRED
```

---

## 6. Gate After Human Input

Once the block above is confirmed, the remaining workflow is production-only:

```text
insert metadata/declarations
-> generate Springer Nature LaTeX package
-> insert figures/tables/SI
-> final reference-style conversion
-> continuous line + page numbering
-> compile PDF
-> visual/scientific production QA
-> PRE_SUBMISSION_PACKAGE_COMPLETE
```

No numerical result should be recalculated during this gate unless a genuine reproducibility error is discovered.
