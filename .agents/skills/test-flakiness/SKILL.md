---
name: test-flakiness
description: "Analyzes bounded, homogeneous, identity-bound test run sets with explicit uncertainty and quarantine authority boundaries; read-only by default with one optional revision-named report."
---

## Contract, modes, and authority

Invoke exactly one mode:

```text
$test-flakiness analyze --manifest <run-set-manifest> [--persist]
$test-flakiness status --report <flakiness-report> [--receipts <status-receipt-manifest>]
```

Contract version: `cgs.test-flakiness/v2`.

`analyze` evaluates already-produced test results. It never launches, retries, or
reorders tests. Without `--persist`, the entire workflow is read-only. `--persist`
is explicit authorization for at most one deterministic, revision-named analysis
report under `production/qa/flakiness/`; it does not authorize any other write.
`status` is always read-only.

This skill never changes test source or skip annotations, runner configuration,
CI, result files, run manifests, parser registries, environment profiles,
quarantine registries, `tests/regression-suite.md`, QA plans, stories, bugs,
release state, catalogs, or session state. It never approves or applies
quarantine. Analysis, report persistence, quarantine approval, quarantine
application, regression selection, test repair, and resolution are separate
authorities.

Reject missing or extra positional arguments, duplicate or unknown options,
option values beginning with `--`, mode-forbidden options, URLs, globs,
directories, symlinks, paths outside the repository, and junction escapes. A
single CI log, workflow file, directory scan, or inferred “latest” run is not a
run set. Return `INSUFFICIENT EVIDENCE` for a valid legacy file containing only
one execution identity; otherwise invalid invocation returns `ERROR`. Never
auto-scan `.github/`, CI directories, reports, or test outputs.

---

## Phase 0: Freeze inputs and applicable governance

Resolve the repository root and canonicalize every supplied path before reading
content. Load every applicable `AGENTS.md` from the root to each selected file in
root-to-target order and list the paths in the output. Record revision for exact
raw bytes for every selected manifest, registry, profile, policy, result, report,
and receipt. Recompute them immediately before returning and, if persisting,
immediately before writing. If any selected input changes, keep the completed
pre-change calculations only as discarded work and return `ERROR — INPUT CHANGED
DURING ANALYSIS` without findings, evidence, quarantine eligibility, or a write.

`analyze` requires manifest schema `cgs.test-run-set/v2` and these exact,
revision-bound dependencies:

- a parser registry with schema `cgs.test-result-parser-registry/v1`;
- an environment-key registry with schema
  `cgs.test-environment-registry/v1`;
- a flakiness policy with schema `cgs.test-flakiness-policy/v1`; and
- an explicit ordered list of result and runner-receipt paths.

The manifest must declare a stable lowercase-kebab `run_set_id`, project and
repository identity, selection rule and time window, producer identity, and a
complete ordered run list. Do not infer missing values from filenames, file
timestamps, neighboring logs, Git HEAD, the analysis host, or prose.

The request may select less work but cannot raise these fixed limits:

| Resource | Fixed maximum |
|---|---:|
| Run-set manifest | 1 MiB |
| Each registry, policy, report, or receipt manifest | 1 MiB |
| Runs named by one run set | 512 |
| Result files per run | 64 |
| Bytes per result file | 64 MiB |
| Aggregate selected result bytes | 2 GiB |
| Parsed test records per run | 100,000 |
| Parsed test records total | 1,000,000 |
| Stable test identities | 10,000 |
| Findings | 4,096 |
| Rows rendered per output table | 500 |
| One parser execution | 30 seconds |
| All parser executions | 300 seconds |
| One parser receipt | 1 MiB |

Reject a manifest or selected byte set above its pre-parse bound as
`ERROR — REQUEST EXCEEDS FIXED BOUND`. If a within-byte-bound result expands
beyond a record, identity, finding, or rendering limit, stop at the deterministic
manifest-order then stable-test-ID boundary. Report the complete candidate-set
identity identifier, included and omitted counts, boundary key, and omitted-tail
identifier as `PARTIAL DATA — BOUNDED INPUT`. Never sample the omitted tail, claim a
complete rate, confirm flakiness, or propose quarantine from a truncated set.

---

