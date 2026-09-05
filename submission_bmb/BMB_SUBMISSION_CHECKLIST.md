# Bulletin of Mathematical Biology — Submission Checklist

This checklist is the current pre-submission status for the BMB package. It distinguishes frozen scientific evidence, completed controlled manuscript repairs, and unresolved human metadata or provenance confirmations.

---

## Current Status

| Item | Status | Notes |
|---|:---:|---|
| Article type | VERIFIED | Original Research; manuscript identity unchanged. |
| Title | PROVISIONAL_VERIFIED | Current title avoids generic fractional-superiority claims; final title pass remains intentionally deferred until prose/abstract closure. |
| Abstract | PROVISIONAL_VERIFIED | 243 words and within BMB guidance; final Abstract pass remains intentionally deferred until manuscript prose closure. |
| Keywords | VERIFIED | 6 keywords. |
| Dominant scientific question | VERIFIED | Within-family fractional improvement -> forecasting skill beyond the model family. |
| Identifiability hierarchy | VERIFIED | Explicitly secondary interpretive axis; not a co-equal novelty claim. |
| Methods forecasting protocol | VERIFIED | 13 expanding-window origins x 12 horizons; persistence, seasonal naive, SARIMA. |
| Methods prespecification terminology | REPAIRED | Manuscript uses `prespecified/documented before execution`, not external-preregistration language. |
| Data provenance wording | REPAIRED_WITH_AUTHOR_CONFIRMATION_PENDING | Canonical file is `data/raw/tb_mes.xlsx`; repository does not independently document the original external acquisition URL/path. |
| Gate 2 / novelty language | VERIFIED | Historical-absence language removed; Discussion cites direct neighboring precedents. |
| Results architecture | REPAIRED | Finding-first; within-family result precedes external-baseline turning point; identifiability explicitly secondary. |
| Discussion architecture | REPAIRED | Turning point leads; literature positioning separated; mechanistic axis compressed and bounded; methodological implication closes section. |
| Conclusion hierarchy | REPAIRED | Returns to dominant forecasting question; mechanistic findings remain qualifiers. |
| Canonical manuscript sync | COMPLETE | `submission_bmb/BMB_MANUSCRIPT.md` synchronized with repaired Introduction, Methods, Results, Discussion, Conclusion and declarations. |
| References | VERIFIED | 19 cited / 19 listed; Roosa & Chowell DOI corrected to `10.1186/s12976-018-0097-6`. |
| Data availability text | DRAFT_COMPLETE / AUTHOR_CONFIRMATION_PENDING | Statement is repository-truthful; original external acquisition route remains for human confirmation if authors wish to state it. |
| Code availability text | DRAFT_COMPLETE | Computational freeze commit: `13015847a6f364505391d4f6e24d9c4c994669ff`; repository private; no archival DOI currently exists. |
| AI/LLM disclosure | VERIFIED_AS_DRAFT | Methods §2.13 documents use; final authors retain responsibility. |
| Cover letter framing | VERIFIED_AS_DRAFT | Scientific framing previously repaired; final consistency pass will follow manuscript claim audit. |
| Claim-precision audit | IN_PROGRESS | Must verify manuscript wording against frozen C01-C11 claim boundaries before prose humanization. |
| Authorship and order | BLOCKED | Final human author list/order not yet confirmed in package. |
| Affiliations | BLOCKED | Final affiliations not yet inserted. |
| Corresponding author/email | BLOCKED | Final contact not yet inserted. |
| ORCID | OPTIONAL/PENDING | Add if available. |
| Author contributions | BLOCKED | Must be confirmed for all final authors; CRediT may be used. |
| Funding | BLOCKED | Final funding/no-funding statement required. |
| Competing interests | BLOCKED | Final author confirmation required. |
| Ethics applicability statement | BLOCKED_FOR_CONFIRMATION | Confirm aggregate/non-identifiable data status and applicable institutional/journal wording; do not assume public-acquisition provenance from the repository. |
| Cover letter sign-off | BLOCKED_BY_METADATA | Scientific body revised; signature metadata pending. |
| Line/page numbering and final source-file packaging | FINAL_PRODUCTION_STEP | Apply at compiled submission stage. |

---

## Readiness Decision

```text
SCIENTIFIC_EVIDENCE_STATUS = FROZEN
GATE_2_EXTERNAL_VERIFICATION = CLOSED
CANONICAL_MANUSCRIPT = submission_bmb/BMB_MANUSCRIPT.md
CANONICAL_REFERENCE_AUDIT = manuscript_package/REFERENCE_AUDIT.md
COMPUTATIONAL_FREEZE_COMMIT = 13015847a6f364505391d4f6e24d9c4c994669ff
NEW_EXPERIMENT_REQUIRED = NO
DOCUMENTARY_TRUTH_REPAIR = COMPLETE
STRUCTURAL_REPAIR = COMPLETE
CANONICAL_MANUSCRIPT_SYNC = COMPLETE
CLAIM_PRECISION_AUDIT = IN_PROGRESS
FORMAL_HUMAN_BLOCKERS_REMAIN = YES
READY_FOR_AUTHOR_SCIENTIFIC_REVIEW = NOT_YET_REISSUED_AFTER_REPAIR
READY_FOR_SUBMISSION = NO
```

Do not mark the package `READY_FOR_AUTHOR_SCIENTIFIC_REVIEW` again until the post-repair claim-precision audit is complete. Do not mark `READY_FOR_SUBMISSION = YES` until human metadata/declaration confirmations, current BMB requirement verification, and final compiled source/PDF checks are complete.
