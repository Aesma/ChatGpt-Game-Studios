---
name: retrospective
description: "Produces immutable, revision-bound sprint or milestone retrospectives whose metrics, causes, actions, owners, deadlines, and trends remain evidence-backed or explicitly UNKNOWN."
---

## Contract and exact invocation

Invoke exactly one target:

```text
$retrospective sprint:<sprint-id> [--run-id <retro-run-id>] [--persist]
$retrospective milestone:<milestone-id> [--run-id <retro-run-id>] [--persist]
```

Contract version: `cgs.retrospective/v2`.

`<sprint-id>` must be `sprint-<lowercase-kebab-or-digits>` and
`<milestone-id>` must be `milestone-<lowercase-kebab-or-digits>`. A run ID is
`retro-<UUIDv4>`. Without `--run-id`, generate one and report it before drafting;
`--persist` requires an explicit `--run-id` so a retry cannot silently create a
second artifact.

Reject missing/multiple targets, unprefixed names, ambiguous type, invalid IDs,
paths, URLs, globs, extra positional arguments, duplicate/unknown options, option
values beginning with `--`, or `--persist` without a run ID. Invalid invocation
returns `analysis_status: BLOCKED`, `persistence_status: NOT_ATTEMPTED`, no
artifact/evidence, and stops before reading project files.

This workflow creates only one immutable retrospective plus its latest-pointer
index when explicitly persisted. It never moves, renames, overwrites, archives,
or edits an earlier retrospective; never updates a sprint/milestone tracker or
action registry; and never invokes planning, a gate, another skill, task, or
external workflow. Suggestions after output are plain-text handoffs only.

Without `--persist`, the workflow is read-only and returns a complete draft in
conversation. `--persist` explicitly authorizes only the two-path transaction
defined in Phase 8; it authorizes no other mutation.

---

## Phase 0: Freeze governance, policy, and fixed bounds

Resolve the repository root and canonicalize selected paths. Load every
applicable `AGENTS.md` from root to target in root-to-target order and list them.
Require `production/retrospectives/policy.yaml` with schema
`cgs.retrospective-policy/v1`, exact version/revision, target source routes, metric
definitions, evidence-confidence rules, required core evidence, Git range rules,
scan protocol rules, report schema, and immutable index semantics. Prose does not
override executable policy.

Fixed limits cannot be raised by policy, target, or user input:

| Resource | Fixed maximum |
|---|---:|
| Plan, tracker/status, policy, index, prior report, or receipt | 1 MiB each |
| Explicit evidence artifacts | 1,024 |
| Aggregate evidence bytes | 256 MiB |
| Evidence-ledger rows | 10,000 |
| Target stories/tasks | 5,000 |
| Status/history events | 100,000 |
| In-period Git commits | 10,000 |
| Scan candidate files | 100,000 |
| Scan candidate bytes | 512 MiB |
| Metrics | 1,024 |
| Observations | 4,096 |
| Action proposals | 64 |
| Rows rendered per report section | 500 |
| Rendered report bytes | 2 MiB |

Reject a required configuration artifact above its per-file bound as BLOCKED.
When otherwise valid selected work exceeds an evidence, event, commit, scan,
metric, observation, action, row, or output bound, stop at declared source order
then stable identity. Record candidate-set reference ID, included/omitted counts,
boundary key, and omitted-tail reference ID; set `analysis_status: RETRO_PARTIAL` and
`data_quality: PARTIAL — BOUNDED EVIDENCE`. Never sample or extrapolate omitted
work or call a truncated trend complete.

revision every selected source from exact raw bytes before interpretation. Recompute
all source and target/index base revision immediately before output and before
persistence. Any change returns `BLOCKED — INPUT CHANGED DURING RETROSPECTIVE`;
do not persist a stale mixture.

---

## Phase 1: Resolve exactly one sprint or milestone

Resolve the target only through the policy's exact route:

- sprint plan: `production/sprints/<sprint-id>.md` plus
  `production/sprint-status.yaml`;
- milestone plan: `production/milestones/<milestone-id>.md` plus
  `production/milestone-status.yaml`.

