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

---

## 2. Load Inputs

### Step 2a — Enumerate from the systems index (authoritative)

Read `design/gdd/systems-index.md` in full before opening any individual GDD.
The Systems Enumeration and its dependency/layer tables are the only authority
for deciding which systems and GDD paths exist for this workflow. A filesystem
glob, filename, document title, `## Summary`, `## Overview`, or prose search may
help display an already-selected system, but must never add or remove a system.

Build an immutable run manifest from the index. Every candidate row must provide:

- a stable system ID explicitly recorded by the index; the `#` ordering column is
  not an identity and must not be promoted into one;
- one legal status from `Not Started`, `In Design`, `In Review`, `Approved`,
  or `Implemented`; only the exact status `Approved` is eligible;
- one explicit repository-relative `Design Doc` path under `design/gdd/`; and
- one unambiguous layer from the index dependency/order data.

Normalize paths only for comparison. Do not guess a missing path from the system
name and do not discover replacement GDDs by scanning the directory. Reject
duplicate IDs, duplicate GDD paths, conflicting layer records, path traversal,
missing files, and ambiguous system-name matches. An invalid status token such as
`Designed` is malformed input, not an alias for `Approved`.

Apply the invocation scope only to this validated manifest:

- `all` selects every eligible row in index order;
- `layer: <name>` selects eligible rows in that exact layer and index order; and
- `[system-name]` must resolve to exactly one indexed row by stable ID or exact
  system name, then that row must be `Approved`.

Legal but ineligible rows are reported as excluded. If a requested row is
ineligible, malformed, missing, or ambiguous, stop with **BLOCKED**. If malformed
or contradictory rows prevent the requested scope from being enumerated
completely, stop before drafting or writing. If no eligible rows remain, stop with
**BLOCKED — no eligible systems found**.

### Step 2b — Full document load (selected manifest only)

Read the full GDD only at each selected manifest path. Confirm its own recorded
identity and status agree with the index; any mismatch is **BLOCKED**. Do not
full-read out-of-scope GDDs merely to decide whether they belong.

Then read for the selected systems:

- `docs/architecture/architecture.md` — module ownership and API boundaries;
- Accepted ADRs whose domains cover selected systems — read the "GDD Requirements
  Addressed", "Decision", and "Engine Compatibility" sections;
- `docs/architecture/control-manifest.md` — manifest version date from header;
- `docs/architecture/tr-registry.yaml` — requirement-to-ADR coverage; and
- `docs/engine-reference/[engine]/VERSION.md` — engine name, version, risk levels.

The architecture is a derived view, not a source that can promote proposals into
contracts. A module mapping or ownership claim is usable only when the architecture
marks it as binding and cites a current Accepted ADR. `NON-BINDING PROPOSAL`,
`DECISION-*` gaps, Proposed/Superseded/Rejected ADRs, stale ADR bindings, and
uncited inferred placements may be reported, but they cannot define a production
epic. If a selected system has no unambiguous binding module, stop with
**BLOCKED — accepted architecture decision required**; do not infer a module.

Report the run manifest before drafting:

```text
Loaded [N] indexed Approved GDDs, [M] Accepted ADRs, engine: [name + version].

| System ID | System | Layer | Index Status | GDD Path | Eligibility |
|---|---|---|---|---|---|
| [stable-id] | [name] | [layer] | Approved | [exact path] | included |
```
---

## 3. Processing Order

Process in dependency-safe layer order:
1. **Foundation** (no dependencies)
2. **Core** (depends on Foundation)
3. **Feature** (depends on Core)
4. **Presentation** (depends on Feature + Core)

Within each layer, use the order from `systems-index.md`.

---

## 4. Define Each Epic

For each selected system, use the binding architectural module recorded in
`architecture.md`. Preserve the stable system ID and exact indexed GDD path in
the draft identity. Do not use a non-binding proposal or an unresolved
`DECISION-*` placement as an architecture module.

Check ADR coverage against the TR registry:
- **Traced requirements**: TR-IDs that have an Accepted ADR covering them
- **Untraced requirements**: TR-IDs with no ADR — warn before proceeding

Present to user before writing anything:

