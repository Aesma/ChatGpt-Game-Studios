# Skill Test Spec: `$bug-triage`

## Skill Summary

`$bug-triage` contract `cgs.bug-triage/v2` produces a bounded, revision-bound,
strictly read-only snapshot of canonical `Open` and `Reopened` bug records. It
separates observed severity, severity/priority recommendations, product decisions,
capacity simulation, history trends, dispositions, and committed transactions.

No snapshot or proposal changes a bug, sprint, capacity, waiver, registry, or
report. An external authorized owner/recorder must atomically apply any accepted
decision against exact preimages.

Canonical bug records use only producer schema `cgs-bug-record/v2`. The dotted
legacy spelling `cgs.bug-record/v2` is explicitly unsupported.

---

## Required test instrumentation

Run behavioral cases in an isolated disposable repository fixture. Record:

1. recursive path/type/revision snapshots before and after invocation;
2. every filesystem mutation attempt;
3. every file read, canonical path, exact byte count, and read order;
4. exact registry discovery order, parse states, counters, and bounded omissions;
5. all canonical snapshot/payload/evidence/finding/pair/transaction revisions;
6. a deterministic clock and UUID source; and
7. which files were not read, including noncanonical fallbacks and historical
   sprint files.

The mutation guard passes only when snapshots are byte-identical and the mutation
attempt ledger is empty. If a required observation cannot be captured, mark the
assertion `UNTESTED`, not PASS. Static inspection is not an executed workflow and
must not update catalog result fields.

---

## Static assertions

- [ ] Frontmatter contains only `name` and non-empty `description`
- [ ] Contract version is exactly `cgs.bug-triage/v2`
- [ ] Metadata describes a read-only canonical backlog snapshot and proposals
- [ ] Exact `full`, `sprint`, and `trend --window` grammar is defined
- [ ] Canonical registry root and unresolved/verification/closed statuses are exact
- [ ] Noncanonical QA/playtest/soak/triage inputs remain unregistered candidates
- [ ] Fixed file/byte/history/evidence/pair/finding/row bounds cannot be raised
- [ ] Failed/malformed/duplicate/omitted/bounded reads force partial coverage and
  health UNKNOWN
- [ ] Active sprint resolves only through stable agreeing authority IDs/revisions,
  never mtime or filename order
- [ ] Sprint mode dispatches exactly `cgs.sprint-tracker/v2` or the explicit
  `cgs.sprint-status/v2` legacy adapter into one normalized authority record;
  absent/unknown/malformed schemas fail closed without heuristic fallback
- [ ] The canonical tracker adapter binds source raw version/revision/event, active
  sprint/state, lifecycle owner/recorder, plan path/raw version/revision/story-set
  revision, dates/timezone/unit, complete stories, and typed capacity receipt
  ID/path/revision/raw revision/unit/operands
- [ ] Capacity has one unit, exact arithmetic, per-bug estimates, deterministic
  order, provisional decrement, and overflow protection
- [ ] Observed severity, severity recommendation, confidence, priority
  recommendation, product decision, disposition, and transaction are distinct
- [ ] Missing reproduction data is deterministic and remains visible
- [ ] Duplicate detection has versioned normalization/thresholds, stable pair IDs,
  and no merge/close authority
- [ ] Trend windows and opened/closed/age metrics require immutable sprint and bug
  history identities/timestamps
- [ ] Truth table defines operation, health, coverage, assignment, mutation,
  sprint, capacity, and trend axes for every path
- [ ] Stable findings and `cgs.review-evidence/v1` are non-authoritative and
  persistence/decision/gate authority are false/NONE
- [ ] Recorder proposals bind snapshot and every canonical preimage and require
  atomic two-sided bug+sprint/capacity application
- [ ] No report persistence, changeset authorization, director gate, mutation, or
  workflow chaining exists

---

## Canonical fixture

Unless overridden, use `production/qa/triage-policy.yaml` schema
`cgs.bug-triage-policy/v1` and direct-child `production/qa/bugs/*.md` records with
schema `cgs-bug-record/v2`. Active sprint `sprint-06` uses canonical
`cgs.sprint-tracker/v2`, `cgs.sprint-plan/v2`, one points unit, matching tracker/
plan/story-set/raw revisions and revisions, and a valid capacity receipt. Trend
history uses `cgs.sprint-history/v1`.
Placeholder revisions are replaced by valid explicit version/revision values.

