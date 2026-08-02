# Skill Test Spec: $playtest-report

## Skill Summary

`$playtest-report` generates a structured playtest report from session notes or
user input. The report is organized into four sections: Feel/Accessibility,
Bugs Observed, Design Feedback, and Next Steps. When multiple testers participated,
the skill aggregates feedback and distinguishes majority opinions from minority
ones. The skill links to existing bug reports when a reported bug matches a file
in `production/qa/bugs/`.

Reports are written to `production/qa/playtest-[date].md` after a "May I apply the proposed changeset?"
7. Report is written on approval; verdict is COMPLETE

**Assertions:**
- [ ] All 4 sections are present in the report
- [ ] Bug is listed in the Bugs section (not the Design Feedback section)
- [ ] Next Steps are appropriate (bug report for crash, design review for feedback)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
3. User answers each prompt
4. Skill compiles report from answers and asks "May I apply the proposed changeset?" before applying a not-yet-authorized changeset
- [ ] Verdict is COMPLETE when report is written

---

## P0 Regression Assertions

- [ ] `new` creates only a blank template labelled `not a completed session`; it produces no findings, CD verdict, or playtest COMPLETE verdict
- [ ] Analyze mode requires a session hypothesis in Test Focus; missing hypothesis is requested and never invented
- [ ] Full analyze runs CD-PLAYTEST, lean/solo analyze skips it, and new mode never runs it
- [ ] Design feedback first identifies a proposed GDD edit; `$propagate-design-change` is suggested only after that GDD is actually revised

## P1 Regression Assertions

- [ ] Missing/unknown mode, analyze without one readable project-internal text path, and missing files are BLOCKED before gate/write
- [ ] Output uses `production/qa/playtest-[date].md`; same-day sessions require a session/build identifier or user choice and never silently overwrite
- [ ] Multi-tester analysis preserves each tester/session, reports explicit counts, and retains minority observations
- [ ] Existing bugs are linked only by a unique ID/description match; ambiguous matches remain candidates and non-reproducible findings remain observations
- [ ] Design cross-reference is limited to explicitly named systems/features/paths and their direct GDDs; unmapped intent is `unknown`
- [ ] Refused authorization reports `report not saved`; only a successfully written analyze report is COMPLETE, while new reports template generated/saved

## Coverage Notes

- CD-PLAYTEST is part of full analyze mode only; new mode and lean/solo analyze do
  not invoke it.
- Video recording or screenshot attachments are not tested; the report is a
  text-only document.
- The case where a tester's identity is unknown (anonymous feedback) follows
  the same aggregation pattern as Case 3 without tester labels.
