# Submission form fields — Bulletin of Mathematical Biology (2026-10-12)

Plain text for copy-paste into the submission system. Source: `manuscript_latex/manuscript.tex` on `main`.

**Article type:** Original Research (Original Article)

**Title:** Within-Family Gains vs External Skill in Fractional SEIT Tuberculosis Forecasts

**Abstract (220 words; BMB limit 150–250):**

An improvement over an integer-order epidemic model does not necessarily imply useful forecasts. We investigated this distinction by independently reimplementing a fractional-order susceptible–exposed–infectious–treated (SEIT) tuberculosis model using 264 monthly notifications from Brazil (2001–2022). Its integer-order counterpart was refitted independently under the same calibration conditions. We then compared both models with persistence, seasonal naive, and seasonal autoregressive integrated moving average (SARIMA) forecasts across 13 expanding-window origins and leads of 1–12 months. Fractional SEIT achieved lower observed root mean squared error (RMSE) and mean absolute error than integer SEIT at every lead (RMSE at lead 1: 792 versus 1186 cases per month). Yet persistence (390) and SARIMA (536) had lower errors throughout, and the fractional model improved on seasonal naive (1091) only at leads 1–5. The fractional order and the progression rate lay at their lower search bounds; in a single-run sensitivity analysis, lowering the bounds moved both estimates and narrowed the within-family margin without changing its sign. Transmission, removal, and excess-mortality rates varied substantially among near-equivalent fits, although their predicted trajectories were similar. The basic reproduction number and disease-free equilibrium were evaluated only for an autonomous reference, not as properties of the time-varying forecasting system. For this national series, with dependent forecast errors and no formal significance tests, the within-family improvement did not establish competitive forecasting performance against persistence or SARIMA.

**Keywords (6):** Mathematical epidemiology; Fractional-order differential equations; Practical identifiability; Forecast evaluation; Basic reproduction number; Tuberculosis

**Authors, in order:**

1. Amaury de Souza — Instituto de Física, Universidade Federal de Mato Grosso do Sul, Campo Grande, Brazil — ORCID 0000-0001-8168-1482
2. Francisco Federico García Crespi (corresponding author) — Department of Computer Engineering, Universidad Miguel Hernández de Elche, Elche, Spain — fedeg@umh.es — ORCID 0000-0002-7129-7791

**Funding:** No funding was received for this study.

**Competing interests:** The authors declare that they have no competing interests.

**Ethics approval:** Not required; secondary, aggregated monthly notification data only.

**Consent for publication:** Not applicable.

**Data availability (short form):** The monthly series and all results are available at Zenodo, https://doi.org/10.5281/zenodo.23298329 (release v1.0.0), and in https://github.com/fedeg-umh-es/tb-fractional-seit-brazil.

**Code availability (short form):** Same Zenodo record and repository; code under the MIT licence.

**Open access:** No. Traditional subscription route; do not select paid open access.

**Files to upload:**

| Item | File |
|---|---|
| Manuscript (PDF) | PDF compiled in Overleaf from `manuscript_latex/TB_SEIT_BMB_overleaf_2026-10-11.zip` (current `main`) |
| LaTeX source | the same ZIP (manuscript.tex, references.bib, sn-jnl.cls, sn-mathphys-ay.bst, figures/, tables/) |
| Cover letter | PDF compiled from `submission_final/COVER_LETTER.tex` |

**Suggested reviewers:** none proposed (add only if the system requires them).
