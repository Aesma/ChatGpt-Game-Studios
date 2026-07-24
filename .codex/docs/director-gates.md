# Director Gates — Shared Review Pattern

This document is a registry of advisory director/lead review prompts. A consumer may use a gate only when its own contract explicitly names the gate, inputs, evidence identity, verdict handling, and supported review modes. Merely referencing this file does not add a CLI flag, spawn authority, write authority, or phase-transition authority.

**Scope**: opt-in consumers only. Required QA, accessibility, security, separation-of-duties, evidence validation, and canonical recorder roles are outside review-mode skipping and remain mandatory.

---

## How to Use This Document

In any skill, replace an inline director prompt with a reference:

```
Spawn `creative-director` through Codex subagent delegation using gate **CD-PILLARS** from
`.codex/docs/director-gates.md`.
```

Pass the context listed under that gate's **Context to pass** field, then handle
the verdict using the **Verdict handling** rules below.

---

## Review-mode contract

Review mode is a consumer capability, not a universal feature. A skill that does not explicitly implement the complete contract below MUST reject or ignore review-mode syntax according to its own interface and MUST NOT claim that a mode changed execution.

The optional configuration record is `production/review-mode.txt` with exactly one value: `full`, `lean`, or `solo`. A consumer may read it only if its own SKILL contract declares review-mode support. A per-run `--review` argument exists only when that consumer declares it.

| Consumer | Gate | `full` | `lean` | `solo` |
|---|---|---:|---:|---:|
| `gate-check` | CD/TD/PR/AD-PHASE-GATE | run all four | run all four | do not run; director-gate contribution is `N/A` |
| `sprint-plan` | PR-SPRINT | run | skip | skip |
| `story-readiness` | QL-STORY-READY | run | skip | skip |
| `milestone-review` | PR-MILESTONE | run | skip | skip |

No other consumer inherits those mappings. In particular, a team orchestrator cannot expose an inert mode parameter merely because it uses this document.

When a declared consumer resolves a mode it records the source (explicit argument or exact configuration path/hash), resolved value, applicable gate IDs, and run/skip disposition. Missing configuration uses the consumer's declared default; there is no repository-wide implied default.

Mode affects only the advisory director/lead gate listed by the consumer. It MUST NOT skip canonical readiness checks, independent QA, accessibility, security, test evidence, source-hash/currentness validation, non-waivable blockers, required role separation, or recorder receipts. A skipped advisory gate is `N/A`, never APPROVE/READY and never proof of completion.

---

## Invocation contract

Before delegation, the consumer freezes an input manifest containing gate ID, reviewer role, exact artifact paths and raw SHA-256 values, transitive evidence hashes, catalog/config hashes when applicable, and expected verdict vocabulary. Delegation is read-only. The reviewer may not edit the reviewed artifact or persist the authoritative gate record.

For multiple applicable gates, delegation may be parallel, but all results must be collected before aggregation. Each result is bound to the frozen manifest and reviewer identity. A separate authorized recorder, when required by the consumer, persists unchanged result bytes plus its raw hash and emits the consumer-declared receipt. No gate is auto-executed and no result advances project stage.

---

## Standard Verdict Format

All gates return one of three verdicts. Skills must handle all three:

| Verdict | Meaning | Default action |
|---------|---------|----------------|
| **APPROVE / READY** | No issues. Proceed. | Continue the workflow |
| **CONCERNS [list]** | Issues present but not blocking. | Surface to user via `user-input request` — options: `Revise flagged items` / `Accept and proceed` / `Discuss further` |
| **REJECT / NOT READY [blockers]** | Blocking issues. Do not proceed. | Surface blockers to user. Do not write files or advance stage until resolved. |

**Escalation rule**: When multiple directors are spawned in parallel, apply the
strictest verdict — one NOT READY overrides all READY verdicts.

---

## Recording Gate Outcomes

A Markdown status line is informative only. When a consumer requires durable evidence, an independently authorized recorder persists the exact review result and a typed receipt bound to gate ID, reviewer identity, input-manifest hash, reviewed artifact hashes, verdict, findings, timestamp, and supersession chain. Stale, malformed, self-authored, or hash-mismatched results are invalid. Only the project-stage authority recorder can advance stage after a current eligible gate record.

