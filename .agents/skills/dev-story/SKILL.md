---
name: dev-story
description: "Implement one exact, readiness-authorized story through a closed single-writer transaction; preserve source provenance, record deterministic test evidence, verify recorder-owned tracker lifecycle transitions with compare-and-swap, and stop at In Review."
---

# Dev Story

Implement one bounded story. This workflow owns implementation only. It may move
the implementation lifecycle from `READY_FOR_DEV` to `IN_PROGRESS` and then to
`IN_REVIEW`; it never writes `Complete`, `Done`, or an equivalent closure state.

Read [implementation-transaction-v2.md](references/implementation-transaction-v2.md)
completely before resolving inputs. That reference defines the canonical request,
plan, ownership, readiness, status-recorder, test-evidence, finding, checkpoint,
and result contracts. Missing, unreadable, or internally inconsistent contract
bytes are `INPUT_ERROR` with zero writes.

## Invocation

Accept exactly:

```text
$dev-story --request <project-relative-request-path>@sha256:<64-lower-hex>
```

The request schema is `cgs.dev-story-request/v2`. It names one exact story, one
admission mode, one persisted readiness record and recorder receipt, one
applicable sprint tracker, the tracker-owned story row, all source manifests, the
intended implementation owner identity, the optional read-only engine-reviewer
identity, the status recorder identity, the failure-checkpoint path, and fixed
limits. The request is scope evidence, not write authorization.

Reject no-argument calls, positional story paths, absolute paths, globs, unsafe
paths, duplicate/unknown options, malformed hashes, mutable selectors such as
`latest`, inferred active-session scope, or more than one story. Return
`USAGE_ERROR` before reading project artifacts and write nothing.

Paths use `/`, Unicode NFC, and project-relative canonical form. Reject traversal,
URI/drive prefixes, symlink escape, case-ambiguous resolution, duplicate aliases,
and any path outside the request's project root. Hash raw bytes with SHA-256.

Run outcomes are exactly:

```text
IMPLEMENTED | PARTIAL | BLOCKED | FAILED | USAGE_ERROR | INPUT_ERROR
```

`IMPLEMENTED` means implementation is in review, not accepted or complete.

## Authority and mutation boundary

The request and frozen sources authorize analysis only. Before any mutation,
produce one complete canonical plan, preview every deterministic candidate and
runtime derivation contract, and obtain one explicit user authorization bound to
`plan_hash`, exact target contracts, owners, and
preconditions. A changed path, owner, operation, candidate, command, or required
source invalidates that authorization.

There are exactly two mutating roles:

1. `implementation_owner` is the sole writer of every business, configuration,
   data, test, raw-log, and manual-evidence artifact in the plan.
2. `status_recorder` is the request's stable lifecycle owner. It prepares exact
   transition proposals, invokes and verifies the tracker-declared
   `lifecycle_recorder`, and owns only the failure checkpoint. It never replaces
   the tracker or story directly. The canonical `cgs.sprint-tracker/v2` recorder
   is the sole tracker writer.

The orchestrator coordinates, verifies, and reports. It never writes a business
artifact. If the orchestrator performs an unavailable delegated role, the plan
must still name one stable role/task identity for that role; this does not merge
the two ownership domains. No path may have two owners.

At most one configured engine specialist may review a frozen packet. The
specialist is read-only, owns no files, may not spawn a writer, and returns only a
hash-bound finding set to the implementation owner. There is no concurrent
primary/specialist write branch.

## Phase 0 — Freeze workflow and request

1. Hash this `SKILL.md`, the transaction reference, and the catalog-declared
   dedicated spec. Record them as `workflow_contract`.
2. Read the exact request bytes, verify its supplied hash and schema, enforce the
   fixed limits, and canonicalize the request according to the reference.
3. Capture project-root identity and a before-mutation snapshot over the complete
   bounded target set. Do not enumerate siblings or recurse beyond a request
   manifest.
