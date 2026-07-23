---
change: "complete-launchpad-reference"
status: "confirmed"
roadmap: "Phase 2: Reproduce inception and feature from a fresh context"
---

# Change Record - Complete the reopenable Launchpad reference

## Intent and first human confirmation

**Observable outcome:** the finite AI Feature Launchpad reference records delivered Phase 1 and
successful Phase 2 replay/documentation evidence, then becomes intentionally complete with no current
approved work while retaining one human-governed atomic reopen path.

**Initial human confirmation:** `confirmed on 2026-07-23 by explicit delegated human command`

This records an attestation of the command; it does not authenticate identity.

## Roadmap lifecycle authorization

**ADR:** `constitution/decisions/ADR-20260723-04-complete-reopenable-reference.md`

## Scope

- Force-refresh the exact default LIGHT profile from Control Tower source commit
  `471071e213614ffd452d23865e30eda2f72c95d2` and prove selected inventory byte equality.
- Preserve all product-owned implementation, tests, workflows, API semantics, trust boundary, replay
  evidence, and public documentation except explicit lifecycle/current-state wording.
- Update inherited local pins for refreshed method assets and add only the three method-development
  laws mechanically required by the changed framework paths.
- Check Phase 2 with concise replay/docs/merge evidence, add exact top-level
  `**Lifecycle:** complete`, and publish the complete-but-reopenable current state.
- Prove complete readiness, blocking current-phase/planning behavior, product integrity, method
  regression evidence, deterministic closeout, and the expected pre-review merge boundary.

## Out of scope

- Product code, API behavior, authentication, dependencies, deployment, production claims, or a new
  product capability.
- Phase 3, speculative backlog, automatic reopening, archival, deletion, or a second replay.
- A design companion, new Architect decision, final Reviewer execution, merge-ready success, merge,
  or human merge authorization.
- Copied method ADRs, aliases, a hidden constraint registry, or weakening any gate.

## Activated proof obligations

| Constraint | Why activated | Expected evidence | Initial state |
|---|---|---|---|
| `FUN-CHANGE-01` | The terminal adoption requires exactly one confirmed governed record. | Branch gate resolves this sole dated record, exact Phase 2 anchor, confirmation, lifecycle ADR, evidence, corrections, and closeout. | pending |
| `FUN-ROADMAP-01` | Phase 2 closes and the Roadmap enters explicit complete state. | Same-diff accepted ADR, checked Phase 2, exact marker, readiness PASS, and actionable planning/current-phase blocks. | pending |
| `NFR-DOCS-01` | Method sync and current-state closeout modify tracked Markdown. | Documentation gate proves UTF-8, CRLF, and balanced fences; semantic review preserves public boundary language. | pending |
| `FUN-MERGE-01` | The branch must stop at draft PR before final review and merge. | Review pre-check passes and merge readiness blocks only on confirmed/PENDING final review state. | pending |
| `FUN-ARCHREVIEW-01` | Refreshed paths carry an already promoted load-bearing lifecycle design. | Source commit and promoted method evidence remain SOUND; this adoption introduces no new design or companion. | pending |
| `FUN-AUTONOMY-01` | The active Constraints set changes under explicit human authorization. | Accepted ADR-04 plus autonomy gate success against `origin/main`. | pending |
| `TEC-STK-01` | The sync and closeout must preserve the approved .NET 10 Minimal API and SQLite surface. | Locked restore/build/tests and source diff show no product implementation or dependency change. | pending |
| `TEC-IDB-01` | Public current-state wording must preserve the conspicuous non-production identity boundary. | Product tests and docs review retain trusted-header warnings and introduce no production auth claim. | pending |
| `FUN-APR-01` | Terminal governance edits must not alter launch approval or audit invariants. | All integration tests pass and product source remains unchanged. | pending |
| `NFR-CI-01` | Existing product-native CI must remain intact and green. | Product workflow is preserved and draft PR checks report successful build/test evidence. | pending |
| `FUN-DETERMINISM-01` | The refreshed lifecycle contract adds mechanically decidable completion and reopen checks. | Synced scripts contain enforcement; focused/full method tests and lifecycle field proofs pass. | pending |
| `NFR-EVAL-01` | Changed framework paths carry new must-pass/must-block lifecycle cases. | Upstream full eval/regression/verification plus every locally available LIGHT check passes at the pinned source. | pending |
| `TEC-DOMAIN-01` | The copied method lifecycle must remain portable rather than Launchpad-specific. | Byte equality with the promoted source and semantic review show domain-neutral method assets. | pending |

## Short implementation plan

1. Sync the exact default LIGHT profile and prove source inventory and byte equality.
2. Update local constraint pins, add the three required method-development laws, and record ADR-04.
3. Apply terminal Roadmap closeout and only the public lifecycle/evidence wording required by it.
4. Run full product, method, lifecycle, provenance, documentation, and review-boundary validation.
5. Record actual evidence, corrections, and closeout; commit logical changes, push, and open draft PR 6.

