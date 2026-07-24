# Skill Test Spec: $dev-story

## Skill Summary

`$dev-story` consumes one exact persisted and current READY record, plans a
closed changeset with disjoint implementation/recorder ownership, executes every
required test with hash-bound evidence, and moves tracker-owned implementation
lifecycle only to `IN_REVIEW`. It never closes a story.

This specification is authoritative for structural and scenario validation of
the staged P1 candidate. It defines expected checks; it does not claim that a
runner executed them. Framework catalog result fields remain unchanged until a
real harness run records evidence.

## Contract Files

```text
.agents/skills/dev-story/SKILL.md
.agents/skills/dev-story/agents/openai.yaml
.agents/skills/dev-story/references/implementation-transaction-v2.md
CGS Skill Testing Framework/skills/pipeline/dev-story.md
```

## Static Assertions

### Invocation and bounded identity

- [ ] Frontmatter contains only `name` and non-empty `description`.
- [ ] Invocation accepts exactly one hash-bound `cgs.dev-story-request/v2`.
- [ ] No-argument, positional, glob, absolute, traversal, latest, and inferred
      session-scope calls fail before mutation.
- [ ] One exact story, sprint tracker, readiness record/receipt, source manifest,
      owner set, checkpoint, and fixed limits are required.
- [ ] Raw bytes, canonical path rules, schemas, and SHA-256 identities are explicit.

### P0 regression protections

- [ ] Captured source/control provenance is immutable and never refreshed here.
- [ ] Ordinary admission requires a fresh persisted READY record; the sole
      non-READY branch requires a current persisted NEEDS_WORK record whose only
      gaps are exact manifest staleness and/or explicitly soft dependencies.
- [ ] Hard dependencies cannot be waived or edited.
- [ ] A soft dependency needs a current structured waiver in admitted evidence or
      a new exact waiver in the approved plan/result; it never mutates the story,
      dependency, readiness registry, or tracker planning fields.
- [ ] Every normal and recovery target, owner, preimage, deterministic candidate
      or runtime derivation contract, output bound, AC/Test mapping, command, and
      write condition is fixed before one plan-hash approval.
- [ ] A writer acknowledgement failure is side-effect free.
- [ ] Changed sources, targets, deterministic candidates, derivation contracts,
      owners, or commands invalidate approval.
- [ ] Partial writes are byte-restored and verified or exposed by a checkpoint.

### DS-004 — lifecycle authority and CAS

- [ ] Sprint tracker is the sole implementation-lifecycle authority.
- [ ] One status recorder is the exact `lifecycle_owner`, owns transition
      proposal/verification/checkpoint, and never writes tracker or story bytes.
- [ ] Tracker declares exact `lifecycle_recorder: cgs.sprint-tracker/v2`; only that
      recorder may write lifecycle-owned story-row fields.
- [ ] Consumer validates canonical `tracker_revision`, event/sprint/ACTIVE
      identity, `lifecycle_owner`, `lifecycle_recorder`, `plan_file`, raw
      `plan_sha256`, `plan_revision`, `story_set_hash`, typed capacity, and full
      story row. The independently computed raw tracker hash is not a field.
- [ ] `cgs.story/v2` raw bytes, Revision, author/readiness fields, history, and
      `x-local-*` extensions remain unchanged throughout the workflow.
- [ ] Each proposal supplies exact tracker raw-hash/revision/plan-revision/
      story-set CAS, stable event/transaction IDs, and requested field owners.
- [ ] Recorder result/receipt binds pre/post raw hashes, revision increment,
      committed CAS, verified read-back, row status/provenance, immutable story,
      unchanged planning fields, and unowned-field comparison.
- [ ] Missing/invalid/partial recorder evidence never becomes a verified result;
      observed unexplained mutation returns PARTIAL with checkpoint evidence.
- [ ] Success requires `TRANSACTION_VERIFIED` at `in_progress` and later
      `in_review`, with `plan_file`/`plan_sha256`/`plan_revision`/`story_set_hash`
      preserved byte-for-byte.

### DS-005 — one business writer

- [ ] Exactly one implementation owner writes source, config, data, schema, asset,
      test, raw-log, and manual-evidence targets.
- [ ] The orchestrator has no inline Config/Data or other business write branch.
- [ ] Each target has one owner and the implementation/recorder path sets are disjoint.
- [ ] An orchestrator fallback retains an explicit stable owner identity and domain.

### DS-006 — engine reviewer is read-only

