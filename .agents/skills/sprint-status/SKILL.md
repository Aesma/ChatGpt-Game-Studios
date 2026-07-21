---
name: sprint-status
description: "Read-only sprint status check that resolves one explicit active sprint, validates tracker identity and freshness against plan/story hashes, recognizes In Review and recovery checkpoints, and refuses a health verdict on conflicting data."
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
files, and makes at most one concrete recommendation. It never uses file
modification time to select a sprint. If sprint identity or tracker freshness
cannot be proven, it returns `DATA CONFLICT` and stops before calculating or
printing a health verdict.

---

## 1. Resolve Exactly One Sprint

**Argument:** the first provided argument (blank = resolve the current sprint)

Read `production/sprint-status.yaml`, when it exists, and
`production/session-state/active.md` as selector inputs before choosing a
plan. Selection and status authority are separate decisions: a tracker may name
the active sprint but is not trusted for story status until Phase 3 passes every
identity and freshness check.

Apply this precedence:

1. **Explicit argument.** Normalize the requested sprint ID and find a plan
   under `production/sprints/` whose declared sprint ID matches it. A
   filename match is only a candidate; the ID inside the plan must agree.
2. **Tracker selector.** With no argument, use exactly one well-formed top-level
   `active_sprint_id` from `production/sprint-status.yaml`.
3. **Session selector.** If the tracker has no `active_sprint_id`, use
   exactly one active sprint ID or plan reference from
   `production/session-state/active.md`.
4. **Ask.** If no source resolves exactly one sprint, or a source contains
   multiple active sprint IDs, list the candidate IDs and paths and ask the user
   which sprint to inspect. Do not continue to status collection.

Never select the most recently modified file and never use mtime as a
tie-breaker. If the selected ID resolves to zero plans, report the missing ID and
source. If it resolves to multiple plans, report the ambiguity and ask; do not
pick one.

An explicit request for a historical sprint may ignore a tracker that
consistently identifies a different active sprint, but the report must mark that
tracker `NOT APPLICABLE — different active sprint` and use story/plan
fallback data. Without an explicit historical argument, disagreement between
the selected plan, tracker, and session-state active sprint is `DATA
CONFLICT`.

If `production/sprints/` does not exist or contains no plan and neither
selector names a sprint, report: "No active sprint found. Start a sprint with
`$sprint-plan new`." Then stop without a verdict.

Read the selected sprint plan in full. Extract:

- sprint ID/number and goal;
- explicit `plan_revision` and `updated_at`, if present;
- start date and end date; and
- every story/task stable ID, exact referenced path or inline entry, priority,
  owner, and estimate.

Record the selection source and selected plan path for the report.

---

## 2. Calculate Days Remaining

Using today's date and the sprint end date from the sprint file, calculate:
- Total sprint days (end minus start)
- Days elapsed
- Days remaining
- Percentage of time consumed

If the sprint file does not include explicit dates, note "Sprint dates not
found — burndown assessment skipped."

---

## 3. Validate the Tracker Before Reading Status

When `production/sprint-status.yaml` exists and applies to the selected
sprint, it may be used only after this complete fail-closed check. Required
top-level fields are:

- `sprint_id` — exact normalized selected sprint ID;
- `active_sprint_id` — exact normalized selected sprint ID for a current
  sprint report;
- `plan_revision` — exact match for the selected plan's explicit
  `plan_revision`;
- `story_set_hash` — `sha256:` plus 64 lowercase hexadecimal digits;
  and
- `updated_at` — a parseable ISO-8601 timestamp.

A legacy `sprint`, `generated`, or `updated` field is not a
substitute for the required contract. If the selected plan lacks an explicit
`plan_revision`, an applicable tracker exists but lacks a required field,
or a field is malformed, return `DATA CONFLICT`. Never fall back to
markdown to bypass a present but invalid applicable tracker.

### 3.1 Recompute the story-set hash

Resolve every plan entry before trusting tracker status. For each item produce
one canonical UTF-8 record:

`<story-id>\t<normalized-path-or-INLINE>\t<source-hash>`

