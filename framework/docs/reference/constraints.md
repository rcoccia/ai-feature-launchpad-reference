# Reference — Constraints

A project's normative constraints live in
[`constitution/constraints.md`](../../../constitution/constraints.md) after inception. This page
explains the contract. Every adopter constitution includes five portable Control Tower baseline
constraints required by the installed kernel, plus its own elicited product constraints.

## Portable inherited baseline

| Constraint | Why it is always present |
|---|---|
| `FUN-CHANGE-01` | Every governed change needs the canonical dated Change Record contract. |
| `FUN-ROADMAP-01` | Readiness and planning share the canonical Roadmap selector. |
| `NFR-DOCS-01` | Tracked Markdown must satisfy the installed documentation gate. |
| `FUN-MERGE-01` | Every PR retains independent final review and human merge authorization. |
| `FUN-ARCHREVIEW-01` | A later load-bearing design must be able to activate the installed architecture path without inventing or aliasing a constraint ID. |

These are method laws, not product features, so they do not count toward the rough 3-6 elicited
product constraints used as THIN inception guidance. Their complete blocks live in the bootstrap
Constraints asset and pin copied local method surfaces. `FUN-ARCHREVIEW-01` is present in every
constitution but becomes a Change Record proof obligation only when architecture is triggered.

## What a constraint records

Each constraint declares:

- a stable `constraint.id`, category, statement, source, severity, and active status;
- pinned local references for non-stakeholder authority;
- a deterministic Gate projection or a review-routed residual for every hard constraint;
- a measurable metric when the property is quantitative.

A hard constraint activated for a change appears as a proof obligation in the canonical Change
Record with its reason, expected evidence, and actual result. The universal Change Record baseline
activates four inherited constraints; explicit risk/impact triggers add obligations, including
`FUN-ARCHREVIEW-01` when load-bearing architecture is present. Applicability and completeness remain
Tower/human/reviewer judgments except where a deterministic gate can prove a trigger with certainty.

## Where enforcement lives

Deterministic properties belong in [Gates](gates.md), not only in prose. LIGHT installs the
docs/readiness, autonomy, provenance, and merge-ready workflow path plus the pre-checks carried by
its lifecycle Skills. Full additionally installs framework-development eval, agent, verification,
and regression checks.

Canonical Roadmap lifecycle is one such hard property: `scaffold_constitution.py` validates every
`## Phase`, derives delivered/current/planned/deferred state, selects current for readiness and
planning, and blocks exhaustion. A review residual remains necessary because syntax cannot prove
that a human's deferral decision is authorized, wise, or current.

Design-level constraints remain binding even when no honest script can decide them. The independent
Reviewer records the required residual disposition, and the human retains strategy, ambiguity,
authenticity, and merge judgment.

## See also

- [Gate catalog and profile availability](gates.md)
- [Decision record contract](decisions.md)
- [Run a slice](../how-to/run-a-slice.md)
