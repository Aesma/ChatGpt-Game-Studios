# Team Narrative — Execution and Evidence Protocol

This reference is normative for `$team-narrative`. It defines review modes,
attempt control, checkpoints, authorization/CAS, partial evidence, and result
receipts. It grants no authority by itself.

## 1. Exact role and mode matrix

Render `cgs.narrative-role-matrix/v2` before any delegation. “Required” means its
evidence must exist for the requested artifact set and terminal status. Conditional
roles are required only when their artifact/constraint type is requested.

| Phase | Role | Full | Lean | Solo | Write scope |
|---|---|---|---|---|---|
| Canon validation | world-builder | required read-only delegate | required read-only delegate | coordinator-only, not independent | none |
| Product canon decision | named canon authority | required when decision exists | same | same | decision only |
| Canon promotion | unique canon writer + registry recorder | conditional | conditional | prohibited | exact authorized canon paths |
| Narrative brief | narrative-director author | required read-only delegate | coordinator proposal, disclosed degradation | coordinator proposal, disclosed degradation | none |
| Dialogue/lore/voice proposal | writer | conditional read-only delegate | coordinator proposal; permitted only for requested text types | coordinator draft only | none |
| Visual narrative proposal | art-director | conditional read-only delegate | skipped; requested visual artifacts remain PARTIAL | skipped | none |
| Level/trigger proposal | level-designer | conditional read-only delegate | skipped; requested level artifacts remain PARTIAL | skipped | none |
| Localization review | localization-lead | required for localizable content | required for localizable content | skipped; localizable content is NOT_LOCALIZATION_READY | none |
| Content writes | unique artifact writers + shared recorder | conditional after authorization | conditional after authorization | prohibited | disjoint authorized paths |
| Final narrative review | fresh independent narrative reviewer | required | required | skipped; NOT_INDEPENDENTLY_REVIEWED | none |
| Evidence | coordinator recorder | exact authorized records | same | exact operational records only | operational root |

The independent narrative reviewer may use a fresh narrative-director review
context, but its identity/attempt token must differ from every narrative-director
authoring context and every author/editor/writer/recorder/approver identity.

Full mode may reach COMPLETE when every requested conditional role and all gates
succeed. Lean may reach COMPLETE only when no requested artifact requires an
omitted art/level specialist and all mandatory validator/localization/reviewer
evidence succeeds. Solo is planning-only: it invokes zero agents, performs no canon
or narrative-content writes, and can return only PARTIAL/BLOCKED with the explicit
quality omissions.

Skipped is not passed. Every omitted role records role, reason, affected artifact
IDs, quality impact, and next action. Never read an unrelated session review-mode
file or silently change modes during a run.

## 2. Attempt, timeout, cancellation, and late-output rules

For each delegate create `cgs.narrative-attempt/v2` with role, identity, task,
input hashes, allowed artifact/proposal IDs, prohibited paths, token, start time,
deadline, retry ordinal, and parent phase.

Hard limits:

- maximum active proposal agents: 3;
- maximum per-attempt deadline: 15 minutes;
- maximum proposal phase deadline: 30 minutes;
- maximum total delegated attempts per run: 10;
- at most one retry for one logical task; and
- no nested delegation.

The request may lower these limits. Awaiting work must still surface concise user
updates at least once per 60 seconds; an update does not extend a deadline.

On timeout, cancellation, invalid payload, or detected side effect:

1. mark the attempt `TIMED_OUT | CANCELED | INVALID | SIDE_EFFECT`;
2. revoke its token and record the revocation in the next immutable checkpoint;
3. cancel dependent attempts and prevent their results from entering any plan;
4. compare all prohibited/target preimages to detect a late or unauthorized write;
5. accept at most one retry only after proving the old attempt wrote nothing;
6. issue a new token and exact input snapshot for the retry; and
7. return PARTIAL if the required result remains unavailable.

A result arriving after deadline/cancellation/revocation is `LATE`. Preserve its
hash/path or payload digest in quarantine evidence, but never merge, authorize,
write, review, or count it as completion. A detected late write is not reverted;
stop BLOCKED/PARTIAL, preserve exact pre/post hashes, and require the artifact owner
to resolve it.

## 3. Immutable checkpoint chain

Use `cgs.team-narrative-checkpoint/v2`:

