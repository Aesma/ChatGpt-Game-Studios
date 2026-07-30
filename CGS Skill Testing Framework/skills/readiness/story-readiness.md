# Behavioral Test Spec: story-readiness

## Skill Summary

`story-readiness` is a bounded, strictly read-only gate. It evaluates each exact
story snapshot independently through the explicit
`cgs.story-v2-readiness-adapter/v1` against current Story, producer contract,
Source Manifest and Currentness Matrix, systems-index/GDD, TR registry, ADR,
control-manifest, dependency, asset, AC/Test, QA-plan, sprint, engine/current-
context, and optional QL-STORY-READY evidence. It returns stable check rows,
stable findings, `READY` / `NEEDS_WORK` / `BLOCKED`, and an unpersisted readiness-
record candidate. It never records the result or authorizes implementation.

This is a repaired catalog candidate and is **NOT EXECUTED**. Do not update
catalog `last_*` or pass/tested fields without immutable runner receipts bound to
the exact candidate revision.

## Contract Sources

- `.agents/skills/story-readiness/SKILL.md`
- `.agents/skills/story-readiness/references/readiness-rules-v1.md`
- `.agents/skills/story-readiness/references/continued-workflow.md`
- `.agents/skills/story-readiness/agents/openai.yaml`

Paths are relative to the formal candidate mirror root.

The compatibility fixture additionally reads exact current producer bytes at
`.agents/skills/create-stories/SKILL.md` and
`.agents/skills/create-stories/references/story-authoring-contract.md`. Their
pinned declared revision and `SKILL || 0x00 || contract` bundle revision are normative in
`readiness-rules-v1.md`; producer drift is an unsupported adapter input until an
independent compatibility update changes this candidate and its tests.

The sprint-selector compatibility snapshot is the final canonical `sprint-plan`
producer SKILL at
`revision:faff9fd8b5b40af18aac66269c3da5ca6ba6b5d868b7c57594280505bdf51901`
and its NOT-EXECUTED behavioral spec at
`revision:f5a996c490856617514c34d0697b6a9a284eb0f7e86cc9f434f34385605cf528`.
These revisions make this compatibility review reproducible; runtime sprint authority
still comes only from exact tracker/plan/source bytes, never from the test spec.

## State Machine

| Scope | Required input | Run result |
|---|---|---|
| one | exactly one canonical `--story` path | independent story result |
| sprint | exact declared `--sprint` ID plus valid tracker/plan/story-set authority | independent result per plan story |
| all | versioned v1 scope manifest and optional current cursor | bounded page of independent results |

Run outcomes: `RUN_COMPLETE`, `RUN_PARTIAL`, `RUN_BLOCKED`, `USAGE_ERROR`,
`INPUT_ERROR`. Per-story verdicts: `READY`, `NEEDS_WORK`, `BLOCKED`. Per-story
evaluation states: `COMPLETE`, `PARTIAL`, `NOT_EVALUATED`.

Direct record candidates are always `NOT_PERSISTED` and
`implementation_gate_eligible: false`. Recorder outcomes belong only to the
independent recorder fixture.

## Deterministic Fixtures

Use isolated repositories with stable clocks and declared revision fixtures for:

- exact story IDs/statuses/types, AC/Test tables, dependencies, assets, scope,
  engine/performance notes, and unresolved markers;
- exact `cgs.story/v2` producer contract bytes, `Source Manifest ID`, `Story Core
  revision`, and complete currentness matrices, plus legacy/mixed/future schemas;
- v1 scope/prior-record manifests and continuation cursors;
- exact `cgs.sprint-tracker/v2` trackers with declared revision, positive revisions,
  events, lifecycle owner/recorder, unique ACTIVE declarations, `plan_file`, raw
  `plan_revision`, plan revisions, story_set_revisions, capacity tuples, complete story
  rows, and corroborating selector sources, plus malformed/conflicting variants;
