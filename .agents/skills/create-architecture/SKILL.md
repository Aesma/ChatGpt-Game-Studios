---
name: create-architecture
description: "Guided, section-by-section authoring of the master architecture document for the game. Reads all GDDs, the systems index, existing ADRs, and the engine reference library to produce a complete architecture blueprint before any code is written. Engine-version-aware: flags knowledge gaps and validates decisions against the pinned engine version."
---

## Invocation and execution

Invoke this workflow as `$create-architecture`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[focus-area: full | layers | data-flow | api-boundaries | adr-audit] [--review full|lean|solo]`. Treat bracketed values as optional unless the workflow says otherwise.

Delegate substantive work to the `technical-director` Codex subagent role when it is available. If that role is unavailable, follow the same responsibilities in the current agent.


# Create Architecture

This skill produces `docs/architecture/architecture.md` — the master architecture
document that translates all approved GDDs into a concrete technical blueprint.
It sits between design and implementation, and must exist before sprint planning begins.

**Distinct from `$architecture-decision`**: ADRs record individual point decisions.
This skill creates the whole-system blueprint that gives ADRs their context.

Resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `production/review-mode.txt` → use that value
3. Else → default to `lean`

See `.codex/docs/director-gates.md` for the full check pattern.

**Argument modes:**
- **No argument / `full`**: Full guided walkthrough — all sections, start to finish
- **`layers`**: Focus on the system layer diagram only
- **`data-flow`**: Focus on data flow between modules only
- **`api-boundaries`**: Focus on API boundary definitions only
- **`adr-audit`**: Audit existing ADRs for engine compatibility gaps only

Reject an unknown or conflicting focus mode. Apply these guards throughout the
existing phases:

- `full`: execute Phases 0–8.
- `layers`: load only the context needed for the System Layer Map and edit only
  that existing section.
- `data-flow`: load only module/dependency context and edit only Data Flow.
- `api-boundaries`: load only module/API context and edit only API Boundaries.
- `adr-audit`: run the existing ADR audit and output findings read-only. Edit
  `architecture.md` only if that exact edit was included in the authorized
  changeset.

A focus run must not rewrite untouched sections or emit a full-mode completion
handoff.

---

## Phase 0: Load All Context

Before anything else, load the full project context in this order:

### 0a. Engine Context (Critical)

Read the engine reference library completely:

1. `docs/engine-reference/[engine]/VERSION.md`
   → Extract: engine name, version, LLM cutoff, post-cutoff risk levels
2. `docs/engine-reference/[engine]/breaking-changes.md`
   → Extract: all HIGH and MEDIUM risk changes
3. `docs/engine-reference/[engine]/deprecated-apis.md`
   → Extract: APIs to avoid
4. `docs/engine-reference/[engine]/current-best-practices.md`
   → Extract: post-cutoff best practices that differ from training data
5. All files in `docs/engine-reference/[engine]/modules/`
   → Extract: current API patterns per domain

If no engine is configured, stop and prompt:
> "No engine is configured. Run `$setup-engine` first. Architecture cannot be
> written without knowing which engine and version you are targeting."

### 0b. Design Context + Technical Requirements Extraction

Read all approved design documents and extract technical requirements from each:

1. `design/gdd/game-concept.md` — game pillars, genre, core loop
2. `design/gdd/systems-index.md` — all systems, dependencies, priority tiers
3. `docs/technical-preferences.md` — naming conventions, performance budgets,
   allowed libraries, forbidden patterns
4. **Every GDD in `design/gdd/`** — for each, extract technical requirements:
   - Data structures implied by the game rules
   - Performance constraints stated or implied
   - Engine capabilities the system requires
   - Cross-system communication patterns (what talks to what, how)
   - State that must persist (save/load implications)
   - Threading or timing requirements

Build a **Technical Requirements Baseline** — a flat list of all extracted
requirements across all GDDs, numbered `TR-[gdd-slug]-[NNN]`. This is the
complete set of what the architecture must cover. Present it as:

```
## Technical Requirements Baseline
Extracted from [N] GDDs | [X] total requirements

