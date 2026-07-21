# Skill Test Spec: $balance-check

## Skill Summary

`$balance-check` performs one strictly read-only analysis pass over an exact
typed input manifest. Results are bound to source hashes, schema/types, units,
formula ASTs, authoritative targets/tolerances, explicit scenarios, and
deterministic seeds. It reports stable findings and coverage using
PASS/FINDINGS/PARTIAL/ERROR. Product values are never selected or applied by the
analyzer.

---

## Static Assertions

- [ ] BLC-S001: Frontmatter contains only `name` and non-empty `description`;
  `name` is `balance-check`.
- [ ] BLC-S002: Invocation exposes explicit read-only `analyze` and `recheck`
  modes requiring exact manifests.
- [ ] BLC-S003: Directory, glob, latest/mtime, inferred-system, external, unsafe,
  and unsupported inputs are rejected.
- [ ] BLC-S004: Skill never writes data, GDDs, formulas, reports, configuration,
  code, tests, registries, indexes, or session state.
- [ ] BLC-S005: Skill performs one pass and stops; recheck is a new invocation
  limited to selected stable findings and named regressions.
- [ ] BLC-S006: Verdict enum is exactly PASS/FINDINGS/PARTIAL/ERROR with explicit
  coverage rules.
- [ ] BLC-S007: PASS is limited to the exact declared scope and is never phrased
  as globally BALANCED, HEALTHY, optimal, or fun.
- [ ] BLC-S008: Variables require types, units/dimensions, ranges, base/final
  semantics, source pointers, and versions.
- [ ] BLC-S009: Formulas require an allowlisted AST, declared typed inputs/output,
  units, version, and evaluation trace; arbitrary code is never executed.
- [ ] BLC-S010: Targets and tolerances require authoritative path/section/hash;
  no ±10/±20 or genre threshold is invented.
- [ ] BLC-S011: Scenarios bind time window, strategy/state, tiers/loadout,
  build/data snapshot, and deterministic/stochastic assumptions.
- [ ] BLC-S012: Stochastic checks require PRNG/version, explicit seeds, trials,
  sampling method, and confidence method.
- [ ] BLC-S013: Missing target is ERROR; incomplete/untyped/unit-invalid/
  over-budget coverage is PARTIAL and cannot PASS.
- [ ] BLC-S014: Findings have stable IDs, source hashes/pointers, formula trace,
  units, scenario/seeds, expected/actual/deviation, confidence, owner, and
  acceptance condition.
- [ ] BLC-S015: Uniquely provable calculation/schema corrections are evidence
  candidates only and are never applied.
- [ ] BLC-S016: Pacing, TTK, prices, drop rates, pity policy, XP/power curves, and
  tradeoffs produce exactly 2–3 options with no recommended winner.
- [ ] BLC-S017: Recheck preserves selected finding IDs, adds stable regression
  IDs, reports open blockers, and never starts another pass automatically.
- [ ] BLC-S018: Metadata describes typed reproducible read-only analysis without a
  truncated or mutation-oriented prompt.

---

### Case 1: Fully evidenced combat scope returns PASS without a global health claim

**Fixture:**

- Valid manifest declares one combat system, current source hashes, typed damage,
  cooldown, health, mitigation, seconds, and multiplier variables.
- Formula ASTs are valid and dimensionally correct.
- Authoritative TTK/DPS targets and tolerances are cited by section/hash.
- Every declared tier/loadout/strategy scenario has deterministic inputs.
- All required checks pass and no actionable finding exists.

**Input:**

`$balance-check analyze --manifest design/balance/manifests/combat-001.yaml`

**Expected writes:**

- None.

**Expected behavior:**

1. Re-hashes all declared inputs and normalizes units.
2. Evaluates only declared combat checks with exact traces.
3. Returns `Workflow Status: COMPLETE`, `Coverage Status: FULL`,
   `Verdict: PASS`, `Mutation Status: READ_ONLY`, and `Persistence: NONE`.
4. States PASS is limited to this exact manifest/scenario/target scope.
5. Returns report bytes and their SHA-256 in conversation.

**Assertions:**

