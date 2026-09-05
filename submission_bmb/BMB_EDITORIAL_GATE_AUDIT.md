# Bulletin of Mathematical Biology — Editorial and Formal Gate Audit

**Verification date**: 2026-09-05  
**Target journal**: *Bulletin of Mathematical Biology*  
**Publisher**: Springer Nature  
**Publishing model**: Hybrid  
**Manuscript identity**: Original Research  
**Canonical manuscript**: `submission_bmb/BMB_MANUSCRIPT.md`

Official sources verified on 2026-09-05:

- Aims and scope: `https://link.springer.com/journal/11538/aims-and-scope`
- Submission guidelines: `https://link.springer.com/journal/11538/submission-guidelines`

---

## 1. Editorial-entry gate

```text
DOMINANT_SCIENTIFIC_QUESTION = STABLE
CANONICAL_EVIDENCE = FROZEN
CLAIM_MAPPING = PASS
CONTRIBUTION_TYPE = STABLE
MANUSCRIPT_IDENTITY = ORIGINAL_RESEARCH
NEW_EXPERIMENT_REQUIRED = NO
```

**Decision**: editorial adaptation may affect packaging, emphasis, and format only. It must not redefine the scientific question or evidence base.

---

## 2. Journal fit

### Manuscript object as written
Independent reimplementation and methodological evaluation of a fractional-order mechanistic epidemic model, centered on whether a within-family fractional-versus-integer error reduction translates into forecasting skill against external baselines. Practical identifiability is a secondary interpretive axis.

### Official scope
The journal states that it publishes research at the interface of the life and mathematical sciences and that contributions should be relevant to both. Original research may provide new biological insights using mathematical tools or mathematical tools/methods with demonstrated applicability to biological investigations.

### Fit assessment

| Check | Assessment |
|---|---|
| Biological object | Tuberculosis dynamics and surveillance forecasting |
| Mathematical object | Fractional-order SEIT dynamics, calibration, identifiability, $R_0$, Matignon stability, temporal forecast evaluation |
| Contribution type | Empirical methodological evaluation of a mechanistic extension under stronger external benchmarking |
| Scope match | VERIFIED / PLAUSIBLE |
| Contribution-type match | PLAUSIBLE but not guaranteed |
| Article type | Original Research is preferable to Methods; the paper does not introduce a new general mathematical method |
| Evidence breadth | Bounded single national time series; claims are correspondingly bounded |
| Editorial-priority risk | MEDIUM |

**Fit verdict**: **MEDIUM / DEFENSIBLE**. The paper sits within mathematical epidemiology and uses mathematical-model analysis with biological data, but the principal editorial risk is contribution threshold rather than topical scope. An editor may regard a single-case methodological evaluation as insufficiently broad unless the title, abstract, and cover letter make the transferable evaluation lesson visible without claiming universal fractional-model behavior.

---

## 3. Desk-reject surface

### Affirmative contribution
**PASS.** The Abstract now states the positive contribution early: the study independently reimplements the model, applies temporal external benchmarking, and demonstrates that the favorable within-family result does not support a general forecasting advantage in this case study.

### Familiar framing
**FAMILIAR / ACCEPTABLE.** Mathematical epidemiology, fractional differential equations, identifiability, $R_0$, equilibrium stability, and prediction are all recognizable mathematical-biology objects. Forecasting terminology is anchored to a mechanistic-model evaluation question rather than presented as a generic time-series paper.

### Two-minute editor test

- **What does the paper contribute?** A controlled empirical test of whether a favorable fractional-versus-integer comparison survives external forecasting benchmarking, plus a secondary practical-identifiability analysis.
- **Why should BMB care?** It addresses how additional mathematical flexibility in a biological dynamical model should be evaluated before predictive value is inferred.
- **Article type?** Original Research.
- **Understandable from title/abstract?** Yes, with moderate contribution-threshold risk.

**Desk-reject surface risk**: **MEDIUM**, driven by editorial priority / generality rather than formal framing.

No scientific expansion is recommended to reduce this risk. The current single-case evidence should remain explicitly bounded.

---

## 4. Current formal requirements verified

