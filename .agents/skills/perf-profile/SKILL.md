---
name: perf-profile
description: "Prepares bounded performance captures or analyzes validated runtime profiler exports against versioned platform budgets, without modifying project files."
---

## Read-only contract and invocation

Invoke this workflow in exactly one mode:

```text
$perf-profile prepare-capture --manifest <capture-request-path>
$perf-profile analyze-export --manifest <analysis-request-path> --input <profiler-export-path>
  [--baseline <baseline-report-or-export-path>]
```

Contract version: `cgs.perf-profile/v2`.

This skill is strictly read-only. It may inspect configuration, validate an
export, normalize measurements in memory, calculate statistics, and return a
capture plan or performance report in conversation. It never launches the game
or profiler, records a capture, edits a project or source file, changes a
performance budget, writes a report, persists evidence, updates a tracker,
creates a follow-up task, or implements an optimization. A separate recorder may
later persist the exact returned bytes under the versioned
`cgs.performance-report-recorder-receipt/v1` contract defined below. Defining that
external interface does not give this analyzer write authority.

Exactly one mode is required. Reject missing or extra positional arguments,
duplicate or unknown options, option values beginning with `--`, globs, URLs,
directories, symlinks, junction escapes, and paths outside the repository.
`--input` is required only for `analyze-export`; `--baseline` is optional only in
that mode. Do not infer a latest capture, build, baseline, budget, platform,
scenario, or profiler export.

For invalid invocation or unusable primary input return `ERROR`, name the input
and reason, emit no budget verdict or evidence record, and stop.

---

## Phase 0: Freeze instructions, request, and bounds

Resolve the repository root and canonicalize all supplied paths before reading
content. Load every applicable `AGENTS.md` from the root to each selected file in
root-to-target order and list them in the output. Read the manifest in full and
require schema `cgs.performance-request/v2`.

Both modes require these stable request fields:

- `request_id`, `mode`, and an explicit ordered matrix of stable
  `platform_profile_id`, `hardware_class_id`, and `scenario_id` cells;
- an exact build identity comprising `build_id`, `artifact_sha256`,
  `source_commit`, `source_tree_state`, `configuration`, engine product/version,
  and engine executable or package receipt SHA-256;
- exact repository-relative paths and SHA-256 values for a platform profile,
  hardware profile, scenario definition, adapter registry, metric registry, unit
  registry, comparison policy, and performance budget manifest;
- capture constraints: warm-up duration, measured duration, repetition count,
  sample interval, seed or `NONE`, save/checkpoint or `NONE`, input-script ID and
  hash or `NONE`, graphics preset, resolution, render scale, VSync, frame cap,
  power mode, thermal policy, background-load policy, and profiler-overhead mode;
- required metric IDs and markers for every matrix cell; and
- whether one optional analyst review is requested.

The manifest may select less work but cannot raise these fixed limits:

| Resource | Fixed maximum |
|---|---:|
| Matrix cells | 256 |
| Primary export files | 64 |
| Baseline export files | 64 |
| Bytes per selected file | 512 MiB |
| Aggregate selected input bytes | 2 GiB |
| Series per export | 4,096 |
| Samples per series | 10,000,000 |
| Repetitions per cell | 128 |
| Markers per export | 100,000 |
| Required metrics per cell | 512 |
| Finding records | 4,096 |
| Rows rendered per output section | 500 |
| One adapter execution | 30 seconds |
| All adapter executions | 300 seconds |
| Adapter receipt bytes | 1 MiB |

Do not partially read a selected manifest, profile, registry, policy, budget, or
receipt. Before parsing a profiler export, reject it if its size exceeds the
per-file or aggregate bound. If declared work exceeds a structural limit, return
`ERROR — REQUEST EXCEEDS FIXED BOUND`. If a valid export is within the byte bound
but normalized trace content exceeds a series, sample, marker, repetition, metric,
finding, or rendering limit, stop at the stated deterministic boundary, record
the complete candidate identity digest, included and omitted counts, boundary,
and overflow digest, and return `PARTIAL — BOUNDED TRACE`; never extrapolate an
overall verdict from the retained prefix.

