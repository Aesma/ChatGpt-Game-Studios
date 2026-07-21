# Skill Test Spec: $retrospective

## Skill Summary

`$retrospective` generates a structured sprint or milestone retrospective covering what went well, what did not, and proposed action items. Every metric is `OBSERVED`, `DERIVED`, or `UNKNOWN`, with source evidence and confidence. Unsupported actual effort, bug counts, deltas, trends, and causes remain `UNKNOWN`.

The skill creates only the retrospective artifact. It invokes no director gate, sprint planning workflow, other skill, or follow-on task. A successfully saved retrospective receives `COMPLETE`; this is an artifact-completion verdict, not a pass/fail assessment of the sprint or milestone.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has at least two phase headings
- [ ] Contains verdict keyword: COMPLETE
- [ ] Defines the metric states `OBSERVED`, `DERIVED`, and `UNKNOWN`
- [ ] Requires evidence IDs and confidence for reported metrics
- [ ] Says that unsupported causes remain `UNKNOWN`
- [ ] Explicitly prohibits invoking `$sprint-plan`, `$gate-check`, or any other skill after save
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts

---

## Behavioral Cases

### Case 1: Happy path — supported completion metrics

**Fixture:**

- `production/sprints/sprint-005.md` records 4 planned stories and their estimates
- `production/sprint-status.yaml` maps the same 4 stories to the same sprint and records 3 as done and 1 as deferred
- an in-scope bug record states that 2 bugs were found and 1 was fixed
- the sprint dates define an objective Git range containing 6 commits

**Input:** `$retrospective sprint-005`

**Expected behavior:**

1. The skill creates evidence-ledger entries with locators and supported scope.
2. Planned and completed task counts are `OBSERVED`.
3. Completion rate is `DERIVED` as `3 / 4 * 100 = 75%` and cites its input evidence.
4. Bug and commit counts cite their in-scope sources.
5. The draft contains what went well, what did not, and action items.
6. After authorization, the file is written and the skill stops with `COMPLETE`.

**Assertions:**

- [ ] Every metric row has a state, evidence or missing-evidence reason, and confidence
- [ ] Every derived metric includes a formula and all input evidence IDs
- [ ] Blocked and deferred stories appear in the "what didn't" section when supported by status evidence
- [ ] At least one proposed action item is tied to evidence from the deferred story
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write
- [ ] No planning or gate workflow is invoked after the file is saved

---

### Case 2: Missing actual effort and bug evidence

**Fixture:**

- `production/sprints/sprint-005.md` contains planned tasks and estimates
- completion status exists, but no time record, actual-effort field, bug event record, or explicit user statement exists
- commit messages mention "fix" several times

**Input:** `$retrospective sprint-005`

**Expected behavior:**

1. The skill records the supported plan and completion evidence.
2. Actual effort, effort delta, estimation variance, overall estimation accuracy, bugs found, and bugs fixed are `UNKNOWN` with confidence `NONE`.
3. Commit-message wording is not used as bug-count evidence.
4. No likely cause is inferred. Cause cells say `UNKNOWN — no event record or user confirmation` unless the user confirms one.
5. The report lists the missing evidence in `Data Gaps` and can still be saved as a retrospective artifact.

**Assertions:**

- [ ] Missing metrics are literally `UNKNOWN`, never zero, none, or a plausible estimate
- [ ] A derived result becomes `UNKNOWN` when any required input is unknown
- [ ] No actual effort is estimated from commits, elapsed dates, or task complexity
- [ ] Bug-like commit messages do not become bug counts
- [ ] No cause, resolution, prevention claim, or trend explanation is invented
- [ ] Successful save returns `COMPLETE` and does not launch another workflow

---

### Case 3: Existing retrospective requires an explicit choice

**Fixture:**

- a retrospective matching sprint-005 already exists
- new supported status evidence is available

**Input:** `$retrospective sprint-005`

**Expected behavior:**

1. The skill detects the existing retrospective before compiling.
2. It offers the documented update-existing or start-fresh choice.
3. It does not silently overwrite the file.
4. It shows the complete proposed changeset once before the first write unless the current task already provides bounded authorization.
5. After the authorized write, the verdict is `COMPLETE` and execution stops.

**Assertions:**

