# Repository-scoped agent guidance

Files below this directory are checked-in project guidance migrated from the
legacy agent-memory templates. They are not ChatGPT memory, are not Codex's
local memory store under `~/.codex/memories`, and must never be treated as
personal or cross-project memory.

Custom agents may consult a matching `<agent-name>/MEMORY.md` when their TOML
instructions point to it. Required team rules still belong in `AGENTS.md` or
other checked-in documentation. Do not store secrets, credentials, private user
preferences, chat transcripts, or machine-specific state here.
