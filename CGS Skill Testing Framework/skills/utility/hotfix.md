# Skill Spec: `$hotfix`

> **Category**: utility
> **Priority**: low
> **Spec written**: 2026-07-22

## Skill Summary

`$hotfix` prepares one immutable local fix candidate. It separates read-only
investigation, isolated worktree creation, code/test writes, commit, build, push, and
release handoff into independently authorized commands and receipts. It never merges,
deploys, rolls back, publishes, or treats model recommendations as release authority.
`HOTFIX READY` requires one exact commit/build/artifact identity, a
failure-sensitive regression receipt, canonical full smoke receipt, current deployed
build receipt, and verified rollback evidence.

---

## Static Assertions

- [ ] YAML frontmatter contains only required `name` and non-empty `description`;
      name matches the skill directory
- [ ] Metadata states local candidate scope and separate code/Git/release/rollback/
      publication authority
- [ ] Has at least two phase headings
- [ ] Skill is explicit-invocation only and one invocation runs one command
- [ ] Defines `plan`, `prepare`, `apply`, `commit`, `build`, `assess`,
      `record-bug`, `push`, and `handoff`
- [ ] Has no merge, deploy, rollback-execution, publish, or send command
- [ ] Never outputs `HOTFIX COMPLETE` from local work
- [ ] `HOTFIX READY` explicitly means local candidate only
- [ ] File-write, repository/worktree, commit, build, push, merge/tag, staging,
      production/rollback, and publication authorities are separate
- [ ] Agent recommendations cannot authorize any repository or external action
- [ ] Investigation is byte-level and Git-state read-only
- [ ] Complete patch paths and preimage hashes are known before `apply` authorization
- [ ] Dirty current worktree is never stashed/reset/cleaned or used for new branch
      creation
- [ ] Commit and push use distinct action records, commands, authorization, and
      receipts
- [ ] Candidate manifest matches staged smoke/release `build-candidate` identity:
      candidate/build/artifact/source/platform plus QA-plan/test-manifest hashes
- [ ] Regression evidence is failure-sensitive and binds commit/build/artifact,
      exact test/argv/runner/timestamps/exit code/log hash
- [ ] Smoke evidence requires persisted sprint `PASS` and
      `Handoff Eligible: YES` for the exact candidate
- [ ] Quick/targeted smoke cannot yield `HOTFIX READY`
- [ ] Pre-release candidate smoke cannot substitute for post-staging
      environment/deployment-bound smoke
- [ ] Current production build/artifact hash comes from a trusted current-state receipt
- [ ] Rollback binds current and previous artifact hashes, owner, triggers, ordered
      steps, data compatibility, backup, rehearsal, and validation receipts
- [ ] Missing/unrehearsed/irreversible rollback blocks readiness
- [ ] Canonical bug update is only `Open → Fixed Pending Verification` and includes
      commit/build/regression evidence
- [ ] `Verified Fixed` and `Closed` remain owned by staged `bug-report`
- [ ] All actual actions and receipts report raw hashes; stale/mismatched evidence
      cannot pass

---

## Director Gate Checks

None. Lead-programmer, QA, producer, and other agents produce candidate-bound
recommendations or receipts only. They are not release-authority gates and cannot
replace the explicit user/repository/remote/deployment/publication action records.

---

## Test Cases

### Case 1: Plan is a zero-mutation investigation

**Fixture:**

- Canonical `BUG-0042` is `Open` and `S1-Critical` with complete reproduction data.
- Repository has an explicit reachable base ref.
- Source and tests can be read.

**Input:** `$hotfix plan BUG-0042`

**Expected behavior:**

1. Bug record, repository, worktree, base ref, candidate paths, and relevant code/tests
   are read and hashed.
2. An exact patch plan lists every proposed code/test/receipt path, preimage hash,
   intended change, unique writer, regression test, build target, risks, rollback
   requirements, and action IDs.
3. No branch, worktree, file, index, staging area, commit, remote, or external state
   changes.
4. Result is `PLAN READY` and `READ_ONLY_NO_CHANGES`.

