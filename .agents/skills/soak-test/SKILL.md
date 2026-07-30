---
name: soak-test
description: "Plans and finalizes exact build-bound endurance runs with expanded checkpoints, unit-safe resource evidence, immutable receipts, and fail-closed stability handoff."
---

# Soak Test

## Purpose and authority boundary

Plan one reproducible endurance protocol, register one exact run, ingest immutable evidence, and finalize one build-bound result. A human or separately authorized harness performs the long-running workload. This workflow does not invent samples, launch an undeclared runner, edit product code, repair tests, change a build, or convert a protocol into proof of execution.

Planning artifacts, run manifests, evidence receipts, results, readiness decisions, and handoff receipts remain distinct. Writing a protocol means `PLANNED`, never executed. Finalizing a result means the evidence artifact is immutable and verified; it does not itself mean stability or release readiness passed.

## Exact invocation contract

**P1 Clause SOAK-CL-004 — Explicit target/profile/build plan grammar.**

Accept only these forms:

~~~text
$soak-test plan {target-id} --candidate-manifest {path} --build-receipt {path} --profile-manifest {path} --environment-manifest {path} --metric-policy {path} --adapter-manifest {path} --protocol-id {protocol-id} --duration-ms {positive-integer} --interval-ms {positive-integer} --focus {dimension-list} [--history-index {path}] [--supersedes {protocol-path}] [--save]
$soak-test start --run-manifest {path}
$soak-test ingest --run-manifest {path} --receipt-manifest {path}
$soak-test finalize --run-manifest {path} --finalize-manifest {path}
$soak-test status --run-manifest {path}
~~~

`focus` is a canonical comma-separated subset of `stability,memory,performance,experience`, with duplicates rejected. There is no implicit target, duration, focus, profile, environment, build, or mode.

Reject unknown modes, unknown or duplicate flags, missing values, extra positional values, ambiguous duration text, non-positive durations, intervals longer than duration, unsafe IDs, absolute paths, dot segments, globs, directory scans, symlink escapes, and missing declared revisions where the selected contract requires them. Reject a plan request that omits the target/system, duration, focus, profile conditions, or exact candidate/build identities. On rejection, write nothing and return `Workflow Verdict: BLOCKED`.

An explicitly bounded request authorizes its in-scope candidate writes. Otherwise preview one complete changeset and obtain one approval before the first write. Never commit, publish outside the project, invoke another workflow, or mutate a source authority automatically.

## Versioned contracts

Freeze the workflow contract before reading input bytes:

~~~yaml template
schema: cgs-soak-test-workflow-contract/v1
inputs:
  candidate: cgs-build-candidate/v1
  build_receipt: cgs-build-receipt/v1
  workload_profile: cgs-soak-workload-profile/v1
  environment_profile: cgs-soak-environment-profile/v1
  metric_policy: cgs-soak-metric-policy/v1
  adapter: cgs-soak-adapter-manifest/v1
  history_index: cgs-soak-history-index/v1
  run_manifest: cgs-soak-run-manifest/v2
  ingest_manifest: cgs-soak-ingest-manifest/v1
  finalize_manifest: cgs-soak-finalize-manifest/v1
outputs:
  protocol: cgs-soak-protocol/v2
  evidence_receipt: cgs-soak-evidence-receipt/v2
  result: cgs-soak-result/v2
  completion_receipt: cgs-soak-completion-receipt/v2
canonical_root: production/qa/soak-tests/
~~~

Unknown or incompatible schema versions are blocking. Record the workflow-contract schema and revision in every output.

## Artifact identity and immutable layout

Use only this layout for new evidence:

~~~text
production/qa/soak-tests/
  _protocols/{protocol-id}/
    protocol.json
    protocol.md
  {run-id}/
    run-manifest.json
    evidence/
      {receipt-id}/
        source.{extension}
        samples.jsonl
        receipt.json
    result.json
    report.md
    completion-receipt.json
~~~

Every protocol ID, run ID, and receipt ID is stable, unique, and includes more identity than a date. Reject path separators and timestamp-only IDs. Every final destination must be absent. Never overwrite, extend in place, merge into, or select by modification time. A changed candidate, build, profile, environment, adapter, metric policy, schedule, observer, or evidence set uses a new immutable ID.

