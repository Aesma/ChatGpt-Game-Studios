# Skill Test Spec: $team-polish

All revisions in this specification are supplied metadata; no identity or currentness decision is derived from file content.

## Contract identity

- Spec schema: `cgs-skill-spec/v2`
- Skill path: `.agents/skills/team-polish/SKILL.md`
- Metadata path: `.agents/skills/team-polish/agents/openai.yaml`
- Target schema: `cgs.polish-target-manifest/v2`
- Context schema: `cgs.polish-context-manifest/v1`
- Assessment/mutation schemas: `cgs.polish-assessment/v2` and `cgs.polish-mutation-manifest/v2`
- Agent schemas: `cgs.polish-agent-task/v1` and `cgs.polish-agent-result/v1`
- Performance schemas: `cgs.polish-profile-request/v1` and `cgs.polish-profile-receipt/v1`
- Verification schemas: `cgs.polish-test-matrix/v1` and `cgs.polish-execution-receipt/v1`
- Recovery schema: `cgs.polish-checkpoint/v1`
- Final report schema: `cgs.polish-verification-report/v2`

## Skill summary

`$team-polish` separates bounded read-only assessment, exact path-owned
implementation, single-owner shared integration, final-candidate build, and
fixed-matrix verification. Performance analysts never patch code; every required
role, test row, context byte, attempt, checkpoint, and final receipt is
revision-bound. Only a current final build with zero release blockers and complete
passing required evidence may receive `READY FOR RELEASE`, which never grants
release authority.

## Static assertions

- [ ] TP-S001: Frontmatter contains only matching name and non-empty description
- [ ] TP-S002: Invocation exposes assess, implement, verify, and resume only
- [ ] TP-S003: No-argument and malformed invocation stop before reads, delegation, or writes
- [ ] TP-S004: Review/full/lean/solo/director-skip flags are rejected
- [ ] TP-S005: Assess never falls through to implementation
- [ ] TP-S006: Assessment, persistence, product writes, build outputs, and external actions have separate authority
- [ ] TP-S007: Assessment delegates are read-only and no product writer runs before exact authorization
- [ ] TP-S008: Mutation manifest enumerates every code/engine/scene/config/VFX/audio/tool/test/build side effect
- [ ] TP-S009: Every output path has one writer and every shared resource one sequential integrator
- [ ] TP-S010: Only canonical disjoint write domains may execute in parallel
- [ ] TP-S011: Performance analyst emits measurements/findings and never fixes code
- [ ] TP-S012: Engine programmer trigger requires trace/module/boundary/confidence evidence
- [ ] TP-S013: Tools programmer trigger is exact content/editor/import/build/automation scope
- [ ] TP-S014: Required-role matrix is policy-bound before assessment
- [ ] TP-S015: Required agent FAIL is blocking and UNKNOWN/TIMEOUT/ERROR/CANCELLED/skip is PARTIAL plus INCOMPLETE
- [ ] TP-S016: Nonblocking role skip requires pre-run NOT_APPLICABLE policy evidence
- [ ] TP-S017: Context manifest has deterministic exact entries and positive file/byte ceilings
- [ ] TP-S018: Context overflow, missing required entry, drift, or unreadable input blocks before delegation
- [ ] TP-S019: Unrestricted full context and inferred related paths are forbidden
- [ ] TP-S020: Perf-profile is not invoked as a nested workflow
- [ ] TP-S021: Direct profile request binds candidate, budget, context, hardware, command, durations, seed, timeout, and outputs
- [ ] TP-S022: Profile receipt binds termination, exit/result, metrics, traces/logs, omissions, and producer
- [ ] TP-S023: Fixed test matrix rows bind category, policy-required state, build/hardware, command, duration, seed, timeout, predicate, and owner
- [ ] TP-S024: Verify cannot add, drop, weaken, or reclassify a test row
- [ ] TP-S025: Execution receipt binds exact matrix row and final candidate/artifact revision
- [ ] TP-S026: NOT_RUN/PARTIAL/UNKNOWN/TIMEOUT/INVALID/UNAVAILABLE required rows map to INCOMPLETE
- [ ] TP-S027: Deterministic verdict order is ERROR, NEEDS MORE WORK, INCOMPLETE, then READY FOR RELEASE
- [ ] TP-S028: READY requires zero open release blockers and every required receipt current/complete/PASS
- [ ] TP-S029: Conclusive required failure takes precedence while incomplete rows stay visible
- [ ] TP-S030: Agent tasks/results bind attempt, context, deadline, timeout, cancel owner, paths, and predecessor
- [ ] TP-S031: Timeout cancels once, reconciles revisions, quarantines late output, and blocks unsafe reassignment
- [ ] TP-S032: Retry is capped at one new attempt after the original and cannot broaden scope
- [ ] TP-S033: Checkpoints are immutable create-only predecessor-linked v1 records
- [ ] TP-S034: Resume verifies the full checkpoint chain and continues only at the next incomplete idempotent step
- [ ] TP-S035: Completed patch/build steps are never replayed from conversation memory
- [ ] TP-S036: Final integrated candidate precedes all release-readiness evidence
- [ ] TP-S037: Any post-build product byte change invalidates the candidate evidence
- [ ] TP-S038: Gameplay-affecting polish requires approved design/UX and final accessibility evidence
- [ ] TP-S039: Root and nested agents share the configured concurrency cap
- [ ] TP-S040: READY always reports Release Authorization NOT GRANTED and triggers no downstream action

