# External Parameter Contract — mu, Lambda, N(t), sigma, gamma, d, alpha

Status: SPECIFICATION. No code written, no model executed, no parameter estimated, manuscript
untouched, optimal control untouched. This document closes the external-evidence decisions still
needed on top of `docs/MODEL_CONTRACT.md` so the fractional SEIT model and its integer
comparator are directly implementable without further scientific judgment calls during coding.

Evidence labeling used throughout: `HECHO VERIFICADO` (a specific, sourced figure or documented
fact), `INFERENCIA` (a conclusion computed from combining verified facts or from the
data/model structure itself), `RECOMENDACIÓN` (a methodological choice made for defensibility
where no external source fixes the answer). No manuscript numerical result was used as a target.
All web sources below were retrieved 2026-08-15.

---

## 1. VERDICT

**EXTERNAL_PARAMETER_CONTRACT_READY_WITH_LIMITATIONS**

Two items keep this from unqualified `READY`: (a) the exact provenance of the `populacao`
column is undocumented, so a `PROVENANCE_REQUIRED` classification and a conservative,
leakage-free substitute are specified below rather than a directly-verified answer; (b) the μ
constant is given from a small number of verified anchor points (not the full annual IBGE
series), with an explicit instruction to pull the precise series before finalizing — but since
the model's sensitivity to μ is negligible (`docs/MODEL_CONTRACT.md`, A04: `sensitivity_required
= NO`), this does not block implementation. Neither issue requires a new scientific decision;
both have a fully specified, conservative fallback.

## 2. Tabla final

| quantity | role | fixed_or_estimated | value_or_bounds | units | source | source_type | temporal_availability | leakage_risk | decision | limitations |
|---|---|---|---|---|---|---|---|---|---|---|
| N(t) | exogenous force-of-infection denominator | fixed (data-driven) | calibration (2001-2020): dataset `populacao` column, used as-is. Validation (2021-2022): **do not** use the dataset's 2021-2022 values; extrapolate forward from a trend fit on 2001-2020 `populacao` only (Section 3). | individuals | Dataset `data/raw/tb_mes.xlsx`, `populacao` column; provenance of this column is undocumented (`DATA_PROVENANCE.md` records no source URL). IBGE publishes two distinct real-world series that could underlie it: annual "Estimativas da População" (trend-based, available ~mid-year, every year, without needing a not-yet-existing census) vs. Census-calibrated retrospective series (2022 Census, ref. date 2022-07-31, first results published 2023-06-28, with further variables released through 2023-2025). | **PROVENANCE_REQUIRED** for 2021-2022 portion; calibration-period portion (2001-2020) is lower risk since it predates the 2022 Census entirely. | HIGH for 2021-2022 if used as-supplied; NONE if the Section 3 extrapolation rule is used instead. | Use dataset values for 2001-2020 (calibration). For 2021-2022 (validation), use the trend-extrapolation substitute in Section 3, not the dataset's own 2021-2022 values, regardless of their true provenance. | If the collaborator later confirms the 2021-2022 `populacao` values came from real-time-available "Estimativas da População" (not census-calibrated retrospective revisions), this restriction could be relaxed — but only after that confirmation, not by assumption. |
| mu | background all-cause mortality (natural exit from every compartment) | fixed (not estimated) | mu ≈ 1/(74×12) ≈ 0.001126/month, from an approximate 2001-2020 average life expectancy at birth of ~74 years (anchors: ~71.1 years in 2000, ~76.2 years in 2019, both pre-pandemic IBGE figures; the 2020-2021 COVID-era dip (74.8, 72.8 years) and 2022 rebound (75.5 years) are single-year shocks from an unrelated cause and are deliberately excluded from this demographic-closure constant). | month⁻¹ | IBGE, Tábuas Completas de Mortalidade / série "Esperança de vida ao nascer" (SIDRA Tabela 3825; historical série 1940-2000 "POP210"); Agência Brasil/Agência IBGE news releases reporting the 2019-2023 figures. | HECHO VERIFICADO (individual anchor years) / INFERENCIA (the ~74-year calibration-window average interpolated from those anchors, not from the full annual series) | Fully available in real time; life-table methodology is retrospective demographic accounting, not a forecast — no leakage concern. | Fix as a single constant for the whole 2001-2022 span (do not time-vary). | Exact annual IBGE series (SIDRA Tabela 3825, or the annual Tábua Completa de Mortalidade publications) was not pulled point-by-point in this review; refining the constant with the full series is a low-priority polish given negligible model sensitivity to mu (`docs/MODEL_CONTRACT.md`, A04). |
| Lambda | recruitment into S | fixed (closure) | Lambda = mu × N̄, N̄ = mean of the calibration-period N(t) series (2001-2020, as defined above) | individuals·month⁻¹ | Derived; not itself an external empirical quantity | RECOMENDACIÓN (demographic-closure convention; see `docs/MODEL_CONTRACT.md` D010) | N/A (fully determined by mu and N̄, both already resolved) | NONE (uses only calibration-window N̄) | Option A confirmed: Lambda = mu·N, no separate estimation, no reformulation into proportions. | None material; S≈N throughout given TB's small population share, so Lambda's precise value has little leverage on I(t) (see `docs/MODEL_CONTRACT.md` §3/A03). |
| sigma | E→I progression rate | estimated via DE | bounds retained: [0.01, 0.50]/month (unchanged from manuscript / `docs/MODEL_CONTRACT.md`) | month⁻¹ | CDC, "Latent Tuberculosis Infection: A Guide for Primary Health Care Providers" / CDC Clinical Overview of Tuberculosis: ~5% of infected persons progress to active disease within 2 years, another ~5% over the remaining lifetime (non-HIV), i.e. lifetime risk ~10%, strongly front-loaded but with a long tail. | HECHO VERIFICADO | Fully available (general clinical/epidemiological fact, not time-indexed to this dataset). | NONE | **STRUCTURAL_LIMITATION_TO_DECLARE** (see Section "sigma" below) — bounds are not respecified, but the single-exponential-compartment structure is flagged as unable to represent the documented fast/slow bimodal progression simultaneously. | Do not redesign the SEIT structure in this pass, per task scope; the limitation must be stated wherever sigma or R0 is later interpreted. |
| gamma | I→T removal rate (diagnosis+treatment pathway) | estimated via DE | **bounds revised**: recommend narrowing to approximately [0.05, 0.30]/month (durations ≈ 3.3–20 months), replacing the manuscript's [0.01, 0.50]/month (durations 2–100 months) as the primary search range; retain [0.01, 0.50] only as a sensitivity-analysis comparison arm. | month⁻¹ | WHO: standard first-line regimen is 6 months (2 months intensive + 4 months continuation). Brazil-specific diagnostic-delay studies (Porto Alegre: median total delay 60 days; Vitória: median total delay 110 days) give a plausible added pre-treatment delay of ~2-3.7 months. Central estimate: (2-3.7 months delay) + 6 months treatment ≈ 8-9.7 months mean total time in I → gamma_central ≈ 1/8.5 ≈ 0.118/month. | HECHO VERIFICADO (WHO 6-month course; Brazil delay-study medians) / INFERENCIA (the combined duration and resulting rate; see math below) | Fully available (published studies, not time-indexed to 2021-2022). | NONE | Narrow the search range as above; document the duration→rate correspondence explicitly (below) rather than converting automatically. | The manuscript never specifies whether "T" means "entered treatment" (duration ≈ delay only, γ toward the range's upper end) or "treated/completed" (duration ≈ delay+course, γ mid-range); this contract adopts the latter (T = completed/removed) as the standard SEIR/SEIT convention for a terminal compartment, and flags the ambiguity explicitly (see below). |
| d | TB-attributable excess mortality (I-compartment exit via death) | estimated via DE | bounds retained: [0.0001, 0.05]/month (unchanged); central plausibility estimate ≈ 0.004/month falls comfortably inside this range. | month⁻¹ | Brazil cohort study (SciELO/PMC, "Predictors of unsuccessful tuberculosis treatment outcomes in Brazil," 178,504 notified cases, 2015-2017): 3.2% cohort case-fatality (died of TB). Converted via competing-hazards relation (below), using gamma≈0.118/month and mu≈0.0011/month. | HECHO VERIFICADO (3.2% cohort case-fatality) / INFERENCIA (the derived hazard d, via an explicit competing-risks formula, not a direct source) | Fully available (retrospective published cohort, not time-indexed to 2021-2022). | NONE | **BOUND_ACCEPTABLE** — retain manuscript bounds as-is; central plausibility check passes. | 3.2% is a cohort case-fatality proportion (fraction who die), not a population mortality rate (WHO's ~2.4-3.6 deaths per 100,000 population/year figure) and not the compartmental hazard d directly — these three quantities must never be substituted for one another (see math below). |
| alpha | fractional order | estimated via DE | primary: [0.50, 1.00]; sensitivity arm: [0.70, 1.00] (manuscript's original bound) | dimensionless (0 < alpha ≤ 1) | Caputo (1967); Diethelm (2010) — both already cited by the manuscript itself — establish only the mathematical validity domain 0 < alpha ≤ 1, not any epidemiologically preferred sub-range. | HECHO VERIFICADO (validity domain) / RECOMENDACIÓN (the specific [0.50,1.00] operating range) | N/A | NONE | 0.50 has **no substantive epidemiological justification** — it is an a priori operational widening chosen for identifiability robustness (`docs/MODEL_CONTRACT.md`, D012), not a value derived from theory, literature, or data. Must not be re-selected based on DE results. | None beyond what is already logged in `docs/MODEL_CONTRACT.md`. |

### sigma — structural limitation (detail)

CDC guidance (general, not Brazil-specific, but standard reference figure) states that among
persons infected with *M. tuberculosis* who are not treated for latent infection: approximately
5% develop active TB disease within the first 2 years post-infection, and another ~5% develop it
at some later point over the remainder of their lifetime (non-HIV population; lifetime risk
~10%; risk is markedly higher, 7-10%/year, for untreated HIV-positive persons). This is a
documented bimodal (fast-progressor / slow-reactivator) process. A single-compartment,
single-rate Exposed stage with one sigma cannot represent both timescales simultaneously — any
sigma chosen will implicitly privilege one subpopulation's dynamics over the other's. This is a
structural property of the SEIT model as specified in the manuscript, not a defect of any
particular sigma value or bound, and is **not** to be fixed by redesigning the compartmental
structure in this pass. **Classification: STRUCTURAL_LIMITATION_TO_DECLARE.** It must be stated
as an explicit caveat wherever sigma or an R0 expression containing sigma is later interpreted.

### gamma — duration-to-rate correspondence (detail, per explicit task instruction)

The compartmental convention assumes an (approximately) exponentially-distributed sojourn time in
I with mean duration D, giving `gamma = 1/D`. This is an approximation: WHO's 6-month treatment
course is a largely fixed/deterministic protocol duration, not literally exponential, and mixing
it with a variable pre-treatment diagnostic delay only partially restores exponential-like
aggregate behavior across a heterogeneous patient population. Two further judgment calls affect
D, both made explicit rather than assumed automatically:

1. **What "T" means.** If T = "entered treatment," D ≈ diagnostic delay only (~2-3.7 months from
   the Brazil studies), giving gamma ≈ 0.27-0.5/month. If T = "completed/removed" (the standard
   terminal-compartment convention adopted here), D ≈ delay + 6-month course ≈ 8-9.7 months,
   giving gamma ≈ 0.10-0.12/month. This contract adopts the second interpretation.
2. **Whose delay estimate.** The Brazil-specific studies found (Porto Alegre: 60-day median
   total delay; Vitória: 110-day median total delay, noted in the underlying meta-analysis as an
   outlier on the high end among low/middle-income-country studies) — a real range, not a single
   number; the central estimate above uses the midpoint of that range.

Combining these gives a central gamma ≈ 0.118/month (D≈8.5 months) with a defensible operating
range of roughly [0.05, 0.30]/month (D between ~3.3 and 20 months), which is proposed as the
**primary** DE search bound, replacing the manuscript's [0.01, 0.50]/month. The manuscript's
original bound is retained as a mandatory sensitivity-analysis comparison arm (does the fitted
gamma or the model comparison change materially under the wider, less-anchored range?), not
discarded. **Classification: BOUND_REQUIRES_REVISION.**

### d — case fatality vs. mortality rate vs. compartmental hazard (detail, per explicit task instruction)

Three distinct quantities, never interchangeable:

- **Case fatality (cohort proportion)**: the fraction of a defined cohort of TB cases who die of
  TB during their disease course. Brazil, 2015-2017 notified cases: 3.2% (178,504 cases).
  Dimensionless, cohort-based, not a rate.
- **Population mortality rate**: deaths per 100,000 population per year (WHO Global TB Report
  figures for Brazil, order 2.4-3.6 per 100,000/year in recent years). This normalizes by total
  population, not by number of TB cases, and is not directly convertible to d without also
  knowing incidence/prevalence at the same time point — it answers a different question (national
  burden) than d does (individual hazard while infectious).
- **Compartmental hazard d**: the instantaneous per-month probability that an individual
  currently in I exits via TB death rather than via gamma (removal) or mu (background death).
  Under competing exponential hazards, the fraction of I-entrants who die (i.e., the case-fatality
  proportion, CFR) relates to d via `CFR = d / (gamma + mu + d)`. Solving with CFR≈0.032,
  gamma≈0.118/month, mu≈0.0011/month: `d ≈ CFR×(gamma+mu) / (1-CFR) ≈ 0.032×0.119/0.968 ≈
  0.0039/month`. This sits comfortably inside the manuscript's existing [0.0001,0.05] bound, so no
  bound revision is proposed for d, only this documented derivation. **Classification:
  BOUND_ACCEPTABLE.**

## 3. VALIDATION EXOGENOUS-INFORMATION CONTRACT

For the 2021-01 to 2022-12 validation window, the model may use **only** the following
demographic information, all derivable from data available by 2020-12:

1. Fit a simple trend (log-linear recommended, given population growth is approximately
   multiplicative) to the `populacao` series restricted to 2001-01 through 2020-12.
2. Extrapolate that fitted trend forward, month by month, through 2022-12, to produce N(t) for
   the validation window.
3. Use this extrapolated N(t) — **never** the dataset's own 2021-2022 `populacao` values — as
   the force-of-infection denominator during the open-loop validation simulation
   (`docs/MODEL_CONTRACT.md`, Sections 9-10).

This applies regardless of whether the dataset's actual 2021-2022 `populacao` values turn out
(on later provenance confirmation) to have been real-time-available "Estimativas da População"
figures — the extrapolation rule is adopted now, conservatively, precisely because that
confirmation does not exist (`PROVENANCE_REQUIRED`, Section 2). If the collaborator later
supplies documented provenance showing the 2021-2022 figures were genuinely available in real
time and are not census-calibrated retrospective revisions, this rule may be revisited as a new,
separately logged decision — never assumed permissible by default.

No other exogenous information dated after 2020-12 (revised life-expectancy figures, revised TB
treatment-outcome statistics, revised WHO regional estimates, etc.) may be used to set any fixed
quantity (mu, Lambda, or bounds) differently for the validation window than for calibration; mu
and Lambda are single constants for the entire 2001-2022 span (Section 2), so this is
automatically satisfied for those two but is stated explicitly here as a general rule covering
any future refinement.

## 4. FINAL EXECUTABLE PARAMETER CONTRACT

```
FIXED CONSTANTS (entire 2001-2022 span, not re-estimated, not time-varying):
  mu     = 1 / (74 * 12)                      ≈ 0.001126 month^-1
  Lambda = mu * mean(N(t), 2001-01..2020-12)  individuals/month

