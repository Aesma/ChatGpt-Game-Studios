---
name: test-flakiness
description: "Analyze homogeneous, identity-bound test run sets for nondeterminism. Produces an optional evidence report and quarantine proposal, but never modifies tests, CI, or the regression selection manifest and never treats sparse or heterogeneous results as confirmed flakiness."
---

## Invocation and execution

Invoke this workflow as `$test-flakiness`.

Arguments: `[run-set: manifest-path | status: report-path] [--persist]`. Treat
bracketed values as optional unless the workflow says otherwise.

Before the first file change, present the complete proposed changeset, listing
every file and intended modification, and obtain one explicit approval. After
approval, make all changes within that boundary continuously without asking
again file by file. If the scope expands materially, stop, present the revised
changeset, and obtain one new approval.

# Test Flakiness Analysis

A flaky test produces different outcomes across independent executions when the
code, test binary, runner configuration, platform, environment, and seed are the
same. Mixed PASS/FAIL text without that identity proof is not flakiness evidence.

This workflow analyzes a bounded run set. It does not run tests, retry tests,
change skip annotations, edit CI, or own the regression selection manifest.

**Optional owned output:**
`production/qa/flakiness/flakiness-report-[run-set-id]-[dataset-hash-prefix].md`

Without `--persist`, the workflow is read-only and returns the full analysis in
conversation.

## Ownership and non-writes

`$test-flakiness` may write only the optional analysis report after a complete
one-file changeset is approved. It never writes or modifies:

- `tests/regression-suite.md`; `$regression-suite` is its sole owner;
- test source, skip/ignore annotations, runner or CI configuration;
- run-set manifests, test results, build records, application receipts, or
  runner receipts;
- QA plans, stories, bugs, release records, session state, catalogs, or guides.

A quarantine proposal is advisory. Approval and application are a separate
changeset owned by the relevant test/CI owner. A persisted flakiness report is
not proof that quarantine was approved, applied, or verified.

---

## Phase 1: Validate the input contract

### 1.1 Supported inputs

- `run-set: [manifest-path]` — analyze one explicit run-set manifest.
- `status: [report-path]` — read an existing flakiness report plus referenced
  quarantine/application/runner receipts and report current state without
  writing.
- `--persist` — optionally persist the analysis report. It does not authorize
  quarantine application.
- No argument — ask for a run-set manifest path or an existing report path.
  Never auto-scan logs and never infer a write mode.

A legacy single CI-log path is not a valid run set. Explain that it must be
wrapped in a manifest with independent run identities. If it represents only one
run, return `INSUFFICIENT EVIDENCE`.

### 1.2 Run-set manifest requirements

Read the manifest as raw bytes and compute
`sha256:<64 lowercase hexadecimal characters>`. Require:

- stable `run_set_id`;
- explicit list of result/receipt paths;
- for every run:
  - unique `run_id`;
  - result path and raw-byte SHA-256;
  - commit SHA;
  - immutable build ID and test-binary hash;
  - runner name/version and runner/config hash;
  - engine version;
  - operating system, architecture, and target platform;
  - environment fingerprint for relevant variables/services/assets;
  - random seed and seed policy;
  - shard/order identity;
  - start/end timestamp;
  - attempt kind: independent, retry, aborted, or resumed;
  - clean-process/isolation evidence.

Missing or invalid identity fields make that run ineligible. Record it under
excluded evidence; never fill values from file timestamps or neighboring logs.

Read each referenced result as raw bytes, verify its captured digest, and use a
schema-aware parser for its declared format. A malformed, truncated, ambiguous,
or partially parsed result is excluded and yields `PARTIAL DATA`. Text searches
may help locate records but cannot establish a test result or run identity.

### 1.3 Stable test identity

Use the runner-qualified stable test ID recorded in the result/receipt. When the
test participates in the staged regression selection contract, preserve the
exact stable `TC-...` test ID and optional `RS-[stable-test-id]` selection ID.

Do not merge by display name, method name, source path, title, or parameterized
base name. Missing or duplicate stable IDs are `INVALID IDENTITY` and are not
included in flakiness statistics.

---

## Phase 2: Form homogeneous independent cohorts

Create a cohort key from the exact tuple:

`commit_sha + build_id + test_binary_hash + runner_version +
runner_config_hash + engine_version + os + architecture + target_platform +
environment_fingerprint + random_seed + seed_policy + shard/order identity`

Runs with any differing tuple field belong to different cohorts. Never aggregate
their outcomes into one failure rate.

Only `attempt_kind: independent` with distinct run IDs and verified
clean-process/isolation evidence counts toward sample size. Retries, resumed
attempts, aborted runs, duplicate receipts, and repeated parsing of the same
result are listed but excluded from the denominator.

For each stable test ID and cohort report:

- included independent run IDs;
- excluded run IDs and exact reasons;
- PASS, FAIL, ERROR, SKIP, ABORTED, and NOT-RUN counts;
- denominator: PASS + FAIL only;
- exact failure rate and 95% Wilson interval when denominator is at least 2.

ERROR, SKIP, ABORTED, and NOT-RUN are never silently converted to FAIL or PASS.
A cohort containing only one valid independent execution has no flakiness rate.

If PASS and FAIL occur only across different cohort keys, return
`HETEROGENEOUS EVIDENCE`. Investigate the changed identity field; do not label
the test flaky.

---

## Phase 3: Determine evidence verdicts

Assign one deterministic verdict per stable test ID and homogeneous cohort:

| Verdict | Required evidence |
|---|---|
| `INSUFFICIENT EVIDENCE` | Fewer than 2 valid independent PASS/FAIL runs |
| `HETEROGENEOUS EVIDENCE` | Outcome differences occur only across different cohort keys |
| `PARTIAL DATA` | Required records are malformed, truncated, or ambiguously parsed |
| `DETERMINISTIC FAILURE` | At least 2 homogeneous independent runs and every valid outcome is FAIL |
| `NO FLAKINESS OBSERVED` | At least 2 homogeneous independent runs and every valid outcome is PASS |
| `SUSPECTED FLAKY` | A homogeneous cohort has both PASS and FAIL but does not meet confirmation criteria |
| `CONFIRMED FLAKY` | At least 10 homogeneous independent runs, including at least 2 PASS and 2 FAIL |
| `INVALID IDENTITY` | Stable test or run identity is missing, duplicate, or contradictory |

`NO FLAKINESS OBSERVED` is limited to the analyzed cohort and sample; it is not
proof that a test can never flake.

Three runs with one failure are always `SUSPECTED FLAKY`. Do not escalate solely
because the point failure rate exceeds 25 percent.

### Controlled reproduction

A controlled reproduction is a separately identified cohort that repeats one
stable test in isolated clean processes with the same complete cohort key. It
may confirm flakiness only when it contains at least 10 independent runs with at
least 2 PASS and 2 FAIL. Retries inside one job are not independent merely
because the runner printed several attempts.

### Root-cause findings

Source patterns, timing correlations, and environment observations are
hypotheses. Label each as `HYPOTHESIS` with supporting and contradicting
evidence. Use `CONFIRMED CAUSE` only when a controlled experiment changes one
factor and reproducibly removes or introduces the mixed outcome.

A deterministic failure is a regression/failure investigation, not a quarantine
candidate.

---

## Phase 4: Evaluate quarantine eligibility and risk

A confirmed flaky verdict does not automatically authorize quarantine.
“Make CI green” is never a valid objective or rationale.

A quarantine proposal is eligible only when either:

1. the same homogeneous cohort has at least 20 independent runs with at least
   3 PASS and 3 FAIL; or
2. a controlled reproduction has at least 10 isolated independent runs with at
   least 2 PASS and 2 FAIL.

Even when evidence eligibility is met, the proposal is invalid unless all fields
are concrete:

- stable test ID and current test-source path/hash;
- run-set/cohort ID, manifest hash, included run IDs, counts, rate, and interval;
- evidence verdict and any cause hypothesis;
- accountable owner;
- tracking issue/work item;
- expiry date no later than 14 days or the end of the current sprint, whichever
  is sooner;
- exact revalidation and removal criteria;
- supported engine/runner quarantine adapter;
- replacement coverage test ID, or explicit `NONE` plus a release-blocking gap;
- mapped stable AC/BUG IDs and criticality;
- player/release risk of disabling this test;
- approval record required before application;
- rollback/re-enable procedure.

Missing any field yields `QUARANTINE INELIGIBLE`. Sparse evidence never becomes
eligible because the observed rate is high.

### Independent quarantine gate

The quarantine application changes test or CI state and is outside this
workflow's owned write set. Present it as a separate future changeset for the
test/CI owner. The applying owner must obtain explicit human approval for the
exact test ID, adapter change, owner, expiry, issue, replacement/risk, and
rollback plan.

Do not ask for or imply application approval as part of persisting this analysis
report. Report persistence and quarantine application are separate decisions.

### Quarantine state machine

Report only states supported by external evidence:

| State | Evidence |
|---|---|
| `SUSPECTED` | Sparse homogeneous mixed outcomes |
| `CONFIRMED` | Confirmation sample criteria met |
| `PROPOSED` | Complete eligible proposal exists |
| `APPROVED` | Separate approval record names the exact proposal/hash |
| `APPLIED` | Application receipt names the approved proposal, adapter, changed config/test hashes, owner, issue, and expiry |
| `VERIFIED` | A later runner receipt uses the applied config hash and records the exact stable test ID as skipped/quarantined |
| `EXPIRED` | Expiry reached without verified renewal or resolution |
| `RESOLVED` | Fix plus required homogeneous verification runs pass and quarantine is removed by its owner |

Never infer `APPROVED` from a conversation summary, `APPLIED` from a proposal or
registry row, or `VERIFIED` from an intended skip. If expiry has passed, surface
a release-blocking revalidation requirement; do not let quarantine hide the
test indefinitely.

When `APPLIED` or `VERIFIED` evidence is available, hand its exact receipt paths
and hashes to `$regression-suite`. That owner may perform the ID-keyed selection
manifest upsert. This workflow never edits the selection manifest itself.

---

## Phase 5: Generate the analysis report

The report must include:

```markdown
# Test Flakiness Analysis: [run-set-id]

**Dataset Manifest**: [path]
**Dataset Hash**: sha256:[digest]
**Analysis Time**: [ISO-8601]
**Operation**: ANALYZED / REPORT_WRITTEN / REPORT_UNCHANGED / REPORT_DECLINED / FAILED
**Overall Evidence**: [strictest applicable evidence verdict]

## Run Validation

| Run ID | Receipt Path + Hash | Cohort ID | Independent? | Included? | Reason |
|---|---|---|---|---|---|

## Cohorts

| Cohort ID | Identity Tuple | Included Runs | Excluded Runs |
|---|---|---|---|

## Per-Test Evidence

| Stable Test ID | Cohort | Pass | Fail | Other | Rate + 95% CI | Verdict |
|---|---|---|---|---|---|---|

## Heterogeneous / Insufficient / Partial Evidence

- [test ID, exact limitation, and required next evidence]

## Root-Cause Hypotheses

- [HYPOTHESIS or CONFIRMED CAUSE, evidence, confidence, next controlled experiment]

## Quarantine Assessment

| Stable Test ID | Evidence Eligibility | Proposal Completeness | State | Missing Fields |
|---|---|---|---|---|

## Required Owner Handoffs

- Test/CI owner: [proposal/application work, if any]
- Regression-suite owner: [only after APPLIED/VERIFIED receipts exist]
```

The report is evidence, not a quarantine registry and not a runner receipt.

---

## Phase 6: Optional persistence and result protocol

Without `--persist`:

- perform no writes;
- return `Operation: ANALYZED`;
- return the evidence verdict independently;
- do not ask for changeset authorization.

With `--persist`:

1. Build the exact report path using the stable run-set ID and dataset-hash
   prefix.
2. Show the complete report and a one-file changeset with explicit non-writes:
   regression manifest, tests, CI/config, run data, and quarantine state.
3. Obtain one approval.
4. Immediately before writing, re-hash the run-set manifest and every included
   receipt; abort if any changed.
5. If updating an existing report, re-hash it and abort on preview/write
   conflict.
6. Write only the report, then read it back byte-for-byte and report its
   SHA-256.
7. If identical, do not rewrite; return `REPORT_UNCHANGED`.

Report both axes:

- Operation: `ANALYZED`, `REPORT_WRITTEN`, `REPORT_UNCHANGED`,
  `REPORT_DECLINED`, or `FAILED`.
- Evidence: one of the Phase 3 verdicts, plus quarantine eligibility/state.

Use `REPORT_WRITTEN` only after read-back verification. Declining report
persistence does not block or erase the completed analysis. Never say a test was
quarantined, CI was changed, or the regression manifest was updated unless
separate external receipts prove those facts.

---

## Collaborative protocol

- Prefer “insufficient” or “heterogeneous” over an unsupported flaky label.
- Sample size, independence, and identity equality are mandatory, not advisory.
- Quarantine is temporary risk acceptance, never a way to hide red CI.
- Always distinguish deterministic regression, flaky behavior, parser failure,
  and environment/config differences.
- Use only the quarantine adapter declared by the engine/test configuration;
  never emit a generic Python/pytest instruction for a non-Python project.
- Do not execute tests or create evidence that only a runner/CI system can own.
- Do not write `tests/regression-suite.md`, even when it lacks quarantine state.
