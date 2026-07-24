---
name: test-setup
description: "Scaffolds and verifies engine-specific test infrastructure, deterministic canaries, argv-based execution manifests, and build-bound CI receipts without treating file existence as a working test system."
---

# Test Setup

Invoke one mode:

- `$test-setup audit [--candidate <candidate-manifest>] --engine-manifest <path> --repo-policy <path>`
- `$test-setup scaffold [--candidate <candidate-manifest>] --engine-manifest <path> --repo-policy <path> --setup-run-id <run-id> [--ci-receipt <path>]`
- `$test-setup verify --candidate <candidate-manifest> --engine-manifest <path> --repo-policy <path> --setup-run-id <run-id> [--ci-receipt <path>]`
- `$test-setup repair --candidate <candidate-manifest> --engine-manifest <path> --repo-policy <path> --setup-run-id <run-id> [--ci-receipt <path>]`
- Legacy `$test-setup force` is an alias for `repair`; it never authorizes bulk overwrite.

No director gate applies.

## Contract manifest

This normative contract is versioned independently from prose:

```yaml template
schema: cgs-test-setup-contract/v1
modes: [audit, scaffold, verify, repair]
required_authorities:
  engine_manifest: <owner-approved-path>
  repository_policy: <owner-approved-path>
  dependency_lock: tests/dependencies.lock.json
owned_outputs:
  layout_manifest: tests/test-layout-manifest.json
  validator_manifest: tests/test-setup-validator-manifest.json
  execution_manifest: tests/test-execution-manifest.json
  workflow_job: .github/workflows/tests.yml#jobs.cgs-tests
  run_root: production/qa/evidence/test-setup/<candidate-id>/<setup-run-id>/
never_writes:
  - root-or-nested-AGENTS.md
  - engine-manifest-or-repository-policy
  - project-descriptor-or-version-authority
  - production/qa/plans/
  - other-workflow-jobs
  - human-authored-tests
receipt_schema: cgs-test-setup-receipt/v2
hash_algorithm: sha256
```

`audit` is strictly read-only. The other modes may write only their authorized
owned paths. They never modify instruction authorities, engine/repository policy,
project descriptors, QA plans, gate rules, unrelated workflow jobs, or human tests.
No mode auto-invokes another skill, gate, commit, or publication.

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
| `Audit Coverage` | `COMPLETE`, `PARTIAL`, `NOT_RUN` |
| `Static Validation` | `PASS`, `FAIL`, `NOT_RUN` |
| `Discovery Status` | `VERIFIED`, `ZERO_TESTS`, `INCOMPLETE`, `NOT_RUN` |
| `Pass Canary Status` | `PASS`, `FAIL`, `TIMEOUT`, `INFRA_ERROR`, `INVALID_RECEIPT`, `NOT_RUN` |
| `Failure Sensitivity` | `VERIFIED`, `NOT_SENSITIVE`, `TIMEOUT`, `INFRA_ERROR`, `INVALID_RECEIPT`, `NOT_RUN` |
| `Determinism Status` | `VERIFIED`, `UNSTABLE`, `PARTIAL`, `NOT_RUN` |
| `Receipt Freshness` | `CURRENT`, `STALE`, `INVALID`, `UNVERIFIED`, `NOT_APPLICABLE` |
| `Verification Level` | `AUDITED`, `CREATED`, `STATIC_VALIDATED`, `DISCOVERY_VERIFIED`, `CANARY_PASS`, `FAILURE_SENSITIVE`, `CI_VERIFIED` |
| `CI Status` | `VERIFIED`, `STATIC_VALIDATED`, `SETUP_PENDING`, `INVALID`, `NOT_CONFIGURED` |
| `Setup Status` | `VERIFIED`, `SETUP_PENDING`, `SCAFFOLDED`, `INCOMPLETE`, `BLOCKED`, `ERROR` |
| `Verdict` | `COMPLETE`, `SETUP_PENDING`, `SCAFFOLDED`, `INCOMPLETE`, `BLOCKED`, `ERROR` |
| `Gate Eligible` | `YES`, `NO` |

