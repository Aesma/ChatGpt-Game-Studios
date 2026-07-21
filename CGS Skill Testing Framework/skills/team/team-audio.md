# Skill Test Spec: $team-audio

## Skill Summary

`$team-audio` creates or revises one authoritative audio specification at
`design/audio/audio-[artifact-id].md`. Audio, sound, accessibility, technical,
engine, QA, and review agents are bounded read-only proposal producers. Every
proposal has one destination; exactly one transaction writer may write the
specification and recovery checkpoint.

The workflow never implements code, tests, middleware, or assets. A current
raw-hash-bound independent review and final user acceptance are required for
`SPEC COMPLETE`. Missing engine validation may yield `SPEC COMPLETE — ENGINE
VALIDATION DEFERRED`, which is explicitly not implementation-ready.

---

## Static Assertions

- [ ] YAML frontmatter contains only `name` and non-empty `description`; `name`
      matches the skill directory
- [ ] Has at least two numbered phase headings
- [ ] Declares SPEC COMPLETE, ENGINE VALIDATION DEFERRED, PARTIAL, ACCEPTED RISK,
      and BLOCKED outcomes
- [ ] Canonical specification path is only
      `design/audio/audio-[artifact-id].md`
- [ ] No positive path spawns gameplay-programmer or writes/reviews code or tests
- [ ] Implementation requires approved spec hash, current engine validation,
      Accepted ADRs, a ready story, and separate `$dev-story` authorization
- [ ] All specialists/reviewers are read-only and exactly one transaction writer
      owns the exact spec/checkpoint paths
- [ ] Proposal schema includes stable ID, evidence/source hashes, one destination,
      decision, owner, acceptance, dependencies, and status
- [ ] Verbatim/all-output aggregation is forbidden
- [ ] Approval is bound to exact paths, operations, owner, hashes, scope, and a
      deterministic plan hash
- [ ] Concurrency, deadline, retry/follow-up, timeout, PARTIAL, rollback,
      checkpoint, and raw-hash resume rules are bounded
- [ ] Critical audio-only gameplay information is a non-waivable blocker
- [ ] QA/playback proposals are PLANNED and never represented as executed evidence
- [ ] Metadata says spec-only/no implementation and matches the canonical boundary
- [ ] A next-step handoff never directly invokes implementation

---

## Director Gate Checks

No implementation or generic director gate runs. The independent audio-spec
review is a read-only, current-hash-bound profile. The author and transaction
writer cannot review their own artifact.

---

## Test Cases

### Case 1: Happy path — reviewed audio specification reaches SPEC COMPLETE

**Fixture:**
- Input is `combat`
- Matching feature GDD, sound bible, accessibility requirements, technical
  preferences, engine reference, and first-hop dependencies fit the context
  budget
- Specification and checkpoint targets are absent
- All required proposal agents complete within their deadlines
- Accessibility returns zero BLOCKING findings
- Engine specialist validates destination-tagged technical proposals
- User resolves genuine product choices
- Exact two-path plan P1 is approved
- One writer writes the approved bytes and verifies raw hash H1
- Fresh independent audio review returns zero BLOCKING findings against H1
- qa-tester returns a PLANNED matrix bound to H1
- User accepts the H1 evidence packet

**Input:** `$team-audio combat`

**Expected behavior:**
1. Builds and hashes a bounded context manifest
2. Collects only structured read-only proposals
3. Routes every proposal to exactly one destination
4. Reduces only AUDIO SPEC material into the draft
5. Previews and obtains one exact plan-hash authorization
6. Uses one writer for the exact spec/checkpoint paths
7. Runs independent review and planned-QA generation against H1
8. Records final acceptance and matching checkpoint state
9. Returns `SPEC COMPLETE`

**Assertions:**
- [ ] Only `design/audio/audio-combat.md` and the authorized checkpoint may change
- [ ] `design/gdd/audio-combat.md` is neither read as authority nor written
- [ ] No code, test, ADR, budget, QA-plan, import-setting, or asset path changes
- [ ] Reviewer differs from author/writer
- [ ] Review, QA-plan proposal, user acceptance, and checkpoint all name H1
- [ ] Routine phase transitions do not request approval

---

### Case 2: TAD-001 — specification freezes before any implementation

**Fixture:**
- Product proposals are still being discussed and no specification hash is
  approved
- A proposal suggests an audio manager, event wiring, and adaptive-music tests
- A delegation spy records roles and write attempts

**Expected behavior:**
1. Routes implementation suggestions to BACKLOG / STORY
2. Does not spawn gameplay-programmer
3. Writes no source or test file
4. Does not invoke `$dev-story`
5. States the independent future prerequisites: accepted current spec hash,
   current engine validation, Accepted ADR, ready story with testable criteria

**Assertions:**
- [ ] Gameplay-programmer spawn count is zero
- [ ] `src/` and `tests/` hashes remain unchanged
- [ ] Discussion approval cannot substitute for approved specification hash
- [ ] Final compilation cannot retroactively authorize code
- [ ] SPEC COMPLETE means specification only, not implementation or QA completion

---

