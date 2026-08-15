# Assumptions register

This register enumerates every methodological detail an independent reimplementation of the
fractional-order SEIT tuberculosis model must specify, mapped against what the manuscript source
(`manuscript/source/BIOMATEMATICA_UNICAMP.docx`) actually states. It was produced by a read-only
inventory of the manuscript text (including embedded equation objects); the manuscript file
itself was not modified. No external literature search was performed to produce this register.

`original_implementation_status` classifies what the manuscript specifies, not what this project
has decided:
- `KNOWN_FROM_MANUSCRIPT` — the manuscript states this explicitly (a formula, a numeric bound, an
  explicit textual rule).
- `PARTIALLY_SPECIFIED` — the manuscript names or partially describes the item but leaves a
  material detail unstated (e.g., a quantity is named with no units, a mechanism is described for
  one compartment but not another).
- `UNKNOWN` — the manuscript does not address this item at all.

`proposed_decision` is left as `PENDING_METHOD_SELECTION` wherever an actual decision requires
external methodological justification (e.g., choosing a specific Caputo solver, a DE
hyperparameter set, an initial-condition rule) rather than being filled in for completeness. Per
`PROJECT_CANON.md` evidence policy, adopting a manuscript-stated value (e.g., Table 1 bounds)
verbatim is itself a decision that must be independently justified for methodological
defensibility, not simply copied to match the manuscript's reported results — such items are
still marked `PENDING_METHOD_SELECTION` even though the manuscript states a candidate value.

