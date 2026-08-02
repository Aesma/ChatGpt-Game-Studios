---
name: story-done
description: "End-of-story completion review. Reads the story file, verifies each acceptance criterion against the implementation, checks for GDD/ADR deviations, prompts code review, updates story status to Complete, and surfaces the next ready story from the sprint."
---

## Invocation and execution

Invoke this workflow as `$story-done`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[story-file-path] [--review full|lean|solo]`. Treat bracketed values as optional unless the workflow says otherwise.


# Story Done

This skill closes the loop between design and implementation. Run it at the end
of implementing any story. It ensures every acceptance criterion is verified
before the story is marked done, GDD and ADR deviations are explicitly
documented rather than silently introduced, code review is prompted rather than
forgotten, and the story file reflects actual completion status.

**Output:** Updated story file (Status: Complete) + surfaced next story.

---

## Phase 1: Find the Story

Resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `production/review-mode.txt` → use that value
3. Else → default to `lean`

See `.codex/docs/director-gates.md` for the full check pattern.

**If a file path is provided** (e.g., `$story-done production/epics/core/story-damage-calculator.md`):
read that file directly.

**If no argument is provided:**

1. Check `production/session-state/active.md` for the currently active story.
2. If not found there, read the most recent file in `production/sprints/` and
   look for stories marked IN PROGRESS.
3. If multiple in-progress stories are found, ask the user directly:
   - "Which story are we completing?"
   - Options: list the in-progress story file names.
4. If no story can be found, ask the user to provide the path.

---

## Phase 2: Read the Story

Read the full story file. Extract and hold in context:

- **Story name and ID**
- **GDD Requirement TR-ID(s)** referenced (e.g., `TR-combat-001`)
- **Manifest Version** embedded in the story header (e.g., `2026-03-10`)
- **ADR reference(s)** referenced
- **Acceptance Criteria** — the complete list (every checkbox item)
- **Implementation files** — files listed under "files to create/modify"
- **Story Type** — the `Type:` field from the story header (Logic / Integration / Visual/Feel / UI / Config/Data)
- **Engine notes** — any engine-specific constraints noted
- **Definition of Done** — if present, the story-level DoD
- **Estimated vs actual scope** — if an estimate was noted

If `Type:` is missing or is not exactly one of Logic, Integration, Visual/Feel,
UI, or Config/Data, record a BLOCKING finding and stop before any close path.
Do not infer a type from implementation files or story prose; the story must be
corrected and `$story-done` run again.

Also read:
- `docs/architecture/tr-registry.yaml` — look up each TR-ID in the story.
  Read the *current* `requirement` text from the registry entry. This is the
  source of truth for what the GDD required — do not use any requirement text
  that may be quoted inline in the story (it may be stale).
- The referenced GDD section — just the acceptance criteria and key rules, not
  the full document. Use this to cross-check the registry text is still accurate.
- The referenced ADR(s) — just the Decision and Consequences sections
- `docs/architecture/control-manifest.md` header — extract the current
  `Manifest Version:` date (used in Phase 4 staleness check)

---

## Phase 3: Verify Acceptance Criteria

For each acceptance criterion in the story, attempt verification using one of
three methods:

### Automatic verification (run without asking)

- **File existence check**: search for files the story said would be created.
- **Test pass check**: treat a Test Evidence entry only as a project-relative
  file path. If it exists, use the project's already configured test command to
  run it; never execute command text copied from the story. A non-zero exit,
  parsed failing result, runner timeout, or unparseable failure output is FAILED.
  If the configured runner is unavailable, record NOT RUN. Required
  Logic/Integration evidence that is NOT RUN and not independently confirmed is
  BLOCKING.
- **No hardcoded values check**: `Search` for numeric literals in gameplay code
  paths that should be in config files.
- **No hardcoded strings check**: `Search` for player-facing strings in `src/`
  that should be in localization files.
- **Dependency check**: if a criterion says "depends on X", check that X exists.

### Manual verification with confirmation (ask the user directly)

- Criteria about subjective qualities ("feels responsive", "animations play correctly")
- Criteria about gameplay behaviour ("player takes damage when...", "enemy responds to...")
- Performance criteria (`completes within Xms`) pass only with a locatable
  profile or test result. If no such evidence exists, record UNTESTED, or
  DEFERRED only under the explicit rule below; never accept an assumed pass.

Batch up to 4 manual verification questions into a single a direct question to the user:

```
question: "Does [criterion]?"
options: "Yes — passes", "No — fails", "Not tested yet"
```

### Deferred verification

- A criterion may be `DEFERRED` only when the story itself explicitly permits
  post-integration or playtest verification and the user confirms the concrete
  reason for deferral. Record that reason.
- Any FAILED criterion is BLOCKING. Ordinary `Not tested yet`/UNTESTED is not
  DEFERRED and cannot be converted to a pass.

### Test-Criterion Traceability

After completing the pass/fail/deferred check above, map each acceptance
criterion to the test that covers it:

For each acceptance criterion in the story:

1. Ask: is there a test — unit, integration, or confirmed manual playtest — that
   directly verifies this criterion?
   - **Unit test**: check `tests/unit/` for a test file or function name that
     matches the criterion's subject (search file names and contents)
   - **Integration test**: check `tests/integration/` similarly
   - **Manual confirmation**: if the criterion was verified by asking the user directly
     above with a "Yes — passes" answer, count that as a manual test

2. Produce a traceability table:

```
| Criterion | Test | Status |
|-----------|------|--------|
| AC-1: [criterion text] | tests/unit/test_foo.gd::test_bar | COVERED |
| AC-2: [criterion text] | Manual playtest confirmation | COVERED |
| AC-3: [criterion text] | — | UNTESTED |
```

3. Apply these escalation rules:

   - If **>50% of criteria are UNTESTED**: escalate to **BLOCKING** — test
     coverage is insufficient to confirm the story is actually done. The verdict
     in Phase 6 cannot be COMPLETE until coverage improves.
   - If any required Logic/Integration criterion is UNTESTED: **BLOCKING**.
     For other story types, some (≤50%) UNTESTED criteria remain ADVISORY but
     are not DEFERRED and must appear in Completion Notes.
   - If **all criteria are COVERED**: no action needed beyond including the
     table in the report.

4. For any ADVISORY untested criteria, add to the Completion Notes in Phase 7:
   `"Untested criteria: [AC-N list]. Recommend adding tests in a follow-up story."`

### Test Evidence Requirement

Based on the Story Type extracted in Phase 2, check for required evidence:

| Story Type | Required Evidence | Gate Level |
|---|---|---|
| **Logic** | Automated unit test in `tests/unit/[system]/` — must exist and pass | BLOCKING |
| **Integration** | Integration test in `tests/integration/[system]/` OR playtest doc | BLOCKING |
| **Visual/Feel** | Screenshot + sign-off in `production/qa/evidence/` | ADVISORY |
| **UI** | Manual walkthrough doc OR interaction test in `production/qa/evidence/` | ADVISORY |
| **Config/Data** | Relevant smoke check report with PASS or policy-accepted PASS WITH WARNINGS | BLOCKING |

**For Logic stories**: first read the story's **Test Evidence** section to extract the
exact required file path. Search for that exact path. If the exact path is not
found, also search `tests/unit/[system]/` broadly (the file may have been placed at a
slightly different location). If no test file is found at either location:
- Flag as **BLOCKING**: "Logic story has no unit test file. Story requires it at
  `[exact-path-from-Test-Evidence-section]`. Create and run the test before marking
  this story Complete."

**For Integration stories**: read the story's **Test Evidence** section for the exact
required path. Check that exact path first, then search
`tests/integration/[system]/` broadly, then check `production/session-logs/` for a
playtest record referencing this story.
If none found: flag as **BLOCKING** (same rule as Logic).

**For Visual/Feel and UI stories**: find files matching `production/qa/evidence/` for a file
referencing this story.
- If none: flag as **ADVISORY** — "No manual test evidence found. Create `production/qa/evidence/[story-slug]-evidence.md` using the test-evidence template and obtain sign-off before final closure."
- If found: read the file and check the sign-off table for unchecked boxes. Search file contents for lines matching `| .* | .* | .* | \[ \] Approved` (a sign-off row with an unchecked checkbox). If any unchecked sign-off rows are found: flag as **ADVISORY** — "Evidence file found at `[path]` but [N] sign-off(s) are still pending (shown as `[ ] Approved` in the sign-off table). Obtain required sign-offs before final closure. Note: for solo developers, all roles may be signed off by the same person."
- If all sign-off rows show `[x] Approved` or equivalent: note "Evidence file found and all sign-offs complete — ADVISORY passed."

**For Config/Data stories**: select the newest existing smoke report that
explicitly names the current sprint or story/system scope. Read its verdict.
PASS is acceptable; PASS WITH WARNINGS is acceptable only when current project
policy permits it and the warnings do not concern this story. FAIL, no related
report, or a report whose scope/date cannot be tied to the current sprint/story
is **BLOCKING**. File existence alone is never evidence.

**If no valid Story Type is set**: retain the BLOCKING finding from Phase 2 and
require the header to be corrected before rerunning.

Any BLOCKING test evidence gap prevents the COMPLETE verdict in Phase 6.

---

## Phase 4: Check for Deviations

Compare the implementation against the design documents.

Run these checks automatically:

1. **GDD rules check**: Using the current requirement text from `tr-registry.yaml`
   (looked up by the story's TR-ID), check that the implementation reflects what
   the GDD actually requires now — not what it required when the story was written.
   `Search` the implemented files for key function names, data structures, or class
   names mentioned in the current GDD section.

2. **Manifest version staleness check**: Compare the `Manifest Version:` date
   embedded in the story header against the `Manifest Version:` date in the
   current `docs/architecture/control-manifest.md` header.
   - If they match → pass silently.
   - If the story's version is older → flag as ADVISORY:
     `ADVISORY: Story was written against manifest v[story-date]; current manifest
     is v[current-date]. New rules may apply. Run $story-readiness to check.`
   - If control-manifest.md does not exist → skip this check.

3. **ADR constraints check**: Read the referenced ADR's Decision section. Check
   for forbidden patterns from `docs/architecture/control-manifest.md` (if it
   exists). `Search` for patterns explicitly forbidden in the ADR.

4. **Hardcoded values check**: `Search` the implemented files for numeric literals
   in gameplay logic that should be in data files.

5. **Scope check**: Did the implementation touch files outside the story's stated
   scope? (files not listed in "files to create/modify")

For each deviation found, categorize:

- **BLOCKING** — implementation contradicts the GDD or ADR (must fix before
  marking complete)
- **ADVISORY** — implementation drifts slightly from spec but is functionally
  equivalent (document, user decides)
- **OUT OF SCOPE** — additional files were touched beyond the story's stated
  boundary (flag for awareness — may be valid or scope creep)

---

## Phase 4b: QA Coverage Gate

**Review mode check** — apply before spawning QL-TEST-COVERAGE:
- `solo` → skip. Note: "QL-TEST-COVERAGE skipped — Solo mode." Proceed to Phase 5.
- `lean` → skip (not a PHASE-GATE). Note: "QL-TEST-COVERAGE skipped — Lean mode." Proceed to Phase 5.
- `full` → spawn as normal.

After completing the deviation checks in Phase 4, spawn `qa-lead` through Codex subagent delegation using gate **QL-TEST-COVERAGE** (`.codex/docs/director-gates.md`).

Pass:
- The story file path and story type
- Test file paths found during Phase 3 (exact paths, or "none found")
- The story's `## QA Test Cases` section (the pre-written test specs from story creation)
- The story's `## Acceptance Criteria` list

