---
name: create-stories
description: "Author one bounded batch of stable, vertically sliced cgs.story/v2 planning artifacts from an exact current epic and current GDD/TR/Accepted-ADR/control evidence, with per-story QA status, append-only identity trace, and full CAS; final readiness remains external."
---

# Create Stories

## Invocation

```text
$create-stories author <production/epics/<epic-slug>/EPIC.md>
  [--batch-size <1..12>]
  [--cursor <cgs.story-batch-cursor/v1 token>]
  --epic-receipt <path> --epic-receipt <revision:...>
  [--qa-plan <path> --qa-plan <revision:...>]
  [--qa-review <path> --qa-review <revision:...>]

$create-stories audit <production/epics/<epic-slug>/EPIC.md>
  [--epic-receipt <path> --epic-receipt <revision:...>]
  [--qa-plan <path> --qa-plan <revision:...>]
  [--qa-review <path> --qa-review <revision:...>]
```

Do not discover or choose an epic. Require the explicit canonical EPIC path.
Reject unknown/duplicate arguments, bare slug, glob, directory, traversal,
outside-root or escaping symlink path, invalid batch/cursor, malformed revision, an
evidence path without its required revision, or both path/inline forms.

Read
[references/story-authoring-contract.md](references/story-authoring-contract.md)
in full before processing. It is normative.

## Ownership and result vocabulary

This workflow decomposes one exact current epic and may mutate only:

- supported direct-child `story-NNN-<slug>.md` files in that epic; and
- the sibling `STORIES.md` current registry plus append-only Story Identity,
  Criterion Allocation, and Batch History ledgers.

The selected EPIC and global epics index are read-only. It never edits sources,
creates/repairs an epic, owns QA plans, writes final
readiness evidence, starts implementation, writes tests, or updates a sprint.
Except for the one capped read-only QA assessment defined below, it never
delegates decomposition, identity, slicing, status, drafting, inventory, or
publication.

| Field | Values |
|---|---|
| Workflow Outcome | `COMPLETE|UNCHANGED|PARTIAL|BLOCKED|DECLINED|ERROR` |
| Story Operation | `CREATE|UPDATE|NO_OP|RETIRE|CONFLICT|DEFERRED|FAILED` |
| Story Status | `AUTHOR_COMPLETE|NEEDS_WORK|BLOCKED|RETIRED` |
| Final Readiness | `NOT_EVALUATED` |
| Context State | `COMPLETE|PARTIAL|INVALID` |
| QA State | `ADEQUATE|GAPS|INADEQUATE|UNKNOWN|NOT_REQUESTED` |
| Route State | `READY|BLOCKED|UNKNOWN|NO_ROUTE` |

`AUTHOR_COMPLETE` is not `READY`. Only a separate current
`story-readiness` result for the exact final story bytes can issue final READY.

---

## Phase 0 — Freeze root and catalog contract

Resolve one repository root and UTC snapshot. Read exact raw bytes and lowercase
revision.

Read `.codex/docs/workflow-catalog.yaml` first. Require unique phase/workflow
IDs and exactly one `create-stories` command entry whose artifact envelope
contains the contract's exact story/STORIES targets. The broad glob does not grant
ownership over unrelated matching Markdown.

Bind exact unique catalog entries for the epic producer, QA-plan source,
story-readiness consumer, and any gap owner. An unversioned catalog is
`LEGACY_UNVERSIONED`; use declared fields only. Never infer a reviewer,
recorder, receipt schema, final-readiness transition, or next command from step
order, comments, filenames, or artifact presence.

Catalog target conflict is ERROR. A missing typed downstream route does not make
safe planning invalid, but its route is UNKNOWN/Stop.

---

## Phase 1 — Validate profile, epic identity, and bounded manifest

`author` and `audit` require the exact explicit EPIC path.

Mutation requires a valid current `cgs.epic-plan/v2` with canonical
`EPIC-MODULE:<module_id>`, stable module/system identity, slug/path,
layer/order/state, exact `cgs.epic-source-manifest/v2`, Story-Creation Contract,
append-only provenance, and one exact current
`cgs.create-epics-result-receipt/v1`. Legacy/malformed/stale epic artifacts are
read-only audit inputs and `BLOCKED_UNSUPPORTED_EPIC` for authoring. Never
retrofit them here.

Apply every count/per-file/class/48-MiB limit and the layered-loading algorithm
from the reference. Inventory only direct children of the selected epic
directory. Never recursively scan production epics, GDDs, ADRs, QA plans,
sprints, tests, or engine source.

