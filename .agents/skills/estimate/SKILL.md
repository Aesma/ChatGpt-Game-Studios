---
name: estimate
description: "Read-only, bounded relative or calibrated estimation evidence with exact scope identity, comparable-history provenance, explicit units and uncertainty, and owner-held decisions."
---

# Estimate

Analyzer contract: `cgs.estimate/v2`.
Evidence envelope: `cgs.review-evidence/v1` with extension
`cgs.estimate-report/v1`.

Estimate one explicitly bound delivery scope. Relative evidence describes
dimensionless complexity. Calibrated evidence may describe effort distributions
only from comparable completed history. Schedule ranges additionally require
current capacity, calendar, dependency, parallelism, and wait evidence. None of
these outputs selects scope, staffing, budget, deadline, or product tradeoffs.

## Invocation: delivery profile and estimate basis

Invoke one exact delivery profile and one exact basis:

```text
$estimate story --basis relative --input <project-relative-story-path> [--evidence <project-relative-evidence-manifest>]
$estimate story --basis calibrated --input <project-relative-story-path> --history <project-relative-history-manifest> [--capacity <project-relative-capacity-receipt>] [--evidence <project-relative-evidence-manifest>]
$estimate sprint --basis relative --input <project-relative-sprint-path> [--evidence <project-relative-evidence-manifest>]
$estimate sprint --basis calibrated --input <project-relative-sprint-path> --history <project-relative-history-manifest> [--capacity <project-relative-capacity-receipt>] [--evidence <project-relative-evidence-manifest>]
$estimate freeform --basis relative --description <text> --scope-id <stable-id> --baseline-sha256 <64-lowercase-hex> --current-sha256 <64-lowercase-hex> [--evidence <project-relative-evidence-manifest>]
$estimate freeform --basis calibrated --description <text> --scope-id <stable-id> --baseline-sha256 <64-lowercase-hex> --current-sha256 <64-lowercase-hex> --history <project-relative-history-manifest> [--capacity <project-relative-capacity-receipt>] [--evidence <project-relative-evidence-manifest>]
```

`story`, `sprint`, and `freeform` are delivery profiles. `relative` and
`calibrated` are estimate bases, not interchangeable result labels. Relative
basis never consumes history or capacity and never emits numeric time.
Calibrated basis requires history; capacity is optional and can add a schedule
range only when every schedule gate passes.

No profile or basis is inferred. Reject missing values, unknown or duplicate
flags, mixed profiles/bases, extra root inputs, history/capacity under relative
basis, capacity without history, empty descriptions, descriptions over 16 KiB,
directories, URLs, globs, regular expressions, `latest`/`most recent`, absolute
paths, dot segments, path escapes, symlinks, junctions, non-regular files, and
ambiguous IDs. Missing required arguments returns `INPUT REQUIRED`; invalid,
unsafe, conflicting, or unreadable arguments return `ERROR`. Neither result emits
estimate evidence.

Never search by title, infer a story/sprint, scan recent work, or select a history,
capacity, baseline, current scope, or evidence file from directory contents, Git,
modification time, or conversation memory.

## Strict read-only and decision boundary

This is a single-analyzer, strictly read-only workflow:

- It may enumerate, hash, parse, and read explicit project-local regular files
  and inspect read-only Git state.
- It must not create, edit, append, re-baseline, split, merge, include, exclude,
  schedule, assign, stage, commit, publish, approve, or persist any file, scope,
  sprint, estimate, budget, staffing plan, calendar, date, decision, or Git state.
- It must not request write approval, invoke a gate, delegate estimation,
  remediation, or owner decisions, invoke another skill, or start a follow-up.
- It performs one pass and stops. A later run is a new invocation against new
  immutable bindings, never an automatic refinement loop.
- It returns one conversation packet. A separately invoked recorder may persist
  the exact returned bytes, but this analyzer never selects a destination or
  writes.

The user or designated producer owns scope inclusion/cuts, staffing, budget,
schedule, target dates, risk appetite, and tradeoffs. ADR/product/dependency
owners resolve their authoritative decisions. An estimate, confidence label,
capacity conflict, or conversational approval is not decision authority.

