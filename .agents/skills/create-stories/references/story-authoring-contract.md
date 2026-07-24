# Create Stories — Identity, Evidence, Slicing, and Transaction Contract

This contract is normative for `$create-stories`. It defines the bounded
one-epic source closure, stable story/acceptance/test identities, vertical-slice
and dependency rules, exact readiness-candidate semantics, per-story partial
handling, inventory/idempotency, append-only trace, and the only permitted
compare-and-set publication.

## 1. Authority and owned artifacts

`$create-stories` is a planning author, not a product-rule, architecture,
test-plan, final-readiness, implementation, or lifecycle authority.

| Information | Authority | Story treatment |
|---|---|---|
| Epic scope/module/system/dependency intent | Current exact epic and its source snapshot | Bounded decomposition input |
| Product behavior and acceptance outcome | Current approved GDD requirement/criterion | Exact cited acceptance projection |
| Stable technical requirement | Current architecture/TR evidence | Exact current TR ID; never guessed |
| Technical realization | Current Accepted ADR/lifecycle evidence | Exact cited implementation constraint |
| Programmer control | Current control manifest and applicable stable Rule IDs | Source-faithful projection |
| Priority | Current epic/GDD planning authority | Exact value/provenance; never inferred from order |
| Test specification | Current exact QA-plan item or bounded concrete author/QA proposal | Exact stable Test ID and AC binding |
| QA adequacy | One bounded read-only QA assessment | Per-story advisory input only |
| Final implementation readiness | Separate `story-readiness` evidence | Never authored or recorded here |

For one explicit epic, the only persistent outputs are:

1. direct-child story files
   `production/epics/<epic-slug>/story-<NNN>-<slug>.md`; and
2. the sibling `production/epics/<epic-slug>/STORIES.md`, using
   `cgs.story-registry/v2` for the current Story Registry plus append-only Story
   Identity, Criterion Allocation, and Batch History ledgers.

The source EPIC and global epics index remain owned by `create-epics` and are
read-only here. The broad catalog glob `production/epics/**/*.md` is an admissibility envelope,
not ownership of every matching file. This workflow never creates or repairs an
epic, GDD, architecture/TR map, control manifest, ADR/lifecycle/review record, QA
plan, final readiness receipt, sprint, implementation, test file, session state,
catalog, or test result.

Every publication is per-file atomic after one batch CAS. Cross-file atomicity is
not claimed. A mid-publication failure is `PARTIAL_WRITE` with exact observed
hashes; it is never reported as a successful batch or silently rolled back.

## 2. Canonical invocation and root/path rules

Supported forms:

```text
$create-stories author <epic-path>
  [--batch-size <1..12>]
  [--cursor <cgs.story-batch-cursor/v1 token>]
  --epic-receipt <path> --expect-epic-receipt <sha256:...>
  [--qa-plan <path> --expect-qa-plan <sha256:...>]
  [--qa-review <path> --expect-qa-review <sha256:...>]

$create-stories audit <epic-path>
  [--epic-receipt <path> --expect-epic-receipt <sha256:...>]
  [--qa-plan <path> --expect-qa-plan <sha256:...>]
  [--qa-review <path> --expect-qa-review <sha256:...>]
```

The epic path must be an explicit canonical project-relative path matching
`production/epics/<one-segment-slug>/EPIC.md`. Reject bare slugs, discovery,
globs, directories, newest/nearest selection, traversal, root escape, symlink
escape, unknown/duplicate flags, invalid batch size, path without its expected
hash, and path plus inline evidence for the same record.

`audit` is strictly read-only. It creates no candidate, approval request,
temporary file, report, QA delegation, cursor file, or persistent mutation.

## 3. Bounded source and target manifest

Freeze one repository-root identity and UTC snapshot. Record normalized
project-relative path, real-path/root result, role, stable source ID, consumed
scope, state, revision, exact raw-byte SHA-256, or explicit
`ABSENT|UNREADABLE`.

Hard ceilings:

| Class | Count | Per file | Class bytes |
|---|---:|---:|---:|
| Workflow catalog | 1 | 512 KiB | 512 KiB |
| Selected `cgs.epic-plan/v2` | 1 | 2 MiB | 2 MiB |
| Create-epics result receipt | 1 | 2 MiB | 2 MiB |
| Story registry `STORIES.md` or ABSENT | 1 | 2 MiB | 2 MiB |
| Direct-child epic inventory entries | 256 | 512 KiB | 16 MiB |
| Current architecture/TR artifact | 1 | 2 MiB | 2 MiB |
| Architecture/TR review/lifecycle evidence | 2 | 2 MiB | 4 MiB |
| Current control manifest | 1 | 2 MiB | 2 MiB |
| Control review/ACTIVE receipt | 2 | 2 MiB | 4 MiB |
| Current approved GDDs linked by the epic | 16 | 2 MiB | 16 MiB |
| GDD approval evidence | 16 | 512 KiB | 8 MiB |
| Governing ADRs | 32 | 512 KiB | 12 MiB |
| ADR lifecycle/review evidence | 32 | 256 KiB | 8 MiB |
| Explicit QA plan | 1 | 2 MiB | 2 MiB |
| Explicit QA assessment | 1 | 2 MiB | 2 MiB |

The complete exact-byte read budget is 48 MiB. Stop `BLOCKED_LIMIT` before
synthesis if any count, per-file, class, or total limit would be exceeded. Do not
sample, truncate, skip a source, raise a limit, or call incomplete coverage
complete.

Layered loading:

1. read catalog, EPIC header/source snapshot/provenance, create-epics receipt,
   story-registry ledgers, architecture/TR indexes, control header/coverage indexes, and supplied evidence
   envelopes;
2. enumerate only direct children of the selected epic directory and build the
   complete intended story inventory;
3. construct and hash the complete ordered source/target manifest;
4. validate exact currentness before loading GDD acceptance, ADR implementation,
   control-rule, or QA item bodies;
5. load only sections linked by the selected epic/TR/rule/QA closure; and
6. re-hash every complete source, target, and directory membership before approval
   and CAS.

Never recursively enumerate `production/epics`, all GDDs, all ADRs, engine
source, QA directories, sprints, or test files. Hashing a file does not authorize
unbounded semantic ingestion.

Canonicalize the ordered manifest as UTF-8/LF JSON with lexicographic keys and
arrays sorted by role, stable ID, normalized path, and scope:

```text
source_manifest_id = sha256:<canonical ordered source/target manifest>
```

Any byte, state, real path, revision, membership, role, scope, or evidence change
changes the identity.

## 4. Current epic, GDD, TR, ADR, and control admission

### Epic

Mutation requires one current supported epic with:

- schema `cgs.epic-plan/v2`;
- canonical `epic_id: EPIC-MODULE:<module_id>`, module ID, sorted system IDs,
  layer/order, canonical slug/path,
  and legal epic state;
- exact GDD/architecture/TR/control/ADR source-snapshot paths and hashes;
- exact `cgs.epic-source-manifest/v2` identity/hash and downstream
  Story-Creation Contract;
- current append-only provenance with no duplicate identity or path owner; and
- one exact `cgs.create-epics-result-receipt/v1` that binds the current epic
  path/hash, source manifest, module map, dependency graph, authorization, writer,
  and observed COMPLETE artifact state.

A legacy or malformed epic may be audited but cannot be mutated or silently
retrofitted. Missing/stale source snapshot or receipt, ambiguous module/system
mapping, or a non-current epic blocks authoring for the whole epic. A current
epic with Planning Status BLOCKED may be decomposed only when its stable
per-TR findings and Story-Creation Contract make affected and unaffected scope
deterministic; affected stories remain BLOCKED and the batch cannot be COMPLETE.

### GDD and acceptance source

Each admitted product statement comes from a current exact GDD hash with current
independent `APPROVED` evidence for the applicable content profile. Status text,
filename, epic prose, architecture prose, or a prior story never approves a GDD.

