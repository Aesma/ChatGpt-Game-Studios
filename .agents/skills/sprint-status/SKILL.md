---
name: sprint-status
description: Read-only sprint status for one stable sprint, with revision-checked tracker evidence, explicit UNKNOWN handling, project-configured staleness, and a bounded estimate-, priority-, and dependency-aware health signal.
---

# Sprint Status

Produce one bounded situational-awareness snapshot for exactly one sprint. The
workflow is strictly read-only: it does not update the plan, tracker, stories,
configuration, checkpoint, scope, or session state; request write authorization;
invoke a director gate; execute another workflow; or infer completion from source
code filenames.

This is a status signal, not a sprint review, delivery commitment, forecast, or
authority to replan scope. It may make one evidence-bound recovery or attention
recommendation and then stops.

## Invocation

Use exactly:

```text
$sprint-status [current|<stable-sprint-id>]
```

- Omitted selector means `current`.
- A stable sprint ID matches `^[a-z0-9][a-z0-9-]*$`.
- Reject extra arguments, path separators, traversal, glob/regex characters, or
  malformed IDs with `run_status: ERROR`; read no sprint evidence and write
  nothing.
- Review-mode files are irrelevant and are not read.

Never choose a sprint or evidence source from mtime, creation time, filename
order, a guessed “latest” value, or conversational memory.

## Load the private contract

Read [sprint-status-rules-v1.md](references/sprint-status-rules-v1.md)
completely. It defines canonical revision validation, source/config schemas, limits, story
normalization, working-day/staleness calculations, weighted progress, dependency
DAG and critical-path rules, health derivation, and bounded output.

Read [continued-workflow.md](references/continued-workflow.md) completely and
execute its phases in order. Missing, unreadable, or contradictory private
contracts return `run_status: ERROR` before sprint evidence is read.

## Read-only boundary

For the entire run:

```text
allowed_project_read_set: <bounded, reported paths>
allowed_project_write_set: []
source_artifacts_mutated: false
authorization_requested: false
director_gate_invoked: false
downstream_workflow_invoked: false
```

Capture declared revisions for every inspected project file before analysis and revalidate
them before returning. If a source changes during the run, set
`data_status: DATA_CONFLICT`, `health_status: UNKNOWN`, discard derived counts and
health, and report the changed path/expected/observed revisions. Never repair or
revert concurrent work.

Apply all fixed file, story, edge, checkpoint, and output limits before parsing.
An exceeded required bound is an explicit data-quality failure, not permission
to truncate inputs and claim complete coverage.

## Status vocabulary

Use these exact machine values:

| Field | Values | Meaning |
|---|---|---|
| `run_status` | `COMPLETE`, `PARTIAL`, `BLOCKED`, `ERROR` | Execution state of this read-only check |
| `data_status` | `VERIFIED`, `PARTIAL`, `DATA_CONFLICT`, `UNAVAILABLE` | Identity, coverage, and source-quality state |
| `health_status` | `ON_TRACK`, `AT_RISK`, `BLOCKED`, `UNKNOWN` | Single sprint health enum |
| `story_status` | `DONE`, `IN_REVIEW`, `IN_PROGRESS`, `READY`, `NOT_STARTED`, `BLOCKED`, `UNKNOWN`, `MISSING` | Per-story observed lifecycle state |
| `stale_status` | `FRESH`, `STALE`, `UNKNOWN`, `NOT_APPLICABLE` | Per-story configured freshness result |
| `schedule_signal` | `AHEAD`, `WITHIN_TOLERANCE`, `LAGGING`, `UNKNOWN` | Weighted progress-versus-time observation |

Display labels may replace underscores with spaces, but the report must retain
the exact machine value. Do not emit `Behind` or `SPRINT COMPLETE` as a health
verdict. A `DATA_CONFLICT` is a data state; a confirmed blocked critical path is
`health_status: BLOCKED`; schedule lag is a `schedule_signal`. These are never
interchangeable.

If required dates are absent or invalid, `health_status` is exactly `UNKNOWN`
with stable missing-field findings. Never print a combined string such as
“ON TRACK / AT RISK / BLOCKED: unknown.”

## Phase 1 — Resolve exactly one sprint

Read selector sources without trusting their story statuses:

- `production/sprint-status.yaml`, when it exists; and
- `production/session-state/active.md`, when it exists.

Apply this precedence:

1. an explicit stable sprint ID;
2. exactly one well-formed top-level tracker `active_sprint_id` for `current`;
3. exactly one explicit session `active_sprint_id` or exact sprint plan reference;
4. otherwise stop and ask the user for one stable sprint ID.

