---
name: release-checklist
description: "Normalize exact release-candidate, build, deployment, platform, legal, and manual evidence into an immutable identity-bound checklist without issuing a release, deployment, or publication decision."
---

# Release Checklist

Normalize one immutable evidence snapshot for one exact release candidate. This
workflow is a collector, not the release gate: an item PASS is not a release PASS, a
normalized checklist is not a go/no-go decision, a build is not deployment, and a
recorded report grants no deployment or publication authority.

## Invocation and strict request

Invoke only as:

`$release-checklist --request <path> --expect-request <sha256>`

Both flags are required exactly once. With missing/invalid flags or unknown arguments,
show that usage and stop before project reads, evidence inspection, output,
delegation, or writes. Reject directories, globs, traversal, moving aliases,
symlink/junction/reparse escape, unsupported schema, unknown/repeated fields, unsafe
IDs, and expected/actual request hash mismatch.

The request is strict `cgs.release-checklist-request/v2` and declares:

- stable release/run IDs, display/semantic version and assessment scope;
- one exact `cgs.release-candidate-manifest/v2` path/hash and candidate identity;
- one exact build-candidate manifest and build receipt path/hash, candidate/build IDs,
  artifact path/hash, source commit/tree/ref/tag identity, toolchain/configuration and
  target platform matrix;
- deployment scope `PRE_DEPLOY`, `DEPLOYMENT_EVIDENCE_INCLUDED`, or
  `POST_DEPLOY`, plus an exact deployment evidence index. Missing deployment receipts
  remain NOT_PROVIDED and cannot satisfy deployment-dependent items;
- exact release-policy and authority-registry paths, schemas, versions and hashes;
- exact ordered evidence index keyed by stable checklist item ID, including every
  referenced dependency path/hash rather than a directory;
- exact applicable `AGENTS.md` root-to-target path/hash chain in precedence order;
- optional exact predecessor report path/hash, never a newest-report lookup;
- fixed item/file/byte/dependency-depth/time budgets and evidence cutoff time source;
- operation `analyze-only` or `record-checklist`; and
- for recording, allowed immutable report root, recorder ID, mutation authority/expiry,
  create-new capability, maximum bytes and explicit non-writes.

Normalize all literal and real paths beneath the project root. Do not infer current/
latest release, build, deployment, policy, evidence, platform, target or predecessor.
No project scan, CI directory walk, internet search or modification-time selection is
allowed.

## Ownership and authority boundaries

The analyzer reads and normalizes evidence only. The recorder may create the exact
presented report bytes after separate mutation authority; it cannot change a row,
reason, status or evidence reference. One transaction has one writer for one absent
target.

The release-policy owner defines items/criteria. Build and deployment systems own
their receipts. Bug registry, QA/manual testers, platform/certification, ratings,
store, legal, privacy, security and waiver authorities own their exact evidence. The
downstream release gate alone interprets the checklist under policy. The model is none
of those authorities and cannot sign, certify, waive, mark N/A, close a bug, or turn a
name/checkbox into approval.

Always report:

- `Gate Decision: NOT_EVALUATED`;
- `Release Authority: NONE`;
- `Deployment Authority: NONE`; and
- `Publication Authority: NONE`.

Never emit RELEASE READY/BLOCKED, GO/NO-GO, ship, deploy or publish authorization.
Never invoke gate-check, team-release, deployment, publication, changelog, patch-notes,
a director, or another workflow.

## Hard bounds and complete coverage

The request/policy may lower but never raise:

| Resource | Hard ceiling |
|---|---:|
| policy checklist items | 512 |
| evidence index entries | 2,048 |
| referenced dependency files | 4,096 |
| total evidence bytes | 128 MiB |
| single evidence file | 16 MiB |
| dependency depth | 8 |
| target platform/configuration rows | 128 |
| total elapsed time | 20 minutes |

Read only explicit indexed paths. Stop before a ceiling and return PARTIAL with exact
completed/omitted item/evidence/file/byte counts, identities, reason and resume cursor.
A truncated, sampled, timed-out or partially decoded evidence set cannot produce PASS.
Rows that could not be completely evaluated remain UNKNOWN and name the owner.

## Canonical schemas and identities

Use strict parsers and exact raw-byte SHA-256. Canonical serialization is UTF-8/LF/NFC,
lowercase hex SHA-256, schema field order, sorted sets and stable item order.

