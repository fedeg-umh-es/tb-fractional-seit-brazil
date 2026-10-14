# Submission record — Bulletin of Mathematical Biology

| Item | Value | Source |
|---|---|---|
| Journal | Bulletin of Mathematical Biology (Springer Nature) | — |
| Submission ID | **BMAB-D-26-01213** | confirmation message, reported by fedeg |
| Date | 2026-10-12 | reported by fedeg |
| Submitting / corresponding author | Francisco Federico García Crespi (fedeg@umh.es) | — |
| Authorisation | both authors (`docs/decisions/AUTHOR_CONFIRMATIONS_2026-10-12.md`) | — |
| Route | traditional subscription; no paid open access | — |

## Files prepared for upload (state of `main` on 2026-10-12)

| Item | Repository file |
|---|---|
| Manuscript PDF | `manuscript_latex/TB_SEIT_BMB_submission_flat_2026-10-12.pdf` |
| LaTeX source | `manuscript_latex/TB_SEIT_BMB_submission_flat_2026-10-12.zip` (built by `tools/build_submission_flat.py`) |
| Cover letter | `submission_final/COVER_LETTER.pdf` |
| Abstract (PDF) | `submission_final/ABSTRACT.pdf` |
| Form fields | `submission_final/SUBMISSION_FORM_FIELDS_2026-10-12.md` |

The exact set uploaded and the final choices in the form (classifications, preferred editors, suggested reviewers) were made by fedeg in the system. The proposals discussed before submission were:

- Classifications: 50 Epidemiology (primary), 20 Computational Biology.
- Preferred editors, in order: Michael Plank, Jane Heffernan, Alexander P. Browning.
- Suggested reviewers: Gerardo Chowell (Georgia State), Christopher N. Angstmann (UNSW), Nicholas G. Reich (UMass Amherst), Sebastian Funk (LSHTM), Richard G. White (LSHTM), Johannes Bracher (KIT). Matthew Simpson was excluded because he is Editor-in-Chief of the journal.

## Editorial decision (2026-10-13)

| Item | Value | Source |
|---|---|---|
| Decision | **Desk reject**: not sent for external review | decision email, reported by fedeg |
| Date | 2026-10-13 | decision email |
| Decided by | Matthew Simpson, Editor-in-Chief | decision email |
| Title as given in the decision | *Within-Family Gains vs External Skill in Fractional SEIT Tuberculosis Forecasts* | decision email |

Stated reason, verbatim:

> The biological impact and implications of the work are not sufficiently strong to be suitable for our readership; therefore we are not sending your manuscript out for review.

The letter also uses the journal's standard wording ("the manuscript is either outside the scope or not suitable for our journal") and says the decision was made "based on an initial reading". Springer Nature announced an email from its Transfer Desk with journal suggestions within 48 hours.

### Reading of the decision

- **Explicit:** the reason is insufficient biological impact and implications for the journal's readership. No formal, policy, data or presentation defect is mentioned.
- **Strong inference:** the failed gate is contribution type and editorial priority, not evidence or scope of topic. The manuscript's main contribution is forecast-evaluation methodology (within-family improvement versus skill against external baselines). Its mechanistic results deliberately bound biological interpretation: β, γ and d are weakly identified, α is not read as biological memory, and DFE instability is stated as a property of the fitted system. The decision came one day after submission, which is consistent with a screening of title, abstract and cover letter.
- **Prior risk assessment:** `submission_bmb/BMB_DESK_REJECT_AUDIT.md` named contribution threshold as the principal desk-reject risk (rated low to moderate).
- **Not inferred:** the decision says nothing about the correctness of the analysis, and nothing in it calls for new experiments.

### Consequences

- No change was made to the manuscript, the evidence or the claims in response to this decision.
- The "After acceptance" step below no longer applies to this submission.
- Any further submission is a new routing decision by the authors. The Transfer Desk suggestions should be checked against the gate that failed here: whether the journal publishes forecast-evaluation methodology for epidemic models without requiring a new biological finding.
- The title in the decision letter matches the submitted package (`manuscript_latex/submission_flat/manuscript.tex`, `submission_final/COVER_LETTER.md`, `submission_final/SUBMISSION_FORM_FIELDS_2026-10-12.md`). Older files under `submission_bmb/`, such as `BMB_TITLE_OPTIONS.md`, still carry earlier titles and are superseded for this purpose.

## After acceptance (not applicable after the 2026-10-13 desk reject)

Add the article DOI to the Zenodo record 10.5281/zenodo.23298329 as a related identifier (metadata edit, no new version).
