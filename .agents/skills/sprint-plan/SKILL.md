---
name: sprint-plan
description: "Create or update a sprint from existing implementation-ready story work items, with read-only readiness and QA checks before one authorized atomic plan/tracker write."
---

## Invocation and execution

Invoke this workflow as `$sprint-plan`.

Arguments: `[new|update] [--review full|lean|solo]`. With no mode, use `new`.
Treat bracketed values as optional unless the workflow says otherwise.

Before the first file change, present the complete proposed changeset, listing
every file and its exact proposed content or complete diff, and obtain one
explicit approval. After approval, make only those changes. If scope, candidate
bytes, findings, or target preimages change, stop, rebuild the complete preview,
and obtain new approval when the changeset changed materially.

This workflow owns only sprint planning. `$sprint-status` owns status reports.
It never creates or repairs epics, stories, GDD requirements, TR registry entries,
ADRs, readiness evidence, QA plans, or `production/review-mode.txt`.

---

## Phase 0: Parse arguments and enforce terminal branches

Parse arguments before reading project files or resolving review mode. Reject an
unknown mode, an unknown review value, or conflicting duplicate arguments with
**Verdict: BLOCKED** and zero gates and zero writes.

### Legacy `status` compatibility branch

If the first mode is the legacy value `status`:

1. Output: "`$sprint-plan status` is read-only status work and has moved to
   `$sprint-status`. Run `$sprint-status` instead."
2. Do not resolve review mode, load planning context, invoke readiness or director
   gates, prepare a changeset, create a directory, or write any file.
3. Assert `gate_count == 0` and `write_count == 0`.
4. **STOP.** This is a terminal branch and cannot enter any later phase.

For `new` and `update`, initialize an in-memory mutation ledger with
`gate_count = 0`, `write_count = 0`, and an empty authorized path set. The ledger
is diagnostic state only and is never persisted.

---

## Phase 1: Resolve review mode once, without configuration writes

Resolve one review mode and keep it unchanged for the whole run:

1. If `--review full|lean|solo` was passed, use it. Do not replace it with a
   value read from disk.
2. Otherwise, if `production/review-mode.txt` exists and contains exactly one of
   `full`, `lean`, or `solo`, use that value.
3. Otherwise, use `lean` for this run and report that the configuration is
   missing or invalid.

Never create or edit `production/review-mode.txt` during sprint planning. Setting
or repairing the persistent review mode is a separate, explicitly authorized
task. The review-mode file is never part of the sprint changeset, so declining a
sprint cannot leave a review-mode side effect.

Use the resolved mode for every read-only readiness check and for PR-SPRINT. See
`.codex/docs/director-gates.md` for gate semantics.

---

## Phase 2: Load authoritative planning inputs

All work in this phase is read-only.

### 2.1 Milestone, capacity, history, and risk context

Read:

- the current milestone from `production/milestones/`;
- `production/sprints/` and the matching current tracker, if present;
- team capacity and estimates in the units already established by the project;
- the latest relevant risk register entries under `production/risk-register/`;
  and
- for `update`, `production/sprint-status.yaml` and the sprint plan whose number
  equals its `sprint` value.

Treat a missing `production/sprints/` directory as empty history. For `update`,
a missing tracker, a missing matching plan, or disagreement between their sprint
identities is **BLOCKED**; do not guess the active sprint from modification time.

### 2.2 Build the existing-story registry

The only source of new sprint work is the story registry already written by the
epic/story workflows. Enumerate `production/epics/*/EPIC.md`, parse each managed
`## Stories` table, and resolve each row to exactly one sibling file matching
`story-[NNN]-[slug].md`. Build an immutable in-memory registry.

A row is structurally valid only when all of the following hold:

- the epic directory supplies the epic slug and the table supplies a three-digit
  story number;
- exactly one sibling story file has that number;
- the file's `# Story [NNN]: [title]`, `Status`, `Layer`, and `Type` agree with
  the EPIC table and epic identity;
- the repository-relative file path is canonical, remains under
  `production/epics/`, and contains no traversal or symlink escape;
- the tuple `[epic-slug]/story-[NNN]` and the file path are both unique; and
- the story file is readable as complete text.

Use `[epic-slug]/story-[NNN]` as the tracker `id` and the exact
repository-relative story path as the canonical work item. This identity comes
from the existing epic slug and story number; never derive identity from a title,
GDD prose, an acceptance criterion, or a newly invented task.

