---
name: team-level
description: "Orchestrate a bounded read-only level-design team into one destination-routed, hash-bound level specification with a single writer, non-waivable accessibility blockers, and independent level review before implementation."
---

## Invocation and execution

Invoke this workflow as `$team-level [level-id]`.

Arguments: `[level-id]`. The level ID identifies one level or area. This
workflow designs or revises exactly one level; it never implements the level.

The user makes product decisions. Routine phase transitions do not require
approval. Before the first mutation, present one complete write plan containing
every exact normal and recovery path, operation, unique owner, baseline hash,
content scope, and write condition. Obtain one approval bound to its plan hash.
A new path, owner change, changed operation, or material content expansion
invalidates that authorization and requires a new complete plan.

This workflow may return:

- `COMPLETE — DESIGN APPROVED`;
- `PARTIAL — NOT APPROVED`;
- `ACCEPTED RISK / NOT APPROVED`; or
- `BLOCKED — PRODUCT DECISION REQUIRED`.

No other success label is allowed. A produced file is not proof of approval.

---

## Phase 0: Validate and freeze one target

Before reading project content or delegating:

1. Require exactly one non-empty level ID.
2. Normalize it to a lowercase ASCII slug containing only `a-z`, `0-9`, and
   single hyphens. Reject path separators, `..`, drive prefixes, control
   characters, leading/trailing hyphens, and ambiguous normalization.
3. Resolve exactly:
   - level source: `design/levels/[level-id].md`;
   - recovery checkpoint:
     `production/session-state/team-level-[level-id].yaml`.
4. If the level source exists, ask whether this is a revision. Do not overwrite
   it under a create operation. If it is absent, use create mode.
5. Capture raw SHA-256 hashes for both existing targets, or `ABSENT`.

With no or invalid argument, print usage and examples, then stop without reading
GDDs, spawning agents, writing files, or emitting a verdict.

---

## Phase 1: Build a bounded context manifest

Read the root and nearest applicable `AGENTS.md` files for both exact target
paths before planning any write. These mandatory instructions do not count
against the content budget. They never convert a level document into a system
GDD; the `design/gdd/` eight-section and `$design-review` rules apply
only to GDDs.

Read only sources needed for this level:

1. `design/gdd/game-concept.md` and `design/gdd/game-pillars.md`;
2. the existing target level document in revision mode;
3. explicit level, narrative, world, art-bible, accessibility, system-GDD, and
   adjacency references named by those sources or by the target brief; and
4. one dependency hop for each referenced adjacent level.

Do not recursively read whole design directories. Set a manifest budget before
delegation: at most 20 files and 250 KiB of raw UTF-8 text. If the relevant set
exceeds either limit, present the omitted candidates and ask the user which
sources to prioritize. Do not silently truncate.

For every included source record exact path, raw `sha256:<64 lowercase hex>`,
byte length, relevant sections, and why it is in scope. Detect duplicate and
cyclic adjacency IDs. A cycle is reported as a dependency fact and is never
followed recursively.

Classify each adjacent interface by stable level ID as `AUTHORED`, `PLANNED`,
`UNRESOLVED`, `BROKEN LINK`, or `INTERFACE CONFLICT`. File existence alone does
not establish a valid interface. Never invent an adjacent level or automatically
start another `$team-level` run.

Freeze the context manifest hash. Every agent prompt receives only the manifest,
the relevant excerpts, and prior structured proposals required for its task—not
all source files verbatim.

---

## Roles, concurrency, and ownership

All expert work is read-only until the approved write transaction.

| Role | Responsibility | May write? |
|---|---|---:|
| narrative-director | narrative-purpose proposal | No |
| world-builder | world constraints and environmental-story proposal | No |
| art-director | visual/wayfinding constraints and art-brief proposal | No |
| level-designer author | layout, pacing, adjacency, and level-source draft | No |
| systems-designer | encounter/system interface proposal | No |
| accessibility-specialist | independent accessibility findings | No |
| qa-tester | proposed tests and playtest coverage after a current level hash exists | No |
| independent level reviewer | `level-review` evidence | No |
| transaction writer | approved level source plus its checkpoint | Yes, exact planned paths only |

