---
name: plan-slice
description: 'Selects an outcome-oriented Roadmap capability, forms a contextual judgment, confirms semantics and proof obligations with the human, then creates exactly one dated Change Record. Use for the next feature, bounded change, Roadmap phase, or /plan-slice.'
---

# Plan Change

Create one confirmed, governed Change Record before implementation.

## Workflow

1. Run `python -B .github/skills/bootstrap-tower/scripts/scaffold_constitution.py
   --current-phase constitution`. A nonzero result blocks; never implement another selector. For a
   valid complete Roadmap, relay the actionable human-reopen diagnostic and create no Change Record.
2. Read Mission, the exact current Roadmap section, Constraints, and the critique/gap register when
   present. Retrieve only materially related decisions, Change Records, reviews, and evidence.
3. State the observable outcome, governed facts, Tower judgment, and any real consequential concern.
   Ask one adaptive decision question at a time. Proposals remain unconfirmed until the human acts.
4. Choose the smallest bounded delivery or an explicitly authorized spike. Record confirmed scope,
   decisions, exclusions, and one short implementation plan.
5. Copy `framework/contracts/change-record.md` to
   `changes/YYYY-MM-DD-<lowercase-kebab-name>.md`. Do not recreate the retired `specs/` namespace.
6. Activate the universal baseline `FUN-CHANGE-01`, `FUN-ROADMAP-01`, `NFR-DOCS-01`, and
   `FUN-MERGE-01`. Add contextually applicable obligations with reasons and expected evidence.
   Run `python -B framework/scripts/check_change_record.py --base <target-ref>`; deterministic
   certainty failures may require additional rows, but automation never edits, removes, or
   de-escalates an obligation.
7. Keep `status: "draft"` until the human confirms the outcome, initial obligations, and short plan.
   Record the attested command without claiming identity, then set `status: "confirmed"`.
8. Delegate Requirements or Planner only when named behavioral or coordination complexity benefits
   from isolated context. Delegate Architect only for a load-bearing design. All specialists edit
   sections of this same record; they create no parallel planning record.

## Gotchas

- **Exactly one record:** one governed change has one dated Change Record; companion artifacts need a
  named trigger.
- **No fixed tiers:** baseline plus explicit triggers replaces Standard/Governed or Ship/Show/Ask.
- **No silent applicability decision:** active constraints remain binding; a gate can add only what
  it proves with certainty and cannot infer that another obligation is irrelevant.
- **Human confirmation is a stop:** do not implement a draft or pending initial attestation.
- **LIGHT is still reviewed:** proportional planning never removes universal independent final
  review or human merge authorization.
- **No legacy adapter:** new work never recreates the retired `specs/` namespace; historical
  retrieval starts at `changes/0000-control-tower-baseline.md`.
- **Complete is non-plannable:** readiness may be green while `--current-phase` blocks because no
  work is currently approved. Route reopening through `replan-and-correct`; never auto-reopen.

## References

- Template: `framework/contracts/change-record.md`
- Model/gate: `framework/scripts/change_record.py`,
  `framework/scripts/check_change_record.py`
- Method: `framework/doctrine/operating-model.md`
