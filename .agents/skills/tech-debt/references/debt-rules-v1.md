# Tech-Debt Rules v1

This file is normative for `$tech-debt`. Keywords **must**, **must not**,
**required**, and **exactly** are contractual.

## 1. Fixed limits and bounded scope

A `cgs.tech-debt-scan-scope/v1` record contains:

- schema, project ID, canonical project root, target commit/ref plus dirty-state
  receipt, manifest ID, generated-at timestamp, and normalized manifest revision;
- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
- explicit exclusion entries with classification, reason, classifier evidence,
  path, size, and revision when readable;
- requested checks, exact rule IDs, analyzer adapter IDs/versions, rulepack/config
  paths and revisions, and declared capabilities;
- allowed read roots and symlink policy; and
- limits plus any owner-approved values lower than the hard caps.

Hard caps:

| Resource | Maximum |
|---|---:|
| Included roots | 16 |
| Directory depth | 24 |
| Included files | 512 |
| Total included bytes | 33,554,432 |
| Bytes per source file | 1,048,576 |
| Requested rules | 128 |
| Analyzer invocations | 16 |
| Analyzer receipts | 64 |
| Candidates returned | 2,048 |
| Evidence/exclusion paths displayed | 256 each |
| Analyzer wall time | 120 seconds each |

Do not follow a symlink/junction/reparse point outside the canonical root. An
unreadable, denied, changed, over-limit, or ambiguous required entry is a coverage
gap. Never silently truncate or sample. If the candidate display cap is reached,
preserve aggregate/result revisions and mark remaining rows `NOT_ENUMERATED`; the
scan is `SCAN_PARTIAL`.

## 2. Classification and exclusions

Every path is one of `INCLUDED`, `EXCLUDED_PROVEN`, or `UNVERIFIED`.

Valid `EXCLUDED_PROVEN` classes are `GENERATED`, `VENDORED`, `THIRD_PARTY`,
`CACHE`, `BUILD_ARTIFACT`, `ENGINE_IMPORT`, and `TEST_FIXTURE`. Classification
requires current evidence such as an owner-approved manifest, dependency lock/
package boundary, engine build/import declaration, generator marker plus producer
identity, or repository attribute. Directory naming alone is insufficient.

Generic size/clone rules exclude paths proven `TEST_FIXTURE`. A rule whose ID and
rulepack explicitly state `applies_to_tests: true` may include them. Unclassified
tests and generated/vendor-like paths are `UNVERIFIED`; they do not silently enter
or leave coverage.

## 3. Rule and analyzer registry

Each requested rule has a registry entry:

```text
rule_id                     globally stable semantic rule key
rule_version                immutable rule semantics version
rulepack_id/version/revision    exact packaged rule definition
evidence_kind               MARKER | SIZE | AST_COMPLEXITY | TOKEN_CLONE |
                            MANUAL | OTHER_DECLARED
supported_languages         explicit set
required_capability         exact adapter capability
default_thresholds          units and numeric values
test_policy                 EXCLUDE_GENERIC | INCLUDE_EXPLICIT
candidate_only              true
```

Renaming diagnostic prose, bumping an analyzer patch, or changing a display title
must not change `rule_id`. A semantic change requires a new `rule_version` and may
require an explicit stable key migration/alias proposal; never silently split or
merge identities.

Analyzer adapter entries define adapter ID/version/revision, executable identity,
supported languages/file types/rules, parser mode, AST/control-flow/clone
capabilities, output schema, read-only argv template, deterministic config inputs,
side-effect declaration, timeout semantics, and compatible rulepack versions.

There is no built-in complexity or clone analyzer. Without a compatible registry
entry and successful receipt, those checks are `UNSUPPORTED` or `UNVERIFIED`.
Text matching does not satisfy either capability.

## 4. Analyzer receipt

Each requested check emits `cgs.tech-debt-analyzer-receipt/v1`:

```text
receipt_id                  UUIDv4
schema
project_id / target_id / scope_manifest_revision
adapter_id / adapter_version / adapter_revision
executable / executable_version / executable_revision when available
rule_id / rule_version / rulepack_id / rulepack_version / rulepack_revision
config_revision
exact redacted argv / canonical cwd
included_subset_manifest_revision
started_at / ended_at / deadline_ms / exit_code / timed_out
status                      COMPLETE | PARTIAL | ERROR | UNSUPPORTED
scanned/excluded/unreadable/unsupported/over_limit counts and bytes
raw_result_revision / normalized_result_revision / redacted_log_revision
side_effect_status          NONE_OBSERVED | MUTATION_OBSERVED | UNVERIFIED
limitations
```

