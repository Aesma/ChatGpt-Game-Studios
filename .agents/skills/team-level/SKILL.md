---
name: team-level
description: Orchestrate one bounded level-design specification through read-only specialists, destination routing, deterministic agent/checkpoint states, a single authorized writer, and hash-bound accessibility, level-review, and QA evidence.
---

# Team Level

Design or revise exactly one level specification. This workflow never implements
gameplay, code, assets, dialogue, system tuning, tests, or adjacent levels. All
specialists, authors, accessibility reviewers, level reviewers, and QA planners
are read-only. One declared transaction writer alone may mutate the exact level
source and recovery checkpoint after a complete hash-bound authorization.

## Invocation

Use exactly:

```text
$team-level <level-id>
```

- Require exactly one argument before any project read or delegation.
- `level-id` matches `^[a-z0-9]+(?:-[a-z0-9]+)*$` exactly; do not normalize an
  ambiguous input into a different ID.
- Reject omitted/extra arguments, path separators, traversal, drive/device
  prefixes, control characters, whitespace, glob/regex syntax, leading/trailing
  hyphens, repeated hyphens, and unsafe Unicode with `run_status: ERROR`.
- On invalid input, show usage and safe examples, read no project file, dispatch
  no agent, request no decision/authorization, write nothing, and emit no design
  verdict.

Review modes do not apply. Do not read a review-mode file or accept
`--review full|lean|solo`. Required specialists/reviewers and evidence are the
same for every run; absence or timeout is explicit PARTIAL/BLOCKED state rather
than a role substitution or hidden quality downgrade.

## Load the private contracts

Read [team-level-contract-v1.md](references/team-level-contract-v1.md)
completely. It defines canonical hashes, fixed bounds, target/operation rules,
context and adjacency manifests, proposal/destination schemas, agent jobs,
checkpoints, level-review, QA, authorization, and completion evidence.

Read [continued-workflow.md](references/continued-workflow.md) completely and
execute it in order. Missing, unreadable, or contradictory contracts return
`run_status: ERROR` before project reads, delegation, decisions, or writes.

## Verdicts and state fields

The workflow verdict is exactly one of:

```text
COMPLETE — DESIGN APPROVED
PARTIAL — NOT APPROVED
ACCEPTED RISK / NOT APPROVED
BLOCKED — PRODUCT DECISION REQUIRED
```

Before a final verdict, record independent machine fields:

- `run_status: ACTIVE|PARTIAL|BLOCKED|COMPLETE|ERROR`;
- `phase_status: NOT_STARTED|READY|RUNNING|COMPLETE|PARTIAL|BLOCKED|TIMED_OUT|STALE`;
- `job_status: QUEUED|RUNNING|COMPLETE|BLOCKED|TIMED_OUT|INVALID|STALE`;
- `write_status: NOT_AUTHORIZED|AUTHORIZED|COMPLETE|PARTIAL|BLOCKED|ERROR`;
- `review_status: NOT_RUN|PASS|FAIL|PARTIAL|STALE`; and
- `approval_status: NOT_REQUESTED|PENDING|ACCEPTED|DECLINED|STALE`.

A produced file, accepted non-blocking risk, completed agent batch, or successful
write never implies DESIGN APPROVED. COMPLETE requires the full evidence matrix
in the private contract.

## User-decision contract

Do not ask for approval at routine phase transitions. Continue automatically
through deterministic read-only work while prerequisites hold.

Ask only when one of these exact conditions occurs:

1. create/revise operation is ambiguous because the target already exists or a
   supplied operation conflicts with observed existence;
2. the bounded context manifest cannot include all required candidates and the
   user must prioritize an explicit list;
3. a genuine product choice or cross-domain conflict has multiple materially
   different outcomes;
4. the user may accept a specifically identified non-blocking risk;
5. an open non-waivable blocker requires either one bounded author-revision scope
   or stop;
6. one complete write/recovery plan needs authorization before first mutation;
7. a materially changed revision requires a replacement write authorization; or
8. the final hash-bound design-acceptance packet and exact COMPLETE-checkpoint
   candidate need combined product acceptance and write authorization.

Every question names stable IDs, exact alternatives, effects, and the default
non-mutating outcome. No unanswered question is inferred as approval. A new
path, owner, operation, source baseline, material draft scope, or candidate hash
invalidates prior authorization.

## Permanent ownership and mutation boundary

Until an exact plan is authorized:

```text
allowed_project_write_set: []
specialist_writes: 0
reviewer_writes: 0
downstream_workflow_invoked: false
implementation_started: false
```