Normalize path separators to `/`. The source hash is the SHA-256 of the
referenced story's raw bytes; for an inline item it is the SHA-256 of the exact
UTF-8 task entry; for a missing referenced file use the literal `MISSING`.
Sort records by story ID using code-point order, join them with LF and no trailing
LF, hash those exact bytes, and prefix the lowercase digest with `sha256:`.
Duplicate or missing stable story IDs make the contract unverifiable and
therefore `DATA CONFLICT`.

Require exact agreement among:

- selected ID, plan-declared ID, tracker `sprint_id`, and—on a current
  sprint report—tracker `active_sprint_id`;
- selected plan `plan_revision` and tracker `plan_revision`; and
- recomputed story-set hash and tracker `story_set_hash`.

The tracker `updated_at` must not predate a parseable plan
`updated_at` or any parseable status-update timestamp in the current story
set. Hash agreement, not timestamps alone, proves freshness.

For each tracker story, require one matching plan/story ID and normalize only
these equivalent lifecycle spellings:

| Story file | Tracker | Report |
|---|---|---|
| Complete or Done | done | DONE |
| In Review | review or in_review | IN REVIEW |
| In Progress | in-progress or in_progress | IN PROGRESS |
| Ready | ready-for-dev or ready_for_dev | READY |
| Not Started | backlog | NOT STARTED |
| Blocked | blocked | BLOCKED |

`IN REVIEW` is implemented but not accepted; it is never counted as
complete. A story/tracker status disagreement after normalization is `DATA
CONFLICT`, not a choice of which source to trust.

### 3.2 Recognize dev-story recovery evidence

For each story, check only the exact derived path
`production/session-state/dev-story-[story-id].yaml`. A checkpoint is
recovery evidence, never a status override or proof of completion.

An unresolved checkpoint must identify the same story ID/path, contain a
well-formed `plan_hash`, source hashes, baseline/current target hashes,
planned and actual write sets, test evidence or error, and an exact safe resume
point. Rehash every current path the checkpoint claims is current. Any malformed
hash, identity mismatch, or current-hash mismatch is `DATA CONFLICT` and
must show observed and expected values.

A valid unresolved PARTIAL or BLOCKED checkpoint requires both story and tracker
to remain IN PROGRESS. IN REVIEW together with such a checkpoint is `DATA
CONFLICT`: staged `$dev-story` permits IN REVIEW only after every
blocking test passes and no partial transaction remains. A valid checkpoint is
reported as `RECOVERY CHECKPOINT` with its plan hash and resume point; the
story is still not complete. A FAILED transaction that was fully restored is
not inferred from a checkpoint unless its recorded baseline hashes equal the
freshly rehashed files.

For an IN REVIEW story, validate the story's recorded plan hash, implementation
and evidence post-write hashes, and test evidence. A missing/malformed hash, a
nonzero test exit code, or an absent log hash contradicts the successful
dev-story projection and is `DATA CONFLICT`.

### 3.3 Conflict response

On any identity, revision, story-set, projection, checkpoint, or evidence
conflict, output only:

`DATA CONFLICT — sprint health not assessed.`

Then list the selected sprint ID/path, selection source, every source checked,
each expected and observed value, and one recovery owner/action. Do not count
stories, calculate completion, emit On Track/At Risk/Behind, or let the skill
repair any file.

### 3.4 Tracker-absent fallback

Only when no applicable tracker exists, scan the selected plan and referenced
story files:

1. Read exact referenced files and scan for DONE, COMPLETE, IN REVIEW, IN
   PROGRESS, READY, BLOCKED, or NOT STARTED (case-insensitive).
2. Scan the plan entry itself for an inline task.
3. If no marker is found, retain the existing fallback classification of NOT
   STARTED.
4. If a referenced file is absent, classify it MISSING.

Add: "⚠ No applicable `sprint-status.yaml` found — status inferred from
markdown. Run `$sprint-plan update` to generate a revisioned tracker."

Optionally search `src/` for a matching system slug as an evidence hint
only; it never changes status, source identity, counts, or verdict.

