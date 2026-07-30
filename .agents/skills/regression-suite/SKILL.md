---
name: regression-suite
description: "Maintain a revision-bound, ID-keyed regression test selection manifest. Verifies stable requirement mappings and failure-sensitivity evidence, but never treats file presence as coverage or test selection as a release test result."
---

## Invocation and execution

Invoke exactly one explicit mode:

```text template
$regression-suite report --scope-manifest <project-relative-path> [--execution-receipt <project-relative-path>]
$regression-suite update --scope-manifest <project-relative-path>
$regression-suite audit --scope-manifest <project-relative-path> [--execution-receipt <project-relative-path>]
```

Reject absent/duplicate/unknown mode or flags, positional QA-plan paths, unresolved
bracket tokens, directories, and implicit write-mode requests before project writes.
`update` never accepts an execution receipt because a successful selection change
creates a new manifest revision and necessarily awaits a later run.

Before the first file change, present the complete proposed changeset, listing
every file and intended modification, and obtain one explicit approval. After
approval, make all changes within that boundary continuously without asking
again file by file. If the scope expands materially, stop, present the revised
changeset, and obtain one new approval.

## Contract manifest

```yaml template
schema: cgs-regression-suite-workflow-contract/v1
scope_schema: cgs-regression-scope/v1
qa_plan_schema: cgs-qa-plan/v2
selection_schema: cgs-regression-selection-manifest/v2
owned_output: tests/regression-suite.md
change_impact_schema: cgs-change-impact/v1
modes:
  report: read_only
  update: keyed_upsert_only
  audit: keyed_upsert_or_approved_tombstone
never_executes_tests: true
```

# Regression Suite Selection

This workflow maintains a curated selection of existing automated tests that are
intended to guard stable acceptance criteria and verified bug failure modes. It
does not author tests, execute tests, validate a build, or declare release
readiness.

**Owned output:** `tests/regression-suite.md`

The owned artifact is a **selection manifest**, not a test result and not a
release receipt. A runner or CI system owns execution and produces a separate,
build-bound receipt. Any release gate that uses regression evidence must consume
both the current selection manifest and a matching execution receipt.

## Ownership and non-writes

`$regression-suite` may write only `tests/regression-suite.md` in `update` or
`audit` mode after the complete changeset is approved.

It never writes or modifies:

- test source files;
- QA plans, stories, GDDs, ADRs, bugs, sprint files, or architecture files;
- runner configuration, CI configuration, build metadata, test results, or
  failure-sensitivity receipts;
- session state, checkpoints, release records, or catalog/guide files.

`report` mode is strictly read-only. If no mode is supplied, return invalid
invocation with the supported forms; never prompt into or infer a write mode.

---

## Phase 1: Resolve mode, scope, and evidence sources

### 1.1 Mode

- **`update`** — propose ID-keyed upserts for newly eligible or changed
  selections in the chosen scope.
- **`audit`** — evaluate every stable requirement in the chosen scope and
  propose ID-keyed upserts, gap records, or explicitly approved tombstones.
  Audit never reconstructs or replaces the full manifest.
- **`report`** — evaluate the existing manifest and available receipts without
  writing any file.

Keep operation status separate from coverage status:

- Operation: `REPORTED`, `UPDATED`, `AUDITED`, `UNCHANGED`, `DECLINED`, or
  `FAILED`.
- Coverage: `VERIFIED COVERAGE`, `GAPS FOUND`, `CRITICAL GAPS`,
  `AWAITING RUN`, `STALE`, or `INDETERMINATE`.

A successful manifest write does not imply verified coverage.

Also report independently:

| Axis | Values |
|---|---|
| Scope Status | CURRENT, PARTIAL, STALE, UNKNOWN |
| Impact Status | CURRENT, PARTIAL, STALE, UNKNOWN |
| Selection Status | CURRENT, PARTIAL, STALE, UNKNOWN |
| Execution Status | CURRENT, NOT_RUN, PARTIAL, STALE, UNKNOWN |
| Persistence | WRITTEN, UNCHANGED, NOT_APPLICABLE, DECLINED, FAILED |