**Assertions:**

- [ ] Plan authorization is requested only after investigation establishes exact scope
- [ ] Vague reproduction blocks before repository/file mutation
- [ ] New paths discovered later require a revised plan

---

### Case 2: Dirty user work is preserved

**Fixture:**

- Current worktree contains tracked and untracked user changes.
- Patch plan proposes an isolated worktree from an explicit base commit.

**Input:** `$hotfix prepare --plan <path> --action-id PREP-1`

**Expected behavior:**

- Preflight reports dirty/staged/untracked state without changing it.
- No branch is created in the dirty current worktree.
- With exact repository-action authorization, only the named isolated branch/worktree
  is created from the exact base commit.
- Without authorization or on collision, operation is `BLOCKED`.

**Assertions:**

- [ ] No stash, reset, clean, checkout-overwrite, deletion, or move of user work
- [ ] Worktree/branch creation is not covered by file-write authorization
- [ ] Timeout becomes unknown and requires read-only reconciliation before retry

---

### Case 3: Apply writes only the authorized patch scope

**Fixture:**

- Isolated worktree receipt is valid.
- Patch plan and run manifest hashes match.
- Exact code and regression-test paths are file-write authorized.

**Input:** `$hotfix apply --run-manifest <path>`

**Expected behavior:**

- Every path preimage is revalidated.
- Only the minimal fix and failure-sensitive regression test are written.
- Patch receipt contains pre/post hashes, diff hash, writer, timestamps, and result.
- No commit, version change, canonical bug edit, push, merge, deployment, or
  publication occurs.
- Result is `PATCH APPLIED` / `PATCHED_UNCOMMITTED`.

**Assertions:**

- [ ] An added unplanned file blocks before write
- [ ] A code fix without a regression test blocks
- [ ] File authorization does not grant commit authority

---

### Case 4: Commit requires its own exact authorization

**Fixture:**

- Patch receipt matches exactly the worktree diff.
- No extra staged/untracked path is present.
- File changes were authorized, but commit was not.

**Input:** `$hotfix commit --run-manifest <path> --action-id COMMIT-1`

**Expected behavior:**

- The workflow displays repo/worktree/branch, parent commit/tree, diff hash, exact
  staged paths/blob hashes, commit message hash, executor/signing policy, and receipt.
- Without explicit commit authorization, it stops at
  `PATCH APPLIED / COMMIT AUTH REQUIRED`.
- With authorization, only listed paths are committed and a full commit/tree/parent
  receipt is verified.
- Result `COMMIT CREATED` does not imply pushed/merged/built/tested.

**Assertions:**

- [ ] File-write approval is not reused as commit approval
- [ ] Commit receipt uses full SHA, never a description
- [ ] Unexpected worktree content blocks the commit

---

### Case 5: Build freezes one staged-compatible candidate

**Fixture:**

- Commit receipt is valid.
- Exact build argv/toolchain/config/output action is authorized.
- Build succeeds with complete log and artifact.

**Input:** `$hotfix build --run-manifest <path> --action-id BUILD-1`

**Expected behavior:**

- Build receipt binds source commit/tree, toolchain/config, argv, timestamps, exit
  code, complete log hash, artifact path/hash, platform, and required provenance.
- Candidate manifest declares `Artifact Type: build-candidate`, schema 1,
  candidate/build/artifact/source/platform, QA-plan and test-manifest paths/hashes.
- Manifest/artifact are re-hashed after persistence.
- Result is `BUILD READY` / `BUILT_UNVERIFIED`.

**Assertions:**

- [ ] Build success alone is not `HOTFIX READY`
- [ ] A rebuild or new commit creates a new candidate and stales all dependent evidence
- [ ] No push/merge/deploy occurs

---

### Case 6: Old-build regression evidence is rejected

**Fixture:**

- Candidate source commit is `C2` with build/artifact hashes `B2/A2`.
- Regression receipt is a passing result for older `C1/B1/A1`.

**Input:** `$hotfix assess ...`

**Expected behavior:**

