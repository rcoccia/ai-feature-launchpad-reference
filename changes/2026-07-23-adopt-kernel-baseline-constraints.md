---
change: "adopt-kernel-baseline-constraints"
status: "reviewed"
roadmap: "Phase 1: Govern one AI-feature launch request"
---

# Change Record - Adopt kernel baseline constraints

## Intent and first human confirmation

**Observable outcome:** the product constitution on its original `eef6851`-pinned LIGHT kit exposes
the exact six portable Control Tower baseline IDs with locally resolvable normative pins, so the
first product Change Record no longer fails on aggregate `FUN-GOV-01`.

**Initial human confirmation:** `confirmed on 2026-07-23 by explicit delegated human command`

This records an attestation of the command; it does not authenticate identity.

## Scope

- Force-refresh the default 56-file LIGHT profile from exact Control Tower source commit
  `ff77efa7d7983b2eabde9baccf1d35e38c4692fb` and verify byte equality.
- Record the governance/strategy correction in one product ADR.
- Replace aggregate `FUN-GOV-01` with the four missing portable baseline blocks, reuse the existing
  product `NFR-DOCS-01`, and retain the other four product laws unchanged.
- Prove deterministic readiness, exact Phase 1 selection, autonomy, provenance, Change Record shape,
  review pre-check behavior, and documentation hygiene.

## Out of scope

- Product code, feature semantics, product build, feature Change Record, architecture or design
  companions, independent semantic readiness, independent final review, merge readiness success,
  merge, deployment, or operations.
- Mission or Roadmap semantic changes, gate weakening, aliases, copied method ADRs, external
  dependencies, or recreation of `specs/`.

## Confirmed decisions

- **Correction radius:** `governance/strategy`; the active Constraints set changes under the
  explicitly delegated command, while Mission, Roadmap outcome, dependencies, and product semantics
  remain unchanged.
- **Trigger:** `new common consumer` plus `gap-in-coding`; fresh inception passed before the exact
  installed-kernel baseline was enforced, but the first Change Record would fail.
- **Path:** direct upstream adjustment in copied kernel assets and the product Constraints artifact;
  never weaken a gate.
- **Architecture judgment:** no load-bearing product or method design is introduced, so
  `FUN-ARCHREVIEW-01` remains available but is not activated for this correction.

## Activated proof obligations

| Constraint | Why activated | Expected evidence | Initial state |
|---|---|---|---|
| `FUN-CHANGE-01` | This governance correction requires exactly one confirmed dated Change Record. | Branch gate passes with this single record and no `specs/` change. | pending |
| `FUN-ROADMAP-01` | The correction preserves the exact current Phase 1 anchor without changing Roadmap semantics. | Readiness passes and the selector returns exact Phase 1. | pending |
| `NFR-DOCS-01` | The refresh and correction modify tracked Markdown. | Documentation gate reports UTF-8 without BOM, CRLF, and balanced fences. | pending |
| `FUN-MERGE-01` | The branch must stop before parent-owned final review and merge. | Review pre-check passes; merge readiness blocks on confirmed status and pending verdict. | pending |
| `FUN-AUTONOMY-01` | The active Constraints set changes under an explicitly delegated human decision. | The autonomy gate passes because ADR-02 records the strategy correction. | pending |

## Short implementation plan

1. Refresh the default LIGHT profile from the exact correction source and verify inventory, byte
   equality, and preservation boundaries.
2. Add the correction ADR and replace the aggregate constraint with four exact locally pinned
   portable blocks.
3. Run focused baseline, readiness, current-phase, autonomy, provenance, documentation, Change
   Record, review pre-check, merge-boundary, and repository-hygiene checks.
4. Record evidence, corrections, and closeout; commit, push, and open draft PR 2 with final review
   pending.

## Evidence

