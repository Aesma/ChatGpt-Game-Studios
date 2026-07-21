---
name: release-checklist
description: "Normalizes exact release-candidate evidence into an immutable checklist with PASS, FAIL, UNKNOWN, or authorized N/A per stable item; it does not issue the release gate verdict."
---

## Invocation and ownership

Invoke only as:

~~~text
$release-checklist --manifest {release-candidate-manifest-path}
~~~

The manifest is mandatory. Reject platform-only arguments, unknown or duplicate flags, missing values, directories, unsafe paths, and positional release/version names. Do not infer the current release, latest build, newest checklist, target platform, or evidence location.

This workflow is an evidence collector and normalizer. It owns one immutable report:

~~~text
production/releases/{release-id}/{release-manifest-sha256}/release-checklist.md
~~~

The path digest segment is the full 64-character lowercase hexadecimal release-manifest SHA-256 without a prefix; never shorten it.

It never edits the release/build manifest, source, tests, bugs, QA evidence, legal/cert/store receipts, changelog, milestone, release policy, session state, or prior reports. It never invokes gate-check, team-release, changelog, a director, or another workflow.

An explicit bounded request authorizes the one report write. Otherwise, present the exact one-file CREATE changeset and obtain one explicit approval before writing. Reject an existing target rather than overwriting it. Evidence changes require a new release manifest hash and report path.

## Result and authority vocabulary

This workflow does not emit RELEASE READY, RELEASE BLOCKED, CONCERNS, GO, NO-GO, or any other release-readiness verdict. The release gate owner consumes this report and applies the named release policy.

Report independently:

- Workflow Status: COMPLETE, PARTIAL, or BLOCKED
- Item Status: PASS, FAIL, UNKNOWN, or N/A
- Persistence: WRITTEN, DECLINED, FAILED, or NOT_ATTEMPTED
- Gate Decision: NOT EVALUATED

Meanings:

- PASS(evidence): verified authoritative evidence positively satisfies the exact item policy for this release candidate;
- FAIL(evidence): verified authoritative evidence conclusively violates the exact item policy for this release candidate;
- UNKNOWN(owner): evidence is absent, unreadable, stale, mismatched, inconclusive, unauthorized, or not machine-verifiable; name the accountable owner;
- N/A(rationale): the signed/verified policy authority says the item does not apply to this release/platform and binds that rationale to the item, policy, release, candidate, and expiry.

File existence, a checkbox, filename, recent modification time, model inference, empty answer, role label, or unsigned statement can never produce PASS or N/A.

Workflow Status is COMPLETE when every policy item was evaluated into one of the four statuses, even when FAIL items exist. It is PARTIAL when one or more declared inputs could not be read or inspected and therefore some evaluations are unavailable. It is BLOCKED when release identity, policy, or scope cannot be uniquely established or persistence authorization/concurrency prevents the required report. These operation states are not release decisions.

## Phase 1: Validate release identity, policy, and instructions

Resolve the manifest literal path and real path. Reject symlinks escaping the project root, malformed syntax, duplicate keys, unsupported schema, dot segments, and paths outside the project root. Read raw bytes once and compute SHA-256 over exact bytes.

Require:

- Artifact Type: release-candidate-manifest
- Schema Version: 1
- stable release ID and semantic/display version;
- target platform/configuration matrix;
- exact build-candidate manifest path and SHA-256;
- candidate ID, build ID, build artifact path/hash, source commit, and release tag or immutable source ref;
- exact release-policy path/hash and policy version;
- ordered evidence index keyed by stable release item ID;
- exact applicable AGENTS.md path/hash chain;
- optional previous checklist path/hash, never a newest-file search;
- generated-at timestamp and manifest owner.

Validate the build-candidate manifest against the staged smoke-check identity contract: Artifact Type: build-candidate, candidate/build/artifact/source/platform identity, QA-plan path/hash, and test-manifest path/hash must match the release manifest. Re-hash the local build artifact; a remote artifact requires a trusted build receipt binding the same identity.

