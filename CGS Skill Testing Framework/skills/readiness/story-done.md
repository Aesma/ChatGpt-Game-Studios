# Skill Test Spec: $story-done

## Contract identity

- Spec ID: `skill-spec.story-done/v2`
- Spec schema: `cgs-skill-spec/v2`
- Category: `readiness`
- Priority: `critical`
- Spec written: `2026-07-23`
- Skill path: `.agents/skills/story-done/SKILL.md`
- Metadata path: `.agents/skills/story-done/agents/openai.yaml`
- Dev-story contracts: `cgs.dev-story-result/v2`, `cgs.dev-story-plan/v2`, `cgs.dev-story-status-transition-proposal/v2`, `cgs.dev-story-status-transaction/v2`, `cgs.dev-story-checkpoint/v2`, and `cgs.dev-story-test-execution/v2`
- Lifecycle authority: immutable `cgs.story/v2`, canonical `cgs.sprint-tracker/v2`, and tracker-declared lifecycle recorder
- Readiness contracts: `cgs.story-readiness-record/v1` and `cgs.story-readiness-recorder-receipt/v1`
- Test contracts: `cgs.dev-story-test-execution/v2` and `cgs.manual-evidence/v1`
- Gate contracts: `cgs.team-qa-result/v2`, `cgs.team-qa-signoff/v2`, `cgs-test-evidence-review-report/v2`, `cgs.story-review-policy/v1`, `cgs.review-evidence/v1`, `cgs.code-review/v2`, `cgs.code-review-recorder-receipt/v1`, and `cgs.review-waiver/v1`
- Owner decision: `cgs.design-equivalence-decision/v1`
- Closure contracts: tracker-only `cgs.story-closure-transaction/v1` and `cgs.story-closure-receipt/v1`
- Closure evaluator/request owner: `story-done`; canonical lifecycle writer: tracker-declared `cgs.sprint-tracker/v2` recorder

## Skill summary

`$story-done` is a fail-closed closure evaluator. It revalidates immutable story requirements, a current tracker row exactly `in_review`, the exact dev-story result/plan/proposal/recorder receipt and execution evidence, required QA/review evidence, and authorized design-equivalence decisions. A closable result only requests the unique tracker lifecycle recorder to change that one row to `done`. Story bytes/Revision, sprint plan bytes, `plan_sha256`, `plan_revision`, `story_set_hash`, session state, and all unowned tracker fields remain immutable.

## Static assertions

