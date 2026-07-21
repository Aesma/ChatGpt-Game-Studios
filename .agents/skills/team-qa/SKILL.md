---
name: team-qa
description: "Orchestrate an evidence-bound QA cycle for one exact build candidate, separating workflow completion from the QA verdict and refusing approval when required evidence is missing, stale, blocked, not run, or unverifiable."
---

# Team QA

Coordinate `qa-lead` and `qa-tester` for one immutable build candidate. This skill
is an orchestrator and evidence consumer. It does not turn plans, chat selections,
agent summaries, filenames, or modification times into test results.

## Invocation

Use one explicit mode:

```text
$team-qa start <scope-id> --run-id <qa-run-id> --candidate <candidate-manifest-path> --qa-plan <qa-plan-path> --smoke-receipt <smoke-report-path>
$team-qa ingest <qa-run-id> --automated-receipt <path>
$team-qa ingest <qa-run-id> --manual-evidence <path>
$team-qa ingest <qa-run-id> --playtest-result <path>
$team-qa ingest <qa-run-id> --soak-result <path>
$team-qa status <qa-run-id>
$team-qa finalize <qa-run-id> --evidence-review <review-report-path>
```

All paths are exact. Reject glob-only, "latest", "most recent", directory-only, and
modification-time selection. A changed build or changed scope starts a new
`qa-run-id`; never mutate an old run to point at a different candidate.

Before the first authorized write, present one complete changeset with every
CREATE path and all explicit non-writes. An invocation that explicitly authorizes
the bounded operation may serve as that authorization. Otherwise obtain one
approval for the complete changeset. Do not re-prompt file by file. If the scope
expands, stop and obtain a new bounded authorization.

This workflow has no review-mode or director-gate branch. It never reads or writes
`production/review-mode.txt` and never writes session state.

## Team and authority

- `qa-lead` may classify risk, draft the strategy, map requirements to evidence,
  and assess the frozen evidence index.
- `qa-tester` may draft test cases and transcribe already-produced evidence into
  the required schema.
- Agent output, a user's chat choice, and a qa-lead recommendation are not
  execution evidence and cannot set a test to PASS.
- Independent tasks may run concurrently only when each owns disjoint proposed
  paths. The orchestrator is the sole publisher of the run manifest, evidence
  index, and signoff.

If subagents are unavailable, perform the same bounded responsibilities locally.
Report every unavailable or timed-out assignment in Workflow Status; do not omit
its required rows.

## Artifact ownership and canonical layout

This skill owns only a fresh directory:

```text
production/qa/team-runs/<qa-run-id>/
  manifest.md
  strategy.md
  cases/<case-id>.md
  evidence/<evidence-id>.md
  evidence-index.md
  signoff.md
```

Reject an existing `qa-run-id` on `start`. Ingest creates a new immutable evidence
record and never overwrites source receipts. Finalize creates `evidence-index.md`
and `signoff.md` only once. Status is read-only.

The run manifest must record:

- artifact type `team-qa-run-manifest` and schema version 1;
- run ID, scope ID, normalized scope type, and ordered in-scope story/requirement
  identifiers;
- exact candidate manifest path and SHA-256;
- candidate ID, build ID/version/hash, artifact path/hash, source commit,
  platform, configuration, and environment;
- exact QA-plan path and SHA-256 plus Effective Plan State;
- exact smoke-report path and SHA-256, candidate/run ID, verdict, and handoff flag;
- creation timestamp and hash algorithm `sha256`.

Every persisted artifact contains its own artifact type, schema version, run ID,
candidate/build identity, source references and hashes, status, and timestamp.
Use repository-relative canonical paths in artifacts. Verify every proposed byte,
write transactionally, re-read the result, and report its SHA-256. A declined or
failed write changes Persistence, never the evidence assessment.

## Status axes

Always report these separately:

- `Workflow Status`: `STARTED`, `RUNNING`, `COMPLETE`, `PARTIAL`, or
  `BLOCKED_AT_ENTRY`.
- `QA Verdict`: `APPROVED`, `APPROVED_WITH_CONDITIONS`, `NOT_APPROVED`, or
  `INCOMPLETE`.
- `Gate Eligible`: `YES` only for `QA Verdict: APPROVED` after a verified,
  persisted `signoff.md`; otherwise `NO`.
- `Persistence`: `NOT_REQUESTED`, `DECLINED`, `VERIFIED`, or `FAILED`.

`Workflow Status: COMPLETE` means the declared review work finished. It never
means tests passed. A complete run may have `QA Verdict: NOT_APPROVED` or
`INCOMPLETE`.

