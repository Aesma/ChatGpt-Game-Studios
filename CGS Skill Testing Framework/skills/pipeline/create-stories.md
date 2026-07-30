# Skill Test Spec: $create-stories

## Purpose

Verify that `$create-stories` authors one bounded batch of
`cgs.story/v2` planning artifacts from one exact current epic and current
GDD/TR/Accepted-ADR/control evidence. The workflow must use stable story, slot,
acceptance, Test, and dependency identities; prefer verifiable vertical slices;
handle source and QA gaps per story; keep author status separate from final
readiness; classify an existing inventory idempotently; preserve append-only
trace; and publish only after a full compare-and-set check.

This specification retains P0 protections against placeholder TRs and missing-QA
Ready claims and closes CS-003 through CS-008. It also covers the stable-ID,
vertical-slice, bounded-batch, partial-result, provenance, and transaction
requirements needed by those findings.

The suite is not executed by creating or staging this file. All execution/result
fields in `CGS Skill Testing Framework/catalog.yaml`, including every
`last_*` field, remain unchanged and empty until an authorized test workflow
actually runs the cases.

## Frozen fixtures and observation

Each case freezes exact raw bytes, canonical/real paths, existence states,
direct-child membership, and revision values for its applicable subset of:

- workflow catalog;
- one explicit `cgs.epic-plan/v2`, its source manifest, and exact
  `cgs.create-epics-result-receipt/v1`;
- sibling `STORIES.md` registry/ledgers or exact ABSENT state;
- the selected epic's complete direct-child inventory;
- current architecture/TR evidence and review/lifecycle records;
- exact approved GDDs and current approval evidence;
- exact governing ADRs and lifecycle/review evidence;
- `cgs.control-manifest/v2` plus review/ACTIVE receipt;
- one explicit QA plan and/or one QA assessment; and
- story targets, local extensions, revision histories, and dependency targets.

Fixtures state stable epic/module/system/source/TR/ADR/Rule/story/slot/AC/Test/
dependency IDs, source locators/excerpts, states, priorities, slice boundaries,
batch/cursor values, reviewer identities, limits, and expected candidate bytes.

The harness records every read, enumeration, prompt, decision, stable-ID
allocation/retirement, QA/delegation event, source/inventory/core/AC-set/candidate
revision, diff, CAS re-read, temp/publication/readback event, route output, and
persistent mutation. Undeclared/unbounded reads and writes outside the exact
authorized story/STORIES targets fail the case.

## Static assertions

- [ ] Frontmatter contains only `name` and a non-empty `description`; name is
  `create-stories`.
- [ ] Metadata states bounded stable story candidates, not final readiness.
- [ ] Invocation has explicit `author|audit`, exact EPIC path, capped batch,
  cursor, and evidence path/revision pairs.
- [ ] Bare slug, automatic epic discovery, newest/nearest evidence, globs,
  traversal, and escaping symlinks are rejected.
- [ ] The catalog glob is treated as an envelope, not ownership of every matching
  file.
- [ ] Owned output is limited to selected direct-child story files, exact managed
  story files and one sibling STORIES registry; EPIC/index remain read-only.
- [ ] `audit` has zero candidate, approval, QA delegation, temporary, report,
  cursor-file, or persistent writes.
- [ ] Mutation requires a current supported `cgs.epic-plan/v2`, source manifest,
  and exact create-epics result receipt; legacy epic migration
  is external.
- [ ] GDD admission requires current exact independent APPROVED evidence.
- [ ] TR admission requires stable ID, exact source/approval revisions, CURRENT, and
  DERIVED_COVERED or visible DECISION_GAP.
- [ ] Placeholder, guessed, repaired, renumbered, or fuzzy TR IDs are forbidden.
- [ ] Accepted-current ADR admission validates lifecycle/review/dependency revisions;
  missing ADR affects only dependent stories.
- [ ] Control rules are selected by stable Rule ID and preserve normative
  strength, scope, conditions, qualifications, and contextual rejection.