```
## Epic: [System Name]

**System ID**: [stable system ID from systems-index]
**Layer**: [Foundation / Core / Feature / Presentation]
**GDD**: design/gdd/[filename].md
**Architecture Module**: [module name from architecture.md]
**Governing ADRs**: [ADR-NNNN, ADR-MMMM]
**Engine Risk**: [LOW / MEDIUM / HIGH — highest risk among governing ADRs]
**GDD Requirements Covered by ADRs**: [N / total]
**Untraced Requirements**: [list TR-IDs with no ADR, or "None"]
```

If there are untraced requirements:
> "⚠️ [N] requirements in [system] have no ADR. The epic can be created, but
> stories for these requirements will be marked Blocked until ADRs exist.
> Run `$architecture-decision` first, or proceed with placeholders."

Ask the user for a scope decision:
- Prompt: "Include Epic: [name] in the proposed changeset?"
- Options:
  - `[A] Include it`
  - `[B] Skip this epic`
  - `[C] Pause — I need to write ADRs first`

These choices select scope only; they do not authorize any file write. Gather all
epic scope decisions before the single changeset preview.

---

## 4a. Inventory Existing Artifacts and Classify the Changeset

Complete this read-only inventory before PR-EPIC and before any write
authorization. Derive every target slug deterministically from the project naming
convention. If no convention exists, use lowercase kebab-case of the epic name;
never add a numeric suffix to hide a collision.

For every proposed `production/epics/[epic-slug]/EPIC.md` and for
`production/epics/index.md`, record:

- target path and whether it exists;
- SHA-256 of the exact current bytes, or `ABSENT`;
- identity found in the file (system ID, GDD path, module, and epic name);
- all index rows that refer to the same ID, GDD, epic name, or target slug; and
- whether the file contains only the recognized generated schema or also contains
  unknown/manual content.

Render the deterministic candidate bytes, including the index row changes. Preserve
the existing index `Last Updated` value when no row changes; a no-op rerun must not
manufacture an update by refreshing a date or reformatting unrelated rows. Then
classify each target as exactly one of:

| Class | Required evidence | Action |
|---|---|---|
| `create` | Target is absent and its ID, GDD, name, and slug have no collision in the index or filesystem. | Show the complete candidate file. |
| `no-op` | Existing bytes already equal the deterministic candidate and the index mapping is exact and unique. | Do not write or ask to overwrite. |
| `update` | Existing artifact has the same stable identity, uses only the recognized generated schema, has no unknown/manual content, and differs from the candidate. The index mapping is unique and compatible. | Show the complete unified diff and ask whether to update or skip this artifact. |
| `conflict` | Identity differs or is missing/ambiguous; another artifact or index row owns the ID/GDD/name/slug; the file has unknown sections or manual content; the index is contradictory; or the file cannot be read safely. | Stop the entire changeset with **BLOCKED**. Never overwrite, delete, rename, merge, or reinterpret the artifact. |

A legacy generated epic without `System ID` may be an `update` only when its
epic name, exact indexed GDD path, binding module, schema, and unique index row all
identify the same indexed system. Otherwise it is a `conflict`. User confirmation
is not permission to relabel a conflict as an update.

Present one inventory table for the requested scope:

```text
| Target | System ID | Preimage SHA-256 | Class | Evidence / action |
|---|---|---|---|---|
| production/epics/.../EPIC.md | SYS-... | [hash/ABSENT] | create/update/no-op/conflict | [...] |
```

For every `update`, show a unified diff against the recorded preimage and offer
`Update` or `Skip`. This is scope selection, not a second write authorization.
For `create`, show the complete proposed content. List `no-op` targets explicitly.
If any target is `conflict`, report the colliding identities and hashes and stop
before the producer gate or any write. Do not write non-conflicting siblings in
the same run; the previewed changeset must remain atomic in scope.

After update/skip choices, freeze the exact candidate bytes, selected path set,
and preimage hashes. If every target is `no-op` or skipped, finish
**COMPLETE — no changes required** without requesting write authorization.

---

## 4b. Producer Epic Structure Gate

**Review mode check** — apply before spawning PR-EPIC:
- `solo` → skip. Note: "PR-EPIC skipped — Solo mode." Proceed to Step 5 (write epic files).
- `lean` → skip (not a PHASE-GATE). Note: "PR-EPIC skipped — Lean mode." Proceed to Step 5 (write epic files).
- `full` → spawn as normal.

