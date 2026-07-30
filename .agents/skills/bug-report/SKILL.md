---
name: bug-report
description: "Creates canonical bug records and evidence-gated lifecycle events with complete draft fields, duplicate-safe allocation, exact runner receipts, and mandatory regression closure."
---

# Bug Report

## Purpose and authority boundary

Create one canonical bug record, produce bounded static candidate findings, record one independently produced build-bound fix candidate, verify one recorded fix against an exact target build, or close one verified defect. Observation, hypothesis, fix reference, candidate recording, runtime reproduction, regression execution, and lifecycle decision remain separate.

This workflow does not assign priority, schedule work, accept risk, implement a fix, invent evidence, waive regression tests, edit triage/sprint/hotfix/release/test-plan artifacts, or invoke another workflow. It records an authorized owner's decision only after the required immutable evidence verifies.

## Explicit subcommand grammar

Accept exactly one form:

~~~text
$bug-report draft --request-manifest {project-relative-path} --request-revision {revision}
$bug-report analyze --analysis-manifest {project-relative-path} --analysis-revision {revision}
$bug-report create --creation-manifest {project-relative-path} --creation-revision {revision}
$bug-report record-fix-candidate --record-manifest {project-relative-path} --record-revision {revision}
$bug-report verify --verification-manifest {project-relative-path} --verification-revision {revision}
$bug-report close --closure-manifest {project-relative-path} --closure-revision {revision}
$bug-report status --bug-id {bug-id} --record-revision {revision}
~~~

Reject an omitted mode, free-form positional description, direct source path, a path in place of a bug ID, unknown mode or flag, duplicate flag, missing value, unsafe ID/path, absolute path, glob, directory scan, or malformed or missing declared revision. Each mode accepts only its listed flags. `draft`, `analyze`, and `status` are read-only. `create`, `record-fix-candidate`, `verify`, and `close` may mutate only their exact owned canonical artifacts after all gates and authorization pass.

Return these independent fields:

| Field | Values |
|---|---|
| `Workflow Status` | `COMPLETE`, `PARTIAL`, `BLOCKED` |
| `Command Disposition` | `SUCCESS`, `NO_CHANGE`, `RETRYABLE_CONFLICT`, `BLOCKED_INPUT`, `BLOCKED_EVIDENCE`, `FAILED_WRITE` |
| `Operation Result` | `DRAFT_INCOMPLETE`, `DRAFT_READY`, `CANDIDATE_FINDINGS`, `DUPLICATE_DECISION_REQUIRED`, `BUG_CREATED`, `OCCURRENCE_LINKED`, `FIX_CANDIDATE_RECORDED`, `FIX_PRESENT_RUNTIME_UNVERIFIED`, `VERIFIED_FIXED`, `STILL_PRESENT`, `CANNOT_VERIFY`, `BUG_CLOSED`, `STATUS_REPORTED`, `ERROR` |
| `Evidence Status` | `VERIFIED`, `STALE`, `PARTIAL`, `UNKNOWN`, `UNAVAILABLE`, `INVALID` |
| `Record Status` | `Open`, `Reopened`, `Fixed Pending Verification`, `Verified Fixed`, `Closed`, `NOT_CREATED`, `UNKNOWN` |
| `Persistence` | `NOT_REQUESTED`, `WRITTEN`, `DECLINED`, `CONFLICT`, `FAILED`, `NOT_ATTEMPTED` |

A parse or identity error produces no business lifecycle result, no bug ID allocation, and no write. `Workflow Status: COMPLETE` means the requested operation was fully evaluated; it does not mean the bug is fixed or closed.

## Versioned artifact contract

Freeze this contract before reading inputs:

~~~yaml template
schema: cgs-bug-report-workflow-contract/v1
inputs:
  draft_request: cgs-bug-draft-request/v1
  analysis_request: cgs-bug-analysis-request/v1
  creation_manifest: cgs-bug-creation-manifest/v1
  fix_candidate_record_request: cgs-bug-fix-candidate-record-request/v1
  hotfix_candidate_link: cgs-hotfix-bug-candidate-link/v1
  verification_manifest: cgs-bug-verification-manifest/v1
  closure_manifest: cgs-bug-closure-manifest/v1
  candidate: cgs-build-candidate/v1
  build_receipt: cgs-build-receipt/v1
  test_execution_manifest: cgs-test-execution-manifest/v1
  reproduction_receipt: cgs-bug-reproduction-receipt/v2
  regression_receipt: cgs-regression-execution-receipt/v2
