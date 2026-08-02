---
name: propagate-design-change
description: "When a GDD is revised, scans all ADRs and the traceability index to identify which architectural decisions are now potentially stale. Produces a change impact report and guides the user through resolution."
---

## Invocation and execution

Invoke this workflow as `$propagate-design-change`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[path/to/changed-gdd.md]`. Treat bracketed values as optional unless the workflow says otherwise.

Delegate substantive work to the `technical-director` Codex subagent role when it is available. If that role is unavailable, follow the same responsibilities in the current agent.


# Propagate Design Change

When a GDD changes, architectural decisions written against it may no longer be
valid. This skill finds every affected ADR, compares what the ADR assumed against
what the GDD now says, and guides the user through resolution.

**Usage:** `$propagate-design-change design/gdd/combat-system.md`

---

## 1. Validate Argument

A GDD path argument is **required**. If missing, fail with:
> "Usage: `$propagate-design-change design/gdd/[system].md`
> Provide the path to the GDD that was changed."

Verify the file exists. If not, fail with:
> "[path] not found. Check the path and try again."

---

## 2. Read the Changed GDD

Read the current GDD in full.

---

## 3. Read the Previous Version

Resolve the target project-relative path and inspect its Git status first.

- If the working tree contains changes to the target, compare `HEAD:[path]` with the working-tree file.
- If the target is clean and its change is already committed, find the most recent commit that modified that path and compare that commit's parent version with the version in that commit.
- If two versions cannot be recovered, report **no comparison baseline** and stop change/impact classification. This is not NO IMPACT and must not be described as nothing to propagate.

With the two verified versions, do a conceptual diff:
- Identify sections that changed (new rules, removed rules, modified formulas,
  changed acceptance criteria, changed tuning knobs)
- Identify sections that are unchanged
- Produce a change summary:

```
## Change Summary: [GDD filename]
Date of revision: [today]

Changed sections:
- [Section name]: [what changed — new rule, removed rule, formula modified, etc.]

Unchanged sections:
- [Section name]

Key changes affecting architecture:
- [Change 1 — likely to affect ADRs]
- [Change 2]
```

---

## 4. Load Architecture Inputs

Read all ADRs in `docs/architecture/`:
- For each ADR, read the full file
- Extract the "GDD Requirements Addressed" table
- Note which GDD documents and requirement IDs each ADR references

Read `docs/architecture/architecture-traceability.md` and any existing TR registry if present. Also scan existing epic and story files for explicit references to the exact GDD path or requirement IDs from that GDD. Do not use fuzzy semantic matching.

Report counts by ADR, traceability/TR entry, epic, and story.

---

## 5. Impact Analysis

For each ADR that references the changed GDD:

Compare the ADR's "GDD Requirements Addressed" entries against the changed sections
of the GDD. For each referenced requirement:

1. **Locate the requirement** in the current GDD — does it still exist?
2. **Compare**: What did the GDD say when the ADR was written vs. what it says now?
3. **Assess the ADR decision**: Is the architectural decision still valid?

Classify each affected ADR as one of:

| Status | Meaning |
|--------|---------|
| ✅ **Still Valid** | The GDD change doesn't affect what this ADR decided |
| ⚠️ **Needs Review** | The GDD change may affect this ADR — human judgment needed |
| 🔴 **Likely Superseded** | The GDD change directly contradicts what this ADR assumed |

For each affected ADR, produce an impact entry:

```
### ADR-NNNN: [title]
Status: [Still Valid / Needs Review / Likely Superseded]

What the ADR recorded about this GDD:
  [Quote only text actually stored in the ADR. If it stores only an ID/summary, show that and state that the historical requirement wording cannot be recovered from the ADR.]

What the GDD now says:
  "[relevant quote from the current GDD]"

Assessment:
  [Explanation of whether the ADR decision is still valid, and why]

Recommended action:
  [Keep as-is | Review and update | Mark Superseded and write new ADR]
```

---

## 6. Present Impact Report

Present the full impact report to the user before asking for any action. Format:

```
## Design Change Impact Report
GDD: [filename]
Date: [today]
Changes detected: [N sections changed]
ADRs referencing this GDD: [M]

### Not Affected
[ADRs referencing this GDD whose decisions remain valid]

### Needs Review ([count])
[ADRs that may need updating]

### Likely Superseded ([count])
[ADRs whose assumptions are now contradicted]
```

---

## 6b. Technical Review Boundary

This workflow reads no review mode and invokes no director gate. The optional `technical-director` delegation named at the top may help perform the same analysis, but it supplies no gate ID or gate verdict.

---

## 7. Resolution Workflow

For each ADR marked "Needs Review" or "Likely Superseded", ask the user what to do:

Ask for each ADR in turn:
> "ADR-NNNN ([title]) — [status]. What would you like to do?"
> Options:
> - "Plan a replacement ADR" — record in the impact report that the user chose supersede and that the replacement has not been created; do not edit the original ADR's Superseded-by field yet
> - "Update in place (minor revision)" — opens the ADR for editing; note what to revise
> - "Keep as-is (the change doesn't actually affect this decision)"
> - "Skip for now (revisit later)"

For a supersede decision, do not pre-allocate an ADR number and do not create a pending `Superseded by` link. Record only the user's decision in the impact report. The original ADR may receive a real replacement reference only after `$architecture-decision` actually creates that ADR.

---

## 8. Update Traceability Index

If `docs/architecture/architecture-traceability.md` exists:
- Add the changed GDD requirements to the "Superseded Requirements" table:

```markdown
## Superseded Requirements
| Date | GDD | Requirement | Changed To | ADRs Affected | Resolution |
|------|-----|-------------|------------|---------------|------------|
| [date] | [gdd] | [old requirement text] | [new requirement text] | ADR-NNNN | [Superseded/Updated/Valid] |
```

Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.

---

## 9. Output Change Impact Document

After all per-artifact decisions, resolve one report path: `production/change-impact-[date]-[system].md`. Build one complete changeset containing that report and only the ADR, traceability/TR, epic, and story files that the user actually chose to edit. Preview the exact paths and modifications once, then write only after authorization. If the final result requires no file edit and the user does not want the report saved, finish read-only without requesting authorization. Any write failure prevents COMPLETE.

The document contains:
- The change summary from step 3
- The full impact analysis from step 5
- Resolution decisions made in step 7
- List of ADRs that need to be written or updated

If user approved: Verdict: **COMPLETE** — change impact report saved.
If user declined: Verdict: **BLOCKED** — user declined write.

---

## 10. Follow-Up Actions

Based on the resolution decisions, suggest:

- **ADRs marked Superseded**: "Run `$architecture-decision [title]` to write the
  replacement ADR. Then re-run `$propagate-design-change` to verify coverage."
- **ADRs to update in place**: List the specific fields to update in each ADR
- **If many ADRs affected**: "Run `$architecture-review` after all ADRs are updated
  to verify the full traceability matrix is still coherent."

---

## Collaborative Protocol

1. **Read silently** — compute the full impact before presenting anything
2. **Show the full report first** — let the user see the scope before asking for action
3. **Ask per-ADR** — don't batch decisions; each affected ADR may need different treatment
4. **Single changeset approval** — preview every affected file together and modify them only after the one approval
5. **Non-destructive** — never delete ADR content; only add "Superseded by" notes
