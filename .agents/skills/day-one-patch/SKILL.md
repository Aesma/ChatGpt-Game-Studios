---
name: day-one-patch
description: "Plan and evidence-gate one bounded day-one patch without implementing fixes, reusing stale release approval, treating unresolved S1 or partial QA as PASS, or authorizing deployment, submission, notification, or publication."
---

# Day-One Patch

This workflow has two responsibilities: create one immutable bounded patch-plan bundle,
and normalize independently produced evidence for one exact new patch candidate. It
does not implement, build, test, verify/close bugs, deploy, submit, publish or notify.

## Invocation and strict request

Invoke only as:

`$day-one-patch --request <path> --request-revision <revision>`

Require both flags exactly once. With missing/invalid flags or unknown arguments, show
that usage and stop before project reads, output, delegation, or writes. Reject
directories, globs, traversal, moving aliases, symlink/junction/reparse escape, unsafe
IDs, unsupported schemas, duplicate/unknown fields and expected/actual request drift.

The request is strict `cgs.day-one-patch-request/v2` and declares mode `PLAN`, `GATE`,
or `RESUME`, stable release/patch/run ID, and operation `analyze-only` or
`record-controller-artifact`.

Every mode declares project root/identity, exact root-to-output `AGENTS.md` path/revision
chain, release/patch policy and owner-registry paths/revisions, hard budgets, output root,
trusted time/cutoff receipt and non-writes. Additionally:

- PLAN names the exact gold-master build/release manifests and artifact revision,
  canonical ordered bug/cert index, target platform matrix and plan ID;
- GATE names one immutable approved v2 plan bundle, exact new build candidate/artifact,
  one `cgs.day-one-patch-evidence-manifest/v2`, new release-candidate manifest, fresh
  release checklist and gate ID; and
- RESUME names one exact immutable checkpoint path/revision and expected predecessor chain.

Validate release/patch/plan/gate/checkpoint IDs before path use. Normalize literal and
real paths under project root. Never infer latest/current build, release gate,
checklist, bug folder, cert feedback, test run, receipt, candidate, platform, owner,
deployment window or previous report. Read only declared inventory; do not scan source,
CI/log/test/bug/release directories or external systems.

## Single responsibility and authority — DOP-004

Keep these authorities independent:

1. planning/evidence normalization — read-only;
2. controller artifact recording — one exact absent plan/gate/checkpoint target;
3. implementation mutation — owned by separately authorized path owners;
4. build/QA/rehearsal execution — owned by separately authorized producers;
5. deployment/platform submission — owned by an independent human launch/deployment
   gate with exact candidate/action/account/environment/time/idempotency authority; and
6. publication/notification — separate human authority for exact channel/account/
   message reference ID/time/idempotency action.

Plan/scope approval authorizes only implementation handoff, never implementation.
Agent/QA-lead/producer/release-manager recommendations, role labels, checkboxes, a
recorded plan, `DAY-ONE PATCH READY` or an old gate never authorize a later layer.

Always return:

- `Implementation Authorization: NOT_GRANTED`;
- `Deployment Decision: NOT_RECORDED`;
- `Deployment Authorization: NOT_GRANTED`;
- `Platform Submission Authorization: NOT_GRANTED`;
- `Publication Authorization: NOT_GRANTED`; and
- `Notification Authorization: NOT_GRANTED`.

Never invoke an implementer, smoke-check, release-checklist, gate-check, team-release,
patch-notes, bug-report, deployment, platform, communication or other workflow.

## Hard bounds and one implementation round — DOP-005

The request/policy may lower but never raise:

| Resource | Hard ceiling |
|---|---:|
| indexed issue/cert candidates | 24 |
| included patch items | 12 |
| implementation rounds | 1 |
| changed files total | 64 |
| changed files per item | 16 |
| changed text lines total | 2,500 |
| changed binary/asset bytes | 64 MiB |
| target platform/configuration rows | 8 |
| evidence/dependency files | 2,048 |
| evidence bytes total | 128 MiB |
| planning/evaluation elapsed | 20 minutes |

