---
name: tech-debt
description: Analyze technical-debt candidates and append-only register evidence through four strictly read-only modes, with stable keys, versioned analyzer receipts, explicit lifecycle state, advisory ranking, and separately authorized atomic conflict check recorder proposals.
---

## Path-first integrity

Accept canonical project-relative paths directly; do not require a caller-supplied
content-derived token. Validate project-root containment, regular-file type, declared
schema/version, stable IDs, permissions, lifecycle state, and path or ID collisions.
Allocate collision-safe IDs independently of file bytes. Before any permitted write,
re-read referenced records and target state, preview the exact authorized changes,
then use same-directory staging plus atomic replacement and rollback on failure.


# Tech Debt

Analyze one bounded project snapshot without changing it. Scanner hits are
candidates, not technical-debt decisions. The skill may propose exact register
events, but it never creates, migrates, appends, rewrites, sorts, or repairs the
authoritative register and never invokes a recorder.

This workflow does not accept debt, resolve debt, choose product priority, assign
sprint scope, estimate delivery time, or certify project quality.

## Invocation

Use exactly one of these forms:

```text
$tech-debt scan --scope <project-relative-manifest>
                --register <project-relative-path>|ABSENT:<project-relative-path>
$tech-debt add --register <project-relative-path>|ABSENT:<project-relative-path>
               [--candidate <project-relative-record>]
$tech-debt prioritize --register <project-relative-path>|ABSENT:<project-relative-path>
$tech-debt report --register <project-relative-path>|ABSENT:<project-relative-path>
                  [--baseline-event <uuid>]
```

- `scan` requires one immutable `cgs.tech-debt-scan-scope/v1` manifest.
- `add` accepts at most one immutable `cgs.tech-debt-manual-candidate/v1`
  record. Without it, return `INPUT_REQUIRED` with the exact missing fields.
- `report` accepts at most one baseline selector.
- Options may appear in either order within a mode, but each may appear once.
- Paths must be canonical project-relative paths: `/` separators, Unicode NFC,
  no absolute path, drive prefix, URI, traversal, glob, symlink escape, or
  case-ambiguous match.
- `@revision:` binds the exact bytes. A revision mismatch, unreadable input, schema
  mismatch, unrelated project/register ID, or mutable/ambiguous resolution is
  an input identity error.

An absent/unknown mode, positional argument, unknown/repeated option, missing
value, malformed UUID/revision/path, illegal option combination, or unexpected
payload returns `USAGE_ERROR`. A well-formed invocation whose referenced input is
invalid returns `INPUT_ERROR`; an invalid register returns `REGISTER_ERROR`.
These are execution states, not debt or project-quality verdicts. Do no scan,
proposal, or write after an invocation/input/register error.

Valid skill outcomes are exactly:

```text
SCAN_COMPLETE | NO_NEW_DEBT_FOUND | SCAN_PARTIAL |
ADD_PREVIEW_READY | ADD_DUPLICATE_FOUND | INPUT_REQUIRED |
PRIORITY_VIEW_READY | PRIORITY_VIEW_PARTIAL |
REPORT_READY | REPORT_PARTIAL |
USAGE_ERROR | INPUT_ERROR | REGISTER_ERROR
```

`REGISTER_UPDATED`, `MUTATION_FAILED`, `PASS`, `FAIL`, `COMPLETE`, severity, and
priority are not skill outcomes.

## Load the contract

Read [debt-rules-v1.md](references/debt-rules-v1.md) completely. It defines
bounded scope, candidate and analyzer receipts, exclusions, stable keying,
register schema/lifecycle, scoring, report baselines, change proposals, and the
independent recorder protocol.

Read [continued-workflow.md](references/continued-workflow.md) completely and
follow the common and mode-specific phases in order. If either file is missing,
unreadable, or internally inconsistent, return `INPUT_ERROR` without analysis.

## Strict read-only boundary

The allowed write set is empty. Do not create a register, migrate legacy data,
append an event, update `last_seen`, persist a report/view/proposal, cache output,
install/update an analyzer, generate a dependency, build the game, edit source,
or reorder existing bytes. Do not request ordinary write permission for this
skill.

Record a before/after mutation snapshot for the bounded inputs. If attributable
mutation cannot be established, disclose concurrent changes without reverting
or assigning blame. A changed analyzed input invalidates its evidence and yields
`SCAN_PARTIAL`, `PRIORITY_VIEW_PARTIAL`, or `REPORT_PARTIAL`; a changed register
identity yields `REGISTER_ERROR`. Never call the independent recorder from this
workflow.

## Register identity, absence, and validity

