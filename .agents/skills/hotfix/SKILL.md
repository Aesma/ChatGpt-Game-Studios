---
name: hotfix
description: "Builds an immutable, locally verified hotfix candidate through read-only investigation, separately authorized patch/repository actions, build-bound regression and smoke evidence, and rollback-safe release handoff without merging, deploying, or publishing."
---

# Hotfix

## Invocation and command boundary

This workflow is explicit-invocation only. Never start it from context matching or
invoke another workflow automatically.

Use one command:

`$hotfix plan <BUG-ID|description>`  
`$hotfix prepare --plan <path> --action-id <id>`  
`$hotfix apply --run-manifest <path>`  
`$hotfix commit --run-manifest <path> --action-id <id>`  
`$hotfix build --run-manifest <path> --action-id <id>`  
`$hotfix assess --candidate <path> --regression <path> --smoke <path> --current-deployment <path> --rollback <path>`  
`$hotfix record-bug --assessment <path>`  
`$hotfix push --run-manifest <path> --action-id <id>`  
`$hotfix handoff --run-manifest <path>`

Reject missing/unknown modes, duplicate flags, missing values, directories, unsafe
paths, malformed IDs, and positional branch/version/environment guesses. A single
invocation performs one command and stops. There is no merge, deploy, rollback,
publication, or communication-send command in this skill.

## Non-negotiable contract

1. **Local candidate only** — `HOTFIX READY` means one immutable candidate was
   locally assessed against exact build, regression, smoke, current-deployment, and
   rollback evidence. It does not mean committed unless a commit receipt exists,
   pushed, merged, staged, deployed, published, complete, or safe to release.
2. **Separate authority layers** — Read-only investigation, worktree/branch creation,
   code/report writes, commit, build, push, merge/tag, staging deployment, production
   deployment/rollback, and publication are distinct actions. Authority at one layer
   never transfers to another.
3. **No model release authority** — Lead programmer, QA, producer, or other agent
   output is an evidence-bound recommendation only. No role label, recommendation,
   readiness result, or conversational phase approval authorizes repository mutation,
   push, merge, deploy, rollback, publish, or send.
4. **Immutable candidate identity** — Every candidate fixes one full source commit,
   build ID, build artifact path and SHA-256, platform/configuration, candidate
   manifest path/hash, QA-plan hash, and test-manifest hash. Any commit, rebuild,
   artifact-byte, configuration, or manifest change creates a new candidate and
   invalidates prior dependent receipts.
5. **Failure-sensitive regression required** — Every bug fix includes an automated
   regression test that would fail on the original defect. Its receipt binds the bug,
   repro case, test ID/path/source hash, fix commit, candidate/build/artifact hashes,
   exact argv, runner/config, timestamps, exit code, complete log hash, and result.
   Manual verification and a generic related suite cannot replace it.
6. **Canonical smoke evidence** — `HOTFIX READY` requires the staged smoke-check
   `smoke-check-receipt` for the same candidate, persisted sprint mode,
   `Verdict: PASS`, `Handoff Eligible: YES`, current QA-plan state, and matching
   transitive hashes. Quick/targeted, warning-bearing, incomplete, unpersisted,
   stale, prior-build, or hash-mismatched smoke evidence is insufficient.
7. **Verified rollback and current build** — The rollback plan binds the exact
   currently deployed production artifact/build hash from a trusted current-state
   receipt, the exact previous/rollback artifact hash, owner, triggers, steps,
   data/schema compatibility, backup/checkpoint, verification, and rehearsal status.
   Missing current identity, unverifiable rollback bytes, or irreversible migration
   blocks release handoff.
8. **Canonical bug transition** — This workflow may only propose
   `Open → Fixed Pending Verification` in
   `production/qa/bugs/<BUG-ID>.md` after the immutable fix commit/build and passing
   regression receipt exist. It never writes `Verified Fixed` or `Closed`; staged
   `bug-report` owns those evidence-gated transitions.
9. **Investigate before authorizing writes** — `plan` is byte-level and Git-state
   read-only. It determines the complete patch scope and preimage hashes first.
   Only then may `apply` use one exact file-write authorization. A discovered new
   path, changed patch intent, or preimage mismatch requires a revised plan and new
   authorization.
10. **No false terminal state** — Never output `HOTFIX COMPLETE`, `MERGED`,
    `DEPLOYED`, `ROLLED BACK`, or `PUBLISHED` without the separate owning workflow's
    verified external receipt. This skill's strongest local state is `HOTFIX READY`;
    its strongest handoff state is `RELEASE HANDOFF READY`.

## Authority layers and receipts

