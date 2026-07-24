---
name: team-qa
description: "Orchestrate one bounded, evidence-bound QA run for an exact scope and build, with immutable checkpoints, controlled concurrency, independent review, and separate workflow-completion and QA-verdict axes."
---

# Team QA

Coordinate one QA run for one immutable scope and build candidate. Plans, selections,
chat responses, agent summaries, workflow completion, filenames and modification times
are not execution evidence. This workflow consumes independently produced evidence and
never turns QA output into release, deployment or publication authority.

## Invocation and strict request — TQA-007

Invoke only as:

`$team-qa --request <path> --expect-request <sha256>`

Require both flags exactly once. Reject unknown or duplicate fields, malformed IDs,
directories where files are required, globs, `latest`, modification-time selection,
unsafe paths, symlink escapes, unsupported schemas and request-hash drift. Stop before
project reads, delegation, output or writes on invocation failure.

The request is strict `cgs.team-qa-request/v2` and declares exactly one operation:

- `START` — validate entry authorities and propose/create the fixed run manifest,
  strategy and case set;
- `INGEST` — validate one exact external evidence receipt and propose/create one
  immutable normalized evidence record plus checkpoint;
- `FREEZE` — freeze the complete ordered evidence manifest after evidence production;
- `FINALIZE` — consume the exact frozen manifest and independent evidence review,
  then derive and optionally record one signoff;
- `STATUS` — read-only validation of one run/checkpoint chain; or
- `RESUME` — resume from one exact immutable checkpoint after revalidation.

The request declares stable scope/run/operation IDs; exact `cgs.team-qa-scope-manifest/v2`
path/hash; candidate/build, QA-plan and smoke authorities; operation-specific evidence
or review inputs; applicable root-to-target `AGENTS.md` path/hash chain; expected
predecessor checkpoint path/hash; exact proposed controller output paths; mutation
authority and expiry when recording; and fixed file, byte, story, receipt, dependency,
agent, response and elapsed-time budgets.

Never infer an active sprint, session, scope, build, QA plan, smoke result, test receipt,
checkpoint, evidence review or run. A changed scope manifest, ordered membership,
candidate/build/artifact/source/platform identity, QA plan, smoke receipt or instruction
chain requires a new run ID.

## Scope authority and bounded context — TQA-007/TQA-016

`cgs.team-qa-scope-manifest/v2` is the sole scope authority. It contains:

- stable scope ID/kind `SPRINT|FEATURE|STORY`, owner and generated time;
- for sprint scope, the exact stable sprint ID and sprint manifest path/hash;
- ordered story/requirement IDs, canonical paths, raw hashes and stable AC IDs;
- exact candidate manifest/build receipt/artifact/source and target platform,
  configuration, environment, device and locale matrix;
- exact QA-plan, test-ID ownership snapshot, evidence policy, producer registry and
  canonical evidence destinations;
- permitted exclusions with required approval contract, never informal omissions; and
- maximum files, raw bytes, story shards, receipts, dependency depth, workers, response
  bytes and elapsed time, each within workflow hard ceilings.

Normalize Unicode NFC, forward-slash project-relative paths and case-fold comparison
keys while preserving raw spellings. Reject duplicate canonical IDs/paths, conflicting
scope membership, multiple sprint candidates, date-only IDs, unsafe paths and hash
mismatches. Sort by stable story then AC/test/check ID.

Load only declared files and recursive dependencies within the budgets. Admit whole
story/requirement authority closures; never silently truncate one. Record selected,
loaded, missing, unreadable, invalid, omitted and unprocessed rows with bytes/edges and
reason. Any required omission or budget exhaustion makes the run partial and QA
incomplete. Delegates receive one bounded story shard and return only schema-conforming
rows plus bounded summaries; they do not receive the full corpus by default.

## Authority, ownership and staged mutation — TQA-008

Read-only evaluation, controller artifact CREATE, test execution, manual observation,
bug creation, evidence review, release gating, deployment and publication are separate
authorities. Approval for one never grants another.

The controller owns only absent-target immutable artifacts below the exact run root:

```text
production/qa/team-runs/{qa-run-id}/
  manifests/{run-manifest-identity-sha256}.yaml
  strategies/{strategy-identity-sha256}.md
  cases/{case-id}-{case-identity-sha256}.md
  evidence/{evidence-id}-{evidence-identity-sha256}.md
  evidence-manifests/{evidence-manifest-identity-sha256}.yaml
  checkpoints/{sequence}-{checkpoint-identity-sha256}.yaml
  signoffs/{signoff-identity-sha256}.md
```

