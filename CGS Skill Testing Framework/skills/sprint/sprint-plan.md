# Skill Test Spec: `$sprint-plan`

## Skill Summary

`$sprint-plan` creates or updates a sprint from exact `cgs.story-registry/v2`
rows and matching `cgs.story/v2` artifacts. New work must be `AUTHOR_COMPLETE`
and have one current persisted `cgs.story-readiness-record/v1` plus matching
`cgs.story-readiness-recorder-receipt/v1` proving
`implementation_gate_eligible: true`. The workflow resolves all previous-sprint
open items, selects work deterministically by dependency graph, layer, priority,
and one capacity unit, and identifies updates only through stable active-sprint
declarations. It freezes QA and bounded producer findings before one authorized
plan write plus a revision-checked single-recorder tracker commit.

Verdicts: `COMPLETE`, `COMPLETE — no changes required`, or `BLOCKED`.

---

## Static assertions

- [ ] YAML frontmatter contains only `name` and a non-empty `description`; name
  matches the skill directory.
- [ ] Arguments expose `new|update`; legacy `status` is a terminal redirect to
  `$sprint-status` with zero gates and zero writes.
- [ ] Review mode resolves once, with CLI override first, and no review-mode file
  is written.
- [ ] New work comes only from current `cgs.story-registry/v2` rows whose matching
  `cgs.story/v2` artifacts are `AUTHOR_COMPLETE` and whose current persisted
  readiness record/recorder receipt proves implementation eligibility.
- [ ] `EPIC.md` `## Stories` rows, story-header `Ready`, conversational verdicts,
  and unpersisted readiness candidates are never sprint eligibility evidence.
- [ ] Selection specifies a dependency-valid topological frontier followed by
  layer, priority, stable-ID tie-break, and capacity fit.
- [ ] Every previous-sprint non-done item requires an explicit carry, defer, or
  cancel-from-scope decision with preserved origin evidence.
- [ ] Tracker rows separate stable `story_id` from canonical project-relative
  `file`, and both are uniqueness/existence checked.
- [ ] Tracker writes use one logical recorder with expected revision, declared revision,
  plan revision, story-set revision, field ownership, and stable event ID.
- [ ] The normative plan declares `cgs.sprint-plan/v2`; the tracker declares
  `cgs.sprint-tracker/v2`; both expose identical `start_date`, `end_date`, IANA
  `timezone`, `estimate_unit`, and complete `stories[]` identity.
- [ ] Both schemas bind one current capacity receipt ID/path/revision/declared revision and
  identical integer `total/committed/reserved/released/remaining` operands where
  `remaining = total - committed - reserved + released`.
- [ ] Tracker `plan_file`, exact declared `plan_file_revision`, `plan_revision`, and
  `story_set_revision` bind the same final `cgs.sprint-plan/v2` bytes.
- [ ] Tracker declares `sprint_state: ACTIVE`, a stable `lifecycle_owner`, and
  `lifecycle_recorder: cgs.sprint-tracker/v2`; these fields are recorder-owned
  and are never inferred by consumers.
- [ ] Plan priority is only `must_have|should_have|could_have`, with explicit
  provenance from authoring `must-have|should-have|nice-to-have`.
- [ ] Every tracker row has an explicit status-update instant and provenance;
  retained/carry rows preserve their prior values and new admission binds the
  activation event plus exact story revision.
- [ ] Update mode resolves exactly one `active_sprint_id` from explicit state,
  session, stage, and milestone declarations and never uses recency.
- [ ] PR-SPRINT findings have stable IDs and at most one directed revision/rerun.
- [ ] QA findings, producer findings, carryover, and final scope resolve before
  preview and authorization.
- Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.
- [ ] Contains `COMPLETE`, `BLOCKED`, and at least two numbered phase headings.

---

## Case 1: New sprint happy path uses deterministic existing-story scope

### Fixture

- The current milestone and one capacity unit are declared.
- Three `cgs.story-registry/v2` rows resolve to matching `cgs.story/v2`
  `AUTHOR_COMPLETE` artifacts with valid dependencies and fitting estimates.
- Each has exactly one persisted current `READY` record and one matching recorder
  receipt proving `implementation_gate_eligible: true` for the exact story bytes,
  core revision, current source closure, checker/ruleset, and resolved review mode.
- The prior sprint has no open work.
- A canonical QA plan exists; review mode is `lean`.
- Both final targets have known prior states.

### Input

