# Model Contract — Fractional SEIT (Independent Reimplementation)

Status: SPECIFICATION. No code written, no experiments run, no parameters optimized. This
document closes the minimal methodological contract needed to *later* implement and calibrate
the fractional SEIT model and its integer comparator defensibly. It resolves a bounded subset of
`docs/ASSUMPTIONS_REGISTER.md` (A01–A16, A18–A32); AIC (A33–A34), final stability/sensitivity
reporting (A36–A37 usage), and all optimal-control items (A38–A45, including the ~48% claim)
remain explicitly deferred (Section 13).

No external literature search tool was used to produce this document. Where an external fact is
invoked, it is labeled `HECHO VERIFICADO` (general, well-established domain knowledge — e.g.
WHO/IBGE-level figures, published numerical-methods results, software-documented defaults),
`INFERENCIA` (a conclusion drawn from the manuscript/data structure itself), or `RECOMENDACIÓN`
(a methodological choice made for defensibility, not derived from a specific external source).
No manuscript numerical result was used as a target.

---

## 1. EXECUTIVE VERDICT

**MODEL_CONTRACT_READY_WITH_REDUCED_PARAMETERIZATION**

The full naive parameterization implied by a literal reading of the manuscript (5 kinetic/order
parameters + 4 initial conditions + Λ + μ, fit against a single national monthly series) is not
defensibly identifiable. A reduced, externally-anchored parameterization (Sections 3–5) brings
the free-parameter count down to the 5 quantities the data can plausibly inform (β, σ, γ, d,
α), with everything else fixed, closed analytically, or supplied exogenously from the data
itself. Under that reduction the contract is implementable.

## 2. CRITICAL ISSUE

The manuscript's implicit observation equation — "the observed monthly number of tuberculosis
cases was associated with the infected compartment I(t)" — equates a **flow** (SINAN monthly
case *notifications*, i.e. new diagnoses per month) with a **stock** (I(t), the number of
individuals currently infectious in the compartmental system). These are not the same quantity
and are not generally proportional to each other over time. This is not a cosmetic wording issue:
it changes what the RMSE loss is actually measuring, and it interacts with the model's borderline
identifiability (Section 11) — an incorrect observation equation gives the optimizer extra
freedom to compensate via β/σ/γ/α trade-offs, which can manufacture an apparent "memory effect"
(α < 1) that is really a mis-specification artifact rather than a genuine epidemiological signal.
Section 6 (Observation Model) fixes this by mapping cases to the E→I **flow**, not to the I(t)
stock. This is the single highest-priority correction in this contract.

## 3. RECOMMENDED MODEL CONTRACT