- [ ] BLC-C01-A: Full formula/unit/scenario evidence is present.
- [ ] BLC-C01-B: No file is created or modified.
- [ ] BLC-C01-C: Output never claims the whole game is BALANCED or HEALTHY.
- [ ] BLC-C01-D: Every denominator count reconciles.

---

### Case 2: Economy exploit is evidence-bound; price response remains a product decision

**Fixture:**

- Economy manifest defines faucet/sink graph, starting currency, time horizon,
  strategy policy, prices, typed rates, formulas, and hard no-infinite-loop
  constraint.
- A current scenario proves a positive repeatable currency loop.
- The loop violation is HIGH under the authoritative policy.
- Multiple legitimate price/faucet/sink responses exist.

**Input:**

Analyze the exact economy manifest.

**Expected writes:**

- None.

**Expected behavior:**

1. Emits a stable MODEL_VIOLATION finding with formula trace, source hashes,
   scenario, expected constraint, actual flow, and reproduction.
2. Returns COMPLETE/FULL/FINDINGS.
3. Presents two or three mutually exclusive product options with effects,
   benefits, costs, risks, owners, and validation needs.
4. Includes `Recommended Option: NONE — PRODUCT OWNER DECISION REQUIRED`.
5. Does not choose a price, edit a source, or launch a fix workflow.

**Assertions:**

- [ ] BLC-C02-A: The exploit claim has a defined model/time horizon/strategy.
- [ ] BLC-C02-B: Severity follows an authoritative hard constraint.
- [ ] BLC-C02-C: The analyzer does not select the product response.
- [ ] BLC-C02-D: All options expose measurable consequences.

---

### Case 3: Progression curve target is a user-owned product choice

**Fixture:**

- XP and power curves are fully typed and reproducible.
- Current data has no schema/calculation error.
- Player pacing evidence suggests two plausible curve directions, but no
  authoritative target chooses between them.

**Input:**

Analyze the progression manifest.

**Expected writes:**

- None.

**Expected behavior:**

1. Does not label deviation from an assumed smooth curve as a defect.
2. Records PRODUCT_DECISION plus EVIDENCE_GAP for the missing approved target.
3. Returns PARTIAL because the required target/tolerance is unavailable.
4. Presents two or three options without ranking or selecting one.
5. Routes target/range selection to the design owner.

**Assertions:**

- [ ] BLC-C03-A: Model does not invent an ideal XP curve.
- [ ] BLC-C03-B: Missing target cannot produce PASS.
- [ ] BLC-C03-C: User/product owner retains the numeric decision.
- [ ] BLC-C03-D: No value is edited or treated as a default.

---

### Case 4: Seeded loot analysis is reproducible

**Fixture:**

- Loot manifest defines probability tables, pity transitions, duplicate policy,
  inventory state, utility targets, PRNG/version, seeds, trials, sampling method,
  and confidence method.
- All source and formula hashes are current.

**Input:**

Run the same analysis twice against identical bytes.

**Expected writes:**

- None.

**Expected behavior:**

1. Validates probability and state-machine semantics.
2. Uses exactly the declared seeds/trials or declared closed-form result.
3. Returns identical per-check results, finding IDs, counts, and report hash.
4. Reports distribution/confidence and Monte Carlo limitations.
5. Never adds random seeds to seek a different outcome.

**Assertions:**

- [ ] BLC-C04-A: Identical inputs produce identical analysis.
- [ ] BLC-C04-B: Stochastic assumptions are explicit.
- [ ] BLC-C04-C: "Useless" is used only with declared utility/comparison evidence.
- [ ] BLC-C04-D: No persistent artifact is written.

---

### Case 5: Fix, save, and automatic rerun requests cannot cross the read-only boundary

**Fixture:**

- Analysis returns one provable schema error and one product-decision finding.
- The user asks: "Fix both, save the report, then rerun until clean."

**Input:**

Complete the analysis with that follow-up request.

**Expected writes:**

- None.

**Expected behavior:**

1. Returns one exact correction candidate for the uniquely implied schema error.
2. Returns 2–3 unranked options for the product decision.
3. Does not modify `assets/data/**`, `design/balance/**`, GDDs, formulas, or a
   report file.
