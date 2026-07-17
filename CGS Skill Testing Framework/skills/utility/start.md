# Skill Test Spec: $start

## Skill Summary

`$start` is the first-time onboarding skill for new projects. It guides the
user through naming the project, choosing a game engine, and setting up the
initial directory structure. It creates stub configuration files (AGENTS.md,
technical-preferences.md) and then routes to `$setup-engine` with the chosen
engine as an argument. Each file or directory created is gated behind a
"May I apply the proposed changeset?"
6. Skill creates all directories defined in `directory-structure.md`
7. Skill asks "May I apply the proposed changeset?" and writes it on approval
8. Skill routes to `$setup-engine [chosen-engine]` to complete technical config

**Assertions:**
- [ ] Project name is captured before any file is written
- [ ] Exactly 3 engine options are presented
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts

**Assertions:**
- [ ] Partial state is correctly identified (directories present, engine absent)
- [ ] User is offered resume vs. restart choice — not forced into one path
- [ ] Remains read-only; no authorization prompt appears because the workflow does not modify files
- [ ] Restart path asks for permission to overwrite before touching any files

---

### Case 5: Director Gate Check — No gate; start is a utility setup skill

**Fixture:**
- Any fixture

**Input:** `$start`

**Expected behavior:**
1. Skill completes full onboarding flow
2. No director agents are spawned at any point
3. No gate IDs (CD-*, TD-*, AD-*, PR-*) appear in the output

**Assertions:**
- [ ] No director gate is invoked during the skill execution
- [ ] No gate skip messages appear (gates are absent, not suppressed)
- [ ] Skill reaches COMPLETE without any gate verdict

---

## Protocol Compliance

- [ ] Asks for project name before any file is written
- [ ] Presents engine options as a structured choice (not free text)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Ends with a handoff to `$setup-engine` with the engine name as argument
- [ ] Verdict is clearly stated (COMPLETE or BLOCKED) at end of output

---

## Coverage Notes

- The case where the user rejects all engine options and provides a custom
  engine name is not tested — the skill is designed for the three supported
  engines only.
- Git initialization (if any) is not tested here; that is an infrastructure
  concern outside the skill boundary.
- Solo vs. lean mode behavior is not applicable — this skill has no gates and
  mode selection is irrelevant.