`$sprint-plan new`

### Expected writes

- `production/sprints/sprint-[NNN].md`
- `production/sprint-status.yaml`
- No other path.

### Expected behavior

The skill orders existing stories through the declared dependency/layer/priority
algorithm, renders an identical ordered set in both drafts, freezes the QA state,
shows one complete changeset, obtains authorization, and commits the pair through
the recorder transaction.

### Assertions

- [ ] Every row references one current registry row, canonical story file, and
  exact readiness record/receipt pair.
- [ ] New rows start canonical `ready_for_dev` without conflating lifecycle and
  priority.
- [ ] Plan and tracker share sprint ID, tracker revision, plan revision,
  story-set revision, and timestamp.
- [ ] Plan/tracker schema versions, dates, IANA timezone, estimate unit, canonical
  priorities, integer estimates, owners, and dependency arrays validate.
- [ ] `sprint_state: ACTIVE`, stable lifecycle owner/recorder, active sprint ID,
  capacity receipt identity, declared revision/revision, exact unit, and recomputed
  operands agree in the pair.
- [ ] Each tracker row has controlled status plus `status_updated_at` and exact
  `status_update_provenance`.
- [ ] Sprint-plan invokes neither readiness evaluation nor its recorder.
- [ ] `COMPLETE` appears only after both exact final revisions verify.

---

## Case 2: Dependency frontier precedes layer and priority

### Fixture

- Implementation-gate-eligible stories have authoring priorities: Presentation must-have
  `STORY-3333333333333333`, Foundation nice-to-have `STORY-1111111111111111`,
  and Core should-have `STORY-2222222222222222`.
- `STORY-2222222222222222` depends on `STORY-1111111111111111`;
  `STORY-3333333333333333` depends on `STORY-2222222222222222`.
- All estimates fit capacity.

### Input

`$sprint-plan new --review lean`

### Expected writes

- The two authorized sprint targets only.

### Expected behavior

The topological frontier permits only the Foundation prerequisite first, then the
Core story, then Presentation. Authoring priorities normalize to plan
`could_have`, `should_have`, and `must_have`; priority cannot leap over
dependencies.

### Assertions

- [ ] Final order is `STORY-1111111111111111`, `STORY-2222222222222222`,
  `STORY-3333333333333333`.
- [ ] Layer and priority are evaluated only among dependency-ready candidates.
- [ ] Both files persist the same order and dependency IDs.
- [ ] No `must-have|should-have|nice-to-have` spelling is persisted as plan
  priority after normalization.
- [ ] No dependency is removed or inferred away to improve priority order.

---

## Case 3: Equal-frontier ties use layer, priority, stable ID, then capacity

### Fixture

- Six independent persisted implementation-gate-eligible stories enter the same
  topological frontier.
- They span all four allowed layers and all three canonical plan priorities
  `must_have|should_have|could_have`.
- Two stories have equal layer and priority but reverse filesystem enumeration.
- Capacity fits only the first four items under the ordered selection.
- One current capacity receipt binds the project unit and exact integer
  total/reserved/released operands.

### Input

`$sprint-plan new`

### Expected writes

- The authorized plan/tracker pair containing four selected rows.

### Expected behavior

The skill ranks layer `Foundation < Core < Feature < Presentation`, then priority
`must_have < should_have < could_have`, then stable story ID code-point order.
It adds only candidates that fit and records remaining candidates as capacity
exclusions.

### Assertions

- [ ] Filesystem order and title do not affect selection.
- [ ] Stable-ID tie-breaking is reproducible.
- [ ] Unknown priority or author-to-plan mapping is `BLOCKED`, never defaulted.
- [ ] Excluded stories and exact capacity evidence appear in the plan.
- [ ] Selected estimates produce `committed`; plan/tracker reproduce identical
  receipt identity and `remaining = total - committed - reserved + released`.
- [ ] Unused capacity is not filled by inventing or splitting work.

---

## Case 4: Invalid dependency or capacity evidence fails closed

### Fixture

Run independently with: a missing dependency ID, a self-edge, a cycle, a
dependent whose prerequisite is excluded, mixed estimate units, an unknown
capacity value, malformed/stale `STORIES.md`, non-`AUTHOR_COMPLETE` story,
unpersisted readiness candidate, missing/mismatched recorder receipt,
`implementation_gate_eligible: false`, or any changed stale-key source.

### Input

`$sprint-plan new`

### Expected writes

- None.

### Expected behavior

