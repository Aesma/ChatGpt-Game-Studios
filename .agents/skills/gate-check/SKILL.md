---
name: gate-check
description: "Validate readiness to advance between development phases. Produces a PASS/CONCERNS/FAIL verdict with specific blockers and required artifacts. Use when user says 'are we ready to move to X', 'can we advance to production', 'check if we can start the next phase', 'pass the gate'."
---

## Invocation and execution

Invoke this workflow as `$gate-check`.

`$gate-check` is a read-only assessment. It MUST NOT create, edit, or delete project
files, including `production/stage.txt`. It may ask questions and emit records in the
conversation, but only a separate, explicitly authorized stage-advancement workflow may
commit a transition.

Arguments: `[transition-id] [--review full|lean|solo]`, where `transition-id` is
exactly one of `concept-to-systems-design`,
`systems-design-to-technical-setup`, `technical-setup-to-pre-production`,
`pre-production-to-production`, `production-to-polish`, or
`polish-to-release`. The transition ID is optional only for selection from the
authoritative current stage. Phase-name shorthand and non-adjacent transitions are invalid.


# Phase Gate Validation

This skill validates whether the project is ready to advance to the next development
phase. It checks for required artifacts, quality standards, and blockers, produces a
strict verdict, then stops without changing project state.

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

`production/stage.txt` is the authoritative current-stage input. `$gate-check` may
read it, but MUST NOT write it, even after PASS or an accepted-risk decision.

---

## 1. Parse and Validate the Transition

Use this exact transition table:

| Transition ID | Required current stage | Candidate next stage |
|---|---|---|
| `concept-to-systems-design` | `Concept` | `Systems Design` |
| `systems-design-to-technical-setup` | `Systems Design` | `Technical Setup` |
| `technical-setup-to-pre-production` | `Technical Setup` | `Pre-Production` |
| `pre-production-to-production` | `Pre-Production` | `Production` |
| `production-to-polish` | `Production` | `Polish` |
| `polish-to-release` | `Polish` | `Release` |

Before artifact or quality checks:

1. Read `production/stage.txt` and trim surrounding whitespace only.
2. If it is missing, empty, or not exactly one of the seven stage names above, return
   `ERROR` and stop. Do not infer an authoritative stage from artifacts.
3. If an ID was supplied, require an exact table match and require the current stage to
   equal its `Required current stage`. Unknown IDs, phase-name shorthand, repeated or
   backward transitions, and mismatches return `ERROR` and stop.
4. With no ID, select the single row whose required stage matches. `Release` has no
   outgoing transition, so return `ERROR` and stop.

`ERROR` is an invocation/state-validation result, not a gate verdict. It emits no gate
record and never mutates project state.

Resolve review mode once for the run: explicit `--review full|lean|solo`, otherwise
`production/review-mode.txt`, otherwise `lean`. In `solo`, skip director spawns but
still run every artifact, quality, evidence-binding, and stale-evidence check.

- With an ID: `$gate-check pre-production-to-production` validates only that exact
  adjacent transition after current-stage validation.
- With no ID: show the mapped transition and ask for confirmation before checks. If
  rejected, stop and list the six exact IDs; another ID must still match current stage.

### Strict verdict and accepted-risk semantics

The verdict is a reproducible assessment, not a permission flag:

- `PASS`: every blocking check passed.
- `CONCERNS`: no blocking check failed, but advisory risks remain.
- `FAIL`: at least one blocking check failed.

A user decision never rewrites or downgrades the verdict. If the user explicitly elects
to continue after CONCERNS or FAIL, record `PROCEED_WITH_ACCEPTED_RISK` while
preserving the verdict and all blocker/finding IDs. This is an advance request in the
conversation only. A separate stage-advancement workflow must preserve gate record ID,
exact verdict, accepted risks, evidence IDs, timestamp, and operator identity in
transition history; accepted risk is never PASS.

### Hash-bound evidence for blocking checks

