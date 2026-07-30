# Sprint Status Rules v1

This private contract is normative for `sprint-status`. If it conflicts with
`SKILL.md`, stop with `run_status: ERROR` before reading sprint evidence. Never
choose the more permissive interpretation.

## Canonical bytes, paths, and revisions

- Read text as UTF-8 without BOM. Canonical derived records use LF.
- Project paths are root-relative, slash-separated, Unicode NFC, and confined to
  the project after canonical resolution. Reject absolute/device paths,
  traversal, alternate data streams, and symlinks/reparse points escaping the
  project.
- A raw source revision is explicit revision declared by the source. A declared revision has
  the form `<explicit-revision>`.
- Stable IDs are compared exactly after schema validation; do not case-fold,
  trim, repair, or infer them from prose.
- Derived objects use canonical JSON: UTF-8/LF, object keys sorted by Unicode
  code point, arrays in declared order unless a rule says to sort, integers only,
  and no comments, duplicate keys, floats, NaN, or Infinity.
- Percentages are integer basis points (`0..10000`). Use floor division for
  progress/time displays and retain all numerator/denominator operands.
- Timestamps are explicit ISO-8601 instants with offsets; convert to the
  configured timezone only for calendar/working-day boundaries.

## Fixed bounds

Apply before parsing or expanding references:

| Object | Maximum |
|---|---:|
| Selector source | 512 KiB |
| Sprint plan | 2 MiB |
| Status tracker | 2 MiB |
| Status configuration | 256 KiB |
| One story or checkpoint | 2 MiB |
| Stories | 500 |
| Dependency edges | 5,000 |
| Checkpoints | 500 |
| Aggregate referenced bytes | 64 MiB |
| Conflicts/findings | 1,000 |
| Summary lines | 50 |
| Attention rows per page | 20 |

A required over-limit input makes the applicable data/health result unavailable.
Do not analyze a prefix as though it represented complete coverage. Counts and
metrics always use the full validated set, even when output rows paginate.

## Stable selector and plan identity

`current` selector fields are only a top-level tracker `active_sprint_id` and an
explicit session `active_sprint_id` or exact plan reference. A filename or mtime
is not authority.

The selected plan implements the project sprint-plan schema and must expose:

```text
schema_version
sprint_id
plan_revision
updated_at
goal
start_date
end_date
timezone
estimate_unit
stories[]
```

Each story row contains stable `story_id`, exact path or canonical inline bytes,
priority, non-negative integer estimate, owner or `UNKNOWN`, and a unique array
of dependency story IDs. Controlled priorities are `MUST_HAVE`, `SHOULD_HAVE`,
and `COULD_HAVE` after the explicit spellings below are normalized.

## Story-set revision

For every plan story, build exactly:

```text
<story-id>\t<normalized-path-or-INLINE>\t<source-revision-or-MISSING>
```

For a referenced story, read the declared path and validate its schema and explicit revision. For an inline story, use the plan-owned story ID and revision. For an absent referenced file, use literal `MISSING`. Sort records by `story-id` in Unicode code-point order for presentation only. Read `story_set_revision` from the authoritative sprint plan; never calculate an identifier from the record bytes. Duplicate or missing IDs and duplicate normalized paths are conflicts.

## Tracker schema and normalization

An applicable tracker must implement its declared project schema and contain:

```text
schema_version
sprint_id
active_sprint_id              # current report only
plan_revision
story_set_revision
updated_at
stories[]
```

Each tracker row has exactly one stable story ID, status, status update timestamp,
and blocker reference/reason when blocked. Coverage is a one-to-one join with the
plan story set.

Only these lifecycle spellings normalize:

| Story spellings | Tracker spellings | `story_status` |
|---|---|---|
| `Complete`, `Done` | `done` | `DONE` |
| `In Review` | `review`, `in_review` | `IN_REVIEW` |
| `In Progress` | `in-progress`, `in_progress` | `IN_PROGRESS` |
| `Ready` | `ready-for-dev`, `ready_for_dev` | `READY` |
| `Not Started` | `backlog` | `NOT_STARTED` |
| `Blocked` | `blocked` | `BLOCKED` |

