# Skill Test Spec: $balance-check

## Skill Summary

`$balance-check` performs one strictly read-only, bounded analysis pass over an
exact typed manifest. Registered adapters bind source bytes to typed variables,
units, authoritative targets/tolerances, formula ASTs, scenarios, simulations,
and deterministic evidence. The analyzer reports stable findings through a
`cgs.review-evidence/v1` envelope with a `cgs.balance-check-report/v1` extension
under contract `cgs.balance-check/v2`.

Verdicts are exactly `PASS`, `FINDINGS`, `PARTIAL`, and `ERROR`. Product targets
and values remain user/owner decisions; the analyzer never edits or selects them.

---

## P1 Remediation Trace

| Audit item | Required behavior | Primary cases |
|---|---|---|
| BLC-003 | Exact deterministic PASS/FINDINGS/PARTIAL/ERROR mapping | 15 |
| BLC-004 | Typed adapters, unit registry, formula provenance and allowlisted AST | 2, 3, 4 |
| BLC-005 | Authoritative targets/tolerances/severity only; no invented thresholds | 5, 7 |
| BLC-006 | Exact project-local manifest/artifact routing and closed domain IDs | 1, 14 |
| BLC-007 | Explicit scenario/model/strategy/time/seed assumptions and bounded uncertainty | 8, 9, 10 |
| BLC-008 | Single analyzer; no delegation, with adapter failures represented as PARTIAL | 3, 17 |
| BLC-009 | Positive/negative four-domain, unit, formula, stochastic, mutation, partial and verdict fixtures | all |

---

## Static Assertions

- [ ] Frontmatter contains only `name` and a non-empty `description`; name is
      `balance-check`.
- [ ] Declares `cgs.balance-check/v2`, `cgs.review-evidence/v1`, and
      `cgs.balance-check-report/v1`.
- [ ] Invocation exposes exact `analyze` and bounded `recheck` modes with explicit
      project-relative regular files and stable finding IDs.
- [ ] Recheck finding tokens use the exact lowercase category plus 12-hex stable
      fingerprint grammar; other stable IDs are exact and case-sensitive.
- [ ] Rejects directories, URLs, globs, regexes, latest/mtime selection, positional
      systems, ambiguity, path escapes, symlinks, and junctions.
- [ ] Declares strict read-only behavior and forbids edits, tuning, value
      selection, report persistence, approval prompts, fix loops, gates,
      delegation, remediation, and downstream skill invocation.
- [ ] Performs exactly one pass; recheck is a separate invocation that also runs
      once and stops.
- [ ] Verdict vocabulary is exactly PASS/FINDINGS/PARTIAL/ERROR with material
      coverage gaps taking precedence over clean/failing subsets.
- [ ] PASS is limited to the exact manifest/targets/model/scenarios/seeds/
      tolerances and never means globally balanced, healthy, optimal, fair, or fun.
- [ ] Reads/hashes applicable root-to-target `AGENTS.md` files and records stable
      project identity.
- [ ] Requires `cgs.balance-input-manifest/v2` and fixed candidate/source/byte/
      variable/unit/formula/AST/target/scenario/check/simulation/trial/evaluation/
      receipt/time/finding limits that a manifest may only lower.
- [ ] Hashes the complete candidate identity sequence while retaining bounded
      detailed rows and exact overflow counts/boundary keys/digests.
- [ ] Requires exact `cgs.balance-adapter-registry/v1` entries and
      `cgs.balance-adapter-receipt/v1` receipts for typed JSON/YAML/CSV, Markdown
      targets, schemas/pointers, units, formulas, scenarios/simulations, and
      recheck evidence.
- [ ] Registered adapters use exact executable identity/hash/version, typed output
      schema, argv arrays, no shell/network, project-read-only sandbox, bounded
      scratch, timeout, and receipt logs.
- [ ] Unsupported, parse-error, timeout, invalid-receipt, mutation-risk, or
      unavailable adapters make checks UNVERIFIABLE and coverage PARTIAL.
- [ ] Target authority order separates governing instructions, approved canonical
      design targets, technical budgets, and non-authoritative observed evidence.
- [ ] Primary target ambiguity/missing state is ERROR; secondary target/tolerance
      gaps are PARTIAL.
- [ ] Tolerances, inclusive boundaries, statistical decision rules, and severity
      mappings require exact authoritative source IDs/locators/hashes.
