# Team Audio — Execution and Recovery Protocol

This reference is normative for `$team-audio`. It defines bounded attempts, the
single checkpoint state machine, compare-and-swap gates, partial evidence, resume,
and completion recording. It grants no content-write authority.

## 1. Fixed phase state machine

The checkpoint phase is exactly one of:

1. `REQUEST_VALIDATED`;
2. `CONTEXT_FROZEN`;
3. `DIRECTION_DECIDED`;
4. `PLAYER_AUDIO_PROPOSALS_READY`;
5. `TECHNICAL_ROUTING_READY`;
6. `DRAFT_READY`;
7. `WRITE_AUTHORIZED`;
8. `SPEC_WRITTEN`;
9. `SPEC_REVIEWED`;
10. `QA_PLANNED`;
11. `ACCEPTED`; or
12. `TERMINAL`.

Allowed phase transitions follow that order. A phase may transition to PARTIAL,
DEFERRED, or BLOCKED without advancing. Resume may repeat a read-only validation,
but cannot skip a prerequisite, move backward, or replay a completed side effect.

There is no review mode. A checkpoint/request containing `review_mode`, `full`,
`lean`, `solo`, a director-gate outcome, or a session-mode source is invalid.

## 2. Single persistent checkpoint

Use exactly:

    production/session-state/team-audio/<artifact-id>/<run-id>.yaml

The file uses `cgs.team-audio-checkpoint/v2`:

```yaml
schema: cgs.team-audio-checkpoint/v2
artifact_id: <id>
run_id: <id>
operation: create | revise
spec_path: design/audio/audio-<artifact-id>.md
record_authorization_id: <id>
record_authorization_sha256: <sha256>
current_sequence: <nonnegative integer>
current_phase: <phase>
current_status: ACTIVE | PARTIAL | DEFERRED | BLOCKED | COMPLETE
history:
  - sequence: <integer>
    phase: <phase>
    status: ACTIVE | PARTIAL | DEFERRED | BLOCKED | COMPLETE
    previous_transition_sha256: <sha256 or ROOT>
    expected_checkpoint_preimage_sha256: <sha256 or ABSENT>
    request_sha256: <sha256>
    context_manifest_sha256: <sha256 or null>
    direction_decision_sha256: <sha256 or null>
    destination_ledger_sha256: <sha256 or null>
    draft_sha256: <sha256 or null>
    write_plan_sha256: <sha256 or null>
    content_approval_sha256: <sha256 or null>
    mutation_authorization_sha256: <sha256 or null>
    observed_spec_sha256: <sha256 or ABSENT | UNKNOWN>
    accessibility_finding_ids: []
    audio_review_sha256: <sha256 or null>
    qa_plan_proposal_sha256: <sha256 or null>
    engine_state: CURRENT | DEFERRED | STALE | NOT_APPLICABLE
    product_acceptance_sha256: <sha256 or null>
    attempts: []
    revoked_tokens: []
    loaded_sources: []
    omitted_sources: []
    open_blocker_ids: []
    actual_write_set: []
    late_or_unauthorized_writes: []
    next_safe_phase: <phase or NONE>
    recorder_identity: <identity>
    recorded_at: <RFC3339 timestamp>
    transition_sha256: <sha256>
```

Each transition hash is computed from canonical fields excluding itself. History is
append-only inside the atomically replaced checkpoint bytes. Validate sequence,
predecessor transition hash, prior checkpoint raw hash, and immutable artifact/run/
operation/spec identity on every update. Maximum checkpoint bytes are 131072; if
history would exceed it, stop PARTIAL and require a new run rather than truncate or
discard history.

Checkpoint record authorization binds this exact path/schema/max size, allowed
phase/status fields, transition validation, one recorder identity, and non-writes.
It does not authorize spec bytes. If no exact record authorization exists, preserve
the candidate payload in conversation and perform no project mutation.

Update the checkpoint after request validation, context freeze, direction decision,
player-facing proposals, technical routing, draft creation, spec authorization,
spec write, review, QA planning, acceptance, and every PARTIAL/DEFERRED/BLOCKED stop.

## 3. Attempt control

Each `cgs.team-audio-agent-attempt/v2` contains logical task ID, role, agent identity,
input/context/predecessor hashes, allowed proposal/finding IDs, prohibited paths,
attempt token, retry ordinal `0 | 1`, start time, deadline, result status, output
hash, omissions, and observed side effects.

Hard caps:

- three simultaneously live agents;
- 10 minutes per attempt;
- 20 minutes per multi-agent phase;
- nine total delegate attempts per run;
- one retry per logical task; and
- zero nested delegation.

At timeout/cancel/failure/invalid output/side effect:

1. mark status `TIMED_OUT | CANCELED | FAILED | INVALID | SIDE_EFFECT`;
2. revoke the token and checkpoint it;
3. cancel dependent attempts;
4. rehash spec/checkpoint and every prohibited path whose preimage was inventoried;
5. quarantine later payloads/patches by hash and never merge them; and
6. return PARTIAL/BLOCKED when required evidence is unavailable.

A retry is allowed only after all inventoried paths prove the prior attempt made no
write. The retry receives a new token, no larger input, and the original absolute
deadline ceiling; it does not reset the 20-minute phase or nine-attempt run cap.
There is no second retry, substitute role, or loop-until-pass.

Any result after revocation/deadline is `LATE`. A late write is not automatically
reverted. Preserve path/pre/post hashes, stop further ordinary writes, and require
the named owner to resolve it. LATE or SIDE_EFFECT evidence prevents SPEC COMPLETE.