- [ ] Non-ACTIVE/current control evidence cannot support AUTHOR_COMPLETE.
- [ ] Stable story ID comes from epic/source/TR/slice identity, not title/order/
  path slug/date/batch.
- [ ] Story slots and criterion slots are monotonic and never reused.
- [ ] Split/merge/move/boundary change retires old identities and allocates new
  story/AC IDs with explicit supersession.
- [ ] Story paths use the immutable SNNN slot under the exact epic directory;
  display-title changes do not silently rename.
- [ ] Every AC has exact approved source span/revision and current TR binding.
- [ ] Every Test ID has one exact story/AC/type/owner binding and complete
  type-specific fields.
- [ ] Dependencies use stable story ID, exact path/core revision, HARD/SOFT, and
  reason/source; the graph is unique and acyclic.
- [ ] Vertical slices have one observable outcome and enforce the 4-TR, 8-AC,
  4-hard-dependency limits.
- [ ] Horizontal component buckets are rejected unless a current evidence-backed
  enabler has an independently verifiable outcome.
- [ ] QA plan selection uses the exact scope-or-sprint/epic/story/path/core/
  AC-set/AC/Test tuple, never mtime/title/slug.
- [ ] At most one 12-story/60-second read-only QA assessment runs and it returns
  a distinct verdict per story.
- [ ] Template status is impossible: status is computed and round-trips identically
  through preview/story/STORIES registry/result.
- [ ] AUTHOR_COMPLETE is distinct from final READY; every authored story says
  `Readiness Verdict: NOT_EVALUATED`.
- [ ] Only exact-revision external story-readiness evidence can later produce READY.
- [ ] Full inventory classifies CREATE/UPDATE/NO_OP/RETIRE/CONFLICT/DEFERRED and
  preserves local extensions/history.
- [ ] A target-local conflict/source gap permits independent safe stories and
  makes the batch PARTIAL; epic-wide ledger/source corruption blocks all.
- [ ] The workflow indexes at most 256 direct children, mutates at most 12 logical
  stories, and respects per-file/class/48-MiB limits.
- [ ] A cursor is inline, revision-bound, deterministic, and never persisted.
- [ ] One authorization binds the complete selected changeset and limitations.
- [ ] Final CAS revalidates every source/target/membership/identity/QA/candidate
  value; any change causes zero new mutations.
- [ ] Publication is described as per-file atomic, never falsely cross-file
  atomic; partial-write state is evidence-honest.
- [ ] Story and story-registry histories are append-only; exact no-op changes
  nothing.
- [ ] The story never embeds its own current artifact revision.
- [ ] Routing returns exactly one catalog-derived action or Stop and executes
  nothing.

## Current authority admission

### Case 1: current supported epic

A unique `cgs.epic-plan/v2` has canonical EPIC-MODULE identity, legal state,
exact `cgs.epic-source-manifest/v2`, current result receipt, and provenance.

**Expected:** The epic is admitted as bounded planning scope. Its prose is not
treated as GDD or ADR authority.

### Case 2: legacy or malformed epic

Exercise managed-schema v1, missing epic ID, duplicate system ID, bad slug/path,
unsupported state, malformed ledger, and stale provenance.

**Expected:** `author` is BLOCKED_UNSUPPORTED_EPIC with zero writes. `audit`
reports exact limitations without retrofitting.

### Case 3: current approved GDD evidence

The epic links two GDD paths/revisions and each exact artifact has current independent
APPROVED evidence.

**Expected:** Only exact linked requirements/criteria are admitted with source
IDs/locators/excerpts and revisions.

### Case 4: GDD status text is not approval

The GDD and epic say Approved but the review record is missing or targets old
bytes.

**Expected:** Affected product evidence is STALE/UNKNOWN; no acceptance outcome is
invented from labels.

### Case 5: current stable TR

Architecture/TR evidence binds a stable TR to exact approved GDD evidence with
CURRENT and DERIVED_COVERED.