### Stale Story Detection

After collecting status for all stories, check each IN PROGRESS story for staleness:

- For each story that has a referenced file, read the file and look for a
  `Last Updated:` field in the frontmatter or header (e.g., `Last Updated: 2026-04-01`
  or `updated: 2026-04-01`). Accept any reasonable date field name: `Last Updated`,
  `Updated`, `last-updated`, `updated_at`.
- Calculate days since that date using today's date.
- If the date is more than 4 days ago, flag the story as **STALE**. (4-day threshold accounts for weekends — a story last touched on Friday won't appear stale until Wednesday.)
- If no date field is found in the story file, note "no timestamp — cannot check staleness."
- If the story has no referenced file (inline task), note "inline task — cannot check staleness."

STALE stories are included in the output table and collected into an "Attention Needed"
section (see Phase 5 output format).

**Stale story escalation**: If any IN PROGRESS story is flagged STALE (no progress in 4+ days), the burndown verdict
is upgraded to at least **At Risk** — even if the completion percentage is within the normal
On Track window. Record this escalation reason: "At Risk — [N] story(ies) with no progress in
[N] days."

---

## 4. Burndown Assessment

Calculate:
- Tasks complete (DONE or COMPLETE)
- Tasks in review (IN REVIEW; not complete)
- Tasks in progress (IN PROGRESS)
- Tasks blocked (BLOCKED)
- Tasks not started (NOT STARTED or MISSING)
- Completion percentage: (complete / total) * 100

Assess burndown by comparing completion percentage to time consumed percentage:

- **On Track**: completion % is within 10 points of time consumed % or ahead
- **At Risk**: completion % is 10-25 points behind time consumed %
- **Behind**: completion % is more than 25 points behind time consumed %

If dates are unavailable, skip the burndown assessment and report "On Track /
At Risk / Behind: unknown — sprint dates not found."

---

## 5. Output

Keep the output concise. The story status table is mandatory — do not truncate it. Aim for under 50 lines total; omit the Emerging Risks section if nothing notable was found. Use this format:

```markdown
## Sprint [N] Status — [Today's Date]
**Sprint Goal**: [from sprint plan]
**Selection**: [argument / tracker.active_sprint_id / session state] → [plan path]
**Sources**: plan revision [value]; tracker updated_at [value or N/A]; story_set_hash [value or fallback]
**Days Remaining**: [N] of [total] ([% time consumed])

### Progress: [complete/total] tasks ([%])

| Story / Task         | Priority   | Status      | Owner   | Blocker        |
|----------------------|------------|-------------|---------|----------------|
| [title]              | Must Have  | DONE        | [owner] |                |
| [title]              | Must Have  | IN REVIEW   | [owner] | awaiting review|
| [title]              | Must Have  | IN PROGRESS | [owner] |                |
| [title]              | Must Have  | BLOCKED     | [owner] | [brief reason] |
| [title]              | Should Have| NOT STARTED | [owner] |                |

### Attention Needed
| Story / Task         | Status      | Last Updated   | Days Stale | Note           |
|----------------------|-------------|----------------|------------|----------------|
| [title]              | IN PROGRESS | [date or N/A]  | [N days]   | [STALE / no timestamp — cannot check staleness / inline task — cannot check staleness] |

*(Omit this section entirely if no IN PROGRESS stories are stale or have timestamp concerns.)*

### Burndown: [On Track / At Risk / Behind]
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
All Must Haves complete. Team can pull from Should Have backlog.
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
- It does not change story status or reconcile conflicting projections
- It does not propose scope cuts (that is `$sprint-plan update`)
- It makes at most one recommendation per run

For more detail on a specific story, the user can read the story file directly
or run `$story-readiness [path]`.

For tracker identity/revision/hash conflicts, route the exact mismatch to the status recorder (normally `$sprint-plan update`; for a current dev-story recovery checkpoint, resume `$dev-story` from the recorded safe point).

For sprint replanning, use `$sprint-plan update`.
For end-of-sprint retrospective, use `$retrospective`.
