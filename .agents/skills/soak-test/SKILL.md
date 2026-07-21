---
name: soak-test
description: "Plans build-bound endurance tests, ingests immutable checkpoint evidence, and finalizes reproducible soak results without confusing an empty protocol with an executed test."
---

# Soak Test

Use one explicit mode:

- `$soak-test plan <target-id> --protocol-id <id> --build <version> --build-hash <hash> --commit <commit> --duration <duration> --interval <duration> --focus <memory|stability|performance|experience|all> --profile <workload-profile-id> --environment <environment-profile-id> [--save-protocol] [--supersedes <protocol-id>]`
- `$soak-test start <protocol-id> --run-id <run-id> --observer <observer-id> --started-at <ISO-8601>`
- `$soak-test ingest <run-id> <path-to-evidence> --receipt-id <receipt-id>`
- `$soak-test finalize <run-id> --ended-at <ISO-8601> --termination <reason>`
- `$soak-test status <run-id>`

The human or an external harness performs the long-running test. This workflow plans
it, preserves supplied evidence, and derives a result. It never simulates missing
samples or claims that writing a protocol executed the test.

An explicit bounded request authorizes its in-scope writes. Otherwise, before the
first file change, show one complete changeset with every intended path and change
and obtain one approval. Do not re-prompt within that boundary. Stop for new approval
only when scope expands materially.

## Artifact and status contract

Use only this canonical layout:

~~~text
production/qa/soak-tests/
  _protocols/<protocol-id>.md
  <run-id>/
    manifest.md
    receipts/<receipt-id>.md
    raw/<receipt-id>.<source-extension>
    samples/<receipt-id>.md
    result.md
~~~

Each layer has one meaning:

- protocol: immutable execution plan; `Artifact Type: soak-test-protocol`,
  `Status: PLANNED`, `Gate Eligible: NO`, `Verdict: PROTOCOL_PLANNED`;
- run manifest: immutable run identity created before evidence ingest;
  `Artifact Type: soak-run-manifest`, `Status: RUNNING`, `Gate Eligible: NO`;
- raw receipt and sample ledger: immutable evidence copied and indexed without
  changing tester values; never a result;
- completed result: only `<run-id>/result.md` with
  `Artifact Type: soak-test-result` and `Status: COMPLETED`.

A protocol, manifest, receipt, sample ledger, legacy soak file, blank template, or
partially filled table is not an execution result. It must never use `Status:
COMPLETED`, `Execution Status: EXECUTED`, `Verdict: COMPLETE`, or `Gate Eligible:
YES`.

Only a result that passes Phase 6 finalization may return `Verdict: COMPLETE`.
`COMPLETE` means the result artifact was finalized and verified; it is independent
from technical or experience readiness.

Never overwrite any canonical artifact. A changed build, workload, environment,
protocol, evidence set, or retry uses a new protocol/run/receipt ID.

## Result fields

Keep these fields independent:

| Field | Allowed values |
|---|---|
| `Status` | `COMPLETED` only on a finalized result |
| `Execution Status` | `EXECUTED`, `FAILED_EARLY`, `INCOMPLETE` |
| `Stability Result` | `PASS`, `FAIL`, `INCONCLUSIVE`, `NOT_IN_SCOPE` |
| `Memory Result` | `PASS`, `FAIL`, `INCONCLUSIVE`, `NOT_IN_SCOPE` |
| `Performance Result` | `PASS`, `FAIL`, `INCONCLUSIVE`, `NOT_IN_SCOPE` |
| `Experience Result` | `PASS`, `FAIL`, `INCONCLUSIVE`, `NOT_IN_SCOPE` |
| `Readiness Result` | `PASS`, `FAIL`, `INCONCLUSIVE` |
| `Gate Eligible` | `YES` or `NO`; only a finalized, conclusive execution or verified early objective failure may be `YES` |
| `Verdict` | `COMPLETE`, `ERROR`, `BLOCKED`, or a mode-specific non-completion verdict |

