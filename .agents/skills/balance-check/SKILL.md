---
name: balance-check
description: "Strictly read-only, bounded balance analysis over typed adapter evidence, authoritative targets, normalized units, formula provenance, and reproducible scenario uncertainty."
---

# Balance Check

Analyzer contract: `cgs.balance-check/v2`.
Evidence envelope: `cgs.review-evidence/v1` with extension
`cgs.balance-check-report/v1`.

Evaluate one declared balance snapshot. This analyzer proves calculations,
compares typed metrics with authoritative targets, and reports scenario-bounded
evidence. It does not tune the game, choose product values, edit truth sources,
or claim that the game is globally balanced, healthy, optimal, fair, or fun.

## Invocation and read-only boundary

Invoke exactly one mode:

```text
$balance-check analyze --manifest <project-relative-manifest-path>
$balance-check recheck --manifest <project-relative-manifest-path> --prior-evidence <project-relative-evidence-path> --change-receipt <project-relative-receipt-path> --findings <comma-separated-stable-finding-IDs>
```

Reject missing values, unknown or duplicate flags, duplicate finding IDs, empty
finding lists, positional systems, directories, URLs, globs, regular expressions,
`latest`/`most recent`, absolute paths, dot segments, path escapes, symlinks,
junctions, non-regular files, and ambiguous IDs with
`ERROR — INVALID INVOCATION`. Show the accepted grammar, set verdict `ERROR`,
emit no review-evidence record, and stop. Never infer a system, GDD, data file,
target, prior report, change, or revision from directory contents, Git history,
filenames, modification time, or conversation memory.

Every `--findings` token must exactly match
`BLF-<lowercase-category-slug>-<12-lowercase-hex>` and be comma-separated without
aliases or display names. Schema-defined artifact, system, metric, formula,
scenario, target, and check IDs are matched as exact case-sensitive values.

This workflow is a single-analyzer, strictly read-only contract:

- It may enumerate, hash, parse, and read declared project-local regular files,
  inspect read-only Git state, and run only registered deterministic adapters in
  a project-read-only sandbox.
- It must not create, edit, append, rewrite, tune, import, rename, move, delete,
  stage, commit, publish, approve, or persist data, GDDs, formulas, targets,
  scenarios, schemas, reports, evidence, tests, indexes, registries, or session
  state.
- It must not request write approval, offer Fix/Save/Apply/Update/Re-run actions,
  invoke a director gate, invoke another skill, delegate analysis or remediation,
  or execute a recommendation.
- It performs one pass and stops. `recheck` is a separate future invocation, not
  an in-session fix-and-rerun loop.
- Its only deliverable is one conversation packet. A separately invoked recorder
  may persist the exact bytes, but this analyzer never selects a path or writes.

The verdict vocabulary is exactly `PASS | FINDINGS | PARTIAL | ERROR`:

- `ERROR`: invocation, scope, primary target, or execution is invalid enough that
  no trustworthy balance evidence can be constructed. No evidence envelope is
  emitted.
- `PARTIAL`: useful evidence exists, but any required input, adapter, target,
  unit, formula, scenario, simulation, check, or recheck channel is incomplete,
  stale, unsupported, ambiguous, over limit, or uncertainty-inconclusive.
- `FINDINGS`: coverage is complete and at least one actionable finding is open.
- `PASS`: coverage is complete and no actionable finding is open.

`PARTIAL` takes precedence over otherwise clean or failing subset results. Preserve
known findings, but do not turn them into an exhaustive verdict. `PASS` applies
only to the exact manifest, targets, model, scenarios, seeds, tolerances, and
limitations in the returned packet.

---

## Phase 0 — Resolve instructions and project identity

Read every applicable `AGENTS.md` from repository root through the manifest and
each declared input directory, in root-to-target order. Record canonical path and
raw-byte SHA-256; the closest applicable instruction wins conflicting
instructions.

Represent `project_id` as the exact string
`root=<forward-slash-canonical-root>;git-root=<root-commit-or-null>` and compute
`project_id_sha256` over its UTF-8 bytes. If Git is unavailable, use `null`, keep
working from current exact file hashes, mark project-revision provenance
incomplete, and force `PARTIAL`; never guess a commit.

