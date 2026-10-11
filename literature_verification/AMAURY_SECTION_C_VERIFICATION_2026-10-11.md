# Verification of the references proposed in Section C of Amaury's e-mail (2026-10-11)

Plan A, step 8.5 (verification part only). Method: each reference was looked up in Crossref
(`api.crossref.org`, 2026-10-11) by title and author, and by DOI for those that did not appear in
the first search. A reference is `VERIFIED` when author(s), year, journal and volume of the
Crossref record match the citation proposed in the e-mail, and the pages and DOI come from that record.
Details: `AMAURY_SECTION_C_VERIFICATION_2026-10-11.csv`.

This only verifies that the references exist and are correctly cited. It does **not** decide which
ones enter the manuscript: the plan adds only those that are verified and actually cited in the
text, and the text (step 8) has not been written yet. I did not read any of the papers, so I do not
vouch for what they say; whatever a sentence attributes to them must be checked when it is written.

## Summary

| Status | Count | References |
|---|---|---|
| VERIFIED | 20 | Tashman 2000; Hyndman & Koehler 2006; Petropoulos et al. 2022; Diebold & Mariano 1995; Harvey, Leybourne & Newbold 1997; Giacomini & White 2006; Clark & West 2007; Gneiting & Raftery 2007; Funk et al. 2019; Reich et al. 2019; Raue et al. 2009; Chowell 2017; Wieland et al. 2021; van den Driessche & Watmough 2002; Ahmed, El-Sayed & El-Saka 2007; Diethelm, Ford & Freed 2004; Angstmann, Henry & McGann 2016; Storn & Price 1997; Hyndman & Khandakar 2008; Blower et al. 1995 |
| VERIFIED_WITH_FLAG | 1 | Cramer et al. 2022: the Crossref record has no page or article number and lists a 2023 correction notice (DOI 10.1073/pnas.2304076120). Read the correction before citing. |
| PARTIAL | 1 | Podlubny 1999: only chapters of the book are indexed; publisher and series are consistent, ISBN and book-level DOI are NOT_VERIFIED. |
| NOT_VERIFIED | 3 | Matignon 1996 (conference proceedings, no matching Crossref record); WHO Global Tuberculosis Report (edition to be fixed); Brazilian Ministry of Health bulletins (specific bulletin to be fixed) |

## Points for the authors

- Hyndman & Khandakar (2008) describes the R `forecast` package. The plan's optional ETS baseline,
  if activated, would use the Python `statsmodels` implementation, so this reference fits only if
  the text discusses automatic ETS/ARIMA selection in general.
- Crossref update records (`update-to`/`updated-by`, and retraction relations) were checked for the
  21 references that have a DOI. The only record found is the correction notice of Cramer et al.
  (2022); Funk et al. (2019) shows a `new_version` link that points to itself (preprint to journal
  version). No retraction record was found. This covers Crossref data only and is not an
  exhaustive retraction search.
- Matignon (1996) is the usual citation for the stability sector condition |arg(lambda)| > alpha*pi/2.
  If the manuscript cites it, its volume, pages and venue should be copied from the proceedings or
  a trustworthy bibliographic database, not from Crossref.
- Diethelm, Ford & Freed (2002, Nonlinear Dynamics 29, 3-22; DOI 10.1023/a:1016592219341) also
  verifies in Crossref. It is the solver reference of the repository (`src/tb_seit/solver.py`)
  and is not in Amaury's list; Amaury's list includes the 2004 error analysis.
- Alphabetical order (B10): Kalizhanova precedes Kharazmi. The `.bib` file to reorder is not in
  the repository yet (`manuscript_draft/references.bib` is the older draft); this is done at step 8.

## Update (2026-10-11, later)

A full audit of the cited references (bibliographic data, DOI, and claim-to-source correspondence) is in `REFERENCE_AUDIT_2026-10-11.md`. Changes with respect to the table above:
Matignon (1996) is now kept as a **provisional** entry (details from secondary sources); the WHO and Ministry of Health documents for B1 were located and read (`B1_SOURCE_EXTRACTS_2026-10-11.md`).
