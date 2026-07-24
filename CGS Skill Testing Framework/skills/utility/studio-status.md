# Skill Test Spec: `$studio-status`

## Skill Summary

`$studio-status` is a strictly read-only consumer of one complete current
`cgs.project-stage-detection/v2` packet. It displays declared and detected stage,
detection result/resolution, confidence, catalog and snapshot identity, evidence,
contradictions, coverage gaps, blocking reasons, and optional active focus.

It never reads stage.txt as authority, derives a stage from project artifacts,
invokes the detector, or treats the packet as gate approval.

---

## Static Assertions

- [ ] YAML frontmatter contains only `name` and a non-empty `description`; name
      matches the skill directory
- [ ] Metadata names the canonical packet contract, currentness validation,
      read-only status summary, and no local stage recalculation
- [ ] Invocation accepts either one explicit inline canonical packet or the exact
      `--analysis <path> --expect-analysis <sha256:...>` pair
- [ ] Unknown/duplicate flags, unsafe paths, directories, malformed hashes, two
      input forms, and ambiguous packet candidates are rejected
- [ ] Missing packet returns BLOCKED/UNKNOWN/LOW without invoking the detector
- [ ] Canonical producer schema is exactly `cgs.project-stage-detection/v2`
- [ ] Recomputes packet ID, project identity, catalog hash, snapshot entries, and
      snapshot manifest before consuming stage fields
- [ ] Stage is copied only from a CURRENT complete packet; no local phase table,
      artifact precedence, source extensions, or file thresholds exist
- [ ] Plain `production/stage.txt` is never stage authority
- [ ] Status result is exactly READY, PARTIAL, BLOCKED, or ERROR
- [ ] Packet context is exactly CURRENT, MISSING, INVALID, STALE,
      PROJECT_MISMATCH, or UNREADABLE
- [ ] Main output separates Declared Stage and Detected Stage
- [ ] Main output includes confidence, evidence IDs, contradictions, read errors,
      coverage gaps, blocking reasons, stage snapshot, catalog identity, and hashes
- [ ] Breadcrumb is optional independent focus evidence and cannot change stage
- [ ] No files are written and no detector, gate, recorder, skill, or agent runs

---

## Director Gate Checks

None. Status reporting is diagnostic only. It must not delegate, evaluate a gate,
advance a stage, or turn a detector result into approval.

---

## Test Cases

### Case 1: Current DETECTED packet and valid focus

**Fixture:**

- One complete canonical packet is explicitly supplied
- Packet ID, project root ID, catalog path/hash, snapshot manifest and every
  required current source validate
- Packet says DETECTED/CLEAR, `declared_stage: Production`,
  `detected_stage: Production`, `confidence: HIGH`
- `active.md` has exactly one valid STATUS block with Epic, Feature, and Task

**Expected behavior:**

1. Validates packet bytes/identity/currentness before reading stage fields.
2. Copies detector result and stage values exactly.
3. Reads only the bounded focus block and returns `Epic > Feature > Task`.
4. Returns `Status Result: READY` and the complete evidence-backed summary.

**Assertions:**

- [ ] Packet context is CURRENT
- [ ] Declared and Detected Stage are separate fields
- [ ] Confidence is HIGH because the producer packet says HIGH, not because of focus
- [ ] Catalog/snapshot/packet IDs and evidence are shown
- [ ] No files or project workflows are changed or invoked

---

### Case 2: STATUS-P1-001 — arbitrary explicit text is not a formal stage

**Fixture:**

- `production/stage.txt` contains `Launch Candidate`, a misspelling, multiple
  non-empty lines, or another arbitrary value
- Variant A supplies no detector packet
- Variant B supplies a CURRENT canonical packet that preserves the legacy text
  as `declared_stage` but returns UNKNOWN/BLOCKED/LOW with UNKNOWN_STAGE_ENUM

**Expected behavior:**

- A returns Status Result BLOCKED, Packet Context MISSING, Detected Stage UNKNOWN,
  Confidence LOW, and STAGE_PACKET_MISSING
- B copies the detector result: Declared Stage remains visible, Detected Stage is
  UNKNOWN, and the exact contradiction/blocking reason is displayed

**Assertions:**

- [ ] studio-status never reads or normalizes stage.txt itself
- [ ] Arbitrary declared text never occupies Detected Stage
- [ ] Empty-project or invalid-stage fallback is not Concept
- [ ] One next action asks for current/valid authority evidence, not a guessed stage

