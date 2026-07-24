---
name: team-release
description: "Orchestrate one immutable release through evidence gates, separately authorized staging and production actions, receipted publication, reconciliation, rollback, and completed stabilization without treating any workflow artifact as permission."
---

# Team Release

Coordinate one exact release candidate from identity validation through stabilization.
Evidence, a producer decision, a recorded file, a role label, and a successful build
are never deployment or publication permission. This workflow is fail-closed and
resumable from immutable action receipts.

## Invocation

Invoke only as:

`$team-release --request <path> --expect-request <sha256>`

Require both flags exactly once. Unknown, duplicate, missing, malformed, relative-to-
another-root, or hash-mismatched arguments stop before project reads, delegation,
output, mutation, deployment, or communication.

The request is strict `cgs.team-release-request/v2` and declares exactly one mode:

- `PREPARE` — read-only gate evaluation, optionally followed by one separately
  authorized immutable controller-record CREATE;
- `REPOSITORY_ACTION` — one separately authorized branch/tag/push/release-object action;
- `STAGE` — one separately authorized staging deployment action;
- `PROMOTE` — one separately authorized production canary/promotion action;
- `PUBLISH` — one separately authorized external communication action;
- `RECONCILE` — read-only external-state lookup for one unknown action, optionally
  followed by one separately authorized immutable reconciliation-receipt CREATE;
- `ROLLBACK` — one exact separately authorized rollback unless an exact, current,
  policy-backed conditional rollback authorization already covers it; or
- `STABILIZE` — read-only monitoring evaluation, optionally followed by one separately
  authorized immutable stabilization-record CREATE.

The request names stable release/run/action IDs, exact request operation, expected
predecessor state/receipt, every path and full lowercase SHA-256, applicable root-to-
target `AGENTS.md` chain, fixed read/byte/dependency/time budgets, and controller output
root. Never infer a newest version, milestone, candidate, report, environment, target,
action, receipt, or policy from directory order, filename, mtime, Git HEAD, or prose.

## Authority model and non-writes — TRL-012

Keep these authorities independent:

1. read-only analysis;
2. controller file CREATE for the exact presented bytes and absent target;
3. repository mutation for exact refs/commits/remote/action;
4. staging deployment for exact artifact/target/action/idempotency key;
5. production deployment or rollback for exact artifact/target/action/idempotency key;
6. external publication for exact account/channel/message/action/idempotency key; and
7. any milestone, stage, issue, store, or release-state update.

Authority at one layer never grants another, and authority expires when any bound byte,
digest, target, action, attempt, or precondition changes. A generic phase approval,
file-write approval, `GO`, `LAUNCH_READY`, `DAY_ONE_PATCH_READY`, role recommendation,
or prior authorization is not reusable authority.

Writer ownership is disjoint. `release-manager` owns only version/scope/release-manifest
coordination and terminal summaries. `devops-engineer` is the unique build/sign/package,
repository-action, deployment, rollback, and external-state reconciliation executor.
QA, security, network, performance, localization, analytics, platform/legal, and other
gate producers own only their declared evidence. `community-manager` owns message drafts
and, under separate publication authority, publication. The controller never claims a
producer's receipt or edits another owner's artifact.

Never update source, tests, CI, evidence, policy, sign-offs, bugs, release or launch
checklists, day-one artifacts, build bytes, refs, tags, stores, infrastructure,
deployments, messages, `production/stage.txt`, or milestone state unless the invocation
is the exact separately authorized owning action. A planned action is not an executed
action.

## Canonical identities — TRL-007

Normalize literal and real paths under the project root, reject dot segments, symlink
escapes, duplicate/unknown keys, unsafe encodings and unsupported schemas, then read raw
bytes once and compute full lowercase SHA-256.

The request binds an immutable `cgs.release-orchestration-manifest/v2` containing:

- release/product IDs, stable approved milestone ID, semantic/display version, version
  policy and registry snapshot identities, regions, channels and target time;
- exact `cgs.release-candidate-manifest/v2`, build-candidate manifest and trusted build
  receipt paths/hashes;
- source commit and tree, immutable ref/tag proposal, dirty-state proof, build/toolchain/
  container/configuration identities and complete platform/configuration matrix;
- artifact path/hash, SBOM path/hash, provenance/signature path/hash and verification
  receipts for every target;
- exact release policy, authority registry, risk manifest, deployment plan,
  communication plan, instruction chain and ordered evidence/gate indexes;