## Phase 1: Validate runs with versioned parsers

Each run entry must contain:

- unique run ID and immutable runner receipt path/revision;
- commit SHA, source-tree state, build ID, build artifact revision, test binary ID
  and revision;
- runner product/version, runner configuration ID/revision, engine product/version,
  and parser format/schema/version;
- OS image ID/revision, OS version, architecture, target platform/profile ID/revision,
  container or machine-image ID/revision, driver/runtime/toolchain versions;
- environment profile ID/revision plus a canonical key/value finding key computed
  by the selected environment registry;
- random seed and seed policy, shard ID/count, test-order ID/revision;
- start/end UTC timestamps, monotonic duration, attempt kind, parent attempt ID
  or `NONE`, process-isolation ID, and clean-process receipt; and
- ordered result paths, exact declared revisions, and declared formats.

Missing, duplicate, contradictory, or revision-invalid critical identity makes that
run ineligible and creates `INVALID IDENTITY`. Do not repair it from another run.

Select exactly one parser registry entry by runner product/version, result
format/schema/version, and platform profile. An entry is valid only when it
declares a stable parser ID/version, exact executable or package revision,
supported format matrix, deterministic arguments, normalized schema
`cgs.test-result-records/v1`, receipt schema
`cgs.test-parser-receipt/v1`, validator receipt IDs for that parser version, and
an isolation policy forbidding network, project writes, undeclared reads, or
child-process expansion.

Run only that parser within fixed limits. Validate its receipt: parser
ID/version/revision, exact argv, start/end UTC, exit status, raw path/revision/bytes,
normalized payload revision/bytes, record count, warnings, and validator identity.
Missing, ambiguous, unsupported, timed-out, nonzero, oversized, malformed, or
revision mismatched parsing excludes the affected result. A suite summary, retry
line, failure block, or truncated XML/JSON/log cannot be promoted to a test
record by text matching.

If no valid primary result remains, return `ERROR — NO USABLE RUN DATA`. If at
least one valid run remains but any declared result, receipt, or required record
is excluded, set coverage to `PARTIAL DATA`, identify every omission, calculate
only disclosed local counts, and emit no `CONFIRMED FLAKY` verdict or quarantine
proposal. Parser warnings that cannot affect record completeness may remain
advisory only when the registry classifies their exact code as non-semantic.

---

## Phase 2: Resolve stable tests and homogeneous independent cohorts

### Stable test identity

Every normalized test record requires:

- runner-qualified stable test ID and runner namespace;
- parameter/case ID or `NONE`;
- test binary ID and revision;
- optional exact `TC-...` requirement-test ID and `RS-...` selection ID; and
- outcome, duration, attempt ID, and originating result/record identity.

The canonical test key is the exact tuple
`runner_namespace + stable_test_id + parameter_or_NONE + test_binary_revision`.
Never merge by display name, method name, title, source path, suite name,
parameterized base name, fuzzy text, or prior spelling.
Missing/duplicate canonical keys are `INVALID IDENTITY` and excluded. Renames
remain distinct unless a separate immutable identity-migration receipt binds the
old and new runner-qualified IDs; the receipt never bridges different binary
revisions inside one cohort.

### Run cohort identity

Create the exact cohort key from:

```text
commit_sha + source_tree_state + build_id + build_artifact_revision +
test_binary_id + test_binary_revision + runner_product/version +
runner_config_id/revision + engine_product/version + os_image_id/revision + os_version +
architecture + target_platform/profile_id/revision + machine_or_container_image/revision +
driver/runtime/toolchain_versions + environment_profile_id/revision +
environment_identity + random_seed + seed_policy + shard_id/count +
test_order_id/revision
```

Runs differing in any field are separate cohorts. Record a canonical cohort JSON
revision as `cohort_id`; do not use display labels or paths in the identity.

Only `attempt_kind: independent` runs with unique run and process-isolation IDs,
no parent attempt, and valid clean-process receipts count toward sample size.
Retries, resumed attempts, aborted runs, duplicates, rerendered receipts, and
multiple parses of the same raw result are excluded from the denominator and
listed with reasons. A retry that later passes does not turn its parent failure
into an independent PASS.

Classify cross-cohort differences separately:

- when code/build/binary/runner/config/engine/seed/order identity differs, use
  `HETEROGENEOUS EVIDENCE` and name exact keys;
- when those keys match but platform, OS/image, architecture, driver/runtime/
  toolchain, machine/container, or registered environment values differ, use
  `ENVIRONMENT DRIFT` and name exact keys; and
- when the environment finding key differs without a field-level explanation,
  use `INVALID IDENTITY`, not an environment hypothesis.

Never pool cross-cohort PASS and FAIL. A valid homogeneous cohort may still be
analyzed locally, but cross-cohort outcome differences are not proof of flaky
behavior or environmental causation.

---

## Phase 3: Compute samples, uncertainty, and evidence verdicts

For each canonical test key and exact cohort, count `PASS`, `FAIL`, `ERROR`,
`SKIP`, `ABORTED`, and `NOT_RUN`. The statistical denominator is only independent
`PASS + FAIL`. Report every other outcome separately. With denominator below two,
do not calculate a flakiness rate.

For denominator at least two report the exact rational failure rate `FAIL / (PASS
+ FAIL)`, decimal rate, sample size, and two-sided 95% Wilson score interval using
`z = 1.959963984540054`. With `n = PASS + FAIL` and `p = FAIL / n`, calculate
`d = 1 + z^2/n`, `center = (p + z^2/(2n))/d`, and
`half = z*sqrt(p*(1-p)/n + z^2/(4n^2))/d`; the interval is
`[max(0, center-half), min(1, center+half)]`. Calculate from full precision and
round only for display according to the versioned policy. The interval is
uncertainty about the sampled cohort, not the probability that the next run will
fail and not proof of a root cause. Report sample selection/time-window
limitations and independence evidence beside the interval.

Apply these fixed minimums; a policy may raise but never lower them:

| Evidence verdict | Required evidence |
|---|---|
| `INSUFFICIENT EVIDENCE` | Fewer than 2 valid independent PASS/FAIL runs |
| `DETERMINISTIC FAILURE` | At least 2 and all are FAIL |
| `NO FLAKINESS OBSERVED` | At least 2 and all are PASS |
| `SUSPECTED FLAKY` | Homogeneous PASS and FAIL below confirmation minimum |
| `CONFIRMED FLAKY` | At least 10, including at least 2 PASS and 2 FAIL |
| `INVALID IDENTITY` | Required run/test identity is missing, duplicate, or contradictory |
| `PARTIAL DATA` | Any required selected evidence is missing, malformed, truncated, excluded, or bounded |
| `HETEROGENEOUS EVIDENCE` | Outcome differences exist only across non-environment cohort keys |
| `ENVIRONMENT DRIFT` | Outcome differences exist only across exact environment/platform cohorts |

Three runs with one failure are always `SUSPECTED FLAKY`, regardless of point
rate or interval. `NO FLAKINESS OBSERVED` applies only to the exact cohort and
sample. A deterministic failure routes to regression/failure investigation and
is never a quarantine candidate.

When multiple limitations apply, preserve every per-cohort verdict and set
analysis coverage by precedence: `PARTIAL DATA` or `INVALID IDENTITY` first,
then cross-cohort `ENVIRONMENT DRIFT`/`HETEROGENEOUS EVIDENCE`, then sample
sufficiency. Do not synthesize one project-wide flaky label from test counts.

---

## Phase 4: Separate environment observations and cause hypotheses

Produce an environment-drift ledger containing each cohort ID, differing
registered keys, source receipt, observed outcomes, and whether a controlled
comparison exists. Environment drift is an identity boundary, not a cause.
Timing proximity, retry order, random/global keywords, a stack trace, source
pattern, resource-load telemetry, or correlation does not prove causation.

Every cause entry has stable test key, cohort IDs, classification
`HYPOTHESIS` or `CONFIRMED CAUSE`, confidence `UNTESTED`, `LOW`, `MEDIUM`, or
`HIGH`, supporting evidence, contradicting evidence, alternative explanations,
and one bounded controlled experiment with success criteria. Confidence is not a
posterior probability and may not replace sample sufficiency.