- systems index rows with system ID, Approved/non-Approved status, GDD path/revision;
- GDD files with stable system/requirement IDs and status;
- TR registries with active/deprecated/superseded/duplicate/mismatched entries;
- Accepted/Proposed/missing ADRs and current/stale control manifests;
- directly authored and imported QA plans with exact story/AC/Test/source binding;
- complete, partial, malformed, changed, and over-limit source sets;
- QL-STORY-READY reviewers producing one revision-bound result per story or injected
  timeout/malformed/cross-story output; and
- a separate failure-injectable readiness recorder with lock, CAS, atomic append,
  stale-source validation, and receipts.

Tests never invoke another project skill. Recorder tests call the independent
fixture directly, not through `$story-readiness`.

## Global Assertions

Every case asserts:

1. allowed write set is empty; no story, plan, tracker, registry, record, cache, or
   evidence file changes;
2. each story result binds exact story/context/source/checker/ruleset revisions and
   checked-at time;
3. partial/unknown/changed required evidence cannot produce `READY`;
4. stable check/finding IDs do not depend on diagnostic wording, line, timestamp,
   source revision, reviewer, verdict, or severity;
5. one story's failure never overwrites or contaminates another story's completed
   result; and
6. no direct result is durable implementation authorization.

Every run envelope must contain `allowed_write_set: []`, `record_mutated: false`,
`recorder_invoked: false`, and `implementation_started: false`.

## Test Cases

### SR-T001 — Exact invocation grammar

**Given** valid fixtures for each of `--story`, `--sprint`, and bounded `--all`.

**When** each documented form is parsed with optional review/prior/cursor options
in any allowed order.

**Then** exactly one scope resolves, options occur at most once, and no positional,
implicit session-story, or recursive-glob scope is introduced.

### SR-T002 — Invalid grammar is not a readiness verdict

**Given** separate missing scope, combined scopes, positional story, unknown/
repeated option, unsafe path, malformed revision/cursor, invalid review value, and
scope-incompatible option invocations.

**When** parsing occurs.

**Then** each returns `USAGE_ERROR`, reads no story beyond input validation, writes
nothing, and does not emit READY/NEEDS_WORK/BLOCKED for a story.

### SR-T003 — Referenced manifest identity fails closed

**Given** revision-mismatched, malformed, unrelated, stale, duplicate-ID, and unsafe-
path all/prior manifests.

**When** input identity is frozen.

**Then** each returns `INPUT_ERROR`, no manifest entry is evaluated, and no stale
prior finding/record is accepted.

### SR-T004 — Story and source revision bind READY

**Given** a fully passing production story and current valid systems index, GDD,
TR registry, ADR, control manifest, dependency, test, asset, and context sources.

**When** one-story lean evaluation completes.

**Then** result is `READY`/`COMPLETE`, and the record candidate contains exact
story/source revision, checked-at UTC, checker/ruleset IDs/versions/revisions, checks,
finding_set_revision, stale predicates, readiness key, and candidate revision.

### SR-T005 — Any bound source change stales the old result

**Given** a prior READY record candidate and separate mutations to story, GDD,
systems index, registry/TR row, ADR, manifest, dependency, asset, QA plan, sprint/
context, review mode, reviewer result, checker, and ruleset.

**When** reuse/currentness is checked.

**Then** each change invalidates the prior candidate; path/verdict/mtime equality
cannot keep it current and no stale record is implementation-gate eligible.

### SR-T006 — Exact current sprint resolves through tracker and plan

**Given** exact raw `production/sprint-status.yaml` bytes with
`schema_version: cgs.sprint-tracker/v2`, positive tracker revision, stable event,
equal requested `sprint_id`/`active_sprint_id`, exactly one `sprint_state: ACTIVE`,
stable lifecycle owner/recorder, canonical `plan_file`, exact raw `plan_revision`,
plan revision/story_set_revision, matching dates/timezone/unit/capacity tuple, complete
story rows, and unique agreeing session/project-stage/milestone declarations. The
referenced `cgs.sprint-plan/v2` ID/revision and revalidate current story_set_revision
also agree.

**When** sprint scope resolves.

