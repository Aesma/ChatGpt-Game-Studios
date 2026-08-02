---
name: create-stories
description: "Break a single epic into implementable story files. Reads the epic, its GDD, governing ADRs, and control manifest. Each story embeds its GDD requirement TR-ID, ADR guidance, acceptance criteria, story type, and test evidence path. Run after $create-epics for each epic."
---

## Invocation and execution

Invoke this workflow as `$create-stories`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[epic-slug | epic-path] [--review full|lean|solo]`. Treat bracketed values as optional unless the workflow says otherwise.

Delegate substantive work to the `lead-programmer` Codex subagent role when it is available. If that role is unavailable, follow the same responsibilities in the current agent.


# Create Stories

A story is a single implementable behaviour — small enough to complete in one
focused session, self-contained, and fully traceable to a GDD requirement and
an ADR decision. Stories are what developers pick up. Epics are what architects
define.

**Run this skill per epic**, not per layer. Run it for Foundation epics first,
then Core, and so on — matching the dependency order.

**Output:** `production/epics/[epic-slug]/story-NNN-[slug].md` files

**Previous step:** `$create-epics [system]`
**Next step after stories exist:** `$story-readiness [story-path]` then `$dev-story [story-path]`

---

## 1. Parse Argument

Extract `--review [full|lean|solo]` if present and store as the review mode
override for this run. If not provided, read `production/review-mode.txt`
(default `lean` if missing). This resolved mode applies to all gate spawns
in this skill — apply the check pattern from `.codex/docs/director-gates.md`
before every gate invocation.

- `$create-stories [epic-slug]` — e.g. `$create-stories combat`
- `$create-stories production/epics/combat/EPIC.md` — full path also accepted
- No argument — ask: "Which epic would you like to break into stories?"
  Find files matching `production/epics/*/EPIC.md` and list available epics with their status.

---

## 2. Load Everything for This Epic

Read in full:

- `production/epics/[epic-slug]/EPIC.md` — epic overview, governing ADRs, GDD requirements table
- The epic's GDD (`design/gdd/[filename].md`) — read all 8 sections, especially Acceptance Criteria, Formulas, and Edge Cases
- All governing ADRs listed in the epic — read the Decision, Implementation Guidelines, Engine Compatibility, and Engine Notes sections
- `docs/architecture/control-manifest.md` — extract rules for this epic's layer;
  require the positive integer Manifest Version from the header
- `docs/architecture/tr-registry.yaml` — load all TR-IDs for this system

Validate each required input separately before decomposition: the EPIC, every
mapped GDD, control manifest, and TR registry must exist and be readable. Report
all missing inputs with the existing upstream workflow that produces them and
stop before producing any Ready story.

**ADR existence validation**: After reading the governing ADRs list from the epic, confirm each ADR file exists on disk. If any ADR file cannot be found, **stop immediately** before decomposing any story:

> "Epic references [ADR-NNNN: title] but `docs/architecture/[adr-file].md` was not found.
> Check the filename in the epic's Governing ADRs list, or run `$architecture-decision`
> to create it. Cannot create stories until all referenced ADR files are present."

Do not proceed to Step 3 until all referenced ADR files are confirmed present.

Report: "Loaded epic [name], GDD [filename], [N] governing ADRs (all confirmed present), control manifest v[date]."

---

## 3. Classify Stories by Type

**Story Type Classification** — assign each story a type based on its acceptance criteria:

| Story Type | Assign when criteria reference... |
|---|---|
| **Logic** | Formulas, numerical thresholds, state transitions, AI decisions, calculations |
| **Integration** | Two or more systems interacting, signals crossing boundaries, save/load round-trips |
| **Visual/Feel** | Animation behaviour, VFX, "feels responsive", timing, screen shake, audio sync |
| **UI** | Menus, HUD elements, buttons, screens, dialogue boxes, tooltips |
| **Config/Data** | Balance tuning values, data file changes only — no new code logic |

Mixed stories: first split independently verifiable criteria when that produces
coherent stories. If criteria cannot be split, use this fixed risk precedence:
Integration > Logic > UI > Visual/Feel > Config/Data. Show the chosen type and
reason in the preview. The type determines the one evidence requirement used by
`$story-done`.

---

## 4. Decompose the GDD into Stories

For each GDD acceptance criterion:

1. Group related criteria that require the same core implementation
2. Each group = one story
3. Order stories: foundational behaviour first, edge cases last, UI last

**Story sizing rule:** one story = one focused session (~2-4 hours). If a
group of criteria would take longer, split into two stories.

For each story, determine:
- **GDD requirement**: which acceptance criterion(ia) does this satisfy?
- **TR-ID**: look up the stable ID in `tr-registry.yaml`. If no stable
  match exists, set the story Status to `Blocked`, report the missing trace in
  the pre-write preview, and do not write a `???` identifier.
- **ADR references / Governing ADRs**:
  - List every applicable real ADR exactly once and mark exactly one item
    explicitly `primary`; do not use list order as an implicit primary marker.
  - Record each referenced ADR's actual Status. Any Proposed or otherwise
    non-Accepted reference makes the story `Blocked` with the specific reason.
  - The only valid N/A form is a Config/Data story whose reference list contains
    exactly one `N/A — [specific reason]` item. The reason must be non-empty,
    non-blank, and not `TBD` or another placeholder. N/A may not be mixed with
    a real ADR. Any invalid N/A form makes the story Blocked before writing.
- **Story Type**: from Step 3 classification
- **Engine risk**: from the ADR's Knowledge Risk field

---

## 4b. QA Lead Story Readiness Gate

**Review mode check** — apply before spawning QL-STORY-READY:
- `solo` → skip. Note: "QL-STORY-READY skipped — Solo mode." Proceed to Step 5 (present stories for review).
- `lean` → skip (not a PHASE-GATE). Note: "QL-STORY-READY skipped — Lean mode." Proceed to Step 5 (present stories for review).
- `full` → spawn as normal.

After decomposing all stories (Step 4 complete) but before presenting them for single changeset approval, spawn `qa-lead` through Codex subagent delegation using gate **QL-STORY-READY** (`.codex/docs/director-gates.md`).

For each story, pass its planned final path and complete inline story draft,
including its current Status, acceptance criteria, type, TR-ID, ADR reference
list with explicit primary, QA cases, and evidence path. Also pass the epic GDD
criteria. The planned path is not an existing file; no story may be written
before this gate returns a per-story verdict.

Present the QA lead's assessment per story. `INADEQUATE` blocks Ready and must be
revised or left out. For `GAPS`, let the user choose: revise and re-review, or
accept the gap and write that story with its existing Blocked/Needs Work status.
A GAPS story may never be written Ready. Proceed when each story is ADEQUATE or
has an explicitly accepted non-Ready gap.

**Before generating test specs**: Find files matching `production/qa/qa-plan-*.md` for the most recently modified file. If found, read it and check whether it contains test case specifications for the stories in this epic (look for story titles or slugs in the plan's Automated Tests Required section). If matching specs exist:
- Ask the user directly:
  - Prompt: "A QA plan exists at [path] with test specs for some of these stories. How do you want to proceed?"
  - Options:
    - `Use existing specs from the QA plan — embed them into the story files (Recommended)`
    - `Generate fresh specs under the resolved review mode — full may use qa-lead; lean/solo use an unreviewed current-agent draft`
    - `Skip test spec generation — I'll fill in ## QA Test Cases manually`
- If "Use existing specs": extract the test case specs from the qa-plan for each matching story and embed them directly into the `## QA Test Cases` section. No qa-lead spawn is needed for covered stories; uncovered stories follow the resolved mode below.
- If "Generate fresh": follow the resolved-mode behavior below; do not bypass it.
- If "Skip": leave `## QA Test Cases` with a placeholder: `*Test cases not yet defined — run $qa-plan to generate them.*`

**After ADEQUATE** (or after qa-plan import): in full mode, qa-lead may produce
the concrete test cases. In lean or solo, do not spawn qa-lead after claiming
the gate was skipped; reuse existing QA-plan content first, then have the current
agent derive an explicitly unreviewed draft from approved GDD acceptance
criteria. For every Logic and Integration story, use this format:

```
Test: [criterion text]
  Given: [precondition]
  When: [action]
  Then: [expected result / assertion]
  Edge cases: [boundary values or failure states to test]
```

For Visual/Feel and UI stories, produce manual verification steps instead:
```
Manual check: [criterion text]
  Setup: [how to reach the state]
  Verify: [what to look for]
  Pass condition: [unambiguous pass description]
```

These test case specs are embedded directly into each story's `## QA Test Cases` section. The developer implements against these cases. The programmer does not write tests from scratch — QA has already defined what "done" looks like.

---

## 5. Present Stories for Review

Before writing any files, scan the target epic directory. Preserve existing
stories and allocate each new story the next available numeric identifier.
When an existing title or TR-ID matches a proposed story, show its scoped diff
and ask `update` or `skip`; never overwrite it as a new 001 sequence.

Before writing any files, present the full story list:

```
## Stories for Epic: [name]

Story 001: [title] — Logic — ADR-NNNN
  Covers: TR-[system]-001 ([1-line summary of requirement])
  Test required: tests/unit/[system]/[slug]_test.[ext]

Story 002: [title] — Integration — ADR-MMMM
  Covers: TR-[system]-002, TR-[system]-003
  Test required: tests/integration/[system]/[slug]_test.[ext]

Story 003: [title] — Visual/Feel — ADR-NNNN
  Covers: TR-[system]-004
  Evidence required: production/qa/evidence/[slug]-evidence.md

[N stories total: N Logic, N Integration, N Visual/Feel, N UI, N Config/Data]
```

Ask the user directly:
- Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.
- Options: `[A] Yes — write all [N] stories` / `[B] Not yet — I want to review or adjust first`

---

## 6. Write Story Files

For each story, write `production/epics/[epic-slug]/story-[NNN]-[slug].md`:

```markdown
# Story [NNN]: [title]

> **Epic**: [epic name]
> **Status**: [computed Ready or Blocked — never hard-code Ready]
> **Layer**: [Foundation / Core / Feature / Presentation]
> **Type**: [Logic | Integration | Visual/Feel | UI | Config/Data]
> **Estimate**: [hours or t-shirt size — fill before sprint planning]
> **Manifest Version**: [positive integer from control-manifest.md header]
> **Last Updated**: [set by $dev-story when implementation begins]

## Context

**GDD**: `design/gdd/[filename].md`
**Requirement**: `TR-[system]-NNN`
*(Requirement text lives in `docs/architecture/tr-registry.yaml` — read fresh at review time)*

**ADR references / Governing ADRs**:
- `ADR-NNNN: title` — **primary** — Status: [Accepted/Proposed/...]
- `ADR-MMMM: title` — secondary — Status: [Accepted/Proposed/...]
- or, for the sole valid exception: `N/A — [specific non-placeholder reason]`

**Primary ADR Decision Summary**: [1-2 sentence summary]
**Secondary ADR Constraints**: [meaning-preserving constraints from each secondary reference]

**Engine**: [name + version] | **Risk**: [LOW / MEDIUM / HIGH]
**Engine Notes**: [from ADR Engine Compatibility section — post-cutoff APIs, verification required]

**Control Manifest Rules (this layer)**:
- Required: [relevant required pattern]
- Forbidden: [relevant forbidden pattern]
- Guardrail: [relevant performance guardrail]

---

## Acceptance Criteria

*From GDD `design/gdd/[filename].md`, scoped to this story:*

- [ ] [criterion 1 — directly from GDD]
- [ ] [criterion 2]
- [ ] [performance criterion if applicable]

---

## Implementation Notes

*Derived from ADR-NNNN Implementation Guidelines:*

[Specific, actionable guidance from the ADR. Do not paraphrase in ways that
change meaning. This is what the programmer reads instead of the ADR.]

---

## Out of Scope

*Handled by neighbouring stories — do not implement here:*

- [Story NNN+1]: [what it handles]

---

## QA Test Cases

*Written by qa-lead at story creation. The developer implements against these — do not invent new test cases during implementation.*

**[For Logic / Integration stories — automated test specs]:**

- **AC-1**: [criterion text]
  - Given: [precondition]
  - When: [action]
  - Then: [assertion]
  - Edge cases: [boundary values / failure states]

**[For Visual/Feel / UI stories — manual verification steps]:**

- **AC-1**: [criterion text]
  - Setup: [how to reach the state]
  - Verify: [what to look for]
  - Pass condition: [unambiguous pass description]

---

## Test Evidence

**Story Type**: [type]
**Required evidence**: [exactly one line selected from the story type]
- Logic → `tests/unit/[system]/[story-slug]_test.[ext]` — must exist and pass
- Integration → `tests/integration/[system]/[story-slug]_test.[ext]` by default;
  use one documented playtest path only when a GDD AC is inherently end-to-end
  manual, and record that reason
- Visual/Feel → `production/qa/evidence/[story-slug]-evidence.md` + sign-off
- UI → one manual evidence path or interaction test chosen in the draft
- Config/Data → one applicable smoke-check result path

Delete the unused type examples from the final story. A consumer must see one
unambiguous path/alternative, not all five.

**Status**: [ ] Not yet created

---

## Dependencies

- Depends on: [Story NNN-1 must be DONE, or "None"]
- Unlocks: [Story NNN+1, or "None"]
```

### Also update `production/epics/[epic-slug]/EPIC.md`

Locate exactly one existing `> **Stories**: Not yet created` metadata field (or
its already-populated Stories section for an update) and replace only that
field/section. If no unique target exists, stop this EPIC edit and report the
partial result; do not rewrite the whole EPIC.

Replace the field with a populated table:

```markdown
## Stories

| # | Story | Type | Status | ADR |
|---|-------|------|--------|-----|
| 001 | [title] | Logic | Ready | ADR-NNNN |
| 002 | [title] | Integration | Ready | ADR-MMMM |
```

### Also update `production/epics/index.md`

Find the unique row in the index table matching this epic (by epic name or
slug). Update its `Stories` column from `Not yet created` to `[N] stories`
(where N is the total preserved plus newly written). If the index is missing or
has zero/multiple matching rows, report that synchronization did not occur and
call the story files/EPIC edit a partial result; never skip silently or rebuild
unrelated rows.

---

## 7. After Writing

Ask the user directly to close with context-aware next steps:

Check:
- Are there other epics in `production/epics/` without stories yet? List them.
- Is this the last epic? If so, include `$sprint-plan` as an option.

Structured prompt:
- Prompt: "[N] stories written to `production/epics/[epic-slug]/`. What next?"
- Options (include all that apply):
  - `[A] Start implementing — run $story-readiness [first-story-path]` (Recommended)
  - `[B] Create stories for [next-epic-slug] — run $create-stories [slug]` (only if other epics have no stories yet)
  - `[C] Plan the sprint — run $sprint-plan new` (only if all epics have stories)
  - `[D] Stop here for this session`

Note in output: "Work through stories in order — each story's `Depends on:` field tells you what must be DONE before you can start it."

---

## Collaborative Protocol

1. **Read before presenting** — load all inputs silently before showing the story list
2. **Ask once** — present all stories for the epic in one summary, not one at a time
3. **Warn on blocked stories** — flag any story with a Proposed ADR before writing
4. **Single changeset approval** — preview the full story set and write it only after the one approval
5. **No invention** — acceptance criteria come from GDDs, implementation notes from ADRs, rules from the manifest
6. **Never start implementation** — this skill stops at the story file level

After writing (or declining):

- **Verdict: COMPLETE** — [N] stories written to `production/epics/[epic-slug]/`. Run `$story-readiness` → `$dev-story` to begin implementation.
- **Verdict: BLOCKED** — user declined. No story files written.