## Canonical result vocabulary

Return exactly one:

- `ERROR`: invalid, unsafe, ambiguous, conflicting, or unreadable invocation/root
  input;
- `INPUT REQUIRED`: a required invocation argument is absent;
- `NOT ESTIMABLE`: scope is bound, but a required product, architecture,
  dependency, acceptance, or completeness decision blocks delivery estimation;
- `PARTIAL ESTIMATE`: useful relative evidence exists, but requested or required
  context/history/capacity/aggregation evidence is incomplete, stale,
  unsupported, over limit, or uncertainty-inconclusive;
- `RELATIVE ESTIMATE`: relative basis completed with a bound factor vector and
  dimensionless band/range only;
- `CALIBRATED EFFORT ESTIMATE`: calibrated history gates pass and effort
  P50/P80/P90 ranges are available, but no complete schedule channel is claimed;
- `CALIBRATED SCHEDULE RANGE`: calibrated effort plus capacity/calendar/DAG/
  wait/parallelism gates pass and elapsed ranges are available.

`ERROR` and `INPUT REQUIRED` emit no evidence record. `NOT ESTIMABLE` and
`PARTIAL ESTIMATE` may return hash-bound non-consumable analysis evidence when a
scope manifest was locked. Only the three complete estimate results may emit an
estimate record eligible for downstream scope evidence, and relative-only
evidence never verifies numeric effort.

---

## Phase 0 — Resolve instructions, project identity, and scope bindings

Read every applicable `AGENTS.md` from repository root through each explicit
input and first-level linked artifact, in root-to-target order. Record canonical
path and raw-byte SHA-256; the nearest applicable instruction wins conflicts.

Represent `project_id` as
`root=<forward-slash-canonical-root>;git-root=<root-commit-or-null>` and compute
`project_id_sha256` over its UTF-8 bytes. If Git is unavailable, use `null`,
continue from exact current hashes, record project-revision provenance as
incomplete, and prevent a complete consumable result; never guess a commit.

Each estimate unit uses `cgs.estimate-scope-binding/v1`:

```yaml
scope_binding_id: <stable ID>
scope_id: <stable Scope ID>
parent_scope_id: <stable epic/sprint/milestone ID or null>
baseline_sha256: <approved immutable baseline hash>
current_scope_sha256: <current scope-manifest hash>
input:
  artifact_id: <stable story/sprint/freeform ID>
  path: <canonical project-relative path or FREEFORM>
  sha256: <exact raw or normalized-description hash>
profile: story | sprint | freeform
work_type:
  taxonomy_id: <stable ID>
  taxonomy_version: <exact version>
  type_id: <stable work-type ID>
completeness: COMPLETE | INCOMPLETE | CONFLICTING
source: <artifact ID/path/locator/hash/schema/owner>
```

For `story`, read the binding from the exact story or one exact direct binding
reference. For `sprint`, every included story row supplies path/hash/binding and
inclusion state; no story is inferred. For `freeform`, normalize description as
UTF-8 Unicode NFC, LF line endings, no trailing line whitespace, and exactly one
final LF, then hash those bytes. The provided Scope ID and baseline/current
hashes remain mandatory; a description without a testable delivery boundary is
`NOT ESTIMABLE`.

A missing/conflicting Scope ID, baseline/current/input hash, taxonomy, profile,
or completeness state produces an `UNBOUND` analysis and no consumable estimate
record. Never repair bindings or invent a baseline.

---

## Phase 1 — Lock bounded context and source provenance

Read only the root input, applicable instruction chain, its exact first-level
story/ADR/dependency/interface/test links, and explicit history/capacity/evidence
manifests. Do not scan all GDDs, code, Git history, TODOs, sprint directories, or
reports for similarity or missing work.

Use fixed limits:

```yaml
max_sprint_stories: 30
max_context_candidates: 128
max_linked_artifacts: 64
max_single_artifact_bytes: 524288
max_total_context_bytes: 4194304
max_history_samples: 512
max_dependency_nodes: 256
max_dependency_edges: 1024
max_schedule_scenarios: 256
max_assumptions: 256
max_unknowns: 256
max_findings: 1024
```

