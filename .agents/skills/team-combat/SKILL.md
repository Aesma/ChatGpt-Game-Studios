---
name: team-combat
description: "Implement one exact combat story only from independently approved design, Accepted architecture, persisted READY evidence, an engine-bound technical plan, and a manifest-authorized non-overlapping write set; completion requires independently reviewed functional and performance evidence."
---

# Team Combat

Coordinate one bounded combat implementation. This workflow never converts free text
into product rules, authors or approves a GDD, accepts an ADR, declares a story Ready,
chooses an engine, fabricates a test/performance result, or closes a story/release.

## Invocation and strict request

Invoke only as:

`$team-combat --request <path> --request <revision>`

Require both flags exactly once. Reject unknown/duplicate keys, missing values,
directories, globs, unsafe/escaping/symlink paths, mutable aliases, unsupported schemas
and request-revision drift. Stop before project discovery, delegation or writes on invalid
invocation.

The strict request is `cgs.team-combat-request/v2` with one operation:

- `PREFLIGHT` — read-only prerequisite, architecture, interface and ownership analysis;
- `EXECUTE` — one exact already-approved implementation manifest;
- `STATUS` — read-only checkpoint and mutation/evidence validation; or
- `RESUME` — continue from one exact immutable checkpoint.

It binds stable run/story/feature IDs; exact story/GDD/design-review/readiness record and
recorder receipt; Accepted ADR ledger; approved tech spec and independent review;
control manifest, QA plan, test-ID ownership, engine profile/version, context manifest,
file-ownership manifest and mutation authorization as applicable; expected predecessor
checkpoint; fixed file/byte/dependency/agent/response/time budgets; and applicable
root-to-target `AGENTS.md` path/revision chain.

A free-text feature, story status text, conversation approval, role recommendation,
accepted-risk prose or previous run is not admission. Never infer newest evidence,
current story, engine, reviewer, ADR, tech spec, manifest, checkpoint or target.

## Authority and side-effect boundary

Before exact manifest approval, every activity is read-only and all planners have
`mutation_authority: NONE`. After approval, only named owners may create/update exact
manifest rows whose base revision/ABSENT precondition still matches. Globs, directories,
“related files,” broad feature authority and retroactive authorization are invalid.

Keep GDD/ADR/story/readiness/control/QA-plan lifecycle, implementation, shared-file
integration, test execution/evidence, performance capture/evidence, checkpoint, bug,
story closure, release and deployment authorities separate. Delegation, retry, resume,
risk acceptance or user enthusiasm never broadens authority.

The orchestrator remains read-only. It never writes GDDs, ADR lifecycle, story/readiness
state, QA plans, external producer evidence, bugs, release state or shared session state.
Every authorized mutation is performed by the sole manifest owner and verified from
workspace bytes.

## Status axes

Report independently:

- `Workflow State`: `PREFLIGHT`, `AUTHORIZED`, `RUNNING`, `INTEGRATING`, `VERIFYING`,
  `COMPLETED`, `PARTIAL`, `BLOCKED`, or `ERROR`;
- `Implementation Verdict`: `COMPLETE`, `NEEDS_WORK`, `PARTIAL_NEEDS_WORK`, or
  `BLOCKED` (display `PARTIAL_NEEDS_WORK` as `PARTIAL / NEEDS WORK`);
- `Merge/Closure Eligible`: `NO` for every state in this workflow; downstream owners
  independently review and close lifecycle; and
- `Persistence`: `ANALYSIS_ONLY`, `VERIFIED`, `DECLINED`, `FAILED`, `CONFLICT`, or
  `NOT_ATTEMPTED`.

Never emit a bare success from task counts. COMPLETE is allowed only through the
deterministic completion record below and still does not close or merge the story.

## Phase 0 — Validate approved inputs

Read each declared input once and validate explicit version/revision metadata for
review/readiness records, every ADR, architecture/tech package, control manifest, QA
plan, engine profile, instruction chain and context manifest.

Require:

