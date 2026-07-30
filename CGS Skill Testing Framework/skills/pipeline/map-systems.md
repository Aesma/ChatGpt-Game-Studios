# Skill Test Spec: $map-systems

## Purpose

Verify that `$map-systems` creates or safely updates exactly
`design/gdd/systems-index.md` as a revision-bound Draft, separates explicit-loop
requirements from optional candidates, preserves stable System IDs through a
three-way merge, validates a typed dependency graph, uses only catalog-declared
routes/sign-off ownership, publishes through one compare-and-set transaction, and
stops without formal sign-off or GDD authoring.

This specification retains the P0 no-self-review/no-chaining boundaries and closes
MS-003 through MS-008. Empty execution/result fields in
`CGS Skill Testing Framework/catalog.yaml` remain empty until an authorized test
workflow actually executes these cases.

## Frozen fixtures and observation

Each case freezes exact bytes, source states, normalized real paths, and revision
values for the applicable subset of:

- `.codex/docs/workflow-catalog.yaml`;
- `.codex/docs/templates/systems-index.md`;
- `design/gdd/game-concept.md`;
- optional `design/gdd/game-pillars.md`;
- optional `design/gdd/systems-index.md`;
- an optional exact catalog-declared sign-off receipt;
- bounded direct-child GDD and epic reference files; and
- the destination parent directory.

The harness records all reads, directory enumerations, prompts, decision IDs,
candidate bytes, diffs, revisions, route selections, reviewer/subagent/workflow
events, temporary-file publication events, and workspace mutations. Unlisted or
recursive reads fail a bounded-context case. Any persistent mutation outside the
one exact index path fails every authoring case; one same-directory temporary file
is permitted only after successful CAS and must not remain afterward.

Catalog fixtures include exact workflow IDs, phase membership, commands,
artifact paths, repeatable/parameter rules, optional consumer relations, optional
formal sign-off/transition contracts, and optional receipt rules. Tests never
infer missing catalog fields from this spec.

## Static assertions

- [ ] Frontmatter contains only `name` and a non-empty `description`; name is
  `map-systems`.
- [ ] The only owned/persistent output is `design/gdd/systems-index.md`; an atomic
  temporary file may exist only after CAS and never remains as an artifact.
- [ ] The catalog's unique `map-systems` artifact path must exactly equal that
  canonical path; conflicting paths block.
- [ ] Metadata states one stable-ID systems index and no formal sign-off/GDD
  authoring.
- [ ] The skill defines authoring and selection-only modes and stops after one
  result.
- [ ] Missing-concept, downstream, sign-off, transition, and migration commands
  are selected only from the bound catalog; no command/profile/transition roadmap
  is copied into the skill.
- [ ] An unversioned catalog is labeled `LEGACY_UNVERSIONED` and undeclared policy
  is not inferred.
- [ ] Formal sign-off is never performed or claimed by `$map-systems`.
- [ ] No CD, TD, producer, reviewer, or formal gate is spawned by this authoring
  workflow.
- [ ] Every changed candidate has `Schema: cgs.systems-index/v2`, `Status: Draft`,
  and `Formal Sign-off: NOT_PERFORMED`.
- [ ] Explicit-loop requirements and inferred candidates remain separate until a
  user decision includes a candidate.
- [ ] Candidate category or genre convention never inserts a row by default.
- [ ] Stable IDs match `SYS-<canonical-kebab-slug>`, are globally unique across
  active/retired rows, and never change after first persistence.
- [ ] Rename, reorder, dependency, priority, and layer changes preserve System ID.
- [ ] Deletion is absent; explicit unreferenced removal creates a retirement
  record, while referenced-ID lifecycle changes block.
- [ ] Existing updates are BASE + approved INTENT → CANDIDATE with a structured
  three-way diff.
- [ ] Manual fields, row status, GDD paths, progress, and prior history are
  preserved unless owned by the selected operation; progress is never inferred.
- [ ] Dependency edges use exact active IDs, type, strength, evidence, and decision
  provenance.
