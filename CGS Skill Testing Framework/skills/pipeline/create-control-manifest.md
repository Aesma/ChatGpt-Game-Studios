# Skill Test Spec: $create-control-manifest

## Skill Summary

`$create-control-manifest` extracts meaning-preserving programmer rules from
Accepted ADRs, technical preferences, and the pinned engine reference. It writes
`docs/architecture/control-manifest.md` only after one complete changeset
authorization. In full review mode it runs TD-MANIFEST; lean and solo record the
gate skip.

---

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only `name` and non-empty `description`
- [ ] Has at least two phase headings
- [ ] Only `must`, `required`, and `always` statements become Required
- [ ] Merely rejected alternatives do not become Forbidden
- [ ] There is exactly one changeset authorization point

---

## Director Gate Checks

- [ ] Full mode runs TD-MANIFEST against the complete extracted rule list
- [ ] Lean and solo skip TD-MANIFEST and name the resolved mode
- [ ] REJECT prevents the manifest write

---

## Test Cases

### Case 1: Happy Path — Accepted ADR rules preserve modality and scope

**Fixture:**
- Four Accepted ADRs contain a mix of `must`, `should`, and `always`
- One ADR lists an unselected alternative without calling it forbidden
- Another ADR explicitly labels an API an anti-pattern
- Review mode resolves to `full`

**Expected behavior:**
1. Required contains the explicit must/required/always rules
2. The should statement remains advisory
3. The ordinary rejected alternative is not turned into a Never rule
4. The explicit anti-pattern appears under Forbidden with source and scope
5. TD-MANIFEST runs, then the complete manifest draft is authorized once

**Assertions:**
- [ ] Every rule preserves modality, scope, and real source
- [ ] Cross-layer rules appear once in Global Rules unless the source defines distinct variants
- [ ] Phase 4 content approval is not treated as file authorization
- [ ] Phase 5 is the only write authorization point

---

### Case 2: Proposed ADRs are not extracted

**Fixture:**
- Three Accepted ADRs and two Proposed ADRs exist

**Assertions:**
- [ ] Only Accepted ADR content becomes manifest rules
- [ ] Proposed content cannot strengthen or forbid implementation behavior
- [ ] The write remains subject to the single complete changeset authorization

---

### Case 3: Review modes use the shared TD-MANIFEST contract

**Assertions:**
- [ ] Full mode invokes TD-MANIFEST before the write
- [ ] Lean and solo do not invoke the gate and show the appropriate skip note
- [ ] A full-mode REJECT prevents the write
- [ ] No mode claims that the workflow has no director gate

---

### Case 4: Edge Case — Manifest already exists

**Fixture:**
- `docs/architecture/control-manifest.md` already exists
- Current Accepted ADRs produce an updated draft

**Input:** `$create-control-manifest update`

**Assertions:**
- [ ] Existing content is read before a replacement is proposed
- [ ] The full replacement is shown at the single authorization point
- [ ] The existing manifest is not overwritten before authorization
- [ ] Ends with the existing next-step handoff

---

### Case 5: Single authorization and rejected full-mode gate

**Assertions:**
- [ ] Phase 4 approval never writes the manifest
- [ ] A full-mode TD-MANIFEST REJECT stops before file authorization/write
- [ ] When the gate permits writing, Phase 5 shows the exact full draft and target once
- [ ] No second per-file or post-review authorization prompt appears

---

### Case 6: Empty/invalid inputs cannot overwrite a manifest

**Assertions:**
- [ ] Zero Accepted ADRs stops and preserves an existing manifest
- [ ] Missing engine configuration or VERSION stops before preview/write
- [ ] ADR Status is read from one normalized status field; ambiguous/missing status is excluded and reported

---

### Case 7: Duplicate/conflicting sources and version updates

**Assertions:**
- [ ] Identical rules merge while preserving all real source paths
- [ ] Conflicting ADR/preference/engine rules block the write with both statements
- [ ] Global sources never receive fabricated ADR IDs
- [ ] New manifest version is 1; each authorized update increments the integer once, including same-day updates
- [ ] Default existing-file mode asks update/stop; `update` still requires authorization

---

## Protocol Compliance

- [ ] Accepted ADR language is not semantically strengthened
- [ ] Ordinary rejected alternatives are not global bans
- [ ] Minimal formatting normalization never changes modality or scope
- [ ] Full/lean/solo gate behavior is deterministic
- [ ] The target file is written only after one complete changeset authorization
