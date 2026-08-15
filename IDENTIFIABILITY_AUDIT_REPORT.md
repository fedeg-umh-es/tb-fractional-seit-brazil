# Identifiability Audit Report

Scope: a focused practical-identifiability audit of the calibrated fractional SEIT TB model
(status: `BASE_MODEL_REIMPLEMENTATION_VALID_WITH_LIMITATIONS`). No model design, bounds, seeds,
solver, observation model, or train/validation split was changed. No optimal control. No
manuscript edits. **No single R0 point estimate is presented as an epidemiologically identified
result in this report** — all R0 values below are the R0 **diagnostic functional**,
`(beta*sigma) / ((sigma+mu)*(gamma+mu+d))`, evaluated at various calibration solutions purely to
assess its stability relative to its component parameters. It is not a manuscript R0 estimate.

## 1. Executive verdict

**IDENTIFIABILITY_AUDIT_SUPPORTS_DERIVED_R0**

Three distinct notions of identifiability were assessed and must not be collapsed into one
statement:

- **Parameter identifiability** (do beta, gamma, d individually have a well-defined value?):
  **WEAK**. Widely different combinations (beta ranging ~6x, gamma ~6x, d >100x within a 1%
  calibration-RMSE band) fit essentially equally well.
- **Predictive identifiability** (do the 5 very-different parameter vectors produce the same
  observable trajectory?): **ROBUST**. Mean monthly coefficient of variation across the 5
  multiseed solutions' predictions is 0.19% in calibration and 0.58% in validation.
- **R0 functional identifiability** (is the specific combination `beta*sigma/[(sigma+mu)(gamma+mu+d)]`
  more stable than its components?): **ROBUST**. R0 diagnostic CV across multiseed solutions is
  0.65% (vs. 58-82% for beta/gamma/d individually); under a systematic profile-objective
  analysis, R0 stays within roughly 1.15-1.19 across a 2%-RMSE-degradation band while beta,
  gamma, and d range over 6x-200x within that same band.
- **Alpha identifiability** (negative control/comparison): **ROBUST**. Sharply peaked profile
  objective, CV 0.08% across seeds, not boundary-stuck, robust to bound restriction.

Given R0 is materially more stable than its individual components, by two independent lines of
evidence (multiseed ensemble and systematic profile-objective bands), there is sufficient basis
to proceed to a formal R0/stability derivation **provided it explicitly reports R0 as a range or
distribution over near-equivalent solutions, not a single point estimate, and never individually
cites beta or gamma as precise transmission/removal rates.**

## 2. Existing multiseed evidence

Starting point (unchanged, none discarded), `outputs/calibration/fractional_multiseed.csv`,
extended with the R0 diagnostic functional and full-span open-loop predictions in
`outputs/identifiability/multiseed_functionals.csv`:

| seed | beta | sigma | gamma | d | alpha | calib. RMSE | R0_diagnostic | val. RMSE |
|---|---|---|---|---|---|---|---|---|
| 20260815 (primary) | 0.07616 | 0.01002 | 0.05681 | 0.000310 | 0.96401 | 605.049 | 1.17562 | 1117.96 |
| 20260816 | 0.41305 | 0.01012 | 0.28185 | 0.036521 | 0.96355 | 610.388 | 1.16330 | 1167.56 |
| 20260817 | 0.08519 | 0.01015 | 0.05414 | 0.009352 | 0.96198 | 606.273 | 1.18669 | 1065.32 |
| 20260818 | 0.27806 | 0.01014 | 0.17386 | 0.038580 | 0.96224 | 609.571 | 1.17177 | 1130.23 |
| 20260819 | 0.38557 | 0.01004 | 0.28478 | 0.009994 | 0.96235 | 609.874 | 1.17160 | 1123.26 |

Calibration RMSE spread: 605.05-610.39 (CV 0.35%). Validation RMSE spread: 1065.32-1167.56 (also
tight, CV ~3%). beta/gamma/d spread widely; alpha and R0_diagnostic do not.

## 3. Parameter stability

`outputs/audits/parameter_robustness.csv` (unchanged from the base-model stage; reproduced here
for context): beta CV 58.0%, gamma CV 59.9%, d CV 82.2%, vs. sigma CV 0.52% and alpha CV 0.08%.
Section 5 (profile-objective) confirms this is not a seed-sampling artifact: it reflects genuine
flatness of the calibration-RMSE surface along the beta/gamma/d directions.

## 4. Prediction stability

`outputs/identifiability/prediction_dispersion.csv`: for each of the 264 months, mean/std/min/max
across the 5 fractional multiseed solutions' predicted monthly flow.

