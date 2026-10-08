# Reference and Bibliography Audit

This document is the canonical audit of citations and references in `submission_bmb/BMB_MANUSCRIPT.md`.

---

## Audit Status

```text
CANONICAL_MANUSCRIPT = submission_bmb/BMB_MANUSCRIPT.md
TOTAL_REFERENCES_IN_MANUSCRIPT = 19
TOTAL_REFERENCES_CITED_IN_TEXT = 19
UNCITED_REFERENCES = 0
UNVERIFIED_IN_TEXT_CITATIONS = 0
DUPLICATE_REFERENCES = 0
ROOSA_CHOWELL_DOI = 10.1186/s12976-018-0097-6
GATE_2_REFERENCES_ADDED_TO_TEXT = Chishtie_2026; Alzahrani_2024; Kalizhanova_2024
CANDIDATE_ONLY_LITERATURE_COUNTED_AS_REFERENCES = NO
REFERENCE_AUDIT_VERDICT = SYNCHRONIZED_PENDING_FINAL_HUMAN_REVIEW
```

---

## Bidirectional Citation Inventory

| Ref | Citation | Text location | Reference list | Identifier |
|---:|---|---|:---:|---|
| 1 | Alzahrani et al. (2024) | Introduction | YES | 10.18576/amis/180101 |
| 2 | Area et al. (2015) | Introduction | YES | 10.1186/s13662-015-0613-5 |
| 3 | Chen et al. (2021) | Discussion | YES | 10.1016/j.apm.2021.03.044 |
| 4 | Chishtie et al. (2026) | Introduction | YES | 10.1016/j.epidem.2026.100887 |
| 5 | Cramer et al. (2022) | Discussion | YES | 10.1073/pnas.2113561119 |
| 6 | Diethelm (2013) | Introduction | YES | 10.1007/s11071-012-0475-2 |
| 7 | Gutenkunst et al. (2007) | Discussion | YES | 10.1371/journal.pcbi.0030189 |
| 8 | Instituto Brasileiro de Geografia e Estatística (2013) | Methods §2.2 | YES | IBGE projections page |
| 9 | Kalizhanova et al. (2024) | Introduction | YES | 10.1038/s41598-024-76721-2 |
| 10 | Kao & Eisenberg (2018) | Discussion | YES | 10.1016/j.epidem.2018.05.010 |
| 11 | Kharazmi et al. (2021) | Discussion | YES | 10.1038/s43588-021-00158-0 |
| 12 | Meshkat et al. (2014) | Discussion | YES | 10.1371/journal.pone.0110261 |
| 13 | Moran et al. (2016) | Introduction; Discussion | YES | 10.1093/infdis/jiw375 |
| 14 | Raue et al. (2009) | Discussion | YES | 10.1093/bioinformatics/btp358 |
| 15 | Rocha et al. (2020) | Introduction | YES | 10.5123/S1679-49742020000100009 |
| 16 | Roosa & Chowell (2019) | Introduction; Discussion | YES | 10.1186/s12976-018-0097-6 |
| 17 | Simpson & Maclaren (2024) | Discussion | YES | 10.1007/s11538-024-01294-0 |
| 18 | Tuncer & Le (2018) | Introduction; Discussion | YES | 10.1016/j.mbs.2018.02.004 |
| 19 | World Health Organization (2022) | Introduction | YES | ISBN 978-92-4-006172-9 |

---

## Gate 2 Literature Rule

The literature verification matrix contains additional adversarial neighbors that are not necessarily cited in the manuscript. They remain audit evidence only unless a sentence in the manuscript materially relies on them.

The current manuscript cites three Gate 2 neighbors because they directly delimit the contribution:

- Chishtie et al. (2026): fractional vs integer SEIQRDP comparison on Canadian COVID-19 data and, separately, rolling-origin validation at 7-, 14- and 21-day horizons; no external statistical/naive benchmark suite is described in the abstract. Evidence level: abstract only (full text not read).
- Alzahrani et al. (2024): fractional SEIR compared with ARIMA(2,0,1) on weekly influenza data as a comparison of fit (full text read on 2026-10-01); no held-out evaluation is described.
- Kalizhanova et al. (2024): TB SARIMA vs basic SIR on held-out data with different training and evaluation windows and a single partition (full text read); no fractional-vs-integer comparison.

No manuscript sentence claims `first study`, `never evaluated`, or universal absence.

## Changes of 2026-10-08

- Bracher et al. (2021) was removed from the manuscript and from the reference list: it concerns the weighted interval score for probabilistic forecasts and supports neither sentence in which it was cited. The list now has 19 entries.
- Pelissari et al. (2020) became Rocha et al. (2020) (first author Rocha MS) and the list was re-sorted; the Cramer et al. (2022) title now ends in "United States".
- Crossref (2026-10-08) confirms authors, year, title, journal, volume and pages for all 19 entries with a DOI. See `docs/audits/CITATION_REPAIR_REPORT_2026-10-08.md` for the evidence level behind each cited claim.

---

## Final Verdict

`REFERENCE_AUDIT_VERDICT = SYNCHRONIZED_PENDING_FINAL_HUMAN_REVIEW`

This status means citation/reference bookkeeping is internally consistent. It does not replace final author verification of names, bibliographic style, or publisher-formatted references at submission.
