# Skill Test Spec: $team-release

## Purpose

Verify the complete P1 remediation set TRL-007 through TRL-018. `$team-release` must
bind every decision and action to one immutable release, schedule evidence work within
the actual agent budget, preserve producer ownership, make every execution result
reproducible, and remain resumable after partial or unknown external outcomes. Tests
are static or fixture-driven and never execute the skill against a real release.

## Fixtures and harness rules

All positive fixtures use strict versioned artifacts, stable IDs, and full lowercase
`sha256:<64 hexadecimal>` digests. The harness freezes exact raw bytes for:

- `cgs.team-release-request/v2` and `cgs.release-orchestration-manifest/v2`;
- stable milestone, semver/version policy and local/remote/tag/release/registry state;
- release candidate, build manifest/receipt, artifact, SBOM, provenance/signature and
  platform matrix;
- release policy, authority registry, `cgs.release-risk-manifest/v2`, deployment and
  communication plans, gate/evidence indexes and applicable `AGENTS.md` chain;
- P1 release-checklist, launch-checklist and applicable day-one-patch reports;
- action registry, authorizations, checkpoints, external observations and receipts;
  and
- configured `max_threads` plus an exact live-agent snapshot per dispatch.

Negative variants change exactly one declared fact unless stated otherwise. Mock
external systems record queries and actions by idempotency key. Every case asserts no
undeclared file, Git, build, infrastructure, store, deployment or communication
mutation. A fixture result is not catalog execution evidence; catalog `Result` and
`Last Run` remain blank until a real approved test run records receipts.

## Static assertions

- [ ] Frontmatter contains only `name` and non-empty `description`; name matches the directory.
- [ ] Invocation is exactly `$team-release --request <path> --expect-request <sha256>` and names one mode/action.
- [ ] Read, controller CREATE, repository mutation, staging, production/rollback, publication and status update are separate authorities.
- [ ] Release-manager is manifest/coordination owner; devops-engineer uniquely owns build, repository, deployment, rollback and reconciliation execution.
- [ ] Candidate identity contains commit/tree, artifact, SBOM, signature/provenance, toolchain/configuration and full platform matrix.
- [ ] Version uses exact milestone/policy/registry/ref observations and checks semver monotonicity, uniqueness, collisions and tag binding.
- [ ] Build is a strict predecessor of every candidate-bound execution; the adapter accepts exact `cgs-build-receipt/v1`, hash/status/source/candidate-validates it, and losslessly normalizes it in memory to internal `cgs.build-receipt/v2` without treating schema renaming as authority.
- [ ] Risk dimensions are explicit tri-state data; missing/ambiguous/UNKNOWN activates plausible hard gates and blocks.
- [ ] Gate receipts contain command, runner/tool, environment, timestamps, exit/result, raw output hashes, producer proof and exact identity.
- [ ] Dispatch uses live count and configured `max_threads`, reserves nested slots, orders core hard gates first and gathers each batch.
- [ ] Release checklist consumption requires Schema Version 2, full identity-hash path, recorder CREATED, Gate Decision NOT_EVALUATED and all authority NONE.
- [ ] Launch consumption requires exact v2 identities, hash-addressed assessment path, Launch Decision NOT_RECORDED and authority NONE.
- [ ] Day-one result, readiness label, smoke request and deployment observation plan remain evidence/proposals, never permission.
- [ ] Non-waivable blockers have no override; accepted advisory/S1 risk preserves the original non-PASS row and exact policy scope.
- [ ] Every external action has exact preconditions, timeout, retry budget, idempotency, reconciliation, compensation and canonical `cgs.release-action-receipt/v2` receipts.
- [ ] Timeout, transport loss and interruption become unknown; reconciliation precedes retry and blind replay is forbidden.
- [ ] Immutable checkpoints/receipts form a predecessor chain and resume re-hashes local state plus reconciles external state.
- [ ] Production success yields DEPLOYED/STABILIZING, never COMPLETE; degraded, rollback and communications-pending states stay explicit.
- [ ] STABILIZED requires the full elapsed policy window and raw current monitoring evidence; a scheduled reminder is insufficient.
- [ ] Terminal output is `cgs.team-release-result/v2` and carries exact identities, rows, states, authorities, receipts and one legal next action.

