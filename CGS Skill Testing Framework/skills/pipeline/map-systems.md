# Skill Test Spec: $map-systems

## Skill Summary

$map-systems authors or updates design/gdd/systems-index.md only after product
decisions, a canonical in-memory draft, and one hash-bound pre-write review
checkpoint. In full mode, CD-SYSTEMS, TD-SYSTEM-BOUNDARY, and PR-SCOPE review the
same candidate SHA-256 concurrently and read-only. A rejection never triggers an
inline rewrite: it returns stable findings for a fresh author task and leaves the
authoritative index unchanged.

The next and explicit system-selection modes are handoff-only. They read the
index, display one stable system selection and a fresh-task $design-system
command, then stop. The skill never invokes $design-system and never loops across
GDDs. Later GDD approval/index recording belongs to an independent reviewer and
recorder, not either author workflow.

This P0 contract covers MS-001 and MS-002.

---

## Static Assertions

Verified without a fixture.

- [ ] YAML frontmatter contains only name and a non-empty description; name is map-systems
- [ ] The workflow has at least two numbered phase headings
- [ ] COMPLETE, BLOCKED, and PARTIAL result paths are defined
- [ ] The authoritative index path is design/gdd/systems-index.md
- [ ] Every full-mode reviewer receives the exact same candidate_sha256 before the first write
- [ ] Reviewer instructions are explicitly read-only and forbid draft or filesystem mutation
- [ ] REJECT and requested revision both stop with stable findings and zero writes
- [ ] Final authorization and post-write verification bind the exact candidate SHA-256
- [ ] next and explicit selection are declared read-only handoff modes
- [ ] No path invokes, executes, chains, or loops $design-system
- [ ] The workflow stops after a verified index/state changeset
- [ ] Later GDD status recording is assigned to a separate hash-bound recorder
- [ ] Every system row has a persistent `SYS-<canonical-kebab-slug>` identity;
      ordering changes never renumber IDs and collisions block writing

---

## Behavioral Cases

### Case 1: Full-mode happy path reviews before any authoritative write

Fixture:

- design/gdd/game-concept.md exists
- design/gdd/systems-index.md does not exist
- production/review-mode.txt contains full
- the user approves enumeration, dependencies, priorities, and the final
  changeset
- CD-SYSTEMS returns APPROVE
- TD-SYSTEM-BOUNDARY returns APPROVE
- PR-SCOPE returns REALISTIC
- a write-event log and filesystem pre-state are captured

Input:

    $map-systems

Expected behavior:

1. The skill produces one complete canonical draft in memory.
   Every enumeration, dependency/order, and progress row contains the same
   stable System ID for that system, even when the legacy template lacks the
   column.
2. It computes candidate_sha256 from the exact UTF-8 LF bytes.
3. It issues all three reviewer delegations before waiting for any result.
4. Every reviewer receives the same bytes and candidate_sha256 and is read-only.
5. No authoritative or temporary index, review record, or state file is written
   before all active results are collected.
6. The skill previews the index and active-state edits and asks once for
   authorization.
7. Immediately before writing it rechecks candidate_sha256 and any existing-index
   base hash.
8. It writes the exact candidate bytes, verifies the on-disk SHA-256, updates only
   the previewed state fields, reports COMPLETE, returns a fresh-task
   $design-system command, and stops.

Assertions:

- [ ] The first filesystem write occurs after every active review result
- [ ] CD-SYSTEMS, TD-SYSTEM-BOUNDARY, and PR-SCOPE share one candidate_sha256
- [ ] Reviewer outputs contain no file mutation
- [ ] The authorized hash equals the verified on-disk index hash
- [ ] No GDD, review record, sign-off, registry, guide, or unrelated file changes
- [ ] Each proposed system has one unique stable ID and the candidate preserves
      existing IDs byte-for-byte
- [ ] The command is displayed but not invoked
- [ ] Verdict is COMPLETE and the workflow terminates

---

### Case 2: Missing concept blocks without writes

Fixture:

- design/gdd/game-concept.md does not exist
- index and state pre-state hashes are recorded

Input:

    $map-systems

Expected behavior:

1. The skill names design/gdd/game-concept.md as missing.
2. It recommends $brainstorm.
3. It returns BLOCKED and stops.

Assertions:

- [ ] No systems index, draft, state, or review artifact is created
- [ ] No reviewer or downstream workflow is invoked
- [ ] The missing path and recovery command are explicit
- [ ] Verdict is BLOCKED

---

### Case 3: Review REJECT cannot write or self-revise

Fixture:

- a complete candidate exists in memory with candidate_sha256 H1
- production/review-mode.txt contains full
- TD-SYSTEM-BOUNDARY returns REJECT with two blocking findings
- the other active reviewers return pass or concerns
- index, active state, and all candidate output paths have recorded pre-state
  hashes

Input:

    Continue from the pre-write review checkpoint

Expected behavior:

1. The skill collects all active results and applies the strictest verdict.
2. TD findings are normalized as TD-SYSTEM-BOUNDARY-F001 and
   TD-SYSTEM-BOUNDARY-F002, each bound to H1 with location, evidence, impact, and
   required outcome.
3. The reviewer does not edit the candidate or any file.
4. The map-systems author does not revise the candidate in the same task.
5. The skill outputs a fresh-author revision handoff containing H1 and both
   finding IDs, returns BLOCKED — REVIEW REJECTED, and stops.

Assertions:

- [ ] Index and state remain byte-for-byte unchanged
- [ ] No temporary draft, review record, or revised candidate is written
- [ ] Stable finding IDs and candidate_sha256 are present
- [ ] No changeset authorization is requested after rejection
- [ ] No $design-system command is invoked
- [ ] The workflow terminates after the handoff

---

### Case 4: Concerns revision invalidates the reviewed hash

Fixture:

- a full-mode candidate H1 receives no rejection and one CD-SYSTEMS concern
- the user chooses revise rather than accept unchanged
- index and state pre-state hashes are recorded

Input:

    Revise the flagged item

Expected behavior:

1. The skill outputs the stable CD finding and a fresh $map-systems author-task
   handoff.
2. It explains that any revised draft must receive a new SHA-256 and repeat all
   active reviews.
3. It stops without applying the proposed revision or writing files.

Assertions:

- [ ] H1 is never reused to authorize changed bytes
- [ ] Index and state remain byte-for-byte unchanged
- [ ] The same-task reviewer does not become an author
- [ ] The same-task author does not revise after review
- [ ] Verdict is BLOCKED and the workflow terminates

---

### Case 5: Accepted concerns bind unchanged bytes only

Fixture:

- candidate H1 receives only non-blocking concerns
- the user accepts the unchanged draft and later authorizes the complete
  changeset
- immediately before write the candidate still hashes to H1

Input:

    Accept unchanged and apply the proposed changeset

Expected behavior:

1. The skill records that the user accepted the findings against H1.
2. It authorizes and writes only the exact H1 bytes.
3. It verifies the on-disk index still hashes to H1.
4. It reports the accepted concern IDs without claiming the reviewers changed
   the draft.

Assertions:

- [ ] Accepted concern evidence names H1
- [ ] Any byte change before write would block instead
- [ ] On-disk index hash equals H1
- [ ] Verdict is COMPLETE only after verification

---

### Case 6: Stale or concurrent bytes cannot pass the write boundary

Fixture variants:

- A: reviewed candidate is H1 but the re-rendered candidate before write is H2
- B: existing index base hash was B1 but is B2 immediately before replacement
- C: on-disk bytes after write do not hash to the authorized candidate hash

Input:

    Apply the authorized changeset

Expected behavior:

- Variant A returns BLOCKED — STALE DRAFT with zero writes.
- Variant B returns BLOCKED — CONCURRENT INDEX CHANGE with zero writes.
- Variant C returns PARTIAL, names the mismatch, and does not claim COMPLETE.

Assertions:

- [ ] A reviewer verdict cannot authorize a different draft hash
- [ ] Existing-index replacement uses the recorded base pre-state
- [ ] Post-write hash verification is mandatory
- [ ] False COMPLETE is impossible

---

### Case 7: next is handoff-only and bounded to one row

Fixture:

- design/gdd/systems-index.md exists
- the recommended design order contains:
  - SYS-001, Movement, Approved
  - SYS-002, Combat, Not Started
  - SYS-003, Progression, Not Started
- hashes for every workspace file are recorded
- an invocation/subagent event log is enabled

Input:

    $map-systems next

Expected behavior:

1. The skill reads the index only.
2. It resolves SYS-002 as the highest-priority Not Started row.
3. It displays SYS-002, Combat, its status, and:
   Start a fresh task and run $design-system "Combat"
4. It returns COMPLETE — HANDOFF ONLY and stops.

Assertions:

- [ ] Every workspace hash is unchanged
- [ ] Exactly one row is selected
- [ ] No $design-system workflow, agent, or tool is invoked
- [ ] No question asks to continue to SYS-003
- [ ] No GDD or checkpoint is created
- [ ] The handoff explicitly requires a fresh task

---

### Case 8: explicit system selection is also handoff-only

Fixture variants:

- A: SYS-003 uniquely identifies Progression
- B: an exact case-insensitive name uniquely identifies Progression
- C: the name is ambiguous
- D: the requested value is absent

Input:

    $map-systems SYS-003

Expected behavior:

- A and B display the resolved row and one fresh-task $design-system command,
  return COMPLETE — HANDOFF ONLY, and stop.
- C and D return BLOCKED with candidates/evidence and no command execution.

Assertions:

- [ ] Stable ID takes precedence over name matching
- [ ] Ambiguous or missing selection never guesses
- [ ] All variants are read-only
- [ ] No variant invokes GDD authoring

---

### Case 9: index completion stops instead of chaining authoring

Fixture:

- a new or updated index has been written and verified
- the first design-order system is SYS-001 Movement
- the user says yes when shown the next command

Input:

    Yes, start Movement

Expected behavior:

1. The completed map-systems task does not interpret yes as authorization to
   enter GDD authoring.
2. It repeats that GDD authoring must start as a fresh task with
   $design-system "Movement".
3. It performs no further write, invocation, question loop, or row update.

Assertions:

- [ ] The map-systems task has already terminated
- [ ] No GDD authoring runs in the completed task
- [ ] No index progress/status update is inferred
- [ ] No next-system loop exists

---

### Case 10: lean and solo do not misrepresent skipped review

Fixture variants:

- A: review mode is lean
- B: review mode is solo
- the user approves all product decisions and the hash-bound changeset

Input:

    $map-systems

Expected behavior:

1. Both variants note CD-SYSTEMS, TD-SYSTEM-BOUNDARY, and PR-SCOPE as skipped
   with the resolved mode.
2. No reviewer is spawned.
3. The user authorization names candidate_sha256.
4. The workflow never labels the draft independently reviewed.
5. After verified writes it returns COMPLETE and stops.

Assertions:

- [ ] All skip notes name gate and mode
- [ ] No independent-review claim appears
- [ ] Authorization and on-disk verification use the same candidate hash
- [ ] No downstream workflow is invoked

---

## Protocol Compliance

- [ ] Product choices follow Question -> Options -> Decision -> Draft -> Approval
- [ ] Filesystem authorization is one complete, hash-bound changeset
- [ ] Full-mode review is read-only, parallel, pre-write, and single-hash
- [ ] Rejection and revision handoffs terminate with zero writes
- [ ] Author, reviewer, GDD author, and recorder roles remain distinct
- [ ] Selection-only modes return one command and stop
- [ ] The workflow never invokes or loops $design-system
- [ ] COMPLETE requires verified authorized bytes
- [ ] Stable system identity is independent of display/design order; a legacy
      no-ID row is explicitly migrated or remains blocked for downstream use

## Coverage Notes

MS-001 is covered by Cases 1 and 3 through 6. MS-002 is covered by Cases 7
through 9. Cases 2 and 10 retain the essential failure and review-mode behavior
needed to make those P0 boundaries deterministic.

Lower-priority work remains outside this P0 candidate, including stable-ID
migration for legacy indexes, three-way merge/delete rules, final shared gate
ownership, context/input budgets, timeout policy beyond blocking the write, and
repository-wide path/caller synchronization.