EXOGENOUS N(t):
  Calibration (2001-01..2020-12): N(t) = data column `populacao`, as supplied.
  Validation  (2021-01..2022-12): N(t) = forward extrapolation of a log-linear trend fit to
                                          `populacao` restricted to 2001-01..2020-12.
                                          Do NOT use the dataset's own 2021-2022 `populacao`
                                          values (PROVENANCE_REQUIRED, Sec. 2/3).

ESTIMATED PARAMETERS (fractional model): beta, sigma, gamma, d, alpha
  bounds:
    beta  : [0.01, 1.00]   month^-1   (unchanged)
    sigma : [0.01, 0.50]   month^-1   (unchanged; STRUCTURAL_LIMITATION_TO_DECLARE applies
                                        wherever sigma/R0 is interpreted, not to the bound itself)
    gamma : [0.05, 0.30]   month^-1   (PRIMARY, revised) / [0.01, 0.50] (SENSITIVITY ARM, manuscript-original)
    d     : [0.0001, 0.05] month^-1   (unchanged; central plausibility ~0.0039)
    alpha : [0.50, 1.00]   dimensionless (PRIMARY, revised) / [0.70, 1.00] (SENSITIVITY ARM, manuscript-original)

ESTIMATED PARAMETERS (integer comparator): beta, sigma, gamma, d   (alpha fixed = 1.0 exactly)
  bounds: same as above minus alpha.