The plan and status artifact each declare schema/version, exact target type/ID,
plan revision, plan raw revision, story/task-set revision, start/end UTC, and source
revision. The status also declares captured-at UTC, event-history receipt, and
one row per exact story/task identity.

Reject zero or multiple matching plans, wrong target type/ID, path collision,
duplicate authority rows, dangling status path, or a second plan claiming the
same identity as `BLOCKED — TARGET NOT UNIQUE`. Do not fuzzy-match display names,
select latest mtime, infer current sprint, or accept an unprefixed argument.

The target period is the plan's exact half-open interval `[start_utc, end_utc)`.
Missing/invalid boundaries make time-bound metrics UNKNOWN. A final status
snapshot is fresh only when `captured_at_utc >= end_utc`, not in the future, and
its plan revision and story/task-set revision equal the selected plan. An active
or pre-end status may support explicitly time-stamped observations but cannot
support final completion/variance/trend claims.

---

## Phase 2: Reconcile plan, tracker, and history revisions

Validate these equality keys before combining plan and status:

```text
target_type + target_id + plan_revision + plan_revision + story_or_task_set_revision
```

For every story/task, require the same stable ID and estimate unit/value in the
plan and status baseline, or an immutable scope-change event binding pre/post
story_set_revisions, owner, reason, UTC within the target period, and transaction ID.
Status, completion, carryover, blocker, bug, effort, and scope-change claims must
reference exact event IDs and source revision.

Any unequal key, unexplained added/removed/changed item, duplicated item, stale
snapshot, conflicting event, or mismatched source revision becomes
`DATA CONFLICT`. Preserve both claims and their evidence; never choose a side.
Set `analysis_status: RETRO_PARTIAL` and block every metric or conclusion whose
inputs touch the conflict. Unaffected local observations may remain supported.

Absent data is not a conflict and not zero. Mark its dependent field `UNKNOWN`.
Never fall back from a present but conflicting YAML tracker to Markdown scanning,
and never make the tracker authoritative for fields its schema does not own.

---

## Phase 3: Build a bounded evidence ledger before analysis

Create an in-memory ledger with stable source IDs. Each row contains source type,
normalized path or immutable conversation locator, exact revision, schema/version,
target/revision/story-set identity, event/commit/message range, covered time and
story/task scope, supported claims, exclusions, freshness, and conflicts.

Allowed source types are `PLAN`, `STATUS`, `EVENT_HISTORY`, `BUG_EVENT`,
`DELIVERY_RECEIPT`, `GIT_RANGE`, `SCAN_SNAPSHOT`, `PRIOR_RETRO`,
`ACTION_DECISION`, and `USER_CONFIRMED`. A user claim is evidence only when the
response is explicit, its exact UTF-8 text revision and conversation run/turn locator
are recorded, and the report labels it `USER_CONFIRMED`; it does not retroactively
change tracker bytes.

Every metric or factual claim has exactly one state:

- `OBSERVED`: directly stated by fresh, in-scope, nonconflicting evidence;
- `DERIVED`: deterministic formula over only supported inputs, with formula,
  units, and every source ID; or
- `UNKNOWN`: an input is absent, stale, conflicting, out of period, truncated, or
  incomparable; value is literally `UNKNOWN`, confidence `NONE`, with reason.

Observed/derived confidence `HIGH|MEDIUM|LOW` comes only from the policy's
evidence-coverage rule and lists its rule ID. Never estimate, interpolate, impute,
silently convert units, or replace UNKNOWN with zero/false/none/not-applicable.

---

## Phase 4: Calculate only evidence-supported metrics and causes

Classify planned, completed-as-planned, completed-with-change, carried, added,
removed, blocked, and unknown stories/tasks only from exact plan/event evidence.
Metrics obey their registered formulas and units:

- planned count/effort comes only from the selected plan revision;
- completed count comes only from fresh completion events or verified delivery
  receipts mapped to exact story/task IDs;
- completion rate is `completed_eligible / planned_eligible * 100` only when both
  sets and exclusion rules are fully known;
- actual effort requires an explicit effort record in the same unit;
- variance requires supported planned and actual values; if either is UNKNOWN,
  variance and estimation accuracy are UNKNOWN;
