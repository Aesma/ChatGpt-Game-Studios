---
name: hotfix
description: "Builds an isolated, revision-bound hotfix candidate with deterministic QA scope, bounded review convergence, verified rollback, and deployment-receipt observation without merging or deploying."
---

# Hotfix

Treat revisions as supplied metadata; never calculate them from file content. Use stable business IDs, canonical paths, schema versions, explicit revisions, and UTC run IDs for identity and currentness.

## Purpose and terminal boundary

Prepare one immutable local hotfix candidate. The workflow separates investigation, isolated repository preparation, file mutation, review, commit, build, QA assessment, push, release handoff, and post-deployment observation into distinct commands and receipts.

Its strongest pre-release state is `HOTFIX READY`. It never merges, tags, deploys, executes rollback, publishes, sends communication, or treats an agent recommendation as release authority. Post-deployment work only consumes an exact external `cgs.release-action-receipt/v2`; without one, the state is `AWAITING DEPLOYMENT`.

## Explicit command grammar

Accept exactly one command per invocation:

~~~text
$hotfix plan --request-manifest {path} --request-revision {revision}
$hotfix prepare --action-manifest {path} --action-revision {revision}
$hotfix apply --run-manifest {path} --run-revision {revision}
$hotfix review --review-manifest {path} --review-revision {revision}
$hotfix commit --action-manifest {path} --action-revision {revision}
$hotfix build --action-manifest {path} --action-revision {revision}
$hotfix assess --assessment-manifest {path} --assessment-revision {revision}
$hotfix record-candidate --link-manifest {path} --link-revision {revision}
$hotfix push --action-manifest {path} --action-revision {revision}
$hotfix handoff --handoff-manifest {path} --handoff-revision {revision}
$hotfix observe --observation-manifest {path} --observation-revision {revision}
$hotfix status --run-manifest {path} --run-revision {revision}
~~~

Reject missing/unknown commands, positional bug/branch/environment guesses, unknown or duplicate flags, missing values, unsafe IDs/paths, absolute paths, globs, directory scans, and empty or malformed explicit revision values. There is no merge, tag, deploy, rollback-execution, publish, or send command. A request for one is rejected before reading project state.

## Versioned workflow and interface contract

Freeze:

~~~yaml template
schema: cgs-hotfix-workflow-contract/v2
inputs:
  request: cgs-hotfix-request/v2
  repo_preflight: cgs-hotfix-repo-preflight/v1
  patch_plan: cgs-hotfix-patch-plan/v2
  run_manifest: cgs-hotfix-run-manifest/v2
  review_manifest: cgs-hotfix-review-manifest/v1
  action_manifest: cgs-hotfix-action-manifest/v2
  assessment_manifest: cgs-hotfix-assessment-manifest/v2
  rollback_plan: cgs-hotfix-rollback-plan/v2
  review_envelope: cgs.review-evidence/v1
  review_extension: cgs.code-review/v2
  review_recorder_receipt: cgs.code-review-recorder-receipt/v1
  team_qa_result: cgs.team-qa-result/v2
  team_qa_signoff: cgs.team-qa-signoff/v2
  deployment_receipt: cgs.release-action-receipt/v2
outputs:
  task_receipt: cgs-hotfix-task-receipt/v1
  finding: cgs-hotfix-finding/v1
  qa_scope: cgs-hotfix-qa-scope/v1
  candidate_link: cgs-hotfix-bug-candidate-link/v1
  assessment: cgs-hotfix-assessment/v2
  handoff: cgs-hotfix-release-handoff/v2
  observation: cgs-hotfix-deployment-observation/v1
interface_bundle: cgs-hotfix-interface-bundle/v1
~~~

Unknown or incompatible schemas are blocking. Every artifact records the workflow-contract path/revision and canonicalization version.

## Independent state fields

Always report:

| Field | Values |
|---|---|
| `Workflow Status` | `COMPLETE`, `PARTIAL`, `BLOCKED` |
| `Operation Result` | `PLAN_READY`, `WORKTREE_READY`, `PATCH_APPLIED`, `REVIEW_READY`, `REVIEW_BLOCKED`, `COMMIT_CREATED`, `BUILD_READY`, `HOTFIX_READY`, `FIX_CANDIDATE_RECORDED`, `PUSHED`, `RELEASE_HANDOFF_READY`, `AWAITING_DEPLOYMENT`, `OBSERVING`, `POST_DEPLOY_VERIFIED`, `ROLLBACK_REQUIRED`, `NO_CHANGE`, `ERROR` |
| `Candidate State` | `UNPLANNED`, `PLANNED`, `PATCHED_UNCOMMITTED`, `COMMITTED_UNBUILT`, `BUILT_UNVERIFIED`, `VERIFIED_LOCAL_CANDIDATE`, `EVIDENCE_STALE` |
| `Evidence Status` | `VERIFIED`, `PARTIAL`, `STALE`, `UNKNOWN`, `UNAVAILABLE`, `INVALID` |
| `Mutation State` | `READ_ONLY_NO_CHANGES`, `WRITTEN`, `NOT_AUTHORIZED`, `CONFLICT`, `FAILED` |
| `External Deployment State` | `NOT_PERFORMED_BY_HOTFIX`, `AWAITING_RECEIPT`, `DEPLOYED_OBSERVED`, `UNKNOWN` |

`HOTFIX READY` means a locally verified candidate only. It never means complete, pushed, merged, deployed, rollback-safe in production, or published. `RELEASE HANDOFF READY` means only that an exact package can be consumed by the separate release owner.

## Canonical immutable artifact root

Use one stable Hotfix ID:

~~~text
production/hotfixes/{hotfix-id}/
  repo-preflight.json
  patch-plan.json
  run-manifest.json
  task-receipts/{task-id}.json
  findings/{finding-id}.json
  qa-scope.json
  patch-receipt.json
  review-receipt.json
  commit-receipt.json
  build-candidate.json
  build-receipt.json
  regression-receipt.json
  smoke-receipt.ref.json
  rollback-plan.json
  rollback-rehearsal-receipt.json
  assessment.json
  bug-candidate-link.json
  push-receipt.json
  release-handoff.json
  deployment-observation.json
~~~

Every writer owns one exact path. Every final target is absent unless a schema explicitly defines a version and existence conflict check projection. Never select latest files, overwrite immutable receipts, or let two roles write one artifact.

## Authority layers

Read-only investigation, worktree/branch creation, code/test writes, review artifacts, commit, build, push, merge/tag, deployment, rollback execution, publication, and communication are separate authority layers. Authorization at one layer does not transfer to another.

- `plan`, `assess`, and `status` are read-only.
- `prepare` requires an exact repository-action authorization.
- `apply` requires exact file-path/approved prior state authorization.
- `commit` requires an exact commit action authorization.
- `build` requires an exact executable action/output authorization.
- `push` requires an exact remote/ref authorization and never force-pushes.
- `record-candidate` requires exact local artifact authorization and never edits the canonical bug.
- `handoff` writes only when its one exact path is separately authorized.
- `observe` writes only an observation artifact and does not deploy or roll back.

Model or agent recommendations can never authorize repository or external actions.

## Phase 0: Read-only repository and bug preflight

`plan` first validates one exact canonical bug record or complete reproducible description. For a bug, require canonical path/revision, schema, stable Bug ID, severity, status, Repro Case ID, actual/expected result, and evidence references. Emergency planning accepts only policy-authorized severity, normally S1-Critical or S2-Major; this workflow does not change severity or priority.

Record `cgs-hotfix-repo-preflight/v1` with:
- repository root and identity;
- applicable instruction and repository-policy paths/revisions;
- current worktree path, branch/ref, full HEAD commit/tree;
- staged, tracked-modified, untracked, conflict, submodule, sparse-checkout, and lock state;
- exact base ref, resolved full commit/tree, reachability proof, and policy-allowed ancestry;
- proposed isolated branch and absolute worktree path;
- branch-name, ref, worktree-path, and ownership collision checks;
- filesystem/device suitability and cleanup/recovery owner;
- observed remote identifiers without fetch or mutation;
- inspection timestamp and raw command/output revisions where applicable.

