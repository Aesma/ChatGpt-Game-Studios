---
name: test-setup
description: "Scaffolds and verifies engine-specific test infrastructure, deterministic canaries, argv-based execution manifests, and build-bound CI receipts without treating file existence as a working test system."
---

# Test Setup

Invoke one mode:

- `$test-setup audit [--candidate <candidate-manifest>]`
- `$test-setup scaffold [--candidate <candidate-manifest>] --setup-run-id <run-id> [--ci-receipt <path>]`
- `$test-setup verify --candidate <candidate-manifest> --setup-run-id <run-id> [--ci-receipt <path>]`
- `$test-setup repair --candidate <candidate-manifest> --setup-run-id <run-id> [--ci-receipt <path>]`
- Legacy `$test-setup force` is an alias for `repair`; it never authorizes bulk overwrite.

No director gate applies.

An explicit bounded request authorizes its in-scope files and execution. Otherwise,
before the first file change or test process, present one complete changeset and
execution plan, including exact paths and allowed argv arrays, and obtain one
approval. Do not re-prompt within that boundary. A materially expanded change,
external secret/runner configuration, or destructive operation requires new
authorization.

## Verification states

Report these fields independently:

| Field | Allowed values |
|---|---|
| `Scaffold Status` | `ABSENT`, `CREATED`, `EXISTING`, `PATCHED`, `INVALID` |
| `Static Validation` | `PASS`, `FAIL`, `NOT_RUN` |
| `Discovery Status` | `VERIFIED`, `ZERO_TESTS`, `INCOMPLETE`, `NOT_RUN` |
| `Pass Canary Status` | `PASS`, `FAIL`, `TIMEOUT`, `INFRA_ERROR`, `INVALID_RECEIPT`, `NOT_RUN` |
| `Failure Sensitivity` | `VERIFIED`, `NOT_SENSITIVE`, `TIMEOUT`, `INFRA_ERROR`, `INVALID_RECEIPT`, `NOT_RUN` |
| `CI Status` | `VERIFIED`, `STATIC_VALIDATED`, `SETUP_PENDING`, `INVALID`, `NOT_CONFIGURED` |
| `Setup Status` | `VERIFIED`, `SETUP_PENDING`, `SCAFFOLDED`, `INCOMPLETE`, `BLOCKED`, `ERROR` |
| `Verdict` | `COMPLETE`, `SETUP_PENDING`, `SCAFFOLDED`, `INCOMPLETE`, `BLOCKED`, `ERROR` |
| `Gate Eligible` | `YES`, `NO` |

`Verdict: COMPLETE`, `Setup Status: VERIFIED`, and `Gate Eligible: YES` are allowed
only when static validation, nonzero discovery, the passing canary, failure
sensitivity, and trusted CI execution all verify for the same current
candidate/build/test-manifest bytes. File or directory existence never proves a
state.

## Canonical setup receipt

A durable setup result, when authorized, lives only at:

`production/qa/evidence/test-setup/<candidate-id>/<setup-run-id>/report.md`

The same immutable run directory owns pass/failure logs and automated receipts.
A run ID must be a stable slug or UUID, not a date alone. Reject path separators,
dot segments, symlink escapes, or an existing run directory. Never select or
overwrite evidence by modification time.

A conversation summary or a report with any missing/hash-mismatched referenced
artifact is not gate evidence.

## Phase 0: Validate inputs and trust boundary

Accept exactly one mode and documented options. Resolve literal/real paths inside the
project root. Reject missing files, directories where a file is required, symlink
escapes, unsupported engine aliases, duplicate conflicting options, unsafe IDs, and
malformed hashes.

Before any scaffold plan, read all applicable instructions from repository root down
to every target directory, including the closest `tests/AGENTS.md`. The closest rule
wins. Record each instruction file path and raw-byte SHA-256 in the setup manifest.
For the current repository, generated test functions must follow
`test_[system]_[scenario]_[expected_result]`, include clear Arrange/Act/Assert, remain
deterministic and isolated, and clean up integration state.

