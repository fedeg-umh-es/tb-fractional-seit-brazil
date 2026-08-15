# Figure/Table Role Map

No canonical figure or table is regenerated, modified, or moved. This is an audit of what
already exists in `results_canonical/`.

## F1_rmse_vs_horizon.png

- **Scientific question**: How does RMSE evolve with horizon for all 5 models simultaneously?
- **Claim supported**: C01 (fractional<integer), C02/C03 (fractional>persistence/SARIMA),
  C04 (fractional vs seasonal-naive crossover).
- **Main/supplement**: Main text. This is the single most information-dense figure -- it
  carries R1, R2, and R3 at once.
- **Reader takeaway**: Fractional beats integer throughout; persistence and SARIMA sit below
  fractional throughout; seasonal-naive crosses fractional's curve around h=7-8.
- **Risk of overinterpretation**: A reader could visually round "fractional beats integer" into
  "fractional is a good forecaster" without registering it's the worst-performing model among
  the non-integer alternatives at most horizons. Caption must state explicitly which comparisons
  are within-family (vs integer) and which are external (vs the other three).
- **Recommendation**: Keep unchanged. Strengthen only the caption/legend text at drafting time
  (not a figure-generation change) to distinguish integer (within-family) from the three
  external baselines, e.g. by grouping legend entries.

## F2a_skill_rmse_vs_horizon.png / F2b_skill_mae_vs_horizon.png

- **Scientific question**: At which horizons, and against which baselines, does the fractional
  model show positive skill?
- **Claim supported**: C02, C03 (negative throughout), C04 (positive h=1-7, negative h=8-12).
- **Main/supplement**: Main text. This pair is the most direct visual evidence for the turning
  point (R2) and the bounded exception (R3); the skill=0 reference line is essential and already
  present.
- **Reader takeaway**: Two of three skill curves never cross above zero; the third crosses
  from positive to negative near h=7-8.
- **Risk of overinterpretation**: None identified beyond the general "skill" caveat (descriptive,
  not tested for significance) -- caption must state this explicitly.
- **Recommendation**: Keep both unchanged; use in Results R2/R3 together, not separately.

## F3_R0_near_equivalent_envelope.png

- **Scientific question**: How stable is the R0 functional across near-equivalent calibration
  solutions, and where does it sit relative to the R0=1 threshold?
- **Claim supported**: C07 (R0>1 across the admissible set).
- **Main/supplement**: Main text (pairs with `table_R0_stability_summary.csv` for R4).
- **Reader takeaway**: The full range and IQR both sit clearly above R0=1; the envelope is
  narrow relative to the individual-parameter variation reported in text.
- **Risk of overinterpretation**: The visual band could be mistaken for a confidence interval.
  Caption must state "practical-identifiability envelope, not a confidence interval" explicitly,
  matching the forbidden-terminology rule already enforced in `results_canonical/RESULT_SET_FREEZE.md`.
- **Recommendation**: Keep unchanged; caption is a drafting-stage responsibility, not a
  regeneration need.

## F4_bias_vs_horizon.png

- **Scientific question**: Do models systematically over- or under-predict, and does this
  worsen with horizon?
- **Claim supported**: No C-ID directly; supports the general reliability picture referenced in
  `FORECASTING_EVALUATION_REPORT.md` Sec 7 (all models underpredict, worsening with horizon;
  fractional bias becomes 100% one-directional from h=6 onward).
- **Main/supplement**: Supplementary. It reinforces but does not add a new C-ID-bearing claim
  beyond what F1/F2 already establish; useful for a careful reader/reviewer but not required to
  carry the paper's main argument.
- **Reader takeaway**: Growing negative bias across all models is a shared limitation of this
  evaluation, not specific to the fractional model.
- **Risk of overinterpretation**: Could be read as "the model is broken" rather than "TB
  incidence rose across the evaluation window and every model under-tracked that rise" -- caption
  should give this context.
- **Recommendation**: Keep as supplementary; optional for main text if space allows, per the
  task's "F4 optional only if genuinely informative" instruction. Judged genuinely informative
  (explains part of why skill is negative), so recommend supplementary inclusion, not omission.

## table_model_contract_status.csv (`01_model_contract/`)

