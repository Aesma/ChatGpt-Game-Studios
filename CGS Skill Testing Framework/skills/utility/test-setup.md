# Skill Test Spec: $test-setup

## Skill Summary

`$test-setup` scaffolds the test framework for the project based on the
configured engine. It creates the `tests/` directory structure defined in
`coding-standards.md` (unit/, integration/, performance/, playtest/) and
generates the appropriate test runner configuration for the detected engine:
GdUnit4 config for Godot, Unity Test Runner asmdef for Unity, or Unreal headless
runner for Unreal Engine.

Treat the complete described file set as one bounded changeset: use existing task authorization, or preview and confirm it once before the first write.
4. Directories and GdUnit4 runner script created on approval
5. Skill confirms the runner script matches the CI command in coding-standards.md:
   `godot --headless --script tests/gdunit4_runner.gd`
6. Verdict is COMPLETE

**Assertions:**
- [ ] All 4 subdirectories (unit/, integration/, performance/, playtest/) are created
- [ ] No unverified homemade GdUnit4 runner is generated; without a known API/failure contract the result is BLOCKED/partial
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
6. Verdict is COMPLETE

**Assertions:**
- [ ] Unity-specific `Tests/` structure is created (not the Godot structure)
- [ ] `.asmdef` files are generated
- [ ] Both asmdef files reference the uniquely resolved real runtime assembly; unknown references block without placeholder JSON
- [ ] EditMode and PlayMode runner config is present
- [ ] Verdict is COMPLETE

---

### Case 3: Test Framework Already Exists — Verifies config, not re-initialized

**Fixture:**
- `tests/unit/`, `tests/integration/` exist
- GdUnit4 runner script exists (Godot project)

**Input:** `$test-setup`

**Expected behavior:**
1. Skill detects existing tests/ structure
2. Skill reports: "Test framework already exists — verifying configuration"
3. Skill checks: runner script path, directory completeness, CI command alignment
4. If all checks pass: reports "Configuration verified — no changes needed"
5. If checks fail (e.g., missing tests/performance/): reports specific gap and
   asks "May I add the missing directories?"

**Assertions:**
- [ ] Skill does NOT reinitialize when framework exists
- [ ] Verification checks are performed on existing structure
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Verdict is COMPLETE whether everything was OK or gaps were fixed

---

### Case 4: No Engine Configured — Redirects to $setup-engine

**Fixture:**
- `technical-preferences.md` contains only placeholders (engine not set)

**Input:** `$test-setup`

**Expected behavior:**
1. Skill reads `technical-preferences.md` and finds engine placeholder
2. Skill reports: "Engine not configured — cannot scaffold engine-specific test framework"
3. Skill suggests running `$setup-engine` first
4. No directories or files are created

**Assertions:**
- [ ] Error message explicitly states engine is not configured
- [ ] `$setup-engine` is suggested as the next step
- [ ] No file modification occurs
- [ ] Verdict is not COMPLETE (blocked state)

---

### Case 5: Director Gate Check — No gate; test-setup is a scaffolding utility

**Fixture:**
- Engine configured, tests/ does not exist

**Input:** `$test-setup`

**Expected behavior:**
1. Skill scaffolds and writes all test framework files
2. No director agents are spawned
3. No gate IDs appear in output

**Assertions:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Verdict is COMPLETE without any gate check

---

## Protocol Compliance

- [ ] Reads engine from `technical-preferences.md` before generating any scaffold
- [ ] Generates engine-appropriate test runner config (not generic)
- [ ] Creates all 4 subdirectories from coding-standards.md
- [ ] Visual/UI evidence points to `production/qa/evidence/`; `tests/evidence/` is not created
- [ ] Unity CI is written only when existing runner/license prerequisites are already configured; no new secret is suggested
- [ ] Unreal CI contains the actual uproject, test prefix, runner shell/command, and failure behavior, or is not written
- [ ] COMPLETE is impossible when the selected engine's runner/assembly/workflow contract remains partial
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Detects existing framework and offers verification (not reinitialization)
- [ ] Verdict is COMPLETE when scaffold is in place

---

## Coverage Notes

- Unreal Engine test scaffolding (headless runner with `-nullrhi`) follows the
  same pattern as Cases 1 and 2 and is not separately fixture-tested.
- CI integration file generation (e.g., `.github/workflows/test.yml`) is
  referenced but not assertion-tested here — it may be a separate skill concern.
- The case where tests/ exists but is from a different engine (e.g., Unity tests
  in a now-Godot project) is not tested; the skill would detect the mismatch
  and offer to reconcile.
