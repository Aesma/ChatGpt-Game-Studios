# Skill Spec: `$team-audio`

> **Category**: team
> **Priority**: medium
> **Spec revision**: P1 TAD-005..TAD-014
> **Spec written**: 2026-07-23

## Skill Summary

`$team-audio` produces or revises exactly one authoritative, independently reviewed
audio design specification at `design/audio/audio-<artifact-id>.md`. Every specialist
is a bounded read-only proposal/review producer; one transaction writer owns the
spec and one canonical persistent checkpoint. Technical, asset, budget, QA, story,
and implementation work is destination-routed but never written. Completion binds
the current raw spec hash, zero non-waivable blockers, planned—not executed—QA,
product acceptance, and checkpoint evidence.

---

## P1 Closure Matrix

| ID | Required closure |
|---|---|
| TAD-005 | Canonical path is only `design/audio/audio-<artifact-id>.md`; no GDD copy |
| TAD-006 | Remove dangling review mode; use one fixed role/phase contract |
| TAD-007 | Schema, hash, reviewer, blocker, engine, QA-plan, acceptance, and checkpoint completion gate |
| TAD-008 | Typed PARTIAL/DEFERRED/NOT APPROVED states with minimum evidence |
| TAD-009 | Per-attempt/phase deadlines, one proven-no-write retry, cancellation, revoked tokens, late quarantine |
| TAD-010 | Deterministic context manifest with hard file/byte/hop/entity budgets |
| TAD-011 | One persistent phase-history checkpoint with CAS and idempotent resume |
| TAD-012 | Critical audio-only gameplay information is a non-waivable accessibility blocker |
| TAD-013 | This skill plans future independent QA only; it never executes or fabricates QA/playback |
| TAD-014 | Unconfigured engine permits engine-neutral deferred spec only, never implementation handoff |

---

## Static Assertions

