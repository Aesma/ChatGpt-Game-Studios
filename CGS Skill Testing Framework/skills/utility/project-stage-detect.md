# Skill Test Spec: $project-stage-detect

## Skill Summary

`$project-stage-detect` is a strictly read-only
`project_stage_detection/v2` evidence service. It validates a versioned stage
authority record, allowed transition/owner, required immutable gate receipts,
and current source/build hashes. It never chooses a stage from artifact counts,
never emits completion percentages, and never performs or persists a transition.

Result is `DETECTED`, `CONFLICT`, `UNKNOWN`, or `ERROR`.
`detected_stage` is one of Concept, Systems Design, Technical Setup,
Pre-Production, Production, Polish, Release, or UNKNOWN. Confidence is
HIGH/MEDIUM/LOW.

---

## Static Assertions

- [ ] YAML frontmatter contains only `name` and non-empty `description`; `name`
      matches the skill directory
- [ ] Has at least two phase headings
- [ ] Contains all seven stage names plus UNKNOWN
- [ ] Result enum is DETECTED, CONFLICT, UNKNOWN, or ERROR
- [ ] Confidence enum is HIGH, MEDIUM, or LOW; PASS/CONCERNS/FAIL are forbidden
      as confidence values
- [ ] Strictly read-only with no authorization prompt or persistent report
- [ ] Versioned schema, transition, owner, receipt, current snapshot, and hashes
      are required for DETECTED
- [ ] Plain stage.txt is a legacy declaration, not automatic authority
- [ ] Artifact/source counts and presence never select or advance stage
- [ ] No completion percentage, progress score, or weighted heuristic exists
- [ ] Output includes snapshot_at, source hashes, stable evidence provenance,
      contradictions, gaps, and advisory disclaimer
- [ ] Role filtering changes only recommendation wording
- [ ] No gate/director/project skill is invoked

---

## Director Gate Checks

None. This utility validates supplied gate evidence but never invokes a gate or
director. It cannot authorize advancement.

---

## Test Cases

### Case 1: Valid current Production authority chain

**Fixture:**
- Shared stage schema is versioned and defines Production, its owner, allowed
  transition from Pre-Production, and required gate receipt
- Authority record contains every required field and raw hash
- Referenced gate receipt is immutable, PASS, owner-authorized, and binds the
  exact from/to stage, commit, dirty-state policy, source/build/test hashes
- Current hashes match
- No duplicate record or contradiction exists

**Input:** `$project-stage-detect`

**Expected behavior:**
1. Validates schema, transition, owner, record, receipt, and current snapshot
2. Returns `result: DETECTED`
3. Returns `detected_stage: Production`
4. Returns `confidence: HIGH`
5. Emits the full v2 packet and advisory disclaimer

**Assertions:**
- [ ] Exact authority/receipt/source hashes are present
- [ ] Stage comes from authority chain, not supporting artifact counts
- [ ] No file is written
- [ ] No gate or transition is executed
- [ ] Recommendation is at most one handoff

---

### Case 2: STAGE-P0-001 — every path is strictly read-only

**Fixture:**
- Valid or invalid project states
- A prior `production/project-stage-report.md` may exist
- User asks to save the new detection packet

**Expected behavior:**
1. Returns the packet in conversation
2. Refuses to write/overwrite a report, stage, receipt, checkpoint, or cache
3. Does not request changeset authorization
4. Does not invoke a recorder or gate

**Assertions:**
- [ ] Pre/post workspace hashes are identical
- [ ] `production/project-stage-report.md` is unchanged
- [ ] `production/stage.txt` is unchanged
- [ ] No `Should the changeset include...` prompt appears
- [ ] Metadata and skill both describe read-only behavior

---

### Case 3: STAGE-P0-002 — proxy artifacts do not define workflow stages

Run these variants without a complete authority chain:

| Variant | Proxy/legacy evidence | Expected |
|---|---|---|
| 3a | systems index exists; engine unconfigured | UNKNOWN, not Technical Setup |
| 3b | engine configured; fewer than ten source files | UNKNOWN, not Pre-Production |
| 3c | ten or more source files | UNKNOWN, not Production |
| 3d | GDDs, epics, and sprint files exist | UNKNOWN, not Production |
| 3e | plain stage.txt says Production | declared_stage Production, detected_stage UNKNOWN |
| 3f | plain stage.txt says Polish or Release | detected_stage UNKNOWN without required receipts |

**Assertions:**
- [ ] No copied heuristic table selects a stage
- [ ] File count/presence remains ADVISORY OBSERVATION
- [ ] Legacy stage value is not silently honored
- [ ] Stage-schema absence is explicit
- [ ] Formal owner/transition/receipt evidence is required

---

### Case 4: STAGE-P0-003 — weak signals never become percentages

**Fixture:**
- `src/` contains 1,000 vendor/generated/example files and two project-owned files
- Tests directory contains many filenames but no coverage receipt
- Several GDD/ADR placeholders exist

**Expected behavior:**
1. Excludes vendor/generated/example files from advisory inventory
2. Reports observations without selecting a stage
3. Emits no design/code/architecture/production/test/overall completion number
4. Returns UNKNOWN when authority evidence is absent