Choose one transaction writer before authorization. It owns both exact target
paths and is the only writer in the run. Normally it is a fresh
`level-designer` writer; if that role is unavailable, the current agent may take
the same responsibility, but the write plan must say so. Ownership cannot change
under an existing approval.

Use at most three live subagents. Start independent jobs in one bounded batch,
then wait for the batch before a dependent phase. Give every job an explicit
input hash, output schema, and ISO-8601 deadline. Unless the user supplied a
smaller bound, the deadline is 10 minutes after dispatch. One narrowed follow-up
is permitted only before its deadline. At the deadline mark the job `TIMED OUT`; do not wait
indefinitely, forge a result, or spawn repeated replacements. Missing required
input yields `PARTIAL — NOT APPROVED` or `BLOCKED`, never COMPLETE.

---

## Phase 2: Collect structured read-only proposals

### 2.1 Narrative, world, and visual direction

Run narrative-director, world-builder, and art-director independently, with the
three-job concurrency cap. Each returns proposals using this schema:

| Field | Requirement |
|---|---|
| proposal_id | stable `NP-*`, `WP-*`, or `AP-*` ID |
| source_role | one role |
| destination | exactly one allowed destination |
| source_refs | paths, sections, and raw hashes |
| level_facing_constraint | concise constraint, or `NONE` |
| assumptions | explicit unresolved assumptions |
| dependencies | stable IDs only |
| status | `PROPOSED`, `BLOCKED`, or `TIMED OUT` |

Allowed destinations are:

- `LEVEL SOURCE`;
- `NARRATIVE / LORE`;
- `ART BRIEF`;
- `SYSTEM GDD`;
- `QA PLAN`;
- `BACKLOG`; or
- `REVIEW ONLY`.

Narrative prose/dialogue routes to NARRATIVE / LORE. Asset-production detail
routes to ART BRIEF. Only spatially authoritative constraints—purpose, landmark
function, sight-line requirement, environmental rule affecting traversal—may
route to LEVEL SOURCE.

### 2.2 Layout and adjacency contract

After Phase 2.1 completes, run one read-only level-designer author task. It
consumes only LEVEL SOURCE proposals and references to other destinations. It
must return:

- stable level identity and purpose;
- critical and optional paths;
- pacing beats and rest points;
- encounter locations expressed as contracts, not system formulas;
- navigation, landmarks, entry/exit points, and softlock prevention;
- stable adjacency interface IDs and state;
- level-facing accessibility requirements;
- open product decisions and dependencies; and
- an in-memory level-source draft.

It must not copy proposal transcripts or external-destination content into the
draft.

### 2.3 Systems integration and production concepts

Run systems-designer and the location-specific art-director in a bounded
two-agent batch using the layout draft hash. They return the same proposal
schema. Enemy formulas, loot tables, balance values, and reusable mechanics go
to SYSTEM GDD. Asset lists, production concepts, palettes, and VFX inventories
go to ART BRIEF. The LEVEL SOURCE may retain only interface IDs, placement
constraints, landmark purpose, and testable encounter/navigation contracts.

If either proposal contradicts the frozen visual direction or a system GDD,
surface the exact conflicting IDs and sources as a product decision. Do not let
the reducer choose across domains.

---

## Phase 3: Accessibility review and convergence

Run a fresh accessibility-specialist against the layout draft hash and committed
project accessibility requirements. The reviewer is strictly read-only.

The first review creates stable findings:

| Field | Requirement |
|---|---|
| finding_id | stable `AX-[level-id]-NNN` |
| severity | `BLOCKING`, `RECOMMENDED`, or `NICE TO HAVE` |
| evidence | exact draft section plus requirement source/hash |
| affected_path | critical/optional path or encounter ID |
| required_outcome | testable closure condition |
| owner | domain owner |
| status | `OPEN` or `CLOSED` |

A BLOCKING finding is non-waivable. The only choices are:

1. authorize a bounded author revision that satisfies the stated outcome; or
2. stop with `BLOCKED — PRODUCT DECISION REQUIRED`.

There is no acknowledge-and-proceed option. Step 5, QA planning, design approval,
and implementation handoff are forbidden while a BLOCKING finding is open.

