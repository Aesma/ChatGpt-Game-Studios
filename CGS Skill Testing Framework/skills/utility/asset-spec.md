# Contract Specification: `asset-spec`

## Purpose

Validate `asset-spec` as a bounded, provenance-preserving asset-brief workflow. It separates explicit requirements, user statements, inferred candidates, confirmations, and reuse candidates; performs finite policy-driven review; and publishes the exact specification with its manifest rows only as one collision-safe transaction.

## Contract identities

- Request: `cgs.asset-spec-request/v2`
- Requirement: `cgs.asset-requirement/v1`
- Confirmation: `cgs.asset-confirmation/v1`
- Global review mode: `cgs.review-mode/v1`
- Reviewer response: `cgs.asset-review/v1`
- Provenance: `cgs.asset-spec-provenance/v1`
- Skill: `.agents/skills/asset-spec/SKILL.md`
- Metadata: `.agents/skills/asset-spec/agents/openai.yaml`

## Invocation

```text
$asset-spec --manifest <request-path>
```

The manifest argument is required exactly once. No manifest prints usage and performs zero project-source reads, reviewer calls, writes, or verdict. Reject moving aliases, directories, traversal, symlink/junction/reparse escapes, unsupported schemas, and duplicate flags.

The request only proposes scope. It is not evidence that an asset is required, confirmation of inference, approval of reuse/license, validation, or file-write authorization.

## P0 invariants retained

1. Target specification and `design/assets/asset-manifest.md` publish in one all-or-none two-file transaction or both retain their exact bases.
2. Any missing/failed/timed-out/skipped/stale/conflicting required evidence forces `BLOCKED_NOT_FOR_PRODUCTION`, `production_eligible: false`, and downstream rejection.
3. `ASSET-NNN` IDs are provisional until manifest/target/source/evidence atomic conflict check and verified atomic commit; drift causes reallocation/rerender/new transaction/new preview/fresh authorization.
4. READY_FOR_PRODUCTION is legal only for a committed read-back verified pair with every required check current PASS.
5. Existing specifications cannot be overwritten without exact update preview/base revision; failed rollback is CRITICAL_INCONSISTENCY, never success.

## P1 requirements

### A. Bounded source inventory — ASSET-P1-001

1. Only individually declared regular repository-local files are readable. Directory recursion, all-source scans, undeclared references, external/home/temp paths, and symlink/reparse/special files are forbidden.
2. Paths normalize to `/`, NFC, case-preserving text and are checked for duplicates/case collisions, type/size/revision mismatch, sensitivity, and root escape.
3. Request budgets may lower but not raise: 128 KiB manifest, 64 sources, 256 KiB/source, 1 MiB total body bytes, 256 locators, 15 minutes analysis, and 32 reuse candidates.
4. Sources process deterministically by priority/path and stop before exceeding a ceiling.
5. Every omitted entry records identity/locator/reason as `OMITTED_BUDGET`, `UNSUPPORTED_TYPE`, `SENSITIVITY_EXCLUDED`, `UNREADABLE`, or `SOURCE_CHANGED`.
6. No silent sample or omitted-scope agreement claim exists. Required omission blocks production; zero trustworthy target sources is ERROR and no write.
7. Credentials, tokens, keys, `.env` contents, unrelated confidential data, and personal data are never read/persisted.

### B. Explicit versus inferred assets and confirmation — ASSET-P1-002

1. Every requirement is `cgs.asset-requirement/v1` with exactly one origin: `EXPLICIT_SOURCE`, `USER_STATED`, `INFERRED_CANDIDATE`, or `REUSE_CANDIDATE`.
2. Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
3. Explicit requirements are extracted first; inferred/reuse candidates are displayed separately.
4. Inference retains `origin: INFERRED_CANDIDATE` after confirmation and never becomes source-explicit.
5. Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
6. Silence, confidence, reviewer agreement, content approval, or write approval is not confirmation.
7. Unconfirmed inference is excluded or keeps both files BLOCKED; confirmation does not prove feasibility/license/reuse/readiness.

### C. Canonical global review mode — ASSET-P1-003

1. Reviewer participation comes only from an exact versioned `cgs.review-mode/v1` global policy with project identity, version, owner, scope, and mode.
2. Local flags, task wording, reviewer availability, or skill defaults cannot select/override mode.
3. FULL requires art and technical reviews. LEAN/SOLO follow only policy-declared participation and cannot turn absent required validation into PASS.
4. Missing/invalid/stale/ambiguous/conflicting policy blocks before reviewer calls.
5. Review mode affects participation only; READY requirements never weaken.
6. Any policy change belongs to its owner and a separate transaction.

### D. Bounded art/technical reviewers and conflicts — ASSET-P1-004

