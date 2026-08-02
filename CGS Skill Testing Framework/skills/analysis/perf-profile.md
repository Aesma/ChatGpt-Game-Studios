# Skill Test Spec: $perf-profile

## Skill Summary

`$perf-profile` is a structured performance profiling workflow that identifies
bottlenecks and recommends optimizations. If profiler data or performance logs
are provided, it analyzes them directly. If not, it guides the user through a
manual profiling checklist. No director gates are invoked. The skill is read-only
and never persists a report or asks for changeset authorization.
Verdicts: WITHIN BUDGET, CONCERNS, or OVER BUDGET.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only the required `name` and non-empty `description`; `name` matches the skill directory
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: WITHIN BUDGET, CONCERNS, OVER BUDGET
- [ ] Remains read-only; no authorization prompt appears and no file is written

**Assertions:**
- [ ] Spike frames are identified by frame number
- [ ] Draw call count and budget are compared explicitly
- [ ] Verdict is CONCERNS when spikes exceed budget even if average is OK
- [ ] At least one specific optimization recommendation is given
- [ ] Every number comes from profiler input; static findings contain only file:line candidates and validation guidance

---

### Case 2: No Profiler Data — Manual checklist output

**Fixture:**
- User runs `$perf-profile` with no arguments
- No profiler data files exist in `production/qa/`

**Input:** `$perf-profile`

**Expected behavior:**
1. Skill finds no profiler data
2. Skill outputs a manual profiling checklist for the user to work through:
   - Enable Godot profiler or target engine's profiler
   - Record a 60-second play session
   - Export frame time data
   - Note any dropped frames or hitches
3. Skill asks user to provide data once collected before running analysis

**Assertions:**
- [ ] Skill does not crash or emit a verdict when no data is provided
- [ ] Manual profiling checklist is output (actionable steps, not just an error)
- [ ] No verdict is emitted (there is nothing to assess yet)
- [ ] No files are written

---

### Case 3: Over Budget — Frame budget exceeded for target platform

**Fixture:**
- Profiler data shows consistent 22ms frame times (target: 16.6ms for 60fps)
- All frames exceed budget; no single spike — systemic issue
- `technical-preferences.md` specifies target platform: PC, 60fps

**Input:** `$perf-profile production/qa/profiler-export-2026-03-20.json`

**Expected behavior:**
1. Skill reads profiler data and technical preferences for performance budget
2. All frames are over the 16.6ms budget
3. Verdict is OVER BUDGET
4. Skill outputs a prioritized optimization list (e.g., LOD system, shader complexity, physics tick rate)
5. Skill returns the measured report in the conversation without a write prompt

**Assertions:**
- [ ] Verdict is OVER BUDGET when all or most frames exceed budget
- [ ] Target frame budget is read from `technical-preferences.md` (not hardcoded)
- [ ] Optimization priority list is provided, not just the raw verdict
- [ ] No report file is written

---

### Case 4: Previous Perf Report Exists — Delta comparison

**Fixture:**
- `production/qa/perf-2026-03-28.md` exists with prior results (avg 15ms, max 19ms)
- New profiler export shows: avg 13ms, max 17ms
- Both reports are for the same scene

**Input:** `$perf-profile production/qa/profiler-export-2026-04-05.json`

**Expected behavior:**
1. Skill reads new profiler data
2. Skill detects prior report for the same scene
3. Skill computes deltas: avg improved 2ms, max improved 2ms
4. Skill presents regression check: no regressions detected
5. Verdict is WITHIN BUDGET; report notes improvement since last profile

**Assertions:**
- [ ] Skill checks `production/qa/` for prior comparable perf reports
- [ ] Delta comparison is shown (prior vs. current for key metrics)
- [ ] Verdict is WITHIN BUDGET when current metrics are within budget
- [ ] Improvement trend is noted positively in the report
- [ ] A prior report is compared only when platform, scene/scenario, and metric definitions match; otherwise the report states that no comparison is valid

---

### Case 5: Gate Compliance — No gate; performance-analyst delegation with fallback

**Fixture:**
- Profiler data shows CONCERNS-level findings (some spikes)
- `review-mode.txt` contains `full`

**Input:** `$perf-profile production/qa/profiler-export-2026-04-01.json`

**Expected behavior:**
1. Skill analyzes profiler data; verdict is CONCERNS
2. No director gate is invoked regardless of review mode
3. If the performance-analyst role is available, it performs the same read-only analysis; otherwise the current agent performs it and reports the fallback
4. Skill never suggests re-running itself merely to obtain the role
5. Skill returns the measured analysis in the conversation and writes nothing

**Assertions:**
- [ ] No director gate is invoked in any review mode
- [ ] Performance-analyst delegation is used when available, with an explicit current-agent fallback when unavailable
- [ ] Output does not suggest re-running `$perf-profile` to obtain that agent
- [ ] No authorization prompt appears and no file is written
- [ ] Verdict is CONCERNS for spike-based findings

---

## Protocol Compliance

- [ ] Reads profiler data when provided; outputs checklist when not
- [ ] Reads `technical-preferences.md` for target platform frame budget
- [ ] Checks for prior perf reports to enable delta comparison
- [ ] System scope resolves to existing code/scenes; full scope names covered platform/scenes and limitations
- [ ] Only the configured engine's patterns are applied; an unconfigured engine uses language-independent scanning
- [ ] Fix Effort is defined as relative S/M/L, and unmeasured Quick Wins never claim numeric gains
- [ ] Remains read-only in static and measured modes
- [ ] No director gates are invoked
- [ ] Verdict is one of: WITHIN BUDGET, CONCERNS, OVER BUDGET
- [ ] No budget verdict is emitted when profiler data is absent, unparsable, or the project budget is missing/placeholder

---

## Coverage Notes

- Platform-specific profiling workflows (console, mobile) are not tested here;
  the checklist output in Case 2 would be platform-specific in practice.
- The delta comparison in Case 4 assumes reports cover the same scene; cross-scene
  comparisons are not explicitly handled.
