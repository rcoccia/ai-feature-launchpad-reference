# Control Tower Operating Model

> Domain-agnostic companion to the Control Tower Manifesto (`framework/doctrine/MANIFESTO.md`).
> The Manifesto declares the principles; this document specifies the governance
> loop and the role boundaries the Manifesto refers to. It is a cleaned,
> reusable copy: it carries no workspace-, platform-, or domain-specific names.
> Concrete instances of these rules live in implementations of this method, such as
> the data-mesh reference towers (external).

## Purpose

This document defines what a control tower is and how it operates.

A control tower is the AI copilot that, under human command, builds a complex software system. It works with the human across the delivery loop and keeps every decision and implementation aligned to the tower artifacts — Vision, Constraints, and Roadmap. It may delegate bounded coding or testing to sub-agents, but that delegation is an execution detail.

```text
human + tower (copilot)  aligned to  Vision / Constraints / Roadmap
   ->  feature: select -> design -> architecture-review -> plan -> code -> test  ->  verified software
```

## Role Boundaries

| Role | Responsibility | Non-goals |
| --- | --- | --- |
| Human / architect | Owns Vision, Constraints, Roadmap; sets direction, selects and approves features, resolves architecture choices | Does not hand-edit every output; does not micromanage per token |
| Control tower (copilot) | Drives the loop with the human: selects the next feature, designs, plans, codes, tests, coordinates independent review, and records — always aligned to the artifacts | Does not take command, and does not let decisions or code drift from the artifacts |
| Execution sub-agent | Implements a bounded coding or testing task delegated by the tower | Does not redefine strategy, broaden scope, or invent missing business semantics |
| Sole producer / branch owner | Owns the branch during the final-review handoff; commits and pushes all protected work before review | Does not share branch ownership with another active writer during final review |
| Independent reviewer | Observes the committed target and local/remote heads, judges without edit access, re-observes heads, and returns the complete actual result | Does not edit, record its own verdict in the repository, or claim authenticated identity |

For a greenfield project, **THIN inception belongs to the main Tower**, before the delivery loop:
it interviews the human and writes the strategy-level Mission, Constraints, and Roadmap. The
Requirements/Planner Agents may be delegated only after `inception-readiness` when explicit
complexity earns isolation; they are not mandatory phases. The Architect Agent begins only inside a
selected delivery slice with a load-bearing design. A missing design is an open question or roadmap
capability, never architecture silently selected during inception.

## Standard Loop

Each tower operates as a repeatable delivery loop:

1. **Sense**: inspect repository state, normative specs, gap registers, recent evidence, tests, and user intent.
2. **Choose next change**: decide with the developer what feature, fix, gap closure, or validation matters next.
3. **Plan visibly**: create one dated Change Record with the outcome, current Roadmap anchor, short
   plan, and activated proof obligations with reasons and expected evidence; stop for human
   confirmation before implementation.
4. **Delegate and implement**: give a bounded prompt to a worker subagent or implementation agent when execution is needed.
5. **Validate and close out**: append evidence/corrections, prepare the scope-preserving Roadmap
   delta and deterministic changelog, and record closeout in the Change Record.
6. **Freeze**: the sole producer commits and pushes implementation, Change Record, triggered design,
   closeout, and evidence. The Tower stops every other writer and names that producer as branch owner.
7. **Review and return**: the no-edit reviewer records the reviewed target, remote/ref, and
   local/remote start heads; judges the slice; rechecks the target and remote/ref; re-observes
   local/remote completion heads; and returns its complete actual result. Missing or moved relevant
   observations are `STALE` with `BLOCK`.
8. **Record the return**: only after the reviewer returns, the Tower appends exactly its target,
   observations, stability, verdict, evidence, and residual dispositions to the same Change Record.
9. **Check and merge**: stable `PROMOTE`, complete residual dispositions, `status: "reviewed"`, and
   merge-ready success are required; the human decides whether to merge.

The tower requires and governs evidence, but the product toolchain and CI produce build, test, lint,
and scan evidence. The Change Record names commands and evidence per obligation, and the independent
reviewer judges adequacy. The core does not implement a universal build system, language discovery,
test runner, scanner, coverage threshold, or language adapter.

## Feature-first Change Rule