Malformed, conflicting, duplicate, or unresolvable rows are reported and excluded.
If any such row is needed by the requested update or makes the selected scope
ambiguous, stop with **BLOCKED**.

### 2.3 Validate every proposed addition against current readiness

An existing registry row becomes an eligible new candidate only when:

1. the EPIC table status is exactly `Ready`;
2. the story header status is exactly `Ready` (not `Needs Work`, `Blocked`,
   `Ready for Dev`, or an inferred synonym);
3. SHA-256 of the exact current story bytes is captured as
   `sha256:<64 lowercase hexadecimal characters>`;
4. the read-only `$story-readiness [story-path] --review [resolved-mode]`
   contract is evaluated for those exact bytes and returns the final verdict
   `READY`; and
5. an immediate re-read has the same SHA-256. A changed file invalidates the
   result and must be checked again before it can be selected.

Record the path, canonical ID, story-byte hash, source status, final readiness
verdict, review mode, layer, dependencies, priority, type, and estimate in the
candidate manifest. A historical verdict, a story header alone, a cached output
for different bytes, or user acceptance of a non-ready result is insufficient.
Do not run a second QL-STORY-READY gate in sprint-plan; the authoritative
story-readiness result already merges that gate in `full` mode.

Stories with final `NEEDS WORK` or `BLOCKED` remain visible as exclusions but
cannot enter the proposed additions. If no eligible new candidate exists for a
`new` sprint, output "No implementation-ready stories in the existing backlog",
recommend `$create-stories` for missing story artifacts and `$story-readiness`
for named gaps, then finish **BLOCKED** with zero producer gates and zero writes.

Existing tracked items retained by `update`, or explicitly carried from the
previous sprint, are not new candidates. Preserve their lifecycle status and
verify that their canonical story file still exists; never reset an in-progress,
review, done, or blocked item to ready.

### 2.4 GDD boundary

GDDs are read-only validation sources only when the readiness contract follows a
story's explicit GDD reference. Never scan `design/gdd/` for "ready features",
turn GDD prose into sprint tasks, invent acceptance criteria, or add a work item
that has no valid existing registry row and story file.

---

## Phase 3: Select scope and render both drafts in memory

### 3.1 New sprint

Derive the next sprint number from the existing numbered sprint files. Before
selecting new work, identify non-done items in the previous tracker and ask the
user to carry, defer, or cancel each group. A carried item keeps its canonical
path, origin sprint, and current lifecycle status and is marked `[CARRY]` in the
draft. The decision selects scope but authorizes no write.

Select only eligible candidates from Phase 2.3. Respect dependency order, then
Foundation → Core → Feature → Presentation layer order, then project priority,
without exceeding agreed capacity. Do not fill unused capacity with invented work.

### 3.2 Update sprint

Start from the matching plan/tracker pair loaded in Phase 2.1. Show current work
items and statuses, then gather requested additions, removals, reprioritization,
or re-estimation. Every addition must pass Phase 2.3 for its current exact bytes.
Preserve existing statuses. Only not-started items (`backlog` or
`ready-for-dev`) may be removed or freely reprioritized; otherwise ask the user
to retain them or handle their lifecycle through the owning workflow.

### 3.3 Render the sprint plan

Render the complete Markdown candidate in memory:

```markdown
# Sprint [N] — [Start Date] to [End Date]

sprint_id: sprint-[NNN]
plan_revision: sha256:[canonical planning-payload digest]
story_set_hash: sha256:[canonical story-set digest]
updated_at: [ISO-8601 timestamp with timezone]

## Sprint Goal
[One sentence tied to the current milestone]

## Capacity
- Total: [X established units]
- Buffer: [Y]
- Available: [Z]

## Work Items
| ID | Story | File | Layer | Priority | Owner | Estimate | Dependencies | Source SHA-256 |
|---|---|---|---|---|---|---:|---|---|
| [epic]/story-[NNN] | [existing title] | `production/epics/.../story-NNN-....md` | [layer] | must-have | [owner] | [estimate] | [IDs or None] | `sha256:...` |

## Carryover from Previous Sprint
| ID | Origin Sprint | Current Status | Decision / Reason |
|---|---:|---|---|

## Readiness Evidence
| ID | Story Status | Final Verdict | Review Mode | Exact Story SHA-256 |
|---|---|---|---|---|

## QA Plan
[path and coverage note, or the exact missing-QA warning from Phase 4]

## Risks
| Risk | Probability | Impact | Mitigation |
|---|---|---|---|

## Definition of Done for this Sprint
- [ ] Every delivered work item satisfies its story acceptance criteria
- [ ] Required automated tests or manual evidence pass
- [ ] QA plan requirements and smoke checks pass
- [ ] QA sign-off has no unresolved S1 or S2 defect
- [ ] Required design deviations and reviews are recorded
```