---

## Tier 1 — Creative Director Gates

Agent: `creative-director` | Role complexity: high-complexity | Domain: Vision, pillars, player experience

---

### CD-PILLARS — Pillar Stress Test

**Trigger**: After game pillars and anti-pillars are defined (brainstorm Phase 4,
or any time pillars are revised)

**Context to pass**:
- Full pillar set with names, definitions, and design tests
- Anti-pillars list
- Core fantasy statement
- Unique hook ("Like X, AND ALSO Y")

**Prompt**:
> "Review these game pillars. Are they falsifiable — could a real design decision
> actually fail this pillar? Do they create meaningful tension with each other? Do
> they differentiate this game from its closest comparables? Would they help resolve
> a design disagreement in practice, or are they too vague to be useful? Return
> specific feedback for each pillar and an overall verdict: APPROVE (strong), CONCERNS
> [list] (needs sharpening), or REJECT (weak — pillars do not carry weight)."

**Verdicts**: APPROVE / CONCERNS / REJECT

---

### CD-GDD-ALIGN — GDD Pillar Alignment Check

**Trigger**: After a system GDD is authored by its owning design workflow. A
`quick-design` proposal does not trigger this gate; only the resulting canonical
artifact after a separately authorized application with a current `APPLIED` receipt
is eligible.

**Context to pass**:
- GDD file path
- Game pillars (from `design/gdd/game-concept.md` or `design/gdd/game-pillars.md`)
- MDA aesthetics target for this game
- System's stated Player Fantasy section

**Prompt**:
> "Review this system GDD for pillar alignment. Does every section serve the stated
> pillars? Are there mechanics or rules that contradict or weaken a pillar? Does
> the Player Fantasy section match the game's core fantasy? Return APPROVE, CONCERNS
> [specific sections with issues], or REJECT [pillar violations that must be
> redesigned before this system is implementable]."

**Verdicts**: APPROVE / CONCERNS / REJECT

---

### CD-SYSTEMS — Systems Decomposition Vision Check

**Trigger**: At `$map-systems`' single pre-write checkpoint, after the complete
canonical index candidate is frozen and SHA-256-bound but before any authoritative
index/state write — validates the complete system set before GDD authoring begins

**Context to pass**:
- Complete proposed systems-index bytes, destination path
  (`design/gdd/systems-index.md`), and candidate SHA-256
- Game pillars and core fantasy (from `design/gdd/game-concept.md`)
- Priority tier assignments (MVP / Vertical Slice / Alpha / Full Vision)
- Any high-risk or bottleneck systems identified in the dependency map

**Prompt**:
> "Read-only review: do not edit the candidate or any file. Bind the response to
> the supplied candidate SHA-256. Review this systems decomposition against the game's design pillars. Does the
> full set of MVP-tier systems collectively deliver the core fantasy? Are there
> systems whose mechanics don't serve any stated pillar — indicating they may be
> scope creep? Are there pillar-critical player experiences that have no system
> assigned to deliver them? Are any systems missing that the core loop requires?
> Return APPROVE (systems serve the vision), CONCERNS [specific gaps or
> misalignments with their pillar implications], or REJECT [fundamental gaps —
> the decomposition misses critical design intent and must be revised before GDD
> authoring begins]."

**Verdicts**: APPROVE / CONCERNS / REJECT

---

### CD-NARRATIVE — Narrative Consistency Check

**Trigger**: After narrative GDDs, lore documents, dialogue specs, or world-building
documents are authored (team-narrative, design-system for story systems, writer
deliverables)

**Context to pass**:
- Document file path(s)
- Game pillars
- Narrative direction brief or tone guide (if exists at `design/narrative/`)
- Any existing lore that the new document references

**Prompt**:
> "Review this narrative content for consistency with the game's pillars and
> established world rules. Does the tone match the game's established voice? Are
> there contradictions with existing lore or world-building? Does the content serve
> the player experience pillar? Return APPROVE, CONCERNS [specific inconsistencies],
> or REJECT [contradictions that break world coherence]."

