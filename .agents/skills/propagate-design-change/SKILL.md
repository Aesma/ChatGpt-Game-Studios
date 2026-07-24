---
name: propagate-design-change
description: "Compare one changed GDD with an explicit immutable baseline, trace stable TR and dependency impacts through a bounded reverse graph, and publish an immutable owner-routed impact record without changing authoritative downstream artifacts."
---

# Propagate Design Change

Analyze one exact GDD change, prove the downstream coverage, assign stable impact
identities, and route work to artifact owners. This workflow is an impact recorder,
not an ADR, registry, epic, story, sprint, GDD, implementation, or readiness
writer. It never automatically applies a downstream resolution.

## Invocation and zero-effect boundary

Invoke only as:

    $propagate-design-change <request-manifest-path>

No argument prints that usage and stops before repository discovery, source reads,
delegation, approval, authorization, or writes.

The request must declare `contract: cgs.propagate-design-change-request/v2` and:

- stable `run_id`; changed GDD ID, normalized current path, and expected raw
  SHA-256;
- explicit immutable baseline kind `git-object | approved-snapshot`, locator,
  resolved object/snapshot ID, baseline path, expected raw SHA-256, and approved
  record path/hash when approval evidence is used;
- explicit rename evidence or exact `baseline_path`; `HEAD:<path>`, a branch name
  that is not resolved to an object ID, mtime, and “previous version” are invalid;
- exact TR registry, architecture/ADR inventory, epic index/inventory, story
  inventory, sprint/work tracker, owner registry, active-work, prior report, owner
  resolution/coordination receipt, and receipt-chain evidence paths with expected
  hashes or `ABSENT`;
- `review_mode: full | lean | solo` and named analysis author, technical
  reviewer, planning owner, report writer, and receipt recorder role identities;
- canonical output root `production/change-impact`, expected report/receipt
  preimages, and exact non-write paths; and
- limits no larger than 48 files, 2097152 exact bytes, 256 graph nodes, 512
  graph edges, 100 impacts, 25 decisions per interaction batch, and four decision
  batches per run.

Reject unknown or duplicate fields, unsafe/aliased paths, invalid IDs/hashes,
mutable baseline locators, target/source aliasing, role substitution, limit
increases, missing expected preimages, or a request that authorizes downstream
artifact writes.

Use runtime task identities when exposed. Otherwise generate one lowercase UUID
per task role and persist it. One human may hold multiple organizational roles in
lean staffing, but the evidence identities and decisions remain explicit. In
full mode the technical reviewer must differ from the analysis author and report
writer.

## Roles and authority

- The GDD owner owns the current product requirement text.
- Registry/architecture owners own TR and ADR truth.
- Epic, story, sprint, and implementation owners own their artifacts and status.
- The analysis author computes diff, coverage, graph, impacts, and routes.
- The independent technical reviewer checks analysis quality only.
- The planning owner approves the exact impact report and owner-routed plan.
- Mutation authority may authorize only the immutable report and result receipt.
- The report writer and receipt recorder apply only that authorized evidence set.

Producer/reviewer advice, plan approval, write authorization, owner coordination,
owner resolution, and receipt recording are separate facts. None substitutes for
another, and this workflow cannot claim to speak for an artifact owner.

## Phase 0: Pin baseline, current bytes, and change identity

Read the request, baseline approval evidence when present, exact baseline bytes,
and exact current GDD bytes. Verify every expected hash before analysis.

For a git baseline, resolve the supplied reference once to an immutable commit or
blob object ID and record both the caller token and resolved ID. For an approved
snapshot, require retrievable immutable bytes plus the matching approval record
and hash. Never silently substitute `HEAD`, a newer approval, or current workspace
bytes.

Rename handling is explicit:

1. use the declared baseline path when it resolves and hashes correctly;
2. otherwise accept only one declared rename proof bound to baseline/current
   paths and hashes; or
3. stop BLOCKED on zero, multiple, or hash-mismatched candidates.

