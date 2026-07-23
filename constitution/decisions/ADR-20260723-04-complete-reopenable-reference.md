# ADR-20260723-04: Complete the reopenable Launchpad reference

- **id:** ADR-20260723-04
- **status:** accepted
- **date:** 2026-07-23
- **trigger:** `roadmap-exhausted / cycle-boundary`

Accepted on 2026-07-23 through an explicit delegated human command. This records an attestation of
the command; it does not authenticate identity.

## Trigger

The `roadmap-exhausted / cycle-boundary` trigger is reached: Phase 1 delivered the governed product,
and the separately authorized fresh-context replay and public evidence for Phase 2 have succeeded.

## Context

The reference adopted its original 56-file LIGHT kit from Control Tower commit
`eef68510e89bee1d16b0425dbc71c603e3e35c96`. Phase 1 was delivered and merged through PR 3. The
no-remote disposable replay froze successful review-ready reconstruction at
`9c12fb06ce3f6589fee7183fdcdd49a15df602cf`, and PR 5 merged the replay tutorial, operations, and
evidence documentation at `2def9df0dcbf8fc48e7e2b7ada2a9c6b7cf206d4`.

Control Tower commit `471071e213614ffd452d23865e30eda2f72c95d2` promotes the finite,
reopenable Roadmap lifecycle contract. Its default LIGHT installer provides deterministic complete,
current-phase, closeout, and reopen behavior without requiring a speculative next phase.

## Decision

Force-refresh this repository's exact default LIGHT inventory from source commit
`471071e213614ffd452d23865e30eda2f72c95d2`, preserving product-owned paths outside that inventory.
Update locally pinned inherited constraint definitions to the copied bytes and add only
`FUN-DETERMINISM-01`, `NFR-EVAL-01`, and `TEC-DOMAIN-01`, which are mechanically required because
this governed sync changes framework paths.

Mark Phase 2 delivered with concise evidence linking the immutable replay commit, the published
documentation, PR 5, and its merge commit. Add exact top-level `**Lifecycle:** complete`. In this
state the repository is intentionally complete and has no current approved work; it is neither
archived nor permanently closed.

A future requirement may reopen the Roadmap only through one human-authorized governed change that
adds a new accepted ADR, references it from the confirmed Change Record's
`## Roadmap lifecycle authorization` section, removes the lifecycle marker, and adds at least one new
non-deferred phase with an unchecked item atomically.

## Consequences

Readiness succeeds and explicitly reports complete/no current work. `--current-phase` and
`plan-slice` fail closed with an actionable human-reopen diagnostic and cannot create a new Change
Record. The historical Phase 1 and Phase 2 evidence remains inspectable and checked.

The active constraint set contains nine method laws and four unchanged product laws. Refreshed method
assets remain locally reproducible through pinned paths and hashes; no method ADR is copied or
aliased into this product repository.

## Non-decisions

This decision does not add Phase 3 or any speculative backlog, change product/API/authentication
semantics, add deployment or production scope, archive or delete the repository, authorize automatic
reopening, trigger a new architecture design, perform final review, or authorize merge.