**Expected:** The exact TR ID is preserved and may support a candidate.

### Case 6: TR gap/state matrix

Exercise DECISION_GAP, CHANGED, STALE, UNBOUND, SOURCE_BLOCKED, provisional,
duplicate, malformed, migration ambiguity, and missing TR.

**Expected:** Each affected story is BLOCKED with exact source/reason. No
placeholder or repaired ID appears; unrelated TRs remain usable.

### Case 7: Accepted-current ADR

ADR path/revision, Accepted transition, recorder, review, dependencies, supersession,
and TR coverage are all current.

**Expected:** Exact implementation constraints are admitted with complete
provenance.

### Case 8: control manifest current and ACTIVE

The v2 control artifact, payload/ruleset/source manifest/history, review, and
ACTIVE receipt all bind current bytes; applicable stable Rule IDs are conflict
free.

**Expected:** Exact rules may support AUTHOR_COMPLETE while retaining RFC level,
scope, conditions, qualifications, and source.

### Case 9: noncurrent control matrix

Exercise absent, DRAFT, PARTIAL, stale, unreviewed, non-ACTIVE, conflict,
blocking UNKNOWN, unsupported schema, and payload/history mismatch.

**Expected:** Affected planning stories are BLOCKED and final readiness remains
NOT_EVALUATED. Current safe planning content may still be written as PARTIAL.

## CS-003 — per-story ADR/source gaps and PARTIAL batches

### Case 10: one missing ADR among independent stories

Three candidate stories use distinct TRs; only story B requires a missing ADR.

**Expected:** B is BLOCKED with exact gap. A and C continue. The batch is PARTIAL,
not globally stopped or falsely COMPLETE.

### Case 11: Proposed ADR affects one story

Only story C depends on a Proposed ADR.

**Expected:** C is BLOCKED/ADR_NOT_ACCEPTED; other current stories retain their
independently computed status.

### Case 12: one ADR governs several stories

The same stale ADR is required by B and D but not A/C.

**Expected:** B/D block; A/C proceed. The gap report groups evidence without
copying one batch status onto all stories.

### Case 13: one story needs two ADRs

One ADR is Accepted-current and one is missing.

**Expected:** That story blocks and records both states; it does not silently use
the accepted subset as complete coverage.

### Case 14: evidence-backed ADR N/A

Current epic/TR evidence carries reason
`NO_ARCHITECTURAL_DECISION_REQUIRED` for a pure data slice.

**Expected:** N/A is admitted with exact reason provenance; the author does not
invent an ADR.

### Case 15: author-invented ADR N/A

No current reason code exists.

**Expected:** N/A is UNKNOWN/BLOCKED for the affected story.

### Case 16: target-local conflict plus safe siblings

One existing story path has unknown/manual content outside `x-local-*`; two new
story targets are collision-free.

**Expected:** Conflicting target is excluded; safe siblings and corresponding
managed ledger rows may publish; outcome PARTIAL.

### Case 17: epic-wide ledger corruption

Two ledger rows own the same slot/story ID/path.

**Expected:** Whole author run is BLOCKED with zero writes; partial publication
cannot safely allocate identities.

## CS-004 — computed status and round-trip invariants

### Case 18: AUTHOR_COMPLETE matrix

All epic/GDD/TR/ADR/ACTIVE-control/priority/slice/dependency/AC/Test evidence is
current and QA is ADEQUATE.

**Expected:** Story Status is AUTHOR_COMPLETE and Readiness Verdict remains
NOT_EVALUATED.

### Case 19: strict status ordering

One story has both missing test fields and a missing required ADR.

**Expected:** BLOCKED wins over NEEDS_WORK. The reason list retains both gaps.

### Case 20: QA gaps downgrade only one story

QA returns ADEQUATE for A and GAPS for B.

**Expected:** A is independently eligible; B is NEEDS_WORK.

### Case 21: template cannot overwrite status

Fixture candidate render template contains a stale AUTHOR_COMPLETE literal while
computed status is BLOCKED.

