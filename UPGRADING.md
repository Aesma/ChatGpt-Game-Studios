# Upgrading ChatGPT Game Studios

This guide describes the active Codex repository layout. Pre-migration release
history remains available in the upstream repository linked from `NOTICE.md`;
legacy provider-specific commands are intentionally not duplicated here.

## Before You Upgrade

1. Commit or otherwise back up project-specific game content.
2. Record custom changes to `AGENTS.md`, `.codex/config.toml`, subagent roles,
   skills, hooks, GDDs, ADRs, and production state.
3. Review the incoming diff before copying infrastructure files.
4. Never overwrite project-specific engine preferences, game designs, assets,
   sprint state, or session recovery files without a deliberate merge.

## Active Repository Surfaces

| Surface | Current location |
| ------- | ---------------- |
| Repository guidance | `AGENTS.md` and nested `**/AGENTS.md` |
| Reusable skills | `.agents/skills/<name>/SKILL.md` |
| Codex subagents | Project-scoped roles auto-discovered from `.codex/agents/<name>.toml` |
| Runtime defaults | `.codex/config.toml` permission profile, hook feature, and global agent limits |
| Project hooks | `.codex/hooks.json` and `.codex/hooks/*.sh` |
| Framework docs/templates | `.codex/docs/` |
| Skill/subagent QA | `CGS Skill Testing Framework/` |

Codex loads project config and hooks only for a trusted repository.

## Migrating from the Upstream Claude Version

This repository is a Codex adaptation of the upstream **Claude Code Game
Studios** project. The active migration mapping is:

| Upstream concept | Codex version |
| ---------------- | ------------- |
| Root and directory instruction files | Root and nested `AGENTS.md` |
| Provider-specific skills | `.agents/skills/` with `$skill-name` invocation |
| Markdown agent definitions | Auto-discovered `.codex/agents/*.toml` subagent roles |
| Provider-specific framework docs | `.codex/docs/` |
| Settings and hook registration | `.codex/config.toml` and `.codex/hooks.json` |
| Glob-scoped rule files | Nested `AGENTS.md` in the governed directory |
| Live terminal status line | Read-only `$studio-status` workflow |
| Hard-coded provider model tiers | All roles inherit the parent-session model and reasoning settings; no per-role overrides |
| Per-file write prompts | One bounded changeset authorization; re-prompt only for material scope expansion |

Legacy source paths are not active compatibility aliases. Remove them after the
migrated surfaces have been verified and project-specific content has been merged.

## Updating from This Repository

Add the template as a remote once:

```bash
git remote add template https://github.com/Aesma/ChatGpt-Game-Studios.git
git fetch template
```

Inspect changes before merging:

```bash
git log --oneline HEAD..template/main
git diff --stat HEAD...template/main
git diff HEAD...template/main -- AGENTS.md .agents .codex "CGS Skill Testing Framework"
```

Choose a normal Git merge, cherry-pick, or manual merge appropriate to your fork.
Do not use destructive reset commands to upgrade a project with local game content.

## Merge Guidance

Usually safe to replace after review:

- Unmodified skills under `.agents/skills/`
- Unmodified subagent definitions under `.codex/agents/`
- Shared templates under `.codex/docs/templates/`
- Hook scripts when the local hook contract is unchanged
- Behavioral specs under `CGS Skill Testing Framework/`

Merge carefully:

- `AGENTS.md` and nested instruction files
- `.codex/config.toml` and `.codex/hooks.json`
- `.codex/docs/technical-preferences.md`
- Customized skills, subagent roles, or QA specifications
- Anything under `design/`, `docs/architecture/`, `assets/`, `src/`, `tests/`,
  `prototypes/`, or `production/`

## Verification After Upgrade

Verify active surfaces recursively rather than trusting documented constants:

```powershell
(Get-ChildItem .agents\skills -Recurse -Filter SKILL.md).Count
(Get-ChildItem .codex\agents -Recurse -Filter *.toml).Count
(Get-ChildItem 'CGS Skill Testing Framework\skills' -Recurse -Filter *.md).Count
(Get-ChildItem 'CGS Skill Testing Framework\agents' -Recurse -Filter *.md).Count
```

The current release should report 74 skill implementations, 49 subagent TOML
definitions, 74 skill specs, and 49 subagent specs. Also verify:

1. Every catalog name is unique and maps to an implementation and spec.
2. `.codex/hooks.json` parses and every registered script exists.
3. All shell hooks use LF line endings.
4. `$studio-status` reports a stable result for the current project state.
5. `$skill-test audit` reports no missing, duplicate, or orphaned entries.
6. Searches outside the provenance notice find no active legacy-provider names,
   legacy paths, or slash-style skill calls.

## License and Provenance

The MIT [`LICENSE`](LICENSE) is preserved unchanged. See [`NOTICE.md`](NOTICE.md)
for upstream authorship and adaptation provenance.
