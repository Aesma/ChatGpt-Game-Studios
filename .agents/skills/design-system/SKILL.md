---
name: design-system
description: "Guided, section-by-section authoring or bounded revision of one system GDD, with versioned content checks, bounded evidence, and hash-bound independent review handoff."
---

## Invocation and author-only contract

Invoke this workflow as $design-system.

This is an authoring workflow for exactly one system GDD. It may write only:

- the target at design/gdd/<system-slug>.md; and
- its checkpoint at production/session-state/design-system-<system-slug>.yaml.

Treat those two paths as the complete maximum mutation set. Before the first
write, present both paths, the selected mode, the exact sections in scope, and
the intended changes; obtain one explicit changeset authorization. Section
approvals later in the workflow approve content, not additional filesystem
scope. If the mutation set or section scope expands, stop and obtain a new
changeset authorization before writing.

Never write or update systems-index.md, entities.yaml, a review record, a
director sign-off, an ADR, an engine-reference document, or any other file.
Never run an inline approval gate and never label this workflow's own output
Approved. Registry/index recording and formal approval are separate
responsibilities that consume hash-bound evidence after this authoring task
stops.

Arguments:

    <system-name-or-gdd-path>
    [--mode new|resume|fill-gaps|revise-section]
    [--section "<canonical-section>"]

The review depth is deliberately not an authoring argument. Formal review
occurs once against the whole artifact in an independent task.

This workflow validates content with content profile system-gdd/v2 and persists
continuity only in design-system-checkpoint/v3. A document created in new mode
declares the profile in its header. An existing unmarked document is validated
through the same profile without silently changing unrelated header bytes.

## 1. Resolve target and explicit mode

A system name or a direct child Markdown path under design/gdd/ is required. If
it is missing, read systems-index.md only to suggest the highest-priority system
whose status is Not Started, then ask whether to use that name. Do not update
the index.

Normalize a name to a lowercase kebab-case slug. Reject an empty slug, path
separators, dot segments, reserved project-document names, or any path whose
resolved direct parent is not design/gdd/. Never use game-concept.md,
systems-index.md, a review report, or a template as the target. If
normalization collides with a different existing document, return
ERROR — TARGET COLLISION and ask the user for the intended existing path or
another name.

Resolve the mode before loading authoring context:

| Mode | Preconditions | Permitted GDD mutation |
|---|---|---|
| new | Target does not exist | Create the skeleton, then fill the eight approved required sections |
| resume | Target and matching unfinished v3 checkpoint exist | Continue the checkpoint's original authorized scope under its origin mode |
| fill-gaps | Target exists | Fill only required sections classified missing, empty, or placeholder-only at the authorized baseline |
| revise-section | Target exists and --section names one supported section | Replace one substantive required section, or add/revise one supported optional section |

If the target does not exist and no mode was supplied, new may be selected. If
the target exists and no mode was supplied, do not infer intent. Show the target
and ask the user to choose resume, fill-gaps, revise-section, or stop.

Retrofit is not a mode or alias. If the user says retrofit, ask them to choose:

- fill-gaps — preserves every substantive existing section; or
- revise-section — intentionally changes one named section.

Reject new for an existing target and every other mode for a missing target.
The eight required canonical sections are:

1. Overview
2. Player Fantasy
3. Detailed Rules
4. Formulas
5. Edge Cases
6. Dependencies
7. Tuning Knobs
8. Acceptance Criteria

The supported optional sections are Visual/Audio Requirements, UI Requirements,
and Open Questions. New and fill-gaps never auto-create optional sections.
revise-section may add or revise exactly one supported optional section only
when that section is named in the authorized scope.

Before any existing-file edit, compute its SHA-256 as base_sha256. Resume
requires target path and current hash to match a v3 checkpoint whose status is
authoring or partial. A target/path/hash mismatch returns
ERROR — STALE CHECKPOINT with zero writes. A v1 or v2 checkpoint lacks the
origin-mode, context, and section-baseline evidence needed for safe continuation; return
ERROR — UNSUPPORTED CHECKPOINT SCHEMA with zero writes and offer a newly
authorized fill-gaps or revise-section run.

Resume is an invocation mode, not new mutation authority. Preserve
checkpoint.origin_mode, authorized_scope, and baseline hashes, set only
invocation_mode to resume, and enforce the origin mode's mutation predicate.

## 2. Inventory sections and authorize the changeset

Read applicable AGENTS.md files from repository root through design/gdd/ before
interpreting the target. For an existing target, read it in full, compute its
hash, reject duplicate canonical headings, and inventory sections using
system-gdd/v2.

Each inventory entry keeps three independent axes:

- requirement: required or optional;
- applicability: applicable, not-applicable, or undecided; and
- content_state: missing, empty, placeholder-only, substantive, or
  not-applicable.

