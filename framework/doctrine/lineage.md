# Lineage and positioning — Control Tower

Canonical source: `framework/doctrine/MANIFESTO.md` §10. The method stands on established practice and adds one distinctive move.

| Established practice | What the Control Tower inherits |
|---|---|
| **Spec-driven development** | The specification is the source of truth that flows to code. |
| **12-factor agents** | Own your prompts and control flow; keep deterministic orchestration out of prose. |
| **Evaluation-driven development** | Evals and golden sets as regression safety; no teaching-to-test. |
| **Context engineering** | Curate, compress, and isolate the durable context — here, the tower's own artifacts. |
| **AI governance** (NIST AI RMF, EU AI Act framing) | Auditability, traceability, human oversight, and documented decisions. |
| **DeepLearning.AI — Spec-Driven Development** (applied prior art) | The `mission.md` / `roadmap.md` / tech-stack constitution, the per-feature requirements/plan/validation spec, and the `feature-spec` / `changelog` skills — the concrete lineage of our templates and skills. |

**The distinctive move:** the Control Tower makes the governing artifacts — Vision,
Constraints, Roadmap — a **living, versioned product** that constrains every decision and
implementation, and keeps a **human-commanded copilot continuously aligned** to them
across the feature lifecycle, with a no-drift discipline. It is a spec/artifact-driven
SDLC copilot method with strong human command, not an autonomous self-improvement loop.
