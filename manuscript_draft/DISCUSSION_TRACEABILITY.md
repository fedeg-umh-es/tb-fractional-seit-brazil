# Discussion Traceability and Argument Audit

**Canonical Discussion text**: `submission_bmb/BMB_MANUSCRIPT.md` §4  
**Source draft**: `manuscript_draft/DISCUSSION_DRAFT.md`  
**Gate 2 status**: `CLOSED`

```text
CENTRAL_TURNING_POINT_LEADS_DISCUSSION = YES
NEW_EMPIRICAL_RESULT_INTRODUCED = NO
HISTORICAL_ABSENCE_CLAIM = NO
FIRST_STUDY_CLAIM = NO
FORECASTING_MECHANISTIC_CONFLATION = NO
IDENTIFIABILITY_AS_SECONDARY_AXIS = YES
R0_ENVELOPE_BOUNDARY_RESPECTED = YES
DFE_MODEL_PROPERTY_GUARDRAIL_RESPECTED = YES
```

## D1 — Main turning point

- Evidence: fractional SEIT has lower error than independently refitted integer SEIT; persistence and SARIMA have lower error than fractional SEIT across all evaluated horizons.
- Permitted interpretation: restricting comparison to the mechanistic family yields a more favorable assessment than external benchmarking.
- Forbidden: generic fractional inferiority/superiority or formal significance claims.

## D2 — External-baseline role and literature boundary

- Evidence: same R1/R2 contrast.
- Core citations: Moran et al. (2016); Cramer et al. (2022); Chen et al. (2021); Kharazmi et al. (2021).
- Gate 2 delimiters added to manuscript: Chishtie et al. (2026), Alzahrani et al. (2024), Kalizhanova et al. (2024).
- Permitted interpretation: adjacent pieces of the problem already exist in the literature; the manuscript asks whether a favorable fractional-vs-integer conclusion survives expansion to external baselines under a common temporal multi-horizon protocol.
- Forbidden: `fractional epidemic models have never been externally benchmarked`; `first study`; universal absence.

## D3 — Seasonal-naive bounded exception

- Evidence: positive skill vs seasonal naive at h=1..7 only; negative at h=8..12.
- Permitted: baseline- and horizon-specific empirical descriptor.
- Forbidden: intrinsic seven-month biological predictability horizon.

## D4 — Parameter non-identifiability vs prediction stability

- Evidence: beta, gamma and d disperse strongly among near-equivalent fits; trajectories are comparatively stable.
- Citations: Tuncer & Le (2018); Roosa & Chowell (2019), DOI `10.1186/s12976-018-0097-6`.
- Forbidden: precise biological interpretation of individual rate estimates; alpha<1 as proof of biological memory.

## D5 — R0 practical-identifiability envelope

- Evidence: R0 in [1.1542, 1.1892] across the predefined 25-member admissible set.
- Citations: Meshkat et al. (2014); Raue et al. (2009).
- Forbidden: confidence interval / credible interval language or generalization to the broader diagnostic pool.

## D6 — Established identifiability principles

- Citations: Simpson & Maclaren (2024); Gutenkunst et al. (2007); Meshkat et al. (2014); Kao & Eisenberg (2018).
- Role: explicitly prevents novelty claims for prediction under parameter non-identifiability or robust composite quantities.

## D7 — DFE stability

- Evidence: 25/25 admissible solutions locally unstable under Matignon's criterion.
- Interpretation: mathematical property of calibrated model; dynamically consistent with R0>1 within the admissible set.
- Forbidden: empirical proof of persistent real-world transmission or evidence of forecasting skill.

## D8 — Boundaries and contribution

- Single national monthly series.
- Descriptive rolling-origin comparisons; no post-hoc predictive-accuracy test.
- Practical-identifiability envelope is operational, not formal statistical uncertainty.
- Optimal-control and historical burden-reduction claims remain outside the reimplementation.
- Bounded contribution: within-family improvement can change interpretation when tested against external baselines; identifiability limits point interpretation while some derived quantities remain robust.