Every new governed change is a bounded delivery or explicitly authorized spike:

- **Delivery (default):** ends with the smallest vertical, observable, verifiable capability that
  did not exist before the change. The Change Record states that outcome before implementation. An ADR,
  a design, selecting a component, or an architecture review is an internal lifecycle step, never
  the roadmap feature by itself.
- **Spike (exception):** reduces one explicit uncertainty and produces no product capability. It
  requires human authorization, one question, a timebox, expected evidence, and an exit criterion:
  `decide`, `block`, or `experiment`. A spike cannot grow into a full future design.

Roadmap phases describe capability or outcome, not planning activities. Canonical `## Phase`
sections derive lifecycle from valid top-level items: all checked is **delivered**; the first
non-deferred phase with any unchecked item is **current**, including partial work; later eligible
phases are **planned**. Optional `**Status:** deferred` keeps history inspectable while excluding it
from selection. Historical entries are evidence, not a reason to retroactively rewrite them, and
deferral is always a human strategy decision rather than an inferred state.

An optional, exact top-level `**Lifecycle:** complete` declares that every non-deferred phase is
delivered and no work is currently approved. It is readiness-valid but not selectable. Without the
marker, the same all-delivered shape is accidental exhaustion and blocks for human re-cadence. A
marker beside any eligible unchecked phase is contradictory and blocks.

All active constraints remain binding. Every Change Record starts with the universal baseline and
adds obligations only through explicit risk/impact triggers. The Tower proposes applicability and
reasons; deterministic gates may add obligations only when certainty is mechanical; the human
confirms the initial set; the reviewer checks concrete omissions. No automation silently removes or
de-escalates an obligation.

## LIGHT Execution Profile

LIGHT is proportional treatment inside `delivery`, not a fixed obligation tier. It applies when the
delivery is bounded and has no Authority/policy delta, new dependency, active constraint-set change,
or load-bearing design.

The main Tower is then the sole producer/branch owner: it elicits, writes the one Change Record,
implements, and closes out in one producer context. Requirements and Planner remain optional
specialists, invoked only when behavioral complexity or task/evidence coordination explicitly
earns isolation. Architect remains conditional on load-bearing design. There is no automatic
Requirements -> Planner -> Architect pipeline.

Planning is **judgment-led**, not a blank intake form. Before writing, the Tower always reads
Mission, current Roadmap state, and active Constraints, plus the critique register when the instance
carries one; it selectively reads prior decisions, Change Records, reviews, and evidence related to the
current capability, affected constraints, dependencies, or changed surfaces. It forms and states a
working judgment, then raises only consequential risks, tensions, assumptions, or omissions it
genuinely perceives. Questions are adaptive and one decision at a time; alternatives, trade-offs,
or a recommendation appear only when useful. “No material concern found” is valid. Every proposal
remains a hypothesis until human confirmation and cannot enter EARS or accepted decisions before
then. Uncertain relevance widens the evidence read; it never becomes an inferred fact.

The final Reviewer is never compressed away: it remains fresh, no-edit, and independent under the
single-writer freeze. If scope, dependency, Authority/policy applicability, active constraints, or
the design boundary becomes uncertain, widen the Correction Radius and stop or delegate before
continuing. Inception readiness runs at inception and after genuine strategy correction, not as
routine ceremony for every delivery.

**Review the approved contract; do not redesign the slice.** A final review may block only for a
concrete violation of confirmed requirements, active constraints, declared scope/evidence, required
gates, governing drift or invention, teaching-to-test, or target stability. A preferred refactor,
new requirement, new gate/artifact, future design/improvement, or explicitly deferred evidence is
non-blocking. A useful observation may enter existing `discovered` semantics; it creates no
mandatory backlog. After a concrete correction, review only affected stale evidence plus the
unchanged contract boundary. This authority limit is semantic reviewer/human judgment, not a
classifier or numeric budget.

## Correction Radius Rule

When implementation reveals a new fact, correct the **nearest authoritative artifact** before
continuing the affected code. Classify the correction semantically into exactly one radius:

| Radius | Use only when | Required action |
|---|---|---|
| **implementation** | confirmed behavior, outcome, Roadmap, active constraint set, Authority/policy applicability, dependencies, and load-bearing design are unchanged | continue with normal code and product-test evidence; no replan |
| **slice** | local change semantics change, while outcome, Roadmap, active constraint set, Authority/policy applicability, and dependencies remain unchanged | update affected Change Record sections and triggered companion before affected code; append the correction and invalidate only stale evidence/review attempts |
| **governance/strategy** | outcome, Roadmap, Gap Register, Authority binding/applicability, dependencies, Mission, or Constraints may change | run the full governed replan and preserve its existing severity and human-routing rules |

For a slice correction, rerun the Change Record pre-check before affected code continues, rerun
affected product evidence after implementation, and obtain a fresh independent final review before
merge. Unrelated evidence remains valid. The correction alone requires neither constitution
readiness nor a course-correction ADR. A changed load-bearing decision still follows the normal
architecture ADR and independent architecture-review.

For governance/strategy, invalidate stale downstream evidence. Rerun constitution readiness when
Mission, Constraints, or Roadmap changed; any Mission or Constraints change stops for the human and
requires an ADR. Policy applicability changes always use this wider radius. If the radius is
uncertain, choose the wider path and stop for the human.

Record the reason in the Change Record's nearest decision/context, Corrections, evidence, or review
surface. Do not create an adjustment log. Radius classification is reviewer/human
judgment, not a deterministic gate.

## Design Review Rule

**Producer ≠ judge applies to the design, not only to the code.** When a change involves a
**load-bearing** architectural decision, the design is challenged **independently before code** —
the `architecture-review` gate, executed by the
`reviewer-agent` (no `edit`), returning **SOUND**, **REWORK**, or **ESCALATE**. Bad
architecture is bad code: a design error propagates and costs more downstream than a coding
error.

An NFR triggers this lifecycle only when satisfying, changing, or preserving it requires that
load-bearing architectural decision. NFR presence or evidence work alone does not.

Two properties make the challenge genuinely adversarial rather than the design's author
approving itself:

- **Structural blindfold.** The challenger receives **only** the terse `design-under-test.md`
  (components, data flow, the decision, constraints touched), `constraints.md`, and the
  **roadmap** (so it knows the target) — never the ADR's persuasive justification. A judge
  cannot inherit a conclusion it has not read.
- **Two lenses, not one.** The challenger holds **both** *minimise-for-this-slice* (YAGNI) and
  *walking-skeleton-for-the-known-target* (build the real shape early to de-risk), kept
  separate. A challenger anchored on minimalism alone rejects every forward-looking design —
  a bias as harmful as the architect's confirmation bias (learned by dogfooding this gate).

The verdict is **three-way on purpose**, because a binary SOUND/REWORK forces the challenger
to resolve a **scope decision** — which the Autonomy Envelope reserves for the human — inside a
technical judgment:

- **SOUND** — coherent and justified; proceed.
- **REWORK** — a **frame-independent defect** (miscalibrated justification, a constraint
  violated or worsened, an internal contradiction), wrong regardless of scope framing;
  corrected upstream (tenet 8) before code.
- **ESCALATE** — a genuine **scope-vs-architecture tension** (defensible as a walking skeleton,
  over-built as YAGNI); the gate states both theses and routes the decision to the **human**,
  it does not decide.

This is **tiered, not ceremony** (tenet 1): it runs for designs expensive to get wrong, not
every slice. The deterministic half (the design is *challenge-able*: a design-under-test
exists, the ADR weighed ≥2 alternatives and named a negative consequence) is enforced by
`check_architecture.py`; the semantic challenge is the reviewer's hostile checklist. Residual
(tenet 12): an LLM challenging an LLM is judgment, not proof, and the challenger itself can be
biased — *who challenges the challenger?* the human. The gate's usefulness must be measured
(real REWORKs/ESCALATEs) or retired. This closes critique **C16**.

Architecture review stays inside a delivery change. It challenges **one** load-bearing decision and
the constraints directly affected by that decision; it must not demand implementation or
production evidence explicitly deferred by the Change Record. The method guidance budgets ADRs at
150 lines or fewer, the design-under-test at 80 lines or fewer, LIGHT planning at 20-30 minutes,
and all design work at 60 minutes or fewer. A budget overrun calls for scope reduction or a
human-authorized spike, not more prose.

