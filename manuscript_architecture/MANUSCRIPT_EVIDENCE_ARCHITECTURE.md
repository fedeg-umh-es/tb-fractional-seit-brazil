# Manuscript Evidence Architecture

Built from the frozen canonical evidence set (`results_canonical/`, HEAD `8ba6ea2`,
RESULT_SET_STATUS=FROZEN_WITH_DOCUMENTED_LIMITATIONS). Architecture only -- no prose paragraphs,
no Results/Discussion/Introduction/Abstract drafting. Every claim below carries a canonical ID
(C01-C11, `results_canonical/07_claim_support/claim_support_table.csv`) or is marked
methodological/descriptive with its supporting artifact.

## 1. Dominant scientific question

Does the improvement obtained by fractionalising the SEIT formulation translate into forecasting
skill beyond the model family, and what mechanistic interpretation remains defensible under
calibration non-identifiability?

This is a two-tier question, not three coordinated ones: the first tier (within-family
improvement vs. external forecasting skill) is the paper's spine and supplies the turning point
(R1->R2->R3); the second tier (what remains mechanistically interpretable given
non-identifiability) is a delimiting axis that constrains which of the first tier's mechanistic
by-products (R0, DFE stability) can be asserted at all. The original three-question framing
(Sec 3 of the task) remains valid and unchanged as the set of precise study sub-questions -- see
`INTRODUCTION_REQUIREMENTS.md`, "Precise study questions" -- but is not the paper-level framing;
promoting all three to equal top-level weight obscured the hierarchy the Results section already
enforces. No evidence, claim, or section mapping changes as a result of this rewording.

## 2. Paper-level promise (one sentence)

> This study presents an independent, reproducible reimplementation and audit of a
> fractional-order SEIT model for Brazilian tuberculosis surveillance data: fractional-order
> dynamics consistently improve the corresponding integer-order SEIT formulation, but this
> within-family improvement does not extend to positive forecasting skill against persistence or
> SARIMA baselines (only partially, and boundedly, against a seasonal-naive baseline), while
> weak identifiability of individual epidemiological rate parameters coexists with a
> comparatively robust derived basic reproduction number and a consistent disease-free
> equilibrium instability result within a pre-defined near-equivalent solution set.

Every clause checked against canonical evidence: "fractionalisation improves integer SEIT"
-> C01; "does not extend to forecasting skill vs persistence/SARIMA" -> C02, C03; "partially vs
seasonal-naive" -> C04; "weak individual parameter identifiability" -> C09; "robust R0" -> C07;
"DFE instability" -> C08. No clause requires unsupported evidence.

## 3. Evidence storyboard (from `results_canonical/RESULT_STORYBOARD.md`, unchanged)

QUESTION -> DESIGN -> R1 (fractional < integer) -> R2 (no external skill) -> TURNING POINT
(persistence/SARIMA beat fractional at every horizon) -> R3 (seasonal-naive partial skill) ->
R4 (weak params, robust R0/DFE) -> BOUNDARY (mechanistic robustness != forecasting superiority).
This storyboard is the load-bearing skeleton for Results and must not be reordered to bury R2/the
turning point.

## 4. Section-by-section architecture

### 4.1 Methods

| | |
|---|---|
| Scientific question | Is the study reproducible and is every subsequent claim traceable to a specific, frozen procedure? |
| Frozen evidence | `docs/MODEL_CONTRACT.md`, `docs/EXTERNAL_PARAMETER_CONTRACT.md`, `docs/FRACTIONAL_DIMENSIONAL_CONSISTENCY.md`, `docs/SARIMA_BASELINE_CONTRACT.md`, `docs/METHOD_DECISION_LOG.md` D024 (seeds), `results_canonical/01_model_contract/table_model_contract_status.csv` |
| Permitted claim | Methodological description only -- data, observation model (flow, not stock), fractional SEIT + Caputo derivative, reference-time scaling, integer comparator (independently re-estimated, never reused), DE calibration (seeds/bounds/policy frozen before any result), identifiability protocol, R0/NGM derivation, Matignon criterion, long-open-loop protocol, rolling-origin protocol (13 origins, h=1-12, leakage rule), baselines (persistence/seasonal-naive/SARIMA with frozen order), horizon-wise metrics, skill definition, H_relax/H_strict_from_h1 descriptors, explicit inference boundary (descriptive only, DM deferred). |
| Forbidden | Any numerical result (no RMSE/R0/skill values belong in Methods); any claim about which model "worked better"; any implementation detail irrelevant to reproducing the reported numbers (e.g. internal refactors, file layout). |
| Figure/Table | None (Methods is procedural); may reference `table_model_contract_status.csv` as a compact contract summary if useful. |
| Limitation/qualifier | Exact reproduction of the historical manuscript is impossible (`REPRODUCTION_MODE=INDEPENDENT_REIMPLEMENTATION`); this must be stated once, plainly, here. |
| Bridge to next section | "With the model, calibration, identifiability, and evaluation protocols fixed in advance, we report results in the order the evidence was generated: within-model-family comparison first, then external-baseline comparison, then mechanistic interpretation." |

