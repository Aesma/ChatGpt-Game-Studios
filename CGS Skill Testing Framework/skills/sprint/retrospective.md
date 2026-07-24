# Skill Test Spec: `$retrospective`

## Skill Summary

`$retrospective` contract `cgs.retrospective/v2` resolves exactly one prefixed
sprint or milestone, reconciles exact plan/tracker revisions, and reports only
observed or deterministically derived facts. Missing, stale, conflicting,
out-of-period, bounded, or incomparable data remains `UNKNOWN` or partial.

Drafting is read-only. Explicit persistence creates one new immutable run report
and atomically advances a navigation-only latest index. Older retrospectives are
never moved, renamed, archived, overwritten, or edited. The workflow stops after
its report and never invokes planning, gates, action tracking, or another task.

The authoritative audit P1 set for this spec is exactly RT-003 through RT-009,
seven findings.

---

## Required test instrumentation

Run behavioral cases in an isolated disposable repository fixture. Record:

1. recursive path/type/SHA-256 snapshots before and after invocation;
2. every filesystem mutation attempt and atomic transaction stage;
3. every file read, canonical path, exact bytes, read order, and pre/post hash;
4. every Git command/range and returned commit identity/time/scope decision;
5. every scan tool/version/hash/argv/scope/file-list/occurrence identity;
6. exact report, index, payload, evidence, observation, action, and omission hashes;
7. deterministic clock/UUID sources and user-confirmation turn identities; and
8. every attempted workflow/task/delegation after output.

Without `--persist`, before/after snapshots and mutation-attempt ledger must be
empty. A successful persist may change only the new immutable report and exact
target index, all-or-none. If instrumentation cannot observe a required fact,
mark the assertion `UNTESTED`, not PASS. Do not invoke the project skill for
static lint and do not update catalog result fields from an uninstrumented run.

---

## Static assertions

- [ ] Frontmatter contains only `name` and a non-empty `description`
- [ ] Contract version is exactly `cgs.retrospective/v2`
- [ ] Metadata states evidence-backed, immutable, and UNKNOWN-preserving behavior
- [ ] Invocation requires exactly one `sprint:<id>` or `milestone:<id>` target
- [ ] Persist requires explicit valid run ID; invalid/ambiguous input fails before reads
- [ ] Plan/status target, revision, plan hash, story/task-set hash, period, source
  revision, and freshness equality are mandatory
- [ ] DATA CONFLICT preserves competing claims and blocks affected metrics
- [ ] Every metric/claim is OBSERVED, DERIVED with formula/sources, or literal
  UNKNOWN with confidence NONE
- [ ] Causes require event evidence or exact user/team confirmation
- [ ] Git commits require exact period, commit range/ancestry, timestamps, and
  scope; no four-week/latest-20 fallback exists
- [ ] Scan trends require identical protocol/tool/argv/scope/match/exclusion and
  compatible repository lineage
- [ ] Actions begin PROPOSED and owner/due remain UNASSIGNED without a binding
  decision receipt or explicit confirmation
- [ ] New runs use canonical immutable type/target/run paths and never mutate old
  retrospective files
- [ ] Latest index schema, preimage, atomic report+index transaction, conflict,
  idempotence, and read-back behavior are explicit
- [ ] Fixed evidence/event/commit/scan/metric/action/row/output limits cannot be raised
- [ ] Analysis, data quality, and persistence axes are independent
- [ ] `cgs.review-evidence/v1` grants no gate/planning/action authority
- [ ] Saving or drafting is terminal and triggers zero follow-on workflows/tasks

---

## Canonical fixture

Unless overridden, use target `sprint:sprint-006`, run ID
`retro-11111111-1111-4111-8111-111111111111`, policy
`cgs.retrospective-policy/v1`, revision `rev-3`, story-set hash `S`, period
`[2026-07-01T00:00:00Z, 2026-07-15T00:00:00Z)`, fresh status captured after end,
baseline commit `C0`, terminal commit `C9`, and a complete bounded scan snapshot.
All placeholder hashes are valid 64-hex values in executable fixtures.

---

## Case 1: Exact prefixed target and option grammar

### Fixture

Provide valid sprint/milestone artifacts plus similarly named plans and unrelated
paths.

### Input

Run missing target, unprefixed `sprint-006`, ambiguous `alpha`, two targets,
wrong prefix/ID, path/URL/glob, extra positional argument, duplicate/unknown
option, value beginning `--`, invalid run ID, persist without run ID, and all
valid grammar variants.

### Expected writes

None for invalid and draft variants.

### Expected behavior

