# Skill Test Spec: `$team-combat`

## Purpose

Verify the complete P1 remediation set TCB-006 through TCB-015. `$team-combat` must
consume durable reviewed architecture, use independent platform-budget performance
evidence, derive completion from a complete identity-bound schema, represent useful
partial work honestly, bound every assignment and context, recover idempotently, block
implementation without an engine, and freeze tests before implementation followed by
independent evidence review.

This specification is static and fixture-driven. It does not invoke the skill, agents,
builds, tests, profilers, upstream design/architecture workflows, Team QA or release.

## Fixtures and harness rules

Positive fixtures contain exact paths, raw bytes, and explicit version/revision metadata for:

- `cgs.team-combat-request/v2` and `cgs.combat-context-manifest/v2`;
- GDD, independent P1 design review and approved target identity;
- Accepted ADR lifecycle ledger and approved `cgs.combat-tech-spec/v2` review;
- persisted story-readiness READY record and recorder receipt;
- control manifest, P1 QA plan, Test-ID ownership and engine profile/version;
- frozen combat interface and pre-implementation test contracts;
- exact file-ownership manifest, authorization and immutable checkpoints;
- writer/integrator results and mutation audits;
- functional runner, performance capture/result/recorder and evidence-review receipts.

Negative variants change exactly one fact unless stated otherwise. Every case asserts no
undeclared GDD, ADR, story/readiness, QA-plan, source, test, evidence, checkpoint,
tracker, release or external mutation. Staging documentation does not populate catalog
execution fields.

## Structural assertions

- [ ] Frontmatter contains only `name` and non-empty `description`; name is `team-combat`.
- [ ] Invocation is exactly `$team-combat --request <path> --request <revision>`.
- [ ] PREFLIGHT, EXECUTE, STATUS and RESUME are explicit operations.
- [ ] Implementation requires exact approved GDD review, Accepted ADRs, reviewed tech spec, persisted READY evidence, control/QA and engine identities.
- [ ] Proposed ADR/architecture sketch/session summary cannot authorize implementation.
- [ ] Zero mutation occurs before exact file-ownership manifest approval.
- [ ] Every path has one owner; shared paths belong only to the integration owner.
- [ ] Context is manifest-bound and capped by files, bytes, depth, interface rows, agents, response and time.
- [ ] No full/lean/solo review mode exists; roles derive from explicit dependency rows.
- [ ] Tasks have deadlines, cancellation tokens, one retry maximum and late-result quarantine.
- [ ] Checkpoints are immutable, predecessor-linked and never use shared active session state.
- [ ] Missing engine blocks EXECUTE and permits only an engine-neutral read-only gap plan.
- [ ] Test contract is frozen before implementation and cannot be edited by implementation writers.
- [ ] QA captures actual commands/results and independent review checks all closure axes.
- [ ] Performance uses exact platform budgets and the three-part `cgs.performance-report/v1` + `cgs.review-evidence/v1` + independent `cgs.performance-report-recorder-receipt/v1` chain.
- [ ] Completion record contains all identities, task/mutation/evidence counts and AC rows.
- [ ] Verdicts are COMPLETE, NEEDS_WORK, PARTIAL_NEEDS_WORK and BLOCKED with deterministic precedence.
- [ ] Local COMPLETE is not story closure, Team QA approval, release GO or deployment authority.
- [ ] Terminal output is `cgs.team-combat-result/v2` with one legal next action.

## P1 traceability

| Audit ID | Primary case |
|---|---|
| TCB-006 | Case 1 |
| TCB-007 | Case 2 |
| TCB-008 | Case 3 |
| TCB-009 | Case 4 |
| TCB-010 | Case 5 |
| TCB-011 | Case 6 |
| TCB-012 | Case 7 |
| TCB-013 | Case 8 |
| TCB-014 | Case 9 |
| TCB-015 | Case 10 |

## Case 1 — Durable ADR/tech-spec authority, not a session sketch — TCB-006

Test planned changes classified as module boundary, local interface detail and
non-architectural. Provide: Proposed ADR only; Accepted ADR without lifecycle/review;
chat architecture sketch; reviewed tech spec for another story; and complete exact
architecture package.

**Expected**

- significant choices require exact Accepted ADR decision locator, lifecycle record and
  independent architecture-review evidence;
- P1 architecture-decision authoring output remains Proposed and blocks EXECUTE;
- bounded implementation detail requires persisted `cgs.combat-tech-spec/v2` plus an
  independent exact-revision APPROVED review;
- NOT_ARCHITECTURAL needs the contract reason and governing source;
- missing authority produces stable blocker and exact upstream question, with zero
  writes and no local ADR/spec authoring or acceptance;