Read in full every applicable AGENTS.md from project root through the report target. Re-hash the declared chain and apply closest-file precedence. A missing or conflicting instruction, invalid release ID, candidate mismatch, artifact mismatch, missing policy, or ambiguous scope returns Workflow Status: BLOCKED, Persistence: NOT_ATTEMPTED, Gate Decision: NOT EVALUATED, and writes nothing.

### Release policy

The hash-bound policy must define, for every stable item ID:

- title, category, target platforms, required/optional condition, and accountable owner;
- authoritative evidence artifact type/schema and allowed producer/verifier;
- exact machine-evaluable pass and fail conditions;
- whether UNKNOWN blocks the later gate;
- N/A authority, required rationale/attestation fields, and expiry rule;
- hard-gate/advisory classification for the downstream gate owner;
- canonical bug severity mapping and any allowed waiver authority;
- required evidence dependencies and cross-item rules.

Do not invent checklist items or criteria. Preserve every ordered policy item, including items with missing evidence.

## Phase 2: Load only indexed evidence

For each policy item, load only the exact evidence-index entries from the release manifest. Every entry requires path, raw-byte SHA-256, Artifact Type, Schema Version, producer/issuer, generated or observed timestamp, candidate/build/platform binding, result fields, and referenced-artifact hashes.

Normalize and resolve every literal/real path. Apply per-item file/byte limits from policy. Do not scan arbitrary CI/log/test directories, source trees, bug folders, milestone folders, store folders, or the internet. Do not select by modification time.

Re-hash every artifact and recursively verify every policy-required referenced artifact. Classify evidence state separately:

- CURRENT: all identities, bytes, schemas, references, timestamps/expiry, producers, and verifiers satisfy policy;
- STALE: readable evidence or a referenced source is for another manifest/build/commit/platform/config or its hash changed;
- UNAVAILABLE: a declared path cannot be read, parsed, decoded, or verified;
- MISSING: no evidence index entry was supplied for a required item;
- INVALID: schema, identity, producer, signature, receipt, or internal references are malformed/inconsistent.

STALE, UNAVAILABLE, MISSING, INVALID, and inconclusive evidence map to Item Status: UNKNOWN unless a separate current authoritative artifact conclusively proves FAIL. Never reuse an older candidate's PASS.

### Human/platform authority receipts

Legal approval, privacy, ratings, platform certification, store configuration, pricing, first-party submission, and named sign-offs require a current authoritative receipt or attestation. It must bind:

- stable item/release/candidate/build/platform IDs;
- exact reviewed artifact paths/hashes and scope;
- authorized identity/role or trusted issuer;
- result, timestamp, expiry, and external reference/job/submission ID;
- signature or hash-bound identity-verification receipt;
- policy path/hash and, for N/A, explicit rationale.

A nonempty name, role label, checked box, or model statement is not approval. The model never signs, assumes legal compliance, certifies a platform result, or grants N/A.

## Phase 3: Validate canonical technical and experience evidence

All dependent artifacts must bind the exact release candidate. A finalized artifact is not automatically a passing artifact.

### Smoke evidence

Accept only the exact indexed canonical report:

~~~text
production/qa/evidence/smoke/{candidate-id}/{run-id}/report.md
~~~

Require Artifact Type: smoke-check-receipt, Schema Version: 1, exact candidate-manifest path/hash, build/source/platform identity, exact QA-plan/test-manifest/scope hashes, Persistence: WRITTEN, sprint mode, Verdict: PASS, Handoff Eligible: YES, and revalidated QA Plan Effective State: CURRENT. Re-hash the candidate manifest, QA-plan captured sources, test manifest, automated receipt/log, manual evidence, and report.

A quick, targeted, INCOMPLETE, FAIL, warning-bearing, stale, unknown, unpersisted, or newest-file-selected receipt cannot yield item PASS. A current conclusive smoke FAIL yields item FAIL when the policy item's fail condition matches; other nonpassing states are UNKNOWN.

### Regression evidence

Require both:

1. the exact current hash-bound regression selection manifest whose QA-plan provenance revalidates CURRENT and whose required stable tests have current mappings and failure-sensitivity receipts; and
2. an exact execution receipt bound to that selection-manifest hash, release build/commit, runner/config, every active stable test ID, test-source hashes, requirement IDs, results, and complete log/receipt hash.

