# Milestone Review Rules v1

This private contract is normative for `milestone-review`. It defines the
canonical inputs, limits, derivations, identities, and immutable-write protocol.
If this file conflicts with `SKILL.md`, stop with `run_status: ERROR`; do not
choose whichever rule is more permissive.

## Canonical values and serialization

- Text is UTF-8 without BOM and uses LF line endings.
- Paths are project-root-relative, slash-separated, Unicode NFC, and confined to
  the project after canonical resolution. Reject absolute paths, traversal,
  symlinks/reparse points escaping the project, device paths, and alternate data
  streams.
- Raw artifact hashes are lowercase hexadecimal SHA-256 over exact file bytes.
- Contract objects use canonical JSON: UTF-8, LF, no insignificant whitespace,
  object keys sorted by Unicode code point, arrays kept in declared order, JSON
  strings escaped by the JSON grammar, integers in base ten, and no floats,
  NaN, Infinity, duplicate keys, comments, or trailing commas.
- A percentage is the unreduced rational pair `numerator/denominator` plus a
  display value rounded half-up to two decimal places. Decisions use the pair,
  never the display value.
- Timestamps are explicit UTC `YYYY-MM-DDTHH:MM:SSZ`; dates are `YYYY-MM-DD`.
- Stable IDs are compared byte-for-byte after schema validation. Do not trim,
  case-fold, or repair an ID.

`source_snapshot_sha256` is SHA-256 over canonical JSON for the ordered evidence
ledger. `evidence_draft_sha256`, producer `result_sha256`, scope-decision hashes,
and `report_candidate_sha256` are hashes over their exact canonical bytes. A
hash never stands in for schema, revision, build, or scope validation.

## Fixed bounds

Apply these limits before parsing untrusted or project-authored content:

| Object | Maximum |
|---|---:|
| Evidence manifest bytes | 1 MiB |
| Milestone bytes | 2 MiB |
| One referenced source | 8 MiB |
| Referenced source rows | 512 |
| Aggregate referenced bytes | 64 MiB |
| Sprint IDs/reports | 64 |
| Milestone scope items | 10,000 |
| Acceptance criteria | 20,000 |
| Bug records | 20,000 |
| Test result records | 50,000 |
| Performance reports/scenarios | 64 / 2,000 |
| Risk/action records | 5,000 |
| Findings | 2,000 |
| Scope candidates | 1,000 |
| Producer result bytes | 1 MiB |
| Final report bytes | 8 MiB |

An exceeded required bound is `OVER_LIMIT`, makes dependent checks unknown, and
sets `evidence_status: PARTIAL`. Do not truncate a source into apparent coverage.
Optional code-health scanning must remain inside the manifest's exact roots and
file count/byte receipt; over-limit scanning is an explicit optional gap.

## Milestone and evidence manifest

The resolved milestone must declare:

```text
schema_version
milestone_id
milestone_revision
target_checkpoint
target_build_id
target_date
sprint_ids[]
required_scope[]
success_criteria[]
quality_thresholds[]
progress_basis
pillar_goal_ids[]
player_goal_ids[]
evidence_manifest_path
```

`progress_basis` is exactly one of `acceptance_criteria`, `story_points`, or
`items`. Every required scope row has a stable ID. Every criterion/threshold has
a stable ID, owner scope ID, exact comparison operator, expected unit/basis, and
required flag. The sprint ID array is ordered, unique, and exact.

The manifest schema is `cgs.milestone-evidence-manifest/v1` and contains:

```text
schema_version
milestone_id
milestone_revision
milestone_sha256
target_checkpoint
target_build_id
captured_at_utc
freshness_policy
repository_revision
sources[]
```

Each `sources[]` row contains stable `source_id`, `source_type`, canonical
`path`, declared `revision`, raw `sha256`, required flag, and the applicable
milestone/sprint/build/hardware/scenario/unit/basis join keys. `freshness_policy`
must identify which source types expire and their exact milestone-owned limits;
absence of a required limit is `MALFORMED`, not permission to invent one.

The required source types are milestone, tracker, sprint report for every exact
sprint ID, bug registry, test result, performance report for every required
threshold, risk register, and pillar/player-goal evidence. Repository code-health
evidence is optional unless the milestone makes it a success criterion.

Order ledger rows by `source_type`, `source_id`, then canonical path. For every
expected row record one of:

```text
VERIFIED | MISSING | EMPTY | MALFORMED | HASH_MISMATCH |
REVISION_CONFLICT | BUILD_CONFLICT | STALE | OUT_OF_SCOPE |
OVER_LIMIT | UNKNOWN
```

Also record declared and observed bytes/hash/revision/build, join result,
freshness result, requirement IDs that consume the source, and a limitation.
Unexpected manifest rows remain `OUT_OF_SCOPE`; missing expected rows are
synthesized as ledger gaps. Neither condition may be silently ignored.

