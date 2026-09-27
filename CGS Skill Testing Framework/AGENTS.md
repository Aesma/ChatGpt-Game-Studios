# CGS Skill Testing Framework — Codex Instructions

This folder is the quality-assurance layer for the ChatGPT Game Studios skills
and Codex subagents. It is self-contained and does not contain game-project tests.

## Key Files

| File | Purpose |
|------|---------|
| `catalog.yaml` | Master registry for skills and subagents, including spec paths and last-test fields. Read this first. |
| `quality-rubric.md` | Category-specific pass/fail metrics used by `$skill-test category`. |
| `skills/[category]/[name].md` | Behavioral spec for a skill. |
| `agents/[tier]/[name].md` | Behavioral spec for a Codex subagent. |
| `templates/skill-test-spec.md` | Template for a new skill spec. |
| `templates/agent-test-spec.md` | Template for a new subagent spec. |
| `results/` | Optional saved test results; gitignored. |

The catalog's `spec:` field is authoritative. Do not infer a path when a catalog
entry exists. Coverage totals must be computed recursively from the actual
`.agents/skills/**/SKILL.md`, `.codex/agents/**/*.toml` (excluding generators),
and spec files rather than copied from prose. The current verified baseline is
74 skills and 49 Codex subagents; compare unique names, not only totals.

## Testing a Skill

1. Read `catalog.yaml` for the skill's spec and category.
2. Read `.agents/skills/[name]/SKILL.md`.
3. Read the listed behavioral spec.
4. Evaluate every assertion case by case.
5. Save results under `results/` and update catalog fields when that changeset is
   within the user's bounded request. Otherwise present the proposed changeset
   and ask once.

Invoke `$skill-improve [name]` for the test → diagnose → propose → revise →
retest loop.

Specs describe current intended behavior. When behavior and a spec disagree,
investigate the implementation first, then update the spec to the agreed behavior.

An explicit bounded user task authorizes its in-scope files. Never request
approval again per file, section, or edit. Ask again only when the work materially
expands scope or reaches a separately gated destructive or external action.

Nothing in `.agents/` or `.codex/` imports this directory. Removing the framework
does not disable skills or subagents; `$skill-test` should report the missing
catalog and explain how to regenerate coverage.
