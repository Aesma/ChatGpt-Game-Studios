---
name: perf-profile
description: "Prepare reproducible performance captures or analyze validated runtime profiler exports against versioned platform-and-scenario budgets with hash-bound evidence."
---

# Performance Profile

This workflow analyzes measurements; it does not turn static suspicion into measured
performance. Without valid runtime samples it may produce a capture plan and optional
static candidates, but it must not report current performance, headroom, expected
gain, budget status, or a completion verdict.

## Invocation contract

Use exactly one mode:

```text
$perf-profile prepare-capture --manifest {capture-request-path}
$perf-profile analyze-export --manifest {analysis-request-path} --input {profiler-export-path} [--baseline {runtime-report-or-export-path}]
```

Parse and validate arguments before reading project files, delegating, asking for
authorization, or writing. With no mode/manifest, show both usage lines and stop with
no reads, writes, delegates, or verdict. Reject unknown or duplicate flags, missing
values, directories, unsafe paths, path traversal, unsupported schemas, and inputs
outside the manifest's authorized read roots.

The request manifest contains:

- `Artifact Type: performance-capture-request` or `performance-analysis-request` and
  `Schema Version: 1`;
- stable request/run IDs and exact mode;
- exact engine/project identity, engine execution-receipt path/hash, build ID,
  build artifact/source-tree/commit hashes, and build configuration;
- exact budget-manifest path/hash and required platform × hardware class × scenario
  matrix;
- exact platform profile, hardware/device ID and specification, OS/driver/runtime,
  graphics preset, resolution/aspect, frame cap/vsync, power/thermal state, and input
  playback/seed sources;
- stable scenario ID/version/source hash, warmup, duration, repetitions, sampling
  interval, profiler/exporter identity and supported schema version;
- exact input and optional baseline path/hash for analysis;
- file/byte/sample budgets, per-task timeout, optional reviewer timeout, output path
  and expected base hash or `ABSENT` when persistence is requested;
- evidence recorder/owner, mutation authority, and explicit non-writes.

Normalize real paths and reject symlinks or junctions escaping the declared roots.
Do not scan for a convenient profiler export, newest prior report, budget, or target
hardware. An explicitly listed path and exact current hash are mandatory.

## Mode A: prepare-capture

This mode never emits `WITHIN BUDGET`, `CONCERNS`, or `OVER BUDGET`. Its result is:

`Analysis Status: MEASUREMENT REQUIRED`

Validate the capture request and budget matrix, then return a platform- and
scenario-specific checklist:

1. verify the exact build/artifact/source and engine receipt hashes;
2. identify target platform, hardware/device, OS/driver/runtime, power/thermal mode,
   display resolution/aspect, graphics preset, frame cap, and vsync;
3. pin stable scenario/version, seed/save/input script, start state, and expected end;
4. define warmup, capture duration, repetitions, sampling interval, profiler settings,
   overhead notes, and cache/restart policy;
5. declare required metrics and units from the budget manifest;
6. run the scenario on target hardware and record dropped frames/hitches plus any
   manual observations with timestamps;
7. export the supported runtime schema, preserve raw bytes, and compute SHA-256;
8. capture logs/build/engine/tool identities and validate the export before analysis.

If a requested engine exporter is not supported by the declared normalization
adapter, identify the missing adapter/schema and stop. Do not invent UI instructions
or silently reinterpret columns.

Optional static candidates must be explicitly requested and bounded to declared
paths. Label them `STATIC CANDIDATES — UNMEASURED`; include file/line and why it may
deserve an instrumentation marker, but assign no performance severity, budget impact,
headroom, or expected gain. Static candidates are never gate evidence and never cause
an optimization recommendation.

Capture planning is read-only and returns its checklist in conversation. Persisting
a capture plan requires a separately requested exact output path, owner, base hash,
candidate hash, and one explicit report-write authorization. It still carries no
budget verdict.

## Runtime export schema

`analyze-export` accepts only a declared adapter that produces normalized
`perf-profile-export-v1`. Preserve the raw input hash and normalized-data hash. The
normalized export requires:

```text
schema/version
exporter product/version and profiler settings/overhead notes
engine product/version/executable receipt hash
build ID, build artifact hash, source tree/commit hash, configuration
platform profile ID/hash, platform, OS/driver/runtime
hardware/device ID and CPU/GPU/RAM/device details
power/thermal mode, graphics preset, resolution/aspect, frame cap/vsync
scenario ID/version/source hash, seed/save/input-playback hashes
capture/run/repetition IDs, captured-at UTC
warmup duration, sample duration, sample interval, frame/sample count
metric definitions, units, direction, timestamps/frame indices, numeric samples
logs/markers and their hashes
```