No marker in tracker-absent fallback is `UNKNOWN`; absent story bytes are
`MISSING`. An unsupported or contradictory value is a conflict. UNKNOWN and
MISSING are excluded from DONE, backlog, weighted totals, incomplete Must-Have
totals, schedule lag, and every claimed complete denominator. Show separate
known-status and known-estimate coverage.

Priority spellings normalize only as follows:

| Plan spelling | Priority |
|---|---|
| `Must Have`, `must_have` | `MUST_HAVE` |
| `Should Have`, `should_have` | `SHOULD_HAVE` |
| `Could Have`, `could_have` | `COULD_HAVE` |

## Data status

- `VERIFIED`: exact tracker/plan/story identity, revision, revision, complete
  coverage, and every required downstream input verify.
- `PARTIAL`: no applicable tracker or a non-conflicting optional/coverage gap is
  explicitly retained. A required missing health input still forces health
  UNKNOWN.
- `DATA_CONFLICT`: two applicable authorities disagree, a declared revision/revision
  fails, a status/checkpoint projection contradicts another, or a source changes
  during the run. No counts or health derived from the conflicting snapshot.
- `UNAVAILABLE`: sprint cannot be uniquely resolved or its required plan cannot
  be safely read.

The report may preserve resolution diagnostics for DATA_CONFLICT/UNAVAILABLE,
but must not mix partial counts from incompatible sources.

## Project-owned status configuration

Read exactly `production/config/sprint-status.yaml`. Its schema is
`cgs.sprint-status-config/v1`:

```yaml
schema_version: cgs.sprint-status-config/v1
config_revision: <stable revision>
updated_at: <ISO-8601 instant>
stale_after_days: <positive integer>
stale_day_basis: CALENDAR_DAYS | WORKING_DAYS
timezone: <IANA timezone>
working_calendar:
  path: <canonical path or null>
  revision: <declared revision or null>
priority_weights:
  MUST_HAVE: <positive integer>
  SHOULD_HAVE: <positive integer>
  COULD_HAVE: <positive integer>
health:
  schedule_lag_at_risk_bps: <integer 0..10000>
  must_have_time_remaining_trigger_bps: <integer 0..10000>
estimate_unit: <exact supported project unit>
```

For CALENDAR_DAYS, calendar path/revision must be null. For WORKING_DAYS, the
calendar is required, project-confined, revision-verified, and must define the full
sprint/as-of date range, working weekdays, holidays, and exceptions without
overlap. Missing or invalid configuration creates stable missing-field findings;
no threshold or weight defaults exist in the skill or spec.

Always output configuration path, revision, declared revision, `stale_after_days`, day
basis, timezone, calendar identity, priority weights, schedule-lag threshold,
Must-Have time trigger, and estimate unit.

## Date and staleness arithmetic

Record one `as_of` instant. Parse plan dates at the configured timezone:

- `total_days` counts configured day-basis intervals from start inclusive to end
  exclusive;
- `elapsed_days` is clamped to `[0,total_days]` only after valid dates/calendar;
- `remaining_days = total_days - elapsed_days`;
- `time_consumed_bps = floor(10000 * elapsed_days / total_days)`;
- `time_remaining_bps = 10000 - time_consumed_bps`.

Zero/negative duration, invalid timezone, missing dates, or incomplete working
calendar makes all date-derived values and health UNKNOWN.

For each IN_PROGRESS story, count configured day-basis boundaries strictly after
its explicit status-update date and through the as-of date. It is STALE only when
`elapsed_status_days > stale_after_days`; equality is FRESH. Missing/invalid
status timestamp or unusable calendar is UNKNOWN. Never substitute file mtime,
commit time, session note age, or the other day basis.

## Dependency graph and remaining critical path

An edge `A -> B` means B depends on A. Validate unique nodes, known endpoints,
no self-edge, unique edges, and a directed acyclic graph using stable story IDs.
Invalid or cyclic input makes dependency/critical-path health inputs UNKNOWN.

For each story, `remaining_estimate` is zero only when status is DONE; otherwise
it is its verified estimate. Compute longest remaining-estimate distance over a
stable topological order. When multiple maximum paths tie, keep the complete set
of nodes participating in any maximum path and select the lexicographically
smallest full ID sequence only for display. `critical_path_estimate` is the
maximum total; the complete critical-node set controls BLOCKED/STALE checks.

