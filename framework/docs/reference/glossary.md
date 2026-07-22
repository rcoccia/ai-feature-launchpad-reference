# Reference - Control Tower vocabulary

Use this page when a Control Tower term appears in the adopter journey. These definitions explain
the method without replacing the normative
[Manifesto](../../doctrine/MANIFESTO.md) or
[Operating Model](../../doctrine/operating-model.md).

## Mission

The durable statement of why the system exists, who it serves, its scope, and its non-goals. Its
canonical artifact is `constitution/mission.md`. Earlier material sometimes called this concept
*Vision*; that is a historical name, not a separate governing artifact.

## Constraints

The technical, functional, and non-functional conditions that every slice must honor. Constraints
record their source and verification route so planning and review do not invent what must hold.
They live in `constitution/constraints.md`.

## Roadmap

The ordered capability outcomes the Tower may select next. A Roadmap describes observable progress,
not a checklist of implementation tasks. Canonical sections begin `## Phase`: all valid items
checked is **delivered**; the first non-deferred phase with any unchecked item is **current**,
including partial work; later eligible phases are **planned**. Optional `**Status:** deferred`
keeps a human-postponed phase inspectable but excludes it from selection. With no eligible unchecked
phase, the Roadmap is **exhausted** and must be re-cadenced. It lives in
`constitution/roadmap.md`.

## Change Record

The canonical working memory and audit record for one governed change. A dated Markdown file under
`changes/` evolves from outcome, Roadmap anchor, proof obligations, and short plan through evidence,
corrections, closeout, and the actual returned independent verdict.

## EARS

The Easy Approach to Requirements Syntax: a legacy technique used by historical Slice Plans. New
Change Records express observable outcomes and proof obligations without requiring EARS.

<a id="evidence-stances"></a>

## Proof obligations

An activated, constraint-anchored claim that the change must prove. Each obligation records why it
applies, what evidence is expected, and the actual result. The baseline is universal; explicit
triggers add obligations. Human confirmation and independent review govern semantic completeness.

## Gate

A deterministic, fail-closed script or check that verifies one stated condition. A green Gate proves
that bounded condition, not semantic completeness, correctness, or production readiness.

## Skill

On-demand workflow guidance loaded by description. A Skill can tell the Tower which Gate to run or
which Agent to delegate to, but the Skill itself does not enforce behavior.

## Agent

A context-isolated role instance with its own model and tools. Tool configuration enforces a role
boundary where possible; semantic responsibilities remain reviewer judgments where the tools cannot
express the boundary.

## LIGHT

Proportional treatment for a bounded delivery with no Authority/policy delta, new dependency, active
constraint-set change, or load-bearing design. The main Tower remains the single producer across
elicitation, Change Record, implementation, and closeout; Requirements/Planner are optional and
Architect is conditional. The fresh no-edit Reviewer remains mandatory. LIGHT is not a waiver and
not a third slice type alongside delivery and spike.

## Roadmap Delta

The closeout reconciliation of what the slice delivered, what approved scope remains, what it
discovered, and which evidence supports the result. New capability or priority is proposed to the
human rather than silently added during closeout.

## Correction radius

The semantic choice of the nearest authoritative artifact that can absorb a fact discovered during
coding without drift:

- `implementation` keeps normal code/test evidence when confirmed behavior and every governing or
  design boundary remain unchanged;
- `slice` corrects affected Change Record sections or triggered design while preserving outcome,
  Roadmap, active constraints, policy applicability, and dependencies;
- `governance/strategy` runs the full governed replan when the outcome or any wider boundary may
  change.

If the radius is uncertain, choose the wider path and stop for the human. Radius selection is
reviewer/human judgment, not a deterministic classifier. See
[Course-correct](../how-to/course-correct.md).

## Related reference

- [Skills](skills.md)
- [Gates](gates.md)
- [Agents](agents.md)
