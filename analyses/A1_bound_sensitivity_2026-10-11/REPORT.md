# A1 — Sensitivity to the lower bounds of alpha and sigma: report (2026-10-11)

**Status: STOPPED by the protocol after the first new fit (F-a).** Only F-0 (control) and F-a were
run; F-b, F-c and I-b were not run. Protocol: `PROTOCOL.md`, commit
`46be6493fd63aa5561fb33d23f996ade8cd4d1b4`, written before execution. Script: `run_bounds.py`.
Nothing in `evidence_S1/`, `results_canonical/` or `outputs/` was touched, and neither phase 2 nor
phase 3 was redone.

## Controls

- Script fidelity (objective at the S1 primary vectors): passed (differences 2.3e-13 and 0).
- F-0 (S1 configuration refitted): passed. It reproduces the S1 fractional primary,
  objective 619.318751, alpha 0.502203, sigma 0.010004.

## Why it stopped (two independent stop conditions, both met by F-a)

1. **Mandatory stop: training RMSE improves by more than 1%.** F-a (alpha in [0.20, 1.00], sigma
   in [0.01, 0.50]) reaches 589.307 against 619.319 for the S1 primary, a change of -4.85%.
2. **Numerical-resolution control failed, narrowly.** The maximum pointwise relative change between
   h = 1 and h = 0.25 is 1.0095% against a 1% threshold. The other criteria pass by a wide margin:
   RMSE change 0.016%, MAE change 0.070%, bias change 0.004% of the observed mean, and the
   refinement is monotone (0.5-vs-0.25 difference 24.4 against 54.9 for 1-vs-0.5). The threshold
   was fixed in advance and is not relaxed; no other grid was tried.

## What F-a shows (descriptive; single seed, single fit)

| | S1 primary (F-0) | F-a |
|---|---|---|
| alpha | 0.5022 | **0.2024** (new bound 0.20) |
| sigma | 0.010004 (bound 0.01) | 0.034974 (interior) |
| beta, gamma, d | 0.1200, 0.2613, 0.0391 | 0.0117, 0.2490, 0.0310 |
| Training RMSE | 619.32 | 589.31 (-4.85%) |
| Validation RMSE 2021-2022, open loop | 1216.54 | 1086.82 (-10.66%) |
| Reference R0 (phase-3 function) | 0.3578 | 0.0405 |

**Facts.**

- With the lower bound of alpha lowered to 0.20, the optimizer returns alpha = 0.2024, again within
  0.01 of the lower bound. By the boundary rule fixed in the protocol, alpha is determined by the
  boundary in F-a as it was in F-0. The training objective keeps decreasing as alpha moves down.
- sigma moves away from 0.01 to 0.035 in this fit. In F-a its bound was not changed, so this
  says nothing about sigma at 0.001 (F-b, F-c and I-b would have addressed that).
- beta = 0.0117 lies within 10% of the range width of its lower bound (0.01); the script
  flagged it.
- The validation RMSE of F-a is below that of the S1 integer primary (1759.54), so the ranking
  against the S1 integer primary does not invert. The ranking against I-b was not evaluated
  because I-b was not run.

**Inference (not tested).** In this single fit alpha is not pinned at 0.50 by the data: relaxing
the bound moves it to the next bound. That supports describing alpha as a bound artefact, which is
what Amaury's request A1 anticipated. It also means the S1 primary vector is not the best fit of the
fractional model under wider bounds, and quantities that depend on it (alpha 0.502, R0 0.34-0.59,
fractional-model skill) are conditional on the 0.50 bound. A single DE seed mixes the effect of the
bound with search variability, but a 4.85% change is well outside the 1% near-equivalence band used
in S1 phase 3.

**Not claimed.** That alpha = 0.20 is a better or more plausible value; that the fractional
model forecasts better with wider bounds (no rolling-origin evaluation was run); that sigma is or
is not at its bound at 0.001.

## Consequence for the manuscript and decisions that belong to the authors

This result may force a change to a central claim (Plan A, rule 3): the S1 evidence presents
alpha = 0.502 and the R0 envelope as conditional on a lower bound of 0.50, and the within-family
comparison could change in size under wider bounds. Nothing in the manuscript has been written yet.
Pending decisions:

