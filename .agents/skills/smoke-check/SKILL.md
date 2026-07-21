---
name: smoke-check
description: "Runs a build-bound smoke gate from current QA-plan mappings, structured runner receipts, and explicit manual evidence; only a complete formal PASS authorizes QA hand-off."
---

## Invocation and safety contract

Invoke one of these supported forms:

~~~text
$smoke-check sprint --candidate {candidate-manifest-path} --qa-plan {qa-plan-path} --run-id {run-id} [--platform pc|console|mobile|all] [--ci-receipt {path}]
$smoke-check quick --candidate {candidate-manifest-path} --qa-plan {qa-plan-path} --run-id {run-id} --checks {stable-id[,stable-id...]} [--platform pc|console|mobile|all] [--ci-receipt {path}]
~~~

The default mode is sprint. Reject unknown positional arguments, unknown flags, duplicate flags, unsupported platform values, a missing flag value, a quick invocation without --checks, or any mode other than sprint or quick. Do not interpret an affected-system name as a mode. A caller such as day-one-patch must translate its scope into stable QA-plan check IDs and use quick --checks.

An explicit bounded user request authorizes its in-scope execution and writes. Otherwise, before the first file change, present one complete changeset and obtain one explicit approval. Do not re-prompt per file. A declined report write does not change the observed test outcome; report Persistence: DECLINED and retain the result in conversation.

This workflow never invokes a director gate and never edits source code, tests, the candidate manifest, the QA plan, session state, or another workflow artifact.

## Canonical artifacts and identity

Use this immutable evidence root:

~~~text
production/qa/evidence/smoke/{candidate-id}/{run-id}/
  automated-receipt.json
  automated.log  (only when runner or CI log bytes exist)
  manual-evidence.md
  report.md
~~~

A run ID is a stable slug or UUID, not a date alone. Reject path separators, dot segments, and any existing run directory. A retry always uses a new run ID. Never choose evidence by modification time and never overwrite a prior receipt.

The only hand-off-eligible artifact is the exact report.md path supplied to a consumer together with the expected candidate ID and candidate-manifest SHA-256. Files in legacy locations, incomplete directories, quick-mode reports, and newest-file guesses are not gate evidence.

## Phase 1: Validate exact candidate and QA-plan inputs

Resolve literal paths and real paths before use. Reject missing files, directories, symlinks escaping the project root, and unreadable or malformed inputs. Read raw bytes once and format every digest exactly as sha256:<64 lowercase hexadecimal characters>.

### Candidate manifest

Require the supplied candidate manifest to contain:

- manifest_version and Artifact Type: build-candidate;
- candidate_id, build_id, build artifact path, and build artifact SHA-256;
- source_commit;
- engine name and exact engine/runner-compatible version;
- platform/configuration target matrix;
- created_at in ISO-8601;
- test_manifest_path and test_manifest_sha256;
- qa_plan_path and qa_plan_sha256.

The --qa-plan path must equal qa_plan_path after normalization, and its raw-byte digest must equal qa_plan_sha256. Verify the candidate build artifact bytes against their digest. If the build is remote, require a verifiable build receipt that binds the same candidate ID, build ID, artifact hash, source commit, platform/configuration, issuer, job ID, and timestamp. Missing or mismatched candidate evidence is INVALID_RECEIPT.

### QA-plan manifest and effective state

Consume the exact staged qa-plan contract, not a most-recent plan:

1. Require Plan State at Generation: CURRENT, manifest_version: 1, hash_algorithm: sha256, the mandatory Sources table, Story Requirement Bindings, Test Summary, and Smoke Test Scope.
2. Re-read every loaded source path recorded in the plan and hash its current raw bytes.
3. Require every current source digest and availability to match the plan. Any mismatch, disappearance, unreadable source, or invalid digest makes the effective state STALE.
4. Reject PARTIAL, STALE, missing stable AC IDs, duplicate IDs, and test/check IDs that do not map one-to-one to a stable AC ID.
5. For sprint mode, select every stable ID in Smoke Test Scope. For quick mode, require each --checks ID to exist in that scope and preserve the explicit subset.
6. Compute scope_sha256 from the ordered selected stable IDs, their stable AC bindings, and their plan rows.

A non-CURRENT QA plan, a plan hash mismatch, or an invalid scope is a blocking currentness error. Do not execute tests or collect manual evidence against it.

### Test execution manifest

Read the exact test manifest path from the candidate manifest and verify its raw-byte digest. It must define:

- manifest version, candidate-compatible engine and runner versions;
- an argv array for each stable automated test ID, with no shell command string;
- a project-root-contained working directory;
- environment-variable allowlist with secret values excluded from reports;
- timeout and output-byte cap;
- exit-code and structured-result parser rules;
- cleanup behavior that terminates the runner process tree on timeout;
- canonical log and receipt fields;
- trusted CI issuer/job allowlist and receipt-signature or verification rules when CI substitution is permitted.