Any blocking item that depends on a review, approval, sign-off, test report, playtest
report, audit, or previously produced result is satisfied only by a current immutable
evidence record. Report existence, a historical verdict string, a statement inside the
reviewed artifact, or user recollection is not approval evidence.

Accepted evidence is a sidecar file or embedded fenced `gate-evidence` block:

```yaml
schema: cgs.review-evidence/v1
record_id: sha256:<canonical-record-payload>
artifact_id: <stable artifact or artifact-set identifier>
artifacts:
  - path: <repository-relative path>
    sha256: <lowercase SHA-256 of exact reviewed bytes>
reviewer: <person or delegated reviewer identity>
verdict: <producer verdict>
timestamp: <ISO-8601 timestamp with timezone>
finding_ids: [<stable finding IDs, possibly empty>]
producer:
  tool: <review, test, audit, or sign-off producer>
  version: <producer version or commit>
```

For an artifact set, list every in-scope path and hash; an aggregate-only hash is not
enough. Recompute every SHA-256 from current bytes. Missing fields or records are
`UNBOUND`; missing artifacts or hash mismatches are `STALE`. Either status fails a
blocking check and forces FAIL. Never fall back to an older glob, document-internal
sign-off, or structural completeness. Corrections require a new record ID and timestamp.
Hash binding proves only what exact bytes were evaluated; the checklist's verdict
threshold still applies.

### Canonical playtest-session evidence

When a check depends on playtest sessions, enumerate only distinct canonical
`production/playtests/<session-id>/report.md` files. A report counts only when:

- `<session-id>` is a valid unique stable ID and matches the report's `Session ID`;
- the report declares `Artifact Type: playtest-session-result`,
  `Status: COMPLETED`, and `Gate Eligible: YES`;
- build identity, tester/participant identity, start/end timestamps, answered
  observations, raw receipt, and SHA-256 fields are complete and non-placeholder;
- the referenced canonical manifest, observation ledger, and raw evidence exist,
  their current exact-byte hashes match the report, and every finding's
  Observation IDs resolve; and
- the report has not been superseded, duplicated under another path, or reused
  for a different build/evidence receipt.

Files under `_protocols/`, `raw/`, `reviews/`, ingest-only sessions, templates,
legacy/noncanonical paths, and malformed or hash-mismatched reports count as
zero sessions. A creative-director review never creates an additional session.
Record every accepted session ID, report path, current report hash, build, and
coverage purpose in the gate evidence.

### Regression-suite evidence

A regression check is satisfied only by both the current
`tests/regression-suite.md` selection manifest and a runner/CI receipt bound to
the exact current selection-manifest hash and target build. Revalidate the
selection manifest's QA-plan and source hashes, stable AC/BUG-to-test mappings,
test-source hashes, current failure-sensitivity receipts, quarantine state, and
active test IDs. Then verify the execution receipt contains the same selection
hash/build, every required active stable test ID, conclusive pass results, and
matching source/config/log hashes. `AWAITING RUN`, `STALE`, `INDETERMINATE`, a
missing sensitivity receipt, or the selection manifest alone cannot satisfy a
gate.

### Release-checklist collector evidence

`$release-checklist` is an evidence collector, not this gate's verdict owner.
Consume only an exact immutable collector report bound to the current release
manifest, release policy, build-candidate manifest, candidate/build/artifact
hashes, source commit, version, platform matrix, and complete item evidence.
Re-hash every referenced receipt and underlying artifact. Require stable item
IDs and one of `PASS(evidence)`, `FAIL(evidence)`, `UNKNOWN(owner)`, or a
policy-authorized `N/A(rationale)`.

`Gate Decision: NOT EVALUATED` is the only valid collector gate field. A HARD
item that is FAIL, UNKNOWN, STALE, UNAVAILABLE, partial, hash-mismatched, or has
an invalid N/A authority fails this gate. Advisory unresolved items produce
CONCERNS when no hard item fails. File existence, a checkbox, a model statement,
or merely running `$release-checklist`/`$launch-checklist` is never release
evidence. This workflow derives and owns the phase-gate verdict from the current
collector evidence.

