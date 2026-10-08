# BMB pre-compilation academic audit — 2026-10-08

**Scope:** diagnostic-only audit of `submission_bmb/BMB_MANUSCRIPT.md` on `fix/bmb-citation-repair-2026-10-08`; PIER paragraph anatomy, C–C–C/skip test, scope/desk-reject surface, and claim-to-evidence consistency. No manuscript, frozen evidence, data, metrics, figures, model, or test script was changed by this audit. **Compilation gate: HOLD.**

## 0. Editorial surface and BMB fit
- **Two-minute desk test:** PARTIAL. The title and abstract distinguish within-family error reduction from external forecast skill, and the empirical negative result is clearly bounded; however, the affirmative transferable contribution to *mathematical biology* is not as explicit as the forecasting comparison.
- **Familiar framing:** PARTIALLY FAMILIAR (SEIT, Caputo, R0 and practical identifiability fit the readership; baseline-relative forecast skill and a primarily methodological benchmarking claim may appear adjacent).
- **Journal fit:** MEDIUM. The BMB aims and scope require life-science/mathematical-science relevance, typically biological insight from mathematical tools or new methods with demonstrated biological applicability. This is an independent reimplementation and case-specific audit, not an original mathematical method or standalone epidemiological explanation. No novelty or biological mechanism should be fabricated to repair fit.
- **Formal gate:** BMB requires editable LaTeX or DOCX source, 150–250 abstract words, 4–6 keywords, numbered lines/pages, declarations, and coauthor approval. PDF compilation does not establish scientific validity.

## 1. C–C–C and skip-reading
- **Macro:** Introduction introduces need for external benchmarks; Results establish within-family advantage, negative skill against persistence/SARIMA, and seasonal-naive exception; Discussion bounds interpretation. Macro C–C–C passes with qualifications.
- **Intro P1–P2:** relevant disease/model context and fit-versus-forecast tension. PASS.
- **Intro P3:** OVERLOADED. First sentence introduces the evaluation question; remaining paragraph both justifies baselines and reviews three different prior studies (Chishtie, Alzahrani, Kalizhanova), each with qualification. Mechanical fix: separate the actual evaluation question from the carefully qualified literature contrast without adding references or priority claims.
- **Intro P4:** identifiability explicitly secondary. PASS.
- **Intro P5–P6:** partially redundant study-objective and protocol inventory. Mechanical fix: P5 state questions and P6 state only the distinct evidence needed and the bounded contribution.
- **Discussion P1–P3:** topic sentences reconstruct central turning point; P1 last sentence on Cramer moves to an external example without fully bridging it. PARTIAL.
- **Discussion P4:** the seasonal-naive exception is clearly benchmark-specific. PASS.
- **Discussion P5–P6:** P6 carries observed R0 result, mechanism speculation, structural-versus-practical literature, and uncertainty-limit caveat. OVERLOADED; split literature/interpretation from evidence-specific scope, without changing claims.
- **Discussion P7:** short DFE paragraph is consistent but can be integrated with P6, maintaining the subspace/frozen-demography caveat below.
- **Discussion P8:** limitations arrive relatively late. Move strongest interpretation limits (single series, 13 origins, supplied cases provenance, operational nature of R0) earlier; keep the full limitation record, including residual autocorrelation, horizon-specific loss dependence and absence of significance tests.
- **Conclusion P1–P3:** defensible limits, but P3 substantially repeats P1; reduce repetition after science issues are closed.

## 2. Claim-to-evidence register
| Claim | Evidence | Judgment |
|---|---|---|
| C01 Fractional SEIT lower *observed* error than independently refit integer SEIT | Frozen long-open-loop and rolling-origin tables | SUPPORTED AS COMPARISON OF TWO FITTED MODEL CONFIGURATIONS. Avoid attributing the reduction causally to fractional differentiation alone; parameter dimension and calibration also differ. |
| C02/03 Negative skill vs persistence and SARIMA for h=1..12 | Canonical horizon/skill CSVs; Figure 1/2 | SUPPORTED as observed descriptive errors, not inference. |
| C04 Seasonal naive positive RMSE/MAE skill h=1..7 and negative h=8..12 | Frozen skill and horizon summary | SUPPORTED; H_relax=7 is baseline/series/origin specific, not an intrinsic limit. |
| C05 Operationally/general forecasting advantage | Negative vs two baselines | NOT SUPPORTED, and manuscript correctly rejects it. |
| C06 Biological memory from alpha<1 | No independent mechanistic evidence | NOT SUPPORTED, correctly excluded. |
| C07 R0 in [1.1542,1.1892] | 25-member near-equivalent admissible set; sigma at lower bound | SUPPORTED CONDITIONALLY, not interval for sampling uncertainty or the 33-point pool. |
| C08 DFE instability | E,I Jacobian Matignon classification on 25 admissible models | SUPPORTED **ONLY FOR FROZEN-DEMOGRAPHY INFECTED SUBSYSTEM**; present wording can mislead as whole 5-state, time-varying N(t) stability result. |
| C09 beta, gamma, d individually weakly identifiable | Profile/multiseed diagnostics | SUPPORTED within operational fitted set; not a proof of structural non-identifiability. |
| C10 Historical 48% optimal control reduction | Not reimplemented | NOT VERIFIED; correctly excluded. |
| C11 Formal statistical superiority/inferiority | No prespecified dependence-aware comparison tests | NOT TESTED; descriptive-only claims appropriate. |