## Phase 1: Resolve exact scope and candidate

For `start`, require the caller to supply all three exact inputs: candidate
manifest, QA plan, and smoke report. Do not infer a sprint, build, platform,
environment, plan, or report from session state, directory contents, or mtime.

Validate the candidate manifest as a structured `build-candidate` receipt. Require
its manifest version, hash algorithm, candidate ID, build ID/version/hash,
artifact path and artifact SHA-256, source commit, engine, platform,
configuration, environment, creation time, and referenced file hashes. Re-hash
the manifest and build artifact. Ambiguous, missing, unreadable, or mismatched
identity yields:

```text
Workflow Status: BLOCKED_AT_ENTRY
QA Verdict: INCOMPLETE
Gate Eligible: NO
Reason: BUILD CANDIDATE EVIDENCE REQUIRED
```

The only permitted output before a valid entry gate is a draft strategy/test plan
in conversation. Do not create the run directory, cases, execution records,
evidence index, bugs, or signoff.

## Phase 2: Revalidate the QA plan

Read the exact QA-plan path. Require the staged `qa-plan` contract: manifest
version 1, `hash_algorithm: sha256`, mandatory Sources table, Story Requirement Bindings, Test Summary, Smoke Test
Scope, stable story/AC/test/check IDs, and
`Plan State at Generation: CURRENT`.

Re-hash every captured source now. Compute Effective Plan State rather than
trusting the stored label:

- `CURRENT` only when every required source and binding still matches;
- `PARTIAL` when required scope or bindings are absent;
- `STALE` when any captured source hash changed.

Only `CURRENT` may proceed. `PARTIAL` or `STALE` returns
`BLOCKED_AT_ENTRY / INCOMPLETE / Gate Eligible: NO` and writes nothing. Never
choose a plan by filename date or mtime.

Create the ordered required-evidence ledger from stable IDs. Each row must identify
story ID, AC ID, test/check ID, method, required scope, required platform or
device, and expected artifact type. The ledger defines the denominator used at
signoff.

An exclusion may remove a row from the required denominator only when an explicit,
persisted approval record names the row ID, reason, approver, timestamp, scope
hash, QA-plan hash, and candidate hash. List exclusions separately; silence,
"not applicable" text, or an agent decision is not approval.

## Phase 3: Enforce the smoke handoff gate

Read only the exact supplied path:

`production/qa/evidence/smoke/<candidate-id>/<smoke-run-id>/report.md`

Require the staged `smoke-check` receipt contract:

- artifact type `smoke-check-receipt`, schema version 1, and persisted report hash;
- exact candidate manifest path/hash, candidate ID, build identity, artifact hash,
  source commit, platform/configuration/environment, and exact QA-plan path/hash;
- current recomputed QA Plan Effective State `CURRENT`;
- mode `sprint`, `Verdict: PASS`, `Handoff Eligible: YES`, and no warnings,
  unknowns, invalid rows, missing rows, or nonconclusive results;
- referenced automated receipt, logs, and manual evidence exist and re-hash.

`TARGETED CHECK PASSED`, quick mode, `FAIL`, `INCOMPLETE`, `UNKNOWN`, a warning,
a missing/unpersisted report, a stale hash, or a candidate/build mismatch is not a
handoff. Return exactly:

```text
Workflow Status: BLOCKED_AT_ENTRY
QA Verdict: INCOMPLETE
Gate Eligible: NO
Reason: SMOKE EVIDENCE REQUIRED
```

A smoke failure may additionally be reported as a current failure, but the team
cycle still does not execute and no signoff is created. Only after the gate passes
may `start` persist `manifest.md` and `strategy.md`.

## Phase 4: Draft strategy and cases

Ask `qa-lead` to classify every ledger row as Logic, Integration, Visual/Feel,
UI, or Config/Data; assign automation, manual, playtest, and soak requirements;
and identify risk and environment coverage. Ask `qa-tester` to draft cases with
stable IDs. Validate proposals against the plan before publication.

A case is an instruction artifact, not proof of execution. Each case must include:

- case ID, story ID, AC ID, test/check ID, candidate/build identity, platform
  constraints, preconditions, ordered steps, expected results, and evidence needs;
- owner role and timeout/escalation guidance;
- `Execution Status: NOT_RUN` and `Evidence Eligible: NO` at creation.

Case approval or a chat response never changes `NOT_RUN`. Persist only the
authorized manifest, strategy, and case set under this run's exclusive paths.

