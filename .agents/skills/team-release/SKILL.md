---
name: team-release
description: "Orchestrates one hash-bound release through evidence gates, separately authorized staging and production actions, verified deployment receipts, and post-release stabilization."
---

# Team Release

Use this workflow only when the caller supplies an exact orchestration manifest. It
coordinates release evidence and explicitly authorized actions; it does not turn a
file-write approval, a readiness verdict, a role label, or a prior approval into
permission to mutate a repository, deploy, or publish.

## Invocation

Accept exactly one mode:

~~~text
$team-release prepare --manifest <release-orchestration-manifest-path> --run-id <id> [--persist]
$team-release stage --run-manifest <path> --action-id <id>
$team-release promote --run-manifest <path> --staging-receipt <path> --smoke-receipt <path> --action-id <id>
$team-release publish --run-manifest <path> --deployment-receipt <path> --action-id <id>
$team-release reconcile --run-manifest <path> --action-id <id>
$team-release stabilize --run-manifest <path> --deployment-receipt <path> --monitoring-receipt <path>
~~~

Reject unknown or duplicate flags, missing values, directories, unsafe paths,
positional version names, and unrecognized modes. Never infer a version, release,
candidate, manifest, latest milestone, newest evidence, environment, account,
channel, action, or previous deployment. `run-id` and `action-id` are stable slugs
or UUIDs, not timestamps alone.

`prepare` is read-only unless `--persist` is supplied. The action modes operate only
on the exact immutable run manifest and receipts named by the caller. A single
invocation may stop at an authorization barrier; it must never cascade from
`prepare` through staging, production, and publication.

## Authority boundaries

Treat these as independent authority layers:

1. **Read-only inspection** — read and hash declared local evidence and external
   status that can be queried without mutation.
2. **File/report writes** — create only the previewed repository files. A bounded
   user request may already authorize those exact writes; otherwise preview the full
   changeset and obtain one approval before the first write.
3. **Repository mutation** — branch creation, version edits, commit, tag, push, or
   release-object mutation requires a separate explicit authorization naming every
   operation, repository/ref, source commit, expected resulting ref, artifact hash,
   and recovery point.
4. **Staging deployment** — requires a separate explicit authorization naming the
   action ID/idempotency key, target account/project/region/environment, exact
   candidate and artifact digest, operations, timeout, previous artifact, and
   rollback behavior.
5. **Production deployment** — requires a new explicit authorization after current
   staging and smoke evidence exists. It must name the production target, artifact,
   canary stages, health thresholds, kill switch, timeout, previous artifact,
   migration/rollback plan, and whether the exact conditional rollback is included.
6. **External communication/publication** — every send, store publication, social or
   community post, stakeholder message, and channel update requires a separate
   explicit authorization naming the account/channel/region, immutable message
   digest, action ID/idempotency key, timing, and recovery/correction plan.

Approval at one layer never carries to another layer or to another target, artifact,
action ID, retry, message revision, account, region, or environment. An external-action
authorization also does not authorize writing its local receipt; that receipt CREATE
must already be inside an exact file-write authorization or obtain one separately. A combined file
changeset approval never authorizes branch/tag/push/deploy/publish/send operations.
Silence, a phase-transition approval, `GO`, `LAUNCH_READY`, or prior deployment
permission is not action authorization.

Every authorization prompt must display the exact proposed action record and ask for
an explicit approve/decline response. A changed target, digest, plan, threshold,
message, or rollback point invalidates the authorization.

## Canonical coordination artifacts and unique writers

For persisted preparation, the controller owns only:

~~~text
production/releases/<release-id>/orchestration/<run-id>/run-manifest.md
production/releases/<release-id>/orchestration/<run-id>/snapshots/<snapshot-id>.md
production/releases/<release-id>/orchestration/<run-id>/summary.md
~~~

Never overwrite a prior artifact. A new state produces a new immutable snapshot.
`summary.md` may be created once at terminal stabilization or cancellation; progress
uses snapshots. Reject an existing target rather than replacing it.

Use a writer ledger before delegation. Exactly one role owns each output path:

| Artifact class | Unique writer |
|---|---|
| coordination run manifest/snapshots/final summary | team-release controller |
| release scope, version and candidate records | release-manager |
| build, tag, deployment, rollback and reconciliation receipts | devops-engineer |
| QA sign-off and regression execution receipt | qa-lead |
| technical sign-off | technical-director |
| security/privacy sign-off | security-engineer |
| multiplayer/network sign-off | network-programmer |
| performance/analytics sign-offs | their named domain owner |
| localization composite receipt | localization recorder validates separate source author, translator, locale reviewer, cultural/legal/platform owner, QA tester, and evidence reviewer receipts; no single role self-signs all axes |
| risk acceptance | policy-named risk owner and approver; the controller only verifies |
| communication draft and publication receipt | community-manager |

