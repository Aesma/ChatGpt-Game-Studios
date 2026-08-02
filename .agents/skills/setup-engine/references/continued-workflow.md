# Setup Engine — Required workflow continuation

This file contains required phases of `$setup-engine`. Read it in full when the main `SKILL.md` reaches its Required continuation section, then execute the phases in order.

## 7. Maintain Engine Reference Docs

Use current official documentation for the confirmed engine/version. Update the
existing `docs/engine-reference/<engine>/VERSION.md` format with the version,
project pin/verification date, and official source links. Do not add LLM cutoff,
training-coverage, or model-risk fields and do not branch the file set on them.

Only update additional reference files when they already exist and the official
source supplies a relevant change. Preview every changed existing file; do not
create an expanded reference tree merely because a version is newer.

---

## 8. Update Root AGENTS.md Link

Keep root `AGENTS.md` in its existing Markdown-link form. Update the existing
`Engine version reference` link and Technology Stack fields for the confirmed
engine/version. Do not add an `@file` import because Codex does not expand it.

---

## 9. Preserve Framework Agent Definitions

`setup`, `refresh`, and `upgrade` must not modify `.codex/agents` or copy project
version state into shared role definitions. Engine roles consume the project
technical preferences and root version-reference link as read-only context.

---
## 10. Refresh Subcommand

If invoked as `$setup-engine refresh`:

1. Read the existing `docs/engine-reference/<engine>/VERSION.md` to get
   the current engine and version
2. Use web search to check for:
   - New engine releases since last verification
   - Updated migration guides
   - Newly deprecated APIs
3. Update all reference docs with new findings
4. Update "Last verified" dates on all modified files
5. Report what changed

---

## 11. Upgrade Subcommand

If invoked as `$setup-engine upgrade [old-version] [new-version]`:

### Step 1 — Read Current Version State

Read root `AGENTS.md`, `docs/technical-preferences.md`, and
`docs/engine-reference/<engine>/VERSION.md` to confirm the current engine/version
state and any migration note URLs already recorded. If `old-version` was not
provided, use the mutually consistent current version; conflicts must be resolved
before any write.

### Step 2 — Fetch Migration Guide

Use web search and open the relevant web page to locate the official migration guide between
`old-version` and `new-version`:

- Search: `"[engine] [old-version] to [new-version] migration guide"`
- Search: `"[engine] [new-version] breaking changes changelog"`
- Fetch the migration guide URL from VERSION.md if one is already recorded,
  or use the URL found via search.

Extract: renamed APIs, removed APIs, changed defaults, behavior changes, and
any "must migrate" items.

### Step 3 — Pre-Upgrade Audit

Scan `src/` for code that uses APIs known to be deprecated or changed in the
target version:

- Search to search for deprecated API names extracted from the migration
  guide (e.g., old function names, removed node types, changed property names)
- List each file that matches, with the specific API reference found

Present the audit results as a table:

```
Pre-Upgrade Audit: [engine] [old-version] → [new-version]
==========================================================

Files requiring changes:
  File                              | Deprecated API Found       | Effort
  --------------------------------- | -------------------------- | ------
  src/gameplay/player_movement.gd   | old_api_name               | Low
  src/ui/hud.gd                     | removed_node_type          | Medium

Breaking changes to watch for:
  - [change description from migration guide]
  - [change description from migration guide]

Recommended migration order (dependency-sorted):
  1. [system/layer with fewest dependencies first]
  2. [next system]
  ...
```
If no deprecated APIs are found in `src/`, report: "No deprecated API usage
found in src/ — upgrade may be low-risk."

### Step 4 — Confirm Upgrade Scope

Ask the user whether the upgrade should be included in the proposed changeset:

> "Pre-upgrade audit complete. Found [N] files using deprecated APIs.
> Has the actual project/engine configuration already been migrated to and
> verified on [new-version]?"

If the user cannot confirm the actual project version, end with the pre-upgrade
audit and do not advance any documentation pin. If confirmed, present one
field-level changeset that updates root `AGENTS.md`,
`docs/technical-preferences.md`, and
`docs/engine-reference/<engine>/VERSION.md` together. If any target cannot be
safely updated from its previewed baseline, write none and report incomplete.

### Step 5 — Update the Three Version Sources

Once the complete changeset is authorized and the actual project version is
confirmed, update all three existing sources to the same engine/version:

1. root `AGENTS.md` Technology Stack and existing version-reference Markdown link;
2. `docs/technical-preferences.md` Engine & Language fields while preserving
   unrelated project choices;
3. `docs/engine-reference/<engine>/VERSION.md` version, pin/verification date,
   official migration URL, and project-specific migration notes.

