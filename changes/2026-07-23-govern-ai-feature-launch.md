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
- The later `Phase 2: Reproduce inception and feature from a fresh context` layered didactic replay.
- Architecture implementation before an actual stable `SOUND`, independent final review, human merge
  authorization, or merge as part of this planning change.
- Recreation of the retired `specs/` namespace.

## Activated proof obligations

| Constraint | Why activated | Expected evidence | Initial state |
|---|---|---|---|
| `FUN-CHANGE-01` | Phase 1 product delivery requires exactly one confirmed dated canonical Change Record before architecture or code. | Change Record gate passes against `origin/main` with this single record, no extra planning record, and no `specs/` path. | pending |
| `FUN-ROADMAP-01` | The complete bounded outcome is the exact current Phase 1 capability and must not drift into speculative later work. | Constitution readiness passes, the current-phase selector returns the exact Phase 1 heading, and closeout later preserves the Roadmap outcome. | pending |
| `NFR-DOCS-01` | This record and later product README, API, and trust-boundary documentation are public delivery evidence. | Documentation gate proves UTF-8 without BOM, CRLF, and balanced fences; review confirms accurate, layered language without a production-ready claim or premature `Phase 2: Reproduce inception and feature from a fresh context` replay. | pending |
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

| Constraint | Result | Evidence |
|---|---|---|
| `FUN-CHANGE-01` | pass | `python -B framework/scripts/check_change_record.py --base origin/main` passes with this one canonical feature record and its triggered design companion; no `specs/` path exists. |
| `FUN-ROADMAP-01` | pass | Readiness passed with exact Phase 1 throughout implementation; closeout checks its delivered item and the selector advances to human-authorized `Phase 2: Reproduce inception and feature from a fresh context` without changing either phase's semantics. |
| `NFR-DOCS-01` | pass | `python -B framework/scripts/check_docs.py` passes 53 tracked Markdown files; README, API, trust-boundary docs, and this record use the exact canonical Phase 2 replay name and do not perform that replay. |
| `FUN-MERGE-01` | pass | The completed confirmed record passes the review pre-check on the frozen pushed target; GitHub checks are green except the expected governed-merge block on `confirmed` status and final verdict `PENDING`. |
| `FUN-ARCHREVIEW-01` | pass | The explicit architecture pre-check passes and the actual stable `SOUND` for design target `ed91419236a01fafffa21760ed446b024b81f7b7` is recorded above; code began only afterward. |
| `FUN-AUTONOMY-01` | pass | `python -B framework/scripts/check_autonomy.py --base origin/main` passes; Mission and Constraints are unchanged and implementation remains inside the confirmed strategy. |
| `TEC-STK-01` | pass | Locked Release restore/build passes for `net10.0`; the API uses direct `Microsoft.Data.Sqlite` 10.0.10 and patched native bundle 2.1.12 against one file-backed SQLite database, with no ORM or provider abstraction. |
| `TEC-IDB-01` | pass | Integration tests prove exact trusted-header validation, every-response warning, no-identity read routes, and Production startup refusal; README and `docs/trust-boundary.md` conspicuously reject a production-authentication claim. |
| `FUN-APR-01` | pass | All 28 integration cases pass, including direct audit retrieval after terminal commands against both Approved and Rejected targets; each proves one appended `Refused` / `request_terminal` event, contiguous sequence, and unchanged durable status/version. |
| `NFR-CI-01` | pass | Product-owned run `29985547135` completed successfully on correction target `94e705f764315998be0b3e237e937597e5dcd1ef`, executing locked restore, Release build, and all 28 integration cases with the new terminal-audit assertions. |

## Corrections

- **Post-design context synchronization:** merge commit
  `d03873cd24525a7e618f37421616f07bea92611b` incorporated human-authorized ADR-03 and planned Phase 2 from
  `3d5714ab5d09f108d2d08cd5688c9408f7b8477f` after the architecture design and review. The added
  phase prevents Roadmap exhaustion after this feature is delivered. Exact Phase 1 remains current
  and unchanged; the observable outcome, active constraints, product design, dependencies, and
  implementation plan do not change. The prior stable architecture `SOUND` remains applicable.
- **Dependency correction:** initial restore resolved transitive
  `SQLitePCLRaw.lib.e_sqlite3` 2.1.11 with a high-severity advisory. The API now pins
  `SQLitePCLRaw.bundle_e_sqlite3` 2.1.12, locked restore is clean, and
  `dotnet list AI.FeatureLaunchpad.sln package --include-transitive --vulnerable` reports no
  vulnerable package.
- **Compile correction:** the first build exposed a generic nullable wrapper that could not represent
  a missing enum role. Explicit actor and role parse records replaced it without casts or behavior
  change; subsequent builds complete with zero warnings and errors.
- **Persistence correctness correction:** before the semantic run, the rejection-field check was
  tightened to require all-null or all-present fields, and audit reads now dispose their reader before
  committing the read transaction.
- **Integration-host correction:** the first complete run had 13 failures because the store captured
  configuration before `WebApplicationFactory` applied its temporary database override; two
  collection/index expectations were also test assertion defects. Store construction now resolves
  final configuration through dependency injection, assertions inspect durable values and SQLite
  auto-indexes correctly, and the next Release run passed all 28 cases.
- **Final-review Attempt 1 correction:** stable review of target
  `72a181c056dcae103af33ddd7e6119ad5d2a05be` found an implementation-evidence gap and a record
  wording defect without finding a product-code defect. The existing terminal test now retrieves
  audit after commands against Approved and Rejected targets and proves exactly one appended
  `Refused` / `request_terminal` event, contiguous sequence, and unchanged durable status/version
  for each. The two ambiguous replay references now use the exact canonical
  `Phase 2: Reproduce inception and feature from a fresh context` name. The focused case and all 28
  integration cases pass without a product-code change; product CI run `29985547135` then passed on
  correction target `94e705f764315998be0b3e237e937597e5dcd1ef`.

## Architecture

**Named trigger:** `launchpad-consistency-and-trust-boundary`

**Companion:** `changes/2026-07-23-govern-ai-feature-launch/design-under-test.md`

**Governing ADR supplied to the form pre-check only:**
`constitution/decisions/ADR-20260723-01-authorize-launchpad-inception.md`

**Affected constraints:** `FUN-CHANGE-01`, `FUN-ROADMAP-01`, `NFR-DOCS-01`, `FUN-MERGE-01`,
`FUN-ARCHREVIEW-01`, `FUN-AUTONOMY-01`, `TEC-STK-01`, `TEC-IDB-01`, `FUN-APR-01`, and `NFR-CI-01`.

### Decision and component boundary

Build one `net10.0` ASP.NET Core Minimal API service and one integration-test project. Route handlers
use `Microsoft.Data.Sqlite` directly against one local SQLite file. A small schema initializer and
focused SQL command functions may organize `Program.cs`, but there is no repository interface,
unit-of-work layer, provider abstraction, ORM, message bus, background worker, or second service.

The fixed aggregate identifies the governed AI feature with one required `featureName`, has exactly
two approval slots, Product and AI-Risk, and has one optional rejection. `featureName` is request
identity, not policy or additional business behavior. The aggregate does not model summaries, model
or provider metadata, risk scores, comments, rejection reasons, policy rules, user directories, or
generic workflow stages. The API establishes no confidentiality or read-authorization policy; its
two GET routes are reference observability surfaces.

The runtime components and flow are:

1. An early middleware adds the non-production warning to every HTTP response.
2. Minimal API routes validate transport shape and map stable problem responses.
3. Command routes parse reference headers and execute direct SQL in one transaction.
4. Read routes materialize the aggregate or its ordered audit events from the same SQLite file.
5. Startup initializes or validates schema version 1 before the listener becomes ready.

### Minimal HTTP, JSON, and identity contract

Request creation accepts a JSON object with exactly one required `featureName` field. The value is
trimmed and must contain 1-120 characters after trimming; missing, non-string, empty, overlong,
malformed, or unknown-field shapes return `400 invalid_request_body`. All decision command routes
remain bodyless, and any body octet on them returns `400 body_not_allowed`. The server creates a
lowercase canonical GUID and UTC timestamps.

```json
{ "featureName": "Customer support answer assistant" }
```

| Method and path | Required reference role | Success |
|---|---|---|
| `POST /api/launch-requests` | `Requester` | `201 Created`, `Location`, and the resource |
| `POST /api/launch-requests/{id}/approvals/product` | `Product` | `200 OK` and the resource |
| `POST /api/launch-requests/{id}/approvals/ai-risk` | `AI-Risk` | `200 OK` and the resource |
| `POST /api/launch-requests/{id}/rejection` | `Product` or `AI-Risk` | `200 OK` and the resource |
| `GET /api/launch-requests/{id}` | none; no identity is consumed | `200 OK` and the resource |
| `GET /api/launch-requests/{id}/audit` | none; no identity is consumed | `200 OK` and ordered events |

