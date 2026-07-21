---
name: create-stories
description: "Break a single epic into traceable story files. Fails closed: a story cannot be Ready without active stable TR-IDs and complete QA specifications, and unresolved traceability is routed to the registry-owning architecture-review workflow. Run after $create-epics for each epic."
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
**Next step after stories exist:** run `$story-readiness [story-path]` for a
`Ready` candidate; run `$dev-story [story-path]` only when readiness returns its
final `READY` verdict.

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
- `docs/architecture/control-manifest.md` — read the exact raw bytes, compute
  `sha256:<64 lowercase hexadecimal characters>`, extract the exact Manifest
  Version header, and preserve each applicable rule's `MUST`, `MUST NOT`,
  `SHOULD`, `SHOULD NOT`, or `MAY` strength plus contextual rejections and
  guardrails for this epic's layer
- `docs/architecture/tr-registry.yaml` — load all TR-IDs for this system

Parse the TR registry before decomposition and record its source status as
`loaded`, `missing`, `unreadable`, or `invalid`. Index only exact IDs matching
`TR-[system]-NNN`; an entry is usable only when it has `status: active`.

`$architecture-review` is the sole workflow that assigns or repairs registry
IDs. `$create-stories` is a registry consumer: it must never create, guess,
renumber, or edit a TR-ID or the registry. A registry source failure does not
stop the draft; it makes every affected story `Blocked` and is included in the
traceability gap report in Step 5.

**ADR existence validation**: After reading the governing ADRs list from the epic, confirm each ADR file exists on disk. If any ADR file cannot be found, **stop immediately** before decomposing any story:

> "Epic references [ADR-NNNN: title] but `docs/architecture/[adr-file].md` was not found.
> Check the filename in the epic's Governing ADRs list, or run `$architecture-decision`
> to create it. Cannot create stories until all referenced ADR files are present."

Do not proceed to Step 3 until all referenced ADR files are confirmed present.

Report: "Loaded epic [name], GDD [filename], [N] governing ADRs (all confirmed present), control manifest v[version], sha256:[hash]."

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

Mixed stories: assign the type that carries the highest implementation risk.
The type determines what test evidence is required before `$story-done` can close the story.

---

## 4. Decompose the GDD into Stories

For each GDD acceptance criterion:

1. Group related criteria that require the same core implementation
2. Each group = one story
3. Order stories: foundational behaviour first, edge cases last, UI last
4. Assign each criterion a story-local stable ID such as `AC-S001-01`.
   Preserve that ID when wording or order changes; never recycle it for a
   different criterion.

**Story sizing rule:** one story = one focused session (~2-4 hours). If a
group of criteria would take longer, split into two stories.

For each story, determine:
- **GDD requirement**: which acceptance criterion(ia) does this satisfy?
- **TR-ID**: map every covered GDD requirement and acceptance criterion to an
  exact registry entry with `status: active`.
  - Exact active match → embed the stable ID unchanged.
  - No match, ambiguous match, malformed ID, unknown ID, non-active entry, or
    unavailable registry → do **not** invent or emit a replacement ID. Set the
    story status to `Blocked`, record the source requirement and GDD location in
    the story's `Traceability Gaps`, and add it to the batch gap report for
    `$architecture-review`.
  - If a story covers several requirements, every one must resolve. One
    unresolved requirement blocks that story; it does not change unrelated
    stories.
  - `TR-[system]-???` and every other placeholder TR value are forbidden in
    previews and written files.
- **Governing ADR**: which ADR governs how to implement this?
  - `Status: Accepted` → embed normally
  - `Status: Proposed` → set story `Status: Blocked` with note: "BLOCKED: ADR-NNNN is Proposed — run `$architecture-decision` to advance it"
  - **Multiple ADRs apply**: List all governing ADRs in the story's `Governing ADRs:` field. Designate the one most directly controlling the implementation pattern as primary (first in the list). Others are listed as secondary references.
  - **No ADR applies at all**: Write `ADR: N/A — [brief reason, e.g. "pure data configuration, no architectural pattern required"]` in the story's ADR field. Do NOT leave the field blank — a blank ADR field means "not checked", not "not applicable".
- **Story Type**: from Step 3 classification
- **Engine risk**: from the ADR's Knowledge Risk field

---

## 4b. QA Lead Story Readiness Gate