4. Require the tracker schema `cgs.sprint-tracker/v2`, a positive
   `tracker_revision`, stable `event_id`, equal `sprint_id`/`active_sprint_id`,
   `sprint_state: ACTIVE`, `lifecycle_owner` equal to the request's exact
   `status_recorder`, and `lifecycle_recorder: cgs.sprint-tracker/v2`. Rehash the
   exact tracker bytes independently; the raw hash is an external CAS binding,
   never an invented tracker field. Require `plan_file`, exact raw-plan
   `plan_sha256`, `plan_revision`, and `story_set_hash` to match the supplied plan,
   and validate the typed capacity and complete story row. Reject any request that
   gives the orchestrator a business path, gives the engine reviewer a write path,
   assigns one path twice, omits the tracker or checkpoint, or permits an unlisted
   output.

Any failure in this phase is `INPUT_ERROR`; allowed write set remains empty.

## Phase 1 — Admit one current implementation gate

Read and hash the story before any delegation. Require `Schema: cgs.story/v2` or
an explicitly versioned compatibility adapter named by the request. Never infer
readiness from `Status`, `Story Status`, a sprint row, prose, or a conversational
readiness result.

Admission mode is exactly `CURRENT_READY` or `STRUCTURED_ACCEPTED_RISK`.

`CURRENT_READY` requires all of the following:

- one persisted `READY` record conforming to
  `cgs.story-readiness-record/v1`, bound to the exact story ID/path/raw hash;
- one valid `cgs.story-readiness-recorder-receipt/v1` proving `RECORDED` or
  `ALREADY_RECORDED` for that exact record/candidate/readiness key and registry
  final hash;
- `implementation_gate_eligible: true` in the persisted record/receipt contract;
- a complete stale key naming every story, GDD, systems-index, TR registry/entry,
  ADR, control-manifest, dependency, asset, AC/Test/QA-plan, sprint/context,
  review-mode, reviewer, checker, and ruleset identity used by the gate; and
- fresh raw bytes, schemas, statuses, joins, and hashes for every stale-key entry.

Independently rehash and revalidate the story, registry/TR entries, Approved GDD,
systems index, every governing ADR, current control manifest, dependencies,
declared assets/tests, technical preferences, engine-version reference, sprint
plan/tracker, readiness registry, record, and receipt. A missing, unreadable,
invalid, hash-mismatched, stale, partial, non-READY, or unpersisted ordinary gate
is `BLOCKED` with zero writes. An old READY claim or changed story cannot
substitute for this gate.

`STRUCTURED_ACCEPTED_RISK` is the only non-READY branch. Require a persisted,
complete `NEEDS_WORK` record and recorder receipt for the exact current story.
Every check except exact control-manifest staleness and/or explicitly soft
dependency incompleteness MUST pass; there may be no BLOCKED/UNVERIFIED check,
architecture gap, hard dependency gap, ambiguous AC/Test mapping, invalid source,
or unknown evidence. The complete plan MUST contain exact structured waiver
records from the reference, and the approval question MUST name them. This mode
never sets `implementation_gate_eligible: true`, never calls the story READY, and
  labels preview, lifecycle transactions, checkpoint, and result `STALE /
ACCEPTED-RISK` or `SOFT-DEPENDENCY / ACCEPTED-RISK` as applicable.

Preserve captured provenance exactly. Never rewrite Manifest Version, Manifest
Hash, Source Snapshot, source-manifest ID, or story-core hash to make evidence
look current. Outside the exact structured-risk branch, a stale control binding
is `BLOCKED` and routes to the story owner for re-authoring followed by a new
readiness record. A risk waiver records both captured and current hashes and
never relabels captured provenance as current.

## Phase 2 — Revalidate dependencies and architecture

Parse every dependency as a stable story ID, canonical path, explicit kind, raw
hash, observed lifecycle, and resolution condition. Kind defaults to hard.

- A hard dependency passes only at `Complete` or `Done` under its governing
  lifecycle schema. Every other state, including missing/unreadable, blocks.
- A soft dependency may continue when the admitted record already contains a
  current structured waiver or when the accepted-risk plan contains a new exact
  waiver bound to dependency ID/path/hash, observed state, reason, approver, and
  expiry. A new waiver is recorded only in the approved plan and final result; it
  never changes the dependency, story author artifact, readiness registry, or
  tracker planning fields.