Preflight states are `SAFE`, `UNSAFE`, and `UNKNOWN`.

A dirty current worktree is never stashed, reset, cleaned, checked out over, moved, or used as the hotfix worktree. Default to a new isolated worktree from the exact base commit. Existing branch/ref/worktree, missing or unreachable base, repository conflict/lock, unsafe path, unresolvable submodule, or UNKNOWN preflight blocks `prepare`. Investigation and preflight make zero byte and zero Git-state changes.

## Phase 1: Deterministic patch and action plan

Produce `cgs-hotfix-patch-plan/v2` with:
- Hotfix/Bug/Repro IDs and canonical bug path/revision;
- repository/base full commit/tree and preflight receipt revision;
- isolated branch/worktree proposal;
- every code/test/local-receipt path, approved prior state revision or `ABSENT`, unique writer, and intended change;
- explicitly excluded refactors, feature work, versions, generated noise, and release notes;
- required failure-sensitive regression Test ID/path/source revision;
- candidate build target and exact build/test/QA manifest paths/revisions;
- complete risk inputs and deterministic QA-scope result/revision;
- required tasks, owners, deadlines, output paths, and criticality;
- correction/review iteration budgets;
- current-production and rollback/rehearsal requirements;
- separate action registry for prepare/apply/review/commit/build/record-candidate/push/handoff/observe;
- plan expiry/currentness rules and revision.

Only after this read-only plan has exact patch paths/preimages may file writes be authorized. A newly required path, changed intent, new risk input, or approved prior state mismatch requires a new plan and authorization.

## Phase 2: Prepare only an isolated worktree

`prepare` revalidate the plan and reruns preflight. Its action manifest binds action/idempotency ID, repository identity, base full commit/tree, exact new branch/ref and worktree path, expected absence, executor, timeout, recovery owner, and receipt destination.

After exact repository-action authorization:
1. acquire only the declared repository lock;
2. revalidate SAFE preflight and target absence;
3. create only the named branch/worktree from the exact base commit;
4. verify observed HEAD/tree/ref/worktree registration and clean isolated state;
5. publish the immutable receipt and read it back.

A busy lock, timeout, interrupted result, branch collision, path collision, or changed base yields `UNKNOWN`, `CONFLICT`, or `BLOCKED`. Reconcile read-only before any retry. Do not delete a failed worktree, modify current user work, create code files, commit, or push in this command.

## Phase 3: Apply only the exact authorized patch

`apply` requires WORKTREE_READY, the exact run/plan/preflight revisions, and authorization for each path/approved prior state/intended change. revalidate isolated HEAD/tree and every approved prior state.

Apply only the minimal fix and its failure-sensitive regression test. Stop before any write if a new file or scope is required. Never refactor, update versions, edit the canonical bug, commit, push, merge, deploy, or publish.

The patch receipt records every path, pre/post revision, normalized diff revision, test-source revision, writer, timestamps, and actual result. `PATCH_APPLIED` means only the isolated files changed as authorized.

## Phase 4: Stable findings and bounded correction convergence

Every review, QA, rollback, or interface issue uses `cgs-hotfix-finding/v1`. Record its stable finding key from:
`workflow-contract revision | Hotfix ID | candidate/plan revision | reviewed artifact revision | rule ID | stable subject | expected value | observed value`.

Finding ID is `HF-F-{rule-id}-{stable-subject-id}` and stores the stable finding key, severity `BLOCKER|MAJOR|MINOR|INFO`, owner, artifact references, remediation condition, first-seen iteration, and current state. Sort by severity, rule ID, subject, then finding key. Unchanged business IDs preserve identical finding IDs and order.

The convergence budget is exact:
1. initial review produces review iteration 0;
2. if result is CONCERNS or REJECT, at most one authorized correction round may address declared findings only;
3. exactly one re-review iteration 1 evaluates the new immutable patch/candidate bytes;
4. any remaining blocking finding, new blocking finding, missing receipt, or REJECT returns `REVIEW_BLOCKED`.

There is no second correction or automatic retry. Escalate remaining findings to the named human/technical owner with preserved receipts. A model recommendation remains advisory.

## Phase 5: Bounded task and delegate receipts

