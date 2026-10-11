# Submission checklist — Bulletin of Mathematical Biology (2026-10-11)

Evidence column: what was checked and where. "Authors" means the item needs the authors, not Claude.

| Item | Status | Evidence |
|---|---|---|
| Abstract length (BMB: 150-250 words) | PASS | 220 words by whitespace count in `manuscript_latex/manuscript.tex`; requirement confirmed in the BMB guidelines through a search snippet on 2026-10-11 |
| Keywords (repo record: 4-6) | PASS | 6 keywords; the 4-6 rule was verified on 2026-09-23 (`submission_bmb/BMB_SUBMISSION_CHECKLIST.md`) and could not be rechecked today (the guidelines page blocks automated access) |
| Editable source plus compiled PDF | READY | source package `manuscript_latex/TB_SEIT_BMB_overleaf_2026-10-11.zip` (class, style, bib, figures, tables); the PDF is compiled by the authors in Overleaf (compiled without errors, reported by fedeg on 2026-10-11) |
| Title page: authors, affiliations, ORCID, e-mail, corresponding author | READY, authors confirm | in `manuscript.tex`; corresponding author F. F. García Crespi as requested by A. de Souza |
| Declarations (funding, competing interests, authors' contributions, ethics, consent, data, code, AI use) | READY, authors confirm | section "Statements and Declarations" of `manuscript.tex` |
| Data and Code Availability with archive DOI | DONE (2026-10-11) | version DOI 10.5281/zenodo.23298329, release v1.0.0, filled in the manuscript (2 places) and the cover letter; record, archive MD5 and frozen-bundle verifier checked (see `docs/decisions/ZENODO_DEPOSIT_RECORD_2026-10-11.md`) |
| Line numbers | PASS | `\linenumbers` in the source |
| Figures | PASS | 5 vector PDFs from the frozen S1 package, unchanged (`manuscript_latex/figures/`); captions revised in the text, not in the figures |
| Tables | PASS | 6 in the text, 4 in the appendix; compile without errors |
| References | PASS with flags | 22 entries audited (`literature_verification/REFERENCE_AUDIT_2026-10-11.md`); one wrong entry corrected; flags: Cramer 2023 correction notice not read, IBGE clause on the 2018 revision, Matignon provisional, six entries supported by title only |
| Every reported number traceable | PASS with flags | `manuscript_latex/CLAIM_EVIDENCE_MATRIX.csv`: 119 rows, 104 VERIFIED, 15 NOT_VERIFIED (each with its reason) |
| No number from the retired operator presented as current | PASS | text search for 1.1542, 1.1892, 0.964, 688.8, "h = 7": no match in `manuscript.tex` |
| Repository tests and evidence integrity | PASS | `pytest` 133 passed; `verify_frozen_bundle.py` PASS (manifest SHA-256 `8e490eb4…faaa1`); `git diff --check` clean over the branch; protected folders unchanged |
| Claims discipline (no priority language, no general fractional superiority, no biological memory from alpha < 1, R0 envelope not a CI) | PASS | reviewed in `manuscript.tex`; sensitivity analysis states that alpha, sigma and the R0 envelope are conditional on the original bounds |
| Cover letter | READY, authors confirm | `submission_final/COVER_LETTER.md`; one bracketed confirmation (originality and approval by both authors) |
| Licences (code MIT, data CC BY 4.0) and reuse of the supplied dataset | PASS | `LICENSE`, `LICENSE-CC-BY-4.0.txt`, `LICENSES.md`; Data and Code Availability updated; decided by fedeg 2026-10-11 (Amaury's written confirmation not in the repository) |
| Route | AUTHORS | Bulletin of Mathematical Biology, traditional subscription route, no paid open access: choose it in the submission system |
| Suggested reviewers | AUTHORS | none proposed here; add if the system asks |
| Decision S1 signed | **OPEN** | `docs/decisions/S1_DECISION_2026-10-11.md`: both sign-off lines blank; agreement reported by fedeg (`AUTHOR_AGREEMENT_2026-10-11.md`) |
| Approval of the final text by both authors | **OPEN** | Amaury is away until 13 October |
| Authorisation to submit | **OPEN** | both authors |
