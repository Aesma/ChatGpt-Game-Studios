# Design System — Required workflow continuation

This continuation is mandatory after the main workflow. It preserves the
author-only mutation boundary: only the selected system GDD and its checkpoint
may change.

## 4. Section-by-section authoring

Process authorized sections in canonical order. revise-section processes only
its selected section. For each section use:

    Context -> Decision Classification -> Questions -> Options -> User Decision
    -> Draft -> Semantic Preflight -> Content Approval
    -> Transactional Preflight -> Atomic Write -> Checkpoint

Content approval is not new filesystem authorization. It confirms that the
displayed draft expresses the accepted decision inside the authorized scope.

### 4a. Classify decisions before drafting

Every material decision used by a written section has a stable checkpoint ID
and exactly one class:

| Class | Authority and required provenance | Handling |
|---|---|---|
| product-choice | User or named product owner; prompt and selected option | Present two to four meaningful options and let the owner decide |
| evidence-backed-hard-constraint | Current owner document path, section, revision, and exact supported fact | The current target cannot override it; route a requested change to the owning document |
| derived-design-constraint | Accepted input decision IDs, derivation, assumptions, and proposed result | Show the derivation; user accepts, rejects, or requests revision; never call it hard evidence |
| technical-handoff | Source question/evidence, destination ADR/TECH, and decision-needed or constraint-to-verify | Keep it out of the GDD and record only in the checkpoint |

Use a decision record shaped as:

    id: DSD-<section-key>-<NNN>
    section: <canonical section>
    class: product-choice | evidence-backed-hard-constraint |
      derived-design-constraint | technical-handoff
    authority: <user, product owner, owner document, or derivation>
    source:
      path: <path or null>
      section: <heading or null>
      revision: <revision or null>
    inputs: []
    derivation: null
    assumptions: []
    outcome: <accepted product/design statement or routed technical question>
    status: accepted | routed | blocked

For product choices, state what the section must decide, cite only relevant
bounded evidence, present options with tradeoffs, and ask the user to decide.
Do not let a specialist, registry claim, ADR, or engine fact make the choice.

For an evidence-backed hard constraint, re-read its owner source before using
it. Explain what remains open for product choice. A user preference in this
target cannot silently override current external-owner evidence. If the user
wants the hard fact changed, mark the section blocked and route work to its
owner.

For a derived design constraint, show inputs, formula or reasoning, and
assumptions. User acceptance makes it an accepted derived proposal, not external
evidence. Preserve the derivation so review can reproduce it.

If discussion reaches implementation or architecture, use technical-handoff and
the main workflow's ADR/TECH boundary. Never answer it in the GDD.

### 4b. Draft only the current section

A GDD draft may include:

- player-visible behavior and intended feeling;
- unambiguous product rules and state outcomes;
- formula meaning, variables, units, ranges, caps, and worked examples;
- product-facing dependency contracts such as required inputs and observable
  outputs, without APIs or data structures;
- designer-facing tuning values and safe gameplay ranges; and
- observable acceptance conditions for the design.

It must not include implementation selections, engine APIs, class/module names,
storage or resource schemas, synchronization mechanisms, architecture
decisions, technical feasibility discussion, review verdicts, reviewer
commentary, QA procedures, or automated-test steps.

Draft only from accepted decision records. Show provisional dependency
assumptions explicitly. Never write empty, unapproved, placeholder, or
speculative content as complete.

### 4c. Semantic preflight before content approval

Run semantic preflight on the complete proposed body before asking for content
approval:

1. Evaluate the section's system-gdd/v2 assertions from Section 5. Record exact
   validation_failures; do not reduce validation to non-empty text.
2. Confirm every material rule traces to an accepted decision record and every
   decision record belongs to the current section.
3. Scan for ADR/TECH, QA, REVIEW_ONLY, and other-document content. Route it out
   and regenerate the draft.
4. Extract named shared facts, formulas, constants, entities, and dependency
   claims from the draft.
5. Compare them with the revision-bound registry snapshot and relevant owner
   evidence. Apply the claim classifications from the main workflow.
6. re-read every loaded source cited as a hard constraint. If evidence changed,
   return ERROR — CONTEXT CLAIM CHANGED, write nothing, and stop.