1. Reviewers are read-only, receive exact proposal/source/policy/check revisions and `cgs.asset-review/v1`, cannot edit/publish/confirm requirements/delegate.
2. Hard ceilings: one art + one technical reviewer, two concurrent tasks, 10 minutes/attempt, 15 minutes/round, one attempt/role/round, zero child delegation, 64 KiB/response.
3. Every assigned check is PASS/BLOCKED/NOT_RUN with evidence/requirement IDs and exact proposal/source/reviewer config/version/timing/response revision.
4. Missing/malformed/stale/partial/timeout/late response is NOT_RUN/BLOCKED; late attempt tokens are revoked/quarantined.
5. Conflict matrix covers art-vs-technical, reviewer-vs-source, reviewer-vs-confirmation, and reviewer-vs-platform/license.
6. Reviewers cannot override sources/user confirmations. User sees options/tradeoffs; a resolution is a revision-bound decision and new proposal. Unresolved conflict blocks READY.

### E. Finite regeneration — ASSET-P1-005

1. At most two regeneration rounds follow the initial candidate; counters are monotonic in provenance.
2. Each round requires at least one new revision-bound accepted input: revised confirmed constraint, changed authoritative source, explicit conflict resolution, or corrected technical/platform/license evidence.
3. “Try again,” unchanged prompt, or dissatisfaction without a constraint cannot start a round.
4. Each round records delta/affected requirements/new proposal revision and reruns every affected check.
5. Limit, timeout, or unchanged proposal stops reviewer/tool calls and returns current DRAFT/BLOCKED with `REGENERATION_LIMIT_REACHED`; no in-place expansion or until-approved loop.

### F. Source/reviewer/transaction provenance — ASSET-P1-006

`cgs.asset-spec-provenance/v1` contains:

1. Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
2. target/project/run IDs, slug/path collision keys, source inventory/snapshot and every included/omitted disposition;
3. global review-mode path/schema/version/revision;
4. Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
5. engine/pipeline/platform source identities;
6. reviewer role and exact agent/config/version, prompt/proposal/source revisions, attempt token/times/status/response/missing fields/conflicts;
7. every regeneration input/delta/proposal/review revision;
8. reuse/license/variant/LOD/platform decisions and confirmations;
9. manifest/spec bases, provisional IDs, transaction/candidate revisions, owners/authorizations, rollback/read-back receipt.

No timestamp, role name, or prose substitutes for source/reviewer/content revisions and locators.

### G. Reuse authorization, license, variant, LOD and platform constraints — ASSET-P1-007

1. Description similarity alone cannot establish reuse or merge IDs.
2. Candidate matrix binds existing ID/key/owner/status/manifest/spec/source revisions and compares function, visual identity, variants/states/localization/accessibility, geometry/topology/scale/pivot/rig/skeleton/bones/animation/material/shader/textures.
3. It also compares resolution/texture sets/LOD chain/thresholds/impostor/collision/physics, platform formats/compression/memory/performance/render/import, modifications/dependencies/acceptance.
4. License/provenance binds source/revision, rights holder, permitted use/modification/derivative/redistribution, attribution, territory/platform, expiry/version, AI restrictions when stated, and outsourcing/downstream constraints.
5. Classification is exactly `EXACT_REUSE`, `VARIANT_REUSE`, `DERIVED_REUSE`, `NEW_ASSET`, or `REUSE_BLOCKED`.
6. User reuse decision/confirmation and declared owner authorization are required. Unknown license, missing provenance, or LOD/platform mismatch cannot be risk-accepted into READY.
7. VARIANT_REUSE needs explicit variant mapping. DERIVED_REUSE receives a new asset identity and requires derivative rights. Existing IDs are never merged by similarity.

### H. Cross-platform slug/path collision safety — ASSET-P1-008

1. Slug uses NFC, locale-independent case fold, deterministic ASCII transliteration, collapsed hyphens, regex `^[a-z0-9]+(?:-[a-z0-9]+)*$`, and 1–64 bytes.
2. Empty/ambiguous transliteration, control/invalid characters, dot/space endings, hidden segments, overlong paths, and reserved device names are rejected.
3. Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
4. Collision key uses NFC + case fold + separator normalization and is checked against filesystem, manifest, and registered specs before drafting and commit.
5. Existing exact path is UPDATE only when embedded stable target ID and manifest owner match. Otherwise PATH_COLLISION and zero writes.
6. No ad hoc suffix, case-variant overwrite, or reuse of another target path. Legacy specs update only at exact manifest-bound path/base revision and are not silently renamed.

## Review/readiness and ID contract

Every exact candidate has source/confirmation, art, technical, engine/import/budget/format/dependency/platform/LOD, reuse/license/ownership, policy/reviewer, path/collision, and manifest/spec/integrity checks. Each is PASS/BLOCKED/NOT_RUN with evidence revision/time. Any required non-PASS means BLOCKED_NOT_FOR_PRODUCTION.

Asset IDs preserve `ASSET-NNN` only through current manifest/reference duplicate audit, provisional in-transaction reservation, exact bases, same transaction/status/provenance rendering, immediate precommit atomic conflict check, and full rerender/repreview/fresh authorization after drift. Existing duplicate/malformed ownership stops allocation.

## Atomic write contract

One indivisible preview shows transaction ID, exact spec/manifest paths, CREATE/UPDATE, owner/writer, bases/ABSENT, candidate revisions, IDs, status, provenance, blockers/validation, rollback plan, and full content/diff.

One exact authorization covers both or neither. Any content/ID/path/status/base/blocker/evidence/owner change invalidates it.