The manifest must be a project-local regular file no larger than 1 MiB with
schema `cgs.balance-input-manifest/v2`. It must bind one stable analysis ID, one
mode, one target snapshot ID, explicit domains from
`combat | economy | progression | loot`, exact system IDs, numeric model,
precision/rounding/overflow policy, source revision, generated-at timestamp, and
ordered stable-ID tables for sources, adapters, units, variables, formulas,
targets, scenarios, simulations, and required checks.

Any source needed to identify the domain, primary question, exact system IDs,
primary authoritative target, unit registry, or formula grammar that is missing,
ambiguous, malformed, outside the project, or hash-invalid yields `ERROR` before
analysis. A valid identified domain with a secondary missing source/check becomes
`PARTIAL`. Do not search `assets/data`, `design/gdd`, reports, or registries for a
replacement.

---

## Phase 1 — Lock a bounded exact-hash manifest

Build one complete candidate identity sequence from the explicit manifest,
source/adapter/unit registries, target records, formula sources, scenario and
simulation definitions, applicable instructions, and recheck evidence when
present. Hash exact raw bytes with SHA-256 before parsing. Normalized text, Git
status, modification time, report date, and filename are never hash inputs or
currentness evidence.

Use these fixed upper bounds:

```yaml
max_manifest_candidates: 256
max_source_files: 128
max_single_source_bytes: 1048576
max_total_source_bytes: 8388608
max_variables: 10000
max_unit_definitions: 1024
max_conversion_rules: 4096
max_formulas: 4096
max_total_ast_nodes: 65536
max_targets: 4096
max_scenarios: 512
max_required_checks: 4096
max_simulation_definitions: 512
max_trials_per_simulation: 1000000
max_total_trials: 2000000
max_total_model_evaluations: 10000000
max_single_receipt_bytes: 1048576
max_adapter_wall_ms: 30000
max_total_wall_ms: 600000
max_findings: 4096
```

Manifest limits may lower but never raise these caps. Sort candidate identities by
channel, stable artifact ID or null, then canonical project-relative path. Stream
the complete ordered identity sequence into `inventory_sha256`, retaining at most
`max_manifest_candidates` detailed rows. On overflow record exact total and
omitted counts, first and last omitted sort keys, and
`omitted_candidates_sha256`. Apply the same bounded-prefix plus exact count/digest
rule to every row limit. Do not parse, simulate, or judge an omitted item. Add an
aggregate `OVER_LIMIT` coverage row naming every affected check and force
`PARTIAL`; never silently truncate, raise a cap, or infer completeness from a
sample.

Each manifest row contains:

```yaml
channel: instruction | source | schema | adapter | unit | formula | target | scenario | simulation | prior-evidence | change
artifact_id: <stable ID or null>
path: <canonical project-relative path>
sha256: <locked 64-lowercase-hex or null>
revalidation_sha256: <final 64-lowercase-hex or null>
bytes: <integer or null>
status: LOCKED | EXCLUDED | MISSING | UNREADABLE | INVALID | UNSUPPORTED | OVER_LIMIT | SYMLINK_REJECTED | OUTSIDE_PROJECT | STALE
reason: <bounded exact reason>
planned_checks: [<stable check IDs>]
```

`manifest_sha256` is SHA-256 over canonical JSON of project identity, invocation,
contract, snapshot and system/domain IDs, numeric policy, fixed/effective limits,
ordered retained rows, inventory digest, and overflow counts/digests. Canonical
JSON uses UTF-8, lexicographically ordered object keys, displayed array order, no
insignificant whitespace, and one final LF.

Before finalization, re-enumerate declared sources and re-hash every locked input.
An added, removed, renamed, or byte-changed input is `STALE`; discard calculations
derived from old bytes, retain unaffected evidence, mark affected checks
incomplete, and return `PARTIAL`. Never mix snapshots or silently restart.

---

## Phase 2 — Parse inputs through registered typed adapters

Never parse a supported extension by intuition. The manifest's exact
`cgs.balance-adapter-registry/v1` must register each parser/evaluator with:

- stable adapter class, adapter ID, semantic version, executable/tool identity
  and hash, supported input schema/version and MIME signature;
- output schema/version, typed-field mapping, error semantics, deterministic
  normalization, and parser precision policy;
