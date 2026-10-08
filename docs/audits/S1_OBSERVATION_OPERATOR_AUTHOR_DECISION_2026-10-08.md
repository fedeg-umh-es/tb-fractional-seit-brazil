# S1 — Scientific decision record: fractional observation operator (2026-10-08)

**Status:** \`AWAITING_AUTHOR_DECISION\`  
**Branch:** \`fix/bmb-citation-repair-2026-10-08\` / PR #3 (draft)  
**Approvers:** Amaury de Souza (corresponding author) and Federico García Crespi (coauthor)  
**Precompilation gate:** \`HOLD\` — no LaTeX/PDF production until scientific decision and verified repairs.

## 1. Verified implementation and mismatch

The existing model implements a Caputo fractional auxiliary state,

\[
{}^CD_t^\alpha C(t)=\tau_0^{1-\alpha}\sigma E(t),\qquad C(0)=0,
\]

and predicts monthly reported notifications by the difference

\[
\widehat y_k=C(t_{k+1})-C(t_k).
\]

This is the actual computation in \`src/tb_seit/model.py\`, \`src/tb_seit/rolling_origin.py\` and \`src/tb_seit/solver.py\`. For \`0<alpha<1\` the solution is

\[
C(t)=\frac{\tau_0^{1-\alpha}}{\Gamma(\alpha)}
\int_0^t(t-s)^{\alpha-1}\sigma E(s)\,ds.
\]

Consequently, \(\widehat y_k\) is a difference of a fractional *memory functional*, not the ordinary monthly accumulated transition count \(\int_{t_k}^{t_{k+1}}\sigma E(s)\,ds\). Equality only follows at \(\alpha=1\). In general the increment is not guaranteed to be nonnegative for every nonnegative progression-rate history; \`C\` should not be called a physical cumulative count without additional justification.

The frozen fractional predictions are all finite and positive in the *evaluated empirical support*: calibration 240/240, validation 24/24, rolling-origin 156/156. Ranges: 7265.975–8216.555, 7165.203–7261.902, and 7159.773–7310.504 respectively. These are forensic checks of previously archived predictions, not new simulations. Positivity in these samples does not validate the physical meaning or general monotonicity of \`C\`.

The initialization \`E(0)=y_0/\sigma\`, where \`y_0\` is the first *monthly* observed count, is likewise a deterministic initialization **proxy**, not an analytical inversion of the fractional monthly observation operator.

## 2. Decision alternatives for the authors

### A — Retain code and frozen results, narrow the scientific claim (preferred *proposal*, not yet authorized)

Declare explicitly that \(\widehat y_k=\Delta C_k\) is an **operational fractional-memory observable calibrated against monthly notifications**, not the ordinary integral of the exposed-to-infectious transition rate; \`C\` must be renamed or described as an auxiliary fractional state, not a physical cumulative case count.

**Preserved:** actual model implementation, fitted parameters, frozen forecasts and metrics, 13-origin 12-horizon evaluation, persistence/seasonal-naive/SARIMA benchmarks, C01–C04 numerical comparisons, and descriptive horizon indices.

**Restricted/rewritten:** do not say the implemented fractional model forecasts actual monthly E→I transition counts or that it physically integrates incident infections; describe it as a phenomenological forecast of notification counts through its defined measurement functional. Do not attribute differences to fractional differentiation of compartment dynamics *alone*, since the observation mapping also differs at \(\alpha=1\). Treat fitted biological rates, \(\alpha\), derived \`R0\`, and DFE stability only as properties/diagnostics of the fitted model under the explicit observation-model limitation; they are not established biological mechanisms or external epidemiological conclusions.

**Required before declaring S1 resolved:**
1. Explicit acceptance by both authors that the study can be framed as a **phenomenological forecasting comparison** with this observation operator, not an epidemiologically validated incidence-flow model.
2. Correct Methods §2.2–2.4: observable, initial-condition proxy and Caputo \(\alpha=1\) special case; replace claims of ordinary time integration and physical cumulative incidence.
3. Propagate interpretation consistently through Abstract, Results, Discussion, Conclusion, figure/table captions, supplementary material, and claim-support/traceability narrative; do not edit frozen evidence files.
4. Rebound \`R0\`/Matignon discussion to the frozen-demography infected \((E,I)\) subsystem, not the full time-varying-population five-state system.
5. Audit every edited claim against code and frozen data; run existing repository tests, check the complete diff, and obtain author-level scientific approval of the repaired text.
6. Reassess journal fit under this narrower phenomenological interpretation rather than compensating with stronger novelty language.

**Conditional advantage:** A may preserve the existing computed results without re-fitting *if* the revised research question and scientific claims remain acceptable and all above conditions pass. This is not automatic approval of the model as epidemiologically valid.

### B — Redefine the output as ordinary monthly incidence

Introduce a measurement operator that produces the ordinary time integral \(\int_{t_k}^{t_{k+1}}\sigma E(s)\,ds\). That is a changed model/observation contract, **not** an editorial correction: review initial conditions, solver/output pipeline, calibration, fair integer comparison, cross-validation and all associated numerical claims. Version the new contract and rerun and independently validate affected experiments only **after** explicit author approval. Do not carry over earlier numerical metrics or figures as if they tested this new observable.

## 3. Author decision required

Record one of:
- \`S1_DECISION = A_ACCEPTED_WITH_SCOPE_RESTRICTIONS\`; both authors accept the phenomenological output mapping and authorize strictly evidence-preserving documentary repairs;
- \`S1_DECISION = B_REDEFINE_MEASUREMENT_OPERATOR\`; both authors accept a model-contract change and authorize a separately specified evidence re-evaluation;
- \`S1_DECISION = DEFER\`; keep the submission blocked.

\`AMAURY_SIGNOFF = PENDING\`
\`FEDERICO_SIGNOFF = PENDING\`

The numerical evidence remains frozen and **the decision is not inferred from a suggestion**. No edits to code, canonical tables, metrics, source data, plots or model results are authorized by this record.

## 4. Separate outstanding gates

- Origin of \`data/raw/tb_mes.xlsx\`: exact \`casos\` extraction configuration not verified; preserve the existing four-candidate audit and source hash. Record a specific Git commit for reviewer access once the relevant branch is selected; verify redistribution/reuse terms separately from the MIT *software* license.
- Run tests against the eventual post-repair HEAD, plus \`git diff --check\` and manuscript-to-evidence checks.
- Author approvals and production QA precede declaring \`READY_FOR_SUBMISSION\`.

**Current state:** \`S1 = OPEN\`, \`READY_TO_COMPILE = NO\`, \`READY_FOR_SUBMISSION = NO\`.
