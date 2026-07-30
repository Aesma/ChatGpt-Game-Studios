# Dev Story Implementation Transaction v2

Treat revisions as supplied metadata; never calculate them from file content. Use stable business IDs, canonical paths, schema versions, explicit revisions, and UTC run IDs.

This file is the normative private contract for `$dev-story`. The skill and this
reference fail closed if their rules conflict. Terms `MUST`, `MUST NOT`, `SHOULD`,
and `MAY` are normative.

## 1. Canonical serialization and validation

- Validate declared identity, schema, version, and revision before use. and render `<explicit-revision>`.
- Canonical structured payloads use UTF-8, LF, Unicode NFC, lexicographically
  sorted map keys, array order as declared, no insignificant whitespace, and no
  timestamp/host/path inference.
- Validate a set as revision over ordered length-delimited records
  `byte_length ":" raw_bytes`. A set contract MUST name its sort key.
- `ABSENT` is a precondition token, not a revision. It requires no filesystem entry
  at the canonical path immediately before create.
- A declared revision mismatch is a conflict even when parsed semantics look equal.

## 2. Fixed limits

The request MUST not exceed:

```yaml
max_request_bytes: 262144
max_sources: 256
max_targets: 128
max_total_source_bytes: 67108864
max_total_candidate_bytes: 67108864
max_acceptance_criteria: 128
max_tests: 128
max_dependencies: 128
max_engine_findings: 64
max_single_log_bytes: 16777216
max_total_log_bytes: 67108864
```

Exceeding a limit is `INPUT_ERROR` before planning or `BLOCKED` before mutation,
depending on when the bounded value becomes knowable. Never truncate, sample, or
describe a partial set as complete.

## 3. Request schema

`cgs.dev-story-request/v2` contains exactly:

```yaml
schema: cgs.dev-story-request/v2
request_id: DSR-<20-lower-hex>
project_root:
  canonical_path: <absolute-path-used-for-boundary-check-only>
  identity: <repository/worktree identity>
story:
  id: STORY-<16-lower-hex>
  path: <project-relative-path>
  expected_revision: <explicit-revision>
  schema: cgs.story/v2
admission_mode: CURRENT_READY | STRUCTURED_ACCEPTED_RISK
readiness:
  registry_path: <project-relative-path>
  registry_expected_revision: <explicit-revision>
  record_id: <stable-record-id>
  record_expected_revision: <explicit-revision>
  candidate_expected_revision: <explicit-revision>
  readiness_key: <stable-key>
  recorder_receipt_path: <project-relative-path>
  recorder_receipt_expected_revision: <explicit-revision>
sprint:
  id: <stable-id>
  plan_file: <project-relative-path>
  plan_revision: <explicit-revision>
  tracker:
    path: production/sprint-status.yaml
    raw_revision: <explicit-revision>
    schema_version: cgs.sprint-tracker/v2
    tracker_revision: <positive-integer>
    event_id: <stable-current-event-id>
    active_sprint_id: <same-as-sprint.id>
    sprint_state: ACTIVE
    lifecycle_owner: <exact-status-recorder-identity>
    lifecycle_recorder: cgs.sprint-tracker/v2
    plan_file: <same-as-sprint.plan_file>
    plan_revision: <same-exact-raw-plan-revision>
    plan_revision: <explicit-revision>
    story_set_revision: <explicit-revision>
    story_row_id: <stable-row-id>
source_manifest:
  path: <project-relative-path>
  expected_revision: <explicit-revision>
  schema: cgs.dev-story-source-manifest/v2
roles:
  implementation_owner: <stable-role-and-task-identity>
  status_recorder: <stable-role-and-task-identity>
  engine_reviewer: <stable-role-and-task-identity | NONE>
checkpoint:
  path: <project-relative-create-only-path>
  expected_state: ABSENT
resume:
  checkpoint_path: <project-relative-path | NONE>
  checkpoint_expected_revision: <explicit-revision> | NONE
limits: <exact values from section 2 or stricter>
generated_at: <RFC-3339-UTC>
```

`request_id` is derived from the canonical request excluding `request_id` and
`generated_at`. The source manifest lists the complete ordered source and proposed
target universe; it cannot use directories, globs, discovery rules, or optional
“related files.” The request MUST name three distinct role identities unless the
engine reviewer is `NONE`.

The checkpoint path MUST be unique to request/story/attempt, under an existing
project-owned recovery root, and `ABSENT`. A fixed overwriteable “latest”
checkpoint is invalid.

