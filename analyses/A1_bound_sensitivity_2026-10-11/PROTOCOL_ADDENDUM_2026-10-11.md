# A1 — Protocol addendum: continuation after the mandatory stop (2026-10-11)

Original protocol: `PROTOCOL.md` (commit `46be6493fd63aa5561fb33d23f996ade8cd4d1b4`). The run
stopped after F-a (see `REPORT.md`, `STOP.txt`, commit `ad60e34`).

## Authorisation

fedeg authorised, in the session of 2026-10-11 and after reading the stop report, running **F-b,
F-c and I-b with the same protocol**. The authorisation covers only these three fits. It does not
cover a rolling-origin re-evaluation, any other bound, or a change of any threshold.

## What does not change

Settings, bounds of each fit, seed, boundary rules, controls and mandatory stops are those of
`PROTOCOL.md`, including: stop if a fit improves the training RMSE by more than 1% over the S1
primary of the same model, if the numerical-resolution control fails, if the optimizer does not
succeed, or if the fractional-versus-integer validation ranking inverts. If one of these occurs
in F-b, F-c or I-b, the run stops again and is reported; no variant is tried.

## What is added (bookkeeping only)

- The script takes the fit ids to run and writes its outputs with the suffix `_continuation`, so
  the record of the stopped run (`fit_parameters.csv`, `numerical_controls.csv`, `STOP.txt`,
  `predictions_F-0.csv`, `predictions_F-a.csv`) is not overwritten.
- Controls 1 and 2 (script fidelity; F-0 reproduces the S1 primary) are run again before the new
  fits, as in the original run.
- F-a enters the final comparison and the ranking test with the values already recorded (not
  re-run), flagged as having failed the numerical-resolution control (1.0095% against 1%) and the
  1% training-improvement stop.
- Because F-a already met a mandatory stop, the comparison table is descriptive for F-a; it is not
  evidence that the stop conditions were satisfied.
