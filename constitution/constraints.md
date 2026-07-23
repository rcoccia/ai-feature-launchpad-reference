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

The existing product `NFR-DOCS-01` also satisfies the installed kernel's documentation baseline.
The following five inherited method laws complete the exact portable baseline without duplicating
that product constraint.

```yaml
constraint:
  id: FUN-CHANGE-01
  category: functional
  statement: "Every governed change has exactly one confirmed dated Change Record before implementation, with explicit outcome, Roadmap anchor, activated obligations, evidence, corrections, closeout, and the actual independent final verdict."
  rationale: "The installed Change Record kernel requires this exact locally resolvable obligation."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Change-Record-Contract","version":"kernel-2026-07-23","path":"framework/contracts/change-record.md","sha256":"26a4d6b94c96728b2af56fe56c6dcc18f3f575eac0fa84b861650eead282c1c6"}]
  applies_to: [planning, design, coding]
  verification: "framework/scripts/check_change_record.py validates the one-record branch contract; independent review judges obligation completeness and genuine confirmation"
  projection: ["framework/scripts/check_change_record.py"]
  residual: [{"id":"FUN-CHANGE-01::obligation-completeness-and-confirmation","statement":"Review and the human confirm that no material obligation was omitted and the initial confirmation was genuine.","route":"review"}]
  severity: hard
  status: active
```

```yaml
constraint:
  id: FUN-ROADMAP-01
  category: functional
  statement: "The Roadmap uses canonical Phase sections: fully checked phases are delivered, the first non-deferred phase with an unchecked item is current, later eligible phases are planned, explicit deferred status is skipped, and exhaustion blocks for human re-cadence."
  rationale: "Readiness and planning must consume one canonical lifecycle selector."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Operating-Model","version":"kernel-2026-07-23","path":"framework/doctrine/operating-model.md","sha256":"86fe07558f908d3ecad9abe281ce3a0e3b8a7aad63cd7c21c85b8044485eb797"}]
  applies_to: [planning, design, coding]
  verification: ".github/skills/bootstrap-tower/scripts/scaffold_constitution.py --readiness/--current-phase validates and selects canonical Roadmap state"
  projection: [".github/skills/bootstrap-tower/scripts/scaffold_constitution.py"]
  residual: [{"id":"FUN-ROADMAP-01::deferral-intent","statement":"Review confirms every deferral is human-authorized and still appropriate.","route":"review"}]
  severity: hard
  status: active
```

```yaml
constraint:
  id: FUN-MERGE-01
  category: functional
  statement: "Every PR records the actual verdict from an independent final no-edit review on a frozen pushed target, satisfies merge readiness, and stops for human merge authorization."
  rationale: "The installed merge kernel preserves producer-judge separation and the human merge boundary."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Merge-Ready-Gate","version":"kernel-2026-07-23","path":"framework/scripts/check_merge_ready.py","sha256":"588759968c5493d5a79e374fccfd373e187781103d9bd1e0519c9719b3548925"}]
  applies_to: [design, coding]
  verification: "framework/scripts/check_merge_ready.py requires reviewed state, latest STABLE/PROMOTE, complete evidence and closeout, and residual dispositions"
  projection: ["framework/scripts/check_merge_ready.py"]
  residual: [{"id":"FUN-MERGE-01::review-genuineness","statement":"Review and the human confirm single-producer ownership, target stability, independent judgment, and faithful recording of the returned verdict.","route":"review"}]
  severity: hard
  status: active
```

```yaml
constraint:
  id: FUN-ARCHREVIEW-01
  category: functional
  statement: "When a change introduces a load-bearing design decision, an independent blindfolded architecture challenge returns SOUND before coding; ordinary changes do not activate this obligation."
  rationale: "A future architecture-triggered Change Record must resolve the exact constraint required by the installed conditional gate."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Architecture-Review-Skill","version":"kernel-2026-07-23","path":".github/skills/architecture-review/SKILL.md","sha256":"bdc295bc8014172fed1ca9f7ecb6f9c9bb4cf27d626fab34a3881a85176f3005"}]
  applies_to: [design]
  verification: ".github/skills/architecture-review/scripts/check_architecture.py validates challengeable form; independent review judges the trigger and design"
  projection: [".github/skills/architecture-review/scripts/check_architecture.py"]
  residual: [{"id":"FUN-ARCHREVIEW-01::semantic-challenge","statement":"Review confirms the trigger is genuinely load-bearing and the blindfolded challenge is independent and substantive.","route":"review"}]
  severity: hard
  status: active
```

```yaml
constraint:
  id: FUN-AUTONOMY-01
  category: functional
  statement: "A change to constitution/mission.md or constitution/constraints.md requires a recorded human-authorized ADR under constitution/decisions; Roadmap lifecycle movement does not activate this obligation."
  rationale: "The first governed strategy correction must resolve the exact constraint required by the installed autonomy and Change Record gates."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Autonomy-Gate","version":"kernel-2026-07-23","path":"framework/scripts/check_autonomy.py","sha256":"e577e4b7b5f623c3106920ce4593eca5df6a9a0bf8dbf20423786aff375f25b7"}]
  applies_to: [design]
  verification: "framework/scripts/check_autonomy.py requires a new ADR for Mission or Constraints changes; independent review judges genuine human authorization"
  projection: ["framework/scripts/check_autonomy.py"]
  residual: [{"id":"FUN-AUTONOMY-01::human-authorization","statement":"Review confirms the strategic decision recorded by the ADR was genuinely authorized by the human.","route":"review"}]
  severity: hard
  status: active
```
