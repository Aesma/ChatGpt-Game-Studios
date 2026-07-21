---
name: estimate
description: "Produces read-only, provenance-bound relative or calibrated effort evidence for story, sprint, and freeform profiles without choosing scope, staffing, budget, or schedule."
---

# Estimate

## Invocation and profile contract

Invoke exactly one profile:

```text
$estimate story --input <story-path> [--history <history-manifest>] [--capacity <capacity-receipt>] [--evidence <evidence-manifest>]
$estimate sprint --input <sprint-path> [--history <history-manifest>] [--capacity <capacity-receipt>] [--evidence <evidence-manifest>]
$estimate freeform --description <text> --scope-id <id> --baseline-sha256 <hash> --current-sha256 <hash> [--history <history-manifest>] [--capacity <capacity-receipt>] [--evidence <evidence-manifest>]
```

- `story` estimates one exact story artifact.
- `sprint` estimates every exact story entry in one sprint manifest, then aggregates
  only compatible calibrated distributions.
- `freeform` estimates a normalized UTF-8 description only when its stable Scope ID
  and immutable baseline/current SHA-256 values are supplied.

No profile is inferred. No arguments, an unflagged path/description, mixed profiles,
unknown flags, repeated inputs, or more than one root input returns `INPUT REQUIRED`
or `ERROR` without estimating. Never search by title or choose a recently modified
story/sprint.

This skill is read-only. It writes no estimate file, story, sprint, plan, decision,
session state, or Git state; invokes no gate; delegates no action; and starts no
follow-up workflow.

## Non-negotiable estimation rules

1. **Relative-first** — Without a valid comparable-history model, output only a
   dimensionless relative-size band/range, factor vector, uncertainty, and evidence
   gaps. Do not output hours, person-days, workdays, calendar days, dates, velocity
   conversions, or a recommended budget.
2. **Calibration before numeric time** — Numeric effort requires completed samples
   from the same team, profile, work-type taxonomy, estimation method/schema, and
   compatible delivery conditions. Calendar/workday duration additionally requires
   a current capacity/calendar receipt and dependency critical path.
3. **Scope-bound receipt** — Every estimate result binds stable Scope ID, immutable
   baseline SHA-256, current scope-manifest SHA-256, input path/content SHA-256, and
   every consumed evidence hash. Missing or conflicting scope bindings return
   `INPUT REQUIRED` or `NOT ESTIMABLE`; never emit a scope-check-compatible receipt.
4. **Evidence, not commitment** — Estimates quantify evidence and uncertainty only.
   The user or designated producer owns scope selection, sprint inclusion, staffing,
   budget, target dates, and tradeoffs. Never commit to a date, select Cut/Keep/Defer,
   recommend a budget, or mutate/re-baseline scope.
5. **Confirmed versus tentative** — Treat only scope, systems, files, dependencies,
   and acceptance boundaries explicitly named by bound artifacts as confirmed.
   Predicted files or inferred integrations are tentative risks, not counted facts.
6. **Blocked decisions stay blocked** — Unresolved product behavior, missing required
   architecture/ADR, incompatible platform choices, unknown migration policy, or an
   unresolved required dependency yields `NOT ESTIMABLE` for delivery. A separately
   scoped discovery estimate may still be reported when its own Scope ID and bounds
   are valid.
7. **Effort is not elapsed time** — Never sum person-effort into calendar duration.
   Elapsed ranges require dependency order, parallelism/WIP limits, reviewer/service
   wait time, team availability, and calendar validity.
8. **Reproducible and mutation-safe** — Hash inputs before parsing and re-hash before
   reporting. Identical immutable inputs, model version, and sample set must produce
   identical factor scores, samples, quantiles, and result. Changed bytes invalidate
   all conclusions.

## Decision and workflow boundaries

| Concern | Owner | Estimate output |
|---|---|---|
| Relative complexity and uncertainty | `estimate` | Evidence-bound factor vector and band |
| Calibrated effort distribution | `estimate` | P50/P80/P90 only when calibration gates pass |
| Capacity and calendars | Team/producer-owned receipt | Consumed, never invented or edited |
| Scope delta | `$scope-check` | Consume exact Scope ID and baseline/current hashes |
| Scope inclusion, cuts, or re-baseline | User/designated producer | Not decided here |
| Sprint composition and scheduling | `$sprint-plan update` or owning planner | Read-only handoff after a human/product decision |
| Architecture decision | ADR owner | Unresolved required ADR blocks delivery estimate |

An estimate, confidence label, model output, or conversational approval is not scope,
budget, staffing, scheduling, implementation, or mutation authority.

## Input and scope-binding contracts

### Shared scope binding

Every estimate unit must provide:

- stable `Scope ID`;
- `Baseline SHA-256` for the approved immutable scope baseline;
- `Current Scope SHA-256` for the current scope manifest;
- parent epic/sprint/milestone Scope ID as applicable;
- input path and SHA-256, or normalized freeform text SHA-256;
- profile and work-type taxonomy ID/version;
- declared completeness state.

For `story`, read these from the story's explicit scope-binding block or one exact
referenced binding artifact. For `sprint`, every story entry must provide its exact
path/hash and scope binding. For `freeform`, the flags are mandatory; the output is
still `NOT ESTIMABLE` if the description cannot state a testable delivery boundary.

These fields deliberately match the staged scope-check estimate-evidence interface.
A result lacking any binding is visibly `UNBOUND` and must not be represented as an
`estimate-receipt`.

### Bounded context

Read the applicable root-to-target `AGENTS.md` chain, the root input, its exact
first-level story/ADR/dependency/test links, and the optional evidence manifests only.
Do not scan all GDDs, code, Git history, TODOs, or sprint directories for similarity.

Budgets:

- at most 30 stories in a sprint estimate;
- at most 50 linked artifacts;
- at most 3 MiB total text;
- at most 100 history samples before deterministic filtering.

If a required root or binding exceeds budget, return `NOT ESTIMABLE`. If only optional
evidence exceeds budget, return `PARTIAL ESTIMATE`, list skipped evidence, and do not
produce numeric effort or elapsed ranges.

### Evidence manifest

An optional evidence manifest is an exact path/hash allowlist containing:

- architecture/ADR, dependency, interface, migration, test, performance, security,
  localization, platform, and release evidence;
- purpose, expected SHA-256, covered Scope IDs, and validity timestamp for each item;
- confirmed affected paths/modules and tentative candidates in separate lists;
- explicit missing/unknown entries.

Code or file counts are never used as effort by themselves.

## Deterministic relative-size model

Record `Model ID: EST-RELATIVE-v1`. Score five evidence axes from 0 through 3. Use the
highest supported level per axis; if evidence is insufficient, record `UNKNOWN` and a
range from the lowest to highest plausible level rather than selecting a point.

| Axis | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Delivery breadth | Local configuration/content only | One bounded implementation unit | Multiple units in one system | Multiple systems or engine/platform boundary |
| Novelty | Existing pattern and owner-proven example | Minor adaptation | New local pattern or material research | New architecture/technology decision required |
| Integration | No runtime integration | One stable interface | Multiple interfaces or service coordination | Cross-platform/network/external-service integration |
| Validation | Existing automated coverage unchanged | One bounded test layer | Multiple test layers or performance validation | Certification/security/migration/large matrix validation |
| Data/release | No persistent/release effect | Reversible config/content | Compatible migration or release coordination | Save/schema migration, irreversible data, or multi-platform rollout |

Sum resolved axis values to form `Relative Complexity Score`. Unknown axes produce a
minimum/maximum score interval. Map scores only to dimensionless bands:

| Score | Relative band |
|---|---|
| 0–3 | `S` |
| 4–7 | `M` |
| 8–11 | `L` |
| 12–15 | `XL` |

When a score interval crosses boundaries, report a band range such as `M–L`. These
bands do not mean days or story points and must not be summed as time.

## Uncertainty and estimability

Evaluate four readiness fields:

| Field | `READY` requires |
|---|---|
| Requirements | Testable delivery boundary and acceptance criteria; no blocking TBD |
| Architecture | Required ADRs/interfaces are accepted and hash-bound, or demonstrably not needed |
| Dependencies | Required dependency states/owners/interfaces are known and compatible |
| Validation | Required test/release/migration evidence is identified |

Derive:

- `NOT ESTIMABLE`: any required product/architecture/dependency choice is `BLOCKED`,
  or the scope binding/completeness is invalid;
- `LOW`: one or more fields is `UNKNOWN` but none is a blocking decision;
- `MEDIUM`: all fields are known and at most one is not fully ready;
- `HIGH`: all four are `READY`, all consumed hashes match, and the relative band is a
  single band rather than a cross-band interval.

This is `Relative Estimate Confidence`, not probability of delivery. Numeric
calibration confidence is reported separately from sample count and variance.

## Comparable-history and calibration contract

History is never discovered by scanning sprint files. `--history` names one immutable
manifest with its own path/hash/schema/model version. Each sample provides:

- sample ID; stable Scope ID; profile; work-type taxonomy ID/version;
- team ID and materially relevant delivery conditions;
- source baseline/current/input hashes;
- the same `EST-RELATIVE-v1` factor vector/score;
- actual completed effort in one declared effort unit;
- start/end and blocked/wait effort recorded separately;
- completion evidence and excluded anomaly flags.

