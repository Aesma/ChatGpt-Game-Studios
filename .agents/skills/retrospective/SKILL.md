---
name: retrospective
description: "Generates an evidence-backed sprint or milestone retrospective while preserving unsupported metrics and causes as UNKNOWN."
---

## Invocation and execution

Invoke this workflow as `$retrospective`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[sprint-N|milestone-name]`. Treat bracketed values as optional unless the workflow says otherwise.

This workflow creates only the retrospective artifact. It never invokes planning, a gate, another skill, or another task.

## Phase 1: Parse Arguments

Determine whether this is a sprint retrospective (`sprint-N`) or a milestone retrospective (`milestone-name`).

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
If [B]: continue to Phase 2 with a blank slate. Before writing the new file, rename the existing one with a `-archived-[date]` suffix.

---

## Phase 2: Load Sprint or Milestone Data

Read the sprint or milestone plan from the appropriate location:

- Sprint plans: `production/sprints/`
- Milestone definitions: `production/milestones/`

**Also check for `production/sprint-status.yaml`**: if it exists, read it alongside the sprint plan. It is the primary source for recorded story completion status (status, completion dates, blockers), but it is not authority for unrelated values such as actual effort or bug counts. Fall back to markdown scanning only if the YAML does not exist. Note discrepancies between the YAML and the sprint plan; do not choose a side silently or calculate a metric from conflicting records.

**If the file does not exist or is empty**, output:

> "No sprint data found for [sprint/milestone]. Run `$sprint-status` to generate
> sprint data first, or provide the sprint details manually."

Then ask the user directly to present two options:

- **[A] Provide data manually** — ask the user to paste or describe the sprint
  tasks, dates, and outcomes; record those claims as `user-provided` evidence.
- **[B] Stop** — abort the skill. Verdict: **BLOCKED** — no sprint data available.

If the user chooses [A], collect the data and continue to Phase 3 using what they provide.
If the user chooses [B], stop here.

Extract recorded planned tasks, estimated effort, owners, goals, dates, completion events, blockers, bug events, and scope changes. Do not turn an absent field into zero, false, completed, or not completed.

Run Git history read-only for the sprint period to understand what was committed and when:

```text
git log --oneline --since="4 weeks ago"
```

Adjust the `--since` date to match the sprint duration if known from the sprint plan. If the dated query fails or returns no usable history, fall back to `git log --oneline -20`. A fallback query is context only: unless its commits can be tied to the target period, report the `Commits` metric as `UNKNOWN`.

### Evidence ledger

Create an in-memory evidence ledger before calculating or drafting anything. Give each item a stable ID such as `SRC-001` and record:

- source type (`plan`, `status`, `git`, `bug-record`, `delivery-artifact`, `prior-retro`, or `user-provided`);
- exact file path, commit range, or user-message locator;
- the target period and story/task scope the item actually covers;
- the claim or field supported by the item; and
- any ambiguity or conflict.

Every reported metric must use exactly one of these evidence states:

- `OBSERVED` — a value is stated directly in one or more in-scope evidence items;
- `DERIVED` — a deterministic calculation uses only supported inputs; record the formula and all input evidence IDs;
- `UNKNOWN` — a required input is absent, ambiguous, conflicting, out of period, or incomparable.

For every metric, record the state, value, source IDs, derivation when applicable, and confidence (`HIGH`, `MEDIUM`, `LOW`, or `NONE`). `UNKNOWN` always has value `UNKNOWN`, confidence `NONE`, and a short missing-evidence reason. Never estimate, interpolate, or substitute a plausible value.

---

## Phase 3: Analyze Completion and Trends

Compare the plan against recorded deliverables and completion events. Check for:

- tasks completed as planned;
- tasks completed but modified from the plan;
- tasks carried over (not completed);
- tasks added mid-sprint (unplanned work); and
- tasks removed or descoped.

Classify an item only when evidence supports that classification. Otherwise preserve its status as `UNKNOWN` and identify the missing or conflicting evidence.

Use the following minimum evidence rules:

| Metric or claim | Acceptable support | Forbidden inference |
|---|---|---|
| Planned tasks or effort | Target plan or explicit user statement | Reconstructing the plan from commits |
| Completed tasks | In-scope status/completion record or verified deliverable mapped to the task | Treating a commit or missing TODO as completion |
| Actual effort | Explicit time/effort record or explicit user statement | Estimating effort from commits, dates, or task complexity |
| Bugs found/fixed | In-scope bug event records or explicit user statement | Counting bug-like commit messages or assuming no record means zero |
| Unplanned work | Recorded scope change or explicit user statement | Treating every unmatched commit as a task |
| Commits | Git range objectively bounded to the target period | Counting the fallback history as period activity |

Calculate `Delta`, completion rate, estimation accuracy, and any trend only when every input is supported. If any required input is `UNKNOWN`, the result is also `UNKNOWN`; include no approximate result.

Scan the codebase for current TODO/FIXME/HACK comments. Record the scan scope, command or method, and repository revision as evidence. Compare against a previous count only when that retrospective documents a compatible scan scope and method. Otherwise keep the trend `UNKNOWN`.

Read previous retrospectives from `production/retrospectives/` to check whether prior action items were recorded as addressed and whether supported, comparable metrics exist. A retrospective's conclusion is not independent evidence for the underlying metric unless it cites its sources.

### Causes and explanations

A cause, blocker resolution, prevention claim, trend explanation, or carryover reason may be stated as fact only when an in-scope event record says it or the user explicitly confirms it. Cite the supporting evidence ID beside the claim.

When no such evidence exists, write `UNKNOWN — no event record or user confirmation`. Do not infer a likely cause from timing, correlation, commit messages, task type, or general experience. You may ask the user to confirm a cause; until confirmation, keep it `UNKNOWN`.

---

## Phase 4: Generate the Retrospective

Use `UNKNOWN` literally wherever evidence is insufficient. Do not omit an expected row merely because its value is unknown.

```markdown
## Retrospective: [Sprint N / Milestone Name]
Period: [Start Date or UNKNOWN] -- [End Date or UNKNOWN]
Generated: [Date]