The workflow reports the exact registry/story/readiness/dependency/capacity defect
and stops before QA, producer review, preview, or mutation instead of choosing a
plausible order or invoking readiness/recorder work itself.

### Assertions

- [ ] Verdict is `BLOCKED`.
- [ ] No priority rule breaks a cycle or missing edge.
- [ ] Unknown/mixed units are not coerced into feasibility.
- [ ] `EPIC.md` rows, story-header `Ready`, a bare `READY`, or user acceptance
  cannot replace the persisted current record and receipt.
- [ ] Gate and write counts remain zero when blocking occurs before gates.

---

## Case 5: Every previous open story receives an explicit decision

### Fixture

- The authoritative prior plan/tracker pair contains three non-done stories.
- User chooses carry for one, defer for one, and cancel from sprint scope for one,
  supplying a reason for each.
- One new persisted implementation-gate-eligible story also fits capacity.

### Input

`$sprint-plan new`

### Expected writes

- The new sprint plan and new active tracker only.
- No prior plan, prior tracker version, or story file is edited separately.

### Expected behavior

The plan records all three decisions. Only the carried item enters the new tracker;
defer and cancel-from-scope affect new sprint inclusion without claiming a story
lifecycle transition.

### Assertions

- [ ] The decision table covers every previous non-done stable story ID once.
- [ ] Each decision has a reason and prior-status evidence.
- [ ] The carried item is marked `[CARRY]`.
- [ ] Deferred/cancelled-from-scope items are absent from the new tracker.

---

## Case 6: Missing or ambiguous carryover decision blocks activation

### Fixture

- The prior pair contains two open items.
- One decision is blank, inferred from status, bulk-defaulted, or contradictory.

### Input

`$sprint-plan new`

### Expected writes

- None.

### Expected behavior

The workflow shows the unresolved item and asks for one explicit carry, defer, or
cancel-from-scope choice. It does not activate a new tracker until the decision
table is complete and frozen.

### Assertions

- [ ] Verdict is `BLOCKED` if the decision remains unresolved.
- [ ] No open item silently disappears or resets.
- [ ] Scope selection is not treated as write authorization.
- [ ] Previous sprint artifacts remain unchanged.

---

## Case 7: Carried lifecycle state and original origin survive

### Fixture

- A story originated in sprint 004, was carried through sprint 005, and is now
  `in-progress` in the authoritative sprint 005 tracker.
- User explicitly carries it into sprint 006.

### Input

`$sprint-plan new`

### Expected writes

- Sprint 006 plan and tracker only.

### Expected behavior

The carried row keeps `origin_sprint: sprint-004`, status `in-progress`, stable
story ID, canonical path, dependencies, remaining-work estimate, and the exact
prior `status_updated_at` plus `status_update_provenance`.

### Assertions

- [ ] Origin is not rewritten to sprint 005 or sprint 006.
- [ ] Status is not reset to `ready_for_dev`, and its status-update time/provenance
  is not replaced by the new sprint activation event.
- [ ] Carryover participates in dependency validation and capacity accounting.
- [ ] Plan and tracker agree on all carried-row fields.

---

## Case 8: Registry-stable story ID is distinct from canonical file path

### Fixture

- `production/epics/combat/STORIES.md` declares `cgs.story-registry/v2` and maps
  stable ID `STORY-a1b2c3d4e5f60708`, never-reused slot `S007`, and canonical path
  `production/epics/combat/story-007-parry.md`.
- The matching file is `cgs.story/v2`, `AUTHOR_COMPLETE`, and reproduces registry
  identity/revision/status plus raw/core revisions. Title punctuation differs from
  filename slug but identity fields agree.
- A current persisted readiness record and recorder receipt bind the same ID/path/
  revisions and prove implementation eligibility.

### Input

`$sprint-plan new`

### Expected writes

- The authorized plan/tracker pair.

### Expected behavior

The tracker stores `story_id: STORY-a1b2c3d4e5f60708` and the exact canonical
project-relative file separately. Registry revision/payload revision, story raw/core
revisions, readiness record/receipt IDs/revisions, and eligibility are copied unchanged
into the planning evidence and revalidated before and after commit.

### Assertions

- [ ] Epic slug, slot/number, title, or filename slug is not used as the stable ID.
- [ ] The path is under `production/epics/`, traversal-free, and a regular file.
- [ ] ID and path are each unique in the selected set.
- [ ] Both targets contain exactly the same ID/path pair.