- independent P1 design review with formal `APPROVED`, exact GDD path/current revision,
  reviewer/author separation, complete coverage and zero unresolved blocker;
- persisted `cgs.story-readiness-record/v1` verdict `READY` for the exact story ID/path/
  raw revision plus `cgs.story-readiness-recorder-receipt/v1` result `RECORDED` or
  `ALREADY_RECORDED`, `implementation_gate_eligible: true`, current registry revision and
  exact dependencies;
- complete testable acceptance criteria with stable TR/AC/Test IDs and evidence targets;
- current control-manifest identity and P1 `cgs-qa-plan`, Schema Version 2, generation
  and recomputed effective states CURRENT, complete scope, `Build Binding` suitable for
  the requested phase and `Gate Evidence: NO`;
- every governing ADR exact, current and lifecycle `Accepted`; and
- configured engine, pinned version, validated project adapter/specialist and target
  platform/configuration profile for EXECUTE.

A Proposed ADR, authoring receipt, advisory/solo review, conversation READY, plan
COMPLETE, stale dependency or accepted risk cannot substitute. Any mismatch returns
`BLOCKED — APPROVED INPUTS NOT PROVEN`, zero writers and zero writes.

## Architecture and durable technical basis — TCB-006

Classify every planned semantic change before implementation:

- `ADR_REQUIRED` for module/public interface, persistence/schema ownership, threading,
  networking/authority, engine subsystem, cross-system lifecycle or other significant
  architectural choice;
- `TECH_SPEC_REQUIRED` for bounded implementation/interface detail already permitted by
  Accepted ADRs; or
- `NOT_ARCHITECTURAL` only with a contract-defined reason and exact governing source.

For ADR_REQUIRED, consume only an exact Accepted ADR with decision locator, lifecycle
record/revision and independent architecture-review evidence. The P1 architecture-decision
authoring output remains Proposed and is not enough. If absent, emit a stable blocker
and route the exact question to the architecture owner; do not draft or accept it here.

For TECH_SPEC_REQUIRED, require persisted `cgs.combat-tech-spec/v2` with stable spec ID,
story/GDD/ADR/control/engine identities, components, data/control flow, event/payload/
AI/VFX/audio/tuning interfaces, failure/rollback, observability, performance strategy,
test seams, target files and supersession identity. Require an independent
`cgs.combat-tech-spec-review/v1` path/revision with reviewer/author separation, exact target
revision and `APPROVED` verdict. Session sketches and planner summaries are not durable
technical authority.

### Missing-engine branch — TCB-014

PREFLIGHT may return an engine-neutral architecture-gap plan when engine is missing,
but it is `ENGINE_NEUTRAL_PLAN_ONLY / IMPLEMENTATION_BLOCKED`, creates no technical
authority or write manifest, and cannot proceed to EXECUTE.

Planning then freezes `cgs.combat-interface-contract/v2`, strictly derived from the
approved architecture package: gameplay events/payloads, AI hooks, VFX hooks, audio
events, tuning schema, deterministic fixtures and versioned compatibility rules. Every
planner proposal binds its revision. Disagreement or a new architecture decision blocks.

## Bounded context protocol — TCB-012

`cgs.combat-context-manifest/v2` is the only context authority. It lists exact
story/GDD/ADR/control/QA/tech/engine sources; component/interface excerpts and raw-byte
span revisions; expected target paths/base revisions; explicit first-order dependencies; and
fixed budgets.

Default hard ceilings are 32 files, 2 MiB, dependency depth 2, 64 interface rows, 6
planner assignments, 128 KiB response per assignment and 30 minutes. A request may lower
but never raise them. Normalize and sort canonical paths/IDs; reject duplicates and
scope disagreement.

Load only declared paths and dependencies. Admit whole dependency/interface closures;
record selected, loaded, missing, unreadable, invalid, omitted and unprocessed rows with
bytes/depth/reason. Required omission or budget exhaustion blocks implementation. Each
delegate receives paths/revisions, minimal interface excerpts and target diff context, not
full repository context. Returned proposals are bounded schema rows plus summaries.

