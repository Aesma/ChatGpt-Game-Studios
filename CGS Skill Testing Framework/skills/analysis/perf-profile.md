# Skill Test Spec: `$perf-profile`

## Skill Summary

`$perf-profile` contract `cgs.perf-profile/v2` is a strictly read-only,
two-mode workflow. `prepare-capture` validates an explicit
platform-by-hardware-by-scenario matrix and returns `MEASUREMENT REQUIRED`.
`analyze-export` accepts only explicit profiler exports, validates them through a
versioned adapter registry, normalizes metrics and units, calculates bounded
per-cell statistics, applies exact platform budgets, and returns a hash-bound
conversation report.

The skill does not launch a build or profiler, capture data, edit a project,
change a budget, write a report, persist evidence, update a tracker, attribute an
unsupported cause, or implement a recommendation. A complete runtime report is
only a candidate for later persistence by an independent recorder.

Result states are `ERROR`, `MEASUREMENT REQUIRED`,
`PARTIAL — MEASUREMENT REQUIRED`, `PARTIAL — BOUNDED TRACE`,
`PARTIAL — BUDGET COVERAGE`, `PARTIAL — MEASUREMENT COVERAGE`, and complete
runtime results with verdict `WITHIN BUDGET`, `CONCERNS`, or `OVER BUDGET`.

---

## Required test instrumentation

Run every behavioral case in an isolated disposable repository fixture. The
harness must record:

1. recursive path/type/SHA-256 snapshots before and after invocation;
2. every filesystem mutation attempt by the skill and any adapter/reviewer;
3. every file read, exact byte count, canonical path, and read order;
4. every adapter identity, executable/package SHA-256, argv, wall time, exit
   status, raw input hash, normalized output hash, and receipt bytes;
5. every delegated role, start/end time, wait count, completion state, and
   returned advisory-note count;
6. the exact response bytes and all canonical payload/evidence hashes; and
7. a deterministic clock and UUID source for repeatable canonicalization tests.

The mutation guard passes only when snapshots are byte-identical and the
mutation-attempt ledger is empty. The adapter sandbox must deny network access,
project writes, undeclared reads, and child-process expansion. If instrumentation
cannot observe a required property, mark it `UNTESTED`; prose claims and static
inspection are not behavioral evidence. Do not update catalog result fields from
this staged specification.

---

## Static assertions

- [ ] Frontmatter contains only `name` and a non-empty `description`
- [ ] Metadata and skill description both state read-only runtime-export analysis
- [ ] Contract version is exactly `cgs.perf-profile/v2`
- [ ] The two accepted invocations and their exact argument rules are explicit
- [ ] Request, build, platform, hardware, scenario, capture, profiler, exporter,
  adapter, budget, metric, unit, and comparison-policy identity are mandatory
- [ ] Adapter registry and receipt schemas, exact tool version/hash, supported
  exporter/schema matrix, sandbox, timeout, and failure behavior are explicit
- [ ] Fixed file, byte, matrix, series, sample, repetition, marker, metric,
  finding, row, adapter-time, and receipt limits cannot be raised by the request
- [ ] Budget-manifest source, precedence, conflict behavior, rule provenance,
  canonical units, and conversion registry are explicit
- [ ] p50, p95, p99, max, exceedance, hitch/spike, duration, and repetition
  statistics are mandatory; averages cannot mask spikes
- [ ] Each platform-by-hardware-by-scenario-by-metric cell is independent and an
  overall verdict requires complete matrix coverage
- [ ] Baseline is explicit and exact comparability keys and decision labels are
  versioned; incompatible data yields no delta
- [ ] Causal language is prohibited without a controlled comparison; hypotheses
  require an experiment and cannot promise a gain
- [ ] Stable finding IDs exclude paths, line numbers, observed values, thresholds,
  severity/status, timestamps, current build hashes, and report hashes
- [ ] Optional review is limited to one performance analyst, three waits and 180
  seconds, cannot change calculations, and does not authorize more delegation
- [ ] Capture plans, partial/truncated/static results, and unpersisted responses
  are explicitly gate-ineligible
- [ ] Complete report/evidence canonicalization and independent recorder boundary
  are explicit; the skill has no write-authorization branch
