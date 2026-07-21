# Skill Test Spec: $code-review

## Skill Summary

`$code-review` performs a strictly read-only architectural and code-quality
review of specified source files. It automatically delegates substantive work
to `lead-programmer` when available and invokes all applicable engine and QA
reviewers. Every result includes mandatory coverage for target files, applicable
checks, explicit ADR evidence, and required reviewers.

Finding severities are `BLOCKING`, `WARNING`, and `INFO`. Verdicts use this
deterministic precedence:

1. `PARTIAL` when mandatory coverage is incomplete.
2. `NEEDS CHANGES` when coverage is complete and a `BLOCKING` finding exists.
3. `CONCERNS` when coverage is complete, no blocking finding exists, and a
   `WARNING` finding exists.
4. `APPROVED` when coverage is complete with no blocking or warning findings.

No director gate is invoked, and no file is edited.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: APPROVED, CONCERNS, NEEDS CHANGES, PARTIAL
- [ ] Defines finding severities: BLOCKING, WARNING, INFO
- [ ] Defines a mandatory coverage gate for files, checks, ADR evidence, and required reviewers
- [ ] Remains strictly read-only; no authorization prompt appears because the workflow does not modify files
- [ ] Has a next-step handoff for each verdict

---

## Director Gate Checks

None. Code review is read-only; domain reviewers are not director gates.

---

## Test Cases

### Case 1: Happy Path — Complete coverage and accepted ADR

**Fixture:**
- `src/gameplay/health_component.gd` exists and follows every applicable coding standard
- The file header references `docs/architecture/adr-004-health.md`
- The referenced ADR has `Status: Accepted` and readable Decision and Consequences sections
- `lead-programmer` and every applicable engine or QA reviewer return usable clean reviews
- Every applicable check can be evaluated as PASS or evidence-backed N/A

**Input:** `$code-review src/gameplay/health_component.gd`

**Expected behavior:**
1. Skill builds and fully reviews the target manifest
2. Skill checks and reports every applicable standard
3. Skill confirms the ADR is Accepted before using it as compliance evidence
4. Skill automatically runs and collects every required reviewer
5. Coverage is COMPLETE and verdict is APPROVED

**Assertions:**
- [ ] Coverage reports target files, checks, ADR evidence, and required reviewers
- [ ] Accepted ADR Decision and Consequences are evaluated
- [ ] All checks are PASS or evidence-backed N/A
- [ ] Verdict is APPROVED only after coverage is COMPLETE
- [ ] No file is edited

---

### Case 2: Needs Changes — Blocking standards violations

**Fixture:**
- `src/ui/inventory_ui.gd` has two public methods without doc comments and uses `GameManager.instance`
- A referenced Accepted ADR is readable and all required reviewers complete
- All remaining mandatory checks are evaluated

**Input:** `$code-review src/ui/inventory_ui.gd`

**Expected behavior:**
1. Skill identifies both missing comments and singleton usage with file and line evidence
2. Findings use BLOCKING severity
3. Coverage is COMPLETE
4. Verdict is NEEDS CHANGES

**Assertions:**
- [ ] Missing comments identify exact methods
- [ ] Singleton usage includes file and line evidence
- [ ] BLOCKING findings map to NEEDS CHANGES when coverage is complete
- [ ] No file is edited

---

### Case 3: Architecture Risk — ADR is not Accepted

**Fixture:**
- `src/core/save_system.gd` references `docs/architecture/adr-010-save.md`
- The ADR exists and has `Status: Proposed`
- All other mandatory checks and reviewers complete

**Input:** `$code-review src/core/save_system.gd`

**Expected behavior:**
1. Skill reads and reports the ADR status
2. Skill does not claim compliance and reports ADR_NOT_EVALUATED
3. Skill emits an ARCHITECTURE RISK finding with WARNING severity
4. Coverage is COMPLETE because the explicit reference was resolved and status-checked
5. Verdict is CONCERNS

**Assertions:**
- [ ] Only Accepted ADRs are used as compliance evidence
- [ ] Proposed ADR yields ADR_NOT_EVALUATED and WARNING
- [ ] WARNING maps to CONCERNS when coverage is complete
- [ ] No file is edited

---

### Case 4: Input Error — Target cannot form a manifest