```text
release_identity_sha256 = sha256(release ID/version + source commit/tree/ref/tag +
  target platform/configuration matrix + release-manifest bytes)
candidate_identity_sha256 = sha256(candidate/build IDs + artifact hash + source
  commit/tree + toolchain/configuration/platform + build receipt hash)
deployment_identity_sha256 = sha256(deployment ID + candidate/artifact/source +
  environment/channel/region/platform/rollout + result/time/evidence/receipt hashes)
instruction_chain_sha256 = sha256(ordered root-to-target AGENTS paths/raw hashes +
  precedence decisions)
evidence_snapshot_sha256 = sha256(cutoff-time receipt + ordered evidence/dependency
  paths/raw hashes/states + candidate/build/deployment bindings)
item_row_sha256 = sha256(stable item/policy + evidence states/hashes + item status +
  owner + N/A/waiver records + reason)
checklist_identity_sha256 = sha256(release/candidate/deployment/policy/instruction/
  evidence identities + ordered item-row hashes + predecessor-delta hash)
```

Deployment identity is `NOT_PROVIDED` when no receipt is supplied; never hash an empty
placeholder as deployment proof. Identical request, policy and evidence bytes must
produce identical rows, counts, reasons, deltas and checklist identity. Generated-at
is supplied by the request's trusted cutoff/time receipt or excluded from the identity.

## Status vocabulary

Assign each policy item exactly one status:

- `PASS(evidence)` — complete CURRENT authoritative evidence satisfies every exact
  positive condition for this candidate/build/deployment/platform scope;
- `FAIL(evidence)` — complete CURRENT authoritative evidence conclusively satisfies an
  exact fail condition for that scope;
- `UNKNOWN(owner)` — missing, stale, partial, unavailable, invalid, inconclusive,
  unauthorized or non-machine-verifiable evidence; or
- `N/A(authority)` — a current verified applicability authority explicitly states the
  item does not apply and binds rationale, item/policy, release/candidate/platform,
  time and expiry.

Evidence state is independently `CURRENT`, `STALE`, `PARTIAL_EVIDENCE`, `MISSING`,
`UNAVAILABLE`, `INVALID`, or `INCONCLUSIVE`. File existence, filename, mtime, a checked
box, role label, empty result, template, unsigned statement, model reasoning or prior
candidate PASS cannot produce PASS/N/A.

Waiver is not an item status. Record `waiver_state`: `NONE`, `VALID`, `STALE`,
`INVALID`, or `OUT_OF_SCOPE`. A valid `cgs.release-waiver/v2` binds the exact FAIL or
UNKNOWN row hash, release/candidate/build/deployment/platform, policy waiver clause,
authorized issuer/identity proof, rationale, compensating controls/evidence,
constraints, issued/expiry times and receipt hash. It never rewrites FAIL/UNKNOWN to
PASS or N/A; only the downstream gate decides whether policy permits it.

Workflow status is `NORMALIZED`, `PARTIAL`, or `BLOCKED`. Recorder status is
`ANALYSIS_ONLY`, `CREATED`, `DECLINED`, `FAILED`, or `RECOVERY_REQUIRED`. These are
operational states, never release verdicts.

## Phase 1 — Validate request and the applicable instruction chain

Strictly parse request, release manifest, candidate/build manifests, policy, authority
registry and evidence index. Hash raw bytes before parsing and reject duplicate keys,
unsupported formats, unsafe references and schema drift.

Read in full every applicable `AGENTS.md` from project root through the requested
report target. Verify the request's ordered path/hash chain, apply closest-file
precedence and record every loaded file, shadowed/conflicting rule and effective
decision. A missing, extra, reordered or hash-mismatched instruction, or an unresolved
conflict, is BLOCKED with zero writes.

The release policy defines every stable item ID, category, target scope, required/
optional/applicability predicate, owner, authoritative artifact schema and allowed
producer/verifier, exact PASS/FAIL conditions, UNKNOWN treatment, N/A authority,
waiver clause/authority, expiry/freshness, hard-gate/advisory class, dependencies,
cross-item rules and canonical severity mapping. Do not invent, omit, reorder or merge
policy items.

## Phase 2 — Pin release candidate, build, artifact, and deployment identities

The release manifest must bind stable release identity, exact source commit/tree/ref/
tag, complete platform/configuration matrix, policy/authority/instruction/evidence
hashes, candidate/build/artifact identity and manifest owner/time.

Validate the build-candidate manifest and build receipt: exact candidate/build IDs,
artifact raw hash, source commit/tree, toolchain/container/dependency/config hashes,
platform matrix, argv, result/exit code, start/end time, producer/verifier, complete log
hash and receipt hash. Re-hash local artifact bytes. For remote artifacts require a
trusted content/attestation receipt; a URL or filename is not identity.

Validate each indexed deployment receipt independently. It must bind deployment ID,
the exact candidate/build/artifact/source, environment/channel/regions/platforms,
rollout wave/state, result, runner/issuer, started/deployed-at times, logs/evidence and
receipt hash. Staging/canary/scheduled/in-progress deployment cannot satisfy production
items unless the policy item explicitly targets that exact scope. A successful build
is not deployment, and deployment does not prove legal/cert/store/manual or publish
approval.