Invalid inputs return BLOCKED/NOT_ATTEMPTED before reading project files. Valid
input consumes one type/target and one option value each. Draft without run ID
generates/reports one UUIDv4; persistence requires the explicit ID.

### Assertions

- [ ] Invalid token and reason are exact
- [ ] No target is inferred from current sprint, mtime, display name, or path
- [ ] Invalid forms emit no draft/evidence
- [ ] Generated run ID has no persistence authority by itself
- [ ] Mutation guard passes

## Case 2: Target lookup is unique and type-safe

### Fixture

Create exact plan/status, missing plan, empty plan, two plans claiming one ID,
wrong target type/ID, duplicate status authority row, dangling status path, and a
newer-mtime unrelated plan.

### Input

Run the exact sprint or milestone target for each fixture.

### Expected writes

None.

### Expected behavior

Only one exact policy-routed plan/status pair resolves. Zero/multiple/mismatched/
dangling identity returns `BLOCKED — TARGET NOT UNIQUE`; newest mtime and fuzzy
names are ignored.

### Assertions

- [ ] Selected normalized paths and raw hashes are reported
- [ ] Target type and stable ID agree in both artifacts
- [ ] No fallback plan is read or selected
- [ ] Blocked output has no retrospective evidence record
- [ ] Mutation guard passes

## Case 3: Plan/tracker revision and story-set conflicts are partial

### Fixture

Vary target ID, plan revision, plan SHA-256, story-set hash, source revision, item
ID, estimate unit/value, added/removed/changed story, and scope-change receipt.
Include one exact valid scope-change transaction.

### Input

Run the target for each variant.

### Expected writes

None.

### Expected behavior

Exact equality combines sources. Unexplained mismatch is DATA CONFLICT,
RETRO_PARTIAL, and blocks affected metrics while retaining both claims. Valid
scope-change evidence binds pre/post sets and supports classification.

### Assertions

- [ ] Every equality key is checked independently
- [ ] Conflict never chooses YAML or Markdown silently
- [ ] Unaffected local observations may remain supported
- [ ] No conflicting input enters a derived formula
- [ ] Mutation guard passes

## Case 4: Fresh final status and period boundaries are required

### Fixture

Use fresh post-end status, pre-end/active status, future capture, missing/invalid/
reversed/equal boundaries, and status captured exactly at end.

### Input

Run each target variant.

### Expected writes

None.

### Expected behavior

Exact-at/after-end and not-future status is fresh. Pre-end is stale and only
supports time-stamped observations; final completion/variance/trend is partial or
UNKNOWN. Invalid boundaries make all time-bound metrics UNKNOWN.

### Assertions

- [ ] Period is half-open `[start,end)`
- [ ] Freshness result and source timestamp are reported
- [ ] Active snapshot never becomes final completion truth
- [ ] Missing boundary is not replaced by default duration
- [ ] Mutation guard passes

## Case 5: Unsupported metrics remain literal UNKNOWN

### Fixture

Plan/completion evidence exists but actual effort, bug events, unplanned-work
events, blocker resolution, and explicit causes are absent. Commit messages say
fix/bug and task complexity appears high.

### Input

Run the sprint draft.

### Expected writes

None.

### Expected behavior

Supported plan/completion values remain observed. Actual effort, effort delta,
variance, accuracy, bugs found/fixed, unplanned work, resolution, and cause are
literal UNKNOWN with confidence NONE and reasons. Commit wording/complexity does
not fill them.

### Assertions

- [ ] UNKNOWN is never zero/false/none/not-applicable
- [ ] A derived metric is UNKNOWN if any required input is UNKNOWN
- [ ] Every metric has state, source/formula or reason, and confidence
- [ ] Summary does not convert UNKNOWN into qualitative certainty
- [ ] Mutation guard passes

## Case 6: Derived metrics use exact identities, units, and formulas

### Fixture

Use four planned eligible stories, three fresh completions, compatible planned/
actual effort pairs, one excluded descoped story with valid event, in-period bug
events, and boundary values affected by display rounding. Add mixed units and
unknown exclusion variants.

### Input

Run the target twice.

### Expected writes

None.

### Expected behavior

Completion is derived from exact eligible sets; effort variance uses compatible
units; bug counts use event identities. Formula, inputs, exclusions, full
precision, and policy rounding are reported. Mixed/unknown inputs remain UNKNOWN.

### Assertions

- [ ] Story IDs reconcile before counts
- [ ] Display rounding cannot change classification
- [ ] Units are never converted implicitly
- [ ] Bug absence is not zero without complete event coverage
- [ ] Repeated results are deterministic

## Case 7: Causes and responsibility require explicit confirmation

