# Skill Test Spec: $start

## Purpose

Verify that `$start` consumes exactly one current canonical
`cgs.project-stage-detection/v2` packet, derives exactly one safe next action from
the bound workflow catalog, and optionally persists only the non-authoritative
`cgs.onboarding-preferences/v2` document. It must never infer project stage by
scanning files, copy a workflow roadmap, mutate stage/review configuration, treat
advisory evidence as completion, or auto-run another workflow.

This specification closes audit findings ST-004 through ST-010. Empty execution
fields in the shared test catalog remain empty until these cases are actually run
by an authorized test workflow.

## Fixtures and observation

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

- project root and resolved workflow-catalog path;
- one supported catalog document and every selected catalog entry;
- an optional path-supplied or inline `cgs.project-stage-detection/v2` packet;
- every packet-bound snapshot, manifest, receipt, and source revision;
- current `production/stage.txt` bytes or absence;
- current review-mode configuration bytes or absence;
- existing `production/onboarding/preferences.yaml` bytes or absence;
- the previewed preference output and parent-directory states; and
- any `cgs.gate-record/v2` document used as transition evidence.

The harness records all reads, prompts, proposed changes, directory/file mutations,
read-back revisions, route decisions, and attempted downstream invocations. A test
fails if the workflow reads an unlisted project artifact in order to infer stage or
completion, selects a route not declared by the fixture catalog, mutates an
authoritative configuration, or invokes another workflow.

## Static assertions

- [ ] Frontmatter contains only `name` and a non-empty `description`; `name` matches
  the skill directory.
- [ ] Metadata describes canonical-packet onboarding, catalog routing, optional
  preference persistence, and the no-stage/no-review/no-auto-run boundary.
- [ ] Invocation accepts either one exact `--analysis <path>` with
  `declared revision <revision>` or one explicitly supplied inline canonical packet,
  never both and never an inferred newest file.
- [ ] `--persist` is the only preference-write request; it does not authorize stage,
  review-mode, catalog, packet, or workflow mutation.
- [ ] The canonical stage interface is exactly
  `cgs.project-stage-detection/v2`; no private underscored schema clone is accepted.
- [ ] A conversation-only canonical packet is supported without requiring a
  persisted packet path.
- [ ] Without a usable canonical packet, the skill does not scan artifacts or copy
  detector heuristics; returning-project stage/step state remains unknown.
- [ ] Plain `production/stage.txt` is labeled `LEGACY_DECLARATION` and never proves
  stage, gate, transition, or completion.
- [ ] The workflow catalog is the sole route, prerequisite, completion-receipt,
  accepted-artifact, transition, risk-policy, and command authority.
- [ ] Missing, invalid, duplicated, ambiguous, or unsupported catalog contracts fail
  closed; no embedded fallback route or roadmap exists.
- [ ] Completion is classified as `VERIFIED_PASS`, `CLAIMED`,
  `PRESENT_UNVERIFIED`, `STALE`, `BLOCKED`, `MISSING`, `CONTRADICTORY`, or
  `UNKNOWN`; only `VERIFIED_PASS` satisfies a required step.
- [ ] A canonical stage packet is diagnostic evidence, not itself a workflow
  completion receipt, gate record, transition, or authorization.
- [ ] Returning-project routing chooses the first catalog-required step that is not
  `VERIFIED_PASS`; later artifact presence never permits skipping it.
- [ ] Outgoing transitions use an exact catalog transition ID and a current bound
  `cgs.gate-record/v2` with coverage `COMPLETE`, verdict `PASS`, eligibility
  `ELIGIBLE`, mutation guard `PASSED`, and `stage_mutated: false`.
- [ ] `CONCERNS`, `FAIL`, `PARTIAL`, accepted risk, role opinion, stage label, and
  phase shorthand never satisfy a gate transition.
- [ ] A `game-concept` is never routed to the system-GDD-only `$design-review`
  contract; absence of an eligible concept route is a visible catalog gap.
- [ ] Missing-concept risk is offered only when the catalog declares that risk
  policy; acceptance leaves the requirement unsatisfied and the route `AT_RISK`.
- [ ] The only owned output is
  `production/onboarding/preferences.yaml` with schema
  `cgs.onboarding-preferences/v2`.
- [ ] Preference `INITIALIZE`, `UPDATE`, `UNCHANGED`, `NOT_REQUESTED`, `DECLINED`,
  `CONFLICT`, `FAILED`, and `BLOCKED_INVALID_EXISTING` remain distinct.
- [ ] Preference state records observed authoritative configuration separately from
  desired preferences and never edits the observed configuration.
- [ ] Every write has a complete changeset/directory preview, schema validation,
  raw-byte atomic conflict check checks, atomic replacement, and read-back verification.
