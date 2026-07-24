# Skill Spec: test-helpers

> **Spec ID**: test-helpers-v2
> **Spec Schema**: cgs-skill-spec/v2
> **Category**: utility
> **Priority**: high
> **Spec written**: 2026-07-22

## Skill Summary

test-helpers consumes one cgs-test-helper-request/v2 and a current
cgs-test-setup-receipt/v2. It generates only declared fixtures, factories,
assertions, adapters, or explicitly isolated test doubles. REAL helpers bind and
execute actual compiled production APIs; all helpers own deterministic setup and
cleanup.

Published helper artifacts bind setup layout, engine, validator, execution and
dependency authorities; production API closure; accepted requirements; runtime
configuration; helper and consumer bytes; compile, discovery, deterministic
baseline, negative-control, cleanup and publication evidence. Helper validation
always reports Business Coverage: NOT ESTABLISHED.

Owned writes are limited to manifest-declared engine-compilable helper/consumer
routes, one canonical helper contract, and immutable test-helper evidence. Test
setup authorities, production code, requirements, QA plans, business tests,
regression manifests, framework/module configuration, instruction files, and
unrelated files are non-writes.

---

## Static Assertions

- [ ] **[TH-SA-001]** Frontmatter has exactly non-empty name and description and
  name is test-helpers.
- [ ] **[TH-SA-002]** cgs-test-helpers-workflow-contract/v1 declares the v2
  request, required test-setup authorities, owned outputs, receipt schema, and
  hash algorithm.
- [ ] **[TH-SA-003]** Missing or non-current test-setup v2 receipt, layout,
  engine, validator, execution, or dependency evidence blocks with zero writes.
- [ ] **[TH-SA-004]** Unknown or unsupported engine, language, framework,
  adapter, module, or schema is explicit invalid input and never continues.
- [ ] **[TH-SA-005]** Every target resolves a complete raw-hash-bound root-to-
  parent AGENTS chain and closest applicable constraints.
- [ ] **[TH-SA-006]** Deterministic style sampling uses explicit path/hash/kind
  rows, canonical duplicate rejection, fixed kind order, and stable path order.
- [ ] **[TH-SA-007]** Samples that violate instructions or coding standards are
  excluded and never copied.
- [ ] **[TH-SA-008]** CREATE or EXTEND conflicts produce a bounded decision
  packet and require an amended request; no delete/regenerate shortcut exists.
- [ ] **[TH-SA-009]** EXTEND is AST or symbol-parser aware, insertion-bounded,
  base-hash guarded, symbol-checked, and reparsed.
- [ ] **[TH-SA-010]** REAL mode validates the production API snapshot, complete
  source/dependency closure, compiled symbol, constructor seam and execution.
- [ ] **[TH-SA-011]** GDD or requirement text supplies expected contract only
  and cannot substitute for implementation.
- [ ] **[TH-SA-012]** Business values enter executable helpers only through
  verified production-config accessors.
- [ ] **[TH-SA-013]** Helper contracts bind accepted requirement, production,
  runtime-config, test-setup and instruction hashes; any drift is STALE.
- [ ] **[TH-SA-014]** Request budgets cover items, output files, input bytes,
  candidate bytes, wall time, and tool limits with a complete ordered ledger.
- [ ] **[TH-SA-015]** Compile, discovery, runtime and receipt results distinguish
  conclusive FAIL from PARTIAL or NOT_RUN.
- [ ] **[TH-SA-016]** Fixtures freeze deterministic controls and equal semantic
  projections across baseline, negative control and isolated baseline rerun.
- [ ] **[TH-SA-017]** Every output path and symbol has one stable owner and
  publication uses an all-file compare-and-set transaction.
- [ ] **[TH-SA-018]** No invalid, partially validated, stale, conflicted or
  unowned helper is published or described as usable.
- [ ] **[TH-SA-019]** Godot, Unity and Unreal lifecycle helpers perform automatic
  failure-safe cleanup and assert restored baselines.
- [ ] **[TH-SA-020]** No mode invokes another workflow, director gate, commit,
  push, publication, or business-coverage claim.

---

## Test Cases

### Case 1 [TH-C01]: Current test-setup authority is a zero-write prerequisite

#### Fixture

- A helper request names exact setup receipt, layout, engine, repository policy,
  validator, execution and dependency paths and hashes.
- Negative variants omit tests, use setup receipt schema v1, use a stale layout
  hash, have partial validator coverage, or lack current discovery and CI proof.

