---
name: review-all-gdds
description: "Holistic cross-GDD consistency and game design review. Reads all system GDDs simultaneously and checks for contradictions between them, stale references, ownership conflicts, formula incompatibilities, and game design theory violations (dominant strategies, economic imbalance, cognitive overload, pillar drift). Run after all MVP GDDs are written, before architecture begins."
---

## Invocation and execution

Invoke this workflow as `$review-all-gdds`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[focus: full | consistency | design-theory | since-last-review]`. Treat bracketed values as optional unless the workflow says otherwise.


# Review All GDDs

This skill reads every system GDD simultaneously and performs two complementary
reviews that cannot be done per-GDD in isolation:

1. **Cross-GDD Consistency** — contradictions, stale references, and ownership
   conflicts between documents
2. **Game Design Holism** — issues that only emerge when you see all systems
   together: dominant strategies, broken economies, cognitive overload, pillar
   drift, competing progression loops

**This is distinct from `$design-review`**, which reviews one GDD for internal
completeness. This skill reviews the *relationships* between all GDDs.

**When to run:**
- After all MVP-tier GDDs are individually approved
- After any GDD is significantly revised mid-production
- Before `$create-architecture` begins (architecture built on inconsistent GDDs
  inherits those inconsistencies)

**Argument modes:**

**Focus:** the first provided argument (blank = `full`)

- **No argument / `full`**: Both consistency and design theory passes
- **`consistency`**: Cross-GDD consistency checks only (faster)
- **`design-theory`**: Game design holism checks only
- **`since-last-review`**: Only GDDs modified since the last review report (git-based)

---

## Phase 1: Load Everything

### Phase 1a — L0: Summary Scan (fast, low tokens)

Before reading any full document, search to extract `## Summary` sections
from all GDD files:

```
Search files matching `design/gdd/*.md` for `## Summary` and include 5 following lines of context.
```

Display a manifest to the user:
```
Found [N] GDDs. Summaries:
  • combat.md — [summary text]
  • inventory.md — [summary text]
  ...
```

For `since-last-review` mode: run `git log --name-only` to identify GDDs
modified since the last review report file was written. Show the user which
GDDs are in scope based on summaries before doing any full reads. Only
proceed to L1 for those GDDs plus any GDDs listed in their "Key deps".

### Phase 1b — Registry Pre-Load (fast baseline)

Before full-reading any GDD, check for the entity registry:

```
Read `design/registry/entities.yaml` in full.
```

If the registry exists and has entries, use it as a **pre-built conflict
baseline**: known entities, items, formulas, and constants with their
authoritative values and source GDDs. In Phase 2, search GDDs for registered
names first — this is faster than reading all GDDs in full before knowing
what to look for.

If the registry is empty or absent: proceed without it. Note in the report:
"Entity registry is empty — consistency checks rely on full GDD reads only.
Run `$consistency-check` after this review to populate the registry."

### Phase 1c — L1/L2: Full Document Load

Full-read the in-scope documents:

1. `design/gdd/game-concept.md` — game vision, core loop, MVP definition
2. `design/gdd/game-pillars.md` if it exists — design pillars and anti-pillars
3. `design/gdd/systems-index.md` — authoritative system list, layers, dependencies, status
4. **Every in-scope system GDD in `design/gdd/`** — read completely (skip
   game-concept.md and systems-index.md — those are read above)

Report: "Loaded [N] system GDDs covering [M] systems. Pillars: [list]. Anti-pillars: [list]."

If fewer than 2 system GDDs exist, stop:
> "Cross-GDD review requires at least 2 system GDDs. Write more GDDs first,
> then re-run `$review-all-gdds`."

---

### Parallel Execution

Phase 2 (Consistency) and Phase 3 (Design Theory) are independent — they read
the same GDD inputs but produce separate reports. Delegate both phases to parallel Codex sub-agents simultaneously rather than waiting for Phase 2 to complete before
starting Phase 3. Collect both results before writing the combined report.

**When spawning parallel Codex subagents for Phase 2 and Phase 3, always pass:**
- The complete list of GDD file paths loaded in Phase 1 (explicit paths, not just counts)
- The full TR registry contents if loaded in Phase 1b (paste the registry text, not just a file path)
- The specific checklist items assigned to that agent's phase (Phase 2 gets 2a–2f; Phase 3 gets 3a–3g)
- The engine name and version from `.codex/docs/technical-preferences.md` and `docs/engine-reference/[engine]/VERSION.md`

Do not rely on the subagent to re-read these files — it has its own context window and cannot access Phase 1 results unless they are explicitly passed in the delegation prompt.

---

## Phase 2: Cross-GDD Consistency

Work through every pair and group of GDDs to find contradictions and gaps.

### 2a: Dependency Bidirectionality

For every GDD's Dependencies section, check that every listed dependency is
reciprocal:
- If GDD-A lists "depends on GDD-B", check that GDD-B lists GDD-A as a dependent
- If GDD-A lists "depended on by GDD-C", check that GDD-C lists GDD-A as a dependency
- Flag any one-directional dependency as a consistency issue

```
⚠️  Dependency Asymmetry
[system-a].md lists: Depends On → [system-b].md
[system-b].md does NOT list [system-a].md as a dependent
→ One of these documents has a stale dependency section
```

### 2b: Rule Contradictions

For each game rule, mechanic, or constraint defined in any GDD, check whether
any other GDD defines a contradicting rule for the same situation:

Categories to scan:
- **Floor/ceiling rules**: Does any GDD define a minimum value for an output? Does any other say a different system can bypass that floor? These contradict.
- **Resource ownership**: If two GDDs both define how a shared resource accumulates or depletes, do they agree?
- **State transitions**: If GDD-A describes what happens when a character dies,
  does GDD-B's description of the same event agree?
- **Timing**: If GDD-A says "X happens on the same frame", does GDD-B assume
  it happens asynchronously?
- **Stacking rules**: If GDD-A says status effects stack, does GDD-B assume
  they don't?

```
🔴 Rule Contradiction
[system-a].md: "Minimum [output] after reduction is [floor_value]"
[system-b].md: "[mechanic] bypasses [system-a]'s rules and can reduce [output] to 0"
→ These rules directly contradict. Which GDD is authoritative?
```

### 2c: Stale References

For every cross-document reference (GDD-A mentions a mechanic, value, or
system name from GDD-B), verify the referenced element still exists in GDD-B
with the same name and behaviour:

- If GDD-A says "combo multiplier from the combat system feeds into score", check
  that the combat GDD actually defines a combo multiplier that outputs to score
- If GDD-A references "the progression curve defined in [system].md", check that
  [system].md actually has that curve, not a different progression model
- If GDD-A was written before GDD-B and assumed a mechanic that GDD-B later
  designed differently, flag GDD-A as containing a stale reference

```
⚠️  Stale Reference
inventory.md (written first): "Item weight uses the encumbrance formula
  from movement.md"
movement.md (written later): Defines no encumbrance formula — uses a flat
  carry limit instead
→ inventory.md references a formula that doesn't exist
```

### 2d: Data and Tuning Knob Ownership Conflicts

Two GDDs should not both claim to own the same data or tuning knob. Scan all
Tuning Knobs sections across all GDDs and flag duplicates:

```
⚠️  Ownership Conflict
[system-a].md Tuning Knobs: "[multiplier_name] — controls [output] scaling"
[system-b].md Tuning Knobs: "[multiplier_name] — scales [output] with [factor]"
→ Two GDDs define multipliers on the same output. Which owns the final value?
  This will produce either a double-application bug or a design conflict.
```

### 2e: Formula Compatibility

For GDDs whose formulas are connected (output of one feeds input of another),
check that the output range of the upstream formula is within the expected
input range of the downstream formula:

- If [system-a].md outputs values between [min]–[max], and [system-b].md is
  designed to receive values between [min2]–[max2], is the mismatch intentional?
- If an economy GDD expects resource acquisition in range X, and the
  progression GDD generates it at range Y, the economy will be trivial or
  inaccessible — is that intended?

Flag incompatibilities as CONCERNS (design judgment needed, not necessarily wrong):

```
⚠️  Formula Range Mismatch
[system-a].md: Max [output] = [value_a] (at max [condition])
[system-b].md: Base [input] = [value_b], max [input] = [value_c]
→ Late-[stage] [scenario] can resolve in a single [event].
  Is this intentional? If not, either [system-a]'s ceiling or [system-b]'s ceiling needs adjustment.
```

### 2f: Acceptance Criteria Cross-Check

Scan Acceptance Criteria sections across all GDDs for contradictions:

- GDD-A criteria: "Player cannot die from a single hit"
- GDD-B criteria: "Boss attack deals 150% of player max health"
These acceptance criteria cannot both pass simultaneously.

---

## Phase 3: Game Design Holism

Review all GDDs together through the lens of game design theory and player
psychology. These are issues that individual GDD reviews cannot catch because
they require seeing all systems at once.

### 3a: Progression Loop Competition

A game should have one dominant progression loop that players feel is "the
point" of the game, with supporting loops that feed into it. When multiple
systems compete equally as the primary progression driver, players don't know
what the game is about.

Scan all GDDs for systems that:
- Award the player's primary resource (XP, levels, prestige, unlocks)
- Define themselves as the "core" or "main" loop
- Have comparable depth and time investment to other systems doing the same

```
⚠️  Competing Progression Loops
combat.md: Awards XP, unlocks abilities, is described as "the core loop"
crafting.md: Awards XP, unlocks recipes, is described as "the primary activity"
exploration.md: Awards XP, unlocks map areas, described as "the main driver"
→ Three systems all claim to be the primary progression loop and all award
  the same primary currency. Players will optimise one and ignore the others.
  Consider: one primary loop with the others as support systems.
```

### 3b: Player Attention Budget

Count how many systems require active player attention simultaneously during
a typical session. Each actively-managed system costs attention:

- Active = player must make decisions about this system regularly during play
- Passive = system runs automatically, player sees results but doesn't manage it

More than 3-4 simultaneously active systems creates cognitive overload for most
players. Present the count and flag if it exceeds 4 concurrent active systems:

```
⚠️  Cognitive Load Risk
Simultaneously active systems during [core loop moment]:
  1. [system-a].md — [decision type] (active)
  2. [system-b].md — [resource management] (active)
  3. [system-c].md — [tracking] (active)
  4. [system-d].md — [item/action use] (active)
  5. [system-e].md — [cooldown/timer management] (active)
  6. [system-f].md — [coordination decisions] (active)
→ 6 simultaneously active systems during the core loop.
  Research suggests 3-4 is the comfortable limit for most players.
  Consider: which of these can be made passive or simplified?
```

### 3c: Dominant Strategy Detection

A dominant strategy makes other strategies irrelevant — players discover it,
use it exclusively, and find the rest of the game boring. Look for:

- **Resource monopolies**: One strategy generates a resource significantly
  faster than all others
- **Risk-free power**: A strategy that is both high-reward and low-risk
  (if high-risk strategies exist, they need proportionally higher reward)
- **No trade-offs**: An option that is superior in all dimensions to all others
- **Obvious optimal path**: If any progression choice is "clearly correct",
  the others aren't real choices

```
⚠️  Potential Dominant Strategy
combat.md: Ranged attacks deal 80% of melee damage with no risk
combat.md: Melee attacks deal 100% damage but require close range
→ Unless melee has a significant compensating advantage (AOE, stagger,
  resource regeneration), ranged is dominant — higher safety, only 20% less
  damage. Consider what melee offers that ranged cannot.
```

### 3d: Economic Loop Analysis

Identify all resources across all GDDs (gold, XP, crafting materials, stamina,
health, mana, etc.). For each resource, map its **sources** (how players gain
it) and **sinks** (how players spend it).

Flag dangerous economic conditions:

| Condition | Sign | Risk |
|-----------|------|------|
| **Infinite source, no sink** | Resource accumulates indefinitely | Late game becomes trivially easy |
| **Sink, no source** | Resource drains to zero | System becomes unavailable |
| **Source >> Sink** | Surplus accumulates | Resource becomes meaningless |
| **Sink >> Source** | Constant scarcity | Frustration and gatekeeping |
| **Positive feedback loop** | More resource → easier to earn more | Runaway leader, snowball |
| **No catch-up** | Falling behind accelerates deficit | Unrecoverable states |

```
🔴 Economic Imbalance: Unbounded Positive Feedback
gold economy:
  Sources: monster drops (scales with player power), merchant selling (unlimited)
  Sinks: equipment purchase (one-time), ability upgrades (finite count)
→ After equipment and abilities are purchased, gold has no sink.
  Infinite surplus. Gold becomes meaningless mid-game.
  Add ongoing gold sinks (upkeep, consumables, cosmetics, gambling).
```

### 3e: Difficulty Curve Consistency

When multiple systems scale with player progression, they must scale in
compatible directions and at compatible rates. Mismatched scaling curves
create unintended difficulty spikes or trivialisations.

For each system that scales over time, extract:
- What scales (enemy health, player damage, resource cost, area size)
- How it scales (linear, exponential, stepped)
- When it scales (level, time, area)

Compare all scaling curves. Flag mismatches:

```
⚠️  Difficulty Curve Mismatch
combat.md: Enemy health scales exponentially with area (×2 per area)
progression.md: Player damage scales linearly with level (+10% per level)
→ By area 5, enemies have 32× base health; player deals ~1.5× base damage.
  The gap widens indefinitely. Late areas will become inaccessibly difficult
  unless the curves are reconciled.
```

### 3f: Pillar Alignment

Every system should clearly serve at least one design pillar. A system that
serves no pillar is "scope creep by design" — it's in the game but not in
service of what the game is trying to be.

For each GDD system, check its Player Fantasy section against the design pillars.
Flag any system whose stated fantasy doesn't map to any pillar:

```
⚠️  Pillar Drift
fishing-system.md: Player Fantasy — "peaceful, meditative activity"
Pillars: "Brutal Combat", "Tense Survival", "Emergent Stories"
→ The fishing system serves none of the three pillars. Either add a pillar
  that covers it, redesign it to serve an existing pillar, or cut it.
```

Also check anti-pillars — flag any system that does what an anti-pillar
explicitly says the game will NOT do:

```
🔴 Anti-Pillar Violation
Anti-Pillar: "We will NOT have linear story progression — player defines their path"
main-quest.md: Defines a 12-chapter linear story with mandatory sequence
→ This system directly violates the defined anti-pillar.
```

### 3g: Player Fantasy Coherence

The player fantasies across all systems should be compatible — they should
reinforce a consistent identity for what the player IS in this game. Conflicting
player fantasies create identity confusion.

```
⚠️  Player Fantasy Conflict
combat.md: "You are a ruthless, precise warrior — every kill is earned"
dialogue.md: "You are a charismatic diplomat — violence is always avoidable"
exploration.md: "You are a reckless adventurer — diving in without a plan"
→ Three systems present incompatible identities. Players will feel the game
  doesn't know what it wants them to be. Consider: do these fantasies serve
  the same core identity from different angles, or do they genuinely conflict?
```

---

## Required continuation

Before continuing, read [references/continued-workflow.md](references/continued-workflow.md) in full. It contains the remaining required phases, output formats, recovery rules, and handoff instructions; execute them in order.