- argv array with typed placeholders, no shell string or network, project-read-only
  mount, bounded scratch, timeout, output cap, and no project mutation; and
- supported project/engine/model version range.

Required classes are present when their channels are in scope:

- structured JSON/YAML/CSV balance-data parser;
- Markdown stable-section/requirement target parser;
- schema and typed-pointer validator;
- unit/dimension registry and conversion parser;
- allowlisted formula parser and typed AST evaluator;
- scenario/simulation definition parser; and
- prior-evidence/change-receipt verifier for `recheck`.

Executables, project scripts, macros, arbitrary code, embedded expressions,
environment files, binary game data, unknown schemas, and unsupported formats do
not enter the model. A valid `cgs.balance-adapter-receipt/v1` binds adapter and
executable IDs/versions/hashes, exact input artifacts and raw hashes, target
snapshot, typed output schema, output digest, argv digest, sandbox policy,
timestamps, exit state, bounded log digests, and parser version.

Adapter state is exactly
`PASS | FAIL | NOT_RUN | UNSUPPORTED | PARSE_ERROR | TIMEOUT | INVALID_RECEIPT`.
An adapter may `PASS` only for current typed output bound to exact source bytes.
A valid `FAIL` proves a declared schema/parser rule violation; it is not the same
as missing/unsupported/parse/timeout evidence. Any non-PASS/non-conclusive state
makes the affected input/check `UNVERIFIABLE`, adapter coverage incomplete, and
forces `PARTIAL`. If project-read-only isolation is unavailable or an adapter
could write/import/cache, do not run it and use `NOT_RUN`. Actual detected project
mutation is `ERROR`, with no evidence envelope.

Build each adapter-derived index once. Do not reread or reparses a source per
variable/check/scenario.

---

## Phase 3 — Normalize authoritative targets, units, and formulas

### Authoritative targets and tolerances

Targets are product truth only when the manifest points to an exact current
approved target record with a stable metric/target ID, owner, lifecycle state,
applicability, source artifact/path/locator/hash, and schema version. Resolve
authority in this order:

1. applicable governing `AGENTS.md` constraints;
2. approved canonical GDD/balance target records for player-facing values,
   pacing, TTK, prices, loot, progression, and policy;
3. approved technical-budget records for technical limits only; and
4. observed telemetry, benchmarks, historical values, prior reports, and manifest
   fallbacks as comparison evidence only, never targets unless an authoritative
   record explicitly promotes them.

One domain cannot silently override another. A missing or conflicting primary
target that prevents the analysis question from being defined is `ERROR`.
Missing, stale, ambiguous, or conflicting secondary targets/tolerances make their
checks `UNVERIFIABLE` and force `PARTIAL`. Never choose the newest, majority,
closest, or most favorable record.

Each target contains:

```yaml
target_id: <stable ID>
metric_id: <stable typed metric ID>
system_id: <stable system ID>
applicability: <typed scenario/state predicate>
expected: <typed value, range, distribution, or invariant>
tolerance:
  kind: ABSOLUTE | RELATIVE | INTERVAL | ONE_SIDED | STATISTICAL
  value: <typed value>
  inclusive_lower: true | false | null
  inclusive_upper: true | false | null
  decision_rule: <stable rule ID>
severity_policy_id: <stable ID>
source: <artifact ID/path/locator/hash/schema/owner/lifecycle>
```

Do not invent ±10%, ±20%, ideal values, genre standards, acceptable confidence,
or a severity scale. A tolerance or severity comes only from authoritative
evidence.

### Typed variables and unit registry

Every variable requires stable variable ID, source artifact/pointer/hash, scalar
or container type, dimension, unit ID, allowed range, null policy, base/final
semantic, version, and scenario mutability. Percent, probability, ratio,
multiplier, frames, seconds, ticks, currency-resource IDs, XP, damage, health,
count, and rates are distinct semantics.

The exact `cgs.balance-unit-registry/v1` defines every unit/dimension and closed
conversion rule with stable conversion ID, source artifact/hash/version, typed
input/output dimensions, exact rational or declared decimal transform, precision,
rounding, domain, and validity range. Do not assume frame/tick rate, convert
percent to multiplier implicitly, merge currencies/resources by label, or combine
incompatible dimensions. Undefined, overflowed, out-of-domain, or dimensionally
invalid values are `UNVERIFIABLE` and force `PARTIAL` when required.

