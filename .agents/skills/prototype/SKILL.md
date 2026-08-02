---
name: prototype
description: "Concept prototype — validate the core idea is worth designing before writing GDDs. Run right after $brainstorm and $setup-engine. Routes to HTML, Engine, or Paper path based on game type. Produces a throwaway build and a PROCEED/PIVOT/KILL verdict."
---

## Invocation and execution

Invoke this workflow as `$prototype`.

This workflow has two bounded write batches because report content does not exist
until after playtesting. Before each batch's first write, present every exact file
and intended modification in that batch and obtain one approval. Do not re-prompt
file by file inside a batch. If a batch's file set expands, stop and re-preview
that batch; never treat the first batch as authorization for unknown report data.

Arguments: `[concept-description] [--path html|engine|paper] [--review full|lean|solo] [--spike]`. Treat bracketed values as optional unless the workflow says otherwise.

Before parsing arguments, read `references/continued-workflow.md` in full, including its Spike Mode section.

Delegate substantive work to the `prototyper` Codex subagent role when it is available. If that role is unavailable, follow the same responsibilities in the current agent.

Run implementation in an isolated Git worktree. At the start, display the actual worktree path and current branch and state that session-state, build files, and report files will all be written there. If the isolated worktree cannot be created or used, show the reason and ask the user to continue in the current workspace or stop. If they decline current-workspace use, stop without writes.


## Purpose

This is the **concept prototype** — a fast, throwaway build that answers one question:
*"Is this core idea actually fun to interact with?"*

**Default use** — run right after `$brainstorm` and `$setup-engine`, before writing
GDDs or architecture docs. Its verdict determines whether the concept is worth the
investment of full design documentation.

**Mid-production?** You can also run this at any stage to test a specific mechanic,
design change, or technical question. Pass `--spike` to activate spike mode: a
lightweight ~4-hour build with no GDD prerequisites and no phase gate implications.

**Already have GDDs and architecture complete?** To validate the full game loop
before committing to Production, run `$vertical-slice` instead.

---

## Phase 1: Define the Question

Resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `production/review-mode.txt` → use that value
3. Else → default to `lean`

**Check for spike mode:** If `--spike` was passed, jump to `references/continued-workflow.md#spike-mode`, already loaded above. Do not enter any concept-prototype phase first.

Otherwise, ask the user directly to confirm intent before proceeding:

- **Prompt**: "How would you like to use this prototype session?"
- **Options**:
  - `Prototype this concept` — build a throwaway build to validate the core idea is fun before writing GDDs (1–3 days)
  - `Skip — concept already proven` — I have enough evidence this works; log it and proceed directly to design
  - `Mid-production spike` — I'm already in Production and want to test a specific mechanic or technical question quickly (~4 hours, no phase gate implications)

**If "Skip — concept already proven":**
Ask (an open-ended question): "What evidence do you have that the concept works?"
Record the one-line answer, then stop. Note: "Concept prototype skipped — evidence:
[answer]." Suggest next step: `$map-systems` or `$design-system [mechanic]`.

**If "Mid-production spike"**: jump to the Spike Mode section in the required continuation.

**If "Prototype this concept"**: continue with Phase 1 below.

---

**A note on prototype strategy:** The research on successful indie development
is consistent — building 2-3 concept variants and letting the best one win is
far more likely to succeed than iterating one concept until it works. This is
your first prototype, not necessarily your only one. If this prototype produces
a PIVOT verdict, consider whether to refine this concept OR start fresh with a
different angle on the same game idea and prototype that instead.

**Game jam as a prototype vehicle:** If you're planning a concept prototype anyway,
consider timing it to a game jam (Ludum Dare, GMTK Game Jam, Global Game Jam). Jams
provide a forced timebox (48-72 hours), instant distribution to thousands of players
who rate and review early builds, and a deadline that prevents scope creep by design.
Many shipped games (Celeste, VVVVVV) began as jam prototypes. Not required — but
worth considering if the timing is right.

