---
name: content-audit
description: "Audit GDD-specified content counts against implemented content. Identifies what's planned vs built."
---

## Invocation and execution

Invoke this workflow as `$content-audit`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[system-name | --summary | (no arg = full audit)]`. Treat bracketed values as optional unless the workflow says otherwise.

Delegate substantive work to the `producer` Codex subagent role when it is available. If that role is unavailable, follow the same responsibilities in the current agent.


When this skill is invoked:

Parse the argument:
- No argument → full audit across all systems
- `[system-name]` → audit that single system only
- `--summary` → summary table only, no file write

For a system argument, resolve the name through `systems-index.md` and the
mapped GDD path. Exactly one match is required. Missing or ambiguous matches
stop with the candidate list and no report write.

If `producer` is available, it may return an analysis draft only and must not
write files. If it is unavailable, continue in the current agent. If delegation
fails after scanning, produce a partial report from the collected evidence and
name the missing analysis; never fabricate the omitted results.

---

## Phase 1 — Context Gathering

1. **Read `design/gdd/systems-index.md`** for the full list of systems, their
   categories, and MVP/priority tier. Also read existing explicit asset-format
   requirements from the in-scope GDDs and `.codex/docs/technical-preferences.md`
   so implementation format can be compared without inventing a new standard.

2. **L0 pre-scan**: Search all GDD files for `## Summary`/`## Overview`
   and common content-count phrases only to prioritize reading order. A missed
   keyword never excludes a GDD and never proves that it has no auditable
   content.

3. **Read every in-scope GDD** (or the single system GDD if a system name was
   given). At minimum read Summary/Overview, Detailed Rules, Visual and Audio
   requirements, and every section containing an explicit list. If those
   sections cannot be located reliably, read the full document.

4. **For each GDD, extract explicit content counts or lists.** Look for patterns
   like:
   - "N enemies" / "enemy types:" / list of named enemies
   - "N levels" / "N areas" / "N maps" / "N stages"
   - "N items" / "N weapons" / "N equipment pieces"
   - "N abilities" / "N skills" / "N spells"
   - "N dialogue scenes" / "N conversations" / "N cutscenes"
   - "N quests" / "N missions" / "N objectives"
   - Any explicit enumerated list (bullet list of named content pieces)

4. **Build a content inventory table** from the extracted data:

   | System | Content Type | Specified Count/List | Source GDD |
   |--------|-------------|---------------------|------------|

   Note: If a GDD describes content qualitatively but gives no count, record
   "Unspecified" and flag it — unspecified counts are a design gap worth noting.

---

## Phase 2 — Implementation Scan

For each content type found in Phase 1, scan the relevant directories and match
implementation identity. When the GDD names content, match each name against
stable existing file/data references and report the missing names; equal raw
file counts do not prove completion. Treat same-named scene, data, and art files
as one content item. Use approximate file counts only when the GDD gives a total
without names, and label that row `Approximate`.

**Levels / Areas / Maps:**
- Find files matching `assets/**/*.tscn`, `assets/**/*.unity`, `assets/**/*.umap`
- Find files matching `src/**/*.tscn`, `src/**/*.unity`
- Look for scene files in subdirectories named `levels/`, `areas/`, `maps/`,
  `worlds/`, `stages/`
- Count unique files that appear to be level/scene definitions (not UI scenes)

**Enemies / Characters / NPCs:**
- Find files matching `assets/data/**/enemies/**`, `assets/data/**/characters/**`
- Find files matching `assets/art/characters/**`
- Find files matching `src/**/enemies/**`, `src/**/characters/**`
- Look for `.json`, `.tres`, `.asset`, `.yaml` data files defining entity stats
- Look for scene/prefab files in character subdirectories

**Items / Equipment / Loot:**
- Find files matching `assets/data/**/items/**`, `assets/data/**/equipment/**`,
  `assets/data/**/loot/**`
- Look for `.json`, `.tres`, `.asset` data files

**Abilities / Skills / Spells:**
- Find files matching `assets/data/**/abilities/**`, `assets/data/**/skills/**`,
  `assets/data/**/spells/**`
- Look for `.json`, `.tres`, `.asset` data files

**Dialogue / Conversations / Cutscenes:**
- Find files matching `assets/**/*.dialogue`, `assets/**/*.csv`, `assets/**/*.ink`
- Include ordinary resources under `assets/audio/**`
- Search file contents for dialogue data files in `assets/data/`

**Quests / Missions:**
- Find files matching `assets/data/**/quests/**`, `assets/data/**/missions/**`
- Look for `.json`, `.yaml` definition files

**Engine-specific notes (acknowledge in the report):**
- Total-only counts are approximations — the skill cannot perfectly parse every
  engine format