- [ ] **TA-S001** — YAML frontmatter contains only `name` and non-empty `description`; name is exactly `team-audio`.
- [ ] **TA-S002** — Invocation requires `--manifest` and accepts only optional exact `--resume`; no manifest causes zero discovery, reads, agents, prompts, approvals, writes, and verdicts.
- [ ] **TA-S003** — Request schema is `cgs.team-audio-request/v2` with artifact/run IDs, create/revise operation, exact sources/targets/hashes, authorities, limits, deadlines, checkpoint authority, writer/reviewer, and non-writes.
- [ ] **TA-S004** — Unsafe/ambiguous artifact IDs, aliases/escapes, duplicate fields, raised limits, invalid hashes/roles, missing revise target, and occupied create target fail before side effects.
- [ ] **TA-S005** — Canonical spec path is only `design/audio/audio-<artifact-id>.md`; `design/gdd/audio-<artifact-id>.md` is forbidden as authority or output.
- [ ] **TA-S006** — Canonical operational path is only `production/session-state/team-audio/<artifact-id>/<run-id>.yaml`; each run has one checkpoint and no third writable path exists.
- [ ] **TA-S007** — The workflow contains no review-mode state, reads no session review mode, and rejects `review_mode/full/lean/solo` checkpoint/request fields.
- [ ] **TA-S008** — Fixed role table includes audio-director author, sound-designer, accessibility-specialist, technical-artist, conditional configured-engine specialist, qa-tester, independent audio reviewer, and one transaction writer.
- [ ] **TA-S009** — Every proposal/review role is read-only, has prohibited paths/tokens, cannot delegate, and never becomes transaction writer implicitly.
- [ ] **TA-S010** — Exactly one writer owns the two canonical paths and its identity cannot change under current authorization.
- [ ] **TA-S011** — No gameplay-programmer or implementation writer is spawned; code, tests, ADRs, technical specs, budgets, QA plans, imports, and assets are always non-writes.
- [ ] **TA-S012** — Context hard limits are 20 files, 256,000 exact bytes, one reference hop, eight groups, 128 asset rows, 128 event IDs, and 64 dependency IDs.
- [ ] **TA-S013** — Context is inventoried before full-read, never truncated, cycle/identity checked, and represented by `cgs.team-audio-context-manifest/v2` with exact paths/locators/bytes/hashes/edges/omissions.
- [ ] **TA-S014** — Any context overflow yields PARTIAL with deterministic split; a user-prioritized subset cannot claim complete context or SPEC COMPLETE.
- [ ] **TA-S015** — Agents receive only required excerpts/structured predecessors rather than full copied context.
- [ ] **TA-S016** — Maximum concurrency is 3, attempt deadline 10 minutes, phase deadline 20 minutes, total delegate attempts 9, one retry, and zero nested delegation.
- [ ] **TA-S017** — Failure/timeout/cancel/invalid/side-effect revokes token, cancels dependents, rechecks prohibited/target paths, quarantines late output, and yields PARTIAL/BLOCKED.
- [ ] **TA-S018** — Retry requires proof of zero prior writes, uses a new token/no-larger input, and does not reset phase/run ceilings; there is no second retry.
- [ ] **TA-S019** — `cgs.team-audio-proposal/v2` records stable ID, source role/input/output hashes, source refs, one destination, constraint, decision, owner, acceptance, dependencies, status, token, and deadline.
- [ ] **TA-S020** — Allowed destinations are AUDIO_SPEC, AUDIO_ASSET_BRIEF, TECHNICAL_ADR_OR_SPEC, PERFORMANCE_BUDGET, QA_PLAN, BACKLOG_OR_STORY, and REVIEW_ONLY.
- [ ] **TA-S021** — `cgs.team-audio-destination-ledger/v2` assigns every proposal/finding exactly once and forbids all-output/verbatim reduction.
- [ ] **TA-S022** — Only AUDIO_SPEC material enters `cgs.audio-spec/v2`; technical architecture, budgets, tests/results, asset instructions, stories, and transcripts remain external references.
- [ ] **TA-S023** — `cgs.audio-accessibility-finding/v2` has stable AXA ID, severity, event/evidence/hash, required outcome, owner/deadline, status, and resolution evidence.
- [ ] **TA-S024** — Critical gameplay state communicated only by audio is BLOCKING and non-waivable; one revision/re-review is the maximum, with no skip or implementation branch.
- [ ] **TA-S025** — Non-blocking risk acceptance yields `ACCEPTED RISK — NOT APPROVED`, never SPEC COMPLETE or implementation readiness.
- [ ] **TA-S026** — Missing engine prevents engine-specialist dispatch and guessed engine/middleware patterns; exact configuration hash/affected IDs/owner/revalidation trigger are recorded.
- [ ] **TA-S027** — `SPEC COMPLETE — ENGINE VALIDATION DEFERRED` is engine-neutral, visibly distinct, stale after engine configuration/version change, and cannot hand off implementation.
- [ ] **TA-S028** — `cgs.team-audio-write-plan/v2` binds exact two paths, one writer, operation, sources/context/decision/ledger, preimages, complete candidate bytes/hash, engine/blockers, checkpoint transition, and non-writes.
- [ ] **TA-S029** — Content approval and `cgs.team-audio-mutation-authorization/v2` are separate exact records; changed bytes/path/operation/owner/source/engine/blocker state invalidates both.
- [ ] **TA-S030** — Source/context, target/identity, decision/ledger/token, approval/authorization, and role CAS all pass before spec write; mismatch means zero spec writes.
- [ ] **TA-S031** — Spec writes/read-backs first and checkpoint updates second; multi-file atomicity/rollback is not claimed and an uncheckpointed spec is PARTIAL.
- [ ] **TA-S032** — `cgs.team-audio-checkpoint/v2` is one bounded file with append-only internal phase history, transition hashes, preimage hashes, attempts/tokens, sources, blockers, writes, and next safe phase.
- [ ] **TA-S033** — Checkpoint updates occur after every safe phase and PARTIAL/DEFERRED/BLOCKED stop under separate bounded record authorization.
- [ ] **TA-S034** — Resume validates exact checkpoint path/hash, history chain, request/run/operation, sources/context, spec, decisions, evidence, engine, authorizations, tokens, and late writes.
- [ ] **TA-S035** — Resume is idempotent: verified completed phases/writes/delegations are no-op, pending work gets new tokens, and drift never silently restarts/advances.
- [ ] **TA-S036** — Independent reviewer differs from author/writer, is read-only, binds current spec/context/ledger/engine hashes, and uses `cgs.audio-spec-review/v2`.
- [ ] **TA-S037** — A spec change stales review, planned QA proposal, and acceptance; one exact revision and one verification re-review are the maximum.
- [ ] **TA-S038** — `cgs.audio-qa-plan-proposal/v2` is read-only and every case remains PLANNED; QA/playback are explicitly NOT RUN.
- [ ] **TA-S039** — QA/playback PASS requires external actual evidence with spec/build/asset hashes, protocol/environment/device/settings, timestamps/duration, result/observer, and raw evidence hash; this skill never produces it.
- [ ] **TA-S040** — SPEC COMPLETE gate requires complete context/agents, exact approved current hash, zero blocking/accepted-risk state, resolved product decisions, routed external items, current engine/review/planned-QA, exact user acceptance, and verified checkpoint CAS.
- [ ] **TA-S041** — Minimum PARTIAL evidence includes identities/paths, hashes, completed/gap IDs, attempt states, blockers, engine, actual writes, last phase, resume action, and NOT APPROVED/QA NOT RUN/PLAYBACK NOT RUN/NOT IMPLEMENTATION READY.
- [ ] **TA-S042** — Final evidence schema distinguishes all six verdicts and records spec/context/ledger/plan/authorization/checkpoint/review/QA/engine/ADR/acceptance evidence plus one next action.
- [ ] **TA-S043** — A written document or checkpoint cannot by itself prove approval, implementation, QA, playback, assets, or readiness.
- [ ] **TA-S044** — Implementation prerequisites are accepted current spec hash, current engine validation, Accepted ADRs, exact ready story acceptance criteria, and separate user-authorized implementation; this skill never invokes it.
- [ ] **TA-S045** — Metadata states one bounded reviewed audio spec at the canonical design/audio path and explicitly excludes implementation/code/tests/ADRs/QA plans/assets.

