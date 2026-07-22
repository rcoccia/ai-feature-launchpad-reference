# Extending Control Tower safely

Control Tower has a deliberately small core: the constitution, feature-first Change Records,
deterministic gates where a property is checkable, independent review, and human command. Extend
it when evidence from more than one use shows a stable need--not because a topic sounds useful.

## Choose the right extension type

| Need | Extension type | Boundary |
|---|---|---|
| Reusable advice or a guided workflow | Generic advisory **Skill** | Guides work; it does not enforce policy or download more skills at runtime. |
| A repeatable, objective check | Deterministic **gate/tool** | Owns one input/output contract and fails closed; do not encode it only in prose. |
| A bounded independent responsibility | Custom **Agent role** | Its configuration and tools must match its claimed authority; judgment is not a fake gate. |
| An organization-owned rule set | External **Authority** policy/catalog | Requires explicit binding, version, owner, facts, and reconciliation; it is not silently mandatory. |
| Build, test, lint, scan, or deployment proof | Product-native **CI adapter/evidence** | The product toolchain produces evidence; the Tower maps and reviews it. |
| A future integration surface | Optional **MCP facade** | Keep it optional until a concrete second consumer proves the shared contract. |

## Core versus extension

Keep in core only what every adoption needs to preserve the method's governance boundary. Put
domain semantics, product build systems, organization policy catalogs, and integration-specific
adapters in extensions. An extension needs a named owner, a version or compatibility statement,
and inspectable evidence for its behavior.

Apply the **second-consumer rule**: prefer an instance-local solution for the first real use. Move
it into the reusable kit only after a second independent consumer demonstrates the same stable
contract. This resists turning one project’s vocabulary into the method’s hidden doctrine.

Semantic or vector search can help a person discover possible material, but it is advisory only.
It cannot decide policy applicability, select mandatory policy, or become a required precondition
for a normal delivery.

## Avoid these anti-patterns

- A runtime skill downloader that changes what an adoption does without a reviewed, versioned kit.
- One skill per topic instead of a small number of coherent, reusable workflows.
- A language-specific build system in core instead of product-native validation evidence.
- Hidden mandatory domain policy with no explicit Authority binding and reconciliation.
- A new “gate” for prose quality, architecture merit, or other semantic judgment a script cannot
  honestly decide.
- An extension with no accountable owner, version, compatibility story, or evidence.

## Decision tree

```text
Is the need reusable across two independent consumers?
  No  -> keep it local, document the evidence, or do nothing.
  Yes -> Is the outcome deterministic and objectively checkable?
            Yes -> add a gate/tool with a small contract.
            No  -> Is it guidance for a repeated workflow?
                      Yes -> add a Skill.
                      No  -> Is it a bounded independent responsibility?
                                Yes -> add an Agent role.
                                No  -> Is it organization-owned policy?
                                          Yes -> bind and reconcile an Authority catalog.
                                          No  -> keep it in product tooling or do nothing.
```

Product build, test, lint, scan, and deploy integration belongs in product tooling when it produces
product evidence. Do not promote it to the core merely because the Tower consumes that evidence.
An MCP facade is a possible future delivery mechanism, not a prerequisite for skills, gates, or
Authority reconciliation.

## Keep the human in command

Extensions must not turn advice into invisible policy, or automation into unreviewed strategy.
When an extension changes Mission, Constraints, roadmap priority, ownership, or an unresolved
architecture trade-off, stop for a human decision and record it. Use the
[overview](overview.md) to keep the deterministic, semantic, and human boundaries clear.