Record source artifact/requirement ID, path, section, stable locator, exact
criterion excerpt, excerpt hash, complete source hash, approval record ID/hash,
and applicable system/epic IDs. If a source-owned requirement/criterion ID is
absent, use the approved exact path/locator/excerpt fingerprint and treat later
identity drift as an explicit migration, never fuzzy continuity.

### TR

Admit a TR only from current architecture/TR evidence when its stable ID,
source requirement/approval hashes, `currentness: CURRENT`, and
`mapping_state: DERIVED_COVERED|DECISION_GAP` reproduce exactly.

- `DERIVED_COVERED` may support an AUTHOR_COMPLETE planning artifact when all other evidence is
  current.
- `DECISION_GAP` keeps only stories covering that TR `BLOCKED`.
- `CHANGED|STALE|UNBOUND|SOURCE_BLOCKED|UNKNOWN`, provisional mapping,
  duplicate identity, or migration ambiguity blocks only affected stories unless
  it corrupts the epic-wide identity ledger.

Never invent, repair, renumber, migrate, or write a TR. Placeholder values,
including every `TR-???` form, are forbidden in memory, previews, and files.

### ADR

An ADR is `ACCEPTED_CURRENT` only when exact path/hash, stable ADR ID,
Accepted lifecycle transition, recorder identity/time, independent review,
dependency/supersession chain, and TR coverage are current and non-conflicting.

Missing, Proposed, Superseded, Rejected, stale, unbound, or conflicting ADR
evidence blocks only stories whose TR/slice requires that ADR. Unrelated stories
continue. `ADR: N/A` is valid only when current epic/TR evidence owns reason
code `NO_ARCHITECTURAL_DECISION_REQUIRED`; the story author cannot invent it.

### Control manifest

Read `cgs.control-manifest/v2` and validate exact artifact, source-manifest,
ruleset, payload, version, immutable provenance, conflict/unknown state, and any
external review/ACTIVE receipt. Project rules only by stable Rule ID and preserve
`MUST|MUST_NOT|SHOULD|SHOULD_NOT|MAY`, full scope, conditions, source, and
qualifications.

An absent, DRAFT/PARTIAL, stale, unreviewed, non-ACTIVE, conflicting, or
unsupported control manifest may support explicit `BLOCKED` planning stories
only; it cannot support `AUTHOR_COMPLETE`. Contextual rejection is never
converted into prohibition.

## 5. Stable story, slot, acceptance, test, and dependency identities

### Story key and ID

Build one canonical `story_key` from:

```text
(epic_id,
 sorted stable source requirement identities,
 sorted current TR IDs,
 one stable observable slice-boundary ID,
 slice-contract version)
```

Identity excludes title, prose summary, priority, extraction order, display
order, filename slug, date, and batch membership.

```text
story_id = STORY-<first 16 lowercase hex of sha256(canonical story_key)>
```

The epic's append-only identity ledger owns a monotonic `story_slot: SNNN`.
Allocate the next never-used slot only for a genuinely new story ID. Never fill a
retired gap, recycle a slot/ID, suffix a collision, or renumber because stories
were reordered.

Preserve a story ID/slot only while the same stable epic/source/slice ownership
remains. A split, merge, moved criterion, changed fingerprint-owned source
identity, or changed observable slice boundary retires the old story and creates
new IDs/slots with explicit `supersedes_story_ids`. A source-owned stable
requirement ID whose approved wording changes may preserve identity while its
source/excerpt hashes and revision diff change.

Any full-hash collision, duplicate ledger owner, duplicate current path, or
conflicting persisted key is an epic-wide `IDENTITY_CONFLICT`.

### Story path

The canonical path is:

```text
production/epics/<epic-slug>/story-<NNN>-<display-slug>.md
```

`NNN` is the numeric part of the immutable slot. A title/display-slug change
does not authorize a rename; preserve the current path until a separate explicit
migration. Path identity is ledger-owned, not rediscovered from title.