outputs:
  registry: cgs-bug-registry/v2
  record: cgs-bug-record/v2
  transition_event: cgs-bug-transition-event/v2
  occurrence_receipt: cgs-bug-occurrence-receipt/v1
  fix_candidate_record_receipt: cgs-bug-fix-candidate-record-receipt/v1
~~~

Unknown or incompatible schemas are blocking.

## Canonical paths and identity

Use only:

~~~text
production/qa/bugs/
  _registry.json
  {bug-id}.md
  _events/{bug-id}/{event-id}.json
  _occurrences/{bug-id}/{occurrence-id}.json
~~~

The record path is exactly `production/qa/bugs/{bug-id}.md`, and its `Bug ID` field must match the filename. Do not read or write `production/bugs/` or use a triage report as a record.

Bug IDs match `BUG-[0-9]{6,}` and are allocated only through `cgs-bug-registry/v2`. Event and occurrence IDs are stable UUIDs or registry-allocated business IDs. Every registry entry binds bug ID, record path/revision, status, severity, duplicate stable business key, creation idempotency key, latest event revision, and occurrence-set revision.

Canonical severity is exactly:
- `S1-Critical`;
- `S2-Major`;
- `S3-Minor`;
- `S4-Trivial`.

Never silently convert `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW`. Severity describes impact and must be supplied or confirmed by an authorized reporter/triage source. `Priority` remains `UNASSIGNED` in this workflow unless a pre-existing authorized triage reference is merely cited; this workflow never assigns it.

## Lifecycle and append-only events

Legal transitions are:

| From | To | Decision owner | Required evidence |
|---|---|---|---|
| no record | `Open` | authorized reporter/record creator | complete draft, duplicate decision, registry allocation |
| `Open` or `Reopened` | `Fixed Pending Verification` | canonical bug-registry recorder under authorized bug owner | current hotfix candidate link; exact commit/tree, candidate/build/artifact/platform, regression/smoke/assessment/rollback identities |
| `Fixed Pending Verification` | `Verified Fixed` | authorized QA verifier | conclusive target-build reproduction PASS and automated regression PASS |
| `Fixed Pending Verification` | `Reopened` | authorized QA verifier | conclusive current-build reproduction or defect-sensitive regression FAIL |
| `Verified Fixed` | `Closed` | authorized QA closure owner | current verified transition plus revalidated automated regression evidence |

This workflow creates the initial event and is the sole canonical registry writer for `Open|Reopened → Fixed Pending Verification`, the QA-owned verification/reopen transitions, and closure. The hotfix workflow only creates an immutable candidate link and never writes the bug record, registry, or transition chain.

Reject `Open|Reopened → Verified Fixed`, `Open|Reopened → Closed`, `Fixed Pending Verification → Closed`, all transitions out of Closed, and every owner/evidence mismatch.

Each accepted transition creates one immutable `cgs-bug-transition-event/v2` containing Event ID, bug ID, old/new status, owner identity/role/authority revision, UTC timestamp, reason, exact evidence paths/revisions, record preimage revision, prior event path/revision, and event revision. The materialized record is updated in the same all-or-none transaction and points to the new event. History is a verified revision chain, not an unstructured Markdown replacement.

## Phase 0: Validate paths, IDs, budgets, and authority

Resolve every literal project-relative path and real path. Reject path escapes, unexpected symlinks, missing regular files, directories used as files, unsupported encodings, duplicate keys, oversize inputs, and schema errors. revision raw bytes before parsing.

Each request manifest declares maximum files, total bytes, per-file bytes, evidence records, findings, and output bytes, all at or below the workflow safety ceiling. Exceeding a budget returns `Workflow Status: PARTIAL`, `Command Disposition: BLOCKED_INPUT`, and no write.

For ID-addressed operations, resolve only the canonical record path and registry entry. Verify registry, record, filename, body ID, status, severity, latest event, and revisions agree. Multiple records with the same ID, an absent registry row, legacy-only data, or any mismatch blocks before business evaluation.

## Phase 1: Draft with required, optional, and unknown fields

`draft` consumes `cgs-bug-draft-request/v1` and produces a conversation-only candidate. It never allocates a Bug ID or writes a canonical record.

Classify fields:

### Required and known before create

