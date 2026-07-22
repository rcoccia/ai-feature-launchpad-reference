# Reference — Agents

> A **subagent** is a context-isolated agent instance with its own tools and model. It enforces
> a **role** — by its tool boundary and by running in a fresh, unbiased context. The human
> dialogues with a single **tower** (the coordinator); the tower delegates to these agents
> itself when isolation helps. The human does not switch agents by hand.

## Profile availability

LIGHT installs `reviewer-agent` and `architect-agent`: independent judgment is mandatory and the
load-bearing design route must remain available. Full additionally installs Requirements and
Planner for explicitly justified specialization.

## The four phase agents

| Agent | Profile | Enters | Role | Tools | Boundary |
|---|---|---|---|---|---|
| `requirements-agent` | Full | Optional after readiness when behavioral complexity or useful isolation is explicit | Elicits requirements and returns a structured handoff for the canonical Change Record; the main Tower handles eligible LIGHT requirements by default. | `read`, `search`, `edit` | Not an inception producer or mandatory LIGHT phase; non-code scope remains a judgment boundary. |
| [`architect-agent`](../../../.github/agents/architect-agent.agent.md) | LIGHT | Inside a selected delivery slice, only when design is load-bearing | Designs the architecture and load-bearing decisions; writes an architecture note, an ADR, and the terse **design-under-test** the challenger will see. | `read`, `search`, `edit` | Does **not** implement code, invent business semantics, or produce the inception constitution. |
| `planner-agent` | Full | Optional when task/evidence coordination exceeds a simple bounded plan | Returns a structured detailed-plan/evidence handoff for integration into the Change Record or its explicitly triggered companion; the main Tower plans eligible LIGHT work by default. | `read`, `search`, `edit` | Does not implement, create a parallel lifecycle record, or become a mandatory pipeline stage. |
| [`reviewer-agent`](../../../.github/agents/reviewer-agent.agent.md) | LIGHT | At inception readiness, design review, and finished-change review | The **independent judge**. For final review it records target/local/remote start and completion observations and returns the complete actual result to the Tower for append-only recording. | `read`, `search`, `execute` | **No `edit` — on purpose.** It cannot fix or record what it judges. |

## The load-bearing boundary: producer != judge

The `reviewer-agent` has **no `edit` tool**, and it runs in a **fresh, context-isolated
subagent** — not a fork of the context that produced the work. That is what makes *producer is
not the judge* real (not a promise in prose):

- it **cannot** silently fix a problem into a pass — it can only PROMOTE or BLOCK and record the gap;
- its verdict is **not anchored** by the reasoning that produced the artifact;
- for a **design** review it is even blindfolded to the architect's justification — it sees only
  the design-under-test, so it cannot inherit the author's conclusion.

Before final change review, the Tower as coordinator stops or idles all other writers, names one
producer branch owner, and requires protected work to be committed and pushed. The reviewer records
the reviewed target, remote/ref, and local/remote heads at start, then rechecks target/remote/ref
and records completion heads; missing or moved relevant observations return `STALE`/`BLOCK`. It
returns the full actual result, and only afterward does the Tower write it.

This role boundary and those observations do not authenticate reviewer identity, prove
single-writer compliance, deterministically prevent outside writes, or guarantee semantic quality.
Those remain reviewer/human residual judgments.

The other three agents have `edit`, but their non-goals (no code, no invented semantics) are
**judgment** boundaries, declared as such — reinforced downstream by the reviewer, not by tools.
For LIGHT delivery they are conditional specialists, not a phase chain.

## This is checked, not just claimed

In the method and Full profile, the rule "no agent's description may claim a boundary its tools
contradict" is enforced deterministically by [`check_agents.py`](gates.md)
(`TEC-AGENTCFG-01`). LIGHT copies the already-checked Reviewer/Architect configurations but does
not activate the framework-development agent workflow. A role boundary is put in **config**
(`tools`) wherever granularity allows; otherwise it is a declared judgment boundary.

## Why a subagent and not just a skill

A subagent is the right primitive when the output is a **small summary/verdict** that must be
formed in an **independent context** (a review). It is the wrong primitive when the output is a
large artifact that must return to the coordinator's working context. That is why the review
runs in a subagent, but planning and coding do not.

## See also

- The skills that delegate to these agents: [`skills.md`](skills.md)
- The `check_agents.py` gate: [`gates.md`](gates.md)
- Producer != judge in context: [`../explanation/overview.md`](../explanation/overview.md#producer--judge)
