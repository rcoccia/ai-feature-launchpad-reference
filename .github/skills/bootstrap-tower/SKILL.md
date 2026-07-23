---
name: bootstrap-tower
description: 'Bootstraps a Control Tower by creating the governing constitution — constitution/mission.md, constitution/constraints.md, constitution/roadmap.md — interview-first, with the main Tower producing a THIN strategy-level constitution before independent readiness. Use when starting a new tower or project with no constitution yet, running inception, or when the user says "bootstrap tower", "create the constitution", "start a new tower", "set up the specs", or invokes /bootstrap-tower. The core is domain-agnostic: it elicits stakeholder constraints, optionally gathers Authority facts, produces the constitution, and gates readiness.'
---

# Bootstrap Tower

Turn raw stakeholder intent into a governed constitution — Mission, Constraints, Roadmap — before the delivery loop starts, so inception is elicited (not invented) and shape-checked.

## When to Use This Skill

- Starting a **new** tower/project that has no `constitution/mission.md`, `constitution/constraints.md`, `constitution/roadmap.md` yet
- The user asks to "bootstrap", run "inception", or "set up the governing artifacts"
- You need the constitution that `plan-slice` will later read

Do **not** use it when: a constitution already exists (use `plan-slice` for the next slice); the work is a brownfield reverse-documentation pass (deferred, not this skill); you need the semantic inception-readiness verdict (a separate gate skill).

## Workflow

### 1. Gather raw input

Read whatever stakeholder material the repo already has (a `README`, a brief, notes). Note what is present and what is missing — do not fill gaps by invention.

If the human declares an external Authority binding, first invoke the relevant **installed** generic
interview skill to collect typed facts and evidence gaps: `classify-data`,
`assess-cloud-workload`, `assess-security-boundary`, or `request-policy-waiver`. Use only the
areas relevant to the declared binding. These skills advise and explain; they do not fetch or
install skills, create a `normative_spec`, select policy, approve a waiver, or claim compliance.
Route their facts to the Authority process before the constitution is produced.

### 2. Elicit BEFORE writing (interview-first)

Ask the user, grouped into exactly these three areas, and **wait** for answers:

| Area | Focus |
|------|-------|
| **Scope** | What the product does / serves; boundaries and non-goals |
| **Decisions** | Stack and key choices; the constraints that will gate work |
| **Context + constraints** | Tone/copy rules, patterns to follow, and which constraints are `hard` vs `soft` |

Do **not** write any file until the user has answered. This is the same anti-invention discipline as `plan-slice`.

### 3. Produce the THIN constitution

The **main Tower** writes the three files from confirmed human inputs, using this skill's assets
(`mission.md`, `constraints.md`, `roadmap.md`). Keep them strategy-level: a complete Mission (all
five sections), the six inherited Control Tower baseline constraints already present in the asset,
a few elicited product laws/boundaries/invariants (roughly 3–6 is usually enough to start), and a
roadmap whose **first current phase is small and bounded**. The inherited baseline does not count
toward the product guidance: it makes the installed Change Record, Roadmap, docs, merge,
conditional architecture-review, and strategy-autonomy kernel locally resolvable. Preserve those
exact IDs and complete blocks; do not aggregate or alias them into a product governance constraint. Author canonical
`## Phase` sections with a non-empty Goal and top-level capability checkboxes. All checked means
delivered; the first non-deferred phase with any unchecked item is current, including partial work;
later eligible phases are planned. `**Status:** deferred` is optional human-governed strategy, never
an inferred label. A fresh constitution must have current work; do not author
`**Lifecycle:** complete` during inception. The marker is reserved for a later human-authorized
final closeout when every non-deferred phase is delivered. This is guidance, not a deterministic
count gate.

Do **not** launch `requirements-agent` or `architect-agent` during THIN inception. Detailed feature
behavior belongs in roadmap capabilities and, after readiness, slice EARS. Technical design belongs
inside a selected delivery slice when it is load-bearing. If a design fact is missing, record an
open question or roadmap capability; do not silently choose an architecture.

