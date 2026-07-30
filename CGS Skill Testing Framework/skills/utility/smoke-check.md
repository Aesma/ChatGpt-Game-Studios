# Skill Spec: $smoke-check

All revisions in this specification are supplied metadata; no identity or currentness decision is derived from file content.

> **Spec ID**: smoke-check-v2
> **Spec Schema**: cgs-skill-spec/v2
> **Category**: utility
> **Priority**: low
> **Spec written**: 2026-07-22

## Skill Summary

`$smoke-check` consumes one `cgs-smoke-run-manifest/v1`, validates exact build, QA-plan, regression-selection, and test-runner bindings, then produces `cgs-smoke-check-receipt/v2`. Only a verified immutable sprint PASS authorizes handoff. Quick success, product failure, infrastructure incompleteness, missing manual evidence, and unpersisted results do not.

## Static Assertions

- **SC-STA-001**: Frontmatter contains only `name` and non-empty `description`; name is `smoke-check`.
- **SC-STA-002**: Exactly two invocation forms exist and both require `--run-manifest`.
- **SC-STA-003**: Positional affected-system and loose candidate/plan/check arguments are rejected.
- **SC-STA-004**: The run manifest schema is `cgs-smoke-run-manifest/v1`.
- **SC-STA-005**: The QA plan schema is `cgs-qa-plan/v2`.
- **SC-STA-006**: The regression selection schema is `cgs-regression-selection-manifest/v2`.
- **SC-STA-007**: Build candidate, build receipt, artifact, source, engine, platform, and configuration are cross-bound.
- **SC-STA-008**: Exact argv arrays, cwd, runner identity, environment allowlist, parser, and exit map are required.
- **SC-STA-009**: Wall-clock, inactivity, output, result, record, and cleanup budgets are required.
- **SC-STA-010**: Timeout, partial, parser, truncation, and cleanup states force INCOMPLETE.
- **SC-STA-011**: Coverage is keyed by stable requirement, acceptance, Coverage Unit, Test, and Smoke Check IDs.
- **SC-STA-012**: Sprint and quick selection rules are deterministic and scope-versioned.
- **SC-STA-013**: Manual silence is UNKNOWN and unapproved substitution cannot pass an automated Test ID.
- **SC-STA-014**: Manual and platform rows bind device, OS, runtime, build, observer, method, and evidence.
- **SC-STA-015**: Verbatim free text is excluded from persisted receipts and bounded redaction metadata is required.
- **SC-STA-016**: The canonical evidence root is `production/qa/evidence/smoke/{candidate-id}/{run-id}/`.
- **SC-STA-017**: The unified receipt schema is `cgs-smoke-check-receipt/v2`.
- **SC-STA-018**: Observed verdict, persistence state, and handoff eligibility are independent.
- **SC-STA-019**: Publication uses absent-target version and existence conflict check, atomic directory publish, and read-back verification.
- **SC-STA-020**: Only a persisted sprint PASS is handoff eligible.

## Protocol Assertions

- **SC-PRO-001**: Validate raw authority bytes before parsing and reject duplicate keys.
- **SC-PRO-002**: Reject missing, stale, partial, invalid, conflicting, or revision mismatched authorities before execution.
- **SC-PRO-003**: Never infer coverage from files or discover tests at execution time.
- **SC-PRO-004**: Never build a shell command or fall back to an undeclared runner.
- **SC-PRO-005**: Terminate the full process tree after timeout or output overflow.
- **SC-PRO-006**: Preserve complete bounded records and label missing or trailing records partial.
- **SC-PRO-007**: Require an exact current plan contract before manual substitution.
- **SC-PRO-008**: Never publish new smoke evidence to a legacy evidence root.
- **SC-PRO-009**: Apply the exhaustive verdict table in priority order.
- **SC-PRO-010**: A declined or failed write preserves the observed verdict but removes handoff eligibility.
- **SC-PRO-011**: Downstream consumers receive and revalidate the exact receipt path and revision.
- **SC-PRO-012**: The workflow never edits product, test, plan, selection, build, or shared workflow artifacts.

## Test Cases

### Case 1 — Exact runner argv and build binding

#### Fixture

A current sprint run manifest binds build `build-a`, artifact revision `a` repeated 64 times, Godot 4.6.3, Windows debug configuration, runner row `RUN-01`, and an ordered argv array. The local project also contains a convenient but different runner command.

#### Input

