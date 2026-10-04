# BMB documentary repair — 2026-10-04

Base reviewed: `3bf022267097848f11fab7ceb131207683b58fa8` (main).
Scope: documentary consistency only. No new experiments, model recalibration,
result recomputation, scientific framing change, or journal submission.

## Findings and repairs

- **B-1 — repaired:** `BMB_ABSTRACT.md` now reproduces the Abstract in
  `submission_bmb/BMB_MANUSCRIPT.md` verbatim (208 whitespace tokens, including
  inline mathematical tokens). The canonical Abstract is unchanged and explicitly
  treats identifiability as secondary. Historical packaging counts are labelled historical.
- **B-2 — already repaired in the reviewed base:** Table 1 is the six-row
  baseline/metric horizon summary. The caption describes horizon descriptors;
  horizon-wise forecast errors are explicitly assigned to Table S1. No table changed.
- **B-3 — repaired:** seven Markdown files incorrectly labelled the manuscript
  assembly commit as the computational freeze. They now identify the canonical
  evidence-freeze commit `5617559bb0bf43d7223a7bb2491ab1e41fa4a084`.
  `results_canonical/RESULT_SET_FREEZE.md` separately records the pre-freeze
  computational HEAD `cfec12a`; `8ba6ea2bac741ae17b05e9b397af4057585929dc`
  corrects a prose claim tally only. These identifiers have distinct roles.
- Availability copies now match the canonical manuscript's public repository
  wording. Author confirmations of redistribution/reuse conditions remain pending.

## Positive checks performed

- Canonical Abstract and submission Abstract: exact text equality.
- Canonical manuscript: only the freeze-label phrase changed; scientific text unchanged.
- No working-tree changes to `results_canonical/`, `data/`, `src/`, `outputs/`,
  `provenance/`, or `scripts/`.
- `src/`, `data/raw/`, and `outputs/` are identical between the evidence-freeze
  commit and the formerly cited assembly commit.
- Canonical raw dataset SHA-256 matches the recorded source hash.
- All seven obsolete assembly-commit citations removed from Markdown documentation.
- Table 1 caption matched to its canonical six-row horizon-summary schema.
- Existing integrity suite: `python -m pytest -q tests/test_canonical_freeze.py` — 15 passed.
- `git diff --check` — passed.

## Boundaries

The local Claude audit commit `bd4b744` was not available on the remote repository.
This repair addresses the same documentary findings against the current remote base;
it does not claim to modify the separate Mac clone or clean its worktrees.

READY_FOR_AUTHOR_SCIENTIFIC_REVIEW = YES (documentary B-1/B-2/B-3 closed here).
READY_FOR_SUBMISSION = NO.
Final author scientific review, author metadata, dataset reuse confirmation,
reference details, editable-source production and rendered-PDF QA remain open.

BMB remains the proposed destination; no novelty claim, journal-fit guarantee,
or independent scientific certification is added by this documentary repair.