Read every selected configuration artifact as exact bytes, verify its declared
SHA-256, and record its normalized repository-relative path and hash. A missing,
changed, malformed, ambiguous, or unsupported critical configuration artifact is
an `ERROR` before analysis. Recompute all selected configuration and input hashes
immediately before returning. If any changed, return `ERROR — INPUT CHANGED
DURING ANALYSIS` without a budget verdict or evidence record.

---

## Phase 1: Resolve platform budgets and metric semantics

The platform profile, hardware profile, scenario definition, metric registry,
unit registry, comparison policy, and budget manifest are authoritative only at
their verified versions and hashes.

### Budget source and precedence

Require budget schema `cgs.performance-budget/v2`. Resolve one rule for every
required metric in every platform-by-hardware-by-scenario cell. Apply precedence
from most specific to least specific:

1. exact platform profile + hardware class + scenario + metric;
2. exact platform profile + scenario + metric;
3. exact platform profile + hardware class + metric;
4. exact platform profile + metric; and
5. declared project fallback + metric, only when the budget manifest explicitly
   permits fallback for that metric.

The budget path is selected by the request and must match the applicable
technical-preferences declaration, when that declaration exists. `AGENTS.md` and
technical preferences may constrain governance and identify the manifest, but
prose numbers are not executable thresholds. No platform default, common target,
or observed value may be invented. Two equally specific applicable rules, an
unknown operator, incompatible unit, missing required rule, manifest mismatch,
or invalid fallback produces `PARTIAL — BUDGET COVERAGE`; local measurements may
be reported but no cell or overall verdict may be synthesized across the gap.

Every rule must declare a stable `rule_id`, metric ID, comparison operator,
threshold, canonical unit, evaluation statistic, allowed exceedance or spike
policy, minimum measured duration, minimum repetitions, warm-up requirement, and
severity mapping. Record the selected rule ID, specificity level, source path,
and source hash beside each result.

### Units and sample semantics

Require metric schema `cgs.performance-metric-registry/v1` and unit schema
`cgs.performance-unit-registry/v1`. Each metric defines dimension, canonical
unit, direction (`lower-is-better`, `higher-is-better`, or bounded), sample
semantics, aggregation eligibility, and valid numeric domain. Convert only by an
explicit versioned rule in the selected unit registry and record conversion ID,
source unit, canonical unit, factor or formula, registry version, and hash.

Never infer that FPS and frame time are interchangeable, convert decimal and
binary byte units silently, merge CPU and GPU time, or aggregate counters,
gauges, durations, rates, and percentages under one formula. Unknown units,
dimension mismatch, NaN, infinity, counter reset without declared handling,
mixed sampling semantics, or out-of-domain values make the affected metric
invalid and therefore coverage `PARTIAL`. Preserve raw numeric precision during
calculation and apply only the comparison policy's display rounding after all
decisions.

---

## Phase 2: Prepare a capture plan

In `prepare-capture`, do not parse runtime data and never issue a performance
verdict. Validate the full request matrix, build identity, profiles, scenario,
registries, policy, and budget coverage. Return `MEASUREMENT REQUIRED` with one
deterministic row per platform-by-hardware-by-scenario cell containing:

- exact build artifact and source identity;
- platform profile, hardware class, OS/driver, power, and thermal requirements;
- scenario version/hash, seed, save/checkpoint, input script, graphics settings,
  resolution, render scale, VSync, frame cap, and background-load rules;
- warm-up, duration, sample interval, repetitions, required markers and metrics;
- required profiler product/version, exporter ID/version, adapter ID/version,
  adapter executable or package hash, export schema/version, and overhead mode;
- applicable budget rule IDs and canonical units; and
- expected export filenames and the exact `analyze-export --manifest ...
  --input ...` handoff, without claiming the files already exist.

If a required identity or budget rule is absent, return `PARTIAL — MEASUREMENT
REQUIRED`, enumerate the unresolved fields or cells, and omit all verdicts. Static
source observations may appear only in a separate `UNMEASURED HYPOTHESES`
section; they are not findings, runtime evidence, bottlenecks, regressions, or
proof that any budget is met or missed.

The capture plan is not evidence, is never gate-eligible, and is never persisted
by this skill.