Legacy protocol or result files are read-only advisory material only when an exact path and revision are supplied. They are not evidence for `cgs-soak-result/v2` and are never handoff eligible.

## Phase 1: Resolve exact candidate, build, and context authorities

Resolve literal project-relative paths and real paths. Require regular files under the project root. Read each authority once, reject duplicate keys, and validate its stable ID, schema/version, explicit revision, and cross-references.

The candidate manifest and build receipt must agree exactly on:

- candidate ID, build ID, artifact path and revision;
- source commit, engine identity and exact version;
- target platform, device class, architecture, and build configuration;
- creation identity, producer/run identity, status, and completeness;
- target system, scene or service applicability.

Require the build receipt to be successful, complete, current, and verifiable. revalidate a local artifact. For a remote artifact, require a signed or issuer-verifiable receipt that binds the same identities and revision. A filename, branch, tag, or user statement is not build evidence.

The workload profile binds stable target ID, ordered step IDs, rates or repetitions, player/bot count, network conditions, save/state setup, deterministic seed or explicit nondeterministic rationale, resets, transitions, incidents to induce or avoid, and profile revision/revision.

The environment profile binds platform, exact device/hardware identity, OS and runtime versions, graphics/quality settings, power and thermal mode, locale, input, accessibility configuration, network topology, background services, and environment revision/revision.

The metric policy binds every metric, unit, budget/baseline, checkpoint requirements, confidence policy, early-stop trigger, recovery policy, and named consumer gate policy. The adapter manifest binds the configured engine/version, collection tools, parsers, source fields, unit conversions, harness execution manifest, and cleanup capability.

All target/build/profile/environment/metric/adapter applicability keys must match. Any missing, stale, partial, conflicting, unsupported, or revision-mismatched authority sets `Input Status: INVALID` or `STALE`, returns `Workflow Verdict: BLOCKED`, and writes nothing.

Consume QA plans, playtest results, bug records, or prior soak results only through explicitly supplied project-relative paths and revision values declared by the request authorities. Revalidate their canonical schema and current status. Other context is labeled `ADVISORY` and cannot change the scope, thresholds, or result. Never read the most recent context.

**P1 Clause SOAK-CL-008 — Explicit version-bound context only.** The preceding
authority rule is the normative closure clause for audit item SOAK-008.

## Phase 2: Validate engine adapter and exact harness contract

**P1 Clause SOAK-CL-007 — Configured engine/version adapter only.**

Load only the adapter matching the candidate's configured engine and exact version. Validate adapter path, declared revision, schema, version range, collection-tool binaries or identities, parser versions, source fields, and unit conversion functions. Never include guidance for another engine or substitute a generic engine heuristic.

The adapter's harness execution manifest must declare:

- executable identity and optional binary revision;
- ordered argv array, project-root-contained cwd, and environment-name allowlist;
- exact target/build/profile/environment identities;
- deterministic seed/order/locale/timezone/clock controls;
- heartbeat interval and missing-heartbeat timeout;
- per-checkpoint capture timeout and whole-run hard deadline;
- stdout, stderr, structured-result, and per-record byte limits;
- process-group creation, child-process enumeration, graceful-stop interval, forced-stop interval, and final cleanup check;
- recovery observation window, recovery checkpoint IDs, and restart prohibition or exact restart policy;
- exit-code map, parser identity, expected evidence paths, and redaction rules.

This workflow never builds a shell string or falls back to another runner. If the engine version, adapter, runner, or cleanup/recovery capability cannot be verified, return `Adapter Status: NEEDS_CONFIRMATION`, `Handoff Eligible: NO`, and do not call the protocol executable or gate capable.

## Phase 3: Normalize metrics, units, budgets, and baselines

Every resource or experience metric has one stable Metric ID and this complete contract:

