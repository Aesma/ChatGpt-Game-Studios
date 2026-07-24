---
name: studio-status
description: "Read-only studio-status consumer that reports declared and detected stage, confidence, contradictions, snapshot identity, and active focus from one current canonical project-stage packet without recalculating stage from artifacts."
---

# Studio Status

## Invocation and execution

Invoke this read-only workflow as:

```text
$studio-status [--analysis <packet-path> --expect-analysis <sha256:...>]
```

`--analysis` and `--expect-analysis` are an inseparable pair. The alternative is
exactly one complete `cgs.project-stage-detection/v2` packet supplied explicitly
in the current invocation or conversation. Reject unknown or duplicate flags,
missing values, malformed expected hashes, directories, traversal, outside-root
paths, symlink escape, both input forms, or more than one candidate packet with
`Status Result: ERROR`.

With no explicit packet and no analysis pair, return `Status Result: BLOCKED`,
`Detected Stage: UNKNOWN`, and `Confidence: LOW`. Recommend obtaining one current
canonical packet, but do not invoke `$project-stage-detect`.

This workflow never searches for the newest report, scans for stage artifacts,
installs or emulates a terminal status line, invokes another skill or agent,
persists a summary, repairs evidence, or creates/modifies/deletes files.

---

## Phase 0: Resolve the project and packet source

Resolve exactly one workspace root. Normalize repository-relative paths with
`/` for identity, retain exact raw bytes for hashes, and reject ambiguous roots.

For a path input:

1. resolve the literal and real path inside the project root;
2. read the explicitly named regular file once;
3. compute lowercase SHA-256 over exact raw bytes; and
4. require exact equality with `--expect-analysis` before parsing.

Do not choose a packet by name, timestamp, directory order, or proximity. For an
inline packet, preserve its exact structured content and validate its canonical
`packet_id`; do not reconstruct omitted fields from prose.

Record the status-summary snapshot time in UTC, the packet source kind
`INLINE` or `PATH`, the supplied path or `INLINE`, and the raw packet hash for a
path input or `NOT_APPLICABLE` for inline structured input.

---

## Phase 1: Validate the complete canonical packet

Consume stage only from the canonical producer contract
`cgs.project-stage-detection/v2`. Require every field and list defined by that
contract, including:

- `schema`, `schema_version: 2`, and `completion_marker: COMPLETE`;
- `packet_id` and `project.root_id`;
- catalog path, schema/version, raw hash, and stage-authority schema version;
- snapshot and revalidation timestamps, VCS identity, dirty state, manifest
  hash, and all ordered entries;
- result, resolution state, declared/detected stage, and confidence;
- the complete authority and receipt records;
- evidence with stable IDs, provenance, fields, times, expected/observed hashes,
  states, and reason codes;
- contradictions, read errors, coverage gaps, blocking reason codes, and
  advisory observations; and
- the exact advisory disclaimer.

Recompute `packet_id` using the producer rule: canonical JSON for the packet core
through `advisory_observations`, excluding `packet_id` and the role-dependent
recommendation. Reject missing, truncated, duplicated, unsupported, or
extra-normalized fields rather than repairing them.

Require the packet's project root ID to match the canonical current root. Read
and hash the exact `.codex/docs/workflow-catalog.yaml`; require its current bytes
to match the packet catalog path/hash. Re-read every packet snapshot entry and
verify its normalized path, current raw hash or explicit source state, and
manifest canonicalization. A packet-declared `ABSENT` or `UNREADABLE` state may
itself be current when the same state and linked reason remain reproducible;
that diagnostic gap blocks stage detection, not packet consumption. Do not
expand beyond the packet manifest or use timestamp age as a substitute for
content currentness.

Classify packet context as:

| Packet Context | Condition |
|---|---|
| `CURRENT` | Complete schema and packet/project/catalog/manifest identities validate; every current raw hash or explicit ABSENT/UNREADABLE state matches the packet |
| `MISSING` | No packet was supplied |
| `INVALID` | Schema, completion marker, packet ID, required field, enum, or canonicalization fails |
| `STALE` | Catalog, packet-declared source, absence state, or manifest hash differs from current bytes |
| `PROJECT_MISMATCH` | Packet root identity differs from the current project |
| `UNREADABLE` | Explicit packet/catalog cannot be read, or a source declared PRESENT/ABSENT cannot now be checked; a reproducible packet-declared UNREADABLE state is not by itself a packet-context failure |

Only `CURRENT` may supply stage context. Any other state returns
`Status Result: BLOCKED`, `Detected Stage: UNKNOWN`, and `Confidence: LOW` with
one exact diagnostic code. Do not consume individual stage fields from an
invalid or partial packet.

---

## Phase 2: Use the detector result without reinterpretation

For a `CURRENT` packet, copy these values exactly and do not recalculate them:

- packet `declared_stage` → `Declared Stage`;
- packet `detected_stage` → `Detected Stage`;
- packet `result` → `Detection Result`;
- packet `resolution_state` → `Detection Resolution`;
- packet `confidence` → `Confidence`;
- packet snapshot/catalog identities and timestamps;
- evidence IDs, contradictions, read errors, coverage gaps, and blocking reason
  codes relevant to the displayed result.

Report a normal stage only when the packet says `result: DETECTED`,
`resolution_state: CLEAR`, and its detected stage is one catalog/schema-valid
stage. If the current packet says `UNKNOWN`, `CONFLICT`, or `ERROR`, preserve its
declared value separately, report `Detected Stage: UNKNOWN`, set
`Status Result: BLOCKED`, and display the packet's confidence and exact blockers.

