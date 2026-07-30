---
name: milestone-review
description: Review one stable milestone for bounded, revision-bound progress, bug, test, performance, risk, and sprint evidence; record deterministic metrics and layered readiness states, keep scope and risk decisions user-owned, and optionally create one immutable authorized report.
---

# Milestone Review

Treat revisions as supplied metadata; never calculate them from file content. Use stable business IDs, canonical paths, schema versions, explicit revisions, and UTC run IDs for identity and currentness.

Review exactly one milestone snapshot without guessing progress, quality, dates,
scope decisions, or authority. Analysis is read-only. The only permitted project
mutation is one immutable review artifact after an exact preview, authorization,
source compare-and-set, atomic create, and post-write verification.

This workflow does not advance a milestone, modify scope, accept risk on the
user's behalf, update a tracker, run tests, fix bugs, change a build, or invoke a
downstream workflow.

## Invocation

Use exactly:

```text
$milestone-review [current|<stable-milestone-id>] [--review full|lean|solo]
```

- Omitted selector means `current`.
- At most one selector and one `--review` occur.
- A milestone ID matches `^[a-z0-9][a-z0-9-]*$` and is not a path/alias.
- Reject positional extras, unknown/repeated options, missing values, path
  separators, traversal, glob/regex characters, or invalid review mode with
  `run_status: ERROR`. Read no milestone evidence, invoke no reviewer, and write
  nothing.
- Review mode resolves once: explicit value, otherwise exact trimmed
  `production/review-mode.txt`, otherwise `lean`. A malformed present file is an
  error; do not silently default around it.

Never select a milestone, sprint, build, evidence source, report, or reviewer
input by modification/creation time, filename order, or “latest” prose.

## Status vocabulary

Keep every field independent:

| Field | Exact values | Meaning |
|---|---|---|
| `run_status` | `COMPLETE`, `PARTIAL`, `BLOCKED`, `ERROR` | Workflow/evaluation execution state |
| `delivery_status` | `COMPLETE`, `INCOMPLETE`, `UNKNOWN` | Required scope and success-criterion state |
| `quality_status` | `PASS`, `FAIL`, `UNKNOWN` | Declared bug/test/performance/quality threshold state |
| `risk_status` | `ON_TRACK`, `AT_RISK`, `OFF_TRACK`, `NOT_REVIEWED`, `UNKNOWN` | Exact producer result, skip, or unavailable review |
| `evidence_status` | `COMPLETE`, `PARTIAL` | Required-source coverage/currentness |
| `evidence_verdict` | `GO`, `CONDITIONAL_GO`, `NO_GO`, `PARTIAL` | Objective readiness derived after risk review |
| `decision_status` | `PROCEED`, `PROCEED_WITH_ACCEPTED_RISK`, `HOLD`, `NOT_RECORDED` | Separate user governance decision |
| `artifact_write_status` | `COMPLETE`, `BLOCKED`, `ERROR`, `NOT_REQUESTED` | Immutable report transaction only |

Do not emit legacy `MILESTONE COMPLETE`, `MILESTONE INCOMPLETE`, bare
`COMPLETE`, producer risk status, or write success as a readiness verdict. A
report write changes only `artifact_write_status`. A user decision changes only
`decision_status` and its decision record.

## Load the contract

Read [milestone-review-rules-v1.md](references/milestone-review-rules-v1.md)
completely. It defines evidence/source schemas, fixed limits, stable findings,
metric formulas, scope-candidate records, producer result binding, layered verdict,
decision records, report serialization/path, and atomic write protocol.

Read [continued-workflow.md](references/continued-workflow.md) completely and
execute its phases in order. Missing, unreadable, or contradictory private
contracts produce `run_status: ERROR`, invoke no reviewer, and write nothing.

## Mutation boundary

Before report authorization:

```text
allowed_project_write_set: []
source_artifacts_mutated: false
report_persisted: false
downstream_workflow_invoked: false
```

After authorization, `allowed_project_write_set` contains exactly one new
`production/milestones/reviews/<milestone-id>/<run-id>.md` path. Never edit,
overwrite, append, rename, delete, stage, or repair another project file. Scratch
data remains outside the project and is not evidence unless represented by a
validated revision-bound receipt.

Capture before/after snapshots for every bounded source and the proposed report
path. Concurrent changes are stale evidence; do not revert or attribute them.

## Resolve one stable milestone

### Explicit ID

Resolve only `production/milestones/<milestone-id>.md`. Its internal stable ID,
when declared, must match the selector/filename.

### `current`

Read these authority sources when present:

- `production/session-state/active.md`
- `production/milestones/index.md`

Parse only explicit `Active Milestone ID:` or `active_milestone_id:` fields.
Resolution succeeds when at least one source declares exactly one valid ID, no
source declares multiple IDs, all present declarations agree, and exactly one
matching milestone file exists. Session state and index are co-equal consistency
evidence; neither timestamp nor filename recency breaks a conflict.

Missing declarations, duplicate/conflicting/malformed IDs, zero/multiple target
files, or an unsafe path returns `run_status: BLOCKED` before evidence loading,
with `artifact_write_status: BLOCKED`. Do not ask the user to choose from a
recency-derived list.

