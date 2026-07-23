---
change: "adopt-kernel-baseline-constraints"
status: "confirmed"
roadmap: "Phase 1: Govern one AI-feature launch request"
---

# Change Record - Adopt kernel baseline constraints

## Intent and first human confirmation

**Observable outcome:** the product constitution on its original `eef6851`-pinned LIGHT kit exposes
the exact six portable Control Tower baseline IDs with locally resolvable normative pins, so the
first product Change Record no longer fails on aggregate `FUN-GOV-01`.

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
| `FUN-AUTONOMY-01` | The active Constraints set changes under an explicitly delegated human decision. | The autonomy gate passes because ADR-02 records the strategy correction. | pending |

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
- **Correction cycle 1:** commit `d7c57220b5bd4850672a95d68426ad2c795974cb` attempted the
  originally confirmed 56-file refresh from external method commit `ff77efa7d7983b2eabde9baccf1d35e38c4692fb`.
  The Change Record gate exposed second-order method-development obligations because the product
  branch then changed method-owned Python and framework paths. The parent selected the wider upstream
  boundary rather than adding decorative product constraints or weakening the gate.
- External method commit `08c481f5afaf2c8ae196812c00f003b10190bda3` completed the six-ID
  portable model. This product branch adopts only the locally pinned `FUN-AUTONOMY-01` definition.
  A normal follow-up corrective commit restores these eight refresh-only paths exactly to
  `origin/main`: `.github/skills/bootstrap-tower/SKILL.md`,
  `.github/skills/bootstrap-tower/assets/constraints.md`,
  `.github/skills/bootstrap-tower/scripts/scaffold_constitution.py`,
  `.github/skills/inception-readiness/SKILL.md`, `framework/contracts/change-record.md`,
  `framework/docs/how-to/govern-inception.md`, `framework/docs/reference/constraints.md`, and
  `framework/docs/reference/gates.md`.
- The original confirmed Scope and Short implementation plan remain above as the historical first
  plan. This append-only correction records why the refresh step was reversed and why the observable
  product outcome is now achieved without installing either external method correction.
- No prior product Change Record, architecture review, implementation evidence, or final review
  existed to invalidate. Mission, Roadmap semantics, and product laws other than removal of the
  redundant governance aggregate remain unchanged.

## Independent final review

**Returned verdict:** `pending`
