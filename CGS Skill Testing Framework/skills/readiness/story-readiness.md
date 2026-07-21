# Skill Test Spec: $story-readiness

## Skill Summary

`$story-readiness` is a read-only, fail-closed gate that checks whether a story
can be assigned for implementation. It validates design and scope completeness,
active TR traceability, Accepted ADRs, a current hashed control-manifest source
snapshot, dependencies, and testable acceptance criteria. In full review mode it
also merges QL-STORY-READY into the final READY / NEEDS WORK / BLOCKED verdict.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty
  `description`; `name` matches the skill directory
- [ ] Has at least two phase headings or numbered check sections
- [ ] Contains verdict keywords READY, NEEDS WORK, and BLOCKED
- [ ] Remains read-only; no file mutation or authorization prompt appears
- [ ] Names `docs/architecture/tr-registry.yaml` and
  `docs/architecture/control-manifest.md` as authoritative sources
- [ ] Defines exact QA mappings: GAPS to at least NEEDS WORK and INADEQUATE to
  BLOCKED
- [ ] Has a next-step handoff that permits implementation only after a final
  READY verdict

---

## Test Cases

### Case 1: Happy Path — Fully current, traceable story

**Fixture:**

- Story exists at `production/epics/core/story-light-pickup.md`
- Story contains an exact active `TR-ID: TR-light-001`
- `docs/architecture/tr-registry.yaml` exists, parses, and contains
  `TR-light-001` with `status: active`
- Story references an existing Accepted ADR
- Current control manifest contains `Manifest Version: 2026-03-10`
- SHA-256 of the raw manifest bytes is
  `sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
- Story header contains that exact Manifest Version and Manifest Hash
- Story has `## Source Snapshot` with the same control-manifest path and hash
- Acceptance criteria, scope, dependencies, type, and test evidence all pass
- Review mode is lean

**Input:** `$story-readiness production/epics/core/story-light-pickup.md`

**Expected behavior:**

1. Reads the story, registry, manifest, and referenced ADR
2. Computes the current manifest SHA-256 from raw bytes
3. Verifies the active TR-ID and all three manifest bindings: version, header
   hash, and source-snapshot hash
4. Notes that QL-STORY-READY is skipped in lean mode
5. Emits final verdict READY

**Assertions:**

- [ ] Registry and manifest are actually read
- [ ] ADR status is verified as Accepted
- [ ] Computed hash, not a copied label, is used for comparison
- [ ] Output includes source status and the gate result
- [ ] Verdict is READY only after every required binding matches
- [ ] No file is written

---

### Case 2: Blocked Path — Referenced ADR is Proposed

**Fixture:**

- Story references `docs/architecture/adr-005-light-system.md`
- The ADR exists with `Status: Proposed`
- All other checks pass

**Input:** `$story-readiness production/epics/core/story-light-system.md`

**Expected behavior:**

1. Reads the story and referenced ADR
2. Names the Proposed ADR as a blocker
3. Emits BLOCKED regardless of other passing checks

**Assertions:**

- [ ] Proposed ADR produces BLOCKED, not NEEDS WORK or READY
- [ ] Output recommends resolving ADR status before implementation
- [ ] No other passing check can override the blocker

---

### Case 3: Needs Work — Missing Acceptance Criteria

**Fixture:**

- Story has no `## Acceptance Criteria` section
- Registry/TR, ADR, manifest snapshot, and other content pass

**Input:** `$story-readiness production/epics/core/story-oxygen-drain.md`

**Expected behavior:**

1. Detects the missing section
2. Emits NEEDS WORK
3. Suggests measurable acceptance criteria

**Assertions:**

- [ ] Missing Acceptance Criteria is identified specifically
- [ ] Verdict is NEEDS WORK, not BLOCKED or READY
- [ ] NEEDS WORK remains distinct from external blockers

---

### Case 4: SR-001 — Registry and TR-ID fail-closed matrix

Run each row independently with all unrelated checks passing.

| Variant | Fixture | Expected verdict |
|---|---|---|
| 4a | Registry missing | BLOCKED |
| 4b | Registry unreadable or invalid YAML | BLOCKED |
| 4c | Registry loaded; story has no TR-ID and no legacy marker | NEEDS WORK |
| 4d | Registry loaded; story has `TR-light-???` | NEEDS WORK |
| 4e | Registry loaded; story references unknown `TR-light-999` | NEEDS WORK |
| 4f | Registry entry is deprecated | NEEDS WORK |
| 4g | Registry entry is superseded and names a replacement | NEEDS WORK; replacement named |
| 4h | Registry loaded; exact ID exists with `status: active` | TR check passes |

**Assertions:**

- [ ] Missing/unreadable/invalid registry never auto-passes
- [ ] Missing, placeholder, malformed, and unknown TR-IDs never produce READY
- [ ] A deprecated or superseded entry never passes as active
- [ ] Source status and exact failing ID are included in evidence
- [ ] No waiver or story age changes any row's result

---

### Case 5: SR-001 — Explicit legacy marker is non-ready

**Fixture:**

- Production story has no TR-ID
- Story contains exact `Traceability: LEGACY-UNTRACED`
- Registry is available and valid
- All unrelated checks pass

**Expected behavior:**

1. Recognizes the story as explicitly legacy rather than inferring legacy from
   age or missing data
2. Emits NEEDS WORK and requests migration to an active TR-ID
3. Never emits READY

**Assertions:**

- [ ] Only the exact marker selects the legacy branch
- [ ] The marker does not count as a passing TR reference
- [ ] If the registry is also unavailable, the stricter result is BLOCKED

---