### Evidence Summary

| Evidence ID | Source | Locator | Supported Scope / Claim | Limitations |
|-------------|--------|---------|-------------------------|-------------|
| SRC-001 | [plan/status/etc.] | [path/range/message] | [claim] | [none or limitation] |

### Metrics

| Metric | Planned | Actual | Delta | State | Evidence / Formula | Confidence |
|--------|---------|--------|-------|-------|--------------------|------------|
| Tasks | [X or UNKNOWN] | [Y or UNKNOWN] | [Z or UNKNOWN] | [OBSERVED/DERIVED/UNKNOWN] | [SRC IDs and formula, or missing-evidence reason] | [HIGH/MEDIUM/LOW/NONE] |
| Completion Rate | -- | [Z% or UNKNOWN] | -- | [DERIVED/UNKNOWN] | [formula + SRC IDs, or reason] | [confidence] |
| Story Points / Effort Days | [X or UNKNOWN] | [Y or UNKNOWN] | [Z or UNKNOWN] | [state] | [evidence/formula/reason] | [confidence] |
| Bugs Found | -- | [N or UNKNOWN] | -- | [state] | [evidence/reason] | [confidence] |
| Bugs Fixed | -- | [N or UNKNOWN] | -- | [state] | [evidence/reason] | [confidence] |
| Unplanned Tasks Added | -- | [N or UNKNOWN] | -- | [state] | [evidence/reason] | [confidence] |
| Commits | -- | [N or UNKNOWN] | -- | [state] | [evidence/reason] | [confidence] |

### Velocity Trend

| Sprint | Planned | Completed | Rate | Evidence | Confidence |
|--------|---------|-----------|------|----------|------------|
| [N-2] | [value/UNKNOWN] | [value/UNKNOWN] | [value/UNKNOWN] | [SRC IDs/reason] | [confidence] |
| [N-1] | [value/UNKNOWN] | [value/UNKNOWN] | [value/UNKNOWN] | [SRC IDs/reason] | [confidence] |
| [N] (current) | [value/UNKNOWN] | [value/UNKNOWN] | [value/UNKNOWN] | [SRC IDs/reason] | [confidence] |

**Trend**: [Increasing / Stable / Decreasing / UNKNOWN]
[Evidence-backed explanation, or `UNKNOWN — comparable supported history is unavailable`]

### What Went Well
- [Observation with evidence ID]
- [Another supported observation, or UNKNOWN]

### What Went Poorly
- [Supported issue and impact with evidence ID]
- [Another supported issue, or UNKNOWN]

### Blockers Encountered

