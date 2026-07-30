# Skill Spec: $soak-test

> **Spec ID**: soak-test-v2
> **Spec Schema**: cgs-skill-spec/v2
> **Category**: utility
> **Priority**: low
> **Spec written**: 2026-07-22

## Skill Summary

`$soak-test` plans exact build-bound endurance protocols, registers fully scheduled runs, ingests append-only evidence receipts, and finalizes unit-safe stability results. Planning, execution, evidence quality, dimension results, readiness, persistence, and handoff remain separate. Only a version and existence conflict check-persisted `cgs-soak-result/v2` with verified conclusive evidence is handoff eligible.

## Static Assertions

- **SOAK-STA-001**: Frontmatter contains only `name` and a non-empty `description`; name is `soak-test`.
- **SOAK-STA-002**: Plan, start, ingest, finalize, and status have explicit non-overlapping grammars.
- **SOAK-STA-003**: Plan requires an explicit target, duration, focus, workload profile, environment, candidate, and build receipt.
- **SOAK-STA-004**: Candidate and build receipt identity, artifact revision, source, engine, platform, and configuration are cross-validated.
- **SOAK-STA-005**: Protocol, run manifest, ingest manifest, finalize manifest, result, and completion receipt use versioned schemas.
- **SOAK-STA-006**: The full checkpoint schedule has unique stable IDs, elapsed offsets, and actual scheduled timestamps.
- **SOAK-STA-007**: Missing checkpoints are `NOT_COLLECTED`, never zero, carried forward, interpolated, or passed.
- **SOAK-STA-008**: Crash, hang, heartbeat timeout, OOM risk, thermal, corruption, resource safety, and observer stops have trigger/evidence/action/classification contracts.
- **SOAK-STA-009**: Existing protocols and results are immutable; extension requires a new ID and exact predecessor revision.
- **SOAK-STA-010**: Only the configured engine and exact verified adapter/version are loaded.
- **SOAK-STA-011**: QA, playtest, bug, and history context is consumed only by explicit path/revision and remains advisory unless authoritative.
- **SOAK-STA-012**: Stability, Memory, Performance, Experience, Recovery, Readiness, Workflow Verdict, and handoff are independent.
- **SOAK-STA-013**: Ingest creates an absent immutable receipt directory containing source, samples, and receipt.
- **SOAK-STA-014**: Finalization freezes exact receipt and sample-set revisions and rejects concurrent evidence drift.
- **SOAK-STA-015**: Smoke evidence cannot close an endurance regression; a matching endurance rerun is required.
- **SOAK-STA-016**: Every metric has stable identity, value kind, source field, raw/canonical units, conversion provenance, aggregation, and uncertainty.
- **SOAK-STA-017**: Thresholds come only from current project budgets or approved matching baselines.
- **SOAK-STA-018**: Missing, stale, mismatched, or unit-incompatible thresholds yield INCONCLUSIVE, never an invented default.
- **SOAK-STA-019**: Heartbeat, capture, run, output, graceful-stop, forced-stop, cleanup, and recovery budgets are explicit.
- **SOAK-STA-020**: Partial, invalid, and unknown samples and execution controls cannot become technical PASS.
- **SOAK-STA-021**: Publication requires target absence, authority revalidate, same-filesystem staging, atomic publish, and read-back.
- **SOAK-STA-022**: The canonical result and completion receipt carry exact evidence paths and revision values.
- **SOAK-STA-023**: Handoff eligibility means verified consumable evidence, not readiness success.
- **SOAK-STA-024**: A protocol or run registration is never executed evidence.

## Protocol Assertions

- **SOAK-PRO-001**: Resolve literal project-relative paths and validate stable IDs, schemas/versions, and explicit revisions before parsing.
- **SOAK-PRO-002**: Reject duplicate keys, unsafe paths, globs, latest-file discovery, and identity conflicts.
- **SOAK-PRO-003**: Never synthesize a runner command or use an unverified engine adapter.
- **SOAK-PRO-004**: Never invent, smooth, interpolate, or silently convert sample values.
- **SOAK-PRO-005**: Preserve complete pre-termination samples and classify all later checkpoints explicitly.
- **SOAK-PRO-006**: Verify full process-tree cleanup and required recovery checkpoints.
- **SOAK-PRO-007**: Never overwrite or mutate prior protocol, run, receipt, result, or shared history bytes.
- **SOAK-PRO-008**: Treat subjective experience independently from objective technical dimensions.
- **SOAK-PRO-009**: Reject finalization when receipt membership changes during version and existence conflict check.
- **SOAK-PRO-010**: Preserve observed dimension results if persistence fails, but force handoff NO.
- **SOAK-PRO-011**: Downstream consumers receive exact result/completion paths and revisions and revalidate all members.
- **SOAK-PRO-012**: Never invoke a smoke check, bug workflow, retest, or downstream gate automatically.
- **SOAK-PRO-013**: Never treat a finalized artifact as an automatic release PASS.
- **SOAK-PRO-014**: Never edit product, tests, candidate, build, profile, environment, metric, adapter, or shared catalog authorities.

