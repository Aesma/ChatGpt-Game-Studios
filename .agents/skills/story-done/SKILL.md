---
name: story-done
description: "Fail-closed end-of-story closure evaluator. Validates immutable story requirements, current tracker IN_REVIEW state, exact dev-story lifecycle receipts and test/review/QA evidence, then requests the unique tracker recorder to commit a tracker-only done transition."
---

## Path-first integrity

Accept canonical project-relative paths directly; do not require a caller-supplied
content-derived token. Validate project-root containment, regular-file type, declared
schema/version, stable IDs, permissions, lifecycle state, and path or ID collisions.
Allocate collision-safe IDs independently of file bytes. Before any permitted write,
re-read referenced records and target state, preview the exact authorized changes,
then use same-directory staging plus atomic replacement and rollback on failure.


# Story Done

## Invocation, authority, and outcomes

Invoke as `$story-done [story-file-path] [--review full|lean|solo]`. The path is optional only for bounded selection from the canonical active sprint tracker. Resolve review mode once from the argument, then `production/review-mode.txt`, then `lean`.

This workflow owns closure evaluation and the exact request for the tracker-row `in_review -> done` transition. It does not own story author bytes, the sprint plan, planning revisions, or the tracker file. The tracker-declared `lifecycle_recorder: cgs.sprint-tracker/v2` is the sole canonical lifecycle writer. `$dev-story` ends at a verified tracker row `in_review`; reject any dev result or transaction claiming Complete/Done.

Return exactly one verdict:

- `COMPLETE`: every required criterion, type obligation, source/readiness check, QA check, and required code review passes on current revisions, and the tracker lifecycle recorder returns a verified `COMMITTED` closure receipt with the row exactly `done`.
- `COMPLETE WITH NOTES`: the same closure conditions hold, with only predeclared optional items, a valid review waiver, or non-blocking findings remaining.
- `BLOCKED`: any required input, evidence, owner decision, current binding, gate, recorder capability, atomic conflict check precondition, commit, or receipt is absent, invalid, stale, partial, failed, or ambiguous.

A closable evidence verdict is not a lifecycle transition. Report completion only after the unique tracker lifecycle recorder returns a verified `COMMITTED` receipt. Before mutation, present the exact tracker-only proposal, tracker prior state revision/revision/event, requested owned row fields, preserved planning tuple, receipt destination, authorization binding, and rollback contract. One explicit approval covers that unchanged request. A different path, byte sequence, precondition, or material intent requires a new preview.

## Versioned contracts

The workflow consumes and emits these explicit schemas:

- `cgs.dev-story-result/v2`
- `cgs.dev-story-plan/v2`
- `cgs.dev-story-status-transition-proposal/v2`
- `cgs.dev-story-status-transaction/v2` (recorder result/receipt)
- `cgs.dev-story-checkpoint/v2`
- `cgs.dev-story-test-execution/v2`
- `cgs.sprint-tracker/v2`
- `cgs.story/v2` (immutable author artifact)
- `cgs.story-readiness-record/v1`
- `cgs.story-readiness-recorder-receipt/v1`
- `cgs.manual-evidence/v1`
- `cgs.team-qa-result/v2`
- `cgs.team-qa-signoff/v2`
- `cgs-test-evidence-review-report/v2`
- `cgs.story-review-policy/v1`
- `cgs.review-evidence/v1`
- `cgs.code-review/v2`
- `cgs.code-review-recorder-receipt/v1`
- `cgs.review-waiver/v1`
- `cgs.design-equivalence-decision/v1`
- `cgs.story-closure-transaction/v1` (tracker-only closure proposal)
- `cgs.story-closure-receipt/v1` (lifecycle-recorder receipt)

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

Stable IDs are required. Preserve explicit story and AC IDs. Test IDs, evidence IDs, QA finding IDs, review IDs, owner-decision IDs, and transaction IDs must be unique within the story and must not be generated from timestamps or prose alone. When a legacy story lacks an AC ID, use `AC-{ordinal}@{plan_revision}` only as a run-local identity bound to the exact approved criterion mapping. Do not fuzzy-match by wording.

