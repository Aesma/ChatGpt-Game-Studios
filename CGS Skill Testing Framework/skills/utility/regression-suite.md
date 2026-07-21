# Skill Test Spec: $regression-suite

## Skill Summary

`$regression-suite` owns only `tests/regression-suite.md`, an ID-keyed selection
manifest. It does not author or execute tests and cannot declare release success
from selection alone.

Verified requirement coverage requires all of:

- an exact stable AC or BUG ID mapped to an exact stable test ID;
- current raw-byte hashes for the QA plan, requirement source, and test source;
- valid failure-sensitivity evidence bound to those IDs and hashes;
- a passing result in a runner receipt bound to the exact current selection
  manifest hash and target build.

`update` and `audit` use per-ID upserts. They never reconstruct the full
manifest. Retirement is an explicitly approved tombstone that preserves
rationale, owner, and history.

---

## Static Assertions

- [ ] YAML frontmatter contains only `name` and non-empty `description`; the name
  matches the skill directory.
- [ ] The only owned output is `tests/regression-suite.md`.
- [ ] The skill states that file names, paths, comments, and keyword matches are
  discovery hints, not coverage.
- [ ] Stable AC, BUG, test, and selection IDs plus raw-byte SHA-256 provenance
  are required.
- [ ] Failure-sensitivity evidence and a current build-bound runner receipt are
  both required for verified coverage.
- [ ] Selection-manifest ownership is separated from runner receipt ownership.
- [ ] `audit` explicitly forbids full-manifest reconstruction.
- [ ] Deletion requires an approved tombstone with retained history.
- [ ] Operation and coverage statuses are independent.
- [ ] `report` is byte-preserving and cannot report “updated.”

---

## Case 1: Same-name empty test file is not coverage

### Fixture

- A current QA plan maps `AC-S001-01` to `TC-combat-S001-AC01`.
- `tests/unit/combat/damage_test.gd` exists, has a matching-looking file name,
  but contains no stable test ID, no assertions, and no sensitivity evidence.
- Record raw bytes/hashes for every fixture file and the existing selection
  manifest.

### Input

`$regression-suite audit scope: production/qa/qa-plan-combat-2026-07-22.md`

The user declines any write so the evidence evaluation can be inspected alone.

### Expected writes

- None.

### Expected non-writes

- Test source, QA plan, selection manifest, receipts, and all other files remain
  byte-for-byte unchanged.

### Expected behavior and verdict

1. The file appears only as a discovery candidate.
2. `AC-S001-01` is a `GAP`; the candidate is `UNMAPPED` or
   `SELECTED_UNVERIFIED`.
3. No `COVERED`, `ELIGIBLE`, or `VERIFIED COVERAGE` claim is made.
4. Operation is `DECLINED`; coverage is `GAPS FOUND`.

### Assertions

- [ ] File existence and matching names never establish coverage.
- [ ] No stable ID or evidence is inferred from the path.
- [ ] No file changes occur.

---

## Case 2: BUG ID in a comment does not prove failure sensitivity

### Fixture

- `BUG-042` is an in-scope stable bug artifact with a recorded raw-byte hash.
- A test source contains the comment “regression for BUG-042” and always passes.
- No receipt proves baseline-pass plus injected-failure fail behavior.
- A current runner receipt may show the always-passing test passed.

### Input

`$regression-suite report scope: production/qa/qa-plan-combat-2026-07-22.md`

### Expected writes

- None.

### Expected non-writes

- Entire fixture tree remains byte-for-byte unchanged.

### Expected behavior and verdict

1. The comment is discovery evidence only.
2. The test is `SELECTED_UNVERIFIED` because sensitivity evidence is absent.
3. `BUG-042` remains a gap even if the ordinary run receipt says PASS.
4. Operation is `REPORTED`; coverage is `GAPS FOUND`.

### Assertions

