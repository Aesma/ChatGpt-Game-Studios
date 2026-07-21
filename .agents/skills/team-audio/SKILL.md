---
name: team-audio
description: "Create and independently review one hash-bound audio specification through bounded read-only specialists, destination routing, and a single writer; never implement code, tests, or assets."
---

## Invocation and execution

Invoke this workflow as `$team-audio [artifact-id]`.

Arguments: `[artifact-id]` identifies one feature or area. This workflow ends at
an approved audio specification. It never implements audio systems, gameplay
wiring, tests, middleware configuration, or assets.

The user decides sonic direction and other product choices. Routine transitions
do not require approval. Before the first mutation, present one complete plan
with every exact normal and recovery path, operation, unique owner, baseline
hash, content scope, and write condition. Obtain one approval bound to a
deterministic plan hash. A new path, owner change, operation change, or material
scope expansion invalidates the approval and requires a new complete plan.

Valid outcomes are:

- `SPEC COMPLETE`;
- `SPEC COMPLETE — ENGINE VALIDATION DEFERRED`;
- `PARTIAL — NOT APPROVED`;
- `ACCEPTED RISK / NOT APPROVED`; or
- `BLOCKED`.

A written document is not proof of approval, implementation, QA, or playback.

---

## Phase 0: Validate and freeze one artifact

Before reading project content or delegating:

1. Require exactly one non-empty artifact ID.
2. Normalize it to a lowercase ASCII slug containing only `a-z`, `0-9`, and
   single hyphens. Reject path separators, `..`, drive prefixes, control
   characters, leading/trailing hyphens, and ambiguous normalization.
3. Resolve exactly:
   - audio specification: `design/audio/audio-[artifact-id].md`;
   - recovery checkpoint:
     `production/session-state/team-audio-[artifact-id].yaml`.
4. If the specification exists, require explicit revise mode. Never overwrite it
   under a create operation. If it is absent, use create mode.
5. Capture raw SHA-256 hashes for both targets, or `ABSENT`.

With no or invalid argument, print usage and examples and stop without reading
project files, spawning agents, writing files, or emitting a verdict.

---

## Phase 1: Build a bounded context manifest

Read the root and nearest applicable `AGENTS.md` files for both targets before
planning writes. Mandatory instruction files do not count against the content
budget.

Load only:

1. the feature/area GDD explicitly matching the artifact;
2. the existing audio specification in revise mode;
3. `design/gdd/sound-bible.md`, if present;
4. the configured engine and pinned version references;
5. explicit first-hop audio, accessibility, technical, ADR, platform, and asset
   index references named by those sources; and
6. summaries or manifests for existing audio assets needed to avoid duplicate
   event/asset IDs.

Do not recursively scan whole design or asset trees and do not send full context
to every agent. Set a limit of 20 files and 250 KiB of raw UTF-8 text. When the
relevant candidates exceed a limit, present the omitted paths and ask the user
which sources to prioritize. Never silently truncate.

For every included source record path, byte length, relevant sections, reason,
and raw `sha256:<64 lowercase hex>`. Detect cycles and stop after one explicit
reference hop. Freeze a canonical context-manifest hash. Each agent receives
only that manifest, the relevant excerpts, and required structured predecessor
results.

A missing sound bible is an explicit input gap, not invented context. It may
permit a feature-local direction, but the report must identify the missing
project-wide constraint and its destination/owner.

---

## Roles, concurrency, and ownership

All proposal producers and reviewers are read-only.

| Role | Responsibility | May write? |
|---|---|---:|
| audio-director author | sonic direction and adaptive behavior proposals | No |
| sound-designer | event, SFX, mix-intent, and asset proposals | No |
| accessibility-specialist | independent accessibility findings | No |
| technical-artist | middleware/bus/streaming/performance proposals | No |
| configured engine specialist | engine validation proposal | No |
| qa-tester | planned validation/playback matrix bound to the current spec hash | No |
| independent audio reviewer | hash-bound audio-spec review | No |
| audio-spec transaction writer | approved spec plus checkpoint | Yes, exact planned paths only |

