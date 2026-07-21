# Skill Test Spec: $perf-profile

## Skill Summary

`$perf-profile` has two explicit modes. `prepare-capture` returns a reproducible
target-hardware checklist and `MEASUREMENT REQUIRED` without a budget verdict.
`analyze-export` validates a versioned runtime export and provenance, computes
percentiles/spikes per platform × hardware × scenario cell, applies an exact budget
manifest, optionally calculates only comparable deltas, and emits hash-bound runtime
evidence. Static candidates never satisfy a performance gate.

---

## Static Assertions (Structural)

- [ ] Frontmatter contains only matching `name` and non-empty `description`
- [ ] Invocation exposes distinct `prepare-capture` and `analyze-export` modes with
  required manifest; analysis also requires explicit `--input`
- [ ] No valid runtime input produces `MEASUREMENT REQUIRED` and no budget verdict
- [ ] Export schema requires build/source, engine receipt, platform/hardware,
  scenario, duration/warmup/repetitions, profiler settings, metric units and samples
- [ ] Malformed, unsupported, empty, non-finite, unit-mixed, or hash-mismatched input
  returns ERROR with null verdict
- [ ] Budgets come from one exact versioned platform/hardware/scenario manifest with
  deterministic precedence; no hardcoded defaults
- [ ] Runtime computation includes mean, p50, p95, p99, max, exceedance rate/duration,
  and spike/hitch frame IDs
- [ ] Every required matrix cell has an independent verdict; overall is worst valid
  cell only when coverage is complete
- [ ] Verdicts are exactly `WITHIN BUDGET`, `CONCERNS`, or `OVER BUDGET`, and only
  valid complete runtime analysis emits one
- [ ] Delta requires exact explicit baseline and matching comparability keys
- [ ] Static candidates carry no severity/headroom/gain and are never gate evidence
- [ ] Only an exactly authorized report path may be written; code/settings/budgets/
  plans/scope/ADRs remain non-writes
- [ ] Optional analyst is read-only, bounded, cannot change verdict, and timeout marks
  review partial without discarding deterministic calculation
- [ ] Gate eligibility and targets-met are distinct, hash-bound fields

---

## Case 1: Prepare capture with no runtime data

**Fixture:** Valid capture manifest names build, target hardware, scenario matrix,
budget, repetitions, duration, metrics, and supported exporter, but no export exists.

**Input:**

`$perf-profile prepare-capture --manifest production/qa/perf/capture-request.json`

**Expected behavior:** Return a hardware/scenario-specific checklist covering build
identity, environment, warmup, duration, repetitions, exporter settings, raw export
hash, dropped-frame/hitch observations, and required metrics.

**Assertions:**

- [ ] Analysis Status is MEASUREMENT REQUIRED
- [ ] Budget Verdict is null/absent
- [ ] No current/headroom/expected-gain estimate appears
- [ ] Nothing is written unless an exact capture-plan output was separately authorized
- [ ] Gate evidence is false

---

## Case 2: Malformed, empty, or unsupported export

**Fixture:** Parameterized inputs cover invalid JSON, unsupported exporter version,
empty frame series, NaN/Infinity, mixed units, duplicate frames, non-monotonic time,
and raw hash mismatch.

**Expected behavior:** Reject before calculations with `Analysis Status: ERROR`,
`Budget Verdict: null`, observed schema/path/hash details, and no report write.

**Assertions:**

- [ ] No invalid sample is silently dropped or interpolated
- [ ] No optimization, delta, gate evidence, or budget verdict is produced
- [ ] Exact validation failure is named

---

## Case 3: Average passes but p99 spikes cause CONCERNS

**Fixture:** Valid runtime export's mean frame time passes. Frames 417, 902, and 1231
violate a required p99/max/hitch rule whose failure severity is CONCERN. Draw calls
pass their rule.

**Expected behavior:** Compute unrounded p50/p95/p99/max, threshold counts/rates and
spike frame IDs. The cell and overall verdict are CONCERNS.

**Assertions:**

- [ ] Passing average cannot override the failed tail/spike rule
- [ ] Frames 417, 902, and 1231 appear with values/durations/markers
- [ ] Draw-call observed statistic and budget rule are explicitly compared
- [ ] Stable finding ID binds input, budget, build, hardware, scenario, and window

---

## Case 4: Sustained failure is OVER BUDGET

**Fixture:** Complete capture has a sustained frame-time violation rate above an
`OVER` rule; all provenance and coverage are valid.

**Expected behavior:** Cell and overall verdict are OVER BUDGET. Findings show
unrounded observed values, expected rule, duration and evidence hashes.

**Assertions:**

- [ ] Threshold is read from the exact budget manifest, not hardcoded
- [ ] Systemic failure uses the rule's OVER severity deterministically
- [ ] Recommendations are measurement experiments, not automatic implementation
- [ ] Numerical expected gain is absent unless backed by comparable measured data

---

## Case 5: Complete matrix is WITHIN BUDGET

**Fixture:** Every required platform × hardware × scenario cell and repetition is
present; every required metric/rule passes.

**Expected behavior:** Each cell and overall verdict are WITHIN BUDGET. If persisted
under exact authorization and hashes remain current, gate evidence and
performance_targets_met are true.

**Assertions:**

