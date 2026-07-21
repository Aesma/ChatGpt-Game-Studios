---
name: architecture-review
description: "Runs a hash-bound, read-only architecture and ADR traceability gate over explicit owner-approved requirements, exact evidence links, engine constraints, and current test-run evidence; returns PASS, BLOCKED, or PARTIAL without modifying project truth sources."
---

## Invocation and public contract

Invoke this workflow as $architecture-review.

Arguments:

- no argument or full — traceability, conflicts, dependency order, engine checks, and current implementation/test evidence when present
- coverage — explicit requirement-to-ADR coverage only
- consistency — cross-ADR conflicts and dependency validity only
- engine — engine-version and API compatibility only
- single-gdd path/to/gdd.md — coverage for one canonical project-relative GDD path
- rtm — full explicit Requirement → ADR → Story → Test Run chain

Unknown modes or ambiguous targets are errors and produce no gate verdict.
single-gdd accepts one existing canonical project-relative path, not a title or
fuzzy name. This workflow does not grade architecture.md against an eight-section
document template; that is a separate document-review concern.

This is a formal, hash-bound gate. Its only verdicts are exactly PASS, BLOCKED,
and PARTIAL. It is read-only by default. It may optionally create one immutable
review report at an exact user-authorized path, but it never changes requirements,
GDDs, ADRs, registries, indexes, stories, tests, test results, signoff, logs, or
session state.

Before creating a report, show the complete report, exact new path, and complete
changeset, then obtain one explicit approval. Reject a report path that already
exists. Never overwrite or update a prior report. Approval to save a report does
not authorize any other write.

## Source ownership and prohibited mutations

Treat sources by their actual owners:

| Source | Authority | Reviewer action |
|--------|-----------|-----------------|
| GDD requirement text and approval | Product/design owner | Read and verify only |
| Technical requirement lifecycle and stable ID | Technical/product owner recorder | Read and verify only |
| ADR decision and lifecycle | ADR owner | Read and verify only |
| Story implementation link | Production owner | Read and verify only |
| Test result | Test runner/QA evidence store | Read and verify only |
| Derived registries and indexes | Their dedicated recorder | Detect drift only |

The reviewer must not:

- create, allocate, rename, revise, deprecate, or approve a TR ID
- infer an approved requirement from prose
- add or repair an ADR, story, test, registry, traceability index, or systems-index link
- change ADR lifecycle, system status, signoff, consistency logs, or session state
- treat user permission to continue development as a changed gate verdict
- invoke another workflow to repair findings in the same review task

## Phase 0: Validate mode, write boundary, and mutation guard

1. Parse the mode and exact target. On an invalid mode, missing target, target
   outside the project, or ambiguous target, return ERROR and no verdict.
2. Establish the allowed write set before reading review inputs:
   - default: empty
   - saved-report request: the one exact, new, user-authorized report path
3. Snapshot every project file outside .git as project-relative path, size, and
   SHA-256. If a report is authorized, exclude only that exact path from the
   before/after comparison.
4. Immediately before the final response, repeat the snapshot. Any added,
   deleted, or changed path outside the allowed write set is
   MUTATION_GUARD_FAILED. Name every changed path, return BLOCKED, stop, and do
   not attempt an automatic revert.

The mutation guard is mandatory in every mode, including conversational output
with no saved report.

## Phase 1: Build the complete target manifest

Build a canonical manifest before evaluating evidence. Include every input
actually used, with:

- canonical project-relative path
- source type: GDD, requirement registry, ADR, architecture, engine reference,
  project standard, story, test source, or test-run record
- complete-file SHA-256
- source revision: repository commit when available, otherwise WORKTREE plus the
  manifest hash

Mode-specific inputs:

- coverage: in-scope GDDs, explicit requirement records, and ADRs
- consistency: ADRs and their explicit dependency/interface records
- engine: ADRs, the pinned VERSION.md, applicable breaking-changes,
  deprecated-apis, and module references
- single-gdd: the exact GDD, its explicit requirement records, and ADRs that
  explicitly name those IDs
- rtm: coverage inputs plus stories, test sources, and test-run records
- full: all of the above that exist in the selected scope

List missing and not-applicable input classes separately. Never silently omit a
file class. Hash the canonical ordered manifest itself as target_manifest_hash.
The report must contain the full manifest, not only a count.

If a critical input class is missing or any intended input could not be read,
continue only far enough to report what was checked and return PARTIAL unless a
confirmed blocker already requires BLOCKED.

## Phase 2: Admit only explicit owner-approved requirements

A requirement is eligible for gate coverage only when all of these are present:

1. A stable requirement ID appears verbatim in the source GDD.
2. Its lifecycle record identifies that exact ID and immutable source text.
3. The record identifies the source GDD path and a source revision or SHA-256
   that matches the manifest.
4. The record contains explicit owner approval: owner identity, approval status,
   and approval timestamp.
5. The lifecycle state is active for the reviewed revision.

Do exact ID matching. Do not use semantic, fuzzy, normalized-text, or
same-intent matching to admit or reuse an ID.

Prose that appears to imply an architectural requirement but fails any admission
condition is not a requirement baseline and must not receive an ID. Emit a
CANDIDATE_REQUIREMENT finding with the source path/hash, exact evidence location,
candidate text, missing approval/provenance fields, and destination owner who may
decide it in a separate task.

