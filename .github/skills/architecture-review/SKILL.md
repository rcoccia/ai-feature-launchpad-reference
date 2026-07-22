---
name: architecture-review
description: 'Independently challenges one triggered load-bearing decision linked from a Change Record before code, returning SOUND/REWORK/ESCALATE. Use for architecture review, design challenge, or /architecture-review.'
---

# Architecture Review

Challenge one expensive-to-reverse decision before implementation.

## Workflow

1. A named load-bearing trigger permits exactly one sibling companion:
   `changes/<dated-record-stem>/design-under-test.md`. The Change Record remains canonical and links
   the companion, trigger, governing ADR, and affected constraints.
2. Run:

   `python -B .github/skills/architecture-review/scripts/check_architecture.py
   changes/<dated-record-stem> --adr <ADR_PATH> --constraints constitution/constraints.md`

   A failure is `REWORK (form)`.
3. Give a fresh no-edit challenger only the companion, Constraints, and Roadmap. Never provide the
   ADR justification.
4. Apply both lenses:
   - minimise-for-change: every element is needed by the bounded outcome;
   - walking-skeleton-for-target: the design establishes the real known target shape.
5. Attack constraint coherence, calibration, reversibility, coupling/blast radius, and internal
   contradiction. Return `SOUND`, `REWORK`, or `ESCALATE`; do not hide a defect as scope tension.
6. The Tower records the actual reviewer/date, frozen target/ref and heads, stability, pre-check,
   lenses, evidence, findings, and returned verdict in `## Architecture review` of the Change Record.
   No `architecture-review.md` exists. Only an actual stable `SOUND` permits code.

## Gotchas

- **NFR presence is not a trigger:** architecture review applies only when satisfying, changing, or
  preserving it requires a load-bearing decision.
- **Blindfold the challenger:** justification belongs to the producing ADR, not the review input.
- **Record after return:** never prewrite `SOUND`.
- **Form is not merit:** the deterministic pre-check proves challengeability only.
- **No legacy adapter:** the companion is linked from `changes/`; never recreate the retired
  `specs/` namespace.

## References

- Pre-check: `./scripts/check_architecture.py`
- Producer/executor: `.github/agents/architect-agent.agent.md`,
  `.github/agents/reviewer-agent.agent.md`
