---
name: test-evidence-review
description: "Reviews requirement-bound evidence on independent structural-quality and current-execution axes with typed admissibility, stable findings, and optional immutable reporting."
---

# Test Evidence Review

## Purpose and authority boundary

Review one explicit, immutable evidence scope. Determine whether the evidence is structurally meaningful and whether it proves a conclusive result for the exact current build. These are independent questions.

This workflow does not execute tests, generate evidence, approve work, edit tests or requirements, fix findings, change a sprint, create attestations, or invoke another workflow. Default operation is byte-for-byte read-only. The only optional mutation is one immutable owned review report when `--persist` is explicitly requested and authorized.

## Invocation contract

Accept exactly:

~~~text
$test-evidence-review --manifest {project-relative-path} --manifest-sha256 {sha256} [--persist]
~~~

Reject no-argument calls, direct test paths, story/system/sprint names, absolute paths, globs, latest-file selectors, unsafe paths, unknown or duplicate flags, missing values, and hashes not expressed as 64 lowercase hexadecimal characters. Never discover the current sprint or infer scope from directory names.

The input uses `schema: cgs-test-evidence-review-manifest/v2`. It is the sole review-scope authority. On invalid or ambiguous input, write nothing and return `Workflow Status: BLOCKED`.

## Versioned workflow contract

Freeze this contract before reading project evidence:

~~~yaml template
schema: cgs-test-evidence-review-workflow-contract/v1
input_schema: cgs-test-evidence-review-manifest/v2
stage_schema: cgs-project-stage-manifest/v1
session_schema: cgs-active-session-manifest/v1
qa_plan_schema: cgs-qa-plan/v2
candidate_schema: cgs-build-candidate/v1
build_receipt_schema: cgs-build-receipt/v1
output_schema: cgs-test-evidence-review-report/v2
default_mutation: none
optional_mutation: one immutable report
~~~

Record the workflow contract schema and SHA-256 in any persisted report.

## Independent result axes

Never emit one overloaded verdict. Every review returns these fields:

| Field | Values | Meaning |
|---|---|---|
| `Workflow Status` | `COMPLETE`, `PARTIAL`, `BLOCKED` | Whether every declared row was evaluated |
| `Structural Quality` | `ADEQUATE`, `INCOMPLETE`, `MISSING`, `UNAVAILABLE`, `UNKNOWN` | Requirement-to-observable quality and provenance |
| `Evidence Admissibility` | `ADMISSIBLE`, `LIMITED`, `INADMISSIBLE`, `UNAVAILABLE`, `UNKNOWN` | What the supplied evidence type may prove |
| `Execution Result` | `PASS`, `FAIL`, `UNKNOWN` | Current-build product outcome only |
| `Execution Currency` | `CURRENT`, `STALE`, `UNAVAILABLE`, `UNKNOWN` | Whether execution bindings match current authorities |
| `Execution Completeness` | `COMPLETE`, `PARTIAL`, `NONE`, `UNKNOWN` | Whether all required runtime rows are conclusive |
| `Execution Scope` | `FULL`, `TARGETED`, `NONE`, `UNKNOWN` | Scope proven by runtime evidence |
| `Closure Eligible` | `YES`, `NO` | Whether every required condition supports closure |
| `Persistence` | `NOT_REQUESTED`, `WRITTEN`, `DECLINED`, `FAILED`, `NOT_ATTEMPTED` | Optional report outcome only |

`COMPLETE` means the review classified every declared row; it does not mean quality or execution passed. `ADEQUATE` does not mean a test ran. `PASS` does not mean the test is meaningful. A structurally adequate test with no current-build receipt is exactly `Structural Quality: ADEQUATE`, `Execution Result: UNKNOWN`, `Execution Currency: UNKNOWN`, `Execution Completeness: NONE`, and closure NO.

## Canonical review manifest

The manifest binds one deterministic review identity:

- review ID, schema, creation identity, canonicalization version, and expected scope SHA-256;
- scope type `story`, `sprint`, or `system`, plus one stable scope ID;
- exact project-stage manifest path/hash and active-session manifest path/hash;
- exact QA-plan path/hash, plan ID, scope ID/hash, source-span hash, ownership hash, and dependency hash;
- exact candidate path/hash, candidate ID, build ID, artifact SHA-256, source commit, engine, platform, and configuration;
- exact build-receipt path/hash and verification identity;
- exact test naming-schema path/hash;
- ordered scope rows;
- a typed evidence registry;
- exact attester-registry or external identity-verification path/hash when attestations are required;
- explicit input byte/file/row budgets;
- optional report destination with the required `ABSENT` precondition.