| ID | component | question | manuscript_information | original_implementation_status | decision_required | proposed_decision | justification | sensitivity_required | status |
|----|-----------|----------|-------------------------|----------------------------------|--------------------|--------------------|----------------|------------------------|--------|
| A01 | Observational mapping | What does the observed variable represent in the model? | Sec 2.1: "The observed monthly number of tuberculosis cases was associated with the infected compartment I(t) of the epidemiological model." Does not address stock-vs-flow (prevalence vs. monthly incidence) consistency or underreporting. | PARTIALLY_SPECIFIED | YES | PENDING_METHOD_SELECTION | Direction of mapping is stated, but whether reported monthly cases should be treated as a flow onto I(t) vs. a proxy for the I(t) stock is not addressed and materially affects model semantics. | YES | PENDING_METHOD_SELECTION |
| A02 | Population term | Is N constant or N(t) time-varying? | Equations use N(t) explicitly (Sec 2.3: beta*S(t)*I(t)/N(t)). Dataset has a `populacao` column with monthly values, but the manuscript never states whether N(t) is drawn directly from that column, interpolated from sparser census figures, or held constant. | PARTIALLY_SPECIFIED | YES | PENDING_METHOD_SELECTION | Structural form (N(t)) is given; the data source/construction of N(t) is not. | YES | PENDING_METHOD_SELECTION |
| A03 | Recruitment rate Lambda | What is Lambda (value or construction rule)? | Named only ("Lambda is the recruitment rate," Sec 2.3). No value, formula (e.g., Lambda = mu*N0), or estimation procedure given. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | YES | PENDING_METHOD_SELECTION |
| A04 | Natural mortality mu | What is mu (value or source)? | Named only ("mu is the natural mortality rate," Sec 2.3). No value or source (e.g., Brazilian life-table-derived) given. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | YES | PENDING_METHOD_SELECTION |
| A05 | Initial condition S0 | What is S(0) for calibration? | Not addressed. Sec 2.7 gives the disease-free equilibrium S* = Lambda/mu, which is a stability-analysis construct, not a stated calibration initial condition. | UNKNOWN | YES | PENDING_METHOD_SELECTION | DFE formula is unrelated to the calibration initial-condition question. | YES | PENDING_METHOD_SELECTION |
| A06 | Initial condition E0 | What is E(0) for calibration? | Not addressed anywhere in the text. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | YES | PENDING_METHOD_SELECTION |
| A07 | Initial condition I0 | What is I(0) for calibration? | Not addressed anywhere in the text (not even stated as "the first observed case count"). | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | YES | PENDING_METHOD_SELECTION |
| A08 | Initial condition T0 | What is T(0) for calibration? | Not addressed anywhere in the text. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | YES | PENDING_METHOD_SELECTION |
| A09 | Time unit | What is the unit of t in the differential system? | Not stated explicitly. Data are monthly (Sec 2.1); parameter magnitudes reported in Table 2 (e.g., sigma=0.0335) are consistent with a monthly timescale but this is an inference, not a manuscript statement. | PARTIALLY_SPECIFIED | YES | PENDING_METHOD_SELECTION | Monthly data cadence is stated; explicit declaration that t is measured in months (vs. some other unit with re-scaled rates) is not. | YES | PENDING_METHOD_SELECTION |
| A10 | Units/interpretation of beta | What does beta mean quantitatively? | "beta is the transmission rate" (Sec 2.3); Table 1 gives search bounds [0.01, 1.00]; no unit/timescale stated. | PARTIALLY_SPECIFIED | YES | PENDING_METHOD_SELECTION | Name and search range given; explicit unit convention (per month, per capita per month, etc.) absent. | YES | PENDING_METHOD_SELECTION |
| A11 | Units/interpretation of sigma | What does sigma mean quantitatively? | "sigma is the progression rate from latent to active TB" (Sec 2.3); Table 1 bounds [0.01, 0.50]; no unit stated. | PARTIALLY_SPECIFIED | YES | PENDING_METHOD_SELECTION | Same gap as A10. | YES | PENDING_METHOD_SELECTION |
| A12 | Units/interpretation of gamma | What does gamma mean quantitatively? | "gamma is the recovery rate" (Sec 2.3); Table 1 bounds [0.01, 0.50]; no unit stated. | PARTIALLY_SPECIFIED | YES | PENDING_METHOD_SELECTION | Same gap as A10. | YES | PENDING_METHOD_SELECTION |
| A13 | Units/interpretation of d | What does d mean quantitatively? | "d is the TB-induced mortality rate" (Sec 2.3); Table 1 bounds [0.0001, 0.05]; no unit stated. | PARTIALLY_SPECIFIED | YES | PENDING_METHOD_SELECTION | Same gap as A10. | YES | PENDING_METHOD_SELECTION |
| A14 | Caputo numerical solver | Which numerical scheme solves the Caputo-fractional SEIT system? | Not addressed. No solver (e.g., Adams-Bashforth-Moulton predictor-corrector, Grunwald-Letnikov, `fde12`-type method) is named anywhere in the manuscript. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on; this is a purely external methodological choice. | YES | PENDING_METHOD_SELECTION |
| A15 | Numerical time step | What integration step size is used? | Not addressed. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | YES | PENDING_METHOD_SELECTION |
| A16 | Solver tolerance/convergence | What convergence rule governs the fractional solver? | Not addressed. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | NO | PENDING_METHOD_SELECTION |
| A17 | Observation-to-model comparison mechanic | How is a simulated trajectory compared to observed monthly cases for the loss? | Sec 2.4 RMSE formula explicitly uses Iobs(t) and Imod(t) at matching time points: RMSE = sqrt((1/n) * sum_t (Iobs(t) - Imod(t))^2). No aggregation/smoothing transform is applied. | KNOWN_FROM_MANUSCRIPT | NO | Direct, same-timestep comparison of simulated I(t) against observed monthly `casos`, matching the manuscript's stated RMSE formula. | Explicit equation in Sec 2.4; consistent with A01's stated I(t)-to-cases mapping. | NO | RESOLVED_FROM_MANUSCRIPT |
| A18 | DE strategy variant | Which Differential Evolution variant/strategy (e.g., rand/1/bin, best/1/bin)? | Only "Differential Evolution algorithm" is named, citing Storn & Price (1997), the general method — no specific strategy variant given. | UNKNOWN | YES | PENDING_METHOD_SELECTION | Citation identifies the general algorithm family only. | YES | PENDING_METHOD_SELECTION |
| A19 | DE population size | What population size was used? | Not addressed. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | YES | PENDING_METHOD_SELECTION |
| A20 | DE mutation parameter (F) | What mutation factor was used? | Not addressed. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | YES | PENDING_METHOD_SELECTION |
| A21 | DE recombination parameter (CR) | What crossover/recombination probability was used? | Not addressed. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | YES | PENDING_METHOD_SELECTION |
| A22 | DE maximum iterations | What generation/iteration budget was used? | Not addressed. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | NO | PENDING_METHOD_SELECTION |
| A23 | DE stopping tolerance | What convergence tolerance stops DE? | Not addressed. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | NO | PENDING_METHOD_SELECTION |
| A24 | Random seed | Was a random seed fixed, and what value? | Not addressed; no seed reported anywhere, despite DE being stochastic. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on; this is a reproducibility gap in the original work itself. | NO | PENDING_METHOD_SELECTION |
| A25 | Optimization loss definition | What exact loss function does DE minimize? | Sec 2.4: RMSE = sqrt((1/n) * sum_{t=1}^{n} (Iobs(t) - Imod(t))^2), explicitly given as an equation, minimized jointly over beta, sigma, gamma, d, and alpha. | KNOWN_FROM_MANUSCRIPT | NO | Adopt the stated RMSE loss over the same 5 simultaneously optimized parameters (beta, sigma, gamma, d, alpha) for the fractional model. | Explicit equation present in the manuscript. | NO | RESOLVED_FROM_MANUSCRIPT |
| A26 | Parameter bounds | What are the DE search bounds for each parameter? | Table 1 gives explicit bounds: beta in [0.01, 1.00]; sigma in [0.01, 0.50]; gamma in [0.01, 0.50]; d in [0.0001, 0.05]; alpha in [0.70, 1.00]. | KNOWN_FROM_MANUSCRIPT | YES | PENDING_METHOD_SELECTION | Bounds are stated, but per the evidence policy they must be adopted (or revised) for independent epidemiological defensibility, not merely copied to reproduce the manuscript's numbers; whether to adopt them as-is, and with what independent justification, is an open decision. | YES | PENDING_METHOD_SELECTION |
| A27 | Integer-order comparator contract | How exactly is the "integer-order model" constructed from the fractional model? | Sec 3.6: "The integer-order model was obtained by setting the fractional parameter equal to unity: alpha = 1." Does not state whether beta, sigma, gamma, d are re-estimated by a fresh DE run with alpha fixed at 1, or whether the fractional model's already-optimized parameter values are simply reused with alpha forced to 1. | PARTIALLY_SPECIFIED | YES | PENDING_METHOD_SELECTION | The alpha=1 substitution is explicit; whether the remaining four parameters are independently re-optimized is not. | YES | PENDING_METHOD_SELECTION |
| A28 | Forecast initialization at 2021-01 | How is the model state initialized to begin the validation-period simulation? | Sec 3.7 states only that parameters are "estimated exclusively using the calibration dataset, while the validation period was reserved for independent predictive assessment." No statement of how S/E/I/T at 2021-01 are obtained (continued trajectory from calibration end vs. reinitialized from observed data). | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | YES | PENDING_METHOD_SELECTION |
| A29 | Validation mode (recursive vs. open-loop) | Is validation a single open-loop forward simulation, or a recursive/rolling one-step-ahead forecast? | Not addressed; Sec 3.7 only describes the calibration/validation split, not the forecasting procedure used within the validation window. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | YES | PENDING_METHOD_SELECTION |
| A30 | RMSE definition (reused in validation/comparison) | Does the validation-period and comparator-table RMSE use the same formula as Sec 2.4? | The Sec 2.4 formula is the only RMSE definition given anywhere in the manuscript; Sec 3.6/3.7 report RMSE values without restating the formula. | PARTIALLY_SPECIFIED | YES | PENDING_METHOD_SELECTION | Formula is known from Sec 2.4; its reuse elsewhere is a reasonable but unstated assumption that must be made explicit, not silently inferred. | NO | PENDING_METHOD_SELECTION |
| A31 | MAE definition | What is the exact Mean Absolute Error formula used? | Only named ("Mean Absolute Error (MAE)," Sec 3.6); no formula given anywhere in the text. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | NO | PENDING_METHOD_SELECTION |
| A32 | Bias definition | Is a bias metric defined/used? | Not mentioned anywhere in the manuscript. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | NO | PENDING_METHOD_SELECTION |
| A33 | AIC likelihood/error model | What error/likelihood model underlies the reported AIC? | Only named ("Akaike Information Criterion (AIC)," Sec 3.6); no formula or likelihood assumption (e.g., Gaussian error via RSS) is given. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | NO | PENDING_METHOD_SELECTION |
| A34 | AIC parameter count | How many free parameters (k) are counted for each model's AIC? | Not stated. Ambiguous whether k=5 (beta, sigma, gamma, d, alpha) for the fractional model vs. k=4 for the integer-order comparator, or whether initial conditions/Lambda/mu are also counted. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | NO | PENDING_METHOD_SELECTION |
| A35 | R0 analytical derivation | What is the closed-form expression for R0? | Sec 2.5 gives the formula explicitly: R0 = beta*sigma / [(sigma + mu)(gamma + mu + d)]. Derivation steps (e.g., next-generation matrix) are not shown, only the final expression. | KNOWN_FROM_MANUSCRIPT | NO | Adopt the stated closed-form R0 expression; independently re-derive it from the stated SEIT system (Sec 2.3) as a Level B verification step rather than accept it uncritically. | Explicit formula given; independent re-derivation is standard due diligence, not a new methodological choice. | NO | RESOLVED_FROM_MANUSCRIPT |
| A36 | Fractional stability criterion | What stability condition applies to the fractional-order Jacobian eigenvalues? | Sec 2.7 gives Matignon's (1996) criterion explicitly: local asymptotic stability holds iff \|arg(lambda_i)\| > alpha*pi/2 for all eigenvalues lambda_i of the Jacobian. The DFE (S* = Lambda/mu, 0, 0, 0) and the abstract Jacobian J = dF/dX are given symbolically; the explicit 4x4 Jacobian entries at the DFE are not shown. | PARTIALLY_SPECIFIED | YES | PENDING_METHOD_SELECTION | Stability criterion formula is explicit and citable; the concrete Jacobian matrix must still be independently derived from the stated system. | NO | PENDING_METHOD_SELECTION |
| A37 | Sensitivity-index definition | What is the exact sensitivity-index formula? | Sec 3.5 gives the normalized forward sensitivity index explicitly: Upsilon_p^{R0} = (partial R0 / partial p) * (p / R0). | KNOWN_FROM_MANUSCRIPT | NO | Adopt the stated normalized forward sensitivity index formula for each parameter p in {beta, sigma, gamma, d, mu}. | Explicit equation given. | NO | RESOLVED_FROM_MANUSCRIPT |
| A38 | Optimal-control equations | What are the full controlled-system equations? | Sec 2.6 gives only the controlled I(t) equation: cD^alpha_t I(t) = sigma*E(t) - (1+u2(t))*gamma*I(t) - (mu+d)*I(t). Control variables u1 (intensified diagnosis) and u3 (contact tracing) are named but do not appear in any equation shown in the text; how they enter the S, E, or I dynamics is not specified. | PARTIALLY_SPECIFIED | YES | PENDING_METHOD_SELECTION | Only u2's placement (reducing effective progression to the treated/removed pathway via gamma) is textually specified; u1 and u3's mechanistic effect on the system is a material gap. | YES | PENDING_METHOD_SELECTION |
| A39 | Optimal-control bounds | What are the admissible bounds for u1, u2, u3? | Not stated numerically anywhere in the extracted text (commonly [0,1] in this literature, but that is an external convention, not a manuscript statement). | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | YES | PENDING_METHOD_SELECTION |
| A40 | Optimal-control objective weights | What are the numeric values of A, B, C, D in the objective functional? | Sec 2.6 gives the functional form explicitly: J(u) = integral_0^T [A*I(t) + B*u1(t)^2 + C*u2(t)^2 + D*u3(t)^2] dt, with A described as "the epidemiological burden weight" and B, C, D as intervention costs — but no numeric values for A, B, C, D are given anywhere. | PARTIALLY_SPECIFIED | YES | PENDING_METHOD_SELECTION | Functional form is explicit; weight values are not, and per collaborator instruction must not be back-fit to reproduce the ~48% claim. | YES | PENDING_METHOD_SELECTION |
| A41 | Intervention horizon T | What is the numeric length of the control horizon T? | T appears only symbolically as the upper integration limit in the objective functional (Sec 2.6); no numeric value (e.g., in months) is given anywhere. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | YES | PENDING_METHOD_SELECTION |
| A42 | Optimal-control numerical method | What numerical method solves the optimal-control problem? | Not addressed. No method (e.g., Pontryagin's Maximum Principle with forward-backward sweep, adjoint-equation derivation, discretization scheme) is named anywhere in the manuscript. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | NO | PENDING_METHOD_SELECTION |
| A43 | Cumulative-case reduction definition | How is the "~48% cumulative case reduction" formally computed? | Narrative only (Results Sec 3.4, Discussion, Conclusion): "The combined intervention scenario reduced cumulative tuberculosis cases ... by approximately 48%." No formula (e.g., (AUC_baseline - AUC_controlled)/AUC_baseline over which horizon) or underlying data table is given; the only support is Figures 6-7, which are embedded images not machine-readable from the source text. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on beyond the narrative percentage itself. | YES | PENDING_METHOD_SELECTION |
| A44 | Peak reduction definition | How is the "~48% epidemic peak reduction" formally computed? | Narrative only (same sections as A43): "...and epidemic peak intensity by approximately 48%." No formula (e.g., max(I_baseline) vs. max(I_controlled), over which window) is given. | UNKNOWN | YES | PENDING_METHOD_SELECTION | No manuscript information to build on. | YES | PENDING_METHOD_SELECTION |
| A45 | Criterion for the historical ~48% claim | What overall evidentiary basis supports the reported ~48% figure? | Entirely narrative/figure-based (Sec 3.4, Discussion, Conclusion; Figures 6-8, embedded images). No numeric table, formula, or reproducible procedure is given in the extracted manuscript text. | UNKNOWN | YES | PENDING_METHOD_SELECTION | Per `PROJECT_CANON.md` and collaborator instruction, this value must be discarded unless independently regenerated; no manuscript detail exists to build a reproduction from. | YES | PENDING_METHOD_SELECTION |

## Note on an unrelated manuscript inconsistency

The manuscript's "Data Availability Statement" (end of document) refers to "Scorpionism
incidence data" obtained from SINAN/IBGE, which is inconsistent with the tuberculosis subject of
the rest of the manuscript and appears to be a copy-paste artifact from an unrelated document.
This is recorded here as an observation only; it is not one of A01-A45 and no action is proposed
regarding it, since the task scope for this repository transition is data/model methodology, not
manuscript editing (`manuscript/source/` remains untouched per project rules).

## Summary counts

Recompute from the table above before citing; do not hand-copy without verifying against the
current version of this file. As of this register's creation (2026-08-15):
- Total assumptions: 45 (A01-A45).
- KNOWN_FROM_MANUSCRIPT: A17, A25, A26, A35, A37 (5). Note A26 and A35 still carry a
  `decision_required = YES` because adopting a manuscript-stated value verbatim is itself a
  decision requiring independent justification under the evidence policy.
- PARTIALLY_SPECIFIED: A01, A02, A09, A10, A11, A12, A13, A27, A30, A36, A38, A40 (12).
- UNKNOWN: A03, A04, A05, A06, A07, A08, A14, A15, A16, A18, A19, A20, A21, A22, A23, A24, A28,
  A29, A31, A32, A33, A34, A39, A41, A42, A43, A44, A45 (28).
- PENDING_METHOD_SELECTION (status column): all 45 entries except A17 and A25, which are fully
  RESOLVED_FROM_MANUSCRIPT with no further method selection required (43).

## Resolution status update — Model Contract review (2026-08-15)

The table above records the manuscript inventory as originally produced and is left unedited.
`docs/MODEL_CONTRACT.md` (methodological review, no code/execution) has since made an explicit
decision for a bounded subset of these items, superseding their `PENDING_METHOD_SELECTION`
status. This section is the pointer; `docs/MODEL_CONTRACT.md` and `docs/METHOD_DECISION_LOG.md`
(D008-D013) hold the actual decisions and their justification.

| ID range | New status | Where resolved |
|---|---|---|
| A01-A16 | RESOLVED_BY_MODEL_CONTRACT | `docs/MODEL_CONTRACT.md`, Sections 3-7 |
| A18-A24 | RESOLVED_BY_MODEL_CONTRACT | `docs/MODEL_CONTRACT.md`, Section 8 |
| A25 | RESOLVED_BY_MODEL_CONTRACT (reinterpreted) | `docs/MODEL_CONTRACT.md`, Section 6 — same RMSE functional form, now compared against the corrected flow-based observation model instead of raw I(t) |
| A26 | RESOLVED_BY_MODEL_CONTRACT (partially — beta/sigma/alpha decided; gamma/d bounds retained provisionally, PENDING an external literature check) | `docs/MODEL_CONTRACT.md`, "Parameter bounds rationale" |
| A27 | RESOLVED_BY_MODEL_CONTRACT | `docs/MODEL_CONTRACT.md`, Section 9 |
| A28-A32 | RESOLVED_BY_MODEL_CONTRACT | `docs/MODEL_CONTRACT.md`, Sections 5, 10 |

Still `PENDING_METHOD_SELECTION` (unchanged, explicitly deferred by `docs/MODEL_CONTRACT.md`
Section 13): A33, A34, A36 (Jacobian derivation still required), A38-A45. A17, A35, A37 remain
`RESOLVED_FROM_MANUSCRIPT` as before.

## External-evidence resolution — Parameter Contract review (2026-08-15)

`docs/EXTERNAL_PARAMETER_CONTRACT.md` (methodological review with cited external sources; no
code/execution) closed the remaining external-evidence sub-decisions within A02-A04, A11-A13,
and finalized A26's alpha rationale. Superseding note only; the original inventory table above
remains unedited.

| ID | New status | Where resolved |
|---|---|---|
| A02 (N/N(t)) | RESOLVED_BY_EXTERNAL_PARAMETER_CONTRACT, with `PROVENANCE_REQUIRED` flagged for the 2021-2022 portion and a conservative extrapolation substitute defined | `docs/EXTERNAL_PARAMETER_CONTRACT.md`, Sections 2-3; `METHOD_DECISION_LOG.md` D016 |
| A03 (Lambda) | RESOLVED_BY_EXTERNAL_PARAMETER_CONTRACT | `docs/EXTERNAL_PARAMETER_CONTRACT.md`, Section 2; D010 (unchanged) |
| A04 (mu) | RESOLVED_BY_EXTERNAL_PARAMETER_CONTRACT | `docs/EXTERNAL_PARAMETER_CONTRACT.md`, Section 2; D015 |
| A11 (sigma) | RESOLVED_BY_EXTERNAL_PARAMETER_CONTRACT (bound unchanged; STRUCTURAL_LIMITATION_TO_DECLARE recorded) | `docs/EXTERNAL_PARAMETER_CONTRACT.md`, "sigma" detail; D019 |
| A12 (gamma) | RESOLVED_BY_EXTERNAL_PARAMETER_CONTRACT (bound revised; manuscript bound kept as sensitivity arm) | `docs/EXTERNAL_PARAMETER_CONTRACT.md`, "gamma" detail; D017 |
| A13 (d) | RESOLVED_BY_EXTERNAL_PARAMETER_CONTRACT (bound confirmed acceptable) | `docs/EXTERNAL_PARAMETER_CONTRACT.md`, "d" detail; D018 |
| A26 (alpha portion) | RESOLVED_BY_EXTERNAL_PARAMETER_CONTRACT (widened bound confirmed as an operational choice, no epidemiological justification claimed) | `docs/EXTERNAL_PARAMETER_CONTRACT.md`, Section 2 (alpha row) |
