---
name: setup-engine
description: "Configure or refresh the project engine documentation from verified official version sources while preserving existing project choices."
---

## Invocation and execution

Invoke this workflow as `$setup-engine`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[engine] | [engine version] | refresh | upgrade [old-version] [new-version] | no args for guided selection`. Treat bracketed values as optional unless the workflow says otherwise.


When this skill is invoked:

## 1. Parse Arguments

Five modes:

- **Full spec**: `$setup-engine godot 4.6`
- **Engine only**: `$setup-engine unity`
- **No args**: `$setup-engine`
- **Refresh**: `$setup-engine refresh`
- **Upgrade**: `$setup-engine upgrade [old-version] [new-version]`

Accept only `godot`, `unity`, or `unreal` as engine identifiers and only one of
the five shapes above. Reject unknown engines, subcommands, missing upgrade
versions, extra positional arguments, and ambiguous version forms with usage;
do not reinterpret them.

Before any mode proposes edits, read root `AGENTS.md`, the project-owned
`docs/technical-preferences.md` (or the read-only
`.codex/docs/technical-preferences.md` template when the project file is absent),
and `docs/engine-reference/<engine>/VERSION.md`. Show field-level old/new values
and preserve every field outside the user's selected setup/reconfigure scope.
If sources conflict, surface the conflict before drafting.

---

## 2. Guided Mode (No Arguments)

### Check for existing game concept

Read `design/gdd/game-concept.md` when it exists and extract genre, scope,
platforms, art style, team size, and any engine recommendation. If absent, tell
the user they may describe the game here or invoke `$brainstorm` separately.

### Collect decision inputs

Ask prior engine experience first, then always verify that preference against
target platform and project constraints. Experience is an important factor, not
a reason to skip the matrix or ignore a hard platform requirement.

Collect:

1. target platforms;
2. 2D/3D requirements and visual goals;
3. primary input;
4. team size/experience;
5. language preference;
6. licensing/budget constraints;
7. concept-specific requirements such as open-world streaming, mobile/web,
   multiplayer, adaptive audio, or console certification.

### Verify current engine facts before recommendation

For each engine being compared, use current official engine, licensing, and
platform-support documentation. Cite the official source and verification date.
Do not repeat hardcoded revenue/install/royalty thresholds, license prices,
console/web/mobile support claims, or absolute suitability conclusions from this
file. When a current official fact cannot be verified, label it `Unknown` and
exclude it from a deterministic recommendation.

Stable qualitative considerations may include editor/workflow complexity,
language ecosystem, the project's desired fidelity, and the user's experience,
but distinguish them from verified current license/platform facts.

### Produce a recommendation

1. Show a comparison table using the user's actual factors.
2. Give one primary recommendation and one alternative with trade-offs.
3. Identify any verified platform/license constraint and source.
4. Explain that engine migration can be costly and requires separate evaluation.
5. Ask the user to choose or explore concept-specific concerns.

The user always makes the engine decision.

---

## 3. Look Up Current Version

For both a user-provided version and a version discovered by search, verify the
exact release against current official engine version/release documentation,
show the source, and ask the user to confirm. If verification is unavailable or
ambiguous, do not write the version.

---

## 4. Update AGENTS.md Technology Stack

### Language Selection

For Godot, ask for GDScript, C#, or both and apply the matching Appendix A
variant.

For Unreal, ask the user to choose one of:

- C++ primary;
- Blueprint primary;
- hybrid C++ + Blueprint, including which layer owns gameplay logic.

Record only the selected language arrangement. Do not force C++ primary.

Unity uses C# unless the existing project records a different supported setup.

Read `AGENTS.md` and show field-level old/new Technology Stack values. For an
existing configuration, change only the user-selected fields. Add the file to
the complete preview but do not edit until the full changeset is authorized.

Use engine-appropriate values:

**Unity:**
```markdown
- **Engine**: Unity [version]
- **Language**: C#
- **Build System**: [existing Unity project build pipeline]
- **Asset Pipeline**: Unity Asset Import Pipeline + Addressables
```

**Unreal:**
```markdown
- **Engine**: Unreal Engine [version]
- **Language**: [C++ | Blueprint | C++ and Blueprint — user-selected ownership]
- **Build System**: Unreal Build Tool (UBT)
- **Asset Pipeline**: Unreal Content Pipeline
```

For Godot, use Appendix A1.

---

## 5. Populate Technical Preferences

Create or update project-owned `docs/technical-preferences.md`. If absent, read
`.codex/docs/technical-preferences.md` only as an initial template. Never write
project state under `.codex/`. Preserve unselected existing fields.

### Engine & Language

Fill the confirmed engine/version and the exact user-selected language. Native
GDExtension/C++ is additional only when existing project files or an explicit
user choice show it is in use; never append it automatically to Godot C# or
mixed-language projects.

### Rendering and Physics

Present current engine-supported defaults as candidates and ask the user to
confirm. Undecided fields retain explicit placeholders and make the result incomplete.

### Naming Conventions

Apply the selected engine/language conventions. Godot variants are in Appendix A.
Unity C# uses PascalCase types/members and `_camelCase` private fields. Unreal
uses its existing prefix conventions and `b` booleans.

### Input & Platform

Populate only from confirmed user/concept choices. Present derived support
levels for confirmation rather than treating a generic mapping as platform fact.

### Remaining Sections

- Ask whether performance budgets should be configured or remain placeholders.
- Preserve the existing configured testing framework. For Godot, the existing
  coding/CI standard is GdUnit4; do not suggest GUT by default. A framework
  change is a user decision shown in the changeset.
- Leave Forbidden Patterns and Allowed Libraries unchanged unless the user is
  actively making that decision. Never add speculative dependencies.

### Engine Specialists Routing

Populate the existing routing section for the selected engine and language.
For Unreal UI, route `.uasset` UMG Widget Blueprint assets in UI/Widget paths to
`ue-umg-specialist`; `.umg` is not a standalone file extension. Route Blueprint
class assets by asset/path context, not extension alone.

For Godot, use Appendix A3. A GDExtension specialist may be listed as applicable
only when the project actually uses native extensions; its availability does
not add C++ to the Language field.

Present the complete preferences draft and add only that project file to the
authorized changeset. Do not write `.codex`.

---

## 6. Verify Version Documentation

Use current official engine documentation for the user-confirmed version.
Record the official source and verification date in the existing VERSION
document format. Do not infer risk from an LLM training cutoff and do not write
model-knowledge fields into project documentation.

---

## Required continuation

Before continuing, read [references/continued-workflow.md](references/continued-workflow.md) in full. It contains the remaining required phases, output formats, recovery rules, and handoff instructions; execute them in order.
