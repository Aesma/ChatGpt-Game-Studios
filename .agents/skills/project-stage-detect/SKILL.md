---
name: project-stage-detect
description: "Read-only project-stage evidence service that validates catalog-backed versioned stage authority and current hash-bound receipts, reports deterministic blockers and contradictions, and never infers progress from artifact counts."
---

## Invocation and execution

Invoke this workflow as `$project-stage-detect [general|programmer|designer|producer]`.

No argument means `general`. The optional role filters only the final
recommendation. Reject unknown, repeated, positional, or combined arguments with
`ERROR` before scanning.

This workflow is strictly read-only. It has no changeset, authorization prompt,
persistent report, stage mutation, gate invocation, recorder invocation, or
director delegation. It returns one canonical conversation packet with schema
`cgs.project-stage-detection/v2`.

Result is exactly `DETECTED`, `CONFLICT`, `UNKNOWN`, or `ERROR`.
`resolution_state` is `CLEAR` only for a clean `DETECTED` result and `BLOCKED`
otherwise. `detected_stage` is one of `Concept`, `Systems Design`, `Technical
Setup`, `Pre-Production`, `Production`, `Polish`, `Release`, or `UNKNOWN`.
Confidence is exactly `HIGH`, `MEDIUM`, or `LOW`.

No result, confidence, or recommendation authorizes a gate or stage transition.

---

## Phase 0: Resolve the catalog-backed contract

Resolve exactly one workspace root. Reject traversal, outside-root paths,
symlink escape, or ambiguous roots. Normalize repository-relative paths with `/`
for identity and retain raw bytes for hashing.

The only stage-policy source is `.codex/docs/workflow-catalog.yaml`. Read and
hash its exact raw bytes before reading any authority record. A usable catalog
contract must be versioned and must declare, without relying on this skill to
fill defaults:

- a unique catalog schema and version;
- the canonical `cgs.project-stage-detection/v2` packet schema identity;
- the exact stage enum and initial-stage rule;
- one stable ID for every allowed transition;
- exact `from` and `to` stages, authorized owner, gate profile, and required
  receipt schema for every transition;
- the canonical authority-record path and authority schema version;
- receipt, previous-record continuity, target commit/ref, dirty-state,
  freshness, and source/build/test/artifact manifest policies; and
- deterministic read limits: maximum referenced entries, maximum bytes per
  entry, and maximum total bytes.

If the catalog is readable but any required contract field is missing,
duplicated, malformed, unsupported, or internally inconsistent, record
`STAGE_SCHEMA_UNVERIFIED` and return `UNKNOWN`. Do not copy a transition table,
owner map, receipt rule, authority path, or fallback read limit into this skill.
If the catalog cannot be read at all, return `ERROR`.

`production/stage.txt`, when present, is read only as a `LEGACY_DECLARATION`.
It is never the authority-record path, never supplies a transition, and never
selects `detected_stage`.

---

## Phase 1: Freeze the deterministic read closure

Set `snapshot_at` once in UTC. Record VCS commit/ref and dirty-state evidence
when available. Apply the catalog's dirty-state policy; unavailable required VCS
identity is a coverage gap, never a guessed clean state.

Build the read closure in this order only:

1. the exact workflow catalog;
2. the catalog-declared authority record, plus optional legacy `stage.txt`;
3. the exact previous authority record referenced by the current record;
4. the exact gate receipts referenced by the current record; and
5. the exact source, build, test, configuration, and artifact manifests and
   entries referenced by those receipts under the catalog policy.

Do not glob for the newest record, discover alternate receipts, recursively
inventory `src/`, or inspect advisory artifacts outside this closure. Stop
before crossing any catalog read limit. Record `READ_BUDGET_EXCEEDED` with the
declared and observed limit; do not silently truncate and continue.

For every closure item, record an explicit `PRESENT`, `ABSENT`, `UNREADABLE`,
`MALFORMED`, or `CHANGED_DURING_SCAN` source state. Hash exact raw bytes with
lowercase SHA-256. An absence marker is data in the snapshot; it is not the hash
of an empty file.