---

## Case 1: Exact modes and fail-fast invocation

### Fixture

Provide a valid project plus unrelated paths and artifacts.

### Input

Run no mode, unknown/multiple modes, paths, extra arguments, duplicate/unknown
options, values beginning with `--`, `--window` in full/sprint, trend without a
window, invalid/date/path-like window IDs, and all three valid commands.

### Expected writes

None.

### Expected behavior

Invalid forms return BLOCKED/UNKNOWN/NONE/UNKNOWN/READ_ONLY_NO_CHANGES before any
project read. Valid forms consume their mode/window once and use no inferred
default.

### Assertions

- [ ] Invalid token and exact reason are reported
- [ ] Invalid forms emit no snapshot, finding, evidence, or proposal
- [ ] Trend requires one lowercase-kebab stable window ID
- [ ] No path or latest artifact is accepted as a mode
- [ ] Mutation guard passes

## Case 2: Only canonical unresolved status enters the backlog

### Fixture

Create canonical records in statuses Open, Reopened, Fixed Pending Verification,
Verified Fixed, Closed, Deferred-as-status, missing, and unknown. Add bug-like QA
plan, playtest, soak, prior-triage, and `production/bugs/` rows. Add otherwise
identical records declaring dotted `cgs.bug-record/v2`, an absent schema, and an
unknown schema.

### Input

Run full.

### Expected writes

None.

### Expected behavior

Only Open/Reopened records enter triage. Verification and closed counts remain
separate. Unsupported/missing status is malformed and makes coverage partial.
Noncanonical rows are not read automatically or counted; explicitly supplied
ones are labeled UNREGISTERED CANDIDATE only.
The dotted/absent/unknown schema records are malformed canonical-root inputs and
make snapshot coverage partial; punctuation is never normalized.

### Assertions

- [ ] DEFERRED is not a status alias
- [ ] No fallback table becomes a canonical bug
- [ ] Only exact `cgs-bug-record/v2` is accepted
- [ ] Counts reconcile with every direct-child canonical record
- [ ] Partial status data makes health UNKNOWN
- [ ] Mutation guard passes

## Case 3: Complete empty registry differs from missing registry

### Fixture

Variant A has existing empty canonical root and valid policy. Variant B lacks the
root. Variant C has complete nonempty S1-S4 backlog.

### Input

Run full for each.

### Expected writes

None.

### Expected behavior

A is TRIAGED/NO_OPEN_BUGS/COMPLETE. B is BLOCKED/UNKNOWN/NONE and names the
expected root. C loads and records declared revisions for all records and reports only unresolved rows in
stable order.

### Assertions

- [ ] Missing registry is never zero bugs
- [ ] Empty registry is reported only after complete discovery
- [ ] Complete nonempty snapshot contains source/policy revisions and counters
- [ ] No variant claims build/release readiness
- [ ] Mutation guard passes

## Case 4: Read failures, malformed records, and duplicate IDs are partial

### Fixture

Discover valid, unreadable, oversized, malformed-schema, missing-ID, duplicate-ID,
revision-changing, and unknown-status records. The readable subset has no critical
bugs.

### Input

Run full.

### Expected writes

None.

### Expected behavior

Every path has byte/revision/parse/ID/status state and exact reason. Counters include
discovered, loaded, failed, duplicate, oversized, omitted, unresolved,
verification, and closed. Result is PARTIAL_TRIAGE/PARTIAL/UNKNOWN; no healthy or
empty conclusion exists.

### Assertions

- [ ] Duplicate IDs never coalesce or select a winner
- [ ] Missing/unreadable records are not zero bugs
- [ ] Input mutation invalidates output rather than mixing versions
- [ ] Loaded subset facts are explicitly local
- [ ] Mutation guard passes

## Case 5: Active sprint resolves by stable authority, never recency

### Fixture

Create agreeing canonical `cgs.sprint-tracker/v2`/session-state sources for
sprint-06 and a newer-mtime sprint-99 plan. The tracker has positive revision,
event ID, ACTIVE identity, stable lifecycle owner/recorder, exact raw tracker
revision, plan path/raw version/revision/story-set revision, dates/timezone/unit, complete
stories, and typed capacity receipt ID/path/revision/raw revision/unit/operands. Run
the same valid normalized fixture through explicit legacy
`cgs.sprint-status/v2`. Add missing, unknown/unversioned/malformed schema,
duplicate-key, missing normalized field, conflicting, dangling, inactive,
out-of-window, plan-revision mismatch, and absent corroboration variants.