- bugs found/fixed require immutable in-period bug open/fix events mapped to the
  target; bug-like commit text and absence of records are not counts; and
- unplanned work requires a scope-change event or explicit confirmed statement.

Every number, percentage, delta, duration, rate, and qualitative trend cites
source IDs. Keep full precision for calculation and apply only policy display
rounding after decisions.

A cause, carryover reason, blocker resolution, prevention claim, trend
explanation, or responsibility statement is factual only when an in-scope event
record states it or a user/team explicitly confirms it. Otherwise write
`UNKNOWN — no in-scope event or explicit confirmation`. Timing, correlation,
commit messages, task category, owner identity, and general experience never
prove cause.

---

## Phase 5: Bound Git evidence to the exact target period

Never run a “last four weeks,” “latest 20,” latest tag, current branch, or mtime
fallback. The plan/status must bind repository identity, baseline commit,
terminal commit, branch/ref identity, and target start/end UTC.

Verify both commits exist in the same repository, baseline is an ancestor of
terminal under the policy's merge rule, and the range contains only commits
reachable in `baseline_exclusive..terminal_inclusive`. For each candidate retain
commit SHA, parent identity, committer UTC, and scope mapping. Count a commit only
when it is in that exact graph range, its committer UTC is within `[start,end)`,
and it satisfies the policy's declared target-scope rule. Report excluded commits
and reasons.

Missing/invalid boundaries, commits, ancestry, ref, timestamps, or scope mapping
makes the Commits metric `UNKNOWN`; Git output may appear only as out-of-scope
context. A commit count never proves completion, effort, bugs, or causation.

---

## Phase 6: Compare TODO/FIXME/HACK only under one scan protocol

The current scan produces a `cgs.retrospective-scan-snapshot/v1` record containing
stable scan protocol ID/version; scanner product/version/executable revision; exact
argv and match semantics; repository revision; included roots; excluded roots,
extensions, generated/vendor/binary rules; file-list reference ID; selected file/byte
counts; TODO/FIXME/HACK counts and stable occurrence IDs; start/end UTC; and any
omissions or errors.

Current counts may be OBSERVED only from a complete bounded scan. Trend against a
prior retrospective is DERIVED only when the prior report exposes a valid scan
snapshot with identical protocol ID/version, scanner version/revision, argv/match
semantics, include/exclude scope reference ID, and compatible repository lineage. The
formula is current minus prior for each marker.

Any scope/tool/version/argv/match/exclusion mismatch, missing prior snapshot,
unrelated repository lineage, partial scan, or unknown prior count makes trend
`UNKNOWN — INCOMPARABLE SCAN`; never compare current raw counts to prose or a
snapshot created under another protocol.

---

## Phase 7: Create observations and proposed actions without assigning people

Every observation has stable ID `ROBS-<category>-<12hex>`, type
`OBSERVATION|DATA_GAP|DATA_CONFLICT`, exact evidence IDs, fact/limitation, and
acceptance for additional evidence. Its revision identity uses repository, target
type/ID/revision, category, and stable evidence/event IDs—not paths, wording,
severity, timestamps, current report revision, or status.

Every action begins as `PROPOSED` with stable ID
`RACT-<category>-<12hex>`, triggering observation IDs, measurable action,
acceptance criteria, owner role candidate or `NONE`, due-window candidate or
`NONE`, and priority candidate or `NONE`. Limit to five top proposals by the
policy's deterministic evidence/impact order.

The model never selects a person, commits a deadline, or turns a candidate into a
team obligation. `owner` and `due` remain `UNASSIGNED` until an exact
`cgs.retrospective-action-decision/v1` receipt or explicit current user/team
confirmation binds action ID, chosen owner, due UTC/window, decision authority,
decision UTC, and the exact action-proposal-set revision shown for confirmation. A
missing/ambiguous response leaves the
proposal valid but unassigned. The report distinguishes `PROPOSED`, `CONFIRMED`,
`CARRIED`, `COMPLETED`, and `CANCELLED`; only external evidence advances state.

Never infer prior action completion from an unchecked box or its absence. A prior
retrospective is evidence that an action was proposed, not that it was performed.