Evidence IDs are the lowercase SHA-256 of canonical JSON containing provenance,
normalized path, relevant field/section, source state, and raw hash or absence
marker. Sort snapshot entries by normalized path and field, serialize canonical
JSON as UTF-8 without BOM, and hash it to produce `snapshot_manifest_hash`.
Each evidence record includes its ID, provenance, path, field/section,
`snapshot_at`, observed hash or absence marker, expected hash when applicable,
validation state, and reason codes.

Allowed provenance values are:

| Provenance | Meaning |
|---|---|
| `CATALOG_AUTHORITY` | versioned workflow and stage policy |
| `AUTHORITY_RECORD` | stage state written by the catalog-authorized owner |
| `GATE_RECEIPT` | immutable evidence for one allowed transition |
| `SOURCE_SNAPSHOT` | exact current source/build/test/config/artifact bytes |
| `LEGACY_DECLARATION` | unversioned text such as `production/stage.txt` |
| `COVERAGE_GAP` | missing, unreadable, malformed, stale, unsupported, or over-limit evidence |

Re-read and re-hash every readable closure item before classification. Record
`reverified_at` in UTC. A required item changed between reads produces
`CHANGED_DURING_SCAN` and prevents `DETECTED`; never combine bytes from different
moments into one clean snapshot.

---

## Phase 2: Validate authority, transition, and receipts

A stage authority record is valid only when it conforms to the catalog-declared
authority schema and supplies:

- schema version and exact catalog version/hash;
- exact stage enum and transition ID;
- authorized owner and `updated_at` timestamp;
- `transition_from`, including the catalog-defined initial-stage rule;
- target commit/ref and dirty-state binding;
- canonical source snapshot/manifest identity;
- exact required receipt IDs, paths, schemas, and raw hashes;
- previous authority-record path/hash required by continuity policy; and
- a record ID/hash that validates under the declared canonicalization rule.

Validate the transition ID, from/to pair, owner, initial-stage rule, continuity,
target, dirty-state, and freshness directly against the same catalog bytes.

Every required receipt must validate its stable ID, schema version, transition
ID, exact from/to stage, gate/profile identity, final eligible `PASS`, authorized
approver, passed-at timestamp, target commit/dirty state, source/build/test and
required artifact manifests, receipt raw hash, and freshness. Recompute every
referenced current hash. A receipt verdict string or filename without the exact
catalog-bound evidence is not a valid receipt.

A parsable authority claim that disagrees with the catalog, owner, transition,
continuity, receipt, target, or current stable hashes is a contradiction. A
missing or unreadable required source is a coverage gap rather than invented
contradictory content.

Plain `production/stage.txt` remains non-authoritative even when its value is a
valid stage enum. Preserve its value and hash as `declared_stage` only when no
versioned authority claim supplies that field; never promote it to
`detected_stage`.

---

## Phase 3: Exclude proxy progress signals

No recursive source or artifact inventory is permitted. Directory names,
artifact presence, GDD/ADR/story/test counts, lines of code, engine
configuration, prototype counts, sprint files, and source-file thresholds never
select or advance a stage, validate a transition, replace a receipt, or raise
confidence.

Generated, vendor, example, cache, imported, and third-party files are never
discovered for advisory counting. If a catalog-valid receipt explicitly binds
one, validate its exact hash only as part of that receipt; its category and
quantity carry no stage meaning.

Do not emit completion percentages, ranges, estimates, weighted scores,
progress bars, file totals, or time-to-next-stage estimates. This workflow owns
no versioned measurement formula or denominator.

`advisory_observations` may contain only non-authoritative facts already present
in the deterministic read closure, such as a legacy declaration. Do not expand
the closure to make the section more informative.

---

## Phase 4: Determine result, blocking reasons, and confidence

Apply this precedence and do not normalize one outcome into another:

### `ERROR`

Return `ERROR`, `detected_stage: UNKNOWN`, `resolution_state: BLOCKED`, and
`confidence: LOW` for invalid invocation/root, an unreadable catalog, no readable
evidence source, or global hashing/integrity failure that prevents a trustworthy
snapshot.