```yaml
schema: cgs.team-narrative-checkpoint/v2
checkpoint_id: <TNC id>
content_id: <stable id>
run_id: <stable id>
sequence: <positive integer>
phase: REQUEST_VALIDATED | CONTEXT_FROZEN | CANON_DECIDED | CANON_FROZEN | BRIEF_READY | PROPOSALS_READY | PLAN_APPROVED | LOCALIZATION_REVIEWED | AUTHORIZED | WRITES_VERIFIED | FINAL_REVIEWED | TERMINAL
status: COMPLETE | PARTIAL | BLOCKED
previous_checkpoint_sha256: <sha256 or ROOT>
request_sha256: <sha256>
context_manifest_sha256: <sha256 or null>
role_matrix_sha256: <sha256>
canon_decision_sha256: <sha256 or null>
canon_baseline_sha256: <sha256 or null>
artifact_plan_sha256: <sha256 or null>
ownership_manifest_sha256: <sha256 or null>
localization_review_sha256: <sha256 or null>
mutation_authorization_sha256: <sha256 or null>
final_artifact_set_sha256: <sha256 or null>
narrative_review_sha256: <sha256 or null>
active_attempt_tokens: []
revoked_attempt_tokens: []
completed_work: []
pending_work: []
finding_ids: []
observed_target_hashes: {}
next_safe_phase: <phase or NONE>
recorder_identity: <identity>
recorded_at: <RFC3339 timestamp>
```

Checkpoints are create-only and linearly chained. A duplicate sequence,
predecessor mismatch, fork, overwritten checkpoint, missing phase dependency, or
schema/hash mismatch is BLOCKED. A checkpoint records evidence state; it does not
approve canon, approve content, authorize writes, or close a finding.

Write a checkpoint after request validation, context freeze, canon decision,
canon freeze, brief, proposals, plan approval, localization review, authorization,
writes, final review, and every PARTIAL/BLOCKED stop when its exact record path is
authorized. If record authority is absent, keep the same structure in conversation
and return BLOCKED before any project mutation.

## 4. Idempotent resume

`--resume` must identify one exact checkpoint path/hash. Rebuild the checkpoint
inventory under the declared operational root within the request budget and require
one linear chain ending at that checkpoint.

Before resuming:

- require matching content ID, run ID, operation, request hash, mode, role matrix,
  identities, and record authorization;
- rehash every checkpoint-bound source, canon file/registry, proposal payload,
  artifact pre/postimage, operational record, and authorization;
- recompute the canon baseline and final artifact-set hash when present;
- revalidate all active/revoked tokens and scan target/prohibited paths for late
  writes; and
- require the recorded `next_safe_phase` to have every prerequisite complete.

If any evidence drifts, return BLOCKED with exact path/expected/observed hash.
Never silently restart, advance canon, reuse stale proposals, replay a write, or
reuse an old reviewer verdict.

Completed immutable work is a no-op on resume. Reissue only pending tasks with new
attempt tokens. If an artifact already equals the authorized candidate and its
write receipt verifies, do not rewrite it. Recovery from a partial multi-file write
must re-inventory the whole authorized target set and obtain fresh authorization
for remaining operations; it cannot assume rollback.

## 5. Approval and authorization records

Canon plan approval and canon mutation authorization are defined in the main
workflow and are separate from narrative content.

Content approval uses `cgs.narrative-content-plan-approval/v2` and binds:

- content/run IDs, operation, mode, request/context/role/canon/brief hashes;
- exact artifact and ownership manifests;
- every artifact ID/path/operation/preimage/candidate/owner/dependency;
- constraint/localization review and handoff-interface hashes;
- open/accepted findings with owner/rationale/review point;
- proposed checkpoint/result paths and expected preimages; and
- explicit non-writes.

Approval accepts content and routing only. It does not authorize mutation.

Mutation authorization uses `cgs.narrative-mutation-authorization/v2` and binds the
approval ID/hash, exact current candidate set, writer/recorder identities,
deterministic order, source/canon/target hashes, operational receipts, and non-
writes. A new path, candidate byte, owner, dependency, finding disposition, canon
hash, constraint, or record target invalidates both preview and authorization.

## 6. Pre-write CAS

Run every gate in one read-only pass immediately before the first content write:

### Source and canon CAS

