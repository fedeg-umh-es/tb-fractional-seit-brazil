# Independent DATASUS/SINAN C4 access log and audit closure

## Isolation, time, and scope

- Access date: 2026-09-23 (Europe/Madrid, CEST), approximately 21:40–21:44.
- Git starting point: `986b84634c7e2f82585506cdb7ca9894537bc330`, branch `audit/c1-clean-20260923`. The worktree was clean before C4. C1–C3 were already documented and were not changed.
- Authority: `provenance/datasus/DATASUS_QUERY.md`, read before access. Only C4 was configured and submitted. No other candidate, filter variant, or microdata route was accessed.
- Official landing page: `https://datasus.saude.gov.br/acesso-a-informacao/casos-de-tuberculose-desde-2001-sinan/` (documented in C1–C3); national TabNet form and result URL: `https://tabnet.datasus.gov.br/cgi/tabcgi.exe?sinannet/cnv/tubercbr.def`.
- `Mostra` opened a new POST-result tab. The displayed URL does not encode the selected settings. No manual CGI POST or invented parameterized URL was used.

## Literal UI configuration and displayed result

- National form heading: `TUBERCULOSE - CASOS CONFIRMADOS NOTIFICADOS NO SISTEMA DE INFORMAÇÃO DE AGRAVOS DE NOTIFICAÇÃO - BRASIL`.
- `Linha` = `Ano In. Tratamento`; `Coluna` = `Mês In. Tratamento`; `Conteúdo` = `Casos confirmados`.
- `PERÍODOS DISPONÍVEIS` = all 22 years `2001` through `2022`, inclusive. The visible years `2023`, `2024`, and `2025` were unselected.
- `SELEÇÕES DISPONÍVEIS` = 71 filters. The only restriction was `Tipo de entrada` = `CASO NOVO`. Each of the other 70 filters remained at `Todas as categorias`. `evidence/C4_form_state.json` records each literal filter label and selected option.
- Output format = `Colunas separadas por ";"`. `Ordenar pelos valores da coluna` and `Exibir linhas zeradas` were unchecked.
- Result heading: `Casos confirmados por Mês In. Tratamento segundo Ano In. Tratamento`; result restriction: `Tipo de entrada : CASO NOVO`; displayed period: `Período: 2001-2022`.

The interface's abbreviated `In. Tratamento` labels unambiguously identify treatment start. The form screenshot, separate `CASO NOVO` screenshot, and complete selected-state JSON were saved before submission. The displayed note says the selected *periods* correspond to diagnosis years even when the row and column use treatment-start dates. The output therefore contains undated treatment-start categories and years after 2022; none prompted a filter change.

## Preserved evidence and output

| Artifact | Contents and SHA-256 |
| --- | --- |
| `evidence/C4_form_configured.png` | Full-page configured form; `58b7e97e1de475eb03393b1bd879050e5e023affb6368f6432a9c372e56ce887`. |
| `evidence/C4_tipo_entrada_CASO_NOVO.png` | Visible filter selection; `d7ade9caf0ee8ddd75e3d4f9b0e993bebf42d11e64d21dcaa707cd45c1d1878f`. |
| `evidence/C4_form_state.json` | Dimensions, all 71 named filter states, years, format, checkboxes and URL; `b2529623a3f44ce09d16b7402b2a50ac3a91e30b4fe913d3b7cc629572c3dbc9`. |
| `evidence/C4_result_table.png` | Full-page result including table and source notes; `f8185e74b9faa2f7ef7cfdc07062d90f4746aa79d1952e2d544b2beef676a2ce`. |
| `evidence/C4_result_notes.png` | Source, update notes, and legend in readable viewport; `2a926bea8e7de07249d8b5e8b08689c16e82e5d2fa47942d950a9645532eb457`. |
| `evidence/C4_result_body.html` | Complete live POST-result document-body serialization, including the `<pre>` table and notes; `2014dec28b72b2d63e04f22051a9333f808a4eb64320141e3d7a9683ab2dab6f`. |
| `raw/C4_datasus_tb_brazil_2001_2022.csv` | Captured text of the semicolon-separated `<pre>` block, encoded Latin-1, including header, all result rows, total, and terminal `&`; `f845d711265ac843d93e83060fe46df7617446c64fe06f055ee0e55348c62b90`. |