Build one deterministic ordered source/target manifest before semantic drafting.
Record exact states/revisions for catalog, EPIC, create-epics receipt, STORIES
registry/absence, story inventory,
architecture/TR evidence, control manifest/review/ACTIVE receipt, exact GDDs and
approval evidence, exact ADR/lifecycle/review evidence, and explicitly supplied
QA evidence.

Any epic-wide identity ambiguity, source change, unreadable required input,
membership instability, or limit overflow blocks publication. Do not sample and
continue.

`audit` validates the complete closure, decomposition, stable identities,
inventory, AC/Test bindings, QA currentness, dependencies, status, append-only
trace, and drift inline. It produces no candidate, approval request, QA
delegation, temporary file, report, cursor file, or mutation.

---

## Phase 2 — Admit current authoritative evidence

### Epic/GDD

Treat the epic as bounded planning scope, not product truth. For every in-scope
requirement/criterion require the exact current approved GDD identity/path/revision,
stable source ID or exact approved stable business key, locator/excerpt revision, and current
independent approval evidence.

Epic summaries, stale source snapshots, filenames, Status text, prior stories,
and architecture prose never approve or replace GDD acceptance outcomes.

### TR

Admit exact stable TR IDs only from current architecture/TR evidence. Reproduce
source requirement/approval revisions, `CURRENT`, and
`DERIVED_COVERED|DECISION_GAP`.

- `DERIVED_COVERED` is eligible for normal decomposition.
- `DECISION_GAP` blocks only affected story candidates.
- stale/unbound/source-blocked/provisional/unknown/ambiguous/migrating TR evidence
  blocks only affected stories unless it corrupts epic-wide identity.

Never create, guess, repair, renumber, or write TRs. No placeholder TR may enter
memory, preview, story, STORIES registry, cursor, or result.

### ADR

For every TR/slice, validate exact ADR ID/path/revision, Accepted lifecycle record,
recorder identity/time, independent review, dependency/supersession chain, and
TR coverage.

Classify `ACCEPTED_CURRENT|PROPOSED|SUPERSEDED|REJECTED|STALE|UNBOUND|CONFLICT|
UNKNOWN|NOT_APPLICABLE_EVIDENCED`. Only ACCEPTED_CURRENT supplies
implementation constraints. Missing/noncurrent ADR evidence blocks the affected
story only. Do not stop unrelated story decomposition.

`NOT_APPLICABLE_EVIDENCED` requires exact current epic/TR reason code
`NO_ARCHITECTURAL_DECISION_REQUIRED`; never invent N/A.

### Control manifest

Validate exact `cgs.control-manifest/v2` artifact/source-manifest/ruleset/
payload/version/history and its independent review/ACTIVE receipt. Map applicable
rules by stable Rule ID and exact TR/scope intersection.

Preserve MUST, MUST_NOT, SHOULD, SHOULD_NOT, MAY, conditions, qualifications,
contextual rejection, guardrail, and source provenance. Never promote or suppress
a rule.

Non-ACTIVE, stale, PARTIAL/DRAFT, conflict/unknown, or unsupported control
evidence makes affected planning stories BLOCKED and ineligible for readiness,
but does not erase their planning value or stop independent safe stories.

---

## Phase 3 — Reconcile stable identities before grouping

Parse the `STORIES.md` append-only Story Identity/Criterion Allocation/Batch
ledgers and every supported story base.
Index story ID, canonical key revision, never-reused slot, path, revision/history,
source/AC/Test IDs, dependency IDs, local extensions, and status.

Detect duplicates/collisions by epic ID, story ID/key/slot/path, source criterion
ownership, AC ID, and Test ID. A corrupt/duplicate story-registry ledger or
ambiguous EPIC/receipt/registry owner blocks the whole run. A target-local unknown/manual
content conflict excludes that story and permits unrelated safe work as PARTIAL.

For each logical slice, compute the reference contract's canonical `story_key`
and `STORY-<epic-id>-<slice-boundary-id>`. Reuse an existing identity only when exact stable
epic/source/slice ownership matches. Allocate the next never-used SNNN only for a
new identity.

Do not derive identity from title, prose, priority, order, filename slug, date,
batch, or mtime. Split/merge/move/boundary change retires old IDs and creates new
story/AC IDs with explicit supersedes links. Never recycle a retired identity or
hide a collision with a suffix.

Preserve an existing canonical path on display-title changes. A rename requires a
separate migration owner and is never silently bundled.

---

## Phase 4 — Build verifiable vertical slices and dependencies

Start from exact current GDD criterion/TR ownership, not desired code files.
Create one independently observable behavior or evidence-backed enabling outcome
per story.

Enforce:

- one stable observable slice-boundary ID and primary outcome;
- at most 4 current TRs and 8 current ACs;
- one primary type from Logic, Integration, Visual/Feel, UI, Config/Data, with
  explicit secondary disciplines;
- necessary end-to-end component/layer reach;
- explicit in-scope/out-of-scope boundaries;
- no duplicated acceptance ownership;
- at most 4 hard direct dependencies; and
- independent verification after hard dependencies.

Do not split into horizontal component buckets when the behavior requires a
vertical path. Allow a single-layer enabler only with exact epic/Accepted-ADR
dependency evidence and its own observable acceptance outcome.

When an evidence-backed split boundary exists, split oversized/multi-outcome
candidates deterministically. Otherwise mark only the affected candidate
BLOCKED/SCOPE_DECISION_REQUIRED.

Build the full current/candidate dependency graph from stable story IDs and exact
paths/core revisions. Record HARD/SOFT plus reason/source. Reject fuzzy/title
matching. Cycles/missing hard dependencies block affected stories; display
topological order never changes identity.

---

## Phase 5 — Assign exact priority, AC IDs, Test IDs, and QA bindings

### Priority

Record `must-have|should-have|nice-to-have` only from exact current epic/GDD
planning evidence, with source ID/locator/revision. Missing/ambiguous priority is
NEEDS_WORK, never inferred from order/layer/type.

### Acceptance

Allocate/preserve `AC-SNNN-CC` from the append-only per-story criterion ledger.
Every AC binds one exact approved source criterion identity/locator/excerpt revision
and current TR IDs. Preserve on reword/reorder only when source ownership remains;
retire rather than move/recycle after regrouping.

### QA plan and Test IDs

Use a QA plan only from the explicit path/revision or unique exact epic link. Validate
its current state and exact tuple:

```text
(qa_scope_or_sprint_id, epic_id, story_id, canonical path,
 captured_story_artifact_revision, story_core_revision, ac_set_revision,
 AC ID, Test ID)
```

Never select by newest/mtime/title/slug or import same-named items from another
sprint/epic/story.

Each current AC receives exactly one type-correct stable ID:

- Logic/Integration `TC-<epic>-SNNN-ACCC`;
- Visual/Feel/UI `MC-<epic>-SNNN-ACCC`;
- Config/Data `SC-<epic>-SNNN-ACCC`.

Require every type-specific test/check field from the reference contract. Any
placeholder, blank, duplicate, ambiguous, wrong-type, or multi-AC Test binding is
missing coverage.

Assign explicit story_core_revision and AC-set revisions before QA content so exact
QA bindings do not self-invalidate.

---

## Phase 6 — Obtain one capped per-story QA assessment

For `author`, validate one explicitly supplied current
`cgs.story-qa-review/v2`; otherwise request at most one read-only `qa-lead`
assessment for the selected batch.

Hard cap: at most 12 stories, one attempt, 60 seconds, no retry, no nested
delegation, and no mutation. Bind one batch payload containing source-manifest ID
and every story ID/path/core revision, type, AC/Test mapping/body, and limitation.

Require a distinct per-story `ADEQUATE|GAPS|INADEQUATE|UNKNOWN` record, stable
finding IDs, exact received core revision, coverage by AC/Test ID, real reviewer
identity distinct from the author, and no-mutation confirmation.

Missing/duplicate/unknown/mismatched/late/partial/timeout/failed/self/mutating
results are UNKNOWN only for affected stories. Never apply one batch verdict to
all stories or fabricate a result.

QA adequacy is advisory to computed author status. It never creates final
readiness evidence.

---

## Phase 7 — Compute status and render cgs.story/v2

For every story use the strictest result:

- BLOCKED for required GDD/TR/ADR/control/dependency/slice/identity failure or QA
  INADEQUATE;
- NEEDS_WORK when no blocker exists but priority, AC/Test mapping/specification,
  optional evidence, or QA GAPS/UNKNOWN is incomplete;
- AUTHOR_COMPLETE only when all current evidence, type-specific QA specs, stable
  IDs, dependencies, ACTIVE control, and per-story QA ADEQUATE checks pass;
- RETIRED only with current removal/replacement evidence and append-only links.

Keep the same value in preview, story, STORIES registry, and result.
Never use a template default.

Render canonical UTF-8/LF `cgs.story/v2` using every ordered section and field
from the reference. Include stable story ID/slot/path, monotonic revision,
priority/provenance, source manifest/core revision, exact source matrix, rule IDs,
acceptance/test IDs, type-only evidence contract, dependencies, findings, local
extensions, and immutable history.

Every changed/current authored story says exactly:

```text
Readiness Verdict: NOT_EVALUATED
Readiness Evidence: NONE_CURRENT
```

It must never contain final READY. AUTHOR_COMPLETE is only authoring completion;
a later exact-revision story-readiness result owns final READY.

New revision is 1; content/provenance update is base + 1. Retire removed rules/
AC/Test/story identities instead of deleting them. Preserve valid `x-local-*`
content without treating it as authority.

Exact semantic/rendered no-op preserves revision/time/history/review observation
and writes nothing. The artifact never embeds its own current file revision.

---

## Phase 8 — Classify the complete inventory and select one bounded batch

Reconcile every logical current story with the full direct-child inventory and
classify exactly:

`CREATE|UPDATE|NO_OP|RETIRE|CONFLICT|DEFERRED`.

Show stable-ID/source/status/priority/slice/AC/Test/dependency/history diffs.
Never overwrite manual/unknown content, silently delete, rename, merge, split,
retarget, or recycle.

Index the entire epic, then select at most batch size, default 8 and maximum 12,
using hard-dependency topological rank, layer, source stable identity, story ID,
then canonical path. No selection by mtime/title/enumeration order.

One missing ADR/TR/QA result or target-local conflict affects only its stories.
Continue independent safe work and make the run PARTIAL. Epic-wide identity/
receipt/registry/source corruption blocks all publication.

If work remains, return the exact inline `cgs.story-batch-cursor/v1` binding
epic/source/inventory/order revisions and remaining stable IDs. Never persist cursor
or session state.

If all items are exact NO_OP, finish UNCHANGED without approval, timestamps,
history, temp files, or writes.

---

## Phase 9 — Preview one changeset, CAS, publish, and verify

Preview:

- every selected story CREATE/UPDATE/RETIRE path, preimage, candidate bytes/revision,
  and stable-ID diff;
- exact `STORIES.md` registry candidate and append-only allocation/batch events;
- source manifest/inventory/batch/cursor/QA identities;
- every DEFERRED/BLOCKED/CONFLICT item; and
- all other persistent paths as NONE.

Use existing bounded authorization or ask once for this exact complete changeset.
The approval authorizes only the listed files/bytes, not product truth, QA/final
readiness, implementation, test evidence, or epic completion. Decline means zero
writes.

Immediately before mutation perform the reference contract's full CAS: re-read the
whole source/target closure, re-enumerate membership/ownership, rebuild
decomposition/IDs/graph/status/inventory/batch/candidates, and revalidate QA.
Every value must equal the preview.

Any change is CAS_CONFLICT with zero new mutations. Do not refresh, merge, retry,
reuse approval, or repair concurrent work.

Publish only previewed paths using same-directory temp files and atomic per-file
create/replace. Verify exact bytes/revisions/schema/identity/revision/status/readiness/
source/AC/Test/dependency/local-extension/history after each write. Publish
`STORIES.md` last, derived only from exact verified story results. Never mutate
EPIC.md or the epics index.

Do not claim cross-file atomicity. On any publication/readback failure, stop
PARTIAL_WRITE with exact verified/uncertain/unattempted revisions. Never delete a
successful write, guess rollback, or report COMPLETE.

---

## Phase 10 — Report and route exactly one next action

Report every field required by the reference, including epic/source/inventory/
batch revisions, story operation/status/readiness, exact AC/Test/dependency IDs,
per-story QA verdicts, append-only events, CAS/readback, and processed/deferred/
blocked counts.

Outcome mapping:

- all current stories safely processed/current with no gaps -> COMPLETE;
- complete exact no-op -> UNCHANGED;
- remaining batch work, story-local blockers/gaps/conflicts, capped QA, or
  publication uncertainty -> PARTIAL;
- epic-wide identity/source/receipt/registry/CAS failure -> BLOCKED;
- decline -> DECLINED;
- invalid invocation/root/catalog -> ERROR.

Select one catalog-derived action in this order:

1. repair epic-wide currentness/identity/receipt/registry;
2. resolve the first deterministic source/TR/ADR/control/slice/QA gap;
3. continue the returned cursor;
4. invoke story-readiness for the first exact AUTHOR_COMPLETE path/revision; or
5. Stop.

Never execute it, print a roadmap, offer implementation for non-final-ready
stories, or claim final READY, epic completion, test execution, sprint selection,
or gate passage.

Always include:

```text
Source Mutations: NONE
QA Plan/Review Record Mutations: NONE
Final Readiness Mutations: NONE
Implementation/Test/Sprint Mutations: NONE
Session-State Mutations: NONE
Auto Executed: false
```

Then stop.