An explicit input may lower but never raise these caps. Build the complete
candidate identity sequence, sorted by channel, stable artifact ID or null, then
canonical path. Stream it into `inventory_sha256`, retaining at most
`max_context_candidates` detailed rows. On overflow record exact total/omitted
counts, first/last omitted sort keys, and `omitted_candidates_sha256`. Use the
same bounded-prefix plus count/digest rule for other row limits.

If a required root, scope binding, sprint story set, or blocking first-level link
exceeds a cap, return `NOT ESTIMABLE`. If optional evidence, history, capacity,
or schedule context exceeds a cap, preserve relative evidence, add one aggregate
`OVER_LIMIT` coverage row naming affected channels, suppress numeric effort/
elapsed output, and return `PARTIAL ESTIMATE`. Never estimate from a silently
truncated sample or context subset.

Each detailed row contains:

```yaml
channel: instruction | root | scope-binding | story | adr | dependency | interface | test | evidence | history | capacity | calendar
artifact_id: <stable ID or null>
scope_ids: [<sorted stable IDs>]
path: <canonical project-relative path>
sha256: <locked 64-lowercase-hex or null>
revalidation_sha256: <final 64-lowercase-hex or null>
bytes: <integer or null>
status: LOCKED | EXCLUDED | MISSING | UNREADABLE | INVALID | OVER_LIMIT | SYMLINK_REJECTED | OUTSIDE_PROJECT | STALE
reason: <bounded exact reason>
```

`context_manifest_sha256` hashes canonical JSON of project identity, invocation,
profile/basis, scope bindings, model/policy IDs, fixed/effective limits, ordered
retained rows, inventory digest, and overflow counts/digests. Canonical JSON is
UTF-8 with lexicographically ordered object keys, displayed array order, no
insignificant whitespace, and one final LF.

An optional `cgs.estimate-evidence-manifest/v1` is an exact path/hash allowlist.
It separates confirmed affected modules/files/interfaces from tentative
candidates and records purpose, covered Scope IDs, owner, validity, explicit
unknowns, and hash for each item. Only exact bound evidence is confirmed.
Predicted files, integrations, or dependencies are tentative risks and never
counted facts; file/code counts alone do not set size or effort.

Before finalizing, re-enumerate explicit inputs and re-hash every consumed
artifact. Added, removed, renamed, or byte-changed input is `STALE`; discard
derived estimates and return
`NOT ESTIMABLE — INPUT CHANGED DURING ESTIMATE` with non-consumable diagnostic
evidence. Never mix snapshots or silently restart.

---

## Phase 2 — Compute deterministic relative evidence first

Use versioned model `cgs.estimate-relative/v2`. Evaluate each estimate unit
independently on five evidence axes. Select only levels supported by exact bound
evidence; an unresolved axis is `UNKNOWN` with minimum/maximum plausible levels,
not a guessed point.

| Axis | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Delivery breadth | Local configuration/content | One bounded implementation unit | Multiple units in one system | Multiple systems or engine/platform boundary |
| Novelty | Existing owner-proven pattern | Minor adaptation | New local pattern or material discovery | New architecture/technology decision required |
| Integration | No runtime integration | One stable interface | Multiple interfaces/service coordination | Cross-platform/network/external-service boundary |
| Validation | Existing coverage unchanged | One bounded test layer | Multiple layers or performance validation | Certification/security/migration/large matrix |
| Data/release | No persistent/release effect | Reversible config/content | Compatible migration/release coordination | Save/schema migration, irreversible data, or multi-platform rollout |

Sum resolved levels into a score; unknown axes produce a score interval. Map only
to dimensionless bands:

```text
0–3 S
4–7 M
8–11 L
12–15 XL
```

A crossing interval becomes a band range such as `M–L`. These are neither hours,
days, dates, story points, budget, nor an additive sprint measure. History and
capacity never alter the factor vector.