| Layer | This skill command | Required authorization | Success receipt/state |
|---|---|---|---|
| read-only investigation | `plan`, `assess`, `handoff` | none | hash-bound report; no mutations |
| isolated branch/worktree | `prepare` | explicit repository-action record | worktree/branch receipt |
| code/test/hotfix-record file writes | `apply` | exact path/operation/preimage changeset | patch receipt |
| commit | `commit` | explicit repository-action record | commit receipt and full SHA |
| build | `build` | explicit build action/output manifest | build receipt and build-candidate manifest |
| push | `push` | explicit remote/ref action record | push receipt with observed remote OID |
| merge/tag/release-object mutation | not supported | separate release repository authorization | release-owner receipt |
| staging deployment | not supported | separate staged `team-release stage` authorization | deployment-action-receipt |
| production deployment/rollback | not supported | new staged `team-release promote` authorization | production/rollback receipt |
| publication/send | not supported | separate staged `team-release publish` authorization | publication receipt |

A user may explicitly pre-authorize multiple exact action records, but each layer must
still be individually named, bounded, invoked, and receipted. A file changeset approval
never authorizes Git or an external action. A commit authorization never authorizes
push. Push never authorizes merge/deploy. Deployment never authorizes publication.
Authorization for an external action does not authorize creation of a local receipt
unless that receipt path has separate exact file-write authorization.

## Canonical artifacts and unique writers

Use one stable `hotfix-id` and run directory:

```text
production/hotfixes/<hotfix-id>/
  patch-plan.yaml
  run-manifest.yaml
  patch-receipt.yaml
  commit-receipt.yaml
  build-candidate.yaml
  build-receipt.yaml
  code-review-receipt.yaml
  regression-receipt.yaml
  rollback-plan.yaml
  assessment.yaml
  push-receipt.yaml
  release-handoff.yaml
```

Paths are illustrative until `plan` resolves the exact manifest. Reject traversal,
collisions, ambiguous IDs, and existing artifacts not declared as expected preimages.
Never select a “latest” file.

Unique writers:

- controller: patch plan, run manifest, assessment, handoff;
- assigned implementation owner: only plan-listed code/test files and patch receipt;
- Git operator: commit or push receipt for its separately authorized action;
- build/devops owner: build candidate and build receipt;
- lead programmer: code-review receipt only;
- QA owner: regression receipt and smoke artifacts;
- release/devops owner: rollback/current-deployment receipts;
- owning fix workflow: the separately authorized canonical bug transition.

No two roles write one path. Missing owner leaves the artifact `UNKNOWN`. A fallback
agent can analyze but cannot impersonate a Git operator, QA executor, human release
authority, remote platform, or deployment system.

## Status vocabulary

| Field | Values |
|---|---|
| Operation Status | `PLAN READY`, `WORKTREE READY`, `PATCH APPLIED`, `COMMIT CREATED`, `BUILD READY`, `HOTFIX READY`, `BUG TRANSITION RECORDED`, `PUSHED`, `RELEASE HANDOFF READY`, `PARTIAL`, `BLOCKED`, `ERROR` |
| Candidate State | `UNPLANNED`, `PLANNED`, `PATCHED_UNCOMMITTED`, `COMMITTED_UNBUILT`, `BUILT_UNVERIFIED`, `VERIFIED_LOCAL_CANDIDATE`, `EVIDENCE_STALE` |
| Mutation State | `READ_ONLY_NO_CHANGES`, `WRITTEN`, `NOT_AUTHORIZED`, `FAILED` |
| External Release State | always `NOT_PERFORMED_BY_HOTFIX` |

`HOTFIX READY` is allowed only with Candidate State
`VERIFIED_LOCAL_CANDIDATE`. `PUSHED` describes only one remote ref update and does not
preserve READY if candidate bytes or evidence changed.

## Phase 0: Read-only bug and repository preflight

`plan` performs only read-only operations and records their results/hashes.

For a bug ID:

- require ID `BUG-[0-9]{4,}` and exactly one canonical path
  `production/qa/bugs/<BUG-ID>.md`;
- require schema/status/severity/repro fields and record bug preimage SHA-256;
- accept canonical severity `S1-Critical` or `S2-Major` for emergency planning;
  lower/unknown severity returns `BLOCKED` or a normal-fix recommendation without
  changing priority;
- never read a legacy bug path as canonical.

For a description, require reproducible symptom, actual/expected results, target
platform/build, and affected system before producing a patch plan. Insufficient
reproduction returns `BLOCKED` and causes no Git or file mutation.

Repository preflight records:

- repository root/identity and applicable instruction hashes;
- current worktree path, current branch/ref, HEAD full commit and tree hash;
- tracked modifications, staged changes, untracked paths, conflicts, and submodule
  state without altering them;
- explicit base ref resolved to a reachable full commit;
- proposed branch/worktree path, collision state, and expected ownership;
- remote names/URLs as identifiers only, without fetching or pushing.

Never create a branch in a dirty current worktree. Default to a new isolated worktree
from the exact base commit, but creation still requires `prepare` authorization.
Missing base, conflict, unsafe path, branch/worktree collision, or inability to
separate user changes returns `BLOCKED`. Never stash, reset, clean, discard, or move
user work.

Investigation reads bounded explicit code/tests and returns observed facts,
hypotheses, affected call sites, and file hashes. It makes zero byte changes and zero
Git-state changes.

## Phase 1: Deterministic patch plan

The controller produces an exact patch plan with:

- hotfix/bug ID, canonical bug path/hash, severity and repro case ID;
- repository/base commit/tree and isolated branch/worktree proposal;
- each code/test/hotfix-record path, current preimage hash or `ABSENT`, unique writer,
  and exact intended change;
- minimal scope and explicit excluded refactors/features;
- required failure-sensitive regression test ID/path and original-failure assertion;
- build target, candidate manifest path, QA-plan/test-manifest paths/hashes;
- risk inputs: code layer, data/save/schema migration, network/security/platform
  impact, affected call graph, and test scope;
- current-deployment receipt and rollback artifact/plan requirements;
- separate action registry for prepare, apply, commit, build, push, and handoff;
- every intended local receipt path and unique writer;
- plan SHA-256 and expiry/currentness rule.

Present product or risk choices separately from the file changeset. Existing bounded
authorization is accepted only if it exactly names the plan's file paths and intended
writes. Otherwise request one file changeset authorization for `apply`. Do not ask
for commit, push, deploy, or publication authority in that file-write prompt.

## Phase 2: Prepare an isolated worktree — repository mutation

`prepare` re-hashes the patch plan and reruns the repository preflight. Display an
exact action record:

- action/idempotency ID;
- repo identity, base ref/full commit/tree;
- new branch and absolute isolated worktree path;
- collision checks and expected resulting ref;
- exact command operation, executor, timeout, and recovery/removal owner;
- planned receipt path and preimage.

Obtain explicit repository-action authorization unless the user already authorized
that exact record. Create only the named branch/worktree. Verify observed branch HEAD,
tree, and worktree path and write the authorized receipt. A timeout or interrupted
response is `UNKNOWN`; reconcile read-only before retrying. Do not create code files,
commit, push, or delete a failed worktree in this command.

## Phase 3: Apply the authorized patch — file writes only

`apply` requires `WORKTREE READY`, the exact plan/run manifests, and the file changeset
authorization. Before writing:

1. re-hash the plan, run manifest, isolated worktree HEAD/tree, and every preimage;
2. verify the worktree has only the expected starting state;
3. verify all intended code and test paths remain inside the authorized list;
4. stop on any mismatch or newly required path.

The implementation owner applies only the minimal fix and its failure-sensitive
regression test. Do not refactor, clean up, change versions, update release notes,
modify the canonical bug, commit, tag, push, merge, deploy, or publish.

The patch receipt records plan/run hashes, base commit/tree, exact path list,
preimage/postimage hashes, normalized diff/patch SHA-256, test-source hash, writer,
start/end timestamps, and actual write result. `PATCH APPLIED` means local files
changed exactly as planned; Candidate State remains `PATCHED_UNCOMMITTED`.

## Phase 4: Create an immutable fix commit — separate repository action

`commit` requires a matching patch receipt and a clean comparison showing exactly the
authorized path/postimage set and nothing else. Display a separate commit action:

- repo/worktree/branch, current parent full SHA/tree, expected diff hash;
- exact staged paths and blob hashes;
- commit message bytes/hash, author/executor identity, signing policy;
- expected receipt path and recovery behavior.

Obtain explicit commit authorization for that record. Stage only the listed paths and
create one commit. Verify and record full commit SHA, tree SHA, parent SHA, every
committed path/blob hash, message hash, signature status, executor, timestamps, exit
result, and clean/expected post-commit worktree state.

`COMMIT CREATED` does not mean pushed, merged, built, tested, or ready. Without commit
authorization, stop at `PATCH APPLIED / COMMIT AUTH REQUIRED`.

## Phase 5: Build and freeze the candidate identity

`build` is a distinct action because it may execute tools and write artifacts. Require
an exact build action/output manifest and its authorization, including argv array,
working directory, toolchain/container/config hashes, timeout, output paths, and
cleanup behavior. Do not synthesize commands.

