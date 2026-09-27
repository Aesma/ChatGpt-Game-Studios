---
name: dev-story
description: "Read a story file and implement it. Loads the full context (story, GDD requirement, ADR guidelines, control manifest), routes to the right programmer agent for the system and engine, implements the code and test, and confirms each acceptance criterion. The core implementation skill — run after $story-readiness, before $code-review and $story-done."
---

## Invocation and execution

Invoke this workflow as `$dev-story`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[story-path]`. Treat bracketed values as optional unless the workflow says otherwise.


# Dev Story

This skill bridges planning and code. It reads a story file in full, assembles
all the context a programmer needs, routes to the correct specialist agent, and
drives implementation to completion — including writing the test.

**The loop for every story:**
```
$qa-plan sprint           ← define test requirements before sprint begins
$story-readiness [path]   ← validate before starting
$dev-story [path]         ← implement it  (this skill)
$code-review [files]      ← review it
$story-done [path]        ← verify and close it
```

**After all sprint stories are done:** run `$team-qa sprint` to execute the full QA cycle and get a sign-off verdict before advancing the project stage.

**Output:** Source code + test file in the project's `src/` and `tests/` directories.

---

## Phase 1: Find the Story

**If a path is provided**: read that file directly.

**If no argument**: check `production/session-state/active.md` for the active
story. If found, confirm: "Continuing work on [story title] — is that correct?"
If not found, ask: "Which story are we implementing?" Then search
`production/epics/**/*.md` and list stories with Status: Ready.

---

## Phase 2: Load Full Context

**Before loading any context, verify required files exist.** Parse the story's
current `ADR references`/`Governing ADRs` list before any write or spawn.

The list must be non-empty, contain no duplicate reference, and contain exactly
one explicitly marked `primary` real ADR. Resolve every ADR ID/reference to
exactly one existing `docs/architecture/adr-*.md`; zero matches, multiple
matches, malformed references, or zero/multiple primary markers are collected
and reported together as BLOCKED.

Read every resolved ADR Status. All real references, primary and secondary, must
be exactly Accepted. Proposed, Deprecated, Superseded, unknown, or missing
Status blocks implementation before story/sprint/session writes or programmer
spawn. Put the primary Decision/Implementation Guidelines and every secondary
Decision, constraint, Engine Compatibility, and ADR Dependencies into one
context package. If those texts conflict and cannot be reconciled directly,
surface the conflict and stop rather than guessing.

The sole exception is Type exactly `Config/Data` with exactly one reference
`N/A — [specific reason]`, where the reason is non-empty, non-blank, and not
TBD/placeholder. N/A may not be mixed with a real ID. Invalid N/A, missing ADR
field, or N/A on another story type is BLOCKED before writes/spawn. Valid N/A
skips ADR-file loading but still requires TR registry, story AC, manifest, and
engine preferences.

The TR registry remains required. A missing registry or any ADR validation
failure is reported read-only; do not change session/story status merely to
record the failure.

Validate the story Status before continuing. Only `Ready` or `In Progress` may
proceed. `Blocked` stops with its recorded reason. `Done`/`Complete` requires an
explicit user decision to reopen and the exact status edit must enter the later
changeset; never reopen automatically. Unknown status is BLOCKED.

Inspect every Acceptance Criterion for `TBD`, placeholders, subjective-only
wording, or an outcome that cannot be tested. Before planning/authorization,
ask the user for measurable replacement text and include any accepted story edit
in the single changeset. Do not brief a writer with ambiguous AC.


Read all of the following simultaneously — these are independent reads. Do not start implementation until all context is loaded:

### The story file
Extract and hold:
- **Story title, ID, layer, type** (Logic / Integration / Visual/Feel / UI / Config/Data)
- **TR-ID** — the GDD requirement identifier
- **Complete ADR references list with one explicit primary, or the validated Config/Data N/A item**
- **Manifest Version** embedded in story header
- **Acceptance Criteria** — every checkbox item, verbatim
- **Implementation Notes** — the ADR guidance section in the story
- **Out of Scope** boundaries
- **Test Evidence** — the required test file path
- **Dependencies** — what must be DONE before this story

### The TR registry
Read `docs/architecture/tr-registry.yaml`. Look up the story's TR-ID.
Read the current `requirement` text — this is the source of truth for what the
GDD requires now. Do not rely on any inline text in the story file (may be stale).

### All governing ADRs
Read every validated referenced ADR. Extract the primary Decision and
Implementation Guidelines plus every secondary Decision, constraint, Engine
Compatibility section, and ADR Dependencies. Preserve which reference supplied
each rule.

### The control manifest
Read `docs/architecture/control-manifest.md`. Extract the rules for this story's layer:
- Required patterns
- Forbidden patterns
- Performance guardrails

Check: does the story's embedded Manifest Version match the current manifest header date?
If they differ, ask the user directly before proceeding:
- Prompt: "Story was written against manifest v[story-date]. Current manifest is v[current-date]. New rules may apply. How do you want to proceed?"
- Options:
  - `[A] Include the story version update in the planned changeset and implement with current rules (Recommended)`
  - `[B] Stop here — show me the manifest difference first`

There is no "old rules with a new version" path. On [A], include the exact story
field edit in the complete Phase 2 plan and use current rules. On [B], stop
without changing the story or spawning a programmer.

### Dependency validation

After extracting the **Dependencies** list from the story file, validate each:

1. Find files matching `production/epics/**/*.md` to find each dependency story file.
2. Read its `Status:` field.
3. If any dependency has Status other than `Complete` or `Done`:
   - Ask the user directly:
     - Prompt: "Story '[current story]' depends on '[dependency title]' which is currently [status], not Complete. How do you want to proceed?"
     - Options:
       - `[A] Proceed anyway — I accept the dependency risk`
       - `[B] Stop — I'll complete the dependency first`
       - `[C] The dependency is done but status wasn't updated — mark it Complete and continue`
   - If [B]: stop read-only and report BLOCKED; do not mutate story or session state and do not spawn a programmer.
   - If [C]: record the dependency-status edit as a candidate for the single
     complete Phase 2 changeset; do not authorize or write it before the source
     and test candidates are also known.
   - If [A]: note in Phase 6 summary under "Deviations": "Implemented with incomplete dependency: [dependency title] — [status]."

