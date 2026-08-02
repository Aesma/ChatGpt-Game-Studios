---
name: qa-plan
description: "Generate a QA test plan for a sprint or feature. Reads GDDs and story files, classifies stories by test type (Logic/Integration/Visual/UI), and produces a structured test plan covering automated tests required, manual test cases, smoke test scope, and playtest sign-off requirements. Run before sprint begins or when starting a major feature."
---

## Invocation and execution

Invoke this workflow as `$qa-plan`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[sprint | sprint-N | feature: system-name | story: path | epic: path]`. Treat bracketed values as optional unless the workflow says otherwise.

Delegate substantive work to the `qa-lead` Codex subagent role when it is available. If that role is unavailable, follow the same responsibilities in the current agent.


# QA Plan

This skill generates a structured QA plan for a sprint, feature, or individual
story. It reads all in-scope story files and their referenced GDDs, classifies
each story by test type, and produces a plan that tells developers exactly what
to automate, what to verify manually, what the smoke test scope is, and when
to bring in a playtester.

Run this before a sprint begins so the team knows upfront what testing work
is required. A test plan written after implementation is a post-mortem, not a
plan.

**Output:** `production/qa/qa-plan-[sprint-slug]-[date].md`

---

## Phase 1: Parse Scope

**Argument:** the provided arguments (blank = ask the user directly)

Determine scope from the argument:

- **`sprint`** — resolve the currently active sprint only from an existing
  active/status reference and verify the referenced sprint plan before
  extracting story paths. Never choose by filename order or modification time.
- **`sprint-N`** — resolve that exact sprint identifier in `production/sprints/`,
  then extract every referenced story path. For either sprint form, if
  `production/sprint-status.yaml` exists and identifies the same sprint, use it
  as the primary story list and fall back to the sprint plan for metadata. Do
  not use a status file for a different sprint.
- **`feature: [system-name]`** — match exact existing epic/story metadata,
  explicit parent-epic/system fields, and GDD references. Do not rely on a path
  or title substring alone. If several feature candidates remain, list their
  paths and identifying fields and ask the user to choose one.
- **`story: [path]`** — validate that the path exists and load that single file.
- **`epic: [path]` / Full epic** — validate the project-local epic path, read its
  existing story references, and load those story files.
- **No argument** — ask the user directly:
  - "What is the scope for this QA plan?"
  - Options: "Current sprint", "Specific feature (enter system name)",
    "Specific story (enter path)", "Full epic"

Reject unknown argument shapes. If the requested sprint, feature, story, or epic
cannot be resolved, or if resolution yields zero valid story files, stop with a
clear scope error and do not request or perform any write.

After resolving a non-empty scope, report: "Building QA plan for [N] stories in [scope]."

If a referenced story does not exist, record its exact path as `MISSING` and
continue with remaining stories. Retain a missing-path list and uncovered count
for the plan summary so the result cannot be mistaken for complete scope
coverage. If no valid story remains, stop.

---

## Phase 2: Load Inputs

For each in-scope story file, read the full file and extract:

- **Story title** and story ID (from filename or header)
- **Story Type** field (if present in the file header — e.g., `Type: Logic`)
- **Acceptance criteria** — the complete numbered/bulleted list
- **Implementation files** — listed under "Files to Create / Modify" or similar
- **Engine notes** — any engine API warnings or version-specific notes
- **GDD reference** — the GDD path(s) cited
- **ADR reference** — the ADR(s) cited
- **Estimate** — hours or story points if present
- **Dependencies** — other stories this one depends on

After reading stories, load supporting context once (not per story):

- `.codex/docs/coding-standards.md` — read the Testing Standards section as the
  authority for story types, required evidence, locations, and gate levels
- `design/gdd/systems-index.md` — to understand system priorities and which
  GDDs are approved
- For each unique GDD referenced across all stories: read the
  **Acceptance Criteria**, **Formulas**, and **Edge Cases** sections. Do not load
  the full GDD text. These three sections contain the testable requirements, the math
  to verify, and the boundary conditions that tests must cover. If an Edge Cases
  section is absent from the GDD, note it per GDD: "No Edge Cases section found — edge
  case coverage will be inferred from acceptance criteria only."
- `docs/architecture/control-manifest.md` — scan for forbidden patterns that
  automated tests should guard against (if the file exists)

If no GDD is referenced in a story, note it as a gap but do not block the plan.
The story will be classified using acceptance criteria alone.

---

## Phase 3: Classify Each Story

For each story, assign a Story Type:

- **If the story already has a `Type:` field in its header**: retain it as the
  declared input, then compare it with the acceptance-criteria indicators and
  the Testing Standards. If they conflict, report the declared and indicated
  types and the resulting evidence risk; do not silently rewrite the story.
- **If the `Type:` field is missing**: infer the type from the acceptance criteria using the table below, and note in the report that the type was inferred (not declared). Flag this as a gap — the story should have its Type declared explicitly before implementation begins.

| Story Type | Classification Indicators |
|---|---|
| **Logic** | Acceptance criteria reference calculations, formulas, numerical thresholds, state transitions, AI decisions, data validation, buff/debuff stacking, economy transactions, or any testable computation |
| **Integration** | Criteria involve two or more systems interacting, signals or events propagating across system boundaries, save/load round-trips, network sync, or persistence |
| **Visual/Feel** | Criteria reference animation behaviour, VFX, shader output, "feels responsive", perceived timing, screen shake, particle effects, audio sync, or visual feedback quality |
| **UI** | Criteria reference menus, HUD elements, buttons, screens, dialogue boxes, inventory panels, tooltips, or any player-facing interface element |
| **Config/Data** | Changes are limited to balance tuning values, data files, or configuration — no new code logic is involved |

**Mixed stories** (e.g., a story that adds both a formula and a UI display):
assign the primary type based on which acceptance criteria carry the highest
implementation risk, and note the secondary type. Mixed Logic+Integration or
Visual+UI combinations are the most common.

After classifying all stories, produce a classification summary table in
conversation before proceeding to Phase 4. This gives the user visibility into
how tests will be allocated.

For every story, derive the gate level only from its existing Type, Definition
of Done, and the Testing Standards. Record the level in the plan's ordinary
story notes or subsection text; do not add a new table column or schema.

---

## Phase 4: Generate Test Plan

Assemble the full QA plan document. Use this structure:

````markdown
# QA Plan: [Sprint/Feature Name]
**Date**: [date]
**Generated by**: $qa-plan
**Scope**: [N valid stories across N systems]
**Coverage gaps**: [N missing referenced stories; exact paths, or None]
**Engine**: [engine name from docs/technical-preferences.md, or "Not configured"]
**Sprint File**: [path to sprint plan if applicable]

---

## Test Summary

| Story | Type | Automated Test Required | Manual Verification Required |
|-------|------|------------------------|------------------------------|
| [story title] | Logic | Unit test — `tests/unit/[system]/` | None |
| [story title] | Integration | Integration test OR documented playtest | [documented playtest if used] |
| [story title] | Visual/Feel | None (not automatable) | Screenshot + lead sign-off in `production/qa/evidence/` |
| [story title] | UI | Interaction test (optional alternative) | Walkthrough doc in `production/qa/evidence/` OR interaction test |
| [story title] | Config/Data | Smoke check | Spot-check in-game values |

For each story, record its Testing Standards gate level in ordinary notes below
the table. UI interaction tests remain optional alternatives; never describe a
manual walkthrough as an automated test.

---

## Automated Tests Required

### [Story Title] — [Type]
**Gate level**: [BLOCKING / ADVISORY — derived from existing standards]
**Test file path**: `tests/[unit|integration]/[system]/[story-slug]_test.[ext]`
**What to test**:
- [Specific formula or rule from the GDD Formulas section]
- [Each named state transition or decision branch]
- [Each side effect that should or should not occur]

**Edge cases to cover**:
- Zero/minimum input values (e.g., 0 damage, empty inventory)
- Maximum/boundary input values (e.g., max level, stat cap)
- Invalid or null input (e.g., missing target, dead entity)
- [Any edge case explicitly called out in the GDD Edge Cases section]

**Estimated test count**: ~[N] unit tests

[If no GDD formula reference was found for this story, note:]
*No formula found in referenced GDD — test cases must be derived from acceptance
criteria directly. Review the GDD Formulas section before writing tests.*

---

## Manual QA Checklist

### [Story Title] — [Type]
**Verification method**: [Screenshot + designer sign-off | Playtest session |
Manual step-through | Comparison against reference footage]
**Who must sign off**: [designer / lead-programmer / qa-lead / art-lead]
**Evidence to capture**: [screenshot of X | video clip of Y | written playtest
notes | side-by-side comparison]
**Evidence location**: `production/qa/evidence/[story-slug]-evidence.md` for
Visual/Feel and UI evidence; only a true playtest session uses the session-log
path in the Playtest Requirements section.

Checklist:
- [ ] [Specific observable condition — concrete and falsifiable]
- [ ] [Another condition]
- [ ] [Every acceptance criterion translated into a manual check item]

*If any criterion uses subjective language ("feels", "looks", "seems"), it must
be supplemented with a specific benchmark or a playtest protocol note.*

---

## Smoke Test Scope

Critical paths to verify before any QA hand-off for this sprint:

1. Game launches to main menu without crash
2. New game / new session can be started
3. [Primary mechanic introduced or changed this sprint]
4. [Any system with a regression risk from this sprint's changes]
5. Save / load cycle completes without data loss (if save system exists)
6. Performance is within budget on target hardware (no new frame spikes)

*Smoke tests are verified by the developer via `$smoke-check`. Reference this
list when running that skill.*

---

## Playtest Requirements

| Story | Playtest Goal | Min Sessions | Target Player Type |
|-------|--------------|--------------|-------------------|
| [story] | [What question must the session answer?] | [N] | [new player / experienced] |

For a real playtest session, write notes to
`production/session-logs/playtest-[sprint]-[story-slug].md` and obtain the
specified review. Do not put ordinary Visual/Feel screenshots or UI walkthrough
evidence in session logs; those remain in `production/qa/evidence/`.

If no stories require playtest validation: *No playtest sessions required for
this sprint.*

---

## Required Evidence by Story

Apply each story's own Definition of Done plus the evidence required for its
type by the Testing Standards. This plan does not replace story DoD or create a
new uniform gate:

- **Logic**: passing automated unit test.
- **Integration**: passing integration test **or** documented playtest.
- **Visual/Feel**: screenshot plus lead sign-off in `production/qa/evidence/`.
- **UI**: walkthrough document or interaction test in the standard evidence location.
- **Config/Data**: applicable smoke-check pass.

Record code review, smoke, regression, and story-status requirements only when
they already appear in the story DoD or existing project standards.
````

When generating content, use the actual story titles, GDD formula text, and
acceptance criteria extracted in Phase 2. Do not use placeholder text — every
test entry should reflect the real requirements of these specific stories.

---

## Phase 5: Write Output

Resolve the exact output target before presenting the changeset. If it already
exists, read it and offer a targeted update or stop. Preserve every entry that
is outside the current scope and never overwrite the existing plan or invent a
new version name automatically.

Show the complete plan and the complete proposed changeset, including every plan
and story file that would be written, then ask the user both questions together:

```
question: "Ready to write the QA plan. Choose output options:"
allow multiple selections
options:
  - "Create/update QA plan at production/qa/qa-plan-[sprint-slug]-[date].md"
  - "Also back-fill test case specs into each story file's ## QA Test Cases section (Recommended — enables $dev-story and $code-review traceability)"
```

If the plan option is selected, apply the previewed create or targeted update
exactly as shown. If the story option is selected, for each in-scope story edit
only its `## QA Test Cases` section. If absent, append it before `## Test
Evidence`. Use manual verification steps for Visual/Feel and UI stories.

After writing, report the path, the valid-story count, the missing/uncovered
paths, and whether the operation created or updated the plan.

Next steps:
- Share this plan with the team before sprint implementation begins.
- Once all sprint stories are implemented, run `$smoke-check sprint` to gate QA
  hand-off — not yet, only after implementation is complete.
- Produce each story's required evidence before marking it done.

---

## Collaborative Protocol

- **Never write the plan without asking** — Phase 5 requires explicit approval.
- **Classify conservatively**: when a story is ambiguous between Logic and
  Integration, classify it as Integration — it requires both unit and
  integration consideration.
- **Do not invent test cases** beyond what acceptance criteria and GDD formulas
  support. If a formula is absent from the GDD, flag it rather than guessing.
- **Playtest requirements are advisory**: the user decides whether a playtest
  is warranted for borderline Visual/Feel stories. Flag the case; do not mandate.
- Ask the user directly for scope selection when no argument is provided.
  Keep all other phases non-interactive — present findings, then ask once to
  approve the write.