The plan references the existing stories; it does not copy, rewrite, or extend
their acceptance criteria.

### 3.4 Render the tracker

Render `production/sprint-status.yaml` in memory from the same selected work-item
set. Keep priority separate from lifecycle status. Every newly selected candidate
starts as `ready-for-dev`, regardless of priority; `should-have` and `nice-to-have`
must not be mislabeled `backlog` merely because of priority. Preserve the status
of retained or carried work.

```yaml
# Generated by $sprint-plan. Lifecycle updates belong to the owning story workflows.
# Story header status Ready maps to initial tracker status ready-for-dev.
# Tracker statuses: backlog | ready-for-dev | in-progress | review | done | blocked

sprint_id: "sprint-[NNN]"
active_sprint_id: "sprint-[NNN]"
plan_file: "production/sprints/sprint-[NNN].md"
plan_revision: "sha256:[canonical planning-payload digest]"
story_set_hash: "sha256:[canonical story-set digest]"
updated_at: "[ISO-8601 timestamp with timezone]"
goal: "[sprint goal]"
start: "[YYYY-MM-DD]"
end: "[YYYY-MM-DD]"
generated: "[ISO-8601 timestamp with timezone]"
qa_plan: "[canonical path or MISSING]"

stories:
  - id: "[epic-slug]/story-[NNN]"
    name: "[existing story title]"
    file: "production/epics/[epic-slug]/story-[NNN]-[slug].md"
    layer: "[Foundation|Core|Feature|Presentation]"
    priority: "must-have" # must-have | should-have | nice-to-have
    status: "ready-for-dev"
    source_status: "Ready"
    source_sha256: "sha256:[64 lowercase hexadecimal characters]"
    readiness_verdict: "READY"
    readiness_review_mode: "[full|lean|solo]"
    origin_sprint: ""
    owner: ""
    estimate: "[value and unit]"
    blocker: ""
    completed: ""
```

Before any gate, assert that the Markdown and YAML drafts contain exactly the
same work-item IDs, paths, priorities, source hashes, and lifecycle meanings.

Compute `story_set_hash` from the current exact story bytes using the same
consumer algorithm as `$sprint-status`: for every selected item render
`<story-id>\t<normalized-project-relative-path>\t<sha256-of-current-raw-story-bytes>`,
sort records by stable story ID using code-point order, join with LF and no
trailing LF, hash the exact UTF-8 bytes, and prefix the lowercase digest with
`sha256:`. Duplicate/missing IDs or unreadable stories block the write.

After QA findings, producer result/accepted concerns, and every final scope value
are resolved, compute `plan_revision` over UTF-8 canonical JSON for the complete
planning payload: sprint identity/dates/goal/capacity, `story_set_hash`, QA-plan
path/state or exact warning, carryover decisions, risks, producer outcome, and
the ordered work-item rows. The payload excludes only the `plan_revision` field
itself. Use one exact `updated_at` timestamp in both files. Re-render both drafts
with these three values before the final preview; any later change requires new
hashes and, when bytes change materially, new authorization.

---

## Phase 4: Resolve QA-plan findings before authorization

Still without writing, search `production/qa/` for the canonical QA plan for
sprint `[N]` or an unambiguous QA plan that identifies that sprint.

- If found, read it, record the path and relevant coverage in both drafts, and
  proceed.
- If absent or ambiguous, surface the finding and ask:
  - `[A] Pause and run $qa-plan sprint first (Recommended)`
  - `[B] Continue with an explicit missing-QA warning`

If `[A]`, discard the write candidate and finish **BLOCKED — QA plan required
before sprint activation** with zero writes. If `[B]`, add this exact block to
the Markdown draft before any producer gate or changeset preview:

```markdown
> ⚠️ **No QA Plan**: This sprint is being activated without a QA plan. Run
> `$qa-plan sprint` before implementation. Production → Polish QA sign-off is
> blocked until a sprint QA plan exists.
```

