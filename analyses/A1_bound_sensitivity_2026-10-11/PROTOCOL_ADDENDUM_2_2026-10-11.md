# A1 — Protocol addendum 2: I-b (2026-10-11)

After the second stop (F-c; `REPORT.md`, continuation section, commit `c64d482`), fedeg authorised,
in the session of 2026-10-11, running **I-b only** with the same protocol: integer model
(alpha = 1), sigma in [0.001, 0.5], beta, gamma and d with their original bounds, same DE settings
and seed. All rules, thresholds, controls and mandatory stops of `PROTOCOL.md` and of addendum 1
apply unchanged; if I-b triggers one, the run stops and is reported. The authorisation does not
cover any rolling-origin evaluation, other bounds, or a change of thresholds.

Bookkeeping: outputs of this run carry the suffix `_I-b` (environment variable `A1_SUFFIX`), so the
earlier records are not overwritten. The final comparison and the ranking test (F-a, F-b and F-c
against I-b and against the S1 integer primary) read the recorded values of F-a, F-b and F-c from
the earlier output files. The numerical-control status recorded for them (F-a FAIL, F-b PASS, F-c
FAIL) is carried into the table. Controls 1 and 2 are run again before I-b, as before.