- Never edit, waive, complete, or reinterpret a dependency story.

Build an architecture coverage table from every planned semantic change to an
exact Accepted ADR ID/path/hash/decision locator or to `NOT_ARCHITECTURAL` with a
contract-defined reason. If any implementation choice changes module boundaries,
public interfaces, persistence/schema ownership, threading, networking,
security, platform/engine policy, or another architecture-controlled concern
without an Accepted ADR, create a stable `DSF-<20-lower-hex>` blocker and stop.
Route it to the catalog-declared architecture decision owner with the exact
question and evidence. Do not offer “proceed anyway,” accept a local signature,
draft an ADR, or implement the choice here.

## Phase 3 — Build one closed plan

Planning is read-only. Ask the named implementation owner for one read-only plan
packet bound to the frozen request, story, readiness, sources, and target
preimages. The owner must acknowledge one complete business write set. Config and
data files are ordinary business artifacts: they have the same sole
implementation owner and never become orchestrator writes.

The canonical `cgs.dev-story-plan/v2` contains:

- story/readiness/tracker/request/workflow identities and raw hashes;
- every source path, status, raw hash, and exact field/section used;
- one row per target with exact path, operation, unique owner, semantic change,
  AC IDs, Test IDs, source bindings, expected preimage hash or `ABSENT`, either a
  deterministic candidate hash or an approved runtime derivation-contract hash,
  output bounds, write condition, and rollback classification;
- exact argv-token arrays, working directory, environment allowlist, timeout,
  runner/tool identity, expected result, and raw-log path for every required test;
- architecture coverage and optional engine-review findings;
- two tracker-row lifecycle transition proposals, stable event/transaction IDs,
  the exact recorder CAS tuple, immutable planning-field assertions, recorder
  result/receipt validation, and partial-publication behavior;
- one create-only failure-checkpoint derivation contract, path, and owner; and
- deterministic canonical serialization plus `plan_hash`.

The status recorder owns exactly the transition proposal/verification and the
checkpoint. It invokes the exact tracker-declared lifecycle recorder rather than
writing the tracker. `cgs.story/v2` is an immutable author artifact throughout
this workflow: its raw bytes, `Revision`, `Story Status`, readiness fields, source
bindings, and `x-local-*` extensions do not change. Implementation lifecycle
exists only in the canonical tracker story row. An admitted compatibility story
schema has the same immutability rule. The sprint tracker remains the sole
lifecycle authority.

Reject a plan when any AC lacks both implementation and evidence mapping; a Test
ID/command/log path is missing; a path is vague or unowned; one path has multiple
owners; an owner writes outside its domain; a candidate/derivation/preimage is
absent; Out-of-Scope work is required; rollback safety is unknown; the engine
reviewer would write; or architecture coverage is incomplete. Runtime-derived
  output is allowed only for raw test/manual logs, their execution records, the two
  transition proposals/results/receipts, and the failure checkpoint; its
  derivation, schema, inputs,
limits, and validation MUST be fully fixed.

If engine review is requested, send one immutable
`cgs.dev-story-engine-review-packet/v1` after the planned file types are known.
Accept only a matching `cgs.dev-story-engine-review-result/v1`; malformed,
missing, wrong-hash, or write-proposing output is a blocker. The implementation
owner alone decides how to resolve non-architectural findings within the existing
closed paths. A new path or architectural finding invalidates the plan.

## Phase 4 — Preview and authorize

Render the complete plan, deterministic candidates, and exact runtime derivation
contracts before any write. Present:

1. admission mode, record/receipt, accepted-risk waivers if any, and fresh-source
   evidence;
2. dependency and architecture tables;
3. every target, owner, preimage, candidate/derivation hash, AC/Test mapping,
   output bound, and condition;
4. exact test invocations and evidence paths;
5. `READY_FOR_DEV -> IN_PROGRESS -> IN_REVIEW` tracker-row proposals;
6. lifecycle-recorder CAS, result/receipt/read-back verification, immutable-story
   and planning-field assertions, and partial-state behavior; and
