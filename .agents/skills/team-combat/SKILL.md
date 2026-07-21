---
name: team-combat
description: "Orchestrate a combat story only after hash-bound design approval, Accepted ADRs, and a final READY story are proven. Plans an exact file-owner manifest before writes, runs only non-overlapping bounded writers, assigns one integration owner, and requires real test evidence for completion."
---

## Invocation and execution

Invoke this workflow as `$team-combat`.

### Implementation invocation

```text
$team-combat <production/epics/.../story-NNN-....md> \
  --design-review <path/to/independent-review-evidence> \
  --readiness-evidence <path/to/final-story-readiness-evidence> \
  --approved-gdd-hash sha256:<64-lowercase-hex>
```

The story path and all three approval arguments are required for implementation.

A free-text feature description is not implementation authorization. When the
argument is missing or is not a concrete story path, output:

> "BLOCKED — team-combat implements one independently approved Ready story.
> Provide a production story path, independent design-review evidence,
> final story-readiness evidence, and the approved GDD hash."

You may summarize which upstream artifacts are missing, but do not author or
revise the GDD, ADR, story, approval evidence, or production files in this run.
Do not spawn implementation writers.

This workflow is an orchestrator. It remains read-only. After an exact manifest
is approved, all authorized writes are delegated to named Codex subagents. A
delegated agent receives no authority beyond its exact manifest rows.

# Team Combat

This workflow coordinates a bounded combat implementation. Product design and
architecture lifecycle decisions must already be approved independently. The
workflow never converts an idea into product rules, accepts an ADR, declares a
story Ready, invents an engine choice, or fabricates validation evidence.

## Non-negotiable invariants

1. **Approved inputs first** — implementation cannot start without a current,
   hash-bound approved GDD, Accepted governing ADRs, a final READY story, explicit
   acceptance criteria, and declared test-evidence destinations.
2. **Read-only proposal first** — planning agents may propose architecture,
   interfaces, paths, and patches, but no file changes occur before manifest
   approval.
3. **Exact authorization** — approval binds exact path, operation, owner, base
   hash, purpose, and manifest hash. Globs and directory-wide grants are invalid.
4. **One writer per path** — every writable path has exactly one owner. Shared
   files belong only to the integration owner.
5. **Bounded concurrency** — only independent tasks with disjoint write sets and
   frozen inputs/interfaces may run in parallel.
6. **No evidence invention** — a test is passing only when an actual command ran
   and its captured evidence proves success for the integrated bytes.
7. **Fail closed** — stale inputs, scope drift, overlap, timeout, late results,
   conflicts, missing evidence, or unauthorized mutations cannot produce
   COMPLETE.

---

## Phase 0: Validate Approved Inputs

Perform this phase without spawning writers and without changing files.

### 0.1 Read and hash the implementation inputs

Read in full:

- the target story;
- its referenced GDD;
- every governing ADR;
- the supplied independent design-review evidence;
- the supplied final story-readiness evidence;
- the current control manifest and QA plan referenced by the story, when the
  story contract requires them;
- engine preferences and the pinned engine version.

Compute SHA-256 over the current raw bytes of the story, GDD, every ADR, control
manifest, QA plan, and approval evidence. Do not hash normalized or copied text.

### 0.2 Prove design approval

The design-review evidence is valid only when all are true:

- it was produced by an independent reviewer, not the GDD author or this
  orchestration;
- its formal verdict is `APPROVED`;
- it names the exact GDD path;
- its reviewed target hash exactly equals both the current raw-byte GDD hash and
  `--approved-gdd-hash`; and
- it contains no unresolved blocker and is not partial, advisory, or stale.

A user statement that the design is approved is not equivalent evidence.
Accepted risk without formal approval is not approval.

### 0.3 Prove story readiness

The readiness evidence is valid only when all are true:

- its final verdict is `READY`;
- it names this exact story path and current raw-byte story hash;
- all required gates in that evidence completed;
- every referenced TR-ID, control-manifest snapshot, QA plan, and dependency is
  current; and
- the story contains complete, testable acceptance criteria and explicit test or
  evidence destinations.

`Status: Ready` in the story alone is not sufficient. A partial, advisory,
NEEDS WORK, BLOCKED, or stale readiness result blocks implementation.

### 0.4 Prove architecture and engine readiness

Every governing ADR must exist, be read in full, and have effective authoritative
`Status: Accepted`. Proposed, missing, deprecated, superseded-without-replacement,
or hash-stale ADR evidence blocks implementation.

An engine and version must be configured. Resolve the primary engine specialist
from the project preferences. If engine configuration, version, or specialist
routing is missing or ambiguous, return BLOCKED; do not improvise an engine-neutral
implementation and do not skip validation.

### 0.5 Preflight verdict

