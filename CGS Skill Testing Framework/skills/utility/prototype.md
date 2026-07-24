# Contract Specification: `prototype`

## Purpose

Validate `prototype` as one finite, isolated, reproducible experiment. Planning is read-only; execution, user routing decision, atomic publication, cleanup, and downstream work have independent authority. Evidence is bound to exact source/dependency/toolchain/build/run receipts, and only the user can select recoverable routing state.

## Contract identity

- Skill: `.agents/skills/prototype/SKILL.md`
- Continuation contract: `.agents/skills/prototype/references/continued-workflow.md`
- Metadata: `.agents/skills/prototype/agents/openai.yaml`
- Run receipt: `cgs.prototype-run-receipt/v1`
- Build receipt: `cgs.prototype-build-receipt/v1`
- Play receipt: `cgs.prototype-play-receipt/v1`
- Skip record: `cgs.prototype-skip/v1`
- Consent record: `cgs.prototype-consent/v1`
- Pivot record: `cgs.prototype-pivot/v1`
- Graveyard event: `cgs.prototype-graveyard-event/v1`
- Cleanup receipt: `cgs.prototype-cleanup-receipt/v1`

## Invocation

```text
$prototype <concept-or-question> [--path html|engine|paper] [--spike]
           [--pivot <pivot-record-path> --expect-pivot <sha256:...>]
```

A missing concept/question prints usage with zero project reads, agents, worktrees, directories, checkpoints, dependencies, or writes. Pivot path/hash must be supplied together and identify one exact immutable record; moving aliases are rejected.

## P0 invariants retained

1. No persistent write—including worktree/temp/root/checkpoint/dependency/cache—occurs before exact execution authorization.
2. All experiment mutations remain under one new authorized isolated root and cannot contaminate production source/assets/tests/design/state.
3. Iteration, command, failure, time, file, byte, dependency-resolution, and play-session budgets are monotonic and necessarily terminate.
4. Agents/reviewers emit advisory recommendations only. `USER_DECISION` requires explicit user selection.
5. Execution authorization never grants publication, cleanup beyond its exact manifest, product/design approval, or downstream authority.
6. REPORT/index/DECISION/pivot/graveyard publish as one CAS-guarded all-or-none transaction or remain non-authoritative.
7. `run_status: COMPLETE` means only bounded experiment/evidence protocol completion; `product_approval: NOT_GRANTED` remains true.

## P1 requirements

### A. No unsupported success probability — PROTO-P1-001

1. HTML, engine, paper, and spike modes are compared by evidence capabilities and limitations, not generic probability.
2. No inherited, anecdotal, or generic numeric success rate may guide selection without exact dataset path/hash, sample/outcome definition/count, period, uncertainty, and applicability to the current hypothesis.
3. Without applicable measurement, record `mode_success_probability: NOT_ESTABLISHED`.
4. Recommendation confidence is evidence quality/limitations, not an invented probability.

### B. Dependency lock, version, build, and dirty-worktree identity — PROTO-P1-002

1. Read-only preflight records repository/root/VCS/commit/branch/Git/submodule identity; pre-existing dirty/untracked path inventory and canonical hash; exact context hashes; OS/architecture; engine/runtime/SDK/compiler/build/package-manager versions and executable hashes where available.
2. Dependency manifest, lockfile, registry/source, cache/offline state, build config, environment allowlist, and generated-output boundaries are explicit and hash-bound.
3. `latest`, floating ranges, mutable URLs, global installs/caches, and unlocked dependency resolution cannot support reproducible build claims.
4. A needed lockfile may be created only inside the prototype root after execution authorization, from an exact pinned dependency manifest/source. Production/global dependencies and lockfiles are unchanged.
5. `build_identity_sha256` binds prototype/run, source manifest, dependency manifest/lock, toolchain, build config, exact command/arguments, and environment allowlist.
6. `cgs.prototype-build-receipt/v1` records exact command/working directory/times/exit/result, identity hashes, toolchain versions, artifacts/log/generated-manifest hashes, and outside-root mutations.
7. PASS requires actual execution, zero exit, expected current artifacts, matching identity, and zero unapproved outside mutation.

### C. Isolation fallback and original-worktree protection — PROTO-P1-003

