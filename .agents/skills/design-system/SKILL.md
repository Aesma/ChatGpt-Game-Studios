---
name: design-system
description: "Guided, section-by-section authoring or bounded revision of one system GDD, with author-only mutation boundaries and hash-bound independent review handoff."
---

## Invocation and author-only contract

Invoke this workflow as $design-system.

This is an authoring workflow for exactly one system GDD. It may write only:

- the target at design/gdd/<system-slug>.md; and
- its checkpoint at production/session-state/design-system-<system-slug>.yaml.

Treat those two paths as the complete maximum mutation set. Before the first
write, present both paths, the selected mode, the exact sections in scope, and the
intended changes; obtain one explicit changeset authorization. Section approvals
later in the workflow approve content, not additional filesystem scope. If the
mutation set or section scope expands, stop and obtain a new changeset
authorization before writing.

Never write or update systems-index.md, entities.yaml, a review record, a director
sign-off, an ADR, an engine-reference document, or any other file. Never run an
inline approval gate and never label this workflow's own output Approved.
Registry/index recording and formal approval are separate responsibilities that
consume hash-bound evidence after this authoring task stops.

Arguments:

    <system-name-or-gdd-path>
    [--mode new|resume|fill-gaps|revise-section]
    [--section "<required-section>"]

The review depth is deliberately not an authoring argument. Formal review occurs
once against the whole artifact in an independent task.

## 1. Resolve target and explicit mode

A system name or a direct child Markdown path under design/gdd/ is required. If
it is missing, read systems-index.md only to suggest the highest-priority system
whose status is Not Started, then ask whether to use that name. Do not update the
index.

Normalize a name to a lowercase kebab-case slug. Reject an empty slug, path
separators, dot segments, reserved project-document names, or any path whose
resolved direct parent is not design/gdd/. Never use game-concept.md,
systems-index.md, a review report, or a template as the target. If normalization
collides with a different existing document, return ERROR — TARGET COLLISION and
ask the user for the intended existing path or another name.

Resolve the mode before reading authoring context:

| Mode | Preconditions | Permitted GDD mutation |
|---|---|---|
| new | Target does not exist | Create the skeleton, then fill approved sections |
| resume | Target and matching checkpoint exist; checkpoint is unfinished | Continue only checkpoint sections that are pending or approved-not-written |
| fill-gaps | Target exists | Fill only required sections that are missing, empty, or placeholder-only |
| revise-section | Target exists and --section names exactly one required section | Replace only that substantive section after a new user decision and approval |

If the target does not exist and no mode was supplied, new may be selected. If
the target exists and no mode was supplied, do not infer intent. Show the target
and ask the user to choose resume, fill-gaps, revise-section, or stop.

Retrofit is not a mode or alias. If the user says retrofit, ask them to choose:

- fill-gaps — preserves every substantive existing section; or
- revise-section — intentionally replaces one named substantive section.

Reject new for an existing target and reject every other mode for a missing
target. revise-section requires exactly one canonical section name:
Overview, Player Fantasy, Detailed Rules, Formulas, Edge Cases, Dependencies,
Tuning Knobs, or Acceptance Criteria.

Before any existing-file edit, compute its SHA-256 as base_sha256. resume also
requires target path and current hash to match the checkpoint. A mismatch returns
ERROR — STALE CHECKPOINT and makes no write.

## 2. Load bounded design context

Read applicable AGENTS.md files from the repository root through design/gdd/, in
order. Then read:

- design/gdd/game-concept.md; fail with BLOCKED if absent;
- design/gdd/systems-index.md; fail with BLOCKED if absent;
- the target GDD for every mode except new;
- design/registry/entities.yaml, if present, as read-only claims/evidence; and
- only first-level dependency GDDs explicitly named for the target in the systems
  index, plus pillar documents directly linked by the game concept.

Do not update any context source. Do not scan thematically related GDDs. Treat a
registry value as a claim with source evidence, not as an automatically locked
product decision. If a target draft would contradict a registry claim, surface
that conflict before a GDD write and require an owner/user decision.

### Design/technology boundary

