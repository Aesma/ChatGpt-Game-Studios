# Create Epics — Continued Workflow

This reference is normative for `$create-epics`. It continues the read-only
planning contract in `../SKILL.md`; it does not grant permission to edit an
epic, the epic index, or any other project artifact.

## 1. Producer realism gate

Run the producer gate only after the candidate plan, candidate bytes, source
manifest, module map, dependency graph, traceability findings, and target
classification are complete.

### Full mode

- Make exactly one bounded, read-only producer review call named `PR-EPIC`.
- Give that call one attempt and at most 60 seconds.
- Do not let the producer delegate, mutate files, approve the plan, authorize
  writes, or record the result.
- Supply the producer with the exact source-manifest digest, plan digest,
  candidate hashes, dependency order, epic statuses, and stable finding IDs.
- Require `cgs.epic-producer-result/v1`:

```yaml
schema: cgs.epic-producer-result/v1
review_id: PR-EPIC
mode: full
status: complete | partial | timeout | failed | side-effect
disposition: REALISTIC | CONCERNS | UNREALISTIC | null
source_manifest_sha256: <sha256>
plan_sha256: <sha256>
candidate_hashes:
  <target_path>: <sha256>
finding_ids: [EPIC-FINDING-...]
omissions: []
reviewer_identity: <producer agent identity>
```

`partial`, `timeout`, `failed`, or `side-effect` is not a pass. It produces
`Workflow PARTIAL`, performs no writes, and preserves the returned omissions or
side-effect evidence. Do not retry, replace the producer with the orchestrator,
or infer a favorable disposition.

If the producer returns `CONCERNS` or `UNREALISTIC`, present exactly these
bounded choices to the planning owner:

1. Accept only non-blocking advisory concerns by recording a rationale, owner,
   and review point for every accepted finding; blocking findings cannot be
   waived this way.
2. Authorize one targeted plan revision addressing named stable finding IDs.

For the targeted revision, revise only the identified plan fields, then
re-render every candidate byte, rebuild the complete target inventory, recompute
the source-manifest and plan digests, and run `PR-EPIC` exactly once more. No
second revision or third review is permitted. If blocking concerns remain, the
disposition remains `UNREALISTIC`, or review is incomplete, stop with:

`BLOCKED — SCOPE DECISION REQUIRED`

Return the stable finding IDs and one concrete owner decision. Perform no
writes.

### Lean and solo modes

- Lean mode records `status: skipped`, `mode: lean`, and the omission reason.
- Solo mode runs zero agents and records `status: skipped`, `mode: solo`, and
  the omission reason.
- A skipped producer review is never represented as `REALISTIC`.
- Lean or solo mode still requires all local mapping, traceability, dependency,
  approval, authorization, CAS, and verification gates.

## 2. Exact plan approval

Before asking for mutation authority, show the planning owner an exact plan
preview containing:

- source-manifest ID and SHA-256 digest;
- every selected `module_id`, canonical epic ID, target path, and included
  `system_ids[]`;
- every skip and its reason;
- create, update, stale-update, no-op, or conflict classification;
- preimage and candidate SHA-256 hashes;
- epic status and every stable traceability finding;
- dependency edges and deterministic topological order;
- producer result and accepted advisory-concern records, if any;
- the proposed epic-index patch; and
- the proposed external receipt path.

Approval must use `cgs.epic-plan-approval/v1` and bind the exact bytes:

```yaml
schema: cgs.epic-plan-approval/v1
approval_id: <stable id>
planning_owner: <identity>
source_manifest_sha256: <sha256>
plan_sha256: <sha256>
module_map_sha256: <sha256>
dependency_graph_sha256: <sha256>
producer_result_sha256: <sha256 or null>
targets:
  <target_path>:
    classification: create | update | stale-update | no-op
    expected_preimage_sha256: <sha256 or ABSENT>
    candidate_sha256: <sha256>
index_expected_preimage_sha256: <sha256 or ABSENT>
index_candidate_sha256: <sha256>
receipt_path: <normalized path>
decision: approved
approved_at: <RFC3339 timestamp>
```

Approval confirms plan content only. It does not change GDD, architecture, ADR,
TR, or existing epic truth, and it does not authorize filesystem mutation.
Conflict candidates cannot appear in an approved plan.

If the owner declines or stops, return `DECLINED` or `STOPPED` with zero writes.
If the owner changes scope, rebuild the plan and obtain a new approval; do not
patch an old approval.

## 3. One bounded mutation authorization

After exact plan approval, present one changeset and request one explicit
mutation authorization. The changeset must contain only:

- selected create, update, and stale-update epic paths;
- the epic-index path and exact candidate hash;
- the create-only result-receipt path;
- every expected preimage hash or `ABSENT` marker;
- every candidate hash;
- source-manifest, plan-approval, producer-result, and plan hashes;
- intended writer and recorder identities; and
- explicit non-write paths.

Authorization must bind this exact set. An approval, producer review, prior
workflow authorization, or vague request to “continue” is not mutation
authorization. Adding, removing, renaming, or re-rendering any target invalidates
the authorization.

## 4. Pre-write compare-and-swap gates

Run all gates in one preflight immediately before the first write. Any mismatch
means zero writes. Reclassify, re-render, re-preview, and obtain fresh approval
and authorization where bytes or scope changed.

### Source CAS