## 4. Source manifest

`cgs.dev-story-source-manifest/v2` contains ordered rows with:

```text
kind / stable_id / canonical_path / expected_raw_revision / schema_or_format /
required_fields_or_sections / authority / required
```

It MUST include the story; readiness registry/record/receipt; sprint plan/tracker;
systems index; Approved GDD; TR registry and exact entries; every governing ADR;
control manifest; dependency stories; declared asset/test/QA sources; technical
preferences; engine-version reference; review-mode/reviewer evidence used by the
READY record; workflow contracts; every existing target; and every resume
checkpoint when applicable.

A proposed new target appears as `kind: target` with `expected_raw_revision:
ABSENT`. Missing required source, duplicate path/ID, alias, unexpected source,
unknown schema, or inconsistent authority is invalid.

## 5. Readiness record consumption and structured risk

For `CURRENT_READY`, a persisted record is eligible only when all of these
independently pass:

1. Record schema and canonical revision are valid;
2. final verdict is `READY` and evaluation state is `COMPLETE`;
3. registry identity/revision/head and declared revision match the recorder receipt;
4. recorder result is `RECORDED` or `ALREADY_RECORDED`;
5. record/candidate/readiness/stale keys match across registry and receipt;
6. `implementation_gate_eligible` is true under the recorder contract;
7. story ID/path/declared revision match the request and current bytes;
8. every `expires_when`/stale-key predicate is present and currently false; and
9. checker, ruleset, review-mode, reviewer, and source schemas are supported.

For `STRUCTURED_ACCEPTED_RISK`, require a persisted, complete `NEEDS_WORK` record
and valid recorder receipt for the exact current story. The record may contain
non-passing checks only for exact control-manifest staleness and/or incomplete
dependencies explicitly declared `soft`. Every other applicable check is PASS;
there is no BLOCKED/UNVERIFIED result or unknown evidence. The recorder receipt
does not claim implementation-gate eligibility and this workflow does not upgrade
the verdict. Any missing/invalid authority, hard dependency, architecture gap,
ambiguous AC/Test, or second source mismatch blocks.

A manifest waiver candidate is exactly:

```yaml
schema: cgs.dev-story-manifest-waiver/v1
waiver_id: MW-<stable-id>
kind: manifest-staleness
implemented_against_revision: <explicit-revision>
current_revision: <explicit-revision>
accepted_by: <user-identity>
accepted_at: <RFC-3339-UTC>
provenance_status: ACCEPTED-RISK
```

The story header/source snapshot MUST agree on `implemented_against_revision`; the
current raw manifest MUST equal `current_revision`; and every non-manifest check MUST
pass. Never change captured version/revision/snapshot fields. A new current manifest
revision invalidates the waiver and plan.

A soft-dependency waiver candidate is exactly:

```yaml
schema: cgs.dev-story-dependency-waiver/v1
waiver_id: DW-<stable-id>
dependency_id: <stable-story-id>
dependency_path: <canonical-project-relative-path>
dependency_revision: <explicit-revision> | MISSING
observed_status: <exact-current-status> | MISSING
accepted_by: <user-identity>
accepted_at: <RFC-3339-UTC>
expires_when: <dependency path/revision/status or governing source changes>
reason: <specific-bounded-risk>
```

The dependency MUST be explicitly soft. The waiver MUST match freshly observed
identity/path/revision/state and is invalid after any change. A hard dependency has
no waiver schema or risk branch. New waivers are bound into the approved plan and
final result only; they never mutate the dependency, story author artifact,
readiness registry, or tracker planning fields. Free text is not a waiver.

The workflow records admission consumption in its plan/result. It does not mutate
the readiness registry or story. Later business/source changes MAY make the record
stale; that does not retroactively invalidate a mutation already admitted after
the final pre-write version and existence conflict check. It does prevent reuse or resume unless the resume
contract proves the same admitted transaction rather than claiming a fresh gate.

## 6. Ownership model

Path ownership is closed and disjoint:

| Domain | Sole writer | Examples |
|---|---|---|
| Business | implementation owner | source, engine config, data, schema, assets, tests, raw logs, manual evidence |
| Lifecycle request/verification | status recorder (`lifecycle_owner`) | transition proposal/result and recorder receipt; no direct tracker/story write |
| Lifecycle commit | tracker-declared recorder | only lifecycle-owned fields in `production/sprint-status.yaml` |
| Recovery | status recorder | the one create-only checkpoint |
| Analysis | no writer | engine review packets/results and architecture findings until included as approved evidence targets |