7. Resolve target-owned change candidates through the user decision and add only
   registry_handoffs. An external-owner conflict blocks the section.
8. Confirm the body is substantive or a permitted, fully reasoned
   not-applicable body and contains no placeholder.

If semantic preflight changes the draft or decision outcome, show the complete
revised body and rerun semantic preflight. Approval of an earlier body does not
apply to changed bytes.

After a clean semantic preflight, ask:

    Approve the <Section Name> content shown above?
    A. Approve this exact content for the authorized write
    B. Revise the draft
    C. Leave this section pending and stop

If B, revise and rerun semantic preflight before asking again. If C, mark the
section pending or blocked, set checkpoint status partial, and stop.

Store the exact approved body under approved_drafts, keyed by section, and set
workflow_state to approved-not-written. This permits safe recovery only while
all bound revisions still match.

### 4d. Transactional preflight immediately before every GDD write

Immediately before writing:

1. Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
2. re-read the registry file when registry_snapshot.revision is non-null and every
   loaded evidence source used by the section. Any mismatch returns
   ERROR — CONTEXT CLAIM CHANGED with zero writes.
3. Confirm target and checkpoint are the only mutation_scope paths.
4. Confirm the section is in authorized_scope and the approved body exactly
   matches approved_drafts.
5. Apply the checkpoint.origin_mode predicate below. invocation_mode resume
   never substitutes a broader predicate.
6. Repeat the routing scan so no technical, QA, or review material entered
   after approval.
7. Confirm current body range is unique and its baseline/current body revision meets
   the origin-mode predicate.
8. If current GDD status is Approved or In Review, include a demotion to
   In Design in this first content-write transaction and invalidate the prior
   handoff as described below.

| origin_mode | Required pre-write predicate |
|---|---|
| new | Current body is the skeleton placeholder, or approved-not-written identifies a recoverable write against matching revisions |
| fill-gaps | Baseline inventory classified the required section missing, empty, or placeholder-only; no substantive baseline body may be replaced |
| revise-section | This is the one selected section; required content had a substantive baseline, while supported optional content may have a substantive, missing, empty, or placeholder-only baseline; the stored baseline body revision/state still matches |

For resume, enforce its stored origin_mode, baseline_target_revision,
baseline_section_revision, and authorized_scope. A revise-section recovery may
replace the still-matching substantive body; do not apply resume's old
"body must be non-substantive" shortcut.

If a predicate fails, return ERROR — MODE MUTATION VIOLATION and make no write.

### 4e. Atomic section write, review invalidation, and checkpoint

Patch by heading boundaries, not a bare placeholder string. A replacement range
starts at the exact level-two canonical heading and ends immediately before the
next level-two heading or end of file. Reject duplicate headings or ambiguity.

For a missing required fill-gaps section, insert its heading and approved body
at the canonical position without changing neighboring section bytes. For an
absent supported optional revise-section, insert only the selected heading/body
at the end, unless the document already establishes an unambiguous optional
section order.

On the first content mutation of an existing artifact:

1. copy any active review_handoff.target_revision, or otherwise the pre-mutation
   target revision when status was Approved or In Review, into
   review_handoff.invalidated_target_revision;
2. set invalidation_reason to content-mutation;
3. clear active target_revision and context_manifest_revision;
4. set GDD status to In Design; and
5. never copy or reconstruct a prior review verdict.

Apply the GDD write atomically. Then:

1. re-read the target;
2. verify exactly one intended section changed and every out-of-scope section is
   byte-for-byte unchanged, except the authorized status demotion;
3. Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
4. set workflow_state written and content_state to substantive or
   not-applicable;
5. attach the section's decision IDs;
6. remove its approved_drafts entry;
7. update checkpoint.current_revision; and
8. atomically write only the authorized checkpoint.

If verification fails, report ERROR with the observed revision and stop. Do not
attempt unrelated cleanup.

## 5. system-gdd/v2 content assertions

Heading presence, word count, and absence of placeholder tokens are necessary
but not sufficient. A required body is valid only when every applicable
assertion below passes. Record failed assertion names in section_inventory.

### A. Overview

Required assertions:

- product-purpose — explains what the system does for play;
- player-encounter — states how or when the player encounters it; and
- lost-value — states what player experience would be lost without it.