An experience/fatigue observation cannot turn an objective stability, memory, or
performance result into PASS or FAIL. Likewise, technical PASS cannot erase
experience concerns. A consumer may combine dimensions only through an explicit,
named gate policy.

## Phase 0: Validate mode, IDs, and paths

Accept exactly one mode and its documented arguments. Reject unknown/missing modes,
unknown options, duplicate options with different values, extra positionals, unsafe
IDs, and invalid durations before writing anything.

IDs must match:

- protocol ID: `SOAK-PROTO-<slug-or-version>`;
- run ID: `SOAK-RUN-<slug-or-uuid>`;
- receipt ID: `SOAK-REC-<slug-or-uuid>`;
- target, workload-profile, and environment-profile IDs:
  lowercase/uppercase letters, digits, hyphens, and underscores only.

Reject path separators, dot segments, timestamp-only IDs, existing-path collisions,
symlink escapes, missing files, directories used as evidence, unsupported file types,
and evidence larger than 100 MiB. Resolve literal real paths inside the project root.
Accept UTF-8 `.md`, `.txt`, `.csv`, `.json`, or `.jsonl` evidence.

On validation failure, return `Verdict: ERROR` or `BLOCKED` with the exact failed
field/path. Write nothing and never emit completion or readiness.

## Phase 1: Validate protocol identity

`plan` requires all of the following before an executable protocol can be produced:

- stable target ID plus exact system, scene/service, and target artifact;
- build version, build hash, and source commit;
- configured engine and version when an engine is involved;
- workload profile ID and content: ordered action/loop step IDs, repetitions or rate,
  player/bot count, network conditions when relevant, save/state setup, deterministic
  seed or explicit `NONDETERMINISTIC` rationale, and reset/transition rules;
- environment profile ID and content: platform, device/hardware, OS, graphics and
  quality settings, power/thermal mode, input, locale, accessibility configuration,
  network topology, and relevant background services;
- requested duration, sampling interval, focus dimensions, observer role, and
  collection-tool/adapter identity with version;
- success criteria or acceptance-criterion IDs under test.

Missing target, build, workload, environment, or observer/collection identity is
`BLOCKED`; do not generate a fillable “executable” protocol with placeholders.

Read context only through explicit IDs and current hashes. Do not read “the most
recent” playtest, QA plan, protocol, or run. If the plan names a playtest session as
experience evidence, accept only the staged canonical playtest contract:

`production/playtests/<session-id>/report.md`

It must contain `Artifact Type: playtest-session-result`, `Status: COMPLETED`, and
`Gate Eligible: YES`, and its manifest, observation-ledger, raw-evidence, and report
hashes must verify. Treat the playtest report as derived context; it never replaces
soak raw samples, run identity, or observer evidence.

## Phase 2: Bind budgets, baselines, and measurement policy

For every required metric, record:

- stable metric ID, dimension, unit, and target/environment scope;
- measurement method, collection tool/adapter, tool version, and source field;
- warm-up duration and excluded warm-up samples;
- checkpoint timing, scene/level transition policy, GC policy, sampling frequency,
  and aggregation method;
- project budget or approved baseline artifact path, revision, and raw SHA-256;
- comparison operator and threshold;
- allowed measurement noise or fluctuation;
- minimum valid samples and confidence/uncertainty method;
- early-stop trigger and safe shutdown/evidence-preservation action.

Use only project budgets or an explicitly approved, matching baseline. Do not invent
or transplant engine-, platform-, or tool-wide thresholds.

A missing, stale, mismatched, or unapproved threshold does not become a default. Mark
that metric `THRESHOLD_UNAVAILABLE`; the protocol may still be saved as `PLANNED`,
but `Threshold Readiness: INCOMPLETE` and `Gate Capable: NO`. Any completed run for
that metric is `INCONCLUSIVE`, never PASS.

