---
name: bug-triage
description: "Builds a read-only, evidence-backed snapshot of the canonical open-bug registry, separates severity evidence from priority and scheduling proposals, and never treats a proposed assignment or risk disposition as committed."
---

# Bug Triage

Invoke as `$bug-triage [sprint|full|trend]`.

The workflow is advisory and read-only. It reads canonical records, validates the
snapshot, and returns proposals in conversation. It never writes a triage report,
edits a bug, changes a sprint, reserves capacity, closes or merges an issue, or
records a risk waiver.

## Non-negotiable contract

1. The canonical bug registry is `production/qa/bugs/*.md`. Files elsewhere are not
   bug records unless a separately approved migration places them in that registry.
2. Read only canonical bug records with an unresolved status. Do not treat QA-plan
   tables, playtest notes, soak-test notes, or a generated triage table as a second
   registry.
3. Severity is observed evidence or an explicitly labeled recommendation. Priority,
   disposition, and schedule are separate decisions.
4. Every schedule value produced here is labeled `PROPOSED` or `UNASSIGNED`. A triage
   snapshot is not proof that a bug or sprint registry was updated.
5. `DEFERRED`, `WONT_FIX_CANDIDATE`, and `ACCEPTED_RISK` are distinct. Deferral is a
   schedule state, a Won't Fix entry is only a candidate, and accepted risk is valid
   only when a complete product-owner waiver already exists in canonical records.
6. Any unreadable, malformed, duplicate-ID, or incompletely loaded canonical record
   makes the operation `PARTIAL_TRIAGE`. Partial data can never support a healthy
   backlog conclusion.
7. Do not infer zero from missing data. Do not infer the active sprint from mtime or
   filename order.
8. No director gate and no authorization prompt applies because this workflow makes
   no file changes.

## Output statuses

Return these independent fields:

| Field | Allowed values |
|---|---|
| `operation_status` | `TRIAGED`, `PARTIAL_TRIAGE`, `BLOCKED` |
| `backlog_health` | `NO_OPEN_BUGS`, `CRITICAL_RISK`, `AT_RISK`, `NO_CRITICAL_FINDINGS`, `UNKNOWN` |
| `mutation_status` | always `READ_ONLY_NO_CHANGES` |
| `snapshot_sha256` | canonical snapshot hash or `null` |
| `active_sprint_id` | stable ID or `null` |
| `assignment_state` | `PROPOSALS_ONLY`, `NOT_APPLICABLE`, `UNKNOWN` |

`TRIAGED` means the requested read-only analysis completed. It does not mean bugs
were assigned, accepted, fixed, closed, or safe to ship.

## Phase 0: Parse arguments

Accept zero or one positional mode:

- `sprint`: analyze unresolved bugs against verified active-sprint scope and capacity,
  but return proposals only.
- `full`: analyze the entire unresolved canonical backlog; schedule suggestions remain
  proposals.
- `trend`: compute only evidence-supported trends; emit no schedule proposal.
- no argument: use `sprint` only when Phase 2 resolves one active sprint; otherwise
  use `full`.

Reject unknown modes, multiple positional modes, paths, and extra arguments with
`operation_status: BLOCKED`. Read nothing beyond argument validation and write
nothing.

## Phase 1: Load the canonical bug snapshot

Enumerate `production/qa/bugs/*.md` in normalized repository-relative path order.
Never fall back to:

- `production/bugs/`;
- `production/qa/bugs.md`;
- a `Bugs Found` table;
- a prior triage output; or
- any "most recent" file.

If the registry directory exists and is empty, return `operation_status: TRIAGED`,
`backlog_health: NO_OPEN_BUGS`, and `mutation_status: READ_ONLY_NO_CHANGES`. If the
registry directory is absent, return `BLOCKED` with the expected canonical path and
suggest `$bug-report`; do not claim that the project has zero bugs.

For every discovered file, record `path`, raw-byte SHA-256, parse result, and bug ID.
Track exact counts for `discovered`, `loaded`, `failed`, `duplicate_id`, `omitted`,
`unresolved`, `verification_queue`, and `closed`.

Required canonical fields are:

- `ID` matching `BUG-[0-9]{4,}`;
- `Title`;
- `Severity`;
- `Status`;
- `Reported`;
- `System`;
- `Build`;
- `Platform`;
- numbered reproduction steps;
- `Expected Result`;
- `Actual Result`.

Canonical severity values are:

| Severity | Meaning |
|---|---|
| `S1-Critical` | crash, data loss, security failure, or complete critical-path failure |
| `S2-Major` | major feature broken without total product failure |
| `S3-Minor` | degraded behavior with a viable workaround |
| `S4-Trivial` | cosmetic, typo, or negligible functional impact |