One invocation proposes one closed changeset whose paths and exact bytes/hashes are
already knowable for that operation. `START` authority covers only the presented run
manifest, strategy, cases and phase checkpoint. It cannot pre-authorize future evidence,
bugs, signoff or dynamically discovered paths. Each `INGEST`, `FREEZE` and `FINALIZE`
operation has its own exact absent-target changeset after the relevant IDs and bytes are
known. If scope or output membership changes, stop for a new operation request and
authority; never claim an unknowable “complete future changeset.”

`qa-lead` owns risk/strategy proposals and assessment of the Phase 5 frozen evidence
manifest. `qa-tester` owns bounded case proposals and faithful transcription of supplied
evidence. The controller is the sole publisher of run artifacts. External runner,
tester, playtest, soak and review owners produce their own receipts. Team QA never writes
`production/qa/bugs/**`, release records, session state, catalog, test sources, builds,
evidence producer receipts or external state.

Before each authorized CREATE, re-hash every input and predecessor, verify target and
parent preconditions, render exact bytes, then use atomic no-replace. Flush, close,
strictly parse, read back and verify bytes/hash. Drift, collision or read-back mismatch
writes nothing further and records recovery-required state.

## Paired status model — TQA-011/TQA-012

Always report these axes together and never emit a bare `COMPLETE`:

- `Workflow State`: `WORKFLOW_NOT_STARTED`, `WORKFLOW_BLOCKED_AT_ENTRY`,
  `WORKFLOW_RUNNING`, `WORKFLOW_PARTIAL`, `WORKFLOW_COMPLETED`,
  `WORKFLOW_CANCELLED`, or `WORKFLOW_ERROR`;
- `QA Verdict`: `QA_APPROVED`, `QA_APPROVED_WITH_CONDITIONS`,
  `QA_NOT_APPROVED`, or `QA_INCOMPLETE`;
- `Gate Eligible`: `YES` only for persisted, verified `QA_APPROVED`; otherwise `NO`;
- `Run Phase`: `PHASE_1_ENTRY`, `PHASE_2_STRATEGY`, `PHASE_3_EVIDENCE`,
  `PHASE_4_FINDINGS`, `PHASE_5_FROZEN`, `PHASE_6_SIGNOFF`, or `TERMINAL`; and
- `Persistence`: `ANALYSIS_ONLY`, `VERIFIED`, `DECLINED`, `FAILED`,
  `CONFLICT`, or `NOT_ATTEMPTED`.

Also render one unambiguous paired line such as:

`Workflow Outcome: WORKFLOW COMPLETED / QA NOT APPROVED`

Workflow completion means every declared row was processed; it never means product
quality passed. A completed workflow may be QA_NOT_APPROVED or QA_INCOMPLETE. The
machine-readable values remain the underscore tokens above.

There is no generic `production/session-state` write. Run recovery state exists only in
the unique run root and every checkpoint binds run, scope, candidate/build, evidence
manifest, signoff/report hashes and the paired status vocabulary. Run IDs are stable
UUIDs/slugs, never date-only, so same-day reports cannot collide.

## Team policy and independence — TQA-015

There is no `full|lean|solo` review mode and no director-gate branch. Review labels may
not reduce evidence, change the denominator, replace a role or alter signoff semantics.

If `qa-tester` is unavailable, the controller may draft bounded cases locally, still
with `Execution State: NOT_RUN`; it cannot manufacture execution. If `qa-lead` is
unavailable, the controller may preserve a draft strategy and mechanically normalize
rows, but a policy-required qa-lead assessment remains missing and yields QA_INCOMPLETE.
The independent `test-evidence-review` receipt is never self-produced or waived by this
fallback. No local fallback may attest a run, manual observation, platform fact,
playtest, soak result or independent review.

## Delegation budget, deadlines and late results — TQA-009/TQA-014

Before every dispatch, read configured `max_threads`, enumerate all live root/child/
nested agents and compute:

`available_child_slots = max(0, max_threads - live_threads_including_controller)`

Then use `dispatch_slots = min(request_worker_limit, available_child_slots)`. If config,
live count or request limit is absent/invalid, work serially. The controller counts as
one; nested delegates consume the same budget and may not spawn without an assigned
slot. Never launch one qa-tester per story without batching.