### Formula provenance and typed AST

Every formula uses `cgs.balance-formula/v1`:

```yaml
formula_id: <stable ID>
formula_version: <exact version>
source: <artifact ID/path/locator/hash/schema/owner/lifecycle>
expression: <bounded exact expression>
inputs: [<stable variable ID/type/dimension/unit/base-final semantic>]
output: <stable metric ID/type/dimension/unit/base-final semantic>
ast: <typed operator tree>
rounding_overflow_policy_id: <stable ID>
applicability: <typed predicate>
```

The allowlist is numeric literals, typed variable references, parentheses,
`+`, `-`, `*`, `/`, `min`, `max`, `clamp`, `pow`, comparisons, and declared
piecewise branches. Never execute source text, scripts, macros, arbitrary
functions, dynamic code, or user-authored plugins. Reject missing variables,
unknown functions, cycles, ambiguous base/final stages, invalid dimensions,
division by zero, invalid probability, NaN, infinity, overflow, and unspecified
rounding. Record exact AST, typed intermediate values, conversions, rounding, and
evaluation trace for every calculated metric.

Conflicting current formula records do not become alternatives chosen by the
analyzer. A conflict that prevents the primary metric is `ERROR`; otherwise it is
a formula coverage gap and `PARTIAL`.

---

## Phase 4 — Freeze bounded scenarios, simulations, and uncertainty

Every scenario contains stable scenario ID, domain/system IDs, target snapshot,
power/content tier, time horizon, start state, player strategy/policy, loadout,
difficulty, relevant system state, exact typed overrides, required metrics/checks,
and deterministic or stochastic classification. Conclusions apply only to this
declared matrix.

Every stochastic simulation uses `cgs.balance-simulation/v1` and declares:

- simulation/model ID and version, scenario ID, formula and variable IDs;
- exact PRNG algorithm/version, ordered seed set, trial count, sampling method,
  warm-up/burn-in if applicable, and state reset policy;
- estimator, confidence method/level, uncertainty decision rule, multiple-test
  correction when required, and stopping rule;
- expected distribution/invariant and authoritative tolerance/precision target;
- maximum model evaluations and receipt/output bounds.

Prefer an exact closed-form result when the declared model and target permit it.
Otherwise execute exactly the declared seeds/trials once, in deterministic order,
within fixed caps. Never add seeds, extend trials, change confidence methods,
discard outliers, or rerun until a preferred result appears.

A valid `cgs.balance-simulation-receipt/v1` binds exact manifest/source/formula/
target/scenario hashes, simulator/PRNG/model versions, seeds, trial/evaluation
counts, distribution summary, estimator, confidence interval or error bound,
decision rule result, convergence diagnostics, and complete output digest.

Missing seeds, PRNG/model version, target precision, decision rule, sufficient
trials, or valid receipt makes the check `UNVERIFIABLE`. When the interval/error
bound overlaps a decision boundary or declared precision is not achieved, record
`INCONCLUSIVE_UNCERTAINTY` and force `PARTIAL`; do not round uncertainty into a
PASS/FAIL. Report assumptions, sample size, confidence interval, Monte Carlo
error, and limits. Deterministic identical inputs must produce identical receipts,
checks, findings, and payload hash except explicitly excluded observation time.

Claims such as dominant, unkillable, useless, infinite, dead zone, power spike,
or healthy economy are invalid without defined alternatives, time windows,
strategies, states, targets, and uncertainty decision rules.

---

## Phase 5 — Validate the snapshot and run declared domain checks

Build one in-memory normalized snapshot keyed by stable IDs. Record original and
normalized values/units, conversion IDs, formula/target/scenario versions, source
locators/hashes, adapter receipts, and evaluation traces. Validate all required
sources, schemas, types, ranges, units, formula DAGs, targets, scenarios, budgets,
and finite arithmetic before interpreting balance.

Run only manifest-declared checks:

- `combat`: formula-traced damage, DPS/burst, cooldown/downtime, mitigation,
  effective health, TTK, sustain, resistance, declared alternatives and states;
