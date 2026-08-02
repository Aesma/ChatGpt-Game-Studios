# Skill Test Spec: $code-review

## Skill Summary

`$code-review` performs an architectural code review of source files in `src/`,
checking coding standards from `AGENTS.md` (doc comments on public APIs,
dependency injection over singletons, data-driven values, testability). Findings
are read-only. Lead-programmer owns the overall review; configured engine
specialists and qa-tester run automatically only when their file/story inputs
apply. These are specialist reviews, not director gates. Verdicts are APPROVED,
APPROVED WITH SUGGESTIONS, or CHANGES REQUIRED.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: APPROVED, APPROVED WITH SUGGESTIONS, CHANGES REQUIRED
- [ ] Remains read-only; no authorization prompt appears because the workflow does not modify files
- [ ] Has a next-step handoff (what to do with findings)

---

## Director Gate Checks

None. Code review is a read-only advisory skill; no gates are invoked.

---

## Test Cases

### Case 1: Happy Path — Source file follows all coding standards

**Fixture:**
- `src/gameplay/health_component.gd` exists with:
  - All public methods have doc comments (`##` notation)
  - No singletons used; dependencies injected via constructor
  - No hardcoded values; all constants reference `assets/data/`
  - ADR reference in file header: `# ADR: docs/architecture/adr-004-health.md`
  - Referenced ADR has `Status: Accepted`

**Input:** `$code-review src/gameplay/health_component.gd`

**Expected behavior:**
1. Skill reads the source file
2. Skill checks all coding standards: doc comments, DI, data-driven, ADR status
3. All checks pass
4. Skill outputs findings summary with all checks PASS
5. Verdict is APPROVED

**Assertions:**
- [ ] Each coding standard check is listed in the output
- [ ] All checks show PASS when standards are met
- [ ] Skill reads referenced ADR to confirm its status
- [ ] Verdict is APPROVED
- [ ] No edits are made to any file

---

### Case 2: Needs Changes — Missing doc comment and singleton usage

**Fixture:**
- `src/ui/inventory_ui.gd` has:
  - 2 public methods without doc comments
  - Uses `GameManager.instance` (singleton pattern)
  - All other standards met

**Input:** `$code-review src/ui/inventory_ui.gd`

**Expected behavior:**
1. Skill reads the source file
2. Skill detects: 2 missing doc comments on public methods
3. Skill detects: singleton usage at specific lines (e.g., line 42, line 87)
4. Findings list the exact method names and line numbers
5. Verdict is CHANGES REQUIRED

**Assertions:**
- [ ] Missing doc comments are listed with method names
- [ ] Singleton usage is flagged with file and line number
- [ ] Verdict is CHANGES REQUIRED when BLOCKING-level standard violations exist
- [ ] Skill does not edit the file — findings are for the developer to act on
- [ ] Output suggests replacing singleton with dependency injection

---

### Case 3: Architecture Risk — ADR reference is Proposed, not Accepted

**Fixture:**
- `src/core/save_system.gd` has a header comment: `# ADR: docs/architecture/adr-010-save.md`
- `adr-010-save.md` exists but has `Status: Proposed`
- Code itself follows all other coding standards

**Input:** `$code-review src/core/save_system.gd`

**Expected behavior:**
1. Skill reads the source file
2. Skill reads referenced ADR — finds `Status: Proposed`
3. Skill flags this as ARCHITECTURE RISK (code is implementing an unaccepted ADR)
4. Other coding standard checks pass
5. Verdict is APPROVED WITH SUGGESTIONS (risk flag is advisory)

**Assertions:**
- [ ] Skill reads referenced ADR file to check its status
- [ ] ARCHITECTURE RISK is flagged when ADR status is Proposed
- [ ] Verdict is APPROVED WITH SUGGESTIONS for ADR risk — advisory severity
- [ ] Output recommends resolving the ADR before the code goes to production

---

### Case 4: Edge Case — No source files found at specified path

**Fixture:**
- User calls `$code-review src/networking/`
- `src/networking/` directory does not exist

**Input:** `$code-review src/networking/`

**Expected behavior:**
1. Skill attempts to read files in `src/networking/`
2. Directory or files not found
3. Skill outputs an error: "No source files found at `src/networking/`"
4. Skill suggests checking `src/` for valid directories
5. No verdict is emitted (nothing was reviewed)

**Assertions:**
- [ ] Skill does not crash when path does not exist
- [ ] Output names the attempted path in the error message
- [ ] Output suggests checking `src/` for valid file paths
- [ ] No verdict is emitted when there is nothing to review

---

### Case 5: Specialist Contract — Applicable reviewers run automatically

**Fixture:**
- Source file follows most standards but has 1 CONCERNS-level finding (a magic number)
- `review-mode.txt` contains `full`

**Input:** `$code-review src/gameplay/loot_system.gd`

**Expected behavior:**
1. Skill reads and reviews the source file
2. Lead-programmer performs the overall review
3. The configured language specialist runs for the target file
4. qa-tester runs only when a supplied story provides the required QA context
5. Skill presents findings with APPROVED WITH SUGGESTIONS

**Assertions:**
- [ ] Lead-programmer review is automatic when available
- [ ] Applicable engine/QA specialists are automatic and are not mislabeled as gates
- [ ] No code edits are made
- [ ] Verdict is APPROVED WITH SUGGESTIONS for advisory-only findings

---

## Protocol Compliance

- [ ] Reads source file(s) and coding standards before reviewing
- [ ] Reads the full root-to-target `AGENTS.md` chain for every target and lists the files used
- [ ] Lists each coding standard check in findings output
- [ ] Does not edit any source files (read-only skill)
- [ ] Specialist reviews do not introduce a director gate
- [ ] Verdict is one of: APPROVED, APPROVED WITH SUGGESTIONS, CHANGES REQUIRED
- [ ] Any blocker, ADR violation, or untestable required AC maps to CHANGES REQUIRED; advisory-only maps to APPROVED WITH SUGGESTIONS; no findings maps to APPROVED

---

## Coverage Notes

- Batch review of all files in a directory is not explicitly tested; behavior
  is assumed to apply the same checks file by file and aggregate the verdict.
- Test coverage checks (verifying corresponding test files exist) are a stretch
  goal not tested here; that is primarily the domain of `$test-evidence-review`.
