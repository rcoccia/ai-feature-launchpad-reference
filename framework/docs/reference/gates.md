# Reference — Gates

> The deterministic checks that make the method *enforceable* rather than aspirational. This
> catalog is the concrete answer to the method's own critique **C2** ("prose-as-governance is
> inapplicable"): every rule that *can* be a script *is* a script, run fail-closed.

## What a gate is

A **gate** is one of the [three primitives](../explanation/overview.md#the-three-primitives)
of the kit (Skill / Gate / Subagent). It is a small, standard-library Python script that:

- is **deterministic** — same inputs, same verdict;
- is **fail-closed** — any problem exits non-zero; silence is never a pass;
- **enforces one constraint** from
  [`constitution/constraints.md`](../../../constitution/constraints.md);
- carries the check **in code**, never in prose (tenet 3 / `FUN-DETERMINISM-01`).

Enforcement lives in the gates and in the subagent tool boundaries — **never** in the skills
(a skill only *guides*). See [`three primitives`](../explanation/overview.md#the-three-primitives).

## The catalog

Grouped by where they act in the loop. "CI" is the GitHub workflow under `.github/workflows/`
that runs the gate on every push/PR; a dash means the gate is run by the **reviewer subagent**
during a review skill, not as a standing CI job.

LIGHT installs standing workflows for docs/readiness, autonomy, provenance, and merge readiness,
plus the pre-checks embedded in its lifecycle Skills. Entries marked **Full** are
framework-development or historical example checks and are not copied/activated by LIGHT. Product
build, test, lint, scan, and deployment checks remain product-native in either profile.

### Constitution & inception

| Gate | Constraint | Enforces | When | CI |
|---|---|---|---|---|
| `bootstrap-tower/scripts/scaffold_constitution.py --check` | `FUN-ROADMAP-01` plus shape | mission/constraints/roadmap are well-formed and the Roadmap has one eligible current phase | inception | `docs.yml` |
| `scaffold_constitution.py --readiness` | portable kernel baseline plus inception readiness | exact inherited baseline IDs, shape, hard verification, Mission Success content, and canonical Roadmap selection | inception, pre-loop | `docs.yml` |
| `scaffold_constitution.py --current-phase` | `FUN-ROADMAP-01` | fully validates phase lifecycle and prints the exact current heading; malformed/exhausted blocks | planning | — (called by `plan-slice`) |

### The change loop

| Gate | Constraint | Enforces | When | CI |
|---|---|---|---|---|
| `framework/scripts/check_change_record.py` | `FUN-CHANGE-01` | exactly one valid dated Change Record governs the branch; companion and retired `specs/` namespace boundaries hold, including the one baseline exception | planning, implementation, pre-merge | `merge.yml` |
| `review-slice/scripts/review_slice.py` | — (review-slice) | the Change Record is reviewable: obligations have passing evidence, corrections/closeout are explicit, and triggered architecture is `SOUND` | pre-review | — (reviewer) |
| **Full:** `framework/scripts/check_regression.py` | `FUN-REGRESS-01` | historical example-instance regression check; Phase 16 rework targets consumer-declared verification | per slice | `regression.yml` |
| **Full:** `run-slice-evals` -> `framework/evals/run_evals.py` | `NFR-EVAL-01` | golden-set discrimination over the gates stays 1.00 (no teaching-to-test) | per slice | `evals.yml` |

### Design (before code)

| Gate | Constraint | Enforces | When | CI |
|---|---|---|---|---|
| `architecture-review/scripts/check_architecture.py` | `FUN-ARCHREVIEW-01` | a load-bearing design is *challenge-able* (design-under-test present; ADR weighed >=2 alternatives and named a negative consequence) before an independent challenge | pre-code | — (reviewer) |

### Integration (before merge)

| Gate | Constraint | Enforces | When | CI |
|---|---|---|---|---|
| **Full:** `framework/scripts/check_verification.py` | `FUN-VERIFY-01` | historical example-instance verification check; Phase 16 rework targets consumer-declared verification | pre-merge | `verify.yml` |
| `framework/scripts/check_autonomy.py` | `FUN-AUTONOMY-01` | any change to mission/constraints is accompanied by a recorded ADR | pre-merge | `autonomy.yml` |
| **Full:** `framework/scripts/check_agents.py` | `TEC-AGENTCFG-01` | no agent's description claims a boundary its tools contradict | pre-merge | `agents.yml` |
| `framework/scripts/check_merge_ready.py` | `FUN-MERGE-01` | the canonical record is reviewed and carries latest stable `PROMOTE`, complete evidence/closeout, and required residual dispositions | pre-merge | `merge.yml` |

### Cross-cutting

| Gate | Constraint | Enforces | When | CI |
|---|---|---|---|---|
| `framework/scripts/check_docs.py` | `NFR-DOCS-01` | every tracked `.md` is UTF-8 no-BOM, CRLF, balanced code fences | always | `docs.yml` |

## Constraints without a dedicated script

Some constraints are **design-level** and are honoured by construction / review rather than by
one gate: `TEC-DOMAIN-01` (domain-agnostic doctrine), `TEC-PRIMITIVES-01` (the three-primitive
separation), `FUN-NOINSTALL-01` (skills/agents are copy-in, no install step). They are listed
for completeness in
[`../../../constitution/constraints.md`](../../../constitution/constraints.md); making them
deterministic where possible is tracked in the
[critique register](../../../constitution/critique-and-mitigations.md) when that instance carries
one.

## Two gates are not standing CI — on purpose

`review_slice.py` and `check_architecture.py` are executed by the **reviewer subagent** inside
the `review-slice` and `architecture-review` skills, not by a permanent workflow. This is the
**producer != judge** discipline: the deterministic pre-check runs *inside* an independent,
context-isolated review, so the check and the judgment travel together. See
[`producer != judge`](../explanation/overview.md#producer--judge).

## Honest boundary

A green gate proves a **form**, not the full truth (tenet 12). `check_architecture.py` proves a
design is *challenge-able*, not *good*; `check_change_record.py` proves record/diff form and
monotonic lifecycle predicates, not obligation completeness; `check_merge_ready.py` proves a
PROMOTE was *recorded*,
with required residual dispositions, not that the review was *genuine*. Reviewed-target,
remote/ref, and start/completion head observations are prospective audit evidence: the existing
merge gate does not enforce their stability, authenticate the reviewer, prevent writes, or judge
semantic adequacy. The substance rests on the independent subagent review plus human command. The
gates raise the floor; they do not replace judgment. In particular, the Roadmap analyzer proves
status syntax and item-derived selection, not that deferral intent is authorized or strategically
sound.

## See also

- The primitives explained: [`../explanation/overview.md`](../explanation/overview.md)
- The constraints they enforce: [`../../../constitution/constraints.md`](../../../constitution/constraints.md)
- The decisions behind them: [`../../../constitution/decisions/`](../../../constitution/decisions/) (ADR log)
- The loop they punctuate: [`../../doctrine/operating-model.md`](../../doctrine/operating-model.md)