- reporter identity/reference and observed-at time;
- concise title, category, stable affected system, and confirmed canonical severity;
- exact candidate/build reference, artifact revision or receipt, source commit, platform, and configuration;
- stable Repro Case ID, preconditions, ordered numbered steps, and reset conditions;
- expected result and observed actual result;
- frequency observation with sample basis;
- impact and user/data/safety consequence;
- evidence references/revisions when the report claims attached evidence.

A required field cannot be an empty string, placeholder, inferred value, or `UNKNOWN`. If build, repro steps, expected result, actual result, system, environment, or severity is not known, return `DRAFT_INCOMPLETE`, name every missing field, group the missing questions into no more than three coherent prompts, and write nothing. Do not call the draft complete because it has a title.

### Optional

Logs, images, videos, save files, traces, related issue IDs, accessibility context, network conditions, and additional observers may be absent. If supplied, every artifact has a path, media type, byte count, revision, capture identity, and build/environment binding.

### Explicitly unknown

Regression origin, suspected component, possible root cause, and affected range may be `UNKNOWN` with a reason and owning investigation role. Unknown values remain unknown; do not turn a source-search guess into an observation.

When all required fields are known and internally consistent, return `DRAFT_READY` with:
- `Observed Facts`;
- `Reporter Statements`;
- `Evidence References`;
- `Inferences/Hypotheses` with confidence and basis;
- `Unknowns`;
- proposed duplicate stable business key inputs.

No record exists until `create` succeeds.

## Phase 2: Analyze explicit bounded sources as candidate findings only

`analyze` consumes `cgs-bug-analysis-request/v1`. It contains an ordered allowlist of project-relative files and raw revision values, explicit analysis questions, parser/language identity, and strict file/byte/finding budgets. Reject a directory, glob, repository-wide implicit scan, path outside the project, changed revision, or undeclared dependency.

Inspect only the declared bytes. Each output is `cgs-bug-candidate-finding/v1` with:
- stable Finding ID and stable business key;
- exact path/revision and tight line or symbol locator;
- observed code fact;
- inferred failure mode, separately labeled;
- confidence `HIGH`, `MEDIUM`, or `LOW` with basis;
- affected system hypothesis;
- reproduction hypothesis and required target-build evidence;
- possible fix direction, labeled non-authoritative;
- false-positive conditions and owning reviewer.

Static analysis never establishes an observed product defect, actual runtime result, severity, occurrence, or reproduction. Return `Operation Result: CANDIDATE_FINDINGS`, `Record Status: NOT_CREATED`, and `Persistence: NOT_REQUESTED`. To register a bug, a separate draft/create request must supply actual reproduction and reporter-owned required fields.

## Phase 3: Compute duplicate candidates without automatic merge

Normalize the complete draft using `cgs-bug-id/v1`:
- stable system ID;
- normalized symptom class;
- expected-observable signature;
- actual-result or crash signature;
- canonical reproduction-step signature;
- platform family;
- data-loss/corruption signature when applicable.

Exclude reporter name, report time, priority, prose formatting, and the new build ID from the primary stable business key so repeated occurrences can match across builds. Preserve those values in the occurrence.

Read only the exact `cgs-bug-registry/v2` path/revision declared by the creation manifest. Compare primary stable business key and explicit secondary similarity keys. Return candidate rows with existing bug ID/path/revision, match rule, matching and differing fields, current status, and confidence. A revision match is a duplicate candidate, not a duplicate decision.

Only an authorized human decision in `cgs-bug-creation-manifest/v1` may select:
- `CREATE_NEW`;
- `LINK_OCCURRENCE` to one exact open or otherwise linkable bug ID;
- `CANCEL`.

Never silently merge, close, overwrite, or discard an independent occurrence. A link creates one immutable occurrence receipt containing its own candidate/build/platform/repro/evidence identity and the deciding human/authority. It does not rewrite the original observation as though both occurrences were identical.

## Phase 4: Allocate an ID atomically and idempotently

`create` requires a DRAFT_READY payload revision, exact registry path/preimage version/revision, duplicate decision, decision owner/authority, and a stable creation idempotency key derived from the request identity.

For `CREATE_NEW`:

1. If the registry already maps the idempotency key to the same draft revision, return the existing Bug ID and record revision as `NO_CHANGE`; do not allocate another ID.
2. If the same key maps to different bytes, return `RETRYABLE_CONFLICT`.
3. Acquire the bounded exclusive registry allocation lock with atomic create-new semantics.
4. Re-read registry bytes and compare version/revision with the creation manifest.
5. Allocate `BUG-` plus the zero-padded numeric `next_sequence`, at least six digits.
6. Verify the registry has no such ID and the record/event targets are absent.
7. Increment `next_sequence`, add the idempotency/stable business key/record entry, render the Open record, and render the immutable creation event.
8. Stage the updated registry, new record, and event on the same filesystem.
9. Validate schemas, revisions, event chain, internal references, and exact write set.
10. Atomically publish all three or none, read back, then release the lock.

If the lock is busy, registry changed, a target appeared, or read-back fails, publish no partial state and return `RETRYABLE_CONFLICT` or `FAILED_WRITE`. Do not auto-retry with a hidden new ID. A rerun uses the same idempotency key and refreshed registry preimage.

For `LINK_OCCURRENCE`, use the same lock/CAS discipline to publish one absent occurrence receipt and the updated registry occurrence-set revision. Do not allocate a new Bug ID.

The canonical Open record uses `cgs-bug-record/v2` and separates:
- observed facts;
- reporter statements;
- environment/build identity;
- reproduction case and expected/actual;
- evidence references;
- hypotheses/inferences with confidence;
- unknowns;
- fix reference;
- verification evidence;
- current status/event revision;
- related bugs/occurrences.

## Phase 5: Record an exact build-bound fix candidate

`record-fix-candidate` consumes one
`cgs-bug-fix-candidate-record-request/v1`. The request binds the canonical
registry and bug-record paths/raw revisions/revision, expected current status
`Open|Reopened`, one current immutable `cgs-hotfix-bug-candidate-link/v1`
path/raw revision, authorized bug owner identity/role/authority path/raw revision,
collision-resistant transition and receipt IDs, absent event/receipt targets,
transaction deadline, and exact authorization over the rendered write set.

The candidate link is the only fix-candidate business handoff. re-read it and
require state `FIX_CANDIDATE`, the same Bug ID and exact current canonical bug
path/revision/status, Hotfix ID, fix full commit/tree, candidate/build/artifact IDs
and revisions, platform/configuration, build-candidate and build-receipt paths/revisions,
regression Test IDs/source/execution-receipt/log revisions, smoke scope/receipt
revisions, HOTFIX READY assessment path/revision, rollback plan/rehearsal identities,
creation owner/time, and canonical link revision. re-read every referenced artifact
and require all commit/candidate/build/artifact/test/smoke/assessment identities
to join exactly. A path label, PR URL, newest build, conversation, deployment
claim, missing test identity, or stale/mismatched byte is blocking.

This mode records provenance; it does not rerun tests or upgrade local evidence
to verification. After owner-authority validation, acquire the canonical registry
lock, reread the registry/record/prior event/link/authority bytes, validate the
complete event chain, and CAS the declared preimages. Atomically publish all or
none of:

1. one immutable `Open|Reopened -> Fixed Pending Verification`
   `cgs-bug-transition-event/v2`;
2. the updated materialized bug record with the exact fix/candidate/build/test
   references and no QA-verification claim;
3. the updated registry row/revision/latest-event revision; and
4. one immutable `cgs-bug-fix-candidate-record-receipt/v1` binding request,
   authority, link, pre/post revisions, lock/CAS/commit/read-back evidence, result,
   and receipt revision.

Only verified all-member read-back may return `FIX_CANDIDATE_RECORDED` and
`Fixed Pending Verification`. Any conflict, collision, invalid authority,
unsupported link, partial write, or read-back mismatch reports non-success and
must not advance canonical state. This mode cannot write `Verified Fixed` or
`Closed`; hotfix cannot invoke or impersonate this recorder and never owns a
canonical bug-registry path.

## Phase 6: Validate verification authority and exact build

`verify` consumes `cgs-bug-verification-manifest/v1`. It binds:
- canonical registry and bug-record paths/revisions;
- expected current status `Fixed Pending Verification`;
- canonical recorder fix-candidate transition event/receipt paths and revisions;
- fix commit/PR, candidate manifest/revision, build receipt/revision, artifact revision, platform/configuration;
- exact Repro Case ID and steps revision;
- exact regression Test ID/path/source revision and failure-sensitivity receipt;
- exact `cgs-test-execution-manifest/v1` path/revision and selected runner row ID;
- either an exact current reproduction/regression receipt set or explicit authorization to execute only the pinned rows;
- QA verifier identity, role, authority path/revision, and transition timestamp;
- record/event destinations with absent-event precondition.

