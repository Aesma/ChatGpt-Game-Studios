---
name: balance-check
description: "Perform one strictly read-only, hash-bound balance analysis over typed data, authoritative targets, normalized units, reproducible formulas, and explicit scenarios; report evidence and product options without selecting or applying values."
---

# Balance Check

`balance-check` evaluates a declared balance scope. It is an analysis workflow,
not a tuning or implementation workflow. It never edits data, GDDs, formulas,
configuration, reports, tests, code, registries, indexes, or session state.

The skill performs exactly one analysis pass and stops. A later recheck is a new
read-only invocation that verifies selected stable findings and explicit
regressions; it is never an in-session fix-and-rerun loop.

## Invocation

Use one explicit mode:

```text
$balance-check analyze --manifest <exact-input-manifest-path>
$balance-check recheck --manifest <exact-input-manifest-path> --prior-report <exact-immutable-report-path> --diff <exact-change-receipt-path> --findings <stable-IDs>
```

All paths must be explicit project-relative files. Reject directory-only, glob,
"latest", "most recent", modification-time, inferred-system, and ambiguous inputs.
Do not search `assets/data/` or `design/gdd/` to guess the intended scope.

Both modes are strictly read-only. Do not ask for write authorization or offer to
save a report. Return the complete report in conversation and report the SHA-256
of its rendered bytes separately. A separately authorized recorder may persist
those exact bytes; this skill does not.

## Status and verdict contract

Always return:

- `Workflow Status`: `COMPLETE`, `PARTIAL`, or `ERROR`.
- `Coverage Status`: `FULL`, `PARTIAL`, or `NONE`.
- `Verdict`: `PASS`, `FINDINGS`, `PARTIAL`, or `ERROR`.
- `Mutation Status`: always `READ_ONLY`.
- `Persistence`: always `NONE`.

Derive the verdict mechanically:

| Condition | Workflow | Coverage | Verdict |
|---|---|---|---|
| Invalid/ambiguous/out-of-project manifest, no usable declared domain, or unsafe formula grammar | ERROR | NONE | ERROR |
| Any required source/check/scenario is missing, unreadable, stale, untyped, unit-invalid, over budget, nonconclusive, or required review fails | PARTIAL | PARTIAL | PARTIAL |
| Otherwise full declared coverage has one or more open actionable findings | COMPLETE | FULL | FINDINGS |
| Otherwise every declared check ran with full evidence and no open actionable finding | COMPLETE | FULL | PASS |

`PASS` means only that the exact declared manifest scope has no detected finding
under its stated targets, scenarios, seeds, tolerances, and model limitations. It
must never be phrased as globally BALANCED, HEALTHY, optimal, or fun.

## Phase 1: Validate a bounded typed input manifest

Require artifact type `balance-check-input-manifest`, schema version 1, analysis
ID, project ID/root, domain set, target system IDs, hash algorithm `sha256`,
creation timestamp, source revision, numeric model/precision/rounding/overflow
policy, explicit budgets, and ordered tables for
Sources, Variables, Formulas, Targets, Scenarios, and Required Checks.

Supported inputs are:

- structured data: `.json`, `.yaml`, or `.yml`;
- authoritative design/balance targets: project Markdown with stable section or
  requirement IDs; and
- explicit schema documents referenced by the manifest.

Reject executables, scripts as formulas, binary inputs, external paths, escaping
symlinks, environment files, and unsupported formats. Resolve each path inside
the project root, read raw bytes, and verify the manifest SHA-256. Duplicate
artifact IDs, duplicate variable/formula IDs, ambiguous pointers, changed bytes,
or malformed syntax are ERROR when they prevent the declared domain from being
identified; otherwise they make affected required coverage PARTIAL.

The manifest must set limits for file count, total bytes, formula nodes, scenario
count, stochastic trials, and analysis time. Do not silently truncate. When a
limit prevents a required check, list the omitted IDs and return PARTIAL.

### Sources table

Each source row requires:

- stable artifact ID, exact path, format, lifecycle status, and SHA-256;
- domain and authoritative owner;
- exact JSON/YAML pointer or Markdown section/requirement ID;
- declared role: data, schema, target, formula, or scenario; and
- precedence when multiple sources legitimately contribute.

If no authoritative target set exists for the requested domain or its primary
analysis question, return ERROR. If that set exists but a secondary required
metric lacks a target/tolerance, or a secondary source/row is missing, return
PARTIAL. Never invent a target from industry
conventions or another game.

### Typed variables and units

Every variable requires stable ID, source artifact/pointer, scalar/container type,
unit and dimension, allowed range, null policy, base/final semantic, and version.
Percent, probability, multiplier, frames, seconds, currency, XP, damage, health,
count, and rate are distinct semantics.

Unit conversions must be declared in the manifest with source and version. Do not
assume frame rate, convert percent to multiplier implicitly, or combine
incompatible dimensions. An undefined or dimensionally invalid value is
`UNVERIFIABLE` and makes required coverage PARTIAL.

### Formula grammar and AST

Every formula requires stable ID, authoritative source location/hash, declared
inputs/output types and units, exact expression, formula version, and parsed AST.
Use only an allowlisted grammar: numeric literals, typed variable references,
parentheses, `+`, `-`, `*`, `/`, `min`, `max`, `clamp`, `pow`, comparisons, and
declared piecewise branches.

Never execute source text, project scripts, macros, arbitrary functions, or
embedded code. Reject unknown functions, missing variables, cycles,
dimension-invalid operations, division by zero, invalid probability, NaN, and
infinity. Record the exact AST and evaluation trace for every result.

### Targets and tolerances

Every expected value/range, pacing goal, hard constraint, comparison baseline,
and tolerance must cite an authoritative path, section/ID, and source hash.
Tolerance direction and boundary inclusivity must be explicit.

Do not invent ±10%, ±20%, genre standards, ideal TTK, ideal prices, or acceptable
drop rates. If a required metric has no authoritative target/tolerance, record
`UNVERIFIABLE — PRODUCT TARGET REQUIRED` and return PARTIAL.

## Phase 2: Freeze reproducible scenario coverage

Every scenario requires:

- stable scenario ID and domain;
- candidate/build or data snapshot ID;
- power/content tier, time horizon, start state, player strategy or policy,
  loadout, difficulty, and relevant system state;
- exact variable overrides and units;
- deterministic/stochastic classification;
- for stochastic checks, PRNG algorithm/version, explicit seeds, trials, sampling
  method, and confidence method; and
- required metric/check IDs.

Conclusions apply only to this matrix. "Dominant", "unkillable", "useless",
"infinite", "dead zone", "power spike", and "healthy economy" are invalid claims
without defined alternatives, time windows, strategies, state constraints, and
targets.

For stochastic analysis, prefer an exact closed-form result when the declared
model permits it. Otherwise run only the manifest-defined seeds/trials and report
sample size, distribution summary, confidence interval, and Monte Carlo error.
Missing seeds, algorithm/version, or trial count makes the stochastic check
UNVERIFIABLE. Never rerun with new seeds until a preferred result appears.

## Phase 3: Normalize and validate the snapshot

Create an in-memory normalized snapshot keyed by stable IDs. Record every source
path/hash, pointer, original value/unit, normalized value/unit, formula version,
and conversion rule.

Validate before domain analysis:

1. all required sources match their recorded bytes;
2. every variable is typed and in its schema range;
3. units and dimensions are compatible;
4. formula ASTs are acyclic and evaluable;
5. targets/tolerances are authoritative and current;
6. scenarios reference existing typed IDs;
7. no divide-by-zero, NaN, infinity, impossible probability, or empty required
   population exists; and
8. budgets cover every required check.

A provable parse/schema/unit/formula defect becomes a finding with its exact
reproduction. It does not permit a data edit. If the defect prevents a required
metric, coverage is PARTIAL even when the defect itself is proven.

## Phase 4: Run declared domain checks

Run only checks named in the manifest.

### Combat