## Evidence coverage

`evidence_status` is `COMPLETE` only if every required expected row is present,
unique, in bounds, and `VERIFIED`, and every required criterion/threshold maps to
at least one verified row. Otherwise it is `PARTIAL`.

Coverage is reported as exact counts and stable missing/gap IDs. A required
source gap propagates to every dependent metric, completion check, delivery or
quality input, and verdict. Independent verified rows remain usable and visible.
Missing and empty sources never become zero observations.

## Metric records and formulas

Every metric is `cgs.milestone-metric/v1` with:

```text
metric_id
metric_type
subject_ids[]
source_refs[]
formula_version
operands
denominator
unit
basis
result
confidence_state
limitation
```

`confidence_state` is `VERIFIED`, `ESTIMATE_BOUND`, or `UNKNOWN`. Use `VERIFIED`
only for direct deterministic calculation from all required verified inputs;
use `ESTIMATE_BOUND` only when the milestone explicitly labels every input as an
estimate and declares the compatible estimation basis; otherwise use `UNKNOWN`.

Formulas are:

- `MR-METRIC/AC-COMPLETION/v1`: `100 * completed_required_ac / total_required_ac`.
  An AC is complete only when the tracker maps it uniquely to the milestone and
  its controlled terminal state is verified. A zero denominator is `UNKNOWN`.
- `MR-METRIC/PLANNED-COMPLETED/v1`: sum planned and completed units solely in the
  milestone's `progress_basis`. For `acceptance_criteria` and `items`, each
  uniquely mapped row is one unit. For `story_points`, use declared non-negative
  integer points; missing points make the affected sum `UNKNOWN`. Never mix or
  substitute bases.
- `MR-METRIC/SPRINT-COMPLETION/v1`: count the exact declared sprint IDs whose
  report is verified and declares the same milestone, revision lineage, and
  controlled terminal state. Report verified-complete, verified-incomplete, and
  unknown counts against the declared sprint denominator.
- `MR-METRIC/BUG-COUNT/v1`: group exact milestone-linked open records by the
  milestone's controlled state and severity maps. Unknown/unmapped values stay
  separate and invalidate thresholds that depend on them.
- `MR-METRIC/TEST/v1`: copy result and coverage numerator/denominator/unit/basis
  from the verified exact-build receipt. Do not convert line, branch, function,
  scenario, or requirement coverage.
- `MR-METRIC/PERFORMANCE/v1`: compare observed and threshold integers only when
  build, hardware profile, scenario, aggregation statistic, sampling window, and
  unit exactly match. Unit conversion is not allowed by this workflow.
- `MR-METRIC/VELOCITY/v1`: `sum(completed compatible units) /
  sum(elapsed working days)` over verified completed declared sprints. Every
  sprint must use the milestone basis and a positive integer elapsed-working-day
  value. Return the unreduced rational pair; incompatible or zero denominators
  make the result `UNKNOWN`.
- `MR-METRIC/ADJUSTED-DAYS/v1`: `ceil(remaining compatible units / velocity)`.
  `remaining = planned - completed` in the same basis and is clamped to zero only
  when both operands are verified. Velocity must be positive. Show the integer
  ceiling calculation and label this an estimate, never a promise/date.
- `MR-METRIC/CODE-MARKERS/v1`: exact counts for controlled literal markers
  `TODO`, `FIXME`, and `HACK` within manifest roots at the exact repository
  revision. Exclude ignored/binary/vendor/generated files only when the receipt
  declares the exclusion policy.

## Delivery and quality checks

Each required scope item and success criterion has an explicit three-state check:
`PASS`, `FAIL`, or `UNKNOWN`. `delivery_status` is `COMPLETE` only when all pass,
`INCOMPLETE` when any conclusively fails, otherwise `UNKNOWN`.

Each required quality threshold has the same three-state check against its exact
operator and matching verified metric. `quality_status` is `PASS` only when all
pass, `FAIL` when any conclusively fails, otherwise `UNKNOWN`. A fail is not
erased by another source gap; report both.

## Stable findings

A finding object uses `cgs.milestone-review-finding/v1`. Its fingerprint input is
canonical JSON of:

```text
{schema_version, milestone_id, finding_type, check_id, subject_ids}
```

Sort and deduplicate `subject_ids`. `finding_id` is `MRF-` plus the first 20
lowercase hex characters of the SHA-256 fingerprint. The full fingerprint hash
is retained. Exclude prose, line numbers, source hashes, observed values,
severity/classification, state, timestamps, reviewer, and verdict so the same
logical finding remains stable across runs.

The full row contains classification `BLOCKER|GAP|RISK|WARNING`, state, concise
evidence-bound summary, source refs, affected requirement IDs, owner or
`UNKNOWN`, external action, deadline or `UNKNOWN`, and deterministic resolution
condition. Duplicate fingerprints are merged by sorted unique evidence refs;
distinct checks are not collapsed.