Every command requires exactly one `X-Reference-Actor-Id` and one
`X-Reference-Actor-Role` header. Actor IDs are 1-128 characters, have no leading or trailing
whitespace, comma, or control character, and compare as case-sensitive ordinal strings. Roles compare
case-sensitively and the only accepted values are `Requester`, `Product`, and `AI-Risk`. A command
with a missing, repeated, or invalid actor fails `401`; a missing, repeated, unknown, or
endpoint-mismatched role fails `403`. The role header is only a trusted-upstream assertion: the
service neither authenticates it nor looks up an actor.

There is no local actor allow-list, so the service cannot classify a syntactically valid upstream
actor assertion as unknown without inventing an identity directory. Any value outside the closed role
set, or any malformed identity-header shape, is the local unknown-identity case and fails closed; a
well-formed actor ID is trusted only within the warned reference boundary.

The complete resource JSON has these keys; nullable decision objects remain present as `null`:

```json
{
  "id": "lowercase-guid",
  "featureName": "Customer support answer assistant",
  "status": "Pending|Approved|Rejected",
  "requesterActorId": "actor",
  "approvals": {
    "product": { "actorId": "actor", "recordedAtUtc": "RFC3339-UTC" },
    "aiRisk": null
  },
  "rejection": null,
  "version": 1,
  "createdAtUtc": "RFC3339-UTC",
  "updatedAtUtc": "RFC3339-UTC"
}
```

When present, `rejection` has exactly `actorId`, `actorRole`, and `recordedAtUtc`. Audit retrieval
returns `requestId`, `featureName`, and an `events` array ordered by `sequence`; every event has
`sequence`, `occurredAtUtc`, `action`, nullable `actorId`, nullable `actorRole`, `outcome`,
`reasonCode`, `statusAfter`, and `versionAfter`. The fixed action values are `Submit`,
`ProductApproval`, `AiRiskApproval`, and `Rejection`; outcomes are `Succeeded` and `Refused`.

Errors use `application/problem+json` with stable `title`, numeric `status`, and `code`, plus
`requestId` only after an existing request has been resolved. Invalid creation JSON or `featureName`
is `400 invalid_request_body`; malformed IDs are `400`; absent IDs are `404`. Missing/invalid actors
are `401`, role failures are `403`, and terminal, duplicate, or separation-of-duties refusals are
`409`.

This is an intentionally spoofable reference boundary. The host refuses to start unless the ASP.NET
Core environment is exactly `Development` or `Testing`. At startup it logs an uppercase
`NON-PRODUCTION TRUSTED-HEADER REFERENCE` warning, and every response, including errors, carries:

`X-Reference-Authentication-Warning: NON-PRODUCTION; caller-supplied headers are not authentication`

The README, API document, and trust-boundary document repeat that warning before examples. The README
and API document show the sole required `featureName` creation field and returned request identity;
they add no list, search, filter, policy, or metadata surface. No forwarded-header trust inference,
OAuth, JWT, cookie, API-key, identity-provider, or production authentication surface is present.

### State, terminal, duplicate, and concurrent behavior

- Creation records the normalized `featureName`, `Pending`, version `0`, and audit sequence `1`.
- A first valid approval fills its role slot, increments the version once, and remains `Pending`.
  The second valid approval must have a different actor and atomically changes the request to
  `Approved`.
- Product and AI-Risk approvers are each distinct from the requester and from each other. These
  checks apply only to approvals; no additional rejector-separation policy is inferred.
- A valid `Product` or `AI-Risk` actor may reject only a `Pending` request. Existing approval evidence
  is retained and the same transaction changes the request to `Rejected`.
- `Approved` and `Rejected` are terminal. Every later decision command is refused and audited without
  changing aggregate version or timestamps.
- Decision POSTs are deliberately not idempotent. While the request remains Pending, repeating a
  filled approval slot, including with the same actor, returns audited
  `409 approval_already_recorded`; after either terminal outcome, the earlier terminal check returns
  `409 request_terminal`. Repeating a rejection therefore encounters the terminal rule. Submission
  retries create separate requests; there is no idempotency key.