If any check fails:

- report `BLOCKED — APPROVED INPUTS NOT PROVEN`;
- list each missing/stale path, expected hash/status, observed hash/status, and
  owner workflow;
- make zero writes;
- spawn zero implementation writers; and
- stop.

An upstream handoff is advice only. Never invoke that workflow automatically.

Record the validated input snapshot in memory:

```yaml
input_snapshot:
  story: { path: ..., sha256: ... }
  gdd: { path: ..., sha256: ..., approved_sha256: ... }
  design_review: { path: ..., sha256: ..., verdict: APPROVED }
  readiness: { path: ..., sha256: ..., verdict: READY }
  adrs:
    - { path: ..., id: ADR-NNNN, sha256: ..., status: Accepted }
  control_manifest: { path: ..., sha256: ... }
  qa_plan: { path: ..., sha256: ... }
  engine: { name: ..., version: ..., specialist: ... }
```

---

## Phase 1: Read-only Requirements and Interface Plan

Planning output is conversation-only until an exact write manifest is approved.
All planning prompts include paths, hashes, acceptance criteria, relevant
interface excerpts, and a context byte/file budget. Do not copy unrestricted
repository context.

### 1.1 Requirements verification

Delegate read-only review to `game-designer`:

- map every acceptance criterion to an existing approved GDD rule;
- flag ambiguity or missing product decisions;
- do not create, revise, reinterpret, or approve product rules;
- return `PLAN_OK` or `BLOCKED` with evidence.

Any missing rule is BLOCKED. A programmer may not fill the gap.

### 1.2 Architecture and interface proposal

Delegate read-only planning to:

- `gameplay-programmer` for core implementation and integration points;
- `ai-programmer` only when the story/ADR explicitly declares an AI dependency;
- `technical-artist` only when the story explicitly requires visual effects;
- `sound-designer` only when the story explicitly requires audio;
- the resolved engine specialist for engine/version validation;
- `qa-tester` for the pre-implementation acceptance-test contract.

Agents may run concurrently only for independent read-only analysis. Each returns:

- proposed exact files and operations;
- interfaces/events/data contracts consumed or produced;
- shared-file changes as proposals for the future integration owner;
- acceptance criteria covered;
- test commands and evidence paths;
- blockers and unresolved dependencies.

They must not write. They must not claim implementation or tests exist.

### 1.3 Freeze shared contracts

The orchestrator synthesizes one interface contract from the approved inputs and
planning results:

- interface-contract version and SHA-256;
- gameplay events and payload schemas;
- AI hooks;
- VFX hooks;
- audio events;
- tuning data schema;
- test seams and deterministic fixtures.

If planners disagree, escalate the conflict to their shared parent and remain
read-only. No implementation begins until one contract is frozen. A real
dependency may not be mislabeled independent merely to enable parallel work.

---

## Phase 2: Build the Exact File-Ownership Manifest

Inventory the current repository and produce every anticipated mutation before
spawning a writer. Include production code, AI, VFX, audio, test fixtures, test
files, test evidence, integration/shared files, and
`production/session-state/active.md` if checkpoints will be persisted.

Each manifest row is exact:

```markdown
| Path | Operation | Sole owner | Base SHA-256/ABSENT | Purpose | Acceptance criteria | Shared? |
|---|---|---|---|---|---|---|
| src/... | create/update | gameplay-programmer | sha256:... | ... | AC-01 | no |
| ... | ... | integration-owner | sha256:... | shared wiring | AC-01, AC-03 | yes |
```

Rules:

- no glob, directory, wildcard, "related files", or unspecified asset path;
- exactly one owner per path;
- one agent may own several paths, but no path may have multiple owners;
- only the named integration owner may own shared controllers, event buses,
  registries, scenes/prefabs, shared resources, integration tests/fixtures, or
  the checkpoint;
- non-integration agents may return proposals for shared paths but may not write
  them;
- each update records the current raw-byte base hash; each creation records
  `ABSENT`;
- test/evidence paths are separate rows with a named owner;
- each acceptance criterion maps to at least one implementation row and one
  planned verification/evidence row.

Choose one `integration-owner` before approval. Prefer `lead-programmer` when
available; otherwise designate `gameplay-programmer` explicitly. Record the
chosen role and its exclusive shared paths. The orchestrator is never the
integration owner.

Compute a canonical SHA-256 over the sorted manifest rows plus the input snapshot
and interface-contract hash. Present:

- the complete manifest;
- ownership/conflict analysis;
- execution batches and their concurrency cap;
- per-task deadline and retry policy;
- the single integration owner;
- planned test commands and evidence destinations;
- the checkpoint path/owner; and
- manifest SHA-256.

Ask once:

> "Approve this exact path/owner/operation/base-hash manifest for implementation?"

