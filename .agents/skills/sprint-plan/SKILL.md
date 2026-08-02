---
name: sprint-plan
description: "Generates a new sprint plan or updates an existing one based on the current milestone, completed work, and available capacity. Pulls context from production documents and design backlogs."
---

## Invocation and execution

Invoke this workflow as `$sprint-plan`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[new|update|status] [--review full|lean|solo]`. Treat bracketed values as optional unless the workflow says otherwise.

Before starting, list `production/sprints/` read-only and use the existing sprint files as initial context. Treat a missing directory as an empty sprint history.


## Phase 0: Parse Arguments

Extract the mode argument (`new`, `update`, or `status`). If omitted, use `new`.
If any other mode or an invalid review value is supplied, show the legal usage
and stop without writing. Resolve the review mode exactly once and store it for
all gate spawns this run:
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `production/review-mode.txt`; use it only when its trimmed value is
   exactly `full`, `lean`, or `solo`
3. Else → default to `lean`

See `.codex/docs/director-gates.md` for the full check pattern.

**Review mode initialization** (only when no valid flag or file value resolved a mode):
- If the file doesn't exist and this is a `new` sprint: ask the user directly:
  - Prompt: "No review mode is set. Which review depth would you like for this sprint?"
  - Options:
    - `[A] full — spawn all director and lead gates`
    - `[B] lean — skip non-phase-gate director reviews (recommended for most sprints)`
    - `[C] solo — skip all gate spawning`
  - After selection: keep the chosen value pending. Do not write it yet; include
    `production/review-mode.txt` in the same final changeset as the sprint plan
    and status YAML.
- If the file doesn't exist and this is NOT a `new` sprint (e.g., updating an existing sprint): default to `lean` silently.

---

## Phase 1: Gather Context

1. **Read the current milestone** from `production/milestones/`.

2. **Read the previous sprint** (if any) from `production/sprints/` to
   understand velocity and carryover.

3. **Read the story backlog** from `production/epics/**/*.md`, excluding epic
   indexes. Candidates are stories whose status is not started/backlog/ready-for-dev
   and whose declared dependencies are complete or are ordered earlier in the
   proposed sprint. If there are no eligible stories, return **BLOCKED**, recommend
   `$create-stories`, and do not invoke a gate or write files.

4. **Resolve capacity** from the current milestone's existing capacity field,
   falling back to the previous sprint's explicit capacity/velocity field. If
   neither is present, ask the user for capacity; do not invent it. Reserve the
   existing 20% buffer, then order candidates by the project's implementation
   layer and existing priority before filling available capacity.

5. **Scan design documents** in `design/gdd/` for features tagged as ready
   for implementation, using them to validate rather than replace story candidates.

6. **Check the risk register** at `production/risk-register/`.

---

## Phase 2: Generate Output

For `new`:

Determine the sprint number from valid files named `production/sprints/sprint-[NNN].md`:
use one greater than the highest existing number, or 001 when none exist. The
markdown target is exactly `production/sprints/sprint-[NNN].md`. If that target
already exists, stop and ask the user to use `update`; never overwrite it.

**Generate a sprint plan** following this format and present it to the user. Do NOT ask to write yet — the producer feasibility gate (Phase 4) runs first and may require revisions before the file is written.

```markdown
# Sprint [N] — [Start Date] to [End Date]

## Sprint Goal
[One sentence describing what this sprint achieves toward the milestone]

## Capacity
- Total days: [X]
- Buffer (20%): [Y days reserved for unplanned work]
- Available: [Z days]

## Tasks

### Must Have (Critical Path)
| ID | Task | Agent/Owner | Est. Days | Dependencies | Acceptance Criteria |
|----|------|-------------|-----------|-------------|-------------------|

### Should Have
| ID | Task | Agent/Owner | Est. Days | Dependencies | Acceptance Criteria |
|----|------|-------------|-----------|-------------|-------------------|

### Nice to Have
| ID | Task | Agent/Owner | Est. Days | Dependencies | Acceptance Criteria |
|----|------|-------------|-----------|-------------|-------------------|

## Carryover from Previous Sprint
| Task | Reason | New Estimate |
|------|--------|-------------|

## Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|

## Dependencies on External Factors
- [List any external dependencies]

