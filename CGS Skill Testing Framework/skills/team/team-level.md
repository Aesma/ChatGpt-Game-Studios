# Skill Test Spec: $team-level

## Skill Summary

Orchestrates the full level design team for a single level or area. Coordinates
narrative-director, world-builder, level-designer, systems-designer, art-director,
accessibility-specialist, and qa-tester through five sequential steps with one
parallel phase (Step 4). Compiles all team outputs into a single level design
document saved to `design/levels/[level-name].md`. It uses user input for genuine
design choices or blockers, not routine step transitions. The full output file set is
authorized once as a bounded changeset, then writes are delegated to subagents. Produces a summary report
with verdict COMPLETE / BLOCKED and handoffs to `$dev-story` and `$qa-plan`.

---

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase/step headings (Step 1 through Step 5 are all present)
- [ ] Contains verdict keywords: COMPLETE, BLOCKED
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
8. Summary report: area overview, encounter count, estimated asset list, narrative beats, cross-team dependencies, verdict: COMPLETE
9. Next steps list `$dev-story` and `$qa-plan`; no incompatible `$design-review` call is made

**Assertions:**
- [ ] All five sources read during context gathering before any agent is spawned
- [ ] narrative-director and world-builder both spawned in Step 1 (may be sequential or parallel — both must complete before Step 2)
- [ ] Routine phase transitions proceed without repeated approval; user input is reserved for consequential choices or blockers
- [ ] Step 4 agents (art-director, accessibility-specialist) launched simultaneously
- [ ] All file writes delegated to sub-agents — orchestrator does not write directly
- [ ] Level doc saved to `design/levels/forest-dungeon.md` (slugified from argument)
- [ ] Verdict COMPLETE in final summary report
- [ ] Next steps include `$dev-story` and `$qa-plan`, not `$design-review`
- [ ] Arguments expose no `--review`; every listed core role remains part of the pipeline
- [ ] Summary report includes: area overview, encounter count, estimated asset list, narrative beats

---

### Case 2: Blocked Agent (world-builder) — Partial report produced with gap noted

**Fixture:**
- `design/gdd/game-concept.md` exists
- World-building docs for the forest region do NOT exist
- world-builder agent returns BLOCKED: "No world-building docs found for the forest region — cannot provide lore context"

**Input:** `$team-level forest dungeon`

**Expected behavior:**
1. Context gathering completes; missing world-building docs noted
2. Step 1 — narrative-director completes successfully; world-builder spawned and returns BLOCKED
3. Error Recovery Protocol triggered: "world-builder: BLOCKED — no world-building docs for forest region"
4. `user-input request` presented with options:
   - (a) Skip world-builder and note the lore gap in the level doc
   - (b) Retry with narrower scope (world-builder focuses only on what can be inferred from game-concept.md)
   - (c) Stop here and create world-building docs first
5. If user chooses (a): pipeline continues with Steps 2–5 using narrative-director context only; level doc compiled with a clearly marked gap section: "World-building context: NOT PROVIDED — see open dependency"
6. Final report produced: partial outputs documented, world-builder section marked BLOCKED, overall verdict: BLOCKED

**Assertions:**
- [ ] BLOCKED surface message appears immediately when world-builder fails — before Step 2 begins without user input
- [ ] `user-input request` offers at minimum three options (skip / retry / stop)
- [ ] Partial report produced — narrative-director's completed work is not discarded
- [ ] Level doc (if compiled) contains an explicit gap notation for the missing world-building context
- [ ] Overall verdict is BLOCKED (not COMPLETE) when world-builder remains unresolved
- [ ] Skill does NOT silently fabricate lore content to fill the gap

---

### Case 3: No Argument — Usage guidance shown

**Fixture:**
- Any project state

**Input:** `$team-level` (no argument)

**Expected behavior:**
1. Skill detects no argument provided
2. Outputs usage message explaining the required argument (level name or area to design)
3. Provides example invocations: `$team-level tutorial`, `$team-level forest dungeon`, `$team-level final boss arena`
4. Skill exits without reading any project files or spawning any subagents

**Assertions:**
- [ ] Skill does NOT spawn any subagents when no argument is given
- [ ] Usage message includes the argument format documented in the skill body
- [ ] At least one example of a valid invocation is shown
- [ ] No GDD or level files read before failing
- [ ] Verdict is NOT shown (pipeline never starts)

---

### Case 4: Accessibility Review Gate — Blocking concern surfaces before sign-off

**Fixture:**
- Steps 1–3 complete successfully
- `design/accessibility-requirements.md` committed tier: Enhanced
- accessibility-specialist (Step 4, parallel) flags a BLOCKING concern: the critical path through the forest dungeon requires players to distinguish between two environmental hazards (toxic pools vs. shallow water) using color alone — no shape, icon, or audio cue differentiates them

**Input:** `$team-level forest dungeon`

