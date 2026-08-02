# Skill Test Spec: $team-ui

## Skill Summary

Orchestrates the UI team through the full UX pipeline for a single UI feature.
Coordinates ux-designer, ui-programmer, art-director, the engine UI specialist,
and accessibility-specialist through five structured phases: Context Gathering +
UX Spec (Phase 1a/1b) → UX Review Gate (Phase 1c) → Visual Design (Phase 2) →
Implementation (Phase 3) → Review in parallel (Phase 4) → Polish (Phase 5).
Uses `user-input request` at each phase transition. Delegates all file writes to
sub-agents and sub-skills (`$ux-design`, `ui-programmer`). Produces a summary report
with verdict COMPLETE / BLOCKED and handoffs to `$ux-review`, `$code-review`,
`$team-polish`.

---

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings (Phase 1a through Phase 5 are all present)
- [ ] Contains verdict keywords: COMPLETE, BLOCKED
- [ ] Remains read-only; no authorization prompt appears because the workflow does not modify files
- [ ] Has a next-step handoff at the end (references `$ux-review`, `$code-review`, `$team-polish`)
- [ ] Error Recovery Protocol section is present with all four recovery steps
- [ ] Uses `user-input request` at phase transitions for user approval before proceeding
- [ ] Phase 4 is explicitly marked as parallel (ux-designer, art-director, accessibility-specialist)
- [ ] UX Review Gate (Phase 1c) is defined as a blocking gate — skill must not proceed to Phase 2 without APPROVED verdict
- [ ] Team Composition lists all five roles (ux-designer, ui-programmer, art-director, engine UI specialist, accessibility-specialist)
- [ ] References the interaction pattern library (`design/ux/interaction-patterns.md`) — ui-programmer must use existing patterns
- [ ] Phase 1a reads `design/accessibility-requirements.md` before design begins

---

## Test Cases

### Case 1: Happy Path — Full pipeline from UX spec through polish succeeds

**Fixture:**
- `design/gdd/game-concept.md` exists with platform targets and intended audience
- `design/player-journey.md` exists
- `design/ux/interaction-patterns.md` exists with relevant patterns
- `design/accessibility-requirements.md` exists with a committed tier (Basic, Standard, Comprehensive, or Exemplary)
- Engine UI specialist configured in `docs/technical-preferences.md`

**Input:** `$team-ui inventory screen`

**Expected behavior:**
1. Phase 1a — orchestrator reads game-concept.md, player-journey.md, relevant GDD UI sections, interaction-patterns.md, accessibility-requirements.md; summarizes a brief for the ux-designer
2. Phase 1b — `$ux-design inventory-screen` invoked (or ux-designer spawned directly); produces `design/ux/inventory-screen.md` using `ux-spec.md` template; `user-input request` confirms spec before review
3. Phase 1c — `$ux-review design/ux/inventory-screen.md` invoked; returns APPROVED; gate passed, proceed to Phase 2
4. Phase 2 — art-director spawned; reviews full UX spec (not only wireframes); applies visual treatment; verifies color contrast; produces visual design spec with asset manifest; `user-input request` confirms before Phase 3
5. Phase 3 — engine UI specialist is spawned first; implementation starts only with a configured engine and an APPROVED spec. Patterns are user-approved and persisted before first review, not created during implementation
6. Phase 4 — ux-designer, art-director, accessibility-specialist spawned in parallel; all three return results before Phase 5
7. Phase 5 — each finding is fixed by the path owner and targeted re-checked by the reviewer who raised it; only then is verdict COMPLETE
8. Summary report: UX spec APPROVED, visual design COMPLETE, implementation COMPLETE, accessibility COMPLIANT, all input methods supported, pattern library updated, verdict: COMPLETE