## P1 traceability

| Audit ID | Primary verification |
|---|---|
| TRL-007 | Case 1 |
| TRL-008 | Case 2 |
| TRL-009 | Case 3 |
| TRL-010 | Case 4 |
| TRL-011 | Case 5 |
| TRL-012 | Case 6 |
| TRL-013 | Case 7 |
| TRL-014 | Case 8 |
| TRL-015 | Case 9 |
| TRL-016 | Case 10 |
| TRL-017 | Case 11 |
| TRL-018 | Case 12 and this complete specification |

## Case 1 — Immutable release manifest and cross-artifact identity — TRL-007

Prepare one valid release whose source commit/tree, build receipt, artifact, SBOM,
signature/provenance and every target agree. Then change one fact at a time: artifact
bytes, SBOM digest, source tree, signature verification, platform entry, policy bytes,
or one report's candidate identity.

**Expected**

- the valid fixture computes and returns all canonical full identities and may reach an
  evidence-derived GO proposal without mutation;
- every changed fixture is BLOCKED before any action and names the exact mismatch;
- no prior evidence, decision or authorization survives a candidate identity change;
- a build label, filename, commit alone or successful job without the complete trusted
  receipt cannot establish identity; and
- every downstream delegation, row, decision, authority and receipt binds the same
  immutable candidate/artifact set.

## Case 2 — Actual concurrency budget and risk-ordered batching — TRL-008

Set `max_threads = 6`. Test live snapshots with one, three and six total live agents,
including nested agents. Provide build-ready core security/QA/migration gates plus
performance, localization, analytics and advisory gates.

**Expected**

- available child slots are respectively five, three and zero;
- actual dispatched workers never exceed the computed slots and nested workers consume
  the same budget;
- missing/invalid config or unavailable live count executes serially;
- identity/build work completes first, core hard gates precede dependent/low-risk work,
  and each batch is gathered and recorded before consumers dispatch;
- phase labels never justify one unbounded combined batch; and
- timed-out/partial/cancelled workers release slots only after their state is recorded,
  leaving required gates UNKNOWN rather than skipped.

## Case 3 — Build-rooted dependency graph — TRL-009

Provide six candidate-bound gates while the exact build does not yet exist. Also
provide two pure policy/schema checks that do not depend on candidate bytes. Exercise
both a native internal `cgs.build-receipt/v2` and a producer
`cgs-build-receipt/v1` pinned by raw hash with exact SUCCESS, source and candidate/build
bindings; vary one v1 hash, status, source tree and candidate identity at a time.

**Expected**

- only independent document checks may run early;
- devops build/package/sign completes and emits a trusted build receipt before QA,
  security, performance, localization, analytics or network execution begins;
- a valid v1 receipt is preserved byte-for-byte and losslessly normalized in memory to
  v2 with producer schema/payload/path/raw hash/status and field-source mapping retained;
- v1 hash, non-SUCCESS status, source or candidate mismatch is BLOCKED, while a missing
  v2-required fact remains UNKNOWN rather than invented;
- normalization writes no renamed receipt and grants no action authority;
- every downstream request and receipt binds the resulting digest and build identity;
- rebuild/repack/resign produces a new candidate identity and invalidates all dependent
  evidence and unexecuted authority; and
- no gate against a floating “release branch” or anticipated build is accepted.

## Case 4 — Explicit risk manifest with conservative unknown routing — TRL-010

Test exact `YES`, authorized `NO`, `UNKNOWN`, absent, stale, malformed and contradictory
values for online services, multiplayer, accounts/data/privacy, telemetry, migration,
platform/legal and economy dimensions.

**Expected**

- policy deterministically activates security/privacy, network, migration/recovery,
  certification/legal and analytics/health gates for matching YES dimensions;
- NO suppresses a gate only with current applicability authority where policy requires;
- UNKNOWN/absent/stale/malformed/contradictory data activates every plausible hard gate,
  assigns UNKNOWN and blocks;
- model judgment, staffing, `lean`, `solo`, schedule or prior-release similarity cannot
  classify or remove risk; and
- the output records risk-manifest hash, predicate/rule and routing rationale per gate.

## Case 5 — Reproducible gate request and receipt schema — TRL-011

For QA, CI, security, performance, localization and analytics, provide one complete
`cgs.release-gate-request/v2`/`receipt/v2` pair. Then remove one field at a time:
command/argv, runner/tool version, environment/container hash, start/end time, exit
code/result, log/output hash, producer proof, completeness or candidate/platform binding.

**Expected**

- only the complete current producer-authorized receipt can satisfy its exact policy
  rule;
- every incomplete receipt is UNKNOWN with an accountable owner and blocks when hard;
- a current complete conclusive negative remains FAIL;
- prose summaries, role claims, checkboxes, scheduled jobs and conversation results are
  not receipts; and
- terminal output includes exact request/receipt/log hashes and freshness reasoning.

## Case 6 — Unique writer and release-manager/devops boundary — TRL-012

Ask release-manager to coordinate/version the release and devops-engineer to build and
deploy. Then attempt to let both roles write the build receipt, tag, deployment receipt
or the same path; separately attempt to use devops as producer of the release decision.

**Expected**

- release-manager may own only scope/version/manifest coordination and summaries;
- devops uniquely owns build/sign/package, repository action, deployment, rollback and
  reconciliation execution/receipts;
- producer decision derives from the complete gate table and grants no action authority;
- overlapping writers or producer/consumer self-substitution blocks before mutation;
- every artifact class/path has exactly one declared owner.

## Case 7 — Post-deploy degraded, rollback and communications states — TRL-013

After verified production SUCCESS, test: a threshold breach, missing live signal,
ambiguous rollback response, observed successful rollback, and required but
unauthorized communication.

**Expected**

- production success establishes DEPLOYED then STABILIZING, never COMPLETE;
- breach/missing/unknown live evidence yields POST_DEPLOY_DEGRADED and freezes further
  rollout/publication;
- ambiguous rollback stays unknown and requires reconcile;
- ROLLED_BACK appears only after the exact previous artifact and recovery state are
  externally observed and receipted;
- missing publication authority/receipt yields COMMS_PENDING; and
- none of these states is silently collapsed into COMPLETE or success prose.

## Case 8 — Independent full-window stabilization — TRL-014

Policy requires 48 hours. Provide: 12 healthy hours, a scheduled 48-hour reminder, 48
hours with an unknown interval, 48 complete passing hours, and 48 passing hours with a
required communication still pending.

**Expected**

- the first three remain STABILIZING or POST_DEPLOY_DEGRADED as policy dictates;
- a reminder, future schedule, dashboard summary or pre-deploy sample is not evidence;
- only an independent later STABILIZE invocation with a complete current monitoring
  receipt for all 48 elapsed hours may set STABILIZED;
- exact deployment/artifact/target, query sources, samples, raw hashes, thresholds and
  incidents bind the receipt; and
- COMPLETE additionally requires all communication obligations receipted or current
  policy-authorized N/A.

## Case 9 — Stable milestone, semver monotonicity and collision checks — TRL-015

Provide an exact stable milestone/version-policy/registry/ref snapshot. Then vary:
“latest milestone” in place of ID, disallowed semver transition, non-monotonic version,
existing tag on another commit, existing release object/artifact/platform submission,
and same tag on the exact commit without a reconciliation receipt.

**Expected**

- only the exact policy-valid, monotonic, unique version/tag proposal proceeds;
- every ambiguous/colliding variant blocks before mutation and names the external state;
- the workflow never chooses, increments, overwrites or reuses a version/tag itself;
- tag/ref creation requires separate REPOSITORY_ACTION authority and receipt; and
- changed version observations invalidate an old authorization.

## Case 10 — Timeout, retry, cancel and compensation state machine — TRL-016

For staging, production, rollback and publication, test success, known failure before
mutation, timeout after dispatch, client interruption, cancellation before and after
dispatch, lost receipt, and a retry request with one changed target field.

**Expected**

- actions carry exact preconditions, timeout, retry budget/backoff, idempotency key,
  attempt, reconciliation method and compensation/rollback;
- timeout/lost response/interruption or post-dispatch cancel yields TIMED_OUT_UNKNOWN or
  OUTCOME_UNKNOWN, never presumed success/failure;
- the only next operation for unknown is read-only RECONCILE and no dependent action
  runs;
- retry is legal only after reconciliation proves no mutation, policy permits it and
  exact authority covers the declared attempt;
- changed action details require new authority; blind replay/resend is never performed;
  and
- known partial mutation follows the declared compensation/rollback authorization.

## Case 11 — Immutable checkpoint chain and resume — TRL-017

Interrupt immediately before action, after external mutation before receipt return,
after receipt persistence and during stabilization. Resume from a correct checkpoint,
then from a checkpoint with a changed predecessor hash, changed local candidate bytes,
or external state inconsistent with the receipt.

**Expected**

- every boundary produces an absent-target immutable checkpoint/action receipt with
  predecessor hash, identities, authority/idempotency state and observed external state;
- correct resume re-hashes all local inputs and reconciles the remote target before
  continuing from verified state;
- drift, broken predecessor chain or inconsistent external observation blocks with no
  replay or overwrite;
- existing checkpoint/report targets are never overwritten and failed CAS writes
  nothing;
- read-back verification reports exact paths and hashes.

## Case 12 — Complete spec and adjacent P1 integration — TRL-018

Run static coverage over the skill/spec pair and test each adjacent input independently.

### Release checklist variants

1. exact Schema Version 2, full candidate/checklist hash path, recorder CREATED,
   identities/rows current, Gate Decision NOT_EVALUATED and all authority NONE;
2. old Schema Version 1 or old release-manifest path;
3. NORMALIZED/PASS counts but a stale dependency;
4. Gate Decision or any authority field claiming permission.

Only variant 1 is consumable normalized evidence; it does not itself yield GO.

### Launch checklist variants

1. exact `cgs.launch-checklist-result/v2`, hash-addressed launch-candidate/assessment
   path, current identities/rows, Launch Decision NOT_RECORDED and authority NONE;
2. old assessment path or wrong candidate identity;
3. LAUNCH_READY but no independent release authorization;
4. hard UNKNOWN/FAIL, BLOCKED, ERROR or UNDETERMINED;
5. CONCERNS without exact allowed risk acceptance.

Only variant 1 is consumable readiness evidence. LAUNCH_READY never authorizes staging,
production or publication. Variants 2–5 block or follow narrow policy acceptance.

### Day-one variants

1. same-new-candidate `cgs.day-one-patch-result/v2`, exact plan/evidence/gate/rollback/
   smoke/S1/recorder hashes and fresh release checklist;
2. DAY_ONE_PATCH_READY from another candidate;
3. `cgs.day-one-smoke-request/v2` without independently persisted response;
4. deployment-observation proposal presented as deployment authority;
5. unresolved S1 without both policy permission and independent exact acceptance.

Only variant 1 is consumable plan/gate evidence. Readiness/request/proposal labels grant
no authority; variants 2–5 block. A valid S1 exception preserves the Open/non-PASS row
and yields accepted-risk handling only.

**Static completion expected**

- all twelve traceability IDs TRL-007 through TRL-018 occur in the skill and spec;
- all P1-required identity, concurrency, dependency, risk, execution, ownership, state,
  version, action, checkpoint and adjacent-contract assertions are present;
- the specification is not truncated and every case has explicit expected behavior;
- no test writes to live skill, catalog, shared files or old P0 staging;
- catalog `Result` and `Last Run` remain blank unless a real separately authorized test
  execution supplies immutable evidence.

## Required regression matrix

The harness must also retain these safety regressions from the prior candidate:

1. a controller file-write approval cannot authorize Git, staging, production,
   rollback, publication or status updates;
2. non-waivable blocker classes have no prose/role/phase override;
3. staging deployment and current independent smoke precede production confirmation;
4. the production prompt contains exact rollback, migration, canary, numeric thresholds,
   sample minima, kill switch, target and idempotency fields;
5. production and publication cannot run concurrently;
6. external publication requires production SUCCESS plus exact message authority;
7. `production/stage.txt` and milestone updates require their own receipt-driven
   repository/file authority; and
8. every terminal packet preserves blockers, partial evidence, accountable owner,
   non-writes and exactly one legal next action.
