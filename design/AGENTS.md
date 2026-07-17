# Design Directory

Apply these standards whenever authoring or editing files under `design/`.

## GDD Files (`design/gdd/`)

Every GDD must include all eight required sections in this order:

1. Overview — one-paragraph summary
2. Player Fantasy — intended feeling and experience
3. Detailed Rules — unambiguous mechanics
4. Formulas — all math defined with variables
5. Edge Cases — unusual situations handled
6. Dependencies — other systems listed
7. Tuning Knobs — configurable values identified
8. Acceptance Criteria — testable success conditions

Use `[system-slug].md` filenames, such as `movement-system.md`. Update
`design/gdd/systems-index.md` whenever adding a GDD. Design in this order:
Foundation → Core → Feature → Presentation → Polish.

Invoke `$design-review [path]` after authoring a GDD and `$review-all-gdds`
after completing a related set.

## Quick Specs (`design/quick-specs/`)

Use quick specs for tuning changes, minor mechanics, or balance adjustments.
Invoke `$quick-design` to author one.

## UX Specs (`design/ux/`)

- Per-screen specs: `design/ux/[screen-name].md`
- HUD design: `design/ux/hud.md`
- Interaction pattern library: `design/ux/interaction-patterns.md`
- Accessibility requirements: `design/ux/accessibility-requirements.md`

Invoke `$ux-design` to author a spec. Validate it with `$ux-review` before
handing work to the UI-focused Codex subagents through `$team-ui`.
