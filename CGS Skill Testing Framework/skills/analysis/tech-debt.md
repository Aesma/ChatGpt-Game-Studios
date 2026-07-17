# Skill Test Spec: $tech-debt

## Skill Summary

`$tech-debt` tracks, categorizes, and prioritizes technical debt across the
codebase. It reads `docs/tech-debt-register.md` for the existing debt register
and scans source files in `src/` for inline `TODO` and `FIXME` comments. It
merges and sorts items by severity. No director gates are invoked. The skill
asks "May I apply the proposed changeset?" before updating. Verdicts:
REGISTER UPDATED or NO NEW DEBT FOUND.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: REGISTER UPDATED, NO NEW DEBT FOUND
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
6. User approves; register updated; verdict REGISTER UPDATED

**Assertions:**
- [ ] Inline comments are found by scanning `src/` recursively
- [ ] Existing register items are not duplicated
- [ ] Combined list is sorted by severity
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
5. User approves; register created with 4 items; verdict REGISTER UPDATED

**Assertions:**
- [ ] Skill does not crash when register file is absent
- [ ] User is offered register creation (not silently skipping)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
5. User approves; register updated; verdict REGISTER UPDATED

**Assertions:**
- [ ] No director gate is invoked in any review mode
- [ ] Debt table is presented before any write prompt
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Write only occurs with explicit user approval

---

## Protocol Compliance

- [ ] Reads `docs/tech-debt-register.md` and scans `src/` before compiling
- [ ] Deduplicates inline comments against existing register items
- [ ] Sorts combined list by severity
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] No director gates are invoked
- [ ] Verdict is REGISTER UPDATED or NO NEW DEBT FOUND

---

## Coverage Notes

- The case where `src/` is empty or absent is not tested; behavior follows
  the NO NEW DEBT FOUND path for the inline scan, but register items would
  still be read and presented.
- TODO comments without severity tags are treated as LOW severity by default;
  this classification detail is an implementation concern, not tested here.