Resolve only canonical project-confined plan candidates and require exactly one
regular file whose declared `sprint_id` equals the selected ID. Record selector
source/path/revision and plan path/revision. A malformed or duplicate declaration,
zero/multiple plan matches, or unsafe path is `run_status: BLOCKED`,
`data_status: UNAVAILABLE`, and `health_status: UNKNOWN`; read no story evidence.

For `current`, tracker and session declarations are co-validation evidence after
precedence resolves an ID. If both are present and disagree, return
`DATA_CONFLICT`. An explicit historical ID may mark a well-formed tracker for a
different active sprint `NOT_APPLICABLE`, but it may not use that tracker's story
statuses.

If no selector and no sprint plan exist, return “No active sprint found” and one
handoff to `$sprint-plan new`, without a health verdict.

## Phase 2 — Validate the plan and exact story set

The selected plan must declare:

- `schema_version`, exact `sprint_id`, `plan_revision`, and `updated_at`;
- goal, start/end dates, timezone, and estimate unit;
- every story's stable ID, exact referenced path or inline record, priority,
  estimate, owner, and dependency IDs; and
- exact status/config/tracker contract versions it expects when declared.

Duplicate/missing story IDs, path escape, duplicate references, invalid priority
or estimate, self-dependency, missing dependency target, or cyclic dependency
graph is recorded exactly. Identity/path/schema conflicts stop as
`DATA_CONFLICT`; missing estimate/priority/dependency information makes the
weighted/critical-path inputs unknown and therefore health unknown.

Construct the deterministic story-set revision using the rules reference: raw story
bytes or exact inline bytes, stable IDs, canonical paths, and explicit `MISSING`
sentinels. Filesystem timestamps never enter this identity.

## Phase 3 — Validate tracker authority before status use

When `production/sprint-status.yaml` applies to the selected sprint, require:

```text
schema_version
sprint_id
active_sprint_id                 # required for current only
plan_revision
story_set_revision
updated_at
stories[]
```

Validate exact selected/plan/tracker IDs, plan revision, revalidate story-set
revision, unique complete story coverage, raw source revisions, controlled statuses, and
tracker `updated_at` not predating the plan or any explicit story status update.
revision/identity agreement—not timestamps alone—proves freshness.

Normalize only the table defined in the rules reference. `IN_REVIEW` is
implemented but not accepted and never counts as DONE. Story/tracker disagreement,
missing tracker entry, extra entry, malformed field, stale applicable tracker, or
revision/revision mismatch returns only:

```text
DATA CONFLICT — sprint health not assessed.
```

Set `data_status: DATA_CONFLICT`, `health_status: UNKNOWN`, name every expected
and observed value/source, provide one recorder recovery action, and stop before
story counts, completion, critical path, or health derivation. Do not fall back
to markdown around an invalid applicable tracker.

## Phase 4 — Tracker-absent markdown fallback

Only when no applicable tracker exists, read the exact plan-referenced story
files or inline records. Accept only explicit controlled lifecycle fields/markers
defined in the rules reference.

- An explicit Not Started marker becomes `NOT_STARTED`.
- No lifecycle marker becomes `UNKNOWN`, creates a data-quality finding, and is
  excluded from DONE/backlog/status denominators and all verified work totals.
- A missing referenced file becomes `MISSING`, not NOT_STARTED or zero work.
- Multiple contradictory markers become `DATA_CONFLICT`.

Report `data_status: PARTIAL` and the exact fallback coverage. Any UNKNOWN or
MISSING required story forces `health_status: UNKNOWN`; it never increases the
backlog, incomplete-Must-Have count, or apparent schedule lag.

Do not scan `src/`, asset folders, build output, git history, or filename slugs.
The existence of an implementation-looking file is neither story status nor an
Evidence Hint and cannot affect identity, coverage, counts, estimates,
critical-path calculation, schedule signal, or health.

## Phase 5 — Validate recovery and review evidence

For each story, inspect only its exact derived
`production/session-state/dev-story-<story-id>.yaml` path when present. A
checkpoint is recovery evidence, never a status override or completion proof.

An unresolved PARTIAL/BLOCKED checkpoint must match story ID/path, plan revision,
source revisions, baseline/current target revisions, planned/actual write sets, test
evidence or error, and safe resume point. revalidate every claimed-current path. It
is valid only while story and tracker both remain IN_PROGRESS; then report
`RECOVERY_CHECKPOINT` without changing story status. Any mismatch, malformed
revision, or unresolved checkpoint with IN_REVIEW is `DATA_CONFLICT`.

For IN_REVIEW, validate recorded plan revision, implementation/evidence post-write
revisions, test command/exit code, and log revision. Missing or failing evidence is
`DATA_CONFLICT`. IN_REVIEW always contributes zero completed estimate.