### Fixture

Provide timing correlation, commit-message explanation, task category, owner
name, event record stating a cause, explicit user/team confirmation, ambiguous
reply, and contradiction between event and user claim.

### Input

Run each variant and answer any cause question as fixture specifies.

### Expected writes

None.

### Expected behavior

Only event record or exact confirmed response supports a bounded factual cause;
the ledger records confirmation text hash and turn locator. Ambiguous/conflicting
claims remain UNKNOWN/DATA CONFLICT. Owner identity alone never implies cause.

### Assertions

- [ ] Correlation and commit prose are not cause proof
- [ ] Confirmation cannot rewrite tracker history
- [ ] Contradictions are preserved, not averaged
- [ ] Prevention/resolution claims obey the same rule
- [ ] Mutation guard passes

## Case 8: Git commits are bound to exact graph range, period, and scope

### Fixture

Provide valid baseline/terminal ancestry with commits inside/outside period and
scope. Add missing boundaries, nonexistent commit, unrelated repository,
nonancestor, missing ref, invalid timestamp/scope mapping, and fallback output
from last four weeks/latest 20.

### Input

Run the target.

### Expected writes

None.

### Expected behavior

Only commits satisfying graph range, committer UTC, and scope rule count. Invalid
identity makes Commits UNKNOWN. Fallback output is never queried or counted.
Commits never prove completion/effort/bugs/cause.

### Assertions

- [ ] Baseline is exclusive and terminal inclusive
- [ ] Included/excluded SHAs and reasons are reported
- [ ] Target half-open period applies
- [ ] No last-four-weeks/latest-20/current-branch inference occurs
- [ ] Mutation guard passes

## Case 9: TODO/FIXME/HACK trends require an identical scan protocol

### Fixture

Create current complete scan and prior snapshots varying protocol version,
scanner version/hash, argv/match semantics, include/exclude roots, generated/
vendor rules, file-list digest, repository lineage, partial status, and counts.

### Input

Run each comparison.

### Expected writes

None.

### Expected behavior

Current counts are observed only from complete scan. Trend is derived only when
all comparability keys and lineage match; otherwise literal
`UNKNOWN — INCOMPARABLE SCAN`. Same protocol computes exact current-minus-prior.

### Assertions

- [ ] Snapshot binds tool/version/hash/argv/scope/revision/counts/occurrences
- [ ] Prose count is not comparable evidence
- [ ] Scope mismatch cannot be normalized heuristically
- [ ] Partial scan cannot produce direction
- [ ] Mutation guard passes

## Case 10: Existing retrospectives remain immutable

### Fixture

An older report and valid target index exist. Run another retrospective using
start-fresh language, same target/new run ID, same run ID/identical content, and
same run ID/different content.

### Input

Run drafts and persist variants.

### Expected writes

Only a genuinely new authorized run may add a new report and update the index.
No old report path/bytes change.

### Expected behavior

Start fresh means new immutable run. Identical existing report+matching index is
UNCHANGED; differing target is CONFLICT. No rename/archive/update-existing path
exists.

### Assertions

- [ ] Historical links and hashes remain valid
- [ ] Old report is never moved, renamed, overwritten, or edited
- [ ] New run ID/path is unique
- [ ] Index is navigation only
- [ ] Filesystem diff matches expected two paths at most

## Case 11: Canonical sprint and milestone output paths are exact

### Fixture

Use one sprint and one milestone target with valid UUID run IDs; add date-only,
flat legacy, wrong-type, wrong-target, outside, and path-collision destinations.

### Input

Run draft/persist.

### Expected writes

Only exact type/target/run report and sibling index in success variants.

### Expected behavior

Intended paths are
`production/retrospectives/<type>/<target-id>/<run-id>.md` and `index.yaml`.
No date-only/flat/legacy path is written. Report/index identities agree.

### Assertions

- [ ] Path components come from validated IDs, not display names
- [ ] Sprint and milestone namespaces cannot collide
- [ ] Run ID, report hash, and target identity appear in index
- [ ] Old alternate paths are never migrated automatically
- [ ] Mutation guard passes for drafts/invalid paths

## Case 12: Report plus latest index persistence is atomic and concurrency-safe

### Fixture

Run variants with absent index, valid prior index, index changed after preview,
source changed before write, report write failure, index write failure, read-back
mismatch, and full success.

### Input

Run with explicit run ID and `--persist`.

### Expected writes

Success changes exactly new report and index. Every failure leaves old index and
all reports unchanged.

### Expected behavior

