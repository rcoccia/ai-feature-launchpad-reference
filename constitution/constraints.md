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
  statement: "Tracked Markdown is UTF-8 without BOM, uses CRLF line endings, and has balanced code fences."
  rationale: "The installed documentation workflow requires reproducible Markdown bytes."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Documentation-Gate","version":"kernel-2026-07-23","path":"framework/scripts/check_docs.py","sha256":"45f74482f6cf295f1d1fabef137d08815244d85a1f9aa5462b6d00764631870f"}]
  applies_to: [coding]
  verification: "framework/scripts/check_docs.py checks every tracked Markdown file"
  projection: ["framework/scripts/check_docs.py"]
  residual: []
  metric: "BOM=0, LoneLF=0, balanced_fences=true"
  severity: hard
  status: active
```

## Inherited Control Tower governance

The documentation law above and the following five inherited method laws form the exact portable
baseline. Three additional method-development laws apply because this governed refresh changes
framework paths. Together they are nine method constraints; the four product constraints above
remain unchanged.

```yaml
constraint:
  id: FUN-CHANGE-01
  category: functional
  statement: "Every governed change has exactly one confirmed dated Change Record before implementation, with explicit outcome, Roadmap anchor, activated obligations, evidence, corrections, closeout, and the actual independent final verdict."
  rationale: "The installed Change Record kernel requires this exact locally resolvable obligation."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Change-Record-Contract","version":"kernel-2026-07-23","path":"framework/contracts/change-record.md","sha256":"69da6b2d235080ffcfaab8ca7057b9ed97ec31562128dabde08cc4a38c500f2b"}]
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
  statement: "The Roadmap uses canonical Phase sections: fully checked phases are delivered, the first non-deferred phase with an unchecked item is current, later eligible phases are planned, and explicit deferred status is skipped. Optional top-level **Lifecycle:** complete is valid only when every non-deferred phase is delivered and means no currently approved work; without it, exhaustion blocks for human re-cadence. Human reopening removes the marker and atomically adds at least one new eligible unchecked phase; contradictory states block."
  rationale: "Readiness, planning, and lifecycle transitions must consume one canonical analyzer without speculative backlog."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Operating-Model","version":"kernel-2026-07-23","path":"framework/doctrine/operating-model.md","sha256":"64b65e4bb117179a1f7afd11e9a4f9d8ca687526036f50ef2b36b118ad6c4152"}]
  applies_to: [planning, design, coding]
  verification: ".github/skills/bootstrap-tower/scripts/scaffold_constitution.py --readiness/--current-phase and framework/scripts/check_change_record.py validate canonical Roadmap state and transitions"
  projection: [".github/skills/bootstrap-tower/scripts/scaffold_constitution.py","framework/scripts/check_change_record.py"]
  residual: [{"id":"FUN-ROADMAP-01::lifecycle-intent","statement":"Review confirms deferral, completion, and reopening are human-authorized and still appropriate; syntax and attestation prove neither identity nor strategic wisdom.","route":"review"}]
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

## Method-development laws for this refresh

```yaml
constraint:
  id: FUN-DETERMINISM-01
  category: functional
  statement: "Mechanically decidable lifecycle and Change Record rules live in scripts and gates rather than prose alone."
  rationale: "The refreshed complete/reopen contract must fail closed through executable enforcement."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Manifesto","version":"tenets-1.0","path":"framework/doctrine/MANIFESTO.md","sha256":"87988d7afd8f1bd4931d250ee1fbcb7fbf8cc99aa52c16d18f0906eca19abcbb"}]
  applies_to: [design, coding]
  verification: "Run the synced Roadmap analyzer and Change Record gate lifecycle cases."
  projection: [".github/skills/bootstrap-tower/scripts/scaffold_constitution.py","framework/scripts/check_change_record.py"]
  residual: [{"id":"FUN-DETERMINISM-01::enforcement-boundary","statement":"Review confirms no mechanically decidable lifecycle rule remains prose-only.","route":"review"}]
  severity: hard
  status: active
```

```yaml
constraint:
  id: NFR-EVAL-01
  category: non_functional
  statement: "The refreshed deterministic lifecycle gates retain must-pass and must-block discrimination at 1.0."
  rationale: "A lifecycle terminal state is safe only when complete, exhausted, contradictory, closeout, and reopen cases remain distinguishable."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Manifesto","version":"tenets-1.0","path":"framework/doctrine/MANIFESTO.md","sha256":"87988d7afd8f1bd4931d250ee1fbcb7fbf8cc99aa52c16d18f0906eca19abcbb"}]
  metric: "gate_discrimination = correct_cases / total_cases == 1.0"
  applies_to: [design, coding]
  verification: "Run the full eval, regression, verification, and bootstrap suites from the exact source checkout plus every targeted check available in the copied LIGHT profile."
  projection: []
  residual: [{"id":"NFR-EVAL-01::source-suite-portability","statement":"Review confirms source-suite success and exact LIGHT byte equality preserve the promoted discrimination in this adopter.","route":"review"}]
  severity: hard
  status: active
```

```yaml
constraint:
  id: TEC-DOMAIN-01
  category: technical
  statement: "Copied Control Tower doctrine and lifecycle enforcement remain domain-agnostic and contain no Launchpad product semantics."
  rationale: "The method refresh must remain portable while product-specific completion evidence stays in product-owned artifacts."
  source: ["normative_spec"]
  reference: [{"source":"normative_spec","id":"Control-Tower-Manifesto","version":"tenets-1.0","path":"framework/doctrine/MANIFESTO.md","sha256":"87988d7afd8f1bd4931d250ee1fbcb7fbf8cc99aa52c16d18f0906eca19abcbb"}]
  applies_to: [design, coding]
  verification: "Prove byte equality with the promoted LIGHT source and review changed method assets for domain-neutral vocabulary."
  projection: []
  residual: [{"id":"TEC-DOMAIN-01::doctrine-agnosticism","statement":"Review confirms copied method assets do not incorporate concrete Launchpad domain semantics.","route":"review"}]
  severity: hard
  status: active
```