Do not convert `CRITICAL/HIGH/MEDIUM/LOW` silently. A legacy or absent severity becomes
`NEEDS_TRIAGE_DATA`; an evidence-backed replacement may appear only in
`severity_recommendation`, with rationale and confidence. It does not overwrite
`severity_observed`.

Classify canonical statuses exactly:

- unresolved backlog: `Open` or `Reopened`;
- verification queue: `Fixed Pending Verification`;
- closed scope: `Verified Fixed` or `Closed`;
- missing or unknown status: malformed and omitted from health metrics.

Load all files before producing counts. An unreadable file, malformed required
identity/status, duplicate bug ID, or omitted record sets
`operation_status: PARTIAL_TRIAGE`. List every failure; never report the loaded subset
as the whole backlog.

Compute `snapshot_sha256` over UTF-8 canonical JSON containing ordered entries
`(bug_id, normalized_path, raw_sha256, parse_state, canonical_status)`, followed by
the exact load counters. The same bytes and counters must produce the same hash.

## Phase 2: Resolve active sprint and capacity without timestamps

For `sprint` mode, or to select the no-argument default, read these authority files
when present:

- `production/session-state/active.md`;
- `production/sprint-status.yaml`.

Accept only explicit `Active Sprint ID: <id>` or `active_sprint_id: <id>` fields.
Every present authority may declare at most one value and all declarations must
agree. Validate the ID against the referenced sprint plan.

Missing, duplicate, conflicting, malformed, or dangling declarations produce
`active_sprint_id: null` and `assignment_state: UNKNOWN`. With an explicit `sprint`
mode, continue the read-only triage but all bugs stay `UNASSIGNED` and
`operation_status` is at least `PARTIAL_TRIAGE`. With no mode, select `full`. Never
select the most recently modified sprint.

Capacity is usable only when the active sprint plan and
`production/sprint-status.yaml` agree on:

- sprint ID and source revisions/hashes;
- one estimate unit, such as points or hours;
- committed amount;
- total capacity; and
- remaining amount, where `remaining = total - committed`.

Each bug must have an estimate in that same unit before it can receive a proposal.
Unknown, negative, inconsistent, or mixed-unit capacity keeps the bug
`UNASSIGNED_CAPACITY_UNKNOWN`. When proposed work exceeds remaining capacity, keep the
overflow `UNASSIGNED_CAPACITY_OVERFLOW`; never displace existing scope automatically.

Add the verified sprint context and capacity source hashes to the canonical snapshot
input and recompute `snapshot_sha256`.

## Phase 3: Validate and classify each unresolved bug

### Reproduction evidence

Tag a bug `NEEDS_REPRO_INFO` when any of these is absent, empty, or a placeholder:

- at least one numbered reproduction step;
- expected result;
- actual result;
- build;
- platform.

Keep the bug in the table. Missing repro data is not permission to invent it.

### Severity and priority

Preserve valid canonical severity as `severity_observed`. If severity is absent or
unsupported, use `NEEDS_TRIAGE_DATA`; an optional recommendation must cite observed
impact, source lines, rationale, and confidence.

Return `priority_recommendation` separately:

- `P1`: evidence shows it blocks QA/release, is an S1 regression, or blocks a required
  critical path;
- `P2`: verified major impact should be addressed before a named milestone;
- `P3`: non-blocking backlog candidate;
- `NEEDS_TRIAGE_DATA`: evidence is insufficient.

Priority remains a producer/QA-owner decision. Never rewrite the observed priority
field and never map `P4` to Won't Fix or accepted risk.

### Duplicate candidates

Normalize titles to lowercase alphanumeric tokens, remove punctuation and common
articles, and compute Jaccard token similarity. Mark two records
`POSSIBLE_DUPLICATE` only when they have the same canonical system and severity and
similarity is at least `0.50`. Record the score and cross-reference both bug IDs.
This is a candidate signal only: do not merge, delete, close, or choose a survivor.

### Scheduling proposals

In `sprint` and `full` modes, use a separate `assignment_proposal` field:

- `PROPOSED:<active-sprint-id>` only when active sprint, capacity, estimate unit, and
  remaining amount all verify;
- `PROPOSED:NEXT_SPRINT` only as a planning candidate with required units shown;
- `PROPOSED:BACKLOG`;
- `UNASSIGNED_CAPACITY_UNKNOWN`;
- `UNASSIGNED_CAPACITY_OVERFLOW`;
- `UNASSIGNED_NEEDS_DECISION`.

