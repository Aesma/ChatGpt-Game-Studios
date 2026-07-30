# Continued Sprint Status Workflow

Execute these phases in order. Stop conditions are mandatory. Preserve a
read-only source ledger and never repair, reconcile, or write project state.

## Phase 0 — Parse and bound the request

1. Parse zero or one selector and normalize omitted input to `current`.
2. Validate selector grammar and reject path-like or extra input.
3. Record contract versions, fixed limits, `as_of` instant, and the permanent
   empty write set.
4. Record that review mode, director gates, write authorization, and downstream
   workflows are out of scope.

Invalid input stops with `run_status: ERROR`, zero sprint-evidence reads, and
zero project writes.

## Phase 1 — Resolve one stable sprint

1. Read bounded tracker/session selector sources when present.
2. Apply explicit → tracker active ID → session active ID/reference precedence.
3. Resolve one canonical plan and validate its declared sprint ID.
4. For current, cross-check all present active declarations for agreement.
5. Record selector values, paths, declared revisions, and resolution rule.

Missing or ambiguous resolution stops with `run_status: BLOCKED`,
`data_status: UNAVAILABLE`, `health_status: UNKNOWN`, no story reads, and one
request for a stable ID. Current-source disagreement is DATA_CONFLICT. Never use
mtime, filename order, or a guessed latest sprint.

## Phase 2 — Freeze plan and story-set identity

1. Apply plan/story/aggregate limits before parsing.
2. Validate plan schema, ID/revision/update time, dates/timezone, estimate unit,
   story IDs/paths, priorities, estimates, owners, and dependency IDs.
3. Read exact referenced story bytes or exact inline records; record missing
   paths without substituting status.
4. Build the deterministic story-set records/revision.
5. Validate the complete dependency graph and record all coverage gaps.

Identity, unsafe-path, or contradictory/cyclic graph data is fail-closed. Missing
health operands are retained as unknown; they are not zeros or backlog.

## Phase 3 — Validate or explicitly omit the tracker

1. Determine whether the tracker applies to the selected current/historical ID.
2. If applicable, validate schema, selected/active IDs, plan revision, story-set
   revision, update time, one-to-one story coverage, controlled statuses, and story
   projection agreement.
3. If a well-formed tracker names another sprint during an explicit historical
   query, mark it NOT_APPLICABLE and use fallback evidence.
4. If no applicable tracker exists, enter markdown fallback and record
   `data_status: PARTIAL`.

Any applicable tracker mismatch emits the exact DATA CONFLICT response and stops
before counts or health. Never bypass it with story markers.

## Phase 4 — Classify story evidence

1. Normalize only controlled tracker/story status spellings.
2. In fallback, an explicit Not Started marker alone becomes NOT_STARTED.
3. Classify no marker as UNKNOWN and a missing referenced file as MISSING.
4. Record known-status and missing/unknown coverage separately.
5. Exclude UNKNOWN/MISSING from DONE, backlog, weighted, Must-Have, schedule, and
   health denominators; any required such gap forces health UNKNOWN.

Do not scan `src/`, assets, build output, history, or filename slugs. No
implementation-looking path is a hint or progress input.

## Phase 5 — Validate recovery/review projections

1. Read only exact derived checkpoint paths that exist.
2. Validate checkpoint identity, plan/source/baseline/current revisions, write sets,
   test/error evidence, and resume point against raw bytes.
3. Require unresolved recovery and both status projections to remain IN_PROGRESS.
4. Validate IN_REVIEW post-write/test/log evidence and absence of unresolved work.

Any contradiction is DATA_CONFLICT and stops before derived counts or health. A
valid checkpoint is a recovery annotation only; IN_REVIEW is unfinished.

## Phase 6 — Validate the single project configuration

1. Read only `production/config/sprint-status.yaml` and apply its bound.
2. Validate `cgs.sprint-status-config/v1`, revision/time, stale value/day basis,
   timezone/calendar, priority weights, health thresholds, and estimate unit.
3. revision and record the configuration plus any exact calendar source.
4. Require estimate-unit compatibility with the plan.

Absent or malformed configuration produces stable data gaps, unknown dependent
calculations, and `health_status: UNKNOWN`. Do not substitute an embedded day or
weight threshold.

## Phase 7 — Compute explicit freshness

1. Freeze one as-of instant and use configured timezone/day basis/calendar.
2. For every IN_PROGRESS story, compute elapsed status days only from its
   explicit status-update timestamp.
3. Apply strict greater-than comparison with configured `stale_after_days`.
4. Emit threshold, operands, result, and stable finding for STALE/UNKNOWN.

Never use file mtime, commit time, or a session note as a status-update proxy.

## Phase 8 — Compute weighted and graph signals

1. Verify complete known story status, estimates, priorities, units, and DAG.
2. Compute estimate totals by state/priority and priority-weighted planned/DONE
   estimates.
3. Compute weighted completion, configured time consumed/remaining, schedule
   lag, and one schedule signal.
4. Use stable topological dynamic programming for remaining critical path and
   tie-node set.
5. Compute blocked/stale/unknown critical nodes, incomplete Must-Have estimate,
   and dependency-blocked downstream estimate.

If any required operand is unknown, preserve available metrics but do not fill
the gap or derive non-UNKNOWN health. Label every schedule calculation a rough
directional signal, not a forecast.

## Phase 9 — Derive one health result

1. Apply `SS-HEALTH-01..05` in order.
2. Record exact rule ID, input tuple, matching stable story/finding IDs, config
   revision/revision, estimate unit, and limitations.
3. Keep DATA_CONFLICT, critical-path BLOCKED, schedule LAGGING, and story BLOCKED
   in their distinct fields.
4. With absent dates or other required inputs, emit only
   `health_status: UNKNOWN` plus exact missing fields—never a list of possible
   verdicts.

## Phase 10 — Build bounded output

1. Assemble `cgs.sprint-status-run/v2` with provenance, coverage, config,
   thresholds, story/estimate/graph/staleness summaries, findings, health
   derivation, and validation limitations.
2. Sort attention rows deterministically; display up to 20 and provide
   `shown/total` plus the last-ID cursor when more exist.
3. Keep the primary summary within 50 rendered lines and make at most one sourced
   recommendation.
4. Create no attachment and request no write.

## Phase 11 — Revalidate and stop

1. Re-resolve and revalidate every inspected selector, plan, story, tracker,
   checkpoint, configuration, and calendar source.
2. If anything changed, discard derived counts/health and return DATA_CONFLICT
   with expected/observed revisions.
3. Confirm the empty write set, no gate/workflow invocation, and no mutation.
4. State that status/estimate inspection did not run tests, prove delivery,
   inspect implementation slugs, or alter project state. Stop.