---

## Phase 3: Validate profiler adapters and normalize exports

In `analyze-export`, `--input` must identify one regular file or one bounded
manifest listing exact regular files. Require each raw export to identify its
exporter and schema/version. Select exactly one entry from a verified
`cgs.profiler-adapter-registry/v1` by exact exporter product, exporter version,
export schema, schema version, and platform profile. Ambiguous or absent matches
are unsupported.

An adapter entry is valid only when it declares:

- stable adapter ID and semantic version;
- exact executable/package identity and SHA-256;
- supported exporter products, versions, schemas, and platform profiles;
- deterministic arguments, parser schema, metric and unit mappings, marker
  mapping, output schema `cgs.performance-trace/v1`, and receipt schema
  `cgs.profiler-adapter-receipt/v1`;
- isolation policy forbidding network access, project writes, child-process
  expansion, and undeclared reads; and
- validator tests and their immutable receipt IDs for the exact adapter version.

Execute only the declared adapter with fixed arguments inside the stated time
and resource limits. Hash the raw input before execution. Validate the resulting
receipt: adapter ID/version/hash, exact argv, start/end UTC timestamps, exit
status, raw-input path/hash/bytes, normalized-output hash/bytes, warnings, and
validator identity must bind to this run. Reject a missing, oversized,
malformed, hash-mismatched, unvalidated, timed-out, or nonzero adapter receipt.
Never parse an unknown format heuristically or edit the raw export.

The normalized `cgs.performance-trace/v1` must retain, for every sample and
marker, raw source identity, repetition, timestamp relative to measured-window
start, metric ID, numeric value, source unit, canonical unit, and conversion ID.
It must also carry the complete capture provenance from Phase 0 plus profiler
product/version, exporter ID/version, adapter ID/version/hash, export settings,
overhead mode, warm-up completion, measured duration, sample interval, capture
start UTC, repetition identity, and raw/normalized hashes.

Classify outcomes mechanically:

- no usable primary export, invalid primary file identity, unsupported primary
  schema, or adapter execution/receipt failure: `ERROR`, no statistics, budget
  verdict, or evidence record;
- at least one usable cell but any required export, cell, repetition, metric,
  marker, critical provenance field, or measured-window requirement is missing
  or invalid: `PARTIAL — MEASUREMENT COVERAGE`, local statistics only and no
  overall verdict; and
- all requested cells and requirements validate: continue with complete
  coverage.

Do not replace a missing capture field with the analysis machine's state, file
metadata, repository HEAD, current time, a nearby profile, or a user assertion.

---

## Phase 4: Calculate per-cell statistics and deterministic verdicts

Analyze each platform-profile-by-hardware-class-by-scenario-by-metric cell
independently. Never pool samples across cells, silently concatenate repetitions,
or average platform results. Apply the selected comparison policy exactly.

For each repetition and for the policy-defined combined view, report:

- valid sample count, measured duration, minimum, arithmetic mean, p50, p95,
  p99, and maximum in canonical units;
- threshold exceedance count, rate, and total/longest consecutive exceedance
  duration;
- spike or hitch count, total duration, longest duration, and worst magnitude,
  using the exact rule window and threshold; and
- missing/invalid sample count and the policy decision inputs.

Percentiles use the comparison policy's declared algorithm and interpolation.
Time-weighted metrics use timestamp deltas; sample-weighted metrics do not.
Threshold equality follows the rule operator. Do not substitute an average for a
p95/p99/max rule, hide a spike behind an average, or create an unconfigured
confidence interval. If the rule requires more repetitions, duration, or samples
than the trace provides, coverage is `PARTIAL`.

For complete cells, evaluate each metric exactly as one of:

- `WITHIN BUDGET`: every required decision condition passes;
- `CONCERNS`: the rule's concern band or allowed transient-spike condition
  matches without any over-budget condition; or
- `OVER BUDGET`: any configured over-budget condition matches.

Cell verdict is the worst metric verdict under the manifest's explicit ordering
`OVER BUDGET > CONCERNS > WITHIN BUDGET`. An overall verdict exists only when
every requested cell is complete; it is the worst complete cell verdict using
the same ordering. Otherwise overall verdict is `NONE — PARTIAL COVERAGE`.