**Assertions:**
- [ ] Phase 1a reads all five sources before briefing ux-designer
- [ ] UX Review Gate checked before Phase 2 — Phase 2 does NOT begin until APPROVED
- [ ] Art-director in Phase 2 reviews full spec, not just wireframe images
- [ ] Engine UI specialist spawned before ui-programmer in Phase 3
- [ ] Phase 4 agents launched simultaneously (ux-designer, art-director, accessibility-specialist)
- [ ] All file writes delegated to sub-agents and sub-skills
- [ ] Verdict COMPLETE in final summary report
- [ ] Next steps include `$ux-review`, `$code-review`, `$team-polish`

---

### Case 2: UX Review Gate — Spec fails review; skill halts before implementation

**Fixture:**
- `design/ux/inventory-screen.md` produced by Phase 1b
- `$ux-review` returns verdict NEEDS REVISION with specific concerns flagged (e.g., gamepad navigation flow incomplete, contrast ratio below minimum)

**Input:** `$team-ui inventory screen`

**Expected behavior:**
1. Phase 1a + 1b complete — UX spec produced
2. Phase 1c — `$ux-review design/ux/inventory-screen.md` returns NEEDS REVISION
3. Skill does NOT advance to Phase 2
4. `user-input request` presented with the specific flagged concerns and options:
   - (a) Return to ux-designer to address the issues and re-review
   - (b) Stop this workflow and make a separate product decision; the verdict remains NEEDS REVISION
5. If user chooses (a): ux-designer revises spec, `$ux-review` re-run; loop continues until APPROVED or user overrides
6. If user chooses (b), the workflow stops without implementation or COMPLETE
7. Skill does NOT silently proceed past the gate

**Assertions:**
- [ ] Phase 2 does NOT begin while UX review verdict is NEEDS REVISION
- [ ] `user-input request` presents the specific flagged concerns before offering options
- [ ] User must make a conscious choice to override — skill does not assume override
- [ ] NEEDS REVISION/MAJOR is never treated as implementation-ready or COMPLETE
- [ ] Revision-and-re-review loop is offered (not just a one-shot failure)
- [ ] Skill does NOT discard the produced UX spec on review failure

---

### Case 3: No Argument — Usage guidance shown

**Fixture:**
- Any project state

**Input:** `$team-ui` (no argument)

**Expected behavior:**
1. Skill detects no argument provided
2. Outputs usage message explaining the required argument (UI feature description)
3. Provides an example invocation: `$team-ui [UI feature description]`
4. Skill exits without spawning any subagents or reading any project files

**Assertions:**
- [ ] Skill does NOT spawn any subagents when no argument is given
- [ ] Usage message includes the argument format documented in the skill body
- [ ] At least one example of a valid invocation is shown
- [ ] No UX spec files or GDDs read before failing
- [ ] Verdict is NOT shown (pipeline never starts)

---

### Case 4: Accessibility Parallel Review — Phase 4 runs three streams simultaneously

**Fixture:**
- `design/ux/inventory-screen.md` exists (APPROVED)
- Visual design spec complete
- Implementation complete
- `design/accessibility-requirements.md` committed tier: Standard

**Input:** `$team-ui inventory screen` (resuming from Phase 3 complete)

**Expected behavior:**
1. Phase 4 begins after implementation is confirmed complete
2. Three Codex subagent delegations issued simultaneously: ux-designer, art-director, accessibility-specialist
3. Each stream operates independently:
   - ux-designer: verifies implementation matches wireframes, tests keyboard-only and gamepad-only navigation, checks accessibility features function
   - art-director: verifies visual consistency with art bible at minimum and maximum supported resolutions
   - accessibility-specialist: audits against the Standard accessibility tier in `design/accessibility-requirements.md`; any violation flagged as a blocker
4. Skill waits for all three results before proceeding to Phase 5
5. `user-input request` presents all three review results before Phase 5 begins

**Assertions:**
- [ ] All three Codex subagent delegations issued before any result is awaited (parallel, not sequential)
- [ ] Phase 5 does NOT begin until all three Phase 4 agents have returned
- [ ] Accessibility-specialist explicitly reads `design/accessibility-requirements.md` for the committed tier
- [ ] Accessibility violations flagged as BLOCKING (not merely advisory)
- [ ] `user-input request` shows all three review streams' results together before Phase 5 approval
- [ ] No Phase 4 agent's output is used as input for another Phase 4 agent