Never use bare `Assigned to`, `Target Sprint`, or language claiming an assignment was
applied. In `trend` mode, use `assignment_state: NOT_APPLICABLE` and omit proposals.

### Disposition and risk

Use these meanings without conflation:

- `DEFERRED`: a scheduling state. A proposal must read `PROPOSED: DEFERRED`; it does
  not close the bug and is not risk acceptance.
- `WONT_FIX_CANDIDATE`: an undecided product candidate. It is never a closure, waiver,
  or accepted risk.
- `ACCEPTED_RISK`: an existing canonical governance decision only.

Treat `ACCEPTED_RISK` as valid only when canonical records include product-owner
identity, precise scope/bug IDs, reason, decision timestamp, expiry or review date,
and the recorder transaction ID. Missing any field produces
`INVALID_ACCEPTED_RISK_CLAIM`; show `NEEDS_PRODUCT_DECISION` and do not count it as
accepted. A conversational user response cannot create `ACCEPTED_RISK` because this
workflow is read-only.

## Phase 4: Compute evidence-supported trends

Use an explicit window with stable sprint ID, start/end timestamps, and source hashes.

- `opened_in_window` requires each bug's immutable reported timestamp.
- `closed_in_window` requires canonical status history with a close event timestamp.
- `net_change = opened_in_window - closed_in_window`.
- Age in sprints requires an ordered, immutable sprint history and each bug's open
  event. Do not derive it from filenames or current status alone.
- Hot-spot and regression counts include only loaded, valid, in-scope records.

If any required event or boundary is missing, render that metric as `UNKNOWN` with the
missing source. Threshold observations such as three bugs in one system are labeled
`OBSERVATION`, include the window and denominator, and never become an automatic
product decision.

## Phase 5: Derive backlog health

Apply this order:

1. `UNKNOWN` when `operation_status: PARTIAL_TRIAGE` or required health evidence is
   incomplete.
2. `NO_OPEN_BUGS` when the canonical registry loaded completely and has zero
   unresolved records.
3. `CRITICAL_RISK` when a verified open S1 exists or a verified required critical
   path is blocked.
4. `AT_RISK` when verified open S2, P1 recommendation, capacity overflow, invalid risk
   claim, or unresolved regression exists.
5. `NO_CRITICAL_FINDINGS` otherwise.

Never say “build is healthy,” “safe to ship,” or “ready for QA” from bug-triage alone.
The field describes only the verified bug snapshot.

## Phase 6: Present the read-only triage snapshot

Return in conversation:

1. operation, backlog-health, mutation, assignment, snapshot, and active-sprint fields;
2. load counters and failures/omissions;
3. source paths and raw hashes;
4. unresolved bugs sorted by valid severity S1 through S4, then
   `NEEDS_TRIAGE_DATA`; within a group sort by reported timestamp oldest first and ID;
5. observed severity/priority/status separately from recommendations;
6. repro gaps and duplicate candidates;
7. assignment proposals or explicit unassigned reasons;
8. disposition/risk validation;
9. evidence-supported trends and `UNKNOWN` reasons;
10. systemic observations and recommended next actions.

Always end with `mutation_status: READ_ONLY_NO_CHANGES` and explicitly state that no
bug, sprint, capacity, status, waiver, or report file changed.

## Recorder handoff contract

If the user wants to apply a priority, assignment, deferral, Won't Fix, or accepted
risk decision, return a proposed recorder transaction in conversation; do not execute
it.

The transaction request must contain:

- proposal ID and `snapshot_sha256`;
- decision owner and authority;
- affected bug IDs and expected preimage SHA-256 for every canonical bug record;
- active sprint ID plus expected preimage SHA-256 for sprint plan and
  `production/sprint-status.yaml`;
- one estimate unit, capacity before, requested units, capacity after, and overflow;
- exact bug-registry changes and matching sprint-registry/capacity changes;
- for Won't Fix or accepted risk: scope, reason, decision timestamp, and expiry or
  review date;
- all-or-nothing rule and intended transaction ID.

A separately authorized sprint-owner/recorder must verify all preimages and apply the
bug and sprint sides atomically. If either side cannot update, neither side may
commit. A later triage may describe an assignment or accepted risk as committed only
when canonical bug and sprint records reference the same transaction ID and consistent
capacity delta. A one-sided or mismatched transaction is
`INCONSISTENT_TRANSACTION`, forces `PARTIAL_TRIAGE`, and cannot be repaired by the
derived snapshot.

Optional next actions may suggest `$bug-report` for a new canonical report or
`$hotfix` for a verified S1/S2 emergency. Do not invoke them automatically.