### Case 3: TAD-002 — exact authorization cannot cover unknown outputs

**Fixture:**
- Read-only proposals are complete
- Plan P1 names exact spec/checkpoint paths, one writer, create operations,
  ABSENT baselines, context/draft hashes, destination ledger, and write conditions
- User approves P1

Run these variants:

| Variant | Event | Expected |
|---|---|---|
| 3a | writer requests an implementation file | stop; P1 does not cover it |
| 3b | writer requests an ADR, QA plan, budget, or asset path | stop; P1 does not cover it |
| 3c | target operation changes create → revise | invalidate P1 |
| 3d | writer identity changes | invalidate P1 |
| 3e | source/target hash changes before write | cancel P1 with zero mutation |
| 3f | unchanged P1 writes both exact paths | no per-file re-prompt |

**Assertions:**
- [ ] No wildcard, directory, related-file, or TBD authorization is valid
- [ ] Path/owner/operation/material-scope expansion requires a complete new plan
- [ ] Approval is deterministic-plan-hash-bound
- [ ] Compare-and-swap uses current raw hashes
- [ ] Implementation files never enter the design changeset

---

### Case 4: TAD-003 — proposal agents cannot race the single writer

**Fixture:**
- Sound designer, accessibility specialist, technical artist, and engine
  specialist run in bounded parallel batches
- Two proposal agents attempt to edit the specification
- The named writer has not yet received authorization

**Expected behavior:**
1. Rejects both write attempts
2. Accepts only schema-valid read-only proposals
3. Resolves duplicate/conflicting proposal IDs before reduction
4. Allows only the approved transaction writer to write after P1 approval

**Assertions:**
- [ ] Parallel agents have zero write ownership
- [ ] Exactly one writer owns both exact targets
- [ ] Author and reviewer cannot silently become writers
- [ ] Overlapping ownership stops and escalates; last-writer-wins is forbidden
- [ ] The orchestrator does not broaden ownership during recovery

---

### Case 5: TAD-004 — technical, QA, asset, and backlog outputs stay separate

**Fixture:**
- Agents return:
  - sonic rules/event contracts/adaptive behavior → AUDIO SPEC
  - detailed production asset instructions → AUDIO ASSET BRIEF
  - Wwise/FMOD/native choice, bus graph, engine nodes → TECHNICAL ADR / SPEC
  - voice/memory/CPU/streaming limits → PERFORMANCE BUDGET
  - trigger/playback test matrix → QA PLAN
  - manager/event wiring tasks → BACKLOG / STORY
  - review discussion → REVIEW ONLY

**Expected behavior:**
1. Records every proposal ID once with exactly one destination
2. Passes only AUDIO SPEC constraints to the reducer
3. References external proposal IDs without copying their content
4. Writes none of the external destinations

**Assertions:**
- [ ] Final spec contains no middleware selection, concrete bus graph, engine
      classes, performance table, code paths, unit tests, QA results, or asset
      production instructions
- [ ] No `combine all team outputs` or verbatim merge remains
- [ ] External destination owners and acceptance conditions are preserved
- [ ] Technical conflicts remain open for the technical owner; reducer does not guess
- [ ] Audio spec remains authority only for player-facing audio behavior

---

### Case 6: Critical accessibility gap is non-waivable

**Fixture:**
- `EnemyNearbyAlert` communicates an off-screen threat only through spatial audio
- Reviewer creates `AXA-stealth-001` as BLOCKING

Run these variants:

| Variant | User response | Expected |
|---|---|---|
| 6a | asks to document and proceed | refuse; remain BLOCKED |
| 6b | selects a visual or haptic equivalent | one bounded author revision and one verification review |
| 6c | same blocker remains on second observation | BLOCKED; no third loop |
| 6d | accepts a non-blocking sensitivity risk | structured risk record; ACCEPTED RISK / NOT APPROVED |

**Assertions:**
- [ ] Event ID, evidence, requirement, owner, and closure condition are explicit
- [ ] No skip or generic user authorization bypasses BLOCKING
- [ ] Stable finding ID survives revision/re-review
- [ ] Implementation and SPEC COMPLETE are impossible while it remains open
- [ ] Accepted risk includes owner/deadline/approved_by/approved_at

---

### Case 7: Bounded concurrency, timeout, partial state, and checkpoint

Run these variants:

| Variant | Event | Expected |
|---|---|---|
| 7a | required agent reaches 10-minute deadline | TIMED OUT; PARTIAL, not COMPLETE |
| 7b | one narrowed follow-up also fails | no further retry/replacement |
| 7c | spec write partially succeeds and byte restoration is unsafe | preserve actual bytes, persist PARTIAL checkpoint |
| 7d | all changed bytes restore and baseline hashes match | rollback may be reported |
| 7e | checkpoint write fails | print RECOVERY CHECKPOINT NOT PERSISTED and deny safe resume |
| 7f | resume hashes match | reuse only matching input/output-hash results |
| 7g | resume hash differs | stop/revalidate; do not duplicate writes or delegation |

**Assertions:**
- [ ] At most three agents are live
- [ ] Every agent has an ISO deadline
- [ ] PARTIAL report preserves completed proposal IDs and explicit gaps
- [ ] Checkpoint includes plan/context/source/baseline/current/draft hashes,
      decisions, findings, agent states/deadlines, engine state, write sets, and
      safe resume point
- [ ] Partial artifacts are never implementation-ready

---

### Case 8: Engine not configured yields explicit deferred completion

**Fixture:**
- Technical preferences show no configured engine
- All engine-neutral product/specification checks pass
- User accepts the current reviewed spec hash H1

**Expected behavior:**
1. Does not spawn any engine specialist
2. Does not guess middleware or engine component patterns
3. Records the configuration source hash and exact revalidation trigger
4. May return `SPEC COMPLETE — ENGINE VALIDATION DEFERRED`
5. Does not hand off to implementation

**Assertions:**
- [ ] technical-artist remains read-only and engine-neutral
- [ ] Deferred state is visible in spec, checkpoint, and report
- [ ] Selecting/configuring an engine makes prior technical validation stale
- [ ] Deferred completion is distinct from SPEC COMPLETE
- [ ] `$dev-story` remains forbidden until current engine validation exists

---

### Case 9: QA and playback evidence are never fabricated

**Fixture:**
- qa-tester proposes six validation cases
- No implementation, audio asset, build, or listening session exists

**Expected behavior:**
1. Reports cases as PLANNED
2. Reports `QA NOT RUN` and `PLAYBACK NOT RUN`
3. Writes no QA plan
4. Claims no pass, coverage, playback quality, mix approval, or accessibility
   playback result

**Assertions:**
- [ ] Agent prose is not execution evidence
- [ ] Filenames, unplayed waveforms, or missing logs do not count as playback
- [ ] Executed evidence would require spec/build/asset hashes, protocol,
      environment/device/settings, timestamps/duration, result/observer, and raw
      evidence hash
- [ ] No command, session, PASS, timestamp, or hash is invented
- [ ] QA proposal is bound to the current spec hash and becomes stale on change

---

### Case 10: Missing or invalid artifact ID fails before reads

**Fixture:**
- Any project state

Run empty input, path traversal, drive prefix, control-character, and ambiguous
slug variants.

**Expected behavior:**
1. Prints required argument and safe examples
2. Stops before project-file reads or delegation
3. Performs no write and emits no verdict

**Assertions:**
- [ ] No agent is spawned
- [ ] No GDD, asset, target, or checkpoint is read
- [ ] Invalid ID cannot escape `design/audio/`
- [ ] Existing spec cannot be overwritten under create mode

---

### Case 11: Context loading and references remain bounded

**Fixture:**
- More than 20 relevant candidates or 250 KiB exist
- Asset lists contain cyclic references
- The sound bible is absent

**Expected behavior:**
1. Stops after one explicit reference hop
2. Surfaces a prioritization choice instead of silent truncation
3. Records exact loaded/omitted paths and raw hashes
4. Tells audio-director the sound bible is absent instead of inventing it
5. Keeps full asset-tree content out of agent prompts

**Assertions:**
- [ ] Context manifest is deterministic and hashable
- [ ] Cycles do not recurse
- [ ] Missing sound bible is a reported dependency/recommendation
- [ ] Agent prompts contain only relevant excerpts and structured predecessors

---

### Case 12: Review and acceptance are current-hash-bound

**Fixture:**
- Audio reviewer approved H1
- Specification later changes and now hashes to H2

**Expected behavior:**
1. Marks H1 review, QA proposal, and acceptance stale
2. Requires a new plan for a material revision and fresh evidence on H2
3. Does not retain SPEC COMPLETE for H2
4. Does not authorize implementation

**Assertions:**
- [ ] Author/writer cannot self-review
- [ ] Reviewer writes no file
- [ ] One verification re-review is the maximum after a blocker revision
- [ ] Checkpoint COMPLETE state must name current hash and acceptance
- [ ] Filename existence or prior prose approval cannot substitute for hashes

---

## Protocol Compliance

- [ ] Product decisions and one exact write authorization are the only routine
      user gates
- [ ] All proposal/review agents are read-only
- [ ] Exactly one writer owns specification and checkpoint
- [ ] Parallel batches respect three-agent and 10-minute limits
- [ ] Destination routing precedes reduction
- [ ] BLOCKING accessibility/review findings cannot be waived
- [ ] PARTIAL/timeout/recovery state is reconstructable
- [ ] Review, QA proposal, and user acceptance bind to current raw hash
- [ ] QA/playback execution is never fabricated
- [ ] No implementation, test, ADR, budget, QA plan, or audio asset is written
- [ ] Canonical path is `design/audio/audio-[artifact-id].md` only
- [ ] Verdict is one of the five declared outcomes

---

## Coverage Notes

The shared workflow guide and catalog remain unchanged because they are outside
this remediation boundary. Catalog last-test fields remain empty: these are
static candidate checks, not executed workflow results.

Future rollout must align the workflow guide and implementation/story consumers
with the canonical audio-spec path and approved raw-hash prerequisite.
