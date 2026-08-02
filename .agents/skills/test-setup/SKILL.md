---
name: test-setup
description: "Scaffold the test framework and CI/CD pipeline for the project's engine. Creates the tests/ directory structure, engine-specific test runner configuration, and GitHub Actions workflow. Run once during Technical Setup phase before the first sprint begins."
---

## Invocation and execution

Invoke this workflow as `$test-setup`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[force]`. Treat bracketed values as optional unless the workflow says otherwise.

Accept no argument or exactly `force`. Unknown/multiple arguments output usage and
stop without reading further or writing.


# Test Setup

This skill scaffolds the automated testing infrastructure for the project.
It detects the configured engine, generates the appropriate test runner
configuration, creates the standard directory layout, and wires up CI/CD
so tests run on every push.

Run this once during the Technical Setup phase, before any implementation
begins. A test framework installed at sprint start costs 30 minutes.
A test framework installed at sprint four costs 3 sprints.

**Output:** `tests/` directory structure + `.github/workflows/tests.yml`

---

## Phase 1: Detect Engine and Existing State

1. **Read engine config**:
   - Read `docs/technical-preferences.md` and extract the `Engine:` value.
   - If engine is not configured (`[TO BE CONFIGURED]`), stop:
     "Engine not configured. Run `$setup-engine` first, then re-run `$test-setup`."

2. **Check for existing test infrastructure**:
   - Check each exact target promised by this workflow: README/placeholder files for unit, integration, performance, playtest, the existing smoke seed, the exact `.github/workflows/tests.yml`, and engine-specific files.
   - An unrelated workflow does not satisfy `tests.yml`; a bare directory is not a versioned artifact.
   - Find files matching `tests/gdunit4_runner.gd` (Godot) or `tests/EditMode/` (Unity) or
     `Source/Tests/` (Unreal) for engine-specific artifacts.

3. **Report findings**:
   - "Engine: [engine]. Test directory: [found / not found]. CI workflow: [found / not found]."
   - If everything already exists AND `force` argument was not passed:
     "Test infrastructure appears to be in place. Re-run with `$test-setup force`
     to create any missing targets. Proceeding will not overwrite existing test files."

If the `force` argument is passed, skip the "already exists" early-exit and
proceed — but still do not overwrite files that already exist at a given path.
Only create files that are missing.

---

## Phase 2: Present Plan

Based on the engine detected and the existing state, present a plan:

Resolve engine family together with configured language/framework (including
versioned values such as Godot 4.x or Unreal Engine 5.x). Unknown or unsupported
combinations stop; do not choose a template from a loose string match.

```
## Test Setup Plan — [Engine]

I will create the following (skipping any that already exist):

tests/
  unit/           — Isolated unit tests for formulas, state, and logic
  integration/    — Cross-system tests and save/load round-trips
  performance/    — Performance and budget tests
  playtest/       — Documented playtest protocols/results
  smoke/          — Existing critical-path seed; not one of the four standard test categories
  README.md       — Test framework documentation

[Engine-specific files — see per-engine details below]

.github/workflows/tests.yml  — CI: run tests on every push to main

Estimated time: ~5 minutes to create all files.
```

Ask: "Should the proposed changeset include these files? Existing test files at the same paths will not be overwritten."

Treat the answer as a scope choice, then obtain the one complete changeset authorization before writing.

---

## Phase 3: Create Directory Structure

After the complete changeset authorization, create the following files. Every
standard directory must contain its listed README/placeholder so it is an actual
versioned changeset item; summaries list files, never claim that empty directories
were committed.

- `tests/unit/README.md` — unit-test scope and naming (unless an existing engine-specific placeholder already versions this directory)
- `tests/integration/README.md` — integration-test scope and naming (same preservation rule)
- `tests/performance/README.md` — performance/budget evidence scope
- `tests/playtest/README.md` — documented playtest protocol/result scope

Never overwrite an existing file; preview only the missing targets.

### `tests/README.md`

````markdown
# Test Infrastructure

**Engine**: [engine name + version]
**Test Framework**: [GdUnit4 | Unity Test Framework | UE Automation]
**CI**: `.github/workflows/tests.yml`
**Setup date**: [date]

## Directory Layout

```
tests/
  unit/           # Isolated unit tests (formulas, state machines, logic)
  integration/    # Cross-system and save/load tests
  performance/    # Performance and budget tests
  playtest/       # Documented playtest protocols/results
  smoke/          # Critical path test list for $smoke-check gate