- [ ] Existing retrospective detection occurs before compilation
- [ ] The user is offered the documented update-existing or start-fresh choice
- [ ] No silent overwrite occurs
- [ ] There is no per-file or per-section authorization loop
- [ ] No next-step skill or gate is invoked

---

### Case 4: Unresolved action items from previous retrospective

**Fixture:**

- `production/retrospectives/retro-sprint-004.md` exists with 2 action items marked `[ ]`
- the artifact is the prior retrospective selected for comparison
- no independent status evidence exists for those actions

**Input:** `$retrospective sprint-005`

**Expected behavior:**

1. The skill reads the prior retrospective.
2. It carries the 2 unchecked items into the follow-up section.
3. The item status remains `UNKNOWN` unless current evidence proves its state; an unchecked box alone is not proof that work was not done.
4. Carry-over items remain distinct from newly proposed action items.

**Assertions:**

- [ ] Prior action items are checked against current evidence
- [ ] Unresolved or unknown-status items appear in the follow-up section
- [ ] Missing follow-up evidence is reported, not converted into `Not Started`
- [ ] Carry-over items are distinct from new action items

---

### Case 5: Ambiguous Git period cannot supply commit count

**Fixture:**

- the target sprint has no reliable start or end dates
- `git log --oneline --since="4 weeks ago"` or `git log --oneline -20` returns commits

**Input:** `$retrospective sprint-005`

**Expected behavior:**

1. The Git output may be used as context.
2. Because it cannot be tied objectively to the target period, `Commits` is `UNKNOWN` with confidence `NONE`.
3. No task, completion, effort, bug, or cause claim is inferred from those commits.

**Assertions:**

- [ ] Fallback Git history is not presented as a sprint metric
- [ ] The missing period boundary is recorded as the reason
- [ ] No unsupported downstream metric is calculated

---

### Case 6: Save is a terminal boundary in sprint mode

**Fixture:**

- sprint-005 has enough evidence to produce a report
- the user authorizes the proposed file write
- the user has not issued a separate planning command in a new task

**Input:** `$retrospective sprint-005`

**Expected behavior:**

1. The skill writes the retrospective.
2. It returns the saved artifact path used by the current implementation and `Verdict: COMPLETE`.
3. It may show `$sprint-plan` as plain-text guidance for a new task.
4. It stops without invoking, preloading, or opening sprint planning.

**Assertions:**

- [ ] Zero follow-on skill invocations occur
- [ ] No retrospective data is passed automatically to `$sprint-plan`
- [ ] No task or workflow is opened automatically
- [ ] The saved artifact path is returned before stop

---

### Case 7: Save is a terminal boundary in milestone mode

**Fixture:**

- a milestone retrospective has been produced and authorized
- `production/session-state/review-mode.txt` contains `full`

**Input:** `$retrospective milestone-alpha`

**Expected behavior:**

1. The skill writes the milestone retrospective and returns `COMPLETE`.
2. Review mode does not alter retrospective behavior.
3. No `$gate-check`, director gate, readiness evaluation, sprint planning, other skill, or new task is invoked.
4. Execution stops after returning the artifact path.

**Assertions:**

- [ ] No director gate is invoked in any review mode
- [ ] No gate result notation is emitted
- [ ] No planning workflow is invoked
- [ ] Milestone outcomes remain evidence-backed; unsupported readiness conclusions are not generated

---

## Protocol Compliance

- [ ] Always shows the retrospective draft before asking to write, unless an existing bounded authorization already covers the write
- [ ] Uses one complete changeset preview and one approval at most; no per-file or per-section re-prompts
- [ ] Every reported metric has a source or explicit `UNKNOWN`, plus confidence
- [ ] Causes require an event record or explicit user confirmation
- [ ] No director gates are invoked
- [ ] Saving the retrospective is terminal; follow-on commands are guidance only
- [ ] A successful save receives `COMPLETE` as an artifact-completion verdict
- [ ] Checks the prior retrospective for unresolved action items without treating absence of follow-up evidence as proof of status

---

## Coverage Notes

- The P0 contract applies equally to sprint and milestone retrospectives.
- This spec does not assert the future immutable-history, argument-resolution, action-ownership, revision-check, or partial-verdict redesigns; those remain outside RT-001 and RT-002.
- Missing evidence is an expected data-quality outcome. It must reduce claims, not encourage generated precision.
