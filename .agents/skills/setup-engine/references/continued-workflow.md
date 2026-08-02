# Setup Engine — Required workflow continuation

This file contains required phases of `$setup-engine`. Read it in full when the main `SKILL.md` reaches its Required continuation section, then execute the phases in order.

## 7. Maintain Engine Reference Docs

Use current official documentation for the confirmed engine/version. Update the
existing `docs/engine-reference/<engine>/VERSION.md` format with the version,
project pin/verification date, and official source links. Do not add LLM cutoff,
training-coverage, or model-risk fields and do not branch the file set on them.

Only update additional reference files when they already exist, the official
source supplies a relevant change, and the exact edit appeared in the preview.
If a file or required official source is missing, leave that file unchanged,
report partial coverage, and do not fabricate a `Last verified` date.

---

## 8. Update Root AGENTS.md Link

Keep root `AGENTS.md` in its existing Markdown-link form. Update the existing
Engine version reference link and Technology Stack fields for the confirmed
engine/version. Do not add an `@file` import.

---

## 9. Preserve Framework Agent Definitions

`setup`, `refresh`, and `upgrade` must not modify `.codex/agents` or copy project
version state into shared role definitions. Engine roles consume project-owned
`docs/technical-preferences.md` and the root version-reference link as read-only context.

---

## 10. Refresh Subcommand

If invoked as `$setup-engine refresh`:

1. Read the existing root AGENTS stack, project technical preferences, and
   `docs/engine-reference/<engine>/VERSION.md`.
2. Verify current releases, migration guides, and deprecations against official sources.
3. Build a candidate edit list only from existing files and source-backed changes.
4. Preview every exact file/section. Update only those existing previewed files.
5. Change `Last verified` only for a file whose relevant official source was
   successfully checked during this run.
6. If any expected file is missing or a source fails, report `PARTIAL` with the
   unchanged file/source; do not claim full refresh.

---

## 11. Upgrade Subcommand

### Step 1 — Read Current Version State

Read root `AGENTS.md`, `docs/technical-preferences.md`, and
`docs/engine-reference/<engine>/VERSION.md`. If old-version is omitted, use only
a mutually consistent current version; resolve conflicts before writes.

### Step 2 — Fetch Migration Guide

Use official engine sources to locate the migration guide and breaking changes
between versions. Extract renamed/removed APIs, changed defaults, and mandatory
migrations. If official verification fails, stop before proposing a version pin.

### Step 3 — Pre-Upgrade Audit

Scan project source for the exact deprecated/changed APIs from the official
guide and report file, API, and estimated effort. A text match is a candidate;
confirm the call-site before reporting it.

### Step 4 — Confirm Upgrade Scope

Ask whether the actual project/engine configuration has already been migrated
and verified on the new version. If not confirmed, end with the audit and do not
advance documentation pins.

### Step 5 — Update the Three Version Sources

After confirmation and one changeset authorization, update root AGENTS,
project `docs/technical-preferences.md`, and VERSION together. If one cannot be
safely updated from its baseline, write none. Preserve unrelated fields.

### Step 6 — Post-Upgrade Reminder

Report that project version documentation was updated, not that the engine
binary or source was migrated. List deprecated-API migration, refresh, and
architecture review as later commands only.

---

## 12. Output Summary

Report verified engine/version, official source, status of the three version
sources, actual-project confirmation, and unresolved Language/Rendering/Physics
fields. Any unresolved required field yields `INCOMPLETE`; otherwise report
`COMPLETE — project version documentation updated` without claiming binary work.

---

## Guardrails

- Verify every supplied/discovered version against current official documentation.
- Verify current licensing/platform assertions against official sources; if
  unavailable, say Unknown and do not repeat cached amounts or thresholds.
- Preview every existing file edit and never silently overwrite references.
- Never write project configuration/version state under `.codex/` and never
  modify `.codex/agents` in setup/refresh/upgrade.
- Show field-level old/new values before editing root AGENTS or technical preferences.
- Unknown/ambiguous sources block the affected write rather than a guessed value.
- Godot Language contains only the actual user-selected languages. GDExtension
  is additional only if the project already uses or explicitly selects it.

---

## Appendix A — Godot Language Configuration

### A1. AGENTS.md Technology Stack Templates

**GDScript:**
```markdown
- **Engine**: Godot [version]
- **Language**: GDScript
- **Build System**: Godot project export pipeline + Export Templates
- **Asset Pipeline**: Godot Import System + custom resource pipeline
```

**C#:**
```markdown
- **Engine**: Godot [version]
- **Language**: C# (.NET 8+, primary)
- **Build System**: .NET SDK + Godot project export pipeline + Export Templates
- **Asset Pipeline**: Godot Import System + custom resource pipeline
```

**Both — GDScript + C#:**
```markdown
- **Engine**: Godot [version]
- **Language**: GDScript (gameplay/UI scripting), C# (performance-critical systems)
- **Build System**: .NET SDK + Godot project export pipeline + Export Templates
- **Asset Pipeline**: Godot Import System + custom resource pipeline
```

SCons is the Godot engine source-build system and is not the normal project
export/build pipeline.

### A2. Naming Conventions

**GDScript:** PascalCase classes/scenes, snake_case variables/functions/signals/files, UPPER_SNAKE_CASE constants.

**C#:** PascalCase classes/members/scenes/files, `_camelCase` private fields,
PascalCase signal delegates with `EventHandler`, PascalCase constants.

**Both:** apply conventions per file language and ask when a new system's language is undecided.

### A3. Engine Specialists Routing

**GDScript:** primary `godot-specialist`; `.gd` →
`godot-gdscript-specialist`; `.gdshader`/VisualShader →
`godot-shader-specialist`; UI/scenes → `godot-specialist`.

**C#:** primary `godot-specialist`; `.cs`/`.csproj`/NuGet →
`godot-csharp-specialist`; shaders → `godot-shader-specialist`; UI/scenes →
`godot-specialist`.

**Both:** route `.gd` and `.cs` to their language specialists and cross-language
boundary decisions to `godot-specialist`.

Only when native extensions are actually present, add `.gdextension`/native C++
routing to `godot-gdextension-specialist`; do not add C++ to Language merely
because the specialist exists.
