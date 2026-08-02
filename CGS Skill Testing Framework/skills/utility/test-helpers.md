# Skill Test Spec: $test-helpers

## Skill Summary

`$test-helpers` generates engine-specific test helper utilities for the project's
test suite. Helpers include factory functions (for creating test entities with
known state), fixture loaders, assertion helpers, and mock stubs for external
dependencies. Generated helpers follow the naming and structure conventions in
`coding-standards.md` and are written to `tests/helpers/`.

Treat the complete described file set as one bounded changeset: use existing task authorization, or preview and confirm it once before the first write.
4. File is written on approval; verdict is COMPLETE

**Assertions:**
- [ ] Generated helper is in GDScript (not C# or Blueprint)
- [ ] Factory function parameters use defaults matching GDD values
- [ ] Helper uses dependency injection (no Autoload/singleton references)
- [ ] Filename follows snake_case convention for GDScript
- [ ] Verdict is COMPLETE

---

### Case 2: No Test Setup Exists — Redirects to $test-setup

**Fixture:**
- `tests/` directory does not exist

**Input:** `$test-helpers player-factory`

**Expected behavior:**
1. Skill checks for `tests/` directory — not found
2. Skill reports: "Test directory not found — test framework must be set up first"
3. Skill suggests running `$test-setup` before generating helpers
4. No helper file is created

**Assertions:**
- [ ] Error message identifies the missing tests/ directory
- [ ] `$test-setup` is suggested as the prerequisite step
- [ ] No file modification occurs
- [ ] Verdict is not COMPLETE (blocked state)

---

### Case 3: Helper Already Exists — never overwritten or extended

**Fixture:**
- `tests/helpers/player_factory.gd` already exists with a `create_player()` function
- User requests a new `create_enemy()` function be added to the factory

**Input:** `$test-helpers enemy-factory`

**Expected behavior:**
1. Skill finds an existing `player_factory.gd` and checks if it's the right file
   to extend (or if a separate `enemy_factory.gd` should be created)
2. Skill reports the existing handwritten helper as skipped and does not edit it.
3. A distinct new helper may be proposed only when it has a non-conflicting scope/name.

**Assertions:**
- [ ] Existing helper is detected and surfaced
- [ ] Existing helper content is not overwritten or extended
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Only Godot+GDScript+GdUnit4, Unity+C#+NUnit, and Unreal+C+++Automation combinations are generated; unsupported combinations BLOCK
- [ ] Godot generic signal wrappers with assumed arity are not generated without a project-proven GdUnit4 pattern
- [ ] Factories construct actual production types/scenes and never use bare Node metadata as Player/attacker/target substitutes
- [ ] Unreal helper and include are under the existing `Source/Tests/` contract
- [ ] Write Output says validated only after an actual configured command succeeds; failures BLOCK and absent execution is `not verified`
5. File is written; verdict is COMPLETE with advisory note

**Assertions:**
- [ ] Skill proceeds without GDD (does not block)
- [ ] Generated helper has placeholder defaults with TODO comment
- [ ] Missing GDD is noted in the output (advisory warning)
- [ ] Verdict is COMPLETE

---

### Case 5: Director Gate Check — No gate; test-helpers is a scaffolding utility

**Fixture:**
- Engine configured, tests/ exists

**Input:** `$test-helpers player-factory`

**Expected behavior:**
1. Skill generates and writes the helper file
2. No director agents are spawned
3. No gate IDs appear in output

**Assertions:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Verdict is COMPLETE without any gate check

---

## Protocol Compliance

### P1 Regression Matrix

- [ ] Missing test root/framework stops before helper creation and points to `$test-setup`.
- [ ] Samples prefer the requested system, use stable path order, cap at five, and list actual files.
- [ ] Scaffold needs only engine/framework/tests; system/all missing GDD or production type yields skipped system plus BLOCKED/partial.
- [ ] `all` maps test directory segments through systems-index Design Doc; ambiguity produces no helper.
- [ ] Existing helpers are never overwritten or extended.
- [ ] Godot scene helper handles load/instantiate failure and documents caller teardown ownership.
- [ ] Global symbol/namespace collisions skip creation rather than overwrite or invent another global name.
- [ ] Created/skipped counts are explicit; created=0 never claims helper files created.

- [ ] Reads engine before generating any helper (helpers are engine-specific)
- [ ] Reads GDD for default values when available
- [ ] Notes missing GDD context rather than blocking
- [ ] Detects existing helper files and offers extend rather than replace
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Verdict is COMPLETE when helper is written

---

## Coverage Notes

- Mock/stub helper generation (for dependencies like save systems or audio buses)
  follows the same pattern as factory helpers and is not separately tested.
- Unity C# helper generation (using NSubstitute or custom mocks) follows the
  same logic as Case 1 with language-appropriate output.
- The case where the requested helper type is not recognized is not tested;
  the skill would ask the user to clarify the helper type.