- [ ] SD-S001: Frontmatter contains only `name` and non-empty `description`
- [ ] SD-S002: Frontmatter name equals the `story-done` directory
- [ ] SD-S003: Invocation accepts one optional exact story path and one review mode
- [ ] SD-S004: The immutable story identity/hash matches a canonical tracker row exactly `in_review`
- [ ] SD-S005: Story-done owns closure evaluation/request only; the tracker-declared lifecycle recorder is sole canonical writer
- [ ] SD-S006: Only `cgs.dev-story-result/v2` outcome IMPLEMENTED with exact proposal and verified recorder result/receipt ending at `in_review` is admissible
- [ ] SD-S007: A persisted current READY record and matching recorder receipt are both revalidated
- [ ] SD-S008: Closure requires `implementation_gate_eligible: true`; accepted-risk or NEEDS_WORK readiness is blocking
- [ ] SD-S009: Test execution consumes the exact `cgs.dev-story-plan/v2` and `cgs.dev-story-test-execution/v2` set
- [ ] SD-S010: Test definitions bind IDs, locator, executable, argv, cwd, environment, timeout, and expected result
- [ ] SD-S011: Run evidence binds command context, timestamps, termination, exit, logs, tree, and per-test results
- [ ] SD-S012: TIMEOUT, partial, missing, changed, or unexecuted test evidence is blocking
- [ ] SD-S013: Verification tree canonicalization includes dev result, plan, transition receipt, and execution-set hashes
- [ ] SD-S014: Every required AC needs direct current PASS evidence
- [ ] SD-S015: Static searches and conversational confirmations are findings only
- [ ] SD-S016: Manual evidence binds identity, session, steps, observation, tree/build, artifacts, and hashes
- [ ] SD-S017: All five Story Type rows are blocking
- [ ] SD-S018: Exact current `cgs.team-qa-result/v2` and persisted `cgs.team-qa-signoff/v2` agree on `QA_APPROVED` and Gate Eligible YES
- [ ] SD-S019: Any Team QA condition, gap, incomplete/nonpass row, stale identity, or unpersisted signoff blocks closure
- [ ] SD-S020: Logic and high-risk stories require review in full, lean, and solo
- [ ] SD-S021: Review policy is predeclared and hash-bound
- [ ] SD-S022: Review skip blocks unless an authorized policy-permitted waiver is current
- [ ] SD-S023: Design mismatch defaults to blocking
- [ ] SD-S024: Functional equivalence requires an authorized owner decision with exact source/subject hashes
- [ ] SD-S025: Owner decisions cannot waive behavior, QA, review, or type evidence
- [ ] SD-S026: Evidence verdict and lifecycle commit are separate states
- [ ] SD-S027: Story-done never writes tracker, story, plan, session, planning hashes, or evidence artifacts directly
- [ ] SD-S028: Closure proposal binds exact tracker CAS tuple, one row transition, lifecycle-owned fields, preservation assertions, rollback, and authorization
- [ ] SD-S029: Recorder capability requires tracker/receipt atomic commit or verified rollback, recovery, and immutable receipt
- [ ] SD-S030: Only a verified COMMITTED receipt and independent read-back permits a Complete verdict
- [ ] SD-S031: Closure preserves story bytes/Revision, plan bytes, `plan_sha256`, `plan_revision`, and `story_set_hash`; none are recomputed
- [ ] SD-S032: No follow-on workflow, commit, push, or publication is automatic
- [ ] SD-S033: Review consumes exact `cgs.review-evidence/v1` plus embedded `cgs.code-review/v2`, never an invented code-review receipt
- [ ] SD-S034: Closure requires an independent current recorder receipt with PERSISTED and `gate_evidence_eligible: true`

## Behavioral cases

### Case 1: Fully current Logic story closes through one tracker-only transaction

#### Fixture

- Immutable `cgs.story/v2` ID/path/hash matches one tracker row exactly `in_review`
- Current persisted READY record, matching recorder receipt, and every stale-key source hash match
- One IMPLEMENTED dev result binds its exact plan, final transition proposal, verified recorder result/receipt, no checkpoint, and two Logic ACs mapped to passing immutable executions
- Tracker planning tuple and all unowned fields are current and frozen
- Team QA result/signoff are current, persisted, `QA_APPROVED`, and Gate Eligible YES
- Required code-review envelope/extension is current `APPROVED` and an exact independent recorder receipt proves PERSISTED/gate eligible
- Tracker lifecycle recorder capability and receipt destination are current

#### Input

`$story-done production/stories/STORY-101.md --review lean`

#### Expected reads

Immutable story, sprint plan/tracker, dev result/plan/final proposal/transaction receipt, readiness record/receipt/sources, test executions/logs, Team QA result/signoff, review policy/evidence/receipt, implementation tree, and recorder capability.

#### Expected writes

Only the tracker-declared recorder may replace the tracker with one row `done` and create the immutable closure receipt.

#### Expected non-writes

Story bytes/Revision, sprint plan, planning hashes, session state, every other tracker row/unowned field, implementation, tests, requirements, and review evidence.

#### Expected behavior

Recompute all hashes, produce a closable evidence verdict, preview once, obtain authorization, invoke the unique recorder, verify `COMMITTED` and independent read-back, then report `COMPLETE`.

#### Assertions