Do not synthesize engine commands, fall back to arbitrary runners, use shell redirection, or select historical XML/JSON/log files by modification time. A missing or invalid execution manifest yields Verdict: INCOMPLETE and Handoff Eligible: NO.

## Phase 2: Produce build-bound automated evidence

Run only the argv entries allowed by the verified test execution manifest, from its verified working directory. Apply the declared timeout and output cap. Capture stdout/stderr without shell interpolation, redact declared sensitive values, terminate the full process tree on timeout, and hash the exact persisted log bytes.

The structured automated receipt must contain:

- Artifact Type: automated-test-receipt and schema version;
- candidate ID, build ID, build artifact hash, source commit;
- platform/configuration;
- test-manifest path and hash;
- QA-plan path and hash, scope hash, and stable test IDs;
- runner name/version, exact argv array, working directory;
- start/end timestamps, observer or CI issuer, exit code;
- total/pass/fail counts and per-test stable ID/status;
- log path, log SHA-256, truncation flag, parser version, and receipt status.

Use these automated statuses:

| Status | Meaning |
|---|---|
| PASS | Valid receipt, zero required test failures, complete untruncated parse |
| FAIL | Valid receipt with one or more required test failures |
| NOT_RUN | Required command did not execute |
| TIMEOUT | Deadline expired and process tree was terminated |
| INFRA_ERROR | Runner crashed, could not start, or returned infrastructure failure |
| INVALID_RECEIPT | Build binding, hashes, counts, IDs, log, or parse is missing/inconsistent |

Only PASS and FAIL are conclusive test outcomes. NOT_RUN, TIMEOUT, INFRA_ERROR, INVALID_RECEIPT, a parse error, and a truncated log are incomplete evidence and can never be treated as a pass.

### External CI substitution

A --ci-receipt may replace local execution only when it is verifiable and binds the exact candidate ID, build ID/hash, source commit, platform/configuration, test-manifest hash, QA-plan hash, scope hash, stable test IDs, runner/version, argv, start/end, issuer/job ID, exit code, complete log hash, parser version, and per-test results. Re-hash every local receipt/log artifact and reject stale or mismatched fields. An unavailable remote artifact, untrusted issuer, truncated log, or non-verifiable job is INVALID_RECEIPT, not PASS.

## Phase 3: Collect explicit manual and platform evidence

Build the required manual rows from the selected stable QA-plan IDs and their Setup, Verify, Pass condition, evidence path, and sign-off owner. Add applicable data-integrity, performance, and platform rows declared by the current QA plan or candidate target matrix. Do not infer coverage from filenames.

Collect rows in no more than three conversational batches, but require an explicit result for every row. Each row must contain:

- stable check ID and stable AC ID;
- exactly one status: PASS, FAIL, NOT RUN, or N-A;
- candidate ID, build ID/hash, source commit;
- platform/configuration, device model, OS/runtime, and input method where applicable;
- observer ID/role and ISO-8601 observation timestamp;
- executed setup/method, observed value, and evidence path/hash;
- failure description for FAIL;
- applicability rule and reason for N-A.

An empty answer, an unselected item, an unsupported multi-select control, missing observer/build/platform/time binding, missing evidence, or ambiguous prose becomes UNKNOWN. Never convert silence into PASS. NOT RUN and UNKNOWN are incomplete. N-A is acceptable only when the QA plan or candidate matrix marks the row optional for that configuration and a reason is recorded.

Keep sensitive or irrelevant free text out of the report. Preview a redacted observation summary and retain a bounded evidence reference/hash rather than copying unlimited raw text.

Every required platform row is independent. Do not average platforms. Any platform FAIL contributes to overall FAIL; any required platform NOT RUN or UNKNOWN contributes to INCOMPLETE. Any explicit save corruption, data loss, critical performance failure, or other required manual FAIL contributes to overall FAIL regardless of which batch contained it.

## Phase 4: Verify coverage and calculate one verdict

For each selected stable ID, require exactly one applicable conclusive receipt:

- automated IDs require a build-bound automated PASS or FAIL row;
- manual IDs require an explicit build-bound PASS, FAIL, or valid N-A row;
- combined methods require both declared components;
- every evidence path must exist and its raw bytes must match its recorded hash.

Missing IDs, duplicate/conflicting rows, missing high-risk coverage, UNKNOWN, NOT RUN, invalid N-A, stale evidence, hash mismatch, or an unverified receipt are incomplete evidence.

Apply this exhaustive, mutually exclusive first-match table:

| Precedence | Condition | Verdict | Handoff Eligible |
|---|---|---|---|
| 1 | Any conclusive automated FAIL or any required manual/data/performance/platform FAIL | FAIL | NO |
| 2 | Any currentness error, missing/invalid evidence, automated status other than PASS/FAIL, UNKNOWN, NOT RUN, coverage gap, invalid N-A, unresolved warning, parser error, or truncated log | INCOMPLETE | NO |
| 3 | Mode is quick and every selected targeted row is current and conclusively PASS or valid N-A | TARGETED CHECK PASSED | NO |
| 4 | Mode is sprint, every required row is current and conclusively PASS or valid N-A, and the warning set is empty | PASS | YES |

FAIL takes precedence when failures and incomplete evidence coexist, while the report also lists the incomplete rows. There is no PASS WITH WARNINGS hand-off state. Any unresolved warning maps to INCOMPLETE. Thus zero-warning and nonzero-warning cases always have one defined result. The table's YES is provisional until Phase 5 verifies persistence; a declined or failed write retains the calculated verdict but changes the returned Handoff Eligible field to NO.

Quick mode is targeted evidence only. It skips nothing within its selected stable IDs, but it never proves full sprint coverage and can never authorize QA or release hand-off.

## Phase 5: Generate the immutable smoke receipt

Generate report.md with these machine-readable fields:

~~~text
Artifact Type: smoke-check-receipt
Schema Version: 1
Receipt ID: {run-id}
Receipt State: COMPLETE | INCOMPLETE | FAILED
Candidate Manifest Path: {path}
Candidate Manifest SHA-256: sha256:{digest}
Candidate ID: {candidate-id}
Build ID: {build-id}
Build Artifact SHA-256: sha256:{digest}
Source Commit: {commit}
Platform Configuration: {matrix}
QA Plan Path: {path}
QA Plan SHA-256: sha256:{digest}
QA Plan Effective State: CURRENT | PARTIAL | STALE
Test Manifest Path: {path}
Test Manifest SHA-256: sha256:{digest}
Scope SHA-256: sha256:{digest}
Mode: sprint | quick
Verdict: PASS | FAIL | INCOMPLETE | TARGETED CHECK PASSED
Handoff Eligible: YES | NO
Started At: {ISO-8601}
Ended At: {ISO-8601}
~~~

Then include:

1. candidate, QA-plan, test-manifest, and scope validation;
2. automated receipt summary with stable test IDs, exit code, parser state, log hash, and failures;
3. one row per manual/platform check with all provenance and evidence hashes;
4. stable AC-to-test/check coverage matrix;
5. failures, incomplete rows, and warnings in separate lists;
6. the exact verdict-table row applied;
7. immutable artifact paths and hashes;
8. persistence result.

Receipt State is FAILED for verdict FAIL, INCOMPLETE for verdict INCOMPLETE, and COMPLETE for PASS or TARGETED CHECK PASSED. COMPLETE does not imply hand-off eligibility; quick remains Handoff Eligible: NO.

Present the complete candidate receipt and proposed operations before writing. If authorized, stage every owned artifact, verify internal references and hashes, then publish the run directory all-or-none. Re-read every file and compare with the approved bytes. If any write or verification fails, Persistence: FAILED and Handoff Eligible: NO; never claim the report was written.

A report write is optional evidence persistence. The observed verdict must still be returned if persistence is declined or fails, but the returned Handoff Eligible value becomes NO and no consumer may use a non-persisted receipt. If candidate identity is not valid enough to form the canonical path, do not create a run directory and report Persistence: NOT_ATTEMPTED.

## Phase 6: Deliver the gate result

Always return:

- exact candidate manifest path/hash and candidate/build identity;
- exact QA-plan path/hash and computed effective state;
- exact smoke receipt path/hash when verified persisted;
- mode, scope stable IDs/hash, automated status, and manual/platform row counts;
- Persistence: WRITTEN, DECLINED, FAILED, or NOT_ATTEMPTED;
- one verdict from the table;
- Handoff Eligible: YES or NO.

Only a verified persisted sprint-mode receipt with Verdict: PASS, Handoff Eligible: YES, exact candidate-manifest match, exact build binding, and currently revalidated QA Plan Effective State: CURRENT may be handed to QA. All other results explicitly say BLOCKED FOR HANDOFF. Do not say that a build is ready when evidence is missing, stale, quick, unpersisted, unknown, or warning-bearing.

Downstream consumers must receive the exact receipt path plus expected candidate ID and candidate-manifest hash. They must re-hash the candidate manifest, QA plan and all captured QA-plan sources, test manifest, automated log, manual evidence, and report. Any mismatch makes the receipt STALE and blocks hand-off. Consumers must never select the most recently modified smoke report.

Recommend correcting reported failures or missing evidence and running a new run ID. Never auto-fix code or tests and never auto-invoke a downstream workflow.
