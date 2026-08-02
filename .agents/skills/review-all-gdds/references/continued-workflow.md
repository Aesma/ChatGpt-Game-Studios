# Review All Gdds — Required workflow continuation

This file contains required phases of `$review-all-gdds`. Read it in full when the main `SKILL.md` reaches its Required continuation section, then execute the phases in order.

## Phase 4: Cross-System Scenario Walkthrough

Walk through the game from the player's perspective to find problems that only
appear at interaction boundaries.

### 4a: Identify Key Multi-System Moments

Identify 3–5 important player-facing moments where multiple systems activate,
including combat/economy, progression/difficulty, narrative/gameplay, and 3+
system chains. List each scenario before proceeding.

Look specifically at combat rewards, level-up during active play, narrative
events that change mechanic availability, death/respawn with persistent state,
and any action whose outputs feed two more systems.

### 4b: Walk Through Each Scenario

For each scenario, step through:

1. trigger;
2. activation order;
3. data flow and validity;
4. player experience;
5. evidence-backed failure modes such as races, feedback loops, broken states,
   contradictory messaging, compounding spikes, reward conflicts, or missing interaction rules.

For each step, identify the triggering action/event, activation order, values
passed between systems, and what the player sees/hears/feels. A plausible race
or reward double-count is a warning until the GDD text establishes the failure.

### 4c: Flag Scenario Issues

- **BLOCKER**: only an explicit contradiction between existing GDD rules, a
  documented broken state transition, or contradictory player-facing outcome
  that makes the scenario incoherent.
- **WARNING**: an interaction is unspecified, or evidence supports a plausible
  compounding/feedback/reward risk but not a direct contradiction.
- **INFO**: minor ordering ambiguity or messaging overlap unlikely to break the scenario.

Undefined combined behavior is not automatically broken. When neither GDD
specifies the interaction, default to WARNING and identify the missing rule.
Every finding cites the scenario, systems, step, and evidence.

Example shape:

```text
Scenario: [player-facing multi-system moment]
Trigger: [action/event]
→ [system A]: [documented output]
→ [system B]: [documented input/reaction]
Finding: [explicit contradiction / unspecified interaction / minor ambiguity]
Evidence: [GDD paths and sections]
```

---

## Phase 5: Output the Review Report

```markdown
## Cross-GDD Review Report
Date: [date]
GDDs Reviewed: [N]
Systems Covered: [list]

### Consistency Issues
#### Blocking
[findings]
#### Warnings
[findings]

### Game Design Issues
#### Blocking
[findings]
#### Warnings
[findings]

### Cross-System Scenario Issues
Scenarios walked: [N]
#### Blockers
[findings]
#### Warnings
[findings]
#### Info
[findings]

### GDDs Flagged for Revision
| GDD | Reason | Type | Priority |
|-----|--------|------|----------|
| [path] | [reason] | [type] | [Blocking/Warning] |

### Verdict: [PASS / CONCERNS / FAIL]

PASS: Zero blockers and zero warnings. INFO items do not affect the verdict.
CONCERNS: Zero blockers and one or more warnings.
FAIL: One or more blockers.

### If FAIL — required actions before re-running
[Specific GDD paths/sections that must be reconciled]
```

---

## Phase 6: Write Optional Report

Analysis is read-only. Offer one optional report write to
`design/gdd/gdd-cross-review-[date].md` under the single changeset approval
policy. If the user declines, finish with zero file changes.

Do not modify systems-index, session state, or status values. The report lists
flagged GDDs and recommended follow-up.

---

## Phase 7: Handoff

After any authorized report write, list applicable later commands as text only:

- `$design-review [flagged-gdd-path]` for a flagged GDD;
- `$design-system [next-system]` only when systems-index has a specific next
  `Not Started` system;
- `$create-architecture` when the verdict is PASS or CONCERNS;
- `$gate-check` when the verdict is PASS.

Recommendations for small edits may be included in the report, but this
workflow never applies an inline quick fix and never executes a handoff command.
End after the command list; the user must invoke later work separately.

---

## Error Recovery Protocol

If a delegated phase is blocked, errors, or fails:

1. surface the agent and reason;
2. mark that phase as partial coverage;
3. complete any independent phase that can still run;
4. produce a partial report with no complete PASS/CONCERNS/FAIL verdict and
   list retry/narrow-scope/stop as later choices.

---

## Collaborative Protocol

1. Load all selected GDDs before presenting analysis.
2. Show the complete analysis before asking about the optional report.
3. Distinguish blockers, warnings, info, and unassessed data.
4. Do not decide which contradictory GDD is authoritative.
5. Preview only the optional report file, then write it after one authorization.
6. Cite exact GDD paths, sections, and text for every issue.