~~~yaml template
metric_id: MET-{stable-id}
dimension: stability|memory|performance|experience
value_kind: gauge|counter|event|ordinal
source_field: {adapter-source-field}
raw_unit: {declared-unit}
canonical_unit: {declared-unit}
conversion_id: {conversion-id}
conversion_version: {version}
aggregation: {aggregation-id}
warmup_ms: {nonnegative-integer}
baseline_required: true|false
baseline_path: {project-relative-path-or-null}
baseline_revision: {revision-or-null}
baseline_revision: {revision-or-null}
comparison: {operator}
threshold_value: {number-or-null}
noise_tolerance: {number-and-unit}
minimum_valid_samples: {positive-integer}
uncertainty_method: {method-id}
confidence_requirement: {policy}
stop_trigger_id: {trigger-id-or-null}
~~~

Use canonical, unambiguous units. Bytes, milliseconds, seconds, hertz, frames per second, percentages, degrees Celsius, counts, and named ordinal scales must never be mixed without a pinned conversion ID/version. Record counter reset and wrap rules. Reject incompatible dimensions, unknown units, lossy implicit conversions, missing conversion provenance, non-finite numbers, and values outside the source field's declared range.

Each threshold comes from a current project budget or an explicitly approved baseline artifact that matches target, build family, workload, environment, adapter, metric definition, warm-up, aggregation, and unit. Record source path, declared revision, revision, approval identity, applicability, comparison operator, and uncertainty allowance.

Never invent a universal percentage, byte amount, consecutive-checkpoint count, or engine default. Missing, stale, mismatched, unapproved, or unit-incompatible threshold yields `Threshold Status: UNAVAILABLE` for that metric. The protocol may be planned, but `Gate Capable: NO`; a result for that metric is `INCONCLUSIVE`, never PASS or FAIL.

A trend, slope, leak, or time-to-exhaustion result is permitted only when the metric policy pins the model ID/version, minimum sample count, excluded transitions and GC windows, fit-quality threshold, confidence interval, and validity range. Otherwise report the observed series without a leak classification or extrapolation.

## Phase 4: Create the complete endurance protocol

`plan` constructs `cgs-soak-protocol/v2` only after Phase 1 and Phase 2 validate. It binds all exact authority paths/revisions and identities, duration, interval, focus dimensions, metric contracts, named gate policy, safety procedures, evidence retention, and retest policy.

Expand the entire checkpoint schedule deterministically:

**P1 Clause SOAK-CL-012 — Fully expanded stable checkpoint schedule.**

1. Create warm-up checkpoints as declared by each metric policy.
2. Create baseline `CP-000000` at elapsed time zero after warm-up.
3. Add monotonically increasing IDs `CP-000001` onward at exact `interval_ms` offsets.
4. Include a final checkpoint at exactly `duration_ms`; if duration is not divisible by interval, mark the last interval as partial by design.
5. For each checkpoint, record planned elapsed milliseconds, required Metric IDs, workload step/range, environment snapshot fields, collection source, capture timeout, observer prompt, and evidence-preservation action.
6. Canonically sort by planned elapsed time, Checkpoint ID, and Metric ID, then revision the schedule bytes as `checkpoint_schedule_revision`.

The protocol contains no observed values. It defines missing checkpoint semantics as `NOT_COLLECTED`, never zero, carry-forward, interpolation, or PASS.

Every early-stop row contains a stable Trigger ID, observed condition, unit, minimum persistence, evidence required, safety action, process-tree cleanup sequence, recovery window, recovery checkpoints, and classifications for confirmed, unconfirmed, and evidence-failure outcomes. Mandatory trigger families include crash, hang or heartbeat loss, OOM risk, thermal safety, data corruption, runaway resource use, and observer emergency stop. A project may add stricter triggers but may not weaken mandatory safe cleanup.

**P1 Clause SOAK-CL-005 — Mandatory early-stop and evidence-preservation contract.**
The preceding trigger families and their evidence/action/classification fields are
the normative closure clause for audit item SOAK-005.

Without `--save`, return the exact candidate bytes and:
- `Artifact Status: PLANNED`
- `Execution Status: NOT_STARTED`
- `Workflow Verdict: PROTOCOL_DRAFTED`
- `Handoff Eligible: NO`

With `--save`, preview the two protocol members and their revisions, require both final paths absent, revalidate all authorities, render in same-filesystem staging, atomically publish the protocol directory, and read back both files. Then return `Workflow Verdict: PROTOCOL_PLANNED`, the exact protocol path/revision, and handoff NO. Planning never returns a Stability, Memory, Performance, Experience, or Readiness PASS.