- [ ] At most one engine reviewer receives one immutable hash-bound packet.
- [ ] Reviewer result states `allowed_write_set: []` and `write_count: 0`.
- [ ] Reviewer never shares a target with the implementation owner.
- [ ] Findings return to the sole implementation owner.
- [ ] A new path invalidates the plan; an architectural finding blocks.

### DS-007 — implementation is not closure

- [ ] Allowed transitions are only `READY_FOR_DEV -> IN_PROGRESS -> IN_REVIEW`.
- [ ] `Complete`, `Done`, acceptance, deploy, and release are never written here.
- [ ] `IMPLEMENTED` explicitly means awaiting review.
- [ ] Success routes to code-review and then story-done; only story-done closes.

### DS-008 — deterministic test execution

- [ ] Every required Test ID binds AC IDs, argv tokens, cwd, environment allowlist,
      timeout, runner/tool identity, source/build identity, expectation, and log path.
- [ ] Every execution records UTC start/end, timeout state, exit/unavailable reason,
      raw-log byte count/hash, observations, and normalized result.
- [ ] Commands execute as argv tokens without shell reinterpretation.
- [ ] Missing, unrun, timed-out, nonzero, hashless, truncated, stale, or malformed
      blocking evidence cannot pass.
- [ ] Any required non-PASS prevents IN_REVIEW and produces PARTIAL after mutation
      or FAILED/BLOCKED with verified zero/restored mutation.

### DS-009 — architecture decisions fail closed

- [ ] Every semantic change maps to an exact Accepted ADR or a justified
      contract-defined `NOT_ARCHITECTURAL` classification.
- [ ] Uncovered architectural choices create stable `DSF-*` blockers.
- [ ] Blockers route to the architecture decision owner with exact evidence and
      resolution condition.
- [ ] No proceed-anyway, local signature, user risk acceptance, drafted ADR, or
      implementation-note bypass exists.

## Test Cases

### Case 1: Happy path — current READY gate and verified tracker transactions

**Fixture**

- Request, source manifest, story, readiness registry/record/receipt, sprint plan,
  and tracker have valid exact hashes.
- Persisted record is `READY`, `COMPLETE`, implementation-gate eligible, and all
  stale-key sources remain current.
- Dependencies are complete, every architectural change has an Accepted ADR, and
  one implementation owner returns exact deterministic candidates and bounded
  derivation contracts for runtime evidence.
- User authorizes the canonical plan hash.
- Every deterministic write reaches its candidate hash, every generated output
  satisfies its derivation contract, and all required tests pass.

**Expected**

1. No mutation occurs before full preview and authorization.
2. Declared lifecycle recorder commits and read-back verifies tracker row
   `in_progress` with one event/transaction ID; story bytes remain unchanged.
3. Sole implementation owner writes exactly the business target set.
4. Tests run exactly and persist raw logs plus execution records.
5. Declared lifecycle recorder commits and read-back verifies tracker row
   `in_review` with one new event/transaction ID; planning fields remain fixed.
6. Result is IMPLEMENTED and routes to review, not completion.

**Assertions**

- [ ] Planned and actual write sets are identical.
- [ ] Entire story raw bytes, Revision, readiness fields, and captured source
      bindings are preserved.
- [ ] Tracker plan file/hash/revision and story-set hash remain unchanged.
- [ ] Every required AC has one or more current passing Test-ID records.
- [ ] No Complete/Done value is written.

### Case 2: Conversational READY without recorder receipt is blocked

**Fixture:** story-readiness returned READY in conversation, but no persisted
record/valid recorder receipt exists.

**Expected:** return BLOCKED with zero writes; route to the independent readiness
recorder owner. Do not simulate persistence or accept the story header.

- [ ] Implementation owner is not dispatched.
- [ ] Tracker and story bytes remain unchanged.
- [ ] `implementation_gate_eligible` is never inferred.

### Case 3: Persisted READY is stale

**Fixture:** admission mode is CURRENT_READY and the record/receipt are valid, but
one Accepted ADR raw hash differs from its stale key.

**Expected:** independently detect staleness, return BLOCKED, and require fresh
readiness evaluation/recording. No waiver branch is offered.

- [ ] Old READY does not pass by ID or verdict alone.
- [ ] Captured story provenance is not rewritten.
- [ ] No plan authorization is requested.

### Case 3b: Structured manifest risk preserves captured provenance

