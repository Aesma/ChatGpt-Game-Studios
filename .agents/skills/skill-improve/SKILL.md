---
name: skill-improve
description: "Improve a Codex skill with a validate-diagnose-patch-revalidate loop, keeping changes only when structural and behavioral results improve."
---

# Skill Improve

## Invocation and execution

Invoke this workflow as `$skill-improve [skill-name]`.

Arguments: `[skill-name]` is required and must match a folder under `.agents/skills/`.

Arguments: `[skill-name]` is required and must match a folder under `.agents/skills/`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

## Phase 1: Locate the skill

Require one skill name and verify `.agents/skills/[name]/SKILL.md` and `agents/openai.yaml` exist. Read the skill, its catalog entry, and any registered spec before diagnosing it.

## Phase 2: Establish a baseline

Run `$skill-test static [name]`. If the catalog assigns a category, also run `$skill-test category [name]`; run `$skill-test spec [name]` when a behavioral spec exists. Record every failure and warning with file-and-line evidence.

If all applicable checks pass, report that no improvement is needed and stop.

## Phase 3: Diagnose narrowly

Map each issue to the Codex skill contract:

1. frontmatter must contain only `name` and `description`;
2. folder and skill names must match;
3. instructions must be actionable and complete;
4. `agents/openai.yaml` must be specific, valid, and invoke `$name`;
5. legacy-platform-only paths, fields, tools, and legacy slash-form skill calls must be absent;
6. writing workflows need one changeset approval before the first write;
7. links, results, and handoffs must be coherent.

Include category or spec failures separately. Do not rewrite passing sections merely for style.

## Phase 4: Preview one changeset

Show concise before/after excerpts and list every file to change, including `SKILL.md`, `agents/openai.yaml`, and any directly affected spec or catalog entry. Obtain one approval for this complete changeset.

## Phase 5: Apply and revalidate

After approval, apply all listed edits without further file-by-file prompts. Re-run every baseline check and compare before/after counts. If the proposed fix requires additional files or broader behavior changes, stop and request a revised changeset approval.

## Phase 6: Keep or restore

- If results improve and no new failures appear, keep the edits and report the evidence.
- If results are unchanged or worse, restore the saved original contents as part of the already disclosed conditional changeset, then re-run static validation.

Do not use destructive repository-wide reset commands.

## Phase 7: Handoff

Recommend `$skill-test static all`, `$skill-test audit`, or `$skill-improve [next-name]` based on the remaining findings.