## Phase 5: Preserve exact protocol history without overwrite

**P1 Clause SOAK-CL-006 — version-bound new protocol extension without overwrite.**

If a history index is supplied, require `cgs-soak-history-index/v1`, a declared revision, and a canonical target/profile/environment key. Validate every referenced protocol path/revision before using it. Do not scan for a recent protocol.

An extension requires both `--supersedes` path and revision, a new protocol ID, and a new final directory. Verify the predecessor's candidate/build/profile/environment/schedule identity and state. Record predecessor path/revision and the exact changed fields in the new protocol. Never edit the predecessor, its run manifests, evidence, results, or history bytes. The owning history workflow may later add the new protocol through its own authorized version and existence conflict check; this workflow does not mutate a shared history index.

## Phase 6: Register one exact run manifest

`start` consumes one complete `cgs-soak-run-manifest/v2` and verifies its CLI revision. It must bind:

- unique run ID and absent canonical run root;
- protocol ID/path/revision and `cgs-soak-protocol/v2` bytes;
- exact candidate/build/artifact/source, target, profile, environment, adapter, metric policy, and gate-policy identities/revisions;
- observer and harness identities;
- actual RFC 3339 start time and monotonic origin;
- the full protocol Checkpoint ID list;
- an actual scheduled RFC 3339 timestamp for every checkpoint, calculated from start time and planned offset;
- exact harness argv row, cwd, deterministic controls, budgets, stop/cleanup/recovery contracts;
- evidence classification and intended result paths.

Reject duplicate Checkpoint IDs, non-increasing offsets or timestamps, schedule/revision mismatch, a start time inconsistent with scheduled times, existing targets, placeholders, or changed authority bytes.

Publish only the exact immutable `run-manifest.json` after authority revalidation, target-absence version and existence conflict check, atomic directory creation, and read-back. Return `Artifact Status: RUNNING`, `Execution Status: NOT_STARTED`, `Workflow Verdict: RUN_REGISTERED`, and handoff NO. Registering the run does not prove the harness launched.

## Phase 7: Ingest append-only checkpoint evidence

**P1 Clause SOAK-CL-010A — Append-only immutable evidence ingest.**

`ingest` verifies the exact run-manifest path/revision and one `cgs-soak-ingest-manifest/v1`. The ingest manifest binds a unique receipt ID, run/protocol/candidate/build identities, source evidence path/revision/media type/size, parser and adapter identity, expected checkpoint subset, observer or harness issuer, collection interval, and receipt destination.

Read source bytes once and revision before parsing. Enforce declared total, line, record, and field-size limits. Reject a source directory, unsupported media type, oversize input, symlink escape, duplicate keys, duplicate Sample IDs, samples for another run/build/profile, or a receipt destination that exists.

Each immutable sample row contains:

- stable Sample ID, Checkpoint ID, Metric ID, and Trigger/Event ID when applicable;
- scheduled timestamp, actual RFC 3339 timestamp, and monotonic elapsed milliseconds;
- observed raw value/unit and canonical value/unit;
- conversion ID/version and conversion result;
- workload step/repetition, seed, and relevant state;
- device, OS/runtime, build configuration, power/thermal state, and network state;
- observer/harness identity, collection method/tool/parser versions;
- source path, record locator, and raw evidence revision;
- row status `COLLECTED`, `PARTIAL`, `INVALID`, or `UNKNOWN`.

Do not interpolate, smooth, carry forward, silently convert, or classify the raw value in the sample ledger. If a supplied record is truncated, unparsable, unit-incompatible, outside the declared range, or lacks provenance, preserve the bounded raw reference and mark the sample `PARTIAL`, `INVALID`, or `UNKNOWN`.

In one all-or-none transaction, render `source.{extension}`, `samples.jsonl`, and `receipt.json`; index their byte counts/revisions; verify internal references; compare-and-swap the absent receipt directory; atomically publish; and read back. Existing receipts and sample rows never change. Return `Workflow Verdict: EVIDENCE_INGESTED`, `Artifact Status: RUNNING`, and handoff NO.

## Phase 8: Verify timeout, cleanup, recovery, and partial evidence