## Behavioral cases

### Case 1: Read-only assessment has zero product mutation

#### Fixture

A valid target v2 manifest, current baseline build, bounded context, requirements,
budgets, test matrix, and required-role policy are present.

#### Input

`$team-polish assess --manifest production/polish/combat-target.yaml --assessment-id combat-a1`

#### Expected reads

Only manifest-declared current paths and the exact role-specific context entries.

#### Expected writes

None without `--persist`; with separately authorized persistence, only exact
create-only controller assessment/proposal/checkpoint paths.

#### Expected non-writes

Product/source/assets/config/tests/builds and every unlisted path.

#### Expected behavior

Run bounded read-only assessments, return stable findings and a proposed mutation
manifest, then stop with implementation not authorized.

#### Assertions

- [ ] TP-C01-A: No implementation writer starts
- [ ] TP-C01-B: Product path revisions remain unchanged
- [ ] TP-C01-C: Persist authority does not authorize patches

#### Case Verdict

PASS when all assertions hold; otherwise FAIL.

### Case 2: Complete mutation manifest and path ownership precede writers

#### Fixture

Proposals include gameplay code, engine code, shared scene/config, shader/VFX,
audio bank/event, tools, regression fixture, build output, caches, logs, and
receipts.

#### Input

`$team-polish implement` with current assessment and mutation manifest.

#### Expected reads

Assessment, target, requirements, policy, complete canonical path inventory,
baseline revisions, and authorization state.

#### Expected writes

None until one preview lists every exact operation/output and authorization binds
those bytes and paths.

#### Expected non-writes

Any omitted class, generated output, alias, ancestor scope, or destructive target.

#### Expected behavior

Reject missing owner/base/operation/dependency/generated-output/validation/rollback
fields and any overlap not assigned to one integrator.

#### Assertions

- [ ] TP-C02-A: Every real side effect is disclosed
- [ ] TP-C02-B: Every path has one unique writer
- [ ] TP-C02-C: New scope requires reassessment and new authorization

#### Case Verdict

PASS when all assertions hold; otherwise FAIL.

### Case 3: Shared resources integrate sequentially after disjoint patches

#### Fixture

Source, VFX, and audio owners have disjoint paths; two contributors propose
fragments for one scene and one event registry.

#### Input

An authorized current mutation manifest and writer ledger.

#### Expected reads

Every patch receipt, shared-resource base revision, ordered integration plan, and
current path inventory.

#### Expected writes

Disjoint owned paths may change in bounded parallel batches; one integrator alone
writes the scene, registry, and integration receipt sequentially.

#### Expected non-writes

Contributors never write shared resources or another owner's path.

#### Expected behavior

Validate each intermediate base/result revision; conflict, drift, partial receipt, or
unexpected path blocks integration.

#### Assertions

- [ ] TP-C03-A: Shared files have exactly one writer
- [ ] TP-C03-B: Every sequential step uses the prior verified result as base
- [ ] TP-C03-C: Conflict resolution cannot change behavior without new authority

#### Case Verdict

PASS when all assertions hold; otherwise FAIL.

### Case 4: Final candidate remeasurement supersedes local patch metrics

#### Fixture

A performance patch passes locally, then VFX particles and audio streaming changes
are integrated into a new candidate.

#### Input

Verify the exact final build-candidate manifest.

#### Expected reads

Final candidate/artifact/source/patch/integration/toolchain revisions, fixed test
matrix, budgets, requirements, and final receipts.

#### Expected writes

Only matrix-declared create-only final evidence and an authorized verification
report.

#### Expected non-writes

Product bytes and baseline/per-patch receipts.

#### Expected behavior

Rerun all required profile, memory, loading, audio, QA, stress/soak, visual, and
accessibility rows on the final artifact revision.

#### Assertions

- [ ] TP-C04-A: Phase 1 and per-patch metrics cannot prove readiness
- [ ] TP-C04-B: Every final receipt names the same artifact revision
- [ ] TP-C04-C: A final budget violation yields NEEDS MORE WORK

#### Case Verdict

PASS when all assertions hold; otherwise FAIL.

### Case 5: Gameplay-affecting polish is design and accessibility gated

#### Fixture

A proposal adds screen shake, flashing feedback, and an audio-only critical cue.

#### Input

Variants with missing design approval, missing reduced-motion/flash/equivalent-cue
evidence, measured accessibility failure, and complete current approvals/evidence.

#### Expected reads

Exact design/UX/accessibility requirements, affected asset/config revisions, policy
thresholds, settings persistence, and independent final review.

#### Expected writes

Only the fully approved mutation may enter the authorized set; final review remains
read-only.

#### Expected non-writes

No requirement or approval record is authored by team-polish.

#### Expected behavior

Missing evidence is INCOMPLETE; measured failure is NEEDS MORE WORK; only the fully
passing final-build variant may continue toward readiness.

#### Assertions

- [ ] TP-C05-A: Technical-art or file approval is not design authority
- [ ] TP-C05-B: Accessibility reviewer is not the effect writer
- [ ] TP-C05-C: Functional-equivalent feedback is required

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 6: Performance analyst never becomes a code writer

#### Fixture

A profile trace identifies an allocation hotspot and proposes an engine or gameplay
source path.

#### Input

One assessment task followed by an authorized implementation task.

#### Expected reads

Analyst receives only the exact bounded capture inputs; programmer receives the
approved finding and owned path.

#### Expected writes

Analyst writes only its measurement receipt; the manifest-named programmer writes
the patch and patch receipt.

#### Expected non-writes

Analyst never edits source, config, assets, tests, or shared resources.

#### Expected behavior

A prompt or receipt assigning source edits to performance-analyst is a structural
failure and blocks integration.

#### Assertions

- [ ] TP-C06-A: Measurement owner and mutation owner are distinct
- [ ] TP-C06-B: Finding records trace/module/confidence and proposed owner
- [ ] TP-C06-C: Analyst cannot self-approve a patch

#### Case Verdict

PASS when all assertions hold; otherwise FAIL.

### Case 7: Fixed test matrix is immutable during verify

#### Fixture

The captured matrix contains stable required CPU, GPU, memory, loading, audio,
regression, stress, soak, minimum-spec, visual, and accessibility rows.

#### Input

Variants remove soak, weaken duration, change hardware, alter pass predicate, add
an ad hoc substitute, and preserve the exact matrix.

#### Expected reads

Matrix path/revision, policy classifications, candidate manifest, environments, and
declared commands.

#### Expected writes

Only exact matrix-declared receipt paths for the unchanged variant.

#### Expected non-writes

Matrix, policy, candidate, and substituted evidence paths remain unchanged.

#### Expected behavior

Every changed/dropped/weakened/reclassified variant blocks; only exact matrix
execution continues.

#### Assertions

- [ ] TP-C07-A: Row IDs and policy-required state are stable
- [ ] TP-C07-B: Command/duration/seed/hardware/predicate are immutable
- [ ] TP-C07-C: Verify cannot choose easier evidence

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 8: Execution receipt distinguishes PASS from unrun and partial states