## Test Cases

### Case 1 [SOAK-C01] — Explicit plan grammar and exact candidate/build manifests

#### Fixture

A caller supplies target `combat-loop`, duration, focus, exact workload and environment manifests, a candidate manifest, and a successful matching build receipt. A second caller supplies the historical shorthand `$soak-test combat 2h`.

#### Input

Parse both requests and validate every supplied authority revision.

#### Expected reads

Only the explicit candidate, build receipt, workload, environment, metric policy, adapter, and optional history authorities named by path and revision.

#### Expected writes

None for the shorthand. For a valid authorized `plan --save`, only the new immutable protocol directory.

#### Expected non-writes

No inferred target, generated build receipt, run root, result, shared authority edit, or live skill edit.

#### Expected behavior

The exact plan request validates target, duration, focus, profile conditions, candidate/build identities, and all required flags. The shorthand and every missing or illegal argument are BLOCKED before a write.

#### Assertions

SOAK-STA-002, SOAK-STA-003, SOAK-STA-004, SOAK-STA-005, SOAK-PRO-001, SOAK-PRO-002.

#### Case Verdict

PASS only if the exact request is accepted and the shorthand is rejected without writes.

### Case 2 [SOAK-C02] — Early crash preserves evidence and applies the stop contract

#### Fixture

A run reaches three checkpoints, records a version-bound crash event, then cannot reach later checkpoints. The protocol declares crash evidence, shutdown, cleanup, recovery, and classification rules.

#### Input

Ingest the crash receipt and finalize with termination `CRASH`.

#### Expected reads

The exact run manifest, protocol, stop-trigger row, evidence receipts, sample ledgers, process-tree cleanup record, and recovery observations.

#### Expected writes

An immutable evidence receipt followed by an authorized result/report/completion receipt under the same run root.

#### Expected non-writes

No discarded early samples, fabricated later values, resumed same-run schedule, technical PASS, or modified protocol.

#### Expected behavior

Pre-crash samples remain traceable. Later checkpoints become `NOT_COLLECTED`; verified crash makes Execution FAILED_EARLY and Stability FAIL. Cleanup and recovery retain their independent classifications.

#### Assertions

SOAK-STA-007, SOAK-STA-008, SOAK-STA-019, SOAK-PRO-005, SOAK-PRO-006.

#### Case Verdict

A conclusive negative result may be finalized and handed off only when all evidence/provenance verifies; readiness remains FAIL.

### Case 3 [SOAK-C03] — History extension creates a new immutable protocol

#### Fixture

A revision-valid history index maps target/profile/environment to `SOAK-PROTO-combat-v1`. A longer request names the predecessor path/revision and a new ID `SOAK-PROTO-combat-v2`.

#### Input

Plan the extension with explicit history-index and supersedes fields.

#### Expected reads

The exact history index, predecessor protocol, candidate/build/profile/environment authorities, and their revisions.

#### Expected writes

Only the absent v2 protocol directory after authorization.

#### Expected non-writes

No v1 edit, result edit, in-place extension, history-index mutation, or timestamp-based selection.

#### Expected behavior

The workflow verifies the predecessor key, records path/revision and changed fields in v2, and leaves every old byte untouched.

#### Assertions

SOAK-STA-009, SOAK-PRO-007.

#### Case Verdict

PASS when v2 is a new immutable version and all protected predecessors remain byte-identical.

### Case 4 [SOAK-C04] — Unsupported engine adapter is blocked

#### Fixture

The candidate declares engine version 4.6.3 but the supplied adapter supports 4.5.x. Another adapter for an unrelated engine is locally available.

#### Input

Validate the plan authorities.

#### Expected reads

The exact candidate and supplied adapter manifests only.

#### Expected writes

None.

#### Expected non-writes

No generic runner manifest, transplanted metric guidance, other-engine instructions, protocol, or evidence.

#### Expected behavior

The version mismatch yields `Adapter Status: NEEDS_CONFIRMATION`, gate capability NO, and Workflow Verdict BLOCKED. The unrelated adapter is ignored.

#### Assertions