Evidence for an early stop or hard timeout must include the trigger or watchdog event, last heartbeat, last complete checkpoint, termination timestamps, graceful and forced stop attempts, child-process enumeration, final process-tree state, output-cap state, evidence flush result, and recovery observations.

Classify the execution control independently:

- `Stop Status: CONFIRMED` when the declared trigger is supported by exact evidence;
- `Stop Status: UNCONFIRMED` when an operator stopped but trigger evidence is insufficient;
- `Cleanup Status: CLEAN` only when the full declared process tree is gone and required flushes completed;
- `Cleanup Status: DIRTY` when a child survives, flush fails, or cleanup exceeds its deadline;
- `Cleanup Status: UNKNOWN` when cleanup proof is missing;
- `Recovery Status: RECOVERED` only when every required recovery checkpoint meets its explicit recovery rule;
- `Recovery Status: NOT_RECOVERED` when a conclusive recovery rule fails;
- `Recovery Status: UNKNOWN` when recovery samples or rules are missing;
- `Recovery Status: NOT_REQUIRED` only when the protocol explicitly says so.

Preserve every complete sample collected before termination. Mark all later scheduled checkpoints `NOT_COLLECTED` with the exact termination reason. A timeout, dirty/unknown cleanup, unknown recovery, output truncation, evidence flush failure, parser failure, or missing expected sample produces partial or inconclusive evidence and can never become a technical PASS.

Do not relaunch or resume under the same run ID unless the protocol contains an exact restart segment with a new segment ID, monotonic discontinuity rule, state reset, and separate checkpoint range. Otherwise recovery means observation after safe stop, not continuation.

## Phase 9: Finalize against a frozen evidence set

**P1 Clause SOAK-CL-010B — Frozen-set finalization and version and existence conflict check drift rejection.**

`finalize` consumes the exact run manifest and `cgs-soak-finalize-manifest/v1`. The finalize manifest pins:

- finalization ID and intended absent result paths;
- run/protocol/candidate/build/profile/environment identities and revisions;
- ordered receipt IDs, paths, and declared revisions;
- canonical receipt-set revision and sample-set revision;
- explicit termination reason and end timestamp;
- expected checkpoint disposition for every Checkpoint ID;
- named gate-policy path/revision and required dimensions;
- output schema and canonicalization version.

Allowed termination reasons are `SCHEDULE_COMPLETED`, `CRASH`, `HANG`, `HEARTBEAT_TIMEOUT`, `OOM_RISK`, `THERMAL_SAFETY`, `DATA_CORRUPTION`, `RESOURCE_SAFETY`, `OBSERVER_STOP`, `EVIDENCE_FAILURE`, or `OTHER` with a non-empty bounded reason.

Re-read and revalidate the protocol, run manifest, candidate, build receipt, all authorities, every evidence member, and the exact frozen receipt set. Reject missing or extra receipts, changed bytes, duplicate Sample IDs, conflicting rows, a new receipt during finalization, samples after an unexplained monotonic reset, or existing result destinations.

Every expected checkpoint receives exactly one disposition: `COLLECTED`, `NOT_COLLECTED`, `PARTIAL`, `INVALID`, or `UNKNOWN`. Never omit a checkpoint or count an absent one as zero.

Derive:
- `Execution Status: EXECUTED` only for `SCHEDULE_COMPLETED` with every required checkpoint valid and all execution-control evidence complete;
- `Execution Status: FAILED_EARLY` for a verified objective product or safety trigger with all pre-stop evidence preserved;
- `Execution Status: PARTIAL` when some valid samples exist but schedule, cleanup, recovery, parsing, or evidence is incomplete;
- `Execution Status: UNKNOWN` when no trustworthy execution identity or sample set exists.

Derive `Evidence Status` separately as `VERIFIED`, `PARTIAL`, `UNKNOWN`, or `INVALID`.

## Phase 10: Calculate unit-safe dimension results and stability verdict

For each in-scope metric, compare only verified canonical-unit samples against its exact matching threshold and baseline. Respect warm-up exclusions, transition/GC policy, minimum valid sample count, aggregation, noise tolerance, and uncertainty/confidence requirements.