Each scope row has:
- stable Scope Row ID, Story ID, Requirement ID, Acceptance Criterion ID, Coverage Unit ID, and QA-plan Test/Check ID;
- story/requirement source path/hash and relevant-source-set hash;
- method, expected observable, failure condition, owner, risk, platform/configuration, and required execution scope;
- ordered required Evidence IDs and allowed evidence-type combinations;
- exact test-source and metadata path/hash where applicable;
- explicit required attestation policy.

Reject duplicate stable IDs, one Test ID assigned ambiguously to incompatible ACs, missing requirement bindings, conflicting paths, and rows not present in the exact QA plan. Preserve canonical row order and compute the scope hash over IDs, methods, observables, owners, evidence contracts, paths, and declared hashes.

## Phase 1: Resolve the unique stage, session, and sprint scope

Hash raw manifest bytes before parsing and reject duplicate keys. Resolve literal real paths within the project root. Reject missing regular files, path escapes, unexpected symlinks, directories, device files, oversize inputs, and unsupported encodings.

Read the exact project-stage and active-session manifests declared by the review manifest. If scope type is `sprint`, require:
- exactly one active sprint ID in the session manifest;
- the same sprint ID and tracker identity in the stage manifest, review manifest, and QA plan;
- current stage/session statuses and matching source hashes;
- no second active sprint and no unresolved active-scope conflict.

For story or system scope, require its stable ID and parent sprint/stage context to be explicit; never select a sprint by modification time. A missing, stale, ambiguous, or multiply active scope makes `Workflow Status: BLOCKED`, all evidence/execution axes UNKNOWN or UNAVAILABLE as appropriate, closure NO, and persistence NOT_ATTEMPTED.

## Phase 2: Revalidate requirement, build, and source bindings

Read and hash the exact QA plan. Require `cgs-qa-plan/v2`, `Plan Status: CURRENT`, `Effective Status: CURRENT`, and `Scope Completeness: COMPLETE`. Re-hash every captured requirement, story, GDD, ADR, control, test source, helper contract, naming schema, candidate, build receipt, test manifest, and evidence source relevant to each row.

The candidate and build receipt must agree exactly on candidate ID, build ID, artifact path/hash, source commit, engine/version, platform, configuration, producer identity, status, and completeness. Re-hash a local artifact; for a remote artifact require a verifiable signed or issuer-bound receipt.

Each row's Story, Requirement, AC, Coverage Unit, and Test/Check IDs must match the QA plan and evidence metadata exactly. A filename, comment, similar description, test discovery result, or directory position cannot create a requirement binding.

Compute `relevant_source_set_sha256` from canonical tuples of path, media type, byte count, and raw hash. Any relevant byte change invalidates dependent evidence immediately:
- a readable hash or identity mismatch is `STALE`;
- an explicitly absent required artifact is `MISSING`;
- a declared artifact that cannot be read, parsed, decoded, or verified is `UNAVAILABLE`;
- an undeclared or indeterminate state is `UNKNOWN`;
- a partly valid receipt or evidence set is `PARTIAL`.

Dates, sprint start, modification time, and newer-looking filenames never restore currentness.

## Phase 3: Apply typed evidence admissibility

Every evidence item has a stable Evidence ID, type, path, raw SHA-256, media type, byte count, producer, timestamp, subject IDs, build binding where applicable, and admissibility contract ID.

Use this evidence-type registry:

| Evidence Type | May establish | Cannot establish alone | Minimum binding |
|---|---|---|---|
| `QA_PLAN_MAPPING` | planned requirement/test mapping | structure quality or execution | plan/scope/source hashes and stable IDs |
| `TEST_SOURCE` | inspectable structure and observable semantics | execution | Requirement/AC/Test IDs and source hash |
| `HELPER_CONTRACT` | helper observable semantics | execution or calling-test sensitivity | helper path/hash and stable observable ID |
| `NEGATIVE_CONTROL_RECEIPT` | failure sensitivity | current product PASS | exact source, requirement, mutation/control and tool hashes |
| `MUTATION_RECEIPT` | failure sensitivity against a defined change | current product PASS unless separately current-build bound | mutation ID, source/build/test IDs and complete receipt |
| `EXECUTION_RECEIPT` | current product PASS/FAIL | structural adequacy | exact candidate/build/source/test/scope/runner hashes |
| `MANUAL_ARTIFACT` | visible or recorded observable | approval or automated execution | artifact receipt, AC/build/platform/capture binding |
| `ARTIFACT_RECEIPT` | artifact provenance and integrity | artifact content truth | artifact hash/size/type, capture identity and method |
| `PLAYTEST_RESULT` | verified session observations | automated test execution | canonical completed result and all referenced hashes |
| `ATTESTATION` | authorized reviewer statement | underlying fact without reviewed evidence | identity/time/scope/build/evidence hashes and authorization source |
| `BUILD_RECEIPT` | build provenance | test execution | candidate/build/artifact/source/platform binding |

A row may combine types only as allowed by its manifest contract. Evidence is:
- `ADMISSIBLE` when type, required fields, exact subjects, hashes, currentness, verifier, and intended axis all match;
- `LIMITED` when valid evidence proves only a declared narrower axis or targeted scope;
- `INADMISSIBLE` when the type is being used to prove a prohibited claim or has a conclusive contract mismatch;
- `UNAVAILABLE` when declared bytes or verifier cannot be accessed;
- `UNKNOWN` when admissibility cannot be determined from declared metadata.

Path presence proves only `Presence: PRESENT`. It never establishes content, currentness, approval, or execution.

## Phase 4: Review automated structural quality semantically

For every automated or combined-method row, inspect exact source bytes and any declared metadata/helper contracts. Evaluate:

1. Stable mapping from Requirement, AC, Coverage Unit, and Test ID to the expected observable.
2. Setup and stimulus that actually exercise the requirement.
3. Assertion or observation semantics that trace to the expected state, event, output, invariant, boundary, or formula.
4. Failure sensitivity: why removal, inversion, boundary violation, or fault injection would fail.
5. Independence from equivalent duplicate assertions and hidden helper behavior.
6. Determinism and isolation risks actually evidenced by time, randomness, shared state, external I/O, order, concurrency, or environment dependence.
7. Required boundary, fault, negative, and formula cases from stable requirement IDs and QA rows.

Never count tokens or lines containing assert, expect, check, or verify. Comments, strings, names, repeated equivalent assertions, and opaque helper calls are not semantic proof. A helper counts only when its exact implementation or contract is hash-bound and inspected. One high-information, failure-sensitive observation may be stronger than many repetitions.

Assign row Structural Quality:
- `ADEQUATE` only when stable mapping, observable semantics, and failure sensitivity are demonstrated with no blocking structural gap;
- `INCOMPLETE` when sources exist but semantics, coverage, independence, or provenance is insufficient;
- `MISSING` only for an explicitly absent required structural artifact;
- `UNAVAILABLE` when declared material cannot be inspected;
- `UNKNOWN` when the manifest does not permit a determination.

## Phase 5: Validate canonical test naming independently

Read the exact hash-bound canonical naming schema declared by the review manifest. It must define stable `system`, `scenario`, and `expected` fields and an unambiguous parser or metadata encoding for repository test names.

A valid name represents `test_{system}_{scenario}_{expected}` according to that exact schema. Missing or ambiguous system/scenario/expected produces a stable naming finding. Do not heuristically split underscore text, invent a system, or infer Requirement/AC coverage from a name.

Naming is a maintainability subfinding only. A conforming name cannot improve Structural Quality without semantic mapping; a nonconforming name cannot erase otherwise demonstrated coverage.

## Phase 6: Inspect manual, visual, log, UI, and playtest evidence

For each manual artifact, verify its `ARTIFACT_RECEIPT` and raw bytes. Require stable Story/Requirement/AC/Check IDs, candidate/build/artifact/source, platform/device/OS/runtime/configuration/input, artifact path/hash/type/size, capture time/method, captor/observer identity, reproducible setup, expected observable, and privacy/redaction class.

Inspect actual content with an appropriate decoder or viewer:
- an image must visibly demonstrate the AC state;
- a walkthrough must preserve ordered actions and observed results;
- a log must include the relevant bounded event/result and parser context;
- UI evidence must identify screen/state/input/platform and observable result.