| Decision | Recommended choice | Scientific justification | Evidence status | Sensitivity required |
|---|---|---|---|---|
| A01 — I(t) vs. observed cases | Do **not** equate casos(t) with I(t). Introduce a flow/accumulator variable driven by σE(t) (Section 6). | SINAN notification counts are new-case flow, not standing prevalence; equating them to a stock compartment is a category error in a compartmental model. | INFERENCIA (from data/model structure) | YES |
| A02 — N or N(t) | N(t) = observed `populacao` column (exogenous, data-driven forcing). Not required to equal S+E+I+T; treat S(t)≈N(t)−E(t)−I(t)−T(t) with S dominating (Brazil population ≫ monthly case counts). | N(t) is directly observed monthly in the dataset; TB prevalence is a small perturbation on national population, so exact closed-population bookkeeping adds identifiability burden without epidemiological payoff. | INFERENCIA | NO |
| A03 — Lambda | Fix via demographic closure: Λ = μ·N̄ (μ from A04, N̄ = mean observed population over calibration window). Not estimated. | Since N(t) is supplied exogenously, Λ's role is reduced to a slow demographic-turnover term; letting it float adds a free parameter with almost no leverage on I(t) dynamics at this population scale. | RECOMENDACIÓN | NO |
| A04 — mu | Fix externally: μ = 1/(life expectancy in months), using Brazil life expectancy ≈ 75 years over the study period → μ ≈ 1/(75×12) ≈ 0.0011/month. Not estimated. | All-cause background mortality is a demographic fact largely unrelated to TB incidence dynamics; incidence data carries essentially no information to identify it, so estimating it from casos(t) would be spurious. | HECHO VERIFICADO (order of magnitude; exact figure should be confirmed against an IBGE life-table if a more precise value is later required) | NO |
| A05 — S0 | S0 = N(t0) − E0 − I0 − T0 (closure identity), effectively ≈ N(t0). | Follows analytically once E0, I0, T0 are fixed/derived (below) and N(t0) is observed. | INFERENCIA | NO |
| A06 — E0 | Quasi-steady-state proxy: E0 = flow(t0)/σ, recomputed inside the objective for every candidate σ (not a free parameter). | Standard "warm start" for compartmental models fit mid-epidemic to an already-endemic series: assumes the exposed pool is near local equilibrium with the observed early incidence flow. | RECOMENDACIÓN | YES |
| A07 — I0 | Quasi-steady-state proxy: I0 = σE0/(γ+μ+d), recomputed for every candidate (σ,γ,d) (not a free parameter). | Same warm-start logic as E0; ties I0 analytically to parameters already being estimated instead of adding a new free dimension. | RECOMENDACIÓN | YES |
| A08 — T0 | Fix T0 = 0. | T does not appear in dS/dt, dE/dt, or dI/dt (Section 6 verifies this from the stated equations) — it is a decoupled sink compartment, so its initial value has zero effect on the fitted trajectory or the loss. | HECHO VERIFICADO (from the manuscript's own equations) | NO |
| A09 — time unit | t measured in months; k = 0..239 ↔ 2001-01..2020-12 for calibration, k = 240..263 ↔ 2021-01..2022-12 for validation. | Matches data cadence; makes the numerical step size (Section 7) an explicit sub-multiple of 1 month. | INFERENCIA | NO |
| A10 — beta | Estimate via DE. Units: month⁻¹ (per-capita transmission coefficient in a standard S·I/N mass-action force of infection). | Standard SEIR/SEIT convention; not fixable externally — this is the core epidemiological unknown the study exists to estimate. | HECHO VERIFICADO (convention) / parameter itself is estimated | YES |
| A11 — sigma | Estimate via DE. Units: month⁻¹ (effective latent→active progression rate for a single aggregate Exposed compartment). | TB latency is biologically bimodal (fast progression within ~1–2 years post-infection vs. slow reactivation over decades); a single-compartment SEIT necessarily lumps this into one effective rate — a known structural simplification, not a defect introduced by this contract. | HECHO VERIFICADO (TB natural history is bimodal, general knowledge) + RECOMENDACIÓN (accept the simplification, flag it) | YES |
| A12 — gamma | Estimate via DE. Units: month⁻¹ (I→T transition rate: time to diagnosis+treatment initiation, not necessarily full cure). WHO standard TB treatment course (~6 months) is a plausible central anchor, not a fixed value. | Anchoring context: standard DOTS treatment duration is a well-known figure; used only as a plausibility check on the fitted value, not as a constraint. | HECHO VERIFICADO (6-month course, general) / parameter itself is estimated | YES |
| A13 — d | Estimate via DE. Units: month⁻¹ (excess TB-attributable mortality). | No external value fixes this at national-aggregate resolution without a dedicated literature/registry lookup (deferred, see A26). | RECOMENDACIÓN | YES |
| A14 — Caputo solver | Diethelm–Ford–Freed fractional Adams–Bashforth–Moulton predictor-corrector (PECE) scheme. | Standard, published, widely re-implemented method for Caputo FDEs (Diethelm, Ford & Freed 2002; consistent with the manuscript's own cited reference, Diethelm 2010). Reduces to a standard explicit/implicit Adams scheme behavior as α→1, which keeps the fractional model and the α=1 comparator on the *same code path* — required for A27 to be a fair comparison. | HECHO VERIFICADO (method exists and is standard) | NO (method choice itself; see A16 for step-size sensitivity) |
| A15 — time step | Start at h = 1 month; formally test h = 1, 1/2, 1/4 month via the convergence check in A16 before freezing. | Must not be chosen for fit quality; must be chosen for numerical convergence. | RECOMENDACIÓN | YES (this *is* the sensitivity check) |
| A16 — convergence rule | Run the solver at h and h/2 (and h/4) with one **fixed, arbitrary** parameter vector (bounds midpoint, not any fitted value); require max relative difference in the resulting I(t)-flow trajectory below a pre-declared threshold (e.g. 1%) before freezing h for all calibration runs. | Prevents "solver chosen because it fits better" — ties h to numerical accuracy only, evaluated once, before any optimization touches real data. | RECOMENDACIÓN | This check IS the sensitivity requirement for A14–A16 |
| A18 — DE strategy | `best1bin` | SciPy `differential_evolution` default; general-purpose, most widely used/audited DE variant. | HECHO VERIFICADO (software default) | NO |
| A19 — DE popsize | 15 × 5 parameters = 75 | SciPy default scaling rule. | HECHO VERIFICADO (software default) | NO |
| A20 — DE mutation | (0.5, 1.0) dithered | SciPy default. | HECHO VERIFICADO (software default) | NO |
| A21 — DE recombination (CR) | 0.7 | SciPy default. | HECHO VERIFICADO (software default) | NO |
| A22 — DE max iterations | 1000, with early stop on `tol` | Conservative, standard cap; not tuned. | RECOMENDACIÓN | NO |
| A23 — DE stopping tolerance | SciPy default (`tol=0.01`, relative population-spread convergence) | Standard, documented, reproducible criterion. | HECHO VERIFICADO (software default) | NO |
| A24 — random seed | Fix one literal seed for the reported run (document the exact integer in `METHOD_DECISION_LOG.md`); additionally run 4 more seeds as a robustness check (Section 12), never to select the "best" one, only to report spread. | Reproducibility requires a documented literal seed; multi-seed spread is the identifiability diagnostic, not a tuning device. | RECOMENDACIÓN | YES (multi-seed spread is a required sensitivity analysis) |
| A25 — loss (RMSE) | RMSE between observed monthly cases and the model-implied monthly **flow** (Section 6), not raw I(t). Same functional form as the manuscript's stated RMSE, reinterpreted to match the corrected A01 observation model. | Keeps the manuscript's stated loss *type*; corrects what the second series in that loss actually represents, per Section 2/6. | INFERENCIA (deviation from literal manuscript wording, logged) | NO |
| A26 — parameter bounds | β [0.01, 1.00] and σ [0.01, 0.50]: retain manuscript bounds (plausible order of magnitude). γ, d: retain manuscript bounds provisionally but flag for literature check (below). α: **widen to [0.5, 1.0]**, not [0.70, 1.00]. | See detailed reasoning in Section "Parameter bounds rationale" below. | Mixed: β/σ = RECOMENDACIÓN (retain); α = RECOMENDACIÓN (change, justified); γ/d = RECOMENDACIÓN (retain, pending external check) | YES |
| A27 — integer comparator | **Re-estimate β, σ, γ, d independently** under the identical DE protocol with α fixed at 1. Do not reuse the fractional-optimal parameter vector. | Reusing fractional-optimal parameters under forced α=1 dynamics is not "the best the integer model can do" — it is a strawman that mechanically favors the fractional model. A fair nested-model comparison requires each model to be independently optimal under matched protocol, bounds, and loss; only out-of-sample performance (Section 10) should then be trusted to say whether fractional order adds genuine skill. | RECOMENDACIÓN (methodological principle, not manuscript-derived) | NO (this is the design itself) |
| A28 — validation-window initial state | The state at 2021-01 is whatever the continuously-integrated, calibration-fitted trajectory produces at that time step — **not** reset using any 2021-2022 observation. | Any reinitialization using validation-period data leaks information into what must remain a genuine out-of-sample test. | RECOMENDACIÓN | NO |
| A29 — forecast/evaluation protocol | Single continuous **open-loop** simulation from 2001-01 through 2022-12 using only calibration-fitted parameters; the last 24 months of that one trajectory are the validation predictions. No recursive/rolling re-initialization with observed data. | Strictest, most defensible out-of-sample design; matches the explicit constraint that no 2021-2022 information may influence the model. | RECOMENDACIÓN | NO |
| A30 — RMSE (validation) | Same construction as A25, computed only over the 24 validation months, using parameters frozen at calibration. | Consistency with the calibration loss definition. | INFERENCIA | NO |
| A31 — MAE | MAE = (1/n)·Σ\|casos_obs(t) − flow_model(t)\|, standard textbook definition, same n and window conventions as RMSE. | Manuscript names MAE but never defines it; this adopts the uncontested standard definition. | RECOMENDACIÓN | NO |
| A32 — bias | bias = (1/n)·Σ(flow_model(t) − casos_obs(t)); report separately for calibration and validation windows. | Not present in the manuscript at all; added as a low-cost diagnostic for systematic over/under-prediction. Purely diagnostic — does not affect the loss or optimization. | RECOMENDACIÓN (new addition, clearly flagged as such) | NO |

### Parameter bounds rationale (A26, detail)

- **β [0.01, 1.00]/month**, **σ [0.01, 0.50]/month**: wide but epidemiologically non-absurd
  ranges for effective, aggregate, compartment-level rates; retained without change.
  `RECOMENDACIÓN`.
- **γ [0.01, 0.50]/month**: implies a mean I→T time between ~2 and ~100 months. The lower bound
  (γ=0.01 → ~100 months, ~8 years) is hard to reconcile with an active DOTS-based treatment
  system; the manuscript gives no citation for this range. `PENDING`: a literature check on
  Brazilian TB diagnostic-and-treatment-initiation delay (SINAN/DATASUS-based studies) is needed
  before tightening this bound with confidence. Retained provisionally; flagged for external
  verification, not silently narrowed.
- **d [0.0001, 0.05]/month**: plausible order of magnitude given documented excess mortality
  associated with active, and especially untreated or HIV-coinfected, TB, but no Brazil-specific
  figure was checked. `PENDING`: literature check on Brazilian TB case-fatality (SINAN/DATASUS
  linkage studies, e.g. Ministry of Health TB surveillance reports) needed before treating this
  range as more than provisional.
- **α [0.70, 1.00] → recommended [0.50, 1.00]**: the manuscript's own citations (Caputo 1967;
  Diethelm 2010) only require 0 < α ≤ 1 for the Caputo derivative to be mathematically valid and
  physically interpretable; there is no epidemiological argument in the manuscript for excluding
  α ∈ [0.5, 0.70). Constraining the search to [0.70, 1.00] a priori assumes "at least moderate
  memory" before the data have said anything about it, which biases the design toward finding a
  fractional-memory effect. Widening the bound lets the data determine how close to integer-order
  (α=1) the fitted process actually is. `RECOMENDACIÓN`, logged as an explicit, justified
  departure from the manuscript.

## 4. PARAMETERS

| parameter | estimated/fixed | units | source/justification | bounds | notes |
|---|---|---|---|---|---|
| β | estimated | month⁻¹ | DE, core unknown | [0.01, 1.00] | — |
| σ | estimated | month⁻¹ | DE, core unknown | [0.01, 0.50] | lumps fast+slow TB progression into one effective rate (structural simplification, flagged) |
| γ | estimated | month⁻¹ | DE, core unknown | [0.01, 0.50] | lower bound PENDING external check (Section "Parameter bounds rationale") |
| d | estimated | month⁻¹ | DE, core unknown | [0.0001, 0.05] | PENDING external check |
| α | estimated | dimensionless (0 < α ≤ 1) | DE, core unknown | [0.50, 1.00] (recommended widening) | integer comparator fixes α ≡ 1 exactly, not estimated in that branch |
| Λ | fixed | individuals·month⁻¹ | Λ = μ·N̄ (demographic closure) | n/a | not estimated |
| μ | fixed | month⁻¹ | ≈ 1/(75×12) from Brazil life expectancy (order-of-magnitude) | n/a | not estimated; refine later if precision matters |
| N(t) | exogenous | individuals | `populacao` column, direct monthly observation | n/a | not estimated, not closed against S+E+I+T |

## 5. INITIAL CONDITIONS

At t0 = 2001-01 (first calibration month):

- `S0 = N(t0) - E0 - I0 - T0` (closure identity; effectively ≈ N(t0) since E0, I0, T0 ≪ N(t0)).
- `E0 = flow(t0) / σ` — recomputed from the flow at t0 (Section 6) for whatever σ the optimizer
  is currently evaluating. Not a free parameter.
- `I0 = σ·E0 / (γ + μ + d)` — recomputed analogously for the currently evaluated (σ, γ, d). Not
  a free parameter.
- `T0 = 0` — fixed; mathematically irrelevant to S/E/I dynamics or the loss (T is decoupled;
  Section 6).

No initial condition is a free DE dimension. This keeps the estimated parameter set at exactly
5: {β, σ, γ, d, α} for the fractional model, {β, σ, γ, d} for the integer comparator.

## 6. OBSERVATION MODEL

**This section is the core correction of this review.**

The manuscript's stated system does not include an explicit observed-case equation beyond the
prose claim "observed cases = I(t)". Given that SINAN case counts are monthly new-notification
flows, the defensible observation model instead ties observed cases to the **E→I transition
flow**, using an auxiliary Caputo accumulator sharing the model's fractional order:

```
cD^alpha_t C(t) = sigma * E(t)          (auxiliary cumulative-incidence accumulator, C(0) = 0)

flow_model(t_k) = C(t_k) - C(t_{k-1})   (model-implied new cases in calendar month k)
```

The loss (A25) and all reported RMSE/MAE/bias metrics (A25, A30–A32) compare `casos_obs(t_k)`
against `flow_model(t_k)`, never against the raw `I(t)` stock.

Verification that T(t) is decoupled (supports A08): the manuscript's own stated equations
(Section 2.3) show `dT/dt = γI(t) − μT(t)` with T appearing on the right-hand side of no other
compartment's equation — T does not feed back into S, E, or I, so its trajectory (and initial
condition) cannot influence the fitted dynamics or the loss. It may be computed for bookkeeping
but is not part of the active calibration state vector.

