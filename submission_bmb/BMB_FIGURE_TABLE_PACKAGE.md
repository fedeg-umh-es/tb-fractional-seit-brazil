# Bulletin of Mathematical Biology — Figure and Table Submission Package

Revision of 2026-10-01. Supersedes the earlier inventory. Captions are maintained in one place per item: figure captions and main-table captions in `submission_bmb/BMB_MANUSCRIPT.md`, supplementary captions in `submission_bmb/BMB_SUPPLEMENTARY_INFORMATION.md`. This file records inventory, sources, verification and open points. No canonical result, figure or table in `results_canonical/` is modified.

---

## 1. Inventory

```text
MAIN_FIGURES = 3        (Figure 1, Figure 2 [panels A-B], Figure 3)
MAIN_TABLES = 2         (Table 1, Table 2)
SUPPLEMENTARY_FIGURES = 1   (Figure S1)
SUPPLEMENTARY_TABLES = 6    (Tables S1A, S1B, S2, S3, S4, S5)
```

Tables S4 and S5 are new relative to the earlier inventory. They trace statements added to the text after the claim audit of 2026-10-01 (parameters at their bounds; the 2020 fall and the 2021–2022 rebound in annual notifications).

## 2. Items

| Item | Where | File | Source data | Supports |
|---|---|---|---|---|
| Figure 1 | Main, §3.1 | `figures/Fig1_rmse_by_horizon.{pdf,png}` | `results_canonical/05_rolling_origin/table_forecasting_by_horizon.csv` | C01–C04 |
| Figure 2 (A, B) | Main, §3.2 | `figures/Fig2_skill_by_horizon.{pdf,png}` | `.../table_skill_by_horizon.csv` | C02–C04; C11 boundary |
| Figure 3 | Main, §3.3 | `figures/Fig3_R0_envelope.{pdf,png}` | `results_canonical/03_R0_stability/table_R0_stability_summary.csv`; the 25 individual values from `outputs/identifiability/{multiseed_functionals,profile_objective}.csv` | C07 |
| Table 1 | Main, §3.2 | `tables/table1.md` | `.../table_horizon_summary.csv` | C01–C05 |
| Table 2 | Main, §3.3 | `tables/table2.md` | `.../table_R0_stability_summary.csv` | C07, C08 |
| Figure S1 | SI | `figures/FigS1_bias_by_horizon.{pdf,png}` | `.../table_forecasting_by_horizon.csv` (bias) | diagnostic context |
| Table S1A | SI | `tables/tableS1A.md` | `results_canonical/04_long_open_loop/table_long_open_loop.csv` | C01 (single-origin stress test) |
| Table S1B | SI | `tables/tableS1B.md` | `.../table_forecasting_by_horizon.csv` | C01–C04, Figure 1, Figure S1 |
| Table S2 | SI | `tables/tableS2.md` | `.../table_skill_by_horizon.csv` | C02–C04; C11 boundary |
| Table S3 | SI | `tables/tableS3.md` | `outputs/calibration/`, `outputs/identifiability/`; summary check against `results_canonical/02_identifiability/table_full_profile_diagnostic.csv` | boundary of C07/C08 |
| Table S4 | SI | `tables/tableS4.md` | `outputs/calibration/{fractional,integer}_multiseed.csv` | C01 reserve; σ and γ at bounds |
| Table S5 | SI | `tables/tableS5.md` | `data/raw/tb_mes.xlsx` | evaluation-window context |

Regeneration: `python scripts/build_bmb_figures.py` and `python scripts/build_bmb_tables.py` (dependencies already declared in `pyproject.toml`). Both scripts read only frozen files and abort if a displayed value differs from the frozen summaries.

## 3. Corrections to the earlier package

The earlier package declared `FIGURE_REGENERATION_REQUIRED = NO` and `TABLE_REGENERATION_REQUIRED = NO`. The 2026-10-01 review found the following, and the submission versions were rebuilt accordingly. The canonical PNGs remain in `results_canonical/06_figures/` as the frozen archive.

