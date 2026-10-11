# Zenodo deposit procedure (GitHub integration), for an agent with web access

Repository: `fedeg-umh-es/tb-fractional-seit-brazil`. Metadata come from `.zenodo.json` (Zenodo ignores `CITATION.cff` when both exist). Everything the archive needs is already in `main`.

## Rules for the agent

- Never type passwords or two-factor codes. If a login or consent screen appears, stop and ask the user to complete it.
- Take a screenshot after each step and keep the URLs visited.
- **Do not create the production release or press any publish button without a written "go" from the user.** A published Zenodo record cannot be deleted; only its metadata can be edited, or a new version added.
- Zenodo's page and menu names may have changed; follow https://help.zenodo.org/docs/github/ if a screen differs.

## Phase A: rehearsal in the Sandbox (no consequences)

1. Open https://sandbox.zenodo.org, log in with GitHub and authorise the application.
2. Open the GitHub settings page of the Sandbox, press "Sync now", and switch on `fedeg-umh-es/tb-fractional-seit-brazil`. If the owner is an organisation, its administrator must approve third-party access.
3. On GitHub, create a release from `main` with the tag `v0.0.0-sandbox`. Wait until the Sandbox shows the new record.
4. Check in the record: title; creators in the order de Souza, García Crespi, with ORCID and affiliation; licence CC BY 4.0; version; description; related identifier "isSupplementTo" pointing to the repository; the file list (a zip of the repository, about 13-14 MB). Check that the archive contains `LICENSE`, `LICENSES.md`, `CITATION.cff`, `evidence_S1/` and `manuscript_latex/`.
5. Report any field that did not validate (especially the `license` value) and stop. Do not continue to Phase B until the user has read the report.

## Phase B: production (only after the user's written "go")

1. Open https://zenodo.org, log in, and repeat steps 2 (Sync, switch on the repository).
2. On GitHub, create the release `v1.0.0` from `main` (title: "TB-SEIT S1 evidence and manuscript package"). Zenodo archives and publishes it automatically.
3. Open the published record and repeat the checks of Phase A step 4.
4. Write down the **version DOI** (`10.5281/zenodo.NNNNNNN`), the concept DOI, the tag, the date and the record URL in a text file for the user. The manuscript should cite the version DOI.
5. Download the archive zip, compute the SHA-256 of `evidence_S1/TB_SEIT_EVIDENCE_FREEZE_2026-10-10/artifact_manifest.json` (expected `8e490eb465fd125bf91177da8fc385366d387a69fd7fd81fab6f9851018faaa1`), and run `verification/verify_frozen_bundle.py` on the extracted copy; the result must be `PASS`.

## Phase C: close the manuscript (Claude Code in the repository)

Replace `[ZENODO_DOI]` and `[RELEASE_TAG]` in `manuscript_latex/manuscript.tex` (Data and Code Availability), `submission_final/COVER_LETTER.md` and `docs/decisions/AVAILABILITY_TEXTS_2026-10-11.md`; fill `doi`, `version` and `date-released` in `CITATION.cff`; rebuild with `python manuscript_latex/tools/build_overleaf_zip.py` and `python manuscript_latex/tools/build_claim_matrix.py`; commit.
After the article is published, add its DOI to the Zenodo record as a related identifier (metadata edit; no new version).
