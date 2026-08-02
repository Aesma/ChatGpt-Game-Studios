---
name: consistency-check
description: "Scan all GDDs against the entity registry to detect cross-document inconsistencies: same entity with different stats, same item with different values, same formula with different variables. Search-first approach — reads registry then targets only conflicting GDD sections rather than full document reads."
---

## Invocation and execution

Invoke this workflow as `$consistency-check`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[full | since-last-review | entity:<name> | item:<name>]`. Treat bracketed values as optional unless the workflow says otherwise.


# Consistency Check

Detects cross-document inconsistencies by comparing all GDDs against the
entity registry (`design/registry/entities.yaml`). Uses a search-first approach:
reads the registry once, then targets only the GDD sections that mention
registered names — no full document reads unless a conflict needs investigation.

**This skill is the write-time safety net.** It catches what `$design-system`'s
per-section checks may have missed and what `$review-all-gdds`'s holistic review
catches too late.

**When to run:**
- After writing each new GDD (before moving to the next system)
- Before `$review-all-gdds` (so that skill starts with a clean baseline)
- Before `$create-architecture` (inconsistencies poison downstream ADRs)
- On demand: `$consistency-check entity:[name]` to check one entity specifically

**Output:** Read-only conflict report. An optional saved copy uses
`design/consistency-report-[date].md` and is written only after the user approves
the complete changeset preview.

---

## Phase 1: Parse Arguments and Load Registry

**Modes:**
- No argument / `full` — check all registered entries against all GDDs
- `since-last-review` — check only GDDs modified since the last review report
- `entity:<name>` — check one specific entity across all GDDs
- `item:<name>` — check one specific item across all GDDs

**Load the registry:**

```
Read `design/registry/entities.yaml` in full.
```

If the file does not exist or has no entries, report that registry comparisons
are unavailable, initialize the four lookup tables as empty, and continue with
the cross-GDD formula, ownership, and dependency checks in Phase 3. Registry
absence is not a reason to skip GDD consistency analysis.

Build four lookup tables from the registry:
- **entity_map**: `{ name → { source, attributes, referenced_by } }`
- **item_map**: `{ name → { source, value_gold, weight, ... } }`
- **formula_map**: `{ name → { source, variables, output_range } }`
- **constant_map**: `{ name → { source, value, unit } }`

Count total registered entries. Report:
```
Registry loaded: [N] entities, [N] items, [N] formulas, [N] constants
Scope: [full | since-last-review | entity:name]
```

---

## Phase 2: Locate In-Scope GDDs

```
Search for files matching `design/gdd/*.md`.
```

Exclude: `game-concept.md`, `systems-index.md`, `game-pillars.md` — these are
not system GDDs.

For `since-last-review` mode:
Find the most recent `design/gdd/gdd-cross-review-*.md`, then use the commit in
which that file first appeared in Git history as the comparison anchor. Include
both committed changes after that anchor and current working-tree modifications.
If the review file has no discoverable first commit, no review exists, or the
repository has no usable Git history, state that incremental scope cannot be
proved and downgrade to `full`. Never infer a file creation date from the
filesystem or return an incremental PASS from an unanchored scan.

If no in-scope system GDD exists, stop with a clear error. Do not produce a
verdict and do not write a report.

Report the in-scope GDD list before scanning.

---

## Phase 3: Search-First Conflict Scan

For every in-scope GDD, first read its Summary or Overview, Dependencies,
Formulas, and the sections that declare entity/system ownership. This baseline
scan is mandatory even when the registry is empty and must check all four
existing consistency classes: registry values (when available), formulas,
ownership, and dependency targets. Search-first remains an optimization for
locating registered names; it must not exclude unregistered formulas, competing
owners, or missing explicit dependencies.

For each registered entry, search every in-scope GDD for the literal escaped
entry name. On a hit, read the complete containing Markdown section so that
table headers, units, formulas, and values remain together; three context lines
are not sufficient evidence. Expand beyond these sections only when a possible
conflict needs investigation.

### 3a: Entity Scan

For each entity in entity_map:

```
Search files matching `design/gdd/*.md` for `[entity_name]` and include 3 surrounding lines of context.
```

For each GDD hit, extract the values mentioned near the entity name:
- any numeric attributes (counts, costs, durations, ranges, rates)
- any categorical attributes (types, tiers, categories)
- any derived values (totals, outputs, results)
- any other attributes registered in entity_map

Compare extracted values against the registry entry.

**Conflict detection:**
- Registry says `[entity_name].[attribute] = [value_A]`. GDD says `[entity_name] has [value_B]`. → **CONFLICT**
- Registry says `[item_name].[attribute] = [value_A]`. GDD says `[item_name] is [value_B]`. → **CONFLICT**
- GDD mentions `[entity_name]` but doesn't specify the attribute. → **NOTE** (no conflict, just unverifiable)

### 3b: Item Scan

For each item in item_map, search all GDDs for the item name. Extract:
- sell price / value / gold value
- weight
- stack rules (stackable / non-stackable)
- category

Compare against registry entry values.

### 3c: Formula Scan

For each formula in formula_map, search all GDDs for the formula name. Extract:
- variable names mentioned near the formula
- output range or cap values mentioned

Compare against registry entry:
- Different variable names → **CONFLICT**
- Output range stated differently → **CONFLICT**

### 3d: Constant Scan

For each constant in constant_map, search all GDDs for the constant name. Extract:
- Any numeric value mentioned near the constant name

Compare against registry value:
- Different number → **CONFLICT**

---

## Phase 4: Deep Investigation (Conflicts Only)

For each conflict found in Phase 3, do a targeted full-section read of the
conflicting GDD to get precise context:

```
Read the complete conflicting section in `design/gdd/[conflicting_gdd].md`.
```
(Or search with wider context if the file is large)

Confirm the conflict with full context. Determine:
1. **Which GDD is correct?** Check the `source:` field in the registry — the
   source GDD is the authoritative owner. Any other GDD that contradicts it
   is the one that needs updating.
2. **Is the registry itself out of date?** If the source GDD was updated after
   the registry entry was written (check git log), the registry may be stale.
3. **Is this a genuine design change?** If the conflict represents an intentional
   design decision, the resolution is: update the source GDD, update the registry,
   then fix all other GDDs.

For each conflict, classify:
- **🔴 CONFLICT** — same named entity/item/formula/constant with different values
  in different GDDs. Must resolve before architecture begins.
- **⚠️ STALE REGISTRY** — source GDD value changed but registry not updated.
  Registry needs updating; other GDDs may be correct already.
- **ℹ️ UNVERIFIABLE** — entity mentioned but no comparable attribute stated.
  Not a conflict; just noting the reference.

---

## Phase 5: Output Report

```
## Consistency Check Report
Date: [date]
Registry entries checked: [N entities, N items, N formulas, N constants]
GDDs scanned: [N] ([list names])