Read the concept description from the argument and derive exactly one safe directory slug. Reject path separators, traversal, absolute paths, and empty/ambiguous slugs. The target is `prototypes/[slug]-concept/` (or the existing spike suffix in Spike Mode).

Before building anything, define
the **falsifiable hypothesis** this prototype must answer:

> *"If the player [does X], they will feel [Y] — we will know this is true if [measurable signal Z]."*

Good: "If the player swings on grapple hooks, traversal will feel fluid — we'll know if
players chain 3+ swings without stopping within 2 minutes of picking it up."

Bad: "Does this feel fun?" ← not testable, not falsifiable.

**If the concept is too vague to form a hypothesis, stop here.** Ask the user to
narrow the question before proceeding. A prototype without a clear question wastes time.

Also ask: **"What is the riskiest assumption in this concept?"** That is the first
thing the prototype should test — not the easiest part, the riskiest.

---

## Phase 2: Load Concept Context

Read `design/gdd/game-concept.md` if it exists. Extract:
- Core fantasy (what the player is supposed to feel)
- Core loop (the moment-to-moment action being tested)

Read `AGENTS.md` and `docs/technical-preferences.md` for the engine and
language in use.

---

## Phase 3: Choose the Prototype Path

Select the prototype path. If one valid `--path [html|engine|paper]` was passed, use it directly and explain why; do not ask the user to choose it again. If it conflicts with the hypothesis (for example HTML for timing-sensitive feel), show the risk and ask only whether to confirm that supplied path or stop.
Otherwise, use this quick-reference first, then read the full path details below:

| Genre | Recommended path | Key reason |
|-------|-----------------|------------|
| Platformer / action / fighter | **Engine** | Feel IS the hypothesis; browser latency produces false results |
| Racing / sports | **Engine** | Same — timing and physics feedback are the point |
| Top-down shooter / twin-stick | **Engine** | Aim feel is timing-sensitive |
| Puzzle (logic) | **HTML** or **Paper** | Timing is not the point; logic and clarity are |
| Card game | **Paper** first | Fastest iteration by hand before touching code |
| Narrative / visual novel | **Paper** (Twine / Ink / Yarn Spinner) | Story is the mechanic — test it without code overhead |
| Strategy / 4X / city builder | **Paper** (spreadsheet sim) | Validate economy and progression rules before building |
| Roguelike (systems-heavy) | **Paper** → Engine | Validate that the ruleset is interesting before building |
| Idle / clicker / incremental | **HTML** | Turn-based logic, no feel sensitivity required |
| Rhythm game | **Paper** first (design levels in audio) | Design levels before the engine exists |
| RPG / open world | **Paper** → Engine | Systems complexity: validate rules, then validate feel |
| Horror / atmospheric | **Engine** | Atmosphere requires real rendering |

**Rule of thumb:** "Does this feel right?" → Engine. "Are these rules interesting?" → Paper. "Is this logic correct?" → HTML or Paper.

### Path: HTML (browser-playable)

**Best for:** Puzzle games, card games, turn-based strategy, word games, idle games,
top-down logic games. Anything where timing precision doesn't matter.

**Tradeoff:** fastest distribution and setup for logic-focused tests, but it cannot establish native timing/feel. The agent writes a single self-contained HTML
file the user opens in a browser — no install required.

**Limitation — browser latency lies about game feel.** Browsers introduce
50–133ms of rendering variance. This makes HTML prototypes fundamentally unreliable
for action games, platformers, fighting games, or anything where input timing,
jump arcs, or collision feel are what you're testing. If feel is the hypothesis,
use the Engine path instead.

**Alternative tools for this path:** PICO-8 (extreme constraints, great for retro
arcade concepts, web-export in one command), Phaser.js (more capable browser game
framework, still no install needed), or Twine (narrative/choice-based games).
These are faster than raw HTML for their respective genres — suggest them if appropriate.

**Output:** A single `prototype.html` (or PICO-8/Phaser equivalent) the user opens in any browser.

