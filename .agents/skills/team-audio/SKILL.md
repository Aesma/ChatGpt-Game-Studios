---
name: team-audio
description: "Create and independently review one bounded, revision-bound audio specification through read-only specialists, destination routing, non-waivable accessibility gates, and one writer; never implement code, tests, ADRs, or assets."
---

## Path-first integrity

Accept canonical project-relative paths directly; do not require a caller-supplied
content-derived token. Validate project-root containment, regular-file type, declared
schema/version, stable IDs, permissions, lifecycle state, and path or ID collisions.
Allocate collision-safe IDs independently of file bytes. Before any permitted write,
re-read referenced records and target state, preview the exact authorized changes,
then use same-directory staging plus atomic replacement and rollback on failure.


# Team Audio

Create or revise one authoritative player-facing audio specification. This skill
ends at a reviewed and explicitly accepted spec revision. It never implements audio
systems, gameplay wiring, tests, middleware configuration, import settings, or
audio assets, and never claims implementation QA or playback occurred.

## Invocation and request contract

Invoke only as:

    $team-audio --manifest <request-path> [--resume <checkpoint-path>]

No manifest prints that usage and stops before repository discovery, project-file
reads, delegation, decisions, approval, authorization, checkpoint writes, or
verdicts.

The manifest declares `contract: cgs.team-audio-request/v2` and:

- stable lowercase `artifact_id`, unique `run_id`, and `operation: create | revise`;
- exact feature/area GDD, optional sound bible, engine/version, accessibility,
  platform, technical/ADR, audio-asset index/summary, and existing spec evidence
  canonical paths with declared schema and stable IDs, or `ABSENT`;
- canonical spec path `design/audio/audio-<artifact-id>.md` and operational path
  `production/session-state/team-audio/<artifact-id>/<run-id>.yaml`, with expected
  prior states/ABSENT;
- named product authority, audio-spec plan approver, mutation authority, one
  transaction writer, and independent reviewer identities;
- checkpoint-record authorization ID/revision or instruction to collect one exact
  bounded record authorization before its first write;
- limits no larger than this contract, exact attempt/phase deadlines, and one
  retry policy; and
- explicit non-writes covering code, tests, ADRs, technical specs, performance
  budgets, QA plans, assets, imports, and every other project path.

Normalize artifact ID to ASCII `a-z`, `0-9`, and single hyphens. Reject separators,
`..`, drive prefixes, controls, leading/trailing/repeated hyphens, ambiguous
normalization, unknown/duplicate fields, unsafe/aliased paths, symlink/junction
escape, raised limits, invalid revisions/roles, target/source aliasing, missing revise
target, occupied create target, or any second audio-spec path. Never create or use
`design/gdd/audio-<artifact-id>.md`.

## Explicit state model

Valid workflow verdicts are exactly:

- `SPEC COMPLETE`;
- `SPEC COMPLETE — ENGINE VALIDATION DEFERRED`;
- `PARTIAL — NOT APPROVED`;
- `ACCEPTED RISK — NOT APPROVED`;
- `DEFERRED — NOT APPROVED`; or
- `BLOCKED`.

`SPEC COMPLETE` means the design specification only. It never means implemented,
asset-complete, QA-passed, playback-approved, or implementation-ready.

This workflow has no review-mode state. It never reads a session `review_mode`,
`full`, `lean`, or `solo` flag. The fixed role/phase contract below is deterministic;
required evidence cannot disappear because of a mode label.

## Paths, ownership, and side-effect boundary

The only writable paths are the canonical audio spec and the one canonical
checkpoint path. Exactly one `audio-spec transaction writer` owns both. Its
identity is frozen before authorization and cannot change under an approved plan.

All specialist, author, accessibility, technical, engine, QA-planning, and review
agents are read-only proposal producers. They receive prohibited paths and attempt
tokens, cannot delegate again, and cannot write project or operational files.

Never spawn gameplay-programmer or any implementation writer. Never invoke
`$dev-story` or another workflow. Suggestions for code, tests, integration,
middleware, assets, budgets, ADRs, or QA route to owner handoffs only.

## Phase 0: Validate request and authorize checkpoint recording

Validate the manifest before other reads. Resolve the two canonical targets and
their exact prior states. In create mode the spec must be ABSENT; in revise mode its
Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
the declared existing run ID/revision for resume.

