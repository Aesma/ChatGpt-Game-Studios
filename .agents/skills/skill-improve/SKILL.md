---
name: skill-improve
description: "Improve a Codex skill with a validate-diagnose-patch-revalidate loop, keeping changes only when structural and behavioral results improve."
---

# Skill Improve

## Invocation and execution

Invoke this workflow as `$skill-improve [skill-name]`.

Arguments: `[skill-name]` is required. Accept only one lowercase-letter,
digit, or hyphen directory name (`^[a-z0-9]+(?:-[a-z0-9]+)*$`). Reject path
separators, `.`, `..`, absolute paths, and names that would resolve outside
`.agents/skills/`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

## Phase 1: Locate the skill

Require one valid skill name and verify `.agents/skills/[name]/SKILL.md` and
`agents/openai.yaml` exist. If the name is invalid, the directory is absent, or
either required file is missing, stop without guessing another path.

Read the skill and its catalog entry. If a registered spec exists, read it. A
missing catalog entry or registered spec is a retained `FAIL / NON-COMPLIANT`
finding, not `N/A`: continue every other available static check, but do not
claim the skill is improved until the missing existing artifact is restored.

If `[skill-name]` is `skill-improve`, complete diagnosis and prepare a proposed
patch only. Do not apply changes to the instructions that govern the current
run; hand the approved draft to a later independent invocation.

## Phase 2: Establish a baseline

Run `$skill-test static [name]`. If the catalog assigns a category, also run
`$skill-test category [name]`; run `$skill-test spec [name]` when a behavioral
spec exists. Record every existing check/assertion by stable identity, status,
and file-and-line evidence. Counts are summary only.

Stop with `NO CHANGE` only when every applicable check is `PASS` and there are
zero `WARN` results. A warning remains eligible for a narrow repair.

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

Show concise before/after excerpts and list only the existing files actually
required for the diagnosed repair, with the exact purpose of each edit. Default
edits are the target `SKILL.md` and metadata, but do not list either unless it
actually changes. A directly affected spec or catalog entry may change only
when independent static evidence shows it is stale relative to an existing
authoritative project contract; never remove a target behavior, delete an
assertion, lower its severity, or change category to manufacture a pass. Obtain
one approval for the complete changeset.

## Phase 5: Apply and revalidate

Before applying, confirm each target still equals the previewed baseline saved in
memory. After approval, apply all listed edits without further file-by-file
prompts. Re-run every baseline check and compare the same check/assertion
identities, not just aggregate counts. If a proposed fix needs broader files or
behavior, stop and request a revised changeset approval.

## Phase 6: Keep or restore

- Keep edits only when the target issue improves, no new FAIL or WARN appears,
  and no existing check/assertion is downgraded. Counts are summary evidence,
  never the decision rule.
- If any baseline check that previously ran cannot be re-run, treat the result as
  unverified and use the disclosed conditional restore.
- Before restore, confirm every target still equals this run's written result.
  Restore only those verified targets to their in-memory originals, then re-run
  validation. If any target differs, stop without overwriting the concurrent
  edit and report **BLOCKED — restore conflict**; never restore the whole file
  over another writer.

Do not use destructive repository-wide reset commands.

## Phase 7: Handoff

Recommend `$skill-test static all`, `$skill-test audit`, or `$skill-improve [next-name]` based on the remaining findings.