## Phase 6 — Load one project-owned status configuration

Read exactly `production/config/sprint-status.yaml`. It must implement
`cgs.sprint-status-config/v1`, remain within fixed bounds, and declare:

- config revision/update time and raw self-independent content revision when used by
  the project convention;
- `stale_after_days`, `stale_day_basis`, timezone, and any required working-day
  calendar path/revision;
- priority weights for Must Have, Should Have, and Could Have;
- schedule-lag threshold in basis points;
- Must-Have time-remaining trigger in basis points; and
- the supported estimate unit matching the sprint plan.

Record path, revision, declared revision, and every effective value in the report. The
skill and its spec never carry a competing 2-day or 4-day constant. Missing,
malformed, unsupported, or incompatible configuration sets
`data_status: PARTIAL`, the affected staleness/weighted inputs to UNKNOWN, and
`health_status: UNKNOWN`; do not invent defaults.

## Phase 7 — Compute configured staleness

Use only an explicit story/tracker status-update timestamp, the run's recorded
`as_of` instant, and the configured timezone/day basis/calendar. Never use file
mtime as an update proxy.

For every IN_PROGRESS story:

- elapsed days greater than `stale_after_days` → `STALE`;
- elapsed days less than or equal to it → `FRESH`;
- missing/invalid timestamp or unusable calendar → `UNKNOWN`.

Other lifecycle states are `NOT_APPLICABLE`. Show the threshold and calculation
operands with each stale finding. Unknown freshness is a data-quality warning and
forces unknown health only when the health algorithm requires that story's
freshness.

## Phase 8 — Compute estimate-, priority-, and DAG-aware signals

Use only validated story status, priority, non-negative integer estimate in one
declared unit, and a validated acyclic dependency graph.

Compute and show:

- known-status coverage and known-estimate coverage;
- raw estimate totals by lifecycle state and priority;
- priority-weighted planned and DONE estimate;
- weighted completion basis points;
- time consumed/remaining basis points from explicit dates/timezone;
- schedule lag and `AHEAD|WITHIN_TOLERANCE|LAGGING` signal using the configured
  threshold;
- remaining-estimate critical path via deterministic DAG dynamic programming;
- blocked/stale/unknown nodes on that critical path; and
- incomplete Must-Have estimate and dependency-blocked downstream estimate.

Do not substitute story counts for estimates, treat UNKNOWN as NOT_STARTED,
count IN_REVIEW as complete, mix estimate units, assign a default priority,
invent dependency edges, or treat an off-path file as progress.

These are rough directional signals from declared estimates and status—not
delivery forecasts. Preserve the estimate uncertainty/coverage and identify the
critical path/tie rule used.

## Phase 9 — Derive one health enum

Apply the first matching rule:

1. unresolved identity/revision/revision/status/checkpoint conflict →
   `data_status: DATA_CONFLICT`, `health_status: UNKNOWN`, with no derived health;
2. required plan/config/date/status/estimate/priority/DAG/staleness input missing
   or invalid → `health_status: UNKNOWN` with exact missing-field IDs;
3. one or more verified BLOCKED stories lie on the deterministic remaining
   critical path → `health_status: BLOCKED`;
4. any verified blocked story off the critical path, stale critical-path story,
   configured schedule lag, or incomplete Must-Have estimate at/below the
   configured time-remaining trigger → `health_status: AT_RISK`;
5. otherwise → `health_status: ON_TRACK`.

Record `health_rule_id`, exact input tuple, configuration revision/revision, and
limitations. `BLOCKED` means a confirmed blocked critical path, not a data
conflict or generic lateness. ON_TRACK is prohibited when any required health
input is unknown.

## Phase 10 — Return a bounded snapshot and stop

Return `cgs.sprint-status-run/v2` with:

- normalized invocation, selector/plan identity, `as_of`, and source revisions;
- run/data/health statuses and derivation rule;
- plan/tracker/config revisions and story-set revision;
- source coverage, UNKNOWN/MISSING counts, conflict list, and recovery evidence;
- status/estimate/priority/critical-path/staleness metrics and all operands;
- effective configured thresholds, units, timezone, and limitations;
- a bounded attention table ordered by severity, priority, then story ID; and
- at most one evidence-bound recommendation with an owner or `UNKNOWN`.

Use the fixed summary/attention-row limits in the rules reference. Counts always
cover the complete validated story set; a displayed subset reports `shown/total`
and a deterministic continuation cursor. Never create an attachment or project
file.

Before returning, revalidate every source. State the validation boundary: this run
inspected declared artifacts and computed a rough signal; it did not run tests,
inspect implementation slugs, modify status/scope, invoke a gate/workflow, or
prove future delivery. Stop.
