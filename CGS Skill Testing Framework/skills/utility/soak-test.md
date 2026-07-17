# Skill Test Spec: $soak-test

## Skill Summary

`$soak-test` generates a structured soak test protocol — an extended runtime
test plan designed to surface memory leaks, performance drift, and stability
issues that only appear under sustained gameplay. The skill produces a document
specifying the test duration, system under test, monitoring checkpoints (e.g.,
memory sample every 30 minutes), pass/fail thresholds, and conditions for early
termination.

The skill asks "May I apply the proposed changeset?" before
persisting. If a previous soak test for the same system exists, the skill offers
to extend the duration or add new conditions. No director gates apply. The verdict
is COMPLETE when the soak test protocol is written.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keyword: COMPLETE
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
5. File is written on approval; verdict is COMPLETE

**Assertions:**
- [ ] Protocol duration matches the requested 2 hours
- [ ] Monitoring checkpoints are at reasonable intervals (e.g., every 30 minutes)
- [ ] Network-specific checks are included (not just generic memory checks)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
3. After user responds with system: Skill asks: "What duration? (e.g., 1h, 4h, 8h)"
4. After user responds with duration: Skill asks for specific conditions or
   uses defaults (normal gameplay loop, default player count)
5. Skill generates protocol from collected inputs and asks "May I apply the proposed changeset?"
   (new file, not overwriting old one)

**Assertions:**
- [ ] Existing soak test is surfaced and referenced
- [ ] User is offered extend vs. new options
- [ ] New file is created (old file is not overwritten)
- [ ] Extended protocol includes both old and new checkpoints
- [ ] Verdict is COMPLETE

---

### Case 4: Mobile Target Platform — Memory-specific checkpoints added

**Fixture:**
- `technical-preferences.md` specifies target platform: Mobile
- User requests soak test for "gameplay session" at 30 minutes

**Input:** `$soak-test gameplay 30m`

**Expected behavior:**
1. Skill reads `technical-preferences.md` and detects mobile target platform
2. Soak test protocol includes mobile-specific memory checkpoints:
   - Check heap memory growth vs. device baseline
   - Check texture memory at checkpoint intervals
   - Add warning threshold at 300MB (mobile ceiling)
3. Protocol also includes thermal/battery drain advisory notes
4. Skill asks "May I apply the proposed changeset?" and writes on approval; verdict is COMPLETE

**Assertions:**
- [ ] Mobile platform is detected from technical-preferences.md
- [ ] Memory checkpoints include mobile-appropriate thresholds (not desktop)
- [ ] Thermal/battery notes are present in the protocol
- [ ] Verdict is COMPLETE

---

### Case 5: Director Gate Check — No gate; soak-test is a planning utility

**Fixture:**
- Valid system and duration provided

**Input:** `$soak-test combat 1h`

**Expected behavior:**
1. Skill generates and writes the soak test protocol
2. No director agents are spawned
3. No gate IDs appear in output

**Assertions:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Skill reaches COMPLETE without any gate check

---

## Protocol Compliance

- [ ] Collects system, duration, and conditions before generating protocol
- [ ] Includes monitoring checkpoints at regular intervals
- [ ] Includes pass/fail thresholds and early termination conditions
- [ ] Adapts checkpoints to target platform (mobile vs. desktop)
- [ ] Uses existing bounded task authorization, or previews and confirms the complete changeset once before the first write; no per-file or per-section re-prompts
- [ ] Verdict is COMPLETE when file is written

---

## Coverage Notes

- Soak tests for specific engine subsystems (rendering pipeline, physics
  simulation) follow the same protocol structure and are not separately tested.
- The case where the user provides a duration shorter than the minimum useful
  soak period (e.g., 5 minutes) is not tested; the skill would note this is
  too short for meaningful results.
- Automated execution of the soak test protocol is outside this skill's scope —
  this skill generates the plan, not the runner.
