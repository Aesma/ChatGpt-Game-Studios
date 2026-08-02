# Skill Test Spec: $bug-report

## Skill Summary

`$bug-report` creates and maintains bug files under the single authoritative
directory `production/qa/bugs/`. New reports use
`BUG-NNNN-[slug].md`. Verify and Close edit that existing file and terminate;
they never fall through into new-report saving.

---

## Static Assertions

- [ ] New-report target is `production/qa/bugs/BUG-NNNN-[slug].md`
- [ ] Verify and Close resolve `production/qa/bugs/[BUG-ID]-*.md`
- [ ] `production/bugs/` is not an output contract
- [ ] Runtime verification cannot be inferred from static code search
- [ ] Verify and Close explicitly end before Phase 3

---

## Case 1: Description/Analyze saves to the canonical path

**Assertions:**

- [ ] The preview names `production/qa/bugs/BUG-NNNN-[slug].md`
- [ ] The report keeps the existing S1–S4 and P1–P4 fields
- [ ] One authorization occurs before the new file is written
- [ ] No second bug directory or filename convention is used

---

## Case 2: Static evidence is insufficient to verify

**Fixture:** The suspected code pattern is absent, but no automated reproduction
or related test can be executed.

**Input:** `$bug-report verify BUG-0007`

**Assertions:**

- [ ] Verdict is CANNOT VERIFY, not VERIFIED FIXED
- [ ] Static search is described only as supporting evidence
- [ ] Top-level Status is not changed
- [ ] No new bug report is created

---

## Case 3: Successful verify enables close

**Fixture:** The documented automated reproduction executes without the bug and
related tests pass.

**Assertions:**

- [ ] The existing bug preview changes top-level Status to `Verified Fixed`
- [ ] Actual verification commands/results are appended
- [ ] One authorization updates that existing file
- [ ] A following Close run can satisfy its `Verified Fixed` precondition
- [ ] Verify terminates without entering Phase 3

---

## Case 4: Still present and close mode terminate cleanly

**Assertions:**

- [ ] STILL PRESENT keeps/sets Status `Open` and records observed failure
- [ ] CANNOT VERIFY never changes status
- [ ] Close requires `Verified Fixed`, previews the closure edit, then ends
- [ ] Neither mode creates or duplicates a report through Phase 3

---

## Protocol Compliance

- [ ] All writes are exact existing/new-file edits shown before one authorization
- [ ] VERIFIED FIXED requires executed reproduction plus passing related tests
- [ ] The status chain is Open → Verified Fixed → Closed
- [ ] No new workflow, state layer, schema, or identifier type is introduced