Manual visual/UI evidence belongs under `production/qa/evidence/`, never
`tests/evidence/`.

## Phase 1: Resolve engine, language, project, and repository policy

Require agreement among:

- `.codex/docs/technical-preferences.md`;
- `docs/engine-reference/<engine>/VERSION.md`;
- the actual project descriptor (`project.godot`, Unity project/package metadata, or
  exactly one `.uproject`);
- configured language/runtime and package/dependency manifests;
- any existing runner/test-framework configuration.

Normalize documented aliases, but never guess an engine. Verify exact engine version,
project root, project name, language, test-framework version, executable/runner
compatibility, and project assembly/module identity. A missing value, placeholder,
multiple project roots, or conflict is `BLOCKED`.

Resolve the repository's trunk/default branch from explicit repository policy or a
verifiable VCS remote/default-branch reference. Do not hard-code `main`. An ambiguous
branch makes active CI generation `SETUP_PENDING`.

Require a project-approved immutable dependency manifest such as
`tests/dependencies.lock.json`. It must bind each test framework, parser, launcher,
and third-party CI action to source, exact version, immutable commit SHA/digest,
license/review status, installation path, and current raw hash. Major tags alone are
not immutable approval.

## Phase 2: Audit existing infrastructure semantically

Do not early-exit because paths exist. Read and parse every managed candidate in full:

- `tests/AGENTS.md` and applicable parent instructions;
- test layout/readmes and all engine-specific runner/config files;
- test-framework dependency installation and lock data;
- Unity `.asmdef`, Godot adapter/runner, or Unreal test module/target data;
- deterministic canary and setup-only failure fixture;
- `tests/test-execution-manifest.json`;
- parser/launcher files referenced by that manifest;
- `.github/workflows/tests.yml` job `cgs-tests`;
- any prior setup receipt explicitly supplied by path.

Classify each file `VALID`, `MISSING`, `MALFORMED`, `STALE`, `CONFLICTING`,
`UNMANAGED`, or `PLACEHOLDER`. Parse JSON/YAML/engine config structurally. Search
managed scalar values for unresolved template sentinels, but do not confuse real
GitHub expressions with placeholders.

For existing CI, validate the exact job ID, event/branch policy, least-privilege
permissions, timeout, dependency cache policy, immutable action SHAs, manifest hash,
runner invocation, log/receipt upload, secret references, and platform prerequisites.
Another workflow file or a job named “test” is not proof.

`repair` and legacy `force` produce an ID-keyed patch for managed fields only. Show
before/after hashes and preserve unmanaged jobs, comments where the parser permits,
human-authored tests, and unrelated files. Never replace the whole workflow or test
tree merely because repair was requested.

## Phase 3: Plan the canonical scaffold

Use this base layout, with nonempty README/manifest files so Git preserves it:

~~~text
tests/
  README.md
  dependencies.lock.json
  test-execution-manifest.json
  unit/
  integration/
  performance/
  playtest/
  setup-canary/
  <engine-specific runner/config/parser files>
~~~

`tests/playtest/` contains test adapters or fixtures only; full gameplay, visual
fidelity, and feel remain manual/playtest evidence. Do not create `tests/evidence/`
or treat `tests/smoke/` as the smoke gate's source of truth.

The README must derive naming, layout, evidence routes, engine/version, exact local
execution entrypoint, CI job ID, prerequisite states, and setup receipt semantics
from the same candidate manifest. It must not claim CI runs or blocks merges unless
a trusted CI receipt verifies that claim.

### Deterministic canaries

Create real, engine-discoverable source tests from an approved, version-matched
adapter template:

- `TST-SETUP-CANARY-PASS-001`: deterministic isolated example test, mapped to
  `AC-TEST-INFRA-CANARY`, with a function name matching the closest AGENTS rule;
- `TST-SETUP-CANARY-FAIL-001`: setup-only intentional failure fixture, mapped to
  `AC-TEST-INFRA-FAILURE-SENSITIVITY`, excluded from ordinary suite selection and
  invocable only by its explicit setup-verification argv entry.

