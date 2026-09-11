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

The original external acquisition route for the complete workbook is not documented in the
supplied file. Provenance is therefore recorded separately for the variables for which an
independent source has been verified.

## Population denominator provenance

The `populacao` column used during the 2001-2020 calibration window matches the annual total
population series from the **2013 revision of the Brazilian national population projection**:

Instituto Brasileiro de Geografia e Estatistica (IBGE). *Projecao da Populacao do Brasil por
Sexo e Idade para o Periodo 2000/2060: Revisao 2013*. Rio de Janeiro: IBGE; 2013. Historical
publication page: `https://ww2.ibge.gov.br/home/estatistica/populacao/projecao_da_populacao/2013/`
(accessed 2026-09-11).

The annual projected total is repeated across the twelve monthly rows of each calendar year in
the supplied dataset. The calibration implementation uses those monthly entries directly as the
exogenous population denominator `N(t)`; the numerical solver then linearly interpolates the
monthly grid to obtain a continuous `N(t)` during integration. For validation/forecast periods,
future population denominators are generated using the repository's train-only extrapolation
rule and do not use population observations beyond the corresponding training endpoint.

The 2013 revision is retained because it is the source that reproduces the denominator series
actually supplied and used by the reimplementation and because it covers the full 2001-2020
calibration interval. The later 2018 revision starts in 2010 and therefore does not cover the
first nine years of the study period; replacing the 2013 series with it would change the
historical model input and would require truncating or otherwise redefining the calibration
window.

**Freeze classification:** this provenance correction is bibliographic/documentary only. It
does not alter the observational workbook, model equations, parameter bounds, calibration,
forecasts, numerical results, figures, tables, or scientific claims. The frozen scientific
result set therefore remains unchanged.

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