If the baseline is valid and has no target file, classify `NEW_GDD`; do not call
it NO IMPACT. Equal verified baseline/current hashes are `NO_CHANGE` with zero
writes.

Derive the stable change identity from canonical UTF-8 fields:

    change_id = PDC-<gdd-stable-id>-<first16(sha256(
      baseline_locator_id + NUL + baseline_path + NUL + baseline_sha256 + NUL +
      current_path + NUL + current_sha256))>

The same exact baseline/current byte pair must reproduce the same `change_id`.
A different current or baseline hash is a different change, never an update to
the old report.

Create `cgs.design-change-baseline/v2` containing locator kind/token/resolved ID,
approval evidence, both paths/hashes/byte counts, rename proof, current workspace
state, diff range, and `change_id`.

## Phase 1: Compute a stable structured diff

Compare the exact pinned bytes. Create `cgs.design-change-diff/v2` rows for added,
removed, and modified requirements, TR references, rules, formulas, acceptance
criteria, constraints, tuning values, and path identity. Each row records:

- stable `delta_id` derived from `change_id`, baseline/current stable requirement
  ID or normalized locator, and change kind;
- baseline and current path, locator, excerpt digest, and containing-section
  digest; never store an unverifiable conceptual-only summary;
- before/after TR IDs and requirement IDs without inventing or renumbering them;
- semantic kind, evidence confidence, and ambiguity finding IDs; and
- exact baseline/current source hashes.

Unchanged context may be listed but cannot generate an impact. Missing, duplicate,
or ambiguous stable requirement identity creates a finding and keeps the delta
open.

## Phase 2: Build a bounded source manifest

Enumerate through declared indexes/registries first; never glob the whole project
as an unbounded fallback. Required coverage layers are:

1. baseline/current GDD and changed requirements;
2. current and baseline-compatible TR registry evidence;
3. architecture module/dependency evidence and ADR inventory/lifecycle evidence;
4. epic inventory/index and exact implicated epics;
5. story inventory and exact implicated stories;
6. sprint/work tracker and active-work sources;
7. owner registry/ownership fields; and
8. existing immutable report, receipt chain, coordination receipts, and owner
   resolution receipts when this is a continuation run.

Create canonical `cgs.pdc-source-manifest/v2` with ordered normalized path, layer,
artifact/stable IDs, inventory authority, owner, exact bytes, raw SHA-256, parsed
state, edge locators, loaded/omitted reason, and expected-current evidence.

Hard maxima are 48 files, 2097152 exact bytes, 256 graph nodes, 512 edges, and 100
impact rows per run. Determine size/count before loading a file; never truncate a
file or silently drop fanout. If any limit would be exceeded, mark the layer
PARTIAL, stop expansion at a deterministic boundary, list omitted identities,
and emit deterministic continuation shards ordered by layer, owner, artifact
type, stable ID, then path. A later run must bind the same change ID and prior
receipt-chain head.

Coverage state is exactly `SCANNED | KNOWN_EMPTY | PARTIAL`. `KNOWN_EMPTY`
requires successful inventory of the authoritative expected location. Missing or
unparseable TR, dependency, ownership, active-work, or required inventory evidence
is PARTIAL, not empty. Any PARTIAL layer forbids NO_IMPACT, ANALYSIS_COMPLETE, or
CONVERGED.

## Phase 3: Traverse stable TR and dependency closure

Use stable TR IDs as the primary join and preserve direct path/ADR/epic/story
edges as diagnostic evidence:

    delta -> TR -> ADR/module dependency -> epic -> story -> sprint/work -> owner

For every delta:

1. reconcile baseline and current TR rows by stable TR ID and row hash;
2. record removed, inactive, duplicated, missing, or ambiguous mappings as
   findings; never invent `TR-???` or infer a replacement ID;
3. traverse all matching ADR, module dependency, epic, story, and work edges;
4. traverse reverse dependency edges so upstream contract changes reach every
   dependent module/artifact;
5. retain all evidence paths while deduplicating artifact nodes; and
6. produce one closure row for each delta: `IMPACTS_FOUND`, `NO_IMPACT_PROVEN`,
   or `OPEN_COVERAGE`.

