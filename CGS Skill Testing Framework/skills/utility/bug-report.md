# Skill Spec: $bug-report

> **Spec ID**: bug-report-v2
> **Spec Schema**: cgs-skill-spec/v2
> **Category**: utility
> **Priority**: low
> **Spec written**: 2026-07-23

## Skill Summary

`$bug-report` uses explicit manifest-driven subcommands to draft, analyze, create,
record one exact hotfix candidate, verify, close, or inspect canonical bug
records. Records live only under `production/qa/bugs/`; only this canonical
registry recorder may move Open/Reopened to Fixed Pending Verification under
owner authority and an atomic append-only event transaction.

## Static Assertions

- **BR-STA-001**: Frontmatter contains only `name` and non-empty `description`; name is `bug-report`.
- **BR-STA-002**: Draft, analyze, create, record-fix-candidate, verify, close, and status have explicit non-overlapping syntax.
- **BR-STA-003**: Unknown modes, illegal flag combinations, positional descriptions/paths, and malformed IDs fail before business work.
- **BR-STA-004**: Required, optional, and explicitly unknown draft fields are separately defined.
- **BR-STA-005**: Missing required build, reproduction, expected, actual, system, environment, or severity fields keep the draft incomplete and unwritten.
- **BR-STA-006**: Duplicate stable business keying yields candidates only; a human decision is required.
- **BR-STA-007**: Linked occurrences preserve their independent build, environment, repro, and evidence identity.
- **BR-STA-008**: Registry sequence allocation uses an exclusive lock, preimage CAS, absent targets, and read-back.
- **BR-STA-009**: Creation idempotency maps the same request/revision to the same Bug ID.
- **BR-STA-010**: Analyze accepts only explicit project paths/revisions and bounded files/bytes/findings.
- **BR-STA-011**: Static analysis outputs candidate findings with observation, inference, confidence, and reproduction gate; it cannot register a runtime defect.
- **BR-STA-012**: Verify selects only exact Test IDs and ordered argv from `cgs-test-execution-manifest/v1`.
- **BR-STA-013**: Runner identity, cwd, environment allowlist, deadlines, caps, cleanup, parser, exit code, and log revision are preserved.
- **BR-STA-014**: NOT_RUN, TIMEOUT, RUNNER_ERROR, PARSE_ERROR, PARTIAL, STALE, UNAVAILABLE, and INVALID_RECEIPT cannot verify.
- **BR-STA-015**: Canonical severity is exactly S1-Critical, S2-Major, S3-Minor, or S4-Trivial.
- **BR-STA-016**: Priority remains independent and is not assigned by this workflow.
- **BR-STA-017**: Canonical record path is exactly `production/qa/bugs/{bug-id}.md`.
- **BR-STA-018**: Canonical records use `cgs-bug-record/v2` and registry `cgs-bug-registry/v2`.
- **BR-STA-019**: Legal states are Open, Reopened, Fixed Pending Verification, Verified Fixed, and Closed with explicit owners/evidence.
- **BR-STA-020**: Static inspection is always runtime-unverified and cannot transition status.
- **BR-STA-021**: Verified Fixed requires matching reproduction PASS and automated failure-sensitive regression PASS.
- **BR-STA-022**: Closed requires current verification plus the same revalidated automated regression evidence.
- **BR-STA-023**: Manual evidence never replaces the automated regression gate and no waiver is invented.
- **BR-STA-024**: Record, registry, and immutable append-only event update all-or-none.
- **BR-STA-025**: `record-fix-candidate` consumes only a current `cgs-hotfix-bug-candidate-link/v1` as business handoff and exact joined commit/candidate/build/test identities.
- **BR-STA-026**: Only the authorized canonical bug-registry recorder may write Open/Reopened to Fixed Pending Verification.
- **BR-STA-027**: Recording a fix candidate never writes Verified Fixed or Closed and never treats hotfix as registry authority.
- **BR-STA-028**: The fix-candidate transition, bug record, registry row, and immutable recorder receipt commit all-or-none under CAS.