`Verdict: COMPLETE`, `Setup Status: VERIFIED`, and `Gate Eligible: YES` are allowed
only when audit coverage is complete; static validation, nonzero discovery, the
passing canary, failure sensitivity, deterministic replay, dependency review, and
trusted CI execution all verify for the same current candidate/build/layout/
test-manifest bytes. File or directory existence never proves a state. Any unreadable,
omitted, timed-out, unavailable, unsupported, hash-mismatched, or unexecuted required
check is `PARTIAL` or `NOT_RUN`, never PASS, and forces `Gate Eligible: NO`.

## Canonical setup receipt

A durable setup result, when authorized, lives only at:

`production/qa/evidence/test-setup/<candidate-id>/<setup-run-id>/report.md`

The same immutable run directory owns `audit.json`, `repair-plan.json`,
`changed-files.json`, per-path backup blobs, exact diffs, pass/failure logs, and
automated receipts.
A run ID must be a stable slug or UUID, not a date alone. Reject path separators,
dot segments, symlink escapes, or an existing run directory. Never select or
overwrite evidence by modification time.

A conversation summary or a report with any missing/hash-mismatched referenced
artifact is not gate evidence. Every consumed receipt must declare its schema,
producer/tool version and hash, dependency path/hash set, raw receipt hash or trusted
signature, and freshness `CURRENT`. `STALE`, `INVALID`, `UNVERIFIED`, partial, or
unreadable receipts cannot advance the verification ladder.

## Phase 0: Validate inputs and trust boundary

Accept exactly one mode and documented options. Resolve literal/real paths inside the
project root. Reject missing files, directories where a file is required, symlink
escapes, unsupported engine aliases, duplicate conflicting options, unsafe IDs, and
malformed hashes.

Before any scaffold or repair plan, enumerate every proposed target first, then read
the complete applicable instruction chain from repository root to each target parent,
including the closest `tests/AGENTS.md`. Resolve precedence per target; the closest
rule wins. Record selected, loaded, unreadable, and omitted instruction paths, raw-byte
SHA-256, and the effective rule source for naming, evidence, isolation, cleanup, and
engine conventions. An unreadable or ambiguous applicable instruction makes
`Audit Coverage: PARTIAL`, prevents writes to its subtree, and forces
`Gate Eligible: NO`.

Derive generated test names from the effective closest rule. For the current
repository that rule requires `test_[system]_[scenario]_[expected_result]`, clear
Arrange/Act/Assert, deterministic isolation, and integration cleanup; this example is
not a fallback when another repository's closest rule differs.

Manual visual/UI evidence belongs under `production/qa/evidence/`, never
`tests/evidence/`.

## Phase 1: Resolve engine, language, project, and repository policy

Require an owner-approved structured engine authority with schema
`cgs-test-setup-engine-manifest/v1`. It must bind normalized engine ID and approved
aliases, exact engine version, language/runtime, project root, project descriptor
path/hash, project/module/assembly identity, framework/adapter identity, and authority
owner/approval. Require a separate `cgs-test-setup-repository-policy/v1` manifest
binding trunk/default branch, PR target policy, required path filters, cache policy,
job timeout, concurrency/cancellation policy, runner labels, and least-privilege
permissions. Hash both raw files and treat them as read-only authorities.

Require exact agreement among those manifests and:

- `.codex/docs/technical-preferences.md`;
- `docs/engine-reference/<engine>/VERSION.md`;
- the actual project descriptor (`project.godot`, Unity project/package metadata, or
  exactly one `.uproject`);
- configured language/runtime and package/dependency manifests;
- any existing runner/test-framework configuration.

Normalize only aliases enumerated by the engine manifest; never infer an alias or
guess an engine. Verify exact engine version,
project root, project name, language, test-framework version, executable/runner
compatibility, and project assembly/module identity. A missing value, placeholder,
multiple project roots, authority hash mismatch, or conflict is `BLOCKED`. The project
descriptor must resolve inside the declared project root, and all version/language/
identity claims must be proven from structured fields rather than a free-text
`Engine:` line.

Verify the repository policy against a verifiable VCS default-branch reference when
available. Do not hard-code `main`, silently substitute a detected branch, or invent
path/cache/timeout defaults. Any ambiguity or mismatch makes active CI generation
`SETUP_PENDING`.

