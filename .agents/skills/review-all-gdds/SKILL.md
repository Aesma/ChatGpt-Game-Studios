---
name: review-all-gdds
description: "Report-only holistic review of the current, hash-bound system-GDD set. Checks cross-document consistency and records design-theory hypotheses without treating unmeasured heuristics as blockers. Returns exactly PASS, CONCERNS, FAIL, or PARTIAL; any persisted output is limited to one explicitly authorized immutable report. Run after all MVP GDDs are approved and before architecture begins."
---

## Invocation and execution

Invoke this workflow as `$review-all-gdds`.

This workflow is report-only. Render the complete report in conversation by
default. If the user asks to persist it, present the exact, unique report path
as the complete proposed changeset and obtain explicit approval before that one
write. Never modify a GDD, `systems-index.md`, the entity registry, session
state, lifecycle status, sign-off, or an existing review report. Remediation
and lifecycle transitions belong to separate owner-authorized workflows.

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
- **`since-last-review`**: GDDs whose content hashes differ from an explicitly
  identified prior report manifest, plus the dependencies already defined by
  this workflow. If no trustworthy manifest exists, fall back to `full`; never
  infer the baseline from report file modification time.

### Frozen public contract

- **Verdict vocabulary:** exactly `PASS`, `CONCERNS`, `FAIL`, or `PARTIAL`.
- **Report-only boundary:** conversation output is the default. The only
  permitted file write is one new, explicitly authorized immutable review
  report. Declining the write causes zero file mutations.
- **Evidence identity:** every report binds its project, mode, source revision,
  canonical input paths, SHA-256 content hashes, run ID, and coverage. Any
  added, removed, renamed, or changed input makes that report stale.
- **Incomplete work:** a worker error, unchecked required scope, missing input,
  or unresolved evidence conflict produces `PARTIAL`; it can never produce
  `PASS`.
- **Blocking boundary:** a deterministic contradiction may block. A design-
  theory observation is `HYPOTHESIS / ADVISORY` unless it reproducibly violates
  an explicit anti-pillar, an owner-approved invariant, or an owner-approved
  quantitative threshold present in the hashed inputs.
- **Accepted risk:** `FAIL` is never relabeled. A gate may consume a separate,
  owner-signed `ACCEPTED_RISK` record that names this run and exact findings,
  scope, owner, and expiry; that record does not change the review verdict.

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

For `since-last-review` mode: identify the baseline report by explicit run ID,
or use the newest report whose embedded project ID and complete input manifest
can be validated. Compare current SHA-256 hashes to that manifest. Do not use
report timestamps or filesystem modification times as evidence. Show the user
which GDDs changed before doing any full reads. Only proceed to L1 for those
GDDs plus any GDDs listed in their "Key deps". If the baseline manifest cannot
be validated, state that incremental scope is unsafe and run `full`.

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

### Phase 1d — Bind the Input Manifest

Before analysis or delegation, build an ordered input manifest containing:

- **Project ID:** canonical repository root plus repository identity (remote
  identity when configured)
- **Run ID:** UTC timestamp plus the first 12 characters of the SHA-256 digest
  of the ordered manifest
- **Mode:** the validated focus argument
- **Source revision:** current commit ID, and whether tracked or untracked input
  files differ from that revision
- **Inputs:** canonical path and SHA-256 hash of every GDD and every supporting
  document actually used, including pillars, systems index, and registry
- **Planned coverage:** phases and checks that apply to the selected mode

Use hashes of the exact file bytes, not timestamps. Pass the manifest and run
ID to every worker. At merge time, record each planned check as `DONE`,
`PARTIAL`, `ERROR`, or `NOT_APPLICABLE` and list any unchecked paths or checks.
The report is current only while its project ID and complete input path/hash set
match the project. Any difference makes it **STALE**; a stale `PASS` or
`CONCERNS` is not valid gate evidence.

---

### Parallel Execution

Phase 2 (Consistency) and Phase 3 (Design Theory) are independent — they read
the same GDD inputs but produce separate reports. Delegate both phases to parallel Codex sub-agents simultaneously rather than waiting for Phase 2 to complete before
starting Phase 3. Collect both results before writing the combined report.

**When spawning parallel Codex subagents for Phase 2 and Phase 3, always pass:**
- The complete list of GDD file paths loaded in Phase 1 (explicit paths, not just counts)
- The run ID and complete path/hash input manifest from Phase 1d
- The full TR registry contents if loaded in Phase 1b (paste the registry text, not just a file path)
- The specific checklist items assigned to that agent's phase (Phase 2 gets 2a–2f; Phase 3 gets 3a–3g)
- The engine name and version from `.codex/docs/technical-preferences.md` and `docs/engine-reference/[engine]/VERSION.md`

Do not rely on the subagent to re-read these files — it has its own context window and cannot access Phase 1 results unless they are explicitly passed in the delegation prompt.
Require each worker to echo the run ID and input hashes it used, identify the
checks it completed, and enumerate unchecked scope. A missing/mismatched hash,
worker error, or incomplete required phase makes the merged verdict `PARTIAL`.

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

### Evidence and severity boundary for Phase 3

Phase 3 does not turn general design advice into architecture blockers. Record
each observation as `HYPOTHESIS / ADVISORY` and include:

1. the exact hashed GDD evidence;
2. assumptions needed for the hypothesis to hold;
3. at least one plausible counterexample or compensating mechanic;
4. a concrete validation plan (simulation, telemetry, playtest, or owner review);
5. the owner-approved invariant or threshold, if one actually exists.

Absent a reproducible violation of an explicit anti-pillar, owner-approved
invariant, or owner-approved threshold in the input manifest, Phase 3 findings
may contribute to `CONCERNS` but never `FAIL`. Missing measurement is reported
as `NEEDS_MEASUREMENT`, not as proof of imbalance, overload, or dominance.

### 3a: Progression Loop Competition

A project may intend one dominant progression loop, several co-equal loops, or
a deliberately open structure. Do not assume one model is universally correct.
Compare the GDDs with the project's explicit pillars and owner-approved loop
invariants; otherwise record loop competition only as a hypothesis to validate.

Scan all GDDs for systems that:
- Award the player's primary resource (XP, levels, prestige, unlocks)
- Define themselves as the "core" or "main" loop
- Have comparable depth and time investment to other systems doing the same

```
💡 HYPOTHESIS / ADVISORY — Competing Progression Loops
combat.md: Awards XP, unlocks abilities, is described as "the core loop"
crafting.md: Awards XP, unlocks recipes, is described as "the primary activity"
exploration.md: Awards XP, unlocks map areas, described as "the main driver"
→ Hypothesis: overlapping claims may make progression intent unclear.
  Assumption: the loops target the same players and session moments.
  Counterexample: the game may intentionally support distinct play styles.
  Validate: owner confirms the intended loop hierarchy, then playtest choice
  distribution and abandonment before changing scope.
```

### 3b: Player Attention Budget

Count how many systems require active player attention simultaneously during
a typical session. Each actively-managed system costs attention:

- Active = player must make decisions about this system regularly during play
- Passive = system runs automatically, player sees results but doesn't manage it

Do not apply a universal "3-4 systems" limit. Present the count, decision
frequency, time pressure, UI support, audience, and any owner-approved attention
budget. Without such a budget or player evidence, exceeding a heuristic count
is an advisory hypothesis only:

```
💡 HYPOTHESIS / ADVISORY — Cognitive Load Risk
Simultaneously active systems during [core loop moment]:
  1. [system-a].md — [decision type] (active)
  2. [system-b].md — [resource management] (active)
  3. [system-c].md — [tracking] (active)
  4. [system-d].md — [item/action use] (active)
  5. [system-e].md — [cooldown/timer management] (active)
  6. [system-f].md — [coordination decisions] (active)
→ Hypothesis: six concurrent decision channels may exceed the intended audience's
  attention budget.
  Assumptions: all six demand frequent decisions under the same time pressure.
  Counterexample: strong automation, pausing, or staged UI may keep load low.
  Validate: measure decision frequency/errors in a representative playtest or
  compare against an owner-approved attention budget.
```

### 3c: Dominant Strategy Detection

A dominant strategy, if demonstrated in the intended play context, can make
alternatives irrelevant. Look for evidence that could support or falsify that
hypothesis:

- **Resource monopolies**: One strategy generates a resource significantly
  faster than all others
- **Risk/reward evidence**: measured outcomes for strategies with different risk
- **Trade-off evidence**: whether an option is superior across approved dimensions
- **Choice evidence**: simulation, telemetry, or playtests showing alternatives
  are consistently irrelevant

```
💡 HYPOTHESIS / ADVISORY — Potential Dominant Strategy
combat.md: Ranged attacks deal 80% of melee damage with no risk
combat.md: Melee attacks deal 100% damage but require close range
→ The damage values alone do not prove dominance.
  Assumptions: safety is materially higher and no hidden costs or encounter
  constraints compensate for it.
  Counterexample: melee may provide AOE, stagger, mobility, or regeneration.
  Validate: simulate encounter outcomes and compare strategy pick/win rates.
```

### 3d: Economic Loop Analysis

