# Reproducibility status

Live tracking table. Update statuses as work progresses; never mark an item COMPLETE or
VERIFIED without a corresponding, checkable artifact in this repository.

| Item                                   | Status       |
|-----------------------------------------|--------------|
| Dataset integrity                       | VERIFIED     |
| Original source preservation            | COMPLETE     |
| Original code recovered                 | NO           |
| Exact reproduction                      | NOT_POSSIBLE |
| Independent reimplementation            | REQUIRED     |
| Method specification                    | COMPLETE (base-model scope only) |
| Base-model implementation (code)        | COMPLETE    |
| Numerical solver verification           | VERIFIED    |
| Numerical convergence (h selection)     | VERIFIED    |
| Population exogenous series (leakage-safe) | COMPLETE |
| Model constants (mu, Lambda)            | COMPLETE    |
| Optimization contract (DE hyperparameters + seeds) | COMPLETE — seeds frozen D024 |
| Fractional model calibration (primary seed 20260815) | COMPLETE  |
| Integer model calibration (primary seed 20260815) | COMPLETE  |
| Multi-seed robustness diagnostics       | COMPLETE — see identifiability caveat below |
| Alpha-bound sensitivity ([0.70,1.00] vs [0.50,1.00]) | COMPLETE — alpha materially unchanged |
| Strict 2021-2022 validation             | COMPLETE — fractional RMSE 1117.96 < integer RMSE 1759.54 |
| Individual-parameter identifiability (beta, gamma, d) | WEAKENS — CV 58-82% across seeds despite stable objective (CV 0.35%); see BASE_MODEL_REIMPLEMENTATION_REPORT.md Sec 12 |
| Fractional model reproduction           | NOT_STARTED (exact reproduction of manuscript values is NOT_POSSIBLE; independent values above are the reimplementation result) |
| Integer model reproduction              | NOT_STARTED (same) |
| Predictive validation                   | COMPLETE (see strict validation row above) |
| R0                                      | NOT_STARTED — see next-gate note (identifiability caveat applies) |
| Stability                               | NOT_STARTED  |
| Sensitivity                             | NOT_STARTED  |
| Optimal control                         | NOT_STARTED  |
| 48% claim                               | NOT_VERIFIED |
| Manuscript revision                     | BLOCKED      |
| LaTeX conversion                        | BLOCKED      |

## Dataset integrity evidence

Confirmed by `scripts/audit_dataset.py` -> `outputs/audits/dataset_integrity.json`:
TOTAL_MONTHS = 264, CALIBRATION_MONTHS = 240, VALIDATION_MONTHS = 24, DUPLICATE_DATES = 0,
MISSING_MONTHS = 0, MISSING_VALUES = 0. Re-run on 2026-08-15 against canonical commit 419f1ca;
output unchanged (`git diff` empty). No missing observations exist in the canonical dataset;
this status must not be described otherwise absent a new reproducible audit that disagrees.

## Next gate

Original computational code/configuration has been confirmed unavailable by the collaborator
(Amaury de Souza). Exact reproduction of the manuscript's numerical results is therefore not
possible. All modeling-related rows (fractional/integer reproduction onward) proceed only under
INDEPENDENT_REIMPLEMENTATION, governed by `docs/REIMPLEMENTATION_PROTOCOL.md`, and are blocked
until the outstanding methodological assumptions in `docs/ASSUMPTIONS_REGISTER.md` are resolved
(status PENDING_METHOD_SELECTION or UNKNOWN) via independent, documented, and auditable
methodological choices — never by reverse-engineering the manuscript's reported values.

## Base-model implementation stage (2026-08-15)

See `BASE_MODEL_REIMPLEMENTATION_REPORT.md` for the full account. The base-model codebase
(`src/tb_seit/`), canonical data split, leakage-safe population exogenous series, fixed
demographic constants, the Diethelm-Ford-Freed fractional solver, the flow-based observation
model, and the numerical convergence check were implemented and tested first
(`tests/test_seit_model.py`, `tests/test_optimization_contract.py`), while calibration was
blocked on an undefined seed contract (`OPTIMIZATION_CONTRACT_INCOMPLETE`).

## Base-model evidence pipeline execution (2026-08-15, continuation)

The seed contract was frozen (`docs/METHOD_DECISION_LOG.md` D024: `PRIMARY_SEED=20260815`,
`DIAGNOSTIC_SEEDS=[20260816..20260819]`) before any DE result existed under it, resolving the
blocker. The full pipeline was then executed: 5-seed x 2-model calibration, primary-seed
integer comparator (independently re-estimated, never reusing fractional parameters), strict
open-loop 2021-2022 validation, alpha-bound sensitivity ([0.70,1.00] vs. primary [0.50,1.00]),
multi-seed identifiability diagnostics, and the fractional-memory kill-condition audit. All 48
tests pass (`tests/test_seed_contract.py` added). Overall verdict:
`BASE_MODEL_REIMPLEMENTATION_VALID_WITH_LIMITATIONS` -- valid, reproducible pipeline; material
limitation is weak individual identifiability of beta/gamma/d (see table above and
`BASE_MODEL_REIMPLEMENTATION_REPORT.md` Sec 12-13). No AIC, R0, stability, sensitivity-index, or
optimal-control work was attempted, per scope; R0/stability work, when it begins, must carry the
identifiability caveat forward rather than treat the primary-seed beta/gamma point estimates as
precise.