## Definition of Done for this Sprint
- [ ] All Must Have tasks completed
- [ ] All tasks pass acceptance criteria
- [ ] QA plan exists (`production/qa/qa-plan-sprint-[N].md`)
- [ ] All Logic/Integration stories have passing unit/integration tests
- [ ] Smoke check passed (`$smoke-check sprint`)
- [ ] QA sign-off report: APPROVED or APPROVED WITH CONDITIONS (`$team-qa sprint`)
- [ ] No S1 or S2 bugs in delivered features
- [ ] Design documents updated for any deviations
- [ ] Code reviewed and merged
```

For `update`:

**Update an existing sprint plan**:

1. Read the most recent sprint plan from `production/sprints/`.
2. Present the current story list with their current statuses from
   `production/sprint-status.yaml`. If the YAML is missing, reconstruct pending
   YAML from the selected sprint markdown and each referenced story's `Status:`
   field. Show every status that cannot be determined; preserve confirmed
   in-progress/done values and do not write until the final authorization.
3. Ask the user what to change: stories to add, remove, reprioritize, or re-estimate. Ask the user directly to gather changes.
4. Apply the changes and re-present the full revised plan for review.
5. Re-run the producer feasibility gate (Phase 4) on the revised plan.
6. Write the updated markdown plan and yaml together (same approval as `new` mode).

Note: `update` mode does not reset story statuses. Stories already marked `in-progress` or `done` keep their status. Only `backlog` and `ready-for-dev` stories can be removed or reprioritized freely.

For `status`:

**Generate a status report**:

```markdown
# Sprint [N] Status -- [Date]

## Progress: [X/Y tasks complete] ([Z%])

### Completed
| Task | Completed By | Notes |
|------|-------------|-------|

### In Progress
| Task | Owner | % Done | Blockers |
|------|-------|--------|----------|

### Not Started
| Task | Owner | At Risk? | Notes |
|------|-------|----------|-------|

### Blocked
| Task | Blocker | Owner of Blocker | ETA |
|------|---------|-----------------|-----|

## Burndown Assessment
[On track / Behind / Ahead]
[If behind: What is being cut or deferred]

## Emerging Risks
- [Any new risks identified this sprint]
```

After presenting this status report, stop. `status` is read-only: do not enter
Phases 3–6, do not invoke PR-SPRINT, do not request authorization, and do not
write any file.

---

## Phase 3: Prepare Sprint Status File

After generating a new sprint plan, or reconstructing a missing YAML in `update`
mode, also prepare the `production/sprint-status.yaml` content.
This is the machine-readable source of truth for story status — read by
`$sprint-status`, `$story-done`, and `$help` without markdown parsing.

**Do not write the yaml yet** — hold it in context. The producer feasibility
gate (Phase 4) and QA plan gate (Phase 5) may revise the pending plan. All
pending files are written together only after Phase 5 in one changeset approval.

Format:

```yaml
# Auto-generated by $sprint-plan. Updated by $story-done and $dev-story.
# DO NOT edit manually — use $story-done to update story status.
#
# Status value mapping (yaml ↔ story file Status field):
#   backlog        ↔  Not Started
#   ready-for-dev  ↔  Ready
#   in-progress    ↔  In Progress
#   review         ↔  In Review
#   done           ↔  Complete
#   blocked        ↔  Blocked

sprint: [N]
goal: "[sprint goal]"
start: "[YYYY-MM-DD]"
end: "[YYYY-MM-DD]"
generated: "[YYYY-MM-DD]"
updated: "[YYYY-MM-DD]"

stories:
  - id: "[epic-story, e.g. 1-1]"
    name: "[story name]"
    file: "[production/stories/path.md]"
    priority: must-have        # must-have | should-have | nice-to-have
    status: ready-for-dev      # backlog | ready-for-dev | in-progress | review | done | blocked
    owner: ""
    estimate_days: 0
    blocker: ""
    completed: ""
