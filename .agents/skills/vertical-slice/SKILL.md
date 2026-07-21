---
name: vertical-slice
description: "Plan and independently evaluate a hash-bound vertical-slice run using bounded implementation batches, immutable playtest evidence, a two-attempt hypothesis limit, and a deterministic non-overridable verdict."
---

# Vertical Slice

A vertical slice tests whether one representative core loop can meet approved
experience, technical, quality, and velocity thresholds. This skill separates
planning from implementation, evidence capture, evaluation, creative advice, and
recording. It never treats a multi-week build as one conversational changeset.

## Invocation and task separation

Use one explicit mode:

```text
$vertical-slice plan --run-id <slice-run-id> --hypothesis-id <VS-H-stable-id> --attempt <01|02> --prerequisites <exact-manifest-path> [--prior-report <exact-path>] [--target-findings <IDs>]
$vertical-slice evaluate --run-id <slice-run-id> --plan <exact-plan-path> --evidence <exact-evidence-manifest-path> --evaluation-id <stable-id> [--creative-concerns <exact-receipt-path>] [--persist]
$vertical-slice status <exact-evaluation-report-path> --expect-report <sha256:...>
```

Each mode runs in a fresh bounded task. A task that authored the plan, changed
slice code, built the candidate, captured playtest evidence, or authored creative
concerns cannot perform the formal evaluation. `status` is read-only.

Canonical orchestration artifacts live under:

`production/validation/vertical-slices/<hypothesis-id>/attempt-<NN>/<slice-run-id>/`

This skill owns only:

- `plan.md` in `plan` mode; and
- a new `reports/<evaluation-id>.md` in `evaluate --persist` mode.

It never writes slice code, build receipts, raw playtest evidence, the evidence
manifest, project stage, session state, `prototypes/index.md`, a pivot note,
`GRAVEYARD.md`, or a gate record. Those belong to separately authorized owners.

Reject glob-only, directory-only, "latest", "most recent", and modification-time
selection. Reject an existing owned output path rather than overwriting it.

## Status axes

Always report these independently:

- `Workflow Status`: `COMPLETE`, `PARTIAL`, `BLOCKED`, or `ERROR`.
- `Evidence Verdict`: `PROCEED`, `PIVOT`, `KILL`, or `INCONCLUSIVE`.
- `Product Decision`: `PROCEED`, `PIVOT`, `KILL`,
  `NEW_HYPOTHESIS_REQUIRED`, or `AWAITING`.
- `Final Verdict`: `PROCEED`, `PIVOT`, `KILL`, or
  `BLOCKED — PRODUCT DECISION REQUIRED`.
- `Currentness`: `CURRENT`, `STALE`, or `INVALID`.
- `Gate Eligible`: `YES` or `NO`.
- `Persistence`: `NOT_REQUESTED`, `DECLINED`, `VERIFIED`, or `FAILED`.

`Workflow Status: COMPLETE` only means the bounded operation finished.
`Gate Eligible: YES` requires a verified persisted, CURRENT report whose Final
Verdict is PROCEED. No other combination advances Pre-Production.

## Phase 1: Validate an exact prerequisite manifest

`plan` reads only the supplied prerequisite manifest. Require artifact type
`vertical-slice-prerequisite-manifest`, schema version 1, project ID, stage,
hash algorithm `sha256`, source commit and tree hash, engine/version, target
platform/configuration, and an ordered Sources table.

The Sources table must bind exact paths, stable IDs, lifecycle statuses, and raw
SHA-256 hashes for:

- game concept and pillars;
- systems index and every in-scope core-loop system ID;
- architecture and control manifest;
- every governing accepted ADR;
- every in-scope current GDD and acceptance-criterion ID;
- relevant UX/accessibility specification;
- engine version reference; and
- any prior prototype or validation evidence used to set thresholds.

Re-read every source and verify its recorded hash and acceptable lifecycle status.
The project stage must be Pre-Production. Missing, unreadable, ambiguous,
unapproved, stale, or contradictory prerequisites return:

```text
Workflow Status: BLOCKED
Evidence Verdict: INCONCLUSIVE
Product Decision: AWAITING
Final Verdict: BLOCKED — PRODUCT DECISION REQUIRED
Currentness: INVALID | STALE
Gate Eligible: NO
Persistence: NOT_REQUESTED
```