## Phase 0: Select and freeze the closure subject

When a path is supplied, read exactly that immutable story file. Otherwise read the canonical active `cgs.sprint-tracker/v2` and select only an unambiguous row with status `in_review`; multiple candidates require user selection. Session prose may be a non-authoritative navigation hint only and cannot select or prove lifecycle state.

Read the story in full and record its raw `story_baseline_revision`. Require a stable story ID/path and immutable requirement core matching the tracker row and dev-story result. The canonical tracker row, not story frontmatter or prose, must be exactly `in_review`. Any other or unknown state is `BLOCKED`.

Resolve and revision the complete input set before evaluating evidence:

1. immutable story bytes, `cgs.dev-story-result/v2`, its exact `cgs.dev-story-plan/v2`, the final `cgs.dev-story-status-transition-proposal/v2`, and verified `cgs.dev-story-status-transaction/v2` result/receipt;
2. Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.
3. the current control manifest, active TR registry entries, governing Accepted ADRs, GDDs, Definition-of-Done profile, review policy, and all additional sources named by the story, plan, or result;
4. the persisted readiness record and recorder receipt, test-execution/manual evidence, Team QA result/signoff, optional persisted evidence-review report, code-review envelope/extension and recorder receipt or waiver, and owner decision records; and
5. every implementation, test, config, runtime-input, log, screenshot, build, and artifact path referenced by those records.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

## Phase 1: Require current readiness

Require one persisted `cgs.story-readiness-record/v1` and its matching immutable
`cgs.story-readiness-recorder-receipt/v1`. The record must identify the exact
current story ID/path/declared revision, have final verdict `READY`,
`evaluation_state: COMPLETE`, `persistence_status: PERSISTED`, zero unknown
required evidence, and `implementation_gate_eligible: true`. Its complete stale
key must name every story, GDD, systems-index, TR registry/entry, ADR,
control-manifest, dependency, asset, AC/Test/QA-plan, sprint/context,
review-mode, reviewer, checker, and ruleset identity used by readiness.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

`STRUCTURED_ACCEPTED_RISK`, `STALE / ACCEPTED-RISK`, and a persisted
`NEEDS_WORK` record may explain a dev-story result but are not closure
readiness. They must return to the readiness owner for a current persisted READY
record before story-done can close the story.

Do not refresh provenance or run a readiness authoring workflow here. Route
stale inputs to their owner.

## Phase 2: Validate the dev-story result and exact executions

Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.

Require its exact `cgs.dev-story-plan/v2`. Each plan test row must contain stable Test ID and mapped AC IDs; kind; exact argv-token array; normalized cwd; environment allowlist; positive bounded timeout; runner/tool name, version, and executable revision or structured not-applicable reason; source/build identity; expected exit/result/assertion contract; and raw-log path, prior state, derivation-contract revision, and byte limit. No Test ID may appear twice under conflicting definitions, every required AC must have deterministic evidence, and free-form shell text or a closure-time replacement command is invalid.

Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

## Phase 3: Resolve criteria and story-type evidence

Every acceptance criterion is required unless its optional/non-blocking
classification existed before plan approval and is bound by the unchanged story,
  Definition-of-Done profile, dev-story result, and plan revisions. A closure-time
request cannot downgrade a criterion.

For each AC emit `PASS`, `FAIL`, `UNTESTED`, `DEFERRED`, or `STALE`.
`COVERED` is only a mapping state. A required AC passes only through direct,
current automated evidence from Phase 2 or a valid
`cgs.manual-evidence/v1` record containing:

- stable evidence ID and exact AC ID;
- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
- reproducible steps and observed result;
- explicit `PASS`;
- tester identity, ISO-8601 session timestamp, and session ID;
- artifact and sign-off IDs with paths/revisions; and
- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

A conversational confirmation, checklist, filename, symbol, keyword, numeric
scan, static inspection, or name similarity is a finding only. It never marks an
AC `PASS`, `COVERED`, or `VERIFIED`. A changed tree, build, artifact, story,
plan, result, or execution-set revision makes dependent evidence `STALE`.

Apply the blocking default evidence matrix unless an unchanged, predeclared
Definition-of-Done profile supplies a stricter or explicitly approved method.

| Story Type | Blocking evidence |
|---|---|
| Logic | Current passing automated unit-test evidence for every required logic AC |
| Integration | Current passing integration evidence or a current revision-bound manual end-to-end session for every required integration AC |
| Visual/Feel | Current revision-bound manual session, declared screenshots/artifacts, and all required sign-offs |
| UI | Current manual walkthrough with artifacts or passing automated interaction evidence, plus declared sign-offs |
| Config/Data | Current passing smoke evidence bound to the exact tree/data revisions |

Missing/unknown Story Type, evidence, artifact, or sign-off is `BLOCKED`.
Every required AC must PASS. An optional AC may be `DEFERRED` only under its
predeclared classification and must appear in Completion Notes.

## Phase 4: Enforce QA coverage and risk-based code review

### QA coverage

Require an exact current `cgs.team-qa-result/v2` and its named immutable
`cgs.team-qa-signoff/v2`. Both must bind the same request, run, scope,
candidate/build/artifact/source, QA-plan, frozen evidence-manifest, independent
review, and signoff identities and revisions. Independently re-read both artifacts
and every referenced authority. The result must be terminal and persisted; the
signoff must state `QA_APPROVED` and `Gate Eligible: YES`, with every required
denominator row passing, all findings dispositioned, all required roles present,
and zero conditions or gaps.

`QA_APPROVED_WITH_CONDITIONS`, `QA_NOT_APPROVED`, `QA_INCOMPLETE`, Gate Eligible
NO, an unpersisted/stale/mismatched signoff, or any required `FAIL`, `BLOCKED`,
`NOT_RUN`, `UNKNOWN`, `STALE`, `INVALID`, missing, `PARTIAL`, `TIMEOUT`,
`CANCELLED`, or `LATE_IGNORED` row is closure-blocking. Team QA remains evidence
only: even current `QA_APPROVED` never grants closure, release, deployment, or
publication authority and never replaces direct per-AC evidence.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

### Code review

Resolve `cgs.story-review-policy/v1` from the unchanged Definition-of-Done
profile or a canonical project policy captured by the story, approved plan, and
dev-story result. The policy records policy ID/version/path/revision, story risk class,
Story Type, required reviewer roles, waiver authority, and whether waiver is
permitted.

The fail-closed default is:

- Logic and any story classified high risk require a current code review in
  every mode, including lean and solo.
- Other stories follow their predeclared policy; absent or ambiguous policy is
  `BLOCKED`, not an invitation to choose at closure.
- `No`, `skip`, missing reviewer, or a mode-based skip is `BLOCKED` when
  review is required.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.

QA and code review cannot manufacture PASS acceptance evidence or override any
readiness, source, type, or AC blocker.

## Phase 5: Enforce design conformance and owner decisions

Compare the current implementation/evidence against exact active TRs, GDD rules,
Accepted ADRs, control-manifest constraints, and approved scope. Give each
deviation a stable finding ID and bind the source ID/path/locator/revision, subject
path/revision, evidence IDs, severity, owner, and status.

Any mismatch is blocking by default. The workflow, model, implementer, reviewer,
or user conversation must not label a mismatch "functionally equivalent" from
subjective inspection.

An equivalence exception exists only through a current
`cgs.design-equivalence-decision/v1` authored by the designated product or
architecture owner. It binds:

- stable decision ID, owner identity/role, authority source path/revision, and
  signature/attestation path/revision;
- exact TR/GDD/ADR/control rule IDs, paths, locators, and revisions;
- exact implementation paths/revisions and affected AC IDs;
- compared semantics, accepted equivalence scope, constraints, non-goals,
  residual risks, and required regression evidence IDs;
- story, dev-story plan/result, execution-set, and verification-tree revisions;
- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

The decision applies only to its exact scope and revisions. Missing authority,
ambiguous scope, stale bytes, expired/revoked status, or uncovered residual risk
is `BLOCKED`. An owner decision may resolve the named design mismatch; it
cannot waive missing behavior evidence, QA, review, or type obligations.

