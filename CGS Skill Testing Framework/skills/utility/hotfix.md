# Skill Test Spec: $hotfix

## Skill Summary

`$hotfix` manages an emergency fix workflow: it creates a hotfix branch from
main, applies a targeted fix to the identified file(s), runs `$smoke-check` to
validate the fix doesn't introduce regressions, and prompts the user to confirm
merge back to main. Each code change requires a "May I apply the proposed changeset?" ask.
Git operations (branch creation, merge) are presented as Bash commands for user
confirmation before execution.

The skill is time-sensitive — director review is optional post-hoc, not a
blocking gate. Verdicts: HOTFIX COMPLETE (fix applied, smoke check passed, merged)
or HOTFIX BLOCKED (fix introduced regression or user declined).

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: HOTFIX COMPLETE, HOTFIX BLOCKED
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
5. Skill runs `$smoke-check` — PASS
6. Skill presents the merge command and asks user to confirm merge to `main`
7. User confirms; merge executes; verdict is HOTFIX COMPLETE

**Assertions:**
- [ ] Hotfix branch is created before any code changes
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
4. If user confirms version bump: skill asks "May I apply the proposed changeset?"
5. After version update and merge: verdict is HOTFIX COMPLETE with version noted

**Assertions:**
- [ ] Version tag context is detected and surfaced to user
- [ ] Patch version bump is suggested (not required) after merge
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Verdict is HOTFIX COMPLETE

---

### Case 4: No Repro Steps — Skill Asks Before Applying Fix

**Fixture:**
- User invokes `$hotfix` with a vague description: "something is broken on level 3"
- No repro steps provided

**Input:** `$hotfix` (vague description)

**Expected behavior:**
1. Skill detects insufficient information to identify the fix location
2. Skill asks: "Please provide reproduction steps and the affected file or system"
3. Skill does NOT create a branch or modify any file until repro steps are provided
4. After user provides repro steps: normal hotfix flow begins

**Assertions:**
- [ ] No branch is created without repro steps
- [ ] No code changes are made without a clearly identified fix location
- [ ] Repro step request is specific (not a generic "please provide more info")
- [ ] Normal hotfix flow resumes after user provides repro steps

---

### Case 5: Director Gate Check — No gate; hotfixes are time-critical

**Fixture:**
- Critical bug with repro steps identified

**Input:** `$hotfix`

**Expected behavior:**
1. Skill completes the hotfix workflow
2. No director agents are spawned during execution
3. No gate IDs appear in output
4. Post-hoc director review (if needed) is a manual follow-up, not invoked here

**Assertions:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Verdict is HOTFIX COMPLETE or HOTFIX BLOCKED — no gate verdict

---

## Protocol Compliance

- [ ] Creates hotfix branch before making any code changes
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Runs `$smoke-check` after applying the fix
- [ ] Requires explicit user confirmation before merging
- [ ] HOTFIX BLOCKED when smoke check fails — no automatic merge
- [ ] Verdict is HOTFIX COMPLETE or HOTFIX BLOCKED

---

## Coverage Notes

- The case where multiple files need to be modified for one fix follows the same
Treat the complete described file set as one bounded changeset: use existing task authorization, or preview and confirm it once before the first write.
- The post-hotfix steps (create bug report, update changelog) are suggested in
  the handoff but not tested as part of this skill's execution.
- Conflict resolution during the merge (if main has diverged) is not tested;
  the skill would surface the conflict and ask the user to resolve it manually.
