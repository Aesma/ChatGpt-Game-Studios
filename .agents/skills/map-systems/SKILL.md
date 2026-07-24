---
name: map-systems
description: "Author or safely update one stable-ID systems index from explicit product decisions, validate its dependency graph, publish one hash-bound Draft, and stop with catalog-derived routing."
---

# Map Systems

## Invocation

```text
$map-systems [next | <system-id-or-name>]
```

Reject unknown flags, multiple selection arguments, directories, globs, or an
empty selection. There are two exclusive modes:

1. no argument — create or update one systems index; or
2. `next`/one selector — resolve one existing row and return one read-only,
   catalog-derived handoff.

Both modes stop after one result. Never invoke another workflow, start formal
sign-off, author a GDD, update progress, or loop to another system.

Read
[references/systems-index-contract.md](references/systems-index-contract.md) in
full before processing either mode. It is normative.

## Authority, ownership, and result vocabulary

This workflow is the single author of registry/graph content at
`design/gdd/systems-index.md`. The current workflow catalog must independently
name the same exact artifact path. A disagreement blocks all authoring.

The only persistent filesystem mutation is one atomic create/replace of that
index. Publication may use one same-directory temporary file only after CAS; it
must be atomically consumed or removed and is never an owned artifact. Session
state, review mode, stage, catalog, concept, template, GDDs, epics, review records,
gate receipts, and latest pointers are read-only or outside scope.

This workflow is not a reviewer or gate owner. It spawns no CD, TD, producer, or
other reviewer. Every changed candidate is `Status: Draft` with
`Formal Sign-off: NOT_PERFORMED`. A separate catalog-declared owner may later
review or sign the exact hash. User content/changeset approval is not formal
sign-off.

Use only these result fields and values:

| Field | Values |
|---|---|
| `Workflow Status` | `COMPLETE`, `PARTIAL`, `BLOCKED`, `STOPPED`, `ERROR` |
| `Index Operation` | `CREATE`, `UPDATE`, `UNCHANGED`, `NOT_REQUESTED`, `DECLINED`, `CONFLICT`, `FAILED` |
| `Route State` | `READY`, `BLOCKED`, `UNKNOWN`, `NO_ROUTE` |
| `Sign-off State` | `NOT_PERFORMED`, `REQUIRED_BY_CATALOG`, `NOT_REQUIRED_BY_CATALOG`, `UNKNOWN` |
| `Context State` | `COMPLETE`, `PARTIAL`, `INVALID` |

`COMPLETE` means only that this bounded authoring or selection interaction
finished honestly. It never means the index is formally approved, a phase/gate
passed, a system GDD completed, or a downstream workflow ran.

---

## Phase 0: Freeze root and bind the workflow catalog

Resolve exactly one repository root. Reject ambiguous roots, traversal, and
root-escaping real paths. Freeze one UTC snapshot and exact raw SHA-256 values.

Read `.codex/docs/workflow-catalog.yaml` before interpreting a route. Require a
parseable catalog with unique phase and workflow IDs and exactly one workflow
entry whose stable ID is `map-systems`. Require that entry to declare:

- one containing phase;
- exact base command `$map-systems`;
- required/optional semantics; and
- one non-wildcard artifact path equal to
  `design/gdd/systems-index.md`.

An unversioned legacy catalog may supply those fields, but report
`Catalog Contract: LEGACY_UNVERSIONED` and use no field it does not declare. Never
upgrade its advisory comments into formal sign-off or transition policy.

Catalog-only routing means:

- missing-concept recovery comes only from the unique catalog entry whose exact
  artifact contract produces `design/gdd/game-concept.md`;
- selection/authoring handoff comes only from a unique catalog-declared consumer,
  or from the first required workflow in the declared next phase when no stronger
  consumer relation exists;
- a required sign-off/transition comes only from an exact catalog-declared owner,
  workflow, profile, transition ID, and receipt rule; and
- the selected command is copied from that entry, never from this document.