#### Fixture

Exercise valid PASS, NOT_RUN hardware, TIMEOUT, truncated log, missing exit,
wrong build revision, wrong seed, inadequate duration, and raw-log mismatch variants.

#### Input

One final-candidate matrix row and one receipt variant per run.

#### Expected reads

Candidate/artifact bytes, matrix row, environment/hardware identity, raw trace/log,
budget rule, and receipt.

#### Expected writes

None from validation; invalid receipts are not repaired.

#### Expected non-writes

No receipt or log is rewritten to PASS.

#### Expected behavior

Only the exact complete current PASS receipt satisfies the row; all nonconclusive
required states map to INCOMPLETE and a conclusive failure maps to NEEDS MORE WORK.

#### Assertions

- [ ] TP-C08-A: Build/revision/command/runtime/result axes are checked separately
- [ ] TP-C08-B: Filename, checkbox, or conversation cannot fill a field
- [ ] TP-C08-C: Required hardware absence never becomes PASS

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 9: Readiness verdict follows one deterministic order

#### Fixture

Run invalid manifest, conclusive current regression, incomplete required evidence,
and fully current passing zero-blocker variants.

#### Input

One exact verification evidence set per variant.

#### Expected reads

Candidate, policy, blocker registry, complete fixed matrix, all receipts, and
evidence snapshot.

#### Expected writes

None unless separately authorized report persistence follows computation.

#### Expected non-writes

Evidence and blocker severity are never rewritten by risk preference.

#### Expected behavior

Return ERROR, NEEDS MORE WORK, INCOMPLETE, and READY FOR RELEASE respectively;
list all incomplete rows even when a conclusive failure takes precedence.

#### Assertions

- [ ] TP-C09-A: Zero open release blockers is mandatory for READY
- [ ] TP-C09-B: Every required receipt must be current complete and passing
- [ ] TP-C09-C: Every outcome reports Release Authorization NOT GRANTED

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 10: Required agent skip and partial terminals cannot be READY

#### Fixture

Policy marks QA and performance roles REQUIRED. Exercise skip, UNKNOWN, TIMEOUT,
ERROR, CANCELLED, and FAIL results; separately mark a tools row NOT_APPLICABLE with
current policy proof.

#### Input

Role matrix, policy, agent tasks/results, and otherwise passing evidence.

#### Expected reads

Required-role classifications, rule IDs, agent receipts, context revisions, and
affected scope.

#### Expected writes

None.

#### Expected non-writes

Role policy and results are not normalized by the controller.

#### Expected behavior

FAIL is a conclusive blocker. Other required non-PASS states produce workflow
PARTIAL and verdict INCOMPLETE. The proven NOT_APPLICABLE tools row is nonblocking.

#### Assertions

- [ ] TP-C10-A: Required skip is visible and non-ready
- [ ] TP-C10-B: Optionality exists before dispatch
- [ ] TP-C10-C: Conversation cannot reclassify a required role

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 11: Timeout, cancellation, late output, and retry are bounded

#### Fixture

A shader writer times out, cancellation is requested, and a late patch changes one
owned path. Exercise confirmed termination and cancellation-failure variants.

#### Input

Agent task/result records, deadline, one-retry policy, checkpoint, and path revisions.

#### Expected reads

Task/attempt/context/predecessor identities, live-agent state, owned/shared
preimages, late-output revisions, and retry budget.

#### Expected writes

Only exact controller checkpoint/quarantine evidence paths; no integration write.

#### Expected non-writes

No reassignment, merge, silent revert, broader retry, or second retry.

#### Expected behavior

Mark TIMEOUT, stop dependents, reconcile all paths, exclude late bytes from
integration, and permit one new attempt only after proven termination and stable base.

#### Assertions

- [ ] TP-C11-A: Late patch is never accepted into the candidate
- [ ] TP-C11-B: Cancellation failure remains BLOCKED
- [ ] TP-C11-C: Retry keeps the approved scope and gets a new attempt ID

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 12: Actual role matrix replaces review-mode templates

#### Fixture

