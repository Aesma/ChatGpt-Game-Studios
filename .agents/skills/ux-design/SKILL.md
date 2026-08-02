---
name: ux-design
description: "Guided, section-by-section UX spec authoring for a screen, flow, or HUD. Reads game concept, player journey, and relevant GDDs to provide context-aware design guidance. Produces ux-spec.md (per screen/flow) or hud-design.md using the studio templates."
---

## Invocation and execution

Invoke this workflow as `$ux-design`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[screen/flow name] or 'hud' or 'patterns'`. Treat bracketed values as optional unless the workflow says otherwise.

Delegate substantive work to the `ux-designer` Codex subagent role when it is available. If that role is unavailable, follow the same responsibilities in the current agent.


When this skill is invoked:

## 1. Parse Arguments & Determine Mode

Three authoring modes exist based on the argument:

| Argument | Mode | Output file |
|----------|------|-------------|
| `hud` | HUD design | `design/ux/hud.md` |
| `patterns` | Interaction pattern library | `design/ux/interaction-patterns.md` |
| Any other value (e.g., `main-menu`, `inventory`) | UX spec for a screen or flow | `design/ux/[argument].md` |
| No argument | Ask the user | (see below) |

**If no argument is provided**, do not fail — ask instead. Ask the user directly:
- "What are we designing today?"
  - Options: "A specific screen or flow (I'll name it)", "The game HUD", "The interaction pattern library", "I'm not sure — help me figure it out"

If the user selects "I'll name it" or types a screen name, normalize it to a non-empty kebab-case filename segment. Reject `/`, `\\`, absolute paths, `.`, `..`, empty slugs, and the reserved slugs `hud` and `interaction-patterns`. Resolve the final path and verify it remains directly inside `design/ux/` before any read or write.

---

## 2. Gather Context (Read Phase)

Read all relevant context **before** asking the user anything. The skill's value
comes from arriving informed.

### 2a: Required Reads

- **Game concept**: Read `design/gdd/game-concept.md` — if missing, warn:
  > "No game concept found. Run `$brainstorm` first to establish the game's
  > foundation before designing UX."
  > Continue anyway if the user asks.

### 2b: Player Journey

Read `design/player-journey.md` if it exists. For each relevant section, extract:
- Which journey phase(s) does this screen appear in?
- What is the player's emotional state on arrival at this screen?
- What player need is this screen serving in the journey?
- What critical moments (from the journey map) does this screen deliver?

If the player journey file does not exist, note the gap and proceed:
> "No player journey map found at `design/player-journey.md`. Designing without it
> means we'll be making assumptions about player context. Consider running a player
> journey session after this spec is drafted."

Also add to the UX spec's Open Questions section:
> "Player journey map not yet created. Template available at `.codex/docs/templates/player-journey.md`. Run `$ux-design` Phase 2b or create it manually to establish player context for this screen."

### 2c: GDD UI Requirements

Find files matching `design/gdd/*.md` and search for `UI Requirements` sections. Read any GDD whose
UI Requirements section references this screen by name or category.

These GDD UI Requirements are the **requirements input** to this spec. Collect them
as a list of constraints the spec must satisfy.

If designing the HUD, read ALL GDD UI Requirements sections — the HUD aggregates
requirements from every system.

### 2d: Existing UX Specs

Find files matching `design/ux/*.md` and note which screens already have specs. For screens that
will link to or from the current screen, read their navigation/flow sections to
find the entry and exit points this spec must match.

### 2e: Interaction Pattern Library

If `design/ux/interaction-patterns.md` exists, read the pattern catalog index
(the list of pattern names and their one-line descriptions). Do not read full
pattern details — just the catalog. This tells you which patterns already exist
so you can reference them rather than reinvent them.

### 2f: Art Bible

Check for `design/art/art-bible.md`. If found, read the visual direction
section. UX layout must align with the aesthetic commitments already made.

### 2g: Accessibility Requirements

Check for `design/accessibility-requirements.md`. If found, read it. The spec
must satisfy the accessibility tier committed to there.

### 2h: Input Method (from Project Config)

Read `docs/technical-preferences.md` and extract the `## Input & Platform`
section. Store these values for use throughout the skill — they drive the
Interaction Map and inform accessibility requirements:

- **Input Methods** — e.g., Keyboard/Mouse, Gamepad, Touch, Mixed
- **Primary Input** — the dominant input for this game
- **Gamepad Support** — Full / Partial / None
- **Touch Support** — Full / Partial / None
- **Target Platforms** — for safe zone and aspect ratio decisions

If the section is unconfigured (`[TO BE CONFIGURED]`), ask once:
> "Input methods aren't configured yet. What does this game target?"
> Options: "Keyboard/Mouse only", "Gamepad only", "Both (PC + Console)", "Touch (mobile)", "All of the above"
>
> (Run `$setup-engine` to save this permanently so you won't be asked again.)

Store the answer for the rest of this session. Do **not** ask again per section
or per screen.

### 2i: Present Context Summary

Before any design work, present a brief summary to the user:

> **Designing: [Screen/Flow Name]**
> - Mode: [UX Spec / HUD Design / Pattern Library]
> - Journey phase(s): [from player-journey.md, or "unknown — no journey map"]
> - GDD requirements feeding this spec: [count and names, or "none found"]
> - Related screens already specced: [list, or "none yet"]
> - Known patterns available: [count, or "no pattern library yet"]
> - Accessibility tier: [from requirements doc, or "not yet defined"]
> - Input methods: [from technical-preferences.md, or "asked above"]

Then ask: "Anything else I should read before we start, or shall we proceed?"

---

## 2b. Retrofit Mode Detection

Before creating a skeleton, check if the target output file already exists.

Find files matching `design/ux/[filename].md` (where `[filename]` is the resolved output path from Phase 1).

**If the file exists — retrofit mode:**
- Read the mode's current authoritative template, then read the target file in full
- Derive the expected section headings from that template and match them exactly. Treat only explicit template placeholders as placeholders; short but real content is not empty, and existing real sections are never renamed or reordered
- Present a section status summary to the user:

> "Found existing UX spec at `design/ux/[filename].md`. Here's what's already done:
>
> | Section | Status |
> |---------|--------|
> | [section heading read from the current authoritative template] | [Complete / Empty / Placeholder] |
> | ... | ... |
>
> I'll work on the [N] incomplete sections only — existing content will not be overwritten."

- Skip Section 3 (skeleton creation) — the file already exists
- In Phase 4 (Section Authoring), only work on sections with Status: Empty or Placeholder
- Edit the file to fill placeholders in-place rather than creating a new skeleton

**If the file does not exist — fresh authoring mode:**
Proceed to Phase 3 (Create File Skeleton) as normal.

---

## 3. Create File Skeleton

Select the existing authoritative template for the mode: `.codex/docs/templates/ux-spec.md`, `.codex/docs/templates/hud-design.md`, or `.codex/docs/templates/interaction-pattern-library.md`. Read it at runtime and instantiate that complete template by replacing only its placeholders; do not maintain or use a copied section skeleton.

Before the first write, preview the concrete UX target, `production/session-state/active.md`, and—when the current spec is already known to require a new/revised pattern—`design/ux/interaction-patterns.md`. State the full intent: create the template skeleton, replace placeholders section by section, persist user-approved pattern entries before first review, and update this task's session state while preserving unrelated content. Obtain one boundary authorization; later section Approval is design-content approval, not another file-write approval. An unpreviewed pattern-library path uses the existing scope-expansion rule.

---

### Template instantiation by mode

- Screen/flow: read and instantiate `.codex/docs/templates/ux-spec.md` in full.
- HUD: read and instantiate `.codex/docs/templates/hud-design.md` in full.
- Patterns: read and instantiate `.codex/docs/templates/interaction-pattern-library.md` in full.

Keep every required heading and instruction from the selected template. Replace placeholders only as sections are approved; never copy a reduced heading list into this workflow.
---

After writing the skeleton, update `production/session-state/active.md` with:
- Task: Designing [screen/flow name] UX spec
- Current section: Starting (skeleton created)
- File: design/ux/[filename].md

---

## Required continuation

Before continuing, read [references/continued-workflow.md](references/continued-workflow.md) in full. It contains the remaining required phases, output formats, recovery rules, and handoff instructions; execute them in order.
