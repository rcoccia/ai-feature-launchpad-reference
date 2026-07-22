# Constraints: AI Feature Launchpad

These active constraints are the confirmed cross-slice laws for the reference. Detailed endpoint,
schema, transaction, and test-case design belongs to the selected feature slice, not this
constitution.

## Approved product surface

```yaml
constraint:
  id: TEC-STK-01
  category: technical
  statement: "Product implementation uses .NET 10 ASP.NET Core Minimal API and persists launch state and audit history in SQLite."
  rationale: "The reference needs one approved, reproducible product surface rather than a provider or persistence abstraction."
  source: ["stakeholder"]
  reference: []
  applies_to: [requirements, design, planning, coding]
  verification: "Review the selected slice design and verify product build and integration-test evidence use the approved runtime, API style, and SQLite persistence surface."
  projection: []
  residual: [{"id":"TEC-STK-01::approved-surface","statement":"Confirm the delivered product remains within the approved .NET 10 Minimal API and SQLite boundary without introducing an abstraction platform.","route":"review"}]
  severity: hard
  status: active
```

## Non-production identity boundary

```yaml
constraint:
  id: TEC-IDB-01
  category: technical
  statement: "Identity is accepted only through trusted-upstream headers in the reference-local and test boundary, and the product conspicuously identifies this as non-production authentication."
  rationale: "The reference must demonstrate actor-aware governance without implying that header trust is production authentication."
  source: ["stakeholder"]
  reference: []
  applies_to: [requirements, design, planning, coding]
  verification: "Review product behavior, tests, and public documentation for the trusted-header boundary, explicit non-production warnings, and absence of OAuth, JWT, or a real identity-provider implementation."
  projection: []
  residual: [{"id":"TEC-IDB-01::boundary-clarity","statement":"Confirm identity trust cannot reasonably be mistaken for a production authentication design or claim.","route":"review"}]
  severity: hard
  status: active
```

## Approval and audit invariants

```yaml
constraint:
  id: FUN-APR-01
  category: functional
  statement: "A launch request starts Pending; Product approval and AI-Risk approval require actors distinct from each other and from the requester; authorized rejection is terminal; and every successful or refused attempt produces append-only audit evidence consistent with durable request state."
  rationale: "The reference exists to make separation of duties and explainable launch governance observable."
  source: ["stakeholder"]
  reference: []
  applies_to: [requirements, design, planning, coding]
  verification: "Use integration-test and review evidence to demonstrate the invariant across approval, rejection, refused attempts, persistence, and reload behavior."
  projection: []
  residual: [{"id":"FUN-APR-01::governance-consistency","statement":"Confirm actor separation, terminal rejection, and request/audit consistency hold across the complete observable capability.","route":"review"}]
  severity: hard
  status: active
```

## Product-native delivery evidence

```yaml
constraint:
  id: NFR-CI-01
  category: non_functional
  statement: "Product behavior is verified by integration tests executed through product-native GitHub Actions CI."
  rationale: "Intent-to-merge evidence must include executable product proof without extending Control Tower into a product build system."
  source: ["stakeholder"]
  reference: []
  applies_to: [planning, coding]
  verification: "Inspect the product-owned workflow and passing integration-test evidence for the selected capability."
  projection: []
  residual: [{"id":"NFR-CI-01::product-evidence","statement":"Confirm CI evidence exercises the observable capability and remains product-owned rather than embedded in framework gates.","route":"review"}]
  severity: hard
  status: active
```

## Documentation hygiene

```yaml
constraint:
  id: NFR-DOCS-01
  category: non_functional
  statement: "Tracked Markdown is public-facing, valid UTF-8 without BOM, CRLF-normalized, and structurally well formed."
  rationale: "The reference must remain portable, readable, and didactic for contributors replaying the method."
  source: ["stakeholder"]
  reference: []
  applies_to: [requirements, design, planning, coding]
  verification: "Run the documentation gate and review changed documentation for clear public teaching and accurate boundary language."
  projection: ["framework/scripts/check_docs.py"]
  residual: [{"id":"NFR-DOCS-01::didactic-quality","statement":"Confirm changed documentation is layered, public, clear, and does not overstate production readiness.","route":"review"}]
  severity: hard
  status: active
```

## Inherited Control Tower governance

```yaml
constraint:
  id: FUN-GOV-01
  category: functional
  statement: "The adopted Control Tower LIGHT lifecycle remains binding: constitution changes require recorded human decisions, constraint provenance is reproducible, current-phase selection is deterministic, and implementation may merge only through the canonical governed evidence path."
  rationale: "The reference proves the Control Tower method only if its inherited hard governance remains active rather than advisory."
  source: ["stakeholder"]
  reference: []
  applies_to: [requirements, design, planning, coding]
  verification: "Run the inherited readiness/current-phase, autonomy, provenance, and governed-merge gates at their documented lifecycle boundaries, with independent review where judgment is required."
  projection: [".github/skills/bootstrap-tower/scripts/scaffold_constitution.py","framework/scripts/check_autonomy.py","framework/scripts/check_provenance.py","framework/scripts/check_merge_ready.py"]
  residual: [{"id":"FUN-GOV-01::governance-application","statement":"Confirm required independent judgments and lifecycle gates were applied without weakening or bypass.","route":"review"}]
  severity: hard
  status: active
```