---

## Case 9: Duplicate, unsafe, renamed, or missing story path blocks

### Fixture

Run independently with duplicate story IDs/slots, duplicate canonical paths,
traversal, symlink escape, registry/story identity disagreement, malformed
append-only registry ledgers, a tracked path renamed without upstream identity
resolution, or a path/record/receipt/stale-key source changed after preview.

### Input

`$sprint-plan update`

### Expected writes

- None for any variant.

### Expected behavior

The skill reports the exact registry/story/readiness identity/path conflict. A
pre-preview conflict blocks scope drafting; a post-preview change fails the atomic conflict check
preflight and invalidates authorization.

### Assertions

- [ ] No ID/path is reconstructed from an EPIC row, story title, or number.
- [ ] No tracker row is silently repointed.
- [ ] A post-preview path change causes a new preview after upstream resolution.
- [ ] Verdict is `BLOCKED` with no successful write claim.

---

## Case 10: New tracker commit starts one recorder revision

### Fixture

- No tracker exists and the new sprint plan path is absent.
- All planning checks pass and the exact pair is authorized.
- Recorder event ID is unused.

### Input

`$sprint-plan new`

### Expected writes

- The new plan.
- A tracker created only through the logical recorder commit.

### Expected behavior

The recorder precondition is `expected_tracker_revision: ABSENT` and
`expected_tracker_revision: ABSENT`; the candidate tracker uses
`schema_version: cgs.sprint-tracker/v2`, `tracker_revision: 1`, and a stable event
ID. Its matching plan uses `schema_version: cgs.sprint-plan/v2`.

### Assertions

- [ ] The tracker has schema version, revision, event ID, plan revision, and
  story-set revision.
- [ ] Plan and tracker contain the same `start_date`, `end_date`, IANA timezone,
  estimate unit, and complete stable STORY-* set.
- [ ] Direct tracker replacement outside the recorder is forbidden.
- [ ] The event ID is included in preview and final verification.
- [ ] One authorized transaction produces both targets.

---

## Case 11: Existing tracker update uses full compare-and-swap tuple

### Fixture

- Active tracker revision is 8 with captured declared revision, plan revision, and
  story-set revision.
- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
  revision after preview but before commit.

### Input

`$sprint-plan update`

### Expected writes

- None after the conflict.

### Expected behavior

The recorder compares every expected field immediately before mutation, rejects
the stale request, and requires context reload/re-render/re-preview. It never
overwrites revision 9 with the candidate based on revision 8.

### Assertions

- [ ] Any tuple mismatch blocks the entire pair.
- [ ] Last-writer-wins is forbidden.
- [ ] The candidate revision would have been exactly 9, never an arbitrary value.
- [ ] Earlier user authorization is invalid after context changes.
- [ ] Schema/date/timezone/unit or per-row status-provenance drift is also a pair
  conflict.

---

## Case 12: Recorder enforces event idempotency and field ownership

### Fixture

Run independently with: the same event ID and identical bytes; the same event ID
with different bytes; a sprint-plan request changing lifecycle-only fields; or a
lifecycle request changing planning-owned identity/scope fields.

### Input

A recorder request made during `$sprint-plan update`.

### Expected writes

- Identical replay: no additional write and verified existing result.
- Every conflicting replay or ownership violation: no write.

### Expected behavior

The recorder recognizes exact idempotent replay, rejects event reuse with new
bytes, and blocks requests outside declared field ownership.

### Assertions

- [ ] One logical recorder mediates every tracker mutation.
- [ ] Event ID is stable across a retry of the same operation.
- [ ] Unknown or cross-owner fields cannot be silently merged.
- [ ] No lost update is reported as `COMPLETE`.

---

## Case 13: Update resolves one stable active sprint across selectors

### Fixture

- Tracker, `production/session-state/active.md`, project-stage declaration, and
  current milestone each explicitly declare `active_sprint_id: sprint-006`.
- Exactly one canonical plan declares `sprint_id: sprint-006`.
- Tracker IDs and plan identity agree.

### Input

`$sprint-plan update`

### Expected writes

- Only the authorized sprint-006 plan and tracker pair.

### Expected behavior

The skill records each selector path/value/revision, resolves sprint 006, and updates
that exact pair regardless of file timestamps or higher-numbered historical plans.

### Assertions