Report a matrix coverage ledger with every requested cell, expected and observed
repetitions, required and valid metrics, adapter receipt IDs, budget-rule IDs,
status, and omission reason. This ledger, not a summary count, determines
completeness.

---

## Phase 5: Compare an explicit baseline without false causality

Never infer a baseline. When `--baseline` is provided, hash and validate it as
either a complete `cgs.performance-report/v1` payload with a valid embedded
`cgs.review-evidence/v1` record, or profiler exports processed through the same
adapter-validation path. A report also needs an exact current
`cgs.performance-report-recorder-receipt/v1` that binds its canonical target and
exact bytes if it is offered as durable evidence; without one it may be used as
disclosed conversational context only, never as gate evidence.

Compute deltas only when the comparison policy permits and these keys match:
platform-profile ID/version/hash, hardware-class ID/version/hash, scenario
ID/version/hash, seed/save/input identity, graphics/resolution/render-scale,
VSync/frame-cap, power/thermal/background-load policy, profiler/exporter/adapter
identity, export and overhead settings, metric ID, sample semantics, canonical
unit and conversion rule, warm-up/duration/sample interval/repetition policy,
budget manifest/rule, and comparison-policy version/hash. Build ID, artifact hash,
and source commit are the explicitly differing comparison axis.

For each comparable metric report absolute and percentage delta for the exact
policy statistics, sample and repetition counts, and the policy's decision
result. Use `REGRESSION`, `IMPROVEMENT`, or `NO MATERIAL CHANGE` only when a
versioned rule with sufficient data authorizes that label. Otherwise report
`DESCRIPTIVE DELTA ONLY`. For incompatible inputs report
`NOT COMPARABLE — <exact mismatched keys>` and calculate no delta.

Temporal adjacency, profiler markers, stack samples, correlation, a hot function,
or a source pattern does not establish causality. Findings must say `observed`,
`correlated`, or `candidate`, never that a function, asset, system, commit, or
thread caused the result unless a separately identified controlled experiment
under the comparison policy isolates that factor. Recommendations are bounded
hypotheses with a proposed experiment and success metric; do not promise an FPS,
latency, memory, or percentage gain.

---

## Phase 6: Normalize stable findings and optional analyst review

Create a finding only for a rule failure, coverage defect, incompatible baseline,
adapter warning that affects interpretation, or statistically supported change.
Each finding uses:

```yaml
id: PFF-<category-slug>-<12-lowercase-hex>
category: BUDGET | COVERAGE | ADAPTER | BASELINE | STATISTICS
metric_id: <stable ID or NONE>
rule_id: <stable ID or NONE>
cell_id: <platform-profile>/<hardware-class>/<scenario or NONE>
status: OPEN
first_seen_build_id: <stable build ID>
current_build_id: <stable build ID>
evidence:
  trace_sha256: <hash or NONE>
  repetition_ids: [<stable IDs>]
  statistic: <name or NONE>
  observed: <value and canonical unit or NONE>
  threshold: <operator, value, unit or NONE>
claim_boundary: <observation, not unsupported cause>
recommendation: <bounded hypothesis and experiment or NONE>
```

Compute the 12-hex suffix from SHA-256 of UTF-8 canonical JSON containing only
the repository identity, category, metric ID, rule ID, platform-profile ID,
hardware-class ID, and scenario ID. Do not include file paths, line numbers,
severity, observed values, thresholds, status, timestamps, current build hashes,
or report hashes. Sort findings by category, metric ID, rule ID, and cell ID.
Coalesce identical canonical identities and list all supporting repetitions.

When `analyst_review: true`, the skill may ask at most one
`performance-analyst` for a read-only review of the already calculated bounded
packet. The reviewer receives no source tree and may not change measurements,
statistics, rules, findings, or verdicts. Total wait is fixed at 180 seconds in
at most three waits of 60 seconds, with no retry or replacement. Late responses
are ignored. Record review status as `COMPLETE`, `NOT REQUESTED`, `UNAVAILABLE`,
`TIMED OUT`, or `FAILED` and include bounded advisory notes separately. Reviewer
failure never changes deterministic calculations or measurement coverage and
does not convert an observation into a causal claim. Also record
`review_coverage` as `COMPLETE` for a completed requested review,
`NOT REQUESTED` when omitted, or `PARTIAL` for unavailable, timed-out, failed,
or ignored-late review. Partial review coverage is disclosed independently from
measurement coverage and the calculated budget verdict. It does not authorize
more delegation.

