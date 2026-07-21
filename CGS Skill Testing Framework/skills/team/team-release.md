# Skill Test Spec: $team-release

## Purpose

Verify that `$team-release` coordinates one immutable release candidate without
confusing evidence, decisions, file changes, deployment authority, or publication
authority. The workflow must be fail-closed under partial evidence and interruptions,
use unique writers, respect the repository-wide agent cap, and remain resumable from
immutable receipts.

## Fixtures

All positive fixtures use stable IDs and full `sha256:<64 lowercase hexadecimal>`
digests. Each fixture declares exact raw bytes for:

- a `release-orchestration-manifest`;
- `release-candidate-manifest`, `build-candidate`, release policy, risk manifest,
  deployment plan, communication plan, and applicable AGENTS.md chain;
- a staged `$release-checklist` report with
  `Artifact Type: release-evidence-checklist`, `Schema Version: 1`,
  `Persistence: WRITTEN`, exact release/policy/candidate/build identity, and complete
  item rows;
- when applicable, a staged `$launch-checklist` persisted report at
  `production/releases/<release-id>/launch-readiness/<assessment-id>/report.md`,
  with exact launch/candidate identity, `Persistence: VERIFIED`, and
  `Launch Decision: NOT_RECORDED`;
- ordered gate manifest and verifiable producer/signature receipts;
- action registry, writer ledger, rollback artifact, canary plan, thresholds, kill
  switch, and idempotency/reconciliation rules.

Negative fixtures change exactly one fact unless the case says otherwise. Tests must
assert that no undeclared filesystem or external mutation occurs.

## Static assertions

- [ ] Frontmatter contains only `name` and non-empty `description`; name matches the directory.
- [ ] Invocation requires one exact manifest/run artifact and explicit mode; it never infers latest version, milestone, evidence, environment, or action.
- [ ] Read-only, file writes, repository mutation, staging deployment, production deployment, and external communication are separate authority layers.
- [ ] Approval at one layer cannot authorize another layer, target, artifact, retry, or revised message.
- [ ] The workflow contains the strict sequence build -> gates -> decision -> staging deploy -> current staging smoke -> human production confirmation -> production deploy.
- [ ] Production and publication cannot run in parallel; drafts are clearly non-publication.
- [ ] Non-waivable blocker classes exist and have no override path.
- [ ] Accepted risk is restricted to policy-waivable issues and requires owner, approver, expiry, compensating controls, monitoring, and rollback.
- [ ] A risk acceptance preserves the original finding and yields only `GO WITH ACCEPTED RISK`.
- [ ] Rollback artifact, migration reversibility, canary percentages/holds, numeric health thresholds, monitoring sources, and kill switch are mandatory before production confirmation.
- [ ] Every required sign-off has producer, artifact type/schema/path/hash, candidate binding, state, and policy class.
- [ ] Required technical-director evidence is explicitly read or dispatched; it cannot be collected from an unspawned role.
- [ ] Missing, timeout, partial, stale, invalid, or unknown required evidence blocks; no generic skip option exists.
- [ ] The staged release checklist is treated as evidence normalization with `Gate Decision: NOT EVALUATED`, not as release permission.
- [ ] A staged launch `LAUNCH_READY` report remains evidence with `Launch Decision: NOT_RECORDED`, not deployment permission.
- [ ] Build/candidate identity includes commit, artifact digest, SBOM, signature/provenance, engine/toolchain, platform/configuration, and stable version tag.
- [ ] The risk manifest deterministically requires security/privacy/network/migration/platform gates; unknown risk is conservative high risk.
- [ ] Build production completes before build-bound QA/performance/analytics delegates start.
- [ ] Exactly one role owns each output class; delegates cannot share or overwrite output paths.
- [ ] Concurrency calculation counts the root and all nested agents. With `max_threads = 6`, no more than five child agents run when the root is the only active thread.
- [ ] External action receipts include action ID, idempotency key, authorization digest, exact target/artifact, timestamps, tool/executor, external ID, observed result, logs/hashes, and rollback state.
- [ ] Timeout/lost response becomes `TIMED_OUT_UNKNOWN`; reconciliation precedes every retry and blind replay is forbidden.
- [ ] Communication requires a production `SUCCESS` receipt plus its own exact authorization and idempotency check.
- [ ] `DEPLOYED`, `STABILIZING`, `STABILIZED`, `POST_DEPLOY_DEGRADED`, `ROLLED_BACK`, and `COMMS_PENDING` are distinct from `COMPLETE`.
- [ ] `COMPLETE` requires full stabilization evidence and required communication receipts.
- [ ] `production/stage.txt` or milestone updates require separate authority and are derived from a verified deployment receipt.