Partition work by stable story shard. Each assignment has assignment ID, exact run/
scope/candidate/build hashes, immutable inputs, exclusive proposal path, read/write
boundary, response schema/size limit, deadline, timeout, cancellation rule and retry
budget of at most one. Gather and record a complete batch before dispatching the next.
No two writers share a target.

On timeout, error, cancellation or partial response, record assignment state
`TIMEOUT|ERROR|CANCELLED|PARTIAL`, attempt, loaded/omitted rows and owner. One retry is
permitted only before Phase 5 freeze, within the same declared inputs/output ownership,
budget and operation authority. A changed assignment requires new authority.

Once the Phase 5 checkpoint is frozen, cancel outstanding assignments. A late response
is `LATE_IGNORED`, may be hashed and listed read-only, but cannot write into, amend or
qualify the frozen run. To admit it, start a new evidence-manifest identity and run.
Timeout/partial/cancelled required work always leaves rows nonconclusive and prevents
QA_APPROVED.

## Phase 1 — Resolve entry authorities

### Candidate and build

Require strict build candidate and trusted build receipt schemas with exact candidate/
build IDs, artifact path/hash, source commit/tree, engine/toolchain/configuration,
platform/environment matrix, build command/runner/times/result/log hashes, SBOM and
provenance/signature when policy requires. Re-hash local bytes and all dependencies.

### QA plan integration

Consume only exact P1 `Artifact Type: cgs-qa-plan`, `Schema Version: 2` at
`production/qa/plans/{plan-id}.md`. Recompute currentness from its scope manifest,
Sources, requirement bindings, Test ID ownership and dependency/coverage rows. Require
`Plan State at Generation: CURRENT`, recomputed `Effective State: CURRENT`, complete
scope/coverage with no required gap, `Build Binding: BOUND` for this candidate and
`Gate Evidence: NO`. The plan is authority for required rows, not proof they ran.

### Smoke integration

Consume only the exact canonical P1 smoke root:

`production/qa/evidence/smoke/{candidate-id}/{smoke-run-id}/`

Require `cgs-smoke-check-receipt/v2`, sprint mode, exact selected-scope hash and indexed
member hashes, exact candidate/build/artifact/source/QA-plan/platform/configuration/
environment identity, current authorities, `Observed Verdict: PASS`, `Persistence:
VERIFIED`, and `Handoff Eligible: YES`. Quick/targeted success, FAIL, INCOMPLETE,
UNKNOWN, stale/partial/invalid/missing/unpersisted evidence or identity mismatch blocks.

Any missing/ambiguous scope, candidate, current plan or valid smoke handoff returns:

```text
Workflow State: WORKFLOW_BLOCKED_AT_ENTRY
QA Verdict: QA_INCOMPLETE
Gate Eligible: NO
Persistence: NOT_ATTEMPTED
```

No run root, cases, evidence, bugs or signoff may be written. Conversation may contain a
bounded draft only. A successful entry gate produces Phase 1 checkpoint 01.

## Phase 2 — Strategy and case set

From the exact plan ledger, qa-lead classifies each row by versioned rule ID into Logic,
Integration, Visual/Feel, UI, Config/Data and any multi-label combination; assigns
automation/manual/playtest/soak methods, risks and target environments. Classification
cannot change plan membership or stable Test IDs.

Each `cgs.team-qa-case/v2` binds case/story/requirement/AC/test IDs, run/scope/candidate/
build/platform, preconditions, ordered steps/expected results, evidence contract,
producer, timeout and escalation. It starts `Execution State: NOT_RUN` and `Evidence
Eligible: NO`. Case approval, qa-lead prose or chat selection cannot change it.

Persist only the exact strategy/cases authorized by START and then Phase 2 checkpoint
02. This phase designs work; it does not execute tests.

## Phase 3 — Ingest current execution evidence

INGEST validates one externally produced receipt; Team QA does not run tests or invent
observations.

### Automated and regression evidence

Require the exact `regression-selection-manifest`, `Schema Version: 2`, at
`tests/regression-suite.md` plus a separately persisted current runner receipt. A
selection is not execution. For every required row verify candidate/build/artifact/
source/plan/selection/platform/environment identity; command/argv/cwd; runner/parser/
tool versions; deterministic controls; start/end; exit code; per-test result/count;
coverage; raw logs/results paths/hashes; producer identity; completeness and persistence.

Normalize to `PASS|FAIL|NOT_RUN|STALE|INVALID|UNKNOWN`. Only an admissible, current,
complete matching receipt supplies PASS or FAIL. Zero exit alone is INVALID; missing
result is NOT_RUN; old build is STALE. Smoke proves only its selected rows.

