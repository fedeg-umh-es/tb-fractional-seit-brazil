# Zenodo deposit: decisions and state (2026-10-11)

For fedeg. `CITATION.cff` and `.zenodo.json` are ready; **the deposit itself has not been created.**

## Decisions (reported by fedeg on 2026-10-11)

| # | Decision | Where it is applied |
|---|---|---|
| 1 | Data (including the supplied series) under **CC BY 4.0**; code under **MIT** | `LICENSE`, `LICENSE-CC-BY-4.0.txt`, `LICENSES.md`; `.zenodo.json` (`license: cc-by-4.0`, record level); `CITATION.cff` (`MIT`, `CC-BY-4.0`); manuscript Data and Code Availability |
| 2 | **Option C**: `manuscript/source/BIOMATEMATICA_UNICAMP.docx` stays in the archive | no `export-ignore`; `LICENSES.md` carves it out ("rights remain with its authors unless they state otherwise"); the manuscript no longer says the original materials are "not publicly available" and says a copy of the working manuscript is archived with the code |
| 3 | The 21 files of `evidence_S1/` with local paths (`/Users/fede/...`) **stay unchanged** (decided by Claude at fedeg's request) | cleaning them breaks the SHA-256 verification of the frozen bundle; the paths are provenance records, not credentials. They show the local user name `fede` |
| 4 | Authors, order, affiliations and ORCID accepted as in the manuscript (de Souza first, García Crespi corresponding) | `.zenodo.json`, `CITATION.cff` |
| 5 | PR #4 merged into `main` | the release tag should point to the merge commit on `main` |

## Points that remain

- The dataset licence and the `.docx` inclusion were decided by fedeg; Amaury's own written confirmation of both is not in the repository.
- `.zenodo.json` accepts one record-level licence; MIT for the code is stated in `LICENSE` and in the record notes. Check in the Sandbox that the `license` value `cc-by-4.0` validates.
- The archived manuscript source contains `[ZENODO_DOI]` and `[RELEASE_TAG]`; it cannot contain its own DOI.
- After the deposit: fill the placeholders (manuscript, cover letter, `CITATION.cff` `doi`/`date-released`) and rebuild the Overleaf package.

Procedure (rehearsal in the Sandbox first, then the production release): `ZENODO_DEPOSIT_PROCEDURE_2026-10-11.md`.