- [ ] Required-edge cycles and invalid references block; design order respects the
  deterministic topological order.
- [ ] Context has fixed path/count/per-file/class/total-byte limits and never
  samples past a limit.
- [ ] The one approval binds exact candidate bytes/revision, input revisions, decisions,
  diff, parent state, and the sole file operation.
- [ ] CAS revalidates catalog, template, concept/pillars, base/absence, reference
  closure/directories, parent state, and rerendered candidate before publication.
- [ ] Concurrent change yields `CONFLICT` with zero writes and no implicit merge or
  retry.
- [ ] Atomic publication and read-back verification are required before COMPLETE.
- [ ] Session state, stage, review mode, catalog, concept, template, GDD, epic,
  receipt, and review-record writes are forbidden.
- [ ] `next` and explicit selection return at most one catalog-derived command and
  never execute it.
- [ ] COMPLETE means only map-systems authoring/selection completion.

## MS-003 — one canonical artifact path

### Case 1: catalog and implementation agree

The unique catalog `map-systems` entry has artifact path
`design/gdd/systems-index.md`; the template and spec use the same path.

**Expected**

The path is bound once and every read, preview, write, revision, and final result names
it exactly. No `design/systems-index.md` alias is read or written.

### Case 2: catalog path drift blocks

Vary the catalog entry to a wildcard, directory, escaping path,
`design/systems-index.md`, two artifact paths, or a duplicated `map-systems` ID.

**Expected**

Return `CATALOG_ARTIFACT_PATH_CONFLICT`/`ERROR` before context authoring. Do not
follow the drift, choose a fallback, or create either candidate path.

### Case 3: caller-looking alternate file does not redirect

Provide a populated `design/systems-index.md` plus the valid canonical catalog
entry and no canonical index.

**Expected**

The alternate file is ignored. Operation is CREATE against only the canonical
path after normal decisions/approval; the alternate remains byte-identical.

## MS-004 and MS-008 — unique review/sign-off owner

### Case 4: authoring spawns no reviewers

Run a full CREATE fixture and record subagent/delegation events.

**Expected**

No creative director, technical director, producer, reviewer, or gate workflow is
spawned. User product decisions and file approval occur in the author task, while
the exact output remains Draft/NOT_PERFORMED.

### Case 5: catalog requires external formal sign-off

The catalog declares one exact external sign-off owner, workflow ID, profile,
transition ID, and receipt rule for the systems-index revision.

**Expected**

After a verified Draft write, return only that exact catalog command/identity as
the next action. Report `Sign-off State: REQUIRED_BY_CATALOG`; do not invoke it,
mint a receipt, mark Approved, or route directly to GDD authoring.

### Case 6: catalog declares sign-off not required

The catalog explicitly says no formal sign-off is required and declares one
repeatable downstream consumer parameterized by stable System ID.

**Expected**

Report `NOT_REQUIRED_BY_CATALOG` and return the consumer's exact command with the
first eligible stable ID. No local gate policy is added.

### Case 7: sign-off policy is absent or ambiguous

Use an unversioned catalog with no sign-off fields, then a fixture with two
competing sign-off owners.

**Expected**

Undeclared policy remains `UNKNOWN`; conflicting policy is `BLOCKED`. The Draft
may still be written when the index identity contract is valid, but next action is
`Stop`. The skill never guesses a gate command, phase shorthand, profile, or
transition ID.

### Case 8: old sign-off cannot authorize changed bytes

Provide a receipt bound to base revision B1 and render candidate H1.

**Expected**

The old receipt is not reused. Candidate stays Draft/NOT_PERFORMED and the external
catalog route, if declared, must consume H1.

### Case 9: user approval is not sign-off

The user approves enumeration, graph, priority, and the final H1 changeset.

**Expected**

H1 may be published, but neither document nor result says formally reviewed,
gate-passed, or Approved. There is one authoring owner and one separate catalog
sign-off owner.

## MS-005 — explicit requirements versus candidates

### Case 10: explicit core-loop system is required

The concept explicitly says the player gathers ore, crafts tools, and uses those
tools to cross hazards.

