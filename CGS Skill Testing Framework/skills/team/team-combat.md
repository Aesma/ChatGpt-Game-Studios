# Skill Test Spec: $team-combat

## Skill Summary

`$team-combat` implements one combat story only after an independent hash-bound
GDD approval, Accepted governing ADRs, and a current final READY story are
proven. Planning is read-only. Before any writer starts, the workflow freezes
interfaces and obtains one approval for an exact path/operation/owner/base-hash
manifest. Only disjoint manifest owners may write concurrently; shared paths
have one integration owner. Timeouts, late results, partial work, checkpoint
recovery, and tests use explicit state. COMPLETE requires actual current test
evidence, never a proposed or narrated result.

## Static Assertions

- [ ] Frontmatter contains `name: team-combat` and a non-empty description
- [ ] Implementation invocation requires a concrete story, design-review
      evidence, readiness evidence, and approved GDD SHA-256
- [ ] GDD/ADR/story/approval artifacts are never authored or promoted by this skill
- [ ] Zero mutations are permitted before exact manifest approval
- [ ] Manifest rows contain path, operation, sole owner, and base hash/ABSENT
- [ ] Delegation and retries do not enlarge file authorization
- [ ] Every writable path has one owner; shared paths belong only to the named
      integration owner
- [ ] Concurrency is capped and limited to disjoint frozen-interface tasks
- [ ] Per-task deadline, cancellation, one-retry maximum, and late-result
      quarantine are defined
- [ ] Checkpoint includes hashes, manifest, task state, deadlines, and next step
- [ ] Test results require actual commands, exit codes, counts, environment,
      evidence paths, and evidence hashes
- [ ] Verdicts include COMPLETE, NEEDS WORK, PARTIAL, and BLOCKED
- [ ] Orchestrator is read-only while authorized subagents may write only exact
      approved manifest rows
- [ ] Metadata describes implementation side effects and prerequisites; it does
      not claim the whole workflow is read-only

---

## Test Cases

### Case 1: Approved-input gate blocks free text and self-approved design

**Fixture variants:**

1. input is only `parry and riposte system`;
2. `--approved-gdd-hash` is missing;
3. review evidence is advisory, partial, not independent, or names another hash;
4. a governing ADR is Proposed;
5. story status says Ready but final readiness evidence is missing/stale;
6. acceptance criteria or test-evidence destinations are incomplete.

**Input examples:**

```text
$team-combat parry and riposte system
$team-combat production/epics/combat/story-001-parry.md --design-review review.md
```

**Expected behavior:**

1. The workflow identifies every missing or stale prerequisite.
2. It reports `BLOCKED — APPROVED INPUTS NOT PROVEN`.
3. It does not create/update a GDD, ADR, story, review record, or implementation
   file.
4. It spawns no implementation writer.
5. It does not treat user confirmation, story status text, or Accepted Risk as
   formal approval.

**Assertions:**

- [ ] Zero mutations
- [ ] Zero implementation writer launches
- [ ] Current and expected paths/hashes/statuses are reported
- [ ] No programmer is asked to invent missing product rules
- [ ] Upstream workflows are handoffs only and are not auto-invoked

---

### Case 2: Valid approved inputs produce read-only planning only

**Fixture:**

- the GDD's current raw SHA-256 equals `--approved-gdd-hash`
- independent review evidence says APPROVED for that exact path/hash
- every governing ADR is Accepted
- final readiness evidence says READY for the exact current story hash
- acceptance criteria, control-manifest snapshot, QA plan, engine, and pinned
  version are current

**Input:**

