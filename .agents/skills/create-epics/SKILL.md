---
name: create-epics
description: "Translate approved GDDs + architecture into epics — one epic per architectural module. Defines scope, governing ADRs, engine risk, and untraced requirements. Does NOT break into stories — run $create-stories [epic-slug] after each epic is created."
---

## Invocation and execution

Invoke this workflow as `$create-epics`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[system-name | layer: foundation|core|feature|presentation | all] [--review full|lean|solo]`. Treat bracketed values as optional unless the workflow says otherwise.

Delegate substantive work to the `technical-director` Codex subagent role when it is available. If that role is unavailable, follow the same responsibilities in the current agent.


# Create Epics

An epic is a named, bounded body of work that maps to one architectural module.
It defines **what** needs to be built and **who owns it architecturally**. It
does not prescribe implementation steps — that is the job of stories.

**Run this skill once per layer** as you approach that layer in development.
Do not create Feature layer epics until Core is nearly complete — the design
will have changed.

**Output:** `production/epics/[epic-slug]/EPIC.md` + `production/epics/index.md`

**Next step after each epic:** `$create-stories [epic-slug]`

**When to run:** After `$create-control-manifest` and `$architecture-review` pass.

---

## 1. Parse Arguments

Resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `production/review-mode.txt` → use that value
3. Else → default to `lean`

See `.codex/docs/director-gates.md` for the full check pattern.

**Modes:**
- `$create-epics all` — process all systems in layer order
- `$create-epics layer: foundation` — Foundation layer only
- `$create-epics layer: core` — Core layer only
- `$create-epics layer: feature` — Feature layer only
- `$create-epics layer: presentation` — Presentation layer only
- `$create-epics [system-name]` — one specific system
- No argument — ask: "Which layer or system would you like to create epics for?"

Normalize the existing layer syntax as `layer:<value>` while tolerating
whitespace after the colon during parsing. The value must be exactly one of
foundation/core/feature/presentation. Empty values, unknown layers, or multiple
conflicting scope modes stop before input loading.

---

## 2. Load Inputs

### Step 2a — Determine scope from the systems index

Read `design/gdd/systems-index.md` first. Use its system-to-file mapping, layer,
and status as the source of scope. Only `Approved` or `Designed` index rows are
eligible. Read each mapped GDD's own Status header and cross-check it; a missing
or contradictory status stops that system with evidence rather than choosing
one source. A `## Summary` search may accelerate
summarization, but a missing Summary never excludes a mapped GDD; read its
Overview instead.

### Step 2b — Full document load (in-scope systems only)

Use the systems-index scope from Step 2a. Read full documents only for in-scope
systems — do not read GDDs or ADRs for out-of-scope systems or layers.

Read for in-scope systems:

- `design/gdd/systems-index.md` — authoritative system list, layers, priority
- In-scope GDDs only (Approved or Designed status, filtered by Step 2a results)
- `docs/architecture/architecture.md` — module ownership and API boundaries
- Accepted ADRs **whose domains cover in-scope systems only** — read the "GDD Requirements Addressed", "Decision", and "Engine Compatibility" sections; skip ADRs for unrelated domains
- `docs/architecture/control-manifest.md` — manifest version date from header
- `docs/architecture/tr-registry.yaml` — for tracing requirements to ADR coverage
- `docs/engine-reference/[engine]/VERSION.md` — engine name, version, risk levels

Report: "Loaded [N] GDDs, [M] ADRs, engine: [name + version]."

---

## 3. Processing Order

Build the dependency graph from the actual dependencies in `systems-index.md`
and process it topologically. Layer order (Foundation, Core, Feature,
Presentation) is only a secondary tie-breaker for nodes that are otherwise
ready; do not assume every Foundation node is dependency-free. Detect and show
cycles. Every epic containing a cyclic requirement is Blocked and is not passed
off as dependency-safe until the cycle is resolved.

---

## 4. Define Each Epic

Use each existing architectural module in `architecture.md` as the epic
identity. Aggregate all in-scope systems owned by the same module into one epic.
If one system crosses modules, allocate each requirement according to the
ownership recorded in architecture.md; do not duplicate the whole system scope
into every epic.

Check ADR coverage against the TR registry:
- **Traced requirements**: TR-IDs that have an Accepted ADR covering them
- **Untraced requirements**: TR-IDs with no ADR — warn before proceeding

Present to user before writing anything:

```
## Epic: [Architecture Module]

**Layer**: [Foundation / Core / Feature / Presentation]
**Systems/GDDs**: [system → design/gdd/filename.md, ...]
**Architecture Module**: [module name from architecture.md]
**Governing ADRs**: [ADR-NNNN, ADR-MMMM]
**Engine Risk**: [LOW / MEDIUM / HIGH / UNKNOWN — highest valid risk among governing ADRs]
**GDD Requirements Covered by ADRs**: [N / total]
**Untraced Requirements**: [list TR-IDs with no ADR, or "None"]
```

Accept only existing LOW/MEDIUM/HIGH risk values. A missing ADR, absent risk
field, or illegal value yields UNKNOWN and prevents the affected requirement
from being described as engine-validated.

If there are untraced requirements, report them without creating placeholders.
An epic containing any untraced Foundation/Core requirement uses the existing
`Blocked` status. For other layers, the epic may remain Ready only when the
untraced rows are explicitly marked blocked in the requirement table.

