# Team UI execution and recovery protocol

This file is normative for `$team-ui`. Its purpose is to make bounded delegation, persistence, cancellation, recovery, and final review deterministic.

## Phase state machine

The only forward states are:

~~~text
REQUEST_VALIDATED
  -> UX_CANDIDATE_WRITTEN
  -> UX_REVIEWED
  -> UX_APPROVED
  -> SUPPORT_CANDIDATES_READY
  -> SUPPORT_ARTIFACTS_WRITTEN
  -> IMPLEMENTATION_MANIFEST_AUTHORIZED
  -> IMPLEMENTATION_WRITTEN
  -> BUILD_EVIDENCE_CAPTURED
  -> FINAL_REVIEWED
  -> IMPLEMENTATION_VERIFIED
~~~

At any transition, `PARTIAL`, `BLOCKED`, `NEEDS_REVISION`, `SPEC_APPROVED`, or `ACCEPTED_RISK_SPEC_NOT_APPROVED` may terminate the run according to the result contract. A resume continues only from the earliest safe state whose inputs remain current. State names are never inferred from file existence.

UX review round 0 follows initial authoring. Author revisions are capped at rounds 1 and 2. Implementation review round 0 follows the initial build. Fix/rebuild rounds are capped at 1 and 2. Round counters never reset on resume or retry.

## Scheduler and attempt budgets

At most three live role tasks may exist at once, including optional consultations. A role task may not spawn a child. Authoring, planning, writing, and fixing are sequential whenever their write sets could overlap. The four mandatory final reviewers run in deterministic order in waves of at most three; the checkpoint records the chosen order before dispatch.

Every task has a default attempt deadline of 600 seconds and a hard cap of 900 seconds. Every active phase has a default and hard cap of 1800 seconds. The request may lower these values but cannot raise them. Authorization/user-decision pauses are not live phases: persist state, cancel live tokens, emit one next action, and stop instead of waiting indefinitely.

A task has at most two attempts: the initial attempt and one eligible retry. The retry uses the same target hashes, role, check IDs, and output schema with a narrower or equal context. It receives a new attempt token and cannot expand scope.

Automatic retry eligibility is limited to:

- a read-only author-in-scratch, planner-in-scratch, consultation, or reviewer whose first attempt made no project mutation;
- an evidence runner only after its entire declared output set is enumerated, its terminal mutation state is known, partial outputs are sealed as ineligible, and the retry uses new exact output paths already authorized;
- a project writer only when the mutation reconciliation proves every declared project target and temporary path remains at its pre-attempt hash/absence. Otherwise the result is `PARTIAL` or `BLOCKED` pending reconciliation and explicit user action.

No task may receive a third attempt. A phase deadline prevents further dispatch even if an individual retry remains.

## Attempt lifecycle, cancellation, and late output

The coordinator assigns every attempt a unique unguessable `attempt_token` and records:

- packet hash, role, task ID, attempt number, target hashes, allowed reads/writes, and context hash;
- dispatch, start, heartbeat if available, deadline, cancel-request, terminal, and receipt times;
- terminal state `SUCCEEDED|FAILED|TIMED_OUT|CANCELLED|UNKNOWN`;
- mutation reconciliation status and returned output hash.

On deadline, coordinator interruption, malformed streaming termination, or phase cancellation:

1. revoke the attempt token and issue cancellation where supported;
2. mark its output eligibility `REVOKED` before dispatching a retry;
3. reconcile all declared targets, temporary paths, raw evidence outputs, and the broader authorized mutation set;
4. checkpoint the observed state;
5. retry only if the eligibility rules above hold.

Any response received after token revocation is `LATE_QUARANTINED`. Record its hash and arrival time but do not parse it into findings, copy it to a canonical artifact, count it for quorum, or use it to decide mutation state. A late successful-looking response never supersedes a newer attempt.

An unavailable cancellation API does not make a task safe. Mark its execution state `UNKNOWN`, reconcile mutations, and stop `PARTIAL` unless the task is read-only and isolation proves it cannot write.

## Mutation transaction and reconciliation

Before a write task starts, capture exact hashes/absence for every authorized path and enumerate the full working mutation set. The active manifest assigns one owner to every path, includes atomic temporary siblings, and declares maximum bytes. Re-hash manifest inputs immediately before dispatch.

After a task terminates for any reason:

1. enumerate all changed paths in the authorized roots using a stable method recorded in the checkpoint;
2. compare normalized paths, operation types, preimages, postimages, byte caps, and writer identity with the active manifest;
3. classify each path `UNCHANGED|EXPECTED_CHANGED|UNEXPECTED_CHANGED|MISSING|UNKNOWN`;
4. reject a claimed success until every expected output reads back with its reported hash;
5. treat `UNEXPECTED_CHANGED` as `BLOCKED: MUTATION_BREACH` and `UNKNOWN` as `PARTIAL: MUTATION_STATE_UNKNOWN`.

