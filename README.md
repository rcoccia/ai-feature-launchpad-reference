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
- [Canonical governed change](changes/2026-07-23-govern-ai-feature-launch.md)

The later fresh-context replay is a separate Roadmap phase. This product documentation delivers the
feature surface; it does not perform or prewrite that replay.