Invoke `$smoke-check sprint --run-manifest fixtures/smoke/run-a.yaml`.

#### Expected reads

The exact run manifest and its revision-bound build candidate, build receipt, QA plan, regression selection, test layout, validator manifest, execution manifest, artifact metadata, and runner binary identity.

#### Expected writes

Only a preview until authorization; after authorization, the immutable run root declared by the manifest.

#### Expected non-writes

No product source, tests, authority manifests, live skill files, legacy evidence roots, or existing run directory.

#### Expected behavior

The workflow validates engine version, build/configuration identity, runner identity, cwd, ordered argv, environment allowlist, parser, exit map, and test IDs. It executes only `RUN-01`; the convenient local command is ignored.

#### Assertions

SC-STA-007, SC-STA-008, SC-PRO-001, SC-PRO-004, SC-PRO-012.

#### Case Verdict

PASS only when every exact binding matches and the pinned argv row produces a complete conclusive receipt; otherwise INCOMPLETE.

### Case 2 — Timeout, output cap, cleanup, and partial parsing

#### Fixture

A runner emits two complete structured records, begins a third record, exceeds the output cap, and leaves one child process alive until terminated.

#### Input

Run the pinned automated row with its declared wall-clock, inactivity, output, record, and cleanup budgets.

#### Expected reads

The run manifest, exact execution manifest, parser contract, and expected result-count mapping.

#### Expected writes

Bounded stdout/stderr captures, automated receipt, partial-result metadata, and final report only within the declared immutable run root after authorization.

#### Expected non-writes

No unbounded log, retry manifest, altered argv, changed seed, or result outside the run root.

#### Expected behavior

The full process tree is terminated; complete records are preserved; the trailing record and missing expected rows are PARTIAL; output revisions and cleanup result are recorded; no retry changes execution controls.

#### Assertions

SC-STA-009, SC-STA-010, SC-PRO-005, SC-PRO-006.

#### Case Verdict

INCOMPLETE with `Execution: PARTIAL`; never PASS or product FAIL solely because of timeout or truncation.

### Case 3 — Stable coverage blocks an unmapped high-risk requirement

#### Fixture

The QA plan contains high-risk requirement `TR-SEC-07`, but no Coverage Unit, Test ID, runner row, or manual contract maps to it. A file named `test_sec_07.gd` exists.

#### Input

Invoke sprint mode with a manifest whose expected scope includes `TR-SEC-07`.

#### Expected reads

The exact current QA plan, regression selection, and their stable-ID coverage matrices.

#### Expected writes

A preview or authorized report identifying the stable coverage gap.

#### Expected non-writes

No generated mapping, modified QA plan, modified test file, or handoff receipt claiming PASS.

#### Expected behavior

The filename is ignored as coverage evidence. The missing stable mapping sets `Scope: INCOMPLETE` and blocks execution or handoff as applicable.

#### Assertions

SC-STA-011, SC-PRO-003, SC-PRO-012.

#### Case Verdict

INCOMPLETE.

### Case 4 — Current QA-plan and regression-selection revisions are mandatory

#### Fixture

The run manifest pins QA plan revision `plan-old` and selection revision 4. The files now contain a different QA plan revision and selection revision 5.

#### Input

Invoke either mode with the stale run manifest.

#### Expected reads

Raw bytes and identity fields for the run manifest, QA plan, regression selection, and their bound sources.

#### Expected writes

No evidence files; a conversation result may explain the mismatch.

#### Expected non-writes

No refreshed manifest, no execution receipt, no inferred newest selection, and no authority edits.

#### Expected behavior

The workflow detects the version/revision mismatch before execution, marks the corresponding axes stale or invalid, and refuses to substitute the newer files.

#### Assertions

SC-STA-004, SC-STA-005, SC-STA-006, SC-PRO-001, SC-PRO-002.

#### Case Verdict

INCOMPLETE.

### Case 5 — Manual text is previewed, bounded, and redacted

#### Fixture

A tester submits a long observation containing an access token, email address, and relevant gameplay result. The run manifest permits a manual row and declares a raw-reference retention record.

#### Input

Provide the observation for stable Check ID `SC-MAN-04`.

#### Expected reads

The manual contract, redaction rules, evidence reference metadata, and exact build/platform identity.

#### Expected writes

Only the approved bounded redacted summary, its revision, redaction rule IDs, and raw-reference path/revision/size/media-type/retention/owner record.

