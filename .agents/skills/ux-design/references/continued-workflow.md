# UX Design — Required workflow continuation

This continuation is part of the `ux-design` author schema. Execute it only after the
main workflow has validated the request, loaded bounded context, obtained the one
task mutation authorization, and created or migrated the exact profile skeleton.

## Phase 5: Section-by-section product decisions and writes

Process only the authorized stable section IDs, in profile order unless the manifest
records a dependency-safe alternative. For each section use:

`Context → Questions → Options → Decision → Draft → Product approval → Atomic write → Checkpoint`

1. **Context**: cite requirement IDs, source paths/hashes, platform/accessibility
   commitments, prior decisions, and open dependency IDs relevant to the section.
2. **Questions**: ask only information not already sourced. Separate product choices
   from missing external requirements.
3. **Options**: present two or three materially distinct approaches and trade-offs.
   Do not select layout, flow, density, input, or interaction behavior by convention.
4. **Decision**: record stable `UXDEC-{artifact-id}-{section-id}-{sequence}`, the real
   decision-maker, options, choice, rationale, sources, and UTC timestamp.
5. **Draft**: show the complete candidate section in conversation. Mark provisional
   content and dependency IDs; never hide a missing source inside confident prose.
6. **Product approval**: ask whether the draft captures the intended design. This is
   a content decision inside the already authorized mutation boundary, not a new
   filesystem authorization.
7. **Atomic write**: only the named UX-author task re-hashes the current target,
   replaces the one authorized stable-ID region, preserves all other bytes, writes
   atomically where supported, and reads the result back. Never prompt again for file
   permission while paths/sections/limits/owners are unchanged.
8. **Checkpoint**: only the checkpoint recorder appends a new immutable checkpoint
   with before/after target hashes, decision ID, section state, operation result,
   remaining budget, open findings, and next legal section.

If product approval is withheld, retain the draft only in conversation/checkpoint
evidence and revise within the manifest's round limit. Do not write it. Exceeding the
round limit returns `PARTIAL` with the unresolved section and one next decision.

## Profile evidence requirements

The exact required H2 headings and stable IDs are defined in `SKILL.md`. The rules
below refine their evidence without creating another schema.

### ux-spec evidence

- `UXS-01` links the player's goal and expected outcome to existing requirement IDs;
  it does not invent missing system behavior.
- `UXS-02` records arrival source, prior action, player state, urgency, and journey
  evidence or an open dependency.
- `UXS-03` and `UXS-04` use stable screen IDs. Every entry/exit names its trigger,
  state carried, destination/source ID, and irreversible effect.
- `UXS-05` establishes information hierarchy before zones. Its component inventory
  gives stable component IDs, content, interactivity, pattern reference/proposal,
  and viewport assumptions. ASCII/wireframe material is explicitly schematic.
- `UXS-06` covers every applicable state. A non-applicable loading, empty, or error
  state needs a source-backed rationale rather than omission.
- `UXS-07` maps every interactive component across every declared input and includes
  focus order, immediate multimodal feedback, outcome, cancel/back, and recovery.
- `UXS-08` maps every player action to a stable event/payload/owner or an explicit
  source-backed `none`; UX does not become the game-state owner.
- `UXS-09` covers enter, exit, and applicable state changes plus reduced-motion
  equivalents and interrupt/cancel behavior.
- `UXS-10` records source-system owner, read/write intent, update trigger/rate, null
  handling, privacy/sensitivity, and stale-data behavior.
- `UXS-11` traces each screen obligation to the external accessibility tier/hash.
  It covers declared keyboard/gamepad/touch/assistive input, text scale/reflow,
  non-color cues, focus restoration, announcements, and reduced motion as applicable.
- `UXS-12` uses real declared layout constraints and localization infrastructure;
  it covers expansion/reflow, truncation policy, plural/gender, dates/numbers,
  placeholders, bidirectionality when targeted, and string ownership. Do not replace
  sources with a generic expansion percentage.
- `UXS-13` cites requirement and decision IDs and adds observable local conditions,
  fixtures, input, expected result, platform/accessibility variant, and evidence.
  It does not copy another document's product rules or require a tester to infer them.
- `UXS-14` lists stable open questions/dependency IDs with severity, owner, evidence,
  status, destination, and one resolution action.

### hud-design evidence

- `HUD-01` records the approved density philosophy and measurable implications.
- `HUD-02` traces every declared requirement ID to an information item, owner, and
  Must Show/Contextual/On Demand/Hidden decision. Surface philosophy conflicts.
- `HUD-03` records safe-zone, aspect, resolution, text-scale, focal-area, and split-
  screen assumptions from the declared platform profile.
- `HUD-04` gives stable element IDs, category, data owner, visual form, update rule,
  visibility/priority, null/error behavior, and pattern reference/proposal.
- `HUD-05` defines exploration/combat/dialogue/cutscene/pause behavior when applicable,
  contention/queue rules, density transitions, and reduced-motion alternatives.
- `HUD-06` covers every declared input/platform/device/resolution/aspect/text-scale
  variant; unsupported configurations become owned dependency gaps.
- `HUD-07` traces committed accessibility obligations, including non-color cues,
  scaling/reflow, assistive exposure, attention demands, and motion.
- `HUD-08` uses the same stable finding schema as `UXS-14`.