#### Input

- Invoke test-helpers with the exact request-manifest path.

#### Expected reads

- Raw request bytes and every test-setup receipt dependency.
- Current candidate/build identity, setup state axes and receipt signature or
  content hash.

#### Expected writes

- None for every negative variant.
- For a fully current variant, prerequisite audit evidence remains staged until
  the complete candidate changeset is authorized.

#### Expected non-writes

- Helper sources, consumers, contracts, logs, framework configuration, test-setup
  manifests and production files on prerequisite failure.

#### Expected behavior

- Recompute setup receipt freshness from all declared dependencies.
- Require Audit Coverage COMPLETE, Static Validation PASS, Verification Level
  CI_VERIFIED, Determinism VERIFIED, Receipt Freshness CURRENT, Setup Status
  VERIFIED and Gate Eligible YES.
- A missing, stale, invalid, partial, unreadable or unverified dependency blocks
  generation with zero project writes.
- Routes and argv are resolved only from current setup manifests.

#### Assertions

- [ ] Path existence or newest receipt selection provides no proof.
- [ ] Missing tests never falls through to generation.
- [ ] The exact prerequisite owner and failed dependency are reported.
- [ ] No other workflow is invoked automatically.

#### Case Verdict

PASS when every non-current setup variant blocks with zero writes and the current
variant alone advances; any continued generation is FAIL.

---

### Case 2 [TH-C02]: Unknown engine or framework is explicit invalid input

#### Fixture

- Request variants contain an unknown engine alias, unsupported language,
  framework not present in the dependency lock, missing adapter row, wrong module
  or unsupported request schema.
- A valid variant matches the setup engine and validator authorities exactly.

#### Input

- Invoke with one variant at a time.

#### Expected reads

- Request, engine authority, layout, validator and execution manifests,
  dependency lock and setup receipt.

#### Expected writes

- None for invalid variants.

#### Expected non-writes

- Framework adapters, module or assembly definitions, project descriptors and
  helper candidates.

#### Expected behavior

- Unknown or unsupported identity produces Input Status INVALID and Workflow
  Status INVALID with exact field evidence.
- No engine, framework, module, adapter or argv is guessed or synthesized.
- A well-formed but temporarily unavailable external prerequisite is BLOCKED with
  partial axes rather than misclassified as valid or invalid candidate code.

#### Assertions

- [ ] Framework field selects one exact approved adapter row.
- [ ] Engine and language agree with the structured setup authority.
- [ ] Error state is terminal for generation.
- [ ] Zero project writes occur.

#### Case Verdict

PASS when every invalid identity stops explicitly and only the exact matching
adapter is routable; otherwise FAIL.

---

### Case 3 [TH-C03]: Closest instruction constraints bind each target

#### Fixture

- Root AGENTS defines general code rules.
- tests AGENTS defines naming, AAA, deterministic isolation and cleanup.
- An engine module subtree defines a closer route-specific rule.
- One variant makes an applicable instruction unreadable.

#### Input

- A request proposes helper, consumer, contract and evidence targets in different
  directory trees.

#### Expected reads

- Complete root-to-parent instruction chain for every proposed target.
- Raw hashes and precedence of selected instruction sources.

#### Expected writes

- Only candidates whose instruction chains are complete and conflict-free.

#### Expected non-writes

- Every instruction file and every target with unreadable or conflicting
  applicable constraints.

#### Expected behavior

- Targets are enumerated before generation.
- Selected, loaded, unreadable, omitted and superseded instruction entries are
  recorded per target.
- Closest applicable naming, AAA, fixture, isolation, lifecycle, ownership and
  engine rules become generation constraints.
- Unreadable or conflicting chains set Instruction Coverage PARTIAL and block
  affected items.

#### Assertions

- [ ] No repository-specific naming fallback overrides a closer rule.
- [ ] Every effective rule records source path and hash.
- [ ] A style sample cannot override instruction authority.
- [ ] Partial instruction coverage is never VERIFIED.

#### Case Verdict

PASS for correct per-target precedence and fail-closed partial handling;
otherwise FAIL.

---

### Case 4 [TH-C04]: Style sampling is deterministic and rejects anti-patterns

#### Fixture

- The request lists more than five explicit path/hash/kind sample rows in shuffled
  order.
- Two rows are canonical path duplicates.
- Some samples contain shared mutable state, missing teardown or generic
  metadata-only factories.
- Remaining valid rows span fixture, factory, assertion, adapter and test-double.

#### Input

- Run prerequisite and sampling phases repeatedly with identical bytes.

#### Expected reads

- Every admitted sample, pinned parser and current instruction/coding-standard
  rules.

#### Expected writes

- Sampling itself writes nothing.

#### Expected non-writes

- Samples, generated candidates and excluded anti-pattern copies.

#### Expected behavior

- Normalize paths with Unicode NFC, forward slashes and case-fold comparison.
- Reject canonical duplicates and hash mismatches.
- Parse and exclude violations before selection.
- Group valid rows in fixture, factory, assertion, adapter, test-double order;
  sort each group by normalized then raw path; select the first per kind up to
  five and fill any capacity from globally sorted remaining valid rows.
- Record selected and excluded rows with hashes and rule IDs.

#### Assertions

- [ ] Repeated runs produce the same ordered selection.
- [ ] Invalid samples are not copied and do not silently consume a slot.
- [ ] Samples influence style only, never production semantics.
- [ ] No representative-sample randomness or filesystem order is used.

#### Case Verdict

PASS when selection and exclusion ledgers are byte-stable across repeats;
otherwise FAIL.

---

### Case 5 [TH-C05]: Existing helper conflict requires an explicit safe choice

#### Fixture

- CREATE targets an existing owned helper.
- An AST parser and current base hash support a safe EXTEND option.
- A distinct canonical layout route can support a safe CREATE option.
- Variants contain a symbol conflict, parser unavailability or concurrent base
  change.

#### Input

- Initial request declares CREATE; a later amended request may declare one chosen
  safe operation.

#### Expected reads

- Existing raw bytes/hash, ownership table, AST or symbol table, layout routes,
  parser row and requested exported signatures.

#### Expected writes

- Initial conflict writes nothing.
- A valid amended EXTEND changes only the parser-defined insertion span.
- A valid amended CREATE writes only the new absent owned path.

#### Expected non-writes

- Existing manual symbols outside the insertion span, unrelated files and any
  target under an unsafe option.

#### Expected behavior

- Emit a bounded decision packet describing EXTEND and CREATE only when each is
  safe, including effects and conflicts.
- Require amended signed request authority before continuing.
- EXTEND verifies exact base hash, rejects symbol conflicts, inserts declared
  symbols only, preserves outside bytes and reparses.
- Parser unavailable or concurrent drift blocks the operation.

#### Assertions

- [ ] No automatic skip, rename, delete or full regeneration occurs.
- [ ] Unsafe choices are omitted rather than advertised.
- [ ] Outside-span bytes remain identical.
- [ ] Concurrent base change produces zero target writes.

#### Case Verdict

PASS for explicit choice, bounded AST patch and preservation; any implicit choice
or overwrite is FAIL.

---

### Case 6 [TH-C06]: REAL helper binds the compiled production API graph

#### Fixture

- An accepted requirement describes an expected combat observable.
- A cgs-production-api-snapshot/v1 binds producer/tool hash, source closure,
  compiled type/signature, constructor seam, dependency edges and config
  accessor.
- Negative variants use a GDD-only type, stale source closure, invented
  constructor, unavailable module import, bare metadata object or wrong compiled
  signature.

#### Input

- Request one REAL factory and helper-only consumer.

#### Expected reads

- Accepted requirement and owner evidence, production API snapshot and complete
  dependency/source/config closure, setup engine/module authority and QA mapping.

#### Expected writes

- Only a verified candidate that imports, instantiates and executes the exact
  production symbol; none for conflicting variants.

#### Expected non-writes

- Production code, runtime configuration, requirements, project module files and
  fake substitute implementations.

#### Expected behavior

- Rehash the API snapshot and complete source closure.
- Resolve actual module, type, normalized signature, constructor or injection
  seam, dependency graph and config accessor.
- Compile against the existing test module without adding configuration.
- Consumer execution evidence binds the real compiled production path.
- Requirement/API/implementation differences set Production Binding
  CONFLICTING or STALE and block the item.

#### Assertions

- [ ] GDD expected behavior never proves implementation exists.
- [ ] Bare Node, GameObject, UObject, metadata or invented class cannot be REAL.
- [ ] Execution evidence names exact production symbol and hashes.
- [ ] ISOLATED_FAKE cannot be silently substituted.

#### Case Verdict