## Protocol Assertions

- **BR-PRO-001**: revision raw manifests and authorities before parsing and reject duplicate keys.
- **BR-PRO-002**: Never read a legacy path or triage report as a canonical bug record.
- **BR-PRO-003**: Never write a canonical record from an incomplete draft.
- **BR-PRO-004**: Never auto-merge, close, or discard a duplicate occurrence.
- **BR-PRO-005**: Never allocate an ID outside the atomic registry transaction.
- **BR-PRO-006**: Never auto-retry an allocation conflict with a hidden new ID.
- **BR-PRO-007**: Never promote a static candidate finding into an observed runtime bug.
- **BR-PRO-008**: Never synthesize a runner command, select tests by name, or fall back to an arbitrary suite.
- **BR-PRO-009**: Never accept an old log based on recency; exact build/commit/platform/manifest/Test ID revisions must match.
- **BR-PRO-010**: Never treat partial, timeout, runner, parser, cleanup, or unreadable evidence as verified.
- **BR-PRO-011**: Never convert legacy textual severity silently.
- **BR-PRO-012**: Never infer priority or schedule from severity.
- **BR-PRO-013**: Never create an illegal status transition or transition a Closed record.
- **BR-PRO-014**: Never accept manual verification as the regression test.
- **BR-PRO-015**: Never edit triage, sprint, hotfix, release, test-plan, source, or test artifacts.
- **BR-PRO-016**: Never invoke another workflow automatically.
- **BR-PRO-017**: Never accept a PR URL, newest build, deployment claim, or conversation in place of the exact candidate link and transitive revisions.
- **BR-PRO-018**: Never let hotfix write or impersonate a canonical bug-registry transaction.
- **BR-PRO-019**: Never upgrade FIX_CANDIDATE evidence into QA verification.
- **BR-PRO-020**: Never publish a candidate transition unless every member and receipt read back at the rendered revision.

## Test Cases

### Case 1 — Manual verification cannot close an ordinary fixed bug

#### Fixture

A canonical record is Verified Fixed and has a valid manual target-build observation, but no automated regression Test ID, failure-sensitivity evidence, execution receipt, or log.

#### Input

Run close with an otherwise valid `cgs-bug-closure-manifest/v1`.

#### Expected reads

The exact registry, record, event chain, candidate/build authorities, reproduction evidence, closure owner authority, and declared regression fields.

#### Expected writes

None.

#### Expected non-writes

No Closed status, closure event, registry update, invented waiver, automated receipt, or modified manual evidence.

#### Expected behavior

Close returns BLOCKED_EVIDENCE/CANNOT_VERIFY, preserves Verified Fixed, and enumerates the missing automated regression contract. Manual observation remains supporting reproduction evidence only.

#### Assertions

BR-STA-021, BR-STA-022, BR-STA-023, BR-PRO-014.

#### Case Verdict

BLOCKED with no mutation.

### Case 2 — Explicit subcommands reject illegal combinations

#### Fixture

Requests include a free-form description without a mode, analyze with a direct path, verify with a closure manifest, duplicate flags, and status with an unsafe Bug ID.

#### Input

Parse each request.

#### Expected reads

Invocation grammar only.

#### Expected writes

None.

#### Expected non-writes

No source scan, manifest read, Bug ID allocation, record mutation, or evidence execution.

#### Expected behavior

Each request returns BLOCKED_INPUT before business evaluation and identifies the exact grammar violation. No business lifecycle result is fabricated.

#### Assertions

BR-STA-002, BR-STA-003, BR-PRO-001.

#### Case Verdict

PASS only if all illegal requests are rejected deterministically.

### Case 3 — Missing critical fields remains a conversation-only draft

#### Fixture

A draft request supplies a title but omits build identity, system, platform/configuration, repro steps, expected result, actual result, and confirmed severity.

#### Input

Run draft with the exact request manifest and revision.

#### Expected reads

Only the draft request and any explicitly referenced evidence.

