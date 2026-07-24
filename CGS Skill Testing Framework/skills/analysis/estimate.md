# Skill Test Spec: $estimate

## Skill Summary

`$estimate` is a single-pass, strictly read-only evidence calculator. It supports
`story`, `sprint`, and `freeform` delivery profiles with explicit `relative` or
`calibrated` bases. Relative output is dimensionless S/M/L/XL evidence; numeric
effort requires comparable completed history, versioned sample-quality policy,
and exact effort units. Elapsed ranges require additional capacity, calendar,
dependency, parallelism, wait, and schedule-policy evidence.

Every locked result is bound to exact scope identity and provenance through a
`cgs.review-evidence/v1` envelope with `cgs.estimate-report/v1` extension under
contract `cgs.estimate/v2`. The analyzer never chooses scope, staffing, budget,
schedule, dates, or product tradeoffs.

---

## P1 Remediation Trace

| Audit item | Required behavior | Primary cases |
|---|---|---|
| EST-003 | Comparable history matches team/profile/work type/model/unit/conditions with include/exclude provenance | 5, 6 |
| EST-004 | No history/default conversion: relative evidence only, never `1 point = 1 day` | 3 |
| EST-005 | Confirmed and tentative affected scope remain distinct | 7 |
| EST-006 | Root-to-target instructions plus explicit first-level context are bounded and hash-bound | 1, 8 |
| EST-007 | Relative and calibration confidence use explicit readiness/sample-quality algorithms | 4, 5, 6 |
| EST-008 | Blocking product/ADR/dependency decisions are `NOT ESTIMABLE`; discovery needs its own scope | 9 |
| EST-009 | Exact profile/basis grammar distinguishes path/description/history/capacity and invalid input states | 1, 2, 17 |

---

## Static Assertions

- [ ] Frontmatter contains only `name` and non-empty `description`; name is
      `estimate`.
- [ ] Declares `cgs.estimate/v2`, `cgs.review-evidence/v1`, and
      `cgs.estimate-report/v1`.
- [ ] Invocation explicitly combines one `story|sprint|freeform` delivery profile
      with one `relative|calibrated` basis; neither is inferred.
- [ ] Calibrated basis requires exact history; relative basis rejects history and
      capacity and can never emit numeric time.
- [ ] Missing arguments, invalid/ambiguous paths, mixed profiles/bases, duplicate
      roots, URLs/globs/regex/latest, escapes, symlinks, junctions, and oversized
      descriptions have deterministic `INPUT REQUIRED` or `ERROR` behavior.
- [ ] Declares single-analyzer strict read-only behavior and forbids writes,
      re-baselining, scope/sprint changes, decisions, persistence, approval prompts,
      gates, delegation, and downstream workflow invocation.
- [ ] Every estimate unit binds `cgs.estimate-scope-binding/v1`, stable Scope ID,
      baseline/current/input hashes, taxonomy/profile identity, and completeness.
- [ ] Freeform normalization is exact and hashable; untestable delivery boundaries
      are `NOT ESTIMABLE`.
- [ ] Reads/hashes the applicable root-to-target `AGENTS.md` chain, root input,
      exact first-level links, and explicit manifests only.
- [ ] Defines fixed sprint-story, context-candidate, linked-artifact, single/total
      byte, history-sample, DAG-node/edge, schedule-scenario, assumption, unknown,
      and finding caps that inputs may only lower.
- [ ] Hashes the complete candidate identity sequence while retaining bounded
      rows and exact overflow counts/boundary keys/digests.
- [ ] Required root/binding overflow is `NOT ESTIMABLE`; optional evidence/history/
      schedule overflow is `PARTIAL ESTIMATE` with no numeric output.
- [ ] `cgs.estimate-evidence-manifest/v1` separates confirmed and tentative scope;
      predicted file/integration counts are never facts or direct effort inputs.
- [ ] `cgs.estimate-relative/v2` uses a deterministic five-axis evidence rubric,
      unknown level ranges, score interval, and dimensionless S/M/L/XL band range.
- [ ] Relative confidence follows exact readiness states and is explicitly not a
      probability, contingency, or time padding.
