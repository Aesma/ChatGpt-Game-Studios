---
name: smoke-check
description: "Run the critical path smoke test gate before QA hand-off. Executes the automated test suite, verifies core functionality, and produces a PASS/FAIL report. Run after a sprint's stories are implemented and before manual QA begins. A failed smoke check means the build is not ready for QA."
---

## Invocation and execution

Invoke this workflow as `$smoke-check`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[sprint | quick | --platform pc|console|mobile|all]`. Treat bracketed values as optional unless the workflow says otherwise.


# Smoke Check

This skill is the gate between "implementation done" and "ready for QA
hand-off". It runs the automated test suite, checks for test coverage gaps,
batch-verifies critical paths with the developer, and produces a PASS/FAIL
report.

The rule is simple: **a build that fails smoke check does not go to QA.**
Handing a broken build to QA wastes their time and demoralises the team.

**Output:** `production/qa/smoke-[date].md`

---

## Parse Arguments

Arguments can be combined: `$smoke-check sprint --platform console`

Validate the complete argument list before reading project files. Accept at most
one base mode and at most one `--platform` value. If an unknown positional
argument or flag is present, or `--platform` is missing a value or has a value
outside `pc|console|mobile|all`, show the legal usage above and stop without
asking questions or writing a report. In particular, a system name is not a
supported positional argument.

**Base mode** (first argument, default: `sprint`):
- `sprint` — full smoke check against the current sprint's stories
- `quick` — skip coverage scan (Phase 3) and Batch 3; use for rapid re-checks

**Platform flag** (`--platform`, default: none):
- `--platform pc` — add PC-specific checks (keyboard, mouse, windowed mode)
- `--platform console` — add console-specific checks (gamepad, TV safe zones,
  platform certification requirements)
- `--platform mobile` — add mobile-specific checks (touch, portrait/landscape,
  battery/thermal behaviour)
- `--platform all` — add all platform variants; output per-platform verdict table

If `--platform` is provided, Phase 4 adds platform-specific batches and
Phase 5 outputs a per-platform verdict table in addition to the overall verdict.

---

## Phase 1: Detect Test Setup

Before running anything, understand the environment:

1. **Test framework check**: verify `tests/` directory exists.
   If it does not: "No test directory found at `tests/`. Run `$test-setup`
   to scaffold the testing infrastructure, or create the directory manually
   if tests live elsewhere." Then stop.

2. **CI check**: check whether `.github/workflows/` contains a workflow file
   referencing tests. Note in the report whether CI is configured.

3. **Engine detection**: read `docs/technical-preferences.md` and
   extract the `Engine:` value. Store this for test command selection in
   Phase 2.

4. **Smoke test list**: check whether `production/qa/smoke-tests.md` or
   `tests/smoke/` exists. If a smoke test list is found, load it for use in
   Phase 4. If neither exists, smoke tests will be drawn from the current QA
   plan (Phase 4 fallback).

5. **Resolve the target sprint**: for `sprint` mode, first parse the `sprint`
   value from `production/sprint-status.yaml` and locate that numbered sprint
   file. If the YAML is absent or unusable, fall back to the highest valid
   numbered `production/sprints/sprint-[NNN].md` file (never modification time)
   and record the fallback reason. `quick` mode may use the same target only as
   context; it does not run coverage.

6. **QA plan check**: accept only a file whose filename or explicit `Sprint:`
   field identifies the resolved sprint exactly. Do not choose a QA plan merely
   because it is newest or mentions the same number elsewhere. If no matching
   plan exists, note: "No QA plan for sprint [N] found. Run `$qa-plan sprint`
   before smoke-checking for best results."

Report findings before proceeding: "Environment: [engine]. Test directory:
[found / not found]. CI configured: [yes / no]. QA plan: [path / not found]."

---

## Phase 2: Run Automated Tests

Attempt to run the test suite through the configured shell. Select the command based on the engine
detected in Phase 1:

**Godot 4:**
```bash
godot --headless --script tests/gdunit4_runner.gd 2>&1
```
If the GDUnit4 runner script does not exist at that path, try:
```bash
godot --headless -s addons/gdunit4/GdUnitRunner.gd 2>&1
```
If neither path exists, note: "GDUnit4 runner not found — confirm the runner
path for your test framework."

**Unity:**
Unity tests require the editor and cannot be run headlessly via shell in most
environments. List `test-results/` read-only, sort entries by modification time,
and inspect the five newest artifacts.
If test result files exist (XML or JSON), report the selected artifact's exact
path and modification time. Treat it as current only when its metadata or
surrounding run context proves it belongs to this check's branch/build and was
completed for the current run. Otherwise record `NOT RUN` rather than reusing a
possibly stale result. Parse PASS/FAIL counts only from a proven-current,
complete artifact. If no valid artifact exists: "Unity tests must be run from the
editor or CI pipeline. Please confirm test status manually before proceeding."

**Unreal Engine:**
List `Saved/Logs/` read-only, filter names containing `test` or `automation`,
sort by modification time, and inspect the five newest matching logs. Report
the selected log path and time, and accept it only when it identifies the
current branch/build/run and contains a complete result. Otherwise record
`NOT RUN`; recency alone is not proof. If no valid matching log is found: "UE automation tests must be run via the Session
Frontend or CI pipeline. Please confirm test status manually."

**Unknown engine / not configured:**
"Engine not configured in `docs/technical-preferences.md`. Run
`$setup-engine` to specify the engine, then re-run `$smoke-check`."

**If the test runner is not available in this environment** (engine binary not
on PATH, runner script not found, etc.), report clearly:

"Automated tests could not be executed — engine binary not found on PATH.
Status will be recorded as NOT RUN. Confirm test results from your local IDE
or CI pipeline. Unconfirmed NOT RUN is treated as PASS WITH WARNINGS, not
FAIL — the developer must manually confirm results."

Do not treat NOT RUN as an automatic FAIL. Record it as a warning. The
developer's manual confirmation in Phase 4 can resolve it.

Parse runner output and extract:
- Total tests run
- Passing count
- Failing count
- Names of any failing tests (up to 10; if more, note the count)
- Any crash or error output from the runner itself

---

## Phase 3: Check Test Coverage

Draw the story list from, in priority order:
1. The QA plan that explicitly matches the resolved target sprint (its Test
   Summary table lists expected test file paths per story)
2. The resolved target sprint file from Phase 1
3. If the `quick` argument was passed, skip this phase entirely and record the
   coverage status as `NOT CHECKED` (not zero MISSING): "Coverage scan skipped —
   run `$smoke-check sprint` for full coverage analysis." A quick run can never
   receive a clean PASS; its highest verdict is PASS WITH WARNINGS.

For each story in scope:

1. Read the story's `Test file:` field or `Test Evidence` section and resolve
   every declared project-relative evidence path exactly.
2. Verify that the exact file exists and that its assertions directly cover
   the story/criterion before assigning COVERED or MANUAL.
3. Only when the story declares no exact path, list same-system files under
   `tests/unit/[system]/` or `tests/integration/[system]/` as **unverified
   candidates**. Name/slug/"closely related" matching never proves COVERED and
   candidates remain MISSING or UNKNOWN as appropriate.

Assign a coverage status to each story:

| Status | Meaning |
|--------|---------|
| **COVERED** | A test file was found matching this story's system and scope |
| **MANUAL** | Story type is Visual/Feel or UI; a test evidence document was found |
| **MISSING** | Logic or Integration story with no matching test file |
| **EXPECTED** | Config/Data story — no test file required; spot-check is sufficient |
| **UNKNOWN** | Story file missing or unreadable |

MISSING entries are advisory gaps. They do not cause a FAIL verdict but must
appear prominently in the report and must be resolved before `$story-done` can
fully close those stories.

---

## Phase 4: Run Manual Smoke Checks

Draw the smoke test checklist from, in priority order:
1. The QA plan's "Smoke Test Scope" section (if QA plan was found in Phase 1)
2. `production/qa/smoke-tests.md` (if it exists)
3. `tests/smoke/` directory contents (if it exists)
4. The standard fallback list below (used only when none of the above exist)

Tailor batches 2 and 3 to the actual systems identified from the sprint or QA
plan. Replace bracketed placeholders with real mechanic names from the current
sprint's stories.

Ask the user directly to batch-verify. Keep the entire Phase 4 interaction to
at most 3 calls, including `--platform all`:

1. automated-test confirmation (when needed) plus Batch 1;
2. Batch 2 plus Batch 3 when applicable;
3. every requested platform section together, plus failure descriptions for
   all selected failures that were not captured inline.

The PC, console, and mobile lists below are sections of that third structured
confirmation, not separate calls. If a base-batch failure needs prose, collect
all such descriptions together rather than asking once per batch.

If Phase 2 recorded automated tests as `NOT RUN`, include a one-time automated
test confirmation in the existing manual confirmation interaction and save the
answer as one of: `CONFIRMED PASS`, `CONFIRMED FAIL`, or `UNCONFIRMED`. Do not
infer an answer from the manual smoke batches. `CONFIRMED FAIL` is a failing
check; `UNCONFIRMED` is a warning; `CONFIRMED PASS` allows the normal coverage
and manual-check rules below to decide the verdict.

**Batch 1 — Core stability (always run):**
```
question: "Core stability — select any items that FAILED (leave all unselected if everything passed):"
allow multiple selections
options:
  - "Game does not launch or crashes before reaching the main menu"
  - "New game / session fails to start"
  - "Main menu does not respond to inputs"
  - "Crash or hang observed during basic navigation"
