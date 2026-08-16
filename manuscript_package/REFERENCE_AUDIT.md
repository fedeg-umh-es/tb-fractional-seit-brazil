# Reference and Bibliography Audit

This document provides a comprehensive audit of all bibliographic citations and references in `manuscript_package/MASTER_MANUSCRIPT.md`, verifying bidirectional citation consistency, absence of duplicates, and completeness of DOI/ISBN metadata.

---

## Audit Checklist & Status Summary

```text
REPOSITORY_AUTHOR = fedeg
TOTAL_VERIFIED_REFERENCES = 16
TOTAL_REFERENCES_CITED_IN_TEXT = 16
UNCITED_VERIFIED_REFERENCES = 0
UNVERIFIED_IN_TEXT_CITATIONS = 0
DUPLICATE_REFERENCES_DETECTED = NO
MISSING_DOIS_OR_IDENTIFIERS = NO
BIBLIOGRAPHIC_METADATA_STATUS = COMPLETE_AND_VERIFIED
```

---

## Bidirectional Citation Cross-Reference Matrix

| Ref ID | Full Citation Label | Used in Intro | Used in Disc | In Master Ref List | DOI / Identifier | Verification Status |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **REF-01** | World Health Organization (2022) | YES (I1) | NO | YES | ISBN 978-92-4-006172-9 | VERIFIED |
| **REF-02** | Pelissari et al. (2020) | YES (I1) | NO | YES | 10.5123/S1679-49742020000100009 | VERIFIED |
| **REF-03** | Moran et al. (2016) | YES (I1) | YES (D2) | YES | 10.1093/infdis/jiw375 | VERIFIED |
| **REF-04** | Bracher et al. (2021) | YES (I1) | YES (D1) | YES | 10.1371/journal.pcbi.1008618 | VERIFIED |
| **REF-05** | Cramer et al. (2022) | NO | YES (D1, D2) | YES | 10.1073/pnas.2113561119 | VERIFIED |
| **REF-06** | Diethelm (2013) | YES (I2) | NO | YES | 10.1007/s11071-012-0475-2 | VERIFIED |
| **REF-07** | Area et al. (2015) | YES (I2) | NO | YES | 10.1016/j.aml.2014.09.006 | VERIFIED |
| **REF-08** | Tuncer & Le (2018) | YES (I3) | YES (D4) | YES | 10.1016/j.mbs.2018.02.004 | VERIFIED |
| **REF-09** | Roosa & Chowell (2019) | YES (I3) | YES (D4) | YES | 10.1186/s12976-018-0094-2 | VERIFIED |
| **REF-10** | Meshkat et al. (2014) | YES (I3) | YES (D5, D6) | YES | 10.1371/journal.pone.0110261 | VERIFIED |
| **REF-11** | Raue et al. (2009) | NO | YES (D5) | YES | 10.1093/bioinformatics/btp358 | VERIFIED |
| **REF-12** | Chen et al. (2021) | NO | YES (D2) | YES | 10.1016/j.apm.2021.03.044 | VERIFIED |
| **REF-13** | Kharazmi et al. (2021) | NO | YES (D2) | YES | 10.1038/s43588-021-00158-0 | VERIFIED |
| **REF-14** | Simpson & Maclaren (2024) | NO | YES (D6) | YES | 10.1007/s11538-024-01294-0 | VERIFIED |
| **REF-15** | Gutenkunst et al. (2007) | NO | YES (D6) | YES | 10.1371/journal.pcbi.0030189 | VERIFIED |
| **REF-16** | Kao & Eisenberg (2018) | NO | YES (D6) | YES | 10.1016/j.epidem.2018.05.010 | VERIFIED |

---

## Detailed In-Text Citation Audit

1. **Introduction Paragraph 1 (I1)**:
   * Text: `(World Health Organization, 2022; Pelissari et al., 2020)` → Mapped to **REF-01** and **REF-02**.
   * Text: `(Moran et al., 2016; Bracher et al., 2021)` → Mapped to **REF-03** and **REF-04**.
2. **Introduction Paragraph 2 (I2)**:
   * Text: `(Diethelm, 2013; Area et al., 2015)` → Mapped to **REF-06** and **REF-07**.
3. **Introduction Paragraph 3 (I3)**:
   * Text: `(Tuncer & Le, 2018; Roosa & Chowell, 2019; Meshkat et al., 2014)` → Mapped to **REF-08**, **REF-09**, and **REF-10**.
4. **Discussion Paragraph 1 (D1)**:
   * Text: `(Bracher et al., 2021; Cramer et al., 2022)` → Mapped to **REF-04** and **REF-05**.
5. **Discussion Paragraph 2 (D2)**:
   * Text: `(Moran et al., 2016; Cramer et al., 2022)` → Mapped to **REF-03** and **REF-05**.
   * Text: `(Chen et al., 2021; Kharazmi et al., 2021)` → Mapped to **REF-12** and **REF-13**.
6. **Discussion Paragraph 4 (D4)**:
   * Text: `(Tuncer & Le, 2018; Roosa & Chowell, 2019)` → Mapped to **REF-08** and **REF-09**.
7. **Discussion Paragraph 5 (D5)**:
   * Text: `(Meshkat et al., 2014; Raue et al., 2009)` → Mapped to **REF-10** and **REF-11**.
8. **Discussion Paragraph 6 (D6 - Literature Boundary)**:
   * Text: `(Simpson & Maclaren, 2024; Gutenkunst et al., 2007)` → Mapped to **REF-14** and **REF-15**.
   * Text: `(Meshkat et al., 2014; Kao & Eisenberg, 2018)` → Mapped to **REF-10** and **REF-16**.

---

## Final Reference Audit Verdict

* `UNRESOLVED_CITATIONS = 0`
* `ORPHAN_REFERENCES = 0`
* `DUPLICATE_ENTRIES = 0`
* `METADATA_DEFICIENCIES = 0`
* `REFERENCE_AUDIT_VERDICT = COMPLETE_AND_VERIFIED`
