# Skill Test Spec: $test-setup

## Skill Summary

`$test-setup` semantically audits or scaffolds engine-specific test infrastructure,
creates a real deterministic canary plus a setup-only failure fixture, emits an
argv-array execution manifest, and verifies discovery and exit-code sensitivity.
File existence is never enough. `Verdict: COMPLETE` requires a trusted build-bound CI
receipt for the same candidate, test-manifest, runner, parser, workflow, log, and
test-source hashes.

The canonical durable result is
`production/qa/evidence/test-setup/<candidate-id>/<setup-run-id>/report.md`.
No director gate applies.

---

## Static Assertions

- [ ] YAML frontmatter contains only `name` and a non-empty `description`; name matches the skill directory
- [ ] Has at least two phase headings
- [ ] Defines audit, scaffold, verify, and repair modes plus invalid-input behavior
- [ ] Reads the full applicable AGENTS chain before planning tests
- [ ] Uses test function naming from the closest `tests/AGENTS.md`
- [ ] Routes manual visual/UI evidence to `production/qa/evidence/`
- [ ] Creates unit, integration, performance, and playtest layout records
- [ ] Creates a deterministic pass canary and a setup-only intentional failure fixture
- [ ] `tests/test-execution-manifest.json` uses argv arrays, environment allowlists, timeout/output caps, parser rules, cleanup, log fields, and trusted-CI rules
- [ ] Automated receipts bind candidate/build/test-manifest/test-source/runner/argv/log/parser details
- [ ] COMPLETE requires nonzero discovery, pass canary exit zero, failure probe nonzero, isolated post-probe pass, and trusted CI receipt
- [ ] Unity requires both valid `.asmdef` files and nonzero discovery
- [ ] Godot completion/exit propagation and Unreal project/runner identity are version-resolved
- [ ] Active CI contains no unresolved placeholders or major-only third-party action tags
- [ ] Missing plugin/license/self-hosted runner/secret/CI receipt yields SETUP_PENDING
- [ ] Existing infrastructure is parsed semantically and repair is ID-keyed, not a full overwrite
- [ ] No director gate applies

---

## Case 1: Scaffold alone is not COMPLETE

**Fixture:**

- Engine/project/version identity is valid
- Approved adapter templates and dependencies are available
- No candidate manifest is supplied, so no build-bound execution can run
- The bounded change authorizes safe scaffold files

**Input:** `$test-setup scaffold --setup-run-id setup-001`

**Expected behavior:**

1. The skill creates the planned layout, required engine files, real canary sources,
   and valid execution manifest.
2. It performs static validation but cannot create build-bound canary receipts.
3. It returns `Setup Status: SCAFFOLDED`, `Verdict: SCAFFOLDED`,
   `Gate Eligible: NO`.

**Assertions:**

- [ ] No COMPLETE, VERIFIED, or CI-wired claim appears
- [ ] Changed-path list matches actual files
- [ ] Manual evidence route is not under tests/evidence

---

## Case 2: Pass and failure canaries prove runner sensitivity

**Fixture:**

- Candidate manifest/build/test manifest and all hashes verify
- Framework/plugin and runner are installed at pinned versions
- Pass and failure stable IDs each resolve to one discovered test
- Execution is authorized

**Input:** `$test-setup verify --candidate production/builds/candidate-17.json --setup-run-id setup-002`

**Expected behavior:**

1. Pass canary is discovered once, passes, and runner exits zero.
2. Intentional failure fixture is discovered once, fails, and runner exits with the
   declared nonzero test-failure code.
3. Pass canary reruns with the failure fixture excluded and passes.
4. All three logs and structured receipts are hash-bound.

**Assertions:**

- [ ] Failure-probe exit zero yields `Failure Sensitivity: NOT_SENSITIVE`
- [ ] Timeout/runner crash/parse failure cannot count as the expected nonzero failure
- [ ] Every receipt contains candidate/build/source/runner/argv/time/count/log/parser/test-source fields
- [ ] Failure fixture is excluded from ordinary suite selection

---

## Case 3: Deterministic example test satisfies gate prerequisite only after execution

**Fixture:**

- The pass canary source exists and follows
  `test_[system]_[scenario]_[expected_result]`
- Its stable ID/source hash appears in the execution manifest
- Current build-bound pass receipt verifies
- Failure sensitivity and CI receipt also verify

**Expected behavior:**

- The example-test prerequisite is verified, not inferred from a README or path.
- Discovery count is greater than zero.
- The exact setup receipt may be gate eligible.

**Assertions:**

- [ ] Source, test ID, AC ID, function identity, and raw hash are recorded
- [ ] A seed file without a current pass receipt is only SCAFFOLDED/AWAITING verification
- [ ] A gate must consume exact setup-receipt and candidate hashes

---

## Case 4: Godot runner must wait and propagate failure

**Variants:**

- A: Approved version-matched official entrypoint/wrapper waits for completion and
  maps pass to zero and failure to nonzero
- B: A runner starts tests and immediately quits zero
- C: Required GdUnit4/addon bytes are absent

**Expected behavior:**

- Only A can advance through canary verification.
- B is `INCOMPLETE` with `Failure Sensitivity: NOT_SENSITIVE` or invalid completion.
- C is `SETUP_PENDING`, not a wired framework.

**Assertions:**

- [ ] Completion signal and failure count are parsed
- [ ] Timeout terminates the runner process tree
- [ ] No fallback runner command is synthesized

