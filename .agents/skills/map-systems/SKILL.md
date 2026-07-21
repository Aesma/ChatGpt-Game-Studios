---
name: map-systems
description: "Decompose a game concept into a reviewed systems index, map dependencies, prioritize design order, and stop with a separate GDD-authoring handoff."
---

## Invocation, ownership, and termination

Invoke this workflow as $map-systems.

This workflow authors or updates exactly one systems registry:
design/gdd/systems-index.md. It may also create or update
production/session-state/active.md only when that state edit was included in the
same authorized changeset preview.

It owns systems enumeration, dependency mapping, priority order, and the index
write. It does not author a system GDD, invoke another skill, record a GDD review,
or change a system row because GDD authoring or review completed. The
$design-system author owns exactly one GDD and its checkpoint; a separate
hash-bound recorder owns later index status changes.

Arguments:

    [next | <system-id-or-name>] [--review full|lean|solo]

The modes are exclusive:

- No selection argument: run the index-authoring workflow below.
- next: read the index, display the highest-priority Not Started system, return a
  fresh-task $design-system command, and stop.
- system-id-or-name: resolve and display that index row, return a fresh-task
  $design-system command, and stop.

Selection-only modes never write files, spawn review agents, invoke
$design-system, or loop to another system. Index-authoring mode stops immediately
after its authorized index/state changes are verified. A user request to begin
GDD authoring is a new task, not another phase of this workflow.

Resolve review mode once:

1. use an explicit --review value;
2. otherwise read production/review-mode.txt;
3. otherwise use lean.

See .codex/docs/director-gates.md for gate definitions. This workflow strengthens
their mutation boundary: every reviewer is read-only and reviews an in-memory,
hash-bound draft before any authoritative write.

## 1. Selection-only handoff

For next or an explicit system ID/name, read design/gdd/systems-index.md and do
nothing else.

For next, select the first Not Started row by Recommended Design Order. For an
explicit value, prefer an exact stable ID match, then an exact case-insensitive
name match. If the index is absent, no eligible row exists, or a name is
ambiguous, return Verdict: BLOCKED with the evidence and stop.

Return:

    System ID: <stable ID, or the row's current identifier if legacy>
    System: <name>
    Status: <current status>
    Handoff: Start a fresh task and run $design-system "<system name>"

Then return Verdict: COMPLETE — HANDOFF ONLY and stop. Do not call the command.
Do not ask whether to continue to another system.

## 2. Load index-authoring context

Read applicable AGENTS.md files, then:

Required:

- design/gdd/game-concept.md

If the concept is missing, return:

    No game concept found at design/gdd/game-concept.md. Run $brainstorm first
    to create one, then return to $map-systems.
    Verdict: BLOCKED

Stop without writing.

Read when present:

- design/gdd/game-pillars.md;
- design/gdd/systems-index.md;
- direct child Markdown files under design/gdd/ only to determine whether a
  named GDD path exists.

Do not invoke any workflow while gathering context.

If the index exists, report its current system count and status counts and ask
the user to choose one bounded intent:

- add newly discovered systems;
- review and revise dependencies or priorities; or
- stop and use a selection-only handoff.

Never silently recreate or overwrite an existing index.

## 3. Enumerate systems collaboratively

Extract explicit systems from the concept's core mechanics, loop, technical
considerations, and MVP definition.

Identify implied candidates, explaining the evidence and player/product reason
for each. Typical implications include inventory data and UI, combat health and
feedback, world streaming and persistence, networking synchronization and lobby
flows, crafting recipes and discovery, dialogue state and localization hooks,
and progression unlocks and save data.

Present each proposed system with:

- stable System ID in the form `SYS-<canonical-kebab-slug>`;
- name;
- category;
- one-sentence responsibility;
- explicit or inferred origin; and
- concept evidence.

Ask the user which systems are missing, should be combined or split, or should be
removed. Iterate in conversation until the user approves the enumeration. Do not
write a draft file during this phase.

System IDs are persistent identity, not display order. Preserve every existing
valid ID exactly. For a new system, derive `SYS-<canonical-kebab-slug>` only when
it is unique across current and proposed rows. A normalization collision is
BLOCKED until the user chooses distinct names/IDs. Never renumber an existing
system when ordering changes. For a legacy row with no System ID, propose one in
the reviewed draft and show the migration explicitly; do not let downstream
workflows consume that row until the ID is recorded.

## 4. Map dependencies collaboratively

For every approved system, map:

- input/output dependencies;
- structural dependencies;
- player-facing UI dependencies; and
- the layer: Foundation, Core, Feature, Presentation, or Polish.

Sort the graph in dependency order. Surface circular dependencies, bottlenecks,
and leaf systems, with proposed cycle-breaking outcomes. Ask the user to approve
or revise the map.

Do not spawn TD-SYSTEM-BOUNDARY here. All active reviews must inspect the same
complete draft and hash at the single pre-write checkpoint in section 7.

## 5. Assign priorities and design order

Propose MVP, Vertical Slice, Alpha, and Full Vision tiers from the concept and
dependency graph. Explain both technical necessity and player-experience impact.

Ask the user to approve or revise the priorities. Then combine dependency order
and milestone priority into the recommended design order.

Do not spawn PR-SCOPE here. It reviews the same complete draft at the pre-write
checkpoint.

## 6. Render one canonical draft

