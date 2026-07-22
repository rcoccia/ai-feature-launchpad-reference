---
name: replan-and-correct
description: 'Routes a mid-loop discovery to the nearest authoritative correction radius: implementation, slice, or governance/strategy. Updates only affected artifacts and stale evidence for local corrections; runs the full human-gated replan for wider changes. Use when a gap appears during coding, a hard constraint is violated, drift/scope/evals diverge, the plan changes, or the user says course correct, replan, adjust the roadmap, or invokes /replan-and-correct.'
---

# Replan and Correct

Turn a mid-loop discovery into the **smallest governed upstream correction that can absorb it** —
never silent drift, never a patched gate, and never constitution-scale ceremony for a local fact.

## When to Use This Skill

- A hard constraint can no longer be honoured, or is violated
- Drift, scope creep, or an eval regression appears
- Any potentially material fact or semantic gap is discovered while coding (the spec←code arc)
- The roadmap sequence no longer holds
- **The roadmap is exhausted** — all phases are complete but work continues (a slice would have "no phase"); re-derive the next wave from the gap register (see the *Roadmap Re-cadence Rule* in `framework/doctrine/operating-model.md`)

Do **not** use it for routine next-slice planning (`plan-slice`), a failing test whose fix changes no
confirmed semantics or boundary, or gating a fresh constitution (`inception-readiness`).

## Workflow

### 1. Choose the Correction Radius

Select exactly one radius before applying a correction:

| Radius | Required boundary | Action |
|---|---|---|
| `implementation` | confirmed behavior, outcome, Roadmap, active constraint set, Authority/policy applicability, dependencies, and load-bearing design are unchanged | continue normal implementation and product evidence; do not replan |
| `slice` | change semantics change, but outcome, Roadmap, active constraint set, Authority/policy applicability, and dependencies remain unchanged | correct affected Change Record sections/triggered design and stale evidence |
| `governance/strategy` | outcome, any wider artifact, binding, applicability, dependency, Mission, or Constraints may change | continue with the full workflow below |

This is a semantic decision, not a deterministic classifier. If uncertain, choose the wider radius
and stop for the human.

For `implementation`, keep the rationale in normal implementation evidence or the final review; do
not edit confirmed plan/obligation semantics merely to prove that no semantic correction occurred.

For `slice`:

1. Update the affected Change Record scope/decisions/plan/evidence expectations and triggered design
   when relevant before continuing affected code.
2. Preserve the observable outcome, Roadmap, active constraint set, Authority/policy applicability,
   and dependencies. If any may change, use `governance/strategy`.
3. Append the correction and mark affected evidence/review attempts stale; never rewrite history.
4. Rerun `review_slice.py` on the Change Record before affected code continues, rerun affected product evidence after
   implementation, and obtain a fresh independent final review before merge. Do not rerun unrelated
   evidence.
5. Record the rationale in the nearest existing requirement source, Decisions/Context, design, or
   final review surface. Add no adjustment log.

A slice correction alone requires neither constitution readiness nor a course-correction ADR. If a
load-bearing decision changes, update the normal architecture ADR and rerun architecture-review
before affected code.

Only `governance/strategy` continues with steps 2-7.

### 2. Classify the trigger

Name the trigger from the taxonomy in `framework/doctrine/artifacts-skills-lifecycle.md` §6.1 (drift, hard-constraint violated, gap-structure changed, eval regression, scope creep, architect decision, new common consumer, gap-in-coding). A **violated hard constraint is a falsifiable trigger** — prefer it over a vague "it feels off".

### 3. Impact scan

List which governing artifacts are affected, in order of impact: Mission → Constraints → Roadmap →
Gap Register → Change Record. Note the downstream changes/tests that ripple.

### 4. Choose a path forward

Score the options (adapted from BMAD `bmad-correct-course`):

| Path | When |
|------|------|
| Direct adjustment | modify/add within the current roadmap/slice structure |
| Rollback | revert a recently completed slice the change invalidates |
| Scope reduction | reduce/redefine scope (mission/roadmap) when the target is no longer viable |

Correct **upstream**, never the gate (tenet 8).

### 5. Route by severity

- **minor** → confirm whether the `slice` radius is sufficient; otherwise widen.
- **moderate** → update the roadmap + gap register.
- **major** → **stop and get the human's decision** for any human-gated boundary in the Autonomy
  Envelope, including Mission/Constraints changes, new capability/priority/phase, strategic or
  previously absent dependencies, ownership boundaries, deployment, credentials, or external
  approval. Do not rewrite strategy autonomously.

### 6. Apply and re-validate

Edit the upstream artifact(s) and invalidate every downstream requirement, design, review, or
evidence item that the change made stale. Rerun readiness only when Mission, Constraints, or
Roadmap changed:

`python .github/skills/bootstrap-tower/scripts/scaffold_constitution.py --readiness constitution`

A correction that breaks constitution shape or coherence is not done. The gate proves only that
checkpoint, not the semantic correctness of the new direction.

### 7. Record

Record the reason in the artifacts that changed plus review/closeout and restart when present.
Append an ADR when Mission or Constraints change, a load-bearing architectural decision changes, or
a new strategic direction requires a durable human decision. Roadmap/Gap loop mechanics do not
require a course-correction ADR merely because this Skill was invoked.

## Gotchas

- **Local is not a waiver:** a `slice` correction cannot change outcome, Roadmap, active constraints,
  policy applicability, or dependencies. Widen immediately when one may change.
- **A prior review can become stale:** a recorded `PROMOTE` never approves semantics or code added
  after that verdict; obtain a fresh independent review.
- **Policy changes are wider:** a changed Authority binding or applicability result always uses
  `governance/strategy`; do not invent replacement semantics or claim compliance.
- **Correct upstream, never the gate** (tenet 8): change the nearest authoritative artifact; never
  weaken a check or test to absorb drift.
- **Mission or Constraints = human decision** (tenet 1): this Skill never rewrites them autonomously.
- **A violated hard constraint is falsifiable** (C7): prefer constraint-anchored triggers over intuition; "gap discovered in coding" is an explicit trigger (the spec←code arc, C1), not silent invention.
- **Reference, don't duplicate** (C11): the trigger taxonomy lives in design §6.1 — point to it, do not copy it into this skill.
- **Domain-agnostic** (TEC-DOMAIN-01): no hardcoded domain names.

## References

- Triggers & procedure: `framework/doctrine/artifacts-skills-lifecycle.md` §6.1 (triggers), §6.2 (procedure)
- Slice pre-check: `../review-slice/scripts/review_slice.py`
- Constitution re-validation: `.github/skills/inception-readiness/SKILL.md`;
  `../bootstrap-tower/scripts/scaffold_constitution.py` (`--readiness`)
- Decision Log: `constitution/decisions/README.md`
- Method: `framework/doctrine/MANIFESTO.md` (tenets 1, 2, 8, 11); loop in `framework/doctrine/operating-model.md`; critiques C15/C7/C1 in `constitution/critique-and-mitigations.md`
- Prior art: BMAD `bmad-correct-course` (change-navigation checklist, Sprint Change Proposal, routing by scope)