The orchestrator MAY fill the named implementation-owner or recorder role only
when the plan retains one stable identity and disjoint paths. It MUST NOT perform
an unowned inline write. A Config/Data story has no special direct-write branch.

The optional engine reviewer receives immutable bytes or exact revision-bound
locators. It cannot edit, apply a patch, create an asset, run a mutation, share
write ownership, or be the fallback implementation owner in the same plan.

## 7. Plan and authorization

`cgs.dev-story-plan/v2` is canonical and includes:

```yaml
schema: cgs.dev-story-plan/v2
plan_id: DSP-<20-lower-hex>
request_id: <request-id>
workflow_contract: <path/revision set>
readiness_admission: <record/receipt/stale-key validation>
accepted_risk: <NONE or exact waiver candidates and labels>
source_snapshot: <ordered path/status/revision/locator rows>
dependency_results: <ordered current dependency rows>
architecture_coverage: <ordered change-to-ADR rows>
engine_review: <NONE or packet/result/finding-set identities>
targets: <ordered target rows>
tests: <ordered test execution rows>
status_transactions: <IN_PROGRESS and IN_REVIEW derivation contracts>
checkpoint_contract: <path/ABSENT/derivation schema and limits>
rollback_operations: <ordered pre-authorized rows or NONE>
canonical_plan_revision: <explicit-revision>
```

Every target row contains:

```text
path / operation(create|replace|generate) / owner /
expected_preimage(revision|ABSENT) / output_kind(DETERMINISTIC|RUNTIME_DERIVED) /
candidate_revision-or-derivation_contract_revision / candidate_or_output_byte_bounds /
semantic_change / AC_IDs / Test_IDs / source_binding_revision / write_condition /
rollback_classification
```

Sort targets by canonical path after uniqueness checks. Deterministic candidate
bytes are prepared before approval and their revision cannot be `TBD`. Runtime-derived
targets are permitted only for raw test/manual logs, their structured execution
records, the two transition proposals/results/receipts, and the failure
checkpoint. Each binds a
canonical derivation contract, exact inputs/schema/limits, expected approved prior state, and
post-write validation; its final declared revision is recorded only after generation. A
runtime output cannot expand the path set or semantic scope. The plan revision is
computed from the canonical plan excluding its own revision. `plan_id` is the first
20 plan-revision hex characters prefixed `DSP-`.

Authorization records user/task identity, RFC 3339 UTC time, exact `plan_revision`,
ordered target-contract-set revision, owner-set revision, source-snapshot revision, and the
literal decision. It expires on any differing byte, derivation rule, or identity.
Authorization cannot be implicit, inherited from request creation, or broadened
after the fact.

## 8. Architecture findings

An architecture-controlled change without an exact Accepted ADR creates
`cgs.dev-story-finding/v2`:

```yaml
schema: cgs.dev-story-finding/v2
finding_id: DSF-<20-lower-hex>
classification: ARCHITECTURE_BLOCKER
story_id: <stable-id>
change_key: <stable semantic-change key>
observation: <current unsupported decision>
evidence: <ordered exact path/revision/locator rows>
owner: architecture-decision-owner
required_action: <one bounded decision question>
resolution_condition: <Accepted ADR ID/path/revision/locator covering the change>
```

Finding identity revisions schema version, story ID, classification, change key,
normalized observation key, and resolution owner/condition. It excludes prose,
line numbers, timestamps, and source revisions so the same unresolved decision
keeps one identity. A changed observation changes identity. No user risk
acceptance, local sign-off, engine-review opinion, or implementation note resolves
this finding.

## 9. Engine-review packet and result

`cgs.dev-story-engine-review-packet/v1` binds packet ID, story/request/plan-draft
revisions, configured engine/version, planned file types and exact read-only paths,
relevant ADR/control/source revisions, questions, no-write rule, and response schema.

`cgs.dev-story-engine-review-result/v1` binds the packet revision and contains ordered
findings with stable IDs, severity, exact evidence, effect, recommendation, and
`architectural: true|false`. The result states `allowed_write_set: []` and
`write_count: 0`. Missing/malformed/wrong-packet/over-limit output is invalid.
Architectural findings block. A recommendation requiring an unplanned path
invalidates the draft. Other findings return to the implementation owner.

