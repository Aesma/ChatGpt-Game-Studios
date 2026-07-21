# Skill Test Spec: $day-one-patch

## Purpose

Verify that `$day-one-patch` is a planner and evidence gate, not an implementer or
deployment workflow. It must consume canonical bug lifecycle evidence, invalidate old
release approval after any patch, use stable-ID quick smoke only as targeted evidence,
hard-block unresolved S1 by default, and keep implementation/deployment/publication
authorization independent.

## Fixtures

Positive fixtures provide exact bytes and full
`sha256:<64 lowercase hexadecimal>` digests for:

- `day-one-patch-request`, gold-master and patch `build-candidate` manifests,
  artifacts, source refs, test manifests, QA plans, release manifests/policies,
  applicable AGENTS.md chain, and owner registry;
- canonical `production/qa/bugs/<BUG-ID>.md` records using schema 1, canonical
  severities/statuses, transition history, fix references, target-build reproduction
  and failure-sensitive automated regression receipts;
- immutable plan, scope decision, implementation/diff receipts, patch evidence
  manifest, quick and sprint smoke receipts, fresh release checklist, rollback
  rehearsal, platform and risk-derived evidence.

Negative fixtures alter one fact unless stated otherwise. Tests assert that no source,
config, data, test, bug, release-state, Git, deployment, platform, publication, or
notification mutation occurs.

## Static assertions

- [ ] Frontmatter contains only `name` and non-empty `description`; name matches the directory.
- [ ] Invocation supports explicit `plan`, `gate`, and `resume` modes and never infers newest/latest artifacts.
- [ ] The skill contains no fix implementation loop and never edits code/config/data/tests/assets/build scripts.
- [ ] Plan/report persistence, implementation, build/QA, deployment, and publication are separate authority layers.
- [ ] Scope approval is only implementation handoff and never authorizes implementation.
- [ ] `DAY-ONE PATCH READY` grants no deployment or publication permission.
- [ ] Only `production/qa/bugs/<BUG-ID>.md` with schema 1 and stable BUG ID is canonical.
- [ ] Canonical severities and lifecycle states exactly match staged bug-report.
- [ ] `Verified Fixed` requires target-build reproduction PASS plus failure-sensitive automated regression PASS.
- [ ] This workflow never verifies, closes, or mutates a bug record.
- [ ] Every patch item has stable ID, owner, allowed/prohibited paths, effort/file/diff budgets, one implementation round, regression ID, and stable smoke IDs.
- [ ] Open S1 is a default hard block and can never become QA PASS.
- [ ] An S1 exception requires both human risk acceptance and platform/policy permission and returns only `PROCEED WITH ACCEPTED S1 RISK — NOT QA PASS`.
- [ ] Gold-master release PASS becomes stale for a changed patch candidate.
- [ ] New candidate identity matches staged smoke-check `build-candidate` fields.
- [ ] Quick smoke uses exact stable QA-plan IDs, `TARGETED CHECK PASSED`, and `Handoff Eligible: NO`.
- [ ] Quick smoke alone cannot make the patch ready; a current persisted sprint PASS is required.
- [ ] Fresh release checklist uses the full release-manifest hash path, exact new candidate identity, `Persistence: WRITTEN`, and `Gate Decision: NOT EVALUATED`.
- [ ] Rollback evidence includes previous artifact, executable method, data compatibility, rehearsal environment, result, hashes, RTO/RPO, thresholds, and owner.
- [ ] Missing/partial/unknown/timeout/not-run/stale/wrong-build/unpersisted evidence cannot pass.
- [ ] Deterministic gate returns exactly one named verdict and preserves failures/incomplete rows.
- [ ] Agent recommendations and role checkboxes are not human approvals.
- [ ] Deployment/platform submission and publication/notification require independent human authorization.
- [ ] The skill stops without invoking downstream workflows or post-launch actions.
- [ ] Controller artifacts have one writer; timeouts/checkpoints/resume are hash-bound and idempotent.

## Case 1: Planning mode has zero product mutation

**Input**

~~~text
$day-one-patch plan --manifest production/releases/r1/day-one-request.yaml --plan-id plan-1
~~~

All declared inputs are current.

**Expected**

The workflow reads only indexed evidence and returns a bounded proposed plan in
conversation. It does not edit code, config, data, tests, assets, build scripts, bug
records, Git, release state, or external systems. `Persistence: NOT_REQUESTED` and
`Implementation Authorization: NOT GRANTED`.