- [ ] Blocking product/ADR/platform/migration/dependency/acceptance decisions return
      `NOT ESTIMABLE`; discovery is not estimated without a separate Scope ID.
- [ ] Calibrated basis requires `cgs.estimate-history/v2`,
      `cgs.estimate-calibration-policy/v1`, and
      `cgs.estimate-unit-registry/v1` with exact provenance.
- [ ] Historical samples bind stable sample/scope/team/profile/work-type/model IDs,
      delivery conditions, factor vector, source bindings, completed effort unit/
      resolution, blocked effort, external wait, completion, and anomaly state.
- [ ] Every history sample gets one deterministic included/excluded reason; no
      cross-team velocity, title similarity, arbitrary recency, global average, or
      silent outlier deletion is used.
- [ ] Calibration policy, not skill prose, defines sample minimum, support,
      extrapolation, dispersion gates, quantiles, resampling, resolution,
      significant digits, and confidence.
- [ ] Failed calibration gates preserve relative evidence, suppress numeric effort,
      and return `PARTIAL ESTIMATE`; no default point/day conversion exists.
- [ ] Calibrated effort uses P50/P80/P90 ranges, exact model/intermediates/sample
      selection, source resolution, dispersion/support, and no false precision.
- [ ] Sprint relative bands and per-story quantiles are never summed; aggregation
      requires `cgs.estimate-aggregation-policy/v1` and compatible distributions.
- [ ] Effort, productive capacity, wait, parallelism, critical path, elapsed
      working time, and dates remain separate.
- [ ] Schedule output requires `cgs.estimate-capacity/v1`, complete acyclic DAG,
      and `cgs.estimate-schedule-policy/v1`; no headcount shortcut/start date/
      perfect parallelism/date commitment is invented.
- [ ] Stable `ESF-...` finding identity excludes mutable paths/hashes/titles/text/
      values/result/confidence/owner/status/run/timestamp/recommendation.
- [ ] Coverage is explicit per candidate/channel/check and missing required
      evidence never becomes `NOT_APPLICABLE`.
- [ ] Canonical results are exactly ERROR, INPUT REQUIRED, NOT ESTIMABLE, PARTIAL
      ESTIMATE, RELATIVE ESTIMATE, CALIBRATED EFFORT ESTIMATE, and CALIBRATED
      SCHEDULE RANGE with deterministic precedence.
- [ ] `estimate_id`, context/inventory/payload/envelope hashes are recomputable;
      run identity/timestamp remain outside deterministic extension bytes.
- [ ] Scope-check eligibility distinguishes relative-only, verified effort,
      verified schedule, and unverified analysis.
- [ ] Returns at most one owner-routed decision boundary and never ranks or executes
      scope, staffing, budget, schedule, date, or product decisions.
- [ ] Metadata names the three profiles, two bases, bounded/hash-bound ranges,
      read-only behavior, and decision boundary.

---

## Director and Delegation Checks

None. Estimate uses one analyzer. A director, producer, planner, specialist, agent,
or workflow cannot convert evidence into scope, staffing, budget, schedule, or
date authority and is never invoked by this analyzer.

---

## Required Fixture Contract

Fixtures provide exact raw bytes and SHA-256 values for instructions, root inputs,
scope bindings, first-level links, evidence/history manifests, calibration/unit/
aggregation/schedule policies, sample completion evidence, capacity/calendar,
dependency DAG, and expected canonical evidence. Tests snapshot all project paths
before and after and inject stale/overflow states deterministically.

---

## Test Cases

### Case 1: Exact profile/basis invocation and path confinement

Valid inputs cover:

```text
$estimate story --basis relative --input stories/s1.md
$estimate story --basis calibrated --input stories/s1.md --history estimates/h1.yaml
$estimate sprint --basis relative --input sprints/sp1.md --evidence estimates/e1.yaml
$estimate sprint --basis calibrated --input sprints/sp1.md --history estimates/h1.yaml --capacity estimates/c1.yaml
```

Invalid variants omit profile/basis/input/history, mix profiles or bases, repeat
roots, pass capacity under relative basis, use an unflagged path, directory, URL,
glob, regex, `latest`, external/absolute/traversal path, symlink, junction, or
unknown flag.

