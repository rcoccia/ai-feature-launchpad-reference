# Tutorial: Your first governed delivery

> **Legacy teaching page.** Phase 30 replaced and retired the `specs/` triplet below in favor of one
> dated Change Record. Do not execute the legacy commands on this page for a new change; use
> [Run a governed change](../how-to/run-a-slice.md). Recover historical artifacts through the
> [baseline index](../../../changes/0000-control-tower-baseline.md). A full didactic rewrite is
> deferred to Phase 31.

This tutorial follows one compact, synthetic product capability from an empty repository to a
merge-ready pull request. It teaches the method; it does not create a consumer application for
you. Replace angle-bracket values with your own paths and product facts.

## What you will complete

By the end, your repository has a THIN constitution, one feature-first
[EARS](../reference/glossary.md#ears) [Slice Plan](../reference/glossary.md#slice-plan), product
toolchain evidence, an independent review, and a
[Roadmap Delta](../reference/glossary.md#roadmap-delta). The example capability is:

> A stockroom service can register a product and later retrieve it by SKU.

It is illustrative. Do not copy its behavior into your product without eliciting your own
requirements.

## 1. Create a fresh repository and copy the kit

The copy-channel bootstrap installs the LIGHT core by default and deliberately does **not** create
a constitution. In PowerShell:

```powershell
git init C:\work\stockroom-service
& 'C:\path\to\control-tower\framework\adoption\scripts\bootstrap.ps1' -Target 'C:\work\stockroom-service'
```

`C:\path\to\control-tower` is an illustrative source location. The script path and `-Target`
parameter are current; choose a real canonical Git checkout of the method. Add `-Profile Full`
only when you need Full-only specialist agents, Authority/GOVERNED extensions, or
framework-development material. Neither profile creates product-native CI or configures branch
protection; existing product workflows are preserved.

Open the target repository in an agent editor. Its entry point sees that `constitution/` is absent
and starts inception rather than coding.

## 2. Run interview-first inception

Invoke `bootstrap-tower`. Answer its Scope, Decisions, and Context + constraints questions before
it writes files. The **main Tower** creates only the
[Mission](../reference/glossary.md#mission), [Constraints](../reference/glossary.md#constraints),
and [Roadmap](../reference/glossary.md#roadmap) strategy artifacts:

```text
constitution/
  mission.md
  constraints.md
  roadmap.md
```

Keep them THIN. For this example, the Roadmap might say “manage stockroom products” rather than
pre-writing an HTTP route, status code, database schema, or test list. Requirements and Architect
never produce inception. Inside a selected delivery they remain optional specialists: Requirements
for behavioral complexity, Architect only for load-bearing design.

Local stakeholder constraints are always the policy starting point. If your organization has an
explicit external Authority, opt into Full, collect only the relevant typed facts with its generic
advisor, and reconcile the candidate policy **before** writing behavior that depends on it. A
candidate lock is inspectable input, not proof of authenticity, approval, or compliance.

## 3. Check readiness independently

The deterministic readiness sub-check has a real command:

```powershell
python .github\skills\bootstrap-tower\scripts\scaffold_constitution.py --readiness constitution
```

Then run `inception-readiness` through a fresh reviewer role. The script proves shape; the
reviewer decides whether the Mission, Constraints, current Roadmap phase, and any explicit deferrals
are coherent and THIN. Only a PASS hands work to `plan-slice`.

## 4. Plan one observable capability first

First observe the exact current phase:

```powershell
python .github\skills\bootstrap-tower\scripts\scaffold_constitution.py --current-phase constitution
```

The selector skips fully checked delivered phases, keeps a partial phase current, and skips only
human-deferred history. An exhausted Roadmap blocks for re-cadence. Invoke `plan-slice` for the
returned roadmap capability; it uses this command without a fallback algorithm. The Tower first
reads the governing
artifacts and selectively relevant history, then states its working judgment. If it perceives a
consequential omission or risk, it explains why and asks one contextual decision question; useful
options remain hypotheses until you confirm one. It may also state that no material concern was
found. Confirm scope, decisions, and in-scope constraints before it writes:

```text
specs/YYYY-MM-DD-register-product/
  requirements.md
  plan.md
  validation.md
```

For this bounded LIGHT example, keep the main Tower as the single producer: it can elicit and write
all three Slice Plan files without launching Requirements or Planner. Use a specialist only when a
named complexity justifies the extra context. Do not reward decorative skepticism: the goal is
useful judgment, not a mandatory number of questions or alternatives.

The behavior belongs in EARS requirements. A compact synthetic example is:

| requirement.id | pattern | statement |
|---|---|---|
| `REQ-PRODUCT-01` | ubiquitous | THE SYSTEM SHALL register a product with a unique SKU. |
| `REQ-PRODUCT-02` | event-driven | WHEN a user requests an existing SKU, THE SYSTEM SHALL return that product. |
| `REQ-PRODUCT-03` | unwanted | IF a user registers a duplicate SKU, THEN THE SYSTEM SHALL reject the request. |

Your own statements, sources, validation evidence, and
[evidence stances](../reference/glossary.md#evidence-stances) must come from your
elicitation--not from this table. Use [`prove-now`](../reference/glossary.md#prove-now) when this
slice must prove a property it changes or claims, [`preserve`](../reference/glossary.md#preserve)
when existing evidence must not regress, and
[`deferred-evidence`](../reference/glossary.md#deferred-evidence) only when you can name the exact
future phase and evidence. None is a waiver. If an Authority reconciliation changes applicable
policy, refresh the requirements, plan, and validation before coding rather than treating the old
plan as current.

## 5. Decide whether design review is needed

For a [LIGHT](../reference/glossary.md#light) delivery, record the implementation decision in the
Slice Plan and proceed. The stockroom example can be LIGHT when it introduces no load-bearing
architecture, Authority/policy delta, new dependency, or active constraint-set change.

Use `architecture-review` before coding when a decision is expensive to reverse. An NFR follows
that path only when it needs the load-bearing architectural answer. The Architect creates an ADR
and a terse `design-under-test.md`;
the independent challenger returns SOUND, REWORK, or ESCALATE. A REWORK fixes the upstream design.
An ESCALATE is a human scope decision. Do not add this ceremony merely because every slice has a
design.

## 6. Implement and collect product-native evidence

Implement only the plan. Put the product's actual build, test, lint, scan, or other proof commands
in `validation.md`, then run them in the product toolchain and CI. For example, these are
**illustrative placeholders**, not Control Tower commands:

```text
<your-build-command>
<your-test-command>
<your-lint-or-scan-command>
```

The Tower governs how that evidence maps to requirements and constraints; it does not install a
language-specific build system or claim to verify every language automatically.

## 7. Review independently and record closeout

First run the deterministic Slice Plan pre-check:

```powershell
python .github\skills\review-slice\scripts\review_slice.py specs\YYYY-MM-DD-register-product
```

Then invoke `review-slice` through a fresh reviewer
[Agent](../reference/glossary.md#agent) with no edit access. It runs the commands named in
`validation.md` and judges scope, EARS completeness, constraint evidence, drift, and
teaching-to-test. Only PROMOTE proceeds.

Run the deterministic changelog operation, then `record-closeout`:

```powershell
python .github\skills\record-closeout\scripts\changelog.py
```

Closeout records the Roadmap Delta in existing artifacts:

| Disposition | Example for this tutorial |
|---|---|
| `delivered` | Registering a product and retrieving it by SKU. |
| `remaining` | Product listing, if it was already part of the approved broader capability. |
| `discovered` | A newly observed need, proposed to the human rather than silently added. |
| `evidence` | The slice path, PROMOTE record, and material product CI evidence. |

An approved partial outcome can be split into checked delivered and unchecked remaining wording
only when original scope and intent are preserved. It remains current while unchecked work exists;
all checked means delivered. New capability, priority, phase, strategic dependency, or explicit
deferral stops for human-directed replanning.

## 8. Confirm merge readiness

Before opening the pull request, run the governed-merge command against your repository's actual
default base ref:

```powershell
python framework\scripts\check_merge_ready.py --base origin/<default-branch>
```

Replace `<default-branch>` with the target repository's default branch--for example,
`origin/main` or `origin/master`. It checks that the pull request's dated slices carry a recorded
PROMOTE review. It does not prove the review was genuine, nor does it merge for you. Open the pull
request after the gates are green; merge remains a human command.

## What to do next

Run the next roadmap capability as a new bounded delivery. If reality contradicts the constitution
or a hard constraint, invoke `replan-and-correct` and change the upstream artifact first. For
optional Authority, domain, CI, or MCP work, read [Extending safely](../explanation/extending-safely.md)
before adding a new core mechanism.
