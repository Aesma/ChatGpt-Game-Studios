---
name: test-flakiness
description: "Detect non-deterministic (flaky) tests by reading CI run logs or test result history. Aggregates pass rates per test, identifies intermittent failures, recommends quarantine or fix, and maintains a flaky test registry. Best run during Polish phase or after multiple CI runs."
---

## Invocation and execution

Invoke this workflow as `$test-flakiness`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[ci-log-path | scan | registry]`. Treat bracketed values as optional unless the workflow says otherwise.


# Test Flakiness Detection

A flaky test is one that sometimes passes and sometimes fails without any code
change. Flaky tests are worse than no tests in some ways — they train the team
to ignore red CI runs, masking genuine failures. This skill identifies them,
explains likely causes, and recommends whether to quarantine or fix each one.

**Output:** Updated `tests/regression-suite.md` quarantine section + optional
`production/qa/flakiness-report-[date].md`

**When to run:**
- Polish phase (tests have had many runs; statistical signal is reliable)
- When developers start dismissing CI failures as "probably flaky"
- After `$regression-suite` identifies quarantined tests that need diagnosis

---

## 1. Parse Arguments

**Modes:**
- `$test-flakiness [ci-log-path]` — analyse a specific CI run log file
- `$test-flakiness scan` — scan all available CI logs in `.github/` or
  standard log output directories
- `$test-flakiness registry` — read existing regression-suite.md quarantine
  section and provide remediation guidance for already-known flaky tests
- No argument — auto-detect: run `scan` if CI logs are accessible, else
  `registry`

---

## 2. Locate CI Log Data

### Option A — GitHub Actions (preferred)

Check read-only for workflow definitions under `.github/` and test-result artifacts under `test-results/`. Treat missing directories as no evidence rather than an error.

For Godot projects: GdUnit4 outputs XML results compatible with JUnit format.
Check `test-results/` for `.xml` files.

For Unity projects: game-ci test runner outputs NUnit XML to `test-results/`
by default.

For Unreal projects: automation logs go to `Saved/Logs/`. Search file contents for
`Result: Success` and `Result: Fail` patterns.

### Option B — Local log files

If a path argument is provided, read that file directly and identify explicit run boundaries. A file containing only one independent run is insufficient history: report SUSPECT/insufficient evidence, do not calculate a flakiness rate, and do not update the quarantine table.

### Option C — No log data available

If no logs found:
> "No CI log data found. To detect flaky tests, this skill needs test result
> history from multiple runs. Options:
> 1. Run the test suite at least 3 times and collect the output logs
> 2. Check CI pipeline output and save a log to `test-results/`
> 3. Run `$test-flakiness registry` to review tests already flagged as flaky
>    in `tests/regression-suite.md`"

Stop and ask the user which option to pursue.

---

## 3. Parse Test Results

For each CI log or result file found, parse:

**JUnit XML format** (GdUnit4 / Unity):
- Search file contents for `<testcase name=` to get test names
- Search file contents for `<failure` or `<error` to identify failures
- Parse `classname` and `name` attributes for full test identifiers

**Plain text logs**:
- Search file contents for pass/fail patterns:
  - Godot: `PASSED` / `FAILED` adjacent to test names
  - Unreal: `Result: Success` / `Result: Fail`
  - Unity: `Test passed` / `Test failed`

Build a table: `test_id → [run1_result, run2_result, run3_result, ...]`

Also capture any build/version identity already present in each input run. Do not create a hash/SHA mechanism. Runs are equivalent-code evidence only when their own logs explicitly identify the same build/version; otherwise record `code equivalence unknown`.

---

## 4. Identify Flaky Tests

A test is **flaky** if it appears in the result history with both PASS and
FAIL outcomes across comparable runs. CONFIRMED FLAKY requires multiple runs, mixed outcomes, and explicit same-build/version evidence. Mixed outcomes with unknown code equivalence remain SUSPECT because they may represent an ordinary regression/fix sequence.

Flakiness thresholds:
- **High flakiness**: Fails in >25% of comparable runs — prioritize a fix and treat the suite as unreliable/blocking
- **Moderate flakiness**: Fails in 5–25% of runs — investigate and fix soon
- **Low/suspected flakiness**: Fails in 1–5% of runs — monitor; may be
  genuinely rare failure

For each flaky test, classify the likely cause:

### Cause classification

| Cause | Symptoms | Fix direction |
|-------|----------|---------------|
| **Timing / async** | Fails after awaiting signals or timers; pass rate correlates with system load | Add explicit await/synchronisation; avoid time-based delays |
| **Order dependency** | Fails when run after specific other tests; passes in isolation | Add proper setup/teardown; ensure test isolation |
| **Random seed** | Fails intermittently with no pattern; involves RNG | Pass explicit seed; don't use `randf()` in tests |
| **Resource leak** | Fails more often later in a test run | Fix cleanup in teardown; check orphan nodes (Godot) or object disposal (Unity) |
| **External state** | Fails when a file, scene, or global exists from a prior test | Isolate test from file system; use in-memory mocks |
| **Floating point** | Fails on comparisons like `== 0.5` | Use epsilon comparison (`is_equal_approx`, `Assert.AreApproximately`) |
| **Scene/prefab load race** | Fails when scenes are not yet ready | Await one frame after instantiation; use `await get_tree().process_frame` |

Search to check the test file for timing calls, randf, global state access,
or equality comparisons on floats to narrow down the cause.

---

## 5. Recommend Action

For each flaky test:

**High flakiness:**
> "Prioritize fixing this test and treat the affected suite as unreliable/blocking. Do not disable or skip it to make CI green. Record an isolation suggestion only if an existing project policy permits it and the user makes that separate decision."

**Investigate and fix soon (Moderate):**
> "This test is intermittently unreliable. Root cause appears to be [cause].
> Suggested fix: [specific fix based on cause classification]. Do not quarantine
> yet — fix the test directly."

**Monitor (Low/suspected):**
> "This test shows suspected flakiness. Collect more run data before
> quarantining. Note it as 'suspected' in the regression suite."

---

## 6. Generate Reports

### In-conversation summary

```
## Flakiness Detection Results

