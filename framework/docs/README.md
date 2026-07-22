# Start Here: Control Tower

Control Tower is a **human-commanded method for governing AI-assisted software delivery**. It
keeps work aligned to three versioned artifacts--[Mission](reference/glossary.md#mission),
[Constraints](reference/glossary.md#constraints), and
[Roadmap](reference/glossary.md#roadmap)--and leaves an auditable record of why a change was made.

It is **not** a framework to import, an autonomous delivery engine, a universal build system, or a
replacement for product engineering judgment. The method governs the work; your product toolchain
still produces its own build, test, lint, scan, and deployment evidence.

## Is it a fit?

Use Control Tower when a system is long-lived, consequential, regulated, multi-team, or likely to
need a durable explanation of decisions. It is most useful when correctness, traceability, and
controlled autonomy matter more than raw generation speed.

Do not start with it for a throwaway prototype, a small solo experiment, or a task where the
governance overhead would exceed the risk. You can also begin
[LIGHT](reference/glossary.md#light): a bounded delivery without a load-bearing design does not
need an architecture-review ritual or automatic phase-agent handoffs. The main Tower remains the
single producer; the fresh no-edit Reviewer remains mandatory.

## The 10-minute mental model

1. **Set the slow law.** A greenfield project begins with a THIN constitution: Mission says why,
   Constraints says what must hold, and Roadmap says what capability comes next.
2. **Deliver one observable capability.** `plan-slice`, a
   [Skill](reference/glossary.md#skill), turns the next Roadmap outcome into one human-confirmed
   [Change Record](reference/glossary.md#change-record) before implementation starts.
3. **Use the right kind of control.** A [Gate](reference/glossary.md#gate) checks form; an
   independent [Agent](reference/glossary.md#agent) judges meaning. The human owns strategy,
   ambiguous scope, and merge.
4. **Record the result.** A promoted delivery records its
   [Roadmap Delta](reference/glossary.md#roadmap-delta)--delivered, remaining, discovered, and
   evidence--before it is merged.

Read the visual explanation before adopting the method:
[`explanation/overview.md`](explanation/overview.md).

## Choose your path

| You are... | Start with | Then |
|---|---|---|
| **New to Control Tower** | [Overview](explanation/overview.md) | [First delivery tutorial](tutorials/first-delivery.md) |
| **Adopting it in a product repository** | [First delivery tutorial](tutorials/first-delivery.md) | [Run a slice](how-to/run-a-slice.md), then [safe extensions](explanation/extending-safely.md) |
| **Maintaining the method (Full/source checkout)** | [Operating model](../doctrine/operating-model.md) | [Constraints contract](reference/constraints.md), [gates](reference/gates.md), and [decision records](reference/decisions.md) |

The copy-channel installer uses **LIGHT by default**: the executable lifecycle core, two agents,
four governance workflows, and their required docs/gates. `-Profile Full` explicitly adds optional
specialists, Authority/GOVERNED components, and framework-development material. Both profiles
preserve product-native CI rather than generating it.

## Reading map

| Need | Read |
|---|---|
| **Tutorial** -- learn by completing one first delivery | [First delivery](tutorials/first-delivery.md) |
| **How-to** -- perform a known task | [Govern inception](how-to/govern-inception.md), [run a slice](how-to/run-a-slice.md), [review a design](how-to/review-a-design.md), [course-correct](how-to/course-correct.md) |
| **Explanation** -- understand the boundaries and reasons | [Overview](explanation/overview.md), [extend safely](explanation/extending-safely.md) |
| **Reference** -- look up a concrete part | [Vocabulary](reference/glossary.md), [skills](reference/skills.md), [gates](reference/gates.md), [agents](reference/agents.md), [constraints](reference/constraints.md), [decisions](reference/decisions.md) |
| **Case studies** -- assess a real adoption | Not yet a maintained docs surface; use the roadmap and gap register, not removed in-repo examples, as the honest status record. |

## What stays elsewhere

- **Normative doctrine:** [`../doctrine/`](../doctrine/) is the authoritative statement of the
  principles and operating loop.
- **Your project's strategy:** `constitution/` is the Mission, Constraints, Roadmap, decisions,
  and gap register for that project. The canonical Mission artifact is
  `constitution/mission.md`; *Vision* is an older name for the concept, not another required file.
- **Your delivery tactics:** `changes/` holds dated
  [Change Records](reference/glossary.md#change-record); the retired legacy tree is recoverable from
  [`../../changes/0000-control-tower-baseline.md`](../../changes/0000-control-tower-baseline.md).
- **Installation and distribution:** [`../adoption/`](../adoption/) documents the current
  LIGHT-default / Full-opt-in copy channel. Plugin packaging, version negotiation, drift detection,
  generated reference, case-study, FAQ/troubleshooting, and automated accessibility/link validation
  are not current guarantees.

Every file here is Markdown governed by `NFR-DOCS-01`: UTF-8 without BOM, CRLF line endings, and
balanced code fences, checked by `framework/scripts/check_docs.py`.
