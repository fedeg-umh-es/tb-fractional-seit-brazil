# Deferred analyses A5-A8: limitation paragraphs (2026-10-11)

**Status: PENDING AGREEMENT OF AMAURY DE SOUZA.** Plan A, step 7. No analysis was run for A5-A8.
The paragraphs below are drafts for the Limitations section of the manuscript. They are not
integrated into any manuscript file until step 8. If Amaury prefers to run any of the four
analyses, the corresponding paragraph is dropped and the analysis gets its own protocol, written
before execution, and its own authorisation (S1 decision record, section 6.3).

Evidence used (all verifiable in the repository): 13 origins (2020-12 to 2021-12), h = 1..12,
156 forecasts per method over 24 target months (2021-01 to 2022-12);
`evidence_S1/TB_SEIT_EVIDENCE_FREEZE_2026-10-10/phase2/`; `DATA_PROVENANCE.md`; annual means of the
monthly counts in `data/raw/tb_mes.xlsx` (8,015 in 2019; 7,201 in 2020; 7,648 in 2021; 8,484 in 2022).

---

## A5 — Formal tests of equal predictive accuracy (Diebold-Mariano with HLN correction, or block bootstrap)

**Reason for deferral.** The evaluation has 13 origins. Errors at consecutive origins for the same
horizon are serially dependent, and errors from different origins refer to the same target months
at different horizons, so the 156 forecasts per method are not independent draws. With so few
origins the power of a Diebold-Mariano test, even with the Harvey-Leybourne-Newbold small-sample
correction, is low, and a block bootstrap needs a block length that the sample cannot support.
The project defined no inferential protocol before the evaluation, and defining one after
seeing the errors would make any p-value hard to interpret.

**Draft paragraph (English, for Limitations).**
> All comparisons of forecast accuracy in this study are descriptive. We report RMSE, MAE, bias and
> scaled errors over 13 expanding-window origins, but we do not test the differences formally. With
> 13 origins, multi-step errors that overlap across origins and a single evaluation window
> (2021-2022), tests of equal predictive accuracy such as the Diebold-Mariano test with the
> small-sample correction of Harvey, Leybourne and Newbold would have little power and rest on
> assumptions that the sample cannot check, and no inferential protocol was specified before the
> evaluation. Statements about which method forecasts better should therefore be read as
> observations for this series and window, not as evidence of a general difference.

*Note for the authors.* Amaury frames A5 as exploratory. The argument that remains is the
absence of a pre-specified protocol and the risk that a p-value would be read as confirmatory;
the computation itself would be arithmetic on the frozen errors. If you choose to run it, it
should be written as a protocol first and labelled exploratory in the text.

---

## A6 — Evaluation before the pandemic (origins before 2020)

**Reason for deferral.** An evaluation with calibration ending in 2016 or 2017 and targets in
2018-2019 is not a recomputation of existing output. It requires new origins, new global fits of
both SEIT models for each of them, new SARIMA fits and new baseline forecasts, all under a
protocol written beforehand. It also touches the same bound-dependence of the fits that the S1
bound-sensitivity step documented, so the new fits would need their own bound decisions.

**Draft paragraph.**
> The evaluation window (2021-2022) follows the disruption of 2020. The annual mean of the monthly
> counts is 8,015 in 2019, 7,201 in 2020, 7,648 in 2021 and 8,484 in 2022, and all five methods
> under-predict on average at every horizon. The smooth trajectories of the SEIT models cannot
> represent a rebound of this kind, and a method that updates to the most recent observation, such
> as persistence, is expected to be favoured in such a window. We did not evaluate origins before
> 2020, so we cannot say whether the ordering of the methods holds outside this post-disruption
> period. The results should be read as specific to the window studied.

*Check before using this text.* "Expected to be favoured" is an inference from the structure of the
methods, not a result of this study. The 2020 decline and the rebound are visible in the annual
means; attributing them to COVID-19 requires the references Amaury proposes for B1.

---

## A7 — Sensitivity to the reconstruction of the case series

**Reason for deferral.** The provenance audit (`DATA_PROVENANCE.md`) tested four pre-specified
DATASUS/SINAN TabNet configurations. None reproduced the 264 supplied monthly counts exactly;
the closest (C1) differs in 99 of the 264 months, and the original extraction route remains
unrecovered. Repeating the rolling-origin comparison with C1 would measure sensitivity to one
alternative reconstruction, which is itself not the source of the series, and would not settle the
provenance question. The data-availability gate remains open and is a separate matter.

**Draft paragraph.**
> The monthly case counts used here come from a file whose original extraction route could not be
> recovered. A pre-specified audit of four DATASUS/SINAN TabNet configurations did not reproduce the
> 264 monthly values exactly; the closest configuration differed in 99 months. We did not repeat the
> forecasting comparison with any of these alternative reconstructions, so we cannot quantify how
> sensitive the results are to the provenance of the series. We treat the supplied file as the
> observational record of the study and report the audit in the Data Availability section.

---

## A8 — Seasonal forcing in the transmission rate

**Reason for deferral.** Adding a term such as beta(t) = beta0 (1 + eps cos(2 pi t / 12 + phi))
introduces two parameters (eps, phi) and changes the model class under evaluation. The study
evaluates the SEIT model as specified; a seasonal variant would be a different model, with its
own calibration, identifiability and bound questions, and not a sensitivity test of the model
evaluated.

**Draft paragraph.**
> The SEIT models as evaluated have no seasonal component, whereas the seasonal naive and SARIMA
> baselines use the 12-month cycle explicitly. The comparison therefore mixes differences in model
> class with differences in how seasonality is represented. A seasonal forcing of the transmission
> rate, for example beta(t) = beta0 (1 + eps cos(2 pi t / 12 + phi)), would add two parameters and
> define a different model; we did not fit it. The positive skill of the fractional model against
> the seasonal naive baseline, limited to the first five horizons in our evaluation, should not be
> read as an advantage of the fractional operator over a seasonal specification.

*Check before using this text.* The "first five horizons" figure is the S1 value
(`phase2/skill_by_horizon.csv`; S1 decision record, section 3). The last sentence is a caution
about interpretation, not a tested claim.

---

## Not covered here (to be decided at step 8)

The sensitivity of alpha, sigma and R0 to the original bounds (step 5) and the transient of E(t)
(step 4) also bear on the Limitations section. Their paragraphs depend on how fedeg and Amaury
decide to present the wider-bound fits and are not drafted in this document.

**Decision pending: agreement of Amaury de Souza that A5, A6, A7 and A8 are declared as
limitations and not executed.**
