# Skill Test Spec: `$test-flakiness`

All revisions in this specification are supplied metadata; no identity or currentness decision is derived from file content.

## Skill Summary

`$test-flakiness` contract `cgs.test-flakiness/v2` analyzes one explicit,
bounded `cgs.test-run-set/v2` dataset. It validates result formats through exact
versioned parsers, forms identity-equal independent cohorts, separates
environment drift from code/config heterogeneity, reports Wilson uncertainty,
and keeps hypotheses distinct from controlled causes.

The workflow is read-only by default. `analyze --persist` may create one
deterministic revision-named analysis report, but analysis always completes
independently of persistence. It never runs tests or changes tests, CI,
quarantine, registries, or `tests/regression-suite.md`. `status` validates
external state receipts without writing.

---

## Required test instrumentation

Run every behavioral case in an isolated disposable repository fixture. Record:

1. recursive path/type/revision snapshots before and after invocation;
2. every filesystem mutation attempt by the workflow and parser;
3. every file read, canonical path, exact byte count, and read order;
4. parser ID/version/package revision, argv, wall time, exit status, raw and
   normalized revisions, receipt bytes, and sandbox denials;
5. all normalized records with originating raw record identity;
6. exact response bytes, canonical payload bytes, evidence bytes, and any report
   write/read-back receipt; and
7. deterministic clock and UUID sources for reproducibility checks.

The mutation guard passes only when before/after snapshots are byte-identical
except for the single authorized report in a `--persist` success case, and the
mutation-attempt ledger contains no unauthorized attempt. Parser isolation must
deny network, project writes, undeclared reads, and child-process expansion. If
any required observation is unavailable, mark the assertion `UNTESTED`, not PASS.
Do not execute this project skill merely to perform static lint, and do not update
catalog result fields from an uninstrumented run.

---

## Static and specification-integrity assertions

- [ ] Frontmatter contains only `name` and a non-empty `description`
- [ ] Contract version is exactly `cgs.test-flakiness/v2`
- [ ] Metadata describes bounded homogeneous analysis and external quarantine
- [ ] Analyze and status argument grammars are exact and reject scan/single-log
  inference
- [ ] Run, test, binary, runner/config, platform, environment, seed, order, and
  process-isolation identity are mandatory
- [ ] Parser registry/receipt schemas, exact tool version/revision, format matrix,
  sandbox, timeouts, and malformed/truncated behavior are explicit
- [ ] Fixed byte, run, result, record, identity, finding, row, parser-time, and
  receipt bounds cannot be raised by a manifest
- [ ] Cross-code/config heterogeneity and environment drift have distinct
  classifications and are never pooled
- [ ] Only independent PASS+FAIL forms the denominator; retry, error, skip,
  aborted, not-run, resume, and duplicate rules are explicit
- [ ] Exact failure rate, sample size, Wilson 95% interval, precision, and
  uncertainty interpretation are defined
- [ ] Confirmation and quarantine minimums are fixed floors; sparse high rates
  cannot bypass them
- [ ] Root cause remains a hypothesis without a one-factor controlled experiment
- [ ] Quarantine eligibility, adapter, owner, expiry, issue, coverage/risk,
  approval, application, verification, rollback, and resolution are distinct
- [ ] Stable finding IDs exclude paths, names, rates, intervals, confidence,
  state, timestamps, current dataset/build, and report revision
- [ ] `cgs.test-flakiness-report/v1`, `cgs.review-evidence/v1`, canonical revisions,
  partial-evidence limits, and quarantine-authority `NONE` are explicit
- [ ] Analysis result and report persistence are independent; default is
  zero-write and optional persistence owns exactly one revision-named report
- [ ] Cases are numbered contiguously from 1 through 20
- [ ] Every case contains `Fixture`, `Input`, `Expected writes`, `Expected
  behavior`, and `Assertions` subsections with non-placeholder content
- [ ] No heading, table, list, code fence, sentence, or case is truncated or
  orphaned; all Markdown fences are balanced
- [ ] Catalog registration points to this analysis spec and shared catalog result
  fields remain outside this candidate's write set

---

## Canonical fixture