- request, context sources/inventories, UX/string/localization interface, canon
  files/registry, product decision, promotion receipt, and canon-baseline digest;
- brief/proposal payload hashes and attempt-token validity; and
- budget counts, loaded/omitted sets, graph nodes/edges, cycles, and references.

### Target and ownership CAS

- every artifact and operational-record preimage or ABSENT marker;
- unique artifact/path identity, create/revise/no-op/conflict classification;
- one writer per normalized path, disjoint writer sets, one shared recorder; and
- exact candidate bytes/hashes, size limits, dependencies, and write order.

### Review, approval, and role CAS

- localization findings/readiness and actual constraint-source hashes;
- plan approval and mutation authorization over the current bytes;
- active writer/recorder/authority identities and mode-required roles; and
- checkpoint chain head, next sequence, result path, and all active/revoked tokens.

Any mismatch means zero new content writes. Recompute the plan and obtain fresh
approval/authorization when any approved byte or scope changed.

## 7. Partial-write and read-back evidence

Single-file atomic replacement does not make a multi-file plan atomic. Write in
declared dependency order; verify each path immediately. Write shared projections
and operational receipts only after their prerequisites succeed.

On failure after one or more writes:

- stop ordinary writes and do not delete, overwrite, or roll back verified output;
- inventory every authorized target and record action `APPLIED | NO_OP |
  NOT_APPLIED | CONFLICT | UNKNOWN` with preimage/candidate/observed hashes;
- revoke active attempts and prevent late patches;
- write an authorized PARTIAL checkpoint/result receipt if safely possible; and
- require fresh inventory/authorization for recovery.

If evidence receipt creation fails, report the exact unreceipted changed set and
remain PARTIAL. Never infer that an accepted proposal or attempted write exists on
disk.

## 8. Review and fix-round convergence

Use at most two fix/re-review rounds after the initial independent narrative
review. Each round must:

1. name stable NRF/LOC finding IDs and exact authorized owner fixes;
2. render exact fix bytes into a new versioned artifact/ownership plan and obtain
   fresh plan approval and mutation authorization unless current authorization
   already binds those exact bytes;
3. recheck preimages/authorization and apply through the same unique writers;
4. read back and recompute the complete final artifact-set hash;
5. mark every prior review bound to another hash stale; and
6. run a fresh independent scoped review over changed artifacts and declared
   dependents.

No third fix round is allowed. Remaining blocker, incomplete coverage, identity
overlap, timeout, or non-convergence is PARTIAL/BLOCKED. Risk acceptance may route
a non-blocking concern but cannot change blocker severity, localization readiness,
or missing review evidence.

## 9. Result receipt and verdict

Use create-only `cgs.team-narrative-result/v2`:

```yaml
schema: cgs.team-narrative-result/v2
result_id: <stable id>
content_id: <id>
run_id: <id>
operation: create | revise
mode: full | lean | solo
verdict: COMPLETE | PARTIAL | BLOCKED
readiness: LOCALIZATION_READY | NOT_LOCALIZATION_READY | NOT_INDEPENDENTLY_REVIEWED | LOCALIZATION_HANDOFF_UNVERIFIED
request_sha256: <sha256>
checkpoint_sha256: <sha256>
canon_baseline_sha256: <sha256 or null>
artifact_plan_sha256: <sha256 or null>
final_artifact_set_sha256: <sha256 or null>
artifacts: []
ownership_manifest_sha256: <sha256 or null>
content_plan_approval_sha256: <sha256 or null>
mutation_authorization_sha256: <sha256 or null>
localization_review_sha256: <sha256 or null>
localization_handoff_path: <canonical path or null when not persisted>
localization_handoff_sha256: <sha256 or null>
localization_handoff_adapter: cgs.narrative-localization-handoff-v2-adapter/v1 | null
narrative_review_sha256: <sha256 or null>
attempt_summary: []
late_or_unauthorized_writes: []
open_finding_ids: []
blockers: []
next_action: <exactly one action>
recorder_identity: <identity>
recorded_at: <RFC3339 timestamp>
```

COMPLETE requires the full gate in the main workflow and a verified result receipt.
A result receipt cannot upgrade its own evidence. PARTIAL and BLOCKED preserve exact
safe progress and one next action. Do not create a timestamp-only receipt for an
exact no-op resume.