Selection alone never yields PASS. PASS requires every required active stable test to have a current passing result and current sensitivity evidence. A current conclusive required test failure yields FAIL. GAP, STALE, AWAITING RUN, INDETERMINATE, quarantine without a policy-authorized disposition, or missing receipt yields UNKNOWN.

### Soak evidence

Accept only the exact indexed canonical result:

~~~text
production/qa/soak-tests/{run-id}/result.md
~~~

Require Artifact Type: soak-test-result, Schema Version: 1, Status: COMPLETED, exact build/source/platform, workload/environment IDs and hashes, observer/timestamps, protocol/manifest/raw/sample hashes, and all referenced receipts. Verdict: COMPLETE proves artifact finalization only.

Item PASS requires Execution Status: EXECUTED, Gate Eligible: YES, Readiness Result: PASS, and every policy-required stability/memory/performance/experience dimension PASS or policy-authorized NOT_IN_SCOPE. A current Readiness Result: FAIL or required dimension FAIL yields FAIL. FAILED_EARLY may yield FAIL only when the canonical result records a verified objective failure allowed by policy. INCOMPLETE, INCONCLUSIVE, profile mismatch, insufficient duration/checkpoints, or hash mismatch yields UNKNOWN.

### Playtest evidence

Accept only exact indexed canonical completed reports:

~~~text
production/playtests/{session-id}/report.md
~~~

Require Artifact Type: playtest-session-result, Schema Version: 1, Status: COMPLETED, Gate Eligible: YES, exact build/source/platform/hypothesis or AC binding, participant/timestamps, evidence receipt, raw/manifest/observation-ledger hashes, and derived-finding links to stable Observation IDs.

Protocols, templates, ingest-only sessions, director reviews, legacy locations, malformed reports, and duplicate session IDs do not count. A policy may define machine-evaluable evidence-completeness conditions such as distinct completed session count/profile coverage. The model cannot translate a subjective finding or director interpretation into release approval. Unresolved or ambiguous product decisions remain UNKNOWN for their owning item.

### Test-evidence review

Accept only an exact persisted report at:

~~~text
production/qa/evidence/reviews/{review-id}/report.md
~~~

Require Artifact Type: test-evidence-review-report, Schema Version: 1, matching candidate/QA-plan/source hashes, Workflow Status: COMPLETE, Overall Evidence Quality: ADEQUATE, Overall Execution Status: PASS, required Execution Scope: FULL, Closure Eligible: YES, Persistence: WRITTEN, and one unique eligible row per required stable AC/check ID. Re-hash all referenced smoke, playtest, test-source, helper-contract, artifact, attestation, and identity receipts.

Conversation-only, PARTIAL, UNKNOWN, STALE, UNAVAILABLE, targeted-only, or hash-mismatched reviews cannot yield item PASS.

## Phase 4: Normalize remaining policy evidence

Use the same exact-evidence rule for every other item.

Examples:

- Build/reproducibility: require a structured build receipt bound to artifact hash, source commit/tag, toolchain/container/config hashes, argv, exit code, timestamps, complete log hash, and reproduction comparison.
- Bug state: require an authoritative bug-registry snapshot path/hash bound to the release scope. Use canonical severities S1 Critical, S2 Major/High, S3 Moderate/Medium, and S4 Minor/Low only through the policy's explicit mapping. An open current S1/S2 produces FAIL when policy says so. A waiver never silently changes FAIL; record its exact authority/scope/expiry for the downstream gate unless policy explicitly defines an authorized N/A.
- Story/milestone completion: require stable story IDs, current story/source hashes, completion receipts, and exact release-scope manifest. A milestone filename or status label alone is insufficient.
- Changelog: require exact path/hash, release/version ID, source commit range, generator/owner, and policy-required approval. Mere existence is UNKNOWN.
- Code-health/TODO scan: require a structured bounded scan receipt with commit, included/excluded paths, tool/version/config, exit code, complete result/log hashes, and policy thresholds. Do not perform an unbounded ad hoc source scan.
- Assets/performance/localization/content: require exact candidate-bound receipts and authoritative thresholds from policy.
- Store/legal/cert/launch operations: require the human/platform authority receipts from Phase 2.