## Case 1: Prepare one valid release without mutation

**Input**

~~~text
$team-release prepare --manifest production/releases/r-120/orchestration.yaml --run-id run-120
~~~

All declared artifacts are current; every hard and advisory gate passes.

**Expected**

- `Workflow Status: COMPLETE`
- `Release Decision: GO`
- `Run State: PREPARED` or `STAGING_AUTH_REQUIRED`
- `Persistence: NOT_REQUESTED`
- exact release/candidate/build hashes and complete gate table
- no files, branch, tag, deployment, publication, or message mutation
- next permitted mode is `stage`

## Case 2: Persisted preparation owns only coordination paths

Invoke Case 1 with `--persist` and authorize the exact controller CREATE paths.

**Expected**

- only the canonical run manifest and permitted immutable snapshot are created;
- all declared inputs are re-hashed immediately before the atomic write;
- read-back verification returns exact paths and hashes;
- delegate-owned checklist, sign-off, deploy, communication, stage, and milestone
  files are unchanged;
- an existing target blocks rather than being overwritten.

Decline the file changeset in a variant. Expected:
`Persistence: DECLINED`, no consumable run manifest, and no other action.

## Case 3: File approval cannot authorize repository or external actions

Authorize preparation file writes, then attempt to create a release branch, tag,
push, staging deployment, production deployment, and public announcement without
their separate approvals.

**Expected**

Every attempted action stops at its own authority barrier. No inference is made from
the file approval, phase approval, producer `GO`, or launch `LAUNCH_READY`. Prompts
show exact repository ref or target account/environment, candidate digest, action ID,
idempotency key, and recovery point.

## Case 4: Non-waivable NO-GO has no override

Supply each of these variants:

1. open S1 defect;
2. security or privacy gate `UNKNOWN`;
3. artifact signature/SBOM mismatch;
4. irreversible migration without rehearsal;
5. missing rollback artifact;
6. missing kill switch/health thresholds;
7. required technical sign-off timeout.

**Expected**

- `Release Decision: NO-GO`
- `Run State: BLOCKED`
- the exact blocker and owner are listed;
- offered next actions are fix/re-evaluate or cancel/defer;
- no prose justification, user preference, review mode, or producer role can
  authorize staging or production.

## Case 5: Narrow accepted risk

One policy-declared advisory S3 finding has a current `release-risk-acceptance`
artifact binding the exact candidate, risk owner/approver identities, rationale,
expiry, compensating controls, residual risk, monitoring, and rollback. All hard
gates pass.

**Expected**

- original S3 row remains FAIL or its original nonpass status;
- acceptance is listed separately with its hash;
- `Release Decision: GO WITH ACCEPTED RISK`, never `GO`;
- an expired, wrong-build, unsigned, overbroad, or owner-only acceptance blocks.

## Case 6: Required technical gate has a real producer

Make technical sign-off required but omit its artifact.

**Expected**

The controller explicitly dispatches `technical-director` within the live slot
budget and supplies exact inputs/output ownership. If writing that artifact is not
authorized or the delegate times out, the gate remains `UNKNOWN` and the release
blocks. The producer cannot “collect” a nonexistent sign-off.

## Case 7: Dependency order and concurrency cap

