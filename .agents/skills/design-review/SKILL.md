---
name: design-review
description: "Reviews a game design document for completeness, internal consistency, implementability, and adherence to project design standards. Run this before handing a design document to programmers."
---

## Invocation and execution

Invoke this workflow as `$design-review`.

This workflow is read-only. It never modifies the target GDD, systems index,
review log, or any other project file, and therefore never requests changeset
authorization.

Arguments: `[path-to-design-doc] [--depth full|lean|solo]`. Treat bracketed values as optional unless the workflow says otherwise.


## Phase 0: Parse Arguments

Require exactly one target path and optionally one valid
`--depth [full|lean|solo]`. Normalize the path and accept only an existing
project-local Markdown file directly under `design/gdd/`. Explicitly reject
`game-concept.md`, `systems-index.md`, anything under `design/gdd/reviews/`,
directories, non-Markdown files, project-external paths, missing/multiple
targets, and unknown flags. On invalid input, stop without a verdict.

Extract `--depth [full|lean|solo]` if present. Default is `full` when no flag is given.

**Note**: `--depth` controls the *analysis depth* of this skill (how many specialist agents are spawned). It is independent of the global review mode in `production/review-mode.txt`, which controls director gate spawning. These are two different concepts — `--depth` is about how thoroughly *this* skill analyses the document.

- **`full`**: Complete review — all phases + specialist agent delegation (Phase 3b)
- **`lean`**: All phases, no specialist agents — faster, single-session analysis
- **`solo`**: Phases 1-4 only, no delegation, no Phase 5 next-step prompt — use when called from within another skill

---

## Phase 1: Load Documents

Read the target design document in full. Read every applicable `AGENTS.md` from
the repository root through the target's parent, with the closest rule taking
precedence, and list the files used in the report. Read only the game concept,
documents explicitly linked by the target, GDDs directly named in Dependencies,
and narrative files explicitly associated with this system. Do not expand
`implied` context into a directory-wide read.

**Dependency graph validation:** For every system listed in Dependencies, compare
the explicit link and systems-index entry. Report one of: `GDD exists`, `listed
but not authored` (including Not Started/In Design), `not listed/unknown`, or
`explicit link broken`. Only the latter two are broken references; an indexed
system awaiting a GDD is not broken.

**Lore/narrative alignment:** Read `design/gdd/game-concept.md` and only narrative
files explicitly linked to this system, when they exist. Note any mechanical choices in this GDD that contradict established world rules, tone, or design pillars. Pass this context to `game-designer` in Phase 3b.

**Prior review check:** Check whether `design/gdd/reviews/[doc-name]-review-log.md` exists. If it does, read the most recent entry — note what verdict was given and what blocking items were listed. This session is a re-review; track whether prior items were addressed.

---

## Phase 2: Completeness Check

Evaluate against the Design Document Standard checklist:

- [ ] Has Overview section (one-paragraph summary)
- [ ] Has Player Fantasy section (intended feeling)
- [ ] Has Detailed Rules section (unambiguous mechanics)
- [ ] Has Formulas section (all math defined with variables)
- [ ] Has Edge Cases section (unusual situations handled)
- [ ] Has Dependencies section (other systems listed)
- [ ] Has Tuning Knobs section (configurable values identified)
- [ ] Has Acceptance Criteria section (testable success conditions)

A heading is complete only when it has substantive, non-placeholder content.
Within these same eight checks, require Formulas to define variables, ranges, and
an example when math applies; Edge Cases to name concrete conditions and outcomes;
Tuning Knobs to give safe ranges and effects; and Acceptance Criteria to be
independently testable. Phrases such as `gracefully`, `feels good`, or `works
correctly` without observable criteria are blockers, not completed sections.

---

## Phase 3: Consistency and Implementability

**Internal consistency:**
- Do the formulas produce values that match the described behavior?
- Do edge cases contradict the main rules?
- Are dependencies bidirectional (does the other system know about this one)?

**Implementability:**
- Are the rules precise enough for a programmer to implement without guessing?
- Are there any "hand-wave" sections where details are missing?
- Are performance implications considered?

**Cross-system consistency:**
- Does this conflict with any existing mechanic?
- Does this create unintended interactions with other systems?
- Is this consistent with the game's established tone and pillars?

---

## Phase 3b: Adversarial Specialist Review (full mode only)

**Skip this phase in `lean` or `solo` mode.**

**This phase is MANDATORY in full mode.** Do not skip it.

**Before spawning any agents**, print this notice:
> "Full review: spawning relevant specialist agents. Duration depends on the selected roles and available capacity. Use `--depth lean` for single-session analysis."

### Step 1 — Identify all domains the GDD touches

Read the GDD and identify every domain present. A GDD can touch multiple domains simultaneously — be thorough. Common signals:

| If the GDD contains... | Spawn these agents |
|------------------------|-------------------|
| Costs, prices, drops, rewards, economy | `economy-designer` |
| Combat stats, damage, health, DPS | `game-designer`, `systems-designer` |
| AI behaviour, pathfinding, targeting | `ai-programmer` |
| Level layout, spawning, wave structure | `level-designer` |
| Player progression, XP, unlocks | `economy-designer`, `game-designer` |
| UI, HUD, menus, player-facing displays | `ux-designer`, `ui-programmer` |
| Dialogue, quests, story, lore | `narrative-director` |
| Animation, feel, timing, juice | `gameplay-programmer` |
| Multiplayer, sync, replication | `network-programmer` |
| Audio cues, music triggers | `audio-director` |
| Performance, draw calls, memory | `performance-analyst` |
| Engine-specific patterns or APIs | Primary engine specialist only when it is configured in `docs/technical-preferences.md`; otherwise skip and report `engine-specific review not run` |
| Acceptance criteria, test coverage | `qa-lead` |
| Data schema, resource structure | `systems-designer` |
| Any gameplay system | `game-designer` (always) |

