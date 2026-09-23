# Independent DATASUS/SINAN C3 access log

## Isolation, time, and scope

- Access date: 2026-09-23 (Europe/Madrid, CEST). The configured form and visible `CASO NOVO` selection were captured at 21:31:54; the result table at 21:32:22; and the semicolon output at 21:33:00.
- Git starting point: `a1cc518521f780eb2b1ba60311c9f22201aeade7`, branch `audit/c1-clean-20260923`. The worktree was clean before C3 and contained the C1 and C2 commits and evidence. Neither candidate was changed or used to construct C3.
- Authority: `provenance/datasus/DATASUS_QUERY.md`, read before access. Only C3 was configured and submitted in this session. C4 was not accessed.
- Official landing page: `https://datasus.saude.gov.br/acesso-a-informacao/casos-de-tuberculose-desde-2001-sinan/`.
- National TabNet form URL: `https://tabnet.datasus.gov.br/cgi/tabcgi.exe?sinannet/cnv/tubercbr.def`.
- The result tab displayed the same URL. Pressing `Mostra` submitted the form and opened a new tab; the POST settings are not represented in a meaningful result URL. No manual CGI POST or invented parameterized URL was used.

## Literal labels and selected configuration observed in the browser

- Portal title: `Casos de Tuberculose - Desde 2001 (SINAN)`.
- Portal prompt: `Abrangência Geográfica:`; selected option: `Brasil por Região, UF e Município`.
- National form heading: `TUBERCULOSE - CASOS CONFIRMADOS NOTIFICADOS NO SISTEMA DE INFORMAÇÃO DE AGRAVOS DE NOTIFICAÇÃO - BRASIL`.
- `Linha` = `Ano Diagnóstico`.
- `Coluna` = `Mês Diagnóstico`.
- `Conteúdo` = `Casos confirmados`.
- `PERÍODOS DISPONÍVEIS` = all years `2001` through `2022`; `2023`, `2024`, and `2025` were not selected.
- `SELEÇÕES DISPONÍVEIS` = 71 filters. The only restricted filter was literal `Tipo de entrada` = `CASO NOVO` (one selected category; no combination). Every other filter remained at its literal value `Todas as categorias`. `evidence/C3_form_state.json` records all 71 individual labels and selections.
- Output format = `Colunas separadas por ";"`. `Ordenar pelos valores da coluna` and `Exibir linhas zeradas` were unchecked.
- Result heading: `Casos confirmados por Mês Diagnóstico segundo Ano Diagnóstico`; result restriction: `Tipo de entrada : CASO NOVO`; displayed period: `Período:  2001-2022`.

The available `CASO NOVO` category is the unambiguous literal interface category for the preregistered C3 restriction. The form, filter-specific screenshot, and full selected-state JSON were saved before submitting the query.

## Preserved interface evidence and output

| Artifact | Contents and status |
| --- | --- |
| `evidence/C3_form_configured.png` | Full-page screenshot of the configured form before submission. |
| `evidence/C3_tipo_entrada_CASO_NOVO.png` | Close screenshot showing `Tipo de entrada` with `CASO NOVO` selected. |
| `evidence/C3_form_state.json` | Selected dimensions, all 71 named filter states, years, format, and form URL before submission. |
| `evidence/C3_result_table.png` | Screenshot of the displayed C3 semicolon-separated table and restriction heading. |
| `evidence/C3_result_notes.png` | Screenshot of the result source and notes. |
| `evidence/C3_result_body.html` | Complete HTML serialization of the live POST-result document body, including `<pre>` output, restriction heading, and source notes; SHA-256 `18030f6b011be60ab8591527dd1a5a0e6fb9ed54a174f622ca76548baa3ed4cd`. It is not an untouched HTTP response or MHTML. |
| `raw/C3_datasus_tb_brazil_2001_2022.csv` | Captured text of the official TabNet `Colunas separadas por ";"` `<pre>` block, encoded Latin-1. It includes the header, 22 year rows, total row, and terminal `&` marker; SHA-256 `ef1c3b725aa9b9e5bf5cd2ba2eec7950c0de2f3e282bb89fda3f7bc2739487e5`. It was not edited after creation. |

No separate CSV download control or server-assigned filename appeared in the result view. **The file under `raw/` is captured interface output, not a raw server CSV download.** Browser DOM extraction normalized line endings to LF; the page declared Windows-1252, and the captured characters were saved in Latin-1. The preserved HTML body and CSV text contain identical `<pre>` content after HTML entity decoding. No MHTML file was produced in this session. These are capture limitations, not changes to the C3 configuration.

## Literal database update notes displayed with C3

> Dados de 2001 a 2019 estão finalizados.
>
> Dados de 2019 passaram por correção em setembro/2025.
>
> Dados de 2020 a 2025 atualizados em Abril/2026, sujeitos à revisão.
>
> Dados disponibilizados no TABNET em 05/2026, após homologação da Coordenação Geral de Vigilância da Tuberculose, Micoses Endêmicas e Micobactérias não Tuberculosas /CGTM/SVSA.

Displayed source: `Fonte: Ministério da Saúde/SVSA - Sistema de Informação de Agravos de Notificação - Sinan Net`. The screenshots and saved HTML body retain the other source notes.

## Deterministic comparison with the immutable workbook

- Workbook: `data/raw/tb_mes.xlsx`, worksheet `dados`, columns `data` and `casos` only; verified SHA-256 `93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b`.
- `C3_compare.py` reads only the captured C3 output and canonical workbook. It verifies input hashes, displayed table header, annual and grand totals, maps each diagnosis year/month to `YYYY-MM`, and compares integer counts without tolerance.
- `C3_monthly_comparison.csv` contains all 264 target months; `C3_discrepant_months.csv` contains every discrepant month.

| Metric | Value |
| --- | ---: |
| `ROWS_EXPECTED` | 264 |
| `ROWS_OBTAINED` | 264 |
| `MISSING_MONTHS` | 0 (`[]`) |
| `EXTRA_MONTHS` | 0 (`[]`) |
| `MISMATCH_MONTHS` | 264 |
| `MAX_ABS_DIFF` | 2131 |
| `TOTAL_ABS_DIFF` | 368,537 |
| `FIRST_MISMATCH` | `2001-01` |
| `LAST_MISMATCH` | `2022-12` |

**C3 = NO_EXACT_MATCH.** The preregistered criterion requires both `MISMATCH_MONTHS = 0` and `MAX_ABS_DIFF = 0`. Work stopped after C3. C4, alternative categories, combined categories, and other filters were not attempted. This finding does not establish the original `casos` acquisition route or close Data Availability.