**Verdicts**: APPROVE / CONCERNS / REJECT

---

### CD-PLAYTEST — Player Experience Validation

**Trigger**: After playtest reports are generated (`$playtest-report`), or after
any session that produces player feedback

**Context to pass**:
- Playtest report file path
- Game pillars and core fantasy statement
- The specific hypothesis being tested

**Prompt**:
> "Review this playtest report against the game's design pillars and core fantasy.
> Is the player experience matching the intended fantasy? Are there systematic issues
> that represent pillar drift — mechanics that feel fine in isolation but undermine
> the intended experience? Return APPROVE (core fantasy is landing), CONCERNS [gaps
> between intended and actual experience], or REJECT [core fantasy is not present —
> redesign needed before further playtesting]."

**Verdicts**: APPROVE / CONCERNS / REJECT

---

### CD-PHASE-GATE — Creative Readiness at Phase Transition

**Trigger**: At `$gate-check` in `full` or `lean`; skip with advisory contribution `N/A` in `solo`. Run in parallel with the other applicable phase gates.

**Context to pass**:
- Target phase name
- List of all artifacts present (file paths)
- Game pillars and core fantasy

**Prompt**:
> "Review the current project state for [target phase] gate readiness from a
> creative direction perspective. Are the game pillars faithfully represented in
> all design artifacts? Does the current state preserve the core fantasy? Are there
> any design decisions across GDDs or architecture that compromise the intended
> player experience? Return READY, CONCERNS [list], or NOT READY [blockers]."

**Verdicts**: READY / CONCERNS / NOT READY

---

## Tier 1 — Technical Director Gates

Agent: `technical-director` | Role complexity: high-complexity | Domain: Architecture, engine risk, performance

---

### TD-SYSTEM-BOUNDARY — System Boundary Architecture Review

**Trigger**: After `$map-systems` Phase 3 dependency mapping is agreed but before
GDD authoring begins — validates that the system structure is architecturally
sound before teams invest in writing GDDs against it

**Context to pass**:
- Systems index path (or the dependency map summary if index not yet written)
- Layer assignments (Foundation / Core / Feature / Presentation / Polish)
- The full dependency graph (what each system depends on)
- Any bottleneck systems flagged (many dependents)
- Any circular dependencies found and their proposed resolutions

**Prompt**:
> "Review this systems decomposition from an architectural perspective before GDD
> authoring begins. Are the system boundaries clean — does each system own a
> distinct concern with minimal overlap? Are there God Object risks (systems doing
> too much)? Does the dependency ordering create implementation-sequencing problems?
> Are there implicit shared-state problems in the proposed boundaries that will
> cause tight coupling when implemented? Are any Foundation-layer systems actually
> dependent on Feature-layer systems (inverted dependency)? Return APPROVE
> (boundaries are architecturally sound — proceed to GDD authoring), CONCERNS
> [specific boundary issues to address in the GDDs themselves], or REJECT
> [fundamental boundary problems — the system structure will cause architectural
> issues and must be restructured before any GDD is written]."

**Verdicts**: APPROVE / CONCERNS / REJECT

---

### TD-FEASIBILITY — Technical Feasibility Assessment

**Trigger**: After the biggest technical risks are recorded in an authoritative
scope/feasibility artifact (brainstorm Phase 6 or another owning workflow). A
`quick-design` proposal alone is not technical-feasibility evidence.

**Context to pass**:
- Concept's core loop description
- Platform target
- Engine choice (or "undecided")
- List of identified technical risks

**Prompt**:
> "Review these technical risks for a [genre] game targeting [platform] using
> [engine or 'undecided engine']. Flag any HIGH risk items that could invalidate
> the concept as described, any risks that are engine-specific and should influence
> the engine choice, and any risks that are commonly underestimated by solo
> developers. Return VIABLE (risks are manageable), CONCERNS [list with mitigation
> suggestions], or HIGH RISK [blockers that require concept or scope revision]."

**Verdicts**: VIABLE / CONCERNS / HIGH RISK

---