If a dependency path/title cannot resolve to exactly one story file, report
BLOCKED and stop before authorization or programmer spawn. The existing
Dependencies field must be corrected first.

---

### Engine reference
Read `docs/technical-preferences.md`:
- `Engine:` value — determines which programmer agents to use
- Naming conventions (class names, file names, signal/event names)
- Performance budgets (frame budget, memory ceiling)
- Forbidden patterns

### Plan, authorize, then mark In Progress

First remain read-only and build the implementation plan. Identify the exact
candidate source/config files, test/evidence files, story file, optional
`production/sprint-status.yaml`, and
`production/session-state/active.md`, with an intended operation for each.
Present that complete changeset once. Only after authorization may implementation
begin; an unlisted file discovered later pauses execution for an expanded
preview.

Then update these status fields within the authorized boundary:

1. **`production/sprint-status.yaml`** (if it exists): find the entry matching this story's file path and set the canonical `status: in_progress`. Update the top-level `updated` field to today's date. If the file does not exist, skip silently.

2. **The story file itself**: set its existing `Status:` field to `In Progress`
   and edit `Last Updated:` to today's date (`YYYY-MM-DD`). If Last Updated is
   absent, add it after Status. This enables sprint-status staleness detection
   without closing the story.

---

## Phase 3: Route to the Right Programmer

Based on the story's **Layer**, **Type**, and **system name**, determine which
specialist to spawn through Codex subagent delegation.

**Config/Data stories:** route the authorized data/config files to one existing
primary programmer role with exclusive write ownership. Do not create a
current-agent direct-write exception.

### Primary agent routing table

Apply routing in this order so overlaps cannot create two writers: story Type
`UI`, then `Visual/Feel`, then explicit AI/networking domain, then layer default,
then Config/Data directory ownership. Select exactly one primary and show which
rule won.

| Story context | Primary agent |
|---|---|
| Foundation layer — any type | `engine-programmer` |
| Any layer — Type: UI | `ui-programmer` |
| Any layer — Type: Visual/Feel | `gameplay-programmer` (implements) |
| Core or Feature — gameplay mechanics | `gameplay-programmer` |
| Core or Feature — AI behaviour, pathfinding | `ai-programmer` |
| Core or Feature — networking, replication | `network-programmer` |
| Config/Data — no code | Existing programmer role matching the owned data directory |

