---
name: tech-debt
description: Track technical-debt candidates and decisions with idempotent fingerprints, evidence-based advisory scoring, and an append-only register history that is never reordered by reports.
---

# Tech Debt

Analyze, record, rank, and report technical debt without turning heuristics into decisions or destroying register history.

This workflow has four modes. Scanning produces candidate evidence, prioritization produces an advisory view, reporting produces a read-only summary, and only an explicitly authorized recorder phase may mutate the register. It does not invoke another project skill, assign sprint scope, or claim a user/producer decision.

## Invocation

`$tech-debt scan [scope]`  
`$tech-debt add`  
`$tech-debt prioritize [scope]`  
`$tech-debt report [baseline]`

An absent or unknown mode, unsupported argument, or ambiguous scope returns `USAGE_ERROR` with usage text and performs no scan or write. A usage error is not a project-quality verdict.

## Authoritative register

The only authoritative file is `docs/tech-debt-register.md`.

Schema version 2 is an append-only event log. Its immutable header declares the schema; every later record is appended in chronological order. Existing records are never sorted, edited, deleted, or regenerated.

Each event contains:

- `event_id`: collision-resistant UUID;
- `debt_id`: collision-resistant UUID assigned by the first `CREATED` event and never reused;
- `event_type`;
- UTC timestamp and actor;
- fingerprint or fingerprint alias when applicable;
- source revision/hash and evidence locator;
- structured payload plus payload hash;
- previous event ID for that debt item.

Required event types are:

- `CREATED` — immutable identity, fingerprint, category, description, evidence, and acceptance rationale;
- `OBSERVED` — updates materialized `last_seen` for a new source revision without creating another debt item;
- `TRIAGED_OPEN`, `ACCEPTED`, `RESOLVED`, `SUPERSEDED` — status transitions with actor, reason, and evidence;
- `FINGERPRINT_ALIAS` — user-confirmed or repository-proven rename/move relationship;
- `ESTIMATE_UPDATED` — numeric scale values and their evidence;
- `PRIORITY_SELECTED` and `SCHEDULE_SELECTED` — explicit user/producer decisions, never analyzer decisions.

Current state is a materialized view obtained by replaying valid events. Status is one of `OPEN`, `ACCEPTED`, `RESOLVED`, or `SUPERSEDED`; unknown legacy state remains `UNKNOWN` until triage.

A missing register may be proposed for creation during an authorized recorder phase. A malformed or unsupported register returns `REGISTER_ERROR` without modification. Migration is an explicit, separately previewed mutation that preserves every legacy byte in a migration appendix or immutable snapshot reference; never silently reinterpret data.

## Stable fingerprint and identity contract

A scanner finding is a `CANDIDATE`, not accepted debt.

Compute fingerprint version `td-fp-v1` as SHA-256 over these length-delimited fields in order:

1. versioned `rule_id`;
2. canonical project-relative path;
3. stable qualified symbol, or `<file>` when unavailable;
4. normalized evidence text.

Normalization rules are deterministic:

- path is repository-canonical casing, Unicode NFC, and `/` separators;
- symbol is the analyzer-provided qualified name with surrounding whitespace removed;
- evidence text is Unicode NFC, line endings normalized to LF, outer whitespace trimmed, and horizontal whitespace collapsed;
- line/column numbers, scan timestamp, source revision, severity, and suggested priority are excluded.

The scanner records the analyzer/rule version separately. It must not invent a fingerprint when a required field cannot be normalized.

Deduplication:

1. Replay the register and build an index of primary fingerprints and aliases.
2. At most one `CREATED` event may own a fingerprint.
3. If the fingerprint already exists, preserve its `debt_id`. For a new source revision, propose one `OBSERVED` event; for the same revision and evidence hash, propose no event.
4. A previously resolved item that appears again is reported as `REAPPEARED`, but its status does not change until the user records a transition.
5. A line move alone leaves the fingerprint unchanged.
6. A path rename changes the raw fingerprint. Preserve identity only when version-control evidence proves the rename or the user confirms the match; append `FINGERPRINT_ALIAS`. Otherwise treat it as a new candidate and do not auto-resolve the old item.
7. If two existing debt IDs own one fingerprint/alias, or one UUID has conflicting owners, return `REGISTER_ERROR` and do not mutate.

Repeated scans therefore create zero duplicate debt entries. They may append a single new observation event only for a new source revision after authorization.

## Scanner evidence contract

A heuristic is never sufficient by itself to establish debt. Each candidate includes:

- rule ID and analyzer version;
- path, symbol, evidence locator, and evidence excerpt/hash;
- source revision/hash;
- category suggestion and confidence;
- why it may be debt and why it may be intentional;
- verification state `VERIFIED` or `UNVERIFIED`;
- owner-triage state;
- fingerprint and matching register identity, if any.

Exclude generated output, vendored dependencies, caches, build artifacts, and third-party code by canonical path rules. Test files are excluded from generic size/duplication rules unless a test-specific rule is explicitly enabled. TODO, FIXME, HACK, deprecated markers, size thresholds, complexity, and clone results are candidates only.

A missing or failed analyzer marks affected rules `UNVERIFIED` and yields `SCAN_PARTIAL`. It must not fabricate duplication or complexity results.

## Mutation protocol

No mode writes before a complete recorder preview.

The preview contains:

- exact register path and `CREATE` or `APPEND_EVENTS` operation;
- current base content hash or `ABSENT`;
- proposed content hash;
- schema version;
- every selected new event in exact order;
- dedup result and affected debt IDs;
- any migration;
- explicit statement that existing event bytes and order are unchanged.

The user chooses which candidates or decisions to record. Analyzer recommendations are not implicit authorization.

After exact authorization:

1. Re-read and validate the register.
2. Compare its current content hash with the authorized base hash.
3. Replay events and rerun fingerprint, UUID, previous-event, payload-hash, and schema checks.
4. Rebase and deduplicate proposed events against the current revision.
5. If content, event IDs, dedup outcome, or proposed hash changes, write nothing and show a fresh preview for fresh authorization.
6. Commit the complete register replacement atomically from a prepared file.
7. Re-read and verify the authorized hash, append-only prefix/order, event chain, and uniqueness.
8. On any failure, restore the exact base file or leave `ABSENT` unchanged and return `MUTATION_FAILED`.

A revision conflict never uses last-writer-wins. A UUID collision is regenerated before preview; a collision discovered after authorization invalidates authorization.

Declined authorization returns `MUTATION_DECLINED` with no write. A successful verified mutation returns `REGISTER_UPDATED`.

## Mode: scan

1. Resolve a bounded, displayed scope and exclusion set.
2. Read the register and capture its hash; if absent, treat it as an empty materialized view but do not create it yet.
3. Run only declared analyzers and capture source revision/hash.
4. Normalize evidence, compute fingerprints, and deduplicate against registered primary fingerprints and aliases.
5. Present:
   - new candidates;
   - known items seen at a new source revision;
   - unchanged known items;
   - reappeared resolved items;
   - unverified candidates;
   - excluded paths and unsupported checks.
6. Do not accept, resolve, prioritize, or schedule a candidate.
7. If the user asks to record selected results, enter the mutation protocol with exact `CREATED`/`OBSERVED`/status events.

Outcomes:

- `SCAN_COMPLETE` — analysis finished with a complete delta;
- `NO_NEW_DEBT_FOUND` — no new candidate and no new observation event;
- `SCAN_PARTIAL` — one or more requested checks are unverified;
- `REGISTER_UPDATED` — selected events were atomically recorded after authorization.

## Mode: add

Collect an explicit manual record:

- description, canonical affected paths, and evidence;
- category, allowing `UNKNOWN`;
- why the debt is consciously accepted for tracking;
- owner, allowing `UNASSIGNED`;
- initial status;
- numeric impact, frequency, and effort inputs or `UNKNOWN`, each with evidence.

Compute a manual rule fingerprint using `manual@1` plus the normal path/symbol/text fields. Deduplicate before proposing a `CREATED` event. If a match exists, offer an observation or triage event for that stable debt ID instead of a duplicate.

Use the mutation protocol. Outcomes are `REGISTER_UPDATED`, `MUTATION_DECLINED`, `MUTATION_FAILED`, or `REGISTER_ERROR`.

## Mode: prioritize

This mode is read-only. It never rewrites, reorders, or appends to the register, and it never edits sprint plans.

Materialize outstanding `OPEN` and `ACCEPTED` items. Use only recorded numeric inputs with evidence:

### Fixed scales

| Input | Allowed values | Meaning |
|---|---|---|
| Impact | 1, 2, 3, 4 | local inconvenience; component/team cost; milestone/product risk; release/security/data-integrity risk |
| Frequency | 1, 2, 3, 4 | rare/one-off; occasional; repeated each sprint; continuous/core-path |
| Effort points | 1, 2, 3, 5, 8, 13 | team-calibrated implementation points; not elapsed time and not a T-shirt label |

Legacy T-shirt sizes are not converted or summed without a recorded team calibration. Missing, out-of-range, inferred, or evidence-free inputs make the item `UNSCORED`.

For scored items compute exactly:

`advisory_score = (impact * frequency) / effort_points`

Retain the unrounded value for ordering and display three decimal places. Sort only the transient view by:

1. advisory score descending;
2. impact descending;
3. frequency descending;
4. effort points ascending;
5. oldest `CREATED` timestamp first;
6. lexical `debt_id`.

Show the values, evidence, calculation, uncertainty, and tie-break result for every row. List `UNSCORED` items separately in lexical debt-ID order.

Label the result `ADVISORY_ONLY`. The user or producer chooses product priority and scheduling. If they later ask to persist a decision, it must be a separately previewed `PRIORITY_SELECTED` or `SCHEDULE_SELECTED` event through the mutation protocol; the calculated view itself is never written.

Outcomes are `PRIORITY_VIEW_READY`, `PRIORITY_VIEW_PARTIAL` when any requested item is unscored, or `REGISTER_ERROR`.

## Mode: report

This mode is read-only.

Replay the event log and report:

- current counts by category, status, and verification state;
- effort-point distribution and unknown count, never a sum of T-shirt sizes;
- created, observed, accepted, resolved, reopened, and superseded changes since an explicit baseline event cursor or register hash;
- trend only when comparable baselines exist;
- age from stable timestamps and sprint IDs recorded by events;
- items older than three completed sprint transitions, when the active sprint history is available;
- data gaps and invalid/unknown legacy fields.

If no valid baseline exists, label change and trend `UNKNOWN` rather than inventing a previous report. Outcomes are `REPORT_READY`, `REPORT_PARTIAL`, or `REGISTER_ERROR`.

## Outcome rules

- A read-only outcome does not imply register mutation.
- `REGISTER_UPDATED` requires authorized atomic mutation plus post-write verification.
- `SCAN_PARTIAL`, `PRIORITY_VIEW_PARTIAL`, and `REPORT_PARTIAL` must name missing evidence.
- Never use `COMPLETE`, `FAIL`, a severity label, or a score as a substitute for these outcomes.
- Report the register base/final hashes for every attempted mutation and the event cursor used by every report.