**Expected:** Rendering rejects the candidate; no file is written.

### Case 22: preview/story/registry/result agreement

Use a mixed AUTHOR_COMPLETE/NEEDS_WORK/BLOCKED batch.

**Expected:** Every representation carries the exact same story ID/status and
counts. A mismatch blocks that target or batch before publication.

### Case 23: write readback status round-trip

After atomic per-file write, reparsing returns a different status, story ID,
readiness field, or source manifest.

**Expected:** Stop PARTIAL_WRITE, report exact observed revision, and never report
COMPLETE.

### Case 24: retired status is evidence-bound

A prior story no longer owns any current source slice and exact replacement
evidence exists.

**Expected:** RETIRED is rendered with superseding IDs/history; the file is not
deleted and no current story reuses its identity.

## CS-005 — capped QA assessment with per-story verdicts

### Case 25: one batch assessment

A selected batch has 12 stories and no supplied QA review.

**Expected:** Exactly one read-only qa-lead request is made for one frozen batch
payload; it returns 12 separate story records.

### Case 26: over-cap batch

The author batch request is 13 or supplied QA result contains 13 story records.

**Expected:** Invocation/assessment is rejected before delegation or publication.

### Case 27: per-story verdicts differ

QA returns ADEQUATE, GAPS, INADEQUATE for three stories.

**Expected:** Their statuses are computed independently as eligible/NEEDS_WORK/
BLOCKED subject to stricter source evidence.

### Case 28: missing QA record

The batch contains A/B/C but the result omits B.

**Expected:** B is QA UNKNOWN/NEEDS_WORK; A/C records remain usable. No batch
verdict is copied.

### Case 29: duplicate, unknown, or mismatched QA record

Exercise duplicate story result, result for D, wrong core revision, wrong batch revision,
or wrong source-manifest ID.

**Expected:** Only affected bindings are UNKNOWN; ambiguous duplicate identity
cannot pass.

### Case 30: QA timeout/partial/failure/late result

The one 60-second attempt fails or returns after token revocation.

**Expected:** No retry. Selected stories lacking valid records are at least
NEEDS_WORK; batch is PARTIAL.

### Case 31: self/mutating QA result

Reviewer identity equals author or no-mutation is false/missing.

**Expected:** Result is invalid UNKNOWN. No self-review or reviewer write is
accepted.

### Case 32: QA ADEQUATE is not final readiness

All QA records are ADEQUATE.

**Expected:** Stories may become AUTHOR_COMPLETE but every final readiness field is
NOT_EVALUATED/NONE_CURRENT.

## CS-006 — one schema, path, status, and Priority contract

### Case 33: full cgs.story/v2 shape

Render one Logic story.

**Expected:** All ordered identity, authority, source, slice, AC, QA, dependency,
gap, local-extension, and revision sections occur exactly once.

### Case 34: exact canonical path

Story slot is S007 under epic slug `combat-core`.

**Expected:** Canonical path is
`production/epics/combat-core/story-007-<preserved-slug>.md`; no layer-based
directory or extra stories subdirectory is used.

### Case 35: title change preserves path

The display title changes while story identity/slice remains.

**Expected:** Story ID, slot, and current path are preserved. No silent rename.

### Case 36: Priority source is exact

Epic/GDD planning evidence assigns `must-have` with stable source locator/revision.

**Expected:** Priority and Priority Source are emitted exactly.

### Case 37: missing/ambiguous priority

No source assigns priority or epic and GDD disagree.

**Expected:** Story is NEEDS_WORK or BLOCKED on conflict; order/layer/type does not
invent priority.

### Case 38: story type controls one evidence contract

Run Logic, Integration, Visual/Feel, UI, and Config/Data variants.

**Expected:** Each story renders only its own required evidence schema, not all
five templates.

### Case 39: identity and readiness fields mandatory

Remove story ID, slot, epic ID, revision, source-manifest/core revision, computed
status, or NOT_EVALUATED readiness.