### Engine specialist — read-only secondary review for code stories

If engine or language remains unconfigured/placeholder, block engine-specific
code stories before spawning. A pure Config/Data story may continue with the
single data writer, but the summary must state that engine validation was not
performed.

Read the `Engine Specialists` section of `docs/technical-preferences.md`
to get the configured primary specialist. The primary programmer exclusively owns
the listed source/test writes. An engine specialist may run alongside it only as
a read-only reviewer returning recommendations. If a specialist must own a
different file, that non-overlapping file ownership must already be explicit in
the authorized changeset.

| Engine | Specialist agents available |
|--------|----------------------------|
| Godot 4 | `godot-specialist`, `godot-gdscript-specialist`, `godot-shader-specialist` |
| Unity | `unity-specialist`, `unity-ui-specialist`, `unity-shader-specialist` |
| Unreal Engine | `unreal-specialist`, `ue-gas-specialist`, `ue-blueprint-specialist`, `ue-umg-specialist`, `ue-replication-specialist` |

**When engine risk is HIGH** (from the ADR or VERSION.md): always spawn the engine
specialist, even for non-engine-facing stories. High risk means the ADR records
assumptions about post-cutoff engine APIs that need expert verification.

---

## Phase 4: Implement

Spawn the one chosen primary programmer through Codex subagent delegation with
the full writer context package. If an engine specialist is applicable, brief it
separately as a read-only reviewer and do not give it source/test write tasks:

Brief the agent with file paths and targeted reading instructions — do not serialize document content into the delegation prompt. The agent reads what it needs directly:

1. **Story file**: `[story-path]` — read in full
2. **GDD requirement**: look up TR-ID `[TR-XXX-NNN]` in `docs/architecture/tr-registry.yaml` — use the `requirement` field as source of truth
3. **ADRs**: every validated primary and secondary ADR path — read the context
   sections assembled in Phase 2; primary drives the main pattern and secondary
   constraints all apply
4. **Control manifest**: `docs/architecture/control-manifest.md` — read rules for the **[layer]** layer only
5. **Engine preferences**: `docs/technical-preferences.md` — read naming conventions and performance budgets
6. **Test file path**: `[path from story's Test Evidence section]` — this file must be created as part of implementation
7. **Test requirement** (Logic and Integration stories only): The test file MUST be created at `[path from the story's Test Evidence section]`. Write the test alongside the implementation — do not defer it. The story cannot be closed via `$story-done` without this file present. Each acceptance criterion must have at least one test function covering it. Test file naming: `[system]_[feature]_test.[ext]`. Function naming: `test_[scenario]_[expected_outcome]`. No random seeds, no time-dependent assertions, no external I/O.
8. **Explicit instruction**: implement this story following the ADR guidelines, respect the manifest rules, stay within the story's Out of Scope boundaries. Write clean, doc-commented public APIs.

The agent should:
- Create or modify files in `src/` following the ADR guidelines
- Respect all Required and Forbidden patterns from the control manifest
- Stay within the story's Out of Scope boundaries (do not touch unrelated files)
- Write clean, doc-commented public APIs

### Config/Data stories

The chosen primary programmer owns the authorized data-file edit. It reports
the exact old/new values and may not touch unlisted files.

### Visual/Feel stories

Spawn `gameplay-programmer` to implement the code/animation calls. Note that
Visual/Feel acceptance criteria cannot be auto-verified — the "does it feel right?"
check happens in `$story-done` via manual confirmation.

---

## Phase 5: Test Evidence Requirements

Run the affected configured test command in this phase after implementation;
creating a test file is not verification. Record the command and actual result.
If execution is unavailable, report `implemented, not verified`. If it fails,
report partial/blocked and do not check the affected AC or claim Implementation
Complete.

| Story Type | Required Evidence | Notes |
|---|---|---|
| **Logic** | Automated unit test at path from story's Test Evidence section | BLOCKING — included in Phase 4 agent brief |
| **Integration** | The one test or reasoned playtest path declared by the story | BLOCKING — do not choose a different alternative during implementation |
| **Visual/Feel** | Evidence doc at `production/qa/evidence/[slug]-evidence.md` | ADVISORY — note in Phase 6 summary |
| **UI** | Manual walkthrough doc or interaction test | ADVISORY — note in Phase 6 summary |
| **Config/Data** | None — smoke check serves as evidence | N/A |

For Visual/Feel and UI stories, include in the Phase 6 summary: "Manual evidence required at `production/qa/evidence/[slug]-evidence.md` before this story can be fully closed." This evidence is blocking for `$story-done` even though this implementation workflow does not create it; never summarize all AC as complete while it is absent.

---

## Phase 6: Collect and Summarise

After the programmer agent(s) complete, collect:

- Files created or modified (with paths)
- Test file created (path and number of test functions written)
- Any deviations from the story's Out of Scope boundary (flag these)
- Any questions or blockers the agent surfaced
- Any engine-specific risks the specialist flagged

Present a concise implementation summary:

```
## [Implemented and Verified | Implemented, Not Verified | Partial | Blocked]: [Story Title]

**Files changed**:
- `src/[path]` — created / modified ([brief description])
- `tests/[path]` — test file ([N] test functions)

**Acceptance criteria covered**:
- [x] [criterion] — actual passing test or directly checked non-automated evidence
- [ ] [criterion] — implemented but not verified / failing test
- [ ] [criterion] — DEFERRED: requires playtest (Visual/Feel)

**Deviations from scope**: [None] or [list files touched outside story boundary]
**Engine risks flagged**: [None] or [specialist finding]
**Blockers**: [None] or [describe]

**Verification**: [actual command and PASS/FAIL, or not run with reason].
This workflow leaves the story and sprint In Progress; it never marks Complete.
`$story-done` owns closure after the remaining evidence is verified.

Ready for: `$code-review [file1] [file2]` then `$story-done [story-path]`
```

---

## Phase 7: Update Session State

Within the already-authorized operation, update the existing current-task/STATUS
block in `production/session-state/active.md` and preserve unrelated content.
Do not append a second stale active-story block on every run:

```
## Session Extract — $dev-story [date]
- Story: [story-path] — [story title]
- Files changed: [comma-separated list]
- Test written: [path, or "None — Visual/Feel/Config story"]
- Blockers: [None, or description]
- Next: $code-review [files] then $story-done [story-path]
```

Create `active.md` if it does not exist. Confirm: "Session state updated."

---

## Error Recovery Protocol

If any spawned agent (through Codex subagent delegation) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** by asking the user directly with choices:
   - Keep the completed partial work and stop
   - Retry with narrower scope inside the authorized boundary
   - Stop and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. A
   blocked primary writer can never be skipped into a ready-for-review or
   complete summary; dependent work stops and affected AC remain unchecked.

Common blockers:
- Input file missing (story not found, GDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `$architecture-decision` first
- Scope too large → split into two stories via `$create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess
- Manifest version mismatch → show the diff; use current rules with an explicit
  planned version edit, or stop

## Collaborative Protocol

- **One primary writer** — one programmer role exclusively owns the authorized
  source/config and test files. Engine specialists are read-only unless the
  initial changeset assigned them a distinct non-overlapping file. The complete
  file set is authorized before status or implementation writes.
- **Load before implementing** — do not start coding until all context is loaded
  (story, TR-ID, ADR, manifest, engine prefs). Incomplete context produces code
  that drifts from design.
- **The ADR is the law** — implementation must follow the ADR's Implementation
  Guidelines. If the guidelines conflict with what seems "better," flag it in the
  summary rather than silently deviating.
- **Stay in scope** — the Out of Scope section is a contract. If implementing
  the story requires touching an out-of-scope file, stop and surface it:
  "Implementing [criterion] requires modifying [file], which is out of scope.
  Shall I proceed or create a separate story?"
- **Test is not optional for Logic/Integration** — do not mark implementation
  complete without the test file existing
- **Visual/Feel criteria are deferred, not skipped** — mark them as DEFERRED
  in the summary; they will be manually verified in `$story-done`
- **Ask before large structural decisions** — if the story requires an
  architectural pattern not covered by the ADR, surface it before implementing:
  "The ADR doesn't specify how to handle [case]. My plan is [X]. Proceed?"

---

## Recommended Next Steps

- Run `$code-review [file1] [file2]` to review the implementation before closing the story
- Run `$story-done [story-path]` to verify acceptance criteria and mark the story complete
- After all sprint stories are done: run `$team-qa sprint` for the full QA cycle before advancing the project stage