Use `CONFIRMED CAUSE` only when a separately identified controlled experiment
changes exactly one registered factor, keeps every other cohort key equal, meets
the flakiness policy's minimum independent runs in both arms, and reproducibly
introduces or removes mixed outcomes. Otherwise remain `HYPOTHESIS`. Never infer
cause from test-name keywords or recommend a guaranteed fix or rate reduction.

---

## Phase 5: Evaluate quarantine without acquiring authority

`CONFIRMED FLAKY` does not automatically authorize quarantine. “Make CI green”
is never a valid rationale. Quarantine evidence eligibility requires complete,
untruncated data and either:

1. one homogeneous cohort with at least 20 independent runs and at least 3 PASS
   and 3 FAIL; or
2. one controlled reproduction with at least 10 isolated independent runs and
   at least 2 PASS and 2 FAIL.

A proposal is `INELIGIBLE` unless all fields are concrete:

- stable proposal ID and canonical test key, current test-source path/revision, test
  binary ID/revision, run-set/cohort IDs, manifest revision, included run IDs, counts,
  rate and Wilson interval;
- evidence verdict, hypothesis boundary, stable AC/BUG IDs, criticality, and
  player/release risk;
- accountable owner, tracking issue, approval owner, and supported engine/runner
  quarantine adapter ID/version/revision;
- expiry no later than 14 days or the current sprint end, whichever is sooner;
- replacement coverage test ID, or explicit `NONE` plus a release-blocking gap;
- exact revalidation, removal, rollback/re-enable, and expiry-escalation rules.

The adapter must be selected from the current engine/test configuration. Never
emit a generic pytest, NUnit, GTest, Godot, Unity, Unreal, or CI skip instruction
unless that exact versioned adapter is declared. A proposal describes a possible
future changeset but contains no executable patch.

Report only the state proven by exact external receipts:

| State | Required evidence |
|---|---|
| `SUSPECTED` | Sparse homogeneous mixed outcomes |
| `CONFIRMED` | Confirmation minimum met |
| `PROPOSED` | Complete eligible proposal revision exists |
| `APPROVED` | Human approval receipt binds exact proposal revision, owner, risk, and expiry |
| `APPLIED` | Application receipt binds approval, adapter, pre/post config/test revisions, owner, issue, and expiry |
| `VERIFIED` | Later runner receipt binds applied config and records exact test key as quarantined |
| `EXPIRED` | Expiry passed without verified renewal or resolution |
| `RESOLVED` | Fix receipt, quarantine-removal receipt, and required homogeneous post-fix passing runs all validate |

Never infer `APPROVED` from conversation, `APPLIED` from a report or registry row,
`VERIFIED` from intended configuration, or `RESOLVED` from a closed issue. An
expired quarantine is a release-blocking revalidation gap and cannot silently
remain active. Preserve proposal/application history in the report while current
state may become `RESOLVED`; this skill does not append or remove registry rows.

`status` validates report schema/revision and each explicitly supplied receipt, then
reports this state machine without writing. It may hand exact APPLIED, VERIFIED,
EXPIRED, or RESOLVED receipt paths/revisions to the regression-suite owner, but
never invokes another workflow or performs an upsert.

---

## Phase 6: Stable findings and revision-bound evidence

Create findings only for data integrity, identity, homogeneity, environment,
sample sufficiency, measured flakiness, controlled cause, or quarantine-state
facts. Each finding uses:

```yaml
id: TFF-<category-slug>-<12-lowercase-hex>
category: DATA | IDENTITY | HOMOGENEITY | ENVIRONMENT | SAMPLE | FLAKINESS | CAUSE | QUARANTINE
canonical_test_key: <runner namespace/test/parameter/binary revision or NONE>
cohort_id: <revision or NONE>
state: OPEN | OBSERVED | RESOLVED
first_seen_run_set: <stable ID>
current_run_set: <stable ID>
evidence:
  manifest_revision: <revision>
  run_ids: [<stable IDs>]
  counts: {pass: <int>, fail: <int>, other: <int>}
  interval_95: <bounds or NONE>
claim_boundary: <measured fact, limitation, or controlled cause>
owner_handoff: <role or NONE>
```