```

## Running Tests

[Engine-specific command — see below]

## Test Naming

- **Files**: `[system]_[feature]_test.[ext]`
- **Functions**: `test_[scenario]_[expected]`
- **Example**: `combat_damage_test.gd` → `test_base_attack_returns_expected_damage()`

## Story Type → Test Evidence

| Story Type | Required Evidence | Location |
|---|---|---|
| Logic | Automated unit test — must pass | `tests/unit/[system]/` |
| Integration | Integration test OR playtest doc | `tests/integration/[system]/` |
| Visual/Feel | Screenshot + lead sign-off | `production/qa/evidence/` |
| UI | Manual walkthrough OR interaction test | `production/qa/evidence/` |
| Config/Data | Smoke check pass | `production/qa/smoke-*.md` |

## CI

Tests run automatically on every push to `main` and on every pull request.
The workflow reports a failed test suite. Repository branch-protection settings,
if separately configured, determine whether that result blocks merging.
````

### Engine-specific files

#### Godot 4 (`Engine: Godot`)

Do not generate a homemade `tests/gdunit4_runner.gd` that calls `run_tests()` and immediately exits successfully. Reuse an existing runner only when its current GdUnit4 API and failure-code propagation are already verifiable in the project. Without that evidence, create only the directory/README targets, report runner and CI as incomplete, and return BLOCKED/partial rather than COMPLETE.

Create `tests/unit/.gdignore_placeholder` with content:
`# Unit tests go here — one subdirectory per system (e.g., tests/unit/combat/)`

Create `tests/integration/.gdignore_placeholder` with content:
`# Integration tests go here — one subdirectory per system`

Note in the README: **Installing GdUnit4**
```
1. Open Godot → AssetLib → search "GdUnit4" → Download & Install
2. Enable the plugin: Project → Project Settings → Plugins → GdUnit4 ✓
3. Restart the editor
4. Verify: res://addons/gdunit4/ exists
```

#### Unity (`Engine: Unity`)

Create `tests/EditMode/` placeholder file `tests/EditMode/README.md`:
```markdown
# Edit Mode Tests
Unit tests that run without entering Play Mode.
Use for pure logic: formulas, state machines, data validation.
Assembly definition required: `tests/EditMode/EditModeTests.asmdef`
```

Create `tests/PlayMode/README.md`:
```markdown
# Play Mode Tests
Integration tests that run in a real game scene.
Use for cross-system interactions, physics, and coroutines.
Assembly definition required: `tests/PlayMode/PlayModeTests.asmdef`
```

Resolve the project's actual runtime assembly name before writing Unity test assemblies. Include `tests/EditMode/EditModeTests.asmdef` and `tests/PlayMode/PlayModeTests.asmdef` in the same changeset with that real reference. If it cannot be uniquely determined, stop the Unity scaffold and do not write placeholder JSON.

Note in the README: **Enabling Unity Test Framework**
```
Window → General → Test Runner
(Unity Test Framework is included by default in Unity 2019+)
```

#### Unreal Engine (`Engine: Unreal` or `Engine: UE5`)

Create `Source/Tests/README.md` only with the actual project/test prefix resolved from the existing `.uproject` and tests; replace `[ActualPrefix]` below. If it cannot be resolved, do not write a placeholder README.
```markdown
# Unreal Automation Tests
Tests use the UE Automation Testing Framework.
Run via: Session Frontend → Automation → select "[ActualPrefix]." tests
Or headlessly: [existing configured runner command using ActualPrefix]

Test class naming: F[SystemName]Test
Test category naming: "[ActualPrefix].[System].[Feature]"
```

---

## Phase 4: Create CI/CD Workflow

### Godot 4

Create `.github/workflows/tests.yml` only when the current GdUnit4 action/runner API, failure propagation, and actual report path are already verifiable. Otherwise leave CI unwritten and report BLOCKED/partial as required by Phase 3.

```yaml
name: Automated Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Run GdUnit4 Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          lfs: true

      - name: Run GdUnit4 Tests
        uses: MikeSchulze/gdUnit4-action@v1
        with:
          godot-version: '[VERSION FROM docs/engine-reference/godot/VERSION.md]'
          paths: |
            tests/unit
            tests/integration
          report-name: test-results

      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: [actual artifact path produced by the verified existing action/runner]
```

