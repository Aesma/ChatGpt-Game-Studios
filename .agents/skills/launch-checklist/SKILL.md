---
name: launch-checklist
description: "Evaluates one immutable launch candidate from build-bound test evidence, verifiable external receipts, and authorized owner attestations using a deterministic readiness algorithm."
---

# Launch Checklist

Explicit invocation only. Use:

- `$launch-checklist assess --manifest <launch-manifest-path> --assessment-id <id> [--persist]`
- `$launch-checklist dry-run --manifest <launch-manifest-path> --assessment-id <id>`

This workflow normalizes evidence and derives an objective readiness verdict. It does
not publish a build, submit certification, provision infrastructure, sign on behalf
of an owner, accept risk, or make the final launch decision. It invokes no director
gate or downstream workflow.

An explicit bounded request authorizes the optional one-report write. Otherwise, when
`--persist` is present, preview the exact one-file changeset and obtain one approval
before writing. Do not prompt in dry-run or non-persisted assessment mode. Never
overwrite an existing assessment.

## Status and verdict contract

Use these independent fields:

| Field | Allowed values |
|---|---|
| `Workflow Status` | `COMPLETE`, `PARTIAL`, `BLOCKED`, `ERROR` |
| `Evidence Coverage` | `COMPLETE`, `PARTIAL`, `UNAVAILABLE` |
| `Check Status` | `PASS`, `FAIL`, `UNKNOWN`, `STALE`, `UNAVAILABLE`, `NOT_APPLICABLE` |
| `Evidence Status` | `VERIFIED`, `MANUAL_REQUIRED`, `MISSING`, `STALE`, `UNAVAILABLE`, `INVALID` |
| `Readiness Verdict` | `LAUNCH_READY`, `LAUNCH_BLOCKED`, `CONCERNS`, `UNDETERMINED`, `ERROR` |
| `Launch Decision` | always `NOT_RECORDED` by this workflow |
| `Persistence` | `VERIFIED`, `NOT_REQUESTED`, `SIMULATION`, `DECLINED`, `FAILED`, `NOT_ATTEMPTED` |

`PASS` is allowed only when the declared evidence contract verifies for the exact
release candidate. A local file, checked checkbox, filename, date, prose claim, or
model inference is never enough to prove an external or human fact.

`LAUNCH_READY` is an evidence result, not permission to launch. A later human or
formal gate may record `GO`, `NO_GO`, or `PROCEED_WITH_ACCEPTED_RISK`, but that
decision cannot rewrite this checklist's statuses or evidence.

## Deterministic readiness algorithm

Each stable check in the launch manifest declares `gate_class: HARD` or `ADVISORY`.
Evaluate every applicable check, then apply this strict order:

1. `ERROR` when the launch manifest or candidate identity cannot be validated.
2. `LAUNCH_BLOCKED` when any applicable HARD check is `FAIL`, `UNKNOWN`, `STALE`, or
   `UNAVAILABLE`; a mandatory HARD domain/check is absent; or partial loading affects
   any HARD check.
3. `CONCERNS` when all applicable HARD checks are `PASS` or valid
   `NOT_APPLICABLE`, but any ADVISORY check is `FAIL`, `UNKNOWN`, `STALE`, or
   `UNAVAILABLE`, or partial loading affects advisory scope only.
4. `LAUNCH_READY` only when every required source loaded, every applicable HARD and
   ADVISORY check is `PASS` or valid `NOT_APPLICABLE`, all bindings/hashes are
   current, and no unresolved warning or manual-required item remains.

`FAIL` takes precedence over incomplete evidence at the same gate class while the
report still lists every incomplete item. `UNKNOWN`, `STALE`, `UNAVAILABLE`,
`MANUAL_REQUIRED`, timeout, omitted evidence, invalid attestation, and unsupported
`NOT_APPLICABLE` can never be treated as PASS.

In dry-run mode set `Readiness Verdict: UNDETERMINED` and show the deterministic
result only as `Simulation Projection`. Dry-run is never a launch verdict.

## Canonical launch and assessment paths

Require the caller to supply one literal manifest path. The canonical convention is:

`production/releases/<release-id>/launch-manifest.yaml`

The immutable assessment path is:

`production/releases/<release-id>/launch-readiness/<assessment-id>/report.md`

