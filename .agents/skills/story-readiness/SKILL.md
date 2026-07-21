---
name: story-readiness
description: "Validate that a story file is implementation-ready. Fails closed when requirement traceability, the current control-manifest snapshot, or the full-mode QA gate is missing or inadequate. Produces READY / NEEDS WORK / BLOCKED with specific gaps. Use when user says 'is this story ready', 'can I start on this story', or 'is story X ready to implement'."
---

## Invocation and execution

Invoke this workflow as `$story-readiness`.

Arguments: `[story-file-path or 'all' or 'sprint'] [--review full|lean|solo]`.
Treat bracketed values as optional unless the workflow says otherwise.

# Story Readiness

This skill validates that a story file contains everything a developer needs
to begin implementation: current requirement traceability, current architecture
controls, testable acceptance criteria, and no unresolved blockers.

**This skill is read-only.** It never edits story files, source documents,
registries, manifests, sprint trackers, or gate records. It reports findings
and can draft missing story text in conversation for the user's approval.

**Output:** A final verdict per story (`READY`, `NEEDS WORK`, or `BLOCKED`) with
specific evidence for every non-passing check. `READY` is never emitted when a
required source is unavailable, a production story is untraced or stale, or a
full-mode QA review returns `GAPS` or `INADEQUATE`.

---

## Phase 0: Resolve Review Mode

Resolve the review mode once at startup and retain it for every story in this
run:

1. If the invocation contains `--review [full|lean|solo]`, use that value.
2. Else read `production/review-mode.txt` and use its value.
3. Else default to `lean`.

See `.codex/docs/director-gates.md` for the shared mode and gate contracts.

---

## 1. Parse Arguments

The first non-review argument selects scope:

- **Specific path**: validate exactly that story file.
- **`sprint`**: read the current sprint plan from `production/sprints/` (most
  recent file), extract every story path it references, and validate each one.
- **`all`**: find files matching `production/epics/**/*.md`, exclude `EPIC.md`
  index files, and validate every story file found.
- **No argument**: ask the user which scope to validate.

If no scope is provided, ask:

- "What would you like to validate?"
  - "A specific story file"
  - "All stories in the current sprint"
  - "All stories in production/epics/"
  - "Stories for a specific epic"

Report the resolved scope before proceeding: `Validating [N] story files.`

---

## 2. Load Supporting Context and Source Status

Load shared sources once, before checking any story. Record each source as
`loaded`, `missing`, `unreadable`, or `invalid`; never convert a missing or
unreadable source into a passing check.

### 2.1 Determine whether the production control plane is required

Set `production_control_plane_required = true` for a story when either condition
is true:

1. Its path is under `production/epics/`; or
2. It declares any production-schema marker, including `Status: Ready`,
   `Status: Ready for Dev`, `Layer:`, `Type:`, `Manifest Version:`,
   `Manifest Hash:`, a `TR-[system]-NNN` requirement, or a governing ADR.

Do not infer that a story is pre-architecture merely because a registry or
manifest is absent. A story outside the production control plane may use an
explicit, reasoned N/A where the checklist permits it; a production story may
not.

### 2.2 Load authoritative sources

- `design/gdd/systems-index.md` — identify approved GDDs.
- `docs/architecture/tr-registry.yaml` — parse all entries and index them by
  exact `id`. Record the registry source status. A missing, unreadable, or
  invalid registry is a critical source failure; TR checks do not auto-pass.
- `docs/architecture/control-manifest.md` — read the raw file bytes, compute a
  lowercase SHA-256 digest, and parse the exact `Manifest Version:` value from
  the header. Record the manifest source status. A missing, unreadable, or
  structurally invalid manifest does not auto-pass production stories.
- Referenced ADRs — for every unique ADR across the selected stories, read the
  file and cache its `Status:` field.
- The current sprint plan — when scope is `sprint`, read it for Must Have /
  Should Have escalation.
- Every selected story — read its current raw bytes and compute a lowercase
  SHA-256 before evaluating any imported QA-plan provenance.

For display and comparison, format the computed manifest digest as
`sha256:<64 lowercase hexadecimal characters>`. Hash the current raw bytes;
never hash normalized, copied, or user-supplied text.

---

## 3. Story Readiness Checklist

Evaluate every item for every story. A story is eligible for `READY` only when
every item passes or has an explicitly permitted N/A reason.

### Design Completeness

- [ ] **GDD requirement referenced**: The story includes a `design/gdd/` path
  and quotes or links a specific requirement, acceptance criterion, or rule
  from that GDD. A bare filename does not pass.
- [ ] **Requirement is self-contained**: The acceptance criteria are
  understandable without opening the GDD.
- [ ] **Acceptance criteria are testable**: Each criterion is a specific,
  observable condition rather than "implement X" or "works correctly."
- [ ] **No acceptance criteria require unsupported judgment calls**
  *(auto-pass for `Type: Visual/Feel` only when paired evidence is specified)*:
  Logic, Integration, UI, and Config/Data criteria need observable benchmarks.
  Each subjective Visual/Feel criterion must name its playtest protocol or an
  evidence path such as `production/qa/evidence/[slug]-evidence.md`.

### Architecture Completeness

- [ ] **ADR referenced or N/A stated**: The story references at least one ADR,
  or explicitly states `No ADR applies` with a brief reason.
- [ ] **ADR is Accepted**: Every referenced ADR must exist and have
  `Status: Accepted`. A missing ADR or an ADR with `Status: Proposed` is
  `BLOCKED`. An explicit, reasoned `No ADR applies` note passes this check.
- [ ] **TR registry is available**:
  - If `production_control_plane_required = true` and the registry is missing,
    unreadable, or invalid, add a `BLOCKED` finding to every affected story.
  - Name `docs/architecture/tr-registry.yaml` and its source status in the
    blocker. Do not use story age, a legacy guess, or a waiver to pass it.
- [ ] **Every TR-ID is valid and active**:
  - A production story must contain at least one exact `TR-[system]-NNN` ID.
  - `TR-[system]-???`, malformed values, and a missing TR-ID are `NEEDS WORK`.
  - Every referenced ID must exist in the loaded registry and have
    `status: active`.
  - An unregistered, deprecated, or superseded ID is `NEEDS WORK`; name the
    current replacement when the registry provides one.
  - A legacy story is recognized only by the exact explicit marker
    `Traceability: LEGACY-UNTRACED`. This marker produces `NEEDS WORK` until the
    story is migrated to an active TR-ID. It never makes a story `READY` and it
    does not bypass an unavailable registry.
- [ ] **Manifest snapshot is present and current**:
  For every story where `production_control_plane_required = true`, require all
  of the following:
  1. `Manifest Version: [exact current manifest version]` in the story header.
  2. `Manifest Hash: sha256:[64 lowercase hex characters]` in the story header.
  3. A `## Source Snapshot` section containing the exact current entry
     ``- `docs/architecture/control-manifest.md`: `sha256:[64 lowercase hex characters]` ``.

  Apply this verdict matrix:

  - Current manifest missing, unreadable, or without a parseable version:
    `NEEDS WORK`.
  - Story manifest version missing or not an exact match: `NEEDS WORK`.
  - Story manifest hash missing, malformed, or not equal to the computed current
    hash: `NEEDS WORK`.
  - Source Snapshot missing, missing the manifest entry, or carrying a different
    hash: `NEEDS WORK`.
  - Version, header hash, and snapshot hash all exactly match the current
    manifest: pass.

  A `Manifest-Note`, waiver, accepted-risk statement, or user choice is
  informational only. It must not replace or rewrite the captured hash and must
  not turn a missing or stale snapshot into a pass.
- [ ] **Engine notes present**: For post-cutoff engine APIs, the story includes
  implementation notes or a verification requirement. A pure data/config story
  may state `N/A — no engine API involved`.
- [ ] **Control manifest rules noted**: Relevant rules from the current control
  manifest are referenced. `N/A — manifest not yet created` is permitted only
  when `production_control_plane_required = false`; it never passes a production
  story.

### Scope Clarity

- [ ] **Estimate present**: The story includes an hours, points, or t-shirt-size
  estimate.
- [ ] **In-scope / Out-of-scope boundary stated**: The story explicitly states
  what it does not include.
