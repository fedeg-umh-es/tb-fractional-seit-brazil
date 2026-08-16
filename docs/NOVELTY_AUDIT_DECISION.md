# Novelty Audit Decision Record

Date: 2026-08-16
Author: fedeg

---

## Decision parameters

```
GAP_STRENGTH                      = MODERATE
PORTFOLIO_DECISION                = ABSORB
DOMINANT_QUESTION                 = KEEP
IDENTIFIABILITY_AXIS              = INTEGRATED_SECONDARY_AXIS
CURRENT_EVIDENCE_SUFFICIENT       = YES
NEW_EXPERIMENT_REQUIRED           = NO
ARFIMA_BLOCKER                    = REJECTED_DIFFERENT_QUESTION
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

This is not claimed as a universally new principle. It is an empirical demonstration in a
model class (fractional epidemic models) where this evaluation was previously absent.

---

## Identifiability role

**Classification**: INTEGRATED_SECONDARY_AXIS

Identifiability functions as a secondary interpretive axis:

- Forecasting establishes what the model *cannot* do (beat external baselines).
- Identifiability establishes what it *can* do (bounded $R_0$, consistent Matignon stability).

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

```
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
- fractional models are superior
- $R_0$ is identifiable (without qualification)
- forecasting superiority

### Preferred bounded formulations

- "the literature examined..."
- "we evaluate..."
- "in this empirical setting..."
- "the results show..."
- "the analysis distinguishes..."
- "the distinctive contribution of this study lies in..."

---

## Literature anchors (priority)

1. **Chen et al. (2021)** — Review of fractional epidemic models. DOI: 10.1016/j.apm.2021.03.044
2. **Kharazmi et al. (2021)** — Identifiability and predictability of integer- and fractional-order
   epidemiological models. DOI: 10.1038/s43588-021-00158-0
3. **Roosa & Chowell (2019)** — Assessing parameter identifiability in compartmental dynamic
   models. DOI: 10.1186/s12976-018-0097-6 [already cited]
4. **Simpson & Maclaren (2024)** — Making Predictions Using Poorly Identified Mathematical
   Models. DOI: 10.1007/s11538-024-01294-0

These anchors were verified in the adversarial novelty audit (2026-08-16). Only verified and
scientifically relevant sources are included.

---

## Claim audit result

Search conducted across `manuscript_draft/` and `submission_bmb/BMB_MANUSCRIPT.md` for:
`first`, `novel`, `novelty`, `unprecedented`, `superior`, `superiority`, `demonstrate`,
`prove`, `generalize`.

**Finding**: Zero instances of unsupported novelty claims in manuscript prose. All occurrences
of `superiority` and `generalize` appear in negation context (e.g., "without claims of...
superiority", "does not generalize"). These are legitimate defensive qualifications.

**Action**: No claims required narrowing. The manuscript's language discipline is already
consistent with the novelty audit.

---

## Changes applied

- Introduction: No changes required. Already establishes criteria A–D.
- Discussion: Added one literature-boundary paragraph anchoring identifiability findings to
  established principles (Simpson & Maclaren 2024, Kharazmi et al. 2021).
- Discussion: Added Chen et al. (2021) as anchor for fractional epidemic model evaluation gap.
- References: Added Chen et al. (2021), Kharazmi et al. (2021), Simpson & Maclaren (2024).
- Conclusion: No changes required. Already uses bounded language.
- Abstract: No changes required.
- Methods: No changes required.
- Results: No changes required.

---

## Guardrails confirmed

- Canonical numerical results: UNCHANGED
- Methods: UNCHANGED
- Model implementation: UNCHANGED
- Figures/data: UNCHANGED
- BMB submission metadata: UNCHANGED
- No new scientific calculation performed.
