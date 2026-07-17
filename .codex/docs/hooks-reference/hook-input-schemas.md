# Hook Input/Output Schemas

Every active event receives JSON on stdin. Common fields include `session_id`,
`turn_id`, `cwd`, `permission_mode`, and `hook_event_name`; handlers should ignore
unknown fields so the schema can evolve. The examples below show only fields used
by this repository. See the
[official Codex hooks documentation](https://learn.chatgpt.com/docs/hooks) for the
current complete contract.

## PreToolUse

Fired before a tool is executed. Can **allow** (exit 0) or **block** (exit 2).

### `PreToolUse`: `Bash`

```json
{
  "session_id": "session_123",
  "turn_id": "turn_456",
  "cwd": "D:/Workspace/AI/ChatGPT-Game-Studios",
  "permission_mode": "project-edit",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "git commit -m 'feat: add player health system'"
  }
}
```

The three registered `PreToolUse` handlers all match `^Bash$` and read
`tool_input.command`. `validate-command-safety.sh` inspects every command;
commit and push validators return immediately when their command does not match.

## PostToolUse

Fired after a tool completes. The registry matches only `^apply_patch$`.
`tool_input.command` contains the submitted patch and `tool_response` contains
the completed tool result.

### `PostToolUse`: `apply_patch`

```json
{
  "session_id": "session_123",
  "turn_id": "turn_456",
  "cwd": "D:/Workspace/AI/ChatGPT-Game-Studios",
  "hook_event_name": "PostToolUse",
  "tool_name": "apply_patch",
  "tool_input": {
    "command": "*** Begin Patch\n*** Update File: assets/data/enemy_stats.json\n...\n*** End Patch"
  },
  "tool_response": {
    "status": "completed"
  }
}
```

An exit code of 2 supplies feedback after the edit; it does not undo or block the
already-completed patch.

## SubagentStart

Fired when a subagent is spawned via the Codex subagent tools.

```json
{
  "session_id": "session_123",
  "turn_id": "turn_456",
  "cwd": "D:/Workspace/AI/ChatGPT-Game-Studios",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent_789",
  "agent_type": "game-designer"
}
```

`SubagentStop` uses the same `agent_id` and `agent_type` identity fields. On a
successful exit it must print a valid JSON hook response such as
`{"continue":true}`.

## Session and compaction events

- `SessionStart`, `PreCompact`, `PostCompact`, and `Stop` all receive JSON on stdin,
  including the common fields above.
- `SessionStart` may emit repository context for Codex.
- Plain stdout from `PreCompact` and `PostCompact` is ignored; these hooks persist
  recovery state through repository files instead.
- A successful `Stop` handler must print a valid JSON hook response such as
  `{"continue":true}`.

## Exit Code Reference

| Exit Code | Meaning | Applicable Events |
|-----------|---------|-------------------|
| 0 | Allow or success; `Stop` and `SubagentStop` must also emit valid JSON | All events |
| 2 | Block the pending tool and surface stderr | `PreToolUse` |
| 2 | Surface post-tool feedback; the completed edit is not rolled back | `PostToolUse` |
| Other | Hook error; event-specific Codex handling applies | All events |

## Notes

- Hooks receive JSON on stdin. The shared `hook-lib.sh` captures it once.
- Structured extraction uses `jq`, then Python, then a limited `sed` fallback.
- On Windows, `grep -P` (Perl regex) is often unavailable. Use `grep -E` (POSIX extended) instead.
- Path separators may be `\` on Windows. Normalize with `sed 's|\\|/|g'` when comparing paths.
- Hook checks are guardrails. Filesystem denies such as `**/.env*` come from the
  `.codex/config.toml` permission profile, not a hook payload convention.