- [ ] SD-C01-A: Exact dev plan/execution command contexts and log hashes support each AC
- [ ] SD-C01-B: Only lifecycle-owned fields of the matching tracker row change `in_review -> done`
- [ ] SD-C01-C: Story/plan/planning tuple remain byte-identical and Complete is reported only after receipt read-back

#### Case Verdict

PASS when all assertions hold; otherwise FAIL.

### Case 2: Static presence cannot rescue failed behavior

#### Fixture

A source file, expected function, boundary number, and matching test name exist,
but the declared test exits nonzero and records FAIL.

#### Input

The exact In Review story path.

#### Expected reads

Current source, dev-story plan/result, failing execution record/log, and all
ordinary sources.

#### Expected writes

None.

#### Expected non-writes

Story, tracker, session, closure request, and closure receipt.

#### Expected behavior

Report static matches as findings, mark the AC FAIL, and return `BLOCKED`
without a close-anyway branch.

#### Assertions

- [ ] SD-C02-A: File/function/number/name presence never becomes PASS
- [ ] SD-C02-B: Direct failing behavior controls the AC result
- [ ] SD-C02-C: COMPLETE WITH NOTES is not offered

#### Case Verdict

PASS when all assertions hold; otherwise FAIL.

### Case 3: Required gap blocks while a predeclared optional deferral is a note

#### Fixture

Variant A has one UNTESTED required AC. Variant B has all required ACs passing
and one optional AC whose classification is unchanged across story, profile,
plan, and dev-story result hashes.

#### Input

Run each variant independently.

#### Expected reads

Exact AC declarations, Definition-of-Done profile, dev-story plan/result, and
mapped evidence.

#### Expected writes

Variant A writes nothing. Variant B may enter the atomic closure transaction
after approval.

#### Expected non-writes

No runtime edit may change an AC classification.

#### Expected behavior

Variant A returns `BLOCKED` regardless of the missing percentage. Variant B
may return `COMPLETE WITH NOTES` and name the optional deferral.

#### Assertions

- [ ] SD-C03-A: One required UNTESTED/DEFERRED/STALE/FAIL result blocks
- [ ] SD-C03-B: Optional status cannot be invented at closure
- [ ] SD-C03-C: No percentage threshold exists

#### Case Verdict

PASS when both variants match; otherwise FAIL.

### Case 4: Every Story Type evidence row is blocking

#### Fixture

Run Logic, Integration, Visual/Feel, UI, Config/Data, and unknown-type variants;
each lacks one declared type obligation while ordinary AC evidence otherwise
passes.

#### Input

One exact story per variant.

#### Expected reads

Story Type, unchanged profile, dev-story plan mappings, manual/automated evidence,
artifacts, smoke records, and sign-offs as applicable.

#### Expected writes

None for every variant.

#### Expected non-writes

No type profile, sign-off, or status projection is created or edited.

#### Expected behavior

Each known type returns `BLOCKED` for its missing obligation; unknown type
also returns `BLOCKED`.

#### Assertions

- [ ] SD-C04-A: Missing visual/UI artifacts or sign-off is not advisory
- [ ] SD-C04-B: Config/Data requires current smoke evidence
- [ ] SD-C04-C: Mode or gate skip cannot bypass the matrix

#### Case Verdict

PASS when all variants block; otherwise FAIL.

### Case 5: Manual evidence is complete only on the exact current tree

#### Fixture

Variant A has a complete manual record with stable IDs, current tree/build,
steps, observation, PASS, tester, session timestamp, artifacts, and sign-offs.
Variant B changes one implementation byte after that session. Variant C is a
conversational Yes without a durable record.

#### Input

Run all variants with otherwise passing inputs.

#### Expected reads

Manual record, artifact/build bytes, dev-story plan declaration, and current
verification tree.

#### Expected writes

Variant A may proceed to an approved closure transaction. Variants B and C write
nothing.

#### Expected non-writes

The manual record is never rewritten to current by story-done.

#### Expected behavior