#### Expected writes

None.

#### Expected non-writes

No registry lock, Bug ID, canonical record, draft file, creation event, or COMPLETE/BUG_CREATED result.

#### Expected behavior

Fields are classified as required/optional/unknown. All missing required fields are listed in at most three coherent question groups. Result is DRAFT_INCOMPLETE and Record Status NOT_CREATED.

#### Assertions

BR-STA-004, BR-STA-005, BR-PRO-003.

#### Case Verdict

DRAFT_INCOMPLETE with zero writes.

### Case 4 — Duplicate candidate needs a human decision and preserves occurrence

#### Fixture

The new complete draft shares a primary stable business key with existing BUG-000042 but differs in build, device, and evidence. No duplicate decision is present.

#### Input

Run create first without a decision, then with an authorized LINK_OCCURRENCE decision.

#### Expected reads

The exact registry preimage, existing bug record/revision, draft payload, candidate/build/evidence authorities, and decision owner authority.

#### Expected writes

First run writes nothing. The authorized second run writes one absent occurrence receipt and the CAS-updated registry occurrence-set revision.

#### Expected non-writes

No silent merge, new Bug ID, overwrite of BUG-000042, changed original observation, status transition, or discarded evidence.

#### Expected behavior

The first result is DUPLICATE_DECISION_REQUIRED. The second links an independently identified occurrence with its own build/repro/evidence identity.

#### Assertions

BR-STA-006, BR-STA-007, BR-PRO-004.

#### Case Verdict

PASS when only the human-confirmed occurrence link is persisted.

### Case 5 — Concurrent allocation and idempotent rerun cannot collide

#### Fixture

Two creation manifests name the same registry revision with different idempotency keys. A third reruns the first request with identical bytes.

#### Input

Attempt both allocations concurrently, then rerun the winning request.

#### Expected reads

Registry preimage/revision, lock state, draft revisions, decision authorities, and target absence.

#### Expected writes

Exactly one winning all-or-none registry/record/creation-event transaction. The loser writes nothing. The identical rerun writes nothing.

#### Expected non-writes

No duplicate Bug ID, partial registry/record state, hidden retry ID, overwritten event, or second record for the same idempotency key.

#### Expected behavior

One allocator obtains the lock and read-back verifies. The loser returns RETRYABLE_CONFLICT. The rerun returns the original Bug ID as NO_CHANGE.

#### Assertions

BR-STA-008, BR-STA-009, BR-PRO-005, BR-PRO-006.

#### Case Verdict

PASS when uniqueness and idempotency both hold.

### Case 6 — Static analyze is bounded and yields candidates only

#### Fixture

An analysis manifest names two project files and revisions with small budgets. One source suggests a null dereference, but no target-build reproduction exists. A third undeclared file appears related.

#### Input

Run analyze.

#### Expected reads

Only the two declared files within file/byte/finding budgets.

#### Expected writes

None.

#### Expected non-writes

No third-file scan, repository glob, canonical bug, severity assignment, occurrence, runtime result, or recommended fix stated as fact.

#### Expected behavior

The workflow emits a stable candidate finding with observed source fact, labeled inference, confidence/basis, reproduction hypothesis, false-positive conditions, and owner. Record Status remains NOT_CREATED.

#### Assertions

BR-STA-010, BR-STA-011, BR-PRO-007.

#### Case Verdict

CANDIDATE_FINDINGS only.

### Case 7 — Verify uses exact runner and fails closed on timeout or old logs

#### Fixture

A verification manifest pins one Test ID and argv row. Variant A offers a PASS log from an older build. Variant B runs the pinned row but times out with partial output. Variant C offers a current complete receipt.

#### Input

Evaluate all three variants.

#### Expected reads

Exact bug/fix/candidate/build/repro/test/failure-sensitivity authorities, execution manifest, runner identity, receipts, logs, and revisions.

#### Expected writes

None for A/B. C may propose a transition only if both reproduction and automated regression evidence conclusively pass.

#### Expected non-writes