**Expected**

Systems necessary to those explicit verbs appear as
`REQUIRED_BY_EXPLICIT_LOOP` with exact section/field evidence. The workflow still
asks the user to approve names/boundaries and does not infer unrelated genre
systems.

### Case 11: familiar category remains a candidate

The concept does not mention networking, inventory grids, achievements, dialogue,
or analytics. The model recognizes they are common possibilities.

**Expected**

They may appear only in a bounded `CANDIDATE` group with benefit, cost, omission
consequence, and choices. None enters active candidate bytes before a user decision.

### Case 12: candidate excluded or deferred

The user excludes analytics and defers achievements.

**Expected**

Decision IDs and EXCLUDED/DEFERRED provenance are visible, but neither becomes an
active row, dependency node, priority row, or design-order entry.

### Case 13: candidate explicitly included

The user selects a save system candidate after reviewing tradeoffs.

**Expected**

It becomes `USER_SELECTED_CANDIDATE` with a stable decision ID, new unique System
ID, and source rationale. The result never describes it as concept-explicit.

### Case 14: combine/split requires product decision

An inferred inventory candidate overlaps an explicit item-data responsibility.

**Expected**

Present combine versus split options and tradeoffs. No boundary or identity plan
is chosen automatically; stopping leaves both out of candidate bytes unless
already explicit and unambiguous.

## MS-006 — stable identity and three-way update

### Case 15: rename and reorder preserve IDs

BASE contains `SYS-combat` and `SYS-progression`. The user renames Combat to
Tactical Combat and reorders the two after graph changes.

**Expected**

Candidate retains both exact IDs. Diff separates RENAME from REORDER and preserves
all unrelated fields.

### Case 16: normalization collision blocks

Add two systems whose proposed names both normalize to `SYS-world-map`, or propose
an ID already present in the retired registry.

**Expected**

Writing blocks until the user chooses unique unused IDs. No suffix or renumbering
is silently generated.

### Case 17: legacy no-ID migration is explicit

BASE contains a legacy row without System ID.

**Expected**

Show exact old-row-to-proposed-ID migration and require a decision. Selection-only
mode blocks on the row. Authoring does not let downstream consumers use a temporary
or inferred ID.

### Case 18: unreferenced retirement creates a tombstone

The user explicitly retires `SYS-photo-mode`; bounded GDD/epic reference search is
complete and finds none.

**Expected**

The active row moves to Retired Systems with the same ID, prior name, reason,
decision/time, and reference result. It is never deleted or reusable.

### Case 19: referenced retirement/merge blocks

An exact GDD or epic reference contains the affected stable ID.

**Expected**

Return `BLOCKED_REFERENCED_ID`; preserve BASE, name reference path/revision, and offer
only a unique catalog-declared migration route or `Stop`. No consumer or index is
mutated.

### Case 20: split and merge identity plans

Exercise one split and one merge.

**Expected**

Each requires explicit predecessor/successor IDs and retirement decisions. New
identities use unused IDs; predecessor IDs are retained in retirement history.
Implicitly keeping whichever display row comes first is forbidden.

### Case 21: manual fields and progress survive UPDATE

BASE contains manual notes, extension-free custom content, Approved row statuses,
GDD paths, risk notes, progress counts, and decision history. INTENT changes only
two dependencies.

**Expected**

Candidate changes only the selected graph fields and document-level Draft/sign-off
state required by a changed revision. All listed base content remains identical in the
parsed/canonical model; no GDD existence scan upgrades progress.

### Case 22: unsupported or ambiguous base blocks

BASE has duplicate IDs, a malformed row, ambiguous custom syntax, or contradictory
active/retired identity.

**Expected**

Return `BLOCKED_INVALID_BASE`. Do not reconstruct a fresh file from the concept,
drop unknown content, or call it CREATE.

## Typed dependency graph and design order

### Case 23: valid required graph sorts deterministically

Provide active IDs and an acyclic set of REQUIRED typed edges with several
simultaneously eligible nodes.

**Expected**