A may PASS; B is STALE/BLOCKED; C is UNTESTED/BLOCKED.

#### Assertions

- [ ] SD-C05-A: Identity/session/behavior/artifact/hash fields are all enforced
- [ ] SD-C05-B: Tree/build drift invalidates the record
- [ ] SD-C05-C: Conversation is not a manual test

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 6: Readiness is checked on current hashes

#### Fixture

Variant A has a persisted current READY record with
`implementation_gate_eligible: true` and a matching `RECORDED` receipt. Variant
B has the same prior record but the GDD changed. Variant C has a direct READY
candidate with no recorder receipt. Variant D has a persisted NEEDS_WORK record
used by dev-story under structured accepted risk. Variant E has a record/receipt
pair whose registry-final hash no longer matches current bytes.

#### Input

Run each variant independently.

#### Expected reads

Record, recorder receipt, readiness registry, TR registry, control manifest,
GDDs, ADRs, profile, story snapshot, and every stale-key source.

#### Expected writes

Only A may later enter an approved closure transaction.

#### Expected non-writes

No record, receipt, registry, source, or story provenance is refreshed here.

#### Expected behavior

A continues. B blocks on current-byte drift; C blocks because the candidate is
not persisted; D blocks because readiness is not READY/gate eligible; E blocks
because receipt/registry identity is not current.

#### Assertions

- [ ] SD-C06-A: A persisted record/receipt never substitutes for current-byte validation
- [ ] SD-C06-B: Record, candidate, readiness key, story hash, and registry-final hash joins are exact
- [ ] SD-C06-C: Only current persisted READY with `implementation_gate_eligible: true` is closable

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 7: Dev result, plan, transition proposal, and recorder receipt are mandatory and exact

#### Fixture

Run missing result, unknown schema, non-IMPLEMENTED outcome, missing plan, duplicate Test ID, changed argv/cwd/environment, unbounded timeout, unresolved checkpoint, missing/mismatched proposal, partial/ambiguous recorder receipt, changed immutable story, changed planning tuple, and fully valid variants.

#### Input

The exact dev-story evidence set except for the named variant.

#### Expected reads

Result, plan, final status-transition proposal, status-transaction result/receipt, immutable story, canonical tracker row/read-back, checkpoint when referenced, and declared inputs.

#### Expected writes

None for invalid variants.

#### Expected non-writes

No ad hoc command, replacement result/plan/receipt, story projection, lifecycle normalization, or planning-hash rewrite is invented.

#### Expected behavior

Every invalid variant returns `BLOCKED`; only `IMPLEMENTED` with no checkpoint and a verified recorder transaction ending at canonical tracker row `in_review` continues.

#### Assertions

- [ ] SD-C07-A: Canonical paths/schemas/raw hashes identify one joined result/plan/proposal/receipt/tracker set
- [ ] SD-C07-B: Test ID/argv/cwd/environment/runner/source/build/timeout/log contract is immutable
- [ ] SD-C07-C: PARTIAL/FAILED/BLOCKED, receipt ambiguity, story/planning change, and free-form shell text are blocking

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 8: Execution evidence preserves command, logs, and partial terminals

#### Fixture

Run PASS, TIMEOUT, partial log, missing exit, nonzero exit, changed environment,
log-hash mismatch, and evidence-tree mismatch variants for one declared test.

#### Input

The same exact dev-story plan/result with one execution record variant at a time.

#### Expected reads

Execution record, plan row, raw log, result-set identity, and current tree.

#### Expected writes

None for invalid or non-PASS variants.

#### Expected non-writes

Execution records and logs are immutable and never normalized after the fact.

#### Expected behavior

Only normal termination, exit zero, PASS, exact command context, exact current
tree, and matching log hashes can support the mapped AC.

#### Assertions

- [ ] SD-C08-A: TIMEOUT and partial are blocking terminals
- [ ] SD-C08-B: Exit/result/log/tree axes are checked separately
- [ ] SD-C08-C: Prose test summaries cannot fill missing fields

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 9: Team QA signoff gaps and nonpass terminals are blocking

#### Fixture

Variant A is `QA_APPROVED`/YES with every required row current. Variant B is
`QA_APPROVED_WITH_CONDITIONS`/NO. Variant C is `QA_INCOMPLETE` with one required
TIMEOUT. Variant D says `QA_APPROVED` in the result but its signoff is absent.
Variant E has a stale candidate/build join.

#### Input

Each exact `cgs.team-qa-result/v2` plus its named signoff in turn.

#### Expected reads

QA result/signoff, frozen evidence manifest, independent review, exact required
denominator, scope/candidate/build/artifact/source/plan hashes, roles, findings,
conditions, persistence, and raw hashes.

#### Expected writes

Only A may later enter closure when all other checks pass.

#### Expected non-writes

QA artifacts, finding dispositions, denominator, and AC classification remain
unchanged.

#### Expected behavior

A satisfies only the QA evidence gate; it does not grant closure. B through E
block without normalization or inferred signoff.

#### Assertions

- [ ] SD-C09-A: Only persisted current QA_APPROVED with Gate Eligible YES satisfies the QA evidence gate
- [ ] SD-C09-B: Result/signoff and every scope/build/evidence identity join exactly
- [ ] SD-C09-C: QA approval grants no closure authority and positive tests do not override nonpass QA

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 10: Lean or solo cannot skip required Logic review

#### Fixture

A Logic story has a current policy requiring review and all tests/QA pass.
Variant A has no review envelope. Variant B has an APPROVED
`cgs.review-evidence/v1` + `cgs.code-review/v2` producer record that remains
NOT_PERSISTED/gate-ineligible. Variant C has a recorder receipt for a stale raw
hash. Exercise lean and solo modes plus a user answer of No/skip.

#### Input

`$story-done production/stories/STORY-LOGIC-202.md --review lean` and the same
path with `--review solo`.

#### Expected reads

Policy, Story Type/risk class, plan, tree, envelope/extension when present,
stale key, recorder receipt/registry when present, and all current bound inputs.

#### Expected writes

None.

#### Expected non-writes

No completion projection and no fabricated waiver.

#### Expected behavior

All variants return `BLOCKED`; conversational skip, APPROVED alone, or a stale
recorder receipt cannot change policy or persistence eligibility.

#### Assertions

- [ ] SD-C10-A: Logic/high-risk review is mode independent
- [ ] SD-C10-B: Missing/ambiguous policy fails closed
- [ ] SD-C10-C: No/skip is not APPROVED
- [ ] SD-C10-D: NOT_PERSISTED/gate-ineligible review evidence cannot close
- [ ] SD-C10-E: Recorder receipt must bind the exact current envelope and stale-key inputs

#### Case Verdict

PASS when all variants block; otherwise FAIL.

### Case 11: Only a policy-permitted current review waiver is non-blocking

#### Fixture

Variant A has a policy that permits waiver plus a signed current risk-owner
waiver bound to policy/story/plan/result/tree hashes. Variant B has a policy
that forbids waiver. Variant C has an expired or stale waiver.

#### Input

Run each variant without persisted eligible code-review evidence.

#### Expected reads

Policy, authority source, waiver, signature/attestation, and all bound bytes.

#### Expected writes

Only A may later close, with notes.

#### Expected non-writes

Policy and waiver records remain immutable.

#### Expected behavior

A may satisfy the review condition as `COMPLETE WITH NOTES`; B and C block.

#### Assertions

- [ ] SD-C11-A: Waiver authority and permission are both required
- [ ] SD-C11-B: Waiver scope and hashes match the exact current candidate
- [ ] SD-C11-C: Waiver cannot cover QA or behavioral gaps

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 12: Subjective functional equivalence is rejected

#### Fixture

