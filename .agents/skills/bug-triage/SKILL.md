---
name: bug-triage
description: "Read all open bugs in production/qa/bugs/, re-evaluate priority vs. severity, propose sprint placement, surface systemic trends, and produce a triage report. Run at sprint start or when the bug count grows enough to need re-prioritization."
---

## Invocation and execution

Invoke this workflow as `$bug-triage`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[sprint | full | trend]`. Treat bracketed values as optional unless the workflow says otherwise.


# Bug Triage

This skill processes the open bug backlog into a prioritised action list with
proposed sprint placement. It does not update a bug or sprint plan, so a report
entry is never a persisted assignment. It distinguishes between **severity** (how bad is the impact?) and
**priority** (how urgently must we fix it?), detects systemic trends, and
ensures no critical bug is lost between sprints.

**Output:** `production/qa/bug-triage-[date].md`

**When to run:**
- Sprint start — propose placement of open bugs for the new sprint or backlog
- After `$team-qa` completes and new bugs have been filed
- When the bug count crosses 10+ open items

---

## 1. Parse Arguments

**Modes:**
- `$bug-triage sprint` — triage against the current sprint; propose fixable bugs
  for the sprint backlog and recommend backlog disposition for the rest
- `$bug-triage full` — full triage of all bugs regardless of sprint scope
- `$bug-triage trend` — trend analysis only (no assignment recommendations);
  it may still save the same report in Step 6 when authorized
- No argument — run sprint mode if a current sprint exists, else full mode

---

## 2. Load Bug Backlog

### Step 2a — Discover bug files

Search for bug-report files in priority order:
1. `production/qa/bugs/*.md` — individual bug report files (preferred format)
2. `production/qa/bugs.md` — single consolidated bug log (fallback)
3. Any `production/qa/qa-plan-*.md` "Bugs Found" table (last resort)

If no bug files found:
> "No bug files found in `production/qa/bugs/`. If bugs are tracked in a
> different location, adjust the file pattern. If no bugs exist yet, there is
> nothing to triage."

Stop and report. Do not proceed if no bugs exist.

### Step 2b — Load sprint context

Read existing sprint status/content and select a sprint only when its own
active/current marker uniquely identifies it. Do not infer the active sprint from
file modification time. If no sprint is uniquely active, triage to backlog only.
From the active sprint, understand:
- Current sprint number / name
- Stories in scope (for assignment target)
- Sprint capacity constraints (if noted)

If no sprint file exists: note "No sprint plan found — backlog recommendations only."

### Step 2c — Load severity reference

Read `.codex/docs/coding-standards.md` for severity/priority definitions if they
exist. If they do not exist, use the standard definitions in Step 3.

---

## 3. Classify Each Bug

For each bug, first parse the top-level Status. Include only `Open` in the open
backlog. Exclude `Verified Fixed` and `Closed`. Put a missing/unknown Status in a
malformed section with its file evidence rather than treating it as open. Also
flag empty reproduction steps and possible duplicates based on same-system
symptoms/title; do not merge, close, or delete them.

Then extract or infer:

### Severity (impact of the bug)

| Severity | Definition |
|----------|-----------|
| **S1 — Critical** | Game crashes, data loss, or complete feature failure. Cannot proceed past this point. |
| **S2 — Major** | Major feature broken but game is still playable. Significant wrong behaviour. |
| **S3 — Minor** | Feature degraded but a workaround exists. Minor wrong behaviour. |
| **S4 — Trivial** | Visual glitch, cosmetic issue, typo. No gameplay impact. |

### Priority (urgency of the fix)

| Priority | Definition |
|----------|-----------|
| **P1 — Immediate** | Blocks QA, blocks release, or is regression from last sprint |
| **P2 — Next Sprint** | Should be resolved before the next major milestone |
| **P3 — Backlog** | Would be good to fix, but no active blocking impact |
| **P4 — Wishlist** | Candidate for deferral or possible out-of-scope disposition; user decision required |

### Proposed Assignment

For each P1/P2 bug in `sprint` mode:
- Identify which story or epic the fix belongs to
- Compare remaining capacity and bug effort only when both use the same existing
  unit and every proposed item has an estimate in that unit
- If comparable capacity exists: record a proposed placement (`Proposed Sprint: [current]`)
- If capacity is full or unknown/incomparable: keep it unassigned and flag
  `Priority overflow` or `Capacity unknown`

For `full` mode, apply the same comparable-capacity rule as sprint mode. Propose
P1 for the current sprint only while remaining capacity exists; overflow stays
unassigned. Propose P2 for the next sprint only when its active plan and comparable
capacity are known. Trend mode skips this entire Assignment subsection. Never
auto-assign merely because the mode is `full`.

### Deviation check

Flag bugs that suggest **systematic problems**:
- 3+ bugs from the same system in the same sprint → "Potential design or
  implementation quality issue in [system]"
- 2+ S1/S2 bugs in the same story → "Story may need to be reopened and
  re-reviewed before shipping"
- Bug filed against a story marked Complete → "Regression in completed story —
  story should be re-opened in sprint tracking"

---

## 4. Trend Analysis

After classifying all bugs, generate trend metrics. A missing filed/closed date,
sprint link, or story link is `Unknown / insufficient data`, not zero, and is
excluded from derived counts, ages, ratios, and hotspot claims:

### Volume trends
- Total open bugs: [N]
- Opened this sprint: [N]
- Closed this sprint: [N]
- Net change: [+N / -N]

### System hot spots
- Which system has the most open bugs?
- Which system has the highest S1/S2 ratio?

### Age analysis
- How many bugs are older than 2 sprints?
- Are any S1/S2 bugs un-assigned (sprint = none)?

### Regression indicator
- Any bugs filed against previously-completed stories?
- Count: [N] regression bugs (story reopened implied)

---

## 5. Generate Triage Report

```markdown
# Bug Triage Report

> **Date**: [date]
> **Mode**: [sprint | full | trend]
> **Generated by**: $bug-triage
> **Open bugs processed**: [N]
> **Sprint in scope**: [sprint name, or "N/A"]

---

## Triage Summary

| Priority | Count | Notes |
|----------|-------|-------|
| P1 — Immediate | [N] | [N] proposed for sprint, [N] overflow |
| P2 — Next Sprint | [N] | [N] proposed for next sprint when capacity is known |
| P3 — Backlog | [N] | Deferred |
| P4 — Wishlist | [N] | User disposition pending |

**Critical (S1/S2) unfixed count**: [N]

---

## P1 Bugs — Immediate

| ID | System | Severity | Summary | Proposed placement | Story |
|----|--------|----------|---------|--------------------|-------|
| BUG-NNN | [system] | S[1-4] | [one-line description] | [sprint] | [story path] |

---

## P2 Bugs — Next Sprint

| ID | System | Severity | Summary | Target Sprint |
|----|--------|----------|---------|---------------|
| BUG-NNN | [system] | S[1-4] | [one-line description] | Sprint [N+1] |

---

## P3/P4 Bugs — Backlog / Wishlist Candidates

| ID | System | Severity | Summary | Disposition |
|----|--------|----------|---------|-------------|
| BUG-NNN | [system] | S4 | [one-line description] | Backlog |

---

## Systemic Issues Flagged

[List any patterns from Step 3 deviation check, or "None identified."]

## Data Quality Flags

[List malformed status/severity, empty reproduction, and possible duplicate
reports with file evidence. These flags never modify source bug files.]

---

## Trend Analysis

**Volume**: [N] open / [net change or `Unknown — insufficient dates`]
**Hot spot**: [system with most bugs, or `Unknown — insufficient classification`]
**Regressions**: [N, or `Unknown — missing story links/status`]
**Aged bugs (>2 sprints old)**: [N, or `Unknown — insufficient dates`]

[If N aged S1/S2 bugs > 0:]
> ⚠️ [N] high-severity bugs have been open for more than 2 sprints without
> assignment proposal. These represent unresolved risk that should be explicitly reviewed.

---

## Recommended Actions

1. [Most urgent action — usually "fix P1 bugs before QA hand-off"]
2. [Second action — usually "investigate [hot spot system] quality"]
3. [Third action — optional improvement]
```

---

## 6. Write and Gate

Present the report in conversation, then add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.

Write only after the single changeset approval, without re-prompting within its boundary.

After writing:
- If any S1 bugs have no accepted placement: "S1 bugs need an explicit sprint
  decision before the sprint can be considered healthy. Run `$sprint-status`
  to see current capacity."
- If regression bugs exist: "Regressions found — consider re-opening the
  affected stories in sprint tracking and running `$smoke-check` to re-gate."
- If no P1 bugs exist: "No P1 bugs — build is in good shape for QA hand-off." Verdict: **COMPLETE** — triage report written.

If user declined write: Verdict: **BLOCKED** — user declined write.

---

## Collaborative Protocol

- **Never close or mark bugs Won't Fix without user approval** — surface them
  as P4 candidates and ask: "Are these acceptable as Won't Fix?"
- **Never claim a report proposal changed sprint state** — flag overflow and let the
  sprint owner decide what to pull
- **Severity is objective; priority is a team decision** — present severity
  classifications as recommendations, not mandates
- **Trend data is informational** — do not block work on trend findings alone;
  surface them as observations