- only the complete package permits freezing the derived interface contract.

## Case 2 — Performance belongs to a measurement owner and budget — TCB-007

The story requires 60-fps frame budget and combat-response latency across two platform
profiles. Test: no numeric budget; qa-tester prose; proposed capture command; one missing
cell; mismatched build; CONCERNS; OVER BUDGET; and complete WITHIN BUDGET evidence.

**Expected**

- performance-analyst, not qa-tester, owns capture/analysis;
- exact `cgs.performance-request/v2` binds numeric rules, metrics/units, profiles,
  hardware, scenarios, integrated build and approved tools/adapters;
- result requires actual capture command/environment/window/sample/repetition data,
  raw revisions, canonical `cgs.performance-report/v1`, matching
  `cgs.review-evidence/v1` and independent
  `cgs.performance-report-recorder-receipt/v1`;
- all three artifacts and their raw revisions bind the current candidate/build/platform/
  budget/input/report identity; the recorder proves unchanged persisted/read-back bytes
  with `decision.evidence_persistence: RECORDED` and
  `decision.gate_evidence_eligible: true` without being the producer or an implementation writer;
- only complete requested-cell coverage with policy verdict WITHIN BUDGET passes;
- missing/invalid recorder receipt, unpersisted bytes or non-gate-eligible evidence is
  NOT PROVEN and prevents COMPLETE when performance is required;
- all other variants are NOT PROVEN and prevent COMPLETE when required;
- no inspection, static estimate, QA prose or candidate-only result becomes measurement.

## Case 3 — Deterministic completion record — TCB-008

Start from all passing inputs. Change one fact per variant: GDD revision; one timed-out task;
one unowned mutation; missing build receipt; one skipped AC; absent performance row;
nonclosure evidence review; open blocker; and fully passing graph.

**Expected**

- `cgs.combat-completion-record/v2` contains every source/architecture/interface/test/
  engine/context/manifest/authorization/checkpoint identity;
- task status counts, mutation pre/post ownership, command/receipt counts, full AC/Test
  matrix, review axes and blocker ledger are explicit;
- strict precedence selects BLOCKED, PARTIAL_NEEDS_WORK, NEEDS_WORK or COMPLETE from
  exact conditions rather than agent summaries/count heuristics;
- only the fully passing graph yields COMPLETE;
- even COMPLETE returns Merge/Closure Eligible NO.

## Case 4 — Useful partial output is PARTIAL / NEEDS WORK — TCB-009

Gameplay and audio complete on disjoint paths, VFX returns a valid partial result and AI
is unavailable. No unsafe mutation occurs and integration has not begun.

**Expected**

- verified independent gameplay/audio paths and revisions remain in the report;
- VFX/AI rows retain exact PARTIAL/unavailable state, dependencies and owners;
- dependent integration and testing do not run;
- verdict is `PARTIAL_NEEDS_WORK`, displayed `PARTIAL / NEEDS WORK`, never COMPLETE;
- partial output cannot be merged, published, used to close the story or accepted as
  release/QA evidence;
- a fully invalid prerequisite remains BLOCKED rather than partial.

## Case 5 — Timeout, retry, cancel and late-patch quarantine — TCB-010

One implementation task times out after possibly writing, another is cancelled before
dispatch, and a timed-out attempt returns later. Test safe no-mutation retry, ambiguous
mutation, changed base and two simultaneous attempts.

**Expected**

- each task has stable attempt, deadline, cancellation token and retry budget at most one;
- timeout triggers cancel and read-only path-state reconciliation;
- retry occurs only when no mutation/unknown state exists and exact bases/authority remain;
- ambiguous mutation or changed base blocks and requires revised manifest;
- simultaneous attempts for the same path are prohibited;
- canceled/superseded late result is LATE_IGNORED and never applied, merged, written or
  treated as evidence;
- every outcome enters checkpoint and partial report deterministically.

## Case 6 — Review mode is absent; staffing comes from dependencies — TCB-011

Test requests with `--review full`, `lean`, `solo`, no AI dependency, and explicit AI/
VFX/audio/performance dependencies. Make the performance owner unavailable.

**Expected**

- all review-mode inputs are rejected with zero side effects;
- gameplay and engine validation are routed by exact manifest/engine profile;
- AI, VFX, audio and performance roles appear only for explicit story/tech-spec rows;
- unavailable required role stays nonconclusive and produces PARTIAL_NEEDS_WORK or
  BLOCKED based on dependency impact;
- orchestrator cannot impersonate reviewer/test/performance owners;
- no named-agent result is fabricated.

## Case 7 — Bounded interface context, never full repository copy — TCB-012