---

## Phase 8: Produce and optionally persist immutable artifacts

The report payload schema is `cgs.retrospective-report/v2` and contains:

1. `Result and Data Quality`
2. `Target, Period, Revision, and Run Identity`
3. `Evidence Ledger`
4. `Plan/Status Reconciliation and Conflicts`
5. `Metrics`
6. `What Went Well`
7. `What Went Poorly`
8. `Blockers, Carryover, and Causes`
9. `Git Period Evidence`
10. `Comparable Scan Snapshot and Trend`
11. `Previous Action Follow-up`
12. `Stable Observations and Data Gaps`
13. `Proposed and Confirmed Actions`
14. `Bounded Omissions`
15. `Handoffs and Stop Boundary`

Canonicalize the machine payload as UTF-8 JSON with lexicographically sorted
object keys, preserved array order, JSON number grammar, and no insignificant
whitespace. Include contract/policy/source/target/revision/story-set/period/Git/
scan/prior-report identities; fixed limits; all metrics/evidence/conflicts/
observations/actions/omissions; producer `retrospective@cgs.retrospective/v2`;
UUIDv4 run ID; and RFC 3339 UTC generated time.

The rendered report bytes contain these fifteen sections plus the exact canonical
payload, but exclude the separate evidence record, any persistence/write receipt,
and the latest index. This makes report/payload/evidence revisions acyclic.

Return independent axes:

- `analysis_status`: `RETRO_COMPLETE`, `RETRO_PARTIAL`, or `BLOCKED`;
- `data_quality`: `COMPLETE`, `SUPPORTED_WITH_UNKNOWNS`,
  `PARTIAL — DATA CONFLICT`, `PARTIAL — STALE STATUS`,
  `PARTIAL — BOUNDED EVIDENCE`, or `NONE`;
- `persistence_status`: `NOT_REQUESTED`, `WRITTEN`, `UNCHANGED`, `CONFLICT`,
  `DECLINED`, or `FAILED`.

Optional unsupported metrics may be UNKNOWN with
`SUPPORTED_WITH_UNKNOWNS` without inventing values. A revision/story-set conflict,
stale final status, required core-evidence gap, or bounded omission makes
`RETRO_PARTIAL`. Persistence status never changes analysis/data-quality results.

For every nonblocked analysis, emit one `cgs.review-evidence/v1` record bound to
the payload revision, exact target/revision/story-set/period/source identities,
observation/action IDs, coverage, producer, run/time, and:

```yaml
artifact_kind: retrospective-report
persistence: NONE | VERIFIED_FILE
gate_evidence_candidate: false
planning_authority: NONE
action_assignment_authority: NONE
```

Return that record after the report, outside the report bytes. After verified
persistence it may additionally bind the report file revision and index revision;
neither persisted file embeds that post-write record.

The intended immutable report path is exactly:

```text
production/retrospectives/<sprint|milestone>/<target-id>/<retro-run-id>.md
```

The latest pointer is exactly:

```text
production/retrospectives/<sprint|milestone>/<target-id>/index.yaml
```

`index.yaml` uses schema `cgs.retrospective-index/v1` and records target identity,
latest run ID/path/report revision, analysis/data-quality states, generated UTC,
and previous index revision or `NONE`. It is navigation only, never metric or
action authority.

Without `--persist`, write nothing. With `--persist`, preview exact report and
index bytes, Revalidate every source and index preimage, and stage a two-path atomic
transaction. The report target must not exist. If it exists with byte-identical
content and the index already points to the same revision, perform no write and return
`UNCHANGED`; any other existing target is `CONFLICT`. Publish report and index
all-or-none, then read both back and return `WRITTEN` only when revisions match.
Failure preserves the old index and every existing report.

Never rename, move, archive, overwrite, or edit any older report. A new run always
uses a new run ID/path; “start fresh” means another immutable run, not historical
mutation. Resolve prior context only from a valid index/predecessor reference;
never rewrite old links.

After returning the draft or verified artifact/index paths and revisions, stop.
Do not invoke sprint planning, milestone review, gate checking, action tracking,
or any other workflow, and do not open another task.
