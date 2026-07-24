# Propagate Design Change — Continued Workflow

This reference is normative for `$propagate-design-change`. It continues the
read-only analysis in `../SKILL.md`. It authorizes no downstream artifact change
and must be read before any report or receipt approval request.

## 1. Independent technical review

Run review only after the baseline/current pair, stable diff, bounded source
manifest, coverage table, complete currently known graph, stable impacts/findings,
active-work freezes, owner routes, report candidate, and receipt candidate are
hash-stable.

### Full mode

- Make one bounded, read-only technical-review call named `TD-CHANGE-IMPACT`.
- Allow one initial attempt lasting at most 60 seconds.
- The reviewer identity must differ from the analysis author and report writer.
- The reviewer cannot delegate, edit, approve, authorize, record, or stand in for
  an artifact owner.
- Pass exact baseline/current, diff, source-manifest, graph, impact-plan, report,
  and receipt candidate hashes.
- Require `cgs.pdc-technical-review-result/v2`:

```yaml
schema: cgs.pdc-technical-review-result/v2
review_id: TD-CHANGE-IMPACT
mode: full
status: complete | partial | timeout | failed | side-effect
disposition: APPROVE | CONCERNS | REJECT | null
analysis_author_identity: <identity>
reviewer_identity: <different identity>
baseline_sha256: <sha256>
current_sha256: <sha256>
diff_sha256: <sha256>
source_manifest_sha256: <sha256>
graph_sha256: <sha256>
impact_plan_sha256: <sha256>
report_candidate_sha256: <sha256>
finding_ids: []
omissions: []
```

`partial`, `timeout`, `failed`, `side-effect`, missing independence, or hash
mismatch yields PARTIAL. It forbids any downstream resolution write and cannot be
replaced by self-review or an inferred pass. A PARTIAL impact report/result
receipt may still be proposed as evidence if all report-only gates pass.

For `CONCERNS` or `REJECT`, the planning owner may stop or authorize exactly one
targeted analysis revision addressing named stable finding IDs. Recompute all
affected diff/manifest/graph/impact/plan/report/receipt hashes, re-inventory the
complete target set, and make exactly one re-review call. No second revision or
third review is permitted. Continued rejection, blocking concern, incomplete
review, or non-convergence yields PARTIAL or
`BLOCKED — OWNER OR SCOPE DECISION REQUIRED`; do not write downstream artifacts.

Non-blocking concerns may be retained only with a named owner, rationale,
acceptance condition, and review point. The reviewer cannot waive PARTIAL
coverage, ambiguous identity, active-work coordination, or missing owner evidence.

### Lean and solo modes

- Lean runs no reviewer and records `status: skipped`, `mode: lean`, and the
  omission reason.
- Solo invokes zero agents and records `status: skipped`, `mode: solo`, and the
  omission reason.
- Skipped is not `APPROVE` and the result must disclose that the analysis was not
  independently reviewed.
- All local coverage, ownership, approval, authorization, CAS, receipt, and
  convergence requirements remain unchanged.

## 2. Exact report-plan approval

After bounded owner decisions and review, present one exact preview containing:

- change ID and immutable baseline/current locators, paths, byte counts, hashes,
  and diff range;
- diff/source-manifest/coverage/graph hashes and every continuation omission;
- every stable delta, impact, finding, artifact snapshot, lifecycle, dependency,
  active-work freeze, and owner route;
- accepted/deferred decisions with rationale, owner, review point, and evidence;
- technical-review result and stable findings;
- report path, expected preimage, full candidate hash or existing immutable report
  hash;
- prior receipt-chain head, proposed sequence/path, expected ABSENT preimage, and
  receipt candidate hash; and
- every source and downstream non-write path/category.

Approval uses `cgs.pdc-report-plan-approval/v2`:

```yaml
schema: cgs.pdc-report-plan-approval/v2
approval_id: <stable id>
planning_owner: <identity>
change_id: <id>
baseline_sha256: <sha256>
current_sha256: <sha256>
diff_sha256: <sha256>
source_manifest_sha256: <sha256>
graph_sha256: <sha256>
impact_plan_sha256: <sha256>
technical_review_sha256: <sha256 or null>
report_path: production/change-impact/<change_id>.md
report_expected_preimage_sha256: <sha256 or ABSENT>
report_candidate_or_root_sha256: <sha256>
previous_receipt_sha256: <sha256 or ROOT>
receipt_path: <normalized create-only path>
receipt_candidate_sha256: <sha256>
decision: approved
approved_at: <RFC3339 timestamp>
```