| Req ID | GDD | System | Requirement | Domain |
|--------|-----|--------|-------------|--------|
| TR-combat-001 | combat.md | Combat | Hitbox detection per-frame | Physics |
| TR-combat-002 | combat.md | Combat | Combo state machine | Core |
| TR-inventory-001 | inventory.md | Inventory | Item persistence | Save/Load |
```

This baseline feeds into every subsequent phase. No GDD requirement should be
left without an architectural decision to support it by the end of this session.

### 0c. Existing Architecture Decisions

Read all files in `docs/architecture/` to understand what has already been decided.
List any ADRs found and their domains.

### 0d. Generate Knowledge Gap Inventory

Before proceeding, display a structured summary:

```
## Engine Knowledge Gap Inventory
Engine: [name + version]
LLM Training Covers: up to approximately [version]
Post-Cutoff Versions: [list]

### HIGH RISK Domains (must verify against engine reference before deciding)
- [Domain]: [Key changes]

### MEDIUM RISK Domains (verify key APIs)
- [Domain]: [Key changes]

### LOW RISK Domains (in training data, likely reliable)
- [Domain]: [no significant post-cutoff changes]

### Systems from GDD that touch HIGH/MEDIUM risk domains:
- [GDD system name] → [domain] → [risk level]
```

Ask the user directly:
- Prompt: "One or more engine domains are HIGH RISK — the LLM's knowledge may be unreliable for these areas. Architectural recommendations in these domains should be cross-referenced with the engine docs before being acted on. How would you like to proceed?"
- Options:
  - `[A] Proceed — flag HIGH RISK domains throughout the output`
  - `[B] Let me check the engine reference first — pause here`
  - `[C] Show me which domains are HIGH RISK and why`

### 0e. Authorize and create the architecture skeleton

For a new full architecture, the first write is a complete heading skeleton for
`docs/architecture/architecture.md` using the structure already defined in
Phase 7. Before that write, show one complete changeset preview that includes:

- creation and all later section/status edits to `architecture.md`;
- the conditional final update to `production/session-state/active.md`.

Obtain authorization once. Create the skeleton with Document Status set to
`In Design`, then persist each subsequently approved section inside that same
boundary. If the scope later adds a file, stop and preview only the expanded
changeset. Focus modes use the same one-authorization rule for their selected
section and must not recreate the skeleton.

---

## Phase 1: System Layer Mapping

Map every system from `systems-index.md` into an architecture layer. The standard
game architecture layers are:

```
┌─────────────────────────────────────────────┐
│  PRESENTATION LAYER                         │  ← UI, HUD, menus, VFX, audio
├─────────────────────────────────────────────┤
│  FEATURE LAYER                              │  ← gameplay systems, AI, quests
├─────────────────────────────────────────────┤
│  CORE LAYER                                 │  ← physics, input, combat, movement
├─────────────────────────────────────────────┤
│  FOUNDATION LAYER                           │  ← engine integration, save/load,
│                                             │    scene management, event bus
├─────────────────────────────────────────────┤
│  PLATFORM LAYER                             │  ← OS, hardware, engine API surface
└─────────────────────────────────────────────┘
```

For each GDD system, ask:
- Which layer does it belong to?
- What are its module boundaries?
- What does it own exclusively? (data, state, behaviour)

Present the proposed layer assignment and ask for approval before proceeding to
the next section. Write the approved layer map immediately to the skeleton file.

**Engine awareness check**: For each system assigned to the Core and Foundation
layers, flag if it touches a HIGH or MEDIUM risk engine domain. Show the relevant
engine reference excerpt inline.

---

## Phase 2: Module Ownership Map

For each module defined in Phase 1, define ownership:

- **Owns**: what data and state this module is solely responsible for
- **Exposes**: what other modules may read or call
- **Consumes**: what it reads from other modules
- **Engine APIs used**: which specific engine classes/nodes/signals this module
  calls directly (with version and risk level noted)

Format as a table per layer, then as an ASCII dependency diagram.

**Engine awareness check**: For every engine API listed, verify against the
relevant module reference doc. If an API is post-cutoff, flag it:

```
⚠️  [ClassName.method()] — Godot 4.6 (post-cutoff, HIGH risk)
    Verified against: docs/engine-reference/godot/modules/[domain].md
    Behaviour confirmed: [yes / NEEDS VERIFICATION]
