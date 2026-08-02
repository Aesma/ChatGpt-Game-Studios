---
name: story-readiness
description: "Validate that a story file is implementation-ready. Checks for embedded GDD requirements, ADR references, engine notes, clear acceptance criteria, and no open design questions. Produces READY / NEEDS WORK / BLOCKED verdict with specific gaps. Use when user says 'is this story ready', 'can I start on this story', 'is story X ready to implement'."
---

## Invocation and execution

Invoke this workflow as `$story-readiness`.

Arguments: `[story-file-path | all | sprint] [--review full|lean|solo]`.
Treat bracketed values as optional unless the workflow says otherwise. Validate
the complete list first: accept one scope and one review flag only; reject
unknown flags, duplicate scopes, and invalid review values before reading files.


# Story Readiness

This skill validates that a story file contains everything a developer needs
to begin implementation — no mid-sprint design interruptions, no guessing,
no ambiguous acceptance criteria. Run it before assigning a story.

**This skill is read-only.** It never edits story files. It reports findings
and asks whether the user wants help filling gaps.

**Output:** Verdict per story (READY / NEEDS WORK / BLOCKED) with a specific
gap list for each non-ready story.

---

## Phase 0: Resolve Review Mode

Resolve the review mode once at startup (store for all gate spawns this run):

1. If skill was called with `--review [full|lean|solo]` → use that value
2. Else read `production/review-mode.txt` → use that value
3. Else → default to `lean`

See `.codex/docs/director-gates.md` for the full check pattern and mode definitions.

---

## 1. Parse Arguments

**Scope:** the first provided argument (blank = ask the user directly)

- **Specific path** (e.g., `$story-readiness production/epics/combat/story-001-basic-attack.md`):
  require an existing regular Markdown file inside `production/epics/` with a
  story title/ID and Status header. Reject directories, outside paths, indexes,
  README/notes, and non-story Markdown.
- **`sprint`**: read the current sprint plan from `production/sprints/` (most
  recent file), extract every story path it references, validate each one.
- **`all`**: find files matching `production/epics/**/*.md`, then retain only
  regular Markdown files with a story title/ID and Status header. Exclude
  `EPIC.md`, README, indexes, notes, and every non-story file; report skipped
  paths.
- **No argument**: ask the user which scope to validate.

If no argument is given, ask the user directly:
- "What would you like to validate?"
  - Options: "A specific story file", "All stories in the current sprint",
    "All stories in production/epics/", "Stories for a specific epic"

Report the scope before proceeding: "Validating [N] story files."

---

## 2. Load Supporting Context

Before checking any stories, load reference documents once (not per-story):

- `design/gdd/systems-index.md` — to know which systems have approved GDDs
- `docs/architecture/control-manifest.md` — to know which manifest rules exist
  (if the file does not exist, note it as missing once; do not re-flag per story)
  Also extract the positive integer `Manifest Version:` from the header block if
  the file exists.
- `docs/architecture/tr-registry.yaml` — index all entries by `id`. Used to
  validate TR-IDs in stories. If the file is missing or cannot be parsed, note
  it once. Any story that declares a TR-ID is BLOCKED because the requirement
  cannot be validated; never assume the story predates tracking.
- All ADR status fields — for each unique ADR referenced across the stories being
  checked, read the ADR file and note its `Status:` field. Cache these so you
  don't re-read the same ADR for every story.
- Every unique GDD/quick-design document referenced by an input story. Resolve
  the cited section/anchor or quoted requirement and confirm it exists in that
  file; filename presence alone is insufficient.
- The current sprint file (if scope is `sprint`) — to identify Must Have /
  Should Have priority for escalation decisions

---

## 3. Story Readiness Checklist

For each story file, evaluate every item below. A story is READY only if all
items pass or are explicitly marked N/A with a stated reason.

### Design Completeness

- [ ] **Systems index support**: if a story claims its system GDD is approved,
  `design/gdd/systems-index.md` must exist and identify that system. A missing
  index or absent entry is NEEDS WORK, not an auto-pass.
- [ ] **GDD requirement referenced**: The story includes a `design/gdd/` path
  and quotes or links a specific requirement, acceptance criterion, or rule from
  that GDD — not just the GDD filename. A link to the document without tracing
  to a specific requirement does not pass.
