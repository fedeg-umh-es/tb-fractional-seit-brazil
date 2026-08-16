# Bulletin of Mathematical Biology — Manuscript Abstract

## Target Journal
* **Journal**: *Bulletin of Mathematical Biology* (Springer Nature / Society for Mathematical Biology)
* **Word Limit Ceiling**: $\le 250\text{ words}$
* **Target Range**: $220\text{–}245\text{ words}$

---

## Abstract Text

Assessing the forecasting utility of fractional-order compartmental models requires distinguishing within-family improvement from performance against external statistical baselines. This study presents an independent reimplementation and methodological audit of a Caputo fractional-order SEIT tuberculosis model applied to Brazilian monthly surveillance data (2001–2022) with notifications mapped to incidence flow. Across a 24-month open-loop simulation and a 13-origin rolling-origin evaluation over 12 monthly lead horizons ($h = 1 \dots 12$), the fractional SEIT model achieved lower forecast error than an independently refitted integer-order comparator. Although the fractional formulation consistently reduced forecast error relative to the independently refitted integer-order SEIT model, this within-family improvement did not translate into positive observed forecast skill against persistence or SARIMA at any evaluated horizon ($H_{\text{relax}} = 0$). Positive observed skill relative to seasonal naive was confined to lead times $h = 1$ through $7\text{ months}$ ($H_{\text{relax}} = 7$), serving as a baseline-specific empirical descriptor. Calibration revealed pronounced practical non-identifiability for individual kinetic rate parameters ($\beta$, $\gamma$, $d$), precluding their interpretation as biological rates despite stable trajectory predictions. Conversely, derived dynamical properties were functionally robust across the 25-member near-equivalent admissible set ($\Delta \text{RMSE}_{\text{cal}} \le 1.0\%$), defining a narrow practical-identifiability envelope for the basic reproduction number ($R_0 \in [1.1542, 1.1892]$) and uniform local instability of the Disease-Free Equilibrium under Matignon's criterion. Fractional differentiation provided within-family error reduction, external baselines exposed the limits of interpreting that improvement as forecasting skill, and weak parameter identifiability coexisted with robust derived threshold properties across the admissible set.

---

## Abstract Audit & Verification

```text
ABSTRACT_WORD_COUNT = 243
ABSTRACT_LIMIT_VERIFIED = YES (243 <= 250)
ABSTRACT_TURNING_POINT_VISIBLE = YES
CONTROL_SENTENCE_INCLUDED = YES
PROHIBITED_WORDS_ABSENT = YES
DESK_REVIEW_INTEGRITY = PASS
```

### Key Elements Preserved:
1. **Methodological Framing**: Distinguishing within-family improvement from external statistical benchmarks.
2. **Empirical Evaluation**: 24-month open-loop stress test and 13 rolling origins across 12 monthly horizons ($h = 1 \dots 12$).
3. **Within-Family Result**: Fractional SEIT achieves lower RMSE/MAE than independently refitted integer SEIT.
4. **Central Turning Point (Verbatim Control Sentence)**: Negative skill against persistence and SARIMA across all horizons ($H_{\text{relax}} = 0$).
5. **Seasonal Naive Exception**: Bounded positive skill for $h = 1 \dots 7\text{ months}$ ($H_{\text{relax}} = 7$).
6. **Mechanistic Identifiability**: Weak parameter identifiability for $\beta, \gamma, d$ coexisting with stable trajectory predictions.
7. **Derived Functional Robustness**: Narrow $R_0$ envelope ($1.1542\text{–}1.1892$) and DFE instability under Matignon's criterion across the admissible set.