- exact adjacent checklist/result inputs when applicable; and
- ordered action registry, writer ledger and generation identity.

Compute and record `release_identity_sha256`, `candidate_identity_sha256`,
`build_identity_sha256`, `artifact_set_identity_sha256`, `risk_identity_sha256`,
`evidence_snapshot_sha256`, `gate_identity_sha256`, `action_registry_sha256`, and
`instruction_chain_sha256`. All reports, delegations, decisions, authorizations,
actions and receipts must bind the same identities. A rebuild, resign, repack, source
change, platform-matrix change, manifest drift, or policy change creates a new identity
and invalidates dependent evidence and unexecuted authority.

## Phase 1 — Resolve version without inference — TRL-015

Read the exact stable milestone record, exact semver/version policy, exact version-
registry/tag snapshot, and current local/remote ref observations declared by the
request. Validate milestone-to-release mapping, allowed semver transition, channel/
prerelease rule, monotonicity, uniqueness, product namespace, immutable tag syntax,
tag-to-commit binding and collision absence across local refs, remote refs, release
objects, artifact registries and platform submissions.

Missing, stale, partial, ambiguous or conflicting version evidence is `BLOCKED`. Never
derive a version from “latest milestone,” select a nearby version, increment a number,
overwrite a tag, or mutate a registry. Tag/ref creation is a later `REPOSITORY_ACTION`
with its own exact authority and receipt.

## Phase 2 — Build-rooted dependency graph — TRL-009

Freeze the build before candidate-bound gates. The build adapter accepts either the
internal `cgs.build-receipt/v2` or the existing producer contract
`cgs-build-receipt/v1`; no other spelling, alias or version is compatible. The request
must pin the producer receipt's exact path and raw-byte SHA-256. For v1, require exact
`status: SUCCESS`, candidate ID and candidate-identity hash, build ID, source commit and
tree, artifact IDs and SHA-256 values, platform/configuration, and approval boundary to
match the release candidate and build-candidate manifest. Also verify every supplied
SBOM, signature, provenance, toolchain, container, command/argv, environment,
runner/job, timestamp, exit, log and target-platform field instead of filling a v2
field by inference.

Normalize a valid v1 receipt in memory to `cgs.build-receipt/v2` without loss: retain
the exact producer schema, full parsed producer payload, raw-byte SHA-256, source path,
producer status and a field-by-field source mapping alongside the normalized v2
candidate/build/source/artifact values. Record a deterministic normalized-view hash.
Do not rewrite, rename, copy or persist the producer receipt. A missing v2-required
fact remains explicit `UNKNOWN` and blocks its dependent gate; it is never synthesized.
Normalization establishes data compatibility only. Neither a schema rename, a
successful build nor the adapter's normalized view grants release, deployment,
publication or file-mutation authority.

Order the dependency graph:

1. identity, version and policy validation;
2. build/package/sign and trusted build receipt;
3. candidate-bound QA, CI, security, privacy, performance, network, localization,
   analytics, certification and recovery evidence;
4. release/launch/day-one normalization and gate evaluation;
5. human producer decision;
6. staging authorization, action and receipt;
7. independent post-stage smoke;
8. production authorization, canary/action and receipt;
9. separately authorized publication; and
10. monitoring, possible rollback and stabilization.

Only pure document/schema checks independent of candidate bytes may run before step 2.
Never run build creation concurrently with a build-bound gate. Every downstream
artifact must bind the exact resulting digest; a new build restarts step 3.

## Phase 3 — Deterministic risk routing — TRL-010

Require exact `cgs.release-risk-manifest/v2`, produced by its declared human/project
authority and bound to release/candidate/policy/time. It has explicit tri-state
`YES|NO|UNKNOWN` dimensions for online connectivity/external services, multiplayer and
network authority, accounts/authentication, player/payment/personal data, telemetry and
privacy, economy/transactions, persistence/schema/data migration, irreversible effects,
platform certification/distribution, legal/ratings, localization, and live-service
health dependencies.

Route gates exclusively through versioned policy predicates. `YES` activates the
relevant gate. `NO` is usable only with the required applicability authority. Missing,
unreadable, stale, ambiguous, contradictory or `UNKNOWN` risk is conservatively treated
as high-risk: activate every plausibly relevant hard gate and leave it `UNKNOWN` until
current evidence exists. Staffing, `lean`, `solo`, schedule pressure or model judgment
cannot remove a gate.

