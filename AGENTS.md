# ChatGPT Game Studios — Codex Project Instructions

This repository turns one Codex task into a coordinated game-development studio.
Use the 49 domain subagents in `.codex/agents/` for delegation and the reusable
skills in `.agents/skills/` for repeatable workflows. Keep domain ownership,
quality gates, and user decisions explicit.

## Technology Stack

- **Engine**: [CHOOSE: Godot 4 / Unity / Unreal Engine 5]
- **Language**: [CHOOSE: GDScript / C# / C++ / Blueprint]
- **Version Control**: Git with trunk-based development
- **Build System**: [SPECIFY after choosing engine]
- **Asset Pipeline**: [SPECIFY after choosing engine]

Engine-specific subagents exist for Godot, Unity, and Unreal. Use only the set
matching the project's selected engine.

## Project Guidance

Codex does not expand `@file` directives in this file. Read the linked guidance
when its subject applies:

- [Directory structure](.codex/docs/directory-structure.md)
- [Engine version reference](docs/engine-reference/godot/VERSION.md)
- [Technical preferences](docs/technical-preferences.md)
- [Coordination rules](.codex/docs/coordination-rules.md)
- [Coding standards](.codex/docs/coding-standards.md)
- [Context management](.codex/docs/context-management.md)
- [Worktree collaboration](.codex/docs/worktree-workflow.md) — read when working in a linked worktree, handing off branch results, or integrating parallel work.

Nested `AGENTS.md` files add more specific requirements for their directory
trees. The closest applicable file takes precedence when guidance differs.

Linked-worktree workflows keep their normal skill entrypoints and apply the
shared worktree protocol to scope and handoff; ordinary local tasks do not
automatically create worktrees.

## Collaboration Protocol

For open-ended design choices, follow **Question → Options → Decision → Draft →
Approval**. Show meaningful tradeoffs and let the user make product decisions.
Once the user authorizes a bounded implementation or migration, carry it through
without asking for approval again for every file. Never commit, push, publish, or
perform destructive cleanup without the user's instruction.

See [Collaborative Design Principle](docs/COLLABORATIVE-DESIGN-PRINCIPLE.md) for
the full protocol and examples.

When starting a game project with no configured engine and no game concept,
invoke `$start` for guided onboarding. Framework maintenance is not game
onboarding.
