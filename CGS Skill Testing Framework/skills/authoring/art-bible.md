# Skill Test Spec: $art-bible

## Skill Summary

`$art-bible` is a guided, section-by-section art bible authoring skill. It
produces a comprehensive visual direction document covering: Visual Style overview,
Color Palette, Typography, Character Design Rules, Environment Style, and UI
Visual Language. The skill follows the skeleton-first pattern: creates the file
with all section headers immediately, then fills each section through discussion
and writes each to disk after user approval.

In `full` review mode, the AD-ART-BIBLE director gate (art director) runs after
the draft is complete and before any section is written. In `lean` and `solo`
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
- [ ] AD-ART-BIBLE gate is invoked in full mode after draft is complete
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
3. User selects Character Design Rules
4. Skill drafts updated content; in full mode, AD-ART-BIBLE is invoked for the
   revised section before applying a not-yet-authorized changeset
5. Skill asks "May I apply the proposed changeset?"
6. Only that section is updated; other sections preserved; verdict is COMPLETE

**Assertions:**
- [ ] Existing art bible is detected and retrofit is offered
- [ ] Only the selected section is updated
- [ ] In full mode: AD-ART-BIBLE gate runs even for single-section retrofit
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
- The Typography section is listed as a required art bible section but its
  specific content requirements are not assertion-tested here.
- The art bible feeds into `$asset-spec` — this relationship is noted in the
  handoff but not tested as part of this skill's spec.
