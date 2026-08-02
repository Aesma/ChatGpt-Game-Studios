---
name: test-helpers
description: "Generate engine-specific test helper libraries for the project's test suite. Reads existing test patterns and produces tests/helpers/ with assertion utilities, factory functions, and mock objects tailored to the project's systems. Reduces boilerplate in new test files."
---

## Invocation and execution

Invoke this workflow as `$test-helpers`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[system-name | all | scaffold]`. Treat bracketed values as optional unless the workflow says otherwise.


# Test Helpers

Writing test cases is faster and more consistent when common setup, teardown,
and assertion patterns are abstracted into helpers. This skill generates a
`tests/helpers/` library tailored to the project's actual engine, language,
and systems — so every developer writes less boilerplate and more assertions.

**Output:** `tests/helpers/` directory with engine-specific helper files

**When to run:**
- After `$test-setup` scaffolds the framework (first time)
- When multiple test files repeat the same setup boilerplate
- When starting to write tests for a new system

---

## 1. Parse Arguments

**Modes:**
- `$test-helpers [system-name]` — generate helpers for a specific system
  (e.g., `$test-helpers combat`)
- `$test-helpers all` — generate helpers for all systems with test files
- `$test-helpers scaffold` — generate only the base helper library (no
  system-specific helpers); use this on first run
- No argument — run `scaffold` if no helpers exist, else `all`

---

## 2. Detect Engine and Language

Read `docs/technical-preferences.md` and extract:
- `Engine:` value
- `Language:` value
- `Framework:` from the Testing section

If engine is not configured: "Engine not configured. Run `$setup-engine` first."

Generate only for combinations implemented below and confirmed by existing test files: Godot 4 + GDScript + GdUnit4, Unity + C# + NUnit, or Unreal + C++ + Automation Tests. Any other engine/language/framework combination is BLOCKED; do not substitute another template.

---

## 3. Load Existing Test Patterns

Scan the test directory for patterns already in use:

```
Search for files matching `tests/**/*_test.*`. (all test files)
```

For a representative sample (up to 5 files), read the test files and extract:
- Setup patterns (how `before_each` / `setUp` / fixtures are written)
- Common assertion patterns (what is being asserted most often)
- Object creation patterns (how game objects or scenes are instantiated in tests)
- Mock/stub patterns (how dependencies are replaced)

This ensures generated helpers match the project's existing style, not a
generic template.

Also read:
- `design/gdd/systems-index.md` — to know which systems exist
- In-scope GDD(s) — to understand what data types and values need testing
- `docs/architecture/tr-registry.yaml` — to map requirements to tested systems

---

## 4. Generate Engine-Specific Helpers

### Godot 4 (GDUnit4 / GDScript)

**Base helper** (`tests/helpers/game_assertions.gd`):

```gdscript
## Game-specific assertion utilities for [Project Name] tests.
## Extends GdUnitAssertions with domain-specific helpers.
##
## Usage:
##   var assert = GameAssertions.new()
##   assert.health_in_range(entity, 0, entity.max_health)

class_name GameAssertions
extends RefCounted

## Assert a value is within the inclusive range [min_val, max_val].
## Use for any formula output that has defined bounds in a GDD.
static func assert_in_range(
    value: float,
    min_val: float,
    max_val: float,
    label: String = "value"
) -> void:
    assert(
        value >= min_val and value <= max_val,
        "%s %.2f is outside expected range [%.2f, %.2f]" % [label, value, min_val, max_val]
    )

## Assert a node exists at path within a parent.
static func assert_node_exists(parent: Node, path: NodePath) -> void:
    assert(
        parent.has_node(path),
        "Expected node at path '%s' to exist." % str(path)
    )
```

Do not generate a generic Godot signal wrapper: callable arity, async completion, and connection cleanup differ by signal. Copy a project-proven GdUnit4 signal assertion pattern only when one already exists; otherwise generate only synchronous helpers and report that signal helpers were omitted.

Generate a factory only from a real production class/scene constructor and an existing test pattern. A bare `Node` plus metadata is never a Player/system substitute. If the production type or injectable construction contract is unclear, omit the factory and return BLOCKED/partial with the missing type named.

**Scene helper** (`tests/helpers/scene_runner_helper.gd`):

```gdscript
## Utilities for scene-based integration tests.
## Wraps GdUnitSceneRunner for common patterns.

class_name SceneRunnerHelper
extends GdUnitTestSuite

## Load a scene and wait one frame for _ready() to complete.
func load_scene_and_wait(scene_path: String) -> Node:
    var scene = load(scene_path).instantiate()
    add_child(scene)
    await get_tree().process_frame
    return scene
```

---

### Unity (NUnit / C#)

**Base helper** (`tests/helpers/GameAssertions.cs`):

```csharp
using NUnit.Framework;
using UnityEngine;

/// <summary>
/// Game-specific assertion utilities for [Project Name] tests.
/// Extends NUnit's Assert with domain-specific helpers.
/// </summary>
public static class GameAssertions
{
    /// <summary>
    /// Assert a value is within an inclusive range [min, max].
    /// Use for any formula output defined in GDD Formulas sections.
    /// </summary>
    public static void AssertInRange(float value, float min, float max, string label = "value")
    {
        Assert.That(value, Is.InRange(min, max),
            $"{label} ({value:F2}) is outside expected range [{min:F2}, {max:F2}]");
    }

    /// <summary>Assert a UnityEvent or C# event was raised during an action.</summary>
    public static void AssertEventRaised(ref bool wasCalled, System.Action action, string eventName)
    {
        wasCalled = false;
        action();
        Assert.IsTrue(wasCalled, $"Expected event '{eventName}' to be raised, but it was not.");
    }

