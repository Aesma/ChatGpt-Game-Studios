# Skill Test Spec: $start

## Purpose

Verify that `$start` gathers onboarding intent, consumes one typed stage-analysis
artifact when supplied, uses the workflow catalog as its sole route source, writes
only non-authoritative preferences, and never promotes stage or disguises a missing
concept as completed.

## Fixtures

Fixtures provide exact bytes and SHA-256 values for workflow catalog, optional
project-stage analysis, its source receipts, observed stage/review-mode,
existing preferences, and proposed output. Tests observe reads, route selection,
changeset previews, directory/file mutations and downstream invocations.

## Static assertions

- [ ] Frontmatter contains only `name` and non-empty `description`; name matches the directory.
- [ ] Invocation supports optional exact analysis and persist flags and rejects newest-file inference.
- [ ] The only owned output is `production/onboarding/preferences.yaml`.
- [ ] The skill never writes authoritative stage or review-mode files.
- [ ] Stage values are OBSERVED_ONLY, PROPOSED_ONLY, or UNKNOWN.
- [ ] Artifact/file existence alone never proves phase, gate, or step completion.
- [ ] One supported stage-analysis artifact supplies typed/hash-bound state evidence.
- [ ] Without analysis the skill reports NOT_SUPPLIED/UNKNOWN and does not duplicate scanning.
- [ ] Workflow catalog is the sole route source; no copied roadmap exists.
- [ ] Route selection uses stable workflow IDs, artifact types, dependencies and first unmet required step.
- [ ] A game concept can route only to a reviewer that explicitly accepts game-concept with a concept profile.
- [ ] A system-GDD-only reviewer is never selected for a game concept.
- [ ] Jumping past a missing concept requires explicit accepted-risk/missing-concept.
- [ ] Accepted risk leaves requirements UNSATISFIED and Route State AT_RISK.
- [ ] Risk acceptance never grants stage, workflow, implementation or external authority.
- [ ] Preferences use schema/version/enums/catalog+analysis hashes and decision provenance.
- [ ] CREATE and UPDATE are distinct; UPDATE preserves history/unrelated fields.
- [ ] Missing directory creation appears in the exact changeset preview.
- [ ] Writes use raw-hash compare-and-set, atomic write and read-back verification.
- [ ] Concurrent preference changes block without merge/overwrite.
- [ ] Existing review mode may be recorded as observed and a different preference selected without mutating it.
- [ ] Agent/director/gate roles never approve stage.
- [ ] Exactly one next workflow or Stop is returned and never auto-run.
- [ ] COMPLETE means onboarding interaction only, not project/gate completion.
- [ ] Metadata discloses non-authoritative preference writes and catalog routing.

## Case 1: Fresh onboarding without persistence

**Input**

~~~text
$start
~~~

No analysis or preference exists.

**Expected**

The workflow asks user intent, reports `Analysis State: NOT_SUPPLIED` and
`Stage Authority: UNKNOWN`, derives only a safe catalog route or UNKNOWN, writes
nothing, returns `Persistence: NOT_REQUESTED`, one next action or Stop, and no stage
completion claim.

## Case 2: File existence does not promote stage

GDD, architecture and source files exist, but no stage analysis is supplied.

**Expected**

The result remains analysis NOT_SUPPLIED/stage UNKNOWN. The workflow does not scan
those directories, infer Systems Design/Technical Setup, change stage, or skip
catalog prerequisites.

## Case 3: Current stage-detection packet

Supply a byte-hash-matched complete `project_stage_detection/v2` packet with
`result: DETECTED`, a current target/source snapshot, valid authority/receipt counts,
and only current VALID/NOT_APPLICABLE evidence.

**Expected**

The packet may constrain catalog routing, but is labeled advisory and never treated
as a gate or transition. The workflow does not recreate detector heuristics. Any
recommended workflow is still resolved from the typed catalog with its exact command,
hash, and dependencies.

## Case 4: Unknown, conflicting, partial, or stale detection

Use each of: packet-byte mismatch, `UNKNOWN`, `CONFLICT`, one changed source hash,
and one unavailable required receipt.

**Expected**

Analysis is unsafe. Satisfied state is not inferred, unsafe later routes are
withheld, workflow status is PARTIAL, and a typed re-detection route is recommended
only when present in the catalog.

## Case 5: No stage mutation

Existing `production/stage.txt` contains any value.

**Expected**

