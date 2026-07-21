---
name: dev-story
description: "Implement one story through a provenance-preserving, dependency-safe, explicitly authorized file transaction. Requires current traceability or a structured accepted-risk exception, fixes every write path and owner before approval, writes implementation plus tests, records deterministic evidence, and hands the story to code review and story-done."
---

## Invocation and execution

Invoke this workflow as `$dev-story [story-path]`.

Treat the story path as optional only for story selection. This workflow never
treats a story as ready merely because its header says `Status: Ready`.

Before the first file mutation, present one complete changeset preview containing
every normal and recovery-only target path, its unique write owner, intended
operation, precondition hash, and acceptance-criterion coverage. Obtain one
explicit approval for that exact plan. Approval is bound to the plan hash. Any
new path, owner change, or materially different operation invalidates the
approval and requires a revised preview.

# Dev Story

This skill implements one bounded story. It does not close a story:

```text
$story-readiness [story-path] -> $dev-story [story-path]
  -> $code-review [implementation files] -> $story-done [story-path]
```

The only successful lifecycle transition made here is `Ready -> In Progress ->
In Review`. `Complete` and `Done` belong exclusively to `$story-done`.

**Outputs:**

- the approved implementation and test/evidence files;
- synchronized story and sprint-tracker status;
- test evidence containing command, exit code, timestamp, and log hash;
- a recovery checkpoint when the transaction cannot complete cleanly; and
- a handoff to `$code-review` and `$story-done`.

---

## Phase 1: Resolve and freeze the input story

### 1.1 Select the story

- When a path is provided, resolve and read exactly that file.
- With no path, read `production/session-state/active.md`. If it names an
  active story, ask: "Continuing work on [story title] — is that correct?"
- If there is no active story, ask which story to implement and list only story
  files under `production/epics/**/*.md` whose recorded status is Ready or In
  Progress. Exclude `EPIC.md`.

Read the selected story in full before any delegation or mutation. Record its raw
SHA-256 hash as `story_baseline_hash`.

### 1.2 Load authoritative context

Before implementation planning, load and hash the raw bytes of every input:

1. the selected story;
2. `docs/architecture/tr-registry.yaml`;
3. every governing ADR referenced by the story;
4. `docs/architecture/control-manifest.md`;
5. `.codex/docs/technical-preferences.md`;
6. the current sprint plan and `production/sprint-status.yaml`, when present;
7. every dependency story; and
8. every additional GDD, UX, asset, schema, or configuration source explicitly
   referenced by the story.

For each input retain `path`, `sha256:<64 lowercase hex>`, and the sections
or fields used. Hash raw bytes, not normalized or copied text. Missing,
unreadable, or structurally invalid required context is BLOCKED.

Extract from the story:

- ID, title, Status, Layer, Type, estimate, and scope boundaries;
- exact active TR-ID values and the named GDD requirement;
- governing ADR paths;
- Manifest Version and Manifest Hash;
- the `docs/architecture/control-manifest.md` entry in `## Source Snapshot`;
- every acceptance criterion verbatim;
- implementation notes and forbidden work;
- exact test/evidence path;
- dependency records; and
- any existing implementation or dependency waiver.

### 1.3 Fail-closed readiness preflight

Do not trust a prior prose claim that a story is ready. Re-evaluate the
implementation-blocking contract used by `$story-readiness`:

- the TR registry must load and parse;
- every production story must contain an exact registered TR-ID with
  `status: active`;
- every governing ADR must exist and have `Status: Accepted`;
- acceptance criteria, scope, story type, and test evidence must be explicit;
- unresolved design or architecture questions block implementation;
- the current control manifest must have a parseable Manifest Version;
- the story header version, header hash, and Source Snapshot manifest hash must
  all bind to the current raw manifest bytes; and
- dependencies must pass Phase 2 below.

A prior `NEEDS WORK` or `BLOCKED` result remains non-ready. The only
exception handled by this skill is the structured manifest accepted-risk branch
in section 1.4, and it never relabels the readiness result as READY. No waiver
can bypass a missing/invalid registry, inactive TR-ID, Proposed/missing ADR,
unresolved architecture decision, ambiguous required behavior, or hard
dependency.

If an acceptance criterion is subjective for a non-Visual/Feel story, stop and
ask the user for a concrete testable restatement. The clarified text and its
story-file edit must appear in the exact changeset plan before implementation.