#### Expected non-writes

No token, email address, verbatim free text, copied raw attachment bytes, or unrelated personal data.

#### Expected behavior

The workflow presents a normalized preview, permits editing, removes secrets and unnecessary personal data, and persists only bounded redacted fields.

#### Assertions

SC-STA-015, SC-PRO-012.

#### Case Verdict

PASS only if no prohibited raw text or secret reaches rendered evidence; otherwise INCOMPLETE with `Evidence: INVALID`.

### Case 6 — Unified stable-check evidence schema

#### Fixture

A run contains one automated, one manual, and one platform check with complete evidence.

#### Input

Render the candidate receipt and report.

#### Expected reads

Frozen stable-check ledger, authority revisions, execution outcomes, manual rows, platform matrix, and evidence revisions.

#### Expected writes

One `cgs-smoke-check-receipt/v2`, authority index, report, and declared evidence members under the canonical run root.

#### Expected non-writes

No ad hoc second receipt schema, ID-less checklist, unbound evidence path, or legacy report.

#### Expected behavior

Every row includes stable Check ID and the relevant requirement, Test, candidate, build, runner, platform, and evidence revisions. The report exposes the same identities and status axes.

#### Assertions

SC-STA-011, SC-STA-016, SC-STA-017, SC-PRO-008.

#### Case Verdict

PASS when all unified schema fields and member revisions validate; otherwise INCOMPLETE.

### Case 7 — Declined persistence does not rewrite the observed verdict

#### Fixture

All complete sprint checks pass, but the user declines the proposed evidence write.

#### Input

Finalize the run after presenting the bounded changeset preview.

#### Expected reads

The complete in-memory result and rendered preview revisions.

#### Expected writes

None.

#### Expected non-writes

No run root, receipt, report, partial staging publication, or authority mutation.

#### Expected behavior

The workflow returns observed verdict PASS, records `Persistence: DECLINED` in conversation, and reports `Handoff Eligible: NO`.

#### Assertions

SC-STA-018, SC-PRO-010.

#### Case Verdict

Observed PASS; persistence DECLINED; handoff NO.

### Case 8 — Platform evidence requires device and OS identity

#### Fixture

A mobile check says only `platform: mobile` and `status: PASS`; device ID, model, OS version, runtime, configuration, input method, and observer are absent.

#### Input

Ingest the manual platform row.

#### Expected reads

The QA-plan platform matrix and exact manual evidence contract.

#### Expected writes

An authorized report may record the row as UNKNOWN and list missing fields.

#### Expected non-writes

No fabricated device or OS values and no PASS platform row.

#### Expected behavior

Generic platform text is insufficient. The workflow marks the row UNKNOWN and the Platform or Evidence axis incomplete.

#### Assertions

SC-STA-014, SC-PRO-002.

#### Case Verdict

INCOMPLETE.

### Case 9 — Automated NOT_RUN needs an explicit permitted substitute

#### Fixture

Automated Test ID `TEST-SAVE-03` is NOT_RUN. A manual observer supplies a PASS observation, but the current QA plan has no substitution contract for that Test ID.

#### Input

Attempt to use the manual observation as substitute evidence.

#### Expected reads

The exact QA-plan substitution table, stable-check ledger, build identity, manual row, and evidence revision.

#### Expected writes

A separate substitution-attempt row may be persisted; the automated row remains NOT_RUN.

#### Expected non-writes

No automated PASS, no synthesized substitution contract, and no handoff authorization.

#### Expected behavior

The workflow records the manual observation separately, records the absent contract, preserves automated NOT_RUN, and classifies the run incomplete. If the observation itself is absent, its row is UNKNOWN.

#### Assertions

SC-STA-013, SC-PRO-007.

#### Case Verdict

INCOMPLETE.

### Case 10 — Canonical immutable evidence root

#### Fixture

A valid run manifest declares `production/qa/evidence/smoke/candidate-a/run-42/`. A writable legacy directory `production/qa/tests/evidence/` also exists.

#### Input

Authorize report persistence.

#### Expected reads

The declared destination, target-absence precondition, authority index, and rendered member revisions.

#### Expected writes

Only the complete canonical candidate/run directory.

#### Expected non-writes

No new file in the legacy directory and no overwrite or merge into another run.

#### Expected behavior

All receipt members are rendered and indexed under the canonical root. The legacy location remains read-only and is never accepted as standalone handoff evidence.