Require a project-approved immutable dependency manifest such as
`tests/dependencies.lock.json`. It must bind each test framework, parser, launcher,
and third-party CI action to source, exact version, immutable commit SHA/digest,
license/review status, named reviewer and review receipt path/hash, installation path,
transitive lock/digest when applicable, security/deprecation disposition, and current
raw hash. CI actions require a full immutable commit SHA plus repository/source and
review receipt; a full SHA without review, or a major tag, is not immutable approval.
Any dependency or review-receipt byte change invalidates prior setup and CI receipts.

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
`UNMANAGED`, `PLACEHOLDER`, or `UNREADABLE`. Parse JSON/YAML/engine config
structurally and validate exact schema, stable IDs, references, and raw hashes. Search
managed scalar values for unresolved template sentinels, but do not confuse real
GitHub expressions with placeholders. Record one audit row per expected artifact with
path, semantic validator ID/version/hash, outcome, evidence, and current content hash.
Path existence alone never yields `VALID`.

For existing CI, parse the complete YAML tree and validate the exact job ID,
event/default/trunk/PR policy, required path filters, least-privilege permissions,
job timeout, concurrency/cancellation, dependency-cache keys and verified restore
policy, immutable reviewed action SHAs, layout/execution-manifest hashes, exact argv
runner invocation, log/receipt upload, secret references, and platform prerequisites.
Another workflow file or a job named “test” is not proof.

`repair` and legacy `force` produce an immutable ID-keyed repair plan for managed
fields only. Every operation records stable managed ID, file path, JSON/YAML pointer
or bounded text anchor, validator/rule ID, preimage hash, before/after value hashes,
and patch hash. Preserve unmanaged jobs, comments where the parser permits,
human-authored tests, and unrelated files. Never replace the whole workflow or test
tree merely because repair was requested.

Before repair, persist exact preimage bytes under the immutable run root at
`backups/<managed-path-id>.bin`, their hashes, and the full diff. Apply all-file
compare-and-set only after every preimage matches; on any mismatch write nothing and
return `BLOCKED — CONCURRENT CHANGE`. Backups are recovery evidence, not permission to
overwrite later edits. Manual recovery requires a separately authorized three-way
patch with current/base/candidate hashes, all-file compare-and-set, and read-back.

If any selected artifact, validator, authority, or required prefix is unreadable,
omitted, unavailable, or over budget, record it explicitly, set
`Audit Coverage: PARTIAL`, and prohibit `COMPLETE` and all repairs whose safety
depends on the missing evidence.

## Phase 3: Plan the canonical scaffold

Create one canonical `tests/test-layout-manifest.json` whose identity is exactly
`cgs-test-layout/v1`: `artifact_type: cgs-test-layout`, integer
`manifest_version: 1`, and `schema: cgs-test-layout/v1`. It binds the
engine/framework, raw source-authority hashes, required directory IDs/paths,
automated setup-receipt route, manual evidence route, naming-rule source/hash, and
forbidden legacy paths. Hash its raw bytes. The skill, README, execution manifest,
QA consumers, review consumers, and gates must consume that exact canonical
path/hash/schema; they must not duplicate or infer layout. The legacy artifact type
`cgs-test-layout-manifest` is incompatible and must not be emitted.
Conflicting external consumer contracts are an owner handoff and `BLOCKED`, not an
authorization to edit shared files.

The manifest declares this base layout, with nonempty README/manifest files so Git
preserves it:

~~~text template
tests/
  README.md
  test-layout-manifest.json
  dependencies.lock.json
  test-setup-validator-manifest.json
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
from the current layout and execution manifest hashes. It must not claim CI runs or
blocks merges unless a trusted CI receipt verifies that claim. Manual evidence is
always routed by the layout manifest to `production/qa/evidence/`; any
`tests/evidence/` declaration is `CONFLICTING`.

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

Create `tests/test-setup-validator-manifest.json` whose identity is exactly
`cgs-test-validator-manifest/v1`: `artifact_type: cgs-test-validator-manifest`,
integer `manifest_version: 1`, and `schema: cgs-test-validator-manifest/v1`.
It contains a stable row for every required static validator. Each row binds
validator ID, applicable artifact/schema, executable or script path, exact version,
raw executable/script hash, rules path/hash, argv-array template, timeout/output cap,
and expected exit mapping. Hash the exact manifest bytes and bind its canonical
path/hash/schema from all static receipts. The legacy artifact type
`cgs-test-setup-validator-manifest` is incompatible and must not be emitted.