### 1.4 Manifest provenance and stale-story choices

Compute `current_hash` from the current raw bytes of
`docs/architecture/control-manifest.md`. Read the story's captured
`Manifest Hash` and Source Snapshot entry as `implemented_against_hash`. Treat this immutable captured value as the story's
`source_manifest_hash`; do not repurpose `current_hash` as source provenance.

The manifest binding passes only when all three story values match the current
manifest: exact version, header hash, and Source Snapshot hash. A matching date
alone never passes.

When the binding is stale, missing, or inconsistent, report the captured and
current values and offer exactly these paths:

- **Stop** — make no mutation and end BLOCKED.
- **Rebase** — make no mutation in `$dev-story`; route the story to its owning
  authoring/update workflow to refresh the version, header hash, Source Snapshot,
  and affected requirements, then require a new final `$story-readiness`
  verdict before rerunning `$dev-story`.
- **Structured accepted risk** — available only when the current manifest is
  readable/valid, the story has a well-formed captured header hash, the Source
  Snapshot contains the same captured hash, and every non-manifest readiness
  check passes. Require an explicit user decision and add the following exact
  record to the planned story edit:

```yaml
implementation_waiver:
  waiver_id: MW-[stable-id]
  kind: manifest-staleness
  implemented_against_hash: sha256:[captured 64-hex hash]
  current_hash: sha256:[current 64-hex hash]
  accepted_by: user
  accepted_at: [ISO-8601 timestamp]
  provenance_status: ACCEPTED-RISK
```

A manifest waiver is invalid unless `waiver_id`,
`implemented_against_hash`, and `current_hash` are exact and internally
consistent. Free text, a Manifest-Note, or a generic "proceed anyway" response
is not a waiver.

On the accepted-risk path:

- never change the story's captured Manifest Version, Manifest Hash, or Source
  Snapshot entry;
- never claim the captured hash is current;
- keep the manifest/readiness result `STALE / ACCEPTED-RISK` in every preview,
  checkpoint, status projection, and summary;
- implement against the captured hash named by
  `implemented_against_hash`; and
- if the current manifest hash changes again before the first mutation, invalidate
  the waiver and restart this section.

---

## Phase 2: Validate dependencies

Parse every dependency as a stable story ID plus a resolvable path. A dependency
is hard by default. It is soft only when the story record explicitly contains
`soft_dependency: true`.

For each dependency, resolve its file and observed status from the file itself.
Use this matrix:

| Dependency | Complete/Done | Ready/In Progress | Draft/Blocked | Missing/unreadable |
|---|---:|---:|---:|---:|
| Hard or type omitted | PASS | BLOCKED | BLOCKED | BLOCKED |
| Explicit soft, no valid waiver | PASS | BLOCKED | BLOCKED | BLOCKED |
| Explicit soft with valid waiver | PASS | ACCEPTED-RISK | ACCEPTED-RISK | ACCEPTED-RISK |

A soft-dependency waiver must be a structured story record containing all of:

```yaml
dependency_waiver:
  waiver_id: DW-[stable-id]
  dependency_id: [stable story ID]
  observed_status: [exact status or MISSING]
  accepted_by: user
  accepted_at: [ISO-8601 timestamp]
  reason: [specific bounded risk]
```

The waiver must match the dependency ID and the freshly observed status. Any
mismatch, status change, missing field, or free-text override is BLOCKED. A user
may approve adding a valid waiver only as part of the complete changeset preview.

Never offer to mark a dependency Complete, never edit a dependency story, and
never allow a waiver for a hard dependency. When blocked, identify the exact
dependency ID, path, observed status, and required resolution, leave all files
unchanged, and stop before planning implementation.

---

## Phase 3: Build the exact file and ownership plan

Planning is read-only. No tracker, story, source, test, waiver, session-state, or
checkpoint file may change in this phase.

### 3.1 Select one implementation writer

Select exactly one primary implementation writer for all business artifacts:

| Story context | Primary implementation writer |
|---|---|
| Foundation or engine/core infrastructure | `engine-programmer` |
| UI | `ui-programmer` |
| AI or pathfinding | `ai-programmer` |
| Networking/replication | `network-programmer` |
| Gameplay, Visual/Feel, or Config/Data | `gameplay-programmer` |

