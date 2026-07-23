# AI Feature Launchpad

> **NON-PRODUCTION TRUSTED-HEADER REFERENCE:** caller-supplied headers are not authentication.
> Run this application only in its local `Development` or test `Testing` environment.

AI Feature Launchpad is a public synthetic-enterprise reference for one governed AI-feature launch.
It demonstrates a request that starts `Pending`, requires distinct Product and AI-Risk approvers who
are also distinct from the requester, supports terminal rejection, and stores durable request and
append-only audit state in SQLite.

The product is intentionally narrow:

- .NET 10 ASP.NET Core Minimal API;
- direct `Microsoft.Data.Sqlite` persistence with one local file;
- integration tests and product-owned GitHub Actions CI;
- no workflow engine, risk scoring, provider abstraction, cloud deployment, or production identity.

## Choose a path

- **Run the finished reference:** continue with [Run locally](#run-locally), then use the
  [API contract](docs/api.md) and [trusted-header boundary](docs/trust-boundary.md).
- **Reconstruct it from zero:** follow the
  [fresh-context tutorial](docs/from-zero-replay.md), then use the
  [operational replay checklist](docs/replay-operations.md).
- **Understand the proof:** read the
  [evidence chain](docs/evidence-chain.md) from Mission through merged PR evidence.

The replay starts in an empty disposable local Git repository. Its method source and instructions
come from public branch `refs/heads/rcoccia-phase2-replay-docs` in
`https://github.com/rcoccia/ai-feature-launchpad-reference`; merged feature baseline
`0a700178269acdf284c14c9033577857357c3dd3` remains the fixed product reference. The disposable
Roadmap reproduces both confirmed phases: Phase 1 is delivered locally, then Phase 2 becomes current
and stays unchecked because the replay report is external evidence rather than a second local slice.

## Run locally

Prerequisites:

- .NET SDK 10.0.302 or a compatible 10.0 feature band;
- a local shell with `curl`.

Restore, build, and test:

```shell
dotnet restore AI.FeatureLaunchpad.sln --locked-mode
dotnet build AI.FeatureLaunchpad.sln --no-restore
dotnet test AI.FeatureLaunchpad.sln --no-build
```

Start the API:

```shell
dotnet run --project src/Launchpad.Api --urls http://localhost:5080
```

The default SQLite file is `./data/launchpad.db`. The directory and database files are ignored by
Git. Set `Launchpad__DatabasePath` to use another local file.

Create the one required product resource:

```shell
curl -i http://localhost:5080/api/launch-requests \
  -X POST \
  -H "Content-Type: application/json" \
  -H "X-Reference-Actor-Id: requester-1" \
  -H "X-Reference-Actor-Role: Requester" \
  -d '{"featureName":"Customer support answer assistant"}'
```

The response starts `Pending` and includes a server-generated request ID. Use that ID for Product
approval:

```shell
curl -i http://localhost:5080/api/launch-requests/REQUEST_ID/approvals/product \
  -X POST \
  -H "X-Reference-Actor-Id: product-approver-1" \
  -H "X-Reference-Actor-Role: Product"
```

AI-Risk approval uses `/approvals/ai-risk` with role `AI-Risk`. Rejection uses `/rejection` with
either `Product` or `AI-Risk`. Decision commands have no request body.

Every response carries:

```text
X-Reference-Authentication-Warning: NON-PRODUCTION; caller-supplied headers are not authentication
```

## Product documentation

- [API contract](docs/api.md)
- [Trusted-header boundary](docs/trust-boundary.md)
- [From-zero replay tutorial](docs/from-zero-replay.md)
- [Operational replay checklist](docs/replay-operations.md)
- [Fresh-context replay evidence](docs/replay-evidence.md)
- [Intent-to-merge evidence chain](docs/evidence-chain.md)
- [Canonical governed change](changes/2026-07-23-govern-ai-feature-launch.md)

Fresh-context replay evidence succeeded. Phase 2 intentionally remains current and unchecked pending
separate human-authorized adoption of the promoted `Lifecycle: complete` contract.
