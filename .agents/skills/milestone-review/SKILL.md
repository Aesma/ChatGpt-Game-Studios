---
name: milestone-review
description: "Generates a comprehensive milestone progress review including feature completeness, quality metrics, risk assessment, and go/no-go recommendation. Use at milestone checkpoints or when evaluating readiness for a milestone deadline."
---

## Invocation and execution

Invoke this workflow as `$milestone-review`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[milestone-name|current] [--review full|lean|solo]`. Treat bracketed values as optional unless the workflow says otherwise.


## Phase 0: Parse Arguments

Require exactly one milestone target: `current` or one specific milestone name. Reject unknown flags, multiple targets, or missing targets before reading review mode. Resolve the target to exactly one file under `production/milestones/`; when a named file is absent or ambiguous, list available milestone files, output **BLOCKED**, and do not run a gate or prepare a write.

Resolve the review mode once and store it for all gate spawns this run:
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `production/review-mode.txt` → use that value
3. Else → default to `lean`

See `.codex/docs/director-gates.md` for the full check pattern.

---

## Phase 1: Load Milestone Data

Read the milestone definition from `production/milestones/`. For `current`, first follow an explicit milestone reference in the existing session, stage, or active sprint artifacts. If there is no unique reference, list the candidate milestone files and ask the user to choose; never select by modification time.

Read only sprint reports explicitly referenced by that milestone or whose header explicitly names it. Follow the milestone's explicit feature/story links, and load the attributable story status, bug/status records, test and coverage results, performance reports, and technical-debt evidence. Include only items linked by milestone ID or an explicit reference. Missing evidence is `unknown`; do not estimate percentages or counts.

---

## Phase 2: Scan Codebase Health

- Scan for `TODO`, `FIXME`, `HACK` markers only in production source and build configuration. Exclude documentation, templates, generated/vendor content, and test fixtures; report the scanned paths/scope with every count
- Check the risk register at `production/risk-register/` and the milestone-linked bug, test, performance, and technical-debt evidence loaded above
- For every metric in the report, retain its source path; where no valid numerator/denominator or measurement exists, write `unknown` rather than inventing a value

---

## Phase 3: Generate the Milestone Review

Compile the complete evidence draft first, but leave the final Go/No-Go Recommendation, Conditions, and Rationale unresolved until Phase 3b.

```markdown
# Milestone Review: [Milestone Name]

## Overview
- **Target Date**: [Date]
- **Current Date**: [Today]
- **Days Remaining**: [N]
- **Sprints Completed**: [X/Y]

## Feature Completeness

### Fully Complete
| Feature | Acceptance Criteria | Test Status |
|---------|-------------------|-------------|

### Partially Complete
| Feature | % Done | Remaining Work | Risk to Milestone |
|---------|--------|---------------|------------------|

### Not Started
| Feature | Priority | Can Cut? | Impact of Cutting |
|---------|----------|----------|------------------|

## Quality Metrics
- **Open S1 Bugs**: [N] -- [List]
- **Open S2 Bugs**: [N]
- **Open S3 Bugs**: [N]
- **Test Coverage**: [X%]
- **Performance**: [Within budget? Details]

## Code Health
- **TODO count**: [N across codebase]
- **FIXME count**: [N]
- **HACK count**: [N]
- **Technical debt items**: [List critical ones]

## Risk Assessment
| Risk | Status | Impact if Realized | Mitigation Status |
|------|--------|-------------------|------------------|

## Velocity Analysis
- **Planned vs Completed** (across all sprints): [X/Y tasks = Z%]
- **Trend**: [Improving / Stable / Declining]
- **Adjusted estimate for remaining work**: [Days needed at current velocity]

## Scope Recommendations
### Protect (Must ship with milestone)
- [Feature and why]

### At Risk (May need to cut or simplify)
- [Feature and risk]

### Cut Candidates (Can defer without compromising milestone)
- [Feature and impact of cutting]

## Go/No-Go Assessment

**Recommendation**: [GO / CONDITIONAL GO / NO-GO]

**Conditions** (if conditional):
- [Condition 1 that must be met]
- [Condition 2 that must be met]

**Rationale**: [Explanation of the recommendation]

## Action Items
| # | Action | Owner | Deadline |
|---|--------|-------|----------|
```

---

## Phase 3b: Producer Risk Assessment

**Review mode check** — apply before spawning PR-MILESTONE:
- `solo` → skip. Note: "PR-MILESTONE skipped — Solo mode." Present the Go/No-Go section without a producer verdict.
- `lean` → skip (not a PHASE-GATE). Note: "PR-MILESTONE skipped — Lean mode." Present the Go/No-Go section without a producer verdict.
- `full` → spawn as normal.

Before generating the Go/No-Go recommendation, spawn `producer` through Codex subagent delegation using gate **PR-MILESTONE** (`.codex/docs/director-gates.md`). In full mode, if the gate or agent is unavailable, times out, or returns no complete verdict, report the missing assessment and stop before final recommendation or write; never simulate a producer verdict.

Pass: milestone name and target date, current completion percentage, blocked story count, velocity data from sprint reports (if available), list of cut candidates.

Present the producer's assessment inline within the Go/No-Go section. The producer's verdict (ON TRACK / AT RISK / OFF TRACK) informs the overall recommendation. After handling that verdict and the user's risk decision, generate the final Go/No-Go Recommendation, Conditions, and Rationale, then present the complete draft. Do not show or persist a final recommendation before this ordering is complete.

If OFF TRACK, ask the user directly before generating the recommendation:
- Prompt: "Producer verdict: OFF TRACK. The milestone is in jeopardy. This review will recommend NO-GO. How do you want to proceed?"
- Options:
  - `[A] Accept NO-GO — generate the full review with that recommendation`
  - `[B] Override to CONDITIONAL GO — I'll document the accepted risks myself`
  - `[C] Stop — I want to address blockers before generating the review`

If AT RISK, ask the user directly:
- Prompt: "Producer verdict: AT RISK. Milestone may slip. How should the Go/No-Go section be framed?"
- Options:
  - `[A] CONDITIONAL GO — include producer's conditions in the review`
  - `[B] NO-GO — conditions cannot be met in time`
  - `[C] GO — I accept the risk and want to proceed`

An OFF TRACK result may produce only **NO-GO**, or **CONDITIONAL GO** when the user explicitly selects [B] and supplies accepted risks/conditions. It can never produce an unconditional GO.

For AT RISK option [C], retain the producer verdict and record the user's specific accepted risks in the existing `Conditions` and `Rationale` sections; do not hide the assessment. Lean/solo reports explicitly state that no producer verdict was obtained.

---

## Phase 4: Save Review

Use `production/milestones/review-[milestone].md`, where `[milestone]` is the uniquely resolved target name. If the file already exists, present it as an update in the changeset preview; never silently overwrite it.

Present the review to the user.

Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.

Determine the delivery verdict from the evidence, independently of saving: output **MILESTONE COMPLETE** only when milestone delivery criteria are complete; otherwise output **MILESTONE INCOMPLETE** and list the unmet criteria. Once the complete changeset is authorized, write the report with that same delivery verdict.

If the changeset is not authorized, state `report not saved` but do not change the already-determined milestone verdict. Input-resolution failures may still end the workflow as **BLOCKED**.

---

## Phase 5: Next Steps

- Run `$gate-check` for a formal phase gate verdict if this milestone marks a development phase boundary.
- Run `$sprint-plan` to adjust the next sprint based on the scope recommendations above.