- [ ] Scope, budget, architecture, implementation, persistence, and follow-up work
  remain separate explicit decisions and workflows

---

## Canonical fixtures

Unless a case overrides them, use:

- request `REQ-PERF-001`, schema `cgs.performance-request/v2`;
- build `BUILD-101`, artifact SHA-256 `A`, clean source commit `C1`, Development
  configuration, exact engine product/version and executable receipt hash;
- two platform profiles `PLAT-PC-60` and `PLAT-DECK-40`, two hardware classes,
  and scenarios `SCN-HUB` and `SCN-COMBAT`, each with a version and source hash;
- metric registry `cgs.performance-metric-registry/v1`, unit registry
  `cgs.performance-unit-registry/v1`, adapter registry
  `cgs.profiler-adapter-registry/v1`, comparison policy
  `cgs.performance-comparison-policy/v1`, and budget
  `cgs.performance-budget/v2` at declared exact hashes;
- a validated adapter `ADP-GODOT-CSV-1` version `1.2.0` with package SHA-256
  `T`, exporter `Godot Profiler CSV` version `4.6.3`, schema `godot-csv/v3`,
  normalized schema `cgs.performance-trace/v1`, and passing validator receipts;
- three measured repetitions after a 30-second warm-up, each 120 seconds at a
  declared sample interval; and
- canonical frame-time unit `ms`, memory unit `byte`, and percentage unit
  `percent`, with explicit conversion IDs where source units differ.

All placeholder hashes are replaced by syntactically valid 64-hex values in the
actual fixture.

---

## Case 1: Strict modes, paths, and explicit input

Run each independently:

| Input | Expected |
|---|---|
| `$perf-profile` | missing mode `ERROR` |
| `$perf-profile unknown --manifest r.yaml` | unknown mode `ERROR` |
| `$perf-profile prepare-capture` | missing manifest `ERROR` |
| `$perf-profile prepare-capture --manifest r.yaml --input x.csv` | mode-forbidden option `ERROR` |
| `$perf-profile analyze-export --manifest r.yaml` | missing input `ERROR` |
| `$perf-profile analyze-export --input x.csv` | missing manifest `ERROR` |
| `$perf-profile analyze-export --manifest r.yaml --input x.csv --baseline b.json` | accepted grammar |
| duplicate `--input`, `--manifest`, or `--baseline` | duplicate option `ERROR` |
| option value begins with `--` | missing value `ERROR` |
| extra positional argument or unknown option | `ERROR` |
| path is a URL, glob, directory, symlink, outside path, or junction escape | `ERROR` |
| omitted input with a matching export elsewhere in the fixture | `ERROR`; no discovery |

Assertions for every invalid row:

- [ ] Rejected token/path and exact reason are reported
- [ ] No export discovery, adapter execution, statistics, verdict, or evidence
- [ ] Mutation guard passes

For accepted grammar, each path is canonicalized once to a repository-relative
forward-slash path; no latest build, capture, or baseline is inferred.

## Case 2: Capture plan carries complete execution identity

Invoke `prepare-capture` with the canonical fixture and a four-cell matrix.

- [ ] Result is exactly `MEASUREMENT REQUIRED`; there is no runtime verdict
- [ ] All applicable root-to-file instructions are read and listed in order
- [ ] Every cell records build/artifact/source/engine identity
- [ ] Platform-profile and hardware-class versions/hashes, OS/driver, power and
  thermal controls are explicit
- [ ] Scenario ID/version/hash, seed, save/checkpoint, input script/hash,
  graphics, resolution, render scale, VSync, cap, and background load are explicit
- [ ] Warm-up, duration, interval, repetition, marker, and metric requirements are
  concrete and cell-specific
- [ ] Profiler, exporter, export schema, adapter ID/version/hash, and overhead mode
  are concrete
- [ ] Budget rule IDs and canonical units resolve for every metric and cell
- [ ] Expected filenames and exact analyze handoff are prospective, not claimed
  to exist
- [ ] Capture plan says gate-ineligible and no `gate-evidence` block exists
- [ ] Mutation guard passes

## Case 3: Missing capture identity remains measurement-required

Run independent variants missing build artifact hash, engine receipt, scenario
hash, platform profile, hardware class, seed policy, graphics setting, capture
duration, profiler version, export schema, adapter version/hash, or one budget
rule.