### 4.2 Results

Five findings (R1-R5), per Sec 21 of the task. R4/R5 kept as **two separate findings** (decision
below, Sec 6 of this document) because they answer different questions (functional
identifiability vs. equilibrium stability) even though both draw on the same near-equivalent
admissible set.

#### R1 -- Fractional formulation improves the integer SEIT comparator

| | |
|---|---|
| Question | Does fractional order improve the SEIT model relative to its own integer-order counterpart? |
| Evidence | Long open-loop stress test (`table_long_open_loop.csv`: fractional RMSE=1117.960 vs integer RMSE=1759.538); rolling-origin fractional-vs-integer row of `table_forecasting_by_horizon.csv` (fractional lower RMSE/MAE at all 12 horizons). |
| Permitted claim | C01 (SUPPORTED_WITHIN_MODEL_FAMILY): fractional SEIT has lower error than the independently re-estimated integer SEIT, consistently, in both protocols. |
| Forbidden | "Fractional SEIT forecasts tuberculosis well" (no baseline comparison yet at this point in the narrative); "fractional SEIT is superior" without the "within-model-family" qualifier. |
| Figure/Table | `table_long_open_loop.csv`; `table_forecasting_by_horizon.csv` (fractional/integer rows); optionally `F1_rmse_vs_horizon.png` (fractional and integer curves only, ignoring baselines for this specific point). |
| Limitation | Two protocols, one comparator family; says nothing yet about external competitiveness. |
| Bridge | "Whether this within-family improvement constitutes genuine forecasting value can only be assessed against baselines outside the SEIT family." |

#### R2 -- Within-family improvement does not translate into external forecasting skill (TURNING POINT)

| | |
|---|---|
| Question | Does the fractional model's advantage over integer SEIT generalize to an advantage over standard forecasting baselines? |
| Evidence | `table_skill_by_horizon.csv` (fractional vs persistence: skill<0 all h=1-12; fractional vs SARIMA: skill<0 all h=1-12); `table_horizon_summary.csv` (H_relax=0, H_strict_from_h1=0 for both baselines). |
| Permitted claim | C02 (NOT_SUPPORTED: outperforms persistence), C03 (NOT_SUPPORTED: outperforms SARIMA), C05 (NOT_SUPPORTED: general operational forecasting improvement). |
| Forbidden | Any "operational superiority" or "superior forecasting performance" language; any softening such as "comparable to" persistence/SARIMA when skill is negative at every horizon. |
| Figure/Table | `F1_rmse_vs_horizon.png` (all 5 models); `F2a_skill_rmse_vs_horizon.png`, `F2b_skill_mae_vs_horizon.png` (skill=0 reference line makes the negative-skill region visually unambiguous). |
| Limitation | Descriptive only (no DM test); 13 origins is a small sample; SARIMA order frozen on 2001-2020 only (a different order might perform differently, but re-selecting now would violate the train-only contract). |
| Bridge | "One baseline comparison behaves differently and must be reported on its own terms." |

#### R3 -- Bounded, horizon-limited skill against seasonal-naive