Load engine measurement guidance only for the configured engine and exact supported
version. Record adapter path/hash/version. If required guidance is unavailable or the
engine version is unverified, return `NEEDS_CONFIRMATION` and do not call the
protocol executable or gate capable. Do not include instructions for unselected
engines.

## Phase 3: Generate an immutable protocol

Expand the entire checkpoint schedule; never leave a “repeat this section”
placeholder. Generate unique IDs such as `CP-000`, `CP-001`, and so on from T+0
through the requested duration at the exact interval, including the final duration.
If duration is not evenly divisible, include the final partial interval and explain
it.

Each checkpoint definition includes planned offset, workload step/repetition range,
required metric IDs, environment/thermal snapshot, expected collection source,
observer prompt, and evidence-preservation action. It has no observed value.

The protocol includes:

1. artifact header and complete target/build/workload/environment identity;
2. acceptance criteria and focus dimensions;
3. warm-up and reset/transition procedure;
4. exact checkpoint table and required sample schema;
5. metric budgets/baselines and provenance;
6. safety/early-termination triggers;
7. evidence collection and receipt instructions;
8. missing-sample semantics (`NOT_COLLECTED`, never zero);
9. dimension and readiness classification rules;
10. retest identity requirements.

Do not include filled result values, a leak judgment, test PASS/FAIL fields, completed
QA sign-off, post-session conclusions, or `Verdict: COMPLETE`.

Without `--save-protocol`, present the candidate protocol and return
`Verdict: PROTOCOL_DRAFTED`, `Status: PLANNED`, `Gate Eligible: NO`, and no path.
With `--save-protocol`, write only
`production/qa/soak-tests/_protocols/<protocol-id>.md` after authorization and
re-read/hash verification. Return:

- `Artifact Type: soak-test-protocol`
- `Status: PLANNED`
- `Execution Status: NOT_STARTED`
- `Gate Eligible: NO`
- `Verdict: PROTOCOL_PLANNED`
- protocol path and SHA-256

Protocol history is selected by exact target/profile/build IDs, never timestamps.
`--supersedes <protocol-id>` creates a new protocol ID/version and records the
predecessor path/hash; it never edits or extends the old file.

## Phase 4: Start one build-bound run

`start` reads the exact protocol ID and verifies its bytes, identity, status, and
hash. Reject a protocol with placeholders, mismatched target/build/profile,
`Threshold Readiness: INCOMPLETE` when the caller requires gate-capable evidence, or
an existing run path.

Create only `production/qa/soak-tests/<run-id>/manifest.md` with:

- `Artifact Type: soak-run-manifest`, schema version, run ID, `Status: RUNNING`,
  `Gate Eligible: NO`;
- protocol ID/path/raw SHA-256;
- target/build/source commit, workload profile/hash, environment profile/hash,
  configured engine/version, duration/interval/focus, checkpoint IDs, metric IDs,
  adapter IDs/hashes, and threshold/baseline source hashes;
- observer ID, actual start timestamp, evidence retention classification, and intended
  result path.

Write after bounded authorization, then re-read and hash it. Return
`Verdict: RUN_STARTED`; never return `EXECUTED`, `COMPLETE`, or a dimension result.

## Phase 5: Ingest immutable evidence receipts

`ingest` verifies the run manifest, evidence path, receipt ID, and absence of
collisions. Read source bytes once and compute raw SHA-256 before interpretation.

Create exactly three immutable files in one all-or-none changeset:

1. `raw/<receipt-id>.<source-extension>` copied byte-for-byte;
2. `samples/<receipt-id>.md`, an observation ledger preserving supplied values;
3. `receipts/<receipt-id>.md`, a receipt binding the other two files and hashes.

Every sample row requires:

- stable sample ID and expected checkpoint ID;
- actual ISO-8601 timestamp and elapsed monotonic time;
- observer ID and raw receipt/source location;
- workload step/repetition, seed, and relevant state;
- platform/device/configuration plus thermal/power state;
- metric ID, observed numeric/text value, unit, collection method, and tool version;
- event/incident ID when applicable;
- raw evidence SHA-256.