After all epics for the current layer are defined (Step 4 completed for all in-scope systems), and before writing any files, spawn `producer` through Codex subagent delegation using gate **PR-EPIC** (`.codex/docs/director-gates.md`).

Pass: the full epic structure summary (all epics, their scope summaries, governing ADR counts), the layer being processed, milestone timeline and team capacity.

Present the producer's assessment.

If UNREALISTIC: offer to revise epic boundaries (split overscoped or merge underscoped epics). Revise and re-run the gate before writing.

If CONCERNS, ask the user directly:
- Prompt: "Producer raised concerns about the epic structure. How do you want to proceed?"
- Options:
  - `[A] Proceed as planned — I accept the producer's concerns`
  - `[B] Revise epic boundaries — split or merge as recommended`
  - `[C] Stop — I want to reconsider the scope`

If [A]: proceed to Step 5.
If [B]: revise epic definitions from Step 4, re-render the candidates, repeat the complete Step 4a inventory/classification, and then re-run the producer gate.
If [C]: stop. Verdict: **BLOCKED** — user wants to reconsider epic scope.

Do not write epic files until the producer gate resolves.

---

## 5. Preview, Write, and Verify

Include only selected `create` and `update` targets in the complete changeset
preview. The preview must list every path, its classification, its recorded
preimage SHA-256, and its complete content or unified diff. If the bounded task
does not already authorize this exact changeset, obtain one explicit approval.
Never ask for authorization per file.

Immediately before the first mutation, re-read every selected target and the
index in one read-only pass:

- a `create` target must still be absent;
- an `update` target must still have the previewed preimage SHA-256; and
- the index must still have its previewed preimage SHA-256 or remain absent.

If any precondition changed, write nothing. Reclassify and re-preview the entire
changeset; a new conflict is **BLOCKED**, and any materially changed changeset
requires new authorization. Never continue with a partially stale preview.

After all preconditions pass, write only the authorized path set. Re-read each
result and verify its exact SHA-256 against the frozen candidate bytes. A failed
write or verification is **BLOCKED** and must report which files may have changed.

### `production/epics/[epic-slug]/EPIC.md`

```markdown
<!-- create-epics:managed-schema v1 -->
# Epic: [System Name]

> **System ID**: [stable system ID from systems-index]
> **Layer**: [Foundation / Core / Feature / Presentation]
> **GDD**: design/gdd/[filename].md
> **Architecture Module**: [binding module name]
> **Status**: Ready
> **Stories**: Not yet created — run `$create-stories [epic-slug]`

## Overview

[1 paragraph describing what this epic implements, derived from the selected GDD
Overview and the binding architecture module responsibilities]

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

### `production/epics/index.md`

Create the index if absent. When it exists, preserve unrelated rows byte-for-byte
and apply only the previewed unique row additions or managed-row updates.

```markdown
# Epics Index

Last Updated: [date]
Engine: [name + version]

| Epic | System ID | Layer | System | GDD | Stories | Status |
|------|-----------|-------|--------|-----|---------|--------|
| [name] | [stable-id] | Foundation | [system] | [file] | Not yet created | Ready |
```

---

## 6. Gate-Check Reminder

After writing all epics for the requested scope:

- **Foundation + Core complete**: These are required for the Pre-Production →
  Production gate. Run `$gate-check production` to check readiness.
- **Reminder**: Epics define scope. Stories define implementation steps. Run
  `$create-stories [epic-slug]` for each epic before developers can pick up work.

---

## Collaborative Protocol

1. **Index-authoritative scope** — only validated Approved rows from `systems-index.md` enter the run
2. **One epic at a time** — present each epic definition and record include/skip decisions before the changeset preview
3. **Warn on gaps** — flag untraced requirements before proceeding
4. **Conflict-safe reruns** — classify every target; never overwrite a conflict or manual content
5. **Single changeset approval** — preview every selected create/update together and write the set only after the one approval
6. **No invention** — all content comes from indexed GDDs, Accepted ADRs, and binding architecture statements
7. **Never create stories** — this skill stops at the epic level

After all requested epics are processed:

- **Verdict: COMPLETE** — [N] epic(s) created/updated and [M] no-op(s) verified. Run `$create-stories [epic-slug]` per changed or current epic.
- **Verdict: BLOCKED** — scope enumeration failed, a binding module is unavailable, an artifact conflict or preimage change exists, the user declined all epics, or no eligible systems were found.