The structured build receipt contains source commit/tree, toolchain/configuration,
exact argv, start/end timestamps, runner/job ID, exit code/result, complete log
path/hash, output artifact path/hash, signature/provenance/SBOM hashes where policy
requires them, and platform matrix.

On success, write a staged-compatible candidate manifest:

```yaml
Artifact Type: build-candidate
Schema Version: 1
Candidate ID: <stable-id>
Build ID: <stable-id>
Build Artifact Path: <path>
Build Artifact SHA-256: <hash>
Source Commit: <full-commit>
Source Tree SHA-256: <hash>
Engine: <name>
Engine Version: <exact-version>
Platform Configuration: <matrix>
Created At: <UTC>
Build Receipt Path: <path>
Build Receipt SHA-256: <hash>
QA Plan Path: <path>
QA Plan SHA-256: <hash>
Test Manifest Path: <path>
Test Manifest SHA-256: <hash>
```

Re-hash the artifact and manifest after persistence. Any rebuild or source/config
change creates a new candidate ID and invalidates review, regression, smoke, rollback
assessment, bug-transition, push/handoff authorization, and receipts.

## Phase 6: Collect candidate-bound recommendations and QA receipts

Delegates may inspect or execute only their assigned artifact and cannot authorize a
release action.

### Code-review recommendation

Lead-programmer returns a receipt bound to candidate manifest/hash, source
commit/tree, patch diff/hash, reviewed path/blob hashes, reviewer identity, timestamps,
stable findings, and result `RECOMMEND READY`, `CONCERNS`, or `REJECT`.
`RECOMMEND READY` is not user authorization.

### Failure-sensitive regression receipt

QA executes the exact declared test and records:

- artifact type/schema and stable receipt ID;
- bug ID, repro case ID, test ID/path/source hash, requirement/AC ID;
- failure-sensitivity receipt or fixture/assertion proving it fails on the original
  defect;
- candidate manifest path/hash, candidate/build/artifact/source commit and platform;
- runner/version/config, exact argv array, working directory;
- start/end UTC timestamps, observer/CI issuer/job ID, exit code and
  `PASS`/`FAIL`/`NOT_RUN`/`TIMEOUT`/`INFRA_ERROR`/`INVALID_RECEIPT`;
- complete untruncated log path/hash and receipt postwrite hash.

Only current `PASS` is positive evidence. Missing sensitivity proof, generic related
tests, manual-only checks, timeout, infra error, truncated logs, or any hash mismatch
blocks readiness.

### Canonical smoke receipt

Consume only the exact staged smoke report and re-hash all transitive artifacts.
Require:

- `Artifact Type: smoke-check-receipt` and `Schema Version: 1`;
- exact candidate-manifest path/hash and candidate/build/artifact/source/platform;
- exact QA-plan/test-manifest/scope and automated/manual evidence hashes;
- `Persistence: WRITTEN`, sprint mode, `Verdict: PASS`,
  `Handoff Eligible: YES`, and current QA-plan effective state;
- complete evidence with no warning, unknown, not-run, timeout, partial, stale, or
  mismatch.

A quick `TARGETED CHECK PASSED` receipt may support diagnosis but never
`HOTFIX READY` or release handoff. This pre-release candidate smoke also cannot be
reused as the post-staging smoke required by staged `team-release`: after verified
staging success, QA must produce a new environment/deployment-bound receipt for the
observed staged artifact.

If a required delegate times out, blocks, returns partial data, or fails to persist
its authorized receipt, keep completed evidence, return `PARTIAL` or `BLOCKED`, and
do not infer a recommendation or PASS.

## Phase 7: Verify current deployment and rollback viability

Read only the exact current-production-state receipt named by the run manifest.
Require:

- artifact type/schema, production account/project/region/environment;
- observation/query timestamp within policy freshness window;
- trusted issuer/observer and external deployment/job ID;
- currently observed build ID, artifact digest, source commit/ref;
- query request/response or log path/hash and identity-verification receipt.

Do not infer the current build from a branch, tag, local file, dashboard label,
“latest” record, or planned deployment.

The rollback plan binds:

- the current deployed build/artifact/source identity above;
- exact previous/rollback build and artifact path/hash, signature/provenance and
  availability verification;
- rollback owner and authorized operator;
- objective triggers and monitoring/query sources;
- kill-switch and ordered executable steps;
- data/save/schema migration scope, compatibility, backup/checkpoint hashes, forward/
  backward compatibility, and reversibility proof;