The checkpoint is one bounded operational file for this exact run, updated
atomically after each safe phase. A later run uses its own run-ID path and cannot
overwrite or reuse this run's history. Before its first mutation, require
`cgs.team-audio-record-authorization/v2` binding artifact/run IDs, exact checkpoint
path/prior state, maximum 131072 bytes, schema, allowed transition fields/phases, one
recorder/writer, and explicit non-writes. If absent, present that exact record plan
once and obtain authorization. This record authority never covers the spec.

Checkpoint transitions, attempts, cancellation, recovery, and atomic conflict check are normative in
`references/execution-and-recovery.md`.

## Phase 1: Build a bounded context manifest

Read applicable AGENTS instructions, then enumerate only:

1. the exact feature/area GDD;
2. the existing canonical spec in revise mode;
3. the declared sound bible when present;
4. configured engine/pinned version evidence;
5. explicit first-hop audio, accessibility, platform, technical, ADR, and asset-
   index references named by those sources; and
6. bounded audio-asset summaries needed to avoid duplicate event/asset IDs.

Content hard limits are 20 files, 256000 exact UTF-8 bytes, one explicit reference
hop, eight source groups, 128 asset-summary rows, 128 audio-event IDs, and 64
dependency IDs. Mandatory applicable AGENTS files are recorded separately and do
not consume the content budget. The request may lower, never raise, a limit.

Inventory size/count before full-read; never truncate. Detect cycles and duplicate/
ambiguous IDs. Exceeding any limit yields `PARTIAL — NOT APPROVED`, exact loaded/
omitted identities, and one deterministic request-split action. A user may choose a
smaller new scope, but the truncated run cannot claim complete context or SPEC
COMPLETE.

Create canonical `cgs.team-audio-context-manifest/v2` with ordered source group,
Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
reference ID, reason, dependency edges, owner, loaded/omitted state, and failure. Compute
its reference ID. Each agent receives only required excerpts and structured predecessor
results, never the full context set by default.

A missing sound bible is an explicit feature-local constraint gap with destination,
owner, and acceptance condition; never invent project-wide direction.

## Fixed roles, concurrency, and attempt limits

The role set is fixed:

| Role | Responsibility | Required state | Write scope |
|---|---|---|---|
| audio-director author | direction/adaptive-rule proposal | required | none |
| sound-designer | event/SFX/mix/asset proposal | required | none |
| accessibility-specialist | independent accessibility findings | required | none |
| technical-artist | engine-neutral technical routing | required | none |
| configured engine specialist | configured-engine validation | required only when engine configured | none |
| qa-tester | planned QA/playback matrix | required after reviewed spec | none |
| independent audio reviewer | current-revision spec review | required | none |
| audio-spec transaction writer | checkpoint and exact authorized spec | required | two canonical paths only |

Use at most three live agents. Every attempt uses
`cgs.team-audio-agent-attempt/v2`, exact input/output revisions, unique token, allowed
proposal/finding IDs, prohibited paths, start/deadline, and retry ordinal. Maximum
per-attempt deadline is 10 minutes, maximum multi-agent phase deadline 20 minutes,
and maximum total delegate attempts per run 9. The request may lower these limits.

On failure/timeout/cancel/invalid output/side effect, revoke the token, cancel
dependents, quarantine late results, and compare prohibited/target prior states. One
narrowed retry is allowed only after proving the failed attempt wrote nothing; it
uses a new token and the same or smaller input scope. A second failure is PARTIAL or
BLOCKED. Never wait indefinitely or substitute the coordinator's invented output.

## Phase 2: Propose and decide sonic direction

The read-only audio-director author returns
`cgs.team-audio-proposal/v2` rows with:

- stable proposal ID, source role, input/context revisions, exact source references;
- exactly one destination, concise audio-spec constraint or `NONE`;
- required product/technical decision or `NONE`;
- owner, acceptance condition, dependencies, and status
  `PROPOSED | BLOCKED | TIMED_OUT | CANCELED`; and
- attempt identity/token/deadline/output revision.

Allowed destinations are exactly `AUDIO_SPEC`, `AUDIO_ASSET_BRIEF`,
`TECHNICAL_ADR_OR_SPEC`, `PERFORMANCE_BUDGET`, `QA_PLAN`, `BACKLOG_OR_STORY`, and
`REVIEW_ONLY`.