Every assigned implementation, review, build, regression, smoke, rollback, or observation task has a `cgs-hotfix-task-receipt/v1` binding Task ID, owner identity/role, exact inputs/revisions, allowed operations, output path, start/deadline/end, status, and result revision.

Task status is `COMPLETE`, `TIMEOUT`, `FAILED`, `PARTIAL`, `BLOCKED`, or `UNAVAILABLE`. No response is UNKNOWN and is represented as UNAVAILABLE with the missing receipt named. Completed partial evidence is preserved.

Core tasks are implementation patch, code review, candidate build, failure-sensitive regression execution, full smoke execution, rollback ownership/rehearsal, and deployment observation when applicable. Any missing, timed-out, failed, partial, unpersisted, or mismatched core receipt blocks HOTFIX READY or post-deployment verification. Do not infer approval or PASS and do not launch an unplanned replacement task.

## Phase 6: Derive deterministic QA scope

The plan records all risk inputs with values `YES`, `NO`, or `UNKNOWN`:
- canonical severity S1 or S2;
- code layer: content/UI, gameplay, engine/core, serialization/save, network, security/auth, platform, build/toolchain;
- data/schema/save migration;
- network protocol or service compatibility;
- security/privacy/permission impact;
- concurrency/timing impact;
- platform-specific behavior and affected platform matrix;
- external API/service impact;
- rollback/data compatibility;
- blast radius and shared-call-graph breadth.

UNKNOWN in any applicable risk input blocks scope finalization.

Start with mandatory:
- exact failure-sensitive regression Test ID;
- build integrity/launch test;
- persisted full sprint smoke for the candidate;
- exact affected platform/configuration.

Then union every matching row:

| Risk predicate | Required additions |
|---|---|
| Severity S1 | full regression suite, all release-policy platforms, data-integrity baseline, extended health checks |
| Severity S2 | affected-module suite and every candidate target platform |
| engine/core or concurrency | full suite, stress/soak scope, shutdown/recovery and performance baseline |
| serialization/save or migration | old/new save compatibility, forward/backward migration, rollback/restore, corruption and data-integrity tests |
| network/external service | client/server compatibility, reconnect, latency/loss, multi-client, protocol-version and service-contract tests |
| security/auth/privacy | permission/auth negative cases, secrets/privacy checks, abuse and audit-log tests |
| platform-specific | exact affected device/OS/config plus the policy baseline comparison platform |
| build/toolchain | clean rebuild, packaging/install/launch, signature/provenance and artifact-integrity tests |
| broad shared call graph | every mapped dependent module suite from the current QA plan |

Normalize stable Test/Check IDs, sort bytewise, reject duplicates/conflicts, and record `qa_scope_revision`. QA may add checks with a reason but may not remove or downgrade a mapped requirement. A discretionary smoke/targeted/full choice cannot replace this matrix.

## Phase 7: Commit and build as separate actions

`commit` requires the exact patch and review state, expected diff, staged path/blob set, parent full commit/tree, commit message records/revision, author/executor, signing policy, receipt path, and explicit commit authorization. Stage only listed paths, create one commit, then verify full commit/tree/parent/message/signature and clean isolated state. COMMIT_CREATED does not mean pushed, built, tested, or ready.

`build` requires an exact action manifest with ordered argv array, cwd, environment allowlist, toolchain/container/config revisions, timeout/output limits, process cleanup, output destinations, and explicit authorization. Never synthesize commands.

The build receipt and `cgs-build-candidate/v1` bind full source commit/tree, candidate/build/artifact IDs and revision, platform/configuration, toolchain, argv, timestamps, runner/job, exit code, complete log revision, QA-plan revision, test-execution-manifest revision, signature/provenance/SBOM when required, and read-back revisions. Any rebuild or declared artifact revision change creates a new candidate and stales dependent evidence.

## Phase 8: Consume only versioned interface artifacts

The run manifest contains `cgs-hotfix-interface-bundle/v1`. Each interface entry has producer, schema, exact path/declared revision, candidate/build/artifact/source/platform binding, status mapping, freshness rule, and verifier.