No two agents may write the same path, shared status file, manifest, or receipt.
Delegates may not edit the controller's artifacts. The controller must not edit
domain evidence or deployment receipts. If the required writer is unavailable, the
artifact remains `UNKNOWN`; do not transfer ownership silently.

## Status vocabulary

Report these fields independently:

| Field | Allowed values |
|---|---|
| `Workflow Status` | `COMPLETE`, `PARTIAL`, `BLOCKED`, `ERROR` |
| `Gate Evidence State` | `CURRENT`, `PARTIAL`, `STALE`, `UNKNOWN`, `INVALID` |
| `Gate Item Status` | `PASS`, `FAIL`, `UNKNOWN`, `NOT_APPLICABLE` |
| `Release Decision` | `GO`, `GO WITH ACCEPTED RISK`, `NO-GO`, `NOT DECIDED` |
| `Run State` | `PREPARED`, `STAGING_AUTH_REQUIRED`, `STAGING_IN_PROGRESS`, `STAGED`, `PRODUCTION_AUTH_REQUIRED`, `PRODUCTION_IN_PROGRESS`, `DEPLOYED`, `STABILIZING`, `STABILIZED`, `POST_DEPLOY_DEGRADED`, `ROLLED_BACK`, `COMMS_PENDING`, `COMPLETE`, `CANCELLED`, `BLOCKED`, `ERROR` |
| `Action State` | `NOT_STARTED`, `AUTHORIZED`, `IN_PROGRESS`, `SUCCEEDED`, `FAILED`, `TIMED_OUT_UNKNOWN`, `ROLLED_BACK`, `RECONCILED` |
| `Persistence` | `WRITTEN`, `NOT_REQUESTED`, `DECLINED`, `FAILED`, `NOT_ATTEMPTED` |

`COMPLETE` is allowed only after required stabilization evidence is current and
passing and every required external communication is either successfully receipted
or explicitly declared not applicable by current policy evidence. A successful
production deployment is `DEPLOYED` or `STABILIZING`, never immediately `COMPLETE`.
A partial report is useful progress, not a release permission.

## Phase 0: Validate one immutable release identity

Resolve every literal and real path. Reject dot segments, symlink escapes, malformed
or duplicate keys, unsupported schemas, and paths outside the project root. Read
raw bytes once and compute full lowercase SHA-256 digests.

Require the orchestration manifest to contain:

- `Artifact Type: release-orchestration-manifest`, schema version, stable release ID,
  semantic/display version, product/game ID, target date, regions and channels;
- exact release-candidate-manifest path/hash and release-policy path/hash;
- exact build-candidate manifest path/hash, candidate ID, build ID, build artifact
  path/hash, source commit, immutable version tag/ref, engine/toolchain version, and
  platform/configuration matrix;
- exact release-evidence-checklist path/hash;
- exact launch-candidate manifest and persisted launch-readiness assessment
  path/hash when launch policy makes them applicable;
- exact risk-manifest path/hash;
- ordered gate manifest with stable gate ID, required/optional condition, hard or
  advisory class, producer role, artifact type/schema/path/hash, candidate/platform
  binding, freshness/expiry rule, and pass/fail semantics;
- exact deployment plan path/hash, staging and production target identities,
  previous artifact/rollback point, migration plan, canary stages, health thresholds,
  kill-switch owner/method, and observation windows;
- exact communication plan path/hash with draft/message digests and publication
  targets, or current policy-authorized not-applicable evidence;
- ordered action registry with stable action IDs, idempotency keys, executor,
  timeout, retry budget, target, expected result, and reconciliation method;
- writer ledger, generation timestamp, owner, and applicable AGENTS.md path/hash
  chain.

A version tag must be a stable identifier permitted by the hash-bound release policy,
match the declared semantic version, bind the source commit/candidate, and pass an
existing-state collision check. A conflicting existing branch, tag, release object,
artifact, deployment, or publication is `BLOCKED` until reconciled; never select or
overwrite it.

Re-hash all declared identity artifacts and the applicable instruction chain. Any
mismatch, ambiguous release identity, dirty/unrecorded candidate, unsupported schema,
or missing policy yields `Workflow Status: BLOCKED`, `Release Decision:
NOT DECIDED`, and no mutable action.

