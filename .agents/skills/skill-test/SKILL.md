---
name: skill-test
description: "Validate Codex skills for structural compliance, UI metadata, migration residue, behavioral specifications, and catalog coverage. Use for one skill or the complete project skill set."
---

# Skill Test

## Invocation and execution

Invoke this workflow as `$skill-test`.

Arguments: `static [skill-name | all] | spec [skill-name] | category [skill-name | all] | audit`.

All four modes are read-only. Present results in conversation and do not create
result files or update catalog fields.

Use `CGS Skill Testing Framework/catalog.yaml`, `CGS Skill Testing Framework/quality-rubric.md`, and the registered spec paths as the testing authority. Do not guess spec paths.

## Phase 1: Parse the mode

- `static [name]`: run structural checks for one `.agents/skills/[name]/` package.
- `static all`: run structural checks for every `.agents/skills/*/SKILL.md` package.
- `spec [name]`: evaluate the skill against its registered behavioral spec.
- `category [name|all]`: evaluate the matching category rubric.
- `audit`: report skill and Codex-agent coverage, missing specs, and recorded test-field state.

If the mode is missing or invalid, show these forms and stop without writing.

## Phase 2: Static validation

Run `skill-creator/scripts/quick_validate.py` only when that existing validator
is discoverable in the current tool environment. If it is unavailable, record
that as `INFO` and still execute all seven project checks:

1. **Frontmatter**: `SKILL.md` has exactly `name` and `description`; both are non-empty. Any additional key is a failure.
2. **Identity**: folder name equals `name`, uses lowercase letters, digits, and hyphens, and is at most 64 characters.
3. **Instructions**: the body contains actionable workflow instructions. Fail
   only unresolved migration placeholders in final executable instructions;
   illustrative `[name]` tokens inside examples and output templates are valid.
4. **UI metadata**: `agents/openai.yaml` has quoted `display_name`, a specific
   25–64 Unicode-character `short_description`, and a `default_prompt`
   containing the exact `$[name]` invocation. A description that is truncated
   or lacks a complete meaning is at least a warning even when its length passes.
5. **Codex compatibility**: fail on legacy-platform-only paths, fields, product
   names, or tool names only when an existing repository migration document
   explicitly identifies them as residue; cite that rule. If no such authority
   exists, do not invent a legacy vocabulary. Continue to fail a project skill
   invoked as `/name` instead of `$name`.
6. **Collaboration boundary**: a writing workflow states the single changeset approval policy; a read-only workflow explicitly says it does not modify files.
7. **Handoff and links**: referenced project skills use `$name`, linked project paths exist or are explicitly described as future outputs, and the workflow ends with a clear result or next action.

Classify each check as `PASS`, `WARN`, or `FAIL`, cite the exact file and line for every issue, and aggregate results without hiding partial failures.

## Phase 3: Static behavioral-contract validation

1. Locate the skill at `.agents/skills/[name]/SKILL.md`.
2. Read its entry from `CGS Skill Testing Framework/catalog.yaml`.
3. Read the registered spec completely.
4. Compare each fixture, expected behavior, and assertion with the written workflow.
5. Mark assertions `PASS`, `PARTIAL`, or `FAIL` and explain non-passing results with direct evidence.
6. State explicitly that PASS means written-contract coverage only; this mode
   does not execute the fixture or target skill.

If the skill, catalog entry, or spec is missing, report the artifact as a
`FAIL`. A single-target invocation ends `NON-COMPLIANT`. In `all` or `audit`,
continue with the other targets and include every missing artifact in the final
failure total; do not hide the result as partial or guess a path.

## Phase 4: Category validation

Read the skill's `category` from the catalog and the matching section of
`CGS Skill Testing Framework/quality-rubric.md`. Evaluate every category metric
independently. If the category has no matching section or no defined metrics,
report a NON-COMPLIANT authority error; do not invent rules. For `category all`,
continue after individual failures and provide a complete summary.

## Phase 5: Audit coverage

Compare these separately normalized identity sets:

- skill implementations: frontmatter `name` from `.agents/skills/*/SKILL.md`;
- role implementations: TOML `name` from `.codex/agents/**/*.toml`, excluding
  generator/helper TOML files rather than counting non-TOML helpers;
- catalog skill/role names and their registered spec mappings;
- spec names resolved through the catalog mappings.

Report duplicates within each set before comparing sets, plus unregistered
implementations, missing or orphaned specs, and missing UI metadata. For each
existing catalog `last_*` result/date field, report whether it is missing,
present, and parseable. Do not call a date stale because no repository policy
defines a staleness threshold. Treat `$studio-status` like every other project skill.

## Phase 6: Present Results

Present the complete result in conversation and make no file changes. Do not
persist results and do not update catalog `last_*` fields.

Verdict: `COMPLIANT`, `WARNINGS`, or `NON-COMPLIANT`.