Expected behavior:

1. Missing required values return `INPUT REQUIRED`; invalid/conflicting/unsafe
   values return `ERROR`.
2. Neither result emits estimate evidence or scans for alternatives.
3. Valid paths are exact project-local regular files and stable IDs are matched
   exactly.

Assertions:

- [ ] Delivery profile and estimate basis are independent explicit dimensions.
- [ ] Relative basis cannot accidentally consume calibration/capacity data.
- [ ] No title, mtime, Git, or conversation inference occurs.

---

### Case 2: Freeform identity is explicit and reproducible

Fixture variants:

- A supplies description, stable Scope ID, baseline hash, and current hash.
- B omits one binding argument.
- C has a description without a testable delivery boundary.
- D supplies equivalent CRLF/decomposed-Unicode input that normalizes to the same
  NFC/LF/trimmed/final-LF bytes as A.

Expected behavior:

1. A/D use the same normalized input SHA-256 and scope binding.
2. B is `INPUT REQUIRED` with no estimate.
3. C is `NOT ESTIMABLE`, emits only non-consumable bound analysis evidence, and
   names the boundary owner.
4. No feature title, story, or baseline is discovered by search.

Assertions:

- [ ] Freeform description size cap is enforced before estimation.
- [ ] Normalized bytes are included in estimate identity.
- [ ] Missing scope identity is never repaired.

---

### Case 3: Relative story without history has no numeric time

Fixture:

- Story has complete scope binding, acceptance, accepted ADR/interface evidence,
  known dependencies, and identified validation.
- No history or capacity is supplied; basis is relative.

Expected behavior:

1. Five-axis factor vector, score, one dimensionless band, and HIGH relative
   confidence are supported by exact evidence.
2. Result is `RELATIVE ESTIMATE` and scope-check eligibility is `RELATIVE_ONLY`.
3. No hours, person-days, workdays, calendar dates, velocity, budget, or
   `1 point = 1 day` conversion appears.

Assertions:

- [ ] Missing history is normal for relative basis, not an implicit fallback.
- [ ] Relative size is neither effort nor elapsed time.
- [ ] No recommended budget is emitted.

---

### Case 4: Unknown axes widen ranges and confidence deterministically

Fixture variants:

- One axis has insufficient integration evidence but no blocking owner decision.
- All axes are known but architecture is PARTIAL and score crosses M/L.
- All readiness fields are READY and one band resolves.

Expected behavior:

1. Unknown axis produces min/max axis values, score interval, and band range; it
   is not guessed.
2. Confidence is respectively LOW, MEDIUM, and HIGH under the stated algorithm.
3. Confidence is not phrased as probability or converted into contingency time.

Assertions:

- [ ] Every axis cites evidence and limitation.
- [ ] History/capacity never alters the factor vector.
- [ ] Band boundaries and score arithmetic are reproducible.

---

### Case 5: Comparable completed samples calibrate effort

Fixture:

- Versioned policy requires at least five samples and defines support, dispersion,
  quantile, rounding, resolution, and confidence gates.
- Six completed samples match team, story profile, taxonomy/type, model, effort
  unit, delivery conditions, bindings, and factor support.
- Completion/sample hashes match and quality gates pass.

Expected behavior:

1. Every sample is `INCLUDED` with exact provenance.
2. Policy-selected deterministic P50/P80/P90 effort ranges and intermediates are
   shown in one effort unit.
3. Result is `CALIBRATED EFFORT ESTIMATE` when no capacity is supplied.
4. Output precision does not exceed sample/unit/model resolution.

Assertions:

- [ ] Sample threshold comes from policy, not hardcoded skill behavior.
- [ ] Quantiles are ranges/evidence, not promises or recommended budget.
- [ ] Sample count, support, dispersion, and calibration confidence are separate.

---

### Case 6: Incompatible or poor-quality history fails calibration

Fixture includes cross-team, sprint-profile, taxonomy mismatch, old model, mixed
unit, incompatible conditions, incomplete/censored work, unresolved anomaly, and
out-of-support samples. Remaining included samples fail policy minimum or
dispersion gate.