Preserve values and observer language. Do not interpolate, smooth, replace, or classify
them in the ledger. A missing expected checkpoint is recorded only during
finalization as `NOT_COLLECTED`; never create a zero-valued sample.

Preview the three-file changeset, verify internal references/hashes, and publish all
or none. Existing receipt paths are immutable. Return `Verdict: EVIDENCE_INGESTED`,
`Status: RUNNING`, receipt/raw/ledger hashes, and `Gate Eligible: NO`.

## Phase 6: Finalize one canonical completed result

`finalize` reads only the requested run's canonical manifest, protocol, receipts, raw
files, and sample ledgers. Recompute every hash and reject missing artifacts,
changed bytes, unresolved references, duplicate sample IDs, samples for another
run/build/profile, or an existing result path.

Finalization requires:

- unique protocol/run IDs and schema version;
- exact target, build version/hash, source commit, workload/profile hash, environment
  profile/hash, platform/device/configuration, engine/adapter version when applicable;
- observer ID, valid start/end timestamps, and end later than start;
- explicit termination reason;
- at least one immutable raw receipt and matching sample ledger;
- baseline sample when required by a metric;
- every expected checkpoint classified as collected or `NOT_COLLECTED`;
- each incident tied to raw evidence/source location;
- all budgets/baselines and threshold states preserved;
- manifest, protocol, receipt, raw-set, and sample-set SHA-256 values.

Allowed termination reasons are `SCHEDULE_COMPLETED`, `CRASH`, `HANG`, `OOM_RISK`,
`THERMAL_SAFETY`, `DATA_CORRUPTION`, `OBSERVER_STOP`, `EVIDENCE_FAILURE`, or
`OTHER:<non-empty-reason>`.

Derive `Execution Status`:

- `EXECUTED` only when termination is `SCHEDULE_COMPLETED`, every required checkpoint
  and baseline sample exists, observer identity is valid, and all hashes/references
  verify;
- `FAILED_EARLY` when a verified crash, hang, OOM risk, data-corruption, or applicable
  threshold/safety trigger ended the run and all evidence collected before termination
  is preserved;
- `INCOMPLETE` for missing checkpoints without a verified product/safety failure,
  observer stop, evidence failure, or otherwise incomplete execution.

Do not discard early samples. List every uncollected checkpoint as `NOT_COLLECTED`
with the termination reason; never count it as zero or PASS.

### Dimension results

For each in-scope dimension, evaluate only matching verified samples against the
protocol's sourced threshold policy:

- missing/unapproved/stale threshold, insufficient valid samples, low confidence,
  missing checkpoint, or incompatible unit/profile: `INCONCLUSIVE`;
- verified threshold breach: `FAIL`;
- all required comparisons passing with required sample count/confidence: `PASS`;
- excluded focus: `NOT_IN_SCOPE`.

A verified crash/hang/data-loss event makes `Stability Result: FAIL` even if later
checkpoints are absent. Do not diagnose a memory leak from monotonic growth alone.
Linear extrapolation or time-to-OOM is prohibited unless the approved protocol
defines the model, minimum sample count, fit quality, confidence interval, and
validity range.

Compute `Readiness Result` from the named gate policy:

- `FAIL` when any required objective dimension fails;
- `INCONCLUSIVE` when any required objective dimension is inconclusive or execution is
  incomplete;
- `PASS` only when every required objective dimension passes and execution is
  `EXECUTED`.

Experience is reported independently. It affects readiness only when the named
consumer policy explicitly requires `Experience Result`; it never rewrites technical
dimensions.

### Gate eligibility

Set `Gate Eligible: YES` only when all provenance/finalization checks pass and either:

- execution is `EXECUTED`, every required gate-policy dimension is conclusive, and all
  required threshold policies are available; or