SOAK-STA-010, SOAK-PRO-003.

#### Case Verdict

BLOCKED with no executable protocol or handoff claim.

### Case 5 [SOAK-C05] — Explicit context revisions prevent unrelated issue import

#### Fixture

The plan authority pins one QA plan and one prior soak result for the same target/build family. A newer but unrelated playtest report exists.

#### Input

Resolve plan context.

#### Expected reads

Only the pinned current QA plan and prior result by exact path/revision, plus required direct authorities.

#### Expected writes

At most the authorized new protocol.

#### Expected non-writes

No newest-file scan, unrelated playtest import, scope expansion, or threshold change from advisory prose.

#### Expected behavior

Matching pinned context is labeled by authority role. The unrelated report is not read or imported. Advisory context cannot alter test scope, identities, or metric budgets.

#### Assertions

SOAK-STA-011, SOAK-PRO-001, SOAK-PRO-002.

#### Case Verdict

PASS when all context is exact, current, and correctly labeled; otherwise BLOCKED or advisory-only.

### Case 6 [SOAK-C06] — Technical and experience dimensions remain independent

#### Fixture

Variant A has Stability, Memory, and Performance PASS with conclusive fatigue Experience FAIL. Variant B has Experience PASS and Memory FAIL. Variant C excludes Experience.

#### Input

Calculate dimension and readiness results using the named gate policy.

#### Expected reads

Verified samples, exact metric policy, threshold sources, experience evidence, and gate-policy path/revision.

#### Expected writes

Only the authorized finalized result set.

#### Expected non-writes

No aggregate field that rewrites a dimension and no automatic release decision.

#### Expected behavior

A preserves objective PASS fields and Experience FAIL; B preserves Memory FAIL; C records Experience NOT_IN_SCOPE. Readiness follows only required policy dimensions.

#### Assertions

SOAK-STA-012, SOAK-PRO-008, SOAK-PRO-013.

#### Case Verdict

PASS when all independent fields remain unchanged and readiness is deterministically derived.

### Case 7 [SOAK-C07] — Append-only ingest and immutable finalization

#### Fixture

Two absent receipt IDs supply complete checkpoint evidence. After preview, an actor modifies one source byte before ingest. In a second run, receipt membership changes during finalization.

#### Input

Attempt ingest, then attempt finalization against a frozen receipt-set revision.

#### Expected reads

Exact run, ingest, and finalize manifests; raw source bytes; receipt directories; authority revisions; and final-root absence.

#### Expected writes

Private staging only for conflicted attempts. A successful attempt writes one absent receipt directory or the three absent result members.

#### Expected non-writes

No overwrite, partial final directory, changed source capture, silently expanded receipt set, or prior evidence edit.

#### Expected behavior

Source drift fails ingest version and existence conflict check. Receipt-set drift fails finalize version and existence conflict check. Successful ingest copies source byte-for-byte and publishes source, samples, and receipt all-or-none.

#### Assertions

SOAK-STA-013, SOAK-STA-014, SOAK-STA-021, SOAK-PRO-007, SOAK-PRO-009.

#### Case Verdict

Conflict attempts are ERROR with handoff NO; only unchanged absent-target transactions pass.

### Case 8 [SOAK-C08] — Endurance regression requires matching re-soak

#### Fixture

A prior exact result proves a memory regression. A code fix has a current smoke PASS but no new soak result.

#### Input

Evaluate retest and closure guidance.

#### Expected reads

The prior result/receipt revisions, fixed candidate/build identities, and smoke receipt only as labeled precondition context.

#### Expected writes

None.

#### Expected non-writes

No closed endurance finding, copied PASS, automatic smoke invocation, or automatic retest run.

#### Expected behavior

The workflow requires a new protocol/run with the same target, workload, environment, metric policy, and duration, plus exact predecessor result revision. Smoke cannot close the regression.

#### Assertions

SOAK-STA-015, SOAK-PRO-012.

#### Case Verdict

INCONCLUSIVE for repair verification until a matching endurance rerun is finalized.

### Case 9 [SOAK-C09] — Full checkpoint expansion and missed-sample semantics

#### Fixture

Duration is 65 minutes, interval is 20 minutes, warm-up is 5 minutes, and the run starts at a fixed RFC 3339 timestamp.

#### Input

Generate the protocol schedule and validate a corresponding run manifest.

#### Expected reads

Duration, interval, warm-up policy, Metric IDs, start time, monotonic origin, and canonicalization rules.

#### Expected writes

An authorized immutable protocol and later the exact run manifest.

#### Expected non-writes

