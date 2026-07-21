# Skill Test Spec: $estimate

## Skill Summary

`$estimate` is a read-only evidence calculator with explicit `story`, `sprint`, and
`freeform` profiles. It always binds valid estimates to stable Scope IDs plus immutable
baseline/current/input hashes. Without a comparable same-team history model it emits
only a dimensionless S/M/L/XL relative band or band range and uncertainty. Numeric
P50/P80/P90 effort requires calibrated history; elapsed workday/date ranges also
require compatible capacity, calendar, dependency-DAG, parallelism, and wait evidence.

It never recommends a budget, promises a date, selects sprint scope, decides
Cut/Keep/Defer, or invokes another workflow. Canonical results are `ERROR`,
`INPUT REQUIRED`, `NOT ESTIMABLE`, `PARTIAL ESTIMATE`, `RELATIVE ESTIMATE`,
`CALIBRATED EFFORT ESTIMATE`, and `CALIBRATED SCHEDULE RANGE`.

## Static assertions

- [ ] YAML frontmatter contains only required `name` and non-empty `description`
- [ ] Metadata names the three profiles, read-only scope, and decision boundary
- [ ] Explicit profile parsing prevents path/description ambiguity
- [ ] Every consumable estimate receipt binds Scope ID, baseline SHA-256, current
      scope SHA-256, input SHA-256, model ID, and all consumed evidence
- [ ] S/M/L/XL are dimensionless relative bands with a deterministic five-axis rubric
- [ ] No uncalibrated hours/days/date or default point-to-day conversion
- [ ] Comparable samples have deterministic inclusion/exclusion rules and provenance
- [ ] Numeric calibration requires a fully resolved current factor score
- [ ] Numeric effort and elapsed duration have separate gates and fields
- [ ] Missing product/ADR/dependency decisions can return `NOT ESTIMABLE`
- [ ] Estimate output does not decide product scope, budget, staffing, or schedule
- [ ] No writes, Git mutation, gate, delegation, or follow-up execution
- [ ] Result vocabulary exactly matches this specification

## Director gate checks

None. An agent, model, or gate cannot turn estimate evidence into scope or schedule
authority.

## Test cases

### Case 1: Story profile with no history returns relative evidence only

**Fixture**

- Story has one stable Scope ID, exact baseline/current hashes, complete acceptance
  boundary, accepted ADR references, ready dependencies, and identified tests.
- No history manifest is supplied.

**Input**

`$estimate story --input <story-path>`

**Expected**

- The five-axis factor vector and evidence are shown.
- A dimensionless single S/M/L/XL band and readiness-derived confidence are emitted.
- Result is `RELATIVE ESTIMATE`.
- Calibration is `NOT_REQUESTED`; no hours, days, dates, velocity conversion, or
  recommended budget appears.
- Receipt binds Scope ID and baseline/current/input hashes.

### Case 2: Freeform profile requires complete explicit scope binding

**Variants**

- A: description plus Scope ID, baseline hash, and current hash are supplied.
- B: one or more binding arguments are absent.
- C: the description has no testable delivery boundary.

**Expected**

- A hashes normalized description bytes and produces a bound relative estimate.
- B returns `INPUT REQUIRED` without estimating.
- C returns `NOT ESTIMABLE` and no consumable receipt.
- No feature title or baseline is discovered by fuzzy search.

### Case 3: Sprint profile estimates stories independently

**Fixture**

- Sprint manifest lists four exact story paths/hashes, Scope IDs, baseline/current
  hashes, inclusion state, and dependency edges.
- No calibrated history exists.

**Expected**

- Each story gets its own factor vector and relative band/range.
- Relative bands are not arithmetically summed into a sprint total.
- `Sprint Effort: UNVERIFIED` identifies the missing calibration.
- No sprint-fit or completion promise is made.

### Case 4: Invalid and ambiguous inputs are deterministic

**Variants**