Populate .codex/docs/templates/systems-index.md in memory for the authoritative
path design/gdd/systems-index.md. The candidate schema must include a persistent
`System ID` column in every enumeration, dependency/order, and progress row; if
the legacy template lacks that column, augment the in-memory candidate rather
than omitting identity. Include enumeration, dependency map, design order,
risks, and progress. Preserve existing IDs, GDD/status claims unless the user
explicitly selected a change; never infer Approved from a GDD's existence.

Render the exact UTF-8 Markdown bytes with LF line endings. Compute:

    candidate_sha256: <SHA-256 of the exact proposed bytes>

Show the complete draft or a lossless reviewable representation plus the hash.
The draft remains in memory. No systems index, temporary draft, review record,
or session-state file may be written before section 8.

Any content change after this point creates a new candidate hash and invalidates
every earlier review and authorization.

## 7. Run one read-only pre-write review checkpoint

Review mode handling:

- solo: note CD-SYSTEMS, TD-SYSTEM-BOUNDARY, and PR-SCOPE skipped — Solo mode.
- lean: note CD-SYSTEMS, TD-SYSTEM-BOUNDARY, and PR-SCOPE skipped — Lean mode.
- full: spawn creative-director for CD-SYSTEMS, technical-director for
  TD-SYSTEM-BOUNDARY, and producer for PR-SCOPE simultaneously. Issue every
  delegation before waiting for any result, then collect all results.

Pass every active reviewer:

- the complete candidate bytes;
- candidate_sha256;
- proposed destination path;
- relevant concept and pillar evidence;
- priority tiers, dependency graph, bottlenecks, cycles, and scope context; and
- an explicit read-only contract: do not write files, edit the draft, revise the
  system set, or invoke another workflow.

Reviewers return only a verdict and stable findings. Every finding must use ID
<gate-id>-F### and include candidate_sha256, location, evidence, impact, and
required outcome. Normalize producer REALISTIC as pass, OPTIMISTIC as concerns,
and UNREALISTIC as reject.

Apply the strictest disposition:

- Any REJECT or UNREALISTIC: display the stable findings, output a revision
  handoff containing candidate_sha256 and every finding ID, return Verdict:
  BLOCKED — REVIEW REJECTED, and stop with zero writes.
- CONCERNS or OPTIMISTIC with no rejection: ask the user to accept the unchanged
  reviewed draft, start a fresh author task to revise the listed findings, or
  stop. Accepting unchanged binds the same candidate_sha256. Choosing revision
  outputs the stable finding handoff and stops with zero writes.
- All pass: continue with the same candidate_sha256.

A reviewer never edits source of truth. A requested revision is performed in a
fresh $map-systems authoring task. That fresh task must re-render, re-hash, and
repeat all active reviews; prior verdicts never authorize changed bytes.

If an active reviewer does not return a complete verdict bound to the candidate
hash, do not write. Return the available stable findings and Verdict: BLOCKED —
INCOMPLETE REVIEW.

For lean or solo, record the skipped gate names and bind the user authorization
to candidate_sha256; do not claim an independent review occurred.

## 8. Authorize and write the reviewed bytes once

Present the complete changeset before the first write:

- design/gdd/systems-index.md: create or replace with the exact bytes whose
  SHA-256 is candidate_sha256;
- production/session-state/active.md: create or update the systems-decomposition
  task/status/file/next fields;
- all other writes: none.

Also show review mode, gate dispositions, candidate_sha256, system counts, first
three design-order entries, and high-risk items. Obtain one explicit changeset
authorization. Review acceptance is not filesystem authorization.

If the user declines, return Verdict: BLOCKED — CHANGESET NOT AUTHORIZED and
stop with zero writes.

Immediately before writing:

1. re-render the candidate and verify its SHA-256 still equals candidate_sha256;
2. in full mode, verify every accepted verdict names candidate_sha256;
3. if updating an existing index, verify its current SHA-256 still equals the
   base hash read in section 2.

Any mismatch returns Verdict: BLOCKED — STALE DRAFT or CONCURRENT INDEX CHANGE
and makes no write.

Write design/gdd/systems-index.md exactly once from the bound candidate bytes,
then re-read it and verify its SHA-256 equals candidate_sha256. Update only the
previewed session-state fields. If either authorized result cannot be verified,
return Verdict: PARTIAL with the exact successful and failed paths; never claim
COMPLETE.

On success return:

    Verdict: COMPLETE
    Index: design/gdd/systems-index.md
    SHA-256: <candidate_sha256>
    Next: Start a fresh task and run $design-system "<first system name>"

Then stop. Do not invoke the command, ask to continue, or process another system.

## Review and recorder separation

This workflow's reviews are advisory/eligibility checks for the systems-index
draft only. They do not approve any future GDD.

After a separate $design-system author task stops at In Review, a separate
independent whole-artifact review may produce hash-bound approval evidence. Only
a separate recorder may compare-and-set the matching systems-index row from its
expected pre-state. Neither this workflow nor the GDD author may infer, record,
or loop over that completion.

## Collaborative protocol

Use Question -> Options -> Decision -> Draft -> Approval for product decisions.
The user approves enumeration, dependencies, priorities, disposition of
non-blocking review findings, and the final hash-bound changeset.

Never write an unreviewed full-mode draft.
Never let a reviewer revise or write the index.
Never reuse a verdict after the draft hash changes.
Never invoke $design-system from this workflow.
Never loop across GDDs.
Always stop after the index write or selection-only handoff.