No repeat-section placeholder, duplicate Checkpoint ID, inferred timestamp, omitted final checkpoint, or zero-valued missing sample.

#### Expected behavior

The schedule includes baseline, 20-, 40-, 60-, and exact 65-minute checkpoints with unique IDs, exact elapsed offsets, and start-derived scheduled timestamps. A missed 40-minute sample becomes `NOT_COLLECTED`.

#### Assertions

SOAK-STA-006, SOAK-STA-007.

#### Case Verdict

PASS only when schedule bytes and revision are deterministic and every expected checkpoint has one disposition.

### Case 10 [SOAK-C10] — Resource units and baseline compatibility are fail-closed

#### Fixture

A memory metric arrives in MiB while the policy requires bytes and pins a conversion. Its baseline was collected on a different workload. A performance counter wraps once.

#### Input

Normalize samples and evaluate metric readiness.

#### Expected reads

Metric contracts, conversion ID/version, counter wrap rule, baseline path/revision/revision/applicability, and raw evidence.

#### Expected writes

Only immutable samples and an authorized result that preserves raw and canonical values.

#### Expected non-writes

No implicit MiB/MB conversion, transplanted baseline, invented threshold, smoothed counter, or PASS from incompatible units.

#### Expected behavior

The pinned conversion is applied and recorded. The mismatched baseline yields Threshold UNAVAILABLE and Memory INCONCLUSIVE. Counter wrap follows only its exact declared rule.

#### Assertions

SOAK-STA-016, SOAK-STA-017, SOAK-STA-018, SOAK-PRO-004.

#### Case Verdict

INCONCLUSIVE for any metric lacking compatible unit and threshold evidence.

### Case 11 [SOAK-C11] — Heartbeat timeout, cleanup, and recovery remain explicit

#### Fixture

A harness misses its heartbeat deadline, graceful stop expires, forced stop removes most children, one child remains, and required recovery samples are absent.

#### Input

Ingest watchdog/cleanup evidence and finalize with `HEARTBEAT_TIMEOUT`.

#### Expected reads

Exact harness budgets, process-tree snapshot, stop attempts, output/flush state, recovery rules, and all checkpoint receipts.

#### Expected writes

An authorized result may preserve the partial evidence and exact control states.

#### Expected non-writes

No clean-cleanup claim, recovered claim, resume under the same run ID, technical PASS, or discarded pre-timeout evidence.

#### Expected behavior

Stop is classified from evidence; cleanup is DIRTY; recovery is UNKNOWN; execution is PARTIAL unless a verified objective trigger independently proves FAILED_EARLY; affected metrics/readiness are INCONCLUSIVE.

#### Assertions

SOAK-STA-008, SOAK-STA-019, SOAK-STA-020, SOAK-PRO-005, SOAK-PRO-006.

#### Case Verdict

INCONCLUSIVE with handoff NO unless a separate fully verified negative-evidence policy is satisfied.

### Case 12 [SOAK-C12] — Partial, invalid, and unknown samples cannot pass

#### Fixture

One sample is truncated, one has an unknown unit, one lacks observer identity, and two checkpoints have no records.

#### Input

Ingest and finalize the bounded evidence set.

#### Expected reads

Raw source bytes, parser contract, unit policy, observer/harness identity, expected checkpoint schedule, and receipt revisions.

#### Expected writes

Immutable bounded evidence and an authorized result marking each row and checkpoint explicitly.

#### Expected non-writes

No interpolation, zero fill, carry-forward, hidden row deletion, or technical PASS.

#### Expected behavior

Rows become PARTIAL, INVALID, or UNKNOWN; missing checkpoints become NOT_COLLECTED; Evidence is PARTIAL or INVALID; execution/readiness are PARTIAL or INCONCLUSIVE and handoff is NO.

#### Assertions

SOAK-STA-007, SOAK-STA-020, SOAK-PRO-004, SOAK-PRO-005.

#### Case Verdict

INCONCLUSIVE or ERROR, never PASS.

### Case 13 [SOAK-C13] — version and existence conflict check persistence and exact handoff semantics

#### Fixture

A complete conclusive negative stability result is rendered. The first attempt has an absent target; the second attempt encounters an existing result path.

#### Input

Publish the result set and construct downstream handoff.

#### Expected reads

Every frozen authority/evidence byte, target absence, rendered schemas, internal member revisions, and read-back bytes.

#### Expected writes

For the first attempt, exactly result.json, report.md, and completion-receipt.json. For the second, no final write.

#### Expected non-writes

No overwrite, partial publication, mutable latest pointer, summary-only handoff, or readiness PASS implied by handoff eligibility.

