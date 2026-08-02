---
name: team-combat
description: "Orchestrate the combat team: coordinates game-designer, gameplay-programmer, ai-programmer, technical-artist, sound-designer, and qa-tester to design, implement, and validate a combat feature end-to-end."
---

## Invocation and execution

Invoke this workflow as `$team-combat`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[combat feature description]`. The description is required. This
team workflow has no director-gate review flag; every core role runs when its
feature responsibility applies.

**Argument check:** If no combat feature description is provided, output:
> "Usage: `$team-combat [combat feature description]` — Provide a description of the combat feature to design and implement (e.g., `melee parry system`, `ranged weapon spread`)."
Then stop immediately without spawning any subagents or reading any files.

When this skill is invoked with a valid argument, orchestrate the combat team through a structured pipeline.

**Decision Points:** Use approve / revise / stop choices at Design →
Architecture, the existing Architecture → Implementation gate, Implementation →
Integration, and Integration → QA. A stop produces a partial BLOCKED report; a
revision re-runs only the affected phase. These are substantive phase decisions,
not repeated file approvals.

## Team Composition
- **game-designer** — Design the mechanic, define formulas and edge cases
- **gameplay-programmer** — Implement the core gameplay code
- **ai-programmer** — Implement NPC/enemy AI behavior for the feature
- **technical-artist** — Create VFX, shader effects, and visual feedback
- **sound-designer** — Define audio events, impact sounds, and ambient combat audio
- **engine specialist** (primary) — Validate architecture and implementation patterns are idiomatic for the engine (read from `docs/technical-preferences.md` Engine Specialists section)
- **qa-tester** — Write test cases and validate the implementation

## How to Delegate

Use the Codex subagent delegation to spawn each team member as a subagent:
- `subagent_type: game-designer` — Design the mechanic, define formulas and edge cases
- `subagent_type: gameplay-programmer` — Implement the core gameplay code
- `subagent_type: ai-programmer` — Implement NPC/enemy AI behavior
- `subagent_type: technical-artist` — Create VFX, shader effects, visual feedback
- `subagent_type: sound-designer` — Define audio events, impact sounds, ambient audio
- `subagent_type: [primary engine specialist]` — Engine idiom validation for architecture and implementation
- `subagent_type: qa-tester` — Write test cases and validate implementation

Always provide full context in each agent's prompt (design doc path, relevant code files, constraints). Launch independent agents in parallel where the pipeline allows it (e.g., Phase 3 agents can run simultaneously).

## Pipeline

### Phase 1: Design
Normalize the feature name to a lowercase alphanumeric/hyphen slug, rejecting
path separators/traversal and an empty result. Resolve one exact
`design/gdd/[slug].md` path and include the corresponding existing
`design/gdd/systems-index.md` update in the later changeset. A collision is an
explicit update choice, never overwrite-by-name.

If that GDD exists, game-designer first checks all eight required sections under
`design/AGENTS.md`; missing decisions must be revised before Architecture.
For a new or validated existing GDD, delegate to **game-designer** as
analysis-only. It returns a complete GDD draft
in conversation and must not create/update files yet. The draft covers: mechanic overview, player fantasy, detailed rules, formulas with variable definitions, edge cases, dependencies, tuning knobs with safe ranges, and acceptance criteria
- Decide and record whether AI behavior is part of the feature. That decision
  controls both Architecture and Implementation; when false, ai-programmer is
  N/A in both phases and in the summary.
- Output: completed design-document draft

Present approve / revise / stop before Architecture.

### Phase 2: Architecture
Delegate to **gameplay-programmer** (with **ai-programmer** if AI is involved)
as analysis-only; neither writes files:
- Review the design document
- Design the code architecture: class structure, interfaces, data flow
- Identify integration points with existing systems
- Output: architecture sketch with file list and interface definitions

Read the configured engine before specialist delegation. If no real engine and
specialist are configured, do not spawn a placeholder. Keep the architecture
engine-agnostic, report **BLOCKED** for implementation, recommend `$setup-engine`,
and stop before Phase 3.

When configured, read the matching existing
`docs/engine-reference/[engine]/VERSION.md` and pass its pinned version to the
**primary engine specialist** with the architecture and GDD path. If the version
reference is missing, mark version validation unavailable and stop making
specific API/deprecation claims until it is supplied. Spawn the specialist to
validate the proposed architecture:
- Is the class/node/component structure idiomatic for the pinned engine? (e.g., Godot node hierarchy, Unity MonoBehaviour vs DOTS, Unreal Actor/Component design)
- Are there engine-native systems that should be used instead of custom implementations?
- Any proposed APIs that are deprecated or changed in the pinned engine version?
- Output: engine architecture notes — incorporate into the architecture before Phase 3 begins

Ask the user directly:
- Prompt: "Architecture sketch complete. Approve to proceed with parallel implementation."
- Options:
  - `[A] Proceed — spawn implementation agents (gameplay-programmer, ai-programmer, technical-artist, sound-designer)`
  - `[B] Revise the architecture first — I'll describe what needs to change`
  - `[C] Stop here — I'll continue later`

