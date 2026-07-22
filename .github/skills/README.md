# Control Tower — Skills

Skills are on-demand guidance under the canonical `.github/skills/` harness location. Deterministic
enforcement remains in scripts/Gates; semantic judgment remains in independent Subagents.

## LIGHT core — copied by default

| Skill | Loop stage | Deterministic surface |
|---|---|---|
| [`bootstrap-tower`](./bootstrap-tower/SKILL.md) | Inception | constitution scaffold/shape |
| [`inception-readiness`](./inception-readiness/SKILL.md) | Inception gate | readiness sub-check |
| [`plan-slice`](./plan-slice/SKILL.md) | Choose + judgment-led Plan | One dated Change Record + initial human confirmation |
| [`architecture-review`](./architecture-review/SKILL.md) | Conditional pre-code design review | architecture pre-check |
| [`review-slice`](./review-slice/SKILL.md) | Final review | Change Record reviewability pre-check |
| [`replan-and-correct`](./replan-and-correct/SKILL.md) | Correction | affected existing gates |
| [`record-closeout`](./record-closeout/SKILL.md) | Record | deterministic changelog |

LIGHT keeps the main Tower as producer, invokes Architect only for load-bearing design, and always
uses a fresh independent Reviewer before closeout. Planning reads governing and selectively
relevant evidence, raises only consequential concerns genuinely perceived, and keeps proposals
hypothetical until human confirmation.

## Full opt-in

The canonical method and `-Profile Full` also provide:

- `run-slice-evals` for framework-development golden regression;
- `classify-data`, `assess-cloud-workload`, and `assess-security-boundary` for typed Authority facts;
- `request-policy-waiver` and `authority-policy-reconciliation` for the optional governed policy
  route.

These Full-only directories are intentionally absent from a LIGHT copy. Install Full from the
canonical method checkout before invoking them.

## Adoption

`framework/adoption/scripts/bootstrap.ps1` copies LIGHT by default and Full explicitly. Skill
definitions remain canonical here; do not maintain divergent copies elsewhere in the method.