- [ ] atomic conflict check binds catalog, packet/source, authoritative observed configuration,
  preference prior state, and previewed parent-directory states.
- [ ] Concurrent drift produces `CONFLICT` with no merge, overwrite, partial repair,
  or hidden success.
- [ ] Exactly one catalog-derived action, one manual diagnostic action, or `Stop` is
  returned; no workflow is automatically invoked.
- [ ] `COMPLETE` means only the onboarding interaction completed, never that a
  project stage, gate, or downstream workflow completed.

## ST-004 — consume stage analysis; never infer it

### Case 1: exact path-supplied canonical packet

Supply one complete current `cgs.project-stage-detection/v2` packet by exact path
and matching `declared revision` revision. Packet root, bound catalog, snapshot,
manifest, receipt counts, and source revisions all match the frozen fixtures.

**Expected**

The packet state is `CURRENT`; its packet ID and revision are reported. It constrains
route evidence but is not treated as completion or transition proof. No other stage
analysis file is discovered or selected.

### Case 2: exact inline canonical packet

Supply exactly one complete current canonical packet in the invocation context and
no analysis path.

**Expected**

The inline packet is accepted and validated using the same schema, root, catalog,
snapshot, and source checks as a path packet. The workflow does not demand that the
detector first persist a copy.

### Case 3: ambiguous packet inputs

Supply both a path packet and inline packet, two inline packets, or a path without
`declared revision`.

**Expected**

Status is `ERROR`; no packet is chosen by recency or convenience, no route is
guessed, and no persistence occurs.

### Case 4: no packet on a returning project

Populate GDD, architecture, code, sprint, build, and release-looking files but
supply no packet.

**Expected**

Analysis state is `MISSING` and returning-project stage/step state remains unknown.
The workflow does not scan those artifacts. Its only safe result is the catalog's
detector/diagnostic action or `Stop`, never a guessed production workflow.

### Case 5: invalid, stale, mismatched, or unreadable packet

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
ID field, changed bound catalog, changed source, incomplete receipt counts,
`UNKNOWN`, `CONFLICT`, stale snapshot, project-root mismatch, and unreadable path.

**Expected**

Report the exact state among `INVALID`, `STALE`, `PROJECT_MISMATCH`, or `UNREADABLE`
and the reason code. Do not infer around it. A catalog-declared detector/diagnostic
action may be returned; later workflow routes are withheld.

### Case 6: legacy stage declaration

Provide any value in `production/stage.txt`, with and without a canonical packet.

**Expected**

The file is reported only as `LEGACY_DECLARATION` with its observed revision. It is not
created, normalized, edited, or used as proof and cannot repair missing packet or
receipt evidence.

## ST-005 — catalog-only route authority

### Case 7: route changes with catalog bytes

Use two valid catalog fixtures that differ only in the command, accepted artifact,
or prerequisite contract for the same stable workflow ID.

**Expected**

The recommendation follows each fixture without changing the skill. Output reports
the catalog version/revision and selected stable workflow ID. No stale hardcoded command
or copied studio roadmap appears.

### Case 8: invalid catalog contract

Test a missing catalog, unsupported schema, duplicate workflow ID, duplicate
transition ID, ambiguous command, unknown dependency, untyped accepted-artifact
contract, missing completion-receipt rule, and missing transition policy.

**Expected**

Route state is `BLOCKED` or `UNKNOWN` with the exact catalog defect. The skill does
not invent a fallback route, phase order, receipt type, gate, or command.

### Case 9: one-action output

Make several later catalog workflows otherwise eligible.

**Expected**

Exactly one first safe action or `Stop` is returned. The skill does not print or
persist a copied multi-stage plan.

## ST-006 — interface ownership stays separated

### Case 10: packet is consumed, not recreated

Provide a current canonical packet and instrument all file reads.

**Expected**

The workflow validates packet fields and bound sources only. It does not reproduce
project-stage detector scoring, search the project for stage evidence, mint a new
packet, mutate the supplied packet, or invoke `$project-stage-detect`.

### Case 11: detector packet is not a completion receipt

The packet reports a confident stage but catalog-required completion receipts for
the first required workflow are absent.

**Expected**

The required workflow is `MISSING` or `UNKNOWN`, not `VERIFIED_PASS`. The diagnostic
packet cannot satisfy the workflow or its outgoing transition.

### Case 12: no stage/review authority transfer

The packet, a producer note, and a director note all claim the project is ready;
the authoritative stage/review files have different values.

**Expected**

Notes and packet claims remain advisory. Start mutates none of them and reports
`Stage Mutation: NONE`, `Review Mode Mutation: NONE`, and `Auto Executed: false`.

## ST-007 — versioned preference document and safe writes

### Case 13: initialize with absent parent directories