- [ ] Stable declarations, not recency, choose the sprint.
- [ ] Exactly one matching plan is required.
- [ ] Tracker `sprint_id` and `active_sprint_id` both match.
- [ ] The selected plan/tracker also agree on exact versioned schema fields,
  dates, timezone, estimate unit, stable STORY-* rows, and plan revision.
- [ ] A sprint-007 historical file is not selected merely because it is newer.

---

## Case 14: Conflicting or malformed active-sprint selectors block

### Fixture

Run independently with tracker `sprint-006` versus session `sprint-005`, malformed
`sprint-6`, duplicate stage declarations, or a current milestone naming two
active sprint IDs.

### Input

`$sprint-plan update`

### Expected writes

- None.

### Expected behavior

The workflow reports every source and raw value, returns `BLOCKED`, and requests
an authoritative correction. It does not choose a majority, precedence winner,
highest number, or most recently modified plan.

### Assertions

- [ ] Conflicting present declarations cannot be ignored.
- [ ] Malformed declarations are errors, not absent values.
- [ ] No QA or producer gate runs after identity is blocked.
- [ ] Both final targets remain unchanged.

---

## Case 15: Missing selector or non-unique plan match cannot use recency

### Fixture

Run independently with no explicit active sprint ID, no plan for the unique ID,
two canonical plans declaring the ID, a missing tracker, or tracker/plan ID
disagreement. Modification times appear to suggest a likely sprint.

### Input

`$sprint-plan update`

### Expected writes

- None.

### Expected behavior

The skill refuses to infer an update target and identifies the exact missing or
non-unique evidence required.

### Assertions

- [ ] The phrase or behavior “most recent sprint” is not used for selection.
- [ ] Exactly one stable ID, one tracker, and one matching plan are mandatory.
- [ ] Filesystem enumeration order is irrelevant.
- [ ] Verdict is `BLOCKED` before scope mutation.

---

## Case 16: Producer REALISTIC result preserves stable findings

### Fixture

- Review mode is `full`; the complete QA-bearing draft is ready.
- PR-SPRINT returns `REALISTIC` with finding `PR-SPRINT-001`, evidence, affected
  capacity field, and disposition `accepted as satisfied`.

### Input

`$sprint-plan new --review full`

### Expected writes

- The authorized plan/tracker pair after the first producer result.

### Expected behavior

The skill records the stable finding ID, evidence, and disposition in the
planning payload, performs no producer rerun, and previews the final bytes.

### Assertions

- [ ] `gate_count` is 1 and `producer_rerun_count` is 0.
- [ ] Finding ID and disposition survive into plan revision input.
- [ ] The gate sees the exact ordered scope and carryover/QA state.
- [ ] No content is appended after authorization.

---

## Case 17: First-pass concerns require explicit acceptance or one revision

### Fixture

- PR-SPRINT first returns `CONCERNS` with stable findings
  `PR-SPRINT-001` and `PR-SPRINT-002`.
- Run independently with user accepting every concern, stopping, or authorizing
  one directed scope/capacity revision.

### Input

`$sprint-plan update --review full`

### Expected writes

- Accept-all variant: the final authorized pair may be written.
- Stop variant: none.
- Revision variant: no write until the single rerun is `REALISTIC`.

### Expected behavior

Acceptance records each risk before preview. Revision targets named findings,
revalidates affected evidence, preserves IDs, and increments rerun count once.

### Assertions

- [ ] Partial or implicit concern acceptance is invalid.
- [ ] Finding IDs do not change during revision.
- [ ] Scope choice is separate from final write authorization.
- [ ] No unbounded producer loop is possible.

---

## Case 18: One directed producer revision converges to REALISTIC

### Fixture

- First PR-SPRINT result is `UNREALISTIC` with `PR-SPRINT-003` and exact evidence.
- User authorizes one bounded capacity/scope revision.
- Affected registry/story/readiness-record/receipt, dependency, capacity,
  carryover, and QA checks pass again.
- The sole rerun returns `REALISTIC` and closes `PR-SPRINT-003`.

### Input

`$sprint-plan new --review full`

### Expected writes

- One final plan/tracker pair after a new complete preview and authorization.

### Expected behavior

The skill performs exactly one directed revision and rerun, passes the prior
finding ID with its disposition, re-renders both files, and freezes only the
converged candidate.

### Assertions

- [ ] `gate_count` is 2 and `producer_rerun_count` is 1.
- [ ] The prior-state approval, if any, is not reused.
- [ ] Both drafts retain the same revised ordered story set.
- [ ] Final finding history remains auditable.

