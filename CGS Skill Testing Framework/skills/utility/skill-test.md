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
  fixture revisions.
- [ ] **[ST-SA-007]** Catalog and legacy `last_*` fields are explicit
  non-writes.
- [ ] **[ST-SA-008]** Invalid or partial infrastructure cannot aggregate to
  `COMPLIANT`.
- [ ] **[ST-SA-009]** One versioned rules authority defines discovery,
  normalization, exclusions, legacy tokens, placeholder contexts, budgets, and
  aggregation.
- [ ] **[ST-SA-010]** A package-local runner is pinned by path, version, revision,
  allowed argv, timeout, interpreter constraint, and JSON output schema.
- [ ] **[ST-SA-011]** Every all/audit run reports deterministic
  selected/loaded/failed/omitted/excluded ledgers.

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

- A valid persisted receipt records declared revisions for target `SKILL.md`,
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

1. Each dependency is revalidate from current raw bytes.
2. Every one-byte variant returns freshness `STALE`.
3. The stored validation verdict remains historical and is not displayed as
   current `COMPLIANT`.

#### Assertions

- [ ] **[ST-C03-A01]** SKILL revision change is stale.
- [ ] **[ST-C03-A02]** Metadata revision change is stale.
- [ ] **[ST-C03-A03]** Spec or rubric revision change is stale.
- [ ] **[ST-C03-A04]** Validator/ruleset or fixture change is stale.
- [ ] **[ST-C03-A05]** Timestamps cannot override revision staleness.

#### Case Verdict

`PASS` when every dependency mutation yields `STALE`; otherwise `FAIL`.

---

### Case 4 [ST-C04]: Receipt captures complete provenance

#### Fixture

- `demo-skill` has valid target files, catalog entry, `VALID SPEC`, rubric,
  contract manifest, and fixtures.
- A pinned external validator is used successfully with known version, revision,
  argv, exit code, and output-log revisions.
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

1. Receipt records every required path/revision and validator execution fact.
2. It records every stable assertion result and aggregation trace.
3. Dependencies are revalidate immediately before the write.
4. Read-back verifies receipt bytes and revision.
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
- The pinned external validator manifest is missing, its version mismatches, it
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
- [ ] **[ST-C07-A02]** Validator argv/path/version/timeout evidence is reported
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
5. A conclusively detected duplicate yields `NON-COMPLIANT`; unrelated partial
   coverage remains visible but cannot replace that higher-priority target fail.
6. An invalid required authority instead yields `TEST_INFRA_INVALID`.

#### Assertions

- [ ] **[ST-C08-A01]** Discovery is recursive and uses one implementation.
- [ ] **[ST-C08-A02]** Selected/loaded/failed/omitted/excluded sets are reported.
- [ ] **[ST-C08-A03]** Duplicate names fail even when totals match.
- [ ] **[ST-C08-A04]** No hard-coded 74/49 requirement determines the result.

#### Case Verdict

`PASS` when recursive set comparison exposes the duplicate and the exact
outcome vector maps to one verdict; otherwise `FAIL`. A read failure with no
conclusive target fail is `PARTIAL`; invalid required authority is `INVALID`.

---


### Case 9 [ST-C09]: Versioned legacy rules distinguish active use from evidence

#### Fixture

- Active target prose names `.claude/`, `CLAUDE.md`, a Claude-only
  frontmatter field, and `AskUserQuestion`.
- A separate heading labelled Migration quotes the same path as removal evidence.
- Rules authority `cgs-skill-test-rules/v1` is current.

#### Input

`$skill-test static legacy-context`

#### Expected reads

- Target package, rules file, validator manifest, and pinned runner.

#### Expected writes

- None.

#### Expected non-writes

- Target, migration evidence, rules, catalog, and receipts remain unchanged.

#### Expected behavior

1. `LEG-001` through `LEG-003` fail active legacy use.
2. The labelled migration quotation passes with recorded context.
3. Every result includes token, rule ID, path, line, and heading/fence context.
4. Validation is `NON-COMPLIANT`.

