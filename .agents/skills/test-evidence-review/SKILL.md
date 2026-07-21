---
name: test-evidence-review
description: "Reviews requirement-bound test and manual evidence on separate structural-quality and current-execution axes, with hash-bound provenance and per-AC closure results."
---

## Invocation and ownership

Invoke as:

~~~text
$test-evidence-review --manifest {evidence-review-manifest-path} [--persist]
~~~

The manifest is mandatory. With no argument, ask for one exact manifest path and do not discover a current sprint, system, story, QA plan, smoke report, or newest file. Reject positional test paths, ambiguous story/system names, unknown flags, duplicate flags, missing values, and any mode not defined above.

This workflow is read-only except for its optional owned report:

~~~text
production/qa/evidence/reviews/{review-id}/report.md
~~~

It never edits tests, stories, QA plans, candidate manifests, smoke/playtest evidence, attestations, registries, session state, or source artifacts. A review ID must be a stable slug or UUID, not a date alone; reject path separators, dot segments, or an existing review directory.

An explicit bounded user request authorizes its in-scope optional report. Otherwise, if --persist is requested, present the complete one-file changeset and obtain one explicit approval before writing. Do not prompt when no write is requested and do not re-prompt within an authorized boundary.

This workflow never invokes a director gate or another workflow.

## Result vocabulary

Do not emit a single overloaded Verdict field. Report these independent fields:

- Workflow Status: COMPLETE, PARTIAL, or BLOCKED
- Overall Evidence Quality: ADEQUATE, INCOMPLETE, MISSING, or UNAVAILABLE
- Overall Execution Status: PASS, FAIL, UNKNOWN, STALE, or UNAVAILABLE
- Execution Scope: FULL, TARGETED, or NONE
- Closure Eligible: YES or NO
- Persistence: NOT_REQUESTED, WRITTEN, DECLINED, FAILED, or NOT_ATTEMPTED

Workflow Status describes whether this review process evaluated the declared scope. Evidence Quality describes structural and semantic sufficiency. Execution Status describes current-build results. COMPLETE never means that evidence passed; ADEQUATE never implies execution; PASS never implies structural quality.

A structurally strong test with no current-build runtime receipt must be reported exactly as Evidence Quality: ADEQUATE, Overall Execution Status: UNKNOWN, Closure Eligible: NO.

## Phase 1: Validate the evidence-review manifest

Resolve the supplied literal path and real path. Reject missing files, directories, symlinks escaping the project root, unreadable bytes, malformed syntax, duplicate keys, and unsupported schema versions. Read each source once as raw bytes and compute SHA-256 over those exact bytes.

Require this manifest schema:

- Artifact Type: test-evidence-review-manifest
- Schema Version: 1
- Review ID and generated-at timestamp
- exact QA-plan path and raw-byte SHA-256
- exact candidate-manifest path and raw-byte SHA-256
- candidate ID, build ID, build artifact SHA-256, source commit, and platform/configuration
- ordered scope rows, each with stable story ID/path/hash, stable AC ID, stable QA-plan test/check ID, evidence method, expected observable, and all expected evidence references
- exact smoke receipt path/hash when automated or smoke evidence is required
- exact completed playtest report path/hash when playtest evidence is required
- test-source, manual-artifact, artifact-receipt, and reviewer-attestation paths/hashes as applicable
- attester registry or external identity-verification source path/hash when an attestation is required

Every scope row must map one stable AC ID to exactly one stable QA-plan test/check ID. Reject duplicate AC IDs, duplicate test/check IDs assigned to different ACs, missing IDs, ambiguous paths, and references not contained by the project root. Preserve the ordered row set and compute a scope SHA-256 over stable IDs, evidence methods, expected observables, paths, and declared hashes.

If the manifest cannot establish a unique scope, return Workflow Status: BLOCKED, Overall Evidence Quality: UNAVAILABLE, Overall Execution Status: UNAVAILABLE, Closure Eligible: NO, and Persistence: NOT_ATTEMPTED. Do not write a report.

## Phase 2: Revalidate QA-plan and candidate currentness

