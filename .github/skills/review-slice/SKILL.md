---
name: review-slice
description: 'Independently reviews a completed confirmed Change Record and frozen implementation target, returning PROMOTE/BLOCK without editing. Use after implementation or correction, before governed merge, or when asked to review or promote a change.'
---

# Review Change

Judge the approved Change Record and frozen target; do not redesign or fix them.

## Workflow

1. The Tower stops every other writer, names one branch owner, and has that producer commit and push
   the Change Record, implementation, design, closeout, and evidence.
2. The no-edit reviewer records the full reviewed target, remote/ref, and start local/remote heads.
   Missing or mismatched observations require `STALE` and actual `BLOCK`.
3. Run:

   `python -B .github/skills/review-slice/scripts/review_slice.py changes/<dated-record>.md
   --constraints constitution/constraints.md`

   A failure means the implementation target is not reviewable. Correct the record or evidence
   upstream; never weaken the pre-check.
4. Run the commands and inspect the artifacts named in the Evidence table. Judge the observable
   outcome, every activated obligation, scope, no-drift/no-invention, correction freshness, and
   teaching-to-test. Check concrete omissions against Mission, Roadmap, and all active Constraints.
5. Immediately re-observe target and remote/ref. Return `STABLE` only when all start/completion
   local/remote heads equal the reviewed target; otherwise return `STALE` and actual `BLOCK`.
6. Return reviewer/date, target/ref, all head observations, stability, actual `PROMOTE|BLOCK`,
   gates, summary, evidence, findings, and one disposition for every review-routed residual of every
   activated hard constraint.
7. The Tower appends the actual return to `## Independent final review` only after return. A stable
   `PROMOTE`, complete residual dispositions, and complete closeout permit `status: "reviewed"` and
   the merge-ready gate. No separate `review.md` exists.

## Blocking boundary

`BLOCK` requires a concrete violated outcome, activated obligation, active constraint, declared
scope/evidence item, required gate, drift/invention rule, target-stability rule, or concrete omitted
obligation. Preferences, future mechanisms, and explicitly deferred evidence are non-blocking.

## Gotchas

- **Producer is not judge:** use the fresh no-edit Reviewer Agent.
- **Recorded text is not identity:** target/head observations and tool boundaries are audit evidence,
  not authentication or semantic proof.
- **A later protected change is stale:** implementation, plan, design, obligation, evidence, Roadmap,
  or changelog edits require a new frozen target and fresh review.
- **No verdict prewriting:** the Tower records only the actual returned result.
- **No legacy adapter:** consume the Change Record; historical `specs/` paths resolve only through
  `changes/0000-control-tower-baseline.md`.

## References

- Pre-check: `./scripts/review_slice.py`
- Shared model: `framework/scripts/change_record.py`
- Executor: `.github/agents/reviewer-agent.agent.md`