Normal candidate paths are exactly:

- `design/levels/<level-id>.md`; and
- `production/session-state/team-level-<level-id>.yaml`.

Choose one transaction writer before preview. It owns both paths for the whole
run and is the only participant that may write. All other roles return bounded
structured payloads. Each write plan binds exact candidate bytes/hashes for its
transition; it cannot pre-authorize unknown future checkpoint content. The first
source transaction may touch the level and checkpoint paths, while a later
finalization plan may touch only the same checkpoint path with the same writer.
No plan may add a third path. External destinations remain proposals for their
owning workflows.

Immediately before and after each authorized checkpoint/level write, compare
raw hashes for every source and target. Never overwrite in create mode, expand
paths by implication, hide a partial write, or let a new owner reuse approval.

## Phase 0 — Freeze target, operation, and run identity

After input validation, resolve the two canonical targets. Capture raw SHA-256 or
`ABSENT`, file type, and canonical confinement. Determine:

- `CREATE` only when level and checkpoint targets are absent;
- `REVISE` only when the level exists and the user explicitly chooses revision;
  and
- `RESUME` only from a valid matching checkpoint.

An existing target blocks CREATE. Missing baseline blocks REVISE. A checkpoint
whose ID/path/schema/hashes do not match current bytes is STALE and cannot
authorize resume. Freeze a run ID from level ID, operation, source-baseline set,
and start UTC timestamp.

## Phase 1 — Build a bounded context manifest

Read root and nearest applicable `AGENTS.md` for both target paths, then only:

1. `design/gdd/game-concept.md` and `design/gdd/game-pillars.md`;
2. the existing target level source in REVISE/RESUME;
3. explicit first-level references from the user brief, required sources, or the
   target source to narrative/world/art/accessibility/system/level artifacts; and
4. one hop of exact adjacent-level interface sources.

Do not recursively crawl design directories. The private contract sets file,
byte, excerpt, adjacency, and prompt budgets. Every manifest row records stable
source ID, canonical path, raw hash, bytes, selected sections/excerpt hashes,
reason, dependency depth, required/optional state, and omission state.

If required candidates exceed a bound, stop before delegation and ask the user
to prioritize the explicit omitted/included list. Never silently truncate.
Detect duplicate/cyclic references; record the cycle and do not follow it.
Compute `context_manifest_sha256` over the canonical ordered rows.

Each job receives only the manifest identity, task-relevant bounded excerpts,
stable references, and required prior structured payloads. Never pass the entire
project context or all earlier agent output verbatim.

## Phase 2 — Validate adjacency interfaces

Represent every adjacency as a stable directional interface record with source
and target level IDs, interface ID, endpoints, directionality, traversal/state
contract, declared revision/hash, reverse-interface reference, and dependency
owner.

Classify each as:

```text
PLANNED | AUTHORED | UNRESOLVED | BROKEN_LINK | INTERFACE_CONFLICT
```

`PLANNED` requires an explicit manifest/roadmap declaration even if no level file
exists. `AUTHORED` requires both authored documents and compatible forward/
reverse claims. Missing target/reverse reference is `BROKEN_LINK`; mismatched
direction, endpoint, traversal state, ID, revision, or reverse claim is
`INTERFACE_CONFLICT`. File existence or a matching filename alone proves none of
these states.

Never invent or auto-author an adjacent level, start another `$team-level`, or
follow a dependency chain beyond one hop. Required BROKEN_LINK,
INTERFACE_CONFLICT, or UNRESOLVED state prevents COMPLETE.

## Roles, batches, and deterministic agent jobs

At most three subagents may be live. Required roles are selected from the
manifest by the applicability matrix in the private contract; level author,
accessibility reviewer, independent level reviewer, and post-source QA planner
are always required. No generic review mode removes or replaces them.

Every job is `cgs.team-level-job/v1` with stable job ID, role, phase, required
flag, exact input hashes, output schema, maximum bytes, dispatch/deadline UTC,
attempt/follow-up count, status, result payload/hash or failure, and dependency
job IDs. Default deadline is ten minutes unless the user imposed a shorter one.
Allow at most one narrowed follow-up before the same deadline; never extend the
deadline, silently substitute a role, forge a result, or spawn repeated
replacements.

At deadline, mark `TIMED_OUT`. Preserve completed independent results. When core
identity/context/level draft evidence remains usable, return a bounded PARTIAL
packet and exact resume point; otherwise BLOCK. A timed-out/invalid/missing
required job always prevents COMPLETE.