Metric result values are `PASS`, `FAIL`, `INCONCLUSIVE`, and `NOT_IN_SCOPE`:
- verified threshold breach is FAIL;
- all required comparisons conclusively within policy are PASS;
- missing/invalid threshold, incompatible unit, insufficient samples, missing checkpoint, low confidence, partial evidence, or unknown cleanup/recovery is INCONCLUSIVE;
- an excluded dimension is NOT_IN_SCOPE.

Derive these independent dimension fields:

**P1 Clause SOAK-CL-009 — Independent objective and experience dimensions.**
- `Stability Result`;
- `Memory Result`;
- `Performance Result`;
- `Experience Result`;
- `Recovery Result`.

A verified crash, hang, data corruption, or mandatory safety trigger makes Stability FAIL even when later checkpoints are not collected. A resource trend is not automatically a leak. Subjective fatigue cannot rewrite an objective dimension, and technical success cannot rewrite Experience.

Apply the named gate policy:
- `Readiness Result: FAIL` when a required dimension conclusively fails;
- `Readiness Result: INCONCLUSIVE` when a required dimension is inconclusive, execution is PARTIAL/UNKNOWN, or evidence is not VERIFIED;
- `Readiness Result: PASS` only when execution is EXECUTED and every required dimension passes or is validly excluded by the policy.

Keep `Workflow Verdict`, artifact finalization, `Readiness Result`, and `Handoff Eligible` separate.

## Phase 11: version and existence conflict check-publish the immutable result and handoff receipt

Render `cgs-soak-result/v2`, a human-readable report, and `cgs-soak-completion-receipt/v2`. The result includes:

- all authority paths/revisions and exact build/target/profile/environment identity;
- full expected-versus-observed checkpoint ledger;
- every metric/unit/conversion/baseline/threshold calculation;
- stop, timeout, cleanup, recovery, and missing-sample classifications;
- execution and evidence statuses;
- Stability, Memory, Performance, Experience, Recovery, and Readiness results;
- limitations, incidents, and exact retest requirements;
- the frozen receipt/sample-set revisions and named gate-policy revision.

Preview paths, byte counts, revision values, and result axes. Then:

1. require all three final paths absent;
2. revalidate every frozen authority and evidence member;
3. confirm the receipt set and checkpoint ledger are unchanged;
4. render in private same-filesystem staging;
5. validate schemas, internal references, and member revisions;
6. compare-and-swap the absent destinations and unchanged inputs;
7. atomically publish all three members without overwrite;
8. read back every member and revalidate its revision.

On drift, collision, partial publication, or read-back mismatch, write no final result, return `Persistence Status: CONFLICT` or `FAILED`, `Workflow Verdict: ERROR`, and handoff NO. A retry uses a new finalization identity and, if any run identity changed, a new run ID.

After verified publication return:
- `Artifact Status: FINALIZED`;
- `Workflow Verdict: RESULT_FINALIZED`;
- exact result and completion-receipt paths/revisions;
- Execution, Evidence, Stability, Memory, Performance, Experience, Recovery, and Readiness fields;
- `Persistence Status: VERIFIED`.

`Handoff Eligible: YES` only when the immutable result and completion receipt verify, `Evidence Status: VERIFIED`, every required result is conclusive, and the exact candidate/build/profile/environment/gate-policy binding is intact. Verified negative evidence such as Stability FAIL may be handed off as a failure result; handoff eligibility never means Readiness PASS.

Every other condition, including PARTIAL, UNKNOWN, INCONCLUSIVE, missing cleanup/recovery proof, unpersisted bytes, or a protocol/run manifest alone, has handoff NO.

## Phase 12: Status, retest, and downstream verification

`status` is read-only. revalidate the exact run manifest and canonical members and return `REGISTERED`, `RUNNING`, `FINALIZED`, `STALE`, `PARTIAL`, or `ERROR`. Never repair evidence during status.

For a verified incident, return a bug-report candidate containing exact run, checkpoint, sample, receipt, build, target, profile, environment, and evidence revisions. Do not create or triage the bug automatically.

