# Skill Test Spec: $dev-story

## Skill Summary

`$dev-story` implements one story without closing it. It independently
revalidates traceability and source provenance, fails closed on hard
dependencies, fixes the complete path/owner/test plan before authorization,
executes the bounded work as a recoverable transaction, and hands a successful
In Review story to `$code-review` and `$story-done`.

A stale control-manifest snapshot is never rewritten to look current. A
structured manifest waiver may authorize an explicit accepted-risk
implementation only when every non-manifest readiness check passes; the captured
hash remains unchanged and the result remains visibly `STALE /
ACCEPTED-RISK`. No waiver can bypass a hard dependency.

---

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only `name` and a non-empty `description`
- [ ] Reads the selected story before delegation or mutation
- [ ] Computes SHA-256 from raw control-manifest bytes
- [ ] Requires exact active TR-ID and Accepted ADR checks
- [ ] Treats the captured Manifest Hash/Source Snapshot as immutable
      `source_manifest_hash` and never rewrites it on the accepted-risk path
- [ ] Manifest waiver requires `waiver_id`, `implemented_against_hash`,
      `current_hash`, and `provenance_status: ACCEPTED-RISK`
- [ ] Hard dependencies have no proceed-anyway branch
- [ ] Soft dependency continuation requires both `soft_dependency: true` and a
      matching structured waiver
- [ ] Complete target paths and unique owners are fixed before approval
- [ ] Every approval is bound to a deterministic plan hash
- [ ] Status mutation happens only after the implementation writer acknowledges
      the approved plan
- [ ] Partial writes are byte-restored or recorded in an explicit checkpoint
- [ ] Success ends at In Review; this skill never writes Complete or Done
- [ ] Successful output hands off to code-review and story-done

---

## Test Cases

### Case 1: Happy path — current provenance, complete dependencies, exact plan

**Fixture:**

- Story is Ready and contains active `TR-light-001`
- Every governing ADR exists with `Status: Accepted`
- The story Manifest Version, Manifest Hash, and Source Snapshot manifest entry
  match the raw current control manifest
- Every dependency file exists with Status Complete
- The planning writer returns exact source and test paths with one owner per path
- Sprint tracker exists and agrees with the story
- User approves the exact plan hash
- Implementation succeeds and every approved test command exits 0

**Expected behavior:**

1. Reads and hashes all authoritative sources and dependencies
2. Produces an exact files/owners/commands preview before any mutation
3. Rehashes every input and target after approval
4. Starts the implementation writer and waits for acknowledgement
5. Synchronizes story and tracker to In Progress
6. Writes only approved owned files
7. Runs and hashes test logs
8. Synchronizes story and tracker to In Review
9. Reports implementation hashes and hands off to code-review/story-done

**Assertions:**

- [ ] No file changes before approval
- [ ] No file has overlapping write owners
- [ ] Test/evidence path is part of the approved plan
- [ ] Story and tracker do not diverge
- [ ] Final story state is In Review, not Complete
- [ ] Evidence includes command, exit code, timestamps, and log hash

---

### Case 2: DS-001 — stale manifest stop path

**Fixture:**

- Current manifest is valid and hashes to `sha256:bbbb...bbbb`
- Story header and Source Snapshot both capture
  `sha256:aaaa...aaaa`
- All non-manifest checks pass
- User chooses Stop

**Expected behavior:**

1. Reports both captured and current hashes
2. Returns BLOCKED
3. Makes no file mutation and starts no implementation writer

**Assertions:**

- [ ] Matching or differing dates do not conceal the hash mismatch
- [ ] Captured provenance is not changed
- [ ] No status, waiver, tracker, or session file is written

---

### Case 3: DS-001 — stale manifest rebase path

Use the Case 2 fixture; user chooses Rebase.

**Expected behavior:**

1. Makes no mutation inside dev-story
2. Routes the story to its owning update workflow
3. Requires refreshed header hash, Source Snapshot, affected requirements, and a
   new final story-readiness verdict before dev-story may rerun

**Assertions:**

- [ ] Dev-story does not rewrite Manifest Version or any provenance field
- [ ] Rebase is not presented as completed by changing only a date
- [ ] Implementation does not begin under the old plan

---

### Case 4: DS-001 — structured accepted-risk path preserves provenance

**Fixture:**

- Same stale hashes as Case 2
- Header and Source Snapshot carry the same well-formed captured hash
- Registry/TR, ADR, criteria, scope, and dependencies all pass
- User explicitly accepts a manifest waiver with stable ID `MW-104`
- Current manifest does not change between approval and mutation