Do not load architecture ADRs, engine modules, breaking-change notes, technical
preferences, or implementation documents into the GDD authoring context. A
system GDD may contain only player-visible behavior and fantasy, product rules,
formula semantics, boundary outcomes, design-facing dependencies, tuning intent,
and observable acceptance conditions.

When an implementation choice, engine capability, API, class/data structure,
persistence representation, synchronization strategy, technical performance
strategy, or ADR question appears:

1. do not put it in the GDD;
2. add a typed handoff entry under technical_handoffs in the authorized
   checkpoint;
3. use destination ADR/TECH;
4. record source evidence and whether it is constraint-to-verify or
   decision-needed; and
5. continue only if the product rule can be decided without choosing the
   implementation.

If the unresolved technical point prevents a product rule from being specified,
mark the affected section blocked in the checkpoint and stop. A later technical
workflow resolves it; this workflow does not create or edit the sidecar or ADR.

Present a short context summary that separates:

- product decisions already made by the user or an authoritative GDD;
- dependency assumptions that are provisional;
- read-only registry claims that need preflight comparison; and
- ADR/TECH handoffs, which will not be written into the GDD.

Ask whether the user is ready to proceed. If not, stop without writing.

## 3. Inspect sections and authorize the changeset

The eight required sections are:

1. Overview
2. Player Fantasy
3. Detailed Rules
4. Formulas
5. Edge Cases
6. Dependencies
7. Tuning Knobs
8. Acceptance Criteria

For fill-gaps, classify each required section before authorization as substantive,
missing, empty, or placeholder-only. Present the inventory and scope only
missing, empty, and placeholder-only sections. Never reinterpret weak but
substantive content as a gap; use revise-section when the user wants to replace
it.

For revise-section, show the selected section's current body and hash, explain
that only that section will be replaced, and obtain a new product decision before
drafting. Other sections are out of scope even if incomplete.

For resume, read section states from the checkpoint and verify them against the
current GDD. Written substantive content wins over a stale pending marker, but a
hash mismatch remains an error. Resume at the first scoped pending section and
do not re-discuss completed sections.

Present one changeset authorization:

    Mode: <mode>
    Target GDD: design/gdd/<system-slug>.md
    Checkpoint: production/session-state/design-system-<system-slug>.yaml
    Sections allowed to change: <exact list>
    Status-header transitions allowed: stale Approved -> In Design on first content mutation; In Design -> In Review only after whole-artifact validation
    Other writes: none

Do not write until the user authorizes this complete boundary.

### New-mode skeleton

After authorization in new mode, create this skeleton atomically:

    # <System Name>

    > **Status**: In Design
    > **Decision Owner**: <user or named product owner>
    > **Last Updated**: <date>
    > **Implements Pillar**: <pillar or "Unassigned">

    ## Overview

    [To be designed]

    ## Player Fantasy

    [To be designed]

    ## Detailed Rules

    [To be designed]

    ## Formulas

    [To be designed]

    ## Edge Cases

    [To be designed]

    ## Dependencies

    [To be designed]

    ## Tuning Knobs

    [To be designed]

    ## Acceptance Criteria

    [To be designed]

The skeleton has exactly the eight required sections. Optional material may be
added later only as substantive approved content; never leave optional
placeholders in a document declared ready for review.

Create or update the authorized checkpoint after the skeleton or existing-target
validation. Use this schema:

    schema: design-system-checkpoint/v2
    target: design/gdd/<system-slug>.md
    mode: new | resume | fill-gaps | revise-section
    base_sha256: <hash before this run, or null for new>
    current_sha256: <hash of current target bytes>
    mutation_scope:
      - design/gdd/<system-slug>.md
      - production/session-state/design-system-<system-slug>.yaml
    scoped_sections:
      - <canonical section>
    section_states:
      <canonical key>: pending | drafting | approved-not-written | written | blocked | out-of-scope
    technical_handoffs: []
    approved_drafts: {}
    status: authoring | partial | ready-for-independent-review | blocked
    review_handoff:
      required: true
      target_sha256: null

The checkpoint is continuity state, not approval evidence. It must never claim a
formal review verdict.

---

## Required continuation

Before continuing, read references/continued-workflow.md in full. It contains the
section transaction, mode-specific mutation rules, content validation, independent
review handoff, recorder contract, and recovery behavior; follow it in order.