### TD-ARCHITECTURE — Architecture Sign-Off

**Trigger**: After the master architecture document is drafted (`$create-architecture`
Phase 7), and after any major architecture revision

**Context to pass**:
- Architecture document path (`docs/architecture/architecture.md`)
- Technical requirements baseline (TR-IDs and count)
- ADR list with statuses
- Engine knowledge gap inventory

**Prompt**:
> "Review this master architecture document for technical soundness. Check: (1) Is
> every technical requirement from the baseline covered by an architectural decision?
> (2) Are all HIGH risk engine domains explicitly addressed or flagged as open
> questions? (3) Are the API boundaries clean, minimal, and implementable? (4) Are
> Foundation layer ADR gaps resolved before implementation begins? Return APPROVE,
> CONCERNS [list], or REJECT [blockers that must be resolved before coding starts]."

**Verdicts**: APPROVE / CONCERNS / REJECT

---

### TD-ADR — Architecture Decision Review

**Trigger**: After an individual ADR is authored (`$architecture-decision`), before
it is marked Accepted

**Context to pass**:
- ADR file path
- Engine version and knowledge gap risk level for the domain
- Related ADRs (if any)

**Prompt**:
> "Review this Architecture Decision Record. Does it have a clear problem statement
> and rationale? Are the rejected alternatives genuinely considered? Does the
> Consequences section acknowledge the trade-offs honestly? Is the engine version
> stamped? Are post-cutoff API risks flagged? Does it link to the GDD requirements
> it covers? Return APPROVE, CONCERNS [specific gaps], or REJECT [the decision is
> underspecified or makes unsound technical assumptions]."

**Verdicts**: APPROVE / CONCERNS / REJECT

---

### TD-ENGINE-RISK — Engine Version Risk Review

**Trigger**: When making architecture decisions that touch post-cutoff engine APIs,
or before finalizing any engine-specific implementation approach

**Context to pass**:
- The specific API or feature being used
- Engine version and LLM knowledge cutoff (from `docs/engine-reference/[engine]/VERSION.md`)
- Relevant excerpt from breaking-changes or deprecated-apis docs

**Prompt**:
> "Review this engine API usage against the version reference. Is this API present
> in [engine version]? Has its signature, behaviour, or namespace changed since the
> LLM knowledge cutoff? Are there known deprecations or post-cutoff alternatives?
> Return APPROVE (safe to use as described), CONCERNS [verify before implementing],
> or REJECT [API has changed — provide corrected approach]."

**Verdicts**: APPROVE / CONCERNS / REJECT

---

### TD-PHASE-GATE — Technical Readiness at Phase Transition

**Trigger**: At `$gate-check` in `full` or `lean`; skip with advisory contribution `N/A` in `solo`. Run in parallel with the other applicable phase gates.

**Context to pass**:
- Target phase name
- Architecture document path (if exists)
- Engine reference path
- ADR list

**Prompt**:
> "Review the current project state for [target phase] gate readiness from a
> technical direction perspective. Is the architecture sound for this phase? Are
> all high-risk engine domains addressed? Are performance budgets realistic and
> documented? Are Foundation-layer decisions complete enough to begin implementation?
> Return READY, CONCERNS [list], or NOT READY [blockers]."

**Verdicts**: READY / CONCERNS / NOT READY

---

## Tier 1 — Producer Gates

Agent: `producer` | Role complexity: high-complexity | Domain: Scope, timeline, dependencies, production risk

---

### PR-SCOPE — Scope and Timeline Validation

**Trigger**: After scope tiers are defined in an authoritative artifact (brainstorm
Phase 6 or another owning workflow). A `quick-design` proposal alone neither defines
the MVP nor supplies a timeline estimate.

**Context to pass**:
- Full vision scope description
- MVP definition
- Timeline estimate
- Team size (solo / small team / etc.)
- Scope tiers (what ships if time runs out)