Create `tests/test-execution-manifest.json` as the single execution contract consumed
by staged `smoke-check` and build/CI runners. It must be valid JSON and contain:

- exact identity `cgs-test-execution-manifest/v1`, represented by
  `artifact_type: cgs-test-execution-manifest`, integer `manifest_version: 1`, and
  `schema: cgs-test-execution-manifest/v1`; contract/layout/engine-authority/
  repository-policy/dependency-lock/validator-manifest canonical paths, exact
  schemas and raw hashes; and `hash_algorithm: sha256`;
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
- manifest-generation tool/adapter/validator identities, versions, immutable hashes,
  source-authority hashes, generated-at timestamp, and deterministic serialization
  policy.

The manifest itself is not a test result. Hash its exact raw bytes and require the
candidate manifest/build receipt to capture that path/hash before a consumer may
execute it.

Validate the execution and layout manifests with validators whose exact argv,
version, executable/script hash, rules hash, and dependency manifest hash are pinned.
Static validation receipts use `cgs-test-setup-static-receipt/v1` and record input
path/hash, validator path/hash/version, argv array, start/end, exit code, stdout/stderr
hashes, rule-level findings, coverage ledger, receipt hash, and producer identity.
Missing validators, unsupported schemas, timeout, unreadable inputs, omitted rules,
partial coverage, or hash mismatch are `Static Validation: NOT_RUN/FAIL` and
`Audit Coverage: PARTIAL`; they never become a static PASS.

Never synthesize an engine command at runtime or fall back to another runner. Execute
only a verified argv entry from the current manifest.

## Phase 5: Build or validate active CI without placeholders

Manage only job ID `cgs-tests` in `.github/workflows/tests.yml`.

An active job may be created or patched only when all values resolve and verify:

- exact trunk/PR branch policy and least-privilege permissions;
- exact default/trunk/PR branch policy from the repository-policy hash, required path
  filters, pinned runner OS/self-hosted labels, concurrency/cancellation, and job
  timeout;
- checked-out commit/candidate identity;
- installed framework/engine/dependencies matching immutable lock hashes;
- Unity license secret presence attestation, Unreal self-hosted editor/runner
  attestation, or Godot addon/runner prerequisites as applicable;
- exact execution-manifest path/hash and approved launcher;
- complete log and structured receipt upload even on failure;
- cache keys bound to engine/framework/dependency-lock/tool hashes, explicit allowed
  restore-key scope, and post-restore dependency hash validation; and
- no unresolved project name, engine version, namespace, secret name, action version,
  path, or runner label.

Every third-party action uses an approved full immutable commit SHA, never only a
major tag. The dependency lock and review receipt must bind its source, full SHA,
reviewer, license, security/deprecation disposition, and review timestamp. Validate
YAML syntax/schema and the job semantically before activation. A cache hit is not
dependency proof; re-hash restored bytes before execution and fail closed on drift.
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

Freeze deterministic controls before the first run: stable seed when the framework
accepts one, test order, locale, timezone, working directory, environment-name set,
parallelism/thread count, timeout, and normalization rule. Do not add retries or alter
controls after observing a result. Compare only a declared semantic projection
(discovered stable IDs, exit-class mapping, pass/fail/skip counts, per-test outcome,
and normalized result payload); timestamps and durations are evidence but are excluded
from equality. A framework that cannot enforce or report a required control yields
`Determinism Status: PARTIAL` and cannot be gate eligible.

Run in this order:

1. pass canary: it must be discovered exactly once, execute, report one pass and zero
   failures, and return exit code zero;
2. failure probe: it must be discovered exactly once, execute the intentional
   assertion failure, report at least one failure, and return a nonzero test-failure
   exit code distinct from timeout/infra errors;
3. pass canary again with the failure fixture excluded: it must still return the same
   conclusive pass, match the first pass semantic projection, and prove deterministic
   cleanup/isolation.