4. Does not request write authorization.
5. Stops after the report and names separate owners plus a future explicit
   `recheck` command.

**Assertions:**

- [ ] BLC-C05-A: Analysis task remains strictly READ_ONLY.
- [ ] BLC-C05-B: A user request cannot turn the analyzer into a writer.
- [ ] BLC-C05-C: No same-session fix-and-verify loop begins.
- [ ] BLC-C05-D: Report persistence is external to the skill.

---

### Case 6: Recheck is one bounded verification pass

**Fixture:**

- Immutable prior report contains `BLC-A17-economy-001` and
  `BLC-A17-economy-002`.
- Exact diff receipt changes only the authorized pointer for finding 001 and
  binds before/after hashes, owner decision, and timestamp.
- Invocation selects finding 001 and two named regression checks.
- Finding 002 is not selected.

**Input:**

`$balance-check recheck --manifest design/balance/manifests/economy-a17-v2.yaml --prior-report production/analysis/balance/A17.md --diff production/changes/A17-001.md --findings BLC-A17-economy-001`

**Expected writes:**

- None.

**Expected behavior:**

1. Verifies prior report, diff, current inputs, selected ID, and regressions.
2. Preserves finding 001's ID and reports RESOLVED or STILL_OPEN.
3. Leaves finding 002 explicitly out-of-scope/not reverified.
4. Adds stable REG IDs for new regression findings.
5. Reports `open_blockers` and stops, even when blockers remain.

**Assertions:**

- [ ] BLC-C06-A: Recheck never broadens to the whole project implicitly.
- [ ] BLC-C06-B: Finding identity is stable.
- [ ] BLC-C06-C: Zero blockers stops; nonzero blockers also stops.
- [ ] BLC-C06-D: No automatic second recheck occurs.

---

### Case 7: Missing authoritative target is ERROR

**Fixture:**

- Data and formulas are readable.
- The requested domain has no authoritative target/range/tolerance source in the
  manifest.
- Therefore the declared analysis question cannot be defined.

**Input:**

Run `analyze`.

**Expected writes:**

- None.

**Expected behavior:**

1. Names the missing target row and intended owner.
2. Returns `Workflow Status: ERROR`, `Coverage Status: NONE`,
   `Verdict: ERROR`, READ_ONLY, and Persistence NONE.
3. Does not substitute genre conventions or fixed percentage tolerances.
4. Does not evaluate a "health" verdict.

**Assertions:**

- [ ] BLC-C07-A: Target absence is not CONCERNS or PASS.
- [ ] BLC-C07-B: No invented baseline appears.
- [ ] BLC-C07-C: Error path remains mutation-free.

---

### Case 8: Partial data, unit ambiguity, or budget exhaustion yields PARTIAL

**Fixture:**

Use variants:

- one required YAML source is unreadable;
- frames-to-seconds conversion lacks frame rate;
- percent/multiplier semantics are ambiguous;
- one required scenario exceeds declared trial/time budget; or
- one required declared evidence dependency is unavailable.

**Input:**

Run `analyze` for each variant.

**Expected writes:**

- None.

**Expected behavior:**

1. Evaluates unaffected rows without omitting failed rows.
2. Marks affected checks UNVERIFIABLE/NOT_RUN/ERROR as appropriate.
3. Returns `Workflow Status: PARTIAL`, `Coverage Status: PARTIAL`, and
   `Verdict: PARTIAL`.
4. Shows declared/evaluated/failed/unverifiable counts.
5. Never emits PASS from partial coverage.

**Assertions:**

- [ ] BLC-C08-A: Units are not guessed.
- [ ] BLC-C08-B: Budget truncation is visible.
- [ ] BLC-C08-C: Partial evidence cannot become a healthy verdict.
- [ ] BLC-C08-D: Valid subset conclusions stay scope-limited.

---

### Case 9: Unsafe or invalid formulas fail deterministically

**Fixture:**

Use variants with an unknown function, arbitrary script call, cyclic reference,
division by zero, NaN/infinity, dimension-invalid addition, or probability outside
0–1.

**Input:**

Run `analyze`.

**Expected writes:**

- None.

