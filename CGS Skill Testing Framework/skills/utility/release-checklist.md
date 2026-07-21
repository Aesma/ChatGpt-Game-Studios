# Skill Spec: $release-checklist

> **Category**: utility
> **Priority**: low
> **Spec written**: 2026-07-22

## Skill Summary

$release-checklist is a release-candidate evidence collector, not the release gate owner. It consumes one exact release manifest and policy, validates only indexed candidate-bound artifacts, and emits an immutable table whose stable items are PASS, FAIL, UNKNOWN, or authorized N/A. It always reports Gate Decision: NOT EVALUATED; a separate gate owner applies the named policy.

---

## Static Assertions

- [ ] YAML frontmatter contains only name and a non-empty description; name is release-checklist
- [ ] The only accepted input is an exact release-candidate manifest
- [ ] Release, candidate, build, artifact, source, platform, policy, and evidence hashes are mandatory
- [ ] Every policy item has exactly one PASS, FAIL, UNKNOWN, or N/A status
- [ ] PASS requires current authoritative positive evidence; existence and empty checks are insufficient
- [ ] Legal/cert/store/sign-off and N/A states require verified authority receipts
- [ ] Smoke, regression, soak, playtest, and test-evidence-review use exact staged canonical consumer contracts
- [ ] The skill never emits a release-readiness verdict or invokes the gate owner
- [ ] Optional predecessor comparison uses an exact path/hash and stable item IDs
- [ ] Reports use immutable release-manifest-hash paths and transactional read-back verification
- [ ] The final phase recommends accountable owners without invoking another workflow

---

## Director Gate Checks

- **Full mode**: N/A; no director gate is invoked.
- **Lean mode**: N/A; no director gate is invoked.
- **Solo mode**: N/A; no director gate is invoked.
- **Release authority**: Gate Decision remains NOT EVALUATED in every mode; the downstream gate owner is separate.

---

## Test Cases

### Case 1: Happy path — all indexed evidence normalizes to PASS

**Fixture**:
- Release manifest, build-candidate manifest, build artifact, policy, and AGENTS chain have matching hashes.
- Every required policy item has exact current authoritative positive evidence for the same candidate/build/platform.
- The report target is absent and the bounded request authorizes writing.

**Expected behavior**:
1. Every stable item is emitted once with PASS(evidence).
2. Summary counts are deterministic and Workflow Status is COMPLETE.
3. The report is written atomically and re-read.
4. Gate Decision remains NOT EVALUATED.

**Assertions**:
- [ ] No RELEASE READY/GO verdict is emitted
- [ ] Every PASS row includes evidence path/hash and candidate binding
- [ ] Persistence and report SHA-256 are reported independently from item status

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 2: Missing candidate identity blocks before evidence evaluation

**Fixture**:
- Release manifest lacks candidate-manifest hash, build ID/artifact hash, source commit, or platform matrix.

**Expected behavior**:
1. Identity validation enumerates missing fields.
2. Workflow Status is BLOCKED and Persistence is NOT_ATTEMPTED.
3. No report or gate decision is produced.

**Assertions**:
- [ ] Old milestone/QA/CI artifacts are not used as fallback
- [ ] No readiness vocabulary appears
- [ ] Zero files are written

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 3: Old-build PASS evidence becomes UNKNOWN

**Fixture**:
- A smoke, regression, CI, or QA receipt says PASS but names a prior candidate/build/commit or has a mismatched source/log hash.

**Expected behavior**:
1. Evidence State is STALE.
2. Item Status is UNKNOWN with the accountable owner.
3. It cannot increase the PASS count.

**Assertions**:
- [ ] Modification time or newest-file ordering cannot rescue it
- [ ] The exact identity/hash mismatch is reported
- [ ] The workflow does not silently convert stale evidence into FAIL or PASS

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 4: Missing legal or certification authority remains UNKNOWN

**Fixture**:
- A legal/cert/store checklist box or role name is nonempty.
- No signed/verifiable authority receipt binds the release/candidate/platform/artifact scope.

**Expected behavior**:
1. The evidence is INVALID or MISSING.
2. Item Status is UNKNOWN.
3. The model neither signs nor grants N/A.

**Assertions**:
- [ ] A human-looking name is not approval
- [ ] N/A requires explicit rationale, authority, policy hash, scope, and expiry
- [ ] Gate Decision remains NOT EVALUATED

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 5: Director gate — none and release verdict has one external owner

**Fixture**:
- Any valid checklist invocation under any external review mode.

**Expected behavior**:
1. No director or gate workflow is invoked.
2. The checklist normalizes evidence only.
3. Gate Decision is NOT EVALUATED.