1. Preferred Git worktree path/base/metadata actions are exact and execution-authorized.
2. If unavailable, no silent fallback occurs. User chooses `isolated_temp_root`, `current_workspace_bounded_root`, or `CANCEL` after a regenerated preview.
3. Every fallback uses a new absent exact root, validates parent/symlink/junction/reparse boundaries, redirects caches/temp/build/user data, and enforces bidirectional production/prototype isolation.
4. Original dirty-worktree manifest is compared before/after every command. Unexpected change is BLOCKED, logged with hashes, never reverted or retroactively authorized.
5. Uncontainable tools do not run.
6. Retention is explicitly `RETAIN`, `CLEAN_AFTER_RECEIPT`, or `CLEAN_LATER`. Cleanup is never implied by KILL/completion.
7. Cleanup may target only the exact newly created root/worktree after receipt preservation and explicit destructive authorization; otherwise retain it with `CLEANUP_REQUIRED`.
8. Cleanup emits a hash-bound receipt and never deletes pre-existing/user/production data.

### D. Run receipt and source-hash provenance — PROTO-P1-004

1. Every run finalizes immutable `RUN-RECEIPT.yaml` as `cgs.prototype-run-receipt/v1`.
2. It binds prototype/run/hypothesis/pivot, skill/continuation-contract paths and hashes, execution authorization, isolation/cleanup, source/dirty manifests, dependency manifest/lock, toolchain/build config/environment/generated outputs, checkpoint chain, commands, build/play/skip/consent/redaction/evidence hashes, budgets/status, draft/proposal, and cleanup receipt.
3. Debrief, recommendation, REPORT, DECISION, index, pivot, and graveyard facts cite the exact run-receipt path/hash and relevant source/build/play hashes.
4. Missing/stale/inconsistent receipt prevents current fact publication and caps recommendation at INCONCLUSIVE.
5. Run receipt and prior receipts are immutable; continuation revalidates exact bytes rather than copying narrative.

### E. Typed skip taxonomy — PROTO-P1-005

Every unexecuted/inapplicable planned step emits `cgs.prototype-skip/v1` with step ID, taxonomy, reason, current evidence/hash, actor/source, time, scope, affected signal/claim, recommendation ceiling, and recovery condition.

Allowed taxonomy is exactly:

- `NOT_APPLICABLE`
- `USER_ACCEPTED_RISK`
- `ENVIRONMENT_BLOCKED`
- `DEPENDENCY_UNAVAILABLE`
- `BUDGET_EXHAUSTED`
- `CONSENT_WITHHELD`
- `UNSUPPORTED_MODE`
- `NOT_REQUESTED`
- `FAILED_PRECONDITION`

Free-text skip is invalid. NOT_APPLICABLE requires a false applicability predicate and evidence. USER_ACCEPTED_RISK needs an exact explicit user response and cannot waive safety, containment, privacy, authorization, destructive-action, identity, or evidence integrity. A skip is never PASS/MET/OBSERVED/evidence of absence. Essential build/play/consent skips force INCONCLUSIVE for affected claims.

### F. Correct design routing — PROTO-P1-006

1. PROCEED is never routed directly to `design-review design/gdd/game-concept.md`.
2. Prototype does not recreate stage heuristics; it uses explicit current artifacts/receipts or reports routing state unknown.
3. Advisory routing is:
   - absent/draft/disputed/unapproved concept → concept owner / brainstorm-class concept authoring or revision;
   - explicitly approved/frozen concept without reviewed systems index → map-systems-class owner;
   - reviewed systems index with missing system GDD → design-system-class owner;
   - complete exact system GDD → `design-review <exact-system-gdd>` owner;
   - technical-only evidence → bounded technical owner handoff.
4. Every route is descriptive only and needs a separate exact task/authorization. No downstream workflow runs automatically.
5. PROCEED does not freeze a concept, approve GDD/architecture/assets, create epics/stories/sprints, or authorize production work.

### G. Pivot lineage — PROTO-P1-007

1. PIVOT selection creates no new run or authorization.
2. `cgs.prototype-pivot/v1` binds pivot ID, parent prototype/run/hypothesis/run-receipt/source/build/play hashes, previous threshold/evidence, retained facts, invalidated/unknown assumptions, changed variable(s), new falsifiable hypothesis/threshold/mode, changed scope/exclusions, dependency/toolchain/privacy changes, new hard budget/isolation proposal, and duplication check.
3. Record begins `authorization_state: NOT_AUTHORIZED`, `next_run_id: NOT_CREATED`.
4. It publishes only with the atomic group.
5. A future `--pivot` run requires exact path/hash and validates parent lineage before planning; it receives new IDs/root/budget/changeset.
6. Evidence carries forward only by exact hashes, never copied narrative. Invalid/missing lineage cannot silently repeat the experiment.

### H. Privacy and consent — PROTO-P1-008

