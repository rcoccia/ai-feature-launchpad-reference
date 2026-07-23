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

Control Tower corrected the fresh-adopter mismatch in merged source commit
`ff77efa7d7983b2eabde9baccf1d35e38c4692fb`. The exact source checkout at that commit was used to
force-refresh the default LIGHT profile. It still contains 56 tracked assets. Every selected target
asset was verified byte-identical to the source, while the product README, LICENSE, and constitution
were unchanged by bootstrap.

The corrected kernel requires every ready constitution to contain `FUN-CHANGE-01`,
`FUN-ROADMAP-01`, `NFR-DOCS-01`, `FUN-MERGE-01`, and `FUN-ARCHREVIEW-01`. The current product
`NFR-DOCS-01` already supplies that exact documentation ID. Keeping `FUN-GOV-01` beside the exact
inherited obligations would add redundant, less precise governance semantics.

## Decision

Adopt the four missing portable Control Tower constraint blocks from the copied current Constraints
asset, including their locally resolvable normative paths and SHA-256 pins. Retain the existing
product `NFR-DOCS-01` as both a product law and the fifth required baseline ID. Supersede the
aggregate `FUN-GOV-01` by removing it from the active constraint set; Git history and this ADR retain
the historical decision.

The active constitution therefore contains nine constraints: the four newly named inherited laws,
the existing `NFR-DOCS-01` baseline/product law, and the four other unchanged product laws. Mission,
Roadmap semantics, product behavior, product architecture, and product code do not change.

## Alternatives considered

1. Keep `FUN-GOV-01` and add the exact inherited IDs. Rejected because the aggregate would be
   redundant and would leave ten active constraints without adding a distinct law.
2. Teach the gate an alias from `FUN-GOV-01` to the exact IDs. Rejected because that would weaken the
   explicit kernel contract and hide the missing obligations rather than correct the upstream
   artifact.
3. Copy Control Tower method ADRs into the product repository. Rejected because the portable
   definitions intentionally pin copied local contracts, doctrine, Skills, and Gates.

## Consequences

Readiness and the first governed Change Record can resolve every exact installed-kernel obligation
from this repository. Future load-bearing designs can activate `FUN-ARCHREVIEW-01`; ordinary changes
leave it inactive.

The initial `eef68510e89bee1d16b0425dbc71c603e3e35c96` source pin remains immutable historical
inception evidence. `ff77efa7d7983b2eabde9baccf1d35e38c4692fb` is the correction source for the
current 56-file LIGHT inventory. Independent semantic readiness, independent final review, and
human merge authorization remain separate pending judgments.
