# Skill Test Spec: $gate-check

## Skill Summary

`$gate-check` validates whether the project is ready to advance to the next
development phase. It checks for required artifacts, runs quality checks, asks
the user about unverifiable items, and produces a PASS/CONCERNS/FAIL verdict.
On PASS with user confirmation, it writes the new stage name to
`production/stage.txt`. It governs all 6 phase transitions and is the most
critical gate-keeping skill in the pipeline.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings (numbered Phase N or ## sections)
- [ ] Contains verdict keywords: PASS, CONCERNS, FAIL
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts

**Assertions:**
- [ ] Skill verifies `design/gdd/game-concept.md` through repository inspection before marking it checked
- [ ] Output includes a "Required Artifacts" section with check status per item
- [ ] Output includes a "Quality Checks" section with check status per item
- [ ] Output includes a "Verdict" line with one of PASS / CONCERNS / FAIL
- [ ] Skill asks about unverifiable quality items (e.g., "Has this been reviewed?") rather than assuming PASS
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
5. Skill waits for user input before finalizing verdict

**Assertions:**
- [ ] Items that cannot be auto-verified are marked `[?] MANUAL CHECK NEEDED` rather than assumed PASS
- [ ] Skill uses a question to the user for at least one unverifiable quality item
- [ ] Skill does not mark unverifiable items as PASS by default

---

---

### Case 5: Director Gate — lean vs full vs solo mode

**Fixture:**
- `production/session-state/review-mode.txt` exists (or equivalent state file)
- All required artifacts for the target gate are present
- `design/gdd/game-concept.md` exists

**Case 5a — full mode:**
- `review-mode.txt` contains `full`

**Input:** `$gate-check systems-design` (with full mode active)

**Expected behavior:**
1. Skill reads review mode — determines `full`
2. Skill spawns all 4 PHASE-GATE director prompts in parallel:
   - CD-PHASE-GATE (creative-director)
   - TD-PHASE-GATE (technical-director)
   - PR-PHASE-GATE (producer)
   - AD-PHASE-GATE (art-director)
3. If one director returns CONCERNS → overall gate verdict is at minimum CONCERNS
4. All 4 verdicts are collected before producing final output

**Assertions (5a):**
- [ ] Skill reads review-mode before deciding which directors to spawn
- [ ] All 4 PHASE-GATE director prompts are spawned (not just 1 or 2)
- [ ] Directors are spawned in parallel (simultaneous, not sequential)
- [ ] A CONCERNS verdict from any one director propagates to overall verdict
- [ ] Verdict is NOT auto-PASS if any director returns CONCERNS or REJECT

**Case 5b — solo mode:**
- `review-mode.txt` contains `solo`

**Input:** `$gate-check systems-design` (with solo mode active)

**Expected behavior:**
1. Skill reads review mode — determines `solo`
2. Each director is noted as skipped: "[CD-PHASE-GATE] skipped — Solo mode"
3. Gate verdict is derived from artifact/quality checks only
4. No director gates spawn

**Assertions (5b):**
- [ ] No director gates are spawned in solo mode
- [ ] Each skipped gate is explicitly noted in output: "[GATE-ID] skipped — Solo mode"
- [ ] Verdict is based on artifact and quality checks only

**Note on Case 3 correction:**
The Case 3 assertions previously stated "Skill does not ask the user which gate to check
if current stage is determinable." This is correct. However, the skill DOES use
user-input request to confirm the auto-detected transition before running full checks —
this is a confirmation step, not a gate selection. Assertions for Case 3 should not
treat this confirmation as a failure.

---

## Protocol Compliance

- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Presents the full checklist and complete stage-file changeset before requesting authorization when the task has not already granted it
- [ ] Ends with a "Follow-Up Actions" section listing next steps per verdict
- [ ] Never advances the stage without explicit user confirmation
- [ ] Never auto-creates `production/stage.txt` if it doesn't exist without asking

---

## Coverage Notes

- The Production → Polish and Polish → Release gates are not covered here
  because they require complex multi-artifact setups (sprint plans, playtest
  data, QA sign-off); these are deferred to dedicated follow-up specs.
- The "CONCERNS" verdict path (minor gaps, not blocking) is not explicitly
  tested here; it falls between Case 1 and Case 2 and follows the same pattern.
- The Vertical Slice validation block (Pre-Production → Production gate) is not
  covered because it requires a playable build context that cannot be expressed
  as a document fixture.