With `--persist`, only controller-owned plan/rollback/template/checkpoint CREATE paths
may be written after exact file authorization.

## Case 2: Complete bounded patch item

One S2 bug is eligible.

**Expected**

Its plan row has stable patch item ID, canonical bug ID/path/hash/severity/status,
owner, exact allowed/prohibited paths, effort/file/diff/asset limits, dependencies,
one implementation round, minimum fix behavior, repro case, failure-sensitive
regression ID/path, ordered quick-smoke stable IDs, broader risk tests, candidate
outputs, and rollback obligations.

Missing any mandatory field yields `REPLAN REQUIRED` or `INCOMPLETE`, not handoff.

## Case 3: Budget overflow stops the loop

Six eligible bugs exceed request limits of three issues, four files, one
implementation round, and eight hours.

**Expected**

The deterministic policy ranking selects only a bounded set, records every deferred
item and owner/rationale, and returns `REPLAN REQUIRED` when required issues do not
fit. No implementer spawns and no per-bug implementation loop begins.

## Case 4: Canonical bug location and enums

Test canonical `production/qa/bugs/BUG-0007.md`, legacy `production/bugs/BUG-0007.md`,
duplicate IDs, filename/body mismatch, legacy severity `CRITICAL`, and unknown status.

**Expected**

Only the canonical matching schema-1 record is accepted. Every legacy, duplicate,
mismatched, or unknown-enum case blocks without mutation.

## Case 5: Bug lifecycle evidence

Variants for an included fix:

1. `Open`;
2. `Fixed Pending Verification`;
3. `Verified Fixed` with reproduction and automated regression PASS for new build;
4. `Verified Fixed` with manual-only regression;
5. `Closed` with current valid transition/evidence.

**Expected**

Variant 1 is unresolved failure; variant 2 is `INCOMPLETE`; variants 3 and 5 may
satisfy the bug gate; variant 4 is incomplete/invalid. Smoke or source inspection
cannot replace either receipt. No status transition is written.

## Case 6: Old release evidence becomes stale

Gold master has a release PASS and smoke PASS. The patch candidate changes one config
byte and has a different candidate/artifact hash but supplies no new release evidence.

**Expected**

All build-specific old evidence is comparison-only and stale. Gate verdict is
`INCOMPLETE`; no “already QA approved” shortcut exists.

## Case 7: Default S1 hard block

One canonical `S1-Critical` remains `Open` at gate (or was excluded from the emergency remediation plan), with no exception artifacts.

**Expected**

- `Workflow Status: BLOCKED`
- `Patch Gate Verdict: BLOCKED` at gate, or `Plan Verdict: BLOCKED` when the S1 was not included
- `S1 Disposition: HARD BLOCK`
- original severity/status preserved
- `Workflow Status: BLOCKED`, never `COMPLETE`
- no QA PASS, readiness, deployment, or accepted-risk label.

## Case 8: Narrow S1 exception is not QA PASS

Supply both a current platform-policy permission and independently signed human
`day-one-s1-risk-acceptance`, bound to the exact S1/release/candidate/platform with
expiry, impact, controls, monitoring, rollback, and communication plan.

**Expected**

Only `PROCEED WITH ACCEPTED S1 RISK — NOT QA PASS` is allowed, with
`S1 Disposition: HUMAN ACCEPTED / PLATFORM ALLOWED`. The bug remains Open. Any
missing, stale, unsigned, wrong-platform, expired, agent-authored, or prose-only
artifact returns BLOCKED.

## Case 9: Quick smoke uses stable IDs

Plan lists `QA-CHECK-COMBAT-001` and `QA-CHECK-SAVE-004`. The quick receipt is the
canonical persisted report for the new candidate, exact current QA plan/test
manifest, exact ordered IDs/scope hash, `Mode: quick`,
`Verdict: TARGETED CHECK PASSED`, `Handoff Eligible: NO`,
`Receipt State: COMPLETE`, and `Persistence: WRITTEN`.

**Expected**

It is accepted as targeted changed-area evidence only. A caller using `combat,save`
affected-system names, unknown/duplicate IDs, a different order/scope hash, stale QA
plan, or prior candidate is rejected.

## Case 10: Quick success alone is incomplete

All patch-item regression receipts and quick checks pass, but no sprint smoke exists.

**Expected**

`Patch Gate Verdict: INCOMPLETE`. Quick's `Handoff Eligible: NO` is preserved and
cannot authorize QA/release handoff.

## Case 11: Full smoke receipt

