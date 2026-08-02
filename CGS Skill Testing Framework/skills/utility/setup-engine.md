# Skill Test Spec: $setup-engine

## Skill Summary

`$setup-engine` configures the project's engine, language, rendering backend,
physics engine, specialist agent assignments, and naming conventions by
populating `technical-preferences.md`. It accepts an optional engine argument
(e.g., `$setup-engine godot`) to skip the engine-selection step. For each
section of `technical-preferences.md`, the skill presents a draft and asks
"May I apply the proposed changeset?" before updating.

The skill also populates the specialist routing table (file extension → agent
mappings) based on the chosen engine. It has no director gates — configuration
is a technical utility task. The verdict is always COMPLETE when the file is
fully written.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keyword: COMPLETE
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
7. File is written after approval; verdict is COMPLETE

**Assertions:**
- [ ] Engine field is set to Godot 4 (not a placeholder)
- [ ] Language field is set to GDScript
- [ ] Naming conventions are GDScript-appropriate (snake_case)
- [ ] Routing table includes `.gd`, `.gdshader`, and `.tscn` entries
- [ ] Specialists are assigned (not placeholders)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts

**Assertions:**
- [ ] Engine field is set to Unity (not Godot or Unreal)
- [ ] Language field is set to C#
- [ ] Naming conventions reflect C# conventions
- [ ] Routing table includes `.cs` and `.unity` entries
- [ ] Verdict is COMPLETE

---

### Case 3: Unreal + Blueprint — Unreal-specific configuration

**Fixture:**
- `technical-preferences.md` contains only placeholders
- Engine argument provided: `unreal`

**Input:** `$setup-engine unreal`

**Expected behavior:**
1. Skill sets engine to Unreal Engine 5, primary language to Blueprint (Visual Scripting)
2. Specialist assignments reference unreal-specialist, blueprint-specialist
3. Routing table: `.uasset` → blueprint-specialist or unreal-specialist,
   `.umap` → unreal-specialist
4. Performance budgets are pre-set with Unreal defaults (e.g., higher draw call budget)
5. Skill asks "May I apply the proposed changeset?" and writes on approval

**Assertions:**
- [ ] Skill does NOT overwrite all fields when only a section update was requested
- [ ] User is offered section-specific reconfiguration
- [ ] Only the selected section is modified in the written file
- [ ] Verdict is COMPLETE

---

### Case 5: Director Gate Check — No gate; setup-engine is a utility skill

**Fixture:**
- Fresh project with no engine configured

**Input:** `$setup-engine godot`

**Expected behavior:**
1. Skill completes full engine configuration
2. No director agents are spawned at any point
3. No gate IDs appear in output

**Assertions:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Verdict is COMPLETE without any gate check

---

## Protocol Compliance

- [ ] Presents draft configuration before asking to write
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Respects engine argument when provided (skips selection step)
- [ ] Detects existing config and offers partial reconfigure
- [ ] Routing table is populated for all key file types for the chosen engine
- [ ] Verdict is COMPLETE after file is written

---

## Coverage Notes

- Godot 4 + C# (instead of GDScript) follows the same flow as Case 1 with
  different naming conventions and the godot-csharp-specialist assignment.
  This variant is not separately tested.
- The engine-version-specific guidance (e.g., Godot 4.6 knowledge gap warning
  from VERSION.md) is surfaced by the skill but not assertion-tested here.
- Performance budget defaults per engine are noted as engine-specific but
  exact default values are not assertion-tested.

## P0 Contract Coverage

- [ ] A provided or discovered engine version is verified against current
  official engine documentation; no LLM cutoff/training-risk field or branch remains.
- [ ] Root AGENTS keeps its existing Markdown version-reference link and never
  receives an `@file` import; setup/refresh/upgrade do not modify `.codex/agents`.
- [ ] Project state is written to `docs/technical-preferences.md`; the `.codex`
  technical-preferences file is read-only template input. Rendering and Physics
  must be confirmed or remain explicit placeholders with an incomplete result.
- [ ] Existing configuration is shown field-by-field and only selected fields
  change; unselected project choices are preserved.
- [ ] Upgrade changes the version pin only after the actual project version is
  confirmed, then updates AGENTS, project technical preferences, and VERSION
  together or writes none. Documentation edits never claim a binary migration.