Approval covers only those exact rows and hashes. Delegation does not enlarge it.
If any agent later needs a new path, different operation, different owner, or a
changed base hash, it must return `SCOPE_CHANGE_REQUEST` without writing. Stop,
present the complete revised manifest, and obtain new approval before continuing.

A broad instruction such as "implement the combat feature" never authorizes an
unknown file.

---

## Phase 3: Initialize Checkpoint and Test Contract

After manifest approval, re-read every approved input and manifest update target.
If any hash or absence expectation changed, write nothing and return
`BLOCKED — STALE SNAPSHOT`.

The integration owner is the sole checkpoint writer. It may create/update
`production/session-state/active.md` only when that exact row was approved.
Record:

- workflow/run ID;
- current phase;
- input snapshot hashes;
- interface-contract and manifest hashes;
- approval record;
- integration owner;
- task IDs, owners, exact paths, deadlines, retry counts, and cancellation tokens;
- status per task: `PLANNED/RUNNING/COMPLETE/PARTIAL/BLOCKED/TIMED_OUT/CANCELED`;
- written paths with pre/post hashes;
- test commands and evidence paths;
- unresolved items and the next safe step.

Repeated checkpoint updates use a verified hash chain: the approved initial base
hash is the first base, and each verified post hash is the only permitted base for
the next update. An external or unexplained hash breaks the chain and blocks the
next write. The path, owner, operation, schema, and purpose never change.

The qa-tester, as the sole owner of approved test-contract/test rows, materializes
tests from the already-approved acceptance criteria before implementation when
the manifest includes those files. It must not alter product rules or application
code. Re-read and hash the written test files. A failed or partial test-contract
task prevents implementation tasks that depend on it.

Checkpoint updates never authorize additional paths.

---

## Phase 4: Bounded Non-overlapping Implementation

### 4.1 Form execution batches

A task is parallel-eligible only when:

- all its write paths are pairwise disjoint from every task in the batch;
- it reads the same frozen input and interface hashes;
- it does not consume another task's result;
- all prerequisites and test contracts are complete; and
- its role owns every write path in its task.

Use a concurrency cap no greater than the smallest of:

- the repository's configured subagent limit;
- four concurrent implementation writers; and
- the number of independent eligible tasks.

Start every task in one eligible batch before waiting for results. Collect all
results before starting a dependent batch. Serialize tasks that overlap or have
real data/interface dependencies.

### 4.2 Bound every task

Before launch, assign:

- stable run/task ID;
- exact manifest subset;
- base hashes;
- interface-contract hash;
- deadline (default 15 minutes unless the approved plan states another bound);
- cancellation token;
- retry budget of at most one; and
- required result schema.

A retry is permitted only after the prior attempt is canceled and all owned paths
still match their approved bases or verified rollback state. Never run two
attempts for the same path concurrently.

On deadline:

1. mark `TIMED_OUT` and issue cancellation;
2. inspect owned paths read-only for side effects;
3. retry once only when safety is proven and the retry remains within the same
   approved manifest;
4. otherwise record PARTIAL/BLOCKED and stop dependent work.

A result received after timeout/cancellation or from a superseded attempt is
`LATE`. Quarantine it: do not write, apply, merge, or use it as evidence.

### 4.3 Enforce result and mutation boundaries

Each writer returns:

```yaml
task_id: ...
attempt: 1
status: COMPLETE | PARTIAL | BLOCKED
input_hashes: ...
interface_hash: ...
owned_paths:
  - path: ...
    base_sha256: ...
    post_sha256: ...
unwritten_paths: []
shared_path_proposals: []
commands_run: []
evidence_paths: []
issues: []
```

After each batch, independently inventory the workspace and verify:

- no unowned or unapproved path changed;
- each changed path was written by its sole owner;
- base and post hashes are reported and match bytes;
- no shared path was touched by a non-integration writer;
- input/interface hashes match the frozen snapshot.

An unauthorized or overlapping mutation is BLOCKED. Do not silently retain,
relabel, or authorize it after the fact. Report the exact path and writer and stop
dependent integration.

Update the checkpoint through its sole owner after each completed batch.

---

## Phase 5: Single-owner Integration

Begin only after every required upstream task is COMPLETE and its mutation audit
passes. A skipped, PARTIAL, BLOCKED, TIMED_OUT, CANCELED, LATE, or unverified
required result prevents integration.

Only the declared integration owner may:

- apply accepted proposals to shared files;
- wire gameplay, AI, VFX, audio, tuning data, and test seams;
- modify approved integration scenes/prefabs/resources;
- resolve patch ordering within the frozen contract; and
- write approved integration fixtures.

Immediately before each shared-file write, verify the approved base hash. If a
base changed or a proposal conflicts with the frozen interface, write nothing to
that path and return BLOCKED. Do not let the orchestrator or a domain writer
perform the integration as a fallback.

