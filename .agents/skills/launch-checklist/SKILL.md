---
name: launch-checklist
description: "Evaluate one immutable launch candidate with build-bound test evidence, risk-profile soak requirements, verified external/manual attestations, recovery rehearsals, and a deterministic readiness projection that never records the launch decision."
---

# Launch Checklist

Evaluate the evidence readiness of one exact launch candidate. A checked box is not
evidence, a build is not deployed service, a readiness verdict is not a launch
decision, and a recorded assessment grants no deployment or publication authority.

## Invocation and strict request

Invoke only as:

`$launch-checklist --request <path> --expect-request <sha256>`

Require both flags exactly once. With a missing/invalid flag or unknown argument, show
that usage and stop before project reads, evidence loading, output, delegation, or
writes. Reject directories, globs, traversal, moving aliases, symlink/junction/reparse
escape, unsafe IDs, unsupported schemas, duplicate/unknown fields, and expected/actual
request hash mismatch.

The request is strict `cgs.launch-checklist-request/v2` and declares:

- mode `ASSESS` or `SIMULATE`, stable release/run/assessment IDs, and operation
  `analyze-only` or `record-assessment`; SIMULATE permits only analyze-only;
- one exact `cgs.launch-candidate-manifest/v2` path/hash;
- candidate/build IDs, artifact path/hash, source commit/tree/ref/tag, engine/toolchain
  and full platform/configuration/region/channel/store matrix;
- exact launch-policy, authority-registry and `cgs.launch-risk-profile/v1` paths,
  schemas, versions and hashes;
- one exact `cgs.launch-test-evidence-manifest/v2` path/hash plus ordered evidence and
  dependency inventory keyed by stable check ID;
- exact applicable root-to-assessment-target `AGENTS.md` path/hash chain in precedence
  order;
- optional exact `release-evidence-checklist` Schema Version 2 report path/hash and
  optional previous launch-assessment path/hash, never latest-file discovery;
- evidence cutoff trusted-time receipt and fixed item/file/byte/depth/time budgets;
- for recording, the immutable assessment root, recorder, mutation authority/expiry,
  create-new capability, maximum report bytes and explicit non-writes.

Validate release/assessment/platform IDs before path use. Normalize literal and real
paths under the project root. Do not infer the latest candidate, build, checklist,
policy, test run, external receipt, sign-off, target, launch date or previous report.
Do not scan CI/log/test/source/milestone/store directories or query external systems.

## Authority and non-writes

This workflow owns evidence normalization and the deterministic readiness verdict only.
It does not own the final launch decision. Always set:

- `Launch Decision: NOT_RECORDED`;
- `Deployment Authority: NONE`; and
- `Publication Authority: NONE`.

The user or separately authorized launch gate alone records GO, NO_GO or accepted risk.
That decision cannot rewrite evidence/check states. The model cannot sign, attest,
waive, accept risk, certify a platform, approve legal/privacy/IP, provision service,
run a rehearsal, deploy, publish, contact an owner, or invoke another workflow.

The analyzer is read-only. The recorder may create exactly the presented immutable
report after separate mutation authority; it cannot change a row, status, verdict or
input. Never edit manifests, evidence, sign-offs, previous assessments, indexes/latest
pointers, Git, builds, stores, infrastructure, deployment or publication state.

## Hard bounds and coverage

The request/policy may lower but never raise:

| Resource | Hard ceiling |
|---|---:|
| stable launch checks | 512 |
| evidence entries | 2,048 |
| dependency files | 4,096 |
| total evidence bytes | 128 MiB |
| single evidence file | 16 MiB |
| dependency depth | 8 |
| platform/configuration rows | 128 |
| total elapsed time | 20 minutes |

Read only explicit inventory paths. Stop before exceeding a ceiling and return
`Workflow Status: PARTIAL` with required/loaded/failed/omitted/stale/manual counts,
paths/hashes, exact reason and identity-bound resume cursor. Never silently sample,
truncate or render omitted inputs as zero/PASS. Partial loading affecting any HARD
check deterministically blocks readiness; advisory-only partial loading yields
CONCERNS but never LAUNCH_READY.