**Runs analysed**: [N]
**Tests tracked**: [N]

### Flaky Tests Found

| Test | System | Fail Rate | Likely Cause | Recommendation |
|------|--------|-----------|--------------|----------------|
| [test_name] | [system] | [N]% | Timing | Quarantine + fix async |
| [test_name] | [system] | [N]% | Float comparison | Fix: use epsilon compare |
| [test_name] | [system] | [N]% | Order dependency | Investigate teardown |

### Clean Tests (no flakiness detected)

[N] tests ran across [N] runs with consistent results — no flakiness detected.

### Data Limitations

[Note if fewer than 5 runs were available — fewer runs = less statistical confidence]
```

---

## 7. Update Regression Suite + Optional Report File

Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.

This workflow never modifies test files or applies skip annotations. Append to the existing Quarantined Tests table only when the test is already actually isolated by a separate, explicitly authorized user action. Otherwise keep the result as an in-conversation recommendation and do not claim quarantine has occurred. Never remove existing entries.

Add the optional report file to the same complete changeset preview; do not request a separate approval.

The full report includes per-test analysis with cause details and
engine-specific fix snippets.

After writing:

- For each suggested isolation: state that the test remains active unless the user separately changes it under an existing project policy.
- For fix-eligible tests: "The fix for [test] is straightforward —
  change the equality comparison on line [N] to use `is_equal_approx`."
- Summary: do not promise green CI from annotations; schedule root-cause fixes before the release gate.

---

## Collaborative Protocol

- **Never delete test files** — quarantine means annotate + list, not remove
- **Never auto-disable or skip tests** — registry text is not proof that CI stopped running a test
- **Statistical confidence matters** — with < 3 runs, flag findings as
  "suspected" not "confirmed"; ask if more run data is available
- **Fix is always the goal** — quarantine is temporary; surface the fix
  direction even when recommending quarantine
- **Single changeset approval** — preview the regression-suite update and report file together; one approval covers both. On write: Verdict: **COMPLETE** — flakiness report written. On decline: Verdict: **BLOCKED** — user declined write.
- **Flakiness in CI is a team problem** — surface the list and recommended
  actions clearly; do not just silently quarantine without the team knowing
