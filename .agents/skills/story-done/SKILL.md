---
name: story-done
description: "Fail-closed end-of-story closure evaluator. Validates immutable story requirements, current tracker IN_REVIEW state, exact dev-story lifecycle receipts and test/review/QA evidence, then requests the unique tracker recorder to commit a tracker-only done transition."
---

# Story Done

## Invocation, authority, and outcomes

Invoke as `$story-done [story-file-path] [--review full|lean|solo]`. The path is optional only for bounded selection from the canonical active sprint tracker. Resolve review mode once from the argument, then `production/review-mode.txt`, then `lean`.

This workflow owns closure evaluation and the exact request for the tracker-row `in_review -> done` transition. It does not own story author bytes, the sprint plan, planning hashes, or the tracker file. The tracker-declared `lifecycle_recorder: cgs.sprint-tracker/v2` is the sole canonical lifecycle writer. `$dev-story` ends at a verified tracker row `in_review`; reject any dev result or transaction claiming Complete/Done.

Return exactly one verdict:

- `COMPLETE`: every required criterion, type obligation, source/readiness check, QA check, and required code review passes on current hashes, and the tracker lifecycle recorder returns a verified `COMMITTED` closure receipt with the row exactly `done`.
- `COMPLETE WITH NOTES`: the same closure conditions hold, with only predeclared optional items, a valid review waiver, or non-blocking findings remaining.
- `BLOCKED`: any required input, evidence, owner decision, current binding, gate, recorder capability, CAS precondition, commit, or receipt is absent, invalid, stale, partial, failed, or ambiguous.

A closable evidence verdict is not a lifecycle transition. Report completion only after the unique tracker lifecycle recorder returns a verified `COMMITTED` receipt. Before mutation, present the exact tracker-only proposal, tracker preimage hash/revision/event, requested owned row fields, preserved planning tuple, receipt destination, authorization binding, and rollback contract. One explicit approval covers that unchanged request. A different path, byte sequence, precondition, or material intent requires a new preview.

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

Schema identity, canonical path, and raw-byte SHA-256 are mandatory whenever a contract is consumed. Unknown versions are `BLOCKED`; do not coerce them. All SHA-256 values use `sha256:` followed by exactly 64 lowercase hexadecimal characters.

Stable IDs are required. Preserve explicit story and AC IDs. Test IDs, evidence IDs, QA finding IDs, review IDs, owner-decision IDs, and transaction IDs must be unique within the story and must not be generated from timestamps or prose alone. When a legacy story lacks an AC ID, use `AC-{ordinal}@{plan_hash}` only as a run-local identity bound to the exact approved criterion mapping. Do not fuzzy-match by wording.

## Phase 0: Select and freeze the closure subject

When a path is supplied, read exactly that immutable story file. Otherwise read the canonical active `cgs.sprint-tracker/v2` and select only an unambiguous row with status `in_review`; multiple candidates require user selection. Session prose may be a non-authoritative navigation hint only and cannot select or prove lifecycle state.

Read the story in full and record its raw `story_baseline_hash`. Require a stable story ID/path and immutable requirement core matching the tracker row and dev-story result. The canonical tracker row, not story frontmatter or prose, must be exactly `in_review`. Any other or unknown state is `BLOCKED`.

Resolve and hash the complete input set before evaluating evidence:

1. immutable story bytes, `cgs.dev-story-result/v2`, its exact `cgs.dev-story-plan/v2`, the final `cgs.dev-story-status-transition-proposal/v2`, and verified `cgs.dev-story-status-transaction/v2` result/receipt;
2. the canonical sprint plan and `cgs.sprint-tracker/v2`, including raw tracker hash, `tracker_revision`, `event_id`, sprint identity/state, `lifecycle_owner`, `lifecycle_recorder`, and frozen `plan_file`/`plan_sha256`/`plan_revision`/`story_set_hash`;
3. the current control manifest, active TR registry entries, governing Accepted ADRs, GDDs, Definition-of-Done profile, review policy, and all additional sources named by the story, plan, or result;
4. the persisted readiness record and recorder receipt, test-execution/manual evidence, Team QA result/signoff, optional persisted evidence-review report, code-review envelope/extension and recorder receipt or waiver, and owner decision records; and
5. every implementation, test, config, runtime-input, log, screenshot, build, and artifact path referenced by those records.

Reject path aliases such as `latest`, ambiguous duplicates, mutable external links without a content hash, missing files, malformed schemas, and any recorded/current hash mismatch. Freeze the story raw hash and planning tuple; closure must preserve them byte-for-byte.

## Phase 1: Require current readiness

Require one persisted `cgs.story-readiness-record/v1` and its matching immutable
`cgs.story-readiness-recorder-receipt/v1`. The record must identify the exact
current story ID/path/raw hash, have final verdict `READY`,
`evaluation_state: COMPLETE`, `persistence_status: PERSISTED`, zero unknown
required evidence, and `implementation_gate_eligible: true`. Its complete stale
key must name every story, GDD, systems-index, TR registry/entry, ADR,
control-manifest, dependency, asset, AC/Test/QA-plan, sprint/context,
review-mode, reviewer, checker, and ruleset identity used by readiness.

The recorder receipt must have result `RECORDED` or `ALREADY_RECORDED`, identify
the same record, candidate, readiness key, story raw hash, registry path, and
verified final registry hash, and bind its own raw-byte hash. Independently
reread and hash the record, receipt, registry, story, and every stale-key source.
The persisted registry entry must equal the consumed record bytes and the
receipt's final identity. A prior READY claim, direct candidate, changed story,
non-READY record, false/missing `implementation_gate_eligible`, stale key,
registry mismatch, or other recorder terminal is `BLOCKED`.

`STRUCTURED_ACCEPTED_RISK`, `STALE / ACCEPTED-RISK`, and a persisted
`NEEDS_WORK` record may explain a dev-story result but are not closure
readiness. They must return to the readiness owner for a current persisted READY
record before story-done can close the story.

Do not refresh provenance or run a readiness authoring workflow here. Route
stale inputs to their owner.

## Phase 2: Validate the dev-story result and exact executions

Require one immutable `cgs.dev-story-result/v2` at its canonical path and raw hash. Only outcome `IMPLEMENTED` is admissible. The result must bind the exact workflow/request/plan/authorization hashes, immutable story identity/hash, readiness record and receipt, owner domains, planned and actual write sets with per-file pre/post hashes, AC coverage, Test-ID executions, lifecycle transaction evidence, checkpoint identity `NONE`, mutation snapshot, and canonical result hash.

Require its exact `cgs.dev-story-plan/v2`. Each plan test row must contain stable Test ID and mapped AC IDs; kind; exact argv-token array; normalized cwd; environment allowlist; positive bounded timeout; runner/tool name, version, and executable hash or structured not-applicable reason; source/build identity; expected exit/result/assertion contract; and raw-log path, preimage, derivation-contract hash, and byte limit. No Test ID may appear twice under conflicting definitions, every required AC must have deterministic evidence, and free-form shell text or a closure-time replacement command is invalid.

For every planned Test ID require one immutable `cgs.dev-story-test-execution/v2` with the same invocation/source/build fields plus start/end RFC-3339 UTC timestamps, timeout state, exit code or exact unavailable reason, raw-log byte count/hash, assertion observations, normalized `PASS|FAIL|BLOCKED` result, canonical path, and raw record hash. Recompute the Test-ID-sorted result-set hash named by the dev-story result and lifecycle transaction. Only current-transaction PASS records that exactly match the plan, finish within timeout, provide complete current logs, and meet the expected contract support an AC. Missing, unrun, timed-out, nonzero, malformed, stale, hashless, truncated, changed, `FAIL`, or `BLOCKED` execution is closure-blocking.

Require the final `cgs.dev-story-status-transition-proposal/v2` and `cgs.dev-story-status-transaction/v2` result/receipt to prove the tracker recorder committed `in_progress -> in_review`. Independently rehash and reread the canonical tracker. Require matching proposal hash, lifecycle owner/recorder identities, exact tracker pre/post hashes, revision/event increment, result `COMMITTED`, final row `in_review`, unchanged immutable story bytes, and byte-for-byte preservation of `plan_file`, `plan_sha256`, `plan_revision`, `story_set_hash`, all unowned row fields, and every other tracker row. A referenced or discoverable unresolved checkpoint, ambiguous/partial receipt, non-`IN_REVIEW` row, or terminal-state claim by dev-story is `BLOCKED`.

Compute `verification_tree_hash` as SHA-256 over UTF-8 LF canonical lines, sorted by normalized path:

    plan_hash={sha256 plan hash}
    dev_story_result_hash={sha256 result hash}
    dev_story_plan_hash={sha256 plan hash}
    dev_story_transition_receipt_hash={sha256 receipt hash}
    test_execution_set_hash={sha256 Test-ID-sorted execution set hash}
    {normalized subject path}\tsha256:{raw subject hash}

Bind the immutable story and canonical tracker raw hashes separately and recheck them immediately before closure. Every automated and manual record must name the exact verification tree or its declared equivalent binding.

## Phase 3: Resolve criteria and story-type evidence

Every acceptance criterion is required unless its optional/non-blocking
classification existed before plan approval and is bound by the unchanged story,
  Definition-of-Done profile, dev-story result, and plan hashes. A closure-time
request cannot downgrade a criterion.

For each AC emit `PASS`, `FAIL`, `UNTESTED`, `DEFERRED`, or `STALE`.
`COVERED` is only a mapping state. A required AC passes only through direct,
current automated evidence from Phase 2 or a valid
`cgs.manual-evidence/v1` record containing:

- stable evidence ID and exact AC ID;
- tested tree hash and optional packaged-build path/hash;
- reproducible steps and observed result;
- explicit `PASS`;
- tester identity, ISO-8601 session timestamp, and session ID;
- artifact and sign-off IDs with paths/hashes; and
- dev-story result, story, plan, producer, canonical path, and evidence hashes.

A conversational confirmation, checklist, filename, symbol, keyword, numeric
scan, static inspection, or name similarity is a finding only. It never marks an
AC `PASS`, `COVERED`, or `VERIFIED`. A changed tree, build, artifact, story,
plan, result, or execution-set hash makes dependent evidence `STALE`.

Apply the blocking default evidence matrix unless an unchanged, predeclared
Definition-of-Done profile supplies a stricter or explicitly approved method.

| Story Type | Blocking evidence |
|---|---|
| Logic | Current passing automated unit-test evidence for every required logic AC |
| Integration | Current passing integration evidence or a current hash-bound manual end-to-end session for every required integration AC |
| Visual/Feel | Current hash-bound manual session, declared screenshots/artifacts, and all required sign-offs |
| UI | Current manual walkthrough with artifacts or passing automated interaction evidence, plus declared sign-offs |
| Config/Data | Current passing smoke evidence bound to the exact tree/data hashes |

Missing/unknown Story Type, evidence, artifact, or sign-off is `BLOCKED`.
Every required AC must PASS. An optional AC may be `DEFERRED` only under its
predeclared classification and must appear in Completion Notes.

## Phase 4: Enforce QA coverage and risk-based code review

### QA coverage

Require an exact current `cgs.team-qa-result/v2` and its named immutable
`cgs.team-qa-signoff/v2`. Both must bind the same request, run, scope,
candidate/build/artifact/source, QA-plan, frozen evidence-manifest, independent
review, and signoff identities and hashes. Independently rehash both artifacts
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

An optional durable evidence-review summary must be the producer's actual
`cgs-test-evidence-review-report/v2`, not its request manifest. Consume it only
from its exact canonical path/hash with `Persistence: WRITTEN`, Workflow Status
COMPLETE, Structural Quality ADEQUATE, Evidence Admissibility ADMISSIBLE,
Execution Result PASS, Execution Currency CURRENT, Execution Completeness
COMPLETE, Execution Scope FULL, Closure Eligible YES, and exact current
scope/candidate/build/artifact/input-set joins. It may summarize underlying
evidence but never substitutes for Team QA signoff or direct AC checks.

### Code review

Resolve `cgs.story-review-policy/v1` from the unchanged Definition-of-Done
profile or a canonical project policy captured by the story, approved plan, and
dev-story result. The policy records policy ID/version/path/hash, story risk class,
Story Type, required reviewer roles, waiver authority, and whether waiver is
permitted.

The fail-closed default is:

- Logic and any story classified high risk require a current code review in
  every mode, including lean and solo.
- Other stories follow their predeclared policy; absent or ambiguous policy is
  `BLOCKED`, not an invitation to choose at closure.
- `No`, `skip`, missing reviewer, or a mode-based skip is `BLOCKED` when
  review is required.

Require the producer's exact `cgs.review-evidence/v1` envelope with its embedded
`cgs.code-review/v2` extension. It must bind the complete target manifest and
raw hashes, rule chains/ledger, Accepted ADRs, tool evidence, reviewer
plan/results and roles, coverage gaps, stable findings, mutation guards, stale
key, producer identity, canonical path/raw hash, and verdict `APPROVED`. Complete
coverage, all required reviewers, unchanged before/after target hashes, zero
open BLOCKING/WARNING findings, and current inputs are mandatory.

The producer record alone is deliberately `gate_evidence_status: NOT_PERSISTED`
and `gate_evidence_eligible: false`; it cannot satisfy closure. Require an
independent external `cgs.code-review-recorder-receipt/v1` that names the exact
envelope path/raw hash and extension schema, independently rehashes every stale-
key input, and records result `RECORDED|ALREADY_RECORDED`, persistence status
`PERSISTED`, `gate_evidence_eligible: true`, recorder/authority identities,
registry path/base/final hashes and revision, lock/CAS/atomicity/read-back
evidence, timestamp, canonical receipt path, and receipt raw hash. Missing,
stale, unpersisted, mismatched, non-APPROVED, recorder-failed, or gate-ineligible
review evidence is `BLOCKED`.

A review waiver is accepted only when the predeclared policy permits it and a
current `cgs.review-waiver/v1` binds waiver ID, authorized risk owner,
policy/story/plan/result/tree hashes, exact skipped review, rationale,
conditions, expiry, signature/attestation path/hash, and waiver hash. It yields
at most `COMPLETE WITH NOTES`. A conversational risk acceptance is invalid.

QA and code review cannot manufacture PASS acceptance evidence or override any
readiness, source, type, or AC blocker.

## Phase 5: Enforce design conformance and owner decisions

Compare the current implementation/evidence against exact active TRs, GDD rules,
Accepted ADRs, control-manifest constraints, and approved scope. Give each
deviation a stable finding ID and bind the source ID/path/locator/hash, subject
path/hash, evidence IDs, severity, owner, and status.

Any mismatch is blocking by default. The workflow, model, implementer, reviewer,
or user conversation must not label a mismatch "functionally equivalent" from
subjective inspection.

An equivalence exception exists only through a current
`cgs.design-equivalence-decision/v1` authored by the designated product or
architecture owner. It binds:

- stable decision ID, owner identity/role, authority source path/hash, and
  signature/attestation path/hash;
- exact TR/GDD/ADR/control rule IDs, paths, locators, and hashes;
- exact implementation paths/hashes and affected AC IDs;
- compared semantics, accepted equivalence scope, constraints, non-goals,
  residual risks, and required regression evidence IDs;
- story, dev-story plan/result, execution-set, and verification-tree hashes;
- decision timestamp, expiry/revocation state, canonical path, and record hash.

The decision applies only to its exact scope and hashes. Missing authority,
ambiguous scope, stale bytes, expired/revoked status, or uncovered residual risk
is `BLOCKED`. An owner decision may resolve the named design mismatch; it
cannot waive missing behavior evidence, QA, review, or type obligations.

## Phase 6: Compute the evidence verdict

Compute before any mutation.

The evidence verdict is `BLOCKED` when any required schema, ID, path, hash,
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
hashes. List every AC with required flag, evidence IDs, method, freshness, QA
finding IDs, and result. List type evidence and every finding. For
`BLOCKED`, write nothing and name the exact owner/evidence needed. No
close-anyway branch exists.