The qa-lead reviews whether the tests actually cover what was specified — not just whether files exist.

Apply the verdict:
- **ADEQUATE** → proceed to Phase 5
- **GAPS** → flag as **ADVISORY**: "QA lead identified coverage gaps: [list]. Story can complete but gaps should be addressed in a follow-up story."
- **INADEQUATE** → flag as **BLOCKING**: "QA lead: critical logic is untested. Verdict cannot be COMPLETE until coverage improves. Specific gaps: [list]."

Skip this phase for Config/Data stories (no code tests required).

---

## Phase 5: Lead Programmer Code Review Gate

**Review mode check** — apply before spawning LP-CODE-REVIEW:
- `solo` → skip. Note: "LP-CODE-REVIEW skipped — Solo mode." Proceed to Phase 6 (completion report).
- `lean` → ask the user directly before proceeding:
  - Prompt: "Code review is skipped in lean mode. Did you run `$code-review` on the implemented files?"
  - Options:
    - `Yes — $code-review passed or was approved with suggestions`
    - `No — skipping code review for this story`
    - `No — I'll run $code-review before the sprint close-out`
  - Record the answer in the completion notes (Phase 7). All three options proceed to Phase 6.
- `full` → spawn as normal.

Spawn `lead-programmer` through Codex subagent delegation using gate **LP-CODE-REVIEW** (`.codex/docs/director-gates.md`).

