# Discussion Argument Map

No Discussion prose is drafted here. The most important objection is confronted first, per
instruction, before the remaining findings are addressed in Results order.

## D0 (lead) -- Does fractional improvement over the integer model imply better forecasting?

- **Finding**: R1 (C01) shows fractional < integer error consistently.
- **Obvious reviewer objection**: "If fractional beats integer, doesn't that mean the fractional
  model is a better forecaster, period?"
- **Existing evidence addressing it**: R2 (C02, C03) -- persistence and SARIMA both beat the
  fractional model at every evaluated horizon.
- **Interpretation allowed**: No -- improving a mechanistic model relative to a nested,
  less-flexible variant of itself is not equivalent to, and does not imply, competitiveness
  against purpose-built or naive external forecasting methods. The two are different comparison
  classes.
- **Remaining limitation**: Only one long-open-loop origin and 13 rolling-origin origins were
  evaluated; the result is protocol- and dataset-specific, not a general theoretical claim about
  fractional calculus.
- **Bounded conclusion**: Fractional order is a genuine within-family improvement to this SEIT
  formulation; that improvement did not translate into external forecasting competitiveness in
  this study.

## D1 -- Why is improvement over integer SEIT insufficient evidence of forecasting superiority?

- **Finding**: R1/R2 jointly (C01 vs. C02/C03).
- **Obvious reviewer objection**: "Isn't the integer-order model a reasonable proxy for
  'standard' forecasting practice, making this comparison sufficient?"
- **Existing evidence addressing it**: Persistence and SARIMA are simpler and, in the case of
  SARIMA, purpose-built statistical forecasting tools; both outperform the mechanistic model
  family entirely (both fractional and integer), so the integer comparator is not a stand-in for
  "forecasting practice" -- it is a nested structural variant of the same mechanistic model.
- **Interpretation allowed**: A model-family-internal ablation (fractional vs. integer) answers
  a structural question about the SEIT formulation; it does not substitute for an external
  forecasting-competitiveness test.
- **Remaining limitation**: Only one purpose-built statistical baseline (SARIMA, one frozen
  order) and one naive baseline family (persistence, seasonal-naive) were tested.
- **Bounded conclusion**: The two evaluation questions (structural improvement vs. forecasting
  competitiveness) require separate baselines and separate claims; this study reports both,
  cleanly separated (Results R1 vs. R2).

## D2 -- What do the persistence/SARIMA comparisons change scientifically?

- **Finding**: R2 (C02, C03, C05).
- **Obvious reviewer objection**: "Doesn't a negative result here undermine the paper's
  contribution?"
- **Existing evidence addressing it**: None needed to rebut -- the negative result is itself the
  contribution: it demonstrates, with a controlled leakage-free protocol, that a common
  evaluation gap (comparing a mechanistic model only to simpler variants of itself) can produce
  a misleadingly favorable picture if external baselines are omitted.
- **Interpretation allowed**: The negative comparisons are central evidence, not a defect to
  explain away; they directly answer the paper's second research question (Sec 3.2 of the
  architecture task).
- **Remaining limitation**: Descriptive only; no significance test performed (see D9).
- **Bounded conclusion**: External-baseline evaluation substantially narrows what can be claimed
  about the fractional model's practical forecasting value, independent of its structural
  merits.

## D3 -- What does the seasonal-naive horizon boundary (h=7) mean?

- **Finding**: R3 (C04).
- **Obvious reviewer objection**: "Does this mean the model is useful for short-term
  forecasting?"
- **Existing evidence addressing it**: The bounded result applies to exactly one baseline
  (seasonal-naive), not to persistence or SARIMA, and is drawn from only 13 origins.
- **Interpretation allowed**: A dataset/protocol-specific descriptor of where one particular
  comparison flips sign; not a general predictability-horizon claim and not evidence of
  practical short-term forecasting utility, since the two other, arguably more informative,
  baselines are never beaten at any horizon.
- **Remaining limitation**: Small-sample horizon-wise estimate (n=13 per cell); no formal test
  of whether h=7 is a stable feature of the data-generating process or protocol noise.
- **Bounded conclusion**: A single-baseline, bounded-horizon positive result exists and is
  reported as such -- it does not rescue a general forecasting-advantage claim.

## D4 -- Why does weak individual parameter identifiability matter?

- **Finding**: R4a (C09).
- **Obvious reviewer objection**: "The calibration converged and produced a low RMSE -- doesn't
  that mean the parameters are trustworthy?"
- **Existing evidence addressing it**: Multiseed and profile-objective evidence shows near-
  identical calibration RMSE (CV~0.35%) achieved by beta/gamma/d combinations differing by
  5x-100x+ -- convergence and low RMSE do not imply unique or precise parameter recovery.
- **Interpretation allowed**: beta, sigma, gamma, d must not be cited as biologically meaningful
  point estimates (e.g. "the transmission rate was X per month") anywhere in the manuscript.
- **Remaining limitation**: Identifiability was assessed practically (multiseed + local profile),
  not via a full structural-identifiability analysis of the ODE system.
- **Bounded conclusion**: This study reports calibrated-model behavior and derived quantities,
  not individual mechanistic rate estimates.

## D5 -- Why can R0 robustness coexist with weak individual parameter estimates?

- **Finding**: R4b (C07) alongside R4a (C09).
- **Obvious reviewer objection**: "If beta/gamma/d aren't identifiable, how can R0 -- which is
  built from them -- be robust?"