Filter deterministically. Include only completed samples with the same team, profile,
work type, model version, effort unit, and compatible delivery conditions. List every
included and excluded sample with a reason. Never use cross-team “velocity”, a global
average, title similarity, or the most recent arbitrary sprint.

Numeric effort calibration is permitted only when:

- at least 5 comparable included samples remain;
- all use one actual-effort unit and matching model version;
- all five current factor axes resolve to one score rather than an unknown interval;
- factor scores cover the current score/range without extrapolation;
- median absolute deviation and coefficient of variation are computable;
- coefficient of variation is at most `0.50` and no unresolved anomaly remains.

For each included sample calculate:

```text
normalized effort ratio = actual effort / max(relative complexity score, 1)
```

Sort ratios deterministically. Use empirical nearest-rank quantiles and report the
exact selected samples:

```text
Effort P50/P80/P90 = current score × ratio P50/P80/P90
```

Round only to the precision of the historical effort unit; show the unrounded
calculation. If gates fail, output `Calibration: UNAVAILABLE` and relative size only.
Never substitute `1 point = 1 day` or another default conversion.

## Capacity, dependencies, and elapsed range

Numeric effort is not an elapsed estimate. `--capacity` must identify one current,
hash-bound receipt containing team ID, effective capacity per working day in the same
unit, availability dates, working calendar/time zone, WIP/parallel-lane limits,
reviewer/service availability, and validity interval.

The root input/evidence must contain a dependency DAG with exact predecessor IDs,
parallelizable work packages, and evidenced external wait ranges. Reject cycles.
For each P50/P80/P90 effort scenario, schedule packages deterministically against the
capacity/calendar/WIP constraints and report the critical path, parallel branches,
effort, wait, and resulting elapsed workdays/calendar dates separately.

If capacity, calendar, dependency DAG, or wait evidence is missing/stale/mismatched,
output `Elapsed Range: UNVERIFIED`. Never divide total effort by headcount as a
shortcut and never invent a start date.

## Sprint aggregation

Estimate each story independently with its own Scope ID and hashes. Relative bands are
reported per story and never arithmetically summed. A numeric sprint effort
distribution is allowed only if every included story has compatible calibrated
distributions in the same unit/model, and the history manifest provides a validated,
hash-bound sprint aggregation model with its correlation assumptions, deterministic
scenario set/seed, and applicability criteria. Per-story quantile columns are not
additive and must never be labeled sprint P50/P80/P90. The sprint manifest must also
declare inclusion and dependency relationships. Otherwise output
`Sprint Effort: UNVERIFIED` and list which stories prevent aggregation.

Elapsed sprint range additionally requires a valid capacity receipt and complete DAG.
Do not infer sprint fit, select stories, remove work, or promise completion within the
timebox. Report any capacity conflict as evidence for a user/producer decision.

## Canonical result states

Derive exactly one:

| Result | Meaning |
|---|---|
| `ERROR` | Invalid/ambiguous profile, unsafe path, unreadable input, schema failure, or dependency cycle |
| `INPUT REQUIRED` | Required profile/input/scope-binding argument is absent; no estimate produced |
| `NOT ESTIMABLE` | Bound delivery scope has a blocking product/architecture/dependency decision or invalid completeness |
| `PARTIAL ESTIMATE` | Relative assessment is valid but required optional evidence was unavailable, stale, hash-mismatched, or over budget |
| `RELATIVE ESTIMATE` | Valid scope-bound relative band/range only; numeric calibration unavailable or not requested |
| `CALIBRATED EFFORT ESTIMATE` | Comparable-history gates pass; relative band plus P50/P80/P90 effort is available |
| `CALIBRATED SCHEDULE RANGE` | Effort calibration plus capacity/calendar/DAG gates pass; elapsed P50/P80/P90 is available |

Do not output `COMPLETE`, a recommended budget, or a committed date.

## Canonical estimate receipt

Only `RELATIVE ESTIMATE`, `CALIBRATED EFFORT ESTIMATE`, or
`CALIBRATED SCHEDULE RANGE` emits an `estimate-receipt`. A partial or blocked result
emits an `estimate-analysis` with the same provenance fields but is not consumable as
complete scope-check effort evidence. For staged scope-check, a relative-only receipt
proves size provenance but leaves `Effort Evidence: UNVERIFIED`; only a current,
binding-matched calibrated-effort or calibrated-schedule receipt may support
`Effort Evidence: VERIFIED`.