Any zero discovery, duplicate ID, unexpected skip, parse error, truncated log,
timeout, runner crash, missing completion signal, failure probe returning zero, or
post-probe contamination, or projection mismatch is `INCOMPLETE`. Set
`Determinism Status: UNSTABLE` for a conclusive projection mismatch and `PARTIAL` for
missing controls/evidence. Never label either verified.

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
- frozen deterministic controls, semantic-projection schema/hash, and comparison
  result;
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
- candidate-manifest, contract, engine authority, repository policy, layout manifest,
  and execution-manifest paths/hashes;
- current runner/config, parser, dependency-lock plus dependency-review receipts,
  workflow, and test-source hashes;
- exact stable IDs and argv arrays used for pass canary, failure probe, and post-probe
  pass;
- start/end, issuer, workflow/job/run IDs, attempt, immutable action SHAs, and exit
  codes;
- complete untruncated log paths/hashes;
- parser version/status, discovery/counts, and per-test results;
- frozen deterministic controls and equal pass semantic-projection hashes;
- baseline PASS, intentional nonzero FAIL, and isolated post-probe PASS;
- receipt raw-byte SHA-256 or trusted signature.

Re-hash every local referenced artifact. Reject another build, stale sources, old
workflow bytes, untrusted issuer, unverifiable remote logs, truncated output,
failure-probe exit zero, or missing per-test IDs as `CI Status: INVALID`, never
verified.

Normalize supplied receipt state before using it: missing schema/hash/signature or a
parse/signature failure is `INVALID`; any dependency hash mismatch is `STALE`; an
unavailable remote receipt/log, timeout, unsupported verifier, or incomplete coverage
is `UNVERIFIED` with partial verification; only a fully revalidated match is
`CURRENT`. No missing or partial CI evidence is inferred from a green badge, latest
run, timestamp, file name, or successful local run.

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
- contract, engine-authority, repository-policy, layout-manifest, dependency-lock, and
  dependency-review receipt paths/hashes;
- complete/partial audit ledger and semantic validator/tool versions/hashes;
- exact created, patched, unchanged, unmanaged, and rejected paths with hashes;
- repair operation IDs, preimage/backup/diff/postimage hashes and compare-and-set
  result when repair ran;
- static parse/schema/placeholder results;
- test manifest path/hash and every canary source stable ID/hash;
- discovery counts;
- pass, failure-probe, and post-probe receipt/log paths/hashes/statuses, frozen
  deterministic controls, projection hashes, and comparison;
- CI workflow path/hash/status/prerequisites and CI receipt/signature;
- every verification-state field, gaps, and non-writes.

Use this machine-readable header:

~~~text template
Artifact Type: test-setup-receipt
Schema Version: 2
Receipt ID: <setup-run-id>
Candidate ID: <candidate-id>
Build ID: <build-id>
Build Artifact SHA-256: sha256:<digest>
Source Commit: <commit>
Contract SHA-256: sha256:<digest>
Engine Manifest Path: <project-relative-path>
Engine Manifest SHA-256: sha256:<digest>
Repository Policy Path: <project-relative-path>
Repository Policy SHA-256: sha256:<digest>
Layout Manifest Path: tests/test-layout-manifest.json
Layout Manifest SHA-256: sha256:<digest>
Test Manifest Path: tests/test-execution-manifest.json
Test Manifest SHA-256: sha256:<digest>
Dependency Lock SHA-256: sha256:<digest>
Audit Coverage: <COMPLETE|PARTIAL|NOT_RUN>
Verification Level: <AUDITED|CREATED|STATIC_VALIDATED|DISCOVERY_VERIFIED|CANARY_PASS|FAILURE_SENSITIVE|CI_VERIFIED>
Determinism Status: <VERIFIED|UNSTABLE|PARTIAL|NOT_RUN>
Receipt Freshness: <CURRENT|STALE|INVALID|UNVERIFIED|NOT_APPLICABLE>
Setup Status: <VERIFIED|SETUP_PENDING|SCAFFOLDED|INCOMPLETE|BLOCKED|ERROR>
CI Status: <VERIFIED|STATIC_VALIDATED|SETUP_PENDING|INVALID|NOT_CONFIGURED>
Pass Canary Status: <status>
Failure Sensitivity: <status>
Gate Eligible: <YES|NO>
Verdict: <COMPLETE|SETUP_PENDING|SCAFFOLDED|INCOMPLETE|BLOCKED|ERROR>
~~~