#### Assertions

SC-STA-016, SC-PRO-008.

#### Case Verdict

PASS only after canonical-root read-back verification; otherwise INCOMPLETE.

### Case 11 — Registered spec is structurally complete and fail-closed

#### Fixture

The registered spec file under `CGS Skill Testing Framework/skills/utility/smoke-check.md`.

#### Input

Run static registration validation for `cgs-skill-spec/v2`.

#### Expected reads

The entire spec and candidate skill.

#### Expected writes

None.

#### Expected non-writes

No spec repair during validation and no live catalog mutation.

#### Expected behavior

Cases are contiguous from 1 through 16. Every case contains Fixture, Input, Expected reads, Expected writes, Expected non-writes, Expected behavior, Assertions, and Case Verdict. Dangerous NOT_RUN, UNKNOWN, timeout, partial, stale, and unpersisted states are expected to block PASS or handoff.

#### Assertions

SC-STA-001 through SC-STA-020; SC-PRO-001 through SC-PRO-012.

#### Case Verdict

PASS only when all structural and fail-closed expectations are present; otherwise FAIL validation.

### Case 12 — Unsupported affected-system invocation is rejected

#### Fixture

A day-one-patch caller attempts `$smoke-check inventory` and another attempts `$smoke-check quick --checks SC-INV-01`.

#### Input

Parse both invocations.

#### Expected reads

The invocation grammar only.

#### Expected writes

None.

#### Expected non-writes

No run manifest, evidence root, QA-plan edit, inferred scope, or execution.

#### Expected behavior

Both invocations are rejected. The caller is instructed to nominate a valid `cgs-smoke-run-manifest/v1` containing exact stable IDs and authority revisions.

#### Assertions

SC-STA-002, SC-STA-003, SC-PRO-012.

#### Case Verdict

INCOMPLETE input; no test verdict or handoff.

### Case 13 — Deterministic selection and scope revision

#### Fixture

The QA plan lists stable checks in reverse order and includes duplicate prose labels. The run manifest pins a canonical selected-scope revision and quick requests three exact Smoke Check IDs.

#### Input

Build the quick stable-check ledger twice.

#### Expected reads

The exact current QA-plan coverage matrix, regression selection, requested stable IDs, and canonicalization version.

#### Expected writes

At most a selected-scope snapshot in the authorized run root.

#### Expected non-writes

No filesystem-discovered tests, prose-filtered rows, affected-system expansion, or reordered authority file.

#### Expected behavior

Both runs filter only declared versioned fields, sort by the documented bytewise key, reject duplicate stable keys, and produce identical selected-scope bytes and revision.

#### Assertions

SC-STA-011, SC-STA-012, SC-PRO-003.

#### Case Verdict

TARGETED CHECK PASSED only after all exact selected checks pass; deterministic mismatch is INCOMPLETE and handoff remains NO.

### Case 14 — Exhaustive verdict and strict handoff

#### Fixture

Four outcome sets are provided: product FAIL plus parser issue; no FAIL but one UNKNOWN; all quick checks pass; and a complete sprint pass.

#### Input

Apply the verdict table to each set in order.

#### Expected reads

All per-check outcomes, status axes, mode, warnings, and evidence completeness.

#### Expected writes

A rendered receipt/report preview for each set; only an authorized complete run may publish.

#### Expected non-writes

No boolean-only summary and no handoff claim for FAIL, INCOMPLETE, or quick success.

#### Expected behavior

Results are respectively FAIL/no handoff, INCOMPLETE/no handoff, TARGETED CHECK PASSED/no handoff, and PASS/provisional handoff pending verified persistence.

#### Assertions

SC-STA-018, SC-STA-020, SC-PRO-009.

#### Case Verdict

PASS only if all four outcomes and handoff decisions match the exhaustive table.

### Case 15 — Immutable version and existence conflict check detects authority drift and target conflict

#### Fixture

The preview is valid, then the QA plan changes before publish and another actor creates the final run root.

#### Input

Authorize the previewed write.

#### Expected reads

Every authority a second time, final-root absence, rendered member bytes, and internal index references.

#### Expected writes

Private same-filesystem staging only; no final publication after conflict detection.

#### Expected non-writes

No overwrite, merge, partial final directory, reused run ID, or authority rollback.

#### Expected behavior

