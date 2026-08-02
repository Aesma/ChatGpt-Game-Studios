# Skill Test Spec: $sprint-plan

## Skill Summary

`$sprint-plan` reads the current milestone file and backlog stories, then
generates a new numbered sprint with stories prioritized by implementation layer
and priority score. In full mode the PR-SPRINT director gate runs after the
sprint draft is compiled (producer reviews the plan). In lean and solo modes
the gate is skipped. The skill asks "May I apply the proposed changeset?"
before persisting. Verdicts: COMPLETE (sprint generated and written) or
BLOCKED (cannot proceed due to missing data or gate failure).

Blank invocation is `new`. `status` is a read-only terminal mode. New/update
writes the sprint markdown, singleton YAML, and a newly selected review mode in
one final authorized changeset after both producer and QA-plan checks.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: COMPLETE, BLOCKED
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
7. User approves; file is written

**Assertions:**
- [ ] Stories are sorted by implementation layer before priority
- [ ] Sprint draft is shown before any write or gate invocation
- [ ] PR-SPRINT gate is invoked in full mode after draft is ready
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Written file path matches `production/sprints/sprint-003.md`
- [ ] Verdict is COMPLETE after successful write

---

### Case 2: Blocked Path — Backlog is empty

**Fixture:**
- `production/milestones/milestone-02.md` exists
- No unstarted stories exist in any epic backlog

**Input:** `$sprint-plan`

**Expected behavior:**
1. Skill reads backlog — finds no unstarted stories
2. Skill outputs "No unstarted stories in backlog"
3. Skill suggests running `$create-stories` to populate the backlog
4. No gate is invoked; no file is written

**Assertions:**
- [ ] Verdict is BLOCKED
- [ ] Output contains "No unstarted stories" or equivalent message
- [ ] Output recommends `$create-stories`
- [ ] PR-SPRINT gate is NOT invoked
- [ ] No file modification occurs

---

### Case 3: Gate returns CONCERNS — Sprint overloaded, revised before write

**Fixture:**
- Backlog has 8 stories totalling 16 points; milestone capacity is 10 points
- `review-mode.txt` contains `full`

**Input:** `$sprint-plan`

**Expected behavior:**
1. Skill drafts sprint with all 8 stories (over capacity)
2. PR-SPRINT gate runs; producer returns CONCERNS: sprint is overloaded
3. Skill presents concern to user and asks which stories to defer
4. User selects 3 stories to defer; sprint is revised to 5 stories / 10 points
5. Skill asks "changeset authorization" with revised sprint; writes on approval

**Assertions:**
- [ ] CONCERNS from PR-SPRINT gate surfaces to user before any write
- [ ] Skill allows sprint to be revised after gate feedback
- [ ] Revised sprint (not original) is written to file
- [ ] Verdict is COMPLETE after revision and write

---

### Case 4: Lean Mode — PR-SPRINT gate skipped

**Fixture:**
- Backlog has 4 stories; milestone capacity is 8 points
- `review-mode.txt` contains `lean`

**Input:** `$sprint-plan`

**Expected behavior:**
1. Skill reads review mode — determines `lean`
2. Skill drafts sprint and presents it to user
3. PR-SPRINT gate is skipped; output notes "[PR-SPRINT] skipped — Lean mode"
4. Skill asks user for direct approval of the sprint
5. User approves; sprint file is written

**Assertions:**
- [ ] PR-SPRINT gate is NOT invoked in lean mode
- [ ] Skip is explicitly noted in output
- [ ] User approval is still required before write (gate skip ≠ approval skip)
- [ ] Verdict is COMPLETE after write

---

### Case 5: Edge Case — Previous sprint still has open stories

**Fixture:**
- `production/sprints/sprint-002.md` exists with 2 stories still `Status: In Progress`
- Backlog has 5 new unstarted stories
- `review-mode.txt` contains `full`

**Input:** `$sprint-plan`

**Expected behavior:**
1. Skill reads sprint-002 and detects 2 open (`in_progress`) stories
2. Skill flags: "Sprint 002 has 2 open stories — confirm carry-over before planning sprint 003"
3. Skill presents user with choice: carry stories over, defer them, or cancel
4. User confirms carry-over; carried stories are prepended to new sprint with `[CARRY]` tag
5. Sprint draft is built; PR-SPRINT gate runs; sprint is written on approval