## Staffing without review mode — TCB-011

There is no `full|lean|solo` review mode and no director-gate template. Reject `--review`
or review-mode fields. Required roles derive only from explicit story/tech-spec
dependency rows:

- gameplay-programmer for core/private gameplay paths;
- ai-programmer only for declared AI dependency;
- technical-artist only for declared VFX dependency;
- sound-designer only for declared audio dependency;
- resolved engine specialist for engine validation;
- qa-tester/test owner for pre-implementation contract and functional execution;
- performance-analyst for required performance evidence; and
- lead-programmer or explicitly designated gameplay-programmer as integration owner.

If a required role is unavailable, keep its work nonconclusive and return
PARTIAL_NEEDS_WORK or BLOCKED according to dependency impact. The orchestrator cannot
impersonate an independent reviewer, test executor or performance owner.

## Phase 1 — Freeze requirements, interfaces and tests before implementation — TCB-015

Read-only planners map every AC to exact approved GDD/ADR/tech rules and propose exact
paths/interfaces. Missing product rule blocks; programmers may not decide it.

Before implementation authorization, require `cgs.combat-test-contract/v2` produced by
the test owner and independently reviewed against the current QA plan. It binds run/
story/GDD/ADR/control/tech/interface/engine/platform revisions; every stable AC/Test ID;
preconditions, inputs, expected observables, deterministic fixtures, negative/boundary/
integration/performance coverage; exact test source/evidence paths; approved commands,
runner/parser/tool versions, environment/config; pass/fail/skip/not-run semantics; and
evidence-review destination.

The contract is a plan, not execution. Implementation writers cannot edit it. If test
sources/fixtures must be created, their exact paths/owners appear in the later mutation
manifest and are materialized before dependent production code tasks. A missing/partial/
stale/unreviewed test contract blocks EXECUTE.

## Phase 2 — Exact file-ownership manifest

Build `cgs.combat-file-ownership-manifest/v2` before any writer. Every sorted row has:

```text
path, operation CREATE|UPDATE, sole owner, raw base revision|ABSENT, purpose,
story/TR/AC/Test IDs, input/interface/test-contract revisions, shared true|false,
preconditions, expected postcondition and rollback/recovery rule
```

Include all production, AI, VFX, audio, data, test, fixture, integration, evidence and
checkpoint paths. No unknown runner outputs may become retained project artifacts.

Every path has one owner. Shared controllers/event buses/registries/scenes/prefabs/
resources/integration fixtures belong only to the named integration owner. Domain
writers may submit read-only shared-path patch proposals but cannot write them.

Choose the integration owner before approval. Allocate manifest_id as TCM-{story-id}-{UTC-run-id} and assign an explicit monotonic manifest_revision. Bind input, architecture, interface, test-contract, engine, and sorted row revisions to that record. Present exact paths/operations/owners/bases, dependency batches, deadlines/retry, integration owner, commands/evidence destinations, and checkpoint targets. Obtain one authorization for that exact manifest ID and revision. A new path, owner, operation, byte sequence, or base returns SCOPE_CHANGE_REQUEST without writing and requires a revised manifest/authorization.

## Immutable checkpoint and recovery — TCB-013

The integration owner is sole writer for approved checkpoints at:

```text
production/combat/runs/{run-id}/checkpoints/
  {sequence}-{checkpoint-identity-revision}.yaml
```

Each create-only `cgs.combat-checkpoint/v2` binds request/input/context/architecture/
interface/test-contract/engine/manifest/authorization identities; predecessor path/revision;
phase/verdict; assignment IDs/owners/paths/deadlines/retry/cancel/late states; written
pre/post revisions; mutation audit; build/test/performance/review evidence; unresolved rows;
and exactly one next action. Never update shared `production/session-state/active.md`.

