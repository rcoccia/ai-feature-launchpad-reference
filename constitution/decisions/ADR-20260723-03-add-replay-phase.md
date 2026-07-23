# ADR-20260723-03: Add the fresh-context replay phase

## Status

Accepted on 2026-07-23 through an explicit delegated human command. This records an attestation of
the command; it does not authenticate identity.

## Trigger

The `roadmap-exhausted / cycle-boundary` trigger is imminent: completing the current Phase 1 would
leave no governed phase for a later replay that the human has already confirmed.

## Context

The Roadmap currently contains only the launch-approval product capability. The human separately
confirmed a later reference outcome: an uninvolved fresh agent starts from an empty disposable local
repository, uses only public documentation, reconstructs THIN inception and the same feature without
parent history or `ask_user`, and reaches review-ready with required gates green.

That replay must record its steps, artifacts, latency, rework, defects, and friction. It does not
need a second cloud repository or merge because the main reference supplies the GitHub merge proof.
The outcome is didactic reproducibility evidence, not a new product capability.

## Decision

Add planned Phase 2, `Reproduce inception and feature from a fresh context`, after the unchanged
Phase 1 product capability. Phase 1 remains current and unchecked; Phase 2 remains planned and
unchecked until the product reference is ready to replay.

Keep the feature, API, trusted-header boundary, integration-test CI, and layered public
documentation in Phase 1 as product delivery evidence. Phase 2 consumes those public surfaces to
test reproducibility without adding product semantics, dependencies, architecture, or code.

Mission and Constraints do not change. This ADR durably records the prior human decision required
to add a strategic phase even though the deterministic autonomy gate only requires an ADR for
Mission or Constraints changes.

## Alternatives considered

1. Let Phase 1 complete with an exhausted Roadmap and plan the replay ad hoc. Rejected because work
   without a current Roadmap phase is governed drift.
2. Embed the replay in Phase 1. Rejected because that would mix product delivery with a later,
   fresh-context reproducibility judgment and obscure when the launch capability is complete.
3. Require a second cloud repository and merge. Rejected because the replay needs local
   reconstruction through review-ready; the main reference already proves GitHub merge.

## Consequences

Phase 1 remains the exact current product phase and its observable capability is semantically
unchanged. Once Phase 1 is delivered, the canonical selector can advance to the human-authorized
replay instead of failing on Roadmap exhaustion.

Phase 2 will produce measured didactic evidence about whether public documentation is sufficient
for fresh reconstruction. No product behavior is activated by this decision, and no product code,
design, reviewer verdict, or merge is authorized by this Change Record.
