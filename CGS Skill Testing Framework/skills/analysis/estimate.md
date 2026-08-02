# Skill Test Spec: $estimate

## Skill Summary

`$estimate` estimates task or story effort using a relative-size scale (S / M /
L / XL) based on story complexity, acceptance criteria count, and historical
sprint velocity from past sprint files. Estimates are advisory and are never
written automatically. No director gates are invoked. Verdicts are effort ranges,
not pass/fail — every run produces an estimate.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains size labels: S, M, L, XL (the "verdict" equivalents for this skill)
- [ ] Remains read-only; no authorization prompt appears because the workflow does not modify files
- [ ] Has a next-step handoff (how to use the estimate in sprint planning)

---

## Director Gate Checks

None. Estimation is an advisory informational skill; no gates are invoked.

---

## Test Cases

### Case 1: Happy Path — Clear story with known tech stack

**Fixture:**
- `production/epics/combat/story-hitbox-detection.md` exists with:
  - 4 clear Acceptance Criteria
  - ADR reference (Accepted status)
  - No "unknown" or "TBD" language in story body
- `production/sprints/sprint-003.md` through `sprint-005.md` exist with velocity data
- Tech stack is GDScript (well-understood by team per sprint history)

**Input:** `$estimate production/epics/combat/story-hitbox-detection.md`

**Expected behavior:**
1. Skill reads the story file — assesses clarity, AC count, tech stack
2. Skill reads sprint history to determine average velocity
3. Skill outputs estimate: M plus optimistic/expected/pessimistic days with reasoning
4. No files are written

**Assertions:**
- [ ] Estimate is M for a clear, well-scoped story with known tech
- [ ] Reasoning references AC count, tech stack familiarity, and velocity data
- [ ] Estimate is presented as a range (e.g., "1–2 days"), not a single point
- [ ] Output contains both the T-shirt size and monotonic three-point day estimates
- [ ] No files are written

---

### Case 2: High Uncertainty — Unknown system, no ADR yet

**Fixture:**
- `production/epics/online/story-lobby-matchmaking.md` exists with:
  - 2 vague Acceptance Criteria (using "should" and "TBD")
  - No ADR reference — matchmaking architecture not yet decided
  - References new subsystem ("online/matchmaking") with no existing source files

**Input:** `$estimate production/epics/online/story-lobby-matchmaking.md`

**Expected behavior:**
1. Skill reads story — finds vague AC, no ADR, no existing source
2. Skill flags multiple uncertainty factors
3. Estimate is L–XL with an explicit risk note: "Estimate range is wide due to architectural unknowns"
4. Skill recommends creating an ADR before development begins

**Assertions:**
- [ ] Estimate is L or XL (not S or M) when significant unknowns exist
- [ ] Risk note explains the specific unknowns driving the wide range
- [ ] Output recommends resolving architectural questions first
- [ ] No files are written

---

### Case 3: No Sprint Velocity Data — Conservative defaults used

**Fixture:**
- Story file exists and is well-defined
- `production/sprints/` is empty — no historical sprints

**Input:** `$estimate production/epics/core/story-save-load.md`

**Expected behavior:**
1. Skill reads story — assesses complexity
2. Skill attempts to read sprint velocity data — finds none
3. Skill notes: "No sprint history found — using conservative defaults for velocity"
4. Estimate uses the documented conservative S/M/L/XL day intervals without inventing a point-to-day conversion
5. No files are written

**Assertions:**
- [ ] Skill does not error when no sprint history exists
- [ ] Output explicitly notes that conservative defaults are being used
- [ ] Estimate is still produced (not blocked by missing velocity)
- [ ] Conservative defaults produce a higher (not lower) estimate range
- [ ] Confidence is lowered and no precise point conversion is claimed

---

### Case 4: Multiple Stories — Each estimated individually plus sprint total

**Fixture:**
- User provides a sprint file: `production/sprints/sprint-007.md` with 4 stories
- Sprint history exists (3 previous sprints)

**Input:** `$estimate production/sprints/sprint-007.md`

**Expected behavior:**
1. Skill reads sprint file — identifies 4 stories
2. Skill estimates each story individually: S, M, M, L
3. Skill computes a sprint aggregate day range from the resolved story ranges
4. Skill presents per-story estimates followed by sprint total
5. No files are written

**Assertions:**
- [ ] Each story receives its own estimate label
- [ ] Sprint total is presented after individual estimates
- [ ] Total is a sum range derived from individual ranges
- [ ] Missing or unresolvable story paths are listed as unestimated and excluded from numeric totals
- [ ] Skill handles sprint files (not just single story files) as input

---

### Case 5: Gate Compliance — No gate; estimates are informational

**Fixture:**
- Story file exists with medium complexity
- `review-mode.txt` contains `full`

**Input:** `$estimate production/epics/core/story-item-pickup.md`

**Expected behavior:**
1. Skill reads story and sprint history; computes estimate
2. No director gate is invoked in any review mode
3. Estimate is presented as advisory output only
4. Skill notes: "Use this estimate in $sprint-plan when selecting stories for the next sprint"

**Assertions:**
- [ ] No director gate is invoked regardless of review mode
- [ ] Output is purely informational — no approval or write prompt
- [ ] Next-step recommendation references `$sprint-plan`
- [ ] Estimate does not change based on review mode

---

### Case 6: Invalid path is not treated as prose

**Assertions:**
- [ ] A nonexistent path, directory, project-external path, or non-Markdown file produces a clear error
- [ ] The filename is not estimated as a natural-language task
- [ ] No partial estimate is fabricated from path text

---

### Case 7: Evidence boundaries and arithmetic

**Assertions:**
- [ ] Applicable nested AGENTS rules are read from root to candidate parent
- [ ] Candidate files come from explicit links/paths/references; unknown boundaries lower confidence
- [ ] LOC/dependency/cyclomatic values appear only when measured; otherwise complexity is qualitative
- [ ] Optimistic ≤ Expected ≤ Pessimistic and expected breakdown sums to recommended budget

---

### Case 8: Low-confidence and split guidance

**Assertions:**
- [ ] `$prototype` is recommended only for a core gameplay/fun hypothesis
- [ ] Architecture uncertainty points to an ADR; unclear requirements request clarification
- [ ] The >10-day split decision uses and cites Expected, not Pessimistic

---

## Protocol Compliance

- [ ] Reads story file before estimating
- [ ] Reads sprint velocity history when available
- [ ] Produces both S/M/L/XL and optimistic/expected/pessimistic day ranges
- [ ] Does not write any files
- [ ] No director gates are invoked
- [ ] Always produces an estimate (never blocked by missing data; uses defaults instead)

---

## Coverage Notes

- The skill does not produce PASS/FAIL verdicts; the "verdict" here is the
  effort range itself. Test assertions focus on the accuracy of the range
  and the quality of the reasoning, not a binary outcome.
- Team-specific velocity calibration (what "M" means for this team) is an
  implementation detail not tested here; it is configured via sprint history.