Separate confirmed and tentative scope per axis. Record evidence artifact/locator/
hash, supported level/range, rationale, and limitation for every axis. Tentative
affected files may widen an axis range only when the model rule explicitly maps
the unresolved integration/breadth risk; their count never directly raises a
score.

### Readiness and relative uncertainty

Evaluate stable readiness IDs for requirements, architecture, dependencies, and
validation:

- `READY`: exact current acceptance/interface/owner evidence is complete;
- `PARTIAL`: known bounded work remains but no owner decision blocks delivery;
- `UNKNOWN`: required evidence is unavailable or ambiguous; and
- `BLOCKED`: a required product, ADR/architecture, platform/migration, dependency,
  or acceptance decision is unresolved.

Any `BLOCKED` required field or invalid scope completeness yields
`NOT ESTIMABLE` for delivery. Identify the decision ID, owner, evidence, and
acceptance needed. A discovery question may be described but not estimated unless
it has a separate Scope ID and explicit invocation.

Relative confidence is deterministic and not a probability of delivery:

- `LOW`: at least one readiness field is `UNKNOWN` and none is `BLOCKED`;
- `MEDIUM`: every field is known and at least one is `PARTIAL`, or the score spans
  multiple bands; and
- `HIGH`: all fields are `READY`, all hashes match, and one band resolves.

Never convert confidence into contingency percentage or hidden time padding.

---

## Phase 3 — Validate history identity, units, and sample quality

Calibrated basis requires one immutable `cgs.estimate-history/v2` manifest, one
`cgs.estimate-calibration-policy/v1`, and one
`cgs.estimate-unit-registry/v1`, each with exact artifact ID/path/hash/schema/
version/owner. History is never discovered from arbitrary prior sprints.

Every historical sample contains:

```yaml
sample_id: <stable ID>
scope_id: <stable completed Scope ID>
profile: story | sprint | freeform
work_type: <taxonomy ID/version/type ID>
team_id: <stable team ID>
delivery_conditions: <versioned typed condition vector>
model_id: cgs.estimate-relative/v2
factor_vector: <five resolved axes>
relative_score: <integer 0..15>
actual_effort:
  value: <non-negative typed value>
  unit_id: <stable effort unit ID>
  resolution: <source measurement precision>
blocked_effort: <typed separate value>
external_wait: <typed separate elapsed value>
completion: <artifact ID/path/locator/hash/status>
source_bindings: <baseline/current/input IDs and hashes>
anomaly: <NONE or stable flag plus disposition evidence>
```

The unit registry distinguishes person effort from elapsed/calendar units and
defines exact conversions, precision, rounding, and validity. Never mix effort
and elapsed units, infer working-day length, convert points to days, or treat
blocked/wait elapsed time as productive effort.

Filter samples deterministically. Include only completed samples whose same exact team,
profile, work-type taxonomy/type, model version, effort unit, delivery-condition
compatibility, scope/completion bindings, and factor support meet the exact
calibration policy. Every sample receives exactly one state:

```text
INCLUDED | EXCLUDED_TEAM | EXCLUDED_PROFILE | EXCLUDED_WORK_TYPE |
EXCLUDED_MODEL | EXCLUDED_UNIT | EXCLUDED_CONDITIONS |
EXCLUDED_INCOMPLETE | EXCLUDED_CENSORED | EXCLUDED_ANOMALY |
EXCLUDED_OUT_OF_SUPPORT | EXCLUDED_INVALID
```

List included and excluded IDs with evidence-bound reasons. Do not use cross-team
velocity, global averages, title/text similarity, arbitrary recency, or silently
delete outliers. Anomaly handling must be policy-defined and preserve the sample
and disposition evidence.

The calibration policy, not this skill, defines minimum included count, score/
factor support, extrapolation rule, allowed dispersion metrics/limits, quantile
method, resampling seed/method if any, measurement resolution, significant-digit
rule, and confidence classification. Validate the policy version and show every
gate. Missing/unsupported policy, insufficient samples, poor quality, excess
variance, mixed units, extrapolation, or unresolved anomaly makes calibration
`UNAVAILABLE`, suppresses numeric effort, preserves relative evidence, and returns
`PARTIAL ESTIMATE` for calibrated basis. Never substitute `1 point = 1 day` or
another conservative default.

