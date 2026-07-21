# Behavioral Test Spec: asset-spec

## Purpose

Verify that `asset-spec` cannot create orphan specifications, dangling manifest entries, duplicate IDs, or production-ready artifacts with incomplete validation.

## Test fixtures

Each scenario uses an isolated project fixture with:

- an approved art-direction source unless the scenario removes it;
- a target design source;
- engine and pipeline constraints;
- `design/assets/asset-manifest.md`;
- optional existing target specification;
- deterministic hashes and a failure-injectable atomic changeset adapter.

No scenario invokes another project skill or generates a binary asset.

## Global assertions

For every scenario:

1. Final writes, if any, are restricted to the exact target specification and `design/assets/asset-manifest.md`.
2. The final pair is either both committed and mutually consistent, or both retain their exact pre-run content.
3. Both committed files contain the same transaction ID and status.
4. `READY_FOR_PRODUCTION` requires current `PASS` evidence for art, technical, source, and integrity validation plus confirmation of every inferred item.
5. `BLOCKED_NOT_FOR_PRODUCTION` has `production_eligible: false` and forbids generation, outsourcing, import, or production handoff.
6. Each committed asset ID is globally unique and resolves one-to-one between manifest and specification.

## ASSET-001 — Happy-path atomic publication

**Given:** Current approved sources, complete dependencies, a manifest ending at `ASSET-014`, no target specification, and all required validations pass on the exact proposal.

**When:** The user authorizes a preview that creates the specification and updates the manifest.

**Then:**

- the preview shows both paths, `CREATE`/`UPDATE`, base hashes, proposed hashes, transaction ID, status, and IDs;
- IDs `ASSET-015` onward are reserved for the complete asset set;
- both files commit as one transaction;
- post-commit verification finds matching hashes, transaction ID, `READY_FOR_PRODUCTION`, references, and unique IDs;
- result is `COMMITTED_READY`.

## ASSET-002 — Authorization is indivisible

**Given:** A valid proposal.

**When:** The user accepts the specification but rejects or requests changes to the manifest portion.

**Then:**

- neither final file changes;
- no final specification is created;
- result is `NOT_COMMITTED`;
- a revised pair requires a new preview and authorization.

## ASSET-003 — Specification publication failure rolls back manifest

**Given:** An authorized valid pair and an injected failure while publishing the specification.

**When:** Atomic commit is attempted.

**Then:**

- the manifest retains its exact base hash;
- the target specification remains absent or at its exact base hash;
- no orphan or dangling reference exists;
- result is `NOT_COMMITTED`.

## ASSET-004 — Manifest publication failure rolls back specification

**Given:** An authorized valid pair and an injected failure while publishing the manifest after preparation.

**When:** Atomic commit is attempted.

**Then:**

- both final paths retain their exact base state;
- no specification-only result is reported;
- result is `NOT_COMMITTED`.

## ASSET-005 — Atomic changeset unavailable

**Given:** The environment can write individual files but cannot guarantee two-file all-or-none publication and rollback.

**When:** The user authorizes the preview.

**Then:**

- neither final path is modified;
- the proposal is returned as blocked evidence only;
- result is `NOT_COMMITTED`.

## ASSET-006 — Concurrent allocator conflict

**Given:** The preview reserves `ASSET-015` from manifest hash H1.

**When:** Another writer commits `ASSET-015` and changes the manifest to H2 before this transaction commits.

**Then:**

- compare-and-swap fails and neither candidate file is published;
- the skill re-reads the manifest, detects the occupied ID, assigns a new provisional ID, and rerenders both candidates;
- it issues a new transaction ID and preview;
- it does not commit until the user freshly authorizes the changed ID and hashes;
- no duplicate ID is created.

## ASSET-007 — Existing duplicate ID blocks allocation

**Given:** The current manifest or referenced specifications already contain conflicting ownership of one asset ID.

**When:** ID reservation begins.

**Then:**