| Constraint | Result | Evidence |
|---|---|---|
| `FUN-CHANGE-01` | pending | Change Record gate and branch-diff hygiene have not yet been recorded. |
| `FUN-ROADMAP-01` | pending | Readiness and exact current-phase selection have not yet been recorded. |
| `NFR-DOCS-01` | pending | Documentation byte/structure evidence has not yet been recorded. |
| `FUN-MERGE-01` | pending | Review pre-check and expected merge-ready boundary have not yet been recorded. |
| `FUN-AUTONOMY-01` | pending | Autonomy evidence has not yet been recorded. |
| `FUN-CHANGE-01` | pass | On corrective commit `01c6e10407c2174ee024726dff0cb9ec4bc1ebc1`, `python -B framework/scripts/check_change_record.py --base origin/main` passed with exactly this one dated record; the net branch diff contains no framework or `specs/` path. |
| `FUN-ROADMAP-01` | pass | Pinned readiness passed and `--current-phase` returned exact `Phase 1: Govern one AI-feature launch request`. The pinned `eef6851` readiness version predates six-ID enforcement, so this is shape/current-phase evidence rather than proof of the new baseline count. |
| `NFR-DOCS-01` | pass | `python -B framework/scripts/check_docs.py` passed all tracked Markdown after CRLF/no-BOM normalization, including the deterministic changelog and closeout record. |
| `FUN-MERGE-01` | pass | The completed confirmed record passes the review pre-check; merge readiness intentionally blocks only on `status: confirmed` and final verdict `PENDING`. |
| `FUN-AUTONOMY-01` | pass | `python -B framework/scripts/check_autonomy.py --base origin/main` passed because ADR-02 records the delegated Constraints decision without claiming identity. |

## Corrections

- **Governance/strategy correction:** exact inherited constraint IDs replace the aggregate
  `FUN-GOV-01`; the source pin, active constraint set, and durable decision are corrected upstream.
- **Correction cycle 1:** commit `d7c57220b5bd4850672a95d68426ad2c795974cb` attempted the
  originally confirmed 56-file refresh from external method commit `ff77efa7d7983b2eabde9baccf1d35e38c4692fb`.
  The Change Record gate exposed second-order method-development obligations because the product
  branch then changed method-owned Python and framework paths. The parent selected the wider upstream
  boundary rather than adding decorative product constraints or weakening the gate.
- External method commit `08c481f5afaf2c8ae196812c00f003b10190bda3` completed the six-ID
  portable model. This product branch adopts only the locally pinned `FUN-AUTONOMY-01` definition.
  Normal follow-up commit `01c6e10407c2174ee024726dff0cb9ec4bc1ebc1` restores these eight
  refresh-only paths exactly to
  `origin/main`: `.github/skills/bootstrap-tower/SKILL.md`,
  `.github/skills/bootstrap-tower/assets/constraints.md`,
  `.github/skills/bootstrap-tower/scripts/scaffold_constitution.py`,
  `.github/skills/inception-readiness/SKILL.md`, `framework/contracts/change-record.md`,
  `framework/docs/how-to/govern-inception.md`, `framework/docs/reference/constraints.md`, and
  `framework/docs/reference/gates.md`.
- The original confirmed Scope and Short implementation plan remain above as the historical first
  plan. This append-only correction records why the refresh step was reversed and why the observable
  product outcome is now achieved without installing either external method correction.
- No prior product Change Record, architecture review, implementation evidence, or final review
  existed to invalidate. Mission, Roadmap semantics, and product laws other than removal of the
  redundant governance aggregate remain unchanged.

## Closeout

| Disposition | Record |
|---|---|
| delivered | The active constitution now has the six exact portable baseline IDs and four other unchanged product laws, removes aggregate `FUN-GOV-01`, pins every inherited definition to a locally present `eef6851`-kit surface, and preserves the original 56-file kit byte-for-byte. |
| remaining | Independent semantic readiness, independent final review, returned-verdict recording, transition to reviewed, merge-ready success, and human merge authorization remain intentionally pending. Phase 1 product capability remains wholly undelivered and unchecked. |
| discovered | The attempted `ff77efa` refresh activated method-development obligations through changed framework paths; upstream method commits `ff77efa7d7983b2eabde9baccf1d35e38c4692fb` and `08c481f5afaf2c8ae196812c00f003b10190bda3` corrected the portable model, while this adopter retained its original kit boundary. |
| evidence | The net branch diff is `CHANGELOG.md`, this Change Record, `constitution/constraints.md`, and ADR-02. Changelog history is deterministic through corrective commit `01c6e10407c2174ee024726dff0cb9ec4bc1ebc1`; no Roadmap delta is applied because this governance correction does not deliver Phase 1 product scope. |

## Independent final review

**Returned verdict:** `PROMOTE`

### Attempt 1

**Reviewer/date:** Reviewer Agent, 2026-07-23

**Reviewed target:** `89c6f9abdec86c214a8445561c7f73449c25dcd9`

**Remote:** `origin`

**Ref:** `refs/heads/rcoccia-adopt-kernel-baseline-constraints`

**Start local head:** `89c6f9abdec86c214a8445561c7f73449c25dcd9`

**Start tracking head:** `89c6f9abdec86c214a8445561c7f73449c25dcd9`

**Start remote head:** `89c6f9abdec86c214a8445561c7f73449c25dcd9`

**Start PR head:** `89c6f9abdec86c214a8445561c7f73449c25dcd9`