Before offering [A], the Phase 2 file list must assign every proposed GDD,
implementation asset/code path, and test path to exactly one writer. Parallel
owners must be non-overlapping; shared integration paths are reserved for the
Phase 4 gameplay-programmer and assigned to no Phase 3 writer. Present every
exact path and intended modification as the complete changeset. Only after the
user approves that architecture and authorizes this changeset may Phase 1's
GDD draft be written by game-designer and implementation agents spawn.

Only spawn implementation agents if user selects [A] and the complete changeset
is authorized.

### Phase 3: Implementation (parallel where possible)
Delegate in parallel using the exact, mutually exclusive paths assigned in
Phase 2:
- **gameplay-programmer**: Implement core combat mechanic code in its paths only
- **ai-programmer**: Implement AI behaviors in its paths only (if applicable)
- **technical-artist**: Create VFX/shader assets in its paths only
- **sound-designer**: Define audio events/mixing assets in its paths only

No Phase 3 agent may edit a shared integration path. If a new path is required,
stop and use the existing scope-expansion reauthorization rule.

After all applicable Phase 3 agents return, present their results with
approve / revise / stop before Integration. An AI-free feature has no AI spawn
and reports that role N/A.

### Phase 4: Integration
Delegate the existing **gameplay-programmer** as the single integration owner.
It receives all Phase 3 results and may edit only the shared integration paths
reserved and approved in Phase 2:
- Wire together gameplay code, AI, VFX, and audio
- Ensure all tuning knobs are exposed and data-driven
- Verify the feature works with existing combat systems

Other Phase 3 agents may review their interfaces but must not write shared files.

Present the integrated result with approve / revise / stop before QA.

### Phase 5: Validation
Delegate to **qa-tester**:
- Write test cases from the acceptance criteria
- Test all edge cases documented in the design
- Verify performance impact is within budget
- List discovered bugs in the validation result. Write a bug file only when its
  exact path was already included in the approved Phase 2 changeset; otherwise
  keep the finding in conversation/summary and do not create an unapproved file.

### Phase 6: Sign-off
- Collect results from all team members
- Report feature status using these exhaustive rules:
  - **COMPLETE**: every required phase completed and all required tests and
    acceptance criteria passed
  - **NEEDS WORK**: implementation is present and required verification ran,
    with only fixable non-blocking defects remaining
  - **BLOCKED**: a required phase failed; engine/ADR dependency is unresolved;
    critical tests could not run; or any required test/acceptance criterion failed
- List every outstanding issue and its assigned owner

## Error Recovery Protocol

If any spawned agent (through Codex subagent delegation) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** by asking the user directly with choices:
   - Skip this agent and note the gap in the partial report (a skipped required
     role remains unresolved and forces final BLOCKED)
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Common blockers:
- Input file missing (story not found, GDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `$architecture-decision` first
- Scope too large → split into two stories via `$create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess

## File Write Protocol

Phase 1–2 subagents are analysis-only. Once architecture defines exact,
non-overlapping paths, the orchestrator obtains one combined changeset approval.
The game-designer then writes only the approved GDD, each Phase 3 agent writes
only its assigned paths, the gameplay-programmer alone writes reserved shared
integration paths, and qa-tester writes only approved test paths. This
orchestrator does not write files directly.

## Output

A summary report covering: design completion status, implementation status per team member, test results, and any open issues.

Verdict: **COMPLETE** — combat feature designed, implemented, and validated.
Verdict: **NEEDS WORK** — implementation exists with only fixable non-blocking defects.
Verdict: **BLOCKED** — a required phase/dependency/test could not pass; partial report produced with unresolved items listed.

## Next Steps

- Run `$code-review` on the implemented combat code before closing stories.
- Run `$balance-check` to validate combat formulas and tuning values.
- Run `$team-polish` if VFX, audio, or performance polish is needed.