| | |
|---|---|
| Question | Is there any external baseline against which the fractional model shows positive skill, and if so, over what horizon range? |
| Evidence | `table_skill_by_horizon.csv` (fractional vs seasonal_naive_12: RMSE skill positive h=1-7, negative h=8-12); `table_horizon_summary.csv` (H_relax=7, H_strict_from_h1=7, both RMSE and MAE). |
| Permitted claim | C04 (SUPPORTED_ONLY_VS_SEASONAL_NAIVE): positive observed RMSE/MAE skill vs seasonal-naive for h=1-7, explicitly bounded. |
| Forbidden | "The useful forecasting horizon is seven months" (a dataset/protocol-specific descriptor, not a general predictability limit -- explicit prohibition in `IDENTIFIABILITY_AUDIT_REPORT.md`/`FORECASTING_EVALUATION_REPORT.md` language conventions carried into this architecture); generalizing H=7 to the other two baselines (H_relax=0 there). |
| Figure/Table | `F2a_skill_rmse_vs_horizon.png` (seasonal-naive curve crossing zero at h=7-8 is the key visual). |
| Limitation | Single baseline, single dataset, single protocol; explicitly a descriptor of this evaluation, not a universal claim. |
| Bridge | "Having established the predictive picture, we turn to what can be said mechanistically about the fitted model itself." |

#### R4 -- Individual parameters weakly identified; R0 functionally robust

| | |
|---|---|
| Question | Given the calibration procedure, can beta, sigma, gamma, d be reported as precise epidemiological rates, and is the derived R0 more or less identifiable than its components? |
| Evidence | `IDENTIFIABILITY_AUDIT_REPORT.md` (multiseed + profile-objective: beta ~5.4x, gamma ~5.3x, d >100x spread at near-identical calibration RMSE, CV~0.35%; alpha CV~0.08%; prediction CV 0.19%/0.58% calibration/validation); `table_R0_stability_summary.csv` (R0 in the near-equivalent admissible set: median 1.1735, IQR [1.1682,1.1770]). |
| Permitted claim | C09 (NOT_SUPPORTED: beta/gamma/d as precise rates); implicit predictive-identifiability and R0-functional-identifiability findings (both ROBUST, methodological/descriptive, sourced to `IDENTIFIABILITY_AUDIT_REPORT.md`, no single C-ID needed -- see traceability matrix note). |
| Forbidden | Reporting any specific beta/gamma/d numeric value as a finding; treating the R0 range as a confidence interval, credible interval, or formal uncertainty interval (must use "practical-identifiability envelope" / "near-equivalent solution range" only). |
| Figure/Table | `F3_R0_near_equivalent_envelope.png`; `table_R0_stability_summary.csv`. |
| Limitation | Only one national monthly series; the admissible-set tolerance (delta RMSE<=1%) is a practical choice, not a formal statistical criterion. |
| Bridge | "Given a robust R0 estimate range, what does it imply for the modeled system's equilibrium behavior?" |

#### R5 -- DFE locally unstable across the near-equivalent admissible set

| | |
|---|---|
| Question | Is the disease-free equilibrium stable or unstable under the fitted fractional dynamics, and how robust is that classification to calibration non-uniqueness? |
| Evidence | `table_R0_stability_summary.csv` (DFE_stable=0, DFE_unstable=25, DFE_ambiguous=0, n=25); Matignon criterion `|arg(lambda_i)|>alpha*pi/2` applied per-solution with each solution's own fitted alpha. |
| Permitted claim | C08 (SUPPORTED): DFE locally unstable in 25/25 near-equivalent admissible solutions. |
| Forbidden | Generalizing to the full 33-solution diagnostic pool (which has 2 stable, diagnostic-only points, `table_full_profile_diagnostic.csv`); treating instability as evidence of forecasting performance. |
| Figure/Table | `table_R0_stability_summary.csv` (shared with R4; a dedicated stability figure was not generated and is not required -- the numeric table is sufficient and unambiguous for a binary 0/25/0 classification). |
| Limitation | Restricted to the near-equivalent admissible set by construction; not a claim about the full parameter space. |
| Bridge | "These mechanistic findings (R4, R5) characterize the fitted dynamical system; they are independent evidence from the forecasting findings (R1-R3) and must not be merged with them in the Discussion." |

### 4.3 Discussion