### Acceptance IDs

Each criterion uses `AC-SNNN-CC`, where `SNNN` is the immutable story slot and
`CC` is a monotonically allocated two-digit criterion slot in that story.
Each row binds exactly one approved source criterion identity/locator/excerpt hash
and one or more exact TR IDs.

Preserve the AC ID while the same source criterion remains owned by the same story.
Never renumber on reorder/reword, recycle a retired criterion slot, duplicate one
source criterion across stories, or move an AC ID to a regrouped story. Split/
merge/move retires the old AC ID and allocates a new one under the new story.

### Test/check IDs

Every current AC has exactly the story-type-required stable ID:

- Logic/Integration: `TC-<epic-slug>-SNNN-ACCC`;
- Visual/Feel/UI: `MC-<epic-slug>-SNNN-ACCC`;
- Config/Data: `SC-<epic-slug>-SNNN-ACCC`.

One Test ID binds exactly one story ID, AC ID, method, owner/source plan, and
lifecycle state. Required fields are concrete:

- TC: Given, When, Then, edge cases, observable assertion, evidence path/schema;
- MC: setup, verify, unambiguous pass condition, evidence path/schema/sign-off;
- SC: setup/data fixture, action/load, observable pass condition, evidence
  path/schema.

Blank, `TBD`, `TODO`, `???`, “fill later,” duplicate, ambiguous, wrong-type,
or multi-AC bindings are missing coverage. Test IDs are never assigned by QA-plan
mtime, filename, title, or prose similarity.

### Dependencies

Every dependency records stable story ID, canonical path, exact current story or
candidate core hash, `HARD|SOFT`, reason/source ID, and status. Cross-epic
dependencies require an explicit current target; they are never discovered by
title.

The full candidate/current graph must be unique, acyclic, and deterministically
topologically sortable. A missing/ambiguous hard dependency or cycle blocks only
affected dependent stories unless the graph/ledger identity is corrupt.
Display/topological order never changes story identity.

## 6. Vertical-slice contract

One story owns one independently observable behavior or enabling outcome. Its
acceptance set, implementation boundary, tests, and completion evidence must be
coherent in one focused implementation transaction.

A valid slice:

- has one stable observable slice-boundary ID and one primary outcome;
- maps no more than 4 current TR IDs and 8 current AC IDs;
- has one primary story type, with secondary disciplines explicitly listed;
- crosses necessary layers/components when that is required to demonstrate the
  outcome;
- states exact in-scope/out-of-scope ownership and does not duplicate an AC;
- has no more than 4 hard direct dependencies; and
- can be verified independently when its hard dependencies are satisfied.

Do not create horizontal “all backend,” “all UI,” “all tests,” or “all data”
stories when the source behavior requires an end-to-end slice. A single-layer
enabling story is valid only when an exact epic/Accepted-ADR dependency requires
it first and its own observable outcome/ACs are independently verifiable.

Oversized, multi-outcome, cyclic, duplicate-AC, or unobservable candidates are
`SLICE_GAP`. Split them deterministically along source-owned behavior boundaries;
never split solely to satisfy a file count. If no evidence-backed boundary exists,
keep the affected candidate `BLOCKED` for a scope decision.

## 7. QA-plan binding, capped per-story QA assessment, and readiness separation

### Exact QA-plan selection

Use a QA plan only when explicitly supplied by exact path plus expected raw hash
or exactly linked by the current epic. Never choose “latest” or search by sprint,
epic title, story slug, or modification time.

For every imported item require exact:

```text
(qa_scope_id_or_sprint_id,
 epic_id,
 story_id,
 canonical story path,
 captured_story_artifact_sha256,
 story_core_sha256,
 ac_set_sha256,
 AC ID,
 Test ID)
```

The plan and every captured source must be CURRENT, complete, uniquely bound, and
hash-valid. The captured story artifact hash must equal the current exact raw
story bytes; core and AC-set hashes are deterministically recomputed from those
bytes and compared with the imported item set. A same-name item from another
sprint/epic/story is unrelated.
PARTIAL/STALE/ambiguous/mismatched evidence is not imported.

