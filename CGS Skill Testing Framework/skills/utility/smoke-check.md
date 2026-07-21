# Skill Spec: $smoke-check

> **Category**: utility
> **Priority**: low
> **Spec written**: 2026-07-22

## Skill Summary

$smoke-check consumes an exact build-candidate manifest, an exact effectively CURRENT QA plan, and its verified test manifest. It produces build-bound automated and explicit manual evidence under production/qa/evidence/smoke/{candidate-id}/{run-id}/. Only a verified persisted sprint receipt with formal PASS and Handoff Eligible: YES can authorize QA hand-off. FAIL, INCOMPLETE, quick-mode targeted success, stale evidence, and non-persisted results are never hand-off eligible.

---

## Static Assertions

- [ ] YAML frontmatter contains only name and a non-empty description; name is smoke-check
- [ ] Supported sprint and quick argument schemas require candidate, QA-plan, and unique run IDs
- [ ] The workflow rejects unknown positional arguments and flags before executing or writing
- [ ] It consumes the QA-plan manifest, verifies its raw hash, and recomputes effective CURRENT state from captured source bytes
- [ ] Automated evidence requires candidate/build/source/platform/runner/argv/exit/log/hash provenance
- [ ] Manual rows require explicit PASS, FAIL, NOT RUN, or N-A plus observer/build/platform/timestamp/evidence provenance
- [ ] Silence and unselected choices become UNKNOWN rather than PASS
- [ ] The verdict table includes automated, manual, platform, data-integrity, performance, warning, parser, and coverage states
- [ ] Quick mode can emit TARGETED CHECK PASSED but is never hand-off eligible
- [ ] The canonical receipt path includes candidate ID and run ID, and prior receipts are immutable
- [ ] The workflow follows bounded changeset authorization and transactional verification
- [ ] The final phase recommends a next action without invoking another workflow

---

## Director Gate Checks

- **Full mode**: N/A; smoke-check never invokes a director gate.
- **Lean mode**: N/A; smoke-check never invokes a director gate.
- **Solo mode**: N/A; smoke-check never invokes a director gate.
- **Consumer gate**: QA hand-off is allowed only from an exact, current, persisted sprint PASS receipt; this is not a director verdict.

---

## Test Cases

### Case 1: Happy path — current full sprint PASS

**Fixture**:
- A candidate manifest binds build CAND-42, build artifact hash, source commit, platform matrix, QA-plan path/hash, and test-manifest path/hash.
- The QA plan says CURRENT; all captured source bytes still match; stable smoke IDs map one-to-one to AC IDs.
- The allowed runner produces a complete PASS receipt and untruncated log.
- Every required manual/platform row is explicitly PASS or valid N-A with observer, build, device, time, and evidence hashes.
- The run ID is unused and the bounded request authorizes persistence.

**Expected behavior**:
1. The skill verifies candidate, build, QA-plan, source, test-manifest, scope, and evidence hashes.
2. It applies verdict-table row 4.
3. It atomically writes and re-reads the exact run directory.
4. It returns PASS, Persistence: WRITTEN, and Handoff Eligible: YES.

**Assertions**:
- [ ] Report header names exact candidate/build/commit/plan/test-manifest/scope identities and hashes
- [ ] Automated and manual rows use stable QA-plan IDs
- [ ] Receipt path is production/qa/evidence/smoke/CAND-42/{run-id}/report.md
- [ ] Only after read-back verification may the response say QA hand-off is allowed

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 2: Automated tests were not run

**Fixture**:
- Candidate and QA plan are current.
- The runner is unavailable and no verifiable exact-build CI receipt is supplied.
- Manual checks otherwise pass.

**Expected behavior**:
1. Automated status is NOT_RUN.
2. Verdict-table row 2 produces INCOMPLETE.
3. Handoff Eligible is NO and the output says BLOCKED FOR HANDOFF.

**Assertions**:
- [ ] NOT_RUN is never PASS or a warning-only hand-off
- [ ] Manual confirmation cannot replace structured automated evidence
- [ ] No ready-for-QA statement appears

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 3: Empty manual response is UNKNOWN

**Fixture**:
- Automated evidence passes.
- The manual input UI returns no selected failures, no explicit rows, or an unanswered item.

**Expected behavior**:
1. Every unanswered row becomes UNKNOWN.
2. The report identifies missing observer/build/platform/time/evidence fields.
3. Verdict is INCOMPLETE and hand-off is blocked.

**Assertions**:
- [ ] Silence is not expanded into PASS rows
- [ ] Every required row has one explicit allowed status
- [ ] UNKNOWN remains visible in the receipt

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 4: Quick targeted success cannot satisfy formal hand-off

**Fixture**:
- Invocation is quick with two valid stable IDs.
- All evidence for those IDs is current and passes.

**Expected behavior**:
1. The scope contains exactly the two selected stable IDs.
2. Verdict-table row 3 returns TARGETED CHECK PASSED.
3. Handoff Eligible is NO because full sprint scope was not evaluated.