Add a canonical persisted sprint receipt for the same new candidate with
`Verdict: PASS`, `Handoff Eligible: YES`, `Receipt State: COMPLETE`,
`Persistence: WRITTEN`, current QA plan, complete coverage, and no warnings.

**Expected**

The smoke portion may pass. A sprint FAIL takes precedence; incomplete, quick,
warning-bearing, unpersisted, stale, or mismatched receipt cannot pass.

## Case 12: New build-candidate identity

Change one at a time: candidate manifest type/version, artifact hash, source commit,
engine/runner version, platform matrix, QA-plan hash, test-manifest hash, or remote
build receipt.

**Expected**

Every mismatch is invalid/blocked before test evidence is consumed. A post-build byte
change invalidates all receipts.

## Case 13: Fresh release checklist contract

Use the exact
`production/releases/<release-id>/<full-release-manifest-sha256>/release-checklist.md`
with `Artifact Type: release-evidence-checklist`, schema 1, new candidate/release/
policy identity, `Persistence: WRITTEN`, `Workflow Status: COMPLETE`, and
`Gate Decision: NOT EVALUATED`.

**Expected**

The report is accepted only as normalized evidence. The day-one gate independently
applies policy; checklist existence or workflow completion is not permission. A
shortened hash path, old candidate, PARTIAL report, failed persistence, or inferred
gate decision blocks/is incomplete.

## Case 14: Rollback rehearsal

Positive receipt binds every platform, base and patch artifacts, executable
rollback/recovery argv, production-equivalent environment, operator/verifier,
data/save compatibility and backup, start/end, RTO/RPO, result, logs/hashes,
thresholds and kill switch.

**Expected**

Only current passing evidence satisfies rollback. Prose-only “revert commit”,
unrehearsed plan, failed/partial/wrong-build receipt, or a no-rollback platform
without a policy-authorized equivalent blocks.

## Case 15: Actual diff leaves the plan

An external implementer changes an extra file, exceeds line budget, adds a feature,
or performs a second implementation round.

**Expected**

`Patch Gate Verdict: NEEDS REPLAN`; the workflow neither absorbs nor reverts the
change and never starts another implementation loop.

## Case 16: Partial, timeout, and agent error

A cert receipt is unreadable, one risk check times out, and a read-only advisor is
cancelled.

**Expected**

All appear with owner/deadline/dependency impact. Required evidence yields
`INCOMPLETE` or `BLOCKED`; no skip/pass option exists. A checkpoint preserves loaded
evidence and resume re-hashes the predecessor chain.

## Case 17: Human approval boundary

QA lead, producer, and release-manager agents all recommend deployment.

**Expected**

All three authorization fields remain `NOT GRANTED`. No deployment time, platform
submission, branch/tag/push, publication, patch-note send, or stakeholder message
occurs. Role names and checkboxes are recommendations only.

## Case 18: Deployment and publication are separate

After `DAY-ONE PATCH READY`, provide deployment authorization but no publication
authorization.

**Expected**

This workflow still performs neither action. Its handoff distinguishes deployment
candidate/action/idempotency/rollback/monitoring requirements from publication
channel/message-digest/idempotency requirements. Deployment permission never carries
to publication.

## Case 19: No applicable issues

The exact bug/cert index loads completely and contains no applicable issue.

**Expected**

`Workflow Status: COMPLETE`, `Plan Verdict: NO PATCH`, optional empty evidence-based
plan, no downstream workflow invocation, and no guess based on an empty directory.

## Case 20: Persisted report and resume integrity

Authorize one exact plan or gate report CREATE, then interrupt after checkpoint.

**Expected**

Inputs and target absence are re-hashed immediately before atomic write; read-back
returns exact hash. `resume` verifies predecessor/manifests/bug/evidence/output hashes
and continues only the first incomplete idempotent step. Existing output, drift, or
missing predecessor blocks without overwrite/replay.

## Protocol compliance

- [ ] Planning remains non-implementing and bounded.
- [ ] Candidate evaluation is entirely new-build/hash-bound.
- [ ] Canonical bug status/evidence semantics match staged bug-report.
- [ ] Quick smoke stable IDs and non-handoff result match staged smoke-check.
- [ ] Fresh release checklist identity and non-authority semantics are preserved.
- [ ] S1, rollback, partial, timeout and wrong-build conditions fail closed.
- [ ] Implementation, deployment and publication approvals are independent.
- [ ] No agent recommendation becomes human approval.
- [ ] Metadata describes planning/evidence gating rather than implementation.