Required metric series depend on the budget manifest and may include frame, CPU,
GPU, render-thread, memory, allocation/GC, draw-call, loading, streaming, bandwidth,
or subsystem timings. Do not fabricate an absent metric.

Reject malformed JSON/CSV, unsupported exporter/schema versions, empty series,
mixed or unknown units, duplicate frame/sample IDs, non-monotonic timestamps,
impossible durations, non-finite values including NaN/Infinity, negative values where
invalid, sample-count mismatches, or a raw-input hash mismatch. Return
`Analysis Status: ERROR`, `Budget Verdict: null`, and no gate evidence.

Missing required provenance, hardware detail, scenario identity, build identity,
required metric, or budget association produces
`Analysis Status: PARTIAL — MEASUREMENT REQUIRED`, `Budget Verdict: null`. Preserve
valid facts but never infer the missing identity.

## Budget source and precedence

Budgets come only from an exact, versioned `performance-budget-v1` manifest named by
the request. A prose FPS target or generic value in project instructions is context,
not an executable budget. If technical preferences point to the budget manifest,
verify both path and hash; never hardcode a frame time, memory, draw-call, load, or
network limit.

Each budget rule has stable rule ID, metric ID, unit/direction, platform profile,
hardware class, scenario or wildcard, statistic/window, threshold, minimum samples/
duration/repetitions, allowed violation count/rate/duration, severity on failure
`CONCERN` or `OVER`, and effective version/date.

Resolve exactly one rule per metric using this precedence:

1. exact platform + hardware/device class + scenario;
2. exact platform + hardware/device class + explicit scenario wildcard;
3. exact platform + declared general hardware class + explicit wildcard.

Never use an engine default. Equal-precedence conflicts, missing required rules,
unit mismatch, expired rules, or a budget whose platform/hardware/scenario does not
match the capture yields `Budget Verdict: null` for the cell and prevents overall
gate eligibility.

## Mode B: analyze-export

### Phase 1: Validate identity and coverage

Read only the exact request, input, budget, and optional baseline paths. Recompute all
hashes. Map every run/repetition to one required matrix cell:

`platform-profile × hardware/device-class × scenario-id/version`

Detect unexpected cells, duplicates, and missing repetitions. Each cell is evaluated
independently. Missing a required cell or minimum repetition/sample duration makes
overall coverage `PARTIAL`; valid complete cells may retain local verdicts, but the
overall `Budget Verdict` is null and `gate_evidence_eligible` is false.

### Phase 2: Compute runtime metrics

For every metric/repetition compute from numeric runtime samples:

- count, duration, mean, median/p50, p95, p99, min, and max;
- threshold-exceed count and rate;
- longest consecutive exceedance and cumulative exceedance duration;
- spike/hitch frame indices or timestamps, values, duration, and associated markers;
- between-repetition spread and confidence/variance fields required by the manifest.

Use a documented percentile interpolation method and deterministic rounding only for
display; compare thresholds using unrounded values. Keep frame/sample IDs so every
spike is traceable to raw input. Do not estimate missing runtime values from code or
neighboring samples.

### Phase 3: Deterministic verdict

Evaluate each budget rule exactly as written:

1. any failed required rule whose failure severity is `OVER` → cell verdict
   `OVER BUDGET`;
2. otherwise any failed `CONCERN` rule, including p99/max/spike/hitch rules → cell
   verdict `CONCERNS`;
3. otherwise, after all required rules and coverage pass → cell verdict
   `WITHIN BUDGET`.

An average within budget never overrides a failed p95/p99/max/spike rule. A systemic
sustained failure is `OVER BUDGET` when the matching rule says `OVER`. Calculate the
overall verdict as the worst valid cell: `OVER BUDGET` > `CONCERNS` >
`WITHIN BUDGET`. Overall verdict exists only when every required cell and rule was
evaluated from valid runtime data.

Report counts of required cells/metrics/rules passed and evaluated. A user may accept
risk, but that does not alter the computed verdict, close findings, or set
`performance_targets_met` to true.

### Phase 4: Findings and evidence-bounded recommendations

Every failed rule creates stable finding:

`PFF-{platform-id}-{hardware-id}-{scenario-id}-{metric-id}-{rule-id}`

Record severity, input/normalized/budget hashes, build/platform/hardware/scenario
identity, repetition/window, observed unrounded statistic, expected rule, spike frame
IDs, confidence/variance, correlated profiler marker/hotspot, and status.