**Expected:** Schema validation fails before publication.

### Case 40: explicit candidate revision consistency

The renderer receives an explicit candidate revision that disagrees with the approved changeset.

**Expected:** Candidate is invalid. Story, core, source, and registry revisions must agree with explicit producer metadata; no ID or revision is derived from content bytes.

### Case 41: schema/path/catalog/spec alignment

Compare SKILL, metadata, reference, this spec, test catalog, and workflow catalog.

**Expected:** Names/command/spec path and artifact envelope agree; broad catalog
glob never expands ownership.

## CS-007 — exact QA-plan routing and binding

### Case 42: exact supplied QA plan

The explicit path/revision plan is CURRENT and binds exact QA scope/sprint, epic,
story, canonical path, current raw story artifact revision, revalidated declared core revision,
AC-set revision, AC, and Test ID.

**Expected:** Only exact matching items are imported with path/revision/owner state.

### Case 43: same name in another sprint

Two plans have identical titles and story text but different sprint IDs.

**Expected:** Only the exact supplied/bound sprint tuple can match.

### Case 44: same slug in another epic

Another epic has the same story display slug and AC text.

**Expected:** Epic/story IDs prevent import; title/slug similarity has no effect.

### Case 45: mtime/latest trap

A newer plan conflicts with the explicit older current plan.

**Expected:** The workflow never reads/selects by mtime or latest filename; only
the explicit exact plan is considered.

### Case 46: stale core or AC-set revision

Plan binds old story core or old AC membership.

**Expected:** Import is rejected for that story, status at least NEEDS_WORK, and
risk acceptance cannot make it current.

### Case 47: partial/ambiguous plan

Exercise PARTIAL, STALE, duplicate Test ID, Test bound to two ACs, missing plan
owner, source revision mismatch, and unsupported schema.

**Expected:** Affected items are not imported; exact reasons remain visible.

### Case 48: exact story-level and epic-level plan items

One supplied plan contains valid items for selected and unselected stories.

**Expected:** Import only selected exact story/AC items. Other items neither
authorize nor contaminate the batch.

## CS-008 — full inventory, idempotency, stable identities, and conflicts

### Case 49: empty inventory create

No story files or ledger rows exist.

**Expected:** New story IDs derive from canonical keys; monotonically allocated
slots/paths are collision-free; candidates classify CREATE revision 1.

### Case 50: exact rerun no-op

Sources, inventory, rendered bytes, QA observation, and append-only trace are
unchanged.

**Expected:** All stories/STORIES registry classify NO_OP; no approval, version/time/
history change, temp file, or write.

### Case 51: managed update

Same story identity/key/path has current approved source wording change and a
valid v2 base without unknown content.

**Expected:** UPDATE base revision + 1 with source/AC/test/status/history diff.

### Case 52: manual content outside extension

Existing target has an unknown manually added section.

**Expected:** Target-local CONFLICT; no overwrite/merge. Independent siblings may
continue PARTIAL.

### Case 53: local extension preservation

Existing story has valid `x-local-notes`.

**Expected:** Update preserves it and never lets it override status/source/AC/
Test/dependency/history fields.

### Case 54: story ID collision

Two distinct full canonical keys share the same truncated STORY ID.

**Expected:** Epic-wide IDENTITY_CONFLICT with both full revisions and zero writes;
no suffix/sequential fallback.

### Case 55: slot/path collision

Two identities claim S004 or the same canonical path.

**Expected:** Whole batch blocks until ledger ownership is repaired externally.

### Case 56: split existing story

One oversized story becomes two evidence-backed vertical slices.

**Expected:** Old story is RETIRED; two new STORY IDs and never-used slots/AC IDs
are created with supersedes links. Old IDs are not moved/reused.

### Case 57: merge existing stories

Two old stories now form one indivisible current slice.

**Expected:** Both old stories retire; one new ID/slot/AC set is allocated. No old
ID is selected as an arbitrary winner.

### Case 58: source criterion moved between stories

