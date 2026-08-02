# Skill Test Spec: $start

## Skill Summary

`$start` is guided onboarding. It detects existing project evidence, asks new
users which of the current A–D starting situations fits, recommends an existing
workflow, and prepares only `production/stage.txt` and
`production/review-mode.txt` when either configuration is missing or an invalid
stage replacement is explicitly approved. It never chooses an engine, scaffolds
the repository, or auto-runs the recommended workflow.

---

## Static Assertions

- [ ] YAML frontmatter contains only `name` and non-empty `description`
- [ ] The workflow takes no arguments
- [ ] The only configured outputs are stage.txt and review-mode.txt
- [ ] One complete changeset approval covers every pending output
- [ ] No director gate or automatic workflow handoff occurs
- [ ] Verdict is COMPLETE after orientation/handoff, independent of whether the user authorized optional configuration writes

---

## Test Cases

### Case 1: New user chooses No idea yet

**Fixture:** no concept, source, production artifacts, stage, or review mode.

**Expected behavior and assertions:**

- [ ] The A–D starting-state question is the first user-facing question
- [ ] Path A recommends `$brainstorm open`
- [ ] Initial stage recommendation is Concept
- [ ] Review mode is selected from full/lean/solo
- [ ] Both pending configuration files are shown in one changeset
- [ ] No engine is selected and no workflow is auto-run

### Case 2: Existing valid stage is authoritative

**Fixture:** `production/stage.txt` contains `Polish`; source and ADR evidence
could otherwise infer Production.

**Assertions:**

- [ ] Existing Polish is preserved
- [ ] Contradictory lower-stage evidence does not downgrade the file
- [ ] stage.txt is absent from the pending changeset

### Case 3: Brownfield evidence never regresses because engine is unset

**Fixture:** engine placeholder remains, while architecture/ADRs and production
source or sprint planning exist.

**Assertions:**

- [ ] Architecture/ADR evidence recommends at least Pre-Production
- [ ] Source or sprint/milestone planning recommends at least Production
- [ ] The placeholder engine does not force Concept
- [ ] Conflicting evidence is shown for user decision before any stage write

### Case 4: Returning user still repairs missing configuration

**Fixture:** engine is configured and game concept exists; stage.txt is missing;
review-mode.txt contains `lean`.

**Assertions:**

- [ ] The A–D creative questionnaire is skipped
- [ ] Existing review mode remains unchanged
- [ ] Only stage.txt is proposed and authorized
- [ ] If both configuration files are already valid, no write approval is requested

### Case 5: Invalid stage requires an explicit replacement decision

**Fixture:** stage.txt is empty or contains an unrecognized value.

**Assertions:**

- [ ] The invalid value and evidence-based recommendation are reported
- [ ] The workflow does not overwrite it silently
- [ ] stage.txt enters the changeset only after the user chooses replacement

### Case 6: Existing-work route keeps current scope

**Assertions:**

- [ ] Path D reports detected artifacts and recommends project-stage-detect/adopt as applicable
- [ ] It does not create directories, AGENTS.md, or technical-preferences.md
- [ ] It does not invoke `$setup-engine [engine]`; it only recommends a next command
- [ ] The final handoff asks which existing next step the user wants and never auto-runs it

---

## Protocol Compliance

- [ ] Detects stage before proposing initialization
- [ ] Uses Concept, Systems Design, Technical Setup, Pre-Production, Production, Polish, Release
- [ ] Existing legal stage is preserved by default
- [ ] Missing configurations alone are written after one complete preview
- [ ] Returning users skip creative questions but not configuration validation
- [ ] No project naming, engine chooser, bulk directory scaffold, or stub files are part of this workflow
