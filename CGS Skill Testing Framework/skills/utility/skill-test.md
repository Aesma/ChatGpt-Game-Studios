# Skill Test Spec: `$skill-test`

> **Spec ID**: skill-test-v2
> **Spec Schema**: cgs-skill-spec/v2
> **Category**: utility
> **Priority**: critical
> **Spec written**: 2026-07-22

## Skill Summary

`$skill-test` supports `static`, `spec`, `category`, and `audit` modes plus the
read-only `--check-receipt [path]` flag. All modes
are read-only unless `--persist-receipt` is explicitly supplied and one immutable
receipt write is approved.

**Owned output:** only
`CGS Skill Testing Framework/results/skill-test/receipt-[receipt-id].yaml`.

**Non-writes:** target skills/specs/rubrics, test fixtures, and
`CGS Skill Testing Framework/catalog.yaml` including every legacy `last_*` field.

**Operation vocabulary:** `ANALYZED`, `RECEIPT_WRITTEN`,
`RECEIPT_UNCHANGED`, `RECEIPT_DECLINED`, `FAILED`.

**Validation vocabulary:** `COMPLIANT`, `WARNINGS`, `NON-COMPLIANT`,
`PARTIAL_VALIDATION`, `TEST_INFRA_INVALID`.

**Receipt freshness:** `CURRENT`, `STALE`, `INVALID`, `UNVERIFIED`.

The workflow never executes the target skill.

---

## Static Assertions

- [ ] **[ST-SA-001]** YAML frontmatter contains exactly non-empty `name` and
  `description`.
- [ ] **[ST-SA-002]** The invocation is `$skill-test`.
- [ ] **[ST-SA-003]** A normative `cgs-skill-contract/v1` manifest exists.
- [ ] **[ST-SA-004]** Structural and semantic validation are separate phases.
- [ ] **[ST-SA-005]** Behavioral specs are preflighted against
  `cgs-skill-spec/v2` before target grading.
- [ ] **[ST-SA-006]** Immutable receipts contain target/authority/validator/
  fixture hashes.
- [ ] **[ST-SA-007]** Catalog and legacy `last_*` fields are explicit
  non-writes.
- [ ] **[ST-SA-008]** Invalid or partial infrastructure cannot aggregate to
  `COMPLIANT`.

---

## Test Cases

### Case 1 [ST-C01]: Missing spec structure invalidates test infrastructure

#### Fixture

- Catalog entry `broken-one` points to `broken-one.md`.
- The spec has prose and assertions but no Case headings, Fixture, stable
  assertion IDs, or Case Verdict.
- The target skill itself is otherwise structurally valid.

#### Input

`$skill-test spec broken-one`

#### Expected reads

- Target `SKILL.md` and metadata.
- Catalog entry and the complete registered broken spec.
- Validator rule set.

#### Expected writes

- None.

#### Expected non-writes

- Target package, broken spec, catalog, and result directory remain unchanged.

#### Expected behavior

1. Spec schema preflight reports every missing required element with rule IDs.
2. Target behavioral assertions are not evaluated.
3. Operation is `ANALYZED`.
4. Validation is `TEST_INFRA_INVALID`, never `COMPLIANT`.

#### Assertions

- [ ] **[ST-C01-A01]** Surviving loose assertions are not graded selectively.
- [ ] **[ST-C01-A02]** The result names `INVALID SPEC`.
- [ ] **[ST-C01-A03]** No target quality verdict is synthesized.

#### Case Verdict

`PASS` when all assertions hold; otherwise `FAIL`. `PARTIAL` is allowed only
when fixture bytes cannot be read; malformed fixture content is expected
`INVALID` infrastructure, not a partial target pass.

---

### Case 2 [ST-C02]: Self-contradictory spec cannot be authority

#### Fixture

- A schema-complete spec summary says the workflow is read-only.
- One Case expects no writes.
- Another Case for the same mode expects a file to be created and returns the
  same success verdict.
- Every heading and stable ID is otherwise valid.

#### Input

`$skill-test spec contradictory-skill`

#### Expected reads

- Target, catalog entry, complete spec, and validator rules.

#### Expected writes

- None.

#### Expected non-writes

- Target, spec, catalog, and fixtures remain byte-for-byte unchanged.

#### Expected behavior

1. Semantic lint constructs mode/write/verdict models.
2. It cites the conflicting summary and Cases.
3. The spec is `INVALID SPEC`.
4. Validation is `TEST_INFRA_INVALID`.

#### Assertions