## Phase 4 — Evidence execution contracts — TRL-011

Every executable gate is declared as `cgs.release-gate-request/v2` and returns a
persisted `cgs.release-gate-receipt/v2`. The request/receipt pair includes stable gate
and run IDs, producer/verifier authority, release/candidate/build/artifact/source/
platform identities, exact inputs/dependencies, tool and runner versions, executable or
workflow identity, exact command/argv, environment/container/config hashes, start/end/
observed times, timeout, exit code and result, coverage/sample scope, raw log/output/
attachment paths and hashes, signature/identity verification, freshness/expiry,
completeness, and canonical `PASS|FAIL|UNKNOWN|TIMEOUT|ERROR|CANCELLED`.

Missing command, runner, environment, timestamp, hash, completeness, candidate binding,
producer proof or required raw output makes the receipt `UNKNOWN`; prose, checkbox,
conversation output, scheduled job, previous run or role label is not evidence. A
conclusive current policy negative is `FAIL`, never softened to UNKNOWN.

Gate rows are immutable and ordered by policy: stable gate ID, applicability, class,
owner, producer, exact request/receipt path/hash, dependencies, candidate/platform,
freshness, result, reason and row hash. One writer owns each output path.

## Phase 5 — Bounded, risk-ordered dispatch — TRL-008

Before each delegation batch, read the configured `max_threads`, enumerate every live
root, child and nested agent, and calculate:

`available_child_slots = max(0, max_threads - live_threads_including_controller)`

If configuration or live count is unavailable/invalid, run serially. Never assume six
free workers because `max_threads = 6`; with only the controller active at most five
children may run. Reserve nested slots explicitly and require delegates not to spawn
unless assigned one. Actual active workers must remain below or equal to the computed
slots, with one slot per dispatched worker.

Dispatch risk-ordered batches only after all dependencies are frozen: identity/build
first; core QA/CI, security/privacy, migration/recovery and platform/legal hard gates
next; network/performance/localization hard gates next; analytics and advisory gates
last. Gather and record a whole batch before dispatching its consumers. Timeouts,
partial responses, cancellation, unavailable owners and malformed receipts remain
UNKNOWN and block dependent hard gates. Preserve completed independent work.

## Phase 6 — Adjacent P1 contracts

### Release checklist

Consume only the exact declared persisted report at:

```text
production/releases/{release-id}/{candidate-identity-sha256}/checklists/
{checklist-identity-sha256}.md
```

Require `Artifact Type: release-evidence-checklist`, `Schema Version: 2`, recorder
`CREATED`, exact request/release/candidate/build/deployment/policy/authority/instruction/
evidence/checklist identities, verified raw report hash, complete ordered row hashes,
and `Gate Decision: NOT_EVALUATED`, `Release Authority: NONE`, `Deployment Authority:
NONE`, `Publication Authority: NONE`. Re-hash every dependency and independently apply
release policy. `NORMALIZED`, counts, PASS rows, N/A or waiver never grant GO.

### Launch checklist

When policy applies, consume only the exact declared report at:

```text
production/releases/{release-id}/{launch-candidate-identity-sha256}/launch-readiness/
{assessment-identity-sha256}.md
```

Require the exact `cgs.launch-checklist-result/v2`, report path/hash, launch candidate,
risk/policy/authority/instruction/test/evidence/assessment identities, complete rows,
recorder success, `Launch Decision: NOT_RECORDED`, `Deployment Authority: NONE`, and
`Publication Authority: NONE`. Readiness is evidence only. BLOCKED/ERROR/UNDETERMINED,
hard UNKNOWN/FAIL, stale identity, or incomplete coverage blocks; concerns follow only
the release policy's narrow risk-acceptance path.

### Day-one patch

When the release is a declared day-one patch, consume the exact approved plan and
`cgs.day-one-patch-result/v2` for the same new release/candidate/build/artifact/source/
platform plus its fresh release checklist. Re-hash plan/evidence/gate/rollback/smoke/
S1/recorder identities and rows. The result, `DAY_ONE_PATCH_READY`, and its
`cgs.day-one-deployment-observation-plan/v1` are evidence/proposals only and grant no
deployment, submission, rollback, message or publication authority. An unresolved S1
exception remains non-PASS; it may proceed only when both release/platform policy and
an exact independent `cgs.day-one-s1-risk-acceptance/v2` allow it, yielding accepted
risk rather than GO. `cgs.day-one-smoke-request/v2` is only a producer handoff; accept
only its independently persisted build-bound response.