```

Get user approval on the ownership map before writing.

---

## Phase 3: Data Flow

Define how data moves between modules during key game scenarios. Cover at minimum:

1. **Frame update path**: Input → Core systems → State → Rendering
2. **Event/signal path**: How systems communicate without tight coupling
3. **Save/load path**: What state is serialised, which module owns serialisation
4. **Initialisation order**: Which modules must boot before others

Use ASCII sequence diagrams where helpful. For each data flow:
- Name the data being transferred
- Identify the producer and consumer
- State whether this is synchronous call, signal/event, or shared state
- Flag any data flows that cross thread boundaries

Confirm each scenario's data flow with the user before adding it to the draft; this is a design decision, not a separate file-write approval.

---

## Phase 4: API Boundaries

Define the public contracts between modules. For each boundary:

- What is the interface a module exposes to the rest of the system?
- What are the entry points (functions/signals/properties)?
- What invariants must callers respect?
- What must the module guarantee to callers?

Write in pseudocode or the project's actual language (from technical preferences).
These become the contracts programmers implement against.

**Engine awareness check**: If any interface uses engine-specific types (e.g.
`Node`, `Resource`, `Signal` in Godot), flag the version and verify the type
exists and has not changed signature in the target engine version.

---

## Phase 5: ADR Audit + Traceability Check

Review all existing ADRs from Phase 0c against both the architecture built in
Phases 1-4 AND the Technical Requirements Baseline from Phase 0b.

### ADR Quality Check

For each ADR:
- [ ] Does it have an Engine Compatibility section?
- [ ] Is the engine version recorded?
- [ ] Are post-cutoff APIs flagged?
- [ ] Does it have a "GDD Requirements Addressed" section?
- [ ] Does it conflict with the layer/ownership decisions made in this session?
- [ ] Is it still valid for the pinned engine version?

| ADR | Engine Compat | Version | GDD Linkage | Conflicts | Valid |
|-----|--------------|---------|-------------|-----------|-------|
| ADR-0001: [title] | ✅/❌ | ✅/❌ | ✅/❌ | None/[conflict] | ✅/⚠️ |

### Traceability Coverage Check

Map every requirement from the Technical Requirements Baseline to existing ADRs.
For each requirement, check if any ADR's "GDD Requirements Addressed" section
or decision text covers it:

| Req ID | Requirement | ADR Coverage | Status |
|--------|-------------|--------------|--------|
| TR-combat-001 | Hitbox detection per-frame | ADR-0003 | ✅ |
| TR-combat-002 | Combo state machine | — | ❌ GAP |

Count: X covered, Y gaps. For each gap, it becomes a **Required New ADR**.

### Required New ADRs

List all decisions made during this architecture session (Phases 1-4) that do
not yet have a corresponding ADR, PLUS all uncovered Technical Requirements.
Group by layer — Foundation first:

**Foundation Layer (must create before any coding):**
- `$architecture-decision [title]` → covers: TR-[id], TR-[id]

**Core Layer:**
- `$architecture-decision [title]` → covers: TR-[id]

---

## Phase 6: Missing ADR List

Based on the full architecture, produce a complete list of ADRs that should exist
but don't yet. Group by priority:

**Must have before coding starts (Foundation & Core decisions):**
- [e.g. "Scene management and scene loading strategy"]
- [e.g. "Event bus vs direct signal architecture"]

**Should have before the relevant system is built:**
- [e.g. "Inventory serialisation format"]

**Can defer to implementation:**
- [e.g. "Specific shader technique for water"]

---

## Phase 7: Finalize the Master Architecture Draft

The skeleton already exists and approved sections have been written
incrementally. Assemble and display the complete final draft, verify every
skeleton section is populated or explicitly deferred, and do not rewrite the
whole file. Keep Document Status as `In Design` until Phase 7b returns gate
results. The initial authorization already covered the final status edit, so do
not request a second file authorization.

The document structure:

```markdown
# [Game Name] — Master Architecture

## Document Status
- Status: In Design
- Version: [N]
- Last Updated: [date]
- Engine: [name + version]
- GDDs Covered: [list]
- ADRs Referenced: [list]

## Engine Knowledge Gap Summary
[Condensed from Phase 0d inventory — HIGH/MEDIUM risk domains and their implications]

## System Layer Map
[From Phase 1]

## Module Ownership
[From Phase 2]

## Data Flow
[From Phase 3]

## API Boundaries
[From Phase 4]

## ADR Audit
[From Phase 5]

## Required ADRs
[From Phase 6]

## Architecture Principles
[3-5 key principles that govern all technical decisions for this project,
derived from the game concept, GDDs, and technical preferences]