Every write transaction begins with `BEGIN IMMEDIATE`, so SQLite chooses one serial order. Concurrent
distinct Product and AI-Risk approvals both succeed in that order and end Approved. For a duplicate
slot, exactly the first succeeds and the later attempt is an audited conflict. If one actor races for
both approval roles, the first role may succeed and the later role is an audited separation conflict.
A rejection race is evaluated against the state left by the preceding transaction: it succeeds if
that state is still Pending and is refused if it is terminal. No scheduling winner is promised, but
each response and the final state are deterministic for the committed order. There is no distributed
lock, retry coordinator, ETag, or deduplication store.

### Direct SQLite schema and initialization

The selected package is direct `Microsoft.Data.Sqlite`, not EF Core. The database path is the
`Launchpad:DatabasePath` setting, defaulting to the untracked local file
`./data/launchpad.db`; integration tests always supply a unique temporary file.

Schema version 1 contains two `STRICT` tables:

| Table | Columns |
|---|---|
| `launch_requests` | `id TEXT PRIMARY KEY`, `feature_name TEXT NOT NULL`, `status TEXT`, `requester_actor_id TEXT`, nullable Product actor/time, nullable AI-Risk actor/time, nullable rejector actor/role/time, `version INTEGER`, `created_at_utc TEXT`, `updated_at_utc TEXT` |
| `audit_events` | `request_id TEXT`, `sequence INTEGER`, `occurred_at_utc TEXT`, `action TEXT`, nullable `actor_id TEXT`, nullable `actor_role TEXT`, `outcome TEXT`, `reason_code TEXT`, `status_after TEXT`, `version_after INTEGER`, composite primary key `(request_id, sequence)`, and a restricting foreign key to `launch_requests` |

`launch_requests` checks that `feature_name` is already trimmed and 1-120 characters, checks exact
status and role enums, paired actor/time nullability, approval-actor separation, and these complete
row shapes: Pending has no rejection and fewer than two approvals; Approved has both approvals and no
rejection; Rejected has a rejection and no completed pair of approvals. Its version equals the count
of successful approval/rejection decisions retained in the row. A trigger blocks deletion, and
another blocks any update to a terminal row.

`audit_events` checks action, role, outcome, status, and the fixed reason-code sets. Success reasons
are `request_created`, `approval_recorded`, and `request_rejected`. Refusal reasons are
`identity_missing`, `identity_invalid`, `role_missing`, `role_unknown`, `role_mismatch`,
`request_terminal`, `approval_already_recorded`, `requester_cannot_approve`, and
`approvers_not_distinct`. Insert triggers require the next contiguous per-request sequence and require
`status_after` and `version_after` to equal the referenced aggregate at insertion. Update and delete
triggers make audit rows append-only.

The request primary key and audit composite primary key are the only indexes. Every supported query
is an ID lookup or an audit range ordered by that composite key; there is no list/status query to
justify another index.

On each connection the service enables `foreign_keys=ON`, `busy_timeout=5000`, and
`synchronous=FULL`; initialization fixes the local journal mode to `DELETE`. Startup obtains an
immediate transaction and reads `PRAGMA user_version`. Version `0` is accepted only when no
Launchpad tables exist, creates all version-1 tables/triggers, and sets `user_version=1` atomically.
Version `1` must contain every expected object. Any partial, newer, or unknown schema fails startup.
There is no migration framework or automatic downgrade.

### One command transaction and audit boundary

For creation, the exact JSON shape, normalized `featureName`, and headers are validated before an ID
exists. One immediate transaction inserts the named request and its sequence-1 success event, then
commits before returning `201`.

For a targeted command, the fixed evaluation order is: transport and canonical GUID; begin immediate
transaction and load target; actor header; role header and endpoint authorization; terminal state;
filled slot; requester separation; other-approver separation; mutation. Once an existing target is
loaded, every identity, authorization, terminal, duplicate, or separation refusal appends one event
with the unchanged state snapshot and commits before its error response is sent. A success updates
the aggregate and version, appends one event with the resulting snapshot, and commits before its
success response. A constraint, audit insert, or commit failure rolls back all writes and never
returns a governed success or refusal.

