---
name: bug-triage
description: "Builds a bounded read-only snapshot of canonical open bugs, separating severity evidence, product decisions, capacity proposals, trends, and committed registry transactions."
---

## Read-only contract and invocation

Invoke exactly one mode:

```text
$bug-triage full
$bug-triage sprint
$bug-triage trend --window <sprint-window-id>
```

Contract version: `cgs.bug-triage/v2`.

This skill is strictly read-only. It returns a hash-bound snapshot and proposals
in conversation. It never creates or edits a bug, report, sprint, capacity,
priority, disposition, waiver, risk, registry, issue, tracker, or session-state
artifact; never closes, merges, assigns, defers, accepts, or fixes a bug; and
never invokes another workflow. A proposal is not a decision or transaction.

Reject missing mode, unknown mode, multiple modes, paths, extra positional
arguments, duplicate or unknown options, option values beginning with `--`, and
`--window` outside `trend`. `trend` requires one stable lowercase-kebab sprint
window ID and consumes it exactly once. Invalid invocation returns
`operation_status: BLOCKED`, `backlog_health: UNKNOWN`,
`mutation_status: READ_ONLY_NO_CHANGES`, no snapshot/evidence record, and stops
before reading project artifacts.

---

## Phase 0: Freeze governance, policy, and fixed bounds

Resolve the repository root. Load every applicable `AGENTS.md` from the root to
each selected artifact in root-to-target order and list them in output. The
canonical registry root is exactly `production/qa/bugs/`; its direct-child
Markdown files are canonical bug records. Never recursively scan, follow a
symlink, or fall back to `production/bugs/`, QA-plan/playtest/soak tables, prior
triage output, issue text, filenames, or “latest” artifacts.

Require policy `production/qa/triage-policy.yaml` with schema
`cgs.bug-triage-policy/v1`, exact version/hash, canonical severity definitions,
evidence-to-recommendation rules, priority-recommendation rules, duplicate
normalization/thresholds, stable sorting, estimate-unit rules, and health mapping.
Prose elsewhere cannot override it. A missing/malformed/hash-inconsistent policy
blocks conclusions; do not invent common severity or capacity rules.

These fixed limits cannot be raised by policy or project input:

| Resource | Fixed maximum |
|---|---:|
| Direct canonical bug files | 10,000 |
| Bytes per bug record | 1 MiB |
| Aggregate canonical bug bytes | 256 MiB |
| Status-history events | 100,000 |
| Sprint-history entries | 256 |
| Evidence references per bug | 1,024 |
| Duplicate candidate pairs | 100,000 |
| Stable findings | 4,096 |
| Rows rendered per section | 500 |
| Policy, sprint status, sprint plan, sprint history, or receipt | 1 MiB each |

Enumerate normalized repository-relative paths in ordinal order. If discovery,
aggregate bytes, history, pair generation, findings, or rendering exceeds a
limit, stop at the stated lexical/stable-ID boundary. Record the complete
candidate-name digest, included/omitted counts, boundary key, and omitted-tail
digest and return `operation_status: PARTIAL_TRIAGE`, snapshot coverage
`PARTIAL — BOUNDED REGISTRY`, and `backlog_health: UNKNOWN`. Never sample the
omitted tail or infer a healthy/empty backlog.

Read selected configuration artifacts in full and compute SHA-256 from exact raw
bytes before parsing. Recompute every selected hash immediately before output. If
anything changes, return `BLOCKED — INPUT CHANGED DURING TRIAGE` without findings,
health, proposals, or evidence.

---

## Phase 1: Load only canonical records and filter by canonical status

If the registry root is missing, return `BLOCKED`, name the expected root, and do
not report zero bugs. If it exists and has no direct-child Markdown records, a
complete scan may return `TRIAGED` and `NO_OPEN_BUGS`.

Each record requires the producer schema `cgs-bug-record/v2` and:

- unique stable `BUG-[0-9]{4,}` ID, title, system ID, owner or `UNASSIGNED`;
- canonical status, severity, reported UTC, last-transition event ID/UTC;
- build ID/artifact SHA-256/source commit and platform-profile ID/hash;
- numbered reproduction steps, expected result, actual result, frequency or
  `UNKNOWN`, and evidence receipt IDs/hashes;

