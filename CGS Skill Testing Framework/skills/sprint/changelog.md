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
- [ ] A specified historical tag uses the previous tag through that tag, never latest-tag..HEAD
- [ ] A missing target boundary stops instead of silently substituting another range
- [ ] Internal output omits unsupported owner, commit hash/range, file-count, and line-count fields
- [ ] Entries are organized into Features / Fixes / Known Issues sections
- [ ] Sprint story references are used to enrich commit descriptions
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
5. User approves; new content is prepended, old entries intact; verdict COMPLETE

**Assertions:**
- [ ] Skill reads existing changelog before applying a not-yet-authorized changeset to detect prior content
- [ ] New section is prepended (not appended or overwriting) existing entries
- [ ] Old changelog entries for v0.2.0 and v0.3.0 are preserved in the written file
- [ ] No whole-file overwrite option is offered
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

- Git-not-initialized behavior is covered by the P1 regression assertions: the
  workflow stops before reading history.
- Merge commits vs. squash commits are not explicitly differentiated in
  these tests; implementation detail of the git log parsing phase.
- The `$patch-notes` skill should be run after `$changelog` for player-facing
  output; that handoff is verified in the patch-notes spec.

## P1 Regression Assertions

- [ ] Git repository validity is checked before any log/tag command; invalid repositories stop
- [ ] No-argument, tag, and sprint inputs have deterministic validation and ambiguous/missing targets stop
- [ ] A GDD can explain a commit/closed story but never independently creates a shipped item
- [ ] Known Issues come only from relevant Open bug reports and are omitted when no source was read
- [ ] Existing CHANGELOG content is read before preview; an existing version section is replaced in place without duplication
- [ ] An unchanged same-version rerun performs no write
- [ ] Player output omits the feedback placeholder when no configured link exists