### SCIENTIFIC BLOCKER S1 — fractional observation operator (Methods §2.2–2.3, model code)
Actual implementation in `src/tb_seit/model.py` and `src/tb_seit/solver.py`:
`D_Caputo^alpha C(t) = tau0^(1-alpha) sigma E(t)` and predicted monthly observations are differences `C(t_{k+1})-C(t_k)`.
For 0<alpha<1, this is a *fractional integral* of the progression rate, not the ordinary time integral of that rate. In general, its monthly increments are not monthly incident transitions `int_{t_k}^{t_{k+1}} sigma E(s) ds`. Counterexample for constant rate r=1, tau0=1: `C(t)=t^alpha/Gamma(1+alpha)`; at alpha=0.963 the first two increments are 1.015314 and 0.963898 rather than 1 and 1. This issue concerns **the meaning of the model's measurement operator**, not floating-point or wording alone. The model's fit and forecasting numbers are real results for the implemented functional; they cannot be represented without qualification as forecasts of a standard monthly integral of E→I incidence. Author/methodological decision required before new compilation. Possible paths (not pre-authorized): reinterpret the quantity honestly as a fractional-incidence proxy, or implement an ordinary-time flow accumulator as part of a scientifically approved model correction, in which case numerical evidence would need re-evaluation. Do **not** silently change equations, code, results or claims.

### MATHEMATICAL PRECISION M1 — Caputo formula at alpha=1
The integral representation `(Gamma(1-alpha))^-1 int_0^t (t-s)^(-alpha) X'(s) ds` is valid for `0<alpha<1`. At `alpha=1`, define the derivative as the ordinary first derivative (or specify the continuous extension). The manuscript currently displays alpha in (0,1] directly above the singular integral form. Editorial/mathematical correction needed.

### MATHEMATICAL PRECISION M2 — DFE stability scope
`scripts/r0_evidence_set_and_stability.py` classifies only the infected 2×2 **(E,I) Jacobian** using `dimensional_audit.j_ei`, not all five states. The model is integrated using an exogenous **time-varying N(t)**. A frozen-demography DFE analysis can be defined for the corresponding fixed N*=S* approximation; do not claim stability/instability of the full nonautonomous 5-state system. The Caputo incidence accumulator C is an unforced bookkeeping coordinate with a zero Jacobian eigenvalue in the full system and cannot be included in a blanket asymptotic-stability claim. Clarify the subspace, fixed-N reference, and conditional conclusion.

### METHOD ATTRIBUTION M3 — train-only and inference
`scripts/run_rolling_origin_forecast.py` calls training-set restriction by origin and refits the SEIT models and SARIMA coefficients, with SARIMA structural order selected on 2001–2020. This supports the intended train-only *design*. The sentence 'guarantees zero information leakage' is stronger than an audit of one script alone; end-to-end implementation validation is distinct from a protocol description. Rolling-origin errors have dependence and n=13 origins; the manuscript appropriately avoids p-value or confidence conclusions.

## 3. References and scholarly consistency
- Independent bibliography-identifier audit through Scholar Sidekick: **17/17 DOI-identified entries matched**, 0 mismatch, 0 retraction signal. IBGE and WHO book/report records have no DOI and were not checked by that batch. Identifier resolution does not prove a citation supports the adjacent scientific claim.
- Chishtie et al. (2026) wording now separates fitted fractional/integer RMSE from rolling-origin comparison for both configurations; the cited work is not the same external-baseline design.
- Alzahrani and Kalizhanova are appropriately qualified by comparison type and unequal historical windows respectively.
- No priority claim or broad absence-in-literature gap was established.

## 4. Actions, prioritized
1. **SCIENTIFIC BLOCKER:** Resolve the fractional-accumulator versus ordinary monthly-incidence observation claim in Methods 2.2–2.3 and connected Abstract/Results/Discussion before changing code or compiling.
2. **ACTION 2:** Scope the Caputo integral to 0<alpha<1, with alpha=1 defined classically — Methods 2.3; mathematical precision.
3. **ACTION 3:** Qualify R0/Matignon claims as frozen-demography infected-subsystem diagnostics — Methods 2.7, Results 3.3, Discussion and Conclusion.
4. **ACTION 4:** Replace causal wording 'fractional differentiation reduced forecast error' by method-comparison wording and keep descriptive/inferential distinction — Abstract, Discussion P1, Conclusion.
5. **ACTION 5:** Split Intro P3; reduce Intro P5–P6 and Discussion P6–P8 paragraph overload and repetitions without inventing claims or altering evidence.

## 5. Gate and test status
- `SCIENTIFIC_GATE = HOLD`, `READY_TO_COMPILE = NO`, `READY_FOR_SUBMISSION = NO`.
- No new calibration, model execution or rerun of canonical numerical analysis was authorized/performed.
- A local `git clone` failed due DNS resolution of github.com in this session; the repository tests have **not been rerun at this HEAD**. The older 30/30 test report is not current validation.
- Test execution is still requested and can be pursued independently of manuscript compilation. Even green tests would not resolve S1: existing tests may encode the observation-operator assumption.
- BMB aims and scope: https://link.springer.com/journal/11538/aims-and-scope. Instructions: https://link.springer.com/journal/11538/submission-guidelines.

**Decision:** return S1 to the scientific claim/measurement gate; do not proceed directly to PDF compilation.