**Then** `cgs.sprint-tracker-v2-readiness-adapter/v1` is the only selected branch;
the tracker declared revision/event and full normalized authority tuple are
bound into context/readiness/stale keys, the exact plan story set is evaluated,
plan priority is preserved only for warnings, and no “most recent”/mtime choice
occurs.

### SR-T007 — Sprint authority conflict blocks selection

**Given** separate missing/invalid/legacy/unknown tracker schema, duplicate keys,
zero/multiple plans, requested/tracker/plan/session/project-stage/milestone ID
disagreement, zero/multiple ACTIVE declarations, inactive state, nonpositive or
changed tracker revision, event/owner/recorder mismatch, `plan_path`/`plan revision`
without canonical fields, `plan_file` escape, raw `plan_revision` mismatch, plan
revision/story-set mismatch, capacity/date/timezone/unit mismatch, duplicate or
incomplete story rows, ambiguous/missing story path, current story/core/readiness-
record/receipt mismatch, and stale timestamp cases.

**When** sprint scope resolves.

**Then** each returns `RUN_BLOCKED` before a sprint verdict summary, names the exact
conflict or `MIGRATION_REQUIRED`, never falls back to legacy aliases or another
adapter, does not choose a file by recency, and writes nothing.

### SR-T008 — All scope is bounded and resumable

**Given** a valid 70-story scope manifest under all caps except the 32-story page
limit.

**When** pages are evaluated.

**Then** page 1 covers ordinals 0–31, returns `RUN_PARTIAL` plus a cursor bound to
manifest/context/ruleset/result-set revisions; subsequent valid cursors cover the next
ordinals without duplicate/omission; no recursive glob occurs.

### SR-T009 — Changed cursor context cannot resume

**Given** a cursor from a completed page and a changed scope manifest, target,
context, checker/ruleset, next ordinal, or completed-result revision.

**When** resume is requested.

**Then** it returns `INPUT_ERROR`, never splices old/new results, and emits no
whole-scope count.

### SR-T010 — Per-story partial isolation

**Given** a batch where A is complete, B has an unreadable required source, and C
exceeds a reference limit.

**When** evaluation runs.

**Then** A retains its complete verdict/record candidate; B/C have independent
partial non-ready results and stable findings; run is `RUN_PARTIAL`; no batch-wide
finding replaces per-story evidence.

### SR-T011 — Approved GDD join passes only exact authority

**Given** one story whose system ID, GDD path/revision, and requirement IDs match one
Approved systems-index row and current Approved GDD rows.

**When** `SR-C003` runs.

**Then** it passes with exact index/GDD/requirement locators and revisions; a bare GDD
filename or copied prose is not the evidence used.

### SR-T012 — Non-Approved or stale GDD is blocked

**Given** separate absent/invalid systems index, duplicate system ID, Draft/
Proposed GDD status, index/current GDD revision mismatch, missing requirement, and
duplicate requirement ID fixtures.

**When** `SR-C003` runs.

**Then** each is `BLOCKED`, creates structured blocker(s) owned by the design/index
authority with external action/evidence/resolution condition, and cannot READY.

### SR-T013 — Story-local GDD binding gap is fixable, not inferred

**Given** valid current index/GDD authority but a story missing system ID, gdd revision,
or stable requirement locator.

**When** `SR-C003` runs.

**Then** it is `FAIL`/`NEEDS_WORK`, identifies the story owner/action and exact
binding needed, and does not infer it from title/path/text similarity.

### SR-T014 — TR registry fail-closed matrix

**Given** independent missing/unreadable/invalid/duplicate registry fixtures and
valid registry rows for missing, placeholder, unregistered, deprecated,
superseded, wrong-system/GDD/requirement, and exact active story TR IDs.

**When** `SR-C004` runs.

**Then** authority failures/duplicates are `BLOCKED`; story-local invalid/inactive
IDs are `FAIL`/`NEEDS_WORK` and name a unique current replacement when proven; only
the exact active join passes.

### SR-T015 — Legacy marker stays non-ready