Assessment IDs are stable slugs or UUIDs, not dates alone. Reject path separators,
dot segments, missing paths, symlink escapes, mismatched release IDs, and existing
assessment directories. Never choose a milestone, release, checklist, receipt, or
prior report by modification time or filename order.

## Phase 0: Validate arguments and dry-run boundary

Accept exactly one mode and documented options. `assess` may persist only with
`--persist`; otherwise it is read-only. `dry-run` rejects `--persist` and performs
zero writes, external submissions, signatures, attestations, and state changes.

Every dry-run output must begin and end with:

`SIMULATION — NOT A LAUNCH VERDICT — NO SIGN-OFFS OR FILES CREATED`

Do not create placeholder sign-offs, synthetic receipt IDs, fake signatures, or
claimed external actions in dry-run.

## Phase 1: Lock one release and build identity

Read the exact launch manifest bytes once and compute
`sha256:<64 lowercase hexadecimal characters>`. Require:

- `Artifact Type: launch-candidate-manifest`, schema version, release ID, game/product
  ID, launch version, target launch timestamp, regions, channels/stores;
- candidate-manifest path/raw SHA-256;
- candidate ID, build ID, build artifact path/raw SHA-256, source commit, immutable
  version tag, engine/version, platform/configuration target matrix;
- exact stable check IDs grouped into mandatory domains;
- for each check: gate class, applicability rule/result, owner role, evidence type,
  evidence path/receipt ID/raw SHA-256, freshness/expiry rule, and expected observable;
- owner/attester registry path/raw SHA-256;
- optional exact previous-assessment path/raw SHA-256 for delta comparison;
- manifest generation timestamp and hash algorithm.

Read and re-hash the candidate manifest. It must contain the staged build-candidate
identity: manifest version/type, same candidate/build/artifact hash/source commit,
engine/runner-compatible version, platform/configuration matrix, test-manifest
path/hash, and QA-plan path/hash.

Re-hash a local build artifact. A remote artifact requires a trusted build receipt
binding release/candidate/build/artifact hash/source commit/platform, issuer, job ID,
timestamp, and signature/verification rule. Any candidate/build mismatch is
`Workflow Status: ERROR`, `Readiness Verdict: ERROR`, and no report write.

## Phase 2: Validate checklist scope and source coverage

The launch manifest is the only routing authority. Require stable IDs for every
applicable domain:

- `BUILD` and code/security;
- `CONTENT`, localization, accessibility, and first-run experience;
- `QA`, performance, bugs, smoke, regression, soak, and playtest as applicable;
- `PLATFORM` certification and distribution;
- `STORE`, pricing, regional availability, and published media;
- `LEGAL`, privacy, licenses, ratings, and IP;
- `INFRA`, analytics, crash reporting, monitoring, capacity, backup, and security;
- `COMMUNITY`, support, moderation, and communications;
- `OPS`, on-call, incident response, rollback, hotfix, launch-day procedure.

A domain may be not applicable only when the manifest records the applicability rule,
reason, authorized owner, candidate/release scope, timestamp, and verifiable
attestation. The model cannot declare a domain or check not applicable.

Load every declared source and record exact counts for `required`, `loaded`, `failed`,
`omitted`, `stale`, `manual_required`, and `not_applicable`. A timeout, unreadable
file, unsupported format, missing source, hash mismatch, or parse failure is visible
and sets `Evidence Coverage: PARTIAL` or `UNAVAILABLE`. Never render omitted data as
zero or a passed checkbox.

Create `evidence_snapshot_sha256` from UTF-8 canonical JSON of ordered rows
`(check_id, gate_class, evidence_path, declared_sha256, observed_sha256,
evidence_status, check_status)`, sorted by stable check ID. Record the
canonicalization rule.

## Phase 3: Normalize evidence types

### Build-bound local/CI evidence

A build, scan, test, benchmark, or configuration item can pass only from a structured
receipt that binds the exact launch/candidate/build/artifact hash/source commit and
applicable platform/configuration. It also needs producer identity/version,
start/end timestamps, command/argv or measurement method, exit/result status, complete
log/artifact paths and hashes, parser/version, omissions, and receipt signature/hash.

Source scans must record repository commit, bounded roots, ruleset version/hash,
counts, findings, and log hash. A scan of a different commit or dirty unrecorded
working tree is stale.

### Verifiable external receipt

Certification, store configuration/publication, ratings, legal publication, trailer
publication, regional pricing, server provisioning, CDN/DDoS, analytics dashboards,
community channels, review-key distribution, and similar external facts default to:

- `Check Status: UNKNOWN`
- `Evidence Status: MANUAL_REQUIRED`

They may change only when a declared receipt verifies all of:

- `Artifact Type: external-launch-receipt`, schema and receipt ID;
- stable check IDs and exact release/candidate/build identity when build-specific;
- issuer/provider, account/project/channel/region/platform, and issuer authority;
- external object/submission/job/version ID and observed status;
- issued/observed/verified timestamps and expiry/review time;
- source URL/API object or exported payload path plus raw SHA-256;
- verification method, trusted issuer/signature/attestation, and verifier identity;
- result semantics matching the check's expected observable.

A screenshot, copied URL, local policy document, email summary, unchecked API result,
or model statement alone is not a verified external receipt. If external systems
cannot be queried or a receipt cannot be verified, keep the item UNKNOWN.

### Authorized owner attestation

Human quality, approval, legal interpretation, visual review, moderation readiness,
on-call briefing, and similar owner-controlled facts require:

- `Artifact Type: launch-owner-attestation`, schema and attestation ID;
- owner identity and role verified against the hash-bound attester registry;
- stable check IDs, release/candidate/build/platform scope;
- explicit statement and observed result;
- exact reviewed artifact/receipt paths and hashes;
- signed-at and valid-until/review timestamp;
- signature or trusted identity-verification receipt.

The workflow never creates, fills, or signs this artifact. A typed name, checkbox,
copied signature block, or attestation for an older build is invalid and leaves the
check UNKNOWN.

### Valid NOT_APPLICABLE evidence

`NOT_APPLICABLE` requires the manifest rule, owner authority, reason, exact scope,
timestamp, and verifiable attestation. An absent file or unsupported platform is not
automatically N/A.

## Phase 4: Consume canonical staged release evidence

Use only exact paths/hashes declared by the launch manifest. Re-hash every referenced
artifact and its transitive evidence. Do not accept protocols, plans, selection
manifests alone, conversation output, legacy locations, or newest-file guesses.

### Smoke

Accept only:

`production/qa/evidence/smoke/<candidate-id>/<run-id>/report.md`

Require `Artifact Type: smoke-check-receipt`, schema version, exact candidate-manifest
path/hash and build binding, persisted sprint mode, `Verdict: PASS`,
`Handoff Eligible: YES`, current QA-plan effective state, test-manifest/scope hashes,
automated receipt/log/manual evidence hashes, and successful read-back/persistence.
Quick, targeted, incomplete, failed, warning-bearing, stale, or unpersisted smoke
evidence cannot pass launch readiness.

### Regression

Require both:

1. the exact current `tests/regression-suite.md` selection manifest with current
   QA-plan/requirement/test-source hashes, stable AC/BUG mappings, and
   failure-sensitivity evidence; and
2. a matching build-bound execution receipt that names the exact selection-manifest
   hash, candidate build/commit, runner/config hash, every selected stable test ID,
   per-test result/duration/source hash/mapping, omissions/skips/quarantines/crashes,
   and receipt hash/signature.

`Coverage: VERIFIED COVERAGE` requires current eligible mappings plus a passing
matching receipt. `GAPS FOUND`, `CRITICAL GAPS`, `AWAITING RUN`, `STALE`,
`INDETERMINATE`, or selection without execution cannot pass.

### Soak

Accept only:

`production/qa/soak-tests/<run-id>/result.md`

Require `Artifact Type: soak-test-result`, schema version, `Status: COMPLETED`, exact
candidate/build/source/workload/environment/platform/observer binding, protocol,
manifest, receipt/raw-set/sample-set/result hashes, and `Gate Eligible: YES`.

For positive launch evidence require `Execution Status: EXECUTED`,
`Readiness Result: PASS`, and every launch-policy-required objective dimension PASS.
`FAILED_EARLY` or a dimension/readiness FAIL is a HARD failure. `INCOMPLETE`,
`INCONCLUSIVE`, `NOT_IN_SCOPE` for a required dimension, or gate-ineligible evidence
is UNKNOWN/incomplete, never PASS. Soak duration comes from the manifest's risk
profile and protocol rationale; do not impose a universal hour count.

### Playtest

Accept only:

`production/playtests/<session-id>/report.md`