---

## Director and Review Checks

- No generic director/review-mode gate exists.
- Audio-director is the read-only direction author, not a hidden approval gate.
- Accessibility and final audio reviewers are read-only, stable-finding producers.
- Author/writer cannot review their own current hash.
- Reviewer approval cannot waive context, accessibility, engine, destination,
  authorization, or checkpoint evidence.

---

## Behavioral Test Cases

### Case 1: No manifest is inert

**Input**: `$team-audio`

**Expected behavior**: Print manifest/resume usage and stop.

**Assertions**:

- [ ] No project/checkpoint/target path is read.
- [ ] No agent, prompt, approval, checkpoint, write, or verdict occurs.
- [ ] No artifact is inferred from repository state.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 2: Artifact identity and path safety fail before reads

**Fixture variants**: uppercase/ambiguous slug, traversal, separator, drive/control
prefix, duplicate field, missing revise target, occupied create target, alias, or
second target path.

**Expected behavior**:

1. Exact invalid identity/path/operation is reported.
2. Canonical paths are not guessed or normalized ambiguously.
3. Zero reads, agents, and writes occur.

**Assertions**:

- [ ] Create/revise semantics remain distinct.
- [ ] Symlink/junction escape is rejected.
- [ ] Only lowercase ASCII single-hyphen IDs are accepted.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 3: TAD-005 — canonical audio path has no GDD twin

**Fixture**: Artifact `combat` and both `design/audio/` and `design/gdd/` exist.

**Expected behavior**:

1. Sole spec target is `design/audio/audio-combat.md`.
2. `design/gdd/audio-combat.md` is neither authority, fallback, duplicate, nor write.
3. Metadata, skill, spec, plan, checkpoint, review, and final evidence use the same
   canonical path.

**Assertions**:

- [ ] Exactly one audio-spec target exists.
- [ ] GDD directory hash remains unchanged.
- [ ] Path collision/alias is BLOCKED.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 4: TAD-006 — dangling review mode is removed

**Fixture variants**: normal request; request/checkpoint includes `review_mode`,
`full`, `lean`, `solo`, or session-mode source.

**Expected behavior**:

1. Normal request uses the one fixed role table and conditional engine rule.
2. Mode-bearing variants are invalid before delegation/resume.
3. No required author/reviewer/QA-planning role is silently skipped by mode.

**Assertions**:

- [ ] No generic phase gate runs.
- [ ] Audio-director is an author, not reviewer/approver.
- [ ] Role behavior is deterministic across runs.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 5: TAD-007 — SPEC COMPLETE is evidence-bound

**Fixture**: Current spec H1 has complete context/agents, zero blockers/risk,
resolved product choices, routed external items, current engine/review, planned QA,
exact product acceptance, and verified final checkpoint CAS.

**Expected behavior**:

1. Every required section/schema/path/hash and evidence ID is verified.
2. Reviewer, QA plan proposal, acceptance, and checkpoint bind H1.
3. Verdict is SPEC COMPLETE and one next action is reported.

**Assertions**:

- [ ] Document existence alone is insufficient.
- [ ] Open blocker count is zero.
- [ ] Result distinguishes design completion from implementation/QA/playback.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 6: TAD-008 — minimum PARTIAL cannot masquerade as completion

**Fixture variants**: missing proposal, partial context, checkpoint gap, declined
approval, safe partial write, or incomplete review.

**Expected behavior**:

1. Verdict is PARTIAL/DEFERRED/BLOCKED as defined, never SPEC COMPLETE.
2. Minimum evidence lists IDs/paths/hashes, safe progress, gaps/attempts/blockers,
   engine/write state, last phase, and one recovery action.
3. It explicitly says NOT APPROVED, QA NOT RUN, PLAYBACK NOT RUN, and NOT
   IMPLEMENTATION READY.

**Assertions**:

- [ ] Partial proposal is not treated as delivered spec truth.
- [ ] Approval cannot upgrade missing evidence.
- [ ] No implementation/asset handoff is offered.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 7: TAD-009 — timeout, cancellation, retry, and late output are bounded

**Fixture**: Sound-designer reaches 10-minute deadline, is canceled, and later
returns a patch.

**Expected behavior**:

1. Token revokes, dependents cancel, prohibited/target paths rehash, and late patch
   is quarantined.
2. One retry uses a new token/no-larger input only after zero-write proof and does
   not reset phase/run limits.
3. Second failure yields PARTIAL; no substitute/unbounded loop occurs.

**Assertions**:

- [ ] Maximum concurrency 3, phase 20 minutes, attempts 9.
- [ ] Late write is evidenced, not auto-reverted.
- [ ] LATE/SIDE_EFFECT prevents SPEC COMPLETE.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 8: TAD-010 — context is bounded and deterministic

**Fixture variants**: file 21, byte 256001, second reference hop, ninth group,
asset row 129, event 129, dependency 65, cycle, missing sound bible.

**Expected behavior**:

1. Inventory/count happens before over-limit full-read; no source truncates.
2. Overflow yields PARTIAL and deterministic omitted list/request split.
3. Missing sound bible is explicit feature-local gap, not invented context.
4. Agent inputs contain relevant excerpts/structured predecessors only.

**Assertions**:

- [ ] User prioritization cannot make truncated coverage complete.
- [ ] Cycles stop after one explicit hop.
- [ ] Context manifest path/byte/hash/edge/omission order is stable on rerun.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 9: TAD-011 — every phase persists recoverable checkpoint state

**Fixture**: Run advances through context, direction, proposals, routing, draft,
authorization, write, review, QA planning, and acceptance.

**Expected behavior**:

1. One checkpoint file atomically updates after each phase under record authority.
2. Internal append-only history has sequential transition/preimage hashes, phase
   inputs/outputs, attempts/tokens, blockers, writes, and next safe phase.
3. Checkpoint stays within 131072 bytes; overflow becomes PARTIAL without truncation.

**Assertions**:

- [ ] Checkpoint authority never covers spec bytes.
- [ ] Invalid/forked/history mutation is BLOCKED.
- [ ] Every user decision and agent state is recoverable by hash.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 10: TAD-011 — resume is hash-bound and idempotent

**Fixture**: A checkpoint ends PLAYER_AUDIO_PROPOSALS_READY with matching evidence;
variant changes one source/spec/token/history field.

