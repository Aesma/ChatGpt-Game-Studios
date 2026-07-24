---
name: test-helpers
description: "Generates hash-bound engine test fixtures and helper contracts against real production APIs, then compiles, discovers, exercises, and cleanup-validates them before publication."
---

## Invocation and boundary

Invoke only as:

~~~text
$test-helpers --manifest {helper-request-manifest-path}
~~~

The manifest is mandatory. Reject legacy system-name, all, scaffold, or helper-name positional arguments; unknown/duplicate flags; missing values; directories; and ambiguous scope. Do not infer a current engine, system, test framework, helper set, or newest file.

## Contract manifest

This normative workflow contract is versioned independently from prose:

~~~yaml template
schema: cgs-test-helpers-workflow-contract/v1
input_schema: cgs-test-helper-request/v2
required_test_setup:
  receipt_schema: cgs-test-setup-receipt/v2
  layout_manifest: tests/test-layout-manifest.json
  validator_manifest: tests/test-setup-validator-manifest.json
  execution_manifest: tests/test-execution-manifest.json
owned_outputs:
  helper_contract: tests/helpers/contracts/<request-id>.json
  evidence_root: production/qa/evidence/test-helpers/<request-id>/<run-id>/
output_contract_schema: cgs-test-helper-artifact/v2
validation_receipt_schema: cgs-test-helper-validation-receipt/v2
hash_algorithm: sha256
~~~

The request must name the exact current test-setup receipt and every manifest above
with raw SHA-256. Re-hash their full dependency sets; names, dates, or successful old
runs do not establish freshness.

This workflow owns only the exact operations declared by the validated manifest:

- helper source files in engine-compilable test routes;
- helper-contract manifests under tests/helpers/contracts/{request-id}.json;
- helper-only validation consumer tests under the engine's compiled test module;
- immutable validation evidence under production/qa/evidence/test-helpers/{request-id}/{run-id}/.

It never edits production code, requirements, QA plans, business tests, regression manifests, test-framework configuration, module/assembly definitions, or session state. If required module/assembly configuration is absent, stop and identify its owner; do not silently create it.

An explicit bounded request authorizes the declared files. Otherwise, after candidate validation and before the first project write, present one complete changeset and obtain one explicit approval. Do not re-prompt within that boundary. New files or operations discovered after approval are material scope expansion.

This workflow never invokes a director gate or another workflow.

## Outcome vocabulary

Report one Workflow Status:

- VERIFIED: every published helper compiled, was discovered, passed its baseline helper consumer, failed its negative control as expected, passed cleanup checks, and was written/read back exactly;
- PARTIAL: a declared batch had both verified published helpers and invalid/omitted items, all listed explicitly;
- INVALID: no requested helper passed required validation, so no helper or helper contract was published;
- BLOCKED: prerequisites, scope, authorization, concurrent-edit protection, or persistence prevented publication.

Report these axes independently:

| Axis | Values |
|---|---|
| Input Status | VALID, INVALID |
| Setup Prerequisite | CURRENT, STALE, INVALID, PARTIAL, NOT_RUN |
| Instruction Coverage | COMPLETE, PARTIAL |
| Production Binding | VERIFIED, CONFLICTING, STALE, NOT_APPLICABLE |
| Compile Status | PASS, FAIL, PARTIAL, NOT_RUN |
| Discovery Status | VERIFIED, ZERO, PARTIAL, NOT_RUN |
| Determinism Status | VERIFIED, UNSTABLE, PARTIAL, NOT_RUN |
| Ownership/CAS | VERIFIED, CONFLICT, PARTIAL, NOT_RUN |
| Receipt Freshness | CURRENT, STALE, INVALID, UNVERIFIED |

Also report Business Coverage: NOT ESTABLISHED for every outcome. A helper validation receipt proves only the helper contract. It never proves a business AC is covered, that a regression test exists, or that a release test passed.

Missing, unreadable, unavailable, unsupported, timed-out, truncated, omitted, stale,
or incompletely covered prerequisites/tests are PARTIAL or NOT_RUN, never PASS. A
conclusive compiler or consumer assertion failure is FAIL. Do not collapse partial
infrastructure into an invalid helper, or an invalid helper into infrastructure
partiality.

## Phase 1: Validate framework, engine, instructions, and scope

Resolve the supplied literal manifest path and real path. Reject symlinks escaping the project root, malformed syntax, duplicate keys, unsupported schema, unsafe slugs, dot segments, and paths outside the project root. Read raw bytes once and compute SHA-256 over exact bytes.