---

## Case 19: Non-converged, malformed, or second producer revision blocks

### Fixture

Run independently when the sole rerun returns `CONCERNS`, `UNREALISTIC`, missing
or malformed findings, duplicate finding IDs, evidence-free findings, an unknown
verdict, or asks for a second revision.

### Input

`$sprint-plan new --review full`

### Expected writes

- None.

### Expected behavior

The workflow returns `BLOCKED` after the bounded rerun (or immediately for
malformed first-pass output), reports all stable finding IDs it received, and
never keeps revising until a favorable answer appears.

### Assertions

- [ ] `producer_rerun_count` never exceeds 1.
- [ ] A rerun must be exactly `REALISTIC` to converge.
- [ ] Malformed or duplicate finding IDs fail closed.
- [ ] No final target write or `COMPLETE` claim occurs.

---

## Case 20: End-to-end stale evidence and atomic rollback regression

### Fixture

- A fully ordered, carryover-resolved, QA- and producer-reviewed pair is
  authorized.
- Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.

### Input

`$sprint-plan update`

### Expected writes

- Preflight conflict variants: none.
- Mid-transaction failure variants: both prior states are restored; only authorized
  transaction temporaries may have been touched and are reported.
- Success control: exactly the two final targets.

### Expected behavior

Every stale input invalidates the frozen transaction. Mid-transaction failure
restores the pair. Only a success control with matching final revisions, incremented
tracker revision, event ID, ordered set, canonical source paths, and still-current
persisted implementation eligibility can complete.

### Assertions

- [ ] One-file success is never reported as sprint success.
- [ ] Changed evidence requires rebuild, invalidated checks, and a new preview.
- [ ] Final verification covers both targets and every selected source path/revision.
- [ ] Final verification covers exact schema versions, canonical priorities,
  date/timezone/unit/capacity equality, and per-row status update provenance.
- [ ] All terminal branches report gate, producer-rerun, and write counts.

---

## Authoritative P1 traceability

| Audit ID | Static contract | Behavioral cases |
|---|---|---|
| SP-005 | Dependency-valid frontier, layer then canonical priority then stable ID, capacity fit | 1–4 |
| SP-006 | Explicit exhaustive carry/defer/cancel-from-scope table with preserved origin/status | 5–7, 20 |
| SP-007 | Stable story ID plus unique canonical existing project-relative path | 8–9, 20 |
| SP-008 | One recorder, full atomic conflict check tuple, monotonic revision, event idempotency, field ownership | 10–12, 20 |
| SP-009 | Unique stable active-sprint selectors and exact plan/tracker match; no recency | 13–15, 20 |
| SP-010 | Stable producer finding IDs and at most one directed revision/rerun | 16–20 |

## Protocol compliance

- [ ] Story-registry/readiness-record/receipt consumption, carryover comparison,
  selector resolution, QA lookup, and producer review are read-only before
  authorization.
- [ ] User scope/carryover/risk decisions are distinct from exact-byte write
  authorization.
- [ ] Review-mode configuration and prior sprint/story artifacts are outside the
  authorized final path set.
- [ ] The final preview includes every target, prior state/atomic conflict check value, candidate revision,
  and exact content or complete diff.
- [ ] Status reporting is handed off to `$sprint-status`.
- [ ] Next steps never offer `$dev-story` without a current persisted record and
  receipt proving `implementation_gate_eligible: true`.

## Coverage notes

- The authoritative P1 set contains exactly six findings: `SP-005` through
  `SP-010`.
- Cases also retain prerequisite fail-closed, pre-authorization QA, current
  registry/story/readiness-record/receipt verification, terminal status redirect,
  and atomic-pair safety guards required by the inherited P0 baseline.
- This is a behavioral/static contract. Runtime execution, real producer
  delegation, injected concurrent writes, filesystem-atomicity guarantees, and
  migrations of separate consumer skills require integration evidence outside
  this specification.

## Path-first integrity regression

1. Invoke the skill with canonical project-relative paths and no caller-supplied content-derived token.
2. Verify that schema versions, stable IDs, permissions, lifecycle state, and path or ID collisions remain enforced.
3. Verify that generated IDs are allocated independently of file bytes.
4. For a permitted mutation, change a declared revision or target state after preview and verify that the atomic conflict check stops the write.
5. Verify that an authorized unchanged candidate is staged beside the target, atomically replaced, re-read, and rolled back on failure.