**Fixture:** admission mode is STRUCTURED_ACCEPTED_RISK; a persisted complete
NEEDS_WORK record has exactly one non-pass for control-manifest staleness; story
header and Source Snapshot agree on captured hash A; current valid manifest is B;
every other check passes; the plan contains a complete `MW-*` waiver.

**Expected:** preview and approval name hashes A/B and the waiver; preserve every
captured provenance field; label all transactions/checkpoints/results `STALE /
ACCEPTED-RISK`; never call the story READY or gate eligible.

- [ ] Free text cannot substitute for the waiver schema.
- [ ] A second current-manifest change invalidates plan and waiver before mutation.
- [ ] Any unrelated non-pass or blocker disables this branch.

### Case 4: Hard and soft dependency matrix

Run each variant with unrelated checks passing:

| Variant | Kind | Current state | READY-bound waiver | Expected |
|---|---|---|---|---|
| 4a | omitted/hard | Complete | none | PASS |
| 4b | hard | Ready | none | BLOCKED |
| 4c | hard | Blocked | structured | BLOCKED |
| 4d | hard | missing | user says proceed | BLOCKED |
| 4e | soft | In Progress | none | BLOCKED |
| 4f | soft | In Progress | exact current waiver in admitted record or approved plan | ACCEPTED-RISK |
| 4g | soft | In Progress | waiver names prior hash/state | BLOCKED |

- [ ] No row edits a dependency.
- [ ] A new soft waiver is permitted only in STRUCTURED_ACCEPTED_RISK mode, inside
      the complete approved plan/result, with no story or tracker-planning write.
- [ ] Accepted risk is visible and never changes the READY record.

### Case 5: DS-004 — tracker-only lifecycle authority

**Fixture:** `cgs.story/v2` has `Story Status: AUTHOR_COMPLETE`; tracker row is
`ready_for_dev`; tracker declares the exact owner/recorder and canonical planning
tuple; all admission checks pass.

**Expected**

1. Preserve the complete story raw bytes and Revision.
2. Submit an exact `cgs.dev-story-status-transition-proposal/v2` with external raw
   tracker hash CAS and requested lifecycle-owned row fields.
3. Update tracker row lifecycle to `in_progress` only through the declared
   `cgs.sprint-tracker/v2` recorder.
4. Verify `cgs.dev-story-status-transaction/v2`, tracker read-back, revision/event,
   status provenance, immutable planning tuple, and unchanged unowned fields.

- [ ] No story projection or competing authoring status is invented.
- [ ] Dev-story never directly replaces tracker bytes.
- [ ] Result cannot continue to business writes until the transaction verifies.

### Case 6: DS-004 — tracker CAS conflicts before recorder commit

**Fixture:** the transition proposal is frozen; an external writer changes tracker
bytes before the canonical lifecycle recorder CAS.

**Expected**

1. Stop before all business writes.
2. Recorder rejects the stale external raw-hash/revision tuple; do not overwrite.
3. Story and business targets remain unchanged; no checkpoint is needed when the
   recorder proves zero mutation.
4. Return BLOCKED with exact observed tracker hash and fresh-planning requirement.

- [ ] There is no last-writer-wins retry.
- [ ] There is no retry using the newly observed tracker bytes.
- [ ] Raw tracker hash is not read from an invented tracker field.

### Case 7: DS-004 — final recorder result is ambiguous after observed change

**Fixture:** all business writes/tests pass; recorder call returns ambiguous after
tracker bytes changed, and no complete valid receipt proves the requested
`in_progress -> in_review` transition.

**Expected:** return PARTIAL, not IMPLEMENTED; preserve all write/test evidence and
record the observed tracker, proposal, recorder result, receipt gap, and unchanged
story hash in the checkpoint.

- [ ] Code-review/story-done handoff is not emitted.
- [ ] Story remains byte-for-byte unchanged and is not closed.
- [ ] Resume is limited to the original plan and current exact hashes.

### Case 8: DS-005 — Config/Data receives one delegated owner

**Fixture:** story type is Config/Data and targets include one engine config, one
data table, one schema, one smoke test, and one raw log.

**Expected:** assign all five business targets to one implementation-owner
identity. Status recorder owns proposals/verification/checkpoint; canonical
lifecycle recorder owns only authorized tracker-row status fields. Orchestrator
writes none.

- [ ] No inline “small data edit” exception exists.
- [ ] Smoke command/log are part of the approved plan.
- [ ] Ownership sets are disjoint and complete.