## Phase 3 — Collect destination-routed proposals

Run applicable narrative-director, world-builder, and art-director jobs in one
bounded read-only batch. A proposal is `cgs.team-level-proposal/v1` with stable
proposal ID, role/job hash, exactly one destination, source/excerpt refs and
hashes, concise level-facing constraint or NONE, assumptions, stable dependency
IDs, product-decision IDs, status, and payload hash.

Allowed destinations are exactly:

```text
LEVEL_SOURCE | NARRATIVE_LORE | ART_BRIEF | SYSTEM_GDD |
QA_PLAN | BACKLOG | REVIEW_ONLY
```

Dialogue/lore prose routes to NARRATIVE_LORE; palettes, assets, VFX, and
production concepts to ART_BRIEF; reusable mechanics, formulas, tuning, loot and
enemy values to SYSTEM_GDD; tests to QA_PLAN. Only spatially authoritative,
testable level constraints may enter LEVEL_SOURCE.

After that batch, run one read-only level-designer author using only
LEVEL_SOURCE proposal fields and references to other destinations. It returns an
in-memory level source with identity, purpose/bounds, critical/optional paths,
pacing, navigation/landmarks, entry/exit and softlock prevention, encounter
interface IDs/contracts, adjacency records, level-facing accessibility,
dependencies, and product decisions.

Run systems-designer and location art-director against the layout draft hash in a
second bounded batch. Cross-domain contradictions become product-decision
records; the reducer never silently chooses. Every proposal is routed once.
Never concatenate transcripts or copy external-destination content verbatim.

## Phase 4 — Accessibility review and bounded convergence

Run a fresh read-only accessibility specialist against the exact layout draft
hash and committed accessibility requirement hashes. Findings use stable
fingerprints/IDs and include severity `BLOCKING|RECOMMENDED|NICE_TO_HAVE`, exact
evidence, affected path/encounter, testable outcome, owner, status, and round.

BLOCKING is non-waivable. The user may choose one exact bounded author diff scope
or stop with `BLOCKED — PRODUCT DECISION REQUIRED`. There is no acknowledge-and-
continue route. A non-blocking risk may be accepted only with finding ID/hash,
bounded risk, owner, deadline, approver, and timestamp; that branch ends
`ACCEPTED RISK / NOT APPROVED`.

An approved blocker revision uses one separate read-only author job and exactly
one verification re-review. The reviewer checks original OPEN IDs and regressions
caused by the exact diff only. Original IDs persist; regression IDs bind the
triggering finding/diff hash. If an original blocker remains open on its second
observation, stop. Never start a third review/rewrite cycle.

## Phase 5 — Route, reduce, and freeze the level source

Build a canonical routing ledger with every proposal/finding ID exactly once.
The reducer includes only the authoritative LEVEL_SOURCE fields defined in the
private contract and references other destinations by stable IDs/hashes. It
excludes lore/dialogue, production art briefs/assets, formulas/tuning, QA cases,
backlog bodies, review discussion, prompts, and raw agent output.

Resolve genuine product choices, then freeze canonical UTF-8/LF level bytes and
`level_draft_sha256`. Record all included proposal/decision/resolved-finding IDs,
current context hash, adjacency/dependency states, and open blocker count.

After every completed phase, construct the next canonical in-memory
`cgs.team-level-checkpoint/v2` snapshot with monotonically increasing
`state_seq`, source/target hashes, decisions, bounded job result payloads/hashes,
routing/finding state, last verified phase, and exact safe resume action. Before
authorization it remains in memory and no project write occurs.

## Phase 6 — Authorize and execute the bounded source transaction

Preview one complete plan with exact two-path write set, create/modify operation
and exact candidate bytes/hash for each path, single writer, baselines,
all source/context/draft hashes, routing ledger, blocker/dependency states,
success/partial/rollback conditions, and canonical `plan_hash`. Obtain one
authorization bound to the full plan.

Rehash all sources/targets. On change, invalidate plan/authorization before any
write. The writer creates/modifies only the level source and checkpoint with
compare-and-set/no-replace semantics, then rereads and verifies exact bytes and
hashes. Checkpoint state is never approval evidence by itself.

On failure, claim rollback only when every changed target byte equals its
verified baseline. Otherwise preserve honest current hashes, persist the planned
PARTIAL checkpoint when possible, and return PARTIAL. If checkpoint persistence
fails, print its complete bounded payload as `RECOVERY CHECKPOINT NOT PERSISTED`
and name every unverified path; never claim safe resume.