| window | mean monthly CV across 5 solutions |
|---|---|
| calibration (2001-01..2020-12) | 0.19% |
| validation (2021-01..2022-12) | 0.58% |

Despite beta ranging 5.4x and gamma 5.3x across these same 5 solutions, the **observable
prediction** they produce is nearly identical month by month, in both calibration and (slightly
less tightly) validation. This directly answers the Phase 2 question: yes, very different
beta/gamma/d vectors produce essentially the same observable trajectory.

## 5. Profile-objective analysis

Grid policy (`scripts/profile_objective.py`, documented before execution): for each profiled
parameter, 7 deterministic points -- the canonical primary-seed value plus 3 points toward each
bound at relative offsets {10%, 30%, 60%} of the distance to that bound (denser near canonical,
sparser toward the bounds, never touching a bound exactly). At each point the parameter is fixed
and the remaining 4 are re-optimized via the same DE policy, same seed (20260815), calibration
data only (`CALIBRATION_MONTHS=240`; validation never enters the objective --
`tests/test_identifiability.py::test_profile_objective_uses_calibration_months_only` and
`test_profile_objective_grid_never_touches_bounds_exactly` confirm this structurally).

`outputs/identifiability/profile_objective.csv` (28 rows = 4 parameters x 7 points):

| parameter | pattern |
|---|---|
| beta | RMSE nearly flat (604.7-610.3, delta<5.3) for fixed beta in roughly [0.07, 0.35]; rises sharply outside that plateau (delta=+2075 at beta=0.036; delta=+429 at beta=0.630). |
| gamma | RMSE nearly flat (605.1-609.7, delta<4.7) across the entire tested range [0.053, 0.203] -- no sharp rise observed within the tested envelope. |
| d | RMSE nearly flat (605.5-610.4, delta<5.4) across the entire tested range [0.00018, 0.0301] -- nearly two orders of magnitude with negligible fit cost. |
| alpha (negative control) | RMSE rises steeply and monotonically away from the canonical value on both sides: delta=+767 at alpha=0.686, +207 at alpha=0.825, +70 at alpha=0.918, and +69/+17 even at the nearby grid points either side of canonical -- a narrow, well-defined minimum, qualitatively unlike beta/gamma/d. |

This is the clearest single piece of evidence in this audit: alpha's profile is sharply peaked;
beta/gamma/d's are flat over wide ranges. The same DE machinery, same seed, same data produces
qualitatively different curvature depending on which parameter is profiled -- this is not an
optimizer artifact.

## 6. Parameter trade-offs

`outputs/figures/identifiability/{beta_vs_gamma,beta_vs_d,gamma_vs_d,beta_vs_R0_diagnostic,gamma_vs_R0_diagnostic}.png`,
pooling all 5 multiseed + 28 profile solutions (33 points total; machine-readable values in
`outputs/identifiability/{multiseed_functionals,profile_objective}.csv`, not only the plots).
Visually and numerically: beta and gamma co-vary (both range together across the flat region,
consistent with a compensating trade-off along the force-of-infection / removal-rate direction);
d varies comparatively independently over a much larger relative range at fixed fit quality.
Both beta-vs-R0 and gamma-vs-R0 scatter far more tightly than beta-vs-gamma itself -- visually
reinforcing Section 7. No causal relationship is inferred from these plots; they are descriptive.

## 7. R0 functional stability

`outputs/identifiability/R0_multiseed_diagnostic.csv` (5-seed ensemble, continuous statistics,
no threshold applied):

| n | mean | median | std | CV | min | max | range | relative range |
|---|---|---|---|---|---|---|---|---|
| 5 | 1.17380 | 1.17177 | 0.00760 | 0.647% | 1.16330 | 1.18669 | 0.02338 | 1.99% |

`outputs/identifiability/near_equivalent_solution_bands.csv` (pooled 33-solution profile+multiseed
evidence, descriptive bands, fixed in advance, not chosen after inspecting values):

| band (RMSE over canonical) | n solutions | beta range | gamma range | d range | R0_diagnostic range |
|---|---|---|---|---|---|
| <=0.1% | 6 | [0.0695, 0.0768] (1.10x) | [0.0515, 0.0568] (1.10x) | [0.00025, 0.00388] (15.4x) | [1.1756, 1.1892] (1.2%) |
| <=0.5% | 12 | [0.0695, 0.1323] (1.90x) | [0.0515, 0.0999] (1.94x) | [0.00025, 0.0334] (132x) | [1.1684, 1.1892] (1.8%) |
| <=1.0% | 25 | [0.0695, 0.4130] (5.94x) | [0.0515, 0.2949] (5.72x) | [0.00018, 0.0386] (210x) | [1.1542, 1.1892] (3.0%) |
| <=2.0% | 25 | (same as 1.0% band -- no additional solutions fell in this wider band) | | | |