Require `Artifact Type: playtest-session-result`, schema version,
`Status: COMPLETED`, `Gate Eligible: YES`, matching candidate build/version/source/
platform/hypothesis or AC IDs, evidence receipt ID, raw evidence, manifest,
observation-ledger and report hashes, and resolvable finding-to-observation links.
A protocol, IN_PROGRESS manifest, director review, legacy report, or session for
another build cannot pass.

### Test-evidence review

Accept only an explicitly declared persisted report at:

`production/qa/evidence/reviews/<review-id>/report.md`

Require `Artifact Type: test-evidence-review-report`, exact candidate/review-manifest/
QA-plan/smoke/playtest/test-source/artifact/attestation hashes,
`Workflow Status: COMPLETE`, `Overall Evidence Quality: ADEQUATE`,
`Overall Execution Status: PASS`, required full execution scope, and
`Closure Eligible: YES`. A conversation-only, targeted-only, incomplete, stale,
unknown, unavailable, nonpersisted, or hash-mismatched review cannot pass.

## Phase 5: Validate recovery and operational evidence

A rollback, restore, hotfix, failover, or go-live procedure cannot pass because a plan
exists. Require a current rehearsal receipt with:

- `Artifact Type: recovery-rehearsal-receipt`, schema and rehearsal ID;
- exact release/candidate/build and production-equivalent environment identity;
- procedure/runbook path/hash, owner and participants;
- start/end timestamps, injected condition, executed steps, logs and artifact hashes;
- declared RTO/RPO or hotfix objective and measured result;
- rollback/restore/data-integrity validation;
- outcome `PASS` or `FAIL`, unresolved findings, and signed receipt/hash.

A verified failed rehearsal is a HARD `FAIL`. Missing, plan-only, stale, partial, or
unverified rehearsal evidence is `UNKNOWN` for a required check and therefore blocks
readiness.

## Phase 6: Derive per-check and aggregate results

For each stable check output:

| Check ID | Domain | Gate Class | Applicability | Expected Observable | Evidence Type | Evidence Path/Receipt | Declared/Observed Hash | Evidence Status | Check Status | Owner | Freshness | Reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Map deterministically:

- `PASS`: verified current evidence proves the expected observable;
- `FAIL`: verified current evidence proves a blocking/noncompliant result;
- `UNKNOWN`: evidence is absent, manual-required, nonconclusive, or insufficient;
- `STALE`: readable binding/hash/scope no longer matches;
- `UNAVAILABLE`: declared evidence cannot be read, parsed, decoded, or verified;
- `NOT_APPLICABLE`: valid applicability attestation verifies.

Do not replace UNKNOWN with a guess, old result, assumed default, or user optimism.
Compute the readiness verdict only after all rows and load counters exist.

Any prior assessment is comparison context only. Load it only from the exact
path/hash in the launch manifest. Compare stable IDs and show resolved, regressed,
unchanged, added, and removed items. Current evidence alone determines the verdict.
A build/candidate/hash change makes old build-bound attestations and receipts stale.

## Phase 7: Present, optionally persist, and stop

The report includes:

1. simulation watermark when applicable;
2. manifest/release/candidate/build/platform identity and hashes;
3. workflow/coverage/readiness/persistence/decision fields;
4. source load counters and evidence snapshot hash;
5. every stable check row;
6. canonical smoke/regression/soak/playtest/test-evidence validation;
7. external receipt and owner-attestation verification;
8. recovery rehearsal results;
9. hard blockers, advisory concerns, unknown/manual/stale/unavailable items;
10. stable-ID delta against an explicitly supplied prior assessment;
11. evidence limitations and exact owning role/next evidence required.

For `assess --persist`, use only the immutable canonical assessment path. Re-hash all
inputs immediately before writing; any change invalidates the candidate report.
Write one report, re-read it, verify internal references, and display its SHA-256.
Declined or failed persistence never changes the observed readiness verdict but makes
the report itself non-durable.

For nonpersisted assessment, return `Persistence: NOT_REQUESTED`. For dry-run, return
`Persistence: SIMULATION`, no path/hash, no sign-offs, `Readiness Verdict:
UNDETERMINED`, and a clearly labeled simulation projection.

Always return `Launch Decision: NOT_RECORDED`. Suggest exact missing evidence owners,
but do not invoke `$gate-check`, `$team-release`, release publication, certification,
store, infrastructure, or communication actions. The user or separately authorized
launch gate owns the final decision.
