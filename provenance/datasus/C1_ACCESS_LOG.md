# Independent DATASUS/SINAN C1 access log

## Isolation and scope

- Date and time of access: 2026-09-23, approximately 20:59–21:03 CEST (Europe/Madrid). The configured-form screenshot was saved at 21:01:32 CEST; the result archive at 21:03:16 CEST.
- Git starting point: `592ef5c96aadcd9fd5f7e9e6ed20effe4a6223f7` on the new `audit/c1-clean-20260923` worktree. It was clean before access and contained no earlier C1/C2 artifacts.
- Methodological authority: `provenance/datasus/DATASUS_QUERY.md`, read before access. Only C1 was submitted. C2–C4 were not configured or submitted in this worktree.
- Official landing page: `https://datasus.saude.gov.br/acesso-a-informacao/casos-de-tuberculose-desde-2001-sinan/`.
- National form URL: `https://tabnet.datasus.gov.br/cgi/tabcgi.exe?sinannet/cnv/tubercbr.def`.
- Result URL displayed by Chrome: the same URL as the form. The form submission opened a new result tab; its POST parameters are not represented in a meaningful result URL. No parameterized URL or manual CGI request was constructed.

## Labels directly observed in the browser

- Portal title: `Casos de Tuberculose - Desde 2001 (SINAN)`.
- Portal scope prompt: `Abrangência Geográfica:`; selected option: `Brasil por Região, UF e Município`.
- National form heading: `TUBERCULOSE - CASOS CONFIRMADOS NOTIFICADOS NO SISTEMA DE INFORMAÇÃO DE AGRAVOS DE NOTIFICAÇÃO - BRASIL`.
- Dimension labels and selected values: `Linha` = `Ano Diagnóstico`; `Coluna` = `Mês Diagnóstico`; `Conteúdo` = `Casos confirmados`.
- Period label: `PERÍODOS DISPONÍVEIS`; selected years: every year from `2001` through `2022`, inclusive. `2023`, `2024`, and `2025` were not selected.
- Filter section label: `SELEÇÕES DISPONÍVEIS`. All 71 selection filters were left at their literal default `Todas as categorias`, including `Ano Diagnóstico`, `Mês Diagnóstico`, `Tipo de entrada`, `Sexo`, `Forma`, all notification and residence geographic filters, and all other filters listed individually with their selected states in `evidence/C1_form_state.json`.
- Output format label: `Colunas separadas por ";"` (selected). `Ordenar pelos valores da coluna` and `Exibir linhas zeradas` were both unchecked.
- Result heading: `Casos confirmados por Mês Diagnóstico segundo Ano Diagnóstico`; displayed period: `Período:  2001-2022`.

These observed labels are semantically unambiguous for the fixed C1 definition: Brazil, confirmed cases, diagnosis year and month, and no additional filters. The form screenshot and machine-readable state were saved **before** pressing `Mostra`.

## Evidence and export

| Artifact | Description |
| --- | --- |
| `evidence/C1_form_configured.png` | Full-page screenshot of the configured form before submission. |
| `evidence/C1_form_state.json` | Literal selected dimensions, all 71 named filters and their selected states, periods, format, and form URL before submission. |
| `evidence/C1_result_table.png` | Screenshot of the displayed semicolon-separated result table. |
| `evidence/C1_result_notes.png` | Screenshot of the displayed source notes and update notes. |
| `evidence/C1_result_POST.mhtml` | Chrome's single-file browser archive of the live POST result, SHA-256 `6664e070faf06d423c749a7e16aa46644f56b023a99fba0a4d4d837919e92c9b`. |
| `raw/C1_datasus_tb_brazil_2001_2022.csv` | Text of the single `<pre>` block shown in TabNet's official `Colunas separadas por ";"` output, encoded as Latin-1. It includes the header, 22 year rows, total row, and terminal `&` marker. Browser DOM extraction normalized the source's CRLF line endings to LF; no data fields were changed, and the file has not been edited after creation. SHA-256 `f9f801641d40c48330ee686af77bb3416044063f886a9306f480b89b4dd6f035`. |

The TabNet interface did **not** offer a separate CSV download link or server-assigned filename in this result view. Thus `C1_datasus_tb_brazil_2001_2022.csv` is a field-for-field capture of the interface's semicolon-separated output block, with normalized line endings, not an untouched downloaded HTTP attachment. The MHTML `<pre>` and saved CSV match after CRLF-to-LF normalization. Original server filename: **none displayed**. Chrome's native Save As preserved the POST result as MHTML; the browser's programmatic HTML export was unavailable. This deviation from the requested native CSV download/HTML capture route is recorded so the file's origin is not overstated.

## Literal database update notes displayed with the result

> Dados de 2001 a 2019 estão finalizados.
>
> Dados de 2019 passaram por correção em setembro/2025.
>
> Dados de 2020 a 2025 atualizados em Abril/2026, sujeitos à revisão.
>
> Dados disponibilizados no TABNET em 05/2026, após homologação da Coordenação Geral de Vigilância da Tuberculose, Micoses Endêmicas e Micobactérias não Tuberculosas /CGTM/SVSA.

The source also states: `Fonte: Ministério da Saúde/SVSA - Sistema de Informação de Agravos de Notificação - Sinan Net`. The screenshot and MHTML preserve the other notes, including the recommendation to include later available periods to capture delayed notifications. The executed C1 period selection remained fixed at 2001–2022.

## Deterministic comparison with the immutable workbook

- Workbook: `data/raw/tb_mes.xlsx`, worksheet `dados`, columns `data` and `casos` only. Verified SHA-256: `93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b`.
- Reproduction: run `provenance/datasus/C1_compare.py` from any directory with the bundled Python runtime and `openpyxl`. The script verifies both input hashes, validates the TabNet header and totals, maps each year and month to `YYYY-MM`, and compares integer counts with zero tolerance. The terminal `&` and displayed total row are excluded from the monthly series.
- Complete comparison: `C1_monthly_comparison.csv`.
- All discrepant months: `C1_discrepant_months.csv`.

| Metric | Value |
| --- | ---: |
| `ROWS_EXPECTED` | 264 |
| `ROWS_OBTAINED` | 264 |
| `MISSING_MONTHS` | 0 (`[]`) |
| `EXTRA_MONTHS` | 0 (`[]`) |
| `MISMATCH_MONTHS` | 99 |
| `MAX_ABS_DIFF` | 608 |
| `TOTAL_ABS_DIFF` | 3236 |
| `FIRST_MISMATCH` | `2002-02` |
| `LAST_MISMATCH` | `2022-12` |

**C1 = NO_EXACT_MATCH.** The prespecified criterion requires both `MISMATCH_MONTHS = 0` and `MAX_ABS_DIFF = 0`. Work stopped after C1; no other candidate was executed. This result does not establish the original acquisition route of the canonical `casos` series or close the Data Availability gate.

## Descriptive comparison with pre-existing, unvalidated main-worktree artifacts

The separate main worktree already contained `C1_monthly_comparison_2026-09-23.csv`. It was read **only after** generating this independent comparison and was never used as an input. The two comparison tables have identical month, workbook count, TabNet count, and difference in all 264 rows (0 value differences). No pre-existing file was modified or incorporated into this worktree.
