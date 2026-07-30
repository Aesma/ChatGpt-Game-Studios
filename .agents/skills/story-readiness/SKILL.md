---
name: story-readiness
description: Validate bounded stories with deterministic, revision-bound Story, GDD, TR, ADR, control, dependency, asset, acceptance-criterion, test, sprint, and optional QA evidence; return stable findings and unpersisted readiness-record candidates without authorizing implementation or writing files.
---

# Story Readiness

Evaluate whether each exact story snapshot is ready for implementation. This is a
strictly read-only evidence gate. It returns one independent verdict and one
revision-bound record candidate per story; it never edits a story, source, tracker,
gate record, readiness registry, or implementation artifact and never invokes a
recorder or implementation workflow.

A conversational `READY` verdict describes the checked snapshot only. It is not
durable implementation authorization. Only a separately persisted and still-
current readiness record may be eligible under a consumer's own gate contract.

## Invocation

Use exactly one scope form:

```text
$story-readiness --story <project-relative-story-path>
                 [--review full|lean|solo]
                 [--prior-records <project-relative-manifest>@<revision>]

$story-readiness --sprint <stable-sprint-id>
                 [--review full|lean|solo]
                 [--prior-records <project-relative-manifest>@<revision>]

$story-readiness --all
                 --scope-manifest <project-relative-manifest>@<revision>
                 [--cursor <cgs-story-readiness-cursor-v1>]
                 [--review full|lean|solo]
                 [--prior-records <project-relative-manifest>@<revision>]
```

- Exactly one of `--story`, `--sprint`, or `--all` is required.
- `--scope-manifest` and `--cursor` are valid only with `--all`.
- Every option may appear once. Paths are canonical project-relative paths with
  `/` separators, Unicode NFC, no glob, traversal, URI, drive prefix, symlink
  escape, or case-ambiguous match.
- A scope/prior-record manifest is bound to its exact raw bytes by revision.
- A sprint ID is a stable declared ID, not a filename or timestamp.

Unknown/missing/repeated options, positional arguments, invalid mode
combinations, malformed paths/revisions/cursors, or an invalid review value return
`USAGE_ERROR` before story resolution. A referenced manifest that is unreadable,
revision-mismatched, malformed, unrelated, or stale returns `INPUT_ERROR`.

Run outcomes are exactly:

```text
RUN_COMPLETE | RUN_PARTIAL | RUN_BLOCKED | USAGE_ERROR | INPUT_ERROR
```

Per-story machine verdicts are exactly `READY`, `NEEDS_WORK`, and `BLOCKED`;
display `NEEDS_WORK` as “NEEDS WORK.” `PASS`, `FAIL`, `COMPLETE`, `APPROVED`, a
story header status, and a prior readiness claim are not verdict substitutes.

## Load the contract

Read [readiness-rules-v1.md](references/readiness-rules-v1.md) completely. It
defines the explicit `cgs.story/v2` producer adapter, source schemas, bounded
manifests, stable checks/findings, exact sprint
resolution, GDD/TR/ADR/control joins, story/AC/Test/dependency/asset validation,
QA normalization, verdict precedence, record candidates, and the independent
recorder protocol.

Read [continued-workflow.md](references/continued-workflow.md) completely and
execute its phases in order. If either contract file is missing, unreadable, or
internally inconsistent, return `INPUT_ERROR` without a readiness verdict.

## Zero-write and implementation boundary

The allowed write set is empty. Do not create or update a story, scope manifest,
sprint plan/tracker, QA plan, finding register, readiness record, cache, draft,
accepted-risk record, migration, or session state. Do not install tools, generate
assets, repair paths/statuses, or ask for ordinary write authorization.

Capture bounded before/after mutation snapshots. Concurrent changes are evidence
of staleness, not permission to revert or assign blame. A changed story or required
source invalidates that story's result; completed unaffected story results remain
valid within their own snapshots. Never call `$dev-story`, another project skill,
or `cgs.story-readiness-recorder/v1`.

## Resolve review mode

Resolve review mode once per run:

1. use the explicit `--review` value;
2. otherwise read exact `production/review-mode.txt` bytes and accept exactly
   `full`, `lean`, or `solo` after trimming one trailing line ending;
3. otherwise default to `lean` and record the absent source.

Malformed present configuration is `INPUT_ERROR`; do not default around it.
`lean` and `solo` skip QL-STORY-READY with an explicit reason. `full` requires
one independently normalized result for every evaluated story before its final
verdict is computed.

## Resolve an exact bounded story set

### One story

`--story` reads exactly the named file. Do not enumerate siblings or infer a
story from session state.

### Active sprint