**Review mode check** — apply before spawning QL-STORY-READY:
- `solo` → skip. Note: "QL-STORY-READY skipped — Solo mode." Continue with QA
  specification coverage below; skipping the gate does not waive test specs.
- `lean` → skip (not a PHASE-GATE). Note: "QL-STORY-READY skipped — Lean mode."
  Continue with QA specification coverage below; skipping the gate does not
  waive test specs.
- `full` → spawn as normal.

After decomposing all stories (Step 4 complete) but before presenting them for single changeset approval, spawn `qa-lead` through Codex subagent delegation using gate **QL-STORY-READY** (`.codex/docs/director-gates.md`). Request one capped batch review, but require a separate verdict for every story.

Pass: the full story list with acceptance criteria, story types, and TR-IDs; the epic's GDD acceptance criteria for reference.

Present the QA lead's assessment and keep the result attached to its story.
`ADEQUATE` does not change the deterministic status; `GAPS` makes the story at
least `Needs Work`; `INADEQUATE` makes it `Blocked`. A stricter pre-existing
status remains. Revise when the user chooses to do so, but never convert a QA
failure to `Ready` by accepting risk.

**Before generating test specs**: A QA plan may be imported only by an explicit,
canonical project-relative plan path selected by the user or referenced by the
epic. Never select a plan by modification time, title text, slug text, or a
"latest" filename. Read the complete plan bytes and compute its SHA-256. Parse
its declared state, source manifest, story bindings, stable AC IDs, and stable
test/check IDs.

Before offering an import, re-read and hash every source path captured by the QA
plan. The plan is usable only when all of the following are true:

- its declared and effective state are both `CURRENT`, never `PARTIAL` or
  `STALE`;
- every captured source path is readable and its current raw-byte hash exactly
  matches the plan manifest;
- each candidate story is identified by its canonical path and its candidate
  byte hash, not by title or slug;
- the plan's stable AC IDs exactly equal the story's stable AC IDs; and
- every imported test/check ID is unique and bound to exactly one matching AC.

If any check fails, report the exact provenance or binding gap, do not import
any affected specification, and keep that story at least `Needs Work` until a
current QA plan is regenerated or fresh specifications are produced. User risk
acceptance cannot make a `PARTIAL` or `STALE` plan current.

If a current, exact matching plan exists:
- Ask the user directly:
  - Prompt: "A QA plan exists at [path] with test specs for some of these stories. How do you want to proceed?"
  - Options:
    - `Use existing specs from the QA plan — embed them into the story files (Recommended)`
    - `Ask qa-lead to generate fresh specs — override the QA plan`
    - `Defer test specs — write affected stories as Needs Work`
- If "Use existing specs": copy only the exact specifications whose stable
  IDs and AC bindings passed the checks above. Record `QA Plan Path`, `QA Plan
  Hash`, `QA Plan State: CURRENT`, and the imported IDs in the story's
  `## QA Test Cases` section. No qa-lead spawn is needed for those exact covered
  criteria. Spawn qa-lead only for criteria with no current exact coverage.
- If "Generate fresh": proceed with the qa-lead spawn below as normal.
- If "Defer": record `QA Coverage: Missing`, list the uncovered AC IDs, and
  set each affected story to `Needs Work` unless it is already `Blocked`. This
  option authorizes writing a non-ready planning artifact only; it never makes
  the story implementation-ready.

**After ADEQUATE, a skipped readiness gate, or qa-plan import**: for every Logic and Integration
story, require one concrete automated test specification per acceptance
criterion. Each specification must have a stable, non-placeholder ID in the
form `TC-[epic-slug]-S[story-number]-AC[criterion-number]`; preserve an existing
ID when revising a story and never renumber IDs merely because wording or order
changes. Use this format:

```
Test ID: TC-[epic-slug]-S[story-number]-AC[criterion-number]
Test: [criterion text]
  Given: [precondition]
  When: [action]
  Then: [expected result / assertion]
  Edge cases: [boundary values or failure states to test]
```

For Visual/Feel and UI stories, produce manual verification steps instead. Give
each check a stable ID in the form
`MC-[epic-slug]-S[story-number]-AC[criterion-number]`:
```
Manual Check ID: MC-[epic-slug]-S[story-number]-AC[criterion-number]
Manual check: [criterion text]
  Setup: [how to reach the state]
  Verify: [what to look for]
  Pass condition: [unambiguous pass description]
```

For Config/Data stories, require a stable smoke-check ID and an observable pass
condition. These specifications are embedded directly into each story's
`## QA Test Cases` section. The developer implements against them.