---

## Phase 4 — Compute calibrated effort without false precision

Only when every calibration gate passes, apply the exact registered model and
policy to the included samples. Record all formulas, ordered inputs, selected
samples, intermediate statistics, dispersion, support diagnostics, and rounding.
Use only deterministic empirical quantiles or an explicitly seeded/versioned
resampling method allowed by policy.

Return effort as P50/P80/P90 ranges in one stable effort unit. A quantile is not
an optimistic/expected/pessimistic promise, delivery probability, budget, or date.
Do not display more significant digits than source resolution and model
uncertainty support. Show unrounded calculations, rounded ranges, measurement
resolution, sample count, effective support, dispersion, and calibration
confidence separately.

When multiple mathematically valid models/policies exist and no authoritative
selection binds one, calibration is `UNAVAILABLE`; do not choose the most precise
or favorable. Relative evidence remains unchanged.

For `sprint`, estimate every story independently. Relative bands are never summed.
Aggregate numeric effort only when every included story has compatible calibrated
distributions in the same model/unit and a current
`cgs.estimate-aggregation-policy/v1` binds dependency/correlation assumptions,
deterministic scenario set and seeds, applicability, and output method. Never add
per-story P50/P80/P90 columns and relabel them sprint quantiles. If any story or
aggregation gate fails, sprint effort is `UNVERIFIED` and calibrated basis returns
`PARTIAL ESTIMATE` with per-story relative evidence.

---

## Phase 5 — Keep effort, capacity, wait, and elapsed ranges separate

Numeric effort never becomes elapsed duration by dividing by headcount. A
schedule channel requires current `cgs.estimate-capacity/v1` evidence binding:

- exact team ID and matching effort unit;
- effective capacity by working day and stable capacity-policy ID;
- availability intervals, working calendar, holidays and time zone;
- WIP and parallel-lane constraints;
- reviewer, service, vendor, and external dependency availability/wait ranges;
- validity interval, owner, source artifact/path/hash/schema; and
- no staffing/budget assumption added by the analyzer.

It also requires a complete acyclic dependency DAG with stable package/predecessor
IDs, parallelizability, resource/owner constraints, exact wait distributions or
ranges, and a versioned `cgs.estimate-schedule-policy/v1`. Reject cycles. Apply the
policy deterministically to P50/P80/P90 effort scenarios and report effort,
productive capacity, external wait, parallel branches, WIP, critical path,
elapsed working-time range, and calendar-date range in separate fields.

Missing capacity is not an error and leaves a valid calibrated effort result.
However, a supplied capacity/calendar/DAG/policy record that is stale, mismatched,
incomplete, unsupported, over limit, or uncertainty-inconclusive returns
`PARTIAL ESTIMATE`, preserving calibrated effort evidence but suppressing a
schedule claim. Never assume a start date, perfect parallelism, constant
availability, generic workday length, or date commitment.

A capacity conflict is evidence for the user/producer. The analyzer must not cut,
keep, defer, remove, add, reorder, staff, split, re-baseline, or promise work.

---

## Phase 6 — Normalize stable findings and coverage

Every blocker, evidence gap, or calibration/schedule limitation uses:

```yaml
id: ESF-<category-slug>-<first-12-fingerprint-hex>
fingerprint_sha256: <64-lowercase-hex>
category: INPUT_GAP | SCOPE_CONFLICT | BLOCKED_DECISION | CONTEXT_OVERFLOW | HISTORY_EXCLUSION | CALIBRATION_GAP | UNIT_GAP | AGGREGATION_GAP | CAPACITY_GAP | DEPENDENCY_GAP | STALE_INPUT
profile: story | sprint | freeform
basis: relative | calibrated
scope_ids: [<sorted stable IDs>]
field_or_policy_id: <stable ID>
status: OPEN | RESOLVED_IN_CURRENT
evidence: [<complete artifact/locator/hash references>]
impact: <bounded consequence for estimate eligibility>
owner: <stable user/producer/data/design/architecture/team owner>
acceptance: <objective current-input closure condition>
```

