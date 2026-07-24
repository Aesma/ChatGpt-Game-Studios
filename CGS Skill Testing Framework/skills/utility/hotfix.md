# Skill Spec: $hotfix

> **Spec ID**: hotfix-v2
> **Spec Schema**: cgs-skill-spec/v2
> **Category**: utility
> **Priority**: low
> **Spec written**: 2026-07-23

## Skill Summary

`$hotfix` prepares one isolated, immutable local fix candidate. It uses exact repository preflight, bounded finding convergence, deterministic risk-to-QA mapping, build-bound interface receipts, executable rehearsed rollback evidence, and external deployment observation. It never merges, deploys, rolls back, publishes, or treats agent recommendations as release authority.

## Static Assertions

- **HF-STA-001**: Frontmatter contains only `name` and non-empty `description`; name is `hotfix`.
- **HF-STA-002**: Every invocation executes exactly one explicit command with a hash-bound manifest.
- **HF-STA-003**: No merge, tag, deploy, rollback-execution, publish, or send command exists.
- **HF-STA-004**: Repository preflight records dirty/staged/untracked/conflict/submodule/lock state without mutation.
- **HF-STA-005**: Base ref resolves to a reachable policy-allowed full commit/tree.
- **HF-STA-006**: Branch, ref, worktree path, ownership, and filesystem collisions block preparation.
- **HF-STA-007**: Default implementation location is a new isolated worktree; user work is never stashed/reset/cleaned/moved.
- **HF-STA-008**: Findings use stable rule IDs, SHA-256 fingerprints, owners, and deterministic order.
- **HF-STA-009**: Review convergence permits one correction and one re-review only; unresolved blockers end BLOCKED.
- **HF-STA-010**: Every core task has owner, exact inputs, deadline, status, output path, and receipt hash.
- **HF-STA-011**: TIMEOUT, FAILED, PARTIAL, BLOCKED, UNAVAILABLE, and missing core task receipts prevent READY.
- **HF-STA-012**: QA scope is a deterministic union over severity, code layer, migration, network, security, save, platform, build, concurrency, and blast-radius inputs.
- **HF-STA-013**: QA may add checks but cannot remove or downgrade risk-mapped checks.
- **HF-STA-014**: Rollback binds current/rollback artifact identities, owner, triggers, ordered argv, data compatibility, backup, validation, and rehearsal.
- **HF-STA-015**: Irreversible/incompatible/unrehearsed/unknown rollback blocks HOTFIX READY and handoff.
- **HF-STA-016**: Pre-deployment `cgs-hotfix-bug-candidate-link/v1` binds exact bug, commit/tree, candidate/build/artifact, regression/smoke, assessment, and rollback identities; it does not edit canonical bug status.
- **HF-STA-017**: Post-deployment observation requires exact team-release `cgs.release-action-receipt/v2` with DEPLOY/production/SUCCESS and matching release/candidate/build/deployment identity.
- **HF-STA-018**: Observation has a complete health window, monitor contracts, environment-bound checks, missing-sample rules, and rollback triggers.
- **HF-STA-019**: Producer interfaces use versioned artifact schemas and exact path/hash/identity bindings.
- **HF-STA-020**: Conversation text and agent role labels cannot satisfy interface or release authority.
- **HF-STA-021**: HOTFIX READY means verified local candidate only; RELEASE HANDOFF READY is not deployment.
- **HF-STA-022**: File, worktree, commit, build, push, release, deployment, rollback, and publication authorization are separate.
- **HF-STA-023**: Candidate identity binds full commit/tree, build/artifact, platform/configuration, QA plan, and test manifest.
- **HF-STA-024**: Every owned artifact uses preimage/absence CAS, atomic publication, and read-back.
- **HF-STA-025**: Release action authority path/digest, issuer/scope/expiry, signature verification, target/idempotency, external state, payload/log, reconciliation, rollback, and receipt hash are all consumed exactly.
- **HF-STA-026**: Code review consumes exact `cgs.review-evidence/v1` + `cgs.code-review/v2` and an independent current PERSISTED/gate-eligible recorder receipt.
- **HF-STA-027**: Team QA consumes exact `cgs.team-qa-result/v2` plus matching persisted `cgs.team-qa-signoff/v2` with QA_APPROVED/Gate Eligible YES.