## Phase 7 — Independent hash-bound level review

After the level source exists and its raw hash verifies, run one fresh independent
read-only reviewer who is not an author or transaction writer. Apply only the
private `cgs.level-review/v1` profile: critical-path continuity, sequence breaks/
softlocks/recovery, pacing, adjacency direction/interface compatibility,
navigation/wayfinding, accessibility, and encounter contracts/dependencies.

Never invoke `$design-review` or system-GDD section rules. Findings use stable
level-review IDs and bind current level raw hash/source sections. A changed level
hash makes all prior review evidence STALE.

For BLOCKING findings, allow at most one separately scoped author revision with a
replacement plan/authorization and exactly one verification re-review limited to
original IDs plus diff regressions. An original blocker still open on second
observation stops BLOCKED. Reviewer timeout, invalid evidence, role collision, or
hash mismatch makes review PARTIAL and prevents COMPLETE.

## Phase 8 — Generate QA plan only after final source hash

Only after the current post-integration/post-review level hash has zero open
BLOCKING accessibility and level-review findings, run one read-only qa-tester.
Its input binds that current raw hash and resolved finding/review IDs. It returns
`cgs.team-level-qa-proposal/v1` with stable planned critical-path, sequence-break,
softlock, boundary, navigation, accessibility, encounter, and playtest case IDs.

The reducer may not change the level after QA input freezes. Any level-byte
change makes the QA proposal STALE and requires a fresh Phase 7 review followed
by fresh Phase 8 QA. Do not write a QA plan in this workflow. These cases are
`PLANNED`, never PASS/executed evidence. Missing/invalid/timed-out QA prevents
COMPLETE.

## Phase 9 — Final acceptance and COMPLETE evidence matrix

Build one final packet binding current level hash, plan/context/checkpoint hashes,
agent job result hashes/statuses, destination ledger, adjacency/dependency states,
zero-blocker findings, independent level-review evidence, planned QA proposal,
all user decision records, and the exact COMPLETE-checkpoint candidate path,
baseline, bytes, hash, writer, compare-and-set condition, and finalization plan
hash. Ask once for combined product acceptance and write authorization of that
exact packet/transition. Prior source-write authorization is not reused for
previously unknown final checkpoint bytes.

`COMPLETE — DESIGN APPROVED` requires every mandatory predicate in
`TL-COMPLETE/v1` from the private contract, including exact target hash, zero open
blockers, no required timeout/partial job, resolved required dependencies,
independent current-hash review PASS, current-hash QA proposal, matching accepted
packet, and a final compare-and-set checkpoint transition by the same authorized
writer. If any predicate is false/unknown, COMPLETE is forbidden.

Final design acceptance does not authorize implementation or another destination.

## Resume and idempotence

On RESUME, validate checkpoint schema, level/run/operation identity,
monotonic `state_seq`, `plan_hash`, context/source/target/current hashes, job
payload/result hashes, write sets, findings, review round, and safe resume phase.

Reuse a COMPLETE job only when its full input hash and stored bounded output
payload/hash validate. Reuse a completed write only when target bytes/hash equal
the checkpoint. Mark mismatches STALE and re-enter the earliest affected phase;
never duplicate a valid job, write, user decision, review round, or QA proposal.
No prose-only claim is resumable evidence.

## Return and stop

Return `cgs.team-level-run/v2` with level/run/operation identity, exact paths and
hashes, context/adjacency/routing summaries, every job/deadline/result state,
decisions, accessibility/level-review evidence and rounds, QA PLANNED IDs,
checkpoint state/safe resume, write receipt, COMPLETE predicate matrix, and one
workflow verdict.

For non-COMPLETE, provide only the blocking product decision or exact safe resume
action; never recommend implementation. For COMPLETE, external destinations and
`$qa-plan` are separate owning-workflow handoffs. Implementation may begin only
later from stories bound to this approved level hash and independently ready.
Stop.

## Non-negotiable rules

- Never call `$design-review` for a level document.
- Never waive a BLOCKING accessibility or level-review finding.
- Never let an author/writer self-review.
- Never run an unbounded review/revision loop.
- Never pass full context or all output verbatim.
- Never generate QA before the final current level hash.
- Never write an external destination or allow multiple writers.
- Never fabricate hashes, jobs, review, test, approval, or checkpoint state.
- Never call PARTIAL, accepted risk, or file production DESIGN APPROVED.