Missing, unreadable, unsupported, timed-out, omitted, stale, or incomplete evidence
is PARTIAL/STALE/UNKNOWN, never current or verified. `Operation`, coverage, and all
status axes remain independent; no generic COMPLETE verdict exists.

### 1.2 QA-plan scope and provenance

Resolve the literal scope-manifest path and real path inside the project. Read its
exact bytes once, record the declared revision, and require `cgs-regression-scope/v1` with:

- stable scope, selection-manifest, revision, and operation IDs;
- exact current `cgs-qa-plan/v2` path/revision and expected plan/scope IDs;
- exact QA-plan Test ID ownership snapshot path/revision;
- exact candidate/build manifest or trusted build-receipt path/revision, build ID,
  artifact revision, source commit, platform, and configuration;
- exact story/AC/Requirement Binding/Coverage Unit IDs and source paths/revisions copied
  from the plan;
- exact in-scope bug paths/revisions;
- exact `cgs-change-impact/v1` path/revision with baseline/current identities;
- exact current selection-manifest path and expected base revision or ABSENT;
- optional execution, sensitivity, quarantine proposal/approval/application/runner,
  and bug-verification receipt paths/revisions; and
- budgets for maximum requirements, bugs, Test IDs, test sources, receipts, files,
  input bytes, coverage units, impact edges, candidate entries, estimated duration,
  output bytes, and wall time, all no higher than workflow maxima.

The hard ceilings are 32,768 requirements/coverage units/Test IDs, 4,096 bugs,
65,536 impact edges, 8,192 files/receipts, 128 MiB input, 32,768 candidate entries,
24 hours estimated selected duration, 16 MiB output, and 120 seconds planning time.
Canonicalize IDs/paths using Unicode NFC, forward slashes, and case-fold comparison
keys while preserving raw spelling. Reject unsafe IDs, canonical duplicates, path
escapes, scope/plan/build disagreement, or a requested budget above a hard ceiling.

Sort requirement units, bugs, and Test IDs by stable canonical ID. Admit only whole
authority closures that fit all budgets. Record a complete selected, loaded, missing,
unreadable, invalid, omitted, and unprocessed ledger with bytes/edges/duration and
stable reason IDs. Never scan all GDDs/stories/tests or silently truncate. Any omitted
required closure yields `Scope Status: PARTIAL` and cannot produce verified coverage.

Read the plan as raw bytes and compute
`<revision>`. Parse its Plan Manifest and:

1. Require Artifact Type `cgs-qa-plan`, Schema Version 2, Plan/Effective State
   `CURRENT`, Scope Coverage `COMPLETE`, and Gate Evidence `NO`.
2. Read and Revalidate every captured scope/story/GDD/ADR/control/requirement span,
   build, ownership, dependency, test/evidence source and raw plan bytes.
3. Validate every Test ID owner and every AC root/branch/boundary/error Coverage Unit
   ID from the plan dependency/coverage matrix.
4. Compare current revisions, ownership revision, dependency graph, build binding, and
   source availability with the captured manifest.
5. Treat any mismatch, disappearance, ownership drift, or newly unreadable source as effective
   `STALE`.
6. Treat partial coverage, unsupported receipt/schema, unavailable verifier, or
   ambiguous coverage unit as `UNKNOWN`; reject `PARTIAL`, `STALE`, or `UNKNOWN` plans
   as verified requirement/coverage evidence.
7. Extract exact stable AC/Coverage Unit IDs and their owned stable `TC-...` automated test IDs.
   `MC-...` and `SC-...` items may be reported as manual/config obligations, but
   they are not automated regression selections unless a separately identified
   automated test exists.

Preserve the QA plan path, raw-byte count and revision, effective state, stable AC IDs, and
stable test IDs in the regression manifest. Never derive identity from mutable
criterion wording, title text, list position, or file name.