The dotted legacy spelling `cgs.bug-record/v2`, an absent schema, or any other
schema is unsupported and makes that record malformed. Never normalize schema
punctuation or infer producer compatibility from matching fields.
- immutable status-history event list with event ID, from/to state, UTC, owner,
  reason, and transaction ID or `NONE`;
- estimate value/unit/source receipt or explicit `UNKNOWN`;
- observed priority decision and disposition decision or `NONE`, each with owner,
  authority, UTC, snapshot/preimage hashes, and transaction ID when present; and
- linked sprint transaction and risk-waiver identity or `NONE`.

Canonical statuses are exactly:

- unresolved: `Open`, `Reopened`;
- verification queue: `Fixed Pending Verification`;
- closed: `Verified Fixed`, `Closed`.

`DEFERRED`, `WONT_FIX_CANDIDATE`, and `ACCEPTED_RISK` are dispositions, not status
aliases. Missing/unknown status is malformed and excluded from health counts.
Only `Open` and `Reopened` enter the triage backlog. Keep verification/closed
counts separately; never reclassify a fallback table row as a bug.

For every discovered file record normalized path, raw SHA-256, byte count, parse
state, stable bug ID or `NONE`, and canonical status or `NONE`. Track exact counts
for `discovered`, `loaded`, `failed`, `duplicate_id`, `oversized`, `omitted`,
`unresolved`, `verification_queue`, and `closed`. An unreadable, malformed,
oversized, duplicate-ID, hash-changed, or omitted canonical record sets snapshot
coverage PARTIAL and `operation_status: PARTIAL_TRIAGE`; list every path/reason.
The loaded subset can never represent the whole backlog or produce health other
than `UNKNOWN`.

Noncanonical bug-like evidence explicitly supplied in conversation is listed
only as `UNREGISTERED CANDIDATE` with its source identity when safe; it is excluded
from counts, severity, trends, duplicates, and health, and no bug is created.

Compute `registry_snapshot_sha256` over UTF-8 canonical JSON containing contract/
policy identities, ordered discovery rows, exact counters, and later sprint/
history context. Use sorted object keys, preserved ordered arrays, JSON number
grammar, and no insignificant whitespace.

---

## Phase 2: Resolve the active sprint from authority, never recency

Only `sprint` mode loads active-sprint context. Read the exact raw bytes and
SHA-256 of `production/sprint-status.yaml`, then dispatch only by its explicit
top-level schema through one of these versioned read-only adapters:

1. `cgs.sprint-tracker/v2` (canonical producer): require positive
   `tracker_revision`, stable `event_id`, equal `sprint_id` and
   `active_sprint_id`, exact `sprint_state: ACTIVE`, stable `lifecycle_owner`,
   exact `lifecycle_recorder: cgs.sprint-tracker/v2`, `plan_file`, exact raw
   `plan_sha256`, `plan_revision`, `story_set_hash`, `updated_at`, `start_date`,
   `end_date`, IANA `timezone`, `estimate_unit`, complete `stories[]`, and the
   typed capacity object: `receipt_id`, `receipt_path`, positive
   `receipt_revision`, exact raw `receipt_sha256`, exact `unit`, and integer
   `total`, `committed`, `reserved`, `released`, and `remaining`.
2. `cgs.sprint-status/v2` (explicit legacy adapter): require its declared
   revision/event identity and the same normalized active-sprint, exact plan
   path/raw hash/revision/story-set binding, date/timezone/unit, capacity-receipt
   identity/operands, and complete story-set fields. Missing any normalized field
   is unsupported; the adapter never invents it from prose or a plan filename.

Both adapters emit the same immutable in-memory authority record containing
source schema, tracker/status revision, raw source SHA-256, active sprint
ID/state, lifecycle owner/recorder, plan path/raw hash/revision/story-set hash,
start/end/timezone/unit, capacity receipt ID/path/revision/raw hash/unit and
operands, stories hash, update time, and last transaction/event ID. Any absent,
unknown, unversioned, duplicate-key, or malformed schema is
`UNSUPPORTED_SPRINT_SCHEMA`: set active sprint unresolved and capacity unknown;
never try the other adapter heuristically.

