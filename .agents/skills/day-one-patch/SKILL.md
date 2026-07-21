---
name: day-one-patch
description: "Plans and evidence-gates one bounded day-one patch without implementing fixes, inheriting stale release approval, accepting unresolved S1 as QA PASS, or authorizing deployment/publication."
---

# Day-One Patch

This workflow has two responsibilities only:

1. produce an immutable, bounded patch and rollback plan; and
2. evaluate evidence created elsewhere for one exact new patch candidate.

It never edits game code, configuration, data, tests, assets, build scripts, bug
records, release state, or external systems. It never implements a fix, invokes
another workflow, deploys, submits a platform build, publishes notes, sends a
message, or closes a bug.

## Invocation

Accept exactly one mode:

~~~text
$day-one-patch plan --manifest <patch-request-manifest-path> --plan-id <id> [--persist]
$day-one-patch gate --plan <patch-plan-path> --candidate <build-candidate-manifest-path> --evidence <patch-evidence-manifest-path> --gate-id <id> [--persist]
$day-one-patch resume --checkpoint <path>
~~~

Reject unknown or duplicate flags, missing values, directories, unsafe paths,
positional scopes, and unrecognized modes. IDs are stable slugs or UUIDs, not dates
alone. Never infer a version, newest gate, latest build, current sprint, bug folder,
cert result, candidate, evidence, or deployment target. With missing arguments,
print only the supported forms and exit without delegation or writes.

`plan` never falls through to implementation or gate. `gate` is read-only except
for its optional gate report/checkpoint. `resume` revalidates immutable state and
continues only the interrupted planning or evidence-evaluation step.

## Independent authorization layers

Keep these authorities separate:

1. **Read-only planning/evaluation** — read and hash only manifest-declared inputs.
2. **Plan/report persistence** — create only the previewed plan, rollback proposal,
   evidence manifest template, gate report, and checkpoint files.
3. **Implementation** — source/config/data/test/asset/build-script mutation is
   outside this workflow and requires a separate exact downstream mutation manifest
   and explicit authorization.
4. **Build/QA execution** — producing a new candidate or running tests requires its
   own bounded execution and output authorization outside this workflow.
5. **Deployment/platform submission** — requires a separate human authorization
   naming candidate digest, platform/account/environment, action/idempotency key,
   rollback point, observation thresholds, and timing.
6. **Publication/notification** — patch-note publication, store text, public posts,
   player or stakeholder messages each require a separate human authorization naming
   channel/account, immutable message digest, action/idempotency key, and timing.

Approval at one layer never carries to another layer, another build, revised plan,
new path, retry, platform, account, message, or action. Scope approval means only
“approved for implementation handoff”; it does not authorize implementation. A
persisted plan, agent recommendation, QA evidence, `DAY-ONE PATCH READY`, or release
manager/producer/QA role label grants no deploy or publication authority.

A bounded request may authorize exact plan/report output paths. Otherwise preview
the complete CREATE set and obtain one approval before persistence. Never include
product mutation in that changeset. This workflow stops if asked to implement,
deploy, submit, publish, notify, or update a bug/release record and reports the
separate authority and owner required.

## Canonical planner artifacts and unique writers

Use:

~~~text
production/releases/<release-id>/day-one-patches/<patch-id>/plans/<plan-id>/plan.md
production/releases/<release-id>/day-one-patches/<patch-id>/plans/<plan-id>/rollback-plan.md
production/releases/<release-id>/day-one-patches/<patch-id>/plans/<plan-id>/evidence-manifest-template.yaml
production/releases/<release-id>/day-one-patches/<patch-id>/plans/<plan-id>/checkpoints/<checkpoint-id>.md
production/releases/<release-id>/day-one-patches/<patch-id>/gates/<gate-id>/report.md
~~~

Release ID, patch ID, plan ID, and gate ID must match the policy's slug/semantic
version grammar and may not contain separators, dot segments, or reserved device
names. Reject existing targets rather than overwrite them.

The day-one-patch controller is the sole writer of the artifacts above. Assessment
agents return read-only recommendations and write nothing. External implementers,
builders, QA owners, bug owners, release managers, and communication owners retain
exclusive ownership of their artifacts; this workflow only consumes their exact
paths/hashes. If the named owner or artifact is unavailable, evidence remains
missing/unknown and ownership is never transferred silently.