Do not write LLM cutoff/risk fields. If existing `breaking-changes.md` or
`deprecated-apis.md` files are also previewed, update only relevant sections.
### Step 6 — Post-Upgrade Reminder

After updating VERSION.md, output:

```
Project version documentation updated consistently: [engine] [old-version] → [new-version]

Next steps:
1. Migrate deprecated API usages in the [N] files listed above
2. Run $setup-engine refresh after upgrading the actual engine binary to
   verify no new deprecations were missed
3. Run $architecture-review — the engine upgrade may invalidate ADRs that
   reference specific APIs or engine capabilities
4. If any ADRs are invalidated, run $propagate-design-change to update
   downstream stories
```

---

## 12. Output Summary

Report whether this run produced a verified setup, a documentation-only update,
or a pre-upgrade audit. Never imply that an engine binary/source migration
occurred from documentation edits alone.

```
Engine documentation result
===========================
Engine/version:  [name] [version]
Official source: [URL]
AGENTS.md:        [updated/unchanged]
Tech Prefs:      [updated/unchanged; unresolved fields listed]
Version ref:     [updated/unchanged]
Actual project:  [user-confirmed / not confirmed]
```

If Rendering, Physics, Language, or the actual project version remains
unconfirmed, report **INCOMPLETE** with those fields. Otherwise report
**COMPLETE — project version documentation updated**; do not claim a binary
migration.

---
## Guardrails

- NEVER guess an engine version — verify it against current official engine documentation and obtain user confirmation
- NEVER overwrite existing reference docs silently — preview whether each file is appended, updated, or replaced
- If reference docs already exist for a different engine, surface the replacement in the complete changeset preview
- Always show field-level old/new values before editing AGENTS.md or technical preferences
- NEVER write project configuration or version state under `.codex/`, and never modify `.codex/agents` from setup/refresh/upgrade
- If web search returns ambiguous results, show the user and let them decide
- When the user chose **GDScript**: copy the GDScript AGENTS.md template from Appendix A1 exactly. NEVER add "C++ via GDExtension" to the Language field. GDScript projects may use GDExtension, but it is not a primary project language. The `godot-gdextension-specialist` in the routing table is available for when native extensions are needed — it does not make C++ a project language.

---

## Appendix A — Godot Language Configuration

All Godot-specific variants for language-dependent configuration. Referenced from Sections 4 and 5 — only relevant when Godot is the chosen engine. Use the subsection matching the language chosen in Section 4.

---

### A1. AGENTS.md Technology Stack Templates

**GDScript:**
```markdown
- **Engine**: Godot [version]
- **Language**: GDScript
- **Build System**: SCons (engine), Godot Export Templates
- **Asset Pipeline**: Godot Import System + custom resource pipeline
```

> **Guardrail**: When using this GDScript template, write the Language field as exactly "`GDScript`" — no additions. Do NOT append "C++ via GDExtension" or any other language. The C# template below includes GDExtension because C# projects commonly wrap native code; GDScript projects do not.

**C#:**
```markdown
- **Engine**: Godot [version]
- **Language**: C# (.NET 8+, primary), C++ via GDExtension (native plugins only)
- **Build System**: .NET SDK + Godot Export Templates
- **Asset Pipeline**: Godot Import System + custom resource pipeline
```

**Both — GDScript + C#:**
```markdown
- **Engine**: Godot [version]
- **Language**: GDScript (gameplay/UI scripting), C# (performance-critical systems), C++ via GDExtension (native only)
- **Build System**: .NET SDK + Godot Export Templates
- **Asset Pipeline**: Godot Import System + custom resource pipeline
```

---

### A2. Naming Conventions