A visual/audio/tools target requires technical-art, sound, tools, QA, and
accessibility rows. No director row exists.

#### Input

Variants pass full, lean, solo, review-skip, and the valid explicit assess command.

#### Expected reads

Only the valid command reads target policy and required-role matrix.

#### Expected writes

None during command validation and read-only assessment.

#### Expected non-writes

No director/lead placeholder receipt or mode-derived skip record.

#### Expected behavior

Reject template review flags. Dispatch the real required rows from policy; each
required row must return current PASS evidence.

#### Assertions

- [ ] TP-C12-A: Presentation mode cannot alter team composition
- [ ] TP-C12-B: No ceremonial director gate exists
- [ ] TP-C12-C: Required roles derive from exact scope triggers

#### Case Verdict

PASS when all assertions hold; otherwise FAIL.

### Case 13: Tools and engine roles have evidence-based triggers

#### Fixture

Exercise editor/import automation, no tools scope, trace-backed engine boundary
above confidence threshold, and vague probably-engine variants.

#### Input

Target/context/policy records and performance finding evidence.

#### Expected reads

Only exact trigger sources and role-specific context.

#### Expected writes

Assessment receipts only; patches require later exact mutation authority.

#### Expected non-writes

No tools or engine patch during assessment.

#### Expected behavior

Tools role runs only for declared tools scope. Engine diagnosis runs only for the
trace/module/boundary/confidence variant; vague claims remain UNKNOWN.

#### Assertions

- [ ] TP-C13-A: Tools programmer is neither dead metadata nor unconditional
- [ ] TP-C13-B: Engine classification has an objective evidence threshold
- [ ] TP-C13-C: Conditional trigger absence is recorded, not guessed

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 14: Context manifest enforces deterministic hard ceilings

#### Fixture

Variants include valid bounded context, missing required entry, revision drift,
unreadable file, file-count overflow, byte overflow, and an agent request for the
whole repository.

#### Input

One context v1 manifest and target policy per variant.

#### Expected reads

Manifest metadata and sizes first; bodies only for valid ordered entries within all
ceilings.

#### Expected writes

None.

#### Expected non-writes

No generated summary, expanded manifest, or hidden cache becomes authority.

#### Expected behavior

Only valid bounded context dispatches. Every other variant blocks before delegation
with exact consumed/required limits and offending entry.

#### Assertions

- [ ] TP-C14-A: Context order and identifier are reproducible
- [ ] TP-C14-B: Overflow never silently truncates required evidence
- [ ] TP-C14-C: Full context and inferred paths are forbidden

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 15: Immutable checkpoints make resume idempotent

#### Fixture

Interrupt after shared integration and before build. Variants include valid chain,
forked predecessor, changed path revision, altered authorization, duplicate completed
step, missing terminal result, and active stale writer.

#### Input

`$team-polish resume --checkpoint production/polish/combat/implementations/run-1/checkpoints/integrated.md`

#### Expected reads

Full predecessor chain, schemas/revisions, manifests, authorization, ledger, agent
results, receipts, context/test matrix, path inventory, retry budget, and next step.

#### Expected writes

Only the next incomplete authorized step and its new create-only checkpoint.

#### Expected non-writes

Completed patches/integration are never replayed; invalid variants write nothing.

#### Expected behavior

Valid chain resumes at build. Every drift/fork/collision/active-writer variant
blocks with one exact recovery requirement.

#### Assertions

- [ ] TP-C15-A: Checkpoint IDs and predecessors are unique
- [ ] TP-C15-B: Resume does not depend on conversation memory
- [ ] TP-C15-C: Idempotence covers patch, integration, build, and verification steps

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 16: Performance capture uses a direct explicit interface

#### Fixture

Exercise valid direct profile request/receipt, unsupported runner, missing hardware,
timeout, mismatched command, mismatched candidate, and a request to invoke
`$perf-profile` implicitly.

#### Input

Assessment profile request and exact target/budget/context records.

#### Expected reads

Request-declared candidate/artifact, budget, context, hardware, tool, command, and
raw receipt evidence only.

#### Expected writes

Only the request-declared immutable profile receipt/log/trace outputs when execution
is supported and authorized.

#### Expected non-writes