---

### Case 3: STATUS-P1-002 — owner, time, receipt, and conflicts remain authoritative

Run CURRENT canonical packet variants whose detector result is:

| Variant | Packet evidence | Expected status |
|---|---|---|
| 3a | Valid current owner, transition, receipt, target and hashes | READY with copied DETECTED stage |
| 3b | Unauthorized owner | BLOCKED; Detection Result CONFLICT; Detected Stage UNKNOWN |
| 3c | Stale receipt or target/source hash disagreement | BLOCKED; copied contradiction IDs and expected/observed values |
| 3d | Missing required receipt/read error | BLOCKED; Detection Result UNKNOWN; copied gap/error IDs |
| 3e | Declared and detected fields disagree under producer rules | BLOCKED unless producer itself returned a valid DETECTED/CLEAR packet |

**Assertions:**

- [ ] studio-status does not independently reinterpret updated_at, owner, gate, or artifacts
- [ ] Detector contradiction and blocker arrays are preserved, not reduced to a warning
- [ ] A detector packet is diagnostic and never presented as a gate receipt
- [ ] Confidence is copied from a CURRENT packet only

---

### Case 4: STATUS-P1-003 — weak artifacts never infer a stage

**Fixture:**

- No valid detector packet
- Game concept, systems index, configured engine preferences, multiple ADRs,
  epics, sprints, QA notes, polish assets, and release filenames exist

**Expected behavior:**

1. Does not inspect those paths for stage classification.
2. Returns BLOCKED, Detected Stage UNKNOWN, Confidence LOW.
3. Recommends obtaining one current canonical packet.

**Assertions:**

- [ ] One ADR does not mean Pre-Production
- [ ] Engine configuration does not mean Technical Setup
- [ ] Artifact names do not produce Polish or Release
- [ ] No “most advanced supported artifact” precedence exists

---

### Case 5: STATUS-P1-004 — vendor/generated/example growth has no effect

**Fixture:**

- Add or remove thousands of files under source, vendor, generated, imported,
  cache, resource-scene, and example trees
- Keep the exact supplied packet, current manifest bytes, and active focus unchanged

**Expected behavior:**

1. Reads only packet-declared currentness entries, the exact catalog, and optional
   active.md.
2. Produces byte-identical stage/result/confidence fields before and after tree growth.
3. Emits no source-file count or extension inventory.

**Assertions:**

- [ ] No recursive source scan occurs
- [ ] Vendor/generated/resource/example files cannot promote Production
- [ ] Files outside the packet manifest do not become stage evidence
- [ ] A packet-declared file is rehashed only for currentness, never counted

---

### Case 6: STATUS-P1-005 — main report exposes uncertainty and provenance

**Fixture:**

- Supply a CURRENT packet containing declared stage, UNKNOWN or CONFLICT result,
  LOW confidence, evidence IDs, contradictions, read errors, coverage gaps,
  blockers, catalog identity, snapshot/reverification times, and manifest hash

**Expected behavior:**

The main summary includes:

- packet context/source/ID/raw hash and project root ID;
- catalog path/version/hash;
- detection result/resolution, declared stage, detected stage, and confidence;
- snapshot/reverification times and manifest hash;
- ordered evidence IDs, contradiction expected/observed values, read errors,
  coverage gaps and blocking flags/reasons; and
- independent focus evidence/diagnostics plus the advisory disclaimer.

**Assertions:**

- [ ] UNKNOWN is never relabeled Concept
- [ ] Conflict and coverage details are not hidden in generic prose
- [ ] Hashes and stable IDs are not replaced with file counts
- [ ] Human-readable compactness does not permit dropping required fields

---

### Case 7: STATUS-P1-006 — all stage consumers use the same packet

**Fixture:**

- Freeze one canonical packet and supply its exact packet ID, project root ID,
  catalog hash, and manifest hash to studio-status and the other conforming consumers
- A local artifact picture would suggest a different stage

**Expected behavior:**

1. studio-status reports exactly the packet's declared/detected stage, result,
   resolution, confidence, contradictions, and blockers.
2. It does not run project-stage-detect or copy its algorithm.
3. It flags stale/invalid packet context rather than switching to local inference.

**Assertions:**