The context manifest lists 40 files while ceilings permit 32/2 MiB/depth 2. One required
interface closure exceeds the byte budget; an undeclared similar combat controller has
newer mtime.

**Expected**

- only declared paths, first-order dependencies, interface spans and target bases load;
- whole closures are admitted deterministically; none is silently truncated;
- complete selected/loaded/missing/unreadable/invalid/omitted/unprocessed ledger and
  budget consumption are returned;
- required omission blocks EXECUTE;
- delegate receives minimal excerpts/revisions/target diff context and bounded response,
  not full source tree;
- undeclared/newer file is ignored and budget above hard ceiling is rejected.

## Case 8 — Immutable checkpoint chain and idempotent resume — TCB-013

Interrupt after test contract, one writer batch and integration. Resume exact checkpoints,
then vary predecessor, story/interface/manifest revision, completed output bytes, unknown
writer state and next-target collision.

**Expected**

- each milestone creates a new ID-addressed `cgs.combat-checkpoint/v2` with predecessor,
  all identities, assignment/writer/evidence states and one legal next action;
- no shared `production/session-state/active.md` is read or written;
- valid resume re-reads the chain and never reruns matching COMPLETE tasks;
- ambiguous outcome is reconciled before continuing and cannot be replayed;
- drift/broken chain/collision blocks without editing history;
- STATUS validates read-only and never repairs state.

## Case 9 — Missing or ambiguous engine blocks implementation — TCB-014

Test absent engine, absent pinned version, ambiguous engine profile, unsupported adapter,
and exact configured engine/version/specialist/profile.

**Expected**

- EXECUTE returns BLOCKED before ownership manifest approval or any writer when engine
  identity/routing is not exact;
- the workflow never invents engine APIs, language, paths, build/test commands or
  specialist;
- PREFLIGHT may return only `ENGINE_NEUTRAL_PLAN_ONLY / IMPLEMENTATION_BLOCKED`, with
  architecture gaps and no implementation authority/writes;
- configured valid fixture binds engine/version/profile to tech spec, interface, tasks,
  test contract and evidence;
- engine change invalidates dependent planning and authorization.

## Case 10 — Test contract before code, execution and independent review after — TCB-015

Test: no pre-implementation contract; programmer-edited test contract; proposed test
commands; current functional PASS but stale performance; unpersisted review; review
Workflow COMPLETE with TARGETED scope; and full current closure evidence.

**Expected**

- reviewed `cgs.combat-test-contract/v2` maps every AC/Test ID, fixtures, negative/
  boundary/integration/performance scope, exact commands and evidence targets before
  implementation authorization;
- implementation writers cannot edit it; authorized test sources/fixtures materialize
  before dependent code;
- actual functional receipts include command/argv, runner/tool/environment, times,
  exit/counts/per-row results, integrated revisions and declared revisions;
- performance follows Case 2 when required;
- independent persisted P1 evidence review must simultaneously be COMPLETE, ADEQUATE,
  ADMISSIBLE, PASS, CURRENT, COMPLETE execution, FULL scope and Closure Eligible YES;
- only the full current fixture can contribute to COMPLETE.

## Shared integration assertions

- [ ] P1 architecture-decision output is Proposed until a separate owner records Accepted.
- [ ] P1 design-review APPROVED and persisted story-readiness READY are admission evidence only.
- [ ] P1 QA plan Schema 2 remains Gate Evidence NO and is not execution.
- [ ] Team-combat receipts may feed Team QA, but local COMPLETE is not QA_APPROVED.
- [ ] Dev-story/story lifecycle ownership stays separate; team-combat never writes Done/Complete.
- [ ] Release-checklist/team-release require their own exact candidate gates and gain no GO/deploy/publish authority here.

## Required P0 regression matrix

Retain these prior safety properties:

1. missing approved GDD revision/review, Accepted ADR or persisted READY evidence blocks
   with zero implementation writers/writes;
2. proposal phase is mutation-free and exact ownership manifest approval precedes all
   writes;
3. every writable path has one owner, shared paths one integration owner, and overlap
   prevents concurrency;
4. interface dependencies are frozen and real producer/consumer edges are serialized;
5. unauthorized mutation fails closed and cannot be retroactively waived;
6. only integration owner writes shared files and verifies bases/post revisions;
7. actual functional execution evidence is required; proposed/narrated tests are NOT_RUN;
8. GDD/ADR/story/readiness/control/QA/release lifecycle artifacts are never rewritten;
9. spec, metadata and SKILL all describe manifest-authorized implementation side effects;
10. catalog result/timestamp fields remain blank without a real authorized execution.
