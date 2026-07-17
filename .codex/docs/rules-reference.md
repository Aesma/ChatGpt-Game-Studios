# Path-Specific Rules

Codex applies directory guidance through nested `AGENTS.md` files. Each migrated
rule lives at the root of the subtree it governs, so no glob frontmatter or
runtime rule adapter is required.

| Instruction file | Effective path | Enforces |
| ---------------- | -------------- | -------- |
| `src/gameplay/AGENTS.md` | `src/gameplay/**` | Data-driven values, delta time, no UI references |
| `src/core/AGENTS.md` | `src/core/**` | Zero allocations in hot paths, thread safety, API stability |
| `src/ai/AGENTS.md` | `src/ai/**` | Performance budgets, debuggability, data-driven parameters |
| `src/networking/AGENTS.md` | `src/networking/**` | Server authority, versioned messages, security |
| `src/ui/AGENTS.md` | `src/ui/**` | No game-state ownership, localization, accessibility |
| `design/gdd/AGENTS.md` | `design/gdd/**` | Eight required sections, formulas, edge cases |
| `design/narrative/AGENTS.md` | `design/narrative/**` | Lore consistency, voice, canon levels |
| `assets/data/AGENTS.md` | `assets/data/**` | JSON validity, naming, schemas |
| `tests/AGENTS.md` | `tests/**` | Test naming, isolation, fixtures, regression coverage |
| `prototypes/AGENTS.md` | `prototypes/**` | Relaxed standards, required hypothesis and findings |
| `assets/shaders/AGENTS.md` | `assets/shaders/**` | Naming, performance budgets, cross-platform rules |

Repository-wide guidance comes from the root `AGENTS.md`; a nested file adds or
overrides guidance only for its own directory tree.

Nested `AGENTS.md` files are behavioral guidance, not filesystem enforcement.
`.codex/rules/project-safety.rules` is an execpolicy for commands that run outside
the sandbox. The `project-edit` permission profile in `.codex/config.toml`
enforces filesystem boundaries such as the `**/.env*` deny.