- [ ] Each variant is `PARTIAL — MEASUREMENT REQUIRED`
- [ ] Exact missing fields and affected cells are enumerated
- [ ] No runtime, cell, overall, regression, or targets-met verdict exists
- [ ] A nearby repository value or host-machine value is never substituted
- [ ] Static source observations, when present, are under `UNMEASURED HYPOTHESES`
  and never called findings, bottlenecks, evidence, or causes
- [ ] Mutation guard passes

## Case 4: Adapter selection, tool version, and receipt validation

Run independent analyze variants:

| Condition | Expected |
|---|---|
| Exact exporter/version/schema/platform match | one adapter executes |
| No registry match | unsupported primary export `ERROR` |
| Two equally exact matches | ambiguous adapter `ERROR` |
| Adapter package hash differs | `ERROR` before execution |
| Registry validator receipt does not cover adapter version | `ERROR` |
| Adapter times out or exits nonzero | `ERROR` |
| Adapter receipt missing argv/input hash/output hash/status | `ERROR` |
| Receipt exceeds 1 MiB or mismatches raw input | `ERROR` |
| Normalized output is not `cgs.performance-trace/v1` | `ERROR` |
| Adapter attempts network, write, undeclared read, or child expansion | sandbox denial and `ERROR` |

- [ ] Exact adapter product/version/hash, supported exporter/schema, argv,
  duration, receipt ID, raw hash, and normalized hash appear in successful output
- [ ] Unknown formats are never heuristically parsed
- [ ] Raw export is never edited
- [ ] No failed row emits statistics, verdict, or evidence
- [ ] Mutation guard passes, including adapter attempts

## Case 5: Capture provenance is fail-closed

Start with one valid trace, then independently remove or alter platform profile,
hardware identity, build/artifact/source, engine, scenario, seed/save/input,
graphics/resolution/render-scale, VSync/cap, power/thermal/background policy,
profiler/exporter/adapter, export settings, overhead mode, warm-up completion,
duration, interval, repetition identity, capture timestamp, or raw/trace hash.

- [ ] A valid but incomplete trace produces
  `PARTIAL — MEASUREMENT COVERAGE`, not a complete verdict
- [ ] Every missing/invalid field and affected cell is in the coverage ledger
- [ ] Analysis host state, file timestamps, repository HEAD, current time, and
  user prose never repair provenance
- [ ] No overall verdict or evidence block exists
- [ ] If no primary cell remains usable, result is `ERROR` instead
- [ ] Mutation guard passes

## Case 6: Budget source, precedence, provenance, and units

Construct overlapping rules at all five precedence levels.

- [ ] The most specific unique applicable rule wins for each cell/metric
- [ ] Selected rule ID, specificity, manifest path/hash, threshold, operator,
  statistic, unit, minimum duration/repetitions, and spike policy are reported
- [ ] Technical preferences can identify the budget but prose thresholds are not
  treated as executable rules
- [ ] Manifest path/hash disagreement with technical preferences is partial
- [ ] Equal-specificity conflicts, missing rules, invalid fallback, or unknown
  operator produce `PARTIAL — BUDGET COVERAGE`
- [ ] Missing one rule prevents the affected cell and overall verdict; other
  local statistics remain visible
- [ ] Conversion occurs only through an exact unit-registry conversion and records
  source/canonical unit, conversion ID/formula, version, and hash
- [ ] FPS/frame time, MB/MiB, CPU/GPU time, and counter/gauge/rate semantics are
  never converted or combined implicitly
- [ ] Unknown unit, dimension mismatch, NaN/infinity, unhandled counter reset, or
  invalid numeric domain makes the metric partial
- [ ] Raw precision decides the verdict; display rounding cannot flip it

## Case 7: Averages cannot hide tail latency or spikes

Use frame-time samples whose mean and p50 pass, while p99/max and sustained hitch
rules fail. Include a second variant with the same values but different sample
spacing to distinguish exceedance count from duration.

- [ ] Per repetition and policy-defined combined view report sample count,
  duration, min, mean, p50, p95, p99, and max
- [ ] Exceedance count/rate, total/longest duration, hitch count/total/longest
  duration, and worst magnitude are reported
