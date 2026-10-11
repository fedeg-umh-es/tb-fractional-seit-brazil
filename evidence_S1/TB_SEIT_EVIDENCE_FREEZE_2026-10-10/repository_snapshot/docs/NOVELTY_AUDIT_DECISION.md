# Novelty Audit Decision Record

Date: 2026-08-16  
Last external-verification update: 2026-09-05  
Author: fedeg

---

## Decision parameters

```text
GAP_STRENGTH                      = MODERATE
PORTFOLIO_DECISION                = ABSORB
DOMINANT_QUESTION                 = KEEP
IDENTIFIABILITY_AXIS              = INTEGRATED_SECONDARY_AXIS
CURRENT_EVIDENCE_SUFFICIENT       = YES
NEW_EXPERIMENT_REQUIRED           = NO
ARFIMA_BLOCKER                    = REJECTED_DIFFERENT_QUESTION
GATE_2_EXTERNAL_VERIFICATION      = CLOSED
DIRECT_PRECEDENT_IN_SEARCHED_SET  = NOT_LOCATED
FIRST_STUDY_CLAIM                 = PROHIBITED
UNIVERSAL_ABSENCE_CLAIM           = PROHIBITED
```

---

## Dominant question (preserved)

> Does improvement of a fractional-order mechanistic epidemic model over its independently
> refitted integer-order counterpart translate into forecasting skill beyond the model family?

Interpreted as an evidence-bounded question for the present TB/Brazil design, not a universal
claim about all fractional epidemic models.

---

## Strongest defensible contribution

External evaluation of whether fractional-vs-integer within-family improvement survives
comparison with statistical forecasting baselines, complemented by bounded interpretation under
practical non-identifiability.

Specifically:

1. **Within-family improvement** (fractional > integer SEIT) is empirically established.
2. **External skill** against persistence and SARIMA is negative at all evaluated horizons.
3. **Weak parameter identifiability** coexists with robust derived $R_0$ and Matignon stability.

The central empirical contribution is:

> WITHIN-FAMILY IMPROVEMENT ≠ EXTERNAL FORECAST SKILL

This is not claimed as a universally new principle and is not supported by a historical-priority
claim. The distinctive contribution lies in testing whether a favorable fractional-vs-integer
conclusion survives a common temporal multi-horizon evaluation against external statistical and
naive forecasting baselines, and in documenting that the inference changes in this TB/Brazil
case.

---

## Gate 2 external verification closure

The adversarial literature search was closed on 2026-09-05 after repeated targeted searches for
studies jointly satisfying all of the following:

1. fractional-order mechanistic epidemic model;
2. comparable integer-order counterpart;
3. external statistical and/or naive forecasting baselines;
4. genuine out-of-sample temporal evaluation; and
5. multiple forecast horizons and/or origins under a common protocol.

**Result**: no direct precedent satisfying all five conditions simultaneously was located in the
searched corpus.

This result is deliberately bounded. It does **not** establish that no such study exists and does
**not** justify `first study`, `never evaluated`, `unprecedented`, or equivalent wording.

Closest adversarial neighbors and their limiting differences are documented in
`literature_verification/LITERATURE_VERIFICATION_MATRIX.md` under L5.

### Scientific friction retained

The literature separately establishes that:

- fractional epidemic formulations can outperform their integer-order counterparts, including in
  some held-out or rolling-origin evaluations;
- fractional epidemic models have been compared with ARIMA-type models;
- identifiability and predictability of integer/fractional epidemiological models have already
  been studied; and
- mechanistic TB models can underperform statistical forecasting approaches such as SARIMA.

The manuscript-relevant unresolved question is therefore not an exact-combination absence claim.
It is whether a favorable fractional-vs-integer result retains its interpretation when the
benchmark set is expanded beyond the model family under a common temporal forecasting protocol.

---

## Identifiability role

**Classification**: INTEGRATED_SECONDARY_AXIS

Identifiability functions as a secondary interpretive axis:

- Forecasting establishes what the model *cannot* do (beat external baselines).
- Identifiability establishes what remains bounded or robust despite weak individual-parameter
  recovery.

Established literature already supports:

- Prediction can remain informative under parameter non-identifiability (Simpson & Maclaren,
  2024; Gutenkunst et al., 2007; Kao & Eisenberg, 2018).
- $R_0$ / composite quantities can be more robust than individual parameters (Meshkat et al.,
  2014; Tuncer & Le, 2018).

