# Skill Test Spec: `$project-stage-detect`

## Skill Summary

`$project-stage-detect` is a strictly read-only
`cgs.project-stage-detection/v2` evidence service. It reads one versioned workflow
catalog, follows only the catalog-declared authority/receipt/manifest closure,
revalidates current hashes, and returns `DETECTED`, `CONFLICT`, `UNKNOWN`, or
`ERROR` with deterministic blocking reasons.

The detector never owns a stage table, transition, gate, recorder, progress
formula, or recursive artifact scan. A plain `production/stage.txt` value is
legacy evidence only.

`resolution_state` is `CLEAR` only for `DETECTED` and `BLOCKED` otherwise.
Confidence is exactly `HIGH`, `MEDIUM`, or `LOW`.

---

## Static Assertions

- [ ] YAML frontmatter contains only `name` and a non-empty `description`; the
      name matches the skill directory
- [ ] Metadata describes a read-only, canonical, catalog-backed evidence packet
- [ ] Invocation permits zero or one exact role: general, programmer, designer,
      or producer
- [ ] Has at least two phase headings
- [ ] Canonical schema is exactly `cgs.project-stage-detection/v2`
- [ ] Result enum is exactly DETECTED, CONFLICT, UNKNOWN, or ERROR
- [ ] Resolution enum is exactly CLEAR or BLOCKED
- [ ] Confidence enum is exactly HIGH, MEDIUM, or LOW; PASS, CONCERNS, FAIL, and
      BLOCKED are forbidden as confidence values
- [ ] Contains all seven stage display names plus UNKNOWN
- [ ] Strictly read-only with no authorization prompt, packet persistence,
      report write, stage mutation, or recorder
- [ ] Reads stage policy only from the versioned workflow catalog and invents no
      transition, owner, receipt, freshness, or scan-limit default
- [ ] Plain stage.txt is LEGACY_DECLARATION and never automatic authority
- [ ] DETECTED requires a current catalog, authority record, allowed transition,
      owner, continuity, receipts, manifests, target, and end-of-scan rehash
- [ ] Read closure is catalog → authority → previous record → receipts → declared
      manifests/entries; recursive and newest-file discovery are forbidden
- [ ] Artifact/source counts, file presence, and generated/vendor/example trees
      never select or advance a stage
- [ ] Completion percentages, ranges, estimates, scores, totals, and time-to-stage
      estimates are forbidden
- [ ] Packet includes project identity, catalog identity/hash, snapshot and
      revalidation times, manifest hash/entries, complete authority and receipt
      fields, stable evidence provenance, contradictions, read errors, coverage
      gaps, blocking codes, completion marker, and disclaimer
- [ ] Role filtering changes only the recommendation role/wording
- [ ] No gate, agent, recorder, or other project skill is invoked

---

## Director Gate Checks

None. The detector validates supplied gate evidence but never runs a gate,
delegates to a director, persists a receipt, or authorizes advancement.

---

## Test Cases

### Case 1: Complete current authority chain detects Production

**Fixture:**

- The workflow catalog has a supported schema/version and declares the canonical
  packet schema, authority schema/path, stage enum, initial rule, transition IDs,
  owners, gate profiles, receipt schemas, continuity, target/dirty/freshness,
  manifest policy, and finite read limits
- One authority record declares the catalog-defined Pre-Production → Production
  transition and contains all required fields and hashes
- Its previous record, required receipt, and source/build/test/artifact manifests
  are present, immutable, authorized, current, and hash-matched
- VCS target and dirty-state policy match
- Every closure item returns the same bytes on the final re-read

**Input:** `$project-stage-detect`

**Expected behavior:**

1. Reads the catalog first and follows only its exact closure.
2. Validates authority schema, transition, owner, continuity, receipt, target,
   manifests, freshness, and current raw hashes.
3. Returns `result: DETECTED`, `resolution_state: CLEAR`,
   `detected_stage: Production`, and `confidence: HIGH`.
4. Returns one complete canonical packet and no mutation.

**Assertions:**

- [ ] Stage comes from the authority chain, not proxy artifacts
- [ ] Packet ID and snapshot manifest hash follow the documented canonicalization
- [ ] Required/valid receipt counts and full receipt records agree
- [ ] Blocking reason list is empty
- [ ] No file, gate, transition, or downstream workflow is executed

---

### Case 2: STAGE-P1-001 — declaration authority is catalog-bound

Run these variants:

| Variant | Fixture | Expected result |
|---|---|---|
| 2a | Catalog lacks versioned stage-authority contract | UNKNOWN / BLOCKED / LOW with STAGE_SCHEMA_UNVERIFIED |
| 2b | Only `production/stage.txt = Production` exists | UNKNOWN / BLOCKED / LOW; legacy value preserved only as declared_stage |
| 2c | Authority record omits owner or updated_at and no stable claim can be validated | UNKNOWN / BLOCKED / LOW with AUTHORITY_MALFORMED |
| 2d | Parsable authority stage is outside catalog enum | CONFLICT / BLOCKED / LOW with UNKNOWN_STAGE_ENUM |
| 2e | Transition or owner disagrees with catalog | CONFLICT / BLOCKED / LOW with INVALID_TRANSITION or UNAUTHORIZED_OWNER |
| 2f | Previous-record continuity hash disagrees | CONFLICT / BLOCKED / LOW with CONTINUITY_MISMATCH |
| 2g | Catalog initial-stage rule validates a complete bootstrap record | DETECTED only if every initial-rule requirement passes |