**Completion local head:** `89c6f9abdec86c214a8445561c7f73449c25dcd9`

**Completion tracking head:** `89c6f9abdec86c214a8445561c7f73449c25dcd9`

**Completion remote head:** `89c6f9abdec86c214a8445561c7f73449c25dcd9`

**Completion PR head:** `89c6f9abdec86c214a8445561c7f73449c25dcd9`

**Stability:** `STABLE`

**Returned verdict:** `PROMOTE`

**Gates:** PASS: Change Record gate, review pre-check, documentation gate for 47 tracked Markdown
files, autonomy with ADR-02, provenance for 10 active constraints, pinned constitution readiness, and
exact current `Phase 1: Govern one AI-feature launch request`. Before this return was recorded,
merge readiness blocked only on confirmed status and final verdict PENDING. PR 2 CI had green docs,
autonomy, and provenance; merge-ready was expectedly red only at the governed-merge step.

**Evidence:** The independent readiness judgment found the constitution THIN and coherent with exact
baseline IDs `FUN-CHANGE-01`, `FUN-ROADMAP-01`, `NFR-DOCS-01`, `FUN-MERGE-01`,
`FUN-ARCHREVIEW-01`, and `FUN-AUTONOMY-01`; exact active set 10; and no `FUN-GOV-01`. The five
locally pinned inherited definitions resolve to `framework/contracts/change-record.md`
`26a4d6b94c96728b2af56fe56c6dcc18f3f575eac0fa84b861650eead282c1c6`,
`framework/doctrine/operating-model.md`
`86fe07558f908d3ecad9abe281ce3a0e3b8a7aad63cd7c21c85b8044485eb797`,
`framework/scripts/check_merge_ready.py`
`588759968c5493d5a79e374fccfd373e187781103d9bd1e0519c9719b3548925`,
`.github/skills/architecture-review/SKILL.md`
`bdc295bc8014172fed1ca9f7ecb6f9c9bb4cf27d626fab34a3881a85176f3005`, and
`framework/scripts/check_autonomy.py`
`e577e4b7b5f623c3106920ce4593eca5df6a9a0bf8dbf20423786aff375f25b7`.
Mission and Roadmap are unchanged, with no deferral. The final diff contains only `CHANGELOG.md`,
this Change Record, `constitution/constraints.md`, and ADR-02; `.github/`, `framework/`, README,
LICENSE, Mission, and Roadmap are unchanged. There is no product code, kit sync, method development,
`specs/`, or cache artifact. All 56 LIGHT assets are byte-identical to the original
`eef68510e89bee1d16b0425dbc71c603e3e35c96` adoption. Commit
`d7c57220b5bd4850672a95d68426ad2c795974cb` records the byte-exact `ff77efa` refresh attempt, and
`01c6e10407c2174ee024726dff0cb9ec4bc1ebc1` restores the pinned boundary without rewriting history;
`ff77efa7d7983b2eabde9baccf1d35e38c4692fb` and
`08c481f5afaf2c8ae196812c00f003b10190bda3` remain accurately identified as external field
feedback.

**Summary:** No findings. Constitution readiness is PASS and the Change Record verdict is PROMOTE.
The five activated obligations pass. Product constraints `TEC-STK-01`, `TEC-IDB-01`,
`FUN-APR-01`, and `NFR-CI-01` are correctly not activated because no product behavior or code
changes. `FUN-ARCHREVIEW-01` is present but not activated because no load-bearing design is
introduced. The reviewed target is stable and ready for the governed merge gate and separate human
merge authorization.

**Findings:** none.

| Residual | Disposition | Notes |
|---|---|---|
| `NFR-DOCS-01::didactic-quality` | covered | The public record distinguishes the pinned product kit, attempted refresh, corrective commit, and external method feedback without overstating product or production readiness. |
| `FUN-CHANGE-01::obligation-completeness-and-confirmation` | covered | Exactly one confirmed Change Record governed the correction; all material obligations and correction evidence are present, and delegated confirmation is recorded as attestation rather than authenticated identity. |
| `FUN-ROADMAP-01::deferral-intent` | covered | No phase was deferred or reprioritized; Phase 1 remains exact, current, unchanged, and wholly unchecked. |
| `FUN-MERGE-01::review-genuineness` | covered | One producer owned the branch and local, tracking, remote, and PR heads remained equal to the reviewed target throughout; this PROMOTE records the actual independent return and preserves human merge authorization. |
| `FUN-AUTONOMY-01::human-authorization` | covered | ADR-02 records the explicit delegated human decision for the Constraints correction without claiming identity authentication; Mission and Roadmap were not changed. |