Derive the final result in strict order:

1. `ERROR` for write/read-back/internal-reference failure.
2. `BLOCKED` for unresolved engine/project/instruction identity, partial safety audit,
   concurrent repair change, or unauthorized required scope.
3. `INCOMPLETE` for invalid config, zero/incomplete discovery, nonpassing baseline,
   nonsensitive failure probe, unstable/partial determinism,
   timeout/infra/parse/truncation/hash failure.
4. `SCAFFOLDED` when safe files exist but execution did not run.
5. `SETUP_PENDING` when local static/discovery/canaries pass but any external
   plugin/package/secret/runner/active-CI/trusted-CI-receipt prerequisite remains.
6. `COMPLETE` only when the audit ledger is complete and all instruction/engine/repo/
   layout semantics, dependency and review-receipt hashes, pinned static validation,
   discovery, pass/fail/post-probe canaries, deterministic projection, active CI, and
   trusted current CI receipt verify for the same candidate/build bytes.

Only case 6 uses `Setup Status: VERIFIED` and `Gate Eligible: YES`.

If report persistence is authorized, stage its owned run-directory files, verify
internal references/hashes, publish all or none, re-read them, and display the setup
report SHA-256. A declined or failed persistence makes the durable setup receipt
unavailable and `Gate Eligible: NO`, without changing observed canary outcomes.

Do not claim files were created unless they appear in the verified changed-path list.
Advance `Verification Level` monotonically and stop at the last proven rung:
`AUDITED -> CREATED -> STATIC_VALIDATED -> DISCOVERY_VERIFIED -> CANARY_PASS ->
FAILURE_SENSITIVE -> CI_VERIFIED`. A higher rung never backfills a lower missing rung.
Do not invoke `$smoke-check`, `$regression-suite`, `$test-evidence-review`, or a gate.
Downstream consumers must receive exact receipt/candidate/test-manifest paths and
expected hashes and must revalidate them; no consumer may choose the newest receipt.

## P1 audit traceability

Each exact ID from the authoritative 2026-07-20 P1 audit table has one independent
trace row linking the normative clause to a dedicated-spec case/assertion. This is
static traceability and does not claim execution.

| Audit ID | Normative clause | Dedicated spec evidence |
|---|---|---|
| `TSU-005` | Phase 2 semantic audit and bounded stable-ID repair | Case 1 — assertions `Stale runner semantics are reported despite every path existing` and `Partial audit coverage prevents repair and gate eligibility` |
| `TSU-006` | Phase 1 root-to-target instruction authority and Phase 3 naming | Case 2 — assertions `Generated names follow the closest tests rule` and `An unreadable applicable rule yields Audit Coverage PARTIAL` |
| `TSU-007` | Contract manifest evidence route and Phase 3 canonical layout | Case 3 — assertions `No generated text routes visual or UI proof under tests` and `Shared consumers are never silently edited` |
| `TSU-008` | Phase 3 versioned layout/validator/execution manifest contract | Case 4 — assertions `Every required directory ID resolves to one contained path` and `The execution manifest binds the layout-manifest hash` |
| `TSU-009` | Phase 1 structured engine/language/project authority | Case 5 — assertions `No engine, language, version, project name, module, or assembly is guessed` and `Identity conflict yields BLOCKED` |
| `TSU-010` | Phase 1 repository policy and Phase 5 reviewable CI | Case 6 — assertions `No branch, path-filter, cache, timeout, or permission default is invented` and `Policy mismatch prevents CI VERIFIED` |
| `TSU-011` | Phase 5 exact managed `cgs-tests` job semantic validation/patch | Case 7 — assertions `Wrong argv is found even if the workflow is syntactically valid` and `Whole-workflow replacement is prohibited` |
| `TSU-012` | Verification states plus Phases 4, 6, and 8 monotonic ladder | Case 8 — assertions `Static parser success does not prove discovery` and `No incomplete branch emits COMPLETE or VERIFIED setup` |
| `TSU-013` | Phase 5 immutable reviewed dependency/action provenance | Case 9 — assertions `Major tags fail immutable identity` and `Full commit SHA alone does not prove review` |