Build the stable finding ID from repository ID, category, canonical test key, cohort ID, and a collision sequence; record external-state receipt identity separately. Do not include paths, line numbers, display names,
observed counts/rates, interval bounds, confidence, severity, state, timestamps,
current run-set/build revisions, or report revisions. Coalesce identical identities,
preserve all supporting run IDs, and sort by category, canonical test key, and
cohort ID.

The analysis payload schema is `cgs.test-flakiness-report/v1`. Canonicalize its
machine-readable payload as UTF-8 JSON with lexicographically sorted object keys,
preserved array order, JSON number grammar, and no insignificant whitespace. It
must contain contract/schema versions; manifest and dependency paths/revisions;
parser/tool/receipt identities; all fixed limits; included/excluded runs;
cohorts and environment drift; stable tests; outcome counts, denominators, rates,
intervals and sample limitations; verdicts; hypotheses; quarantine eligibility
and state; stable findings; bounded omissions; producer
`test-flakiness@cgs.test-flakiness/v2`; UUIDv4 analysis ID; and RFC 3339 UTC time.

For every non-`ERROR` analysis, return one fenced `analysis-evidence` block with
schema `cgs.review-evidence/v1`, record ID derived from the canonical record after
omitting only `record_id`, artifact kind `test-flakiness-analysis`, artifact
identity `<run_set_id>/<manifest_revision>`, payload revision, producer, run/time,
coverage `COMPLETE` or `PARTIAL`, all finding IDs, and:

```yaml
quarantine_authority: NONE
gate_evidence_candidate: false
persistence: NONE | VERIFIED_FILE
report_path: <normalized path or NONE>
report_file_revision: <revision or NONE>
write_receipt_id: <revision or NONE>
```

Partial evidence truthfully proves only its limitations and included local facts;
it can never support confirmation or quarantine. The evidence record never grants
approval, application, regression-selection, release, or test-change authority.

---

## Phase 7: Output and optional report persistence

Return these headings exactly once and in order for `analyze`:

1. `Result and Persistence`
2. `Dataset and Tool Identity`
3. `Run Validation`
4. `Homogeneous Cohorts`
5. `Environment Drift`
6. `Per-Test Statistics and Uncertainty`
7. `Evidence Verdicts`
8. `Cause Hypotheses`
9. `Quarantine Assessment`
10. `Stable Findings`
11. `Bounded Omissions`
12. `Owner Handoffs`
13. `Analysis Evidence`

Always report independent axes:

- `analysis_result`: `COMPLETE`, `PARTIAL`, or `ERROR`;
- `report_persistence`: `NOT_REQUESTED`, `WRITTEN`, `UNCHANGED`, `DECLINED`,
  `CONFLICT`, or `FAILED`; and
- per-test/cohort evidence verdict and quarantine state.

Omitting or declining persistence never blocks, erases, or changes completed
analysis. Persistence failure changes only `report_persistence`.

With `--persist`, derive exactly
`production/qa/flakiness/flakiness-report-<run-set-id>-<UTC-run-id>.md`.
Validate that the normalized target is inside that directory and is not a
symlink. The single report contains the human-readable sections plus the exact
canonical payload, but not the post-write evidence record or write receipt.
Immediately before writing, revalidate every
input. If the target exists with identical bytes, do not rewrite and report
`UNCHANGED`. If it differs, return `CONFLICT` and preserve it; never overwrite or
rename a concurrent/user report. Otherwise write only that one file, read it back
byte-for-byte, and return `WRITTEN` only after reporting its revision and a
`cgs.analysis-report-write-receipt/v1` binding target path, payload revision, evidence
artifact identity, persisted-file revision, writer contract, and UTC time. record
the receipt ID first, then the post-write evidence record may bind that receipt
ID and file revision; the receipt never embeds the evidence record ID, avoiding a
cyclic revision. A denied write or missing output directory yields `DECLINED` or
`FAILED` while analysis remains available in conversation.

For `status`, return `Result`, `Report Identity`, `Receipt Validation`,
`Quarantine State`, `Expiry and Resolution`, and `Owner Handoffs`; emit no new
analysis finding or report write.

After output, stop. Do not launch tests, request quarantine approval, apply a
skip, update regression selection, create an issue/story, edit code, or chain
into another workflow.