### Case 9: DS-005 — mixed business owners are rejected

**Fixture:** planner assigns source to gameplay-programmer and data to a second
data writer.

**Expected:** reject before approval and require one implementation owner for the
entire business write set.

- [ ] No files or statuses change.
- [ ] Splitting paths by file type does not bypass the one-writer contract.

### Case 10: DS-006 — valid read-only engine review

**Fixture:** planned file types need engine review. One specialist returns a valid
packet-bound result with two non-architectural findings, empty write set, and zero
writes. The primary resolves them within existing planned paths.

**Expected:** include finding-set hash in the plan; retain the same sole business
owner and exact path set.

- [ ] Reviewer cannot apply its recommendation.
- [ ] Result is rejected if packet or source hash differs.
- [ ] Findings remain attributable and hash-bound.

### Case 11: DS-006 — reviewer proposes a write or new path

**Fixture:** engine specialist edits a config candidate or says a new engine file
must be created.

**Expected:** reject the result/plan, make zero mutation, and rebuild only after a
new complete path plan; reviewer never gains ownership.

- [ ] Concurrent primary/reviewer mutation is forbidden.
- [ ] Existing approval cannot cover the new path.

### Case 12: DS-007 — implementation success stops at In Review

**Fixture:** all files and tests pass, story bytes are unchanged, and the final
tracker transition receipt/read-back verifies `in_review`.

**Expected:** outcome IMPLEMENTED, lifecycle IN_REVIEW, next action code-review
then story-done.

- [ ] “Complete,” “Done,” “accepted,” and “closed” are absent from mutations.
- [ ] IN REVIEW is explicitly not completion.
- [ ] Closure workflow is not invoked by dev-story.

### Case 13: DS-008 — exact deterministic execution receipt

**Fixture:** one integration Test ID maps two AC IDs; approved argv exits 0 and
produces a complete raw log.

**Expected:** evidence contains exact argv tokens, cwd, allowed environment,
runner version/hash, source/build identity, UTC start/end, timeout state, exit 0,
raw-log path/byte count/hash, assertions, PASS, and result-set hash.

- [ ] A prose “tests passed” summary is insufficient.
- [ ] A user-run-later instruction is insufficient.
- [ ] Raw log is written by the implementation owner and matches its plan row.

### Case 14: DS-008 — nonzero required test after implementation writes

**Fixture:** source/tests are at approved candidate hashes, but one required test
exits 1 with a complete hashed log.

**Expected:** do not publish IN_REVIEW; retain/verify IN_PROGRESS, create checkpoint,
return PARTIAL, and expose the failing Test/AC mapping.

- [ ] Failure is never converted to warning or PASS.
- [ ] Exact exit, timestamps, and log hash are retained.
- [ ] No review/closure handoff is emitted.

### Case 15: DS-008 — unavailable, timed-out, or hashless evidence matrix

| Variant | Observation | Expected |
|---|---|---|
| 15a | command not run | non-PASS; no IN_REVIEW |
| 15b | timeout | non-PASS with timeout receipt; no IN_REVIEW |
| 15c | exit 0, log missing | non-PASS; no IN_REVIEW |
| 15d | exit 0, truncated log | non-PASS; no IN_REVIEW |
| 15e | different argv/cwd | plan invalidated; stop |
| 15f | manual check promised later | non-PASS; no IN_REVIEW |

- [ ] Each post-mutation variant returns PARTIAL and checkpoints exact state.
- [ ] Zero/restored-mutation variants may return FAILED only after hash verification.

### Case 16: DS-009 — missing or Proposed ADR

**Fixture:** a planned persistence/schema-ownership change has no Accepted ADR;
one Proposed ADR discusses it.

**Expected:** create stable architecture blocker, route the exact decision to the
architecture decision owner, and return BLOCKED with zero mutation.

- [ ] Proposed is not Accepted.
- [ ] User approval of the implementation plan cannot waive the blocker.
- [ ] The workflow does not draft, accept, or implement an ADR decision.

### Case 17: DS-009 — stable finding across line/hash drift

**Fixture:** rerun Case 16 after diagnostic prose and source line numbers change,
but the semantic decision gap and owner/resolution condition remain the same.

**Expected:** finding ID remains stable; evidence hashes update. A changed semantic
observation produces a new finding ID.

- [ ] Timestamp/prose/line number/raw source hash do not control identity.
- [ ] Resolution requires an exact Accepted ADR binding.