A filename, caption, path, field being nonempty, or date alone is never content proof. An undecodable artifact or unavailable viewer is UNAVAILABLE, not MISSING or PASS.

For playtest evidence, require an exact current canonical completed result and every referenced manifest, observation ledger, raw artifact, and receipt hash. Derived findings must resolve to stable Observation IDs and raw evidence. A plan, protocol, ingest-only session, director review, legacy path, or summary is inadmissible as executed playtest evidence.

## Phase 7: Verify attestations without impersonation

A nonempty sign-off field or role label is not an attestation. Require a separate typed `ATTESTATION` record binding:
- verifier-supported reviewer identity and authorized role;
- timestamp and validity interval;
- exact review scope, Story/Requirement/AC/Check IDs;
- candidate/build/artifact/source identities;
- exact reviewed evidence paths/hashes;
- attestation statement, result, and policy ID;
- attester-registry path/hash or external verification receipt.

Verify authorization for the exact scope. A mismatch, expired authorization, stale source/evidence hash, unverifiable identity, or out-of-scope statement is INADMISSIBLE or INCOMPLETE and blocks closure.

The model must never create, complete, copy forward, or sign an attestation on behalf of any person or role.

## Phase 8: Verify current execution independently

For every row requiring runtime evidence, consume only the exact typed `EXECUTION_RECEIPT` declared by Evidence ID. Validate its schema adapter and all referenced raw bytes. A current receipt binds:
- candidate manifest and build receipt paths/hashes;
- candidate/build/artifact/source identities;
- QA plan, scope, requirement, AC, Coverage Unit, Test/Check IDs;
- test execution manifest, runner/version, ordered argv, cwd, deterministic controls;
- platform/configuration and required device identity;
- timestamps, result rows, parser, logs, completeness, and receipt hash;
- immutable persistence/read-back state when the producer contract requires it.

A `cgs-smoke-check-receipt/v2` is admissible only from the canonical candidate/run evidence root, with exact selected-scope hash and all indexed member hashes verified. Sprint PASS may establish FULL execution scope; quick TARGETED CHECK PASSED can establish only the exact targeted rows and never full closure.

Other execution receipt types require a registered schema adapter with the same exact build, scope, result, completeness, and hash guarantees. A generic CI success, console text, newest report, selected test list, QA plan, or user claim cannot establish execution.

Map per row:
- `Execution Result: FAIL` only from a current admissible conclusive failure;
- `Execution Result: PASS` only from a current admissible conclusive pass;
- otherwise `Execution Result: UNKNOWN`.
- `Execution Currency: CURRENT` only when every binding/hash is current; readable mismatch is STALE; unreadable required binding is UNAVAILABLE; no determinate receipt is UNKNOWN.
- `Execution Completeness: COMPLETE` only when every required result row/log/parser record is present and conclusive; some valid rows plus gaps is PARTIAL; no receipt is NONE; indeterminate membership is UNKNOWN.
- `Execution Scope: FULL` only when exact required full scope is proven; exact subset is TARGETED; no execution is NONE; indeterminate scope is UNKNOWN.

Structural quality never changes these fields.

## Phase 9: Create stable findings and per-AC results

Use versioned rule IDs, including:
- `TER-R-SCOPE-001` ambiguous active scope;
- `TER-R-BIND-001` requirement/build/hash mismatch;
- `TER-R-ADMIT-001` inadmissible evidence type;
- `TER-R-STRUCT-001` missing semantic observable;
- `TER-R-SENSE-001` failure sensitivity unproven;
- `TER-R-NAME-001` canonical naming mismatch;
- `TER-R-ATTEST-001` invalid attestation;
- `TER-R-EXEC-001` no conclusive current execution;
- `TER-R-STALE-001` relevant bytes changed;
- `TER-R-UNAVAIL-001` declared evidence cannot be inspected;
- `TER-R-PARTIAL-001` evidence or execution set incomplete.

For every finding compute a deterministic fingerprint over:
`workflow-contract hash | review scope hash | Scope Row ID | Requirement ID | AC ID | Evidence ID or none | axis | rule ID | observed identity/hash`.

