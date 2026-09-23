# Independent DATASUS/SINAN C2 access log

## Isolation, time, and scope

- Access date: 2026-09-23 (Europe/Madrid, CEST). The configured form was captured at 21:20:50, the result table at 21:21:31, and the captured semicolon output at 21:24:03.
- Git starting point: `73505c98e229e88bb990edfa61262b2d8aae291d`, branch `audit/c1-clean-20260923`. The worktree was clean before C2, and the prior C1 commit and evidence were present. C1 was not changed.
- Authority: `provenance/datasus/DATASUS_QUERY.md`, read before the new access. The only candidate configured and submitted in this session was C2. C3 and C4 were not accessed.
- Official landing page: `https://datasus.saude.gov.br/acesso-a-informacao/casos-de-tuberculose-desde-2001-sinan/`.
- National TabNet form URL: `https://tabnet.datasus.gov.br/cgi/tabcgi.exe?sinannet/cnv/tubercbr.def`.
- Result tab displayed the same URL. The query opened a new tab after pressing `Mostra`; its POST parameters are not represented in a meaningful result URL. No manual CGI POST or parameterized URL was constructed.

## Labels observed directly in the official browser interface

- Portal title: `Casos de Tuberculose - Desde 2001 (SINAN)`.
- Geographic prompt: `Abrangência Geográfica:`. Selected portal option: `Brasil por Região, UF e Município`.
- National form heading: `TUBERCULOSE - CASOS CONFIRMADOS NOTIFICADOS NO SISTEMA DE INFORMAÇÃO DE AGRAVOS DE NOTIFICAÇÃO - BRASIL`.
- `Linha` = `Ano In. Tratamento`.
- `Coluna` = `Mês In. Tratamento`.
- `Conteúdo` = `Casos confirmados`.
- `PERÍODOS DISPONÍVEIS` = every year `2001` through `2022`, inclusive; `2023`, `2024`, and `2025` were not selected.
- `SELEÇÕES DISPONÍVEIS` = 71 filters, each at the literal value `Todas as categorias`. Their individual literal labels and selected values are in `evidence/C2_form_state.json`. This includes `Tipo de entrada`, sex, clinical form, age, every notification/residence geography, and all other displayed filters. No additional subset was selected.
- Output format = `Colunas separadas por ";"`. `Ordenar pelos valores da coluna` and `Exibir linhas zeradas` were unchecked.
- Result heading = `Casos confirmados por Mês In. Tratamento segundo Ano In. Tratamento`; displayed `Período:  2001-2022`.

The observed abbreviations `In. Tratamento` unambiguously denote treatment start in the matching year and month dimensions. The form screenshot and full selected-state JSON were saved before submitting C2.

## Preserved interface evidence

| Artifact | Contents and status |
| --- | --- |
| `evidence/C2_form_configured.png` | Full-page screenshot before submission. |
| `evidence/C2_form_state.json` | Selected dimensions, all 71 named filter states, years, format, and form URL before submission. |
| `evidence/C2_result_table.png` | Screenshot of the semicolon-separated result table. |
| `evidence/C2_result_notes.png` | Screenshot of source and update notes. |
| `evidence/C2_result_body.html` | Complete HTML serialization of the live POST-result document body, including the `<pre>` table and source notes; SHA-256 `bad67e0450efaf3cb75954d15a321d5acf79bd6485faef6ea648490e313700f3`. This is neither an untouched HTTP response nor a Chrome MHTML archive. |
| `raw/C2_datasus_tb_brazil_2001_2022.csv` | Captured text of the TabNet `Colunas separadas por ";"` `<pre>` block, encoded Latin-1, SHA-256 `feb11a85b14074937c70e233197311e84ae4e059f3aff18f0597a60dba3b0aad`. It includes all displayed rows, totals, and the terminal `&` marker. It was not edited after creation. |

No separate CSV download control or server-assigned filename appeared in the result view. **The file in `raw/` is a captured interface output, not a raw server CSV download.** Browser DOM extraction normalizes line endings to LF; the page declared Windows-1252 and the captured characters were stored in Latin-1. Chrome's native Save As could not reliably target the C2 result while another Chrome tab was being used concurrently, so no C2 MHTML was saved. The HTML DOM serialization above preserves the displayed POST result and its notes; this capture-route difference is an access incident, not a change to the C2 configuration.

## Literal database update notes displayed with C2

> Dados de 2001 a 2019 estão finalizados.
>
> Dados de 2019 passaram por correção em setembro/2025.
>
> Dados de 2020 a 2025 atualizados em Abril/2026, sujeitos à revisão.
>
> Dados disponibilizados no TABNET em 05/2026, após homologação da Coordenação Geral de Vigilância da Tuberculose, Micoses Endêmicas e Micobactérias não Tuberculosas /CGTM/SVSA.

Displayed source: `Fonte: Ministério da Saúde/SVSA - Sistema de Informação de Agravos de Notificação - Sinan Net`. Another displayed note says: `Períodos disponíveis - Correspondem aos anos de diagnóstico dos casos (até 2024).` Accordingly, the selected periods refer to diagnosis years even when the row and column dimensions show treatment-start dates. C2's result visibly includes `Em Branco/ign`, `<1975`, and treatment-start years `2023`–`2026`; none prompted a filter change.

## Deterministic comparison

- Immutable workbook: `data/raw/tb_mes.xlsx`, worksheet `dados`, `data` and `casos` columns only; SHA-256 verified as `93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b`.
- `C2_compare.py` verifies both input hashes, the displayed header, every row total and the grand total; interprets TabNet `-` as zero; maps numeric treatment-start year/month cells to `YYYY-MM`; and compares the 264 target months with zero tolerance. It makes no changes to either source.
- `C2_monthly_comparison.csv` contains all 264 target months. `C2_discrepant_months.csv` contains every discrepant target month.
- `ROWS_OBTAINED` counts target-window rows in the comparison. `EXTRA_MONTHS` reports the 48 additional dated treatment-start month cells shown in the unfiltered source table (`2023-01` through `2026-12`, including cells displayed as `-`). There are 312 dated month cells in the full source table. Non-date categories `Em Branco/ign` and `<1975` are not silently assigned to target months; together they account for 37,775 cases. The 48 out-of-window dated cells account for 4,104 cases. The 264 target cells total 1,924,105; these three subtotals reconcile to the displayed grand total of 1,965,984.

| Metric | Value |
| --- | ---: |
| `ROWS_EXPECTED` | 264 |
| `ROWS_OBTAINED` | 264 target rows |
| `MISSING_MONTHS` | 0 (`[]`) |
| `EXTRA_MONTHS` | 48 (`2023-01` through `2026-12`) |
| `MISMATCH_MONTHS` | 264 |
| `MAX_ABS_DIFF` | 790 |
| `TOTAL_ABS_DIFF` | 44,685 |
| `FIRST_MISMATCH` | `2001-01` |
| `LAST_MISMATCH` | `2022-12` |

**C2 = NO_EXACT_MATCH.** The prespecified criterion requires `MISMATCH_MONTHS = 0` and `MAX_ABS_DIFF = 0`. Work stopped after C2. No alternative filters or other candidates were run. This result does not establish the original `casos` acquisition route or close Data Availability.
