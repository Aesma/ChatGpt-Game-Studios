---
name: project-stage-detect
description: "Read-only project-stage evidence service that validates versioned stage declarations and gate receipts against current source hashes, reports confidence and contradictions, and never infers progress from artifact counts."
---

## Invocation and execution

Invoke this workflow as `$project-stage-detect [general|programmer|designer|producer]`.

No argument means `general`. The optional role filters only the final
recommendation; it never changes evidence, stage, result state, or confidence.
Reject unknown, repeated, or combined roles with `ERROR`.

This workflow is strictly read-only. It has no changeset, authorization prompt,
persistent report, stage mutation, gate invocation, or director delegation.

Output schema: `project_stage_detection/v2`.

Result state is exactly one of:

- `DETECTED`;
- `CONFLICT`;
- `UNKNOWN`; or
- `ERROR`.

`detected_stage` is one of `Concept`, `Systems Design`, `Technical Setup`,
`Pre-Production`, `Production`, `Polish`, `Release`, or `UNKNOWN`.
Confidence is exactly `HIGH`, `MEDIUM`, or `LOW`.

No result authorizes a stage transition or gate.

---

## Phase 0: Freeze a read-only snapshot

Resolve one workspace root. Reject traversal, outside-root paths, symlink escape,
or ambiguous roots.

Record:

- `snapshot_at` in UTC;
- VCS commit/ref and dirty-state evidence when available;
- exact stage-schema/catalog sources and raw hashes;
- declared stage record and raw hash, when present;
- referenced gate receipt paths and raw hashes;
- exact source/build/artifact manifests referenced by those receipts; and
- included, excluded, inaccessible, malformed, and concurrently changed sources.

Use stable evidence IDs and provenance types:

| Provenance | Meaning |
|---|---|
| AUTHORITY RECORD | versioned stage state written by its declared owner |
| GATE RECEIPT | immutable evidence for one allowed transition |
| SOURCE SNAPSHOT | current raw artifact/build/config hashes |
| LEGACY DECLARATION | unversioned stage text such as a plain stage.txt value |
| ADVISORY OBSERVATION | artifact presence/absence with no transition authority |
| COVERAGE GAP | unreadable, malformed, missing, stale, or unsupported evidence |

All evidence records contain ID, path, relevant field/section, raw hash,
snapshot time, and validation state.

If the shared workflow catalog does not provide a versioned stage schema,
allowed transition, owner, and receipt requirements, record `STAGE SCHEMA
UNVERIFIED`. Do not copy or invent a stage table inside this workflow.

---

## Phase 1: Validate the stage authority contract

A stage authority record is valid only when the shared versioned schema defines
and the record supplies:

- `schema_version`;
- allowed exact `stage` enum;
- `owner` authorized for that transition;
- `transition_from`;
- `updated_at`;
- target commit/ref and dirty-state policy;
- canonical `source_snapshot_hash`;
- required gate receipt ID/path/hash, or explicit schema rule that no receipt is
  required; and
- previous authority-record hash for transition continuity.

Validate the transition against the schema-defined graph and owner. Validate
every required receipt for:

- stable receipt ID and schema version;
- exact from/to stage;
- gate/profile identity and final PASS state;
- authorized owner/approver;
- passed-at timestamp;
- target commit/dirty state;
- source, build, test, and required artifact hashes;
- receipt raw hash matching the authority record; and
- current freshness under the schema policy.

A plain `production/stage.txt` value without this provenance is a LEGACY
DECLARATION, not authoritative stage evidence. Report its declared value and
hash, but do not promote it to `detected_stage`.

Unknown enum values, missing fields, invalid transitions, unauthorized owners,
unreadable/corrupt records, stale receipts, hash mismatches, or missing required
receipts cannot be repaired or guessed here. They produce UNKNOWN or CONFLICT.

---

## Phase 2: Collect supporting and contradictory evidence

Read only evidence explicitly required by the stage schema/receipt and a bounded
set of advisory artifacts needed to explain contradictions. Hash every source.

Artifact presence, directory names, GDD/ADR/story/test counts, lines of code,
source-file thresholds, engine configuration, prototype counts, and sprint-file
existence are ADVISORY OBSERVATIONS only. They may explain a conflict or suggest
a question, but they can never:

- select a stage;
- advance a stage;
- validate a transition;
- substitute for a gate receipt;
- increase confidence to HIGH; or
- produce a completion percentage.

Exclude generated, vendor, example, cache, imported, and third-party files from
any source inventory unless the authoritative receipt explicitly includes them.
Never classify Production because a source directory contains ten or more files.