1. Before participant feedback, recording, telemetry, personal logs, direct quotes, or identifiers, show purpose, participant type, data categories/method, recording types, storage/access/recipients, retention/cleanup, quote/anonymization, decline/withdrawal, and excluded sensitive data.
2. Consent is explicit per participant and data category in `cgs.prototype-consent/v1`; silence is no consent.
3. Feedback consent does not imply recording, quote, publication, or identity-disclosure consent.
4. Minors/vulnerable participants require an applicable owner-approved policy and necessary guardian/organizational consent; otherwise `CONSENT_WITHHELD`.
5. Secrets/credentials/private keys are never persisted. Collection is minimized and participants are pseudonymized.
6. Raw personal/sensitive evidence is quarantined in an authorized restricted root or not written, never published/indexed, and remains BLOCKED until an authorized redaction receipt exists.
7. Withdrawal stops collection and marks evidence `WITHDRAWN_NOT_USABLE`; deletion/retention follows explicit authority.
8. Play receipts bind pseudonymous participant, consent, build/run/source, protocol/facts/reports/measurements/redaction/evidence and keep observed fact, participant report, model inference, and not observed separate.

### I. Recoverable explicitly confirmed KILL — PROTO-P1-009

1. KILL recommendation, initial user selection, explicit KILL confirmation, graveyard publication authorization, cleanup, and reopening are separate actions.
2. Confirmation is bound to exact prototype/run/run-receipt and states non-deletion, retained evidence, proposed graveyard/index state, reopen semantics, and separate publication approval.
3. Only unambiguous affirmative confirmation produces `USER_DECISION: KILL` and state `USER_KILLED_RECOVERABLE`; otherwise decision remains PENDING and no graveyard event is written.
4. `cgs.prototype-graveyard-event/v1` binds exact evidence/confirmation hashes, reason, what worked, retained/reusable evidence, privacy limits, reopen prerequisites, and `destructive_cleanup_authorized: false`.
5. KILL never deletes source/prototype/evidence/report/branch/worktree and is never forced by pivot/iteration count.
6. REOPEN requires future explicit user confirmation plus a separate atomic publication transaction, appends a linked event, preserves history, and starts no prototype automatically.

## Evidence and recommendation contract

The continuation reference is mandatory and its previewed SHA-256 is revalidated before use. It validates the entire current run packet and excludes stale, withdrawn, consent-restricted, differently hashed, or mixed-contract evidence.

Draft sections separate experiment/receipt identity, observed facts, participant reports, build/play results, typed skips/unsupported scope, not-run/not-observed/withdrawn items, model inferences, and recommendation.

Recommendation values are `PROCEED | PIVOT | KILL | INCONCLUSIVE`. An optional reviewer is advisory only. No reviewer/director can change receipts, select a user decision, or mutate publication.

User routing values are `PROCEED | PIVOT | KILL | DEFER | MORE_EVIDENCE | PENDING`. Exact response/options/receipt/time/record hash are retained; the selection itself writes nothing.

## Execution authorization and finite loop

The complete execution preview includes exact isolation actions, authored paths, local locks, receipts, consent paths, generated subtrees, commands, dependency sources, toolchain/build/environment identity, source/dirty snapshots, budgets/deadline, privacy/retention/cleanup, operations/owners/base hashes/byte ceilings, non-writes, and excluded publication paths.

Any expansion or drift requires a new preview/authorization. Counters increment before work; limit exhaustion stops tools and does not reset/extend in place. Checkpoint resume verifies the hash chain and all source/lock/toolchain/build/evidence/consent/pivot/dirty identities.

## Atomic publication contract

After a valid explicit user decision, the proposed group contains final REPORT, DECISION, exact index change, PIVOT-NOTE for PIVOT, graveyard event only for confirmed KILL, and authorized transaction paths. Every member shares transaction ID, run-receipt/source/lock/toolchain/build/play hashes, skip/privacy state, recommendation, exact decision record, scope `EXPERIMENT ROUTING ONLY — NOT PRODUCT APPROVAL`, and recovery lineage.

Execution authorization, consent, recommendation, user selection, and content approval do not authorize publication. Preview exact paths/operations/owners/base hashes/content and recovery mechanics, then obtain publication authorization.

Before commit, CAS all targets and evidence identities, stage/cross-validate, and prove atomic apply or safe rollback. Any failure modifies no final target and returns `PARTIAL — PUBLICATION_NOT_COMMITTED`. Read-back inconsistency is BLOCKED and is never presented as authoritative.

