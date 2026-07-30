---
name: smoke-check
description: "Runs a deterministic, build-bound smoke gate from pinned QA mappings and exact runner receipts; only an immutable sprint PASS authorizes handoff."
---

## Purpose and non-authority

Run one bounded smoke check against one immutable build candidate. The workflow consumes current planning and selection artifacts, executes or verifies only exact declared runner rows, records explicit automated and manual evidence, and publishes one immutable receipt.

The workflow does not edit product source, tests, QA plans, regression selections, build artifacts, test manifests, session state, or other workflow artifacts. A QA plan or regression selection is planning evidence, never proof that a test ran. A smoke receipt is evidence only for the exact build, scope, platform, runner, and run identity bound into it.

## Invocation contract

Accept exactly one of these forms:

~~~text
$smoke-check sprint --run-manifest {project-relative-path}
$smoke-check quick --run-manifest {project-relative-path}
~~~

Reject positional scope names, affected-system names, unknown modes, unknown or duplicate flags, missing values, absolute paths, paths outside the project root, and every invocation that supplies loose candidate, plan, check, platform, runner, or receipt arguments. There is no implicit default mode. A caller such as day-one-patch must create or nominate a valid run manifest whose stable check IDs express the intended scope; it must not call `$smoke-check {affected-system}`.

The run manifest uses `schema: cgs-smoke-run-manifest/v1`. It is the sole invocation authority and contains:

- immutable `run_id`, `mode`, `candidate_id`, `build_id`, and `artifact_revision`;
- project-relative path plus revision for the build candidate manifest, build receipt, QA plan, regression selection manifest, test layout, validator manifest, and test execution manifest;
- exact expected identity, schema, revision, status, and currentness fields for each authority;
- exact source commit, engine identity and version, build configuration, target platform, and platform/device matrix;
- exact QA-plan `plan_id`, `scope_id`, `scope_revision`, source/requirement span, ownership revision, and dependency revision;
- exact regression `selection_id`, `selection_revision`, `selection_revision`, and selected Test IDs;
- mode-specific requested Smoke Check IDs, with sprint scope declared as a complete pinned set and quick scope declared as an exact subset;
- exact runner-row IDs, ordered argv arrays, working directory, environment allowlist, parser, exit mapping, timeout, output limit, process-tree cleanup policy, and deterministic controls;
- optional prior execution-receipt path and revision, never an unbound log or newest-file selector;
- required manual checks and permitted automated-substitution contracts;
- canonical evidence destinations and the required `ABSENT` precondition for the run root.

Reject duplicate keys, duplicate IDs, missing revisions, empty or malformed explicit revision values, unsupported schemas, mutable aliases, globs, directory scans, and paths selected by modification time.

## Versioned workflow contract

Freeze this contract before reading project inputs:

~~~yaml template
schema: cgs-smoke-check-workflow-contract/v1
input:
  run_manifest_schema: cgs-smoke-run-manifest/v1
  qa_plan_schema: cgs-qa-plan/v2
  regression_selection_schema: cgs-regression-selection-manifest/v2
  build_candidate_schema: cgs-build-candidate/v1
  build_receipt_schema: cgs-build-receipt/v1
  test_layout_schema: cgs-test-layout/v1
  validator_manifest_schema: cgs-test-validator-manifest/v1
  execution_manifest_schema: cgs-test-execution-manifest/v1
output:
  receipt_schema: cgs-smoke-check-receipt/v2
  evidence_root: production/qa/evidence/smoke/{candidate_id}/{run_id}/
status_axes:
  - Input
  - Scope
  - Automated
  - Manual
  - Platform
  - Execution
  - Evidence
  - Receipt
  - Persistence
verdicts:
  - FAIL
  - INCOMPLETE
  - TARGETED CHECK PASSED
  - PASS
handoff_requires: persisted sprint PASS
~~~

Record the contract schema and revision in the final receipt. Unknown schemas or incompatible major versions make `Input: INVALID` and the observed verdict `INCOMPLETE`.

## Phase 1: Resolve and revision exact authorities

Resolve the literal run-manifest path and every path it names. Normalize project-relative paths, compare resolved real paths with the project root, and reject an escape, missing regular file, unexpected symlink, directory, device, or alternate data stream.

Read exact bounded files before parsing; validate declared identity, schema, version, and revision. Parse using duplicate-key rejection. Compare every observed revision and identity field with the run manifest. Then perform a second consistency pass:

