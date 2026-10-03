# State freeze — 2026-10-03

Baseline commit before this note: `2d4b991`. Tag: `state-freeze-2026-10-03`.

## Status

```text
SCIENCE = FROZEN (results_canonical/ unchanged)
MANUSCRIPT = CONSOLIDATED_DRAFT (submission_bmb/BMB_MANUSCRIPT.md)
FIGURES_TABLES_SUBMISSION_FORMAT = REGENERATED (scripts/publication_figures.py -> submission_bmb/figures, submission_bmb/tables)
TABLES_1_2 = EMBEDDED_IN_MANUSCRIPT
REFERENCES = CORRECTED_AND_SYNCED (REFERENCE_AUDIT.md, LITERATURE_VERIFICATION_MATRIX.md)
READY_FOR_SUBMISSION = NO
```

## Changes since the previous canonical update

- Repository stated as public in the Code/Data Availability text.
- Author surname corrected to García Crespi.
- COVID-19 context stated in Methods 2.2 (annual totals 2019-2022; calibration window includes 2020; no pandemic term in the model).
- Sigma reported as bound-constrained in all 25 admissible solutions (0.0100-0.0102 per month); R0 envelope stated as conditional on that value.
- Reference errors corrected (Area et al., Meshkat et al., Raue et al., Rocha et al. 2020 in place of Pelissari, Roosa K.).
- Call-outs for Figures 1-3, S1 and Tables 1-2, S1-S3 added to Results.
- Figures 1, 2 (A/B), 3, S1 regenerated at 600 dpi (PNG + PDF) from frozen tables; the script asserts agreement with the frozen R0 and horizon values.
- Tables 1 and 2 embedded in Results with captions aligned to the canonical tables.

## Pending (not closed)

- Alzahrani 2024: author list not verified.
- Rocha et al. 2020: English title and article number not verified.
- Conversion to LaTeX (Overleaf) and render check of tables and figure call-outs.
- Human gate: Amaury's final scientific review; CRediT statements; author list/order/affiliations; funding, ethics and competing-interest metadata; authorization to submit.