### Missing, empty, or malformed milestone

After stable resolution, the milestone file must be a non-empty regular file with
one matching ID, schema/version, target checkpoint/build, target date, exact sprint
IDs, required scope/success criteria, quality thresholds, progress basis, pillar/
player goals, and evidence-manifest reference.

- absent or zero-byte file: `BLOCKED` subtype `MILESTONE_MISSING_OR_EMPTY`;
- parse/schema/ID conflict: `BLOCKED` subtype `MILESTONE_INVALID`;
- ambiguous duplicate criteria/sprint IDs/builds: `BLOCKED` subtype
  `MILESTONE_INCONSISTENT`.

In these branches, emit a resolution diagnostic only: no metric template,
evidence-only draft, producer review, evidence verdict, decision prompt, or report
write.

## Load a bounded evidence manifest

Read the exact manifest referenced by the milestone; the canonical default is
`production/milestones/evidence/<milestone-id>.yaml`. It must be
`cgs.milestone-evidence-manifest/v1` and bind the milestone declared version/revision,
target build/checkpoint, capture time/freshness policy, repository revision, and:

- current tracker path/version/revision and milestone/AC mappings;
- the milestone's exact ordered sprint ID set, with one report path/version/revision
  and working-day/unit basis per sprint;
- bug registry path/version/revision and controlled state/severity mapping;
- test-result path/version/revision, exact build, measurement basis, and threshold;
- performance report paths/revisions/revisions, exact build/hardware/scenario/units,
  and matching milestone thresholds;
- risk register path/version/revision and stable risk IDs/owners/status;
- exact pillar/player-goal and dependency evidence used by scope candidates; and
- bounded repository roots/receipt for optional code-health counts.

Apply the fixed limits in the rules reference. The milestone sprint ID set is the
scope authority; do not read “all sprint reports.” Missing/extra/duplicate sprint,
source over-limit, or omitted row is explicit coverage, never silent inclusion.

For every source, record exactly one state:

```text
VERIFIED | MISSING | EMPTY | MALFORMED | REVISION_MISMATCH |
REVISION_CONFLICT | BUILD_CONFLICT | STALE | OUT_OF_SCOPE |
OVER_LIMIT | UNKNOWN
```

Verify canonical project confinement, declared revision, declared/internal revisions,
build/hardware/scope joins, unique stable IDs, and milestone-declared freshness.
Do not invent a default maximum age. A dirty/mismatched repository makes only
repository-derived evidence unavailable.

Any required non-VERIFIED source sets `evidence_status: PARTIAL`, every dependent
metric/check to `UNKNOWN`/`UNVERIFIED`, and forbids `GO`. Preserve independent
verified evidence; never fill gaps from memory, old reports, role opinion, or
model inference.

Create `source_snapshot_revision` over canonical ordered evidence-ledger rows and
record the canonicalization version. Revalidate every source at finalization and
immediately before an authorized write.

## Compute deterministic metrics

Use only `VERIFIED` sources and the formulas in the rules reference. Every metric
row includes stable metric ID, source paths/revisions/revisions, formula version,
operands, denominator, unit/basis, exact result or `UNKNOWN`, confidence state,
and limitation.

Required metrics include:

- feature/acceptance-criterion completion;
- planned versus completed units in the milestone-declared basis;
- exact sprint completion counts;
- open bug counts by milestone-declared controlled severity/state;
- test result/coverage in its declared basis without conversion;
- performance comparisons for matching build/hardware/scenario/units;
- velocity per working day using only compatible verified completed sprints;
- adjusted remaining working days using ceiling division and positive velocity;
  and
- bounded TODO/FIXME/HACK counts only from the exact repository revision/roots.

Never render an unavailable value as zero, convert coverage bases/units, mix
points/items/ACs, omit a denominator, use calendar days for working days, or
invent feature percentages/velocity/confidence.

## Stable findings, blockers, risks, and actions

Normalize each non-pass or coverage gap as
`cgs.milestone-review-finding/v1` with stable `MRF-<20hex>` identity, finding/check
type, milestone/subject IDs, source evidence, classification
`BLOCKER|GAP|RISK|WARNING`, state, owner, external action, deadline or `UNKNOWN`,
and deterministic resolution condition. Finding identity excludes wording,
line, source revision, value, severity, status, timestamp, reviewer, and verdict.

Do not drop lower-level gaps when a blocker controls. A prior risk/action status
is not current unless its exact source/version/revision verifies.

## Scope candidates are not product decisions

The analyzer may return evidence-backed `PROTECT`, `SIMPLIFY`, `DEFER`, or `CUT`
candidates. Each `cgs.milestone-scope-candidate/v1` has stable candidate ID,
affected scope/criterion IDs, source revisions, schedule effect and derivation,
player/pillar impact bound to current pillar evidence, dependency/quality/risk
impact, alternative/tradeoff, product decision owner, and status
`CANDIDATE_NOT_DECIDED`.

