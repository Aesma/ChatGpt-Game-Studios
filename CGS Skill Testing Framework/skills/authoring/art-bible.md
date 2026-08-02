# Skill Test Spec: $art-bible

## Skill Summary

`$art-bible` is a guided, section-by-section art bible authoring skill. Its nine
sections are Visual Identity Statement, Mood & Atmosphere, Shape Language, Color
System, Character Design Direction, Environment Design Language, UI/HUD Visual
Direction, Asset Standards, and Reference Direction. Fresh authoring previews
that exact skeleton and target path before the first write.

In `full` review mode, the AD-ART-BIBLE director gate (art director) runs after
all nine sections have been authored into the draft and before asset production.
It does not run for a partial-scope edit. In `lean` and `solo`
modes, AD-ART-BIBLE is skipped and only user approval is required. The verdict
is COMPLETE when all sections are written.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keyword: COMPLETE
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
6. All sections written after approval; verdict is COMPLETE

**Assertions:**
- [ ] Skeleton file is created first (before any section content is written)
- [ ] The fresh skeleton contains the same nine headings and order as retrofit and authoring phases
- [ ] The target path, skeleton, and any directory creation are authorized before the first write
- [ ] AD-ART-BIBLE gate is invoked in full mode after draft is complete
- [ ] AD-ART-BIBLE is executed by `art-director`, never `creative-director`
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
3. User selects Character Design Rules
4. Skill drafts updated content; because this is a partial-scope edit, it does
   not run the production-ready AD-ART-BIBLE sign-off
5. Skill asks "May I apply the proposed changeset?"
6. Only that section is updated; other sections preserved; verdict is COMPLETE

**Assertions:**
- [ ] Existing art bible is detected and retrofit is offered
- [ ] Only the selected section is updated
- [ ] A single-section retrofit does not receive global production-ready sign-off
- [ ] Other sections are preserved
- [ ] Verdict is COMPLETE

---

### Case 5: Solo Mode — AD-ART-BIBLE Skipped, Noted in Output

**Fixture:**
- No existing art bible
- `production/session-state/review-mode.txt` contains `solo`

**Input:** `$art-bible`

**Expected behavior:**
1. Skill reads review mode — determines `solo`
2. Art bible is drafted and written with only user approval
3. AD-ART-BIBLE gate is skipped: output notes "[AD-ART-BIBLE] skipped — solo mode"
4. No director agents are spawned
5. Verdict is COMPLETE

**Assertions:**
- [ ] AD-ART-BIBLE gate is NOT invoked in solo mode
- [ ] Skip is explicitly noted with "solo mode" label
- [ ] No director agents of any kind are spawned
- [ ] Verdict is COMPLETE

---

## Protocol Compliance

- [ ] Creates skeleton file immediately with all section headers
- [ ] Uses exactly the nine canonical section names in summary, retrofit, skeleton, and assertions
- [ ] Discusses and drafts one section at a time
- [ ] AD-ART-BIBLE gate runs in full mode after all sections are drafted
- [ ] AD-ART-BIBLE is skipped in lean and solo modes — noted by name
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Verdict is COMPLETE when all sections are written

---

## Coverage Notes

- The case where AD-ART-BIBLE returns REJECT (not just CONCERNS) is not
  separately tested; the skill would block writing and ask the user how to
  proceed (revise or override).
- Typography is handled within UI/HUD Visual Direction; it is not a separate
  tenth section.
- The art bible feeds into `$asset-spec` — this relationship is noted in the
  handoff but not tested as part of this skill's spec.

## P1 Regression Assertions

- [ ] AD-ART-BIBLE runs only after all nine sections have substantive content; partial scope never receives production-ready sign-off
- [ ] Fresh authoring cannot choose section 8 alone, and retrofit can do so only when sections 1–4 are complete
- [ ] File authorization and per-section product approval are distinct
- [ ] A failed mandatory specialist prevents that section from being written as complete; parallel partial failure is surfaced
- [ ] The design-system state check excludes game-concept, systems-index, and review reports