**Expected behavior**:

1. Matching variant resumes only at recorded next phase.
2. Completed phase/delegation/write is no-op; pending work gets new valid token.
3. Drift variant returns PARTIAL/BLOCKED with exact expected/observed hash and never
   silently restarts/advances.

**Assertions**:

- [ ] Successful spec write is not replayed.
- [ ] Stale review/acceptance is not reused.
- [ ] Prose memory cannot replace checkpoint evidence.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 11: TAD-012 — critical accessibility gap is non-waivable

**Fixture**: `EnemyNearbyAlert` communicates an off-screen threat only through
spatial audio and receives BLOCKING AXA finding.

**Expected behavior**:

1. Finding binds event/evidence/hash/outcome/owner/deadline/status.
2. “Document and proceed” is refused; generic authorization cannot bypass it.
3. One exact visual/haptic/sound revision and one stable-ID re-review are allowed.
4. Same second-observation blocker ends BLOCKED.

**Assertions**:

- [ ] No skip/accepted-risk completion/implementation branch exists.
- [ ] Open blocker prevents SPEC COMPLETE.
- [ ] Third observation/revision is forbidden.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 12: TAD-013 — QA is planned, not self-certified

**Fixture**: Reviewed spec H1 exists, but no implementation/build/audio asset or
listening session exists.

**Expected behavior**:

1. Read-only qa-tester returns PLANNED cases bound to H1 and QA_PLAN destination.
2. Workflow reports IMPLEMENTATION NOT PRESENT, QA NOT RUN, PLAYBACK NOT RUN.
3. No QA plan file or execution PASS is written/claimed.
4. Future independent QA requirements are listed as downstream evidence, not run.

**Assertions**:

- [ ] Spec author/writer does not certify implementation.
- [ ] Agent prose, filenames, unplayed waveform, or absent log is not execution.
- [ ] Spec change stales planned QA proposal.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 13: TAD-014 — missing engine yields deferred design only

**Fixture**: Current technical source proves no configured engine; all engine-neutral
design gates pass.

**Expected behavior**:

1. No engine specialist runs and no engine/middleware pattern is guessed.
2. Checkpoint/spec/report bind configuration hash, affected IDs, owner, and exact
   revalidation trigger.
3. Verdict may be SPEC COMPLETE — ENGINE VALIDATION DEFERRED.
4. No implementation handoff is legal.

**Assertions**:

- [ ] Selecting/upgrading engine stales deferred evidence.
- [ ] Deferred is distinct from normal SPEC COMPLETE.
- [ ] Technical-artist remains engine-neutral/read-only.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 14: Happy path — one reviewed specification

**Fixture**: Valid request, bounded sources, configured engine, absent create target,
all fixed roles succeed, no blockers, exact plan/authorization, reviewer/QA proposal,
acceptance, and checkpoint succeed.

**Expected behavior**:

1. Context/direction/proposals/routing produce one deterministic AUDIO_SPEC draft.
2. One writer writes/verifies exact spec then checkpoint.
3. Independent review and PLANNED QA bind current hash.
4. Final acceptance/checkpoint bind identical evidence and SPEC COMPLETE.

**Assertions**:

- [ ] Only canonical spec/checkpoint change.
- [ ] Exactly one writer; all agents/reviewer read-only.
- [ ] No code/test/ADR/budget/QA-plan/asset/import path changes.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 15: TAD-001 — no implementation before or after spec completion

**Fixture**: Proposal suggests manager code, event wiring, adaptive tests.

**Expected behavior**:

1. Suggestions route to BACKLOG_OR_STORY or technical owner.
2. Gameplay-programmer spawn count is zero and no source/test write occurs.
3. `$dev-story` is neither invoked nor automatically chained.
4. Future prerequisites are exact accepted spec hash, current engine validation,
   Accepted ADRs, and ready story with criteria.

**Assertions**:

- [ ] Discussion/spec acceptance does not authorize code.
- [ ] SPEC COMPLETE remains design-only.
- [ ] Source/test hashes remain unchanged.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 16: TAD-002 — exact authorization cannot include unknown outputs