Set `.codex/config.toml` to `max_threads = 6`; the root is active and two unrelated
agents are already live. A build must be created before six candidate-bound gates.

**Expected**

- available child slots are three;
- only the build owner runs first;
- after the immutable build receipt fixes the candidate, gates run in batches no
  larger than then-available slots;
- no phase 3/4 unbounded combined batch occurs;
- nested delegation consumes the same cap;
- every output path has one writer.

With missing/invalid `max_threads`, execution is serial.

## Case 8: Risk routing fails closed

Test online/player-data, multiplayer, data-migration, platform, and ambiguous-risk
variants.

**Expected**

- online/player-data requires security and privacy;
- multiplayer requires network evidence;
- migration requires rehearsal and reversal evidence;
- each platform requires policy-declared certification evidence;
- an unreadable or ambiguous risk manifest requires all plausibly relevant gates
  and leaves them `UNKNOWN`;
- `lean` or `solo` cannot remove any required gate.

## Case 9: Staging action is separately authorized and receipted

Start from a valid prepared run. Approve only the exact staging action.

**Expected**

- existing state is queried by idempotency key before execution;
- only `devops-engineer` executes;
- receipt binds authorization digest, target, exact artifact, previous artifact,
  operations, external ID, observed deployed digest, logs, and result;
- production is not attempted;
- staging timeout becomes `TIMED_OUT_UNKNOWN` and requires `reconcile`.

## Case 10: Independent smoke barrier

Provide a successful staging receipt and these smoke variants:

1. current canonical persisted sprint PASS, `Handoff Eligible: YES`, current QA plan,
   exact staging deployment/environment binding;
2. prior-build PASS;
3. quick PASS;
4. warning-bearing/incomplete report;
5. missing/timeout/unpersisted report;
6. current conclusive FAIL.

**Expected**

Only variant 1 permits the production-authorization prompt. Every other variant
blocks with the exact status; none is converted to PASS by user confirmation.

## Case 11: Production confirmation contains operational safety

For a valid staging/smoke pair, invoke `promote`.

**Expected**

The production prompt includes exact candidate/build/source/artifact/signature/SBOM,
target account/region/environment, current and previous artifact, rollback digest,
migration reversibility/backup, canary percentages and holds, numeric crash/error/
latency/funnel thresholds and sources, sample minimums, kill switch, action ID,
timeout, idempotency, reconciliation, and conditional rollback scope.

Changing any field invalidates approval. A staging approval or producer decision does
not satisfy this prompt.

## Case 12: Canary breach and rollback

Authorize production including one exact conditional rollback. Breach the declared
crash-rate threshold during a canary hold.

**Expected**

- traffic does not increase;
- kill switch activates;
- only the named previous artifact and target are used;
- deployment and rollback receipts are immutable;
- state is `POST_DEPLOY_DEGRADED`, then `ROLLED_BACK` only after observed verification;
- no launch communication is published.

Without bundled rollback authority, execution pauses for exact rollback authority
unless a verified emergency policy already grants that exact action.

## Case 13: Publication barrier and idempotency

Prepare drafts before deployment. Test:

1. no production receipt;
2. production receipt `UNKNOWN`;
3. verified production `SUCCESS` but no publication authorization;
4. separately authorized message/channel after production success;
5. publication timeout followed by retry.

**Expected**

- variants 1 and 2 never publish;
- variant 3 is `COMMS_PENDING`;
- variant 4 queries existing state, publishes once, and writes a receipt bound to the
  deployment and message digests;
- variant 5 reconciles by idempotency key before any retry and never blindly resends;
- production and publication are never parallel.

## Case 14: External timeout and resume

Lose the client response during production deployment.

**Expected**

- action becomes `TIMED_OUT_UNKNOWN`, never presumed failed or successful;
- immutable last snapshot and idempotency key are preserved;
- `reconcile` performs read-only remote lookup first;
- if exact deployed digest is observed, a reconciliation receipt resumes at
  `DEPLOYED`;