Also compute `dependency_blocked_estimate` as the unique sum of remaining
estimates for non-DONE descendants of each confirmed BLOCKED story. Do not double
count nodes reachable from multiple blockers.

## Priority- and estimate-weighted progress

For each known-status story with verified estimate and priority:

```text
weighted_planned_i = estimate_i * configured_priority_weight_i
weighted_done_i = weighted_planned_i when story_status = DONE, otherwise 0
```

Then:

```text
weighted_planned = sum(weighted_planned_i)
weighted_done = sum(weighted_done_i)
weighted_completion_bps = floor(10000 * weighted_done / weighted_planned)
schedule_lag_bps = time_consumed_bps - weighted_completion_bps
```

A zero denominator or incomplete required status/estimate/priority coverage makes
weighted completion and health UNKNOWN. Never use task count as a substitute.

`schedule_signal` is:

- `UNKNOWN` if an operand/config threshold is unknown;
- `LAGGING` when `schedule_lag_bps >= schedule_lag_at_risk_bps`;
- `AHEAD` when `schedule_lag_bps < 0`; and
- `WITHIN_TOLERANCE` otherwise.

Keep exact integer operands, unit, priority weights, config revision/revision, and
coverage. These calculations are a rough directional signal from estimates, not
a forecast or delivery promise.

## Must-Have risk and health derivation

`incomplete_must_have_estimate` is the sum of verified estimates for MUST_HAVE
stories whose known status is not DONE. UNKNOWN/MISSING status or missing
estimate/priority does not add zero; it makes the required input unknown.

Apply the first matching health rule:

| Rule | Condition | `health_status` |
|---|---|---|
| `SS-HEALTH-01` | DATA_CONFLICT or UNAVAILABLE | `UNKNOWN` with no health calculation |
| `SS-HEALTH-02` | Any required plan/config/date/status/estimate/priority/DAG/staleness operand is unknown | `UNKNOWN` |
| `SS-HEALTH-03` | At least one confirmed BLOCKED node is in the complete critical-node set | `BLOCKED` |
| `SS-HEALTH-04` | Confirmed off-critical-path BLOCKED node, critical-path STALE node, LAGGING schedule signal, or positive incomplete Must-Have estimate when `time_remaining_bps <= must_have_time_remaining_trigger_bps` | `AT_RISK` |
| `SS-HEALTH-05` | All prerequisites known and none of the above | `ON_TRACK` |

Record the first rule ID, exact boolean/input tuple, matching stable story IDs,
and configuration identity. `BLOCKED` is not a synonym for DATA_CONFLICT or
LAGGING. ON_TRACK never means DONE and is prohibited with a required unknown.

## Recovery and review evidence

A dev-story checkpoint is usable only when its schema, story/path identity, plan
revision, source/baseline/current revisions, intended/actual write sets, evidence/error,
and resume point validate against raw current bytes. It cannot override tracker or
story status.

Unresolved PARTIAL/BLOCKED recovery requires both projections IN_PROGRESS.
IN_REVIEW requires a matching plan revision, post-write implementation/evidence
revisions, executed blocking test with exit code zero, and log revision, with no
unresolved transaction. Contradictions are DATA_CONFLICT.

## Stable findings

Use `cgs.sprint-status-finding/v1`. Allocate its stable ID as `SSF-<sprint-id>-<finding-type>-<finding-ordinal>`. Persist the ID across reruns and keep subject and field IDs as separate fields.

Sort/deduplicate ID arrays. Exclude wording, line, observed value/revision,
classification, status, timestamp, and recommendation so the same logical gap
retains its ID. A row includes classification `CONFLICT|BLOCKER|DATA_GAP|RISK|
WARNING`, source refs, expected/observed values, affected calculations, owner or
UNKNOWN, recovery/action, and resolution condition.

## Bounded output

The run envelope is `cgs.sprint-status-run/v2`. Keep the primary summary at or
below 50 rendered lines. It contains provenance, config/thresholds, coverage,
status/estimate summaries, critical path, health derivation, limitations, and one
recommendation.

Show at most 20 attention rows ordered by classification priority
`CONFLICT,BLOCKER,DATA_GAP,RISK,WARNING`, then story priority, then stable ID.
Report `shown/total` and continuation cursor equal to the last shown stable ID.
Pagination changes display only, never metrics. Create no attachment or project
artifact.