- **Existing evidence addressing it**: The near-equivalent admissible set shows R0 confined to
  [1.1542, 1.1892] while its components vary far more widely -- a functional-combination
  identifiability pattern distinct from single-parameter identifiability (predictive
  identifiability shows the same pattern: 0.19%/0.58% prediction CV).
- **Interpretation allowed**: R0 (and predictions) are compensating combinations of the
  individually weak parameters; this is a property of the model's structure under this
  calibration procedure, not evidence that the individual parameters are secretly well
  determined.
- **Remaining limitation**: This is an empirical (numerical) observation over a bounded
  practical-identifiability envelope, not a formal proof of structural identifiability of the
  R0 functional.
- **Bounded conclusion**: Different quantities derived from the same calibration carry different
  epistemic weight; R0 and predictions are the two that can be reported with confidence here.

## D6 -- What does the DFE result support?

- **Finding**: R5 (C08).
- **Obvious reviewer objection**: "Does instability of the DFE tell us anything new beyond
  R0>1?"
- **Existing evidence addressing it**: The Matignon-criterion classification (0 stable/25
  unstable/0 ambiguous) is an independent confirmation, computed per-solution using each
  solution's own fitted alpha, that the R0>1 threshold and the fractional stability criterion
  agree throughout the admissible set.
- **Interpretation allowed**: The qualitative conclusion ("persistent transmission dynamically
  consistent with the fitted model") is well supported within the admissible set.
- **Remaining limitation**: Restricted to the 25-member near-equivalent admissible set; the full
  33-solution profile pool includes 2 stable (diagnostic-only) points and must not be cited as
  contradicting or extending this result.
- **Bounded conclusion**: DFE instability is a robust, internally consistent mechanistic result
  within the defined admissible set -- and nothing more than that.

## D7 -- Why must mechanistic and forecasting conclusions remain separate?

- **Finding**: Cross-cutting (R1-R3 vs. R4-R5).
- **Obvious reviewer objection**: "If R0>1 and the DFE is unstable, doesn't that support the
  model's predictive validity?"
- **Existing evidence addressing it**: None of R4/R5's evidence involves out-of-sample
  forecasting performance; R1-R3's evidence involves no equilibrium analysis. They are
  computed from different procedures answering different questions.
- **Interpretation allowed**: Mechanistic self-consistency (a stable, well-behaved calibrated
  dynamical system) is a necessary sanity property, not evidence of forecasting accuracy against
  external baselines.
- **Remaining limitation**: None beyond restating the general separation.
- **Bounded conclusion**: The paper must never present R4/R5 as support for, or in tension with,
  R1-R3's forecasting conclusions.

## D8 -- Why can't alpha<1 be presented as evidence of epidemiological memory?

- **Finding**: Alpha stability (C06, negative claim).
- **Obvious reviewer objection**: "Alpha was reliably estimated below 1 -- doesn't that confirm
  memory effects in TB transmission?"
- **Existing evidence addressing it**: Alpha's numerical stability across seeds and bound
  restriction (`IDENTIFIABILITY_AUDIT_REPORT.md`) shows the *estimate* is reliable; it says
  nothing about whether the fractional-order mechanism corresponds to an actual biological or
  epidemiological memory process versus a flexible curve-fitting device.
- **Interpretation allowed**: Report alpha's numerical stability as a modeling result; do not
  claim it demonstrates a biological mechanism.
- **Remaining limitation**: No independent biological evidence (e.g. mechanistic latency data)
  was brought to bear on this question in this study.
- **Bounded conclusion**: Alpha is a well-identified model parameter; its biological
  interpretation remains an open question outside this study's evidentiary scope.

## D9 -- What cannot yet be claimed because rolling-origin inference is descriptive?

- **Finding**: C11 (inference boundary).
- **Obvious reviewer objection**: "Are the negative-skill results statistically significant?"
- **Existing evidence addressing it**: No DM test (or equivalent) has been run; serial
  dependence of rolling-origin horizon-specific loss differentials has not been characterized
  (distinct from the long-open-loop residual autocorrelation, which *was* characterized and is
  not a substitute).
- **Interpretation allowed**: "Observed" / "descriptive" skill language only; explicitly no
  "statistically significant" language anywhere.
- **Remaining limitation**: A future pre-specified, horizon-wise, HAC-aware DM protocol would be
  required before any significance claim.
- **Bounded conclusion**: The skill findings stand as descriptive, reproducible, leakage-audited
  observations -- not as tested statistical claims.

## D10 -- What remains outside this study?

- **Finding**: Scope boundary.
- **Obvious reviewer objection**: "Why doesn't this paper address optimal control or the
  historical 48% claim, given the manuscript this reimplements discusses them?"
- **Existing evidence addressing it**: Optimal control was never implemented or verified in this
  reimplementation (`OPTIMAL_CONTROL=DEFERRED_NOT_VERIFIED`); the historical ~48% claim is
  `NOT_VERIFIED` and REFERENCE_ONLY_NOT_EVIDENCE throughout this project.
- **Interpretation allowed**: State the scope boundary plainly; do not attempt to explain away
  or apologize for not covering it.
- **Remaining limitation**: N/A -- this is itself the limitation statement.
- **Bounded conclusion**: DM inference, optimal control, and the historical 48% claim are
  explicitly out of scope for this study and deferred to future, separately-scoped work.
