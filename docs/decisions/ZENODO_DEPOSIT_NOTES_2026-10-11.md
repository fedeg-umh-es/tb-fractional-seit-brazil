# Notes for the Zenodo deposit (2026-10-11)

For fedeg. Plan A, step 9. `CITATION.cff` and `.zenodo.json` are drafts at the repository root.
**No deposit was created.**

## Decisions that are yours

1. **Local paths in the frozen evidence.** 21 files under `evidence_S1/` contain absolute local
   paths (`/Users/fede/...`), 296 occurrences in total. They are provenance records (execution
   logs, JSON provenance, phase reports, verification scripts) and are covered by the manifest
   SHA-256 values, so cleaning them would break `verify_frozen_bundle.py`. Decide whether they
   remain in the public deposit. The files are:
   `phase1/{control_worktrees_before.json, verification.json, SCIENTIFIC_SUMMARY.md,
   package_provenance.json, comparison_sources.json, execution_result.json, execution.log,
   tb_global_refit_phase1/results_global_primary/phase1_report.json}`;
   `phase2/{execution_provenance.json, phase2_report.json, baseline_reuse_verification.json,
   phase1_tests_reverified.json, AUDIT_REPORT.md}`; `phase3/execution_provenance.json`;
   `SOURCE_PROVENANCE.json`; and under `verification/`: `phase2_zip/verify_phase2_zip_20261010.py`,
   `freeze_evidence_20261010.py`, `git_integrity.json`, `phase3_conformity/{existing_phase3_evidence/execution_provenance.json,
   chronology_fragments.jsonl, audit_phase3_conformity_20261010.py}`.
2. **Licence.** The repository has no licence file, and I did not choose one. Zenodo requires a
   licence for open access. Choose one (code and data may need different licences) and add it to
   `CITATION.cff` (`license`) and `.zenodo.json` (`license`).
3. **Authors.** Order, affiliations and ORCIDs are not verified in the repository (the
   submission checklist lists them as pending). The two drafts use "García Crespi, Federico" first
   and "de Souza, Amaury" second, only as placeholders. Affiliation and ORCID fields are omitted.
4. **Release tag and content.** The evidence commit `53eae10` is on the branch
   `evidence/s1-freeze-2026-10-10`. The deposit should be a tagged release that also contains the
   analyses of this branch (`analyses/`, `docs/decisions/`). Create the tag yourself after the pull
   request is reviewed, for example from the merge commit, and put it in `[RELEASE_TAG]`. If you use
   the Zenodo-GitHub integration, it reads `.zenodo.json`.
5. **Upload type.** `.zenodo.json` uses `software`, since the deposit is mainly code. If you prefer
   `dataset` or a mixed record, change that field.
6. **Version and DOI.** `version` and `doi` are not set in either file; the DOI is issued by the
   deposit. Update `CITATION.cff` after that, and fill `[ZENODO_DOI]` in the availability texts.

## What the drafts contain

Title, abstract, repository URL, keywords, the S1 evidence commit and date, and the placeholders
above. The abstract describes the study neutrally and makes no claim about results.