Require Artifact Type: test-helper-request, Schema Version: 2 and:

- unique request ID and run ID, neither a date alone;
- exact `cgs-test-setup-receipt/v2` path/hash and its declared candidate/build IDs;
- exact engine-authority, repository-policy, layout-manifest, validator-manifest,
  execution-manifest, dependency-lock, test-framework, and current setup discovery/
  CI receipt paths/hashes copied from that setup receipt;
- exact engine, engine version, language, project root, module/assembly, and test
  framework copied from the current engine/layout authorities;
- exact engine-adapter ID/path/hash and validator-manifest row IDs for compile,
  discovery, consumer-run, AST/symbol parse, receipt parse, timeout, output-cap,
  cleanup, and result parsing;
- exact QA-plan path/hash and effective CURRENT source snapshot when stable AC/test IDs are declared;
- exact `cgs-production-api-snapshot/v1` path/hash with producer/tool/version/hash,
  source-closure ledger, exported symbols/signatures, constructors, dependency edges,
  runtime-config accessors, and compile identity;
- ordered helper items;
- batch limits: maximum items, output files, source/input bytes, candidate bytes,
  wall time, and per-tool time/output bytes, all at or below contract maxima;
- explicit omitted-item policy;
- exact existing-pattern sample paths/hashes when style sampling is requested.

Each helper item requires:

- stable Helper ID and helper kind: fixture, factory, assertion, adapter, or test-double;
- SUT Mode: REAL or ISOLATED_FAKE;
- stable AC IDs and stable test/check IDs from the CURRENT QA plan, or an explicit NONE when the helper is framework-only;
- requirement source paths/hashes and expected observable;
- real production type/module/symbol, source paths/hashes, constructor/dependency seams, and runtime config sources/hashes for REAL mode;
- interface/protocol source paths/hashes and allowed seam for ISOLATED_FAKE mode;
- exact output path, engine module/assembly, operation CREATE or EXTEND, and expected base-file hash for EXTEND;
- exported helper symbols and normalized signatures;
- exact helper-only consumer test path and canonical test name;
- cleanup obligations and resource types;
- validation failure condition for the negative control.
- stable ownership ID for every proposed source, consumer, contract, receipt, and log;
- deterministic controls: seed, order, locale, timezone, environment-name set,
  parallelism, cleanup baseline, and semantic-projection schema.

Canonicalize request/helper IDs and project-relative paths with Unicode NFC, forward
slashes, and case-folded comparison keys while preserving raw spelling for evidence.
Reject canonical duplicates, path traversal, duplicate helper/ownership IDs, duplicate
output paths, unmapped stable IDs, noncanonical slugs, invalid operations, or scope
above hard contract maxima.

Before loading item sources, sort items by canonical Helper ID then canonical output
path. Admit only whole items that fit every declared budget. Record a complete ledger
of selected, loaded, verified, invalid, blocked, omitted, unreadable, and unprocessed
items with reason/rule IDs and bytes/time consumed. Never silently truncate a batch.
When a wall/input budget is exhausted, mark every remaining item OMITTED in sorted
order and set overall Workflow Status PARTIAL if any verified item is published.

**P1 Clause TH-CL-012 — Bounded batch and complete partial ledger.** The preceding
item-budget admission, ordered omission, and complete coverage-ledger rules are the
normative closure clause for audit item TH-012.

### Framework prerequisite

**P1 Clause TH-CL-005 — Current test-setup authority.**

Require tests/ plus the exact layout, validator, and execution manifests to exist and
validate the supplied test-setup receipt schema/content hash. Re-hash every dependency
named by that receipt and require `Audit Coverage: COMPLETE`, `Static Validation:
PASS`, `Verification Level: CI_VERIFIED`, `Determinism Status: VERIFIED`, `Receipt
Freshness: CURRENT`, `Setup Status: VERIFIED`, and `Gate Eligible: YES` for the same
candidate/build and current bytes. A missing, stale, invalid, partial, unverified, or
unreadable setup authority is BLOCKED with zero project writes.

Resolve helper/consumer/contract/evidence routes only from the current layout-manifest
IDs. Resolve adapter and parser argv only from the current validator/execution
manifests and dependency lock. Never synthesize an engine command, test route,
framework adapter, or evidence path.