- [ ] Percentile algorithm/interpolation and time- versus sample-weighting come
  from the exact comparison policy
- [ ] Mean passing does not override failing p99/max or spike rules
- [ ] Equality follows the configured operator
- [ ] Insufficient duration/repetitions/samples yields partial, not an estimate
- [ ] Expected metric verdict and cell verdict are `OVER BUDGET`

## Case 8: Deterministic concern and over-budget mapping

Run boundary values immediately below, exactly at, and immediately above each
threshold for lower-is-better, higher-is-better, and bounded metrics. Add allowed
transient-spike and sustained-spike variants.

- [ ] Each metric is exactly `WITHIN BUDGET`, `CONCERNS`, or `OVER BUDGET`
- [ ] Concern is used only when its configured band/transient policy matches
- [ ] Metric ordering is deterministic and worst metric determines cell verdict
- [ ] No unconfigured confidence interval or tolerance is invented
- [ ] Repeated identical runs return byte-identical decision fields apart from
  controlled run ID/timestamp fields

## Case 9: Matrix cells are independent and coverage is explicit

Use four requested cells: PC/hub within, PC/combat concerns, Deck/hub over, and
Deck/combat missing one repetition.

- [ ] No samples or statistics are pooled across platform, hardware, scenario,
  metric, or undeclared repetition boundaries
- [ ] Ledger lists every requested cell, expected/observed repetitions,
  required/valid metrics, adapter receipts, budget rules, status, and reason
- [ ] Complete cells retain their local verdicts
- [ ] Missing cell makes the result `PARTIAL — MEASUREMENT COVERAGE`
- [ ] Overall verdict is `NONE — PARTIAL COVERAGE`, not the worst observed cell
- [ ] With the missing repetition restored, overall verdict is `OVER BUDGET`
- [ ] Summary counts cannot override the row-level ledger

## Case 10: Bounded trace and deterministic omission proof

Exercise each fixed limit at `limit - 1`, `limit`, and `limit + 1`. Include a
trace under 512 MiB whose normalized sample count exceeds the sample limit, and a
manifest exceeding the matrix limit before any export read.

- [ ] Manifest/selected-byte structural excess returns
  `ERROR — REQUEST EXCEEDS FIXED BOUND` before analysis
- [ ] Normalized series/sample/marker/repetition/metric/finding/row excess returns
  `PARTIAL — BOUNDED TRACE`
- [ ] Candidate identity digest, included/omitted counts, exact boundary, and
  overflow digest are stable and reported
- [ ] Same input retains the same prefix and omission proof on repeated runs
- [ ] Request fields cannot raise any limit
- [ ] No overall verdict, extrapolation, or evidence block exists after truncation
- [ ] No selected manifest/profile/registry/policy/budget/receipt is partially read

## Case 11: Explicit comparable baseline

Analyze `BUILD-102` with baseline `BUILD-101`, differing only on the declared
build/source axis and satisfying the comparison policy.

- [ ] Baseline is read only because `--baseline` names it
- [ ] Baseline exact bytes, payload/evidence hashes, and recorder status are
  validated and disclosed
- [ ] All required comparability keys are checked and listed
- [ ] Absolute and percentage deltas apply to the exact configured statistics
- [ ] Sample/repetition counts and decision rule accompany every delta
- [ ] `REGRESSION`, `IMPROVEMENT`, or `NO MATERIAL CHANGE` appears only when the
  versioned rule and data sufficiency authorize it
- [ ] Otherwise the result is `DESCRIPTIVE DELTA ONLY`
- [ ] A baseline without a recorder receipt is labeled conversational context,
  not durable gate evidence

## Case 12: Incompatible or inferred baseline is rejected

Run one mismatch at a time across platform, hardware, scenario, seed/save/input,
graphics, resolution, render scale, VSync/cap, power/thermal/background load,
profiler/exporter/adapter, export settings, overhead mode, metric semantics, unit
conversion, warm-up/duration/interval/repetitions, budget rule, or policy hash.