`story_core_sha256` is the canonical story source/scope/slice/AC/dependency
payload excluding QA specs, advisory review, final-readiness fields, revision
history, generated time, and hashes. This avoids self-reference while binding
tests to the exact behavior under test. The exact rendered artifact hash remains
external.

### One capped QA assessment

For `author`, validate a supplied current `cgs.story-qa-review/v2`; otherwise
request at most one read-only `qa-lead` assessment for the selected batch.
Hard cap: 12 stories, one attempt, 60 seconds, no retry, no nested delegation, no
mutation. Freeze one batch payload containing every story ID/path/core hash,
source-manifest ID, AC/Test mapping, types, test bodies, and limitations.

The result must return one separate record per story:

```text
story_id
received_story_core_sha256
verdict: ADEQUATE | GAPS | INADEQUATE | UNKNOWN
stable_finding_ids
coverage_by_AC_and_Test_ID
reviewer_task_id
no_mutation: true
```

Missing story result, payload/hash mismatch, duplicate/unknown story result,
malformed/late/partial/timeout/failed assessment, matching author identity, or
mutation is `UNKNOWN` for only affected stories. No batch-wide verdict may be
copied onto each story.

### Computed author status

Use the strictest applicable status:

- `BLOCKED`: required TR/GDD/ADR/control/dependency evidence is invalid or
  missing, slice/identity conflict exists, or QA verdict is INADEQUATE;
- `NEEDS_WORK`: no blocker, but priority, exact AC/Test mapping, concrete test
  fields, optional evidence, or QA verdict is incomplete/GAPS/UNKNOWN;
- `AUTHOR_COMPLETE`: all current epic/GDD/TR/Accepted-ADR/ACTIVE-control,
  priority, dependency, AC/Test, and per-story QA ADEQUATE predicates pass.

The same computed status must appear in preview, story, `STORIES.md` registry,
and result. It is never a template constant.

Every authored/changed story records:

```text
Readiness Verdict: NOT_EVALUATED
Readiness Evidence: NONE_CURRENT
```

`AUTHOR_COMPLETE` means only that this planning artifact is complete enough to
run the catalog-declared
`story-readiness` workflow. This author never emits final `READY`, writes or
retargets a readiness receipt, starts implementation, or lets QA/user risk
acceptance override failed current evidence. Any changed story byte invalidates a
prior readiness observation.

## 8. Canonical cgs.story/v2 schema

Render exact UTF-8/LF with these ordered sections:

1. Document Identity and Authority Boundary;
2. Epic/Story Identity and Revision;
3. Computed Author Status and Final Readiness Separation;
4. Priority, Layer, Type, and Observable Slice;
5. Source Manifest and Currentness Matrix;
6. Exact GDD/TR/ADR/Control Rule Bindings;
7. Acceptance Criteria with stable IDs and source spans;
8. In Scope / Out of Scope;
9. Implementation Constraints from accepted evidence;
10. QA Specifications and exact AC/Test bindings;
11. Required Evidence for this story type only;
12. Stable Dependency Graph;
13. Gaps/Findings and Resolution Owners;
14. Local Extensions under `x-local-*`; and
15. Immutable Revision History.

Required identity fields:

```text
Schema: cgs.story/v2
Story ID: STORY-<16 lowercase hex>
Story Slot: SNNN
Epic ID: <stable ID>
Canonical Path: production/epics/<slug>/story-NNN-<slug>.md
Revision: <positive monotonic integer>
Prior Artifact SHA-256: <sha256:... | ABSENT>
Source Manifest ID: sha256:<digest>
Story Core SHA-256: sha256:<digest>
Story Status: AUTHOR_COMPLETE | NEEDS_WORK | BLOCKED | RETIRED
Readiness Verdict: NOT_EVALUATED
Readiness Evidence: NONE_CURRENT
Priority: must-have | should-have | nice-to-have
Priority Source: <path + stable ID/locator + sha256>
```

