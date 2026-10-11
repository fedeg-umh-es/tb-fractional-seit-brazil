# R0 / Stability Analysis Note

Status: **RESOLVED.** `FRACTIONAL_R0_PARAMETERIZATION_CONFLICT` (raised in the original version
of this note) is resolved by `docs/FRACTIONAL_DIMENSIONAL_CONSISTENCY.md`, which audits an
explicit common reference-time scaling (`tau0 = 1 month`) and shows it (a) resolves the
dimensional mismatch exactly, for every mechanism, for any `alpha in (0,1]`; (b) leaves every
existing trajectory numerically unchanged (max absolute/relative/RMSE difference = 0.0 exactly,
tested); and (c) leaves R0 and the Matignon stability classification exactly invariant (proved
algebraically and confirmed numerically for non-trivial scaling factors, not just the trivial
`c=1` case relevant here). See `docs/FRACTIONAL_DIMENSIONAL_CONSISTENCY.md` for the full audit
and Steps 5-7 below for the resulting formal stability result.

**CORRECTION (superseding an earlier error in this note):** an earlier version of this note's
closing paragraph stated the qualitative finding using looser language that could be read as
"R0 stayed above 1 throughout the full 33-solution pool." **That reading is false.** The full
`FULL_PROFILE_DIAGNOSTIC_POOL` (n=33) contains **2 solutions with R0<1** (deliberately poor-fit
profile probes, `R0_min=0.6393`) — see Step 6 below. Only the pre-registered
`NEAR_EQUIVALENT_ADMISSIBLE_SET` (delta calibration RMSE `<=1%`, n=25, the same tolerance already
established descriptively in `IDENTIFIABILITY_AUDIT_REPORT.md` Sec 5) has R0>1 in every one of
its 25 solutions. These two sets are now named and reported separately everywhere in this note
and must never be conflated.

No single-point R0 is reported anywhere in this note. Beta, gamma, and d are never named
individually as precise rates outside of their role as inputs to the R0 functional or as raw,
explicitly-labeled calibration artifacts.

---

## Step 1 — R0 formula confirmation

Implemented at `src/tb_seit/r0.py::r0_diagnostic`:

```
R0_diagnostic(beta, sigma, gamma, d, mu) = (beta * sigma) / ((sigma + mu) * (gamma + mu + d))
```

This is the exact formula the manuscript states (Sec 2.5, extracted verbatim during the earlier
manuscript inventory: `R0 = beta*sigma / [(sigma+mu)(gamma+mu+d)]`;
`docs/ASSUMPTIONS_REGISTER.md` A35, `KNOWN_FROM_MANUSCRIPT`). It is also the formula already
used throughout the identifiability audit (`IDENTIFIABILITY_AUDIT_REPORT.md`), unchanged here.

## Step 2 / Part A — R0 near-equivalent solution envelope (NOT a confidence interval)

Per the user's explicit correction: the ~33-solution profile+multiseed pool is **not a
bootstrap sample** and must not be labeled or treated as a frequentist CI. Computed over the
full, unfiltered pool (5 multiseed + 28 profile solutions = 33; `scripts/
r0_envelope_and_residual_diagnostics.py::part_a_envelope`,
`outputs/identifiability/R0_near_equivalent_solution_envelope.csv`):

```
R0_NEAR_EQUIVALENT_SOLUTION_ENVELOPE
  n_solutions        33
  median             1.1735
  mean               1.1692
  min                0.6393
  max                1.6149
  IQR                [1.1662, 1.1816]  (width 0.0153, ~1.3% of the median)
  full_range         [0.6393, 1.6149]  (width 0.9756, ~83% of the mean)
```

**Relationship between R0 variation and calibration-RMSE degradation** (Pearson correlation
between %-RMSE-degradation-over-canonical and |R0 - pool mean|): **r = 0.838**. Breaking the
pool down by RMSE-degradation band (descriptive, not significance thresholds) makes this
concrete:

```
band (RMSE over canonical)   n    R0 range            rel. width
<=0.1%                        6   [1.1756, 1.1892]     1.15%
<=0.5%                       12   [1.1684, 1.1892]     1.76%
<=1.0%                       25   [1.1542, 1.1892]     2.99%
<=2.0%                       25   [1.1542, 1.1892]     2.99%
<=5.0%                       26   [1.1228, 1.1892]     5.67%
full pool (up to +343%)      33   [0.6393, 1.6149]     83.44%
```

Reading: the full min-max range is dominated entirely by a handful of profile-objective probe
points deliberately constructed far from the canonical fit (e.g. the most extreme beta grid
point, RMSE degraded by +343% over canonical) to expose profile curvature
(`IDENTIFIABILITY_AUDIT_REPORT.md` Sec 5) — those are not plausible alternative model fits. The
median/IQR describe the bulk of the pool and are far tighter. R0's spread grows monotonically
and strongly (r=0.84) with how far a solution's fit quality has degraded, which is exactly the
behavior expected of a well-identified functional evaluated over an ensemble of solutions that
range from "as good as the canonical fit" to "deliberately poor."

