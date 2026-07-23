# Design under test - Launchpad consistency and trust boundary

## Trigger and governing constraints

Named trigger: `launchpad-consistency-and-trust-boundary`

Constraint set: `FUN-CHANGE-01`, `FUN-ROADMAP-01`, `NFR-DOCS-01`, `FUN-MERGE-01`,
`FUN-ARCHREVIEW-01`, `FUN-AUTONOMY-01`, `TEC-STK-01`, `TEC-IDB-01`, `FUN-APR-01`, and
`NFR-CI-01`.

Roadmap target: `Phase 1: Govern one AI-feature launch request`.

## System boundary

- One `net10.0` ASP.NET Core Minimal API service.
- One integration-test project and one product-owned GitHub Actions workflow.
- One local file-backed SQLite database accessed directly through `Microsoft.Data.Sqlite`.
- No ORM, repository interface, persistence provider, message bus, worker, or second service.
- No generic engine, scoring, OAuth, JWT, identity provider, cloud, deployment, or production claim.

## HTTP and identity contract

Request creation accepts a JSON object with exactly one required `featureName` field:

```json
{ "featureName": "Customer support answer assistant" }
```

The value is trimmed and must contain 1-120 characters after trimming. Missing, non-string, empty,
overlong, malformed, or unknown-field shapes return `400 invalid_request_body`. All decision command
routes remain bodyless, and any body octet on them returns `400 body_not_allowed`.

| Method and path | Exact `X-Reference-Actor-Role` | Success |
|---|---|---|
| `POST /api/launch-requests` | `Requester` | `201` plus resource and `Location` |
| `POST /api/launch-requests/{id}/approvals/product` | `Product` | `200` plus resource |
| `POST /api/launch-requests/{id}/approvals/ai-risk` | `AI-Risk` | `200` plus resource |
| `POST /api/launch-requests/{id}/rejection` | `Product` or `AI-Risk` | `200` plus resource |
| `GET /api/launch-requests/{id}` | not consumed | `200` plus resource |
| `GET /api/launch-requests/{id}/audit` | not consumed | `200` plus ordered events |

Commands require one `X-Reference-Actor-Id` and one `X-Reference-Actor-Role`. Actor IDs are
case-sensitive ordinal values of 1-128 characters with no edge whitespace, comma, or control
character. Accepted role values are case-sensitive `Requester`, `Product`, and `AI-Risk`. Missing,
repeated, or invalid actors return `401`; missing, repeated, unknown, or route-mismatched roles return
`403`. Read routes consume no identity and establish no read-authorization policy.

There is no actor allow-list. A well-formed upstream actor assertion is accepted inside the reference
boundary; malformed header shape and values outside the closed role set are the local unknown
identity cases and fail closed.

The resource has `id`, `featureName`, `status`, `requesterActorId`, `approvals` (`product`,
`aiRisk`), `rejection`, `version`, `createdAtUtc`, and `updatedAtUtc`. `featureName` identifies the
governed request; it is not policy or additional business behavior. Approval objects have `actorId`
and `recordedAtUtc`; rejection has `actorId`, `actorRole`, and `recordedAtUtc`. Nullable objects
remain present as `null`.

Audit JSON has `requestId`, `featureName`, and ordered `events`. An event has `sequence`,
`occurredAtUtc`, `action`, nullable `actorId`, nullable `actorRole`, `outcome`, `reasonCode`,
`statusAfter`, and `versionAfter`. Actions are `Submit`, `ProductApproval`, `AiRiskApproval`, and
`Rejection`; outcomes are `Succeeded` and `Refused`.

Problems use `application/problem+json` with `title`, `status`, `code`, and `requestId` after target
resolution. Invalid creation JSON or `featureName`, decision-body, or GUID errors return `400`;
absent targets `404`; identity errors `401`; role errors `403`; terminal, duplicate, and
actor-separation refusals `409`.

The host starts only in `Development` or `Testing`, logs
`NON-PRODUCTION TRUSTED-HEADER REFERENCE`, and adds this header to every response:

`X-Reference-Authentication-Warning: NON-PRODUCTION; caller-supplied headers are not authentication`

## State and command rules

- New requests retain the normalized `featureName` and are `Pending`, version `0`, with audit
  sequence `1`.