A QA specification is complete only when its stable ID and every field required
for that story type contain concrete values. Blank values and markers such as
`TBD`, `TODO`, `???`, or "fill later" count as missing coverage. Match
specifications to the stable AC IDs, not only to mutable criterion text or order.

### 4c. Compute Story Status (fail closed)

Compute `story_status` for each story before previewing or rendering any file.
Use the strictest applicable result (`Blocked` > `Needs Work` > `Ready`):

- `Blocked` — any covered requirement lacks an exact active TR-ID; the registry
  is missing/unreadable/invalid; a governing ADR is missing or Proposed; or the
  full-mode QA gate returns `INADEQUATE` or no valid verdict.
- `Needs Work` — no blocker exists, but any acceptance criterion lacks its
  required complete QA specification or stable test/manual-check ID; QA specs
  were deferred; or the full-mode QA gate returns `GAPS`.
- `Ready` — every covered requirement maps to an exact active TR-ID, all ADR
  checks pass, every acceptance criterion has its required complete QA
  specification and stable ID, and the applicable QA gate does not downgrade
  the result.

Never use a template default to set status. Keep the same computed status in the
preview, story header, EPIC table, and completion summary. `Ready` in this skill
means eligible for `$story-readiness`; that downstream workflow still makes the
authoritative implementation-readiness decision.

---

## 5. Present Stories for Review

Before writing any files, present the full story list:

```
## Stories for Epic: [name]

Story 001: [title] — Logic — ADR-NNNN
  Status: [Ready | Needs Work | Blocked]
  Covers: TR-[system]-001 ([1-line summary of requirement])
  QA coverage: [complete | missing AC-N, ...]
  Test required: tests/unit/[system]/[slug]_test.[ext]

Story 002: [title] — Integration — ADR-MMMM
  Status: [Ready | Needs Work | Blocked]
  Covers: TR-[system]-002, TR-[system]-003
  QA coverage: [complete | missing AC-N, ...]
  Test required: tests/integration/[system]/[slug]_test.[ext]

Story 003: [title] — Visual/Feel — ADR-NNNN
  Status: [Ready | Needs Work | Blocked]
  Covers: TR-[system]-004
  QA coverage: [complete | missing AC-N, ...]
  Evidence required: production/qa/evidence/[slug]-evidence.md

[N stories total: N Logic, N Integration, N Visual/Feel, N UI, N Config/Data]

### Traceability Gaps — route to `$architecture-review`
- [Story NNN / GDD path + section / requirement text / reason unresolved]
```

Omit the Traceability Gaps section only when there are no gaps. The report is an
ownership handoff, not permission for this skill to edit the registry. Confirm
that the preview contains no `TR-...-???` or other placeholder TR value before
asking for changeset authorization.

Ask the user directly:
- Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.
- Options: `[A] Yes — write all [N] stories` / `[B] Not yet — I want to review or adjust first`

---

## 6. Write Story Files

For each story, write `production/epics/[epic-slug]/story-[NNN]-[slug].md`:

```markdown
# Story [NNN]: [title]

> **Epic**: [epic name]
> **Status**: [story_status — Ready | Needs Work | Blocked]
> **Layer**: [Foundation / Core / Feature / Presentation]
> **Type**: [Logic | Integration | Visual/Feel | UI | Config/Data]
> **Estimate**: [hours or t-shirt size — fill before sprint planning]
> **Manifest Version**: [date from control-manifest.md header]
> **Manifest Hash**: sha256:[hash of exact current control-manifest.md bytes]
> **Last Updated**: [set by $dev-story when implementation begins]

## Context

**GDD**: `design/gdd/[filename].md`
**Requirement**: [one or more exact active `TR-[system]-NNN` values, or `Unresolved — see Traceability Gaps`]
*(Requirement text lives in `docs/architecture/tr-registry.yaml` — read fresh at review time)*

**Traceability Gaps**: [None | GDD path + section, unresolved requirement text, and reason]

**ADR Governing Implementation**: [ADR-NNNN: title]
**ADR Decision Summary**: [1-2 sentence summary of what the ADR decided]

**Engine**: [name + version] | **Risk**: [LOW / MEDIUM / HIGH]
**Engine Notes**: [from ADR Engine Compatibility section — post-cutoff APIs, verification required]

**Control Manifest Rules (this layer)**:
- MUST / MUST NOT: [applicable mandatory rules, preserving conditions]
- SHOULD / SHOULD NOT: [applicable recommendations, preserving conditions]
- MAY: [applicable permitted options]
- Contextual Rejections: [rejected alternatives and reconsideration conditions; not prohibitions]
- Guardrail: [relevant performance guardrail]

## Source Snapshot

- `docs/architecture/control-manifest.md`: `sha256:[same exact hash as the header]`

---

## Acceptance Criteria

*From GDD `design/gdd/[filename].md`, scoped to this story:*

- [ ] **AC-S[story-number]-01**: [criterion 1 — directly from GDD]
- [ ] **AC-S[story-number]-02**: [criterion 2]
- [ ] **AC-S[story-number]-03**: [performance criterion if applicable]

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

**QA Coverage**: [Complete | Missing — AC IDs]

**[For Logic / Integration stories — automated test specs]:**

- **TC-[epic-slug]-S[story-number]-AC[criterion-number]** — **AC-S[story-number]-[criterion-number]**: [criterion text]
  - Given: [precondition]
  - When: [action]
  - Then: [assertion]
  - Edge cases: [boundary values / failure states]

**[For Visual/Feel / UI stories — manual verification steps]:**

- **MC-[epic-slug]-S[story-number]-AC[criterion-number]** — **AC-S[story-number]-[criterion-number]**: [criterion text]
  - Setup: [how to reach the state]
  - Verify: [what to look for]
  - Pass condition: [unambiguous pass description]

---

## Test Evidence

**Story Type**: [type]
**Required evidence**:
- Logic: `tests/unit/[system]/[story-slug]_test.[ext]` — must exist and pass
- Integration: `tests/integration/[system]/[story-slug]_test.[ext]` OR playtest doc
- Visual/Feel: `production/qa/evidence/[story-slug]-evidence.md` + sign-off
- UI: `production/qa/evidence/[story-slug]-evidence.md` or interaction test
- Config/Data: smoke check pass (`production/qa/smoke-*.md`)

**Status**: [ ] Not yet created

---

## Dependencies

- Depends on: [Story NNN-1 must be DONE, or "None"]
- Unlocks: [Story NNN+1, or "None"]
```

### Also update `production/epics/[epic-slug]/EPIC.md`

Replace the "Stories: Not yet created" line with a populated table:

```markdown
## Stories

| # | Story | Type | Status | ADR |
|---|-------|------|--------|-----|
| 001 | [title] | Logic | [story_status] | ADR-NNNN |
| 002 | [title] | Integration | [story_status] | ADR-MMMM |
```

### Also update `production/epics/index.md`

Find the row in the index table matching this epic (by epic name or slug). Update its `Stories` column from `Not yet created` to `[N] stories` (where N is the count just written). If the index file does not exist, skip silently.

---

## 7. After Writing

Ask the user directly to close with context-aware next steps:

Check:
- Are there other epics in `production/epics/` without stories yet? List them.
- Is this the last epic? If so, include `$sprint-plan` as an option.
- Which written stories are `Needs Work` or `Blocked`? Do not offer
  `$dev-story` for those stories. Route missing TR work to
  `$architecture-review` and missing QA coverage to `$qa-plan`.

Structured prompt:
- Prompt: "[N] stories written to `production/epics/[epic-slug]/`. What next?"
- Options (include all that apply):
  - `[A] Validate the first Ready story — run $story-readiness [first-ready-story-path]` (Recommended; only if a Ready story exists)
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
6. **Fail closed** — never invent TR-IDs, never render a status constant, and never label missing QA coverage Ready
7. **Never start implementation** — this skill stops at the story file level

After writing (or declining):

- **Verdict: COMPLETE** — [N] stories written to `production/epics/[epic-slug]/`: [R] Ready, [W] Needs Work, [B] Blocked. Run `$story-readiness` only for a Ready candidate; `$dev-story` is allowed only after the downstream final verdict is READY.
- **Verdict: NEEDS WORK** — stories were written, but none is currently Ready and no hard blocker exists. Resolve the listed QA coverage gaps with `$qa-plan`, then rerun `$create-stories`.
- **Verdict: BLOCKED** — one or more stories have traceability, ADR, or full-mode QA blockers. The written files remain planning artifacts; route TR registry gaps to `$architecture-review` and do not run `$dev-story` for them.
- **Verdict: BLOCKED** — user declined. No story files written.
