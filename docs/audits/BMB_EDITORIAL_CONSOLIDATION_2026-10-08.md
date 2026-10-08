# BMB editorial consolidation — 2026-10-08 (follow-up to citation repair)

## Scope and baseline
Branch: `fix/bmb-citation-repair-2026-10-08`, based on the existing citation-repair draft PR #3. The prior historical report `docs/audits/CITATION_REPAIR_REPORT_2026-10-08.md` is retained unchanged and describes the state before this follow-up.

## Corrections applied
- Chishtie et al. (2026): characterization updated after examining the accessible full text (Section 4.4, Tables 5–6). Table 5 compares fractional and integer SEIQRDP error, while Table 6 reports rolling-origin results for both formulations at 7-, 14-, and 21-day lead horizons. This is not presented as equivalent to the manuscript's external-baseline evaluation.
- Rocha et al. (2020): moved from the introductory disease-burden sentence to the SINAN surveillance background in Methods 2.2. The article describes SINAN, not the independently verified extraction provenance of the supplied dataset. Bibliographic article identifier corrected to e2019017, as recorded in PubMed (PMID 32074197) and SciELO.
- Embedded existing publication-format Figure 1, Figure 2 (panels A/B) and Figure 3 and their claim-safe captions from `BMB_FIGURE_TABLE_PACKAGE.md` in Results. The image files were already present on main; they were not regenerated or edited.
- Created `BMB_SUPPLEMENTARY_INFORMATION.md` with a pointer to the existing Figure S1 and tables S1A, S1B, S2 and S3 recovered from the earlier working branch. The tables were checked against frozen inputs: 12 × 5 × 3 forecast-metric cells, 12 × 2 × 3 × 2 skill cells, and the 33 profile/multiseed points including 25 admissible solutions (R0 1.1542–1.1892) and 2 non-admissible points with R0 < 1. Checks compared displayed precision to source CSVs. No DFE stability labels are assigned to individual rows: the available evidence only supports the admissible-set 25/25 aggregate.
- Kept the short title and confirmed exact equality of manuscript abstract and separate `BMB_ABSTRACT.md`.

## Evidence and boundaries
- Full Chishtie article available via author-uploaded full text (ResearchGate), DOI: 10.1016/j.epidem.2026.100887.
- Rocha original full-text record: https://www.scielo.br/j/ress/a/K8Bh4JKPmdqySDZBj6JBPxn/ ; PubMed: https://pubmed.ncbi.nlm.nih.gov/32074197/.
- Main-text forecasting results, statistical claims, model, metrics, datasets and frozen evidence were not changed; these edits are editorial only.
- Repository-diff comparison with main shows no altered paths in `results_canonical/`, `outputs/`, `src/`, `scripts/`, `tests/`, `data/`, or `manuscript/source/`.
- Supplementary-table validation checked rounded exported values against existing result files, not fresh model execution.
- No local clone/network available for running repository pytest or producing a visual PDF render in this session. The 30/30 prior tests belong to the preceding citation-repair report; they were not re-run after these edits. A current test run and figure/PDF visual inspection remain necessary.

## Remaining author/institutional confirmations
- Final author list/order, all affiliations, corresponding author, ORCIDs (optional), CRediT, funding, competing interests, ethics/consent, data-access/reuse permissions and final coauthor review.
- Original canonical case-series extraction settings remain unverified; four candidate DATASUS/SINAN queries did not match all 264 observations. Do not claim otherwise.
- Final production QA (LaTeX/Overleaf, citation rendering, journal formatting, figure and table legibility) is not performed here.

Verdict: `DOCUMENTARY_CONSOLIDATION_COMPLETED_WITH_HUMAN_AND_PRODUCTION_BLOCKERS`; `READY_FOR_SUBMISSION = NO`.
