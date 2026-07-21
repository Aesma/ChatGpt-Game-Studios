# Skill Spec: $team-ui

> **Category**: team
> **Priority**: medium
> **Spec written**: 2026-07-22

## Skill Summary

$team-ui consumes one exact UI feature request manifest, authors and independently reviews a hash-bound UX spec, then plans a separately authorized implementation with one writer. Reviewers are read-only and bounded. Verdict: COMPLETE is legal only when the post-fix final build/source hash has complete UX, art, accessibility, engine, input, layout, localization, text-scaling, colorblind, motion, cleanup, and main-thread evidence.

---

## Static Assertions

- [ ] YAML frontmatter contains only name and a non-empty description; name is team-ui
- [ ] No-argument validation occurs before project reads or delegation
- [ ] UX-review uses the staged read-only record schema, stable UXF IDs, exact target hash, and persisted recorder envelope
- [ ] NEEDS REVISION/accepted risk cannot authorize production implementation or COMPLETE
- [ ] UX revisions and implementation fixes are each capped at two rounds
- [ ] Every artifact path has one writer and reviewers are read-only
- [ ] ui-programmer cannot modify the global interaction-pattern library
- [ ] Design-support and implementation each require a precise later authorization boundary
- [ ] Implementation manifest lists exact paths, operations, base hashes, writer, evidence paths, and non-writes
- [ ] Review concurrency, task/phase deadlines, one retry, PARTIAL behavior, checkpoints, and resume revalidation are explicit
- [ ] Post-fix reviews bind the final build/source-set hash and stale every prior review
- [ ] COMPLETE requires zero open blockers and the full build-bound evidence matrix
- [ ] Skill/spec both acknowledge project writes and exact mutation allowlists
- [ ] The final phase emits one state-driven next action without invoking another workflow

---

## Director Gate Checks

- **Full mode**: optional director consultations may run, but their output is advisory and cannot replace mandatory evidence.
- **Lean mode**: optional consultations are skipped; all mandatory independent reviews remain.
- **Solo mode**: no independent quorum exists, so design/prototype work may proceed but production COMPLETE is impossible.
- **Mandatory reviews**: UX conformance, art consistency, accessibility, and engine/QA evidence cannot be skipped by mode.

---

## Test Cases

### Case 1: Happy path — approved spec to verified final build

**Fixture**:
- Valid feature manifest, context/hash budget, configured engine, applicable AGENTS chain, interaction library, accessibility targets, and exact owners.
- UX review returns current-hash APPROVED with zero blockers.
- Visual/asset/engine artifacts and precise implementation manifest are separately authorized.
- One writer implements only listed paths.
- All final evidence streams pass on the same post-fix build/source hash.

**Expected behavior**:
1. Design, review, support-artifact, implementation, build, and final-review checkpoints are persisted.
2. Every mutation stays inside the active manifest.
3. Final result is Pipeline Result: IMPLEMENTATION_VERIFIED and Verdict: COMPLETE.

**Assertions**:
- [ ] UX approval envelope embeds the unmodified read-only review record and revalidates target SHA-256
- [ ] ui-programmer never writes design artifacts or the global pattern library
- [ ] All mandatory review outputs bind the final build/source hash
- [ ] Final result reports exact artifact/evidence/checkpoint hashes

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 2: NEEDS REVISION cannot be overridden into production

**Fixture**:
- UX review returns NEEDS REVISION with gamepad and contrast blockers.
- User records accepted risk.

**Expected behavior**:
1. Original review verdict and approval_status remain unchanged.
2. Pipeline Result is ACCEPTED_RISK_SPEC_NOT_APPROVED.
3. Only a separately authorized nonproduction prototype/backlog proposal is legal.
4. Visual production work, implementation writer, and COMPLETE do not run.

**Assertions**:
- [ ] No implementation manifest is generated
- [ ] Accepted risk lists stable open finding IDs and target hash
- [ ] No approved/implementation-ready wording appears

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 3: UX convergence stops after two revisions

**Fixture**:
- The same stable UXF navigation blocker remains after revision rounds 1 and 2.

**Expected behavior**:
1. Author remains the only spec writer; reviewer remains independent/read-only.
2. Each round maps the same finding ID to exact diffs and performs regression scan.
3. Automatic loop stops after round 2 with BLOCKED/USER DECISION.

**Assertions**:
- [ ] No third automatic revision occurs
- [ ] Legal options are narrow/redefine, stop, or accepted-risk nonproduction path
- [ ] The stale prior hashes cannot be reused

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 4: Programmer global-pattern mutation is refused

**Fixture**:
- Implementation introduces a new interaction and attempts to edit design/ux/interaction-patterns.md.

**Expected behavior**:
1. New behavior is represented as stable feature-local UXP proposal owned by ux-author.
2. Mutation guard detects/refuses programmer write to the global library.
3. Cross-screen behavior blocks until the external library/ADR owner acts.

**Assertions**:
- [ ] Programmer source allowlist excludes the global library
- [ ] Proposal is not labelled globally approved
- [ ] User work is not silently reverted

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 5: Post-polish change invalidates old reviews

**Fixture**:
- Initial implementation build B1 receives blocking findings.
- Unique writer fixes them and produces build B2.

**Expected behavior**:
1. All B1 reviews become stale.
2. Previously failed checks plus the full regression matrix run against B2.
3. COMPLETE is possible only if every required B2 stream/evidence row is complete and blockers are zero.

