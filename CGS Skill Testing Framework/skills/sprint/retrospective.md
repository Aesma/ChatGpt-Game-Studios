# Skill Test Spec: $retrospective

## Skill Summary

`$retrospective` generates a structured sprint or milestone retrospective
covering three categories: what went well, what didn't, and action items.
It reads sprint files and session logs to compile observations, then produces
a retrospective document. No director gates are used — retrospectives are
team self-reflection artifacts. The skill asks "May I apply the proposed changeset?" before persisting.
Verdict is always COMPLETE (retrospective is structured output, not a pass/fail
assessment).

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keyword: COMPLETE
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
5. User approves; file is written; verdict COMPLETE

**Assertions:**
- [ ] Retrospective contains all three categories (went well / didn't / actions)
- [ ] Blocked and deferred stories appear in the "what didn't" section
- [ ] At least one action item is generated from the blocked story
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
5. File is overwritten; verdict COMPLETE

**Assertions:**
- [ ] Skill checks for existing retrospective file before compiling
- [ ] User is offered append or replace choice — not silently overwritten
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Verdict is COMPLETE after write regardless of append vs. replace

---

### Case 4: Edge Case — Unresolved action items from previous retrospective

**Fixture:**
- `production/retrospectives/retro-sprint-004.md` exists with 2 action items marked `[ ]` (not done)
- User runs `$retrospective sprint-005`

**Input:** `$retrospective sprint-005`

**Expected behavior:**
1. Skill reads the most recent prior retrospective (retro-sprint-004)
2. Skill detects 2 unchecked action items from sprint-004
3. Skill includes a "Carry-over from Sprint 004" section in the new retrospective
4. The unresolved items are listed with a note that they were not followed up

**Assertions:**
- [ ] Skill reads the most recent prior retrospective to check for open action items
- [ ] Unresolved action items appear in the new retrospective under a carry-over section
- [ ] Carry-over items are distinct from newly generated action items
- [ ] Output notes that these items were not followed up in the previous sprint

---

### Case 5: Gate Compliance — No gate invoked in any mode

**Fixture:**
- `production/sprints/sprint-005.md` exists with complete stories
- `production/session-state/review-mode.txt` contains `full`

**Input:** `$retrospective sprint-005`

**Expected behavior:**
1. Skill compiles retrospective in full mode
2. No director gate is invoked (retrospectives are team self-reflection, not delivery gates)
3. Skill asks user for approval and writes file on confirmation
4. Verdict is COMPLETE

**Assertions:**
- [ ] No director gate is invoked regardless of review mode
- [ ] Output does not contain any gate invocation or gate result notation
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Review mode file content is irrelevant to this skill's behavior

---

## Protocol Compliance

- [ ] Always shows retrospective draft before asking to write
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] No director gates are invoked
- [ ] Verdict is always COMPLETE (not a pass/fail skill)
- [ ] Checks prior retrospective for unresolved action items

---

## Coverage Notes

- Milestone retrospectives (as opposed to sprint retrospectives) follow the
  same pattern but read milestone files instead of sprint files; not
  separately tested here.
- The case where session logs are empty is similar to Case 2 (no data);
  the skill falls back to manual input in both situations.

## P0 Contract Coverage

- [ ] A sprint-status file contributes metrics only when its identifier matches
  the requested sprint; milestone retrospectives use only explicitly included
  sprints/goals.
- [ ] Missing actual effort, bug counts, estimation inputs, or prior velocity
  are written as `N/A — source unavailable` and are not inferred from commits.
- [ ] Start-fresh lists the archive source, archive target, and new retrospective
  in one changeset and rechecks the baseline before moving anything.
- [ ] Completion provides `$sprint-plan` / `$gate-check` only as later handoff
  commands and never invokes either workflow automatically.

## P1 Contract Coverage

- [ ] Missing arguments list sprint/milestone candidates; unknown, ambiguous,
  missing, or empty targets stop or use explicitly supplied user data.
- [ ] Git metrics use the target's explicit period; no recent-20 fallback exists.
- [ ] TODO/FIXME/HACK trends compare the same directories/exclusions; otherwise
  only the current count is reported.
- [ ] Missing velocity periods show N/A, and a trend requires at least two
  comparable periods.
- [ ] Artifact-backed observations, user reflections, and unknown causes are
  labeled separately.
- [ ] Missing action owners/deadlines remain Unassigned/Not set, and the draft
  commitments are confirmed before save.