One automatic review round reports at most five high-confidence findings. **SOUND** proceeds;
**ESCALATE** goes to the human; **REWORK** stops and returns to the human rather than auto-looping.
A second round requires explicit human authorization. These are proportionality guidelines and
independent-review judgments, not fragile deterministic line or time gates.

## Reuse And Common Promotion Rule

Reuse before invention. Every tower must actively inspect the proven reference track before designing an equivalent mechanism.

When a new tower slice overlaps a capability the proven track already implements, classify the overlap before planning implementation:

- **Promote common**: the capability is level-agnostic and should become a shared concept or, after a second validated consumer exists, shared deterministic runtime.
- **Adapt locally**: the discipline applies, but the artifact vocabulary is level-specific.
- **Keep track-specific**: the capability encodes one level's semantics and must not leak into another level.
- **Defer extraction**: the concept looks common, but common code would be speculative until another track proves real use.

The tower must make that classification visible in the plan or review. The architect should not have to argue repeatedly that a proven element might be reusable.

A recurring first-class candidate is a **shared change-delivery context envelope**: a wave- or slice-local context carrying identity, branch/change coherence, repository or data-product anchors, trigger or change intent, platform role anchors, evidence sources, warnings, and blocking findings. Towers should reuse or promote such an envelope before inventing a track-specific bootstrap. Level-specific contract semantics still belong in the level artifact, never in the shared envelope.

## Evaluation Harness Boundary

The evaluation harness is a validation harness, not a hosting environment.

The tower must treat the harness as a place to exercise conversations, sandbox materialization, scenario fixtures, evaluator checks, and reports. It can prove or falsify behavior; it must not become the product runtime or the place where a missing capability is hidden.

When a feature gap appears in the harness, classify it before changing code:

- **Product/skill/runtime gap**: implement or plan the missing capability in the product itself, then add or update coverage to prove it.
- **Test-harness gap**: update the harness only when the validation framework itself cannot express an already-defined behavior.
- **Scenario/fixture gap**: update fixtures or scenario expectations only when the expected behavior is already valid and the test data is stale or incomplete.
- **Environment prerequisite**: classify missing external access, credentials, or live platform state as prerequisite, not as feature success.

Do not modify the harness runtime to host a missing feature. Do not treat a passing setup, sandbox, or contract validation as production hosting.

## Evaluation Prompt Integrity Rule

Do not cheat with evaluation opening prompts.

Natural scenarios must simulate a plausible stakeholder conversation, not hand the agent a procedural checklist. An opening prompt may describe the business situation, stakeholder role, broad intent, and hard safety constraints. It must not preload the exact solution path.

For natural scenarios, the opening prompt must not provide:

- exact internal file names, flow names, or artifact paths the agent should create;
- exact runtime tools, scripts, gates, or checker names to invoke;
- strict schema field names solely to make validation pass;
- a step-by-step implementation or handoff checklist;
- hidden acceptance criteria phrased as user instructions;
- answers to clarifying questions the agent is supposed to ask;
- tower/worker/test implementation details that a real stakeholder would not know.

If a passing scenario relies on that kind of scaffolding, the tower must label it as guided or deterministic coverage, not as natural-agent proof.

When a natural scenario fails, the tower must not fix the failure by enriching the opening prompt with the missing internal behavior. It must classify the gap and, when appropriate, fix the prompt, skill, runtime validator, fixture, or evaluator. The harness validates the behavior; it must not supply the behavior.

The lesson generalizes to every tower:

```text
A feature is not closed when it validates inside a contract;
it is closed only when the required facts travel explicitly, verifiably,
and non-inventably into the implementation.
```

Replace the contract name with the level-specific contract for your domain. The closeout gate remains the same: contract validation is necessary, but implementation readiness is the feature boundary.

## Roadmap Re-cadence Rule

**The Roadmap is reopenable, not permanently terminal.** It is the sequenced, bounded set of
currently approved capability. All phases delivered without an explicit lifecycle marker is
accidental exhaustion and means **replan the next wave**. All phases delivered with
`**Lifecycle:** complete` means no work is currently approved, not deletion or archival. If a new
requirement arrives months later, the human may reopen it through a governed transition.