Pass: implementation file paths, story file path, relevant GDD section, governing ADR.

Present the verdict to the user. If CONCERNS, surface them by asking the user directly:
- Options: `Revise flagged issues` / `Accept and proceed` / `Discuss further`
If REJECT, do not proceed to Phase 6 verdict until the issues are resolved.

If the story has no implementation files, record **BLOCKING** and do not allow a
close verdict. The only exception is a Config/Data story whose declared output
files exist and whose values plus relevant smoke evidence were verified; in that
case there may be no code file for LP review.

---

## Phase 6: Present the Completion Report

Before updating any files, present the full report:

```markdown
## Story Done: [Story Name]
**Story**: [file path]
**Date**: [today]

### Acceptance Criteria: [X/Y passing]
- [x] [Criterion 1] — auto-verified (test passes)
- [x] [Criterion 2] — confirmed
- [ ] [Criterion 3] — FAILS: [reason]
- [?] [Criterion 4] — DEFERRED: requires playtest

### Test-Criterion Traceability
| Criterion | Test | Status |
|-----------|------|--------|
| AC-1: [text] | [test file::test name] | COVERED |
| AC-2: [text] | Manual confirmation | COVERED |
| AC-3: [text] | — | UNTESTED |

### Test Evidence
**Story Type**: [Logic | Integration | Visual/Feel | UI | Config/Data | Not declared]
**Required evidence**: [unit test file | integration test or playtest | screenshot + sign-off | walkthrough doc | smoke check pass]
**Evidence found**: [YES — `[path]` | NO — BLOCKING | NO — ADVISORY]

### Deviations
[NONE] OR:
- BLOCKING: [description] — [GDD/ADR reference]
- ADVISORY: [description] — user accepted / flagged for tech debt

### Scope
[All changes within stated scope] OR:
- Extra files touched: [list] — [note whether valid or scope creep]

### Verdict: COMPLETE / COMPLETE WITH NOTES / BLOCKED
```

**Verdict definitions:**
- **COMPLETE**: all criteria PASS, required implementation/output files and test
  evidence are verified, and there are no blocking deviations
- **COMPLETE WITH NOTES**: no FAILED or ordinary required UNTESTED criteria; any
  DEFERRED item was explicitly allowed by the story for post-integration/playtest
  verification, has a user-confirmed reason, and all other blockers are absent;
  advisory deviations are documented
- **BLOCKED**: any FAILED criterion; missing/invalid Story Type; missing required
  implementation/output file; missing, failed, NOT RUN, unrelated, or stale
  required evidence; blocking design/code-review finding; or an UNTESTED required
  Logic/Integration criterion

If the verdict is **BLOCKED**: do not proceed to Phase 7. List what must be
fixed. Offer to help fix the blocking items.

---

## Phase 7: Update Story Status

Ask the user directly before writing anything:
- Prompt: "Verification complete. How do you want to proceed?"
- Options:
  - `Close the story — update file, mark Complete, log notes (Recommended)`
  - `Close and log advisory deviations as tech debt in docs/tech-debt-register.md`
  - `There are issues I want to fix first — don't close yet`

Only COMPLETE or COMPLETE WITH NOTES reaches this phase. If "Close" or "Close
and log tech debt" is selected, prepare the edits below. BLOCKED has no override
or close option; list the blockers, stop without writing, and rerun `$story-done`
after they are fixed.
If "Close and log tech debt": also prepare the advisory-deviation append to
`docs/tech-debt-register.md` (creating it only if selected and absent).
If "Fix first": stop here and list what the user flagged. Do not write any files.

Before any write, present one complete changeset listing the exact story path,
`production/sprint-status.yaml` when it exists, `production/session-state/active.md`
(create or append), and the tech-debt register only when selected. Summarize each
edit precisely and obtain the single authorization required at the top. After
approval, apply all listed edits continuously; if not approved, write none.

1. Update the status field: `Status: Complete`
2. Update the `Last Updated:` field in the story header to today's date (format: `YYYY-MM-DD`). If the field does not exist, add it after the `Status:` line.
3. Add a `## Completion Notes` section at the bottom:

```markdown
## Completion Notes
**Completed**: [date]
**Criteria**: [X/Y passing] ([any deferred items listed])
**Deviations**: [None] or [list of advisory deviations]
**Test Evidence**: [Logic: test file at path | Visual/Feel: evidence doc at path | None required (Config/Data)]
**Code Review**: [Pending / Complete / Skipped]
```

4. If the user chose "Close and log tech debt": append each advisory deviation to `docs/tech-debt-register.md` in this format:
   ```
   - **[date]** ([story title]): [deviation description] — tracked from [story file path]
   ```
   Create the file with a `# Tech Debt Register` heading if it does not exist.

5. **Update `production/sprint-status.yaml`** (if it exists):
   - Find the entry matching this story's file path or ID
   - Set `status: done` and `completed: [today's date]`
   - Update the top-level `updated` field
   - This is a silent update — no extra approval needed (already approved in step above)

6. **Suggest a git commit**: Output a ready-to-use commit command covering the implementation files from the dev-story summary and the updated story file:

```
Suggested commit:
git add [src/ and tests/ files changed during implementation] [story-file-path]
git commit -m "feat: [story title] ([TR-ID])"
```

Before suggesting the commit, explicitly verify design-document references and scan the changed files for hardcoded design values; do not assume a local commit hook exists.

### Session State Update

After updating the story file, silently append to
`production/session-state/active.md`:

    ## Session Extract — $story-done [date]
    - Verdict: [COMPLETE / COMPLETE WITH NOTES / BLOCKED]
    - Story: [story file path] — [story title]
    - Tech debt logged: [N items, or "None"]
    - Next recommended: [next ready story title and path, or "None identified"]

If `active.md` does not exist, create it with this block as the initial content.
Confirm in conversation: "Session state updated."

---

## Phase 8: Surface the Next Story

After completion, help the developer keep momentum:

1. Read the current sprint plan from `production/sprints/`.
2. Find stories that are:
   - Status: READY or NOT STARTED
   - Not blocked by other incomplete stories
   - In the Must Have or Should Have tier

Present:

```
### Next Up
The following stories are ready to pick up:
1. [Story name] — [1-line description] — Est: [X hrs]
2. [Story name] — [1-line description] — Est: [X hrs]

Run `$story-readiness [path]` to confirm a story is implementation-ready
before starting.
```

If no more Must Have stories remain in this sprint (all are Complete or Blocked):

```
### Sprint Close-Out Sequence

All Must Have stories are complete. QA sign-off is required before advancing.
Run these in order:

1. `$smoke-check sprint` — verify the critical path still works end-to-end
2. `$team-qa sprint` — full QA cycle: test case execution, bug triage, sign-off report
3. `$retrospective` — capture what went well, what didn't, and action items for the next sprint
4. `$gate-check` — advance to the next phase once QA approves (only if advancing a phase)
5. `$sprint-plan new` — plan the next sprint, incorporating velocity data and retrospective action items

Do not run `$gate-check` until `$team-qa` returns APPROVED or APPROVED WITH CONDITIONS.
```

If there are Should Have stories still unstarted, surface them alongside the close-out sequence so the user can choose: close the sprint now, or pull in more work first.

If no more stories are ready but Must Have stories are still In Progress (not Complete):
"No more stories ready to start — [N] Must Have stories still in progress. Continue implementing those before sprint close-out."

---

## Collaborative Protocol

- **Never mark a story complete without user approval** — Phase 7 requires an
  explicit "yes" before any file is edited.
- **Never auto-fix failing criteria** — report them and ask what to do.
- **Deviations are facts, not judgments** — present them neutrally; the user
  decides if they are acceptable.
- **BLOCKED verdict cannot be overridden** — list required fixes and stop. Only
  COMPLETE or COMPLETE WITH NOTES can update story status.
- Ask the user directly for the code review prompt and for batching manual
  criteria confirmations.

---

## Recommended Next Steps

- Run `$story-readiness [next-story-path]` to validate the next story before starting implementation
- If all Must Have stories are complete: run `$smoke-check sprint` → `$team-qa sprint` → `$gate-check`
- If tech debt was logged: track it via `$tech-debt` to keep the register current