### Manual evidence

Require `cgs.team-qa-manual-evidence/v2`: evidence/case/story/AC/test/step IDs; run/
candidate/build/artifact/source/platform/config/environment/device/OS/input; tester
identity or approved pseudonym/role; start/end; executed preconditions; actual result
for every step; result `PASS|FAIL|BLOCKED|NOT_RUN`; rationale/attestation; and required
attachment/log paths/hashes. Re-hash attachments.

A user choice, chat narrative, agent observation, missing per-step actual, device,
tester, time, attestation or attachment is INVALID/UNKNOWN, never PASS. Transcription
must preserve source bytes and provenance.

### Playtest and soak

Playtest evidence requires exact P1 `cgs.playtest-report/v2` at
`production/playtests/{session-id}/report.md` plus independent
`cgs.playtest-report-recorder-receipt/v1`; accept `RECORDED COMPLETED — GATE ELIGIBLE`
only after report/session/protocol/build/bundle/candidate/recorder and every raw hash
verify. FINALIZATION READY, COMPLETED, a candidate record or intended path alone is not
persisted gate evidence.

Soak evidence requires exact P1 `cgs-soak-result/v2` and
`cgs-soak-completion-receipt/v2` beneath its canonical run root, `Persistence Status:
VERIFIED`, exact candidate/build/profile/environment/gate-policy identity and verified
receipt/sample hashes. Evaluate Execution, Evidence, Stability, Memory, Performance,
Experience, Recovery and Readiness separately. `Handoff Eligible: YES` permits
consumption, not PASS; a required row passes only when its exact readiness/dimension
policy passes.

Every accepted or rejected receipt creates at most its separately authorized immutable
normalized record and Phase 3 checkpoint. Never edit source receipts.

## Phase 4 — Findings and collision-free bug handoff

For every current failure create a finding row with collision-resistant occurrence ID:

`TQA-OCC-{qa-run-id}-{test-or-case-id}-{short-evidence-sha256}`

Fingerprint exact scope, stable AC/test/check ID, platform and failure signature. Link
an existing bug only when its canonical stored fingerprint and occurrence mapping match.

Never scan for, reserve or increment `BUG-NNN`; never write the canonical bug registry.
Parallel testers propose findings only. After exact finding IDs/paths/hashes exist, send
unmatched occurrences to one serialized `bug-report` owner under a separate bug-write
authority. This later handoff was not part of START authorization. Until every required
failure has a verified bug receipt or approved policy disposition, QA remains
QA_NOT_APPROVED and Gate Eligible NO. Record Phase 4 checkpoint 04.

## Phase 5 — Freeze evidence manifest and checkpoint — TQA-010/TQA-013

FREEZE creates one ordered `cgs.team-qa-evidence-manifest/v2` containing:

- request/run/scope/candidate/build/artifact/source/QA-plan/smoke/instruction identities;
- every required plan row exactly once with method, owner and normalized status;
- exact receipt/report/attachment paths and hashes plus currentness/admissibility;
- declared, excluded, required, conclusive, pass, fail, blocked, not-run, stale,
  invalid, unknown, partial, timeout, cancelled and late-ignored counts;
- exclusion approval receipts, findings, occurrences, bugs/dispositions and gaps;
- assignment/batch ledger with slot arithmetic, deadlines, attempts and outcomes; and
- freeze time, input-set hash, ordered-row hash and evidence-manifest identity.

Every phase milestone 01–05 has immutable `cgs.team-qa-checkpoint/v2` with sequence,
predecessor path/hash, paired statuses, phase, input/output identities, current evidence-
manifest identity or NONE, exact agent/assignment states, pending/cancelled/late work,
budgets consumed, persistence and one legal resume action.

Phase 5 cancels outstanding work, re-hashes the predecessor chain and every evidence
dependency, then CAS-publishes the manifest and checkpoint. It never modifies earlier
artifacts. Changed evidence after freeze makes the run stale; create a new run/manifest,
not an edit.

The Phase 6 signoff input is only the exact Phase 1–5 frozen evidence manifest and
checkpoint plus the exact independent review. Do not describe its input as “Phases 4–6”
or include its own Phase 6 output.

## Resume protocol — TQA-013/TQA-014

RESUME requires exact checkpoint path/hash and expected predecessor chain. Re-hash the
request, scope, candidate/build/artifact, plan, smoke, all published run members and
external evidence named by the checkpoint. Recompute status and budget use. Validate
every target remains absent and reconcile assignment states; do not replay completed
assignments or admit LATE_IGNORED data.