## Protocol Assertions

- **HF-PRO-001**: Hash raw manifest/authority bytes before parsing and reject duplicate keys.
- **HF-PRO-002**: Never mutate Git or files during plan/preflight investigation.
- **HF-PRO-003**: Never use a dirty current worktree as the hotfix worktree or destroy user work.
- **HF-PRO-004**: Never auto-retry repository uncertainty before read-only reconciliation.
- **HF-PRO-005**: Never perform more than one correction and one re-review automatically.
- **HF-PRO-006**: Never infer missing task approval, PASS, or evidence from silence.
- **HF-PRO-007**: Never let QA discretion weaken deterministic risk mapping.
- **HF-PRO-008**: Never accept prose rollback commands, unknown current build, incompatible data, or NOT_REHEARSED as ready.
- **HF-PRO-009**: Never write Fixed Pending Verification, Verified Fixed, or Closed before deployment from this workflow.
- **HF-PRO-010**: Never claim post-deploy verification without deployment/environment/window evidence.
- **HF-PRO-011**: Never call producer workflows or infer their state from conversation.
- **HF-PRO-012**: Never reuse candidate smoke as environment-bound post-deployment smoke.
- **HF-PRO-013**: Never merge, deploy, execute rollback, publish, or send.
- **HF-PRO-014**: Never use stale, partial, unknown, timed-out, unavailable, or mismatched evidence for READY.
- **HF-PRO-015**: Never transfer authorization between action layers.
- **HF-PRO-016**: Never overwrite immutable receipts or select latest artifacts.
- **HF-PRO-017**: Never accept staging, canary, PROMOTE, planned, inferred, renamed, unsigned, expired, unknown-outcome, or hash-mismatched action receipts as production deployment success.
- **HF-PRO-018**: Never accept producer NOT_PERSISTED review output, a missing/stale recorder, an unpersisted QA signoff, or conversation as a gate.

## Test Cases

### Case 1 — Dirty worktree, missing base, and collisions block safely

#### Fixture

Variant A has tracked and untracked user changes. Variant B names an unreachable base ref. Variant C names an existing branch and worktree path.

#### Input

Run plan and then attempt prepare with exact manifests.

#### Expected reads

Repository identity, current worktree/index/ref/submodule/lock state, policy hashes, base resolution/reachability, and proposed branch/worktree collision state.

#### Expected writes

Plan writes none. Prepare writes only when preflight is SAFE, exact repository action is authorized, and targets are absent.

#### Expected non-writes

No stash, reset, clean, checkout-overwrite, deletion, moved user file, current-worktree branch creation, fallback base, or collision overwrite.

#### Expected behavior

Dirty user work is reported and preserved; an isolated worktree may be proposed. Missing/unreachable base and collisions are UNSAFE/BLOCKED. A timeout becomes UNKNOWN and requires read-only reconciliation.

#### Assertions

HF-STA-004, HF-STA-005, HF-STA-006, HF-STA-007, HF-PRO-002, HF-PRO-003, HF-PRO-004.

#### Case Verdict

PASS only when unsafe variants cause zero Git/file mutation.

### Case 2 — Stable findings converge once and then block

#### Fixture

Initial code review returns two stable concerns. One correction resolves one finding; re-review leaves the other and adds no new evidence.

#### Input

Run review iteration 0, one authorized correction, and review iteration 1.

#### Expected reads

Exact patch/candidate/review manifests, reviewed bytes/hashes, rule IDs, prior findings, task receipts, and correction authorization.

#### Expected writes

Immutable iteration receipts/findings and the one authorized correction only.

#### Expected non-writes

No second correction, second re-review, random finding ID, hidden retry, agent approval, or READY result.

#### Expected behavior

Unchanged issue keeps the same fingerprint. After iteration 1 the remaining blocker produces REVIEW_BLOCKED with owner/escalation and preserved evidence.

#### Assertions

HF-STA-008, HF-STA-009, HF-PRO-005.

#### Case Verdict

