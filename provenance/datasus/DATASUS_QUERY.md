PROVENANCE_AUDIT = tb_mes.xlsx / casos
SCOPE = CASOS_PROVENANCE_ONLY
THIS_AUDIT_DOES_NOT_BY_ITSELF_CLOSE_DATA_AVAILABILITY

CANONICAL_FILE = data/raw/tb_mes.xlsx (SHA-256 93e75138827704af22389c38eddc04eda5efd44389f10cffbabfd0a4e1ea662b) — IMMUTABLE
TARGET = 2001-01 .. 2022-12, N = 264

MODEL_DATA_DEPENDENCIES
    casos:
        calibration target             = 2001-01 .. 2020-12
        validation observations        = 2021-01 .. 2022-12
        provenance required            = 2001-01 .. 2022-12
    populacao:
        calibration/model input        = 2001-01 .. 2020-12
        validation forcing             = train-only log-linear extrapolation
                                         (observed 2021-2022 population NOT used)
        provenance required for
            model reproducibility      = 2001-01 .. 2020-12
            distributed dataset        = 2001-01 .. 2022-12
    TI:
        present in canonical source file
        not loaded by canonical modelling pipeline
        no independent provenance required to reproduce frozen results

DATA_AVAILABILITY_GATE = OPEN
    closes only when CASOS_PROVENANCE and POPULACAO_PROVENANCE
    are both resolved or documented as limitations

MATCH_CRITERION (pre-specified, no tolerance):
    MISMATCH_MONTHS = 0 AND MAX_ABS_DIFF = 0

CANDIDATE_SET (closed, ordered — no candidate may be added after first access)
    C1 = Brasil / confirmed cases / diagnosis year+month / no additional filters
    C2 = Brasil / confirmed cases / treatment-start year+month / no additional filters
    C3 = C1 restricted to new cases (Tipo de entrada = Caso novo)
    C4 = C2 restricted to new cases (Tipo de entrada = Caso novo)

UI_CONFIGURATION_RULE:
    Candidate definitions are semantic and fixed before access.
    A different literal UI label is admissible only if it is the unambiguous
    interface label for the same pre-specified dimension/filter. Label
    differences must be documented and do not create a new candidate.
    If a pre-specified configuration is unavailable, mark that candidate
    UNAVAILABLE; do not replace it with another configuration.

STOPPING RULE:
    first candidate meeting MATCH_CRITERION → EXACT_MATCH, stop
    all candidates fail or unavailable   → NO_EXACT_MATCH, stop,
                                           document discrepancy table

ACCEPTED_OUTCOMES = EXACT_MATCH | NO_EXACT_MATCH
NO_EXACT_MATCH does not authorise any change to the dataset, the model,
or any frozen result. It is documented as a provenance limitation.

ACCESS_DATE =
SOURCE_URL =

POST_ACCESS_OUTCOME (recorded 2026-09-23; definitions above remain preregistered)
    C1 = NO_EXACT_MATCH
    C2 = NO_EXACT_MATCH
    C3 = NO_EXACT_MATCH
    C4 = NO_EXACT_MATCH
    CASOS_PROVENANCE = NO_EXACT_MATCH
    CANDIDATE_SET_EXHAUSTED = YES
    POPULACAO_PROVENANCE = RESOLVED
    SCIENCE = FROZEN
    STOP_AFTER_C4 = YES
    DETAILS = C4_ACCESS_LOG.md and the four candidate access logs
    DATA_AVAILABILITY_GATE = OPEN pending explicit provenance-limitation wording