Ask the user directly:
- Prompt: "Shall I create Epic: [name]?"
- Options:
  - `[A] Yes, create it`
  - `[B] Skip this epic`
  - `[C] Pause — I need to write ADRs first`

---

## 4b. Producer Epic Structure Gate

**Review mode check** — apply before spawning PR-EPIC:
- `solo` → skip. Note: "PR-EPIC skipped — Solo mode." Proceed to Step 5 (write epic files).
- `lean` → skip (not a PHASE-GATE). Note: "PR-EPIC skipped — Lean mode." Proceed to Step 5 (write epic files).
- `full` → spawn as normal.

After all epics for the current layer are defined (Step 4 completed for all in-scope systems), and before writing any files, spawn `producer` through Codex subagent delegation using gate **PR-EPIC** (`.codex/docs/director-gates.md`).

Pass, for every epic: its complete inline `EPIC.md` draft, the planned final
path, and the complete planned `production/epics/index.md` edit, plus the layer,
milestone timeline, and team capacity. These are planned paths, not files that
already exist. The gate must review the exact write candidates; do not write a
skeleton or temporary epic before the gate.

Present the producer's assessment.

If UNREALISTIC, ask the user to choose `Revise boundaries` or `Stop`. Show the
exact proposed split/merge before revising and re-run the gate only after the
user selects revise. A stop ends BLOCKED; never loop automatically.

If CONCERNS, ask the user directly:
- Prompt: "Producer raised concerns about the epic structure. How do you want to proceed?"
- Options:
  - `[A] Proceed as planned — I accept the producer's concerns`
  - `[B] Revise epic boundaries — split or merge as recommended`
  - `[C] Stop — I want to reconsider the scope`

If [A]: proceed to Step 5.
If [B]: revise epic definitions from Step 4 and re-run the producer gate.
If [C]: stop. Verdict: **BLOCKED** — user wants to reconsider epic scope.

Do not write epic files until the producer gate resolves.

---

## 5. Write Epic Files

Before the preview, inspect every planned EPIC path and the index. For an
existing EPIC, show its scoped diff and ask `update` or `skip`; never overwrite
silently. A skipped epic is omitted from the write set.

For the index, match by unique epic slug/module. Update exactly one matching row
or append one new row, retain every out-of-scope row unchanged, and report an
error on duplicate matches rather than rebuilding the table.

Add this proposed file or edit to the complete changeset preview; do not write it until that changeset is authorized.

After user confirms, write:

### `production/epics/[epic-slug]/EPIC.md`

```markdown
# Epic: [Architecture Module]

> **Layer**: [Foundation / Core / Feature / Presentation]
> **Systems/GDDs**: [system → design/gdd/filename.md, ...]
> **Architecture Module**: [module name]
> **Status**: [Ready | Blocked — untraced Foundation/Core requirement]
> **Stories**: Not yet created — run `$create-stories [epic-slug]`

## Overview

[1 paragraph describing what this epic implements, derived from the GDD Overview
and the architecture module's stated responsibilities]

## Governing ADRs

| ADR | Decision Summary | Engine Risk |
|-----|-----------------|-------------|
| ADR-NNNN: [title] | [1-line summary] | LOW/MEDIUM/HIGH |

## GDD Requirements

| TR-ID | Requirement | ADR Coverage |
|-------|-------------|--------------|
| TR-[system]-001 | [requirement text from registry] | ADR-NNNN ✅ |
| TR-[system]-002 | [requirement text] | ❌ No ADR |

## Definition of Done

This epic is complete when:
- All stories are implemented, reviewed, and closed via `$story-done`
- All acceptance criteria from `design/gdd/[filename].md` are verified
- All Logic and Integration stories have passing test files in `tests/`
- All Visual/Feel and UI stories have evidence docs with sign-off in `production/qa/evidence/`

## Next Step

Run `$create-stories [epic-slug]` to break this epic into implementable stories.
```

### Update `production/epics/index.md`

Create or update the master index:

```markdown
# Epics Index

Last Updated: [date]
Engine: [name + version]

| Epic | Layer | System | GDD | Stories | Status |
|------|-------|--------|-----|---------|--------|
| [module name] | Foundation | [systems] | [files] | Not yet created | [Ready/Blocked] |
```

---

## 6. Gate-Check Reminder

After writing all epics for the requested scope:

- **Foundation + Core complete**: These are required for the Pre-Production →
  Production gate. Run `$gate-check pre-production` to check readiness.
- **Reminder**: Epics define scope. Stories define implementation steps. Run
  `$create-stories [epic-slug]` for each epic before developers can pick up work.

---

## Collaborative Protocol

1. **One epic at a time** — present each epic definition before asking to create it
2. **Warn on gaps** — flag untraced requirements before proceeding
3. **Single changeset approval** — preview every requested epic file together and write the set only after the one approval
4. **No invention** — all content comes from GDDs, ADRs, and architecture docs
5. **Never create stories** — this skill stops at the epic level

After all requested epics are processed:

- **Verdict: COMPLETE** — [N] epic(s) written. Run `$create-stories [epic-slug]` per epic.
- **Verdict: BLOCKED** — user declined all epics, or no eligible systems found.