## Step 3 / Part B — Residual dependence diagnostic (model-diagnostic only)

`scripts/r0_envelope_and_residual_diagnostics.py::part_b_residual_diagnostics` ->
`outputs/audits/residual_autocorrelation_diagnostics.csv`. ACF and Ljung-Box implemented
directly (numpy + `scipy.stats.chi2`, standard textbook formulas) rather than via `statsmodels`
(not installed; adding it was declined). Validated against synthetic white-noise (correctly
non-significant) and a strong AR(1) series (correctly flagged significant) in
`tests/test_r0_stability.py`.

```
RESIDUAL_AUTOCORRELATION
  model        split         n    lags  acf(1)  acf(2)  acf(3)  Ljung-Box Q   p-value      sig(0.05)
  fractional   calibration   240  20    0.195   0.308   0.258   235.78        8.3e-39      YES
  integer      calibration   240  20    0.484   0.558   0.520   1060.79       4.2e-212     YES
  fractional   validation    24    6    0.602   0.480   0.362   24.62         4.0e-4       YES
  integer      validation    24    6    0.628   0.509   0.393   27.77         1.0e-4       YES
```

**Confirmed as expected**: significant positive autocorrelation in every one of the four
residual series, including calibration (n=240, where the Ljung-Box test has ample power — this
is not merely a validation small-sample artifact). The validation segment (n=24) result is
still reported with an explicit reliability caveat, per instruction: with only 6 lags tested
against 24 points, the test has limited power, so while significance was found here (making
the low-power caveat moot in this direction — a significant result under low power is still
informative), a *non*-significant result on this segment would not have been strong evidence of
independence.

**Per instruction, this finding does NOT determine an R0 uncertainty interval by itself.** A
formal, time-dependence-aware sampling method (e.g. moving-block bootstrap over refits) would be
required for that and is explicitly out of scope for this task, deferred to a future, separate
experiment.

## Step 4 / Part C — Fractional next-generation-matrix derivation and Matignon stability

### Infected subsystem and disease-free equilibrium

The implemented system (`src/tb_seit/model.py::seit_rhs`) is:

```
C D_t^alpha S = Lambda - beta*S*I/N - mu*S
C D_t^alpha E = beta*S*I/N - (sigma+mu)*E
C D_t^alpha I = sigma*E - (gamma+mu+d)*I
C D_t^alpha T = gamma*I - mu*T
```

(The auxiliary accumulator `C(t)` in the code, `dC/dt^alpha = sigma*E`, is a bookkeeping variable
for the observation model, not part of the epidemiological dynamics, and is excluded here, as is
`T`, which is dynamically decoupled -- confirmed algebraically below.)

At the disease-free equilibrium (DFE), `E*=I*=T*=0`, `S*=N*=Lambda/mu` (consistent with the
demographic closure `Lambda = mu * mean(N_train)` already fixed in
`docs/EXTERNAL_PARAMETER_CONTRACT.md`, giving `S*/N*=1`).

### Jacobian at the DFE

Linearizing the full (S,E,I) system at the DFE (T decouples: its own row/column contributes
only the eigenvalue `-mu<0`, always stable, confirmed by inspection of `∂(dT/dt)/∂{S,E,I}=0`):

```
J(DFE) = [ -mu,              0,                -beta ]
         [  0,        -(sigma+mu),               beta ]
         [  0,             sigma,        -(gamma+mu+d) ]
```

Column S is `[-mu, 0, 0]^T`, so `J` is block lower-triangular: eigenvalues are `{-mu}` union
`eig(J_EI)`, where

```
J_EI = [ -(sigma+mu),        beta       ]
       [    sigma,      -(gamma+mu+d)   ]
```

This confirms (E,I) is exactly the correct "infected subsystem" for the next-generation-matrix
(NGM) construction — verified from the model's own Jacobian structure, not assumed.

### F and V matrices (van den Driessche & Watmough construction)

New-infection matrix (only E receives new infections; the sigma*E term in dI/dt is a
*transition*, not a new infection):

```
F = [ 0   beta ]      V = [ sigma+mu        0        ]
    [ 0    0   ]          [  -sigma    gamma+mu+d     ]
```

`det(V) = (sigma+mu)(gamma+mu+d) > 0` always. `V^{-1} = 1/det(V) * [[gamma+mu+d, 0], [sigma,
sigma+mu]]`. `F V^{-1}` has the form `[[a, b], [0, 0]]` with `a = beta*sigma/det(V)`; its
eigenvalues are `{0, a}`, so the spectral radius (= R0 by definition) is:

```
R0 = beta*sigma / [(sigma+mu)(gamma+mu+d)]
```

**Exactly matching the implemented formula** (Step 1) — independently re-derived here from the
model's own equations, not merely copied from the manuscript.

### Is the threshold alpha-independent? (proved, not assumed)

`det(J_EI) = (sigma+mu)(gamma+mu+d) - beta*sigma = det(V)*(1 - R0)` (algebraic identity;
`tests/test_r0_stability.py::test_r0_matches_next_generation_matrix_determinant_identity`
confirms this numerically for several parameter draws). `trace(J_EI) = -(sigma+mu) -
(gamma+mu+d) < 0` always.

- **If R0 > 1**: `det(J_EI) < 0` &rArr; the two eigenvalues of `J_EI` are real with opposite
  sign &rArr; one eigenvalue is real and **positive**, i.e. `arg(lambda) = 0`. Matignon's
  criterion for the Caputo system requires `|arg(lambda)| > alpha*pi/2` for stability; since
  `0 > alpha*pi/2` is false for any `alpha > 0`, the DFE is **unstable for every alpha in
  (0, 1]** whenever R0 > 1 by the classical (alpha-independent) formula. No alpha-dependence
  in this direction.
- **If R0 < 1**: `det(J_EI) > 0` and `trace(J_EI) < 0` &rArr; both eigenvalues have negative
  real part (standard 2x2 Routh-Hurwitz), i.e. `arg(lambda) in (pi/2, pi]` (principal branch)
  &rArr; `|arg(lambda)| > pi/2`. Since the fitted/contracted `alpha` domain in this project is
  always `<= 1` (`docs/MODEL_CONTRACT.md`: primary `[0.50,1.00]`, sensitivity `[0.70,1.00]`),
  `alpha*pi/2 <= pi/2 < |arg(lambda)|`, so Matignon's condition holds **for every alpha in
  (0, 1]** whenever R0 < 1 by the classical formula. Again no alpha-dependence.

**Conclusion (rigorous, not assumed): for this model, with alpha restricted to (0, 1] (true for
every alpha value used anywhere in this project), the classical, alpha-independent R0 formula is
exactly the fractional (Caputo/Matignon) local-stability threshold too — R0=1 is the threshold
in both the integer and fractional sense, with no alpha-dependent correction to the threshold
itself.** This is a real mathematical result for this specific model (derived above), not a
borrowed analogy, and it is exactly the logic the manuscript's own Section 2.7 already uses
(R0<1 stable / R0>1 unstable, alongside a separately-stated Matignon criterion) — this
derivation independently verifies that usage is legitimate for this model structure.

### Parameter units under the Caputo formulation — RESOLVED

The original version of this note flagged a genuine dimensional question: `beta, sigma, gamma,
d` are DE-estimated with no `alpha`-dependent rescaling despite `alpha != 1`, while `mu` is
fixed externally as a genuine `month^-1` constant, and the R0 formula sums them directly
(`sigma+mu`, `gamma+mu+d`).

`docs/FRACTIONAL_DIMENSIONAL_CONSISTENCY.md` resolves this by making the implicit convention
explicit rather than choosing a new one: introduce a reference timescale `tau0 = 1 month` and
write `C D_t^alpha X = tau0^(1-alpha) * F(X;theta)`, where `F` is built entirely from ordinary,
uniformly-`month^-1` rate constants (`beta, sigma, gamma, d, mu` — none individually rescaled).
This is shown (Phase 1 of that document) to resolve the dimensional mismatch **exactly**, for
every one of the six mechanisms (recruitment, transmission, progression, treatment, natural
mortality, TB mortality), for any `alpha in (0,1]` — so `sigma+mu` and `gamma+mu+d` are, under
this formulation, always sums of two genuinely same-dimensioned `month^-1` quantities; the
mixing concern is resolved, not merely bounded.

**Numerically** (Phase 2 of that document), since this project's entire time axis is already in
months, `tau0=1 month` makes the conversion factor `tau0^(1-alpha)` equal to exactly `1.0` for
any `alpha` — so every existing trajectory (fractional and integer, calibration and validation,
primary-seed parameters) is **numerically identical, not merely close**, under the corrected
formulation: max absolute difference, max relative difference, and RMSE difference are all
exactly `0.0` (`outputs/audits/dimensional_scaling_numerical_equivalence.csv`,
`tests/test_dimensional_audit.py::test_numerical_equivalence_report_shows_zero_difference`). No
recalibration is required or was performed.

