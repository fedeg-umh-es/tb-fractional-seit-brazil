# Bulletin of Mathematical Biology — Manuscript Abstract

## Target Journal
* **Journal**: *Bulletin of Mathematical Biology* (Springer Nature / Society for Mathematical Biology)
* **Word Limit Ceiling**: $\le 250\text{ words}$
* **Target Range**: $220\text{–}245\text{ words}$

---

## Abstract Text

Assessing fractional-order compartmental models for forecasting requires separating within-family improvement from performance against external baselines. We independently reimplemented and audited a Caputo fractional-order SEIT tuberculosis model using monthly Brazilian surveillance data from 2001–2022, with notifications represented as incidence flow. In a 24-month open-loop stress test and a 13-origin rolling-origin evaluation across 12 monthly lead horizons, the fractional model attained lower forecast error than an independently re-estimated integer-order comparator under the same parameter bounds. This within-family advantage did not translate into positive observed skill against persistence or SARIMA at any evaluated horizon ($H_{\text{relax}} = 0$). Observed skill relative to seasonal naive was positive from $h=1$ through $h=7$ ($H_{\text{relax}} = 7$), with a 2.7% margin at $h=7$; this is a baseline-specific empirical descriptor. As a secondary analysis, practical identifiability was weak for $\beta$, $\gamma$, and $d$, precluding their interpretation as precisely estimated epidemiological rates despite comparatively stable trajectory predictions. Across the predefined 25-member near-equivalent admissible set ($\Delta \text{RMSE}_{\text{cal}} \le 1.0\%$), $R_0$ ranged from 1.1542 to 1.1892, conditional on the latent-progression rate $\sigma$ lying at its lower search bound in every solution; local instability of the Disease-Free Equilibrium followed from $R_0 > 1$. Within this case study, within-family error reduction therefore did not extend to a general forecasting advantage over external baselines, and the identifiability results bound the mechanistic interpretation of the fitted model rather than constituting an independent forecasting claim.

---

## Abstract Audit & Verification

```text
ABSTRACT_WORD_COUNT = 228 (whitespace-delimited tokens, LaTeX included)
ABSTRACT_LIMIT_VERIFIED = YES (228 <= 250)
SYNCED_WITH_MANUSCRIPT = 2026-10-01 (text identical to the Abstract in BMB_MANUSCRIPT.md; claim-audit items A-F)
ABSTRACT_TURNING_POINT_VISIBLE = YES
CONTROL_SENTENCE_INCLUDED = YES
PROHIBITED_WORDS_ABSENT = YES
DESK_REVIEW_INTEGRITY = PASS
```

### Key Elements Preserved:
1. **Methodological Framing**: Distinguishing within-family improvement from external statistical benchmarks.
2. **Empirical Evaluation**: 24-month open-loop stress test and 13 rolling origins across 12 monthly horizons ($h = 1 \dots 12$).
3. **Within-Family Result**: Fractional SEIT achieves lower RMSE/MAE than independently refitted integer SEIT under the same frozen parameter bounds (not attributed to the fractional operator alone).
4. **Central Turning Point (Verbatim Control Sentence)**: Negative skill against persistence and SARIMA across all horizons ($H_{\text{relax}} = 0$).
5. **Seasonal Naive Exception**: Bounded positive skill for $h = 1 \dots 7\text{ months}$ ($H_{\text{relax}} = 7$), with a 2.7% margin at $h = 7$.
6. **Mechanistic Identifiability**: Weak parameter identifiability for $\beta, \gamma, d$ coexisting with stable trajectory predictions.
7. **Derived Quantities, Bounded**: Narrow $R_0$ envelope ($1.1542\text{–}1.1892$) conditional on $\sigma$ at its lower search bound in all 25 solutions; DFE instability follows from $R_0 > 1$ and is not an independent result.
