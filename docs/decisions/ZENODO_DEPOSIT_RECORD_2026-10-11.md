# Zenodo deposit record (production), 2026-10-11

Facts reported by fedeg and checked against the public Zenodo API (https://zenodo.org/api/records/23298329) on 2026-10-11.

| Item | Value |
|---|---|
| Version DOI (cite this) | 10.5281/zenodo.23298329 |
| Concept DOI (all versions) | 10.5281/zenodo.23298328 |
| Release tag | v1.0.0 |
| Publication date | 2026-10-11 |
| Archived commit | `d6667ef` (main after PR #4; the zip folder is named `fedeg-umh-es-tb-fractional-seit-brazil-d6667ef`) |
| File | `fedeg-umh-es/tb-fractional-seit-brazil-v1.0.0.zip`, 15,899,425 bytes, MD5 `bf5e85bdb3c7b758985a001ee80b8f16` |
| Licence in the record | CC BY 4.0 (code under MIT is stated in the description and notes) |
| Resource type / version | software / 1.0.0 |
| Creators and order | de Souza, Amaury (ORCID 0000-0001-8168-1482, UFMS); García Crespi, Francisco Federico (ORCID 0000-0002-7129-7791, UMH) |
| Related identifier | isSupplementTo https://github.com/fedeg-umh-es/tb-fractional-seit-brazil |

## Checks done by Claude on the downloaded archive

- API file size and MD5 equal the downloaded file (bf5e85bd...).
- SHA-256 of `evidence_S1/TB_SEIT_EVIDENCE_FREEZE_2026-10-10/artifact_manifest.json` = `8e490eb465fd125bf91177da8fc385366d387a69fd7fd81fab6f9851018faaa1` (expected value).
- `verification/verify_frozen_bundle.py` run on the extracted bundle finished without assertion errors (780 predictions, 156 pairs per model, 29 claims, 66 freeze checks, 0 scientific executions).

## Known limits

- The archived `manuscript_latex/manuscript.tex` still contains the placeholders `[ZENODO_DOI]` and `[RELEASE_TAG]`, since a record cannot contain its own DOI. The record's notes say so. The manuscript submitted to the journal carries the DOI.
- The record has the repository state at `d6667ef`. Later commits (this file included) are not in the archive. If the final text changes in a way that matters for reproducibility, a new version (v1.0.1) is needed; changes to the manuscript text alone do not require it.
- The record is published; files cannot be deleted. Metadata can be edited (for example, add the article DOI as a related identifier after acceptance).