## Status and verdict vocabulary

Return these independent fields:

| Field | Allowed values |
|---|---|
| `Workflow Status` | `COMPLETE`, `PARTIAL`, `BLOCKED`, `ERROR` |
| `Plan Verdict` | `READY FOR IMPLEMENTATION HANDOFF`, `REPLAN REQUIRED`, `NO PATCH`, `INCOMPLETE`, `BLOCKED` |
| `Evidence State` | `CURRENT`, `STALE`, `MISSING`, `PARTIAL`, `UNKNOWN`, `INVALID`, `NOT_RUN`, `UNAVAILABLE` |
| `Patch Gate Verdict` | `DAY-ONE PATCH READY`, `NEEDS REPLAN`, `INCOMPLETE`, `BLOCKED`, `ERROR`, `PROCEED WITH ACCEPTED S1 RISK — NOT QA PASS` |
| `S1 Disposition` | `NONE`, `HARD BLOCK`, `HUMAN ACCEPTED / PLATFORM ALLOWED` |
| `Implementation Authorization` | always `NOT GRANTED` |
| `Deployment Authorization` | always `NOT GRANTED` |
| `Publication Authorization` | always `NOT GRANTED` |
| `Persistence` | `WRITTEN`, `NOT_REQUESTED`, `DECLINED`, `FAILED`, `NOT_ATTEMPTED` |

`COMPLETE` describes successful planning/evaluation, not implementation or release.
No partial, timeout, stale, unknown, unavailable, not-run, wrong-build, or
non-persisted required evidence may become PASS.

## Phase 0: Validate one release and patch request

Resolve every literal and real path. Reject symlink escapes, dot segments, malformed
or duplicate keys, unsupported schemas, unbounded scans, and paths outside the
project root. Read raw bytes once and compute full lowercase SHA-256.

Require:

- `Artifact Type: day-one-patch-request`, schema version, stable release ID, product
  ID, patch ID/version, target window, regions and platforms;
- exact gold-master `build-candidate` manifest path/hash, candidate/build IDs,
  artifact path/hash, source commit, immutable tag/ref, engine/toolchain version,
  platform/configuration matrix, test-manifest path/hash, and QA-plan path/hash;
- exact original release-candidate manifest, release-policy, and prior release-gate
  evidence paths/hashes for comparison only;
- ordered canonical bug index with exact `production/qa/bugs/<BUG-ID>.md` path and
  raw-byte hash; exact cert-feedback/external issue receipts when applicable;
- patch budgets: maximum issue count, implementation round count, effort, changed
  file count, diff/line/asset size, platform count, and calendar window;
- risk policy defining S1/S2 handling, security/privacy/data/platform conditions,
  required QA matrix, rollback requirements, and readiness algorithm;
- target hardware/environment inventory, deployment/monitoring policy, owner registry,
  output root, generated-at timestamp, and applicable AGENTS.md path/hash chain.

Re-hash the gold-master candidate/artifact, policy, every bug, cert receipt, and
instruction. Prior release evidence must bind the gold master; it is historical
context only. A missing/ambiguous identity, hash mismatch, unsafe version, dirty
unrecorded source, missing budget, or invalid policy returns `Workflow Status:
BLOCKED` and writes nothing.

## Phase 1: Load the canonical bug state machine

Only canonical records at `production/qa/bugs/<BUG-ID>.md` are bug authority. Require:

- `Schema Version: 1`;
- filename and field ID matching `BUG-[0-9]{4,}`;
- severity exactly `S1-Critical`, `S2-Major`, `S3-Minor`, or `S4-Trivial`;
- status exactly `Open`, `Fixed Pending Verification`, `Verified Fixed`, or `Closed`;
- current transition history and raw-byte SHA-256.

Never read `production/bugs/`, triage output, filenames as severity, or free-text
priority as lifecycle authority. Reject duplicate IDs, filename/body mismatch,
unknown enums, illegal transitions, or ambiguous records.

Respect the staged bug lifecycle:

- `Open` means unresolved.
- `Fixed Pending Verification` means a fix owner recorded a candidate fix, but it is
  not verified.
- `Verified Fixed` requires both a target-build reproduction PASS receipt and a
  failure-sensitive automated regression PASS receipt bound to the exact fix
  revision/build/platform.
- `Closed` additionally requires the authorized QA closure transition and the same
  current evidence.
