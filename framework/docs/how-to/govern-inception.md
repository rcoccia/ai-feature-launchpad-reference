# How-to — Govern inception

> Turn raw stakeholder intent into a governed **constitution** — Mission, Constraints, Roadmap
> — *before* the delivery loop starts, so inception is **elicited, not invented**. Do this once,
> at the start of a project (or when a new instance needs its own constitution).

## When

You have no `constitution/mission.md` / `constitution/constraints.md` / `constitution/roadmap.md` yet. If they exist
and you just need the next slice, go to [`run-a-slice.md`](run-a-slice.md) instead.

## The steps

### 1. Elicit before writing — `bootstrap-tower`

Run [`bootstrap-tower`](../reference/skills.md). It is **interview-first**: it asks you, grouped
into three areas, and waits for your answers *before* the **main Tower** writes any file:

- **Scope** — what the product does; boundaries and non-goals.
- **Decisions** — stack and key choices; the constraints that will gate work.
- **Context + constraints** — patterns to follow, and which constraints are `hard` vs `soft`.

> Do not let the copilot pre-fill the constitution from a brief. Preloading the solution is
> **invention**, not inception — the discipline the whole method exists to protect (tenet 4).

The output is **THIN strategy**, not a disguised delivery slice:

- **Constraints** are cross-slice laws, boundaries, and invariants. They are not a catalogue of
  endpoints, status codes, feature flows, or test cases.
- **Roadmap phases** are capabilities. Their detailed confirmed behavior becomes EARS only after
  readiness, in the selected slice.
- A missing technical design stays an open question or roadmap capability. The bootstrap does not
  decide it by launching the Architect Agent.

Requirements and Architect are **not** inception producers. They enter after readiness:
`plan-slice` invokes Requirements for a selected slice; Architect enters only inside a delivery
slice that needs a load-bearing design.

### 2. Declare the policy boundary

If an external Authority is declared, use the relevant installed generic advisor to collect typed
facts, then reconcile the Authority before producing the constitution. Without an Authority, the
elicited local stakeholder constraints are the mandatory policy input. Optional domain advisors are
advisory extensions, never an implicit mandatory baseline.

### 3. Shape-check (deterministic)

The skill scaffolds the three files from its own `assets/` (`.github/skills/bootstrap-tower/assets/`) and validates their **shape**:

```text
python .github/skills/bootstrap-tower/scripts/scaffold_constitution.py --check constitution
```

Fix until it exits 0. This proves *form* (all sections present, constraints well-formed, every
canonical phase has a Goal and top-level item, and a current phase exists) — not yet *coherence*.
All checked phases are delivered; a partial first eligible phase is current; explicit
`**Status:** deferred` is skipped but still validated. If no non-deferred unchecked phase remains,
the Roadmap is exhausted and the check blocks for re-cadence.

### 4. Gate for coherence — `inception-readiness`

Shape is necessary, not sufficient: a well-formed constitution can still be incoherent. Hand it
to [`inception-readiness`](../reference/skills.md), run **independently** by the `reviewer-agent`
(producer != judge). It runs the deterministic readiness check plus a semantic checklist:

- does each mission **Success** criterion map to a roadmap phase?
- is **Phase 1** one bounded, self-contained session?
- is anything both in scope and a non-goal?
- do the constraints cover the qualities the mission implies?
- is the constitution proportionate THIN strategy rather than feature requirements or unselected
  architecture?

Verdict: **PASS** or **BLOCK**. On BLOCK, correct the **upstream** artifact
(mission / constraints / roadmap) — never weaken the gate.

### 5. Hand off

On PASS, the constitution is ready. Go to [`run-a-slice.md`](run-a-slice.md); `plan-slice` consumes
the exact phase returned by `--current-phase`, not a second prose algorithm.

## The shape to remember

```text
Human interview -> Tower writes THIN constitution -> --check -> Reviewer readiness -> plan-slice
                                                                     -> Requirements -> Architect (only if load-bearing)
```

Elicit, don't invent. Prove form with the script, coherence with an independent review.

## Fresh THIN walkthrough

| Moment | What happens |
|---|---|
| **Human input** | Confirms Scope (purpose, users, non-goals), Decisions (durable boundaries and known constraints), and Context + constraints (hard/soft, patterns, Authority binding if any). |
| **Tower writes** | Creates Mission, a small set of cross-slice constraints with provenance, and a roadmap whose first capability is bounded. It records an unresolved technical choice as an open question or roadmap capability. |
| **Not yet** | No Requirements or Architect Agent, EARS, endpoint/status-code behavior, feature flow, test catalogue, or hidden technical design. |
| **Reviewer gates** | Runs deterministic readiness and judges coherence plus THIN proportionality. |
| **After PASS** | The canonical selector identifies current; `plan-slice` uses it and elicits detailed requirements; Architect is invoked only if that delivery's design is load-bearing. |

The script can prove explicit status syntax and item-derived state. It cannot decide whether
deferring a phase is authorized, wise, or still appropriate; that remains human strategy and
independent semantic review.

## See also

- The skills: [`../reference/skills.md`](../reference/skills.md)
- Running the first slice next: [`run-a-slice.md`](run-a-slice.md)
- If you must change the constitution later: [`course-correct.md`](course-correct.md)
