# Skill Test Spec: $regression-suite

## Skill Summary

`$regression-suite` maps test coverage to GDD requirements: it reads the
acceptance criteria from story files in the current sprint (or a specified epic),
then scans `tests/` for corresponding test files and checks whether each AC has
a matching assertion. It produces a coverage report identifying which ACs are
fully covered, partially covered, or untested, and which test files have no
matching AC (orphan tests).

The skill may write a coverage report to `production/qa/` after a "May I apply the proposed changeset?"
6. File is written on approval; verdict is FULL COVERAGE

**Assertions:**
- [ ] All 6 ACs appear in the coverage report
- [ ] Each AC is marked as covered with the matching test file referenced
- [ ] Verdict is FULL COVERAGE
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
5. Report is written; verdict is GAPS FOUND

**Assertions:**
- [ ] The 3 untested ACs are listed by name in the report
- [ ] Matched ACs are also shown (not only the gaps)
- [ ] Verdict is GAPS FOUND (not FULL COVERAGE)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts

---

### Case 3: Critical AC Untested — CRITICAL GAPS verdict, flagged prominently

**Fixture:**
- Sprint has 4 stories; one story is Priority: Critical with 2 ACs
- One of the critical-priority ACs has no test

**Input:** `$regression-suite`

**Expected behavior:**
1. Skill reads all stories and ACs, noting which stories are critical priority
2. Skill scans tests — the critical AC has no match
3. Report prominently flags: "CRITICAL GAP: [AC text] — no test found (Critical priority story)"
4. Skill recommends blocking story completion until test is added
5. Verdict is CRITICAL GAPS

**Assertions:**
- [ ] Verdict is CRITICAL GAPS (not GAPS FOUND)
- [ ] Critical priority AC is flagged more prominently than normal gaps
- [ ] Recommendation to block story completion is included
- [ ] Non-critical gaps (if any) are also listed

---

### Case 4: Orphan Tests — Test file has no matching AC

**Fixture:**
- `tests/unit/save_system_test.gd` exists with assertions for scenarios
  not present in any current story's AC list
- Current sprint stories do not reference save system

**Input:** `$regression-suite`

**Expected behavior:**
1. Skill scans tests and cross-references ACs
2. `save_system_test.gd` assertions do not match any current AC
3. Test file is flagged as ORPHAN TEST in the coverage report
4. Report notes: "Orphan tests may belong to a past or future sprint, or AC was renamed"
5. Verdict is FULL COVERAGE or GAPS FOUND depending on overall AC coverage
   (orphan tests do not affect verdict, they are advisory)

**Assertions:**
- [ ] Orphan test is flagged in the report
- [ ] Orphan flag includes the filename and suggestion (past sprint / renamed AC)
- [ ] Orphan tests do not cause a GAPS FOUND verdict on their own
- [ ] Overall verdict reflects AC coverage only

---

### Case 5: Director Gate Check — No gate; regression-suite is a QA utility

**Fixture:**
- Sprint with stories and test files

**Input:** `$regression-suite`

**Expected behavior:**
1. Skill produces coverage report and writes it
2. No director agents are spawned
3. No gate IDs appear in output

**Assertions:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Verdict is FULL COVERAGE, GAPS FOUND, or CRITICAL GAPS — no gate verdict

---

## Protocol Compliance

- [ ] Reads story ACs from sprint files before scanning tests
- [ ] Matches ACs to tests by system name and scenario (not file name alone)
- [ ] Flags critical-priority untested ACs as CRITICAL GAPS
- [ ] Flags orphan tests (exist in tests/ but no AC matches)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Verdict is FULL COVERAGE, GAPS FOUND, or CRITICAL GAPS

---

## Coverage Notes

- The heuristic for matching an AC to a test (by system name + scenario keywords)
  is approximate; exact matching logic is defined in the skill body.
- Integration test coverage is mapped the same way as unit test coverage; no
  distinction in verdicts is made between the two.
- This skill does not run the tests — it maps AC text to test assertions. Test
  execution is handled by the CI pipeline.