Implementation differs from an exact GDD or Accepted ADR rule, while the
implementer or model says the result is functionally equivalent. No owner
decision record exists.

#### Input

The exact story and mismatching source/implementation evidence.

#### Expected reads

Requirement ID/path/locator/hash, subject path/hash, AC mapping, and review
findings.

#### Expected writes

None.

#### Expected non-writes

No requirement, ADR, implementation, owner record, or status is modified.

#### Expected behavior

Create a stable blocking mismatch finding and request the designated product or
architecture owner decision.

#### Assertions

- [ ] SD-C12-A: Model judgment cannot resolve the mismatch
- [ ] SD-C12-B: Similar outcomes or wording are insufficient
- [ ] SD-C12-C: The exact owner and evidence needed are named

#### Case Verdict

PASS when the mismatch blocks; otherwise FAIL.

### Case 13: Exact owner decision resolves only its named design scope

#### Fixture

Variant A has a signed current owner decision binding exact authority, source,
subject, AC, dev-story plan/result, tree, semantic comparison, regression evidence,
scope, and expiry. Variant B changes one source byte. Variant C has missing owner
authority. Variant D asks the decision to waive a failed test.

#### Input

Each decision record with otherwise identical evidence.

#### Expected reads

Decision, authority/signature, named sources/subjects, and regression evidence.

#### Expected writes

Only A may later enter closure.

#### Expected non-writes

Decision and governed artifacts remain unchanged.

#### Expected behavior

A resolves only the named mismatch. B, C, and D return `BLOCKED`.

#### Assertions

- [ ] SD-C13-A: Decision scope and current hashes are exact
- [ ] SD-C13-B: Expired/revoked/stale/unauthorized decisions fail
- [ ] SD-C13-C: Owner decision cannot manufacture test PASS

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 14: Lifecycle recorder unavailability or CAS conflict prevents canonical writes

#### Fixture

Variant A has no declared tracker lifecycle recorder capability. Variant B changes tracker bytes/revision/event after preview. Variant C collides with a non-identical create-only receipt path. Variant D changes plan/story bytes before commit.

#### Input

A closable evidence verdict and approved tracker-only closure proposal.

#### Expected reads

Recorder identity/capability, proposal/authorization hashes, every evidence hash, immutable story/plan hashes, exact tracker preimage/CAS tuple, and receipt destination.

#### Expected writes

None.

#### Expected non-writes

Tracker, receipt path, story, plan, planning hashes, session state, implementation, and sources.

#### Expected behavior

Abort before commit and return `BLOCKED` with the exact conflict; do not retry against a new preimage.

#### Assertions

- [ ] SD-C14-A: Story-done direct tracker replacement and sequential cross-owner writes are forbidden
- [ ] SD-C14-B: Full tracker/story/plan CAS and preservation checks precede recorder commit
- [ ] SD-C14-C: Conflict/collision never mints a replacement transaction silently

#### Case Verdict

PASS when every variant leaves canonical bytes identical; otherwise FAIL.

### Case 15: Injected lifecycle-recorder failure restores the tracker preimage

#### Fixture

The recorder stages the exact tracker replacement and receipt, then an injected failure occurs after tracker replacement would otherwise become visible.

#### Input

One approved tracker-only `cgs.story-closure-transaction/v1`.

#### Expected reads

Proposal, staged bytes, tracker preimage, immutable story/plan hashes, recorder journal, and rollback data.

#### Expected writes

Only recorder-controlled rollback/journal/immutable aborted-receipt writes permitted by its capability; final tracker bytes equal the complete preimage.

#### Expected non-writes

No story, plan, session, planning-hash, evidence, or independent repair write.

#### Expected behavior

Return `ROLLED_BACK` or `RECOVERY_REQUIRED`, never Complete. If recovery is required, name the exact recorder recovery action and do not retry silently.

#### Assertions