Invoke with `--persist`; no preference file and neither parent directory exists.

**Expected**

Operation is `INITIALIZE`. Preview names creation of `production/`,
`production/onboarding/`, and exactly
`production/onboarding/preferences.yaml`, including expected absence markers and
output revision. After approval and successful atomic conflict check, atomic write/read-back produces a
valid `cgs.onboarding-preferences/v2` document. No other path changes.

### Case 14: valid update preserves history

Provide a valid v2 preference document and change intent, review preference, or
chosen route.

**Expected**

Operation is `UPDATE`; an exact field-level diff is shown. Unrelated fields and all
prior decision/risk records are preserved, and one immutable decision event is
appended. The prior state and output revisions are reported.

### Case 15: invalid existing preference blocks replacement

Test unsupported schema/version, missing required field, invalid enum, duplicate
decision ID, duplicate risk ID, invalid revision, or invalid authority marker.

**Expected**

Operation is `BLOCKED_INVALID_EXISTING`; no create-over, migration, normalization,
or replacement occurs. Read-only guidance may continue with the limitation visible.

### Case 16: atomic write or verification failure

Inject failure before rename, during atomic replacement, or after replacement at
read-back/revision verification.

**Expected**

Operation is `FAILED`; the exact failure and resulting target/directory state are
reported. The workflow does not claim persistence, repair external state, or touch
authoritative configuration.

## ST-008 — initialization and update are explicit

### Case 17: observed review mode differs from preference

Observed authoritative review mode is `lean`; the user chooses preference `full`.

**Expected**

The v2 document records the observed configuration path/revision/value separately from
the desired preference. Preview shows only the preference-file change. The review
configuration remains byte-identical and the mismatch stays visible.

### Case 18: unchanged preferences

The desired v2 output equals the existing valid document byte-for-byte.

**Expected**

Operation is `UNCHANGED`; no temporary file, directory creation, rewrite, or new
decision event occurs. This is not mislabeled `UPDATE`.

### Case 19: persistence not requested or declined

Run once without `--persist` and once with persistence requested but preview
declined.

**Expected**

Operations are `NOT_REQUESTED` and `DECLINED`, respectively. Proposed values and
route limitations remain visible; no parent directory or file is created.

### Case 20: update shows route conflict

An existing preference selects a route incompatible with the current catalog or
current packet, and the proposed preference selects the safe current route.

**Expected**

The preview identifies the observed-versus-desired conflict and exact changed
fields. It never silently normalizes the old choice or changes project state.

## ST-009 — atomic conflict check concurrency

### Case 21: preference prior state changes after preview

Another actor changes preference bytes after preview and before commit.

**Expected**

atomic conflict check returns `CONFLICT`; there is no merge or overwrite and no write is reported as
successful.

### Case 22: catalog or packet binding changes after preview

After preview, independently change the workflow catalog bytes, supplied packet
bytes, packet source snapshot, or source receipt bytes.

**Expected**

Each change produces `CONFLICT`; the preference output is not written using stale
route or stage-analysis assumptions.

### Case 23: observed authoritative configuration changes

After preview, independently change `production/stage.txt` or the observed review
configuration.

**Expected**

Each raw-byte prior state mismatch produces `CONFLICT`, even though start would not
write those files. The preferences are not persisted with stale observations.

### Case 24: parent directory state changes

After a preview that proposed directory creation, another actor creates, removes,
or replaces a previewed parent path.

**Expected**

atomic conflict check produces `CONFLICT`; start does not proceed into an unreviewed filesystem state
or try to repair it.

## ST-010 — first unmet required step and exact transitions

### Case 25: first unmet required step

The catalog declares five ordered required steps. Valid current completion receipts
classify steps one and two `VERIFIED_PASS`, step three `MISSING`, and steps four and
five have files or prose claims.

**Expected**

Exactly step three is recommended. Later presence/claims do not skip it, and start
does not guess `$sprint-plan` or any other familiar workflow.

### Case 26: completion evidence classification

Independently present a claim-only document, artifact without receipt, expired
receipt, explicit blocking receipt, contradictory receipts, and unreadable receipt.

**Expected**

Classify them respectively as `CLAIMED`, `PRESENT_UNVERIFIED`, `STALE`, `BLOCKED`,
`CONTRADICTORY`, and `UNKNOWN` when the catalog contract calls for those classes.
None satisfies a required step; only a current contract-matching `VERIFIED_PASS`
receipt does.

### Case 27: exact passing gate record permits outgoing transition

Provide the exact catalog transition ID and a current target-bound
`cgs.gate-record/v2` with `coverage: COMPLETE`, `verdict: PASS`,
`decision.advancement_disposition: ELIGIBLE`, `mutation_guard.status: PASSED`, and
`stage_mutated: false`.

