---
change: "govern-ai-feature-launch"
status: "confirmed"
roadmap: "Phase 1: Govern one AI-feature launch request"
---

# Change Record - Govern one AI-feature launch request

## Intent and first human confirmation

**Observable outcome:** an internal product team can submit and govern one AI-feature launch request
from Pending to an approved or terminally rejected outcome through a .NET 10 ASP.NET Core Minimal
API, with durable SQLite request and append-only audit state, enforced separation among requester,
Product approver, and AI-Risk approver, conspicuously non-production trusted-header identity,
integration-test evidence, product-native GitHub Actions CI, and accurate product documentation.

**Initial human confirmation:** `confirmed on 2026-07-23 by prior explicit human decisions and the delegated command to create this Phase 1 feature Change Record`

This records an attestation of the command; it does not authenticate identity.

## Governed facts and Tower judgment

- **Governed facts:** Mission and the exact current Roadmap Phase require one launch request to begin
  Pending, require Product and AI-Risk approvals by actors distinct from each other and the requester,
  make authorized rejection terminal, and require append-only audit evidence for every successful or
  refused attempt consistent with durable SQLite state.
- **Approved surface:** the product is a .NET 10 ASP.NET Core Minimal API with SQLite, integration
  tests, product-native GitHub Actions, and trusted-upstream identity headers used only in a
  conspicuously reference-local/test, non-production boundary.
- **Tower judgment:** the smallest bounded delivery is one request lifecycle with only submission,
  Product approval, AI-Risk approval, authorized rejection, retrieval, and audit observability needed
  to prove the confirmed semantics. It is not a generic policy or workflow platform.
- **Technical-shape delegation:** the Architect may select the smallest conventional endpoint paths,
  JSON fields, SQLite schema and transaction layout, status and error shapes, and idempotency and
  concurrency behavior that realize the confirmed semantics. Those choices must not add business
  meaning, weaken actor separation, hide refused attempts, or broaden the product boundary.
- **Consequential concern:** request state, decision outcomes, and audit evidence can contradict each
  other under refusal, duplication, concurrency, or process reload unless they share an explicit
  transactional consistency model; trusted headers can also be mistaken for production
  authentication unless the boundary is explicit in behavior and documentation.

## Scope

- Scaffold one .NET 10 solution containing an ASP.NET Core Minimal API and an integration-test
  project, backed directly by SQLite without a provider or persistence abstraction.
- Deliver the single Phase 1 request lifecycle: submission starts Pending; successful Product and
  AI-Risk approvals require three distinct actors; completion of both approvals produces the approved
  outcome; and an authorized rejection produces a terminal rejected outcome.
- Persist request state and append-only audit history so every successful or refused attempt remains
  consistent with durable state across process reload.
- Accept actor and role identity only from explicit trusted-upstream headers at the
  reference-local/test boundary, with conspicuous non-production warnings and no implication of real
  authentication.
- Define duplicate, idempotent, and concurrent-attempt behavior in the triggered architecture design,
  then prove the selected behavior without weakening the confirmed invariants.
- Add semantic integration tests for persistence and reload, actor separation, both approvals,
  terminal rejection, refused-attempt audit, and the architecture-selected duplicate and concurrency
  behavior.
- Add a product-owned GitHub Actions workflow that builds and runs the integration tests.
- Add accurate README, API, and trust-boundary evidence needed to deliver this product slice while
  preserving the later layered fresh-replay documentation boundary.
- Complete the named architecture design and independent blindfolded architecture review before any
  product code.

## Out of scope

- Changes to Mission, Constraints, Roadmap semantics, inception decisions, or the installed Control
  Tower method kit.
- A generic policy or workflow engine, risk scoring, provider abstraction, distribution capability,
  or unrelated product features.
- OAuth, JWT, a real identity provider, production authentication, cloud deployment, release
  automation, operations runtime, or a production-ready claim.
- The later Phase 31 layered didactic fresh replay.
- Architecture implementation before an actual stable `SOUND`, independent final review, human merge
  authorization, or merge as part of this planning change.
- Recreation of the retired `specs/` namespace.

## Activated proof obligations