- [ ] **[ST-C02-A01]** Schema completeness alone does not pass semantic lint.
- [ ] **[ST-C02-A02]** Contradictions receive stable lint rule IDs and lines.
- [ ] **[ST-C02-A03]** Target `COMPLIANT` is prohibited.

#### Case Verdict

`PASS` when the contradiction invalidates infrastructure; otherwise `FAIL`.

---

### Case 3 [ST-C03]: Target or authority byte change makes receipt stale

#### Fixture

- A valid persisted receipt records raw-byte hashes for target `SKILL.md`,
  metadata, catalog entry, spec, rubric, validator rules, and fixture snapshot.
- Each dependency initially matches.
- Test variants change exactly one byte in each dependency in turn.

#### Input

`$skill-test static demo-skill --check-receipt [receipt-path]`

#### Expected reads

- Receipt and every recorded dependency.

#### Expected writes

- None.

#### Expected non-writes

- Receipt, changed dependency, catalog, and all other files remain unchanged.

#### Expected behavior

1. Each dependency is rehashed from current raw bytes.
2. Every one-byte variant returns freshness `STALE`.
3. The stored validation verdict remains historical and is not displayed as
   current `COMPLIANT`.

#### Assertions

- [ ] **[ST-C03-A01]** SKILL hash change is stale.
- [ ] **[ST-C03-A02]** Metadata hash change is stale.
- [ ] **[ST-C03-A03]** Spec or rubric hash change is stale.
- [ ] **[ST-C03-A04]** Validator/ruleset or fixture change is stale.
- [ ] **[ST-C03-A05]** Timestamps cannot override hash staleness.

#### Case Verdict

`PASS` when every dependency mutation yields `STALE`; otherwise `FAIL`.

---

### Case 4 [ST-C04]: Receipt captures complete provenance

#### Fixture

- `demo-skill` has valid target files, catalog entry, `VALID SPEC`, rubric,
  contract manifest, and fixtures.
- A pinned external validator is used successfully with known version, hash,
  argv, exit code, and output-log hashes.
- `--persist-receipt` is supplied.
- The user approves the exact one-file receipt changeset.

#### Input

`$skill-test spec demo-skill --persist-receipt`

#### Expected reads

- Every target, authority, validator, and fixture input listed in the receipt.

#### Expected writes

- One new immutable
  `CGS Skill Testing Framework/results/skill-test/receipt-[receipt-id].yaml`.

#### Expected non-writes

- Target package, spec, rubric, catalog, and all `last_*` fields remain
  byte-for-byte unchanged.

#### Expected behavior

1. Receipt records every required path/hash and validator execution fact.
2. It records every stable assertion result and aggregation trace.
3. Dependencies are rehashed immediately before the write.
4. Read-back verifies receipt bytes and SHA-256.
5. Operation is `RECEIPT_WRITTEN`.

#### Assertions

- [ ] **[ST-C04-A01]** No required provenance field is missing.
- [ ] **[ST-C04-A02]** Receipt is immutable and versioned.
- [ ] **[ST-C04-A03]** Catalog `last_*` values are not populated or repurposed.
- [ ] **[ST-C04-A04]** Written status requires read-back verification.

#### Case Verdict

`PASS` when exactly one verified receipt is written; `FAIL` on any unlisted
write; `PARTIAL` only for a documented pre-write dependency read failure.

---

### Case 5 [ST-C05]: Boilerplate cannot hide a later silent write

#### Fixture

- Target Contract Manifest declares `writes: []` and says read-only near the top.
- A later phase instructs the workflow to silently append to
  `production/session-state/active.md`.
- Frontmatter, metadata, headings, and invocation tokens are mechanically valid.

#### Input

`$skill-test static hidden-write`

#### Expected reads

- Target package and validator authorities.

#### Expected writes

- None.

#### Expected non-writes

- Target, session state, catalog, and receipts remain unchanged.

#### Expected behavior

1. Structural checks may pass.
2. `SEM-002 WRITE_SET` and `SEM-010 INTERNAL_CONTRADICTION` fail.
3. Validation is `NON-COMPLIANT`.

#### Assertions

- [ ] **[ST-C05-A01]** “Read-only” keyword presence is not a semantic pass.
- [ ] **[ST-C05-A02]** The later write path and contradicting manifest field are
  both cited.
- [ ] **[ST-C05-A03]** Static boilerplate cannot cancel semantic failure.

#### Case Verdict

`PASS` when the hidden write produces `NON-COMPLIANT`; otherwise `FAIL`.

---

### Case 6 [ST-C06]: False-success branch fails state-machine validation

#### Fixture

- A target exposes optional `write-plan` and `backfill-only` operations.
- Its manifest allows only selected, verified operations to return `written`.
- The prose says a backfill-only selection reports “plan written” and registers
  an output path that was never created.