If no current QA plan is available, report `Scope Status: UNKNOWN`, coverage
`INDETERMINATE`, and do not claim AC
coverage. The user may still approve clearly labelled gap entries, but no
requirement is `VERIFIED COVERAGE`.

### 1.3 Bug requirements

Load only scope-declared bug artifacts as raw bytes. A regression bug requirement is
eligible only when the authoritative artifact has state `VERIFIED_FIXED` and binds:

- exact stable `BUG-[number]` ID, source path/revision, original failure/reproduction ID,
  severity, and owner;
- fix commit and source-tree identity;
- verification receipt path/revision proving the original failure on a pre-fix build and
  pass on the fixed build with current reproduction/test revisions; and
- fixed build ID/artifact revision/source commit/platform/configuration exactly matching
  the scope target build or an explicitly declared compatible build matrix.

`Closed`, `Fixed`, merged PR, assignee statement, changelog text, or fix commit alone
does not prove verified repair. A missing/mismatched verification receipt or target
build makes the bug status `UNKNOWN/STALE` and excludes it from verified-fixed
prioritization while preserving it as an explicit requirement gap.

A bug ID in a test file name, comment, or prose is discovery evidence only. It
does not prove that the test exercises the original failure or would fail if the
bug returned.

### 1.4 Change impact and deterministic prioritization

Validate `cgs-change-impact/v1` schema, producer/tool/version/revision, baseline/current
source commits, changed path preimage/result revision, changed Requirement Binding/
AC/BUG/Coverage Unit IDs, impacted production symbols/systems, and dependency edges.
Every impact edge names its source authority/path/revision, relation, and nonnegative graph
distance. Revalidate all local dependencies. Missing edges/endpoints, unmatched change,
partial traversal, stale baseline/current identity, or unavailable producer makes
`Impact Status: PARTIAL/STALE/UNKNOWN`; never infer impact from filenames or prose.

Build the candidate set from exact current plan ownership and impact rows, then sort by
this lexicographic key without model scoring:

1. obligation class: critical verified-fixed bug, critical changed requirement,
   direct changed requirement, direct dependency impact, required always-run baseline,
   transitive impact, then unaffected retained selection;
2. requirement severity rank P0, P1, P2, P3, then UNSPECIFIED;
3. impact graph distance ascending;
4. stable Coverage Unit ID, Test ID, and source canonical path ascending.

Select every mandatory P0/P1 critical/verified-fixed obligation first. Then admit whole
tests in key order while maximum Test IDs, files, input bytes, candidate entries, and
estimated-duration budgets permit. Record selected and omitted rows with full sort key,
estimated duration source/revision, and reason. If a mandatory item cannot fit, is missing,
or has unknown impact/severity/duration, set Selection Status PARTIAL/UNKNOWN and
Coverage `CRITICAL GAPS`; never silently demote it or use an invented score.

### 1.5 Existing manifest and external evidence

Read `tests/regression-suite.md` as raw bytes when it exists and compute its
revision. Parse only explicitly keyed managed entries. Preserve legacy or
unrecognized content byte-for-byte.

Locate, but do not create or modify:

- configured runner/CI test result receipts, normally under `test-results/`;
- failure-sensitivity or mutation receipts;
- the current release/build identity when one exists;
- authoritative quarantine records and the runner/CI configuration they claim
  to affect.

When several receipts exist, match by exact IDs and revisions. Do not use “latest
file” as proof of current execution.

For quarantine, distinguish state-machine evidence exactly:

- `REQUESTED` or `PROPOSED` is advisory and never changes runner state;
- `APPROVED` requires a separate authorized approval receipt;
- `APPLIED` requires the approved proposal, application receipt, adapter identity,
  changed runner/config path/revisions, owner, issue, and unexpired deadline;
- `VERIFIED` additionally requires a later runner receipt bound to the exact applied
  config revision, selection manifest, target build, and stable Test ID, explicitly
  recording it skipped/quarantined.

