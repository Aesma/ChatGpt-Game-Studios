# Skill Test Spec: $test-flakiness

## Skill Summary

`$test-flakiness` detects non-deterministic tests by analyzing test history logs
(if available) or scanning test source code for common flakiness patterns (random
numbers without seeds, real-time waits, external I/O). No director gates are
invoked. The skill does not write outside the authorized changeset. Verdicts: NO FLAKINESS,
SUSPECT TESTS FOUND, or CONFIRMED FLAKY.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: NO FLAKINESS, SUSPECT TESTS FOUND, CONFIRMED FLAKY
- [ ] Remains read-only; no authorization prompt appears because the workflow does not modify files

**Assertions:**
- [ ] No director gate is invoked in any review mode
- [ ] CONFIRMED FLAKY verdict requires history-based evidence (not just source patterns)
- [ ] CONFIRMED FLAKY requires multiple runs whose logs identify the same build/version; unknown code equivalence remains SUSPECT
- [ ] A single-run log is insufficient evidence, has no flakiness rate, and cannot update quarantine
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Flakiness report is advisory for qa-lead; skill does not auto-disable tests
- [ ] High flakiness prioritizes a fix and blocks trust in the suite; it never instructs automatic skip-to-green
- [ ] Quarantined Tests is updated only for a test already isolated by a separate user-authorized action

---

## Protocol Compliance

## P1 Regression Matrix

- [ ] `.github/` workflow YAML identifies framework only and is never counted as result history.
- [ ] JUnit parsing uses testcase hierarchy and classname+name; suite failure and skipped/not-run are not false testcase outcomes.
- [ ] Run boundaries are result files/explicit sections; missing tests are not observed and the denominator is actual N/M observations.
- [ ] Fewer than three comparable observed runs is SUSPECT before percentage tiers are considered.
- [ ] Cause classification is a likely hypothesis with source evidence or UNKNOWN, never a confirmed root cause from keywords.
- [ ] Missing registry/Quarantined section keeps output in conversation and creates no structure.
- [ ] Existing Test File+Function rows are not appended twice.
- [ ] The optional report is offered only after analysis and written only on explicit opt-in.

- [ ] Reads test history logs when available; falls back to source analysis when not
- [ ] Notes clearly which analysis mode is being used (history vs. source-only)
- [ ] Flakiness threshold (e.g., 95% pass rate) is used for SUSPECT classification
- [ ] CONFIRMED FLAKY requires history evidence; SUSPECT covers source patterns only
- [ ] Mixed outcomes with `code equivalence unknown` are SUSPECT, not CONFIRMED
- [ ] Does not disable or modify any test files
- [ ] No director gates are invoked
- [ ] Verdict is one of: NO FLAKINESS, SUSPECT TESTS FOUND, CONFIRMED FLAKY

---

## Coverage Notes

- The pass-rate threshold for SUSPECT classification (95% suggested above) is an
  implementation detail; the tests verify that intermittent failures are flagged,
  not the exact threshold value.
- Tests that fail due to environment issues (missing assets, wrong platform) are
  not flakiness — the skill distinguishes environment failures from non-determinism
  in the test itself; this distinction is not explicitly tested here.