- rehearsal environment, timestamps, result, logs/hashes, observed restored artifact,
  and validation test receipts; or explicit `NOT REHEARSED`.

`NOT REHEARSED`, missing rollback bytes, unknown current artifact, incompatible save/
schema state, irreversible migration, missing owner, or stale hashes blocks
`HOTFIX READY` and `RELEASE HANDOFF READY`. This workflow does not execute rollback.

## Phase 8: Derive exactly one local assessment

Re-hash the run/plan, commit, build candidate/artifact, review, regression, smoke,
current-deployment, and rollback artifacts.

Return `HOTFIX READY` only when all are true:

1. exact authorized patch paths were committed in one immutable source commit;
2. build-candidate bytes/hash and build receipt are valid;
3. code review has no open blocking finding;
4. failure-sensitive regression receipt is current `PASS`;
5. canonical persisted sprint smoke receipt is current `PASS` and handoff eligible;
6. candidate/source/build/platform identity matches across every receipt;
7. current production artifact is currently verified;
8. rollback artifact, data compatibility, owner, triggers, steps, rehearsal, and
   validation receipts are verified;
9. no required evidence is partial, stale, unknown, timed out, unreadable, or
   mismatched.

Otherwise return `PARTIAL`, `BLOCKED`, or `EVIDENCE STALE` with exact failed
conditions. Agent recommendations never override the table. The assessment records
every input path/hash, result, and timestamp. It has
`External Release State: NOT_PERFORMED_BY_HOTFIX`.

## Phase 9: Record the canonical bug handoff

`record-bug` is a separate exact file-write operation. It requires `HOTFIX READY`,
current bug preimage hash, current `Status: Open`, and authorization for only
`production/qa/bugs/<BUG-ID>.md`.

Propose one atomic edit:

- set `Status: Fixed Pending Verification`;
- record fix full commit, candidate/build/artifact hashes and platform;
- record regression test ID/path and passing receipt path/hash;
- record smoke and assessment paths/hashes;
- append `Open → Fixed Pending Verification` history with fix implementer identity/
  role, UTC timestamp, reason, and bug-record preimage hash.

If status or preimage changed, stop and regenerate. Do not write `Verified Fixed` or
`Closed`. After an independently verified deployment, staged `bug-report verify` must
collect the exact target-build reproduction receipt plus the same failure-sensitive
regression evidence before any later transition.

## Phase 10: Push and release handoff

### Push

`push` is a separate remote mutation. Re-hash the run/commit/candidate/assessment and
perform a read-only remote-state check. Display:

- remote identity/URL, destination ref, expected current remote OID or `ABSENT`;
- local full commit/tree and candidate/artifact hash;
- force policy (must be false), action/idempotency ID, timeout, reconciliation method;
- credential/account identity as a non-secret identifier;
- exact intended ref update and receipt path.

Obtain explicit push authorization for this record. Never force-push. After execution,
query the remote and write a receipt containing authorization digest, old/new observed
OID, remote/ref, result, timestamps, tool/provider response hash, and reconciliation
state. Timeout or unknown response is `UNKNOWN`; reconcile before retrying. `PUSHED`
does not mean merged or deployed.

### Release handoff

`handoff` is read-only unless its exact handoff-report path is separately authorized.
Require current `HOTFIX READY` assessment and any release-policy-required push
receipt. Produce a hash-bound `hotfix-release-handoff` containing:

- bug/hotfix/run IDs and every plan/run/assessment hash;
- source commit/tree, candidate/build/artifact/platform identity;
- build, regression, smoke, review, current-deployment, rollback, and push receipt
  paths/hashes;
- exact release policy/orchestration inputs and missing release evidence;
- explicit statement that merge, staging, production, rollback, publication, and
  communication remain not performed and unauthorized.

`RELEASE HANDOFF READY` means only that the package is ready for the staged
`team-release prepare` entry point. It does not satisfy the later team-release staging
receipt, environment-bound staging smoke, human production confirmation, production
receipt, monitoring window, rollback receipt, or publication receipt.

## Final response

Always report:

- command and operation/candidate/mutation/external-release states;
- bug, repo/base/commit/tree, candidate/build/artifact/platform identities;
- exact file/repository/remote actions actually performed and their receipt hashes;
- regression/smoke/current-deployment/rollback evidence state and stale reasons;
- separate authorization ledger for file, repository, build, push, and external
  release/publication layers;
- partial/timeout/unknown items and one accountable next owner;
- one next permitted command or `none`.

Never say “hotfix complete,” “merged,” “deployed,” “rolled back,” or “published” from
a patch, commit, push, recommendation, candidate build, smoke receipt, or handoff
alone.