After a fix, rerun the same target/profile/environment/metric policy/duration under a new protocol and run ID. Pin the predecessor result path/revision and the fixed candidate/build identities. Only a matching targeted endurance rerun can verify the endurance regression. A smoke result may be a short precondition health check, but it cannot close a memory, performance, endurance, recovery, or fatigue regression.

**P1 Clause SOAK-CL-011 — Matching endurance rerun, never smoke substitution.**
The preceding retest rule is the normative closure clause for audit item SOAK-011.

A downstream consumer receives the exact completion-receipt path/revision, result path/revision, candidate ID, build ID, artifact revision, profile/environment revisions, and gate-policy revision. It must revalidate every referenced member and validate `cgs-soak-result/v2`, `cgs-soak-completion-receipt/v2`, `Persistence Status: VERIFIED`, and the exact result axes. It must not select a newest file, accept a summary, or treat `Handoff Eligible: YES` as Readiness PASS.

## Required invariants

- Exact candidate, build, protocol, run, receipt, and finalize manifests define identity.
- The configured engine and exact verified adapter are the only measurement route.
- Checkpoint IDs and scheduled times are fully expanded before execution.
- Every resource value carries a canonical unit, conversion provenance, and matching budget or baseline.
- Timeout, cleanup, recovery, partial, invalid, and unknown states remain explicit.
- Existing receipts and results are immutable; publication uses absent-target version and existence conflict check.
- Objective and subjective dimensions never overwrite one another.
- A finalized artifact is not automatically a passing stability or readiness result.
- Only exact persisted, verified, conclusive evidence is handoff eligible.
- Endurance regressions require a matching endurance rerun, not a smoke substitution.

## P1 remediation trace

This trace is structural evidence only and changes no workflow behavior. Every P1
audit ID maps to concrete clause, case, and assertion IDs; no prose range is a
traceability substitute.

```yaml
schema: cgs-p1-remediation-trace/v1
entries:
  - audit_id: SOAK-004
    skill_clause_ids: [SOAK-CL-004]
    spec_case_ids: [SOAK-C01]
    assertion_ids: [SOAK-STA-002, SOAK-STA-003, SOAK-STA-004, SOAK-STA-005, SOAK-PRO-001, SOAK-PRO-002]
  - audit_id: SOAK-005
    skill_clause_ids: [SOAK-CL-005]
    spec_case_ids: [SOAK-C02, SOAK-C11]
    assertion_ids: [SOAK-STA-008, SOAK-STA-019, SOAK-STA-020, SOAK-PRO-005, SOAK-PRO-006]
  - audit_id: SOAK-006
    skill_clause_ids: [SOAK-CL-006]
    spec_case_ids: [SOAK-C03]
    assertion_ids: [SOAK-STA-009, SOAK-PRO-007]
  - audit_id: SOAK-007
    skill_clause_ids: [SOAK-CL-007]
    spec_case_ids: [SOAK-C04]
    assertion_ids: [SOAK-STA-010, SOAK-PRO-003]
  - audit_id: SOAK-008
    skill_clause_ids: [SOAK-CL-008]
    spec_case_ids: [SOAK-C05]
    assertion_ids: [SOAK-STA-011, SOAK-PRO-001, SOAK-PRO-002]
  - audit_id: SOAK-009
    skill_clause_ids: [SOAK-CL-009]
    spec_case_ids: [SOAK-C06]
    assertion_ids: [SOAK-STA-012, SOAK-PRO-008, SOAK-PRO-013]
  - audit_id: SOAK-010
    skill_clause_ids: [SOAK-CL-010A, SOAK-CL-010B]
    spec_case_ids: [SOAK-C07, SOAK-C13]
    assertion_ids: [SOAK-STA-013, SOAK-STA-014, SOAK-STA-021, SOAK-STA-022, SOAK-PRO-007, SOAK-PRO-009, SOAK-PRO-010]
  - audit_id: SOAK-011
    skill_clause_ids: [SOAK-CL-011]
    spec_case_ids: [SOAK-C08]
    assertion_ids: [SOAK-STA-015, SOAK-PRO-012]
  - audit_id: SOAK-012
    skill_clause_ids: [SOAK-CL-012]
    spec_case_ids: [SOAK-C09]
    assertion_ids: [SOAK-STA-006, SOAK-STA-007]
```