## Phase 1: Lock the build and evidence dependency graph

The build artifact is the root of all candidate-dependent gates. Validate its local
bytes or a trusted build receipt binding artifact digest, source commit, build ID,
toolchain/container/configuration hashes, exact argv, timestamps, runner/job ID,
exit result, logs, SBOM, signature/provenance, and target platform matrix.

Do not start QA, performance, localization, analytics, security, privacy, network,
launch, staging smoke, or release decisions against a floating or unbuilt candidate.
If a new build is required, its exact repo writes and build-side mutations require
their applicable authorization. After the build receipt fixes the candidate identity,
freeze that identity; any rebuild creates a new candidate and invalidates dependent
evidence and prior action authorization.

Create a dependency plan in this order:

1. candidate/build identity and reproducibility receipt;
2. independent candidate-bound domain gates;
3. release and launch evidence normalization;
4. producer decision;
5. staging action;
6. current staging smoke evidence;
7. production authorization and action;
8. deployment receipt, monitoring, and separately authorized communication.

## Phase 2: Read the exact staged checklist contracts

Consume the declared release checklist only at:

~~~text
production/releases/<release-id>/<release-manifest-sha256>/release-checklist.md
~~~

Require `Artifact Type: release-evidence-checklist`, `Schema Version: 1`, exact
release-manifest/policy/candidate paths and hashes, the same candidate/build/artifact/
source/platform identity, `Persistence: WRITTEN`, and a verified report digest.
`Workflow Status: COMPLETE` means every item was normalized; it is not a release
verdict. Re-hash every transitive evidence dependency and independently apply the
declared release policy. `PARTIAL`, `BLOCKED`, unavailable, stale, invalid, or
mismatched evidence blocks every dependent hard gate.

When launch assessment is applicable, consume only the exact declared persisted
report at:

~~~text
production/releases/<release-id>/launch-readiness/<assessment-id>/report.md
~~~

Require the same launch-candidate and build identity, verified report bytes,
`Persistence: VERIFIED`, and `Launch Decision: NOT_RECORDED`. `LAUNCH_READY` is
positive readiness evidence, not permission to deploy. `LAUNCH_BLOCKED`, `ERROR`,
`UNDETERMINED`, partial hard evidence, or any hard `UNKNOWN`, `STALE`, or
`UNAVAILABLE` blocks. `CONCERNS` may proceed only through the narrowly scoped risk
acceptance rules below.

Never invoke either checklist workflow, choose a newest report, or infer a verdict
from file existence, counts, `Workflow Status`, or a role label.

## Phase 3: Resolve risk-driven gates and dispatch safely

The exact risk manifest must declare whether the product has online connectivity,
multiplayer/network authority, accounts/authentication, player or payment data,
telemetry/privacy scope, irreversible data migration, platform certification, legal
or ratings obligations, and external services. It must bind the release/candidate,
source policy, owner, timestamp, and digest.

Risk routing is deterministic:

- online, accounts, player/payment data, telemetry, or privacy scope requires current
  security and privacy evidence;
- multiplayer requires current network stability/load/reconnect/authority evidence;
- data/schema migration requires current migration rehearsal and rollback evidence;
- every target platform requires its declared certification/distribution evidence;
- analytics and critical-funnel evidence is required when the deployment plan uses
  those metrics as health thresholds.

Missing, unreadable, stale, or ambiguous risk data is treated conservatively as
high-risk: require the relevant gates and leave them `UNKNOWN` until current evidence
exists. Never silently skip a safety gate because of `full`, `lean`, `solo`, staffing,
time pressure, or missing files. Review modes may reduce advisory commentary only;
they never remove required gates.

### Concurrency budget

Read `.codex/config.toml` and use its configured `max_threads`. The root orchestrator
counts as one live thread. Before every dispatch, enumerate all live agents and
compute:

~~~text
available_child_slots = max(0, max_threads - live_threads_including_orchestrator)
~~~

With this repository's `max_threads = 6` and only the root active, at most five child
agents may run. If configuration is absent or invalid, dispatch serially. Reserve and
release slots explicitly; include nested delegation in the same global budget.
Delegates may not spawn children unless the controller assigns a bounded nested slot.

Batch only gates whose candidate and inputs are already fixed and which have no
producer/consumer or writer dependency. Never run build creation concurrently with
candidate-bound QA/performance/analytics. Never start phases 3 and 4 as one
unbounded batch. Gather every batch and record results before dispatching its
dependents.

