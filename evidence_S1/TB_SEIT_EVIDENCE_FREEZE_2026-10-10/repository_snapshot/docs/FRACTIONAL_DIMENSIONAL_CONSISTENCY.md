# Fractional SEIT Dimensional Consistency Audit

Resolves `FRACTIONAL_R0_PARAMETERIZATION_CONFLICT` raised in `R0_STABILITY_ANALYSIS_NOTE.md`.
Audits an explicit common reference-time scaling `tau0 = 1 month`. Does not recalibrate, does
not change bounds/seeds/observations/forecasting model, does not touch optimal control or the
manuscript.

## Phase 1 — Dimensional derivation

### Units of the Caputo derivative

For `0 < alpha <= 1`, the Caputo derivative is
`C D_t^alpha X(t) = 1/Gamma(1-alpha) * integral_0^t (t-s)^{-alpha} X'(s) ds`.
Dimensionally: `X'(s)` has units `[X]/[time]`; `(t-s)^{-alpha}` has units `[time]^{-alpha}`; `ds`
contributes `[time]`. Net: `[X]/[time] * [time]^{-alpha} * [time] = [X] * [time]^{-alpha}`
(Gamma(1-alpha) is dimensionless). So:

```
[C D_t^alpha X] = [X] / [time]^alpha
```

for every state `X in {S, E, I, T}` (and the auxiliary accumulator `C(t)`, which is governed by
the same Caputo operator in the implementation and must be scaled identically for the solver's
uniform-alpha, uniform-h treatment to remain internally consistent -- it is not itself an
epidemiological compartment, but it IS part of the fractional ODE/FDE system actually being
integrated).

### OLD_FORMULATION / DIMENSIONAL_CONFLICT

As implemented prior to this audit (`src/tb_seit/model.py::seit_rhs`, unchanged by this audit --
see Phase 2), the right-hand side is written directly in terms of month^-1 rate constants:

```
C D_t^alpha S = Lambda - beta*S*I/N - mu*S
```

Each RHS term (`Lambda`, `beta*S*I/N`, `mu*S`) has units `[individuals]/[time]^1` (since
`beta`, `mu` are calibrated/fixed as ordinary per-month rates: `mu = 1/(74*12)` per month,
`beta`/`sigma`/`gamma`/`d` searched over month^-1-labeled DE bounds). The left-hand side requires
`[individuals]/[time]^alpha`. **These match only when `alpha = 1`.** For any fitted `alpha != 1`
(true for the fractional model's primary/diagnostic/profile solutions, all `alpha` approx
0.92-0.96), the equation as written is dimensionally inconsistent — this is exactly the conflict
flagged in `R0_STABILITY_ANALYSIS_NOTE.md`.

### REFERENCE_TIME_FORMULATION

Introduce an explicit reference timescale `tau0`, a genuinely dimensional quantity (`[time]`),
set to `tau0 = 1 month`, and write:

```
C D_t^alpha X = tau0^(1-alpha) * F(X; theta)
```

where `F(X; theta)` is the SAME epidemiological vector field as before, built entirely from
ordinary month^-1 rate constants (`beta, sigma, gamma, d, mu` all retain units `month^-1`;
`Lambda` retains units `individuals * month^-1`) -- i.e. `F` itself is unchanged; only an
explicit conversion factor `tau0^(1-alpha)` is introduced, multiplying the ENTIRE vector field
uniformly (not selected terms, not selected parameters):

```
C D_t^alpha S = tau0^(1-alpha) * [ Lambda - beta*S*I/N - mu*S ]
C D_t^alpha E = tau0^(1-alpha) * [ beta*S*I/N - (sigma+mu)*E ]
C D_t^alpha I = tau0^(1-alpha) * [ sigma*E - (gamma+mu+d)*I ]
C D_t^alpha T = tau0^(1-alpha) * [ gamma*I - mu*T ]
C D_t^alpha C = tau0^(1-alpha) * [ sigma*E ]                    (accumulator; Phase 3)
```

`tau0^(1-alpha)` has units `[time]^(1-alpha)`. Each bracketed term has units
`[individuals]/[time]^1` as established above. Multiplying:

```
[individuals]/[time]^1 * [time]^(1-alpha) = [individuals] * [time]^(-1+1-alpha)
                                           = [individuals] * [time]^(-alpha)
                                           = [individuals] / [time]^alpha
```

**This exactly matches the required left-hand-side units, `[X]/[time]^alpha`, for every
compartment, for any `alpha in (0,1]`.** Checked individually for each mechanism (all share the
identical structural argument, since each is a product/sum of one or two month^-1 rates times a
population-valued state or Lambda):

| mechanism | term | units before scaling | units after x tau0^(1-alpha) |
|---|---|---|---|
| recruitment | `Lambda` | individuals/month | individuals/month^alpha |
| transmission | `beta*S*I/N` | (month^-1)*(individuals)*(individuals)/(individuals) = individuals/month | individuals/month^alpha |
| progression (E->I) | `sigma*E` | individuals/month | individuals/month^alpha |
| treatment/removal (I->T) | `gamma*I` | individuals/month | individuals/month^alpha |
| natural mortality | `mu*S`, `mu*E`, `mu*T` (via the (sigma+mu), (gamma+mu+d), mu*T terms) | individuals/month | individuals/month^alpha |
| TB-induced mortality | `d*I` (via (gamma+mu+d)) | individuals/month | individuals/month^alpha |

**DIMENSIONAL_STATUS: RESOLVED.** All six mechanisms individually check out; the scaling
resolves the conflict exactly, not approximately, for every `alpha in (0,1]`.

Not `REFERENCE_TIME_SCALING_INVALID` -- the formulation resolves the dimensions exactly.

## Note on why this differs from (and repairs) the earlier concern

`R0_STABILITY_ANALYSIS_NOTE.md`'s conflict was framed as "maybe `sigma`/`gamma`/`d` are secretly
`month^-alpha` quantities while `mu` is genuinely `month^-1`, so `sigma+mu` mixes dimensions."
The reference-time formulation resolves this by rejecting that framing: under
`REFERENCE_TIME_FORMULATION`, `beta, sigma, gamma, d, mu` are ALL, uniformly and always, genuine
`month^-1` quantities (exactly as they were calibrated, bounded, and interpreted throughout this
entire project) -- no individual parameter is ever fractionally rescaled. The dimensional
conversion for `alpha != 1` is instead confined entirely to the single explicit scalar
`tau0^(1-alpha)`, applied uniformly outside the sums `(sigma+mu)`, `(gamma+mu+d)` -- so those
sums are never dimensionally mixed in the first place. This is a strictly more consistent
bookkeeping than either "rescale some parameters" (rejected) or "ignore the issue" (the
`OLD_FORMULATION`'s implicit, undocumented stance).