Regrouping moves one criterion from story A to new story C.

**Expected:** A's old AC ID retires; C receives a new AC ID under C's slot. The AC
ID is not transplanted.

### Case 59: removed source with no valid replacement

A source disappears but removal/current lifecycle evidence is ambiguous.

**Expected:** Existing story is CONFLICT/BLOCKED, not silently retired/deleted.

### Case 60: registry ownership conflict

STORIES registry has duplicate/mismatched epic ownership, malformed append-only
ledgers, or conflicts with the read-only EPIC/receipt identity.

**Expected:** Epic-wide publication blocks; story counts are not patched by name
or slug guessing.

## Stable AC/Test identities, dependencies, and vertical slicing

### Case 61: stable story under reorder

Source requirements, story display order, and filesystem enumeration are
reordered without changing source/slice ownership.

**Expected:** Story ID, slot, path, AC IDs, and Test IDs remain unchanged.

### Case 62: source-owned requirement reworded

Same approved stable requirement/criterion ID changes exact wording.

**Expected:** Preserve story/AC identities, update excerpt/source/core revisions and
revision diff only after current approval covers new bytes.

### Case 63: stable business key-owned source changes

A no-ID source's locator/text identity changes.

**Expected:** Explicit migration/new story or AC identity is required; fuzzy
continuity is forbidden.

### Case 64: exact Test-ID/type matrix

Exercise TC, MC, and SC patterns with complete required fields.

**Expected:** Every ID deterministically uses epic slug, immutable story slot, and
criterion slot and binds one AC only.

### Case 65: placeholder or incomplete Test spec

Exercise blank/TBD/TODO/???/fill-later, wrong type, missing assertion/pass
condition/evidence path, and duplicate ID.

**Expected:** Missing QA coverage; story cannot be AUTHOR_COMPLETE.

### Case 66: valid vertical slice

A player action crosses input, gameplay logic, persistence event, and observable
feedback to satisfy one behavior.

**Expected:** One verifiable vertical story is preferred over component buckets.

### Case 67: valid evidence-backed enabler

An Accepted ADR requires a serialization foundation before an end-to-end slice,
and it has an independently observable round-trip AC.

**Expected:** The single-layer enabler is valid with exact dependency provenance.

### Case 68: invalid horizontal decomposition

The candidate proposes “all backend,” “all UI,” and “all tests” stories for one
behavior without independent outcomes.

**Expected:** SLICE_GAP; regroup into observable slices or block for scope
decision.

### Case 69: slice limit matrix

Exercise more than 4 TRs, 8 ACs, 4 hard direct dependencies, several primary
outcomes, duplicate AC ownership, and no observable pass condition.

**Expected:** Deterministic evidence-backed split or affected BLOCKED status; no
arbitrary file-count split.

### Case 70: dependency DAG

Dependencies resolve by stable ID/path/core revision and form a valid DAG.

**Expected:** Deterministic topological order is used for batching but never
changes identity.

### Case 71: dependency failure matrix

Exercise missing/ambiguous hard dependency, stale core revision, self-edge, duplicate
edge, cycle, and cross-epic title-only reference.

**Expected:** Affected dependent stories block; exact IDs/evidence are reported.
Epic-wide identity corruption blocks all.

### Case 72: soft dependency

A current source explicitly marks one dependency SOFT with reason.

**Expected:** Preserve it without treating it as a hard start blocker; absence of
explicit SOFT means HARD.

## Bounded batches, CAS, append-only trace, and readiness handoff

### Case 73: default and maximum batch

Twenty logical mutations exist.

**Expected:** Default selects 8; explicit 12 selects 12; remaining items are
DEFERRED with a deterministic inline cursor and outcome PARTIAL.

### Case 74: deterministic cursor resume

Resume with the exact cursor and unchanged epic/source/inventory/order revisions.

**Expected:** Select the next stable IDs without duplication or omission.

### Case 75: stale/tampered cursor

Change epic, source manifest, inventory, ordering ruleset, remaining IDs, or
cursor revision.