- A successful approval fills one fixed slot and increments version once.
- Product and AI-Risk approvers are each distinct from the requester and each other.
- The second approval changes the request to `Approved` in the same transaction.
- Product or AI-Risk may reject a Pending request; any existing single approval remains recorded.
- No rejector-separation rule is added.
- `Approved` and `Rejected` are terminal.
- A duplicate approval is refused; a repeated rejection is terminally refused.
- Submission retry creates another request. There is no idempotency key, ETag, or retry coordinator.

## SQLite layout

Schema version 1 has two `STRICT` tables:

1. `launch_requests`: text GUID primary key; non-null `feature_name`; exact status; requester;
   nullable Product actor/time; nullable AI-Risk actor/time; nullable rejector actor/role/time;
   integer version; created/updated UTC timestamps.
2. `audit_events`: request ID; per-request integer sequence; UTC timestamp; action; nullable actor and
   role; outcome; reason code; status/version snapshot; primary key `(request_id, sequence)`; foreign
   key to the request with delete restricted.

Request checks enforce `feature_name` is already trimmed and 1-120 characters, paired fields, exact
enums, approval actor separation, complete Pending/Approved/Rejected row shapes, and version equal to
retained successful decisions. Triggers block request deletion and terminal-row update.

Audit checks enforce exact enums and reason sets. Insert triggers require the next sequence and a
status/version snapshot equal to the request row. Update and delete triggers abort. The two primary
keys are the only indexes.

Every connection uses `foreign_keys=ON`, `busy_timeout=5000`, and `synchronous=FULL`; journal mode is
`DELETE`. `Launchpad:DatabasePath` defaults to untracked `./data/launchpad.db`. Startup accepts only
an empty version-0 store, which it creates and marks version 1 atomically, or a complete version-1
store. Partial and unknown versions stop startup.

## Transaction and ordering

Every write uses `BEGIN IMMEDIATE`.

Creation validates the exact JSON shape, normalized `featureName`, and headers, then inserts the named
aggregate plus sequence-1 audit and commits before `201`.

A targeted command validates transport/GUID, starts the transaction, and loads the target. Evaluation
then proceeds in this order: actor; role and route authorization; terminal state; filled slot;
requester separation; other-approver separation; mutation. After an existing target is loaded, a
refusal inserts one event with the unchanged snapshot and commits before the error response. A success
updates state/version, inserts one event with the resulting snapshot, and commits before the success
response. Any write or commit failure rolls back both.

Malformed method/path, malformed creation JSON or `featureName`, a non-empty decision body, malformed
GUID, nonexistent targets, GETs, and database availability failures have no request-attached audit.
An invalid creation body has no request-attached audit because no request exists. Availability
failures are infrastructure errors, not `Refused` outcomes.

Concurrent writers serialize by SQLite lock acquisition. Distinct approval roles can both succeed;
duplicate slots produce one success then one audited conflict; one actor racing both roles produces
one success then one audited separation conflict. Rejection is evaluated against the preceding
committed state. Per-request sequence is authoritative ordering.

## Evidence surface

- File-backed HTTP integration tests cover the sole `featureName` creation field and its
  normalization, validation, persistence, resource, and audit projection; contract, headers, state
  transitions, actor separation, rejection, terminal and other refused attempts, duplicates,
  concurrent commands, audit append-only enforcement, malformed/nonexistent exclusions, schema
  checks, and warning behavior.
- Reload tests dispose and recreate the host against the same temporary database file.
- A Production-environment test expects startup refusal.
- Product CI installs .NET `10.0.x` and runs restore, build, and integration tests with read-only
  repository permission.
- README, API, and trust-boundary documents carry the non-production warning; README and API examples
  show `featureName` without adding summary, model, provider, risk, list, search, or filter surfaces.

## Costs and reversibility facts

- Direct SQL and triggers require manual mapping and explicit future `user_version` migrations.
- SQLite serializes writers; lock timeout can produce an unaudited infrastructure failure.
- Duplicate submission after an unknown response can create another request.
- Audit has no retention or deletion path.
- Adding approval roles changes the fixed schema.
- Trusted identity headers are caller-spoofable.
- Before implementation the design can be replaced and challenged again.
- After implementation, incompatible reference data may be archived and a new store initialized;
  existing audit rows are not rewritten.