    /// <summary>Assert a component exists on a GameObject.</summary>
    public static void AssertHasComponent<T>(GameObject obj) where T : Component
    {
        var component = obj.GetComponent<T>();
        Assert.IsNotNull(component,
            $"Expected GameObject '{obj.name}' to have component {typeof(T).Name}.");
    }
}
```

**Factory helper** (`tests/helpers/GameFactory.cs`):

```csharp
using UnityEngine;

/// <summary>
/// Factory methods for creating minimal test objects without loading scenes.
/// </summary>
public static class GameFactory
{
    /// <summary>Create a minimal GameObject with a named component for testing.</summary>
    public static GameObject MakeGameObject(string name = "TestObject")
    {
        var go = new GameObject(name);
        return go;
    }

    /// <summary>
    /// Create a ScriptableObject of type T for data-driven tests.
    /// Dispose with Object.DestroyImmediate after test.
    /// </summary>
    public static T MakeScriptableObject<T>() where T : ScriptableObject
    {
        return ScriptableObject.CreateInstance<T>();
    }
}
```

---

### Unreal Engine (C++)

**Base helper** (`Source/Tests/GameTestHelpers.h`):

```cpp
#pragma once

#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"

/**
 * Game-specific assertion macros and helpers for [Project Name] automation tests.
 * Include in any test file that needs domain-specific assertions.
 *
 * Usage:
 *   GAME_TEST_ASSERT_IN_RANGE(TestName, DamageValue, 10.0f, 50.0f, TEXT("Damage"));
 */

// Assert a float value is within inclusive range [Min, Max]
#define GAME_TEST_ASSERT_IN_RANGE(TestName, Value, Min, Max, Label) \
    TestTrue( \
        FString::Printf(TEXT("%s (%.2f) in range [%.2f, %.2f]"), Label, Value, Min, Max), \
        (Value) >= (Min) && (Value) <= (Max) \
    )

// Assert a UObject pointer is valid (not null, not garbage collected)
#define GAME_TEST_ASSERT_VALID(TestName, Ptr, Label) \
    TestTrue( \
        FString::Printf(TEXT("%s is valid"), Label), \
        IsValid(Ptr) \
    )

// Assert an Actor is in the world (spawned successfully)
#define GAME_TEST_ASSERT_SPAWNED(TestName, ActorPtr, ClassName) \
    TestNotNull( \
        FString::Printf(TEXT("Spawned actor of class %s"), TEXT(#ClassName)), \
        ActorPtr \
    )

/**
 * Helper to create a minimal test world.
 * Remember to call World->DestroyWorld(false) in teardown.
 */
namespace GameTestHelpers
{
    inline UWorld* CreateTestWorld(const FString& WorldName = TEXT("TestWorld"))
    {
        UWorld* World = UWorld::CreateWorld(EWorldType::Game, false);
        FWorldContext& WorldContext = GEngine->CreateNewWorldContext(EWorldType::Game);
        WorldContext.SetCurrentWorld(World);
        return World;
    }
}
```

---

## 5. Generate System-Specific Helpers

For `[system-name]` or `all` modes, generate a helper per system:

Read the system's GDD to extract:
- Data types (entity types, component names)
- Formula variables and their bounds
- Common test scenarios mentioned in Edge Cases

Generate a system helper in the engine's existing test tree with factory functions specific to real production objects. For Unreal, keep it under `Source/Tests/`; for Godot/Unity use the existing `tests/helpers/` tree.

Never emit placeholder attacker/target `Node` metadata factories. Derive constructors, dependencies, and bounds from the actual production type plus its linked GDD, or do not generate the system helper.

---

## 6. Write Output

Present a summary of what will be created:

```
## Test Helpers to Create

Base helpers (engine: [engine]):
- tests/helpers/game_assertions.[ext]
- tests/helpers/game_factory.[ext]
[engine-specific extras]

For Unreal, list `Source/Tests/GameTestHelpers.h` and use a project-relative include from the existing test module; never list or include `tests/helpers/GameTestHelpers.h`.

System helpers ([mode]):
- tests/helpers/[system]_factory.[ext]  ← from [system] GDD
```

Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.

**Never overwrite existing files.** If a file already exists, report:
"Skipping `[path]` — already exists. Remove the file manually if you want it
regenerated."

At the existing Write Output completion point, report validation truthfully. If this step already ran the project's configured test command, only a successful actual result may be called `validated`; a failure uses the existing BLOCKED path. If no command ran, label the generated files `not verified` and do not claim compile/load/runner success. Do not add a new post-write phase or validation mechanism.

After writing: Verdict: **COMPLETE** — helper files created (validated only when supported by the actual result above; otherwise not verified).

"Helper files created. To use them in a test:
- Godot: `class_name` is auto-imported — no explicit import needed
- Unity: Add `using` directive or reference the test assembly
- Unreal: include `GameTestHelpers.h` through the existing `Source/Tests/` module's project-relative include path"

---

## Collaborative Protocol

- **Never overwrite existing helpers** — they may contain hand-written
  customisations. Only generate new files that don't exist yet
- **Generated factories use production types** — never replace a real class with metadata on a generic object
- **Helpers should reflect the GDD** — bounds and constants in helpers should
  trace to GDD Formulas sections, not invented values
- **Single changeset approval** — preview all proposed `tests/` files together and create them only after the one approval

## Next Steps

- Run `$test-setup` if the test framework has not been scaffolded yet.
- Use `$dev-story` to implement stories — helpers reduce boilerplate in new test files.
