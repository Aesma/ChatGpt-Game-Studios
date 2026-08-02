---
name: scope-check
description: "Analyze a feature or sprint for scope creep by comparing current scope against the original plan. Flags additions, quantifies bloat, and recommends cuts. Use when user says 'any scope creep', 'scope review', 'are we staying in scope'."
---

## Invocation and execution

Invoke this workflow as `$scope-check`.

Arguments: `[feature-name or sprint-N]`. Treat bracketed values as optional unless the workflow says otherwise.


# Scope Check

This skill is read-only — it reports findings but writes no files.

Compare a selected baseline document with current story/goal/deliverable scope.
Code files, commits, and TODOs are supporting evidence only; they are never
counted as scope items.

---

## Phase 1: Resolve Target and Baseline

Accept a feature name, `sprint-N`, milestone name, or a project-contained story
path. With no argument, read existing active milestone/sprint references and
resolve the current sprint against that milestone. If there are multiple
candidates or no unique baseline, list the candidates and stop rather than guess.

- Feature: use an explicitly referenced or uniquely matching design/plan artifact.
- Sprint: use its exact sprint plan as the baseline.
- Milestone: use its exact milestone goals/deliverables.
- Story path: read the story and its explicitly referenced parent epic as baseline.

Label the result **selected baseline document at audit time**, and cite its path
and available date. A current GDD is not proof of the original historical scope.
If no earlier existing plan artifact is available, state that historical creep
cannot be proven and do not attribute when the change occurred.

---

## Phase 2: Build a Comparable Current Scope

Extract baseline items at one level: stories, goals, or deliverables. Build the
current set from existing artifacts at the same level. Use related source files,
commits, and TODO/FIXME references only as evidence that a particular item exists
or changed; never count them as additional scope items.

---

## Phase 3: Compare Item by Item

For each addition, locate an existing change record that documents either a
comparable cut or an explicit timeline extension. Report additions, removals,
and their mappings separately. Do not let the number of small removals cancel a
larger addition.

If comparable effort exists, report the evidence-backed effort delta. If it does
not, omit a percentage and state that item counts cannot establish bloat because
the items may differ in size.

```markdown
## Scope Check: [Target]
**Baseline at audit time**: [path and date]
**Historical limitation**: [earlier artifact path or cannot prove historical creep]

### Comparable Scope
| Item | Baseline | Current | Evidence |
|------|----------|---------|----------|
| [story/goal/deliverable] | [yes/no] | [yes/no] | [artifact path] |

### Additions
| Addition | Matching Cut / Timeline Extension | Evidence | Status |
|----------|-----------------------------------|----------|--------|
| [item] | [mapped item/extension or none] | [path] | [accounted/unmapped] |

### Removals
| Removal | Evidence |
|---------|----------|
| [item] | [path] |

### Quantification
[Comparable effort delta, or: percentage unavailable — comparable effort data absent]

### Risks and Recommendations
[Evidence-backed schedule, quality, and integration risks; user decision points]
```

---

## Phase 4: Verdict

- **PASS**: no unmapped additions are evidenced.
- **CONCERNS**: unmapped additions exist but their effort/impact is incomplete
  or plausibly manageable.
- **FAIL**: evidence shows one or more unmapped additions materially exceed the
  selected baseline without an equivalent cut or explicit timeline extension.

Do not derive a verdict from a net item-count percentage. Present descoped items
separately so they cannot mask additions.

---

## Phase 5: Handoff

Remain read-only. Cite the exact unresolved additions and the existing planning
artifact that would need a user-authorized update. Do not invoke a gate or write
a new baseline.
