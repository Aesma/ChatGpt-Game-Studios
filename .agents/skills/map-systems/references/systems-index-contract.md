# Map Systems — Registry, Graph, Merge, and Transaction Contract

This contract is normative for `$map-systems`. It defines the only owned artifact,
bounded input closure, stable identities, dependency graph, update semantics, and
single-file compare-and-set transaction.

## 1. Artifact and authority boundary

The only owned artifact is:

```text
design/gdd/systems-index.md
```

The bound workflow catalog must contain exactly one `map-systems` entry whose
artifact path resolves to that exact repository-relative file. A missing,
wildcarded, different, duplicated, or escaping path is
`CATALOG_ARTIFACT_PATH_CONFLICT`; do not read or write an alternative index.

`$map-systems` owns only the registry content, dependency graph, milestone
priority, design order, and explicit retirement records. It never owns:

- formal sign-off, phase or gate state;
- GDD authoring, review, approval, or progress recording;
- epic/story reference migration;
- session-state or latest-pointer recording; or
- a catalog, template, concept, pillar, GDD, epic, receipt, or review record.

Every changed index is rendered with document status `Draft` and formal sign-off
state `NOT_PERFORMED`. User approval of product choices or of the file changeset
does not change either value.

## 2. Frozen bounded context

Freeze one repository-root identity and one UTC snapshot. Read exact raw bytes
once, normalize no source in place, and record the declared revision or an explicit
`ABSENT`/`UNREADABLE` marker.

The base closure and hard ceilings are:

| Class | Allowed locations | Count limit | Per-file bytes | Class bytes |
|---|---|---:|---:|---:|
| Catalog | `.codex/docs/workflow-catalog.yaml` | 1 | 512 KiB | 512 KiB |
| Template | `.codex/docs/templates/systems-index.md` | 1 | 512 KiB | 512 KiB |
| Concept | `design/gdd/game-concept.md` | 1 | 512 KiB | 512 KiB |
| Pillars | `design/gdd/game-pillars.md` | 1 | 256 KiB | 256 KiB |
| Base index | `design/gdd/systems-index.md` | 1 | 1 MiB | 1 MiB |
| Sign-off receipt | exactly one catalog-declared path, only when routing requires it | 1 | 256 KiB | 256 KiB |
| Direct GDD references | direct child `design/gdd/*.md`, excluding the three files above | 64 | 64 KiB | 2 MiB |
| Epic references | direct child `production/epics/*.md` | 128 | 64 KiB | 4 MiB |

Total bytes read under this workflow must not exceed 8 MiB. Directory enumeration
must stop at the declared direct-child boundary; never recurse, follow a symlink
outside the root, or choose files by newest/nearest time.

Concept, template, catalog, and existing-index bytes are required for authoring.
Pillars are optional. A sign-off receipt is read only from one exact
catalog-declared path when selection/UNCHANGED routing requires it; never discover
one by name or recency. GDD and epic reference closures are read only for an update
that proposes an ID migration, rename, split, merge, or retirement. Search them
only for exact stable System IDs and catalog-declared reference fields; do not
ingest their general design content.

If any required input is too large, unreadable, changes during the snapshot, or a
needed reference closure exceeds a count/class/total limit, return `PARTIAL` with
`CONTEXT_BUDGET_EXCEEDED` or the exact read reason. Do not sample, infer absence,
approve a destructive update, or write.

## 3. Canonical index schema

The exact candidate is UTF-8 without BOM and LF line endings. It augments the
repository template where necessary and contains:

```text
Schema: cgs.systems-index/v2
Status: Draft
Catalog revision: <bound raw catalog revision>
Concept revision: <bound raw concept revision>
Base Index revision: <revision-or-ABSENT>
Decision IDs: <ordered IDs>
Formal Sign-off: NOT_PERFORMED
```

Required sections are:

1. overview and source identities;
2. systems enumeration;
3. typed dependency registry;
4. validated dependency layers and topological order;
5. milestone priorities and recommended design order;
6. cycles, bottlenecks, risks, and unresolved items;
7. progress fields preserved from the base without inference;
8. retired-system registry; and
9. decision provenance and three-way diff summary.