---

## Case 5: Unity creates valid assemblies and proves discovery

**Fixture:**

- Unity version and project assemblies are known
- Pinned Unity Test Framework is installed
- Both asmdef paths are initially absent

**Expected behavior:**

- Skill creates valid JSON at `tests/EditMode/EditModeTests.asmdef` and
  `tests/PlayMode/PlayModeTests.asmdef`.
- Exact project assembly references and test-assembly optional references validate.
- Compilation succeeds and pass canary discovery count is greater than zero.

**Assertions:**

- [ ] README text alone cannot satisfy asmdef requirement
- [ ] Missing/unresolved assembly reference yields INCOMPLETE
- [ ] Unity license/CI receipt absence yields SETUP_PENDING even after local pass

---

## Case 6: Unresolved active CI never becomes COMPLETE

**Variants:**

- Godot engine version or addon dependency is unresolved
- Unity license-secret presence is unverified
- Unreal project name, editor path, namespace, or self-hosted runner is unresolved
- Third-party actions use major tags instead of approved immutable SHAs

**Expected behavior:**

- No unresolved active `cgs-tests` job is created or described as wired.
- Every missing prerequisite is listed.
- `CI Status: SETUP_PENDING` or `INVALID`, `Gate Eligible: NO`.

**Assertions:**

- [ ] Template sentinels and unresolved project values block activation
- [ ] External license/runner provisioning is not automated
- [ ] Static YAML validity alone never means CI VERIFIED

---

## Case 7: Existing paths with wrong semantics do not early-exit

**Fixture:**

- `tests/` and `.github/workflows/tests.yml` exist
- Workflow job invokes a different runner string and has no receipt/log upload
- Failure fixture is missing
- No trusted CI receipt exists

**Input:** `$test-setup audit --candidate production/builds/candidate-17.json`

**Expected behavior:**

- Skill parses files and reports exact semantic gaps.
- It does not say configuration is verified.
- Audit performs no write.

**Assertions:**

- [ ] Existing directory/workflow presence is insufficient
- [ ] Setup status is INCOMPLETE or SETUP_PENDING
- [ ] Repair proposal, if requested separately, is keyed to managed IDs

---

## Case 8: Repair preserves unmanaged workflow content

**Fixture:**

- Workflow contains managed job `cgs-tests` plus human jobs `lint` and `package`
- Managed job has stale manifest hash and action SHA
- User authorizes the exact repair patch

**Expected behavior:**

- Only managed fields under `cgs-tests` change.
- Human jobs and unrelated test sources remain byte/logically preserved.
- Before/after hashes and exact diff are recorded.

**Assertions:**

- [ ] Legacy `force` behaves like keyed repair, not regeneration
- [ ] No whole-workflow/tree overwrite occurs
- [ ] A changed test manifest invalidates prior execution/CI receipts

---

## Case 9: Trusted CI receipt must match every execution binding

**Fixture:**

- Local static/discovery/pass/failure checks all verify
- Active workflow is semantically valid
- Supplied CI receipt has one variant mismatch: prior build, prior test-manifest
  hash, changed canary source, different argv, truncated log, untrusted issuer, old
  workflow hash, or failure-probe exit zero

**Expected behavior:**

- Each mismatch yields `CI Status: INVALID`, `Setup Status: INCOMPLETE`,
  `Gate Eligible: NO`.
- No CI-wired or COMPLETE claim appears.

**Assertions:**

- [ ] Receipt binds candidate/build/test sources/runner/parser/workflow/action SHA/log/per-test results
- [ ] Dates or newest-file selection cannot establish currentness
- [ ] Remote artifact unavailability is not PASS

---

## Case 10: Fully verified setup may return COMPLETE

**Fixture:**

- All scaffold semantics and dependency hashes pass
- Candidate/build/test sources are current
- Static validation and discovery pass
- Baseline pass, intentional failure, and isolated post-probe pass receipts verify
- Active CI job is placeholder-free and pinned
- Trusted CI receipt proves the same sequence and bindings
- Durable setup report write and read-back succeed

**Expected behavior:**

- `Setup Status: VERIFIED`
- `CI Status: VERIFIED`
- `Verdict: COMPLETE`
- `Gate Eligible: YES`

**Assertions:**

- [ ] Setup report header contains all required machine-readable fields
- [ ] Completion receipt lists every source/config/log/receipt hash
- [ ] COMPLETE is withheld if persistence or any revalidation fails
- [ ] No downstream workflow is invoked automatically

---

## Director Gate Checks

None. `$test-setup` is an infrastructure verification utility.

## Protocol Compliance

- [ ] Bounded authorization covers exact writes and allowed execution argv arrays
- [ ] Multi-file changes publish all-or-none
- [ ] Runner execution never uses shell interpolation or arbitrary fallback commands
- [ ] Secrets are allowlisted by name and values are excluded/redacted
- [ ] Timeout kills the full process tree and incomplete evidence never passes
- [ ] Catalog and workflow guide are not modified by this workflow

## Coverage Notes

The cases close all four P0 failures: missing executed example test, unreliable
Godot completion/exit status, absent Unity asmdefs, and unresolved CI placeholders or
prerequisites falsely described as complete. They also encode the staged
smoke-check/regression-suite/test-evidence-review execution-manifest and receipt
bindings for candidate, build, test source, runner, timeout, log, parser, and CI
currentness.