When appending a system selector to a consumer command, require the consumer entry
to be repeatable or explicitly parameterized by stable System ID. Pass only the
validated ID, never an unescaped display name.

If a route is missing, duplicated, ambiguous, incompatible, or lacks a required
sign-off contract, use `Route State: BLOCKED` or `UNKNOWN`, name the catalog gap,
and return `Stop`. Do not hardcode `$brainstorm`, `$design-system`, `$gate-check`,
phase shorthand, a profile, or a transition ID.

Catalog defects affecting the index identity/path block all reads and writes.
Catalog defects affecting only a later route do not invalidate an otherwise
authorized Draft write; they remain visible in the final result.

---

## Phase 1: Selection-only mode

For `next` or one selector, read only the bound catalog, exact systems index, and
one exact catalog-declared sign-off receipt when the route contract requires it,
all under the reference contract's limits. Do not read the concept, template,
GDDs, epics, review mode, stage, or session state.

Require a parseable `cgs.systems-index/v2` index with unique valid active/retired
System IDs, valid status values, valid dependency references, and one deterministic
Recommended Design Order. A legacy no-ID row makes selection `BLOCKED`; do not
invent a temporary ID.

- `next` selects the first active `Not Started` row in Recommended Design Order.
- an explicit selector first requires exact case-sensitive System ID equality;
  only if no ID matches may an exact case-insensitive display-name match be used,
  and it must be unique.

No eligible row, ambiguous name, invalid index, or missing index is `BLOCKED` with
evidence. Never choose by filename, table position outside the canonical order,
mtime, similarity, or inferred GDD state.

Resolve the next route from the catalog:

1. if the catalog declares a required formal sign-off/transition for this index,
   require its exact current hash-bound receipt; when absent, recommend only the
   catalog's sign-off action without a system selector;
2. only when the catalog explicitly declares formal sign-off not required,
   resolve the unique allowed repeatable consumer and append the stable System ID
   as its data argument; or
3. when sign-off policy is undeclared/ambiguous or neither route is safe, return
   `Route State: UNKNOWN`/`BLOCKED` and `Stop`.

Return index path/hash, selected System ID/name/status/order, sign-off state,
catalog path/hash, exact catalog entry/command or gap, `Index Operation:
NOT_REQUESTED`, `Auto Executed: false`, and one handoff or `Stop`. Then stop.

---

## Phase 2: Load one bounded authoring snapshot

For authoring, load only the closure and budgets in the reference contract:

- bound workflow catalog;
- `.codex/docs/templates/systems-index.md`;
- required `design/gdd/game-concept.md`;
- optional `design/gdd/game-pillars.md`; and
- existing `design/gdd/systems-index.md`, when present.

Do not enumerate GDD or epic reference files until a proposed update affects an
existing identity or lifecycle. If that occurs, enumerate only the contract's
direct-child bounded reference closure and read only exact ID/reference evidence.

Missing concept is `BLOCKED`. Resolve a recovery action only from the catalog's
unique exact concept-artifact producer; if none exists, return `Stop`. Never invoke
the action.

Oversize, unreadable, ambiguous, changed-during-read, symlink-escaping, malformed,
or budget-exceeded required context is `PARTIAL`/`INVALID`. Report exact file and
budget use and stop with zero writes. Do not sample or replace an invalid existing
index.

When no index exists, operation is `CREATE`. When one exists, validate its schema,
stable IDs, references, graph, and preserved manual fields, record its base hash,
and ask the user to choose one bounded intent:

- add systems;
- rename/reclassify existing systems;
- revise dependencies;
- reprioritize/reorder;
- explicitly retire, split, merge, or migrate legacy IDs; or
- stop/selection-only handoff.

Do not silently recreate an existing index or combine unselected operations.

---

## Phase 3: Separate explicit requirements from candidates

Extract only systems directly required by explicit core-loop, MVP, mechanic, or
product statements. For each, show:

- proposed stable System ID;
- display name and responsibility;
- `REQUIRED_BY_EXPLICIT_LOOP` classification;
- exact concept section/field evidence; and
- why the explicit loop cannot work without it.

Then present inferred possibilities separately as `CANDIDATE`, each with evidence,
player/product benefit, scope cost, omission consequence, and two or three viable
include/combine/defer/exclude options when a real choice exists.

Do not use a fixed genre/category checklist as the default system set. A familiar
inventory, combat, save, UI, networking, analytics, localization, accessibility,
or progression pattern remains a candidate unless explicit source evidence makes
it required.

Ask the user to decide each bounded candidate group and to identify missing,
combined, split, renamed, excluded, or deferred systems. Assign a stable decision
ID to each accepted choice. Only `REQUIRED_BY_EXPLICIT_LOOP` and explicitly
`USER_SELECTED_CANDIDATE` systems enter the Draft.

Iterate until the user approves the active enumeration and excluded/deferred list.
No file, temporary draft, state, or review record is written.

Apply the stable-ID rules in the reference contract. Existing IDs never change.
Normalization collision, implicit legacy migration, ID reuse, or an unresolved
split/merge identity plan is `BLOCKED` before graph construction.

---

## Phase 4: Build and approve the typed dependency graph

For every active System ID, propose typed edges using the reference contract:

- dependent (`from_id`) and prerequisite (`to_id`);
- kind `INPUT_OUTPUT`, `STRUCTURAL`, or `PLAYER_UI`;
- strength `REQUIRED` or `OPTIONAL`;
- evidence and decision ID.

Validate exact active IDs, reject self/unknown/retired/duplicate/contradictory
edges, and compute the deterministic required-edge topology. Show roots, leaves,
bottlenecks, disconnected components, and every cycle.

An unresolved required cycle is `BLOCKED`. Present concrete tradeoffs and let the
user choose an edge removal/downgrade, interface/system addition, combination, or
Stop. Never silently break a cycle or disguise it with display order.

Ask the user to approve the complete edge set and cycle resolutions. Graph changes
made after approval require a new decision and recomputation.

---

## Phase 5: Approve priorities and deterministic design order

Propose MVP, Vertical Slice, Alpha, or Full Vision priority for each active ID from
the explicit concept scope and approved graph. Explain technical prerequisite and
player-experience tradeoffs. Categories/layers and priorities are proposals, not
defaults.

Ask the user to approve or revise them. Compute Recommended Design Order so every
required prerequisite precedes its dependent; within currently eligible systems,
order by approved milestone tier and then stable ID. A manual order that violates a
required edge is invalid until the edge or order receives an explicit decision.

No inferred candidate, retired ID, or unresolved graph node may enter the active
order.

---

## Phase 6: Apply a three-way update and render one Draft

For CREATE, build a new canonical model. For UPDATE, apply exactly:

```text
BASE + user-approved INTENT operations -> CANDIDATE
```

Follow the reference contract's operation, preservation, identity, retirement,
and bounded downstream-reference rules. A rename/reorder preserves ID. No delete
operation exists. A referenced retirement/migration/split/merge is
`BLOCKED_REFERENCED_ID` and must be handed to a separate catalog-declared migration
workflow when one exists; otherwise `Stop`.

Preserve status, GDD path, progress, manual notes, unknown supported content, and
history outside selected fields. Never infer progress from file presence.

Populate the repository template in memory and augment it to exact
`cgs.systems-index/v2`. Every changed document is:

```text
Status: Draft
Formal Sign-off: NOT_PERFORMED
```

Render exact UTF-8/LF bytes and compute `candidate_sha256`. Show:

- input paths/hashes and context-budget use;
- complete candidate bytes or a lossless reviewable representation;
- stable-ID registry, active/retired changes, and provenance;
- typed graph, cycles/bottlenecks, priority, and order;
- the structured BASE/INTENT/CANDIDATE diff;
- preserved manual/status/GDD/progress fields;
- unresolved risks/catalog gaps; and
- the sole possible filesystem change.

