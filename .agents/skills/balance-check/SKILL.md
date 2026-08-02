---
name: balance-check
description: "Analyzes game balance data files, formulas, and configuration to identify outliers, broken progressions, degenerate strategies, and economy imbalances. Use after modifying any balance-related data or design. Use when user says 'balance report', 'check game balance', 'run a balance check'."
---

## Invocation and execution

Invoke this workflow as `$balance-check`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[system-name|path-to-data-file]`. Treat bracketed values as optional unless the workflow says otherwise.

Delegate substantive work to the `economy-designer` Codex subagent role when it is available. If that role is unavailable, follow the same responsibilities in the current agent.


## Phase 1: Identify Balance Domain

Determine the balance domain from the first provided argument:

- **Combat** → weapon/ability DPS, time-to-kill, damage type interactions
- **Economy** → resource faucets/sinks, acquisition rates, item pricing
- **Progression** → XP/power curves, dead zones, power spikes
- **Loot** → rarity distribution, pity timers, inventory pressure
- **File path given** → load that file directly and infer domain from content

If no argument, ask the user which system to check.

---

## Phase 2: Read Data Files

Read relevant files from `assets/data/` and `design/balance/` for the identified domain.
Note every file read — they will appear in the Data Sources section of the report.

---

## Phase 3: Read Design Document

Read the GDD for the system from `design/gdd/` to understand intended design targets,
tuning knobs, and expected value ranges. This is the baseline for "correct" behaviour.

---

## Phase 4: Perform Analysis

Run domain-specific checks:

**Combat balance:**
- Calculate DPS for all weapons/abilities at each power tier
- Check time-to-kill at each tier
- Identify any options that dominate all others (strictly better)
- Check if defensive options can create unkillable states
- Verify damage type/resistance interactions are balanced

**Economy balance:**
- Map all resource faucets and sinks with flow rates
- Project resource accumulation over time
- Check for infinite resource loops
- Verify gold sinks scale with gold generation
- Check if any items are never worth purchasing

**Progression balance:**
- Plot the XP curve and power curve
- Check for dead zones (no meaningful progression for too long)
- Check for power spikes (sudden jumps in capability)
- Verify content gates align with expected player power
- Check if skip/grind strategies break intended pacing

**Loot balance:**
- Calculate expected time to acquire each rarity tier
- Check pity timer math
- Verify no loot is strictly useless at any stage
- Check inventory pressure vs acquisition rate

---

## Phase 5: Output the Analysis

```
## Balance Check: [System Name]

### Data Sources Analyzed
- [List of files read]

### Verdict: [BALANCED / CONCERNS / OUT OF BALANCE]

- BALANCED: every applicable calculation is supported by a design baseline and no material deviation is found.
- CONCERNS: one or more non-blocking deviations or unevaluated items require review.
- OUT OF BALANCE: at least one critical deviation or degenerate strategy is supported by the cited formula and values.

### Findings
| Value | Formula or Source | Expected | Actual | Deviation | Severity |
|-------|-------------------|----------|--------|-----------|----------|

### Degenerate Strategies Found
- [Strategy description and why it is problematic]

### Progression Analysis
[Graph description or table showing progression curve health]

### Recommendations
| Priority | Issue | Suggested Fix | Impact |
|----------|-------|--------------|--------|

### Values That Need Attention
[Specific values with suggested adjustments and rationale]
```

---

## Phase 6: Fix & Verify Cycle

After presenting the report, ask the user directly:
- Prompt: "Balance check complete. What would you like to do next?"
- Options:
  - `[A] Fix highest-priority issue now — walk me through it`
  - `[B] Save report to design/balance/balance-check-[system]-[date].md`
  - `[C] Stop here — I'll review the findings manually`

If [A]:
- Ask which issue to address first (refer to the Recommendations table by priority row)
- Show the current value, proposed value, exact target file, and the complete
  resulting edit for every affected data, formula, GDD, or ADR file. Obtain the
  single changeset authorization before changing any of them. If another file is
  discovered afterward, stop and present a revised complete changeset instead of
  editing outside the approved boundary.
- After authorization, apply only the previewed edits.
- After each fix, offer to re-run the relevant balance checks to verify no new outliers were introduced
- If the fix changes a tuning knob defined in a GDD or referenced by an ADR, remind the user:
  > "This value is defined in a design document. After the approved GDD edit has actually been written, run `$propagate-design-change [path]` on that changed GDD to find downstream impacts. Do not propagate a proposed value that is not yet in the document."

If [B]:
- Write the report to `design/balance/balance-check-[system]-[date].md` (create the directory if needed). Use the current date for [date] in YYYY-MM-DD format.
- Confirm the file was written, then end with: "Re-run `$balance-check` after fixes to verify."

If [C]:
- Summarize open issues and end with: "Re-run `$balance-check` after fixes to verify."
