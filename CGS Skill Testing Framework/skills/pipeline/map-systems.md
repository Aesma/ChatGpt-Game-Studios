# Skill Test Spec: $map-systems

## Skill Summary

`$map-systems` decomposes a game concept into a systems index. It reads the
approved game concept and pillars, enumerates both explicit and implicit systems,
maps dependencies between systems, assigns priority tiers (MVP / Vertical Slice /
Alpha / Full Vision), and organizes systems into a layered design order
(Foundation → Core → Feature → Presentation). The output is written to
`design/gdd/systems-index.md` after user approval.

This skill is required between game concept approval and per-system GDD creation
— it is a mandatory gate in the pipeline. In `full` review mode, TD-SYSTEM-BOUNDARY runs after dependency approval, PR-SCOPE after priority
approval, and CD-SYSTEMS after the authorized index draft, following their shared
gate trigger order. In `lean` or `solo` mode, both gates are
skipped. The skill writes to `design/gdd/systems-index.md`.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: COMPLETE, BLOCKED
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
6. Writes systems-index.md after approval
7. Updates `production/session-state/active.md`

**Assertions:**
- [ ] Between 5 and 8 systems are identified (not fewer, not more without explanation)
- [ ] Full-mode gates follow their shared trigger order; no TD/CD parallel assertion is made
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] systems-index.md is NOT written outside the authorized changeset
- [ ] Session state is updated after writing
- [ ] Verdict is COMPLETE
- [ ] PR-SCOPE handles REALISTIC, OPTIMISTIC, and UNREALISTIC exactly; it does not invent a CONCERNS branch
- [ ] The first complete changeset contains both `design/gdd/systems-index.md` and `production/session-state/active.md`
- [ ] CD-SYSTEMS REJECT leaves the index as a draft and cannot write an Approved/COMPLETE session state

---

### Case 2: Failure Path — No game concept found

**Fixture:**
- `design/gdd/game-concept.md` does NOT exist
- `design/gdd/` directory may be empty or absent

**Input:** `$map-systems`

**Expected behavior:**
1. Skill attempts to read `design/gdd/game-concept.md`
2. File not found
3. Skill outputs: "No game concept found. Run `$brainstorm` to create one, then return to `$map-systems`."
4. Skill exits without creating systems-index.md

**Assertions:**
- [ ] Skill outputs a clear error naming the missing file path
- [ ] Skill recommends `$brainstorm` as the next action
- [ ] No systems-index.md is created
- [ ] Verdict is BLOCKED

---

### Case 3: Director Gate — CD-SYSTEMS returns CONCERNS (missing core system)

**Fixture:**
- Game concept exists
- `production/review-mode.txt` contains `full`
- CD-SYSTEMS gate returns CONCERNS: "The [core-system] is implied by the concept but not identified"

**Input:** `$map-systems`

**Expected behavior:**
1. Systems are drafted (5-8 initial systems identified)
2. CD-SYSTEMS gate returns CONCERNS naming the missing core system
3. TD-SYSTEM-BOUNDARY returns APPROVED
4. Skill surfaces CD-SYSTEMS concerns to user
5. User is asked: revise systems list to add the missing system, or proceed as-is
6. If revised: updated systems list shown before "May I apply the proposed changeset?"
3. User chooses an action
4. Skill does NOT silently overwrite the existing index

**Assertions:**
- [ ] Skill detects and reads the existing systems-index.md before proceeding
- [ ] User is offered update/review options — not auto-overwritten
- [ ] Existing system count is presented to the user
- [ ] Skill does NOT proceed with a full re-decomposition without user choosing to do so

---

### Case 5: Director Gate — Lean mode and solo mode both skip gates, noted

**Fixture (lean mode):**
- Game concept exists
- `production/review-mode.txt` contains `lean`

**Lean mode expected behavior:**
1. Systems are decomposed and drafted
2. Both CD-SYSTEMS and TD-SYSTEM-BOUNDARY are skipped
3. Output notes: "CD-SYSTEMS skipped — lean mode" and "TD-SYSTEM-BOUNDARY skipped — lean mode"
4. "May I apply the proposed changeset?" asked before applying a not-yet-authorized changeset
- [ ] systems-index.md is NOT written outside the authorized changeset
- [ ] Full-mode TD-SYSTEM-BOUNDARY, PR-SCOPE, and CD-SYSTEMS follow their shared trigger order
- [ ] Skipped gates noted by name and mode in lean/solo output
- [ ] Ends with next-step handoff: `$design-system [next-system]`

---

## P1 Regression Assertions

- [ ] No-arg, next, and system-name are mutually exclusive; unknown flags/invalid review values are BLOCKED
- [ ] next/system-name requires one parseable canonical index and an exact system; failure never invokes design-system
- [ ] Existing-index choices route Update→Phase 2, Priorities→Phase 4, Design next→Phase 6; cancel/unknown stops
- [ ] Required full-mode gate timeout/unavailable/partial result stops downstream writing and never simulates a verdict
- [ ] PR-SCOPE receives unknown for missing timeline/team-size/complexity; no count×average estimate is invented
- [ ] Existing progress, design links, and manual notes survive index update; only new systems become Not Started
- [ ] map-systems reaches COMPLETE before any separately authorized design-system task and does not loop within one invocation
- [ ] Review mode fixture path is `production/review-mode.txt`; invalid values are reported before fallback

## Coverage Notes

- Circular dependency detection (System A depends on System B which depends on A)
  is part of the dependency mapping phase — not independently fixture-tested here.
- Priority tier assignment (MVP heuristics) is evaluated as part of the Case 1
  collaborative workflow rather than independently.
- The `next` argument mode (handing off the highest-priority undesigned system to
  `$design-system`) is not tested here — it is a post-index-creation convenience.
