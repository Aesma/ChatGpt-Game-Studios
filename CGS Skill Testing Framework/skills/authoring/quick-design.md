# Skill Test Spec: $quick-design

## Skill Summary

`$quick-design` produces a lightweight design spec for features too small to
warrant a full 8-section GDD. The target scope is under 4 hours of design time
for a single-system feature. Instead of the full 8-section GDD format, the
quick-design spec uses a streamlined 3-section format: Overview, Rules, and
Acceptance Criteria.

The skill has no director gates — adding gate overhead would defeat the purpose
of a lightweight design tool. The skill asks "May I apply the proposed changeset?" is asked
6. File is written after approval

**Assertions:**
- [ ] Spec contains exactly 3 sections: Overview, Rules, Acceptance Criteria
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] File is written to the correct path: `design/quick-notes/[name].md`
- [ ] Verdict is CREATED after successful write

---

### Case 2: Failure Path — Scope check fails; redirected to $design-system

**Fixture:**
- Feature described spans multiple systems or would take more than 4 hours of design time
  (e.g., "redesign the entire combat system" or "new progression mechanic affecting all classes")

**Input:** `$quick-design [large-feature]`

**Expected behavior:**
1. Skill asks scoping questions
2. Skill determines scope exceeds the sub-4h / single-system threshold
3. Skill outputs: "This feature is too large for a quick-design. Use `$design-system [name]` for a full GDD."
4. Skill does NOT write a quick-note file
5. Verdict is REDIRECTED

**Assertions:**
- [ ] Skill detects the scope excess and stops before drafting
- [ ] Message explicitly names `$design-system` as the correct alternative
- [ ] No quick-note file is written
- [ ] Verdict is REDIRECTED (not CREATED or BLOCKED)

---

### Case 3: Edge Case — File already exists; offered to update

**Fixture:**
- `design/quick-notes/[name].md` already exists from a previous session

**Input:** `$quick-design [name]`

**Expected behavior:**
1. Skill detects existing quick-note file and reads its current content
2. Skill asks: "[name].md already exists. Update it, or create a new version?"
3. User selects update
4. Skill shows the existing spec and asks which section to revise
5. Updated spec is shown, "May I apply the proposed changeset?" asked, file updated after approval

**Assertions:**
- [ ] Skill detects and reads the existing file before offering to update
- [ ] User is offered update or create-new options — not auto-overwritten
- [ ] Only the revised section is updated (or the whole spec if user chooses full rewrite)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] No director gates — no review-mode.txt read
- [ ] Ends with next-step handoff (e.g., proceed to implementation or `$dev-story`)

---

## Coverage Notes

- The scope threshold heuristic (sub-4h, single-system) is a judgment call —
  the skill's internal check is the authoritative definition and is not
  independently tested by counting hours.
- The `design/quick-notes/` directory is created automatically if it does not
  exist — this filesystem behavior is not independently tested here.
- Integration with the story pipeline (can a quick-design generate a story
  directly?) is out of scope for this spec — quick-designs are standalone.