`NO_IMPACT_PROVEN` requires every layer SCANNED/KNOWN_EMPTY, unambiguous TR
identity, and explicit evidence that no dependency edge continues. Successfully
scanned empty subsets cannot close a partial branch.

## Phase 4: Normalize stable impacts and findings

Artifact identity is the declared stable ID. When the authoritative artifact
format has no stable ID, use `PATH:<normalized-path>` and report the missing-ID
finding; never use a mutable title or array position.

Derive:

    impact_id = PDCI-<first20(sha256(
      change_id + NUL + delta_id + NUL + artifact_type + NUL + artifact_id + NUL + impact_kind))>

    finding_id = PDCF-<first20(sha256(
      change_id + NUL + finding_kind + NUL + subject_id + NUL + evidence_fingerprint))>

Each `cgs.design-change-finding/v2` row contains `change_id`, `finding_id`,
subject delta/artifact ID, `status: OPEN | ROUTED | RESOLVED`, exact `evidence[]`
path/locator/hash entries, owner route, acceptance condition, and `resolution`
receipt/path/hash/verifier fields. RESOLVED requires current owner evidence;
approval or prose acknowledgement alone cannot close a finding.

Each `cgs.design-change-impact/v2` row contains:

- `change_id`, `delta_id`, `impact_id`, artifact type/ID/path/current raw hash;
- exact `evidence[]` containing every incoming TR/direct/dependency edge with
  source locator/hash;
- classification `STILL_VALID | NEEDS_REVIEW | LIKELY_SUPERSEDED |
  TRACEABILITY_GAP | DEPENDENCY_IMPACT | ACTIVE_WORK_RISK`;
- lifecycle field `status: OPEN | COORDINATION_REQUIRED | ROUTED | DEFERRED |
  RESOLVED`;
- artifact owner identity/source/hash, owner workflow, requested action, acceptance
  condition, and due/review point when known;
- resolution decision, rationale, evidence receipt path/hash, artifact postimage
  hash, verifier, and verification time when resolved; and
- stable finding IDs and dependency blockers.

The same change/delta/artifact/kind reproduces the same impact ID. Reruns fold
new evidence into a receipt transition; they never replace or renumber an impact.

Allowed lifecycle transitions are:

- `OPEN -> COORDINATION_REQUIRED | ROUTED | DEFERRED | RESOLVED`;
- `COORDINATION_REQUIRED -> ROUTED | DEFERRED | RESOLVED` only with valid active-
  work coordination evidence;
- `ROUTED -> DEFERRED | RESOLVED`;
- `DEFERRED -> ROUTED | RESOLVED`; and
- `RESOLVED` is terminal for this change ID.

`RESOLVED` requires an external `cgs.owner-design-change-resolution/v1` receipt
from the declared owner workflow binding impact ID, artifact pre/post hashes,
action, verification evidence, and owner/verifier identities. This workflow reads
that receipt; it does not create it or edit the resolved artifact.

## Phase 5: Freeze active work and route ownership

Reconcile story/work status across the artifact, sprint tracker, plan, and owner
registry. Any `In Progress`, `In Review`, active equivalent, or status conflict
creates `ACTIVE_WORK_RISK` with lifecycle `COORDINATION_REQUIRED` and an elevated
warning before decisions.

Record exact owner/assignee, status source/path/hash, `updated_at`, artifact raw
hash, sprint/work ID, and coordination requirement. Treat missing owner,
`updated_at`, or hash as PARTIAL. The route remains frozen until an external
`cgs.active-work-coordination-receipt/v1` binds the impact, owner, artifact hash,
active status, coordination decision, and expiry/review point. A generic user
approval cannot unfreeze it. This is the default concurrency freeze for every
affected in-progress artifact.

Resolve owners from authoritative artifact/registry ownership evidence. Missing,
conflicting, or inferred ownership creates a stable finding and prevents ROUTED.
Create `cgs.owner-routed-design-change-plan/v2`, grouped by owner, with exact
impact IDs, artifact snapshots, owner workflow, requested decision, acceptance
condition, dependencies, coordination state, and required receipt schema.

