---
name: sprint-status
description: "Fast sprint status check. Resolves the active sprint from session state, sprint-status YAML, or numbered sprint files, then scans story status and produces a concise progress snapshot with burndown assessment and emerging risks. Run at any time during a sprint for quick situational awareness. Use when user asks 'how is the sprint going', 'sprint update', 'show sprint progress'."
---

## Invocation and execution

Invoke this workflow as `$sprint-status`.

Arguments: `[sprint-number or blank for current]`. Treat bracketed values as optional unless the workflow says otherwise.


# Sprint Status

This is a fast situational awareness check, not a sprint review. It reads the
current sprint plan and story files, scans for status markers, and produces a
concise snapshot in under 30 lines. For detailed sprint management, use
`$sprint-plan update` or `$milestone-review`.

**This skill is read-only.** It never proposes changes, never asks to write
files, and makes at most one concrete recommendation.

---

## 1. Find the Sprint

**Argument:** the first provided argument (blank = use current sprint)

- If an argument is given (e.g., `$sprint-status 3`), search
  `production/sprints/` for a file matching `sprint-03.md`, `sprint-3.md`,
  or similar. Report which file was found.
- If no argument is given, first read `production/session-state/active.md` and
  use an explicit sprint path or number recorded there. If that reference is
  absent or invalid, use the `sprint` value in `production/sprint-status.yaml`.
  If neither source resolves a sprint, choose the highest valid sprint number
  in `production/sprints/` (never modification time) and report why fallback was
  required.
- If `production/sprints/` does not exist or is empty, report: "No sprint
  files found. Start a sprint with `$sprint-plan new`." Then stop.

Read the sprint file in full. Extract:
- Sprint number and goal
- Start date and end date
- All story or task entries with their priority (Must Have / Should Have /
  Nice to Have), owner, and estimate

---

## 2. Calculate Days Remaining

Using today's date and valid sprint start/end dates, calculate calendar-day
differences consistently. Clamp elapsed days and time consumed to 0–100% for a
sprint that has not started or has already ended; days remaining cannot become
negative. If start equals end, either date is invalid, or an explicit date is
missing, report the affected values as `unknown`, skip percentage division, and
note "Sprint dates invalid or not found — burndown assessment skipped."

---

## 3. Scan Story Status

**First: check for `production/sprint-status.yaml`.**

Parse it only when it is valid YAML, has a sprint identifier, and has
`stories` as a list. If parsing fails or these required shapes are missing,
label the YAML `unusable` with the reason and use the existing markdown
fallback without guessing. When valid and its `sprint` value equals the target
sprint number, it is authoritative: extract each story's status plus `goal`,
`start`, and `end`. When it belongs to another sprint, state that fact and ignore it for
the requested target; use the markdown/story fallback below. This prevents an
explicit historical request from being replaced by current singleton state.

Map existing YAML values to report labels as follows:
- `backlog` and `ready` → `NOT STARTED`
- `in_progress` → `IN PROGRESS`
- `review` → `IN REVIEW`
- `done` → `DONE`
- `blocked` → `BLOCKED`
For read compatibility, accept legacy `ready-for-dev` and `in-progress`, but
all future writers use canonical `ready` and `in_progress`; never rewrite legacy
values during this read-only workflow.

**If `sprint-status.yaml` is missing or belongs to another sprint** (legacy or
historical sprint), fall back to markdown scanning:

1. If the entry references a story file path, check if the file exists. Read
   only its header/frontmatter `Status:` field; words such as "complete" or
   "blocked" in acceptance criteria or prose never determine status.
2. If the entry has no file path (inline task in the sprint plan), parse only
   the status column/value on that same task-table row.
3. If no status marker is found, classify as NOT STARTED.
4. If a file is referenced but does not exist, classify as MISSING and note it.

When using the fallback, add a note at the bottom of the output:
"⚠ No `sprint-status.yaml` found — status inferred from markdown. Run `$sprint-plan update` to generate one."

Optionally (fast check only — do not do a deep scan): search `src/` for a
directory or file name that matches the story's system slug. Report any result
only as an `unverified implementation hint`; it never changes story status,
completion percentage, or sprint health.

### Stale Story Detection

After collecting status for all stories, check each IN PROGRESS story for staleness:

- For each story that has a referenced file, read the file and look for a
  `Last Updated:` field in the frontmatter or header (e.g., `Last Updated: 2026-04-01`
  or `updated: 2026-04-01`). Accept any reasonable date field name: `Last Updated`,
  `Updated`, `last-updated`, `updated_at`.
