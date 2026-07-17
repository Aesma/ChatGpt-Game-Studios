# Skill Test Spec: $story-done

## Skill Summary

`$story-done` closes the loop between design and implementation. Run at the
end of implementing a story, it reads the story file and verifies each
acceptance criterion against the implementation. It checks for GDD and ADR
deviations, prompts a code review, updates the story status to `Complete`,
logs any tech debt, and surfaces the next ready story from the sprint. It
produces a COMPLETE / COMPLETE WITH NOTES / BLOCKED verdict and writes to
the story file and optionally to `docs/tech-debt-register.md`.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥5 phase headings (complex skill warranting `context: fork` if applicable)
- [ ] Contains verdict keywords: COMPLETE, BLOCKED
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
10. If yes: skill updates the story file
11. Skill surfaces the next `Ready for Dev` story from the sprint

**Assertions:**
- [ ] Skill reads `docs/architecture/tr-registry.yaml` for TR-ID requirement text (not just story)
- [ ] Skill reads the referenced ADR file (not just the story reference)
- [ ] Each acceptance criterion is listed with VERIFIED / DEFERRED / FAILED status
- [ ] Skill prompts the user for code review outcome (does not skip this step)
- [ ] Verdict is COMPLETE when all criteria are verified and no deviations exist
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
4. If user says No: criterion is marked DEFERRED, verdict becomes COMPLETE WITH NOTES
5. Skill records the deferred criterion in completion notes
6. Asks "May I apply the proposed changeset?"

**Assertions:**
- [ ] Skill asks the user about unverifiable criteria rather than assuming PASS
- [ ] Deferred criteria result in COMPLETE WITH NOTES (not COMPLETE or BLOCKED)
- [ ] The deferred criterion is explicitly named in the completion notes
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts

---

### Case 3: Blocked Path — GDD deviation detected

**Fixture:**
- Story TR-ID points to requirement: "Player can carry max 3 light sources"
- Implementation in `src/` uses a variable `MAX_CARRIED_LIGHTS = 5`
- This is a deliberate deviation from the GDD

**Input:** `$story-done production/epics/core/story-light-pickup.md`

**Expected behavior:**
1. Skill reads the GDD requirement text (max 3)
2. Skill detects discrepancy between requirement and implementation value (5)
3. Skill flags this as a GDD deviation and asks the user to classify it:
   - INTENTIONAL: document the deviation and reason
   - ERROR: implementation must be fixed before story can be marked Complete
   - OUT OF SCOPE: requirement changed and GDD needs updating
4. If INTENTIONAL: skill records deviation in completion notes, verdict is COMPLETE WITH NOTES
5. If ERROR: verdict is BLOCKED until implementation is corrected

**Assertions:**
- [ ] Skill detects the mismatch between GDD requirement and implementation value
- [ ] Skill asks the user to classify the deviation (not auto-assumes either way)
- [ ] INTENTIONAL deviation → COMPLETE WITH NOTES (not BLOCKED)
- [ ] ERROR deviation → BLOCKED verdict until fixed
- [ ] Detected deviations are recorded in completion notes or tech debt register

---

### Case 4: Edge Case — No argument, auto-detect current story

**Fixture:**
- `production/session-state/active.md` contains a reference to
  `production/epics/core/story-oxygen-drain.md` as the active story
- That story file exists with `Status: In Progress`

**Input:** `$story-done` (no argument)

**Expected behavior:**
1. Skill reads `production/session-state/active.md`
2. Skill finds the active story reference
3. Skill reads that story file and proceeds normally
4. Output confirms which story was auto-detected

**Assertions:**
- [ ] Skill reads `production/session-state/active.md` when no argument is given
- [ ] Skill identifies and confirms the auto-detected story before proceeding
- [ ] If no story is found in session state, skill asks the user to provide a path

---

---

### Case 5: Director Gate — LP-CODE-REVIEW behavior across review modes

**Fixture:**
- Story file at `production/epics/core/story-light-pickup.md`
- All acceptance criteria verified, no GDD deviations
- `production/session-state/review-mode.txt` exists

**Case 5a — full mode:**
- `review-mode.txt` contains `full`

**Input:** `$story-done production/epics/core/story-light-pickup.md` (full mode)

**Expected behavior:**
1. Skill reads review mode — determines `full`
2. After implementation verification, skill invokes LP-CODE-REVIEW gate
3. Lead programmer reviews the implementation
4. If LP verdict is NEEDS CHANGES → story cannot be marked Complete
5. If LP verdict is APPROVED → skill proceeds to mark story Complete

**Assertions (5a):**
- [ ] Skill reads review mode before deciding whether to invoke LP-CODE-REVIEW
- [ ] LP-CODE-REVIEW gate is invoked in full mode after implementation check
- [ ] An LP NEEDS CHANGES verdict prevents story from being marked Complete
- [ ] Gate result is noted in output: "Gate: LP-CODE-REVIEW — [result]"
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts

**Case 5b — lean or solo mode:**
- `review-mode.txt` contains `lean` or `solo`

**Expected behavior:**
1. Skill reads review mode — determines `lean` or `solo`
2. LP-CODE-REVIEW gate is SKIPPED
3. Output notes the skip: "[LP-CODE-REVIEW] skipped — Lean/Solo mode"
4. Story completion proceeds based on acceptance criteria check only

**Assertions (5b):**
- [ ] LP-CODE-REVIEW gate does NOT spawn in lean or solo mode
- [ ] Skip is explicitly noted in output
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts

---

## Protocol Compliance

- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Presents complete findings (criteria check, deviation check) before asking approval
- [ ] Ends by surfacing the next ready story from the sprint plan
- [ ] Does not mark a story Complete if any criteria are in ERROR state
- [ ] Does not skip the code review prompt

---

## Coverage Notes

- The full 8-phase flow of the skill is exercised across Cases 1-3; not all
  edge cases within each phase are covered.
- Tech debt logging (deferred items written to `docs/tech-debt-register.md`)
  is mentioned in Case 2 but not the primary assertion focus; dedicated
  coverage deferred.
- The `sprint-status.yaml` update (Phase 7 in the skill) is implied by Case 1
  but not the primary assertion; assumed to follow the same "changeset authorization" pattern.
- Stories with multiple TR-IDs or multiple ADRs are not explicitly tested.