Workflow progress is separate:

    pending | drafting | approved-not-written | written | blocked | out-of-scope

not-applicable is approved substantive content, not an empty section or a token
such as N/A. It is permitted only for Formulas, Dependencies, Tuning Knobs, and
the supported optional sections. Its body must explain why the section does not
apply and the resulting observable design consequence. Overview, Player
Fantasy, Detailed Rules, Edge Cases, and Acceptance Criteria are always
applicable.

For fill-gaps, scope only required sections whose baseline content_state is
missing, empty, or placeholder-only. Weak but substantive content is not a gap;
use revise-section to change it.

For revise-section, show the selected current body and body SHA-256. A required
section must be substantive; use fill-gaps for a required gap. A supported
optional section may be substantive, missing, empty, or placeholder-only because
its explicit selection is the authority to add or replace it. All other sections
remain out of scope.

For resume, obtain scope, origin mode, section inventory, and baseline hashes
from the matching v3 checkpoint. Verify written sections against the target.
Substantive written content wins over a stale pending marker, but any target or
baseline mismatch remains an error. Do not re-discuss written sections.

Present one changeset authorization:

    Invocation mode: <new|resume|fill-gaps|revise-section>
    Origin mode: <new|fill-gaps|revise-section>
    Content profile: system-gdd/v2
    Target GDD: design/gdd/<system-slug>.md
    Checkpoint: production/session-state/design-system-<system-slug>.yaml
    Sections allowed to change: <exact canonical list>
    Header changes allowed: profile declaration for new; stale status demotion
      on first content mutation; In Review only after whole-artifact validation
    Other writes: none

Do not load the broader authoring context or write until the user authorizes
this complete boundary.

## 3. Load bounded, hash-manifested design context

After changeset authorization, construct candidates in this stable order:

1. applicable AGENTS.md files from root through design/gdd/;
2. the existing target, when present;
3. design/gdd/game-concept.md;
4. design/gdd/systems-index.md;
5. design/registry/entities.yaml, when present;
6. first-level dependency GDDs in systems-index order; and
7. pillar documents in their game-concept link order.

game-concept.md and systems-index.md are mandatory. Fail BLOCKED if either is
absent. Do not scan thematically related GDDs or follow second-level links.

The complete loaded context, including AGENTS.md and the target, is limited to:

- at most 12 files; and
- at most 524288 bytes.

Determine candidate sizes before content loading. Never partially read or
truncate a file to fit. Record every loaded path, role, byte length, and SHA-256;
record every omitted candidate with its role, byte length, and reason. Compute a
SHA-256 digest over the ordered manifest records.

If a mandatory or selected linked candidate would exceed either limit, write at
most the already-authorized checkpoint with status partial and reason
CONTEXT_BUDGET_EXCEEDED, leave the GDD unchanged, report the loaded and omitted
lists, and stop. Required context is never silently omitted.

Do not update a context source. The registry is read-only claim evidence, not an
automatically locked source of product truth. Record its file hash and classify
each relevant claim:

- current-owner-evidence — evidence is schema-valid, names an external owner,
  and its source path, source hash, and value agree;
- target-owned-change-candidate — the target owns the current claim and a newly
  approved target decision may later require a recorder update;
- external-owner-conflict — current external-owner evidence contradicts the
  proposed target rule;
- stale — the cited source or source hash no longer supports the claim;
- legacy-unverified — the registry schema lacks hash-bound ownership evidence;
  or
- malformed — required claim fields are invalid.

Legacy-unverified, stale, and malformed claims must be surfaced but cannot
silently become hard constraints. A target-owned change produces only a
registry_handoffs entry in the checkpoint. An external-owner conflict blocks the
section until the owning GDD is resolved; this author does not change either
external source.

### Design and technology boundary

Do not load architecture ADRs, engine modules, breaking-change notes, technical
preferences, or implementation documents into the GDD authoring context. A
system GDD may contain only player-visible behavior and fantasy, product rules,
formula semantics, boundary outcomes, design-facing dependencies, tuning
intent, and observable acceptance conditions.

When an implementation choice, engine capability, API, class/data structure,
persistence representation, synchronization strategy, technical performance
strategy, or ADR question appears:

1. do not put it in the GDD;
2. add a typed technical_handoffs entry in the authorized checkpoint;
3. use destination ADR/TECH;
4. record source evidence and decision-needed or constraint-to-verify; and
5. continue only when the product rule can be decided without the implementation.

If the technical point prevents a product rule from being specified, mark the
affected section blocked, set checkpoint status blocked, and stop.