- [ ] **Requirement is self-contained**: The acceptance criteria in the story
  are understandable without opening the GDD. A developer should not need to
  read a separate document to understand what DONE means.
- [ ] **Acceptance criteria are testable**: Each criterion is a specific,
  observable condition — not "implement X" or "the system works correctly".
  Bad example: "Implement the jump mechanic." Good example: "Jump reaches
  max height of 5 units within 0.3 seconds when jump is held."
- [ ] **No acceptance criteria require judgment calls** *(auto-pass for `Type: Visual/Feel`)*: Criteria like
  "feels responsive" or "looks good" are not testable without a defined
  benchmark. For Logic, Integration, UI, and Config/Data stories, these must be
  replaced with specific observable conditions. For Visual/Feel stories, subjective
  criteria are expected and this check auto-passes — instead verify that each
  subjective criterion has a paired playtest protocol or evidence requirement
  (e.g., "evidence doc required at `production/qa/evidence/[slug]-evidence.md`").
  PASS if the acceptance criterion ends with or is accompanied by an explicit reference to a file path such as `production/qa/evidence/[slug]-evidence.md`. NEEDS WORK if the criterion is purely subjective with no evidence file path specified.

### Architecture Completeness

- [ ] **Governing ADRs are explicit**: Parse every item in the story's
  `Governing ADRs` list. With multiple ADRs, exactly one list item must carry an
  explicit primary marker; neither list order nor the first item implies primary.
  Zero or multiple primary markers are **BLOCKED**, including a single unmarked
  real ADR. Missing/empty ADR data is **BLOCKED**. The only N/A form accepted is
  for `Type: Config/Data` and must be the sole item `N/A — [non-empty,
  non-placeholder reason]`;
  N/A for any other type is **BLOCKED**.
- [ ] **Every ADR is Accepted**: Read every referenced ADR, not only the primary.
  Each file must exist and its `Status:` must be exactly `Accepted`. Proposed,
  missing, or any other status is **BLOCKED**.
- [ ] **TR-ID is valid and active**: If the story contains a `TR-[system]-NNN`
  reference, look it up in the TR registry loaded in Section 2.
  - If the ID exists and `status: active` → pass.
  - If the ID exists and `status: deprecated` or `status: superseded` →
    NEEDS WORK: the requirement was removed or replaced.
    Fix: update the story to reference the current requirement ID or remove if no longer applicable.
  - If the ID does not exist in the registry → NEEDS WORK: ID was not registered
    (story may predate registry, or registry needs an `$architecture-review` run).
  - If the story declares a TR-ID and the registry is missing/unparseable →
    **BLOCKED**.
  - If the story explicitly has no TR-ID, validate its existing specific GDD or
    quick-design requirement reference instead; do not infer that it predates tracking.
- [ ] **Manifest version is current**: If the story has a positive integer
  `Manifest Version:` in its header AND the control manifest exists:
  - If story version exactly matches the current integer → pass.
  - If story version differs from the current manifest → NEEDS WORK: new rules may
    apply. Fix: review changed manifest rules, update story if any forbidden/required
    entries changed, then update the story's `Manifest Version:` to current.
  - If the manifest exists but the story has no `Manifest Version:` → NEEDS WORK.
  - If the manifest itself does not exist, note that once under the existing
    project-stage rule and do not pretend the version check passed.
- [ ] **Engine notes present**: For any post-cutoff engine API this story
  is likely to touch, implementation notes or a verification requirement are
  included. If the story clearly does not touch engine APIs (e.g., it is a
  pure data/config change), "N/A — no engine API involved" is acceptable.
- [ ] **Control manifest rules noted**: Relevant layer rules from the control
  manifest are referenced, OR "N/A — manifest not yet created" is stated.
  This item auto-passes if `docs/architecture/control-manifest.md` does not
  exist yet (do not penalize stories written before the manifest was created).

### Scope Clarity

- [ ] **Estimate present**: The story includes a size estimate (hours,
  points, or a t-shirt size). A story with no estimate cannot be planned.
- [ ] **In-scope / Out-of-scope boundary stated**: The story states what
  it does NOT include, either in an explicit Out of Scope section or in
  language that makes the boundary unambiguous. Without this, scope creep
  during implementation is likely.