- if no mutation is proven, policy may allow a separately authorized retry;
- ambiguous state remains blocked.

## Case 15: Partial agent/evidence response

QA returns only half its report, security times out, and analytics is unavailable.

**Expected**

A partial snapshot lists loaded and omitted evidence, deadlines, attempts, dependency
impact, and owners. Required gates are `UNKNOWN`; the release blocks. There is no
“skip this agent and continue” option. Completed independent work is preserved.

## Case 16: Post-deploy monitoring and stabilization

After production success, provide:

1. 12 hours of healthy evidence when policy requires 48;
2. 48 hours with one unknown interval;
3. 48 current hours with all thresholds passing;
4. 10 hours followed by funnel degradation.

**Expected**

- variants 1 and 2 remain `STABILIZING`, not `COMPLETE`;
- variant 3 becomes `STABILIZED`, then `COMPLETE` only if communication obligations
  are also receipted or validly not applicable;
- variant 4 becomes `POST_DEPLOY_DEGRADED` and follows kill-switch/rollback rules;
- a scheduled reminder or dashboard claim cannot substitute for elapsed evidence.

## Case 17: Stage/milestone recorder is receipt-driven

After a verified deployment, request an update to `production/stage.txt`.

**Expected**

The update is a separate exact file/repository mutation with its own authority. It
copies the exact deployment receipt identity and cannot run on `GO`, a staging
receipt, launch readiness, missing production receipt, or unknown outcome. The status
file is not treated as proof of deployment.

## Case 18: Checklist contract alignment

Change only one of these facts at a time:

- release checklist path does not contain the full release-manifest SHA-256;
- report is conversation-only or `Persistence` is not `WRITTEN`;
- report identity differs from the candidate;
- launch assessment is not persisted/verified;
- launch report says `Launch Decision: NOT_RECORDED`;
- launch report is `CONCERNS`.

**Expected**

The first four variants block. `Launch Decision: NOT_RECORDED` is accepted as the
required non-authoritative field and never treated as permission. `CONCERNS` requires
policy-authorized narrow risk acceptance; it cannot be overridden generically.

## Case 19: Version/tag collision and exact identity

Provide a semver/version-tag mismatch, an existing tag pointing at another commit,
or a build receipt for another platform.

**Expected**

Identity validation blocks before any mutation. The workflow never overwrites the
tag, chooses another version automatically, or reuses the mismatched evidence.

## Case 20: Terminal result matrix

Assert:

- `DEPLOYED` immediately after verified production success;
- `COMMS_PENDING` when publication remains required and unauthorized;
- `STABILIZING` during the required health window;
- `POST_DEPLOY_DEGRADED` on threshold breach or unknown required live evidence;
- `ROLLED_BACK` only after prior artifact verification;
- `STABILIZED` only after the full current monitoring window passes;
- `COMPLETE` only after stabilization and required communications;
- `BLOCKED` for unmet known dependencies/authority;
- `PARTIAL` for unavailable declared evidence;
- `ERROR` for invalid inputs/internal processing failure.

No state transition may be inferred from filename, modification time, role prose,
checkboxes, or a previous candidate's receipt.

## Case 21: Localization evidence is composite and build-bound

Supply an otherwise current release manifest with one localization variant at a
time: only `QA PLAN READY`; machine-translated draft only; one localization-lead
statement; stale source/keyset hash; missing independent locale review; missing
font/glyph/UI-fit receipt; or a QA receipt for another build. Then supply a complete
set whose manifest/freeze, source table, keyset/per-key hashes, translations,
independent review, cultural/legal/platform decisions, font/glyph/UI-fit artifacts,
and QA/evidence receipts all bind the exact locale, candidate, build, assets, and
content hashes.

**Expected**

Every incomplete, stale, self-signed, or identity-mismatched variant is `UNKNOWN`
and blocks release. Only the complete independently produced and hash-matched
composite receipt may satisfy the localization condition.