- Re-read every source-manifest entry.
- Recompute every source SHA-256 and exact byte count.
- Recompute the canonical manifest digest.
- Require equality with the approved source manifest.
- Revalidate current-selection rules, exact `Approved` status, architecture
  target hashes, Accepted ADR lifecycle evidence, and TR-registry identities.

### Target-set CAS

- Re-read every selected epic target, the epic index, and receipt target in one
  inventory pass.
- Require each epic and index preimage to equal the authorized SHA-256 or
  `ABSENT` marker.
- Require the receipt target to remain `ABSENT`; receipts are create-only.
- Re-run create/no-op/update/stale-update/conflict classification.
- Require the complete normalized target set to equal the authorized set.

### Identity CAS

- Require every canonical `EPIC-MODULE:<module_id>` identity and target path to
  remain unique.
- Require each system-to-module responsibility slice to remain unambiguous.
- Require existing managed files to retain the expected managed schema and
  `module_id`.
- Require the index ownership/schema evidence to remain compatible.

### Approval and authorization CAS

- Require the plan approval to bind the current source, plan, module-map,
  dependency-graph, producer-result, target, index, and receipt hashes.
- Require the mutation authorization to bind the same current changeset.
- Require approval and authorization identities to remain attributable.

### Role CAS

- Require the active writer identity to equal the authorized writer.
- Require the active recorder identity to equal the authorized recorder.
- The planning owner, producer reviewer, writer, and recorder are separate roles
  in the evidence model even when lean staffing permits one human to hold more
  than one role. No role substitutes for another role's decision.

## 5. Bounded writes and verification

Write only after every CAS gate passes.

1. Write changed epic files in deterministic dependency order. Break equal-rank
   ties by canonical `order_key`, then `module_id`.
2. For each file, use an atomic single-file replacement where supported, then
   immediately read it back and verify exact candidate bytes and SHA-256.
3. Write and verify the epic index after every epic file succeeds.
4. Write the external result receipt last, as a create-only file, then read it
   back and verify its bytes and SHA-256.
5. Do not create story files, change story indexes, invoke `$create-stories`, or
   modify any source artifact.

Single-file replacement does not make a multi-file changeset atomic. Never
claim whole-set rollback or atomicity. If any write, read-back, hash, index, or
receipt step fails after at least one file was changed, preserve the evidence,
stop further ordinary writes, and return `Workflow PARTIAL`.

If safely possible within the already authorized receipt path, write a PARTIAL
result receipt listing exact applied and not-applied paths plus their expected,
preimage, candidate, and observed hashes. Do not overwrite an existing receipt
and do not attempt destructive rollback. If the receipt itself fails after all
epic and index writes, report an unreceipted changed set and remain PARTIAL; do
not claim completion.

## 6. External result receipt

Use `cgs.create-epics-result-receipt/v1`:

```yaml
schema: cgs.create-epics-result-receipt/v1
receipt_id: <stable id>
status: COMPLETE | PARTIAL
source_manifest_id: <id>
source_manifest_sha256: <sha256>
plan_sha256: <sha256>
plan_approval_id: <id>
plan_approval_sha256: <sha256>
mutation_authorization_id: <id>
mutation_authorization_sha256: <sha256>
producer_result_sha256: <sha256 or null>
writer_identity: <identity>
recorder_identity: <identity>
targets:
  <normalized path>:
    action: create | update | stale-update | no-op | not-applied
    expected_preimage_sha256: <sha256 or ABSENT>
    candidate_sha256: <sha256>
    observed_sha256: <sha256 or ABSENT | UNKNOWN>
index:
  path: <normalized path>
  expected_preimage_sha256: <sha256 or ABSENT>
  candidate_sha256: <sha256>
  observed_sha256: <sha256 or ABSENT | UNKNOWN>
finding_ids: []
recorded_at: <RFC3339 timestamp>
```

The receipt is evidence about the result; it is not an approval and cannot
authorize repair. Epic and index bytes may record the stable receipt ID, but
must not embed the receipt's path or hash, which would create a hash cycle.

## 7. Terminal outcomes

- `Workflow COMPLETE`: every selected create/update/stale-update was written and
  verified, every no-op was revalidated, the index matches, and the COMPLETE
  receipt exists and verifies.
- `Workflow COMPLETE — NO_CHANGES_REQUIRED`: every eligible target is a current
  no-op or an explicitly approved skip after fresh source and target checks. Do
  not create a receipt solely to record workflow activity.
- `Workflow PARTIAL`: a required source, producer, write, verification, or
  receipt operation is incomplete or failed after safe progress. Report exact
  evidence and one recovery action.
- `Workflow BLOCKED`: mapping ambiguity, invalid status, ADR/TR gap, dependency
  cycle, artifact conflict, unresolved producer scope decision, or CAS mismatch
  prevents a safe approved plan. Perform no writes for a pre-write block.
- `Workflow DECLINED` or `Workflow STOPPED`: the user declines or stops before
  authorized mutation. Perform zero writes.

Do not equate “process ran” with completion. The terminal verdict is determined
by verified artifact state and receipt state.

## 8. Downstream handoff

Offer exactly one next action. Prefer the highest-priority unresolved blocker.
Only when at least one epic is `Ready` may the next action be to prepare stories
for one named epic. The handoff must bind:

- epic ID, normalized path, and SHA-256;
- source-manifest ID and SHA-256;
- module ID and included system IDs;
- exact TR rows and stable finding IDs; and
- dependency/order evidence.

A `Blocked` epic remains ineligible for story creation. Never invoke a downstream
skill automatically.
