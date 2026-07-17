# Skill Test Spec: $design-system

## Skill Summary

`$design-system` guides the user through section-by-section authoring of a Game
Design Document (GDD) for a single game system. All 8 required sections must be
authored: Overview, Player Fantasy, Detailed Rules, Formulas, Edge Cases,
Dependencies, Tuning Knobs, and Acceptance Criteria. The skill uses a
skeleton-first approach — it creates the GDD file with all 8 section headers
before filling any content, then applies the approved bounded document changeset
without section-by-section re-prompts.

The CD-GDD-ALIGN gate (creative-director) runs in both `full` AND `lean` modes.
It is only skipped in `solo` mode. If an existing GDD file is found, the skill
offers a retrofit mode to update specific sections rather than rewriting the whole
document.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: APPROVED, NEEDS REVISION, MAJOR REVISION
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
6. Section written to file after user approval
7. Process repeats for all 8 sections

**Assertions:**
- [ ] Skeleton file is created with all 8 section headers before any content is written
- [ ] CD-GDD-ALIGN runs on each section in lean mode (not skipped)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
3. User selects a specific section (e.g., Formulas)
4. Skill authors only that section, runs CD-GDD-ALIGN, asks "May I apply the proposed changeset?"
5. Only the selected section is updated — other sections are not modified

**Assertions:**
- [ ] Skill detects and reads existing GDD before offering retrofit mode
- [ ] User is asked which section to update — not asked to rewrite the whole document
- [ ] Only the selected section is rewritten — others remain unchanged
- [ ] CD-GDD-ALIGN still runs on the updated section
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts

**Assertions:**
- [ ] Section is NOT written when CD-GDD-ALIGN returns MAJOR REVISION
- [ ] Gate feedback is shown to the user before requesting revision
- [ ] CD-GDD-ALIGN runs again after the section is revised
- [ ] Skill does NOT auto-proceed to the next section while MAJOR REVISION is unresolved

---

### Case 4: Solo Mode — CD-GDD-ALIGN skipped; sections written with user approval only

**Fixture:**
- New GDD being authored
- `production/session-state/review-mode.txt` contains `solo`

**Input:** `$design-system [system-name]`

**Expected behavior:**
1. Skeleton file is created with 8 section headers
2. For each section: drafted, shown to user
3. CD-GDD-ALIGN is skipped — noted per section: "CD-GDD-ALIGN skipped — solo mode"
4. "May I apply the proposed changeset?" asked after user reviews draft
5. Section written after user approval
6. No gate review at any stage

**Assertions:**
- [ ] "CD-GDD-ALIGN skipped — solo mode" noted for each section
- [ ] Sections are written after user approval alone (no gate required)
- [ ] Skill does NOT spawn any CD-GDD-ALIGN gate in solo mode
- [ ] Full GDD is written with only user approval in solo mode

---

### Case 5: Director Gate — Empty sections not written to file

**Fixture:**
- GDD authoring in progress
- User and skill discuss one section but do not produce any approved content
  (e.g., discussion ends without a decision, or user says "skip for now")

**Input:** `$design-system [system-name]`

**Expected behavior:**
1. Section discussion produces no approved content
2. Skill does NOT write an empty or placeholder body to the section
3. The section header remains in the skeleton file but the body stays empty
4. Skill moves to the next section without writing the empty one
5. At the end, incomplete sections are listed and user is reminded to return to them

**Assertions:**
- [ ] Empty or unapproved sections are NOT written to the file
- [ ] Skeleton section header remains (preserves structure)
- [ ] Skill tracks and lists incomplete sections at the end of the session
- [ ] Skill does NOT write "TBD" or placeholder content outside the authorized changeset

---

## Protocol Compliance

- [ ] Skeleton file created with all 8 headers before any content is written
- [ ] CD-GDD-ALIGN runs in both full AND lean mode (not just full)
- [ ] CD-GDD-ALIGN skipped only in solo mode — noted per section
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] MAJOR REVISION from CD-GDD-ALIGN blocks section write until resolved
- [ ] Only approved, non-empty sections are written to the file
- [ ] Ends with next-step handoff: `$review-all-gdds` or `$map-systems next`

---

## Coverage Notes

- The 8 required sections are validated against the project's design document
  standards defined in `AGENTS.md` — not re-enumerated here.
- The skill's internal section-ordering logic (which section to author first) is
  not independently tested — the order follows the standard GDD template.
- Pillar alignment checking within CD-GDD-ALIGN is evaluated holistically by
  the gate agent — specific pillar checks are not fixture-tested here.