### `CONFLICT`

Return `CONFLICT`, `detected_stage: UNKNOWN`, `resolution_state: BLOCKED`, and
`confidence: LOW` only when readable stable evidence makes a positive
contradiction: unknown stage enum in a parsable authority record, invalid
transition/owner/continuity, wrong receipt identity or verdict, expected versus
observed hash mismatch, conflicting authority records in the declared chain, or
target/build/source disagreement. Preserve the claimed value separately as
`declared_stage`.

### `UNKNOWN`

Return `UNKNOWN`, `detected_stage: UNKNOWN`, and `resolution_state: BLOCKED` when
authority cannot be established without guessing, including:

- readable catalog with a missing/unsupported stage contract;
- no authority record or only a legacy declaration;
- malformed authority with no stable parsable claim;
- missing or unreadable required receipt, manifest, or current source;
- required VCS identity unavailable;
- read budget exceeded; or
- required evidence changed during the scan.

Confidence is `LOW` for a missing/invalid authority chain or any critical gap.
It may be `MEDIUM` only when the catalog explicitly declares a gap
non-authoritative and incapable of affecting authority, currentness, or
freshness. `MEDIUM` never authorizes an unknown stage.

### `DETECTED`

Return `DETECTED`, the exact authority stage, and `resolution_state: CLEAR` only
when one complete catalog-valid authority chain, allowed transition and owner,
all required receipts, current target, stable source/build/test/artifact hashes,
and the end-of-scan rehash agree with no contradiction or blocking gap.

Confidence is `HIGH` for a complete current chain. It may be `MEDIUM` only when
the catalog explicitly permits a non-authoritative gap that cannot affect the
stage or freshness.

Never use `PASS`, `CONCERNS`, or `FAIL` as confidence values. `BLOCKED` is a
resolution state, not a fifth result or a confidence value.

Use stable blocking reason codes, including when applicable:
`INVALID_INVOCATION`, `INVALID_ROOT`, `CATALOG_UNREADABLE`,
`STAGE_SCHEMA_UNVERIFIED`, `AUTHORITY_MISSING`, `AUTHORITY_UNREADABLE`,
`AUTHORITY_MALFORMED`, `UNKNOWN_STAGE_ENUM`, `INVALID_TRANSITION`,
`UNAUTHORIZED_OWNER`, `CONTINUITY_MISMATCH`, `RECEIPT_MISSING`,
`RECEIPT_UNREADABLE`, `RECEIPT_INVALID`, `TARGET_UNVERIFIED`,
`HASH_MISMATCH`, `READ_BUDGET_EXCEEDED`, and `CHANGED_DURING_SCAN`.

---

## Phase 5: Return one canonical packet

Return in conversation only. Preserve list order defined by the canonical schema;
do not omit empty required lists or substitute prose for structured fields.