This is a documented deviation from the manuscript's literal wording; it is logged as such
(Section 14 / decision log) rather than silently substituted.

## 7. NUMERICAL CONTRACT

- **Solver**: Diethelm–Ford–Freed fractional Adams–Bashforth–Moulton predictor-corrector (PECE)
  scheme for the Caputo system, applied identically to the fractional model and (with α=1) the
  integer comparator.
- **Time step**: start at h=1 month; freeze the final h only after the step-halving convergence
  check below passes. Candidate set to test: h ∈ {1, 1/2, 1/4} month.
- **Convergence check**: at one fixed, arbitrary parameter vector (bounds midpoint — never a
  fitted value), compare the resulting monthly `flow_model(t)` series at h vs. h/2 vs. h/4;
  require the maximum relative difference to fall below a pre-declared threshold (recommended:
  1%) before any calibration run uses that h. This check must be performed once, before DE is
  ever run against real data, and its outcome (chosen h, observed convergence numbers) must be
  logged in `METHOD_DECISION_LOG.md`.

## 8. OPTIMIZATION CONTRACT

Differential Evolution (SciPy `differential_evolution`, or an equivalent implementation
reproducing the same defaults):

- Strategy: `best1bin`
- Population size: `popsize=15` (→ 75 candidate vectors for 5 free parameters)
- Mutation: `(0.5, 1.0)` dithered
- Recombination: `CR=0.7`
- Max iterations: `maxiter=1000`
- Stopping tolerance: `tol=0.01` (SciPy default relative convergence)
- Bounds: as in Section 3/4 (β, σ, γ, d, α; α fixed=1, i.e. excluded from the free-parameter
  vector, for the integer comparator)