Each delegation prompt names the release/candidate/build hashes, exact inputs, output
path, unique writer, read/write boundary, deadline, and required response schema.
Record `PASS`, `FAIL`, `UNKNOWN`, `TIMEOUT`, `ERROR`, or `CANCELLED` plus exact
artifact path/hash. A required timeout, partial response, missing artifact, agent
error, or unavailable writer is `UNKNOWN` and blocks; there is no generic “skip
agent” escape hatch. Produce a partial snapshot and identify the owner/evidence
needed.

## Phase 4: Assemble the gate manifest and independent sign-offs

For every ordered gate, verify the artifact's raw hash, artifact type/schema,
authorized producer, candidate/build/platform binding, timestamps/expiry, referenced
hashes, result semantics, and signature/identity receipt when required. Assign
exactly one item status; a missing or malformed sign-off is `UNKNOWN`, never PASS.

The gate manifest must list every required sign-off with its producer, path, hash,
state, dependencies, and policy class. When technical sign-off is required and no
current artifact exists, explicitly dispatch `technical-director` within the
concurrency budget to inspect the exact candidate and create only its assigned
artifact if that exact write is authorized. If it cannot be dispatched or the
artifact is missing, partial, stale, timed out, or hash-mismatched, the technical gate
is `UNKNOWN` and the release is `BLOCKED`. Do the same for every other required role;
never collect a sign-off from a role that was neither a verified producer nor an
explicitly dispatched owner.

For localization, require exact current localization manifest/freeze record,
source locale table/keyset/per-key hashes, target locale translations, independent
review receipts, font/glyph/UI-fit artifacts, cultural/legal/platform-owner
decisions, and build-bound QA/evidence receipts. Verify locale, candidate, build,
source, keyset, translation, asset, and evidence hashes. `QA PLAN READY`, an MT
draft, an unreviewed table, or one localization-lead statement is `UNKNOWN`, not PASS.

Human/platform approvals require a verifiable current attestation or external receipt
binding the stable gate IDs, release/candidate/build/platform, reviewed paths/hashes,
authorized identity/role or issuer, result, timestamp/expiry, and policy digest. The
model cannot sign, certify, grant not-applicable status, or substitute its judgment.

## Phase 5: Derive GO, risk acceptance, or NO-GO

Evaluate all hard gates before advisory gates.

The following blocker classes are non-waivable:

- any current open S1 Critical or S2 Major/High defect under the canonical policy;
- failed, unknown, stale, or missing security, privacy, legal, compliance, ratings,
  platform certification, or required multiplayer/network gate;
- wrong release/candidate/build/source/platform identity, artifact digest,
  signature, provenance, SBOM, or version/tag collision;
- irreversible or unrehearsed data migration, unknown production data impact, or
  missing migration reversal evidence;
- missing, unverified, or unusable rollback artifact/plan/owner;
- missing canary plan, observable health thresholds, monitoring, or kill switch;
- missing, partial, timed-out, stale, or invalid required QA, technical, producer, or
  other hard sign-off;
- failed or non-current staging smoke evidence at the later production-promotion checkpoint;
- any policy-declared non-waivable hard gate applicable at the current checkpoint.

Staging smoke is deliberately not part of the pre-staging release decision because it
does not exist until staging succeeds. It becomes a non-waivable hard gate only when
`promote` is evaluated. These blockers can only be fixed and re-evaluated or the release can be cancelled/deferred.
Do not offer an override option and do not accept prose justification as a bypass.

Only a policy-declared waivable advisory or allowed lower-severity finding may be
accepted. Require an immutable `release-risk-acceptance` artifact from the named
risk owner and approval authority, with finding IDs, original status, exact
release/candidate/build scope, rationale, expiry/review time, compensating controls,
residual risk, monitoring thresholds, rollback trigger/point, and identity
verification. Preserve the original finding and status. A valid acceptance changes
the decision only to `GO WITH ACCEPTED RISK`; it never turns the finding into PASS,
N/A, or `GO`.

Decision algorithm for the gates applicable at the current checkpoint:

1. any non-waivable FAIL/UNKNOWN, missing required gate, or invalid identity ->
   `NO-GO`, `Run State: BLOCKED`;
2. otherwise any unresolved hard FAIL/UNKNOWN -> `NO-GO`, `BLOCKED`;
3. otherwise any policy-waivable issue without valid acceptance -> `NO-GO`,
   `BLOCKED`;