Every active-system occurrence in enumeration, dependency, layer/order, priority,
risk, and progress data uses one exact stable System ID. Names are display data,
not identity. A filename, table position, status label, or normalized name never
substitutes for an ID.

Valid document statuses are `Draft`, `Under Review`, and `Approved`; this author
always emits `Draft` for changed bytes. Valid active-row statuses are `Not Started`,
`In Design`, `In Review`, `Approved`, and `Implemented`. Valid priorities are
`MVP`, `Vertical Slice`, `Alpha`, and `Full Vision`; valid layers are `Foundation`,
`Core`, `Feature`, `Presentation`, and `Polish`. A custom category is permitted only
as a non-empty user-approved display label. Retired systems live only in the
retired registry and do not use an active-row status.

The authoring workflow may initialize a new row only with status `Not Started` and
GDD path `—`. Existing row status/GDD/epic claims are preserved exactly unless a
separate current recorder already changed the base before this run. `$map-systems`
never infers `In Design`, `In Review`, `Approved`, or `Implemented` from file
presence.

## 4. Stable System IDs and lifecycle

A valid ID matches:

```text
^SYS-[a-z0-9]+(?:-[a-z0-9]+)*$
```

For a new included system, propose `SYS-<canonical-kebab-slug>` exactly once. The
user may choose another valid, unused ID before the candidate is frozen. Require
exact case-sensitive uniqueness across active and retired rows and every proposed
split/merge target.

After first persistence, an ID is immutable:

- rename preserves the ID;
- priority, layer, display order, or dependency changes preserve the ID;
- an ID is never recycled, renumbered, or reassigned;
- normalization collision blocks until the user selects distinct IDs;
- a legacy no-ID row requires an explicit old-row-to-new-ID migration decision;
  it is never silently assigned; and
- split and merge operations require an explicit identity plan. New children or a
  new merged identity receive unused IDs; predecessor IDs move to the retired
  registry rather than disappearing.

Deletion is not an operation. Explicit removal of an unreferenced system moves it
to the retired registry with ID, prior name, reason, decision ID, timestamp, and
downstream-reference result. If any bounded GDD/epic reference exists, retirement,
merge, or identity migration is `BLOCKED_REFERENCED_ID` until a separately owned
reference-migration workflow completes. `$map-systems` never edits those consumers.

## 5. Explicit systems and candidates

Maintain separate in-memory sets:

- `REQUIRED_BY_EXPLICIT_LOOP` — directly named or logically necessary in an
  explicit core-loop/MVP statement, with exact concept field/line evidence;
- `CANDIDATE` — an inferred possibility, with evidence, benefit, cost, and omission
  consequence;
- `USER_SELECTED_CANDIDATE` — a candidate the user explicitly included under a
  stable decision ID; and
- `EXCLUDED` or `DEFERRED` — a candidate the user rejected or postponed.

Only `REQUIRED_BY_EXPLICIT_LOOP` and `USER_SELECTED_CANDIDATE` enter active index
rows. Candidate category, familiar genre convention, fixed checklist, or reviewer
opinion never inserts a row. Present candidate classes in bounded groups and ask
the user to include, exclude, defer, combine, or split each one. Preserve every
decision in the candidate provenance section.

## 6. Typed dependency graph

Each dependency edge contains:

- dependent System ID (`from_id`);
- prerequisite System ID (`to_id`);
- kind `INPUT_OUTPUT`, `STRUCTURAL`, or `PLAYER_UI`;
- strength `REQUIRED` or `OPTIONAL`;
- exact evidence and decision ID; and
- state `ACTIVE`, `REMOVED`, or `DOWNGRADED`.

`from_id` depends on `to_id`. Active edges must reference two distinct active
System IDs. Reject unknown, retired, self, duplicate, or contradictory edges.

Build a deterministic graph from active `REQUIRED` edges. Use Kahn topological
sorting with stable System ID as the tie-break inside the currently available set.
No design-order entry may precede one of its required prerequisites.

