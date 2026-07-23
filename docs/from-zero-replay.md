# Tutorial: reconstruct AI Feature Launchpad from zero

This tutorial prepares the Roadmap Phase 2 replay. It does not perform the replay, claim that a
replay passed, or replace the later replay evidence.

The replay begins in an empty disposable local Git repository, with no parent conversation history.
An uninvolved agent uses only the public documentation branch as its method and product reference.
It must never call `ask_user`. A material blocker is escalated once with `send_session_message` to
the parent session identified in the replay command, after which the replay agent idles.

## Public source and fixed reference

Use these public coordinates:

| Purpose | Coordinate |
|---|---|
| Repository | `https://github.com/rcoccia/ai-feature-launchpad-reference` |
| Documentation branch | `refs/heads/rcoccia-phase2-replay-docs` |
| Merged product baseline | `0a700178269acdf284c14c9033577857357c3dd3` |
| Merged feature PR | `https://github.com/rcoccia/ai-feature-launchpad-reference/pull/3` |
| Canonical feature record | `changes/2026-07-23-govern-ai-feature-launch.md` |
| Reviewed design | `changes/2026-07-23-govern-ai-feature-launch/design-under-test.md` |

Clone the documentation branch outside the empty target. Record the resolved branch head because
documentation corrections may advance it while the product baseline remains fixed:

```powershell
git clone --branch rcoccia-phase2-replay-docs --single-branch `
  https://github.com/rcoccia/ai-feature-launchpad-reference.git `
  C:\replay\launchpad-public-source
git -C C:\replay\launchpad-public-source rev-parse HEAD
git -C C:\replay\launchpad-public-source merge-base --is-ancestor `
  0a700178269acdf284c14c9033577857357c3dd3 HEAD
```

The source checkout is an input, not the replay target. Do not copy `src/`, `tests/`, solution files,
package manifests, product workflows, constitution files, Change Records, or product documentation
from it. Read the public Markdown surfaces and use its installer only to copy the LIGHT method.
This preserves reconstruction rather than turning the exercise into a file-copy comparison.

## Human-confirmed semantics

The following block is the replay's human-confirmed authority. It is input to inception and planning,
not an implementation suggestion and not private parent context:

- Build a public synthetic-enterprise reference for one governed AI-feature launch request.
- The request starts `Pending`. Product and AI-Risk approvals require actors distinct from each other
  and from the requester. Either authorized role may reject a Pending request, and rejection is
  terminal.
- Durable request state and append-only evidence for successful and refused attempts share one
  SQLite consistency boundary.
- The approved stack is .NET 10, ASP.NET Core Minimal API, direct SQLite, integration tests, and a
  product-owned GitHub Actions workflow.
- Caller-supplied trusted-upstream headers are allowed only inside an explicit local/test,
  non-production identity boundary. They are not authentication.
- The reference is not a workflow platform, provider abstraction, production identity system,
  deployment, operations runtime, or production-ready product.
- The replay may autonomously reconstruct the confirmed artifacts and implementation. It must not
  ask questions with `ask_user`; only a material blocker may be sent to the supplied parent session.
- The local exit is review-ready. Do not create a second cloud repository, PR, merge, or production
  claim, and do not invoke the independent final reviewer.

Implementation choices below remain subordinate to that authority and to the generated constitution.

## 1. Create the empty target and install LIGHT

Prerequisites are Git, Python 3, PowerShell 7, and .NET SDK 10.0.302 or a compatible 10.0 feature band.

```powershell
New-Item -ItemType Directory -Force C:\replay\launchpad-from-zero | Out-Null
git -C C:\replay\launchpad-from-zero init
git -C C:\replay\launchpad-from-zero branch -M main

& C:\replay\launchpad-public-source\framework\adoption\scripts\bootstrap.ps1 `
  -Target C:\replay\launchpad-from-zero `
  -Profile Light

git -C C:\replay\launchpad-from-zero add .
git -C C:\replay\launchpad-from-zero commit -m "Install Control Tower LIGHT"
```

Expected checkpoint:

- the target contains `.github/`, `framework/`, `AGENTS.md`, `CLAUDE.md`, and `.gitattributes`;
- it contains no `constitution/`, `changes/`, product source, product test, or product workflow;
- the installer reports `Control Tower Light profile copied`;
- `git status --short` is empty after the commit.

## 2. Run THIN inception without questions

Invoke `bootstrap-tower` in the target. Supply the human-confirmed semantics above as the already
answered Scope, Decisions, and Context + constraints interview. The replay command has delegated
autonomy to write the three strategy artifacts without `ask_user`.

Create only:

- `constitution/mission.md`;
- `constitution/constraints.md`;
- `constitution/roadmap.md`;
- the inception ADR required for the confirmed Mission and Constraints.

The Mission stays strategy-level: one launch-approval reference, its users, observable success, and
the explicit non-goals. Reproduce the confirmed two-phase Roadmap:

`Phase 1: Govern one AI-feature launch request`

`Phase 2: Reproduce inception and feature from a fresh context`