Never read `production/stage.txt` as authority. Never inspect game-concept,
systems-index, engine preferences, ADRs, source extensions, source counts,
generated/vendor/example trees, sprint files, QA notes, or release filenames to
derive, confirm, override, or increase confidence in a stage. Those signals do
not repair a missing, invalid, stale, conflicted, or unknown packet.

The packet is diagnostic context, not gate approval. A detected later stage does
not prove individual workflow steps complete and does not authorize advancement.

---

## Phase 3: Read active focus independently

Read `production/session-state/active.md` only as optional focus/recovery state,
never as stage evidence. Its absence produces `Focus State: NONE_RECORDED` and is
not a stage blocker.

When the file exists:

1. record exact path, raw SHA-256, and focus snapshot time;
2. require exactly one opening `<!-- STATUS -->` and exactly one later closing
   `<!-- /STATUS -->` marker;
3. read only the bounded block;
4. accept at most one non-empty `Epic:`, `Feature:`, and `Task:` field;
5. join present values in that order with ` > `; and
6. re-read and re-hash the file before returning.

Text outside the markers is ignored. Missing, reversed, or duplicate markers,
duplicate fields, read failure, or mid-read changes produce
`Focus State: UNKNOWN` or `STALE`, no fabricated breadcrumb, and a structured
focus diagnostic. Focus failure may make an otherwise current detected summary
`PARTIAL`, but it never alters stage result or confidence.

`Recovery` is the exact `active.md` path only when that file exists; otherwise
`NONE`. Never create or repair it.

---

## Phase 4: Determine status result

Use exactly one status result:

- `READY`: packet context is CURRENT, detection is DETECTED/CLEAR, and focus is
  CURRENT or NONE_RECORDED;
- `PARTIAL`: packet context is CURRENT and detection is DETECTED/CLEAR, but
  optional focus is UNKNOWN or STALE;
- `BLOCKED`: packet is missing/invalid/stale/mismatched/unreadable, or its current
  detector result is UNKNOWN, CONFLICT, or ERROR; or
- `ERROR`: invocation or project-root validation failed before a trustworthy
  packet context could be established.

Use stable status diagnostic codes when applicable:

`INVALID_INVOCATION`, `INVALID_ROOT`, `STAGE_PACKET_MISSING`,
`STAGE_PACKET_UNREADABLE`, `STAGE_PACKET_INVALID`, `STAGE_PACKET_STALE`,
`STAGE_PACKET_PROJECT_MISMATCH`, `DETECTION_UNKNOWN`, `DETECTION_CONFLICT`,
`DETECTION_ERROR`, `FOCUS_UNREADABLE`, `FOCUS_MARKERS_INVALID`,
`FOCUS_FIELDS_INVALID`, and `FOCUS_CHANGED_DURING_READ`.

Give at most one next action. Packet failures recommend obtaining or refreshing
the exact detector packet; detector blockers recommend resolving the packet's
first blocking reason; focus-only failures recommend repairing focus state
through its separate owner. Do not invoke or perform the action.

---

## Phase 5: Return the compact evidence-backed summary

Return in conversation only:

```text
Studio Status
Status Result: READY | PARTIAL | BLOCKED | ERROR
Packet Context: CURRENT | MISSING | INVALID | STALE | PROJECT_MISMATCH | UNREADABLE
Packet ID: <sha256-id | NONE>
Packet Source: <INLINE | repository-relative-path | NONE>
Packet Raw SHA-256: <sha256 | NOT_APPLICABLE | NONE>
Project Root ID: <sha256 | UNVERIFIED>
Catalog: <path>@<version> sha256:<hash | UNVERIFIED>
Detection Result: DETECTED | CONFLICT | UNKNOWN | ERROR | UNAVAILABLE
Detection Resolution: CLEAR | BLOCKED | UNAVAILABLE
Declared Stage: <value | NONE | UNAVAILABLE>
Detected Stage: <catalog stage | UNKNOWN>
Confidence: HIGH | MEDIUM | LOW
Stage Snapshot: <snapshot_at / reverified_at / manifest_sha256 | UNAVAILABLE>
Stage Evidence IDs: <ordered IDs | NONE>
Stage Contradictions: <ordered IDs with expected/observed values | NONE>
Stage Read Errors: <ordered evidence ID + reason code | NONE>
Stage Coverage Gaps: <ordered evidence ID + reason code + blocking flag | NONE>
Stage Blocking Reasons: <ordered codes | NONE>
Focus State: CURRENT | NONE_RECORDED | UNKNOWN | STALE
Focus: <Epic > Feature > Task | none recorded | UNKNOWN>
Focus Evidence: <active.md path + raw hash + snapshot time | NONE>
Focus Diagnostics: <ordered codes | NONE>
Recovery: <production/session-state/active.md | NONE>
Next Action: <one action | NONE>
Files Written: NONE
Auto Executed: false
Disclaimer: STATUS SUMMARY ONLY — NOT A GATE OR TRANSITION
```

Do not hide a declared/detected disagreement, collapse packet contradictions into
one prose warning, relabel UNKNOWN as Concept, or replace hashes and stable IDs
with artifact counts.

## Non-negotiable rules

- Never write files, persist the summary, or request write authorization.
- Never invoke the detector, gate, recorder, agent, or another project workflow.
- Never infer or confirm stage from project artifacts or file counts.
- Never treat legacy stage text as authority.
- Never consume a partial, stale, mismatched, or invalid packet.
- Never let focus state change stage, confidence, or gate meaning.