Overview is always applicable and cannot be N/A. Infrastructure systems must
still be framed by observable play effects.

### B. Player Fantasy

Required assertions:

- intended-feeling — names the emotion, competence, tension, or power fantasy;
- pillar-connection — links it to a current game pillar; and
- concrete-moment — describes a player moment that demonstrates the fantasy.

State whether the fantasy is experienced directly, indirectly through outcomes,
or both. This section is always applicable.

### C. Detailed Rules

Required assertions:

- core-rules — gives unambiguous product rules;
- decisions-and-states — defines player decisions plus valid states and
  transitions, or a reason the mechanic is stateless;
- constraints — states product-level limits and invalid actions; and
- interaction-contracts — for each interaction, gives design-owned input,
  observable output, play-relevant timing, and rule owner.

Do not specify APIs, messages, classes, resources, serialization, or event-bus
choices. This section is always applicable.

### D. Formulas

Every gameplay formula must provide:

- stable design name and mathematical expression;
- every variable's meaning, unit, type, and allowed gameplay range;
- output range with cap/floor behavior; and
- one worked gameplay example.

Formula TBD is invalid. Formulas may be not-applicable only when the approved
body explains why no quantitative transformation governs the system and what
observable rule replaces formula-driven behavior.

### E. Edge Cases

Each entry must pair an exact condition with an exact product outcome. Cover
zero, maximum, invalid/unavailable actions, simultaneous rules, tie-breaking,
and degenerate strategies when applicable. Logging, thread safety, replication,
persistence recovery, and automated-test mechanics are not product outcomes.

This section is always applicable and cannot be N/A.

### F. Dependencies

For each dependency state:

- upstream or downstream direction;
- hard or soft necessity;
- product-owned input and observable output;
- current, provisional, planned-not-authored, unknown, or broken-link status;
  and
- owner of the product rule.

Dependencies may be not-applicable only when the approved body states that no
external system input/output is required and explains the resulting boundary.
Do not claim bidirectional agreement unless the dependency source was loaded
and agrees.

### G. Tuning Knobs

For each knob state the designer-facing value, decided default when available,
safe range, effect of increase/decrease, extreme behavior, and interactions with
other knobs. Do not prescribe config formats, editor tools, asset types, or
runtime storage.

Tuning Knobs may be not-applicable only when the approved body explains why the
system intentionally has no adjustable gameplay value and identifies the fixed
observable rule.

### H. Acceptance Criteria

Use independently observable product conditions, normally:

    GIVEN <player-visible initial state>
    WHEN <player action or product trigger>
    THEN <specific measurable gameplay outcome>

Required assertions:

- core-rule-coverage — every core rule has at least one condition;
- formula-coverage — every applicable formula has boundary/example coverage;
  and
- product-observability — outcomes are measurable in play without prescribing
  QA procedure or implementation instrumentation.

This section is always applicable and cannot be N/A.

### Optional material

Visual/Audio Requirements, UI Requirements, and Open Questions do not count
toward the eight required sections.

- absent optional section: valid and out-of-scope;
- present substantive optional section: valid;
- present approved not-applicable optional section: valid when it contains a
  reason and observable consequence;
- present empty or placeholder-only optional section: invalid for whole-artifact
  completion.

New and fill-gaps do not add optional material. Only an explicitly scoped
revise-section invocation may add or change one supported optional section.

## 6. Specialist consultation boundary and failure schema

Consultation is optional unless the author identifies a specific evidence gap
that cannot be resolved by user product decision alone. It must help only the
current section and obey all caps:

- at most one adviser for a section;
- at most three consultations for the whole run;
- one bounded question and one 60-second attempt per consultation;
- no automatic retry; and
- no nested delegation by the adviser.

Record:

    id: DSC-<NNN>
    section: <canonical section>
    role: <specialist role>
    question: <one bounded question>
    input_hashes: []
    required: true | false
    status: complete | partial | timeout | failed | skipped
    evidence_summary: <bounded summary or null>
    fallback: none | explicit-user-decision | section-blocked

The adviser returns proposals or evidence only. It cannot write files, approve
content, update status, or create product/technical decisions.

For optional partial, timeout, or failure, continue only after an explicit user
decision that does not require the missing evidence; record fallback
explicit-user-decision. For required non-complete input, mark the section
blocked, set checkpoint status partial, record section-blocked, and stop. Never
invent missing output. Reject a second adviser for one section or a fourth
consultation in the run.

