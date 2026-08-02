---
name: team-audio
description: "Orchestrate audio team: audio-director + sound-designer + technical-artist + gameplay-programmer for full audio pipeline from direction to implementation."
---

## Invocation and execution

Invoke this workflow as `$team-audio`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[feature or area to design audio for]`. Treat bracketed values as optional unless the workflow says otherwise.


If no argument is provided, output usage guidance and exit without spawning any agents:
> Usage: `$team-audio [feature or area]` — specify the feature or area to design audio for (e.g., `combat`, `main menu`, `forest biome`, `boss encounter`). Do not ask the user directly here; output the guidance directly.

When this skill is invoked with an argument, orchestrate the audio team through a structured pipeline.

**Decision Points:** At each step transition, ask the user directly to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next step.

1. **Read the argument** for the target feature or area (e.g., `combat`,
   `main menu`, `forest biome`, `boss encounter`). Preserve that display
   name, but derive filenames only from a lowercase ASCII alphanumeric/hyphen
   slug. Reject path separators/traversal and an empty slug. If the resolved
   document already exists, show it as an explicit update in the changeset;
   never overwrite silently.

2. **Gather context**:
   - Match design docs by exact feature slug or an explicit reference. If
     multiple GDDs match, ask the user to choose; do not scan/import unrelated
     systems. With no matching GDD, report a design gap and tell audio-director
     its direction is provisional.
   - Read the sound bible at `design/gdd/sound-bible.md` if it exists. If it
     does not, state that project-wide sonic identity is unavailable, continue,
     and carry the limitation into the final summary.
   - Read existing audio asset lists in `assets/audio/`
   - Read any existing sound design docs for this area

## How to Delegate

Use the Codex subagent delegation to spawn each team member as a subagent:
- `subagent_type: audio-director` — Sonic identity, emotional tone, audio palette
- `subagent_type: sound-designer` — SFX specifications, audio events, mixing groups
- `subagent_type: technical-artist` — Audio middleware, bus structure, memory budgets
- `subagent_type: [primary engine specialist]` — Validate audio integration patterns for the engine
- `subagent_type: gameplay-programmer` — Audio manager, gameplay triggers, adaptive music

Always provide full context in each agent's prompt (feature description, existing audio assets, design doc references).

3. **Orchestrate the audio team** in sequence:

Steps 1–3 are analysis-only. Every subagent returns its direction, event list,
accessibility findings, and technical plan in conversation and must not create or
edit files. This makes the complete Step 4 changeset knowable before delegation.

### Step 1: Audio Direction (audio-director)
Spawn the `audio-director` agent to:
- Define the sonic identity for this feature/area
- Specify the emotional tone and audio palette
- Set music direction (adaptive layers, stems, transitions)
- Define audio priorities and mix targets
- Establish any adaptive audio rules (combat intensity, exploration, tension)

### Step 2: Sound Design and Audio Accessibility (parallel)
Spawn the `sound-designer` agent to:
- Create detailed SFX specifications for every audio event
- Define sound categories (ambient, UI, gameplay, music, dialogue)
- Specify per-sound parameters (volume range, pitch variation, attenuation)
- Plan audio event list with trigger conditions
- Define mixing groups and ducking rules

Spawn the `accessibility-specialist` agent in parallel, using the Step 1
planned cue inventory (not a not-yet-produced event list), to:
- Identify which audio events carry critical gameplay information (damage received, enemy nearby, objective complete) and require visual alternatives for hearing-impaired players
- Specify subtitle requirements: which audio events need captions, what text format, on-screen duration
- Check that no gameplay state is communicated by audio alone (all must have a visual fallback)
- Review the audio event list for any that could cause issues for players with auditory sensitivities (high-frequency alerts, sudden loud events)
- Output: audio accessibility requirements list integrated into the audio event spec

After sound-designer returns the actual event list, have
accessibility-specialist perform the final Step 2 check against that exact list
before the Step 2 decision. No planned cue may substitute for this final check.

If any critical gameplay cue lacks a visual, haptic, or text alternative, the
pipeline is **BLOCKED**. Step 3 may continue as analysis, but do not enter Step 4,
write a document, or allow COMPLETE until the sound/accessibility design is
revised and the accessibility-specialist confirms the gap is no longer blocking.

### Step 3: Technical Implementation (parallel)
Spawn the `technical-artist` agent to:
- Define audio bus structure/routing and platform memory budgets
- Plan streaming vs preloaded asset strategy
- Specify audio-reactive VFX constraints
- Do not own middleware/code integration decisions; the engine specialist
  validates engine patterns and gameplay-programmer owns Step 4 integration

Spawn the **primary engine specialist** in parallel (from `docs/technical-preferences.md` Engine Specialists) to validate the integration approach:
- Is the proposed audio middleware integration idiomatic for the engine? (e.g., Godot's built-in AudioStreamPlayer vs FMOD, Unity's Audio Mixer vs Wwise, Unreal's MetaSounds vs FMOD)
- Any engine-specific audio node/component patterns that should be used?
- Known audio system changes in the pinned engine version that affect the integration plan?
- Output: engine audio integration notes to merge with the technical-artist's plan

If no engine is configured, skip the specialist spawn and mark engine
integration as deferred. Step 4 must not write engine-specific source or tests;
instead gameplay-programmer returns implementation tasks in conversation. The
audio design document may still be COMPLETE as a design deliverable when every
other required output is present and the deferral is explicit.

At the end of each Step 1–3, present `approve / revise / stop` choices for the
actual direction, event/accessibility set, or technical plan. Stop produces a
partial BLOCKED summary and does not start dependent work; revise re-runs the
affected analysis. These are product decisions, not file approvals.

### Step 4: Authorized Code and Document Integration

After Step 3 is consolidated, identify the exact final
`design/audio/audio-[feature-slug].md` path plus every implementation and test
path needed below. Present their intended edits as one complete changeset and
obtain authorization. Do not use directory globs or allow a subagent to add an
unlisted file; material expansion requires the existing reauthorization rule.

After authorization, spawn the `gameplay-programmer` as the sole owner of the
listed code/test paths to:
- Implement audio manager system or review existing
- Wire up audio events to gameplay triggers
- Implement adaptive music system (if specified)
- Set up audio occlusion/reverb zones
- Write unit tests for audio event triggers
- Run the affected configured tests when a runner is available and report the
  actual command/result. If unavailable, record `tests deferred/not run`;
  never claim they passed.

4. After code integration, spawn the existing `audio-director` as the sole owner
of the approved `design/audio/audio-[feature-slug].md` path. It compiles all
confirmed team outputs and implementation references into that document and
writes no other file. The gameplay-programmer does not edit the audio document.

5. **Save only to** `design/audio/audio-[feature-slug].md`.

   Note: If `design/audio/` does not exist, the audio-director may create it as
   part of writing the already approved exact document path.

6. **Output a summary** with: audio event count, estimated asset count,
   implementation tasks, and any open questions between team members.

Verdict: **COMPLETE** only when all required design outputs exist, no critical
accessibility blocker remains, and the audio document write succeeds. With a
configured engine, required implementation/test work must also complete and
actual test status must be reported; unavailable tests are recorded as deferred,
not passed. With no configured engine, COMPLETE applies only to the explicitly
deferred design document and no engine-specific source may be written.

If any required step or write fails, or the pipeline stops because a dependency is unresolved (e.g., critical accessibility gap or missing GDD not resolved by the user):

Verdict: **BLOCKED** — [reason]

## File Write Protocol

Steps 1–3 are analysis-only and perform no writes. After their results determine
exact paths, the orchestrator obtains one combined changeset approval. The
gameplay-programmer writes only the approved implementation/test paths, and the
audio-director alone writes the approved audio document. This orchestrator does
not write files directly; neither writer may expand its boundary without the
existing reauthorization rule.

## Next Steps

- Review the audio design doc with the audio-director before implementation begins.
- Use `$dev-story` to implement the audio manager and event system once the design is approved.
- Run `$asset-audit` after audio assets are created to verify naming and format compliance.

## Error Recovery Protocol

If any spawned agent (through Codex subagent delegation) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** by asking the user directly with choices:
   - Skip this agent and note the gap in the partial report (not available for a
     blocking critical-gameplay accessibility gap)
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Common blockers:
- Input file missing (story not found, GDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `$architecture-decision` first
- Scope too large → split into two stories via `$create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess
