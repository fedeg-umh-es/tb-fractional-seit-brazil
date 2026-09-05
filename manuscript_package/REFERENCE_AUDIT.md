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

| Ref | Citation | Intro | Discussion | Reference list | Identifier |
|---:|---|:---:|:---:|:---:|---|
| 1 | Alzahrani et al. (2024) | NO | YES | YES | 10.18576/amis/180101 |
| 2 | Area et al. (2015) | YES | NO | YES | 10.1016/j.aml.2014.09.006 |
| 3 | Bracher et al. (2021) | YES | YES | YES | 10.1371/journal.pcbi.1008618 |
| 4 | Chen et al. (2021) | NO | YES | YES | 10.1016/j.apm.2021.03.044 |
| 5 | Chishtie et al. (2026) | NO | YES | YES | 10.1016/j.epidem.2026.100887 |
| 6 | Cramer et al. (2022) | NO | YES | YES | 10.1073/pnas.2113561119 |
| 7 | Diethelm (2013) | YES | NO | YES | 10.1007/s11071-012-0475-2 |
| 8 | Gutenkunst et al. (2007) | NO | YES | YES | 10.1371/journal.pcbi.0030189 |
| 9 | Kalizhanova et al. (2024) | NO | YES | YES | 10.1038/s41598-024-76721-2 |
| 10 | Kao & Eisenberg (2018) | NO | YES | YES | 10.1016/j.epidem.2018.05.010 |
| 11 | Kharazmi et al. (2021) | NO | YES | YES | 10.1038/s43588-021-00158-0 |
| 12 | Meshkat et al. (2014) | YES | YES | YES | 10.1371/journal.pone.0110261 |
| 13 | Moran et al. (2016) | YES | YES | YES | 10.1093/infdis/jiw375 |
| 14 | Pelissari et al. (2020) | YES | NO | YES | 10.5123/S1679-49742020000100009 |
| 15 | Raue et al. (2009) | NO | YES | YES | 10.1093/bioinformatics/btp358 |
| 16 | Roosa & Chowell (2019) | YES | YES | YES | 10.1186/s12976-018-0097-6 |
| 17 | Simpson & Maclaren (2024) | NO | YES | YES | 10.1007/s11538-024-01294-0 |
| 18 | Tuncer & Le (2018) | YES | YES | YES | 10.1016/j.mbs.2018.02.004 |
| 19 | World Health Organization (2022) | YES | NO | YES | ISBN 978-92-4-006172-9 |

---

## Gate 2 Literature Rule

The literature verification matrix contains additional adversarial neighbors that are not necessarily cited in the manuscript. They remain audit evidence only unless a sentence in the manuscript materially relies on them.

The current manuscript cites three Gate 2 neighbors because they directly delimit the contribution:

- Chishtie et al. (2026): fractional vs integer with rolling-origin OOS multi-horizon forecasting, without the external statistical/naive benchmark suite used here.
- Alzahrani et al. (2024): fractional SEIR compared with ARIMA, without the same common rolling-origin multi-horizon protocol.
- Kalizhanova et al. (2024): TB mechanistic SIR vs SARIMA under temporal validation, without a fractional-vs-integer comparison.

No manuscript sentence claims `first study`, `never evaluated`, or universal absence.

---

## Final Verdict

`REFERENCE_AUDIT_VERDICT = SYNCHRONIZED_PENDING_FINAL_HUMAN_REVIEW`

This status means citation/reference bookkeeping is internally consistent. It does not replace final author verification of names, bibliographic style, or publisher-formatted references at submission.