1. Whether to run F-b, F-c and I-b under this same protocol (about one minute each). The stop
   clause halts this step, so I have not run them without your authorisation.
2. Whether the numerical-control miss (1.0095% against 1%) is accepted as a documented
   limitation or treated as a failure. The protocol treats it as a failure; changing it requires a
   decision, not a new grid chosen after seeing the result.
3. Whether a rolling-origin re-evaluation with widened bounds is warranted. It needs separate
   authorisation from fedeg and Amaury and is not part of Plan A.
4. How B5 and B2 are worded: the manuscript can say that alpha lies at its bound and that, when the
   bound is lowered to 0.20, the fit moves to the new bound with a lower training RMSE (-4.85%) and
   a lower validation RMSE; it cannot present alpha = 0.502 as an estimate.

Steps 6 to 10 were not started: step 8 depends on this step, and the plan requires stopping when a
result may change a central claim.

---

# Continuation (authorised by fedeg, 2026-10-11): F-b, F-c, I-b

Authorisation and rules: `PROTOCOL_ADDENDUM_2026-10-11.md` (commit `872aadc`), script options in
commit `962f076`, both made before the run. Outputs carry the suffix `_continuation`; the record of
the first stop is unchanged. Controls 1 and 2 passed again (F-0 reproduces the S1 primary).

**Status: STOPPED AGAIN at F-c. I-b was not run.**

## Results (single DE seed, calibration 2001-01 to 2020-12)

| | S1 primary (F-0) | F-b | F-c | F-a (first run) |
|---|---|---|---|---|
| alpha bounds / sigma bounds | [0.50,1] / [0.01,0.5] | [0.50,1] / [0.001,0.5] | [0.20,1] / [0.001,0.5] | [0.20,1] / [0.01,0.5] |
| alpha | 0.5022 | 0.5005 | 0.2003 | 0.2024 |
| sigma | 0.010004 | **0.006616** | 0.035936 | 0.034974 |
| beta / gamma / d | 0.1200 / 0.2613 / 0.0391 | 0.0131 / 0.2769 / 0.0081 | 0.0120 / 0.1335 / 0.0310 | 0.0117 / 0.2490 / 0.0310 |
| Training RMSE (change vs S1) | 619.32 | 615.82 (-0.57%) | 589.23 (-4.86%) | 589.31 (-4.85%) |
| Validation RMSE 2021-22 (change) | 1216.54 | 1195.56 (-1.72%) | 1078.60 (-11.34%) | 1086.82 (-10.66%) |
| Reference R0 (phase-3 function) | 0.3578 | 0.0391 | 0.0704 | 0.0405 |
| alpha determined by boundary? | yes | yes | yes | yes |
| sigma determined by boundary? | yes | **no** (0.0066 > 1.1 x 0.001) | no | no |
| Numerical control (h = 1 vs 0.25) | n/a | PASS (max pointwise 0.12%) | **FAIL** (1.0064%) | FAIL (1.0095%) |

## Why it stopped

F-c meets the same two stop conditions as F-a: training RMSE improves by 4.86% (limit 1%) and the
maximum pointwise relative change between h = 1 and h = 0.25 is 1.0064% (limit 1%). RMSE, MAE and
bias changes are far below 1% (0.016%, 0.069%, 0.004%) and refinement is monotone. The pointwise
excess appears in both fits with alpha near 0.2, which is where the protocol anticipated the
solver might behave worse. The threshold is not relaxed and no other grid was tried.

## Reading

**Facts.**

- **alpha** lies within 0.01 of its lower bound in all four fractional fits: 0.5005 with bound
  0.50, 0.2003 and 0.2024 with bound 0.20. Lowering the bound moves alpha to the new bound, and the
  training RMSE falls by about 4.9% when it does. In this dataset and with these bounds, alpha is
  not determined by the data in the range tested.
- **sigma** is interior when its lower bound is 0.001: 0.0066 in F-b and 0.0359 in F-c. By the
  protocol's rule it is not boundary-determined there. The S1 value 0.010004 is therefore a
  consequence of the 0.01 bound, not an estimate. The change in the training objective from
  moving only the sigma bound (F-b) is -0.57%, inside the 1% band used for near-equivalence in S1
  phase 3.