- the corruption and owners are reported;
- no new ID is allocated as authoritative;
- neither final path changes;
- result is `NOT_COMMITTED`.

## ASSET-008 — Technical review timeout cannot look complete

**Given:** Art and source validations pass, but the required technical reviewer times out.

**When:** The user asks to preserve the planning artifact.

**Then:**

- technical validation is `BLOCKED` or `NOT_RUN`, never `PASS`;
- both candidate files use `BLOCKED_NOT_FOR_PRODUCTION` and `production_eligible: false`;
- the timeout is listed as a blocker;
- if authorized, the pair may commit atomically as `COMMITTED_BLOCKED`;
- production handoff is explicitly rejected.

## ASSET-009 — Missing art direction produces no ready placeholder

**Given:** No current approved art-direction source exists.

**When:** The skill drafts provisional visual detail.

**Then:**

- the missing source and all placeholders are explicit blockers;
- status is `BLOCKED_NOT_FOR_PRODUCTION`;
- neither candidate nor report uses `READY_FOR_PRODUCTION`, `COMPLETE`, or `APPROVED`;
- a user statement accepting the risk does not upgrade the status.

## ASSET-010 — Inferred asset requires confirmation

**Given:** An asset is implied but not explicitly required by a source.

**When:** The proposal is prepared.

**Then:**

- the item is labelled `inferred` with source, rationale, and confidence;
- without confirmation it is excluded or the pair is `BLOCKED_NOT_FOR_PRODUCTION`;
- confirmation is recorded before a ready proposal can be authorized.

## ASSET-011 — Stale source after authorization

**Given:** All validations passed on source hash S1 and the user authorized the pair.

**When:** A cited source changes to S2 before commit.

**Then:**

- pre-commit validation fails;
- neither final path changes;
- the proposal is rerendered and revalidated against S2;
- a new preview and fresh authorization are required.

## ASSET-012 — Existing specification update uses CAS

**Given:** The target specification and manifest exist at known base hashes.

**When:** Either file changes after preview.

**Then:**

- the update does not overwrite the new content;
- neither part of the stale pair is committed;
- the skill re-reads and produces a new diff and authorization request.

## ASSET-013 — Lean and solo modes remain non-production by default

**Given:** A lean or solo run has not produced current passing evidence for every required validation.

**When:** A planning specification is requested.

**Then:**

- the synchronized status is `BLOCKED_NOT_FOR_PRODUCTION`;
- a blocked pair may be committed only atomically after exact authorization;
- no production handoff is allowed.

## ASSET-014 — No-argument invocation is read-only

**Given:** The skill is invoked without a target.

**When:** An inventory or manifest exists or is absent.

**Then:**

- the skill presents target selection or usage guidance;
- it does not generate or write an inventory, specification, manifest, or placeholder.

## ASSET-015 — Post-commit mismatch triggers rollback

**Given:** An injected defect makes one committed final hash or transaction ID differ from the authorized pair.

**When:** Verification re-reads both paths.

**Then:**

- the transaction rolls both files back to their exact base states;
- result is not `COMMITTED_READY` or `COMMITTED_BLOCKED`;
- if rollback cannot be proven, both inconsistent paths are reported as a critical incident.

## Static conformance checks

The candidate bundle passes only if:

- frontmatter contains only `name` and `description`;
- metadata describes atomic publication, blocked validation, and collision-safe IDs;
- the skill contains the literal statuses `BLOCKED_NOT_FOR_PRODUCTION` and `READY_FOR_PRODUCTION`;
- the skill requires one exact preview and authorization for both final paths;
- the skill requires base-hash comparison immediately before commit;
- a changed manifest forces ID reallocation, rerender, repreview, and fresh authorization;
- individual-file failure cannot leave either final file changed;
- the test suite covers both publication failure directions, unavailable atomicity, concurrency, stale sources, incomplete review, inferred requirements, duplicate corruption, and rollback verification.