- `economy`: typed faucet/sink graph, resource IDs, rates, starting balances,
  horizons, prices, conservation/invariants, accumulation, and reproducible cycles;
- `progression`: XP/level/power/unlock/content-gate curves over declared horizons,
  states, strategies, thresholds, and boundary rules; and
- `loot`: normalized probability/pity state machine, duplicate policy, rarity
  acquisition, attempts/time, inventory pressure, utility target, and declared
  stochastic confidence.

Each check state is exactly
`PASS | FAIL | UNVERIFIABLE | NOT_RUN | STALE | ERROR`. A `FAIL` requires complete
current typed evidence and a violated authoritative target/tolerance decision
rule. `NOT_APPLICABLE` is not a check state; exclude a check only when the manifest
contains an authoritative typed applicability predicate that evaluates false,
and represent that exclusion in coverage. A schema/unit/formula error may be a
proven finding while still forcing `PARTIAL` if it blocks another required check.

Each result records stable check/metric IDs, typed input IDs, formula AST/trace,
scenario/seed/simulation receipt, authoritative expected/tolerance/severity
sources, actual value/distribution, typed deviation, uncertainty, owner, and exact
evidence references.

---

## Phase 6 — Emit stable findings and preserve product decisions

Every finding uses:

```yaml
id: BLF-<category-slug>-<first-12-fingerprint-hex>
fingerprint_sha256: <64-lowercase-hex>
category: SCHEMA_ERROR | UNIT_ERROR | FORMULA_ERROR | TARGET_VIOLATION | MODEL_VIOLATION | PRODUCT_DECISION | EVIDENCE_GAP | SIMULATION_UNCERTAINTY | REGRESSION
class: PROVABLE_ERROR | MODEL_VIOLATION | PRODUCT_DECISION | EVIDENCE_GAP
severity: BLOCKER | HIGH | MEDIUM | LOW | INFO | UNRATED
confidence: PROVEN | HIGH | MEDIUM | LOW | UNRATED
status: OPEN | RESOLVED_IN_CURRENT | STILL_OPEN | UNVERIFIABLE
domain: combat | economy | progression | loot
system_id: <stable ID>
metric_id: <stable ID or null>
check_id: <stable ID>
formula_ids: [<stable IDs>]
scenario_ids: [<stable IDs>]
target_ids: [<stable IDs>]
evidence: [<exact artifact/locator/hash/receipt references>]
expected_actual_deviation_uncertainty: <typed bounded values>
reproduction: <bounded deterministic steps>
impact: <evidence-bounded consequence>
owner: <stable data/design/economy/systems/technical owner>
acceptance: <objective current-snapshot closure condition>
limitations: <scope/confidence limits>
```

Fingerprint canonical JSON from `project_id_sha256`, category, stable domain/
system/metric/check/formula/scenario/target IDs, and stable evidence artifact IDs.
Exclude paths, pointers, raw wording, hashes, current values, deviation, severity,
confidence, status, owner, run ID, timestamps, and recommendation. Thus a moved
source or changed value keeps the same logical finding ID; a different target,
scenario, formula, or check does not. Deduplicate only the complete fingerprint.
Incompatible identity/evidence under one fingerprint is a coverage conflict and
forces `PARTIAL`.

Severity follows authoritative constraints, tolerance/severity policy, and proven
impact, never rhetorical language or deviation magnitude alone:

- `BLOCKER`: a required metric cannot be validly computed, or a required current
  scenario proves a prohibited non-finite/impossible state;
- `HIGH`: a current scenario violates an explicit authoritative hard constraint
  or proves a declared exploit/infinite loop;
- `MEDIUM`/`LOW`: only through an exact authoritative severity mapping;
- `UNRATED`: product choice or evidence gap without approved severity; and
- `INFO`: reproducible non-actionable context.

For a `PROVABLE_ERROR` whose correction is uniquely implied by current schema,
unit conversion, or formula evidence, provide one read-only correction candidate
with current pointer/hash, governing proof, mathematically implied value/expression,
downstream recomputation set, owner, and acceptance. Never apply it.