- Calculate days since that date using today's date.
- If the date is more than 4 days ago, flag the story as **STALE**. (4-day threshold accounts for weekends — a story last touched on Friday won't appear stale until Wednesday.)
- If no date field is found in the story file, use a `Last Updated` value from
  `active.md` only when it explicitly identifies the same story. Otherwise note
  "no timestamp — cannot check staleness." Story-file evidence always wins.
- If the story has no referenced file (inline task), note "inline task — cannot check staleness."

STALE stories are included in the output table and collected into an "Attention Needed"
section (see Phase 5 output format).

**Stale story escalation**: If any IN PROGRESS story is flagged STALE (no progress in 4+ days), the burndown verdict
is upgraded to at least **AT RISK** — even if the completion percentage is within the normal
ON TRACK window. Record this escalation reason: "AT RISK — [N] story(ies) with no progress in
[N] days."

---

## 4. Burndown Assessment

Calculate:
- Tasks complete (DONE or COMPLETE)
- Tasks in progress (IN PROGRESS)
- Tasks blocked (BLOCKED)
- Tasks not started (NOT STARTED)
- Missing referenced tasks (MISSING), retained as a distinct data-quality label
- Completion percentage: (complete / total) * 100, with MISSING still included
  in the denominator but never described as normal not-started work

Assess burndown by comparing completion percentage to time consumed percentage:

- **ON TRACK**: completion is ahead or no more than 10 percentage points behind
  time consumed (`gap <= 10`)
- **AT RISK**: the gap is greater than 10 and at most 25 points
  (`10 < gap <= 25`)
- **BEHIND**: the gap is greater than 25 points

These are the only sprint-health verdicts. A story-level `BLOCKED` status is a
risk reason, never a sprint-health verdict. If all Must Haves are done, health is
still ON TRACK and the completion flag below is added.

If dates are unavailable, skip the burndown assessment and report "ON TRACK /
AT RISK / BEHIND: unknown — sprint dates not found."

---

## 5. Output

Keep the output concise. The story status table is mandatory — do not truncate it. Aim for under 50 lines total; omit the Emerging Risks section if nothing notable was found. Use this format:

```markdown
## Sprint [N] Status — [Today's Date]
**Sprint Goal**: [from sprint plan]
**Days Remaining**: [N] of [total] ([% time consumed])

### Progress: [complete/total] tasks ([%])

| Story / Task         | Priority   | Status      | Owner   | Blocker        |
|----------------------|------------|-------------|---------|----------------|
| [title]              | Must Have  | DONE        | [owner] |                |
| [title]              | Must Have  | IN PROGRESS | [owner] |                |
| [title]              | Must Have  | BLOCKED     | [owner] | [brief reason] |
| [title]              | Should Have| NOT STARTED | [owner] |                |

### Attention Needed
| Story / Task         | Status      | Last Updated   | Days Stale | Note           |
|----------------------|-------------|----------------|------------|----------------|
| [title]              | IN PROGRESS | [date or N/A]  | [N days]   | [STALE / no timestamp — cannot check staleness / inline task — cannot check staleness] |

*(Omit this section entirely if no IN PROGRESS stories are stale or have timestamp concerns.)*

### Burndown: [ON TRACK / AT RISK / BEHIND]
[1-2 sentences. If behind: which Must Haves are at risk. If on track: confirm
and note any Should Haves the team could pull.]

### Must-Haves at Risk
[List any Must Have stories that are BLOCKED or NOT STARTED with less than
40% of sprint time remaining. If none, write "None."]

### Emerging Risks
[Any risks visible from the story scan: missing files, cascading blockers,
stories with no owner. If none, write "None identified."]

### Recommendation
[One concrete action, or "Sprint is on track — no action needed."]
```

---

## 6. Fast Escalation Rules

Apply these rules before outputting, and place the flag at the TOP of the
output if triggered (above the status table):

**Critical flag** — if Must Have stories are BLOCKED or NOT STARTED and
less than 40% of the sprint time remains:

```
SPRINT AT RISK: [N] Must Have stories are not complete with [X]% of sprint
time remaining. Recommend replanning with `$sprint-plan update`.
```

**Completion flag** — if all Must Have stories are DONE:

```
ON TRACK — all Must Haves complete. Team can pull from Should Have backlog.
```

**Missing stories flag** — if any referenced story files do not exist:

```
NOTE: [N] story files referenced in the sprint plan are missing.
Run `$story-readiness sprint` to validate story file coverage.
```

---

## Collaborative Protocol

This skill is read-only. It reports observed facts from files on disk.

- It does not update the sprint plan
- It does not change story status
- It does not propose scope cuts (that is `$sprint-plan update`)
- It makes at most one recommendation per run

For more detail on a specific story, the user can read the story file directly
or run `$story-readiness [path]`.

For sprint replanning, use `$sprint-plan update`.
For end-of-sprint retrospective, use `$retrospective`.