PASS only for verified compiled real-SUT binding; otherwise BLOCKED or INVALID
with no published helper.

---

### Case 7 [TH-C07]: Constants and defaults retain authoritative provenance

#### Fixture

- A helper needs a business-affecting damage value, a requirement expected value
  and a semantically irrelevant local object label.
- Production exposes the damage value through a current config accessor.
- A negative variant copies the GDD number into executable helper setup.
- Another variant changes production config or requirement bytes after validation.

#### Input

- Generate and validate the helper contract.

#### Expected reads

- Runtime-config accessor and source closure, accepted requirement, API snapshot,
  helper request and consumer expectation.

#### Expected writes

- Candidate and contract only when every literal has valid provenance.

#### Expected non-writes

- Production config, requirements and duplicated business constants.

#### Expected behavior

- Classify values as PRODUCTION_CONFIG, REQUIREMENT_EXPECTED_ONLY or
  TEST_LOCAL_NONBUSINESS.
- Business setup values enter code only via verified production accessor.
- Requirement expected values appear only in consumer expectations and retain
  requirement path/hash.
- Contract records class, symbol, source hash and owner for every value.
- Source drift makes candidate or published contract STALE.

#### Assertions

- [ ] Stable IDs or unchanged text cannot override hash drift.
- [ ] Requirement values never initialize the SUT.
- [ ] Local values are shown irrelevant to business outcome.
- [ ] Downstream consumer must rehash all value sources.

#### Case Verdict

PASS for complete provenance and stale detection; copied or unbound business
values are FAIL.

---

### Case 8 [TH-C08]: Batch budgets and partial ledger are deterministic

#### Fixture

- A request declares more items than maximum items and files.
- Later items cross input-byte or wall-time limits.
- Some admitted items verify, one conclusively fails compile, one has runner
  timeout and several are never admitted.

#### Input

- Run with frozen budget values at or below workflow hard maxima.

#### Expected reads

- Request header and item metadata first, then only whole admitted item source
  sets in canonical Helper ID and output-path order.

#### Expected writes

- After authorization, only verified item candidates, contracts and evidence.
- No invalid, partially validated, omitted or unprocessed helper targets.

#### Expected non-writes

- Items outside the admitted set and every source authority.

#### Expected behavior

- Budgets cover items, output files, input bytes, candidate bytes, wall time and
  per-tool time/output.
- Record selected, loaded, verified, invalid, blocked, omitted, unreadable and
  unprocessed rows with stable reason IDs and consumption.
- Remaining items become ordered OMITTED when a budget is exhausted.
- Conclusive compiler failure is INVALID; timeout or unavailable runner is
  PARTIAL VALIDATION.
- Mixed verified publication yields Workflow Status PARTIAL.

#### Assertions

- [ ] No item is silently truncated or partially loaded.
- [ ] Same request and budgets produce the same ledger.
- [ ] No verified item means partial infrastructure yields BLOCKED and zero
  helper publication.
- [ ] Counts reconcile to all declared items.

#### Case Verdict

PASS when ledger, publication subset and status are deterministic and complete;
otherwise FAIL.

---

### Case 9 [TH-C09]: Compile and discovery distinguish failure from incomplete evidence

#### Fixture

- Candidate bytes and setup manifests are current.
- Variants include conclusive compile diagnostics, complete zero discovery,
  compiler timeout, unavailable parser, truncated log, missing receipt field and
  successful compile/discovery.

#### Input

- Validate candidates in the isolated staging tree using only pinned argv rows.

#### Expected reads

- Validator and execution manifests, adapter/dependency hashes, candidate source,
  parser schemas and current setup receipt.

#### Expected writes

- Immutable logs and receipts for checks that actually ran.
- No project helper publication until the candidate is fully verified.

#### Expected non-writes

- Synthesized shell commands, fallback runners, fabricated receipts and
  partially validated helper targets.

#### Expected behavior

- Conclusive current compile diagnostics map Compile Status FAIL.
- Complete zero discovery maps Discovery Status ZERO.
- Timeout, unavailable or unsupported tool, truncated/incomplete output,
  unreadable evidence or missing receipt fields map PARTIAL or NOT_RUN.
- Every receipt binds argv, tool/parser versions and hashes, inputs, timestamps,
  exit class, output/log hashes, rule coverage and producer.

#### Assertions

- [ ] Infrastructure partial is not mislabelled invalid candidate code.
- [ ] Conclusive invalid code is not hidden as partial.
- [ ] Static source generation never proves compile or discovery.
- [ ] Only current complete receipts can support VERIFIED CANDIDATE.