`COMPLETE` requires correct version/capability, exact target subset, successful
parse/execution, zero unexplained mutation, within-limit completion, and hashable
results. Unknown version, stale target, parser rejection, timeout, nonzero exit,
malformed output, partial file support, unhashable result, or mutation is not a
successful check. Preserve independent successful receipts, but classify affected
candidates/checks `UNVERIFIED` and the scan `SCAN_PARTIAL`.

## 5. Candidate schema and evidence states

A `cgs.tech-debt-candidate/v2` contains:

```text
candidate_id                TDC- plus first non-empty stable value of stable key, or
                            TDC-UNVERIFIED-<receipt UUID> when no stable key
state                       HEURISTIC_CANDIDATE | EVIDENCE_SUPPORTED | UNVERIFIED
rule_id / rule_version
project_id / target_id / source revision
scope_manifest_revision
canonical path / stable qualified symbol or <file>
Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
evidence excerpt revision; redacted bounded excerpt only when safe
analyzer receipt IDs and revisions
defect_class / category suggestion or UNKNOWN
why_debt / why_intentional
confidence and basis
owner_triage                 REQUIRED | SELECTED | REJECTED | DEFERRED
stable_key_version / stable_key or UNKNOWN
register_match               NEW | MATCHED | UNCHANGED | REAPPEARED | UNKNOWN
matched debt_id and event cursor when applicable
limitations / stale_key
```

`HEURISTIC_CANDIDATE` is required for marker, file-size, naming, or keyword rules,
even when the text scan receipt is complete. `EVIDENCE_SUPPORTED` requires a
successful analyzer/manual evidence contract appropriate to the rule, but remains
a candidate until a human owner selects it. `UNVERIFIED` covers missing identity,
unsupported analysis, incomplete evidence, or changed input.

A candidate never asserts accepted debt, severity, product priority, schedule,
or lifecycle state. `owner_triage: SELECTED` authorizes only proposal construction,
not persistence or risk/debt acceptance.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

## 6. Stable key v2

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

```text
td-key-v1
rule_id                     stable semantic key, not analyzer version
canonical project-relative path
stable qualified symbol or <file>
defect_class                stable controlled token
semantic_evidence_key       analyzer structural key or normalized manual key
```

For marker rules, `semantic_evidence_key` is the marker class plus normalized
marker body after removing the marker token and volatile issue/line formatting.
For size rules it is the declared metric kind, not the observed numeric value.
For AST/clone rules it is the adapter-provided stable structural identity. For
`manual@2`, normalize the explicit defect class and concise description by NFC,
LF, trim, lowercase where language-safe, and collapsed horizontal whitespace.

Exclude volatile observation data from the stable key: line/column/byte offsets,
observed size, thresholds, timestamps, tool versions, diagnostic wording, excerpts,
confidence, severity, score, owner, and lifecycle state.

The scanner records all excluded evidence separately. If a required field is
ambiguous or an analyzer cannot provide a stable structural identity, stable key
is `UNKNOWN`; do not synthesize one.

Aliases use `cgs.tech-debt-key-alias/v1`: old/new stable keys, stable
debt UUID, VCS move/copy evidence identity or explicit user selection, exact
source identities, reason, proposer, and proposal revision. The analyzer may propose
an alias; only the recorder can append it.

## 7. Register v3

The register is canonical UTF-8 with LF endings using
`canonical-json-lines/v1`. Record 1 is one immutable `GENESIS` record. Later
transactions append zero or more ordered `EVENT` records followed by exactly one
`COMMIT` marker. An event is authoritative only through the latest valid commit.
Existing genesis, event, and commit bytes are never edited, deleted, or reordered.

Immutable `GENESIS` fields:

```text
schema                      cgs.tech-debt-register/v3
record_type                 GENESIS
register_id                 UUIDv4
project_id                  stable project UUID/ID
created_at                  RFC 3339 UTC
serialization               canonical-json-lines/v1
id_strategy              stable-fields
stable_key_version         td-key-v1
event_schema                cgs.tech-debt-event/v3
```

Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.

Each `cgs.tech-debt-event/v3` contains:

```text
event_id / debt_id          unique UUIDv4 values (debt_id repeats across its chain)
sequence                    global integer, previous + 1
event_type
occurred_at                 RFC 3339 UTC
actor_id / actor_role / authority_ref
source_target_id / source_revision / evidence_refs
stable key / alias fields when applicable
previous_global_event_id/revision
previous_debt_event_id/revision or NONE
payload / payload_revision
event_revision                  positive monotonic event revision
```