**Assertions**:
- [ ] No CD-, TD-, AD-, PR-, or release gate verdict appears
- [ ] Workflow Status is not presented as readiness
- [ ] The spec and implementation use the same collector contract

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 6: Current negative evidence creates FAIL items, not workflow failure

**Fixture**:
- Exact current evidence shows a required smoke failure, regression test failure, open policy-blocking S1 bug, or soak Readiness Result: FAIL.
- All inputs are readable.

**Expected behavior**:
1. Each matching item is FAIL(evidence).
2. Workflow Status is COMPLETE after every policy item is evaluated.
3. Summary exposes failures but issues no release verdict.

**Assertions**:
- [ ] FAIL item provenance names exact candidate-bound evidence
- [ ] A valid failure is not downgraded to UNKNOWN
- [ ] COMPLETE describes collection only

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 7: Unreadable required artifact yields PARTIAL

**Fixture**:
- Release identity and policy are valid.
- One indexed required evidence artifact exists but cannot be read, parsed, decoded, or verified.

**Expected behavior**:
1. Evidence State is UNAVAILABLE and Item Status is UNKNOWN.
2. Workflow Status is PARTIAL.
3. The affected row remains present with its owner.

**Assertions**:
- [ ] UNAVAILABLE is not hidden as PASS or product FAIL
- [ ] The report cannot have a complete-looking blank checkbox
- [ ] Gate Decision remains NOT EVALUATED

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 8: Stable predecessor delta is reproducible

**Fixture**:
- Manifest names an exact previous report path/hash with the same policy item namespace.
- Current evidence changes two item statuses and leaves others unchanged.

**Expected behavior**:
1. Comparison uses exact stable Item IDs.
2. Delta labels are RESOLVED, REGRESSED, CHANGED, UNCHANGED, ADDED, or REMOVED.
3. Prior evidence does not affect current statuses.
4. Re-running identical bytes produces identical ordered rows/counts/delta.

**Assertions**:
- [ ] No newest previous report discovery occurs
- [ ] Candidate/report hashes are shown
- [ ] Mismatched prior policy/report becomes comparison unavailable

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 9: Canonical technical evidence matrix is enforced

**Fixture**:
- Current smoke sprint PASS, regression selection plus matching execution/sensitivity receipts, soak completed PASS, completed canonical playtests, and persisted full-scope evidence review are indexed.
- Alternate fixtures use quick smoke, regression selection alone, soak COMPLETE but inconclusive, playtest protocol, or conversation-only evidence review.

**Expected behavior**:
1. Only exact current canonical positive artifacts may yield PASS.
2. Finalization words alone do not imply technical/readiness PASS.
3. Alternate fixtures yield UNKNOWN unless they contain current conclusive failure evidence.

**Assertions**:
- [ ] Every referenced raw/log/source/manifest hash is revalidated
- [ ] Regression selection without execution cannot pass
- [ ] Soak Verdict: COMPLETE is not treated as Readiness Result: PASS
- [ ] Playtest template/review does not count as session result
- [ ] Test-evidence review requires ADEQUATE/PASS/FULL/Closure Eligible YES and persisted report

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 10: Authorized N/A is distinct from silence

**Fixture**:
- One item is irrelevant to a target platform.
- A verified policy authority receipt binds item/release/candidate/platform, rationale, policy hash, timestamp, and expiry.
- Another item merely has an empty or unchecked field.

**Expected behavior**:
1. The first item is N/A with authority provenance.
2. The second item is UNKNOWN with owner.
3. Neither is PASS.

**Assertions**:
- [ ] Blank or unselected values never become N/A
- [ ] Expired/out-of-scope authority makes N/A invalid
- [ ] Counts distinguish PASS, UNKNOWN, and N/A

**Case Verdict**: PASS / FAIL / PARTIAL

---

## Protocol Compliance

- [ ] Explicit bounded requests authorize the one report write
- [ ] Otherwise one complete CREATE changeset is previewed and approved once
- [ ] Only manifest-indexed evidence is read; no arbitrary scans or newest-file selection
- [ ] All inputs are re-hashed immediately before write
- [ ] Report path includes release ID and full release-manifest digest
- [ ] Existing report targets are never overwritten
- [ ] Non-owned release/evidence artifacts remain byte-identical
- [ ] No downstream workflow, director, sign-off, bug closure, or evidence creation is performed

---

## Coverage Notes

This is a behavioral specification, not an executed test result. Runtime fixtures should cover manifest/path/symlink validation, candidate/build/source/platform mismatches, policy parsing, authoritative N/A/legal receipts, exact dependency consumers, evidence recursion, bug severity/waivers, unavailable inputs, previous-report delta, deterministic ordering, concurrent changes, write decline/failure, and proof that no readiness verdict or non-owned write occurs.