An unresolved required cycle blocks freezing and writing. Show the complete cycle
by IDs and ask the user to remove an edge, downgrade a genuinely optional edge,
introduce a user-approved interface/system, combine systems, or stop. Never break
a cycle automatically. Optional cycles remain explicit risks and cannot be
described as required ordering.

Report in/out degree, roots, leaves, fan-in/fan-out bottlenecks, and disconnected
components from the frozen graph. Layers and milestone priorities are proposals
until the user approves them. The final recommended order must satisfy required
topology first, then the approved milestone tier, then stable ID for deterministic
ties.

## 7. Three-way update and structured diff

For an existing valid or explicitly migrated index, construct:

1. `BASE` — exact parsed base bytes/model and revision;
2. `INTENT` — only user-approved operations and decision IDs; and
3. `CANDIDATE` — deterministic application of INTENT to BASE.

Allowed operations are `ADD`, `RENAME`, `RECLASSIFY`, `DEPENDENCY_CHANGE`,
`REPRIORITIZE`, `REORDER`, `RETIRE`, `SPLIT`, `MERGE`, and `LEGACY_ID_MIGRATION`.
Every operation names affected IDs, exact old/new values, reason, decision ID, and
downstream-reference result when applicable.

Preserve all base fields outside the selected operations, including human notes,
unknown extension-free columns/sections, status, GDD paths, progress counts, risk
notes, and prior decision/retirement history. Unsupported or ambiguous base syntax
is `BLOCKED_INVALID_BASE`; do not reconstruct or replace the file from the concept.

Show a lossless three-way diff organized as:

- unchanged preserved fields;
- additions;
- explicit modifications;
- reordered-only rows;
- new retirement records;
- blocked/ambiguous requested changes; and
- downstream references read and their exact revisions.

A requested operation not represented in the diff is not authorized. A candidate
must never silently delete, renumber, normalize, infer progress, or drop manual
content.

## 8. Approval and candidate identity

The user owns all product decisions: system inclusion, combination/split, stable
IDs before first persistence, dependencies, cycle resolution, priority, layer,
order, and retirement intent. Use Question → Options → Decision → Draft → Approval.

After all decisions, assign candidate_revision from the explicit base revision plus one, or 1 for create, and render one exact candidate:

```text
candidate_revision: <explicit candidate revision>
```

Show the complete bytes or a lossless reviewable representation, three-way diff,
input revisions, context-budget use, unresolved risks, and the one-file changeset.
Obtain one approval bound to the candidate revision and decision IDs. An earlier
enumeration/dependency/priority decision is not final filesystem approval. A
bounded explicit instruction to apply the displayed candidate may serve as that
one approval; do not ask again per section or field.

Any content or decision change creates a new candidate revision and invalidates the
old approval. Formal sign-off is outside this approval and outside this workflow.

## 9. Compare-and-set and atomic publication

The preview binds:

- repository root identity;
- catalog, template, concept, and optional pillar raw revisions/source states;
- base index raw revision or `ABSENT`;
- every bounded downstream-reference path/revision/source state read;
- every enumerated directory identity and count used for that closure;
- candidate bytes/revision and ordered decision IDs; and
- destination parent existence/type/real-path state.

Immediately before mutation, re-read the complete bound closure.
Require every value and source state to equal the preview. Re-render the candidate
from the frozen BASE and INTENT and require the same candidate revision.

Any difference is `CONFLICT`: write nothing, preserve both observed states, and do
not merge, refresh, retry, or ask the user to accept changed bytes implicitly.

After CAS succeeds:

1. write the exact candidate bytes to a same-directory temporary file;
2. flush and close as supported;
3. atomically create or replace only `design/gdd/systems-index.md`;
4. re-read exact bytes and verify candidate revision;
5. reparse and validate schema, stable IDs, references, graph, order, decisions,
   and `Status: Draft`/`Formal Sign-off: NOT_PERFORMED`; and
6. verify that no other workflow-owned path changed because of this run.

Report `WRITTEN` only after every verification passes. Pre-publication failure is
`FAILED` with no success claim. A publication/read-back mismatch is `PARTIAL` and
must name the exact observed state; do not repair external state or claim
`COMPLETE`.