This workflow never executes the owner plan. It never edits, supersedes, updates,
freezes, closes, or changes status in a GDD, TR registry, ADR, architecture, epic,
story, sprint, work tracker, implementation, test, or owner record.

## Phase 6: Bounded owner decisions

Show the complete normalized impact matrix before asking for dispositions. Offer
bulk choices grouped by owner and action:

- route to the named owner workflow;
- defer with rationale, accountable owner, and review point;
- record still-valid only with exact owner evidence and acceptance rationale; or
- stop without writing.

Still-valid classification does not itself set RESOLVED. Resolution still
requires the declared owner's external resolution receipt and current artifact
verification.

Do not ask once per ADR/artifact. Present no more than 25 decision rows in one
interaction and no more than four decision interactions in a run. Exceptions are
grouped into the next bounded batch. More than 100 decision rows or unreviewed
remainder yields PARTIAL plus deterministic continuation shards; do not treat
omitted rows as accepted, deferred, or no-impact.

Planning-owner decisions change only the route-plan snapshot. They cannot waive
baseline/hash failures, partial coverage, traceability gaps, active-work
coordination, owner evidence, review failure, or downstream owner authority.

## Phase 7: Immutable report and event chain

The canonical report path is exactly:

    production/change-impact/<change_id>.md

It uses `cgs.design-change-impact-report/v2`, binds baseline/current/diff/source-
manifest hashes, coverage, deltas, graph, impacts/findings, active-work freezes,
owner routes, reviewer result, and current convergence state. It is create-only
and immutable.

Its `change_status` is exactly `PARTIAL | NO_IMPACT | ANALYSIS_COMPLETE |
CONVERGED | BLOCKED`; the report also records open/resolved impact and finding IDs
so change, finding, and artifact/impact state can be folded without free text.

- If ABSENT, render complete deterministic candidate bytes.
- If present and valid for the same change ID, use it as the immutable event root;
  never rewrite it.
- If present with another identity, schema, malformed provenance, or incompatible
  hashes, return BLOCKED conflict.

Later coverage, coordination, owner-resolution, or convergence evidence is
appended only through create-only receipts at:

    production/change-impact/receipts/<change_id>/<sequence>-<digest-prefix>.yaml

Each receipt points to the report hash and previous receipt hash or `ROOT`, so the
current state is the deterministic fold of one report plus one linear receipt
chain. A fork, missing sequence, duplicate predecessor, or invalid transition is
BLOCKED. An unchanged rerun creates no activity-only receipt.

Read and follow `references/continued-workflow.md` in full. It defines the
independent review/convergence cap, exact plan approval, report-only mutation
authorization, CAS gates, write/receipt protocol, partial behavior, and terminal
verdicts.

## Convergence rules

Analysis is `ANALYSIS_COMPLETE` only when every delta has full closure, every
impact/finding is stable and owner-routed or resolved, active work is explicitly
frozen/coordinated, all required layers have complete coverage, and technical
review requirements are satisfied.

The change is `CONVERGED` only when:

- every delta is `NO_IMPACT_PROVEN` or all of its impacts are RESOLVED;
- every owner-resolution receipt and artifact postimage revalidates;
- all dependency branches are closed;
- no OPEN, COORDINATION_REQUIRED, ROUTED, DEFERRED, partial-coverage, owner,
  traceability, reviewer, CAS, or receipt-chain finding remains; and
- a fresh bounded rescan against the same baseline/current hash pair discovers no
  new impact.

Rerunning until a favorable label is not convergence. New GDD baseline/current
bytes create a new change ID; they never close the old change by substitution.

## Non-write boundary

The only writable artifacts are the exact immutable impact report and one
create-only result/convergence receipt authorized for the current run. All source
and downstream artifacts are read-only. Never invoke an owner workflow
automatically, create a placeholder replacement ADR, or represent a proposed
route as an applied resolution.
