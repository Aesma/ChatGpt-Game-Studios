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

1. Read `production/stage.txt` when present. Trim the first line only to
   determine emptiness; when non-empty, display that first line's effective
   text rather than any later content. If any later line is non-empty, report the file as malformed;
   never concatenate it into Stage.
2. Regardless of whether an explicit value exists, inspect the following
   evidence to calculate an inference for Evidence/Warning only:
   - `design/gdd/game-concept.md`
   - `design/gdd/systems-index.md`
   - `docs/technical-preferences.md`
   - `docs/architecture/adr-*.md`
   - source files under `src/` with extensions `.gd`, `.cs`, `.cpp`, `.h`, `.py`, `.rs`, `.lua`, `.tscn`, or `.tres`
3. For technical preferences, read every `**Engine**:` or
   `- **Engine**:` entry. Ignore blank/placeholder values. Exactly one
   consistent non-placeholder value is configured; multiple distinct values are
   contradictory evidence and no value is chosen for inference.
4. Infer the most advanced supported stage in this order:
   - At least 10 recognized source files: `Production`
   - At least one ADR: `Pre-Production`
   - Engine configured: `Technical Setup`
   - Systems index present: `Systems Design`
   - Game concept present: `Concept`
   - No evidence: `Concept`

The complete legal set is exactly `Concept`, `Systems Design`,
`Technical Setup`, `Pre-Production`, `Production`, `Polish`, and
`Release`. Only an explicit `production/stage.txt` may select `Polish` or
`Release`. If the explicit value is missing/empty, use the inference as Stage. If it is
non-empty, never replace it with the inference; report contradictory evidence
as a warning. Also warn when the explicit value is outside Concept, Systems
Design, Technical Setup, Pre-Production, Production, Polish, or Release.

## Build the active breadcrumb

Whenever `production/session-state/active.md` exists, verify that exactly paired
`<!-- STATUS -->` and `<!-- /STATUS -->` markers bound the status block. Report
missing, duplicate, reversed, or otherwise malformed markers for every stage,
including an unrecognized explicit stage.

For a valid `Production`, `Polish`, or `Release` stage and valid paired markers:

1. Read only the bounded status block.
2. Extract optional `Epic:`, `Feature:`, and `Task:` values.
3. Join non-empty values in that order with ` > `.
4. If the block or all values are absent, report that no active focus is recorded.

For a valid earlier stage, keep the required field and report
`Focus: not applicable`. For a valid late stage with no bounded breadcrumb,
report `Focus: none recorded`. For an unrecognized stage, use
`Focus: not applicable` unless the user explicitly asks for bounded raw
details. Never extract focus from unbounded/malformed text.

## Report

Return a compact status report:

```text
Stage: <stage>
Focus: <Epic > Feature > Task | none recorded>
Evidence: <explicit stage file or the artifacts used for inference>
Recovery: <active.md path when valid | active.md path — malformed STATUS block | none>
```

Call out contradictory evidence, an unrecognized/extra-line stage file, or
malformed status markers without changing files. A malformed active.md path may
be shown for diagnosis but is not described as a usable recovery breadcrumb.
