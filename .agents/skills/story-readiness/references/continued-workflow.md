# Story Readiness Continued Workflow

Execute all applicable phases in order. The entire workflow is read-only.

## Phase 0 — Parse and load

1. Parse the exact invocation grammar in `SKILL.md`.
2. Reject missing/conflicting/unknown/repeated/unsafe inputs as `USAGE_ERROR`.
3. Resolve one canonical project root and load both normative reference files.
4. Resolve review mode once; a malformed present config is `INPUT_ERROR`.
5. Validate optional scope/prior-record manifest bytes, schema, project/target,
   normalized revision, and cursor before resolving stories.

Stop on error without enumerating/scanning unrelated paths or producing a story
verdict.

## Phase 1 — Resolve exact story set

### Specific story

Read only the exact canonical path and establish its declared revision/size. Missing,
ambiguous, unsafe, or over-limit identity is a one-story blocked/input result; do
not search for a replacement.

### Sprint

1. Read exact `production/sprint-status.yaml` bytes, read its declared revision, and
   select `cgs.sprint-tracker-v2-readiness-adapter/v1` only from exact
   `schema_version: cgs.sprint-tracker/v2`.
2. Validate positive tracker revision, stable event ID, equal sprint/active IDs,
   exactly one ACTIVE declaration, stable lifecycle owner/recorder, `plan_file`,
   raw `plan_revision`, plan revision, story_set_revision, dates/timezone/unit, capacity
   receipt/operands, and complete story rows.
3. Resolve only the declared `plan_file`, read exact bytes and record the explicit revision, require
   `cgs.sprint-plan/v2`, and validate plan ID/revision/declared revision plus exact tracker/
   plan payload agreement.
4. Recompute `story_set_revision` from every plan row and current story bytes; validate
   each complete tracker row's current story/core/readiness-record/receipt identity.
5. Require exact requested/tracker/plan and every present unique session/project-
   stage/milestone ACTIVE declaration to agree.
6. Preserve plan order for display; use stable story ID order for canonical revisions.

Any unsupported/legacy schema, `plan_path`/`plan revision` substitution, zero/multiple
plan, duplicate/missing ID or ACTIVE declaration, inactive state, missing story,
stale tracker/plan/story revision/timestamp, incomplete row, capacity/payload
mismatch, or selector conflict returns `RUN_BLOCKED`. Never use “most recent.”

### All

Use only ordered scope-manifest entries. Validate the cursor then take at most the
next 32 stories within all other caps. Do not recursively glob. Precompute the next
cursor inputs but emit a cursor only after completed-result revisions are known.

## Phase 2 — Freeze context and before snapshot

For each selected story independently:

1. Read exact story bytes and scan only the explicit top-level schema marker; do
   not interpret producer-owned fields before adapter selection.
2. Determine production-control applicability before authority availability.
3. Select exactly `cgs.story-v2-readiness-adapter/v1` only for one unambiguous
   `Schema: cgs.story/v2`; bind the exact create-stories producer SKILL/contract
   declared revision and their declared producer-version tuple.
   Unsupported/legacy/mixed/future schemas fail closed with
   `MIGRATION_REQUIRED`, never by applying guessed v2 or legacy fields.
4. Parse `Source Manifest ID`, `Story Core revision`, `Story Slot`, canonical path,
   producer status/readiness boundary, and the complete Source Manifest and
   Currentness Matrix. Reconstruct the producer manifest identity, recompute the
   producer-defined Story Core projection, and compare every matrix row with
   current source bytes/state/identity.
5. Resolve systems index, bound GDD/requirements, registry/TR rows, control
   manifest/rules, ADRs, dependencies, assets, QA plan/sources, technical/engine
   references, review mode, and sprint/current-context evidence as applicable.
6. read raw bytes and record the explicit revision and validate internal IDs/statuses/relationships.
7. Record every attempted source status and fixed-limit use.
8. Build `cgs.story-readiness-context/v1` with adapter/producer bundle,
   Source Manifest, Story Core, and currentness identities, then record its explicit revision.
9. Capture a streaming before snapshot for every bounded input path plus relevant
   declared-absent asset path. The allowed write set is empty.

Source failure for one story must not erase another story's completed context.

## Phase 3 — Run deterministic checks

For each story, evaluate `SR-C001` through `SR-C015` in numeric order. Emit one
structured row for each check even when an earlier blocker exists; downstream
checks may be `UNVERIFIED` only with the exact missing prerequisite.

Apply these joins before prose-quality checks:

1. story ID/schema, exact v2 adapter/producer contract, identity fields, Source
   Manifest ID, Story Core revision, complete currentness matrix, and production
   classification;
2. systems-index → Approved GDD path/revision → requirement ID;
3. story TR → current registry → same system/GDD/requirement;
4. governing ADR paths/revisions/status;
5. current control artifact/source-manifest/ruleset/review/ACTIVE-receipt rows and
   applicable stable Rule-ID locators through the v2 currentness matrix;