No nested workflow invocation, inferred artifact path, or prose-only substitute.

#### Expected behavior

Accept only the current matching receipt; record unsupported/missing/timeout as
NOT_RUN or INVALID and keep readiness non-ready.

#### Assertions

- [ ] TP-C16-A: Nested perf-profile behavior is not assumed
- [ ] TP-C16-B: Request and receipt schemas define the entire compatibility boundary
- [ ] TP-C16-C: Failure state maps deterministically to incomplete evidence

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 17: Post-build byte change invalidates every final receipt

#### Fixture

A complete final candidate and passing matrix exist, then one audio bank byte
changes after build.

#### Input

Verify using the old candidate and receipts.

#### Expected reads

Current artifact/source/asset/config bytes and every captured revision.

#### Expected writes

None.

#### Expected non-writes

No receipt, candidate manifest, or report is refreshed in place.

#### Expected behavior

Mark the candidate and dependent evidence stale; require a new candidate and full
matrix rerun.

#### Assertions

- [ ] TP-C17-A: Timestamp recency cannot hide byte drift
- [ ] TP-C17-B: Local unaffected tests cannot preserve READY
- [ ] TP-C17-C: Old report remains immutable history

#### Case Verdict

PASS when stale evidence blocks; otherwise FAIL.

### Case 18: Hidden or owner-violating write blocks integration

#### Fixture

A technical artist changes an unlisted render setting or another owner's path.

#### Input

Current writer ledger, mutation manifest, patch receipt, and reconciled inventory.

#### Expected reads

All declared and observed path revisions, canonical aliases, owner IDs, and generated
outputs.

#### Expected writes

Only an immutable failure/checkpoint record in exact controller paths.

#### Expected non-writes

No silent absorption, revert, integration, candidate build, or READY report.

#### Expected behavior

Record the unexpected write and owner violation, stop dependents, and return a
non-ready state with recovery boundary.

#### Assertions

- [ ] TP-C18-A: Manifest-outside writes are visible
- [ ] TP-C18-B: Controller never silently repairs another writer's output
- [ ] TP-C18-C: Dirty state cannot become a candidate

#### Case Verdict

PASS when all assertions hold; otherwise FAIL.

### Case 19: Bounded concurrency counts root and nested agents

#### Fixture

`.codex/config.toml` sets max_threads six; root plus two unrelated agents are
live; five independent assessment rows are ready.

#### Input

One valid assess invocation.

#### Expected reads

Exact config and live-agent inventory before each batch.

#### Expected writes

Only role-declared assessment outputs when persistence is separately authorized.

#### Expected non-writes

No extra task is dispatched beyond available slots.

#### Expected behavior

Dispatch at most three children, count nested delegation against the same cap, gather
the batch, then release slots. Invalid config falls back to serial.

#### Assertions

- [ ] TP-C19-A: Root counts as one live thread
- [ ] TP-C19-B: Nested agents cannot bypass the cap
- [ ] TP-C19-C: Dependent work waits for predecessor receipts

#### Case Verdict

PASS when concurrency never exceeds the calculation; otherwise FAIL.

### Case 20: Report persistence and release boundary stay separate

#### Fixture

A final candidate satisfies every required row and has zero open release blockers.
Variant A declines persistence; Variant B authorizes one exact absent report path.

#### Input

Verify with `--persist` only in Variant B.

#### Expected reads

Every final input is revalidate immediately before report creation.

#### Expected writes

A creates none. B atomically creates and verifies exactly one v2 report at the
previewed path.

#### Expected non-writes

No commit, tag, push, release object, deployment, upload, store submission, message,
stage update, scheduling action, or downstream workflow.

#### Expected behavior

Both conversational outcomes say READY FOR RELEASE and Release Authorization NOT
GRANTED; only B yields a consumable persisted report/revision.

#### Assertions

- [ ] TP-C20-A: Readiness is evidence, not release authority
- [ ] TP-C20-B: Declined/failed persistence creates no consumable report
- [ ] TP-C20-C: Downstream consumers must revalidate and obtain separate authority

#### Case Verdict

PASS when all assertions hold; otherwise FAIL.

## Protocol compliance