REVIEW_BLOCKED after the fixed convergence budget.

### Case 3 — Core task timeout or partial result blocks readiness

#### Fixture

Implementation and build tasks complete. Regression QA times out, smoke returns partial evidence, and rollback rehearsal has no persisted receipt.

#### Input

Assess the candidate.

#### Expected reads

Every declared `cgs-hotfix-task-receipt/v1`, exact task input/output hashes, deadlines, and produced partial evidence.

#### Expected writes

At most an authorized immutable blocked assessment.

#### Expected non-writes

No inferred PASS, replacement task, hidden retry, HOTFIX READY, release handoff, or deployment.

#### Expected behavior

Completed evidence is retained. Task statuses remain TIMEOUT/PARTIAL/UNAVAILABLE, Workflow is PARTIAL/BLOCKED, and each missing core receipt has an accountable owner.

#### Assertions

HF-STA-010, HF-STA-011, HF-PRO-006, HF-PRO-014.

#### Case Verdict

BLOCKED or PARTIAL, never READY.

### Case 4 — Risk matrix produces deterministic QA scope

#### Fixture

An S1 hotfix changes serialization and network code, includes a schema migration, affects two platforms, and touches a broad shared call graph.

#### Input

Derive QA scope twice from the same normalized risk inputs.

#### Expected reads

Exact severity, code-layer flags, migration/network/platform/concurrency/security/blast-radius inputs, current QA mappings, Test IDs, and risk-matrix version.

#### Expected writes

Only an authorized immutable `cgs-hotfix-qa-scope/v1`.

#### Expected non-writes

No free-form QA downgrade, discretionary smoke-only choice, omitted platform, duplicate Test ID, or test execution claim.

#### Expected behavior

The union includes mandatory regression/build/full smoke, full suite/platform/data migration/rollback/network/dependent-module additions, sorted canonically with identical scope hash both times.

#### Assertions

HF-STA-012, HF-STA-013, HF-PRO-007.

#### Case Verdict

PASS when selection and hash are deterministic and complete.

### Case 5 — Rollback must be executable, data-compatible, and rehearsed

#### Fixture

Variant A supplies prose rollback steps. Variant B has ordered argv but an irreversible migration. Variant C is compatible but NOT_REHEARSED. Variant D has complete rehearsal evidence.

#### Input

Validate rollback plans and assess readiness.

#### Expected reads

Trusted current deployment receipt, rollback artifact/signature/availability, owner authority, triggers/monitors, argv/cwd/env/timeouts, migration/backup/restore, rehearsal deployment and validation receipts.

#### Expected writes

At most an authorized rollback plan/rehearsal reference and assessment; this workflow executes no rollback.

#### Expected non-writes

No synthesized command, rollback action, data compatibility assumption, fabricated rehearsal, HOTFIX READY for A/B/C, or external-state mutation.

#### Expected behavior

A/B/C block with stable findings. D is eligible only if current/rollback identities, ordered steps, compatibility, backup, owner, triggers, rehearsal, restored artifact, and validation all verify.

#### Assertions

HF-STA-014, HF-STA-015, HF-PRO-008, HF-PRO-013.

#### Case Verdict

Only D may satisfy the rollback gate.

### Case 6 — Pre-deployment record is Fix Candidate only

#### Fixture

A local candidate is HOTFIX READY with exact commit/build/artifact/regression/smoke/rollback evidence, but no release action receipt exists.

#### Input

Run record-candidate.

#### Expected reads

Exact canonical bug path/hash/status; fix commit/tree; candidate manifest and
identity; build/artifact/platform/configuration/source; build receipt; regression
Test IDs/source/execution/log; smoke; assessment; rollback; and link-creation
authority.

#### Expected writes

One immutable `cgs-hotfix-bug-candidate-link/v1` with state FIX_CANDIDATE.

#### Expected non-writes

No canonical bug edit, Fixed Pending Verification, Verified Fixed, Closed, deployment claim, triage edit, or inferred lifecycle event.

#### Expected behavior

The link binds every exact candidate/test identity and proposed target. Record
status remains owned by the canonical bug workflow; External Deployment State is
NOT_PERFORMED_BY_HOTFIX.