### QA-plan contract

Read the exact QA-plan bytes named by the manifest and require the captured digest to match. Apply the staged qa-plan consumer contract:

1. Require Plan State at Generation: CURRENT, manifest_version: 1, hash_algorithm: sha256, Sources, Story Requirement Bindings, Test Summary, and Smoke Test Scope.
2. Re-read every captured source path and hash its current raw bytes.
3. Any source mismatch, disappearance, unreadable source, invalid digest, PARTIAL generation state, missing stable AC binding, or duplicate mapping makes the effective state STALE or UNAVAILABLE.
4. Require every review scope row to match the plan's story ID/path/hash, stable AC ID, stable test/check ID, method, expected evidence path, and owner.
5. Do not infer a mapping from a filename, directory, comment, test name, or similar wording.

### Candidate contract

Read and hash the exact candidate manifest. Require candidate ID, build ID, build artifact hash, source commit, platform/configuration, QA-plan path/hash, and test-manifest path/hash to match the review manifest and current QA plan. Re-hash a local build artifact; for a remote build require its trusted build receipt.

Any relevant story, GDD, ADR, control, QA-plan, candidate, build, test-manifest, test-source, or evidence byte change from a captured digest makes dependent evidence STALE. Dates and modification times never establish freshness.

Currentness failures do not become product-level MISSING findings. Record a mismatched readable input as STALE. Record an input that cannot be read or parsed as UNAVAILABLE and set Workflow Status: PARTIAL. Never silently omit its AC rows.

## Phase 3: Review automated-test structural quality

Use the QA-plan's stable AC-to-test mapping and the exact test-source path/hash from each manifest row. Path presence proves only Presence: PRESENT. Re-hash the source and require the digest to match before semantic review.

For each automated or combined-method AC row, evaluate:

1. Requirement mapping: the stable test ID and source metadata explicitly bind the exact stable AC ID and expected observable.
2. Observable semantics: trace setup, stimulus, and the actual asserted state/event/output to the AC. Comments and names are context, not proof.
3. Failure sensitivity: identify why the test would fail if the required behavior were removed, inverted, or changed. Accept a requirement-bound negative control, boundary/fault case, or current mutation-test receipt that names the same stable IDs and source/build hashes.
4. Independence: distinguish genuinely different observables and cases from duplicate or equivalent assertions.
5. Helper traceability: a helper assertion counts only after its implementation/contract is read, hash-bound, and shown to check the required observable.
6. Boundary/formula coverage: use stable requirement IDs and declared plan rows, not keyword searches.
7. Determinism/isolation findings: report timing, randomness, external I/O, shared state, or hidden-order dependencies when actually evidenced.

Never count lines containing assert, expect, check, or verify. Ignore such tokens inside comments, strings, names, or unreviewed helpers. Repeated low-information assertions do not improve quality, while one high-information failure-sensitive assertion may be sufficient.

Test naming is an independent maintainability finding. Parse the repository convention test_{system}_{scenario}_{expected}. A name missing system, scenario, or expected is nonconforming. A conforming name does not prove coverage, and a nonconforming name must never be split heuristically to invent a system or requirement mapping.

Assign per automated row:

- ADEQUATE only when mapping, observable semantics, and failure sensitivity are demonstrated and no blocking structural gap remains;
- INCOMPLETE when evidence is present but semantic coverage or provenance is insufficient;
- MISSING only when a required artifact is explicitly absent;
- UNAVAILABLE when a declared artifact exists but cannot be read, parsed, or inspected.

## Phase 4: Review manual, visual, UI, and playtest evidence

For every required manual artifact, validate both an artifact receipt and the artifact bytes. A path that exists establishes only Presence: PRESENT.

The receipt must bind:

- stable story, AC, and QA-plan check IDs;
- candidate ID, build ID/hash, source commit, platform/configuration, device/runtime/input profile;
- artifact path, MIME type, byte size, SHA-256, capture timestamp, and capture method;
- captor/observer identity;
- expected observable and reproducible setup;
- privacy/redaction classification.