Present a short context summary separating user/authoritative product decisions,
provisional dependency assumptions, registry claim classes, evidence-backed
constraints, derived design constraints, and ADR/TECH handoffs. Ask whether the
user is ready to proceed. If not, stop without changing the GDD.

### New-mode skeleton

Only after context succeeds, create this skeleton atomically in authorized new
mode:

    # <System Name>

    > **Status**: In Design
    > **Document Schema**: system-gdd/v2
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

The skeleton has exactly the eight required sections and no optional
placeholders.

Create or update only the authorized checkpoint. Its required shape is:

    schema: design-system-checkpoint/v3
    content_profile: system-gdd/v2
    target: design/gdd/<system-slug>.md
    origin_mode: new | fill-gaps | revise-section
    invocation_mode: new | resume | fill-gaps | revise-section
    base_sha256: <pre-run target hash or null>
    baseline_target_sha256: <authorized target hash or null for new>
    current_sha256: <current target hash or null before new skeleton>
    baseline_section_sha256: {}
    mutation_scope:
      - design/gdd/<system-slug>.md
      - production/session-state/design-system-<system-slug>.yaml
    authorized_scope:
      - <canonical section>
    section_inventory:
      <canonical section>:
        requirement: required | optional
        applicability: applicable | not-applicable | undecided
        content_state: missing | empty | placeholder-only | substantive | not-applicable
        workflow_state: pending | drafting | approved-not-written | written | blocked | out-of-scope
        validation_failures: []
        decision_ids: []
    context_manifest:
      max_files: 12
      max_bytes: 524288
      total_files: 0
      total_bytes: 0
      files: []
      omitted: []
      manifest_sha256: null
    registry_snapshot:
      path: design/registry/entities.yaml
      sha256: null
      schema: absent
      claims: []
    decision_records: []
    consultations: []
    technical_handoffs: []
    registry_handoffs: []
    approved_drafts: {}
    status: authoring | partial | ready-for-independent-review | blocked
    reason: null
    review_handoff:
      required: true
      target_sha256: null
      content_profile: system-gdd/v2
      context_manifest_sha256: null
      invalidated_target_sha256: null
      invalidation_reason: null

The checkpoint is continuity and provenance state, not approval evidence. It
must never claim a formal review verdict.

## P1 audit traceability

Each authoritative P1 audit finding has one independent trace row. A row records
where the remediation is normative and which dedicated-spec case/assertion checks
it; the matrix is traceability only and does not claim that any case was run.

| Audit ID | Normative clause | Dedicated spec evidence |
|---|---|---|
| `DSG-005` | Section 2 plus `references/continued-workflow.md` Section 5, `system-gdd/v2 content assertions` | Case 9 — assertions `Eight sections have explicit content assertions` and `Any failure blocks In Review` |
| `DSG-006` | Section 3, `Load bounded, hash-manifested design context` | Case 10 — assertions `Both numeric limits are enforced` and `Required context is not silently omitted` |
| `DSG-007` | Section 3 registry snapshot/claim classification | Case 11 — assertions `Six claim classes are defined` and `Registry is never edited` |
| `DSG-008` | `references/continued-workflow.md` Sections 4c–4d, semantic then transactional preflight | Case 11 — assertions `Semantic claim comparison precedes approval` and `Transaction preflight re-hashes registry/evidence` |
| `DSG-009` | `references/continued-workflow.md` Section 6, specialist consultation boundary and failure schema | Case 12 — assertions `Complete/partial/timeout/failed/skipped states exist` and `Missing specialist output is not invented` |
| `DSG-010` | Section 2 section inventory plus `references/continued-workflow.md` Section 5 optional material | Case 13 — assertions `Optional absence is not a gap` and `Exactly three supported optional names exist` |
| `DSG-011` | `references/continued-workflow.md` Section 4a, decision classification | Case 14 — assertions `Exactly four decision classes exist` and `Derived constraint preserves derivation` |
| `DSG-012` | Section 1 explicit modes plus `references/continued-workflow.md` Section 9 recovery/resume | Cases 4 and 15 — assertions `Missing checkpoint makes resume unavailable` and `Resume never broadens permission` |
| `DSG-013` | `references/continued-workflow.md` Sections 4e and 8, review invalidation and independent recorder handoff | Case 16 — assertions `Prior evidence is not copied to changed bytes` and `Stale target/context cannot authorize Approved` |
| `DSG-014` | This trace matrix and the required dedicated specification boundary | Case 17 — assertions `Three validation axes are separate`, `Failures/unexecuted checks are not hidden`, and `Current hashes are required for registration` |

---

## Required continuation

Before continuing, read references/continued-workflow.md in full. It contains
the decision taxonomy, semantic and transactional preflights, section
transactions, content assertions, consultation limits, validation, independent
review handoff, and recovery behavior; follow it in order.