`authority_ref` may be `NONE` only for mechanical `CREATED`, `OBSERVED`, and
analyzer-derived estimate proposals that have independent selection evidence.
Lifecycle, acceptance, resolution, priority, and scheduling events require exact
authorized owner/producer evidence in their payload.

Required event types and payloads:

| Event | Required payload and effect |
|---|---|
| `CREATED` | primary stable key, description, defect class, category/owner or UNKNOWN/UNASSIGNED, initial evidence; creates `OPEN` |
| `OBSERVED` | new source identity/evidence revision and observation reason; status unchanged |
| `TRIAGED_OPEN` | owner, triage reason, evidence; status `OPEN` |
| `ACCEPTED` | authorized owner, acceptance reason, known consequences, controls, review/expiry trigger; status `ACCEPTED` |
| `REOPENED` | authorized owner, reappearance/new evidence, reason; `RESOLVED` to `OPEN` |
| `RESOLVED` | authorized resolver, resolution reason, changed artifact/test evidence revisions, verification reference; status `RESOLVED` |
| `SUPERSEDED` | authorized owner, reason, successor debt UUID(s); status `SUPERSEDED` |
| `STABLE_KEY_ALIAS` | alias record and move/user evidence; status unchanged |
| `ESTIMATE_UPDATED` | impact/frequency/effort values or UNKNOWN, scale/version, evidence; status unchanged |
| `PRIORITY_SELECTED` | producer/user decision, reason, source advisory view revision; status unchanged |
| `SCHEDULE_SELECTED` | producer decision, sprint/milestone identity and reason; status unchanged |

Valid lifecycle transitions:

```text
NONE       --CREATED------> OPEN
OPEN       --TRIAGED_OPEN-> OPEN
OPEN       --ACCEPTED-----> ACCEPTED
OPEN       --RESOLVED-----> RESOLVED
OPEN       --SUPERSEDED---> SUPERSEDED
ACCEPTED   --TRIAGED_OPEN-> OPEN
ACCEPTED   --ACCEPTED-----> ACCEPTED (new review/terms required)
ACCEPTED   --RESOLVED-----> RESOLVED
ACCEPTED   --SUPERSEDED---> SUPERSEDED
RESOLVED   --REOPENED-----> OPEN
RESOLVED   --SUPERSEDED---> SUPERSEDED
```

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

The materialized item view contains stable debt ID, primary/alias stable keys,
status, owner, created/last-observed/last-transition timestamps, acceptance terms,
resolution/supersession evidence, current estimates, selected decisions, source
evidence, and head event. It is derived by replay and is never authoritative.

## 8. Missing, legacy, and invalid registers

- `ABSENT:<canonical-path>` is valid only when the path is confirmed absent.
  Analyzer modes produce an empty/partial view and may construct a
  `CREATE_REGISTER` proposal. They never create the file.
- A valid recognized v1/v2 register produces `REGISTER_ERROR` subtype
  `MIGRATION_REQUIRED`. A migration proposal must bind every original byte by
  revision and either preserve those bytes in an immutable appendix or point to an
  immutable snapshot. It must define deterministic ID/stable key/status mappings
  and all `UNKNOWN` fields. Migration needs a separate recorder transaction and
  new exact authorization.
- An unrecognized schema, malformed syntax, revision/chain mismatch, invalid
  lifecycle, or conflicting owner is `REGISTER_ERROR`. Do not repair, append,
  migrate, or compute a misleading partial register view.

## 9. Dedup and observation rules

Replay the valid register into one index of primary stable keys and aliases.
Exactly one `CREATED` event owns a stable key. For each candidate:

1. No match: classify `NEW`; after owner selection propose one `CREATED` event.
2. Match and same source identity plus evidence revision as the last observation:
   classify `UNCHANGED`; propose nothing.
3. Match and materially new evidence at a new source identity: classify `MATCHED`;
   after owner selection propose one `OBSERVED` event. Metric-only churn excluded
   from `td-key-v1` may be evidence for an observation.
4. Match with current `RESOLVED`: classify `REAPPEARED`; propose no state change
   unless an owner separately selects `REOPENED` with evidence/reason.
5. Suspected move: propose an alias only with exact evidence from Section 6.

Multiple candidates with one stable key in one run collapse to one candidate
with all source evidence. Any ambiguity is explicit and no event is proposed.

## 10. Advisory scoring

Allowed scales and formula are those in `SKILL.md`. Each value identifies its
latest valid `ESTIMATE_UPDATED` event and evidence revision. Exact rational comparison
must be used for ordering; floating-point rounding is display-only.

Tie-break in exact order: score descending, impact descending, frequency
descending, effort ascending, oldest valid `CREATED.occurred_at`, lexical UUID.
Unscored rows never intermix with scored rows. An advisory view has a view ID,
register ID/revision/revision/head, selection filter, generated-at timestamp, row
inputs/evidence/formula/tie-break trace, gaps, and normalized view revision.