- **Reference R0** is not stable under these bounds. In F-b, with a training RMSE only 0.57% below
  the S1 primary, R0 is 0.039 against 0.358; in F-c and F-a it is 0.070 and 0.040. All are below
  the S1 envelope for the full pool (minimum 0.3417). The S1 envelope (0.3417-0.5879 for the
  admissible set) is conditional on the original bounds and does not cover solutions that are
  equally good at the 1% level once sigma is allowed to go below 0.01.
- **Validation ranking** against the S1 integer primary (1759.54) does not invert for F-a, F-b or
  F-c (all between 1078.6 and 1195.6). The test against I-b, as the protocol defines it, could not
  be completed because I-b was not run.
- **beta** is near its lower bound (0.01) in F-b, F-c and F-a, and **gamma** is flagged near a bound
  in F-b. Those bounds were not changed. The ordinary integer-model d, which Amaury mentioned, was
  not examined because I-b did not run.

**Inference (not tested).** The fractional fit in S1 sits at the corner of the original box
(alpha at 0.50, sigma at 0.01) and parts of the reported structure (alpha value, sigma value, R0
level) follow from that box. The result supports Amaury's reading of request A1, that alpha at the
bound is a bound artefact rather than a feature of the data, and extends it to sigma. It also
weakens any use of the S1 R0 envelope as a statement about the data: a near-equivalent fit (F-b)
sits well outside it. A single seed mixes the effect of the bounds with search variability, but F-b
and F-c agree on direction and the R0 gap is large (about an order of magnitude).

**Not claimed.** That any of the wider-bound fits is more plausible biologically (sigma = 0.0066
corresponds to a mean E-to-I progression time of about 12.6 years, and alpha = 0.20 is far from any
usual range); that the fractional model forecasts better under wider bounds (no rolling-origin
evaluation was run); anything about the integer model with sigma in [0.001, 0.5].

## Consequences for the manuscript

Plan A rule 3 applies: this result may force a change to a central claim. At least these elements
of the S1 presentation need to be reworded as conditional on the original bounds: alpha = 0.502,
sigma = 0.0100, the reference R0 envelope 0.3417-0.5879, and the statement that R0 is
comparatively stable across near-equivalent solutions (S1 phase 3 explored only solutions inside
the original box). What stays untouched: the fractional-versus-integer ordering in validation and
the negative skill against persistence and SARIMA in the S1 rolling-origin evidence, which used the
original bounds and were not recomputed.

## Pending decisions (fedeg, then Amaury)

1. Run I-b alone? It does not depend on the alpha bound, takes about 30 s, and would complete the
   ranking test and the integer-d check. The stop clause covers it, so it was not run.
2. Treat the numerical-control miss in F-a and F-c (about 1.006-1.010% against 1%) as a failure, as
   the protocol does, or document it as a limitation of the h = 1 solver at alpha near 0.2.
3. Whether the manuscript presents S1 as it is with these results as a sensitivity analysis, or
   whether a rolling-origin re-evaluation with wider bounds is warranted. The latter needs separate
   authorisation from fedeg and Amaury and is outside Plan A.

---

# I-b (authorised by fedeg, 2026-10-11, addendum 2: `PROTOCOL_ADDENDUM_2_2026-10-11.md`, commit `950b486`)

Controls 1 and 2 passed again. Outputs: `*_I-b.*`. Run order and rules as in the protocol.

**Status: STOPPED (third time, mandatory stop on training RMSE). The step 5 fits are now complete
for the authorised set; no further fit is pending.** The script stopped before building its
comparison table, so the comparisons below were computed afterwards from the recorded outputs.

## Result

| | S1 integer primary | I-b (sigma in [0.001, 0.5]) |
|---|---|---|
| beta / sigma / gamma / d | 0.0612 / 0.010173 / 0.0532 / 0.000213 | 0.3931 / **0.001002** / 0.2182 / 0.00933 |
| Training RMSE (change) | 776.04 | 689.07 (**-11.21%**) |
| Validation RMSE 2021-22, open loop (change) | 1759.54 | 1375.28 (-21.84%) |
| Reference R0 | not reported in S1 | 0.809 |
| sigma determined by boundary? | n/a | **yes** (0.001002 < 1.1 x 0.001) |
| Numerical control (h = 1 vs 0.25) | n/a | PASS (max pointwise change 1.6e-6) |