#### Expected behavior

The first attempt version and existence conflict check-publishes and read-back verifies the negative result; it may be handoff eligible while Readiness remains FAIL. The collision returns Persistence CONFLICT and handoff NO.

#### Assertions

SOAK-STA-021, SOAK-STA-022, SOAK-STA-023, SOAK-PRO-010, SOAK-PRO-011, SOAK-PRO-013.

#### Case Verdict

PASS only for verified immutable publication and exact path/revision handoff; collision is ERROR without overwrite.

### Case 14 [SOAK-C14] — Complete scheduled run happy path

#### Fixture

All exact authorities are current; the configured adapter matches; all thresholds/baselines and units validate; every scheduled checkpoint is collected; no stop trigger fires; cleanup/recovery requirements are satisfied or validly not required.

#### Input

Plan, register, ingest the frozen evidence set, finalize, and verify as a downstream consumer.

#### Expected reads

Exact candidate/build/profile/environment/metric/adapter/protocol/run/ingest/finalize manifests and every evidence member by path/revision.

#### Expected writes

One immutable protocol directory, one immutable run manifest, absent receipt directories, and one atomically published result/report/completion set.

#### Expected non-writes

No source authority edit, old artifact overwrite, legacy evidence, undeclared runner, newest-file lookup, or automatic downstream action.

#### Expected behavior

The workflow expands deterministic checkpoints, preserves unit-safe samples, freezes receipt membership, derives EXECUTED and VERIFIED, computes each independent dimension and Readiness PASS, version and existence conflict check-publishes, reads back, and returns exact result/completion paths and revisions with handoff YES.

#### Assertions

SOAK-STA-001 through SOAK-STA-024; SOAK-PRO-001 through SOAK-PRO-014.

#### Case Verdict

PASS only when all bindings, evidence, dimension policies, persistence checks, and downstream revalidate verification succeed.

## P1 Remediation Trace

```yaml
schema: cgs-p1-remediation-trace/v1
entries:
  - audit_id: SOAK-004
    skill_clause_ids: [SOAK-CL-004]
    spec_case_ids: [SOAK-C01]
    assertion_ids: [SOAK-STA-002, SOAK-STA-003, SOAK-STA-004, SOAK-STA-005, SOAK-PRO-001, SOAK-PRO-002]
  - audit_id: SOAK-005
    skill_clause_ids: [SOAK-CL-005]
    spec_case_ids: [SOAK-C02, SOAK-C11]
    assertion_ids: [SOAK-STA-008, SOAK-STA-019, SOAK-STA-020, SOAK-PRO-005, SOAK-PRO-006]
  - audit_id: SOAK-006
    skill_clause_ids: [SOAK-CL-006]
    spec_case_ids: [SOAK-C03]
    assertion_ids: [SOAK-STA-009, SOAK-PRO-007]
  - audit_id: SOAK-007
    skill_clause_ids: [SOAK-CL-007]
    spec_case_ids: [SOAK-C04]
    assertion_ids: [SOAK-STA-010, SOAK-PRO-003]
  - audit_id: SOAK-008
    skill_clause_ids: [SOAK-CL-008]
    spec_case_ids: [SOAK-C05]
    assertion_ids: [SOAK-STA-011, SOAK-PRO-001, SOAK-PRO-002]
  - audit_id: SOAK-009
    skill_clause_ids: [SOAK-CL-009]
    spec_case_ids: [SOAK-C06]
    assertion_ids: [SOAK-STA-012, SOAK-PRO-008, SOAK-PRO-013]
  - audit_id: SOAK-010
    skill_clause_ids: [SOAK-CL-010A, SOAK-CL-010B]
    spec_case_ids: [SOAK-C07, SOAK-C13]
    assertion_ids: [SOAK-STA-013, SOAK-STA-014, SOAK-STA-021, SOAK-STA-022, SOAK-PRO-007, SOAK-PRO-009, SOAK-PRO-010]
  - audit_id: SOAK-011
    skill_clause_ids: [SOAK-CL-011]
    spec_case_ids: [SOAK-C08]
    assertion_ids: [SOAK-STA-015, SOAK-PRO-012]
  - audit_id: SOAK-012
    skill_clause_ids: [SOAK-CL-012]
    spec_case_ids: [SOAK-C09]
    assertion_ids: [SOAK-STA-006, SOAK-STA-007]
```

Every P1 ID has an explicit clause/case/assertion join; a prose range is not a
traceability substitute. This written spec does not claim execution. Runtime
claims still require current immutable receipts bound to the exact candidate.
