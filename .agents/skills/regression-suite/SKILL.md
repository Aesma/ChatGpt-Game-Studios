---
name: regression-suite
description: "Map test coverage to GDD critical paths, identify fixed bugs without regression tests, flag coverage drift from new features, and maintain tests/regression-suite.md. Run after implementing a bug fix or before a release gate."
---

## Invocation and execution

Invoke this workflow as `$regression-suite`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[update | audit | report]`. Treat bracketed values as optional unless the workflow says otherwise.


# Regression Suite

This skill ensures that every bug fix is backed by a test that would have
caught the original bug — and that the regression suite stays current as the
game evolves. It also detects when new features have been added without
corresponding regression coverage.

A regression suite is not a new test category — it is a **curated list of
tests already in `tests/`** that collectively cover the game's critical paths
and known failure points. This skill maintains that list.

**Output:** `tests/regression-suite.md`

**When to run:**
- After fixing a bug (confirm a regression test was written or identify gap)
- Before a release gate (`$gate-check polish` requires regression suite exists)
- As part of sprint close to detect coverage drift

---

## 1. Parse Arguments

**Modes:**
- `$regression-suite update` — scan new bug fixes this sprint, register existing
  matching tests in the manifest, and record missing-test gaps; it does not
  create test files
- `$regression-suite audit` — full audit of all GDD critical paths vs.
  existing test coverage; flag paths with no regression test
- `$regression-suite report` — read-only status report (no writes); suitable
  for sprint reviews
- No argument — if a sprint is clearly active (sprint plan exists with in-progress stories), run `update`. If ambiguous or no active sprint is detected, ask the user directly:
  - Prompt: "No subcommand specified. Which mode do you want to run?"
  - Options:
    - `[A] update — register existing tests for this sprint and record missing-test gaps`
    - `[B] audit — full audit of all GDD critical paths vs. existing test coverage`
    - `[C] report — read-only status report (no writes)`

Reject any other mode. Resolve the current sprint explicitly for `update`.

---

## 2. Load Context

### Step 2a — Load existing regression suite

Read `tests/regression-suite.md` if it exists. Extract:
- Total registered regression tests
- Last updated date
- Any tests flagged as `STALE` or `QUARANTINED`

If it does not exist: in `report` mode note "No regression suite found" and
continue read-only; in `update` or `audit` mode note that creation is a proposed
write which still requires authorization.

### Step 2b — Load test inventory

Find all test files:
```
tests/unit/**/*_test.*
tests/integration/**/*_test.*
tests/regression/**/*
```

For each file, note the system and filename. A name match only identifies a
candidate; read each relevant test function and its assertions before assigning
coverage. Compare every existing manifest entry to the inventory. If its file
or function is missing or renamed without an unambiguous replacement, retain
the row but mark it `STALE`; exclude it from valid coverage totals.

### Step 2c — Load GDD critical paths

For `audit` mode: read `design/gdd/systems-index.md` to get all systems.
For each MVP-tier system, read its GDD and extract:
- Acceptance Criteria (these define the critical paths)
- Formulas section (formulas must have regression tests)
- Edge Cases section (known edge cases should have regression tests)

For `update` mode: skip full GDD scan. Instead read the current sprint plan
and story files to find stories with Status: Complete this sprint.

### Step 2d — Load closed bugs

Find files matching `production/qa/bugs/*.md` and filter for bugs with a `Status: Closed`
or `Status: Fixed` field. Note the system and whether the fix cites a regression test.

### Step 2e — Load project test command

Read `docs/technical-preferences.md` and existing project CI configuration for
the selected engine/framework command. If no command is configured, write
`Unavailable — project test command not configured`; do not guess one.

### Step 2f — Validate auditable scope

Report missing input collections separately. If the selected mode has no test
inventory and no applicable GDD criteria, completed stories, or closed bugs,
there is no auditable scope: report the gaps, do not calculate a percentage,
and do not create an empty manifest. An empty test inventory alongside real
criteria/bugs is still auditable and yields MISSING coverage rather than a fake
zero-input percentage.

---

## 3. Map Coverage — Critical Paths

For `audit` mode only:

For each GDD acceptance criterion, determine whether a test exists:

1. Search `tests/unit/[system]/` and `tests/integration/[system]/` for candidate
   file/function names, then read the relevant test functions.
2. Match the criterion's scenario and expected result to a concrete assertion.
3. Assign coverage:

| Status | Meaning |
|--------|---------|
| **COVERED** | A relevant assertion verifies the criterion's scenario and expected result |
| **PARTIAL** | A candidate exists but lacks the matching assertion or covers only part of the scenario |
| **MISSING** | No test found for this critical path |
| **EXEMPT** | The criterion is explicitly non-automatable under the Testing Standards |

Do not exempt all UI criteria. A UI criterion with an existing interaction test
is mapped like any other automated criterion. Visual/Feel or UI is EXEMPT only
when its specific observable outcome cannot be automated under the standards.

Elevate MISSING items that correspond to formulas or state machines to
**HIGH PRIORITY** gap.

---

## 4. Map Coverage — Fixed Bugs

For each closed bug:

1. Extract the system slug from the bug's metadata.
2. Search unit/integration tests for a test that references the bug ID or its
   specific failure scenario, then verify the matching assertion.
3. Assign `HAS REGRESSION TEST` or `MISSING REGRESSION TEST`.

For a missing test, record the gap and suggested file path. Do not create the
test or claim update mode adds it.

---

## 5. Detect Coverage Drift

Use only current sprint artifacts that explicitly list changed/completed stories
and systems, plus existing sprint/retrospective identifiers that establish a
comparable prior suite update. Evaluate:

- current sprint completed stories with no corresponding test assertions;
- systems explicitly added by a current sprint change record;
- GDD sections explicitly listed as revised in a current change record;
- a suite update tied to an earlier named sprint/retrospective.

Do not infer drift from filesystem modification times, an arbitrary date gap,
or a vague "more than two sprints" estimate. If current/prior sprint evidence
cannot be established, write `Coverage drift: Not assessed — comparable sprint
evidence unavailable`.

---

## 6. Generate Report and Suite Manifest

### Report format (in conversation)

```
## Regression Suite Status

**Mode**: [update | audit | report]
**Existing registered tests**: [N]
**Test files scanned**: [N]

### Critical Path Coverage (audit mode only)
| System | Total ACs | Covered | Partial | Missing | Exempt |
|--------|-----------|---------|---------|---------|--------|
| [name] | [N] | [N] | [N] | [N] | [N] |

**Coverage rate (non-exempt, excluding STALE rows)**: [N]% / Not calculated

### Bug Regression Coverage
| Bug ID | System | Severity | Has Regression Test? |
|--------|--------|----------|----------------------|
| BUG-NNN | [system] | S[N] | YES / NO |

### Coverage Drift Indicators
[Evidence-backed indicators, None detected, or Not assessed.]

### Recommended New Regression Tests
| Priority | System | Suggested Test File | Covers |
|----------|--------|---------------------|--------|
| HIGH | [system] | `tests/unit/[system]/[slug]_regression_test.[ext]` | BUG-NNN / AC-[N] |
```

### Suite manifest format (`tests/regression-suite.md`)

```markdown
# Regression Suite Manifest

> Last Updated: [date]
> Total valid registered tests: [N; excludes STALE]
> Coverage: [N]% of GDD critical paths / Not calculated

## How to run

[Configured engine/project command, or Unavailable — project test command not configured]

## Registered Regression Tests

### [System Name]

| Test File | Test Function (if known) | Covers | Added / Status |
|-----------|--------------------------|--------|----------------|
| `tests/unit/[system]/[file]_test.[ext]` | `test_[scenario]` | AC-N / BUG-NNN | [date or STALE] |

## Known Gaps

| Priority | System | Suggested Path | Covers | Reason Not Yet Written |
|----------|--------|----------------|--------|------------------------|
| HIGH | [system] | `tests/unit/[system]/[path]` | BUG-NNN | Bug fixed without test |

## Quarantined Tests

Tests suspected or confirmed flaky; they remain enabled in CI while awaiting a fix:

| Test File | Function | Reason | Quarantined Since |
|-----------|----------|--------|-------------------|
| (none) | | | |
```

---

## 7. Write Output

Add the manifest create/edit to the complete changeset preview; do not write it
until authorized.

- `update`: add registrations for existing verified tests, record gaps, and
  target-update rows that became STALE. Preserve all unrelated entries.
- `audit`: regenerate current coverage while retaining any missing/renamed
  historical entry as STALE rather than deleting it. STALE rows never count as
  valid coverage.
- `report`: write nothing.

For `report`, finish with **COMPLETE** — read-only status reported. For `update`
or `audit`, say the suite was updated only after the authorized manifest write.
If the user chooses not to write, report **COMPLETE — analysis finished;
manifest not written**.

---

## Collaborative Protocol

- **Never remove existing regression tests from the manifest** without explicit
  user approval; missing entries are marked STALE
- **Gaps are advisory, not blocking** — surface them clearly but do not prevent
  other work from proceeding (except at a separate release gate)
- **Quarantine is not disabling** — suspected or confirmed flaky tests remain
  in CI and should be fixed by `$test-flakiness`; never add skip/disable instructions
- **Single changeset approval** — include the manifest in the complete preview before creating or updating it