An unapproved, inferred, ambiguous, or stale requirement is UNVERIFIED and forces
PARTIAL unless a separate confirmed blocker already forces BLOCKED. Never edit
the registry. If registry text differs from its bound GDD revision, report
REGISTRY_DRIFT; do not reconcile it.

## Phase 3: Verify explicit traceability

For each admitted requirement, accept ADR coverage only when:

- an in-scope ADR names the exact requirement ID in its explicit requirements section
- the ADR source revision is in the manifest
- the ADR lifecycle state is valid for use by the gate
- the cited decision actually addresses the named requirement without conflict

Use these coverage states:

- VERIFIED_COVERED — exact current link and valid decision evidence
- VERIFIED_GAP — admitted requirement has no exact usable ADR link
- UNVERIFIED_LINK — only prose similarity, a GDD-level mention, an implicit
  relationship, a stale revision, or an ambiguous link exists

Implicit coverage never becomes VERIFIED_COVERED. A GDD filename or system name
alone is not a requirement link. Do not repair a missing link.

For full and rtm modes, extend the chain using exact IDs:

- Story evidence is valid only when the story names the exact requirement ID and
  governing ADR ID.
- Test linkage is valid only when the test source names the exact requirement,
  ADR, or story ID required by the project contract.
- A test file's existence proves discovery only, never execution or success.

## Phase 4: Verify actual test-run evidence

Where test evidence is in scope, locate the latest authoritative run record for
the exact test source and reviewed source revision. Valid executed evidence must
contain:

- immutable test run ID
- exact test path and its content hash
- linked requirement/ADR/story IDs
- result
- execution timestamp
- reviewed source revision or target manifest hash

Classify it exactly as:

- EXECUTED_PASS — latest authoritative run passed and matches the current revision/hash
- EXECUTED_FAIL — latest authoritative matching run failed
- STALE_RUN — a run exists but targets another revision/hash
- DISCOVERED_NOT_EXECUTED — a test file exists without an authoritative run
- MISSING_EVIDENCE — the claimed test or run record is absent
- NOT_APPLICABLE — explicitly justified by the governing requirement contract

Only EXECUTED_PASS counts as passing evidence. File existence, a story's stated
test path, an old run, an implicit link, or a generated test name never counts as
covered or passing. EXECUTED_FAIL is a confirmed blocker. STALE_RUN,
DISCOVERED_NOT_EXECUTED, and MISSING_EVIDENCE force PARTIAL when test evidence is
required.

## Phase 5: Consistency, dependency, and engine checks

Compare current, in-scope ADR decisions for:

- incompatible ownership of the same state or resource
- contradictory integration contracts
- frame/resource budgets that cannot simultaneously hold
- dependency cycles, missing dependencies, or dependencies on unusable ADRs
- contradictory architecture patterns for the same boundary
- incompatible assumptions about the pinned engine version or API

For engine checks, bind every conclusion to the manifest's pinned VERSION.md and
cited engine-reference file/hash. A missing or unreadable required engine
reference is unknown evidence and prevents PASS. Do not silently substitute
training knowledge for the pinned reference.

In full mode, request independent read-only findings from technical-director and
lead-programmer in parallel when those roles are available. Each reviewer returns
findings only and receives the same target_manifest_hash. If either required
reviewer declines, times out, errors, or reviews a different manifest, record the
failure and return PARTIAL unless a confirmed blocker requires BLOCKED. No
reviewer may modify project files.

## Phase 6: Deterministic verdict

Apply this precedence:

1. BLOCKED when the mutation guard fails or any confirmed in-scope blocker
   exists, including a verified critical coverage gap, blocking ADR conflict,
   dependency cycle, incompatible pinned-engine decision, or current
   EXECUTED_FAIL where test evidence is required.
2. PARTIAL when no confirmed blocker exists but the review cannot certify the
   target: incomplete manifest, missing critical input, candidate/unapproved
   requirement, UNVERIFIED_LINK, unknown engine evidence, stale/missing test-run
   evidence, or required reviewer failure.
3. PASS only when the manifest is complete and current, every admitted in-scope
   requirement has exact valid coverage, every required check completed, all
   required test evidence is EXECUTED_PASS or justified NOT_APPLICABLE, no
   blocker exists, and the mutation guard passes.

Never emit PASS with unknown, implicit, missing, or stale evidence. Do not emit
legacy advisory or document-review labels as gate verdicts.

## Phase 7: Staleness and gate use

A report is usable only for its exact target_manifest_hash. Before any consumer
uses it as gate evidence, rebuild the target manifest using the report's recorded
scope. If any path, content hash, source revision, required input, or report scope
differs, mark the report STALE. A stale report has no current gate value and must
not be relabeled.

PASS means the exact current manifest satisfies this gate. BLOCKED means a
confirmed blocker exists. PARTIAL means certification is incomplete. These are
formal machine semantics, not advisory prose.

An owner may separately sign an ACCEPTED_RISK record, but it:

- is not produced or written by this reviewer
- names the original report ID and finding IDs
- is limited to an exact manifest hash and scope
- identifies the accountable owner, signature timestamp, rationale, and expiry
- becomes invalid on scope/hash change or expiry
- never edits or converts the original BLOCKED/PARTIAL verdict to PASS

Permission to continue work is a risk disposition, not gate passage.

## Required continuation

Read references/continued-workflow.md in full. It defines the immutable report
schema, saved-report procedure, final mutation check, and handoff. Follow it
without expanding the write surface.