```yaml
Artifact Type: estimate-receipt
Schema Version: 1
Estimate ID: <deterministic-id>
Result: RELATIVE ESTIMATE | CALIBRATED EFFORT ESTIMATE | CALIBRATED SCHEDULE RANGE
Profile: story | sprint | freeform
Scope Bindings:
  - Scope ID: <stable-id>
    Baseline SHA-256: <hash>
    Current Scope SHA-256: <hash>
    Input Path: <path-or-FREEFORM>
    Input SHA-256: <hash>
Model ID: EST-RELATIVE-v1
Relative Factor Vector: <five-axis values/ranges>
Relative Score Range: <min-max>
Relative Band Range: <S|M|L|XL or range>
Relative Estimate Confidence: LOW | MEDIUM | HIGH
History Manifest: <path/hash or NONE>
Included Samples: <ordered IDs and hashes>
Excluded Samples: <ordered IDs and reasons>
Calibration: AVAILABLE | UNAVAILABLE | NOT_REQUESTED
Effort Unit: <unit or NOT_APPLICABLE>
Effort P50/P80/P90: <values or UNVERIFIED>
Capacity Receipt: <path/hash or NONE>
Dependency Evidence: <path/hash or NONE>
Elapsed P50/P80/P90: <effort/wait/critical-path values or UNVERIFIED>
Assumptions: <ordered evidence-bound list>
Unknowns: <ordered list>
Consumed Artifacts: <canonical paths, byte lengths, SHA-256 values>
Generated At: <timestamp>
```

The receipt ID is derived from profile, ordered scope bindings, model ID, history
sample set, capacity/dependency hashes, and assumptions. A changed Scope ID,
baseline/current/input hash, model, sample, evidence, or capacity receipt creates a new
estimate identity and invalidates the old result for scope-check consumption.

## Phase 0: Validate profile and paths

Parse exactly one profile and its required flags. Canonicalize paths inside the
repository, reject aliases/traversal, and record all root preimage hashes. Validate
scope bindings before reading optional evidence.

## Phase 1: Load bounded scope and readiness evidence

Read the applicable AGENTS chain, root input, exact first-level links, and manifest
allowlists within budget. Separate confirmed scope/paths from tentative candidates.
Validate requirements, architecture, dependencies, validation, and blocking decisions.

If delivery is blocked, identify the smallest separately bounded discovery question;
do not estimate that discovery unless it already has its own Scope ID and invocation.

## Phase 2: Compute relative size and uncertainty

Apply `EST-RELATIVE-v1` independently to every estimate unit. Show axis evidence,
unknown ranges, score calculation, band mapping, and readiness-derived confidence.
Do not use history or capacity to alter the relative factor vector.

## Phase 3: Select comparable history

When `--history` is present, validate its binding and filter samples with the fixed
rules. List included/excluded samples and compute dispersion. If any calibration gate
fails, preserve the relative result and mark numeric calibration unavailable.

## Phase 4: Optionally compute effort and elapsed distributions

Compute empirical P50/P80/P90 effort only when all history gates pass. Compute elapsed
scenarios only when the capacity/calendar/DAG contract also passes. Keep effort,
external wait, and elapsed values in separate columns and show formulas.

For sprint profile, preserve per-story estimates and aggregate only compatible
distributions; otherwise make aggregation `UNVERIFIED`.

## Phase 5: Re-hash, report, and stop

Re-read and re-hash every consumed artifact. If any bytes changed, discard estimates
and return `NOT ESTIMABLE — INPUT CHANGED DURING ESTIMATE`.

Output:

```markdown
# Estimate
Result: <canonical result>
Operation: READ_ONLY

## Scope bindings and inputs
## Confirmed and tentative scope
## Readiness and blocking decisions
## Relative factor vector, score, band, and confidence
## Comparable-history inclusion/exclusion
## Effort P50/P80/P90 or calibration gaps
## Dependency DAG, capacity, critical path, and elapsed range or gaps
## Per-story and aggregate evidence for sprint profile
## Assumptions and unknowns
## Canonical estimate receipt or non-consumable analysis
## Decision boundary and handoff
```

The handoff states that the estimate is quantitative evidence only. If product choices
or capacity conflicts exist, present the affected Scope IDs and ask the user or
producer to choose scope, staffing, or schedule. Do not rank options or invoke
`$scope-check`, `$sprint-plan`, `$prototype`, `$architecture-decision`, or any agent.

End by stating that no file, scope, sprint, budget, staffing plan, date, workflow, or
Git state was changed.

## Final invariants

- No uncalibrated numeric time or `1 point = 1 day` default.
- No recommended budget, sprint-fit claim, deadline promise, or product decision.
- Every consumable receipt binds Scope ID and immutable baseline/current hashes.
- Relative size, effort, wait, capacity, and elapsed time remain distinct.
- Missing required ADR/product/dependency decisions block delivery estimates.
- Identical immutable inputs and sample set reproduce the same estimate.
