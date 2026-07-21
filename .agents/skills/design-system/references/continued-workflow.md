# Design System — Required workflow continuation

This continuation is mandatory after the main workflow. It preserves the
author-only mutation boundary: only the selected system GDD and its checkpoint
may change.

## 4. Section-by-section authoring

Process scoped sections in canonical order. revise-section processes only its one
selected section. For each section use:

    Context -> Questions -> Options -> User Decision -> Draft ->
    Content Approval -> Preflight -> Atomic Write -> Checkpoint

Content approval is not a new filesystem authorization. It confirms that the
draft expresses the user's product decision inside the already authorized
changeset.

### 4a. Context, questions, and decision

State what the section must decide and cite only relevant product/design evidence
from the bounded context. Clearly label provisional dependency assumptions.

For a product choice, present two to four meaningful options with tradeoffs and
ask the user to decide. Do not let a specialist, registry claim, ADR, or engine
fact silently make a product decision. For a hard product constraint with direct
evidence, explain the evidence and ask only for the remaining design choice.

If the discussion reaches an implementation or architecture question, route it
to technical_handoffs in the checkpoint as described in the main workflow. Do
not answer it inside the GDD and do not quote an ADR or engine implementation into
the section.

### 4b. Draft and content approval

Draft only the current section. A GDD draft may include:

- player-visible behavior and intended feeling;
- unambiguous product rules and state outcomes;
- formula meaning, variables, ranges, and design caps;
- product-facing dependency contracts such as required inputs and observable
  outputs, without APIs or data structures;
- designer-facing tuning values and safe gameplay ranges; and
- observable acceptance conditions for the design.

It must not include implementation selections, engine APIs, class/module names,
storage or resource schemas, synchronization mechanisms, architecture decisions,
technical feasibility discussion, review verdicts, reviewer commentary, or QA
test procedures.

Show the full proposed section body and, in the same response, ask:

    Approve the <Section Name> content?
    A. Approve this content for the authorized write
    B. Revise the draft
    C. Leave this section pending and stop

If B, revise and ask again. If C, mark the section pending or blocked in the
checkpoint, set checkpoint status to partial, and stop. Never write empty,
unapproved, placeholder, or speculative content as if complete.

### 4c. Preflight before every GDD write

Immediately before writing:

1. Re-read the target bytes and compute SHA-256.
2. Compare that hash with checkpoint.current_sha256. On mismatch, return
   ERROR — CONCURRENT TARGET CHANGE, write nothing, and stop.
3. Confirm the target and checkpoint are the only paths in mutation_scope.
4. Confirm the current section is in scoped_sections.
5. Apply the mode guard in the following table.
6. Scan the approved draft for content that belongs in ADR/TECH, QA,
   REVIEW_ONLY, or another document; route it out before writing.
7. Compare named values in the draft with relevant read-only registry claims.
   If a material value conflicts, surface the evidence and obtain the product
   owner's decision before writing. Do not update the registry.
8. Confirm the draft is substantive and contains no placeholder.
9. If the current GDD header says Approved, include a demotion to In Design in
   this first content-write transaction; the old approval is stale once bytes change.

| Mode | Required pre-write predicate |
|---|---|
| new | Current body is the skeleton placeholder, or an approved-not-written checkpoint state identifies a recoverable write |
| resume | Checkpoint marks this section pending or approved-not-written and current body is not substantive |
| fill-gaps | Baseline inventory classified this section missing, empty, or placeholder-only; no substantive body may be replaced |
| revise-section | This is the one selected section and its current body hash matches the authorized baseline |

If any predicate fails, return ERROR — MODE MUTATION VIOLATION and make no write.

### 4d. Atomic section write and checkpoint

Patch by heading boundaries, not by a bare placeholder string. The replacement
range starts at the exact level-two canonical heading and ends immediately before
the next level-two heading or end of file. Reject duplicate canonical headings or
an ambiguous range.

For a missing fill-gaps section, insert the canonical heading and approved body
at its canonical position without changing neighboring section bytes.

Apply the GDD write atomically. Then:

1. re-read the target from disk;
2. verify exactly one intended section changed and every out-of-scope section is
   byte-for-byte unchanged, except for an authorized stale Approved to In Design
   header demotion;
3. compute the new SHA-256;
4. set the section state to written;
5. update checkpoint.current_sha256 to the new hash; and
6. atomically write only the authorized checkpoint.

If verification fails, report ERROR with the observed hash and stop. Do not
attempt unrelated cleanup.

## 5. Section requirements

The following guidance defines design content, not implementation content.

### A. Overview

Write a concise explanation of what the system does for play, how the player
encounters it, and why the game needs it. Align it with the systems index
description, but do not cite or describe an ADR. Infrastructure systems must
still be framed by their observable effect on play.

Questions should establish:

- the system's one-sentence product purpose;
- active, passive, or automatic player interaction; and
- what player experience would be lost without it.

### B. Player Fantasy

Define the intended emotion, competence, tension, or power fantasy. Ask whether
the system is experienced directly, indirectly through outcomes, or both. Connect
the answer to a game pillar and a concrete player moment.

A creative specialist may offer candidate framings when useful. Specialist
output is advisory; present alternatives to the user, record the user's decision,
and never let a specialist write the file.

### C. Detailed Rules

Specify rules, player decision points, valid states, transitions, constraints, and
interactions with other systems. The rules must be precise at the product level
without choosing code structure.

Use these subsections when applicable:

- Core Rules
- States and Transitions
- Interactions with Other Systems

For each interaction, state the design-owned input, observable output, timing
semantics relevant to play, and rule owner. Do not specify APIs, messages, classes,
resources, serialization, or event-bus choices. Route those to ADR/TECH.

Specialists may identify rule gaps or alternatives. They return proposals only;
the user decides and the author writes.

### D. Formulas

For each gameplay formula define:

- a stable design name;
- the mathematical expression;
- every variable, unit, type, and allowed gameplay range;
- output range and cap/floor behavior; and
- a worked gameplay example.

Do not use Formula TBD. Do not turn the section into an implementation function,
data schema, or optimization plan. If the formula depends on an unresolved
product value, keep the section pending rather than inventing a number.

A systems or economy specialist may propose curves and explain tradeoffs. The
user selects the product rule before the author drafts it.

### E. Edge Cases

Format each item as an exact condition and exact product outcome. Cover zero,
maximum, invalid or unavailable actions, simultaneous rules, tie-breaking, and
known degenerate strategies where applicable.

Handle the player-visible resolution. Logging, thread safety, replication,
persistence recovery, and automated-test mechanics belong outside the GDD unless
the user first converts their effect into a product rule.

### F. Dependencies

List only explicit design dependencies. For each, state:

- upstream or downstream direction;
- hard or soft necessity;
- product-owned input and observable output;
- provisional status if the dependency GDD is not authored; and
- the GDD/system that owns the product rule.

Do not claim bidirectional consistency unless the dependency document was in the
bounded context and actually agrees. Flag a mismatch before writing.

### G. Tuning Knobs

List designer-adjustable gameplay values, defaults if decided, safe ranges,
extreme behavior, and interactions among knobs. Do not prescribe config formats,
editor tooling, asset types, or runtime storage.

### H. Acceptance Criteria

Write independently observable design conditions, normally as:

    GIVEN <player-visible initial state>
    WHEN <player action or product trigger>
    THEN <specific measurable gameplay outcome>

Cover every core rule and formula. Acceptance criteria define what the product
must do; QA test matrices, automation steps, instrumentation, frame-time
implementation budgets, and test data belong in QA or ADR/TECH handoffs.

### Optional material

Visual/audio requirements, UI requirements, and open questions are not part of
the eight-section completeness count. Add an optional section only when it has
substantive user-approved content and was included in the authorized section
scope. Never leave an optional placeholder in an artifact marked In Review.

A visual or UI requirement may specify player-facing feedback and accessibility
intent. Asset production instructions, screen implementation, render technique,
and tool choices belong in later specialized documents.

## 6. Specialist consultation boundary

Use specialist consultation only when it helps the current scoped section.
Provide bounded design context and one concrete question. Agents are advisers:
they do not write files, approve the GDD, update status, or create technical
decisions.