## Open Questions
[Decisions deferred — must be resolved before the relevant layer is built]
```

---

## Phase 7b: Technical Director Sign-Off + Lead Programmer Feasibility Review

Run this phase after the complete draft exists but before any Complete/Approved
status or completion handoff is written.

- In `full` mode, start independent TD-ARCHITECTURE and LP-FEASIBILITY reviews
  concurrently against the same complete draft and Technical Requirements
  Baseline. Neither verdict is input to the other.
- The author must not self-sign as technical director. If either required role is
  unavailable or fails, sign-off is blocked; do not fabricate a verdict.
- In `lean` or `solo`, record that both gates were skipped according to review
  mode and do not write director sign-off.

Present the two real verdicts side by side. Handle the strictest result:
REJECT or INFEASIBLE leaves the existing skeleton/approved sections `In Design`
and forbids "Architecture Complete"; CONCERNS may be revised or explicitly
accepted; only successful/accepted results allow the already-authorized Document
Status edit. Record the gate's actual verdict vocabulary rather than inventing a
replacement status.

---

## Phase 8: Handoff

**Step 1 — Update session state**: Only when `active.md` was included in the
initial authorized changeset, write a summary covering the architecture status,
real TD/LP results or skips, blockers, required ADRs, and next step.

**Step 2 — Output the handoff** using exactly this template (no freeform prose, no rephrasing of section titles):

---

## Architecture [Complete | In Design — Blocked]

`docs/architecture/architecture.md` [version from Document Status] — [actual TD
and LP verdicts, skips, or blocker]. [One sentence on what the architecture covers.]

---

## Run These ADRs Next

**1. `$architecture-decision "[Title]"` → ADR-[XXXX]**
[One sentence: what it defines and what it unblocks.]

**2. `$architecture-decision "[Title]"` → ADR-[XXXX]**
[One sentence.]

**3. `$architecture-decision "[Title]"` → ADR-[XXXX]**
[One sentence.]

List top 3 from Phase 6 in priority order. If fewer than 3 remain, list only what's outstanding.

---

## Gate-Check Readiness

> **Required before `$gate-check technical-setup`:**
> - [ ] Accept ADRs: [list Proposed ADR IDs that must be Accepted]
> - [ ] Write ADRs: [list ADR IDs that must still be written]
> - [ ] Run `$test-setup` — scaffolds the configured test directories and CI workflow; it does not claim an example test exists
> - [ ] Run `$ux-design` separately for each required screen/HUD and with `patterns` when an interaction library is required; author `design/ux/accessibility-requirements.md` explicitly from its existing template
>
> Run `$gate-check technical-setup` when all boxes are checked.

If nothing is blocking, write instead:
> No blockers — run `$gate-check technical-setup` now.

---

## Open Questions to Watch

| ID | Summary | Priority | Resolution Path |
|----|---------|----------|-----------------|
| QQ-XX | [short description] | High / Medium / Low | [ADR or system that resolves it] |

Omit this section entirely if there are no open QQs.

---

(End of handoff. Do not add trailing commentary after the closing rule.)

---

## Collaborative Protocol

This skill follows the collaborative design principle at every phase:

1. **Load context silently** — do not narrate file reads
2. **Present findings** — show the knowledge gap inventory and layer proposals
3. **Ask before deciding** — present options for each architectural choice
4. **Draft before approval** — show the content inline before asking to write it.
   Never ask approval for a section the user has not yet seen.
5. **Use the single changeset approval policy** — plain text "a separate file prompt" is not
   sufficient. Use the structured tool with labeled options [A]/[B]/[C] (write now /
   show full draft first / not yet). For multi-file changesets, list every file
   and what changes, then ask once grouped — not separate plain-text asks per file.
6. **Incremental writing** — write each approved section immediately; do not
   accumulate everything and write at the end. This survives session crashes.

Never make a binding architectural decision without user input. If the user is
unsure, present 2-4 options with pros/cons before asking them to decide.

---

## Recommended Next Steps

- Run `$architecture-decision [title]` for each required ADR listed in Phase 6 — Foundation layer ADRs first
- Run `$architecture-review` — bootstraps the Requirements Traceability Matrix and TR registry from the ADRs just written. Required before the Pre-Production gate.
- Run `$test-setup` to scaffold the configured test directories and CI workflow; do not treat scaffolding as proof that an example test was created or passed
- Run `$ux-design` separately for the required screens/HUD and `$ux-design patterns` for the interaction library; create `design/ux/accessibility-requirements.md` only through an explicit, authorized template-based edit
- Run `$create-control-manifest` once the required ADRs are written to produce the layer rules manifest
- Run `$gate-check technical-setup` when all required ADRs and the applicable test/UX artifacts are complete