Static source/diff inspection may return only `FIX PRESENT / RUNTIME UNVERIFIED` or `FIX NOT FOUND / RUNTIME UNVERIFIED`. It never changes status.

Revalidate candidate and build receipt agreement on candidate/build/artifact/source/engine/platform/configuration. re-read a local artifact or verify the remote producer receipt. Old logs and receipts are rejected by exact identity/revision, not by timestamp heuristics.

## Phase 7: Execute or consume only the project test manifest

The project execution manifest is the only command authority. Validate:
- runner row ID, runner/binary identity and version;
- ordered argv array and exact selected Test IDs;
- project-root-contained cwd;
- environment-name allowlist and secret redaction policy;
- deterministic seed/order/locale/timezone/clock/parallelism;
- wall-clock and inactivity deadlines;
- stdout/stderr/result/per-record byte limits;
- process-group creation and full process-tree cleanup;
- exit-code map, parser/version, expected result count, log/result destinations.

Never build a shell command, discover a related test by name, run an arbitrary suite, or fall back to an engine default. If execution is authorized, preserve every argv element and use only declared environment names.

Classify runner evidence:
- `PASS` and `FAIL` only when a complete current receipt is conclusive;
- `NOT_RUN`, `TIMEOUT`, `RUNNER_ERROR`, `PARSE_ERROR`, `PARTIAL`, `INVALID_RECEIPT`, `STALE`, and `UNAVAILABLE` are nonconclusive.

On deadline, output cap, cancellation, or crash, terminate the full process tree, record cleanup, revision bounded output, preserve complete parsed records, and mark missing/trailing rows PARTIAL. Never retry with changed argv, seed, scope, parser, or budgets.

Every reproduction receipt contains bug/repro IDs, build/fix/platform/configuration, runner or manual observer identity, start/end, each executed step, expected/observed result, outcome, evidence path/revision, and receipt revision.

Every automated regression receipt contains Test ID/path/source revision, bug/repro IDs, build/fix/platform/configuration, runner/argv/cwd/manifest revision, start/end, exit code/parser/result counts, outcome, log path/revision, cleanup, and receipt revision. It also references current failure-sensitivity evidence proving the test would fail for the original defect. Manual evidence cannot be this receipt.

## Phase 8: Derive verification result and CAS-transition

Use both target-build reproduction and automated regression evidence:

- if both are current, complete, admissible, and PASS, return `VERIFIED_FIXED` and propose `Fixed Pending Verification → Verified Fixed`;
- if a current conclusive reproduction or defect-sensitive regression is FAIL and demonstrates the original defect, return `STILL_PRESENT` and propose `Fixed Pending Verification → Reopened`;
- if either is missing, stale, partial, mismatched, unreadable, nonconclusive, timed out, runner-failed, parser-failed, or from the wrong build/platform/commit/Test ID, return `CANNOT_VERIFY`, preserve `Fixed Pending Verification`, and write nothing;
- static-only evidence returns `FIX_PRESENT_RUNTIME_UNVERIFIED` and `CANNOT_VERIFY`.

For an authorized transition, re-read registry, record, prior event, fix/candidate/build/test authorities, receipts, logs, and verifier authority. Require the new event target absent. Stage the updated record projection, new event, and updated registry row; validate the revision chain; CAS unchanged preimages and absent event; atomically publish all or none; and read back every member. A conflict returns no transition and preserves the observed verification result separately from Persistence.

## Phase 9: Close only with current automated regression evidence

`close` consumes `cgs-bug-closure-manifest/v1`. Require:
- current record state `Verified Fixed`;
- exact current `Fixed Pending Verification → Verified Fixed` event and revision chain;
- exact passing target-build reproduction receipt;
- exact passing automated regression Test ID/path receipt;
- same fix commit, candidate/build/artifact, platform/configuration, Repro Case ID, execution-manifest revision, and failure-sensitivity evidence;
- readable logs/evidence with matching raw revision;
- authorized QA closure owner identity/role and authority path/revision;
- bounded closure reason and immutable closure Event ID.

Manual observation may support the reproduction receipt but never replaces the automated regression Test ID, execution receipt, log, or failure-sensitivity evidence. The repository policy grants no regression-test waiver. A field containing `Manual verification`, `not automatable`, or an approval note is not a regression receipt.

Missing, wrong-build, stale, partial, timed-out, runner-error, unverifiable, non-passing, or manual-only regression evidence returns `BLOCKED_EVIDENCE`, `Operation Result: CANNOT_VERIFY`, leaves the record `Verified Fixed`, and writes nothing.

On success, propose one CAS transaction:
- set materialized status to `Closed`;
- append the immutable `Verified Fixed → Closed` event;
- update registry status/latest-event/revision;
- add the closure record fields: resolution, fix reference, candidate/build/artifact, reproduction receipt, QA verifier, closure owner/authority, automated regression Test ID/path, execution receipt/log revisions, and UTC time.

Closed records have no outgoing transition.

## Phase 10: Status and deterministic handoff

`status` is read-only. Resolve the exact registry entry and record revision, verify the complete event chain and referenced current artifacts, and return current record state, severity, priority reference, evidence currency, duplicate stable business key, occurrence count/set revision, and any integrity findings. It never repairs stale data.

Every mutation preview lists:
- exact CREATE/UPDATE paths;
- preimage and rendered revision values;
- registry revision and lock/CAS preconditions;
- business result, evidence status, resulting record status, and persistence consequence;
- explicit non-writes.

If authorization is declined, preserve the evaluated Operation Result but set Persistence DECLINED and leave canonical state unchanged.

Return exact canonical record path/revision, registry path/version/revision, latest transition event path/revision, occurrence receipt path/revision when applicable, and all consumed evidence identities. Downstream consumers must re-read the registry, record, event chain, and referenced receipts. They must never select a newest bug file, treat a candidate finding as a bug, or treat `Verified Fixed`/`Closed` without the exact event/evidence chain as current.

## Required invariants

- Explicit subcommands and manifests define every operation and illegal combination.
- Required create fields cannot remain unknown or inferred.
- Duplicate candidates require a human decision and independent occurrences remain traceable.
- Registry allocation is concurrency-safe and idempotent.
- Static analysis creates candidate findings, never runtime defects.
- Only exact project-manifest argv and current receipts can verify.
- Timeout, runner error, stale, partial, unavailable, and invalid evidence cannot verify.
- Severity is S1-Critical/S2-Major/S3-Minor/S4-Trivial; priority is separate.
- Manual verification never substitutes for an automated regression test.
- Record projections and immutable append-only events transition atomically.
- Only bug-report `record-fix-candidate` may record Open/Reopened to Fixed Pending
  Verification; hotfix supplies evidence but never registry authority.


## P1 audit traceability

This trace maps the repaired behavior to exact dedicated-spec assertions without changing the sealed contract.

| Audit ID | Enforcing SKILL clause | Dedicated spec case and assertions |
|---|---|---|
| BR-005 | Explicit subcommand grammar — draft/analyze/create/record-fix-candidate/verify/close/status are non-overlapping; invalid forms stop before business work | Case 2; BR-STA-002, BR-STA-003, BR-PRO-001 |
| BR-006 | Phase 1 — required/optional/unknown are explicit and missing critical fields stay conversation-only DRAFT | Case 3; BR-STA-004, BR-STA-005, BR-PRO-003 |
| BR-007 | Phase 3 — stable business key produces duplicate candidates only; human decision preserves each occurrence | Case 4; BR-STA-006, BR-STA-007, BR-PRO-004 |
| BR-008 | Phase 4 — exclusive registry allocation, CAS/absence checks, read-back, and request idempotency prevent collision | Case 5; BR-STA-008, BR-STA-009, BR-PRO-005, BR-PRO-006 |
| BR-009 | Phase 0 + Phase 2 — explicit project-contained paths/revisions and file/byte/finding budgets yield candidate findings, never runtime defects | Case 6; BR-STA-010, BR-STA-011, BR-PRO-007 |
| BR-010 | Phases 6–8 — only exact manifest Test IDs/argv run with bounded deadline, runner/exit/log identity; timeout/partial/stale/error cannot verify | Case 7; BR-STA-012–BR-STA-014, BR-PRO-008–BR-PRO-010 |
| BR-011 | Versioned artifact contract + Phase 1 — severity is exactly S1-Critical/S2-Major/S3-Minor/S4-Trivial and priority remains triage-owned | Case 8; BR-STA-015, BR-STA-016, BR-PRO-011, BR-PRO-012 |
| BR-012 | Phase 0 — canonical ID/path normalization rejects malformed/missing/duplicate/noncanonical/out-of-root/unreadable inputs with zero business verdict/write | Case 2; BR-STA-003, BR-STA-017, BR-STA-018, BR-PRO-001, BR-PRO-002 |
