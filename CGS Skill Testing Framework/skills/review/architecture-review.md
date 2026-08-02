# Skill Test Spec: $architecture-review

## Skill Summary

`$architecture-review` reviews architecture coverage, consistency, and engine
compatibility across GDDs and ADRs. Its modes are `full`, `coverage`,
`consistency`, `engine`, `single-gdd`, and `rtm`. It produces the
workflow's canonical verdicts: PASS, CONCERNS, or FAIL.

The workflow may write only a user-authorized, mode-eligible changeset. Depending
on mode and user selection, that changeset can contain a review report,
traceability index, TR registry, RTM, systems-index edits, a
consistency-failures append, and session state. Report-only means exactly one
file and no hidden side effects.

---

## Static Assertions

- [ ] YAML frontmatter contains the required name and non-empty description
- [ ] Verdicts are exactly PASS / CONCERNS / FAIL
- [ ] All six invocation modes are declared
- [ ] A mode-to-phase/output matrix prevents fall-through
- [ ] One complete changeset is previewed before the first write
- [ ] No test is described as passing unless it was actually executed

---

## Case 1: Full mode writes an explicitly previewed changeset

**Input:** `$architecture-review full`

**Expected behavior:**

1. Runs Phases 1–6 in scope.
2. Builds the report with PASS / CONCERNS / FAIL.
3. Shows every selected report/index/registry/ancillary target and exact edit
   before the first write.
4. One authorization applies only that displayed changeset.

**Assertions:**

- [ ] Systems-index edits are not applied during Phase 5b
- [ ] Consistency-failures and session-state edits appear in the same preview
- [ ] Adding a file after preview requires a revised complete approval
- [ ] Declining leaves every candidate file unchanged

---

## Case 2: Report-only has no ancillary writes

**Input:** `$architecture-review full`, then choose report-only.

**Assertions:**

- [ ] Only `docs/architecture/architecture-review-[date].md` is written
- [ ] Traceability index, TR registry, systems index, consistency failures, RTM,
      and `production/session-state/active.md` remain unchanged
- [ ] Verdict vocabulary remains PASS / CONCERNS / FAIL

---

## Case 3: Test-file existence is not test success

**Fixture:** A story names an existing automated-test file, but the test is not
executed during the review.

**Input:** `$architecture-review rtm`

**Assertions:**

- [ ] Status is `FILE EXISTS (not executed)`, not COVERED or passing
- [ ] Missing paths are `FILE MISSING`
- [ ] Linkage percentage is not called passing-test or full-chain coverage
- [ ] No test result is inferred from a file search

---

## Case 4: Modes execute only their declared branches

**Assertions:**

- [ ] `coverage` runs GDD/ADR traceability but not consistency or engine phases
- [ ] `consistency` reads ADR conflict inputs and cannot update the TR registry
- [ ] `engine` reads ADR/engine-reference inputs and does not extract GDD requirements
- [ ] `single-gdd` reports and updates only the named GDD's scoped rows
- [ ] `rtm` reads stories/tests and is the only dedicated RTM-output mode
- [ ] Counts and report sections never imply out-of-scope documents were reviewed

---

## Protocol Compliance

- [ ] Canonical output and tests agree on side effects and verdicts
- [ ] Complete changeset approval occurs before every selected write
- [ ] Report-only has no session-state or logging side effect
- [ ] File existence is reported as evidence only, never as a passing test
- [ ] The workflow does not create an additional mode, phase, schema, or verdict

## P1 Regression Assertions

- [ ] Missing/invalid `single-gdd` paths and unknown modes stop without a verdict
- [ ] Single-GDD ADR selection scans Summary and `GDD Requirements Addressed`, not titles alone
- [ ] Implicit decision-text matches are Partial, never Covered
- [ ] TR reuse requires same-system semantic evidence and the registry is re-read before assigning new lowercase-slug IDs
- [ ] Only `rtm` reads stories/tests or writes the RTM; `full` does not expand based on repository state
- [ ] Engine reads are limited to domains named by in-scope ADRs
- [ ] A partial full review cannot PASS, and failed specialist scope is visible
- [ ] Handoff reports actual architecture evidence and does not invent unrelated test/UX gate prerequisites