7. canonical `plan_hash`.

Ask once: `Approve dev-story plan sha256:<plan_hash> and this exact changeset?`
An approval is valid only for the displayed canonical plan/candidates and the
current user/task. Refusal is `BLOCKED` with zero writes. Approval does not permit
new paths, changed candidates, architecture decisions, or closure.

## Phase 5 — Execute with CAS and unique ownership

Immediately before the first mutation, rehash every request, source, readiness,
registry, receipt, tracker, story, target, and workflow-contract input. Recompute
   dependency states, tracker raw hash/identity/revision/event, immutable
   plan-file/hash/revision/story-set tuple, stale key,
deterministic candidates, derivation contracts, and plan hash. Any difference
causes zero writes and `BLOCKED`; there is no hidden retry or last-writer-wins.

Require both mutating roles to acknowledge their exact owned path sets and target
contract hashes. A missing/malformed acknowledgement occurs before mutation and
returns `FAILED` with all targets unchanged.

The status recorder then requests the `IN_PROGRESS` tracker-row transaction:

1. rehash the immutable story and exact tracker preimage;
2. prepare one transition proposal carrying a stable `status_transaction_id` and
   recorder `event_id`, requested lifecycle-owned row fields, and exact CAS tuple:
   `expected_tracker_revision`, external `expected_tracker_sha256`,
   `expected_plan_revision`, `expected_story_set_hash`, and
   `requested_field_owners`;
3. invoke only the declared `lifecycle_recorder: cgs.sprint-tracker/v2`;
4. verify the recorder result/receipt, then reread and hash the tracker; and
5. require revision increment by one, the exact event/transaction, row status
   `in_progress` with timestamp/provenance, unchanged story bytes, unchanged
   `plan_file`/`plan_sha256`/`plan_revision`/`story_set_hash`, and every unowned
   tracker field unchanged.

The workflow never writes the tracker directly or claims cross-file atomicity. A
rejected/blocked recorder call with unchanged bytes stops before business writes.
If tracker bytes changed without a fully verified recorder receipt, or the result
is ambiguous/partial, stop all business writes, preserve observed bytes, write the
pre-authorized checkpoint if its `ABSENT` CAS still holds, and return `PARTIAL`.
Do not guess a compensating write or report synchronization.

After verified `IN_PROGRESS`, the implementation owner alone writes the approved
business targets in deterministic plan order. Before each replace/create, recheck
that path's expected current hash/absence and all not-yet-written target
preconditions. After each deterministic write, reread raw bytes and require the
candidate hash. After each runtime-generated evidence write, reread raw bytes and
verify its generator contract, schema, input identities, and byte bounds before
recording the actual hash. The owner returns an ordered actual-write receipt. Any
new path, owner change, candidate/derivation mismatch, CAS conflict, or write
failure stops immediately.

## Phase 6 — Execute and preserve test evidence

Run every approved test exactly as an argv-token array; do not reinterpret it in
a shell, append flags, change cwd/environment, or substitute a later user-run.
For each test, persist the approved raw combined log through the implementation
owner and record:

- stable Test ID and mapped AC IDs;
- exact argv tokens, cwd, environment allowlist, runner/tool version and hash;
- source/build/configuration identity;
- RFC 3339 UTC start/end timestamps, timeout state, and exit code or exact
  unavailable reason;
- raw log path, byte count, and SHA-256; and
- normalized `PASS | FAIL | BLOCKED` result.

Only the approved expected exit/result and required assertions may pass. Missing,
unrun, timed-out, nonzero, malformed, stale, hashless, or truncated blocking
evidence is not PASS. Any required non-PASS result prevents `IN_REVIEW` and enters
Phase 8. Never ask the user to run a blocking test later.

## Phase 7 — Publish In Review

Only after every deterministic business candidate is present at its exact hash,
every generated output satisfies its approved derivation contract, every required
test is PASS, every AC has current evidence, and actual paths equal the planned set
may the recorder derive and prepare `IN_REVIEW` candidates.

The authoritative tracker row and verified status transaction record:

- `plan_hash`, request/readiness record/receipt identities;
- implementation owner, lifecycle owner, and lifecycle recorder identities;
- exact implementation/test/evidence paths and post-write hashes;
- complete per-Test-ID execution records and result-set hash;
- source-context, dependency, architecture, and engine-review finding-set hashes;
- admission mode, provenance label, and exact waiver IDs/hashes or `NONE`;
- `status_transaction_id`, prior transaction ID, and current UTC time; and
- next owner/action: code review followed by story-done.

Submit an `IN_REVIEW` proposal through the same tracker recorder contract as
`IN_PROGRESS`, with a new stable event/transaction ID and the exact current raw
tracker CAS binding. Rehash and verify the recorder receipt and final tracker.
Require row status `in_review`, revision increment by one, unchanged story bytes,
and byte-for-byte preservation of `plan_file`, `plan_sha256`, `plan_revision`, and
`story_set_hash`. An unverified or partial recorder publication is `PARTIAL`,
never `IMPLEMENTED`.

On success return `IMPLEMENTED`, with both tracker transactions verified and the
authoritative row exactly `in_review`. Do not mutate session state, story bytes,
readiness registry, source provenance,
authoring status, review results, or closure state.

## Phase 8 — Failure, checkpoint, and resume

If failure occurs before any mutation, return `FAILED` or `BLOCKED` as classified
and write nothing. After any mutation, do not say “rolled back” unless every
changed path is safely restored from captured bytes and each raw hash is verified.
Restoration itself must be an approved plan operation; there is no ad hoc revert.

Otherwise the recorder writes only the pre-authorized, create-only
`cgs.dev-story-checkpoint/v2` after verifying its `ABSENT` precondition. It records
   the plan/request/readiness/source hashes, owners, expected and observed tracker
   transaction states, immutable story hash, every planned/actual write and hash, completed AC/Test
rows, raw-log evidence, failure, unexecuted work, and one exact safe resume point.
The result is `PARTIAL`. If checkpoint creation also fails, report that failure
and all observed states; never hide the partial writes.

Resume is allowed only through a new request that names the exact checkpoint path
and hash. Revalidate the checkpoint schema, original plan/authorization identity,
all sources, every current target, ownership, and readiness-consumption evidence.
Resume cannot add a path, change an owner/candidate/command, reuse stale READY,
silently delete the checkpoint, or skip a failed test. Any mismatch is `BLOCKED`
and requires a fresh plan and authorization.

## Phase 9 — Return and route

Return `cgs.dev-story-result/v2` with workflow/request/plan hashes, outcome,
source coverage, readiness consumption, dependency/architecture results, owners,
planned/actual write sets, per-file pre/post hashes, both exact tracker transition
proposals/results/receipts, immutable story and planning-field verification,
Test-ID evidence, AC coverage, checkpoint, and mutation snapshot.

For `IMPLEMENTED`, route exactly:

```text
Implementation is IN REVIEW. Run the catalog-declared code-review workflow on
the exact implementation/test paths, then run story-done for this exact story.
Only story-done may close it.
```

For every other outcome, route only the stable finding owner/action or the exact
checkpoint resume. Never invoke another project workflow, claim tests passed
without execution, or recommend closure.

## Non-negotiable rules

- One implementation owner writes every business/config/data/test/evidence path.
- One status recorder owns proposals/verification/checkpoint; only the declared
  `cgs.sprint-tracker/v2` lifecycle recorder writes tracker lifecycle fields.
- An engine specialist is read-only and never overlaps the primary writer.
- The tracker is lifecycle authority; `cgs.story/v2` bytes and Revision are immutable.
- Raw tracker hash is an external CAS binding, never a tracker field.
- Plan file/hash/revision/story-set fields are preserved by lifecycle transitions.
- Required tests need exact execution receipts and raw-log hashes.
- Uncovered architecture is BLOCKED and routed to the ADR owner.
- Changed inputs, targets, deterministic candidates, derivation contracts, or
  owners invalidate plan authorization.
- Partial writes are restored with verified byte identity or exposed by checkpoint.
- This workflow stops at `IN_REVIEW` and never writes `Complete` or `Done`.