#### Assertions

- [ ] **[ST-C09-A01]** Exact patterns and severity come from the versioned rules.
- [ ] **[ST-C09-A02]** Context exceptions are bounded to labelled evidence.
- [ ] **[ST-C09-A03]** Bare English read/write verbs are not tool-token matches.

#### Case Verdict

`PASS` when active use fails and labelled evidence does not; otherwise `FAIL`.

---

### Case 10 [ST-C10]: Template-aware parsing preserves declared metavariables

#### Fixture

- An Arguments section contains `$demo <target> [--flag]`.
- A labelled Output Template YAML fence contains `<generated-id>`.
- An active contract YAML fence contains `<unresolved>`.
- Active prose contains `TODO`; a labelled example contains the same token.

#### Input

`$skill-test static placeholder-context`

#### Expected reads

- Target Markdown, rules authority, validator manifest, and pinned runner.

#### Expected writes

- None.

#### Expected non-writes

- Target, examples, templates, and receipts remain unchanged.

#### Expected behavior

1. Declared invocation/path metavariables pass `PH-002`.
2. The bounded output template passes `PH-003`.
3. Active structured placeholder fails `PH-004`.
4. Active sentinel fails `PH-001`; its labelled-template instance is allowed.
5. Validation is `NON-COMPLIANT` because active failures remain.

#### Assertions

- [ ] **[ST-C10-A01]** Fence and heading state are parsed, not guessed by token.
- [ ] **[ST-C10-A02]** Legal authoring templates are not false positives.
- [ ] **[ST-C10-A03]** Active contract placeholders cannot hide in YAML/TOML/JSON.

#### Case Verdict

`PASS` when each token receives the stated context-specific result; otherwise
`FAIL`.

---

### Case 11 [ST-C11]: All-mode budgets produce a complete coverage ledger

#### Fixture

- Recursive discovery selects paths beyond the versioned file or byte budget.
- A separate variant has an unreadable subtree.
- Candidate paths are presented in a deliberately unstable filesystem order.

#### Input

`$skill-test static all`, then `$skill-test audit`

#### Expected reads

- Discovery roots, rules budgets, every admitted path, and available metadata.

#### Expected writes

- None.

#### Expected non-writes

- Implementations, catalog, rules, and receipts remain unchanged.

#### Expected behavior

1. Paths are normalized and sorted before budget admission.
2. The report includes complete selected/loaded/failed/omitted/excluded sets.
3. An unreadable subtree is a failed prefix with unknown descendants, not empty.
4. File, total-byte, per-file, wall-time, and concurrency budgets are reported.
5. With no conclusive target fail, omission/timeout/read failure aggregates to
   `PARTIAL_VALIDATION`.

#### Assertions

- [ ] **[ST-C11-A01]** Repeated runs choose the same admitted paths.
- [ ] **[ST-C11-A02]** Every selected path has one terminal ledger class.
- [ ] **[ST-C11-A03]** Static all and audit share one implementation and budgets.
- [ ] **[ST-C11-A04]** Partial coverage never becomes an empty pass.

#### Case Verdict

`PASS` when deterministic omission is fully reported as partial; otherwise
`FAIL`.

---

### Case 12 [ST-C12]: Aggregation cross-products have one verdict

#### Fixture

Use these exact outcome vectors:

- required authority INVALID + target FAIL;
- target FAIL + unrelated coverage PARTIAL;
- target PASS + coverage PARTIAL;
- target WARN with complete coverage;
- all required PASS;
- empty required assertion set.

#### Input

Aggregate each vector with `cgs-skill-test-rules/v1`.

#### Expected reads

- Versioned aggregation table and the exact outcome vector.

#### Expected writes

- None.

#### Expected non-writes

- Target, authorities, rules, and receipts remain unchanged.

#### Expected behavior

1. Results are respectively `TEST_INFRA_INVALID`, `NON-COMPLIANT`,
   `PARTIAL_VALIDATION`, `WARNINGS`, `COMPLIANT`, and
   `TEST_INFRA_INVALID`.