- [ ] SD-C15-A: No partial `done` row survives verified rollback
- [ ] SD-C15-B: Story/plan/planning tuple stay unchanged and partial state cannot produce COMMITTED
- [ ] SD-C15-C: Recovery evidence is distinct from closure success

#### Case Verdict

PASS when no successful closure is reported and final tracker state matches the receipt; otherwise FAIL.

### Case 16: Dev-story terminal-state claim is rejected as owner drift

#### Fixture

A dev result, status proposal, or status-transaction receipt claims that dev-story committed tracker row `done`, mutated story bytes/Revision, or supplies a dev-authored closure receipt.

#### Input

The exact dev result/proposal/receipt set and current immutable story/tracker.

#### Expected reads

Story, tracker, dev producer schemas, proposal/result/receipt identities, and alleged closure receipt.

#### Expected writes

None.

#### Expected non-writes

No normalization of terminal state, story rewrite, tracker rewrite, planning-hash rewrite, or new closure receipt.

#### Expected behavior

Return `BLOCKED`, identify `in_review` as dev-story's only valid terminal row, and route producer evidence back for correction.

#### Assertions

- [ ] SD-C16-A: Dev-story may end only at canonical tracker row `in_review`
- [ ] SD-C16-B: Producer and lifecycle-recorder identities are validated
- [ ] SD-C16-C: Owner drift never becomes imported closure provenance

#### Case Verdict

PASS when the owner violation blocks; otherwise FAIL.

### Case 17: Test-evidence review summary keeps quality and execution separate

#### Fixture

Exercise `ADEQUATE + UNKNOWN`, `ADEQUATE + PASS + TARGETED`, stale hashes,
missing durable persistence, and fully current
`COMPLETE/ADEQUATE/PASS/FULL/Closure Eligible YES` variants.

#### Input

One exact persisted `cgs-test-evidence-review-report/v2` and its input manifest
identity per variant.

#### Expected reads

Every captured QA/story/build/test/smoke/playtest/manual/attestation path and
hash plus the direct AC evidence.

#### Expected writes

None from review consumption itself.

#### Expected non-writes

Review artifacts and direct evidence remain immutable.

#### Expected behavior

Only the fully current variant can summarize evidence; all others block. Even
the valid summary does not replace direct AC checks or Team QA result/signoff.

#### Assertions

- [ ] SD-C17-A: ADEQUATE alone never proves execution
- [ ] SD-C17-B: TARGETED cannot satisfy FULL closure scope
- [ ] SD-C17-C: Summary and direct evidence remain separate layers

#### Case Verdict

PASS when all variants match; otherwise FAIL.

### Case 18: Tracker-only closure preserves planning and story identity

#### Fixture

The active `cgs.sprint-tracker/v2` has valid sprint IDs/state, revision/event, lifecycle owner/recorder, exact plan path/hash/revision/story-set hash, and one matching row `in_review`. Story and plan raw bytes are frozen.

#### Input

A fully authorized tracker-only closure proposal with current CAS preimage.

#### Expected reads

Immutable story, plan, tracker preimage, dev transition receipt, closure proposal/authorization, recorder capability, and receipt destination.

#### Expected writes

The lifecycle recorder replaces only the tracker with the one permitted row transition and creates one immutable COMMITTED receipt.

#### Expected non-writes

Story bytes/Revision, plan bytes, `plan_sha256`, `plan_revision`, `story_set_hash`, session state, unrelated rows, unowned fields, implementation, and sources.

#### Expected behavior

Commit `in_review -> done`, re-read tracker/story/plan/receipt, verify the exact revision/event increment and preservation assertions, then report the evidence verdict.

#### Assertions

- [ ] SD-C18-A: Story-set hash is preserved byte-for-byte and never recomputed
- [ ] SD-C18-B: Only tracker-declared lifecycle-owned fields of the named row change
- [ ] SD-C18-C: Receipt tracker post-hash equals verified read-back and all protected hashes match preimages

#### Case Verdict