## 10. Lifecycle and recorder contract

Canonical implementation lifecycle values and tracker serialization are:

| Canonical | Exact tracker `stories[].status` |
|---|---|
| `READY_FOR_DEV` | `ready_for_dev` |
| `IN_PROGRESS` | `in_progress` |
| `IN_REVIEW` | `in_review` |
| `COMPLETE` or `DONE` | `done` (read-only to this workflow) |
| `BLOCKED` | `blocked` (read-only to this workflow) |

This workflow may request only `READY_FOR_DEV -> IN_PROGRESS -> IN_REVIEW`.
Unknown spellings, multiple rows, or a story ID/path mismatch are conflicts, not
values to normalize heuristically. `cgs.story/v2` is an immutable author artifact:
raw bytes, `Revision`, author/readiness fields, prior history, and `x-local-*`
extensions MUST remain unchanged.

Consume these exact top-level `cgs.sprint-tracker/v2` fields without aliases:
`tracker_revision`, `event_id`, `sprint_id`, `active_sprint_id`, `sprint_state`,
`lifecycle_owner`, `lifecycle_recorder`, `plan_file`, `plan_revision`,
`plan_revision`, `story_set_revision`, `updated_at`, `goal`, `start_date`, `end_date`,
`timezone`, `estimate_unit`, `capacity`, `qa_plan`, and `stories`. Require equal
sprint IDs, ACTIVE state, a positive revision, the request's status-recorder
identity in `lifecycle_owner`, and exact `lifecycle_recorder:
cgs.sprint-tracker/v2`. The consumer independently revisions exact tracker bytes;
that declared revision is a request/manifest/version and existence conflict check binding and MUST NOT be read from or
written as a tracker field.

The selected plan path and exact raw bytes MUST match tracker `plan_file` and
`plan_revision`. Freeze `plan_revision` and `story_set_revision`; lifecycle transitions
do not own or revalidate them. Validate typed capacity, its receipt/declared revision and
integer operands, and the complete current story row including status timestamp
and provenance. Any missing/renamed field, invalid type, duplicate row, aggregate-
only substitution, or mismatch is `BLOCKED` before mutation.

Each transition starts with a canonical proposal containing:

```yaml
schema: cgs.dev-story-status-transition-proposal/v2
status_transaction_id: DST-<uuid-or-128-bit-random-id>
tracker_path: production/sprint-status.yaml
expected_tracker_revision: <explicit-revision>
expected_tracker_revision: <positive-integer>
expected_plan_revision: <explicit-revision>
expected_story_set_revision: <explicit-revision>
requested_field_owners:
  - stories[<story-id>].status
  - stories[<story-id>].status_updated_at
  - stories[<story-id>].status_update_provenance
event_id: dev-story/<story-id>/<status_transaction_id>
story_id: <stable-id>
story_path: <canonical-path>
story_revision: <explicit-revision>
from_status: ready_for_dev | in_progress
to_status: in_progress | in_review
provenance: <plan/readiness/result-set/owner bindings>
```

The proposal preserves tracker `plan_file`, `plan_revision`, `plan_revision`,
`story_set_revision`, sprint identity, capacity, QA-plan, all unowned story fields,
and every other row. `IN_PROGRESS` derives from the approved plan, current tracker
approved prior state, immutable story/readiness admission, transaction ID, and one timestamp.
`IN_REVIEW` additionally binds verified actual target revisions and canonical
execution records.

Invoke only the tracker-declared lifecycle recorder. Do not replace tracker bytes
directly. A valid `cgs.dev-story-status-transaction/v2` result/receipt binds the
proposal revision, lifecycle owner/recorder identities, exact tracker pre/post raw
revisions and byte counts, prior/new revisions, event/transaction IDs, requested
field-owner set, observed row transition/provenance, version and existence conflict check outcome `COMMITTED`,
read-back `VERIFIED`, immutable story revision, unchanged planning tuple, and complete
unowned-field comparison. Independently reread the tracker and reproduce every
receipt assertion before reporting `TRANSACTION_VERIFIED`.

A rejected recorder request with unchanged tracker bytes is zero-write BLOCKED or
FAILED as classified. Changed tracker bytes without a fully valid receipt,
revision/event mismatch, unowned-field change, or unknown/partial recorder result
is `PARTIAL_PUBLICATION`; stop other writers and attempt only the authorized
create-only checkpoint. Never synthesize a receipt, retry with last-writer-wins,
or claim rollback unless a pre-authorized restoration reproduces the exact raw
tracker approved prior state.

