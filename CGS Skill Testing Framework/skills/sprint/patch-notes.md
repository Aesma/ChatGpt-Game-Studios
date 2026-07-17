# Skill Test Spec: $patch-notes

## Skill Summary

`$patch-notes` generates player-facing patch notes
from existing changelog content, stripping internal task IDs and technical
jargon in favor of plain language. It filters entries to only those relevant
to players (visible features and bug fixes; internal refactors are excluded).
No director gates are used. The skill asks "May I apply the proposed changeset?" before persisting. Verdict is always COMPLETE.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keyword: COMPLETE
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
6. User approves; file written; verdict COMPLETE

**Assertions:**
- [ ] Only 3 entries appear in the patch notes (2 internal entries excluded)
- [ ] Entries are written in plain language without internal task IDs
- [ ] File path matches `docs/patch-notes-v0.4.0.md`
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Verdict is COMPLETE after write

---

### Case 2: No Changelog Found — Directed to run $changelog first

**Fixture:**
- `docs/CHANGELOG.md` does NOT exist

**Input:** `$patch-notes v0.4.0`

**Expected behavior:**
1. Skill attempts to read `docs/CHANGELOG.md` — not found
2. Skill outputs: "No changelog found — run $changelog first to generate one"
3. No patch notes are generated; no file is written

**Assertions:**
- [ ] Skill does not crash when changelog is absent
- [ ] Output explicitly directs user to run `$changelog`
- [ ] Remains read-only; no authorization prompt appears because the workflow does not modify files
- [ ] Verdict is BLOCKED (dependency not met)

---

### Case 3: Tone Guidance from Design Folder — Incorporated into output

**Fixture:**
- `docs/CHANGELOG.md` exists with player-facing entries
- `design/community/tone-guide.md` exists with guidance: "upbeat, encouraging tone; avoid passive voice"

**Input:** `$patch-notes v0.4.0`

**Expected behavior:**
1. Skill reads changelog
2. Skill detects tone guide at `design/community/tone-guide.md`
3. Skill applies tone guidance when rewriting entries in plain language
4. Patch notes use upbeat, active-voice phrasing
5. Skill presents draft, asks to write, writes on approval

**Assertions:**
- [ ] Skill checks `design/` for a community or tone guidance file
- [ ] Tone guide content influences phrasing of patch note entries
- [ ] Output reflects active voice and upbeat tone where applicable
- [ ] Skill notes that tone guidance was applied

---

### Case 4: Patch Note Template Exists — Used instead of generated structure

**Fixture:**
- `docs/patch-notes-template.md` exists with a project-specific structured header format
- `docs/CHANGELOG.md` exists with player-facing entries

**Input:** `$patch-notes v0.4.0`

**Expected behavior:**
1. Skill reads changelog and detects template exists
2. Skill populates the template with player-facing entries
3. Template header/footer structure is preserved in the output
4. Skill asks "changeset authorization" and writes on approval

**Assertions:**
- [ ] Skill checks for a patch notes template before generating from scratch
- [ ] Template structure is used when found (not overridden by default format)
- [ ] Player-facing entries are inserted into the correct template section
- [ ] Output note confirms template was used

---

### Case 5: Gate Compliance — No gate; community-manager is separate

**Fixture:**
- `docs/CHANGELOG.md` exists with player-facing entries
- `review-mode.txt` contains `full`

**Input:** `$patch-notes v0.4.0`

**Expected behavior:**
1. Skill compiles patch notes in full mode
2. No director gate is invoked (community review is a separate, manual step)
3. Skill inherits the parent Codex model and reasoning settings
4. Skill notes in output: "Consider sharing draft with community manager before publishing"
5. Skill asks user for approval and writes on confirmation

**Assertions:**
- [ ] No director gate is invoked regardless of review mode
- [ ] Output suggests (but does not require) community manager review
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Verdict is COMPLETE

---

## Protocol Compliance

- [ ] Reads `docs/CHANGELOG.md` before generating patch notes
- [ ] Filters entries to player-facing items only
- [ ] Rewrites entries in plain language without internal IDs
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] No director gates are invoked
- [ ] Does not pin model or reasoning settings; inherits the parent Codex session

---

## Coverage Notes

- The case where all changelog entries are internal (zero player-facing items)
  is not tested; behavior is an empty patch notes draft with a warning.
- Version number parsing from the changelog header is an implementation detail
  not verified here.
- The community manager consultation noted in Case 5 is advisory; a separate
  skill or manual review handles that step.