```

Initialize each story from the sprint plan's task tables:
- Must Have tasks → `priority: must-have`, `status: ready-for-dev`
- Should Have tasks → `priority: should-have`, `status: backlog`
- Nice to Have tasks → `priority: nice-to-have`, `status: backlog`

For `update`: read the existing `sprint-status.yaml`, carry over statuses for
stories that haven't changed, add new stories, remove dropped ones.

---

## Phase 4: Producer Feasibility Gate

**Review mode check** — apply before spawning PR-SPRINT:
- `solo` → skip. Note: "PR-SPRINT skipped — Solo mode." Proceed to Phase 5 (QA plan gate).
- `lean` → skip (not a PHASE-GATE). Note: "PR-SPRINT skipped — Lean mode." Proceed to Phase 5 (QA plan gate).
- `full` → spawn as normal.

Before finalising the sprint plan, spawn `producer` through Codex subagent delegation using gate **PR-SPRINT** (`.codex/docs/director-gates.md`).

Pass: proposed story list (titles, estimates, dependencies), total team capacity in hours/days, any carryover from the previous sprint, milestone constraints and deadline.

Present the producer's assessment.

If UNREALISTIC: revise the story selection (defer stories to Should Have or Nice to Have) and re-present the updated plan, then proceed to Phase 5.

If CONCERNS, ask the user directly:
- Prompt: "Producer flagged concerns with this sprint plan. How do you want to proceed?"
- Options:
  - `[A] Proceed as planned — I accept the risk`
  - `[B] Adjust scope — defer some Should Have stories`
  - `[C] Extend the sprint timeline`

If [A]: proceed to Phase 5.
If [B]: revise the story list, re-present the updated plan, then proceed to Phase 5.
If [C]: adjust sprint dates and capacity, re-present the updated plan, then proceed to Phase 5.

After handling the producer's verdict, keep the final sprint markdown, status
YAML, and any pending review-mode value in memory and proceed to Phase 5. Do not
write or announce COMPLETE yet.

---

## Phase 5: QA Plan Gate

Before closing the sprint plan, check whether a QA plan exists for this sprint.

Search for `production/qa/qa-plan-sprint-[N].md` or any file in `production/qa/` referencing this sprint number.

**If a QA plan is found**: note it in the sprint plan output — "QA Plan: `[path]`" — and proceed.

**If no QA plan exists**: do not silently proceed. Surface this explicitly:

> "This sprint has no QA plan. A sprint plan without a QA plan means test requirements are undefined — developers won't know what 'done' looks like from a QA perspective, and the sprint cannot pass the Production → Polish gate without one.
>
> Run `$qa-plan sprint` now, before starting any implementation. It takes one session and produces the test case requirements each story needs."

Ask the user directly:
- Prompt: "No QA plan found for this sprint. How do you want to proceed?"
- Options:
  - `[A] Run $qa-plan sprint now — I'll do that before starting implementation (Recommended)`
  - `[B] Skip for now — I understand QA sign-off will be blocked at the Production → Polish gate`

If [A]: keep the pending sprint unchanged and make `$qa-plan sprint` the first
post-write instruction.
If [B]: add this warning block to the pending sprint plan before any write:

```markdown
> ⚠️ **No QA Plan**: This sprint was started without a QA plan. Run `$qa-plan sprint`
> before the last story is implemented. The Production → Polish gate requires a QA
> sign-off report, which requires a QA plan.
```

After the QA choice is resolved, present the one complete changeset with exact
paths: `production/sprints/sprint-[NNN].md`, `production/sprint-status.yaml`, and
`production/review-mode.txt` only when a new value is pending. Verify that the
markdown and YAML story IDs, paths, and statuses correspond one-to-one. Obtain
one authorization, then write all pending files together. On success, verdict
**COMPLETE**. If authorization is declined or any pending file cannot be prepared,
write none and return **BLOCKED**.

After writing, add:

> **Scope check:** If this sprint includes stories added beyond the original epic scope, run `$scope-check [epic]` to detect scope creep before implementation begins.

---

## Phase 6: Next Steps

After the sprint plan is written and QA plan status is resolved:

- `$qa-plan sprint` — **required before implementation begins** — defines test cases per story so developers implement against QA specs, not a blank slate
- `$story-readiness [story-file]` — validate a story is ready before starting it
- `$dev-story [story-file]` — begin implementing the first story
- `$sprint-status` — check progress mid-sprint
- `$scope-check [epic]` — verify no scope creep before implementation begins

**Review mode configuration:** All director gates (producer feasibility, QA review, code review) respect the project review mode. The review mode is set in Phase 0 when the file does not exist (for `new` sprints), or can be overridden per-run with `--review full|lean|solo` as an argument. The file `production/review-mode.txt` contains one of:
- `lean` — skip automated director gates (default if file is absent — fastest for solo dev)
- `full` — run all director gates as spawned sub-agents
- `solo` — skip all gates unconditionally (single-developer, no review)

This file is read by `$sprint-plan`, `$story-readiness`, `$story-done`, and other skills at startup.