- [ ] **Story dependencies listed**: If this story depends on other stories
  being DONE first, those story IDs are listed. If there are no dependencies,
  "None" is explicitly stated (not just omitted).

### Open Questions

- [ ] **No unresolved design questions**: The story does not contain explicit
  `UNRESOLVED`, `TBD`, `TODO`, `Open Question`, or placeholder markers in
  acceptance criteria, implementation notes, or rules. A normal question mark,
  answered FAQ, or example punctuation is not an unresolved marker. A critical
  unresolved item without a named owner is BLOCKED.
- [ ] **Dependency stories are not in DRAFT**: Resolve an explicit dependency
  path first. Otherwise match its ID exactly against story headers under
  `production/epics/`. Zero or multiple matches are BLOCKED and the evidence is
  listed. Read the uniquely resolved file's Status; DRAFT or missing is BLOCKED.

### Asset References Check

- [ ] **Referenced assets exist**: Scan the story text for asset path patterns
  (paths containing `assets/`, or file extensions `.png`, `.jpg`, `.svg`,
  `.wav`, `.ogg`, `.mp3`, `.glb`, `.gltf`, `.tres`, `.tscn`, `.res`).
  - Classify each path as a prerequisite/input to reuse or an output named under
    `Files to Create`/equivalent. Future outputs are not required to exist.
  - For each prerequisite asset path, check the exact matching file.
  - If any prerequisite asset does not exist: **NEEDS WORK** — note the missing
    path(s). (The story references assets that have not been created yet.
    Either remove the reference, create a placeholder, or mark it as an
    explicit dependency on an asset creation story.)
  - If all referenced assets exist: note "Referenced assets verified:
    [count] found."
  - If no asset paths are referenced in the story: note "No asset references
    found in story — skipping asset check." This item auto-passes.
  - This is an existence-only check. Do not validate file format or content.

### Definition of Done

- [ ] **Minimum testable acceptance criteria by story type**:
  - Logic / Integration stories: at least 3
  - Visual/Feel and UI stories: at least 2
  - Config/Data stories: at least 1
  Apply the threshold matching the story's `Type:` field. If the story has fewer than the minimum, mark as NEEDS WORK.
- [ ] **Performance budget noted if applicable**: If this story touches any
  part of the gameplay loop, rendering, or physics, a performance budget or
  a "no performance impact expected — [reason]" note is present.
- [ ] **Story Type declared**: The story includes a `Type:` field in its header
  identifying the test category (Logic / Integration / Visual/Feel / UI / Config/Data).
  Without this, test evidence requirements cannot be enforced at story close.
  Fix: Add `Type: [Logic|Integration|Visual/Feel|UI|Config/Data]` to the story header.
- [ ] **Test evidence requirement is clear**: the `## Test Evidence` section
  contains exactly one type-appropriate evidence path/alternative. Integration
  uses a test by default; a playtest alternative needs the GDD-AC reason. Lists
  of every type's possible path are ambiguous and NEEDS WORK.
  Fix: Add `## Test Evidence` with the expected evidence location for the story's type.

---

## 4. Director Gate — Story Readiness Review

Run this after all local checklist items and before assigning or outputting the
final verdict. Apply the review mode resolved in Phase 0:

- `solo` → skip and note `QL-STORY-READY skipped — Solo mode.`
- `lean` → skip and note `QL-STORY-READY skipped — Lean mode.`
- `full` → for each story in scope, sequentially spawn `qa-lead` using gate
  **QL-STORY-READY** and pass the required standard context: story path, story
  type, full acceptance-criteria list, TR-ID plus current registry requirement
  text, dependency states, and provisional local verdict.

Record a separate gate result for every story; never reuse one result across an
`all` or `sprint` scope. Apply it before the final verdict:

- **ADEQUATE** → adds no finding.
- **GAPS** → that story is at least NEEDS WORK; report the specific gaps.
- **INADEQUATE** → that story is BLOCKED.
- If the agent/gate fails or returns no usable verdict, that story cannot be
  READY. Report it as incomplete and keep completed story results in the
  aggregate.

This read-only gate has no accept-and-proceed or write-story option. After all
required per-story gates finish, assign and output final verdicts once.