---

## Phase 7: Return a canonical read-only report

Return exactly one mode-appropriate report in conversation and stop.

`prepare-capture` headings:

1. `Result`
2. `Request and Configuration Identity`
3. `Capture Matrix`
4. `Profiler and Adapter Requirements`
5. `Budget and Unit Coverage`
6. `Unresolved Capture Requirements`
7. `Unmeasured Hypotheses`
8. `Handoff`
9. `Evidence Eligibility`

`analyze-export` headings:

1. `Result`
2. `Request, Build, and Capture Identity`
3. `Input and Adapter Receipts`
4. `Coverage Ledger`
5. `Per-Cell Statistics`
6. `Budget Evaluation`
7. `Baseline Comparison`
8. `Findings`
9. `Hypotheses and Experiments`
10. `Analyst Review`
11. `Bounded Omissions`
12. `Evidence Record`

The runtime payload uses schema `cgs.performance-report/v1`. Canonicalize as
UTF-8 JSON with lexicographically sorted object keys, preserved array order,
JSON number grammar, and no insignificant whitespace. The canonical payload must
include contract and schema versions; request, build, platform, hardware,
scenario, capture, profiler, exporter, adapter, registry, policy, budget, raw
input, normalized trace, and baseline identities/hashes; limits; coverage ledger;
statistics; rule decisions; verdicts; stable findings; review status and review
coverage; omissions;
producer `perf-profile@cgs.perf-profile/v2`; and a UUIDv4 run ID and UTC timestamp
used only as run metadata.

For a complete `analyze-export` result only, emit one fenced block labeled
`gate-evidence` containing a `cgs.review-evidence/v1` record with:

```yaml
schema: cgs.review-evidence/v1
record_id: <sha256 of canonical record excluding only record_id>
artifact_kind: performance-runtime-report
artifact_identity: <request_id>/<build_id>
artifact_sha256: <sha256 of canonical cgs.performance-report/v1 payload>
producer: perf-profile@cgs.perf-profile/v2
run_id: <UUIDv4>
generated_at_utc: <RFC 3339 UTC>
coverage: COMPLETE
verdict: WITHIN BUDGET | CONCERNS | OVER BUDGET
performance_targets_met_candidate: true | false
persistence: NONE
gate_evidence_candidate: true
recorder_receipt: NONE
```

`performance_targets_met_candidate` is true only for `WITHIN BUDGET`. This record
is hash-bound but not durable evidence because the skill is read-only. It always
retains `persistence: NONE` and `recorder_receipt: NONE`; an external receipt never
rewrites the analyzer output.

### Independent performance-report recorder contract

The only compatible durable-recording interface is
`cgs.performance-report-recorder-receipt/v1`. The independent recorder receives
the exact complete returned report bytes and all exact source bindings, recomputes
the embedded `cgs.performance-report/v1` payload hash and
`cgs.review-evidence/v1` record ID, and proves a create-only compare-and-set plus
read-back. The analyzer, its optional analyst reviewer, and the recorder identities
must all differ.

Compute `performance_candidate_sha256` over canonical JSON containing the exact
request ID/hash; build ID, candidate ID, artifact hash, source commit/tree state,
engine/configuration; ordered platform-profile, hardware-class and scenario
identities/hashes; budget path/schema/hash and ordered rule IDs; policy/registry/
adapter/profiler/exporter identities/hashes; ordered raw-input and normalized-trace
hashes; canonical payload hash; evidence record ID; and report raw-byte hash. Use
the lowercase digest without `sha256:` in these exact paths:

```text
production/qa/evidence/performance/<performance_candidate_sha256>/reports/<record_id_sha256>.md
production/qa/evidence/performance/<performance_candidate_sha256>/receipts/<record_id_sha256>.yaml
```

`record_id_sha256` is the lowercase digest portion of the embedded generic
`record_id`. Both targets must be absent; a recorder may not choose an alias,
overwrite a prior result, or derive identity from a timestamp.

The receipt is canonical UTF-8 YAML and contains at least:

```yaml
schema: cgs.performance-report-recorder-receipt/v1
receipt_id: sha256:<canonical receipt payload with receipt_id omitted>
recorder: {identity: <independent ID>, version: <version>, implementation_sha256: <hash>}
producer: perf-profile@cgs.perf-profile/v2
source:
  report_raw_sha256: sha256:<hash>
  report_bytes: <positive integer>
  payload_schema: cgs.performance-report/v1
  payload_sha256: sha256:<hash>
  evidence_schema: cgs.review-evidence/v1
  evidence_record_id: sha256:<hash>
  analyzer_persistence: NONE
  analyzer_recorder_receipt: NONE
identity:
  performance_candidate_sha256: sha256:<hash>
  request: {id: <ID>, sha256: sha256:<hash>}
  build: {id: <ID>, candidate_id: <ID>, artifact_sha256: sha256:<hash>, source_commit: <ID>, source_tree_state: <state>, configuration: <ID>}
  platform_matrix_sha256: sha256:<ordered platform/hardware/scenario identity digest>
  budget: {schema: cgs.performance-budget/v2, path: <canonical path>, sha256: sha256:<hash>, rule_set_sha256: sha256:<hash>}
  input_set_sha256: sha256:<ordered raw export/adapter receipt/normalized trace digest>
target:
  report_path: production/qa/evidence/performance/<performance_candidate_sha256>/reports/<record_id_sha256>.md
  receipt_path: production/qa/evidence/performance/<performance_candidate_sha256>/receipts/<record_id_sha256>.yaml
  expected_report_preimage: ABSENT
  expected_receipt_preimage: ABSENT
  persisted_report_sha256: sha256:<same report raw hash>
  persisted_report_bytes: <same byte count>
write:
  compare_and_set: CREATED
  write_started_at_utc: <RFC3339 UTC>
  write_completed_at_utc: <RFC3339 UTC>
  read_back: VERIFIED
  read_back_at_utc: <RFC3339 UTC>
  read_back_sha256: sha256:<same report raw hash>
decision:
  verdict: WITHIN BUDGET | CONCERNS | OVER BUDGET
  performance_targets_met: true | false
  evidence_persistence: RECORDED
  gate_evidence_eligible: true
```

The receipt repeats every exact candidate/build/platform/budget/input binding; the
set digests are not substitutes for the underlying bounded ordered rows. It is
valid only for a complete analyzer record whose coverage is `COMPLETE`, whose
candidate flag agrees with the unchanged verdict, whose report target bytes equal
the returned bytes, and whose CAS/read-back are verified. `gate_evidence_eligible:
true` means the durable record is admissible for either a positive or negative gate
decision; it does not mean targets passed. `performance_targets_met` is true only
for the unchanged `WITHIN BUDGET` verdict. `CONCERNS` and `OVER BUDGET` remain
eligible conclusive evidence with `performance_targets_met: false`.

A receipt with a changed verdict/payload, reused target, wrong canonical path,
identity overlap, partial matrix, missing underlying bindings, stale hash,
non-created CAS, or failed/unknown read-back is invalid and gate-ineligible. The
recorder cannot change calculations, coverage, findings, or verdict, and cannot
turn preparation, partial, bounded, error, or measurement-required output into a
complete report.

For `MEASUREMENT REQUIRED`, any `PARTIAL`, or `ERROR`, emit no `gate-evidence`
block and set evidence eligibility to `INELIGIBLE`. A capture plan, static scan,
truncated trace, incomplete matrix, unsupported adapter, missing provenance,
missing budget rule, incompatible baseline, or unpersisted conversation is never
proof that performance targets are met.

After returning the report, do not modify files or chain into `$tech-debt`,
`$architecture-decision`, `$create-stories`, implementation, retesting, or any
other workflow. Scope changes, budget changes, architecture decisions,
optimization implementation, and durable evidence recording require separate
explicitly authorized work.