Therefore identifiability principles are NOT claimed as contributions invented here. Our
contribution is an applied demonstration showing what remains interpretable in this specific
fractional SEIT evaluation.

---

## ARFIMA experiment — rejection rationale

```text
ARFIMA_EXPERIMENT = NOT_REQUIRED
```

An ARFIMA or other fractional statistical comparator would address the different question of
*why* the fractional SEIT improves over the integer SEIT, or whether long-memory structure in
the data explains that improvement.

That question is outside the dominant manuscript question ("does fractional-vs-integer
improvement translate into forecasting skill beyond the model family?").

The current evidence is sufficient to answer the dominant question without an ARFIMA
experiment.

---

## Novelty language discipline

### Forbidden terms (in unsupported context)

- first
- novel framework
- unprecedented
- previous studies have never
- never evaluated
- fractional models are superior
- $R_0$ is identifiable (without qualification)
- forecasting superiority

### Preferred bounded formulations

- "the literature examined..."
- "no direct precedent was located in the searched corpus..."
- "we evaluate..."
- "in this empirical setting..."
- "the results show..."
- "the analysis distinguishes..."
- "the distinctive contribution of this study lies in..."
- "the inference changes when the benchmark set is expanded beyond the model family..."

---

## Literature anchors (priority)

### Existing manuscript anchors

1. **Chen et al. (2021)** — Review of fractional epidemic models. DOI: 10.1016/j.apm.2021.03.044
2. **Kharazmi et al. (2021)** — Identifiability and predictability of integer- and fractional-order
   epidemiological models. DOI: 10.1038/s43588-021-00158-0
3. **Roosa & Chowell (2019)** — Assessing parameter identifiability in compartmental dynamic
   models. DOI: 10.1186/s12976-018-0097-6
4. **Simpson & Maclaren (2024)** — Making Predictions Using Poorly Identified Mathematical
   Models. DOI: 10.1007/s11538-024-01294-0

### Gate 2 adversarial neighbors to be considered during manuscript citation review

- **Chishtie et al. (2026)** — fractional vs integer with rolling-origin OOS, 7/14/21-day horizons;
  no external statistical/naive benchmark in the same protocol. DOI: 10.1016/j.epidem.2026.100887
- **Alzahrani et al. (2024)** — fractional SEIR vs ARIMA; no equivalent rolling-origin
  multi-horizon benchmark. DOI: 10.18576/amis/180101
- **Rajagopal et al. (2020)** — fractional vs integer prediction on held-out data; no external
  benchmark suite. DOI: 10.1007/s11071-020-05757-6
- **Kalizhanova et al. (2024)** — TB SIR vs SARIMA with temporally separated evaluation; no
  fractional model. DOI: 10.1038/s41598-024-76721-2
- **Jiru & Kumaravel (2026)** — fractional/integer SEIHR with OLS comparator but only three annual
  observations and no comparable multi-origin/multi-horizon evaluation. DOI: 10.1038/s41598-026-56464-y
- **Muhafzan et al. (2024)** — fractional SEIT for TB focused on stability/vaccination rather than
  OOS forecasting. DOI: 10.28919/cmbn/8853

These sources delimit the contribution. They are not used to manufacture an absence claim.

---

## Claim audit result

The previous claim audit found zero unsupported novelty claims in manuscript prose. After Gate 2
closure, one internal novelty-record sentence was narrowed: the prior wording that external
baseline evaluation was "previously absent" from the model class is no longer retained.

**Current rule**: manuscript prose must not assert historical absence. Any novelty framing must be
based on the scientific friction and on the empirical change in inference when the comparison set
is expanded beyond the fractional/integer family.

---

## Changes applied in this update

- `literature_verification/LITERATURE_VERIFICATION_MATRIX.md`: added L5 adversarial direct-precedent
  section and formal Gate 2 closure.
- Corrected Roosa & Chowell (2019) DOI in the literature matrix to
  `10.1186/s12976-018-0097-6`.
- This file: removed the obsolete wording that the evaluation was "previously absent" from
  fractional epidemic models.
- Added bounded Gate 2 language and explicit prohibition of historical-priority claims.
- Canonical numerical results: unchanged.
- Methods and model implementation: unchanged.
- No new scientific calculation performed.

---

## Guardrails confirmed

- Canonical numerical results: UNCHANGED
- Methods: UNCHANGED
- Model implementation: UNCHANGED
- Figures/data: UNCHANGED
- BMB submission metadata: UNCHANGED
- No new experiment required by Gate 2
- Identifiability remains secondary
- Portfolio decision remains `ABSORB`
