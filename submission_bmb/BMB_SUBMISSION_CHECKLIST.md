# Bulletin of Mathematical Biology — Submission Checklist

This checklist is the current pre-submission status for the BMB package after documentary repair, structural revision, claim audit, controlled prose pass, and current official BMB requirement verification.

---

## Current Status

| Item | Status | Notes |
|---|:---:|---|
| Article type | VERIFIED | Original Research; do not reclassify as Methods because no new general mathematical method is introduced. |
| Title | VERIFIED_FOR_AUTHOR_REVIEW | Avoids generic fractional-superiority claims; final human approval pending. |
| Abstract | VERIFIED | Approximately 208 words; current BMB requirement is 150–250 words. |
| Keywords | VERIFIED | 6 keywords; current BMB requirement is 4–6. |
| Dominant scientific question | VERIFIED | Within-family fractional improvement -> forecasting skill beyond the model family. |
| Identifiability hierarchy | VERIFIED | Explicitly secondary interpretive axis; not a co-equal novelty claim. |
| Methods forecasting protocol | VERIFIED | 13 expanding-window origins x 12 horizons; persistence, seasonal naive, SARIMA. |
| Methods prespecification terminology | REPAIRED | Uses `prespecified/documented before execution`, not external-preregistration language. |
| Data provenance wording | REPAIRED / AUTHOR REVIEW PENDING | Population 2001–2020 traces to IBGE 2013. Cases audit C1–C4 is closed with no exact reconstruction; C1 is closest (99/264 discrepant months). The supplied series remains unchanged. |
| Gate 2 / novelty language | VERIFIED | No first/never/unprecedented claim; adjacent precedents acknowledged. |
| Results architecture | VERIFIED | Finding-first; within-family result precedes external-baseline turning point; identifiability secondary. |
| Discussion architecture | VERIFIED | Turning point leads; literature positioning separated; mechanistic axis bounded; methodological implication closes section. |
| Conclusion hierarchy | VERIFIED | Returns to dominant forecasting question; seasonal-naive exception retained explicitly. |
| Canonical manuscript sync | COMPLETE | `submission_bmb/BMB_MANUSCRIPT.md` is synchronized with the repaired source sections. |
| Claim-precision audit | PASS | C01–C11 and M01–M04 audited in `submission_bmb/PRE_SUBMISSION_CLAIM_AUDIT.md`. |
| Controlled prose pass | COMPLETE | Prose revised selectively; Methods/Results not stylistically rewritten where no scientific communication gain justified it. |
| References | VERIFIED_CONTENT | 20 cited / 20 listed, including the IBGE population source; DOI audit passed. Final BMB style conversion remains a production task. |
| Figure/table package | CLAIM_AUDITED | Captions distinguish within-family/external, descriptive/inferential, envelope/CI, and profile-objective terminology. |
| Data availability text | LIMITATION_DRAFTED / BLOCKED_FOR_AUTHOR_ACCESS_CONFIRMATION | BMB requires a statement explaining how supporting data can be accessed and any reuse conditions. Confirm an actual sharing route; do not imply that an audited TabNet query produced the canonical case series. |
| Code availability text | DRAFT_COMPLETE | Frozen computational commit `13015847a6f364505391d4f6e24d9c4c994669ff`; private repository; no archival DOI currently exists. |
| AI/LLM disclosure | VERIFIED_AS_DRAFT | Methods §2.13 satisfies current BMB instruction to document generative LLM use; human accountability retained. |
| Cover letter framing | CLAIM_AUDITED | Contribution bounded to case-study evidence; no universal fractional-model claim. |
| Current BMB scope/requirements | VERIFIED_2026-09-23 | Official [BMB submission guidelines](https://link.springer.com/journal/11538/submission-guidelines) rechecked, including Data Availability and editable-source requirements. |
| Authorship and order | BLOCKED | Final human author list/order required before submission. |
| Affiliations | BLOCKED | Final affiliations required. |
| Corresponding author/email | BLOCKED | Active corresponding-author email required. |
| ORCID | OPTIONAL/PENDING | Add if available. |
| Author contributions | BLOCKED | Final contribution statement required/strongly expected for transparency. |
| Funding | BLOCKED | Final funding/no-funding statement required. |
| Competing interests | BLOCKED | Financial and non-financial interests confirmation required. |
| Ethics applicability statement | BLOCKED_FOR_CONFIRMATION | Human/institutional confirmation required for aggregate/non-identifiable data and applicable wording. |
| Data provenance/access | BLOCKED_FOR_CONFIRMATION | Four prespecified cases queries are exhausted with no exact match. Confirm permitted access/redistribution for the supplied series and state conditions accurately; no new candidate search is planned. |
| Cover letter sign-off | BLOCKED_BY_METADATA | Corresponding-author metadata pending. |
| Editable LaTeX/Word source | FINAL_PRODUCTION_STEP | BMB requires complete editable source files; LaTeX recommended. |
| Compiled PDF | FINAL_PRODUCTION_STEP | Required with LaTeX source. |
| Continuous line numbering | FINAL_PRODUCTION_STEP | Required by current BMB guidelines. |
| Sequential page numbering | FINAL_PRODUCTION_STEP | Required by current BMB guidelines. |
| Figure accessibility/placement | FINAL_PRODUCTION_STEP | Descriptive captions complete; final pattern/contrast/placement QA pending. |
| Supplementary package | FINAL_PRODUCTION_STEP | Inventory complete; final file naming, citations, and packaging pending. |

---

## Editorial Gate

```text
BMB_PUBLISHING_MODEL = HYBRID
SCOPE_GATE = PASS_PLAUSIBLE
CONTRIBUTION_THRESHOLD_RISK = MEDIUM
ARTICLE_TYPE = ORIGINAL_RESEARCH
SCIENTIFIC_EXPANSION_RECOMMENDED = NO
JOURNAL_REROUTING_RECOMMENDED = NO
```

The remaining desk-reject risk is principally contribution threshold/editorial priority, not a missing experiment or obvious scope mismatch. Do not broaden the claims or reopen the evidence set merely to reduce this risk.

---

## Readiness Decision

```text
SCIENTIFIC_EVIDENCE_STATUS = FROZEN
GATE_2_EXTERNAL_VERIFICATION = CLOSED
CANONICAL_MANUSCRIPT = submission_bmb/BMB_MANUSCRIPT.md
CANONICAL_REFERENCE_AUDIT = manuscript_package/REFERENCE_AUDIT.md
COMPUTATIONAL_FREEZE_COMMIT = 13015847a6f364505391d4f6e24d9c4c994669ff
NEW_EXPERIMENT_REQUIRED = NO
DOCUMENTARY_TRUTH_REPAIR = COMPLETE_WITH_CASES_PROVENANCE_LIMITATION
STRUCTURAL_REPAIR = COMPLETE
CLAIM_PRECISION_AUDIT = PASS
CONTROLLED_PROSE_PASS = COMPLETE
CANONICAL_MANUSCRIPT_SYNC = COMPLETE
CURRENT_BMB_REQUIREMENTS_VERIFIED = 2026-09-23
CASOS_PROVENANCE = NO_EXACT_MATCH
CANDIDATE_SET_EXHAUSTED = YES
READY_FOR_AUTHOR_SCIENTIFIC_REVIEW = YES
FORMAL_HUMAN_BLOCKERS_REMAIN = YES
FINAL_PRODUCTION_QA = PENDING
READY_FOR_SUBMISSION = NO
```

The package is now ready for human scientific/author review. It must not be marked `READY_FOR_SUBMISSION = YES` until authorship, affiliations, corresponding-author metadata, contributions, funding, competing interests, ethics/data-access confirmations, and final compiled source/PDF QA are complete.