Any user change after rendering produces a new decision, rerender, diff, and hash.
This workflow does not spawn reviewers. Formal review/sign-off belongs only to the
catalog-declared external owner and is never claimed here.

If canonical candidate bytes equal the valid base bytes, use `Index Operation:
UNCHANGED`; do not rewrite or mint a no-op decision merely to claim completion.

---

## Phase 7: Obtain one hash-bound changeset approval

Preview exactly one operation:

```text
design/gdd/systems-index.md: CREATE | REPLACE with candidate_sha256
all other writes: NONE
```

Bind the preview to candidate hash, base hash/absence, catalog/template/concept/
pillar hashes, bounded reference closure, decision IDs, destination parent state,
and complete diff. Explicitly state:

```text
Formal Sign-off: NOT_PERFORMED
Stage Mutation: NONE
Session-State Mutation: NONE
Downstream Workflow Execution: NONE
```

Obtain one approval for the exact displayed changeset. If declined, return
`STOPPED`, `Index Operation: DECLINED`, and zero writes. Do not ask again per row,
section, or field. Approval never extends to a changed candidate hash or another
path.

---

## Phase 8: Compare-and-set, publish once, and verify

Immediately before mutation, execute the complete compare-and-set contract in the
reference. Re-hash root-bound catalog, template, concept, pillars, base/absence,
bounded reference closure/directory states, destination parent, and rerendered
candidate.

Any difference returns `BLOCKED`, `Index Operation: CONFLICT`, exact old/new
hashes or states, and zero writes. Do not merge, refresh, retry, overwrite, or
request implicit acceptance of new bytes.

After CAS succeeds, atomically publish only the exact candidate bytes, re-read
them, verify the hash and complete v2 registry/graph/order/provenance invariants,
and confirm no other path was changed by this workflow.

- verified exact write -> `Index Operation: CREATE` or `UPDATE` and authoring may
  be `COMPLETE`;
- pre-publication failure -> `Index Operation: FAILED`, `BLOCKED`, no success;
- publication/read-back mismatch or uncertain resulting state -> `PARTIAL`, exact
  observed state, never `COMPLETE`.

Never repair or revert external concurrent changes.

---

## Phase 9: Return one catalog-derived next action and stop

After a verified write or `UNCHANGED`, re-read the catalog hash and resolve:

1. a required formal sign-off/transition owner and exact action, when declared;
2. only when the catalog explicitly declares formal sign-off not required, the
   unique catalog-declared downstream consumer for one first eligible active
   system; or
3. `Route State: UNKNOWN`/`NO_ROUTE` and `Stop` when sign-off policy or a safe
   route is undeclared.

Do not infer sign-off from user approval, status text, agent opinion, prior hash,
or file presence. Do not invent a gate profile/transition ID or reuse an old
sign-off after the candidate hash changes.

Return:

- workflow/index operation and context states;
- catalog path/contract/version/hash;
- index path/base hash/candidate hash/on-disk hash;
- counts of required, user-selected candidate, excluded/deferred, active, and
  retired systems;
- decision IDs and structured diff summary;
- graph node/required-edge/optional-edge/root/leaf/cycle/bottleneck counts;
- formal sign-off state/owner/receipt requirement or catalog gap;
- route state, exact catalog workflow ID/command or `Stop`;
- `Stage Mutation: NONE`, `Session-State Mutation: NONE`,
  `Auto Executed: false`; and
- exactly one next action.

Then stop. Never invoke the command, ask to continue, update a system row after a
GDD/review, or process another system.

## Status mapping

- invalid invocation/root/catalog index identity -> `ERROR`;
- missing concept, invalid base, identity/graph/reference/catalog safety blocker,
  declined required product decision, or CAS conflict -> `BLOCKED`/`STOPPED` as
  applicable;
- budget/read uncertainty or post-publication uncertainty -> `PARTIAL`;
- verified Draft write, honest UNCHANGED, or read-only one-row selection ->
  `COMPLETE` for this workflow only.
