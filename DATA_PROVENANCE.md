# Data provenance

## Canonical observational dataset

- Original filename: `tb_mes (1).xlsx`
- Repository filename: `data/raw/tb_mes.xlsx`
- Supplied by: Amaury de Souza, for this collaboration
- Ingestion date: 2026-08-15
- Byte size: 23028
- SHA-256: `93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b`
- Structure (non-scientific inspection): single worksheet `dados`, 264 data rows (plus header
  row), columns `data` (date), `ano` (year), `monthes` (month), `casos` (reported TB cases),
  `populacao` (population), `TI` (incidence rate). Sparse free-text notes present in column H
  for a subset of rows; no other data columns populated beyond column F.
- Observed date range in file: 2001-01-01 to 2022-12-01 (264 monthly rows), consistent with the
  canonical observational period 2001-01 through 2022-12 declared in `PROJECT_CANON.md`.

The original governmental (or other) source/download URL for this dataset is not present in the
supplied file or in any material provided by the collaborator. It is therefore **not recorded**
here and must not be invented or assumed.

## Manuscript source

- Original filename: `BIOMATEMATICA UNICAMP.docx`
- Repository filename: `manuscript/source/BIOMATEMATICA_UNICAMP.docx`
- Supplied by: Amaury de Souza, for this collaboration
- Ingestion date: 2026-08-15
- Byte size: 6511822
- SHA-256: `10e652628a7786460243fd47201bbfef498356fcee9766ce3fab48f64fa4ac88`
- Role: current manuscript draft under independent reproducibility audit

## Immutability

Both files above are preserved exactly as supplied. Neither file has been, nor may be, modified
in place. Any derived/cleaned data must be written to `data/processed/`; any manuscript edits
must occur in a separate, non-`manuscript/source/` location once permitted by the project stage.

## Machine-readable manifest

See `outputs/audits/source_manifest.csv` for the manifest recording the same fields in
structured form.