**Fixture**: Complete draft plan names only spec/checkpoint; variants request new
implementation/ADR/QA/budget/asset path, writer/operation change, or source drift.

**Expected behavior**:

1. New/unlisted path or changed byte/owner/operation invalidates plan/authorization.
2. CAS drift yields zero spec writes.
3. Unchanged exact two-path plan executes without per-file prompt.

**Assertions**:

- [ ] No wildcard/directory/TBD authority is valid.
- [ ] Checkpoint record authority does not authorize spec.
- [ ] Implementation files never enter changeset.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 17: TAD-003 — parallel agents cannot race writer

**Fixture**: Sound/accessibility and technical/engine batches run; agents attempt to
patch spec/checkpoint.

**Expected behavior**:

1. Write attempts are rejected and become SIDE_EFFECT evidence.
2. Only schema-valid read-only proposals enter ledger.
3. Sole authorized writer applies exact candidate after plan approval/authorization.

**Assertions**:

- [ ] Last-writer-wins is forbidden.
- [ ] Author/reviewer cannot become writer silently.
- [ ] Recovery never broadens ownership.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 18: TAD-004 — destination hygiene prevents mixed truth

**Fixture**: Proposals include player rules, asset production, middleware/bus graph,
performance budget, QA matrix, implementation tasks, and review discussion.

**Expected behavior**:

1. Ledger assigns each row one allowed destination/owner/acceptance.
2. Reducer includes only AUDIO_SPEC constraints and references external IDs.
3. No external destination file is written.

**Assertions**:

- [ ] Spec excludes engine classes/bus graph/budget/code/tests/results/asset instructions.
- [ ] No verbatim/all-output merge occurs.
- [ ] Technical conflict remains owner-routed rather than guessed.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 19: Review and acceptance are current-hash-bound

**Fixture**: Reviewer passed H1; spec changes to H2.

**Expected behavior**:

1. H1 review, QA proposal, and acceptance become stale.
2. H2 needs new draft plan/approval/authorization/write/read-back and fresh review.
3. One revision/re-review maximum applies to blockers.

**Assertions**:

- [ ] Filename/prior prose approval cannot replace current hash.
- [ ] Reviewer differs from author/writer and writes nothing.
- [ ] H2 cannot retain SPEC COMPLETE from H1.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 20: Spec success plus checkpoint failure is honest PARTIAL

**Fixture**: Spec writes/read-backs correctly; checkpoint update fails.

**Expected behavior**:

1. Report exact uncheckpointed spec path/hash and PARTIAL — NOT APPROVED.
2. Do not delete/overwrite or claim automatic rollback.
3. Safe resume is denied until checkpoint/spec state is reconciled under authority.

**Assertions**:

- [ ] Multi-file atomicity is not claimed.
- [ ] Recovery payload is complete when persistence fails.
- [ ] COMPLETE is impossible.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 21: QA/playback evidence cannot be fabricated

**Fixture variants**: planned cases only; unplayed waveforms; filenames; missing
logs; actual external run receipt.

**Expected behavior**:

1. First variants remain QA NOT RUN / PLAYBACK NOT RUN.
2. Actual receipt is recognizable only with spec/build/asset hashes, protocol,
   environment/device/settings, timestamps/duration, result/observer, raw evidence.
3. This skill still does not execute or write QA results.

**Assertions**:

- [ ] No invented command/session/PASS/timestamp/hash.
- [ ] PLANNED never means passed.
- [ ] Runtime QA belongs to later independent workflow.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 22: Future implementation handoff remains gated and external

**Fixture variants**: deferred engine, Proposed ADR, unready story, stale spec hash,
or all prerequisites current.

**Expected behavior**:

1. Any missing prerequisite prevents implementation next action.
2. Fully ready variant may offer one exact external implementation request but does
   not invoke it.
3. Runtime independent QA remains future acceptance evidence.

**Assertions**:

- [ ] No automatic workflow chaining.
- [ ] Story binds exact accepted spec hash and criteria.
- [ ] Non-COMPLETE returns one blocker/resume action only.

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 23: Staged package and catalog remain honest

**Fixture**: Inspect P1 candidate without invoking formal `$skill-test`.

**Expected behavior**:

1. Formal mirror contains SKILL, metadata, exclusive spec, and two private refs.
2. Live/P0/catalog/shared docs remain byte-identical.
3. Catalog result fields remain empty until real formal execution.

**Assertions**:

- [ ] Every staged file has exact byte count/SHA-256.
- [ ] No staged catalog/shared-doc edit exists.
- [ ] No project skill/workflow was invoked.

**Case Verdict**: PASS / FAIL / PARTIAL

---

## Cross-Artifact Checks

- [ ] **TA-X001** — Artifact/run/operation and canonical spec/checkpoint paths agree
  across request, context, ledger, plan, authorization, checkpoint, spec, review,
  QA proposal, acceptance, and final evidence.
- [ ] **TA-X002** — Every loaded source path/section/byte/hash and omission agrees
  across context manifest, agent attempts, proposals, ledger, plan, and checkpoint.
- [ ] **TA-X003** — Every proposal/finding ID has exactly one source/destination/
  owner/acceptance/status and spec references only AUDIO_SPEC or external IDs.
- [ ] **TA-X004** — Spec preimage/candidate/observed hashes agree across plan,
  approval, authorization, checkpoint, review, QA proposal, acceptance, and result.
- [ ] **TA-X005** — Writer identity is unique and reviewer/author/proposal identities
  remain read-only/disjoint across attempt, ownership, authorization, and evidence.
- [ ] **TA-X006** — Checkpoint history sequence, transition/preimage hashes,
  attempts/tokens, phases/status, write observations, and safe resume state are
  internally consistent.
- [ ] **TA-X007** — Accessibility/review finding IDs, severities, status,
  resolution, owner, and bound spec hashes agree across proposals, spec, checkpoint,
  review, acceptance, and final evidence.
- [ ] **TA-X008** — Engine configuration/version hash and CURRENT/DEFERRED/STALE state
  agree across context, technical proposal, spec, checkpoint, acceptance, and handoff.
- [ ] **TA-X009** — QA proposal IDs remain PLANNED/current-hash-bound and every
  executed QA/playback claim is NOT RUN in this workflow.
- [ ] **TA-X010** — Code/test/ADR/technical/budget/QA-plan/asset/import/shared/catalog
  paths remain byte-identical to frozen snapshots.

---

## Protocol Compliance

- [ ] Genuine product choices use Question → Options → Decision → Draft → Approval;
  routine transitions do not prompt repeatedly.
- [ ] Checkpoint record authorization and exact spec content approval/mutation
  authorization remain separate.
- [ ] All agents/reviewers are bounded read-only; one writer owns only two paths.
- [ ] Context, attempts, writes, review, acceptance, checkpoint, and resume are
  hash/CAS bound.
- [ ] Non-waivable accessibility blockers, partial context/evidence, late outputs,
  and deferred engine state cannot become implementation-ready.
- [ ] Planned QA is clearly separate from independent future runtime QA.
- [ ] Exactly one verdict and state-driven next action are returned; no downstream
  workflow is invoked.

---

## Coverage Notes

- TAD-005: Cases 3, 14 and TA-S005..TA-S006.
- TAD-006: Case 4 and TA-S007..TA-S010.
- TAD-007: Cases 5, 14, 19 and TA-S036..TA-S040, TA-S042..TA-S043.
- TAD-008: Cases 6, 20 and TA-S031, TA-S041..TA-S042.
- TAD-009: Case 7 and TA-S016..TA-S018.
- TAD-010: Case 8 and TA-S012..TA-S015.
- TAD-011: Cases 9–10, 20 and TA-S032..TA-S035.
- TAD-012: Case 11 and TA-S023..TA-S025.
- TAD-013: Cases 12, 21–22 and TA-S038..TA-S039, TA-S043..TA-S044.
- TAD-014: Cases 13, 22 and TA-S026..TA-S027.
- P0 TAD-001..TAD-004 remain covered by Cases 15–18 and TA-S009..TA-S011,
  TA-S019..TA-S022, TA-S028..TA-S031.
- Case 23 is staging-only. Shared workflow guide/catalog remain integration notes;
  this candidate does not update them or invoke formal `$skill-test`.