- Exact commit/build/artifact mismatches are listed.
- Receipt becomes stale/invalid even though its result says PASS.
- Result is `EVIDENCE STALE` or `BLOCKED`, never `HOTFIX READY`.

**Assertions:**

- [ ] Command, exit code, timestamps, runner/config, test-source and log hashes are also
      required
- [ ] Generic suite or manual verification cannot replace failure-sensitive receipt
- [ ] No agent recommendation overrides the mismatch

---

### Case 7: Quick smoke is targeted evidence only

**Fixture:**

- Exact candidate has a persisted quick smoke report with
  `Verdict: TARGETED CHECK PASSED` and `Handoff Eligible: NO`.
- Regression receipt passes.

**Input:** `$hotfix assess ...`

**Expected behavior:**

- Quick receipt may be listed as diagnostic evidence.
- Missing persisted sprint-mode PASS/handoff-eligible smoke blocks readiness.
- Result is `PARTIAL` or `BLOCKED`.

**Assertions:**

- [ ] Quick mode never becomes full smoke PASS
- [ ] Pre-release smoke is never represented as post-staging smoke
- [ ] No release handoff is ready

---

### Case 8: Agent recommendations are not deployment approval

**Fixture:**

- Lead-programmer recommends ready.
- QA regression and smoke receipts pass.
- Producer agent recommends urgent release timing.
- User supplied no merge/deploy/publication authorization.

**Expected behavior:**

- Recommendations are recorded with candidate hash but grant no action authority.
- Hotfix may become locally ready only if all other objective gates, including
  rollback/current-build evidence, pass.
- No merge, staging, production, rollback, publication, or send occurs.

**Assertions:**

- [ ] Producer recommendation is not human production confirmation
- [ ] `HOTFIX READY` still reports `External Release State: NOT_PERFORMED_BY_HOTFIX`
- [ ] No action is inferred from urgency or role labels

---

### Case 9: Complete current evidence yields local HOTFIX READY only

**Fixture:**

- Exact patch/commit/build receipts match.
- Code review has no blocking finding.
- Failure-sensitive regression is current PASS.
- Persisted sprint smoke is current PASS and handoff eligible.
- Trusted production-state receipt proves current artifact hash.
- Rollback artifact, compatibility, owner, triggers, rehearsal, and validation
  receipts match.
- No required evidence is partial/stale/unknown.

**Input:** `$hotfix assess ...`

**Expected behavior:**

- Every path and transitive hash is recomputed.
- Candidate State is `VERIFIED_LOCAL_CANDIDATE`.
- Operation Status is `HOTFIX READY`.
- External Release State remains `NOT_PERFORMED_BY_HOTFIX`.
- No repository or external action occurs.

**Assertions:**

- [ ] READY means local candidate only
- [ ] No `HOTFIX COMPLETE`, merged, deployed, or published claim
- [ ] Assessment lists exact evidence paths/hashes and timestamp

---

### Case 10: Unknown current build or rollback blocks readiness

**Variants:**

- A: production-state receipt is missing or stale;
- B: rollback artifact bytes/hash are unavailable;
- C: migration is irreversible or save/schema rollback is incompatible;
- D: rollback was not rehearsed;
- E: rollback owner/trigger/backup is missing.

**Expected behavior:**

- Exact gap is reported.
- Result is `BLOCKED` or `PARTIAL`.
- No deploy or rollback action is attempted.
- A branch/tag/dashboard label or local “latest” file is not accepted as current build
  evidence.

**Assertions:**

- [ ] Current and previous artifact hashes are distinct explicit fields
- [ ] Rollback rehearsal requires observed restored artifact and validation receipts
- [ ] A prose rollback plan alone cannot yield READY

---

### Case 11: Bug transition matches staged bug-report state machine

**Fixture:**

- `BUG-0042` is still `Open` and its preimage hash matches.
- Assessment is `HOTFIX READY`.
- Exact bug-file write is separately authorized.

**Input:** `$hotfix record-bug --assessment <path>`

**Expected behavior:**