**Assertions:**
- [ ] Skill checks the most recent sprint file for open stories
- [ ] User is asked to confirm carry-over before sprint planning continues
- [ ] Carried stories appear in the new sprint draft with a distinguishing label
- [ ] Skill does not silently ignore open stories from the previous sprint

---

## Protocol Compliance

- [ ] Shows draft sprint before invoking PR-SPRINT gate or asking to write
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] PR-SPRINT gate only runs in full mode
- [ ] Skip message appears in lean and solo mode output
- [ ] Verdict is clearly stated at the end of the skill output
- [ ] Blank mode is `new`; unknown modes stop without writes
- [ ] `status` returns immediately after its report with no gate, authorization, or write
- [ ] Eligible stories come from `production/epics/**/*.md` and have satisfiable dependencies
- [ ] Capacity comes from an existing milestone/previous-sprint field or an explicit user answer, with 20% buffer
- [ ] Sprint number is max existing valid number plus one and target is `production/sprints/sprint-[NNN].md`
- [ ] A per-run `--review` value is resolved once and cannot be overwritten by the global file
- [ ] QA-plan handling finishes before the single changeset and COMPLETE verdict
- [ ] Missing `sprint-status.yaml` in update mode is reconstructed without resetting confirmed progress

---

### Case 6: Status mode is terminal and read-only

**Input:** `$sprint-plan status`

**Assertions:**
- [ ] The status report is shown and the workflow stops
- [ ] PR-SPRINT and the QA-plan write path are not entered
- [ ] No changeset authorization is requested and no file changes

### Case 7: Review override and first-run mode stay pending

**Fixture:** global mode is `lean`; invocation is `$sprint-plan new --review full`.

**Assertions:**
- [ ] Resolved mode remains `full` and PR-SPRINT runs
- [ ] The global file is not re-read to overwrite the per-run value
- [ ] When review-mode is initially absent, the selected value is not written early
- [ ] Any pending review-mode value is listed with markdown and YAML in the final changeset

### Case 8: QA decision precedes the only write

**Fixture:** no matching QA plan exists and the user chooses Skip.

**Assertions:**
- [ ] The warning block is merged into the pending sprint plan
- [ ] The final preview shows the warning and both sprint output paths
- [ ] COMPLETE appears only after the authorized writes succeed

### Case 9: Legacy update restores pending YAML

**Fixture:** sprint markdown and referenced stories exist; `sprint-status.yaml` does not.

**Assertions:**
- [ ] Pending YAML is reconstructed from markdown and story header statuses
- [ ] Confirmed `in_progress` and `done` states are preserved
- [ ] Unknown states are surfaced before authorization and are not guessed

### Case 10: Milestone, sprint history, and carryover are deterministic

**Assertions:**
- [ ] Current milestone and previous sprint use highest valid identifiers, not modification time
- [ ] Duplicate/conflicting identifiers block planning and missing milestone returns BLOCKED
- [ ] Open previous-sprint stories require carry/defer/cancel decisions before the draft
- [ ] A latest valid retrospective is read as context without accepting an extra argument

### Case 11: UNREALISTIC and gate failure never rewrite scope silently

**Assertions:**
- [ ] UNREALISTIC lists producer-recommended defer candidates and capacity impact
- [ ] The user chooses the actual deferrals; no choice means BLOCKED and no writes
- [ ] A missing/error/invalid PR-SPRINT result in full mode stops the run
- [ ] The current run never silently falls back to lean/solo

### Case 12: QA identity and atomic correspondence

**Assertions:**
- [ ] QA plan matches only by canonical filename or exact Sprint field
- [ ] Bare occurrences of the sprint number do not qualify
- [ ] Markdown and YAML require unique non-empty story IDs and project-relative paths
- [ ] Duplicate/missing mappings or a preparation/write failure cannot leave a partial plan
- [ ] Update removal is limited to `backlog`/`ready`; `in_progress`/`done` remain unless explicitly corrected

---

## Coverage Notes

- The case where no milestone file exists is not explicitly tested; behavior
  follows the BLOCKED pattern with a suggestion to run `$gate-check` for
  milestone progression.
- Solo mode behavior is equivalent to lean (gate skipped, user approval
  required) and is not separately tested.
- Parallel story selection algorithms are not tested here; those are unit
  concerns for the sprint-plan subagent.