A governed attempt is therefore a valid creation command attached to its newly created named request,
or a bodyless decision command attached to an existing request row. Routing/method failures, malformed
creation JSON or `featureName`, a non-empty decision body, malformed GUID, nonexistent target, and GET
requests are outside that auditable aggregate boundary. In particular, an invalid creation body has
no request-attached audit because no request exists. A database-open, lock-timeout, or commit failure
is an infrastructure failure (`503` where safely classifiable), not a falsely reported `Refused`
outcome, because no durable audit can be guaranteed while the store is unavailable. This boundary is
explicit in API documentation and tests.

Reads use a read transaction so a resource snapshot cannot mix aggregate versions. The SQLite file
is reopened on every host lifetime; no process memory is authoritative. Audit `sequence`, rather
than timestamp precision, establishes durable order. Timestamps use a canonical seven-fraction-digit
UTC `Z` representation.

### Test and product-CI evidence

Integration tests run the actual Minimal API through `WebApplicationFactory` against a temporary
file-backed SQLite database. They cover exact creation shape and `featureName` normalization,
validation, persistence, resource, and audit projection; exact contract/error/warning shapes; Pending
creation; both approval orders; requester and cross-approver separation; either authorized rejection
role; retained pre-rejection approval; terminal refusals; missing/invalid/unknown/mismatched headers;
duplicate commands; malformed creation and targeted-command/nonexistent exclusions; direct rejection
of audit update/delete; and schema version refusal.

Concurrency tests issue real parallel HTTP commands and assert the allowed serial winner, every
response, final aggregate, contiguous audit order, and snapshot/version consistency. Reload tests
dispose the first host, start a new host against the same file, and compare resource and audit state.
A production-environment test asserts startup refusal; every HTTP test asserts the warning header.

The product-owned `.github/workflows/product-ci.yml` has read-only contents permission, installs
.NET `10.0.x`, and runs restore, build, and integration tests on pull requests and main-branch pushes.
It has no deployment, release, cloud, or Control Tower gate implementation.

### Alternatives and trade-offs

1. **EF Core with its SQLite provider and migrations.** It would reduce handwritten materialization
   and provide a migration mechanism, but adds change tracking, model conventions, and an abstraction
   whose transaction ordering and database checks still require explicit SQL. For one fixed aggregate
   and two tables, direct `Microsoft.Data.Sqlite` is smaller and makes the exact state/audit commit
   boundary inspectable.
2. **Separate approval/rejection tables or a generic event-sourced workflow.** Normalized decision
   rows would make a future variable role set easier, but this phase has exactly two fixed roles.
   Additional joins, cross-table triggers, projection logic, or a workflow engine enlarge the
   consistency surface without delivering the bounded outcome.
3. **In-memory state, a separate audit file, or an audit transaction after state commit.** These
   shapes are mechanically simpler in parts but cannot provide durable reload and atomic
   state/audit evidence, so they do not satisfy the confirmed invariant.
4. **Idempotency keys or optimistic HTTP preconditions.** They can support distributed retry
   protocols, but no such protocol is confirmed. Explicit audited duplicate conflicts and SQLite
   serialization keep this single-process reference testable without inventing one.

The negative consequences are deliberate: direct SQL and schema triggers require manual mapping and
manual future migrations; SQLite serializes writers and a five-second lock timeout can surface an
unaudited infrastructure error; duplicate submission after a lost response can create another
request; append-only audit grows without retention; fixed approval columns make adding roles a schema
change; and trusted headers remain trivially spoofable. The startup guard and warnings make the last
cost visible rather than solving production identity.

### Reversibility, migration, and file impact

Before code, this design is reversible by changing this confirmed record and re-running the
independent challenge. After implementation, a future schema change must be a governed,
`user_version`-incrementing explicit migration; unknown versions continue to fail closed. For this
non-production reference, an incompatible reversal may archive the SQLite file and initialize a new
one, but must never rewrite an existing audit history in place. Replacing SQLite or the identity
boundary later touches the one API project and its integration tests; there is no compatibility
facade to preserve.

The expected implementation blast radius is limited to `AI.FeatureLaunchpad.sln`,
`src/Launchpad.Api/` (project, host/contracts, and direct schema/SQL), and
`tests/Launchpad.Api.IntegrationTests/`; `.github/workflows/product-ci.yml`; `.gitignore` for local
database files; and the existing `README.md` plus `docs/api.md` and `docs/trust-boundary.md`. No
Mission, Constraints, Roadmap, ADR, framework, deployment, or second-service file is changed.

Architecture production is complete in this record and its sole companion. Independent challenge is
still pending; no product code may begin before an actual stable `SOUND` is returned and recorded by
the Tower.