Only a current unexpired `VERIFIED` row becomes selection state `QUARANTINED`.
`APPLIED` without the later matching runner receipt is
`QUARANTINE_APPLIED_UNVERIFIED`; proposal/registry text alone is
`QUARANTINE_REQUESTED`. Neither counts as pass or verified coverage. Expired, removed,
revision-mismatched, or unreadable evidence is STALE/UNKNOWN and release-blocking.

---

## Phase 2: Build the test evidence inventory

Read every candidate test source in full and record its explicit revision. A path,
file name, directory, function name, comment, or keyword match may identify a
candidate, but none of those facts establishes coverage.

For each candidate collect:

- exact stable test ID;
- exact mapped stable AC and/or BUG IDs;
- exact mapped Coverage Unit IDs for AC root, branch, boundary, error/recovery, and
  verified bug reproduction units;
- test source path and declared revision;
- test function/case identity used by the runner;
- requirement source path and declared revision;
- Requirement Binding ID, raw span revision, and current build binding;
- QA plan path/revision/effective state for AC mappings;
- failure-sensitivity receipt path/revision/status;
- quarantine record and applied runner/config revision, if relevant.
- current change-impact row/distance and deterministic prioritization key.

A candidate without a unique stable test ID or an exact stable requirement ID is
`UNMAPPED`. Never invent, renumber, or write an ID into source files.

### Failure-sensitivity evidence

A mapping is sensitivity-verified only when an external receipt proves all of
the following:

1. It names the exact stable Test ID and every claimed AC/BUG/Coverage Unit ID.
2. It records the same test-source, requirement-file/span, QA-plan, ownership snapshot,
   and build revisions currently
   observed.
3. It identifies the injected or recreated failure condition.
4. The baseline test passed.
5. The test failed when that failure condition was introduced.
6. The receipt itself has a recorded declared revision and a valid producer/run
   identity.

A test that merely asserts something, contains an ID in a comment, or passed once
without the failure condition is not sensitivity-verified.

### Selection evidence states

Assign one deterministic state to each candidate:

| State | Required meaning |
|---|---|
| `ELIGIBLE` | Exact stable mapping, current source revision, and valid failure-sensitivity evidence |
| `SELECTED_UNVERIFIED` | Candidate is selected but mapping or sensitivity evidence is incomplete |
| `STALE` | A captured QA-plan, requirement, test, or sensitivity revision no longer matches |
| `MISSING` | No candidate test exists for the stable requirement |
| `QUARANTINED` | Authoritative quarantine is applied and verified against current runner/config |
| `QUARANTINE_APPLIED_UNVERIFIED` | Application receipt is current but no later matching runner receipt proves the skip |
| `QUARANTINE_REQUESTED` | Quarantine is claimed but runner/config application is not verified |
| `PARTIAL` | Required mapping, impact, sensitivity, parser, or receipt coverage is incomplete |
| `UNKNOWN` | Required evidence cannot be read or conclusively validated |
| `TOMBSTONED` | Entry is retired with retained history, reason, and explicit approval |

Only `ELIGIBLE` entries can contribute to verified coverage, and only when a
matching current execution receipt also passes.

---

## Phase 3: Validate build-bound execution separately

This workflow never executes a runner and never creates an execution receipt.

A conforming runner/CI receipt must contain:

- immutable candidate/build manifest revision, build ID/artifact revision, source commit,
  platform, and configuration matching the scope;
- exact declared revision of `tests/regression-suite.md` used for selection;
- selection schema/manifest/revision IDs, QA-plan revision, Test ID ownership snapshot
  revision, and requirement-span revisions;
- runner identity/version and runner/config revision;
- invocation timestamp and exit status;
- every active selected stable test ID;
- for each test: result, duration, test-source path/revision, and mapped stable
  AC/BUG IDs;