Fingerprint canonical JSON from `project_id_sha256`, category, profile/basis,
sorted stable Scope IDs, field/policy ID, and stable source artifact IDs. Exclude
paths, hashes, titles, descriptions, raw values, size/confidence/result labels,
owner, status, timestamps, run identity, and recommendation. The same logical gap
keeps its ID after path/wording/value changes; a different scope/policy/field does
not. Deduplicate only the full fingerprint; incompatible evidence under one
fingerprint is a scope/evidence conflict and prevents a complete result.

Record one coverage row for every instruction, root, scope binding, first-level
link, history sample, unit/model/policy, capacity/calendar, dependency node/edge,
and required calculation:

```yaml
channel_id: <stable artifact/channel/check ID>
artifact_or_scope_id: <stable ID or null>
path: <canonical project-relative path or null>
sha256: <hash or null>
bytes: <integer or null>
status: COMPLETE | PARTIAL | FAILED | NOT_APPLICABLE
checks:
  SNAPSHOT: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  SCOPE_BINDING: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  CONTEXT: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  READINESS: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  RELATIVE_MODEL: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  HISTORY: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  UNITS: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  CALIBRATION: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  AGGREGATION: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  CAPACITY: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  SCHEDULE: DONE | PARTIAL | FAILED | NOT_APPLICABLE
limitation: <none or exact bounded reason>
```

Relative basis makes history/calibration/capacity/schedule `NOT_APPLICABLE`.
Calibrated basis requires history/units/calibration; capacity/schedule are
`NOT_APPLICABLE` only when capacity was not supplied. Missing required evidence is
never `NOT_APPLICABLE`.

---

## Phase 7 — Apply result precedence and build stable evidence

Apply the first matching rule:

1. Missing invocation arguments: `INPUT REQUIRED`, no estimate/evidence.
2. Invalid/unsafe/ambiguous/conflicting/unreadable invocation or root input:
   `ERROR`, no estimate/evidence.
3. Valid root with incomplete/conflicting scope binding, blocking required decision,
   required-root overflow, or changed input: `NOT ESTIMABLE`.
4. Valid relative evidence but any requested/required optional channel is
   incomplete, stale, unsupported, over limit, conflict/uncertainty-inconclusive,
   calibrated history fails, or supplied capacity/schedule fails:
   `PARTIAL ESTIMATE`.
5. Relative basis with complete required scope/context/readiness evidence:
   `RELATIVE ESTIMATE`.
6. Calibrated basis with complete calibration and no valid complete supplied
   schedule channel: `CALIBRATED EFFORT ESTIMATE`.
7. Calibrated basis with complete calibration and complete supplied capacity/
   calendar/DAG/schedule channel: `CALIBRATED SCHEDULE RANGE`.

Known relative evidence, calibrated effort, blockers, excluded samples, and
coverage gaps remain visible when an earlier incomplete result takes precedence.
No result implies sprint fit, approved budget, staffing, deadline, or commitment.

For a locked scope, return one deterministic extension:

```yaml
schema: cgs.estimate-report/v1
contract: cgs.estimate/v2
result: <canonical result>
operation: READ_ONLY
project_id: <canonical project identity>
project_id_sha256: <hash>
estimate_id: EST-<first-24-identity-hex>
profile: story | sprint | freeform
basis: relative | calibrated
scope_bindings: [<ordered exact binding records>]
context_manifest:
  sha256: <context manifest hash>
  inventory_sha256: <complete candidate identity digest>
  limits: <fixed and effective limits>
  overflow: <exact counts, boundary keys, and omitted digests>
  rows: [<ordered detailed rows>]
confirmed_scope: []
tentative_scope: []
readiness: <ordered field states/evidence/owners>
relative:
  model_id: cgs.estimate-relative/v2
  factor_vectors: []
  score_ranges: []
  band_ranges: []
  confidence: <LOW | MEDIUM | HIGH per unit>
history:
  manifest_and_policy: <IDs/hashes or null>
  included_samples: []
  excluded_samples: []
  quality_and_support: <gates/statistics/limitations>
calibration:
  state: AVAILABLE | UNAVAILABLE | NOT_REQUESTED
  unit: <stable effort unit ID or null>
  p50_p80_p90_ranges: <typed ranges or null>
  calculations: <bounded exact formulas/intermediates/rounding>
aggregation: <policy/scenarios/result or null>
capacity_and_schedule:
  capacity_receipt: <ID/hash or null>
  dependency_dag: <IDs/hash or null>
  effort_wait_parallelism_critical_path_elapsed: <separate fields or null>
findings: [<ordered stable findings>]
coverage:
  dimensions: <status/reason per required channel>
  ledger: [<ordered rows>]
assumptions: []
unknowns: []
scope_check_eligibility: RELATIVE_ONLY | VERIFIED_EFFORT | VERIFIED_SCHEDULE | UNVERIFIED
recommendation: <one owner-specific decision/action or none>
disclaimer: <required boundary text>
```