**Assertions**:
- [ ] B1 approval cannot be attached to B2
- [ ] Stable UIF finding transitions are preserved
- [ ] New fix paths require a new implementation authorization

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 6: Design authorization cannot pre-authorize unknown implementation

**Fixture**:
- UX candidate exists but visual, engine, and implementation paths are not yet planned.

**Expected behavior**:
1. Initial authorization contains only exact UX/review/checkpoint paths and bounded revision rules.
2. Visual/engine candidate bytes are planned before their authorization.
3. Precise implementation manifest is presented and authorized separately.

**Assertions**:
- [ ] No broad all-pipeline changeset is requested
- [ ] Nested roles do not independently re-prompt per file
- [ ] Every implementation operation has exact path/base hash/writer/non-writes

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 7: No argument exits before reads

**Fixture**:
- Any project state.

**Expected behavior**:
1. Invocation without --manifest shows exact usage.
2. No project file is read, no agent is spawned, no checkpoint is written, and no verdict is issued.

**Assertions**:
- [ ] Validation precedes review-mode/context resolution
- [ ] No side effect occurs
- [ ] Usage names the required manifest

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 8: Missing engine blocks production, not design

**Fixture**:
- Valid design context but Engine Status: UNCONFIGURED.

**Expected behavior**:
1. UX author/review may reach SPEC_APPROVED.
2. No ui-programmer or production implementation begins.
3. Result identifies engine configuration/plan as the single next action.

**Assertions**:
- [ ] No generic engine hierarchy is invented
- [ ] Prototype, if separately authorized, is explicitly nonproduction
- [ ] COMPLETE is impossible

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 9: Bounded parallel review timeout yields PARTIAL and resumable checkpoint

**Fixture**:
- Four required review streams; concurrency cap is 3.
- One stream times out twice while others complete.

**Expected behavior**:
1. At most three agents run concurrently and no child delegation occurs.
2. One same-hash narrowed retry is attempted.
3. Timeout produces PARTIAL; quorum is not fabricated.
4. Checkpoint records completed streams, timeout, hashes, deadline, and next legal retry.

**Assertions**:
- [ ] Missing reviewer is never treated as approval
- [ ] Resume re-hashes all inputs and invalidates stale results
- [ ] No dependent COMPLETE occurs

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 10: Final evidence matrix enforces nested UI rules

**Fixture**:
- Implementation passes basic navigation but lacks one committed text-scale/reflow row and main-thread profile.

**Expected behavior**:
1. Missing rows are blocking UNKNOWN/NOT RUN evidence.
2. Result is NEEDS_REVISION or PARTIAL, never COMPLETE.
3. Exact owners and evidence paths are reported.

**Assertions**:
- [ ] Keyboard/gamepad/target inputs, resolutions/aspects, locales, text scales, colorblind modes, reduced motion, lifecycle, and main-thread checks are enumerated
- [ ] File existence or reviewer prose cannot replace build-bound receipts
- [ ] src/ui/AGENTS constraints are represented

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 11: Review-mode cannot weaken mandatory quorum

**Fixture**:
- Mode is lean or solo.

**Expected behavior**:
1. Lean skips optional director consultations but keeps four mandatory review streams.
2. Solo records that independent quorum is unavailable and cannot return production COMPLETE.

**Assertions**:
- [ ] Art/accessibility/engine/UX checks are not silently skipped
- [ ] Optional consultation output never counts as gate evidence
- [ ] Mode is resolved once and checkpointed

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 12: Side-effect contract matches implementation

**Fixture**:
- Design and implementation writes are requested.

**Expected behavior**:
1. The spec declares controlled writes rather than read-only behavior.
2. Each phase's complete mutation allowlist is previewed and authorized at its proper boundary.
3. Non-owned paths remain byte-identical.

**Assertions**:
- [ ] No statement claims the orchestrator pipeline is read-only
- [ ] Review tasks are read-only while named writer tasks perform writes
- [ ] Write/read-back and outside-path mutation checks are reported

**Case Verdict**: PASS / FAIL / PARTIAL

---

## Protocol Compliance

- [ ] Explicit bounded requests authorize only operations already enumerated at that boundary
- [ ] Newly discovered implementation scope requires the separate precise manifest approval
- [ ] Stable finding IDs and current hashes govern every revision/review
- [ ] Unique writer ownership remains unchanged through fixes
- [ ] Timeouts/errors/missing quorum are PARTIAL/BLOCKED, never skipped
- [ ] Checkpoints are immutable, hash-bound, and resumable
- [ ] Accepted risk cannot create approval or production COMPLETE
- [ ] Global UX source, ADRs, game-state owners, and unrelated paths are non-writes
- [ ] Final COMPLETE is bound to the post-fix build/source-set and conclusive evidence

---

## Coverage Notes

This is a behavioral specification, not an executed test result. Runtime fixtures should cover manifest/path/symlink validation, context budgets, nested AGENTS precedence, create/revise base hashes, ux-review record persistence envelope, two-round UX and implementation loops, pattern proposals, missing engine/ADR/library, all authorization boundaries, parallel scheduling/timeouts/retry, checkpoint interruption/resume, outside-path mutation detection, final evidence matrices, and proof that reviewers and non-owned artifacts remain byte-identical.