- explicit omissions, skips, quarantines, crashes, and incomplete discovery;
- start/end timestamps, process termination state, complete untruncated log path/revision,
  parser path/version/revision/status, and coverage ledger; and
- receipt declared revision or a verifiable signature.

A receipt is current only when its selection-manifest revision equals the currently
observed manifest revision, its test-source revision match, and its build identity is
the exact build being evaluated. A receipt bound to a prior manifest, prior test
bytes, or another build is stale.

`report` and `audit` may classify an explicitly supplied receipt; `update` never uses
one to claim post-write execution. After any changed manifest publication, set
`Execution Status: NOT_RUN` and Coverage `AWAITING RUN` until a separate runner owner
produces a receipt for the new exact manifest/build. This workflow never invokes that
runner, waits for it, or manufactures its receipt.

### Coverage computation

Use exact set operations. The required set is every scope-declared current QA-plan
Coverage Unit ID, including every AC root, branch, boundary, error/recovery, and
verified bug reproduction unit. The mapped set is the union of exact current coverage
unit claims from selected stable Test IDs. `required - mapped` is always `MISSING`; it
is never subjectively called partial or covered.

For each Coverage Unit ID in stable order:

- `VERIFIED` — at least one exact `ELIGIBLE` selected Test ID maps the unit, has
  current failure-sensitivity evidence for that unit, and PASS in the exact current
  selection/build execution receipt;
- `GAP` — the unit is MISSING, mapping/sensitivity is conclusive invalid, execution
  FAIL/SKIP, or its only test is quarantined;
- `STALE` — any required scope/plan/requirement span/ownership/build/impact/test/
  sensitivity/selection/quarantine/execution revision mismatches;
- `AWAITING RUN` — current mapping/sensitivity/selection is eligible, but no current
  matching build-bound execution receipt exists;
- `INDETERMINATE` — evidence is unreadable, unavailable, unsupported, partial, or
  otherwise cannot be classified conclusively.

An AC/BUG is VERIFIED only when all of its required Coverage Unit IDs are VERIFIED.
Record the exact missing/stale/awaiting/indeterminate unit sets; a nonempty verified
subset never upgrades the AC/BUG.

Never collapse `AWAITING RUN`, `STALE`, or `INDETERMINATE` into `VERIFIED`.

Aggregate coverage deterministically: any nonverified mandatory P0/P1 or verified-fixed
bug unit yields `CRITICAL GAPS`; otherwise any STALE unit yields `STALE`; any
INDETERMINATE unit yields `INDETERMINATE`; any GAP yields `GAPS FOUND`; any AWAITING
RUN yields `AWAITING RUN`; only all-VERIFIED yields `VERIFIED COVERAGE`. Always report
per-state counts and unit IDs so aggregate priority does not hide mixed states.

### Release-gate contract

A release gate may pass regression evidence only when all are true:

1. The selection manifest is current and its QA-plan provenance revalidates
   `CURRENT`.
2. The gate reads a runner receipt bound to the exact selection-manifest revision
   and target build.
3. Every required active stable test ID is present and passes.
4. Every counted requirement has current failure-sensitivity evidence.
5. No critical gap, unverified skip, or unverified quarantine remains.

The selection manifest alone must never produce release `PASS`. This workflow
reports the two required artifact paths/revisions but does not make the release
decision.

---

## Phase 4: Build an ID-keyed selection patch

### 4.1 Managed entry schema

The file begins with a machine-readable header:

```yaml template
Artifact Type: regression-selection-manifest
Schema Version: 2
Manifest ID: <stable-id>
Revision: <positive-integer>
Scope Manifest: <path + revision>
QA Plan: <path + revision + effective CURRENT>
Build Binding: <candidate/build/artifact/source/platform/config revisions>
Test ID Ownership Snapshot: <path + revision + revision>
Change Impact: <path + revision + CURRENT>
Selection Algorithm: cgs-regression-priority/v1
Selection Status: <CURRENT|PARTIAL|STALE|UNKNOWN>
revision format: revision
```