- [ ] TP-P001: Resolve one explicit mode and exact manifest/checkpoint path
- [ ] TP-P002: Read only revision-bound context within deterministic ceilings
- [ ] TP-P003: Keep assessment roles read-only
- [ ] TP-P004: Preview one complete mutation set before product writers
- [ ] TP-P005: Assign one writer per path and one integrator per shared resource
- [ ] TP-P006: Keep analyst, programmer, integrator, build owner, QA, and accessibility ownership distinct
- [ ] TP-P007: Bind every agent attempt to task/result/deadline/context/checkpoint records
- [ ] TP-P008: Cancel and reconcile before one bounded retry
- [ ] TP-P009: Resume only from a verified immutable checkpoint chain
- [ ] TP-P010: Build one final candidate after integration
- [ ] TP-P011: Execute the unchanged fixed matrix on that exact candidate
- [ ] TP-P012: Preserve every failure, omission, unavailable, timeout, and not-run row
- [ ] TP-P013: Compute the deterministic verdict without conversational override
- [ ] TP-P014: Persist only exact create-only controller outputs after authorization
- [ ] TP-P015: Never invoke perf-profile or another downstream workflow automatically
- [ ] TP-P016: Never grant release, commit, push, publish, deploy, message, or schedule authority

## Verdict matrix

| Highest-priority condition | Workflow Status | Readiness Verdict |
|---|---|---|
| Invalid candidate/manifest/policy/internal processing | ERROR | ERROR |
| Current conclusive budget/test/blocker/design/accessibility/unexpected-write failure | COMPLETE or PARTIAL as evidenced | NEEDS MORE WORK |
| Required missing/not-run/partial/unknown/timeout/stale/invalid/unavailable evidence or agent row | PARTIAL or BLOCKED as evidenced | INCOMPLETE |
| Zero blockers and all required current complete passing receipts | COMPLETE | READY FOR RELEASE |

Every row returns `Release Authorization: NOT GRANTED`.

## Audit remediation traceability

| Audit ID | Contract closure |
|---|---|
| TPL-001 | TP-S008–TP-S010 and Cases 2–3 enforce path ownership/shared integration |
| TPL-002 | TP-S036–TP-S037 and Cases 4/17 bind evidence to the final candidate |
| TPL-003 | TP-S006–TP-S009 and Case 2 disclose every mutation/output class |
| TPL-004 | TP-S005–TP-S007 and Case 1 keep assessment read-only before authorization |
| TPL-005 | TP-S038 and Case 5 enforce design and accessibility authority |
| TPL-006 | TP-S011 and Case 6 separate performance analyst from code writer |
| TPL-007 | TP-S023–TP-S026 and Cases 7–8 define fixed test and execution evidence |
| TPL-008 | TP-S027–TP-S029 and Case 9 define deterministic readiness |
| TPL-009 | TP-S014–TP-S016 and Case 10 map required agent partial/skip states |
| TPL-010 | TP-S030–TP-S032 and Case 11 define timeout/cancel/late/retry handling |
| TPL-011 | TP-S004/TP-S014 and Case 12 replace inert review modes with real role policy |
| TPL-012 | TP-S013 and Case 13 define tools-programmer trigger/output |
| TPL-013 | TP-S017–TP-S019 and Case 14 define bounded context authority |
| TPL-014 | TP-S033–TP-S035 and Case 15 define checkpoint/resume/idempotence |
| TPL-015 | TP-S020–TP-S022 and Case 16 define direct performance interface and failure mapping |

## Validation boundary and shared integration note

This is a static contract specification. It validates exact text, schemas, state
mappings, role triggers, and non-write boundaries; it does not execute profiling,
builds, soak/stress tests, agent cancellation, filesystem rollback, or checkpoint
resume. Runtime conformance requires schema-valid fixtures, final-candidate revision
checks, timeout/late-write injection, context-budget overflow tests, and checkpoint
fork/replay tests.

The staged candidate names shared records that other skills or runners may produce,
but it does not modify their live schemas or catalog entries. Integration must align
producer schema/version, canonical path, identity, and declared revisions before this
consumer can accept them; otherwise team-polish fails closed as INCOMPLETE or
BLOCKED.