Do not silently revert or overwrite unexpected changes. Report the exact path and observed hash without exposing sensitive contents. A later task cannot legalize an earlier out-of-manifest mutation.

The coordinator-recorder does not share project-output paths with role writers. It may write only currently authorized record paths and their declared temporary siblings.

## Immutable checkpoints

After every phase transition, authorization decision, task terminal state, timeout/cancellation, mutation reconciliation, finding transition, build identity change, and persistence failure, create a new checkpoint:

~~~text
production/ui/team-ui/<screen-id>/<run-id>/checkpoints/<sequence>-<phase>.yaml
~~~

`<sequence>` is a zero-padded monotonically increasing integer starting at `0000`. A final checkpoint is never overwritten. Create exact candidate bytes, verify the maximum record size, write to the authorized `.tmp-<attempt-token>` sibling, read back and hash, atomically replace the absent final path, read back the final path, verify the same hash, then confirm the temporary sibling is absent. If atomic replacement is unavailable, write the absent final path once and read back; record `atomicity: UNAVAILABLE`, and do not proceed until the user accepts the weaker persistence property or supplies a supported recorder.

Each checkpoint conforms to `cgs.team-ui-checkpoint/v2` and contains:

- schema, screen/run IDs, sequence, state, pipeline result if terminal, and creation timestamp;
- request path/hash, skill and both normative-reference hashes, instruction-chain paths/hashes;
- previous checkpoint path/hash, current checkpoint candidate hash, and recorder identity;
- context manifest hash and exact accepted/rejected counts/bytes;
- consultation mode and mode decision source;
- current UX/support/ADR/pattern/implementation/build/source-set/evidence paths and hashes;
- active authorization state plus exact mutation-manifest path/hash;
- per-role task IDs, attempt tokens/status/deadlines, cancellation/retry/quarantine records;
- mutation ledger and reconciliation result;
- stable UXF/UIF finding state transitions and round counters;
- evidence coverage summary listing required/pass/fail/unknown/not-run/stale row IDs;
- persistence method, temporary/final read-back hashes, and next legal transition/action.

Checkpoints store hashes and bounded summaries, not entire context, logs, reviewer payloads, or evidence matrices. A checkpoint is capped at 524288 bytes. If the record cannot fit, persist separately authorized bounded immutable envelopes and include their hashes; never truncate identity, mutations, findings, or required coverage.

If checkpoint persistence or read-back verification fails, revoke live tasks, return `PARTIAL: CHECKPOINT_PERSISTENCE_FAILED`, and do not advance.

## Resume validation and invalidation

`--resume` takes one exact checkpoint path. Validate invocation before project reads, then read and validate the named v2 request and require its `resume_checkpoint.path` to equal the flag and its `resume_checkpoint.sha256` to match the checkpoint bytes. Validate that the path matches the request’s screen/run canonical checkpoint family. A checkpoint is eligible only when its schema is v2, its prior link chain is intact, and it was not terminally superseded by a later checkpoint named in the same chain.

Re-read and re-hash:

- request, skill contract, normative references, and ordered instruction chain;
- every context input used by completed states;
- UX spec and approval envelope;
- visual, asset, engine-plan, art-bible target/authoring-receipt/independent `cgs.art-bible-review/v1` APPROVE evidence, Accepted ADR, and pattern inputs;
- implementation manifest and every implementation source path;
- engine/version, adapter, build artifact/receipt, raw logs, evidence matrix, and review envelopes;
- every authorized target involved in a nonterminal or uncertain attempt.

Apply these invalidation rules:

| Changed or uncertain identity | Earliest safe state |
|---|---|
| request, screen/run, contract, or instruction chain | `REQUEST_VALIDATED` after revalidation; prior authorization cannot be reused |
| UX/context requirement input | `UX_CANDIDATE_WRITTEN` or earlier; approval and all descendants stale |
| UX spec or UX envelope | `UX_REVIEWED` or earlier; support/implementation/build/final review stale |
| visual/asset/engine/art-bible target, authoring receipt, independent review/ADR/pattern input | `SUPPORT_CANDIDATES_READY` or earlier; implementation and descendants stale |
| implementation manifest/base/source | `IMPLEMENTATION_MANIFEST_AUTHORIZED` or earlier; build/evidence/reviews stale |
| engine/version/adapter/build/raw evidence | `IMPLEMENTATION_WRITTEN` or earlier; evidence/reviews stale |
| one final review envelope only | `BUILD_EVIDENCE_CAPTURED`; rerun that stream unless target changed |
| unknown writer/runner mutation state | no automatic resume; reconcile or stop `PARTIAL` |