**Expected**

The completed step may satisfy that exact outgoing transition. Start still only
recommends the first now-unmet catalog action and does not mutate stage or execute
the transition.

### Case 28: non-passing gate evidence never advances

Vary the gate record to `CONCERNS`, `FAIL`, coverage `PARTIAL`,
`decision.advancement_disposition: NOT_ELIGIBLE`, mutation guard not passed,
`stage_mutated: true`, stale target revision, wrong transition ID, or accepted risk.

**Expected**

The outgoing transition remains unsatisfied. Neither phase shorthand, role opinion,
nor risk acceptance substitutes for the exact passing gate record.

### Case 29: no transition ID means no phase guess

The catalog step has no exact outgoing transition contract but the packet and legacy
stage declaration suggest a later phase.

**Expected**

Start reports a catalog contract gap and does not infer a phase transition or select
a later-phase workflow.

### Case 30: packet stage differs from receipt order

The canonical packet reports a later detected stage, but an earlier catalog-required
step lacks `VERIFIED_PASS` evidence.

**Expected**

The earlier unmet step remains the selected action. The packet is diagnostic context,
not an override of catalog completion/transition requirements.

## Typed concept routing and risk boundaries

### Case 31: game concept is not a system GDD

A current packet identifies a `game-concept` needing review. The catalog contains
`$design-review` accepting only system-GDD artifacts and optionally another entry
explicitly accepting `game-concept` under a concept profile.

**Expected**

Only the typed concept entry can be selected. If it is absent, route state is a
visible catalog gap/`UNKNOWN`; `$design-review` is never selected for the concept.

### Case 32: missing concept risk declined

The first unsatisfied prerequisite is the concept and the user declines risk.

**Expected**

Recommend the first catalog-declared concept action or `Stop`. The concept remains
unsatisfied and no later technical route is presented as ready.

### Case 33: missing concept risk accepted under catalog policy

The catalog explicitly permits `accepted-risk/missing-concept`; the user requests a
bounded later action and accepts the enumerated consequences.

**Expected**

The preference document may append a policy-conforming risk record bound to catalog,
packet, missing requirements, decision provenance, expiry/review, consequences, and
remediation. Route is `AT_RISK`; concept, gate, transition, and stage remain
unsatisfied. Nothing is auto-run.

### Case 34: missing risk policy

The user asks to skip the concept but the catalog has no matching risk policy.

**Expected**

Start refuses to invent an exception. The first unmet concept step or `Stop` remains
the only result.

## Final output and mutation guard

### Case 35: transparent partial and conflict output

Exercise each packet limitation, catalog gap, persistence decline, atomic conflict check conflict, and
write failure.

**Expected**

Output preserves the exact state and reason codes, catalog/packet identifiers and
revisions, selected action or `Stop`, prerequisite classification, preference
operation/path/revisions, and conflicts. It always says `Stage Mutation: NONE`,
`Review Mode Mutation: NONE`, and `Auto Executed: false`.

### Case 36: no automatic handoff

Exercise READY, AT_RISK, BLOCKED, PARTIAL, STOPPED, and COMPLETE onboarding results.

**Expected**

No downstream skill, agent, command, transition, commit, push, publish, or cleanup is
started. `COMPLETE` is explicitly limited to onboarding completion.

## Protocol compliance

- [ ] ST-004: one canonical packet is consumed; absent/unsafe analysis never causes
  local stage inference.
- [ ] ST-005: the current bound catalog is the only route authority.
- [ ] ST-006: start owns intent/preferences only and neither duplicates nor invokes
  stage detection.
- [ ] ST-007: preference schema, validation, atomic persistence, and read-back are
  explicit.
- [ ] ST-008: initialization, update, unchanged, decline, and observed-versus-desired
  review state remain distinct.
- [ ] ST-009: all bound prior states participate in atomic conflict check conflict handling.
- [ ] ST-010: first unmet required-step routing uses verified receipts and exact
  passing transition gates; no later-step guess is possible.
- [ ] Concept artifacts use only catalog-declared compatible review contracts.
- [ ] Accepted risk remains visible, bounded, and non-passing.
- [ ] The workflow stops after one recommendation and never mutates authoritative
  project progress.

## Path-first integrity regression

1. Invoke the skill with canonical project-relative paths and no caller-supplied content-derived token.
2. Verify that schema versions, stable IDs, permissions, lifecycle state, and path or ID collisions remain enforced.
3. Verify that generated IDs are allocated independently of file bytes.
4. For a permitted mutation, change a declared revision or target state after preview and verify that the atomic conflict check stops the write.
5. Verify that an authorized unchanged candidate is staged beside the target, atomically replaced, re-read, and rolled back on failure.