**Given** `Traceability: LEGACY-UNTRACED` with a valid registry and, separately, an
unavailable registry.

**When** readiness runs.

**Then** the valid-registry case is `NEEDS_WORK`; unavailable authority is
`BLOCKED`; neither infers a TR or returns READY.

### SR-T016 — ADR status and N/A are exact

**Given** Accepted, Proposed, missing, duplicate-ID, and reasoned architecture-
neutral N/A fixtures.

**When** `SR-C005` runs.

**Then** exact Accepted revisions pass; Proposed/missing/invalid/duplicate block;
reasoned N/A passes only when no architecture choice is unresolved; generic “N/A”
or waiver text does not.

### SR-T017 — cgs.story/v2 control currentness matrix

**Given** a production story and separate missing/unreadable/invalid authority,
missing/duplicate/stale control rows, malformed/mismatched `Source Manifest ID`,
mismatched `Story Core revision`, non-current review/ACTIVE receipt, unresolved Rule
ID/locator, and fully matching producer-v2 fixtures.

**When** `SR-C006` runs.

**Then** every missing/stale case fails closed, the recomputed producer manifest/
core revisions and current Rule-ID locators pass, and dates/copied labels never hide
byte mismatch. Absence of legacy `Manifest Version`, `manifest revision`, or `## Source
Snapshot` does not fail the valid v2 fixture.

### SR-T018 — Notes and legacy fields cannot rewrite v2 provenance

**Given** stale v2 currentness/source/core evidence plus Manifest-Note, accepted
risk, waiver text, or matching legacy Manifest Version/revision/Source Snapshot fields.

**When** the control check runs.

**Then** captured/current revisions remain distinct, finding observation may say
`WAIVER_PRESENT`, check still fails, final cannot READY, legacy fields cannot
satisfy the v2 adapter, and no source is edited.

### SR-T019 — Stable check rows are complete and ordered

**Given** any meaningfully parsed story.

**When** deterministic evaluation completes.

**Then** one row for each applicable `SR-C001..SR-C016` appears in numeric order
with version/revision/applicability/inputs/evidence/status/finding IDs; prerequisites
produce explicit UNVERIFIED rows rather than silently omitted checks.

### SR-T020 — Finding IDs survive irrelevant movement and wording

**Given** the same check/story/subject/defect key at changed line, diagnostic text,
timestamp, story/source revision, owner, reviewer, classification, and verdict.

**When** `srf-v1` is computed.

**Then** the `SRF-<20hex>` ID remains identical. Changing check, stable story ID,
subject ID/kind, or defect key changes the ID.

### SR-T021 — Findings carry actionable blocker structure

**Given** a hard dependency blocker, Proposed ADR blocker, story-local AC gap, and
unknown asset finding.

**When** findings normalize.

**Then** every row contains classification, observation, owner role,
external_action, dependency ID or NONE, exact evidence/revision/locator, and a
deterministic resolution condition; free-form blocker prose alone fails schema.

### SR-T022 — Prior finding comparison is read-only

**Given** a valid prior-record manifest with one still-current, one absent-under-
complete-coverage, and one waiver-referenced finding.

**When** comparison runs.

**Then** observations are `STILL_OPEN`, `RESOLVED_CANDIDATE`, and
`WAIVER_PRESENT`; verdict rules remain unchanged; no OPEN/RESOLVED/WAIVED state is
persisted. Incomplete current coverage cannot claim resolution.

### SR-T023 — Acceptance criteria require stable unique IDs

**Given** missing, placeholder, duplicate, malformed, insufficient-count,
non-observable, and valid type-appropriate AC fixtures.

**When** `SR-C007/SR-C008` run.

**Then** invalid rows fail with exact AC evidence; only unique `AC-SNNN-CC` rows
whose SNNN matches `Story Slot`, whose CC is a two-digit criterion slot, and which
meet type count/observability pass; Visual/Feel requires protocol/rubric/evidence
rather than subjective prose alone. Legacy `AC-<story-id>-NNN` is not required or
accepted as a v2 substitute.

