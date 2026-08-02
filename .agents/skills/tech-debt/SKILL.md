---
name: tech-debt
description: "Track, categorize, and prioritize technical debt across the codebase. Scans for debt indicators, maintains a debt register, and recommends repayment scheduling."
---

## Invocation and execution

Invoke this workflow as `$tech-debt`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[scan|add|prioritize|report]`. Treat bracketed values as optional unless the workflow says otherwise.


## Phase 1: Parse Subcommand

Determine the mode from the argument:

- `scan` — Scan the codebase for tech debt indicators
- `add` — Add a new tech debt entry manually
- `prioritize` — Re-prioritize the existing debt register
- `report` — Generate a summary report of current debt status

If no subcommand is provided, output usage and stop. Verdict: **FAIL** — missing required subcommand.

---

## Phase 2A: Scan Mode

Search the codebase for debt indicators:

- `TODO` comments (count and categorize)
- `FIXME` comments (these are bugs disguised as debt)
- `HACK` comments (workarounds that need proper solutions)
- `@deprecated` markers
- Duplicated code blocks (similar patterns in multiple files)
- Files over 500 lines (potential god objects)
- Functions over 50 lines (potential complexity)

Categorize each finding:

- **Architecture Debt**: Wrong abstractions, missing patterns, coupling issues
- **Code Quality Debt**: Duplication, complexity, naming, missing types
- **Test Debt**: Missing tests, flaky tests, untested edge cases
- **Documentation Debt**: Missing docs, outdated docs, undocumented APIs
- **Dependency Debt**: Outdated packages, deprecated APIs, version conflicts
- **Performance Debt**: Known slow paths, unoptimized queries, memory issues

Present the findings to the user.

Before appending, compare every candidate with `docs/tech-debt-register.md` by affected Files plus Description and, for code markers, the recorded marker location. If the same debt is already registered, report `already registered` in the session and do not append another TD row. If the original marker text or location changed, report that its state cannot be confirmed; do not infer resolution or create a replacement row automatically.

Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.

Once the complete changeset is authorized, update the register (append new entries, do not overwrite existing ones). Verdict: **COMPLETE** — scan findings written to register.

If the complete changeset is not authorized, stop here. Verdict: **BLOCKED** — changeset not authorized.

---

## Phase 2B: Add Mode

Ask the user for the description, affected files, and impact if left unfixed (plain text prompts).

Then ask the user directly to collect the **category**:
- Prompt: "What category does this tech debt belong to?"
- Options:
  - `[A] Architecture Debt — wrong abstractions, missing patterns, coupling issues`
  - `[B] Code Quality Debt — duplication, complexity, naming, missing types`
  - `[C] Test Debt — missing tests, flaky tests, untested edge cases`
  - `[D] Documentation Debt — missing/outdated docs, undocumented APIs`
  - `[E] Dependency Debt — outdated packages, deprecated APIs, version conflicts`
  - `[F] Performance Debt — known slow paths, memory issues, unoptimized queries`

Then ask the user directly to collect the **estimated fix effort**:
- Prompt: "What is the estimated effort to fix this item?"
- Options:
  - `[A] S — Small (under 1 day)`
  - `[B] M — Medium (1–3 days)`
  - `[C] L — Large (3–7 days)`
  - `[D] XL — Extra Large (over 1 week)`

Present the complete new entry to the user.

Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.

Once the complete changeset is authorized, append the entry. Verdict: **COMPLETE** — entry added to register.

If the complete changeset is not authorized, stop here. Verdict: **BLOCKED** — changeset not authorized.

---

## Phase 2C: Prioritize Mode

Read the debt register at `docs/tech-debt-register.md`.

Use only the fields already present in the register. Sort deterministically by Impact (`Critical` > `High` > `Med` > `Low`), then by lower Effort (`S` < `M` < `L` < `XL`), then by ID ascending. Update the existing Priority cells to reflect that ordering; do not invent frequency values, numeric mappings, or new fields.

Re-sort only the existing table rows by this rule and recommend which items to include in the next sprint.

Present the re-prioritized register to the user.

Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.

Once the complete changeset is authorized, write the updated file. Verdict: **COMPLETE** — register re-prioritized and saved.

If the complete changeset is not authorized, stop here. Verdict: **BLOCKED** — changeset not authorized.

---

## Phase 2D: Report Mode

Read the debt register. Generate only statistics directly supported by its current columns:

- Total items by category
- Effort distribution (counts of S/M/L/XL)
- Impact distribution
- Count assigned to Backlog versus an explicitly named sprint
- Age hints only where Added/Sprint values are directly comparable

The register has no resolution status or prior-report baseline. Do not claim items-resolved counts or a growing/stable/shrinking trend. If age cannot be established from existing values, state `age unknown` rather than guessing.

Output the report to the user. This mode is read-only — no files are written. Verdict: **COMPLETE** — debt report generated.

---

## Phase 3: Next Steps

- Run `$sprint-plan` to schedule high-priority debt items into the next sprint.
- Run `$tech-debt report` at the start of each sprint to track debt trends over time.

### Debt Register Format

```markdown
## Technical Debt Register
Last updated: [Date]
Total items: [N] | Estimated total effort: [T-shirt sizes summed]

| ID | Category | Description | Files | Effort | Impact | Priority | Added | Sprint |
|----|----------|-------------|-------|--------|--------|----------|-------|--------|
| TD-001 | [Cat] | [Description] | [files] | [S/M/L/XL] | [Low/Med/High/Critical] | [Score] | [Date] | [Sprint to fix or "Backlog"] |
```

### Rules
- Tech debt is not inherently bad — it is a tool. The register tracks conscious decisions.
- Every debt entry must explain WHY it was accepted (deadline, prototype, missing info)
- "Scan" should run at least once per sprint to catch new debt
- Items older than 3 sprints without action should either be fixed or consciously accepted with a documented reason
