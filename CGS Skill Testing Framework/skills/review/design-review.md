# Skill Test Spec: $design-review

## Skill Summary

`$design-review` reads a game design document (GDD) and evaluates it against
the project's 8-section design standard (Overview, Player Fantasy, Detailed
Rules, Formulas, Edge Cases, Dependencies, Tuning Knobs, Acceptance Criteria).
It checks for internal consistency, implementability, and cross-system
conflicts. It produces a verdict of APPROVED, NEEDS REVISION, or MAJOR
REVISION NEEDED. It is a read-only skill (no file writes) and runs as a
`context: fork` subagent.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings or numbered steps
- [ ] Contains verdict keywords: APPROVED, NEEDS REVISION, MAJOR REVISION NEEDED
- [ ] Remains read-only; no authorization prompt appears because the workflow does not modify files
- [ ] Output format is documented (review template shown in skill body)

---

## Test Cases

### Case 1: Happy Path — Complete GDD, all 8 sections present

**Fixture:**
- `design/gdd/light-manipulation.md` exists (use `_fixtures/minimal-game-concept.md`
  as a stand-in — represents a complete document with all required content)
- All 8 required sections are populated with substantive content
- Formulas section contains at least one formula with defined variables
- Acceptance Criteria section contains at least 3 testable criteria

**Input:** `$design-review design/gdd/light-manipulation.md`

**Expected behavior:**
1. Skill reads the target document in full
2. Skill reads AGENTS.md for project context and standards
3. Skill evaluates all 8 required sections (present/absent check)
4. Skill checks internal consistency (formulas match described behavior)
5. Skill checks implementability (rules are precise enough to code)
6. Skill outputs structured review with section-by-section status
7. Skill outputs APPROVED verdict

**Assertions:**
- [ ] Skill reads the target file before producing any output
- [ ] Output includes a "Completeness" section showing X/8 sections present
- [ ] Output includes an "Internal Consistency" section
- [ ] Output includes an "Implementability" section
- [ ] Output ends with a verdict line: APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED
- [ ] APPROVED verdict is given when all 8 sections are present and consistent

---

### Case 2: Failure Path — Incomplete GDD (4/8 sections)

**Fixture:**
- Create the case from this inline document description; no fixture file is required.
- `design/gdd/light-manipulation.md` has Overview, Player Fantasy, Detailed Rules,
  and Dependencies. Formulas, Edge Cases, Tuning Knobs, and Acceptance Criteria
  are absent.

**Input:** `$design-review design/gdd/light-manipulation.md`

**Expected behavior:**
1. Skill reads the document
2. Skill identifies 4 missing sections
3. Skill outputs "Completeness: 4/8 sections present"
4. Skill lists specifically which 4 sections are missing
5. Skill outputs MAJOR REVISION NEEDED verdict (not APPROVED or NEEDS REVISION)

**Assertions:**
- [ ] Output shows "4/8" in the completeness section (not a higher number)
- [ ] Output explicitly names each missing section (Formulas, Edge Cases, Tuning Knobs, Acceptance Criteria)
- [ ] Verdict is MAJOR REVISION NEEDED (not APPROVED or NEEDS REVISION) when ≥3 sections are missing
- [ ] Output does not suggest the document is implementation-ready
- [ ] Skill does not write any files (read-only enforcement)

---

### Case 3: Partial Path — 7/8 sections, minor inconsistency

**Fixture:**
- GDD has all sections except Formulas
- The described behavior mentions numeric values but no formulas are defined
- Acceptance Criteria exist but are vague ("feels good" rather than measurable)

**Input:** `$design-review design/gdd/[document].md`

**Expected behavior:**
1. Skill identifies missing Formulas section
2. Skill flags vague acceptance criteria as an implementability issue
3. Skill outputs NEEDS REVISION verdict (not APPROVED, not MAJOR REVISION NEEDED)
4. Skill provides specific remediation notes for each issue

**Assertions:**
- [ ] Verdict is NEEDS REVISION (not APPROVED, not MAJOR REVISION NEEDED) for 7/8 with issues
- [ ] Output identifies the missing Formulas section specifically
- [ ] Output flags the vague acceptance criteria as an implementability gap
- [ ] Each flagged issue has a specific, actionable remediation note

---

### Case 4: Edge Case — File not found

**Fixture:**
- The path provided does not exist in the project

**Input:** `$design-review design/gdd/nonexistent.md`