If a consultation fails, times out, or returns incomplete evidence, do not
silently invent its missing contribution. Either continue with an explicit user
decision when specialist input was optional, or mark the section blocked/partial
in the checkpoint and stop. The author-only mutation set does not expand.

## 7. Whole-artifact validation

After all scoped sections are written, re-read the entire GDD from disk and
compute its current SHA-256. Validate the artifact as a whole:

- all eight canonical headings occur exactly once;
- every required body is substantive and contains no placeholder;
- rules, formulas, edge outcomes, dependencies, tuning knobs, and acceptance
  conditions are internally coherent;
- formula variables and ranges are defined;
- acceptance conditions cover each core rule and formula;
- no ADR/TECH, QA procedure, reviewer discussion, or approval evidence appears
  in the GDD; and
- optional sections, if any, contain substantive content.

Mode completion has two dimensions:

- run scope complete — every section authorized for this invocation was written;
- artifact complete — the whole current GDD passes all eight-section checks.

If run scope is complete but the artifact is not, keep the GDD status In Design,
set checkpoint status to partial, list the remaining incomplete sections, and
stop. Do not call it complete.

If the whole artifact passes, perform one final hash-guarded GDD write that sets
only the document Status header to In Review. A prior Approved header is stale as
soon as revise-section changes the artifact; demote it to In Review. Never write
Approved or embed review/sign-off text.

Re-read the file, compute the final SHA-256, set checkpoint status to
ready-for-independent-review, and set:

    approved_drafts: {}
    review_handoff:
      required: true
      target_sha256: <final SHA-256>
      target_status: In Review
      command: $design-review design/gdd/<system-slug>.md
      task_requirement: fresh independent task

The checkpoint records a request for review, not a verdict.

## 8. Independent review and recorder handoff

Return this handoff in conversation:

    Authoring complete for: design/gdd/<system-slug>.md
    Current SHA-256: <final hash>
    Author status: In Review
    Independent review required: open a fresh task and run
      $design-review design/gdd/<system-slug>.md
    Author mutations: target GDD and checkpoint only
    Registry/index/sign-off mutations: none

Then stop. Never invoke design-review in this task, never self-review for formal
approval, and never continue into consistency-check, gate-check, registry
recording, or systems-index recording.

A later recorder, outside this workflow, may record approval only when all of the
following evidence is present:

1. a formal independent whole-artifact review report;
2. verdict exactly APPROVED;
3. report target path exactly matches the GDD;
4. report target SHA-256 equals the GDD's current SHA-256;
5. review independence is formal, not advisory-only or same-task;
6. the report is immutable/hash-bound; and
7. the systems-index row still matches the recorder's expected pre-state.

The recorder must re-read the current GDD hash immediately before mutation and
use compare-and-set. A hash mismatch returns STALE REVIEW and changes nothing. An
index pre-state mismatch returns CONCURRENT INDEX CHANGE and changes nothing.

The only legal systems-index status values are:

- Not Started
- In Design
- In Review
- Approved
- Implemented

Designed is invalid. This authoring workflow never writes any index status. Only
the independent recorder may set Approved, and only from current-hash APPROVED
evidence. NEEDS REVISION, MAJOR REVISION NEEDED, PARTIAL REVIEW, accepted risk,
solo/advisory review, a missing hash, or a stale hash can never authorize
Approved.

When review requires revision, start a separate design-system task in
revise-section mode for one selected GDD section. After that edit, obtain another
fresh whole-artifact review of the new hash.

## 9. Recovery and resume

On interruption, re-read the target and checkpoint. Validate schema, target path,
mode, mutation_scope, and current_sha256 before continuing.

- Matching hash: resume at approved-not-written first, otherwise the first pending
  scoped section.
- Different hash: return ERROR — STALE CHECKPOINT and stop without writing.
- Missing checkpoint: resume mode is unavailable. The user may explicitly choose
  fill-gaps or revise-section after a new inventory and changeset authorization.
- A written substantive section is never re-authored by resume.
- An approved-not-written draft may be recovered only if its approved content is
  present in the checkpoint and the target hash still matches.

Never use conversation memory as approval or hash evidence. Never reconstruct a
formal verdict in the checkpoint.