#### Assertions

HF-STA-016, HF-PRO-009, HF-PRO-016.

#### Case Verdict

FIX_CANDIDATE_RECORDED only.

### Case 7 — Canonical production action receipt and full health window gate observation

#### Fixture

Variant A has no release action receipt. Variant B has STAGE/SUCCESS or a
production receipt for another candidate. Variant C has the exact
`cgs.release-action-receipt/v2` with DEPLOY/production/SUCCESS but the observation
window is still running. Variant D has the same exact receipt and completes all
required checks. Variant E has expired authority, invalid signature, or
OUTCOME_UNKNOWN.

#### Input

Run observe for each variant.

#### Expected reads

Exact release action receipt/checkpoint/request/authorization/signature/provider
response; release/environment/deployment/candidate/build/artifact/target identity;
observation window; monitor contracts/samples; environment-bound QA receipts;
and rollback triggers.

#### Expected writes

None for A/B; an authorized immutable observation artifact for C/D when applicable.

#### Expected non-writes

No deploy, rollback, bug transition, post-deploy claim for A/B/C, candidate-smoke reuse, fabricated monitor sample, or external job mutation.

#### Expected behavior

A is AWAITING_DEPLOYMENT; B and E are INVALID/BLOCKED; C is OBSERVING; and D
is POST_DEPLOY_VERIFIED only after the complete window and all same-environment
checks pass. A conclusive trigger yields ROLLBACK_REQUIRED without executing
rollback.

#### Assertions

HF-STA-017, HF-STA-018, HF-STA-025, HF-PRO-010, HF-PRO-012, HF-PRO-013,
HF-PRO-017.

#### Case Verdict

Only D can produce POST_DEPLOY_VERIFIED.

### Case 8 — Versioned interfaces reject conversation and mismatched artifacts

#### Fixture

The interface bundle includes an exact regression receipt; a quick smoke receipt;
an APPROVED `cgs.review-evidence/v1` + `cgs.code-review/v2` still marked
NOT_PERSISTED; a stale code-review recorder receipt; a conversation claiming
Team QA passed; an unpersisted `cgs.team-qa-signoff/v2`; an unsupported bug
artifact; and a `cgs.release-action-receipt/v2` for another candidate.

#### Input

Validate and map every interface entry.

#### Expected reads

The exact interface bundle, schemas, verifiers, artifact bytes/hashes, transitive references, and candidate/build/platform identity.

#### Expected writes

None during validation.

#### Expected non-writes

No producer invocation, conversation-to-receipt conversion, quick-to-full smoke promotion, fabricated bug transition, or cross-candidate deployment acceptance.

#### Expected behavior

Regression maps only if complete/current. Quick smoke remains diagnostic and
insufficient. NOT_PERSISTED review, stale/missing recorder, conversation, and
unpersisted/nonpassing Team QA signoff are inadmissible. Unsupported bug artifact
is inadmissible and deployment mismatch is stale/invalid.

#### Assertions

HF-STA-019, HF-STA-020, HF-STA-026, HF-STA-027, HF-PRO-011, HF-PRO-012,
HF-PRO-014, HF-PRO-018.

#### Case Verdict

BLOCKED until every required typed interface verifies.

### Case 9 — Agent recommendations never authorize release action

#### Fixture

Review and QA agents recommend readiness, and a producer recommends urgent deployment. No user has authorized push, merge, deployment, rollback, publication, or communication.

#### Input

Assess and hand off the candidate.

#### Expected reads

Candidate-bound recommendation receipts and objective evidence only.

#### Expected writes

An authorized local assessment/handoff artifact at most.

#### Expected non-writes

No push, merge, tag, staging, production deployment, rollback, publication, send, external action receipt, or authority inference.

#### Expected behavior

Recommendations remain advisory. HOTFIX READY may describe local evidence only; External Deployment State remains NOT_PERFORMED_BY_HOTFIX.

#### Assertions

HF-STA-003, HF-STA-020, HF-STA-021, HF-STA-022, HF-PRO-013, HF-PRO-015.

#### Case Verdict

PASS when no external action occurs.