- Exclude files whose directory semantics identify UI, tests, editor examples,
  or samples; do not count every scene match as a level

---

## Phase 3 — Gap Report

Produce the gap table:

```
| System | Content Type | Specified | Found | Gap | Status | Notes |
|--------|-------------|-----------|-------|-----|--------|-------|
```

For each identity that exists in the wrong explicit format, keep it in Found but
add `FORMAT ISSUE` to Notes with expected and actual formats. Format issues are
completeness gaps for the final verdict, distinct from missing names.

**Status categories (numeric rows only):**
- `COMPLETE` — Found ≥ Specified (100%+)
- `IN PROGRESS` — Found is 50–99% of Specified
- `EARLY` — Found is 1–49% of Specified
- `NOT STARTED` — Found is 0
- `UNSPECIFIED` — design names a content area but provides no count/list; this
  row is not assigned a numeric completion status and does not enter totals

**Priority flags:**
Flag a row as `HIGH PRIORITY` only when it has a real gap and:
- Status is `NOT STARTED` or `EARLY`; AND
- either the system is tagged MVP/Vertical Slice in the systems index, or the
  systems index shows the system blocks downstream systems.

A COMPLETE or UNSPECIFIED row is never HIGH PRIORITY merely because its system
has dependents.

**Summary line:**
- Exclude UNSPECIFIED rows from numeric sums.
- Total content items specified (sum of numeric Specified values)
- Total content items found (cap each row's contribution at its Specified value;
  report excess identities separately in Notes)
- Each numeric Gap is `max(0, Specified - Found)`.
- If total Specified is zero, output `Overall gap: not computable — no numeric
  specifications`; never divide by zero. Otherwise compute
  `sum(row gaps) / total Specified * 100`.

---

## Phase 4 — Output

### Full audit and single-system modes

Present the gap table and summary to the user without writing a file. If the
user explicitly chooses to save it, use the single existing path
`docs/content-audit-[date].md`, show that complete file operation/content in
one changeset preview, and write only after authorization:

```markdown
# Content Audit — [Date]

## Summary
- **Total specified**: [N] content items across [M] systems
- **Total found**: [N]
- **Gap**: [N] items ([X%] unimplemented)
- **Scope**: [Full audit | System: name]

> Note: Counts are approximations based on file scanning.
> The audit cannot distinguish shipped content from editor/test assets.
> Manual verification is recommended for any HIGH PRIORITY gaps.

## Gap Table

| System | Content Type | Specified | Found | Gap | Status |
|--------|-------------|-----------|-------|-----|--------|

## HIGH PRIORITY Gaps

[List systems flagged HIGH PRIORITY with rationale]

## Per-System Breakdown

### [System Name]
- **GDD**: `design/gdd/[file].md`
- **Content types audited**: [list]
- **Notes**: [any caveats about scan accuracy for this system]

## Recommendation

Focus implementation effort on:
1. [Highest-gap HIGH PRIORITY system]
2. [Second system]
3. [Third system]

## Unspecified Content Counts

The following GDDs describe content without giving explicit counts. These rows
remain auditable as qualitative design gaps but receive no numeric status.
Consider adding counts to improve auditability:
[List of GDDs and content types with "Unspecified"]
```

After writing the report, ask:

> "Would you like to create backlog stories for any of the content gaps?"

If yes: for each system the user selects, suggest a story title and point them
to `$create-stories [epic-slug]` or `$quick-design` depending on the size of the gap.

### --summary mode

Print the Gap Table and Summary directly to conversation. Do not write a file.
End with: "You can choose to save the full report to
`docs/content-audit-[date].md`."

---

## Phase 5 — Next Steps

After the audit, recommend the highest-value follow-up actions:

- If a content area is `UNSPECIFIED` → run `$design-system [name]` to define a
  count/list.
- If a numeric row is `NOT STARTED` and its specification already exists → point
  to the existing stories/planning path; do not ask design-system to add a count
  that is already present.
- If total gap is >50% → "Run `$sprint-plan` to allocate content work across upcoming sprints."
- If backlog stories are needed → "Run `$create-stories [epic-slug]` for each HIGH PRIORITY gap."
- If `--summary` was used → "Choose whether to save the full report to
  `docs/content-audit-[date].md`."

**Verdict (exactly one):**
- **MISSING CRITICAL CONTENT** — a missing/format-invalid item is explicitly
  critical in the GDD or blocks an MVP/Vertical Slice path.
- **GAPS FOUND** — any non-critical missing name, numeric gap, format issue, or
  UNSPECIFIED design gap exists.
- **COMPLETE** — every auditable named/numeric item is present in the required
  format and no UNSPECIFIED row remains.