- Source inspection, diff presence, a manual-only check, smoke alone, or a test file's
  existence proves at most `FIX PRESENT / RUNTIME UNVERIFIED`.

This workflow never mutates status. For gate evaluation, an included bug must be
`Verified Fixed` or `Closed` and its receipts must revalidate against the new patch
candidate. `Fixed Pending Verification` is `INCOMPLETE`; `Open` is unresolved.

## Phase 2: Select one bounded patch set

Normalize issues into stable patch item IDs such as `DOP-ITEM-0001`. Preserve the
source bug/cert ID and evidence hash.

An item may be included only when all are true:

- it is a fix to an existing defect or mandatory cert issue, not a feature, refactor,
  cleanup, architecture change, speculative optimization, or new behavior;
- one owner and exact allowed/prohibited path set are known;
- estimated effort, changed files, diff/asset size, platform scope, dependency count,
  and total patch budgets remain within policy;
- the minimum viable change, risk class, data/save/network/security effect, candidate
  build impact, and rollback method are explicit;
- required failure-sensitive regression test ID/path, target-build reproduction case,
  QA-plan stable check IDs, hardware/platform rows, and evidence owners are known;
- implementation can complete in the one manifest-declared implementation round.

Do not implement or start an open-ended per-bug loop. If the candidate count or any
budget is exceeded, deterministically rank by the policy's severity/risk/cert rules,
include only the bounded non-S1 set, mark the rest deferred with owner/rationale, and
return `REPLAN REQUIRED` when required items cannot fit. Never estimate by severity
alone when the request requires real team capacity or platform timing evidence.

### S1 rule

An unresolved `S1-Critical` is a default release hard block. It must either be
included as the highest-priority bounded emergency remediation item or the plan is
`BLOCKED`; it may not be casually deferred. A complete plan may return
`READY FOR IMPLEMENTATION HANDOFF` so an independently authorized owner can attempt
the fix, but this is not QA or release readiness. At `gate`, the bug must be
`Verified Fixed` or `Closed` with current new-candidate evidence before
`DAY-ONE PATCH READY` is possible.

If the S1 is still unresolved at gate, the only exception requires both:

1. a current platform/release-policy receipt explicitly allowing shipment with that
   exact unresolved S1 on the named release/candidate/platform; and
2. an independent human `day-one-s1-risk-acceptance` artifact binding bug/release/
   candidate/platform, authority identity, explicit decision, rationale, expiry,
   player/data impact, compensating controls, monitoring thresholds, rollback trigger,
   prior artifact, and communication plan.

This workflow never creates or solicits that acceptance. Even when both verify, the
only gate result is `PROCEED WITH ACCEPTED S1 RISK — NOT QA PASS`, with
`S1 Disposition: HUMAN ACCEPTED / PLATFORM ALLOWED`. Preserve the bug's `Open` status
and original severity. Without both, return `BLOCKED`, `S1 Disposition: HARD BLOCK`.
No agent, producer, QA lead, release manager, prose rationale, checkbox, or old
release approval can waive S1.

## Phase 3: Build the immutable patch plan

For each included item record:

- stable patch item ID; canonical bug/cert ID, path/hash, severity/status;
- exact requirement and evidence sources/hashes;
- owner, estimated effort basis, risk class, dependencies, and implementation round;
- exact allowed and prohibited paths, maximum changed files/diff/assets, generated
  outputs, and no-feature/no-refactor constraint;
- minimum fix behavior and acceptance criteria without prescribing unreviewed design;
- target-build reproduction case ID and failure-sensitive automated regression test
  ID/path;
- ordered quick-smoke stable QA-plan check IDs and expected scope hash inputs;
- required broader regression, sprint smoke, security/privacy/data/network/platform
  checks derived from risk;
- candidate/build/release evidence outputs required from downstream owners;
- rollback, monitoring, player impact, and deferred-work linkage.

The plan must also contain a complete handoff manifest. Each downstream implementation
item receives only its exact bug evidence, requirements, allowed paths, diff budget,
test expectations, rollback obligations, deadline, and output receipt schema.
Implementation requires its own exact mutation authorization and occurs outside this
workflow. Do not invoke or simulate an implementer.

### Rollback plan

The rollback proposal must name, per platform:

- exact gold-master/previous artifact path/hash and patch candidate placeholder;
- executable rollback/revoke/forward-recovery steps and tool/version;
- save/data/schema compatibility in both directions, backup/checkpoint, and
  irreversible operations;
