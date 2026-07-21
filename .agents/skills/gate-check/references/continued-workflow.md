# Gate Check — Required workflow continuation

This file contains required phases of `$gate-check`. Read it in full when the main `SKILL.md` reaches its Required continuation section, then execute the phases in order.

## 5. Output the Verdict

```
## Gate Check: [transition-id] — [Current Phase] → [Candidate Next Phase]

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
- **PASS**: Every blocking check passed
- **CONCERNS**: No blocking check failed, but one or more advisory risks remain
- **FAIL**: At least one blocking check failed; risk acceptance does not change this verdict
```

### Required immutable gate record

After Chain-of-Verification, emit this machine-readable record in the conversation.
Compute `record_id` as SHA-256 of canonicalized record content excluding
`record_id`. Any revision requires a new record ID.

```yaml
schema: cgs.gate-record/v1
record_id: sha256:<canonical-gate-record>
transition_id: <exact transition ID>
current_stage: <validated stage.txt value>
candidate_next_stage: <table-mapped stage>
generated_at: <ISO-8601 timestamp with timezone>
gate:
  tool: gate-check
  version: cgs.gate-check/p0-v1
checks:
  - check_id: <stable checklist ID>
    kind: <blocking|advisory>
    status: <PASS|FAIL|MANUAL_CHECK_NEEDED|UNBOUND|STALE|NOT_APPLICABLE>
    artifact_sha256: [<current artifact hashes>]
    evidence_record_ids: [<validated evidence IDs>]
    finding_ids: [<stable finding IDs>]
verdict: <PASS|CONCERNS|FAIL>
advancement_disposition: <ELIGIBLE|NOT_ELIGIBLE>
stage_mutated: false
```

The record MUST retain every UNBOUND or STALE finding and MUST say
`stage_mutated: false`. Do not save it to the repository.

---

## 5a. Chain-of-Verification

After drafting the verdict in Phase 5, challenge it before finalising.

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
Do NOT reference the draft verdict text — re-check specific files or ask the user.

**Step 3 — Revise if needed:**
- If any answer reveals a missed blocker → upgrade verdict (PASS→CONCERNS or CONCERNS→FAIL)
- If any answer reveals an over-stated blocker → downgrade only if citing specific evidence
- If answers are consistent → confirm verdict unchanged

**Step 4 — Note the verification** in the final report output:
`Chain-of-Verification: [N] questions checked — verdict [unchanged | revised from X to Y]`

---

## 6. Stop Without Updating Stage

`$gate-check` is read-only. PASS makes the gate record `ELIGIBLE`; it does not
authorize this skill to edit `production/stage.txt`. CONCERNS and FAIL remain
`NOT_ELIGIBLE` under the strict verdict.

If the user explicitly chooses to continue after CONCERNS or FAIL, keep the immutable
gate record unchanged and emit a separate request in the conversation:

```yaml
schema: cgs.advance-request/v1
transition_id: <exact transition ID>
gate_record_id: <cgs.gate-record/v1 record ID>
requested_disposition: PROCEED_WITH_ACCEPTED_RISK
operator: <explicit user identity, or user-unverified>
timestamp: <ISO-8601 timestamp with timezone>
accepted_risk_finding_ids: [<all explicitly accepted blocker/risk IDs>]
evidence_record_ids: [<evidence IDs from the gate record>]
```

This request does not advance the stage and must never relabel the gate as PASS. Only an
independent, explicitly authorized stage-advancement workflow may mutate stage state.
That workflow must compare-and-set the current stage against the transition origin,
validate the gate-record hash, preserve exact verdict and override fields, append
transition history, and perform an atomic update. If no such workflow is available, stop
after emitting the record/request and state that the project was not advanced.
---

## 7. Closing Next-Step Structured prompt

After the verdict and immutable gate record (and any accepted-risk request) are presented, close with a structured next-step prompt. Do not imply that the stage changed.

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
> 3. Playtest → `$playtest-report` — at least 1 session required to pass the Pre-Production gate; 3+ recommended before committing the full team
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
- **Bounded design change needed?** → run `$quick-design` only when its effort-independent structural-risk preflight says the change is eligible. Its output is a non-authoritative versioned proposal; an independent authorized application step must produce a current `APPLIED` receipt before downstream workflows may consume the changed canonical artifact.
- **No UX specs?** → `$ux-design [screen name]` to author specs, or `$team-ui [feature]` for full pipeline
- **UX specs not reviewed?** → `$ux-review [file]` or `$ux-review all` to validate
- **No accessibility requirements doc?** → stop the screen/HUD readiness path and
  request a separately authorized accessibility-foundation artifact from its
  owner; `$ux-design` must not create accessibility and pattern prerequisites as
  side effects of another artifact
- **No interaction pattern library?** → use a separate, one-artifact
  `$ux-design patterns ...` authoring task only under the UX-library owner; a
  screen/HUD author may create feature-local `UXP-*` proposals but not mutate
  the global library
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
- **No playtest data?** → `$playtest-report`
- **No playtest sessions beyond the minimum?** → Additional sessions give more reliable signal. 3+ total is recommended before committing the full team. Use `$playtest-report` to structure findings.
- **No Difficulty Curve doc?** → Create `design/difficulty-curve.md` through the owning design workflow from `.codex/docs/templates/difficulty-curve.md`. A `$quick-design` proposal may suggest a bounded edit only after its structural-risk preflight passes; it cannot create or replace the authoritative curve by itself.
- **No player journey map?** → create `design/player-journey.md` as a separate
  explicitly authorized artifact task; do not bundle it into a screen/HUD write
- **Need a quick sprint check?** → `$sprint-status` for current sprint progress snapshot
- **Performance unknown?** → `$perf-profile`
- **Not localized?** → `$localize`
- **Ready for release?** → `$launch-checklist`

---

## Collaborative Protocol

This skill follows the collaborative design principle:

1. **Scan first**: Check artifacts, quality gates, and hash-bound evidence.
2. **Ask about unknowns**: Do not assume PASS for unverifiable items.
3. **Present findings**: Show the checklist, strict verdict, and immutable gate record.
4. **User decides**: The user may accept identified risk, but that never changes the verdict.
5. **Remain read-only**: Never create or edit `stage.txt`, evidence, reports, or missing artifacts.
6. **Never auto-fix**: Report missing or stale evidence and name a possible next action;
   do not create files or re-run the gate to manufacture PASS.

Do not prevent a user from expressing an accepted-risk decision. Record that decision as
a separate `cgs.advance-request/v1`, explain that no stage mutation occurred, and stop.