## Architecture review

**Reviewer/date:** Reviewer Agent, 2026-07-23

**Reviewed design target/ref:** `ed91419236a01fafffa21760ed446b024b81f7b7` at
`origin/rcoccia-govern-ai-feature-launch`

**Start heads:** local HEAD `ed91419236a01fafffa21760ed446b024b81f7b7`; local origin ref
`ed91419236a01fafffa21760ed446b024b81f7b7`; remote ref
`ed91419236a01fafffa21760ed446b024b81f7b7`

**Completion heads:** local HEAD `ed91419236a01fafffa21760ed446b024b81f7b7`; local origin ref
`ed91419236a01fafffa21760ed446b024b81f7b7`; remote ref
`ed91419236a01fafffa21760ed446b024b81f7b7`

**Stability:** `STABLE`

**Pre-check:** `PASS` - the explicit architecture pre-check found the companion challengeable
against the inception ADR and active Constraints.

**Returned verdict:** `SOUND`

**Architecture:** One .NET 10 ASP.NET Core Minimal API uses direct file-backed SQLite transactions
for durable request and append-only audit state, accepts identity only through conspicuously
non-production trusted headers, and fixes approval, rejection, duplicate, and concurrency semantics.

**Direct constraints:** `TEC-STK-01` remains bounded to the approved stack; `TEC-IDB-01` is enforced
by the Development/Testing startup boundary and warning; `FUN-APR-01` is resolved through fixed
states, actor separation, terminal outcomes, audited atomic transactions, and serialized writers;
`FUN-ROADMAP-01` remains anchored to exact Phase 1; and `NFR-CI-01` plus `NFR-DOCS-01` are resolved by
product-native CI and accurate product documentation.

**Lenses:** Minimise-for-change found fixed approval slots, direct SQL, and two tables avoid generic
platforms while naming the proportional schema and serialization costs. Walking-skeleton-for-target
found end-to-end creation, approval, rejection, transport, durable audit, reload, concurrency, CI,
and documentation coverage.

**Evidence:** The blindfolded challenge reviewed the companion against Constraints and Roadmap at the
stable target above. Existing routes remain as designed; no additional surface is required.

**Findings:** none.

**Summary:** No constraint incoherence, calibration defect, irreversibility defect, scope tension, or
internal contradiction was found.

**Residual:** `FUN-ARCHREVIEW-01::semantic-challenge` is covered by this returned stable `SOUND`.

## Delivery metrics

| Metric | Result |
|---|---|
| planned steps | 5 of 5 completed |
| changed artifacts | 25 branch paths: 21 product implementation paths, canonical record, design companion, Roadmap, and changelog |
| elapsed | approximately 12 minutes from implementation authorization to the first green remote product CI result |
| executable proof | 28 integration cases; zero failed or skipped on the final local Release run |
| rework | 4 targeted cycles: dependency advisory correction, compile-time role model correction, first-run test-host/assertion correction, and final-review evidence/wording correction |
| defects found | 1 vulnerable transitive dependency, 1 compile type defect, 1 test-host configuration defect, 2 initial assertion defects, 2 proactive persistence correctness defects, 1 final-review evidence gap, and 1 record wording defect; all corrected, with no known product defect remaining |

## Closeout

| Disposition | Record |
|---|---|
| delivered | The exact Phase 1 launch request is delivered through a .NET 10 Minimal API with the sole `featureName` input, direct file-backed SQLite atomic state/audit transitions, distinct requester/Product/AI-Risk approvals, authorized terminal rejection, audited refusals, trusted-header warnings, 28 integration cases, product CI, and bounded public docs. |
| remaining | A fresh independent final no-edit review, actual returned-verdict recording, governed-merge success, and separate human merge authorization remain pending. The planned Phase 2 fresh-context replay remains wholly unstarted. |
| discovered | The initial SQLite native bundle carried a published advisory, the test host initially applied its database override too late, and final-review Attempt 1 found one evidence gap plus one record wording defect; all were corrected without changing product semantics, architecture, constraints, dependencies beyond the patched direct pin, or scope. |
| evidence | Phase 1 is checked in `constitution/roadmap.md`; deterministic `CHANGELOG.md` tracks implementation commit `8d5099acf00ac4d4c61040858698b6aa90b97c2d`; post-correction locked restore and zero-warning/error Release build pass, all 28 integration cases pass, the vulnerability scan is clean, and product CI run `29985547135` is green on correction target `94e705f764315998be0b3e237e937597e5dcd1ef`. |

