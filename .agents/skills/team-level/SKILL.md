---
name: team-level
description: "Orchestrate level design team: level-designer + narrative-director + world-builder + art-director + systems-designer + qa-tester for complete area/level creation."
---

## Invocation and execution

Invoke this workflow as `$team-level`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[level name or area to design]`. The target is required.


Before any file read, verify that a non-flag target is present. If absent,
output usage plus examples (`$team-level tutorial`, `$team-level forest dungeon`,
`$team-level final boss arena`) and stop with no verdict, authorization, or
subagent spawn.

**Decision Points:** Ask for user input only at genuine branches: the Step 1
direction choice, a Step 2 adjacent-area dependency choice, and a Step 4
blocking-accessibility revision choice. Within an accepted direction, routine
dependent steps continue without transition re-prompts.

1. **Read the argument** for the target level or area (e.g., `tutorial`,
   `forest dungeon`, `hub town`, `final boss arena`).

2. **Gather context**:
   - Read the game concept at `design/gdd/game-concept.md`
   - Read game pillars at `design/gdd/game-pillars.md`
   - Read existing level docs in `design/levels/`
   - Read relevant narrative docs in `design/narrative/`
   - Read world-building docs for the area's region/faction

## How to Delegate

Use the Codex subagent delegation to spawn each team member as a subagent:
- `subagent_type: narrative-director` — Narrative purpose, characters, emotional arc
- `subagent_type: world-builder` — Lore context, environmental storytelling, world rules
- `subagent_type: level-designer` — Spatial layout, pacing, encounters, navigation
- `subagent_type: systems-designer` — Enemy compositions, loot tables, difficulty balance
- `subagent_type: art-director` — Visual theme, color palette, lighting, asset requirements
- `subagent_type: accessibility-specialist` — Navigation clarity, colorblind safety, cognitive load
- `subagent_type: qa-tester` — Test cases, boundary testing, playtest checklist

Always provide full context in each agent's prompt (game concept, pillars, existing level docs, narrative docs).

3. **Orchestrate the level design team** in sequence:

Steps 1–5 are analysis-only: every professional subagent returns content in
conversation and must not create or edit a level, narrative, or test-checklist
file. The outputs will be compiled into one final level document.

### Step 1: Narrative + Visual Direction (narrative-director + world-builder + art-director, parallel)

Spawn all three agents simultaneously — issue all three subagent delegations before waiting for any result.

Spawn the `narrative-director` agent to:
- Define the narrative purpose of this area (what story beats happen here?)
- Identify key characters, dialogue triggers, and lore elements
- Specify emotional arc (how should the player feel entering, during, leaving?)

Spawn the `world-builder` agent to:
- Provide lore context for the area (history, faction presence, ecology)
- Define environmental storytelling opportunities
- Specify any world rules that affect gameplay in this area

Spawn the `art-director` agent to:
- Establish visual theme targets for this area — these are INPUTS to layout, not outputs of it
- Define the color temperature and lighting mood for this area (how does it differ from adjacent areas?)
- Specify shape language direction (angular fortress? organic cave? decayed grandeur?)
- Name the primary visual landmarks that will orient the player
- Read `design/art/art-bible.md` if it exists — anchor all direction in the established art bible

**The art-director's visual targets from Step 1 must be passed to the level-designer in Step 2** as explicit constraints. Layout decisions happen within the visual direction, not before it.

**Direction decision**: Present the three Step 1 outputs together. Ask only
when they offer materially different narrative/visual directions; record the
selected direction before Step 2. If no meaningful alternative exists, continue.

### Step 2: Layout and Encounter Design (level-designer)
Spawn the `level-designer` agent with the full Step 1 output as context:
- Narrative brief (from narrative-director)
- Lore foundation (from world-builder)
- **Visual direction targets (from art-director)** — layout must work within these targets, not contradict them

The level-designer should:
- Design the spatial layout (critical path, optional paths, secrets) — ensuring primary routes align with the visual landmark targets from Step 1
- Define pacing curve (tension peaks, rest areas, exploration zones) — coordinated with the emotional arc from narrative-director
- Place encounters with difficulty progression
- Design environmental puzzles or navigation challenges
- Define points of interest and landmarks for wayfinding — these must match the visual landmarks the art-director specified
- Specify entry/exit points and connections to adjacent areas

**Adjacent area dependency check**: After the layout is produced, check `design/levels/` for each adjacent area referenced by the level-designer. If any referenced area's `.md` file does not exist, surface the gap:
> "Level references [area-name] as an adjacent area but `design/levels/[area-name].md` does not exist."

Ask the user directly with options:
- (a) Proceed with a placeholder reference — mark the connection as UNRESOLVED in the level doc and list it in the open cross-level dependencies section of the summary report
- (b) Pause and run `$team-level [area-name]` first to establish that area

Do NOT invent content for the missing adjacent area.

After resolving any adjacent-area dependency choice, continue to Step 3 without
a routine transition approval.

### Step 3: Systems Integration (systems-designer)
Spawn the `systems-designer` agent to:
- Specify enemy compositions and encounter formulas
- Define loot tables and reward placement
- Balance difficulty relative to expected player level/gear
- Design any area-specific mechanics or environmental hazards
- Specify resource distribution (health pickups, save points, shops)

Present Step 3 results in conversation and continue to Step 4 within the
accepted direction; do not add a routine transition approval.

### Step 4: Production Concepts + Accessibility (art-director + accessibility-specialist, parallel)

**Note**: The art-director's directional pass (visual theme, color targets, mood) happened in Step 1. This pass is location-specific production concepts — given the finalized layout, what does each specific space look like?

Spawn the `art-director` agent with the finalized layout from Step 2:
- Produce location-specific concept specs for key spaces (entrance, key encounter zones, landmarks, exits)
- Specify which art assets are unique to this area vs. shared from the global pool
- Define sight-line and lighting setups per key space (these are now layout-informed, not directional)
- Specify VFX needs that are specific to this area's layout (weather volumes, particles, atmospheric effects)
- Flag any locations where the layout creates visual direction conflicts with the Step 1 targets — surface these as production risks

Spawn the `accessibility-specialist` agent in parallel to:
- Review the level layout for navigation clarity (can players orient themselves without relying on color alone?)
- Check that critical path signposting uses shape/icon/sound cues in addition to color
- Review any puzzle mechanics for cognitive load — flag anything that requires holding more than 3 simultaneous states
- Check that key gameplay areas have sufficient contrast for colorblind players
- Output: accessibility concerns list with severity (BLOCKING / RECOMMENDED / NICE TO HAVE)

Wait for both agents to return before proceeding.

Present both Step 4 results. If the accessibility-specialist returned a BLOCKING
concern, the only completion path is to return to level-designer and art-director,
revise the flagged elements, and have accessibility-specialist re-check them as
non-blocking. The user may stop, but cannot accept/document a blocker as complete.
Do not enter Step 5 or permit COMPLETE while a BLOCKING concern remains.
RECOMMENDED and NICE TO HAVE concerns may be recorded without blocking.

### Step 5: QA Planning (qa-tester)
Spawn the `qa-tester` agent to:
- Write test cases for the critical path
- Identify boundary and edge cases (sequence breaks, softlocks)
- Create a playtest checklist for the area
- Define acceptance criteria for level completion

4. **Compile the level design document** combining all team outputs into the
   level design template format.

After all analysis outputs are collected and no accessibility blocker remains,
present one changeset containing the exact final path
`design/levels/[level-name-slug].md` and the intended compiled sections. Obtain
one authorization, then spawn `level-designer` as the sole writer:
- Pass all subagent outputs, the level brief, game pillars, and relevant GDD sections
- Compile Step 5 test cases/checklist and narrative/world/art material into the
  one level document; do not create separate narrative or test-checklist files
- Write only the approved final path and request no separate approval
- The orchestrator does not write files directly

5. **Save to** `design/levels/[level-name-slug].md` (handled only by the
level-designer after authorization).

6. **Output a summary** with: area overview, encounter count, estimated asset
   list, narrative beats, any cross-team dependencies or open questions, open
   cross-level dependencies (adjacent areas referenced but not yet designed, each
   marked UNRESOLVED), and accessibility concerns with their resolution status.

## File Write Protocol

Steps 1–5 perform no writes. The current workflow has one concrete output, the
final level document. After all content and its exact slugged path are known,
the orchestrator obtains one changeset authorization and delegates that single
file to level-designer. Narrative content and QA checklists are sections of the
final document, not independent files. The orchestrator does not write directly.

Verdict: **COMPLETE** — level design document produced and all team outputs compiled.
Verdict: **BLOCKED** — one or more agents blocked; partial report produced with unresolved items listed.

## Next Steps

- Run `$dev-story` to implement level content once the design is approved.
- Run `$qa-plan` to generate a QA test plan for this level.

## Error Recovery Protocol

If any spawned agent (through Codex subagent delegation) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** by asking the user directly with choices:
   - Skip this agent and note the gap in the partial report (not available for a
     BLOCKING accessibility finding)
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Common blockers:
- Input file missing (story not found, GDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `$architecture-decision` first
- Scope too large → split into two stories via `$create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess
