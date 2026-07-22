# Run a governed change

Use this path after constitution readiness passes. A new change has one canonical working memory:
`changes/YYYY-MM-DD-name.md`.

## 1. Select the current Roadmap outcome

Read:

- `constitution/mission.md`
- `constitution/constraints.md`
- `constitution/roadmap.md`
- `constitution/gap-register.md`, when present

Select one incomplete Roadmap phase. If no phase is available, run `replan-and-correct`; do not
create an unanchored record.

## 2. Create and confirm one Change Record

Invoke `plan-slice`. It creates or updates exactly one dated record from
`framework/contracts/change-record.md`.

Before implementation, the record must contain:

- the observable outcome and exact Roadmap anchor;
- one short implementation plan;
- the universal baseline plus obligations activated by explicit triggers;
- a reason and expected evidence for every obligation;
- an honest initial-confirmation state.

The Tower proposes and explains the set. Deterministic gates may add only obligations they can prove
are required with certainty. The human confirms the initial record before work. No automation may
silently remove or de-escalate an obligation.

## 3. Design only when triggered

When load-bearing risk is present, invoke the Architect and keep `design-under-test.md` as the one
named sibling companion. Run `architecture-review` before code. The Tower records the actual
`STABLE` / `SOUND` return in the Change Record; there is no separate review record.

## 4. Implement and append evidence

Implement only the confirmed scope. Preserve the initial obligation rows and append:

- evidence with actual command/result per obligation;
- corrections and invalidated attempts;
- explicit residual dispositions;
- closeout data, including the scope-preserving Roadmap delta and changelog result.

Run:

```powershell
python -B framework/scripts/check_change_record.py --base origin/master
python -B .github/skills/review-slice/scripts/review_slice.py changes/YYYY-MM-DD-name
```

The first gate rejects any add/modify/copy/rename that recreates the retired `specs/` namespace.
Historical retrieval uses the
[baseline migration index](../../../changes/0000-control-tower-baseline.md); the one deletion-only
retirement remains an explicit governed exception in the gate.

## 5. Freeze and review

The sole producer commits and pushes a clean target. Invoke `review-slice` in the no-edit Reviewer
Agent against the exact local and remote SHA. The reviewer returns the actual result; the Tower then
appends it unchanged to the same Change Record.

A current result requires:

- target stability;
- latest verdict `PROMOTE`;
- complete evidence and residual dispositions;
- `status: "reviewed"`.

Any protected post-review change requires a new committed target and a fresh independent review.

## 6. Check merge readiness and stop for the human

Run:

```powershell
python -B framework/scripts/check_merge_ready.py `
  --record changes/YYYY-MM-DD-name.md `
  --constraints constitution/constraints.md
```

Merge readiness does not merge. The final mandatory stop is human merge authorization.
