---
name: inception-readiness
description: 'Gates a Control Tower constitution before the delivery loop: runs the deterministic readiness sub-checks (scaffold_constitution.py --readiness) and then a semantic coherence checklist — traceability, first-phase boundedness, scope/non-goals, constraint coverage, and THIN strategy-vs-tactics proportionality — returning a PASS/BLOCK verdict. Run it independently (via the reviewer-agent, producer != judge) after bootstrap-tower and before plan-slice, or when the user says "inception readiness", "is the constitution ready", "readiness gate", "check the constitution", or invokes /inception-readiness.'
---

# Inception Readiness

Judge whether a freshly created constitution is **coherent and ready to start the loop** — not merely well-formed — and return a PASS/BLOCK verdict.

## When to Use This Skill

- After `bootstrap-tower` has produced `constitution/mission.md`, `constitution/constraints.md`, `constitution/roadmap.md`, and before `plan-slice`
- The user asks "is the constitution ready?", "run the readiness gate", or the constitution changed materially and coherence must be re-confirmed

Do **not** use it for: reviewing a completed feature slice (that is the `review-slice` skill); the deterministic shape-check alone (`--check`); or producing the constitution (`bootstrap-tower`).

## Workflow

### 1. Run the deterministic gate

From the repo root:

`python .github/skills/bootstrap-tower/scripts/scaffold_constitution.py --readiness constitution`

It must exit 0 — shape is valid **and** the constitution contains the exact inherited baseline IDs
`FUN-CHANGE-01`, `FUN-ROADMAP-01`, `NFR-DOCS-01`, `FUN-MERGE-01`, and
`FUN-ARCHREVIEW-01`; every hard constraint carries a `verification`; every canonical Roadmap phase
(including deferred history) has a non-empty Goal and valid top-level item; the first non-deferred
phase with an unchecked item is selectable; and the mission Success section is non-empty. Delivered
phases are skipped; a partial phase remains current; an exhausted Roadmap blocks for re-cadence. If
it fails, **BLOCK**: name the artifact to fix; do not judge coherence on a malformed constitution.

### 2. Apply the semantic checklist (judgment)

With the deterministic gate green, judge coherence:

| Check | Ask |
|-------|-----|
| Traceability | does each mission Success criterion map to at least one roadmap phase? |
| First phase bounded | is Phase 1 one focused session, with no dependency on a later phase? |
| Scope vs non-goals | is anything both in scope and a non-goal? |
| Product constraint coverage | beyond the inherited method baseline, do elicited constraints cover the stack/qualities the mission implies (no glaring gap)? |
| No orphan phase | does every roadmap phase advance the mission? |
| Deferral intent | is every explicit `**Status:** deferred` human-authorized and still appropriate? |
| THIN proportionality | are constraints cross-slice laws/boundaries/invariants and roadmap phases capabilities, with detailed behavior deferred to slice EARS? Block a feature catalogue, endpoint/test flow, or unselected architecture embedded in strategy. |

### 3. Verdict

Return **PASS** or **BLOCK**:

- **PASS** — the constitution is coherent and ready; hand off to `plan-slice`.
- **BLOCK** — list the specific failures, propose gap-register entries, and name the **upstream** artifact (mission / constraints / roadmap) to change first (tenet 8). Never fix the gate or weaken a check.

## Who runs it

Run **independently** of whoever produced the constitution. The `reviewer-agent` (no `edit`) is the intended executor, so the producer is not the judge (tenets 5 and 7; critiques C5/C9).

## Gotchas

- **Form is not coherence:** a green `--readiness` proves structure, not sense. The semantic checklist is the actual gate — do not stop at the script.
- **Deterministic checks live in the script** (tenet 3): do not restate or re-implement `--readiness` logic in this prose.
- **Correct upstream** (tenet 8): on BLOCK, change mission/constraints/roadmap — never the gate or the check.
- **Producer ≠ judge:** do not run this on a constitution you just authored yourself in the same breath; hand it to an independent reviewer.
- **No teaching-to-test:** never weaken a check to force a PASS.
- **No numeric proxy for judgment:** THIN proportionality is semantic review, not a maximum
  constraint count or constitution-length gate. The five inherited method constraints are kernel
  obligations, not product-scope inflation.
- **Status syntax is not intent:** the deterministic gate can validate `deferred`; only human
  strategy and independent judgment can establish whether deferral is wise or current.
- **Domain-agnostic** (TEC-DOMAIN-01): no hardcoded domain names.

## References

- Deterministic gate: [`../bootstrap-tower/scripts/scaffold_constitution.py`](../bootstrap-tower/scripts/scaffold_constitution.py) (`--readiness`)
- Executor: `.github/agents/reviewer-agent.agent.md`
- Upstream artifacts: `.github/skills/bootstrap-tower/assets/mission.md`, `.github/skills/bootstrap-tower/assets/constraints.md`, `.github/skills/bootstrap-tower/assets/roadmap.md`
- Method: `framework/doctrine/MANIFESTO.md`; loop in `framework/doctrine/operating-model.md`; critiques C15/C5 in `constitution/critique-and-mitigations.md`
- Prior art: BMAD `check-implementation-readiness` (READY / NEEDS WORK / NOT READY)