### Case 18: Plan-hash authorization and new-file discovery

**Fixture:** user approved plan P1; implementation owner discovers an additional
test helper or schema file.

**Expected:** stop before touching the new path. P1 authorization expires. Rebuild
the complete plan from fresh readiness/current sources and request new approval.

- [ ] The new path is not patched opportunistically.
- [ ] New preview includes the complete set, not only the added file.
- [ ] Prior writes, if any, are exposed through the failure contract.

### Case 19: Writer acknowledgement failure is side-effect free

**Fixture:** plan is approved, but implementation owner or recorder cannot
acknowledge exact owned paths/target-contract hashes.

**Expected:** return FAILED, all target preimages unchanged, no checkpoint needed.

- [ ] Tracker remains READY_FOR_DEV.
- [ ] Story bytes and Revision are unchanged.
- [ ] Business paths and logs remain unchanged/absent.

### Case 20: Resume is bound to the original partial transaction

**Fixture:** a valid create-only checkpoint records a failed test after business
writes. Resume request names its exact path/hash; immutable story, tracker
planning tuple, sources, and recorded tracker lifecycle transaction remain exact.

**Expected:** validate gate-consumption proof and every current target, continue
only at the recorded ordinal under the same plan/owners/deterministic candidates/
derivation contracts/commands.

- [ ] Checkpoint is not modified or deleted.
- [ ] Resume cannot add scope or skip the failing test.
- [ ] Any other stale-key/source change blocks and requires fresh READY/plan.

### Case 21: Checkpoint path already exists

**Fixture:** before the first mutation, the request's create-only checkpoint path
exists although its precondition is ABSENT.

**Expected:** return BLOCKED with zero writes; never overwrite or select a “latest”
checkpoint.

- [ ] Existing recovery evidence is preserved.
- [ ] A unique fresh request/checkpoint path is required.

### Case 22: Fully verified pre-authorized restoration

**Fixture:** a write fails; every changed path has an approved rollback operation
and is safely restored to its captured bytes.

**Expected:** reread every path, require exact baseline hashes plus a valid tracker
transaction receipt/read-back and unchanged story bytes, then return FAILED. If
any comparison fails, return PARTIAL.

- [ ] “Rolled back” appears only after full byte-identity verification.
- [ ] No ad hoc git reset/checkout or unplanned compensating edit is used.

## Protocol Compliance

- [ ] Request, readiness, plan, authorization, deterministic candidates, runtime
      derivations, executions, status transactions, checkpoints, and result use
      explicit versioned schemas.
- [ ] All evidence is path/hash/locator bound and bounded by fixed limits.
- [ ] Mutation snapshots distinguish no-write, restored, and partial outcomes.
- [ ] The candidate preserves P0 provenance, dependency, and closed-plan controls.
- [ ] DS-004 through DS-009 each have static assertions and adversarial cases.
- [ ] Dedicated spec result fields are not treated as executed evidence.

## P1 Finding Coverage

| Finding | Contract remediation | Primary cases |
|---|---|---|
| DS-004 | tracker-only authority; exact owner/recorder and planning tuple; external raw-hash CAS; immutable story; honest partial result | 5–7 |
| DS-005 | one implementation owner for all business/config/data/test/evidence paths; no orchestrator write | 8–9 |
| DS-006 | one read-only engine reviewer; findings to sole writer; no overlap | 10–11 |
| DS-007 | only READY_FOR_DEV→IN_PROGRESS→IN_REVIEW; story-done owns closure | 12 |
| DS-008 | exact argv execution, timestamps, exit/timeout, raw-log hash, non-PASS terminal | 13–15 |
| DS-009 | stable architecture blocker; Accepted ADR required; external owner route | 16–17 |

## Cross-skill compatibility notes

- The candidate consumes the persisted READY or narrowly scoped NEEDS_WORK
  record/receipt contract defined by staged P1 `story-readiness`; it never treats
  a conversational candidate as implementation authorization or upgrades a
  NEEDS_WORK verdict.
- The candidate preserves staged P1 `create-stories` `cgs.story/v2` as a wholly
  immutable author artifact; implementation lifecycle exists only in the tracker.
- Downstream code-review/story-done consumers must consume
  `cgs.dev-story-result/v2`, exact file/test hashes, and the IN_REVIEW transaction;
  current staged P1 story-done still requires the removed story projection/pair
  and therefore must be migrated before integration can pass.