Choose exactly one transaction writer before authorization. Normally use a fresh
audio-spec writer acting under the audio-director contract. If unavailable, the
current agent may take that responsibility, but the plan must name it.
Ownership cannot change under an existing approval.

Use at most three live subagents. Dispatch independent work as one bounded batch
before waiting. Every job receives an input hash, output schema, and ISO-8601
deadline. Unless the user supplied a smaller bound, the deadline is 10 minutes
after dispatch. Allow at most one narrowed follow-up before the deadline. At the
deadline mark `TIMED OUT`; never wait indefinitely, invent output, or start an
unbounded replacement loop. Missing required output yields PARTIAL or BLOCKED,
never a COMPLETE state.

No gameplay-programmer or implementation writer is part of this workflow.

---

## Phase 2: Collect structured audio proposals

Every agent returns only this schema:

| Field | Requirement |
|---|---|
| proposal_id | stable role-prefixed ID |
| source_role | exactly one role |
| source_refs | paths, sections, and raw hashes |
| destination | exactly one allowed destination |
| audio_spec_constraint | concise player-facing rule or `NONE` |
| required_decision | one explicit product/technical decision or `NONE` |
| owner | destination owner |
| acceptance | testable closure condition |
| dependencies | stable IDs |
| status | `PROPOSED`, `BLOCKED`, or `TIMED OUT` |

Allowed destinations are:

- `AUDIO SPEC`;
- `AUDIO ASSET BRIEF`;
- `TECHNICAL ADR / SPEC`;
- `PERFORMANCE BUDGET`;
- `QA PLAN`;
- `BACKLOG / STORY`; or
- `REVIEW ONLY`.

### 2.1 Sonic direction

Run one read-only audio-director author. It proposes sonic identity, emotional
tone, palette, music/adaptive-state intent, mix priorities, and player-facing
audio rules. Present two or three options only where a genuine product decision
exists; record the selected decision ID.

### 2.2 Sound design and accessibility

After the direction is selected, run sound-designer and
accessibility-specialist in one two-agent batch against the direction hash.

The sound-designer proposes stable audio event IDs, trigger conditions,
priority, spatial behavior, variation intent, mix/ducking behavior, captions,
and asset needs. Detailed asset-production instructions route to AUDIO ASSET
BRIEF.

The accessibility-specialist independently checks:

- critical gameplay information has visual or tactile equivalence;
- captions/subtitles identify source and critical meaning;
- spatial-only cues have a non-audio directional alternative;
- sudden/loud/high-frequency behavior has sensitivity controls; and
- silence, overlapping cues, or mix priority cannot hide critical feedback.

Findings use stable `AXA-[artifact-id]-NNN` IDs with severity, exact evidence,
required outcome, owner, and `OPEN`/`CLOSED` status.

A BLOCKING finding—especially a critical gameplay state communicated only by
audio—is non-waivable. The user may authorize an exact sound/UI/haptic design
revision or stop BLOCKED. There is no skip, acknowledge-and-proceed, or
implementation branch.

A user may accept only a non-blocking risk by recording finding ID, bounded risk,
owner, deadline, `approved_by`, and `approved_at`. That path ends `ACCEPTED RISK
/ NOT APPROVED` and cannot authorize implementation.

One separate read-only author revision and one finding-ID-preserving,
diff-limited verification re-review are allowed. If the same blocker remains on
the second observation, stop BLOCKED. Never recurse.

### 2.3 Technical and engine validation

After the player-facing audio draft is stable, run technical-artist and the one
configured engine specialist in parallel. They return destination-tagged,
read-only proposals.

Middleware choice, engine component/node patterns, bus topology, streaming
strategy, and technical architecture route to TECHNICAL ADR / SPEC. Memory,
voice-count, CPU, streaming, and platform limits route to PERFORMANCE BUDGET.
Implementation files and integration work route to BACKLOG / STORY. None of
these are silently promoted into AUDIO SPEC.