Identify all resources across all GDDs (gold, XP, crafting materials, stamina,
health, mana, etc.). For each resource, map its **sources** (how players gain
it) and **sinks** (how players spend it).

Record these as economic hypotheses unless dimension/range evidence and an
owner-approved invariant make the violation reproducible:

| Condition | Sign | Risk |
|-----------|------|------|
| **Infinite source, no sink** | Resource may accumulate over the modeled horizon | Validate whether surplus erodes intended choices |
| **Sink, no source** | Resource may drain toward zero | Validate availability across intended sessions |
| **Source >> Sink** | Modeled surplus may grow | Validate whether the resource loses decision value |
| **Sink >> Source** | Modeled scarcity may persist | Validate frustration and gatekeeping risk |
| **Positive feedback loop** | More resource may accelerate acquisition | Validate snowball magnitude and caps |
| **No catch-up** | Deficit may accelerate | Validate recovery paths and terminal states |

```
💡 HYPOTHESIS / ADVISORY — Possible Unbounded Positive Feedback
gold economy:
  Sources: monster drops (scales with player power), merchant selling (unlimited)
  Sinks: equipment purchase (one-time), ability upgrades (finite count)
→ Hypothesis: after finite purchases, gold may accumulate without a meaningful
  sink. Counterexample: capped runs, resets, or unlisted recurring sinks may
  bound accumulation. Validate with a source/sink simulation across the intended
  play horizon before recommending new sinks.
```

### 3e: Difficulty Curve Consistency

When multiple systems scale with player progression, compare their directions,
rates, units, domains, caps, and the project's approved difficulty targets.
Curve differences are not defects by themselves.

For each system that scales over time, extract:
- What scales (enemy health, player damage, resource cost, area size)
- How it scales (linear, exponential, stepped)
- When it scales (level, time, area)

Compare all scaling curves. Treat a mismatch as a hypothesis until units,
domains, caps, encounter cadence, and an owner-approved target are verified:

```
💡 HYPOTHESIS / ADVISORY — Difficulty Curve Mismatch
combat.md: Enemy health scales exponentially with area (×2 per area)
progression.md: Player damage scales linearly with level (+10% per level)
→ Hypothesis: the stated curves may widen the time-to-kill gap.
  Counterexample: abilities, party size, caps, or area cadence may compensate.
  Validate with unit-checked simulation against the owner-approved difficulty
  target; do not infer inaccessibility from these two formulas alone.
```

### 3f: Pillar Alignment

Check whether each system documents a relationship to the approved design
pillars. A missing or ambiguous mapping is evidence for an owner clarification,
not proof that the system is scope creep.

For each GDD system, check its Player Fantasy section against the design pillars.
When alignment is interpretive, record it as a hypothesis rather than a blocker:

```
💡 HYPOTHESIS / ADVISORY — Possible Pillar Drift
fishing-system.md: Player Fantasy — "peaceful, meditative activity"
Pillars: "Brutal Combat", "Tense Survival", "Emergent Stories"
→ Hypothesis: the connection to an approved pillar is not documented.
  Counterexample: fishing may create tense survival decisions through food,
  exposure, or risk. Validate with the owner; do not recommend cutting solely
  from a missing textual mapping.
```

Also check anti-pillars — flag any system that does what an anti-pillar
explicitly says the game will NOT do:

```
🔴 Deterministic Anti-Pillar Violation
Anti-Pillar: "We will NOT have linear story progression — player defines their path"
main-quest.md: Defines a 12-chapter linear story with mandatory sequence
→ This may block only when the anti-pillar is explicit and current, the
  conflicting rule is quoted from a hashed input, and no scoped exception is
  present. Otherwise downgrade it to an advisory clarification request.
```

### 3g: Player Fantasy Coherence

Compare player fantasies with any explicit, owner-approved identity invariant.
Different fantasies may be complementary, contextual, or intentionally
contrasting; textual difference alone does not demonstrate identity confusion.

```
💡 HYPOTHESIS / ADVISORY — Player Fantasy Conflict
combat.md: "You are a ruthless, precise warrior — every kill is earned"
dialogue.md: "You are a charismatic diplomat — violence is always avoidable"
exploration.md: "You are a reckless adventurer — diving in without a plan"
→ Hypothesis: these identities may feel incoherent.
  Counterexample: the intended fantasy may be a versatile character whose
  identity changes by context. Validate against an explicit fantasy invariant
  and representative player interpretation before treating this as a defect.
```

---

## Required continuation

Before continuing, read [references/continued-workflow.md](references/continued-workflow.md) in full. It contains the remaining required phases, output formats, recovery rules, and handoff instructions; execute them in order.