### SR-T024 — Test IDs and AC coverage are bijectively auditable

**Given** duplicate Test ID, orphan AC reference, uncovered AC, ambiguous multiple
definitions, wrong evidence kind, conflicting target path, and valid many-tests-to-
one-AC fixtures.

**When** `SR-C008` runs.

**Then** every invalid case fails; each current AC has exactly one Test definition,
whose `TC|MC|SC` prefix matches story type and whose epic/SNNN/ACCC components
match canonical epic slug, Story Slot, and referenced `AC-SNNN-CC`. No ID is
inferred from headings/order and legacy `TEST-<story-id>-NNN` is not required.

### SR-T025 — Imported QA provenance must be fully current

**Given** separate QA plan revision mismatch, PARTIAL/STALE effective state, missing/
changed captured source, story path/revision drift, AC set drift, Test set drift,
duplicate/orphan imported Test, and exact CURRENT fixtures.

**When** imported QA evidence is validated.

**Then** only the exact current story/AC/Test/source binding passes; all other cases
are `FAIL`/NEEDS_WORK and cannot be waived into READY.

### SR-T026 — Hard dependency status matrix

**Given** a unique hard dependency in Complete, Done, Ready, In Progress, Draft,
Blocked, missing, unreadable, ID/path mismatch, and cycle variants.

**When** `SR-C010` runs.

**Then** only Complete/Done pass; every other current state is BLOCKED with stable
dependency ID, owner/external action, evidence, and exact resolution condition.

### SR-T027 — Soft dependency needs a real fallback

**Given** an existing soft dependency with and without a bounded nonblocking
interface/fallback, plus missing/Draft/Blocked soft variants.

**When** dependency validation runs.

**Then** only the existing non-conflicting dependency with valid fallback passes;
the others fail or block when functionally hard; free-text waiver does not alter
the result.

### SR-T028 — Existing assets are distinct from planned assets

**Given** readable existing paths, absent paths with unique producer stories, and
duplicate textual references.

**When** `SR-C011` runs.

**Then** existing files are `EXISTING`, valid absent producer rows are
`PLANNED_WITH_STORY`, references deduplicate by canonical path, and the two classes
are never reported as equivalent.

### SR-T029 — Planned hard asset blocks until delivered

**Given** an absent planned asset whose producer dependency is hard/default and
currently Ready or In Progress.

**When** asset/dependency checks run.

**Then** asset is `PLANNED_WITH_STORY`, final is BLOCKED, finding includes producer
dependency ID/owner/evidence/resolution, and it is not mislabeled as an ordinary
broken path.

### SR-T030 — Broken and unknown assets remain distinct

**Given** absent asset with no producer, Complete producer whose asset is absent,
and unsafe/ambiguous/unreadable/over-limit asset paths.

**When** `SR-C011` runs.

**Then** the first two are `BROKEN`/FAIL/NEEDS_WORK; the others are `UNKNOWN`/
UNVERIFIED/partial; no unknown becomes pass or planned dependency.

### SR-T031 — Unresolved markers use structural context

**Given** TODO/TBD/UNRESOLVED/???/undecided markers in normative sections and
question marks only in URLs, quoted strings, test data, or resolved FAQ rows.

**When** `SR-C012` runs.

**Then** normative unresolved markers fail with exact locators; benign literal
question marks do not produce false blockers.

### SR-T032 — Full QA verdict mapping cannot be bypassed

**Given** complete packets with base READY/NEEDS_WORK/BLOCKED and ADEQUATE, GAPS,
INADEQUATE, timeout, missing, malformed, duplicate, cross-story, or revision-mismatched
results.

**When** `SR-C016` merges.

**Then** ADEQUATE keeps base; GAPS is at least NEEDS_WORK; INADEQUATE is BLOCKED;
invalid/unavailable is BLOCKED; accepted risk never upgrades; no proceed-anyway
path exists.

### SR-T033 — Batch QA returns one stable result per story