If no engine is configured, do not spawn an engine specialist and do not guess
an engine pattern. Record `ENGINE VALIDATION DEFERRED` with the configuration
source hash and revalidation trigger. The engine-neutral specification may later
be `SPEC COMPLETE — ENGINE VALIDATION DEFERRED`, but it cannot hand off to
implementation until current engine validation is added.

Any proposed technical decision requiring an ADR remains a referenced open
dependency until the ADR is Accepted. This workflow does not write ADRs.

---

## Phase 3: Route and reduce one authoritative audio specification

Create a ledger containing every proposal/finding ID and exactly one
destination. Deduplicate by stable ID and reference; never merge all agent output
verbatim. Cross-domain conflicts go to the shared parent: creative/audio
direction conflicts require a product decision, and technical conflicts require
the technical owner. The reducer never guesses.

The AUDIO SPEC may contain only:

- artifact identity, purpose, scope, and source snapshot references;
- approved sonic direction and emotional/player-feedback goals;
- stable audio-event contracts: trigger, priority, player-facing result,
  spatial behavior, variation intent, and abstract mix/ducking behavior;
- adaptive music states and transition rules without implementation;
- required visual/tactile alternatives, captions, sensitivity controls, and
  resolved accessibility finding IDs;
- references to asset, technical, budget, QA, and backlog proposal IDs;
- dependencies, accepted product decisions, engine-validation state, and open
  blockers; and
- testable design acceptance criteria.

It must exclude middleware selection, engine node/component classes, concrete
bus graphs, memory/CPU/streaming budgets, code or implementation paths, unit
tests, QA/playback results, asset-production instructions, and review
transcripts. Those stay in their destination proposals and are handed to owning
workflows; this run writes none of them.

After genuine product decisions are resolved, form the exact UTF-8 draft and
compute its raw hash. If required proposals timed out or blocked, the optional
written draft must visibly say `PARTIAL — NOT APPROVED` and cannot become an
implementation source.

---

## Phase 4: Authorize and execute one write transaction

Before any mutation, present:

- exact specification and checkpoint paths;
- create/modify operation for each;
- single transaction writer;
- baseline raw hashes or `ABSENT`;
- context-manifest and source hashes;
- destination ledger and exact draft hash;
- engine-validation state and open blocker count;
- success, rollback, partial-write, and checkpoint conditions; and
- canonical deterministic `plan_hash`.

Ask once for approval. Authorization never covers code, tests, ADRs, technical
specs, performance budgets, QA plans, audio assets, import settings, or any
unlisted path. Any new path, owner, operation, or material draft change requires
a complete new plan and approval.

Immediately before writing, rehash every source and target. Any mismatch cancels
the plan before mutation.

The transaction writer writes the exact audio specification bytes, verifies the
raw hash against the approved draft hash, and updates only the exact checkpoint
with:

- artifact ID/path and create/revise mode;
- plan, context-manifest, source, baseline, draft, and current hashes;
- decision, proposal, and finding IDs;
- agent completion/BLOCKED/TIMED OUT states and deadlines;
- engine-validation state and open blockers;
- planned and actual write sets;
- last verified phase and exact safe resume point; and
- state `ACTIVE`, `PARTIAL`, `BLOCKED`, or `COMPLETE`.

If a write fails, claim rollback only after every affected path is restored
byte-for-byte and matches its baseline raw hash. Otherwise preserve the actual
partial state, persist the checkpoint, and return PARTIAL. If checkpoint writing
also fails, print the complete intended payload as `RECOVERY CHECKPOINT NOT
PERSISTED`, list every unverified path/hash, and do not claim safe resumability.

Resume only after current raw hashes match the checkpoint. Reuse agent output
only when its input and output hashes still match. Never repeat a successful
write or delegation based on prose alone.

---

## Phase 5: Independent audio-spec review

After a verified specification write, compute its current raw hash and run a
fresh independent audio reviewer. The reviewer cannot be an author or
transaction writer, is strictly read-only, and binds every finding to that hash.

The review profile checks:

1. sonic-direction coherence and scope;
2. completeness and uniqueness of audio-event contracts;
3. critical-feedback redundancy and accessibility;
4. abstract mix priority, ducking, and cue-conflict behavior;
5. adaptive music states, transitions, interruption, and recovery;
6. destination hygiene and absence of technical/QA/implementation pollution;
7. dependency, engine-validation, and acceptance-criteria clarity.

Findings use stable `AR-[artifact-id]-NNN` IDs with severity, exact evidence,
required outcome, owner, and status. BLOCKING findings cannot be waived. Permit
one fresh read-only author revision and exactly one verification re-review
limited to OPEN IDs and diff regressions. The same blocker remaining on the
second observation ends BLOCKED. Reviewer evidence is stale immediately when
the specification hash changes.

A revision requires a new exact draft, fresh baselines, new plan hash, and user
approval; the same transaction writer applies it. Neither reviewer writes.

---

## Phase 6: Planned QA/playback matrix and final acceptance

After zero BLOCKING accessibility and review findings remain, a read-only
qa-tester may propose a validation matrix bound to the current specification
hash. Route it to QA PLAN; do not write it here.

Each proposed case is `PLANNED` and may cover event triggers, priority/ducking,
adaptive transitions, caption/fallback behavior, silence/overlap, platform
routing, performance budgets, and playback sessions. This workflow has no
implementation or produced audio to execute, so it normally reports
`QA NOT RUN` and `PLAYBACK NOT RUN`.

Never claim a QA case, listening session, playback, mix review, or accessibility
check passed unless it actually ran and records:

- exact spec and build/asset hashes;
- command or playback-session protocol and environment;
- device/platform and relevant audio settings;
- start/end timestamps and duration;
- exit/result and named observer when manual;
- raw log, capture, or signed evidence hash; and
- PASS/FAIL/BLOCKED outcome.

Agent prose, planned cases, filenames, waveforms not listened to, or absent logs
are not execution evidence.

Present the current spec hash, review evidence IDs, engine state, open
dependencies, and planned QA IDs for final user acceptance.

Emit `SPEC COMPLETE` only when:

- every required agent completed within its deadline;
- target raw hash matches the approved draft/revision;
- zero BLOCKING accessibility/review findings remain;
- no accepted-risk record leaves the spec NOT APPROVED;
- all required product dependencies are resolved;
- independent review evidence and planned QA matrix bind to the current hash;
- engine validation is current;
- the user explicitly accepts that same hash/evidence packet; and
- after final compare-and-swap, the same writer records matching hashes,
  evidence IDs, acceptance, and COMPLETE state in the checkpoint.

When all conditions except engine validation pass, emit
`SPEC COMPLETE — ENGINE VALIDATION DEFERRED` and preserve the exact revalidation
trigger. This is not implementation-ready. Declined/deferred acceptance remains
NOT APPROVED.

---

## Output and handoff

Report:

- artifact ID, exact path, raw hash, and context-manifest hash;
- proposal/finding counts by destination;
- agent completion/BLOCKED/TIMED OUT states;
- accessibility and audio-review evidence IDs and bound hash;
- engine-validation and ADR dependency states;
- checkpoint state and safe resume point;
- planned QA/playback separately from executed evidence; and
- exactly one workflow verdict.

This workflow never invokes `$dev-story`. A later implementation may begin only
when the current specification hash is accepted, engine validation is current,
every required technical decision has an Accepted ADR, a story captures the
exact spec hash and testable acceptance criteria, and that story passes its own
readiness gate. Implementation then belongs to a separate user-authorized
`$dev-story [story-path]` run.

For non-COMPLETE outcomes, give only the blocking decision or safe resume action.
Do not recommend code or asset production.

---

## Non-negotiable rules

- Never spawn gameplay-programmer or write/review implementation in this skill.
- Never write code, tests, ADRs, technical specs, budgets, QA plans, import
  settings, or audio assets.
- Never allow more than one transaction writer or expand approved paths.
- Never let proposal agents or reviewers write.
- Never merge all agent outputs into the audio specification.
- Never waive a BLOCKING accessibility or review finding.
- Never fabricate QA, playback, mix-review, hash, or completion evidence.
- Never call a partial/deferred/unreviewed specification implementation-ready.