### Input

Run sprint for each.

### Expected writes

None.

### Expected behavior

Both exact supported adapters resolve the same sprint-06 authority record and
plan. Newest mtime and filename are ignored. Unknown/malformed/incomplete or
conflicting authority is UNRESOLVED, keeps every bug unassigned, makes capacity
UNKNOWN, and makes operation at least partial; no cross-adapter guessing occurs.

### Assertions

- [ ] Every authority/plan path and revision is reported
- [ ] Canonical tracker raw version/revision/event, ACTIVE ID/state, lifecycle
  owner/recorder, plan raw version/revision/story-set binding, date/timezone/unit,
  stories revision, and capacity receipt ID/path/revision/raw revision/unit/operands
  survive normalization unchanged
- [ ] Unknown or incomplete schema reports `UNSUPPORTED_SPRINT_SCHEMA`
- [ ] Each source declares at most one active ID
- [ ] Full/trend do not read active-sprint artifacts
- [ ] No historical plan is selected as fallback
- [ ] Mutation guard passes

## Case 6: Capacity simulation uses one unit and decrements provisionally

### Fixture

The normalized tracker adapter and plan bind one current raw-versioned capacity
receipt with one exact unit, total 10, committed 4, reserved 2, released 0, and
remaining 4 points.
Ordered bugs require 2, 3, 1, and unknown points. Add mixed-unit, negative,
nonfinite, stale-receipt, arithmetic-mismatch, and already-committed variants.

### Input

Run sprint.

### Expected writes

None; canonical remaining stays four.

### Expected behavior

First 2-point bug is proposed, provisional remaining becomes two; 3-point bug is
overflow; 1-point bug is proposed, final provisional is one; unknown estimate is
capacity-unknown. Invalid capacity yields no active-sprint proposals. Valid
already-committed work is excluded only through a consistent transaction.

### Assertions

- [ ] Formula `total - committed - reserved + released` recomputes remaining
- [ ] Provisional remaining is not reset per bug and never becomes negative
- [ ] Overflow is never assigned and committed scope is never displaced
- [ ] Mixed units cannot be converted implicitly
- [ ] Simulation order and full allocation ledger are deterministic

## Case 7: Severity evidence and confidence cannot be inferred

### Fixture

Use valid S1-S4 records, textual CRITICAL/HIGH/MEDIUM/LOW, missing severity,
complete corroborated impact evidence, self-report-only evidence, conflicting
receipts, and missing policy rule inputs.

### Input

Run full.

### Expected writes

None.

### Expected behavior

Valid canonical values remain observed. Legacy/missing values become
NEEDS_TRIAGE_DATA. Recommendation contains separate rule/evidence locations,
facts, contradictions, limitations, rationale, and policy-computed confidence;
conflict/missing input yields no recommendation confidence.

### Assertions

- [ ] Observed severity is never overwritten by recommendation
- [ ] No silent legacy-enum conversion occurs
- [ ] Model intuition cannot raise confidence
- [ ] Severity recommendation is not product priority
- [ ] Mutation guard passes

## Case 8: Priority and risk dispositions require product authority

### Fixture

Provide priority recommendation only, valid canonical priority decision, invalid
decision missing owner/transaction, deferred proposal, Won't Fix suggestion,
complete accepted-risk waiver/transaction, incomplete/one-sided waiver, and
expired waiver.

### Input

Run full and sprint.

### Expected writes

None.

### Expected behavior

Recommendation stays advisory. Valid decision is reported separately; invalid is
INVALID_PRIORITY_DECISION. DEFERRED leaves status unresolved;
WONT_FIX_CANDIDATE is not closure; only complete consistent waiver is
ACCEPTED_RISK. Invalid/expired risk raises AT_RISK when coverage is complete.

### Assertions

- [ ] P4 is unsupported and maps to no disposition
- [ ] Conversation never creates/renews a decision or waiver
- [ ] Accepted risk binds owner/authority/scope/reason/time/expiry/snapshot/
  preimages/transaction