```yaml
schema: cgs.project-stage-detection/v2
schema_version: 2
completion_marker: COMPLETE
packet_id: sha256:<canonical-core-payload>
project:
  root_id: sha256:<canonical-real-root-identity>
catalog:
  path: .codex/docs/workflow-catalog.yaml
  schema_version: <value-or-UNVERIFIED>
  catalog_version: <value-or-UNVERIFIED>
  raw_sha256: <sha256>
  stage_authority_schema_version: <value-or-UNVERIFIED>
snapshot:
  snapshot_at: <UTC>
  reverified_at: <UTC>
  vcs_commit: <hash-or-UNVERIFIED>
  vcs_ref: <ref-or-UNVERIFIED>
  dirty_state: <clean|dirty|UNVERIFIED>
  manifest_sha256: <sha256>
  entries:
    - path: <normalized-repository-relative-path>
      field: <field-or-section>
      source_state: PRESENT | ABSENT | UNREADABLE | MALFORMED | CHANGED_DURING_SCAN
      raw_sha256: <sha256-or-ABSENT-or-UNVERIFIED>
      snapshot_at: <UTC>
result: DETECTED | CONFLICT | UNKNOWN | ERROR
resolution_state: CLEAR | BLOCKED
detected_stage: Concept | Systems Design | Technical Setup | Pre-Production | Production | Polish | Release | UNKNOWN
declared_stage: <authority-claim-or-legacy-value-or-NONE>
confidence: HIGH | MEDIUM | LOW
authority:
  schema_version: <value-or-UNVERIFIED>
  record_id: <id-or-NONE>
  record_path: <path-or-NONE>
  record_sha256: <sha256-or-NONE>
  owner: <owner-or-UNVERIFIED>
  transition_id: <id-or-UNVERIFIED>
  transition_from: <stage-or-UNVERIFIED>
  previous_record_sha256: <sha256-or-NONE-or-UNVERIFIED>
receipts:
  required: <count-or-UNVERIFIED>
  valid: <count>
  records:
    - id: <stable-id>
      schema_version: <version>
      path: <path>
      expected_sha256: <sha256>
      observed_sha256: <sha256-or-UNVERIFIED>
      state: VALID | INVALID | STALE | UNVERIFIED
evidence:
  - id: <stable-id>
    provenance: CATALOG_AUTHORITY | AUTHORITY_RECORD | GATE_RECEIPT | SOURCE_SNAPSHOT | LEGACY_DECLARATION | COVERAGE_GAP
    path: <path>
    field: <field-or-section>
    snapshot_at: <UTC>
    expected_sha256: <sha256-or-NOT_APPLICABLE>
    observed_sha256: <sha256-or-ABSENT-or-UNVERIFIED>
    state: VALID | INVALID | STALE | UNVERIFIED | NOT_APPLICABLE
    reason_codes: [<stable-code>]
contradictions:
  - id: <stable-id>
    field: <field>
    expected: <redacted-value-or-hash>
    observed: <redacted-value-or-hash>
    evidence_ids: [<stable-id>]
read_errors:
  - evidence_id: <stable-id>
    reason_code: <stable-code>
coverage_gaps:
  - evidence_id: <stable-id>
    reason_code: <stable-code>
    blocking: <true|false>
blocking_reason_codes: [<stable-code>]
advisory_observations:
  - evidence_id: <stable-id>
    observation: <non-authoritative-fact-from-read-closure>
recommendation:
  role: general | programmer | designer | producer
  action: <one evidence-resolution or formal-transition handoff>
disclaimer: ADVISORY DETECTION ONLY — NOT A GATE OR TRANSITION
```

`packet_id` is the SHA-256 of canonical JSON for every field from `schema`
through `advisory_observations`, excluding `packet_id` itself and excluding the
role-dependent `recommendation`. This keeps the evidence identity stable across
role filters while exact serialized packet bytes may differ in recommendation.

For the same frozen snapshot, every field except `recommendation.role` and its
wording must be byte-for-byte identical across role filters.

Give at most one next action: resolve the first deterministic blocking reason,
run a separately authorized formal gate when advancement is desired, or align a
consumer to this packet schema. Do not invoke the action.

---

## Read-only and consumer boundaries

Never write `production/project-stage-report.md`, `production/stage.txt`, an
authority record, receipt, packet, cache, checkpoint, or any project file. Never
ask to persist this packet inside this workflow.

Do not invoke `$gate-check`, `$start`, `$help`, `$studio-status`, another project
skill, an agent, or a recorder. A handoff is text only.

Consumers must validate the complete canonical
`cgs.project-stage-detection/v2` packet, catalog hash, packet ID, project root ID,
and current snapshot before use. They must not parse a prose stage line,
recalculate stage from artifacts, treat `UNKNOWN`/`CONFLICT` as a stage, or use
this detector as gate approval.

## Non-negotiable rules

- Never mutate the project or request write authorization.
- Never invent missing catalog authority policy.
- Never infer a stage from file, source, or artifact counts.
- Never emit completion percentages, progress scores, or time estimates.
- Never treat an unversioned stage value as authoritative.
- Never hide read errors, contradictions, stale evidence, or scan limits.
- Never use detection as permission to advance.