TTK targets, pacing, prices, drop rates, pity policy, XP/power curves, difficulty,
reward utility, acceptable risk, and tradeoffs remain product decisions unless an
approved source already fixes them. For each `PRODUCT_DECISION`, present exactly
two or three mutually exclusive options with measured effects, benefits, costs,
risks, affected strategies, confidence, owner/artifacts, and validation needs.
State `Recommended Option: NONE — PRODUCT OWNER DECISION REQUIRED`. Never rank,
select, average, or apply an option.

---

## Phase 7 — Build coverage and apply the verdict mechanically

Record one row for every candidate, source, adapter, target, unit, formula,
scenario, simulation, required check, and recheck input:

```yaml
channel_id: <stable artifact/channel/check ID>
artifact_id: <stable ID or null>
path: <canonical project-relative path or null>
sha256: <hash or null>
bytes: <integer or null>
status: COMPLETE | PARTIAL | FAILED | NOT_APPLICABLE
checks:
  SNAPSHOT: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  INPUTS: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  ADAPTERS: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  TARGETS: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  UNITS: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  FORMULAS: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  SCENARIOS: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  SIMULATIONS: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  DOMAIN_CHECKS: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  RECHECK: DONE | PARTIAL | FAILED | NOT_APPLICABLE
limitation: <none or exact bounded reason>
```

Apply this exact precedence:

1. Invalid invocation/manifest/scope/primary target/unsafe formula grammar,
   actual mutation, no usable declared domain, no trustworthy normalized
   snapshot, or failed evidence construction: verdict `ERROR`, coverage `NONE`,
   no evidence record.
2. Any required coverage channel/check is incomplete, unavailable, stale,
   unsupported, invalid, over limit, `UNVERIFIABLE`, `NOT_RUN`, adapter-failed,
   target/unit/formula-conflicted, or uncertainty-inconclusive: verdict `PARTIAL`,
   coverage `PARTIAL`.
3. Complete coverage with at least one actionable `OPEN` or `STILL_OPEN` finding:
   verdict `FINDINGS`, coverage `FULL`.
4. Complete coverage with no actionable finding: verdict `PASS`, coverage `FULL`.

Workflow status is `ERROR` for `ERROR`, `PARTIAL` for `PARTIAL`, and `COMPLETE`
for `FINDINGS` or `PASS`. Mutation status is always `READ_ONLY`; persistence is
always `NONE`. No role, user selection, clean subset, missing evidence, or absence
of newly discovered findings may upgrade `PARTIAL` to `PASS`.

---

## Phase 8 — Return one hash-bound balance evidence packet

Return one machine payload followed by a concise human projection:

```yaml
schema: cgs.balance-check-report/v1
contract: cgs.balance-check/v2
result: OK
verdict: PASS | FINDINGS | PARTIAL
workflow_status: COMPLETE | PARTIAL
coverage_status: FULL | PARTIAL
mutation_status: READ_ONLY
persistence: NONE
project_id: <canonical project identity>
project_id_sha256: <hash>
mode: analyze | recheck
analysis_id: <stable ID>
target_snapshot_id: <stable ID>
domains: [<sorted closed-enum values>]
systems: [<sorted stable IDs>]
manifest:
  sha256: <manifest hash>
  inventory_sha256: <complete candidate identity digest>
  limits: <fixed and effective limits>
  overflow: <exact counts, boundary keys, and omitted-sequence digests>
  rows: [<ordered detailed rows>]
numeric_policy: <model/precision/rounding/overflow IDs and evidence>
adapter_receipts: [<ordered validated receipt summaries>]
targets: [<ordered authoritative target/tolerance records>]
units: [<ordered variables/conversions/normalized values>]
formulas: [<ordered typed ASTs and traces>]
scenarios: [<ordered assumptions and coverage>]
simulations: [<ordered receipt summaries and uncertainty>]
checks: [<ordered results>]
findings: [<ordered stable findings>]
product_options: [<unranked option sets>]
correction_candidates: [<read-only uniquely proven candidates>]
coverage:
  dimensions: <status/reason per required channel>
  ledger: [<ordered rows>]
counts: <declared/evaluated/pass/fail/unverifiable/not-run/stale/error reconciliation>
prior_evidence: <validated identity/hash or null>
change_receipt: <validated identity/hash or null>
limitations: []
recommendation: <one owner-specific action or none>
disclaimer: <required boundary text>
```