- [ ] Expired risk cannot suppress health risk
- [ ] Mutation guard passes

## Case 9: Required reproduction schema is deterministic

### Fixture

For separate bugs omit/placeholder numbered steps, expected result, actual result,
build identity, platform profile, or evidence receipt; include one complete bug.

### Input

Run full.

### Expected writes

None.

### Expected behavior

Every incomplete bug remains visible with NEEDS_REPRO_INFO and exact missing
fields. Complete bug passes. Incomplete reproduction cannot become confirmed
impact evidence or disappear from counts.

### Assertions

- [ ] Each required field is checked independently
- [ ] Placeholder and revision-invalid receipt count as missing
- [ ] Missing data is never invented from adjacent bugs
- [ ] Owner handoff requests exact next evidence
- [ ] Mutation guard passes

## Case 10: Duplicate candidates are deterministic and never merged

### Fixture

Create exact symptom stable business keys, fuzzy pairs above/equal/below raw threshold,
different system, incompatible build/platform/severity, missing stable business key data,
and transitive A-B/B-C pairs without A-C match.

### Input

Run full twice.

### Expected writes

None.

### Expected behavior

Exact/fuzzy rules produce stable ordered pair IDs, methods, scores, thresholds,
shared/differing evidence, confidence, and state `POSSIBLE_DUPLICATE`. Missing
inputs are insufficient and receive no duplicate state.
Transitivity is not assumed. Every bug remains open and separate.

### Assertions

- [ ] Raw precision controls threshold equality
- [ ] Pair ID and ordering recompute identically
- [ ] No survivor, merge, close, delete, or exclusion occurs
- [ ] Fuzzy title alone cannot bridge incompatible scope
- [ ] Mutation guard passes

## Case 11: Trend metrics require immutable window and status history

### Fixture

Provide valid sprint-06 window `[start,end)`, open/reopen/close events at boundaries,
ordered history for age, regression/hot-spot identities, and variants with missing,
duplicate, overlapping, unordered, revision-mismatched, open-ended window or absent
event timestamps.

### Input

Run `trend --window sprint-06`.

### Expected writes

None.

### Expected behavior

Valid counts use event times and exact half-open window; net equals opened minus
closed. Age uses first-open and ordered sprint history. Invalid sources make
affected metrics UNKNOWN and trend/operation partial. Mtime/current status/date
never substitutes.

### Assertions

- [ ] Reopen/open and verified-fixed/closed event semantics are explicit
- [ ] Boundary events classify deterministically
- [ ] Observed hot spots include numerator, denominator, window, policy, limits
- [ ] Pattern is not called a cause or automatic priority
- [ ] Trend emits no assignment proposal

## Case 12: Fixed limits produce bounded partial, never healthy sampling

### Fixture

Exercise every fixed limit at minus one, equal, and plus one. Include aggregate
bytes overflow, history overflow, pair explosion, finding overflow, row overflow,
and policy/input attempts to raise limits.

### Input

Run applicable mode for every fixture.

### Expected writes

None.

### Expected behavior

Overflow stops at lexical/stable boundary, records candidate-name revision,
included/omitted counts, boundary key, and tail revision, and returns
PARTIAL_TRIAGE/PARTIAL — BOUNDED REGISTRY/UNKNOWN. No omitted-tail sample or
health extrapolation is allowed.

### Assertions

- [ ] Policy and input cannot raise limits
- [ ] Same input retains identical prefix and omission proof
- [ ] Oversized selected configuration is not partially read
- [ ] Partial output cannot produce a recorder transaction candidate
- [ ] Mutation guard passes

## Case 13: Snapshot revision is stable and stale input is distinct

### Fixture

Runs A/B use identical policy, discovery rows, bytes, counters, and mode-specific
sprint/history context under controlled run metadata. Run C changes one bug byte;
D changes one counter; E changes active sprint/status revision.

### Input

Run the same mode for each.

### Expected writes

None.

### Expected behavior

A/B have the same `registry_snapshot_revision`; C/D/E differ. Run ID/time do not
enter snapshot identity. Old proposals are stale and fail preimage checks.

### Assertions

- [ ] Snapshot revision validates against explicit producer metadata
- [ ] Discovery order is normalized path order
- [ ] revision covers parse states, statuses, counters, policy, and relevant context
- [ ] Derived snapshot is not a registry source of truth
- [ ] Mutation guard passes