Its bytes/hash are reported as OBSERVED_ONLY. The file is never created, edited,
deleted, renamed, normalized or used as proof. Every result says
`Authoritative Stage Mutation: NONE`.

## Case 6: Review preference is non-authoritative

Observed review mode is lean; the user prefers full.

**Expected**

Preferences may record `Review Mode Preference: full` and the observed lean hash.
The configuration file remains unchanged. No contradiction is hidden.

## Case 7: Preference CREATE includes directories

**Input**

~~~text
$start --persist
~~~

The preference target and both parent directories are absent.

**Expected**

Preview lists creation of `production/`, `production/onboarding/`, and the exact file.
After approval, atomic create/read-back succeeds. No other file or directory is
created.

## Case 8: Preference UPDATE preserves history

A valid schema-1 preference exists. User changes intent/review preference.

**Expected**

Operation is UPDATE; unrelated fields and prior decision/risk history are preserved,
a new immutable decision event is appended, and the exact field diff/preimage/output
hash is shown.

## Case 9: Concurrent UPDATE conflict

After preview, another actor changes the preference bytes.

**Expected**

CAS fails, operation CONFLICT, workflow BLOCKED, no merge/overwrite, and stage/review
mode remain untouched.

## Case 10: Invalid existing preferences

Existing preference has unsupported schema, duplicate decision ID, or invalid enum.

**Expected**

Writes block; the file is not replaced with a new document. Read-only guidance may
continue with limitations shown.

## Case 11: Catalog-derived route changes automatically

Two catalog fixtures differ only in the command/dependency of the same stable workflow
ID.

**Expected**

The recommendation follows each fixture without changing this skill. No embedded
roadmap or stale hardcoded command is used.

## Case 12: Missing or invalid catalog

Catalog is missing, duplicated, unsupported or lacks typed route metadata.

**Expected**

Route is BLOCKED/UNKNOWN, no guessed command, and persistence records the limitation
only if authorized.

## Case 13: Correct concept artifact routing

A current analysis says an existing `game-concept` needs review. Catalog has one
concept-profile reviewer and one system-GDD-only reviewer.

**Expected**

Only the concept-profile entry is eligible. Removing its accepted artifact type
produces a catalog gap/UNKNOWN rather than routing to the system-GDD rubric.

## Case 14: Fresh idea route

User selects no idea or vague idea. Catalog contains a workflow explicitly accepting
open-ideation or idea-hint input.

**Expected**

That stable entry is the single recommendation. The skill does not print a copied
full studio pipeline or make an engine recommendation.

## Case 15: Missing concept, risk declined

Analysis marks concept as an unsatisfied predecessor. User declines risk.

**Expected**

Recommend the first missing concept step or Stop. Requirement remains UNSATISFIED;
no later technical route is presented as READY.

## Case 16: Missing concept, risk accepted

User explicitly asks for later technical work and accepts the bounded consequences.

**Expected**

One `accepted-risk/missing-concept` record contains missing requirement IDs, chosen
workflow, user/decision/time, consequences, expiry/review, remediation and
catalog/analysis hashes. Route is AT_RISK; concept/gate/stage remain unsatisfied and
no workflow is run.

## Case 17: Role recommendations are not approvals

A stage analysis, producer/director prose or observed stage label says the project is
ready.

**Expected**

Without current required evidence receipts, start does not mark a step/stage complete.
No model or role label becomes authority.

## Case 18: Declined persistence remains visible

The user declines the preferences changeset.

**Expected**

Return Preference Operation/Persistence DECLINED, exact proposed values, route and
analysis limitations, plus unchanged stage/review-mode hashes. Do not collapse output
to a misleading success line.

## Case 19: Returning project first unmet step

A returning project has many artifacts and a CURRENT analysis with ordered required
steps; the third is the first unmet one.

**Expected**

Recommend exactly the third catalog entry. Do not guess sprint planning or skip it
because later files exist.

## Case 20: No automatic handoff

Any route is READY or AT_RISK.

**Expected**

The result contains one recommendation or Stop and invokes nothing. COMPLETE, if
reported, is explicitly onboarding completion only.

## Protocol compliance

- [ ] Start records intent/preferences, not authoritative project progress.
- [ ] Stage analysis and catalog own evidence/routing truth.
- [ ] Concept artifacts use typed review routes.
- [ ] Missing-concept risk remains visible and non-passing.
- [ ] Preference persistence is bounded, schema-valid and CAS-protected.
- [ ] Output preserves conflict/decline/partial state and stops.
