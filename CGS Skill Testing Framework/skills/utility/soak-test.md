# Skill Test Spec: $soak-test

## Skill Summary

`$soak-test` generates a human-executed endurance-test protocol for a named
target. Invocation is `$soak-test [target] [duration] [focus]`. The protocol
uses the existing memory, stability, and balance observations, reads configured
project budgets/platforms when present, and defines early-stop conditions. It
does not run the soak and does not claim the future soak has passed.

The only result of this workflow run is reported in ordinary language as
`Protocol written: [path]` or `Protocol not written: [reason]`. The protocol's
future PASS / PASS WITH CONCERNS / FAIL field is the sole test verdict.

---

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only `name` and non-empty `description`
- [ ] Invocation declares `[target] [duration] [focus]`
- [ ] Protocol header records the target, duration, focus, and engine
- [ ] Protocol contains PASS / PASS WITH CONCERNS / FAIL for the future soak
- [ ] Workflow output does not use COMPLETE as a file-write verdict
- [ ] One complete changeset is authorized before the protocol file is written
- [ ] No director gate is invoked

---

## Test Cases

### Case 1: Target and duration parse correctly

**Input:** `$soak-test gameplay 30m`

**Expected behavior and assertions:**

- [ ] Target is `gameplay`
- [ ] Duration is `30m`; focus defaults to `all`
- [ ] Checkpoints are T+0, T+10, T+20, and T+30
- [ ] The written protocol header identifies the gameplay target
- [ ] Successful persistence says `Protocol written: production/qa/soak-test-[date]-30m.md`
- [ ] No COMPLETE verdict is emitted

### Case 2: Missing target is collected once

**Input:** `$soak-test`

**Expected behavior and assertions:**

- [ ] The skill asks once for the gameplay loop, system, or scenario under test
- [ ] Duration and focus retain their existing defaults
- [ ] No protocol is generated until the target is known

### Case 3: Early termination is explicit

**Fixture:** a normal all-focus protocol.

**Assertions:**

- [ ] Pre-session instructions require the tester to review stop rules
- [ ] Crash or hang stops the session and records the occurrence time
- [ ] Data corruption stops the session
- [ ] A sustained breach of the configured budget stops the session
- [ ] An operating-system or device safety warning stops the session
- [ ] Any early-stop condition contributes to the protocol's future FAIL verdict

### Case 4: Platform adaptation stays within configured evidence

**Fixture:** `technical-preferences.md` declares a target platform and a memory
ceiling.

**Assertions:**

- [ ] The protocol may use the declared platform and configured memory ceiling
- [ ] It does not invent a hard-coded 300 MB mobile threshold
- [ ] It does not add network checks unless those are already part of the target/context
- [ ] It does not promise thermal/battery instrumentation not declared by the workflow

### Case 5: Existing output is not silently overwritten

**Fixture:** `production/qa/soak-test-[date]-1h.md` already exists.

**Assertions:**

- [ ] The existing path is detected before writing
- [ ] Updating that exact file and its intended changes are shown in the one changeset
- [ ] Declined or failed authorization reports `Protocol not written: [reason]`
- [ ] No extend/new mode is invented and the old file is not silently replaced

### Case 6: Protocol verdict remains distinct from generation

**Assertions:**

- [ ] PASS / PASS WITH CONCERNS / FAIL appear only as fields for the future executed soak
- [ ] Generating or writing the template does not set that future verdict
- [ ] Instructions to file bugs apply only after a human completes the protocol and records issues

---

## Protocol Compliance

- [ ] Collects target and applies existing duration/focus defaults
- [ ] Includes regular checkpoints and early-stop conditions
- [ ] Uses project-configured thresholds where available
- [ ] Requires one complete changeset authorization before writing
- [ ] Uses ordinary written/not-written statements, not a second verdict
- [ ] Remains a protocol generator; it never runs the endurance session