---

## 5. Verdict Assignment

Assign one of three verdicts per story:

**READY** — All checklist items pass or have explicit N/A justifications.
The story can be assigned immediately.

**NEEDS WORK** — One or more checklist items fail, but all dependency stories
exist and are not DRAFT. The story can be fixed before assignment.

**BLOCKED** — Any referenced ADR is missing or not Accepted; multi-ADR primary
markers are absent/ambiguous; ADR data is missing or N/A is invalid for the
story type; a declared TR-ID cannot be validated because the registry is
missing/unparseable; a dependency story is missing or DRAFT; a critical
UNRESOLVED question has no owner; or the full QL-STORY-READY gate is INADEQUATE
or fails to return a usable result. Any blocker forces the final verdict to
BLOCKED even when NEEDS WORK findings also exist.

**NEEDS WORK floor from the gate** — QL-STORY-READY GAPS can never produce READY.

---

## 6. Output Format

### Single story output

```
## Story Readiness: [story title]
File: [path]
Verdict: [READY / NEEDS WORK / BLOCKED]

### Passing Checks (N/[total])
[list passing items briefly]

### Gaps
- [Checklist item]: [exact description of what is missing or wrong]
  Fix: [specific text needed to resolve this gap]

### Blockers (if BLOCKED)
- [What is blocking]: [story ID or design question that must resolve first]
```

### Multiple story aggregate output

```
## Story Readiness Summary — [scope] — [date]

Ready:      [N] stories
Needs Work: [N] stories
Blocked:    [N] stories

### Ready Stories
- [story title] ([path])

### Needs Work
- [story title]: [primary gap — one line]
- [story title]: [primary gap — one line]

### Blocked Stories
- [story title]: Blocked by [story ID / design question]

---
[Full detail for each non-ready story follows, using the single-story format]
```

### Sprint escalation

If the scope is `sprint` and any Must Have stories are NEEDS WORK or BLOCKED,
add a prominent warning at the top of the output:

```
WARNING: [N] Must Have stories are not implementation-ready.
[List them with their primary gap or blocker.]
Resolve these before the sprint begins or replan with `$sprint-plan update`.
```

---

## 7. Collaborative Protocol

This skill is read-only. It never writes files or asks for changeset approval.
It may provide fix guidance or draft missing text in conversation only.

After reporting findings, offer:

"Would you like help filling in the gaps for any of these stories? I can
draft the missing sections for your approval."

If the user says yes for a specific story, draft only the missing sections
in conversation. Do not use file-editing capabilities — the user (or
`$create-stories`) handles writing.

**Redirect rules:**
- If a story file does not exist at all: "This story file is missing entirely.
  If its epic already exists, run `$create-stories [epic-slug]`. Only when no
  epic exists should you run `$create-epics [layer]` first."
- If a story has no GDD reference and the work appears small: "This story has
  no GDD reference. If the change is small (under ~4 hours), run
  `$quick-design [description]` to create a Quick Design Spec, then reference
  that spec in the story."
- If a story's scope has grown beyond its original sizing: "This story appears
  to have expanded in scope. Consider splitting it or escalating to the producer
  before implementation begins."

---

## 8. Next-Story Handoff

After completing a single-story readiness check (not `all` or `sprint` scope):

1. Prefer `production/sprint-status.yaml` when it identifies the current
   sprint; otherwise use the highest valid numbered sprint file and referenced
   story headers.
2. Find candidate stories whose canonical status is `ready` or
   `backlog` (header fallback: Ready or Not Started), excluding the story just
   checked and incomplete dependencies, in Must Have or Should Have.

If any are found, surface up to 3:

```
### Other Candidate Stories in This Sprint (Readiness Not Yet Verified)

1. [Story name] — [1-line description] — Est: [X hrs]
2. [Story name] — [1-line description] — Est: [X hrs]

Run `$story-readiness [path]` to validate before starting.
```

If no sprint file exists or no other ready stories are found, skip this section silently.

---


## Recommended Next Steps

- Run `$dev-story [story-path]` to begin implementation once the story is READY
- Run `$story-readiness sprint` to check all stories in the current sprint at once
- Run `$create-stories [epic-slug]` if a story file is missing entirely
