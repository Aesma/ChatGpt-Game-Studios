# Skill Test Spec: $changelog

## Skill Summary

`$changelog` generates a developer-facing
changelog by reading git commit history and closed sprint stories since the
last release tag. It organizes entries into features, fixes, and known issues.
No director gates are used. The skill asks "May I apply the proposed changeset?"
before persisting. Verdict is always COMPLETE.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keyword: COMPLETE
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
6. User approves; file written; verdict COMPLETE

**Assertions:**
- [ ] Changelog covers commits since the most recent git tag
- [ ] Entries are organized into Features / Fixes / Known Issues sections
- [ ] Sprint story references are used to enrich commit descriptions
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
5. User approves; new content is prepended, old entries intact; verdict COMPLETE

**Assertions:**
- [ ] Skill reads existing changelog before applying a not-yet-authorized changeset to detect prior content
- [ ] New section is prepended (not appended or overwriting) existing entries
- [ ] Old changelog entries for v0.2.0 and v0.3.0 are preserved in the written file
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts

---

### Case 5: Gate Compliance — No gate; read-then-write with approval

**Fixture:**
- Git history has commits since last tag
- `review-mode.txt` contains `full`

**Input:** `$changelog`

**Expected behavior:**
1. Skill compiles changelog in full mode
2. No director gate is invoked (changelog generation is compilation, not a delivery gate)
3. Skill inherits the parent Codex model and reasoning settings
4. Skill asks user for approval and writes file on confirmation

**Assertions:**
- [ ] No director gate is invoked regardless of review mode
- [ ] Output does not reference any gate result
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Verdict is COMPLETE

---

## Protocol Compliance

- [ ] Reads git log and sprint story files before compiling
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] No director gates are invoked
- [ ] Verdict is always COMPLETE
- [ ] Does not pin model or reasoning settings; inherits the parent Codex session

---

## Coverage Notes

- The case where git is not initialized in the repository is not tested;
  behavior would depend on git command failure handling.
- Merge commits vs. squash commits are not explicitly differentiated in
  these tests; implementation detail of the git log parsing phase.
- The `$patch-notes` skill should be run after `$changelog` for player-facing
  output; that handoff is verified in the patch-notes spec.