The changed revision and appeared target fail version and existence conflict check. The workflow preserves the observed verdict, sets persistence CONFLICT, forces handoff NO, and requires a new run ID.

#### Assertions

SC-STA-019, SC-PRO-010, SC-PRO-012.

#### Case Verdict

Observed result preserved; persistence CONFLICT; handoff NO.

### Case 16 — Complete sprint happy path and downstream verification

#### Fixture

All authorities are current and revision-matched; deterministic selection is complete; exact runner rows and permitted manual rows conclusively pass; the canonical target is absent.

#### Input

Invoke sprint mode, authorize persistence, then hand the exact receipt path and revision to a downstream consumer.

#### Expected reads

All pinned authorities, execution evidence, manual/platform evidence, rendered bytes, and post-publication read-back bytes.

#### Expected writes

One atomically published immutable canonical run root containing the indexed `cgs-smoke-check-receipt/v2` and report.

#### Expected non-writes

No authority changes, legacy evidence, quick receipt, unindexed member, or mutable latest pointer.

#### Expected behavior

The workflow verifies every binding, applies rule 4, version and existence conflict check-publishes, reads back every member, sets `Persistence: VERIFIED`, and returns the exact receipt path/revision with candidate/build/artifact identities. The consumer revalidate the receipt and every indexed member before accepting handoff.

#### Assertions

SC-STA-001 through SC-STA-020; SC-PRO-001 through SC-PRO-012.

#### Case Verdict

PASS with Handoff Eligible YES only after verified immutable publication and consumer revision verification.

---

## Authoritative P1 audit traceability

| Audit ID | Implemented clause | Concrete case and assertion cells |
|---|---|---|
| `SC-005` | `SKILL.md` Phase 3 exact project runner validation | Case 1 “Exact runner argv and build binding”; `SC-STA-007`; `SC-STA-008`; `SC-PRO-004` |
| `SC-006` | `SKILL.md` Phase 4 bounded execution, cleanup, and partial parsing | Case 2 “Timeout, output cap, cleanup, and partial parsing”; `SC-STA-009`; `SC-STA-010`; `SC-PRO-005`; `SC-PRO-006` |
| `SC-007` | `SKILL.md` Phase 2 stable-ID coverage ledger and high-risk blocker | Case 3 “Stable coverage blocks an unmapped high-risk requirement”; `SC-STA-011`; `SC-PRO-003` |
| `SC-008` | `SKILL.md` Phase 1 current QA-plan/selection/candidate authority binding | Case 4 “Current QA-plan and regression-selection revisions are mandatory”; `SC-STA-004`; `SC-STA-005`; `SC-STA-006`; `SC-PRO-001`; `SC-PRO-002` |
| `SC-009` | `SKILL.md` Phase 5 bounded redacted manual evidence | Case 5 “Manual text is previewed, bounded, and redacted”; `SC-STA-015`; `SC-PRO-012` |
| `SC-010` | `SKILL.md` Phase 2 ledger plus Phase 7 unified receipt | Case 6 “Unified stable-check evidence schema”; `SC-STA-011`; `SC-STA-016`; `SC-STA-017`; `SC-PRO-008` |
| `SC-011` | `SKILL.md` Phase 8 independent observed verdict/persistence/handoff axes | Case 7 “Declined persistence does not rewrite the observed verdict”; `SC-STA-018`; `SC-PRO-010` |
| `SC-012` | `SKILL.md` Phase 5 device/platform evidence matrix | Case 8 “Platform evidence requires device and OS identity”; `SC-STA-014`; `SC-PRO-002` |
| `SC-023` | `SKILL.md` Phase 5 explicit per-check substitute collection | Case 9 “Automated NOT_RUN needs an explicit permitted substitute”; `SC-STA-013`; `SC-PRO-007` |
| `SC-024` | `SKILL.md` Phase 7 canonical immutable evidence root and receipt | Case 10 “Canonical immutable evidence root”; `SC-STA-016`; `SC-PRO-008` |
| `SC-025` | Dedicated spec's complete fixtures and exhaustive fail-closed verdict contract | Case 11 “Registered spec is structurally complete and fail-closed”; `SC-STA-001`; `SC-STA-010`; `SC-PRO-009` |
| `SC-026` | `SKILL.md` invocation schema rejects positional affected-system calls | Case 12 “Unsupported affected-system invocation is rejected”; `SC-STA-002`; `SC-STA-003`; `SC-PRO-012` |