After integration, re-read every manifest path and record its post hash. Verify
that all cross-domain references resolve and no path outside the manifest
changed. Update the checkpoint through the integration owner.

---

## Phase 6: Independent Test Execution and Evidence

The qa-tester may execute only the approved test plan against the integrated
post-hash snapshot. It is independent of implementation writers and owns only
the approved test/evidence paths.

For every command actually run, capture:

- exact command;
- working directory and relevant engine/platform/version;
- start/end time;
- exit code;
- passed, failed, skipped, and not-run counts;
- integrated manifest hash and implementation post hashes;
- raw log/result artifact path and SHA-256;
- acceptance criteria covered.

A statement, code inspection, proposed command, mocked transcript, or agent
summary is not execution evidence. Never say `passed`, `validated`,
`performance within budget`, or `COMPLETE` when the corresponding command was
not run or its evidence is missing/stale.

Performance is verified only when the approved story/QA plan supplies a numeric
budget, an approved measurement command, and captured results. Otherwise report
`PERFORMANCE NOT RUN/NOT PROVEN`.

The evidence owner may write only exact approved evidence paths. Unexpected
runner outputs require a manifest scope-change request before they may be
retained as project artifacts. Recompute evidence hashes after writing.

Map every acceptance criterion to current passing evidence. Missing, stale,
partial, skipped, not-run, or failing evidence remains unresolved.

---

## Phase 7: Deterministic Sign-off

Re-read approved inputs, manifest files, checkpoint, and evidence. Recompute
hashes. Use the strictest applicable verdict:

### COMPLETE

Allowed only when all are true:

- approved GDD, Accepted ADR, READY story, control-manifest, and QA-plan hashes
  remain current;
- every required task and integration is COMPLETE;
- no task timed out, was canceled, returned late/partial, or exceeded scope;
- every manifest mutation has the correct sole owner and verified post hash;
- every acceptance criterion maps to actual passing evidence for the integrated
  bytes;
- required build/tests executed with zero blocking failures;
- no unresolved blocker, conflict, unauthorized write, or unproven required
  performance claim remains.

### NEEDS WORK

Use when the authorized pipeline and integration completed, but current test
evidence contains failures or non-blocking defects that require another approved
changeset. List exact failing criteria, evidence, owners, and proposed next
scope. Never describe the feature as validated.

### PARTIAL

Use when independent work produced usable results but one or more required tasks
are PARTIAL, TIMED_OUT, CANCELED, LATE, skipped, or unavailable. Do not integrate
dependent output, close the story, or claim validation.

### BLOCKED

Use when prerequisites are invalid/stale, manifest authorization is absent,
ownership overlaps, an unauthorized write occurred, a required dependency
failed, integration conflicts, or trustworthy evidence cannot be established.

A user may accept risk, but acceptance does not convert PARTIAL, BLOCKED, missing
execution, or failing evidence to COMPLETE.

Output:

```markdown
## Combat Team Report
Run ID: [...]
Story/GDD/ADR hashes: [...]
Interface/manifest hashes: [...]
Approved manifest: [...]
Integration owner: [...]
Task outcomes and deadlines: [...]
Changed paths with owner and pre/post hashes: [...]
Test commands and evidence hashes: [...]
Acceptance-criteria evidence matrix: [...]
Unauthorized/conflicted/late paths: [...]
Checkpoint: [...]
Outstanding items and owners: [...]

Verdict: COMPLETE | NEEDS WORK | PARTIAL | BLOCKED
```

Recommend only the next legal handoff implied by the verdict. Do not run it
automatically.

---

## Recovery and Resume Protocol

Always produce a partial report when any launched task fails or times out.

To resume:

1. read `production/session-state/active.md` when it is an approved checkpoint;
2. verify run ID, input, interface, manifest, file, and evidence hashes;
3. reject stale or malformed checkpoint state as BLOCKED;
4. do not repeat tasks whose COMPLETE post hashes still match;
5. never revive a canceled/superseded attempt or consume a late result;
6. continue only the next safe incomplete task under the same approved manifest;
7. request a revised manifest approval for every changed path, owner, operation,
   or base hash.

The orchestrator never edits the checkpoint. The checkpoint's sole owner performs
approved updates.

## Side-effect contract

Before exact manifest approval: zero mutations.

After approval: mutations are allowed only on exact manifest paths, by their
named sole owners, with base-hash checks. The workflow may create or update
implementation, test, evidence, integration, and checkpoint files only when each
appears in the approved manifest. It never writes GDDs, ADR lifecycle state,
story readiness state, or approval evidence.

No delegation, retry, resume, user risk acceptance, or broad task description
expands file authorization.