An unknown or unsupported engine, language, framework, adapter row, module/assembly,
or request/authority schema is `Input Status: INVALID`, Workflow Status INVALID, and
zero writes. A well-formed request whose declared current external prerequisite is
temporarily unavailable is BLOCKED/PARTIAL, not a guessed continuation.

**P1 Clause TH-CL-006 — Unsupported engine/language/framework stop.** The preceding
INVALID/zero-write branch and exact adapter routing are the normative closure clause
for audit item TH-006.

Enumerate every proposed source, consumer, contract, and evidence target before
generation. For each target, read in full every applicable AGENTS.md from project root
through its parent, including tests/AGENTS.md. Record selected, loaded, unreadable,
omitted, and superseded paths/hashes and the effective closest source for naming,
AAA, fixture, isolation, lifecycle, ownership, and engine rules. Conflicting or
unreadable applicable instructions make `Instruction Coverage: PARTIAL` and block the
affected item; do not copy a local pattern that violates instructions.

**P1 Clause TH-CL-007 — Complete closest-rule instruction chain.** The preceding
root-to-target AGENTS coverage and conflict rule are the normative closure clause for
audit item TH-007.

### Deterministic style sampling

**P1 Clause TH-CL-008 — Deterministic compliant style sampling.**

Use only explicit sample path/hash/kind rows from the request manifest. Resolve and
reject canonical duplicate paths, unreadable/hash-mismatched samples, or paths outside
the project. Parse every admitted sample with the pinned language validator, apply the
current instruction/coding-standard rules, and exclude violations before selection.

Selection is deterministic: group valid samples by kind in this order: fixture,
factory, assertion, adapter, test-double; sort each group by normalized case-folded
path then raw path; take the first item from each nonempty group until five are chosen;
if capacity remains, merge all unchosen valid samples and fill by the same path order.
Record selected and excluded samples with hashes and rule IDs. Do not backfill from an
invalid sample and do not learn semantics from samples. They are style hints only;
never reproduce nondeterminism, shared mutable state, missing teardown, opaque helpers,
generic naming, production API guesses, or other anti-patterns.

## Phase 2: Resolve real production contracts

**P1 Clause TH-CL-010 — REAL production API and requirement-owner join.**

For every REAL item:

1. Validate the production API snapshot schema/hash/tool identity, then re-hash its
   complete source closure, generated dependencies, runtime config, and accepted
   requirement sources.
2. Require every requirement ID to resolve to an accepted/current owner artifact.
   GDD text supplies the expected contract only; it never proves implementation.
3. Resolve the declared type/module/symbol, normalized signature, constructor or
   dependency-injection seam, direct dependency edges, and runtime-config accessor
   from the actual compiled production graph.
4. Verify the type and dependency closure can be imported by the declared test
   module/assembly without adding production or module configuration.
5. Require generated factory/fixture code to instantiate that real production type or its real subclass/component through the declared API.
6. Require the helper consumer to call the exact declared real production
   method/event/property path and collect adapter-defined execution evidence binding
   the module/type/symbol signature and production binary/source hashes.
7. Inject actual production config only through the resolved production accessor or a
   hash-bound adapter around that accessor. Never duplicate a GDD number as a helper
   constant or new oracle.
8. If requirement, API snapshot, implementation graph, compiled symbol, or runtime
   config differs, set `Production Binding: CONFLICTING/STALE`, report the exact
   mismatch, and block the item instead of generating a fake implementation.

A bare Node, GameObject, UObject, dictionary, metadata bag, or invented class cannot stand in for a REAL SUT. Setting metadata fields such as health or attack does not demonstrate that production combat/player code ran.

For every ISOLATED_FAKE item:

- label the source header, contract manifest, validation receipt, and output as ISOLATED_FAKE;
- implement only the exact hash-bound production interface/protocol at an approved dependency seam;
- prohibit production-type, business-coverage, formula-oracle, and actual-system claims;
- require consumers to inject it into a separate real SUT;
- reject a fake that reproduces the behavior being tested or becomes an independent business oracle.

A fake may validate an interaction seam; it cannot satisfy AC coverage or substitute for a missing business test.

### Value and oracle provenance

**P1 Clause TH-CL-011 — Hash-bound value/oracle provenance.**