- [ ] No ±10/±20, genre standard, ideal TTK/price/drop rate, confidence target, or
      severity threshold is invented.
- [ ] Variables require stable IDs, source pointers/hashes, type, dimension, unit,
      range, null policy, base/final semantic, version, and scenario mutability.
- [ ] `cgs.balance-unit-registry/v1` provides closed, versioned exact conversions;
      percent/probability/ratio/multiplier and frames/ticks/seconds remain distinct.
- [ ] `cgs.balance-formula/v1` binds authoritative provenance, typed input/output,
      base/final semantics, formula version, allowlisted AST, rounding/overflow,
      applicability, and exact trace.
- [ ] Arbitrary code, scripts, macros, unknown functions, cycles, invalid units,
      divide-by-zero, NaN/infinity, overflow, and unspecified rounding never enter
      a balance conclusion.
- [ ] Scenarios bind stable IDs, snapshot, tiers, horizon, state, strategy, loadout,
      difficulty, typed overrides, required metrics, and deterministic/stochastic
      classification.
- [ ] `cgs.balance-simulation/v1` and
      `cgs.balance-simulation-receipt/v1` bind model/PRNG versions, seeds, trials,
      sampling, estimator, confidence/error method, decision/stopping rules,
      evaluations, diagnostics, and output digest.
- [ ] Inconclusive uncertainty or insufficient precision is PARTIAL, never rounded
      into PASS/FAIL; seeds/trials are never extended to seek a result.
- [ ] Four domain checks are scope/model/target bounded and never infer dominant,
      unkillable, useless, infinite, dead zone, spike, or healthy claims from prose.
- [ ] Stable `BLF-...` findings exclude mutable paths/pointers/wording/hashes/
      values/severity/status/owner/run/timestamp/recommendation from identity.
- [ ] Uniquely provable correction candidates remain read-only evidence; product
      decisions get exactly two or three unranked options and no selected winner.
- [ ] Coverage is explicit per source/channel/check and reconciles every declared,
      evaluated, failed, unverifiable, not-run, stale, and error count.
- [ ] Deterministic extension/envelope hashes recompute; observation time is
      excluded from the same-input analysis payload hash.
- [ ] Recheck validates prior evidence/change receipt, preserves selected IDs,
      limits regressions, never broadens scope, and never auto-runs again.
- [ ] Recheck change evidence conforms to `cgs.balance-change-receipt/v1`.
- [ ] Metadata describes typed adapters, authoritative targets/units/formulas,
      bounded simulations, hash-bound verdicts, read-only behavior, and no product
      value selection.

---

## Director and Delegation Checks

None. Balance-check uses one analyzer and registered deterministic adapters only.
It never invokes a director, economy designer, systems designer, reviewer,
specialist, recorder, remediation agent, or downstream workflow. Adapter failure
is evidence coverage failure, not a reason to invent or delegate a fallback.

---

## Required Fixture Contract

Fixtures provide exact raw bytes and expected SHA-256 values for the manifest,
instructions, typed data, schemas, target/technical sources, adapter and unit
registries, formula sources/AST receipts, scenarios, simulation receipts, prior
evidence/change receipts, and expected canonical evidence. Adapter and simulator
time/failure behavior is injected deterministically. Mutation tests snapshot all
project paths before and after.

---

## Test Cases

### Case 1: Exact invocation and artifact routing

Fixture:

- A valid `cgs.balance-input-manifest/v2` binds one analysis/snapshot, stable
  combat/economy/progression/loot domain and system IDs, and every source hash.
- Invalid variants use a directory, URL, glob, regex, `latest`, duplicate flag,
  positional system, external/absolute path, dot segment, symlink, junction,
  duplicate stable ID, or ambiguous artifact pointer.

Inputs:

```text
$balance-check analyze --manifest design/balance/manifests/combat-a1.yaml
$balance-check recheck --manifest design/balance/manifests/combat-a2.yaml --prior-evidence evidence/combat-a1.yaml --change-receipt changes/combat-a1-a2.yaml --findings BLF-target-0123456789ab
```

Expected behavior:

1. Valid invocations resolve only the named project-local regular files and exact
   stable IDs.
2. Invalid invocations return verdict `ERROR`, no review-evidence envelope, and
   run no adapter/simulation.
