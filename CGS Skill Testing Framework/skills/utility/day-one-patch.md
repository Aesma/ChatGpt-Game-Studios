# Skill Test Spec: $day-one-patch

## Skill Summary

`$day-one-patch` is an execution-oriented mini-sprint for safe P1/P2 launch
fixes. It scopes, locates, authorizes, implements, verifies, and records the
patch. Canonical bugs live in `production/qa/bugs/`. It is not a read-only
planning utility.

---

## Static Assertions

- [ ] Missing/invalid/non-Release-or-Polish stage stops before spawn or write
- [ ] No required input references `production/gate-checks/`
- [ ] One complete changeset includes rollback, source/config, tests, and record
- [ ] P0/CRITICAL issues stop ordinary patch execution and point to `$hotfix`
- [ ] QA FAIL cannot produce a PASS patch record

---

## Test Cases

### Case 1: Scope-only stop outside Release/Polish

**Assertions:**
- [ ] Missing, invalid, Concept, Systems Design, Technical Setup, Pre-Production, or Production stage stops
- [ ] No role is spawned
- [ ] No file is written
- [ ] No patch-complete result is emitted

---

### Case 2: Full execution after exact read-only location

**Fixture:**
- Stage is Release or Polish
- Safe P1/P2 bugs exist under `production/qa/bugs/`
- Existing release/launch checklist and QA sign-off artifacts cover the build

**Assertions:**
- [ ] lead-programmer first identifies exact candidate source/config and test files read-only
- [ ] release-manager first drafts rollback read-only
- [ ] Rollback, source/config, tests, and final patch record are shown in one changeset before the first write
- [ ] Implementation and verification happen only after that authorization
- [ ] A newly discovered file pauses execution for an expanded preview

---

### Case 3: Locator or implementation agent failure

**Assertions:**
- [ ] Failure is surfaced with the affected fix and partial evidence
- [ ] Unknown source/test files are not guessed into an authorized write
- [ ] The workflow does not silently continue to a complete patch record

---

### Case 4: QA FAIL after implementation

**Assertions:**
- [ ] The failing fix and all files it changed are listed
- [ ] User chooses a within-boundary fix or a specific revert
- [ ] Remaining changes are retested as a combination
- [ ] Until restoration/fix and verification pass, no Phase 6 PASS record is written

---

### Case 5: P0/CRITICAL issue

**Assertions:**
- [ ] The issue is excluded from ordinary day-one scope
- [ ] Execution stops before patch writes
- [ ] Output gives explicit existing `$hotfix` guidance
- [ ] P0 is not treated as a four-hour ordinary patch candidate

---

### Case 6: Scope sources and no-issue behavior

**Assertions:**
- [ ] `known-bugs`, `cert-feedback`, and `all` filter the actual inputs
- [ ] Unknown/empty/conflicting scope stops; no argument defaults to all
- [ ] Cert feedback requires user-supplied existing text/file
- [ ] No eligible issue produces no empty rollback/patch record
- [ ] Open deferred AC from Done stories is included only when relevant and still open

---

### Case 7: Security, effort, ordering, and verification boundary

**Assertions:**
- [ ] Open critical/high security blocks ordinary completion; lower findings remain visible
- [ ] Unknown effort defaults to defer until read-only lead-programmer evidence exists
- [ ] Fixes run in dependency/approved order and a blocked fix stops dependents
- [ ] Targeted checks run directly; a full `$smoke-check` requires explicit separate invocation

---

## Protocol Compliance

- [ ] Uses canonical `production/qa/bugs/`
- [ ] Reads real stage/checklist/QA artifacts rather than a nonexistent gate report
- [ ] Exact write ownership is known before authorization
- [ ] One complete changeset authorization covers the mini-sprint
- [ ] Verification results control whether a final patch record may claim PASS