- [ ] A BUG ID string match is not treated as a verified mapping.
- [ ] A normal pass is not substituted for failure-sensitivity evidence.
- [ ] Report mode never says the manifest was updated.

---

## Case 3: Exact mapping plus sensitivity and current run verifies coverage

### Fixture

- A QA plan with raw-byte hash `sha256:[plan-hash]` is generation-state
  `CURRENT` and remains effectively current after every captured source is
  rehashed.
- It maps `AC-S001-01` to `TC-combat-S001-AC01`.
- The test source declares that exact stable test/AC mapping and has current
  raw-byte hash `sha256:[test-hash]`.
- A valid sensitivity receipt binds the same IDs, requirement hash, and test
  hash; baseline passes and injected failure fails.
- `tests/regression-suite.md` contains active
  `RS-TC-combat-S001-AC01` and has hash `sha256:[manifest-hash]`.
- A runner receipt binds the exact manifest hash, target build, test-source hash,
  stable test ID, and PASS result.

### Input

`$regression-suite report scope: production/qa/qa-plan-combat-2026-07-22.md`

### Expected writes

- None.

### Expected non-writes

- Entire fixture tree remains byte-for-byte unchanged.

### Expected behavior and verdict

1. QA-plan provenance revalidates `CURRENT`.
2. The selection entry is `ELIGIBLE`.
3. The current receipt is accepted only because manifest, build, and source
   hashes match.
4. `AC-S001-01` is `VERIFIED`.
5. Operation is `REPORTED`; coverage is `VERIFIED COVERAGE`.

### Assertions

- [ ] Stable AC/test IDs match the qa-plan contract exactly.
- [ ] All raw-byte hashes are checked.
- [ ] Selection and execution remain separate artifacts.
- [ ] No release PASS is emitted by this utility.

---

## Case 4: QA-plan or source mutation makes mapping stale

### Fixture

- Start from Case 3.
- Change one byte in a story, GDD, ADR, QA plan, requirement source, or test
  source after the captured hash was recorded.

### Input

`$regression-suite report scope: production/qa/qa-plan-combat-2026-07-22.md`

### Expected writes

- None.

### Expected non-writes

- Validation does not mutate the QA plan, selection manifest, source, or
  receipts.

### Expected behavior and verdict

1. Raw-byte revalidation detects the mismatch.
2. The affected plan/mapping/selection is `STALE`.
3. Old sensitivity and run receipts cannot make it current.
4. Operation is `REPORTED`; coverage is `STALE`.

### Assertions

- [ ] Timestamps and “latest file” heuristics are not used.
- [ ] A stale producer plan is rejected as consumer evidence.
- [ ] Stable IDs aid regeneration but never override hash staleness.

---

## Case 5: Selection manifest without matching run receipt is not release proof

### Fixture

- A current selection manifest contains only `ELIGIBLE` entries.
- No runner receipt exists for the exact current manifest hash and target build,
  or the only receipt binds a prior manifest/build.

### Input

`$regression-suite report scope: production/qa/qa-plan-combat-2026-07-22.md`

### Expected writes

- None.

### Expected non-writes

- No test result, runner receipt, release record, or manifest update is created.

### Expected behavior and verdict

1. The manifest is described as selection only.
2. The old/missing receipt is rejected.
3. Operation is `REPORTED`; coverage is `AWAITING RUN`.
4. The response does not print a release run command as evidence and does not
   declare release PASS.

### Assertions

- [ ] Selection alone cannot produce `VERIFIED COVERAGE`.
- [ ] The exact manifest hash and build identity are required.
- [ ] This skill never fabricates or writes a run receipt.

---

## Case 6: Audit performs keyed upsert without losing human content

### Fixture

- `tests/regression-suite.md` contains:
  - managed entry `RS-TC-combat-S001-AC01`;
  - human Owner, Rationale, comments, and three History items;
  - an unknown custom field;
  - unrelated legacy prose before and after the managed block.
- Current evidence changes only the test-source hash and selection-evidence
  state.
