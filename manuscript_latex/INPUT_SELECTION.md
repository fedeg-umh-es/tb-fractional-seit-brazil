# Which LaTeX source produced the PDF sent to Amaury on 2026-10-10 (Plan A, step 8.1)

Date of this record: 2026-10-11. Files are in `incoming/`, byte-identical to what fedeg uploaded.

| File | SHA-256 | Notes |
|---|---|---|
| `incoming/sent_to_Amaury_2026-10-10_1622.pdf` | `5073b20a…d2c6` | 19 pages, created 2026-10-10 16:22:01 UTC (pdfTeX 1.40.29) |
| `incoming/manuscript_2.tex` | `54843db5…7361` | candidate A (`manuscript (2).tex`) |
| `incoming/TB_SEIT_BMB_Springer_LaTeX_AUTHOR_REVIEW.zip` | `2b244940…23f` | candidate B; contains `manuscript.tex` (SHA-256 `79bde2a4…0743`), `manuscript.pdf` (21 pages, created 2026-10-10 15:28 UTC), class, style, `.bib` |

## Choice

**Active source: candidate A, `manuscript_2.tex`.** Candidate B is kept only for provenance and as the
origin of the class file (`sn-jnl.cls`), the style file and the six-entry `.bib`.

## Justification (text comparison, no compilation)

The sent PDF's text was extracted with `pdftotext` and compared with both candidates.

- The title of the sent PDF, "Within-Family Gains vs External Skill in Fractional SEIT Tuberculosis Forecasts", is the title of
  candidate A. Candidate B has a different title ("Within-Family Error Reduction Versus External
  Forecasting Skill ... A Methodological Investigation of SEIT Tuberculosis Dynamics").
- The abstract of the sent PDF equals candidate A's abstract word for word (the first sentence "An
  improvement over an integer-order epidemic model does not necessarily imply useful forecasts" is not in B).
- Ten sentences taken from different sections of candidate A (Methods, Results, Discussion,
  Declarations; e.g. "Origin-specific SARIMA coefficient estimates were not retained...", "The code was generated using
  artificial intelligence tools...") were all found in the sent PDF after removing hyphenation and line numbers.
- Candidate B is an earlier draft: its PDF was created 61 minutes earlier than the sent PDF, and its text
  does not contain the phrase "were not retained" (candidate A, 3 occurrences, as in the sent PDF).
- Amaury's e-mail quotes the title of candidate A and the sentences that are in A ("an unpublished working manuscript",
  "Kalizhanova before Kharazmi").

Limit: the match is by extracted text, not by byte or layout comparison; I did not compile either source.

## Files not used

`Asthma_Mortality_Brazil.pdf` (uploaded in the same message) is the manuscript of a different project. It was not
used and is not copied into the repository (`PROJECT_CANON.md`: no mixing of projects).