- [ ] Same packet and snapshot produce the same stage context across consumers
- [ ] Packet result remains canonical even when artifact heuristics disagree
- [ ] No prose-stage parsing or alternate stage table exists
- [ ] Stale packet cannot be reused after catalog or manifest drift

---

### Case 8: Packet validation and currentness fail closed

Run these variants:

| Fault | Expected packet context / result | Diagnostic |
|---|---|---|
| No supplied packet | MISSING / BLOCKED | STAGE_PACKET_MISSING |
| Packet path unreadable | UNREADABLE / BLOCKED | STAGE_PACKET_UNREADABLE |
| Raw packet hash mismatch | INVALID / BLOCKED | STAGE_PACKET_INVALID |
| Wrong schema/version/completion marker | INVALID / BLOCKED | STAGE_PACKET_INVALID |
| Missing/truncated required section | INVALID / BLOCKED | STAGE_PACKET_INVALID |
| Packet ID canonicalization mismatch | INVALID / BLOCKED | STAGE_PACKET_INVALID |
| Project root ID mismatch | PROJECT_MISMATCH / BLOCKED | STAGE_PACKET_PROJECT_MISMATCH |
| Catalog or manifest entry drift | STALE / BLOCKED | STAGE_PACKET_STALE |
| Source declared PRESENT/ABSENT cannot now be checked | UNREADABLE / BLOCKED | STAGE_PACKET_UNREADABLE |
| Source declared UNREADABLE remains unreadable with the same linked reason | CURRENT; copy detector UNKNOWN/BLOCKED | detector reason code |
| Invalid invocation/root/path | result ERROR | INVALID_INVOCATION or INVALID_ROOT |

For every packet-context failure, Detected Stage is UNKNOWN and Confidence is LOW.
No partial field from the bad packet is consumed.

---

### Case 9: Focus is independent and bounded

Run absent file, valid block, empty valid block, missing close marker, reversed
markers, duplicate marker blocks, duplicate Epic/Feature/Task fields, read failure,
and mid-read change variants.

**Expected behavior:**

- Absent file → NONE_RECORDED, `Focus: none recorded`, Recovery NONE
- Valid block → ordered non-empty Epic > Feature > Task values only
- Malformed/read-failed block → UNKNOWN with exact focus diagnostic
- Mid-read change → STALE with FOCUS_CHANGED_DURING_READ
- Focus UNKNOWN/STALE makes a valid stage summary PARTIAL, not a different stage

**Assertions:**

- [ ] Text outside the single bounded block is ignored
- [ ] No unbounded or duplicate block is parsed
- [ ] Focus never changes detector result, stage, confidence, or blockers
- [ ] active.md is never repaired or created

---

### Case 10: Every path remains strictly read-only

**Fixture:** valid, invalid, stale, missing, and malformed inputs; user asks to
refresh the detector, repair active.md, save the summary, or advance the stage.

**Expected behavior:** returns the appropriate summary and at most one textual
next action, with `Files Written: NONE` and `Auto Executed: false`.

**Assertions:**

- [ ] Pre/post workspace hashes are identical
- [ ] No write authorization prompt appears
- [ ] No packet, report, cache, focus, stage, authority, or receipt is written
- [ ] Detector, gate, recorder, agent, and project-skill invocation count is zero
- [ ] No terminal status line is installed or emulated

---

## Protocol Compliance

- [ ] Packet source is explicit and unambiguous
- [ ] Packet schema/ID/project/catalog/manifest validate before stage consumption
- [ ] Only CURRENT packet context supplies stage fields
- [ ] Declared and detected stages remain separate
- [ ] UNKNOWN/CONFLICT/ERROR remain blocked and visible
- [ ] Confidence and all provenance come from the canonical packet
- [ ] Artifact counts, file presence, and legacy text never infer stage
- [ ] Focus is independent, bounded, hash-bound, and optional
- [ ] Output is compact but retains required evidence and contradictions
- [ ] Workflow is read-only and invokes nothing downstream
- [ ] Output says `STATUS SUMMARY ONLY — NOT A GATE OR TRANSITION`

---

## Coverage Notes

When the shared catalog-backed authority contract is unavailable, the detector
packet is expected to be UNKNOWN/BLOCKED; studio-status must report that outcome
faithfully. Restoring the old stage.txt/ADR/source-count fallback is always a
failure, not graceful degradation.

Catalog last-test fields remain empty until these cases are actually executed;
authoring this specification is not current test evidence.