## Case 14: Stable finding and evidence identity

### Fixture

Generate one finding; vary paths, titles, descriptions, observed values,
severity/priority recommendation, confidence, state, timestamp, owner name,
snapshot/report revision without changing stable business identity. Then vary category,
bug IDs, sprint/window, policy rule, or transaction/waiver/pair ID. Include
complete and partial snapshots.

### Input

Run twice for every variant.

### Expected writes

None.

### Expected behavior

Noncanonical changes preserve `BTF-<category>-<stable-business-key>`; canonical
changes alter it. Findings coalesce and retain evidence. Each nonblocked snapshot
emits one revision-bound `cgs.review-evidence/v1`; partial coverage is explicit.

### Assertions

- [ ] Finding business key/suffix and explicit payload/record revisions validate against producer metadata
- [ ] Paths/content/values/recommendations/confidence/time/current revision/owner are
  excluded from finding ID
- [ ] Evidence says persistence NONE, authority false/NONE, gate false, read-only
- [ ] Partial evidence cannot support health or transaction
- [ ] Mutation guard passes

## Case 15: Truth table is complete for every outcome

### Fixture

Create invalid invocation, missing registry, missing policy, complete empty,
complete full, complete sprint, complete trend, partial read, unresolved sprint,
partial history, bounded registry, and input-change variants.

### Input

Run the applicable mode.

### Expected writes

None.

### Expected behavior

Every response includes operation, health, coverage, assignment, mutation,
active-sprint, capacity, and trend axes with exact table-compatible values. No
successful or P1-containing path omits operation status.

### Assertions

- [ ] BLOCKED has no snapshot/evidence and health UNKNOWN
- [ ] PARTIAL always has health UNKNOWN
- [ ] Trend assignment is NOT_APPLICABLE
- [ ] Full never claims active capacity
- [ ] Mutation is READ_ONLY_NO_CHANGES in every row

## Case 16: Full and trend cannot masquerade as applied schedule

### Fixture

Provide high-priority bugs and available active sprint, then run full and trend.

### Input

Run each mode.

### Expected writes

None.

### Expected behavior

Full may use PROPOSED:NEXT_SPRINT/BACKLOG or UNASSIGNED_NEEDS_DECISION without
reading active capacity. Trend produces no assignment fields. Neither says
assigned, scheduled, committed, reserved, moved, accepted, or deferred as fact.

### Assertions

- [ ] `assignment_state` is mode-correct
- [ ] No bare Assigned To or Target Sprint wording exists
- [ ] Proposal does not alter capacity
- [ ] No derived report becomes a second schedule source
- [ ] Mutation guard passes

## Case 17: Existing commitments require consistent two-sided transactions

### Fixture

Create bug-only transaction, sprint-only transaction, mismatched IDs, mismatched
capacity delta/unit, changed preimage, and a fully consistent bug+sprint-status+
plan+capacity transaction.

### Input

Run sprint.

### Expected writes

None.

### Expected behavior

Only fully consistent commitment is excluded from new allocation. Every one-
sided/mismatched case is INCONSISTENT_TRANSACTION, unassigned, partial, health
UNKNOWN; the skill does not repair or ratify it.

### Assertions

- [ ] Same transaction ID and unit/delta exist on every canonical side
- [ ] Preimage and postimage revisions validate
- [ ] Inconsistent work is not double-counted or silently accepted
- [ ] Snapshot remains derived/read-only
- [ ] Mutation guard passes

## Case 18: Recorder handoff is complete, atomic, and unapplied

### Fixture

Use a complete sprint proposal and separately exercise priority, assignment,
defer, Won't Fix, and accepted-risk decisions. Remove one required transaction
field at a time.

### Input

Request a transaction proposal in conversation after triage.

### Expected writes

None; no recorder is invoked.

### Expected behavior

Complete `cgs.bug-triage-transaction-proposal/v1` binds snapshot, owner/authority,
bug/sprint/capacity preimages, exact two-sided changes, unit/capacity delta,
overflow, all-or-nothing rule, intended ID, and risk fields when applicable.
Incomplete candidate is ineligible and unapplied.

### Assertions

- [ ] Proposal never claims transaction commitment
- [ ] Either all canonical sides update later or none do
- [ ] Won't Fix/risk requires scope/reason/time/expiry
- [ ] This workflow never applies or verifies the transaction
- [ ] Mutation guard passes

