# Skill Test Spec: $create-stories

## Skill Summary

`$create-stories` writes the existing Markdown/header-and-sections story format
to `production/epics/[epic-slug]/story-NNN-[slug].md`. The current Requirement
line carries the TR-ID and Acceptance Criteria remain in their existing section;
the workflow does not require frontmatter, Priority, or a separate Definition of
Done field. ADR references are a non-empty list with exactly one explicit
primary, except for the narrowly valid Config/Data N/A form.

---

## Static Assertions

- [ ] Output path and naming match the existing epic-slug directory contract
- [ ] Tests do not require fields absent from the current story template
- [ ] Status is computed per story rather than hard-coded Ready
- [ ] Full QL-STORY-READY receives planned path plus complete inline draft before writes
- [ ] Lean and solo do not spawn qa-lead after recording a gate skip

---

## Test Cases

### Case 1: Happy Path — existing fields, Accepted ADR list

**Fixture:**
- One epic decomposes into three stories
- Each story has a stable TR-ID
- All ADR references are Accepted and each list has exactly one explicit primary
- Review mode resolves to lean

**Assertions:**
- [ ] Files use `production/epics/[epic-slug]/story-NNN-[slug].md`
- [ ] Requirement and Acceptance Criteria use their current locations
- [ ] No Priority, independent DoD, or frontmatter field is invented
- [ ] qa-lead is not spawned; any derived QA cases are marked unreviewed
- [ ] All files and EPIC/index edits are included in one changeset authorization

---

### Case 2: Planned-path gate contract

**Fixture:** review mode resolves to full

**Assertions:**
- [ ] QL-STORY-READY receives one complete inline draft and planned final path per story
- [ ] Planned paths are not described as files already on disk
- [ ] Per-story verdicts are returned before the write authorization
- [ ] No story file is written before the gate resolves

---

### Case 3: Proposed ADR and missing TR-ID compute Blocked

**Assertions:**
- [ ] A Proposed ADR is shown with its actual Status and makes that story Blocked
- [ ] A missing stable TR-ID makes that story Blocked
- [ ] The workflow never writes `TR-[system]-???` as a developer-ready identifier
- [ ] Other fully valid stories keep their independently computed status

---

### Case 4: Multiple ADR references require one explicit primary

**Assertions:**
- [ ] All applicable references are listed without duplicates
- [ ] Exactly one item is explicitly marked primary; list order is not a substitute
- [ ] Any non-Accepted secondary reference makes the story Blocked
- [ ] The preview shows every reference and actual Status

---

### Case 5: Valid Config/Data N/A

**Fixture:** Type is exactly Config/Data and the only ADR reference is
`N/A — balance table values only; no architectural pattern`.

**Assertions:**
- [ ] The story may proceed without resolving an ADR file
- [ ] The specific reason is preserved
- [ ] N/A is not mixed with a real ADR

---

### Case 6: Invalid N/A forms

**Assertions:**
- [ ] Non-Config/Data N/A is Blocked
- [ ] Empty, whitespace-only, TBD, or placeholder reason is Blocked
- [ ] N/A mixed with a real ADR is Blocked
- [ ] Missing ADR reference field is Blocked

---

### Case 7: No argument or missing epic

**Assertions:**
- [ ] No argument lists available EPIC.md files and waits for a choice
- [ ] Missing epic path produces a clear error
- [ ] EPIC.md and index files are excluded from story globs
- [ ] No story is written without a valid selected epic

---

### Case 8: Evidence, numbering, and integration alternative

**Assertions:**
- [ ] Existing story numbers are preserved and new stories take the next available number
- [ ] Duplicate title/TR-ID requires update or skip
- [ ] Each story stores exactly one type-appropriate evidence path/alternative
- [ ] Integration defaults to an automated test; manual playtest requires a GDD-AC reason

---

### Case 9: Input/index/gate gaps and mixed type

**Assertions:**
- [ ] Missing EPIC, GDD, manifest, or TR registry stops before any Ready story
- [ ] Mixed unsplittable type uses Integration > Logic > UI > Visual/Feel > Config/Data with reason
- [ ] GAPS may be revised or accepted only as non-Ready; INADEQUATE cannot proceed
- [ ] Missing/ambiguous EPIC or index target is reported as partial, never silently skipped

---

## Protocol Compliance

- [ ] Existing story field set is consistent with consumers
- [ ] Validity and Blocked reasons are visible before authorization
- [ ] Full gate is pre-write; lean/solo do not secretly delegate QA work
- [ ] One complete changeset authorization covers the story batch and listed edits
- [ ] Ends with the existing `$story-readiness` then `$dev-story` handoff