`PRIORITY_SELECTED` and `SCHEDULE_SELECTED` record human decisions and may differ
from the advisory order. The analyzer cannot emit those events without exact user/
producer selection and cannot persist them.

## 11. Reporting and baselines

A baseline event must exist in the current global chain. A baseline register revision
must identify an immutable ancestor whose head event/revision can be proven. A sibling,
future, corrupt, unrelated, or ambiguous baseline is `INPUT_ERROR`. No baseline
means point-in-time counts only and change/trend `UNKNOWN`.

Trend compares identical metric definitions and exact event intervals. Timestamps
are RFC 3339 UTC. Sprint aging requires ordered, immutable sprint transition IDs
and completed timestamps; calendar guesses or current sprint names are invalid.

## 12. Change proposal schema

`cgs.tech-debt-change-proposal/v1` contains:

```text
proposal_id / proposal_revision
created_at / expires_at
project_id / target_id
register path / register_id or RESERVED_UUID
schema / operation
base_content_revision or ABSENT
base_revision / base_last_event_id/revision
ordered exact event bytes / reserved event and debt UUIDs
dedup index revision / selected candidate or decision revisions
authority references required by event types
proposed revision / last event ID/revision / content revision
append_only_proof
stale_key
persisted=false / authorization=false
```

The proposal is deterministic except for explicitly reserved UUIDs/timestamps;
these are included in its revision. Any changed byte, UUID, time, event order, dedup
result, base, authority reference, or proposed revision is a new proposal requiring
fresh selection and authorization.

## 13. Independent recorder protocol

`cgs.tech-debt-recorder/v1` is a separate component/workflow. The analyzer does
not call it. A conforming recorder must:

1. accept one exact proposal revision plus separate current authorization identifying
   operation, register path, event IDs, final revision, authorizer, and expiry;
2. acquire an implementation-defined exclusive lock or use a filesystem/database
   primitive that supports atomic conflict check;
3. reread and validate the current register schema, chains, lifecycle,
   stable key ownership, and current UUID uniqueness;
4. Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.
5. return `UUID_COLLISION` without regenerating/writing when a reserved proposal
   UUID now exists in different content; regeneration creates a new proposal and
   requires fresh authorization;
6. compare the exact base tuple `(path, register_id, content_revision, revision,
   last_event_id, last_event_revision)` or confirmed absence, and return
   `CAS_CONFLICT` without writing if any other part changed;
7. revalidate proposal bytes, authority, reserved UUID uniqueness, lifecycle,
   predecessors, and event/payload/commit/final revisions against that exact base;
8. write a same-directory prepared file, flush it, atomically replace/create the
   target, and flush directory metadata when the platform supports it;
9. reread and verify exact final revision, revision/head, prior-byte prefix/order,
   chains, lifecycle, ownership, and uniqueness; and
10. emit an immutable recorder receipt containing base/final identity, lock/atomic conflict check/
    atomicity evidence, authorization identity/revision, event IDs, timings, result,
    and receipt revision.

Recorder results are exactly `RECORDER_COMMITTED`, `ALREADY_APPLIED`,
`CAS_CONFLICT`, `UUID_COLLISION`, `AUTHORIZATION_INVALID`, `PROPOSAL_INVALID`, or
`RECORDER_FAILED`. On any result other than the first two, the original target
must remain byte-identical or absence must remain. There is no last-writer-wins.

After `CAS_CONFLICT`, analysis may replay the new valid register and construct a
fresh proposal, but it must not automatically write or reuse the old
authorization. Conflict retry therefore means **re-analyze → new proposal → new
authorization → new recorder transaction**, not a hidden write retry.

## 14. Result envelope

Every result includes:

```text
schema: cgs.tech-debt-analysis/v2
mode / outcome / normalized invocation
project/target/scope identity and revisions
register path/presence/schema/id/revision/revision/head
input records and revisions
coverage ledger / fixed-limit use / exclusions / gaps
analyzer receipts and revisions
candidates / stable keys / dedup classifications
materialized lifecycle view revision
advisory view or report/baseline as applicable
change proposal or NONE
before/after mutation snapshot revisions and changed paths
register_mutated=false
proposal_persisted=false
decision_authority_exercised=false
stale_key
```

The stale key includes project target identity, scope/input revisions, register base
identity, analyzer/rulepack/config revisions, and baseline identity. Any change makes
the result stale. Confirmed candidates remain visible under a partial outcome;
uncertainty never becomes a debt decision or a clean claim.