When `production/session-state/active.md` exists, read its stable active-sprint
field as corroboration. Each source may declare exactly one active sprint ID. All
present declarations must agree. Re-read and raw-hash the referenced
`cgs.sprint-plan/v2`; validate exact schema, ID, raw bytes against
`plan_sha256`, plan revision, story-set hash, dates/timezone/unit, stable story
join, and typed capacity object against
the normalized authority record.

Missing, duplicate, conflicting, dangling, inactive, out-of-window, or hash-
mismatched authority sets `active_sprint_status: UNRESOLVED`, keeps all bugs
unassigned, and makes operation at least `PARTIAL_TRIAGE`. Never inspect mtimes,
filename order, Git recency, or historical plans to choose another sprint.

Capacity is `VERIFIED` only when plan, normalized sprint adapter, and the exact
raw-hashed capacity receipt agree on sprint ID/hashes, receipt
ID/path/revision/hash, one exact estimate unit, total, committed, reserved,
completed/released amount, and remaining, with:

```text
remaining = total - committed - reserved + released
```

All values must be finite nonnegative integers and the recomputed remaining must
equal the declared value. Mixed units, missing estimates, negative or inconsistent
values, stale source hashes, or one-sided transactions yield
`capacity_status: UNKNOWN` and no active-sprint assignment proposal.

`full` and `trend` do not resolve or simulate active capacity. Their
`active_sprint_status` and `capacity_status` are `NOT_REQUESTED` and their
assignment state is respectively `PROPOSALS_ONLY` for backlog/next-sprint
planning or `NOT_APPLICABLE` for trends.

---

## Phase 3: Validate reproduction, severity, priority, and disposition

### Reproduction evidence

Tag `NEEDS_REPRO_INFO` when any required numbered step, expected result, actual
result, build identity, platform profile, or evidence receipt is absent, empty,
placeholder, malformed, or hash-invalid. Report each missing field. Keep the bug
visible, but do not invent content or use incomplete reproduction as confirmed
impact evidence.

### Severity evidence and recommendation

Preserve valid canonical `S1-Critical`, `S2-Major`, `S3-Minor`, or `S4-Trivial`
as `severity_observed`. Textual `CRITICAL/HIGH/MEDIUM/LOW`, missing, or unsupported
values become `NEEDS_TRIAGE_DATA`; never silently convert them.

An optional `severity_recommendation` is separate and must include policy rule ID,
recommended S1-S4 value, raw impact facts, exact evidence receipt IDs/hashes and
record locations, contradictions, limitations, rationale, and confidence
`LOW|MEDIUM|HIGH` computed by the policy's declared evidence-coverage rule. If the
rule inputs are missing or conflict, recommendation is `NEEDS_TRIAGE_DATA` and
confidence `NONE`. The model may not upgrade confidence by intuition or turn a
recommendation into observed severity.

### Product priority

Report canonical product priority decision as `priority_decision` only when its
owner/authority, decision UTC, affected bug ID, source snapshot hash, reason, and
transaction ID all validate. Otherwise it is `UNDECIDED` or
`INVALID_PRIORITY_DECISION`.

Return a distinct advisory `priority_recommendation` of `P1`, `P2`, `P3`, or
`NEEDS_TRIAGE_DATA`, with policy rule/evidence/rationale. No recommendation is a
human decision. `P4` is unsupported and cannot mean deferred, Won't Fix, or
accepted risk. Product-owner choice and recorder transaction remain separate.

### Disposition and risk

- `DEFERRED` is a scheduling decision that leaves canonical status unresolved;
- `WONT_FIX_CANDIDATE` is an undecided proposal, never closure or waiver; and
- `ACCEPTED_RISK` is valid only with exact product-owner identity/authority,
  affected bug/scope, reason, decision UTC, expiry or review UTC, source snapshot
  and preimage hashes, and a recorder transaction referenced consistently by all
  affected canonical records.

Missing/inconsistent fields produce `INVALID_ACCEPTED_RISK_CLAIM` and
`NEEDS_PRODUCT_DECISION`. An expired waiver is `EXPIRED_ACCEPTED_RISK` and does
not suppress health risk. Conversation cannot create or renew any disposition.

---

## Phase 4: Detect deterministic duplicate candidates without merging