**Assertions:**

- [ ] No local transition/owner/initial-stage fallback is used
- [ ] Timestamp, target, dirty-state, continuity, and receipt requirements are
      checked rather than inferred
- [ ] A stage label never takes precedence over a versioned contract
- [ ] `declared_stage` does not become `detected_stage` on blocked variants

---

### Case 3: STAGE-P1-002 — snapshot provenance is replayable and drift-aware

**Fixture:**

- A catalog-valid closure contains authority, receipt, source, build, test, and
  artifact entries
- Each entry has known raw bytes and expected hashes
- Variant A remains stable; Variant B changes one required source after its first
  read; Variant C has a stable expected/observed hash mismatch

**Expected behavior:**

- A records `snapshot_at`, `reverified_at`, catalog raw hash, stable per-entry raw
  hashes, field/section, per-entry snapshot time, manifest hash, evidence IDs,
  project root ID, and packet ID
- B returns UNKNOWN / BLOCKED with CHANGED_DURING_SCAN
- C returns CONFLICT / BLOCKED with expected and observed hashes linked to stable
  evidence IDs

**Assertions:**

- [ ] Snapshot entries are sorted by normalized path and field before canonical hash
- [ ] Absence is an explicit marker, not an empty-file hash
- [ ] Receipt records are emitted, not only aggregate counts
- [ ] Catalog identity/hash is present in the packet
- [ ] Bytes from different moments are never combined into DETECTED

---

### Case 4: STAGE-P1-003 — confidence vocabulary is independent

Run valid, conflicted, missing-authority, invalid-invocation, and explicitly
catalog-permitted non-authoritative-gap variants.

**Expected behavior:**

- Clean complete chain → DETECTED / HIGH
- Catalog-permitted non-authoritative gap incapable of affecting stage/currentness
  → DETECTED / MEDIUM
- Positive contradiction → CONFLICT / LOW
- Missing critical authority → UNKNOWN / LOW
- Invalid invocation or unreadable catalog → ERROR / LOW

**Assertions:**

- [ ] Confidence is always HIGH, MEDIUM, or LOW
- [ ] PASS, CONCERNS, FAIL, CLEAR, and BLOCKED never occupy confidence
- [ ] MEDIUM never upgrades an unknown stage or relaxes a required receipt

---

### Case 5: STAGE-P1-004 — manifest-only reads ignore source-tree volume

**Fixture:**

- `src/`, `vendor/`, `generated/`, `examples/`, caches, and imported trees contain
  thousands of files
- The catalog-declared closure references two project files and one explicit
  generated build file
- No authority chain exists in Variant A; a valid chain exists in Variant B

**Expected behavior:**

1. Performs no recursive inventory and no newest-file/glob receipt discovery.
2. Reads only the catalog closure and optional legacy declaration.
3. Validates the explicitly bound generated file hash without assigning category
   or count-based stage meaning.
4. A returns UNKNOWN; B follows only the valid authority chain.

**Assertions:**

- [ ] Tree size and file extensions do not affect result or confidence
- [ ] No file total is emitted
- [ ] Generated/vendor/example presence cannot substitute for a receipt
- [ ] Advisory observations do not expand the read closure

---

### Case 6: STAGE-P1-005 — no unsupported progress measurement

**Fixture:**

- Many GDD, ADR, source, test, sprint, prototype, and placeholder files exist
- User asks for completion percentage, approximate range, progress bar, and
  estimated time to the next stage

**Expected behavior:**

1. Returns only the canonical stage-evidence packet.
2. Emits no percentage, range, weighted score, progress total, or time estimate.
3. Does not invent a formula version or denominator.

**Assertions:**

- [ ] No design/code/test/overall completion number appears
- [ ] “Approximate” or advisory wording does not make a number permissible
- [ ] Artifact quantities remain absent from classification and output

---

### Case 7: STAGE-P1-006 — one canonical consumer packet

**Fixture:**

- Freeze one valid snapshot
- Run general, programmer, designer, and producer role variants
- Present the resulting packet to conforming start/help/studio-status consumers
- A nonconforming consumer attempts to parse prose or recalculate stage from files

**Expected behavior:**

1. Every role produces the exact `cgs.project-stage-detection/v2` required fields.
2. Packet ID covers the canonical core through advisory observations and excludes
   packet_id plus role-dependent recommendation.
3. Every field before recommendation is byte-identical across roles.
4. Consumers bind the same packet ID, project root ID, catalog hash, and snapshot
   manifest hash; recalculation is contract drift.