The caller identifies the authoritative register; do not discover one by name.
A present register must validate exactly as `cgs.tech-debt-register/v3`, including
its project/register UUIDs, monotonic revision, append-only global event sequence,
event/payload revisions, global and per-debt predecessor chains, UUID uniqueness,
stable key ownership, lifecycle transitions, and declared revision.

Replay valid events to obtain the current view. Never treat a materialized table,
sorted report, comment, or prose summary as authoritative. Unknown legacy state
is `UNKNOWN` and cannot be silently mapped.

For `ABSENT:<path>`:

- verify that the exact canonical path is absent;
- `scan` analyzes against an empty index and marks `REGISTER_ABSENT`;
- `add` may return a `CREATE_REGISTER` proposal;
- `prioritize` returns `PRIORITY_VIEW_PARTIAL` with an empty view; and
- `report` returns `REPORT_PARTIAL` with absence and all register-derived metrics
  `UNKNOWN`.

Absence never creates a file. A malformed, revision-mismatched, conflicting, or
unsupported register returns `REGISTER_ERROR` in every mode. A recognized legacy
schema returns `REGISTER_ERROR` subtype `MIGRATION_REQUIRED` plus a read-only
migration proposal; it is never repaired or reinterpreted here.

## Candidate, evidence, and decision boundary

Every scanner result is a `cgs.tech-debt-candidate/v2`. It must name its stable
rule, exact source evidence, frozen scope, analyzer receipt(s), confidence,
verification state, intentional-design alternative, triage requirement,
stable key, and any register match.

Candidate states are:

```text
HEURISTIC_CANDIDATE | EVIDENCE_SUPPORTED | UNVERIFIED
```

A TODO/FIXME/HACK/deprecated marker, file-length threshold, keyword hit, naming
pattern, or path convention is only `HEURISTIC_CANDIDATE`. It is never debt,
severity, acceptance, priority, or proof of duplication/complexity. Owner triage
is required before a candidate can be selected for a `CREATED` proposal.

Complexity requires a compatible language-aware control-flow/AST analyzer.
Duplication requires a compatible token/AST clone analyzer with declared minimum
clone size and normalization. Missing, failed, timed-out, stale, incompatible,
unversioned, or side-effecting analyzers make the affected check `UNVERIFIED` and
the scan `SCAN_PARTIAL`. Never fabricate a result or replace unsupported analysis
with prose review or text similarity.

Generated output, vendored/third-party dependencies, caches, build artifacts,
engine imports, and test fixtures are excluded only by versioned scope/classification
evidence. Tests are excluded from generic size/clone rules unless a test-specific
rule is explicitly enabled. Every exclusion is visible in the coverage ledger;
missing classification is `UNVERIFIED`, not an inferred exclusion.

## Stable identity and deduplication

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

Replay all primary stable keys and aliases before classifying a candidate:

- one stable key/alias has at most one owning `debt_id`;
- an existing stable key preserves its UUID and may produce one `OBSERVED`
  proposal only for materially new evidence at a new source identity;
- the same source/evidence produces no event;
- a resolved match is `REAPPEARED`, but remains `RESOLVED` unless an authorized
  `REOPENED` event is recorded externally;
- line moves do not change identity;
- a path/symbol move obtains an alias only from an immutable VCS move receipt or
  a user-selected alias proposal; absent that evidence it remains a new candidate;
  and
- duplicate stable key owners, duplicate/conflicting UUIDs, broken aliases, or
  event-chain conflicts return `REGISTER_ERROR`.

The analyzer never assigns a debt UUID. A proposal may reserve an RFC 4122 UUIDv4,
but the independent recorder must collision-check it under atomic conflict check; a collision
invalidates the proposal and authorization.

## Mode: scan

1. Validate the scope manifest, its project/target identity, explicit included
   paths, checks, analyzers, exclusions, and fixed limits.
2. Validate/replay the register or establish exact absence.
3. Run only declared read-only analyzer commands. Emit a
   `cgs.tech-debt-analyzer-receipt/v1` for every requested check.
4. Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
5. Return new, matched, unchanged, reappeared, unverified, excluded, unsupported,
   timed-out, and over-limit rows separately.
6. Present only a `cgs.tech-debt-change-proposal/v1` for owner-selected candidates.
   Do not triage, record, accept, prioritize, schedule, or resolve them.

Return `SCAN_COMPLETE` when every requested check completed and the delta is
known; `NO_NEW_DEBT_FOUND` when complete analysis has no new candidate or new
observation proposal; otherwise return `SCAN_PARTIAL` and enumerate gaps. A
complete scan may still contain candidates.

## Mode: add