No synthesized command, test-name discovery, arbitrary suite, old-log reuse, partial PASS, changed retry controls, or unbounded output.

#### Expected behavior

A is STALE/CANNOT_VERIFY. B terminates the full process tree, preserves bounded partial records, and returns PARTIAL/CANNOT_VERIFY. C preserves argv/cwd/deadlines/exit/parser/log provenance.

#### Assertions

BR-STA-012, BR-STA-013, BR-STA-014, BR-PRO-008, BR-PRO-009, BR-PRO-010.

#### Case Verdict

Only current complete exact evidence can proceed to verification.

### Case 8 — Severity vocabulary is canonical and priority remains separate

#### Fixture

Four valid reports use S1-Critical through S4-Trivial. Two invalid drafts use HIGH and MEDIUM and ask the workflow to assign priority.

#### Input

Validate severity and priority fields.

#### Expected reads

The exact draft/creation manifest and any cited authorized triage reference.

#### Expected writes

None for invalid drafts.

#### Expected non-writes

No legacy severity conversion, inferred priority, scheduling change, triage edit, or record with an invalid enum.

#### Expected behavior

Canonical severities pass. HIGH/MEDIUM block for reporter confirmation. Priority remains UNASSIGNED unless a pre-existing owner decision is merely referenced.

#### Assertions

BR-STA-015, BR-STA-016, BR-PRO-011, BR-PRO-012.

#### Case Verdict

PASS when severity and priority ownership remain distinct.

### Case 9 — Static fix presence remains runtime unverified

#### Fixture

A Fixed Pending Verification record has a source diff that appears to remove the defect, but no current reproduction or regression receipt.

#### Input

Run verify.

#### Expected reads

The exact record/fix/source paths and revisions plus the verification manifest.

#### Expected writes

None.

#### Expected non-writes

No Verified Fixed status, transition event, registry update, runner receipt, or claim that reproduction steps ran.

#### Expected behavior

Static state is FIX PRESENT / RUNTIME UNVERIFIED; operation is CANNOT_VERIFY; record state remains Fixed Pending Verification.

#### Assertions

BR-STA-020, BR-PRO-010.

#### Case Verdict

CANNOT_VERIFY.

### Case 10 — Matching target-build and regression evidence verifies atomically

#### Fixture

A Fixed Pending Verification record binds a fix commit/build/platform/repro case/Test ID. Both exact current receipts are complete PASS, and failure-sensitivity evidence verifies.

#### Input

Run verify with an authorized QA verifier.

#### Expected reads

Registry/record/event preimages; exact fix, candidate/build, repro, test source, execution manifest, runner/log receipts, and verifier authority.

#### Expected writes

One immutable verification event, CAS-updated record projection, and CAS-updated registry row, all-or-none.

#### Expected non-writes

No triage/sprint/test/source edit, second event, partial state, priority change, or closure event.

#### Expected behavior

All revisions and bindings revalidate; the event chain advances; status becomes Verified Fixed only after atomic publish and read-back.

#### Assertions

BR-STA-019, BR-STA-021, BR-STA-024.

#### Case Verdict

VERIFIED_FIXED with Persistence WRITTEN.

### Case 11 — Conclusive defect evidence reopens; partial evidence does not

#### Fixture

Variant A has a current complete reproduction FAIL demonstrating the original defect. Variant B has a regression RUNNER_ERROR and truncated log.

#### Input

Run verify for both.

#### Expected reads

The same exact verification authority set and receipts.

#### Expected writes

A may atomically create the reopen event and update record/registry. B writes nothing.

#### Expected non-writes

No Verified Fixed or Closed state, no discarded failure receipt, no mutation from runner error, and no partial transition.

#### Expected behavior

A returns STILL_PRESENT and transitions to Open with retained evidence. B returns CANNOT_VERIFY and preserves Fixed Pending Verification.

#### Assertions

BR-STA-014, BR-STA-019, BR-PRO-010.

#### Case Verdict

PASS when conclusive failure and infrastructure uncertainty remain distinct.

### Case 12 — Illegal lifecycle transitions are rejected

#### Fixture

Requests attempt Open→Verified Fixed, Reopened→Closed, Fixed Pending
Verification→Closed, Closed→Open, hotfix-authored registry mutation, and verify
without the canonical recorder's fix-candidate transition.

#### Input

Run the requested verify or close operation.

#### Expected reads

The exact registry, record, event chain, operation manifest, and owner/evidence authority.

#### Expected writes

None.

#### Expected non-writes

No status patch, event, registry update, evidence insertion, or owner impersonation.

#### Expected behavior

Each request identifies the required current state, transition owner, and missing evidence. Closed remains terminal.

#### Assertions

BR-STA-019, BR-PRO-013.

#### Case Verdict

BLOCKED with unchanged bytes.

### Case 13 — Close consumes current verified automated evidence

#### Fixture

A Verified Fixed record has a valid revision chain, current reproduction PASS, automated regression PASS, failure-sensitivity proof, exact build/fix/Test ID binding, and authorized QA closure owner.

#### Input

Run close.

#### Expected reads

Registry/record/event chain, candidate/build/fix, reproduction, execution manifest, regression receipt/log, sensitivity evidence, and closure authority.

#### Expected writes

One immutable closure event, CAS-updated Closed record, and CAS-updated registry row, all-or-none.

#### Expected non-writes

No manual-only regression field, waiver, triage edit, source/test edit, partial close, or outgoing event after closure.

#### Expected behavior

All evidence is re-read, closure fields are complete, event chain advances, and read-back verifies Closed.

#### Assertions

BR-STA-022, BR-STA-023, BR-STA-024, BR-PRO-014.

#### Case Verdict

BUG_CLOSED only after verified atomic persistence.

### Case 14 — Registry or record drift aborts mutation

#### Fixture

A valid create or transition preview is authorized, then another actor changes the registry revision or record bytes before CAS.

#### Input

Attempt publication.

#### Expected reads

Every preimage authority again, target absence, lock state, staged bytes, and internal references.

#### Expected writes

Private same-filesystem staging only; no final mutation after drift detection.

#### Expected non-writes

No overwritten registry, stale record projection, orphan event, partial occurrence, rollback, or hidden new ID.

#### Expected behavior

CAS fails with RETRYABLE_CONFLICT, preserves the evaluated business result separately from Persistence, and requires a refreshed manifest/preimage.

#### Assertions

BR-STA-008, BR-STA-024, BR-PRO-005, BR-PRO-006.

#### Case Verdict

CONFLICT with canonical bytes unchanged.

### Case 15 — Registered spec is complete and contract-aligned

#### Fixture

The P1 candidate skill, metadata, and registered spec.

#### Input

Run static contract validation.

#### Expected reads

Exactly the three candidate files.

#### Expected writes

None.

#### Expected non-writes

No live skill, old P0 staging, shared catalog, production record, registry, test, or source modification.

#### Expected behavior

The spec uses `cgs-skill-spec/v2`; Cases 1 through 17 are contiguous and each contains Fixture, Input, Expected reads, Expected writes, Expected non-writes, Expected behavior, Assertions, and Case Verdict. Invocation, schemas, severity, write sets, evidence gates, and result vocabulary match the skill.

#### Assertions

BR-STA-001 through BR-STA-028; BR-PRO-001 through BR-PRO-020.

#### Case Verdict

PASS only when structure and behavioral contracts are fully aligned.

### Case 16 — Complete new bug creation happy path

#### Fixture

A DRAFT_READY report has all required observed fields, exact evidence, confirmed S2-Major severity, no confirmed duplicate, authorized CREATE_NEW decision, unused idempotency key, current registry preimage, and absent targets.

#### Input

Run create.

#### Expected reads

The exact creation manifest, draft payload, candidate/build/evidence authorities, registry, duplicate candidates, and decision authority.

#### Expected writes

One updated registry, one Open canonical record, and one immutable creation event in an all-or-none transaction.

#### Expected non-writes

No legacy path, priority assignment, source/test/triage/sprint edit, extra occurrence, duplicate record, or unbounded artifact.

#### Expected behavior

The workflow locks and revalidates the registry, allocates the next six-digit Bug ID, writes observed and inferred sections separately, publishes atomically, reads back, and returns exact paths/revisions with BUG_CREATED.

#### Assertions

BR-STA-001 through BR-STA-028; BR-PRO-001 through BR-PRO-020.

#### Case Verdict

BUG_CREATED only after complete CAS/read-back verification.

### Case 17 — Canonical recorder accepts an exact hotfix Fix Candidate only

#### Fixture

Variant A has an Open canonical record and one current immutable
`cgs-hotfix-bug-candidate-link/v1` whose Bug ID/path/revision/status, fix full
commit/tree, candidate/build/artifact/platform, build receipts, regression Test
IDs/execution/logs, smoke, HOTFIX READY assessment, and rollback identities all
join, plus current bug-owner authority and absent event/receipt targets. Variant
B lets hotfix propose direct registry bytes. Variant C changes the build receipt
after link creation. Variant D asks to write Verified Fixed directly.

#### Input

Run `record-fix-candidate` independently for each exact record manifest.

#### Expected reads

Record manifest, candidate link, canonical registry/record/prior event, owner
authority, and every exact commit/candidate/build/test/smoke/assessment/rollback
artifact named by the link.

#### Expected writes

Only A atomically writes one Fixed Pending Verification event, updated bug
record, updated registry row, and immutable recorder receipt.

#### Expected non-writes

Hotfix artifacts, source/tests/builds, QA verification evidence, Verified Fixed,
Closed, release, and deployment state remain unchanged.

#### Expected behavior

A re-reads all joins, validates owner authority, locks/CASes canonical preimages,
publishes all four members, verifies read-back, and returns
FIX_CANDIDATE_RECORDED. B through D block with zero lifecycle advance.

#### Assertions

BR-STA-002, BR-STA-019, BR-STA-024 through BR-STA-028; BR-PRO-013,
BR-PRO-015 through BR-PRO-020.

#### Case Verdict

PASS only if A reaches Fixed Pending Verification through the canonical recorder
and every authority, drift, or illegal-terminal variant preserves prior bytes.


## P1 audit remediation trace

| Audit ID | SKILL clause | Case/assertion binding | Fail-closed observation |
|---|---|---|---|
| BR-005 | Explicit grammar | Case 2 / BR-STA-002, BR-STA-003, BR-PRO-001 | Illegal/ambiguous combinations perform zero business work |
| BR-006 | Phase 1 | Case 3 / BR-STA-004, BR-STA-005, BR-PRO-003 | Missing critical fields cannot create a complete record |
| BR-007 | Phase 3 | Case 4 / BR-STA-006, BR-STA-007, BR-PRO-004 | Duplicate candidates never auto-merge/discard occurrences |
| BR-008 | Phase 4 | Case 5 / BR-STA-008, BR-STA-009, BR-PRO-005, BR-PRO-006 | Collision/CAS conflict cannot allocate a hidden new ID |
| BR-009 | Phases 0/2 | Case 6 / BR-STA-010, BR-STA-011, BR-PRO-007 | Static inference cannot become an observed runtime bug |
| BR-010 | Phases 6–8 | Case 7 / BR-STA-012–014, BR-PRO-008–010 | Timeout/old log/runner/parser/partial evidence cannot verify |
| BR-011 | Artifact contract/Phase 1 | Case 8 / BR-STA-015, BR-STA-016, BR-PRO-011, BR-PRO-012 | Legacy textual severity and priority inference are rejected |
| BR-012 | Phase 0 | Case 2 / BR-STA-003, BR-STA-017, BR-STA-018, BR-PRO-001, BR-PRO-002 | Malformed/ambiguous/noncanonical/out-of-root/unreadable input yields zero write |
