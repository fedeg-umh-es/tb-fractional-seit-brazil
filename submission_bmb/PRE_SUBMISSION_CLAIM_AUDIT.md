# Pre-submission Claim Precision Audit

**Target manuscript**: `submission_bmb/BMB_MANUSCRIPT.md`  
**Canonical evidence**: `results_canonical/`  
**Claim registry**: `manuscript_architecture/CLAIM_TRACEABILITY_MATRIX.csv` and `results_canonical/07_claim_support/claim_support_table.csv`  
**Scientific evidence status**: FROZEN  
**New experiments authorized by this audit**: NO

This audit checks whether the pre-submission narrative stays within the already-frozen evidence. It does not reassess or expand the experiment set.

---

## 1. Paper-level hierarchy

```text
DOMINANT_QUESTION = within-family improvement -> forecasting skill beyond model family
SECONDARY_AXIS = practical identifiability and robustness of derived quantities
IDENTIFIABILITY_AS_NOVELTY_CLAIM = NO
GENERIC_FRACTIONAL_SUPERIORITY = NO
BIOLOGICAL_MEMORY_CLAIM = NO
FORMAL_FORECAST_SIGNIFICANCE_CLAIM = NO
FIRST_STUDY_OR_HISTORICAL_ABSENCE_CLAIM = NO
```

**Verdict**: PASS after structural repair.

---

## 2. Claim-by-claim audit

| ID | Frozen evidence boundary | Manuscript-safe formulation | Audit status |
|---|---|---|---|
| C01 | Fractional SEIT has lower observed forecast error than independently refitted integer SEIT across evaluated protocols/horizons | Consistent **within-family** observed error reduction; no generic superiority | PASS |
| C02 | Observed skill versus persistence is negative at $h=1,\dots,12$ | Persistence has lower descriptive sample error than fractional SEIT at every evaluated horizon | PASS |
| C03 | Observed skill versus SARIMA is negative at $h=1,\dots,12$ | SARIMA has lower descriptive sample error than fractional SEIT at every evaluated horizon | PASS |
| C04 | Observed skill versus seasonal naive is positive only at $h=1,\dots,7$ | Baseline-specific positive-skill window; $H=7$ is an empirical descriptor, not a predictability limit | PASS |
| C05 | General operational fractional forecasting advantage is not supported | Within-family improvement is insufficient to establish general forecasting advantage beyond the model family | PASS after final Conclusion wording repair in source draft |
| C06 | $\alpha<1$ does not demonstrate biological memory | Fitted fractional order is not interpreted as evidence of biological/epidemiological memory | PASS |
| C07 | $R_0>1$ for all 25 near-equivalent admissible solutions; $R_0=1.1542$–$1.1892$ | Report as practical-identifiability envelope over the predefined admissible set, never as confidence/credible interval; broader 33-member pool explicitly excluded | PASS |
| C08 | DFE locally unstable for 25/25 admissible solutions under Matignon | Model property restricted to the predefined admissible set; no real-world persistence or forecasting claim | PASS |
| C09 | $\beta,\gamma,d$ are weakly identifiable | Do not interpret them as precisely estimated epidemiological rates | PASS after Abstract source wording repair |
| C10 | Historical ~48% optimal-control claim not verified | Optimal-control/historical burden-reduction claims remain outside current evidence base | PASS |
| C11 | Formal predictive superiority/inferiority not tested | Rolling-origin comparisons are descriptive; no formal significance or inferential superiority claim | PASS |

---

## 3. Methodological claims

| ID | Required boundary | Audit status |
|---|---|---|
| M01 | Observations are represented as monthly incidence flow via the $E\to I$ transition/accumulator, not as infectious stock | PASS |
| M02 | Common reference-time scaling $\tau_0=1$ month resolves dimensional consistency without changing numerical trajectories | PASS |
| M03 | Weak individual-parameter identifiability can coexist here with comparatively stable trajectories and robust derived quantities | PASS |
| M04 | Rolling-origin evaluation uses strict temporal separation and train-only information at each origin | PASS |

---

## 4. Terminology controls

```text
PROFILE_LIKELIHOOD_AS_EXECUTED_METHOD = FORBIDDEN
CANONICAL_TERM = profile-objective exploration

EXTERNAL_PREREGISTRATION_CLAIM = FORBIDDEN_UNLESS_DOCUMENTED
CANONICAL_TERM = prespecified / documented before execution

R0_CONFIDENCE_INTERVAL = FORBIDDEN
CANONICAL_TERM = practical-identifiability envelope

H7_PREDICTABILITY_LIMIT = FORBIDDEN
CANONICAL_TERM = baseline-specific empirical horizon descriptor

ALPHA_MEMORY_EVIDENCE = FORBIDDEN

GENERIC_FRACTIONAL_SUPERIORITY = FORBIDDEN

FORECAST_SIGNIFICANCE = NOT_TESTED
```

**Verdict**: PASS in repaired source sections and submission package. Historical/internal frozen artifacts may retain older repository terminology; they are not to be rewritten if doing so would modify the frozen evidence package. Submission-facing text must use the canonical terminology above.

---

## 5. Figure/table claim audit

`submission_bmb/BMB_FIGURE_TABLE_PACKAGE.md` was repaired so that:

- Figure 1 explicitly separates the within-family comparator from the three external baselines.
- Figure 2 explicitly labels skill as descriptive and states that no prespecified predictive-accuracy significance test was applied.
- Figure 3 explicitly states that the $R_0$ range is a practical-identifiability envelope and not a confidence or credible interval.
- Figure S1 is diagnostic context only.
- Table S3 uses **profile-objective diagnostic exploration**, not profile likelihood.
- Long-open-loop and rolling-origin results remain visibly separate protocols.

**Verdict**: PASS. No figure or table regeneration is required.

---

## 6. Residual synchronization item

Two source-level wording repairs were made during this audit:

1. `manuscript_draft/ABSTRACT_DRAFT.md`: changed the parameter-identifiability implication from an absolute prohibition on interpreting parameters as biological rates to the evidence-supported boundary that they cannot be treated as **precisely estimated epidemiological rates**; the secondary status of the mechanistic axis is also explicit.
2. `manuscript_draft/CONCLUSION_DRAFT.md`: replaced the unqualified phrase that the external test "failed" with a benchmark-specific statement: persistence and SARIMA remain unfavorable at all horizons, while seasonal-naive skill is positive only through $h=7$.

These two source repairs must be synchronized into `submission_bmb/BMB_MANUSCRIPT.md` before `CLAIM_PRECISION_AUDIT` can be marked fully complete for the canonical assembled manuscript.

---

## 7. Gate decision

```text
SCIENTIFIC_BLOCKER = NO
NEW_EXPERIMENT_REQUIRED = NO
FROZEN_NUMBERS_CHANGED = NO
FROZEN_EVIDENCE_CHANGED = NO
FIGURE_REGENERATION_REQUIRED = NO
CLAIM_REGISTRY_CONSISTENCY = PASS
SOURCE_DRAFT_CLAIMS = PASS
CANONICAL_ASSEMBLY_SYNC = PENDING_TWO_BOUNDED_TEXT_REPAIRS
PHASE_3_STATUS = PASS_PENDING_CANONICAL_SYNC
NEXT_ALLOWED_STAGE = canonical sync -> controlled prose pass
```