- no profile; unflagged path; mixed story/freeform flags; two inputs; bad path;
  traversal path; unknown flag; sprint beyond the story budget.

**Expected**

- Missing required arguments return `INPUT REQUIRED`.
- Invalid, ambiguous, unsafe, or unreadable inputs return `ERROR`.
- Required root/binding budget overflow returns `NOT ESTIMABLE`.
- No estimate or repository scan occurs.

### Case 5: Missing history never creates a day conversion

**Fixture**

- Story is fully estimable but no historical sample exists.

**Expected**

- Relative size remains available.
- Calibration is `UNAVAILABLE` or `NOT_REQUESTED` as applicable.
- The output never substitutes `1 point = 1 day`, a generic velocity, or conservative
  numeric defaults.

### Case 6: Cross-team and incompatible samples are excluded

**Fixture**

- History contains samples from another team, another profile, another work taxonomy,
  an older model version, incomplete work, and three valid same-team samples.

**Expected**

- Every sample is listed with deterministic inclusion/exclusion reason.
- Only three samples remain, below the five-sample calibration minimum.
- Result remains `RELATIVE ESTIMATE`; numeric calibration is unavailable.
- No excluded sample affects quantiles.

### Case 7: Five low-variance comparable samples calibrate effort

**Fixture**

- Five or more completed same-team/story/work-type/model samples use one effort unit,
  cover the current factor score, and have coefficient of variation at most 0.50.
- Sample completion receipts and hashes match.

**Expected**

- Normalized effort ratios and empirical nearest-rank P50/P80/P90 selections are shown.
- Result is `CALIBRATED EFFORT ESTIMATE`.
- Effort values remain in the historical effort unit; no elapsed days/date is emitted
  without capacity evidence.
- Included sample IDs/hashes make the calculation reproducible.

### Case 8: High variance or extrapolation rejects calibration

**Variants**

- comparable-sample coefficient of variation exceeds 0.50;
- current score is outside historical coverage;
- mixed effort units or unresolved anomaly exists.

**Expected**

- Calibration is `UNAVAILABLE` with exact failing gate.
- Relative factor/band evidence is preserved.
- No P50/P80/P90 numeric effort is fabricated.

### Case 9: Architecture or product decision blocks delivery estimate

**Fixture**

- Matchmaking story includes blocking TBD product behavior and requires an ADR that
  is missing or Proposed.

**Expected**

- Requirements/architecture readiness names the exact blockers.
- Result is `NOT ESTIMABLE`, not an arbitrary L/XL delivery estimate.
- A discovery question may be identified but is not estimated without its own Scope
  ID and separate explicit invocation.
- No architecture workflow is started.

### Case 10: Tentative affected files are not counted as facts

**Fixture**

- Bound evidence confirms two affected modules and names five predicted candidates.

**Expected**

- Confirmed and tentative paths are listed separately.
- Tentative file count does not directly affect relative score or numeric effort.
- Missing confirmation contributes to uncertainty with its evidence source.

### Case 11: Capacity and DAG enable elapsed scenarios

**Fixture**

- Calibrated P50/P80/P90 effort exists.
- Capacity receipt matches team/unit and contains dates, calendar/time zone, WIP,
  availability, reviewers, and validity.
- An acyclic dependency DAG and evidenced wait ranges cover all work packages.

**Expected**

- Result is `CALIBRATED SCHEDULE RANGE`.
- Effort, external wait, parallel work, critical path, elapsed workdays, and calendar
  dates remain separate and formulas are shown.
- No date is called a commitment or recommendation.

### Case 12: Missing capacity cannot be replaced with headcount arithmetic

**Fixture**

- Calibrated effort exists but capacity/calendar/DAG evidence is absent or stale.

**Expected**

- Result remains `CALIBRATED EFFORT ESTIMATE`.
- `Elapsed Range: UNVERIFIED` is explicit.
- The skill does not divide effort by people, assume perfect parallelism, or invent a
  start date.