The pass canary performs an exact deterministic assertion with no clock, random,
network, filesystem, or mutable external dependency. The failure fixture intentionally
produces one framework-level assertion failure; it is never counted as an ordinary
required passing test.

Record each stable ID, source path, function/case identity, mapped AC ID, and raw-byte
SHA-256 in the execution manifest. A README example or empty placeholder is not a
canary.

### Engine-required artifacts

Generate only from the approved adapter for the exact engine/framework version.

- Godot: create the required framework integration and, if repository standards
  require `tests/gdunit4_runner.gd`, copy a version-matched official/approved wrapper
  that blocks until suite completion and propagates the framework's exit code.
  Missing GdUnit4/addon bytes or an unverified async completion API is
  `SETUP_PENDING`, not a working runner.
- Unity: create both `tests/EditMode/EditModeTests.asmdef` and
  `tests/PlayMode/PlayModeTests.asmdef`, plus canary sources in the appropriate test
  assembly. Resolve exact project assembly references; include the test-assembly
  optional references required by the pinned Unity Test Framework. Parse both files
  as JSON, validate names/references/platform settings, compile, and require discovery
  count greater than zero. A README mentioning asmdefs is insufficient.
- Unreal: resolve the actual `.uproject` filename, project/module namespace, test
  target/module, Unreal Editor path, automation filter, and self-hosted runner labels.
  A literal project or namespace placeholder is invalid.

If any required engine file, plugin/package, project assembly/module, executable,
secret, or runner prerequisite cannot be verified, scaffold only the safe in-scope
files, report the exact prerequisite, and use `SETUP_PENDING`. Do not create or
describe an unresolved active CI job as wired.

## Phase 4: Generate the argv allowlist execution manifest

Create `tests/test-execution-manifest.json` as the single execution contract consumed
by staged `smoke-check` and build/CI runners. It must be valid JSON and contain:

- `artifact_type: test-execution-manifest`, `manifest_version`, and `hash_algorithm:
  sha256`;
- compatible engine, engine version, framework, runner name/version, runner/config
  paths and SHA-256;
- project-root-contained working directory;
- exact test-source entries with stable test ID, case identity, mapped AC/BUG IDs,
  source path, and raw-byte SHA-256;
- one argv array per stable automated test ID/scope, with executable and each argument
  as a separate array element and no shell command string, interpolation,
  redirection, pipeline, or command substitution;
- separate setup-only argv entries for pass-canary and failure-probe selection;
- environment-variable name allowlist, required/optional classification, redaction
  names, and an explicit prohibition on persisting secret values;
- timeout milliseconds, output-byte cap, and full runner-process-tree termination on
  timeout;
- exit-code mapping for pass, conclusive test failure, timeout, and infrastructure
  error;
- structured-result parser path, parser name/version/hash, output format/schema, and
  total/pass/fail/skip/discovery validation rules;
- canonical log path pattern, receipt path pattern, UTF-8/line-ending policy,
  truncation semantics, and SHA-256 rules;
- cleanup behavior and allowed created temporary paths;
- trusted CI issuer/job allowlist, signature/attestation verification, immutable
  action/dependency SHAs, and receipt-substitution rules;
- manifest-generation source hashes and generated-at timestamp.

The manifest itself is not a test result. Hash its exact raw bytes and require the
candidate manifest/build receipt to capture that path/hash before a consumer may
execute it.

Never synthesize an engine command at runtime or fall back to another runner. Execute
only a verified argv entry from the current manifest.

## Phase 5: Build or validate active CI without placeholders

Manage only job ID `cgs-tests` in `.github/workflows/tests.yml`.

An active job may be created or patched only when all values resolve and verify:

- exact trunk/PR branch policy and least-privilege permissions;
- pinned runner OS/self-hosted labels and job timeout;
- checked-out commit/candidate identity;
- installed framework/engine/dependencies matching immutable lock hashes;
- Unity license secret presence attestation, Unreal self-hosted editor/runner
  attestation, or Godot addon/runner prerequisites as applicable;
