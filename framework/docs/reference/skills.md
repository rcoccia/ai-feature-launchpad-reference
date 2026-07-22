# Reference — Skills

> A **Skill** is on-demand guidance. It enforces nothing by itself: deterministic enforcement lives
> in [Gates](gates.md), while independent semantic judgment lives in
> [Subagents](agents.md).

## LIGHT core

LIGHT installs the seven Skills needed for the proportional default lifecycle.

| Skill | What it does | Verdict / gate |
|---|---|---|
| [`bootstrap-tower`](../../../.github/skills/bootstrap-tower/) | Main-Tower, interview-first THIN constitution with canonical phase lifecycle. | `scaffold_constitution.py --check` |
| [`inception-readiness`](../../../.github/skills/inception-readiness/) | Independent coherence and human-deferral judgment before the first delivery. | PASS/BLOCK; `--readiness` |
| [`plan-slice`](../../../.github/skills/plan-slice/) | Consumes `--current-phase` without fallback, forms a contextual judgment, writes exactly one dated Change Record, and stops for initial human confirmation. | `--current-phase`; `check_change_record.py` |
| [`architecture-review`](../../../.github/skills/architecture-review/) | Challenges a load-bearing design before code. | SOUND/REWORK/ESCALATE; `check_architecture.py` |
| [`review-slice`](../../../.github/skills/review-slice/) | Runs deterministic and semantic final review on a frozen target. | PROMOTE/BLOCK; `review_slice.py` |
| [`replan-and-correct`](../../../.github/skills/replan-and-correct/) | Routes a discovery to implementation, slice, or governance/strategy correction. | Conditional existing gates |
| [`record-closeout`](../../../.github/skills/record-closeout/) | Before target freeze, prepares changelog, scope-preserving Roadmap Delta, and Closeout in the Change Record. | `changelog.py` |

The main Tower owns eligible LIGHT planning and delivery. Its planning judgment raises only
consequential concerns it genuinely sees; options remain hypotheses until human confirmation.
Architect enters only for load-bearing design; Reviewer remains fresh, no-edit, and mandatory.
The selector deterministically advances delivered/partial/planned state and blocks exhaustion;
humans alone decide whether an explicit `deferred` status is appropriate.

## Full opt-in

Full adds framework-development evaluation through `run-slice-evals` and the optional Authority/
GOVERNED Skills `classify-data`, `assess-cloud-workload`, `assess-security-boundary`,
`request-policy-waiver`, and `authority-policy-reconciliation`. Those components are absent from a
LIGHT copy. Run the canonical installer with `-Profile Full` before following a Full-only route.

Requirements and Planner specialization are Full-only **agents**, not Skills. Their presence does
not create an automatic phase pipeline.

## The pattern

A Skill may run a deterministic pre-check, then delegate semantic judgment to an independent
reviewer. Form is necessary, not sufficient. For final review, target/head observations and the
single-writer freeze are audit evidence; merge readiness requires the shared model's reviewed,
stable-PROMOTE, evidence, closeout, and residual predicates.

## See also

- [Gates and profile availability](gates.md)
- [Agents and profile availability](agents.md)
- [Three primitives](../explanation/overview.md#the-three-primitives)