For each item record:

| Item ID | Category | Policy Class | Owner | Evidence State | Item Status | Evidence Paths + SHA-256 | Candidate Binding | Result/Reason | N/A Authority |
|---|---|---|---|---|---|---|---|---|---|

Assign exactly one status. Never leave a blank checkbox or treat silence as PASS.

## Phase 5: Aggregate deterministically and compare an exact predecessor

Report counts of PASS, FAIL, UNKNOWN, and N/A plus hard-gate/advisory classifications, but do not turn them into a release verdict.

- Workflow Status is PARTIAL if any indexed artifact or required referenced artifact was UNAVAILABLE and could not be evaluated.
- Otherwise Workflow Status is COMPLETE after every policy item has one normalized status.
- Any invalid release identity/policy/scope remains BLOCKED.
- Gate Decision is always NOT EVALUATED.

If the manifest provides a previous checklist path/hash:

1. verify its Artifact Type, schema, report hash, prior release/candidate/policy identity, and stable item IDs;
2. compare current and prior rows by exact Item ID;
3. report status/evidence-hash transitions as RESOLVED, REGRESSED, CHANGED, UNCHANGED, ADDED, or REMOVED;
4. keep prior evidence from affecting current status;
5. mark comparison unavailable if the prior report is unreadable or mismatched rather than searching for another report.

The same manifest, policy, and evidence bytes must produce the same ordered item IDs, statuses, reasons, summary counts, and delta.

## Phase 6: Generate and persist the immutable report

Start with:

~~~text
Artifact Type: release-evidence-checklist
Schema Version: 1
Release Manifest Path: {path}
Release Manifest SHA-256: sha256:{digest}
Release ID: {release-id}
Release Version: {version}
Release Policy Path: {path}
Release Policy SHA-256: sha256:{digest}
Candidate Manifest Path: {path}
Candidate Manifest SHA-256: sha256:{digest}
Candidate ID: {candidate-id}
Build ID: {build-id}
Build Artifact SHA-256: sha256:{digest}
Source Commit: {commit}
Target Platforms: {platform/configuration matrix}
Generated At: {ISO-8601}
Workflow Status: COMPLETE | PARTIAL | BLOCKED
PASS Count: {n}
FAIL Count: {n}
UNKNOWN Count: {n}
N/A Count: {n}
Gate Decision: NOT EVALUATED
Persistence: WRITTEN
~~~

Include the loaded AGENTS chain/hashes, evidence inventory/currentness, complete ordered item table, failures, unknowns with owners, N/A authorities, policy classifications, exact predecessor delta, omitted/unavailable inputs, and downstream consumer requirements.

Preview the exact report bytes and one CREATE operation. The embedded Persistence: WRITTEN field becomes valid only after the atomic write and read-back verification succeed; if they do not, no consumable report exists. Immediately before writing, re-hash the release manifest, policy, candidate/build, instructions, every evidence artifact/reference, and the absent target path. Abort on any change or target creation. Write atomically, re-read exact bytes, verify internal references/counts, and compute the report SHA-256.

On success return Persistence: WRITTEN and the verified path/hash. If approval is declined or write/read-back fails, report Workflow Status: BLOCKED and Persistence: DECLINED or FAILED; do not claim a durable checklist. Gate Decision remains NOT EVALUATED.

## Phase 7: Handoff contract

A downstream gate must receive the exact report path/hash, release-manifest path/hash, release-policy path/hash, candidate-manifest path/hash, and candidate/build identity. It must re-hash every evidence dependency and independently apply the named policy. It must treat UNKNOWN and PARTIAL according to that policy and must never infer a gate decision from file existence, counts alone, or this workflow's operation status.

Recommend the accountable owner for each FAIL, UNKNOWN, invalid N/A, or unavailable artifact. Do not auto-fix evidence, close bugs, create a changelog, solicit or fabricate sign-offs, or invoke the gate owner.
