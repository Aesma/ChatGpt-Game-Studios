# Skill Test Spec: $create-epics

## Skill Summary

`$create-epics` reads all approved GDDs and translates them into EPIC.md files,
one per system. Epics are organized by layer (Foundation → Core → Feature →
Presentation) and processed in priority order within each layer. Each EPIC.md
includes scope, governing ADRs, GDD requirements, engine risk level, and a
Definition of Done. The skill asks "May I apply the proposed changeset?"
5. After approval: writes both EPIC files
6. Creates or updates `production/epics/index.md`

**Assertions:**
- [ ] Epic summary is shown before any write ask
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
3. For the second system (no existing file): proceeds normally with "changeset authorization"

**Assertions:**
- [ ] Skill detects existing EPIC files before applying a not-yet-authorized changeset
- [ ] User is offered "update" or "skip" options — not auto-overwritten
- [ ] The new system's EPIC is created normally without conflict

---

### Case 5: Director Gate — PR-EPIC returns CONCERNS

**Fixture:**
- 2 approved GDDs exist
- `production/session-state/review-mode.txt` contains `full`
- PR-EPIC gate returns CONCERNS (e.g., scope of one epic is too large)

**Input:** `$create-epics`

**Expected behavior:**
1. PR-EPIC gate spawns and returns CONCERNS with specific feedback
2. Skill surfaces the concerns to the user before any write ask
3. User is given options: revise epics, accept concerns and proceed, or stop
4. If user revises: updated epic drafts are shown before the "changeset authorization" ask
5. Skill does NOT write epics while CONCERNS are unaddressed

**Assertions:**
- [ ] CONCERNS from PR-EPIC are shown to the user before applying a not-yet-authorized changeset
- [ ] Skill does NOT auto-write epics when CONCERNS are returned
- [ ] User is given a clear choice to revise, proceed, or stop
- [ ] Revised epic drafts are re-shown after revision before final approval

---

## Protocol Compliance

- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] PR-EPIC gate (if active) runs before write asks — not after
- [ ] Skipped gates noted by name and mode in output
- [ ] EPIC.md content sourced only from GDDs, ADRs, and architecture docs — nothing invented
- [ ] Ends with next-step handoff: `$create-stories [epic-slug]` per created epic

---

## Coverage Notes

- Processing of Core, Feature, and Presentation layers follows the same per-epic
  pattern as Foundation — layer-specific ordering is not independently tested.
- Engine risk level assignment (LOW/MEDIUM/HIGH) from governing ADRs is
  validated implicitly via Case 1's fixture structure.
- The `layer: [name]` and `[system-name]` argument modes follow the same approval
  pattern as the default (all systems) mode.