**Distribution — the HTML path's biggest advantage:** Unlike Engine prototypes, this
build can reach real players globally in minutes. Use this actively:
- **itch.io** — upload the file, share the link, get play counts and written feedback
  within hours. Free. The indie community plays rough builds here without expecting
  polish. This is genuine external validation at zero cost.
- **Loom + file share** — share via Google Drive/Dropbox, ask someone to record their
  screen + audio with Loom while playing. You get a video of real first-impression
  reactions and confusion without synchronous scheduling.
- **r/playmygame or r/WebGames** (Reddit) — active communities that specifically
  test early builds and give unsolicited honest feedback.
- **Game dev Discord servers** (GMTK, Brackeys, GameDev.tv) — members test each
  other's prototypes routinely; an HTML file is the easiest possible ask.

---

### Path: Engine (engine project)

**Best for:** Action games, platformers, physics-heavy games, anything where
moment-to-moment feel IS the hypothesis. Use this when HTML latency would lie about
the result.

**Tradeoff:** best fidelity for feel, with more setup and likely iterative debugging. Expect multiple rounds of iteration — this is
normal, not a failure.

**Limitation — requires engine installed and running.** This path is a
multi-turn collaborative loop:
1. Agent writes the code
2. User runs it in the engine
3. User reports errors or observations
4. Agent fixes and iterates

**Sunk cost rule:** Ask the user for elapsed time at iteration checkpoints. If they report more than 2 hours without
reaching a playable state, stop. If elapsed time is unavailable, ask; never claim to have measured it automatically. The scope is too large or the question is wrong.
Reframe the hypothesis and simplify aggressively, or switch to Paper path.

**Output:** A minimal runnable engine project in `prototypes/[name]-concept/`.

**Lighter alternative — Love2D (Lua):** If the project engine (Godot, Unity, Unreal)
feels too heavy to stand up for a throwaway build, consider Love2D — a minimal 2D
framework that installs in minutes, requires no project scaffolding, and renders
natively with no browser latency. Used by many indie devs for rapid 2D action and
platformer prototypes (Balatro prototyped in Love2D; Nuclear Throne's early builds
used it). It sits between HTML overhead and full engine overhead: heavier than
opening a browser, lighter than setting up a full engine project. Best for 2D
action/platformer feel validation when the project engine is 3D-first or takes
significant time to configure.

---

### Path: Paper (rules document + play log)

**Best for:** Strategy games, card games, board game-style mechanics, economy
systems, progression loops, any game where the logic can be simulated by hand.
Works for any genre when you need to validate rules, not feel.

**Evidence boundary:** No code, engine, or install is required, but a simulated paper session proves only that the rules can be walked through; it does not prove fun, comprehension, or reliability.

**Limitation — cannot validate moment-to-moment feel.** A simulated paper run can check that rules are executable. Only observations from real testers can support claims about comprehension, interesting decisions, fun, or a PROCEED/PIVOT/KILL recommendation.

**Paper playtest observation protocol (run this with 5+ people):**
1. Brief the rules once. Hand them the rule summary sheet. Then step back.
2. Do NOT explain further. Do NOT help. Do NOT clarify. Confusion is data.
3. Watch silently. Note every moment they slow down, re-read, or ask a question.
4. After the session, ask one question only: "What was confusing?" — not "Did you like it?"
5. Use fresh testers for each iteration. The same person cannot give new first-impression data.
6. If 3+ testers hit the same confusion point, that rule is broken — redesign it before re-testing.

**Output:** A printable rules document plus a simulated rules-walkthrough log, explicitly labelled as non-player evidence.

**Narrative tools for this path:** For dialogue-heavy and story-driven games, skip the
generic rules doc — use a dedicated narrative scripting tool instead:
- **Twine** — zero-code hypertext fiction; ideal for branching structure experiments and choice-impact testing
- **Ink** (Inkle) — plain-text scripting language used in *80 Days*, *Heaven's Vault*, and *Overboard*; exports directly to Unity and Godot
- **Yarn Spinner** — dialogue scripting used in *A Short Hike*, *DREDGE*, and *Night in the Woods*; integrates natively with Unity and Godot