Classify every generated literal/default as `PRODUCTION_CONFIG`,
`REQUIREMENT_EXPECTED_ONLY`, or `TEST_LOCAL_NONBUSINESS`. A business-affecting value
may appear in executable helper code only as a call/injection through a verified
`PRODUCTION_CONFIG` accessor. `REQUIREMENT_EXPECTED_ONLY` belongs only in the consumer
expectation and retains accepted requirement ID/path/hash; it must not initialize the
SUT. `TEST_LOCAL_NONBUSINESS` must be semantically irrelevant to the business result.

Record each value provenance class, accessor or expectation symbol, source path/hash,
and owner in the helper artifact contract. Re-hash all sources before validation,
publish, and downstream consumption. Any change makes the candidate or published
contract STALE; stable IDs and unchanged literal text do not prove freshness.

## Phase 3: Design lifecycle-safe engine helpers

Every generated helper owns setup and teardown. Cleanup is automatic, idempotent, exception/failure-safe, and verified after every helper-only consumer.

### Godot 4

- Use the configured compiled/discovered Godot test adapter and actual project types.
- Validate a signal exists before connection.
- Use a framework signal spy or a generated typed adapter whose callable signature matches the reflected signal arity, including zero, one, and multiple arguments.
- Make capture one-shot when only one emission is expected; disconnect in teardown/finally even when the action or assertion fails.
- Track every instantiated Node, scene, Resource, timer, and connection. Remove/free owned nodes and await only adapter-defined deterministic frames.
- After teardown assert no owned node, signal connection, timer, or scene-tree child remains.

Do not emit a generic one-argument lambda for an arbitrary signal and do not leave a permanent connection.

### Unity

- Place helpers and consumers under the exact existing test assembly directory named by the request; require its current asmdef path/hash and assembly reference.
- Instantiate real MonoBehaviour/ScriptableObject types through declared production APIs.
- A fixture owns every GameObject, Component, ScriptableObject, native allocation, event subscription, and temporary asset it creates.
- TearDown or IDisposable cleanup runs in a finally-safe path and destroys/unsubscribes all owned resources.
- After teardown assert resource/object/subscription counts returned to the adapter baseline.

Never require each caller to remember DestroyImmediate.

### Unreal Engine

- Place headers/sources and consumers inside an existing project Tests module named by the request, for example Source/{Project}Tests/Public/Helpers and Source/{Project}Tests/Private.
- Require current .uproject/.uplugin, Tests Target/ModuleRules or Build.cs, dependency modules, include roots, and adapter hashes before generation.
- Never write an Unreal helper only to tests/helpers or claim a header is usable without a compiled Tests module route.
- Represent world ownership with an RAII fixture. Its constructor creates the isolated test world/context through the approved engine adapter; its destructor always destroys actors/world, clears delegates/timers, removes the exact FWorldContext, and releases roots.
- Disable copy, define safe move behavior only if needed, and assert no world/context/global delegate remains after scope exit.

Never return a bare UWorld pointer whose cleanup is left to the caller and never leak or reuse uncontrolled GEngine world contexts.

## Phase 4: Generate traceable candidates and contracts

Each helper source header must contain machine-readable annotations:

~~~text
Helper Contract ID: {stable-helper-id}
Helper Contract Version: 2
Helper Kind: fixture | factory | assertion | adapter | test-double
SUT Mode: REAL | ISOLATED_FAKE
Stable AC IDs: {ids-or-NONE}
Stable Test/Check IDs: {ids-or-NONE}
Requirement Sources: {paths + sha256 digests}
Production Symbols: {module/type/symbol + source digests}
Runtime Config Sources: {paths + sha256 digests}
Production API Snapshot SHA-256: sha256:{digest}
Test Setup Receipt SHA-256: sha256:{digest}
Layout/Engine/Validator/Execution SHA-256: {digests}
Applicable AGENTS Chain SHA-256: sha256:{digest}
Generated From Request SHA-256: sha256:{digest}
Business Coverage: NOT ESTABLISHED
~~~

Do not embed the helper source's own raw hash in itself. After candidate bytes are final, build a separate contract payload containing:

- stable helper identity/version/kind/SUT mode;
- annotations above;
- exact helper and consumer paths/raw-byte hashes;
- normalized exported symbol signatures;
- setup/teardown ownership and observable cleanup assertions;
- imported production symbols and hashes;
- production API snapshot/tool/source-closure hashes and compiled symbol evidence;
- test-setup receipt plus engine/layout/validator/execution/dependency hashes;
- per-literal value/oracle provenance class, accessor/expectation symbol, source hash,
  and owner;
- expected helper behavior and negative-control condition;
- engine/framework/adapter/module/assembly/config hashes.

