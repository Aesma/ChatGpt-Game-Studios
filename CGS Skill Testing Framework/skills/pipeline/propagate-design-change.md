# Skill Test Spec: $propagate-design-change

## Skill Summary

`$propagate-design-change` handles GDD revision cascades. When a GDD is updated,
the skill traces all downstream artifacts that reference it: ADRs, TR-registry
entries, stories, and epics. It produces a structured impact report showing what
needs to change and why. The skill does not automatically apply changes. It treats
the complete described file set as one bounded changeset: use existing task
authorization, or preview and confirm it once before the first write.

**Assertions:**
- [ ] Impact report identifies all 3 affected artifacts (1 epic + 2 stories)
- [ ] Each affected artifact's proposed change is shown before asking to write
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Skill does not apply changes outside the authorized bounded changeset
- [ ] Verdict is COMPLETE after all approved changes are applied

---

### Case 2: No Impact — Changed GDD has no downstream references

**Fixture:**
- `design/gdd/[system].md` exists and has been revised
- No ADRs, stories, or epics reference this GDD's TR-IDs or GDD path

**Input:** `$propagate-design-change design/gdd/[system].md`

**Expected behavior:**
1. Skill reads the revised GDD
2. Skill scans all ADRs, stories, and epics for references
3. No references found
4. Skill outputs: "No downstream impact found for [system].md — no artifacts reference this GDD."
5. No write operations are performed

**Assertions:**
- [ ] Skill outputs the "No downstream impact found" message
- [ ] Verdict is NO IMPACT
- [ ] Remains read-only; no authorization prompt appears because the workflow does not modify files
- [ ] Skill does NOT error or crash when no references are found

---

### Case 3: In-Progress Story Warning — Referenced story is currently being developed

**Fixture:**
- A story referencing this GDD has `Status: In Progress`
- The developer has already started implementing this story

**Input:** `$propagate-design-change design/gdd/[system].md`

**Expected behavior:**
1. Skill identifies the In Progress story as an affected artifact
2. Skill outputs an elevated warning: "CAUTION: [story-file] is currently In Progress — a developer may be working on this. Coordinate before updating."
3. The warning appears in the impact report before the "changeset authorization" ask for that story
4. User can still approve or skip the update for that story

**Assertions:**
- [ ] In Progress story is flagged with an elevated warning (distinct from regular affected-artifact entries)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Skill still offers to update the story — the warning does not block the option
- [ ] Other (non-In-Progress) artifacts are not affected by this warning

---

### Case 4: Edge Case — No argument provided

**Fixture:**
- Multiple GDDs exist in `design/gdd/`

**Input:** `$propagate-design-change` (no argument)

**Expected behavior:**
1. Skill detects no argument is provided
2. Skill outputs a usage error: "No GDD specified. Usage: $propagate-design-change design/gdd/[system].md"
3. Skill lists recently modified GDDs as suggestions (git log)
4. No analysis is performed

**Assertions:**
- [ ] Skill outputs a usage error when no argument is given
- [ ] Usage example is shown with the correct path format
- [ ] No impact analysis is performed without a target GDD
- [ ] Skill does NOT silently pick a GDD without user input

---

### Case 5: Director Gate — No gate spawned regardless of review mode

**Fixture:**
- A GDD has been revised with downstream references
- `production/session-state/review-mode.txt` exists with `full`

**Input:** `$propagate-design-change design/gdd/[system].md`

**Expected behavior:**
1. Skill reads the GDD and traces downstream references
2. Skill does NOT read `production/session-state/review-mode.txt`
3. No director gate agents are spawned at any point
4. Impact report is produced and the complete artifact batch is authorized once

**Assertions:**
- [ ] No director gate agents are spawned (no CD-, TD-, PR-, AD- prefixed gates)
- [ ] Skill does NOT read `production/session-state/review-mode.txt`
- [ ] Output contains no "Gate: [GATE-ID]" or gate-skipped entries
- [ ] Review mode has no effect on this skill's behavior

---

## Protocol Compliance

- [ ] Reads revised GDD and all potentially affected artifacts before producing impact report
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] In Progress stories flagged with elevated warning before their approval ask
- [ ] No director gates — no review-mode.txt read
- [ ] Ends with next-step handoff appropriate to verdict (COMPLETE or NO IMPACT)

---

## Coverage Notes

- ADR impact (when a GDD change requires an ADR update or new ADR) follows the
  same bounded batch-authorization pattern as story/epic updates — not independently
  fixture-tested.
- TR-registry impact (when changed GDD requires new or updated TR-IDs) is part
  of the analysis phase but not independently fixture-tested.
- The git diff comparison method (detecting what changed in the GDD) is a runtime
  concern — fixtures use pre-arranged content differences.
