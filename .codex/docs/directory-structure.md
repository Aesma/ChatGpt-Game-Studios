# Directory Structure

```text
/
├── AGENTS.md                    # Repository-wide Codex guidance
├── .agents/
│   └── skills/                  # 74 reusable `$skill` workflows
├── .codex/
│   ├── config.toml              # Runtime defaults, permissions, and global agent limits
│   ├── hooks.json               # Codex lifecycle hook registration
│   ├── hooks/                   # Hook scripts invoked by hooks.json
│   ├── agents/                  # 49 auto-discovered Codex subagent TOML definitions
│   ├── rules/                   # Sandbox-external command policy (execpolicy)
│   ├── guidance/agent-memory/   # Repository-only role guidance and memory
│   └── docs/                    # Framework guidance and document templates
├── src/                         # Game source; nested AGENTS.md files scope code rules
├── assets/                      # Art, audio, VFX, shaders, and data
├── design/                      # GDDs, narrative, levels, and balance docs
├── docs/                        # Architecture, engine reference, and project docs
│   └── engine-reference/        # Version-pinned engine API snapshots
├── tests/                       # Unit, integration, performance, and playtest suites
├── tools/                       # Build and pipeline tools
├── prototypes/                  # Throwaway prototypes isolated from src/
├── CGS Skill Testing Framework/ # Behavioral specs for 74 skills and 49 subagents
└── production/                  # Sprints, milestones, releases, and recovery state
    ├── session-state/           # Active recovery checkpoint
    └── session-logs/            # Optional session audit trail
```

Codex loads `AGENTS.md` from the repository root down to the working directory.
The closest nested file supplies the most specific rules for that subtree.