- Record exact pre-run bytes and manifest hash.

### Input

`$regression-suite audit scope: production/qa/qa-plan-combat-2026-07-22.md`

The user approves the displayed per-ID changeset.

### Expected writes

- Modify only `tests/regression-suite.md`.
- Patch only the approved machine-owned fields for the keyed entry and append
  one History item.

### Expected non-writes

- Owner, Rationale, prior History, custom field, comments, and unrelated legacy
  bytes remain unchanged.
- Test source, receipts, QA plan, and all other files remain unchanged.

### Expected behavior and verdict

1. The preview names the exact selection ID and field changes.
2. The pre-write manifest hash matches the previewed hash.
3. Read-back verifies approved changes and preservation invariants.
4. Operation is `AUDITED` or `UPDATED` as applicable.
5. Coverage is computed independently; it may be `AWAITING RUN` because the
   manifest hash changed.

### Assertions

- [ ] Audit never renders a replacement full manifest.
- [ ] Human and unknown content is preserved.
- [ ] The reported final hash equals the written raw bytes.
- [ ] Operation success does not imply verified coverage.

---

## Case 7: Retirement requires an approved tombstone

### Fixture

- A managed active entry is absent from the current candidate set.
- The entry contains owner, rationale, and history.
- The user approves ordinary upserts but does not approve retirement.

### Input

`$regression-suite audit scope: production/qa/qa-plan-combat-2026-07-22.md`

### Expected writes

- Approved unrelated upserts may be written.
- The absent entry itself is not changed.

### Expected non-writes

- The absent entry is not deleted, shortened, or tombstoned without approval.
- Its owner, rationale, and history remain byte-for-byte unchanged.

### Expected behavior and verdict

1. Drift is reported with a separate tombstone proposal.
2. Ledger result for that selection ID is `not-approved`.
3. If later explicitly approved, lifecycle changes to `TOMBSTONED` with reason,
   approver, timestamp, and appended history; the prior entry is retained.
4. Physical deletion never occurs.

### Assertions

- [ ] No audit full rewrite removes the entry.
- [ ] Tombstone authorization is independent and explicit.
- [ ] History and rationale survive retirement.

---

## Case 8: Concurrent manifest edit aborts the patch

### Fixture

- A complete per-ID diff was approved against manifest hash
  `sha256:[preview-hash]`.
- Before write, another actor changes the manifest bytes.

### Input

Continue the approved `update` or `audit` operation.

### Expected writes

- None by `$regression-suite` after detecting the conflict.

### Expected non-writes

- The concurrent edit and every source file remain unchanged.

### Expected behavior and verdict

1. Immediate pre-write hash comparison detects the conflict.
2. No keyed patch is applied.
3. Operation is `FAILED` with expected and observed hashes.
4. No “updated” or release-ready claim appears.

### Assertions

- [ ] Concurrent human edits are never overwritten.
- [ ] Read-back success is not claimed when no write occurred.
- [ ] Coverage status remains separate from operation failure.

---

## Protocol Compliance

- [ ] Coverage uses stable IDs, current hashes, sensitivity evidence, and a
  matching current execution result.
- [ ] QA-plan `PARTIAL` and effective `STALE` states are rejected.
- [ ] Selection manifest and build-bound receipt ownership are distinct.
- [ ] Update/audit change only keyed fields or append keyed entries.
- [ ] Removal is an approved tombstone, never deletion.
- [ ] Report mode preserves every file byte and returns `REPORTED`.
- [ ] Operation status never stands in for coverage or release status.

---

## Coverage Notes

- The CGS catalog test-result fields remain unchanged because the staging scope
  forbids shared catalog edits.
- Workflow/release guides still need a consumer migration so their gates require
  both the selection-manifest hash and a matching build-bound receipt.
- Receipt storage and signing are runner/CI-owned; this spec validates the
  consumer contract without allowing this skill to manufacture evidence.