List every failed path/ID. Do not create a plan, worktree, prototype file, or
implementation task.

## Phase 2: Freeze the hypothesis and attempt budget

A hypothesis ID is stable across at most two attempts:

- attempt `01` is the initial run;
- attempt `02` is the single targeted rerun;
- attempt `03` or higher is invalid and returns BLOCKED without writing.

The plan must assign stable IDs to the validation question, each proceed
criterion, each kill rule, each system/AC, each implementation story, each
expected build check, each playtest cell, and each velocity unit.

Freeze a `Hypothesis Definition Hash` over the exact question, intended core
fantasy, proceed criteria, kill rules, measurement definitions, network profile,
and decision matrix version. Freeze a separate `Scope Hash` over the ordered
systems, ACs, story rows, target quality, environment, session matrix, and
prerequisite source hashes.

Attempt 02 requires an exact immutable attempt-01 report path and SHA-256. It is
allowed only when that report is CURRENT, has the same hypothesis ID and
Hypothesis Definition Hash, and its Final Verdict is PIVOT. The rerun plan must:

- name the prior finding IDs being tested;
- retain the original thresholds and measurement definitions;
- include only fixes for those findings plus explicit regression rows; and
- preserve successful prior evidence as historical context, never as proof for a
  changed build.

Changing the validation question, threshold meaning, core fantasy, or kill rule
requires a new hypothesis ID and a new attempt 01. It is not a rerun.

After attempt 02, the same hypothesis cannot create another plan. Another failure
ends in KILL or `BLOCKED — PRODUCT DECISION REQUIRED`. The user may start a
separately approved new hypothesis, but neither this skill nor an adviser may
silently reset the attempt counter.

## Phase 3: Define deterministic evidence requirements

The plan must define the complete start -> challenge -> resolution loop using
stable system and AC IDs. "All core systems" means the exact ordered IDs in the
plan, not an inferred set. The user makes the product scope decision before the
plan is written.

For every proceed criterion define:

- stable criterion ID and requirement/AC owner;
- metric, unit, measurement method, threshold, sample size, and allowed
  tolerance;
- required build/platform/configuration;
- required receipt type and evidence owner; and
- PASS, FAIL, NOT_RUN, UNKNOWN, and STALE mapping.

For every kill rule define an objective, preapproved predicate. KILL cannot be
invented after seeing results.

### Build and technical evidence

Define exact engine/version, build configuration, platform, required commands,
exit expectations, artifact type, and checks. A successful editor launch,
unhashed executable, transcript without provenance, or user claim is not build
evidence.

### Playtest session matrix

Define exact session cells before implementation: session IDs or ID pattern,
tester cohort/role, minimum distinct tester count, platform/device/input,
environment, loop start/end conditions, observation method, required raw capture,
and criteria/hypothesis IDs.

Each completed receipt must contain session ID, tester pseudonymous ID and role,
candidate/build/source identity, timestamps, platform/device/input, step/event
observations, completion state, blockers, raw recording/log path and hash,
observer/producer identity, and attestation. Chat answers and a retrospective
summary alone are not evidence.

If sample count, cohort diversity, required raw capture, or a planned matrix cell
is missing, the affected criterion is NOT_RUN or UNKNOWN and the Evidence Verdict
cannot be PROCEED.

### Network profile

If network interaction is part of the core fantasy or any required criterion,
predefine real-peer or simulated-latency cells for target latency, jitter, loss,
and peer count. Local 0 ms evidence may cover non-network rows only. Missing
target network cells makes the network criterion NOT_RUN and the overall Evidence
Verdict INCONCLUSIVE unless another verified required failure already establishes
PIVOT or KILL.

### Velocity ledger

Define scope units and require each implementation batch to record actual start
and end timestamps, active time, blocked time, owner, story/finding IDs,
pre/post commit and tree hashes, build ID, completed units, and exclusions.
Estimates and day-label prose are not observations. Missing required velocity
fields yields UNKNOWN and prevents PROCEED.

## Phase 4: Produce an immutable slice plan

Use this exact header:

```markdown
Artifact Type: vertical-slice-plan
Schema Version: 1
Slice Run ID: <slice-run-id>
Hypothesis ID: <VS-H-stable-id>
Attempt: <01|02>
Plan Author Task ID: <task-id>
Created At UTC: <RFC3339>
Prerequisite Manifest Path/SHA-256: <path> / <sha256:...>
Source Commit: <git object ID>
Source Tree: <git tree object ID>
Source Manifest SHA-256: <sha256:...>
Engine/Version: <values>
Platform/Configuration: <values>
Hypothesis Definition SHA-256: <sha256:...>
Scope SHA-256: <sha256:...>
Prior Report Path/SHA-256: <path/hash | NONE>
Plan Status: FROZEN
Implementation Authorized: NO
```

Include:

1. validation question, core fantasy, non-goals, and immutable attempt rules;
2. ordered scope manifest with system, GDD, AC, and source hashes;
3. proceed criteria and kill-rule matrices;
4. representative quality definition and objective acceptance measures;
5. bounded implementation story table;
6. build/test receipt requirements;
7. playtest session matrix including network cells when applicable;
8. velocity schema and time/scope budget;
9. deterministic verdict matrix version;
10. worktree and artifact ownership contract; and
11. exact non-writes.

Each implementation story row must include a stable story ID, owned outcome,
input hashes, exact allowed mutation paths or globs, acceptance IDs, dependencies,
owner role, initial-batch ID, at most one remediation-batch ID, and stop
conditions. The plan does not authorize those batches.

Before writing, show the full plan and one exact changeset containing only
`plan.md`. Obtain one bounded authorization unless the request already explicitly
authorizes that path. Re-hash all prerequisites immediately before writing. On
change, return `ERROR — STALE PREREQUISITES` and write nothing.

Reject an existing plan path. Write atomically, re-read, validate every ID/hash,
and report the plan SHA-256. A declined or failed persistence never claims the
plan is frozen.

## Phase 5: Handoff bounded implementation batches

After plan persistence, stop. Do not implement in the planning task.

Every implementation story is executed in a fresh task and an isolated Git
worktree. Lack of an isolated worktree returns BLOCKED; user consent cannot turn
the main workspace into the slice worktree. Record worktree path, branch, base
commit/tree, owner, and retention policy. Never delete or merge the worktree
automatically.

Before each initial or remediation batch writes code, its owner must present an
exact mutation manifest and obtain bounded authorization. The manifest binds:

- run, hypothesis, attempt, plan path/hash, scope hash, story and batch IDs;
- worktree/branch/base commit/tree and pre-batch tree hash;
- exact CREATE/MODIFY paths or tightly bounded globs;
- engine/version/platform/configuration;
- acceptance/build commands and expected receipts; and
- owner task ID, deadline, and stop conditions.

A new path, dependency, system, acceptance criterion, or design rule outside that
manifest stops the batch. It requires a new authorized batch or a product
decision; it is never absorbed into the original changeset.

Each story has at most one initial batch and one targeted remediation batch.
Build failure, deadline expiry, unauthorized scope need, or the exhausted
remediation budget produces a PARTIAL or BLOCKED receipt and stops. There is no
open-ended "run, report, fix, repeat" loop.

Each batch produces an immutable receipt with the manifest hash, actual changed
path/hash list, pre/post commit and tree hashes, commands, exit codes, logs/hashes,
build IDs/artifact hashes, timings, completed scope units, blocker/finding IDs,
and result `PASS`, `FAIL`, `PARTIAL`, or `BLOCKED`. Agent summaries or chat
observations are not receipts.

After all planned stories, a separately authorized build owner produces one final
candidate manifest binding the exact source commit/tree, engine/version,
platform/configuration, build artifact path/hash, build command/receipt, plan
path/hash, and scope hash. Any subsequent code, content, configuration, or build
change creates a different candidate and invalidates evidence for the old one.

## Phase 6: Capture immutable playtest and velocity evidence

Playtest capture is a separate task from planning, implementation, and evaluation.
It executes only the frozen session matrix against the exact final candidate.
Persist raw capture and one immutable receipt per session under paths owned by the
capture task. Do not backfill missing steps from conversation.