A user may accept only a non-blocking risk. Record its stable finding ID,
specific bounded risk, owner, deadline, `approved_by`, and `approved_at`. The
workflow then ends `ACCEPTED RISK / NOT APPROVED`; it cannot emit COMPLETE or
authorize implementation.

If a BLOCKING finding is revised, start a separate read-only author task with an
exact diff scope. Permit exactly one verification re-review. The re-review checks
only the original OPEN finding IDs and regressions caused by that diff. It keeps
the original IDs; diff-only regressions receive IDs linked to the triggering
finding. If the same blocker is still open on the second observation, stop
`BLOCKED — PRODUCT DECISION REQUIRED`. Never enter a recursive
review → rewrite → review loop.

---

## Phase 4: Route destinations and decide the level source

Create a routing ledger containing every proposal/finding ID and exactly one
destination. Resolve duplicates by reference; never merge source text verbatim.

The level-source reducer may include only:

- level identity, purpose, boundaries, and source snapshot references;
- spatial layout, critical/optional paths, pacing, navigation, landmarks, and
  softlock constraints;
- encounter and mechanic interfaces by stable ID, without formulas or loot
  tables;
- adjacency interfaces and their states;
- level-facing art/wayfinding constraints;
- accessibility requirements and resolved finding IDs; and
- open level dependencies and user decisions.

It must exclude lore prose, dialogue, art-production briefs, asset inventories,
system formulas/tuning tables, QA cases, backlog items, review transcripts, and
raw agent output. Those remain structured proposals in the report and are handed
to their owning workflow later. This run writes none of those destinations.

Ask the user only about unresolved product choices or cross-domain conflicts.
After those decisions, compute the exact UTF-8 draft hash and preserve each
decision ID in the draft.

---

## Phase 5: Authorize and execute one bounded write transaction

Before any mutation, present:

- exact level and checkpoint paths;
- create/modify operation for each;
- the single transaction writer;
- baseline raw hashes or `ABSENT`;
- frozen context-manifest hash and source hashes;
- exact destination ledger;
- exact draft hash;
- resolved accessibility findings and open blocker count;
- success, partial-write, rollback, and checkpoint conditions; and
- a deterministic canonical `plan_hash`.

Ask once for approval of that complete plan. Authorization never covers
NARRATIVE / LORE, ART BRIEF, SYSTEM GDD, QA PLAN, BACKLOG, implementation,
tests, assets, or any unlisted path. Material draft change, new path, new owner,
or changed operation requires a new full plan and approval.

Immediately before writing, rehash every source and target. Any mismatch cancels
the plan before mutation.

The transaction writer writes the level source and verifies its raw hash against
the approved draft hash. It updates only the exact checkpoint path with:

- level ID/path and create/revise mode;
- plan hash, context-manifest hash, source hashes, and baseline/current hashes;
- decision and proposal/finding IDs;
- agent completion/BLOCKED/TIMED OUT states and deadlines;
- review round and current open blockers;
- planned and actual write sets;
- last verified phase and exact safe resume point; and
- state `ACTIVE`, `PARTIAL`, `BLOCKED`, or `COMPLETE`.

If a write fails, describe rollback only after every changed path is restored
byte-for-byte and its baseline hash verifies. Otherwise preserve the actual
partial state, write the failure checkpoint, and return `PARTIAL — NOT
APPROVED`. If the checkpoint write itself fails, print the complete intended
checkpoint payload as `RECOVERY CHECKPOINT NOT PERSISTED`, name every
unverified path/hash, and stop; do not claim the run is safely resumable. Never
hide a partial write or claim approval.

Resume only when current raw hashes match the checkpoint's claimed hashes.
Reuse a completed agent result only when its input and output hashes still
match; otherwise rerun it. Never duplicate a completed write or delegation on
the strength of prose alone.

---

## Phase 6: Independent level-review profile

After a verified level-source write, compute its current raw hash and run one
fresh independent reviewer. The reviewer must not be the author/transaction
writer, must be strictly read-only, and must bind all evidence to that exact
hash.

The `level-review` profile checks only:

1. critical-path continuity and completion;
2. sequence breaks, softlocks, and recovery routes;
3. pacing and rest/pressure transitions;
4. adjacency IDs, directionality, and interface compatibility;
5. navigation and wayfinding without color-only cues;
6. accessibility requirements and resolved finding IDs; and
7. encounter contracts, dependencies, and acceptance boundaries.

It does not apply system-GDD section rules, call `$design-review`, write the
level source, or generate implementation. Findings use stable `LR-[level-id]-NNN`
IDs with severity, exact evidence, required outcome, owner, and status.

If review returns BLOCKING findings, permit at most one separately authorized
author revision. A fresh read-only author task receives only OPEN finding IDs
and the approved diff scope and returns a revised draft plus exact diff. Rebuild
the complete plan with fresh baselines and a new plan hash; only after approval
may the same transaction writer apply it. The reviewer never writes. Then run
exactly one verification re-review limited to those IDs and diff regressions. Any original blocker still open after that
second observation ends `BLOCKED — PRODUCT DECISION REQUIRED`. A timeout,
missing evidence, reviewer/author identity collision, or evidence hash that does
not equal the current raw level hash prevents approval.

No level-review evidence is reused after the level file hash changes.

---

## Phase 7: QA proposal and approval gate

Only after the current level hash has zero open BLOCKING accessibility and
level-review findings may a read-only qa-tester propose QA coverage. It receives
the current level hash and returns planned critical-path, sequence-break,
softlock, boundary, navigation, accessibility, and playtest cases with stable
IDs and source sections.

These are `PLANNED` tests, not executed evidence. Do not write a QA plan in this
workflow. Do not claim PASS, coverage, playtest completion, or test evidence
unless an external runner actually executed the named command/session and
returned timestamp, exit/result, and raw log/evidence hash. Missing or timed-out
QA proposals prevent COMPLETE and yield PARTIAL.

Present a hash-bound final design-acceptance packet after the QA proposal. It
contains the current level hash, review evidence IDs, resolved findings,
adjacency/dependency state, and planned QA case IDs. Ask for final design
acceptance as a product decision. Declining or deferring acceptance leaves the
design NOT APPROVED and does not authorize implementation.

Emit `COMPLETE — DESIGN APPROVED` only when:

- the target raw hash matches the approved draft/revision;
- every required agent completed within its deadline;
- all adjacency and required dependencies are resolved;
- zero accessibility and level-review BLOCKING findings remain;
- no accepted-risk record leaves the design NOT APPROVED;
- independent level-review evidence is bound to the current level hash;
- the QA proposal is bound to the same hash;
- the user explicitly accepted that same hash and evidence packet; and
- after one last compare-and-swap check, the same transaction writer records the
  same plan, file hash, evidence IDs, acceptance decision, and COMPLETE state in
  the pre-authorized checkpoint.

Final design acceptance is not permission to implement.

---

## Output and handoff

Report:

- level ID, exact path, raw hash, and context-manifest hash;
- proposal/finding destination counts;
- agent completion, BLOCKED, and TIMED OUT states;
- accessibility and level-review evidence IDs with bound hash;
- adjacency/dependency state;
- checkpoint path/state and safe resume point;
- planned QA cases separately from any executed evidence; and
- exactly one workflow verdict.

A COMPLETE result may hand off to the owning workflows for NARRATIVE / LORE,
ART BRIEF, SYSTEM GDD, BACKLOG, and `$qa-plan`. Implementation remains forbidden
until the current level hash is DESIGN APPROVED, implementation stories are
created from that exact hash, and those stories pass their own readiness gate.
Only then may a separate `$dev-story [story-path]` run begin.

For every non-COMPLETE result, give only the blocking decision or exact safe
resume action. Never recommend implementation.

---

## Non-negotiable rules

- Never call `$design-review` for a level document.
- Never waive a BLOCKING accessibility or level-review finding.
- Never let an author or writer sign its own review.
- Never run an unbounded review/revision loop.
- Never pass all agent output verbatim to the reducer.
- Never write an external destination inside this workflow.
- Never allow more than one transaction writer or expand its approved paths.
- Never implement gameplay, code, assets, or tests in this workflow.
- Never fabricate agent results, test execution, hashes, or review evidence.
- Never call a partial artifact COMPLETE or DESIGN APPROVED.