After authorization, re-read all sources/policy/confirmations/reviews/reuse/license/paths/bases/IDs/candidates. Prepare non-final siblings and validate the pair. If all-or-none commit+rollback cannot be guaranteed, modify neither.

Read-back requires authorized revisions, matching transaction/status/provenance, one-to-one manifest/spec mappings, global unique IDs, correct target ownership/path, and READY only on all PASS. Failure restores both bases. Unproven rollback is CRITICAL_INCONSISTENCY.

## Behavioral cases

### Case 1 — Source budget

Exact inventory exceeds 64 entries/1 MiB. Processing stops before excess reads, lists every omitted entry/reason, and any required omission yields blocked non-production pair or no trustworthy-output ERROR. No recursive expansion occurs.

### Case 2 — Explicit and inferred requirement

Source explicitly requires a hero portrait; model infers damage-state variants. Portrait is EXPLICIT_SOURCE. Variants remain INFERRED_CANDIDATE with rationale/confidence and cannot enter READY until an exact confirmation record exists.

### Case 3 — Local full flag conflicts with global SOLO

Local request cannot override global policy. SOLO is recorded, no unauthorized reviewer calls occur, and missing independent art/technical evidence keeps the pair BLOCKED.

### Case 4 — Technical timeout and reviewer conflict

Art response passes; technical task times out and later returns. Timeout is NOT_RUN/BLOCKED, late response quarantined. If art and source conflict, user receives a conflict matrix; no agent silently resolves it.

### Case 5 — Regenerate loop

First revision has one confirmed constraint; second has a license correction. Third “try again” request is refused with REGENERATION_LIMIT_REACHED and no reviewer/tool call.

### Case 6 — Provenance drift

Source or reviewer config changes after authorization. Precommit atomic conflict check fails, neither final file changes, provenance/candidate are rebuilt, and a new preview/authorization is required.

### Case 7 — Similar asset cannot be reused

Description matches an existing mesh, but license lacks derivative rights and mobile LOD/memory requirements fail. Classification is REUSE_BLOCKED or NEW_ASSET; IDs are not merged and READY is impossible on that reuse decision.

### Case 8 — Slug collision

Two Unicode/case variants normalize to the same display slug. Stable target-key paths differ deterministically. An existing path owned by another target yields PATH_COLLISION; no numeric suffix or overwrite occurs.

### Case 9 — P0 atomic/ID/readiness regression

Rejecting manifest portion writes neither file. Manifest atomic conflict check conflict reallocates/rerenders/repreviews. Reviewer missing means BLOCKED_NOT_FOR_PRODUCTION. Single-file publication failure restores both bases.

## Negative assertions

Any is a contract failure:

- all-source/unbounded scan or reading omitted/sensitive/undeclared content;
- inferred requirement treated as explicit/confirmed;
- local review mode overriding canonical global policy;
- unbounded reviewer, retry, child delegation, late response acceptance, or agent-resolved conflict;
- regenerate without new constraint or beyond two rounds;
- missing source/reviewer/config/content revisions and locators;
- reuse based only on text similarity or with unknown license/LOD/platform fit;
- raw slug path, reserved/invalid/case-colliding path, silent suffix, or foreign-target overwrite;
- READY with any required non-PASS;
- non-atomic spec/manifest publication or stale ID commit.

## Remediation traceability

| Finding | Closure evidence |
|---|---|
| ASSET-P1-001 | Section A defines exact inventory, hard file/byte/time/locator budgets, sensitivity exclusions and omissions |
| ASSET-P1-002 | Section B preserves explicit/user/inferred/reuse origins and requires exact confirmation records |
| ASSET-P1-003 | Section C consumes only versioned global review policy and forbids local overrides |
| ASSET-P1-004 | Section D bounds reviewers/time/response/delegation and defines partial/late/conflict terminals |
| ASSET-P1-005 | Section E caps regeneration at two new-constraint rounds |
| ASSET-P1-006 | Section F defines full source/reviewer/policy/regeneration/reuse/transaction provenance |
| ASSET-P1-007 | Section G gates reuse on owner/license/variant/LOD/platform/provenance constraints |
| ASSET-P1-008 | Section H defines normalized target-key paths, reserved names, collision keys, ownership and atomic conflict check |

## Outcomes

Return `COMMITTED_READY`, `COMMITTED_BLOCKED`, `NOT_COMMITTED`, or `CRITICAL_INCONSISTENCY` with both paths/revisions when committed, IDs, source/review/reuse/provenance evidence, omissions/blockers, regeneration count, collision retry, production-handoff permission, and `auto_executed: false`.

## Path-first integrity regression

1. Invoke the skill with canonical project-relative paths and no caller-supplied content-derived token.
2. Verify that schema versions, stable IDs, permissions, lifecycle state, and path or ID collisions remain enforced.
3. Verify that generated IDs are allocated independently of file bytes.
4. For a permitted mutation, change a declared revision or target state after preview and verify that the atomic conflict check stops the write.
5. Verify that an authorized unchanged candidate is staged beside the target, atomically replaced, re-read, and rolled back on failure.
