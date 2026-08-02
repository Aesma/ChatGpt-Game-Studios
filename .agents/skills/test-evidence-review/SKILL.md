---
name: test-evidence-review
description: "Quality review of test files and manual evidence documents. Goes beyond existence checks — evaluates assertion coverage, edge case handling, naming conventions, and evidence completeness. Produces ADEQUATE/INCOMPLETE/MISSING verdict per story. Run before QA sign-off or on demand."
---

## Invocation and execution

Invoke this workflow as `$test-evidence-review`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[story-path | sprint | system-name]`. Treat bracketed values as optional unless the workflow says otherwise.


# Test Evidence Review

`$smoke-check` verifies that test files **exist** and **pass**. This skill
goes further — it reviews the **quality** of those tests and evidence documents.
A test file that exists and passes may still leave critical behaviour uncovered.
A manual evidence doc that exists may lack the sign-offs required for closure.

**Output:** Summary report (in conversation) + optional `production/qa/evidence-review-[date].md`

**When to run:**
- Before QA hand-off sign-off (`$team-qa` Phase 5)
- On any story where test quality is in question
- As part of milestone review for Logic and Integration story quality audit

---

## 1. Parse Arguments

**Modes:**
- `$test-evidence-review [story-path]` — review a single story's evidence
- `$test-evidence-review sprint` — review all stories in the current sprint
- `$test-evidence-review [system-name]` — review all stories in an epic/system
- No argument — ask which scope: "Single story", "Current sprint", "A system"

---

## 2. Load Stories in Scope

Based on the argument:

**Single story**: Read the story file directly. Extract: Story Type, Test
Evidence section, story slug, system name.

**Sprint**: Resolve the current sprint from an explicit active-state/sprint-status
identifier. If sources disagree or multiple sprint files match, list candidates
and ask the user; never select by modification time. Extract the story paths
explicitly listed by the chosen sprint plan and read each story file.

**System**: Prefer story paths explicitly listed by the relevant sprint/epic
documents. Use `production/epics/[system-name]/story-*.md` only as a fallback and
retain every unambiguous match rather than choosing one.

For each story, collect:
- `Type:` field (Logic / Integration / Visual/Feel / UI / Config/Data)
- `## Test Evidence` section — the stated expected test file path or evidence doc
- Story slug (from file name)
- System name (from directory path)
- Acceptance Criteria list (all checkbox items)

---

## 3. Locate Evidence Files

For each story, first validate every path explicitly declared in its `## Test Evidence` section. The path must stay inside the project and must exist. Only when no path is declared may the conventions below be used as fallbacks; label any fallback match as inferred rather than a confirmed story link.

Fallback conventions:

**Logic stories**: Find files matching `tests/unit/[system]/[story-slug]_test.*`
  - If not found, also try: Search in `tests/unit/[system]/` for files
    containing the story slug

**Integration stories**: Find files matching `tests/integration/[system]/[story-slug]_test.*`
  - Also check `production/session-logs/` for playtest records mentioning the story

**Visual/Feel and UI stories**: Find files matching `production/qa/evidence/[story-slug]-evidence.*`

**Config/Data stories**: A smoke report is evidence only when its body explicitly links the current story/system and the relevant acceptance criterion. An unrelated global smoke report is not evidence.

Note what was found (path) or not found (gap) for each story.

---

## 4. Review Automated Test Quality (Logic / Integration)

For each test file found, read it and evaluate:

Also inspect the current scope's existing execution result. ADEQUATE requires an identifiable current PASS for that test/evidence scope. If no current run result is available, record `execution status unknown` and cap the story at INCOMPLETE. This review does not add a test-execution phase and does not substitute for smoke or QA.

### Assertion coverage

Identify framework assertions inside actual test-function bodies; do not count
comments, helper definitions, or unrelated text containing assert/expect/check.
Recognize expected-exception and equivalent verification patterns as assertions.
Assertion count is secondary to acceptance-criterion coverage.

Thresholds:
- **3+ assertions per test function** → normal count signal
- **1-2 assertions per test function** → advisory only; one precise assertion may fully prove the criterion
- **0 assertions** (test exists but no asserts) → flag as BLOCKING — the
  test passes vacuously and proves nothing

### Edge case coverage

For each acceptance criterion in the story that contains a number, threshold,
or "when X happens" conditional: check whether a test function name or
test body references that specific case.

Map each criterion's concrete values, thresholds, and conditions to a local test
case/assertion. Keywords such as zero/max/null/empty/min/invalid only help locate
candidates and cannot by themselves prove coverage.

For formula traceability, read only the GDD directly linked by the story and its
relevant Formulas/acceptance-criteria section. If the story has no direct GDD link,
record `formula traceability unknown`; do not scan all GDDs or invent a source.

### Naming quality

Test function names should describe: the scenario + the expected result.
Pattern: `test_[scenario]_[expected_outcome]`

Flag functions named generically (`test_1`, `test_run`, `testBasic`) as
**naming issues** — they make failures harder to diagnose.

### Coding-standard quality