The story never embeds its own current artifact hash. New revision is 1; a
content/provenance update is base + 1; exact no-op preserves version/time/history
and writes nothing.

Only the current story type's evidence contract is rendered. Do not emit the
other four type templates as if they were required.

Each actual update appends one immutable event with event ID, base/candidate
revision, base artifact hash, source-manifest/core hashes, changed stable IDs,
batch ID, generated-at UTC, and author task identity. Never edit/delete/reorder
prior events.

Unknown/manual content is allowed only in `x-local-*` sections and is preserved
without becoming authoritative. Unknown content elsewhere makes the base a
conflict.

## 9. Full-epic inventory and deterministic classification

`STORIES.md` uses `cgs.story-registry/v2`. Its canonical UTF-8/LF fields and
sections are:

```text
Schema: cgs.story-registry/v2
Epic ID: EPIC-MODULE:<module_id>
Epic Path: production/epics/<epic-slug>/EPIC.md
Epic Artifact SHA-256: sha256:<digest>
Create-Epics Receipt ID / SHA-256: <exact current receipt>
Epic Source Manifest ID / SHA-256: <exact current source manifest>
Registry Revision: <positive monotonic integer>
Prior Registry Artifact SHA-256: <sha256:... | ABSENT>
Current Registry Payload SHA-256: sha256:<canonical semantic payload>
```

Ordered sections are Authority Boundary, Current Story Registry, Story Identity
Ledger, Criterion Allocation Ledger, Retired/Superseded Identities, Batch History,
Local Extensions, and Registry Revision History. The current registry is a
derived projection; all allocation/retirement/history ledgers are append-only.
This author never embeds the registry's own current artifact hash.

On first safe publication the registry revision is 1. A semantic/trace update is
base + 1. Exact no-op preserves registry revision/time/history and writes nothing.
Unknown content is valid only under `x-local-*`; it cannot allocate identity or
override a current row.

Before decomposition, inventory:

- read-only EPIC identity/source snapshot/provenance and exact result receipt;
- `STORIES.md` current registry and append-only ledgers, or exact ABSENT state;
- every direct-child file and exact hash/ABSENT state;
- every supported story ID, slot, key hash, path, revision/history, AC/Test ID,
  dependency, local extension, and current status; and
- every collision by story ID, slot, path, key, source criterion, AC ID, and Test
  ID.

Decompose the complete current epic source closure in memory, reconcile it with
the inventory, then classify each logical story:

| Class | Condition | Action |
|---|---|---|
| `CREATE` | New identity/slot/path, target absent, no collision | Candidate revision 1 |
| `UPDATE` | Same identity/key/path, valid managed v2 base, deterministic content change | Candidate base + 1 and diff |
| `NO_OP` | Exact semantic/rendered equality and current trace | No write/event/approval |
| `RETIRE` | Current source/slice no longer owns a valid story and evidence proves replacement/removal | Retired candidate; never delete |
| `CONFLICT` | Identity/path/key/manual-content/preimage ambiguity | No write for affected target |
| `DEFERRED` | Outside selected bounded batch | Cursor/remaining work only |

Show stable-ID rule/AC/Test/dependency/source/status/history diffs. Never silently
delete, rename, merge, split, retarget, or overwrite a story.

A target-local conflict or source gap excludes only affected stories and makes the
batch PARTIAL; independent safe stories remain eligible for publication. A
duplicate/corrupt story registry ledger, conflicting registry ownership,
ambiguous epic identity/receipt, or source-manifest corruption blocks the whole
batch.

## 10. Bounded batch and deterministic partial result

Index the complete epic, then select at most `batch_size` logical story
mutations, default 8 and hard maximum 12. Selection order is:

1. current hard-dependency topological rank;
2. layer rank;
3. source requirement stable ID/locator;
4. story ID; and
5. canonical path.