Finding ID is `TER-F-{first-16-hex-of-fingerprint}`. Store the full SHA-256 fingerprint, severity `BLOCKER|MAJOR|MINOR|INFO`, axis, rule ID, stable subjects, observed/expected values, evidence references, and owning role. Sort findings by Scope Row ID, axis, rule ID, Evidence ID, then fingerprint. Rerunning unchanged bytes yields identical IDs and order.

Emit exactly one result row for every declared AC:

| Scope Row ID | Story ID | Requirement ID | AC ID | Test/Check ID | Method | Presence | Structural Quality | Evidence Admissibility | Execution Result | Execution Currency | Execution Completeness | Execution Scope | Attestation | Blocking Finding IDs | Closure Eligible |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Never omit a row because an input is unreadable. Mark the appropriate fields UNAVAILABLE/UNKNOWN/PARTIAL and attach stable findings.

## Phase 10: Aggregate with one deterministic decision table

Aggregate without hiding row states:

1. `Workflow Status: BLOCKED` for invalid or ambiguous review scope; otherwise PARTIAL when any declared row could not be fully inspected; otherwise COMPLETE.
2. Structural Quality is MISSING if any required structural artifact is explicitly absent; otherwise UNAVAILABLE if any is unreadable; otherwise UNKNOWN if any row cannot be determined; otherwise INCOMPLETE if any structural gap exists; otherwise ADEQUATE.
3. Evidence Admissibility is INADMISSIBLE if any required evidence is conclusively prohibited or mismatched; otherwise UNAVAILABLE if required evidence cannot be accessed; otherwise UNKNOWN if indeterminate; otherwise LIMITED if any required claim is proven only narrowly; otherwise ADMISSIBLE.
4. Execution Result is FAIL if any current admissible required row conclusively fails; otherwise UNKNOWN unless every required row conclusively passes; otherwise PASS.
5. Execution Currency is STALE if any required readable binding changed; otherwise UNAVAILABLE if any required binding cannot be read; otherwise UNKNOWN if any required currency is indeterminate; otherwise CURRENT.
6. Execution Completeness is NONE when no runtime receipt exists for any required row; otherwise UNKNOWN when expected membership is indeterminate; otherwise PARTIAL when any required row or record is nonconclusive/missing; otherwise COMPLETE.
7. Execution Scope is FULL only when every row's required full scope is current and conclusive; otherwise TARGETED when all available conclusive execution is an exact subset; otherwise NONE when no execution exists; otherwise UNKNOWN.
8. Closure Eligible is YES only when Workflow COMPLETE, Structural ADEQUATE, Admissibility ADMISSIBLE, Execution PASS/CURRENT/COMPLETE with required FULL scope, all required attestations verify, and no blocking finding exists. Otherwise NO.

These axes are the only review decision vocabulary. Do not append `PASS/WARNINGS/FAIL`, `ADEQUATE/INCOMPLETE/MISSING` as a single verdict, or `COMPLETE/CONCERNS` as a second verdict.

## Phase 11: Present a read-only result

Always present:
- review manifest path/hash, workflow contract hash, Review ID, Scope ID, and scope SHA-256;
- stage/session/sprint identities and hashes;
- QA plan, candidate, build receipt, artifact, source-set, naming schema, evidence-registry, and attester-registry hashes;
- complete per-AC table;
- stable findings with rule IDs and fingerprints;
- structural, admissibility, execution, currentness, completeness, scope, attestation, and persistence sections;
- aggregate axes and Closure Eligible;
- exact remediation owner for every blocker.

Without `--persist`, write nothing, return `Persistence: NOT_REQUESTED`, and list zero owned write paths. The review describes underlying evidence but is not itself a durable closure receipt.

## Phase 12: Optionally CAS-persist one immutable report

The only owned output is:

~~~text
production/qa/evidence/reviews/{review-id}-{first-12-hex-of-scope-sha256}/report.md
~~~

Reject an existing directory or report. Never overwrite, append, choose a date-only filename, or update a latest pointer.

Before writing, preview the exact one-file CREATE operation, byte count, report SHA-256, all non-writes, aggregate axes, closure result, and persistence consequence. If persistence was not already authorized, obtain one explicit approval. A decline preserves every observed review result, sets `Persistence: DECLINED`, and makes the review report unavailable as durable evidence.

