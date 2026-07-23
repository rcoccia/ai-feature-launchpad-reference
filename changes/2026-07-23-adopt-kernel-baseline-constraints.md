---
change: "adopt-kernel-baseline-constraints"
status: "confirmed"
roadmap: "Phase 1: Govern one AI-feature launch request"
---

# Change Record - Adopt kernel baseline constraints

## Intent and first human confirmation

**Observable outcome:** the refreshed LIGHT kernel and product constitution expose the exact five
portable Control Tower baseline IDs, with locally resolvable normative pins, so deterministic
readiness and the first product Change Record no longer fail on the aggregate `FUN-GOV-01`.

**Initial human confirmation:** `confirmed on 2026-07-23 by explicit delegated human command`

This records an attestation of the command; it does not authenticate identity.

## Scope

- Force-refresh the default 56-file LIGHT profile from exact Control Tower source commit
  `ff77efa7d7983b2eabde9baccf1d35e38c4692fb` and verify byte equality.
- Record the governance/strategy correction in one product ADR.
- Replace aggregate `FUN-GOV-01` with the four missing portable baseline blocks, reuse the existing
  product `NFR-DOCS-01`, and retain the other four product laws unchanged.
- Prove deterministic readiness, exact Phase 1 selection, autonomy, provenance, Change Record shape,
  review pre-check behavior, and documentation hygiene.

## Out of scope

- Product code, feature semantics, product build, feature Change Record, architecture or design
  companions, independent semantic readiness, independent final review, merge readiness success,
  merge, deployment, or operations.
- Mission or Roadmap semantic changes, gate weakening, aliases, copied method ADRs, external
  dependencies, or recreation of `specs/`.

## Confirmed decisions

- **Correction radius:** `governance/strategy`; the active Constraints set changes under the
  explicitly delegated command, while Mission, Roadmap outcome, dependencies, and product semantics
  remain unchanged.
- **Trigger:** `new common consumer` plus `gap-in-coding`; fresh inception passed before the exact
  installed-kernel baseline was enforced, but the first Change Record would fail.
- **Path:** direct upstream adjustment in copied kernel assets and the product Constraints artifact;
  never weaken a gate.
- **Architecture judgment:** no load-bearing product or method design is introduced, so
  `FUN-ARCHREVIEW-01` remains available but is not activated for this correction.

## Activated proof obligations

| Constraint | Why activated | Expected evidence | Initial state |
|---|---|---|---|
| `FUN-CHANGE-01` | This governance correction requires exactly one confirmed dated Change Record. | Branch gate passes with this single record and no `specs/` change. | pending |
| `FUN-ROADMAP-01` | The correction preserves the exact current Phase 1 anchor without changing Roadmap semantics. | Readiness passes and the selector returns exact Phase 1. | pending |
| `NFR-DOCS-01` | The refresh and correction modify tracked Markdown. | Documentation gate reports UTF-8 without BOM, CRLF, and balanced fences. | pending |
| `FUN-MERGE-01` | The branch must stop before parent-owned final review and merge. | Review pre-check passes; merge readiness blocks on confirmed status and pending verdict. | pending |

## Short implementation plan

1. Refresh the default LIGHT profile from the exact correction source and verify inventory, byte
   equality, and preservation boundaries.
2. Add the correction ADR and replace the aggregate constraint with four exact locally pinned
   portable blocks.
3. Run focused baseline, readiness, current-phase, autonomy, provenance, documentation, Change
   Record, review pre-check, merge-boundary, and repository-hygiene checks.
4. Record evidence, corrections, and closeout; commit, push, and open draft PR 2 with final review
   pending.

## Evidence

| Constraint | Result | Evidence |
|---|---|---|
| `FUN-CHANGE-01` | pending | Change Record gate and branch-diff hygiene have not yet been recorded. |
| `FUN-ROADMAP-01` | pending | Readiness and exact current-phase selection have not yet been recorded. |
| `NFR-DOCS-01` | pending | Documentation byte/structure evidence has not yet been recorded. |
| `FUN-MERGE-01` | pending | Review pre-check and expected merge-ready boundary have not yet been recorded. |

## Corrections

- **Governance/strategy correction:** exact inherited constraint IDs replace the aggregate
  `FUN-GOV-01`; the source pin, active constraint set, and durable decision are corrected upstream.
- The bootstrap refresh necessarily preceded creation of a gate-resolvable Change Record because the
  field finding was precisely that the prior constitution lacked the exact installed-kernel IDs.
  The explicit delegated command authorized this bounded pre-feature correction.
- No prior product Change Record, architecture review, implementation evidence, or final review
  existed to invalidate. Mission, Roadmap semantics, and product laws other than removal of the
  redundant governance aggregate remain unchanged.

## Independent final review

**Returned verdict:** `pending`