Expected behavior:

1. Every sample receives exactly one included/excluded state and evidence reason.
2. Excluded samples do not affect any statistic.
3. Calibrated basis returns `PARTIAL ESTIMATE`, calibration `UNAVAILABLE`, and
   preserves relative evidence without numeric effort.
4. No cross-team velocity/global average/title similarity/recent sprint/default
   conversion substitutes for missing quality.

Assertions:

- [ ] Outliers are not silently deleted.
- [ ] Extrapolation beyond factor support is rejected by policy.
- [ ] Unit and actual-effort resolution remain explicit.

---

### Case 7: Confirmed and tentative affected files remain distinct

Fixture:

- Bound evidence confirms two modules/interfaces.
- Five predicted files and two inferred integrations are tentative.

Expected behavior:

1. Confirmed and tentative scope are separate exact-hash lists.
2. Tentative counts do not directly affect relative score or effort.
3. A model axis may widen only through its explicit unresolved breadth/integration
   rule, with evidence and limitation.

Assertions:

- [ ] Predicted paths are never reported as affected facts.
- [ ] File/code count is not a calibration input by itself.
- [ ] Estimate output exposes scope uncertainty instead of false certainty.

---

### Case 8: Bounded root context and overflow behavior

Fixture variants exceed sprint-story, linked-artifact, context-candidate,
single/total-byte, history-sample, DAG-node/edge, or finding caps.

Expected behavior:

1. Complete candidate identity digest plus bounded rows, exact overflow count,
   boundary keys, and omitted digest are reported when enumeration is safe.
2. Required root/binding/story overflow is `NOT ESTIMABLE`.
3. Optional evidence/history/capacity overflow is `PARTIAL ESTIMATE`, suppresses
   numeric effort/elapsed output, and preserves bounded relative evidence.
4. No truncated subset is treated as complete or calibrated.

Assertions:

- [ ] Inputs cannot raise fixed caps.
- [ ] All affected coverage channels are named.
- [ ] Repository-wide GDD/code/TODO/history scans never occur.

---

### Case 9: Product, ADR, or dependency decision blocks delivery

Fixture:

- Story has unresolved player behavior, missing required accepted ADR, and unknown
  dependency interface/owner.

Expected behavior:

1. Readiness states are BLOCKED with stable decision/owner/evidence/acceptance IDs.
2. Result is `NOT ESTIMABLE`, not a guessed L/XL, padded range, or calendar date.
3. A smallest discovery question may be described but is not estimated without a
   separate Scope ID and invocation.
4. No product or architecture choice is made and no workflow starts.

Assertions:

- [ ] Blocking decision differs from ordinary uncertainty.
- [ ] Owner decision is not delegated by the analyzer.
- [ ] Bound non-consumable evidence preserves why estimation stopped.

---

### Case 10: Effort calibration never implies elapsed duration

Fixture:

- Valid calibrated effort exists.
- Capacity, calendar, DAG, wait, or schedule policy is absent because no capacity
  flag was supplied.

Expected behavior:

1. Result remains `CALIBRATED EFFORT ESTIMATE`.
2. Capacity/schedule channels are `NOT_APPLICABLE` and elapsed is null.
3. Analyzer does not divide by headcount, assume a workday/start date/perfect
   parallelism, or convert effort to dates.

Assertions:

- [ ] Effort, wait, capacity, elapsed time, and date are distinct fields/units.
- [ ] Missing optional capacity does not invalidate calibrated effort.
- [ ] No schedule commitment is implied.

---

### Case 11: Complete capacity and DAG produce a schedule range

Fixture:

- Calibrated P50/P80/P90 effort ranges exist.
- Current `cgs.estimate-capacity/v1` binds matching team/unit, availability,
  working calendar/time zone, WIP/parallel lanes, reviewers/services, validity,
  and owner.
- Complete acyclic dependency DAG and `cgs.estimate-schedule-policy/v1` bind wait,
  correlation, critical-path, and scenario assumptions.

Expected behavior:

1. Result is `CALIBRATED SCHEDULE RANGE` and eligibility `VERIFIED_SCHEDULE`.
2. Effort, productive capacity, waits, parallel branches, WIP, critical path,
   elapsed working-time range, and dates remain separate with formulas.
3. No range is called a commitment, budget, staffing recommendation, or promised
   date.

Assertions:

- [ ] DAG cycles are invalid and prevent schedule output.
- [ ] A supplied stale/mismatched capacity channel returns PARTIAL ESTIMATE while
      preserving effort evidence.
- [ ] Capacity conflict is routed to user/producer, not resolved here.

---

### Case 12: Sprint aggregation requires compatible distributions

Fixture variants:

- A: every story has compatible same-unit/model calibrated distributions and a
  valid `cgs.estimate-aggregation-policy/v1` with dependency/correlation,
  deterministic scenarios/seeds, and applicability.
- B: one story lacks calibration or uses another unit/model.

Expected behavior:

1. Every story keeps its own binding/factor/band/distribution.
2. A aggregates through the named policy, not by summing quantile columns.
3. B returns `PARTIAL ESTIMATE`, sprint effort `UNVERIFIED`, and names the blocking
   story while preserving per-story relative evidence.
4. Neither variant decides sprint inclusion or fit.

Assertions:

- [ ] Relative bands are never added.
- [ ] Per-story P50/P80/P90 columns are not relabeled sprint quantiles.
- [ ] Sprint story count cap is enforced before aggregation.

---

### Case 13: False precision and alternative calibration models fail closed

Fixture variants:

- Historical effort resolution is one half-day equivalent in a stable effort
  unit, while raw model math yields many decimals.
- Two valid calibration policies/models exist with no authoritative selection.
- A seeded resampling policy omits its seed/version.

Expected behavior:

1. Displayed ranges obey source/model significant-digit and rounding policy and
   show unrounded intermediates separately.
2. Ambiguous model/policy or missing resampling provenance makes calibration
   unavailable and result PARTIAL ESTIMATE.
3. Analyzer does not choose the narrower/more favorable range or print a point
   “expected” estimate.

Assertions:

- [ ] P50/P80/P90 are labeled distributions/ranges, not confidence promises.
- [ ] No generic optimistic/expected/pessimistic days appear.
- [ ] Numeric unit and measurement precision are explicit.

---

### Case 14: Stable findings and estimate identity have separate semantics

Fixture:

- Run A has one stable calibration gap for the same profile/basis/Scope IDs/policy.
- Run B moves/rewrites sources and changes hashes/current values/owner/result label
  without changing that logical gap.
- Run C changes Scope ID or calibration policy ID.

Expected behavior:

1. A/B preserve one `ESF-...` finding ID while estimate/context/payload/record
   hashes change.
2. C produces a different finding fingerprint.
3. Any changed scope/baseline/current/input/model/sample/evidence/capacity hash
   creates a different `estimate_id` and invalidates receipt reuse.

Assertions:

- [ ] Finding identity excludes mutable presentation/evidence values.
- [ ] Estimate identity intentionally includes immutable scope and consumed sample/
      policy/evidence hashes.
- [ ] Scope-check eligibility cannot reuse a mismatched estimate identity.

---

### Case 15: Final re-hash detects mutation

Fixture:

- Root story, scope binding, history, sample completion, evidence, capacity, or DAG
  bytes change after lock and before output.

Expected behavior:

1. Re-enumeration/re-hashing detects added/removed/renamed/changed input.
2. Derived estimates are discarded.
3. Result is `NOT ESTIMABLE — INPUT CHANGED DURING ESTIMATE`, with only
   non-consumable hash-bound diagnostics.
4. No mixed snapshot or automatic restart occurs.

Assertions:

- [ ] Mtime/Git labels do not substitute for raw hashes.
- [ ] Changed input cannot produce a scope-check-eligible record.
- [ ] Project remains byte-identical except the externally injected fixture change.

---

### Case 16: Strict read-only owner boundary

Fixture:

- Calibrated evidence conflicts with recorded sprint capacity.
- User asks to cut stories, assign staff, save the estimate, update sprint, and
  invoke planning/architecture workflows.

