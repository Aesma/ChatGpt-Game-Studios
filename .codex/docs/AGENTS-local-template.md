# AGENTS.override.md Template

Copy this file to the project root as `AGENTS.override.md` for temporary local
instructions. Codex checks `AGENTS.override.md` before `AGENTS.md` at the same
directory level. The override is gitignored and should not be committed.

```markdown
# Personal Preferences

## Reasoning Preferences
- Use deeper reasoning for cross-system or high-stakes design decisions
- Keep simple lookups and mechanical edits concise

## Workflow Preferences
- Always run tests after code changes
- Compact context proactively at 60% usage
- Start a new Codex task for unrelated work

## Local Environment
- Python command: python (or py / python3)
- Shell: Git Bash on Windows
- IDE: VS Code with Codex extension

## Communication Style
- Keep responses concise
- Show file paths in all code references
- Explain architectural decisions briefly

## Personal Shortcuts
- When I say "review", run $code-review on the last changed files
- When I say "status", show git status + sprint progress
```

## Setup

1. Copy this template to your project root: `cp .codex/docs/AGENTS-local-template.md AGENTS.override.md`
2. Edit to match your preferences
3. Verify `AGENTS.override.md` is in `.gitignore`
4. Remove the override when you want the shared `AGENTS.md` to apply again