PASS when every assertion and receipt check holds; otherwise FAIL.

## Protocol compliance

- [ ] SD-P001: Read the complete selected story before evaluation or mutation
- [ ] SD-P002: Use raw SHA-256 for every mutable and evidence boundary
- [ ] SD-P003: Preserve exact stable IDs and reject ambiguous duplicates
- [ ] SD-P004: Keep readiness, evidence, QA, review, design, and lifecycle axes separate
- [ ] SD-P005: Present one deterministic evidence report before authorization
- [ ] SD-P006: Present the complete byte-exact transaction once
- [ ] SD-P007: Re-preview after any path, byte, preimage, authorization, or intent change
- [ ] SD-P008: Write nothing on a BLOCKED evidence verdict
- [ ] SD-P009: Use only the atomic recorder for lifecycle projection writes
- [ ] SD-P010: Treat ABORTED/ROLLED_BACK/RECOVERY_REQUIRED as non-closure
- [ ] SD-P011: Never overwrite immutable evidence, decision, transaction, or receipt records
- [ ] SD-P012: Never infer an owner approval, waiver, or PASS from conversation
- [ ] SD-P013: Never commit, push, publish, or invoke a follow-on workflow automatically
- [ ] SD-P014: Surface exact recovery/owner/evidence needs without claiming completion

## Verdict matrix

| Condition | COMPLETE | COMPLETE WITH NOTES | BLOCKED |
|---|---:|---:|---:|
| All required AC and type obligations current PASS | required | required | false or missing |
| Current readiness | persisted READY, eligible | persisted READY, eligible | stale/unpersisted/non-READY/ineligible |
| Dev result/plan/proposal/recorder receipt/executions valid | required | required | invalid/partial/non-IN_REVIEW |
| Team QA evidence | QA_APPROVED / YES | QA_APPROVED / YES | other/stale/unpersisted |
| Required review | APPROVED | APPROVED or valid policy-permitted waiver | missing/rejected/stale |
| Design mismatch | absent/resolved | absent/resolved with advisory risk | unresolved/subjective |
| Closure receipt | COMMITTED | COMMITTED | any other state |

## Audit remediation traceability

| Audit ID | Contract closure |
|---|---|
| SD-001 | Static assertions SD-S014–SD-S017 and Cases 2–5 forbid heuristic PASS |
| SD-002 | SD-S014 and Case 3 require every required AC to PASS |
| SD-003 | SD-S017 and Case 4 make every Story Type obligation blocking |
| SD-004 | SD-S016 and Case 5 require hash/session/identity-bound manual evidence |
| SD-005 | SD-S009–SD-S013 and Cases 7–8 consume exact dev-story plan/execution/log schemas |
| SD-006 | SD-S018–SD-S019 and Case 9 make every Team QA nonpass/condition/gap blocking |
| SD-007 | SD-S020–SD-S022 and Cases 10–11 enforce predeclared risk review/waiver policy |
| SD-008 | SD-S007–SD-S008 and Case 6 require current persisted READY and exact recorder evidence |
| SD-009 | SD-S023–SD-S025 and Cases 12–13 reserve equivalence for authorized owners |
| SD-010 | SD-S026–SD-S031 and Cases 14–15/18 require tracker-only CAS closure, immutable planning/story inputs, rollback, and receipt |
| SD-011 | SD-S004–SD-S006/SD-S027–SD-S031 and Cases 1/7/14–16/18 define immutable story/planning ownership and tracker-recorder-only closure |

## Validation boundary

This is a static contract specification. It proves that the staged skill text
contains testable fail-closed rules and exact state mappings. It does not execute
a test runner, readiness workflow, QA review, code review, game build, or closure
recorder. Runtime conformance requires fixtures implementing the named schemas,
fault injection for the recorder, and byte-level postcondition checks. Cross-skill
The candidate consumes only the staged producer contracts named above and
rejects every nonconforming or stale producer output at the consumer boundary.
