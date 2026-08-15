# R0 / Stability Analysis Note

Status: **PARTIAL — STOPPED at Part C with `FRACTIONAL_R0_PARAMETERIZATION_CONFLICT`.**
Parts A and B (below) are complete, executed, and tested. Part C's algebraic derivation is
complete and verified, but surfaces a genuine, previously-undisclosed-at-this-level of
scrutiny dimensional-consistency question that this note flags rather than resolves — per
this task's own explicit instruction and the reviewer role's "STOP and flag the conflict
rather than resolving it silently."

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

### Parameter units under the Caputo formulation — the conflict

This is where a genuine, unresolved issue surfaces, per the explicit instruction to verify
this and STOP if inconsistent.

For `C D_t^alpha S(t)` to be dimensionally well-posed, the right-hand side must carry units of
`[S]/[time]^alpha`. Written as `Lambda - beta*S*I/N - mu*S` with `beta`, `mu` treated as plain
`[time]^-1` rate constants (the convention this entire project has used throughout — no
`k^{1-alpha}` rescaling is applied anywhere in `src/tb_seit/model.py` or
`src/tb_seit/solver.py`; confirmed by reading the implementation, not assumed), the right-hand
side actually carries units of `[S]/[time]`, not `[S]/[time]^alpha`, whenever `alpha != 1`. This
is a well-known, frequently-unaddressed ambiguity in the applied Caputo-fractional-epidemiology
literature (the manuscript itself gives no unit for beta/sigma/gamma/d anywhere, per
`docs/ASSUMPTIONS_REGISTER.md` A10-A13, `PARTIALLY_SPECIFIED`) — this project's implementation
follows that same, already-disclosed convention, not a new one invented for R0.

**Why this specifically threatens the R0 formula (not just the ODE solver, which was already
accepted with this caveat in prior stages)**: R0 is a *ratio* of products of rate constants, and
is provably invariant under any *uniform* rescaling applied to all of beta, sigma, gamma, d, and
mu together (multiplying every rate by the same constant `c` scales both numerator and
denominator by `c^2`, leaving R0 unchanged) — so if a rigorous `k^{1-alpha}` correction were
applied uniformly, R0's *value* would be unaffected. **The actual problem is `mu`**: `mu` is
fixed *externally* from Brazilian life-expectancy data as a genuine `month^-1` constant
(`docs/EXTERNAL_PARAMETER_CONTRACT.md`, D015) — it is not, and cannot self-consistently be,
subject to whatever implicit `alpha`-dependent rescaling the DE-estimated `sigma`, `gamma` might
carry if a rigorous fractional reparameterization were later applied to them alone. `sigma` and
`mu` are summed directly (`sigma + mu`), and `gamma`, `mu`, `d` are summed directly
(`gamma + mu + d`), inside the R0 formula itself. If `sigma`/`gamma`/`d` are secretly
`month^-alpha` quantities (fitted with `alpha=0.964`, i.e. very close to but not exactly 1) while
`mu` is unambiguously `month^-1`, these additive terms mix two different physical dimensions —
and because `alpha` is close to 1 here, the numerical impact would likely be small, but "likely
small" is not the same as "verified," and this project's own standard (flag disclosed
uncertainty rather than average it away) requires surfacing this rather than asserting it away.

**FRACTIONAL_R0_PARAMETERIZATION_CONFLICT.** This is not resolved in this note. Two
possible resolution paths exist and require an explicit decision (not one this review should
make unilaterally): (a) accept the naive/shared convention used throughout this entire project
and the manuscript, documenting the resulting R0 with this caveat attached; or (b) apply a
uniform `k^{1-alpha}` reparameterization to all rate constants *including* re-deriving `mu` under
that convention (not merely relabeling the already-fitted `sigma`/`gamma`/`d`), and recalibrate
before recomputing R0. Neither path is chosen here.

### What remains true regardless of this conflict

The threshold-alpha-independence proof above (R0=1 is the fractional stability boundary for
alpha in (0,1], regardless of dimensional convention) is a statement about the *algebraic
structure* of the model and holds under either resolution path. Separately: **every R0 value in
the near-equivalent envelope (Step 2/Part A) that falls within any RMSE-degradation band up to
5% is greater than 1** (band minima: 1.176, 1.168, 1.154, 1.154, 1.123 respectively, for the
0.1%-5% bands) — R0 does not approach the threshold of 1 anywhere within the range of solutions
that fit the calibration data reasonably well; only the most extreme, poorly-fitting profile
probe points (RMSE degraded by >100%) produce R0 values near or below 1. Given R0's provable
invariance to *uniform* rescaling (shown above), and given `mu` is small relative to `sigma`/
`gamma` across the entire near-equivalent pool (bounding how much the `mu`-mixing issue could
plausibly move R0), the qualitative conclusion **"the disease-free equilibrium is unstable
(R0>1, persistent transmission) across the entire near-equivalent solution envelope, for every
alpha value used in this project"** is very likely robust to the unresolved dimensional
question — but this is stated as a qualitative, hedged read of the evidence, not as the
formally verified, ready-for-manuscript numeric result the task requested, which remains
blocked on resolving the conflict above.

## What was NOT completed in this task

Per the STOP: no R0 confidence interval or bootstrap was constructed (also explicitly
out-of-scope per the user's Part B instruction); no final numeric R0 range was certified as the
formally verified fractional-consistent threshold; no final stability classification was issued
as a manuscript-ready result. Parts A, B, and the NGM/Matignon algebraic derivation in Part C are
complete, tested, and usable as-is; only the units-conflict resolution and the resulting final
numeric certification are pending a decision.