## Phase 5: Ingest automated evidence

This skill does not execute tests and does not infer a result from a test file,
test plan, qa-lead statement, terminal transcript pasted without provenance, or
process exit text alone.

Accept an exact structured receipt bound to this run's candidate. For regression
coverage, require the exact current `tests/regression-suite.md` selection-manifest
hash from the staged `regression-suite` contract and a matching build-bound runner
receipt. For every required automated ID verify:

- receipt artifact type/schema and evidence ID;
- candidate ID, build ID/hash, artifact hash, source commit, platform,
  configuration, environment, and QA-plan hash;
- stable test/check and AC IDs plus selection-manifest path/hash;
- exact command/argv, working directory, runner and version, start/end timestamps,
  exit code, per-test results and counts;
- log/result paths and SHA-256 hashes;
- producer/tool identity and attestation.

Normalize each required row to `PASS`, `FAIL`, `NOT_RUN`, `STALE`, `INVALID`, or
`UNKNOWN`. Only a structurally valid, current, matching receipt can supply
`PASS` or `FAIL`. A zero exit code without the required receipt is `INVALID`.
Missing results are `NOT_RUN`; old-build results are `STALE`. None of these may
be relabeled PASS.

The smoke receipt proves only its declared smoke rows. It cannot satisfy unrelated
automated rows in the QA plan.

## Phase 6: Ingest manual evidence

A canonical manual evidence record requires all of:

- artifact type `team-qa-manual-evidence`, schema version 1, evidence ID, and case
  ID;
- stable story, AC, test/check, and step IDs;
- run ID, candidate ID, build ID/hash, artifact hash, source commit, platform,
  configuration, environment, device/OS/input details;
- tester identity or approved pseudonymous ID, tester role, start/end timestamps,
  and attestation;
- executed preconditions and an actual observed result for every step;
- overall result `PASS`, `FAIL`, `BLOCKED`, or `NOT_RUN` with rationale;
- at least one attachment or log path with its SHA-256, as required by the case.

`qa-tester` may transcribe a supplied receipt but must preserve the source bytes
and provenance. The orchestrator re-hashes attachments before ingest. A user's
"Pass" selection, a conversational description, an agent observation, missing
per-step actuals, missing tester/time/device data, or unverified attachments is
`INVALID` or `UNKNOWN`, never PASS.

If an otherwise valid current manual record reports `FAIL`, `BLOCKED`, or
`NOT_RUN`, preserve that exact status in the ledger.

## Phase 7: Consume playtest and soak evidence

When the plan requires playtest evidence, accept only the exact canonical staged
`playtest-report` result:

`production/playtests/<session-id>/report.md`

Require artifact type `playtest-session-result`, schema version 1,
`Status: COMPLETED`, `Gate Eligible: YES`, matching build version/hash, source
commit, platform/configuration, hypothesis/AC IDs, timestamps, participant count,
evidence receipt ID, raw-evidence hash, manifest hash, and observation-ledger
hash. Re-hash all referenced artifacts. `COMPLETE` text alone is not PASS.

When the plan requires soak evidence, accept only:

`production/qa/soak-tests/<soak-run-id>/result.md`

Require artifact type `soak-test-result`, schema version 1, `Status: COMPLETED`,
matching build/profile/source/platform and verified receipt/raw/ledger hashes.
Inspect `Execution Status`, `Readiness Result`, `Gate Eligible`, and every required
Stability, Memory, Performance, and Experience dimension. A plan row passes only
when the named gate policy and required dimensions pass. `Verdict: COMPLETE`
describes artifact finalization and never substitutes for readiness.

Missing, in-progress, wrong-build, stale, inconclusive, or gate-ineligible
playtest/soak evidence leaves the corresponding required row nonconclusive.

## Phase 8: Findings and collision-free bug handoff

For each valid current failure, create a finding in the evidence index with a
collision-resistant occurrence ID:

`TQA-OCC-<qa-run-id>-<case-or-test-id>-<short-evidence-hash>`

Normalize a fingerprint from scope, stable AC/test/check ID, platform, and failure
signature. Link an existing canonical bug only when its stored fingerprint and
occurrence mapping match.

This skill never scans for the next `BUG-NNN`, never reserves or increments bug
numbers, and never writes `production/qa/bugs/**`. Parallel qa-testers may propose
finding text only. Hand unmatched occurrences, fingerprints, evidence paths, and
hashes to one serialized `bug-report` owner. Until every required failure has a
verified canonical bug receipt or an approved non-bug disposition, the QA verdict
is `NOT_APPROVED` and Gate Eligible is `NO`. This single-owner handoff removes
parallel bug-ID allocation races.