Direction proposals cover sonic identity, emotional tone, palette, adaptive-music
intent, abstract mix priorities, and player-facing audio goals. Present two or
three mutually exclusive choices only for genuine product decisions. Record
`cgs.audio-product-decision/v2` with decision ID, options/evidence revisions, choice,
rationale, authority, and timestamp. Routine derivation needs no repeated approval.

Unresolved creative direction returns DEFERRED/BLOCKED and prevents dependent
proposal dispatch.

## Phase 3: Collect sound and accessibility proposals

After direction is frozen, run sound-designer and accessibility-specialist together
against the exact direction/context revisions.

The sound-designer proposes stable event IDs, trigger/priority/player result,
spatial behavior, variation, abstract mix/ducking, captions, and asset needs.
Production instructions route to AUDIO_ASSET_BRIEF and are not copied into the spec.

The accessibility specialist independently checks critical-feedback redundancy,
captions/source identification, spatial alternatives, loud/sudden/high-frequency
controls, silence/overlap, and cue-priority masking. Use
`cgs.audio-accessibility-finding/v2` with stable `AXA-<artifact-id>-<stable key>`,
severity, event ID, exact evidence/path/revision, required outcome, owner, deadline,
status `OPEN | ROUTED | RESOLVED`, and resolution evidence.

A BLOCKING finding, especially critical game state communicated only by audio, is
non-waivable. Only an exact sound/visual/haptic design revision followed by one
finding-ID-preserving verification re-review may close it. The same blocker on the
second observation ends BLOCKED. No skip, acknowledge-and-proceed, accepted-risk
completion, or implementation branch exists.

Only non-blocking risk may be accepted, with exact finding ID/risk/owner/deadline/
approver/time. The verdict is `ACCEPTED RISK — NOT APPROVED`; it cannot reach SPEC
COMPLETE or implementation.

## Phase 4: Route technical and engine validation

After the player-facing draft is stable, run technical-artist and the configured
engine specialist in parallel. They are read-only and destination-tag every row.

- Middleware, bus/streaming architecture, and engine component/node patterns route
  to TECHNICAL_ADR_OR_SPEC.
- CPU, memory, voice-count, streaming, and platform thresholds route to
  PERFORMANCE_BUDGET.
- Implementation/integration work routes to BACKLOG_OR_STORY.
- Only player-facing rules and abstract design constraints may route to AUDIO_SPEC.

This skill writes none of those external destinations. Decisions requiring an ADR
remain owner-routed dependencies until an external Accepted ADR exists.

If engine evidence declares no configured engine, do not call an engine specialist
or guess engine/middleware patterns. Record `ENGINE_VALIDATION_DEFERRED` with
configuration path/revision, affected proposal/dependency IDs, owner, and exact trigger:
engine selected/configured or pinned version changed. Engine-neutral design may
later reach `SPEC COMPLETE — ENGINE VALIDATION DEFERRED`, but it is never
implementation-ready and cannot produce an implementation handoff.

## Phase 5: Reduce one authoritative audio-spec candidate

Build `cgs.team-audio-destination-ledger/v2`: every proposal/finding ID appears
exactly once with source revision, destination, owner, acceptance, dependency, and
status. Deduplicate by stable identity/evidence. Creative conflicts route to product
authority; technical conflicts route to technical owner. The reducer never guesses
or concatenates all agent prose.

Render exactly one UTF-8 candidate at
`design/audio/audio-<artifact-id>.md` using the schema in
`references/audio-spec-schema.md`. It contains only player-facing audio direction,
event/adaptive contracts, abstract mix behavior, accessibility alternatives,
design acceptance criteria, source revisions, and references to external destination
IDs. It excludes implementation, concrete technical architecture, budgets, tests/
QA results, asset production, and review transcripts.

If required output is missing/timed out/blocked or context is partial, an optional
candidate must visibly say `PARTIAL — NOT APPROVED`, list exact gaps, and cannot be
accepted or handed to implementation.

## Phase 6: Approve and write the exact candidate

After all genuine product choices, render complete bytes and create
`cgs.team-audio-write-plan/v2` with:

- artifact/run IDs, create/revise operation, exact spec/checkpoint paths;
- one transaction writer, source/context/decision/ledger revisions;
- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
- engine state, destination/open-blocker counts, deterministic write order;
- checkpoint transition candidate/revision, partial/recovery rules; and
- explicit non-writes.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
that revision, then one separate `cgs.team-audio-mutation-authorization/v2` for only the
spec candidate and exact checkpoint transition. A new byte/path/operation/owner/
source/engine/blocker state invalidates approval and authorization.

