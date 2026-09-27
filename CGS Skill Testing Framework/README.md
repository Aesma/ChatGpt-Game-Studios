# CGS Skill Testing Framework

Quality-assurance infrastructure for **ChatGPT Game Studios**. It tests the
repository's reusable skills and Codex subagent definitions, not games created
with the framework.

The framework currently covers **74 skills** and **49 Codex subagents**. These
totals are verification results, not constants: every audit must recompute them
recursively from the implementation directories and compare them with the catalog
and spec directories.

## Coverage Contract

An audit is complete only when all four sets agree by unique name:

| Surface | Recursive source | Expected now |
|---------|------------------|--------------|
| Skill implementations | `.agents/skills/**/SKILL.md` | 74 |
| Skill catalog entries | `catalog.yaml` under `skills:` | 74 |
| Skill behavioral specs | `skills/**/*.md` | 74 |
| Codex subagent definitions | `.codex/agents/**/*.toml`, excluding generators | 49 |
| Subagent catalog entries | `catalog.yaml` under `agents:` | 49 |
| Subagent behavioral specs | `agents/**/*.md` | 49 |

The audit must report missing names, duplicates, stale spec paths, and orphaned
specs. A matching numeric total alone does not prove coverage.

## Layout

```text
CGS Skill Testing Framework/
├── AGENTS.md
├── README.md
├── catalog.yaml
├── quality-rubric.md
├── templates/
│   ├── skill-test-spec.md
│   └── agent-test-spec.md
├── skills/
│   ├── gate/
│   ├── review/
│   ├── authoring/
│   ├── readiness/
│   ├── pipeline/
│   ├── analysis/
│   ├── team/
│   ├── sprint/
│   └── utility/
├── agents/
└── results/                 # optional run output; gitignored
```

`catalog.yaml` is authoritative for category, priority, spec path, and last-test
metadata. The filesystem remains authoritative for discovery and coverage totals.

## Using the Framework

```text
$skill-test static [skill-name|all]     # structural checks
$skill-test spec [skill-name]           # behavioral spec evaluation
$skill-test category [skill-name|all]   # category rubric
$skill-test audit                       # recursive coverage comparison
$skill-improve [skill-name]             # diagnose, revise, and retest
```

Important coverage additions in this migration:

- `skills/pipeline/vertical-slice.md` covers the previously missing
  `$vertical-slice` behavior.
- `skills/utility/studio-status.md` covers `$studio-status`, the read-only Codex
  replacement for the unsupported live terminal status line.

## Codex Structural Baseline

A migrated skill is rooted at `.agents/skills/<name>/SKILL.md`. Its YAML
frontmatter requires a matching `name` and a non-empty `description`; invocation,
arguments, delegation, and safety requirements belong in the Markdown body.
Behavioral tests must require only the frontmatter used by the migrated Codex
skill format; provider-specific metadata belongs neither in assertions nor new
skill files.

Codex subagents are configured by `.codex/agents/<name>.toml`. Agent specs should
verify the effective role, boundaries, delegation behavior, and output contract,
and confirm that all roles inherit the parent-session model and reasoning settings.

## Changeset Authorization Policy

An explicit bounded user task authorizes all writes within that scope. If the
user has not authorized a bounded change, present the proposed changeset and ask
once before applying it. Do not ask again for every file, section, or edit.
Request new direction only when work materially expands scope or reaches a
separately gated destructive or external action.

Specs should test this policy directly. They must not require the legacy phrase
or one approval prompt per file.

## Adding a Spec

1. Discover the implementation under `.agents/skills/` or `.codex/agents/`.
2. Copy the matching template from `templates/`.
3. Add the behavioral spec under the appropriate recursive category.
4. Add a unique catalog entry whose `spec:` path points to the new file.
5. Run `$skill-test audit`, then `$skill-test spec <name>`.

The specs describe agreed current behavior. If implementation and spec disagree,
investigate the implementation first; update whichever side is wrong rather than
changing the test merely to make it pass.

## Optional and Self-Contained

Nothing under `.agents/` or `.codex/` imports this directory at runtime. Removing
the testing framework does not disable skills or subagents, although coverage and
behavioral QA commands will no longer have their catalog and specs.
