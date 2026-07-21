---
name: asset-spec
description: Generate traceable per-asset visual specifications and AI prompts, then publish each specification together with its master-manifest entries as one collision-safe transaction. Use for production asset briefs; incomplete validation is always marked non-production.
---

# Asset Spec

Create implementation-ready asset specifications without allowing an orphan specification, a dangling manifest entry, a duplicate asset ID, or an incompletely validated artifact to appear production-ready.

This workflow specifies assets. It does not generate image/audio/model files, invoke another project skill, or claim approval from any role.

## Invocation

`$asset-spec <target>`

`<target>` is an exact entity, system, level, screen, or approved content scope.

When no target is supplied:

1. Read an existing entity inventory and asset manifest, if available.
2. Present a read-only target selection or usage guidance.
3. Do not create an inventory, specification, manifest, or placeholder.

## Non-negotiable invariants

1. **Atomic publication:** the target specification and `design/assets/asset-manifest.md` are one changeset. A run may publish both or neither. Never expose a specification without its manifest rows, or manifest rows without their specification.
2. **No false readiness:** any missing, failed, timed-out, skipped, stale, or contradictory required validation forces `BLOCKED_NOT_FOR_PRODUCTION`. User acceptance of risk cannot convert that state to production-ready.
3. **Collision-safe IDs:** `ASSET-NNN` IDs are provisional until a compare-and-swap commit against the current manifest succeeds. A changed manifest requires reallocation, rerendering, a new preview, and fresh authorization.
4. **No silent inference:** every inferred asset or requirement is visibly labelled `inferred` and must be confirmed by the user. Unconfirmed inferences cannot be production-ready.
5. **No unilateral overwrite:** an existing specification may be updated only when its exact path and replacement are shown in the transaction preview.

## Status contract

Every specification and each of its manifest rows carries the same status and transaction ID.

| Status | Meaning | Downstream use |
|---|---|---|
| `DRAFT` | Proposal has not completed authorization and commit | No production use |
| `BLOCKED_NOT_FOR_PRODUCTION` | One or more required validations or confirmations are not current and passing | Planning only; asset generation, outsourcing, import, and production handoff must reject it |
| `READY_FOR_PRODUCTION` | All required validations pass on the exact proposed content, all inferred items are confirmed, the user authorized the exact transaction, and commit verification succeeded | Production handoff allowed |

Never use `COMPLETE`, `APPROVED`, or similar wording as a substitute for `READY_FOR_PRODUCTION`.

## Required inputs and provenance

Read only the sources needed for the target:

- approved art direction or art bible;
- target GDD, UX, level, character, narrative, or architecture sources;
- engine and asset-pipeline constraints;
- the current `design/assets/asset-manifest.md`;
- the existing target specification, if updating one.

For every source, record:

- normalized project-relative path;
- content hash captured at draft time;
- requirement locator such as heading, entity key, or line anchor;
- whether each requirement is `explicit` or `inferred`;
- confidence and user confirmation for inferred requirements.

A missing authoritative source is a blocker, not permission to invent production-ready detail. Proposed placeholders may appear only under `BLOCKED_NOT_FOR_PRODUCTION` and must be listed as blockers.

## Workflow

### 1. Fix the transaction boundary

Resolve and display the two final paths before drafting:

- `design/assets/specs/<target-slug>-assets.md`
- `design/assets/asset-manifest.md`

Reject absolute paths, parent traversal, paths outside the project, or a target slug that normalizes ambiguously. Detect whether the specification path is new or an explicit update. Capture the current content hash of each existing final file, or `ABSENT`.

Do not write final files during discovery, inventory, drafting, review, or preview.

### 2. Build and confirm the asset inventory

Extract explicit assets first. Present inferred assets separately with their source, rationale, and confidence. Ask the user to confirm, exclude, or revise each inferred item before it can become production-ready.

For each included asset, define:

- stable asset key and provisional ID;
- asset type and intended use;
- visual description, silhouette, material, palette, scale, and variants as applicable;
- dimensions, format, color space, transparency, compression, polygon/texture/bone budgets, and platform constraints as applicable;
- naming convention and destination path;
- dependencies and required companion assets;
- acceptance checks;
- generation prompt plus negative constraints where useful;
- provenance records.

Do not generate binary assets.

### 3. Validate the exact proposal

Required production validations are:

- **Art validation:** consistency with the approved art direction, readable silhouette, palette/material rules, and target presentation.
- **Technical validation:** engine compatibility, import settings, budgets, formats, naming, dependency completeness, and target-platform constraints.
- **Source validation:** all cited hashes are current, all required sources exist, and all inferred requirements are confirmed.
- **Integrity validation:** manifest references, specification references, asset keys, IDs, statuses, and transaction metadata agree.

In full mode, request art and technical reviews of the exact rendered proposal. Reviewers advise; they do not approve or publish. Apply one consolidated revision round, then rerun every affected check.

Lean or solo mode may prepare a planning artifact, but it is `BLOCKED_NOT_FOR_PRODUCTION` unless current evidence independently satisfies every required validation.

Record each validation as `PASS`, `BLOCKED`, or `NOT_RUN`, with reviewer/evidence, content hash, and timestamp. A failure, timeout, unavailable reviewer, stale hash, unresolved conflict, missing dependency, placeholder, or `NOT_RUN` yields `BLOCKED_NOT_FOR_PRODUCTION`.

### 4. Reserve collision-safe IDs

Preserve the project format `ASSET-NNN` without trusting a stale `max + 1` calculation.

1. Read the current manifest and all referenced specification IDs needed to detect duplicates.
2. If existing duplicate IDs or malformed ownership are found, stop before publication and report the corruption.
3. Record the manifest base hash.
4. Allocate the next contiguous IDs only as provisional reservations inside this transaction.
5. Render both candidate files with the same transaction ID, status, and asset mappings.
6. Immediately before commit, compare the current manifest and target-spec hashes with their recorded base hashes.
7. If either changed, publish nothing. Re-read, recheck duplicates, reallocate IDs if necessary, rerender both candidates, issue a new transaction ID, show a new preview, and obtain fresh authorization. Never silently change an authorized ID.
8. The commit primitive must fail when its compare condition is no longer true.

### 5. Preview one exact changeset

Show a single transaction preview containing:

- transaction ID;
- both exact final paths;
- operation for each path: `CREATE` or `UPDATE`;
- base hash or `ABSENT`;
- proposed content hash;
- every reserved asset ID and asset key;
- synchronized status;
- blockers and missing validations;
- concise diffs or complete proposed content sufficient for informed review.

Ask once for authorization of this exact two-file changeset. If the user declines either file, publish neither. Any content, ID, path, status, blocker, or base-hash change invalidates the authorization and requires a new preview.

### 6. Commit atomically

After authorization:

1. Revalidate source hashes, dependency evidence, manifest/spec base hashes, ID uniqueness, status equality, cross-references, and proposed hashes.
2. Prepare both complete candidate files in isolated temporary siblings that are not visible as final project artifacts.
3. Validate the prepared pair as a unit.
4. Use an atomic changeset facility with rollback: publish both final files, or restore both exact pre-commit states on any error.
5. If the environment cannot guarantee all-or-none publication and rollback for these two paths, do not modify either final path. Return a blocked proposal instead.
6. Never handle a failure by leaving one final file committed and promising to repair the other later.

For a new specification, an unexpected file at the target path is a compare failure. For an update, a hash mismatch is a compare failure. Do not overwrite it.

### 7. Verify the committed pair

Re-read both final files and require:

- hashes equal the authorized proposed hashes;
- both contain the same transaction ID and status;
- every new/updated manifest row resolves to the target specification;
- every specified asset has exactly one matching manifest row;
- all IDs are globally unique;
- `READY_FOR_PRODUCTION` appears only when every required validation is current and `PASS`;
- no temporary or recovery artifact is presented as a final deliverable.

If verification fails, invoke transaction rollback. If rollback cannot be proven, report the exact inconsistent paths as a critical incident and do not claim completion.

## Required document fields

The specification must include:

- target and transaction ID;
- status and `production_eligible: true|false`;
- source provenance table with hashes and locators;
- validation matrix;
- blocker list;
- asset table mapping stable keys to IDs;
- detailed per-asset requirements and acceptance checks;
- prompts and negative constraints;
- dependency and destination mapping;
- change history.

The manifest entries must include at least:

- asset ID;
- stable asset key;
- target;
- specification path;
- asset type;
- status;
- transaction ID;
- dependency state.

## Completion report

Report:

- `COMMITTED_READY` only after verified atomic commit with `READY_FOR_PRODUCTION`;
- `COMMITTED_BLOCKED` only after a verified atomic commit whose two files both say `BLOCKED_NOT_FOR_PRODUCTION`;
- `NOT_COMMITTED` when authorization was declined, compare failed, atomicity was unavailable, preparation failed, or rollback restored the original pair;
- the two final paths and verified hashes when committed;
- reserved IDs;
- validation evidence and blockers;
- whether production handoff is allowed;
- any concurrency retry and the superseded transaction ID.

Never claim success from a draft, preview, single-file write, unverified pair, or partial validation.