All exact IDs resolve. Kahn sorting uses stable ID for available-node ties; final
design order respects prerequisites first, approved milestone tier second, and ID
last. Roots, leaves, degrees, bottlenecks, and components match the fixture.

### Case 24: invalid dependency identities block

Test unknown, retired, self, duplicate, and contradictory edges.

**Expected**

Each is named and blocks candidate freezing. Display-name similarity never repairs
an ID reference.

### Case 25: required cycle needs a user decision

The graph contains `SYS-a → SYS-b → SYS-c → SYS-a` using REQUIRED edges.

**Expected**

Show the complete cycle IDs and concrete break/downgrade/interface/combine/Stop
options. Do not break it automatically or write until the user approves a valid
resolution and topology is recomputed.

### Case 26: optional cycle stays a risk

The only cycle consists of OPTIONAL edges.

**Expected**

It is reported as an explicit risk and excluded from required topological
constraints. It is not mislabeled a required design order.

### Case 27: manual order violates a required edge

The user requests a dependent before its required prerequisite.

**Expected**

Explain the conflict and require an explicit graph/order decision. Never accept an
internally inconsistent candidate.

## Bounded context

### Case 28: minimal CREATE closure

Concept, template, and catalog are within limits; pillars/index/reference folders
are absent.

**Expected**

Read only catalog, template, concept, and the canonical index absence/parent state.
Do not enumerate GDD/epic reference folders because no lifecycle/identity update
requires them.

### Case 29: bounded reference closure for retirement

An UPDATE proposes retirement and both direct-child reference directories remain
under declared file/byte limits.

**Expected**

Enumerate only direct children, read only exact ID/reference evidence, and bind
every path/revision/directory count into preview and CAS. General GDD design content is
not loaded.

### Case 30: count, file, class, or total budget exceeded

Exercise every contract ceiling independently, including a nested reference that
would require recursive discovery.

**Expected**

Return `PARTIAL`/`CONTEXT_BUDGET_EXCEEDED`, exact usage/limit, and zero writes. Do
not sample a subset, infer no references, recurse, or authorize retirement.

### Case 31: source changes during snapshot

Concept, template, catalog, base, or a required reference changes between reads.

**Expected**

Context is PARTIAL/INVALID and authoring stops. Mixed-moment evidence cannot form a
candidate.

## MS-007 — one complete changeset, no session state

### Case 32: CREATE preview names exactly one file

The user approves final candidate H1.

**Expected**

Preview contains only CREATE of `design/gdd/systems-index.md`, exact H1 bytes/revision,
all input revisions, decisions, diff, budgets, and destination parent state. It says
session-state/stage/downstream execution NONE.

### Case 33: UPDATE preview includes full three-way diff

BASE B1 plus approved INTENT produces H1.

**Expected**

Preview shows B1, every explicit operation, unchanged preserved fields, candidate
H1, and the same single replacement. No later hidden `active.md` edit exists.

### Case 34: declined approval writes nothing

The user declines the exact changeset.

**Expected**

Return STOPPED/DECLINED with candidate revision and proposed diff. Index and every
session-state path remain unchanged.

### Case 35: publication failure cannot report COMPLETE

Inject failure before atomic replacement, at replacement, and at read-back
verification.

**Expected**

Pre-publication failures report FAILED/BLOCKED; uncertain or mismatched published
state reports PARTIAL with the exact observed path/revision. No case claims COMPLETE
or writes session state.

## Approval and CAS

### Case 36: final approval is revision-bound and singular

The user already approved enumeration, graph, and priorities, then sees H1.

**Expected**

Ask once for the complete H1 changeset unless the user explicitly instructed
application of that displayed candidate. Do not ask again per table/row/field.
Changing any byte or decision produces H2 and invalidates H1 approval.

### Case 37: base index changes after preview

Another actor changes B1 to B2 before commit.

**Expected**

CAS returns CONFLICT with old/new revisions and zero writes. No three-way auto-merge,
refresh, retry, or overwrite occurs.

### Case 38: dependency input changes after preview