## Phase 7: Close through the tracker lifecycle recorder

Only a closable evidence verdict may prepare `cgs.story-closure-transaction/v1`. It is a tracker-only lifecycle proposal. Story-done never writes the tracker, story, sprint plan, session state, planning hashes, or evidence artifacts directly.

The proposal contains:

- schema, transaction ID, story/dev-result/plan/readiness/dev-transition/execution-set/tree/QA/review/waiver/owner-decision identities and hashes;
- exact canonical tracker path, external raw preimage hash, expected `tracker_revision`, `event_id`, sprint identity/state, lifecycle owner, and `lifecycle_recorder: cgs.sprint-tracker/v2`;
- the requested transition for exactly one matching row, `in_review -> done`, plus only tracker-declared lifecycle-owned completion timestamp/provenance fields;
- the frozen `plan_file`, `plan_sha256`, `plan_revision`, and `story_set_hash` as preservation assertions, never recomputed proposed values;
- immutable story path/raw hash and assertions that story bytes/Revision, every unowned tracker field, and every other tracker row remain byte-for-byte unchanged;
- receipt create-only destination, recorder implementation/version/capability identity, rollback contract, and authorization identity bound to the exact proposal hash.

Invoke only the tracker-declared lifecycle recorder. Require compare-and-swap on the exact tracker raw hash, revision, event, sprint identity, lifecycle owner, planning tuple, and story-row preimage. The recorder must stage the exact tracker replacement and immutable receipt, verify hashes, commit both or restore the complete tracker preimage, support crash recovery, and reject an existing non-identical receipt destination. No last-writer-wins retry or silent replacement transaction is allowed.

Immediately before commit, rehash every read/source/evidence input, immutable story, plan, and tracker preimage. Any mismatch aborts with zero committed canonical changes. After commit, independently reread the tracker, story, plan, and receipt.

Accept only `cgs.story-closure-receipt/v1` with transaction/proposal/authorization/recorder IDs and hashes; result `COMMITTED`; timestamp and recovery state `NOT_REQUIRED`; tracker pre/post/read-back raw hashes; exact revision/event increment; observed row transition `in_review -> done`; the precise lifecycle-owned field set; unchanged planning tuple, unowned fields, other rows, story bytes/Revision, and plan bytes; and receipt path/hash.

`ABORTED`, `ROLLED_BACK`, `RECOVERY_REQUIRED`, receipt failure, read-back mismatch, CAS conflict, unowned change, planning-hash change, or ambiguous/partial recorder result means no successful closure. Preserve or restore the tracker row to `in_review`, emit exact recovery evidence, and do not mint a replacement transaction silently.

Only after a verified `COMMITTED` receipt and independent read-back may the final verdict be `COMPLETE` or `COMPLETE WITH NOTES`.

## Phase 8: Handoff

After successful tracker closure, re-read the same current tracker and surface up to three dependency-ready Must Have or Should Have rows. Recommend `$story-readiness [path]`. Do not rewrite the story or sprint plan, recompute planning hashes, update session prose, execute another workflow, commit, push, publish, or modify implementation/source files automatically.

## Non-negotiable rules

- Static presence or keyword checks never PASS an AC.
- Every required AC and Story Type obligation needs direct current PASS evidence.
- Test execution consumes the exact hash-bound dev-story plan and immutable `cgs.dev-story-test-execution/v2` records.
- Required QA gaps are blocking.
- Logic/high-risk review cannot disappear in lean or solo mode.
- Readiness requires a current persisted READY record, matching recorder receipt, and `implementation_gate_eligible: true`.
- Design equivalence belongs only to a current authorized owner decision.
- `cgs.story/v2` bytes and Revision are immutable during implementation and closure.
- `plan_file`, `plan_sha256`, `plan_revision`, and `story_set_hash` remain immutable; story-done never recomputes them.
- Canonical lifecycle exists only in the matching `cgs.sprint-tracker/v2` row, and only its declared lifecycle recorder may change owned lifecycle fields.
- Dev-story ends at `in_review`; story-done may request but never directly write `done`.
- No required gap can be hidden in notes or overridden conversationally.
