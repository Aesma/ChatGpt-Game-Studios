# Skill Test Spec: `$vertical-slice`

> **Category**: pipeline
> **Priority**: high
> **Spec written**: 2026-07-18

## Skill Summary

`$vertical-slice` validates whether a representative, production-quality core
loop is fun, technically feasible, and buildable at a sustainable velocity before
the project advances from Pre-Production to Production. It scopes an isolated
prototype, records playtest and velocity evidence, emits PROCEED, PIVOT, or KILL,
and routes the result through the configured review mode.

---

## Static Assertions

- [ ] YAML frontmatter contains `name: vertical-slice` and a non-empty `description`
- [ ] The documented invocation is `$vertical-slice`
- [ ] At least five distinct workflow phases are present
- [ ] Uses `.codex/docs/`, `.agents/skills/`, and `AGENTS.md` paths only
- [ ] Contains PROCEED, PIVOT, and KILL verdicts
- [ ] Requires an isolated worktree, or user confirmation before modifying the current workspace
- [ ] Ends with explicit next actions for every verdict

---

## Director Gate Checks

- **Full mode**: delegate CD-PLAYTEST review to the `creative-director` Codex subagent
- **Lean mode**: skip CD-PLAYTEST and record that it was skipped
- **Solo mode**: skip all director review and record that it was skipped
- A CONCERNS, PIVOT, or KILL outcome must never auto-advance the stage

---

## Test Cases

### Case 1: Happy Path — representative slice reaches PROCEED

**Fixture:**
- `production/review-mode.txt` contains `full`
- Concept, systems index, accepted ADRs, control manifest, and relevant GDDs exist
- An isolated Git worktree is available
- The user confirms a three-to-five-minute core-loop scope
- A completed playtest demonstrates the full start → challenge → resolution loop

**Expected behavior:**
1. Read all design and architecture inputs and state one falsifiable validation question.
2. Confirm scope, timebox, representative quality, and success criteria before implementation.
3. Keep implementation under `prototypes/[concept]-vertical-slice/` and label it non-production.
4. Record real daily velocity and structured playtest observations.
5. Include `REPORT.md` and `prototypes/index.md` in one bounded changeset, using existing task authorization or one confirmation before writing.
6. Delegate CD-PLAYTEST to `creative-director` and report the final PROCEED verdict.

**Assertions:**
- [ ] Slice scope contains the complete core loop and is limited to three-to-five minutes
- [ ] Production code does not import from the slice
- [ ] Velocity values are actual observations, not estimates
- [ ] At least one completed playtest is documented
- [ ] The creative-director review occurs in full mode
- [ ] Recommended handoff includes `$gate-check pre-production`

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 2: Blocked — required Pre-Production inputs are missing

**Fixture:**
- `design/gdd/game-concept.md` exists
- `design/gdd/systems-index.md`, the control manifest, and accepted ADRs are absent

**Expected behavior:**
1. Report each missing prerequisite rather than inventing its content.
2. Explain that feasibility cannot be evaluated against an undefined architecture or scope.
3. Stop before creating a worktree or prototype files.
4. Recommend the applicable design and architecture skills.

**Assertions:**
- [ ] Missing files are named precisely
- [ ] No prototype or session checkpoint is created
- [ ] No PROCEED verdict is emitted
- [ ] Next actions include `$map-systems`, `$create-architecture`, or `$architecture-decision` as applicable

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 3: Pivot Re-run — previous evidence informs the new question

**Fixture:**
- A previous slice contains `PIVOT-NOTE.md` and `REPORT.md`
- Revised GDDs and ADRs address the previous failure
- Review mode is `lean`

**Expected behavior:**
1. Read the prior pivot evidence before proposing scope.
2. Preserve successful systems and target the documented failure with a new validation question.
3. Record the run as a re-validation, not a first attempt.
4. Skip CD-PLAYTEST in lean mode and state why.

**Assertions:**
- [ ] The new validation question directly addresses the prior failure
- [ ] Known successful mechanics are not needlessly re-scoped
- [ ] The report identifies this as a PIVOT re-run
- [ ] Lean-mode gate behavior is explicit

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 4: Edge Case — day-three sunk-cost checkpoint fails

**Fixture:**
- Planned duration is ten days
- At the end of day three, the complete loop is not demonstrable
- The blocker is an invalid architecture assumption

**Expected behavior:**
1. Stop further implementation at the checkpoint.
2. Surface the architectural blocker and its impact on the validation question.
3. Recommend cutting scope or revisiting the ADR; do not hide the delay by reducing quality.

**Assertions:**
- [ ] Work does not continue automatically after the checkpoint
- [ ] The blocker is captured in session state and the eventual report
- [ ] Scope reduction is considered before quality reduction
- [ ] The skill does not issue PROCEED

**Case Verdict**: PASS / FAIL / PARTIAL

---

### Case 5: Mode and Verdict Matrix — PIVOT/KILL cannot advance

**Fixture:**
- Run the same inconclusive evidence under full, lean, and solo review modes
- The playtest evidence supports PIVOT

**Expected behavior:**
1. Full mode delegates CD-PLAYTEST; lean and solo modes do not.
2. All modes preserve the evidence-driven PIVOT unless an allowed full-mode review changes it with rationale.
3. No mode updates the project stage to Production.
4. The skill offers `PIVOT-NOTE.md` and revision/re-test next steps.

**Assertions:**
- [ ] Review-mode differences affect review, not underlying evidence
- [ ] No PIVOT or KILL path auto-advances the stage
- [ ] PIVOT produces carry-forward guidance
- [ ] KILL, when selected, records reusable lessons in `prototypes/GRAVEYARD.md`

**Case Verdict**: PASS / FAIL / PARTIAL

---

## Protocol Compliance

- [ ] Confirms scope before implementation
- [ ] Uses an isolated worktree or obtains approval to use the current workspace
- [ ] Treats reports and append-only decision records as one bounded changeset and does not re-prompt per file
- [ ] Uses Codex subagent delegation for independent specialist work
- [ ] Uses `$skill` syntax and Codex paths throughout
- [ ] Returns a concrete verdict, evidence summary, and next step

---

## Coverage Notes

This spec tests the workflow contract, not game-specific playability. Engine build
commands and real multiplayer latency require live project execution. The catalog
and coverage audit must discover this file recursively; no hard-coded skill total
may substitute for comparing actual skill directories, catalog entries, and specs.