### Localization evidence

Localization checks consume the exact current localization manifest and freeze
record, source-locale table/keyset/per-key hashes, each target locale table and
translation-review receipt, font/glyph/UI-fit artifacts, and the exact
candidate/build/platform receipt. Re-hash every dependency and require locale,
source, keyset, translation, font/asset, candidate, and build identities to
match. Source copies, MT drafts, placeholders, missing keys, unreviewed
translations, `QA PLAN READY`, filenames, or a localization-lead statement are
not passing evidence. Cultural, legal, rating, and market findings require the
authorized human owner receipt for the exact locale/scope. Any required locale
with UNKNOWN, STALE, PARTIAL, unverified, or mismatched evidence fails a blocking
localization check.
---

## 2. Phase Gate Definitions

### Gate: Concept → Systems Design

**Required Artifacts:**
- [ ] `design/gdd/game-concept.md` exists and has content
- [ ] Game pillars defined (in concept doc or `design/gdd/game-pillars.md`)
- [ ] Visual Identity Anchor section exists in `design/gdd/game-concept.md` (from brainstorm Phase 4 art-director output)

**Recommended (not blocking):**
- [ ] Concept prototype exists in `prototypes/` with a REPORT.md showing PROCEED verdict
      (`$prototype [core-mechanic]`) — skipping this means GDDs may be written for an
      idea that hasn't been played. Acceptable if the concept is proven by other means.

**Quality Checks:**
- [ ] Game concept has a current hash-bound `$design-review` evidence record whose verdict satisfies this gate
- [ ] Core loop is described and understood
- [ ] Target audience is identified
- [ ] Visual Identity Anchor contains a one-line visual rule and at least 2 supporting visual principles

---

### Gate: Systems Design → Technical Setup

**Required Artifacts:**
- [ ] Systems index exists at `design/gdd/systems-index.md` with at least MVP systems enumerated
- [ ] All MVP-tier GDDs exist and each has current hash-bound `$design-review` evidence satisfying this gate
- [ ] A current hash-bound `$review-all-gdds` evidence record covers the complete MVP GDD set

**Quality Checks:**
- [ ] Every MVP GDD's current hash-bound review verdict satisfies this gate; section count alone is insufficient
- [ ] The current hash-bound `$review-all-gdds` evidence verdict satisfies this gate
- [ ] All cross-GDD consistency issues flagged by `$review-all-gdds` are resolved or explicitly accepted
- [ ] System dependencies are mapped in the systems index and are bidirectionally consistent
- [ ] MVP priority tier is defined
- [ ] No stale GDD references flagged (older GDDs updated to reflect decisions made in later GDDs)

---

### Gate: Technical Setup → Pre-Production

**Required Artifacts:**
- [ ] Engine chosen (AGENTS.md Technology Stack is not `[CHOOSE]`)
- [ ] Technical preferences configured (`.codex/docs/technical-preferences.md` populated)
- [ ] Art bible exists at `design/art/art-bible.md` with at least Sections 1–4 (Visual Identity Foundation)
- [ ] At least 3 Architecture Decision Records in `docs/architecture/` covering
      Foundation-layer systems (scene management, event architecture, save/load)
- [ ] Engine reference docs exist in `docs/engine-reference/[engine]/`
- [ ] Test framework initialized: `tests/unit/` and `tests/integration/` directories exist
- [ ] CI/CD test workflow exists at `.github/workflows/tests.yml` (or equivalent)
- [ ] At least one example test file exists to confirm the framework is functional
- [ ] Master architecture document exists at `docs/architecture/architecture.md`
- [ ] Architecture traceability index exists at `docs/architecture/requirements-traceability.md`
- [ ] Current hash-bound `$architecture-review` evidence covers the architecture document, traceability index, and in-scope ADRs
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
- [ ] An explicitly supplied persisted `vertical-slice-evaluation-report` schema 1 is
      read-back verified and bound to its externally supplied report SHA-256. Re-hash
      its full plan/prerequisite/hypothesis/scope/evidence/source/tree/candidate/build/
      batch/playtest/velocity/decision graph. PASS requires `Workflow Status: COMPLETE`,
      all three verdict axes `PROCEED`, `Currentness: CURRENT`, `Gate Eligible: YES`,
      `Persistence: VERIFIED`, and no later source/build mutation. Filename, mtime,
      directory existence, or an unbound `REPORT.md` is zero evidence.