Stale artifacts remain preserved as history but are marked ineligible by path/hash. Never rewrite an old checkpoint, envelope, raw receipt, or result to make it current. Resume preserves revision/fix/attempt counters and stable finding IDs.

If a referenced file is missing, hash-mismatched, outside the project, or exceeds current limits, fail closed. The single next action names the earliest invalidated prerequisite.

## UX review persistence

The independent UX reviewer returns a bounded `cgs.review-evidence/v1` envelope with an exact `cgs.ux-review/v2` extension in conversation. It retains `gate_evidence_status: NOT_PERSISTED` and `gate_evidence_eligible: false`. The coordinator verifies task identity, packet hash, current UX-review bundle and author-contract manifest, target hash, generic record ID, extension completeness, assertion/requirement coverage, finding IDs/fingerprints, mutation guard, and response size; re-hashes the unchanged target; then wraps the exact response bytes without alteration in the canonical `cgs.team-ui-ux-review-recording/v1` envelope. The wrapper records the embedded hash and its own write/read-back hash and does not mutate the embedded gate fields.

If the target changed between review and persistence, the response is stale and cannot be persisted as eligible approval evidence. If envelope persistence fails, the spec is not formally approved.

## Runtime evidence execution

The evidence runner is neither UI programmer nor reviewer. Its packet fixes the implementation-manifest, source-set, engine/version, platform/config, adapter, build target, coverage-profile, raw-output paths, and time budgets. The runner may execute only those declared adapters and may write only exact raw outputs.

The runner must record real execution receipts. A simulated command, invented log, `NOT_RUN` placeholder, existence-only observation, review narrative, or old receipt cannot satisfy a row. Raw receipts are sealed by hash before reviewer dispatch. If a rerun changes any source/build/config identity, allocate the next evidence round, stale old rows, and run required coverage again.

Runner timeout follows cancellation and reconciliation rules. A retry never overwrites first-attempt output; it uses exact pre-authorized attempt-specific paths. Unknown external engine state or unbounded background process yields `PARTIAL` and blocks review quorum.

## Mandatory final reviews and evidence quorum

Freeze one review-set manifest before dispatch. It names the exact final build/source-set, evidence-matrix hash, four stream packet hashes, reviewer identities, required check IDs, deterministic wave order, and deadlines. Identities must prove:

- UX reviewer is not UX author, UI programmer, evidence runner, or another mandatory reviewer;
- art reviewer is not art author, UI programmer, evidence runner, or another mandatory reviewer;
- accessibility reviewer and engine/QA reviewer are each distinct from all authors, writer, runner, and each other.

Every stream must return `COMPLETE` on the frozen identities and cover all assigned checks. Concurrency is at most three, so use a second wave for at least one stream. A timed-out, cancelled, failed, malformed, missing, wrong-target, or late-quarantined stream makes the review set `PARTIAL`; advisory consultations cannot fill it.

The coordinator persists the exact reviewer responses in immutable envelopes only after verifying their target identities. Quorum requires all four eligible envelopes, complete global required-check coverage, a complete runtime matrix, and zero open blocking findings.

## Fix rounds and final-hash rule

Only the original UI-programmer identity may fix implementation files. A fix authorization maps exact open blocking UIF IDs to existing manifest operations and expected bases. New paths, owners, or operations require a new implementation manifest and authorization.

After a fix:

1. reconcile mutations and hash the new source set;
2. rerun the build/evidence runner to obtain a new build and evidence round;
3. mark every prior runtime row and final review envelope stale;
4. create a new review-set manifest for the new hashes;
5. run all previously open checks and the complete regression matrix, not only changed areas.

Stop after fix round 2. If the same blocker remains, evidence is incomplete, a required task is unavailable, or a writer breached ownership, use `BLOCKED` or `PARTIAL` according to whether the terminal state is known. User risk acceptance cannot close a mandatory UI, accessibility, engine, or evidence blocker.

## Final result

The coordinator writes the canonical `result.md` only after stopping all role tasks and reconciling mutations. It records exact status/verdict mapping, current and stale artifact hashes, authorization states, task/attempt histories, cancellations/quarantine, checkpoint chain, mutations, UXF/UIF transitions, build/source-set and evidence identities, per-stream outcome, missing coverage, and persistence/read-back hash.

`COMPLETE` requires every predicate from the request-and-record contract on one current final hash. Otherwise identify the first unsatisfied predicate and emit exactly one legal next action. Do not continue automatically after writing the result.
