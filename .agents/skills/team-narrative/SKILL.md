---
name: team-narrative
description: "Coordinate canon-safe narrative content through frozen-baseline planning, bounded read-only proposals, single-owner writes, localization gating, and independent final-hash review."
---

# Team Narrative

Create or revise narrative content without allowing parallel authors, stale reviews,
or unresolved localization defects to change canon or ship as complete.

## Invocation contract

Invoke as:

`$team-narrative --manifest {narrative-content-request-path} [--resume {checkpoint-path}]`

Parse and validate arguments before reading project files, delegating, asking for a
decision, or writing anything. With no manifest, print the usage line and stop with
no side effects. Do not infer a topic from the repository.

The request manifest is required to contain:

- stable `content_id`, unique `run_id`, and operation `create` or `revise`;
- narrative goal, intended audience, content-rating policy, and spoiler class;
- requested artifact types and explicit destination paths;
- canon roots, registries, voice profiles, UX/string constraint sources, and
  gameplay/level trigger-contract sources;
- expected base hash for every existing file that may be changed;
- proposed owner role for every artifact and every shared registry;
- read budget per source group, maximum parallelism, per-attempt deadline, phase
  deadline, and checkpoint root;
- the authority allowed to decide canon, authorize canon promotion, and authorize
  narrative-content writes.

Reject path traversal, absolute paths outside the repository, duplicate normalized
paths, duplicate IDs, missing revise targets, occupied create targets, unsupported
artifact types, and any manifest that names the same path for two writers. Never
write through symlinks or junctions that resolve outside the repository.

## Non-negotiable invariants

1. Canon validation and explicit canon decisions finish before dialogue, visual, or
   level proposals start. A frozen canon baseline hash is the hard dependency gate.
2. Delegates are read-only proposal or review agents until a separately authorized
   mutation manifest names their exact paths. A proposal is never permission to
   write.
3. Each artifact path has exactly one writer. Shared registries and manifests have
   one recorder and are updated sequentially with base-hash checks.
4. An author cannot approve their own artifact. Final review is fresh, independent,
   read-only, and bound to the final artifact-set hash.
5. Any blocking localization defect yields `NOT LOCALIZATION READY`; accepting the
   risk does not turn it into `COMPLETE` and does not permit downstream localization
   or implementation handoff.
6. Do not invoke a system-GDD review workflow for narrative artifacts. Use the
   narrative review profile in this document.
7. Never implement engine code, triggers, assets, translations, or other production
   work. This workflow produces authorized narrative artifacts and contracts only.

## Evidence and records

Use immutable operational records under:

`production/narrative/team-narrative/{content_id}/{run_id}/`

The coordinator is the sole writer for these records:

- `context-manifest.yaml`: normalized source paths, exact hashes, selected sections,
  byte/token budgets, omissions, and dependency edges;
- `ownership-manifest.yaml`: artifact path, artifact type, one writer identity,
  reviewer identity, destination owner, and expected base hash;
- `mutation-manifest.yaml`: the exact authorized operations and limits;
- `checkpoints/{sequence}-{phase}.yaml`: immutable phase state and attempt tokens;
- `review/narrative-review.yaml`: final review evidence;
- `result.yaml`: terminal status and one next action.

Every finding and proposed change has a stable ID. Use `NCF-{check-id}` for canon
findings, `NCP-{artifact-id}` for proposals, `LOC-{string-id}-{check-id}` for
localization findings, and `NRF-{profile-check-id}` for final-review findings.

## Phase 1: Validate request and build bounded canon graph

1. Normalize and validate the request manifest and all destination paths.
2. Build a directed canon dependency graph from only the declared roots and direct
   references. Detect cycles, missing references, ambiguous IDs, and budget overflow.
   Do not recursively load the whole repository.
3. Write `context-manifest.yaml` only within already granted orchestration-record
   authority. If that authority is absent, keep the record in conversation and
   return `BLOCKED` without creating it.
4. Delegate a read-only canon inspection to `world-builder`. It returns source-bound
   findings and a proposed canon diff; it creates or edits no files.
5. Delegate a read-only narrative brief proposal to `narrative-director`. It must cite
   the context-manifest hashes and mark assumptions as unresolved, not canon.