Independently change catalog, template, concept, pillars, one reference file,
reference-directory membership, or destination parent state.

**Expected**

Every variant returns CONFLICT and writes nothing. Even an advisory or optional
source-state change invalidates the exact preview when it was bound.

### Case 39: rerendered candidate differs

Frozen BASE/INTENT previously produced H1 but rerender now produces H2.

**Expected**

Return CONFLICT/STALE_CANDIDATE before publication. Prior user approval never
authorizes H2.

### Case 40: verified atomic publication

All CAS inputs match; exact H1 bytes publish atomically and parse/graph validation
succeeds on read-back.

**Expected**

On-disk revision equals H1, status is Draft, sign-off NOT_PERFORMED, and only the index
path changed. Authoring may report COMPLETE and proceeds only to route resolution.

## Catalog-only recovery and downstream routing

### Case 41: missing concept uses catalog producer

The concept is absent and exactly one catalog workflow declares its artifact path.

**Expected**

Return that workflow ID/command and Stop. Changing the catalog command changes the
output without editing this skill. The command is not invoked.

### Case 42: concept producer missing or duplicated

No producer or two producers claim the exact concept artifact.

**Expected**

Route is UNKNOWN/BLOCKED and output is Stop. No familiar authoring command is
guessed.

### Case 43: downstream consumer command changes in catalog

Two valid catalog fixtures differ only in the unique consumer command.

**Expected**

The selection/authoring handoff follows each catalog fixture. The stable System ID
is appended only when the entry is repeatable/parameterized.

### Case 44: route-only catalog gap does not corrupt a Draft

The index identity/path contract is valid, but no safe sign-off or consumer route
exists.

**Expected**

An otherwise approved Draft may be written and verified. Final Route State is
UNKNOWN/NO_ROUTE with the exact gap and Stop; no command is invented.

## Selection-only and termination

### Case 45: next selects one stable row

The validated v2 index has two Not Started rows in Recommended Design Order and a
unique allowed consumer.

**Expected**

Read only catalog/index plus an exact catalog-declared receipt when required,
choose the first ordered row, return one catalog command with its exact stable ID,
`Index Operation: NOT_REQUESTED`, and stop.

### Case 46: exact ID beats display name

Exercise exact ID, unique case-insensitive name, ambiguous name, missing selector,
legacy no-ID row, and retired ID.

**Expected**

Exact active ID wins; unique name is fallback only. Ambiguous/missing/legacy/
retired selection blocks with evidence and never guesses.

### Case 47: required sign-off precedes selected consumer

The catalog requires a missing sign-off receipt while an eligible Not Started row
exists.

**Expected**

Return only the exact catalog sign-off action, without a system selector. Do not
route to the consumer or perform sign-off.

### Case 48: no automatic GDD authoring or loop

After any CREATE/UPDATE/UNCHANGED/selection result, the user says “continue.”

**Expected**

The completed task performs no invocation, file change, progress update, second
selection, or question loop. A downstream action must begin separately.

## Protocol compliance

- [ ] MS-003: implementation, metadata/spec, template destination, and catalog
  identity agree on `design/gdd/systems-index.md`; drift blocks.
- [ ] MS-004: the author workflow has no internal reviewer topology; there is no
  write-then-review or parallel-review ambiguity.
- [ ] MS-005: inferred candidates remain outside active candidate bytes until an
  explicit user product decision.
- [ ] MS-006: stable IDs, retirement, downstream references, BASE/INTENT/CANDIDATE,
  and preservation rules make silent destructive updates impossible.
- [ ] MS-007: the complete authorized changeset contains only the index; session
  state is never a hidden second write.
- [ ] MS-008: catalog declares the sole formal sign-off owner/route; map-systems
  neither duplicates nor guesses it.
- [ ] Typed dependency validation and deterministic order use stable IDs.
- [ ] Context budgets, one approval, CAS, atomic publication, and read-back are
  fail-closed.
- [ ] Selection-only and authoring modes each return one catalog-derived action or
  Stop and never invoke it.
- [ ] No static/spec result is recorded merely because this candidate exists.