- Seed: one literal, documented seed for the reported "primary" run; 4 additional literal seeds
  run only for the robustness diagnostic in Section 12 — never used to cherry-pick a result.
- Loss: RMSE as defined in Section 6/A25, evaluated on 2001-01 to 2020-12 only.

None of the above hyperparameters may be adjusted based on 2021-2022 (validation) performance,
per the project's canonical constraint.

## 9. INTEGER COMPARATOR CONTRACT

Same SEIT structure, same solver, same numerical step, same observation model (Section 6), same
loss, same DE protocol and bounds (minus α), with `alpha` fixed at exactly `1.0` and **excluded**
from the DE free-parameter vector. β, σ, γ, d are independently re-estimated under this
constrained system — the fractional-optimal parameter vector is never reused. This isolates the
marginal effect of the fractional order as cleanly as the shared-code-path solver (Section 7)
allows.

## 10. VALIDATION CONTRACT

1. Fit both models (fractional and integer comparator) using only 2001-01 to 2020-12 data, per
   Sections 6–9.
2. Using the resulting fitted parameters (frozen — no further adjustment), integrate each model
   continuously, open-loop, from 2001-01 through 2022-12 in a single run.
3. Extract the last 24 monthly `flow_model(t)` values (2021-01 to 2022-12) as that model's
   validation predictions.