## Canonical identities and statuses

Use strict schema parsers and record SHA-256 of exact raw bytes before parsing.
Canonical serialization is UTF-8/LF/NFC, schema field order, sorted sets and stable
check-ID order.

```text
launch_candidate_identity_sha256 = sha256(release/product/version + candidate/build/
  artifact/source + platform/configuration/region/channel/store matrix + manifest)
risk_requirement_identity_sha256 = sha256(risk-profile bytes + launch-policy rule +
  selected risk dimensions + derived soak/recovery/capacity requirements/rationale)
instruction_chain_sha256 = sha256(ordered AGENTS paths/raw hashes + precedence decisions)
test_evidence_manifest_sha256 = sha256(candidate identity + platform matrix + ordered
  test/run/evidence entries and dependency hashes)
evidence_snapshot_sha256 = sha256(cutoff-time receipt + ordered check/evidence raw hashes,
  states, bindings, coverage and omissions)
check_row_sha256 = sha256(check/policy/gate/applicability + evidence states/hashes +
  check status + owner + attestation/N-A/waiver + reason)
assessment_identity_sha256 = sha256(assessment ID + launch candidate/risk/policy/
  authority/instruction/test/evidence identities + ordered row hashes + verdict + delta)
```

Identical request and input bytes produce identical rows, counters, reasons, verdict
and assessment identity. Generated-at is taken from the trusted cutoff receipt or kept
outside the identity.

Use independent fields:

| Field | Values |
|---|---|
| Workflow Status | `ASSESSED`, `PARTIAL`, `BLOCKED`, `ERROR` |
| Evidence Coverage | `COMPLETE`, `PARTIAL`, `UNAVAILABLE` |
| Evidence State | `CURRENT`, `STALE`, `PARTIAL_EVIDENCE`, `MISSING`, `UNAVAILABLE`, `INVALID`, `MANUAL_REQUIRED`, `INCONCLUSIVE` |
| Check Status | `PASS`, `FAIL`, `UNKNOWN`, `NOT_APPLICABLE` |
| Readiness Verdict | `LAUNCH_READY`, `LAUNCH_BLOCKED`, `CONCERNS`, `UNDETERMINED`, `ERROR` |
| Launch Decision | always `NOT_RECORDED` |
| Recorder Status | `ANALYSIS_ONLY`, `CREATED`, `SIMULATION`, `FAILED`, `RECOVERY_REQUIRED` |

PASS requires complete CURRENT authoritative evidence for this exact candidate/scope.
NOT_APPLICABLE requires current authorized applicability attestation. Missing, stale,
partial, unavailable, invalid, manual-required or inconclusive evidence maps to UNKNOWN,
unless separate CURRENT authoritative evidence proves FAIL. A file, date, screenshot,
URL, role/name, checkbox, prose assertion or previous-build PASS never proves a check.

## Deterministic readiness algorithm

After every stable row and coverage counter exists, apply exactly:

1. `ERROR` if request/manifest, candidate/build/artifact/source/platform identity,
   policy/item namespace or instruction chain cannot be uniquely validated.
2. `LAUNCH_BLOCKED` if any applicable HARD check is FAIL or UNKNOWN; any mandatory HARD
   domain/check is missing; any HARD evidence is stale/partial/unavailable/invalid/
   manual-required; or incomplete loading affects HARD scope.
3. `CONCERNS` if every HARD check is PASS or authorized NOT_APPLICABLE, but any ADVISORY
   check is FAIL/UNKNOWN or advisory evidence/coverage is incomplete.
4. `LAUNCH_READY` only when Evidence Coverage is COMPLETE, every required source loaded,
   all applicable HARD and ADVISORY checks are PASS or authorized NOT_APPLICABLE, all
   identities/receipts are current, and no warning/manual/waiver/omission remains.

At a gate class, conclusive FAIL takes precedence while the report still lists every
incomplete input. Risk acceptance or waiver never changes a check or readiness verdict;
the final launch gate owns that separate decision.