6. `Story Slot: SNNN` → `AC-SNNN-CC` → exactly one type-correct
   `TC|MC|SC-<epic>-SNNN-ACCC` per AC → type-specific QA fields and, when
   imported, current QA-plan/core/AC-set/source-manifest provenance;
7. dependency IDs/paths/kinds/current revisions/status/cycles;
8. asset path → current existence or exact producer dependency;
9. scope/type/estimate/engine/performance/unresolved-question requirements;
10. sprint membership/current-context evidence; and
11. source stability/mutation guard after Phase 5.

Generate stable findings at each non-pass. Fill owner, external action,
dependency ID, evidence, and deterministic resolution condition; do not emit a
free-form blocker without those fields.

## Phase 4 — Compute base verdict and QA packets

1. Compute base verdict from `SR-C001..SR-C015` precedence without discarding
   lower-severity gaps.
2. For lean/solo, create the exact `SR-C016 NOT_APPLICABLE` row and skip reason.
3. For full mode, freeze one QA packet per story after deterministic checks.
4. Dispatch/collect results with story-independent identities. A batch transport
   may carry multiple packets, but each result must echo exactly one packet and
   cannot contain a batch-wide verdict.
5. Normalize ADEQUATE/GAPS/INADEQUATE or mark only the affected story
   `UNVERIFIED` for missing/invalid/timeout/revision mismatch.
6. Create stable `SR-C016` findings and merge the final verdict deterministically.

Reviewer prose cannot alter source facts, finding classification, or another
story's result.

## Phase 5 — After snapshot and currentness

Repeat the bounded source snapshot for every story and compare exact paths,
presence, sizes, and declared revision. Also recheck sprint tracker/plan identity for a
sprint run and the scope/cursor context for an all run.

- A changed story/source makes only affected evidence stale, marks `SR-C015`
  `UNVERIFIED`, and prevents `READY`.
- A changed sprint/scope authority that invalidates set identity makes the run
  `RUN_BLOCKED` or `RUN_PARTIAL` while preserving independently complete records.
- An observed write by this workflow is `INPUT_ERROR` and no result is eligible.
- Never revert, repair, delete, overwrite, or attribute concurrent changes.

## Phase 6 — Prior finding comparison

When a valid prior-record manifest exists:

1. select at most one exact prior record per stable story ID;
2. validate record/receipt/project identity and relation to current sources;
3. match current/prior findings by `srf-v1` stable finding key;
4. label current matches `STILL_OPEN`;
5. label prior-only findings `RESOLVED_CANDIDATE` only under complete current
   equivalent coverage; otherwise retain them as unverified prior gaps; and
6. display valid waivers as `WAIVER_PRESENT` without changing check/verdict.

Do not persist any lifecycle transition.

## Phase 7 — Build record candidates

For each meaningfully evaluated story:

1. verify ordered check rows and finding set/revision;
2. recompute base/QA/final verdict and evaluation state;
3. bind adapter/producer SKILL/contract/bundle, Source Manifest ID, and Story Core
   revision, then
   build the readiness and stale keys from stable IDs/versions, allocate the candidate ID from the story ID and UTC run ID, and record its explicit revision;
4. enumerate every exact `expires_when` source/contract predicate;
5. set persistence and implementation eligibility fields to false; and
6. confirm no candidate claims to be a recorder receipt or durable authorization.

Do not build a misleading record for an unresolved story identity. Instead return
the partial/blocked result and exact gap.

## Phase 8 — Aggregate independently

Create the run envelope from ordered per-story results. Report:

- processed/total/page ordinal range and continuation;
- counts by final verdict plus partial/not-evaluated counts;
- source coverage and limit gaps;
- each story's complete source/check/finding/verdict/record-candidate detail;
- exact Must Have/Should Have non-ready warnings for sprint scope; and
- mutation snapshot evidence and fixed zero-write assertions.

Use `RUN_COMPLETE` only when every selected story/page entry has complete
evaluation. A complete story verdict is exactly `READY`, `NEEDS_WORK`, or
`BLOCKED`. Use `RUN_PARTIAL` when independent results are retained alongside any
partial/changed/over-limit/reviewer-incomplete story. Use `RUN_BLOCKED` when set
identity cannot resolve or no story can be meaningfully evaluated.

## Phase 9 — Return and stop

Return one canonical `cgs.story-readiness-run/v2` result in conversation. State:

```text
allowed_write_set: []
record_mutated: false
recorder_invoked: false
implementation_started: false
```

Explain that a durable record requires fresh exact authorization to a separate
recorder, which this workflow does not invoke. Offer only conversation drafting
help for story-local gaps. Do not edit, dispatch implementation, persist findings,
or invoke another project workflow.