Unless overridden, use run set `run-set-alpha`, schema `cgs.test-run-set/v2`,
with exact revisions for parser registry `cgs.test-result-parser-registry/v1`,
environment registry `cgs.test-environment-registry/v1`, and policy
`cgs.test-flakiness-policy/v1`. The parser is `PARSER-GODOT-JUNIT-1` version
`1.4.0`, package revision `P`, validated for runner/schema/platform, and emits
`cgs.test-result-records/v1` plus `cgs.test-parser-receipt/v1`.

Canonical test `godot::TC-combat-S001-AC01::NONE::<binary-revision>` uses one clean
build/commit/config/engine/platform/environment/seed/order identity. Every
independent run has a unique run ID, process-isolation ID, result revision, and runner
receipt. Fixture placeholders are replaced by valid explicit revisions.

---

## Case 1: Strict invocation and no discovery

### Fixture

Provide valid manifests/reports plus unrelated `.github/` workflows, CI logs,
and result directories that would be discoverable by a scan.

### Input

Run missing mode/options, unknown mode, duplicate options, extra positional
arguments, option values beginning with `--`, URLs, globs, directories,
symlinks, junction escapes, outside paths, `analyze --report`, `status --manifest`,
and a bare CI-log path. Also run each valid grammar.

### Expected writes

None for all invalid/default cases. `--persist` is not used.

### Expected behavior

Invalid grammar returns `ERROR` with the rejected token and reason. A legacy file
proving only one execution returns `INSUFFICIENT EVIDENCE`. Valid analyze/status
paths are canonicalized once. No latest file, workflow, log, or directory scan is
inferred.

### Assertions

- [ ] Exact valid commands match the contract
- [ ] No invalid input launches a parser or emits findings/evidence
- [ ] Single-log repeated lines/retries do not become independent runs
- [ ] Unrelated files are never read
- [ ] Mutation guard passes

## Case 2: Versioned parser and malformed/truncated results

### Fixture

Create valid XML, truncated XML, summary-only XML, ambiguous suite/test records,
unsupported schema, two equally exact parser matches, wrong parser package revision,
invalid validator receipt, timeout, nonzero exit, oversized receipt, mismatched
declared revision, and a parser sandbox write/network attempt.

### Input

Analyze each variant independently, then one mixed run set containing valid and
malformed declared results.

### Expected writes

None.

### Expected behavior

Only an exact validated parser executes. Unusable primary data is `ERROR — NO
USABLE RUN DATA`. Mixed valid/invalid data is `PARTIAL DATA`; valid local counts
remain disclosed, but confirmation and quarantine proposal are forbidden.

### Assertions

- [ ] Parser product/version/revision, supported format/schema/platform, argv, raw
  and normalized revisions, timing, and receipt identity are reported
- [ ] Text matching never promotes suite summary, retry text, or failure blocks
- [ ] Every malformed/truncated/ambiguous omission has an exact reason
- [ ] Sandbox violations fail closed and mutation guard passes
- [ ] No partial input yields `CONFIRMED FLAKY`

## Case 3: Runner-qualified test identity prevents false merges

### Fixture

Provide same display name in two runner namespaces, parameter cases A/B, same
runner-qualified ID from different binary revisions, renamed display text with
unchanged stable ID, duplicate canonical IDs, missing stable IDs, and one valid
identity-migration receipt.

### Input

Analyze the combined run set.

### Expected writes

None.

### Expected behavior

Canonical keys remain distinct by namespace, stable ID, parameter ID, and binary
revision. Display rename alone preserves identity; missing/duplicate identities are
`INVALID IDENTITY`. Migration binds only declared IDs and never crosses binary
revisions in a cohort.

### Assertions

- [ ] Display/method/path/suite/base-name equality never merges tests
- [ ] Binary revision is part of every canonical test key
- [ ] Invalid identities are excluded from statistics with exact reasons
- [ ] Valid records retain raw result/record provenance
- [ ] Mutation guard passes

## Case 4: Code, build, runner, seed, or order changes are heterogeneous

### Fixture

For one stable test, create PASS in one cohort and FAIL in cohorts differing one
at a time by commit, tree state, build ID/artifact revision, binary, runner version,
config revision, engine version, seed/policy, shard, or test-order revision.

### Input

Analyze the run set.

### Expected writes

None.

### Expected behavior

Each changed key creates a distinct cohort and classification
`HETEROGENEOUS EVIDENCE`. No cross-cohort denominator, rate, flaky verdict, or
quarantine proposal exists.

### Assertions