`estimate_id` is SHA-256 over canonical JSON of project identity, profile/basis,
ordered scope bindings including baseline/current/input hashes, relative model,
calibration/aggregation/schedule policy IDs, included history sample IDs/hashes,
evidence/context hashes, and capacity/DAG hashes. Exclude observation timestamp,
run identity, rendering, and recommendation. A changed scope/hash/model/policy/
sample/evidence/capacity creates a new estimate identity.

Sort bindings and evidence by stable IDs, included/excluded samples by sample ID,
findings by category/scope/field/fingerprint, and all assumptions/unknowns by
stable key. Render numeric values no more precisely than the unit/model policy.
Run identity and observation time appear only in the outer envelope, so identical
immutable inputs/policies/sample set reproduce the same extension bytes and
estimate ID.

Hash canonical extension JSON with Phase 1 canonicalization and wrap it in:

```yaml
schema: cgs.review-evidence/v1
record_id: sha256:<SHA-256 of canonical envelope payload excluding record_id>
artifact_id: estimate:<project_id_sha256>:<estimate_id>:<context_manifest_sha256>
artifacts: [<every retained locked input path and SHA-256, sorted as manifest>]
reviewer: <stable task identity or codex-task:<run_id>>
review_run_id: <lowercase UUID>
review_depth: bounded-full
independence: analyzer-read-only
verdict: <canonical estimate result>
timestamp: <UTC ISO-8601>
finding_ids: [<sorted stable finding IDs>]
unresolved_blocker_ids: [<sorted open binding/decision/coverage IDs>]
report_payload_sha256: <SHA-256 of canonical extension payload>
producer:
  tool: estimate
  version: cgs.estimate/v2
extension: <complete cgs.estimate-report/v1 payload>
```

Recompute artifact, context/inventory, payload, estimate identity, and record
hashes once. Fail with `ERROR — EVIDENCE CONSTRUCTION FAILED` and no evidence
record instead of emitting inconsistent bytes.

The disclaimer states: relative bands are dimensionless; numeric effort requires
the named comparable sample/model/unit policy; elapsed ranges require the named
capacity/calendar/DAG policy; quantiles/ranges are not promises; no scope,
staffing, budget, schedule, date, or project state was selected or changed.

---

## Phase 8 — Return one owner decision boundary and stop

Return at most one next action from the highest-impact open evidence:

- missing/unclear product scope, acceptance, cut/keep/defer, risk, or tradeoff:
  user/designated product owner;
- missing/proposed required ADR/interface/platform/migration decision: named
  architecture/technical owner;
- dependency state/owner/interface unknown: dependency owner;
- history/sample/unit/model gap: estimation-data or team-history owner;
- capacity/calendar/staffing/schedule conflict: producer/team owner;
- complete evidence with no blocker: no follow-up required.

State affected Scope IDs, evidence, and objective acceptance. Do not rank choices,
recommend a budget, select staffing/scope/date, invoke or message the owner, or launch
`scope-check`, `sprint-plan`, `prototype`, `architecture-decision`, or any other
workflow.

Stop after the packet. No file, scope, sprint, estimate, budget, staffing plan,
calendar, date, workflow, or Git state was changed.
