# Final gate (2026-10-11)

```text
SUBMISSION_GATE = SUBMISSION_GATE_PASS_WITH_AUTHOR_ACTIONS
READY_FOR_SUBMISSION = NO   (author actions below are required first)
NOTHING_LEFT_FOR_CLAUDE_TO_CHANGE_IN_THE_SCIENCE = YES
```

What this status means: everything that depends on the repository is done and checked (see `SUBMISSION_CHECKLIST_2026-10-11.md`). What remains depends only on the authors, in this order.

## Author actions

1. **Zenodo deposit (fedeg).** Create the deposit and the release tag from the reviewed branch; choose the licence and the record type; decide whether the 21 files of `evidence_S1/` with local paths stay (`docs/decisions/ZENODO_DEPOSIT_NOTES_2026-10-11.md`). Then replace `[ZENODO_DOI]` and `[RELEASE_TAG]` in the manuscript (Data and Code Availability) and in the cover letter.
2. **Reuse conditions of the supplied dataset (both authors).** The Data Availability statement says that public availability is not a grant of reuse rights; confirm the wording with the person who supplied the file.
3. **Amaury (returns 13 October).** Sign `S1_DECISION_2026-10-11.md` (date and initials on the two sign-off lines); read the new text (Limitations, bound sensitivity, transient of E(t), the B1 paragraph), and confirm the cover letter. Optional: replace or add to the B1 paragraph with his own draft.
4. **Open reference flags (fedeg).** Read the 2023 correction notice of Cramer et al. (2022); confirm or drop the IBGE clause on the 2018 revision; replace Matignon (1996) by the primary source when you have it.
5. **Final review and submission.** Review the compiled PDF; choose the traditional subscription route in the system; confirm in the cover letter that the work is not published or under consideration elsewhere and that both authors approved it; both authors authorise the submission.

## What would reopen the science (not planned)

A rolling-origin evaluation with the wider bounds, an evaluation before 2020, a formal test of equal predictive accuracy, or a seasonal variant. All are declared as limitations. Any of them needs its own protocol and the authorisation of both authors.

## Records

Decisions: `docs/decisions/` (S1 decision, deferred analyses, agreement, availability texts, Zenodo notes). Analyses with protocols committed before execution: `analyses/A1_*` (bounds), `A2_transient_E_*`, `A2_tables_*`, `A3_*`. Reference audit and B1 sources: `literature_verification/`.