- exact execution-manifest path/hash and approved launcher;
- complete log and structured receipt upload even on failure;
- no unresolved project name, engine version, namespace, secret name, action version,
  path, or runner label.

Every third-party action uses an approved full immutable commit SHA, never only a
major tag. Validate YAML syntax/schema and the job semantically before activation.
If secrets, plugins, external runners, or immutable dependencies are unavailable,
leave the active job uncreated/unmodified, return `CI Status: SETUP_PENDING`, and
provide a precise prerequisite list. Do not automate license acquisition or external
runner provisioning.

`CI Status: STATIC_VALIDATED` means only the repository configuration parsed; it does
not mean the job executed. `CI Status: VERIFIED` requires the trusted build-bound
receipt in Phase 7.

## Phase 6: Execute pass and failure canaries safely

Execution requires an exact candidate manifest with the staged smoke-compatible
fields:

- `manifest_version` and `Artifact Type: build-candidate`;
- candidate ID, build ID, build artifact path/hash, source commit;
- engine name and exact runner-compatible version;
- platform/configuration target matrix and ISO-8601 creation time;
- test execution manifest path/hash;
- QA-plan path/hash when present for the candidate.

Re-hash the candidate, local build artifact or trusted remote build receipt, execution
manifest, runner/config, parser, and canary source bytes. Reject any mismatch.

For each canary, spawn only the verified argv array directly, from the verified
working directory. Never invoke a shell or evaluate a command string. Apply the
declared environment-name allowlist, timeout, output cap, redaction, and process-tree
cleanup. Capture stdout/stderr bytes, persist the exact log, and hash them.

Run in this order:

1. pass canary: it must be discovered exactly once, execute, report one pass and zero
   failures, and return exit code zero;
2. failure probe: it must be discovered exactly once, execute the intentional
   assertion failure, report at least one failure, and return a nonzero test-failure
   exit code distinct from timeout/infra errors;
3. pass canary again with the failure fixture excluded: it must still return the same
   conclusive pass and prove cleanup/isolation.

Any zero discovery, duplicate ID, unexpected skip, parse error, truncated log,
timeout, runner crash, missing completion signal, failure probe returning zero, or
post-probe contamination is `INCOMPLETE`. Never label it verified.

### Automated receipt schema

Each run produces an immutable structured receipt matching staged consumers:

- `Artifact Type: automated-test-receipt`, schema version, and receipt ID;
- candidate ID, build ID, build artifact SHA-256, source commit, and
  platform/configuration;
- candidate-manifest path/hash and test-manifest path/hash;
- QA-plan path/hash or explicit `NOT_APPLICABLE`, scope SHA-256, stable test IDs;
- test-source paths/hashes and mapped stable AC/BUG IDs;
- runner name/version and runner/config hash;
- exact argv array and working directory;
- start/end ISO-8601 timestamps, observer identity, exit code, and termination state;
- total/discovered/pass/fail/skip counts plus per-test stable ID/status/duration;
- log path/hash, output bytes, truncation flag;
- parser path/name/version/hash and parse status;
- receipt status: `PASS`, `FAIL`, `NOT_RUN`, `TIMEOUT`, `INFRA_ERROR`, or
  `INVALID_RECEIPT`;
- producer/run identity and receipt raw-byte SHA-256 or verifiable signature.

Only `PASS` and `FAIL` are conclusive. The pass canary needs `PASS`; the intentional
failure probe needs a valid `FAIL`. Timeout, infra error, invalid receipt, missing
completion, parse failure, and truncation are never proof.

## Phase 7: Verify CI with the same build-bound contract

A supplied CI receipt may establish `CI Status: VERIFIED` only when the trusted issuer
and job ID are allowlisted and its signature/attestation verifies. It must bind:

- exact candidate ID, build ID/artifact hash, source commit, platform/configuration;
- candidate-manifest and execution-manifest paths/hashes;
- current runner/config, parser, dependency-lock, workflow, and test-source hashes;
- exact stable IDs and argv arrays used for pass canary, failure probe, and post-probe
  pass;