`--sprint` resolves the exact declared sprint ID through
the exact raw bytes of `production/sprint-status.yaml`, the plan referenced by its
canonical `cgs.sprint-tracker/v2` fields, and current story bytes. Select
`cgs.sprint-tracker-v2-readiness-adapter/v1` only from the exact top-level schema;
legacy `plan_path`/`plan revision`, unknown schemas, or field-name guessing never form
authority. Never select “most recent,” use mtime, or choose among multiple matches.

Require a positive `tracker_revision`, stable `event_id`, equal requested
`sprint_id`/`active_sprint_id`, exactly one `sprint_state: ACTIVE` declaration,
stable `lifecycle_owner` and `lifecycle_recorder: cgs.sprint-tracker/v2`, canonical
`plan_file`, exact raw `plan_revision`, matching `plan_revision`, and recomputed
`story_set_revision`. Record the tracker's own raw revision and revision in the context/
stale key. Resolve only that `plan_file`; require exact `cgs.sprint-plan/v2`
schema/ID/revision and exact date/timezone/estimate-unit/capacity receipt and
operand agreement. Validate complete tracker/plan story coverage and each row's
stable ID, canonical path, priority, current story/core revisions, lifecycle
provenance, readiness record/receipt binding, and gate-eligibility state.
Every present session, project-stage, and current-milestone ACTIVE declaration must
be unique and agree, but none can override tracker/plan identity. Missing,
malformed, stale, duplicate, ambiguous, inactive, or conflicting sprint authority
returns `RUN_BLOCKED` before a sprint verdict summary.

### All stories

`--all` consumes only `cgs.story-readiness-scope/v1`; it never performs an
unbounded recursive glob. The manifest contains the exact ordered story ID/path/
declared revision set, root/project/target identity, generation time, and manifest revision.
Apply the fixed page/file/byte/reference/reviewer limits in the rules reference.

When work remains, return `RUN_PARTIAL` with a deterministic continuation cursor
bound to the scope manifest, next ordinal, completed result-set revision, ruleset, and
source snapshot. A changed manifest/context invalidates the cursor. Never silently
sample or describe a partial page as the whole project.

## Freeze current context and authoritative sources

For every selected story, validate the declared revision before evaluation and
create a `cgs.story-readiness-context/v1` snapshot. It includes project target/
dirty identity and exact source status/path/revision/fields used for:

- the story and optional prior readiness record;
- the selected story adapter and exact create-stories producer SKILL/contract
  bytes plus their NUL-delimited bundle identity;
- `design/gdd/systems-index.md`, the bound Approved system GDD, and the exact GDD
  requirement IDs/locators;
- `docs/architecture/tr-registry.yaml` and every referenced TR entry;
- the story's `Source Manifest ID`, `Story Core revision`, complete Source Manifest
  and Currentness Matrix, and every current source row used by that matrix;
- `docs/architecture/control-manifest.md`, its current artifact/source-manifest/
  ruleset state, applicable Rule IDs, and the story's exact currentness rows;
- every governing ADR and its status;
- dependency stories and declared asset/test evidence;
- imported QA plan/source manifests when claimed;
- `.codex/docs/technical-preferences.md`, configured engine-version reference,
  and `production/review-mode.txt` when relevant; and
- sprint tracker adapter/schema/declared revision/event/unique ACTIVE declaration,
  exact `plan_file`/raw `plan_revision`, plan revision/story set, and session
  corroboration for sprint scope.

Each source status is exactly `LOADED_VALID`, `ABSENT`, `UNREADABLE`, `INVALID`,
`revision mismatch`, `STALE`, `UNSUPPORTED`, or `OVER_LIMIT`. Do not turn missing or
unreadable evidence into N/A or a pass.

A story is in the production control plane when its path is under
`production/epics/` or it contains a production schema marker listed in the rules
reference. Select an adapter before interpreting producer-owned fields. The only
gate-eligible production adapter is
`cgs.story-v2-readiness-adapter/v1` for exact `Schema: cgs.story/v2`; an absent,
legacy, mixed, or future schema is `UNSUPPORTED` and fails closed without applying
v2 field rules to unrelated bytes. Production stories require a valid registry,
current control manifest, Approved GDD binding, active TR, and a fully current
producer Source Manifest and Currentness Matrix. `LEGACY-UNTRACED` is explicit
`NEEDS_WORK`, never READY and never a bypass for an unavailable source.

## Deterministic checks and stable findings

Evaluate every applicable check ID from `SR-C001` through `SR-C016`. A check
result is exactly `PASS`, `FAIL`, `BLOCKED`, `NOT_APPLICABLE`, or `UNVERIFIED` and
contains applicability, inputs/revisions, deterministic assertion, evidence locators,
finding IDs, and check-version revision.