**Assertions:**

- [ ] Schema identity and completion marker are exact
- [ ] Packet includes no locally summarized executable stage rule
- [ ] UNKNOWN/CONFLICT cannot be treated as a stage
- [ ] Stale packet cannot be reused after catalog or snapshot drift
- [ ] Detector does not invoke consumers or change its result to match one

---

### Case 8: STAGE-P1-007 — deterministic fault and budget matrix

Run every row independently:

| Fault | Expected result | Required reason |
|---|---|---|
| Invalid role, root, traversal, or symlink escape | ERROR / BLOCKED / LOW | INVALID_INVOCATION or INVALID_ROOT |
| Catalog unreadable | ERROR / BLOCKED / LOW | CATALOG_UNREADABLE |
| Catalog readable but stage contract missing/malformed/unsupported | UNKNOWN / BLOCKED / LOW | STAGE_SCHEMA_UNVERIFIED |
| Authority absent | UNKNOWN / BLOCKED / LOW | AUTHORITY_MISSING |
| Authority unreadable | UNKNOWN / BLOCKED / LOW | AUTHORITY_UNREADABLE |
| Authority malformed without a stable parsable claim | UNKNOWN / BLOCKED / LOW | AUTHORITY_MALFORMED |
| Parsable authority contradicts enum/transition/owner/continuity | CONFLICT / BLOCKED / LOW | exact contradiction code |
| Required receipt absent or unreadable | UNKNOWN / BLOCKED / LOW | RECEIPT_MISSING or RECEIPT_UNREADABLE |
| Readable receipt identity/verdict/hash contradicts authority | CONFLICT / BLOCKED / LOW | RECEIPT_INVALID or HASH_MISMATCH |
| Required VCS target cannot be verified | UNKNOWN / BLOCKED / LOW | TARGET_UNVERIFIED |
| Catalog read-entry or byte limit would be crossed | UNKNOWN / BLOCKED / LOW | READ_BUDGET_EXCEEDED |
| Required source changes between reads | UNKNOWN / BLOCKED / LOW | CHANGED_DURING_SCAN |

**Assertions:**

- [ ] No crash or silent truncation
- [ ] Read errors and coverage gaps retain evidence IDs and stable reason codes
- [ ] Positive contradictions are distinct from unavailable evidence
- [ ] BLOCKED is a resolution state, never a fifth result or confidence value
- [ ] No malformed value is normalized into a valid stage

---

### Case 9: Polish and Release require exact formal authority

**Fixture:**

- Variant A has a complete catalog-valid Production → Polish authority chain
- Variant B has only polish-oriented assets and QA notes
- Variant C has a complete catalog-valid Polish → Release authority chain
- Variant D has only release filenames, checklist prose, and legacy stage.txt

**Expected behavior:**

- A detects Polish and C detects Release only from their complete authority chains
- B and D return UNKNOWN / BLOCKED

**Assertions:**

- [ ] Later stages are never inferred from names, counts, or legacy text
- [ ] PASS text alone is insufficient when receipt identity or hashes are stale
- [ ] Owner, transition, target, receipt, and current manifest are validated

---

### Case 10: Every path remains strictly read-only

**Fixture:**

- Valid and invalid project states
- A prior `production/project-stage-report.md` may exist
- User asks to save the packet, repair authority, run the gate, or update stage.txt

**Expected behavior:**

1. Returns one packet in conversation.
2. Does not write, overwrite, authorize, delegate, invoke, or persist anything.
3. Gives at most one textual handoff.

**Assertions:**

- [ ] Pre/post workspace hashes are identical
- [ ] No changeset or write-authorization prompt appears
- [ ] No report, packet, cache, receipt, authority, or stage file changes
- [ ] Gate, agent, recorder, and project-skill invocation count is zero

---

## Protocol Compliance

- [ ] Catalog hash and contract validation precede authority classification
- [ ] Read closure is deterministic, finite, and receipt-manifest driven
- [ ] Snapshot hashes and final rehash precede result classification
- [ ] DETECTED requires one complete current authority chain
- [ ] Missing, inaccessible, over-limit, changed, and contradictory evidence fail closed
- [ ] Confidence uses HIGH/MEDIUM/LOW only
- [ ] Result and resolution state remain separate
- [ ] Artifact counts and presence remain non-authoritative
- [ ] No progress measurements are emitted
- [ ] Packet schema and canonical identity are stable across consumers
- [ ] Workflow is read-only and invokes no downstream workflow
- [ ] Output says `ADVISORY DETECTION ONLY — NOT A GATE OR TRANSITION`

---

## Coverage Notes

If the repository's shared workflow catalog does not yet provide the required
versioned authority contract, Case 2a is the mandatory fail-closed behavior:
`UNKNOWN`, `BLOCKED`, `LOW`, and `STAGE_SCHEMA_UNVERIFIED`. The detector must not
restore heuristics to manufacture a usable stage.

Catalog last-test fields remain empty until these cases are actually executed;
authoring this specification alone is not test evidence.