## 11. Test execution and evidence

Each plan test row contains:

```yaml
test_id: TEST-<stable-id>
ac_ids: [AC-<stable-id>]
kind: unit | integration | smoke | manual-capture | other-supported
argv: [<exact token>, ...]
cwd: <canonical-project-relative-path>
environment_allowlist: {<name>: <non-secret-value-or-bound-source>}
timeout_seconds: <positive-integer>
runner:
  name: <name>
  version: <exact-version>
  executable_revision: <explicit-revision> | NOT_APPLICABLE_WITH_REASON
source_identity: <ordered path/revision set>
build_identity: <exact build/candidate revision | NOT_APPLICABLE_WITH_REASON>
expected: <exact exit/result/assertion contract>
raw_log_path: <implementation-owner target path>
raw_log_expected_preimage: <explicit-revision> | ABSENT
raw_log_derivation_contract_revision: <explicit-revision>
raw_log_byte_limit: <positive-integer-at-or-below-fixed-limit>
```

Execution produces `cgs.dev-story-test-execution/v2` with the same fields plus
start/end RFC 3339 UTC, timeout state, exit code or unavailable reason, raw-log
byte count/revision, assertion observations, and normalized result. The result-set
revision is computed over Test-ID-sorted canonical execution records.

For manual capture, `argv` names the deterministic capture/validation command,
not an instruction for later work. Human judgment MAY be an observation only
when the story's approved evidence contract requires it and the artifact records
observer identity, exact build, procedure, time, result, and raw asset revision.

Required evidence is PASS only if it was executed in the current transaction,
matches the approved invocation/source/build, finished within timeout, produced a
complete captured log, and met the expected contract. `SKIPPED`, `UNKNOWN`,
`UNAVAILABLE`, and `NOT_RUN` are blocking non-PASS states.

## 12. Checkpoint and resume

`cgs.dev-story-checkpoint/v2` is immutable and create-only. It contains:

```text
checkpoint ID/revision / created-at / result PARTIAL / request+plan+authorization /
readiness admission / complete source snapshot / owners / failure classification /
status proposal/recorder result+receipt/observed tracker state /
planned+actual write sets / per-path baseline+candidate+current revisions /
AC and Test progress / test execution and raw logs / unexecuted work /
safe resume phase+ordinal / stale predicates / recovery owner+action
```

Checkpoint ID revisions plan, transaction, failure classification, actual-write set,
observed tracker/receipt state, and safe resume point; it excludes timestamp and prose. The
checkpoint revision covers complete canonical bytes.

Resume requires an exact request/checkpoint/revision and the same plan/authorization,
owners, path set, deterministic candidates, runtime derivation contracts, source
admission, and lifecycle transaction chain.
It may continue only from the recorded ordinal after verifying every current
path. Because the story is immutable, any story-byte change after admission is an
unrelated stale-key change and blocks resume. A fresh plan requires fresh READY
and fresh authorization.

Checkpoint consumption does not authorize deletion or mutation of the checkpoint.

## 13. Terminal result

`cgs.dev-story-result/v2` contains:

```text
schema/outcome / workflow+request+plan+authorization revisions / story identity /
readiness consumption / source/dependency/architecture/engine-review results /
owner domains / planned+actual writes and revisions / lifecycle transaction evidence /
tracker proposal/result/receipt + independent read-back verification / Test-ID executions /
AC coverage / checkpoint identity or NONE / before+after mutation snapshot /
next owner/action / generated-at / canonical result revision
```

Outcome rules:

- `IMPLEMENTED`: exact write set, all required tests PASS, immutable story bytes,
  and tracker-only lifecycle transaction verified at `in_review`, with no
  unresolved checkpoint and closure untouched.
- `PARTIAL`: at least one mutation occurred and complete intended state was not
  verified, regardless of checkpoint-write success.
- `BLOCKED`: a contract, evidence, dependency, architecture, version and existence conflict check, or authorization
  precondition prevents safe progress; zero mutation unless reporting an already
  partial resumed state.
- `FAILED`: execution failed while all targets remain/restored to verified
  preimages and no partial state remains.
- `USAGE_ERROR` or `INPUT_ERROR`: invocation/request invalid; zero writes.

The result never equates `IMPLEMENTED` with accepted, complete, done, deployed,
or released. Only the catalog-declared closure workflow owns completion.
