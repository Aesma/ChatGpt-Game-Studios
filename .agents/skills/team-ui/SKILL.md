---
name: team-ui
description: "Orchestrate the UI team through the full UX pipeline: from UX spec authoring through visual design, implementation, review, and polish. Integrates with $ux-design, $ux-review, and studio UX templates."
---

## Invocation and execution

Invoke this workflow as `$team-ui`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[UI feature description]`. Reject unknown flags or extra control arguments before project reads.

If no UI feature description is provided, output usage with an example and exit
without reading project files, spawning agents, or writing.

When this skill is invoked, orchestrate the UI team through a structured pipeline.

**Decision Points:** At each phase transition, ask the user directly to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase.

## Team Composition
- **ux-designer** — User flows, wireframes, accessibility, input handling
- **ui-programmer** — UI framework, screens, structured prompts, data binding, implementation
- **art-director** — Visual style, layout polish, consistency with art bible
- **engine UI specialist** — Validates UI implementation patterns against engine-specific best practices (read from `docs/technical-preferences.md` Engine Specialists → UI Specialist)
- **accessibility-specialist** — Audits accessibility compliance at Phase 4

**Templates used by this pipeline:**
- `.codex/docs/templates/ux-spec.md` — Standard screen/flow UX specification
- `.codex/docs/templates/hud-design.md` — HUD-specific UX specification
- `.codex/docs/templates/interaction-pattern-library.md` — Reusable interaction patterns
- `.codex/docs/templates/accessibility-requirements.md` — Template whose committed instance supplies the accessibility tier

## How to Delegate

Use the Codex subagent delegation to spawn each team member as a subagent:
- `subagent_type: ux-designer` — User flows, wireframes, accessibility, input handling
- `subagent_type: ui-programmer` — UI framework, screens, structured prompts, data binding
- `subagent_type: art-director` — Visual style, layout polish, art bible consistency
- `subagent_type: [UI engine specialist]` — Engine-specific UI pattern validation (e.g., unity-ui-specialist, ue-umg-specialist, godot-specialist)
- `subagent_type: accessibility-specialist` — Accessibility compliance audit

Always provide full context in each agent's prompt (feature requirements, existing UI patterns, platform targets). Launch independent agents in parallel where the pipeline allows it (e.g., Phase 4 review agents can run simultaneously).

## Pipeline

### Phase 1a: Context Gathering

Before designing anything, read and synthesize:
- `design/gdd/game-concept.md` — platform targets and intended audience
- `design/player-journey.md` — player's state and context when they reach this screen
- All GDD UI Requirements sections relevant to this feature
- `design/ux/interaction-patterns.md` — existing patterns to reuse (not reinvent)
- `design/accessibility-requirements.md` — committed accessibility tier: Basic, Standard, Comprehensive, or Exemplary

**If `design/ux/interaction-patterns.md` does not exist**, surface the gap immediately:
> "interaction-patterns.md does not exist — no existing patterns to reuse."

Then keep the bootstrap inside Phase 1 authoring: present meaningful behavior options for every pattern the current spec requires, record the user's design decision, and use the existing `$ux-design patterns` pattern-library writer as the only writer for `design/ux/interaction-patterns.md`. The approved pattern entry must be persisted before the current spec cites it and before the first `$ux-review`.

Do NOT invent patterns or defer authority until implementation. If the pattern decision is not approved, the library path was not included in the authorized changeset, or persistence fails, produce a BLOCKED/partial UX spec and do not enter Phase 1c, 2, or 3.

Summarize the context in a brief for the ux-designer: what the player is doing, what they need, what constraints apply, and which existing patterns are relevant.

### Phase 1b: UX Spec Authoring

Choose one authoring route before work starts: use `$ux-design [feature name]`, or use ux-designer only when that entry is unavailable, with the same template and path contract. Do not switch routes mid-run.

If designing the HUD, use `.codex/docs/templates/hud-design.md`; otherwise use
`.codex/docs/templates/ux-spec.md`. The fallback ux-designer must read and preserve
the complete same template and output-path contract.

> **Notes on special cases:**
> - For HUD design specifically, invoke `$ux-design` with `argument: hud` (e.g., `$ux-design hud`).
> - For the interaction pattern library, run `$ux-design patterns` once at project start and update it whenever new patterns are introduced during later phases.

Output: `design/ux/[feature-name].md` with all required spec sections filled.

Before the first write, resolve and preview one changeset containing the concrete UX spec, visual spec, implementation targets, session-state target, and `design/ux/interaction-patterns.md` whenever the current spec is known to require a new or revised pattern. Assign the pattern library to its single writer and each other path to one owner. Nested authoring inherits this boundary and does not request another authorization; newly discovered paths use the existing material-scope-expansion rule.

### Phase 1c: UX Review

After the spec is complete, invoke `$ux-review design/ux/[feature-name].md`.

**Gate**: Do not proceed to Phase 2 until the verdict is APPROVED. If the verdict is NEEDS REVISION or MAJOR, the ux-designer must address the flagged issues and re-run the existing Phase 1c review. The user may stop this workflow and make a separate product decision, but this workflow never relabels that verdict as implementation-ready.

### Phase 2: Visual Design

Delegate to **art-director**:
- Review the full UX spec (flows, wireframes, interaction patterns, accessibility notes) — not just the wireframe images
- Apply visual treatment from the art bible: colors, typography, spacing, animation style
- Check that visual design preserves accessibility compliance: verify color contrast ratios, and confirm color is never the only indicator of state (shape, text, or icon must reinforce it)
- Specify all asset requirements needed from the art pipeline: icons at specified sizes, background textures, fonts, decorative elements — with precise dimensions and format requirements
- Ensure consistency with existing implemented UI screens
- Output: visual design spec with style notes and asset manifest

### Phase 3: Implementation

Before implementation begins, spawn the **engine UI specialist** (from `docs/technical-preferences.md` Engine Specialists → UI Specialist) to review the UX spec and visual design spec for engine-specific implementation guidance:
- Which engine UI framework should be used for this screen? (e.g., UI Toolkit vs UGUI in Unity, Control nodes vs CanvasLayer in Godot, UMG vs CommonUI in Unreal)
- Any engine-specific gotchas for the proposed layout or interaction patterns?
- Recommended structured prompt/node structure for the engine?
- Output: engine UI implementation notes to hand off to ui-programmer before they begin

If no engine is configured, Phase 1 design artifacts may be completed, but stop BLOCKED before Phase 3. Do not ask ui-programmer to guess an engine framework and do not spawn multiple engine specialists.

Delegate to **ui-programmer**:
- Implement the UI following the UX spec and visual design spec
- **Use patterns from `design/ux/interaction-patterns.md`** — do not reinvent patterns that are already specified. If a pattern almost fits but needs modification, note the deviation and flag it for ux-designer review.
- **UI NEVER owns or modifies game state** — display only; emit events for all player actions
- All text through the localization system — no hardcoded player-facing strings
- Support exactly the target inputs configured in `.codex/docs/technical-preferences.md`; do not infer keyboard/gamepad from platform. If target inputs are unconfigured, stop BLOCKED before implementation.
- Implement accessibility features per the committed tier in `design/accessibility-requirements.md`
- Wire up data binding to game state
- Do not create an authoritative pattern during implementation. A newly discovered pattern requirement returns to Phase 1's user decision, single pattern-library writer, authorized edit, and review before implementation resumes.
- Output: implemented UI feature

### Phase 4: Review (parallel)

Delegate in parallel:
- **ux-designer**: Verify implementation matches wireframes and interaction spec. Test keyboard-only and gamepad-only navigation. Check accessibility features function correctly.
- **art-director**: Verify visual consistency with art bible. Check at minimum and maximum supported resolutions.
- **accessibility-specialist**: Verify compliance against the committed accessibility tier documented in `design/accessibility-requirements.md`. Flag any violations as blockers.

All three review streams must report before proceeding to Phase 5.

### Phase 5: Polish

- Assign every finding to the existing owner of the affected file and address all review feedback without concurrent edits to one path
- Verify animations are skippable and respect the player's motion reduction preferences
- Confirm UI sounds trigger through the audio event system (no direct audio calls)
- Test at all supported resolutions and aspect ratios
- **Verify `design/ux/interaction-patterns.md` is up to date** — if any new patterns were introduced during this feature's implementation, confirm they have been added to the library
- **For HUD mode only**, confirm all HUD elements respect the visual budget defined in `design/ux/hud.md` (element count, screen region allocations, maximum opacity values). Screen/flow modes use their own approved spec constraints and do not require `hud.md`.

After each fix, return the affected file to the same Phase 4 reviewer that raised the finding for a targeted re-check. COMPLETE requires all blockers to be closed, all three required reviewers to have confirmed their findings, and no change to reviewed content after the last re-check.

## Quick Reference — When to Use Which Skill

- `$ux-design` — Author a new UX spec for a screen, flow, or HUD from scratch
- `$ux-review` — Validate a completed UX spec before implementation
- `$team-ui [feature]` — Full pipeline from concept through polish (calls `$ux-design` and `$ux-review` internally)
- `$quick-design` — Small UI changes that don't need a full new UX spec

## Error Recovery Protocol

If any spawned agent (through Codex subagent delegation) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** by asking the user directly with choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Common blockers:
- Input file missing (story not found, GDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `$architecture-decision` first
- Scope too large → split into two stories via `$create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess

## File Write Protocol

All file writes (UX specs, interaction pattern library updates, implementation files) are
delegated to sub-agents and sub-skills (`$ux-design`, `ui-programmer`). Each enforces the
single Phase 1 changeset boundary and does not re-prompt. Each target has one writer. This orchestrator does not write files directly.

## Output

A summary report covering: UX spec status, UX review verdict, visual design status, implementation status, accessibility compliance, input method support, interaction pattern library update status, and any outstanding issues.

Verdict: **COMPLETE** — UI feature delivered through full pipeline (UX spec → visual → implementation → review → polish).
Verdict: **BLOCKED** — pipeline halted; surface the blocker and its phase before stopping.

## Next Steps

- Run `$ux-review` on the final spec if not yet approved.
- Run `$code-review` on the UI implementation before closing stories.
- Run `$team-polish` if visual or audio polish pass is needed.
