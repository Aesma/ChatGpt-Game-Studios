---
name: retrospective
description: "Generates a sprint or milestone retrospective by analyzing completed work, velocity, blockers, and patterns. Produces actionable insights for the next iteration."
---

## Invocation and execution

Invoke this workflow as `$retrospective`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[sprint-N|milestone-name]`. Treat bracketed values as optional unless the workflow says otherwise.


## Phase 1: Parse Arguments

Determine whether this is a sprint retrospective (`sprint-N`) or a milestone retrospective (`milestone-name`). Resolve one exact existing target and retain its identifier for every later data-source check. Do not allow a current status file to substitute for a different or historical target.

---

## Phase 1b: Check for Existing Retrospective

Before loading any data, search for an existing retrospective file:

- For sprint retrospectives: `production/retrospectives/retro-[sprint-slug]-*.md`
  (also check `production/sprints/sprint-[N]-retrospective.md` as an alternate location)
- For milestone retrospectives: `production/retrospectives/retro-[milestone-name]-*.md`

If a matching file is found, ask the user directly:
- Prompt: "An existing retrospective was found: [filename]. How do you want to proceed?"
- Options:
  - `[A] Update existing — load it and add/revise sections with new data`
  - `[B] Start fresh — generate a new retrospective (archive the old one)`

If [A]: read the existing file and carry its content forward, revising sections with new data.
If [B]: continue to Phase 2 with a blank slate. Do not rename anything yet.
The source path, archived target path, and new retrospective path must appear
in the same complete changeset preview. Immediately before applying it, verify
the existing file still matches the previewed baseline; on any conflict, stop
without moving or overwriting either version.

---

## Phase 2: Load Sprint or Milestone Data

Read the sprint or milestone plan from the appropriate location:

- Sprint plans: `production/sprints/`
- Milestone definitions: `production/milestones/`

**Also check for `production/sprint-status.yaml`**: use it only when its sprint
identifier matches the exact retrospective target. For a matching sprint it is
the primary source for actual story completion status; otherwise report it as
unrelated and do not use it. A milestone retrospective aggregates only the
sprints/goals explicitly included by the milestone artifact and never imports
an unrelated current sprint status. Note discrepancies between matching status
and plan sources.

**If the file does not exist or is empty**, output:

> "No sprint data found for [sprint/milestone]. Run `$sprint-status` to generate
> sprint data first, or provide the sprint details manually."

Then ask the user directly to present two options:

- **[A] Provide data manually** — ask the user to paste or describe the sprint
  tasks, dates, and outcomes; use that as the source of truth for the retrospective.
- **[B] Stop** — abort the skill. Verdict: **BLOCKED** — no sprint data available.

If the user chooses [A], collect the data and continue to Phase 3 using what they provide.
If the user chooses [B], stop here.

Extract: planned tasks, estimated effort, owners, and goals.

Actual effort, bug counts, estimation accuracy, and historical velocity may be
calculated only when existing sprint/status/bug/retrospective artifacts explicitly
provide the required values. Missing inputs must be written as
`N/A — source unavailable`; do not infer time spent from commits or completion dates.

Run Git history read-only for the sprint period to understand what was actually committed and when:

```
git log --oneline --since="4 weeks ago"
```

Adjust the `--since` date to match the sprint duration if known from the sprint plan. If the dated query fails or returns no usable history, fall back to `git log --oneline -20`.

---

## Phase 3: Analyze Completion and Trends

Scan for completed and incomplete tasks by comparing the plan against actual deliverables. Check for:

- Tasks completed as planned
- Tasks completed but modified from the plan
- Tasks carried over (not completed)
- Tasks added mid-sprint (unplanned work)
- Tasks removed or descoped

Scan the codebase for TODO/FIXME trends:

- Count current TODO/FIXME/HACK comments
- Compare to previous sprint counts if available (check previous retrospectives)
- Note whether technical debt is growing or shrinking

Read previous retrospectives (if any) from `production/retrospectives/` to check:

- Were previous action items addressed?
- Are the same problems recurring?
- How has velocity trended?

---

## Phase 4: Generate the Retrospective

Keep every metric source-traceable. Use `N/A — source unavailable` for any
actual effort, bug count, estimation accuracy, or velocity input not explicitly
present in an existing artifact.

```markdown
## Retrospective: [Sprint N / Milestone Name]
Period: [Start Date] -- [End Date]
Generated: [Date]

### Metrics