**Expected behavior:**
1. Skill attempts to read the file
2. File not found
3. Skill outputs an error message naming the missing file
4. Skill suggests checking the path or listing files in `design/gdd/`
5. Skill does NOT produce a verdict

**Assertions:**
- [ ] Skill outputs a clear error when the file is not found
- [ ] Skill does NOT output APPROVED, NEEDS REVISION, or MAJOR REVISION NEEDED when file is missing
- [ ] Skill suggests a corrective action (check path, list available GDDs)

---

---

### Case 5: Director Gate — no gate spawned regardless of review mode

**Fixture:**
- `design/gdd/light-manipulation.md` exists with all 8 sections
- `production/session-state/review-mode.txt` exists with `full` (most permissive mode)

**Input:** `$design-review design/gdd/light-manipulation.md` (with full review mode active)

**Expected behavior:**
1. Skill reads the GDD document
2. Skill does NOT read `review-mode.txt` — this skill has no director gates
3. Skill produces the review output normally
4. No director gate agents are spawned at any point
5. Verdict is APPROVED (all 8 sections present in fixture)

**Assertions:**
- [ ] Skill does NOT spawn any director gate agent (CD-, TD-, PR-, AD- prefixed agents)
- [ ] Skill does NOT read `review-mode.txt` or equivalent mode file
- [ ] The `--review` flag or `full` mode state has NO effect on whether directors spawn
- [ ] Output does not contain any "Gate: [GATE-ID]" entries
- [ ] Skill IS the review — it does not delegate the review to a director

---

### Case 6: Unsupported document types stop without a verdict

**Inputs:** missing target; multiple targets; directory; non-Markdown file;
project-external path; `game-concept.md`; `systems-index.md`; review report; or
any Markdown file outside the supported `design/gdd/` system-GDD set.

**Assertions:**
- [ ] Each invalid input produces a clear error and no verdict
- [ ] The eight-section system-GDD standard is not applied to concept, UX, narrative, level, or report documents
- [ ] No file is modified and no authorization prompt appears

---

### Case 7: Full review respects capacity and reports specialist failure

**Fixture:** more relevant specialist roles than available subagent slots, with
one attempted specialist failing.

**Assertions:**
- [ ] Roles are deduplicated and run in bounded batches that leave space for the primary task
- [ ] No unstarted or failed role is represented by a simulated result
- [ ] Completed findings are still reported with the failed role and reason listed
- [ ] If missing evidence prevents a clean conclusion, no APPROVED verdict is produced
- [ ] If no required specialist succeeds, the workflow ends with an error and no verdict

---

### Case 8: Revision verdict remains read-only

**Assertions:**
- [ ] NEEDS REVISION and MAJOR REVISION NEEDED list exact sections to change
- [ ] The workflow does not revise the GDD, update systems-index, or append a review log
- [ ] No option can mark revised content Approved without a later re-review

---

## Protocol Compliance

- [ ] Does NOT use file-editing operations (read-only skill)
- [ ] Presents complete findings before any verdict
- [ ] Does not ask for approval before producing output (no writes to approve)
- [ ] Ends with recommended next step (e.g., fix issues and re-run, or proceed to `$map-systems`)

---

## Coverage Notes

- Cross-system consistency checking (Case 3 in the skill's own phase list) is
  not directly tested here because it requires multiple GDD files to compare;
  this is covered by the `$review-all-gdds` spec instead.
- The skill's `context: fork` behavior (running as a subagent) is not tested
  at the spec level — this is a runtime behavior verified manually.
- Performance and edge cases involving very large GDD files are not in scope.

## P1 Regression Assertions

- [ ] The complete root-to-target AGENTS chain is read and listed
- [ ] Related reads are limited to explicit links, direct Dependencies, game concept, and explicitly associated narrative files
- [ ] Dependencies distinguish existing, listed-not-authored, unknown, and explicitly broken links
- [ ] Empty/placeholder headings fail completeness; formulas, edge cases, tuning knobs, and ACs satisfy content-level directory rules
- [ ] Verdict mapping is deterministic: no blocker APPROVED, local blocker NEEDS REVISION, core contradiction/unresolved decision/3+ substantive omissions MAJOR REVISION NEEDED
- [ ] No director overrides the mapping; primary reviewer merges specialist results by location+defect
- [ ] Findings require evidence, impact, classification, and an actionable correction without quota-driven issue invention
- [ ] Unconfigured engine skips engine review without guessing
- [ ] lean/solo show no fabricated specialist/director output
- [ ] Scope Signal uses mutually exclusive XL→L→M→S bands (7+, 5–6, 3–4, 0–2 dependencies)
