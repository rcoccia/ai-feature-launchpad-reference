# Fresh-context replay evidence

This is the public evidence summary for the disposable local reconstruction of AI Feature Launchpad.
It records reproducibility through the review-ready boundary; it does not claim final review, merge,
local Phase 2 implementation, or Phase 2 completion.

## Provenance and boundary

- Public documentation source advanced append-only through
  `a29b507bd435f3128ad637c312aaf23ce947ca8d` ->
  `c77afc2cd745e86f3a6ef8e652a30da1f10e57a8` ->
  `3796075cdddbf5358f4ba3e0659aca81af83a1b8`.
- The final source pin contains merged product baseline
  `0a700178269acdf284c14c9033577857357c3dd3` in its ancestry.
- The no-remote disposable repository froze the final replay at
  `9c12fb06ce3f6589fee7183fdcdd49a15df602cf`.
- Total measured elapsed time was 109.27 minutes.
- The source evidence was `replay-report.md` plus Git metadata at that immutable local replay commit.
  The [canonical Phase 2 Change Record](../changes/2026-07-23-replay-launchpad-from-zero.md) preserves
  its public evidence and correction chain.

The replay started from an empty initialized repository, configured no Git remote, used no cloud
repository or pull request, and performed no final product review or merge. Questions used only the
parent message route; `ask_user` was never used.

## Reproducibility result

| Checkpoint | Evidence |
|---|---|
| LIGHT installation | The installer copied 56 files and preserved 0; it seeded neither constitution nor product. |
| THIN inception | Mission, Constraints, a two-phase Roadmap, and one inception ADR passed readiness; Phase 1 was current and Phase 2 planned. |
| Constraint model | Provenance resolved six inherited plus four product constraints, ten active constraints in total. |
| Governed slice | Exactly one confirmed Phase 1 Change Record existed before design or product code. |
| Architecture | The first design passed form and received `SOUND`; nested-JSON analysis exposed a design defect, so the design was corrected and received a fresh stable `SOUND`. |
| Product | The replay reconstructed the .NET 10 Minimal API, direct file-backed SQLite, locked dependencies, product CI, integration tests, and public product docs. |
| Product proof | Locked restore passed; Release build had zero warnings and errors; 28 tests passed with none failed or skipped; the transitive vulnerability scan found no vulnerable packages. |
| Governance proof | After truthful Phase 1 closeout, readiness stayed green, current selection returned exact `Phase 2: Reproduce inception and feature from a fresh context`, and Change Record, docs, autonomy, provenance, architecture-form, review-precheck, and diff checks passed. |
| Review-ready boundary | Merge readiness stopped only because the historical Phase 1 record remained `confirmed` with final verdict `pending`. |
| Hygiene | The immutable target contained 82 tracked files and no build, test, database, Python-cache, stash, or untracked residue. |

The 82 tracked files comprised 56 LIGHT files, four constitution artifacts, one Change Record, one
design companion, 18 product files, `CHANGELOG.md`, and the replay report.

## Rework and corrections

The first documentation source required only Phase 1 in the disposable Roadmap. Truthful Phase 1
closeout therefore exhausted the Roadmap and made the required final readiness/current/change gates
mutually impossible. Source `c77afc2cd745e86f3a6ef8e652a30da1f10e57a8` corrected the tutorial to
reproduce planned, unchecked Phase 2. The historical Phase 1 record then remained valid while the
selector advanced to Phase 2.

The first local implementation also returned flattened internal request state and a bare audit array.
Comparison with the allowed public API document exposed missing nested DTOs and per-decision
timestamps. The design was corrected and independently challenged again before product correction.
Source `3796075cdddbf5358f4ba3e0659aca81af83a1b8` then made the nested request/audit examples,
decision `recordedAtUtc`, and event `occurredAtUtc` unmistakable field-by-field reconstruction input.
The final source advance required evidence updates only because the corrected local design,
implementation, and contract tests already matched that public contract.

## Result boundary

The final public documentation was reproducible to the required all-green local review-ready
boundary. The disposable replay did not implement or close Phase 2 and created no second Change
Record, remote repository, final-review verdict, or merge. Phase 2 remains current and unchecked in
the public reference.