4. Compute RMSE, MAE, and bias (Sections 3/A30–A32) between those predictions and the observed
   2021-01 to 2022-12 `casos` values.
5. No parameter, bound, solver choice, or hyperparameter may be revisited based on the outcome
   of step 4. If validation performance is poor, that is a result to report (see Section 15 —
   Kill Condition), not a cue to re-tune.

## 11. IDENTIFIABILITY RISK

**MODERATE.**

With the reductions in Sections 3–5 (μ, Λ fixed/closed; N(t) exogenous; E0, I0 analytically
derived; T0/T decoupled and excluded), the free-parameter count is reduced from a naive ~11
unknowns to exactly 5 (β, σ, γ, d, α) for the fractional model. This is a substantially more
identifiable design than a literal reading of the manuscript would imply, and is consistent with
what a single 240-point monthly aggregate series can plausibly inform.

It is not `LOW` risk, because:
- β and σ can trade off against each other (faster transmission + slower progression can mimic
  slower transmission + faster progression in aggregate incidence) — a generic, well-known
  identifiability issue for compartmental models fit to a single incidence series.
- α (fractional order) can partially trade off against γ and d, since reducing α changes the
  effective memory/decay behavior of E and I in ways that can statistically mimic adjusting the
  removal rates — this is a specific, known critique of fractional-order epidemic models that
  claim improved fit: added flexibility from a non-integer order will frequently improve
  in-sample fit over a nested integer model *by construction*, independent of whether any real
  "memory effect" exists. `INFERENCIA` (general modeling principle), not from a specific citation.