Approval confirms report and route-plan content. It does not approve or authorize
any GDD, registry, ADR, architecture, epic, story, sprint, implementation, test,
owner-record, or readiness mutation. A scope, route, lifecycle, candidate byte,
source hash, receipt head, identity, or path change invalidates approval.

## 3. Report-only mutation authorization

After plan approval, request one explicit authorization for exactly:

1. the immutable report create when its expected preimage is `ABSENT`; and
2. one create-only result/convergence receipt at the exact proposed path.

For a continuation run with an existing valid report, authorize only the new
receipt. The authorization binds approval ID/hash, change ID, report root hash,
receipt-chain head, exact target paths/preimages/candidate hashes, writer,
recorder, and explicit non-write categories. Never ask per impact or per owner.

A request to “apply the design change,” owner-route approval, reviewer approval,
or prior run authorization is not report mutation authorization. Any downstream
write in the proposed set is invalid and stops BLOCKED.

If the user declines or stops, return DECLINED or STOPPED with zero writes.

## 4. Pre-write compare-and-swap gates

Run every gate in one read-only preflight immediately before the first write. Any
pre-write mismatch produces zero writes, invalidates stale approval/authorization,
and requires re-analysis or a new preview.

### Baseline/current and source CAS

- Re-read immutable baseline bytes and current GDD bytes and require the approved
  paths, resolved locator IDs, byte counts, and SHA-256 hashes.
- Re-read every source-manifest path and inventory authority; require exact bytes,
  hashes, parse/coverage states, loaded/omitted set, node/edge/impact counts, and
  deterministic continuation boundary.
- Recompute diff, manifest, coverage, graph, impact, finding, owner-route, and
  technical-review input hashes.

### Impact and owner-evidence CAS

- Re-derive every stable change/delta/impact/finding/artifact ID.
- Revalidate TR and dependency closure, artifact snapshots, ownership, active-work
  status/updated-at/hash, coordination receipts, and owner-resolution receipts.
- Require all receipt identities, schemas, target hashes, transitions, and
  verification evidence to match the approved fold.

### Immutable target and chain CAS

- If creating the report, require its target to remain `ABSENT`.
- If continuing, require the existing report bytes/hash/schema/change ID to equal
  the approved immutable root.
- Inventory the bounded receipt directory and require exactly one linear chain,
  the approved head, no fork/gap/duplicate predecessor, and the proposed receipt
  target `ABSENT`.
- Recompute the deterministic folded state and proposed sequence/digest prefix.

### Approval, authorization, and role CAS

- Require current bytes/state to match every hash in the report-plan approval.
- Require mutation authorization to bind only the current report/receipt set.
- Require active analysis author, reviewer, planning owner, writer, and recorder
  identities to match their evidence. In full mode enforce reviewer independence.

## 5. Bounded write and verification protocol

After all CAS gates pass:

1. If the report is absent, create it using atomic single-file creation where
   supported; read it back and verify exact candidate bytes and SHA-256.
2. If the report already exists, do not rewrite, touch, reformat, or timestamp it.
3. Create the result/convergence receipt last; read it back and verify exact bytes
   and SHA-256.
4. Re-read the report root and predecessor receipt and verify that the new receipt
   extends the authorized linear chain.
5. Do not perform any downstream or owner-plan write before, between, or after
   those evidence writes.

Atomic single-file creation does not make the two-file initial run atomic. Never
claim multi-file rollback. If the report is created but receipt creation or
verification fails, return PARTIAL with an unreceipted immutable report root,
stop further writes, and preserve exact expected/observed hashes. Do not delete or
overwrite the report. A later authorized recovery receipt may attach to that root.

If receipt creation succeeds but final chain verification fails, return PARTIAL,
identify the conflicting chain evidence, and do not create a compensating receipt
under the stale state.