**Expected behavior:**

1. Adds the structured waiver to the exact file plan
2. Records:
   - `waiver_id: MW-104`
   - `implemented_against_hash: sha256:aaaa...aaaa`
   - `current_hash: sha256:bbbb...bbbb`
   - `provenance_status: ACCEPTED-RISK`
3. Leaves Manifest Version, Manifest Hash, and Source Snapshot unchanged
4. Labels previews, checkpoints, and final output `STALE / ACCEPTED-RISK`
5. Never claims the story received a READY verdict

**Assertions:**

- [ ] Old and current hashes remain distinguishable
- [ ] Free text or Manifest-Note alone cannot authorize the branch
- [ ] Waiver cannot hide any other readiness gap
- [ ] The captured source hash is never replaced by current_hash
- [ ] Success may reach In Review but remains accepted-risk provenance

---

### Case 5: DS-001 — waiver invalidated by a second manifest change

**Fixture:**

- User approved Case 4 against current hash B
- Immediately before mutation the current manifest hashes to C

**Expected behavior:**

1. Compare-and-swap preflight detects the change
2. Makes no mutation under the approved plan
3. Invalidates the waiver/plan and returns to provenance validation

**Assertions:**

- [ ] Hash C is never accepted by a waiver naming hash B
- [ ] No file is changed under the stale plan hash

---

### Case 6: DS-002 — dependency state/type matrix

Run every row with unrelated checks passing.

| Variant | Dependency declaration | Observed state | Waiver | Expected |
|---|---|---|---|---|
| 6a | type omitted | Complete | none | PASS |
| 6b | hard | Ready | none | BLOCKED |
| 6c | hard | Draft | user says proceed | BLOCKED |
| 6d | hard | Blocked | structured waiver | BLOCKED |
| 6e | hard | missing | free text | BLOCKED |
| 6f | `soft_dependency: true` | In Progress | none | BLOCKED |
| 6g | `soft_dependency: true` | In Progress | valid matching waiver | ACCEPTED-RISK |
| 6h | `soft_dependency: true` | Draft | valid matching waiver | ACCEPTED-RISK |
| 6i | `soft_dependency: true` | missing | valid matching waiver naming MISSING | ACCEPTED-RISK |
| 6j | `soft_dependency: true` | Blocked | waiver names Ready | BLOCKED |

**Assertions:**

- [ ] Dependency type defaults to hard
- [ ] No hard-dependency row can be overridden
- [ ] Soft flag without a waiver cannot proceed
- [ ] Waiver ID, dependency ID, and observed status must match fresh evidence
- [ ] No branch edits or completes the dependency story
- [ ] BLOCKED occurs before implementation planning or status mutation

---

### Case 7: DS-003 — plan must close the write set and ownership

**Fixture:**

- Readiness and dependency checks pass
- Planner initially returns `src/light/**`, an exact test path, and two writers
  for one source file

**Expected behavior:**

1. Rejects the plan before authorization
2. Requires exact paths instead of the glob
3. Requires one unique writer per path
4. Includes story, optional tracker, active session, and failure-only checkpoint
   paths in the preview
5. Computes plan hash only after every path, owner, baseline hash, criterion
   mapping, and command is resolved

**Assertions:**

- [ ] A directory, glob, related-files label, or TBD path cannot be approved
- [ ] Engine specialist is read-only
- [ ] Config/Data still receives one implementation writer
- [ ] Every acceptance criterion maps to implementation and evidence
- [ ] No status or Last Updated field changes during planning

---

### Case 8: DS-003 — authorization is plan-hash bound

**Fixture:**

- User approved plan P1
- The writer later discovers one additional schema file is required

**Expected behavior:**

1. Stops before modifying the unplanned file
2. Does not interpret P1 approval as permission for the new path
3. Rebuilds the complete plan with fresh hashes and requests approval for P2

**Assertions:**

- [ ] No per-file prompt occurs within unchanged P1
- [ ] Material path expansion always invalidates P1
- [ ] P2 includes the full changeset, not only the added file

---

### Case 9: DS-003 — writer spawn failure is side-effect free

**Fixture:**

- User approved a complete plan
- Primary writer fails to start or does not acknowledge exact ownership

**Expected behavior:**

1. No story/tracker/source/test status mutation has occurred
2. Returns FAILED with the spawn/acknowledgement reason
3. Leaves baseline hashes unchanged

**Assertions:**

- [ ] Story is not prematurely set In Progress
- [ ] Tracker is not prematurely set in_progress
- [ ] No success handoff is emitted

