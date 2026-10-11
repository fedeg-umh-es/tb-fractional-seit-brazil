# Upload manifest — what goes into the submission system

| # | File | Where it comes from | State |
|---|---|---|---|
| 1 | Manuscript PDF | compile the final project in Overleaf after filling `[ZENODO_DOI]` and `[RELEASE_TAG]` | after the Zenodo deposit |
| 2 | Editable source (all style files and figures) | export the Overleaf project as a zip, or use `manuscript_latex/TB_SEIT_BMB_overleaf_2026-10-11.zip` if nothing was edited in Overleaf (SHA-256 of the repository version: see below) | after step 1 |
| 3 | Cover letter | `submission_final/COVER_LETTER.md` (paste the text, or export to PDF) | after the Zenodo deposit |
| 4 | Figures F1-F5 (separate files, if the system asks) | `manuscript_latex/figures/*.pdf` | ready |
| 5 | Supplementary material | none required: the evidence is archived at Zenodo | n/a |

Repository package at the time of writing: `manuscript_latex/TB_SEIT_BMB_overleaf_2026-10-11.zip`; the current SHA-256 is printed by
`python manuscript_latex/tools/build_overleaf_zip.py` (the file is rebuilt deterministically).

Before uploading, in the PDF check: references in alphabetical order, Matignon marked as provisional (remove the provisional note only when the primary source has been verified), the placeholders replaced, Table and Figure numbers, the appendix tables.