- [ ] **Story dependencies listed**: Dependencies are listed by stable story ID,
  or `None` is explicit.

### Open Questions

- [ ] **No unresolved design questions**: Acceptance criteria, implementation
  notes, and rule statements contain no unresolved `UNRESOLVED`, `TBD`, `TODO`,
  `?`, or equivalent marker.
- [ ] **Dependency stories are not DRAFT**: Every listed dependency exists and
  is not DRAFT. A missing or DRAFT dependency is `BLOCKED`.

### Asset References Check

- [ ] **Referenced assets exist**: Scan for paths containing `assets/` or ending
  in `.png`, `.jpg`, `.svg`, `.wav`, `.ogg`, `.mp3`, `.glb`, `.gltf`, `.tres`,
  `.tscn`, or `.res`.
  - Missing referenced assets are `NEEDS WORK`; name every missing path.
  - If all exist, report `Referenced assets verified: [count] found.`
  - If none are referenced, report `No asset references found in story —
    skipping asset check.` and pass this item.

This is an existence-only check; do not validate asset contents.

### Definition of Done

- [ ] **Minimum testable acceptance criteria by story type**:
  - Logic / Integration: at least 3
  - Visual/Feel / UI: at least 2
  - Config/Data: at least 1
- [ ] **Performance budget noted if applicable**: Gameplay-loop, rendering, or
  physics work names a budget or states `no performance impact expected` with a
  reason.
- [ ] **Story Type declared**: `Type:` is one of Logic, Integration,
  Visual/Feel, UI, or Config/Data.
- [ ] **Test evidence requirement is clear**: A `## Test Evidence` section names
  the expected test or evidence path for the declared type.
- [ ] **Imported QA plan evidence is current**: When `## QA Test Cases` names a
  `QA Plan Path` or claims imported plan IDs, read the complete plan and verify
  all of the following before those specifications can satisfy readiness:
  - the recorded `QA Plan Hash` equals the current raw-byte SHA-256 of that
    canonical plan path;
  - the plan's declared and recomputed effective states are both `CURRENT`, not
    `PARTIAL` or `STALE`;
  - every source path in the plan manifest still exists and matches its captured
    raw-byte hash;
  - the plan binding names this exact story path and current story hash;
  - the story's stable AC IDs exactly match the bound AC IDs; and
  - every imported stable test/check ID is unique and maps to exactly one AC.

  Any missing path/hash/binding, source mismatch, `PARTIAL`/`STALE` state, or
  ambiguous ID is `NEEDS WORK`; list the exact gap. It cannot be waived into a
  pass. Stories whose QA specifications were authored directly and do not claim
  a QA-plan import remain subject to the ordinary completeness checks.

---

## 4. Compute the Base Verdict

Compute a base verdict from deterministic checks before the optional QA gate:

- **BLOCKED** — Any critical source blocker, missing/DRAFT dependency, missing
  or Proposed ADR, or critical unresolved design question without an owner.
- **NEEDS WORK** — No blocker exists, but one or more checks fail, including
  missing/invalid TR-ID, `LEGACY-UNTRACED`, or missing/stale manifest snapshot.
- **READY** — Every deterministic check passes or has an explicitly permitted
  N/A reason.

List NEEDS WORK findings even when a stricter blocker makes the base verdict
`BLOCKED`.

---

## 5. Director Gate and Final Verdict

Apply the review mode resolved in Phase 0 to QL-STORY-READY:

- `solo` — skip and record `[QL-STORY-READY] skipped — Solo mode`.
- `lean` — skip and record `[QL-STORY-READY] skipped — Lean mode`.
- `full` — spawn `qa-lead` through Codex subagent delegation using gate
  **QL-STORY-READY** from `.codex/docs/director-gates.md` after deterministic
  checks finish and before emitting the final verdict.

For each story, pass:

- Story file path and title
- Story type
- Acceptance criteria, verbatim
- TR-ID and current registry requirement text
- Dependency states
- Base verdict and deterministic findings

Map the gate result without exception:

| QA result | Required final effect |
|---|---|
| `ADEQUATE` | Keep the base verdict. |
| `GAPS [list]` | Add the QA gaps and set the final verdict to at least `NEEDS WORK`. A pre-existing `BLOCKED` remains `BLOCKED`. |
| `INADEQUATE [blockers]` | Add the QA blockers and set the final verdict to `BLOCKED`, even when the base verdict was `READY`. |
| Gate fails to return a valid verdict in `full` mode | Set the final verdict to `BLOCKED` and report the gate failure. |

There is no `proceed anyway` path from `INADEQUATE`. If the user accepts risk
for `GAPS`, record the accepted risk in the response only; the story remains
`NEEDS WORK` (or `BLOCKED` if already blocked). Accepted risk never produces
`READY` and never changes story or source files.

Final verdict is the strictest result across deterministic checks and the QA
gate: `BLOCKED` > `NEEDS WORK` > `READY`.

---

## 6. Output Format

### Single story

```markdown
## Story Readiness: [story title]
File: [path]
Verdict: [READY / NEEDS WORK / BLOCKED]

### Source Status
- TR registry: [loaded / missing / unreadable / invalid]
- Control manifest: [loaded / missing / unreadable / invalid]
- Current manifest version: [value / unavailable]
- Current manifest hash: [sha256:... / unavailable]

### Gate
- QL-STORY-READY: [ADEQUATE / GAPS / INADEQUATE / skipped / failed]

### Passing Checks (N/[total])
[list passing items briefly]

### Gaps
- [check]: [exact missing, stale, or invalid value]
  Evidence: [path and field/section]
  Fix: [specific resolution]

### Blockers (if BLOCKED)
- [blocker]: [dependency, source, ADR, or QA condition that must resolve]

### Accepted Risks (if any)
- [risk and user decision]; verdict remains [NEEDS WORK / BLOCKED].
```

### Multiple stories

```markdown
## Story Readiness Summary — [scope] — [date]

Ready:      [N] stories
Needs Work: [N] stories
Blocked:    [N] stories

### Ready Stories
- [story title] ([path])

### Needs Work
- [story title]: [primary gap]

### Blocked Stories
- [story title]: [primary blocker]

---
[Full detail for each non-ready story follows in the single-story format.]
```

For `sprint` scope, if any Must Have story is not READY, add:

```text
WARNING: [N] Must Have stories are not implementation-ready.
[List each story with its primary gap or blocker.]
Resolve these before the sprint begins or replan with `$sprint-plan update`.
```

Never label a base verdict as final before the required full-mode QA result is
merged.

---

## 7. Collaborative Protocol

This workflow is read-only. After the final report, offer:

"Would you like help drafting the missing sections for any of these stories?"

If the user selects a story, draft only the missing sections in conversation.
Do not edit files. For a QA `GAPS` result, the available choices are:

- Draft the suggested gaps
- Record accepted risk and keep the non-ready verdict
- Discuss further

For `INADEQUATE`, offer only revision help or discussion; do not offer to
proceed to implementation.

Redirect rules:

- Missing story: run `$create-epics [layer]` and then
  `$create-stories [epic-slug]`.
- Missing GDD reference for a small change: consider
  `$quick-design [description]`, then reference the resulting spec.
- Scope larger than its estimate: split it or escalate to the producer.
- Missing TR registry: run `$architecture-review` to establish it.
- Missing/currently unsnapshotted manifest: regenerate the manifest as needed,
  then update the story through its owning workflow; a waiver cannot substitute.

---

## 8. Next-Story Handoff

After a single-story check, and only when that story's **final** verdict is
`READY`, read the current sprint file from `production/sprints/` (most recent)
and surface up to three other Must Have or Should Have stories that are marked
READY or NOT STARTED and have no incomplete dependencies:

```markdown
### Other Ready Stories in This Sprint

1. [Story name] — [description] — Est: [X hrs]

Run `$story-readiness [path]` to validate before starting.
```

If no sprint file or eligible story exists, omit this section.

---

## Recommended Next Steps

- Run `$dev-story [story-path]` only when the final verdict is `READY`.
- Run `$story-readiness sprint` to inspect the current sprint.
- Run `$create-stories [epic-slug]` if a story file is missing.
- Resolve every named source, traceability, snapshot, or QA issue before treating
  a non-ready story as implementation-authorized.