**Assertions:**
- [ ] No `10+ files → Production` behavior
- [ ] No exact or approximate percentage appears
- [ ] File count cannot substitute for approval/test/gate receipt
- [ ] Placeholder existence is not completion evidence
- [ ] Output does not imply production began

---

### Case 5: Declaration and current evidence conflict

**Fixture:**
- Versioned authority record declares Production
- Receipt names a different source snapshot or build hash
- Current source/build hashes are available

**Expected behavior:**
1. Preserves Production only as declared_stage
2. Lists exact expected/observed hashes
3. Returns CONFLICT
4. Returns detected_stage UNKNOWN and confidence LOW
5. Recommends resolving or rerunning the formal evidence owner

**Assertions:**
- [ ] Declared stage is not silently overridden or honored
- [ ] Contradiction has stable evidence ID
- [ ] No new stage is inferred from current artifacts

---

### Case 6: Invalid, corrupt, missing, or inaccessible evidence fails closed

Run unknown stage enum, invalid transition, unauthorized owner, missing receipt,
corrupt record, permission failure, and concurrently changed source variants.

**Expected behavior:**
- Invalid invocation/global evidence failure → ERROR
- Existing contradictory declaration → CONFLICT
- Missing/incomplete authority chain → UNKNOWN
- detected_stage remains UNKNOWN
- confidence is LOW unless schema explicitly allows a non-authoritative gap

**Assertions:**
- [ ] No crash
- [ ] No malformed value is normalized into a valid stage
- [ ] Coverage gaps name exact evidence state
- [ ] Concurrent changes make affected hashes stale

---

### Case 7: Polish and Release require exact formal receipts

**Fixture:**
- Variant A has valid current Production→Polish receipt and authority record
- Variant B has only polish-oriented files and QA notes
- Variant C has valid current Polish→Release receipt and authority record
- Variant D has only a release build filename/store checklist

**Expected behavior:**
- A detects Polish according to schema
- C detects Release according to schema
- B and D return UNKNOWN

**Assertions:**
- [ ] Polish/Release are never inferred from artifact names
- [ ] PASS receipt alone is insufficient if target hashes are stale
- [ ] Required owner and transition are validated

---

### Case 8: Role filter cannot alter stage evidence

**Fixture:**
- One frozen valid snapshot
- Run general, programmer, designer, and producer filters

**Expected behavior:**
1. All evidence/result/stage/confidence/contradiction fields are byte-identical
2. Only recommendation role/wording differs

**Assertions:**
- [ ] Role filter is not an alternate detection algorithm
- [ ] Unknown role returns ERROR before scan

---

### Case 9: Missing shared stage schema returns UNKNOWN

**Fixture:**
- Artifacts and legacy stage.txt exist
- Shared catalog has no versioned stage enum/transition/owner/receipt contract

**Expected behavior:**
1. Records STAGE SCHEMA UNVERIFIED
2. Returns UNKNOWN, detected_stage UNKNOWN, confidence LOW
3. Makes no local replacement schema
4. Reports legacy declaration separately

**Assertions:**
- [ ] Skill does not invent authoritative mappings
- [ ] No duplicated start/help/studio-status heuristic is used
- [ ] Missing shared contract is a cross-skill blocker, not a guessed stage

---

### Case 10: Consumer consistency uses one packet and snapshot

**Fixture:**
- start, help, and studio-status consume the same v2 packet/hash
- One consumer attempts to recalculate stage from file counts

**Expected behavior:**
1. Packet result remains canonical for that snapshot
2. Nonconforming consumer is flagged as contract drift
3. Detector does not change its result to match consumer heuristics

**Assertions:**
- [ ] Consumers cannot treat UNKNOWN/CONFLICT as a stage
- [ ] Prose stage parsing is forbidden
- [ ] Stale packet cannot be reused after snapshot change

---

### Case 11: No gate or downstream workflow runs

**Fixture:**
- Any stage evidence and review mode

**Expected behavior:**
1. Reads and validates evidence
2. Spawns no director
3. Does not invoke gate-check, start, help, studio-status, or another project skill
4. Returns one advisory packet

**Assertions:**
- [ ] Gate/director invocation count is zero
- [ ] No gate skip messages
- [ ] Handoff text is not execution

---

## Protocol Compliance

- [ ] Snapshot and schema hashes precede classification
- [ ] DETECTED requires one complete current authority chain
- [ ] Missing/invalid/conflicting evidence fails closed
- [ ] Confidence uses HIGH/MEDIUM/LOW only
- [ ] Artifact counts remain non-authoritative
- [ ] No percentages are emitted
- [ ] Skill is read-only
- [ ] Role filtering affects only recommendation
- [ ] No project workflow is invoked
- [ ] Output says ADVISORY DETECTION ONLY — NOT A GATE OR TRANSITION

---

## Coverage Notes

The shared versioned stage schema and migration of start/help/studio-status are
outside this remediation boundary. Until those shared contracts exist, UNKNOWN
is the correct fail-closed result rather than a heuristic stage.

Catalog last-test fields remain empty because these are static candidates, not
executed behavioral tests.
