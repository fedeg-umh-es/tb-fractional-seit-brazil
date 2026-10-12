# Upload manifest — what goes into the submission system

| # | File | Where it comes from | State |
|---|---|---|---|
| 1 | Manuscript PDF | `manuscript_latex/TB_SEIT_BMB_submission_flat_2026-10-12.pdf` (compiled with pdfLaTeX from the flat package, 27 pages, 0 errors) | ready |
| 2 | Editable source | `manuscript_latex/TB_SEIT_BMB_submission_flat_2026-10-12.zip`: one `manuscript.tex` (tables inlined, bibliography embedded), `sn-jnl.cls`, F1-F5 at the root; built by `python manuscript_latex/tools/build_submission_flat.py`. The first package (subfolders, `\input`, modified `.bst`, extra packages) was reported as "LaTeX unsupported" by the submission system on 2026-10-12 | ready |
| 3 | Cover letter | `submission_final/COVER_LETTER.pdf`, compiled with pdfLaTeX from `COVER_LETTER.tex` (article class, 2 pages) | ready |
| 4 | Figures F1-F5 (separate files, if the system asks) | `manuscript_latex/figures/*.pdf` | ready |
| 5 | Supplementary material | none required: the evidence is archived at Zenodo | n/a |

Repository package at the time of writing: `manuscript_latex/TB_SEIT_BMB_overleaf_2026-10-11.zip`; the current SHA-256 is printed by
`python manuscript_latex/tools/build_overleaf_zip.py` (the file is rebuilt deterministically).

Before uploading, in the PDF check: references in alphabetical order, Matignon marked as provisional (remove the provisional note only when the primary source has been verified), the placeholders replaced, Table and Figure numbers, the appendix tables.