| Constraint | Why activated | Expected evidence | Initial state |
|---|---|---|---|
| `FUN-CHANGE-01` | Phase 1 product delivery requires exactly one confirmed dated canonical Change Record before architecture or code. | Change Record gate passes against `origin/main` with this single record, no extra planning record, and no `specs/` path. | pending |
| `FUN-ROADMAP-01` | The complete bounded outcome is the exact current Phase 1 capability and must not drift into speculative later work. | Constitution readiness passes, the current-phase selector returns the exact Phase 1 heading, and closeout later preserves the Roadmap outcome. | pending |
| `NFR-DOCS-01` | This record and later product README, API, and trust-boundary documentation are public delivery evidence. | Documentation gate proves UTF-8 without BOM, CRLF, and balanced fences; review confirms accurate, layered language without a production-ready claim or premature Phase 31 replay. | pending |
| `FUN-MERGE-01` | The feature will produce a PR whose frozen implementation target requires independent final no-edit review and separate human merge authorization. | Review pre-check and final gates pass on a frozen pushed target; the actual stable verdict is recorded and merge remains human-authorized. | pending |
| `FUN-ARCHREVIEW-01` | Named trigger `launchpad-consistency-and-trust-boundary` covers transactionally consistent request, decision, refusal, and audit state plus an explicit trusted-header boundary. | Architect-produced sibling design, architecture pre-check, and an actual independent blindfolded stable `SOUND` are recorded before code. | pending |
| `FUN-AUTONOMY-01` | Product implementation must preserve the confirmed Mission and Constraints without silently changing strategy. | Autonomy gate and branch diff prove no Mission or Constraints change and no unauthorized strategy ADR is needed. | pending |
| `TEC-STK-01` | The slice creates the approved runtime, Minimal API, durable store, and executable product tests. | Solution and project files target .NET 10; build and integration tests exercise direct SQLite persistence with no provider abstraction. | pending |
| `TEC-IDB-01` | Every request decision is actor-aware, so the trusted-header identity boundary is part of behavior, tests, and public evidence. | API behavior, integration tests, and documentation identify the exact trusted headers as reference-local/test only and conspicuously reject production-authentication claims; no OAuth, JWT, or IdP is added. | pending |
| `FUN-APR-01` | The feature directly implements Pending creation, three-actor approval separation, terminal authorized rejection, and append-only evidence for successful and refused attempts. | Integration tests and durable-state inspection prove all transitions, refusals, actor rules, terminal behavior, audit append-only behavior, persistence, reload, and architecture-selected duplicate/concurrency semantics. | pending |
| `NFR-CI-01` | Product behavior needs executable intent-to-merge evidence independent of Control Tower framework gates. | A product-owned GitHub Actions workflow restores, builds, and runs the semantic integration tests successfully. | pending |

## Short implementation plan

1. Have the Architect define the minimal API, data, transaction, duplicate/concurrency, and identity
   boundary in this record and the sparse sibling design; obtain an independent blindfolded stable
   `SOUND` before code.
2. Scaffold the .NET 10 solution, Minimal API, integration-test project, direct SQLite dependency,
   and product-owned GitHub Actions workflow using bounded contracts consistent with the confirmed
   semantics.
3. Implement durable SQLite request and append-only audit persistence, atomic state-and-audit
   transitions, trusted-header actor and role handling, approvals, terminal rejection, and audited
   refused attempts.
4. Add semantic integration tests for actor separation, approvals, terminal rejection, refused
   attempts, persistence and reload, and the architecture-selected duplicate and concurrent behavior;
   run product build, tests, and CI.
5. Update the product README, API, and trust-boundary evidence; complete closeout and obtain the
   independent final review before separate human merge authorization.

## Evidence

`pending`

## Corrections

`pending`

## Architecture

**Named trigger:** `launchpad-consistency-and-trust-boundary`

The trigger requires the Architect to add the minimal load-bearing decision to this section and
create only the sibling
`changes/2026-07-23-govern-ai-feature-launch/design-under-test.md`. The design must resolve
transactional request/approval/rejection/audit consistency, refused and duplicate/concurrent attempt
behavior, durable reload behavior, and the trusted-header boundary against the activated constraints.
The existing inception authorization is
`constitution/decisions/ADR-20260723-01-authorize-launchpad-inception.md`. Architecture production and
independent challenge are pending; no product code may begin before an actual stable `SOUND`.

## Architecture review

**Returned verdict:** `pending`

No verdict is prewritten. The actual independent blindfolded result will be recorded only after the
design companion and frozen architecture target exist.

## Independent final review

**Returned verdict:** `pending`

No final verdict is prewritten. Independent no-edit final review, target-stability evidence, residual
dispositions, and human merge authorization remain pending.