---

### Case 5: Missing Interaction Pattern Library — Skill notes the gap rather than inventing patterns

**Fixture:**
- `design/ux/interaction-patterns.md` does NOT exist
- All other required files present

**Input:** `$team-ui settings menu`

**Expected behavior:**
1. Phase 1a — orchestrator attempts to read `design/ux/interaction-patterns.md`; file not found
2. Skill surfaces the gap: "interaction-patterns.md does not exist — no existing patterns to reuse"
3. `user-input request` presented with options:
   - (a) Approve the required pattern behavior and persist it through the single pattern-library writer inside Phase 1
   - (b) Leave the pattern unresolved and stop with BLOCKED/partial design output
4. Skill does NOT invent or assume patterns from other sources
5. The library edit and current spec are in the same pre-authorized changeset; the entry is written before the spec's first review
6. If approval, authorization, or persistence is missing, Phase 1c/2/3 do not run

**Assertions:**
- [ ] Skill does NOT silently ignore the missing pattern library
- [ ] Skill does NOT invent patterns by guessing from the feature name or GDD alone
- [ ] User approves behavior before the pattern-library writer persists it
- [ ] ui-programmer never backfills an authoritative pattern after implementation
- [ ] Final report documents pattern library status (created / absent / updated)
- [ ] Skill does NOT fail entirely — the gap is noted and user is given a choice

---

## Protocol Compliance

- [ ] `user-input request` used at each phase transition — user approves before pipeline advances
- [ ] UX Review Gate (Phase 1c) is blocking — Phase 2 cannot begin without APPROVED or explicit user override
- [ ] All file writes delegated to sub-agents and sub-skills — orchestrator does not call Write or Edit directly
- [ ] Phase 4 agents launched in parallel per skill spec
- [ ] Error Recovery Protocol followed: surface → assess → offer options → partial report
- [ ] Partial report always produced even when agents are BLOCKED
- [ ] Verdict is one of COMPLETE / BLOCKED
- [ ] No configured engine stops before Phase 3 and produces no engine implementation
- [ ] One Phase 1 changeset covers known spec, visual, implementation, conditional pattern-library, and session-state targets
- [ ] Every Phase 5 blocker fix receives a targeted re-check before COMPLETE
- [ ] Next steps present at end: `$ux-review`, `$code-review`, `$team-polish`

---

## Coverage Notes

### P1 Regression Matrix

- [ ] No argument exits with usage before reads/spawns/writes; unknown flags and invalid review values fail.
- [ ] `$ux-design` is the deterministic default authoring route; fallback uses the same full template/path and is identified.
- [ ] All authoring reads the exact `.codex/docs/templates/` source, not a filename-only or shortened contract.
- [ ] Accessibility tiers are only Basic/Standard/Comprehensive/Exemplary; legacy names are gaps, never guessed mappings.
- [ ] Implementation covers only configured target inputs and BLOCKS when they are unconfigured.
- [ ] Review mode cannot skip art-director's required Phase 2/4 production responsibility.
- [ ] HUD visual-budget checks run only for HUD; normal screens/flows use their own spec constraints.
- [ ] Every Phase 5 edit has one file owner and returns to its original reviewer for a targeted re-check.

- The HUD-specific path (`$ux-design hud` + `hud-design.md` template + visual budget check in Phase 5)
  is not separately tested here; it shares the same phase structure but uses different templates.
- The "Update in place" path for interaction-patterns.md (new pattern added during implementation)
  is exercised implicitly in Case 1 Step 5 — a dedicated fixture with a known new pattern would
  strengthen coverage.
- Engine UI specialist unavailable (no engine configured) — skill spec states "skip if no engine
  configured"; this path is asserted in Case 1 but not given a dedicated fixture.
- The NEEDS REVISION acceptance-risk override (Case 2 option b) requires the override to be
  explicitly documented in the report; this is asserted but not further tested for downstream effects.
