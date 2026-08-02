# Skill Test Spec: $dev-story

## Skill Summary

`$dev-story` validates the current story contract, plans exact writes, obtains
one complete authorization, delegates implementation to one primary writer, and
runs affected tests. It leaves story/sprint status In Progress. It does not
embed LP-CODE-REVIEW or close the story; `$code-review` and `$story-done`
remain separate next steps.

---

## Static Assertions

- [ ] No story, sprint, active, source, or test write occurs before the complete plan is authorized
- [ ] ADR references are a unique list with exactly one explicit primary
- [ ] Every real ADR reference must resolve uniquely and be Accepted
- [ ] Config/Data N/A is accepted only under the narrow reasoned exception
- [ ] One primary programmer owns all listed source/config and test writes
- [ ] Actual test execution controls verified/completion wording

---

## Test Cases

### Case 1: Happy Path — one primary and Accepted secondaries

**Assertions:**
- [ ] Every ADR resolves to exactly one file and every Status is Accepted
- [ ] Primary Decision/Guidelines and every secondary constraint enter the context package
- [ ] Exact story, sprint, active, source/config, and test operations are authorized before writes
- [ ] Primary writer ownership does not overlap a read-only engine reviewer
- [ ] Passing test command and result are recorded
- [ ] Story and sprint remain In Progress; no Complete status is written

---

### Case 2: ADR list validation blocks before writes/spawn

**Fixtures include:** secondary Proposed/Deprecated/Superseded; missing or
ambiguous ADR file; duplicate reference; malformed reference; zero primary; two
primaries; missing Status.

**Assertions:**
- [ ] All detected ADR errors are listed together
- [ ] No story/sprint/session status changes
- [ ] No programmer is spawned
- [ ] No list-first fallback is used to guess primary

---

### Case 3: Valid Config/Data N/A

**Fixture:** Type exactly Config/Data with sole
`N/A — update existing balance table values; no architecture pattern`.

**Assertions:**
- [ ] ADR file loading is skipped
- [ ] TR, AC, manifest, and engine preferences are still loaded
- [ ] A primary programmer, not the orchestrator, owns the authorized data edit

---

### Case 4: Invalid N/A

**Assertions:**
- [ ] Non-Config/Data N/A is blocked
- [ ] Empty, blank, TBD, or placeholder reason is blocked
- [ ] N/A mixed with real ADR is blocked
- [ ] Missing ADR field is blocked before writes/spawn

---

### Case 5: Manifest staleness cannot be disguised

**Assertions:**
- [ ] User may include a real version update and use current rules, or stop for a diff
- [ ] There is no old-rules option that writes the current manifest version
- [ ] Stopping leaves story status and version unchanged

---

### Case 6: Missing dependency is BLOCKED

**Assertions:**
- [ ] Missing, zero-match, or ambiguous dependency resolution stops before authorization/spawn
- [ ] Warning-only continuation is not allowed

---

### Case 7: Test failure or unavailable execution

**Assertions:**
- [ ] Created test files are actually run with the affected configured command
- [ ] A FAIL produces Partial/Blocked, leaves affected AC unchecked, and never says Implementation Complete
- [ ] An unavailable command produces Implemented, Not Verified and leaves AC unchecked
- [ ] Only actual PASS or directly checked non-automated evidence may mark an AC covered

---

### Case 8: No embedded LP-CODE-REVIEW or closure

**Assertions:**
- [ ] Full/lean/solo do not run LP-CODE-REVIEW in this workflow
- [ ] Output points to the existing `$code-review` step
- [ ] `$story-done` remains the sole closure step

---

### Case 9: Status, AC, routing, and engine configuration

**Assertions:**
- [ ] Only Ready/In Progress proceeds; Blocked/unknown stops and Done requires explicit reopen
- [ ] TBD/subjective AC is clarified before authorization/spawn
- [ ] Routing precedence selects exactly one primary writer for overlapping contexts
- [ ] Unconfigured engine blocks engine-specific code; pure data may proceed with a warning
- [ ] Sprint YAML uses canonical `in_progress` consistently

---

### Case 10: Evidence, blocked writer, and active state

**Assertions:**
- [ ] Integration uses the single evidence alternative declared by the story
- [ ] Missing Visual/UI evidence remains blocking for story closure
- [ ] A blocked writer can only produce Partial/Blocked with affected AC unchecked
- [ ] active.md updates one current-task/STATUS block without appending stale duplicates

---

## Protocol Compliance

- [ ] Unlisted files pause the run for expanded authorization
- [ ] One writer owns source/config and tests; secondary review is read-only
- [ ] Dependency and ADR failures occur before side effects
- [ ] Summary wording reflects actual implementation and verification state
- [ ] Ends with `$code-review` then `$story-done`
