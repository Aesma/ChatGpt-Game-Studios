---
name: regression-suite
description: "Maintain a hash-bound, ID-keyed regression test selection manifest. Verifies stable requirement mappings and failure-sensitivity evidence, but never treats file presence as coverage or test selection as a release test result."
---

## Invocation and execution

Invoke this workflow as `$regression-suite`.

Before the first file change, present the complete proposed changeset, listing
every file and intended modification, and obtain one explicit approval. After
approval, make all changes within that boundary continuously without asking
again file by file. If the scope expands materially, stop, present the revised
changeset, and obtain one new approval.

Arguments: `[update | audit | report] [scope: qa-plan-path]`. Treat bracketed
values as optional unless the workflow says otherwise.

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

`report` mode is strictly read-only. If no mode is supplied, ask the user to
choose `update`, `audit`, or `report`; never infer a write mode.

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

### 1.2 QA-plan scope and provenance

Resolve one explicit QA plan for the intended sprint, feature, or story scope.
Use `scope: [qa-plan-path]` when supplied. If several plans could match, ask the
user to select one; never choose by modification time alone.

Read the plan as raw bytes and compute
`sha256:<64 lowercase hexadecimal characters>`. Parse its Plan Manifest and:

1. Require `Plan State at Generation: CURRENT`.
2. Read every captured source path and hash its current raw bytes.
3. Compare current hashes and source availability with the captured manifest.
4. Treat any mismatch, disappearance, or newly unreadable source as effective
   `STALE`.
5. Reject `PARTIAL` or effective `STALE` plans as requirement/coverage evidence.
6. Extract exact stable AC IDs and their stable `TC-...` automated test IDs.
   `MC-...` and `SC-...` items may be reported as manual/config obligations, but
   they are not automated regression selections unless a separately identified
   automated test exists.

Preserve the QA plan path, raw-byte hash, effective state, stable AC IDs, and
stable test IDs in the regression manifest. Never derive identity from mutable
criterion wording, title text, list position, or file name.

If no current QA plan is available, report `INDETERMINATE` and do not claim AC
coverage. The user may still approve clearly labelled gap entries, but no
requirement is `VERIFIED COVERAGE`.

### 1.3 Bug requirements

Load in-scope bug artifacts as raw bytes. A bug mapping requires an exact stable
`BUG-[number]` ID, the bug source path, and its raw-byte SHA-256. Preserve any
verified fix/build references found in the authoritative bug artifact.

A bug ID in a test file name, comment, or prose is discovery evidence only. It
does not prove that the test exercises the original failure or would fail if the
bug returned.

### 1.4 Existing manifest and external evidence

Read `tests/regression-suite.md` as raw bytes when it exists and compute its
SHA-256. Parse only explicitly keyed managed entries. Preserve legacy or
unrecognized content byte-for-byte.

Locate, but do not create or modify:

- configured runner/CI test result receipts, normally under `test-results/`;
- failure-sensitivity or mutation receipts;
- the current release/build identity when one exists;
- authoritative quarantine records and the runner/CI configuration they claim
  to affect.

When several receipts exist, match by exact IDs and hashes. Do not use “latest
file” as proof of current execution.

---

## Phase 2: Build the test evidence inventory

Read every candidate test source in full and hash its exact raw bytes. A path,
file name, directory, function name, comment, or keyword match may identify a
candidate, but none of those facts establishes coverage.

For each candidate collect:

- exact stable test ID;
- exact mapped stable AC and/or BUG IDs;
- test source path and raw-byte SHA-256;
- test function/case identity used by the runner;
- requirement source path and raw-byte SHA-256;
- QA plan path/hash/effective state for AC mappings;
- failure-sensitivity receipt path/hash/status;
- quarantine record and applied runner/config hash, if relevant.

A candidate without a unique stable test ID or an exact stable requirement ID is
`UNMAPPED`. Never invent, renumber, or write an ID into source files.