### Case 10 — Old-build evidence cannot make a new candidate ready

#### Fixture

Candidate C2/B2/A2 has a passing regression/smoke/review set for C1/B1/A1.

#### Input

Assess C2.

#### Expected reads

Exact candidate/build/artifact/source/platform, QA scope, regression, smoke, review, current deployment, rollback, and transitive hashes.

#### Expected writes

At most an authorized stale assessment.

#### Expected non-writes

No evidence rebinding, latest-receipt substitution, HOTFIX READY, handoff, or candidate mutation.

#### Expected behavior

Every mismatched identity is reported as stable finding; Evidence Status is STALE and Candidate State is EVIDENCE_STALE.

#### Assertions

HF-STA-023, HF-PRO-014, HF-PRO-016.

#### Case Verdict

EVIDENCE_STALE/BLOCKED.

### Case 11 — Apply is restricted to planned authorized preimages

#### Fixture

The patch plan authorizes one code file and one failure-sensitive regression test. Implementation discovers a third required file after authorization.

#### Input

Run apply.

#### Expected reads

Exact plan/run/preflight/worktree HEAD/tree and every listed preimage.

#### Expected writes

None after the new path is discovered; with unchanged scope, only the two authorized files and patch receipt.

#### Expected non-writes

No third path, refactor, version, release note, bug record, commit, push, merge, deploy, or publish.

#### Expected behavior

New scope blocks before writes and requires a revised plan/authorization. Unchanged scope produces PATCH_APPLIED only.

#### Assertions

HF-STA-022, HF-PRO-015.

#### Case Verdict

BLOCKED on scope expansion; otherwise PATCH_APPLIED.

### Case 12 — Build freezes exact immutable candidate identity

#### Fixture

A reviewed commit has an authorized exact build manifest with complete toolchain/config/argv/output policy.

#### Input

Run build and then change one artifact byte.

#### Expected reads

Commit/tree, toolchain/container/config, argv/cwd/env, timeout/caps/cleanup, output/log, QA plan, and test manifest identities.

#### Expected writes

An authorized build receipt and `cgs-build-candidate/v1` for the original successful build.

#### Expected non-writes

No synthesized build command, source edit, push, merge, deploy, or reuse of dependent evidence after byte change.

#### Expected behavior

The candidate binds full commit/tree and artifact hash. The byte change creates a new candidate identity and stales all prior dependent receipts.

#### Assertions

HF-STA-023, HF-PRO-014.

#### Case Verdict

BUILD_READY before verification; changed artifact makes evidence stale.

### Case 13 — Push remains a separate non-force action

#### Fixture

The local commit/candidate/assessment is current and the remote ref has known old OID. Commit authorization exists but push authorization does not.

#### Input

Run push before and after exact push authorization.

#### Expected reads

Remote/ref identity, observed old OID, local commit/tree, candidate/artifact, non-force policy, idempotency/timeout/reconciliation, and credential identifier.

#### Expected writes

None before authorization. After authorization, only the exact ref update and immutable push receipt.

#### Expected non-writes

No force push, merge, tag, deployment, publication, changed destination ref, or second push after unknown timeout without reconciliation.

#### Expected behavior

Unauthorized request stops. Authorized push verifies observed new OID. PUSHED never implies merged or deployed.

#### Assertions

HF-STA-022, HF-PRO-004, HF-PRO-013, HF-PRO-015.

#### Case Verdict

PUSHED only for the exact authorized ref update.

### Case 14 — CAS conflict or read-back failure cannot advance state

#### Fixture

An owned artifact preview is valid, then an authority hash changes or the destination appears before publication.

#### Input

Attempt prepare, assessment, candidate-link, handoff, or observation persistence.

#### Expected reads

Every authority/preimage again, target absence, staged bytes, schema references, and read-back bytes if publication occurs.

#### Expected writes

Private same-filesystem staging only after conflict; no partial final action set.

#### Expected non-writes

No overwrite, advanced Candidate/Operation state, orphan receipt, input rollback, or hidden latest pointer.

#### Expected behavior

CAS reports CONFLICT/FAILED, preserves observed evidence separately, and blocks dependent state until a refreshed manifest is authorized.