Do not decide, apply, prioritize, or phrase a candidate as committed scope. A
final scope change requires a separate user-owned decision artifact with candidate
ID/revision, choice, decision maker, timestamp, rationale, accepted impacts, and
follow-up owner. This review may quote a supplied current decision artifact but
does not mutate milestone/tracker/scope.

## Evidence-only draft precedes producer review

Build `cgs.milestone-evidence-draft/v1` in memory after evidence/metrics/findings/
candidates. It contains no producer result, `risk_status`, `evidence_verdict`,
`decision_status`, or report-write state. Serialize its exact canonical bytes and
record `evidence_draft_revision`. Show the draft identity/revision before review.

Review mode:

- `solo`: `risk_status: NOT_REVIEWED`, exact Solo skip record;
- `lean`: `risk_status: NOT_REVIEWED`, exact Lean skip record;
- `full`: dispatch `producer` through Codex subagent delegation using
  `PR-MILESTONE` from `.codex/docs/director-gates.md` with the exact immutable
  draft records/revision and no write authority.

A valid `cgs.milestone-risk-review/v1` echoes milestone/build,
`evidence_draft_revision`, `source_snapshot_revision`, reviewer identity, timestamps,
one of `ON_TRACK|AT_RISK|OFF_TRACK`, stable risk/mitigation rows, limitations, and
result revision. The producer cannot change draft bytes, metrics, source states, scope,
or product decisions.

Timeout, unavailable/delegation error, malformed/duplicate result, different
milestone/build/revision, or invented metric sets `risk_status: UNKNOWN`, adds a
stable reviewer gap, and forces `evidence_verdict: PARTIAL`. Preserve the draft;
do not silently rerun against changed input.

## Derive objective statuses and verdict

First compute:

- `delivery_status: COMPLETE` only when every required scope item and success
  criterion is verified complete; `INCOMPLETE` for verified incomplete/blocked;
  otherwise `UNKNOWN`.
- `quality_status: PASS` only when every declared required threshold has matching
  verified evidence and passes; `FAIL` for a conclusive required threshold
  failure; otherwise `UNKNOWN`.

Then apply the first matching rule:

1. evidence partial, delivery/quality unknown, or required full-mode producer gap
   → `evidence_verdict: PARTIAL`;
2. delivery incomplete, quality fail, open required blocker, or OFF_TRACK
   → `NO_GO`;
3. complete evidence/delivery/quality, no blocker, and AT_RISK
   → `CONDITIONAL_GO` with sourced owner/deadline conditions;
4. complete evidence/delivery/quality, no blocker, and ON_TRACK or NOT_REVIEWED
   → `GO`.

No user choice changes evidence, delivery, quality, risk, or objective verdict.

## Record a separate governance decision

After showing objective fields, gaps, risks, and tradeoffs, the user may choose:

- `PROCEED` only for objective GO;
- `PROCEED_WITH_ACCEPTED_RISK` for CONDITIONAL_GO, NO_GO, or PARTIAL;
- `HOLD`; or
- no decision, recorded as `NOT_RECORDED`.

A risk-acceptance record requires user-supplied decision maker, UTC timestamp,
rationale, exact accepted stable risk/gap IDs, and follow-up owners/deadlines. Do
not invent or infer them. Reject `PROCEED` for a non-GO result rather than
renaming/reframing the evidence. Accepted risk is governance evidence, not
readiness evidence.

## Preview and create one immutable report

Path is exactly:

```text
production/milestones/reviews/<milestone-id>/<run-id>.md
```

`run-id` is `<UTC-YYYYMMDDTHHMMSSZ>-<run-sequence>`. The report
uses schema `cgs.milestone-review-report/v2` and contains resolved ID/authority,
run/target/review identities,
every layered status, evidence ledger/source revisions/revisions, snapshot/draft/
producer/finding/candidate/decision revisions, metric formulas/operands/confidence,
scope candidates/decisions, stable findings/actions, canonicalization, and stale
conditions.

Construct exact final bytes and `report_candidate_revision`, then preview canonical
path, `CREATE_NEW`, source base revision set, report revision/size, and allowed write set.
Use existing task authorization only when it explicitly covers the exact candidate;
otherwise obtain one authorization. Decline means `artifact_write_status: BLOCKED`.

After authorization, revalidate every source and require the report path still absent.
Any change invalidates candidate/authorization and requires new evidence, run ID,
path, preview, and authorization. Never overwrite or invent a suffix.

Atomically create only the authorized path from a same-directory prepared file,
then reread and verify exact report revision/bytes and that all sources remain
unchanged. Failure leaves the target absent or returns a verified failure state;
never report success from a partial/unverified write. Successful creation sets
only `artifact_write_status: COMPLETE`.

## Return and stop

Return `cgs.milestone-review-run/v2` with normalized invocation, milestone/
authority, run/source/draft/producer/report identities, fixed-limit coverage,
evidence ledger, metrics, findings, scope candidates and supplied decisions,
layered status derivation, separate decision record, mutation snapshots, report
path/revision or null, and stale key.

Do not claim an unpersisted/partial report exists, invoke gate-check/sprint-plan,
advance a milestone, or execute a recommendation. Stop after the result.