Sort sources and adapters by stable artifact ID, targets/units/formulas/scenarios/
simulations/checks/findings by their stable IDs, and options by finding then
option ID. Render typed numbers through the declared numeric policy. Do not place
run identity, wall-clock duration, ambient environment, or observation time in
the deterministic analysis payload. Run identity and observation time appear only
in the outer envelope. Identical inputs and adapter/simulation receipts must
produce identical deterministic payload bytes and finding IDs.

Hash canonical deterministic extension JSON using Phase 1 canonicalization and
wrap it in:

```yaml
schema: cgs.review-evidence/v1
record_id: sha256:<SHA-256 of canonical envelope payload excluding record_id>
artifact_id: balance-check:<project_id_sha256>:<analysis_id>:<manifest_sha256>
artifacts: [<every retained locked input path and SHA-256, sorted as manifest>]
reviewer: <stable task identity or codex-task:<run_id>>
review_run_id: <run_id>
review_depth: bounded-full
independence: analyzer-read-only
verdict: <PASS | FINDINGS | PARTIAL>
timestamp: <UTC ISO-8601>
finding_ids: [<sorted stable finding IDs>]
unresolved_blocker_ids: [<sorted OPEN/STILL_OPEN BLOCKER and coverage IDs>]
report_payload_sha256: <SHA-256 of canonical deterministic extension payload>
producer:
  tool: balance-check
  version: cgs.balance-check/v2
extension: <complete cgs.balance-check-report/v1 payload>
```

The outer run ID and timestamp supply execution provenance without changing
same-input analysis identity. Canonicalize the envelope without `record_id`, then
recompute every artifact, manifest, payload, and record hash once. Return
`ERROR — EVIDENCE CONSTRUCTION FAILED` without an evidence record rather than
emit inconsistent evidence.

The disclaimer states that `PASS` is limited to the exact declared model and is
not a global balance/fun claim; `PARTIAL` is not evidence of balance; stochastic
claims apply only to declared assumptions/confidence; product values were not
selected; and no project state was changed.

---

## Phase 9 — Perform one bounded recheck

`recheck` requires a current manifest plus one immutable prior
`cgs.review-evidence/v1` record produced by `balance-check` with recognized
`cgs.balance-check-report/v1` extension, and one
`cgs.balance-change-receipt/v1`. Recompute the prior record, payload, artifact,
manifest, project, analysis, target, formula, unit, scenario, and finding hashes.

The change receipt binds exact before/after artifact IDs, canonical paths, raw
hashes, pointers, selected product decision or correction authority, owner,
timestamp, and affected stable target/unit/formula/scenario/check IDs. Reject a
receipt that changes undeclared sources, expands domain/scope, or alters target,
formula, unit, scenario, or model meaning beyond the selected findings. Such work
requires a new `analyze` manifest and analysis ID.

Re-evaluate only selected finding IDs and explicit regression checks from the
prior packet. Preserve every selected ID. Mark it `RESOLVED_IN_CURRENT` only when
its recorded acceptance is proven by current exact-hash evidence; otherwise
`STILL_OPEN` or `UNVERIFIABLE`. Preserve unselected prior findings as
out-of-scope history, never as reverified. New regressions receive ordinary stable
`BLF-REGRESSION-*` fingerprints from their exact logical identities.

Run once. Report `open_blockers` and stop whether zero or nonzero. Never broaden
the recheck, modify inputs, apply an option/correction, or start another pass.

---

## Phase 10 — Return one owner-routed recommendation and stop

Return at most one next action from the highest-impact open evidence:

- uniquely proven schema/unit/derived-calculation defect: data/schema owner;
- approved value within an existing tuning range: balance-data owner;
- target/range, pacing, TTK, loot, price, progression, difficulty, or product
  policy: design/economy/systems owner for an explicit user decision, followed by
  separate downstream propagation;
- formula architecture, precision, overflow, or technical constraint:
  technical/ADR owner;
- missing adapter/simulation evidence: adapter/model owner; or
- no finding with complete coverage: no follow-up required.

Do not invoke the owner. Stop after returning the packet and recommendation.
Never persist the report, change a value, update the catalog, or automatically
re-run.