#### Input

`$skill-test static false-success`

#### Expected reads

- Target package and validator authorities.

#### Expected writes

- None.

#### Expected non-writes

- Target outputs, catalog, and receipts remain unchanged.

#### Expected behavior

1. `SEM-004 RESULT_TRUTH`, `SEM-005 STATE_MACHINE`, and
   `SEM-006 VERDICT_TRUTH_TABLE` fail.
2. The unselected/nonexistent artifact is named.
3. Validation is `NON-COMPLIANT`.

#### Assertions

- [ ] **[ST-C06-A01]** Success wording is tied to actual operation state.
- [ ] **[ST-C06-A02]** A nonexistent output cannot be checkpointed or reported.
- [ ] **[ST-C06-A03]** A top-level changeset policy does not mask the false
  result.

#### Case Verdict

`PASS` when all semantic rules fail as expected; otherwise `FAIL`.

---

### Case 7 [ST-C07]: Missing or failed validator yields partial validation

#### Fixture

- Built-in structural/semantic inputs are readable.
- The pinned external validator manifest is missing, its hash mismatches, it
  times out, or its output is invalid.
- All checks that can safely continue pass.

#### Input

`$skill-test static demo-skill`

#### Expected reads

- Target and all available validator authorities.

#### Expected writes

- None.

#### Expected non-writes

- Target, catalog, fixtures, and result directory remain unchanged.

#### Expected behavior

1. The external-validator failure and coverage reduction are explicit.
2. Safe built-in checks still run.
3. Validation is `PARTIAL_VALIDATION`, never `COMPLIANT`.

#### Assertions

- [ ] **[ST-C07-A01]** Missing validation coverage is not silently skipped.
- [ ] **[ST-C07-A02]** Validator argv/version/hash/timeout evidence is reported
  when available.
- [ ] **[ST-C07-A03]** Aggregation follows the fixed truth table.

#### Case Verdict

`PASS` when incomplete coverage yields `PARTIAL_VALIDATION`; otherwise `FAIL`.

---

### Case 8 [ST-C08]: Audit derives recursive sets and rejects duplicates

#### Fixture

- One valid nested skill exists below `.agents/skills/group/nested/SKILL.md`.
- One valid nested agent TOML exists.
- A generator helper is present under an explicitly excluded generator path.
- Two catalog names normalize to the same Unicode NFC/case-folded name.
- Aggregate totals happen to match historical prose counts.

#### Input

`$skill-test audit`

#### Expected reads

- Recursive skill, metadata, agent, catalog, and registered-spec sets.

#### Expected writes

- None.

#### Expected non-writes

- Implementations, specs, catalog, and result directories remain unchanged.

#### Expected behavior

1. Nested skill and agent are included.
2. Generator exclusion is reported with its rule ID and path.
3. Duplicate normalized names fail before set comparison.
4. Historical totals do not produce a pass.
5. Validation is `NON-COMPLIANT` or `PARTIAL_VALIDATION` if required reads fail.

#### Assertions

- [ ] **[ST-C08-A01]** Discovery is recursive and uses one implementation.
- [ ] **[ST-C08-A02]** Selected/loaded/failed/omitted/excluded sets are reported.
- [ ] **[ST-C08-A03]** Duplicate names fail even when totals match.
- [ ] **[ST-C08-A04]** No hard-coded 74/49 requirement determines the result.

#### Case Verdict

`PASS` when recursive set comparison exposes the duplicate; otherwise `FAIL`.
`PARTIAL` applies only when a required fixture path cannot be read.

---

## Protocol Compliance

- [ ] **[ST-PC-001]** Validation is read-only unless receipt persistence is
  explicitly requested.
- [ ] **[ST-PC-002]** Invalid specs stop behavioral grading.
- [ ] **[ST-PC-003]** Structural and semantic results remain separate.
- [ ] **[ST-PC-004]** The fixed aggregation table prevents invalid/partial
  `COMPLIANT`.
- [ ] **[ST-PC-005]** Persisted receipts bind every required dependency.
- [ ] **[ST-PC-006]** Legacy catalog `last_*` fields are never written.
- [ ] **[ST-PC-007]** No target skill is executed or modified.
- [ ] **[ST-PC-008]** Every finding includes stable ID and direct evidence.

---

## Coverage Notes

This spec validates the written-contract analyzer and receipt protocol. It does
not run `$skill-test`, execute target skills, mutate catalog results, or prove a
future external validator implementation. Catalog receipt-reference schema,
hook migration, and flow-diagram updates remain separately owned work.
