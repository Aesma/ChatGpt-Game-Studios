# Active Hooks

Project hooks are registered in `.codex/hooks.json` and implemented under
`.codex/hooks/`. The registry has 12 handlers across 8 Codex events: 11 mappings
from the source project plus one supplemental command-safety handler. Notification
is not counted because Codex uses native `[tui]` desktop notifications instead.

| Script | Event | Matcher / trigger | Action |
| --- | --- | --- | --- |
| `session-start.sh` | `SessionStart` | startup, resume, clear, compact | Loads branch, activity, stage, and recovery context |
| `detect-gaps.sh` | `SessionStart` | startup, resume, clear, compact | Detects fresh projects and documentation gaps |
| `validate-command-safety.sh` | `PreToolUse` | `^Bash$` | Quote-aware inspection of every shell command; blocks commands prohibited by the project safety policy |
| `validate-commit.sh` | `PreToolUse` | `^Bash$`; quality checks only when the command is `git commit` | Checks staged GDD structure, JSON, hardcoded gameplay values, and TODO format |
| `validate-push.sh` | `PreToolUse` | `^Bash$`; exits unless the command is `git push` | Protects configured branches and surfaces push risk |
| `validate-assets.sh` | `PostToolUse` | `^apply_patch$`; ignores paths outside `assets/` | Checks asset naming and JSON validity after the edit |
| `validate-skill-change.sh` | `PostToolUse` | `^apply_patch$`; ignores paths outside `.agents/skills/` | Recommends `$skill-test` after skill changes |
| `pre-compact.sh` | `PreCompact` | manual or automatic compaction | Saves recoverable repository context; plain stdout is ignored by this event |
| `post-compact.sh` | `PostCompact` | manual or automatic compaction | Restores the `active.md` reminder; plain stdout is ignored by this event |
| `log-agent.sh` | `SubagentStart` | any Codex subagent start | Opens an audit entry using `agent_id` and `agent_type` |
| `log-agent-stop.sh` | `SubagentStop` | any Codex subagent stop | Completes the audit entry and returns the required JSON continuation response |
| `session-stop.sh` | `Stop` | task stop | Records session/Git activity and returns the required JSON continuation response |

`hook-lib.sh` is the thirteenth shell script but is a shared helper, not a
registered handler. The 8 registered events are `SessionStart`, `PreToolUse`,
`PostToolUse`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`, and
`Stop`.

## Trust, safety, and notifications

Codex does not load project hooks until the repository is trusted. Review the
resolved registry with `/hooks` before trusting it. Trust is tied to the current
hook-configuration revision, so a registry change is reviewable rather than silently
inheriting an earlier decision.

`PreToolUse` command checks are defense in depth, not the filesystem sandbox.
The `.env*` deny is enforced by the `project-edit` permission profile in
`.codex/config.toml`; the hook does not claim to enforce that boundary.

The source Notification hook was not migrated. Native desktop notification is
configured under `[tui]` in `.codex/config.toml`.

Schema details: [hook-input-schemas.md](hooks-reference/hook-input-schemas.md).
For the current event and output contract, use the
[official Codex hooks documentation](https://learn.chatgpt.com/docs/hooks).
