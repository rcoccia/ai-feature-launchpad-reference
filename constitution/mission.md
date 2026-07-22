# Mission: AI Feature Launchpad

## Purpose / Vision

AI Feature Launchpad is a public synthetic-enterprise reference that proves and teaches the Control
Tower intent-to-merge method through one governed AI-feature launch journey. It gives internal
enterprise product teams a concrete example of turning confirmed product intent into reviewable,
auditable delivery evidence without presenting the reference as a production platform.

## Target users

The primary users are internal enterprise product teams submitting an AI-enabled feature for
governed launch. Contributors and reviewers also use the repository to learn how product intent,
constraints, decisions, implementation evidence, and merge governance remain traceable.

## Scope

The reference covers one observable launch-approval capability. A launch request begins Pending,
requires distinct Product and AI-Risk approvals from actors who are also distinct from the requester,
supports terminal rejection by an authorized actor, emits append-only audit evidence for every
successful or refused attempt, and persists state and audit history in SQLite.

The implementation surface is a .NET 10 ASP.NET Core Minimal API with a conspicuously
non-production, reference-local trusted-upstream-header identity boundary. Product-native GitHub
Actions and integration tests provide implementation evidence. Layered public documentation
connects the product capability to the Control Tower intent-to-merge lifecycle. Release, deployment,
and operations are evidence boundaries only.

## Success criteria

- An internal product team can follow the single launch-approval capability from confirmed intent
  through governed implementation and merge evidence.
- The capability observably enforces actor separation, terminal authorized rejection, durable state,
  and append-only audit evidence for successful and refused attempts.
- The public reference clearly teaches which artifacts and gates establish intent-to-merge evidence
  while identifying its identity boundary and the product as non-production.

## Non-goals / boundaries

The reference does not provide a generic workflow or policy engine, risk scoring, cloud deployment,
an operations runtime, provider abstraction, a generic enterprise platform, production
authentication, or a production-ready claim. OAuth, JWT, and a real identity provider are outside
the reference boundary. Unrelated product features and speculative later product phases are out of
scope.
