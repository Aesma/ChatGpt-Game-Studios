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

If the argument is not exactly one of `scan`, `add`, `prioritize`, or `report`,
output the same usage and stop with **FAIL**. Do not treat unknown or extra
arguments as scan/report. All four modes use only `docs/tech-debt-register.md`.
If it is absent, scan/add may propose creating that existing register format in
their changeset; prioritize/report stop with a clear missing-register error and
do not output COMPLETE.

---

## Phase 2A: Scan Mode

Search only project-owned source, configuration, and test files. Exclude vendored
dependencies, generated files, build/cache/output directories, and this workflow's
own documentation. Search for debt indicators:

- `TODO` comments (count and categorize)
- `FIXME` comments (candidates that may be bugs rather than accepted debt)
- `HACK` comments (workarounds that need proper solutions)
- `@deprecated` markers
- Duplicated code blocks (similar patterns in multiple files)
- Files over 500 lines (candidate only)
- Functions over 50 lines (candidate only)

Length, duplication, and marker matches are discovery signals, not automatic debt.
Before registration, state the concrete impact. A FIXME enters the register only
when the user confirms it is consciously deferred/accepted work and supplies WHY;
otherwise leave it as an unregistered bug/candidate.

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

Ask the user for the description, affected files, impact if left unfixed, and WHY
the debt is consciously accepted (deadline, prototype, missing information, or
another explicit reason). Normalize Impact to exactly Low, Med, High, or Critical.

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

Derive the next unused ID from the current register, use the current date, set the
existing Sprint column to Backlog unless the user provides an existing sprint, and
calculate Priority by the Phase 2C Impact/Effort/ID rule. Present the complete new
entry to the user. Immediately before append, re-read the table; if the candidate
ID is now occupied, select the next unused ID rather than overwriting a row.

Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.

Once the complete changeset is authorized, append the entry. Verdict: **COMPLETE** — entry added to register.

If the complete changeset is not authorized, stop here. Verdict: **BLOCKED** — changeset not authorized.

---

## Phase 2C: Prioritize Mode

Read the debt register at `docs/tech-debt-register.md`.

Use only the fields already present in the register. Sort deterministically by Impact (`Critical` > `High` > `Med` > `Low`), then by lower Effort (`S` < `M` < `L` < `XL`), then by ID ascending. Update the existing Priority cells to reflect that ordering; do not invent frequency values, numeric mappings, or new fields.

Re-sort only the existing table rows by this rule and recommend which items to include in the next sprint. Preserve every non-table paragraph, heading, comment, unknown column, and hand-written note except the existing header statistics that this mode explicitly updates.

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
Total items: [N] | Effort distribution: S [N] / M [N] / L [N] / XL [N]

| ID | Category | Description | Files | Effort | Impact | Priority | Added | Sprint |
|----|----------|-------------|-------|--------|--------|----------|-------|--------|
| TD-001 | [Cat] | [Description] | [files] | [S/M/L/XL] | [Low/Med/High/Critical] | [Score] | [Date] | [Sprint to fix or "Backlog"] |
```

### Rules
- Tech debt is not inherently bad — it is a tool. The register tracks conscious decisions.
- Every debt entry must explain WHY it was accepted (deadline, prototype, missing info)
- "Scan" should run at least once per sprint to catch new debt
- Only rows with an existing, directly comparable sprint number can receive an "older than 3 sprints" hint. For date-only/Backlog/ambiguous values, report `age unknown` rather than guessing.