**GDScript:**
- Classes: PascalCase (e.g., `PlayerController`)
- Variables/functions: snake_case (e.g., `move_speed`)
- Signals: snake_case past tense (e.g., `health_changed`)
- Files: snake_case matching class (e.g., `player_controller.gd`)
- Scenes: PascalCase matching root node (e.g., `PlayerController.tscn`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_HEALTH`)

**C#:**
- Classes: PascalCase (`PlayerController`) — must also be `partial`
- Public properties/fields: PascalCase (`MoveSpeed`, `JumpVelocity`)
- Private fields: `_camelCase` (`_currentHealth`, `_isGrounded`)
- Methods: PascalCase (`TakeDamage()`, `GetCurrentHealth()`)
- Signal delegates: PascalCase + `EventHandler` suffix (`HealthChangedEventHandler`)
- Files: PascalCase matching class (`PlayerController.cs`)
- Scenes: PascalCase matching root node (`PlayerController.tscn`)
- Constants: PascalCase (`MaxHealth`, `DefaultMoveSpeed`)

**Both — GDScript + C#:**
Use GDScript conventions for `.gd` files and C# conventions for `.cs` files. Mixed-language files do not exist — the boundary is per-file. When in doubt about which language a new system should use, ask the user and record the decision in `technical-preferences.md`.

---

### A3. Engine Specialists Routing

**GDScript:**
```markdown
## Engine Specialists
- **Primary**: godot-specialist
- **Language/Code Specialist**: godot-gdscript-specialist (all .gd files)
- **Shader Specialist**: godot-shader-specialist (.gdshader files, VisualShader resources)
- **UI Specialist**: godot-specialist (no dedicated UI specialist — primary covers all UI)
- **Additional Specialists**: godot-gdextension-specialist (GDExtension / native C++ bindings only)
- **Routing Notes**: Invoke primary for architecture decisions, ADR validation, and cross-cutting code review. Invoke GDScript specialist for code quality, signal architecture, static typing enforcement, and GDScript idioms. Invoke shader specialist for material design and shader code. Invoke GDExtension specialist only when native extensions are involved.

### File Extension Routing

| File Extension / Type | Specialist to Spawn |
|-----------------------|---------------------|
| Game code (.gd files) | godot-gdscript-specialist |
| Shader / material files (.gdshader, VisualShader) | godot-shader-specialist |
| UI / screen files (Control nodes, CanvasLayer) | godot-specialist |
| Scene / prefab / level files (.tscn, .tres) | godot-specialist |
| Native extension / plugin files (.gdextension, C++) | godot-gdextension-specialist |
| General architecture review | godot-specialist |
```

**C#:**
```markdown
## Engine Specialists
- **Primary**: godot-specialist
- **Language/Code Specialist**: godot-csharp-specialist (all .cs files)
- **Shader Specialist**: godot-shader-specialist (.gdshader files, VisualShader resources)
- **UI Specialist**: godot-specialist (no dedicated UI specialist — primary covers all UI)
- **Additional Specialists**: godot-gdextension-specialist (GDExtension / native C++ bindings only)
- **Routing Notes**: Invoke primary for architecture decisions, ADR validation, and cross-cutting code review. Invoke C# specialist for code quality, [Signal] delegate patterns, [Export] attributes, .csproj management, and C#-specific Godot idioms. Invoke shader specialist for material design and shader code. Invoke GDExtension specialist only when native C++ plugins are involved.

### File Extension Routing

| File Extension / Type | Specialist to Spawn |
|-----------------------|---------------------|
| Game code (.cs files) | godot-csharp-specialist |
| Shader / material files (.gdshader, VisualShader) | godot-shader-specialist |
| UI / screen files (Control nodes, CanvasLayer) | godot-specialist |
| Scene / prefab / level files (.tscn, .tres) | godot-specialist |
| Project config (.csproj, NuGet) | godot-csharp-specialist |
| Native extension / plugin files (.gdextension, C++) | godot-gdextension-specialist |
| General architecture review | godot-specialist |
```

**Both — GDScript + C#:**
```markdown
## Engine Specialists
- **Primary**: godot-specialist
- **GDScript Specialist**: godot-gdscript-specialist (.gd files — gameplay/UI scripts)
- **C# Specialist**: godot-csharp-specialist (.cs files — performance-critical systems)
- **Shader Specialist**: godot-shader-specialist (.gdshader files, VisualShader resources)
- **UI Specialist**: godot-specialist (no dedicated UI specialist — primary covers all UI)
- **Additional Specialists**: godot-gdextension-specialist (GDExtension / native C++ bindings only)
- **Routing Notes**: Invoke primary for cross-language architecture decisions and which systems belong in which language. Invoke GDScript specialist for .gd files. Invoke C# specialist for .cs files and .csproj management. Prefer signals over direct cross-language method calls at the boundary.

### File Extension Routing

| File Extension / Type | Specialist to Spawn |
|-----------------------|---------------------|
| Game code (.gd files) | godot-gdscript-specialist |
| Game code (.cs files) | godot-csharp-specialist |
| Cross-language boundary decisions | godot-specialist |
| Shader / material files (.gdshader, VisualShader) | godot-shader-specialist |
| UI / screen files (Control nodes, CanvasLayer) | godot-specialist |
| Scene / prefab / level files (.tscn, .tres) | godot-specialist |
| Project config (.csproj, NuGet) | godot-csharp-specialist |
| Native extension / plugin files (.gdextension, C++) | godot-gdextension-specialist |
| General architecture review | godot-specialist |
```
