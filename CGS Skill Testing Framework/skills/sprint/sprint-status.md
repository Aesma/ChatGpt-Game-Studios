# Skill Test Spec: $sprint-status

## Skill Summary

`$sprint-status` is a read-only status skill that reads the current active
sprint file and the session state to produce a concise sprint health summary.
It reports story counts by status (Complete / In Progress / Blocked / Not Started)
and emits one of three sprint-health verdicts: ON TRACK, AT RISK, or BEHIND.
It never writes files and does not invoke any director gates. It is designed for
fast, low-cost status checks during a session.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings or numbered check sections
- [ ] Contains sprint-health verdict keywords: ON TRACK, AT RISK, BEHIND
- [ ] Remains read-only; no authorization prompt appears because the workflow does not modify files
- [ ] Has a next-step handoff (what to do based on the verdict)

---

## Director Gate Checks

None. `$sprint-status` is a read-only reporting skill; no gates are invoked.

---

## Test Cases

### Case 1: Happy Path — Mixed sprint, AT RISK with named blocker

**Fixture:**
- `production/sprints/sprint-004.md` exists (active sprint, linked in `active.md`)
- Sprint contains 6 stories:
  - 3 with `Status: Complete`
  - 2 with `Status: In Progress`
  - 1 with `Status: Blocked` (blocker: "Waiting on physics ADR acceptance")
- Sprint end date is 2 days away

**Input:** `$sprint-status`

**Expected behavior:**
1. Skill reads `production/session-state/active.md` to find active sprint reference
2. Skill reads `production/sprints/sprint-004.md`
3. Skill counts stories by status: 3 Complete, 2 In Progress, 1 Blocked
4. Skill detects a Blocked story and the approaching deadline
5. Skill outputs AT RISK verdict with the blocker named explicitly

**Assertions:**
- [ ] Output includes story count breakdown by status
- [ ] Output names the specific blocked story and its blocker reason
- [ ] Verdict is AT RISK (not BLOCKED, not ON TRACK) when any story is Blocked
- [ ] Skill does not write any files

---

### Case 2: All Stories Complete — ON TRACK with completion flag

**Fixture:**
- `production/sprints/sprint-004.md` exists
- All 5 stories have `Status: Complete`

**Input:** `$sprint-status`

**Expected behavior:**
1. Skill reads sprint file — all stories are Complete
2. Skill outputs ON TRACK and adds the all-Must-Haves completion flag
3. Skill suggests running `$milestone-review` or `$sprint-plan` as next steps

**Assertions:**
- [ ] Verdict is ON TRACK when all stories are Complete
- [ ] Output notes that the sprint is fully done
- [ ] Next-step suggestion references `$milestone-review` or `$sprint-plan`
- [ ] No files are written

---

### Case 3: No Active Sprint File — Guidance to run $sprint-plan

**Fixture:**
- `production/session-state/active.md` does not reference an active sprint
- `production/sprints/` directory is empty or absent

**Input:** `$sprint-status`

**Expected behavior:**
1. Skill reads `active.md` — finds no active sprint reference
2. Skill checks `production/sprints/` — finds no files
3. Skill outputs an informational message: no active sprint detected
4. Skill suggests running `$sprint-plan` to create one

**Assertions:**
- [ ] Skill does not error or crash when no sprint file exists
- [ ] Output clearly states no active sprint was found
- [ ] Output recommends `$sprint-plan` as the next action
- [ ] No verdict keyword is emitted (no sprint to assess)

---

### Case 4: Edge Case — Stale In Progress Story (flagged)

**Fixture:**
- `production/sprints/sprint-004.md` exists
- One story file has `Status: In Progress` and `Last Updated: 2026-03-30`
  (more than 4 days before today's session date)
- No stories are Blocked

**Input:** `$sprint-status`

**Expected behavior:**
1. Skill reads the story file's Last Updated field
2. Skill detects the story has been In Progress for >4 days without update
3. Skill flags the story as "stale" in the output
4. Verdict is AT RISK (stale in-progress stories indicate a hidden blocker)

**Assertions:**
- [ ] Skill compares story "last updated" metadata against session date
- [ ] Stale In Progress story is flagged by name in the output
- [ ] Verdict is AT RISK, not ON TRACK, when a stale story is detected
- [ ] Output does not conflate "stale" with "Blocked" — the label is distinct

---

### Case 5: Gate Compliance — Read-only; no gate invocation

**Fixture:**
- `production/sprints/sprint-004.md` exists with 4 stories (2 Complete, 2 In Progress)
- `production/session-state/review-mode.txt` contains `full`

**Input:** `$sprint-status`

**Expected behavior:**
1. Skill reads sprint and produces status summary
2. Skill does NOT invoke any director gate regardless of review mode
3. Output is a plain status report with ON TRACK, AT RISK, or BEHIND verdict
4. Skill does not prompt for user approval or ask to write any file

**Assertions:**
- [ ] No director gate is invoked in any review mode
- [ ] Remains read-only; no authorization prompt appears because the workflow does not modify files
- [ ] Skill completes and returns a verdict without user interaction
- [ ] Review mode file is ignored (or confirmed irrelevant) by this skill

---

## Protocol Compliance

- [ ] Does NOT use file-editing operations (read-only skill)
- [ ] Presents story count breakdown before emitting verdict
- [ ] Does not ask for approval
- [ ] Ends with a recommended next step based on verdict
- [ ] Does not pin model or reasoning settings; inherits the parent Codex session
- [ ] Blank invocation resolves active.md, then matching YAML, then highest numbered sprint
- [ ] Explicit historical sprint ignores singleton YAML for another sprint
- [ ] `in-progress` and historical `in_progress` both report IN PROGRESS
- [ ] Story BLOCKED is a risk reason, never a sprint-health verdict
- [ ] Staleness uses the story file and a >4 day threshold; active.md is same-story fallback only

---

### Case 6: Explicit historical sprint is not replaced by current YAML

**Fixture:** request sprint 3; markdown for sprint 3 exists; singleton YAML says sprint 4.

**Assertions:**
- [ ] Report remains scoped to sprint 3
- [ ] YAML is identified as belonging to sprint 4 and ignored for statuses/dates
- [ ] Markdown/story fallback is used without writing

### Case 7: Current sprint source priority is deterministic

**Fixture:** active.md references sprint 4, YAML says sprint 5, and sprint 6 has
the newest modification time.

**Assertions:**
- [ ] Blank invocation selects sprint 4 from active.md
- [ ] If active.md is invalid, matching YAML is tried next
- [ ] Only when both are unusable is the highest numbered sprint selected
- [ ] Modification time alone never selects the current sprint

---

## Coverage Notes

- The case where multiple sprints are active simultaneously is not tested;
  the skill reads whichever sprint `active.md` references.
- Partial sprint completion percentages are not explicitly verified; the
  count-by-status output implies them.
- The `solo` mode review-mode variant is not separately tested; gate
  behavior in Case 5 applies to all modes equally.
