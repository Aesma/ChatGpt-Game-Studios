# ChatGPT Game Studios -- Complete Workflow Guide

> Compatibility authority: machine routing and stage detection use the versioned `cgs.workflow-catalog/v2` record at `.codex/docs/workflow-catalog.yaml` and its schema at `.codex/docs/schemas/workflow-catalog-v2.md`. This guide is explanatory. If prose and the current catalog version disagree, automation fails closed; it does not infer completion or stage from file presence.


> **How to go from zero to a shipped game using the Agent Architecture.**
>
> This guide walks you through every phase of game development using the
> 49-subagent system, 74 skills, and 12 registered hook handlers across 8 events. It assumes you
> have Codex installed and are working from the project root.
>
> The pipeline has 7 phases. Each adjacent transition has a read-only gate
> assessment (`$gate-check <transition-id>`). A passing gate record is evidence,
> not stage mutation. The authoritative phase sequence and external-recorder
> boundary are defined in `.codex/docs/workflow-catalog.yaml` and read by `$help`.
>
> A bare `$skill-name` in prose, a heading, table, or flow diagram is only a
> workflow label, not an executable invocation. Copyable command templates below
> include every required mode/flag and leave caller-supplied values in
> `<placeholders>`; unresolved templates return input-required and must not run.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Phase 1: Concept](#phase-1-concept)
3. [Phase 2: Systems Design](#phase-2-systems-design)
4. [Phase 3: Technical Setup](#phase-3-technical-setup)
5. [Phase 4: Pre-Production](#phase-4-pre-production)
6. [Phase 5: Production](#phase-5-production)
7. [Phase 6: Polish](#phase-6-polish)
8. [Phase 7: Release](#phase-7-release)
9. [Cross-Cutting Concerns](#cross-cutting-concerns)
10. [Appendix A: Agent Quick-Reference](#appendix-a-agent-quick-reference)
11. [Appendix B: Skill Quick-Reference](#appendix-b-skill-quick-reference)
12. [Appendix C: Common Workflows](#appendix-c-common-workflows)

---

## Quick Start

### What You Need

Before you start, make sure you have:

- **Codex** installed and working
- **Git** with Git Bash (Windows) or standard terminal (Mac/Linux)
- **jq** (optional but recommended -- hooks fall back to `grep` if missing)
- **Python 3** (optional -- some hooks use it for JSON validation)

### Step 1: Clone and Open

```bash
git clone <repo-url> my-game
cd my-game
```

### Step 2: Run $start

If this is your first session:

```
$start
```

This guided onboarding asks where you are and routes you to the right phase:

- **Path A** -- No idea yet: routes to `$brainstorm`
- **Path B** -- Vague idea: routes to `$brainstorm` with seed
- **Path C** -- Clear concept: routes to `$setup-engine` and `$map-systems`
- **Path D1** -- Existing project, few artifacts: normal flow
- **Path D2** -- Existing project, GDDs/ADRs exist: runs `$project-stage-detect`
  then `$adopt` for brownfield migration

### Step 3: Verify Hooks Are Working

Start a new Codex task. You should see output from the
`session-start.sh` hook:

```
=== ChatGPT Game Studios -- Session Context ===
Branch: main
Recent commits:
  abc1234 Initial commit
===================================
```

If you see this, hooks are working. If not, check `.codex/hooks.json` to
make sure the hook paths are correct for your OS.

### Step 4: Ask for Help Anytime

At any point, run:

```
$help
```

This resolves current stage from the catalog-declared authority record at
`production/stage/authority.json`, validates its receipt chain, and tells you
what to do next. `production/stage.txt` is only a legacy declaration and never
authoritative. Missing or invalid authority remains UNKNOWN; artifact presence
does not initialize or advance stage.

### Step 5: Create Your Directory Structure

Directories are created as needed. The system expects this layout:

```
src/                  # Game source code
  core/               # Engine/framework code
  gameplay/           # Gameplay systems
  ai/                 # AI systems
  networking/         # Multiplayer code
  ui/                 # UI code
  tools/              # Dev tools
assets/               # Game assets
  art/                # Sprites, models, textures
  audio/              # Music, SFX
  vfx/                # Particle effects
  shaders/            # Shader files
  data/               # JSON config/balance data
design/               # Design documents
  gdd/                # Game design documents
  narrative/          # Story, lore, dialogue
  levels/             # Level design documents
  balance/            # Balance spreadsheets and data
  ux/                 # UX specifications
docs/                 # Technical documentation
  architecture/       # Architecture Decision Records
  api/                # API documentation
  postmortems/        # Post-mortems
tests/                # Test suites
prototypes/           # Throwaway prototypes
production/           # Sprint plans, milestones, releases
  sprints/
  milestones/
  releases/
  epics/              # Epic and story files (from $create-epics + $create-stories)
  playtests/          # Canonical playtest sessions: <session-id>/report.md
  session-state/      # Ephemeral session state (gitignored)
  session-logs/       # Session audit trail (gitignored)
```

> **Tip:** You do not need all of these on day one. Create directories as you
> reach the phase that needs them. The important thing is to follow this
> structure when you do create them, because the **rules system** enforces
> standards based on file paths. Code in `src/gameplay/` gets gameplay rules,
> code in `src/ai/` gets AI rules, and so on.

---

## Phase 1: Concept

### What Happens in This Phase

You go from "no idea" or "vague idea" to a structured game concept document
with defined pillars and a player journey. This is where you figure out
**what** you are making and **why**.

### Phase 1 Pipeline

```text
$brainstorm <request-manifest-path>
  --> game-concept.md + cgs.brainstorm-authoring-receipt/v1
       |--> optional external cgs.concept-approval/v1
       |--> optional $prototype <concept-or-question> --path <html|engine|paper>
       |--> $map-systems
       |     --> design/gdd/systems-index.md
       +--> $setup-engine --manifest <engine-request-path>
```

### Step 1.1: Brainstorm With $brainstorm

This is your starting point. Run the brainstorm skill:

```
$brainstorm <request-manifest-path>
```

Or with a genre hint:

```
$brainstorm <request-manifest-path>
```

Put any seed such as “roguelike deckbuilder” inside the exact
`cgs.brainstorm-request/v2` manifest; positional seed text is not accepted.

**What happens:** The brainstorm skill guides you through a collaborative 6-phase
ideation process using professional studio techniques:

1. Asks about your interests, themes, and constraints
2. Generates 10 concept seeds with MDA (Mechanics, Dynamics, Aesthetics) analysis
3. You pick 2-3 favorites for deep analysis
4. Performs player motivation mapping and audience targeting
5. You choose the winning concept
6. Formalizes it into `design/gdd/game-concept.md`

The concept document includes:

- Elevator pitch (one sentence)
- Core fantasy (what the player imagines themselves doing)
- MDA breakdown
- Target audience (Bartle types, demographics)
- Core loop diagram
- Unique selling proposition
- Comparable titles and differentiation
- Game pillars (3-5 non-negotiable design values)
- Anti-pillars (things the game intentionally avoids)

### Step 1.2: Review the Concept (Optional but Recommended)

Use a separately authorized independent concept-review process. If it persists
an approval, require a version-bound `cgs.concept-approval/v1` record for the exact
concept. No P1 project skill produces this record: `$design-review` accepts
system GDDs only and must not be routed to `design/gdd/game-concept.md`. If no
independent reviewer/recorder is available, report the approval as UNKNOWN.

### Step 1.3: Choose Your Engine

```
$setup-engine --manifest <engine-request-path>
```

Or with a specific engine:

```
$setup-engine --manifest <engine-request-path>
```

The requested product/version and operation belong inside the version-bound engine
request manifest; positional engine/version arguments are not accepted.

**What $setup-engine does:**

- Populates `.codex/docs/technical-preferences.md` with naming conventions,
  performance budgets, and engine-specific defaults
- Detects knowledge gaps (engine version newer than LLM training data) and
  advises cross-referencing `docs/engine-reference/`
- Creates version-pinned reference docs in `docs/engine-reference/`

**Why this matters:** Once you set the engine, the system knows which
engine-specialist agents to use. If you pick Godot, agents like
`godot-specialist`, `godot-gdscript-specialist`, and `godot-shader-specialist`
become your go-to experts.

### Step 1.4: Decompose Your Concept Into Systems

Before writing individual GDDs, enumerate all the systems your game needs:

```
$map-systems
```

This creates `design/gdd/systems-index.md` -- a master tracking document that:

- Lists every system your game needs (combat, movement, UI, etc.)
- Maps dependencies between systems
- Assigns priority tiers (MVP, Vertical Slice, Alpha, Full Vision)
- Determines design order (Foundation > Core > Feature > Presentation > Polish)

This step is **required** before proceeding to Phase 2. Research from 155 game
postmortems confirms that skipping systems enumeration costs 5-10x more in
production.

### Phase 1 Gate

```
$gate-check concept-to-systems-design
```

**Normative gate contract (`gate.concept-to-systems-design/v2`):**

- `CSD-A01`, `CSD-Q01`, and `CSD-Q02` evaluate the exact current
  `design/gdd/game-concept.md` path and declared revision and its substantive concept,
  pillar, and Visual Identity Anchor content; file presence alone never passes.
- `CSD-M01/v1` requires the accountable owner attestation bound to the same
  concept and scope revisions are still current.
- The concept-prototype row `CSD-R01` is advisory and optional. Its absence may
  produce CONCERNS but is not a blocking pass requirement.
- Only a current conversation-produced `cgs.gate-record/v2` bound to this exact
  transition/profile versions and dependency identities, with PASS, COMPLETE coverage, and
  ELIGIBLE disposition, may be considered by the external stage recorder.

**Verdict:** PASS / CONCERNS / FAIL / PARTIAL. Only PASS with COMPLETE coverage,
ELIGIBLE disposition, and current evidence may be considered by the separately
configured external stage recorder. The gate itself never advances stage.

---

## Phase 2: Systems Design

### What Happens in This Phase

You create all the design documents that define how your game works. Nothing
gets coded yet -- this is pure design. Each system identified in the systems
index gets its own GDD, authored section by section, reviewed individually,
and then all GDDs are cross-checked for consistency.

### Phase 2 Pipeline

```
$map-systems next  -->  $design-system <system-name-or-gdd-path> --mode new  -->  $design-review <path-to-system-gdd> --depth lean
       |                     |                     |
       v                     v                     v
  Picks next system    Section-by-section     Validates 8
  from systems-index   GDD authoring          required sections
                       (incremental writes)   APPROVED/NEEDS REVISION
       |
       |  (repeat for each MVP system)
       v
$review-all-gdds
       |
       v
  Cross-GDD consistency + design theory review
  PASS / CONCERNS / FAIL
```

### Step 2.1: Author System GDDs

Design each system in dependency order using the guided workflow:

```
$map-systems next
```

This picks the highest-priority undesigned system and hands off to
`$design-system`, which guides you through creating its GDD section by section.

You can also design a specific system directly:

```
$design-system combat-system
```

**What $design-system does:**

1. Reads your game concept, systems index, and any upstream/downstream GDDs
2. Runs a Technical Feasibility Pre-Check (domain mapping + feasibility brief)
3. Walks you through each of the 8 required GDD sections one at a time
4. Each section follows: Context > Questions > Options > Decision > Draft > content acceptance
5. Accepted sections are persisted within the single bounded changeset authorization (survives crashes without repeated write prompts)
6. Flags conflicts with existing approved GDDs
7. Routes to specialist agents per category (systems-designer for math,
   economy-designer for economy, narrative-director for story systems)

**The 8 required GDD sections:**

| # | Section | What Goes Here |
|---|---------|---------------|
| 1 | **Overview** | One-paragraph summary of the system |
| 2 | **Player Fantasy** | What the player imagines/feels when using this system |
| 3 | **Detailed Rules** | Unambiguous mechanical rules |
| 4 | **Formulas** | Every calculation, with variable definitions and ranges |
| 5 | **Edge Cases** | What happens in weird situations? Explicitly resolved. |
| 6 | **Dependencies** | What other systems this connects to (bidirectional) |
| 7 | **Tuning Knobs** | Which values designers can safely change, with safe ranges |
| 8 | **Acceptance Criteria** | How do you test that this works? Specific, measurable. |

Plus a **Game Feel** section: feel reference, input responsiveness (ms/frames),
animation feel targets (startup/active/recovery), impact moments, weight profile.

### Step 2.2: Review Each GDD

Before the next system starts, validate the current one:

```
$design-review design/gdd/combat-system.md
```

Checks all 8 sections for completeness, formula clarity, edge case resolution,
bidirectional dependencies, and testable acceptance criteria.

**Verdict:** APPROVED / NEEDS REVISION / MAJOR REVISION. Only APPROVED GDDs
should proceed. The review command returns a conversation-only
`cgs.review-evidence/v1` envelope with a `cgs.design-review/v2` extension; it
does not persist gate evidence. A required catalog step becomes complete only
after an independent external persistence owner stores the exact envelope
byte-for-byte and verifies read-back/currentness; the final
`PA-DESIGN-REVIEW-1` adapter consumes that persisted envelope. No generic
recorder receipt is synthesized.

### Step 2.3: Small Changes Without Full GDDs

For tuning changes, small additions, or tweaks that do not warrant a full GDD:

```
$quick-design propose "<change>" --change-id <QD-stable-id> --version <vNNN> --target <design/gdd/system-slug.md> --target-id <SYS-stable-id> --section "<exact-level-two-heading>"
```

This creates a lightweight spec in `design/quick-specs/` instead of a full
8-section GDD. Use it for tuning, number changes, and small additions.

### Step 2.4: Cross-GDD Consistency Review

After all MVP system GDDs are approved individually:

```
$review-all-gdds
```

This reads ALL GDDs simultaneously and runs two analysis phases:

**Phase 1 -- Cross-GDD Consistency:**
- Dependency bidirectionality (A references B, does B reference A?)
- Rule contradictions between systems
- Stale references to renamed or removed systems
- Ownership conflicts (two systems claiming the same responsibility)
- Formula range compatibility (does System A's output fit System B's input?)
- Acceptance criteria cross-check

**Phase 2 -- Design Theory (Game Design Holism):**
- Competing progression loops (do two systems fight for the same reward space?)
- Cognitive load (more than 4 active systems at once?)
- Dominant strategies (one approach that makes all others irrelevant)
- Economic loop analysis (sources and sinks balanced?)
- Difficulty curve consistency across systems
- Pillar alignment and anti-pillar violations
- Player fantasy coherence

**Output:** `design/gdd/gdd-cross-review-[date].md` with a verdict.

### Step 2.5: Narrative Design (If Applicable)

If your game has story, lore, or dialogue, this is when you build it:

1. **World-building** -- Use `world-builder` to define factions, history,
   geography, and rules of your world
2. **Story structure** -- Use `narrative-director` to design story arcs,
   character arcs, and narrative beats
3. **Character sheets** -- Use the `narrative-character-sheet.md` template

### Phase 2 Gate

```
$gate-check systems-design-to-technical-setup
```

**Normative gate contract (`gate.systems-design-to-technical-setup/v2`):**

- `SDT-A01`, `SDT-A02`, `SDT-Q01`, and `SDT-Q02` bind the current
  systems-index path and declared revision and every exact MVP GDD path and declared revision from that
  manifest; filenames, status text, or counts alone never pass.
- Every MVP GDD needs current `PA-DESIGN-REVIEW-1` PASSING evidence: the
  byte-identical persisted `cgs.review-evidence/v1` envelope with its
  `cgs.design-review/v2` producer extension, exact target path and revision, complete finding
  set, and `APPROVED`. This is `PERSISTED_ENVELOPE_COMPLETE`; unpersisted,
  solo/advisory, NEEDS REVISION, or stale evidence is ineligible.
- `SDT-E02` needs persisted/read-back `cgs.review-evidence/v1` plus
  `cgs.cross-gdd-review/v2`, bound to the complete current MVP manifest and all
  producer/ruleset/bundle versions, full coverage, and PASS. CONCERNS does not
  pass this profile.
- The resulting `cgs.gate-record/v2` must bind the exact profile and source
  versions and report PASS, COMPLETE coverage, and ELIGIBLE disposition.

---

## Phase 3: Technical Setup

### What Happens in This Phase

You make key technical decisions, document them as Architecture Decision Records
(ADRs), validate them through review, and produce a control manifest that
gives programmers flat, actionable rules. You also establish UX foundations.

### Phase 3 Pipeline

```
create-architecture workflow  -->  architecture-decision workflow (x N)  -->  architecture-review workflow
        |                          |                                   |
        v                          v                                   v
  Master architecture       Per-decision ADRs              Validates completeness,
  document covering         in docs/architecture/          dependency ordering,
  all systems               adr-*.md                       engine compatibility
                                                                      |
                                                                      v
                                                         create-control-manifest workflow
                                                                      |
                                                                      v
                                                         Flat programmer rules
                                                         docs/architecture/
                                                         control-manifest.md
        Also in this phase:
        -------------------
        ux-design workflow  -->  ux-review workflow
        Accessibility requirements doc
        Interaction pattern library
```

### Step 3.1: Master Architecture Document

```
$create-architecture new
```

Creates the overarching architecture document in `docs/architecture/architecture.md`
covering system boundaries, data flow, and integration points.

### Step 3.2: Architecture Decision Records (ADRs)

For each significant technical decision:

```
$architecture-decision <architecture-decision-request-manifest-path>
```

**What happens:** The skill guides you through creating an ADR with:
- Context and decision drivers
- All options with pros/cons and engine compatibility
- Chosen option with rationale
- Consequences (positive, negative, risks)
- Dependencies (Depends On, Enables, Blocks, Ordering Note)
- GDD Requirements Addressed (linked by TR-ID)

ADRs go through a lifecycle: Proposed > Accepted > Superseded/Deprecated.
The authoring workflow persists `cgs.adr-authoring-receipt/v1`, but it does not
accept its own ADR. Gate-eligible completion additionally requires a current
`cgs.adr-lifecycle-record/v1` from the independent external ADR lifecycle
recorder, bound to the exact authoring receipt and ADR content revision.

**Minimum 3 Foundation-layer ADRs are required** before the gate check.

**Retrofitting existing ADRs:** If you already have ADRs from a brownfield
project:

```
$architecture-decision <architecture-decision-request-manifest-path>
```

Set `operation: retrofit` in the request manifest and bind the exact existing ADR
path and current declared revision. The workflow then detects missing sections without
silently overwriting existing content.

### Step 3.3: Architecture Review

```
$architecture-review
```

Validates all ADRs together:
- Topological sort of ADR dependencies (detects cycles)
- Engine compatibility verification
- GDD Revision Flags (flags GDD sections that need updates based on ADR choices)
- TR-ID registry maintenance (`docs/architecture/tr-registry.yaml`)

### Step 3.4: Control Manifest

```
$create-control-manifest new
```

Takes all Accepted ADRs and produces a flat programmer rules sheet:

```
docs/architecture/control-manifest.md
```

This contains Required patterns, Forbidden patterns, and Guardrails organized
by code layer. Stories created later embed the manifest version date so
staleness can be detected.

### Step 3.5: Accessibility Requirements

Create `design/accessibility-requirements.md` using the template. Commit to a
tier (Basic / Standard / Comprehensive / Exemplary) and fill the 4-axis feature
matrix (visual, motor, cognitive, auditory).

This document is required in Phase 3 because UX specs (written in Phase 4)
reference this tier — it is a design prerequisite, not a UX deliverable.

### Phase 3 Gate

```
$gate-check technical-setup-to-pre-production
```

**Normative gate contract (`gate.technical-setup-to-pre-production/v2`):**

- `TSP-A01` through `TSP-A04` and `TSP-Q01` through `TSP-Q03` validate the
  fixed technical-preferences, Art Bible, accessibility, interaction-pattern,
  architecture, traceability, control, engine-reference, test-root, canary, and
  CI paths by exact current declared revision. Presence or an ADR count alone does not
  pass; the authoritative manifest must bind the required Foundation ADR IDs,
  paths, versions, lifecycle state, engine version, and traceability.
- `TSP-E01` requires a persisted current `PA-ARCH-REVIEW-1` report with exact
  target-manifest and source revisions, every required reviewer complete, mutation
  guard passing, and verdict PASS.
- `TSP-Q03` requires the configured canary's exact schema/versioned runner
  receipt, command, source/config revisions, current execution identity, and
  conclusive PASS; source presence or exit code alone is insufficient.
- Only a current `cgs.gate-record/v2` for this exact profile with PASS,
  COMPLETE coverage, and ELIGIBLE disposition can reach the external recorder.

---

## Phase 4: Pre-Production

### What Happens in This Phase

You create UX specs for key screens, prototype risky mechanics, turn design
documents into implementable stories, plan your first sprint, and build a
Vertical Slice that proves the core loop is fun.

### Phase 4 Pipeline

```
ux-design workflow  -->  vertical-slice workflow  -->  create-epics workflow  -->  create-stories workflow  -->  sprint-plan workflow
    |                   |                   |                   |                       |
    v                   v                   v                   v                       v
  UX specs       Production-quality   Epic files in       Story files in          First sprint with
  design/ux/     end-to-end build     production/         production/             prioritized stories
                 in prototypes/       epics/*/EPIC.md     epics/*/story-*.md      production/sprints/
                 PROCEED/PIVOT/KILL   (one per module)    (one per behaviour)     sprint-*.md
    |                                                          |
    v                                                          v
 ux-review workflow                                     story-readiness workflow
 (validates specs                                       (validates each story
  before epics)                                          conversation candidate)
                                                               |
                                                               v
                                                    independent external recorder
                                                (cgs.story-readiness-recorder/v1;
                                                  not a project skill or command)
                                                               |
                                                               v
                                               persisted READY record + exact
                                        cgs.story-readiness-recorder-receipt/v1
                                       (RECORDED or ALREADY_RECORDED; exact
                                        record/receipt/declared revisions current;
                                        implementation_gate_eligible: true)
                                                               |
                                                               v
                                                           dev-story workflow
                                                     (consumes the current persisted
                                                       READY record/receipt pair)
```

### Step 4.1: UX Specs for Key Screens

Before writing epics, create UX specs so that story authors know what screens
exist and what player interactions they must support.

**UX Specs:**

```
$ux-design --manifest <main-menu-request-path>
$ux-design --manifest <core-gameplay-hud-request-path>
```

Three modes: screen/flow, HUD, and interaction patterns. Output goes to
`design/ux/`. Each spec includes: player need, layout zones, states,
interaction map, data requirements, events fired, accessibility, localization.

Reads your `accessibility-requirements.md` (written in Phase 3) and your
input method config from `technical-preferences.md` to drive accessibility
and input coverage checks — no need to re-specify them per screen.

> **Tip:** `$design-system` emits a 📌 UX Flag for every system with UI
> requirements. Use those flags as a checklist for which screens need specs.

**Interaction Pattern Library:**

```
$ux-design --manifest <interaction-pattern-library-request-path>
```

Create `design/ux/interaction-patterns.md` — 16 standard controls plus
game-specific patterns (inventory slot, ability icon, HUD bar, dialogue box,
etc.) with animation and sound standards.

**UX Review:**

```
$ux-review all
```

Validates UX specs for GDD alignment and accessibility tier compliance.
Produces a conversation-only `cgs.review-evidence/v1` envelope with a
`cgs.ux-review/v2` extension and an APPROVED / NEEDS REVISION / MAJOR REVISION
NEEDED verdict. The producer fixes `gate_evidence_status: NOT_PERSISTED` and
`gate_evidence_eligible: false`. This is candidate-only conversation completion
for downstream workflow routing, never persisted or gate completion. The final
gate adapter authorizes no current durable UX recorder schema, so
Pre-Production → Production remains
`BLOCKED_PENDING_VERSIONED_RECORDER`; no wrapper may rewrite the embedded
candidate fields or make that candidate gate eligible.

### Step 4.2: Build the Vertical Slice

The vertical slice is the production-quality proof that you can build the full
game loop end-to-end before committing to full Production.

Plan and evaluate in separate tasks; implementation/build/playtest evidence belongs
to separately authorized owners:

```
$vertical-slice plan --request <project-relative-plan-request>
$vertical-slice evaluate --request <project-relative-evaluation-request> --persist
$vertical-slice status --report <project-relative-report>
```

**What it proves:** Does a player, starting from nothing, experience the core
fantasy within a few minutes, without developer guidance?

**What it builds:** A near-production-quality playable build covering at least
one complete [start → challenge → resolution] cycle. Uses real architecture
layers, real naming conventions, no hardcoded values — but not final art or
audio. This is not a throwaway like the concept prototype; it demonstrates
production pipeline feasibility.

**Note on concept prototyping:** If you ran `$prototype` in Phase 1 (Concept),
you already validated the core idea is fun. The vertical slice now validates
you can build it properly. They answer different questions. If you skipped the
concept prototype, now is a reasonable time to run one first before investing
in the full slice.

**Verdict:** An independent evaluator derives the evidence verdict; directors can
add creative concerns but cannot upgrade evidence. Only a separately recorded user
product decision can make the final decision. Downstream work may consume PROCEED
only from an exact current persisted report whose complete candidate/source/build/
scope/evidence/playtest/velocity graph revalidates.

### Step 4.3: Create Epics and Stories From Design Artifacts

```
$create-epics <foundation-request-manifest-path>
$create-stories author <epic-path> --epic-receipt <epic-receipt-path>
$create-epics <core-request-manifest-path>
$create-stories author <epic-path> --epic-receipt <epic-receipt-path>
```

`$create-epics` reads your GDDs, ADRs, and architecture to define epic scope —
one epic per architectural module. Then `$create-stories` breaks each epic into
implementable story files in `production/epics/[slug]/`. Each story embeds:
- GDD requirement references (TR-IDs, not quoted text -- stays fresh)
- ADR references (only from Accepted ADRs; Proposed ADRs cause `Status: Blocked`)
- Control manifest version date (for staleness detection)
- Engine-specific implementation notes
- Acceptance criteria from the GDD

Once stories exist, validate the selected story and use the independent external
recorder to obtain its current persisted `cgs.story-readiness-record/v1` READY
record plus exact `cgs.story-readiness-recorder-receipt/v1`. Require `RECORDED`
or `ALREADY_RECORDED`, exact record/receipt identities and revisions and currentness, and
`implementation_gate_eligible: true`. Only then run
`$dev-story --request <project-relative-request-path>` to
implement one — it routes
automatically to the correct programmer agent.

### Step 4.4: Validate Stories Before Pickup

```
$story-readiness --story <project-relative-story-path>
```

Checks: Design completeness, Architecture coverage, Scope clarity, Definition
of Done. Verdict: READY / NEEDS WORK / BLOCKED.

That verdict is a conversation candidate, not pickup authorization. An
independent external `cgs.story-readiness-recorder/v1`—not a project skill or
`$` command—must persist the exact READY candidate. Pickup requires the current
persisted `cgs.story-readiness-record/v1` plus its exact
`cgs.story-readiness-recorder-receipt/v1`, bound to the story, registry, source
paths and declared revisions, ruleset, check rows, candidate/record/receipt identities, and
current staleness key. Only `RECORDED` or `ALREADY_RECORDED` with
`implementation_gate_eligible: true` qualifies; NEEDS WORK, BLOCKED, partial,
stale, or unpersisted evidence never makes a story ready for implementation.

### Step 4.5: Effort Estimation

```
$estimate story --basis relative --input <project-relative-story-path>
```

Provides effort estimates with risk assessment.

### Step 4.6: Plan Your First Sprint

```
$sprint-plan new
```

**What happens:** The `producer` agent collaborates on sprint planning:
- Asks for sprint goal and available time
- Breaks the goal into Must Have / Should Have / Nice to Have tasks
- Identifies risks and blockers
- Creates `production/sprints/sprint-01.md`
- Populates `production/sprint-status.yaml` (machine-readable story tracking)

### Step 4.7: Vertical Slice (Hard Gate)

Before advancing to Production, build and validate a Vertical Slice when that
scope is selected:

- One complete end-to-end core loop, playable from start to finish
- Representative quality (not placeholder everything)
- Played unguided in the required distinct sessions
- Each counted session has a canonical completed result at
  `production/playtests/<session-id>/report.md`

`$gate-check` is authoritative only for its read-only gate assessment; it never
mutates stage. The assessment accepts only an explicitly supplied, externally
version-bound `vertical-slice-evaluation-report`
whose declared workflow/evidence/product/final states are COMPLETE/PROCEED, whose persistence
and currentness verify, and whose full referenced graph still matches. Session or
file existence alone never passes.

### Phase 4 Gate

```
$gate-check pre-production-to-production
```

**Current normative gate status
(`gate.pre-production-to-production/v2`): `BLOCKED_PENDING_VERSIONED_RECORDER`.**

- `PPP-E03` requires current PASSING `PA-UX-REVIEW-1` evidence for the main
  menu, applicable core HUD, and pause menu. The final adapter has no PASSING
  state under the current producer and authorizes no durable recorder schema:
  an APPROVED conversation candidate is incomplete, while NEEDS REVISION is
  failing. Both retain `NOT_PERSISTED` and `gate_evidence_eligible: false`.
- UX `CONVERSATION_COMPLETE` may satisfy only the catalog's declared non-gate
  downstream routing prerequisite. It cannot satisfy `PPP-E03`, make a
  `cgs.gate-record/v2` ELIGIBLE, or clear the transition blocker. No wrapper may
  rewrite the embedded UX evidence fields.
- If a future final producer and gate adapter jointly authorize an exact
  versioned recorder, `PPP-E01` still requires the explicit persisted
  `cgs.vertical-slice-evaluation-report/v2` with its complete current
  plan/source/candidate/build/scope/session/network/velocity/decision graph,
  declared revisions, `Persistence: VERIFIED`, `Gate Eligible: YES`, and all verdict
  axes PROCEED.
- `PPP-A01`, `PPP-A02`, `PPP-A03`, and `PPP-Q01` still require exact current
  sprint/control/epic/story/GDD/ADR/UX/build manifest paths and declared revisions;
  existence, filenames, or counts do not pass. `PPP-E02` separately requires
  current PASSING `PA-ART-BIBLE-1` external evidence, and `PPP-M01/v1` requires
  the accountable owner attestation bound to the exact build/report/scope
  identities.
- `PPP-R01` playtest evidence is advisory: when supplied it must be a current
  `PA-PLAYTEST-1` pair—`cgs.playtest-report/v2` plus
  `cgs.playtest-report-recorder-receipt/v1`—for the exact slice build, with
  state `RECORDED COMPLETED — GATE ELIGIBLE`. Its absence is CONCERNS, not a
  substitute for `PPP-M01`.
- A concept prototype is optional/advisory and is not a Phase 4 pass
  requirement.

---

## Phase 5: Production

### What Happens in This Phase

This is the core production loop. You work in sprints (typically 1-2 weeks),
implementing features story by story, tracking progress, and closing stories
through a structured completion review. This phase repeats until your game
is content-complete.

### Phase 5 Pipeline (Per Sprint)

```text
$sprint-plan new
  --> $story-readiness --story <project-relative-story-path>
  --> independent external cgs.story-readiness-recorder/v1
      (not a project skill or $ command)
  --> persisted cgs.story-readiness-record/v1 READY
      + cgs.story-readiness-recorder-receipt/v1
      (RECORDED or ALREADY_RECORDED; exact record/receipt/declared revisions current;
       implementation_gate_eligible: true)
  --> $dev-story --request <project-relative-request-path>
  --> $code-review --target <project-relative-file-or-directory>
  --> independent external cgs.code-review-recorder-receipt/v1
  --> $story-done <story-file-path>

$sprint-status
$scope-check compare --baseline <approved-scope-path> --current <current-scope-path>
$retrospective sprint:<sprint-id>
```

### Step 5.1: The Story Lifecycle

The production lifecycle separates immutable planning inputs from tracker-owned state:

```text
$story-readiness --story <project-relative-story-path>
  --> independent external cgs.story-readiness-recorder/v1
      (not a project skill or $ command)
  --> persisted cgs.story-readiness-record/v1 READY
      + cgs.story-readiness-recorder-receipt/v1
      (RECORDED or ALREADY_RECORDED; exact record/receipt/declared revisions current;
       implementation_gate_eligible: true)
  --> $dev-story --request <project-relative-request-path>
  --> $code-review --target <project-relative-file-or-directory>
  --> independent external cgs.code-review-recorder-receipt/v1
  --> $story-done <story-file-path>
  --> next eligible tracker row
```

- The story file is an immutable requirement core during implementation and closure.
- The sprint plan owns `plan revision and story-set revision`. Implementation and closure MUST NOT recompute or rewrite them.
- `$story-readiness` emits only a NOT_PERSISTED conversation candidate. The
  independent external recorder must persist the exact READY record and emit
  its valid receipt; `$dev-story` consumes only that current record/receipt pair
  after independently verifying `RECORDED` or `ALREADY_RECORDED`, all bound raw
  versions/currentness, and `implementation_gate_eligible: true`.
- `$dev-story` produces version-bound implementation and test evidence and requests a canonical lifecycle update through the tracker recorder.
- `$code-review` returns a current `cgs.review-evidence/v1` envelope with a
  `cgs.code-review/v2` extension, but that producer output is `NOT_PERSISTED` and
  not gate eligible. A separately authorized independent external recorder must
  persist and bind it through `cgs.code-review-recorder-receipt/v1`; the
  code-review skill never creates or invokes that receipt.
- The canonical lifecycle owner updates only the matching row in `cgs.sprint-tracker/v2`, using a revision check against the current tracker revision and emitting its proposal/result/receipt chain.
- `$story-done` verifies the immutable story core, current tracker row in `IN_REVIEW`, exact dev result/transition receipt, independent readiness/review/QA/test evidence, and all source revisions. If eligible, it requests the tracker recorder to move only that row to the catalog-declared completed state.
- A failed transaction restores the original tracker bytes; it does not partially update story, plan, session, or planning records. The persisted recorder receipt is the lifecycle evidence.
- COMPLETE/BLOCKED summaries do not themselves change canonical state, and no skill selects a newest tracker or receipt.

Use each skill's exact manifest-based invocation. Tech-debt findings are proposals until their owning recorder accepts them.

### Step 5.2: Sprint Tracking

Check progress anytime:

```
$sprint-status
```

Quick 30-line snapshot reading from `production/sprint-status.yaml`.

If scope is growing:

```
$scope-check compare --baseline <approved-scope-path> --current production/sprints/sprint-03.md
```

This compares current scope against the original plan and flags scope increase,
recommends cuts.

### Step 5.3: Content Tracking

```
$content-audit
```

Compares GDD-specified content against what has been implemented. Catches
content gaps early.

### Step 5.4: Design Change Propagation

When a GDD changes after stories have been created:

```
$propagate-design-change <request-manifest-path>
```

Git-diffs the GDD, finds affected ADRs, generates an impact report, and
walks you through Superseded/update/keep decisions.

### Step 5.5: Multi-System Features (Team Orchestration)

Team workflows do not share a universal phase count, review-mode flag, or implementation authority. Each team skill's own manifest, prerequisites, ownership, and receipts control the run.

Examples:

```
$team-combat --request <request-path>
$team-narrative --manifest <request-path> [--resume <checkpoint-path>]
$team-ui --manifest <ui-request-path> [--resume <checkpoint-path>]
$team-level <level-id>
$team-audio --manifest <request-path> [--resume <checkpoint-path>]
```

`$team-audio` is spec-only. Its canonical output is `design/audio/audio-<artifact-id>.md`; it does not implement, import, or validate runtime audio events. Implementation requires a later approved story/architecture handoff, and runtime/audio quality is assessed by an independent later QA workflow. A team-audio checkpoint supports bounded resume only when its exact source and candidate revisions remain current.

Decision points and separately authorized writes stay with the user/owning recorder described by each skill.

### Step 5.6: Sprint Review and Next Sprint

At the end of a sprint:

```
$retrospective sprint:<sprint-id>
```

Analyzes planned vs. completed, velocity, blockers, and actionable improvements.

Then plan the next sprint:

```
$sprint-plan new
```

### Step 5.7: Milestone Reviews

At milestone checkpoints:

```
$milestone-review <stable-milestone-id>
```

Produces feature completeness, quality metrics, risk assessment, and an
evidence-backed milestone progression recommendation.

### Phase 5 Gate

```
$gate-check production-to-polish
```

**Normative gate contract (`gate.production-to-polish/v2`):**

- `PTP-A01` and `PTP-A02` require one explicit current production/milestone
  scope manifest and candidate build, with exact paths and declared revisions binding every
  in-scope requirement, story, implementation, QA-plan, test ID, source, and
  end-to-end gameplay path. Tracker status or story counts alone never pass.
- `PTP-E01` requires current PASSING `PA-REGRESSION-1` selection and runner/CI
  receipts bound to the exact selection ID and candidate build.
- `PTP-E02` requires persisted/read-back
  `cgs-smoke-check-receipt/v2` for the exact build, full selected scope,
  `Observed Verdict: PASS`, `Persistence: VERIFIED`, and
  `Handoff Eligible: YES`; quick/targeted or warning-bearing evidence is
  ineligible.
- `PTP-E03` requires current persisted/read-back `cgs.team-qa-signoff/v2`,
  `WORKFLOW_COMPLETED`, `QA_APPROVED`, `Persistence: VERIFIED`, and
  `Gate Eligible: YES` for that same candidate/build.
- `PTP-E04` requires three distinct current `PA-PLAYTEST-1` pairs—each exact
  `cgs.playtest-report/v2` plus
  `cgs.playtest-report-recorder-receipt/v1`, with matching build/session/
  protocol/bundle/dependency paths and versions and state
  `RECORDED COMPLETED — GATE ELIGIBLE`—covering new-player, mid-game, and
  difficulty-curve scopes.
- `PTP-E05` requires current PASSING `PA-PERFORMANCE-1` analyzer/report/
  `cgs.performance-report-recorder-receipt/v1` evidence for every required
  platform/scenario row. `PTP-Q01` through `PTP-Q03` separately require the
  exact current bug, fun/confusion/difficulty, UX, and accessibility evidence.
- Only a current `cgs.gate-record/v2` for this profile with every blocking row
  passing, COMPLETE coverage, and ELIGIBLE disposition can reach the external
  recorder.

---

## Phase 6: Polish

### What Happens in This Phase

Your game is feature-complete. Now you make it good. This phase focuses on
performance, balance, accessibility, audio, visual polish, and playtesting.

### Phase 6 Pipeline

```
perf-profile workflow  -->  balance-check workflow  -->  asset-audit workflow  -->  playtest-report workflow (x3)
       |                  |                    |                    |
       v                  v                    v                    v
  Profile CPU/GPU    Analyze formulas     Verify naming,      Cover: new player,
  memory, optimize   and data for         formats, sizes      mid-game, difficulty
  bottlenecks        broken progressions                      curve

  tech-debt workflow  -->  team-polish workflow
       |                |
       v                v
  Track and        Coordinated pass:
  prioritize       performance + art +
  debt items       audio + UX + QA
```

### Step 6.1: Performance Profiling

```
$perf-profile analyze-export --manifest <analysis-request-path> --input <profiler-export-path>
```

Guides you through structured performance profiling:
- Establish targets (FPS, memory, platform)
- Identify bottlenecks ranked by impact
- Generate actionable optimization tasks with code locations and expected gains

### Step 6.2: Balance Analysis

```
$balance-check analyze --manifest <project-relative-manifest-path>
```

Analyzes balance data for statistical outliers, broken progression curves,
degenerate strategies, and economy imbalances.

### Step 6.3: Asset Audit

```
$asset-audit --manifest <project-relative-manifest-path>
```

Verifies naming conventions, file format standards, and size budgets across
all assets.

### Step 6.4: Playtesting (Required: 3 Sessions)

For each session, create or reuse a protocol, ingest immutable evidence, then
finalize the stable session ID:

```
$playtest-report template --protocol-id <protocol-id>
$playtest-report ingest --session <session-manifest> --bundle <evidence-bundle>
$playtest-report finalize --session <session-manifest> --bundle <evidence-bundle>
```

Only `production/playtests/<session-id>/report.md` with `Status: COMPLETED`,
`Gate Eligible: YES`, complete build/session/tester fields, and matching raw and
observation identity counts. The workflow returns a `cgs.playtest-report/v2`
candidate but does not persist it; a current
`cgs.playtest-report-recorder-receipt/v1` from the independent external
playtest recorder must bind and persist that exact candidate before it is gate
eligible. Director reviews are separate derived artifacts and never create
another session. Three distinct completed sessions are required,
covering:
- New player experience
- Mid-game systems
- Difficulty curve

### Step 6.5: Technical Debt Assessment

```
$tech-debt report --register <project-relative-path>
```

Scans for TODO/FIXME/HACK comments, code duplication, overly complex functions,
missing tests, and outdated dependencies. Each item categorized and prioritized.

### Step 6.6: Coordinated Polish Pass

```
$team-polish verify --candidate-manifest <candidate-manifest-path> --verification-id <stable-id> --persist
```

Verifies the exact final candidate against the immutable polish test matrix,
including current performance, regression, accessibility, visual, audio, and
platform evidence. Assessment and implementation are separate prior invocations;
only `verify ... --persist` can produce the current
`cgs.polish-verification-report/v2` required by the catalog.

### Step 6.7: Localization and Accessibility

```
$localize scan --request <request-path>
```

Scans for hardcoded strings, concatenation that breaks translation, text that
does not account for expansion, and missing locale files.

Accessibility is audited against the tier committed in Phase 3's accessibility
requirements document.

### Phase 6 Gate

```
$gate-check polish-to-release
```

**Normative gate contract (`gate.polish-to-release/v2`):**

- `PTR-A01` requires mutually bound current release/policy/candidate manifests
  with exact schema versions, IDs, repository-relative paths, declared revision,
  candidate/build/artifact identities, and complete feature/content/platform/locale
  scope. Package or manifest presence alone never passes.
- `PTR-E01` requires persisted current `cgs.release-checklist-result/v2`
  evidence for `PA-RELEASE-COLLECTOR-1`, bound to the exact release policy and
  candidate, with every HARD row PASS or policy-authorized N/A. UNKNOWN,
  STALE, partial, revision mismatch, or invalid N/A is ineligible.
- `PTR-E02` through `PTR-E05` require current PASSING
  `cgs.team-qa-signoff/v2`, full-scope
  `cgs-smoke-check-receipt/v2` plus regression selection/runner receipt,
  persisted/read-back `cgs-test-evidence-review-report/v2`, and
  `PA-PERFORMANCE-1` analyzer/report/
  `cgs.performance-report-recorder-receipt/v1`, all bound to the same exact
  candidate/build/platform paths and versions and their adapter-specific
  persistence/current/gate-eligibility states.
- `PTR-E06` requires the exact non-persisted localization review envelope and
  `cgs.localization-evidence-manifest/v2` extension together with current
  `cgs.localization-evidence-review-recorder-receipt/v1`, complete required
  locale coverage, read-back verified persistence, and gate eligibility.
- `PTR-Q01` and `PTR-Q02` require the exact current bug, accessibility,
  legal/privacy/rating/certification, package, store metadata, changelog,
  patch-note, and balance evidence enumerated by the release manifests and
  policy. Prose assertions or file existence are insufficient.
- Only a current `cgs.gate-record/v2` for this exact profile with every
  blocking row passing, COMPLETE coverage, and ELIGIBLE disposition may be
  considered by the external recorder.

---

## Phase 7: Release

### What Happens in This Phase

Your game is polished, tested, and ready. Now you ship it.

### Phase 7 Pipeline

```
release-checklist workflow  -->  launch-checklist workflow  -->  team-release workflow
        |                       |                      |
        v                       v                      v
  Candidate-bound         Version-bound launch       Coordinate bounded
  evidence collector      assessment; no           staging/production/
  (no gate verdict)       publishing authority     communication phases
                    Also: changelog, patch-notes, hotfix workflows
```

### Step 7.1: Release Checklist

```
$release-checklist --request <path>
```

Collects and normalizes current candidate-bound evidence into stable
`PASS/FAIL/UNKNOWN/authorized N/A` items. It always emits `Gate Decision: NOT
EVALUATED`; `$gate-check` separately emits a read-only gate assessment and
does not advance stage. Coverage includes:
- Build verification (all platforms compile and run)
- Certification requirements (platform-specific)
- Store metadata (descriptions, screenshots, trailers)
- Legal compliance (EULA, privacy policy, ratings)
- Save game compatibility
- Analytics verification

### Step 7.2: Launch Readiness (Full Validation)

```
$launch-checklist --request <path>
```

Complete cross-department, build/version-bound assessment. External or manual facts
remain UNKNOWN until a verifiable receipt or authorized owner attestation exists;
the workflow does not publish or make the final launch decision:

The department rows below are coverage orientation, not pass criteria. Launch
readiness must come from the exact `cgs.launch-checklist-result/v2` bound to the
request, release/candidate/build/artifact paths and declared revisions, policy/risk
profile, complete evidence-manifest rows, current versioned receipts, and its
native persistence/currentness result. Missing, stale, partial, unpersisted, or
unsupported evidence remains UNKNOWN/blocked regardless of filenames or counts.

| Department | What Is Checked |
|-----------|---------------|
| **Engineering** | Build stability, crash rates, memory leaks, load times |
| **Design** | Feature completeness, tutorial flow, difficulty curve |
| **Art** | Asset quality, missing textures, LOD levels |
| **Audio** | Missing sounds, mixing levels, spatial audio |
| **QA** | Open bug count by severity, regression suite pass rate |
| **Narrative** | Dialogue completeness, lore consistency, typos |
| **Localization** | All strings translated, no truncation, locale testing |
| **Accessibility** | Compliance checklist, assistive feature testing |
| **Store** | Metadata complete, screenshots approved, pricing set |
| **Marketing** | Press kit ready, launch trailer, social media scheduled |
| **Community** | Patch notes draft, FAQ prepared, support channels ready |
| **Infrastructure** | Servers scaled, CDN configured, monitoring active |
| **Legal** | EULA finalized, privacy policy, COPPA/GDPR compliance |

Each check row uses exactly `PASS`, `FAIL`, `UNKNOWN`, or `NOT_APPLICABLE`.
The evidence-readiness verdict is exactly one of `LAUNCH_READY`,
`LAUNCH_BLOCKED`, `CONCERNS`, `UNDETERMINED`, or `ERROR`, and the result always
states `Launch Decision: NOT_RECORDED`. GO/NO_GO belongs only to the user or a
separately authorized launch gate. The launch-checklist workflow neither
records nor invokes that decision and does not ship, deploy, or publish.

### Step 7.3: Generate Player-Facing Content

```
$patch-notes --request <path>
```

Generates a local, player-facing draft only from the request-bound approved
release change manifest and verified production deployment evidence. The
`cgs.approved-release-change-manifest/v2` source is an EXTERNAL_BOUNDARY input;
no P1 project skill produces it. For any non-source locale, the exact request
must also bind current `cgs.localization-manifest/v2`,
`cgs.localization-package/v1`, `cgs.translation-delivery/v1`, and
`cgs.locale-review/v1` evidence produced through the localization workflow.

```
$changelog --request <path>
```

Generates an internal changelog (more technical, for the team).

### Step 7.4: Coordinate the Release

```
$team-release --request <path>
```

Prepares a version-bound coordination run. Staging, production promotion, and
communication are separate invocations with separate explicit authorizations;
one invocation never cascades across them. It coordinates release-manager, QA,
and DevOps through:
1. Pre-release validation
2. Build management
3. Final QA sign-off
4. Deployment preparation
5. Evidence-bound input for the separately authorized launch gate and
   post-deploy stabilization

### Step 7.5: Ship

The `validate-push` hook will warn you when pushing to `main` or `develop`.
This is intentional -- release pushes should be deliberate:

```bash
git tag v1.0.0
git push origin main --tags
```

### Step 7.6: Post-Launch

**Hotfix workflow** for critical production bugs:

```
$hotfix plan --request-manifest <path>
```

Bypasses normal sprint processes with a full audit trail:
1. Creates a hotfix branch
2. Implements the fix
3. Ensures backport to development branch
4. Documents the incident

**Post-mortem** after launch stabilizes:

```
Ask Codex to create a post-mortem using the template at
.codex/docs/templates/post-mortem.md
```

---

## Cross-Cutting Concerns

These topics apply across all phases.

### Director Review Modes

Review mode is opt-in per consumer, not a flag inherited by every gate-using skill. The optional `production/review-mode.txt` value is read only by a skill that explicitly declares support.

| Consumer | `full` | `lean` | `solo` |
|---|---|---|---|
| `$gate-check` | four phase director gates | four phase director gates | director contribution `N/A` |
| `$sprint-plan` | PR-SPRINT | skip advisory gate | skip advisory gate |
| `$story-readiness` | QL-STORY-READY | skip advisory gate | skip advisory gate |
| `$milestone-review` | PR-MILESTONE | skip advisory gate | skip advisory gate |

No mode may skip required QA, accessibility, security, evidence/currentness validation, separation of duties, non-waivable blockers, or canonical recorder receipts. A skipped advisory gate is `N/A`, never approval. Other skills expose `--review` only if their own interface explicitly defines it.

Full gate registry and evidence rules: `.codex/docs/director-gates.md`.

---

### The Collaboration Protocol

This system is **user-driven collaborative**, not autonomous.

**Pattern:** Question > Options > Decision > Draft > Approval

Every agent interaction follows this pattern:
1. Agent asks clarifying questions
2. Agent presents 2-4 options with trade-offs and reasoning
3. You decide
4. Agent drafts based on your decision
5. You review and refine
6. Agent asks "May I apply the proposed changeset?" before applying a not-yet-authorized changeset

See `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md` for the full protocol with
examples.

### The user-input request Tool

Agents use the `user-input request` tool for structured option presentation.
The pattern is Explain then Capture: full analysis in conversation text first,
then a clean UI picker for the decision. Use it for design choices,
architecture decisions, and strategic questions. Do not use it for open-ended
discovery questions or simple yes/no confirmations.

### Agent Coordination (3-Tier Hierarchy)

```
Tier 1 (Directors):    creative-director, technical-director, producer
                                          |
Tier 2 (Leads):        game-designer, lead-programmer, art-director,
                       audio-director, narrative-director, qa-lead,
                       release-manager, localization-lead
                                          |
Tier 3 (Specialists):  gameplay-programmer, engine-programmer,
                       ai-programmer, network-programmer, ui-programmer,
                       tools-programmer, systems-designer, level-designer,
                       economy-designer, world-builder, writer,
                       technical-artist, sound-designer, ux-designer,
                       qa-tester, performance-analyst, devops-engineer,
                       analytics-engineer, accessibility-specialist,
                       live-ops-designer, prototyper, security-engineer,
                       community-manager, godot-specialist,
                       godot-gdscript-specialist, godot-shader-specialist,
                       godot-csharp-specialist, godot-gdextension-specialist,
                       unity-specialist, unity-dots-specialist,
                       unity-shader-specialist, unity-addressables-specialist,
                       unity-ui-specialist, unreal-specialist,
                       ue-blueprint-specialist, ue-gas-specialist,
                       ue-replication-specialist, ue-umg-specialist
```

**Coordination rules:**
- Vertical delegation: Directors > Leads > Specialists. Never skip tiers for
  complex decisions.
- Horizontal consultation: Agents at the same tier may consult each other but
  must not make binding decisions outside their domain.
- Conflict resolution: Design conflicts go to `creative-director`. Technical
  conflicts go to `technical-director`. Scope conflicts go to `producer`.
- No unilateral cross-domain changes.

### Automated Hooks (Safety Net)

The trusted project registers 12 handlers across 8 events in `.codex/hooks.json`:

| Hook | Trigger | What It Does |
|------|---------|-------------|
| `session-start.sh` | Session start | Shows branch, recent commits, detects active.md for recovery |
| `detect-gaps.sh` | Session start | Detects fresh projects (no engine, no concept) and suggests `$start` |
| `validate-command-safety.sh` | Before every Bash command | Quote-aware enforcement of the project command deny policy |
| `pre-compact.sh` | Before compaction | Dumps session state into conversation for auto-recovery |
| `post-compact.sh` | After compaction | Reminds Codex to restore session state from `active.md` |
| `validate-commit.sh` | Before commit | Checks for design doc references, valid JSON, no hardcoded values |
| `validate-push.sh` | Before push | Warns on pushes to main/develop |
| `validate-assets.sh` | After `apply_patch` | Checks changed asset naming and JSON validity; feedback does not roll back the patch |
| `validate-skill-change.sh` | Skill file written | Advises running `$skill-test` after `.agents/skills/` changes |
| `log-agent.sh` | Agent start | Logs agent invocations for audit trail |
| `log-agent-stop.sh` | Agent stop | Completes agent audit trail (start + stop) |
| `session-stop.sh` | Session end | Final session logging |

These are the 11 migrated source mappings plus one supplemental command-safety
handler. `hook-lib.sh` is a shared helper, not a registered handler. The source
Notification event is not counted; desktop notifications use Codex `[tui]`
settings.

### Context Resilience

**Session state file:** `production/session-state/active.md` is a living
checkpoint. Update it after each significant milestone. After any disruption
(compaction, crash, `/clear`), read this file first.

**Incremental writing:** When creating multi-section documents, persist each
accepted section as part of the authorized changeset. Ask at substantive design
decision points, not again for every file edit. This lets completed work survive
crashes and context compactions.

**Automatic recovery:** The `session-start.sh` hook detects and previews
`active.md` automatically. The `pre-compact.sh` hook dumps state into the
conversation before compaction.

**Sprint status tracking:** `production/sprint-status.yaml` is the
machine-readable story tracker. Written by `$sprint-plan` (init) and
`$story-done` (status updates). Read by `$sprint-status`, `$help`, and
`$story-done` (next story). Eliminates fragile markdown scanning.

### Brownfield Adoption

For existing projects that already have some artifacts:

```
$adopt
```

Or targeted:

```
$adopt gdds
$adopt adrs
$adopt stories
$adopt infra
```

This audits existing artifacts for **format** (not existence), classifies gaps
as BLOCKING/HIGH/MEDIUM/LOW, builds an ordered migration plan, and writes
`docs/adoption-plan-[date].md`. Core principle: MIGRATION not REPLACEMENT --
it never regenerates existing work, only fills gaps.

Individual skills expose bounded brownfield operations through their actual
invocation contracts:

```
$design-system design/gdd/combat-system.md --mode fill-gaps
$architecture-decision <architecture-decision-request-manifest-path>
```

For an ADR, the request manifest declares `operation: retrofit`, the exact target
path, and its current declared revision. `design-system` has no `retrofit` alias:
`fill-gaps` preserves substantive sections, while an intentional one-section
change uses `--mode revise-section --section "<canonical-section>"`.

### Gate System

Phase gates are read-only assessments. Use the exact catalog transition ID:

```
$gate-check concept-to-systems-design
$gate-check systems-design-to-technical-setup
$gate-check technical-setup-to-pre-production
$gate-check pre-production-to-production
$gate-check production-to-polish
$gate-check polish-to-release
```

The conversational `cgs.gate-record/v2` verdict is PASS, CONCERNS, FAIL, or
PARTIAL. Only PASS + COMPLETE coverage + ELIGIBLE disposition + CURRENT evidence
can be considered for advancement. `$gate-check` writes no files and never
updates `production/stage.txt` or the authority record.

Stage mutation belongs only to a separately configured external recorder at
`production/stage/external-recorder-contract.json`, using contract schema
`cgs.external-stage-transition-recorder-contract/v1`. It must verify the exact
gate record identity and all dependencies, compare-and-swap
`production/stage/authority.json`, append immutable history, atomically persist
or restore the preimage, read back the result, and emit
`cgs.external-stage-transition-receipt/v1`. No P1 project skill implements or
invokes this recorder. A missing or invalid recorder contract means
`UNKNOWN_ADVANCEMENT_UNSUPPORTED`; stage does not advance.

### Reverse Documentation

For code that exists without design docs (common after brownfield adoption):

```
$reverse-document --manifest <request-path>
```

Reads existing code and generates GDD-format design documentation from it.

---

## Appendix A: Agent Quick-Reference

### "I need to do X -- which agent do I use?"

| I need to... | Agent | Tier |
|-------------|-------|------|
| Come up with a game idea | `$brainstorm` skill | -- |
| Design a game mechanic | `game-designer` | 2 |
| Design specific formulas/numbers | `systems-designer` | 3 |
| Design a game level | `level-designer` | 3 |
| Design loot tables / economy | `economy-designer` | 3 |
| Build world lore | `world-builder` | 3 |
| Write dialogue | `writer` | 3 |
| Plan the story | `narrative-director` | 2 |
| Plan a sprint | `producer` | 1 |
| Make a creative decision | `creative-director` | 1 |
| Make a technical decision | `technical-director` | 1 |
| Implement gameplay code | `gameplay-programmer` | 3 |
| Implement core engine systems | `engine-programmer` | 3 |
| Implement AI behavior | `ai-programmer` | 3 |
| Implement multiplayer | `network-programmer` | 3 |
| Implement UI | `ui-programmer` | 3 |
| Build dev tools | `tools-programmer` | 3 |
| Review code architecture | `lead-programmer` | 2 |
| Create shaders / VFX | `technical-artist` | 3 |
| Define visual style | `art-director` | 2 |
| Define audio style | `audio-director` | 2 |
| Design sound effects | `sound-designer` | 3 |
| Design UX flows | `ux-designer` | 3 |
| Write test cases | `qa-tester` | 3 |
| Plan test strategy | `qa-lead` | 2 |
| Profile performance | `performance-analyst` | 3 |
| Set up CI/CD | `devops-engineer` | 3 |
| Design analytics | `analytics-engineer` | 3 |
| Check accessibility | `accessibility-specialist` | 3 |
| Plan live operations | `live-ops-designer` | 3 |
| Manage a release | `release-manager` | 2 |
| Manage localization | `localization-lead` | 2 |
| Prototype quickly | `prototyper` | 3 |
| Audit security | `security-engineer` | 3 |
| Communicate with players | `community-manager` | 3 |
| Godot-specific help | `godot-specialist` | 3 |
| GDScript-specific help | `godot-gdscript-specialist` | 3 |
| Godot shader help | `godot-shader-specialist` | 3 |
| GDExtension modules | `godot-gdextension-specialist` | 3 |
| Unity-specific help | `unity-specialist` | 3 |
| Unity DOTS/ECS | `unity-dots-specialist` | 3 |
| Unity shaders/VFX | `unity-shader-specialist` | 3 |
| Unity Addressables | `unity-addressables-specialist` | 3 |
| Unity UI Toolkit | `unity-ui-specialist` | 3 |
| Unreal-specific help | `unreal-specialist` | 3 |
| Unreal GAS | `ue-gas-specialist` | 3 |
| Unreal Blueprints | `ue-blueprint-specialist` | 3 |
| Unreal replication | `ue-replication-specialist` | 3 |
| Unreal UMG/CommonUI | `ue-umg-specialist` | 3 |

### Agent Hierarchy

```
                    creative-director / technical-director / producer
                                         |
          ---------------------------------------------------------------
          |            |           |           |          |        |       |
    game-designer  lead-prog  art-dir  audio-dir  narr-dir  qa-lead  release-mgr
          |            |           |           |          |        |        |
     specialists  programmers  tech-art  snd-design  writer   qa-tester  devops
     (systems,    (gameplay,             (sound)     (world-  (perf,     (analytics,
      economy,     engine,                           builder)  access.)   security)
      level)       ai, net,
                   ui, tools)
```

**Escalation rule:** If two agents disagree, go up. Design conflicts go to
`creative-director`. Technical conflicts go to `technical-director`. Scope
conflicts go to `producer`.

---

## Appendix B: Skill Quick-Reference

### All 74 Skills by Category

#### Onboarding and Navigation (7)

| Command | Purpose | Phase |
|---------|---------|-------|
| `$start` | Guided onboarding, routes to right workflow | Any (first session) |
| `$help` | Context-aware "what do I do next?" | Any |
| `$project-stage-detect` | Full project audit to determine current phase | Any |
| `$studio-status` | Read-only stage, active focus, evidence, and recovery summary | Any |
| `$setup-engine` | Configure engine, pin version, set preferences | 1 |
| `$adopt` | Brownfield audit and migration plan | Any (existing projects) |
| `$skill-improve` | Improve a skill via test-fix-retest loop | Any |

#### Game Design (6)

| Command | Purpose | Phase |
|---------|---------|-------|
| `$brainstorm` | Collaborative ideation with MDA analysis | 1 |
| `$map-systems` | Decompose concept into systems index | 1-2 |
| `$design-system` | Guided section-by-section GDD authoring | 2 |
| `$quick-design` | Versioned proposal for structurally low-risk bounded changes; separate application required | 2+ |
| `$review-all-gdds` | Cross-GDD consistency and design theory review | 2 |
| `$propagate-design-change` | Find ADRs/stories affected by GDD changes | 5 |

#### UX and Interface (2)

| Command | Purpose | Phase |
|---------|---------|-------|
| `$ux-design` | Author UX specs (screen/flow, HUD, patterns) | 4 |
| `$ux-review` | Validate UX specs for accessibility and GDD alignment | 4 |

#### Architecture (4)

| Command | Purpose | Phase |
|---------|---------|-------|
| `$create-architecture` | Master architecture document | 3 |
| `$architecture-decision` | Create or retrofit an ADR | 3 |
| `$architecture-review` | Validate all ADRs, dependency ordering | 3 |
| `$create-control-manifest` | Flat programmer rules from Accepted ADRs | 3 |

#### Stories and Sprints (8)

| Command | Purpose | Phase |
|---------|---------|-------|
| `$create-epics` | Translate GDDs + ADRs into epics (one per module) | 4 |
| `$create-stories` | Break a single epic into story files | 4 |
| `$dev-story` | Implement a story — routes to the correct programmer agent | 5 |
| `$sprint-plan` | Create or manage sprint plans | 4-5 |
| `$sprint-status` | Quick 30-line sprint snapshot | 5 |
| `$story-readiness` | Validate story is implementation-ready | 4-5 |
| `$story-done` | 8-phase story completion review | 5 |
| `$estimate` | Read-only relative or calibrated evidence via explicit story/sprint/freeform profile | 4-5 |

#### Reviews and Analysis (13)

| Command | Purpose | Phase |
|---------|---------|-------|
| `$design-review` | Validate GDD against 8-section standard | 1-2 |
| `$code-review` | Architectural code review | 5+ |
| `$balance-check` | Game balance formula analysis | 5-6 |
| `$asset-audit` | Asset naming, format, size verification | 6 |
| `$asset-spec` | Per-asset visual specs and AI generation prompts | 5-6 |
| `$content-audit` | GDD-specified content vs. implemented | 5 |
| `$consistency-check` | Cross-GDD entity and formula inconsistency scan | 2+ |
| `$scope-check` | Compare explicit immutable baseline/current scope by stable IDs; product decisions remain external | 5 |
| `$perf-profile` | Capture preparation or runtime-export analysis; only persisted build-bound runtime reports are gate eligible | 6 |
| `$tech-debt` | Tech debt scanning and prioritization | 6 |
| `$gate-check` | Read-only transition assessment with PASS/CONCERNS/FAIL/PARTIAL; no stage mutation | All transitions |
| `$reverse-document` | Generate design docs from existing code | Any |
| `$security-audit` | Security vulnerability audit (save, network, input) | 6-7 |

#### QA and Testing (9)

| Command | Purpose | Phase |
|---------|---------|-------|
| `$qa-plan` | Generate QA test plan for a sprint or feature | 5 |
| `$smoke-check` | Critical path smoke test gate before QA hand-off | 5-6 |
| `$soak-test` | Soak test protocol for extended play sessions | 6 |
| `$regression-suite` | Map test coverage, identify fixed bugs lacking regression tests | 5-6 |
| `$test-setup` | Scaffold test framework and CI/CD pipeline | 4 |
| `$test-helpers` | Generate engine-specific test helper libraries | 4-5 |
| `$test-evidence-review` | Quality review of test files and manual evidence | 5 |
| `$test-flakiness` | Detect non-deterministic tests from CI logs | 5-6 |
| `$skill-test` | Validate skill files for structural and behavioral correctness | Any |

#### Production Management (6)

| Command | Purpose | Phase |
|---------|---------|-------|
| `$milestone-review` | Milestone progress and progression recommendation | 5 |
| `$retrospective` | Sprint retrospective analysis | 5 |
| `$bug-report` | Structured bug report creation | 5+ |
| `$bug-triage` | Read-only evidence triage with proposed priority/scheduling/risk dispositions; a separate recorder commits decisions | 5+ |
| `$playtest-report` | Create protocols, ingest immutable evidence, and finalize canonical completed session reports | 4-6 |
| `$onboard` | Onboard a new team member | Any |

#### Release (6)

| Command | Purpose | Phase |
|---------|---------|-------|
| `$release-checklist` | Candidate-bound evidence collector; gate decision is not evaluated | 7 |
| `$launch-checklist` | Version-bound launch assessment with verified external receipts | 7 |
| `$changelog` | Generate a range-bound local changelog entry from an exact request manifest; never implies deployment/publication | 7 |
| `$patch-notes` | Local player-facing draft from exact approved candidate plus verified production deployment receipt; never publishes | 7 |
| `$hotfix` | Emergency fix workflow | 7+ |
| `$day-one-patch` | Scoped patch for issues found after gold master | 7+ |

#### Creative (4)

| Command | Purpose | Phase |
|---------|---------|-------|
| `$prototype` | Concept prototype — validate core idea before GDDs | 1 |
| `$art-bible` | Guided Art Bible authoring — visual identity spec | 1-2 |
| `$vertical-slice` | Production-quality end-to-end build before Production | 4 |
| `$localize` | String extraction and validation | 6-7 |

#### Team Orchestration (9)

| Command | Purpose | Phase |
|---------|---------|-------|
| `$team-combat` | Combat feature: design through implementation | 5 |
| `$team-narrative` | Narrative content: structure through dialogue | 5 |
| `$team-ui` | UI feature: UX spec through polished implementation | 5 |
| `$team-level` | Level: layout through dressed encounters | 5 |
| `$team-audio` | Version-bound audio specification only; implementation and QA are later independent workflows | 5 |
| `$team-polish` | Coordinated polish: perf + art + audio + QA | 6 |
| `$team-release` | Version-bound release coordination with separate staging, production, publication, and stabilization authorizations | 7 |
| `$team-live-ops` | Live-ops planning: seasonal events, battle pass, retention | 7+ |
| `$team-qa` | Exact-candidate QA cycle; only persisted COMPLETE + APPROVED + Gate Eligible YES hands off | 6-7 |

---

## Appendix C: Common Workflows

### Workflow 1: "I just started and have no game idea"

```text
$start
$brainstorm <request-manifest-path>
$setup-engine --manifest <engine-request-path>
# Optional: separately obtain exact external cgs.concept-approval/v1.
$map-systems
$gate-check concept-to-systems-design
$design-system <system-name-or-gdd-path> --mode new
```

### Workflow 2: "I have designs and want to start coding"

```text
$design-review <path-to-system-gdd> --depth lean
$review-all-gdds
$gate-check systems-design-to-technical-setup
$create-architecture new
$architecture-decision <request-manifest-path>
$architecture-review
$create-control-manifest new
$gate-check technical-setup-to-pre-production
$create-epics <request-manifest-path>
$create-stories author <epic-path> --epic-receipt <epic-receipt-path>
$sprint-plan new
$story-readiness --story <project-relative-story-path>
# Via external cgs.story-readiness-recorder/v1 (not a project skill or command),
# independently obtain the current persisted cgs.story-readiness-record/v1 READY
# plus cgs.story-readiness-recorder-receipt/v1: RECORDED or ALREADY_RECORDED,
# exact record/receipt/declared revisions current, implementation_gate_eligible: true.
$dev-story --request <project-relative-request-path>
$code-review --target <project-relative-file-or-directory>
# Separately obtain cgs.code-review-recorder-receipt/v1.
$story-done <story-file-path>
```

### Workflow 3: "I need to add a complex feature mid-production"

```text
$design-system <system-name-or-gdd-path> --mode revise-section --section "<canonical-section>"
$design-review <path-to-system-gdd> --depth lean
$propagate-design-change <request-manifest-path>
$estimate story --basis relative --input <project-relative-story-path>
$team-narrative --manifest <request-path> [--resume <checkpoint-path>]
$team-ui --manifest <ui-request-path> [--resume <checkpoint-path>]
$story-done <story-file-path>
$balance-check analyze --manifest <project-relative-manifest-path>
```

For a structurally low-risk proposal, use the complete quick-design `propose`
form shown earlier instead of abbreviating its required identity fields.

### Workflow 4: "Something broke in production"

```text
$hotfix plan --request-manifest <path>
$code-review --target <project-relative-file-or-directory>
# Separately record the exact approved code-review envelope.
$release-checklist --request <path>
```

### Workflow 5: "I have an existing project and want to use this system"

```text
$start
$project-stage-detect
$adopt
$design-system design/gdd/<system-slug>.md --mode fill-gaps
$architecture-decision <architecture-decision-request-manifest-path>
$gate-check <exact-catalog-transition-id>
```

The architecture-decision request manifest declares `operation: retrofit`.

### Workflow 6: "Starting a new sprint"

```text
$retrospective sprint:<sprint-id>
$sprint-plan new
$scope-check compare --baseline <approved-scope-path> --current <current-scope-path>
$story-readiness --story <project-relative-story-path>
$story-done <story-file-path>
$sprint-status
```

### Workflow 7: "Shipping the game"

```text
$gate-check polish-to-release
$tech-debt report --register <project-relative-path>
$localize validate --request <request-path>
$release-checklist --request <path>
$launch-checklist --request <path>
$team-release --request <path>
$changelog --request <path>
$patch-notes --request <path>
$hotfix plan --request-manifest <path>
```

Deployment/publication remain separately authorized external operations.

### Workflow 8: "I'm lost / don't know what to do next"

```text
$help
$project-stage-detect
$gate-check <exact-catalog-transition-id>
```

---

## Tips for Getting the Most Out of the System

1. **Always start with design, then implement.** The agent system is built
   around the assumption that a design document exists before code is written.
   Agents reference GDDs constantly.

2. **Use team skills for cross-cutting features.** Do not try to manually
   coordinate 4 agents yourself -- let `$team-combat`, `$team-narrative`,
   etc. handle the orchestration.

3. **Trust the rules system.** When a rule flags something in your code, fix
   it. The rules encode hard-won game development wisdom (data-driven values,
   delta time, accessibility, etc.).

4. **Compact proactively.** At ~65-70% context usage, compact or `/clear`.
   The pre-compact hook saves your progress. Do not wait until you are at the
   limit.

5. **Use the right tier of agent.** Do not ask `creative-director` to write a
   shader. Do not ask `qa-tester` to make design decisions. The hierarchy
   exists for a reason.

6. **Run $help when uncertain.** It reads your actual project state and tells
   you the single most important next step.

7. **Run `$design-review` before handing designs to programmers.** This
   catches incomplete specs early, saving rework.

8. **Run `$code-review` after every major feature.** Catch architectural
   issues before they propagate.

9. **Prototype risky mechanics first.** A day of prototyping can save a week
   of production on a mechanic that does not work.

10. **Keep your sprint plans honest.** Use `$scope-check compare --baseline <approved-scope-path> --current <current-scope-path>` regularly. Scope
    creep is the number one killer of indie games.

11. **Document decisions with ADRs.** Future-you will thank present-you for
    recording *why* things were built the way they were.

12. **Use the story lifecycle religiously.** Run `$story-readiness`, obtain the
    independently persisted current READY record and valid recorder receipt,
    then allow pickup; run `$story-done` after completion. This catches
    deviations early and keeps the pipeline honest.

13. **Write to files early and often.** Incremental section writing means your
    design decisions survive crashes and compactions. The file is the memory,
    not the conversation.
