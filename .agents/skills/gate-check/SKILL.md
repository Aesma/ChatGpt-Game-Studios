---
name: gate-check
description: "Validate readiness to advance between development phases. Produces a PASS/CONCERNS/FAIL verdict with specific blockers and required artifacts. Use when user says 'are we ready to move to X', 'can we advance to production', 'check if we can start the next phase', 'pass the gate'."
---

## Invocation and execution

Invoke this workflow as `$gate-check`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[source-phase: concept | systems-design | technical-setup | pre-production | production | polish] [--review full|lean|solo]`. Treat bracketed values as optional unless the workflow says otherwise.


# Phase Gate Validation

This skill validates whether the project is ready to advance to the next development
phase. It checks for required artifacts, quality standards, and blockers.

**Distinct from `$project-stage-detect`**: That skill is diagnostic ("where are we?").
This skill is prescriptive ("are we ready to advance?" with a formal verdict).

## Production Stages (7)

The project progresses through these stages:

1. **Concept** — Brainstorming, game concept document
2. **Systems Design** — Mapping systems, writing GDDs
3. **Technical Setup** — Engine config, architecture decisions
4. **Pre-Production** — Prototyping, vertical slice validation
5. **Production** — Feature development (Epic/Feature/Task tracking active)
6. **Polish** — Performance, playtesting, bug fixing
7. **Release** — Launch prep, certification

**When a gate passes**, write the new stage name to `production/stage.txt`
(single line, e.g. `Production`). This becomes the source of truth for subsequent `$studio-status` reports.

---

## 1. Parse Arguments

**Source phase:** the first provided argument names the current/source stage.
The six canonical mappings are: `concept` → Concept to Systems Design,
`systems-design` → Systems Design to Technical Setup, `technical-setup` →
Technical Setup to Pre-Production, `pre-production` → Pre-Production to
Production, `production` → Production to Polish, and `polish` → Polish to
Release. Unknown tokens are errors; do not infer aliases.

For every invocation, first read or infer the current stage and compare it with
the requested source phase. On mismatch, show both pieces of evidence and stop
without checking or writing the stage. A no-argument run detects the source
phase, then confirms it with the user.

Also resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `production/review-mode.txt` → use that value
3. Else → default to `lean`

Note: in `solo` mode, director spawns (CD-PHASE-GATE, TD-PHASE-GATE,
PR-PHASE-GATE, AD-PHASE-GATE) are skipped. All automatically verifiable
artifact and quality checks still run; solo is not existence-only. In `lean` mode, all four directors still run (phase gates are the purpose of lean mode).

- **With argument**: `$gate-check pre-production` — validate the
  Pre-Production to Production transition, after confirming the current stage is
  Pre-Production
- **No argument**: Auto-detect current stage using the existing
  `$project-stage-detect` artifact heuristics. Missing/invalid `stage.txt` with
  one unambiguous inferred stage may proceed to confirmation. If artifact
  signals conflict across stages, show them and ask the user to resolve the
  current stage; do not select the most advanced signal automatically. Then
  **confirm with the user before running**:

  Ask the user directly:
  - Prompt: "Detected stage: **[current stage]**. Running gate for [Current] → [Next] transition. Is this correct?"
  - Options:
    - `[A] Yes — run this gate`
    - `[B] No — pick a different gate` (if selected, show a second structured prompt listing all gate options: Concept → Systems Design, Systems Design → Technical Setup, Technical Setup → Pre-Production, Pre-Production → Production, Production → Polish, Polish → Release)

  Do not skip this confirmation step when no argument is provided.

---

## 2. Phase Gate Definitions

### Gate: Concept → Systems Design

**Required Artifacts:**
- [ ] `design/gdd/game-concept.md` exists and has content
- [ ] Game pillars defined (in concept doc or `design/gdd/game-pillars.md`)
- [ ] Visual Identity Anchor section exists in `design/gdd/game-concept.md` (from brainstorm Phase 4 art-director output)

**Recommended (not blocking):**
- [ ] Concept prototype exists in `prototypes/` with a REPORT.md showing PROCEED from an executed playable/interactive prototype; a Paper-mode or purely simulated log is not PROCEED evidence
      (`$prototype [core-mechanic]`) — skipping this means GDDs may be written for an
      idea that hasn't been played. Acceptable if the concept is proven by other means.

**Quality Checks:**
- [ ] Game concept directly contains a coherent core loop, target audience, and Visual Identity Anchor required by this gate
- [ ] Core loop is described and understood
- [ ] Target audience is identified
- [ ] Visual Identity Anchor contains a one-line visual rule and at least 2 supporting visual principles

---

### Gate: Systems Design → Technical Setup

**Required Artifacts:**
- [ ] Systems index exists at `design/gdd/systems-index.md` with at least MVP systems enumerated
- [ ] All MVP-tier GDDs exist with substantive eight-section content and their systems-index rows are `Approved`
- [ ] A cross-GDD review report exists in `design/gdd/` (from `$review-all-gdds`)

**Quality Checks:**
- [ ] Every MVP GDD has substantive Overview, Player Fantasy, Detailed Rules, Formulas, Edge Cases, Dependencies, Tuning Knobs, and Acceptance Criteria; each systems-index status is `Approved`
- [ ] `$review-all-gdds` verdict is not FAIL (cross-GDD consistency and design theory checks pass)
- [ ] All cross-GDD consistency issues flagged by `$review-all-gdds` are resolved or explicitly accepted
- [ ] System dependencies are mapped in the systems index and are bidirectionally consistent
- [ ] MVP priority tier is defined
- [ ] No stale GDD references flagged (older GDDs updated to reflect decisions made in later GDDs)

---

### Gate: Technical Setup → Pre-Production

**Required Artifacts:**
- [ ] Engine chosen (AGENTS.md Technology Stack is not `[CHOOSE]`)
- [ ] Technical preferences configured (`docs/technical-preferences.md` populated)
- [ ] Art bible exists at `design/art/art-bible.md` with at least Sections 1–4 (Visual Identity Foundation)
- [ ] At least 3 Architecture Decision Records in `docs/architecture/` covering
      Foundation-layer systems (scene management, event architecture, save/load)
- [ ] Engine reference docs exist in `docs/engine-reference/[engine]/`
- [ ] Test framework initialized: `tests/unit/` and `tests/integration/` directories exist
- [ ] CI/CD test workflow exists at `.github/workflows/tests.yml` (or equivalent)
- [ ] At least one example test file exists to confirm the framework is functional
- [ ] Master architecture document exists at `docs/architecture/architecture.md`
- [ ] Architecture traceability index exists at `docs/architecture/requirements-traceability.md`
- [ ] `$architecture-review` has been run (a review report file exists in `docs/architecture/`)
- [ ] `design/accessibility-requirements.md` exists with accessibility tier committed
- [ ] `design/ux/interaction-patterns.md` exists (pattern library initialized, even if minimal)

**Quality Checks:**
- [ ] Architecture decisions cover core systems (rendering, input, state management)
- [ ] Technical preferences have naming conventions and performance budgets set
- [ ] Accessibility tier is defined and documented (even "Basic" is acceptable — undefined is not)
- [ ] At least one screen's UX spec started (often the main menu or core HUD is designed during Technical Setup)
- [ ] All ADRs have an **Engine Compatibility section** with engine version stamped
- [ ] All ADRs have a **GDD Requirements Addressed section** with explicit GDD linkage
- [ ] No ADR references APIs listed in `docs/engine-reference/[engine]/deprecated-apis.md`
- [ ] All HIGH RISK engine domains (per VERSION.md) have been explicitly addressed
      in the architecture document or flagged as open questions
- [ ] Architecture traceability matrix has **zero Foundation layer gaps**
      (all Foundation requirements must have ADR coverage before Pre-Production)

**ADR Circular Dependency Check**: For all ADRs in `docs/architecture/`, read each ADR's
"ADR Dependencies" / "Depends On" section. Build a dependency graph (ADR-A → ADR-B means
A depends on B). If any cycle is detected (e.g. A→B→A, or A→B→C→A):
- Flag as **FAIL**: "Circular ADR dependency: [ADR-X] → [ADR-Y] → [ADR-X].
  Neither can reach Accepted while the cycle exists. Remove one 'Depends On' edge to
  break the cycle."

**Engine Validation** (read `docs/engine-reference/[engine]/VERSION.md` first):
- [ ] ADRs that touch post-cutoff engine APIs are flagged with Knowledge Risk: HIGH/MEDIUM
- [ ] `$architecture-review` engine audit shows no deprecated API usage
- [ ] All ADRs agree on the same engine version (no stale version references)

---

### Gate: Pre-Production → Production

**Required Artifacts:**
- [ ] First sprint plan exists in `production/sprints/`
- [ ] Art bible is complete (all 9 sections) and AD-ART-BIBLE sign-off verdict is recorded in `design/art/art-bible.md`
- [ ] All MVP-tier GDDs from systems index are complete
- [ ] Master architecture document exists at `docs/architecture/architecture.md`
- [ ] At least 3 ADRs covering Foundation-layer decisions exist in `docs/architecture/`
- [ ] All Foundation and Core layer ADRs have status `Accepted` (not `Proposed`) — stories cannot be unblocked until their governing ADR is accepted
- [ ] Control manifest exists at `docs/architecture/control-manifest.md`
      (generated by `$create-control-manifest` from Accepted ADRs)
- [ ] Epics defined in `production/epics/` with at least Foundation and Core
      layer epics present (use `$create-epics layer: foundation` and
      `$create-epics layer: core` to create them, then `$create-stories [epic-slug]`
      for each epic)
- [ ] UX specs exist for key screens: main menu, core gameplay HUD (at `design/ux/`), pause menu
- [ ] HUD design document exists at `design/ux/hud.md` (if game has in-game HUD)
- [ ] All key screen UX specs have passed `$ux-review` with verdict APPROVED; NEEDS REVISION cannot be accepted as implementation-ready

**Recommended (not blocking; missing items produce CONCERNS):**
- [ ] Vertical slice artifact exists and is playable, with REPORT.md; if built,
      its quality checks below cover playable-build validation without counting
      the artifact a second time
- [ ] At least one documented playtest session/report exists
- [ ] Entity inventory exists at `design/assets/entity-inventory.md`

**Quality Checks:**
- [ ] **Core loop fun is validated** — playtest data confirms the central mechanic is enjoyable, not just functional. Explicitly check the Vertical Slice playtest report.
- [ ] UX specs cover all UI Requirements sections from MVP-tier GDDs
- [ ] Interaction pattern library documents patterns used in key screens
- [ ] Accessibility tier from `design/ux/accessibility-requirements.md` is addressed in all key screen UX specs
- [ ] Sprint plan references real story file paths from `production/epics/`
      (not just GDDs — stories must embed GDD req ID + ADR reference)
- [ ] **Vertical Slice is COMPLETE**, not just scoped — the build demonstrates the full core loop end-to-end. At least one complete [start → challenge → resolution] cycle works.
- [ ] Architecture document has no unresolved open questions in Foundation or Core layers
- [ ] All ADRs have Engine Compatibility sections stamped with the engine version
- [ ] All ADRs have ADR Dependencies sections (even if all fields are "None")
- [ ] Manual validation confirms GDDs + architecture + epics are coherent
      (run `$review-all-gdds` and `$architecture-review` if not done recently)
- [ ] **Core fantasy is delivered** — at least one playtester independently described an experience that matches the Player Fantasy section of the core system GDDs (without being prompted).

**Vertical Slice Validation** (only run these checks if a Vertical Slice was built):
- [ ] A human has played through the core loop without developer guidance
- [ ] The game communicates what to do within the first 2 minutes of play
- [ ] No critical "fun blocker" bugs exist in the Vertical Slice build
- [ ] The core mechanic feels good to interact with (this is a subjective check — ask the user)

> **Verdict rules for Vertical Slice:**
> - **Slice was built AND any validation item is NO** → verdict is automatically FAIL. A broken
>   or unfun vertical slice should not advance to Production.
> - **Slice was not built (skipped)** → downgrade to CONCERNS only, not FAIL. Surface the risk
>   clearly: "Advancing without a validated Vertical Slice increases the risk of late-stage design
>   pivots. Recommended before committing full production scope." The user decides.
> - Skipping is a valid solo dev or time-constrained call. Shipping a broken one is not.

---

### Gate: Production → Polish

**Required Artifacts:**
- [ ] `src/` has active code organized into subsystems
- [ ] All core mechanics from GDD are implemented (cross-reference `design/gdd/` with `src/`)
- [ ] Main gameplay path is playable end-to-end
- [ ] Test files exist in `tests/unit/` and `tests/integration/` covering Logic and Integration stories
- [ ] All Logic stories from this sprint have corresponding unit test files in `tests/unit/`
- [ ] Smoke check has been run in base mode (not quick) with a PASS or PASS WITH WARNINGS verdict — report exists in `production/qa/` and records checked coverage
- [ ] QA sign-off report exists in `production/qa/` (generated by `$team-qa`) with verdict APPROVED or APPROVED WITH CONDITIONS
- [ ] At least 3 distinct completed playtest sessions are documented in `production/playtests/`; each must contain analyzed source notes/observations, not an empty `$playtest-report new` template
- [ ] Playtest reports cover: new player experience, mid-game systems, and difficulty curve
- [ ] Fun hypothesis from Game Concept has been explicitly validated or revised

**Recommended (not blocking):**
- [ ] At least one QA plan exists in `production/qa/` covering this production phase — run `$qa-plan` if missing (CONCERNS)

**Quality Checks:**
- [ ] Tests are passing (run test suite through the configured shell)
- [ ] No critical/blocker bugs in any bug tracker or known issues
- [ ] Core loop plays as designed (compare to GDD acceptance criteria)
- [ ] Performance is within an explicitly configured budget and supported by actual profiler measurements; a report without measurements or a project without configured targets cannot pass this item
- [ ] Playtest findings have been reviewed and critical fun issues addressed (not just documented)
- [ ] No "confusion loops" identified — no point in the game where >50% of playtesters got stuck without knowing why
- [ ] Difficulty curve matches the Difficulty Curve design doc (if one exists at `design/difficulty-curve.md`)
- [ ] All implemented screens have corresponding UX specs (no "designed in-code" screens)
- [ ] Interaction pattern library is up-to-date with all patterns used in implementation
- [ ] Accessibility compliance verified against committed tier in `design/accessibility-requirements.md`

---

### Gate: Polish → Release

**Required Artifacts:**
- [ ] All features from milestone plan are implemented
- [ ] Content is complete (all levels, assets, dialogue referenced in design docs exist)
- [ ] Localization strings are externalized (no hardcoded player-facing text in `src/`)
- [ ] QA test plan exists (`$qa-plan` output in `production/qa/`)
- [ ] QA sign-off report exists (`$team-qa` output — APPROVED or APPROVED WITH CONDITIONS)
- [ ] All Must Have story test evidence is present (Logic/Integration: test files pass; Visual/Feel/UI: sign-off docs in `production/qa/evidence/`)
- [ ] Smoke check passes cleanly (PASS verdict) on the release candidate build
- [ ] No test regressions from previous sprint (test suite passes fully)
- [ ] Balance data has been reviewed (`$balance-check` run)
- [ ] Consume the exact persisted `production/launch/launch-checklist-[date].md` path supplied by the launch-checklist run (or ask the user for the exact path); its body records canonical verdict `LAUNCH READY`. Never select by modification time. `LAUNCH BLOCKED` is FAIL, `CONCERNS` remains a gate concern, and dry-run/session-only output is not sign-off evidence
- [ ] Store metadata prepared (if applicable)
- [ ] Changelog / patch notes drafted

**Quality Checks:**
- [ ] Full QA pass signed off by `qa-lead`
- [ ] All tests passing
- [ ] Performance targets met across all target platforms
- [ ] No known critical, high, or medium-severity bugs
- [ ] Accessibility basics covered (remapping, text scaling if applicable)
- [ ] Localization verified for all target languages
- [ ] Legal requirements met (EULA, privacy policy, age ratings if applicable)
- [ ] Build compiles and packages cleanly

---

## 3. Run the Gate Check

**Before running artifact checks**, read `docs/consistency-failures.md` if it exists.
Extract entries whose Domain matches the target phase (e.g., if checking
Systems Design → Technical Setup, pull entries in Economy, Combat, or any GDD domain;
if checking Technical Setup → Pre-Production, pull entries in Architecture, Engine).
Carry these as context — recurring conflict patterns in the target domain warrant
increased scrutiny on those specific checks.

For each item in the target gate, evaluate applicability first. At the
Polish-to-Release gate, use existing target-platform, target-language, store,
and release-method evidence. Mark a check N/A only with that evidence and do not
count it missing or passing.

### Artifact Checks
- Search for matching files and read them to verify files exist and have meaningful content
- For reports/reviews, verify their existing scope, date/build/system linkage,
  and verdict cover this gate. A stale or unrelated file does not satisfy the
  artifact merely because its name matches.
- Don't just check existence — verify the file has real content (not just a template header)
- For code checks, verify directory structure and file counts

**Systems Design → Technical Setup gate — cross-GDD review check**:
Search files matching `design/gdd/gdd-cross-review-*.md` to find the
`$review-all-gdds` report.
If no file matches, mark the "cross-GDD review report exists" artifact as **FAIL** and
surface it prominently: "No `$review-all-gdds` report found in `design/gdd/`. Run
`$review-all-gdds` before advancing to Technical Setup."
If a file is found, read it and check the verdict line: a FAIL verdict means the
cross-GDD consistency check failed and must be resolved before advancing.

### Quality Checks
- For test checks: run the suite only when an explicit configured test command
  exists. No configured command is MANUAL/CONCERNS and cannot be inferred as a
  pass; an actual non-zero/failing run is FAIL.
- For design review checks: read the GDD and check for the 8 required sections
- For performance checks: read `docs/technical-preferences.md` and require both
  explicit configured budgets and actual profiler measurements in `tests/performance/`
  or a `$perf-profile` output that contains those measurements. Missing measurements
  or placeholder budgets are MANUAL CHECK NEEDED and cannot be reported as within budget.
- For localization checks: `Search` for hardcoded strings in `src/`

### Cross-Reference Checks
- Compare `design/gdd/` documents against `src/` implementations
- Check that every system referenced in architecture docs has corresponding code
- Verify sprint plans reference real work items

---

## 4. Collaborative Assessment

For items that can't be automatically verified, **ask the user**:

- "I can't automatically verify that the core loop plays well. Has it been playtested?"
- "No playtest report found. Has informal testing been done?"
- "Performance profiling data isn't available. Would you like to run `$perf-profile`?"

**Never assume PASS for unverifiable items.** Mark them as MANUAL CHECK NEEDED.

---

## 4b. Director Panel Assessment

**Apply review mode before spawning any director:**
- `solo` → skip all four directors. Note in output: "Director Panel skipped — Solo mode. Gate verdict based on artifact and quality checks only." Proceed to Phase 5.
- `lean` → spawn all four directors (phase gates always run in lean mode — this is their purpose).
- `full` → spawn all four directors as normal.

(Review mode was resolved in Phase 1. Use that stored value here.)

Before generating the final verdict, spawn all four directors as **parallel subagents** through Codex subagent delegation using the parallel gate protocol from `.codex/docs/director-gates.md`. Issue all four subagent delegations simultaneously — do not wait for one before starting the next.

**Spawn in parallel:**

1. **`creative-director`** — gate **CD-PHASE-GATE** (`.codex/docs/director-gates.md`)
2. **`technical-director`** — gate **TD-PHASE-GATE** (`.codex/docs/director-gates.md`)
3. **`producer`** — gate **PR-PHASE-GATE** (`.codex/docs/director-gates.md`)
4. **`art-director`** — gate **AD-PHASE-GATE** (`.codex/docs/director-gates.md`)

Pass to each: target phase name, list of artifacts present, and the context fields listed in that gate's definition.

**Collect all four responses, then present the Director Panel summary.** If any
required director fails, times out, or returns no valid verdict, list that gate
as unavailable. Do not fabricate READY. Use completed evidence to produce at
most CONCERNS when the missing panel result is non-blocking for the resolved
mode, or FAIL when readiness cannot be established; never PASS with an
incomplete required panel:

```
## Director Panel Assessment

Creative Director:  [READY / CONCERNS / NOT READY]
  [feedback]

Technical Director: [READY / CONCERNS / NOT READY]
  [feedback]

Producer:           [READY / CONCERNS / NOT READY]
  [feedback]

Art Director:       [READY / CONCERNS / NOT READY]
  [feedback]
```

**Apply to the verdict:**
- Any director returns NOT READY → verdict is FAIL and cannot advance the stage
- Any director returns CONCERNS → verdict is minimum CONCERNS
- All four READY → eligible for PASS (still subject to artifact and quality checks from Section 3)

---

## Required continuation

Before continuing, read [references/continued-workflow.md](references/continued-workflow.md) in full. It contains the remaining required phases, output formats, recovery rules, and handoff instructions; execute them in order.
