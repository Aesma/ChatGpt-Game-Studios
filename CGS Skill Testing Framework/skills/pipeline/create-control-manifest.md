# Skill Test Spec: $create-control-manifest

## Skill Summary

`$create-control-manifest` reads all Accepted ADRs from `docs/architecture/` and
generates a control manifest — a summary document that captures all architectural
constraints, required patterns, and forbidden patterns in one place. The manifest
is the reference document that story authors use when writing story files, ensuring
stories inherit the correct architectural rules without having to read all ADRs
individually.

The skill only includes Accepted ADRs; Proposed ADRs are excluded and noted. It
has no director gates. The skill asks "May I apply the proposed changeset?"
6. Writes the manifest after approval

**Assertions:**
- [ ] All 4 Accepted ADRs are represented in the manifest
- [ ] Manifest includes distinct sections for Required Patterns and Forbidden Patterns
- [ ] Manifest includes the source ADR number for each constraint
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts

**Assertions:**
- [ ] Only the 3 Accepted ADRs appear in the manifest content
- [ ] Excluded Proposed ADRs are listed by name in the output
- [ ] User sees the exclusion list before approving the write
- [ ] Skill does NOT silently omit Proposed ADRs without noting them

---

### Case 4: Edge Case — Manifest already exists

**Fixture:**
- `docs/architecture/control-manifest.md` already exists (version 1, dated last week)
- `docs/architecture/` contains Accepted ADRs (some new since last manifest)

**Input:** `$create-control-manifest`

**Expected behavior:**
1. Skill detects existing manifest and reads its version number / date
2. Skill offers to regenerate: "control-manifest.md already exists (v1, [date]). Regenerate with current ADRs?"
3. If user confirms: skill drafts updated manifest, increments version number
4. Asks "May I apply the proposed changeset?" (overwrite)
5. Writes updated manifest after approval

**Assertions:**
- [ ] Skill reads and reports the existing manifest version before offering to regenerate
- [ ] User is offered a regenerate/skip choice — not auto-overwritten
- [ ] Updated manifest has an incremented version number
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] No director gates — no review-mode.txt read
- [ ] Ends with next-step handoff: `$create-epics` or `$create-stories`

---

## Coverage Notes

- The exact section structure of the generated manifest (constraint tables, pattern
  lists) is defined by the skill body and not re-enumerated in test assertions.
- The `version` field incrementing logic (v1 → v2) is tested via Case 4 but exact
  version numbering format is not fixture-locked.
- ADR parsing (extracting Required/Forbidden Patterns) depends on consistent ADR
  structure — tested implicitly via Case 1's fixture.
