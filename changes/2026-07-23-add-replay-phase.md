---
change: "add-replay-phase"
status: "confirmed"
roadmap: "Phase 1: Govern one AI-feature launch request"
---

# Change Record - Add the fresh-context replay phase

## Intent and first human confirmation

**Observable outcome:** the Roadmap remains current at the unchanged Phase 1 product capability and
adds one human-authorized planned phase for a public-docs-only fresh replay, preventing future
Roadmap exhaustion before feature implementation begins.

**Initial human confirmation:** `confirmed on 2026-07-23 by explicit delegated human command`

This records an attestation of the command; it does not authenticate identity.

## Scope

- Record the prior human decision to add one didactic reproducibility phase after Phase 1.
- Preserve the exact Phase 1 launch-approval outcome, including feature, API, trusted-header,
  integration-test CI, and layered public documentation evidence.
- Add planned Phase 2 for an uninvolved fresh agent to reconstruct THIN inception and the same
  feature from an empty disposable local repository using only public documentation.
- Prove Roadmap selection, strategy authorization, provenance, Change Record shape, review
  readiness, expected merge boundary, documentation hygiene, and repository hygiene.

## Out of scope

- Product code, product behavior, feature design, architecture companions, product tests, a second
  cloud repository, a second merge, deployment, operations, or production-readiness claims.
- Mission or Constraints changes, new product semantics, new dependencies, Roadmap delivery
  movement, Phase 1 completion, Phase 2 execution, independent final review, or merge.

## Confirmed decisions

- **Correction radius:** `governance/strategy`; adding a Roadmap phase is a human-gated strategy
  change, while Mission, Constraints, dependencies, and product semantics remain unchanged.
- **Trigger:** `roadmap-exhausted / cycle-boundary`; completing the only current phase would
  otherwise leave the confirmed replay without a governed Roadmap anchor.
- **Path:** direct upstream adjustment through ADR-03 and the Roadmap; do not embed replay in Phase 1
  and do not weaken readiness.
- **Phase boundary:** Phase 1 remains current and semantically unchanged; Phase 2 is planned,
  unchecked, and limited to measured fresh-context reproducibility.
- **Product applicability:** all active product constraints remain binding for future product work,
  but none is activated here because this correction changes no product behavior.
- **Architecture judgment:** no load-bearing product or method design is introduced, so no design
  companion or architecture review is triggered.

## Activated proof obligations

| Constraint | Why activated | Expected evidence | Initial state |
|---|---|---|---|
| `FUN-CHANGE-01` | This governance correction requires exactly one confirmed dated Change Record. | Branch gate passes with this single record and no legacy `specs/` change. | pending |
| `FUN-ROADMAP-01` | The Roadmap gains one planned phase while Phase 1 must remain the exact current anchor. | Readiness passes and the selector returns exact Phase 1. | pending |
| `NFR-DOCS-01` | The correction modifies tracked public Markdown. | Documentation gate reports UTF-8 without BOM, CRLF, and balanced fences. | pending |
| `FUN-MERGE-01` | The branch must stop before independent final review and human merge authorization. | Review pre-check passes; merge readiness blocks only on confirmed status and pending verdict. | pending |
| `FUN-ARCHREVIEW-01` | The universal baseline requires an explicit architecture-trigger judgment. | Record, diff, and pre-check confirm no load-bearing design or companion was introduced. | pending |
| `FUN-AUTONOMY-01` | Adding a strategic phase is human-gated even though no Mission or Constraints file changes. | ADR-03 records the delegated decision and the autonomy gate passes against `origin/main`. | pending |

## Short implementation plan

1. Add ADR-03 and update only the Roadmap within the constitution, preserving Phase 1 semantics.
2. Run documentation, readiness, exact current-phase, autonomy, provenance, Change Record, diff,
   and cache checks.
3. Record evidence, corrections, deterministic changelog, and closeout without marking either phase
   delivered.
4. Pass the review pre-check, prove the expected confirmed/pending merge boundary, then commit, push,
   and open draft PR 4 for later independent review and human merge.

## Evidence

| Constraint | Result | Evidence |
|---|---|---|
| `FUN-CHANGE-01` | pending | Change Record gate and branch-diff hygiene have not yet been recorded. |
| `FUN-ROADMAP-01` | pending | Readiness and exact current-phase selection have not yet been recorded. |
| `NFR-DOCS-01` | pending | Documentation byte and structure evidence has not yet been recorded. |
| `FUN-MERGE-01` | pending | Review pre-check and expected merge-ready boundary have not yet been recorded. |
| `FUN-ARCHREVIEW-01` | pending | No-trigger and no-companion evidence has not yet been recorded. |
| `FUN-AUTONOMY-01` | pending | Human-decision ADR and autonomy evidence have not yet been recorded. |

## Corrections

- **Governance/strategy correction:** add the human-confirmed replay outcome upstream before product
  implementation so completion of Phase 1 does not leave the Roadmap exhausted.
- No prior product requirement, design, implementation evidence, architecture review, or final
  review exists to invalidate. Mission, Constraints, active product laws, dependencies, and Phase 1
  semantics remain unchanged.

## Independent final review

**Returned verdict:** `pending`