2. Lower-priority axes remain visible in the trace.
3. No vector permits two aggregate verdicts.

#### Assertions

- [ ] **[ST-C12-A01]** Required-authority invalid outranks target failure.
- [ ] **[ST-C12-A02]** Conclusive target failure outranks unrelated partial.
- [ ] **[ST-C12-A03]** Empty coverage cannot pass.
- [ ] **[ST-C12-A04]** The runner and prose use the same table.

#### Case Verdict

`PASS` only when all six vectors match exactly; otherwise `FAIL`.

---

### Case 13 [ST-C13]: Canonical names expose duplicates and path aliases first

#### Fixture

- Raw names include `Skill-A`, `skill-a`, surrounding whitespace, decomposed
  Unicode, and a name longer than 64 code points.
- Two selected paths identify the same filesystem object.
- Catalog totals still match implementation totals.

#### Input

`$skill-test audit`

#### Expected reads

- Exact raw names and selected path identities from implementations and catalog.

#### Expected writes

- None.

#### Expected non-writes

- Names, paths, catalog, and specs remain unchanged.

#### Expected behavior

1. Duplicate keys use `NFC(raw).casefold()` before grammar rejection.
2. No source is silently trimmed or Unicode-normalized for acceptance.
3. Grammar, length, hyphen, and canonical-form failures remain separate.
4. Same-object paths are reported as `path_alias`.
5. Exact missing/extra/duplicate/invalid/path-alias diffs determine
   `NON-COMPLIANT`; equal totals do not pass.

#### Assertions

- [ ] **[ST-C13-A01]** Both duplicate sources are retained in evidence.
- [ ] **[ST-C13-A02]** Invalid names cannot disappear before duplicate checking.
- [ ] **[ST-C13-A03]** Path identity is independent of name identity.
- [ ] **[ST-C13-A04]** Exact set differences are deterministic.

#### Case Verdict

`PASS` when all normalization and alias defects are reported before set
comparison; otherwise `FAIL`.

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
- [ ] **[ST-PC-009]** Pinned runner and rules revisions are validated before use.
- [ ] **[ST-PC-010]** Recursive discovery, exact exclusions, budgets, and name
  normalization are shared across modes.

---

## Coverage Notes

This spec validates the written-contract analyzer and receipt protocol. It does
not run `$skill-test`, execute target skills, mutate catalog results, or prove a
future external validator implementation. Catalog receipt-reference schema, shared template/rubric migration,
hook migration, candidate-root support, and flow-diagram updates remain
separately owned work.



## P1 audit remediation trace

| Audit ID | SKILL clause | Case/assertion binding | Rejected shortcut |
|---|---|---|---|
| ST-004 | Contract Manifest / Phase 5.4 | Case 8; ST-C08-A01–A04, ST-PC-010 | Nonrecursive `.agents/skills/*/SKILL.md` discovery |
| ST-005 | Contract Manifest / Phase 5.4 | Case 8; ST-C08-A01–A04, ST-PC-010 | Unfiltered `.codex/agents/**` or hidden/generated TOML inputs |
| ST-006 | Phase 1 canonical rules | Case 9; ST-C09-A01–A03 | Subjective legacy/product/tool-name judgment |
| ST-007 | Phase 3 template parser | Case 10; ST-C10-A01–A03 | Token-only unresolved-placeholder failure |
| ST-008 | Phase 1 pinned validator | Case 7; ST-C07-A01–A03, ST-SA-010, ST-PC-009 | Optional unpinned quick validator or silent fallback |
| ST-009 | Phase 6 aggregation | Case 12; ST-C12-A01–A04, ST-SA-008 | Undefined PASS/WARN/FAIL conversion or empty COMPLIANT |
| ST-010 | Phase 5 all/audit ledger | Case 11; ST-C11-A01–A04, ST-SA-011 | Unbounded scan or unreadable-file omission reported complete |
| ST-011 | Phase 5.4 identity/diff | Case 13; ST-C13-A01–A04 and Case 8 ST-C08-A03 | Normalization collision hidden by equal totals |