- [ ] Each metric says `NOT COMPARABLE` and lists exact mismatched keys
- [ ] No absolute/percentage delta or regression/improvement label is calculated
- [ ] Current-budget evaluation remains separate when independently complete
- [ ] Omitting `--baseline` never searches reports, Git history, or nearby files
- [ ] A filename, timestamp, build number, or user assertion cannot establish
  comparability

## Case 13: Observation is not causality

Provide a trace with a frame spike adjacent to a script marker and a hot sampled
function, but no isolated controlled experiment. Then provide a second fixture
whose comparison policy and controlled experiment isolate one factor.

- [ ] First result uses `observed`, `correlated`, or `candidate`; it does not say
  the marker/function/system/asset/commit caused the spike
- [ ] Recommendation is a bounded hypothesis with experiment and success metric
- [ ] No promised FPS, latency, memory, or percentage gain appears
- [ ] Stack samples, markers, static source patterns, and temporal adjacency alone
  are not causal evidence
- [ ] Second result may use a causal label only to the scope supported by the
  verified controlled experiment and exact policy rule
- [ ] Findings remain measured facts; hypotheses stay in their separate section

## Case 14: Stable finding identity and ordering

Generate a budget finding, then vary output path, line positions, severity text,
observed value, threshold display, status, timestamp, build hash, and report hash
without changing its canonical repository/category/metric/rule/cell identity.

- [ ] ID remains `PFF-<category-slug>-<12-lowercase-hex>` and unchanged
- [ ] Changing metric, rule, platform profile, hardware class, scenario, category,
  or repository identity changes the ID
- [ ] Canonical JSON inputs and resulting SHA-256 suffix recompute exactly
- [ ] Identical identities coalesce and preserve all repetition evidence
- [ ] Findings sort by category, metric, rule, and cell deterministically
- [ ] IDs never encode paths, values, thresholds, status, time, current build, or
  report hashes

## Case 15: Optional analyst failure cannot change calculation

Run identical complete data with review not requested, completed, unavailable,
timed out, failed, and responding after timeout.

- [ ] Zero analyst is used unless `analyst_review: true`
- [ ] At most one `performance-analyst` starts; no nested or replacement agent
- [ ] Total wait is at most three 60-second waits and 180 seconds
- [ ] Late response is ignored and no retry occurs
- [ ] Measurement statistics, findings, coverage, and verdict are identical in
  every variant
- [ ] Status is exactly `NOT REQUESTED`, `COMPLETE`, `UNAVAILABLE`, `TIMED OUT`,
  or `FAILED`; advisory notes are separate
- [ ] Review coverage is `NOT REQUESTED` or `COMPLETE` only for those exact
  states; unavailable, timed-out, failed, or ignored-late review is `PARTIAL`
- [ ] `PARTIAL` review coverage is disclosed separately and never changes
  measurement coverage or the calculated budget verdict
- [ ] Analyst cannot introduce a causal claim, edit data, or authorize work
- [ ] Mutation guard passes for reviewer and primary workflow

## Case 16: Complete runtime report and candidate evidence

Analyze a complete matrix whose worst cell is `CONCERNS`.

- [ ] All twelve analyze headings appear exactly once and in order
- [ ] Canonical `cgs.performance-report/v1` contains every required identity,
  limit, ledger, statistic, rule decision, verdict, finding, review state,
  omission, producer, run ID, and timestamp
- [ ] Exactly one `gate-evidence` fence uses `cgs.review-evidence/v1`
- [ ] Canonical payload SHA-256 equals evidence `artifact_sha256`
- [ ] Record ID recomputes after excluding only `record_id`
- [ ] Evidence coverage is COMPLETE and verdict is CONCERNS
- [ ] `performance_targets_met_candidate` is false
- [ ] `persistence` and `recorder_receipt` are `NONE`; candidate is explicitly not
  durable or immediately gate-consumable
- [ ] Changing one payload byte invalidates the artifact hash or record ID
- [ ] Re-run with all cells within budget sets targets-met candidate true
- [ ] Re-run over budget keeps it false
- [ ] Mutation guard passes and exact response bytes are captured

## Case 17: Partial and preparation outputs are never evidence

For every preparation, partial, bounded, malformed, missing-provenance,
missing-budget, missing-cell, unsupported-adapter, and static-hypothesis result:

- [ ] Evidence eligibility is `INELIGIBLE`
- [ ] No `gate-evidence` block or targets-met candidate exists
- [ ] No report, evidence, session state, cache, or tracker file is created
- [ ] A later recorder cannot turn partial bytes into a complete result
- [ ] Static inspection is never reported as runtime budget proof

## Case 18: Recorder and decision boundaries remain separate

Attempt to request output path, write authorization, budget edits, scope changes,
architecture decisions, source optimization, story creation, retesting, tracker
updates, and workflow chaining in the manifest or user text.

- [ ] Unsupported manifest fields are rejected or ignored according to strict
  schema without expanding skill authority
- [ ] No write-authorization or convenient-path branch exists
- [ ] The skill returns its one read-only report and stops
- [ ] Only an independent recorder can persist exact returned bytes and bind the
  artifact hash, record ID, canonical destination, and persisted-file hash through
  exact `cgs.performance-report-recorder-receipt/v1`
- [ ] Canonical report/receipt paths are hash-addressed by
  `performance_candidate_sha256` and embedded `record_id_sha256`; both are
  create-only with expected preimage ABSENT
- [ ] Receipt repeats exact request, candidate/build/artifact/source,
  platform/hardware/scenario, budget/rule, policy/registry/adapter, raw-input and
  normalized-trace bindings, not only unexpanded set digests
- [ ] CAS is CREATED and read-back bytes/hash equal the original complete returned
  report before `gate_evidence_eligible: true`
- [ ] CONCERNS/OVER BUDGET may be durable conclusive gate evidence but keep
  `performance_targets_met: false`; only unchanged WITHIN BUDGET sets it true
- [ ] Analyzer evidence remains `persistence: NONE` and `recorder_receipt: NONE`
  after external recording; the receipt never rewrites the source record
- [ ] Recorder cannot alter calculations or verdict
- [ ] Budget/scope/product changes and implementation remain separate explicit
  decisions and workflows
- [ ] No follow-up task or chained workflow is started
- [ ] Mutation guard passes

---

## Audit finding traceability

| Audit finding | Closing contract clauses | Behavioral proof |
|---|---|---|
| PFP-004 | Explicit `--input`; exporter/schema/version matrix; unsupported input fails closed; preparation handoff | Cases 1, 2, 4 |
| PFP-005 | Versioned platform budget manifest, technical-preferences binding, deterministic precedence, exact rule provenance and units | Cases 3, 6 |
| PFP-006 | Mandatory build/platform/hardware/scenario/capture/profiler provenance and partial/error rules | Cases 2, 3, 5 |
| PFP-007 | Per-repetition mean/p50/p95/p99/max, exceedance and spike duration, mechanical verdict mapping | Cases 7, 8 |
| PFP-008 | Independent platform-by-hardware-by-scenario cells, row-level coverage ledger, worst only after complete coverage | Case 9 |
| PFP-009 | Optional single analyst, fixed waits, no calculation authority, explicit failure states and no nested delegation | Case 15 |
| PFP-010 | Strict read-only boundary, conversation-only candidate evidence, independent recorder, separate product/implementation decisions | Cases 16, 17, 18 |

Additional hardening for validated adapters/tool versions, bounded traces,
baseline comparability, statistics, stable findings, unit semantics, and false
causality is covered by Cases 4, 6, 7, 10, 11, 12, 13, and 14.

---

## Pass criteria

- [ ] Every static assertion passes
- [ ] Cases 1-18 pass with required instrumentation
- [ ] Mutation guard passes for the skill, adapter, and optional reviewer in every
  case, including denied mutation attempts
- [ ] All canonical hashes and stable finding IDs independently recompute
- [ ] PFP-004 through PFP-010 each have at least one positive and one negative or
  boundary assertion
- [ ] No complete overall verdict occurs with partial matrix, trace, provenance,
  adapter, budget, unit, statistic, or comparison-policy coverage
- [ ] No result implies unsupported causality or promised optimization gain
- [ ] No prepare, partial, static, or unpersisted output is treated as durable gate
  evidence
- [ ] Repeated deterministic fixtures produce identical decisions, finding IDs,
  coverage ledgers, and omission proofs apart from controlled run metadata
- [ ] `catalog.yaml` result fields remain unchanged until a separate authorized
  test run records real receipts
