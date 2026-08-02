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

1. **Cross-GDD Consistency** — contradictions, stale references, and ownership conflicts
2. **Game Design Holism** — issues that only emerge when you see all systems together

**This is distinct from `$design-review`**, which reviews one GDD for internal
completeness. This skill reviews the relationships between all GDDs.

**When to run:**
- After all MVP-tier GDDs are individually approved
- After any GDD is significantly revised mid-production
- Before `$create-architecture` begins

**Focus modes:**

- no argument / `full`: both consistency and design-theory passes
- `consistency`: consistency only
- `design-theory`: design theory only
- `since-last-review`: full check over the GDDs selected since the last report

---

## Phase 1: Load Everything

### Phase 1a — L0: Summary Scan

Read `design/gdd/systems-index.md` first. Build the system-GDD manifest only
from explicit Design Doc paths whose files exist. Treat concept, pillars, and
index files as context; exclude prior `gdd-cross-review-*` reports. Extract a
`## Summary` when present, otherwise summarize from the title and `## Overview`
without treating the absent Summary as a defect.

For `since-last-review`, locate the most recent existing
`design/gdd/gdd-cross-review-*.md` by its recorded report date, using the path
only as a deterministic tie-breaker. If no report exists, say so and fall back
to `full`. Use Git to select system GDDs changed after that report. Expand the
selection only through standard `Dependencies` / `Depends On` entries and the
systems-index dependency field; do not use a non-standard "Key deps" field.

Display the manifest and selected scope before full reads.

### Phase 1b — Registry Pre-Load

Read `design/registry/entities.yaml` when it exists. Treat it as a candidate
name/source index that accelerates searches, not as authoritative truth. Every
conflict conclusion must cite the current source GDD text. If the registry is
empty, continue with full reads and note the limitation.

### Phase 1c — L1/L2: Full Document Load

Read in full:

1. `design/gdd/game-concept.md`;
2. `design/gdd/game-pillars.md` when present;
3. `design/gdd/systems-index.md`;
4. every selected system GDD listed by systems-index.

Report the loaded systems, pillars, and anti-pillars. If fewer than two system
GDDs exist, stop and explain that a cross-GDD review requires at least two.

### Parallel Execution

Respect focus mode. In `full`, Phase 2 and Phase 3 are independent. Before
delegating, check available capacity. Start at most one bounded subtask for each
phase (two total). If capacity is unavailable, run the phases sequentially in
the current agent. Single-focus modes run only their selected phase;
`since-last-review` runs both over its selected set.

Pass each delegated subtask the explicit GDD paths, registry text as candidate
index, assigned checklist, and engine/version context. Collect every started
subtask. A failure produces the continuation's partial-coverage handling and
cannot be hidden inside a complete verdict.

---

## Phase 2: Cross-GDD Consistency

### 2a: Dependency References

For every standard `Dependencies` / `Depends On` entry, verify the target
exists, the forward dependency agrees with systems-index, and any explicitly
stated reverse relationship is not contradictory. Do not require reciprocal
dependents lists.

### 2b: Rule Contradictions

Check whether two documents define incompatible rules for the same situation,
including floor/ceiling rules, shared resource ownership, state transitions,
timing, and stacking. Every conclusion cites both GDDs and their exact sections.

Scan specifically for:
- a minimum/maximum in one GDD that another mechanic bypasses;
- two owners changing the same shared resource;
- incompatible descriptions of death, completion, or another shared event;
- synchronous versus asynchronous assumptions;
- incompatible stacking behavior.

Report the two statements and ask which existing GDD should become
authoritative; do not decide it in the review.

### 2c: Stale References

Verify that every cross-document mechanic, value, system, and formula reference
still exists with the stated behavior.

Examples include a referenced combo multiplier that no longer exists, a named
progression curve whose model changed, or an encumbrance formula replaced by a
flat limit. Cite the referencing and target sections.

### 2d: Data and Tuning Knob Ownership Conflicts

Scan Tuning Knobs sections for duplicate ownership claims over the same value or output.

Explain the concrete double-application or conflicting-authority risk rather
than flagging two similarly named but unrelated knobs.

### 2e: Formula Compatibility

For connected formulas, compare documented output/input ranges, units, event
frequency, and the time horizon over which they interact. If any required
range, frequency, unit, or duration is absent, report the undefined input and
do not infer a single-event outcome, surplus, deficit, or severity conclusion.

When evidence is complete, report the upstream range, downstream expected
range, relevant frequency/horizon, and the exact mismatch. Treat compatibility
questions as design judgment unless they create an explicit contradiction.

### 2f: Acceptance Criteria Cross-Check

Flag acceptance criteria that cannot both pass in the same documented scenario.

Name the shared scenario and show why the two criteria are mutually exclusive.

---

## Phase 3: Game Design Holism

The checks in this phase are contextual heuristics, not universal laws. When
target-player, genre, session structure, or core-loop context is missing, report
the hypothesis as a risk to validate rather than a blocker.

### 3a: Progression Loop Competition

Map systems that award primary progression resources or claim to be core/main.
Multiple deep loops may be intentional; do not require exactly one dominant
loop. Flag only evidence-backed competition for the same player goal/resource,
and label uncertain cases as validation risks.

Consider award type, unlock depth, time investment, and how supporting loops
feed a larger goal. Genre conventions and intentionally plural progression are
valid contextual counter-evidence.

### 3b: Player Attention Budget

Count simultaneously active decisions in a specific documented gameplay moment.
The common 3–4 item range is a heuristic, not a hard limit. Without target-player
or moment-specific evidence, report "attention-load hypothesis — validate" and
never make the count alone a blocker.

Distinguish active decisions from passive state displays. List the selected
moment and each active system so the heuristic is auditable.

### 3c: Dominant Strategy Detection

Look for resource monopolies, risk-free power, missing trade-offs, and clearly
superior paths. Require comparable quantitative/contextual evidence; otherwise
state which values are undefined.

Compare reward, risk, opportunity cost, and applicability in the same scenario;
a qualitative label such as "safe" is not sufficient without supporting rules.

### 3d: Economic Loop Analysis

Map sources and sinks for each resource. Do not conclude source >> sink, sink >>
source, unbounded accumulation, or positive feedback without documented amount,
frequency, caps, and relevant duration. Missing inputs are data gaps, not
economic verdicts.

Potential conditions to examine once evidence exists include infinite source
with no ongoing sink, sink with no source, surplus/scarcity, positive feedback,
and absence of catch-up. Record caps and one-time versus repeatable flows.

### 3e: Difficulty Curve Consistency

Compare only curves with defined variables, units, ranges, and progression
horizons. Missing numeric evidence is reported rather than filled in.

Extract what scales, the mathematical/step model, and the trigger (level, time,
area, etc.) before comparing curves.

### 3f: Pillar Alignment

Check Player Fantasy sections against pillars and anti-pillars. A direct
anti-pillar contradiction is stronger evidence than an absent mapping; do not
invent alignment requirements for an undocumented pillar set.

For a flagged system, cite the fantasy and pillar/anti-pillar text and explain
the relationship. Absence of a mapping is a warning or unassessed gap, not an
automatic scope-creep verdict.

### 3g: Player Fantasy Coherence

Compare fantasies in their documented player roles and contexts. Different
fantasies are not automatically incompatible; cite the concrete identity or
choice conflict.

Ask whether apparently different fantasies reinforce a broader identity from
different angles before calling them incoherent.

---

## Required continuation

Before continuing, read [references/continued-workflow.md](references/continued-workflow.md) in full. It contains the remaining required phases, output formats, recovery rules, and handoff instructions; execute them in order.
