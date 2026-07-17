# Lead Programmer — Repository Guidance

> Scope: this file is checked-in guidance for this repository only. It is not
> automatically persisted across projects and is not a substitute for Codex or
> ChatGPT memory controls.

## Skill authoring conventions

### Frontmatter

- Skills live at `.agents/skills/<name>/SKILL.md`.
- Follow the active Codex skill schema used by neighboring migrated skills.
- Do not reintroduce legacy provider-specific tool allowlists, model pins,
  fork-context declarations, or agent-routing frontmatter.
- Put runtime workflow and capability guidance in the skill body when needed;
  actual tools and permissions remain controlled by the parent Codex session.

### File layout

- Use one subdirectory per skill; never use flat skill Markdown files.
- Use `##` for phases and `###` for subsections.
- Phase names follow `Phase N: Verb Noun` where practical.
- Put output-format templates in fenced code blocks.
- Treat an explicitly authorized bounded changeset as sufficient permission to
  write; request a new decision only when materially expanding scope.

### Known canonical paths

- Tech debt register: `docs/tech-debt-register.md`
- Sprint files: `production/sprints/`
- Epic story files: `production/epics/[epic-slug]/story-[NNN]-[slug].md`
- Control manifest: `docs/architecture/control-manifest.md`
- Session state: `production/session-state/active.md`
- Systems index: `design/gdd/systems-index.md`
- Engine reference: `docs/engine-reference/[engine]/VERSION.md`

Verify a path exists before introducing a new reference.

### Previously completed workflow

- `story-done` — end-of-story completion handshake; writes the story file as
  part of its authorized changeset.