Header revision increments exactly once for a changed keyed publication and remains
unchanged for a no-op. The file's own declared revision is reported externally and is never
embedded recursively.

Use one stable selection ID per stable test ID:

`RS-[stable-test-id]`, for example `RS-TC-combat-S001-AC01`.

Each managed entry is bounded by exact markers:

```markdown template
<!-- RS-ENTRY-BEGIN: RS-TC-combat-S001-AC01 -->
### RS-TC-combat-S001-AC01

- Lifecycle: ACTIVE
- Test ID: TC-combat-S001-AC01
- Test source: tests/unit/combat/damage_test.gd
- Test source revision: revision:[reference ID]
- Covers AC IDs: AC-S001-01
- Covers BUG IDs: none
- Coverage Unit IDs: [AC root/branch/boundary/error IDs]
- Requirement bindings: [file/span revisions]
- QA plan/build/ownership snapshot: [paths + revisions + states]
- Change impact / priority key: [impact row/revision + exact lexicographic key]
- Estimated duration source: [duration + source/revision]
- Sensitivity receipt: [path + revision reference ID, or missing]
- Selection evidence: ELIGIBLE
- Owner: [human-owned; preserve]
- Rationale: [human-owned; preserve]
- History:
  - [timestamp] [machine field changes and reason]
<!-- RS-ENTRY-END: RS-TC-combat-S001-AC01 -->
```

Test execution results do not belong in this block. They remain in runner
receipts so a manifest update cannot create a circular receipt/revision dependency.

### 4.2 Upsert rules

For `update` and `audit`:

1. Parse entries by exact selection ID.
2. For an existing ID, patch only changed machine-owned fields: test source/revision,
   requirement/Coverage Unit IDs and file/span revisions, QA-plan/build/ownership
   provenance, impact/priority/duration evidence, sensitivity/quarantine receipts,
   lifecycle, and selection-evidence state.
3. Preserve Owner, Rationale, all History items, unknown fields, comments, and
   unrelated surrounding bytes.
4. Append one history event describing each machine-owned change.
5. For a new ID, append one complete managed entry to the managed section.
6. Keep legacy unkeyed content untouched. Add new managed entries alongside it;
   do not migrate or delete legacy text implicitly.
7. Never rebuild the document from discovered files and never replace the full
   manifest in `audit` mode.
8. Validate Test ID and Selection ID ownership/tombstones before adding an entry;
   IDs are never recycled or rebound to another Test ID or requirement.

If a managed block is duplicated, malformed, or cannot be patched without
ambiguity, mark the operation `FAILED` and make no write.

### 4.3 Tombstones, never implicit deletion

An entry absent from the current candidate set is not deleted. Propose a
tombstone separately with:

- stable selection ID;
- prior entry retained;
- `Lifecycle: TOMBSTONED`;
- retirement reason;
- approver and approval timestamp;
- optional replacement/superseding ID;
- immutable prior Test ID/requirement/Coverage Unit ownership and non-reuse marker;
- appended history event.

Apply a tombstone only when it is explicitly listed in the approved changeset.
Without that approval, leave the entry byte-for-byte unchanged and report the
drift. Never physically remove the entry or its history.

Tombstone approval is revision-bound to exact Selection ID, prior entry revision, reason,
replacement, approver, timestamp, and candidate manifest revision. The same ID remains
reserved forever. A replacement receives a new Selection ID and preserves a
supersedes link. Duplicate/malformed blocks, ownership conflicts, stale prior revisions,
or attempted ID reuse fail the complete patch before any write.

---

## Phase 5: Preview, write, and verify

### 5.1 Conversation report

Report:

- selected scope and QA-plan path/revision/effective state;
- manifest path/current revision;
- requirement counts by `VERIFIED`, `GAP`, `STALE`, `AWAITING RUN`, and
  `INDETERMINATE`;