| Requirement | Official BMB requirement | Package status |
|---|---|---|
| Editable source files | Required; LaTeX encouraged/recommended and Word accepted | PENDING FINAL PRODUCTION |
| PDF compiled output | Required for LaTeX submission | PENDING FINAL PRODUCTION |
| Title | Concise/informative | PRESENT; final author review pending |
| Authors | Names required | BLOCKED — HUMAN INPUT |
| Affiliations | Institution/(department), city, country | BLOCKED — HUMAN INPUT |
| Corresponding author | Clear designation + active email | BLOCKED — HUMAN INPUT |
| ORCID | If available / recommended | OPTIONAL/PENDING |
| LLM authorship | LLMs cannot be authors | PASS |
| LLM use disclosure | Generative LLM use should be documented in Methods | PASS — Methods §2.13 |
| Abstract | 150–250 words | PASS — approximately 208 words |
| Keywords | 4–6 | PASS — 6 |
| Declarations | Relevant statements required; incomplete submissions returned | PARTIAL — human confirmations pending |
| Funding | Must be disclosed | BLOCKED — HUMAN INPUT |
| Competing interests | Required disclosure | BLOCKED — HUMAN INPUT |
| Author contributions | Recommended/expected for research transparency; included among declaration summary items | BLOCKED — HUMAN INPUT |
| Ethics/consent | Include as applicable | BLOCKED — HUMAN/INSTITUTIONAL CONFIRMATION |
| Data Availability | Required for original research | DRAFT COMPLETE; provenance/access confirmation pending |
| Code Availability | Include as applicable | DRAFT COMPLETE |
| References | Author-year; alphabetized; DOI links when available | CONTENT AUDIT PASS; final style conversion pending |
| Tables/figures | Consecutive citation/numbering; captions required | CONTENT PACKAGE PASS; final insertion/production pending |
| Figure accessibility | Descriptive captions; patterns in addition to colors; contrast | CAPTION PASS; visual accessibility production check pending |
| Supplementary material | Standard formats; spreadsheets may be CSV/XLSX | CONTENT INVENTORY COMPLETE; final files/labels pending |
| Line numbering | Continuous | PENDING FINAL PRODUCTION |
| Page numbering | Sequential | PENDING FINAL PRODUCTION |

---

## 5. Data-policy gate

BMB requires a Data Availability Statement for all original research and strongly encourages public deposition of supporting data. The statement must explain how supporting data can be accessed. Public sharing is encouraged but the journal wording does not, for this data type, establish a universal mandatory-public-deposition requirement.

Current repository facts:

- canonical observational file: `data/raw/tb_mes.xlsx`;
- supplied by Amaury de Souza for the collaboration;
- repository provenance and hash recorded;
- original governmental download URL/acquisition route is **not independently recorded** in the supplied repository materials;
- repository is private;
- reviewer access or a reproducible bundle can be provided;
- no public archival DOI currently exists.

### Required human decision before submission

The authors must confirm one of the following evidence-backed paths:

1. provide and verify the original public acquisition source/URL and confirm redistribution rights; or
2. retain the repository-truthful statement that the supplied source file is available to editors/reviewers through controlled repository/bundle access, with any reuse conditions stated accurately.

Do **not** infer a SINAN/DATASUS download route merely from subject matter or secondary references.

**Data-policy status**: `BLOCKED_FOR_AUTHOR_PROVENANCE_AND_ACCESS_CONFIRMATION`.

---

## 6. Policy and declarations gate

Human confirmation remains mandatory for:

- final author identities and order;
- affiliations;
- corresponding author and active institutional email;
- author contributions / CRediT mapping;
- funding;
- financial and non-financial competing interests;
- ethics/consent applicability wording;
- data provenance/access route.

These are not inferable from the repository and must not be filled by AI assumption.

---

## 7. Production gate

After human metadata and declarations are closed:

1. generate the Springer Nature LaTeX source/package;
2. insert main figures/tables and supplementary references in consecutive order;
3. apply claim-safe captions from `BMB_FIGURE_TABLE_PACKAGE.md`;
4. convert references to final BMB author-year style and alphabetic order;
5. add continuous line numbering and sequential page numbering;
6. compile PDF;
7. run visual QA for equations, figures, tables, captions, page breaks, and cross-references;
8. verify all source files and supplementary files are present.

No new numerical analysis is authorized during production.

---

## 8. Gate decision

```text
FORMAL_GATE = BLOCKED_BY_HUMAN_METADATA_AND_FINAL_PRODUCTION
POLICY_GATE = BLOCKED_BY_HUMAN_DECLARATIONS_AND_DATA_PROVENANCE_CONFIRMATION
SCOPE_GATE = PASS_PLAUSIBLE
CONTRIBUTION_THRESHOLD_GATE = MEDIUM_RISK
EVIDENCE_GATE = PASS_BOUNDED
PROBLEM_AND_FRAMING_GATE = PASS
EXECUTION_AND_CONTEXT_GATE = PASS_PENDING_FINAL_PRODUCTION_QA

SCIENTIFIC_REPAIR_REQUIRED = NO
NEW_EXPERIMENT_REQUIRED = NO
JOURNAL_REROUTING_REQUIRED = NO
READY_FOR_AUTHOR_SCIENTIFIC_REVIEW = YES
READY_FOR_SUBMISSION = NO
```

**Next gate**: human author review and completion of metadata/declarations/data-access confirmation, followed by final LaTeX/PDF production QA.