- **Scientific question**: What exactly was calibrated, under what fixed contract?
- **Claim supported**: M01, M02 (methodological, no C-ID).
- **Main/supplement**: Source for Methods prose; not typically reproduced as a manuscript table
  verbatim, but every value in it must appear somewhere in Methods text.
- **Recommendation**: Keep as an internal reference artifact; not necessarily a manuscript
  table itself.

## table_full_profile_diagnostic.csv (`02_identifiability/`)

- **Scientific question**: What does the full (non-admissible-filtered) profile pool look like,
  and why is it excluded from the primary R0 claim?
- **Claim supported**: Negative-space support for C07 (defines what C07 explicitly excludes).
- **Main/supplement**: Supplementary, or a single sentence + footnote in main text referencing
  it. Its entire purpose is defensive (prevents the "R0>1 throughout" overclaim previously
  caught and corrected, D027/D031) -- it does not need a dedicated main-text figure.
- **Recommendation**: Keep as supplementary reference table; cite explicitly wherever C07/C08 are
  stated, so the admissible-set restriction is visible next to the claim, not just in a footnote.

## table_R0_stability_summary.csv (`03_R0_stability/`)

- **Scientific question**: What are the R0 range and DFE stability classification for the
  primary (admissible) evidence set?
- **Claim supported**: C07, C08.
- **Main/supplement**: Main text (pairs with F3).
- **Recommendation**: Keep unchanged; this single row is the entire quantitative basis for R4/R5
  and should be reproduced as a compact manuscript table.

## table_long_open_loop.csv (`04_long_open_loop/`)

- **Scientific question**: How did fractional vs integer perform under a single, long,
  realistic-forecasting-style stress test?
- **Claim supported**: C01 (long-open-loop half of the evidence).
- **Main/supplement**: Main text, small table, in R1.
- **Risk of overinterpretation**: Easy to conflate with rolling-origin numbers if presented
  nearby without a protocol label -- `FORECASTING_EVALUATION_REPORT.md` Sec 12 already enforces
  this separation; the manuscript table/caption must carry the "LONG_OPEN_LOOP_STRESS_TEST,
  single origin" label explicitly, every time it appears.
- **Recommendation**: Keep unchanged; never place in the same table as rolling-origin metrics.

## table_forecasting_by_horizon.csv / table_skill_by_horizon.csv / table_horizon_summary.csv (`05_rolling_origin/`)

- **Scientific question**: Primary quantitative evidence for R1-R3.
- **Claim supported**: C01-C05.
- **Main/supplement**: `table_horizon_summary.csv` -> main text (compact, 6 rows). The 60-row
  and 144-row detail tables -> supplementary (too large for main text; main text should show
  the figures F1/F2a/F2b instead and cite the CSVs as source data).
- **Recommendation**: Keep unchanged; supplementary data files, cited from Results prose and
  from figure captions ("underlying values in Supplementary Table Sx").

## claim_support_table.csv (`07_claim_support/`)

- **Scientific question**: Which candidate claims does the evidence actually support, and in
  what exact words?
- **Claim supported**: All of C01-C11 (this *is* the claim registry).
- **Main/supplement**: Internal manuscript-drafting tool, not itself a manuscript artifact. Not
  intended for publication as a table, though its content should visibly shape every claim made
  in Results/Discussion/Conclusion.
- **Recommendation**: Keep unchanged; treat as the drafting-stage source of truth for wording
  (`CLAIM_TRACEABILITY_MATRIX.csv` in this directory is the manuscript-facing derivative of it).

## Redundancy check

No two canonical artifacts were found to be redundant. `table_full_profile_diagnostic.csv` and
`table_R0_stability_summary.csv` cover deliberately different, non-overlapping sets (33 vs 25)
and both are needed precisely to keep them visibly separate. `table_forecasting_by_horizon.csv`
and `table_skill_by_horizon.csv` present raw errors vs. derived skill respectively -- both
needed, neither redundant.

## Presentation blockers found

None. No genuine scientific-presentation blocker was identified in any canonical figure or
table. The only recommendations above are drafting-stage caption/labeling choices (not
regeneration, not data changes, not plotting-code changes), consistent with the task's
instruction that a cosmetic preference is not a scientific blocker.