Serialize the payload as UTF-8 JSON Canonicalization Scheme (RFC 8785) bytes, compute
Helper Contract SHA-256 over those exact bytes, and write the canonical payload plus
digest to tests/helpers/contracts/{request-id}.json. Consumers such as
test-evidence-review must re-hash the helper source, contract payload, test-setup
authorities, production API closure, runtime config, requirements, and applicable
instructions. Any mismatch is STALE.

Stable AC/test annotations declare intended traceability only. They do not prove coverage or failure sensitivity for a business test.

### Existing helpers

**P1 Clause TH-CL-009 — Safe CREATE/EXTEND conflict decision.**

For CREATE, require the target not to exist. For EXTEND:

1. verify the current raw-byte hash equals expected base-file hash;
2. parse using the engine-language AST or symbol parser from the adapter;
3. reject duplicate/conflicting exported symbols;
4. insert only declared symbols at the parser-defined location;
5. preserve every byte outside the authorized insertion span;
6. reparse and compare the symbol table.

If parsing is unavailable or the target changed, block the item. Never replace the file, ask the user to delete it, or use whole-file regeneration to preserve custom code.

If CREATE finds an existing target, or EXTEND finds a symbol/path ownership conflict,
do not skip, delete, rename, or choose automatically. Emit one decision packet with
two bounded options when both are safe: `EXTEND` the existing owner using its exact
base hash and declared insertion symbol, or `CREATE` at a new canonical layout-owned
path with a new ownership ID. Record effects and conflicts; require an amended signed
request manifest before continuing. If either option is unsafe, omit it rather than
presenting a false choice.

Build an ownership table before candidate generation. Every helper, consumer,
contract, receipt, log, and temporary staging path has one stable owner ID, operation,
precondition (`ABSENT` for CREATE or exact SHA-256 for EXTEND), and authorized final
hash. Canonical path or symbol collisions block all involved items.

## Phase 5: Compile, discover, exercise, and prove cleanup

Validation occurs against an isolated staging tree containing the exact candidate
bytes before the project changeset preview. Revalidate the current test-setup receipt,
layout/engine/validator/execution manifests, adapter row, and dependency hashes before
each tool class. Execute only pinned argv arrays allowlisted by those manifests; never
synthesize shell commands. Apply the recorded working directory, environment-name
allowlist, timeout, output cap, parser, redaction, and process-tree cleanup rules.

Freeze request-declared seed, order, locale, timezone, environment-name set,
parallelism, cleanup baseline, timeout, and semantic-projection schema before the
first run. Do not add retries or change controls after observing results. Run each
baseline consumer twice in clean fixtures around the negative control and compare its
declared semantic projection: discovered stable ID, production-path binding, outcome,
observable, and cleanup baseline. Exclude timestamps/durations from equality but keep
them in evidence. A projection mismatch is `Determinism Status: UNSTABLE`.

For each item require all of:

1. Parse/compile success in the actual engine test module or assembly.
2. Test discovery finds the exact canonical helper-only consumer test.
3. Baseline consumer PASS before and after the negative control with equal semantic
   projections.
4. REAL mode execution receipt names the real production module/type/symbol and demonstrates the declared production path executed.
5. Negative-control run produces the expected FAIL for the same helper source/contract, stable IDs, production/requirement hashes, and controlled failure condition.
6. Teardown runs after both pass and fail paths.
7. Post-teardown cleanup assertions pass with no leaked nodes, objects, subscriptions, worlds, contexts, delegates, timers, roots, or temporary assets.
8. Logs are complete, untruncated, parsed, redacted, and hash-recorded.
9. Every compile/discovery/run/cleanup receipt uses
   `cgs-test-helper-validation-receipt/v2` and binds current test-setup, manifest,
   adapter, production API, requirement, source, argv, control, result, log, and
   parser hashes.

The negative control validates failure sensitivity of the helper contract/consumer only. It is not the regression-suite failure-sensitivity receipt for a business test and cannot make a stable AC VERIFIED.

Classify each candidate:

- VERIFIED CANDIDATE: every check above passes;
- INVALID CANDIDATE: a conclusive current compile FAIL, complete zero discovery,
  baseline/negative-control FAIL, real-SUT mismatch, deterministic mismatch, cleanup
  FAIL, receipt INVALID, or hash STALE result proves the candidate invalid;