Workflow previews bytes, validates preimages, stages both, publishes all-or-none,
and read-backs hashes before WRITTEN. Conflicts/failures do not claim persistence.
Analysis/data quality remain independent.

### Assertions

- [ ] No partially published report/index pair exists
- [ ] Concurrent user index edit is preserved
- [ ] Index previous-hash chain validates
- [ ] WRITTEN requires both read-back hashes
- [ ] No third file changes

## Case 13: Action owner and due date require a team decision

### Fixture

Create evidence-backed proposed actions with model-suggested person/date, owner
role only, exact decision receipt, explicit current confirmation, ambiguous user
reply, and no response.

### Input

Run draft and respond as fixtures specify.

### Expected writes

None without persistence; action registry is never written.

### Expected behavior

Actions begin PROPOSED. Person/deadline suggestions remain candidates;
owner/due are UNASSIGNED absent exact receipt/confirmation. Exact decision binds
action ID, owner, due, authority/time, and the action-proposal-set hash shown for
confirmation and yields CONFIRMED.

### Assertions

- [ ] Model never assigns a person or commits a deadline
- [ ] Ambiguous/no response remains UNASSIGNED
- [ ] Confirmation locator/text hash is evidence
- [ ] Action can be useful while unassigned
- [ ] At most five actions survive deterministic ordering

## Case 14: Prior actions do not self-report completion

### Fixture

Latest prior report proposes actions marked unchecked; current delivery receipt
proves one complete, one explicit cancellation receipt exists, and others have no
evidence. Add invalid/missing latest index and a prior conclusion without sources.

### Input

Run current target.

### Expected writes

None.

### Expected behavior

Valid external evidence advances exact actions. Unchecked/absent status remains
UNKNOWN, and prior conclusions are not independent underlying evidence. Invalid
index yields disclosed missing prior context, not a scan of all reports.

### Assertions

- [ ] Prior report path/hash/target validates before use
- [ ] Proposal history is distinct from execution evidence
- [ ] Missing follow-up never becomes Not Started
- [ ] No prior report is modified
- [ ] Mutation guard passes

## Case 15: Stable observation and action identity does not churn

### Fixture

Generate one observation/action, then vary path, wording, severity/priority,
owner/due/status, timestamp, current report hash without canonical identity
change. Then vary target/revision/category/evidence/event or triggering observation.

### Input

Run each fixture twice.

### Expected writes

None.

### Expected behavior

Noncanonical variations preserve ROBS/RACT IDs; canonical identity changes alter
them. Duplicates coalesce, evidence remains, ordering is deterministic.

### Assertions

- [ ] Canonical JSON and 12-hex suffix recompute
- [ ] Paths/wording/owner/due/status/time/report hash are excluded
- [ ] Target/revision/category/stable evidence identity is included
- [ ] Action identity includes triggering observation IDs
- [ ] Mutation guard passes

## Case 16: Fixed bounds produce deterministic partial evidence

### Fixture

Exercise every fixed limit at minus one, equal, and plus one, including Git,
scan, event, evidence, action, rows, and rendered report. Attempt to raise bounds
through policy or target fields.

### Input

Run the target.

### Expected writes

None unless an in-bound explicit persistence case is separately exercised.

### Expected behavior

Overflow stops at source/stable-ID boundary with candidate digest, included/
omitted counts, boundary, and tail digest; analysis/data quality are bounded
partial. Omitted work is never sampled or extrapolated.

### Assertions

- [ ] Policy/input cannot raise bounds
- [ ] Same evidence yields same retained prefix/proof
- [ ] Required configuration files are never partially read
- [ ] Truncated trend is not complete
- [ ] Mutation guard passes

## Case 17: Complete sprint retrospective with supported unknowns

### Fixture

Use exact fresh plan/status revisions, period Git range, complete scan, supported
completion, but optional actual-effort and bug metrics absent.

### Input

Run draft, then explicit persist.

### Expected writes

Draft none; persist exact new report and index.

### Expected behavior

Analysis is RETRO_COMPLETE with data quality SUPPORTED_WITH_UNKNOWNS; optional
metrics remain literal UNKNOWN. Persistence becomes WRITTEN only after atomic
read-back. COMPLETE does not mean sprint success/readiness.

### Assertions

- [ ] All 15 report headings appear once/in order, followed by one separate
  evidence record outside the report bytes
- [ ] Metrics and UNKNOWN gaps are fully represented
- [ ] Evidence record binds exact payload/source/target/revision identities
- [ ] Gate/planning/action authority remain NONE/false
- [ ] Stop boundary holds

## Case 18: Milestone retrospective uses the same evidence contract

### Fixture