**R0 and the Matignon classification** (Phases 4-5 of that document) are proved algebraically to
be exactly invariant under ANY common positive scaling factor `c` applied to the whole vector
field (not just the trivial `c=1` relevant here): `F_alpha = c*F`, `V_alpha = c*V` implies
`F_alpha * V_alpha^{-1} = F*V^{-1}` exactly (the scalar cancels through the matrix inverse), so
R0 is unchanged; and `J_alpha = c*J` implies `arg(c*lambda) = arg(lambda)` for `c>0` (scaling a
complex number by a positive real does not change its argument), so the Matignon angular
classification is unchanged. Both confirmed numerically in `tests/test_dimensional_audit.py` for
several non-trivial `c` values (0.3, 2.5, 3.0, 7.7, 10.0), not just `c=1`.

**Conclusion: `FRACTIONAL_R0_PARAMETERIZATION_CONFLICT` is resolved. The R0 formula, its already-
reported values (Step 2/Part A), and the alpha-independence proof above all stand exactly as
previously computed — nothing numeric changes. What changed is that the dimensional legitimacy
of using this formula for `alpha != 1` is now proved explicitly, rather than left as an open
question.**

## Step 6 — R0 evidence sets (corrected, mandatory separation)

`scripts/r0_evidence_set_and_stability.py` -> `outputs/identifiability/R0_evidence_set_classification.csv`.
Two sets, never to be conflated:

```
R0_EVIDENCE_SETS
  FULL_PROFILE_DIAGNOSTIC_POOL         (all 33 profile+multiseed solutions, unfiltered)
    n=33   R0 in [0.6393, 1.6149]   median=1.1735   IQR=[1.1662,1.1816]
    n(R0<1) = 2      n(R0>1) = 31

  NEAR_EQUIVALENT_ADMISSIBLE_SET        (delta calibration RMSE <= 1%, pre-registered
                                          tolerance, IDENTIFIABILITY_AUDIT_REPORT.md Sec 5)
    n=25   R0 in [1.1542, 1.1892]   median=1.1735   IQR=[1.1682,1.1770]
    n(R0<1) = 0      n(R0>1) = 25
```

Across the predefined near-equivalent solution set (delta calibration RMSE <=1%), the R0
functional ranged from 1.1542 to 1.1892 (all 25 solutions R0>1); this is a
**practical-identifiability envelope / near-equivalent solution range, not a confidence
interval**. The full diagnostic pool additionally contains 2 solutions (of 33) with R0<1 — both
are deliberately poor-fit profile probes (RMSE degraded far beyond the admissible tolerance) and
are reported for completeness (Step 7), not as evidence bearing on the primary conclusion.

## Step 7 — Formal stability result

`scripts/r0_evidence_set_and_stability.py` -> `outputs/audits/dfe_stability_by_evidence_set.csv`.
For every solution, using its own fitted `alpha` (not a fixed value), the commensurate
Caputo/Matignon criterion `|arg(lambda_i)| > alpha*pi/2` is applied to `J_EI` at the DFE:

```
DFE_STABILITY -- NEAR_EQUIVALENT_ADMISSIBLE_SET (n=25, the primary evidence set)
  n_stable = 0    n_unstable = 25    n_ambiguous = 0
  angular margin (|arg(lambda)| - alpha*pi/2): min=-1.5199 rad, max=-1.5093 rad
  (all margins negative and of comparable magnitude -- every admissible solution is unstable,
   with an angular margin around -1.51 rad, i.e. roughly -alpha*pi/2, since the binding
   eigenvalue is real and positive, arg=0, in every one of these R0>1 solutions)

DFE_STABILITY -- FULL_PROFILE_DIAGNOSTIC_POOL (n=33, PROFILE_DIAGNOSTIC_ONLY)
  n_stable = 2    n_unstable = 31    n_ambiguous = 0
  angular margin: min=-1.5482 rad, max=+1.5710 rad
  (the 2 stable points are exactly the 2 R0<1 deliberately-poor-fit profile probes from Step 6;
   PROFILE_DIAGNOSTIC_ONLY -- these do not inform the primary mechanistic conclusion)
```

**Formal result (near-equivalent admissible set, the primary evidence set): the disease-free
equilibrium is locally asymptotically unstable under the commensurate Caputo/Matignon criterion
in all 25 of 25 near-equivalent solutions**, using each solution's own fitted alpha. This
mirrors the R0>1 classification exactly (as proved in Step 4/5: for this model, with alpha in
(0,1], the two criteria are mathematically equivalent, not merely correlated). Zero ambiguous
cases.

## What was completed / not completed

Completed and tested: the reference-time dimensional audit (all 4 phases of
`docs/FRACTIONAL_DIMENSIONAL_CONSISTENCY.md`), the corrected evidence-set separation, and the
formal per-solution stability classification over the near-equivalent admissible set. Per
instruction, still explicitly out of scope: any R0 confidence interval / bootstrap (a future,
separate, time-dependence-aware resampling experiment would be required, not attempted here);
recalibration (not required — the numerical-equivalence check found zero difference); optimal
control; manuscript edits.
