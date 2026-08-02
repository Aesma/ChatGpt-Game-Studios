---
name: ux-review
description: "Validates a UX spec, HUD design, or interaction pattern library for completeness, accessibility compliance, GDD alignment, and implementation readiness. Produces APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED verdict with specific gaps."
---

## Invocation and execution

Invoke this workflow as `$ux-review`.

Arguments: `[file-path or 'all' or 'hud' or 'patterns']`. Treat bracketed values as optional unless the workflow says otherwise.

Delegate substantive work to the `ux-designer` Codex subagent role when it is available. If that role is unavailable, follow the same responsibilities in the current agent.


## Overview

Validates UX design documents before they enter the implementation pipeline.
Acts as the quality gate between UX Design and Visual Design/Implementation in
the `$team-ui` pipeline.

**Run this skill:**
- After completing a UX spec with `$ux-design`
- Before handing off to `ui-programmer` or `art-director`
- Before the Pre-Production to Production gate check (which requires key screens
  to have reviewed UX specs)
- After major revisions to a UX spec

**Verdict levels:**
- **APPROVED** — spec is complete, consistent, and implementation-ready
- **NEEDS REVISION** — specific gaps found; fix before handoff but not a full redesign
- **MAJOR REVISION NEEDED** — fundamental issues with scope, player need, or
  completeness; needs significant rework

---

## Phase 1: Parse Arguments

- **Specific file path** (e.g., `$ux-review design/ux/inventory.md`): validate
  that one document
- **`all`**: find all files in `design/ux/` and validate each
- **`hud`**: validate `design/ux/hud.md` specifically
- **`patterns`**: validate `design/ux/interaction-patterns.md` specifically
- **No argument**: ask the user which spec to validate

Route each file before review. The two reserved paths are `design/ux/hud.md` (HUD) and `design/ux/interaction-patterns.md` (pattern library). Any other candidate must match the header contract of `.codex/docs/templates/ux-spec.md`; otherwise report it as unsupported and issue no verdict. `all` reviews and summarizes only these three supported types, with unsupported Markdown listed separately.

---

## Phase 2: Load Cross-Reference Context

Before validating any spec, load the authoritative template for its routed type: `.codex/docs/templates/ux-spec.md`, `.codex/docs/templates/hud-design.md`, or `.codex/docs/templates/interaction-pattern-library.md`. Its current headings and requirements are the completeness contract; do not maintain a second copied section schema.

Then load:

1. **Input & Platform config**: Read `docs/technical-preferences.md` and
   extract `## Input & Platform`. This is the authoritative source for which input
   methods the game supports — use it to drive the Input Method Coverage checks in
   Phase 3A, not the spec's own header. If unconfigured, fall back to the spec header.
2. The accessibility tier committed to in `design/accessibility-requirements.md`. This central document is the only tier authority. If it is missing or still placeholder, report `tier unknown` and do not claim COMPLIANT. If the spec header differs from its committed tier, record a blocker. Use only Basic / Standard / Comprehensive / Exemplary; never guess a mapping for legacy names.
3. The interaction pattern library at `design/ux/interaction-patterns.md` (if
   it exists)
4. The GDDs referenced in the spec's header (read their UI Requirements sections)
5. The player journey map at `design/player-journey.md` (if it exists) for
   context-arrival validation

---

## Phase 3: Template-Routed Validation

For each supported file, compare it against the current authoritative template selected in Phase 1. Check every required heading and substantive placeholder, then apply the quality rules described by that same template.

- **UX spec**: validate purpose/player need, arrival context, navigation and entry/exit, layout/component inventory, applicable states, interactions for configured inputs, data ownership, accessibility, localization, and acceptance criteria.
- **HUD**: validate the HUD template's information architecture, applicable gameplay contexts, layout zones, element specs, feedback, visual budget, platform adaptation, tuning knobs, accessibility, and acceptance criteria.
- **Pattern library**: validate the pattern template's catalog and entries, standard controls actually used by the project, navigation/loading/error patterns, animation/sound standards, accessibility, and internal consistency.

Count a template heading as present only when it contains substantive non-placeholder content. An unsupported document receives an error but no completeness denominator or verdict.
## Phase 4: Output the Verdict

```markdown
## UX Review: [Document Name]
**Date**: [date]
**Reviewer**: ux-review skill
**Document**: [file path]
**Platform Target**: [from header]
**Accessibility Tier**: [from header or accessibility-requirements.md]

### Completeness: [X/Y sections present]
- [x] Purpose & Player Need
- [ ] States & Variants — MISSING: error state not documented

### Quality Issues: [N found]
1. **[Issue title]** [BLOCKING / ADVISORY]
   - What's wrong: [specific description]
   - Where: [section name]
   - Fix: [specific action to take]

### GDD Alignment: [ALIGNED / GAPS FOUND]
- GDD [name] UI Requirements — [X/Y requirements covered]
- Missing: [list any uncovered GDD requirements]

### Accessibility: [COMPLIANT / GAPS / NON-COMPLIANT]
- Target tier: [tier]
- [list specific accessibility findings]

### Pattern Library: [CONSISTENT / INCONSISTENCIES FOUND]
- [findings]

### Verdict: APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED
**Blocking issues**: [N] — must be resolved before implementation
**Advisory issues**: [N] — recommended but not blocking

Verdict mapping is deterministic:
- **APPROVED**: zero blockers. Advisory findings do not lower the verdict.
- **NEEDS REVISION**: one or more localized, fixable blockers with the document's purpose, main flow, input contract, and data ownership otherwise coherent.
- **MAJOR REVISION NEEDED**: Purpose/Player Need is missing; the main flow, input behavior, or data ownership contradicts itself; or multiple core sections from the routed template are substantively missing.

Always list blocker count and locations. Then use the matching handoff:

[For APPROVED]: This spec is ready for handoff to `$team-ui` Phase 2
(Visual Design).

[For NEEDS REVISION]: Address the [N] blocking issues above, then re-run
`$ux-review`.

[For MAJOR REVISION NEEDED]: The spec has fundamental gaps in [areas].
Recommend returning to `$ux-design` to rework [sections].
```

---

## Phase 5: Collaborative Protocol

This skill is READ-ONLY — it never edits or writes files. It reports findings only.

After delivering the verdict:
- For **APPROVED**: suggest running `$team-ui` to begin implementation coordination
- For **NEEDS REVISION**: offer to help fix specific gaps ("Would you like me to
  help draft the missing error state?") — but do not auto-fix; wait for user
  instruction
- For **MAJOR REVISION NEEDED**: suggest returning to `$ux-design` with the
  specific sections to rework

Never block the user from proceeding — the verdict is advisory. Document risks,
present findings, let the user decide whether to proceed despite concerns. A user
who chooses to proceed with a NEEDS REVISION spec takes on the documented risk.