SIMULATE always returns `Readiness Verdict: UNDETERMINED` and labels the algorithmic
result only `Simulation Projection`. Simulation is never durable evidence.

## Phase 1 — Validate request, instructions, candidate, and policy

Strictly parse and hash request, launch/candidate/build manifests, launch policy,
authority registry, risk profile, test evidence manifest and indexes. Reject malformed
syntax, duplicate keys, unsupported artifacts and hash/identity drift.

Read in full every applicable `AGENTS.md` from project root through the requested
assessment target. Verify ordered paths/hashes, apply closest-file precedence and
record loaded, shadowed and effective rules. A missing, extra, reordered, mismatched or
unresolved instruction conflict is ERROR with zero writes.

The launch candidate manifest binds release/product/version/launch-window identity,
candidate/build/artifact/source, immutable tag, engine/toolchain, full target matrix,
mandatory domains, stable check IDs, gate classes, applicability, owner, exact evidence
contract/index entry, freshness/expiry, expected observable, N/A/waiver authority and
policy hashes. Do not invent or omit domains/checks.

Re-hash local artifact bytes; remote artifact needs a trusted content/build attestation.
Build receipt binds artifact/source/toolchain/config/platform, argv, result/exit code,
times, producer/verifier and complete log hash. Any core mismatch is ERROR.

## Phase 2 — Load the complete test-evidence manifest — LC-004

`cgs.launch-test-evidence-manifest/v2` binds the exact launch candidate, release policy,
QA-plan/test-selection/source hashes, full target matrix and each required check/test
entry. Each execution entry contains run/test IDs, platform/configuration/device,
runner/tool/parser versions, exact command/argv and environment/config hash, start/end
times, exit code, result, per-test result/duration/source/requirement mapping, skips/
omissions/quarantines/crashes, raw output/log/artifact paths+hashes, completeness and
receipt signature/hash.

Re-hash every entry and dependency. A plan, template, selected test list, discovered
file, CI badge, log directory or exit code without complete bound logs/results cannot
PASS. The full platform/configuration matrix required by policy must be covered; one
platform cannot stand in for another. Different build/commit/artifact, changed test
source/selection/log, incomplete result or stale tool/policy binding is UNKNOWN/STALE,
never PASS. Exact CURRENT conclusive negative evidence becomes FAIL under policy.

An optional `release-evidence-checklist` Schema Version 2 is normalized input only.
Re-hash its request/release/candidate/build/deployment/policy/instruction/evidence/
checklist identities, every row and dependency. Its Gate Decision must be
NOT_EVALUATED. File existence, NORMALIZED workflow, PASS counts or waivers never
substitute for launch-specific checks or the launch verdict.

## Phase 3 — Derive risk-profile requirements — LC-005

The immutable `cgs.launch-risk-profile/v1` declares approved risk dimensions such as
concurrency/traffic, persistence/data-loss impact, networking, platform count, live-
service dependency, economy/transactions, content size, prior incidents and change
magnitude. The launch policy supplies versioned deterministic lookup/formula rules and
authority.

Compute required soak duration, workload/profile, checkpoint cadence, sample coverage,
capacity margin, recovery objectives and any required repetitions exclusively from
those typed inputs/rules. Record rule ID/version/hash, input values, derived minimums,
rounding/unit normalization and rationale as `risk_requirement_identity_sha256`.
Never impose a universal 8-hour duration, pick a convenient tier, lower a requirement,
or infer missing risk inputs. Missing/ambiguous policy or profile makes the affected
HARD checks UNKNOWN and blocks readiness.

Soak PASS requires the exact candidate/environment/workload/profile, EXECUTED and gate-
eligible result, executed duration at least the derived minimum, required checkpoints/
samples, and every required stability/memory/performance/experience dimension PASS.
Failed/insufficient/inconclusive execution cannot pass even if a report says COMPLETED.

## Phase 4 — Normalize canonical technical and experience evidence