If context is missing or contradictory, report stable finding IDs, the competing
claims with source paths and hashes, affected downstream artifacts, and selectable
canon options. Stop before any writer, art-director, or level-designer delegation.

## Phase 2: Decide, authorize, and freeze canon

Canon choice is a product decision. Ask the named canon authority to choose among
the source-backed options; never select a convenient version on the user's behalf.
Record the decision ID, choice, rationale, decision-maker, and timestamp.

If the decision requires changing canon, first present a canon-only mutation
manifest containing every operation, path, expected base hash, proposed new ID or
registry entry, assigned unique writer, maximum bytes, and explicit non-writes.
Obtain separate promotion authorization from the named authority. Then:

1. one canon writer applies the authorized canon files sequentially;
2. one canon-registry recorder updates shared registries sequentially;
3. each writer verifies the expected base hash immediately before writing and stops
   on drift or an unlisted path;
4. read back every changed file, validate IDs and references, and compute hashes;
5. compute the canon-baseline hash from a canonical, sorted manifest of canon paths
   and hashes.

No downstream proposal may start until the checkpoint state is `CANON_FROZEN` and
contains the canon-baseline hash. Authorization refusal, unresolved canon, hash
drift, validation failure, or an unverified registry update is `BLOCKED`.

## Phase 3: Run bounded read-only proposals

After `CANON_FROZEN`, issue these independent proposal tasks together, up to the
manifest's maximum concurrency and never more than three at once:

- `writer`: dialogue, string-key, lore-text, and voice proposals;
- `art-director`: a visual narrative brief only, with no asset production;
- `level-designer`: trigger, discovery, pacing, and environmental-storytelling
  contracts only, with no engine implementation.

Each task receives the same frozen canon-baseline hash, only its declared context
slice, an artifact schema, prohibited paths, and a unique attempt token. It returns
proposal text, citations, destination suggestions, assumptions, and stable proposal
IDs. It must not write content or operational files and must not delegate again.

Concurrency controls:

- default and maximum concurrency: 3;
- default per-attempt deadline: 15 minutes; manifest may lower it, not raise it;
- maximum phase deadline: 30 minutes;
- at most one retry, only for an attempt proven to have made no writes;
- on timeout or cancellation, revoke the attempt token and ignore/quarantine every
  late result or patch from that token;
- a missing, timed-out, or invalid proposal produces `PARTIAL` and a checkpoint;
  dependent writes do not begin.

## Phase 4: Route ownership and obtain write authorization

Reconcile proposals without writing them. Create an ownership manifest where every
normalized destination path has one writer and every writer has a disjoint path set.
Typical ownership is:

- canon files: canon writer; canon registry: canon-registry recorder;
- arc/brief: narrative author; dialogue/string source: dialogue writer;
- lore entry: lore writer; trigger contract: level-integration writer;
- visual narrative brief: art-brief writer;
- operational evidence and final result: coordinator recorder.

Experts may propose across these boundaries, but only the named owner may write the
path. If a shared path cannot be split, assign one recorder and serialize all
accepted changes through that recorder.

Before the first narrative-content write, present one exact mutation manifest that
lists every operation, destination, expected base hash, writer identity, proposal
IDs, size limit, and explicit non-writes. Obtain authorization from the named content
authority. Unknown paths and later scope expansion require a revised manifest and
new authorization. Do not ask again per file inside an unchanged authorized scope.

## Phase 5: Localization review before delivery

The `localization-lead` performs a read-only review of accepted dialogue and string
proposals against the actual declared UX and string-system sources. Never substitute
a generic fixed limit such as 120 characters. If a constraint source is absent,
record the constraint as `UNKNOWN` and block affected strings.

Check stable string IDs, source-language ownership, placeholders, formatter
contracts, plurals, gender, grammar dependencies, concatenation, locale-specific
dates/numbers, expansion budgets from the real UI constraints, cultural assumptions,
content-rating exposure, and spoiler partitioning.

Every blocking defect must be fixed by the assigned artifact owner inside the
authorized manifest and then re-reviewed, or the run becomes
`NOT LOCALIZATION READY`. A user may accept the business risk, but the terminal
verdict remains `PARTIAL`, never `COMPLETE`, and no localization or implementation
handoff is allowed.

## Phase 6: Apply writes and verify read-back

