# Skill Spec: $test-evidence-review

> **Category**: analysis
> **Priority**: low
> **Spec written**: 2026-07-22

## Skill Summary

$test-evidence-review consumes one exact evidence-review manifest whose stable AC rows bind a CURRENT QA plan, candidate build, test sources, smoke/playtest receipts, manual artifacts, and reviewer attestations by raw-byte SHA-256. It reports Workflow Status, Evidence Quality, Execution Status/Scope, Closure Eligibility, and Persistence as separate fields. It never treats source structure, file presence, dates, or sign-off labels as proof of current execution.

---

## Static Assertions

- [ ] YAML frontmatter contains only name and a non-empty description; name is test-evidence-review
- [ ] The only accepted scope input is an exact evidence-review manifest
- [ ] Every scope row requires stable story, AC, and QA-plan test/check IDs plus expected evidence paths/hashes
- [ ] QA-plan effective CURRENT state is recomputed from every captured source byte hash
- [ ] Structural quality and current execution use separate result fields
- [ ] No assertion-token count or assertion-per-function threshold determines quality
- [ ] Manual artifact presence is distinct from content inspection and provenance validation
- [ ] Reviewer attestations bind identity, scope, build, artifact hashes, and an authorization source; the model cannot sign
- [ ] Canonical staged smoke-check and playtest-report consumer contracts are explicit
- [ ] Read failures are UNAVAILABLE/PARTIAL, not product-level MISSING
- [ ] Optional persistence owns exactly one unique review report and follows bounded authorization/read-back verification
- [ ] The workflow ends with ownership-aware remediation without invoking another workflow

---

## Director Gate Checks

- **Full mode**: N/A; no director gate is invoked.
- **Lean mode**: N/A; no director gate is invoked.
- **Solo mode**: N/A; no director gate is invoked.
- **QA review distinction**: attester identity verification is evidence validation, not a director gate and not approval fabricated by this skill.

---

## Test Cases

### Case 1: Structurally adequate test without runtime receipt

**Fixture**:
- One automated AC row has exact current QA-plan/test-source hashes.
- Requirement mapping, expected observable, and failure sensitivity are demonstrated.
- No current-build smoke receipt is declared.

**Expected behavior**:
1. Structural review reports Evidence Quality: ADEQUATE.
2. Runtime review reports Overall Execution Status: UNKNOWN and Execution Scope: NONE.
3. Closure Eligible is NO.

**Assertions**:
- [ ] ADEQUATE is never described as evidence that tests ran or passed
- [ ] No current receipt cannot become a warning-only pass
- [ ] The missing runtime receipt is listed separately from structural findings

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 2: Assertion-token forgery does not improve quality

**Fixture**:
- A test file contains assert/expect/check/verify in comments, strings, duplicated lines, and an unreviewed helper call.
- None of those operations is traced to the AC observable or shown failure-sensitive.

**Expected behavior**:
1. The workflow ignores comments, strings, repeated equivalents, and opaque helpers as proof.
2. It records Evidence Quality: INCOMPLETE for that row.
3. Assertion line count is not reported as an adequacy threshold.

**Assertions**:
- [ ] Three or more assertion-looking lines do not automatically pass
- [ ] Helper semantics must be reviewed and hash-bound
- [ ] One meaningful negative control may carry more evidence than repeated assertions

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 3: Existing screenshot without provenance is incomplete

**Fixture**:
- A screenshot path exists.
- Artifact hash/build/platform/captor/AC mapping or capture metadata is missing.

**Expected behavior**:
1. Presence is PRESENT.
2. Evidence Quality is INCOMPLETE, not ADEQUATE.
3. Execution Status is UNKNOWN and Closure Eligible is NO.

**Assertions**:
- [ ] Path existence and date alone do not prove content
- [ ] The missing receipt fields are enumerated
- [ ] The skill does not invent capture metadata

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 4: Happy path — current per-AC evidence is closure eligible

**Fixture**:
- The review manifest has unique stable AC/test IDs and matching hashes.
- QA plan is effectively CURRENT; candidate/build/test-manifest bindings match.
- Automated tests have a persisted full-scope smoke PASS receipt.
- Manual/playtest artifacts are content-inspected, hash-valid, build-bound, and have verified current attestations.
- --persist is authorized and the review ID is unused.

**Expected behavior**:
1. Every AC emits exactly one ADEQUATE/PASS/FULL row.
2. Workflow Status is COMPLETE and aggregate quality/execution are ADEQUATE/PASS.
3. The report is atomically written and re-read.
4. Overall Closure Eligible is YES.

**Assertions**:
- [ ] Exact input and report hashes are emitted
- [ ] No row is inferred from filenames or recent modification time
- [ ] Persistence is recorded independently from the evidence-based closure assessment

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 5: Director gate — none and no model-created sign-off

**Fixture**:
- Review mode elsewhere is full.
- One manual artifact requires QA-lead attestation.