## Case 19: Backlog health is mechanical and not release readiness

### Fixture

Create complete empty, open S1, critical-path blocker, open S2, P1 recommendation,
capacity overflow, inconsistent transaction, invalid/expired risk, unresolved
regression, benign S3/S4-only, and partial-evidence variants.

### Input

Run full/sprint as applicable.

### Expected writes

None.

### Expected behavior

Health follows exact precedence UNKNOWN, NO_OPEN_BUGS, CRITICAL_RISK, AT_RISK,
NO_CRITICAL_FINDINGS. First matching condition wins. Output describes only bug
snapshot health.

### Assertions

- [ ] Partial precedes otherwise benign loaded subset
- [ ] S1/critical path precedes S2/P1/overflow
- [ ] No output says healthy build, safe to ship, release ready, or QA ready
- [ ] Accepted risk does not erase the underlying open bug record
- [ ] Mutation guard passes

## Case 20: Strict read-only and no workflow chaining

### Fixture

Include existing bugs, triage reports, sprint files, capacity, waivers, session
state, catalogs, and user requests to assign/merge/close/defer/accept/write/report/
update/start another workflow.

### Input

Run every mode and those embedded requests.

### Expected writes

None under all variants.

### Expected behavior

The workflow returns one snapshot/proposal and stops. Embedded requests cannot
expand authority. No authorization prompt, director, recorder, issue, report,
mutation, or chained workflow occurs.

### Assertions

- [ ] Before/after recursive snapshots are byte-identical
- [ ] Mutation-attempt ledger is empty
- [ ] No bug/sprint/capacity/risk/report/catalog/session file changes
- [ ] Final line states READ_ONLY_NO_CHANGES
- [ ] Metadata, skill, and spec share this boundary

---

## Audit finding traceability

| Audit finding | Closing contract clauses | Behavioral proof |
|---|---|---|
| BT-004 | Canonical direct-child registry only; exact Open/Reopened filter; noncanonical evidence excluded as UNREGISTERED CANDIDATE | Cases 2-4 |
| BT-005 | Exact tracker/status adapters normalize stable active ID, source revision/raw revision, plan binding, stories and capacity; unknown schema fails closed; no mtime fallback | Case 5 |
| BT-006 | Exact estimate unit/capacity formula, deterministic provisional allocation, decrement and overflow/unassigned states | Case 6 |
| BT-007 | Observed severity, evidence/rule/confidence recommendation, priority recommendation, and human decision are distinct | Cases 7, 8 |
| BT-008 | Immutable sprint window/history events determine opened/closed/net/age; missing data is UNKNOWN | Case 11 |
| BT-009 | Required reproduction validation and stable deterministic duplicate candidates without merge | Cases 9, 10 |
| BT-010 | Complete discovery counters, fixed bounds, partial on unreadable/malformed/duplicate/omitted input, health UNKNOWN | Cases 4, 12 |
| BT-011 | Full truth table separates operation, health, coverage, assignment, mutation, sprint, capacity, and trend on every path | Case 15 |

Additional stable snapshot/finding/evidence, authority, recorder, transaction, and
health boundaries are covered by Cases 13-20.

---

## Pass criteria

- [ ] Every static assertion passes
- [ ] Cases 1-20 pass with required instrumentation
- [ ] Mutation guard passes in every case
- [ ] All snapshot/payload/evidence/finding/pair/transaction/omission revisions
  independently recompute
- [ ] BT-004 through BT-011 each have positive and negative/boundary proof
- [ ] No noncanonical, malformed, duplicate, missing, unreadable, omitted,
  bounded, inconsistent-authority, or incomplete-history input yields healthy
  backlog or applied transaction
- [ ] Capacity never uses mixed units, resets remaining, overallocates, or changes
  canonical state
- [ ] Duplicate/repro/severity/priority/risk output never acquires merge, decision,
  closure, acceptance, assignment, or recorder authority
- [ ] Every response uses the complete truth-table axes
- [ ] Repeated deterministic fixtures produce identical ordering, statistics,
  findings, revisions, and omission proofs apart from controlled run metadata
- [ ] Live skill/spec/metadata, P0 staging, shared files, and catalog remain
  unchanged by this candidate