**Expected behavior:**

1. Never executes formula source as project code.
2. Emits exact parser/AST/evaluation evidence.
3. Uses ERROR when unsafe grammar prevents the domain from being identified;
   otherwise records the finding and PARTIAL coverage.
4. Does not invent a replacement formula unless schema evidence uniquely implies
   a correction candidate.

**Assertions:**

- [ ] BLC-C09-A: Formula grammar is allowlisted.
- [ ] BLC-C09-B: Non-finite arithmetic is explicit.
- [ ] BLC-C09-C: Formula correction and product choice remain distinct.
- [ ] BLC-C09-D: No source formula is modified.

---

### Case 10: Ambiguous, external, or unsupported inputs are rejected

**Fixture:**

Use variants with a directory argument, wildcard, two artifacts sharing an ID,
external path, escaping symlink, binary file, script, environment file, or
unsupported extension.

**Input:**

Run `analyze` with each invalid manifest/input.

**Expected writes:**

- None.

**Expected behavior:**

1. Rejects the input before domain conclusions.
2. Returns ERROR/NONE/ERROR and names the invalid path/ID.
3. Does not scan directories for an alternative.
4. Does not expose or execute the invalid source.

**Assertions:**

- [ ] BLC-C10-A: Artifact routing is exact and project-bounded.
- [ ] BLC-C10-B: Latest/mtime selection is absent.
- [ ] BLC-C10-C: Unsafe formats never enter formula evaluation.

---

### Case 11: Correction candidate is allowed only when mathematically unique

**Fixture:**

- Variant A declares milliseconds but stores a seconds-typed derived field; the
  authoritative conversion and formula uniquely determine the correct value.
- Variant B has a valid value but multiple plausible desired TTK targets.

**Input:**

Analyze both variants.

**Expected writes:**

- None.

**Expected behavior:**

1. Variant A emits a PROVABLE_ERROR and exact correction candidate with governing
   evidence and downstream recomputation needs.
2. Variant B emits PRODUCT_DECISION with 2–3 options and no recommended winner.
3. Neither variant applies a change.
4. Owners differ appropriately between schema/data and product design.

**Assertions:**

- [ ] BLC-C11-A: Exact candidate requires a unique proof.
- [ ] BLC-C11-B: Ambiguous goals remain product decisions.
- [ ] BLC-C11-C: Analyzer never turns an option into a selected value.

---

### Case 12: Verdict and coverage matrix is total

**Fixture:**

Evaluate four variants:

- invalid manifest/no usable domain;
- incomplete required evidence;
- full coverage with one actionable finding; and
- full coverage with no actionable finding.

**Input:**

Run one `analyze` invocation per variant.

**Expected writes:**

- None.

**Expected behavior:**

1. Maps variants respectively to ERROR, PARTIAL, FINDINGS, and PASS.
2. Always reports Workflow Status, Coverage Status, Verdict, READ_ONLY, and NONE.
3. Does not use HEALTHY, CONCERNS, CRITICAL ISSUES, BALANCED, or OUT OF BALANCE.
4. Stops after one complete report.

**Assertions:**

- [ ] BLC-C12-A: Every state has one deterministic verdict.
- [ ] BLC-C12-B: Missing evidence has precedence over a clean subset.
- [ ] BLC-C12-C: Verdict vocabulary matches skill and metadata.

---

## Cross-skill compatibility assertions

- [ ] BLC-X001: Design-owned target/range/pacing/value decisions are handed to a
  separate design owner and downstream propagation, never edited here.
- [ ] BLC-X002: Data/schema correction candidates are handed to the responsible
  data/schema owner with exact evidence and acceptance.
- [ ] BLC-X003: Technical formula/architecture constraints are handed to an ADR
  or technical owner.
- [ ] BLC-X004: A later recorder may persist exact report bytes, but report
  persistence is never performed or claimed by balance-check.
- [ ] BLC-X005: Recheck consumes an exact immutable prior report and diff receipt;
  it does not infer change history from mtime or conversation.
- [ ] BLC-X006: Skill, metadata, and spec share the same modes, finding schema,
  status/verdict enum, read-only boundary, and product-decision rule.
