# Intent-to-merge evidence chain

AI Feature Launchpad is a didactic reference: each implementation claim traces to a governing
artifact and executable evidence. The chain is not a production certification.

## Reference mapping

| Link | Public artifact | What it proves |
|---|---|---|
| Purpose | `constitution/mission.md` | One synthetic-enterprise launch-approval capability, its users, success, and non-goals. |
| Delivery selector | `constitution/roadmap.md` | Phase 1 delivered the feature; Phase 2 remains open until a fresh replay succeeds. |
| Cross-slice laws | `constitution/constraints.md` | Six inherited Control Tower laws plus four product laws bind planning, design, code, evidence, and review. |
| Human authority | `constitution/decisions/ADR-20260723-01-authorize-launchpad-inception.md` | Attests the confirmed inception decision without claiming identity authentication. |
| Governed slice | `changes/2026-07-23-govern-ai-feature-launch.md` | Connects Phase 1 to scope, ten obligations, plan, append-only evidence, corrections, closeout, and actual reviews. |
| Load-bearing design | `changes/2026-07-23-govern-ai-feature-launch/design-under-test.md` | Fixes API, SQLite, transaction, concurrency, refusal-audit, and trusted-header semantics before code. |
| Architecture challenge | Phase 1 Change Record, `Architecture review` | Independent stable `SOUND` at design target `ed91419236a01fafffa21760ed446b024b81f7b7`. |
| Implementation | `src/Launchpad.Api/` | .NET 10 Minimal API and direct file-backed SQLite implementation. |
| Executable proof | `tests/Launchpad.Api.IntegrationTests/` | 28 integration cases over behavior, persistence, audit, concurrency, and identity warnings. |
| Product CI | `.github/workflows/product-ci.yml` | Locked restore, Release build, and tests in product-owned CI. |
| Product contract | `README.md`, `docs/api.md`, `docs/trust-boundary.md` | Run instructions, exact nested request/audit JSON with decision/event timestamps, and explicit non-production identity boundary. |
| Final judgment | Phase 1 Change Record, `Independent final review` | Append-only BLOCK corrections followed by actual stable `PROMOTE`. |
| Merge proof | PR 3 and merge commit `0a700178269acdf284c14c9033577857357c3dd3` | Human-controlled GitHub merge of the reviewed reference feature. |

The merged run's product CI evidence includes successful correction run `29985547135` on
`94e705f764315998be0b3e237e937597e5dcd1ef`. The final reviewed feature record was then merged through
PR 3. These references prove the public reference; a replay must still generate its own local build,
test, gate, architecture, and review-ready evidence.

## Constraint-to-proof map

| Constraint | Primary proof |
|---|---|
| `FUN-CHANGE-01` | One confirmed dated Phase 1 record and Change Record gate. |
| `FUN-ROADMAP-01` | Readiness/current-phase selector and scope-preserving Roadmap closeout. |
| `NFR-DOCS-01` | Documentation gate plus public, layered review. |
| `FUN-MERGE-01` | Frozen no-edit final review, recorded actual verdict, merge-ready gate, human merge. |
| `FUN-ARCHREVIEW-01` | Named trigger, design companion, form gate, stable `SOUND` before code. |
| `FUN-AUTONOMY-01` | Inception ADR and autonomy gate. |
| `TEC-STK-01` | `net10.0` projects, direct SQLite package/store, locked build and tests. |
| `TEC-IDB-01` | Development/Testing startup guard, every-response warning, tests, and boundary doc. |
| `FUN-APR-01` | Atomic state/audit implementation and semantic integration cases. |
| `NFR-CI-01` | Product-owned workflow and successful build-and-test run. |

## Non-production identity boundary

`X-Reference-Actor-Id` and `X-Reference-Actor-Role` are caller-supplied assertions from a hypothetical
trusted upstream. They are intentionally spoofable and are not authentication. The host is restricted
to `Development` and `Testing`, logs a warning, and adds
`X-Reference-Authentication-Warning` to every response. The reference contains no OAuth, JWT, cookie,
API key, actor directory, forwarded-header trust inference, or identity provider.

This boundary demonstrates actor-aware governance only. It proves neither confidentiality nor
production authorization. A production system would require authenticated transport and upstream
identity, issuer/audience validation, credential lifecycle, authorization policy, data protection,
monitoring, deployment controls, and threat analysis.

## Replay interpretation

The public reference proves one complete intent-to-merge chain. Phase 2 asks a different question:
are the public docs sufficient for an uninvolved agent to reconstruct the same governed feature from
zero and reach review-ready?

The disposable reconstruction mirrors the reference's two-phase Roadmap. Its sole local delivery
record remains historically anchored to Phase 1. Once Phase 1 is truthfully checked at closeout,
readiness stays green and the selector advances to the planned, unchecked Phase 2 instead of reporting
Roadmap exhaustion.

A successful replay adds external reproducibility evidence; it does not require a second local
Change Record, implement or close local Phase 2, or add a second product capability, production
assurance, cloud repository, final reviewer verdict, or merge. Until that measured replay passes and
is recorded by the parent reference, the Phase 2 Roadmap item remains unchecked.