3. No source is guessed from common balance/GDD directories, Git, mtime, or name.

Assertions:

- [ ] Routing is exact, unique, confined, and no-follow.
- [ ] Domain and system identity come from the manifest, not user prose.
- [ ] Invalid inputs are not exposed or executed.

---

### Case 2: Typed adapter receipts build one normalized snapshot

Fixture:

- JSON, YAML, CSV, and Markdown sources have registered exact parser adapters.
- Receipts bind executable/tool identity/hash/version, input bytes, typed output
  schema, pointers/sections, argv digest, sandbox, logs, and target snapshot.
- Every source is parsed once into stable variable/target/formula/scenario IDs.

Input: Analyze the exact multi-source manifest.

Expected behavior:

1. Source extension alone has no evidentiary effect.
2. Typed output enters one in-memory index and is reused by checks.
3. Each normalized record retains source artifact, pointer/locator, raw hash,
   schema, adapter, and receipt digest.
4. No per-check reparsing or undeclared repository scan occurs.

Assertions:

- [ ] Adapter registry and receipts conform to v1 contracts.
- [ ] Sandbox is project-read-only and network-free.
- [ ] Exact parser failures are distinguishable from conclusive schema failures.

---

### Case 3: Missing, unsafe, or failing adapter is PARTIAL

Fixture variants:

- No compatible YAML adapter.
- Executable hash/version mismatches registry.
- Parser times out or emits malformed/truncated output.
- Registry supplies a shell string, network dependency, or project-writing
  adapter.

Expected behavior:

1. States are `UNSUPPORTED`, `INVALID_RECEIPT`, `TIMEOUT`, `PARSE_ERROR`, or
   `NOT_RUN` as exact evidence dictates.
2. Affected rows/checks are `UNVERIFIABLE`; adapter coverage is incomplete.
3. Verdict is `PARTIAL` when domain/primary target remain trustworthy.
4. Actual detected project mutation is `ERROR` with no evidence record.

Assertions:

- [ ] No parser is synthesized and no role is delegated as fallback.
- [ ] Parse/timeout/unsupported is not a balance finding or PASS.
- [ ] No project bytes change in a valid run.

---

### Case 4: Unit and formula provenance is typed and exact

Fixture variants:

- Exact frame-to-seconds conversion cites a target frame-rate rule.
- Another conversion lacks frame rate.
- Percent, probability, ratio, and multiplier values share display numbers but
  distinct unit IDs.
- Formula records cover base/final damage with an allowlisted typed AST.
- Invalid records contain ambiguous stage, unit-invalid addition, unknown
  function, cycle, division by zero, NaN/infinity, overflow, or missing rounding.

Expected behavior:

1. Valid conversions/formulas produce exact typed traces.
2. Missing conversion context and invalid formula semantics are
   `UNVERIFIABLE`/`PARTIAL` unless primary scope cannot be identified, then
   `ERROR`.
3. Formula text is never executed as code.
4. A provable formula/schema defect may produce a stable finding while blocked
   dependent checks remain PARTIAL.

Assertions:

- [ ] Original/normalized values and conversion IDs are preserved.
- [ ] Base and final semantics never collapse implicitly.
- [ ] Resource currencies/XP are not merged by display label.

---

### Case 5: Authoritative target and tolerance precedence

Fixture:

- Governing instruction sets a safety constraint.
- Approved canonical GDD target sets TTK with exact applicability and inclusive
  tolerance boundaries.
- Technical budget sets a CPU limit only.
- Telemetry and a historical report contain different observed TTK values.
- Secondary metric has no tolerance.

Expected behavior:

1. Governing, canonical design, and technical sources remain within their domains.
2. Telemetry/history are comparison evidence, not silently promoted targets.
3. The secondary check is `UNVERIFIABLE` and verdict `PARTIAL`.
4. No ±10/±20, genre standard, ideal target, confidence, or severity is invented.

Assertions:

- [ ] Each target/tolerance cites stable ID, owner, lifecycle, locator, hash, and
      schema.
- [ ] Boundary direction/inclusivity and decision rule are exact.
- [ ] Conflicting primary targets yield `ERROR`; secondary conflicts yield
      `PARTIAL`.

---

### Case 6: Fully evidenced combat scope returns PASS only locally

Fixture:

- Typed damage, cooldown, health, mitigation, time, resistance, and loadout data.
- Current formula ASTs and authoritative DPS/TTK targets/tolerances.
- Complete declared tier/state/strategy scenarios; all checks pass.
- Every adapter, unit, formula, scenario, and coverage row is current and within
  bounds.

Expected behavior:

1. Verdict is `PASS`, workflow `COMPLETE`, coverage `FULL`.
2. Every metric has exact formula/conversion/scenario evidence.
3. Output says PASS is limited to this manifest/model/targets/matrix.
4. It never says globally BALANCED, HEALTHY, optimal, fair, or fun.

Assertions:

- [ ] A complete clean scope, not an empty search, supports PASS.
- [ ] Counts reconcile exactly.
- [ ] No value/report/project file is changed.

---

### Case 7: Economy exploit is a finding; response remains a decision

Fixture:

- A typed faucet/sink graph defines stable resource IDs, initial state, horizon,
  strategy, prices, formulas, and hard no-positive-repeatable-cycle target.
- One current scenario proves a repeatable positive currency loop.
- Multiple legitimate product responses exist.

Expected behavior:

1. Complete coverage produces stable `MODEL_VIOLATION`/`FINDINGS` evidence with
   exact reproduction and authoritative severity.
2. The analyzer presents exactly two or three mutually exclusive responses with
   measured effects/risks/owners/validation needs.
3. It prints `Recommended Option: NONE — PRODUCT OWNER DECISION REQUIRED`.
4. It does not choose a price/faucet/sink value or invoke an owner.

Assertions:

- [ ] Infinite/exploit claim has exact model, state, strategy, and horizon.
- [ ] Severity comes from authoritative policy, not magnitude rhetoric.
- [ ] Every option is unranked and unapplied.

---

### Case 8: Progression target absence preserves product ownership

Fixture:

- Typed XP/power/unlock curves and formulas are valid.
- Current data has no calculation defect.
- No approved primary pacing target chooses between plausible curve directions.

Expected behavior:

1. Primary analysis question is undefined and verdict is `ERROR` with no evidence
   envelope.
2. No smooth curve, ideal pace, midpoint, or genre baseline is invented.
3. A diagnostic may identify the design owner and missing stable target record.
4. No option is applied or treated as default.

Assertions:

- [ ] Missing primary target differs from a missing secondary tolerance.
- [ ] Product owner retains the numeric decision.
- [ ] Error path remains strictly read-only.

---

### Case 9: Seeded loot simulation is reproducible

Fixture:

- Probability/pity/duplicate state machine, inventory/utility state, and target
  precision are fully typed.
- `cgs.balance-simulation/v1` declares PRNG/model versions, ordered seeds, trials,
  sampling, estimator, confidence/error method, stopping and decision rules.
- A valid simulation receipt binds all source/formula/target/scenario hashes.

Expected behavior:

1. Two runs over identical bytes/receipts produce identical deterministic payload,
   checks, findings, and payload hash.
2. Distribution summary, interval/error, sample size, diagnostics, and limitations
   are reported.
3. No seed/trial/outlier/method changes occur after seeing results.
4. “Useless” is used only with an exact utility target/state/comparison set.

Assertions:

- [ ] PRNG and simulator identity are versioned.
- [ ] Closed-form results are preferred when declared model permits them.
- [ ] Observation timestamp is outside deterministic analysis hashing.

---

### Case 10: Uncertainty overlap and trial limits yield PARTIAL

Fixture variants:

- Confidence interval overlaps the authoritative decision boundary.
- Declared precision is not achieved within fixed trials.
- Missing seed, PRNG/model version, confidence method, or decision rule.
- Requested trials/evaluations/time exceed fixed caps.

Expected behavior:

1. Check is `INCONCLUSIVE_UNCERTAINTY` or `UNVERIFIABLE`.
2. Simulation coverage is incomplete and verdict is `PARTIAL`.
3. Complete subset estimates remain visible but non-exhaustive.
4. Trials/seeds/confidence are not extended or changed to force PASS/FAIL.

Assertions:

- [ ] Uncertainty is not rounded away.
- [ ] Fixed caps cannot be raised by the manifest.
- [ ] PARTIAL is not described as balanced or harmless.

---

### Case 11: Bounded manifest overflow remains reproducible

Fixture:

- Candidate, source, formula, scenario, or finding counts exceed fixed/effective
  caps.
- The complete ordered identity sequence remains enumerable.

Expected behavior:

1. Complete identity digest, retained bounded prefix, exact total/omitted count,
   boundary sort keys, and omitted digest are recorded.
2. Omitted items are neither parsed nor judged.
3. One aggregate `OVER_LIMIT` coverage row names every affected check.
4. Verdict is `PARTIAL`, never PASS/FINDINGS from a sample.

Assertions:

- [ ] Output remains bounded without silently hiding overflow.
- [ ] No individual omitted ID list is required beyond configured detailed caps.
- [ ] Same identity stream produces the same overflow digest.

---

### Case 12: Stable findings survive non-semantic changes

Fixture:

- Run A contains one target violation with stable system/metric/check/formula/
  scenario/target/evidence artifact IDs.
- Run B moves the source path, changes wording, raw bytes/current value, severity
  presentation, owner, and timestamp without changing logical identity.
- Run C changes the stable scenario or target ID.

Expected behavior:

1. Runs A/B retain one `BLF-...` finding ID while artifact/manifest/payload/record
   hashes change.
2. Run C produces a different fingerprint and ID.
3. Incompatible evidence under one fingerprint forces `PARTIAL`.

Assertions:

- [ ] Paths, pointers, wording, hashes, values, deviation, severity, confidence,
      status, owner, run, timestamp, and recommendation are excluded.
- [ ] Stable logical IDs and evidence artifact IDs participate.
- [ ] Findings sort deterministically.

---

### Case 13: Unique correction and product option remain distinct

Fixture:

- Variant A has a unit/schema-derived value whose correction is mathematically
  unique under current authoritative evidence.
- Variant B has valid data but two plausible TTK targets.

Expected behavior:

1. Variant A emits a read-only correction candidate with proof, downstream
   recomputation set, owner, and acceptance.
2. Variant B is a `PRODUCT_DECISION` with exactly two or three unranked options and
   no recommended winner.
3. Neither source is edited and neither choice is applied.

Assertions:

- [ ] Correction candidate requires uniqueness, not preference.
- [ ] Product target selection remains with the product/design owner.
- [ ] No same-session fix-and-verify loop starts.

---

### Case 14: Unsafe, unsupported, stale, and ambiguous inputs fail closed

Fixture variants:

- Executable/script/environment/binary input.
- Unsupported source/schema or ambiguous pointer/duplicate identity.
- Escaping path/symlink or changed source bytes after manifest lock.
- Unsafe formula grammar that prevents primary metric definition.

Expected behavior:

1. Invalid primary scope/grammar returns `ERROR` with no evidence envelope.
2. A valid scope with secondary stale/unsupported evidence returns `PARTIAL` and
   preserves unaffected evidence.
3. Final re-enumeration/re-hashing detects added/removed/renamed/changed inputs and
   discards old-byte calculations.
4. No invalid source is executed or substituted.

Assertions:

- [ ] Error versus partial follows primary-scope trustworthiness.
- [ ] Hashes, not mtime/Git labels, determine currentness.
- [ ] Mixed snapshots never yield PASS or FINDINGS.

---

### Case 15: Verdict and coverage matrix is total

Evaluate independent variants:

| Evidence state | Verdict | Coverage | Workflow |
|---|---|---|---|
| invalid invocation/scope/primary target/unsafe grammar/no trustworthy packet | `ERROR` | `NONE` | `ERROR` |
| any material required coverage gap, including uncertainty | `PARTIAL` | `PARTIAL` | `PARTIAL` |
| full coverage with actionable open findings | `FINDINGS` | `FULL` | `COMPLETE` |
| full coverage with no actionable finding | `PASS` | `FULL` | `COMPLETE` |

Assertions:

- [ ] First matching rule is applied mechanically.
- [ ] PARTIAL takes precedence over clean or failing subsets while known findings
      remain visible.
- [ ] Vocabulary excludes BALANCED, HEALTHY, CONCERNS, CRITICAL ISSUES, and OUT OF
      BALANCE.
- [ ] Mutation is READ_ONLY and persistence NONE on every non-error packet.

---

### Case 16: Hash-bound evidence is deterministic and current

Fixture:

- All inputs, adapters, targets, units, formulas, scenarios, simulations, and
  checks are current and within limits.