Missing core release/candidate/build identity is BLOCKED. Missing deployment evidence
does not invent a deployment; deployment-dependent rows become UNKNOWN unless an exact
authorized N/A applies.

## Phase 3 — Load only indexed, complete, fresh evidence

For every item, load only its exact evidence-index entries and recursively declared
dependencies within bounds. Each artifact records raw path/hash, artifact type/schema,
producer/issuer/verifier, tool/version/config/argv where applicable, start/end or
observed time, result/exit code, candidate/build/artifact/source/platform/deployment
bindings, completeness fields, logs/raw attachments and referenced hashes.

Re-hash every artifact/dependency. Evaluate freshness only by the policy's cutoff,
expiry and source-revision rules, never mtime. Evidence is:

- CURRENT only if all bytes, identities, schemas, bindings, scope, authority,
  timestamps, completeness and dependencies match;
- STALE when readable evidence or dependency belongs to another revision/candidate/
  build/deployment/platform, changed bytes, or exceeded policy freshness;
- PARTIAL_EVIDENCE when declared output/log/test/attachment coverage is incomplete;
- MISSING when required index entry is absent;
- UNAVAILABLE when declared bytes cannot be read/decoded/parsed/verified;
- INVALID when schema, identity, authority, signature or references are inconsistent;
  or
- INCONCLUSIVE when current complete evidence does not satisfy an exact PASS/FAIL rule.

All non-CURRENT states map to UNKNOWN unless a separate CURRENT authoritative artifact
conclusively proves FAIL. An unreadable/limit/timeout condition also makes workflow
PARTIAL; a fully read STALE/MISSING/INVALID/INCONCLUSIVE set can still be NORMALIZED
with UNKNOWN rows. Never reuse old evidence or silently sample a log.

## Phase 4 — Normalize technical, test, bug, and content evidence

Technical/automated receipts require exact run/test IDs, candidate/build/source/
platform/config, runner/tool version, argv/environment hash, test source/selection/
requirement hashes, start/end time, exit code, per-test results, completeness statement,
complete raw/log/receipt hashes and authorized producer/verifier. Selection, plan,
template, discovery, “completed” label or conversation output alone cannot PASS.

For canonical smoke, regression, soak, performance, playtest and test-evidence review,
require the exact persisted artifact type/schema and all policy-required dependencies.
PASS needs CURRENT complete execution plus the exact positive readiness/coverage/result
fields. A CURRENT conclusive policy fail becomes FAIL. Incomplete, targeted where full
is required, quarantined without current policy disposition, missing sensitivity,
profile mismatch, insufficient duration/participants, or finalization-only status is
UNKNOWN.

Bug evidence requires an exact authoritative registry snapshot bound to the release
scope/candidate/cutoff. Canonical severity is:

| Canonical | Meaning |
|---|---|
| S1 | Critical |
| S2 | Major / High |
| S3 | Moderate / Medium |
| S4 | Minor / Low |

Legacy labels/numbers require the policy's explicit schema-versioned migration mapping
and mapping hash; otherwise severity is UNKNOWN. Do not infer severity from text.
Open current S1/S2 or other severities yield FAIL only under exact policy conditions.
A waiver remains separate and never closes/reclassifies the bug or changes item status.

Assets, performance, localization, content, changelog, scope and code-health evidence
use the same exact candidate-bound structured-receipt rules. Do not perform ad hoc
source/TODO/asset scans or treat a file's existence as acceptance.

## Phase 5 — Validate platform, certification, legal, store, and manual authority

Human/platform-controlled items require a current receipt whose issuer is allowed by
the hash-bound authority registry. Every receipt binds stable item/release/candidate/
build/artifact/platform/deployment IDs, exact reviewed artifact paths/hashes, scope and
jurisdiction/region/channel, decision/result, constraints, authority/role, identity or
signature verification receipt, issued/observed time, expiry, external submission/job/
case ID where applicable, policy path/hash and receipt hash.

Additional minimums:

- platform/certification: platform/product/account IDs, package digest, certification
  suite/version, submission attempt, official result and unresolved conditions;
- store/pricing/listing: exact listing/media/legal-text/pricing hashes, territories,
  storefront state and authorized operator receipt;
- legal/privacy/ratings/security: named jurisdiction/scope, reviewed bytes, explicit
  decision/limitations and authorized counsel/DPO/rating/security attestation;
- manual QA/accessibility/experience: plan/case IDs, exact device/OS/input/profile,
  candidate/build, executor identity, expected/actual result, start/end time, raw
  attachment hashes and policy-required distinct verifier; and
