---
name: quick-design
description: "Create an independent lightweight design spec for a small tuning change, minor mechanic, or tightly scoped addition."
---

## Invocation and execution

Invoke this workflow as `$quick-design`.

Before the first file change, present the complete proposed changeset, listing every file and intended modification, and obtain one explicit approval. After approval, make all changes within that boundary continuously without asking again file by file. If the scope expands materially, stop, present the revised changeset, and obtain one new approval.

Arguments: `[brief description of the change]`. Treat bracketed values as optional unless the workflow says otherwise.


# Quick Design

This is the **lightweight design path** for changes that don't need a full GDD.
Full GDD authoring via `$design-system` is the heavyweight path. Use this skill
for work under approximately 4 hours of implementation — tuning adjustments,
minor behavioral tweaks, small additions to existing systems, or standalone
features too small to warrant a full document.

**Output:** `design/quick-specs/[name]-[date].md`

**When to run:** Anytime a change is too small for `$design-system` but too
meaningful to implement without a written rationale.

---

## 1. Classify the Change

First, read the argument and determine which category this change falls into:

- **Tuning** — changing numbers or balance values in an existing system with no
  behavioral change (most minimal path). Example: "increase jump height from 5
  to 6 units", "reduce enemy patrol speed by 10%".
- **Tweak** — a small behavioral change to an existing system that introduces no
  new states, branches, or systems. Example: "make dash invincible on frame 1",
  "allow combo to cancel into roll".
- **Addition** — adding a small mechanic to an existing system that may introduce
  1-2 new states or interactions. Example: "add a parry window to the block
  mechanic", "add a charge variant to the basic attack".
- **New Small System** — a standalone feature small enough that it has no
  existing GDD, fits within approximately 4 hours of implementation, requires
  no systems-index entry, and creates no significant cross-system contract.
  Example: "achievement popup system", "simple day/night visual cycle".

Before drafting, redirect to `$design-system` if the change is likely to exceed
approximately 4 hours of implementation, introduces a significant cross-system
contract, changes core system rules, or adds a system that belongs in
`design/gdd/systems-index.md`. These are hard scope boundaries regardless of the
selected category. Determine the systems-index requirement during this phase,
not after drafting.

If there is no argument, ask the user to describe the change (plain text prompt), then classify it using the criteria above.

Present the inferred classification by asking the user directly:
- Prompt: "I've classified this as **[inferred type]** — [brief reason]. Is that correct?"
- Options:
  - `[A] Yes — [inferred type] is correct`
  - `[B] Tuning — changing numbers or balance values only`
  - `[C] Tweak — small behavioral change to an existing system`
  - `[D] Addition — adding a small mechanic to an existing system`
  - `[E] New Small System — standalone feature, approximately 4 hours or less, no index entry`
  - `[F] This is too large — redirect me to $design-system`

If [F], or if the selected type still crosses any hard boundary above: stop.
Verdict: **REDIRECTED** — use `$design-system` for this change. Otherwise:
proceed with the selected type.

---

## 2. Context Scan

Before drafting anything:

- Search `design/gdd/` by explicit system reference, exact slug, and title.
  List candidate paths. Read the uniquely relevant GDD sections; if more than
  one candidate remains, ask the user to select one rather than choosing by
  filename similarity.
- Check whether `design/gdd/systems-index.md` exists. If it does, read it to
  understand where this system sits in the dependency graph and what tier it
  belongs to. If it does not exist, note "No systems index found — skipping
  dependency tier check." and continue.
- Read `docs/technical-preferences.md` and
  `docs/architecture/control-manifest.md` when present to determine the project's
  selected data/config format and constraints. If no format is configured and
  existing data files do not establish one, record the format as "TBD — user
  decision" instead of choosing JSON.
- Check `design/quick-specs/` for prior specs that touched this system. List the
  candidates and compare their relevant rules. If an unresolved contradiction
  remains, surface it and do not claim `COMPLETE` until the user resolves it.
- If this is a Tuning change, also check `assets/data/` for the existing data
  file and format that hold the relevant values.

Report the selected GDD and section, the data format source, prior specs checked,
and any unresolved conflicts.

---

## 3. Draft the Quick Design Spec

Use the appropriate spec format for the change category.

### For Tuning changes

Produce a single table:

```markdown
# Quick Design Spec: [Title]

**Type**: Tuning
**System**: [System name]
**GDD Reference**: `design/gdd/[filename].md` — Tuning Knobs section
**Date**: [today]

## Change

| Parameter | Old Value | New Value | Rationale |
|-----------|-----------|-----------|-----------|
| [param]   | [old]     | [new]     | [why]     |

## Tuning Knob Mapping

Maps to GDD Tuning Knob: [knob name and its documented range].
New value is [within / at the edge of / outside] the documented range.
[If outside: explain why the range should be extended.]

## Acceptance Criteria

- [ ] [Parameter] reads [new value] from `[existing project data path]`
- [ ] Behavior difference is observable in [specific context]
- [ ] No regression in [related behavior]
```

### For Tweak and Addition changes