---

### Case 10: DS-003 — failure after partial business writes

**Fixture:**

- Writer acknowledged and synchronized In Progress status was applied
- One approved source file was changed
- Test creation then fails
- Restoring every changed path byte-for-byte is not safe

**Expected behavior:**

1. Keeps story and tracker synchronized at In Progress
2. Writes only the pre-authorized failure checkpoint
3. Checkpoint contains plan/source/baseline/current hashes, planned and actual
   write sets, owner, criteria progress, evidence/error, and resume point
4. Returns PARTIAL and does not hand off to review

**Assertions:**

- [ ] Partial work is not described as rolled back
- [ ] Story is not moved to In Review or Complete
- [ ] Checkpoint makes the partial state reconstructable

---

### Case 11: DS-003 — safe rollback verifies byte identity

Use Case 10, but every affected file can be restored safely.

**Expected behavior:**

1. Restores every target from captured bytes
2. Verifies each restored raw SHA-256 equals its baseline
3. Restores both status projections together
4. Returns FAILED, not PARTIAL

**Assertions:**

- [ ] "Rolled back" is used only after all hash comparisons pass
- [ ] A failed one-sided status restore produces a checkpoint instead

---

### Case 12: Proposed or missing ADR blocks implementation

**Fixture:**

- Story references one ADR with `Status: Proposed`
- Other checks pass

**Expected behavior:**

1. Names the blocking ADR and observed status
2. Routes resolution to the ADR owner
3. Leaves story/tracker unchanged and starts no implementation writer

**Assertions:**

- [ ] No accepted-risk or generic proceed option is offered
- [ ] Uncovered architecture is never decided inside dev-story

---

### Case 13: Ambiguous acceptance criterion is clarified before planning

**Fixture:**

- Non-Visual/Feel story contains "movement feels responsive"
- Other checks pass

**Expected behavior:**

1. Surfaces the exact ambiguous criterion
2. Requests a measurable restatement
3. Includes the approved story-text edit in the complete file plan
4. Uses the restated criterion in implementation and test mapping

**Assertions:**

- [ ] The skill does not guess or plan against the vague text
- [ ] Clarification does not mutate the story before plan approval

---

### Case 14: No argument uses session state with confirmation

**Fixture:**

- Invocation has no story path
- `production/session-state/active.md` names an In Progress story

**Expected behavior:**

1. Reads session state
2. Confirms "Continuing work on [story title] — is that correct?"
3. Reads the confirmed story before delegation

**Assertions:**

- [ ] Active story is not silently assumed
- [ ] Missing active reference causes a direct story-selection question

---

### Case 15: Tracker revision/hash stays synchronized across lifecycle writes

- [ ] Invalid sprint identity, plan revision, story-set hash, or updated_at blocks mutation
- [ ] Ready→In Progress and In Progress→In Review are story/tracker CAS pairs
- [ ] Each story-byte change recomputes sorted `ID<TAB>path<TAB>raw-hash` story_set_hash
- [ ] plan_revision is preserved and updated_at is timezone-qualified
- [ ] Partial recovery keeps In Progress, a current tracker hash, and exact checkpoint hashes

## Protocol Compliance

- [ ] Uses current raw source hashes, not copied labels
- [ ] Does not convert story-readiness NEEDS WORK/BLOCKED into READY
- [ ] Structured manifest accepted risk is the only narrow non-READY
      implementation branch
- [ ] Never bypasses a registry, TR, ADR, architecture, ambiguity, or hard
      dependency blocker
- [ ] Uses one complete authorization for a closed plan
- [ ] Uses compare-and-swap checks before every transaction
- [ ] Records deterministic test evidence
- [ ] Keeps story/tracker states synchronized
- [ ] Ends successful work at In Review with exact next-step paths
- [ ] Never marks a story Complete

---

## Coverage Notes

These cases fully exercise DS-001, DS-002, and DS-003. The candidate also states
the existing implementation-only lifecycle explicitly so the P0 transaction does
not manufacture a Complete status.

Cross-skill integration remains required before production rollout:

- `$story-readiness` intentionally keeps a manifest-waived story non-ready; its
  report must never call the dev-story waiver branch READY.
- `$create-stories` must emit active TR and full manifest Source Snapshot fields
  for the ordinary current-provenance path.
- `$code-review` and `$story-done` must consume plan/source/test hashes and
  preserve accepted-risk provenance.
- Sprint/status readers must recognize synchronized In Review and recovery
  checkpoints.