### Failure-sensitivity evidence

A mapping is sensitivity-verified only when an external receipt proves all of
the following:

1. It names the exact stable test ID and mapped AC/BUG ID.
2. It records the same test-source hash and requirement-source hash currently
   observed.
3. It identifies the injected or recreated failure condition.
4. The baseline test passed.
5. The test failed when that failure condition was introduced.
6. The receipt itself has a recorded raw-byte SHA-256 and a valid producer/run
   identity.

A test that merely asserts something, contains an ID in a comment, or passed once
without the failure condition is not sensitivity-verified.

### Selection evidence states

Assign one deterministic state to each candidate:

| State | Required meaning |
|---|---|
| `ELIGIBLE` | Exact stable mapping, current source hashes, and valid failure-sensitivity evidence |
| `SELECTED_UNVERIFIED` | Candidate is selected but mapping or sensitivity evidence is incomplete |
| `STALE` | A captured QA-plan, requirement, test, or sensitivity hash no longer matches |
| `MISSING` | No candidate test exists for the stable requirement |
| `QUARANTINED` | Authoritative quarantine is applied and verified against current runner/config |
| `QUARANTINE_REQUESTED` | Quarantine is claimed but runner/config application is not verified |
| `TOMBSTONED` | Entry is retired with retained history, reason, and explicit approval |

Only `ELIGIBLE` entries can contribute to verified coverage, and only when a
matching current execution receipt also passes.

---

## Phase 3: Validate build-bound execution separately

This workflow never executes a runner and never creates an execution receipt.

A conforming runner/CI receipt must contain:

- immutable build ID plus build/commit hash;
- exact raw-byte SHA-256 of `tests/regression-suite.md` used for selection;
- runner identity/version and runner/config hash;
- invocation timestamp and exit status;
- every active selected stable test ID;
- for each test: result, duration, test-source path/hash, and mapped stable
  AC/BUG IDs;
- explicit omissions, skips, quarantines, crashes, and incomplete discovery;
- receipt raw-byte SHA-256 or a verifiable signature.

A receipt is current only when its selection-manifest hash equals the currently
observed manifest hash, its test-source hashes match, and its build identity is
the exact build being evaluated. A receipt bound to a prior manifest, prior test
bytes, or another build is stale.

### Coverage computation

For each stable AC/BUG requirement:

- `VERIFIED` — at least one `ELIGIBLE` selected test has a passing result in the
  current matching execution receipt.
- `GAP` — no candidate, incomplete stable mapping, missing/invalid sensitivity
  evidence, or a selected test did not pass.
- `STALE` — any required source, plan, test, sensitivity, manifest, or receipt
  hash is stale.
- `AWAITING RUN` — selection evidence is eligible/current, but no matching
  build-bound receipt exists.
- `INDETERMINATE` — a required source or receipt cannot be read or validated.

Never collapse `AWAITING RUN`, `STALE`, or `INDETERMINATE` into `VERIFIED`.

### Release-gate contract

A release gate may pass regression evidence only when all are true:

1. The selection manifest is current and its QA-plan provenance revalidates
   `CURRENT`.
2. The gate reads a runner receipt bound to the exact selection-manifest hash
   and target build.
3. Every required active stable test ID is present and passes.
4. Every counted requirement has current failure-sensitivity evidence.
5. No critical gap, unverified skip, or unverified quarantine remains.

The selection manifest alone must never produce release `PASS`. This workflow
reports the two required artifact paths/hashes but does not make the release
decision.

---

## Phase 4: Build an ID-keyed selection patch

### 4.1 Managed entry schema

Use one stable selection ID per stable test ID:

`RS-[stable-test-id]`, for example `RS-TC-combat-S001-AC01`.

Each managed entry is bounded by exact markers:

```markdown
<!-- RS-ENTRY-BEGIN: RS-TC-combat-S001-AC01 -->
### RS-TC-combat-S001-AC01

- Lifecycle: ACTIVE
- Test ID: TC-combat-S001-AC01
- Test source: tests/unit/combat/damage_test.gd
- Test source hash: sha256:[digest]
- Covers AC IDs: AC-S001-01
- Covers BUG IDs: none
- Requirement sources: [path + sha256 digest]
- QA plan: [path + sha256 digest + effective CURRENT]
- Sensitivity receipt: [path + sha256 digest, or missing]
- Selection evidence: ELIGIBLE
- Owner: [human-owned; preserve]
- Rationale: [human-owned; preserve]
- History:
  - [timestamp] [machine field changes and reason]
<!-- RS-ENTRY-END: RS-TC-combat-S001-AC01 -->
```

Test execution results do not belong in this block. They remain in runner
receipts so a manifest update cannot create a circular receipt/hash dependency.

### 4.2 Upsert rules

For `update` and `audit`:

1. Parse entries by exact selection ID.
2. For an existing ID, patch only changed machine-owned fields: test source/hash,
   requirement IDs/sources/hashes, QA-plan provenance, sensitivity receipt, and
   selection-evidence state.
3. Preserve Owner, Rationale, all History items, unknown fields, comments, and
   unrelated surrounding bytes.
4. Append one history event describing each machine-owned change.
5. For a new ID, append one complete managed entry to the managed section.
6. Keep legacy unkeyed content untouched. Add new managed entries alongside it;
   do not migrate or delete legacy text implicitly.
7. Never rebuild the document from discovered files and never replace the full
   manifest in `audit` mode.

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
- appended history event.

Apply a tombstone only when it is explicitly listed in the approved changeset.
Without that approval, leave the entry byte-for-byte unchanged and report the
drift. Never physically remove the entry or its history.

---

## Phase 5: Preview, write, and verify

### 5.1 Conversation report

Report:

- selected scope and QA-plan path/hash/effective state;
- manifest path/current hash;
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

For `update` or `audit`, show the complete keyed diff and explicit non-writes,
then ask once to apply the one-file changeset.

Immediately before writing:

1. Re-read and re-hash the manifest.
2. Abort if its hash differs from the previewed hash.
3. Re-hash every source used by a proposed machine-owned field and abort if any
   changed.
4. Apply only the approved per-ID field patches, appends, and tombstones.
5. Write only `tests/regression-suite.md`.
6. Read it back, verify the approved changes, verify preserved human/unknown
   fields, and compute the final raw-byte SHA-256.

If approved output is byte-for-byte identical, do not rewrite it; report
`UNCHANGED` with the verified hash.

### 5.3 Result protocol

Report a per-operation ledger:

| Operation | Selection IDs | Result | Artifact hash / Evidence |
|---|---|---|---|
| upsert | [IDs] | written / unchanged / declined / failed | [hash or reason] |
| tombstone | [IDs] | written / not-approved / declined / failed | [hash or reason] |

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
  or when no receipt exists for the current manifest hash.
- `Coverage: STALE` or `INDETERMINATE` when provenance cannot validate.

A successful `UPDATED` or `AUDITED` operation may legitimately pair with
`GAPS FOUND`, `AWAITING RUN`, `STALE`, or `INDETERMINATE`. Never translate an
operation success into release readiness.

---

## Collaborative protocol

- Exact IDs and hashes are authority; names and prose are discovery hints.
- Do not create missing business tests. Hand gaps to the story/test-authoring
  owner with stable AC/BUG IDs, expected failure condition, and evidence needed.
  `$test-helpers` is not a business-test author and is not a valid remediation
  for a missing regression test.
- Quarantine does not count as passing coverage. An unapplied quarantine request
  is not reported as applied.
- Preserve human rationale, owner, comments, and history on every patch.
- Never execute a test command or manufacture a runner receipt.
- Never write catalog or workflow-guide changes from this workflow.