Expected behavior:

1. Analyzer reports affected Scope IDs, conflict evidence, and one producer/user
   decision boundary.
2. It does not rank Cut/Keep/Defer, recommend budget, select staffing/scope/date,
   edit/save/re-baseline, request write approval, delegate, or invoke anything.
3. It stops after one packet.

Assertions:

- [ ] Estimate evidence is not authority.
- [ ] No file, sprint, scope, calendar, decision, workflow, session, or Git state
      changes.
- [ ] No automatic follow-up run begins.

---

### Case 17: Canonical result precedence is total

Evaluate independent states:

| State | Result |
|---|---|
| missing required invocation argument | `INPUT REQUIRED` |
| invalid/unsafe/ambiguous root or no scope identity | `ERROR` |
| bound scope with blocking decision/invalid completeness/root overflow/stale input | `NOT ESTIMABLE` |
| useful relative evidence but requested/required optional channel incomplete | `PARTIAL ESTIMATE` |
| complete relative basis | `RELATIVE ESTIMATE` |
| complete calibration without supplied schedule channel | `CALIBRATED EFFORT ESTIMATE` |
| complete calibration plus supplied schedule channel | `CALIBRATED SCHEDULE RANGE` |

Assertions:

- [ ] First matching rule wins mechanically.
- [ ] Earlier incomplete results preserve known relative/effort/gap evidence but
      cannot claim downstream eligibility.
- [ ] No COMPLETE status, recommended budget, sprint-fit claim, or deadline promise
      appears.

---

### Case 18: Hash-bound output and catalog hygiene

Fixture:

- Identical immutable profile/basis, root/scope bytes, model/policies, included/
  excluded sample set, evidence, capacity/DAG, and assumptions are processed twice.

Expected behavior:

1. Extension conforms to `cgs.estimate-report/v1`; envelope conforms to
   `cgs.review-evidence/v1`.
2. Context inventory/manifest, estimate identity, payload, artifact, and record
   hashes recompute.
3. Identical inputs produce identical extension bytes and estimate ID; outer run
   ID/timestamp may differ without entering deterministic payload.
4. Catalog test-result fields remain blank until authorized behavioral execution.

Assertions:

- [ ] Only complete results can be scope-check eligible; relative eligibility does
      not verify numeric effort.
- [ ] Inconsistent evidence construction returns ERROR without a record.
- [ ] Structural edits alone are not recorded as a test pass.

---

## Protocol Compliance

- [ ] Profile, basis, scope identity, baseline/current/input hashes, project
      identity, context, and every consumed policy/sample are exact and hash-bound.
- [ ] Relative output is deterministic, dimensionless, evidence-scoped, and
      available without false time conversion.
- [ ] Historical sample inclusion/exclusion, units, quality, support, variance,
      uncertainty, and quantiles are versioned and reproducible.
- [ ] No numeric effort is emitted without complete comparable-history calibration.
- [ ] No elapsed/date range is emitted without complete capacity/calendar/DAG/
      wait/parallelism schedule evidence.
- [ ] Confirmed versus tentative scope, effort versus elapsed, and estimator versus
      owner decisions remain separate.
- [ ] Bounded context/overflow and stale input fail closed without sampled claims.
- [ ] Stable findings and estimate identity use their distinct documented inputs.
- [ ] Analyzer is project-read-only, single-pass, conversation-only, and invokes
      no gate, agent, recorder, owner, or downstream workflow.
- [ ] Output conforms to `cgs.review-evidence/v1` plus
      `cgs.estimate-report/v1` under `cgs.estimate/v2`.

---

## Coverage Notes

Tests must evaluate algorithm/provenance properties rather than hardcode that a
subjective fixture “should be M” or “should take N days.” Calibration fixture
thresholds belong to the explicit policy bytes. Schedule fixtures must distinguish
person effort, external wait, capacity, critical path, elapsed work time, and
calendar dates.

Report persistence belongs to a separate recorder contract. The catalog entry
points to this file, and its `last_*` fields remain blank until an authorized test
workflow actually executes every case. Editing this contract/spec or running
structural probes alone is not a test pass and must not create a catalog result.