## Practical-identifiability audit (2026-08-15, continuation)

See `IDENTIFIABILITY_AUDIT_REPORT.md` for the full account. Focused audit distinguishing
parameter, predictive, and R0-functional identifiability, using the existing 5-seed multiseed
ensemble plus a new profile-objective analysis (28 additional calibration-only re-optimizations,
grid documented in `scripts/profile_objective.py` before execution). Findings: parameter
identifiability = WEAK (beta/gamma/d flat over wide ranges); predictive identifiability = ROBUST
(mean monthly prediction CV 0.19% calibration / 0.58% validation across the 5 solutions); R0
diagnostic functional identifiability = ROBUST (CV 0.65% across seeds; stays within a ~3% band
even where beta/gamma/d range 6x-210x under a 1% RMSE-degradation allowance); alpha
identifiability = ROBUST (sharply peaked profile, CV 0.08%). Verdict:
`IDENTIFIABILITY_AUDIT_SUPPORTS_DERIVED_R0` -- a formal R0/stability derivation may proceed, but
must report R0 as a range over near-equivalent solutions (not a single point estimate) and must
not individually cite beta/gamma/d as precise rates.

## R0 / stability continuation (2026-08-15) -- STOPPED, not completed

See `R0_STABILITY_ANALYSIS_NOTE.md`. Completed: the R0 near-equivalent solution envelope over
the full 33-solution pool (median 1.1735, IQR [1.1662,1.1816], explicitly not a confidence
interval); ACF/Ljung-Box residual diagnostics (all four residual series show significant
autocorrelation, p<0.001); an independent next-generation-matrix re-derivation of R0 from the
model's own Jacobian, proving the R0=1 threshold is alpha-independent for alpha in (0,1].
**Not completed at that point**: a genuine dimensional-consistency question was found (mu is a
true month^-1 constant while sigma/gamma/d carry no alpha-dependent rescaling despite alpha!=1,
and R0's formula sums them) and the task halted with `FRACTIONAL_R0_PARAMETERIZATION_CONFLICT`
per explicit instruction, rather than resolving it silently. `docs/METHOD_DECISION_LOG.md` D027
has the full account.

## Dimensional consistency audit and conflict resolution (2026-08-15, continuation)

See `docs/FRACTIONAL_DIMENSIONAL_CONSISTENCY.md` and `docs/METHOD_DECISION_LOG.md` D028.
`FRACTIONAL_R0_PARAMETERIZATION_CONFLICT` is **RESOLVED**: an explicit common reference-time
scaling (`tau0=1 month`, applied uniformly to the whole vector field) resolves the dimensional
mismatch exactly for any alpha in (0,1], leaves every existing trajectory numerically unchanged
(difference = 0.0 exactly; no recalibration performed or required), and leaves R0 and the
Matignon stability classification exactly invariant (proved algebraically and confirmed
numerically for non-trivial scaling factors). D028 also corrects a factual error in the prior
version of `R0_STABILITY_ANALYSIS_NOTE.md`: the full 33-solution `FULL_PROFILE_DIAGNOSTIC_POOL`
contains 2 solutions with R0<1 (poor-fit profile probes) and must never be described as
uniformly R0>1; only the `NEAR_EQUIVALENT_ADMISSIBLE_SET` (delta calibration RMSE<=1%, n=25) has
R0>1 in all 25 solutions. Formal stability result over that admissible set (each solution's own
fitted alpha, commensurate Matignon criterion): 0 stable, 25 unstable, 0 ambiguous.

## Rolling-origin forecasting evaluation (2026-08-15, continuation)

See `FORECASTING_EVALUATION_REPORT.md` and `docs/METHOD_DECISION_LOG.md` D029. 13-origin
expanding-window rolling evaluation (h=1..12, 780 leakage-audited forecasts) against 3
baselines (persistence, seasonal_naive_12, SARIMA frozen order per
`docs/SARIMA_BASELINE_CONTRACT.md`). Fractional model beats the integer comparator at every
horizon; underperforms persistence and SARIMA at every horizon; beats seasonal_naive_12 only for
h=1-7 of 12. Verdict: `FRACTIONAL_ADVANTAGE_ONLY_VS_INTEGER`. Dimensional consistency, R0,
stability, and identifiability findings were not reopened.

## Canonical evidence freeze (2026-08-15, continuation)

See `results_canonical/EVIDENCE_FREEZE_REPORT.md`, `results_canonical/RESULT_SET_FREEZE.md`, and
`docs/METHOD_DECISION_LOG.md` D030. RESULT_SET_STATUS = `FROZEN_WITH_DOCUMENTED_LIMITATIONS`.
Evidence-packaging only, no new experiments. Canonical tables/figures/claim-support audit
(`results_canonical/07_claim_support/claim_support_table.csv`, 11 claims) built deterministically
from already-frozen artifacts, cross-checked with no conflicts. Reopening restricted per
`results_canonical/RESULT_SET_FREEZE.md`'s reopening policy. Next stage: evidence-first
manuscript architecture from this frozen result set.