- N/A or waiver: exact separate authority and fields defined in Status vocabulary.

A self-attestation is valid only when policy/authority registry explicitly permits that
named role for that item and the identity proof is current; the model/recorder can
never be the attestor. Missing, expired, unsigned, wrong-scope or unverified receipt is
UNKNOWN, not PASS/N/A. A negative authoritative receipt may yield FAIL only through
the exact policy fail rule.

## Phase 6 — Assign deterministic item rows and optional predecessor delta

Emit every ordered policy item once as `cgs.release-checklist-item/v2`:

```text
item_id, category, policy class/hash, platform/configuration/deployment scope,
owner, evidence states and path/raw hashes, dependency/coverage/freshness result,
item status, exact rule/reason, N/A receipt, waiver state/receipt, item_row_sha256
```

Never leave blank boxes. Apply rules in policy order using canonical typed values; sort
multi-evidence hashes and target sets. Cross-item dependencies cannot make PASS unless
every required dependency is CURRENT and satisfies its exact condition.

If an exact predecessor path/hash is provided, validate artifact/schema/report hash,
release/candidate/policy namespace and stable item IDs. Compare current/prior row hashes
as RESOLVED, REGRESSED, CHANGED, UNCHANGED, ADDED or REMOVED. Prior evidence never
affects current status. An invalid predecessor makes comparison unavailable; never
search for another.

## Phase 7 — Aggregate without a release verdict and freeze checklist identity

Count PASS, FAIL, UNKNOWN and N/A by policy class and platform; report valid/stale/
invalid waiver counts separately. Do not calculate readiness, risk acceptance, GO/
NO-GO or release verdict from counts.

Workflow is PARTIAL when a limit/timeout/unavailable input prevented complete
inspection. Otherwise it is NORMALIZED after every item has one status, including FAIL
or UNKNOWN. Invalid/ambiguous release identity, policy, instruction chain or item
namespace is BLOCKED. Gate Decision remains NOT_EVALUATED.

Compute checklist identity from the frozen identities, ordered row hashes and delta.
The immutable report target is exactly:

```text
production/releases/{release-id}/{candidate-identity-sha256}/checklists/
{checklist-identity-sha256}.md
```

Both digest segments are full 64-character lowercase hex. Never use date-only,
short-hash, latest or mutable alias paths.

## Phase 8 — Analyze-only or recorder create-only CAS

`analyze-only` returns exact report candidate bytes/hash and `Recorder Status:
ANALYSIS_ONLY`; it writes nothing. The report header states
`Artifact Type: release-evidence-checklist`, `Schema Version: 2`, every canonical
identity/status/count, `Gate Decision: NOT_EVALUATED`, and all three authority NONE
fields. It includes the loaded AGENTS chain, evidence inventory/states, ordered item
rows, failures, unknowns/owners, N/A/waiver receipts, predecessor delta, omissions and
consumer requirements.

`record-checklist` may create only that one absent immutable target. Its parent must
already exist. Preview one mutation manifest with request/release/candidate/build/
deployment/policy/authority/instruction/evidence/checklist hashes, target expected
ABSENT, exact report bytes/hash, recorder, create-new primitive, size, authority/expiry
and non-writes. Evidence normalization approval is not mutation authority.

Immediately before create, CAS every input/dependency hash and identity, Git/artifact/
deployment state, cutoff/authority validity, parent identity, report bytes and target
ABSENT state. Use an atomic no-replace/create-new primitive; if unavailable or anything
drifts, write nothing. Flush, close, strictly parse, read back and verify the exact file,
internal identities, row hashes/counts and report hash. An existing target or drift
returns recorder FAILED without overwriting. A post-create mismatch returns
RECOVERY_REQUIRED and exact expected/actual hashes; never overwrite or silently delete.

The recorder never updates an index, latest pointer, prior report, manifest, evidence,
policy, Git, build, deployment, gate state or external system.

## Phase 9 — Consumer contract and stop

Return `cgs.release-checklist-result/v2` with request/release/candidate/build/deployment/
policy/authority/instruction/evidence/checklist identities; evidence-state and item/
waiver counts; complete rows/delta; workflow and recorder statuses; report target/hash
or NOT_WRITTEN; non-writes; blockers/partial scope; accountable owner per FAIL/UNKNOWN/
invalid N/A/waiver; and exactly one legal next action.

A downstream gate receives the exact report path/hash and every identity, re-hashes all
dependencies, independently applies the named policy, and remains the only release
decision owner. File existence, workflow status, recorder status, counts, PASS rows or
waivers alone never imply readiness.

Stop after the packet. Do not invoke the gate, owners, evidence producers, deployment
or publication. Do not fix evidence, close bugs, solicit/sign attestations, deploy,
message, upload or publish.