1. **Resolution.** The canonical PNGs are 720×480 px at 120 dpi (779×201 px for F3), insufficient for print. The submission figures are vector PDF plus 600-dpi PNG.
2. **F3 drawn line.** The canonical F3 draws a thin grey line extending 0.02 beyond the minimum and maximum (`ax.hlines(1, R0_min − 0.02, R0_max + 0.02)` in `scripts/build_canonical_evidence_package.py`), with no legend entry. It can be read as a wider envelope than the stated range of 1.1542–1.1892. It also overlapped the x-axis title with the legend. The new Figure 3 omits the line, shows the 25 individual values (reproducing the frozen minimum, quartiles, median and maximum exactly), and keeps the legend outside the axes.
3. **Labels.** Legends used internal names (`seasonal_naive_12`). The new figures use descriptive labels, group the legend into "within family" and "external baselines" as the role map recommended, and use a colour-blind-safe palette with distinct markers and line styles.
4. **Table 1 caption.** The earlier caption described "out-of-sample forecast errors" and "mean RMSE/MAE", but `table_horizon_summary.csv` holds only the three horizon descriptors for six baseline–metric pairs. The caption now describes what the table contains.
5. **Table S3 contents.** The earlier text described a table with parameter values, calibration error, $R_0$ and DFE stability for 33 points, but `table_full_profile_diagnostic.csv` is a single summary row. Table S3 now lists the 33 solutions from the frozen `outputs/` files. A per-solution DFE column is not given, because the frozen files report DFE classification only in aggregate (31 unstable, 2 stable).
6. **Captions updated** for the claim-audit changes: σ at its lower bound (Figure 3, Table 2), DFE instability following from $R_0 > 1$ (Table 2), the 2020 fall and rebound (Figure S1), and the coincidence of persistence and seasonal naive at $h = 12$ (Figures 1, 2, Tables S1B, S2).

## 4. Verification performed

```text
FIGURE_SERIES_MATCH_FROZEN_CSV = YES   (16 plotted series compared with the CSV values, exact to 1e-12)
FIG3_25_VALUES_REPRODUCE_FROZEN_SUMMARY = YES   (min, Q1, median, Q3, max identical)
TABLE_S3_POOL_REPRODUCES_FROZEN_SUMMARY = YES   (n = 33; R0 range 0.6393-1.6149; 2 below 1, 31 above 1; 25 within 1%)
TABLE_S5_XLSX_EQUALS_OUTPUTS_SERIES = YES       (annual totals from tb_mes.xlsx = observed series in outputs/)
IMAGE_PATHS_RESOLVE = YES
EVERY_CITED_ITEM_DEFINED = YES
CANONICAL_INTEGRITY_TESTS = 30 passed   (tests/test_canonical_freeze.py, test_manuscript_architecture.py, test_repository_integrity.py)
```

Claim-safety gate (carried over and re-checked against the new captions): within-family versus external labelling, descriptive versus inferential skill, horizon descriptors as non-universal, $R_0$ envelope not a confidence interval, DFE as a model property, profile-objective terminology.

## 5. Open points

- **Artwork specification.** The figure widths are 142–172 mm. I have not checked them against the current BMB/Springer Nature artwork guidelines (column widths, minimum resolution for line art, font size at final size, accepted formats). Pending.
- **LaTeX conversion.** Figures and tables are embedded in Markdown. Conversion to the Springer Nature LaTeX class, with float placement and numbering, remains a production step.
- **Supplementary item order.** Table S3 is first cited in Methods (§2.6), before Tables S1A–S1B, so the supplementary numbers do not follow order of first citation. Renumbering is optional.
- **Figure accessibility.** The palette and markers were chosen for colour-blind and grayscale legibility; a formal contrast check was not run.