#### Case Verdict

PASS when every variant receives the exact fail-closed classification; otherwise
FAIL.

---

### Case 10 [TH-C10]: Fixtures are deterministic across pass, fail and cleanup

#### Fixture

- Seed, order, locale, timezone, environment-name set, parallelism, timeout,
  cleanup baseline and projection schema are frozen.
- A helper consumer passes, its controlled negative condition fails and a clean
  consumer rerun passes.
- Negative variants leak a signal/object/world, change production-path binding,
  produce a different observable or lack a deterministic control.

#### Input

- Run the three-stage helper validation sequence.

#### Expected reads

- Current candidate, production/API/config authorities, adapter/manifest rows and
  frozen controls.

#### Expected writes

- Complete, untruncated, redacted baseline, negative and rerun logs and v2
  validation receipts.

#### Expected non-writes

- Ad hoc retry policy, changed controls, persistent fixture state and ordinary
  business-test evidence.

#### Expected behavior

- Both pass projections contain equal discovered ID, production-path binding,
  outcome, observable and cleanup baseline.
- Timestamps and durations remain evidence but are excluded from equality.
- Negative control is a conclusive expected helper-contract FAIL, not timeout or
  infrastructure error.
- Cleanup runs on pass and fail paths.
- Projection mismatch yields Determinism UNSTABLE; missing control yields PARTIAL.

#### Assertions

- [ ] No retry is added after observing failure.
- [ ] Godot connections, Unity objects/subscriptions and Unreal worlds/contexts
  return to adapter baseline.
- [ ] Failure sensitivity is limited to helper contract, not business coverage.
- [ ] A leak prevents publication.

#### Case Verdict

PASS only for equal isolated pass projections, expected negative failure and
verified cleanup; otherwise INVALID or PARTIAL with no publication.

---

### Case 11 [TH-C11]: Ownership table and all-file CAS preserve concurrent work

#### Fixture

- A verified publication batch contains CREATE and EXTEND operations plus
  consumer, contract, receipt and log outputs.
- Every path has one stable owner, precondition and final hash.
- One variant introduces canonical path/symbol collision.
- Another changes one EXTEND base after preview.

#### Input

- Preview then publish the exact transaction.

#### Expected reads

- Ownership table, every current authority, CREATE absence, EXTEND preimage,
  candidate postimages and transaction-adapter contract.

#### Expected writes

- On a clean variant, the exact all-or-none authorized batch.
- On collision, authority drift or preimage mismatch, no target writes and one
  immutable blocked receipt outside target paths.

#### Expected non-writes

- Diverged user bytes, unrelated files, unowned paths and blanket backup restores.

#### Expected behavior

- Canonical path or symbol collisions block all involved items.
- Immediately before first write, all authorities and path preconditions are
  rehashed.
- Unsupported atomic/recovery semantics yield Ownership/CAS PARTIAL and publish
  nothing.
- Clean publish stages and verifies hashes, commits all-or-none, rereads bytes and
  reparses symbols.
- Interrupted publication records PREIMAGE, POSTIMAGE and DIVERGED states and
  requires separate authorized three-way/CAS recovery.

#### Assertions

- [ ] Any preflight mismatch writes zero target files.
- [ ] Each final path has exactly one owner.
- [ ] Backups never overwrite divergent work automatically.
- [ ] Read-back hashes equal validated candidate hashes.

#### Case Verdict

PASS for no-write conflicts and exact transactional publication; any collateral
or partial overwrite is FAIL.

---

### Case 12 [TH-C12]: Fully verified helper publishes without business claims

#### Fixture

- v2 request and all setup authorities are current.
- Instruction coverage and production binding verify.
- Samples are deterministic and valid.
- REAL helper and consumer compile and discover in the existing engine test
  module.
- Equal isolated baselines surround the expected negative control and cleanup
  passes.
- Ownership/CAS publication and read-back succeed.

#### Input

- One exact authorized helper request and run identity.

#### Expected reads

- Every request, setup, instruction, production API, requirement, config,
  dependency, candidate, validator, execution, log and receipt dependency.

#### Expected writes

- Exact owned helper/consumer paths, canonical cgs-test-helper-artifact/v2,
  immutable cgs-test-helper-validation-receipt/v2 and logs.

#### Expected non-writes

- Production, requirements, QA plans, business tests, regression manifests,
  framework/module configuration, instruction files, session state and
  downstream workflows.

#### Expected behavior

- All independent axes are current and verified.
- Workflow Status is VERIFIED, Ownership/CAS is VERIFIED and Receipt Freshness is
  CURRENT.
- Helper is described as usable only for helper infrastructure.
- Business Coverage remains NOT ESTABLISHED.
- No director gate or downstream workflow is invoked.

#### Assertions

- [ ] Contract binds all source and authority hashes and normalized symbols.
- [ ] Receipt binds compile, discovery, both baselines, negative control,
  production path, determinism, cleanup, logs and publication.
- [ ] Stable AC annotations do not claim coverage.
- [ ] Persistence or read-back failure removes usable status.

#### Case Verdict

PASS only for the complete current transaction; every missing or stale predicate
fails closed.

---

## Protocol Compliance

- [ ] **[TH-PC-001]** Exact request path, schema, IDs, canonical paths and hard
  budgets validate before item source loading.
- [ ] **[TH-PC-002]** Test-setup receipt and layout/engine/validator/execution/
  dependency authorities are rehashed and current before generation.
- [ ] **[TH-PC-003]** Every target has a complete closest-rule instruction chain.
- [ ] **[TH-PC-004]** Production API and accepted-requirement owners remain
  distinct and discrepancies are explicit.
- [ ] **[TH-PC-005]** REAL and ISOLATED_FAKE claims are non-overlapping and
  Business Coverage is always NOT ESTABLISHED.
- [ ] **[TH-PC-006]** Commands use pinned argv arrays with environment allowlist,
  timeout, output cap, redaction, parser and process-tree cleanup.
- [ ] **[TH-PC-007]** Compile/discovery/runtime partiality is preserved and never
  converted to PASS or hidden as conclusive invalidity.
- [ ] **[TH-PC-008]** Deterministic controls are frozen before execution and no
  post-observation retry policy is invented.
- [ ] **[TH-PC-009]** CREATE and EXTEND ownership preconditions use all-file CAS.
- [ ] **[TH-PC-010]** Only verified candidates enter the publication set and
  mixed outcomes retain a complete ledger.
- [ ] **[TH-PC-011]** Multi-file persistence is transactionally staged, hash-
  verified, read back and recovery-safe.
- [ ] **[TH-PC-012]** No production/shared authority, downstream workflow, gate,
  commit, push or publication is modified or invoked.

## Coverage Notes

```yaml
schema: cgs-p1-remediation-trace/v1
entries:
  - audit_id: TH-005
    skill_clause_id: TH-CL-005
    spec_case_id: TH-C01
    assertion_ids: [TH-SA-003, TH-PC-002]
  - audit_id: TH-006
    skill_clause_id: TH-CL-006
    spec_case_id: TH-C02
    assertion_ids: [TH-SA-004, TH-PC-006]
  - audit_id: TH-007
    skill_clause_id: TH-CL-007
    spec_case_id: TH-C03
    assertion_ids: [TH-SA-005, TH-PC-003]
  - audit_id: TH-008
    skill_clause_id: TH-CL-008
    spec_case_id: TH-C04
    assertion_ids: [TH-SA-006, TH-SA-007, TH-PC-008]
  - audit_id: TH-009
    skill_clause_id: TH-CL-009
    spec_case_id: TH-C05
    assertion_ids: [TH-SA-008, TH-SA-009, TH-PC-009]
  - audit_id: TH-010
    skill_clause_id: TH-CL-010
    spec_case_id: TH-C06
    assertion_ids: [TH-SA-010, TH-SA-011, TH-PC-004, TH-PC-005]
  - audit_id: TH-011
    skill_clause_id: TH-CL-011
    spec_case_id: TH-C07
    assertion_ids: [TH-SA-012, TH-SA-013, TH-PC-004]
  - audit_id: TH-012
    skill_clause_id: TH-CL-012
    spec_case_id: TH-C08
    assertion_ids: [TH-SA-014, TH-SA-018, TH-PC-001, TH-PC-010]
```

Each P1 audit ID therefore has an exact clause/case/assertion join rather than a
prose range. Cases TH-C09 through TH-C12 preserve and strengthen the P0 compile/
discovery, lifecycle, real-SUT, cleanup, and transaction guarantees. This written
spec does not claim that an engine adapter, compiler, runner, or generated helper
executed; those claims require current pinned runtime receipts.