Use only exact indexed persisted artifacts and recursively verify their dependencies.

- Smoke: exact candidate-bound sprint/full scope, PASS, eligible handoff, current QA
  plan/test manifest, complete automated/manual/log hashes; quick/targeted/incomplete/
  warning/stale/unpersisted variants cannot PASS where full launch scope is required.
- Regression: current selection/requirements/test-source/failure-sensitivity plus one
  matching complete execution receipt for every active stable test; selection alone,
  gaps, awaiting run, stale, quarantine without authorized disposition or missing
  sensitivity is UNKNOWN.
- Soak/performance/capacity: apply Phase 3 requirements and exact protocol/manifest/raw/
  sample/result hashes.
- Playtest/accessibility/manual experience: completed candidate-bound session/case,
  exact participant/profile/device/scope, raw/ledger/attachment hashes and policy-
  required attester/verifier; protocols and subjective model interpretation cannot PASS.
- Test-evidence review: exact persisted full-scope candidate-bound review with adequate
  evidence, passing execution, eligible closure and all referenced hashes. Conversation,
  targeted, partial, stale, unavailable or mismatched review cannot PASS.

Source/security/config/content/localization/assets scans require structured bounded
receipts with commit/roots/rules/tool/argv/exit/counts/findings/omissions/log hashes.
Never run an ad hoc unbounded scan or infer a pass from file presence.

## Phase 5 — Verify external receipts and immutable sign-offs — LC-007

Certification, ratings, store/pricing/media publication, privacy/legal/IP, production
service/CDN/DDoS, analytics/crash/monitoring, community/support/moderation, review-key
distribution and similar external facts default to UNKNOWN/MANUAL_REQUIRED.

A valid `cgs.external-launch-receipt/v2` binds stable check IDs, exact release/candidate/
build/artifact/platform/region/channel/account/product, external object/submission/job/
version ID, expected observable and result, issuer/provider authority, source API/export
payload path/hash, issued/observed/verified times, expiry, verifier identity/method and
signature/receipt hash. Screenshots, copied URLs/emails, local policy files and model
statements are not receipts.

A valid `cgs.launch-owner-attestation/v2` binds attestation ID, owner identity/role and
authority-registry proof, stable check IDs, release/candidate/build/artifact/source/
platform scope, exact statement/result, reviewed paths/hashes, signed-at, valid-until,
signature or identity-verification receipt and attestation hash. The workflow never
creates, fills, copies or signs it. Typed names, checkbox/signature blocks, silence,
or older-build attestations remain UNKNOWN.

Any change to candidate/build/artifact/source/platform, reviewed bytes, policy or
authority registry makes a build-bound receipt/attestation STALE. N/A needs the same
immutable identity/time/scope/hash plus explicit applicability rule and rationale.
Waiver/risk acceptance remains separate from evidence readiness and cannot yield PASS.

## Phase 6 — Validate recovery rehearsal and objectives — LC-006

A plan/runbook or pipeline presence never proves rollback, restore, failover, hotfix or
go-live recovery. Require `cgs.recovery-rehearsal-receipt/v2` with rehearsal ID; exact
candidate/build/artifact and production-equivalent environment/data/schema; immutable
runbook/procedure hash; accountable owner, operator and verifier; injected failure;
executed step IDs; start/end timestamps; command/log/artifact/backup/restore hashes;
policy/risk-profile RTO, RPO and hotfix objectives with units; measured recovery time,
recovery point/data loss, integrity/consistency checks and service validation; outcome,
unresolved findings and signed receipt hash.

Compare measured values to the exact Phase 3 objectives. A CURRENT conclusive failed
rehearsal or exceeded RTO/RPO is HARD FAIL and LAUNCH_BLOCKED. Missing, plan-only,
stale, partial, wrong-environment, unverifiable or inconclusive rehearsal is UNKNOWN for
a required HARD check and also blocks readiness. Only a new immutable passing rehearsal
can replace the evidence; never relabel the failed receipt.

## Phase 7 — Normalize rows, coverage, and predecessor delta — LC-010