1. The build candidate, build receipt, artifact, source commit, engine version, platform, and configuration must agree exactly.
2. The build receipt must be successful, complete, current, and bound to the candidate manifest and artifact revision.
3. The QA plan must be `cgs-qa-plan/v2`, `Plan Status: CURRENT`, `Effective Status: CURRENT`, and `Scope Completeness: COMPLETE`. Its plan, scope, source span, requirement, ownership, and dependency revisions must match the run manifest.
4. The regression selection must be `cgs-regression-selection-manifest/v2`, have a final current status, and match the QA plan, scope, build applicability, selection revision, and exact selected Test IDs.
5. The test layout, validator manifest, and execution manifest must be current, mutually bound, and match the exact engine version and project root used by the build.
6. Any prior execution receipt must match the candidate, build, artifact, source, QA scope, regression selection, test manifest, runner rows, argv, deterministic controls, platform, and configuration byte-for-byte after canonicalization.

If any authority is missing, stale, partial, invalid, conflicting, or revision mismatched, set the relevant axes to `INVALID`, `STALE`, `PARTIAL`, or `UNKNOWN`; do not execute and classify the observed verdict as `INCOMPLETE`.

Never infer currentness from a filename, branch name, directory location, timestamp alone, or an artifact named `latest`.

## Phase 2: Build a deterministic stable-check ledger

Coverage is keyed by stable identifiers, never by a discovered filename. Build one ledger row for every selected Smoke Check ID:

~~~yaml template
smoke_check_id: SC-{stable-id}
requirement_ids: [TR-{stable-id}]
acceptance_criterion_ids: [AC-{stable-id}]
coverage_unit_ids: [CU-{stable-id}]
test_ids: [TEST-{stable-id}]
owner: {owner-id}
risk: critical|high|medium|low
platform_config_id: {platform-config-id}
execution_kind: automated|manual|automated-with-permitted-manual-substitute
runner_row_id: {runner-row-id-or-null}
manual_contract_id: {manual-contract-id-or-null}
source_revision:
  qa_plan_revision: {revision}
  regression_selection_revision: {revision}
~~~

Create rows only from the exact current QA-plan coverage matrix and exact regression selection. Validate one-to-one or explicitly declared many-to-one relationships among requirement, acceptance criterion, Coverage Unit, Test ID, runner row, platform, and owner. A found test file is not coverage. An unmapped critical or high-risk requirement, selected Test ID without a runner row, duplicate stable ID, ambiguous owner, or missing platform row makes `Scope: INCOMPLETE`.

Selection rules are deterministic:

- `sprint` selects the complete QA-plan Smoke Test Scope plus every current critical changed requirement, verified-fixed regression, integrity check, and mandatory platform baseline declared by the plan.
- `quick` selects exactly the requested stable Smoke Check IDs declared in the run manifest. It never expands by affected-system text and never authorizes handoff.
- Filter only on versioned fields declared in the plan and selection contract. Never filter on prose, filesystem presence, timestamp, or test discovery.
- Sort canonical rows by Smoke Check ID, platform-config ID, Test ID, and runner-row ID using bytewise UTF-8 ordering.
- Reject duplicate canonical keys and reject requested IDs absent from the current plan.

Validate the selected stable Check IDs against the run manifest and record its supplied `selected_scope_revision`. Freeze the selected rows before execution.

## Phase 3: Validate the exact runner

Use only argv arrays from the pinned `cgs-test-execution-manifest/v1`. Never construct a shell string, substitute a convenient local command, call the engine's default test runner, or discover tests at runtime.

For every selected automated row validate:

- runner row ID, executable identity and optional binary revision;
- engine identity and exact version;
- ordered argv array, working directory, and project root;
- named environment allowlist with redacted value revisions where values are sensitive;
- test IDs and platform/configuration identity;
- parser version, structured result path, allowed exit-code mapping, and expected result count;
- deterministic seed, order, locale, timezone, clock policy, parallelism, shard identity, and external-network policy;
- wall-clock deadline, inactivity deadline, stdout/stderr byte limits, result byte limit, and per-record limit;
- process-group creation and complete child-process-tree termination policy.

Any mismatch makes `Execution: INVALID`. Do not silently repair the manifest. Do not fall back to another runner.

A trusted prior execution receipt may replace local execution only when its complete records with declared identities, schemas, and revisions are available and every binding above matches exactly. Otherwise execute the pinned argv rows. Preserve each argv element as one argument and set only allowlisted environment names.

## Phase 4: Execute with bounded partial-result handling

Before each row, record the exact start identity and budgets. Capture stdout and stderr separately up to their byte limits. On deadline, inactivity deadline, cancellation, or output overflow:

1. terminate the full process group or process tree;
2. wait the bounded cleanup interval;
3. Record any surviving child PIDs as cleanup failure;
4. revision the captured bounded bytes;
5. parse only complete records available within the cap;
6. mark incomplete trailing records and missing expected result rows as partial;
7. never retry with changed argv, seed, order, shard, parser, or budgets.

Per-check automated states are `PASS`, `FAIL`, `NOT_RUN`, `TIMEOUT`, `INFRA_ERROR`, `INVALID_RECEIPT`, `PARSE_ERROR`, or `PARTIAL`. Only `PASS` and `FAIL` are conclusive test outcomes. Timeout, truncation, parser failure, missing results, cleanup failure, crash without a complete structured receipt, and a non-mapped exit code set `Execution: PARTIAL` or `INVALID` and force `INCOMPLETE`; they are not product failures and cannot become PASS.

Record each command's exact argv JSON, cwd, environment-name set, runner revision, manifest revision, timestamps, duration, exit code, termination reason, output revisions, parser identity, expected/observed result counts, cleanup result, and per-check outcomes.

## Phase 5: Collect explicit manual and substitution evidence

Every required manual, platform, data-integrity, and performance check has its own stable Smoke Check ID. Every attempted substitution for an automated Test ID has a separate substitution row. No response or an omitted row is `UNKNOWN`, never PASS.

Manual statuses are `PASS`, `FAIL`, `NOT_RUN`, `N-A`, and `UNKNOWN`. `N-A` is valid only when the QA plan contains an applicability rule whose ID and revision are recorded. A manual observation can substitute for an automated Test ID only when the current QA plan contains an explicit allowed-substitution contract binding the same requirement, Test ID, build, platform, method, observer qualification, and evidence class. Without that exact contract, the automated state remains `NOT_RUN` and the run is `INCOMPLETE`.

Each observation or substitute row contains:

~~~yaml template
smoke_check_id: SC-{stable-id}
test_id: TEST-{stable-id-or-null}
substitution_contract_id: SUB-{stable-id-or-null}
status: PASS|FAIL|NOT_RUN|N-A|UNKNOWN
evidence_level: OBSERVED|VERIFIED|UNKNOWN
candidate_id: {candidate-id}
build_id: {build-id}
artifact_revision: {revision}
source_commit: {commit}
platform_config_id: {platform-config-id}
device_id: {device-id}
device_model: {device-model}
os_name: {os-name}
os_version: {os-version}
runtime_version: {runtime-version}
build_configuration: {configuration}
input_method: {input-method}
observer_id: {observer-id}
observed_at: {rfc3339}
method_id: {method-id}
observation_summary: {bounded-redacted-summary}
evidence_path: {project-relative-path-or-null}
evidence_revision: {revision-or-null}
~~~

Require exact device and OS identity for each platform row. A generic platform label such as `pc` is insufficient. Missing device, OS, runtime, build configuration, input method, observer, method, observation, or evidence binding makes that row `UNKNOWN`.

Do not persist a user's verbatim free text. Before persistence, show a bounded normalized preview, allow edit, remove secrets and unnecessary personal data, and store only the redacted summary. If source material must be retained, store only a bounded raw-reference record containing the external or project-relative reference path, declared revision, media type, byte count, retention class, and owner; never copy raw content into the smoke report or receipt. Record redaction rule IDs and the recorder-supplied summary revision.

## Phase 6: Derive status axes and exhaustive verdict

Compute these axes independently: `Input`, `Scope`, `Automated`, `Manual`, `Platform`, `Execution`, `Evidence`, `Receipt`, and `Persistence`. Preserve all per-check rows; do not collapse unknowns into success.

Apply the first matching rule:

| Priority | Condition | Observed Verdict | Handoff Eligible |
|---:|---|---|---|
| 1 | Any conclusive automated, manual, platform, data-integrity, or performance FAIL | `FAIL` | `NO` |
| 2 | Any invalid/stale/missing authority; scope gap; critical/high-risk unmapped item; NOT_RUN/UNKNOWN; timeout; infra, parser, cleanup, or truncation problem; partial receipt; warning requiring review; or missing evidence | `INCOMPLETE` | `NO` |
| 3 | Quick mode and all selected checks are conclusively PASS or valid N-A | `TARGETED CHECK PASSED` | `NO` |
| 4 | Sprint mode, complete current scope, and every required row is conclusively PASS or valid N-A with no unresolved warning | `PASS` | provisionally `YES`, subject to persistence |

No other verdict exists. A product failure outranks infrastructure incompleteness so failures remain visible, while unresolved infrastructure is also listed on its axis. `TARGETED CHECK PASSED` is never equivalent to PASS.

## Phase 7: Build the unified receipt

Create `cgs-smoke-check-receipt/v2` with stable field names and canonical ordering. It must include:

- workflow contract schema/revision and tool revision;
- run manifest path/revision, run ID, mode, timestamps, and canonicalization version;
- candidate, build, artifact, source, engine, platform, configuration, device, and OS identity;
- path/revision/schema/identity/currentness for every authority consumed;
- selected scope revision and every stable-check ledger row;
- runner row IDs, exact argv arrays, cwd, environment-name set, runner and manifest revisions;
- deterministic controls, budgets, execution outcomes, output paths/revisions, and partial-result metadata;
- manual/substitute rows, redaction metadata, and external evidence path/revision;
- all status axes, exhaustive-rule ID, observed verdict, persistence state, and handoff decision;
- canonical evidence paths and revision for every persisted member.

The canonical immutable evidence root is:

~~~text
production/qa/evidence/smoke/{candidate-id}/{run-id}/
  run-manifest.snapshot
  authority-index.json
  selected-scope.json
  automated-receipt.json
  automated.stdout.log
  automated.stderr.log
  manual-evidence.md
  smoke-receipt.json
  report.md
~~~

Write log files only when captured bytes exist. The authority index records each required member, media type, byte count, and declared revision. Legacy paths may be read only when an exact path and revision are pinned for migration evidence; never publish new evidence there and never treat a legacy file alone as handoff evidence.

The human-readable report names each stable Check ID and shows candidate revision, build revision, runner revision, evidence path/revision, status axes, observed verdict, persistence state, and the exact exhaustive rule applied. It must not claim that planned, selected, NOT_RUN, UNKNOWN, partial, or substituted-without-contract work passed.

## Phase 8: Preview and version and existence conflict check-publish atomically

The observed verdict exists independently of persistence. Before writing, present a bounded changeset preview containing destinations, byte counts, revision values, redaction summary, observed verdict, and handoff consequence. A user decline leaves the observed verdict unchanged, sets `Persistence: DECLINED`, and forces `Handoff Eligible: NO`.

For an authorized write:

1. Require the final run root to be absent.
2. Re-read and revalidate the run manifest and every authority. Compare identity, size, and revision with the frozen snapshot.
3. Reconfirm the build artifact identity and exact selected-scope bytes.
4. Reconfirm every external evidence path/revision and reapply the redaction boundary.
5. Render all members in a private same-filesystem staging directory.
6. Validate rendered schema, identity, and declared revision and validate internal references against the authority index.
7. version and existence conflict check by checking the final root is still absent and every authority still matches.
8. Atomically publish the complete directory without overwriting.
9. Read back every member, revalidate revisions, and validate the receipt and index.

If an authority changed, the target appeared, a member is missing, publication is partial, or read-back differs, set `Persistence: CONFLICT` or `FAILED`, force `Handoff Eligible: NO`, preserve the observed verdict, and require a new run ID for retry. Never merge into an existing run, overwrite evidence, or leave a partial final directory.

After verified publication, set `Persistence: VERIFIED`. Only a sprint `PASS` with verified immutable receipt publication has `Handoff Eligible: YES`.

## Phase 9: Handoff and consumer verification

Return the observed verdict even when persistence is declined or fails. Report:

- candidate ID, build ID, artifact revision, source commit, mode, and run ID;
- exact selected-scope revision and count;
- status axes and exhaustive rule ID;
- automated/manual/substitute/platform counts by state;
- timeout, truncation, parser, cleanup, and evidence warnings;
- observed verdict, persistence state, and handoff eligibility;
- exact receipt path and receipt revision when persisted.

A downstream consumer must receive the exact receipt path, receipt revision, candidate ID, build ID, and artifact revision. It must revalidate the receipt, authority index, and all referenced evidence, verify `cgs-smoke-check-receipt/v2`, verify `Persistence: VERIFIED`, and verify the exact build binding. Directory scans, newest-file selection, bare run IDs, summaries, quick-mode results, and unpersisted conversation results are never valid handoff inputs.

## Required invariants

- Exact pinned argv arrays are the only executable authority.
- QA and regression artifacts select work; they do not prove execution.
- Stable requirement and Test ID mappings define coverage; filenames do not.
- Timeout, partial output, parser failure, and missing manual responses cannot pass.
- Manual substitution is explicit, build-bound, and plan-authorized.
- Device, OS, runtime, configuration, observer, and evidence identity are preserved.
- Free text is previewed, bounded, normalized, and redacted before persistence.
- One canonical immutable evidence root and one unified receipt schema are used.
- Observed verdict, persistence, and handoff are separate fields.
- Quick success never authorizes handoff.
- Only a version and existence conflict check-persisted sprint PASS authorizes handoff.
