# Skill Spec: $test-helpers

> **Category**: utility
> **Priority**: low
> **Spec written**: 2026-07-22

## Skill Summary

$test-helpers consumes one exact helper-request manifest and generates only declared fixtures, factories, assertions, adapters, or isolated test doubles. REAL helpers must import and execute actual production types. Every published helper has stable AC/test annotations, raw source hashes, a separate canonical helper-contract hash, a compiled/discovered helper-only consumer, baseline and negative-control receipts, and automatic cleanup evidence. Helper validation never establishes business coverage.

---

## Static Assertions

- [ ] YAML frontmatter contains only name and a non-empty description; name is test-helpers
- [ ] The only accepted input is an exact helper-request manifest
- [ ] tests/, framework manifest/discovery receipt, engine adapter, and applicable AGENTS chain are mandatory prerequisites
- [ ] REAL and ISOLATED_FAKE modes have non-overlapping claims
- [ ] REAL helpers must instantiate and execute declared production types/symbols
- [ ] Bare metadata objects cannot masquerade as production SUTs
- [ ] Godot, Unity, and Unreal lifecycle requirements include automatic failure-safe cleanup assertions
- [ ] Unreal helpers require an existing compiled Tests module and RAII world/context ownership
- [ ] Every helper source has stable annotations and a separate deterministic helper-contract hash
- [ ] Validation requires compile, discovery, baseline PASS, negative-control FAIL, real-SUT path evidence, and cleanup PASS
- [ ] INVALID candidates are not published or described as usable
- [ ] Existing helpers use hash-guarded AST/symbol-aware additive extension
- [ ] Final output always reports Business Coverage: NOT ESTABLISHED
- [ ] The final phase recommends remediation without invoking another workflow

---

## Director Gate Checks

- **Full mode**: N/A; no director gate is invoked.
- **Lean mode**: N/A; no director gate is invoked.
- **Solo mode**: N/A; no director gate is invoked.
- **Validation distinction**: compiler/test-runner execution validates helper infrastructure and is not a director approval or release gate.

---

## Test Cases

### Case 1: Happy path — real SUT factory is validated before publication

**Fixture**:
- The request binds a CURRENT QA plan, stable AC/test IDs, actual CombatComponent type/source/config hashes, framework/adapter/module hashes, and an unused helper/run ID.
- The generated factory instantiates CombatComponent through its production constructor/dependency seam.
- The consumer calls the declared production damage path.

**Expected behavior**:
1. The helper and consumer compile in the actual test module and are discovered.
2. Baseline consumer passes and its receipt proves the production symbol executed.
3. The controlled wrong-observable negative run fails.
4. Cleanup passes and the authorized files are atomically written/read back.
5. Workflow Status is VERIFIED and Business Coverage is NOT ESTABLISHED.

**Assertions**:
- [ ] No generic metadata-only substitute is created
- [ ] Helper source and deterministic contract hashes are reported
- [ ] Stable AC/test annotations do not claim coverage
- [ ] Usable is stated only after final read-back verification

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 2: Missing test framework blocks with zero writes

**Fixture**:
- tests/, the framework manifest, current discovery receipt, or the engine adapter is absent/invalid.

**Expected behavior**:
1. Prerequisite validation reports every missing or mismatched artifact.
2. Workflow Status is BLOCKED.
3. No helper, consumer, contract, receipt, log, module, or framework file is written.

**Assertions**:
- [ ] Unknown engine/language/framework does not continue
- [ ] No COMPLETE/VERIFIED claim appears
- [ ] The exact prerequisite owner is identified without auto-running another workflow

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 3: Fake cannot impersonate the production system

**Fixture**:
- A requested factory would return a bare Node/GameObject/UObject and store health/attack metadata.
- The item is declared REAL.

**Expected behavior**:
1. The candidate is rejected because it neither imports nor executes the production SUT.
2. It is not relabelled automatically as a valid real factory.
3. A separately declared ISOLATED_FAKE is allowed only at a hash-bound interface seam and carries Business Coverage: NOT ESTABLISHED.

**Assertions**:
- [ ] Metadata manipulation cannot prove actual combat/player code ran
- [ ] Fake output is visibly labelled in source, contract, and receipt
- [ ] A fake cannot become a business formula oracle

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 4: Unreal helper compiles in Tests module and cleans world context

**Fixture**:
- Existing project Tests module, Build.cs/Target/include/dependency hashes, and Unreal adapter are valid.
- The helper requests an isolated test world.

**Expected behavior**:
1. Header/source and consumer are placed inside the compiled Tests module.
2. RAII fixture owns the world and exact FWorldContext.
3. Baseline and forced-failure paths both invoke teardown.
4. Post-scope assertions find no world, context, delegate, timer, actor, or root leak.

**Assertions**:
- [ ] Nothing is emitted only to tests/helpers as an uncompiled Unreal header
- [ ] No bare UWorld pointer delegates cleanup to the caller
- [ ] Tests module compile and discovery receipts are required

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 5: Director gate — none

**Fixture**:
- A valid request under any external review mode.

**Expected behavior**:
1. No director agent or gate is invoked.
2. Engine adapter validation alone determines helper candidate status.

**Assertions**:
- [ ] No CD-, TD-, AD-, PR-, or QL-gate appears
- [ ] VERIFIED helper status is not called director approval
- [ ] Business Coverage remains NOT ESTABLISHED

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 6: Compile or consumer failure prevents usable publication

**Fixture**:
- Candidate generation succeeds, but compile fails, discovery misses the consumer, baseline fails, negative control unexpectedly passes, or cleanup detects a leak.

**Expected behavior**:
1. Candidate status is INVALID CANDIDATE with exact receipt/log evidence.
2. The helper and contract are excluded from the project changeset.
3. If every item is invalid, Workflow Status is INVALID and no helper files are written.

**Assertions**:
- [ ] Source creation alone never produces VERIFIED
- [ ] Parser error, timeout, truncated log, or invalid receipt is also invalid
- [ ] Output never tells consumers to use the failed helper

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 7: Godot signal and Unity object lifecycles are failure-safe

**Fixture**:
- Godot helpers cover zero-, one-, and multi-argument signals.
- Unity helper owns GameObjects, ScriptableObjects, and event subscriptions.
- One consumer assertion intentionally throws/fails.

**Expected behavior**:
1. Godot validates signal existence/arity, uses one-shot capture where applicable, and disconnects on failure.
2. Unity teardown destroys/unsubscribes all owned resources on failure.
3. Adapter snapshots return to baseline.

**Assertions**:
- [ ] No permanent signal connection remains
- [ ] No caller-managed DestroyImmediate requirement remains
- [ ] Cleanup is verified for both baseline and negative-control paths

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 8: Production or requirement hash change makes candidate stale

**Fixture**:
- Candidate validation completed.
- Before write, a production source, runtime config, requirement, applicable AGENTS file, adapter, or EXTEND base changes.

**Expected behavior**:
1. Immediate pre-write re-hash detects the changed bytes.
2. The affected operation aborts.
3. No stale helper/contract is published or described as verified.

**Assertions**:
- [ ] Dates or unchanged names cannot override a digest mismatch
- [ ] Consumer revalidation can later mark a published helper contract STALE
- [ ] Stable IDs remain identifiers, not freshness proof

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 9: Existing helper extension preserves manual code

**Fixture**:
- EXTEND declares the exact existing source hash and one new exported symbol.
- The language AST/symbol parser is available.

**Expected behavior**:
1. Existing hash is verified and symbol conflicts are checked.
2. Only the parser-defined insertion span changes.
3. Bytes outside that span and existing symbols remain unchanged.
4. The extended candidate is reparsed and fully validated.

**Assertions**:
- [ ] No whole-file overwrite or delete-and-regenerate instruction appears
- [ ] A concurrent edit blocks the operation
- [ ] Parser unavailability blocks safe extension

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 10: Batch budget and cross-skill contract are explicit

**Fixture**:
- The request declares six items but a maximum of four.
- Four candidates verify, one is omitted by policy, and one fails cleanup.

**Expected behavior**:
1. Ordered omitted/invalid lists preserve all six items.
2. Only the four verified candidates appear in the authorized write set.
3. Overall Workflow Status is PARTIAL after successful persistence.
4. Contract manifests expose source/helper/requirement hashes to test-evidence-review.
5. Regression-suite is told that helper validation is not a business-test sensitivity receipt.

**Assertions**:
- [ ] No item is silently truncated
- [ ] Partial does not hide failed or omitted items
- [ ] test-helpers is never recommended as a substitute for a missing regression/business test

**Case Verdict**: PASS / FAIL / PARTIAL

---

## Protocol Compliance

- [ ] Explicit bounded requests authorize all declared in-scope writes
- [ ] Otherwise the fully validated changeset is previewed and approved once
- [ ] Production, business-test, QA-plan, regression, framework, module, and session-state files remain non-writes
- [ ] Commands come only from verified argv adapters with timeout, output cap, parser, redaction, and process-tree cleanup
- [ ] Multi-file publication is transactional and read-back verified
- [ ] No invalid helper remains in an approved write set
- [ ] Every published helper has immutable validation evidence and a deterministic contract hash
- [ ] The workflow never invokes another workflow or claims business coverage

---

## Coverage Notes

This is a behavioral specification, not an executed test result. Runtime fixtures should cover manifest/path validation, nested AGENTS conflicts, all three engine adapters, REAL/ISOLATED_FAKE boundaries, Godot signal arities, Unity failure-path disposal, Unreal Tests-module linking and RAII cleanup, stable annotations, contract canonicalization, negative controls, timeouts/truncated logs, AST-safe extension, concurrent changes, batch budgets, transactional writes, and downstream stale-contract detection.
