---
name: perf-profile
description: "Structured performance profiling workflow. Identifies bottlenecks, measures against budgets, and generates optimization recommendations with priority rankings."
---

## Invocation and execution

Invoke this workflow as `$perf-profile`.

Arguments: `[system-name | full | path/to/existing-profiler-data]`. A data path is a single existing profiler or benchmark file.

Delegate substantive work to the `performance-analyst` Codex subagent role when it is available. If that role is unavailable, follow the same responsibilities in the current agent.


## Phase 1: Determine Scope

Read the argument:

- System name → resolve it to an existing code/scene scope, then perform a static candidate scan for that scope. If it cannot be resolved uniquely, stop and ask; do not scan a guessed system.
- `full` → perform a static candidate scan across all systems and state the platforms and scenes actually covered. Unknown coverage remains an explicit limitation.
- Existing profiler/benchmark path → parse that file and perform measured budget analysis

With no argument, look only for an explicitly identified existing profiler data artifact. If none is available, output the target-engine/platform data-capture checklist and stop without a budget verdict. If a supplied data file cannot be parsed, report the file/error and stop; never fall back to estimated measurements.

---

## Phase 2: Load Performance Budgets

Read the configured engine, target platform, and language first. Apply only the matching engine's hot-path patterns. If the engine is unconfigured, use language-independent patterns and state that engine-specific coverage is unavailable; never combine Godot, Unity, and Unreal APIs in one assumed scan.

For measured runs, look for the nearest prior performance report only when it records the same target platform, scene/scenario, and metric definitions. Show deltas only for comparable metrics; otherwise state `historical comparison unavailable` and do not compare unlike runs.

Check for existing performance targets in design docs or AGENTS.md:

- Target FPS (e.g., 60fps = 16.67ms frame budget)
- Memory budget (total and per-system)
- Load time targets
- Draw call budgets
- Network bandwidth limits (if multiplayer)

Treat missing values and placeholders such as `[TO BE CONFIGURED]` as unconfigured. Ask for a target or report raw measurements only. Never substitute example values such as 16.67ms, and do not issue WITHIN BUDGET/CONCERNS/OVER BUDGET without a configured budget.

---

## Phase 3: Analyze Evidence

When profiler/benchmark data is present, derive every quantitative metric from that file and compare it only with configured project budgets. When no runtime data is present, the checks below are a static candidate scan only: report file:line candidates and a capture checklist; do not fill runtime values, Status, Estimated Current, or Expected gain, and do not issue a budget verdict.

**CPU Profiling Candidates:**
- `_process()` / `Update()` / `Tick()` functions — list locations and flag them for measurement; do not estimate cost
- Nested loops over large collections
- String operations in hot paths
- Allocation patterns in per-frame code
- Unoptimized search/sort over game entities
- Expensive physics queries (raycasts, overlaps) every frame

**Memory Profiling Targets:**
- Large data structures and their growth patterns
- Large texture/asset files to measure in the target runtime; do not infer resident memory
- Object pool vs instantiate/destroy patterns
- Leaked references (objects that should be freed but aren't)
- Cache sizes and eviction policies

**Rendering Targets (if applicable):**
- Rendering patterns whose draw calls must be measured
- Overdraw from overlapping transparent objects
- Shader complexity
- Unoptimized particle systems
- Missing LODs or occlusion culling

**I/O Targets:**
- Save/load performance
- Asset loading patterns (sync vs async)
- Network message frequency and size

---

## Phase 4: Generate Profiling Report

```markdown
## Performance Profile: [System or Full]
Generated: [Date]

### Performance Budgets
| Metric | Project Budget | Measured Current | Status |
|--------|----------------|------------------|--------|
| Frame time | [configured budget or unknown] | [from profiler data only] | [measured result or unavailable] |
| Memory | [configured budget or unknown] | [from profiler data only] | [measured result or unavailable] |
| Load time | [configured budget or unknown] | [from profiler data only] | [measured result or unavailable] |
| Draw calls | [configured budget or unknown] | [from profiler data only] | [measured result or unavailable] |

### Hotspots Identified
| # | Location | Issue | Estimated Impact | Fix Effort |
|---|----------|-------|------------------|------------|

`Fix Effort` is a relative implementation estimate: **S** = localized change, **M** = multi-file or system adjustment, **L** = architectural/cross-system work. It is not a schedule commitment.

### Optimization Recommendations (Priority Order)
1. **[Title]** — [Description]
   - Location: [file:line]
   - Expected direction: [non-numeric until verified with the same scenario]
   - Risk: [Low/Med/High]
   - Approach: [How to implement]

### Quick Wins (< 1 hour each)
- [Candidate optimization 1 — describe only the expected direction until the same scenario is benchmarked after implementation; do not claim a numeric gain without that measurement]

### Requires Investigation
- [Area that needs actual runtime profiling to confirm impact]
```

With runtime data and configured budgets, output measured headroom and exactly one verdict: **WITHIN BUDGET**, **CONCERNS**, or **OVER BUDGET**. Without both, output only candidates/raw measurements, limitations, and the next data-capture action; no budget verdict.

---

## Phase 5: Scope and Timeline Decision

Activate this phase only if any hotspot has Fix Effort rated M or L.

Present significant-effort items as non-executing next-step options only: investigate with a measured follow-up, consider `$scope-check [feature]`, or separately request an architectural decision. This workflow does not implement, schedule, write a backlog/known issue, or start another write workflow.

This skill is read-only — no files are written. A measured run uses the Phase 4 budget verdict; a static/no-budget run ends without one.

---

## Phase 6: Next Steps

- If bottlenecks require architectural change: run `$architecture-decision`.
- If scope reduction is needed: run `$scope-check [feature]`.
- To schedule optimizations: run `$sprint-plan update`.

### Rules
- Never optimize without measuring first — gut feelings about performance are unreliable
- Recommendations must include estimated impact — "make it faster" is not actionable
- Profile on target hardware, not just development machines
- Static analysis (this skill) identifies candidates; runtime profiling confirms