**Given** A receives ADEQUATE, B GAPS, C timeout, and D a cross-story result.

**When** full-mode batch review completes.

**Then** A/B keep independent complete outcomes, C/D are independently
UNVERIFIED/BLOCKED, stable QA finding IDs use their own packet/story/AC subjects,
run is partial, and no batch-wide verdict contaminates A/B.

### SR-T034 — Lean and solo skip only QA

**Given** lean and solo modes with deterministic gaps/blockers.

**When** evaluation runs.

**Then** `SR-C016` is permitted N/A with exact skip/source evidence, deterministic
checks still control verdict, and skipping QA cannot bypass GDD/TR/manifest or
dependency failures.

### SR-T035 — Verdict precedence is deterministic

**Given** check matrices for all-pass, FAIL-only, UNVERIFIED-only, BLOCKED plus
lower gaps, and partial all-pass cases.

**When** verdict computes.

**Then** results are READY, NEEDS_WORK, NEEDS_WORK, BLOCKED, and non-ready partial
respectively; all gaps remain listed beneath a stricter blocker; `RUN_COMPLETE`
describes coverage and may contain non-ready stories.

### SR-T036 — Direct readiness record is not persisted authority

**Given** a complete READY result.

**When** the skill returns.

**Then** its candidate is content/revision-bound but says `NOT_PERSISTED`,
`implementation_gate_eligible: false`, `record_mutated: false`, and
`recorder_invoked: false`; no recorder call, record path write, or dev-story
handoff as authorized work occurs.

### SR-T037 — Independent recorder revalidates sources and CAS

**Given** exact authorization/candidate/registry base and separate variants where
a stale-key source changes, candidate is already exact, registry base changes, or
all inputs remain current.

**When** the recorder fixture runs directly.

**Then** results are `STALE_CANDIDATE`, `ALREADY_RECORDED`, `CAS_CONFLICT`, or
`RECORDED`; only RECORDED writes atomically; conflicts/staleness preserve target
bytes and require fresh analysis/authorization; the recorder cannot upgrade a
non-ready candidate.

### SR-T038 — Recorder failure is atomic and auditable

**Given** injected prepare/flush/replace/post-verification failures.

**When** the recorder fixture executes.

**Then** result is `RECORDER_FAILED`, original registry bytes or exact absence
remain, no partial record becomes visible, and the receipt identifies the failed
stage without implementation eligibility.

### SR-T039 — Metadata and spec remain synchronized

**Given** SKILL, references, metadata, and this spec.

**When** static conformance runs.

**Then** exact scopes/outcomes/verdicts, 16 check IDs, v2 adapter identity and
producer SKILL/contract/bundle revision binding, stable finding schema, bounded/partial behavior,
current source joins, per-story QA isolation, record/recorder separation, and
NOT-EXECUTED test state agree without mutation or implementation-authorization
contradictions.

### SR-T040 — Exact create-stories cgs.story/v2 output is consumable

**Given** exact current create-stories SKILL and producer-contract bytes whose raw
paths and declared producer versions equal the adapter's supported values, plus a conforming
`cgs.story/v2` artifact with `Source Manifest ID`, `Story Core revision`, complete
Source Manifest and Currentness Matrix, `AC-SNNN-CC`, and one type-correct
`TC|MC|SC-<epic>-SNNN-ACCC` row per AC, with no `Manifest Version`, `Manifest
revision`, `## Source Snapshot`, or legacy AC/TEST ID fields.

**When** `cgs.story-v2-readiness-adapter/v1` parses and recomputes the producer
manifest/core identities before `SR-C001..SR-C015` run.

**Then** adapter/schema/identity checks pass, absence of non-produced legacy fields
creates no finding, exact currentness and AC/Test bindings remain auditable, and
the story may reach READY only if every independent readiness check passes.

### SR-T041 — Unsupported or mixed producer schema fails closed

**Given** separate absent-schema, legacy-only, future-schema, duplicate-v2-marker,
mixed legacy/v2-ID, copied-reference ID-without-matrix, and producer-contract_revision-drift
fixtures.