## 4. Checkpoint update CAS

Before each checkpoint update:

- require current checkpoint preimage hash/ABSENT and valid internal history;
- rehash every source, predecessor proposal/result, spec target, decision,
  authorization, reviewer/QA evidence named by the transition;
- require active recorder identity and record-authorization hash;
- require no revoked/late token output entered accepted state; and
- require the candidate transition to be the unique legal next sequence/phase.

On mismatch, write nothing and return BLOCKED with exact field/path/expected/
observed hashes. Checkpoint status does not overwrite source truth or authorize a
spec write.

## 5. Spec write CAS and transaction

Immediately before the spec write, perform one complete preflight:

### Source and context CAS

- request, all loaded source bytes, inventory/omission set, context limits/hash,
  direction decision, proposals/findings, destination ledger, engine evidence, and
  attempt/token states.

### Target and identity CAS

- canonical spec path, artifact/run/operation, spec preimage/ABSENT, checkpoint
  preimage/history, one transaction writer, and zero alias/second-target conflict.

### Approval and authorization CAS

- complete draft bytes/hash, write-plan hash, content approval identity/hash,
  mutation authorization identity/hash, exact two-path write set, and non-writes.

Any mismatch means zero spec writes and invalidates stale approval/authorization.

Write the spec first with atomic single-file replacement where supported, then read
back/verify exact bytes/raw hash. Update the checkpoint second. Single-file atomic
operations do not make the pair atomic.

If spec succeeds and checkpoint fails, return `PARTIAL — NOT APPROVED`, report an
uncheckpointed spec with exact expected/observed hashes, and do not claim safe
resume. Do not delete or overwrite the spec as rollback. If spec write/read-back
fails, preserve exact observed state and update PARTIAL checkpoint only when the
record CAS still safely applies.

Rollback may be claimed only if a separately authorized recovery restored every
affected path byte-for-byte and raw hashes equal recorded preimages. This workflow
does not assume or automatically perform destructive rollback.

## 6. Idempotent resume

`--resume` must name the canonical checkpoint path and expected raw hash. Read and
validate the entire internal history, request/content/run/operation identity,
record authorization, transition chain, current source/context hashes, spec
preimage/current hash, decisions, proposal/review/QA hashes, engine state, product
acceptance, attempt tokens, and prohibited-path observations.

Resume only from `next_safe_phase`. Completed phase evidence with matching inputs/
outputs is a no-op. Never repeat a successful spec write, product decision,
delegation, review, or QA proposal from prose alone. Pending/retry work receives a
new permitted token; revoked tokens stay revoked.

Any source, spec, checkpoint, engine, decision, ownership, authorization, or
attempt-state drift returns BLOCKED/PARTIAL with exact expected/observed hashes.
Never silently restart under the old run ID or advance a stale spec review/
acceptance.

## 7. Review/revision convergence

Accessibility and final audio review each permit one author revision and one
verification re-review. A revision must render exact new bytes and obtain a new
write plan, content approval, mutation authorization, CAS, spec write/read-back, and
checkpoint transition. The re-review uses a fresh token/identity and binds the new
spec hash while preserving stable finding IDs.

No second revision or third observation is permitted for the same blocker. The same
blocker, partial review, reviewer/author/writer identity overlap, timeout, or stale
hash ends BLOCKED/PARTIAL.

## 8. Minimum PARTIAL and terminal evidence

Even when no spec can be safely written, a PARTIAL response/checkpoint candidate
must contain:

- artifact/run/operation and canonical paths;
- current request/context/source/spec/checkpoint hashes or UNKNOWN;
- completed proposal/finding IDs and their destination/owner;
- missing/blocked/timed-out/canceled/late attempt states;
- accessibility/review blockers and engine state;
- actual/attempted write set with observed hashes;
- last verified phase and exact safe resume action; and
- explicit `NOT APPROVED`, `QA NOT RUN`, `PLAYBACK NOT RUN`, and
  `NOT IMPLEMENTATION READY` labels.

`cgs.team-audio-final-evidence/v2` records the terminal packet:

```yaml
schema: cgs.team-audio-final-evidence/v2
artifact_id: <id>
run_id: <id>
verdict: SPEC_COMPLETE | SPEC_COMPLETE_ENGINE_VALIDATION_DEFERRED | PARTIAL_NOT_APPROVED | ACCEPTED_RISK_NOT_APPROVED | DEFERRED_NOT_APPROVED | BLOCKED
spec_path: design/audio/audio-<artifact-id>.md
spec_sha256: <sha256 or ABSENT | UNKNOWN>
context_manifest_sha256: <sha256>
direction_decision_sha256: <sha256 or null>
destination_ledger_sha256: <sha256 or null>
write_plan_sha256: <sha256 or null>
mutation_authorization_sha256: <sha256 or null>
checkpoint_sha256: <sha256 or null>
proposal_counts_by_destination: {}
attempt_states: []
accessibility_finding_ids: []
audio_review_sha256: <sha256 or null>
qa_plan_proposal_sha256: <sha256 or null>
engine_state: CURRENT | DEFERRED | STALE | NOT_APPLICABLE
adr_dependencies: []
product_acceptance_sha256: <sha256 or null>
qa_execution: NOT_RUN
playback_execution: NOT_RUN
implementation_state: NOT_PRESENT
open_blocker_ids: []
next_action: <exactly one action>
recorded_at: <RFC3339 timestamp>
```

The final evidence is embedded in the verified checkpoint transition or returned in
conversation when checkpoint persistence fails. It is not a third writable path and
cannot upgrade missing evidence by assertion.
