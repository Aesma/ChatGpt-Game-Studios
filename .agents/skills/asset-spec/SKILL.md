---
name: asset-spec
description: Generate provenance-bound per-asset production briefs from bounded sources, explicit or confirmed requirements, and finite art/technical review, then publish each specification with its manifest rows as one collision-safe transaction.
---

# Asset Spec

Create asset specifications without orphan specs, dangling manifest rows, duplicate IDs, hidden inferred requirements, unsafe reuse, path collisions, or incomplete validation appearing production-ready. This workflow does not generate binary assets, invoke another project workflow, or grant production approval on behalf of a reviewer.

## Invocation

```text
$asset-spec --manifest <asset-spec-request-path> --expect-manifest <sha256:...>
```

Both arguments are required exactly once. With no manifest, show usage and stop with zero project-source reads, reviewers, writes, or verdict. Reject unknown/repeated flags, missing values, directories, moving aliases such as `latest`, malformed hashes, traversal, symlink/junction/reparse escape, schema mismatch, and expected/actual hash mismatch.

The request conforms to `cgs.asset-spec-request/v2` and includes:

- stable request/run/target IDs, target display name, asset-spec intent, and exact approved content scope;
- exact source inventory with normalized path, expected SHA-256/size/type, stable locator set, inclusion reason, priority, and sensitivity class;
- expected asset-manifest path/hash or ABSENT, optional exact existing target-spec path/hash, and proposed target ownership;
- canonical global review-mode source path/expected SHA-256/schema;
- engine, asset-pipeline, target platform/configuration, performance/memory, and packaging constraints with source IDs;
- asset reuse candidates with exact manifest/spec/license/source hashes;
- source/reviewer/regeneration/time/byte budgets that may only lower hard ceilings;
- output owner, manifest owner, evidence recorder, unique writers, transaction adapter/rollback policy, and explicit non-writes.

The manifest is a scope request, not evidence that an asset is required, confirmation of an inference, approval of reuse/license, reviewer validation, or file-write authorization.

## Atomic status and authority boundary

The target specification and `design/assets/asset-manifest.md` form one two-file transaction. They publish together with identical transaction ID/status, or neither final path changes.

Statuses are exactly:

- `DRAFT` — uncommitted candidate; no production use;
- `BLOCKED_NOT_FOR_PRODUCTION` — missing/failed/timed-out/skipped/stale/conflicting source, confirmation, review, reuse, license, platform, path, or integrity evidence; generation, outsourcing, purchase, import, production handoff, and release consumers must reject it;
- `READY_FOR_PRODUCTION` — every required check is current PASS on the exact authorized bytes, all included inferred requirements are explicitly confirmed, and the atomic commit/read-back is verified.

`production_eligible` is false except for a verified committed READY pair. Risk acceptance cannot turn blocked/unknown evidence into READY. Never substitute COMPLETE/APPROVED for READY_FOR_PRODUCTION.

There are separate user decisions for inferred-requirement confirmation, conflict resolution, reuse approval, candidate content approval, and exact transaction write authorization. None implies another.

## Bounded source contract — ASSET-P1-001

Read only individually declared regular project files. Do not scan “all available sources,” recurse a directory, follow an undeclared reference, read external/home/temp paths, or inspect secrets/configuration unrelated to the target.

Normalize project-relative paths to `/`, Unicode NFC, and case-preserving text. Resolve real paths and reject outside-root paths, symlinks/junctions/reparse points, special files, duplicate/case-colliding entries, declared/actual type-size-hash mismatch, and disallowed sensitivity classes.

Default hard ceilings per invocation:

| Resource | Ceiling |
|---|---:|
| request manifest bytes | 128 KiB |
| declared source entries | 64 |
| source body bytes per file | 256 KiB |
| total source body bytes | 1 MiB |
| stable locators evaluated | 256 |
| source-analysis elapsed time | 15 minutes |
| existing reuse candidates | 32 |

The effective value is `min(requested, hard ceiling)`. Unparseable/non-positive values are ERROR. Sort sources by `(priority, normalized_path, expected_hash)` and stop before the next read would exceed a ceiling.

