# Skill Test Spec: $brainstorm

## Skill Summary

`$brainstorm` facilitates guided game concept ideation. It presents 2-4 concept
options with pros/cons, lets the user choose and refine a concept, and produces
a structured `design/gdd/game-concept.md` document. The skill is collaborative —
it asks questions before proposing options and iterates until the user approves
a concept direction.

In `full` review mode, CD-PILLARS and AD-CONCEPT-VISUAL spawn in parallel after
pillars are formed. TD-FEASIBILITY runs after technical risks exist and before
scope tiers; PR-SCOPE runs after scope tiers. In `lean` mode,
all 4 inline gates are skipped (lean mode only runs PHASE-GATEs, and brainstorm
has none). In `solo` mode, all gates are skipped. The skill asks "May I apply the proposed changeset?"
8. Concept written after approval

**Assertions:**
- [ ] Exactly 3 concept options are presented (not 1, not 5+)
- [ ] CD-PILLARS and AD-CONCEPT-VISUAL spawn together; TD-FEASIBILITY and PR-SCOPE run later when their inputs exist
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Concept file is NOT written outside the authorized changeset
- [ ] Next-step handoff to `$map-systems` is present

---

### Case 2: Failure Path — CD-PILLARS returns REJECT

**Fixture:**
- Concept draft is complete
- `production/session-state/review-mode.txt` contains `full`
- CD-PILLARS gate returns REJECT: "The concept has no identifiable creative pillar"

**Input:** `$brainstorm`

**Expected behavior:**
1. CD-PILLARS gate returns REJECT with specific feedback
2. Skill surfaces the rejection to the user
3. Concept is NOT written to file
4. User is asked to rethink the concept direction or stop; no override-to-write is offered
5. If rethinking: skill returns to the concept options phase

**Assertions:**
- [ ] Concept is NOT written when CD-PILLARS returns REJECT
- [ ] Rejection feedback is shown to the user verbatim
- [ ] User is given revision or stop options, never an override-to-write option
- [ ] Skill returns to concept ideation phase if user chooses to rethink

---

### Case 3: Lean Mode — All 4 gates skipped; concept written after user confirms

**Fixture:**
- No existing game concept
- `production/session-state/review-mode.txt` contains `lean`

**Input:** `$brainstorm`

**Expected behavior:**
1. Concept options are presented and user selects one
2. Concept is elaborated into a structured draft
3. All 4 director gates are skipped — each noted: "[GATE-ID] skipped — lean mode"
4. Skill asks user to confirm the concept is ready to write
5. "May I apply the proposed changeset?" asked after confirmation
6. Concept written after approval

**Assertions:**
- [ ] All 4 gate skip notes appear: "CD-PILLARS skipped — lean mode", "AD-CONCEPT-VISUAL skipped — lean mode", "TD-FEASIBILITY skipped — lean mode", "PR-SCOPE skipped — lean mode"
- [ ] Concept is written after user confirmation only (no director approval needed in lean)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
5. Concept written after user approval

**Assertions:**
- [ ] All 4 skip notes appear with "solo mode" label
- [ ] No director agents are spawned
- [ ] Concept is written with only user approval
- [ ] Behavior is otherwise equivalent to lean mode for this skill

---

### Case 5: Director Gate — PR-SCOPE returns CONCERNS (scope too large)

**Fixture:**
- Concept draft is complete
- `production/session-state/review-mode.txt` contains `full`
- PR-SCOPE gate returns CONCERNS: "The concept scope would require 18+ months for a solo developer"

**Input:** `$brainstorm`

**Expected behavior:**
1. PR-SCOPE gate returns CONCERNS with specific scope feedback
2. Skill surfaces the scope concerns to the user
3. Scope concerns are documented in the concept draft before applying a not-yet-authorized changeset
4. User is asked: reduce scope, accept concerns and document them, or rethink
5. If concerns are accepted: concept is written with a "Scope Risk" note embedded

**Assertions:**
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Ends with next-step handoff: `$map-systems`

---

## Coverage Notes

- Existing `game-concept.md` enters resume mode: the skill inventories complete,
  placeholder, and missing sections, then changes only the user-selected scope.
  Completed ideation and unchanged gate results are reused rather than restarted.
- At the context threshold, the skill says the concept is saved only when the
  file was actually written; otherwise it explicitly says progress is conversation-only.

- AD-CONCEPT-VISUAL is paired only with CD-PILLARS; TD-FEASIBILITY and PR-SCOPE
  retain their dependency-ordered positions.
- The iterative concept refinement loop (user rejects all options, skill
  generates new ones) is not fixture-tested — it follows the same pattern as
  the option selection phase.
- The game-concept.md document structure (required sections) is defined in the
  skill body and not re-enumerated in test assertions.

## P1 Regression Assertions

- [ ] CD REJECT has no override-to-write path; revised pillars are re-reviewed
- [ ] CONCERNS/HIGH RISK/UNREALISTIC/OPTIMISTIC results require accept-risk, revise-and-re-review, or stop handling as applicable
- [ ] Every populated template field is sourced from the user/existing docs; unknown decisions are `Unknown` or `Open Question`
- [ ] No engine preference produces `Undecided`, never a recommendation
- [ ] Platform requirements are passed to setup-engine without hard-coded platform-to-engine claims
- [ ] Comparable titles and audience fit are labeled hypotheses unless a source was supplied
- [ ] Game concept is never sent to the system-GDD design-review workflow