- operator and independent verifier, required permissions, timeout, RTO/RPO;
- rehearsal environment equivalent to production, command/argv, workload, duration,
  expected observables, logs/receipt paths, and pass/fail semantics;
- numeric crash/error/data-loss/funnel thresholds, sample/window requirements,
  observation cadence, automatic/manual stop point and kill-switch owner;
- player/stakeholder message drafts and channels as proposals only.

A platform that cannot roll back requires a current policy-authorized recovery
alternative with equivalent containment and verification. “Revert the commit,” a
role name, or an untested prose checklist is not a valid gate artifact.

## Phase 4: Persist or hand off the plan

If there are no applicable open/cert issues, return `Plan Verdict: NO PATCH`,
`Workflow Status: COMPLETE`, and optionally persist an empty evidence-based plan.
Do not infer “no issues” from an empty scan; the exact indexed sources must load.

If an S1 cannot be included in the bounded emergency remediation set, return
`Plan Verdict: BLOCKED`, `Workflow Status: BLOCKED`. An included S1 may be handed
off only for an independently authorized fix attempt; no S1 exception artifact is
needed merely to plan the fix. A partial/timeout/unavailable assessment returns
`INCOMPLETE`, never handoff-ready.

Otherwise present the exact plan and tradeoffs. A human may approve, adjust, or
decline the scope. Approval records a scope decision only. After a current approved
scope record is supplied, return `READY FOR IMPLEMENTATION HANDOFF`; still return
`Implementation Authorization: NOT GRANTED`.

For persistence, preview only the controller-owned CREATE paths. Re-hash all inputs
and target absence immediately before atomic writes; read back bytes, validate every
reference/count, and return full SHA-256. Declined/failed persistence produces no
consumable plan.

## Phase 5: Validate the new patch candidate and implementation receipts

`gate` requires an immutable approved plan and an independently produced
`build-candidate`. The candidate must contain the exact smoke-check identity contract:

- `Artifact Type: build-candidate`, schema/manifest version;
- candidate ID, build ID, build artifact path/SHA-256, source commit;
- engine and exact runner-compatible version;
- platform/configuration target matrix and created-at timestamp;
- test-manifest path/SHA-256 and QA-plan path/SHA-256;
- trusted build receipt for a remote artifact.

The patch evidence manifest requires:

- `Artifact Type: day-one-patch-evidence`, schema version, plan path/hash;
- base gold-master and new patch candidate identities;
- exact release-candidate-manifest and release-policy paths/hashes for the new build;
- ordered patch item implementation receipts, diff manifest, source/base/result
  hashes, changed paths, owner, commands, timestamps, result, and omissions;
- exact revalidated canonical bug records and their target-build reproduction and
  failure-sensitive regression receipts;
- quick and sprint smoke report paths/hashes;
- fresh release-evidence-checklist path/hash;
- rollback rehearsal, broader regression/risk evidence, platform receipts, and
  monitoring/deployment handoff definitions;
- generation timestamp, owner, hash algorithm, and applicable instructions.

Re-hash the plan, candidate, artifact, source snapshot/commit, implementation receipts,
diff paths, bug records, tests, QA plan, policy, and every evidence reference. The
actual diff must be a subset of each item's allowed paths and total budgets, with no
unplanned item, extra implementation round, new feature, refactor, generated output,
or owner violation. Any scope expansion returns `NEEDS REPLAN`. This workflow does
not repair or revert it.

A changed build makes every gold-master release PASS, smoke receipt, QA sign-off,
cert claim that is build-specific, and profiler/test result stale. They may appear
only in the comparison section and can never satisfy the patch gate.

## Phase 6: Consume exact quick and full smoke receipts

For changed-area evidence, accept only the exact declared canonical quick report:

~~~text
production/qa/evidence/smoke/<candidate-id>/<run-id>/report.md
~~~

Require `Artifact Type: smoke-check-receipt`, `Schema Version: 1`, exact candidate
manifest path/hash and candidate/build/artifact/source/platform identity, exact QA
plan/test manifest paths/hashes, `QA Plan Effective State: CURRENT`, `Mode: quick`,
`Verdict: TARGETED CHECK PASSED`, `Handoff Eligible: NO`,
`Receipt State: COMPLETE`, `Persistence: WRITTEN`, and a scope containing exactly the ordered stable QA-plan check IDs declared by included
patch items. Recompute and verify the scope hash and every automated/manual evidence
hash.