For declared loadouts/tiers/scenarios, evaluate formula-traced DPS, burst,
cooldown/downtime, mitigation, effective health, TTK, sustain, and resistance
interactions. Dominance requires a defined alternative set and all declared
comparison dimensions; otherwise label the claim UNVERIFIABLE or scenario-local.

### Economy

Evaluate declared faucet/sink graphs, rates/units, starting balances, time
horizons, pricing constraints, conservation rules, accumulation, and cycles.
"Infinite loop" requires a reproducible current scenario and formula trace.
Affordability or desirability conclusions require authoritative target/policy.

### Progression

Evaluate XP, level/power, unlock, and content-gate curves over declared horizons
and strategies. Dead zones and spikes require authoritative thresholds and exact
boundary rules. A difference from a smooth curve is not automatically a defect.

### Loot

Evaluate normalized probability tables, rarity acquisition, pity state machine,
duplicate policy, expected attempts/time, inventory pressure, and declared
stochastic confidence. "Useless" requires a defined utility target, player state,
and comparison set.

For every check, record status `PASS`, `FAIL`, `UNVERIFIABLE`, `NOT_RUN`,
`STALE`, or `ERROR` with exact input IDs, formula/AST, scenario/seed set,
expected/tolerance, actual result, deviation, and evidence trace.

## Phase 5: Emit stable evidence-bound findings

Assign IDs deterministically by domain, source path, pointer/section, formula ID,
scenario ID, and check ID:

`BLC-<analysis-id>-<domain>-<three-digit-sequence>`

On `recheck`, preserve supplied prior finding IDs. New regression findings use
`BLC-<analysis-id>-REG-<three-digit-sequence>`. Never renumber history.

Each finding must contain:

```yaml
id: <stable-id>
class: PROVABLE_ERROR | MODEL_VIOLATION | PRODUCT_DECISION | EVIDENCE_GAP
severity: BLOCKER | HIGH | MEDIUM | LOW | INFO | UNRATED
confidence: PROVEN | HIGH | MEDIUM | LOW
status: OPEN | RESOLVED | STILL_OPEN | UNVERIFIABLE
domain: combat | economy | progression | loot
source_path: <exact project-relative path>
source_sha256: <sha256:...>
source_pointer_or_section: <pointer or stable section ID>
schema_and_formula_ids: [<IDs>]
formula_ast_and_trace: <exact trace or NOT_APPLICABLE>
variables_and_units: <original and normalized>
scenario_and_seed_set: <IDs and seeds>
expected_target_and_tolerance: <values plus source/hash>
actual_and_deviation: <typed values>
reproduction: <bounded deterministic steps>
impact: <evidence-bounded consequence>
owner: <data | design | economy | systems | technical>
acceptance: <observable resolution condition>
limitations: <scope/confidence limits>
```

Severity follows evidence, not rhetorical intensity:

- BLOCKER: a required metric cannot be validly computed, or a required current
  scenario produces a prohibited non-finite/impossible state.
- HIGH: a verified current scenario violates an explicit authoritative hard
  constraint or proves a declared exploit/infinite loop.
- MEDIUM/LOW: only when an authoritative severity/tolerance policy maps the
  measured deviation to that level.
- UNRATED: evidence shows a product choice or gap but no approved severity rule.
- INFO: reproducible non-actionable context.

A missing secondary metric target is an EVIDENCE_GAP/UNRATED finding and
PARTIAL coverage, not an outlier with a model-invented threshold. Absence of the
domain's primary target set remains the Phase 1 ERROR condition.

## Phase 6: Keep correction facts separate from product decisions

### Provable calculation or schema correction

For a PROVABLE_ERROR whose correction is uniquely implied by the declared schema,
unit conversion, or formula, provide an exact `Correction Candidate` containing:

- erroneous source pointer/hash and current typed value/expression;
- governing schema/conversion/formula evidence;
- mathematically implied corrected value/expression;
- downstream metrics that must be recomputed; and
- responsible owner and acceptance condition.

This is evidence, not an edit. The skill remains READ_ONLY and never applies the
candidate.

### Product value or policy decision

TTK targets, pacing, prices, drop rates, pity policy, XP/power curves, difficulty,
reward utility, and acceptable tradeoffs are product decisions unless an
authoritative source already fixes them.

