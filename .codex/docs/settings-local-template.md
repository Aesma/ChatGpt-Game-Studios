# Personal Codex Configuration Guide

The filename is retained as a migration reference; Codex does not use
`settings.local.json`.

- Put personal defaults in `~/.codex/config.toml`.
- Put shared, trusted-repository settings in `.codex/config.toml`.
- Put personal lifecycle hooks in `~/.codex/hooks.json`.
- Keep the repository's shared hook registration in `.codex/hooks.json`.

Do not create a second untracked `.codex/config.toml` inside this repository;
it would shadow or conflict with the checked-in project configuration.

Use the Codex UI or CLI surface to choose personal permission, model, and reasoning
settings. The trusted repository supplies `project-edit` as its default permission
profile but does not pin a model or reasoning effort; all 49 subagent roles inherit
the parent session.

Use only keys supported by your installed Codex version in personal config.
Project-local config is loaded only after the repository is trusted.

## Permission Modes

- **Implementation**: choose the project's `project-edit` permission profile in
  the Codex surface.
- **Review or planning**: choose a read-only permission mode.
- **Broader access**: use only for a specific trusted workflow and return to a
  tighter mode afterward.

Do not set `sandbox_mode` in a config layer that also relies on permission
profiles. A loaded `sandbox_mode` bypasses the profile selection, including the
project's `.env` deny rules. Use one permission mechanism consistently; this
repository uses profiles.

Sandbox approval and workflow authorization are different. An explicit bounded
user request authorizes its in-scope changeset, but Codex must still request any
platform approval required to leave the sandbox, use restricted network access,
or perform another separately gated action.

## Personal Hooks

Personal hooks belong in `~/.codex/hooks.json`; project hooks belong in
`.codex/hooks.json`. Do not define the same hook set both in `hooks.json` and an
inline `[hooks]` table at the same config layer. See the
[official hooks documentation](https://learn.chatgpt.com/docs/hooks) for current
events, input fields, and command output behavior.