```text
$team-combat production/epics/combat/story-001-parry.md \
  --design-review design/gdd/reviews/parry-review.md \
  --readiness-evidence production/qa/readiness/parry.md \
  --approved-gdd-hash sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

**Expected behavior:**

1. All current raw-byte hashes are recorded.
2. Requirements, implementation, engine, and QA planners return proposals only.
3. A frozen interface contract and exact file manifest are produced.
4. No file is changed before manifest approval.

**Assertions:**

- [ ] Input snapshot names story/GDD/ADR/review/readiness hashes
- [ ] Planning agents have an explicit no-write contract
- [ ] Interface disagreements block implementation
- [ ] Mutation audit remains empty through manifest presentation

---

### Case 3: Exact manifest authorization cannot expand

**Fixture:**

- planning proposes three exact files: one gameplay file, one test file, and
  `production/session-state/active.md`
- current bytes/base hashes are known
- user approves the canonical manifest hash
- a writer later requests a fourth file

**Expected behavior:**

1. Manifest rows show exact path, create/update operation, sole owner, base
   SHA-256/ABSENT, purpose, and acceptance criteria.
2. The fourth path receives `SCOPE_CHANGE_REQUEST` and is not written.
3. Execution stops before dependent work.
4. A revised complete manifest requires a new user approval.

**Assertions:**

- [ ] No globs or directory-wide authorization
- [ ] Approval binds exact manifest and input/interface hashes
- [ ] New path, operation, owner, or base hash invalidates authorization
- [ ] Delegated agents do not inherit broader write authority
- [ ] Unauthorized scope is never approved retroactively

---

### Case 4: Overlapping writers are not launched concurrently

**Fixture:**

- gameplay and AI proposals both request `src/combat/combat_controller.*`
- gameplay owns a separate core file
- AI owns a separate behavior file
- interface contract is frozen

**Expected behavior:**

1. Ownership analysis detects the shared requested path.
2. The shared path is assigned only to the integration owner.
3. Gameplay and AI may concurrently write only their disjoint private paths.
4. Both return read-only proposals for the shared path.
5. If unique ownership cannot be resolved before approval, verdict is BLOCKED.

**Assertions:**

- [ ] Exactly one manifest owner for every path
- [ ] No overlapping write sets in a concurrent batch
- [ ] Real dependencies are serialized
- [ ] Workspace audit detects a non-owner shared-file write as BLOCKED

---

### Case 5: Integration has one explicit owner and hash guard

**Fixture:**

- all required private-domain tasks are COMPLETE
- `lead-programmer` is the declared integration owner
- shared files and their approved base hashes are listed in the manifest
- domain agents provide proposals for shared wiring

**Expected behavior:**

1. Only `lead-programmer` receives shared manifest rows.
2. The integration owner rechecks each base hash before writing.
3. It applies compatible proposals in dependency order.
4. Domain writers and orchestrator do not touch shared files.
5. Every integrated path receives a verified post hash.

**Assertions:**

- [ ] Integration owner is selected before authorization
- [ ] Shared paths are exclusive to that owner
- [ ] Base mismatch produces zero writes to the conflicting path and BLOCKED
- [ ] Integration never begins after a required partial/timeout/late result
- [ ] Integration result lists pre/post hashes

---

### Case 6: Bounded parallel batch succeeds

**Fixture:**

- gameplay, AI, VFX, and audio are explicit story dependencies
- each has a disjoint approved path set
- all consume the same frozen input/interface hashes
- configured subagent limit is at least four

**Expected behavior:**

1. Four stable task IDs, deadlines, cancellation tokens, and manifest subsets are
   created.
2. All four tasks in the eligible batch are launched before awaiting results.
3. No task consumes another task's output.
4. The workflow waits for the complete batch before integration.
5. Returned path hashes and ownership are audited.

**Assertions:**

- [ ] Concurrency never exceeds four or the repository limit
- [ ] Only disjoint tasks share a batch
- [ ] Result schema includes input/interface and pre/post hashes
- [ ] Integration waits for all required COMPLETE audited results

---

### Case 7: Timeout, cancellation, late result, and partial report

**Fixture:**

- gameplay completes
- VFX exceeds its approved deadline
- cancellation is issued
- VFX returns a patch after cancellation
- retry safety cannot be proven

**Expected behavior:**

1. VFX is marked TIMED_OUT and CANCELED.
2. The late patch is marked LATE and quarantined.
3. It is not written, merged, integrated, or treated as evidence.
4. Gameplay's verified result appears in a partial report.
5. Dependent integration does not start.
6. Overall verdict is PARTIAL or BLOCKED, never COMPLETE.

**Assertions:**

- [ ] At most one retry and only after safe path-state verification
- [ ] No concurrent attempts own the same path
- [ ] Late result cannot update checkpoint post hashes
- [ ] Completed independent work is not discarded
- [ ] Timeout cannot be accepted as risk into COMPLETE

---

### Case 8: Unauthorized writer mutation fails closed

**Fixture:**

- AI owns `src/ai/parry_behavior.*`
- during execution it also changes a shared combat controller
- the controller is owned by the integration owner

**Expected behavior:**

1. Post-batch workspace inventory detects both changes.
2. The AI result is rejected as scope/ownership violation.
3. Exact unauthorized path, writer, and observed hash are reported.
4. Integration and dependent testing stop.
5. Overall verdict is BLOCKED.

**Assertions:**

- [ ] Unauthorized mutation is not silently retained
- [ ] User cannot retroactively waive it into the old manifest
- [ ] No other agent overwrites the path to conceal the violation
- [ ] Partial report retains only verified in-scope results

---

### Case 9: Checkpoint resume is hash-bound and idempotent

**Fixture variants:**

- a valid checkpoint records Phase 4 complete gameplay post hashes and VFX still
  PLANNED;
- a checkpoint's story or manifest hash differs from current bytes;
- a checkpoint names a canceled attempt that later returned.

**Expected behavior:**

1. Valid resume verifies run/input/interface/manifest/file/evidence hashes.
2. It does not rerun a COMPLETE task whose post hashes still match.
3. It continues only the next safe incomplete task.
4. Stale checkpoint state returns BLOCKED.
5. Canceled/superseded/late results are never revived.
6. Only the integration owner writes the approved checkpoint path.

**Assertions:**

- [ ] Resume is idempotent
- [ ] Checkpoint includes task deadlines/retries/cancellation state
- [ ] Repeated checkpoint updates follow one verified post-hash-to-next-base chain
- [ ] Path or owner changes require revised manifest approval
- [ ] Orchestrator does not edit the checkpoint

---

### Case 10: Tests cannot be claimed without execution evidence

**Fixture variants:**

1. qa-tester only inspects code and proposes a command;
2. command runs but evidence log is missing;
3. evidence was generated for different integration post hashes;
4. tests run with failures/skips/not-run criteria;
5. tests run successfully and record all required fields.

**Expected behavior:**

1. Proposed or narrated commands are reported NOT RUN.
2. Missing/stale evidence cannot support a passing criterion.
3. Actual execution records command, working directory, engine/platform/version,
   timestamps, exit code, counts, integrated hashes, evidence path/hash, and
   acceptance-criteria mapping.
4. Performance is unproven without numeric budget, measurement command, and
   captured result.
5. COMPLETE is possible only for variant 5 when all other gates pass.

**Assertions:**

- [ ] No fabricated `passed`, `validated`, or performance claim
- [ ] Evidence is bound to current integrated bytes
- [ ] Failures produce NEEDS WORK or BLOCKED
- [ ] Partial/skipped/not-run required tests prevent COMPLETE
- [ ] Evidence writer stays inside exact manifest paths

---

### Case 11: Happy path — approved story to verified combat implementation

**Fixture:**

- every Phase 0 input is current and approved
- planners freeze one consistent engine-validated interface
- user approves a complete non-overlapping manifest
- test contract is materialized before implementation
- every required domain writer and integration owner completes on time
- all mutation audits pass
- actual build/tests pass and evidence covers every acceptance criterion

**Expected behavior:**

1. Input and interface hashes are frozen.
2. Exact manifest and integration owner are approved once.
3. Eligible domain writers execute in bounded disjoint batches.
4. The sole integration owner wires shared files.
5. Independent QA runs the approved commands and hashes evidence.
6. Final revalidation finds no stale input, scope violation, timeout, blocker, or
   uncovered criterion.
7. Verdict is COMPLETE.

**Assertions:**

- [ ] No design/ADR/story lifecycle file changed
- [ ] Every changed file has approved owner and pre/post hashes
- [ ] Every acceptance criterion maps to current passing evidence
- [ ] Final report names commands, evidence hashes, manifest, checkpoint, and
      integration owner
- [ ] COMPLETE is deterministic rather than agent self-report

---

### Case 12: No argument

**Input:** `$team-combat`

**Expected behavior:**

1. The workflow prints implementation usage with all approval arguments.
2. It explains that free text is insufficient.
3. It reads no project files and spawns no agent.
4. It performs no write and emits no success verdict.

**Assertions:**

- [ ] Clear story-path usage
- [ ] Zero file reads beyond invocation parsing
- [ ] Zero agents and mutations
- [ ] No silent story selection

---

## Verdict Matrix

| Condition | Maximum verdict |
|---|---|
| Missing/stale approval, ADR, READY evidence, engine, or manifest | BLOCKED |
| Unauthorized/overlapping write or integration conflict | BLOCKED |
| Required task partial, timed out, canceled, late, skipped, or unavailable | PARTIAL |
| Integrated code has current failing tests/non-blocking defects | NEEDS WORK |
| Required test/evidence missing, stale, skipped, or not run | BLOCKED or NEEDS WORK; never COMPLETE |
| All inputs/tasks/integration/evidence current and passing | COMPLETE |

## Protocol Compliance

- [ ] Approved inputs are proven before implementation planning
- [ ] Proposal phase is mutation-free
- [ ] Exact manifest approval precedes all writers
- [ ] One writer per path and one named integration owner
- [ ] Parallelism is disjoint, dependency-aware, and capped
- [ ] Timeout/retry/cancel/late-result behavior is deterministic
- [ ] Checkpoint recovery is hash-bound and idempotent
- [ ] Actual test execution and current evidence gate COMPLETE
- [ ] PARTIAL is always reported when launched work is incomplete
- [ ] Side effects stated by SKILL, metadata, and spec are consistent
- [ ] Authorization is never broadened by delegation, retry, or resume

## Coverage Notes

- The workflow does not test upstream design-review, ADR acceptance, or
  story-readiness correctness; it validates their supplied evidence and current
  hashes.
- Shared workflow-guide/catalog wording and cross-skill owner handoffs require a
  separately authorized shared update.