**Assertions**:
- [ ] The result never says PASS or ready for QA/release
- [ ] Coverage outside the targeted IDs is not implied
- [ ] A missing or unknown selected row changes the result to INCOMPLETE

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 5: Director gate — none

**Fixture**:
- Any valid sprint or quick invocation.

**Expected behavior**:
1. No director agent or gate is invoked.
2. The smoke evidence verdict is calculated locally from the deterministic table.

**Assertions**:
- [ ] No CD-, TD-, AD-, or PR-gate controls the result
- [ ] No director skip message is required
- [ ] QA hand-off eligibility is not represented as a director approval

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 6: Old build or stale QA plan is rejected

**Fixture**:
- A historical XML/log says PASS for another build, or the supplied QA-plan bytes/source bytes no longer match their captured hashes.

**Expected behavior**:
1. The workflow refuses most-recent-file selection.
2. The old build receipt is INVALID_RECEIPT or the QA plan is effectively STALE.
3. No tests execute against a stale plan; verdict is INCOMPLETE.

**Assertions**:
- [ ] Candidate ID, build hash, source commit, platform, plan hash, and scope hash must all match
- [ ] PARTIAL or STALE plans cannot supply smoke IDs
- [ ] Handoff Eligible is NO

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 7: Any platform or Batch-3-equivalent failure fails overall

**Fixture**:
- Automated tests pass.
- One platform row reports FAIL, or a data-integrity/performance row reports save corruption, data loss, or a critical performance failure.
- Other rows pass.

**Expected behavior**:
1. The failure is retained with its stable ID and provenance.
2. Verdict-table row 1 returns FAIL regardless of batch or platform.
3. Handoff is blocked.

**Assertions**:
- [ ] Platform failures are not averaged away
- [ ] Data-integrity and performance failures participate in the single verdict function
- [ ] Failures plus incomplete rows still yield FAIL while listing both

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 8: Runner crash, timeout, parse error, or truncated log

**Fixture**:
- Candidate and QA plan are current.
- The runner crashes, exceeds its deadline, returns an unparseable result, or hits the output cap.

**Expected behavior**:
1. Process cleanup follows the test manifest.
2. Status is TIMEOUT, INFRA_ERROR, or INVALID_RECEIPT.
3. Verdict is INCOMPLETE and hand-off is blocked.

**Assertions**:
- [ ] Infrastructure errors cannot become test PASS
- [ ] Log truncation is explicit
- [ ] Exit code, parser state, and log hash are preserved when available

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 9: Warning truth table is exhaustive

**Fixture**:
- Matrix A has all required evidence passing and no warning.
- Matrix B has all required evidence passing but one unresolved warning or coverage gap.
- Matrix C has one valid test failure plus one incomplete row.

**Expected behavior**:
1. Matrix A in sprint mode returns PASS.
2. Matrix B returns INCOMPLETE; there is no hand-off-capable PASS WITH WARNINGS.
3. Matrix C returns FAIL by precedence and also lists the incomplete row.

**Assertions**:
- [ ] Each matrix selects exactly one verdict-table row
- [ ] Warning count zero and nonzero are both defined
- [ ] FAIL precedence is deterministic

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 10: Exact-build external CI receipt may substitute locally

**Fixture**:
- Local execution is unavailable.
- A CI receipt and log are verifiable and bind the exact candidate/build/commit/platform/test-manifest/QA-plan/scope IDs and hashes.

**Expected behavior**:
1. The workflow re-hashes available receipt/log artifacts and validates issuer/job/timestamps/argv/results.
2. A complete exact-build CI PASS can supply the automated PASS row.
3. A missing remote artifact, mismatched field, untrusted issuer, or truncated log becomes INVALID_RECEIPT.

**Assertions**:
- [ ] A generic user statement that CI passed is insufficient
- [ ] A historical CI success for another candidate is stale
- [ ] Local and CI evidence use the same receipt schema

**Case Verdict**: PASS / FAIL / PARTIAL

---

## Protocol Compliance

- [ ] Treats an explicit bounded request as authorization for all in-scope execution and writes
- [ ] If no bounded authorization exists, previews one complete changeset and asks once before the first write
- [ ] Does not re-prompt within an authorized changeset
- [ ] Returns observed verdict even if persistence is declined, while marking the receipt non-consumable
- [ ] Executes only verified argv allowlists with timeout, output cap, redaction, and process-tree cleanup
- [ ] Does not auto-fix code/tests or modify the candidate manifest, QA plan, session state, or source artifacts
- [ ] Does not invoke director gates or downstream workflows
- [ ] Downstream hand-off requires an exact receipt path and candidate-manifest identity, never newest-file discovery

---

## Coverage Notes

This is a behavioral specification, not an executed test result. Runtime fixtures must cover argv execution, process-tree timeout cleanup, output truncation, symlink escape, build/plan/test-manifest hash mutation, explicit manual-row collection, multi-platform aggregation, quick scope, CI receipt validation, transactional persistence, and downstream stale-receipt rejection. team-qa, day-one-patch, the workflow catalog, and the workflow guide must independently migrate to the exact receipt/candidate consumer contract.