All other items (initial conditions, observation model, solver, DE hyperparameters, validation
protocol, RMSE/MAE/bias definitions) are unchanged from docs/MODEL_CONTRACT.md, Sections 4-10.
```

## 5. UNRESOLVED ITEMS

Only genuine blockers/open loose ends, none of which stop implementation given the fallbacks
above:

- **N(t) provenance for 2021-2022** (`PROVENANCE_REQUIRED`): unresolved as a factual matter, but
  not blocking — the Section 3 extrapolation rule is a complete, conservative substitute. Should
  be revisited with the collaborator (Amaury de Souza) as a documentation task, not a modeling
  task.
- **Precise annual mu series (2001-2020)**: the ~74-year constant used here is interpolated from
  two verified anchor points (2000, 2019) plus knowledge that 2020-2022 were COVID-distorted
  outliers deliberately excluded; the full IBGE SIDRA Tabela 3825 / annual Tábua Completa de
  Mortalidade series was not pulled point-by-point. Low priority given negligible model
  sensitivity to mu.
- **T-compartment semantics** ("entered treatment" vs. "treated/completed") is genuinely
  ambiguous in the manuscript; this contract makes an explicit, logged choice (Section "gamma"
  detail) rather than leaving it open, so it is not a blocker, but it should be flagged if the
  manuscript is ever revised.

## 6. KILL/STOP CONDITION

No finding in this review produces a dimensional incompatibility or an undocumented-provenance
situation without a conservative substitute — implementation is **not** blocked. The one
condition that would newly justify stopping before implementation: if, during actual data
inspection at implementation time, the `populacao` column for 2021-2022 is found to be
**identical, to the last digit, to the post-2022-Census-calibrated retrospective series**
(rather than plausibly matching the real-time "Estimativas da População" series), that would be
strong evidence the entire historical `populacao` series (not just 2021-2022) was
retrospectively reconstructed by the collaborator using post-hoc-revised inputs, which could also
affect the 2001-2020 calibration-period N(t) in ways not yet audited. In that specific case,
implementation should pause and the full `populacao` series' provenance should be clarified with
the collaborator before calibration, rather than only patching the validation window as in
Section 3.