Emit every ordered stable check once as `cgs.launch-check-row/v2`:

```text
check ID, domain, gate class, applicability, expected observable, owner,
evidence type/path/raw hash/dependencies/state/freshness/coverage, candidate/platform
binding, check status, N/A/attestation/waiver references, exact reason, row hash
```

Assign PASS/FAIL/UNKNOWN/NOT_APPLICABLE only by policy typed rules. Preserve complete
load counters by domain/gate/platform. Evidence retrieval/parsing/limit/timeout failure
sets visible PARTIAL/UNAVAILABLE coverage; never suppress an omitted row.

If an exact predecessor path/hash is supplied, verify schema/report/assessment/candidate/
policy namespace and stable IDs. Compare row hashes as RESOLVED, REGRESSED, CHANGED,
UNCHANGED, ADDED or REMOVED. Prior evidence never affects current verdict. A candidate,
build, artifact or reviewed-byte change makes old bound receipts/sign-offs stale; an
invalid predecessor makes comparison unavailable, never a latest-file search.

## Phase 8 — Derive readiness and immutable assessment identity — LC-008/009

Apply the deterministic algorithm only after all rows/counters exist. Report blockers,
concerns and unknown/manual/stale/partial/unavailable evidence separately. Compute the
assessment identity from every frozen input/row/verdict/delta.

The immutable report target is exactly:

```text
production/releases/{release-id}/{launch-candidate-identity-sha256}/launch-readiness/
{assessment-identity-sha256}.md
```

Both digest segments are full 64-character lowercase hex. Each assessment ID/run and
changed input produces a new identity/path. Never use a date-only, mutable, short-hash,
latest, or in-place status file, and never overwrite an existing assessment.

`LAUNCH_READY`, `LAUNCH_BLOCKED` and `CONCERNS` are objective evidence verdicts only.
The user/separate launch gate remains the single final decision owner. This workflow
does not call gate-check or team-release, and the gate must consume exact assessment/
candidate/policy/evidence hashes and independently record its decision.

## Phase 9 — Analyze, simulate, or create one report

ASSESS + analyze-only returns exact report bytes/hash with `Recorder Status:
ANALYSIS_ONLY` and zero writes. SIMULATE begins and ends with:

`SIMULATION — NOT A LAUNCH VERDICT — NO SIGN-OFFS OR FILES CREATED`

It returns `Readiness Verdict: UNDETERMINED`, a clearly labeled Simulation Projection,
`Recorder Status: SIMULATION`, no durable report path/hash, and zero files, signatures,
receipts, submissions, messages or external actions.

ASSESS + record-assessment may create the one absent canonical report only. Its parent
must already exist. Preview one mutation manifest containing request/launch candidate/
risk/policy/authority/instruction/test/evidence/row/assessment/delta hashes, target
expected ABSENT, exact report bytes/hash, recorder, create-new primitive, maximum bytes,
authority/expiry and non-writes.

Immediately before create, CAS every input/dependency/object/artifact hash, cutoff and
authority validity, parent identity, report bytes and target ABSENT state. Use atomic
no-replace/create-new; if unavailable, target exists or anything drifts, write nothing.
Flush, close, strictly parse, read back and verify internal identities/rows/counters/
verdict/report hash. A post-create mismatch is RECOVERY_REQUIRED with exact expected/
actual hashes; never overwrite or silently delete evidence.

## Phase 10 — Terminal packet and stop

Return `cgs.launch-checklist-result/v2` with request/release/candidate/build/artifact/
source/platform/risk/policy/authority/instruction/test/evidence/assessment identities;
coverage counters; every row/status; QA/external/manual/recovery results; blockers,
concerns and omissions; verdict/projection; recorder/target/hash or NOT_WRITTEN;
Launch Decision NOT_RECORDED; authority NONE fields; non-writes; and exactly one legal
next owner/action.

Stop after the packet. Do not invoke the user gate, team-release, gate-check, evidence
owners, test/rehearsal systems, deployment, stores, infrastructure, communications or
publication.