RESUME requires exact checkpoint path/revision and predecessor chain. re-read every source,
manifest target, written output and evidence; verify next-target preconditions and
reconcile ambiguous task/writer outcomes. Do not rerun COMPLETE tasks whose post revisions
match, revive canceled/superseded attempts, apply late patches or expand scope. Broken
chain, drift, unknown outcome or collision blocks. STATUS validates read-only and never
repairs a checkpoint.

## Phase 3 — Bounded non-overlapping writers — TCB-010

Before each batch, read configured `max_threads`, enumerate every live root/child/nested
agent and calculate:

`available_child_slots = max(0, max_threads - live_threads_including_controller)`

Use `dispatch_slots = min(4, request_worker_limit, available_child_slots)`. Invalid or
unknown configuration/count runs serially. Nested delegation consumes the same slots.

Parallel eligibility requires disjoint paths, identical frozen input/interface/test
revisions, no producer/consumer edge and complete prerequisites. Gather/audit a whole batch
before dependents. Real AI/VFX/audio event dependencies wait for the interface and any
producing task; never label them independent for concurrency.

Each `cgs.combat-task-request/v2` declares stable task/attempt ID, exact manifest subset,
base revisions, deadline, cancellation token, retry budget at most one, response limit and
result schema. On timeout cancel, inspect owned paths read-only, and retry only if no
unknown/partial mutation exists, bases still match and authorization covers the attempt.
Never run overlapping attempts.

Timeout/cancelled/superseded results are `LATE_IGNORED` if they arrive later; never apply,
merge, write or use them as evidence. Any required PARTIAL/TIMED_OUT/CANCELLED/
LATE_IGNORED result prevents dependent integration and COMPLETE. Preserve verified
independent work in a partial report.

After every batch independently inventory declared targets and relevant workspace
change evidence. Verify no unowned/unapproved path changed, sole owner/base/post revisions
match and no domain owner touched a shared file. Any unauthorized/overlapping mutation
is BLOCKED and cannot be retroactively waived.

## Phase 4 — Single-owner integration

Only the approved integration owner may apply compatible proposals to shared rows after
every required upstream result is complete and audited. Recheck each base immediately
before write, apply dependency order within the frozen interface, verify cross-domain
references, re-read every target and confirm no out-of-manifest change. Conflict,
stale base or incomplete predecessor writes nothing to the affected shared path and
blocks. The orchestrator/domain writers cannot integrate as fallback.

## Functional and performance execution — TCB-007/TCB-015

After integration, build/test execution is independent from implementation writers and
binds the exact integrated manifest/post-revision set.

### Functional evidence

For every actual command, `cgs.combat-test-execution-receipt/v2` records exact command/
argv, cwd, engine/platform/version, runner/parser/tool and environment/config revisions,
start/end, exit code, pass/fail/skip/not-run counts, per-Test/AC rows, integrated post
revisions, raw log/result paths/revisions, producer identity and persistence/read-back state.
Proposed commands, inspection, transcript prose or generic CI success are NOT_RUN.

### Performance evidence

When story/QA/tech policy requires performance, consume an exact numeric platform budget
with rule/metric/unit/threshold/profile/hardware/scenario revisions. `performance-analyst`,
not qa-tester, owns capture/analysis. Require an exact `cgs.performance-request/v2`,
approved profiler/tool/adapter versions, capture command/environment, warm-up/window/
sample/repetition rules and raw export revisions. Consume the exact three-part producer
chain: canonical `cgs.performance-report/v1` payload, its matching
`cgs.review-evidence/v1` record, and a separately produced
`cgs.performance-report-recorder-receipt/v1`. re-read raw bytes independently. The
report and evidence record must agree on report/artifact revision, record/run IDs, complete
coverage and policy verdict; they must bind this current candidate, integrated build,
platform/hardware/scenario, numeric budget/rules, profiler/adapter and raw input set.

The recorder must be independent from the performance producer and implementation
writers. Its exact path and raw revision must bind the unchanged report raw revision,
evidence record ID/revision, current candidate/build/platform/budget/input identities,
persisted destination and read-back revision, with persistence proven and
`decision.evidence_persistence: RECORDED` and
`decision.gate_evidence_eligible: true`. A conversation block, report filename, producer label, copied or
renamed schema, self-recording, or receipt for different bytes cannot supply durability
or gate eligibility.