Only after canon freeze, valid ownership, localization clearance, and content-write
authorization may the unique artifact owners write. Apply operations sequentially
per path with an immediate base-hash guard and atomic replacement where supported.
Reject unlisted writes, ownership mismatches, oversized output, broken references,
or a changed canon-baseline hash.

After all writes, read back every artifact, validate schema and reference integrity,
and create a canonical sorted final artifact manifest. Its hash is the
`final_artifact_set_hash`. A write failure produces `PARTIAL`; do not claim or infer
that an unwritten proposal was delivered.

Mystery truths belong only in an access-controlled private canon artifact such as
`design/narrative/canon/private/{content_id}-truths.*`. Public artifacts may contain
stable truth IDs but not their protected answers. Validate the declared spoiler
class and access boundary during read-back.

## Phase 7: Independent narrative review on final hashes

Spawn a fresh reviewer who did not author, edit, record, or approve any reviewed
artifact. The reviewer is read-only, receives the frozen canon-baseline hash and
`final_artifact_set_hash`, and loads only the final hashed files. The reviewer uses
this narrative-specific profile:

- canon consistency and source/hash/reference integrity;
- character voice and relationship continuity;
- arc purpose, pacing, causality, and emotional progression;
- gameplay/level trigger-contract completeness without implementation;
- mystery truth-ID coverage and public/private spoiler separation;
- localization readiness and real UX/string constraints;
- content-rating and cultural-safety policy compliance.

Persist stable findings, severity, evidence path/hash, owner, required destination,
and disposition in `review/narrative-review.yaml`. The review is current only when
its recorded artifact-set hash equals the recomputed final hash.

If polish or fixes occur, the prior approval becomes stale. The same unique owners
may apply only authorized fixes; then recompute hashes and run a fresh independent
scoped review over every changed artifact and its dependents. Allow at most two fix
rounds. Unresolved blockers, stale evidence, or reviewer/author identity overlap is
`PARTIAL` or `BLOCKED`, never `COMPLETE`.

## Checkpoint and recovery protocol

Write an immutable checkpoint after request validation, canon decision, canon
freeze, proposals, authorization, localization review, writes, and final review.
Each checkpoint records input hashes, output hashes, decisions, authorizations,
ownership, active/revoked attempt tokens, completed and pending work, blockers, and
the exact next safe phase.

On `--resume`, validate content ID, run ID, checkpoint chain, current source hashes,
canon-baseline hash, authorization scope, and absence of late writes. Resume only
from the recorded next phase. Drift or an invalid chain is `BLOCKED`; never silently
restart or reuse stale proposals/reviews.

Agent errors are surfaced immediately. Preserve valid read-only proposals in the
checkpoint, cancel dependents, and return `PARTIAL` when independent work succeeded.
Never skip a required agent, reviewer, canon decision, or localization blocker to
keep the pipeline moving.

## Completion gate and output

`Verdict: COMPLETE` is legal only when all of the following are true:

- canon is frozen and its current baseline hash is recorded;
- every authorized artifact exists at its declared path with its final hash;
- ownership and base-hash guards passed, with no unlisted writes;
- localization status is `LOCALIZATION READY` with zero blocking findings;
- canon, voice, arc, trigger contract, mystery-truth boundary, content rating, and
  references pass the independent review on the current final artifact-set hash;
- all final evidence, checkpoints, and `result.yaml` were read back successfully;
- there are zero unresolved blockers and zero stale or late results.

Otherwise return exactly one of:

- `Verdict: PARTIAL` — safe work/evidence exists, but delivery is incomplete; include
  `NOT LOCALIZATION READY` when applicable;
- `Verdict: BLOCKED` — no safe progress can continue without a decision, authority,
  missing dependency, or drift resolution.

The final report includes content/run IDs, status, canon-baseline hash, final
artifact-set hash, artifact path/hash/owner table, authorization IDs, localization
status and evidence, final reviewer identity and review hash, blockers, checkpoint
path, and exactly one status-driven next action.

For `COMPLETE`, the next action may be an explicit downstream handoff request using
the artifact manifest and `LOCALIZATION READY` evidence. Do not invoke another
workflow and do not start localization, assets, or production implementation from
this skill. For `PARTIAL` or `BLOCKED`, the one next action must resolve the named
blocking condition.