At inception, Phase 1 is current and unchecked. Phase 2 is planned and unchecked. This planned second
phase prevents Roadmap exhaustion when the Phase 1 delivery is truthfully closed.

The Constraints artifact contains exactly these ten active laws:

| Constraint | Required meaning |
|---|---|
| `FUN-CHANGE-01` | One confirmed dated Change Record before implementation. |
| `FUN-ROADMAP-01` | Canonical current-phase selection and human re-cadence on exhaustion. |
| `NFR-DOCS-01` | Public UTF-8/no-BOM, CRLF, structurally valid Markdown. |
| `FUN-MERGE-01` | Frozen independent final review and separate human merge authorization. |
| `FUN-ARCHREVIEW-01` | Stable independent `SOUND` before code when design is load-bearing. |
| `FUN-AUTONOMY-01` | Mission or Constraints changes require a human-authorized ADR. |
| `TEC-STK-01` | .NET 10 Minimal API with request and audit persistence in SQLite. |
| `TEC-IDB-01` | Trusted headers are local/test-only and conspicuously non-production. |
| `FUN-APR-01` | Pending, actor separation, terminal rejection, and append-only attempt evidence. |
| `NFR-CI-01` | Product behavior is proven by integration tests in product-owned GitHub Actions CI. |

Use the public `constitution/mission.md`, `constitution/constraints.md`, `constitution/roadmap.md`,
and inception ADR only as post-authoring semantic comparisons. Do not copy them into the target.
Phase 2 is a planned reproducibility phase in the disposable Roadmap, not another product capability.

Gate inception:

```powershell
Set-Location C:\replay\launchpad-from-zero
python -B .github\skills\bootstrap-tower\scripts\scaffold_constitution.py `
  --readiness constitution
python -B .github\skills\bootstrap-tower\scripts\scaffold_constitution.py `
  --current-phase constitution
python -B framework\scripts\check_docs.py
python -B framework\scripts\check_provenance.py
```

Obtain an independent `inception-readiness` PASS, then commit inception and tag the immutable replay
base:

```powershell
git add constitution
git commit -m "Bootstrap AI Feature Launchpad inception"
git tag replay-inception
```

Expected checkpoint: readiness is `PASS`, provenance reports ten active constraints, the selector
prints the exact Phase 1 heading, and planned Phase 2 remains unchecked.

## 3. Confirm the sole local delivery Change Record before code

Invoke `plan-slice`. Use the confirmed semantics and exact current Roadmap item. Create exactly:

`changes/YYYY-MM-DD-govern-ai-feature-launch.md`

The record must contain the observable outcome, bounded scope, exclusions, all ten activated
obligations, expected evidence, and a short implementation plan. It must name the load-bearing trigger
`launchpad-consistency-and-trust-boundary`, but no product code exists yet. Record the delegated
human confirmation as an attested command that does not authenticate identity, then set
`status: "confirmed"`.

The canonical public Phase 1 record is a lifecycle example, not a record to copy. Its sequence is:
confirmed plan, design, stable architecture `SOUND`, implementation attempts, append-only corrections,
closeout, independent final-review attempts, actual `PROMOTE`, and human merge. The disposable replay
creates no second Change Record for Phase 2: its external replay report is Phase 2 evidence.

```powershell
python -B framework\scripts\check_change_record.py --base replay-inception
python -B framework\scripts\check_autonomy.py --base replay-inception
python -B framework\scripts\check_docs.py
python -B framework\scripts\check_provenance.py
```

Expected checkpoint: one confirmed dated record, ten obligations, no retired `specs/` path, and no
product implementation.

## 4. Produce and challenge the design

Use an Architect Agent to produce the named design inside the Change Record and its sole allowed
companion:

`changes/YYYY-MM-DD-govern-ai-feature-launch/design-under-test.md`

The design must resolve:

- one Minimal API and one integration-test project;
- direct `Microsoft.Data.Sqlite` access to one file-backed database;
- fixed Product and AI-Risk approval slots;
- exact trusted-header, route, JSON, problem, and warning contracts;
- two `STRICT` SQLite tables, append-only audit triggers, schema versioning, and startup validation;
- atomic state-and-audit writes with `BEGIN IMMEDIATE`;
- fixed validation order, audited refusals, terminal behavior, duplicate behavior, and serialized
  concurrency;
- reload, schema, identity-warning, refusal, and concurrency integration evidence;
- no ORM, repository/provider layer, generic workflow, identity provider, cloud, or production claim.

Use the public design companion, [API contract](api.md), and
[trusted-header boundary](trust-boundary.md) as the complete semantic reference. Run the architecture
form gate, commit and push a stable design target if the agent harness requires a remote ref, and
invoke an independent no-edit architecture reviewer:

```powershell
python -B .github\skills\architecture-review\scripts\check_architecture.py `
  changes\YYYY-MM-DD-govern-ai-feature-launch `
  --constraints constitution\constraints.md `
  --adr constitution\decisions\ADR-YYYYMMDD-01-authorize-launchpad-inception.md