**When** adapter selection and currentness validation run.

**Then** no guessed adapter or legacy fallback is used; source status is
`UNSUPPORTED` or invalid as applicable, the result names `MIGRATION_REQUIRED` or
the exact repair condition, READY and gate eligibility remain false, and no file
or recorder is mutated.

## Static Conformance Checks

The candidate passes static conformance only when:

- SKILL frontmatter has exactly `name` and `description`; metadata YAML parses and
  names one/sprint/bounded-all plus the read-only recorder boundary;
- every SKILL Markdown link resolves inside the formal mirror;
- all three scope grammars, five run outcomes, three verdicts, and three evaluation
  states match across contracts and spec;
- all 16 stable check IDs are present exactly once in the registry and evaluation
  order is fixed;
- the one supported production branch is exact `cgs.story/v2`, binds the adapter
  and pinned producer SKILL/contract/bundle revision, and rejects producer drift or
  legacy/mixed/future schemas without a guessed fallback;
- source snapshots include Story, producer Source Manifest ID/Story Core/currentness
  rows, systems-index/GDD, TR registry, ADRs, control manifest, dependencies/assets/
  tests, and applicable sprint/current context;
- READY candidates include story/source revision, checked-at, checker/ruleset,
  checks/findings, verdict, stale predicates, and false persistence/eligibility;
- sprint resolution selects only `cgs.sprint-tracker/v2`, binds tracker declared revision/
  positive revision/event and unique ACTIVE declarations, consumes `plan_file` plus
  raw `plan_revision`, and verifies complete tracker/plan tuple, story rows, revision,
  and revalidate story_set_revision without legacy aliases or recency;
- all scope is manifest-bound, capped, paged, and continuation-bound; per-story
  partials survive batch failures;
- systems index/GDD requires stable system/path/revision/Approved status and stable
  requirements; active TR and Accepted ADR joins are exact;
- v2 AC/Test IDs are exact `AC-SNNN-CC` and type-correct
  `TC|MC|SC-<epic>-SNNN-ACCC`, with matching components and exactly one current
  Test per AC; producer-absent legacy fields/IDs are not required;
- dependency and asset classifications have deterministic status/verdict effects;
- every finding has stable identity, owner, action, evidence, and resolution;
- full QA has per-story packets/results and strict no-bypass mapping;
- direct output never writes/invokes a recorder, and recorder CAS/staleness/
  atomicity is independently specified; and
- catalog test/pass fields remain unchanged because this spec is not executed.

## Audit Traceability

| Audit item | Closing contract | Primary tests |
|---|---|---|
| SR-004 | story and every current source revision, checked-at, checker/ruleset, stale predicates in each record candidate | SR-T004–SR-T005, SR-T036–SR-T038 |
| SR-005 | exact cgs.sprint-tracker/v2 declared revision/unique-ACTIVE authority plus plan_file/raw-plan_revision/story-set resolution; no legacy aliases or recency choice | SR-T006–SR-T007 |
| SR-006 | independent per-story deterministic/QA/results, partial isolation, bounded continuation | SR-T008–SR-T010, SR-T033 |
| SR-007 | stable system ID plus exact systems-index/GDD path/revision/Approved status and requirement join | SR-T011–SR-T015 |
| SR-008 | stable check/finding schema with classification, owner, external action, dependency, evidence, resolution | SR-T019–SR-T022 |
| SR-009 | `EXISTING` / `PLANNED_WITH_STORY` / `BROKEN` / `UNKNOWN`, with hard planned producer blocked | SR-T028–SR-T030 |

P0 protections remain covered: registry/TR fail-closed (SR-T014–SR-T015), exact
v2 producer/current-control currentness without waiver override (SR-T017–SR-T018,
SR-T040–SR-T041), and strict full-mode
QA GAPS/INADEQUATE mapping (SR-T032–SR-T034). Dependency and AC/Test/QA-plan
validation are covered by SR-T023–SR-T027; read-only record/recorder separation by
SR-T036–SR-T038.