Broken chain, changed candidate/scope/instruction, missing member, drifted evidence,
ambiguous assignment outcome or target collision blocks resume with exact owner/action.
Resume continues only the single legal next operation stored in the checkpoint. STATUS
does the same validation read-only and never repairs a run.

## Phase 6 — Independent review and deterministic signoff

Consume only the exact persisted P1 evidence-review path:

`production/qa/evidence/reviews/{review-id}-{scope-sha256-prefix}/report.md`

Require the request schema `cgs-test-evidence-review-manifest/v2`, report raw hash,
`Persistence: WRITTEN`, exact run/scope/candidate/build/artifact/QA-plan/evidence-
manifest/input-set identities and complete row correspondence. Closure requires all
review axes simultaneously:

- `Workflow Status: COMPLETE`;
- `Structural Quality: ADEQUATE`;
- `Evidence Admissibility: ADMISSIBLE`;
- `Execution Result: PASS`;
- `Execution Currency: CURRENT`;
- `Execution Completeness: COMPLETE`;
- `Execution Scope: FULL`; and
- `Closure Eligible: YES`.

Any other combination is non-closure evidence. COMPLETE alone is never PASS.

Apply this signoff precedence to the frozen required denominator:

| Priority | Condition | QA Verdict | Gate Eligible |
|---:|---|---|---|
| 1 | Any current required FAIL, failed required readiness dimension, or unresolved policy S1/S2 failure | QA_NOT_APPROVED | NO |
| 2 | Otherwise any required BLOCKED, NOT_RUN, UNKNOWN, STALE, INVALID, missing, PARTIAL, TIMEOUT, CANCELLED, LATE_IGNORED, missing required role assessment, or non-closure review axis | QA_INCOMPLETE | NO |
| 3 | All rows pass with only policy-approved nonblocking conditions | QA_APPROVED_WITH_CONDITIONS | NO |
| 4 | Every required row passes, all findings are dispositioned, all required role assessments exist, review is closure eligible and no condition remains | QA_APPROVED | YES after verified signoff persistence |

Failure takes precedence over incomplete evidence, but all incomplete rows remain listed.
No required row disappears from the denominator. Exclusion is valid only from an exact
current approval binding row/scope/plan/candidate/policy/approver/time/hash.

`qa-lead` may assess only the frozen Phase 1–5 manifest and cannot change rows, evidence,
counts or review axes. The controller applies the deterministic table. Create
`cgs.team-qa-signoff/v2` with every identity, denominator arithmetic, ordered result
rows, findings/bugs/dispositions, conditions, gaps, paired workflow/QA statuses,
Gate Eligible, persistence and report hash. Gate Eligible remains NO if persistence is
declined, failed, conflicted or unverified.

## QA and release integration

Return `cgs.team-qa-result/v2` with the exact signoff path/hash or NOT_WRITTEN. This is
QA evidence only:

- `$release-checklist` may normalize it only through its exact ordered evidence index
  and policy adapter into `release-evidence-checklist` Schema Version 2. That checklist
  still has `Gate Decision: NOT_EVALUATED` and Release/Deployment/Publication Authority
  NONE.
- `$team-release` may consume the exact team-QA signoff only through its declared
  `cgs.release-gate-request/v2`/`cgs.release-gate-receipt/v2` policy binding for the same
  candidate/build/artifact/source/platform. A QA_APPROVED result is not release GO and
  grants no staging, production or publication authority.
- QA_NOT_APPROVED, QA_INCOMPLETE, Gate Eligible NO, stale identity, unpersisted signoff
  or any mismatched review/checkpoint hash remains a nonpassing release-gate input.

Never invoke those workflows or update their artifacts.

## Terminal result — TQA-017

Every operation returns `cgs.team-qa-result/v2` with request/run/scope/candidate/build/
artifact/source/plan/smoke/instruction/evidence/review/signoff identities; paired
Workflow State and QA Verdict; Gate Eligible, Run Phase and Persistence; complete scope/
budget/assignment ledgers; denominator/status counts; findings and bug handoffs; all
checkpoint paths/hashes; partial/timeout/cancelled/late/stale rows and accountable
owners; explicit non-writes; and exactly one legal next operation/owner or `none`.

Do not recommend a release gate unless Gate Eligible is YES from a verified QA_APPROVED
signoff. Stop after the packet. Never continue into another operation or workflow in the
same invocation.
