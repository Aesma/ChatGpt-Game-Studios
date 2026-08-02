---
name: map-systems
description: "Decompose a game concept into individual systems, map dependencies, prioritize design order, and create the systems index."
---

## Invocation and execution

Invoke this workflow as `$map-systems`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[next | system-name] [--review full|lean|solo]`. Treat bracketed values as optional unless the workflow says otherwise.


When this skill is invoked:

## Parse Arguments

Exactly three mutually exclusive modes:

- **No argument**: `$map-systems` — Run the decomposition workflow (Phases 1-5) to create or update the systems index.
- **`next`**: `$map-systems next` — Require one readable `design/gdd/systems-index.md`, then enter Phase 6.
- **System name**: `$map-systems [system-name]` — Require that same unique readable index and an exact system entry, then enter Phase 6.

Reject unknown flags, multiple mode arguments, and invalid `--review` values with **BLOCKED**. `next`/system-name never falls back to decomposition or invokes `$design-system` when the index is absent, duplicated, or unparseable; report the problem and suggest the existing no-argument mode.

Also resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `production/review-mode.txt` → use a valid `full|lean|solo` value;
   if its contents are invalid, report the value before falling back to `lean`
3. Else → default to `lean`

See `.codex/docs/director-gates.md` for the full check pattern.

In full mode, keep the shared trigger order: TD-SYSTEM-BOUNDARY follows approved
dependency mapping, PR-SCOPE follows approved priorities, and CD-SYSTEMS follows
the written index draft. Do not run TD/CD in parallel merely to reduce latency.

---

## Phase 1: Read Concept (Required Context)

Read the game concept and any existing design work. This provides the raw material
for systems decomposition.

**Required:**
- Read `design/gdd/game-concept.md` — **fail with a clear message if missing**:
  > "No game concept found at `design/gdd/game-concept.md`. Run `$brainstorm` first
  > to create one, then come back to decompose it into systems."

**Optional (read if they exist):**
- Read `design/gdd/game-pillars.md` — pillars constrain priority and scope
- Read `design/gdd/systems-index.md` — if exists, **resume** from where it left off
  (update, don't recreate from scratch)
- Find files matching `design/gdd/*.md` — check which system GDDs already exist

**If the systems index already exists:**
- Read it and present current status to the user
- Ask the user directly to ask:
  "The systems index already exists with [N] systems ([M] designed, [K] not started).
  What would you like to do?"
  - Options: "Update the index with new systems", "Design the next undesigned system",
    "Review and revise priorities", or cancel
  - Route **Update** to Phase 2, **Review and revise priorities** to Phase 4, and **Design next** to Phase 6. Cancel or an unrecognized answer stops without changes

---

## Phase 2: Systems Enumeration (Collaborative)

Extract and identify all systems the game needs. This is the creative core of the
skill — it requires human judgment because concept docs rarely enumerate every
system explicitly.

### Step 2a: Extract Explicit Systems

Scan the game concept for directly mentioned systems and mechanics:
- Core Mechanics section (most explicit)
- Core Loop section (implies what systems drive each loop tier)
- Technical Considerations section (networking, procedural generation, etc.)
- MVP Definition section (required features = required systems)

### Step 2b: Identify Implicit Systems

For each explicit system, identify the **hidden systems** it implies. Games always
need more systems than the concept doc mentions. Use this inference pattern:

- "Inventory" implies: item database, equipment slots, weight/capacity rules,
  inventory UI, item serialization for save/load
- "Combat" implies: damage calculation, health system, hit detection, status effects,
  enemy AI, combat UI (health bars, damage numbers), death/respawn
- "Open world" implies: streaming/chunking, LOD system, fast travel, map/minimap,
  point of interest tracking, world state persistence
- "Multiplayer" implies: networking layer, lobby/matchmaking, state synchronization,
  anti-cheat, network UI (ping, player list)
- "Crafting" implies: recipe database, ingredient gathering, crafting UI,
  success/failure mechanics, recipe discovery/learning
- "Dialogue" implies: dialogue tree system, dialogue UI, choice tracking, NPC
  state management, localization hooks
- "Progression" implies: XP system, level-up mechanics, skill tree, unlock
  tracking, progression UI, progression save data

Explain in conversation text why each implicit system is needed (with examples).

### Step 2c: User Review

Present the enumeration organized by category. For each system, show:
- Name
- Category
- Brief description (1 sentence)
- Whether it was explicit (from concept) or implicit (inferred)

Then ask the user directly to capture feedback:
- "Are there systems missing from this list?"
- "Should any of these be combined or split?"
- "Are there systems listed that this game does NOT need?"

Iterate until the user approves the enumeration.

---

## Phase 3: Dependency Mapping (Collaborative)

For each system, determine what it depends on. A system "depends on" another if
it cannot function without that other system existing first.

### Step 3a: Map Dependencies

For each system, list its dependencies. Use these dependency heuristics:
- **Input/output dependencies**: System A produces data System B needs
- **Structural dependencies**: System A provides the framework System B plugs into
- **UI dependencies**: Every gameplay system has a corresponding UI system that
  depends on it (but UI is designed after the gameplay system)

### Step 3b: Sort by Dependency Order

Arrange systems into layers:
1. **Foundation**: Systems with zero dependencies (designed and built first)
2. **Core**: Systems depending only on Foundation systems
3. **Feature**: Systems depending on Core systems
4. **Presentation**: UI and feedback systems that wrap gameplay systems
5. **Polish**: Meta-systems, tutorials, analytics, accessibility

### Step 3c: Detect Circular Dependencies

Check for cycles in the dependency graph. If found:
- Highlight them to the user
- Propose resolutions (interface abstraction, simultaneous design, breaking the
  cycle by defining a contract between the two systems)

### Step 3d: Present to User

Show the dependency map as a layered list. Highlight:
- Any circular dependencies
- Any "bottleneck" systems (many others depend on them — these are high-risk)
- Any systems with no dependents (leaf nodes — lower risk, can be designed late)

Ask the user directly to ask: "Does this dependency ordering look right? Any
dependencies I'm missing or that should be removed?"

**Review mode check** — apply before spawning TD-SYSTEM-BOUNDARY:
- `solo` → skip. Note: "TD-SYSTEM-BOUNDARY skipped — Solo mode." Proceed to priority assignment.
- `lean` → skip (not a PHASE-GATE). Note: "TD-SYSTEM-BOUNDARY skipped — Lean mode." Proceed to priority assignment.
- `full` → spawn as normal.

**After dependency mapping is approved, spawn `technical-director` through Codex subagent delegation using gate TD-SYSTEM-BOUNDARY (`.codex/docs/director-gates.md`) before proceeding to priority assignment.**

Pass: the dependency map summary, layer assignments, bottleneck systems list, any circular dependency resolutions.

Present the assessment. If the required full-mode delegation is unavailable, times out, errors, or lacks a verdict, list the failure and stop before priority/write; never simulate approval. If REJECT, revise the system boundaries with the user before moving to priority assignment. If CONCERNS, note them inline in the systems index and continue.

---

## Phase 4: Priority Assignment (Collaborative)

Assign each system to a priority tier based on what milestone it's needed for.

### Step 4a: Auto-Assign Based on Concept

Use these heuristics for initial assignment:
- **MVP**: Systems mentioned in the concept's "Required for MVP" section, plus their
  Foundation-layer dependencies
- **Vertical Slice**: Systems needed for a complete experience in one area
- **Alpha**: All remaining gameplay systems
- **Full Vision**: Polish, meta, and nice-to-have systems

### Step 4b: User Review

Present the priority assignments in a table. For each tier, explain why systems
were placed there.

Ask the user directly to ask: "Do these priority assignments match your vision?
Which systems should be higher or lower priority?"

Explain reasoning in conversation: "I placed [system] in MVP because the core loop
requires it — without [system], the 30-second loop can't function."

**"Why" column guidance**: When explaining why each system was placed in a priority tier, mix technical necessity with player-experience reasoning. Do not use purely technical justifications like "Combat needs damage math" — connect to player experience where relevant. Examples of good "Why" entries:
- "Required for the core loop — without it, placement decisions have no consequence (Pillar 2: Placement is the Puzzle)"
- "Ballista's punch-through identity is established here — this stat definition is what makes it feel different from Archer"
- "Foundation for all economy decisions — players must understand upgrade costs to make meaningful placement choices"

Pure technical necessity ("X depends on Y") is insufficient alone when the system directly shapes player experience.

**Review mode check** — apply before spawning PR-SCOPE:
- `solo` → skip. Note: "PR-SCOPE skipped — Solo mode." Proceed to writing the systems index.
- `lean` → skip (not a PHASE-GATE). Note: "PR-SCOPE skipped — Lean mode." Proceed to writing the systems index.
- `full` → spawn as normal.

**After priorities are approved, spawn `producer` through Codex subagent delegation using gate PR-SCOPE (`.codex/docs/director-gates.md`) before writing the index.**

Pass: total system count per milestone tier, available implementation-volume evidence, team size, and stated project timeline. Missing timeline/team-size/complexity data is passed explicitly as `unknown`; never manufacture `system count × average complexity`. If the missing inputs prevent a meaningful gate decision, ask the user before invoking it.

If the required full-mode producer delegation is unavailable, times out, errors, or lacks a verdict, list the failure and stop before writing; never simulate approval.

Apply the exact PR-SCOPE contract: **REALISTIC** continues; **OPTIMISTIC** shows the specific schedule/scope adjustments and asks the user to revise or explicitly accept them; **UNREALISTIC** does not write and requires scope revision or stop. Do not handle a nonexistent CONCERNS result.

### Step 4c: Determine Design Order

Combine dependency sort + priority tier to produce the final design order:
1. MVP Foundation systems first
2. MVP Core systems second
3. MVP Feature systems third
4. Vertical Slice Foundation/Core systems
5. ...and so on

This is the order the team should write GDDs in.

---

## Phase 5: Create Systems Index (Write)

### Step 5a: Draft the Document

Using the template at `.codex/docs/templates/systems-index.md`, populate the
systems index with all data from Phases 2-4:
- Fill the enumeration table
- Fill the dependency map
- Fill the recommended design order
- Fill the high-risk systems
- Fill the progress tracker. When updating an existing index, preserve every existing system's status, design-doc link, and manual notes; only genuinely new systems start as `Not Started`. A deletion or merge occurs only after the user's Phase 2 decision

### Step 5b: Approval

Present a summary of the document:
- Total systems count by category
- MVP system count
- First 3 systems in the design order
- Any high-risk items

The complete changeset preview must show both the concrete `design/gdd/systems-index.md` edit and the concrete `production/session-state/active.md` edit. Do not write either file until that combined changeset has received its one authorization. Do not pre-author a Creative Director note whose content is not yet known.

**Review mode check** — apply before spawning CD-SYSTEMS:
- `solo` → skip. Note: "CD-SYSTEMS skipped — Solo mode." Proceed to Phase 7 next steps.
- `lean` → skip (not a PHASE-GATE). Note: "CD-SYSTEMS skipped — Lean mode." Proceed to Phase 7 next steps.
- `full` → spawn as normal.

**After the systems index is written, spawn `creative-director` through Codex subagent delegation using gate CD-SYSTEMS (`.codex/docs/director-gates.md`).**

Pass: systems index path, game pillars and core fantasy (from `design/gdd/game-concept.md`), MVP priority tier system list.

If the required full-mode creative-director delegation is unavailable, times out, errors, or lacks a verdict, list the failure, retain any written index only as a draft, and stop without COMPLETE/session approval status. Never simulate approval.

Present the assessment. If REJECT, keep any already-written index only as a draft, do not update session state to created/COMPLETE, show the blocker, and stop until the user authorizes a revision and CD-SYSTEMS is run again. If CONCERNS, ask the user whether to revise or explicitly accept them. Any resulting index note or system-set change was not in the initial content preview, so show the revised same-file changeset and obtain a new authorization before writing it.

### Step 5c: Update Session State

Only after CD-SYSTEMS returns APPROVE, or the user explicitly accepts CONCERNS (and any newly previewed edit is authorized), create/update `production/session-state/active.md` with:
- Task: Systems decomposition
- Status: Systems index created
- File: design/gdd/systems-index.md
- Next: Design individual system GDDs

**Verdict: COMPLETE** — the systems index is written and the applicable CD-SYSTEMS outcome is resolved.
If the user declined, CD-SYSTEMS rejected, or a required post-gate revision was not authorized: **Verdict: BLOCKED**. Never mark the index Approved or the session COMPLETE before that point.

---

## Phase 6: Design Individual Systems (Handoff to $design-system)

This phase is entered when:
- The user says "yes" to designing systems after creating the index
- The user invokes `$map-systems [system-name]`
- The user invokes `$map-systems next`

### Step 6a: Select the System

- If a system name was provided, find it in the systems index
- If `next` was used, pick the highest-priority undesigned system (by design order)
- If the user just finished the index, ask:
  "Would you like to start designing individual systems now? The first system in
  the design order is [name]. Or would you prefer to stop here and come back later?"

Ask the user directly for: "Start designing [system-name] now, pick a different
system, or stop here?"

### Step 6b: Hand Off to $design-system

First finish `$map-systems` with its own **COMPLETE** handoff, naming the selected system but performing no further write. Only if the user then explicitly starts that separate task should `$design-system [system-name]` run under its own workflow/write boundary. Do not nest it into the already-authorized map-systems changeset.

The `$design-system` skill handles the full GDD authoring process:
- Gathers context from game concept, systems index, and dependency GDDs
- Creates a file skeleton immediately
- Walks through all 8 required sections one at a time (collaborative, incremental)
- Cross-references existing docs to prevent contradictions
- Routes to specialist agents for domain expertise
- Writes each section to file as soon as it's approved
- Runs `$design-review` when complete
- Updates the systems index

**Do not duplicate the $design-system workflow here.** This skill owns the systems
*index*; `$design-system` owns individual system *GDDs*.

### Step 6c: Loop or Stop

Do not loop inside this invocation. After the separate `$design-system` task completes, a later explicit `$map-systems next` invocation may select another system.

---

## Phase 7: Suggest Next Steps

After the systems index is created (or after designing some systems), present next actions by asking the user directly:

- "Systems index is written. What would you like to do next?"
  - [A] Start designing GDDs — run `$design-system [first-system-in-order]`
  - [B] Run `$gate-check systems-design` — triggers the CD-SYSTEMS and TD-SYSTEM-BOUNDARY gates automatically for a formal director sign-off on the system set
  - [C] Stop here for this session

**The gate-check option ([B]) is worth highlighting**: running `$gate-check systems-design` triggers both the CD-SYSTEMS and TD-SYSTEM-BOUNDARY gates, catching scope issues, missing systems, and boundary problems before they're locked in across many documents. It is optional but recommended for new projects.

After any individual GDD is completed:
- "Run `$design-review design/gdd/[system].md` in a fresh session to validate quality"
- "Run `$gate-check systems-design` when all MVP GDDs are complete"

---

## Collaborative Protocol

This skill follows the collaborative design principle at every phase:

1. **Question -> Options -> Decision -> Draft -> Approval** at every step
2. **direct question to the user** at every decision point (Explain -> Capture pattern):
   - Phase 2: "Missing systems? Combine or split?"
   - Phase 3: "Dependency ordering correct?"
   - Phase 4: "Priority assignments match your vision?"
   - Phase 5: Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.
   - Phase 6: "Start designing, pick different, or stop?" then hand off to `$design-system`
3. **Single changeset authorization**: preview the systems-index edit before the first file write
4. **Incremental writing**: Update the systems index after each system is designed
5. **Handoff**: Individual GDD authoring is owned by `$design-system`, which handles
   incremental section writing, cross-referencing, design review, and index updates
6. **Session state updates**: Write to `production/session-state/active.md` after
   each milestone (index created, system designed, priorities changed)

**Never** auto-generate the full systems list and write it without review.
**Never** start designing a system without user confirmation.
**Always** show the enumeration, dependencies, and priorities for user validation.

## Context Window Awareness

If context reaches or exceeds 70% at any point, append this notice:

> **Context is approaching the limit (≥70%).** The systems index is saved to
> `design/gdd/systems-index.md`. Open a fresh Codex session to continue
> designing individual GDDs — run `$map-systems next` to pick up where you left off.

---

## Recommended Next Steps

- Run `$design-system [first-system-in-order]` to author the first GDD (use design order from the index)
- Run `$map-systems next` to always pick the highest-priority undesigned system automatically
- Run `$design-review design/gdd/[system].md` in a fresh session after each GDD is authored
- Run `$gate-check pre-production` when all MVP GDDs are authored and reviewed