```

For any selected item, ask the user to briefly describe what failed before generating the report.

**Batch 2 — Sprint changes and regression (always run):**
```
question: "Sprint changes and regression — select any items that FAILED (leave all unselected if everything passed):"
allow multiple selections
options:
  - "[Primary mechanic this sprint] — FAILED"
  - "[Second notable change this sprint, if any] — FAILED"
  - "Regression in a previous sprint's feature — FAILED"
  - "Other unexpected breakage observed — FAILED"
```

For any selected item, ask the user to briefly describe what broke before generating the report.

**Batch 3 — Data integrity and performance (run unless `quick` argument):**
```
question: "Data integrity and performance — select any items that FAILED or were skipped (leave all unselected if everything passed):"
allow multiple selections
options:
  - "Save / load — FAILED (data loss or corruption observed)"
  - "Save / load — N/A (save system not yet implemented)"
  - "Frame rate drops or hitches observed — FAILED"
  - "Performance not checked this session"
```

For any FAILED item selected, ask the user to describe what broke before generating the report.

Record selected structured results exactly as selections and store only text
the user actually supplied as verbatim failure descriptions. Do not invent a
PASS sentence or label an unselected option as a verbatim user response.

**Platform Batches** *(run only if `--platform` argument was provided)*:

**PC platform** (`--platform pc` or `--platform all`):
```
question: "PC Platform — select any items that FAILED (leave all unselected if everything passed):"
allow multiple selections
options:
  - "Keyboard controls — FAILED (describe issue after)"
  - "Mouse input or cursor visibility — FAILED (describe issue after)"
  - "Windowed / fullscreen mode — FAILED (describe issue after)"
  - "Resolution change — FAILED (describe issue after)"