- execution is `FAILED_EARLY` because a verified objective product/safety failure
  occurred, so the artifact is valid negative evidence.

Set `Gate Eligible: NO` for `INCOMPLETE`, any unresolved provenance or threshold gap,
any required inconclusive dimension, or evidence that cannot support the named gate
policy. Gate eligibility never converts a failed or inconclusive result into PASS.

### Canonical result header

The result must start with these machine-readable fields:

~~~text
Artifact Type: soak-test-result
Schema Version: 1
Run ID: <run-id>
Protocol ID: <protocol-id>
Status: COMPLETED
Gate Eligible: <YES|NO>
Execution Status: <EXECUTED|FAILED_EARLY|INCOMPLETE>
Readiness Result: <PASS|FAIL|INCONCLUSIVE>
Stability Result: <PASS|FAIL|INCONCLUSIVE|NOT_IN_SCOPE>
Memory Result: <PASS|FAIL|INCONCLUSIVE|NOT_IN_SCOPE>
Performance Result: <PASS|FAIL|INCONCLUSIVE|NOT_IN_SCOPE>
Experience Result: <PASS|FAIL|INCONCLUSIVE|NOT_IN_SCOPE>
Target ID: <target-id>
Build Version: <version>
Build Hash: <hash>
Source Commit: <commit>
Workload Profile ID: <id>
Workload Profile SHA-256: <hash>
Environment Profile ID: <id>
Environment Profile SHA-256: <hash>
Platform Configuration: <platform/device/config>
Observer ID: <observer-id>
Started At: <ISO-8601>
Ended At: <ISO-8601>
Termination Reason: <reason>
Evidence Receipt IDs: <ordered-ids>
Protocol SHA-256: <hash>
Manifest SHA-256: <hash>
Raw Evidence Set SHA-256: <hash>
Sample Ledger Set SHA-256: <hash>
~~~

The body includes provenance, target/build/environment/workload, expected-versus-
collected checkpoints, raw sample traceability, early termination, metric
calculations, threshold sources, confidence/limitations, the four dimension results,
readiness policy/result, incidents, experience evidence, and retest requirements.

Preview the exact result changeset, write only `<run-id>/result.md`, re-read it, verify
the header/internal references, and compute its SHA-256. Only then return:

- `Status: COMPLETED`
- `Verdict: COMPLETE`
- `Gate Eligible: <YES|NO>` derived by the rule above
- `Canonical Result: production/qa/soak-tests/<run-id>/result.md`
- completion receipt with protocol, manifest, receipt, raw-set, sample-set, and result
  hashes
- execution, readiness, and all dimension results

A completed failing, early-failed, incomplete, or inconclusive result remains honest:
`Verdict: COMPLETE` confirms artifact finalization only and cannot be presented as
PASS. A malformed or provenance-incomplete run returns `ERROR` and writes no result.

## Phase 7: Status and downstream routing

`status <run-id>` is read-only. Validate the canonical paths and hashes and return one
of `RUNNING`, `COMPLETED`, `STALE`, `PARTIAL`, or `ERROR`. A legacy protocol/result
does not count. Do not mutate artifacts.

For each verified incident, return a bug-report candidate containing run ID, sample
IDs, receipt IDs, build/environment identity, severity evidence, and fingerprint.
Do not create or triage a bug automatically.

After a fix:

- a smoke check may be used only as a short precondition check;
- it cannot close, replace, or pass a memory, performance, endurance, or fatigue
  regression;
- rerun the same target, workload, environment, thresholds, and duration under a new
  protocol/run ID, with an explicit predecessor result path/hash;
- compare only hash-valid matching profiles.

Do not invoke downstream workflows automatically. Never claim a release gate consumed
the result unless that consumer independently validates the canonical result path,
`Status: COMPLETED`, all receipt/hashes, build/profile identity, execution status,
dimension results, and readiness policy.