When writing constraints, state a **verifiable property, not a mechanism** — freezing a specific
product/algorithm in a *hard* constraint is the **C16 self-confirmation trap** (the mechanism is a
design decision for `architecture-review`/ADR, not a constraint). See the template's *"Proprietà,
non meccanismo"* note. Also declare provenance with the template's inline-JSON fields: a non-empty
`source`; a pinned local `reference` for every non-stakeholder authority; and, for every hard
constraint, a tracked gate `projection` or a review-routed `residual`. The gate proves
structure/local reproducibility, not source authenticity or semantic adequacy. The inherited
baseline already pins copied local method surfaces; product constraints retain their own elicited or
Authority provenance.

### 4. Validate the shape (deterministic)

Scaffold missing files (idempotent, non-destructive) and then shape-check, from the repo root:

- Scaffold: `python .github/skills/bootstrap-tower/scripts/scaffold_constitution.py constitution`
- Check: `python .github/skills/bootstrap-tower/scripts/scaffold_constitution.py --check constitution`

Fix the constitution until `--check` exits 0. The **script is the enforcement**; this SKILL.md deliberately carries none of the checks (tenet 3).

### 5. Gate, then hand off

Before handoff, run the **inception-readiness** gate (skill `inception-readiness`, executed independently by the `reviewer-agent` — producer ≠ judge): it runs `--readiness` plus a semantic coherence checklist and returns PASS/BLOCK. The shape-check is **necessary, not sufficient**: a well-formed constitution can still be incoherent. On active PASS, hand off to `plan-slice`, which consumes the same canonical current-phase selector; on BLOCK, correct the flagged artifact upstream first. An all-delivered Roadmap without the lifecycle marker blocks for human re-cadence. A valid complete Roadmap passes readiness as no current work, but `plan-slice` remains blocked until a governed human reopen.

## Policy boundary

An external Authority can make applicable policy mandatory only through its explicit binding and
reconciliation path. Without an Authority, local stakeholder constraints are the mandatory policy
input. Optional installed domain advisors may help collect facts but are advisory extensions; they
do not silently add policy or claim compliance.

## Gotchas

- **Never** write mission/constraints/roadmap before the user answers the elicitation — preloading the solution is invention, not inception (tenet 4), and is prompt-cheating.
- **THIN is strategy, not a hidden slice:** do not launch Requirements or Architect here and do not
  convert feature flows, endpoints, status codes, or test cases into constraints. Those roles enter
  after readiness, in a selected delivery slice.
- **Do not silently design:** an unresolved technical choice is an open question or roadmap
  capability, not an architecture selected during inception.
- **Deterministic checks belong in the script, not this prose** (tenet 3): shape validation is `scaffold_constitution.py --check`. Do not restate or re-implement it conversationally.
- **Domain-agnostic** (TEC-DOMAIN-01): never hardcode a domain, workspace, or platform name in this skill or the script.
- **Authority absence is meaningful:** do not invent a baseline policy when no external Authority is
  declared; use the stakeholder constraints that were actually elicited. This does not remove the
  inherited Control Tower method baseline required by the installed kernel.
- **Shape-check is not the gate:** passing `--check` proves form, not coherence. Do not imply an all-clear; the readiness gate is separate.
- **Deferral is never automatic:** the script validates and skips explicit `deferred` status, but a
  human decides whether that status is intended, authorized, and still appropriate.
- **Complete is not a placeholder:** never add speculative work to avoid exhaustion. Valid completion
  records no currently approved work; reopening requires a governed human decision.

## References

- Templates: `.github/skills/bootstrap-tower/assets/mission.md`, `.github/skills/bootstrap-tower/assets/constraints.md`, `.github/skills/bootstrap-tower/assets/roadmap.md`
- Post-readiness slice roles: `.github/agents/requirements-agent.agent.md`, `.github/agents/architect-agent.agent.md`
- Optional Authority advisors: `classify-data`, `assess-cloud-workload`, `assess-security-boundary`,
  `request-policy-waiver`, and `authority-policy-reconciliation`
- Script: [`./scripts/scaffold_constitution.py`](./scripts/scaffold_constitution.py) (`--help` for usage)
- Method: `framework/doctrine/MANIFESTO.md`; loop in `framework/doctrine/operating-model.md`; critiques C1/C4/C14/C15 in `constitution/critique-and-mitigations.md`
- Prior art: DeepLearning.AI *Spec-Driven Development* ("Creating the Constitution", interview-first); BMAD analysis/planning + `generate-project-context`