Use unique milestone plan/status with task-set revision and several bounded
delivery sources. Review-mode/session settings contain values that previously
would trigger a gate.

### Input

Run `milestone:milestone-alpha` with explicit run ID and persist.

### Expected writes

Only the milestone run report and index.

### Expected behavior

Milestone follows identical revision/evidence/UNKNOWN/action/immutability rules.
Review settings are not read. It does not evaluate phase readiness or invoke a
gate.

### Assertions

- [ ] Milestone namespace/path is exact
- [ ] Task-set conflicts are partial
- [ ] Unsupported outcome/readiness remains UNKNOWN
- [ ] No gate/director/planning invocation occurs
- [ ] Transaction is two-path atomic

## Case 19: Analysis, quality, persistence, and evidence axes stay independent

### Fixture

Create blocked target, complete all-supported, complete with optional unknowns,
data conflict, stale status, bounded evidence, draft, write success, unchanged,
conflict, declined, and failure variants.

### Input

Run applicable command for every variant.

### Expected writes

Only successful authorized persistence may change two exact paths.

### Expected behavior

Each response has exact analysis/data-quality/persistence states. Persistence
failure never erases analysis. Nonblocked analysis emits one non-authoritative
`cgs.review-evidence/v1`; blocked emits none.

### Assertions

- [ ] Every branch populates all three axes
- [ ] Partial cannot be relabeled complete by successful write
- [ ] Draft evidence says persistence NONE and report/payload/evidence hashes are
  acyclic
- [ ] Evidence grants no gate/planning/action authority
- [ ] Hashes independently recompute

## Case 20: Terminal stop and zero workflow expansion

### Fixture

Provide sprint/milestone artifacts and requests to start planning, run gate,
update action tracker, edit status, open a new task, archive an old report, or
invoke another skill after draft/save.

### Input

Run draft and persist variants.

### Expected writes

Draft none; persist only new immutable report/index.

### Expected behavior

Workflow returns artifact/index paths/hashes and stops. It may list plain-text
handoffs but does not invoke/preload/start anything or mutate other artifacts.

### Assertions

- [ ] Zero follow-on skill/gate/task/delegation calls occur
- [ ] No retrospective data is automatically passed to planning
- [ ] No action/status/plan/gate/catalog/session file changes
- [ ] No old report is archived or renamed
- [ ] Mutation boundary matches mode exactly

---

## Authoritative P1 traceability

| Audit finding | Closing contract clauses | Behavioral proof |
|---|---|---|
| RT-003 | Every run has immutable ID/path; no update/rename/archive; latest navigation index changes atomically | Cases 10-12 |
| RT-004 | Exact target/revision/plan hash/story-set/source/freshness equality; conflicts preserved as DATA CONFLICT/PARTIAL | Cases 3, 4 |
| RT-005 | Actions begin PROPOSED; owner/due UNASSIGNED until receipt or exact team confirmation | Case 13 |
| RT-006 | Required `sprint:<id>` or `milestone:<id>` grammar, unique type-safe lookup, strict invalid behavior | Cases 1, 2 |
| RT-007 | Immutable canonical `production/retrospectives/<type>/<id>/<run-id>.md` plus sibling index | Cases 10-12 |
| RT-008 | Exact plan period and baseline..terminal graph/timestamp/scope metadata; no recency fallback | Case 8 |
| RT-009 | Scan protocol/tool/version/argv/scope/exclusion/revision equivalence required before trend | Case 9 |

Exactly seven P1 IDs are in scope: RT-003, RT-004, RT-005, RT-006, RT-007,
RT-008, and RT-009. No P2/P3 item is claimed as an authoritative closure by this
trace table, even where adjacent hardening supports deterministic testing.

---

## Pass criteria

- [ ] Every static assertion passes
- [ ] Cases 1-20 pass with required instrumentation
- [ ] Every authoritative P1 ID has positive and negative/boundary proof
- [ ] No plan/tracker revision conflict or stale snapshot enters a supported metric
- [ ] No unsupported metric/cause/owner/deadline is generated
- [ ] No Git or scan trend uses an inferred/incomparable window or protocol
- [ ] Historical retrospective bytes/paths never change
- [ ] Persistence is exactly atomic new report + latest index and is never required
  for analysis completion
- [ ] All source/payload/evidence/observation/action/index/omission hashes recompute
- [ ] Repeated deterministic fixtures preserve metrics, IDs, ordering, and proofs
  apart from controlled run metadata
- [ ] Zero follow-on workflow/task invocation occurs
- [ ] Live skill/spec/metadata, old P0 staging, shared files, and catalog remain
  unchanged by this candidate