Validate the manual candidate record. Required fields are description, stable
defect class, canonical affected path(s), stable symbol or `<file>`, evidence,
source identity, category or `UNKNOWN`, owner or `UNASSIGNED`, and why the item is
being considered for owner triage. Impact/frequency/effort may be `UNKNOWN`; any
numeric value requires evidence and the fixed scales.

Manual input is still a candidate. It cannot declare `ACCEPTED`, `RESOLVED`,
`SUPERSEDED`, product priority, or sprint scheduling. Use the `manual@2` rule and
`td-key-v1`, then deduplicate against the register. Return:

- `INPUT_REQUIRED` when no candidate record or required field is present;
- `ADD_DUPLICATE_FOUND` with the stable existing debt ID and an optional exact
  `OBSERVED`/triage proposal when the stable key matches; or
- `ADD_PREVIEW_READY` with an exact `CREATED`/`CREATE_REGISTER` proposal after
  owner selection.

No outcome writes the proposal.

## Mode: prioritize

This mode is read-only and outputs `ADVISORY_ONLY`. Replay current `OPEN` and
`ACCEPTED` items. Use only recorded, evidence-linked values:

| Input | Allowed values | Meaning |
|---|---|---|
| Impact | 1, 2, 3, 4 | local; component/team; milestone/product; release/security/data-integrity |
| Frequency | 1, 2, 3, 4 | rare; occasional; each sprint; continuous/core-path |
| Effort points | 1, 2, 3, 5, 8, 13 | team-calibrated implementation points, not time |

An absent, inferred, stale, evidence-free, or out-of-range input makes the item
`UNSCORED`. Never convert or sum T-shirt sizes without a separately recorded team
calibration.

For scored items compute exactly:

```text
advisory_score = (impact * frequency) / effort_points
```

Retain the exact rational/unrounded value; display three decimals. Sort the
transient view by score descending, impact descending, frequency descending,
effort ascending, oldest `CREATED` timestamp first, then lexical `debt_id`.
List `UNSCORED` rows separately by lexical debt ID. Show source events/evidence,
calculation, uncertainty, and tie-breaks. Never reorder the register or propose a
priority/schedule event unless the user separately selects a decision for an
external recorder proposal.

Return `PRIORITY_VIEW_READY` when every requested outstanding item is scored, or
`PRIORITY_VIEW_PARTIAL` with gaps when any is unscored, inaccessible, absent, or
changed.

## Mode: report

Replay the immutable event log without writing. Report current counts by category,
lifecycle status, and verification state; effort-point distribution and unknown
count; evidence ages; and explicit data gaps.

Change/trend requires a valid baseline event UUID or register revision that is an
ancestor of the current chain. Compute created, observed, accepted, reopened,
resolved, and superseded transitions from exact event cursors. Derive age only
from recorded UTC event timestamps. “Older than three completed sprints” requires
stable sprint-transition events or an immutable external sprint-history receipt;
otherwise it is `UNKNOWN`.

Return `REPORT_READY` when requested register/baseline fields are complete;
otherwise `REPORT_PARTIAL`. Missing or incomparable baseline makes change/trend
`UNKNOWN`, never zero. A malformed/unrelated baseline is `INPUT_ERROR`; a broken
register chain is `REGISTER_ERROR`.

## Change proposal and independent recorder boundary

Any user-selected creation, observation, lifecycle, alias, estimate, priority, or
schedule change is represented only as a
`cgs.tech-debt-change-proposal/v1`. The proposal binds:

- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
  base revision, last global event UUID/revision, and operation `CREATE_REGISTER` or
  `APPEND_EVENTS`;
- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
- owner selection and decision-authority references required by the event type;
- proposal ID/revision, creation/expiry time, and an explicit statement that it is
  `NOT_PERSISTED` and `NOT_AUTHORIZATION`.

The independent `cgs.tech-debt-recorder/v1` protocol in the rules reference is
the only writer contract. This skill does not implement, dispatch, or simulate
it. A future recorder requires a new exact authorization over one proposal revision.
Analyzer conversation, a scan request, owner triage, or prior authorization is
not write authority.

## Return and stop

Return the mode, outcome, normalized invocation, project/target/register identity,
input revisions, bounded coverage ledger, analyzer receipts, exclusions/gaps,
candidates and stable keys, dedup/lifecycle view, advisory calculations or
report baseline, proposal (if selected), before/after mutation evidence, and stale
key. Mark every direct result:

```text
register_mutated: false
proposal_persisted: false
decision_authority_exercised: false
recorder_invoked: false
```

Then stop. Do not invoke a recorder, migration, estimator, sprint planner,
remediation workflow, or another project skill.