## Phase 9: Freeze and review evidence

Before finalize, build an ordered `evidence-index.md` containing:

- run/candidate/build/scope/QA-plan identity and hashes;
- every ledger row and its normalized status;
- exact receipt/report/attachment paths and hashes;
- required, excluded, conclusive, pass, fail, blocked, not-run, stale, invalid,
  and unknown counts;
- exclusions and approval-receipt hashes;
- findings, occurrence IDs, bug/disposition receipts, and unresolved gaps;
- freeze timestamp, hash algorithm, and ordered-artifact count.

Finalize consumes only this frozen index. Re-hash every referenced artifact.
Changed evidence makes the frozen index `STALE`; reject signoff and start a new
QA run rather than editing history.

Read only the exact `--evidence-review` path under
`production/qa/evidence/reviews/<review-id>/report.md`. Require the staged
`test-evidence-review` contract and an exact manifest/index/candidate/build match:

- `Artifact Type: test-evidence-review-report` and schema version 1;
- `Workflow Status: COMPLETE`;
- `Overall Evidence Quality: ADEQUATE`;
- `Overall Execution Status: PASS`;
- `Execution Scope: FULL` and sufficient for every required plan row;
- `Closure Eligible: YES`;
- exact QA plan, candidate, evidence-index, and report hashes.

Any other combination is not closure evidence. In particular, `Workflow Status:
COMPLETE` alone never means PASS.

## Phase 10: Deterministic signoff

Apply this precedence to the frozen required denominator:

| Precedence | Condition | QA Verdict | Gate Eligible |
|---|---|---|---|
| 1 | Any valid current required FAIL, failed required readiness dimension, or unresolved severity-1/2 failure | NOT_APPROVED | NO |
| 2 | Otherwise any required BLOCKED, NOT_RUN, UNKNOWN, STALE, INVALID, missing artifact, PARTIAL/BLOCKED review, or non-FULL/non-eligible review | INCOMPLETE | NO |
| 3 | All required rows pass and only explicitly approved nonblocking conditions remain | APPROVED_WITH_CONDITIONS | NO |
| 4 | All required rows pass, every finding is dispositioned, review is closure-eligible, and no condition remains | APPROVED | YES after verified persistence |

When failure and incomplete evidence coexist, `NOT_APPROVED` takes precedence and
the signoff must also list every incomplete row. No required row disappears from
the denominator. Show total declared, approved exclusions, required denominator,
and all status counts so the arithmetic is auditable.

`qa-lead` may draft the assessment but cannot override this table. The final
`signoff.md` header contains:

```text
Artifact Type: team-qa-signoff
Schema Version: 1
QA Run ID: <qa-run-id>
Scope ID: <scope-id>
Candidate ID: <candidate-id>
Build ID: <build-id>
Build Hash: <sha256>
Source Commit: <commit>
Platform/Configuration/Environment: <values>
QA Plan Path/SHA-256: <path> / <sha256>
Smoke Report Path/SHA-256: <path> / <sha256>
Evidence Index Path/SHA-256: <path> / <sha256>
Evidence Review Path/SHA-256: <path> / <sha256>
Workflow Status: COMPLETE | PARTIAL
QA Verdict: APPROVED | APPROVED_WITH_CONDITIONS | NOT_APPROVED | INCOMPLETE
Gate Eligible: YES | NO
Persistence: VERIFIED
```

Then include denominator arithmetic, per-row result table, failure/incomplete
sections, findings and bug handoffs, conditions, and exact next actions.

Revalidate all hashes immediately before writing. Publish `signoff.md` atomically,
re-read it, and verify its bytes. If persistence is declined or fails, return the
calculated QA verdict but `Gate Eligible: NO` and the appropriate Persistence;
never claim that signoff exists.

## Final response

Every mode ends with the exact run ID, canonical paths inspected or created,
verified hashes, Workflow Status, QA Verdict, Gate Eligible, Persistence, gaps,
and next action. Use `BLOCKED_AT_ENTRY / INCOMPLETE` for a failed entry gate;
`RUNNING / INCOMPLETE` while required evidence remains; and the deterministic
Phase 10 result only after finalize.

Do not recommend a downstream phase gate unless `Gate Eligible: YES`. For all
other outcomes, name the precise missing, stale, blocked, failed, or undispositioned
IDs and the command or artifact needed to resume this same run.
