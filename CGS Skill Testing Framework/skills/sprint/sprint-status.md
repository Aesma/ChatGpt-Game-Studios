# Skill Test Spec: $sprint-status

## Skill Summary

`$sprint-status` is a read-only status skill that resolves exactly one sprint from an explicit argument, a revisioned tracker selector, or session state; it never uses mtime as authority. Before trusting tracker status it validates sprint identity, plan revision, a deterministic raw-story-set hash, and update timestamps. Any mismatch yields DATA CONFLICT and no health verdict. It recognizes In Review as unfinished and treats dev-story recovery checkpoints as hash-bound recovery evidence, not completion. It never writes files or invokes director gates.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings or numbered check sections
- [ ] Contains verdict keywords: ON TRACK, AT RISK, BLOCKED
- [ ] Remains read-only; no authorization prompt appears because the workflow does not modify files
- [ ] Has a next-step handoff (what to do based on the verdict)
- [ ] Explicitly forbids mtime-based sprint selection
- [ ] Requires sprint_id, active_sprint_id, plan_revision, story_set_hash, and updated_at before trusting an applicable tracker
- [ ] DATA CONFLICT stops before story counts or a health verdict
- [ ] IN REVIEW is never counted Complete
- [ ] Recovery checkpoints are identity- and hash-validated and never override status

---

## Director Gate Checks

None. `$sprint-status` is a read-only reporting skill; no gates are invoked.

---

## Test Cases

### Case 1: Happy Path — Mixed sprint, AT RISK with named blocker

**Fixture:**
- `production/sprints/sprint-004.md` declares `sprint_id: sprint-004`, `plan_revision: 7`, and an `updated_at` timestamp; it is active and linked in `active.md`
- `production/sprint-status.yaml` contains matching `active_sprint_id`, `sprint_id`, `plan_revision`, recomputed `story_set_hash`, and a non-older `updated_at`
- Sprint contains 6 stories:
  - 3 with `Status: Complete`
  - 2 with `Status: In Progress`
  - 1 with `Status: Blocked` (blocker: "Waiting on physics ADR acceptance")
- Sprint end date is 2 days away

**Input:** `$sprint-status`

**Expected behavior:**
1. Skill reads tracker and session selector inputs, chooses tracker `active_sprint_id` by precedence, and verifies session agreement
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

### Case 2: All Stories Complete — Sprint COMPLETE verdict

**Fixture:**
- `production/sprints/sprint-004.md` exists
- All 5 stories have `Status: Complete`

**Input:** `$sprint-status`

**Expected behavior:**
1. Skill reads sprint file — all stories are Complete
2. Skill outputs ON TRACK verdict or SPRINT COMPLETE label
3. Skill suggests running `$milestone-review` or `$sprint-plan` as next steps