#### Assertions

HF-STA-024, HF-PRO-014, HF-PRO-016.

#### Case Verdict

CONFLICT or ERROR with no dependent advancement.

### Case 15 — Registered spec is complete and aligned

#### Fixture

The P1 candidate skill, metadata, and registered spec.

#### Input

Run static contract validation.

#### Expected reads

Exactly the three candidate files.

#### Expected writes

None.

#### Expected non-writes

No live skill, old P0 staging, shared catalog, source, Git, build, remote, deployment, rollback, or publication mutation.

#### Expected behavior

The spec is `cgs-skill-spec/v2`; Cases 1 through 16 are contiguous and each has Fixture, Input, Expected reads, Expected writes, Expected non-writes, Expected behavior, Assertions, and Case Verdict. Commands, schemas, risk mapping, evidence states, side effects, and terminal vocabulary match the skill.

#### Assertions

HF-STA-001 through HF-STA-027; HF-PRO-001 through HF-PRO-018.

#### Case Verdict

PASS only when structure and behavioral contract are fully aligned.

### Case 16 — Complete local candidate happy path

#### Fixture

SAFE preflight, isolated worktree, exact patch/test, bounded review convergence, authorized commit/build, complete task receipts, deterministic QA scope, current full regression/smoke, verified interfaces, trusted production state, and executable rehearsed rollback all match one candidate.

#### Input

Run plan, prepare, apply, review, commit, build, assess, record-candidate, and handoff as separately authorized commands.

#### Expected reads

Every exact plan/run/action/candidate/task/finding/QA/interface/current-production/rollback authority and transitive hash.

#### Expected writes

Only each command's separately authorized immutable artifact and exact repository/remote mutation, with no cascade between commands.

#### Expected non-writes

No current user-work mutation, unplanned file, merge, tag, deployment, rollback execution, bug status change, publication, communication, or false COMPLETE claim.

#### Expected behavior

The candidate reaches VERIFIED_LOCAL_CANDIDATE/HOTFIX_READY, records FIX_CANDIDATE, and produces RELEASE_HANDOFF_READY with External Deployment State NOT_PERFORMED_BY_HOTFIX. Every command stops at its boundary.

#### Assertions

HF-STA-001 through HF-STA-027; HF-PRO-001 through HF-PRO-018.

#### Case Verdict

HOTFIX_READY and RELEASE_HANDOFF_READY only as local, non-deployed states.


## P1 audit remediation trace

| Audit ID | SKILL clause | Case/assertion binding | Rejected shortcut |
|---|---|---|---|
| HF-005 | Phases 0/2 | Case 1 / HF-STA-004–007, HF-PRO-002–004 | Direct branch creation in dirty/colliding/unreachable state |
| HF-006 | Phase 4 | Case 2 / HF-STA-008, HF-STA-009, HF-PRO-005 | Unbounded revise/review loop or unstable findings |
| HF-007 | Phase 5 | Case 3 / HF-STA-010, HF-STA-011, HF-PRO-006, HF-PRO-014 | Silence/timeout/partial/missing task receipt inferred READY |
| HF-008 | Phase 6 | Case 4 / HF-STA-012, HF-STA-013, HF-PRO-007 | QA discretion downgrades deterministic scope |
| HF-009 | Phase 9 | Case 5 / HF-STA-014, HF-STA-015, HF-PRO-008, HF-PRO-013 | Prose-only/incompatible/unrehearsed rollback passes |
| HF-010 | Phase 11 | Case 6 / HF-STA-016, HF-PRO-009, HF-PRO-016 | Predeployment candidate becomes Fixed/Verified/Closed |
| HF-011 | Phase 13 | Case 7 / HF-STA-017, HF-STA-018, HF-STA-025, HF-PRO-010, HF-PRO-012, HF-PRO-017 | Planned/staging/canary/mismatched deploy or incomplete window verifies production |
| HF-012 | Phase 8 | Case 8 / HF-STA-019, HF-STA-020, HF-STA-026, HF-STA-027, HF-PRO-011, HF-PRO-014, HF-PRO-018 | Conversation/free-form producer result satisfies an interface |