## Evidence

| Constraint | Result | Evidence |
|---|---|---|
| `FUN-CHANGE-01` | pending | Governed branch validation has not yet been recorded. |
| `FUN-ROADMAP-01` | pending | Terminal Roadmap and lifecycle CLI evidence have not yet been recorded. |
| `NFR-DOCS-01` | pending | Documentation validation has not yet been recorded. |
| `FUN-MERGE-01` | pending | Review pre-check and expected merge block have not yet been recorded. |
| `FUN-ARCHREVIEW-01` | pending | Promoted source design evidence has not yet been recorded. |
| `FUN-AUTONOMY-01` | pending | Autonomy validation has not yet been recorded. |
| `TEC-STK-01` | pending | Product build/test evidence has not yet been recorded. |
| `TEC-IDB-01` | pending | Identity-boundary preservation evidence has not yet been recorded. |
| `FUN-APR-01` | pending | Approval/audit invariant evidence has not yet been recorded. |
| `NFR-CI-01` | pending | Product CI preservation evidence has not yet been recorded. |
| `FUN-DETERMINISM-01` | pending | Deterministic lifecycle enforcement evidence has not yet been recorded. |
| `NFR-EVAL-01` | pending | Method eval/regression evidence has not yet been recorded. |
| `TEC-DOMAIN-01` | pending | Domain-neutral byte-equality evidence has not yet been recorded. |
| `FUN-CHANGE-01` | pass | `python -B framework/scripts/check_change_record.py --base origin/main` passes with exactly this one dated record, exact Phase 2 anchor, confirmed attestation, same-diff accepted ADR-04, and terminal lifecycle authorization. |
| `FUN-ROADMAP-01` | pass | `--check` reports `valid constitution shape: constitution`; deterministic readiness exits 0 with exact `constitution ready: Roadmap lifecycle complete; no current approved work: constitution`. `--current-phase` exits 1 with empty stdout and the exact actionable human-reopen diagnostic. A plan-slice selector proof left the dated-record count unchanged at 5. |
| `NFR-DOCS-01` | pass | `python -B framework/scripts/check_docs.py` passes all 60 tracked Markdown files. Current-state edits preserve the non-production warning and distinguish public Phase 2 adoption from the replay repository's intentionally unchecked local Phase 2. |
| `FUN-MERGE-01` | pass | `review_slice.py` pre-check passes. `check_merge_ready.py --base origin/main` exits 1 only because status is `confirmed` rather than `reviewed` and the final returned verdict is `PENDING`. No Reviewer or merge is performed by this producer. |
| `FUN-ARCHREVIEW-01` | pass | This adopter introduces no new design. Promoted source Change Record `changes/2026-07-23-reopenable-roadmap-completion.md` retains the prior stable `SOUND` architecture challenge at design target `7cac934122beb59f81a165fbe51a0ee590625c17`; this branch copies only the promoted LIGHT result. |
| `FUN-AUTONOMY-01` | pass | `python -B framework/scripts/check_autonomy.py --base origin/main` passes against newly accepted ADR-04 and the recorded delegated human command without claiming authenticated identity. |
| `TEC-STK-01` | pass | Locked restore and Release build pass with 0 warnings and 0 errors; all 28 integration tests pass. The branch diff contains no `src/`, `tests/`, project, solution, or lock-file change. |
| `TEC-IDB-01` | pass | All 28 product tests pass, no auth code changes, and README retains the first-line conspicuous non-production trusted-header warning. |
| `FUN-APR-01` | pass | All 28 approval, rejection, audit, persistence, concurrency, and refusal integration cases pass; product implementation is byte-unchanged from `origin/main`. |
| `NFR-CI-01` | pass | `.github/workflows/product-ci.yml` is unchanged; the same locked restore, Release build, and test commands pass locally, and merged PR 5 reports all six non-merge checks successful. |
| `FUN-DETERMINISM-01` | pass | Exact-source focused tests pass 47/47. Complete readiness/current behavior, same-diff closeout authorization, and atomic reopen remain enforced in the copied analyzer and Change Record gate rather than prose only. |
| `NFR-EVAL-01` | pass | From exact source checkout `471071e213614ffd452d23865e30eda2f72c95d2`, the full harness classifies 71/71 cases correctly at `1.00`; regression, verification, and four-agent checks pass; adoption/bootstrap tests pass 7/7 with LIGHT 56 and Full 201 field evidence. |
| `TEC-DOMAIN-01` | pass | The default LIGHT installer reports 56 copied and 0 preserved. SHA-256 comparison reports 0/56 mismatches against exact source HEAD `471071e213614ffd452d23865e30eda2f72c95d2`; only product-owned governance/evidence files contain Launchpad semantics. |

### Method sync inventory