The load-bearing signal: **a slice with no roadmap phase is a replanning trigger, not a valid
state.** A dated slice that declares "no phase" is either drift or the sign that the roadmap is
exhausted and must be re-derived (trigger *roadmap-exhausted / cycle-boundary* in
`framework/doctrine/artifacts-skills-lifecycle.md` §6.1, handled by `replan-and-correct`). Tolerating
"no phase" slice after slice is how a tower silently unmoors from its own constitution —
observed, and corrected, in this method's own history (critique **C17**, ADR-11).

The canonical Roadmap analyzer in
`.github/skills/bootstrap-tower/scripts/scaffold_constitution.py` makes accidental exhaustion fail
closed for `--check`, `--readiness`, and `--current-phase`. Valid complete state passes `--check`
and `--readiness` with no current work, while `--current-phase` and `plan-slice` remain blocking.
Re-cadencing active exhaustion is a governed course-correction. Reopening complete state is one
human-authorized change that removes the marker and adds at least one newly approved, non-deferred
phase with an unchecked item; its confirmed Change Record and newly accepted ADR attest the
decision in the same diff. Either half-transition blocks. Correct upstream; never justify
unanchored slices or add speculative backlog. The analyzer proves explicit syntax and item-derived
state, not identity or strategic wisdom.

## Change Closeout Rule

Every non-trivial completed change must leave its durable trace in the canonical Change Record.

Closeout is prepared **before** the final frozen review target so Roadmap/changelog state is judged
with the implementation. After the return, the Tower appends only the actual final result and
residual dispositions; stable `PROMOTE` plus `status: "reviewed"` permits merge readiness.

At closeout, the tower must update at least one relevant artifact when the slice changes any of these:

- current state or validated baseline;
- next recommended slice;
- open or closed gap;
- architectural decision;
- worker prompt pattern;
- test strategy or test result authority;
- runtime/skill/product boundary;
- autopilot stop condition;
- restart context.

Typical closeout targets (by convention) are:

- the **Mission** document for durable direction changes;
- the **Restart / Session** state for new restart state or operating instructions;
- the **Roadmap / Baseline** document for validated baseline, status, and roadmap movement;
- the **Gap Register** for spec/tower/implementation gaps;
- **Diagnostics** or review files for evidence, failures, and lessons.

### Roadmap Delta

At every **promoted delivery or spike** closeout, reconcile the approved roadmap outcome using
existing artifacts; do not create a new per-slice delta file. Record:

- `delivered`: the exact observable outcome completed;
- `remaining`: the already-approved capability portion not delivered;
- `discovered`: a proposed new capability or dependency supported by evidence;
- `evidence`: at minimum the Change Record and reviewed target, plus implementation/merge
  commit and material CI/eval pointers when available.

For fully delivered approved outcomes, mark `[x]` and append concise evidence. For a partial
approved outcome, the tower may autonomously split or rephrase it into a checked delivered outcome
and unchecked remaining outcome only when the original approved scope and intent are preserved.
Git history and the evidence trace the wording change. A phase remains incomplete while approved
remaining outcomes are unchecked; do not tick a broad parent outcome for partial delivery.
The canonical selector therefore keeps a partial phase current, advances past a fully checked
delivered phase, skips only explicitly deferred phases, and blocks on exhaustion. Adding, retaining,
or removing `**Status:** deferred` is human Roadmap/replan judgment, never a closeout heuristic.
When closeout delivers the final eligible phase, it may add `**Lifecycle:** complete` only with the
confirmed human authorization and accepted ADR in the same candidate. Leaving the final outcome
unchecked or adding a speculative placeholder is not valid closeout.

This autonomy does not authorize strategy. A new capability, priority or order change, new phase,
or strategic dependency stops for human-directed `replan-and-correct` and an ADR when severity
requires. Bugs, gaps, and risks go to the gap register unless later approved as capability.
Technical tasks are lifecycle work, not roadmap outcomes. A spike records its question, exit,
evidence, and roadmap impact but never masquerades as delivered product capability.

The deterministic changelog remains separate. Delivered/remaining classification is semantic
judgment for the independent reviewer; no deterministic semantic-classification gate is claimed.

If a change is purely mechanical and does not change governance state, the Tower records that fact
in its Closeout and final summary:

```text
Tower artifacts unchanged: no governance-state delta from this mechanical slice.
```

This exception is narrow. If a future tower session would need the result to choose the next slice, reproduce the validation baseline, or understand why a decision was made, the result belongs in a tower artifact.

## Worker Prompt Contract

Every worker prompt should specify:

- goal and reason for the slice;
- required inputs and references;
- expected output artifacts;
- allowed files and forbidden files;
- implementation boundaries;
- required unit tests and evaluation-harness tests;
- validation commands;
- explicit statement that the evaluation harness is validation only, not feature hosting;
- for natural evaluation scenarios, explicit no-prompt-cheating constraints and expected stakeholder realism;
- expected implementation-handoff evidence when the slice changes product behavior;
- blocker criteria;
- review evidence expected from the worker.

The tower must not delegate vague work like "improve the agent". It delegates bounded, reviewable slices.

## Autopilot Mode

When the developer authorizes autopilot, the tower continues the loop autonomously:

```text
choose slice -> plan -> delegate/implement -> validate -> review -> commit -> choose next slice
```

Autopilot stops when:

- a blocker requires developer or domain decision;
- tests fail in a way that cannot be safely fixed within scope;
- the tower detects scope drift;
- a change would cross ownership boundaries;
- the next slice is ambiguous or strategic rather than local;
- credentials, secrets, or external approvals are required.

Autopilot does not mean uncontrolled implementation. It means the tower can keep executing the governance loop without asking for permission at every small step, while preserving scope, tests, review, and commits.

Autopilot must apply the Slice Closeout Rule after every completed slice. The tower should not continue to the next autonomous slice while governance artifacts are stale.

The boundary between what the tower may do autonomously and what requires the human — and its deterministic edge — is specified in **Autonomy Envelope** below.

## Autonomy Envelope

Tenet 1 (copilot, not autopilot) and tenet 11 (human governance *at the loop*, not per token) stop being in tension once the boundary is explicit: the tower runs the loop autonomously **inside an envelope** and stops for the human **at the envelope's edge**. Autonomy is about *cadence* — not asking permission at every step — never about *command*: strategy and the governing artifacts stay the human's.

| Class | Autonomous (no permission needed) | Human-gated (stop / recorded sign-off) |
|---|---|---|
| Local implementation | plan a bounded slice, write code and tests, run gates, review, record closeout, mechanical edits | — |
| Governing artifacts | advance approved roadmap outcomes, including a scope-preserving delivered/remaining wording split with evidence | **change Vision (`mission.md`) or Constraints (`constraints.md`)** — a load-bearing decision; add capability, reprioritize/order, add a phase, or introduce a strategic dependency |
| Boundaries | stay within declared scope and ownership | cross an ownership boundary; add a dependency absent from the constraints; deploy; use credentials/secrets/external approvals |
| Direction | select the next *local* slice from the roadmap | a *strategic* or ambiguous next step; a reprioritization |

The **load-bearing edge is enforced deterministically** (tenet 3): a change to the constitution (`constitution/mission.md` or `constitution/constraints.md`) must be accompanied by a recorded decision — a new ADR under `constitution/decisions/` — checked fail-closed by `framework/scripts/check_autonomy.py` (constraint `FUN-AUTONOMY-01`) in CI. The copilot cannot silently rewrite Vision or Constraints on autopilot; it stops and records *why* (tenet 8).

The other stop conditions (scope drift, ambiguity, generic boundary crossings) remain **judgment triggers** — documented above, not a deterministic gate. Claiming otherwise would be false precision (tenet 12: make deferred controls explicit). This is the standing answer to the copilot-vs-autopilot tension (critique C13): the boundary is explicit, and its most load-bearing edge is a check, not a promise.

## Agent Skills Rule

When a slice touches agent skills, skill packaging, skill routing, or `SKILL.md` files, the tower must reread the public Agent Skills guidance before planning or delegating the work:

- `https://agentskills.io/home`;
- the official specification if the work depends on exact format details;
- your repository's skill instructions, especially any file that scopes `**/skills/**/SKILL.md`.

The tower should preserve the Agent Skills architecture:

- skills package procedural knowledge and repeatable workflows;
- `SKILL.md` carries metadata and instructions;
- references, scripts, and assets are loaded only when needed through progressive disclosure;
- agent prompts define role, boundaries, and decision policy;
- deterministic artifact production belongs in tools/runtime, not hidden in conversational skill prose.

If a proposed skill change would make the skill act as a runtime host, compiler, or implementation engine, the tower must block or re-scope it.

## Primitives And Delegation

The kit is built from three distinct primitives; conflating them is the error behind critique C14. **Enforcement lives in the gates and the subagent tool boundaries, never in the skills.**

| Primitive | What it is | What it enforces |
|---|---|---|
| **Skill** | on-demand instructions loaded by `description` (progressive disclosure); guidance | nothing — it *guides* |
| **Gate** | a deterministic script (e.g. `framework/scripts/check_*.py`), run in CI or via the agent's bash | a *rule*, fail-closed |
| **Subagent** | a context-isolated agent instance with its own `tools`/`model`, agent-initiated, returning a summary | a *role* (tool boundary + unbiased fresh context) |

A role boundary is enforced by **config** (`tools`, `user-invocable`, `disable-model-invocation`, `agents`) wherever the tool granularity allows; where it cannot, the boundary is a **judgment** boundary, declared as such — never a prose claim the tools contradict (constraint `TEC-AGENTCFG-01`, checked by `framework/scripts/check_agents.py`).

**Interaction model.** The human dialogues with a single **tower** (the coordinator). The tower **delegates to subagents itself** when context isolation helps — the human does not switch agents manually (tenet 11); delegation is agent-initiated, not user-driven. Before final review, the coordinator stops or idles all other writers and names exactly one producer as branch owner; that producer commits and pushes protected work. One delegation is load-bearing, not a convenience: the **independent review must run in a context-isolated subagent** — a fresh, ex-novo context, not a fork of the producer's — so the verdict is not anchored by the context that produced the work. The no-edit reviewer returns its complete actual target/head observations, stability, verdict, evidence, and residual dispositions; only then does the Tower record the result. Subagents are the right tool when the output is a small summary/verdict (review); they are the wrong tool when the output is a large artifact that must return to the coordinator's context.

The single-writer freeze and target/head observations are operational audit boundaries, not
authentication or deterministic proof. They neither identify the reviewer nor prove that no outside
write occurred or that the semantic judgment was adequate. A post-review change to product, Change
Record plan/design/obligations/evidence, constraints, Roadmap, or changelog requires a newly committed target and fresh review by
reviewer/human judgment; no deterministic target-diff or protected-path gate is claimed.

## Agent Prompt And Instructions Rule

When a slice touches agent prompts, prompt files, repository instructions, or agent-customization files, the tower must reread the relevant agent-platform documentation before planning or delegating the work, and honor the repository's own prompt/instruction guidance (for example any file that scopes `**/*.prompt.md`).

This applies to paths and file types such as:

- `*.agent.md`;
- `*.prompt.md`;
- `*.instructions.md`;
- repository-level agent instructions and prompt directories.

The tower should preserve the customization boundary:

- agent prompts define role, operating stance, routing, autonomy, and decision policy;
- instruction files define durable workspace or file-scope guardrails;
- prompt files define reusable task entrypoints;
- skills define reusable procedures and workflows;
- deterministic behavior belongs in tools/runtime and tests, not hidden inside prompt prose.

If a prompt or instruction change would hide runtime behavior, bypass tests, or turn agent customization into an unreviewable implementation engine, the tower must block or re-scope it.

## Tower Artifacts

Tower-owned artifacts include:

- canonical dated Change Records and their explicitly triggered companions;
- mission documents;
- restart prompts;
- gap registers;
- architecture decisions;
- roadmap / readiness plans;
- returned review results recorded inside the Change Record;
- diagnostics;
- worker prompts;
- promotion/block decisions.

Specifier-owned or runtime-owned artifacts remain separate: agent prompts, skills, deterministic scripts, schemas, fixtures, tests, and produced contracts/handoffs.

## Common Rule

A tower succeeds when the next feature is clear, scoped, tested, reviewed, and aligned to Vision, Constraints, and Roadmap.

It fails when it drifts from the artifacts, takes command from the human, or degrades into an unaligned generic task runner.