- PARTIAL VALIDATION: compiler/runner/parser unavailable or unsupported, timeout,
  killed/incomplete process, partial discovery, truncated output, missing receipt
  field, unreadable evidence, or incomplete validator coverage prevents a conclusion;
- OMITTED: outside approved budget or explicitly omitted by policy;
- BLOCKED ITEM: prerequisite, conflict, source mismatch, or safe extension is unavailable.

Do not publish invalid or partially validated candidates as usable helpers. If no
candidate is verified, return INVALID when all attempted results are conclusive
invalid, otherwise Workflow Status BLOCKED with partial axes and zero helper/contract
writes. In a mixed batch,
preview and publish only verified candidates; list every invalid, partially validated,
omitted, blocked, and unprocessed item with stable reason IDs, producing overall
PARTIAL after verified persistence.

## Phase 6: Preview, persist transactionally, and verify

For verified candidates, preview the complete changeset:

- every CREATE helper and helper-only consumer;
- every exact EXTEND insertion and previewed base hash;
- contract manifest;
- immutable validation receipt and logs under the request/run evidence directory;
- explicit non-writes, including production code, business tests, QA plan, regression manifest, framework/module configuration, and session state.

The validation receipt must bind request/helper/contract/ownership IDs,
test-setup/layout/engine/validator/execution/dependency paths/hashes,
helper/consumer/source hashes, stable annotations, production API closure/
requirement/config hashes, engine/framework/adapter/module hashes, exact argv,
runner/parser versions and hashes, deterministic controls/projection hashes,
timestamps, exit codes, compile/discovery results, both baseline results,
negative-control result, real-SUT path evidence, cleanup assertions, logs/hashes,
coverage ledger, every independent status axis, and validation status.

Immediately before applying, re-hash every authority/input and every ownership-table
path. Require CREATE paths ABSENT and EXTEND paths at exact preimage hashes. Any
authority drift or path mismatch sets `Ownership/CAS: CONFLICT`, aborts the complete
publication batch before its first write, and preserves external work.

Stage all owned bytes with a transaction ID using the approved same-filesystem
publication adapter. Verify staged hashes, then publish the authorized changeset
all-or-none. If the environment cannot provide the adapter's declared atomicity and
recovery protocol, use `Ownership/CAS: PARTIAL` and publish nothing. Re-read every
file, compare with approved bytes, reparse helper symbols, and verify final hashes
equal the validated candidate hashes.

If publication is interrupted, stop writes, record every current path/hash as
PREIMAGE, POSTIMAGE, or DIVERGED, and persist an immutable partial-application receipt
outside target paths. Never blindly restore a saved file. Recovery is a separate
authorized three-way/CAS operation that preserves diverged current bytes.

If persistence or read-back fails, report BLOCKED and do not claim a usable helper. Never return VERIFIED merely because source files were written.

## Phase 7: Report result and consumer contract

Report:

- request manifest path/hash, request ID, run ID, and scope budget;
- engine/language/framework/adapter/module/assembly identities and hashes;
- QA-plan effective state and stable annotations;
- per-item operation, target, SUT mode, production symbols, helper source hash, contract hash, validation receipt/log hashes, and candidate status;
- verified, invalid, blocked, and omitted counts;
- partially validated and unprocessed counts plus the full ordered coverage ledger;
- test-setup receipt and layout/engine/validator/execution/dependency freshness;
- Instruction Coverage, Production Binding, Compile, Discovery, Determinism,
  Ownership/CAS, and Receipt Freshness axes;
- Workflow Status;
- Business Coverage: NOT ESTABLISHED;
- exact written/unchanged/declined/failed operation ledger.

Only VERIFIED or PARTIAL may describe published helpers as usable, and only for helper infrastructure. INVALID and BLOCKED say no usable helper was published.

Downstream test-evidence-review may count a helper assertion only after reading and re-hashing the exact helper source and contract and proving its observable semantics. Regression-suite must still require a separate stable business-test mapping, current requirement/test hashes, its own failure-sensitivity receipt, and a current execution receipt. Never recommend test-helpers as a substitute for a missing regression/business test.

Recommend the exact prerequisite, source owner, contract mismatch, or cleanup/validation failure to address. Do not auto-run another workflow or claim that any business test was scaffolded.

## P1 remediation trace

This trace is structural evidence only; it adds no behavior beyond the cited
clauses. Every P1 audit ID maps to one concrete SKILL clause, one dedicated spec
case, and explicit assertion IDs—never to a prose line range.

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
