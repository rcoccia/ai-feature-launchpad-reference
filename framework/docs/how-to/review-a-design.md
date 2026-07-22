# How-to — Review a design

> Challenge a **load-bearing design before code**, independently, so a design error is caught
> when it is cheapest to fix. Bad architecture is bad code: the mistake propagates and costs
> more downstream. This applies *producer != judge* to the design, not only the code.

## When to run it (and when not)

Run it when a change involves a **load-bearing** architectural decision. An NFR enters this path only
when satisfying, changing, or preserving it requires that load-bearing decision. Skip evidence-only
or preserved NFR work with no load-bearing choice — reviewing it here would be ceremony.

## The steps

### 1. The architect produces two artifacts

The `architect-agent` writes the usual ADR **and** a terse `design-under-test.md`: components,
data flow, the decision, the constraints touched — **without the justifications**. That terse
file, not the persuasive ADR, is what the challenger will see.

### 2. Deterministic pre-check — is it challenge-able?

```text
python .github/skills/architecture-review/scripts/check_architecture.py <DESIGN_DIR> --adr <ADR_PATH> --constraints constitution/constraints.md
```

Use this canonical form when `design-under-test.md` is the named sibling companion beneath the
Change Record's `changes/<record-stem>/` directory and the ADR is under
`constitution/decisions/`. The shorthand
`python .github/skills/architecture-review/scripts/check_architecture.py <DESIGN_DIR>` is
supported only when the ADR and constraints are colocated with the design directory.

It must exit 0: a `design-under-test.md` exists, the ADR weighed **>=2 alternatives**, and it named
at least one **negative/risk** consequence. If it fails, the design is not even
challenge-able (a single-option, all-upside ADR has nothing to attack) — send it back.

### 3. Challenge it — hostile, blindfolded, independent

[`architecture-review`](../reference/skills.md) hands the challenge to the `reviewer-agent` in a
fresh, context-isolated subagent. Two properties keep it genuinely adversarial:

- **Structural blindfold** — the challenger receives **only** the `design-under-test`,
  `constraints.md`, and the roadmap. **Never** the ADR's justification. It cannot inherit a
  conclusion it has not read.
- **Two lenses** — it judges under *both* "minimise for this slice" (YAGNI) *and* "walking
  skeleton for the known target" (build the real shape early to de-risk), kept separate. A
  challenger that only minimises rejects every forward-looking design — a bias as bad as the
  architect's.

### 4. Read the verdict — three ways

- **SOUND** — justified for the scope; proceed to code.
- **REWORK** — a **frame-independent defect** (a miscalibrated justification, a constraint
  violated or worsened, an internal contradiction). Wrong regardless of scope framing — fix the
  design first (tenet 8).
- **ESCALATE** — a genuine **scope-vs-architecture tension** (build the shape now vs defer). The
  gate does **not** decide this; it states both cases and routes the decision to **you**.

> ESCALATE is not a hiding place: any real defect is still REWORK, and an escalation must come
> with both the "build it now" and the "defer it" case written out.

### 5. Record

The Tower records the actual return in the canonical Change Record's Architecture review section.
There is no separate architecture review file. Only a stable `SOUND` permits code.

## The honest residual

An LLM challenging an LLM is **judgment, not proof** — and the challenger itself can be biased.
The blindfold, the two lenses, and ESCALATE govern that bias; they do not eliminate it. The last
line of defense is you: *who challenges the challenger?* The human. Measure the gate's usefulness
(real REWORKs / ESCALATEs) or retire it (tenet 12).

## See also

- The skill and its checklist: [`../reference/skills.md`](../reference/skills.md)
- The pre-check gate: [`../reference/gates.md`](../reference/gates.md) (`check_architecture.py`)
- The decision that introduced it: [`../reference/decisions.md`](../reference/decisions.md) (ADR-10)