It is not `HIGH`/`UNACCEPTABLE` because the reduced parameterization, combined with a genuinely
out-of-sample validation window (Section 10) and the multi-seed robustness check (Section 12),
gives a real chance to detect and report non-identifiability rather than paper over it with an
overconfident point estimate.

## 12. SENSITIVITY ANALYSES REQUIRED

Minimal set, all pre-registered here (not to be expanded or narrowed after seeing results):

1. **Step-size convergence** (A16): h vs h/2 vs h/4 at a fixed arbitrary parameter vector —
   required before any calibration run.
2. **Multi-seed DE robustness** (A24): re-run calibration with 5 literal seeds; report the range
   and coefficient of variation of the resulting (β, σ, γ, d, α) estimates and of the calibration
   RMSE. Large spread in parameters despite similar RMSE is the diagnostic signature of
   non-identifiability (Section 11) and must be reported as such, not averaged away.
3. **α-bound sensitivity**: re-run calibration with the manuscript's original α bound [0.70,1.00]
   alongside the recommended [0.50,1.00], to make explicit how much the manuscript's a priori
   restriction affects the fitted α and downstream comparator conclusions.
4. **Bounds check for γ, d**: report whether the DE-optimal γ, d land near a bound edge (a sign
   the bound itself, not the data, is determining the estimate) — informs whether the "PENDING"
   literature check in Section 3 is urgent.

## 13. DEFERRED ITEMS

Explicitly out of scope for this contract:

- AIC (A33–A34): requires this contract's observation model to be frozen first (done here) plus
  an explicit likelihood/error-model choice and an agreed parameter count per model — not
  resolved now.
- Final stability classification (beyond the manuscript-stated Matignon criterion already logged
  in `docs/ASSUMPTIONS_REGISTER.md`, A36) — requires fitted parameters, which do not yet exist.
- R0 sensitivity indices (A37 usage) — same dependency.
- Optimal control in full (A38–A45), including control-variable placement for u1/u3, bounds,
  objective weights, horizon, and numerical method.