The historical product pin remains `eef68510e89bee1d16b0425dbc71c603e3e35c96`; this governed
refresh pins exact Control Tower source `471071e213614ffd452d23865e30eda2f72c95d2`. The default
LIGHT installer copied 56 tracked files, preserved 0, and deleted nothing. Direct SHA-256 comparison
after commit found 56 equal and 0 mismatched:

```text
.gitattributes
.github/agents/architect-agent.agent.md
.github/agents/README.md
.github/agents/reviewer-agent.agent.md
.github/copilot-instructions.md
.github/skills/architecture-review/scripts/check_architecture.py
.github/skills/architecture-review/SKILL.md
.github/skills/bootstrap-tower/assets/constraints.md
.github/skills/bootstrap-tower/assets/mission.md
.github/skills/bootstrap-tower/assets/roadmap.md
.github/skills/bootstrap-tower/scripts/scaffold_constitution.py
.github/skills/bootstrap-tower/SKILL.md
.github/skills/inception-readiness/SKILL.md
.github/skills/plan-slice/SKILL.md
.github/skills/README.md
.github/skills/record-closeout/scripts/changelog.py
.github/skills/record-closeout/SKILL.md
.github/skills/replan-and-correct/SKILL.md
.github/skills/review-slice/scripts/review_slice.py
.github/skills/review-slice/SKILL.md
.github/workflows/autonomy.yml
.github/workflows/docs.yml
.github/workflows/merge.yml
.github/workflows/provenance.yml
AGENTS.md
CLAUDE.md
framework/adoption/install.md
framework/adoption/quickstart.md
framework/adoption/scripts/bootstrap.ps1
framework/contracts/change-record.md
framework/docs/explanation/extending-safely.md
framework/docs/explanation/overview.md
framework/docs/how-to/course-correct.md
framework/docs/how-to/govern-inception.md
framework/docs/how-to/review-a-design.md
framework/docs/how-to/run-a-slice.md
framework/docs/README.md
framework/docs/reference/agents.md
framework/docs/reference/constraints.md
framework/docs/reference/decisions.md
framework/docs/reference/gates.md
framework/docs/reference/glossary.md
framework/docs/reference/skills.md
framework/docs/tutorials/first-delivery.md
framework/doctrine/artifacts-skills-lifecycle.md
framework/doctrine/glossary.md
framework/doctrine/lineage.md
framework/doctrine/MANIFESTO.md
framework/doctrine/operating-model.md
framework/scripts/change_record.py
framework/scripts/check_autonomy.py
framework/scripts/check_change_record.py
framework/scripts/check_docs.py
framework/scripts/check_merge_ready.py
framework/scripts/check_provenance.py
framework/scripts/constraint_model.py
```

Twenty copied paths changed relative to `origin/main`: `.github/copilot-instructions.md`;
bootstrap-tower `SKILL.md`, constraints/roadmap assets, and analyzer; inception-readiness,
plan-slice, record-closeout, and replan-and-correct Skills; the Change Record contract; seven
framework guidance/doctrine documents; and `framework/scripts/change_record.py` plus
`framework/scripts/check_change_record.py`. All other copied paths were byte-identical already.

## Corrections

- **ADR shape correction:** the first recorded ADR status used a prose heading. The promoted gate
  required exact `- **status:** accepted`; ADR-04 was corrected before terminal validation, with no
  decision or scope change.
- **Eval invocation correction:** the first full eval attempt launched the absolute source script
  while retaining the adopter working directory. Root-relative provenance fixture resolution
  therefore misclassified only `provenance/good` and reported 70/71. Rerunning from exact source
  checkout root passed 71/71 at `1.00`; no source, fixture, gate, or product file changed.
- No product defect, lifecycle-contract defect, architecture rework, gate weakening, or constraint
  decoration was required.

## Closeout

| Disposition | Record |
|---|---|
| delivered | Exact 56-file LIGHT refresh from `471071e`; 13 locally reproducible active constraints; checked Phase 2 replay/docs evidence; exact complete lifecycle marker; complete/no-current CLI behavior; and current public documentation. |
| remaining | Independent final review, returned-verdict recording, transition to reviewed, merge-ready success, and human merge authorization remain intentionally outside this producer scope. No approved product or Roadmap work remains. |
| discovered | The first source eval invocation must run from the source checkout root because provenance golden references are root-relative; corrected execution passed all 71 cases. |
| evidence | Roadmap Delta links replay `9c12fb06ce3f6589fee7183fdcdd49a15df602cf`, public replay evidence, PR 5 merge `2def9df0dcbf8fc48e7e2b7ada2a9c6b7cf206d4`, and PR 3 product proof. `CHANGELOG.md` deterministically advances through evidence commit `c8d587202f9e6b51e0bc3f67dcee919e0729d0bd`. |

## Independent final review

**Returned verdict:** `pending`