### interaction-pattern-library evidence

- `PAT-01` names the external UX-library owner, canonical scope, consumers, and
  current target/base/schema hashes.
- `PAT-02` catalog rows use stable `UXP-GLOBAL-*` IDs, versions, status, category,
  anchors, source proposal IDs, and owner.
- `PAT-03` entries match catalog IDs and define all states, supported inputs, focus,
  cancel/back behavior, multimodal feedback, accessibility, localization, data/event
  boundaries, use/non-use rules, and references.
- `PAT-04` lists unmerged feature-local `UXP-{screen-id}-{slug}` proposals with source
  screen/hash, requested disposition, owner, and blocker status.
- `PAT-05` uses the same stable finding schema as `UXS-14`.

Only a run whose sole target is the global library and whose mutation authority is
the named external UX-library owner may add or revise canonical patterns. Apply one
stable pattern-ID patch at a time with the current base hash. A collision, stale base,
duplicate semantic pattern, or unowned cross-screen behavior is `BLOCKED`; never
append optimistically.

## Phase 6: Cross-reference and dependency gate

After selected sections are written, run deterministic checks against the exact
bounded context manifest:

1. every applicable GDD requirement ID is covered or has an OPEN owned gap;
2. every navigation edge agrees by stable screen ID and expected neighbor hash;
3. every global pattern reference resolves at the declared library hash, while every
   local proposal remains explicitly non-global;
4. accessibility obligations trace to the external foundation tier/hash;
5. every data-dependent component/HUD element defines null, empty, stale, loading,
   and error behavior when applicable;
6. every declared platform/input/resolution/aspect/text-scale target is covered;
7. each profile-required section ID is present once, correctly headed, substantive,
   and current against its source hashes;
8. author and decision provenance match recorded identities.

Emit stable `UXD-{artifact-id}-{check-id}` findings with severity `BLOCKING` or
`ADVISORY`, evidence path/hash/section, expected rule, observed state, owner,
destination, and status `OPEN` or `CLOSED`. Advisory improvements may remain for
review; any BLOCKING or critical dependency finding prevents `READY_FOR_REVIEW`.

Read back the target and compute `target_sha256`. Recheck immediately before output;
if the bytes changed, return `PARTIAL` with `target-changed-during-authoring` and do
not reuse previous section results.

## Phase 7: Bounded consultations and failures

The UX-author owns target bytes. Consultants are read-only and return evidence to the
author; they never edit the target, checkpoint, accessibility foundation, pattern
library, or implementation files.

Use at most two consultants concurrently. Each gets exact context paths/hashes, one
question, stable task/attempt ID, result schema, and prohibited writes. Cap each
attempt at 15 minutes and the consultation phase at 30 minutes. Allow at most one
retry after proving the first attempt wrote nothing. Revoke canceled attempt tokens
and ignore/quarantine late results.

Possible consultations include art direction, read-only UI feasibility, gameplay
requirement ownership, narrative text constraints, and accessibility conformance.
Consultants cannot approve product choices, define the accessibility tier, merge a
global pattern, or implement UI.

A timeout, malformed result, missing required consultation, or side-effect attempt
produces `PARTIAL` and an immutable checkpoint. Preserve valid approved sections;
do not mark a dependent section current or silently skip the failed evidence.

## Phase 8: Checkpoint and resume

On `--resume`, validate the exact checkpoint path, request/run/artifact IDs,
checkpoint chain, author schema hash, instruction/context hashes, target hash,
authorization manifest, owner identities, section states, decisions, and absence of
late writes. Resume from the recorded next legal transition only.

If the schema changed, switch to `migrate-schema`; if a source changed, mark only its
dependent sections STALE; if target or authorization drifted, return `BLOCKED`. Never
infer completion from non-placeholder text alone and never replay a prior write.

## Phase 9: Determine authoring result and hand off

Set the artifact header and final result deterministically:

- all profile sections current, every critical dependency present, zero BLOCKING
  findings, read-back hashes stable: `Status: READY_FOR_REVIEW` and
  `Verdict: READY_FOR_REVIEW`;
- some safe work is written but sections, dependencies, evidence, consultations, or
  migration remain: `Status: PARTIAL` and `Verdict: PARTIAL`;
- no safe transition is possible because identity, authorization, ownership, target
  drift, or an unresolved mandatory decision prevents work: preserve the last safe
  artifact status and return `Verdict: BLOCKED`.

Never emit `COMPLETE`, `APPROVED`, or `IMPLEMENTATION READY` from authoring. User risk
acceptance keeps named findings OPEN and cannot upgrade status.

Return artifact/run/screen IDs, profile and author schema hash, actual author task ID,
target path/hash, context manifest hash, section-state matrix, decision IDs,
authorization manifest/hash, dependency/finding table, checkpoint path/hash, and
exactly one status-driven next action.

For `READY_FOR_REVIEW`, the next action is to request a fresh independent read-only
review of this exact target hash. The reviewer task must differ from the author and
must return the hash-bound current-schema review record. Do not invoke that review,
persist its record, start visual work, or start implementation in this workflow.

For `PARTIAL` or `BLOCKED`, the sole next action resolves one named dependency,
decision, authorization, drift, owner, or timed-out evidence item. Do not claim that
this run created an accessibility foundation or any artifact other than its one
authorized target and checkpoints.