For records with sufficient reproduction identity, compute a normalized symptom
fingerprint using the policy's versioned normalization over system ID, canonical
symptom code, affected operation/task, expected/actual outcome codes, platform
scope, and build lineage. Exact fingerprints form a strong duplicate candidate.

The policy may additionally define token normalization and a Jaccard threshold
for title/reproduction similarity. Calculate intersection/union over the exact
normalized token sets and compare raw precision. A fuzzy candidate requires same
system and compatible build/platform/severity scopes. Missing required fields
means `DUPLICATE_DATA_INSUFFICIENT`, not a match.

Each candidate has stable pair ID, ordered two bug IDs, match method, policy rule,
fingerprints, score/threshold or `NONE`, shared/differing evidence, and confidence.
Classify every qualifying pair exactly as `POSSIBLE_DUPLICATE`; nonqualifying or
insufficient pairs receive no duplicate state.
Never choose a survivor, merge, close, delete, rewrite, or exclude either bug.
Cap pairs before rendering under Phase 0 and make overflow partial.

---

## Phase 5: Simulate capacity proposals deterministically

In `sprint` mode, first exclude already committed bugs only when bug, sprint plan,
sprint status, and capacity receipt share one transaction ID and consistent unit/
delta. A one-sided or mismatched commitment is `INCONSISTENT_TRANSACTION`, remains
visible/unassigned, and forces partial triage.

Order remaining unresolved bugs by:

1. valid canonical priority decision `P1`, `P2`, `P3`, then undecided;
2. verified severity S1 through S4, then `NEEDS_TRIAGE_DATA`;
3. verified critical-path/regression blocker before non-blocker;
4. reported UTC oldest first; and
5. bug ID lexical order.

This order is for simulation, not an authoritative product priority. Starting
with verified remaining capacity, process each bug once:

- unknown/mixed-unit estimate: `UNASSIGNED_CAPACITY_UNKNOWN`;
- estimate less than or equal to provisional remaining:
  `PROPOSED:<active-sprint-id>`, then subtract it from provisional remaining;
- estimate above provisional remaining: `UNASSIGNED_CAPACITY_OVERFLOW`, with
  requested/provisional/overflow values.

Never reset provisional remaining per bug, exceed zero, displace committed scope,
split an indivisible estimate, or label overflow assigned. Report initial and
final provisional capacity plus an ordered allocation ledger. Canonical capacity
does not change.

In `full`, use only `PROPOSED:NEXT_SPRINT`, `PROPOSED:BACKLOG`, or
`UNASSIGNED_NEEDS_DECISION` with required estimate units; do not claim active
capacity. In `trend`, emit no assignment fields.

---

## Phase 6: Calculate history-bound trends

Only `trend --window <id>` loads `production/sprints/history.yaml` with schema
`cgs.sprint-history/v1`. Resolve exactly one immutable entry with the requested
stable ID, start/end UTC, ordered predecessor/successor IDs, plan/status hashes,
and history receipt. Duplicate, missing, overlapping, unordered, hash-mismatched,
or open-ended windows make trend coverage partial; do not substitute calendar
dates or active sprint.

For each valid canonical bug history:

- `opened_in_window` requires an immutable Open/Reopened event within `[start,end)`;
- `closed_in_window` requires a Verified Fixed/Closed event within `[start,end)`;
- `net_change = opened_in_window - closed_in_window`;
- sprint age requires the bug's first open event and ordered history entries; and
- regressions/hot spots require policy-defined event/system identities and only
  loaded valid records in the exact window.

Missing event UTC, transition, history entry, or receipt makes the affected metric
`UNKNOWN` with exact reason and makes `trend_status: PARTIAL`. Never derive closed
time from mtime/current status or age from filename/current sprint count.

Threshold patterns are `OBSERVATION` records with numerator, denominator, window,
policy rule, and uncertainty/coverage limitation. They are not systemic causes,
priority decisions, or automatic actions.

---

## Phase 7: Derive stable findings and backlog health

Create findings only for data, reproduction, severity, duplicate, transaction,
capacity, history, or risk facts:

```yaml
id: BTF-<category-slug>-<12-lowercase-hex>
category: DATA | REPRO | SEVERITY | DUPLICATE | TRANSACTION | CAPACITY | HISTORY | RISK
bug_ids: [<sorted stable IDs>]
sprint_or_window_id: <stable ID or NONE>
policy_rule_id: <stable ID or NONE>
state: OBSERVED
evidence:
  registry_snapshot_sha256: <hash>
  source_paths_and_hashes: [<identities>]
claim_boundary: <fact, recommendation, or limitation>
owner_handoff: <role or NONE>
```

Compute the suffix from SHA-256 of UTF-8 canonical JSON containing repository
identity, category, sorted bug IDs, sprint/window ID, policy rule ID, and stable
transaction/waiver/pair ID or `NONE`. Exclude paths, titles, descriptions,
observed values, severity/priority recommendations, confidence, status,
timestamps, current snapshot/report hashes, and owner names. Coalesce identical
identities, preserve all evidence, and sort by category then ID.

Apply backlog health in this exact order:

1. `UNKNOWN` for `PARTIAL_TRIAGE`, incomplete bounded registry, invalid policy,
   unresolved required authority, or incomplete health evidence;
2. `NO_OPEN_BUGS` only for a complete canonical snapshot with zero unresolved;
3. `CRITICAL_RISK` for a verified open S1 or verified required critical-path
   blocker;
4. `AT_RISK` for verified open S2, P1 recommendation, capacity overflow,
   inconsistent transaction, invalid/expired risk claim, or unresolved regression;
5. `NO_CRITICAL_FINDINGS` otherwise.

This is bug-snapshot health only. Never say build healthy, safe to ship, release
ready, QA ready, or risk accepted from this workflow.

---

## Phase 8: Return snapshot, truth table, and recorder handoff

Return headings exactly once in order:

1. `Result Axes`
2. `Registry, Policy, and Snapshot Identity`
3. `Load Coverage and Omissions`
4. `Canonical Open Bugs`
5. `Reproduction Gaps`
6. `Severity Evidence and Recommendations`
7. `Priority and Disposition Decisions`
8. `Duplicate Candidates`
9. `Active Sprint and Capacity`
10. `Assignment Proposals`
11. `History-Bound Trends`
12. `Backlog Health`
13. `Stable Findings`
14. `Decision and Recorder Handoffs`
15. `Evidence Record`

Use these exact secondary-axis vocabularies:

- `active_sprint_status`: `NOT_REQUESTED`, `NOT_EVALUATED`, `ACTIVE`, or
  `UNRESOLVED`;
- `capacity_status`: `NOT_REQUESTED`, `NOT_EVALUATED`, `VERIFIED`, or `UNKNOWN`;
- `trend_status`: `NOT_REQUESTED`, `NOT_EVALUATED`, `COMPLETE`, or `PARTIAL`;
- `assignment_state`: `PROPOSALS_ONLY`, `NOT_APPLICABLE`, or `UNKNOWN`.

Use this truth table; no branch may omit an axis:

| Condition | operation_status | backlog_health | snapshot_coverage | active_sprint_status | capacity_status | trend_status | assignment_state | mutation_status |
|---|---|---|---|---|---|---|---|---|
| Invalid invocation or missing registry/policy | `BLOCKED` | `UNKNOWN` | `NONE` | `NOT_EVALUATED` | `NOT_EVALUATED` | `NOT_EVALUATED` | `UNKNOWN` | `READ_ONLY_NO_CHANGES` |
| Complete empty registry in `full` | `TRIAGED` | `NO_OPEN_BUGS` | `COMPLETE` | `NOT_REQUESTED` | `NOT_REQUESTED` | `NOT_REQUESTED` | `NOT_APPLICABLE` | `READ_ONLY_NO_CHANGES` |
| Complete empty registry in `sprint` | `TRIAGED` | `NO_OPEN_BUGS` | `COMPLETE` | `NOT_EVALUATED` | `NOT_EVALUATED` | `NOT_REQUESTED` | `NOT_APPLICABLE` | `READ_ONLY_NO_CHANGES` |
| Complete empty registry and valid window in `trend` | `TRIAGED` | `NO_OPEN_BUGS` | `COMPLETE` | `NOT_REQUESTED` | `NOT_REQUESTED` | `COMPLETE` | `NOT_APPLICABLE` | `READ_ONLY_NO_CHANGES` |
| Complete nonempty `full` | `TRIAGED` | Phase 7 result | `COMPLETE` | `NOT_REQUESTED` | `NOT_REQUESTED` | `NOT_REQUESTED` | `PROPOSALS_ONLY` | `READ_ONLY_NO_CHANGES` |
| Complete nonempty `sprint` with verified authority/capacity | `TRIAGED` | Phase 7 result | `COMPLETE` | `ACTIVE` | `VERIFIED` | `NOT_REQUESTED` | `PROPOSALS_ONLY` | `READ_ONLY_NO_CHANGES` |
| Complete registry but unresolved sprint authority | `PARTIAL_TRIAGE` | `UNKNOWN` | `PARTIAL` | `UNRESOLVED` | `NOT_EVALUATED` | `NOT_REQUESTED` | `UNKNOWN` | `READ_ONLY_NO_CHANGES` |
| Complete registry and active sprint but invalid capacity | `PARTIAL_TRIAGE` | `UNKNOWN` | `PARTIAL` | `ACTIVE` | `UNKNOWN` | `NOT_REQUESTED` | `UNKNOWN` | `READ_ONLY_NO_CHANGES` |
| Complete `trend` with valid window/history | `TRIAGED` | Phase 7 result | `COMPLETE` | `NOT_REQUESTED` | `NOT_REQUESTED` | `COMPLETE` | `NOT_APPLICABLE` | `READ_ONLY_NO_CHANGES` |
| Complete registry but invalid/incomplete trend history | `PARTIAL_TRIAGE` | `UNKNOWN` | `PARTIAL` | `NOT_REQUESTED` | `NOT_REQUESTED` | `PARTIAL` | `NOT_APPLICABLE` | `READ_ONLY_NO_CHANGES` |
| Any failed/duplicate/malformed/omitted/bounded registry record | `PARTIAL_TRIAGE` | `UNKNOWN` | `PARTIAL` | `NOT_EVALUATED` | `NOT_EVALUATED` | `NOT_EVALUATED` | `UNKNOWN` | `READ_ONLY_NO_CHANGES` |
| Input changes during run | `BLOCKED` | `UNKNOWN` | `INVALIDATED` | `NOT_EVALUATED` | `NOT_EVALUATED` | `NOT_EVALUATED` | `UNKNOWN` | `READ_ONLY_NO_CHANGES` |

Also report exact load
counters, initial/final provisional capacity, and proposal/unknown counts. Sort
open bugs by Phase 5 order and all other rows by stable IDs.

The snapshot payload schema is `cgs.bug-triage-snapshot/v2`. Canonicalize with
sorted object keys and preserved ordered arrays. Include contract/policy/source/
sprint/history identities, limits, counters, coverage, open records, evidence and
recommendations, duplicates, capacity ledger, trends, health, findings, all result
axes, producer `bug-triage@cgs.bug-triage/v2`, UUIDv4 run ID, and RFC 3339 UTC.

For every non-blocked snapshot, emit one `cgs.review-evidence/v1` record bound to
the payload hash, exact source identities, finding IDs, coverage, health, producer,
run/time, and:

```yaml
artifact_kind: bug-triage-snapshot
persistence: NONE
authoritative_registry_change: false
decision_authority: NONE
gate_evidence_candidate: false
mutation_status: READ_ONLY_NO_CHANGES
```

Partial evidence proves only included facts and omissions; it cannot support a
healthy backlog or transaction.

When a product/QA/sprint owner wants to apply a priority, assignment, deferral,
Won't Fix, or risk decision, return a
`cgs.bug-triage-transaction-proposal/v1` candidate with proposal/snapshot IDs,
decision owner/authority, affected bug IDs and exact preimage hashes, sprint plan/
status/capacity preimages, single estimate unit, capacity before/requested/after/
overflow, exact two-sided changes, risk scope/reason/time/expiry when applicable,
all-or-nothing rule, and intended transaction ID. This skill does not apply it.

Only a separately authorized recorder may validate all preimages and atomically
update bug and sprint/capacity records. Later triage recognizes commitment only
when every canonical side references one transaction ID and consistent delta.
End with `mutation_status: READ_ONLY_NO_CHANGES` and stop; do not persist the
snapshot or start another workflow.