**Assertions:**
- [ ] Verdict is ON TRACK or SPRINT COMPLETE when all stories are Complete
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
- One story has `Status: In Progress` with a note in `active.md`:
  `Last updated: 2026-03-30` (more than 2 days before today's session date)
- No stories are Blocked

**Input:** `$sprint-status`

**Expected behavior:**
1. Skill reads sprint file and session state
2. Skill detects the story has been In Progress for >2 days without update
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
- `production/sprints/sprint-004.md` and `production/sprint-status.yaml` satisfy the same identity/revision/hash/timestamp contract as Case 1 and contain 4 stories (2 Complete, 2 In Progress)
- `production/session-state/review-mode.txt` contains `full`

**Input:** `$sprint-status`

**Expected behavior:**
1. Skill reads sprint and produces status summary
2. Skill does NOT invoke any director gate regardless of review mode
3. Output is a plain status report with ON TRACK, AT RISK, or BLOCKED verdict
4. Skill does not prompt for user approval or ask to write any file

**Assertions:**
- [ ] No director gate is invoked in any review mode
- [ ] Remains read-only; no authorization prompt appears because the workflow does not modify files
- [ ] Skill completes and returns a verdict without user interaction
- [ ] Review mode file is ignored (or confirmed irrelevant) by this skill

---


### Case 6: SS-001 — active sprint beats newer mtime

**Fixture:**
- No sprint argument is provided
- `production/sprint-status.yaml` is absent
- `production/session-state/active.md` names only `sprint-004`
- `sprint-099.md` has a newer filesystem modification time than
  `sprint-004.md`

**Input:** `$sprint-status`

**Expected behavior:**
1. Selects sprint-004 from session state
2. Reads sprint-004 and does not inspect mtime as a selector or tie-breaker
3. Reports the selection source and exact plan path

**Assertions:**
- [ ] sprint-099 is not selected
- [ ] No "most recently modified" heuristic is used
- [ ] A missing/ambiguous active reference causes a question, not a guess
- [ ] No files are written

---

### Case 7: SS-002 — applicable tracker mismatch fails closed

Run each variant with session state selecting sprint-004 and an applicable
tracker present:

| Variant | Tracker/plan defect |
|---|---|
| 7a | tracker `sprint_id` names sprint-003 |
| 7b | tracker `plan_revision` differs from the plan |
| 7c | tracker `story_set_hash` differs from the raw current story set |
| 7d | tracker `updated_at` predates a current plan/story status update |
| 7e | one required identity/freshness field is missing or malformed |
| 7f | one story and tracker entry disagree after status normalization |

**Input:** `$sprint-status`

**Expected behavior:**
1. Names the selected sprint and selection source
2. Recomputes identity and hashes before using tracker statuses
3. Outputs `DATA CONFLICT — sprint health not assessed.`
4. Lists exact expected/observed values and one recorder recovery action
5. Stops before counts, completion, burndown, or a health verdict

**Assertions:**
- [ ] No mismatch variant silently falls back to markdown
- [ ] No tracker value overrides a current plan/story value
- [ ] DATA CONFLICT does not include ON TRACK, AT RISK, BLOCKED, or a completion percentage
- [ ] The skill does not repair or write any file

---

### Case 8: Staged dev-story success — In Review is unfinished

**Fixture:**
- Sprint, tracker, plan revision, story-set hash, and timestamps all agree
- One story records `Status: In Review`
- Its tracker status is `in_review` (repeat with legacy writer token
  `review`)
- The story records a well-formed dev-story plan hash, implementation/evidence
  post-write hashes, an executed test command with exit code 0, and a log hash
- No unresolved recovery checkpoint exists

**Input:** `$sprint-status`

**Expected behavior:**
1. Normalizes both tracker spellings to IN REVIEW
2. Validates the success evidence hashes
3. Reports the story as IN REVIEW
4. Does not include it in Complete/DONE counts

**Assertions:**
- [ ] IN REVIEW remains distinct from IN PROGRESS and DONE
- [ ] Missing plan/evidence/log hashes or a nonzero exit code yields DATA CONFLICT
- [ ] An In Review story cannot make an all-Must-Haves-complete claim
- [ ] No files are written

---

### Case 9: Staged dev-story failure checkpoint semantics

Run these variants:

| Variant | Checkpoint/status state | Expected |
|---|---|---|
| 9a | unresolved PARTIAL checkpoint; identity and all claimed current hashes match; story/tracker both In Progress | report RECOVERY CHECKPOINT with plan hash and resume point; not complete |
| 9b | unresolved checkpoint has wrong story ID, malformed hash, or a claimed current hash mismatch | DATA CONFLICT; no health verdict |
| 9c | unresolved PARTIAL/BLOCKED checkpoint while story or tracker is In Review | DATA CONFLICT; no health verdict |
| 9d | checkpoint claims fully restored FAILED state but current raw hashes do not equal all recorded baselines | DATA CONFLICT; do not claim rollback |

**Input:** `$sprint-status`

**Assertions:**
- [ ] A checkpoint is evidence, never authority to override story/tracker status
- [ ] Valid partial recovery stays In Progress
- [ ] No failed or partial checkpoint is treated as Complete
- [ ] Hash validation uses raw current bytes and exact lowercase SHA-256 values
- [ ] No files are written

---

## Protocol Compliance

- [ ] Does NOT use file-editing operations (read-only skill)
- [ ] Presents story count breakdown before emitting a verdict only after source validation
- [ ] Emits no story counts or health verdict on DATA CONFLICT
- [ ] Does not ask for approval
- [ ] Ends with a recommended next step based on verdict
- [ ] Does not pin model or reasoning settings; inherits the parent Codex session

---

## Coverage Notes

- Multiple active sprint references are fail-closed structurally but are not a separate fixture; Case 6 covers the no-mtime selection rule.
- Partial sprint completion percentages are not explicitly verified; the
  count-by-status output implies them.
- The `solo` mode review-mode variant is not separately tested; gate
  behavior in Case 5 applies to all modes equally.