Never invoke those workflows, discover their latest output, or treat their file
existence, workflow completion, result label, verdict, recorder or role as authority.

## Phase 7 — Gate decision

Hard blockers include open policy-defined S1/S2 defects; failed/unknown security,
privacy, legal, ratings, certification, network or migration gates; identity, artifact,
SBOM, signature, provenance, source, platform or version collision; unrehearsed or
irreversible data impact; missing verified rollback; missing canary, numeric health
threshold, monitoring or kill switch; partial/stale/timeout/invalid hard evidence; and,
at promotion time, non-current staging smoke.

These classes have no generic override. They can only be fixed and re-evaluated or the
release cancelled/deferred. Do not solicit prose justification.

Only a policy-declared waivable advisory/lower-severity finding may use immutable
`cgs.release-risk-acceptance/v2` from the named owner and independent authority, binding
finding IDs, original status, exact identities/scope, rationale, issued/expiry,
compensating controls, residual risk, monitoring and rollback triggers. Preserve the
original row. Valid acceptance yields only `GO_WITH_ACCEPTED_RISK`.

Decision: any non-waivable or unresolved hard FAIL/UNKNOWN -> `NO_GO`; any waivable
issue without valid acceptance -> `NO_GO`; otherwise valid accepted issues ->
`GO_WITH_ACCEPTED_RISK`; otherwise every required current gate PASS -> `GO`. A producer
records this evidence-derived decision but grants no later authority.

## Phase 8 — Action state machine, checkpoints and recovery — TRL-016/TRL-017

Each registered action declares action ID/type, idempotency key, attempt number,
executor, exact target/account/project/region/environment/channel, artifact or message
digest, preconditions and expected prior state, timeout, retry budget/backoff,
reconciliation query, expected observable/result, rollback/compensation, authorization
scope/expiry and receipt target.

Canonical action states are `NOT_STARTED`, `AUTH_REQUIRED`, `AUTHORIZED`, `IN_PROGRESS`,
`SUCCEEDED`, `FAILED`, `TIMED_OUT_UNKNOWN`, `OUTCOME_UNKNOWN`, `ROLLED_BACK`,
`RECONCILED_NO_MUTATION`, and `RECONCILED_MUTATION`.

Immediately before action, re-hash all inputs and authority, query existing state by
target plus idempotency key, and write/return an immutable pre-action checkpoint. After
each external observation or action, create an immutable
`cgs.release-action-receipt/v2`; this remains the sole canonical action receipt even
when an adapter normalized an upstream build receipt. It contains predecessor and
checkpoint hashes, request and authorization path/digest, authorization issuer/scope/
expiry and signature verification, exact release/candidate/build/deployment identities,
`action`, environment, target and idempotency key, exact operations, executor/tool
versions, start/end/observed time, external IDs, expected/actual state/digest, logs/raw
payload hashes, `result`, retry/reconciliation and rollback state, plus its own
canonical identity hash. A production success receipt has exactly `action: DEPLOY`,
`environment: production`, and `result: SUCCESS`; staging, canary, planned, inferred or
renamed receipts cannot satisfy that combination.

Timeout, transport loss, cancellation after dispatch, client interruption, missing
receipt or ambiguous external response becomes `OUTCOME_UNKNOWN` or
`TIMED_OUT_UNKNOWN`, never FAILED or SUCCESS. Freeze dependents. The only next action is
read-only `RECONCILE` using the same target/idempotency key and provider observation.
Never replay. Retry only after a receipt proves no mutation occurred, policy permits
the attempt, the same logical idempotency key plus declared attempt are used, and fresh
authority is obtained when any action field or authority expired. Resume only from a
verified predecessor checkpoint/receipt chain after re-hashing local inputs and
reconciling external state.

Canonical immutable controller paths are:

```text
production/releases/{release-id}/orchestration/{run-id}/
  manifests/{release-identity-sha256}.yaml
  checkpoints/{checkpoint-identity-sha256}.yaml
  actions/{action-id}/{action-receipt-identity-sha256}.yaml
  summaries/{summary-identity-sha256}.md
```

Each CREATE is absent-target, atomic no-replace, separately authorized, read-back
verified and hash-reported. Existing target or CAS drift writes nothing.

## Phase 9 — Staging, independent smoke, and production