- [ ] First sprint plan exists in `production/sprints/`
- [ ] Art bible is complete (all 9 sections) and current hash-bound AD-ART-BIBLE evidence records an accepted verdict outside the reviewed artifact
- [ ] Entity inventory exists at `design/assets/entity-inventory.md` (recommended — run `$asset-spec` with no arguments to generate collaboratively from GDDs + art bible)
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
- [ ] The exact build artifact named and hashed by the eligible Vertical Slice report
      exists and matches its candidate/source/platform/configuration identity
- [ ] Vertical Slice has at least 1 distinct canonical completed playtest session
      that passes the validator above — **recommended, not blocking**; if absent,
      surface as CONCERNS
- [ ] The counted Vertical Slice report is exactly
      `production/playtests/<session-id>/report.md`; no equivalent/legacy path or
      template may satisfy this check
- [ ] UX specs exist for key screens: main menu, core gameplay HUD (at `design/ux/`), pause menu
- [ ] HUD design document exists at `design/ux/hud.md` (if game has in-game HUD)
- [ ] Every key screen UX spec has current hash-bound `$ux-review` evidence whose verdict satisfies this gate

**Quality Checks:**
- [ ] **Core loop fun is validated** — playtest data confirms the central mechanic is enjoyable, not just functional. Explicitly check the Vertical Slice playtest report.
- [ ] UX specs cover all UI Requirements sections from MVP-tier GDDs
- [ ] Interaction pattern library documents patterns used in key screens
- [ ] Accessibility tier from `design/accessibility-requirements.md` is addressed in all key screen UX specs
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
> - Any missing, PARTIAL, INCONCLUSIVE, PIVOT, KILL, BLOCKED, stale, unpersisted,
>   advisory-only, hash-mismatched, or later-mutated result is FAIL for this transition.
> - Creative/director concerns remain advisory and cannot upgrade evidence or override
>   the separately recorded product decision.
> - Only the exact current persisted PROCEED report described above can satisfy this
>   transition; skipping the slice does not become PASS or CONCERNS by policy shortcut.

---

### Gate: Production → Polish

**Required Artifacts:**
- [ ] `src/` has active code organized into subsystems
- [ ] All core mechanics from GDD are implemented (cross-reference `design/gdd/` with `src/`)
- [ ] Main gameplay path is playable end-to-end
- [ ] Test files exist in `tests/unit/` and `tests/integration/` covering Logic and Integration stories
- [ ] All Logic stories from this sprint have corresponding unit test files in `tests/unit/`
- [ ] Smoke check has been run with a PASS or PASS WITH WARNINGS verdict — report exists in `production/qa/`
- [ ] QA plan exists in `production/qa/` (generated by `$qa-plan`) covering this sprint or final production sprint
- [ ] At least one QA plan exists in `production/qa/` covering this production phase — run `$qa-plan` if missing (CONCERNS — advisory, not blocking)
- [ ] QA sign-off report exists in `production/qa/` (generated by `$team-qa`) with verdict APPROVED or APPROVED WITH CONDITIONS
- [ ] At least 3 distinct session IDs have canonical completed reports that each
      pass the playtest-session validator above
- [ ] Playtest reports cover: new player experience, mid-game systems, and difficulty curve
- [ ] Fun hypothesis from Game Concept has been explicitly validated or revised

**Quality Checks:**
- [ ] Regression selection and the exact build-bound runner receipt both pass
      the regression-suite evidence contract above; do not infer this from a
      manifest or command string alone
- [ ] No critical/blocker bugs in any bug tracker or known issues
- [ ] Core loop plays as designed (compare to GDD acceptance criteria)
- [ ] Performance is within budget (check technical-preferences.md targets)
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
- [ ] Localization source/keyset extraction is current and hash-bound; absence of
      a hardcoded-string search finding alone is not full localization evidence
- [ ] QA test plan exists (`$qa-plan` output in `production/qa/`)
- [ ] Exact persisted `$team-qa` report is bound to this candidate/build and
      current evidence index, with `Workflow Status: COMPLETE`, `QA Verdict:
      APPROVED`, `Gate Eligible: YES`, and verified hashes; APPROVED_WITH_CONDITIONS,
      NOT_APPROVED, INCOMPLETE, PARTIAL, stale, or unpersisted results do not pass
- [ ] All Must Have story test evidence is present (Logic/Integration: test files pass; Visual/Feel/UI: sign-off docs in `production/qa/evidence/`)
- [ ] Smoke check passes cleanly (PASS verdict) on the release candidate build
- [ ] No test regressions from previous sprint (test suite passes fully)
- [ ] Balance data has been reviewed (`$balance-check` run)
- [ ] The exact current `$release-checklist` collector report and release policy
      pass the collector-evidence contract above; running a checklist or launch
      workflow is insufficient
- [ ] Store metadata prepared (if applicable)
- [ ] Changelog / patch notes drafted

**Quality Checks:**
- [ ] Full QA pass signed off by `qa-lead`
- [ ] All tests passing
- [ ] Performance targets met across all target platforms
- [ ] No known critical, high, or medium-severity bugs
- [ ] Accessibility basics covered (remapping, text scaling if applicable)
- [ ] Every required target locale passes the localization-evidence contract
      above for the exact release candidate build
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

For each item in the target gate:

### Artifact Checks
- Search for matching files and read them to verify files exist and have meaningful content
- Don't just check existence — verify the file has real content (not just a template header)
- For code checks, verify directory structure and file counts

**Systems Design → Technical Setup gate — cross-GDD review check**:
Search `design/gdd/gdd-cross-review-*.md` and associated evidence records. Validate
the evidence schema, recompute the SHA-256 of every current MVP GDD in its artifact set,
and apply the required producer-verdict threshold. A report without bound evidence is
`UNBOUND`; a record whose manifest omits a current MVP GDD or has any hash mismatch is
`STALE`. Either is FAIL. Do not select a report merely because its filename is newest or
accept a verdict line copied from historical content.

### Quality Checks
- For test checks: Run the test suite through the configured shell if a test runner is configured
- For design review checks: read the GDD and check for the 8 required sections
- For performance checks: consume only an explicitly named, persisted and read-back
  verified `performance-runtime-report-v1` plus its exact versioned
  `performance-budget-v1` manifest. Recompute the report, input, normalized-data,
  budget, source/build, platform/hardware, scenario and required-matrix hashes.
  PASS requires `evidence_kind: RUNTIME_MEASUREMENT`, full required coverage,
  `gate_evidence_eligible: true`, `performance_targets_met: true`, and overall
  `Budget Verdict: WITHIN BUDGET`. A recent filename, prose target, static analysis,
  capture plan, conversation output, accepted risk, partial matrix, stale hash,
  `CONCERNS`, or `OVER BUDGET` is not performance PASS evidence.
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

**Collect all four responses, then present the Director Panel summary:**

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
- Any director returns NOT READY → verdict is minimum FAIL. Accepted risk may request advancement but MUST NOT change that FAIL verdict
- Any director returns CONCERNS → verdict is minimum CONCERNS
- All four READY → eligible for PASS (still subject to artifact and quality checks from Section 3)

---

## Required continuation

Before continuing, read [references/continued-workflow.md](references/continued-workflow.md) in full. It contains the remaining required phases, output formats, recovery rules, and handoff instructions; execute them in order.
