# Gate Check — Required workflow continuation

This file contains required phases of `$gate-check`. Read it in full when the main `SKILL.md` reaches its Required continuation section, then execute the phases in order.

## 5. Output the Verdict

```
## Gate Check: [Current Phase] → [Target Phase]

**Date**: [date]
**Checked by**: gate-check skill

### Required Artifacts: [X/Y present]
- [x] design/gdd/game-concept.md — exists, 2.4KB
- [ ] docs/architecture/ — MISSING (no ADRs found)
- [x] production/sprints/ — exists, 1 sprint plan

### Quality Checks: [X/Y passing]
- [x] GDD has 8/8 required sections
- [ ] Tests — FAILED (3 failures in tests/unit/)
- [?] Core loop playtested — MANUAL CHECK NEEDED

### Blockers
1. **No Architecture Decision Records** — Run `$architecture-decision` to create one
   covering core system architecture before entering production.
2. **3 test failures** — Fix failing tests in tests/unit/ before advancing.

### Recommendations
- [Priority actions to resolve blockers]
- [Optional improvements that aren't blocking]

### Verdict: [PASS / CONCERNS / FAIL]
- **FAIL**: any blocking Required item is absent, any explicit auto-check fails,
  or any director returns NOT READY/REJECT
- **CONCERNS**: no blocker exists, but at least one Recommended item is absent
  or a confirmed non-blocking quality concern remains
- **PASS**: every blocking/quality check passes and no blocking manual item is
  unanswered. An unanswered blocking manual item cannot PASS.
```

---

## 5a. Chain-of-Verification

After drafting the verdict in Phase 5, challenge it before finalising. Reuse
manual answers already collected in Phase 4; do not ask the same question twice.
If the challenge discovers a new blocking manual question, ask it before the
final verdict. Until answered, the result cannot be PASS.

**Step 1 — Generate 5 challenge questions** designed to disprove the verdict:

> **Tool-action requirement**: At least 2 of the 5 challenge questions below must be answered by re-reading a specific file (file read) or re-running a specific check (Search tool) — not by reflection alone. Mark these with [TOOL ACTION] to indicate a tool was used.

For a **PASS** draft:
- "Which quality checks did I verify by actually reading a file, vs. inferring they passed?"
- "Are there MANUAL CHECK NEEDED items I marked PASS without user confirmation? [TOOL ACTION] Re-scan the checklist for any [?] or MANUAL CHECK items."
- "Did I confirm all listed artifacts have real content, not just empty headers? [TOOL ACTION] Re-read the file and check it has non-placeholder content."
- "Could any blocker I dismissed as minor actually prevent the phase from succeeding?"
- "Which single check am I least confident in, and why?"

For a **CONCERNS** draft:
- "Could any listed CONCERN be elevated to a blocker given the project's current state?"
- "Is the concern resolvable within the next phase, or does it compound over time?"
- "Did I soften any FAIL condition into a CONCERN to avoid a harder verdict?"
- "Are there artifacts I didn't check that could reveal additional blockers?"
- "Do all the CONCERNS together create a blocking problem even if each is minor alone?"

For a **FAIL** draft:
- "Have I accurately separated hard blockers from strong recommendations?"
- "Are there any PASS items I was too lenient about?"
- "Am I missing any additional blockers the user should know about?"
- "Can I provide a minimal path to PASS — the specific 3 things that must change?"
- "Is the fail condition resolvable, or does it indicate a deeper design problem?"

**Step 2 — Answer each question** independently.
Do NOT reference the draft verdict text — re-check specific files or use already
collected user evidence. Newly required manual evidence is gathered before the
verdict is finalized; unanswered items remain explicitly pending.

**Step 3 — Revise if needed:**
- If any answer reveals a missed blocker → upgrade verdict (PASS→CONCERNS or CONCERNS→FAIL)
- If any answer reveals an over-stated blocker → downgrade only if citing specific evidence
- If answers are consistent → confirm verdict unchanged

**Step 4 — Note the verification** in the final report output:
`Chain-of-Verification: [N] questions checked — verdict [unchanged | revised from X to Y]`

---

## 6. Update Stage on PASS

When the verdict is **PASS**, or **CONCERNS** and the user explicitly accepts
the listed non-blocking concerns, and the user confirms they want to advance:

1. Write the new stage name to `production/stage.txt` (single line, no trailing newline)
2. Subsequent `$studio-status` runs report the new stage from this file

Example: if passing the "Pre-Production → Production" gate, the approved change writes the single value `Production` to `production/stage.txt`.

**Use the single changeset approval policy**: Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.

---

## 7. Closing Next-Step Structured prompt

After the verdict is presented and any stage.txt update is complete, close with a structured next-step prompt by asking the user directly.

**Tailor the options to the gate that just ran:**

For **systems-design PASS**:
```
Gate passed. What would you like to do next?
[A] Run $create-architecture — produce your master architecture blueprint and ADR work plan (recommended next step)
[B] Design more GDDs first — return here when all MVP systems are complete
[C] Stop here for this session
```

> **Note for systems-design PASS**: `$create-architecture` is the required next step before writing any ADRs. It produces the master architecture document and a prioritized list of ADRs to write. Running `$architecture-decision` without this step means writing ADRs without a blueprint — skip it at your own risk.

For **technical-setup PASS**:
```
Gate passed. What would you like to do next?
[A] Run $create-control-manifest — generate the layer rules manifest from your Accepted ADRs (do this first)
[B] Run $vertical-slice — build the Vertical Slice (do this before writing epics — validate fun first)
[C] Write more ADRs first — run $architecture-decision [next-system]
[D] Stop here for this session
```

