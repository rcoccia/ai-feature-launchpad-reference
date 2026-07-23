# ADR-20260723-02: Adopt kernel baseline constraints

## Status

Accepted on 2026-07-23 through an explicit delegated human command. This records an attestation of
the command; it does not authenticate identity.

## Trigger

A `new common consumer` and `gap-in-coding` finding exposed a governance/strategy correction:
the active constraint set did not name the exact portable obligations required by the installed
Change Record kernel.

## Context

Inception commit `374678b37af3ae05b08c9b438d5a85c4370bdcef` adopted the default Control
Tower LIGHT profile from source commit `eef68510e89bee1d16b0425dbc71c603e3e35c96`. That historical
source copied 56 tracked assets and the resulting constitution passed the then-current readiness
gate. Its product constraint `FUN-GOV-01` compressed inherited lifecycle expectations into one
aggregate law.

Control Tower first corrected the fresh-adopter mismatch in merged source commit
`ff77efa7d7983b2eabde9baccf1d35e38c4692fb`. Product correction commit
`d7c57220b5bd4850672a95d68426ad2c795974cb` attempted a force-refresh from that source. The
attempt proved all 56 selected files byte-identical, but the product Change Record gate then
correctly treated changed method-owned Python and framework paths as method development and required
four non-portable method obligations. That made a full kit refresh the wrong correction boundary for
an intentionally pinned public adopter.

The attempted refresh was therefore reverted path-by-path in a later corrective commit without
rewriting history. The public repository remains on the 56-file LIGHT kit adopted from
`eef68510e89bee1d16b0425dbc71c603e3e35c96`; its `.github/` and `framework/` assets remain
byte-identical to `origin/main`.

Control Tower then corrected the remaining strategy-correction gap in merged source commit
`08c481f5afaf2c8ae196812c00f003b10190bda3`. Together, PR 57 and PR 58 are external field-feedback
evidence; neither method commit is installed into this repository. The resulting portable baseline
IDs are `FUN-CHANGE-01`, `FUN-ROADMAP-01`, `NFR-DOCS-01`, `FUN-MERGE-01`,
`FUN-ARCHREVIEW-01`, and `FUN-AUTONOMY-01`. The current product `NFR-DOCS-01` already supplies the
documentation ID. Keeping `FUN-GOV-01` beside the exact inherited obligations would add redundant,
less precise governance semantics.

## Decision

Adopt the five missing portable Control Tower constraint definitions established by the external
method corrections, but pin each definition to the corresponding normative file already present in
the original local LIGHT kit. Retain the existing product `NFR-DOCS-01` as both a product law and
the sixth required baseline ID. Supersede the
aggregate `FUN-GOV-01` by removing it from the active constraint set; Git history and this ADR retain
the historical decision.

The active constitution therefore contains ten constraints: the five newly named inherited laws,
the existing `NFR-DOCS-01` baseline/product law, and the four other unchanged product laws. Mission,
Roadmap semantics, product behavior, product architecture, and product code do not change.

## Alternatives considered

1. Keep `FUN-GOV-01` and add the exact inherited IDs. Rejected because the aggregate would be
   redundant and would leave eleven active constraints without adding a distinct law.
2. Teach the gate an alias from `FUN-GOV-01` to the exact IDs. Rejected because that would weaken the
   explicit kernel contract and hide the missing obligations rather than correct the upstream
   artifact.
3. Refresh the complete LIGHT kit from PR 57 or PR 58. Rejected after the recorded attempt because
   method-owned path changes activate method-development obligations in the product branch.
4. Copy Control Tower method ADRs into the product repository. Rejected because the portable
   definitions intentionally pin copied local contracts, doctrine, Skills, and Gates.

## Consequences

The first governed Change Record can resolve every exact obligation required by the pinned local
kernel, including `FUN-AUTONOMY-01` for a Constraints correction. The pinned readiness script
predates the six-ID rule, so a passing local readiness result proves shape and the older checks, not
the new six-ID completeness; the active set and provenance evidence establish that completeness.
Future load-bearing designs can activate `FUN-ARCHREVIEW-01`; ordinary changes leave it inactive.

The initial `eef68510e89bee1d16b0425dbc71c603e3e35c96` source pin remains immutable historical
inception evidence and the source of the current 56-file LIGHT inventory. Method commits
`ff77efa7d7983b2eabde9baccf1d35e38c4692fb` and
`08c481f5afaf2c8ae196812c00f003b10190bda3` remain external correction evidence. Independent
semantic readiness, independent final review, and human merge authorization remain separate pending
judgments.
