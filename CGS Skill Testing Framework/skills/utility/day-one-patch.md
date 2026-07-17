# Skill Test Spec: $day-one-patch

## Skill Summary

`$day-one-patch` prepares a day-one patch plan for issues that are known at
launch but deferred from the v1.0 release. It reads open bug reports in
`production/bugs/`, deferred acceptance criteria from story files (stories
marked `Status: Done` but with noted deferred ACs), and produces a prioritized
patch plan with estimated fix timelines per issue.

The patch plan is written to `production/releases/day-one-patch.md` after a
"May I apply the proposed changeset?"
6. File written; verdict is COMPLETE

**Assertions:**
- [ ] All 3 bugs appear in the plan
- [ ] Bugs are prioritized by severity (MEDIUM before LOW)
- [ ] Fix estimates are provided per issue
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
6. File written; verdict is COMPLETE

**Assertions:**
- [ ] "No known issues at launch" note appears in the written file
- [ ] Template headers are present in the empty plan
- [ ] Skill does NOT error out when there are no issues to plan
- [ ] Verdict is COMPLETE

---

### Case 5: Director Gate Check — No gate; day-one-patch is a planning utility

**Fixture:**
- Known issues present in production/bugs/

**Input:** `$day-one-patch`

**Expected behavior:**
1. Skill generates and writes the patch plan
2. No director agents are spawned
3. No gate IDs appear in output

**Assertions:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Verdict is COMPLETE without any gate check

---

## Protocol Compliance

- [ ] Reads open bugs from `production/bugs/` before generating the plan
- [ ] Scans story files for deferred AC notes
- [ ] Escalates CRITICAL (P0) bugs with explicit `$hotfix` guidance
- [ ] Produces an empty plan with note when no issues exist (not an error)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Verdict is COMPLETE in all paths

---

## Coverage Notes

- The case where multiple CRITICAL bugs exist is handled the same as Case 2;
  all P0 issues are escalated together.
- Timeline estimation for the patch (e.g., "patch available in 3 days")
  requires manual QA and build time estimates; the skill uses rough estimates
  based on severity, not actual team velocity.
- The patch notes player communication document (`$patch-notes`) is a separate
  skill invoked after the patch plan is executed.