4. otherwise any valid accepted issue -> `GO WITH ACCEPTED RISK`;
5. otherwise all required gates current and passing -> `GO`.

The producer may record the decision only from the complete gate table. A producer
decision does not authorize a repository mutation, deployment, rollback, publication,
or stakeholder message.

## Phase 6: Staging deployment action

`stage` requires `GO` or `GO WITH ACCEPTED RISK`, the immutable run manifest, a
registered staging action ID, and a fresh read-only existing-state check by its
idempotency key. Display the exact staging action record and obtain independent
staging authorization.

Only `devops-engineer` executes the authorized action. It must write an immutable
`deployment-action-receipt` containing schema/version, action ID/idempotency key,
authorization record digest, release/candidate/build/artifact/source identity,
target account/project/region/environment, prior artifact, exact operations,
start/end timestamps, executor and tool versions, result, external deployment/job
IDs, observed deployed artifact digest, logs/hashes, and rollback status.

Allowed result values are `SUCCESS`, `FAILED`, `ROLLED_BACK`, and `UNKNOWN`. A
timeout or lost response is `Action State: TIMED_OUT_UNKNOWN`; never replay it. Use
`reconcile` to query external state read-only by the same idempotency key and target,
then write a reconciliation receipt. Retry only after reconciliation proves no
mutation occurred and the policy permits another attempt; a retry uses the same
logical idempotency key plus the manifest-declared attempt number and requires new
authorization if any action detail changed.

A staging receipt is deployment evidence only. It does not authorize or prove
production deployment.

## Phase 7: Independent current staging smoke gate

After a verified staging `SUCCESS` receipt, obtain a new exact smoke receipt for the
deployed artifact. Accept only the manifest-declared canonical report:

~~~text
production/qa/evidence/smoke/<candidate-id>/<run-id>/report.md
~~~

Require `Artifact Type: smoke-check-receipt`, `Schema Version: 1`, exact
candidate-manifest path/hash and build/source/platform identity, persisted sprint
mode, `Verdict: PASS`, `Handoff Eligible: YES`, revalidated `QA Plan Effective
State: CURRENT`, exact test-manifest/scope/automated receipt/log/manual evidence
hashes, and an environment/deployment binding to the verified staging receipt,
target, and observed deployed artifact digest.

The staging smoke must be produced independently by the QA owner, after staging
success, and its timestamps must fall within the policy freshness window. Quick,
targeted, incomplete, warning-bearing, conversation-only, unpersisted, prior-build,
stale, partial, unavailable, timed-out, or mismatched smoke evidence blocks
production. Never ask for production authorization until this gate is current PASS.

## Phase 8: Human production confirmation and production action

`promote` must re-hash the run manifest, staging receipt, smoke receipt, release
policy, deployment plan, risk acceptances, rollback artifact, and exact build
artifact immediately before prompting. Abort if any byte or external target state
changed.

Show one production action record containing:

- release/version, candidate/build/source commit, artifact path and SHA-256,
  signature/provenance/SBOM verification;
- exact production account/project/region/environment and current deployed version;
- staging receipt and smoke receipt paths/hashes;
- previous production artifact and verified rollback artifact/path/hash;
- migration steps, data scope, reversibility proof, backup/checkpoint, and rollback
  ordering;
- canary/rollout stages with traffic percentages, hold durations, and owners;
- numeric error-rate, crash-rate, latency/capacity, and critical-funnel thresholds,
  their query sources, baseline windows, sample minimums, and evaluation cadence;
- automatic/manual kill-switch mechanism, authorized operator, and trigger;
- action ID/idempotency key, timeout, retry/reconciliation policy;
- whether the exact conditional rollback action is included in this authorization.

Obtain a new explicit production authorization. If conditional rollback is bundled,
it is authorized only for the named previous artifact, targets, threshold triggers,
and time window. Otherwise pause for separate rollback authorization unless immediate
safety policy already supplies verified authority.

Only `devops-engineer` executes canary stages. After each hold, verify the declared
metrics and receipt hashes. Do not increase traffic on missing, delayed, partial,
unknown, stale, or threshold-breaching telemetry. A breach activates the exact
authorized kill switch and rollback path; otherwise stop and request the required
authority.

Write an immutable production `deployment-action-receipt` with all staging receipt
fields plus every canary stage, planned/actual traffic, observation windows, sample
counts, threshold values/observations, decisions, kill-switch events, migration
results, deployed and previous artifact digests, and final result. Only verified
`Result: SUCCESS` with the observed production artifact digest establishes
`Run State: DEPLOYED`. `FAILED`, `UNKNOWN`, or timeout never does.

