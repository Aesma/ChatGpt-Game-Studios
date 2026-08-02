# Prototype — Required workflow continuation

This file contains required phases of `$prototype`. Read it in full when the main `SKILL.md` reaches its Required continuation section, then execute the phases in order.

## Phase 7: Draft Prototype Report In Memory

Read `.codex/docs/templates/prototype-report.md` and fill every section from actual observations. Keep REPORT.md and the corresponding `prototypes/index.md` row in memory; do not write them yet. Simulated Paper walkthroughs must be labelled non-player evidence and cannot support a player-experience recommendation.

---

## Phase 8: Creative Director Review

**Review mode check:**
- `solo` → skip. Note: "CD-PLAYTEST skipped — Solo mode."
- `lean` → skip. Note: "CD-PLAYTEST skipped — Lean mode."
- `full` → spawn `creative-director` through Codex subagent delegation using gate **CD-PLAYTEST** if `design/gdd/game-concept.md` exists with game pillars defined. If pillars are absent, record the skip reason.

Pass the in-memory report draft, original hypothesis, and existing pillars/core fantasy. The gate returns only its standard **APPROVE / CONCERNS / REJECT** verdict about evidence support and pillar drift. It does not return, choose, modify, or override PROCEED/PIVOT/KILL.

APPROVE leaves the user's recommendation unchanged. For CONCERNS or REJECT, show the evidence and let the user re-decide among the existing recommendations or stop; the user owns that product decision. Resolve this before any report/index write.

---

## Phase 9: Finalize, Write, and Hand Off

After review and the user's final recommendation, assemble Batch 2: the actual REPORT.md, `prototypes/index.md`, and the applicable PIVOT-NOTE.md or GRAVEYARD.md edit. Show every exact path and modification together and obtain one authorization, then write them as one bounded batch. If the file set expands or any write fails, stop and do not claim completion. Do not update the verdict after this write.

Output a summary: the hypothesis, the result, and the user-owned final recommendation.
Link to `prototypes/[concept-name]-concept/REPORT.md`.

**If PROCEED:**
Your concept prototype validated the core idea. Now design it properly, informed by
what you just learned.

Recommended path (in order):
1. Reconcile the existing game-concept sections against what the prototype revealed; do not pass the concept document to the system-GDD-only `$design-review`
2. `$gate-check` — confirm readiness to advance to Systems Design
3. `$art-bible` — define visual identity (optional but worth doing before GDDs)
4. `$map-systems` — decompose the concept into all game systems
5. `$design-system [mechanic]` — GDD for each MVP system; use prototype learnings
   in the Tuning Knobs and Formulas sections
6. `$review-all-gdds` — cross-system consistency check

**Note:** If you used the HTML path and feel is still uncertain, consider running
a quick engine path prototype targeting feel before writing GDDs.

**If PIVOT:**

Before routing to the next prototype, capture the carry-forward note. Ask these
two questions (plain text, one at a time):

1. "What specifically worked in this prototype that we should preserve in the next version?"
2. "What is the single most important thing to change?"

The PIVOT-NOTE.md content (original hypothesis, what to keep/change, and revised hypothesis) is part of the single Phase 9 Batch 2 preview and write; do not ask for a separate file authorization. When `$prototype` is next run, read only PIVOT notes linked from this concept's REPORT/index row or located in its explicitly related concept directory. Do not chain unrelated notes merely because they exist elsewhere under `prototypes/`. Use the linked revised hypothesis as the starting point.

- Run `$prototype [revised-concept]` to test the adjusted direction
- Or `$brainstorm [hint]` if the concept needs more fundamental rethinking

**If KILL:**

Before moving on, run this check to confirm the verdict is sound and not temporary frustration:

- [ ] Core mechanic still unclear to testers after 2+ playtests?
- [ ] No "fun moment" (smile, laugh, or retry by choice) observed in any session?
- [ ] 3+ PIVOT iterations on the same concept with no clear improvement?
- [ ] Concept only works when heavily explained or when the dev guides the player?
- [ ] Building this feels like obligation, not excitement?

Check a box only when an existing REPORT/index entry provides the supporting playtest or pivot evidence. If the thresholds are not evidenced, recommend another focused test or PIVOT rather than forcing KILL. The checklist informs the user's decision; it never auto-selects KILL.

**Document the kill in `prototypes/GRAVEYARD.md`** only as part of the single Phase 9 Batch 2 preview and write. Add one entry:

```
## [Concept Name] — YYYY-MM-DD
- **Kill reason:** [specific blocker — not "it was boring" but "players never understood the core action"]
- **What worked:** [2-3 things worth carrying forward to future concepts]
- **What failed:** [the specific mechanic, design decision, or scope issue]
- **Next time:** [one explicit action to try differently on a similar concept]
```