Recommendations are measurement experiments, not implementation orders. Tie each to
finding IDs and measured markers. State hypothesis, expected direction, risk, owner
domain, proposed instrumentation/change, and the exact same capture matrix needed to
validate it. Do not claim a numerical expected gain unless a comparable measured
experiment supplies it; label any unmeasured estimate explicitly `HYPOTHESIS`.

This workflow never edits code, assets, engine settings, budgets, plans, scope, ADRs,
backlogs, or finding status. Optimization, scope, scheduling, and architecture
decisions belong to separately authorized owners/workflows.

### Phase 5: Comparable delta

A baseline is considered only when its path/hash is explicit. Compare it with current
data only if normalized schema/adapter, metric definitions/units, platform profile,
hardware/device class, scenario ID/version/source hash, graphics/build configuration,
resolution/aspect, frame cap/vsync, profiler settings, warmup, sampling method, and
budget version are compatible. Build/source IDs may differ and must be shown as the
comparison axis.

If any comparability key differs, output `Delta Status: NOT COMPARABLE` with exact
differences and compute no delta/trend. If comparable, report baseline/current hashes
and absolute/percentage deltas for mean, p50, p95, p99, max, exceedance rate, and hitch
counts. Describe direction, but call a change an improvement/regression only when the
declared repetition/confidence rule supports it; otherwise label it descriptive only.

Do not search directories for a previous report or compare different scenes,
platforms, hardware, settings, or metric windows.

## Optional independent analyst review

After deterministic computation, at most one read-only `performance-analyst` may
review calculation evidence, finding/marker correlation, and experiment proposals.
The reviewer receives exact hashes and cannot recalculate with hidden data, change a
verdict, write files, delegate, or implement fixes.

Cap review at 15 minutes with at most one retry after a malformed/timeout response.
Revoke attempt tokens and ignore late results. Reviewer failure leaves the computed
runtime verdict unchanged and sets `analyst_review: PARTIAL/NOT REVIEWED`; never claim
independent review completion. Analyst review is not required for mathematical gate
eligibility.

## Report persistence and gate evidence

Analysis is read-only unless the request explicitly names one report path. Before a
report write, present the exact operation, normalized path, expected base hash or
`ABSENT`, candidate bytes/hash, maximum size, single recorder, and explicit non-writes;
obtain one report-write authorization. Recheck every input and base hash, write only
that report, then read back and hash it. Scope expansion requires new authorization.

The report uses `performance-runtime-report-v1` and includes:

- report/request/run IDs, generated-at UTC, raw/normalized/budget hashes;
- complete provenance and required/observed coverage matrix;
- per-cell metrics, rule evaluations, findings, overall verdict, and delta record;
- reviewer status, report persistence/read-back hash, and one next action;
- `evidence_kind: RUNTIME_MEASUREMENT`;
- `gate_evidence_eligible`: true only for a persisted, read-back verified, full-
  coverage report whose current input/build/platform/hardware/scenario/budget hashes
  match;
- `performance_targets_met`: true only when gate evidence is eligible and the overall
  verdict is `WITHIN BUDGET`;
- `stale_when`: any bound hash or required matrix changes.

A capture plan or static-candidate output uses
`evidence_kind: STATIC_OR_CAPTURE_PLAN`, `gate_evidence_eligible: false`,
`performance_targets_met: false`, and `Budget Verdict: null`. Conversation-only,
unpersisted, partial, stale, accepted-risk, or hash-mismatched reports are likewise
not eligible. Gate consumers must reject them rather than reinterpret prose.

## Recovery and terminal output

Malformed input returns `ERROR`; missing provenance/coverage/budget evidence returns
`PARTIAL — MEASUREMENT REQUIRED`; no runtime input in prepare mode returns
`MEASUREMENT REQUIRED`. Never output a budget verdict in these states.

If interrupted, resume only from an exact checkpoint/report candidate named in the
request. Re-hash request, input, adapter, normalized data, budget, baseline, build,
platform, hardware, scenario, and report base. Any drift invalidates dependent
calculations and authorization; recompute from the earliest affected phase. Never
reuse stale verdicts or late reviewer output.

For a valid complete analysis, output:

- `Analysis Status: COMPLETE`;
- `Budget Verdict: WITHIN BUDGET | CONCERNS | OVER BUDGET`;
- coverage, provenance, bound hashes, per-cell metrics, spike frames, findings,
  persistence/gate fields, analyst-review status, and exactly one next action.

The next action for measurement-required output is to capture one named missing
matrix cell. For a measured finding it is to hand one stable finding to its proper
owner for a separately authorized experiment. Do not auto-invoke another workflow or
start optimization work.