The file under `raw/` is captured interface output, **not** a server CSV download. Browser DOM extraction normalized line endings to LF; the page declared Windows-1252 and the captured text was saved in Latin-1. The preserved HTML body and CSV contain identical `<pre>` content after HTML entity decoding. No MHTML was produced. These are capture limitations, not changes to C4.

## Source notes displayed with C4

The result identifies `Ministério da Saúde/SVSA - Sistema de Informação de Agravos de Notificação - Sinan Net` as source. It says data for 2001–2019 are final; 2019 underwent correction in September 2025; 2020–2025 were updated in April 2026 and are subject to revision; and the data were made available in TabNet in May 2026. The saved result HTML and screenshots preserve the literal notes and further source qualifications.

## Exact comparison with immutable `casos`

- Canonical workbook: `data/raw/tb_mes.xlsx`, worksheet `dados`, columns `data` and `casos`; SHA-256 `93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b`, verified before comparison.
- `C4_compare.py` verifies both input hashes, the displayed header, every row total and grand total, then maps numeric treatment-start year/month cells to `YYYY-MM`. The displayed `-` is interpreted as zero, as the result legend specifies. The script compares integer counts without tolerance and writes all 264 target rows to `C4_monthly_comparison.csv` and all discrepancies to `C4_discrepant_months.csv`.
- The source contains 312 dated month cells: 264 target cells plus 48 cells from `2023-01` through `2026-12` (including displayed zeroes). The target cells sum to 1,570,975; out-of-window dated cells sum to 1,492; `Em Branco/ign` and `<1975` sum to 24,612. These reconcile exactly to the displayed grand total of 1,597,079. Undated categories were not assigned to target months.

| Metric | Value |
| --- | ---: |
| `ROWS_EXPECTED` | 264 |
| `ROWS_OBTAINED` | 264 target rows |
| `MISSING_MONTHS` | 0 (`[]`) |
| `EXTRA_MONTHS` | 48 dated cells outside the target window |
| `MISMATCH_MONTHS` | 264 |
| `MAX_ABS_DIFF` | 2,441 |
| `TOTAL_ABS_DIFF` | 394,641 |
| `FIRST_MISMATCH` | `2001-01` |
| `LAST_MISMATCH` | `2022-12` |

**C4 = NO_EXACT_MATCH.** The prespecified exact criterion requires `MISMATCH_MONTHS = 0` and `MAX_ABS_DIFF = 0`. C4 fails both conditions.

## Final audit disposition

| Candidate | Result | Mismatched target months | Total absolute difference |
| --- | --- | ---: | ---: |
| C1 | `NO_EXACT_MATCH` | 99 | 3,236 |
| C2 | `NO_EXACT_MATCH` | 264 | 44,685 |
| C3 | `NO_EXACT_MATCH` | 264 | 368,537 |
| C4 | `NO_EXACT_MATCH` | 264 | 394,641 |

`CASOS_PROVENANCE = NO_EXACT_MATCH` and `CANDIDATE_SET_EXHAUSTED = YES`. The original `casos` series supplied by the collaborator could not be reconstructed exactly under any of the four prespecified DATASUS/SINAN configurations. C1 was closest by both mismatched-month count and total absolute difference, but still differed in 99 of 264 months. The original series is preserved without modification. This is a provenance limitation to disclose when Data Availability and manuscript wording are next revised; it does not itself authorize recalibration or alter frozen findings. The audit stops after C4. There is no C5, further filter search, or microdata access without an explicit methodological amendment.