N/A is allowed only where the rules explicitly permit it and must include current
positive evidence and a reason. A source absence is not positive N/A evidence.

Every non-pass creates `cgs.story-readiness-finding/v1` with a deterministic
`SRF-<stable-finding-key>` ID, check/story identity, classification, current observation
state, owner, external action, optional dependency ID, exact evidence, resolution
condition, first-seen reference when available, and current snapshot revision.
Diagnostic wording, line number, verdict, timestamp, and source byte count and revision do not
control finding identity.

Finding classification is `GAP`, `BLOCKER`, or `WARNING`. Observation is
`OPEN`, `STILL_OPEN`, `RESOLVED_CANDIDATE`, or `WAIVER_PRESENT`. This analysis
does not persist lifecycle changes. A waiver remains evidence and never converts a
failed/blocked required check into `PASS` or `READY`.

## Required design and architecture joins

A production story passes design traceability only when:

1. it declares a stable system ID, exact canonical GDD path/revision, and stable GDD
   requirement ID/locator;
2. `systems-index.md` has exactly one matching system entry whose path/revision match
   current GDD raw bytes and whose status is exactly `Approved`;
3. the GDD identifies the same system/requirement and its canonical status is
   `Approved` where the schema requires a document status;
4. every exact story TR ID exists once in the current registry with
   `status: active`, maps to that system/GDD requirement, and has no unresolved
   supersession; and
5. every governing ADR exists, revisions exactly, and has `Status: Accepted`.

A missing/invalid critical source, Proposed/missing ADR, non-Approved GDD, stale
index/gdd revision, or ambiguous join is a `BLOCKER`. A story-local missing/malformed
binding with otherwise available authority is a `GAP`. No filename, quoted prose,
old record, waiver, or inferred system substitutes for the stable joins.

For `cgs.story/v2`, recompute and compare the producer-owned `Source Manifest ID`
and `Story Core revision`, then validate every required row in `Source Manifest and
Currentness Matrix` against current exact bytes/state. The current control artifact,
its external review/ACTIVE receipt when required, and every applicable stable Rule
ID must match the control rows and exact bindings in the story. `Manifest Version`,
`manifest revision`, and a `## Source Snapshot` section are not fields produced by
`cgs.story/v2`; their absence is never a failure under this adapter and their
presence never substitutes for the producer fields. Missing, malformed, incomplete,
or stale producer fields or unavailable/invalid authority fail closed. Notes,
waivers, and accepted risk never rewrite provenance or produce READY.

## Story schema, AC, Test ID, and dependency validation

The rules reference defines the adapter-specific canonical story fields. For
`cgs.story/v2`, `Story Slot: SNNN` owns the ID suffixes. In particular:

- every acceptance criterion has one unique `AC-SNNN-CC` ID whose story-slot
  component matches the header and a specific observable assertion; required
  counts depend on declared story type;
- every current AC has exactly one unique type-correct
  `TC|MC|SC-<epic-slug>-SNNN-ACCC` ID, whose epic, story-slot, and criterion-slot
  components match the current story and AC, with no orphan or ambiguous mapping;
- Logic/Integration use `TC`, Visual/Feel/UI use `MC`, and Config/Data use `SC`;
  directly authored and imported QA specifications obey the same ID/cardinality
  and type-specific evidence rules;
- imported QA-plan evidence is usable only when plan bytes, effective `CURRENT`
  state, complete source manifest, exact story path/revision, AC set, Test ID set, and
  one-to-one Test-ID definition are current;
- dependencies use unique stable story IDs, canonical paths, explicit hard/soft
  kind, current declared revision/statuses, and resolution conditions; and
- a hard dependency passes only when its current story state is `Complete` or
  `Done`. Missing, unreadable, Draft, Blocked, Ready, or In Progress hard
  dependencies are blockers.

Do not infer IDs from headings or line order. Placeholder, duplicate, malformed,
or conflicting AC/Test/dependency IDs are gaps or blockers as fixed by the rules.

## Asset dependency classification

Normalize every declared or detected asset reference as exactly:

```text
EXISTING | PLANNED_WITH_STORY | BROKEN | UNKNOWN
```

- `EXISTING` requires one safe canonical path whose current file exists.
- `PLANNED_WITH_STORY` requires a declared stable dependency story ID/path whose
  scope explicitly produces that asset. Hard is the default. Until a hard asset
  dependency is `Complete`/`Done` and the asset exists, the story is `BLOCKED`.
- `BROKEN` is a missing path with no valid producing story, or a completed producer
  whose promised asset is absent; it is `NEEDS_WORK` unless another required
  dependency rule is stricter.
- `UNKNOWN` is ambiguous, unsafe, unreadable, unsupported, or over-limit evidence;
  it makes evaluation partial and cannot pass.

Asset existence checks content presence only. They do not validate art/audio/model
quality. Planned assets are never disguised as ordinary broken references.

## QA review and batch isolation

After deterministic checks, full mode sends one immutable
`cgs.story-readiness-qa-packet/v1` per story to QL-STORY-READY. Each packet binds
story/context/check-result revisions and contains story type, verbatim ACs with IDs,
GDD/TR requirement text, dependencies, base verdict, and stable deterministic
findings. Reviewer output cannot change deterministic evidence.

Dispatch `qa-lead` through Codex subagent delegation using gate
`QL-STORY-READY` from `.codex/docs/director-gates.md`. A bounded batch may be
dispatched together, but packet ownership and returned verdict/finding identity
remain one story at a time; never ask the reviewer for a batch-wide verdict.

Normalize one result per packet/story:

| QA result | Final effect |
|---|---|
| `ADEQUATE` | keep deterministic verdict |
| `GAPS` | create stable QA gaps; final is at least `NEEDS_WORK` |
| `INADEQUATE` | create stable QA blockers; final is `BLOCKED` |
| timeout, unavailable, malformed, duplicate, missing, or revision mismatch | QA check `UNVERIFIED`; final is `BLOCKED` |

Accepted risk never upgrades the result. In a batch, a failed/missing QA result
affects only its story. Preserve completed per-story results, mark the run
`RUN_PARTIAL` when any packet is incomplete, and never collapse reviewer prose
into an untraceable batch-wide finding.

## Verdict and run outcome

For each story, compute the deterministic base verdict from current check rows:

1. any `BLOCKED` check/finding -> `BLOCKED`;
2. otherwise any `FAIL` or `UNVERIFIED` required check -> `NEEDS_WORK`;
3. otherwise all applicable checks `PASS` or permitted `NOT_APPLICABLE` -> `READY`.

Then merge the QA result using the strict table above. `READY` additionally
requires `evaluation_state: COMPLETE`, complete mutation snapshots, and zero
unknown required evidence. List gaps even when a stricter blocker controls.

Run outcome:

- `RUN_BLOCKED` when scope/sprint identity cannot resolve or no story can be
  meaningfully evaluated;
- `RUN_PARTIAL` when at least one selected story is not evaluated completely,
  exceeds limits, changes during the run, or lacks a required full-mode QA result,
  while at least one independent result is retained; or
- `RUN_COMPLETE` when every selected story has a complete final result.

A run may be `RUN_COMPLETE` while containing `NEEDS_WORK` or `BLOCKED` stories;
completion describes evaluation coverage, not readiness.

## Readiness record candidate and independent recorder

Return one `cgs.story-readiness-record-candidate/v1` per evaluated story containing
story ID/path/declared revision, selected adapter ID and producer SKILL/contract/bundle
revisions, checked-at UTC time,
checker/ruleset ID/version/revision, review mode, full context/source snapshot,
producer Source Manifest ID/Story Core revision, stable check rows/findings, base/QA/final
verdicts, evaluation state, record/readiness keys and revisions, and exact
`expires_when` conditions.

Every direct candidate states:

```text
persistence_status: NOT_PERSISTED
implementation_gate_eligible: false
record_mutated: false
recorder_invoked: false
```

`cgs.story-readiness-recorder/v1` in the rules reference is a separate writer. It
requires new exact authorization and independently rehashes every source, verifies
the candidate/verdict, performs a CAS append to an owner-declared readiness
registry, and emits a persistence receipt. This skill never dispatches or simulates
it. A record is stale immediately when any story, GDD, systems index, registry/TR,
ADR, control manifest, dependency, asset, AC/Test/QA-plan, sprint/current-context,
story adapter/producer SKILL/contract/bundle, review-mode, reviewer-result, checker,
or ruleset identity changes.

## Return and stop

Return `cgs.story-readiness-run/v2` with normalized invocation, run outcome,
scope/sprint identity, limits/continuation, source coverage, mutation evidence,
and the ordered independent per-story results. Each result includes current source
revisions, checks, stable findings with owner/action/evidence/resolution, QA result,
verdict derivation, record candidate/revision, and stale key.

Every run envelope states:

```text
allowed_write_set: []
record_mutated: false
recorder_invoked: false
implementation_started: false
```

For sprint scope, flag each Must Have/Should Have non-ready story from the exact
validated plan. Do not recommend implementation for a non-ready or unpersisted
result. Offer conversation-only drafting help for story-local gaps, then stop;
never edit or invoke another workflow.