Even allowing calibration RMSE to degrade by a full percentage point over the canonical value,
beta and gamma range by roughly 6x and d by over 200x, while R0_diagnostic stays within a ~3%
band around 1.17. **This is not merely "5 optimizer seeds agreeing"** (the explicit pitfall the
task warns against) -- it is confirmed by a much larger, systematically constructed
profile-objective pool spanning deliberately displaced parameter values. Conversely, this
finding is not treated as automatic proof of identifiability either: R0's stability here is
relative to the calibration-RMSE surface of *this* dataset and model, not externally validated
against an independent epidemiological ground truth (out of scope for this audit).

## 8. Alpha stability

Multiseed: 0.9620-0.9640 (CV 0.08%). Profile-objective (Section 5): sharply peaked, delta_rmse
rises to the hundreds within ~0.05-0.28 units of displacement in either direction. Carried
forward from the base-model stage: robust to bound restriction ([0.70,1.00] gives alpha=0.9623,
essentially unchanged from the [0.50,1.00] primary result of 0.9640) and never sticks at either
bound. Alpha is the best-identified of the five estimated quantities, by a wide margin.

## 9. Validation residual-sign audit

`outputs/audits/validation_residual_signs.csv` (convention: `residual = predicted - observed`,
confirmed by exact recomputation against the stored predictions, 0 mismatches for both models):

| model | n | positive | negative | zero |
|---|---|---|---|---|
| fractional | 24 | 4 | 20 | 0 |
| integer | 24 | 0 | 24 | 0 |

Confirms the suspected pattern exactly: the integer comparator underpredicts in **every single**
one of the 24 validation months (hence `MAE == |bias| == 1588.649` exactly, only possible when
every residual shares the same sign). The fractional model also underpredicts on balance (20/24
months) but with 4 months of overprediction, consistent with its smaller `|bias| < MAE`
(851.150 < 953.230). This is reported as a verified fact about the existing fit, not a new
interpretation of the model.

## 10. Interpretation limits

- This audit assesses identifiability **relative to this calibration dataset, model structure,
  and DE configuration** -- it is a practical/numerical identifiability study, not a formal
  structural-identifiability proof (which would require symbolic/algebraic analysis of the ODE
  system, not attempted here).
- "R0 diagnostic functional" stability (Section 7) is evidence that a formal R0 derivation is
  *statistically* well-founded on this evidence base; it says nothing about whether R0≈1.17 is
  epidemiologically accurate for Brazilian TB -- that requires external validation, out of scope.
- The profile-objective grid (Section 5) was built once and executed without inspecting
  intermediate results; it deliberately does not reach the extreme edges of the bounds (max
  offset 60% of the distance to a bound), so this audit cannot rule out different behavior in
  the unexplored outer 40% of each parameter's range.
- Alpha<1 is, again, **not** interpreted as proof of epidemiological memory anywhere in this
  report -- Section 8 only characterizes the numerical stability of the alpha estimate itself.

## 11. Decision gate

**IDENTIFIABILITY_AUDIT_SUPPORTS_DERIVED_R0**

Per the task's own definition: "R0 appears materially more stable than its individual component
parameters, with sufficient evidence to proceed to formal R0/stability analysis." Sections 4, 7
document exactly this across two independent lines of evidence (multiseed ensemble; systematic
profile-objective bands). This verdict is compatible with, and does not override, the WEAK
classification for raw parameter identifiability (Section 3/5) -- the two findings are precisely
why "supports derived R0" (a specific functional combination) is the correct verdict rather than
a blanket statement about the model's parameters.

## 12. Next permitted step

**Proceed to formal R0/stability analysis** (the next item explicitly deferred since
`docs/MODEL_CONTRACT.md` Section 13 / `BASE_MODEL_REIMPLEMENTATION_REPORT.md` Section 16), with
two carried-forward constraints established by this audit:

1. Report R0 as a range/distribution over near-equivalent solutions (e.g. the ~1.15-1.19 band
   from Section 7), not a single point estimate from the primary seed alone.
2. Do not individually cite beta, gamma, or d as precise, epidemiologically meaningful
   transmission/removal rates in that analysis -- Section 3/5 established they are not
   individually identifiable from this data under this model structure. Any stability analysis
   requiring the explicit Jacobian (`docs/ASSUMPTIONS_REGISTER.md` A36) should be framed in
   terms of R0 and alpha (both well-identified here) rather than raw beta/gamma/d values.

Optimal control, AIC, and the historical ~48% claim remain out of scope, unchanged from prior
stages.
