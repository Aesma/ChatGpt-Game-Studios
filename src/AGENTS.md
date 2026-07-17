# Source Directory

Apply these standards whenever writing or editing game code under `src/`.

## Engine Version Warning

Engine APIs change over time. Always check `docs/engine-reference/` before using
an engine API, and verify signatures against the pinned reference instead of
guessing.

## Coding Standards

- All public APIs require doc comments.
- Gameplay values must be data-driven through external configuration, never hardcoded.
- Prefer dependency injection over singletons for testability.
- Every new system needs a corresponding ADR in `docs/architecture/`.
- Commits must reference the relevant story ID or design document.

## File Routing

Match the engine-specialist Codex subagent to the file type being written. See
the file-extension routing section in `.codex/docs/technical-preferences.md`.
When in doubt, use the primary engine specialist configured there.

## Tests

Tests live in `tests/`, not in `src/`. Invoke `$test-setup` to scaffold the test
framework if it does not exist. Every gameplay system should have unit tests for
its formulas and edge cases.

## Verification-Driven Development

Write tests first when adding gameplay systems. For UI changes, verify with
screenshots. Compare expected and actual output before declaring work complete.
