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

Also report Business Coverage: NOT ESTABLISHED for every outcome. A helper validation receipt proves only the helper contract. It never proves a business AC is covered, that a regression test exists, or that a release test passed.

## Phase 1: Validate framework, engine, instructions, and scope

Resolve the supplied literal manifest path and real path. Reject symlinks escaping the project root, malformed syntax, duplicate keys, unsupported schema, unsafe slugs, dot segments, and paths outside the project root. Read raw bytes once and compute SHA-256 over exact bytes.

Require Artifact Type: test-helper-request, Schema Version: 1 and:

- unique request ID and run ID, neither a date alone;
- exact engine, engine version, language, and test framework;
- exact test-framework manifest path/hash and current discovery receipt path/hash;
- exact engine-adapter path/hash containing compile, discovery, consumer-run, timeout, output-cap, cleanup, and parser rules;
- exact QA-plan path/hash and effective CURRENT source snapshot when stable AC/test IDs are declared;
- ordered helper items;
- batch limits: maximum items, files, and candidate bytes;
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

Reject duplicate helper IDs, duplicate output paths, unmapped stable IDs, noncanonical slugs, invalid operations, or scope above the declared limits. Preserve an ordered omitted list; never silently truncate a batch.

### Framework prerequisite

Require tests/ and the test-framework manifest to exist. Validate the framework discovery receipt against the current engine/framework/config hashes. Unknown or mismatched engine, language, framework, adapter, module, or receipt is BLOCKED with zero writes.

Read in full every applicable AGENTS.md from the project root through each target test directory, including tests/AGENTS.md. Hash and record the exact instruction chain. Conflicting instructions block the affected item; do not copy a local pattern that violates the applicable instructions.

### Deterministic style sampling

Use only explicit sample paths from the request manifest. Sort normalized paths and select at most five using stable kind coverage in this order: fixture, factory, assertion, adapter, test-double, then lexical path. Treat samples as style hints only. Record violations and do not reproduce nondeterminism, shared mutable state, missing teardown, opaque helpers, generic naming, or other anti-patterns.

## Phase 2: Resolve real production contracts

For every REAL item:

1. Read and hash the exact production sources, generated code dependencies, runtime config, and requirement sources from the manifest.
2. Resolve the declared type/module/symbol and constructor or dependency-injection seam.
3. Verify the type can be imported by the declared test module/assembly.
4. Require generated factory/fixture code to instantiate that real production type or its real subclass/component through the declared API.
5. Require the helper consumer to call at least one declared real production method/event/property path and observe the QA-plan expected result.
6. Inject the actual production config or a hash-bound config adapter. Never duplicate a GDD number as a new oracle.
7. If the requirement and implementation differ, report the mismatch and block the item instead of generating a fake implementation of the requirement.

A bare Node, GameObject, UObject, dictionary, metadata bag, or invented class cannot stand in for a REAL SUT. Setting metadata fields such as health or attack does not demonstrate that production combat/player code ran.

For every ISOLATED_FAKE item:

- label the source header, contract manifest, validation receipt, and output as ISOLATED_FAKE;
- implement only the exact hash-bound production interface/protocol at an approved dependency seam;
- prohibit production-type, business-coverage, formula-oracle, and actual-system claims;
- require consumers to inject it into a separate real SUT;
- reject a fake that reproduces the behavior being tested or becomes an independent business oracle.

A fake may validate an interaction seam; it cannot satisfy AC coverage or substitute for a missing business test.

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
Helper Contract Version: 1
Helper Kind: fixture | factory | assertion | adapter | test-double
SUT Mode: REAL | ISOLATED_FAKE
Stable AC IDs: {ids-or-NONE}
Stable Test/Check IDs: {ids-or-NONE}
Requirement Sources: {paths + sha256 digests}
Production Symbols: {module/type/symbol + source digests}
Runtime Config Sources: {paths + sha256 digests}
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
- expected helper behavior and negative-control condition;
- engine/framework/adapter/module/assembly/config hashes.

Serialize the payload as UTF-8 JSON Canonicalization Scheme (RFC 8785) bytes, compute Helper Contract SHA-256 over those exact bytes, and write the canonical payload plus digest to tests/helpers/contracts/{request-id}.json. Consumers such as test-evidence-review must re-hash the helper source, contract payload, production sources, requirements, and applicable instructions. Any mismatch is STALE.

Stable AC/test annotations declare intended traceability only. They do not prove coverage or failure sensitivity for a business test.

### Existing helpers

For CREATE, require the target not to exist. For EXTEND:

1. verify the current raw-byte hash equals expected base-file hash;
2. parse using the engine-language AST or symbol parser from the adapter;
3. reject duplicate/conflicting exported symbols;
4. insert only declared symbols at the parser-defined location;
5. preserve every byte outside the authorized insertion span;
6. reparse and compare the symbol table.

If parsing is unavailable or the target changed, block the item. Never replace the file, ask the user to delete it, or use whole-file regeneration to preserve custom code.

## Phase 5: Compile, discover, exercise, and prove cleanup

Validation occurs against an isolated staging tree containing the exact candidate bytes before the project changeset preview. Execute only argv arrays allowlisted by the verified engine adapter; never synthesize shell commands. Apply its working directory, environment allowlist, timeout, output cap, parser, and process-tree cleanup rules.

For each item require all of:

1. Parse/compile success in the actual engine test module or assembly.
2. Test discovery finds the exact canonical helper-only consumer test.
3. Baseline consumer PASS.
4. REAL mode execution receipt names the real production module/type/symbol and demonstrates the declared production path executed.
5. Negative-control run produces the expected FAIL for the same helper source/contract, stable IDs, production/requirement hashes, and controlled failure condition.
6. Teardown runs after both pass and fail paths.
7. Post-teardown cleanup assertions pass with no leaked nodes, objects, subscriptions, worlds, contexts, delegates, timers, roots, or temporary assets.
8. Logs are complete, untruncated, parsed, redacted, and hash-recorded.

The negative control validates failure sensitivity of the helper contract/consumer only. It is not the regression-suite failure-sensitivity receipt for a business test and cannot make a stable AC VERIFIED.

Classify each candidate:

- VERIFIED CANDIDATE: every check above passes;
- INVALID CANDIDATE: compile, discovery, baseline, negative-control, real-SUT path, cleanup, receipt, or hash check fails;
- OMITTED: outside approved budget or explicitly omitted by policy;
- BLOCKED ITEM: prerequisite, conflict, source mismatch, or safe extension is unavailable.

Do not publish invalid candidates as usable helpers. If no candidate is verified, return INVALID or BLOCKED with zero helper/contract writes. In a mixed batch, preview and publish only verified candidates; list every invalid, omitted, and blocked item, producing overall PARTIAL after verified persistence.

## Phase 6: Preview, persist transactionally, and verify

For verified candidates, preview the complete changeset:

- every CREATE helper and helper-only consumer;
- every exact EXTEND insertion and previewed base hash;
- contract manifest;
- immutable validation receipt and logs under the request/run evidence directory;
- explicit non-writes, including production code, business tests, QA plan, regression manifest, framework/module configuration, and session state.

The validation receipt must bind request/helper/contract IDs, helper/consumer/source hashes, stable annotations, production/requirement/config hashes, engine/framework/adapter/module hashes, exact argv, runner/version, timestamps, exit codes, discovery result, baseline result, negative-control result, real-SUT path evidence, cleanup assertions, logs/hashes, and validation status.

Immediately before applying, re-hash every input and EXTEND base. Abort on change. Stage all owned bytes and publish the authorized changeset all-or-none. Re-read every file, compare with approved bytes, reparse helper symbols, and verify the final hashes equal the validated candidate hashes.

If persistence or read-back fails, report BLOCKED and do not claim a usable helper. Never return VERIFIED merely because source files were written.

## Phase 7: Report result and consumer contract

Report:

- request manifest path/hash, request ID, run ID, and scope budget;
- engine/language/framework/adapter/module/assembly identities and hashes;
- QA-plan effective state and stable annotations;
- per-item operation, target, SUT mode, production symbols, helper source hash, contract hash, validation receipt/log hashes, and candidate status;
- verified, invalid, blocked, and omitted counts;
- Workflow Status;
- Business Coverage: NOT ESTABLISHED;
- exact written/unchanged/declined/failed operation ledger.

Only VERIFIED or PARTIAL may describe published helpers as usable, and only for helper infrastructure. INVALID and BLOCKED say no usable helper was published.

Downstream test-evidence-review may count a helper assertion only after reading and re-hashing the exact helper source and contract and proving its observable semantics. Regression-suite must still require a separate stable business-test mapping, current requirement/test hashes, its own failure-sensitivity receipt, and a current execution receipt. Never recommend test-helpers as a substitute for a missing regression/business test.

Recommend the exact prerequisite, source owner, contract mismatch, or cleanup/validation failure to address. Do not auto-run another workflow or claim that any business test was scaffolded.