Stop condition met: training RMSE improves by 11.2% (limit 1%).

## Facts

- The integer model also improves when sigma is allowed to go lower, and it moves to the new bound
  (sigma = 0.001002). For the integer model, sigma at the bound is a bound effect as it was at
  0.01: the objective keeps decreasing as sigma goes down.
- The integer d in I-b is 0.00933, well inside its range [0.0001, 0.05]; the S1 integer d
  (0.000213) was close to its lower bound, as Amaury noted, and moves away from it when sigma is
  free. The d bound was not widened.
- **Validation ranking: not inverted.** All fractional fits stay below I-b in validation (F-a
  1086.8, F-b 1195.6, F-c 1078.6 against I-b 1375.3) and in training (589.3, 615.8, 589.2 against
  689.1). It is also not inverted against the S1 integer primary.
- **The within-family advantage shrinks a lot.** Fractional-to-integer RMSE ratio:

  | Comparison | Training | Validation |
  |---|---|---|
  | S1 primary fractional / S1 primary integer | 0.798 | 0.691 |
  | F-b / I-b (same sigma bound 0.001, alpha bound 0.50 for the fractional) | 0.894 | 0.869 |
  | F-c / I-b (alpha bound 0.20 for the fractional) | 0.855 | 0.784 |

  With a matched sigma bound, the fractional model's lower validation RMSE falls from 31% to 13%
  (F-b against I-b). The ordering holds in this single-seed set, but its size depends on the
  bounds.

## Reading

**Inference (not tested).** In S1, part of the apparent gain of the fractional model over the
integer one came from the 0.01 lower bound of sigma binding the integer model harder than the
fractional one. Letting both models use sigma down to 0.001 removes about half of the validation
gap. This is a single DE seed per fit and a single dataset; the size of the reduction should not be
quoted as a general quantity.

**Not claimed.** That the wider-bound integer model is a better or more plausible description
(sigma = 0.001 implies a mean E-to-I progression time of about 83 years, which is the proposed
bound and nothing the data supports on its own); that the within-family ordering would persist in
rolling-origin (not evaluated); that the integer model forecasts better than persistence or SARIMA
(not evaluated).

## Overall conclusion of step 5

1. alpha lies at the lower bound in every fractional fit (0.50 or 0.20): it is bound-determined.
2. sigma lies at its lower bound for the integer model (0.01 in S1, 0.001 in I-b) and is
   interior for the fractional model once the bound is 0.001 (0.0066, 0.0359).
3. The reference R0 of the fractional model changes by about an order of magnitude (0.04-0.07
   against 0.36) among fits whose training RMSE differs by 0.6% (F-b) to 4.9%; the S1 envelope is
   conditional on the original bounds.
4. The fractional-over-integer ordering in training and validation holds in all comparisons, but
   its magnitude drops from 20-31% to 10-13% (training/validation, F-b against I-b) when sigma is
   bounded identically.

None of these runs evaluated rolling-origin forecasts. The S1 skill statements against
persistence, seasonal naive and SARIMA were computed with the original bounds and are neither
confirmed nor contradicted here. Passing from this step to the manuscript (B2, B5, Abstract,
Results, Discussion) means deciding how to present S1 as conditional on the original bounds; that
decision needs fedeg and Amaury.

## Pending decisions

1. The marginal numerical-control miss for F-a and F-c (1.010% and 1.006% against 1%): failure, as
   in the protocol, or documented limitation of h = 1 at alpha near 0.2. I-b and F-b pass.
2. Whether the wider-bound results are reported as a sensitivity analysis alongside S1 (my
   recommendation: yes, in Methods/Results with the caveats above and without claiming the
   wider-bound fits as primary) or whether a rolling-origin re-evaluation is warranted
   (outside Plan A; needs fedeg and Amaury).
3. Which of steps 6-10 to start. Step 7 (limitation text) does not depend on step 5; step 8
   (manuscript) depends on both the decision above and on Amaury's sign-off on the S1 decision.