## Independent final review

**Returned verdict:** `BLOCK`

### Attempt 1

**Reviewer/date:** Reviewer Agent, 2026-07-23

**Reviewed target:** `72a181c056dcae103af33ddd7e6119ad5d2a05be`

**Remote:** `origin`

**Ref:** `refs/heads/rcoccia-govern-ai-feature-launch` (PR 3)

**Start local head:** `72a181c056dcae103af33ddd7e6119ad5d2a05be`

**Start local origin head:** `72a181c056dcae103af33ddd7e6119ad5d2a05be`

**Start remote head:** `72a181c056dcae103af33ddd7e6119ad5d2a05be`

**Completion local head:** `72a181c056dcae103af33ddd7e6119ad5d2a05be`

**Completion local origin head:** `72a181c056dcae103af33ddd7e6119ad5d2a05be`

**Completion remote head:** `72a181c056dcae103af33ddd7e6119ad5d2a05be`

**Stability:** `STABLE`

**Returned verdict:** `BLOCK`

**Gates:** PASS: review pre-check, Change Record gate, architecture pre-check, documentation gate for
53 tracked Markdown files, autonomy, provenance for 10 active constraints, constitution readiness,
exact current Phase 2, diff and cache hygiene, locked restore, Release build with zero warnings and
errors, 28 integration tests, no vulnerable package with SQLitePCLRaw 2.1.12, product CI run
`29984157180` on the exact target, and green docs/autonomy/provenance checks. Merge readiness
expectedly blocked on confirmed status and final verdict `PENDING` before this actual return was
recorded.

**Evidence:** Architecture `SOUND` remained fresh and implementation matched its one .NET 10 Minimal
API, direct file-backed SQLite transactional state/audit, conspicuously non-production trusted
headers, and fixed approval, rejection, duplicate, and concurrency semantics. The target remained
clean and stable across local HEAD, local origin, and remote observations.

**Summary:** Blocking evidence gaps remain. Terminal refusal audit is not genuinely integration
tested for both Approved and Rejected targets, and two Change Record references use undefined
`Phase 31` instead of the canonical Phase 2 replay name. No architecture, implementation, constraint,
scope, or dependency contradiction was found.

**Findings:**

1. The terminal-refusal integration test asserts `409` and unchanged aggregate version but never
   retrieves audit or proves a newly appended `Refused` / `request_terminal` event for either an
   Approved or Rejected target. Product code routes through `RefuseAsync`, but `FUN-APR-01` evidence
   is incomplete.
2. Two Change Record references use undefined `Phase 31`, while the product Roadmap names
   `Phase 2: Reproduce inception and feature from a fresh context`. This leaves `NFR-DOCS-01`
   wording ambiguous.

**Reviewer notes:** Existing routes and architecture remain unchanged. Correct only the focused
terminal-audit assertions and canonical Phase 2 wording, rerun product and governance evidence, and
obtain a fresh independent final review.

| Residual | Disposition | Notes |
|---|---|---|
| `FUN-CHANGE-01::obligation-completeness-and-confirmation` | covered | One confirmed canonical Change Record preserves the complete review and correction history. |
| `FUN-ROADMAP-01::deferral-intent` | covered | Phase 1 is delivered and the human-authorized Phase 2 replay is current without deferral. |
| `NFR-DOCS-01::didactic-quality` | follow-up | Replace undefined Phase 31 wording with the exact canonical Phase 2 replay name. |
| `FUN-MERGE-01::review-genuineness` | covered | This actual stable `BLOCK` is recorded without claiming merge authorization. |
| `FUN-ARCHREVIEW-01::semantic-challenge` | covered | The prior stable architecture `SOUND` remains applicable and fresh. |
| `FUN-AUTONOMY-01::human-authorization` | covered | Mission and Constraints remain unchanged and no new strategic decision was made. |
| `TEC-STK-01::approved-surface` | covered | The implementation remains one .NET 10 Minimal API with direct file-backed SQLite. |
| `TEC-IDB-01::boundary-clarity` | covered | Startup guard, every-response warning, tests, and docs keep trusted headers conspicuously non-production. |
| `FUN-APR-01::governance-consistency` | follow-up | Add direct audit assertions for terminal commands against Approved and Rejected targets. |
| `NFR-CI-01::product-evidence` | follow-up | Rerun product CI after the terminal-audit assertions execute in the full suite. |