Argument map only -- see `DISCUSSION_ARGUMENT_MAP.md` for the full per-finding table. Discussion
order should mirror Results order (R1->R2->R3->R4/R5) and close with the inference/scope
boundary (Sec 13-14 of the task): DM tests deferred, optimal control deferred, historical ~48%
claim not verified.

### 4.4 Introduction

Not drafted; see `INTRODUCTION_REQUIREMENTS.md`. Logical funnel only: scientific stakes ->
limitation of evaluating mechanistic epidemic models only against integer-order variants of
themselves -> need to separate model-family improvement from forecasting skill -> the
identifiability problem -> precise research question -> study design. Any novelty/gap statement
is `REQUIRES_LITERATURE_VERIFICATION`.

### 4.5 Conclusion

Must preserve the bounded finding, not collapse it. Permitted closing claims: C01 (within-family),
C02/C03/C05 (not supported vs persistence/SARIMA/generally), C04 (bounded vs seasonal-naive),
C07/C08 (R0/DFE within the admissible set), C09 (parameters not precise). Forbidden closing
claims: "fractional models are superior" (unqualified); any operational-deployment
recommendation; any claim depending on C06, C10, or C11.

### 4.6 Abstract

Not drafted; evidence sequence only, per Sec 21 of the task: problem -> independent
reimplementation -> methodological correction (flow, not stock) -> within-family result (C01) ->
external-baseline turning point (C02/C03, bounded C04) -> identifiability/R0 result (C09, C07,
C08) -> bounded implication (mirrors Sec 2 promise above).

## 5. Key limitations (full list: `results_canonical/KNOWN_LIMITATIONS.md`, L01-L12, unchanged)

Most manuscript-relevant subset: L02 (weak beta/gamma/d identifiability), L03 (R0 range is not
a CI), L07 (only 13 rolling-origin origins), L08 (persistence/SARIMA outperform fractional
descriptively at all horizons), L10 (rolling-origin loss-differential dependence not yet
characterized), L11 (no DM/inferential test performed), L12 (historical ~48% not verified).

## 6. Design decision: R4/R5 as separate findings

Kept separate. R4 answers "what is/isn't identifiable" (an epistemic/statistical question about
the calibration procedure); R5 answers "what does the fitted system imply dynamically" (a
model-behavior question). Merging them would obscure that R5's conclusion (DFE unstable) holds
regardless of which point in the admissible set is chosen -- exactly because R0 is the robust
functional established in R4. Keeping them separate makes that logical dependency legible
instead of flattening it into one paragraph.

## 7. Forbidden narrative moves (repository-wide, applies to every section)

- Claiming general/operational forecasting superiority for the fractional model.
- Treating alpha<1 as proof of epidemiological memory (C06).
- Reporting beta/gamma/d as precisely estimated rates (C09).
- Describing the full 33-solution profile pool as the admissible scientific set, or as evidence
  that "R0>1 across all explored solutions."
- Generalizing DFE instability beyond the 25-member near-equivalent admissible set.
- Any statistical-significance language for rolling-origin comparisons (C11; DM_TESTS deferred).
- Using the historical manuscript's numbers, figures, or the ~48% optimal-control claim as
  evidence (C10; REFERENCE_ONLY_NOT_EVIDENCE throughout).
- Inventing a literature novelty/gap claim without a `REQUIRES_LITERATURE_VERIFICATION` flag.

## 8. Explicit turning point

`fractional < integer error` (R1, C01) does **not** imply `fractional > persistence/SARIMA
skill` (R2, C02/C03). This is the manuscript's central scientific turning point and must appear
as a named result (R2), not be diluted across the Discussion or relegated to a limitations
paragraph.

## 9. Recommended Inside-Out writing order

1. Methods (fully mechanical, lowest interpretive risk, unblocks everything else).
2. Results R1 -> R2 -> R3 (forecasting findings, in evidence-generation order).
3. Results R4 -> R5 (mechanistic findings).
4. Discussion (per `DISCUSSION_ARGUMENT_MAP.md`, mirroring Results order).
5. Conclusion (bounded synthesis only).
6. Introduction (written last, so the "gap" it establishes is exactly the question the already-
   written Results/Discussion answer -- prevents inventing a gap the paper doesn't actually
   fill).
7. Abstract (written last of all, compressed from the finished Introduction+Results+Discussion).