| Producer contract | Accepted artifact | Hotfix mapping |
|---|---|---|
| build owner | `cgs-build-candidate/v1` + `cgs-build-receipt/v1` | success only when exact artifact and source verify |
| review owner | `cgs.review-evidence/v1` + `cgs.code-review/v2` + independent `cgs.code-review-recorder-receipt/v1` | only current APPROVED, PERSISTED, gate-eligible exact envelope/extension satisfies review |
| QA scope owner | `cgs-hotfix-qa-scope/v1` | exact scope revision only; selection does not prove execution |
| regression runner | `cgs-regression-execution-receipt/v2` | only exact current complete PASS satisfies regression |
| smoke runner | `cgs-smoke-check-receipt/v2` | only persisted sprint PASS with handoff YES and exact scope/build satisfies candidate smoke |
| QA coordinator | `cgs.team-qa-result/v2` + persisted `cgs.team-qa-signoff/v2` | only exact current QA_APPROVED, Gate Eligible YES, persisted signoff satisfies QA evidence |
| bug owner | `cgs-bug-transition-event/v2` | records external canonical bug transition only; hotfix does not fabricate it |
| release owner | `cgs.release-action-receipt/v2` | only `DEPLOY`/`production`/`SUCCESS` with exact release/candidate/build/deployment authority and revisions may start observation |
| observation owner | `cgs-hotfix-deployment-observation/v1` | proves only its complete health window and bound deployment |

Unknown schemas, missing verifiers, unsupported versions, unreadable bytes, partial/unpersisted artifacts, or revision/identity mismatch map to PARTIAL, UNKNOWN, STALE, UNAVAILABLE, or INVALID and block dependent results. Never parse conversational text or invoke the producer workflow.

For code review, revalidate the generic envelope and embedded extension plus every
stale-key input. The producer's own NOT_PERSISTED/gate-ineligible fields never
satisfy HOTFIX READY; the independent recorder receipt must name the same raw
path/revision, record `RECORDED|ALREADY_RECORDED`, PERSISTED and gate eligible true,
and bind recorder authority, registry final revision, version and existence conflict check/atomicity and read-back.
For Team QA, revalidate result/signoff and require matching request/run/scope,
candidate/build/artifact/source/plan/evidence/review identities,
`QA_APPROVED`, Gate Eligible YES, and verified signoff persistence. Missing or
unknown recorder/signoff, any mismatch, and free text fail closed.

## Phase 9: Verify rollback executability and rehearsal

`cgs-hotfix-rollback-plan/v2` binds:
- trusted current-production-state receipt with account/project/region/environment, deployment ID, build/artifact/source identities, issuer, query time, and raw response revision;
- exact rollback build/artifact path/revision, signature/provenance, availability, and retention;
- rollback owner/operator identity and authority reference;
- objective trigger IDs, threshold values/units, monitors, decision deadline, and escalation path;
- kill switch plus ordered rollback argv arrays, cwd, environment allowlist, credentials identity without secrets, timeouts, output caps, cleanup, and expected external state transitions;
- data/save/schema migration IDs, forward/backward compatibility, irreversible operations, backup/checkpoint paths/revisions, restore procedure, and validation;
- ordered post-rollback health, data-integrity, smoke, and regression checks;
- rehearsal environment/deployment ID, start/end, exact steps, observed restored artifact, validation receipts/logs/revisions, result, and rehearsal receipt revision.

A prose command, shell string, branch/tag/dashboard label, unknown current artifact, missing rollback bytes/owner/triggers/validation, unavailable backup, incompatible data/save/schema, irreversible migration, NOT_REHEARSED, partial rehearsal, or stale revision blocks HOTFIX READY and RELEASE HANDOFF READY. This workflow never executes rollback.

## Phase 10: Assess one immutable local candidate

`assess` revalidate plan/run/preflight/patch/review/commit/build/candidate, QA scope, task receipts, regression, smoke, current-production, rollback, rehearsal, and interface bundle.