| Metric | Planned | Actual | Delta |
|--------|---------|--------|-------|
| Tasks | [X] | [Y] | [+/- Z] |
| Completion Rate | -- | [Z%] | -- |
| Story Points / Effort Days | [X] | [Y] | [+/- Z] |
| Bugs Found | -- | [N] | -- |
| Bugs Fixed | -- | [N] | -- |
| Unplanned Tasks Added | -- | [N] | -- |
| Commits | -- | [N] | -- |

### Velocity Trend

| Sprint | Planned | Completed | Rate |
|--------|---------|-----------|------|
| [N-2] | [X] | [Y] | [Z%] |
| [N-1] | [X] | [Y] | [Z%] |
| [N] (current) | [X] | [Y] | [Z%] |

**Trend**: [Increasing / Stable / Decreasing]
[One sentence explaining the trend]

### What Went Well
- [Observation backed by specific data or examples]
- [Another positive observation]
- [Recognize specific contributions or decisions that paid off]

### What Went Poorly
- [Specific issue with measurable impact -- e.g., "Feature X took 5 days
  instead of estimated 2, blocking tasks Y and Z"]
- [Another issue with impact]
- [Do not assign blame -- focus on systemic causes]

### Blockers Encountered

| Blocker | Duration | Resolution | Prevention |
|---------|----------|------------|------------|
| [What blocked progress] | [How long] | [How it was resolved] | [How to prevent recurrence] |

### Estimation Accuracy

| Task | Estimated | Actual | Variance | Likely Cause |
|------|-----------|--------|----------|--------------|
| [Most overestimated task] | [X] | [Y] | [+Z] | [Why] |
| [Most underestimated task] | [X] | [Y] | [-Z] | [Why] |

**Overall estimation accuracy**: [X%] of tasks within +/- 20% of estimate

[Analysis: Are we consistently over- or under-estimating? For which types of
tasks? What adjustment should we apply?]

### Carryover Analysis

| Task | Original Sprint | Times Carried | Reason | Action |
|------|----------------|---------------|--------|--------|
| [Task that was not completed] | [Sprint N-X] | [N] | [Why] | [Complete / Descope / Redesign] |

### Technical Debt Status
- Current TODO count: [N] (previous: [N])
- Current FIXME count: [N] (previous: [N])
- Current HACK count: [N] (previous: [N])
- Trend: [Growing / Stable / Shrinking]
- [Note any areas of concern]

### Previous Action Items Follow-Up

| Action Item (from Sprint N-1) | Status | Notes |
|-------------------------------|--------|-------|
| [Previous action] | [Done / In Progress / Not Started] | [Context] |

### Action Items for Next Iteration

| # | Action | Owner | Priority | Deadline |
|---|--------|-------|----------|----------|
| 1 | [Specific, measurable action] | [Who] | [High/Med/Low] | [When] |
| 2 | [Another action] | [Who] | [Priority] | [When] |

### Process Improvements
- [Specific change to how we work, with expected benefit]
- [Another improvement -- keep it to 2-3 actionable items, not a wish list]

### Summary
[2-3 sentence overall assessment: Was this a good sprint/milestone? What is
the single most important thing to change going forward?]
```

---

## Phase 5: Save Retrospective

Present the retrospective and top findings to the user (completion rate, velocity trend, top blocker, most important action item).

Add this proposed file or edit to the complete changeset preview; do not write
it until that changeset is authorized. Use
`production/retrospectives/retro-[sprint-slug]-[date].md` for a sprint or
`production/retrospectives/retro-[milestone-name]-[date].md` for a milestone.
If Start fresh was selected, the archive move and new file are part of this
same changeset.

Once the complete changeset is authorized, write the file, creating the `production/retrospectives/` directory if needed. Verdict: **COMPLETE** — retrospective saved.

If the complete changeset is not authorized, stop here. Verdict: **BLOCKED** — changeset not authorized.

---

## Phase 6: Next Steps

End after saving or declining the retrospective. Provide the generated file
path and relevant existing commands as optional handoffs:

- `$sprint-plan new` may consume the retrospective when the user invokes it later.
- For a milestone, `$gate-check` may be run later as a separate explicit workflow.

Do not invoke either workflow from this retrospective run.

### Guidelines

- Be honest and specific. Vague retrospectives produce vague improvements.
- Focus on systemic issues, not individual blame.
- Limit action items to 3-5.
- Do not assign an owner, deadline, or cause unless an artifact or the user supplies it.
- For milestone retrospectives, evaluate only explicitly included goals and sprints.