**Expected:** BLOCKED_STALE_CURSOR, zero writes, and no silent restart from title/
order.

### Case 76: input count/per-file/class/total limits

Exercise every declared ceiling independently, including 257 direct children and
48-MiB total overflow.

**Expected:** BLOCKED_LIMIT before synthesis; no sampling, truncation, partial
truth claim, QA delegation, or write.

### Case 77: no recursive or unrelated scan

Thousands of unrelated epics/GDDs/ADRs/QA plans/sprints/tests exist.

**Expected:** None is recursively scanned or ingested. Only exact selected closure
and direct-child inventory are read.

### Case 78: one complete authorization

A mixed CREATE/UPDATE/RETIRE batch is ready.

**Expected:** Existing bounded authorization or one approval binds every path,
preimage, candidate, diff, source/inventory/batch/QA revision, history append, and
omitted limitation. No per-story prompt.

### Case 79: full CAS change matrix

After approval independently change catalog, EPIC/receipt/STORIES, directory membership,
story target/local extension/history, GDD/approval, TR/architecture, ADR/lifecycle,
control/review/ACTIVE, QA plan/review, dependency target, cursor, or candidate.

**Expected:** Each change is CAS_CONFLICT with zero new mutations, no refresh/
merge/retry, and no approval reuse.

### Case 80: verified per-file publication

CAS passes and every atomic file create/replace/readback verifies.

**Expected:** STORIES current registry/ledgers publish last and only from verified
story results. EPIC/index remain unchanged. Exact external artifact revisions are
reported.

### Case 81: mid-publication failure

One story verifies, the next write/readback fails.

**Expected:** PARTIAL_WRITE lists verified, uncertain, unchanged, and unattempted
paths/revisions. It does not claim cross-file rollback, delete success, or COMPLETE.

### Case 82: append-only revision and allocation history

Update/retire stories and append STORIES batch/allocation events.

**Expected:** Prior events/slots/IDs remain byte-for-byte and ordered; each new
event binds base/candidate/source/core/batch revisions and author/time.

### Case 83: exact no-op trace

Everything is semantically and byte-identical.

**Expected:** No revision/time/event/QA invalidation/approval/temp/write.

### Case 84: readiness separation and stale prior receipt

An existing final READY receipt targets the base story; authoring changes one byte.

**Expected:** Candidate records NOT_EVALUATED/NONE_CURRENT. Receipt becomes stale
observation and is never retargeted or rewritten.

### Case 85: exact final handoff

One final story is AUTHOR_COMPLETE and catalog declares story-readiness.

**Expected:** Return exactly one catalog-derived command with exact path and
external artifact revision, without executing it or claiming READY.

### Case 86: missing typed route

Catalog does not define enough schema/transition policy for a gap owner or
story-readiness.

**Expected:** Route UNKNOWN/Stop. Never hardcode architecture, QA, sprint, gate,
or implementation commands.

### Case 87: terminal outcome matrix

Exercise COMPLETE, UNCHANGED, PARTIAL, BLOCKED, DECLINED, ERROR, and
PARTIAL_WRITE.

**Expected:** Report exact epic/source/inventory/batch/cursor/story/QA/CAS/history
states and one next action or Stop. Never claim final READY, epic completion, test
execution, implementation, sprint selection, or gate passage.

## Coverage map

- CS-003: Cases 10-17.
- CS-004: Cases 18-24.
- CS-005: Cases 25-32.
- CS-006: Cases 33-41.
- CS-007: Cases 42-48.
- CS-008: Cases 49-60.
- Stable ID, dependency, and vertical slicing: Cases 61-72.
- Bounded batch, append-only trace, CAS, and readiness separation: Cases 73-87.
- P0 placeholder-TR and QA fail-closed protections: static assertions and Cases
  5-6, 18-20, 42-47, and 64-65.

Passing static structure or staging this candidate is not behavior-suite
execution. Test evidence fields remain owned by the designated test workflow.