```markdown
# Quick Design Spec: [Title]

**Type**: [Tweak / Addition]
**System**: [System name]
**GDD Reference**: `design/gdd/[filename].md`
**Date**: [today]

## Change Summary

[1-2 sentences describing what changes and why.]

## Motivation

[Why is this change needed? What player experience problem does it solve?
Reference the relevant MDA aesthetic or player feedback if applicable.]

## Design Delta

Current GDD says (quoting `design/gdd/[filename].md`, [section]):

> [exact quote of the relevant rule or description]

This spec changes that to:

[New rule or description, written with the same precision as a GDD Detailed
Rules section. A programmer should be able to implement from this text alone.]

## New Rules / Values

[Full unambiguous statement of the replacement content. If this introduces
new states, list them. If it introduces new parameters, define their ranges.]

## Affected Systems

| System | Impact | Action Required |
|--------|--------|-----------------|
| [system] | [how it is affected] | [update GDD / update data file / no action] |

## Acceptance Criteria

- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]
- [ ] No regression: [the original behavior this must not break]

## GDD Update Required?

[Yes / No]
[When required: which file, which section, and what the update should say.]
```

### For New Small System changes

Use a trimmed GDD structure. Include only the sections that are directly
necessary — skip Player Fantasy, full Formulas, and Edge Cases unless the
system specifically requires them.

```markdown
# Quick Design Spec: [Title]

**Type**: New Small System
**Scope**: [1-2 sentence description of what this system does and doesn't do]
**Date**: [today]
**Estimated Implementation**: [hours]

## Overview

[One paragraph a new team member could understand. What does this system do,
when does it activate, and what does it produce?]

## Core Rules

[Unambiguous rules for the system. Use numbered lists for sequential behavior
and bullet lists for conditions. Be precise enough that a programmer can
implement without asking questions.]

## Tuning Knobs

| Knob | Default | Range | Category | Rationale |
|------|---------|-------|----------|-----------|
| [name] | [value] | [min–max] | [feel/curve/gate] | [why this default] |

Store values in the existing project-selected data/config format and path. If
the project has not selected a format, write `TBD — user decision`; do not
default to JSON or hardcode values.

## Acceptance Criteria

- [ ] [Functional criterion: does the right thing]
- [ ] [Functional criterion: handles the edge case]
- [ ] [Experiential criterion: feels right — what a playtest validates]
- [ ] [Regression criterion: does not break adjacent system]

## Systems Index

This system is below the existing systems-index tracking threshold; otherwise
the workflow would have redirected in Phase 1.
```

---

## 4. Approval and Filing

Present the draft to the user in full. Then ask the user directly:
- Prompt: "Here's the Quick Design Spec draft. How do you want to proceed?"
- Options:
  - `[A] Approve — write it as shown`
  - `[B] Revise — I'll describe what to change`
  - `[C] This grew too large — redirect to $design-system instead`

If [B]: collect the requested changes, revise the draft, and re-present this structured prompt.
If [C]: stop. Verdict: **REDIRECTED** — use `$design-system` for this change.

If [A]: determine the target quick-spec path, then check whether that exact file
already exists. If it exists, read and show the current content and offer only a
targeted update or stop; do not overwrite it or invent a new version name. Add
the chosen create/update to the complete changeset preview and obtain the one
changeset authorization before writing.

Use today's date in the filename. The title should be a kebab-case description
of the change (e.g., `jump-height-tuning-2026-03-10`,
`parry-window-addition-2026-03-10`).

This workflow writes only the quick spec. If a GDD update is required, record
the target file, section, and required delta under `GDD Update Required?`, but
do not edit the GDD. If the change cannot be implemented without changing core
rules or a cross-system contract, return to the Phase 1 boundary and end as
**REDIRECTED**.

---

## 5. Handoff

After writing the file, search existing story metadata and references for a
story that already cites the new spec.

- If exactly one story references it, report that path and offer
  `$story-readiness [story-path]` and then `$dev-story [story-path]` as later
  commands.
- If no story references it, report only the spec path and state that a story
  must cite it before story-readiness or implementation.
- If multiple stories reference it, list them and let the user choose later;
  do not assume an implementation target.

Always output:

```
Quick Design Spec written to: design/quick-specs/[filename].md
Type: [Tuning / Tweak / Addition / New Small System]
System: [system name]
GDD update: [Required — not applied by this workflow / Not required]
Story handoff: [existing story path / no referencing story found / candidates]
```

### Pipeline Notes

Verdict: **COMPLETE** — quick design spec written.

Quick Design Specs **bypass** `$design-review` and `$review-all-gdds` by
design. They are for small, low-risk, well-scoped changes where the cost of
the full review pipeline exceeds the risk of the change itself.

Redirect to the full pipeline if any of the following are true:
- The change adds a new system that belongs in the systems index
- The change significantly alters cross-system behavior or a system's
  contracts with other systems
- The change introduces new player-facing mechanics that affect the
  game's MDA aesthetic balance
- Implementation is likely to exceed one week of work

In those cases: "This change has grown beyond quick-spec scope. I recommend
using `$design-system` to author a full GDD for this."

---

## Recommended Next Steps

- When an existing story references this spec, run `$story-readiness [story-path]`
  before implementation, followed by `$dev-story [story-path]` after readiness passes.
- If no story references the spec, report the spec path; do not claim it is
  implementation-ready.
- If the change is larger than expected, run `$design-system [system-name]` to
  author a full GDD instead.