Never pass affected-system names to quick smoke and never translate them at gate time.
The plan must supply stable IDs before implementation. Quick smoke is targeted
evidence only; its `Handoff Eligible: NO` is expected and cannot be rewritten.

`DAY-ONE PATCH READY` additionally requires a separately persisted sprint-mode smoke
receipt for the same candidate with `Verdict: PASS`, `Handoff Eligible: YES`,
`QA Plan Effective State: CURRENT`, `Receipt State: COMPLETE`, `Persistence: WRITTEN`,
complete current stable-ID coverage, no warning, and verified transitive hashes.
Quick success alone yields `INCOMPLETE`.

FAIL takes precedence over missing evidence. Quick/sprint `INCOMPLETE`, NOT_RUN,
TIMEOUT, warning-bearing, stale, unpersisted, wrong-build, or mismatched receipts
cannot pass.

## Phase 7: Revalidate bug, rollback, regression, and release evidence

For every included bug:

- canonical status must be `Verified Fixed` or `Closed`; the exact unresolved S1
  covered by both exception artifacts is tracked separately and never satisfies this
  QA item or contributes to `DAY-ONE PATCH READY`;
- re-hash the `Fixed Pending Verification → Verified Fixed` transition;
- require a target-build reproduction PASS for the exact bug/repro case/new candidate/
  fix commit/platform;
- require a failure-sensitive automated regression PASS matching the record's test
  ID/path, fix commit, exact invocation, exit code, and complete log hash;
- manual evidence or smoke cannot replace the automated regression receipt.

`Open` is a conclusive unresolved failure. `Fixed Pending Verification`, missing or
mismatched receipts, or static-only `FIX PRESENT / RUNTIME UNVERIFIED` is incomplete.
Do not mutate the record or claim it was closed.

Require a current rollback rehearsal receipt for each platform, binding plan, base
artifact, patch candidate, recovery method, environment, operator/verifier,
command/argv, tool version, data compatibility/backups, start/end, measured RTO/RPO,
observed result, logs/hashes, and verdict. A missing, failed, partial, stale, or
platform-inapplicable rollback without a verified equivalent recovery blocks.


### New release-candidate manifest

Validate the exact new release manifest before its checklist. Require:

- `Artifact Type: release-candidate-manifest`, `Schema Version: 1`, stable release
  ID and semantic/display version;
- platform/configuration matrix;
- exact patch build-candidate manifest path/raw SHA-256 and matching candidate ID,
  build ID, artifact path/hash, source commit, and immutable release tag/ref;
- exact release-policy path/hash and policy version;
- ordered evidence index keyed by stable release item ID, including the patch-specific
  receipts above;
- exact applicable AGENTS.md path/hash chain;
- generated-at timestamp and manifest owner.

Re-hash every indexed artifact and reference. A manifest for the gold master, another
candidate/platform, an inferred latest build, or an unsigned/unverifiable remote
artifact is stale or invalid and cannot route checklist evidence.

Consume the fresh release checklist only at:

~~~text
production/releases/<release-id>/<release-manifest-sha256>/release-checklist.md
~~~

Require `Artifact Type: release-evidence-checklist`, `Schema Version: 1`, the full
64-character release-manifest digest path segment, exact new release/policy/candidate/
build/artifact/source/platform identity, `Persistence: WRITTEN`, and verified report
bytes/references. `Workflow Status: COMPLETE` means all items were normalized;
`Gate Decision: NOT EVALUATED` is required and is not permission. Independently apply
the release policy. Any required FAIL, UNKNOWN, stale, partial, missing, invalid,
wrong-build, or unavailable evidence blocks or makes the gate incomplete according
to the deterministic table.

## Phase 8: Deterministic patch gate

Evaluate only current evidence for the exact new candidate.

Apply this first-match order:

1. invalid plan/candidate/evidence/release identity -> `ERROR`;
2. unresolved S1 without verified exception pair -> `BLOCKED`;
3. any current conclusive included-bug failure other than the exact accepted S1,
   smoke/regression/rehearsal failure, required release-policy FAIL, scope/budget
   violation, new feature/refactor, or rollback unavailable -> `NEEDS REPLAN` or
   `BLOCKED` as named by policy;