Return HOTFIX READY only when:
1. repository preflight and isolated worktree receipts verify;
2. authorized patch and commit contain exactly planned paths;
3. build candidate and artifact bind the exact full commit/configuration;
4. bounded review convergence has no blocking finding;
5. every core task receipt is COMPLETE;
6. deterministic QA scope is complete and every required execution receipt is current conclusive PASS;
7. candidate-bound full sprint smoke is persisted PASS with handoff YES;
8. every interface artifact and transitive revision verifies;
9. current production identity is trusted and current;
10. rollback artifact, executable steps, data compatibility, backup, owner, trigger, rehearsal, and validations verify;
11. no required state is partial, stale, unknown, timed out, unavailable, invalid, or mismatched.

Otherwise return REVIEW_BLOCKED, PARTIAL, BLOCKED, or EVIDENCE_STALE with stable Finding IDs and accountable owners. External Deployment State remains NOT_PERFORMED_BY_HOTFIX.

## Phase 11: Record a build-bound Fix Candidate, not a fixed bug

`record-candidate` creates `cgs-hotfix-bug-candidate-link/v1` only after HOTFIX READY. It binds Bug/Hotfix IDs; canonical bug path/revision/status; fix full commit/tree; candidate manifest ID/path/revision and candidate-identity revision; build ID plus build-receipt path/revision; artifact path/revision, platform/configuration and source identity; exact regression Test IDs/source revisions/execution-receipt/log paths/revisions; smoke scope/receipt; assessment and rollback plan/rehearsal paths/revisions; proposed deployment targets; creation owner/time; canonical link revision; and state `FIX_CANDIDATE`.

It does not edit the canonical bug record, write `Fixed Pending Verification`, `Verified Fixed`, or `Closed`, or claim deployment. The link is an immutable candidate relationship, not a bug lifecycle transition. The authorized `$bug-report record-fix-candidate` recorder may consume it; a later exact release action receipt and observation package for the same candidate may be consumed by the canonical bug owner.

## Phase 12: Push and release handoff remain non-release actions

`push` requires exact remote/ref, expected old OID or ABSENT, local full commit/tree, non-force policy, action/idempotency ID, timeout, reconciliation procedure, credential/account identifier, receipt destination, and explicit push authorization. Never force-push. Query observed remote OID after execution. Timeout/unknown response must be reconciled read-only before retry. PUSHED does not mean merged or deployed.

`handoff` consumes HOTFIX READY and policy-required push receipt. Its `cgs-hotfix-release-handoff/v2` binds every input path/revision and explicitly lists merge, tag, staging, production, rollback execution, publication, and communications as not performed. It contains exact target refs/environments, candidate identity, deterministic QA scope, rollback plan/rehearsal, unresolved risks, and required next-owner actions.

## Phase 13: Observe only an externally completed deployment

`observe` consumes one exact canonical `cgs.release-action-receipt/v2` produced by
team-release and one observation manifest. If no verified external receipt exists,
return:
- Operation Result: AWAITING_DEPLOYMENT;
- External Deployment State: AWAITING_RECEIPT;
- Mutation State: READ_ONLY_NO_CHANGES;
- no health or bug-verification claim.

A valid receipt must have exactly `action: DEPLOY`, `environment: production`,
and `result: SUCCESS`. It binds and revalidates predecessor/checkpoint revisions;
request and authorization path/identifier; authority issuer/scope/expiry and signature
verification; exact release, candidate identity, build, deployment, source commit,
artifact and target identities; idempotency key and exact operations; executor/tool
versions; start/end/observed times; external IDs; expected/actual state/identifier;
logs/raw-payload revisions; retry/reconciliation/rollback state; and its canonical
identity revision. The observed candidate/build/artifact/deployment must join the
hotfix release handoff and observation manifest exactly.

A staging, canary, PROMOTE, planned, inferred, renamed, unsigned, expired-authority,
revision mismatched, `OUTCOME_UNKNOWN`, or `TIMED_OUT_UNKNOWN` receipt is not deployment
success and cannot start or complete observation.

The observation manifest binds:
- deployment/environment/candidate identities;
- health-window start, minimum duration, planned end, and completeness;
- stable monitor IDs, queries, thresholds, units, cadence, missing-sample policy, and raw receipt revisions;
- environment/deployment-bound smoke, regression, data-integrity, migration, performance, security, and platform checks required by QA scope;
- rollback trigger IDs and owner;
- intended immutable observation path.