If the named role is unavailable, the current agent may perform the same role,
but the plan must still name one writer. Config/Data is not an inline exception.

When engine-specific review is needed, consult at most one configured engine
specialist during planning. The engine specialist is read-only and returns
findings to the primary writer; it owns no files.

The status recorder is the sole writer for:

- the selected story;
- `production/sprint-status.yaml`, when it exists;
- `production/session-state/active.md`; and
- `production/session-state/dev-story-[story-id].yaml`, a failure-only recovery
  checkpoint.

No path may have more than one write owner.

### 3.2 Produce a closed plan

Ask the primary writer for a read-only implementation plan. It must name every
file it will create or modify; directory names, globs, "related files", and
to-be-determined paths are not accepted. The declared test/evidence path must be
included.

Build one plan table with:

- exact path;
- create or modify;
- unique owner;
- intended semantic change;
- acceptance criteria covered;
- baseline SHA-256 or `ABSENT`;
- applicable source-context hashes;
- normal, success-only, or failure-only write condition; and
- test command(s) that validate the file.

Also include every status/waiver/session/checkpoint file owned by the status
recorder. Capture a baseline raw hash for every existing target and an
`ABSENT` precondition for every planned new file.

Reject the plan when:

- any acceptance criterion has no implementation or evidence mapping;
- a target path or owner is unresolved;
- two agents would write the same path;
- a required test/evidence path is absent;
- the writer cannot stay inside Out of Scope;
- a required architectural decision is not covered by an Accepted ADR; or
- the exact test command cannot be determined.

An uncovered architecture choice is BLOCKED and must be routed to the ADR owner.
It is never approved as an implementation detail inside this skill.

### 3.3 Preview and authorize once

Present:

1. readiness/provenance state, including both manifest hashes;
2. dependency matrix and all accepted-risk records;
3. the complete file/owner plan;
4. exact test commands;
5. lifecycle transitions;
6. rollback/checkpoint behavior; and
7. a deterministic SHA-256 of the canonical plan, `plan_hash`.

Ask once: "Approve implementation plan `[plan_hash]` and this complete
changeset?"

Approval covers only that plan. Before approval there are no writes. After
approval, do not re-prompt per file. If any path, owner, operation, acceptance
mapping, or required command changes, stop, rebuild the plan with fresh baseline
hashes, and request approval for the new plan hash.

---

## Phase 4: Execute the authorized transaction

### 4.1 Compare-and-swap preflight

Immediately before the first mutation, rehash every input and target. All must
match the source and baseline hashes in the approved plan. Re-resolve dependency
statuses and recompute the current manifest hash.

If anything changed, make no mutation. Report the changed path and restart
validation/planning. Never apply an approved plan to changed inputs.

When a sprint tracker exists, validate its `sprint_id`, `active_sprint_id`,
`plan_revision`, `story_set_hash`, and `updated_at` using the exact
`$sprint-status` contract before mutation. Capture its raw-byte preimage hash.
An invalid or conflicting tracker blocks the transaction; never repair it by
guessing. Preserve `sprint_id`, `active_sprint_id`, and `plan_revision` during
lifecycle updates.

### 4.2 Start and synchronize

Start the primary writer with the approved plan and source-hash package. Require
an acknowledgement that it can write exactly its owned paths. A failure to start
or acknowledge occurs before status mutation and leaves story/tracker unchanged.

After acknowledgement and immediately before the first business-artifact write,
the status recorder prepares synchronized replacements for the story and existing
sprint tracker, changing both projections from Ready to In Progress. Apply them
with compare-and-swap semantics. If both cannot be applied, restore the applied
side from its captured bytes. If safe restoration is impossible, write the
approved failure checkpoint and stop; never continue with divergent statuses.
The tracker replacement must recompute `story_set_hash` from every current story
using sorted `ID<TAB>path<TAB>raw-byte-hash` records and set a timezone-qualified
`updated_at`; it must not change `plan_revision`.

### 4.3 Implement only the plan

The primary writer may create or modify only its owned, approved paths. It must:

- follow the Accepted ADR and captured control rules;
- preserve Out of Scope boundaries;
- implement every mapped criterion;
- write the planned automated test or evidence file in the same transaction; and
- report actual paths and post-write hashes.

