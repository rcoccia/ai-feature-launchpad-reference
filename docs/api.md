# API contract

> **NON-PRODUCTION TRUSTED-HEADER REFERENCE:** caller-supplied headers are not authentication.

The API exposes one launch-request resource. It has no list, search, filter, policy, scoring, model,
provider, deployment, or operations endpoint.

## Identity headers

Every command requires exactly one of each header:

| Header | Contract |
|---|---|
| `X-Reference-Actor-Id` | Case-sensitive, 1-128 characters, with no edge whitespace, comma, or control character. |
| `X-Reference-Actor-Role` | Exact `Requester`, `Product`, or `AI-Risk`. |

The role must match the command. Read routes consume no identity and establish no read-authorization
policy.

## Routes

| Method and path | Required role | Success |
|---|---|---|
| `POST /api/launch-requests` | `Requester` | `201 Created`, `Location`, and resource |
| `POST /api/launch-requests/{id}/approvals/product` | `Product` | `200 OK` and resource |
| `POST /api/launch-requests/{id}/approvals/ai-risk` | `AI-Risk` | `200 OK` and resource |
| `POST /api/launch-requests/{id}/rejection` | `Product` or `AI-Risk` | `200 OK` and resource |
| `GET /api/launch-requests/{id}` | none | `200 OK` and resource |
| `GET /api/launch-requests/{id}/audit` | none | `200 OK` and ordered audit |

IDs must use the canonical lowercase hyphenated GUID form.

## Create a request

Creation accepts JSON with exactly one required field:

```json
{
  "featureName": "Customer support answer assistant"
}
```

`featureName` is trimmed and must contain 1-120 characters. It identifies the AI feature being
governed; it does not add policy or risk metadata. Missing, malformed, non-string, empty, overlong, or
unknown fields return `400 invalid_request_body`. A malformed creation body has no request-attached
audit because no request exists.

The resource shape is:

```json
{
  "id": "6cb42d6c-b533-44c8-8eaa-f4b90cebd573",
  "featureName": "Customer support answer assistant",
  "status": "Pending",
  "requesterActorId": "requester-1",
  "approvals": {
    "product": null,
    "aiRisk": null
  },
  "rejection": null,
  "version": 0,
  "createdAtUtc": "2026-07-23T01:00:00.0000000Z",
  "updatedAtUtc": "2026-07-23T01:00:00.0000000Z"
}
```

Approval objects contain `actorId` and `recordedAtUtc`. A rejection contains `actorId`, `actorRole`,
and `recordedAtUtc`. Nullable decision objects remain present as `null`.

## State and refusal behavior

- A request starts `Pending`, version `0`.
- The first valid approval fills its fixed role slot and increments the version.
- The second approval must use another actor and changes the request to `Approved`.
- Product and AI-Risk approvers must each differ from the requester and from each other.
- Product or AI-Risk may reject a `Pending` request. No rejector-separation rule is added.
- `Approved` and `Rejected` are terminal.
- Duplicate approvals and terminal commands return audited `409` conflicts.
- Submission retries create separate requests. There is no idempotency key or ETag.

Concurrent writes serialize through SQLite. Distinct approval roles can both succeed. Duplicate
slots produce one success and one audited conflict. One actor racing both approval roles produces
one success and one audited separation conflict. A rejection race is evaluated against the preceding
committed state.

## Audit

Audit retrieval returns the request identity and events ordered by per-request `sequence`:

```json
{
  "requestId": "6cb42d6c-b533-44c8-8eaa-f4b90cebd573",
  "featureName": "Customer support answer assistant",
  "events": [
    {
      "sequence": 1,
      "occurredAtUtc": "2026-07-23T01:00:00.0000000Z",
      "action": "Submit",
      "actorId": "requester-1",
      "actorRole": "Requester",
      "outcome": "Succeeded",
      "reasonCode": "request_created",
      "statusAfter": "Pending",
      "versionAfter": 0
    }
  ]
}
```

Actions are `Submit`, `ProductApproval`, `AiRiskApproval`, and `Rejection`. Outcomes are `Succeeded`
and `Refused`. Once an existing target is loaded, identity, authorization, terminal, duplicate, and
actor-separation refusals append an event with the unchanged durable snapshot before the error
response.

Routing or method failures, malformed creation bodies, non-empty decision bodies, malformed IDs,
missing targets, reads, and database availability failures have no request-attached audit.

## Problems

Problems use `application/problem+json`:

```json
{
  "title": "Approval is already recorded",
  "status": 409,
  "code": "approval_already_recorded",
  "requestId": "6cb42d6c-b533-44c8-8eaa-f4b90cebd573"
}
```

`requestId` is present only after an existing target is resolved.

| Status | Codes |
|---|---|
| `400` | `invalid_request_body`, `body_not_allowed`, `invalid_request_id` |
| `401` | `identity_missing`, `identity_invalid` |
| `403` | `role_missing`, `role_unknown`, `role_mismatch` |
| `404` | `request_not_found` |
| `409` | `request_terminal`, `approval_already_recorded`, `requester_cannot_approve`, `approvers_not_distinct` |
| `503` | `database_unavailable` |