```

Record the actual returned stable `SOUND` in the Change Record. Do not borrow the merged run's
`SOUND`, and do not write product code unless the fresh challenge itself returns `SOUND`.

## 5. Scaffold the product

After `SOUND`, create the conventional solution and projects:

```powershell
dotnet new globaljson --sdk-version 10.0.302 --roll-forward latestFeature
dotnet new sln --name AI.FeatureLaunchpad --format sln
dotnet new web --name Launchpad.Api --output src\Launchpad.Api --framework net10.0
dotnet new xunit --name Launchpad.Api.IntegrationTests `
  --output tests\Launchpad.Api.IntegrationTests --framework net10.0
dotnet sln AI.FeatureLaunchpad.sln add src\Launchpad.Api\Launchpad.Api.csproj
dotnet sln AI.FeatureLaunchpad.sln add `
  tests\Launchpad.Api.IntegrationTests\Launchpad.Api.IntegrationTests.csproj
dotnet add tests\Launchpad.Api.IntegrationTests\Launchpad.Api.IntegrationTests.csproj `
  reference src\Launchpad.Api\Launchpad.Api.csproj
dotnet add src\Launchpad.Api\Launchpad.Api.csproj package `
  Microsoft.Data.Sqlite --version 10.0.10
dotnet add src\Launchpad.Api\Launchpad.Api.csproj package `
  SQLitePCLRaw.bundle_e_sqlite3 --version 2.1.12
dotnet add tests\Launchpad.Api.IntegrationTests\Launchpad.Api.IntegrationTests.csproj package `
  Microsoft.AspNetCore.Mvc.Testing --version 10.0.10
dotnet restore AI.FeatureLaunchpad.sln --use-lock-file
```

Set `RestorePackagesWithLockFile` and `TreatWarningsAsErrors` for both projects. Keep the generated
lock files. Add the local SQLite and .NET build outputs to `.gitignore`.

## 6. Implement only the reviewed contract

The expected product surfaces are:

- `src/Launchpad.Api/`: host, API contract and validation, direct SQLite schema/store, settings, and
  development launch settings;
- `tests/Launchpad.Api.IntegrationTests/`: actual-host, file-backed HTTP integration tests;
- `.github/workflows/product-ci.yml`: locked restore, Release build, and Release tests on pull
  requests and main pushes;
- `README.md`, `docs/api.md`, and `docs/trust-boundary.md`: product operation and boundary evidence.

Reconstruct behavior from the reviewed design and public API/trust documents. Do not read or copy
the public branch's C# source or test implementation. Preserve the fixed aggregate and exact
non-production boundary. The integration suite must prove creation, both approval orders, actor
separation, both authorized rejection roles, retained pre-rejection approval, successful and refused
audit events, terminal attempts against Approved and Rejected targets, duplicates, parallel commands,
durable reload, schema and append-only enforcement, warning behavior, and Production startup refusal.

The merged reference used 28 integration cases. A faithful replay should reach the same count and
must not weaken semantic coverage to make the number pass.

Run product proof:

```powershell
dotnet restore AI.FeatureLaunchpad.sln --locked-mode
dotnet build AI.FeatureLaunchpad.sln --configuration Release --no-restore
dotnet test AI.FeatureLaunchpad.sln --configuration Release --no-build
dotnet list AI.FeatureLaunchpad.sln package --include-transitive --vulnerable
```

Expected checkpoint: zero build warnings or errors, 28 passing integration cases with no skips, and
no vulnerable package.

## 7. Reach review-ready and stop

Append every implementation and correction attempt to the Change Record; never replace earlier
evidence. Run `record-closeout`, truthfully check the delivered Phase 1 Roadmap item, generate the
deterministic changelog, and leave the Phase 1 record historically anchored to its exact Phase 1
heading with status `confirmed` and independent final verdict `pending`. Phase 2 then becomes current
and remains unchecked.

Run the local pre-review gates:

```powershell
python -B .github\skills\bootstrap-tower\scripts\scaffold_constitution.py `
  --readiness constitution
python -B .github\skills\bootstrap-tower\scripts\scaffold_constitution.py `
  --current-phase constitution
python -B framework\scripts\check_change_record.py --base replay-inception
python -B framework\scripts\check_docs.py
python -B framework\scripts\check_autonomy.py --base replay-inception
python -B framework\scripts\check_provenance.py
python -B .github\skills\review-slice\scripts\review_slice.py `
  changes\YYYY-MM-DD-govern-ai-feature-launch.md `
  --constraints constitution\constraints.md
git diff --check replay-inception..HEAD
git status --short
```

Readiness must remain green and the selector must print exact
`Phase 2: Reproduce inception and feature from a fresh context`. The Change Record gate still finds
the sole Phase 1 record and accepts its historical Phase 1 Roadmap anchor.

`check_merge_ready.py` must still fail only because the Phase 1 record is `confirmed` and the
independent final verdict is `pending`. That is the correct review-ready boundary, not a failed
replay.

Do not implement or close local Phase 2, create a second replay Change Record, invoke the final
Reviewer Agent, create a second GitHub repository or PR, merge, or deploy. Record the replay
measurements described in [Operational replay](replay-operations.md), send that external Phase 2
evidence to the parent, and stop.
