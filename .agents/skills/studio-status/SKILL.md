---
name: studio-status
description: "Report the current game-production stage and active Epic, Feature, and Task breadcrumb from project artifacts. Use when the user asks for studio status, production phase, current focus, or recovery context."
---

# Studio Status

## Invocation and execution

Invoke this read-only workflow as `$studio-status`.

Do not install or emulate a terminal status line. Do not create or modify files.

## Resolve the project root

Use the current workspace root. Normalize path separators only for display. Treat missing optional files and directories as absent evidence, not errors.

## Determine the stage

1. If `production/stage.txt` exists and its first line is non-empty, use that value exactly.
2. Otherwise inspect the following evidence:
   - `design/gdd/game-concept.md`
   - `design/gdd/systems-index.md`
   - `.codex/docs/technical-preferences.md`
   - `docs/architecture/adr-*.md`
   - source files under `src/` with extensions `.gd`, `.cs`, `.cpp`, `.h`, `.py`, `.rs`, `.lua`, `.tscn`, or `.tres`
3. For technical preferences, consider the engine configured only when the first `**Engine**:` or `- **Engine**:` entry exists and does not contain `TO BE CONFIGURED`.
4. Infer the most advanced supported stage in this order:
   - At least 10 recognized source files: `Production`
   - At least one ADR: `Pre-Production`
   - Engine configured: `Technical Setup`
   - Systems index present: `Systems Design`
   - Game concept present: `Concept`
   - No evidence: `Concept`

Only an explicit `production/stage.txt` may select later stages such as `Polish` or `Release`.

## Build the active breadcrumb

For `Production`, `Polish`, or `Release`, inspect `production/session-state/active.md` when it exists.

1. Read only the block between `<!-- STATUS -->` and `<!-- /STATUS -->`.
2. Extract optional `Epic:`, `Feature:`, and `Task:` values.
3. Join non-empty values in that order with ` > `.
4. If the block or all values are absent, report that no active focus is recorded.

For earlier stages, omit the breadcrumb unless the user explicitly asks to see the stored session focus.

## Report

Return a compact status report:

```text
Stage: <stage>
Focus: <Epic > Feature > Task | none recorded>
Evidence: <explicit stage file or the artifacts used for inference>
Recovery: <active.md path when present | none>
```

Call out contradictory evidence, an unrecognized explicit stage, or malformed status markers without changing the files.