**Prompt**:
> "Review this scope estimate. Is the MVP achievable in the stated timeline for
> the stated team size? Are the scope tiers correctly ordered by risk — does each
> tier deliver a shippable product if work stops there? What is the most likely
> cut point under time pressure, and is it a graceful fallback or a broken product?
> Return REALISTIC (scope matches capacity), OPTIMISTIC [specific adjustments
> recommended], or UNREALISTIC [blockers — timeline or MVP must be revised]."

**Verdicts**: REALISTIC / OPTIMISTIC / UNREALISTIC

---

### PR-SPRINT — Sprint Feasibility Review

**Trigger**: In `$sprint-plan` only when its resolved declared mode is `full`; skipped in `lean`/`solo`. A mid-sprint scope change uses this gate only if its owning consumer separately declares the same contract.

**Context to pass**:
- Proposed sprint story list (titles, estimates, dependencies)
- Team capacity (hours available)
- Current sprint backlog debt (if any)
- Milestone constraints

**Prompt**:
> "Review this sprint plan for feasibility. Is the story load realistic for the
> available capacity? Are stories correctly ordered by dependency? Are there hidden
> dependencies between stories that could block the sprint mid-way? Are any stories
> underestimated given their technical complexity? Return REALISTIC (plan is
> achievable), CONCERNS [specific risks], or UNREALISTIC [sprint must be
> descoped — identify which stories to defer]."

**Verdicts**: REALISTIC / CONCERNS / UNREALISTIC

---

### PR-MILESTONE — Milestone Risk Assessment

**Trigger**: In `$milestone-review` only when its resolved declared mode is `full`; skipped in `lean`/`solo`. Other workflows use it only through an explicit local contract.

**Context to pass**:
- Milestone definition and target date
- Current completion percentage
- Blocked stories count
- Sprint velocity data (if available)

**Prompt**:
> "Review this milestone status. Based on current velocity and blocked story count,
> will this milestone hit its target date? What are the top 3 production risks
> between now and the milestone? Are there scope items that should be cut to protect
> the milestone date vs. items that are non-negotiable? Return ON TRACK, AT RISK
> [specific mitigations], or OFF TRACK [date must slip or scope must cut — provide
> both options]."

**Verdicts**: ON TRACK / AT RISK / OFF TRACK

---

### PR-EPIC — Epic Structure Feasibility Review

**Trigger**: After epics are defined by `$create-epics`, before stories are
broken out — validates the epic structure is producible before `$create-stories`
is invoked

**Context to pass**:
- Epic definition file paths (all epics just created)
- Epic index path (`production/epics/index.md`)
- Milestone timeline and target dates
- Team capacity (solo / small team / size)
- Layer being epiced (Foundation / Core / Feature / etc.)

**Prompt**:
> "Review this epic structure for production feasibility before story breakdown
> begins. Are the epic boundaries scoped appropriately — could each epic realistically
> complete before a milestone deadline? Are epics correctly ordered by system
> dependency — does any epic require another epic's output before it can start?
> Are any epics underscoped (too small, should merge) or overscoped (too large,
> should split into 2-3 focused epics)? Are the Foundation-layer epics scoped to
> allow Core-layer epics to begin at the start of the next sprint after Foundation
> completes? Return REALISTIC (epic structure is producible), CONCERNS [specific
> structural adjustments before stories are written], or UNREALISTIC [epics must
> be split, merged, or reordered — story breakdown cannot begin until resolved]."

**Verdicts**: REALISTIC / CONCERNS / UNREALISTIC

---

### PR-PHASE-GATE — Production Readiness at Phase Transition

**Trigger**: At `$gate-check` in `full` or `lean`; skip with advisory contribution `N/A` in `solo`. Run in parallel with the other applicable phase gates.

**Context to pass**:
- Target phase name
- Sprint and milestone artifacts present
- Team size and capacity
- Current blocked story count

**Prompt**:
> "Review the current project state for [target phase] gate readiness from a
> production perspective. Is the scope realistic for the stated timeline and team
> size? Are dependencies properly ordered so the team can actually execute in
> sequence? Are there milestone or sprint risks that could derail the phase within
> the first two sprints? Return READY, CONCERNS [list], or NOT READY [blockers]."

**Verdicts**: READY / CONCERNS / NOT READY

---

## Tier 1 — Art Director Gates

