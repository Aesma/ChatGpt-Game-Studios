# Skill Test Spec: $bug-report

## Skill Summary

`$bug-report` creates a structured bug report document from a user description.
It produces a report with the following required fields: Title, Repro Steps,
Expected Behavior, Actual Behavior, Severity (CRITICAL/HIGH/MEDIUM/LOW), Affected
System(s), and Build/Version. If the user's initial description is missing any
required field, the skill asks follow-up questions to fill the gaps before
producing the draft.

The skill checks for possibly duplicate reports (by comparing to existing files
in `production/bugs/`) and offers to link rather than create a new report. Each
report is written to `production/bugs/bug-[date]-[slug].md` after a "May I apply the proposed changeset?"
6. File is written on approval; verdict is COMPLETE

**Assertions:**
- [ ] All 7 required fields are present in the report
- [ ] Severity is CRITICAL for a crash report
- [ ] Filename follows the `bug-[date]-[slug].md` convention
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts

**Assertions:**
- [ ] At least 3 follow-up questions are asked to fill missing fields
- [ ] Each required field is filled before the report is finalized
- [ ] Report is not written until all required fields are present
- [ ] Verdict is COMPLETE after all fields are filled and file is written

---

### Case 3: Possible Duplicate — Offers to link rather than create new

**Fixture:**
- `production/bugs/bug-2026-03-20-audio-cut-out.md` already exists with
  similar title and MEDIUM severity

**Input:** `$bug-report` (user describes: "Audio randomly stops working")

**Expected behavior:**
1. Skill scans existing reports and finds the similar audio bug
2. Skill reports: "A similar bug report exists: bug-2026-03-20-audio-cut-out.md"
3. Skill presents options: link as duplicate (add note to existing), create new anyway
4. If user chooses link: skill adds a cross-reference note to the existing file
   (asks "May I apply the proposed changeset?")
5. If user chooses create new: normal report creation proceeds

**Assertions:**
- [ ] Existing similar report is surfaced before creating a new one
- [ ] User is given the choice (not forced to link or create)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Verdict is COMPLETE when the report file is written

---

## Coverage Notes

- The case where the user provides a severity that seems too low for the
  described impact (e.g., LOW for a crash) is not tested; the skill may suggest
  a higher severity but ultimately respects user input.
- Build/version field is required but may be "unknown" if the user doesn't know —
  this is accepted as a valid value and not tested separately.
- Report slug generation (sanitizing the title into a filename) is an
  implementation detail not assertion-tested here.