> **Note for technical-setup PASS**: The Pre-Production sequence is deliberately ordered
> to validate fun before committing to detailed planning:
>
> 1. `$create-control-manifest` — extract technical rules from Accepted ADRs (required before epics)
> 2. `$vertical-slice` — build the Vertical Slice **FIRST**, before writing epics or stories
> 3. Playtest → `$playtest-report analyze [path-to-completed-session-notes]` — at least 1 completed analyze report required to pass the Pre-Production gate; 3+ recommended before committing the full team
> 4. `$ux-design [screen]` — UX specs for main menu, core HUD, pause menu (if not done)
> 5. `$create-epics layer:foundation` then `$create-epics layer:core` — plan after fun is validated
> 6. `$create-stories [epic-slug]` for each epic
> 7. `$sprint-plan new`
>
> **Why prototype before epics?** If the prototype reveals the core loop needs to change,
> epics written before that discovery will be partially wrong. Validate fun cheaply first,
> then plan in detail. This is the #1 lesson from GDC postmortem data.

For all other gates, offer the two most logical next steps for that phase plus "Stop here".

---

## 8. Follow-Up Actions

Based on the verdict, suggest specific next steps:

- **No art bible?** → `$art-bible` to create the visual identity specification
- **Art bible exists but no asset specs?** → `$asset-spec system:[name]` to generate per-asset visual specs and generation prompts from approved GDDs
- **No game concept?** → `$brainstorm` to create one
- **No systems index?** → `$map-systems` to decompose the concept into systems
- **Missing design docs?** → `$reverse-document` or delegate to `game-designer`
- **Small design change needed?** → `$quick-design` for changes under ~4 hours (bypasses full GDD pipeline)
- **No UX specs?** → `$ux-design [screen name]` to author specs, or `$team-ui [feature]` for full pipeline
- **UX specs not reviewed?** → `$ux-review [file]` or `$ux-review all` to validate
- **No accessibility requirements doc?** → author `design/ux/accessibility-requirements.md` explicitly from the existing template in an authorized edit; `$ux-design` does not create it implicitly
- **No interaction pattern library?** → `$ux-design patterns` to initialize it
- **GDDs not cross-reviewed?** → `$review-all-gdds` (run after all MVP GDDs are individually approved)
- **Cross-GDD consistency issues?** → fix flagged GDDs, then re-run `$review-all-gdds`
- **No test framework?** → `$test-setup` to scaffold the framework for your engine
- **No QA plan for current sprint?** → `$qa-plan sprint` to generate one before implementation begins
- **Missing ADRs?** → `$architecture-decision` for individual decisions
- **No master architecture doc?** → `$create-architecture` for the full blueprint
- **ADRs missing engine compatibility sections?** → Re-run `$architecture-decision`
  or manually add Engine Compatibility sections to existing ADRs
- **Missing control manifest?** → `$create-control-manifest` (requires Accepted ADRs)
- **Missing epics?** → `$create-epics layer: foundation` then `$create-epics layer: core` (requires control manifest)
- **Missing stories for an epic?** → `$create-stories [epic-slug]` (run after each epic is created)
- **Stories not implementation-ready?** → `$story-readiness` to validate stories before developers pick them up
- **Tests failing?** → delegate to `lead-programmer` or `qa-tester`
- **No playtest data?** → `$playtest-report new` to create a template, then `$playtest-report analyze [path-to-completed-session-notes]` after the session
- **No playtest sessions beyond the minimum?** → Additional sessions give more reliable signal. 3+ total is recommended before committing the full team. Use `$playtest-report analyze [path-to-completed-session-notes]` to structure completed findings.
- **No Difficulty Curve doc?** → Create `design/difficulty-curve.md` from the template at `.codex/docs/templates/difficulty-curve.md` — or use `$quick-design "difficulty curve"` for a guided session.
- **No player journey map?** → Create `design/player-journey.md` from the template at `.codex/docs/templates/player-journey.md` — or author it collaboratively using `$ux-design` Phase 2b.
- **Need a quick sprint check?** → `$sprint-status` for current sprint progress snapshot
- **Performance unknown?** → `$perf-profile`
- **Not localized?** → `$localize scan` first; use the explicit locale-taking mode required by the resulting work
- **Ready for release?** → `$launch-checklist [YYYY-MM-DD]`; pass its exact persisted report path and canonical verdict back to this gate

---

## Collaborative Protocol

This skill follows the collaborative design principle:

1. **Scan first**: Check all artifacts and quality gates
2. **Ask about unknowns**: Don't assume PASS for things you can't verify
3. **Present findings**: Show the full checklist with status
4. **User decides within the verdict boundary**: concerns may be accepted, but a
   FAIL remains the current-stage result
5. **Get approval**: Add an eligible stage edit to the complete changeset preview; do not write it until that changeset is authorized.
6. **Never auto-fix**: If required artifacts are missing, report the FAIL verdict and
   name the skill to run (e.g. "run `$test-setup`"). Do NOT create missing files or
   re-run the gate automatically. Creating files to manufacture a PASS defeats the
   gate's purpose.

A FAIL, including any NOT READY/REJECT result or blocking artifact/manual item,
cannot be overridden into phase advancement and cannot write `stage.txt`.
The user may accept the risk while remaining in the current stage. CONCERNS may
be explicitly accepted and advanced as described above.
