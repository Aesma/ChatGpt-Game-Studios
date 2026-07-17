# Skill Test Spec: $qa-plan

## Skill Summary

`$qa-plan` generates a structured QA test plan for a feature or sprint milestone.
It reads story files for the specified sprint, extracts acceptance criteria from
each story, cross-references test standards from `coding-standards.md` to assign
the appropriate test type (unit, integration, visual, UI, or config/data), and
produces a prioritized QA plan document.

The skill asks "May I apply the proposed changeset?" before
persisting the output. If an existing test plan for the same sprint is found, the
skill offers to update rather than replace. The verdict is COMPLETE when the plan
is written. No director gates are used — gate-level story readiness is handled by
`$story-readiness`.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keyword: COMPLETE
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
6. File is written on approval; verdict is COMPLETE

**Assertions:**
- [ ] All 4 stories are included in the plan
- [ ] Test type is assigned per coding-standards.md (not guessed)
- [ ] Gate level (BLOCKING vs ADVISORY) is noted for each story
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
5. Updated plan is written on approval

**Assertions:**
- [ ] Skill detects the existing plan file
- [ ] "update" language is used (not "overwrite")
- [ ] Only new stories are proposed for addition — existing entries preserved
- [ ] Verdict is COMPLETE

---

### Case 4: No Stories Found for Sprint — Error with guidance

**Fixture:**
- `production/sprints/sprint-007.md` does not exist
- No other sprint file matching sprint-007

**Input:** `$qa-plan sprint-007`

**Expected behavior:**
1. Skill attempts to read sprint-007.md — file not found
2. Skill outputs: "No sprint file found for sprint-007"
3. Skill suggests running `$sprint-plan` to create the sprint first
4. No plan is written; no "changeset authorization" is asked

**Assertions:**
- [ ] Error message names the missing sprint file
- [ ] `$sprint-plan` is suggested as the remediation step
- [ ] No file modification occurs
- [ ] Verdict is not COMPLETE (error state)

---

### Case 5: Director Gate Check — No gate; QA planning is a utility

**Fixture:**
- Sprint with valid stories and AC

**Input:** `$qa-plan sprint-003`

**Expected behavior:**
1. Skill generates and writes QA plan
2. No director agents are spawned
3. No gate IDs appear in output

**Assertions:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Skill reaches COMPLETE without any gate check

---

## Protocol Compliance

- [ ] Reads coding-standards.md test evidence table before assigning test types
- [ ] Assigns BLOCKING or ADVISORY gate level per story type
- [ ] Flags stories with no AC as UNTESTABLE (does not silently skip them)
- [ ] Detects existing plan and offers update path
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Verdict is COMPLETE when plan is written

---

## Coverage Notes

- The case where `coding-standards.md` is missing (skill cannot assign test types)
  is not fixture-tested; behavior would follow the BLOCKED pattern with a note
  to restore the standards file.
- Multi-sprint planning (spanning 2 sprints) is not tested; the skill is designed
  for one sprint at a time.
- Config/data story type (balance tuning → smoke check) follows the same
  assignment pattern as other types in Case 1 and is not separately tested.