| Blocker | Duration | Resolution | Prevention | Evidence |
|---------|----------|------------|------------|----------|
| [blocker/UNKNOWN] | [duration/UNKNOWN] | [resolution/UNKNOWN] | [prevention/UNKNOWN] | [SRC IDs/reason] |

### Estimation Accuracy

| Task | Estimated | Actual | Variance | Cause | Evidence / Formula | Confidence |
|------|-----------|--------|----------|-------|--------------------|------------|
| [task] | [value/UNKNOWN] | [value/UNKNOWN] | [value/UNKNOWN] | [confirmed cause or UNKNOWN] | [SRC IDs/formula/reason] | [confidence] |

**Overall estimation accuracy**: [supported result or UNKNOWN]

[Evidence-backed analysis, or `UNKNOWN — supported estimate/actual pairs are unavailable`]

### Carryover Analysis

| Task | Original Sprint | Times Carried | Reason | Action | Evidence |
|------|----------------|---------------|--------|--------|----------|
| [task] | [value/UNKNOWN] | [value/UNKNOWN] | [confirmed reason/UNKNOWN] | [proposed action] | [SRC IDs/reason] |

### Technical Debt Status
- Current TODO count: [N or UNKNOWN] (previous: [N or UNKNOWN])
- Current FIXME count: [N or UNKNOWN] (previous: [N or UNKNOWN])
- Current HACK count: [N or UNKNOWN] (previous: [N or UNKNOWN])
- Trend: [Growing / Stable / Shrinking / UNKNOWN]
- Evidence: [scan scope, method, revision, and comparable prior source; or reason]

### Previous Action Items Follow-Up

| Action Item (from Sprint N-1) | Status | Notes | Evidence |
|-------------------------------|--------|-------|----------|
| [previous action] | [Done / In Progress / Not Started / UNKNOWN] | [context] | [SRC IDs/reason] |

### Action Items for Next Iteration

| # | Action | Owner | Priority | Deadline | Triggering Evidence |
|---|--------|-------|----------|----------|---------------------|
| 1 | [specific, measurable action] | [who] | [High/Med/Low] | [when] | [SRC IDs] |
| 2 | [another action] | [who] | [priority] | [when] | [SRC IDs] |

### Process Improvements
- [Specific change tied to supported evidence]
- [Another supported improvement]

### Data Gaps
- [Each UNKNOWN field and the evidence needed to resolve it]

### Summary
[2-3 sentence evidence-backed assessment. Do not convert UNKNOWN metrics or causes into a qualitative conclusion.]
```

Before presenting the draft, audit every number, percentage, delta, trend, cause, and explanation against the evidence ledger. Replace any unsupported value or claim with `UNKNOWN` and state why.

---

## Phase 5: Save Retrospective

Present the retrospective and top supported findings to the user. If completion rate, velocity trend, top blocker, or most important action item is unsupported, present it as `UNKNOWN` rather than filling it in.

Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized. (or `production/retrospectives/retro-[milestone-name]-[date].md` for milestone retrospectives)

Once the complete changeset is authorized, write the file, creating the `production/retrospectives/` directory if needed. Verdict: **COMPLETE** — retrospective saved.

If the complete changeset is not authorized, stop here. Verdict: **BLOCKED** — changeset not authorized.

---

## Phase 6: Return Artifact and Stop

After the retrospective is saved:

1. Return the saved artifact path and `Verdict: COMPLETE`.
2. Optionally list relevant commands the user could run in a new task, as plain text only.
3. Stop the workflow immediately.

Do not invoke `$sprint-plan`, `$gate-check`, or any other skill. Do not start planning, evaluate phase readiness, open another task, or pass retrospective data into another workflow. This rule applies to both sprint and milestone retrospectives, regardless of review mode or user interest in the next phase. A later planning or gate workflow requires an explicit command in a new task.

### Guidelines

- Be honest and specific. Unsupported precision is not useful specificity.
- Focus on systemic issues, not individual blame.
- Limit action items to 3-5. More than that dilutes focus.
- Every action item must have an owner and a deadline.
- Check whether previous action items were completed. Recurring unaddressed items are a process smell.
- If this is a milestone retrospective, report only evidence-backed milestone outcomes; do not evaluate or invoke readiness gates.
- `UNKNOWN` is a valid and required result when evidence is missing. It is never equivalent to zero, none, false, or not applicable.
