---
change: "<lowercase-kebab-name>"
status: "draft"
roadmap: "<exact canonical Phase heading>"
---

# Change Record - <observable change name>

## Intent and first human confirmation

**Observable outcome:** <what becomes observably true>

**Initial human confirmation:** `pending`

Text records an attested command; it does not authenticate identity.

## Scope

- <bounded scope>

## Out of scope

- <explicit exclusion>

## Activated proof obligations

| Constraint | Why activated | Expected evidence | Initial state |
|---|---|---|---|
| `<constraint.id>` | <reason> | <expected evidence> | pending |

## Short implementation plan

1. <one bounded implementation step>

## Evidence

`pending`

When work begins, replace the pending marker with append-only attempt rows. Repeat a constraint id
when a failed/pending attempt is followed by new evidence; the latest row controls readiness.

| Constraint | Result | Evidence |
|---|---|---|
| `<constraint.id>` | pending | <command, artifact, or observation> |

## Corrections

`pending`

## Architecture

Add this section only when a named load-bearing trigger requires the sibling
`changes/<record-stem>/design-under-test.md`.

## Architecture review

Add this section only for triggered architecture and record the actual returned result after return.

## Closeout

Add before final review:

| Disposition | Record |
|---|---|
| delivered | <scope-preserving delivered outcome> |
| remaining | <approved remaining outcome or explicit none> |
| discovered | <evidence-backed discovery or explicit none> |
| evidence | <Roadmap/changelog evidence> |

## Independent final review

**Returned verdict:** `pending`

After the no-edit reviewer returns, append attempts as `### Attempt N` and record reviewer/date,
reviewed target, remote/ref, start/completion local and remote heads, stability, actual verdict,
gates, summary, evidence, and this table:

**Reviewer/date:** <Reviewer Agent, YYYY-MM-DD>

**Reviewed target:** `<full commit SHA>`

**Remote:** `<remote>`

**Ref:** `<refs/heads/branch>`

**Start local head:** `<full commit SHA>`

**Start remote head:** `<full commit SHA>`

**Completion local head:** `<full commit SHA>`

**Completion remote head:** `<full commit SHA>`

**Stability:** `STABLE|STALE`

**Returned verdict:** `PROMOTE|BLOCK`

**Gates:** <actual gate results>

**Evidence:** <durable evidence links or observations>

**Summary:** <actual concise reviewer summary>

| Residual | Disposition | Notes |
|---|---|---|
| `<residual.id>` | covered | <non-placeholder disposition evidence> |