The evidence-manifest owner then freezes an ordered manifest containing:

- artifact type `vertical-slice-evidence-manifest` and schema version 1;
- run/hypothesis/attempt, plan path/hash, Hypothesis Definition Hash, Scope Hash;
- prerequisite manifest path/hash and source-set hash;
- final candidate manifest path/hash, commit/tree, build artifact path/hash,
  engine/version/platform/configuration;
- every batch receipt and hash;
- every playtest session receipt/raw artifact and hash;
- velocity ledger path/hash;
- current criterion-result rows keyed by stable IDs;
- known gaps, invalid rows, failures, and finding IDs; and
- evidence-manifest creation timestamp and hash algorithm.

The manifest owner must be distinct from the formal evaluator. Missing, stale,
malformed, or wrong-build inputs remain visible; they are not omitted to improve
the verdict.

## Phase 7: Independent deterministic evaluation

`evaluate` requires a fresh evaluator task ID distinct from all plan, build,
capture, evidence-manifest, and creative-concern task IDs. Read only the exact
plan and evidence manifest. Re-hash their entire referenced graph and confirm one
run, hypothesis, attempt, scope, candidate, engine, platform, and build identity.

Normalize each required row to `PASS`, `FAIL`, `NOT_RUN`, `UNKNOWN`, `STALE`, or
`INVALID`. Apply this precedence:

| Precedence | Condition | Evidence Verdict | Workflow Status |
|---|---|---|---|
| 1 | A verified current preapproved kill rule is true | KILL | COMPLETE |
| 2 | Otherwise any verified current required criterion fails | PIVOT | COMPLETE |
| 3 | Otherwise any required row/evidence is NOT_RUN, UNKNOWN, STALE, INVALID, missing, or partial | INCONCLUSIVE | PARTIAL |
| 4 | Every required criterion passes, session/network matrix is complete, velocity is known, and no blocker remains | PROCEED | COMPLETE |

A reviewer, director, agent, or user cannot change the Evidence Verdict. List
failure and incomplete rows even when a higher-precedence result applies.

## Phase 8: Optional creative concerns and product decision

Creative review is advisory and occurs only after the Evidence Verdict exists. If
`--creative-concerns` is supplied, require an immutable
`vertical-slice-creative-concerns` receipt bound to the exact plan hash, evidence
manifest hash, candidate/build hash, hypothesis/attempt, decision-matrix
version, and the independently recomputed deterministic Evidence Verdict. Record
its concerns and recommended downgrade; do not accept a verdict field as authority.

Creative concerns may never:

- upgrade PIVOT, KILL, or INCONCLUSIVE to PROCEED;
- waive a failed threshold, missing session, stale build, or network gap;
- override a user PIVOT or KILL;
- edit the evidence, plan, report, or project stage; or
- declare their recommendation final.

After evidence and optional concerns, the product owner decides within this
one-way matrix:

| Evidence Verdict / attempt | Allowed Product Decision | Final Verdict |
|---|---|---|
| PROCEED / 01 | PROCEED, PIVOT, or KILL | same as decision |
| PROCEED / 02 | PROCEED, KILL, or NEW_HYPOTHESIS_REQUIRED | PROCEED, KILL, or BLOCKED — PRODUCT DECISION REQUIRED |
| PIVOT / 01 | PIVOT or KILL | same as decision |
| PIVOT / 02 | KILL or NEW_HYPOTHESIS_REQUIRED | KILL or BLOCKED — PRODUCT DECISION REQUIRED |
| KILL / any | KILL or NEW_HYPOTHESIS_REQUIRED | KILL or BLOCKED — PRODUCT DECISION REQUIRED |
| INCONCLUSIVE / any | KILL or AWAITING | KILL or BLOCKED — PRODUCT DECISION REQUIRED |

The product owner may conservatively downgrade evidence but cannot upgrade it.
If no allowed decision is recorded, Final Verdict is BLOCKED. A PIVOT on attempt
01 authorizes only one targeted attempt-02 plan; it does not authorize code or a
new hypothesis. Attempt-02 failure never produces another same-hypothesis PIVOT.

## Phase 9: Persist one immutable evaluation report

Use this exact header:

```markdown
Artifact Type: vertical-slice-evaluation-report
Schema Version: 1
Evaluation ID: <stable-id>
Slice Run ID: <slice-run-id>
Hypothesis ID: <VS-H-stable-id>
Attempt: <01|02>
Evaluator Task ID: <task-id>
Plan Path/SHA-256: <path> / <sha256:...>
Prerequisite Manifest Path/SHA-256: <path> / <sha256:...>
Hypothesis Definition SHA-256: <sha256:...>
Scope SHA-256: <sha256:...>
Evidence Manifest Path/SHA-256: <path> / <sha256:...>
Source Commit/Tree: <git object IDs>
Source Manifest SHA-256: <sha256:...>
Candidate Manifest Path/SHA-256: <path> / <sha256:...>
Build Artifact Path/SHA-256: <path> / <sha256:...>
Engine/Version: <values>
Platform/Configuration: <values>
Batch Receipt Set SHA-256: <sha256:...>
Playtest Session Set SHA-256: <sha256:...>
Velocity Ledger Path/SHA-256: <path> / <sha256:...>
Creative Concerns Path/SHA-256: <path/hash | NONE>
Decision Matrix Version/SHA-256: <values>
Workflow Status: COMPLETE | PARTIAL
Evidence Verdict: PROCEED | PIVOT | KILL | INCONCLUSIVE
Product Decision: PROCEED | PIVOT | KILL | NEW_HYPOTHESIS_REQUIRED | AWAITING
Final Verdict: PROCEED | PIVOT | KILL | BLOCKED — PRODUCT DECISION REQUIRED
Currentness: CURRENT
Gate Eligible: YES | NO
Persistence: VERIFIED
Created At UTC: <RFC3339>
```

Include prerequisite and candidate identity, scope/criteria tables, build results,
playtest matrix and raw-evidence references, network evidence, velocity arithmetic,
all failures/gaps, creative concerns labeled advisory, product decision, attempt
history, deterministic derivation, and exact next owner.

`Gate Eligible` is provisionally YES only for Final Verdict PROCEED, Evidence
Verdict PROCEED, complete evidence, and CURRENT inputs. Before `--persist`, show
the exact one-file CREATE and all non-writes. Re-hash every input immediately
before writing. Reject an existing evaluation path. Write atomically, re-read the
bytes, and verify its SHA-256. Only then return Gate Eligible YES and Persistence
VERIFIED.

If persistence is absent, declined, or fails, retain the calculated evidence and
final verdict but return Gate Eligible NO. This skill never updates an index or
stage; a later recorder must independently revalidate the report and candidate.

## Phase 10: Read-only currentness status

`status` requires the exact persisted report plus its externally recorded
`--expect-report` SHA-256, then reads the complete referenced graph. Reject a
report-byte mismatch as STALE before interpreting its verdict.
Report `Currentness: CURRENT` only when all paths, hashes, IDs, engine/platform,
source commit/tree, build artifact, session set, velocity ledger, and decision
matrix still match.

Any changed source, code, content, configuration, candidate manifest, build
artifact, plan, playtest receipt, raw capture, velocity record, concern receipt,
or report byte makes the result STALE and `Gate Eligible: NO`. A same filename or
successful rebuild does not preserve identity.

A gate consumer may accept only a persisted report with:

- artifact type/schema valid;
- `Workflow Status: COMPLETE`;
- `Evidence Verdict: PROCEED`;
- `Product Decision: PROCEED`;
- `Final Verdict: PROCEED`;
- `Currentness: CURRENT`;
- `Gate Eligible: YES`;
- exact current report and candidate hashes; and
- no later code/build mutation.

All PIVOT, KILL, INCONCLUSIVE, PARTIAL, BLOCKED, stale, invalid, unpersisted, or
advisory-only results are gate-ineligible.

## Final response

Every mode reports exact paths and hashes, hypothesis/attempt/run IDs, owned
writes and explicit non-writes, every status axis, gaps/findings, remaining
attempt budget, and the next separate owner.

Do not chain into implementation, playtest capture, creative review, index
recording, stage transition, or Production planning. Never claim that a plan
authorization approves implementation, that one chat playtest proves a criterion,
or that creative authority can replace evidence.