Agent: `art-director` | Role complexity: standard-complexity | Domain: Visual identity, art bible, visual production readiness

---

### AD-CONCEPT-VISUAL — Visual Identity Anchor

**Trigger**: After game pillars are locked (brainstorm Phase 4), in parallel with CD-PILLARS

**Context to pass**:
- Game concept (elevator pitch, core fantasy, unique hook)
- Full pillar set with names, definitions, and design tests
- Target platform (if known)
- Any reference games or visual touchstones mentioned by the user

**Prompt**:
> "Based on these game pillars and core concept, propose 2-3 distinct visual identity
> directions. For each direction provide: (1) a one-line visual rule that could guide
> all visual decisions (e.g., 'everything must move', 'beauty is in the decay'), (2)
> mood and atmosphere targets, (3) shape language (sharp/rounded/organic/geometric
> emphasis), (4) color philosophy (palette direction, what colors mean in this world).
> Be specific — avoid generic descriptions. One direction should directly serve the
> primary design pillar. Name each direction. Recommend which best serves the stated
> pillars and explain why."

**Verdicts**: CONCEPTS (multiple valid options — user selects) / STRONG (one direction clearly dominant) / CONCERNS (pillars don't provide enough direction to differentiate visual identity yet)

---

### AD-ART-BIBLE — Art Bible Sign-Off

**Trigger**: Only after `$art-bible` proves the AB-1 artifact has all nine stable
sections in COMPLETE state and freezes the exact review candidate bytes; before
any asset specification, generation, import, outsourcing, or implementation

**Context to pass**:
- Canonical art bible path (`design/art/art-bible.md`) and exact raw-byte SHA-256
- AB-1 schema version; all nine stable section IDs, states, and section hashes
- Ordered dependency/source manifest with current hashes
- Author identity and evidence that the assigned `art-director` reviewer did not
  author, revise, or persist the candidate
- Proposed immutable external review-record ID/path; the reviewer itself is read-only
- Game pillars and core fantasy
- Platform and performance constraints (from `.codex/docs/technical-preferences.md` if configured)
- Visual identity anchor chosen during brainstorm (from `design/gdd/game-concept.md`)

**Prompt**:
> "Independently and read-only review the exact art-bible candidate hash supplied;
> echo that hash and the nine-section manifest in the response. Review completeness
> and internal consistency. Does the color
> system match the mood targets? Does the shape language follow from the visual
> identity statement? Are the asset standards achievable within the platform
> constraints? Does the character design direction give artists enough to work from
> without over-specifying? Are there contradictions between sections? Would an
> outsourcing team be able to produce assets from this document without additional
> briefing? Return APPROVE (all nine current sections are complete and the exact
> candidate is production-ready), CONCERNS [specific
> sections needing clarification], or REJECT [fundamental inconsistencies that must
> be resolved before asset production begins]."

**Verdicts**: APPROVE / CONCERNS / REJECT

The response must include reviewer identity, reviewed artifact/dependency hashes,
stable finding IDs, timestamp, and separation attestation. A separate recorder may
persist those unchanged bytes as an immutable review record. The reviewer never
writes the art bible or record. Any candidate/section/dependency byte change makes
APPROVE stale; DRAFT/PARTIAL, missing identity separation, malformed output, or
hash mismatch cannot authorize asset production.

---

### AD-PHASE-GATE — Visual Readiness at Phase Transition

**Trigger**: At `$gate-check` in `full` or `lean`; skip with advisory contribution `N/A` in `solo`. Run in parallel with the other applicable phase gates.

**Context to pass**:
- Target phase name
- List of all art/visual artifacts present (file paths)
- Visual identity anchor from `design/gdd/game-concept.md` (if present)
- Art bible path if it exists (`design/art/art-bible.md`)

**Prompt**:
> "Review the current project state for [target phase] gate readiness from a visual
> direction perspective. Is the visual identity established and documented at the
> level this phase requires? Are the right visual artifacts in place? Would visual
> teams be able to begin their work without visual direction gaps that cause costly
> rework later? Are there visual decisions that are being deferred past their latest
> responsible moment? Return READY, CONCERNS [specific visual direction gaps that
> could cause production rework], or NOT READY [visual blockers that must exist
> before this phase can succeed — specify what artifact is missing and why it
> matters at this stage]."

**Verdicts**: READY / CONCERNS / NOT READY

---

## Tier 2 — Lead Gates

These gates are invoked by orchestration skills and senior skills when a domain
specialist's feasibility sign-off is needed. Tier 2 leads use standard-complexity (default).

---

### LP-FEASIBILITY — Lead Programmer Implementation Feasibility

**Trigger**: After the master architecture document is written (`$create-architecture`
Phase 7b), or when a new architectural pattern is proposed

**Context to pass**:
- Architecture document path
- Technical requirements baseline summary
- ADR list with statuses

**Prompt**:
> "Review this architecture for implementation feasibility. Flag: (a) any decisions
> that would be difficult or impossible to implement with the stated engine and
> language, (b) any missing interface definitions that programmers would need to
> invent themselves, (c) any patterns that create avoidable technical debt or
> that contradict standard [engine] idioms. Return FEASIBLE, CONCERNS [list], or
> INFEASIBLE [blockers that make this architecture unimplementable as written]."

**Verdicts**: FEASIBLE / CONCERNS / INFEASIBLE

---

### LP-CODE-REVIEW — Lead Programmer Code Review

**Trigger**: After a dev story is implemented (`$dev-story`, `$story-done`), or
as part of `$code-review`

**Context to pass**:
- Implementation file paths
- Story file path (for acceptance criteria)
- Relevant GDD section
- ADR that governs this system

**Prompt**:
> "Review this implementation against the story acceptance criteria and governing
> ADR. Does the code match the architecture boundary definitions? Are there
> violations of the coding standards or forbidden patterns? Is the public API
> testable and documented? Are there any correctness issues against the GDD rules?
> Return APPROVE, CONCERNS [specific issues], or REJECT [must be revised before merge]."

**Verdicts**: APPROVE / CONCERNS / REJECT

---

### QL-STORY-READY — QA Lead Story Readiness Check

**Trigger**: In `$story-readiness` only when its resolved declared mode is `full`; skipped in `lean`/`solo`. `$create-stories` and `$sprint-plan` do not inherit this gate unless their own contracts explicitly adopt it.

**Context to pass**:
- Story file path
- Story type (Logic / Integration / Visual/Feel / UI / Config/Data)
- Acceptance criteria list (verbatim from the story)
- The GDD requirement (TR-ID and text) the story covers

**Prompt**:
> "Review this story's acceptance criteria for testability before it enters the
> sprint. Are all criteria specific enough that a developer would know unambiguously
> when they are done? For Logic-type stories: can every criterion be verified with
> an automated test? For Integration stories: is each criterion observable in a
> controlled test environment? Flag criteria that are too vague to implement
> against, and flag criteria that require a full game build to test (mark these
> DEFERRED, not BLOCKED). Return ADEQUATE (criteria are implementable as written),
> GAPS [specific criteria needing refinement], or INADEQUATE [criteria are too
> vague — story must be revised before sprint inclusion]."

**Verdicts**: ADEQUATE / GAPS / INADEQUATE

---

### QL-TEST-COVERAGE — QA Lead Test Coverage Review

**Trigger**: After implementation stories are complete, before marking an epic
done, or at `$gate-check` Production → Polish

**Context to pass**:
- List of implemented stories with story types (Logic / Integration / Visual / UI / Config)
- Test file paths in `tests/`
- GDD acceptance criteria for the system

**Prompt**:
> "Review the test coverage for these implementation stories. Are all Logic stories
> covered by passing unit tests? Are Integration stories covered by integration
> tests or documented playtests? Are the GDD acceptance criteria each mapped to at
> least one test? Are there untested edge cases from the GDD Edge Cases section?
> Return ADEQUATE (coverage meets standards), GAPS [specific missing tests], or
> INADEQUATE [critical logic is untested — do not advance]."

**Verdicts**: ADEQUATE / GAPS / INADEQUATE

---

### ND-CONSISTENCY — Narrative Director Consistency Check

**Trigger**: After writer deliverables (dialogue, lore, item descriptions) are
authored, or when a design decision has narrative implications

**Context to pass**:
- Document or content file path(s)
- Narrative bible or tone guide path (if exists)
- Relevant world-building rules
- Character or faction profiles affected

**Prompt**:
> "Review this narrative content for internal consistency and adherence to
> established world rules. Are character voices consistent with their established
> profiles? Does the lore contradict any established facts? Is the tone consistent
> with the game's narrative direction? Return APPROVE, CONCERNS [specific
> inconsistencies to fix], or REJECT [contradictions that break the narrative
> foundation]."