Each item also has a lower explicit effort/dependency/diff/generated-output budget.
Stop before any ceiling; do not start a per-bug loop or split into hidden rounds.
Deterministically rank using the frozen patch policy, record all excluded/deferred IDs,
owners and reasons, and return REPLAN REQUIRED/BLOCKED when a required issue cannot fit.
Limit/timeout/unreadable/omitted evidence returns INCOMPLETE with exact counters, revisions,
reason and identity-bound resume cursor; no partial set can become ready.

## Canonical identities and states

Strictly parse schema, stable IDs, canonical paths, and explicit revisions before
normalization. Canonical serialization is UTF-8/LF/NFC with schema field order,
sorted sets, and stable ID order.

```text
base_candidate_id = declared release candidate/build ID
patch_item_id = DOPI-{patch-id}-{source-issue-id}
plan_id = DOPPLAN-{patch-id}-{utc-run-id}
new_candidate_id = declared new candidate/build ID
evidence_snapshot_id = DOPEV-{patch-id}-{utc-run-id}
gate_id = DOPGATE-{patch-id}-{utc-run-id}
```

Stable finding ID is `DOPF-{patch-id}-{item-or-document-id}-{rule-id}`. Normalize
and collision-check every ID. Do not recycle IDs across changed scope; retain
explicit supersedes lineage.

Use independent fields:

| Field | Values |
|---|---|
| Workflow Status | `PLANNED`, `EVALUATED`, `PARTIAL`, `BLOCKED`, `ERROR` |
| Plan Verdict | `READY_FOR_IMPLEMENTATION_HANDOFF`, `REPLAN_REQUIRED`, `NO_PATCH`, `INCOMPLETE`, `BLOCKED` |
| Evidence State | `CURRENT`, `STALE`, `MISSING`, `PARTIAL`, `UNKNOWN`, `INVALID`, `NOT_RUN`, `TIMEOUT`, `UNAVAILABLE` |
| Patch Gate Verdict | `DAY_ONE_PATCH_READY`, `NEEDS_REPLAN`, `INCOMPLETE`, `BLOCKED`, `ERROR`, `PROCEED_WITH_ACCEPTED_S1_RISK_NOT_QA_PASS` |
| S1 Disposition | `NONE`, `HARD_BLOCK`, `HUMAN_ACCEPTED_PLATFORM_ALLOWED` |
| Recorder Status | `ANALYSIS_ONLY`, `CREATED`, `FAILED`, `RECOVERY_REQUIRED` |

Old-build PASS, stale/partial/unknown/not-run/timeout/unavailable/unpersisted or wrong-
candidate evidence never satisfies the new gate.

## Phase 1 — Validate base release and canonical issue state

Read/revisions request, instructions, gold-master build/release manifests and artifact,
patch/release policies, owner registry, target matrix and exact bug/cert evidence index.
Read in full the declared root-to-output AGENTS chain, verify order/revisions and apply
closest-file precedence. Drift, unsafe paths, missing budgets or ambiguous identity is
BLOCKED with zero writes.

Only declared canonical `production/qa/bugs/<BUG-ID>.md` records are lifecycle
authority. Require schema/version, filename/body stable ID, canonical severity/status,
transition history and declared revision. Do not infer lifecycle/severity from filenames,
triage output or prose.

`Open` is unresolved. `Fixed Pending Verification` is not verified. `Verified Fixed`
requires a target-build reproduction PASS and a failure-sensitive automated regression
PASS for the exact fix/candidate/platform. `Closed` additionally requires an authorized
QA transition. Static/source/diff/manual-only/smoke evidence is at most
`FIX_PRESENT_RUNTIME_UNVERIFIED`. This workflow never changes a bug record.

Any changed patch candidate makes gold-master release/smoke/cert/sign-off/build-bound
PASS stale and comparison-only.

## Phase 2 — Select bounded items and freeze mutation ownership — DOP-005/007

An item is eligible only when it fixes an existing defect or mandatory certification
issue, not a feature/refactor/cleanup/architecture change/speculative optimization;
fits every total/item budget and the single round; and has exact evidence, risk,
acceptance, tests, rollback and owner scope.

Each `cgs.day-one-patch-item/v2` contains:

- stable item/source bug-or-cert IDs and declared revision, severity/status and requirement;
- immutable owner ID/role/registry revision and implementation-receipt producer;
- exact allowed path literals/roots, expected generated paths and explicit prohibited
  paths/categories; symlink/rename/generated-output rules;
- maximum files, lines, binary bytes, effort, dependencies and round exactly 1;
- minimum behavior/acceptance without unapproved design expansion;
- save/data/schema/network/security/privacy/platform impact and risk class;
- reproduction case, failure-sensitive regression test and exact stable QA check IDs;
- required new candidate/build/diff/implementation/QA/release evidence outputs; and
- rollback, monitoring, deferred-work and supersedes lineage.

The downstream mutation manifest must be a subset of owner/paths/budgets. Authorization
for one item/path never covers another. Unknown owner/scope or required item outside
budget yields REPLAN REQUIRED/BLOCKED, not silent transfer to the main agent. The plan
does not invoke or simulate implementation.

### S1 hard block

Unresolved S1 is a default hard block and highest-priority emergency planning item. If
it cannot fit, Plan Verdict is BLOCKED. At gate it must be Verified Fixed/Closed with
new-candidate evidence for DAY_ONE_PATCH_READY.

The only non-passing exception requires both exact platform/release-policy permission
and independent human `cgs.day-one-s1-risk-acceptance/v2`, bound to bug/release/new
candidate/platform, authority identity/signature, explicit decision, impact,
compensating controls, monitoring/rollback/communication, issued/expiry and revisions.
This workflow never creates/solicits it. Even when valid the verdict is only
PROCEED_WITH_ACCEPTED_S1_RISK_NOT_QA_PASS; the bug stays Open. Without both: BLOCKED.

## Phase 3 — Build one immutable v2 plan bundle — DOP-010

Create `cgs.day-one-patch-plan/v2` containing request/base/policy/owner/instruction
identities, ordered included/deferred v2 items, findings, scope-decision placeholder,
one implementation round, full budgets and these nested artifacts:

1. `cgs.day-one-rollback-plan/v2` per Phase 4;
2. quick and sprint `cgs.day-one-smoke-request/v2` handoffs per Phase 5;
3. `cgs.day-one-patch-evidence-manifest/v2` template listing every required producer,
   artifact type/schema/path/revision placeholder, candidate binding and deadline; and
4. `cgs.day-one-deployment-observation-plan/v1` proposal with no authority.

Every claim/finding/item links stable IDs and immutable source revision. Free-text
commit/tag/build slots are not evidence. The bundle records `plan_id`,
exact non-writes and downstream contract versions.

No issues may yield NO_PATCH only after the complete indexed issue/cert sources load;
an empty/unreadable directory is not evidence. A partial/timeout/unavailable plan is
INCOMPLETE and not handoff-ready. A human scope decision may approve/adjust/decline the
bundle, but `READY_FOR_IMPLEMENTATION_HANDOFF` still leaves Implementation
Authorization NOT_GRANTED.

## Phase 4 — Executable rollback and rehearsal contract — DOP-006

`cgs.day-one-rollback-plan/v2` declares per platform/configuration:

- exact base artifact and new-candidate placeholder/identity requirements;
- rollback/revoke/forward-recovery method, executable command/argv, tool/version,
  permissions, idempotency key and ordered step IDs;
- save/data/schema compatibility in both directions, migration reversibility,
  backup/checkpoint/restore revisions and irreversible-operation handling;
- operator, independent verifier, timeout, policy/risk-derived RTO/RPO/hotfix target;
- production-equivalent rehearsal environment/workload/duration, expected observables,
  log/receipt outputs and numeric PASS/FAIL rules; and
- crash/error/data-loss/funnel thresholds, sample/window/cadence, automatic/manual stop
  point, kill switch owner and safe terminal state.

No-rollback platforms require current policy-authorized equivalent containment and
verification. “Revert the commit,” a plan/runbook/role name or untested prose is not
gate evidence.

