# ADR-20260723-01: Authorize AI Feature Launchpad inception

## Status

Accepted on 2026-07-23 by the human stakeholder.

## Trigger

The public `rcoccia/ai-feature-launchpad-reference` repository required a human-authorized,
traceable inception before any product slice could be planned or implemented.

## Context

The repository began with its product-owned README and MIT license. Control Tower LIGHT was adopted
from the local source checkout at
`C:\Users\rcoccia\source\repos\copilot-worktrees\control-tower\rcoccia-congenial-potato`, pinned at
full commit `eef68510e89bee1d16b0425dbc71c603e3e35c96`. The default `Light` profile copied exactly 56
tracked assets, preserved the existing product files, and seeded no constitution.

The stakeholder confirmed a synthetic enterprise reference named AI Feature Launchpad for internal
enterprise product teams submitting AI-enabled features for governed launch. The first observable
capability starts a request Pending, requires distinct Product and AI-Risk approvers who are each
distinct from the requester, makes authorized rejection terminal, records append-only audit evidence
for every successful or refused attempt, and persists request state and audit history in SQLite.

The confirmed product surface is .NET 10 ASP.NET Core Minimal API, SQLite, product-native GitHub
Actions CI, and integration tests. Identity uses trusted-upstream headers only inside a conspicuously
non-production reference-local/test boundary; OAuth, JWT, and a real identity provider are excluded.
The reference proves and teaches complete Control Tower intent-to-merge evidence. Release,
deployment, and operations are evidence boundaries only.

## Decision

Authorize the thin Mission, Constraints, and Roadmap for AI Feature Launchpad with one current phase:
the governed launch-approval capability. Adopt the pinned Control Tower LIGHT lifecycle and its hard
governance as the repository's delivery method.

This inception does not authorize product code, a feature Change Record, an architecture choice for
transactions or schema, production authentication, deployment, an operations runtime, or a
production-ready claim. Those product design decisions may be considered only within an authorized
feature slice after independent inception readiness.

## Alternatives considered

1. Author product code or a detailed feature Change Record during inception. Rejected because it
   would collapse strategy into implementation and bypass independent readiness and slice planning.
2. Build a generic workflow, policy, identity, provider, or enterprise platform. Rejected because it
   would obscure the single observable capability and contradict the confirmed non-goals.
3. Adopt the full Control Tower profile. Rejected because LIGHT supplies the required lifecycle core
   while leaving product build, tests, and other product concerns product-native.

## Consequences

The repository now has a small, public governing constitution and one auditable authorization
decision tied to an exact Control Tower source pin and profile. Phase 1 can be selected
deterministically after parent-owned independent semantic inception readiness.

The negative trade-off is deliberate narrowness: the reference will not demonstrate production
identity, deployment, operations, generic policy composition, or speculative follow-on capabilities.
Future scope requires a new human decision instead of being inferred from this inception.