For each PRODUCT_DECISION finding, present exactly two or three mutually exclusive
options. Include for every option:

- proposed target/policy/range, clearly labeled as an option;
- measured effect on every affected declared metric/scenario;
- benefits, costs, risks, affected player strategies, and confidence;
- authoritative artifacts/owners that would need revision; and
- validation evidence needed after the decision.

Include `Recommended Option: NONE — PRODUCT OWNER DECISION REQUIRED`. Do not rank
an option as best, silently select a midpoint, turn the current value into a
default, or ask for permission to edit it.

Route the selected decision to a separate owner:

- schema, unit, or derived-calculation defect -> data/schema owner;
- value inside an already approved tuning range -> balance-data owner;
- target/range, pacing, TTK, loot, price, progression, or core rule -> design
  owner, followed by downstream propagation;
- formula architecture or technical constraint -> technical/ADR owner.

No owner handoff expands this skill's read-only boundary.

## Phase 7: One-pass report and stop

Return this report in conversation:

```markdown
# Balance Check Analysis: <analysis-id>

Artifact Type: balance-check-analysis-report
Schema Version: 1
Mode: analyze | recheck
Analysis ID: <stable-id>
Input Manifest Path/SHA-256: <path> / <sha256:...>
Source Revision: <revision>
Input Snapshot SHA-256: <sha256:...>
Formula/Schema Set SHA-256: <sha256:...>
Scenario Matrix SHA-256: <sha256:...>
Target/Tolerance Set SHA-256: <sha256:...>
Prior Report Path/SHA-256: <path/hash | NONE>
Diff Receipt Path/SHA-256: <path/hash | NONE>
Workflow Status: COMPLETE | PARTIAL | ERROR
Coverage Status: FULL | PARTIAL | NONE
Verdict: PASS | FINDINGS | PARTIAL | ERROR
Mutation Status: READ_ONLY
Persistence: NONE

## Scope and Source Coverage
## Schema, Unit, and Formula Validation
## Scenario and Seed Coverage
## Check Results
## Findings
## Product Decision Options
## Correction Candidates
## Limitations and Unverifiable Claims
## Owner Handoffs
```

Sort sources, checks, scenarios, and findings by their stable IDs. Render numbers
using the manifest precision/rounding policy and exclude wall-clock or ambient
state not declared in the manifest, so identical inputs produce identical bytes.

Show denominator arithmetic: declared sources/checks/scenarios, evaluated,
passed, failed, unverifiable, not-run, stale, and error counts. Include every
source hash and all stable findings. Compute and return the report-bytes SHA-256
outside the report body so there is no self-hash.

After the report, stop. Do not offer Fix, Save, Apply, Update, or automatic
Re-run actions. State that a separate owner may act on a selected option or
correction, after which a new `recheck` invocation may verify exact evidence.

## Phase 8: Bounded recheck

`recheck` requires:

- exact immutable prior report path/hash and matching analysis ID;
- exact change receipt binding before/after source paths, pointers, raw hashes,
  selected product decision or correction authority, owner, and timestamp;
- explicit prior finding IDs; and
- an explicit regression-check set from the prior report.

Reject a diff that changes undeclared sources, scenarios, target meanings, or
formula semantics. Such a change needs a new `analyze` manifest and analysis ID.

Recheck only the selected finding IDs and named regression checks. Preserve all
other prior findings as out-of-scope history; never claim they were reverified.
Re-hash current inputs and run one pass.

Report `RESOLVED` or `STILL_OPEN` per selected ID and any stable regression
findings. If `open_blockers=0`, report that fact and stop. If blockers remain,
report them and stop. Never modify inputs, broaden the recheck, or automatically
start another pass.

## Final response boundary

Every response names exact input paths/hashes, declared scope, coverage,
reproducibility assumptions, stable findings, product options without a selected
winner, report SHA-256, all status axes, and the next external owner.

No director gate applies. No agent, user selection, or missing evidence may turn
PARTIAL into PASS. No absence of newly discovered findings proves convergence
outside the declared scope.
