# Operational replay

Use this checklist while running the [from-zero tutorial](from-zero-replay.md). It keeps the replay
fresh, measurable, and bounded at review-ready.

## Invocation contract

The replay command must supply:

- the public repository and `refs/heads/rcoccia-phase2-replay-docs`;
- an empty disposable local repository path;
- a parent session identifier for `send_session_message`;
- delegated autonomy to use the tutorial's human-confirmed semantics;
- an explicit prohibition on `ask_user`, final review, a second cloud repository or PR, and merge.

The agent may make local commits and may use a local branch or tag to freeze checkpoints. It must not
inspect private conversation history or copy product source/tests from the public reference.

## Checklist

| Checkpoint | Required observation | Record |
|---|---|---|
| Start | Target is an empty initialized Git repository; source branch and resolved head are recorded. | start timestamp, paths, branch head |
| LIGHT | Installer copies the LIGHT profile and no constitution or product is seeded. | command, copied/preserved counts |
| Inception | Mission, Constraints, the two-phase Roadmap, and inception ADR are authored from confirmed semantics; Phase 1 is current and Phase 2 is planned. | artifact list, readiness verdict |
| Constraint set | Six inherited and four product laws are active, for ten total. | provenance output |
| Plan | The sole local delivery record is one confirmed Phase 1 Change Record before design or code. | record path, confirmation text, gate |
| Design | One named companion resolves state/audit and identity boundaries. | design commit/ref |
| JSON contract | Design and DTOs match the nested request and audit examples in `docs/api.md`, including per-decision `recordedAtUtc` and per-event `occurredAtUtc`. | field-by-field checklist and contract tests |
| Architecture | Independent no-edit challenge returns fresh stable `SOUND`. | reviewer, target SHA, result |
| Product | .NET 10 Minimal API, direct SQLite, integration tests, workflow, and public docs exist. | changed paths |
| Product proof | Locked restore, zero-warning Release build, 28 tests, and vulnerability scan pass. | command outputs, durations |
| Roadmap advance | Phase 1 is truthfully checked at closeout; readiness stays green and the selector advances to exact Phase 2. | Roadmap diff, readiness and selector outputs |
| Governance proof | The historical Phase 1 Change Record plus readiness, docs, autonomy, provenance, and review pre-check pass. | gate outputs |
| Boundary | Merge readiness fails only on `confirmed` / final verdict `pending`. | expected failure |
| Exit | Local target is clean and review-ready; Phase 2 is current and unchecked, with no second local Change Record. | end timestamp, HEAD |

## Escalation rule

Never call `ask_user`. Resolve ordinary implementation choices from the confirmed artifacts, public
docs, and the smallest constraint-preserving design.

A blocker is material only when proceeding would require changing confirmed product semantics,
Mission, Constraints, approved stack, identity boundary, or the review-ready exit. For one material
blocker, send one concise message:

```text
send_session_message(
  session_id = <parent-session-id-from-invocation>,
  message = "BLOCKED: <fact>. Impact: <governed artifact or constraint>. Smallest decision needed: <decision>."
)
```

Then idle. Do not send repeated status messages and do not continue by inventing authority.

## Evidence log

Keep an append-only replay log in the disposable target. For each step record:

| Field | What to capture |
|---|---|
| step | Number and observable checkpoint |
| started/completed | UTC timestamps |
| artifacts | Created or changed paths |
| commands | Exact commands and exit codes |
| latency | Wall-clock duration |
| rework | Failed attempt followed by correction |
| defects | Product, test, documentation, dependency, or record defect |
| friction | Ambiguity, missing prerequisite, unclear instruction, or avoidable manual work |
| evidence | Commit SHA, gate output, test count, or other durable observation |

Never erase a failed attempt. Append its correction and identify whether the tutorial, public product
docs, or implementation caused the gap.

## Cleanup

After evidence has been sent to the parent and acknowledged:

1. Stop any API process by its recorded process ID.
2. Remove only the disposable target and public source clone.
3. Do not delete or alter the main reference checkout.
4. Retain the evidence log in the parent-owned evidence location.

Cleanup is after review-ready evidence capture. A cleaned directory without retained evidence is not
a successful replay.

## Review-ready exit

The replay is complete only when all required local gates and product proof pass, the working tree is
clean, and merge readiness has the single expected `confirmed` / `pending` boundary. Stop before final
review. The sole local Change Record remains anchored to delivered Phase 1. Do not create a Phase 2
Change Record or close Phase 2: the retained external replay report is its evidence. The main
reference's merged PR 3 supplies GitHub review and merge proof; the disposable replay does not
duplicate it.