Performance passes only with complete requested cell coverage and exact policy verdict
`WITHIN BUDGET`. CONCERNS, OVER BUDGET, partial/unknown cells, missing budget, unsupported
adapter, absent capture, candidate-only evidence, mismatched build, missing/invalid
recorder receipt, non-persisted report or `gate_evidence_eligible` other than true is not proven
and prevents COMPLETE when performance is required.

## Independent evidence review — TCB-015

After execution, require the exact persisted P1 test-evidence-review report at its
ID-addressed canonical path. It must bind this story/QA plan/candidate/build/artifact/
integrated post revisions/test and performance receipt set, with `Persistence: WRITTEN` and
all closure axes simultaneously:

- `Workflow Status: COMPLETE`;
- `Structural Quality: ADEQUATE`;
- `Evidence Admissibility: ADMISSIBLE`;
- `Execution Result: PASS`;
- `Execution Currency: CURRENT`;
- `Execution Completeness: COMPLETE`;
- `Execution Scope: FULL`; and
- `Closure Eligible: YES`.

The reviewer cannot be an implementation writer or evidence producer. COMPLETE alone,
an unpersisted review, target-only scope or missing performance row is not closure.

## Deterministic completion schema — TCB-008/TCB-009

Freeze `cgs.combat-completion-record/v2` over:

- all input, architecture, interface, test-contract, engine, context, manifest,
  authorization and checkpoint identities;
- required/planned/completed/partial/blocked/timed-out/cancelled/late task counts;
- every allowed mutation owner/base/post revision and unauthorized/conflict count;
- build and functional/performance command/receipt identities and counts;
- complete AC/Test evidence matrix, independent review axes, open defect/blocker ledger,
  residual gaps and accountable owners.

Apply strict precedence:

1. invalid/stale prerequisite, absent authorization, ownership overlap, unauthorized
   mutation, integration conflict, unknown mutation outcome or untrustworthy evidence ->
   `BLOCKED`;
2. otherwise any required partial/timeout/cancel/late/skipped/unavailable task or useful
   incomplete result -> `PARTIAL_NEEDS_WORK` (`PARTIAL / NEEDS WORK`);
3. otherwise integrated implementation completed but current tests/performance have
   conclusive failures or nonblocking defects -> `NEEDS_WORK`;
4. only when every source stays current, every required task/integration completes,
   every mutation verifies, all required build/functional/performance evidence is
   current/full/passing, independent review is closure-eligible, every AC maps to PASS,
   and no blocker/unauthorized/unproven row remains -> `COMPLETE`.

Risk acceptance cannot convert missing execution, PARTIAL_NEEDS_WORK, BLOCKED or failing
evidence to COMPLETE. COMPLETE is implementation evidence only; Merge/Closure Eligible
remains NO.

## Shared integration and terminal packet

Return `cgs.team-combat-result/v2` with every identity above, exact verdict/persistence,
task/concurrency/deadline/retry ledger, mutation audit, changed paths with owners/pre/
post revisions, commands/evidence revisions, AC matrix, checkpoints, late/conflict/unauthorized
rows, remaining owners, explicit non-writes and exactly one legal next action.

Shared consumers must preserve boundaries:

- architecture-decision output is Proposed until its separate review/lifecycle owner
  records Accepted; team-combat never promotes it;
- design-review approval and persisted story-readiness READY are exact admission evidence,
  not file-write or closure authority;
- P1 QA plan is Gate Evidence NO; team-combat execution receipts may later feed Team QA,
  but local COMPLETE is not `QA_APPROVED`;
- dev-story/story lifecycle ownership remains separate; this workflow never writes Done,
  Complete or tracker closure;
- release-checklist/team-release cannot treat combat COMPLETE as release GO or deployment/
  publication authority without their exact candidate-bound evidence and gates.

Stop after the packet. Never invoke another workflow or perform the next handoff.