### Case 6: SR-002 — Manifest source and snapshot matrix

All variants use a production story with valid active TR and Accepted ADR.

| Variant | Fixture | Expected verdict |
|---|---|---|
| 6a | Control manifest missing/unreadable/invalid | NEEDS WORK |
| 6b | Current manifest valid; story Manifest Version missing | NEEDS WORK |
| 6c | Story version differs from current version | NEEDS WORK |
| 6d | Story Manifest Hash missing or malformed | NEEDS WORK |
| 6e | Story hash is well formed but differs from computed current hash | NEEDS WORK |
| 6f | `## Source Snapshot` missing | NEEDS WORK |
| 6g | Snapshot manifest entry missing or has a different hash | NEEDS WORK |
| 6h | Version, header hash, and snapshot hash all equal current manifest | Manifest check passes |

**Assertions:**

- [ ] Production control-plane requirement is determined independently of
  whether the manifest exists
- [ ] Manifest bytes are hashed with SHA-256 and formatted `sha256:<64hex>`
- [ ] Matching dates do not hide differing content hashes
- [ ] Matching header hash does not hide a missing/stale source snapshot
- [ ] Every missing or stale variant is non-ready

---

### Case 7: SR-002 — Risk waiver cannot rewrite provenance

**Fixture:**

- Current manifest hash is `sha256:bbbb...bbbb`
- Story records an older `Manifest Hash: sha256:aaaa...aaaa`
- Story contains a `Manifest-Note`, waiver ID, or accepted-risk statement saying
  to proceed with old rules
- All unrelated checks pass

**Expected behavior:**

1. Preserves and reports both the captured story hash and current computed hash
2. Records the risk statement only as informational evidence
3. Emits NEEDS WORK
4. Does not replace the story hash, treat it as current, or emit READY

**Assertions:**

- [ ] Waiver text does not alter the manifest comparison
- [ ] Output never claims the old hash equals the current hash
- [ ] Read-only behavior is preserved

---

### Case 8: SR-003 — QL-STORY-READY verdict matrix in full mode

**Fixture:**

- `production/review-mode.txt` contains `full`
- Deterministic checks produce base READY unless a variant says otherwise
- QL-STORY-READY returns one result per variant

| Variant | Base verdict | QA result | Expected final verdict |
|---|---|---|---|
| 8a | READY | ADEQUATE | READY |
| 8b | NEEDS WORK | ADEQUATE | NEEDS WORK |
| 8c | READY | GAPS | NEEDS WORK |
| 8d | BLOCKED | GAPS | BLOCKED |
| 8e | READY | INADEQUATE | BLOCKED |
| 8f | NEEDS WORK | INADEQUATE | BLOCKED |
| 8g | READY | invalid/no gate result | BLOCKED |

**Assertions:**

- [ ] Gate runs after deterministic checks and before final output
- [ ] `Gate: QL-STORY-READY — [result]` is present
- [ ] GAPS can never leave a final READY verdict
- [ ] INADEQUATE always produces final BLOCKED
- [ ] No `proceed anyway` option is offered for INADEQUATE

---

### Case 9: SR-003 — Accepted QA risk remains non-ready

**Fixture:**

- Base verdict is READY
- Full-mode QA returns GAPS
- User chooses to accept the stated risk

**Expected behavior:**

1. Records the accepted risk in the response
2. Keeps the final verdict NEEDS WORK
3. Does not modify the story or gate record
4. Does not recommend `$dev-story` for this story

**Assertions:**

- [ ] Accepted risk is not a verdict override
- [ ] Final verdict remains NEEDS WORK
- [ ] The only implementation handoff is conditioned on final READY

---

### Case 10: Lean and solo modes skip the QA gate

Run once with `production/review-mode.txt` set to `lean` and once with `solo`.

**Expected behavior:**

1. QL-STORY-READY does not spawn
2. Output records the exact Lean/Solo skip message
3. Final verdict equals the deterministic base verdict

**Assertions:**

- [ ] The gate is not invoked in lean or solo mode
- [ ] Skip is explicit in output
- [ ] Skipping QA does not bypass registry, TR-ID, or manifest checks

---

### Case 11: Imported QA-plan provenance is current and exact

**Fixture**: A story claims imported QA-plan IDs. Exercise a valid current plan,
a plan-byte mismatch, a captured source mismatch, `PARTIAL`, effective `STALE`,
story-hash drift, AC drift, and duplicate/ambiguous test IDs.

**Expected**:

- [ ] The plan and every captured source are re-hashed before evidence is accepted
- [ ] Only an exact `CURRENT` story/path/hash/AC/test binding can satisfy readiness
- [ ] Every invalid provenance case yields at least `NEEDS WORK`
- [ ] No user waiver converts failed provenance into a pass

## Protocol Compliance

- [ ] Uses no file-editing operations
- [ ] Presents source status and complete check results before the final verdict
- [ ] Does not ask for write approval because the workflow is read-only
- [ ] Keeps blocker and fixable-gap semantics distinct
- [ ] Never emits READY for unavailable registry, untraced production story,
  stale/missing production manifest snapshot, QA GAPS, or QA INADEQUATE
- [ ] Ends with a next step appropriate to the final verdict

---

## Coverage Notes

- These cases cover the three P0 remediation contracts SR-001, SR-002, and
  SR-003, including their no-bypass branches.
- Hash-bound readiness records, stable finding IDs, exact active-sprint
  resolution, bounded batch scans, approved-GDD verification, and asset
  dependency classification remain outside this P0 spec revision.
- Upstream story creation must eventually emit the required active TR and source
  snapshot fields; until then the intentional fail-closed result is non-ready.