**Verdicts**: APPROVE / CONCERNS / REJECT

---

### AD-VISUAL — Art Director Visual Consistency Review

**Trigger**: After art direction decisions are made, when new asset types are
introduced, or when a tech art decision affects visual style

**Context to pass**:
- Art bible path (if exists at `design/art/art-bible.md`)
- The specific asset type, style decision, or visual direction being reviewed
- Reference images or style descriptions
- Platform and performance constraints

**Prompt**:
> "Review this visual direction decision for consistency with the established art
> style and production constraints. Does it match the art bible? Is it achievable
> within the platform's performance budget? Are there asset pipeline implications
> that create technical risk? Return APPROVE, CONCERNS [specific adjustments], or
> REJECT [style violation or production risk that must be resolved first]."

**Verdicts**: APPROVE / CONCERNS / REJECT

---

## Parallel Gate Protocol

When a workflow requires multiple directors at the same checkpoint (most common
at `$gate-check`), spawn all agents simultaneously:

```
Spawn in parallel (issue all Codex subagent delegations before waiting for any result):
1. creative-director  → gate CD-PHASE-GATE
2. technical-director → gate TD-PHASE-GATE
3. producer           → gate PR-PHASE-GATE
4. art-director       → gate AD-PHASE-GATE

Collect all four verdicts, then apply escalation rules:
- Any NOT READY / REJECT → overall verdict minimum FAIL
- Any CONCERNS → overall verdict minimum CONCERNS
- All READY / APPROVE → eligible for PASS (still subject to artifact checks)
```

