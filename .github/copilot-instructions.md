# Control Tower — agent bootstrap

This repository is built with the **Control Tower** method: human-commanded, artifact-aligned,
gate-enforced. The method lives under `.github/` (skills, agents, instructions, workflows) and
`framework/` (gates in `scripts/`, plus `doctrine/`, `templates/`, `evals/`, `docs/`, `adoption/`).
This is the entry point a fresh agent reads automatically — **load the method before you act; it
points into the method, it does not restate it.**

## First: which state is this repository in?

Look for the constitution — `constitution/mission.md`, `constitution/constraints.md`,
`constitution/roadmap.md`.

- **Absent (greenfield).** You are *before* the loop. Your first move is **inception, not code**:
  run the `bootstrap-tower` skill — interview the human for scope, decisions, and constraints,
  produce the three governing artifacts, and gate them with `inception-readiness`. Do **not**
  invent the mission — elicit it (tenet 4). Nothing else starts until the constitution exists and
  passes the readiness gate.
- **Present.** You are *in* the loop. Read `framework/doctrine/operating-model.md` (the loop),
  `constitution/constraints.md` (the rules), `constitution/roadmap.md` (the next change), and the
  instance gap register when present. Run the canonical current-phase selector through `plan-slice`.
  A valid complete Roadmap has no current work: do not create a slice; wait for a human-authorized
  atomic reopen through `replan-and-correct`.

Background: `README.md`, `framework/doctrine/MANIFESTO.md`. Human-facing reading layer:
`framework/docs/` (start at `framework/docs/README.md`).

## Layout (five buckets)

- **`.github/`** — framework, harness-pinned: `skills/`, `agents/`, `instructions/`, `workflows/`.
- **`framework/`** — framework, portable: `scripts/` (gates), `doctrine/`, `contracts/`, `docs/`,
  and `adoption/`; Full also carries framework-development `evals/`.
- **`constitution/`** — strategy: mission, constraints, roadmap, `decisions/` (ADRs), gap register.
- **`changes/`** — canonical working memory and audit record: one dated Change Record per new
  governed change, with only explicitly triggered companions.
- **Legacy `specs/`** — retired from the active tree; recover immutable historical evidence through
  `changes/0000-control-tower-baseline.md`, never by recreating the namespace for new work.

## How to work here

- **The human commands; you propose.** Strategic decisions — and any change to
  `constitution/mission.md` or `constitution/constraints.md` — stop for the human and are recorded
  as an ADR under `constitution/decisions/` (enforced by `framework/scripts/check_autonomy.py`).
- **Work in bounded changes**, one roadmap phase at a time:
  `Sense -> Choose -> Plan (before code) -> Design -> Architecture-review (if load-bearing) ->
  Code -> Closeout -> Review -> Record`. A change with **no roadmap phase is a replanning trigger**, not a
  valid state. Accidental exhaustion requires re-cadence; explicit complete state blocks planning
  until human-authorized reopen (run `replan-and-correct`; see the Roadmap Re-cadence Rule).
- **Skills drive each step** (`.github/skills/`, loaded on demand by description): the LIGHT core is
  `bootstrap-tower`, `inception-readiness`, `plan-slice`, `architecture-review`, `review-slice`,
  `record-closeout`, and `replan-and-correct`. Full additionally provides `run-slice-evals` and
  optional Authority/GOVERNED Skills.
- **Gates enforce the rules** (`framework/scripts/check_*.py`; Full also has
  `framework/evals/run_evals.py`) — deterministic and fail-closed. Never weaken a gate to pass;
  correct the artifact **upstream** (tenet 8).
- **Independent review is mandatory before merge:** the reviewer runs in a fresh, context-isolated
  subagent with no `edit` tool (producer != judge). The Tower records the actual returned `PROMOTE`
  in the same Change Record (`framework/scripts/check_merge_ready.py`, `FUN-MERGE-01`).
- **Docs discipline** (`NFR-DOCS-01`): every tracked `.md` is UTF-8 no-BOM, CRLF, with balanced
  code fences (`framework/scripts/check_docs.py`).

## If this repository is the Control Tower method's own repo (it dogfoods itself)

Then you are **evolving the method**, not building a product with it: a change under
`.github/skills/`, `.github/agents/`, or `framework/` alters the **kit every adopter receives**,
not just this instance — treat it with that gravity. This is **orientation**, not a control: the
enforcement that such a change is independently reviewed before merge is already `FUN-MERGE-01`
(`framework/scripts/check_merge_ready.py`). For an adopter repo building its own product, this
section is inert.

## The one rule behind all the others

Nothing drifts silently from the three governing artifacts (Mission, Constraints, Roadmap). If
reality demands a change, change the **artifact first**, with a recorded reason — never patch the
code or the gate to hide the drift.