```

For any selected item, ask the user to briefly describe what failed before generating the report.

**Console platform** (`--platform console` or `--platform all`):
```
question: "Console Platform — select any items that FAILED (leave all unselected if everything passed):"
allow multiple selections
options:
  - "Gamepad input — FAILED (describe issue after)"
  - "UI outside TV safe zone / text clipped — FAILED (describe what is clipped after)"
  - "Keyboard/mouse fallback shown to gamepad user — FAILED (describe after)"
  - "Cold start (no prior save) — FAILED (describe issue after)"
```

For any selected item, ask the user to briefly describe what failed before generating the report.

**Mobile platform** (`--platform mobile` or `--platform all`):
```
question: "Mobile Platform — select any items that FAILED (leave all unselected if everything passed):"
allow multiple selections
options:
  - "Touch controls — FAILED (describe issue after)"
  - "Orientation change (portrait ↔ landscape) — FAILED (describe what breaks after)"
  - "Background / foreground transition (home button) — FAILED (describe issue after)"
  - "Performance / thermal throttling on target device — FAILED (describe after)"
```

For any selected item, ask the user to briefly describe what failed before generating the report.

---

## Phase 5: Generate Report

Assemble the full smoke check report:

````markdown
## Smoke Check Report
**Date**: [date]
**Sprint**: [sprint name / number, or "Not identified"]
**Engine**: [engine]
**QA Plan**: [path, or "Not found — run $qa-plan first"]
**Argument**: [sprint | quick | blank]

---

### Automated Tests

**Status**: [PASS ([N] tests, [N] passing) | FAIL ([N] failures) |
NOT RUN ([reason])]
**Manual confirmation for NOT RUN**: [CONFIRMED PASS | CONFIRMED FAIL |
UNCONFIRMED | N/A]

[If FAIL, list failing tests:]
- `[test name]` — [brief failure description from runner output]

---

### Test Coverage

| Story | Type | Test File | Coverage Status |
|-------|------|-----------|----------------|
| [title] | Logic | `tests/unit/[system]/[slug]_test.[ext]` | COVERED |
| [title] | Visual/Feel | `tests/evidence/[slug]-screenshots.md` | MANUAL |
| [title] | Logic | — | MISSING ⚠ |
| [title] | Config/Data | — | EXPECTED |

**Summary**: [N] covered, [N] manual, [N] missing, [N] expected, or
`NOT CHECKED — quick mode`.

---

### Manual Smoke Checks

- [x] Game launches without crash — PASS
- [x] New game starts — PASS
- [x] [Core mechanic] — PASS
- [ ] [Other check] — FAIL: [user's description]
- [x] Save / load — PASS
- [-] Performance — not checked this session

---

### Missing Test Evidence

Stories that must have test evidence before they can be marked COMPLETE via
`$story-done`:

- **[story title]** (`[path]`) — Logic story has no test file.
  Expected location: `tests/unit/[system]/[story-slug]_test.[ext]`

[If none:] "All Logic and Integration stories have test coverage."

---

### Platform-Specific Results *(only if `--platform` was provided)*

| Platform | Checks Run | Passed | Failed | Platform Verdict |
|----------|-----------|--------|--------|-----------------|
| PC | [N] | [N] | [N] | PASS / FAIL |
| Console | [N] | [N] | [N] | PASS / FAIL |
| Mobile | [N] | [N] | [N] | PASS / FAIL |

**Platform notes**: [any platform-specific observations not captured in pass/fail]

Any platform with one or more FAIL checks contributes to the overall FAIL verdict.

---

### Verdict: [PASS | PASS WITH WARNINGS | FAIL]

[Verdict rules — first matching rule wins:]

**FAIL** if ANY of:
- Automated test suite ran and reported one or more test failures
- Automated tests were NOT RUN and the developer answered `CONFIRMED FAIL`
- Any executed manual check is marked FAILED, including Batch 1, Batch 2,
  Batch 3, or any requested platform batch

**PASS WITH WARNINGS** if there are no FAIL conditions and ANY of:
- Automated tests are NOT RUN and remain `UNCONFIRMED`
- One or more Logic/Integration stories have MISSING test evidence
- Performance was not checked this session
- Coverage is `NOT CHECKED` because quick mode was used

**PASS** if ALL of:
- Automated tests PASS, or NOT RUN with `CONFIRMED PASS`
- All executed smoke checks in every base and platform batch PASS or N/A
- No MISSING test evidence entries
- No warning condition above applies

`N/A` is not a failure. Apply these rules in the order shown; every combination
of automated-test confirmation, coverage, and executed manual results must map
to exactly one verdict.
````

---

## Phase 6: Write and Gate

Present the full report in conversation. Before the preview, check whether
`production/qa/smoke-[date].md` already exists. If so, label the operation as an
update, describe exactly which content will be replaced, and include that
overwrite in the same complete changeset. Without explicit authorization to
update that path, leave the existing report unchanged. Do not invent a second
filename.

Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.

Write only after the single changeset approval, without re-prompting within its boundary.

After writing, deliver the gate verdict:

**If verdict is FAIL:**

"The smoke check failed. Do not hand off to QA until these failures are
resolved:

[List each failing automated test or smoke check with a one-line description]

Fix the failures and run `$smoke-check` again to re-gate before QA hand-off."

**If verdict is PASS WITH WARNINGS:**

"Smoke check passed with warnings. The build is ready for manual QA.

Advisory items to resolve before running `$story-done` on affected stories:
[list MISSING test evidence entries]

QA hand-off: share `production/qa/qa-plan-[sprint].md` with the qa-tester
agent to begin manual verification."

**If verdict is PASS:**

"Smoke check passed cleanly. The build is ready for manual QA.

QA hand-off: share `production/qa/qa-plan-[sprint].md` with the qa-tester
agent to begin manual verification."

---

## Collaborative Protocol

- **Never treat NOT RUN as automatic FAIL** — record it as NOT RUN and let
  the developer confirm status manually. Unconfirmed NOT RUN contributes to
  PASS WITH WARNINGS, not FAIL.
- **Never auto-fix failures** — report them and state what must be resolved.
  Do not attempt to edit source code or test files.
- **PASS WITH WARNINGS does not block QA hand-off** — it records advisory
  gaps for `$story-done` to follow up on.
- **`quick` argument** skips Phase 3 (coverage scan) and Phase 4 Batch 3.
  Use it for rapid re-checks after fixing a specific failure.
- Ask the user directly for all manual smoke check verification.
- **Never write the report without asking** — Phase 6 requires explicit
  approval before any file is created.