This file exists so the same mistake doesn't get made twice on the next concept.

- Run `$brainstorm open` or `$brainstorm [new-hint]` to explore a different concept
- The prototype report is the deliverable — no further action needed

---

---

## Spike Mode

**Triggered by:** `--spike` flag OR "Mid-production spike" entry choice in Phase 1.

**Purpose:** Test a specific technical or design question mid-production, without
the overhead of a full concept prototype workflow. No GDD prerequisites. No phase
gate implications. Hard cap: ~4 hours.

**When to use:**
- You're in Production and want to test whether a new mechanic should be added
- You're unsure if a technical approach will work before building it properly
- A design change is being considered and you want a quick before/after comparison
- A GDD system is proving harder than expected and you want to prototype the hard part
- You need to confirm target hardware can sustain the required framerate before writing gameplay code (**performance spike** — see below)

**Spike Mode workflow (replaces Phases 1–9):**

1. **Define the spike question** (an open-ended question): "What specific question does this spike answer? Give me one sentence: 'Can we [do X] using [approach Y]?'"

2. **Choose path** — same structured choice prompt as Phase 3 (HTML / Engine / Paper).

3. **Scope** — maximum 2-3 bullet points. One mechanic, one technical question, nothing else.

4. **Build** — same relaxed standards as concept prototype. Before writing, show the spike worktree/current-workspace path plus all initial build files as Batch 1 and obtain one authorization. Ask the user to report elapsed time at checkpoints; if they report 4 hours without a demonstrable result, the question is too large. Split it. Do not pretend to time the work automatically.

5. **Observe and decide** — no formal playtest debrief. Ask: "Did the spike answer the question? YES or NO, and why in one sentence."

6. **Write a spike note** (not a full report) to `prototypes/[concept-name]-spike-[date]/SPIKE-NOTE.md`. Preview it together with the exact `production/session-state/active.md` restoration as Batch 2 and obtain one authorization:
   - Question tested
   - Result (YES it works / NO it doesn't / PARTIAL — needs more investigation)
   - What to do next (add to current sprint / investigate further / abandon the idea)

7. **Update `production/session-state/active.md`** only after the spike note is ready and Batch 2 is authorized. If the build fails or Batch 2 is declined/fails, retain the prior active-sprint state, report the incomplete spike, and never clear it as though the spike completed.

**No CD gate. No phase gate. No PROCEED/PIVOT/KILL.** Spike results inform decisions; they don't make them. The developer decides whether to add the mechanic/approach to the sprint backlog based on what the spike revealed.

**Performance spike (special case):** If the game involves demanding rendering —
large open worlds, hundreds of simultaneous physics bodies, heavy particle systems,
complex shaders — run a performance spike before writing gameplay code to confirm
the target hardware can sustain the required framerate. This is distinct from other
spikes in two ways:
- The question is "can the engine render [scene X] at 60fps on [minimum spec hardware]?"
  not "does this mechanic feel good?"
- The output is a benchmark number, not a feel verdict
- No gameplay logic is needed — just the maximum intended scene load (terrain, draw
  calls, physics objects, particles) running at once
- Build time stays within the ~4-hour cap; the spike is setting up the rendering
  load, not the game
- If the answer is NO at this scope, this is an architecture or scope constraint
  that affects everything downstream — better to surface it now than during Sprint 8

---

### Important Constraints

- Prototype code must NEVER import from production source files
- Production code must NEVER import from prototype directories
- If the recommendation is PROCEED, production implementation is written from
  scratch — prototype code is never refactored into production
- Total effort is hard-capped at 1 day (concept prototypes test one mechanic)
- Test ONE mechanic — if scope grows, stop and simplify the question
- No polish. No menus, no game over, no music, no UI unless it IS the mechanic
- If stuck after 2 hours of engine iteration, reframe the question or switch paths
- **Three evidenced PIVOT iterations trigger a user decision, not an automatic KILL.**
  Count only related REPORT/index-linked iterations. Ask: "Is this the right idea,
  or am I in the sunk cost trap?" If the evidence is incomplete, recommend another
  focused test; the user still chooses PIVOT or KILL.
- Building 2-3 different concept variants and picking the best one is a healthier
  strategy than iterating one concept to death. Natural selection between prototypes
  beats willpower.
- **Networked/multiplayer games:** A local prototype cannot validate the feel of a
  networked mechanic. Latency fundamentally changes how combat, movement, and
  prediction feel — a prototype running at 0ms local will feel entirely different at
  80ms network delay. Use a local prototype to validate that the mechanic is
  *interesting*. Do not use it as evidence that it *feels good* under real network
  conditions. Network feel requires real peers or simulated latency (e.g., throttle
  tools, network condition simulators).