- start/end, issuer, workflow/job/run IDs, attempt, immutable action SHAs, and exit
  codes;
- complete untruncated log paths/hashes;
- parser version/status, discovery/counts, and per-test results;
- baseline PASS, intentional nonzero FAIL, and isolated post-probe PASS;
- receipt raw-byte SHA-256 or trusted signature.

Re-hash every local referenced artifact. Reject another build, stale sources, old
workflow bytes, untrusted issuer, unverifiable remote logs, truncated output,
failure-probe exit zero, or missing per-test IDs as `CI Status: INVALID`, never
verified.

Without such a receipt, a semantically valid workflow remains
`CI Status: STATIC_VALIDATED` or `SETUP_PENDING`; never say CI/CD is wired up.

## Phase 8: Finalize the setup receipt and verdict

Before writing, re-hash all candidate, build, instruction, dependency, source,
runner, parser, manifest, workflow, log, and receipt inputs. If anything changed,
discard the proposed report and revalidate.

The setup report must include:

- artifact/schema/run identity and generation timestamp;
- exact candidate/build/platform/source-commit binding;
- engine/project/language/framework/runner/adapter/dependency versions and hashes;
- applicable AGENTS chain and effective naming/evidence rules;
- exact created, patched, unchanged, unmanaged, and rejected paths with hashes;
- static parse/schema/placeholder results;
- test manifest path/hash and every canary source stable ID/hash;
- discovery counts;
- pass, failure-probe, and post-probe receipt/log paths/hashes/statuses;
- CI workflow path/hash/status/prerequisites and CI receipt/signature;
- every verification-state field, gaps, and non-writes.

Use this machine-readable header:

~~~text
Artifact Type: test-setup-receipt
Schema Version: 1
Receipt ID: <setup-run-id>
Candidate ID: <candidate-id>
Build ID: <build-id>
Build Artifact SHA-256: sha256:<digest>
Source Commit: <commit>
Test Manifest Path: tests/test-execution-manifest.json
Test Manifest SHA-256: sha256:<digest>
Setup Status: <VERIFIED|SETUP_PENDING|SCAFFOLDED|INCOMPLETE|BLOCKED|ERROR>
CI Status: <VERIFIED|STATIC_VALIDATED|SETUP_PENDING|INVALID|NOT_CONFIGURED>
Pass Canary Status: <status>
Failure Sensitivity: <status>
Gate Eligible: <YES|NO>
Verdict: <COMPLETE|SETUP_PENDING|SCAFFOLDED|INCOMPLETE|BLOCKED|ERROR>
~~~

Derive the final result in strict order:

1. `ERROR` for write/read-back/internal-reference failure.
2. `BLOCKED` for unresolved engine/project identity or unauthorized required scope.
3. `INCOMPLETE` for invalid config, zero/incomplete discovery, nonpassing baseline,
   nonsensitive failure probe, timeout/infra/parse/truncation/hash failure.
4. `SCAFFOLDED` when safe files exist but execution did not run.
5. `SETUP_PENDING` when local static/discovery/canaries pass but any external
   plugin/package/secret/runner/active-CI/trusted-CI-receipt prerequisite remains.
6. `COMPLETE` only when all scaffold semantics, dependency hashes, static validation,
   discovery, pass/fail/post-probe canaries, active CI, and trusted CI receipt verify
   for the same current candidate/build bytes.

Only case 6 uses `Setup Status: VERIFIED` and `Gate Eligible: YES`.

If report persistence is authorized, stage its owned run-directory files, verify
internal references/hashes, publish all or none, re-read them, and display the setup
report SHA-256. A declined or failed persistence makes the durable setup receipt
unavailable and `Gate Eligible: NO`, without changing observed canary outcomes.

Do not claim files were created unless they appear in the verified changed-path list.
Do not invoke `$smoke-check`, `$regression-suite`, `$test-evidence-review`, or a gate.
Downstream consumers must receive exact receipt/candidate/test-manifest paths and
expected hashes and must revalidate them; no consumer may choose the newest receipt.