### Attempt 2

**Reviewer/date:** Reviewer Agent, 2026-07-23

**Reviewed target:** `06daf05b8af4bcb48d14c19479c090ca9a92e241`

**Remote:** `origin`

**Ref:** `refs/heads/rcoccia-govern-ai-feature-launch` (PR 3)

**Start local head:** `06daf05b8af4bcb48d14c19479c090ca9a92e241`

**Start local origin head:** `06daf05b8af4bcb48d14c19479c090ca9a92e241`

**Start remote head:** `06daf05b8af4bcb48d14c19479c090ca9a92e241`

**Completion local head:** `06daf05b8af4bcb48d14c19479c090ca9a92e241`

**Completion local origin head:** `06daf05b8af4bcb48d14c19479c090ca9a92e241`

**Completion remote head:** `06daf05b8af4bcb48d14c19479c090ca9a92e241`

**Stability:** `STABLE`

**Returned verdict:** `BLOCK`

**Gates:** PASS: review pre-check, Change Record gate, architecture pre-check, documentation gate for
53 tracked Markdown files, constitution readiness with exact current Phase 2, autonomy, provenance
for 10 active constraints, diff and cache hygiene, locked restore, Release build with zero warnings
and errors, 28 integration tests, no vulnerable package, and current product CI run `29985658230`.
Merge readiness expectedly remained blocked on confirmed status and the latest returned `BLOCK`.

**Evidence:** Attempt 1 findings were resolved: terminal refusals against Approved and Rejected
targets now have direct audit assertions, the exact Phase 2 wording is used where Roadmap context is
required, and product CI is current. Architecture and scope remain unchanged: one .NET 10 Minimal
API, direct file-backed SQLite transactional state/audit, conspicuously non-production trusted
headers, and fixed approval, rejection, duplicate, and concurrency semantics. Product source and
tests remained stable and the reviewed target was clean across local HEAD, local origin, and remote.

**Summary:** The implementation and prior review findings are resolved, but the canonical record
rewrote historical evidence and metrics instead of appending newer attempts, and its latest
documentation evidence overclaims where the exact Roadmap Phase 2 title appears.

**Findings:**

1. Prior `NFR-DOCS-01`, `FUN-APR-01`, and `NFR-CI-01` Evidence rows and the prior rework/defect
   metrics were deleted or replaced. The canonical Change Record must preserve those historical
   rows verbatim and append newer evidence and metrics.
2. The current `NFR-DOCS-01` Evidence row falsely claims README, API, and trust-boundary docs use
   the exact canonical Phase 2 replay name. Search finds that exact title only in the Roadmap and
   this Change Record; the product docs accurately prove API and trust boundaries without needing
   the Roadmap title.

**Reviewer notes:** No future work requested.

| Residual | Disposition | Notes |
|---|---|---|
| `FUN-CHANGE-01::obligation-completeness-and-confirmation` | follow-up | Restore deleted historical evidence and metrics verbatim, then append corrections without rewriting Attempts 1 or 2. |
| `FUN-ROADMAP-01::deferral-intent` | covered | Phase 1 remains delivered and exact Phase 2 remains current without Roadmap change. |
| `NFR-DOCS-01::didactic-quality` | follow-up | Preserve the overclaim as history and append accurate evidence about where the exact Phase 2 title is required and present. |
| `FUN-MERGE-01::review-genuineness` | covered | Both actual stable `BLOCK` attempts are recorded and merge remains unauthorized. |
| `FUN-ARCHREVIEW-01::semantic-challenge` | covered | The stable architecture `SOUND` remains applicable and unchanged. |
| `FUN-AUTONOMY-01::human-authorization` | covered | Mission and Constraints remain unchanged and no strategic decision was made. |
| `TEC-STK-01::approved-surface` | covered | Product source remains the approved .NET 10 Minimal API and direct SQLite surface. |
| `TEC-IDB-01::boundary-clarity` | covered | The trusted-header boundary remains conspicuously non-production in behavior, tests, and docs. |
| `FUN-APR-01::governance-consistency` | covered | Terminal refusal audit is now directly proven for Approved and Rejected targets. |
| `NFR-CI-01::product-evidence` | covered | Product CI run `29985658230` is green on the reviewed target. |