An engine reviewer may inspect planned files and return findings but may not
write. Any discovered need for an unplanned file stops the transaction. Do not
silently expand scope.

### 4.4 Run and record deterministic tests

Run every approved command. For each command record:

- exact command;
- working directory;
- start/end timestamps in ISO-8601;
- exit code;
- SHA-256 of the raw captured log; and
- pass/fail/blocked result.

Tests that were not run, returned a nonzero exit code, or lack a log hash are not
passing evidence. Logic and Integration stories require their planned automated
tests. Visual/Feel and UI stories require the planned manual-evidence artifact;
Config/Data requires its planned smoke check. Do not ask the user to run blocking
tests later as a substitute.

### 4.5 Commit the status projection

Only when all planned writes exist, ownership matches, target hashes are known,
and every blocking test passes may the status recorder compare-and-swap both the
story and existing sprint tracker to In Review. The story update also records:

- plan hash;
- exact implementation and evidence paths with post-write hashes;
- test command evidence;
- source-context hashes;
- manifest provenance state and waiver IDs; and
- dependency waiver IDs.

Because the story bytes change, recompute the tracker `story_set_hash` from the
complete current story set and update `updated_at` in the same compare-and-swap.
Re-read both projections and verify the hash/identity contract before success.

Update `production/session-state/active.md` within the same approved status
recording step. Never set Complete or Done.

Treat the authorized work as one logical transaction: either every approved
business artifact and synchronized status projection reaches the success state,
or the workflow emits the explicit partial/failure state below.

### 4.6 Failure and partial-write recovery

If the writer fails before any business-artifact mutation, restore both status
projections to their captured pre-transaction bytes and report FAILED.

If any business artifact was created or modified, do not describe the transaction
as rolled back unless every affected path was restored byte-for-byte and verified
against its baseline hash. Otherwise:

1. keep story and tracker synchronized at In Progress;
2. write the pre-authorized failure checkpoint at
   `production/session-state/dev-story-[story-id].yaml`;
3. record plan hash, source hashes, baseline and current target hashes, planned
   and actual write sets, owner, completed criteria, test evidence, error, and
   the exact safe resume point; and
4. return PARTIAL or BLOCKED.

The retained tracker must still carry the current story-set hash and
timezone-qualified `updated_at`. The checkpoint records expected/current tracker
hashes and the unchanged `plan_revision`. A checkpoint never substitutes for an
invalid tracker.

A failure checkpoint is evidence, not permission to expand the plan. Resume only
after revalidating its hashes. Never move a partial or failed transaction to In
Review.

---

## Phase 5: Report and hand off

Use one of `IMPLEMENTED`, `PARTIAL`, `BLOCKED`, or `FAILED`.

```markdown
## Dev Story: [story ID] — [IMPLEMENTED/PARTIAL/BLOCKED/FAILED]

Plan: sha256:[plan hash]
Story status: [In Review/In Progress/unchanged]
Tracker status: [in_review/in_progress/not present/unchanged]
Manifest provenance: [CURRENT or STALE / ACCEPTED-RISK]
Implemented against: sha256:[hash]
Current manifest: sha256:[hash]

### Files and owners
- [path] — [owner] — [created/modified] — sha256:[post-write hash]

### Acceptance criteria
- [criterion] — [implemented/tested/deferred/blocked] — [evidence]

### Test evidence
- [command] — exit [code] — log sha256:[hash] — [PASS/FAIL/BLOCKED]

### Waivers
- [waiver ID and exact bounded effect, or None]

### Recovery
- [checkpoint path and resume point, or None]
```

For `IMPLEMENTED`, hand off:

```text
Ready for $code-review [exact implementation and test/evidence paths].
After review, run $story-done [story-path]. Only $story-done may mark it Complete.
```

For every other result, give only the remediation or safe resume action. Do not
recommend review or closure.

---

## Non-negotiable rules

- Never overwrite captured manifest provenance to make a stale story look
  current.
- Never treat a waiver as READY.
- Never bypass a hard, missing, Draft, Blocked, or incomplete dependency.
- Never edit a dependency's status.
- Never mutate any file before the exact plan is approved.
- Never allow overlapping write ownership.
- Never accept a changed input under an old plan hash.
- Never report unexecuted or failing tests as passing.
- Never set a story to Complete or Done.
- Never hide partial writes; restore them byte-for-byte or checkpoint them.