Before the window ends, return OBSERVING. Missing samples, unavailable monitor, stale receipt, wrong environment/artifact, or partial window remains PARTIAL/UNKNOWN and cannot verify.

Return POST_DEPLOY_VERIFIED only when the full window completed, exact deployed artifact remained observed, every required environment-bound check conclusively passed, no rollback trigger fired, and the immutable observation receipt read-back verifies. Return ROLLBACK_REQUIRED when a conclusive trigger fires, with exact trigger/evidence/owner, but do not execute rollback. Produce an exact observation package for the canonical bug owner; do not transition the bug yourself.

## Phase 14: version and existence conflict check persistence and final response

For each owned artifact:
1. preview exact path, operation, approved prior state/ABSENT, byte count, rendered revision, authorization layer, and non-writes;
2. revalidate every authority and input immediately before mutation;
3. stage on the same filesystem;
4. validate schema, stable findings, references, and transitive revisions;
5. version and existence conflict check unchanged inputs and expected destination;
6. atomically publish the exact action set;
7. read back and revision every member.

On conflict, timeout, partial write, or read-back mismatch, preserve observed evidence/results but report Mutation State CONFLICT/FAILED and do not advance dependent state.

Always report exact command, Workflow/Operation/Candidate/Evidence/Mutation/External Deployment states, repository/base/commit/tree, candidate/build/artifact/platform identities, action authorization ledger, task/finding/QA-scope/rollback/interface states, actual side effects and receipt revisions, partial/timeout/unknown items, next accountable owner, and one next permitted command or none.

Never say hotfix complete, merged, deployed, rolled back, or published from local candidate evidence or agent advice.


## P1 audit traceability

This table binds the sealed hotfix semantics to exact cases/assertions; it grants no new action authority.

| Audit ID | Enforcing SKILL clause | Dedicated spec case and assertions |
|---|---|---|
| HF-005 | Phase 0 + Phase 2 — dirty/staged/untracked/conflict/submodule/lock, reachable base, branch/ref/worktree ownership/collision preflight; isolated worktree only | Case 1; HF-STA-004–HF-STA-007, HF-PRO-002–HF-PRO-004 |
| HF-006 | Phase 4 — stable finding IDs/finding keys and exactly one correction plus one re-review; unresolved blockers end BLOCKED | Case 2; HF-STA-008, HF-STA-009, HF-PRO-005 |
| HF-007 | Phase 5 — each core task has owner/inputs/deadline/status/output/receipt; timeout/failure/partial/unavailable/missing blocks READY | Case 3; HF-STA-010, HF-STA-011, HF-PRO-006, HF-PRO-014 |
| HF-008 | Phase 6 — deterministic union over severity/layer/migration/network/security/save/platform/build/concurrency/blast radius; QA may add but not subtract | Case 4; HF-STA-012, HF-STA-013, HF-PRO-007 |
| HF-009 | Phase 9 — rollback binds artifact identities, owner, triggers, ordered argv, data compatibility/backup/validation and rehearsal; unknown/irreversible blocks | Case 5; HF-STA-014, HF-STA-015, HF-PRO-008, HF-PRO-013 |
| HF-010 | Phase 11 — predeployment output is exact build-bound `cgs-hotfix-bug-candidate-link/v1`; hotfix never edits canonical bug status | Case 6; HF-STA-016, HF-PRO-009, HF-PRO-016 |
| HF-011 | Phase 13 — only matching Team Release DEPLOY/production/SUCCESS receipt plus complete environment health window supports observation; otherwise AWAITING DEPLOYMENT | Case 7; HF-STA-017, HF-STA-018, HF-STA-025, HF-PRO-010, HF-PRO-012, HF-PRO-017 |
| HF-012 | Phase 8 — smoke/team-QA/bug interfaces are exact versioned path/revision/identity artifacts with deterministic mappings; conversation and agent labels are invalid | Case 8; HF-STA-019, HF-STA-020, HF-STA-026, HF-STA-027, HF-PRO-011, HF-PRO-014, HF-PRO-018 |