- [ ] Exact differing keys and cohort revisions are reported
- [ ] Same test name cannot override run identity
- [ ] Homogeneous local all-pass/all-fail evidence remains local
- [ ] No project-wide flaky label is synthesized
- [ ] Mutation guard passes

## Case 5: Environment drift is separated from heterogeneity

### Fixture

Keep code/build/binary/runner/config/engine/seed/order identical while varying one
at a time: platform profile, OS image/version, architecture, driver/runtime/
toolchain, machine/container image, or registered environment value. Add an
unexplained finding key mismatch.

### Input

Analyze PASS/FAIL outcomes across these runs.

### Expected writes

None.

### Expected behavior

Explained environment differences produce separate cohorts and `ENVIRONMENT
DRIFT`; unexplained finding key mismatch is `INVALID IDENTITY`. Neither is called
flakiness or environmental cause.

### Assertions

- [ ] Environment ledger lists exact keys, receipts, cohorts, and outcomes
- [ ] No cross-environment pooling occurs
- [ ] `ENVIRONMENT DRIFT` remains an identity boundary, not a causal conclusion
- [ ] Host environment never fills captured environment fields
- [ ] Mutation guard passes

## Case 6: Independence and denominator rules

### Fixture

Include independent PASS/FAIL, retry PASS after parent FAIL, resumed attempt,
aborted run, ERROR, SKIP, NOT_RUN, duplicate receipt, duplicate process-isolation
ID, and the same raw result parsed twice.

### Input

Analyze the canonical test.

### Expected writes

None.

### Expected behavior

Only unique clean-process independent PASS and FAIL enter the denominator. Every
other record is counted separately and excluded with reason. Retry success does
not erase or duplicate the parent outcome.

### Assertions

- [ ] Denominator equals independent PASS + FAIL exactly
- [ ] Run IDs and process-isolation IDs are unique
- [ ] ERROR/SKIP/ABORTED/NOT_RUN never become PASS or FAIL
- [ ] Duplicate/raw reparse never increases sample size
- [ ] Mutation guard passes

## Case 7: Wilson uncertainty and boundary precision

### Fixture

Use homogeneous cohorts with counts 1/1, 2/0, 0/2, 2/8, 3/17, and large counts
near a policy decision threshold. Supply independently calculated Wilson
intervals using the contract z value.

### Input

Analyze all cohorts twice with different display rounding settings permitted by
the policy.

### Expected writes

None.

### Expected behavior

Exact rational rates, denominator, decimal rate, and 95% Wilson interval match
the reference calculation. Full precision controls decisions; display rounding
does not change a verdict.

### Assertions

- [ ] No rate exists below denominator two
- [ ] Interval is never described as next-run probability or root-cause proof
- [ ] Sample window and independence limitations accompany statistics
- [ ] Policy may raise but not lower fixed sample floors
- [ ] Repeated decisions are deterministic

## Case 8: Sparse samples cannot confirm or quarantine

### Fixture

Create one-run PASS, one-run FAIL, two PASS, two FAIL, and three runs with two
PASS/one FAIL.

### Input

Analyze each independently.

### Expected writes

None.

### Expected behavior

One run is `INSUFFICIENT EVIDENCE`; all PASS is `NO FLAKINESS OBSERVED`; all FAIL
is `DETERMINISTIC FAILURE`; three with one failure is `SUSPECTED FLAKY` even
though its point rate exceeds 25 percent. All are quarantine-ineligible.

### Assertions

- [ ] Single PASS is not a universal no-flake claim
- [ ] Deterministic failure routes away from quarantine
- [ ] High sparse rate cannot bypass fixed floors
- [ ] No proposal or quarantine adapter instruction is produced
- [ ] Mutation guard passes

## Case 9: Controlled homogeneous reproduction confirms flakiness

### Fixture

Use ten isolated independent runs in one exact cohort, with eight PASS and two
FAIL, complete parser/provenance coverage, and no excluded evidence. Add a
variant with ten retries inside one job.

### Input

Analyze each variant.

### Expected writes

None.

### Expected behavior

The independent cohort is `CONFIRMED FLAKY`; the retry-only variant remains
insufficient because attempts are not independent. Confirmation does not approve
or apply quarantine.

### Assertions

- [ ] Minimum run/pass/fail counts are checked exactly
- [ ] Complete coverage is required for confirmation
- [ ] Retry print count cannot satisfy independence
- [ ] Quarantine authority remains `NONE`
- [ ] Mutation guard passes

## Case 10: Fixed input bounds and deterministic partial proof

### Fixture

Exercise every limit at limit minus one, limit, and limit plus one. Include a
within-byte-bound result expanding beyond the record limit and a rendered table
beyond 500 rows.

### Input

Analyze each boundary fixture; add manifest fields attempting to raise limits.

### Expected writes

None, including with unauthorized embedded persistence fields.

### Expected behavior

Pre-parse manifest/byte excess is `ERROR — REQUEST EXCEEDS FIXED BOUND`.
Post-parse record/identity/finding/row excess is `PARTIAL DATA — BOUNDED INPUT`
with stable complete-set identifier, included/omitted counts, boundary key, and tail
identifier.

### Assertions

- [ ] Manifest cannot raise any fixed limit
- [ ] Deterministic manifest and stable-test ordering selects the same prefix
- [ ] No omitted-tail sampling, complete rate, confirmation, or quarantine
- [ ] Selected manifests/registries/policies/receipts are never partially read
- [ ] Mutation guard passes

## Case 11: Root-cause hypotheses require controlled experiments

### Fixture

Provide timing correlation, retry order, random/global keywords, stack trace,
source pattern, and load telemetry without an experiment. Then add a valid
two-arm experiment changing exactly one registered factor, with policy-sufficient
independent runs. Add a confounded two-factor variant.

### Input

Analyze each dataset.

### Expected writes

None.

### Expected behavior

Uncontrolled and confounded observations remain `HYPOTHESIS` with disclosed
confidence, supporting/contradicting evidence, alternatives, and next experiment.
Only the valid one-factor experiment may produce `CONFIRMED CAUSE` within its
measured scope.

### Assertions

- [ ] Test-name keywords never infer cause
- [ ] Confidence is not presented as posterior probability
- [ ] Every hypothesis includes falsifiable success criteria
- [ ] No guaranteed fix or failure-rate reduction is promised
- [ ] Mutation guard passes

## Case 12: Quarantine evidence and proposal completeness

### Fixture

Create confirmed cohorts at 10 runs/2 PASS/2 FAIL and 20 runs/3 PASS/3 FAIL,
plus controlled reproduction. Vary owner, issue, expiry, source/binary revisions,
AC/BUG mapping, risk, adapter, replacement coverage/gap, approval owner,
revalidation/removal, rollback, and expiry escalation fields.

### Input

Request an assessment, not application.

### Expected writes

None.

### Expected behavior

Only the fixed evidence alternatives satisfy evidence eligibility. Every missing
field yields `INELIGIBLE`; a complete eligible record is at most `PROPOSED` and
contains no executable patch.

### Assertions

- [ ] Confirmation alone does not authorize quarantine
- [ ] “Make CI green” is rejected
- [ ] Expiry is no later than 14 days/current sprint end
- [ ] Missing replacement coverage creates an explicit release-blocking gap
- [ ] No generic framework skip instruction is emitted without exact adapter

## Case 13: Quarantine states require exact authority receipts

### Fixture

Start with a complete proposal. Add variants with conversation approval only,
exact approval receipt, application receipt, intended skip text, and later runner
receipt bound to applied configuration and canonical test key.

### Input

Run `status --report ... --receipts ...` for each variant.

### Expected writes

None.

### Expected behavior

States progress only `PROPOSED` → `APPROVED` → `APPLIED` → `VERIFIED` when each
exact receipt validates. Conversation and intent text do not advance state.

### Assertions

- [ ] Approval binds proposal revision, owner, risk, and expiry
- [ ] Application binds approval, adapter, and pre/post revisions
- [ ] Verification binds applied config and observed quarantine result
- [ ] Report/registry row alone is never application evidence
- [ ] No CI/test/regression-manifest write occurs

## Case 14: Expiry and resolution do not leave permanent quarantine

### Fixture

Provide expired state without renewal; valid renewal; closed issue without fix;
fix receipt without removal; removal without post-fix runs; and complete fix,
removal, plus policy-sufficient homogeneous post-fix passing runs that executed
the test under the new configuration.

### Input

Run status for each fixture.

### Expected writes

None.

### Expected behavior

Expired evidence becomes `EXPIRED` with release-blocking revalidation. Only the
complete final fixture becomes `RESOLVED`. Historical proposal/application data
remains visible without an append-only registry mutation.

### Assertions

- [ ] Closed issue alone is not resolution
- [ ] Skipped post-fix runs do not prove repair
- [ ] Removal and homogeneous passing verification are both mandatory
- [ ] Renewal must bind current risk/owner/expiry
- [ ] Mutation guard passes

## Case 15: Default analysis is strictly read-only

### Fixture

Use a complete run set with existing flakiness reports, test annotations, CI
files, quarantine records, regression manifest, and QA trackers.

### Input

Run `analyze --manifest run-set.yaml` without `--persist`.

### Expected writes

None.

### Expected behavior

Analysis and evidence return in conversation with `analysis_result: COMPLETE`
and `report_persistence: NOT_REQUESTED`. No authorization question occurs.

### Assertions

- [ ] Before/after snapshots are byte-identical
- [ ] Mutation-attempt ledger is empty
- [ ] Report omission cannot become BLOCKED or alter evidence verdicts
- [ ] Quarantine/regression/test/CI ownership is unchanged
- [ ] No chained workflow or follow-up task starts

## Case 16: Optional one-report persistence is isolated and safe

### Fixture

Use a complete analysis. Run variants with absent target directory, denied write,
new target, identical existing bytes, conflicting existing bytes, selected input
changed before write, and read-back mismatch.

### Input

Run `analyze --manifest run-set.yaml --persist`; the flag is the bounded
one-report authorization. Also simulate user withdrawal before write.

### Expected writes

Only the new-target success may create exactly
`production/qa/flakiness/flakiness-report-<run-set-id>-<UTC-run-id>.md`. No variant
overwrites, renames, or modifies another file.

### Expected behavior

Persistence is respectively `FAILED`, `DECLINED`, `WRITTEN`, `UNCHANGED`,
`CONFLICT`, input-change `ERROR`, or `FAILED`. Analysis remains independently
available except when input mutation invalidates it. `WRITTEN` requires exact
read-back and a binding write receipt.

### Assertions

- [ ] Derived path uses validated run-set ID and manifest revision prefix
- [ ] Existing conflicting/user bytes are preserved
- [ ] Report file revision, payload revision, artifact identity, path, writer, and time
  bind in the write receipt without a cyclic evidence-record reference
- [ ] No report status implies quarantine approval/application
- [ ] Filesystem diff is at most the one owned report

## Case 17: Stable finding identity and lifecycle

### Fixture

Generate one finding, then vary file paths, line numbers, display names, counts,
rate, interval, confidence, severity, state, timestamp, current run set/build, and
report revision without changing repository/category/test/cohort/external-receipt
identity. Then vary each canonical identity field.

### Input

Analyze each fixture twice.

### Expected writes

None.

### Expected behavior

Noncanonical changes preserve `TFF-<category>-<12-lowercase-hex>`; each canonical
identity change changes it. Duplicate identities coalesce and preserve all run
evidence; ordering is deterministic.

### Assertions

- [ ] Stable business-ID components and collision suffix independently validate
- [ ] Paths/names/measurements/state/time/build/report never enter the ID
- [ ] Category, canonical test key, cohort, repository, and external receipt do
  enter the identity exactly
- [ ] First/current run-set lifecycle fields do not churn ID
- [ ] Mutation guard passes

## Case 18: Evidence is canonical, stable, and authority-free

### Fixture

Use complete confirmed, complete no-flakiness, insufficient, heterogeneous,
environment-drift, and partial datasets. Provide a deterministic clock/UUID.

### Input

Analyze each without persistence, then persist the complete confirmed report.

### Expected writes

None except the explicitly persisted report variant.

### Expected behavior

Every non-error result emits exactly one `cgs.review-evidence/v1` record bound to
canonical `cgs.test-flakiness-report/v1`. Partial evidence has coverage PARTIAL
and cannot support confirmation/quarantine. Conversation-only records say
persistence NONE; the post-write response record says VERIFIED_FILE and binds its
separately computed write receipt. The persisted report itself does not embed
post-write evidence or a self-referential file revision.

### Assertions

- [ ] Payload and record revisions independently revalidate
- [ ] Changing an artifact requires a new explicit artifact revision or record ID
- [ ] Producer, run/time, manifest identity, findings, and coverage are present
- [ ] `quarantine_authority: NONE` and `gate_evidence_candidate: false` always
- [ ] Persistence changes durability only, not measurements/verdicts

## Case 19: Status mode validates rather than invents state

### Fixture

Provide a valid report, report with bad payload/evidence revision, report above size
limit, absent receipt manifest, malformed receipts, unrelated receipts, and
complete state-transition receipts.

### Input

Run status with each explicit report/receipt set.

### Expected writes

None under all variants.

### Expected behavior

Invalid primary report returns `ERROR`; missing/invalid optional receipts leave
state at the last proven transition and disclose gaps. No receipt discovery
occurs. Valid APPLIED/VERIFIED/EXPIRED/RESOLVED receipt paths/revisions are presented
only as owner handoffs.

### Assertions

- [ ] Status never reparses run results or creates new analysis findings
- [ ] Receipt order cannot skip a state prerequisite
- [ ] Unrelated receipt identity is rejected
- [ ] Regression-suite owner receives only exact external receipt identities
- [ ] Mutation guard passes

## Case 20: Dedicated spec is complete and contract-aligned

### Fixture

Run a Markdown/spec linter against the staged skill, metadata, this exact spec,
and catalog registration. Also feed the linter damaged copies with a truncated
Case 7, missing Assertions section, orphan list item, unbalanced fence,
noncontiguous numbering, and old write/verdict vocabulary.

### Input

Perform structural validation only; do not invoke `$test-flakiness`.

### Expected writes

None.

### Expected behavior

The staged three-file candidate passes. Every damaged copy fails with a precise
structural or contract-parity error. Catalog remains unchanged and continues to
point to `CGS Skill Testing Framework/skills/analysis/test-flakiness.md`.

### Assertions

- [ ] Cases 1-20 exist once, contiguously, and with all five required subsections
- [ ] All Markdown fences/headings/tables/lists are complete
- [ ] Invocation, schemas, verdicts, persistence, evidence, and write-set terms
  match the skill and metadata
- [ ] No legacy `COMPLETE/BLOCKED` single-axis result or implicit registry write
  remains
- [ ] Static validation does not modify catalog result fields

---

## Audit finding traceability

| Audit finding | Closing contract clauses | Behavioral proof |
|---|---|---|
| TF-004 | Exact format parser registry, schema/version/tool revision, validated receipt, partial parse fail-closed | Cases 2, 10 |
| TF-005 | Runner-qualified canonical test key includes parameter identity and binary revision; no name merge | Cases 3, 17 |
| TF-006 | Hypothesis/confidence boundary and one-factor controlled experiment for confirmed cause | Case 11 |
| TF-007 | Explicit manifest only; fixed file/byte/time/record/row limits and deterministic omission proof | Cases 1, 10 |
| TF-008 | PROPOSED/APPROVED/APPLIED/VERIFIED states require distinct exact authority receipts | Cases 12, 13, 19 |
| TF-009 | EXPIRED and RESOLVED states require renewal/fix/removal/post-fix evidence while preserving history | Case 14 |
| TF-010 | Analysis result and optional report persistence are independent; refusal/failure never blocks analysis | Cases 15, 16, 18 |
| TF-017 | Skill/spec/metadata share v2 invocation, read/write set, dual axes, verdicts, evidence, and complete Case grammar | Case 20 |

Homogeneous identity, uncertainty, environment drift, quarantine authority,
stable evidence, and bounded partial behavior receive additional positive and
negative coverage in Cases 4-9, 12-14, and 17-19.

---

## Pass criteria

- [ ] Every static and specification-integrity assertion passes
- [ ] Cases 1-20 pass with all required instrumentation
- [ ] Mutation guard passes in every default/status/error/partial case and every
  optional persistence variant except the exact one-report success
- [ ] Parser sandbox violations never mutate the fixture
- [ ] All stable IDs, cohort revisions, candidate/tail identifiers, payload revisions,
  evidence record IDs, file revisions, and write receipts independently revalidate
- [ ] TF-004 through TF-010 and TF-017 each have positive and negative/boundary
  behavioral proof
- [ ] No heterogeneous, environment-drift, sparse, invalid, malformed, truncated,
  or bounded data confirms flakiness or supports quarantine
- [ ] No report or conversation advances quarantine authority or writes the
  regression manifest
- [ ] Repeated fixtures produce identical cohorting, statistics, verdicts,
  finding IDs, and omission proofs apart from controlled run metadata
- [ ] Shared catalog and live skill/spec/metadata remain unchanged by this
  candidate and by static verification