---

## Adding New Gates

When a new gate is needed for a new skill or workflow:

1. Assign a gate ID: `[DIRECTOR-PREFIX]-[DESCRIPTIVE-SLUG]`
   - Prefixes: `CD-` `TD-` `PR-` `LP-` `QL-` `ND-` `AD-`
   - Add new prefixes for new agents: `audio-director` → `AU-`, `ux-designer` → `UX-`
2. Add the gate under the appropriate director section with all five fields:
   Trigger, Context to pass, Prompt, Verdicts, and any special handling notes
3. Reference it in skills by ID only — never copy the prompt text into the skill

---

## Gate registry by stage

This table is discovery metadata, not a required-gate matrix. The consumer-specific mode table and each consumer's own contract decide applicability.

| Stage | Available gate IDs |
|---|---|
| Concept | CD-PILLARS, AD-CONCEPT-VISUAL, TD-FEASIBILITY, PR-SCOPE |
| Systems Design | TD-SYSTEM-BOUNDARY, CD-SYSTEMS, PR-SCOPE, CD-GDD-ALIGN, ND-CONSISTENCY, AD-VISUAL |
| Technical Setup | TD-ARCHITECTURE, TD-ADR, LP-FEASIBILITY, AD-ART-BIBLE, TD-ENGINE-RISK |
| Pre-Production | PR-EPIC, QL-STORY-READY, PR-SPRINT, CD/TD/PR/AD-PHASE-GATE, CD-PLAYTEST |
| Production | LP-CODE-REVIEW, QL-STORY-READY, PR-SPRINT, QL-TEST-COVERAGE, PR-MILESTONE, AD-VISUAL |
| Polish | QL-TEST-COVERAGE, CD-PLAYTEST, PR-MILESTONE, AD-VISUAL |
| Release | CD/TD/PR/AD-PHASE-GATE, QL-TEST-COVERAGE |