### Case 13: Sprint aggregation requires compatible distributions

**Variants**

- A: every story has same-unit/model calibrated distributions and complete DAG.
- A also provides a validated hash-bound sprint aggregation model, correlation
  assumptions, and deterministic scenario set/seed.
- B: one story lacks calibration or uses another unit.

**Expected**

- A aggregates numeric distributions while preserving per-story values.
- B reports `Sprint Effort: UNVERIFIED` and identifies the blocking story.
- Per-story quantile columns are never summed and relabeled as sprint quantiles.
- Neither variant decides whether the sprint should contain the stories.

### Case 14: Scope-check receipt binding is exact

**Fixture**

- Estimate receipt initially matches Scope ID `SC-17`, baseline hash `B1`, and current
  scope hash `C1`.
- Variants alter Scope ID, baseline hash, current hash, input hash, model, sample set,
  or capacity evidence.

**Expected**

- The original receipt exposes every required binding for staged scope-check.
- A relative-only receipt remains `Effort Evidence: UNVERIFIED`; only a matching
  calibrated-effort or calibrated-schedule receipt can support `VERIFIED` effort.
- Every altered variant produces a different Estimate ID and invalidates reuse.
- An `UNBOUND`, partial, or blocked analysis is never presented as an
  `estimate-receipt`.

### Case 15: Estimate cannot make scope or schedule decisions

**Fixture**

- Calibrated evidence exceeds currently recorded sprint capacity.
- No user/producer tradeoff decision exists.

**Expected**

- The capacity conflict and affected Scope IDs are reported.
- The skill asks the user/producer to choose scope, staffing, or schedule.
- It does not recommend a budget, rank options, cut/keep/defer work, remove stories,
  re-baseline, promise a date, or invoke another workflow.

### Case 16: Mutation guard invalidates the result

**Fixture**

- Story, history, evidence, or capacity bytes change after initial hashing and before
  final reporting.

**Expected**

- Final re-hash detects the change.
- Result is `NOT ESTIMABLE — INPUT CHANGED DURING ESTIMATE`.
- Prior calculations are discarded and no consumable receipt is emitted.

### Case 17: Identical immutable inputs reproduce the estimate

**Fixture**

- Two runs use identical profile, root bytes, scope bindings, model version, history
  sample set, capacity/dependency evidence, and assumptions.

**Expected**

- Factor vector, band/range, sample inclusion/exclusion, P50/P80/P90 values, critical
  path, Estimate ID, and canonical result are identical.
- Generated timestamp is excluded from the Estimate ID.

## Protocol compliance

- [ ] Reads only the root input, applicable AGENTS chain, explicit first-level links,
      and exact manifest allowlists within budgets
- [ ] Re-hashes all consumed artifacts before reporting
- [ ] Does not scan arbitrary sprint history, code, Git, GDD, or TODO files
- [ ] Never emits numeric time without comparable-history calibration
- [ ] Never emits elapsed days/dates without capacity/calendar/DAG evidence
- [ ] Every consumable receipt binds Scope ID plus baseline/current/input hashes
- [ ] Does not write, mutate Git, invoke gates, delegate, or launch another workflow
- [ ] Does not make scope, budget, staffing, or schedule decisions

## Audit remediation coverage

- Cases 1 and 5–8 close EST-001: uncalibrated inputs remain relative-only; calibrated
  numeric effort exposes comparable samples, model, dispersion, and quantiles.
- Cases 1–4 close EST-002: story, sprint, and freeform inputs share one explicit
  profile/result/receipt contract across skill, metadata, and this specification.
- Cases 6–17 cover history comparability, no-history behavior, tentative scope,
  bounded context, confidence, blocking decisions, validation, probability semantics,
  provenance, effort-versus-elapsed separation, scope-check binding, and mutation
  safety.