Immediately before writing, run source/context, spec/checkpoint target, identity/
ownership, decision/ledger, attempt-token, approval/authorization, and role atomic conflict check in
one read-only pass. Any mismatch yields zero spec writes and fresh planning.

The single writer writes the spec with atomic single-file replacement where
supported and immediate read-back/revision verification, then atomically updates the
checkpoint. Multi-file atomicity is not claimed. A spec success plus checkpoint
failure is PARTIAL and not safely resumable; preserve actual revisions, never delete
or overwrite for rollback, and print the complete recovery payload.

## Phase 7: Independent current-revision review

After verified spec write, run a fresh, read-only reviewer whose identity/token
differs from audio-director author and transaction writer. Review only the exact
Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
`cgs.audio-spec-review/v2`.

Review covers direction coherence, event identity/completeness, accessibility,
abstract mix/cue conflicts, adaptive-state transitions/interruption/recovery,
destination hygiene, dependencies/engine state, and acceptance criteria.
Findings use stable `AR-<artifact-id>-<check>-<stable key>` with severity, evidence
locator/revision, owner, required outcome, status, and resolution.

BLOCKING findings are non-waivable. Permit one exact author revision with a new
candidate/plan/approval/authorization, followed by exactly one fresh verification
re-review over stable OPEN IDs and diff regressions. The same blocker remaining on
the second observation is BLOCKED. Any spec revision change stales prior review, QA
plan proposal, and user acceptance.

## Phase 8: Plan future independent QA; do not execute it

After zero BLOCKING accessibility/review findings, a read-only qa-tester proposes
`cgs.audio-qa-plan-proposal/v2` bound to the current spec revision. Cases may cover event
triggers, priority/ducking, adaptive transitions, caption/alternative cues,
silence/overlap, platform routing, performance-budget references, and playback.

Every case status is `PLANNED`. This skill has no implementation/build/produced
audio and must report `IMPLEMENTATION NOT PRESENT`, `QA NOT RUN`, and `PLAYBACK NOT
RUN`. It writes no QA plan and never treats agent prose, filenames, unplayed
waveforms, or missing logs as execution evidence.

Future implementation acceptance requires independent QA outside this skill. Such
evidence must bind spec/build/asset revisions, protocol/environment/device/settings,
timestamps/duration, result/observer, raw log/capture/signature revision, and
PASS/FAIL/BLOCKED. This workflow neither produces nor consumes that evidence as a
completion requirement for design.

## Phase 9: Final evidence-bound acceptance

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

Emit `SPEC COMPLETE` only when:

- context coverage is complete and every fixed required agent completed in bounds;
- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
- zero BLOCKING accessibility/review findings and zero accepted-risk state remain;
- every product decision is resolved and every external technical/asset/QA/backlog
  item is destination-routed with owner/acceptance;
- engine validation is current;
- independent review and planned QA proposal bind the current spec revision;
- product authority accepts that exact revision/evidence packet; and
- final atomic conflict check and verified checkpoint update record state COMPLETE.

When every condition except engine validation passes, emit
`SPEC COMPLETE — ENGINE VALIDATION DEFERRED` with the exact trigger and no
implementation handoff. Declined/postponed acceptance is `DEFERRED — NOT APPROVED`.
Any safe but incomplete work is `PARTIAL — NOT APPROVED`; a decision, conflict,
non-waivable blocker, invalid checkpoint, or unsafe drift may be BLOCKED.

The final report and checkpoint include artifact/run IDs, exact spec path/revision,
context/decision/ledger/plan/authorization revisions, proposal/finding counts by
destination, agent attempt/deadline/result states, reviewer/result revision, engine/ADR
state, planned-versus-executed QA/playback labels, open blockers, last verified
phase, safe resume point, and exactly one verdict/next action.

Read and follow `references/execution-and-recovery.md` in full for checkpoint
transitions, resume, partial evidence, and terminal receipt rules.

## Handoff boundary

This skill never invokes an implementation workflow. A later implementation request
is legal only when the current spec revision is accepted, engine validation is current,
every required technical decision has an Accepted ADR, one story binds the exact
spec revision and acceptance criteria, and story readiness passes. Implementation and
independent runtime QA belong to separate user-authorized workflows.

For non-COMPLETE outcomes, return only the highest-priority product decision,
dependency, accessibility fix, context split, checkpoint recovery, or resume action.
Do not recommend code or asset production.