## Behavioral cases

### Case 1 — No generic success-rate guidance

No applicable dataset exists. Mode options show capabilities/limitations and `mode_success_probability: NOT_ESTABLISHED`; no percentage appears. A dataset-backed percentage includes every required provenance/applicability field.

### Case 2 — Dirty worktree and reproducible build

Pre-existing user changes are frozen by path/hash. Build uses pinned engine/toolchain and prototype-local lock. Actual receipt binds exact source/lock/config/command/artifacts. A changed outside-root file blocks the run and is not reverted.

### Case 3 — Worktree fallback

Requested worktree cannot be created. Zero writes occur until the user explicitly chooses temp, bounded current root, or cancel and approves a regenerated changeset. Temp retention/cleanup and original-tree postchecks are explicit.

### Case 4 — Receipt-bound publication facts

A build/debrief exists but RUN-RECEIPT hash is stale. Recommendation becomes INCONCLUSIVE and no report/index fact publishes as current. Revalidation with matching receipt enables a proposal.

### Case 5 — Skip taxonomy

Environment lacks the pinned engine. Record ENVIRONMENT_BLOCKED with current evidence and affected claim; do not mark pass. User risk acceptance cannot waive the missing executable or privacy boundary.

### Case 6 — Correct PROCEED routing

Concept is a draft and no system GDD exists. Advisory route is concept authoring/revision, not `design-review game-concept.md`; nothing executes. When a complete exact system GDD exists, only that GDD may be named for design review.

### Case 7 — Bound PIVOT

The user selects PIVOT. Record parent receipt/failure evidence, one changed assumption, new threshold, exclusions/budget, and duplication check. The next run fails closed without exact pivot path/hash and always uses new IDs/root/authorization.

### Case 8 — Consent and withdrawal

An external participant accepts text feedback but rejects recording/publication. Only consented minimized feedback is usable; no recording/quote publication occurs. Later withdrawal marks linked evidence unusable and lowers the recommendation ceiling without silent deletion.

### Case 9 — KILL pending/confirmed/reopened

Agent recommends KILL; user is silent: PENDING and no graveyard. User explicitly confirms exact KILL: recoverable event is proposed, evidence retained, no deletion. Publication requires separate approval. Later REOPEN appends history after explicit confirmation and launches nothing.

### Case 10 — P0 authorization and bounded-loop regression

Before execution approval, filesystem is unchanged. Two consecutive failures at the limit stop commands. No agent chooses a final decision. Publication CAS conflict leaves no half-authoritative report/index/decision/graveyard.

## Negative assertions

Any of these is a contract failure:

- unsupported numeric success-rate guidance;
- executable build without exact dependency lock/toolchain/source identity;
- silent isolation fallback, global install/cache, production-lock mutation, or automatic revert of dirty worktree;
- debrief/index fact without exact run receipt/source hashes;
- free-text or pass-equivalent skip;
- direct PROCEED route to concept-file design review;
- pivot without exact parent failure evidence and changed hypothesis/threshold;
- recording, quote, personal data, or publication without category-specific consent/redaction;
- forced, agent-owned, destructive, unconfirmed, or irreversible KILL;
- cleanup implied by KILL;
- execution approval treated as publication/downstream authority.

## Remediation traceability

| Finding | Closure evidence |
|---|---|
| PROTO-P1-001 | Section A removes generic percentages and requires measured dataset provenance/applicability |
| PROTO-P1-002 | Section B pins lock/toolchain/build/source/dirty/generated identities and receipt semantics |
| PROTO-P1-003 | Section C defines explicit fallback choices, original-worktree guards, retention and cleanup receipts |
| PROTO-P1-004 | Section D makes immutable run receipt/source hashes mandatory for all downstream facts |
| PROTO-P1-005 | Section E defines exclusive typed skip taxonomy and claim ceilings |
| PROTO-P1-006 | Section F maps concept → systems → system GDD → review correctly and forbids direct concept-file review |
| PROTO-P1-007 | Section G binds each pivot to parent failure evidence, changed hypothesis/criteria, and new-run identity |
| PROTO-P1-008 | Section H defines consent categories, minimization, redaction, withdrawal, retention, and receipt binding |
| PROTO-P1-009 | Section I separates recommendation/confirmation/publication/cleanup/reopen and preserves recoverable history |

## Final outcome fields

Every result independently reports run/build/play/recommendation/user-decision/decision-record/run-receipt/publication/cleanup status, exact evidence identities, `product_approval: NOT_GRANTED`, and `auto_executed_downstream: false`.