Apply the existing coding-standard checks for deterministic behavior, isolation from live external systems/state, and absence of unexplained hardcoded test data in addition to naming. These findings participate in the same story-level quality verdict; they do not introduce a test-path mode or a second verdict vocabulary.

### Formula traceability

For Logic stories where the GDD has a Formulas section: check that the test
file contains at least one test whose name or comment references the formula
name or a formula value. A test that exercises a formula without mentioning
it by name is harder to maintain when the formula changes.

---

## 5. Review Manual Evidence Quality (Visual/Feel / UI)

For each evidence document found, read it and evaluate:

### Criterion linkage

The evidence doc should reference each acceptance criterion from the story.
Check: does the evidence doc contain each criterion (or a clear rephrasing)?
Missing criteria mean a criterion was never verified.

### Sign-off completeness

Apply the existing story-type contract rather than requiring three universal
signatures. Visual/Feel requires screenshot evidence plus the applicable lead
sign-off. UI requires a documented walkthrough or interaction test. Check only
roles required by that evidence type; a non-applicable signature is N/A.

### Screenshot / artefact completeness

For Visual/Feel stories: check whether screenshot file paths are referenced
in the evidence doc. If referenced, search those paths to confirm they exist.

For UI stories: check whether a walkthrough sequence (step-by-step interaction
log) is present.

### Date coverage

Evidence doc should have a date. Compare freshness only with an existing story or
evidence `Last Updated` value that directly represents the last major change. If
that value is absent, report `freshness unknown`; do not substitute sprint start,
file mtime, or another inferred date.

For an Integration story whose declared evidence is a documented playtest, review
criterion linkage, date, and concrete observations. Assertion-count/naming rules
are N/A for that evidence and must not be forced onto it.

---

## 6. Build the Review Report

For each story, assign a verdict:

| Verdict | Meaning |
|---------|---------|
| **ADEQUATE** | Static test/evidence quality is sufficient, all criteria are covered, and a current scope pass result is identifiable |
| **INCOMPLETE** | Test/evidence exists but has quality gaps (thin assertions, missing sign-offs) |
| **MISSING** | No test or evidence found for a story type that requires it |

The overall sprint/system verdict is the worst story verdict present. COMPLETE
means only that the review ran. If any story is MISSING or has a genuine BLOCKING
gap, keep the three-level overall verdict and describe workflow status as
CONCERNS; do not introduce a fourth evidence verdict.

```markdown
## Test Evidence Review

> **Date**: [date]
> **Scope**: [single story path | Sprint [N] | [system name]]
> **Stories reviewed**: [N]
> **Overall verdict**: ADEQUATE / INCOMPLETE / MISSING

---

### Story-by-Story Results

#### [Story Title] — [Type] — [ADEQUATE/INCOMPLETE/MISSING]

**Test/evidence path**: `[path]` (found) / (not found)

**Automated test quality** *(Logic/Integration only)*:
- Assertion coverage: [N per function on average] — [adequate / thin / none]
- Edge cases: [covered / partial / not found]
- Naming: [consistent / [N] generic names flagged]
- Formula traceability: [yes / no — formula names not referenced in tests]

**Manual evidence quality** *(Visual/Feel/UI only)*:
- Criterion linkage: [N/M criteria referenced]
- Sign-offs: [Developer ✓ | Designer ✗ | QA Lead ✗]
- Artefacts: [screenshots present / missing / N/A]
- Freshness: [dated [date] — current / potentially stale]

**Issues**:
- BLOCKING: [description] *(prevents story-done)*
- ADVISORY: [description] *(should fix before release)*

---

### Summary

| Story | Type | Verdict | Issues |
|-------|------|---------|--------|
| [title] | Logic | ADEQUATE | None |
| [title] | Integration | INCOMPLETE | Thin assertions (avg 1.2/function) |
| [title] | Visual/Feel | INCOMPLETE | QA lead sign-off missing |
| [title] | Logic | MISSING | No test file found |

**BLOCKING items** (must resolve before story can be closed): [N]
**ADVISORY items** (should address before release): [N]
```

---

## 7. Write Output (Optional)

Present the report in conversation.

Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.

This is optional — the report is useful standalone. Write only if the user
wants a persistent record.

After the report:

- For BLOCKING items: "These must be resolved before `$story-done` can mark the
  story Complete. Would you like to address any of them now?"
- For thin assertions: "Consider running `$test-helpers [system]` to see
  scaffolded assertion patterns for common cases."
- For missing sign-offs: "Manual sign-off is required from [role]. Share
  `[evidence-path]` with them to complete sign-off."

Verdict: **COMPLETE** — evidence review finished. Use CONCERNS if BLOCKING items were found.

---

## Collaborative Protocol

- **Report quality issues, do not fix them** — this skill reads and evaluates;
  it does not modify test files or evidence documents
- **ADEQUATE means static evidence quality is sufficient for this review, not release approval**. Missing current execution results cap the story at INCOMPLETE.
- **BLOCKING vs. ADVISORY distinction is important** — only flag BLOCKING when
  the gap leaves a story criterion genuinely unverified
- **Single changeset approval** — the report file is optional; when requested, include it in the complete preview and write it only after the one approval