- Expected canonical extension and envelope bytes are supplied.

Expected behavior:

1. Extension conforms to `cgs.balance-check-report/v1` and envelope to
   `cgs.review-evidence/v1`.
2. Artifact, inventory, manifest, deterministic payload, and record hashes
   recompute.
3. Same inputs/receipts produce identical deterministic payload bytes.
4. Outer timestamp changes observation provenance without changing the
   deterministic payload hash.

Assertions:

- [ ] Any byte change invalidates the relevant artifact and downstream hashes.
- [ ] Inconsistent construction returns ERROR without an evidence record.
- [ ] Summary is not a weaker machine-evidence mode because no summary flag exists.

---

### Case 17: Strict read-only and no delegation

Fixture:

- Analysis finds one proven schema defect and one product decision.
- User asks to fix both, save the report, delegate to economy designer, and rerun
  until clean.
- One adapter requests a project-writing sandbox.

Expected behavior:

1. Analyzer reports one correction candidate and unranked product options.
2. It does not write, ask for write approval, delegate, invoke a skill/agent,
   persist evidence, or start another pass.
3. Mutating adapter is `NOT_RUN`, affected coverage is `PARTIAL`.
4. It returns at most one external owner-routed recommendation and stops.

Assertions:

- [ ] No project, report, test, registry, index, or session bytes change.
- [ ] Delegation failure cannot be hidden because delegation is not part of the
      contract.
- [ ] Analyzer never selects product values.

---

### Case 18: Recheck is one bounded verification pass

Fixture:

- Prior exact `cgs.review-evidence/v1` record contains two stable findings.
- Change receipt binds before/after artifacts, hashes, pointers, owner authority,
  and affected stable IDs for only finding A.
- Invocation selects A plus named regression checks; B is unselected.

Expected behavior:

1. Prior envelope/payload/artifacts/project/analysis/target/formula/unit/scenario/
   finding hashes and change receipt all validate.
2. A keeps its ID and becomes `RESOLVED_IN_CURRENT`, `STILL_OPEN`, or
   `UNVERIFIABLE` only from current evidence.
3. B is preserved as out-of-scope history, not reverified.
4. New regressions use stable `BLF-REGRESSION-*` identities.
5. Analyzer reports open blockers and stops whether zero or nonzero.

Assertions:

- [ ] Recheck never broadens domain, target, model, or semantic meaning.
- [ ] Change evidence conforms to `cgs.balance-change-receipt/v1`.
- [ ] Unauthorized semantic expansion requires a new analyze manifest/ID.
- [ ] No automatic second recheck occurs.

---

## Protocol Compliance

- [ ] Exact invocation, project identity, source bytes, adapters, targets, units,
      formulas, scenarios, simulations, and checks are hash-bound.
- [ ] Fixed budgets and overflow digests make analysis bounded without claiming
      sampled completeness.
- [ ] Typed adapter failure is visible coverage, not inferred evidence or delegated
      fallback.
- [ ] Target/tolerance/severity authority and unit/formula provenance are explicit.
- [ ] Scenario/stochastic conclusions disclose model, horizon, strategy, state,
      PRNG/seeds/trials/confidence/error and decision limits.
- [ ] Every material gap or inconclusive uncertainty prevents PASS/FINDINGS.
- [ ] Stable findings preserve logical identity across non-semantic edits.
- [ ] Product options remain unranked and correction candidates unapplied.
- [ ] Analyzer and recheck are single-pass, project-read-only, conversation-only,
      and invoke no gate, agent, recorder, owner, or downstream workflow.
- [ ] Output conforms to `cgs.review-evidence/v1` plus
      `cgs.balance-check-report/v1` under `cgs.balance-check/v2`.

---

## Coverage Notes

Tests must distinguish primary-scope `ERROR` from secondary-coverage `PARTIAL`, a
conclusive target violation from a parse failure, deterministic receipt replay
from a new simulation, exact conversion from a guessed unit, and uncertainty
overlap from a definitive target decision. Four domain fixtures are mandatory:
combat, economy, progression, and loot.

Report persistence belongs to a separate recorder contract. The catalog entry
points to this file, and its `last_*` fields remain blank until an authorized test
workflow actually executes every case. Editing the contract/spec or running
structural probes alone is not a test pass and must not create a catalog result.