Re-hash the artifact and compare size/type. Inspect its actual content using an appropriate decoder or viewer. A screenshot must visibly demonstrate the expected state for its AC; a walkthrough must preserve ordered actions and observable results; a log must contain the relevant bounded event/result. A filename, path, caption, or creation date alone is never evidence of content. If content cannot be decoded or inspected, mark the row UNAVAILABLE rather than assuming it passes.

### Reviewer attestation

A nonempty sign-off field is not an approval. Require a separate attestation that binds reviewer identity/role, timestamp, exact scope IDs, candidate/build identity, artifact paths/hashes, attestation statement, and the reviewed result. Verify identity and authorization against the manifest's hash-bound attester registry or external verification receipt. A mismatched, unverifiable, stale, or out-of-scope attestation is INCOMPLETE and cannot authorize closure.

The model must never invent an identity, infer approval from a role label, or sign on behalf of a developer, designer, art lead, QA lead, or other reviewer.

### Canonical playtest consumer

When a QA-plan row requires playtest evidence, accept only the exact hash-bound canonical path:

~~~text
production/playtests/{session-id}/report.md
~~~

Require Artifact Type: playtest-session-result, Schema Version: 1, Status: COMPLETED, Gate Eligible: YES, matching candidate build/version/source/platform/hypothesis or AC IDs, evidence receipt ID, raw-evidence SHA-256, manifest SHA-256, and observation-ledger SHA-256. Re-hash the referenced manifest, raw evidence, observation ledger, and report. Require derived findings to resolve to stable Observation IDs and the verified raw hash.

Protocols, templates, ingest-only sessions, raw notes, director reviews, legacy paths, malformed reports, or newest-file guesses cannot satisfy an AC.

## Phase 5: Verify current-build execution evidence

Structural quality and execution are independent. For every automated, smoke, or combined-method AC row, load the exact smoke receipt and hash declared by the review manifest. Apply the staged smoke-check consumer contract:

- canonical path production/qa/evidence/smoke/{candidate-id}/{run-id}/report.md;
- Artifact Type: smoke-check-receipt and Schema Version: 1;
- exact candidate-manifest path/hash, candidate ID, build ID/hash, source commit, and platform/configuration;
- exact QA-plan path/hash with recomputed QA Plan Effective State: CURRENT;
- exact test-manifest path/hash and scope hash;
- exact automated receipt/log/manual-evidence paths and hashes;
- persisted receipt with no read-back failure;
- stable test/check rows covering the declared AC IDs.

Re-hash the candidate manifest, QA plan and all captured QA-plan sources, test manifest, automated receipt/log, manual evidence, and smoke report. Do not select the most recently modified receipt.

Map execution status deterministically:

- FAIL if a valid current-build receipt has a conclusive required FAIL;
- STALE if readable receipt bindings or hashes no longer match;
- UNAVAILABLE if a declared receipt or required referenced artifact cannot be read/parsed;
- UNKNOWN if no current-build receipt is declared or its required AC result is NOT RUN, UNKNOWN, incomplete, targeted outside the row, or otherwise nonconclusive;
- PASS only when every required row has a conclusive current-build pass.

Record Execution Scope: FULL only for a verified persisted sprint-mode smoke receipt with Verdict: PASS and Handoff Eligible: YES. A verified quick TARGETED CHECK PASSED receipt may establish a current targeted row but Execution Scope remains TARGETED and Closure Eligible remains NO. INCOMPLETE, FAIL, warning-bearing, quick, stale, missing, and unpersisted smoke results never authorize closure.

Manual and playtest execution rows use their verified build-bound artifact/attestation or completed-session status. Missing runtime evidence never downgrades to a structural warning.

## Phase 6: Build per-AC and aggregate results

Emit exactly one result row for every manifest AC:

| Story ID | AC ID | Test/Check ID | Method | Presence | Evidence Quality | Execution Status | Execution Scope | Attestation | Blocking Findings | Closure Eligible |
|---|---|---|---|---|---|---|---|---|---|---|

Per-row Closure Eligible is YES only when:

- all paths/hashes/currentness checks pass;
- Evidence Quality is ADEQUATE;
- Execution Status is PASS with the QA-plan-required scope;
- required manual/playtest content inspection passes;
- every required attestation is verified and current;
- no blocking finding remains.

Aggregate without hiding rows:

- Overall Evidence Quality is MISSING if any required artifact is explicitly absent; otherwise UNAVAILABLE if any row could not be inspected; otherwise INCOMPLETE if any row has a structural/provenance gap; otherwise ADEQUATE.
- Overall Execution Status is FAIL if any valid current failure exists; otherwise STALE if any binding/hash is stale; otherwise UNAVAILABLE if required evidence could not be read; otherwise UNKNOWN if any required result is absent/nonconclusive; otherwise PASS.
- Execution Scope is FULL only when every row has its required full-scope evidence; otherwise TARGETED when all evaluated runtime evidence is targeted; otherwise NONE.
- Workflow Status is BLOCKED for an invalid/ambiguous manifest, PARTIAL for read/parse/inspection failures that leave declared rows unevaluated, and COMPLETE when every declared row was evaluated even when its quality is MISSING or INCOMPLETE.
- Overall Closure Eligible is YES only if every row is eligible, Workflow Status is COMPLETE, Overall Evidence Quality is ADEQUATE, Overall Execution Status is PASS, and Execution Scope satisfies every QA-plan row.

Do not replace these fields with PASS/WARNINGS/FAIL, ADEQUATE/INCOMPLETE/MISSING as a single verdict, or a trailing Verdict: COMPLETE/CONCERNS line.

## Phase 7: Present and optionally persist the review

Present a machine-readable header:

~~~text
Artifact Type: test-evidence-review-report
Schema Version: 1
Review ID: {review-id}
Review Manifest Path: {path}
Review Manifest SHA-256: sha256:{digest}
Scope SHA-256: sha256:{digest}
QA Plan Path: {path}
QA Plan SHA-256: sha256:{digest}
QA Plan Effective State: CURRENT | STALE | UNAVAILABLE
Candidate Manifest Path: {path}
Candidate Manifest SHA-256: sha256:{digest}
Candidate ID: {candidate-id}
Build ID: {build-id}
Build Artifact SHA-256: sha256:{digest}
Source Commit: {commit}
Workflow Status: COMPLETE | PARTIAL | BLOCKED
Overall Evidence Quality: ADEQUATE | INCOMPLETE | MISSING | UNAVAILABLE
Overall Execution Status: PASS | FAIL | UNKNOWN | STALE | UNAVAILABLE
Execution Scope: FULL | TARGETED | NONE
Closure Eligible: YES | NO
Persistence: NOT_REQUESTED | WRITTEN | DECLINED | FAILED | NOT_ATTEMPTED
~~~

Then present:

1. exact review-manifest, QA-plan, candidate, smoke, playtest, test-source, artifact, receipt, attestation, and scope hashes;
2. the complete per-AC table;
3. structural findings separated from runtime findings;
4. unavailable inputs separated from known missing product evidence;
5. aggregate fields from Phase 6;
6. remediation owner for each blocking gap;
7. Persistence state.

With --persist, generate the full report at production/qa/evidence/reviews/{review-id}/report.md. Preview the exact one-file CREATE operation and explicit non-writes. Reject an existing review directory rather than overwriting. If authorized, re-hash all inputs immediately before writing, abort on any change, write atomically, re-read the bytes, and report the verified report SHA-256. On decline or failure, preserve the evidence-quality, execution, and closure assessment unchanged and report Persistence: DECLINED or FAILED. Persistence is an independent workflow result; a non-persisted review cannot itself be cited as a durable review receipt.

Without --persist, make no write and report Persistence: NOT_REQUESTED. A conversation-only review may describe the eligibility of the underlying evidence, but the review itself is not a durable closure receipt.

Recommend the exact missing/stale/unavailable evidence or owning role to address. Do not fix tests, create evidence, solicit a fake sign-off, mutate another artifact, or invoke a downstream workflow.