## Phase 6: Compute the evidence verdict

Compute before any mutation.

The evidence verdict is `BLOCKED` when any required schema, ID, path, revision,
source, current readiness check, AC result, Story Type obligation, QA result,
required review, owner decision, or recorder prerequisite fails.

The evidence verdict is `COMPLETE` when all required checks pass, provenance
is `READY`, and there are no valid non-blocking notes.

The evidence verdict is `COMPLETE WITH NOTES` only when complete conditions
hold and all remaining notes come from predeclared optional ACs, a valid review
waiver, or advisory findings affecting no
required obligation.

Present the story baseline, dev-story result/plan/status transaction, persisted
readiness record/recorder receipt, execution set, verification tree, QA,
review/waiver, owner decisions, and proposed transaction
revisions. List every AC with required flag, evidence IDs, method, freshness, QA
finding IDs, and result. List type evidence and every finding. For
`BLOCKED`, write nothing and name the exact owner/evidence needed. No
close-anyway branch exists.

## Phase 7: Close through the tracker lifecycle recorder

Only a closable evidence verdict may prepare `cgs.story-closure-transaction/v1`. It is a tracker-only lifecycle proposal. Story-done never writes the tracker, story, sprint plan, session state, planning revisions, or evidence artifacts directly.

The proposal contains:

- schema, transaction ID, story/dev-result/plan/readiness/dev-transition/execution-set/tree/QA/review/waiver/owner-decision identities and revisions;
- Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.
- the requested transition for exactly one matching row, `in_review -> done`, plus only tracker-declared lifecycle-owned completion timestamp/provenance fields;
- the frozen `plan_file`, `plan_file_revision`, `plan_revision`, and `story_set_revision` as preservation assertions, never recomputed proposed values;
- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
- receipt create-only destination, recorder implementation/version/capability identity, rollback contract, and authorization identity bound to the exact proposal revision.

Invoke only the tracker-declared lifecycle recorder. Require compare-and-swap on the exact tracker declared revision, revision, event, sprint identity, lifecycle owner, planning tuple, and story-row prior state. The recorder must stage the exact tracker replacement and immutable receipt, verify revisions, commit both or restore the complete tracker prior state, support crash recovery, and reject an existing non-identical receipt destination. No last-writer-wins retry or silent replacement transaction is allowed.

Immediately before commit, re-read every read/source/evidence input, immutable story, plan, and tracker prior state. Any mismatch aborts with zero committed canonical changes. After commit, independently reread the tracker, story, plan, and receipt.

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

`ABORTED`, `ROLLED_BACK`, `RECOVERY_REQUIRED`, receipt failure, read-back mismatch, atomic conflict check conflict, unowned change, planning-revision change, or ambiguous/partial recorder result means no successful closure. Preserve or restore the tracker row to `in_review`, emit exact recovery evidence, and do not mint a replacement transaction silently.

Only after a verified `COMMITTED` receipt and independent read-back may the final verdict be `COMPLETE` or `COMPLETE WITH NOTES`.

## Phase 8: Handoff

Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.

## Non-negotiable rules

- Static presence or keyword checks never PASS an AC.
- Every required AC and Story Type obligation needs direct current PASS evidence.
- Test execution consumes the exact revision-bound dev-story plan and immutable `cgs.dev-story-test-execution/v2` records.
- Required QA gaps are blocking.
- Logic/high-risk review cannot disappear in lean or solo mode.
- Readiness requires a current persisted READY record, matching recorder receipt, and `implementation_gate_eligible: true`.
- Design equivalence belongs only to a current authorized owner decision.
- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
- `plan_file`, `plan_file_revision`, `plan_revision`, and `story_set_revision` remain immutable; story-done never recomputes them.
- Canonical lifecycle exists only in the matching `cgs.sprint-tracker/v2` row, and only its declared lifecycle recorder may change owned lifecycle fields.
- Dev-story ends at `in_review`; story-done may request but never directly write `done`.
- No required gap can be hidden in notes or overridden conversationally.
