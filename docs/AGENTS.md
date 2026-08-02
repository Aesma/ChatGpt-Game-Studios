# Docs Directory

Apply these standards whenever authoring or editing files under `docs/`.

## Architecture Decision Records (`docs/architecture/`)

Use `.codex/docs/templates/architecture-decision-record.md`.

Required sections are Title, Status, Context, Decision, Consequences, ADR
Dependencies, Engine Compatibility, and GDD Requirements Addressed.

The status lifecycle is `Proposed` → `Accepted` → `Superseded`. Never skip
`Accepted`; stories referencing a proposed ADR remain blocked. Invoke
`$architecture-decision` for the guided workflow.

## TR Registry (`docs/architecture/tr-registry.yaml`)

- Stable requirement IDs use lowercase system slugs, for example `TR-mov-001`,
  and link GDD requirements to stories.
- Never renumber existing IDs; append new IDs only.
- `$architecture-review` updates the registry during its traceability phase.

## Control Manifest (`docs/architecture/control-manifest.md`)

- Record Required / Forbidden / Guardrail rules per layer.
- Keep a date-stamped `Manifest Version:` in the header.
- Stories embed that version; `$story-done` checks for staleness.

Invoke `$architecture-review` after completing a set of ADRs.

## Engine Reference (`docs/engine-reference/`)

These are version-pinned API snapshots. Check them before using engine APIs.
The current engine selection is recorded in the matching `VERSION.md`, initially
`docs/engine-reference/godot/VERSION.md`.