4. otherwise any required evidence `PARTIAL`, `UNKNOWN`, `STALE`, `MISSING`,
   `NOT_RUN`, `TIMEOUT`, `INVALID`, `UNAVAILABLE`, wrong-build, unpersisted, or
   incomplete platform coverage -> `INCOMPLETE`;
5. otherwise, an unresolved S1 with verified human acceptance and platform permission
   -> `PROCEED WITH ACCEPTED S1 RISK — NOT QA PASS`;
6. only when every included bug is verifiably fixed, all risk-derived tests and both
   quick/full smoke requirements pass, rollback rehearsal passes, the fresh release
   evidence is current, zero release blockers remain, and the actual diff stays
   within plan -> `DAY-ONE PATCH READY`.


Map the gate verdict to workflow status without ambiguity:

- `ERROR` -> `Workflow Status: ERROR`;
- `BLOCKED` or `NEEDS REPLAN` -> `Workflow Status: BLOCKED`;
- `INCOMPLETE` -> `Workflow Status: PARTIAL`;
- `PROCEED WITH ACCEPTED S1 RISK — NOT QA PASS` -> `Workflow Status: COMPLETE`
  only because the exceptional evidence evaluation completed; it remains non-passing
  and non-authorizing;
- `DAY-ONE PATCH READY` -> `Workflow Status: COMPLETE`.

An unresolved S1 without the verified exception pair can therefore never return
`Workflow Status: COMPLETE`.

Always list failures and incomplete rows even when an earlier result wins. A QA lead,
producer, release manager, model, checkbox, old gate, or user phase approval cannot
convert evidence state. Every result returns all three authorization fields as
`NOT GRANTED`.

## Phase 9: Timeout, partial evidence, checkpoint, and resume

Bound read-only assessment delegations by `.codex/config.toml max_threads`; count the
root and all nested agents. With `max_threads = 6` and only the root live, at most
five children may run. If configuration is missing/invalid, run serially. Assign
deadlines and gather bounded batches.

A timeout, blocked/error response, unreadable source, partial evidence, or cancelled
delegate remains visible with owner, attempted scope, deadline, and dependency
impact. Required unknown/partial work blocks readiness; there is no “skip and pass.”
No late response may mutate an already persisted plan/report.

Write immutable checkpoints after input validation, issue selection, plan decision,
candidate validation, and gate aggregation. Each binds predecessor hash, manifests,
bug/evidence inventory, agent statuses, decisions, output bytes/hashes, and next
permitted step. `resume` re-hashes the chain and continues only the first incomplete
idempotent read/write. Drift or an existing output blocks; never replay completed
writes from conversation memory.

## Phase 10: Deployment and publication handoff — stop

The plan may define the receipts a separately authorized deployment must later
produce:

- deployment action/authorization IDs and idempotency key;
- exact patch candidate/artifact/platform/account/environment and previous artifact;
- start/end, external job/submission ID, observed installed digest and result;
- rollout/hold stages, monitoring window, numeric crash/error/data-loss/funnel
  thresholds, sample requirements, observation cadence, owner and kill switch;
- rollback/recovery action and receipt;
- terminal states such as `DEPLOYED`, `STABILIZING`, `STABILIZED`,
  `POST_DEPLOY_DEGRADED`, and `ROLLED_BACK`.

Publication must wait for a verified successful deployment receipt and its own human
authorization/message digest/idempotency check. Bug verification/closure must follow
the canonical bug state machine and its authorized owners; this workflow never runs
those transitions.

Stop after returning the gate report. Do not choose deployment timing, submit a
platform build, update release/stage state, publish patch notes, notify players or
stakeholders, schedule monitoring, or perform post-launch operations.

## Output

Always include:

- release/patch/base/new candidate/build/artifact/source/platform identity;
- plan, evidence, gate, S1, persistence, and all authorization states;
- bounded included/deferred item tables with stable IDs, bug states and exact hashes;
- implementation/diff/reproduction/regression/smoke/release/rollback evidence matrix;
- failures, stale/partial/not-run/timeout/unknown rows and accountable owners;
- immutable output/checkpoint paths and hashes;
- one next permitted action or `none`.

A downstream deployment owner must re-hash the candidate and report, obtain explicit
deployment authority, and treat `DAY-ONE PATCH READY` as evidence rather than
permission.