- The historical ~48% cumulative-case/peak-reduction claim: remains `REFERENCE_ONLY_NOT_EVIDENCE`
  and must be discarded unless independently regenerated under a fully specified optimal-control
  contract (not attempted here).
- Manuscript rewriting and LaTeX conversion: blocked per `REPRODUCIBILITY_STATUS.md`.

## 14. IMPLEMENTATION HANDOFF

Compact specification for implementation (no further scientific decisions required for the base
model + comparator + validation pipeline described here):

```
MODEL: Caputo-fractional SEIT, compartments S,E,I,T, plus auxiliary flow accumulator C.
  dS/dt^alpha = Lambda - beta*S*I/N(t) - mu*S
  dE/dt^alpha = beta*S*I/N(t) - (sigma+mu)*E
  dI/dt^alpha = sigma*E - (gamma+mu+d)*I
  dT/dt^alpha = gamma*I - mu*T                      [decoupled; compute for bookkeeping only]
  dC/dt^alpha = sigma*E                             [auxiliary; C(0)=0]
  flow_model(t_k) = C(t_k) - C(t_{k-1})

FIXED:
  mu    = 1 / (75*12)                months^-1
  Lambda = mu * mean(N(t) over 2001-01..2020-12)
  N(t)  = data column `populacao`, monthly, exogenous

INITIAL CONDITIONS (t0 = 2001-01), recomputed per candidate (sigma, gamma, d):
  E0 = flow(t0) / sigma
  I0 = sigma*E0 / (gamma + mu + d)
  T0 = 0
  S0 = N(t0) - E0 - I0 - T0

FREE PARAMETERS (fractional model): beta, sigma, gamma, d, alpha
  bounds: beta [0.01,1.00], sigma [0.01,0.50], gamma [0.01,0.50], d [0.0001,0.05], alpha [0.50,1.00]

FREE PARAMETERS (integer comparator): beta, sigma, gamma, d   (alpha fixed = 1.0 exactly)
  bounds: same as above minus alpha

SOLVER: Diethelm-Ford-Freed fractional Adams-Bashforth-Moulton predictor-corrector (PECE),
  same implementation/code path for alpha<1 and alpha=1.
  Step size h: freeze via step-halving convergence check (Sec. 7) before calibration; candidates {1, 1/2, 1/4} month.

LOSS: RMSE(casos_obs(t), flow_model(t)) over 2001-01..2020-12 only.

OPTIMIZER: scipy.optimize.differential_evolution
  strategy=best1bin, popsize=15, mutation=(0.5,1.0), recombination=0.7,
  maxiter=1000, tol=0.01, bounds as above, seed=<one literal documented integer>.
  Additional literal seeds {4 more} run only for the robustness diagnostic (Sec. 12), never to select a result.

VALIDATION: single continuous open-loop integration 2001-01..2022-12 using calibration-frozen
  parameters; last 24 months (2021-01..2022-12) compared against observed casos via RMSE, MAE, bias
  (Sec. 3, A30-A32). No re-initialization, no recursive updating, no re-tuning on this window.

OUT OF SCOPE for this implementation pass: AIC, final stability/sensitivity reporting, optimal
  control, the ~48% claim, manuscript/LaTeX edits.
```

## 15. KILL CONDITION

Abandon the fractional-order framing as the headline scientific claim (not necessarily the whole
SEIT reimplementation) if, after implementing Sections 6–10 exactly as specified:

- the multi-seed robustness check (Section 12.2) shows β, σ, γ, α estimates varying widely across
  seeds while calibration RMSE stays statistically indistinguishable (the "sloppy model"
  signature of non-identifiability), **and/or**
- the honestly-refit integer-order comparator (Section 9) achieves out-of-sample validation RMSE
  (Section 10) that is not meaningfully better for the fractional model — i.e., α's extra
  flexibility buys negligible or no genuine predictive skill on 2021-2022.

If either condition holds, the correct action is to report that the fractional order does not
carry demonstrable, identifiable scientific content in this dataset — not to select the
best-looking seed, narrow the α bound post hoc, or otherwise engineer a result. This is precisely
the failure mode the project's "no reproducir números antiguos" constraint exists to prevent.
