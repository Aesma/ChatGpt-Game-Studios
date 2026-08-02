# Skill Test Spec: $test-evidence-review

## Skill Summary

`$test-evidence-review` reviews evidence per story. Inputs are a story path, `sprint`,
or a system name. It reports ADEQUATE / INCOMPLETE / MISSING per story and
aggregates the worst verdict. It checks criterion coverage plus naming, determinism,
isolation, and unexplained hardcoded data. It never edits tests or evidence; only the
optional authorized review report is writable.

## Static Assertions

- [ ] YAML frontmatter has only `name` and non-empty `description`
- [ ] Accepted scopes are story path, current sprint, and system name
- [ ] Verdicts are exactly ADEQUATE, INCOMPLETE, and MISSING
- [ ] Explicit story evidence paths are checked before fallback conventions
- [ ] Current execution status participates in ADEQUATE
- [ ] Naming, determinism, isolation, and hardcoded-data quality are checked

## Cases

### Case 1: Story evidence is adequate

- Story declares a project-local unit-test path and every acceptance criterion maps to an assertion.
- A current result for the same scope records PASS.
- Naming, determinism, isolation, and test data satisfy coding standards.
- Expected: declared path is used and story verdict is ADEQUATE.

### Case 2: Test exists but was not run

- The declared test has strong static quality but no identifiable current execution result.
- Expected: `execution status unknown`; verdict is INCOMPLETE, never ADEQUATE or shipping-ready.

### Case 3: Config story has an unrelated smoke report

- A global smoke PASS exists but its body does not mention the story/system or criterion.
- Expected: it is not accepted as evidence; result is MISSING or INCOMPLETE according to other evidence.

### Case 4: Declared path precedes fallback

- Story declares a valid custom evidence path while a similarly named conventional file also exists.
- Expected: review uses the declared path. Fallback is used only when no declaration exists and is labeled inferred.

### Case 5: Sprint/system aggregation

- All story paths come from the active sprint/epic context.
- Each story receives ADEQUATE/INCOMPLETE/MISSING and the overall verdict is the worst present.

## Assertions

- [ ] No test-path-only invocation mode or PASS/WARNINGS/FAIL verdict remains
- [ ] An unrelated smoke report cannot satisfy a Config/Data story
- [ ] No current pass result means at most INCOMPLETE
- [ ] ADEQUATE is described as static evidence-quality sufficiency, not release/shipping approval
- [ ] Generic names, timing dependence, live external calls, and unexplained magic data are evaluated inside Automated Test Quality
- [ ] The review never modifies test or evidence files
- [ ] Optional report writing uses the single authorized changeset only when requested
