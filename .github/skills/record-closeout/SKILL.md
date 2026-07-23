---
name: record-closeout
description: 'Prepares deterministic changelog and scope-preserving Roadmap closeout evidence inside a confirmed Change Record before the final frozen review target. Use when implementation evidence is complete and the change is ready to freeze.'
---

# Record Closeout

Prepare closeout before final review so the independent judgment covers the complete merge target.

## Workflow

1. Require a `confirmed` Change Record whose implementation evidence passes every activated
   obligation, whose Corrections section is explicit, and whose triggered architecture result is
   stable `SOUND`.
2. Run `python -B .github/skills/record-closeout/scripts/changelog.py` from the repository root.
3. Apply the scope-preserving Roadmap delta. Record exactly these dispositions in `## Closeout`:
   `delivered`, `remaining`, `discovered`, and `evidence`. Use explicit `none` only when it is a real
   semantic result, not a placeholder.
4. A fully delivered approved outcome may be checked with concise evidence. Partial delivery splits
   delivered and remaining wording only when the approved scope is preserved. New capability,
   priority, phase, dependency, or deferral requires human-directed replan.
5. When this delivers the final eligible phase, do not leave it unchecked or invent a placeholder.
   The candidate must add top-level `**Lifecycle:** complete`, a newly accepted human-authorized
   ADR, and this protected Change Record section in the same diff:

   ```markdown
   ## Roadmap lifecycle authorization

   **ADR:** `constitution/decisions/ADR-YYYYMMDD-NN-lowercase-kebab-name.md`
   ```

6. Commit and push changelog, Roadmap, Change Record, implementation, design, and evidence. Freeze
   that target, then invoke universal final no-edit review.
7. After the reviewer returns, the Tower appends the actual result. Only stable `PROMOTE`, complete
   residual dispositions, `status: "reviewed"`, merge-ready success, and human authorization permit
   merge.

## Gotchas

- **Closeout is reviewed:** do not append governance state after final review and pretend the old
  verdict covers it.
- **Changelog is deterministic, Roadmap delta is judgment:** never encode semantic closeout in the
  helper.
- **No separate delta/review file:** the Change Record is the durable audit chain.
- **No baseline retirement unless triggered:** the reserved deletion-only transition is a separate
  governed Change Record.
- **Complete is reopenable:** it means no currently approved work, not archival or permanent closure.

## References

- Changelog helper: `./scripts/changelog.py`
- Shared model: `framework/scripts/change_record.py`
- Roadmap rules: `framework/doctrine/operating-model.md`