## 7. Whole-artifact and context validation

After all authorized sections are written, re-read the whole GDD and compute its
revision. Validate:

- every required canonical heading occurs exactly once;
- every required body passes all applicable system-gdd/v2 assertions;
- not-applicable is used only for permitted sections and has accepted decision
  provenance plus the required rationale;
- rules, formulas, edge outcomes, dependencies, knobs, and acceptance
  conditions are internally coherent;
- no ADR/TECH, QA procedure, reviewer discussion, or approval evidence appears;
- each present optional section is substantive or valid not-applicable; and
- every loaded context file still matches context_manifest.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

Mode completion has two dimensions:

- run scope complete — every authorized section was written; and
- artifact complete — the whole current GDD passes system-gdd/v2.

If run scope is complete but artifact is not, keep status In Design, set
checkpoint status partial, list validation failures and incomplete sections,
and stop.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

    approved_drafts: {}
    review_handoff:
      required: true
      target_revision: <final target revision>
      content_profile: system-gdd/v2
      context_manifest_revision: <current manifest reference ID>
      invalidated_target_revision: <prior revision or null>
      invalidation_reason: <content-mutation or null>
      target_status: In Review
      command: $design-review design/gdd/<system-slug>.md
      task_requirement: fresh independent task

The checkpoint records a review request, not a verdict or immutable review
receipt.

## 8. Independent review and recorder handoff

Return:

    Authoring complete for: design/gdd/<system-slug>.md
    Content profile: system-gdd/v2
    Current revision: <final target revision>
    Context manifest revision: <manifest reference ID>
    Author status: In Review
    Independent review required: open a fresh task and run
      $design-review design/gdd/<system-slug>.md
    Author mutations: target GDD and checkpoint only
    Registry/index/sign-off mutations: none

Then stop. Never invoke design-review in this task or continue into another
workflow.

A conversation summary or this mutable checkpoint is not immutable approval
evidence. A later external recorder may approve only from a persisted canonical
independent report and immutable receipt that satisfy all of:

1. whole-artifact formal review verdict exactly APPROVED;
2. report target path and revision equal the current GDD;
3. report profile is system-gdd/v2 or a compatible independently validated
   profile;
4. review independence is formal, not same-task or advisory-only;
5. report and receipt are immutable/revision-bound;
6. any required context binding is current;
7. systems-index expected pre-state still matches; and
8. the recorder re-reads immediately before atomic conflict check.

STALE REVIEW, context mismatch, index mismatch, NEEDS REVISION, MAJOR REVISION
NEEDED, PARTIAL REVIEW, accepted risk, solo/advisory review, or missing receipt
cannot authorize Approved.

Legal systems-index states remain Not Started, In Design, In Review, Approved,
and Implemented. Designed is invalid. This author never writes the index.

When review requires revision, start a separate design-system task in
revise-section mode for one selected section. That first mutation invalidates
the prior handoff. Review the new whole-artifact revision in another fresh task.

## 9. Recovery and resume

On interruption, re-read target and checkpoint. Require
design-system-checkpoint/v3 and validate content_profile, target, origin_mode,
invocation_mode, mutation_scope, authorized_scope, baseline revisions,
context-manifest records, registry snapshot, and current_revision.

- Matching evidence: set invocation_mode resume and preserve origin_mode;
  recover approved-not-written first, otherwise the first pending authorized
  section.
- Target revision mismatch: ERROR — STALE CHECKPOINT, zero writes.
- Relevant context/registry/evidence revision mismatch:
  ERROR — CONTEXT CLAIM CHANGED, zero writes until a new inventory and
  authorization.
- Missing checkpoint: resume unavailable; user may explicitly choose a new
  fill-gaps or revise-section run.
- v1/v2 checkpoint: ERROR — UNSUPPORTED CHECKPOINT SCHEMA, zero writes.
- Written substantive section: never re-authored by resume.
- approved-not-written: recover only the exact stored body while target,
  origin-mode baseline, registry, and evidence revisions match.

Never use conversation memory as approval, decision provenance, or revision
evidence. Never reconstruct a formal verdict in the checkpoint.