All three let you write and playtest branching dialogue in minutes. Key metric for
narrative prototypes: **time to first emotional beat** — how many exchanges before
the player feels something? If it takes more than 3-4 exchanges, the opening is too slow.

---

Assess which path best fits the hypothesis, then ask the user directly with your
recommendation pre-stated:

- **Prompt**: "Which prototype path would you like to use? (Based on your concept, I'd recommend [path] — [one sentence reason].)"
- **Options**:
  - `HTML — browser prototype` — puzzle, card, turn-based, strategy, idle. Opens by double-clicking, no install. **Not suitable for action games** — browser latency lies about feel.
  - `Engine — native prototype` — action, platformer, physics, or anything where feel IS the hypothesis. Higher setup cost and iterative debugging are normal. Requires engine installed.
  - `Paper — rules document + play log` — strategy, economy, logic, board-game-style mechanics. A simulated run checks rule executability only; real testers are required for experience conclusions.

---

## Phase 4: Plan the Prototype

Define in 3–5 bullet points the minimum viable prototype:

- What is the falsifiable hypothesis?
- What is the riskiest assumption — and how does this prototype test it first?
- What is the absolute minimum needed to answer the question?
- What is explicitly cut? (menus, save systems, error handling, polish, architecture — all of it)

**Scope constraint:** A concept prototype tests ONE mechanic — not the whole game.
If scope covers more than one mechanic, cut it down. When in doubt, cut more.

Before presenting the plan, inspect the exact target directory. If it already exists, offer exactly: **extend** the related prototype, **replace in place**, or **archive then start fresh** (plus stop). Replace and archive are destructive/move operations that require separate explicit confirmation and verified source/destination paths; never silently overwrite. If the existing directory is unrelated to the same concept, stop for a new safe slug rather than treating it as a continuation.

Present this plan to the user before building. Get confirmation before proceeding.

At concept-prototype timebox checkpoints, ask the user for elapsed time. Apply
the existing one-day limit only to the user-reported elapsed value; if it is
unknown, ask rather than claiming to measure it automatically.

Once confirmed, draft (but do not write) the session checkpoint for `production/session-state/active.md`. Include concept name, hypothesis, path, scope, and current phase. The initial-build changeset in Phase 5 must preview this checkpoint together with every initial file for the selected path before either is written.

---

## Phase 5: Implement

Use two bounded write batches. Batch 1 is the initial build: preview the session checkpoint and every initial prototype file with exact paths, then obtain one authorization before writing. Batch 2 occurs after playtest/review: preview the actual REPORT, index, and applicable PIVOT/GRAVEYARD outcome files together, then obtain one authorization. If either batch gains an unlisted file, re-preview that batch; never authorize unknown content or ask file by file.

Use the same three marker lines in syntax valid for each format:
- HTML: `<!-- PROTOTYPE - NOT FOR PRODUCTION | Question: ... | Date: ... -->`
- Markdown: an HTML comment or blockquote carrying those three lines
- Engine code: that language's line/block comment syntax

After the initial-build batch is authorized, create/write its files.

Standards are intentionally relaxed:

- Hardcode values freely
- Use placeholder assets (colored rectangles, debug shapes)
- Skip error handling entirely
- Use the simplest approach that works
- Copy code rather than importing from production
- No architecture, no patterns, no abstractions

**Do not add polish.** No menus, no game over screens, no music, no tutorial text
unless the tutorial IS the mechanic being tested. Every addition beyond the
hypothesis is waste.

**Playtesting tip:** If you have access to anyone who hasn't seen the game —
friends, family, strangers online — watching them play without explanation gives
far better signal than testing it yourself. Watch silently; don't guide them.
Confusion is data. Ask one question after: "What was confusing?" Not "Did you
like it?"

**No external testers available?** Use rotation: if you built system A, you're a
naive tester for system B. In a two-person team this works well. Solo developer?
Step away for 2-3 days before playing fresh — you won't have perfect first-impression
signal, but you'll surface the worst blockers. Another option: play your own
prototype as a speedrun (force yourself through it in 5 minutes without stopping
to fix things) — the friction you feel is what strangers will hit.