**Expected behavior:**
1. Steps 1–3 complete; Step 4 parallel phase begins
2. accessibility-specialist returns: BLOCKING concern — "Critical path hazard distinction relies on color only (toxic pools vs. shallow water). Shape, icon, or audio cue required per Enhanced accessibility tier."
3. art-director returns Step 4 output (complete)
4. Skill presents both Step 4 results via `user-input request` — BLOCKING concern highlighted prominently
5. The only completion option is return to level-designer + art-director to redesign before Step 5; the user may also stop
6. Skill does NOT proceed past the BLOCKING concern
7. After revision, accessibility-specialist re-runs the check and must clear/downgrade it before Step 5
8. Final report includes the concern and resolution status

**Assertions:**
- [ ] BLOCKING accessibility concern is not treated as advisory — it is surfaced as a blocker
- [ ] `user-input request` presents the specific concern text (not just "accessibility issue found")
- [ ] Step 5 does NOT begin while the BLOCKING concern remains
- [ ] Revision path offered: level-designer + art-director can be sent back before proceeding
- [ ] Final report includes the accessibility concern and its resolution status
- [ ] art-director's completed output is NOT discarded when accessibility-specialist blocks
- [ ] User acceptance/documentation cannot convert an unresolved blocker into COMPLETE

---

### Case 5: Circular Level Reference — Adjacent area dependency flagged

**Fixture:**
- Steps 1–3 in progress
- level-designer (Step 2) produces a layout that specifies entry/exit points connecting to "the crystal caves" (an adjacent area)
- `design/levels/crystal-caves.md` does NOT exist — the crystal caves area has not been designed yet

**Input:** `$team-level forest dungeon`

**Expected behavior:**
1. Step 2 — level-designer produces layout including: "West exit connects to crystal-caves entry point A"
2. Orchestrator (or level-designer subagent) checks `design/levels/` for `crystal-caves.md`; file not found
3. Dependency gap surfaced: "Level references crystal-caves as an adjacent area but `design/levels/crystal-caves.md` does not exist"
4. `user-input request` presented with options:
   - (a) Proceed with a placeholder reference — note the dependency in the level doc as UNRESOLVED
   - (b) Pause and run `$team-level crystal caves` first to establish that area
5. Skill does NOT invent crystal caves content to satisfy the reference
6. If user chooses (a): level doc compiled with the west exit marked "→ crystal-caves (UNRESOLVED — area not yet designed)"; flagged in the open dependencies section of the summary report
7. Final report includes open cross-level dependencies section

**Assertions:**
- [ ] Skill detects the missing adjacent area by checking `design/levels/` — does not assume it will be created later
- [ ] Skill does NOT fabricate crystal caves content (lore, layout, connections) to resolve the reference
- [ ] `user-input request` offers a "design crystal caves first" option referencing `$team-level`
- [ ] If user proceeds with placeholder, level doc explicitly marks the west exit as UNRESOLVED
- [ ] Summary report includes an open cross-level dependencies section listing unresolved references
- [ ] Circular or forward references do not cause the skill to loop or crash

---

## Protocol Compliance

- [ ] Uses one bounded changeset authorization for the complete output set; does not re-prompt at each phase transition
- [ ] All file writes delegated to sub-agents through Codex subagent delegation — orchestrator does not call Write or Edit directly
- [ ] Error Recovery Protocol followed: surface → assess → offer options → partial report
- [ ] Step 4 agents (art-director, accessibility-specialist) launched in parallel per skill spec
- [ ] Partial report always produced even when agents are BLOCKED
- [ ] Accessibility BLOCKING concerns surface before sign-off and require explicit user acknowledgment
- [ ] Verdict is one of COMPLETE / BLOCKED
- [ ] Next steps present at end: `$dev-story`, `$qa-plan`
- [ ] Missing target stops before all reads, spawns, authorization, and verdict output
- [ ] Core roles are not conditional on a review mode
- [ ] Steps 1–5 are analysis-only; routine transitions do not repeatedly ask approval
- [ ] The only written output is the exact slugged final level document
- [ ] level-designer is its sole writer after one complete changeset authorization
- [ ] Narrative and QA checklist content are embedded sections, not independent files
- [ ] A BLOCKING accessibility concern requires revision and re-check before Step 5/COMPLETE

---

## Coverage Notes

- narrative-director and world-builder in Step 1 may be sequential or parallel — the skill spec
  spawns both but does not mandate simultaneous launch; coverage of parallel Step 1 would require
  an explicit timing assertion fixture.
- The "Retry with narrower scope" option in the blocked world-builder case (Case 2) — the
  retry behavior itself is not tested in depth; its full path is analogous to the blocked agent
  pattern covered in Case 2 and in other team-* specs.
- systems-designer (Step 3) block scenarios are not separately tested; the same Error Recovery
  Protocol applies and the pattern is validated by Case 2.
- Step 4 parallel ordering (art-director completing before or after accessibility-specialist)
  does not affect outcomes — both must return before Step 5 regardless of order.
- The level doc slug convention (argument → filename) is implicitly tested by Case 1
  (`forest dungeon` → `forest-dungeon.md`); multi-word slugification edge cases (special
  characters, very long names) are not covered.