**Fixture:** `src/networking/` does not exist.

**Input:** `$code-review src/networking/`

**Expected behavior:**
1. Skill reports that no source files were found at the attempted path
2. Skill suggests checking valid project paths
3. Skill emits no verdict because no target manifest exists

**Assertions:**
- [ ] Missing input does not crash the workflow
- [ ] Error names the attempted path
- [ ] No verdict is emitted
- [ ] No file is edited

---

### Case 5: Required reviewers are automatic

**Fixture:**
- A valid source file references an Accepted ADR
- Project configuration makes `lead-programmer` and one engine specialist required
- A Logic story also makes `qa-tester` required
- All three reviewers return usable results; one reports a WARNING

**Input:** `$code-review src/gameplay/loot_system.gd production/epics/loot/story-001.md`

**Expected behavior:**
1. Skill lists why each reviewer applies
2. Skill spawns all required reviewers automatically and in parallel
3. No director gate is invoked
4. Coverage is COMPLETE and verdict is CONCERNS

**Assertions:**
- [ ] Reviewer delegation is automatic, not merely suggested
- [ ] All required reviewer results are collected
- [ ] No director gate is invoked
- [ ] WARNING maps to CONCERNS

---

### Case 6: Missing ADR reference forces PARTIAL

**Fixture:**
- A readable source file contains no ADR reference
- No story path with an ADR reference is provided
- All non-ADR checks and required reviewers complete

**Input:** `$code-review src/gameplay/unreferenced_system.gd`

**Expected behavior:**
1. Skill reports ADR_NOT_EVALUATED
2. Skill does not report ADR compliance
3. Coverage lists the missing ADR evidence as a gap
4. Verdict is PARTIAL and approval is prohibited

**Assertions:**
- [ ] No ADR never maps to COMPLIANT
- [ ] Missing ADR evidence is named in coverage
- [ ] PARTIAL takes precedence over otherwise clean findings

---

### Case 7: Reviewer timeout forces PARTIAL

**Fixture:**
- Target files, checks, and Accepted ADR evidence are otherwise complete
- One required engine reviewer times out after the bounded wait and retry

**Input:** `$code-review src/gameplay/timed_review.gd`

**Expected behavior:**
1. Skill records REVIEWER_TIMEOUT for the named reviewer
2. Skill does not infer a clean reviewer result
3. Coverage is PARTIAL
4. Verdict is PARTIAL even if another reviewer found a BLOCKING issue

**Assertions:**
- [ ] Required reviewer completion count is reported
- [ ] Timeout is a named coverage gap
- [ ] PARTIAL has precedence over findings-based verdicts
- [ ] APPROVED is never emitted

---

### Case 8: Required file or check gap forces PARTIAL

**Fixture:**
- A directory manifest contains three source files but one cannot be read
- At least one applicable standards check is UNVERIFIED
- Completed review work contains no warning or blocking finding

**Input:** `$code-review src/gameplay/`

**Expected behavior:**
1. Skill reports reviewed count versus manifest count and names the unreadable file
2. Skill names the UNVERIFIED check
3. Coverage is PARTIAL and verdict is PARTIAL

**Assertions:**
- [ ] A file is never silently omitted
- [ ] UNVERIFIED is not treated as PASS or N/A
- [ ] Incomplete mandatory coverage prohibits APPROVED

---

## Protocol Compliance

- [ ] Reads target files and applicable standards before reviewing
- [ ] Lists every applicable check as PASS, FAIL, N/A, or UNVERIFIED with evidence
- [ ] Confirms ADR status and evaluates only Accepted ADRs for compliance
- [ ] Automatically delegates required domain reviewers and reports their completion
- [ ] Reports mandatory coverage before the verdict
- [ ] Does not edit any file
- [ ] No director gates are invoked
- [ ] Verdict is exactly one of: APPROVED, CONCERNS, NEEDS CHANGES, PARTIAL
- [ ] PARTIAL takes precedence whenever mandatory coverage is incomplete

---

## Coverage Notes

- Directory aggregation must preserve the complete resolved manifest; any omitted or unreadable file is PARTIAL.
- Corresponding test-file existence remains owned by `$test-evidence-review` and is not an approval condition here.