For an authorized write:
1. re-read and re-hash the manifest and every stage, session, QA, requirement, candidate, build, test, evidence, naming, adapter, and attestation input;
2. compare all identities and hashes with the frozen snapshot;
3. require the final directory and report still absent;
4. render the complete `cgs-test-evidence-review-report/v2` in private same-filesystem staging;
5. validate stable finding IDs, per-AC row count, internal references, and report hash;
6. compare-and-swap unchanged inputs and absent destination;
7. atomically publish the one report without overwrite;
8. read back bytes, re-hash, and validate the schema/header.

On drift, collision, write failure, or read-back mismatch, report `Persistence: FAILED`, preserve the observed axes and findings, set the persisted-review receipt availability to NO, and never claim the report was written.

The persisted report header includes:
- artifact/schema/review/scope/workflow-contract identities and hashes;
- exact stage/session/sprint, QA plan, candidate/build/artifact/source, evidence registry, and input-set hashes;
- Workflow Status, Structural Quality, Evidence Admissibility, Execution Result, Execution Currency, Execution Completeness, Execution Scope, Closure Eligible, and Persistence;
- stable findings-set SHA-256;
- report body canonicalization version.

A downstream consumer receives the exact report path and SHA-256 plus review scope, candidate, build, artifact, and input-set hashes. It must re-hash the report and referenced authorities. It must not use a newest report, conversation summary, or Persistence other than WRITTEN.

## Required invariants

- Active scope comes only from exact stage/session manifests, never recent files.
- Every AC row binds stable requirement, test/check, build, and evidence identities.
- Evidence type and admissibility limit what each artifact may prove.
- File presence and token counts cannot establish quality or execution.
- Structural quality and current execution remain independent.
- Relevant source byte changes make dependent evidence stale.
- Missing, unavailable, partial, stale, and unknown states remain distinct.
- The model never fabricates or impersonates a signatory.
- Naming conformance is independent and cannot prove coverage.
- Stable rule IDs and hash fingerprints make findings reproducible.
- Default operation is byte-for-byte read-only.
- Optional persistence creates one immutable CAS-verified report only.



## P1 audit traceability

This table is trace metadata only; it does not add behavior. Each row binds one audit ID to the exact enforcing clause and dedicated-spec assertion set.

| Audit ID | Enforcing SKILL clause | Dedicated spec case and assertions |
|---|---|---|
| TER-004 | Phase 1 — stage/session authority selects one declared active sprint; timestamps/newest directories are forbidden | Case 1; TER-STA-003, TER-STA-004, TER-PRO-001, TER-PRO-002 |
| TER-005 | Canonical review manifest + Phase 2 — every row binds stable Story/Requirement/AC/Coverage Unit/Test/build/evidence identities and hashes | Case 2; TER-STA-005, TER-STA-006, TER-PRO-002, TER-PRO-005 |
| TER-006 | Phase 4 — semantic observable and failure sensitivity, never names/comments/token counts, establish structural coverage | Case 3; TER-STA-007, TER-STA-017, TER-PRO-005 |
| TER-007 | Phase 7 — attestation requires verified identity, time, scope, build, hashes, statement, result, and authority; the model never signs | Case 4; TER-STA-008, TER-PRO-006 |
| TER-008 | Phase 2 — exact relevant source-set hashes determine currency; dates/sprint start/mtime cannot restore freshness | Case 5; TER-STA-009, TER-PRO-008 |
| TER-009 | Phases 9–10 — every AC row persists and missing/unavailable/partial/stale/unknown remain distinct | Case 6; TER-STA-010, TER-STA-020, TER-PRO-003, TER-PRO-007 |
| TER-010 | Independent result axes + Phase 10 — workflow status, quality, execution, closure, and persistence use one deterministic multi-axis table, with no second verdict | Case 7; TER-STA-011, TER-STA-012, TER-STA-019 |
| TER-015 | Phase 5 — canonical naming parses stable system/scenario/expected fields; failure is only a naming finding and never coverage | Case 8; TER-STA-013, TER-STA-014, TER-PRO-005 |
| TER-016 | Purpose/authority, invocation, independent axes, Phases 11–12 — one evidence-review manifest interface, read-only default, optional authorized report, no code-quality substitute | Case 9; TER-STA-001–TER-STA-024 and TER-PRO-001–TER-PRO-015 |