## Scope candidates and decisions

A candidate is `cgs.milestone-scope-candidate/v1` with `candidate_id`, action
`PROTECT|SIMPLIFY|DEFER|CUT`, affected scope and criterion IDs, source refs and
hashes, schedule-effect operands/formula/basis, verified pillar/player impact,
dependency/quality/risk impact, alternative, tradeoff, decision owner, and exact
status `CANDIDATE_NOT_DECIDED`.

Its stable ID is `MSC-` plus the first 20 lowercase hex characters of SHA-256
over canonical `{schema_version,milestone_id,action,scope_ids,criterion_ids}`.
Sort/deduplicate ID arrays. Unknown effects remain unknown; do not turn an
unsupported schedule estimate into a reason to cut.

Only a separate `cgs.milestone-scope-decision/v1` supplied by the user can decide
a candidate. It binds candidate ID and full candidate hash and records exact
choice, decision-maker identity, UTC timestamp, rationale, accepted impacts, and
follow-up owner/deadline. Invalid/stale decisions are quoted as gaps and never
applied by this review.

## Evidence-only draft and producer receipt

The canonical evidence draft contains only:

```text
schema_version
milestone_identity
target_identity
review_mode
source_snapshot_sha256
evidence_status
evidence_ledger
coverage
metrics
delivery_inputs
quality_inputs
findings
scope_candidates
supplied_scope_decisions
limitations
```

It must not contain producer output, `risk_status`, `evidence_verdict`,
`decision_status`, governance decision, write authorization, report path/hash,
or `artifact_write_status`. Freeze exact draft bytes before reviewer dispatch.

A producer result uses `cgs.milestone-risk-review/v1`, echoes exact milestone,
target, draft hash, and source-snapshot hash, and records reviewer ID, start/end
UTC timestamps, `ON_TRACK|AT_RISK|OFF_TRACK`, stable risks/mitigations with
source refs and owner/deadline or `UNKNOWN`, limitations, and its own hash. Hash
or identity mismatch, invalid schema, duplicated response, unsupported metric, or
timeout is a reviewer gap: `risk_status: UNKNOWN` and objective `PARTIAL`.

Lean and Solo produce an explicit deterministic skip receipt, not a producer
opinion, and set `risk_status: NOT_REVIEWED`.

## Layered verdict and decision

Derive in this order:

1. `delivery_status` and `quality_status` from checks.
2. `risk_status` from one valid same-draft producer receipt or explicit mode skip.
3. `evidence_verdict` from the first matching rule in `SKILL.md`.
4. `decision_status` only from a user governance record.
5. `artifact_write_status` only from the optional report transaction.

Store a `verdict_rule_id` (`MR-VERDICT-01` through `MR-VERDICT-04`) and exact
input tuple. Accepted risk never changes that tuple or any objective field.

A governance record is `cgs.milestone-governance-decision/v1` and binds
milestone ID, target, source snapshot, evidence draft, producer result or skip,
and objective verdict hashes. It contains `decision_status`, user-supplied
decision maker/time/rationale, accepted stable IDs, follow-up owners/deadlines,
and record hash. Missing required user fields means `NOT_RECORDED`; do not fill
them from task/session identity.

## Immutable report transaction

The path is exactly
`production/milestones/reviews/<milestone-id>/<run-id>.md`, where `run-id` is the
current review's frozen UTC second plus the first 12 characters of
`source_snapshot_sha256`. A pre-existing path is a collision and blocks the
write. Do not select another time, append a counter, or overwrite.

Final report bytes use schema `cgs.milestone-review-report/v2`, UTF-8/LF, and a
fixed section order: identity; layered statuses; evidence ledger/coverage;
metrics and derivations; delivery/quality checks; findings; scope candidates and
supplied decisions; risk review/skip; objective verdict; separate governance
decision; limits/limitations; immutable provenance; mutation/write receipt.

Before authorization, preview canonical path, operation `CREATE_NEW`, exact
candidate hash/size, frozen source base set, and singleton allowed write set. An
authorization is valid only for all those values. After authorization:

1. Re-resolve and raw-hash every source and authority file; require the identical
   frozen base set and require target absence.
2. Prepare exact bytes in the report's directory without exposing the target.
3. Atomically create the target with create-new/no-replace semantics.
4. Reread target, verify exact bytes/hash, and rehash sources again.
5. Record success only if every check passes. Clean up only the workflow-owned
   temporary file after validating its exact path; never modify the target.

Any pre-write change invalidates the candidate and authorization. Any ambiguous
post-write state is `artifact_write_status: ERROR` with an honest existence/hash
observation, never claimed success. Successful persistence changes no readiness
or decision field.