**Expected behavior**:
1. No director gate or agent is invoked.
2. The skill verifies an existing attestation against its identity source.
3. If it is absent, Closure Eligible is NO; the model does not fill it in.

**Assertions**:
- [ ] No CD-, TD-, AD-, PR-, or QL-gate controls the result
- [ ] A role label alone is not an attestation
- [ ] No approval is inferred or generated

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 6: Signed evidence becomes stale after source change

**Fixture**:
- An attestation correctly names an earlier test/artifact hash.
- The current test source, story/GDD source, candidate, or artifact bytes differ.

**Expected behavior**:
1. The changed digest is reported.
2. Execution Status becomes STALE when runtime binding changed; affected quality/attestation is INCOMPLETE.
3. Closure Eligible is NO despite the nonempty signature.

**Assertions**:
- [ ] Dates do not override hash mismatch
- [ ] The old attestation is not silently carried forward
- [ ] Remediation names the artifact owner/reviewer that must refresh evidence

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 7: Read failure is unavailable, not missing

**Fixture**:
- A declared evidence path exists but cannot be read, parsed, decoded, or inspected.

**Expected behavior**:
1. Presence remains PRESENT when existence is known.
2. Row quality/execution is UNAVAILABLE as applicable.
3. Workflow Status is PARTIAL, not COMPLETE.
4. The workflow does not claim the product lacks evidence.

**Assertions**:
- [ ] UNAVAILABLE is separated from explicit MISSING
- [ ] The AC row remains in the report
- [ ] Overall Closure Eligible is NO

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 8: Canonical naming is advisory and cannot prove coverage

**Fixture**:
- Test A is named test_combat_damage_clamps_zero and maps semantically to its AC.
- Test B is named test_damage_clamps_zero without the system segment.
- Test C has a conforming name but no AC mapping or failure-sensitive observable.

**Expected behavior**:
1. Test A passes the naming check.
2. Test B receives a naming finding and is not heuristically split to invent a system.
3. Test C's name does not satisfy requirement coverage.

**Assertions**:
- [ ] Parser requires system, scenario, and expected fields
- [ ] Naming and semantic quality are separate
- [ ] No filename creates a stable AC binding

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 9: Canonical playtest evidence is verified end to end

**Fixture**:
- A QA-plan row requires a playtest.
- The exact canonical completed report binds the same build/platform/AC IDs and references raw evidence, manifest, and observation-ledger hashes.

**Expected behavior**:
1. The workflow verifies production/playtests/{session-id}/report.md and every referenced hash.
2. Derived findings resolve to Observation IDs and raw source hash.
3. A protocol, director review, ingest-only session, or legacy-path report is rejected.

**Assertions**:
- [ ] Status: COMPLETED and Gate Eligible: YES are both required
- [ ] File existence alone is insufficient
- [ ] Mismatched build or observation hash yields STALE/INCOMPLETE and blocks closure

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 10: Smoke receipt is exact, current, and scope-aware

**Fixture**:
- One exact persisted sprint smoke receipt has formal PASS, Handoff Eligible: YES, and matching candidate/QA-plan/test-manifest/scope hashes.
- A second fixture is a quick TARGETED CHECK PASSED receipt.

**Expected behavior**:
1. The sprint receipt yields PASS/FULL for covered rows after all referenced hashes revalidate.
2. The quick receipt may yield a current targeted row but Execution Scope is TARGETED.
3. Quick evidence never makes Closure Eligible YES.

**Assertions**:
- [ ] No newest-receipt discovery occurs
- [ ] INCOMPLETE, warning-bearing, stale, unpersisted, or hash-mismatched smoke evidence cannot pass
- [ ] Exact candidate-manifest identity is required

**Case Verdict**: PASS / FAIL / PARTIAL

---

## Protocol Compliance

- [ ] Explicit bounded requests authorize in-scope optional report writes
- [ ] Without bounded authorization, --persist previews one complete one-file changeset and asks once
- [ ] Without --persist the workflow remains byte-for-byte read-only
- [ ] It never edits tests/evidence or invokes directors/downstream workflows
- [ ] Missing, unavailable, stale, structural, runtime, and persistence states remain distinct
- [ ] Every declared AC appears exactly once in the output
- [ ] Persisted reports use unique review IDs and verified raw-byte hashes
- [ ] Conversation-only or failed/declined persistence is never closure evidence

---

## Coverage Notes

This is a behavioral specification, not an executed test result. Runtime fixtures should cover manifest/path validation, duplicate IDs, symlink escape, QA-plan source mutation, opaque assertion helpers, mutation/negative-control receipts, image/log decoding, attester identity verification, current/quick/stale smoke receipts, canonical playtest hashes, optional write decline/failure, and proof that all non-owned files remain byte-identical. story-done, team-qa, milestone-review, catalog, and workflow-guide consumers must independently adopt the same exact-manifest and dual-axis result contract.
