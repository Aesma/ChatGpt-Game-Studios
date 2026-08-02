---
name: team-polish
description: "Orchestrate the polish team: coordinates performance-analyst, technical-artist, sound-designer, and qa-tester to optimize, polish, and harden a feature or area for release quality."
---

## Invocation and execution

Invoke this workflow as `$team-polish`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[feature or area to polish]`. Reject unknown flags and extra control arguments with usage and exit before delegation.

If no argument is provided, output usage guidance and exit without spawning any agents:
> Usage: `$team-polish [feature or area]` — specify the feature or area to polish (e.g., `combat`, `main menu`, `inventory system`, `level-1`). Do not ask the user directly here; output the guidance directly.

When this skill is invoked with an argument, orchestrate the polish team through a structured pipeline.

**Decision Points:** At each phase transition, ask the user directly to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase.

## Team Composition
- **performance-analyst** — Profiling, optimization, memory analysis, frame budget
- **engine-programmer** — Engine-level bottlenecks: rendering pipeline, memory, resource loading (invoke when performance-analyst identifies low-level root causes)
- **technical-artist** — VFX polish, shader optimization, visual quality
- **sound-designer** — Audio polish, mixing, ambient layers, feedback sounds
- **tools-programmer** — Content pipeline tool verification, editor tool stability, automation fixes (invoke when content authoring tools are involved in the polished area)
- **qa-tester** — Edge case testing, regression testing, soak testing

## How to Delegate

Use the Codex subagent delegation to spawn each team member as a subagent:
- `subagent_type: performance-analyst` — Profiling, optimization, memory analysis
- `subagent_type: engine-programmer` — Engine-level fixes for rendering, memory, resource loading
- `subagent_type: technical-artist` — VFX polish, shader optimization, visual quality
- `subagent_type: sound-designer` — Audio polish, mixing, ambient layers
- `subagent_type: tools-programmer` — Content pipeline and editor tool verification
- `subagent_type: qa-tester` — Edge case testing, regression testing, soak testing

Always provide full context in each agent's prompt (target feature/area, performance budgets, known issues). Launch independent agents in parallel where the pipeline allows it (e.g., Phases 3 and 4 can run simultaneously).

Before parallel delegation, assign every candidate file to one writer. If performance and visual work overlap on a shader, particle asset, render configuration, or draw-call resource, give that path to one responsible agent and make the other agent advisory for that path.

## Pipeline

### Phase 1: Assessment
Resolve the argument to one concrete feature/area, its runnable build entry, related
assets/configuration, and the applicable performance-budget source. If multiple
features share the name or more than one build entry is plausible, list candidates
and wait for the user to choose; do not profile or write against an assumed target.

Choose one profiling execution entry for this run. The orchestrator may run the
existing `$perf-profile` workflow and hand its result to the performance-analyst,
or the performance-analyst may perform the same checks directly; never run both
and create competing baselines.

Delegate to **performance-analyst**:
- Profile the uniquely resolved target through `$perf-profile [existing-profiler-data-path]`
  when claiming runtime budget results. A system/full static scan supplies
  candidates only and cannot prove a frame/memory budget.
- Identify performance bottlenecks and frame budget violations only from actual
  comparable measurements and configured budgets
- Measure memory usage and check for leaks
- Benchmark against target hardware specs
- Identify the concrete code, shader, VFX, audio, configuration, test-result, and report files that the pass may change; assign each to one owner
- Output: performance report with prioritized optimization list and candidate-file ownership map

During Assessment, determine whether the resolved target includes content-authoring
or editor-tool files. If so, assign those already identified files to
**tools-programmer** for stability/automation checks; otherwise omit that role from
this run. Do not list a conditional role that the pipeline can never dispatch.

Read performance targets only from the existing technical preferences/budget
documents. If no applicable budget is configured, report the missing criterion
and end with NEEDS MORE WORK; do not invent 60fps, memory, platform, or hardware
targets.

After Phase 1, present those concrete files and intended changes as the single changeset and obtain approval before Phases 2–4 write anything. All before metrics must describe the same approved baseline. A newly discovered bug report or unlisted repair path is a material scope expansion and must be added through the existing revised-changeset rule.

### Phase 2: Optimization
Delegate to **performance-analyst** (with relevant programmers as needed):
- Fix performance hotspots identified in Phase 1
- Optimize draw calls, reduce overdraw
- Fix memory leaks and reduce allocation pressure
- Verify optimizations don't change gameplay behavior
- Output: optimized code with before/after metrics

Performance after metrics are measured only after the authorized outputs from Phases 2–4 are combined into one candidate version; do not compare a Phase 1 baseline with an intermediate file version.

If Phase 1 identified engine-level root causes (rendering pipeline, resource loading, memory allocator), delegate those fixes to **engine-programmer** in parallel:
- Optimize hot paths in engine systems
- Fix allocation pressure in core loops
- Output: engine-level fixes with profiler validation

### Phase 3: Visual Polish (parallel with Phase 2)
Delegate to **technical-artist**:
- Review VFX for quality and consistency with art bible
- Optimize particle systems and shader effects
- Add screen shake, camera effects, and visual juice where appropriate
- Ensure effects degrade gracefully on lower settings
- Output: polished visual effects

Do not edit a shader, VFX asset, or rendering configuration owned by Phase 2; return recommendations to its owner instead.

### Phase 4: Audio Polish (parallel with Phase 2)
Delegate to **sound-designer**:
- Review audio events for completeness (are any actions missing sound feedback?)
- Check audio mix levels — nothing too loud or too quiet relative to the mix
- Add ambient audio layers for atmosphere
- Verify audio plays correctly with spatial positioning
- Output: audio polish list and mixing notes

### Phase 5: Hardening
Delegate to **qa-tester**:
- Test all edge cases: boundary conditions, rapid inputs, unusual sequences
- Soak test: run the feature for extended periods checking for degradation
- Stress test: maximum entities, worst-case scenarios
- Regression test: verify polish changes haven't broken existing functionality
- Test on minimum spec hardware (if available)
- For every required check, record `executed` with PASS/FAIL, or `not run` with the concrete reason. Do not infer execution from code inspection or simulate unavailable hardware/builds.
- Output: test results with any remaining issues and explicit executed/not-run status

### Phase 6: Sign-off
- Collect results from all team members
- Compare performance metrics against budgets
- READY FOR RELEASE requires the combined candidate to meet budgets, all release-critical regression/stress/target-hardware checks to have actually run and passed, and no unresolved blocker from performance, visual, audio, or QA work
- If a release-critical check did not run, a regression remains, or required evidence is unknown, report NEEDS MORE WORK and list the missing evidence; never convert `not run` into PASS
- Report: READY FOR RELEASE / NEEDS MORE WORK
- List any remaining issues with severity and recommendations

## Error Recovery Protocol

If any spawned agent (through Codex subagent delegation) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** by asking the user directly with choices:
   - Skip only advisory work that cannot affect release readiness and note the gap in the final report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Performance baseline/combined-candidate measurement, final regression/stress
evidence, and the owner of any identified blocker are required. If one fails,
stop dependent work and return NEEDS MORE WORK with a partial report; Skip cannot
turn missing critical evidence into READY FOR RELEASE.

Common blockers:
- Input file missing (story not found, GDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `$architecture-decision` first
- Scope too large → split into two stories via `$create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess

## File Write Protocol

All file writes (performance reports, test results, evidence docs) are delegated to
sub-agents spawned through Codex subagent delegation. After Phase 1 identifies candidate files and assigns one owner to each, the orchestrator obtains one combined changeset approval before delegation. Each sub-agent writes only its assigned paths within that boundary without prompting again. This orchestrator does not write files directly.

## Output

A summary report covering: performance before/after metrics, visual polish changes, audio polish changes, test results, and release readiness assessment.

## Next Steps

- If READY FOR RELEASE: run `$release-checklist` for the final pre-release validation.
- If NEEDS MORE WORK: schedule remaining issues in `$sprint-plan update` and re-run `$team-polish` after fixes.
- Run `$gate-check` for a formal phase gate verdict before handing off to release.