For every omitted/unsupported entry record path, expected hash/size/type, locator scope, inclusion reason, and disposition `OMITTED_BUDGET | UNSUPPORTED_TYPE | SENSITIVITY_EXCLUDED | UNREADABLE | HASH_MISMATCH`. Never silently sample or claim omitted sources agree.

Sensitive sources default to excluded. Never read or persist credentials, tokens, private keys, `.env` content, personal participant data, or unrelated confidential material. A required excluded/unreadable/omitted source yields `BLOCKED_NOT_FOR_PRODUCTION`; if no trustworthy target source can be read, return ERROR and write nothing.

## Global review-mode contract — ASSET-P1-003

Review participation is governed only by the exact manifest-declared canonical global policy with schema `cgs.review-mode/v1`. Validate its path/hash, project identity, effective scope, mode, policy version, and owner. Do not infer mode from a local flag, reviewer availability, task phrasing, or current file contents outside that policy.

Accepted modes:

- `FULL` — independent art and technical reviews are both required;
- `LEAN` — policy-declared reduced reviewer participation is allowed for planning, but any missing required art/technical validation remains blocked;
- `SOLO` — no external reviewer is assumed; the output remains blocked unless independent current evidence satisfies every production check.

Missing, invalid, stale, ambiguous, or conflicting global policy returns BLOCKED before reviewer calls. A user cannot override it inside this run; the policy owner must change it separately. Review mode changes participation only and never weakens READY requirements.

## Requirement provenance and confirmations — ASSET-P1-002/006

Build a requirement ledger before drafting. Every entry conforms to `cgs.asset-requirement/v1` and has stable requirement ID plus exactly one origin:

- `EXPLICIT_SOURCE` — the source directly requires the asset/detail;
- `USER_STATED` — the user explicitly adds it in this run;
- `INFERRED_CANDIDATE` — the model/reviewer believes it follows from evidence but it is not stated;
- `REUSE_CANDIDATE` — an existing asset may satisfy some need subject to the reuse matrix.

Every entry records source path/SHA-256/bytes/type, exact heading/key/line-range locator, locator text hash, normalized claim, request/source snapshot hashes, rationale, confidence basis, affected asset keys, and confirmation state.

An inferred candidate is displayed separately from explicit requirements. It stays `origin: INFERRED_CANDIDATE` even after confirmation. Before inclusion in READY content, record one user response conforming to `cgs.asset-confirmation/v1`: exact question/options, exact answer `CONFIRM | REJECT | REVISE`, requirement IDs, displayed proposal hash, timestamp, and canonical record SHA-256. Silence, reviewer agreement, confidence, or content approval is not confirmation.

Unconfirmed inference must be excluded or keep the synchronized pair BLOCKED. Confirmation does not prove feasibility, license, reuse, or production approval.

Create `cgs.asset-spec-provenance/v1` containing:

- request path/schema/expected/actual hash and skill/metadata source hashes;
- target/project/run identity, normalized/collision keys, source inventory/snapshot and every included/omitted source disposition;
- global review-mode path/schema/version/hash;
- every requirement/confirmation ID and source locator/hash;
- engine/pipeline/platform source identities;
- art/technical reviewer role, exact agent/config/version identity, prompt/proposal/source hashes, attempt token, start/end, timeout/status, response hash, missing fields, and conflict IDs;
- regeneration round inputs/constraints/proposal/review hashes;
- reuse/license/variant/LOD/platform decisions and confirmation hashes;
- manifest/spec bases, provisional IDs, transaction/candidate hashes, owner/authorization IDs, and final read-back receipt when committed.

Timestamps and prose never replace exact hashes/locators.

## Canonical target path and collision contract — ASSET-P1-008

Derive a display slug from the target name using Unicode NFC, locale-independent case fold, ASCII transliteration where deterministic, replacement of non-alphanumeric runs by one `-`, trimming, and regex `^[a-z0-9]+(?:-[a-z0-9]+)*$`. The slug is 1–64 bytes.

Reject empty/ambiguous transliteration, leading/trailing dot/space, control characters, Windows-invalid characters, device/reserved names (`CON`, `PRN`, `AUX`, `NUL`, `COM1`–`COM9`, `LPT1`–`LPT9` case-insensitive), hidden segments, or a final normalized path beyond the project's cross-platform path-length ceiling.

Compute:

```text
target_key = sha256(project_id + "\n" + stable_target_id)
collision_key = Unicode-NFC + casefold + separator-normalized canonical relative path
new_spec_path = design/assets/specs/<slug>--<target_key8>-assets.md
```

The stable target-key suffix is mandatory for new specs. Before drafting, compare collision keys against the filesystem, manifest, and registered spec paths. If the exact path exists, it is an UPDATE only when its embedded stable target ID and manifest ownership match; otherwise return `PATH_COLLISION` and write nothing. Never add an ad hoc numeric suffix, overwrite a case variant, or reuse another target's path.

Existing legacy specs may be updated only through the exact manifest-bound path/base hash; do not silently rename/migrate them. Absolute paths and traversal are forbidden.

## Inventory and per-asset specification

Extract EXPLICIT_SOURCE and USER_STATED requirements first. Present INFERRED_CANDIDATE and REUSE_CANDIDATE items separately for confirmation/decision.

Each included asset defines stable asset key and provisional ID; asset type/use; visual description/silhouette/material/palette/scale; variants; dimensions/format/color space/transparency/compression; polygon/texture/bone/animation budgets; LOD chain and switching policy; target platform tiers; naming/destination; dependencies/companion assets; acceptance checks; prompts/negative constraints; and requirement/provenance IDs.

Do not generate a binary asset.

## Reuse decision matrix — ASSET-P1-007

Description similarity alone never establishes reuse. For each candidate, validate:

- existing asset ID/key/owner/status plus exact manifest/spec/source hashes;
- intended function/context, visual identity, variant/state/localization/accessibility needs;
- geometry/topology/scale/pivot/rig/skeleton/bone/animation/material/shader/texture compatibility;
- resolution, texture sets, LOD count/thresholds, impostor/collision/physics needs;
- per-platform format/compression/memory/performance/render-pipeline/import constraints;
- license/provenance source path/hash, rights holder, permitted use/modification/derivative/redistribution, attribution, territory/platform, expiry/version, AI-training/generation restrictions when stated, and downstream/outsourcing constraints;
- required modifications, derivative ownership, acceptance checks, dependencies, and cost/risk.

Classify exactly:

- `EXACT_REUSE` — no spec-affecting change and every constraint/license/platform check passes;
- `VARIANT_REUSE` — authorized variant under the same stable identity with explicit variant mapping and compatibility;
- `DERIVED_REUSE` — new asset identity is required and source/license permit the derivative;
- `NEW_ASSET` — reuse does not meet constraints;
- `REUSE_BLOCKED` — owner, source, license, LOD, platform, provenance, or compatibility evidence is missing/conflicting.

Reuse requires an exact user decision/confirmation plus owner authorization where declared. Unknown license or platform/LOD mismatch cannot be risk-accepted into READY. Never merge two existing asset IDs or replace manifest ownership because descriptions look similar.

## Bounded art and technical review — ASSET-P1-004

Reviewers are read-only and receive the exact proposal hash, source snapshot, review-mode hash, check IDs, and response schema `cgs.asset-review/v1`. They cannot edit candidates, approve publication, add confirmed requirements, or delegate.

Hard review ceilings:

- at most one art reviewer and one technical reviewer;
- at most two concurrent reviewer tasks;
- at most 10 minutes per attempt and 15 minutes total per round;
- one attempt per role per round; no automatic retry;
- no child delegation;
- response maximum 64 KiB per role.

Each response reports every assigned check ID as `PASS | BLOCKED | NOT_RUN`, exact finding/evidence/requirement IDs, proposal/source hashes, reviewer role/config/version, start/end, and limitations. Missing fields/checks, malformed schema, stale proposal hash, timeout, late response, or partial response is NOT_RUN/BLOCKED. Revoke timed-out attempt tokens; ignore/quarantine late results.

Build a conflict matrix for art-vs-technical, reviewer-vs-source, reviewer-vs-user-confirmation, and reviewer-vs-platform/license claims. Reviewers cannot override sources or confirmed user decisions. Present conflicts with options/tradeoffs to the user; a resolution creates a hash-bound decision record and a new proposal. Unresolved conflict blocks READY.

FULL requires both complete current reviews. LEAN/SOLO follow global participation rules but cannot mark absent required validation PASS.

## Finite regeneration — ASSET-P1-005

Allow at most two regeneration rounds after the initial candidate. Counters are monotonic and stored in provenance.

Each regenerate request must introduce at least one hash-bound new input:

- user-confirmed new/revised constraint;
- changed authoritative source with new hash/locator;
- explicit conflict-resolution decision;
- corrected technical/platform/license evidence.

“Try again,” reviewer dissatisfaction without a new constraint, or an unchanged prompt is insufficient. Record exact delta and affected requirements; render a new proposal hash and rerun every affected source/reuse/art/technical/integrity check.

On round limit, timeout, or repeated unchanged proposal, stop reviewer/tool calls. Return the best current DRAFT/BLOCKED proposal with `REGENERATION_LIMIT_REACHED`; do not expand the limit or loop until approval.

## Collision-safe asset IDs and validations

Required checks for the exact candidate:

- source/provenance and confirmations;
- art consistency/readability;
- technical engine/import/budget/format/dependency/platform/LOD constraints;
- reuse/license/ownership;
- global review policy/reviewer completeness;
- path/slug/collision safety;
- manifest/spec/asset-key/ID/status/transaction integrity.

Each validation is PASS/BLOCKED/NOT_RUN with evidence hash/time. Any non-PASS required check yields BLOCKED_NOT_FOR_PRODUCTION.

Preserve `ASSET-NNN` only with manifest CAS:

1. read current manifest and referenced IDs needed for global uniqueness;
2. detect existing duplicate/malformed ownership and stop;
3. record manifest and target-spec base hashes;
4. allocate contiguous provisional IDs inside this transaction;
5. render both files with one transaction ID/status/provenance hash;
6. immediately before commit rehash sources, policy, confirmation/reviews, reuse/license evidence, manifest/spec bases, path collision set, IDs, and candidates;
7. any drift publishes nothing, reallocates/rerenders when necessary, creates a new transaction/preview, and requires fresh authorization;
8. never silently change an authorized ID/path/status.

## Exact preview and atomic commit

Show one indivisible preview with transaction ID, exact spec/manifest paths, CREATE/UPDATE operations, owner/writer, base hash/ABSENT, full candidate hash, provisional IDs, synchronized status, provenance hash, validation/blocker matrix, rollback plan, and complete content/diff sufficient for informed review.

Ask once for that exact two-file authorization. Declining/changing either part commits neither. Any content/ID/path/status/base/blocker/evidence/owner change invalidates approval.

After authorization, revalidate every bound hash and collision. Prepare complete candidates in isolated non-final siblings and validate as a pair. Use an all-or-none transaction with exact rollback; if unavailable, write neither. Never leave one final file and promise repair.

Read back both paths and require authorized hashes, same transaction/status/provenance, one-to-one rows/spec assets, global ID uniqueness, exact target ownership/path, and READY only with all PASS. Failure rolls both back. Unproven rollback reports a critical incident with exact divergent paths/hashes and never claims commit success.

## Required fields and completion

Specification includes target/stable target ID/slug/collision key/transaction; status/production eligibility; source/provenance/requirement/confirmation tables; review mode/reviewer receipts/conflicts/regeneration history; reuse/license/LOD/platform matrix; validation/blocker matrix; asset key-ID table; detailed requirements/acceptance/prompts/dependencies/destinations; and history.

Manifest rows include asset ID/key/target ID/spec path/type/status/transaction/provenance hash/dependency state/reuse classification/platform/LOD/license state.

Return exactly one:

- `COMMITTED_READY` — verified atomic READY pair;
- `COMMITTED_BLOCKED` — verified atomic blocked pair, explicitly non-production;
- `NOT_COMMITTED` — declined/stale/conflicted/collision/atomicity/preparation/rollback-restored outcome;
- `CRITICAL_INCONSISTENCY` — rollback could not restore/prove both bases.

Report both final paths/hashes when committed, IDs, source/review/reuse/provenance evidence, omissions/blockers, regeneration count, collision retry, production-handoff permission, and `auto_executed: false`. Never claim success from a preview, one-file write, unverified pair, partial source/reviewer response, or inferred requirement without confirmation.