Do not use title, file mtime, directory enumeration order, or prior display
number. A cursor is canonical `cgs.story-batch-cursor/v1` binding epic ID/hash,
source-manifest ID, inventory hash, ordering ruleset hash, last selected story ID,
remaining IDs, and cursor SHA-256. It is returned inline, never persisted.

Outcome:

- `COMPLETE`: every current logical story is NO_OP or safely published in this
  run, with no source/status/QA/conflict gap;
- `UNCHANGED`: complete inventory and sources match with zero mutations;
- `PARTIAL`: remaining DEFERRED stories, story-local BLOCKED/NEEDS_WORK/
  CONFLICT items, capped/failed QA, or publication uncertainty exists;
- `BLOCKED`: epic-wide identity/source/receipt/registry/CAS failure prevents safe
  publication;
- `DECLINED|ERROR`: explicit decline or invalid invocation/root/catalog.

One missing ADR never stops unrelated stories. A PARTIAL run reports exact
processed/deferred/blocked IDs and reproducible cursor; it never claims epic
completion.

## 11. Preview, approval, full CAS, and publication

Preview one exact changeset containing selected story CREATE/UPDATE/RETIRE paths,
the precise `STORIES.md` registry/append-only-ledger candidate,
all preimage hashes/states, complete stable-ID diffs, candidate bytes/hashes,
source manifest, QA result, append-only events, and every omitted/blocked item.

Use existing bounded authorization or obtain one approval for that complete
changeset. Approval is file authorization only—not source approval, QA approval,
final readiness, implementation, test evidence, or an epic completion claim.

Immediately before mutation:

1. re-read/re-hash the full source and target closure;
2. re-enumerate direct-child membership and unique registry/ledger ownership;
3. rebuild source manifest, decomposition, story keys/IDs/slots, AC/Test IDs,
   dependency DAG, status matrix, inventory classification, batch selection, and
   candidate bytes;
4. revalidate supplied/generated QA payload and exact per-story records; and
5. require every state/hash/identity/diff/cursor/candidate to equal the approved
   preview.

Any difference is `CAS_CONFLICT`: zero new mutations, no refresh/merge/retry,
and no reuse of authorization.

Publish selected files in the previewed order using same-directory temporary
files and atomic per-file create/replace. Re-read each result immediately and
verify exact bytes/hash/schema/ID/revision/status/readiness separation/
source/AC/Test/dependency/local-extension/history invariants. Publish
`STORIES.md` last and derive its current registry plus new append-only events
only from exact verified story results. Never mutate EPIC.md or the epics index.

If any write/readback fails, stop. Report exact verified, uncertain, unchanged,
and not-attempted paths/hashes as `PARTIAL_WRITE`. Never claim cross-file
rollback, delete a successfully written file, repair concurrent work, or report
COMPLETE.

## 12. Terminal report and routing

Return:

- workflow/profile/outcome and exact epic ID/path/hash/schema;
- catalog identity/hash and route state;
- source-manifest ID, budget use, inventory hash, batch ID/cursor;
- current GDD/TR/ADR/control evidence matrix;
- every story ID/slot/path/class/base/candidate/on-disk hash;
- story status, readiness NOT_EVALUATED, priority/type/slice/dependencies;
- exact AC/Test IDs and coverage;
- per-story QA verdict/finding IDs;
- append-only story-registry/story events and read-only epic receipt state;
- processed/deferred/blocked/conflict/gap counts; and
- exactly one catalog-derived next action or `Stop`.

Priority order for the one action:

1. repair epic-wide currentness/identity/receipt/registry evidence;
2. resolve the first deterministic affected GDD/TR/ADR/control/slice/QA gap;
3. continue the returned bounded cursor;
4. run catalog-declared `story-readiness` for the first exact
   AUTHOR_COMPLETE path/hash; or
5. Stop.

Never execute the next action, hardcode a gate/implementation/sprint command when
catalog policy is missing, or claim final READY, implementation started, epic
complete, test execution, or gate passage.