Also set tracker `qa_plan: "MISSING"`. The choice is part of scope resolution,
not permission to write. No QA finding or warning may be appended after approval
or after either target is written.

---

## Phase 5: Producer feasibility gate before authorization

The gate input is the full current Markdown/YAML draft, including readiness
hashes, carryover decisions, and QA-plan finding.

- `solo`: do not spawn; report `[PR-SPRINT] skipped — Solo mode`.
- `lean`: do not spawn; report `[PR-SPRINT] skipped — Lean mode`.
- `full`: spawn `producer` through Codex subagent delegation using **PR-SPRINT**
  from `.codex/docs/director-gates.md`, increment `gate_count`, and await its
  verdict.

Pass the selected existing story list, estimates, dependency order, capacity,
carryover, milestone constraints, excluded non-ready stories, and QA finding.

- `REALISTIC`: proceed.
- `CONCERNS`: surface all concerns. The user may revise scope, accept the stated
  risk, or stop. Acceptance records the concern in the draft before preview.
- `UNREALISTIC`: do not write. Revise scope or capacity with the user and rerun
  every invalidated selection/readiness/QA check and PR-SPRINT as applicable.
  If unresolved, finish **BLOCKED**.
- Missing, failed, or malformed full-mode verdict: finish **BLOCKED**.

After any revision, re-render both complete drafts and repeat their set-equivalence
assertion. Gate output, warnings, and accepted risk must all be reflected before
the final changeset is frozen.

---

## Phase 6: Freeze, preview, authorize, and atomically write

### 6.1 Freeze and preview

Freeze the exact UTF-8 bytes for:

- `production/sprints/sprint-[NNN].md`; and
- `production/sprint-status.yaml`.

Record SHA-256 of each target's current exact bytes, or `ABSENT`, plus SHA-256 of
each frozen candidate. Present one complete changeset preview containing both
paths, both preimages, both candidate hashes, and the complete new content or
complete unified diff. State explicitly that no other file, including
`production/review-mode.txt`, will change.

Obtain one explicit authorization for this exact pair. If declined, write
nothing and finish **BLOCKED — changeset not authorized**. Authorization of an
earlier draft does not authorize a later QA warning, gate revision, story hash,
or scope change.

### 6.2 Compare-and-swap preconditions

Immediately before the first mutation, perform one read-only preflight:

- every selected/carryover story still exists and matches the previewed
  `source_sha256`;
- every target still matches its previewed preimage or remains absent; and
- the plan and tracker candidates still have identical work-item sets.

If any precondition changed, write nothing. Return to the relevant read-only
phase, rebuild both drafts, re-run invalidated gates, and re-preview. Materially
different bytes require new authorization.

### 6.3 Atomic pair write and verification

Treat the two files as one transaction:

1. Create same-directory temporary siblings containing only the authorized
   candidate bytes; increment `write_count` for these authorized transaction
   writes only.
2. Re-read the temporary files and verify their hashes against the preview.
3. Recheck both target preimages once more, then replace both targets as one
   transactional pair. Preserve the captured preimages until both replacements
   succeed.
4. If either replacement or verification fails, restore both preimages (or
   remove only a newly created target), report every path that may have changed,
   and finish **BLOCKED**. Never report partial success as COMPLETE.
5. Re-read both final files and verify their exact hashes and work-item-set
   equivalence. Remove transaction temporaries only after successful verification.

Do not write either final target before Phase 4, Phase 5, complete preview, and
authorization have all resolved.

---

## Phase 7: Verdict and handoff

Emit **Verdict: COMPLETE** only after both authorized final files exist and pass
exact hash verification. Report the two final hashes and the number of selected,
carried, and excluded non-ready work items.

Then suggest only applicable next steps:

- `$qa-plan sprint` first when `qa_plan: MISSING`;
- `$story-readiness [story-path]` to revalidate if a story changes;
- `$dev-story [story-path]` only for a currently final-READY work item; and
- `$sprint-status` for all status reporting.

Other terminal results are explicit:

- **Verdict: BLOCKED** — no current READY candidate, invalid registry identity,
  missing update pair, unresolved QA/producer blocker, changed precondition,
  declined authorization, or failed atomic verification.
- **Verdict: COMPLETE — no changes required** — `update` renders byte-identical
  plan and tracker candidates and verifies both current files; no write occurs.

In every terminal branch, report `gate_count`, `write_count`, and all paths
written. The legacy `status` branch must always report zero for both counts.