- One atomic edit sets `Fixed Pending Verification`, records full fix
  commit/candidate/build/artifact/platform identity, regression test/receipt, smoke and
  assessment hashes, and appends transition history with owner/time/reason/preimage.
- No `Verified Fixed` or `Closed` state is written.
- If bug status/hash changed, no mutation occurs.

**Assertions:**

- [ ] Code changeset authorization does not automatically cover bug-file edit
- [ ] Fix workflow owns only `Open → Fixed Pending Verification`
- [ ] Later verification requires target-build reproduction plus automated regression
      through staged `bug-report`

---

### Case 12: Push is separate and still not merge/deploy

**Fixture:**

- Commit/candidate/assessment are current.
- Remote destination ref has observed old OID `R1`.
- Commit authorization exists; push authorization does not.

**Input:** `$hotfix push --run-manifest <path> --action-id PUSH-1`

**Expected behavior:**

- Exact remote/ref, expected old OID, new commit/tree, artifact hash, non-force policy,
  idempotency ID, timeout, reconciliation, and receipt are shown.
- No push occurs without explicit authorization.
- With authorization, observed remote OID must become the exact commit and a receipt
  is written.
- Result `PUSHED` does not mean merged/deployed.

**Assertions:**

- [ ] Never force-push
- [ ] Unknown timeout is reconciled before retry
- [ ] Changed remote state invalidates authorization

---

### Case 13: Handoff cannot reuse pre-release smoke as staging evidence

**Fixture:**

- Local assessment is `HOTFIX READY` and policy-required push receipt is valid.
- No staging deployment receipt or environment-bound staging smoke exists.

**Input:** `$hotfix handoff --run-manifest <path>`

**Expected behavior:**

- Hash-bound hotfix handoff package references the candidate evidence and exact release
  inputs.
- It explicitly lists staging deployment, staging smoke, production confirmation,
  production receipt, monitoring, rollback execution, and publication as not
  performed.
- `RELEASE HANDOFF READY` means ready for staged `team-release prepare` only.

**Assertions:**

- [ ] Hotfix does not invoke release workflow
- [ ] New staging smoke must bind deployment receipt, environment, and observed artifact
- [ ] No merge/deploy/publish authority appears in handoff state

---

### Case 14: Every command has one deterministic side-effect boundary

**Variants:**

- `plan`, `prepare`, `apply`, `commit`, `build`, `assess`, `record-bug`,
  `push`, `handoff`, invalid command, and requests to merge/deploy/publish.

**Expected behavior:**

- Each supported command performs only its declared layer and stops.
- Invalid command reads/writes nothing after argument validation.
- Merge/deploy/publish requests are rejected as unsupported and name the separate
  release owner/authorization requirement without invoking it.
- No command returns `HOTFIX COMPLETE`.

**Assertions:**

- [ ] SKILL and spec invocation/verdict dictionaries match
- [ ] No command cascades across authority layers
- [ ] Actual actions and receipt hashes are reported; absent actions remain not
      performed

---

## Protocol Compliance

- [ ] Read-only investigation precedes exact file changeset authorization
- [ ] Existing bounded authorization is accepted only for the exact named layer/action
- [ ] New paths, ref changes, rebuilt artifacts, or changed external targets require
      revised authorization
- [ ] No per-file prompts occur inside an unchanged authorized patch manifest
- [ ] Repository/remote/external action authorization never derives from file approval
- [ ] Partial, timeout, stale, unknown, and mismatch states block dependent actions
- [ ] No destructive cleanup or silent user-work handling
- [ ] One next permitted command is returned and nothing is invoked automatically

---

## Coverage Notes

Cases 9 and 14 close HF-001; Case 8 closes HF-002; Cases 5–7 close HF-003; Cases
1–4 close HF-004. Cases 10–13 cover the required rollback/current-build, canonical
bug-state, smoke/release receipt, and authority-boundary integration. These are
behavioral expectations only: this remediation performed static validation and did
not create a branch, edit code, commit, build, push, merge, deploy, roll back, publish,
run tests, or execute any project workflow.