Do not emit the upload step unless that actual path is already confirmed from the
project's action/runner contract; the report name alone is not proof of `reports/`.

### Unity

Create `.github/workflows/tests.yml` only when the repository's existing CI configuration already provides the required Unity runner/license prerequisites. Do not create a workflow that is known to fail pending a new secret, and do not propose creating a secret. When the prerequisites are absent, stop at plan/partial state and leave the workflow unwritten.

```yaml
name: Automated Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Run Unity Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          lfs: true

      - name: Run Edit Mode Tests
        uses: game-ci/unity-test-runner@v4
        env:
          UNITY_LICENSE: ${{ secrets.UNITY_LICENSE }}
        with:
          testMode: editmode
          artifactsPath: test-results/editmode

      - name: Run Play Mode Tests
        uses: game-ci/unity-test-runner@v4
        env:
          UNITY_LICENSE: ${{ secrets.UNITY_LICENSE }}
        with:
          testMode: playmode
          artifactsPath: test-results/playmode

      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: test-results/
```

Use only the already configured credential name; never invent or request a new secret from this workflow.

### Unreal Engine

Create `.github/workflows/tests.yml` only after reading a unique existing `.uproject` name, automation test prefix, configured runner command/shell, failure exit behavior, and actual log artifact path. Generate the workflow from those concrete existing values. If any prerequisite is missing, return BLOCKED/partial and do not write a workflow containing placeholder project names, test prefixes, commands, environment variables, shells, or artifact paths. Do not propose new runner credentials or configuration.

---

## Phase 5: Create Smoke Test Seed

Create `tests/smoke/critical-paths.md` from the existing game concept and technical
preferences. Include only implemented/applicable core paths and configured budgets;
unknown items stay visibly `TO BE DEFINED` and make this seed incomplete evidence.
Do not assume a main menu, save/load, 60fps, or five-minute memory window.

Template shape:

```markdown
# Smoke Test: Critical Paths

**Purpose**: Run these 10-15 checks in under 15 minutes before any QA hand-off.
**Run via**: `$smoke-check` (which reads this file)
**Update**: Add new entries when new core systems are implemented.

## Core Stability (always run)

1. [Applicable launch/entry path from the game concept — or TO BE DEFINED]

## Core Mechanic (update per sprint)

<!-- Add the primary mechanic for each sprint here as it is implemented -->
<!-- Example: "Player can move, jump, and the camera follows correctly" -->
4. [Primary mechanic — update when first core system is implemented]

## Data Integrity

5. [Applicable data-integrity path — or N/A / TO BE DEFINED]

## Performance

7. [Configured performance budget on target hardware — or TO BE DEFINED]
```

---

## Phase 6: Post-Setup Summary

After writing all files, report:

```
Test infrastructure created for [engine].

Files created:
- tests/README.md
- [actual placeholder/README files created under tests/unit, integration, performance, playtest]
- tests/smoke/critical-paths.md
[engine-specific files]
- .github/workflows/tests.yml

Next steps:
1. [Engine-specific install step, e.g., "Install GdUnit4 via AssetLib"]
2. Write your first test: create tests/unit/[first-system]/[system]_test.[ext]
3. Run `$qa-plan sprint` before your first sprint to classify stories and set
   test evidence requirements
4. `$smoke-check` before every QA hand-off

Gate note: $gate-check Technical Setup → Pre-Production checks:
- tests/ directory with unit/ and integration/ subdirectories
- .github/workflows/tests.yml
- Example tests are a separate implementation task; this scaffold does not create or promise a production example test.

Verdict: **COMPLETE** — only when the selected engine's required scaffold and runnable existing-prerequisite CI contract are actually complete. Otherwise verdict is **BLOCKED** with the incomplete paths listed.
```

---

## Collaborative Protocol

- **Never overwrite existing test files** — only create files that are missing.
  If a test runner file exists, leave it as-is.
- **Use one changeset authorization** — Phase 2 previews every file before the first write; do not ask again file by file.
- **Engine detection is non-negotiable** — if the engine is not configured,
  stop and redirect to `$setup-engine`. Do not guess.
- **`force` flag skips the "already exists" early-exit but never overwrites.**
  It means "create any missing files even if the directory already exists."
- Unity CI is omitted when its existing runner/license prerequisite is absent;
  do not recommend creating a new secret as part of this workflow.
