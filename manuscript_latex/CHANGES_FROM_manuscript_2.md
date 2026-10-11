# Changes from `incoming/manuscript_2.tex` (2026-10-11)

Full diff: `diff incoming/manuscript_2.tex manuscript.tex`. Order of integration: Methods, Results, Discussion, Conclusions, Introduction, Abstract.

| Item | Change |
|---|---|
| Metadata | corresponding author marked on García Crespi (`fedeg@umh.es`) |
| B7, Methods 2.1 | "an unpublished working manuscript" replaced by "the materials of the original study, which were provided by the collaborating author and are not publicly available" (no preprint cited) |
| B8, Methods 2.2 | IBGE 2013 revision justified from `DATA_PROVENANCE.md` (reproduces the supplied denominators; the 2018 revision starts in 2010) |
| 8.4, Methods 2.2 | explicit statement that there is no separate detection or notification process; E(0) = y0/sigma is an approximation |
| Methods | DE, MASE and next-generation matrix cited; SARIMA coefficients now regenerated (max relative error 9.2e-9) and reported in the appendix; MASE defined |
| Methods (new) | subsections "Sensitivity to the lower bounds of alpha and sigma" and "Transient of the exposed compartment", with the rules fixed before running |
| B5, Results 3.1 | sigma at its bound, d differing by a factor of about 180, 0.47 per year, plausibility not assessed |
| B4, Results 3.2 | persistence and seasonal naive identical at h = 12 (RMSE 1152.958); MAE, bias and MASE statements with the appendix tables |
| Results (new) | subsections on the bound sensitivity (Table 6) and on the transient of E(t) |
| B1, Discussion | paragraph rebuilt from WHO (2024) and Ministry of Health (2024) sources; observed changes and the sources' attribution kept apart; no causal claim of our own |
| B2, B5, Discussion | bound-conditional size of the within-family margin, asymptotics of the linearized system vs fitted trajectory, caution on alpha, sigma and d |
| B9, Limitations | new subsection: provenance (A7), post-disruption window (A6), no formal tests (A5), seasonality (A8), bounds sensitivity, SARIMA boundary coefficient |
| Conclusions | one sentence on bounds and the within-family margin |
| B6, Introduction | out-of-sample evaluation against simple benchmarks, with six new references; identifiability references |
| B3, Abstract | RMSE at lead 1 for the five methods; sentence on the bound sensitivity |
| Declarations | Data and Code Availability use the Zenodo placeholders and the S1 evidence commit |
| B10 | references sorted by surname (patched `.bst`) |
| Appendix | MAE, bias, MASE by lead and SARIMA coefficients by origin |

Not done: A5-A8 analyses (declared as limitations); update of the population source; any citation of references that could not be verified.

## Reference audit (2026-10-11)

| Change | Reason |
|---|---|
| Area et al. entry replaced (Adv. Differ. Equ. 2015:278, DOI 10.1186/s13662-015-0613-5) and the Introduction sentence reworded | the previous DOI, title and pages belonged to no matching paper, and the paper does not use a Caputo formulation in its model |
| Simpson and Maclaren sentence reworded | the paper links parameter and prediction confidence sets; it does not state that identifiability and prediction stability "need not coincide" |
| MASE sentence: "in the spirit of" Hyndman and Koehler | the seasonal-naive scale is our definition |
| Diebold-Mariano and HLN citations placed on the tests they name | the power argument is ours |
| Epidemic-forecast sentence: "evaluations that included null, baseline or naive models" | what the three abstracts support |
| Matignon (1996) added, provisional | cited for the stability condition already used |
| WHO 2024 and Ministry of Health 2024 added | B1 |
| IBGE entry: URL changed to the IBGE library copy of the 2013 methodological note | previous URL not checkable |