`STAGE` requires GO/GO_WITH_ACCEPTED_RISK, exact run/action and fresh staging authority.
Only devops executes and receipts. A staging success does not authorize production.

After observed staging success, require an independently produced current persisted
canonical smoke receipt binding the staging action receipt, exact environment,
candidate/build/artifact/source/platform, current QA plan/test manifest, exact command/
runner/environment/times/log hashes, complete required scope, positive verdict and
handoff eligibility. Quick, targeted where full is required, stale, prior-build,
partial, warning-bearing, unavailable, unpersisted, timed-out or mismatched evidence
blocks promotion.

`PROMOTE` re-hashes all identities and external target state, then presents the exact
production action: current/previous/rollback artifact; migration/reversal/backup;
canary traffic stages/holds; numeric error/crash/latency/capacity/funnel thresholds,
queries/baselines/sample minima/cadence; kill switch and owner; action/idempotency/
timeout/retry/reconcile fields; and conditional rollback scope. Obtain new exact
production authority. Only devops executes. At every hold, missing/delayed/partial/
unknown/stale/breaching telemetry stops traffic increase and follows exact rollback
authority. Only verified observed production `SUCCESS` establishes `DEPLOYED`.

## Phase 10 — Publication barrier

Drafts may be separately file-authorized before deployment but are not publication.
`PUBLISH` requires verified production SUCCESS for the same artifact/target and any
policy-required initial health hold, plus a new exact publication authorization per
account/channel/region/message digest/action/idempotency key. Query existing state
before send. Only community-manager publishes and returns a receipt binding deployment,
message and external object identity. Unknown publication outcome reconciles before any
retry. Production and publication never run concurrently.

## Phase 11 — Deployment is not stabilization — TRL-013/TRL-014

Run states are `PREPARED`, `STAGING_AUTH_REQUIRED`, `STAGING_IN_PROGRESS`, `STAGED`,
`PRODUCTION_AUTH_REQUIRED`, `PRODUCTION_IN_PROGRESS`, `DEPLOYED`, `STABILIZING`,
`STABILIZED`, `POST_DEPLOY_DEGRADED`, `ROLLED_BACK`, `COMMS_PENDING`, `COMPLETE`,
`CANCELLED`, `BLOCKED`, `PARTIAL`, and `ERROR`.

Production success yields `DEPLOYED`, then `STABILIZING`; it never yields COMPLETE.
Required communication without verified publication yields `COMMS_PENDING`. A failed,
unknown or missing post-deploy signal, threshold breach, incident, rollback need, or
unverified external state yields `POST_DEPLOY_DEGRADED`, freezes rollout/publication,
and identifies exact rollback/reconciliation/communication authority needed. Use
`ROLLED_BACK` only after observing the exact previous artifact and recovery state.

`STABILIZE` is an independent later invocation after the complete policy window. When
policy requires 48 hours, accept no less than 48 elapsed hours. Require
`cgs.release-monitoring-receipt/v2` bound to production receipt/artifact/targets and
covering the whole window with query sources, sampling cadence/counts, raw hashes,
threshold observations, unknown intervals and incident/rollback state. A reminder,
scheduled job, future promise or dashboard summary is not elapsed evidence. Only full
coverage with all hard signals current/pass and no unknown interval yields STABILIZED.
COMPLETE additionally requires every required communication receipt or current
policy-authorized N/A. Post-deploy failure remains explicit; never silently report
COMPLETE.

## Terminal packet — TRL-018

Always return `cgs.team-release-result/v2` containing:

- every release/candidate/build/artifact/version/risk/policy/authority/instruction/
  evidence/gate/action identity;
- workflow, decision, run, action, recorder and stabilization states;
- ordered gate rows, hard blockers, original accepted-risk rows and acceptance hashes;
- dependency graph, risk routing, dispatch batches, live-slot arithmetic, timeouts,
  partial/unavailable evidence and accountable owners;
- staging, smoke, production, rollback, publication, monitoring, checkpoint and
  reconciliation receipt paths/hashes or `NOT_PROVIDED`;
- authority ledger, idempotency/attempt/retry state, non-writes and persistence target/
  hash or `NOT_WRITTEN`; and
- exactly one legal next action/owner, or `none`.

`BLOCKED` means a known unmet dependency/authority; `PARTIAL` means declared evidence
could not all be loaded; `ERROR` means invalid input or internal processing failure.
None grants permission. Stop after the packet. Never invoke an adjacent workflow or
continue into another action in the same invocation.