Spawn `game-designer` for all GDDs that describe gameplay mechanics or player-facing rules.
Spawn `systems-designer` for all GDDs that contain formulas or system interaction rules.
These are the most common baselines — but not required for pure UI specs, audio specs, or lore documents. Use the domain table above to determine which specialists are truly relevant.

### Step 2 — Spawn all relevant specialists in parallel

**CRITICAL: Subagent delegation in this skill starts a separate Codex agent — a separate independent Codex session
with its own context window. It is NOT task tracking. Do NOT simulate specialist
perspectives internally. Do NOT reason through domain views yourself. You MUST issue
actual subagent delegations. A simulated review is not a specialist review.**

Deduplicate the relevant role list, rank it by the target GDD's principal
risks, and inspect the currently available subagent capacity. Keep execution
space for the primary task. Start only the roles that fit; run the remainder in
bounded batches as slots become available. Never fabricate a role result that
was not actually returned.

**Prompt each specialist for evidence:**
> "Here is the GDD for [system] and the main review's structural findings so far.
> Verify the design from your domain. For each issue, cite the document location,
> explain its impact, classify it as blocking/recommended/nice-to-have, and give
> an actionable correction. Do not manufacture findings when a requirement is
> already satisfied. Disagreement with the main review is welcome when supported."

**Additional instructions per agent type:**

- **`game-designer`**: Anchor your review to the `Player Fantasy` heading of this GDD. Does this design actually deliver that fantasy? Would a player feel the intended experience? Flag any rules that serve implementability but undermine the stated feeling.

- **`systems-designer`**: For every formula in the GDD, plug in boundary values (minimum and maximum plausible inputs). Report whether any outputs go degenerate — negative values, division by zero, infinity, or nonsensical results at the extremes.

- **`qa-lead`**: Review every acceptance criterion. Flag any that are not independently testable — phrases like "feels balanced", "works correctly", "performs well" are not ACs. Suggest concrete rewrites for any that fail this test.

### Step 3 — Complete and merge specialist results

After all attempted specialist batches settle, list any role that did not
complete and the reason. Use completed findings to produce NEEDS REVISION or
MAJOR REVISION NEEDED when those existing conditions are already established.
If missing reviews are necessary to establish a clean result, state that the
full review is incomplete and do not issue a verdict. If no required specialist
succeeds, stop with a clear error and no verdict.

Merge findings that cite the same document location and defect, preserving every
source on the merged item. The primary reviewer performs the final synthesis;
do not spawn a director or let any single specialist override the deterministic
Phase 4 mapping.

### Step 4 — Surface disagreements

If specialists disagree with each other or with the creative-director, do NOT silently pick one view. Present the disagreement explicitly in Phase 4 so the user can adjudicate.

Mark every finding with its source: `[game-designer]`, `[economy-designer]`, `[creative-director]` etc.

---

## Phase 4: Output Review

```
## Design Review: [Document Title]
Specialists consulted: [list agents spawned]
Re-review: [Yes — prior verdict was X on YYYY-MM-DD / No — first review]

### Completeness: [X/8 sections present]
[List missing sections]

### Dependency Graph
[List each declared dependency and whether its GDD file exists on disk]
- ✓ enemy-definition-data.md — exists
- ✗ loot-system.md — NOT FOUND (file does not exist yet)

### Required Before Implementation
[Numbered list — blocking issues only. Each item tagged with source agent.]

### Recommended Revisions
[Numbered list — important but not blocking. Source-tagged.]

### Specialist Disagreements
[Any cases where agents disagreed with each other or with the main review.
Present both sides — do not silently resolve.]

### Nice-to-Have
[Minor improvements, low priority.]

For `lean` and `solo`, write `Specialists consulted: none`; use `primary review`
as the finding source and omit specialist disagreements or any senior/director
verdict. For `full`, list only roles that actually returned.

### Scope Signal
Estimate implementation scope based on: dependency count, formula count,
systems touched, and whether new ADRs are required.
Evaluate in order XL → L → M → S and stop at the first match:
- **XL** — cross-cutting concern or 7+ dependencies; multiple new ADRs likely
- **L** — multi-system integration, 3+ formulas, or 5–6 dependencies
- **M** — moderate complexity, 1–2 formulas, 3–4 dependencies
- **S** — single system, no formulas, no new ADRs, 0–2 dependencies
A formula or ADR condition may raise the result only to the explicitly matching
higher band. Label clearly: "Rough scope signal: M (producer should verify before sprint planning)"

### Verdict: [APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED]
```

Apply this mapping consistently:
- `APPROVED`: no blocking issue; recommended and nice-to-have items may remain.
- `NEEDS REVISION`: at least one local, repairable blocker.
- `MAJOR REVISION NEEDED`: core rules contradict each other, a core product
  decision is unresolved, or at least three required sections lack substantive
  content.
No specialist synthesis may downgrade an existing blocker.

This entire skill is read-only — no files are written in any phase.

---

## Phase 5: Next Steps

Output non-writing guidance and end the review.

- For APPROVED, explain the existing downstream step without changing
  `systems-index.md` or a review log.
- For NEEDS REVISION or MAJOR REVISION NEEDED, list the exact existing GDD
  sections that require revision and any decisions the user must make. Tell the
  user to revise in a separate explicit request and then invoke
  `$design-review [same-path]` again.
- Do not implement revisions, mark Approved, offer a skip-re-review path, update
  tracking files, or create/append a review log during this run.
- Offer Stop and at most the directly relevant next action. Do not claim any
  document or status was changed.