- selected entries by evidence state;
- exact runner receipt/build used, or why no current receipt exists;
- proposed keyed upserts and tombstones;
- operation status and coverage status as separate fields.

File-name or text matches may appear only under “discovery candidates”; never
under verified coverage.

### 5.2 Authorization and concurrent-edit guard

`report` mode shows the report, records `Operation: REPORTED`, and performs no
write. Do not ask for write authorization and do not say the suite was updated.

For `update` or `audit`, show the complete keyed diff, candidate manifest bytes/revision,
every entry preimage/result revision, separate tombstone approvals, and explicit
non-writes. A truncated/summary-only diff cannot authorize. Ask once to apply the
one-file changeset.

Immediately before writing:

1. Re-read and Revalidate the manifest.
2. Abort if its revision differs from the previewed revision.
3. Revalidate the scope, QA plan, all requirement spans, Test ID ownership, build,
   change-impact, bug verification, test/sensitivity/quarantine and execution sources
   used by proposed machine-owned fields; abort if any availability/revision/state changed.
4. Revalidate every Selection ID ownership, entry preimage, tombstone approval, and
   exact candidate declared revision. Any conflict aborts the whole patch before writing.
5. Apply only the approved per-ID field patches, appends, and tombstones to an isolated
   staged candidate; parse and verify schema, unique IDs, revision increment, history,
   non-reuse, preservation, and internal references.
6. Publish only `tests/regression-suite.md` with compare-and-set against the previewed
   raw manifest revision.
7. Read it back, verify exact candidate bytes, approved changes, preserved human/
   unknown fields, and record the final incremented manifest revision.

If CAS, persistence, parse, reference, preservation, or read-back verification fails,
report `Persistence: FAILED`, `Operation: FAILED`, preserve concurrent bytes, and never
claim any keyed change applied. Do not restore a saved whole manifest over a diverged
file; recovery requires a new preview from current bytes.

If approved output is byte-for-byte identical, do not rewrite it; report
`UNCHANGED` with the verified revision.

### 5.3 Result protocol

Report a per-operation ledger:

| Operation | Selection IDs | Result | artifact revision / Evidence |
|---|---|---|---|
| upsert | [IDs] | written / unchanged / declined / failed | [revision or reason] |
| tombstone | [IDs] | written / not-approved / declined / failed | [revision or reason] |

Use `written` only after read-back verification. Never report the manifest as
updated after a report-only run, declined write, conflict abort, or failed
verification.

Final output contains both dimensions:

- `Operation: REPORTED` for report mode.
- `Operation: UPDATED` or `AUDITED` only after verified keyed changes.
- `Operation: UNCHANGED` when verified bytes already match.
- `Operation: DECLINED` or `FAILED` otherwise.
- `Coverage: VERIFIED COVERAGE` only when current mappings, sensitivity evidence,
  and matching build-bound pass receipt all validate.
- `Coverage: GAPS FOUND` or `CRITICAL GAPS` when coverage evidence is missing or
  failed.
- `Coverage: AWAITING RUN` after a manifest change invalidates an older receipt
  or when no receipt exists for the current manifest revision.
- `Coverage: STALE` or `INDETERMINATE` when provenance cannot validate.

A successful `UPDATED` or `AUDITED` operation may legitimately pair with
`GAPS FOUND`, `AWAITING RUN`, `STALE`, or `INDETERMINATE`. Never translate an
operation success into release readiness.

---

## Collaborative protocol

- Exact IDs and revisions are authority; names and prose are discovery hints.
- Do not create missing business tests. Hand gaps to the story/test-authoring
  owner with stable AC/BUG IDs, expected failure condition, and evidence needed.
  `$test-helpers` is not a business-test author and is not a valid remediation
  for a missing regression test.
- Quarantine does not count as passing coverage. An unapplied quarantine request
  is not reported as applied.
- Preserve human rationale, owner, comments, and history on every patch.
- Never execute a test command or manufacture a runner receipt.
- Never write catalog or workflow-guide changes from this workflow.