## Phase 9: Communication publication barrier

The community manager may create drafts before deployment only within an authorized
file changeset. Draft creation is not publication and must not imply that deployment
succeeded.

`publish` is allowed only after re-verifying an immutable production receipt with
`Result: SUCCESS`, matching candidate/artifact/target, and any policy-required
initial health hold. Re-hash the exact message bytes. Then display and obtain a
separate publication authorization for each action ID, idempotency key,
account/channel/region, message digest, timing, and correction/withdrawal plan.

Before sending, query existing external state by idempotency key and message digest.
Only `community-manager` publishes and writes an immutable
`communication-publication-receipt` with authorization digest, deployment receipt
digest, target account/channel/region, message digest, external object ID/URL,
timestamps, observed status, and verification payload/hash.

If production fails, rolls back, is unknown, or lacks a receipt, do not publish.
After a successful deployment with drafts but without authorization or verified
publication, use `Run State: COMMS_PENDING`. A publication timeout is unknown: first
reconcile external state and never blindly resend.

## Phase 10: Monitoring, rollback, and stabilization

After deployment, enter `STABILIZING`. Monitor for the policy-declared observation
window, which must be at least 48 hours when the release policy requires 48-hour
monitoring. Bind every sample to the production deployment receipt, query source,
time window, thresholds, and raw evidence hashes.

If any error/crash/funnel/security/capacity threshold breaches, a required signal
disappears, or evidence becomes partial/unknown:

1. set `Run State: POST_DEPLOY_DEGRADED`;
2. stop further traffic increases and publication actions not already completed;
3. execute only the exact authorized kill switch/rollback, or request the missing
   authority;
4. write deployment/rollback and reconciliation receipts;
5. use `ROLLED_BACK` only when the previous artifact is observed and verified;
6. issue corrective communication only through a new separately authorized
   publication action.

`stabilize` may produce `STABILIZED` only from a current monitoring receipt covering
the full required duration with all hard health thresholds passing, no unresolved
unknown interval, exact deployed artifact identity, and verified incident/rollback
state. Do not satisfy elapsed time by scheduling a reminder, predicting future
health, or using a pre-deploy dashboard snapshot.

Only after `STABILIZED` and required communications are verified may the controller
write the terminal summary and report `Run State: COMPLETE`.

## Failure, timeout, resume, and partial reporting

For an agent or evidence timeout, record what loaded, what did not, deadline,
attempt, dependency impact, and owner. Required `UNKNOWN`, `TIMEOUT`, partial, stale,
or unavailable evidence blocks its dependent phase. Never offer “skip and continue”
for a required safety, quality, staging-smoke, or authorization gate.

For an external action timeout or client interruption:

- preserve the immutable last snapshot and action ID/idempotency key;
- assume outcome `UNKNOWN`, not failed and not successful;
- run only read-only reconciliation first;
- compare observed remote object, target artifact digest, timestamps, and receipt;
- continue from verified state rather than replaying prior steps;
- require new authorization for changed actions or expired authority.

Always provide a partial snapshot/report even when blocked. Use `ERROR` for invalid
workflow inputs/internal processing failure, `BLOCKED` for a known unmet dependency
or missing authority, and `PARTIAL` when some declared evidence could not be loaded.
None of these states grants release permission.

## Persistence and final output

For `prepare --persist`, preview the exact controller-owned CREATE operations. Just
before writing, re-hash every declared input and verify every target is absent. Write
atomically, read back exact bytes, validate internal hashes/IDs, and return the path
and SHA-256. Declined or failed persistence produces no consumable run manifest.

Every response includes:

- release/version/candidate/build/artifact/source/platform identity;
- workflow, evidence, decision, run, action, and persistence states;
- current gate table with producer, artifact path/hash, status, and reason;
- non-waivable blockers and separately listed accepted risks;
- action authorization ledger and idempotency/reconciliation state;
- staging, smoke, production, rollback, publication, and monitoring receipt hashes;
- concurrency batches, timeouts, partial inputs, and exact accountable next owner;
- the next permitted mode, or `none`.

Updating `production/stage.txt`, milestone state, a release branch/tag, or any other
repository record is a separate exact file/repository mutation. It may occur only
after verifying the production receipt and obtaining its own applicable
authorization. Such a record is derived from the receipt; it is never proof that
deployment happened.