- [ ] Required/evaluated/passed cell, metric, and rule counts are complete
- [ ] Gate eligibility requires persisted read-back report and current hashes
- [ ] Conversation-only output cannot claim gate evidence

---

## Case 6: Multi-platform or scenario coverage gap

**Fixture:** PC/scenario-A passes and console/scenario-A passes, but required
console/scenario-B is absent.

**Expected behavior:** Preserve local valid cell verdicts but set overall analysis
PARTIAL — MEASUREMENT REQUIRED, overall Budget Verdict null, gate evidence false, and
one next action to capture console/scenario-B.

**Assertions:**

- [ ] Results are never averaged across cells
- [ ] Worst-cell aggregation occurs only after full coverage
- [ ] Missing cell cannot be waived into targets met

---

## Case 7: Comparable baseline delta

**Fixture:** Explicit baseline and current input match schema/adapter, metric units,
platform/hardware, scenario/version/hash, graphics/config/resolution, profiler,
warmup/sampling, and budget version; build hashes differ intentionally.

**Expected behavior:** Show baseline/current build and data hashes plus absolute and
percentage deltas for mean, p50, p95, p99, max, exceedance rate and hitches.

**Assertions:**

- [ ] Baseline is not discovered by scanning a directory
- [ ] Delta uses identical dimensions and metric windows
- [ ] Improvement/regression language requires declared confidence/repetition rule;
  otherwise change is descriptive

---

## Case 8: Incompatible baseline forbids delta

**Fixture:** Baseline differs by scenario version, hardware class, resolution, or
profiler settings.

**Expected behavior:** Output `Delta Status: NOT COMPARABLE`, enumerate exact differing
keys, and compute no delta, trend, improvement, or regression.

**Assertions:**

- [ ] Cross-scene/platform/hardware/settings comparison is rejected
- [ ] Current standalone verdict may remain valid if its own evidence is complete

---

## Case 9: Static candidates can never satisfy a gate

**Fixture:** Prepare mode lists bounded source candidates but no runtime export.

**Expected behavior:** Label every item `STATIC CANDIDATES — UNMEASURED`, assign no
performance severity/impact/headroom/gain, return null budget verdict, and set
`evidence_kind: STATIC_OR_CAPTURE_PLAN`, gate false, targets met false.

**Assertions:**

- [ ] Static source analysis is not described as profiling current performance
- [ ] Gate consumer has explicit machine-readable rejection fields
- [ ] Existing source files or clean static scan cannot imply performance met

---

## Case 10: Optional analyst timeout preserves calculation, not review claim

**Fixture:** Runtime computation deterministically yields CONCERNS; the optional
performance-analyst times out and later returns a result.

**Expected behavior:** Revoke token, ignore late result, permit at most one retry,
retain CONCERNS, and report analyst_review PARTIAL/NOT REVIEWED.

**Assertions:**

- [ ] Reviewer is read-only, bounded to 15 minutes, and cannot delegate
- [ ] Reviewer cannot modify the mathematical verdict
- [ ] Review failure does not discard valid runtime calculations
- [ ] Independent review completion is not claimed

---

## Case 11: Report-write authorization and mutation guard

**Fixture:** Valid analysis requests one report path. A recommendation suggests code,
budget, and engine-setting changes.

**Expected behavior:** Preview one exact report operation/base/candidate hash and
obtain authorization. Write/read back only that report. Return owner-domain experiment
handoffs; do not implement or mutate other artifacts.

**Assertions:**

- [ ] No report write occurs without exact output authorization
- [ ] Scope expansion requires new authorization
- [ ] Code, assets, engine settings, budgets, plans, scope, ADRs, and findings are not
  edited
- [ ] Final report hash is recorded

---

## Case 12: Budget precedence and provenance gaps

**Fixture:** One capture has two equal-precedence budget rules; another lacks hardware
power state and scenario source hash.

**Expected behavior:** Conflict produces null verdict for the affected cell. Missing
critical provenance produces PARTIAL — MEASUREMENT REQUIRED. Neither becomes gate
eligible or targets met.

**Assertions:**

- [ ] Exact platform/hardware/scenario rule precedence is deterministic
- [ ] Generic prose or engine defaults do not fill missing budgets
- [ ] Missing provenance is not inferred from filenames or neighboring reports
- [ ] Output identifies exact owner/input required to resolve the gap

---

## Protocol Compliance

- [ ] Capture planning and runtime analysis never share verdict semantics
- [ ] Runtime evidence is bound to input/build/platform/hardware/scenario/budget hashes
- [ ] Percentiles and spikes participate in deterministic per-cell verdicts
- [ ] Full coverage is required for overall verdict and gate eligibility
- [ ] Static output is machine-readably gate-ineligible
- [ ] Report persistence is the only optional mutation and requires exact authority
- [ ] Recommendations remain measured hypotheses for separate owners
- [ ] Terminal output contains provenance, coverage, rule evaluations, findings,
  hashes, persistence/gate fields, and exactly one next action

---

## Coverage Notes

Cases 1–6 and 9 directly regress PFP-001 through PFP-003: no-measurement claims,
runtime-export/verdict contract drift, and static evidence entering performance gates.
Cases 7–8 and 10–12 cover comparable deltas, reviewer failure, report authorization,
budget precedence, malformed inputs, and incomplete provenance so the P0 gates cannot
be bypassed indirectly.
