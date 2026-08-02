---
name: team-narrative
description: "Orchestrate the narrative team: coordinates narrative-director, writer, world-builder, and level-designer to create cohesive story content, world lore, and narrative-driven level design."
---

## Invocation and execution

Invoke this workflow as `$team-narrative`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[narrative content description]`. Reject unknown flags or extra control arguments with the usage message and exit without spawning agents.

If no argument is provided, output usage guidance and exit without spawning any agents:
> Usage: `$team-narrative [narrative content description]` — describe the story content, scene, or narrative area to work on (e.g., `boss encounter cutscene`, `faction intro dialogue`, `tutorial narrative`). Do not ask the user directly here; output the guidance directly.

When this skill is invoked with an argument, orchestrate the narrative team through a structured pipeline.

**Decision Points:** Ask the user only when a phase presents a meaningful narrative
choice. Present the subagent's proposals as selectable options, write the full
analysis in conversation, and capture the decision with concise labels. A phase
confirmation is a product decision, not another file-write authorization; a pure
status transition does not require a redundant approval.

## Team Composition
- **narrative-director** — Story arcs, character design, dialogue strategy, narrative vision
- **writer** — Dialogue writing, lore entries, item descriptions, in-game text
- **world-builder** — World rules, faction design, history, geography, environmental storytelling
- **art-director** — Character visual design, environmental visual storytelling, cutscene/cinematic tone
- **level-designer** — Level layouts that serve the narrative, pacing, environmental storytelling beats
- **localization-lead** — Localization readiness — flags non-localizable strings, cultural assumptions, and i18n gaps

## How to Delegate

Use the Codex subagent delegation to spawn each team member as a subagent:
- `subagent_type: narrative-director` — Story arcs, character design, narrative vision
- `subagent_type: writer` — Dialogue writing, lore entries, in-game text
- `subagent_type: world-builder` — World rules, faction design, history, geography
- `subagent_type: art-director` — Character visual profiles, environmental visual storytelling, cinematic tone
- `subagent_type: level-designer` — Level layouts that serve the narrative, pacing
- `subagent_type: localization-lead` — Localization readiness — flags non-localizable strings, cultural assumptions, and i18n gaps

Always provide full context in each agent's prompt (narrative brief, lore dependencies, character profiles). Launch independent agents in parallel where the pipeline allows it (e.g., Phase 2 agents can run simultaneously).

Before delegation, assign each writable file to exactly one subagent. Lore, voice-profile, and canon sources shared by multiple agents are read-only inputs; no two concurrently running agents may edit the same path.

## Pipeline

### Phase 1: Narrative Direction
Before delegation, parse the request into a content type, target entity, and the
existing authoritative narrative documents that may own it. Search the relevant
lore/character/dialogue locations and list candidate targets. If the request does
not resolve to exactly one target, present the candidates and wait for the user to
choose; do not start a writing agent while the destination is ambiguous.

Delegate to **narrative-director**:
- Define the narrative purpose of this content: what story beat does it serve?
- Identify characters involved, their motivations, and how this fits the overall arc
- Set the emotional tone and pacing targets
- Specify any lore dependencies or new lore this introduces
- Output: narrative brief with story requirements

After the brief is approved, resolve the concrete target paths for the brief, lore, dialogue, visual direction, and level integration. Present every existing or new file and its intended change as one changeset and obtain the single write approval before any subagent writes. Each path must have one owner. If later canon work requires an unlisted path, stop and revise this same changeset boundary before writing it.

### Phase 2: World Foundation and Drafting

Give the **world-builder**, **writer**, and **art-director** the same approved Phase 1 canon inputs and existing lore as read-only context. Independent work may start in parallel, but canon-dependent dialogue remains provisional until the world-builder completes the contradiction check:

- **world-builder**: Create or update lore entries for factions, locations, and history relevant to this content. Cross-reference against existing lore for contradictions and propose canon levels with their downstream impact. The narrative-director checks consistency and the user confirms the canon-level decision at the existing Phase 2 decision point; no agent may silently finalize it.
- **writer**: Draft character dialogue using voice profiles. Dialogue that depends on canon introduced or changed by the brief must be marked provisional. It may be finalized only after the world-builder's check has resolved that canon. Respect the project's dialogue-box and localization constraints; if they are absent, treat 120 characters only as a risk signal.
- **art-director**: Define character visual design direction for key characters appearing in this content (silhouette, visual archetype, distinguishing features). Specify environmental visual storytelling elements for each key space (prop composition, lighting notes, spatial arrangement). Define tone palette and cinematic direction for any cutscenes or scripted sequences.

If the world-builder reports a canon conflict, do not finalize writer output or enter Phase 3 until the conflict is resolved. Work that does not depend on the disputed fact may remain provisional in the partial report.

### Phase 3: Level Narrative Integration
Delegate to **level-designer**:
- Review the narrative brief and lore foundation
- Design environmental storytelling elements in the level
- Place narrative triggers, dialogue zones, and discovery points
- Ensure pacing serves both gameplay and story

### Phase 4: Review and Consistency
Delegate to **narrative-director**:
- Review all dialogue against character voice profiles
- Verify lore consistency across new and existing entries
- Confirm narrative pacing aligns with level design
- Check that all mysteries have documented "true answers"

### Phase 5: Polish (parallel)
Delegate read-only checks in parallel:
- **writer**: Inspect the reviewed candidate for dialogue-box constraints, string keys, and placeholder consistency; return findings without changing reviewed files.
- **localization-lead**: Inspect i18n compliance, hardcoded formatting, configured locale/layout constraints, and cultural assumptions; return findings without changing reviewed files.
- **world-builder**: Verify that user-confirmed canon levels and lore facts are reflected consistently; do not silently finalize or change canon.

Return each finding to the sole owner of the affected file. After any fix, send the corrected final candidate back through the existing Phase 4 narrative-director consistency review. COMPLETE is permitted only after that re-review passes. Nothing may change dialogue, lore, canon, or level integration after the final review.

## Error Recovery Protocol

If any spawned agent (through Codex subagent delegation) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** by asking the user directly with choices:
   - Skip only work that is advisory to the final narrative verdict and note the gap in the partial report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

A missing canon check, required voice profile, required localization check, or
other dependency of the final candidate cannot be skipped into COMPLETE. Stop
dependent phases and return BLOCKED/partial. Already-running agents may return
their results, but may not write a shared or unassigned path.

Common blockers:
- Input file missing (story not found, GDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `$architecture-decision` first
- Scope too large → split into two stories via `$create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess

## File Write Protocol

All file writes (narrative docs, dialogue files, lore entries) are delegated to
sub-agents spawned through Codex subagent delegation. After Phase 1 resolves the target paths, the orchestrator obtains one combined changeset approval before any write, and each sub-agent writes only its assigned, non-overlapping paths within that approved boundary without prompting again. This orchestrator does not write files directly.

## Output

A summary report covering: narrative brief status, lore entries created/updated, dialogue lines written, level narrative integration points, consistency review results, and any unresolved contradictions.

Verdict: **COMPLETE** — all required artifacts were delivered, the final candidate passed consistency review, and no unresolved canon, voice, localization, or prerequisite blocker remains.

If the pipeline stops because a dependency is unresolved (e.g., lore contradiction or missing prerequisite not resolved by the user):

Verdict: **BLOCKED** — [reason]

## Next Steps

- Run `$localize extract` to extract new strings for translation after dialogue is finalized.
- Run `$dev-story` to implement dialogue triggers and narrative events in-engine.
