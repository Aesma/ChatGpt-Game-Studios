# Review All Gdds — Required workflow continuation

This file contains required phases of `$review-all-gdds`. Read it in full when the main `SKILL.md` reaches its Required continuation section, then execute the phases in order.

## Phase 4: Cross-System Scenario Walkthrough

Walk through the game from the player's perspective to find problems that only
appear at the interaction boundary between multiple systems — things static
analysis of individual GDDs cannot surface.

### 4a: Identify Key Multi-System Moments

Scan all GDDs and identify the 3–5 most important player-facing moments where
multiple systems activate simultaneously. Look specifically for:

- **Combat + Economy overlap**: killing enemies that drop resources, spending
  resources during combat, death/respawn interacting with economy state
- **Progression + Difficulty overlap**: level-up triggering mid-fight, ability
  unlocks changing combat viability, difficulty scaling at progression milestones
- **Narrative + Gameplay overlap**: dialogue choices locking/unlocking mechanics,
  story beats interrupting resource loops, quest completion triggering system
  state changes
- **3+ system chains**: any player action that triggers System A, which feeds
  into System B, which triggers System C (these are highest-risk interaction paths)

List each identified scenario with a one-line description before proceeding.

### 4b: Walk Through Each Scenario

For each scenario, step through the sequence explicitly:

1. **Trigger** — what player action or game event starts this?
2. **Activation order** — which systems activate, in what sequence?
3. **Data flow** — what does each system output, and is that output a valid
   input for the next system in the chain?
4. **Player experience** — what does the player see, hear, or feel at each step?
5. **Failure modes** — are there any of the following?
   - **Race conditions**: two systems trying to modify the same state simultaneously
   - **Feedback loops**: System A amplifies System B which re-amplifies System A
     with no cap or dampener
   - **Broken state transitions**: a system assumes a state that a previous
     system may have changed (e.g., "player is alive" assumption after a combat
     step that could have caused death)
   - **Contradictory messaging**: player receives conflicting feedback from two
     systems reacting to the same event (e.g., "success" sound + "failure" UI)
   - **Compounding difficulty spikes**: two systems both scaling up at the same
     progression point, multiplying the intended difficulty increase
   - **Reward conflicts**: two systems both reacting to the same trigger with
     rewards that together exceed the intended value (double-dipping)
   - **Undefined behavior**: the GDDs don't specify what happens in this combined
     state (neither system's rules cover it)

```
Example walkthrough:
Scenario: Player kills elite enemy at level-up threshold during active quest

Trigger: Player lands killing blow on elite enemy
→ combat.md: awards kill XP (100 pts)
→ progression.md: XP total crosses level threshold → triggers level-up
  Output: new level, stat increases, ability unlock popup
→ quest.md: kill-count criterion met → triggers quest completion event
  Output: quest reward XP (500 pts), completion fanfare
→ progression.md (again): quest XP added → triggers SECOND level-up in same frame
  ⚠️  Data flow issue: quest.md awards XP without checking if a level-up
  is already in progress. progression.md has no guard against concurrent
  level-up events. Undefined behavior: does the player level up once or twice?
  Does the ability popup fire twice? Does the second level use the updated or
  pre-update stat baseline?
```

### 4c: Flag Scenario Issues

For each problem found during the walkthrough, categorize severity:

- **BLOCKER**: undefined behavior, broken state transition, or contradictory
  player messaging — the experience is broken or incoherent in this scenario
- **WARNING**: compounding spikes, feedback loops without caps, reward conflicts —
  the experience works but produces unintended outcomes
- **INFO**: minor ordering ambiguity or messaging overlap — worth noting but
  unlikely to cause player-visible problems

Add all findings to the output report under **"Cross-System Scenario Issues"**.
Each finding must cite: the scenario name, the specific systems involved, the
step where the issue occurs, and the nature of the failure mode.

---

## Phase 5: Output the Review Report

```
## Cross-GDD Review Report
Date: [date]
GDDs Reviewed: [N]
Systems Covered: [list]

---

### Consistency Issues

#### Blocking (must resolve before architecture begins)
🔴 [Issue title]
[What GDDs are involved, what the contradiction is, what needs to change]

#### Warnings (should resolve, but won't block)
⚠️  [Issue title]
[What GDDs are involved, what the concern is]

---

### Game Design Issues

#### Blocking
🔴 [Issue title]
[What the problem is, which GDDs are involved, design recommendation]

#### Warnings
⚠️  [Issue title]
[What the concern is, which GDDs are affected, recommendation]

---

### Cross-System Scenario Issues

Scenarios walked: [N]
[List scenario names]

#### Blockers
🔴 [Scenario name] — [Systems involved]
[Step where failure occurs, nature of the failure mode, what must be resolved]

#### Warnings
⚠️  [Scenario name] — [Systems involved]
[What the unintended outcome is, recommendation]

#### Info
ℹ️  [Scenario name] — [Systems involved]
[Minor ordering ambiguity or note]

---

### GDDs Flagged for Revision

| GDD | Reason | Type | Priority |
|-----|--------|------|----------|
| [system-a].md | Rule contradiction with [system-b].md | Consistency | Blocking |
| [system-c].md | Stale reference to nonexistent mechanic | Consistency | Blocking |
| [system-d].md | No pillar alignment | Design Theory | Warning |

---

### Verdict: [PASS / CONCERNS / FAIL]

PASS: No blocking issues. Warnings present but don't prevent architecture.
CONCERNS: Warnings present that should be resolved but are not blocking.
FAIL: One or more blocking issues must be resolved before architecture begins.

### If FAIL — required actions before re-running:
[Specific list of what must change in which GDD]
```

---

## Phase 6: Write Report and Flag GDDs

Use the single changeset approval policy:
- Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.
- Options: `[A] Yes — write the report` / `[B] No — skip`

If any GDDs are flagged for revision, use a second a direct question to the user:
- Prompt: "Should I update the systems index to mark these GDDs as needing revision? ([list of flagged GDDs])"
- Options: `[A] Yes — update systems index` / `[B] No — leave as-is`
- Once the complete changeset is authorized, update each flagged GDD's Status field in systems-index.md to "Needs Revision".
  (Do NOT append parentheticals to the status value — other skills match "Needs Revision"
  as an exact string and parentheticals break that match.)

### Session State Update

After writing the report (and updating the systems index when included in the authorized changeset), silently
append to `production/session-state/active.md`:

    ## Session Extract — $review-all-gdds [date]
    - Verdict: [PASS / CONCERNS / FAIL]
    - GDDs reviewed: [N]
    - Flagged for revision: [comma-separated list, or "None"]
    - Blocking issues: [N — brief one-line descriptions, or "None"]
    - Recommended next: [the Phase 7 handoff action, condensed to one line]
    - Report: design/gdd/gdd-cross-review-[date].md   ← only if user approved the write
    - Report: (not written — user declined at [date])  ← only if user declined the write

Use the appropriate line based on the user's response to the write-permission structured prompt in Phase 6.

If `active.md` does not exist, create it with this block as the initial content.
Confirm in conversation: "Session state updated."

---

## Phase 7: Handoff

After all file writes are complete, ask the user directly for a closing structured prompt.

Before building options, check project state:
- Are there any Warning-level items that are simple edits (flagged with "30-second edit", "brief addition", or similar)? → offer inline quick-fix option
- Are any GDDs in the "Flagged for Revision" table? → offer $design-review option for each
- Read systems-index.md for the next system with Status: Not Started → offer $design-system option
- Is the verdict PASS or CONCERNS? → offer $gate-check or $create-architecture

Build the option list dynamically — only include options that apply:

**Option pool:**
- `[_] Apply quick fix: [W-XX description] in [gdd-name].md — [effort estimate]` (one option per simple-edit warning; only for Warning-level, not Blocking)
- `[_] Run $design-review [flagged-gdd-path] — address flagged warnings` (one per flagged GDD, if any)
- `[_] Run $design-system [next-system] — next in design order` (always include, name the actual system)
- `[_] Run $create-architecture — begin architecture (verdict is PASS/CONCERNS)` (include if verdict is not FAIL)
- `[_] Run $gate-check — validate Systems Design phase gate` (include if verdict is PASS)
- `[_] Stop here`

Assign letters A, B, C… only to included options. Mark the most pipeline-advancing option as `(recommended)`.

Never end the skill with plain text. Always close with this structured prompt.

---

## Error Recovery Protocol

If any spawned agent returns BLOCKED, errors, or fails to complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" before continuing
2. **Assess dependencies**: If the blocked agent's output is required by a later phase, do not proceed past that phase without user input
3. **Offer options** by asking the user directly with three choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope (fewer GDDs, single-system focus)
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed so work is not lost

---

## Collaborative Protocol

1. **Read silently** — load all GDDs before presenting anything
2. **Show everything** — present the full consistency and design theory analysis
   before asking for any action
3. **Distinguish blocking from advisory** — not every issue needs to block
   architecture; be clear about which do
4. **Don't make design decisions** — flag contradictions and options, but never
   unilaterally decide which GDD is "right"
5. **Single changeset approval** — preview the report and systems-index update together, then write both after the one approval
6. **Be specific** — every issue must cite the exact GDD, section, and text
   involved; no vague warnings