---

### Conflicts Found (must resolve before architecture)

🔴 [Entity/Item/Formula/Constant Name]
   Registry (source: [gdd]): [attribute] = [value]
   Conflict in [other_gdd].md: [attribute] = [different_value]
   → Resolution needed: [which doc to change and to what]

---

### Stale Registry Entries (registry behind the GDD)

⚠️ [Entry Name]
   Registry says: [value] (written [date])
   Source GDD now says: [new value]
   → Update registry entry to match source GDD, then check referenced_by docs.

---

### Unverifiable References (no conflict, informational)

ℹ️ [gdd].md mentions [entity_name] but states no comparable attributes.
   No conflict detected. No action required.

---

### Clean Entries (no issues found)

✅ [N] registry entries verified across all GDDs with no conflicts.

---

Verdict: PASS | CONFLICTS FOUND
```

**Verdict:**
- **PASS** — no conflicts. Registry and GDDs agree on all checked values.
- **CONFLICTS FOUND** — one or more conflicts detected. List resolution steps.

---

## Phase 6: Suggested Corrections and Optional Report

Remain read-only. List each proposed GDD or registry correction, its evidence,
and the exact existing field or section that would need a later edit. Do not
update the registry, create a failure log, or write session state.

Offer to save the report only as `design/consistency-report-[date].md`. Before
writing it, show the complete file content/operation in one changeset preview
and obtain explicit authorization. If the report is not actually written, do
not cite that path as an artifact.

## Phase 7: Closing

Do not append to `production/session-state/active.md` and do not claim a report
file exists unless Phase 6 saved it successfully.

Then close with an a structured choice prompt:

- **Prompt**: "Consistency check complete — [N] conflicts found. What next?"
- **Options**:
  - `[A] Fix the highest-priority conflict now`
  - `[B] Save full report and stop`
  - `[C] Run $design-review on the most conflicted GDD`
  - `[D] Stop here`

Never end the skill with plain text. Always close with this structured prompt.

---

## Recovery / Reference

- **If PASS**: Run `$review-all-gdds` for holistic design-theory review, or
  `$create-architecture` if all MVP GDDs are complete.
- **If CONFLICTS FOUND**: Fix the flagged GDDs, then re-run
  `$consistency-check` to confirm resolution.
- **If STALE REGISTRY**: Use the report's proposed correction in a separate
  explicitly authorized edit, then re-run to verify.
- Run `$consistency-check` after writing each new GDD to catch issues early,
  not at architecture time.