**Want more granular UX data?** Ask the tester to **think aloud** as they play —
narrate their thoughts in real time: "I'm pressing space... nothing happened... is
that the jump key?" This surfaces confusion the moment it happens rather than
waiting for a post-play debrief. Best for UI/UX and onboarding clarity. Silent
observation is still better for testing raw feel; think-aloud changes how people
play slightly but gives much richer data about why they're confused.

**HTML prototype?** itch.io, Reddit (r/playmygame), and Discord (GMTK, Brackeys)
let you reach strangers today at zero cost — see the distribution options in the
HTML path section above.

**Testing AI, NPC, or complex system behavior before writing the code?** Use the
**Wizard of Oz** technique: one person plays normally while a second person secretly
controls the NPC, enemy, or system behavior in real time — making the decisions a
human would make, not an algorithm. The player believes it's automated. This lets
you validate whether your AI design *feels right* before writing a single line of
pathfinding or decision tree code. When you observe what responses the human
controller naturally produces, you learn exactly what the AI needs to do.

### Engine path: multi-turn loop

After writing the initial code:

> "The prototype files are written. Run the project in your engine now.
> If there are errors, paste them here and I'll fix them. If it runs,
> describe what you see and whether it feels like it's answering the question."

Iterate until the prototype is playable. Each loop:
1. User runs → reports errors or observations
2. Agent fixes errors or adjusts the mechanic
3. Repeat until playable or sunk cost rule triggers

### HTML path: single output

Write a single `prototype.html` to `prototypes/[concept-name]-concept/`. Include
all styles, logic, and assets inline. The file must be openable by double-clicking
with no server required.

### Paper path: document + log

Write `prototypes/[concept-name]-concept/rules.md` and `play-log.md`. Label the latter `simulated rules walkthrough — not player evidence`; it may record dice rolls, decisions, and outcomes only to test rule executability.

---

## Phase 6: Playtest Debrief

The prototype is built. Now hand it to the user and capture what they actually
experienced. Do NOT skip to report generation — the report is only as good as the
observations you collect here.

**For HTML path:** Say exactly this:
> "The prototype is ready. Open `prototypes/[name]-concept/prototype.html` in your
> browser and play it. Take as long as you need. Don't rush through it — try to
> approach it the way a new player would. Come back here when you're done."

**For Engine path:** The multi-turn iteration loop already captured errors and
behavior. Now ask for the overall assessment:
> "Now that it's running — play through it a few times as if you're the player,
> not the developer. Come back when you have a feel for it."

**For Paper path:** Say exactly this:
> "The simulated play log checks only whether the rules can be walked through. It cannot answer the experience hypothesis. Run the rules with at least one real tester and return with their observations; without that evidence the recommendation remains needs-more-validation."

Once the user returns, ask these questions **one at a time** — wait for each answer
before asking the next:

1. **Hypothesis check:**
   > "The hypothesis was: [restate the hypothesis from Phase 1]. Did it hold up —
   > CONFIRMED, PARTIALLY CONFIRMED, or REFUTED? Tell me what you saw."

2. **Best moment:**
   > "What was the moment — if any — where it felt like it was working? Be specific."

3. **Worst moment:**
   > "What was the most frustrating, confusing, or broken moment? Be specific —
   > not 'it felt slow' but 'the jump took about half a second to respond and it
   > felt like I was fighting the controls'."

4. **Surprise:**
   > "Did anything happen that you didn't expect — good or bad?"

5. **Verdict:**
   > "PROCEED, PIVOT, or KILL — and one sentence why."

Collect all answers before moving to report generation. If any answer is vague
("it felt fine", "pretty good"), ask a follow-up: "Can you be more specific?
What exactly felt fine about it?" Precise observations make the report useful.
Vague ones make it useless.

---

## Required continuation

Continue with the already-loaded [references/continued-workflow.md](references/continued-workflow.md). It contains the remaining required phases, output formats, recovery rules, and handoff instructions; execute them in order.