Do not estimate design, code, architecture, production, test, milestone, or
overall completion percentages. Do not produce weighted scores, progress bars,
or precise completion numbers without a separately versioned measurement schema
and real denominator; no such schema is assumed here.

If the current source/build/config hashes differ from those bound to the
authority record or receipt, record exact expected/observed hashes as a
contradiction. Do not silently honor the declared stage.

Rehash every read source before returning. Concurrent change makes affected
evidence stale and prevents a clean DETECTED result.

---

## Phase 3: Determine result and confidence

Apply this order:

### ERROR

Return `ERROR`, `detected_stage: UNKNOWN`, and `confidence: LOW` when the
workspace root is invalid, no evidence source can be read, evidence integrity
fails globally, or invocation is invalid.

### CONFLICT

Return `CONFLICT`, `detected_stage: UNKNOWN`, and `confidence: LOW` when a stage
declaration exists but conflicts with schema, transition, owner, receipt,
target/build/source hashes, or another valid authority record. Preserve the
claimed value separately as `declared_stage`.

### UNKNOWN

Return `UNKNOWN` and `detected_stage: UNKNOWN` when no complete authority chain
exists.

- Confidence is LOW for legacy/invalid/missing stage authority, missing required
  receipts, or critical coverage gaps.
- Confidence may be MEDIUM only when the stage schema is valid and most
  authority evidence is present, but a non-authoritative freshness/supporting
  check is incomplete. MEDIUM never authorizes a stage value.

### DETECTED

Return `DETECTED` and the exact stage only when one valid authority record,
allowed transition/owner, all required receipts, and current target/source/build
hashes agree with no contradiction.

- Confidence is HIGH when the complete current authority chain and all required
  evidence validate.
- Confidence is MEDIUM only if the schema explicitly permits an advisory source
  gap that cannot affect authority or freshness.

Never use `PASS`, `CONCERNS`, or `FAIL` as confidence values.

---

## Phase 4: Return one evidence packet

Return in conversation only:

```yaml
schema: project_stage_detection/v2
result: DETECTED | CONFLICT | UNKNOWN | ERROR
detected_stage: Concept | Systems Design | Technical Setup | Pre-Production | Production | Polish | Release | UNKNOWN
declared_stage: <value-or-NONE>
confidence: HIGH | MEDIUM | LOW
snapshot_at: <UTC>
target:
  commit: <hash-or-UNVERIFIED>
  dirty_state: <clean|dirty|UNVERIFIED>
  source_snapshot_hash: <sha256-or-UNVERIFIED>
authority:
  schema_version: <version-or-UNVERIFIED>
  record_path: <path-or-NONE>
  record_hash: <sha256-or-NONE>
  owner: <owner-or-UNVERIFIED>
  transition_from: <stage-or-UNVERIFIED>
receipts:
  required: <count-or-UNVERIFIED>
  valid: <count>
evidence:
  - id: <stable-id>
    provenance: <type>
    path: <path>
    hash: <sha256>
    state: VALID | INVALID | STALE | UNVERIFIED | NOT_APPLICABLE
contradictions:
  - id: <stable-id>
    expected: <redacted value/hash>
    observed: <redacted value/hash>
coverage_gaps:
  - <exact gap>
advisory_observations:
  - <observation explicitly marked non-authoritative>
recommendation:
  role: general | programmer | designer | producer
  action: <one evidence-resolution or formal-transition action>
disclaimer: ADVISORY DETECTION ONLY — NOT A GATE OR TRANSITION
```

The role filter may change only `recommendation.role` and wording. All preceding
fields must be byte-for-byte identical for the same snapshot.

Give at most one next action:

- resolve the missing/conflicting authority evidence;
- run the separately authorized formal gate when advancement is desired; or
- align a direct consumer to this schema.

Do not invoke the action.

---

## Read-only and consumer boundaries

Never write `production/project-stage-report.md`, `production/stage.txt`, an
authority record, receipt, cache, checkpoint, or any project file. Never ask to
persist the packet inside this workflow.

Do not invoke `$gate-check`, `$start`, `$help`, `$studio-status`, or another
project skill. Refer to a separately authorized formal gate only as a handoff.

Consumers must use the full `project_stage_detection/v2` packet and current
snapshot hash. They must not parse a prose stage line, substitute their own
artifact-count heuristic, treat UNKNOWN/CONFLICT as a stage, or use this detector
as gate approval.

---

## Non-negotiable rules

- Never mutate the project or request write authorization.
- Never infer a stage from file/source/artifact counts.
- Never emit completion percentages.
- Never treat an unversioned stage value as authoritative.
- Never hide contradictions or stale hashes.
- Never use detection as permission to advance.