## 6. Result and convergence receipt

Use `cgs.pdc-result-receipt/v2`:

```yaml
schema: cgs.pdc-result-receipt/v2
receipt_id: <stable id>
change_id: <id>
sequence: <positive integer>
status: PARTIAL | NO_IMPACT | ANALYSIS_COMPLETE | CONVERGED
report_path: production/change-impact/<change_id>.md
report_sha256: <sha256>
previous_receipt_sha256: <sha256 or ROOT>
baseline_sha256: <sha256>
current_sha256: <sha256>
diff_sha256: <sha256>
source_manifest_sha256: <sha256>
graph_sha256: <sha256>
impact_plan_sha256: <sha256>
technical_review_sha256: <sha256 or null>
plan_approval_id: <id>
plan_approval_sha256: <sha256>
mutation_authorization_id: <id>
mutation_authorization_sha256: <sha256>
writer_identity: <identity>
recorder_identity: <identity>
coverage_transitions: []
impact_transitions: []
finding_transitions: []
owner_resolution_receipts: []
coordination_receipts: []
open_impact_ids: []
open_finding_ids: []
continuation_shards: []
recorded_at: <RFC3339 timestamp>
```

Every transition records prior/current lifecycle, evidence path/hash, owner, and
acceptance condition. A receipt cannot rewrite the report, authorize downstream
work, manufacture an owner resolution, close a missing edge, or skip a sequence.

Receipt IDs and paths are derived from `change_id`, sequence, and canonical
candidate digest. The receipt does not embed its own final hash.

## 7. Fold and convergence verification

Fold the immutable report followed by receipts in ascending sequence. Reject an
illegal lifecycle transition, mismatched predecessor, evidence that predates its
claimed artifact preimage, duplicate receipt, or receipt for another change ID.

For each delta, closure requires either:

- `NO_IMPACT_PROVEN` with complete layer/dependency coverage; or
- every reachable stable impact RESOLVED by a current owner receipt and verified
  artifact postimage.

`ANALYSIS_COMPLETE` means the bounded full graph is proven and every non-resolved
impact has a valid owner route/freeze; it does not mean downstream resolution.
`CONVERGED` additionally requires every delta closed, all impacts RESOLVED or
no-impact proven, no open findings/deferred routes/partial shards, complete
dependency closure, valid owner/coordination receipts, and a fresh rescan of the
same baseline/current pair with no new impacts.

One run permits one analysis/review cycle, at most one targeted revision/re-review,
four decision interactions, one report create, and one receipt create. Remaining
work is PARTIAL with one deterministic continuation shard; never loop until pass.

## 8. Terminal outcomes

- `NO_CHANGE`: verified hashes equal; no report, receipt, approval, or write.
- `NEW_GDD`: valid baseline proves absence; report the new-file condition without
  claiming downstream no-impact and perform no automatic propagation.
- `BLOCKED`: baseline/change identity, immutable target, chain, approval,
  authorization, or safety conflict prevents trustworthy evidence; pre-write
  block means zero writes.
- `PARTIAL`: any required layer, mapping, owner, active-work field, bounded fanout,
  review, decision batch, write, receipt, or convergence proof is incomplete.
- `NO_IMPACT`: a real diff exists and every delta has full no-impact closure.
- `ANALYSIS_COMPLETE`: every impact is stable, complete, and owner-routed or
  resolved, but downstream work may remain.
- `CONVERGED`: every delta, dependency, impact, finding, coordination, and owner
  resolution is closed and freshly revalidated.
- `DECLINED` / `STOPPED`: the user declines or stops evidence creation; zero
  unauthorized writes.

Never use generic COMPLETE to blur analysis completion with downstream
convergence. PARTIAL cannot be upgraded by approval, reviewer disposition,
successfully scanned empty subsets, or report creation.

## 9. Handoff

Return exactly one next action. Prefer the highest-priority open coordination,
coverage, owner, TR, or dependency finding. Otherwise route one named impact to
its declared owner workflow, binding change/impact/artifact IDs, report/receipt
hashes, artifact preimage hash, requested action, acceptance condition, and
required resolution receipt schema. Do not invoke the workflow automatically.