Gate requires `cgs.day-one-recovery-rehearsal/v2` binding plan, base/new artifacts,
platform/environment/data/schema, operator/verifier, exact commands/steps, permissions,
start/end, backups/restore/integrity, measured RTO/RPO, thresholds, logs/artifacts and
verdict. Failed/exceeded/incompatible rehearsal is conclusive BLOCKED/NEEDS_REPLAN;
missing/stale/partial/wrong-build/wrong-environment is INCOMPLETE. A report revision alone
never proves rehearsal.

## Phase 5 — Versioned QA/smoke handoffs, never inline execution — DOP-008/009

This workflow never delegates or runs QA. The plan emits immutable request records for
separately authorized producers. Each request has producer/owner, deadline/timeout,
candidate/build/artifact/source/platform, QA plan/test manifest, exact tests/check IDs,
scope/budget, command policy, output artifact type/schema/path and required raw/log/
receipt revision. Timeout/cancel/error becomes TIMEOUT/NOT_RUN/UNAVAILABLE at gate, never
skip/pass. No late receipt may mutate a frozen/persisted gate report.

Each `cgs.day-one-smoke-request/v2` contains:

- request/plan/item IDs/revisions and expected response schema/version;
- mode `QUICK_TARGETED` or `SPRINT_FULL`;
- exact new build-candidate manifest/candidate/build/artifact/source/platform identity;
- exact QA-plan/test-manifest paths/revisions and ordered stable QA check IDs;
- canonical scope serialization/revision, exclusions, timeout and output report path; and
- expected verdict, completeness, persistence and handoff semantics.

Never pass free-form affected-system names. Quick request uses only the union of
ordered stable item check IDs. Its verified response is targeted evidence and must
remain Handoff Eligible NO. SPRINT_FULL is a distinct request/receipt for complete
candidate coverage and eligible handoff. Quick success alone is INCOMPLETE.

At gate accept only exact persisted supported `smoke-check-receipt` schema pinned by
the plan/QA policy. Revalidate candidate/QA/test/scope/automation/manual/log dependencies.
FAIL takes precedence. Partial, warning, stale, timeout, wrong-build, unpersisted or
mismatched receipt cannot pass.

## Phase 6 — Validate new candidate, actual diff, and v2 evidence manifest

GATE requires an approved immutable v2 plan, exact independently produced build
candidate/artifact and `cgs.day-one-patch-evidence-manifest/v2`. Validate new candidate/
build/artifact/source/toolchain/platform/QA/test identities and trusted build receipt.

The evidence manifest binds plan/base/new identities, new release manifest/policy,
ordered v2 items, implementation and diff receipts, actual changed paths/revisions, owner,
commands/times/results/omissions, canonical bug states, reproduction/regression,
quick/full smoke, risk evidence, fresh release checklist, rollback rehearsal, platform
receipts and observation/deployment handoff definitions.

Revalidate every input/dependency. Actual diff must be a subset of each allowed path and
all item/total budgets; prohibited/extra path, owner violation, new item/feature/refactor,
generated output drift or round >1 yields NEEDS_REPLAN. This workflow does not absorb,
edit, repair or revert it.

Every included bug must be Verified Fixed/Closed with exact new-candidate reproduction
PASS and failure-sensitive automated regression PASS (except separately reported S1
exception). Manual/smoke/static evidence cannot replace regression. Preserve lifecycle;
never close a bug.

## Phase 7 — Consume fresh release normalization and re-evaluate policy

Consume only a persisted `Artifact Type: release-evidence-checklist`, `Schema Version:
2` for the exact new release/candidate/build/artifact/source/platform. Require its
full candidate/checklist identity path, exact report revision, release-policy/instruction/
evidence identities, ordered row revisions, recorder CREATED, and `Gate Decision:
NOT_EVALUATED` with Release/Deployment/Publication Authority NONE.

Revalidate every referenced dependency and independently apply the release policy. The
checklist is normalized input only: file existence, workflow NORMALIZED, counts,
PASS rows or waivers are not patch readiness/permission. Required FAIL, UNKNOWN,
stale, partial, missing, invalid, wrong-build or unavailable evidence yields the policy-
defined BLOCKED/INCOMPLETE result. Any gold-master Schema1/old path/report is stale.

## Phase 8 — Deterministic new-candidate gate — DOP-008/010

Create stable `cgs.day-one-patch-gate-row/v2` for every item/evidence obligation with
finding IDs, paths/declared revision, candidate/platform binding, state, owner, reason and row
revision. Preserve all failing/incomplete rows even when an earlier rule determines verdict.

Apply first-match order:

1. invalid plan/new-candidate/evidence/release identity -> ERROR;
2. unresolved S1 without the exact exception pair -> BLOCKED;
3. current conclusive bug/test/smoke/rehearsal/release-policy failure, scope/budget/
   owner violation, feature/refactor, unavailable rollback -> BLOCKED or NEEDS_REPLAN
   exactly as frozen policy states;
4. required PARTIAL/UNKNOWN/STALE/MISSING/NOT_RUN/TIMEOUT/INVALID/UNAVAILABLE/wrong-build/
   unpersisted evidence or incomplete platform coverage -> INCOMPLETE;
5. exact unresolved S1 with verified human acceptance plus platform permission ->
   PROCEED_WITH_ACCEPTED_S1_RISK_NOT_QA_PASS; and
6. only all verifiably fixed items, risk-derived regression, quick and full smoke,
   passing rollback rehearsal, current release evidence, no blockers and in-plan diff ->
   DAY_ONE_PATCH_READY.

Map ERROR→ERROR, BLOCKED/NEEDS_REPLAN→BLOCKED, INCOMPLETE→PARTIAL, and completed
non-passing S1 exception or DAY_ONE_PATCH_READY→EVALUATED. No unresolved S1 without
exception, timeout, partial or missing required evidence returns EVALUATED/ready.

## Phase 9 — Immutable controller artifacts, checkpoint, and resume

Each invocation may record at most one controller-owned absent artifact:

```text
production/releases/{release-id}/day-one-patches/{patch-id}/plans/{plan-id}.yaml
production/releases/{release-id}/day-one-patches/{patch-id}/gates/{gate-id}.md
production/releases/{release-id}/day-one-patches/{patch-id}/checkpoints/{checkpoint-id}.yaml
```

All reference IDs are schema-valid explicit revision. analyze-only writes nothing. For recording,
preview exact bytes/revision/target expected ABSENT, all input identities, recorder,
create-new primitive, size, authority/expiry and non-writes. Immediately before create,
CAS every input/dependency/owner/candidate/artifact/evidence/output revision, parent identity
and target absence. Use atomic no-replace/create-new, then flush, strictly parse,
read-back and verify. Drift/existing target writes nothing; post-create mismatch is
RECOVERY_REQUIRED and never silently overwritten/deleted.

Checkpoint binds predecessor, exact mode/state, manifests, issue/evidence inventory,
decisions, outputs/revisions and next legal idempotent step. RESUME revalidates the entire
chain and continues only that step. Never replay completed writes or trust conversation
memory.

## Phase 10 — Deployment/observation proposal and stop — DOP-011

`cgs.day-one-deployment-observation-plan/v1` is a proposal only. It defines the receipt
a separately authorized deployment must later produce: authorization/action IDs,
idempotency key, candidate/artifact/platform/account/environment, prior artifact,
external job/submission ID, observed installed reference ID/result, rollout/hold stages,
minimum observation window, crash/error/data-loss/funnel thresholds, sample/cadence,
owner, kill switch, automatic stop/rollback points and terminal states DEPLOYED,
STABILIZING, STABILIZED, POST_DEPLOY_DEGRADED or ROLLED_BACK.

Publication requires a verified successful deployment/observation receipt plus its own
message/channel authority. Bug verification/closure stays with canonical owners. This
workflow never chooses timing, runs deployment/monitoring/rollback, submits platform
builds, updates release/stage state, publishes notes or sends messages.

Return `cgs.day-one-patch-result/v2` with all identities; included/deferred items and
budgets; plan/evidence/gate/S1/recorder/authorization states; diff/bug/repro/regression/
smoke/release/rollback rows; stale/partial/not-run/timeout/unknown owners; target/revision or
NOT_WRITTEN; non-writes; and exactly one legal next action. Then stop.
