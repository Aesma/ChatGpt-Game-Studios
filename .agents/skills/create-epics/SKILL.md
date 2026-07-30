---
name: create-epics
description: "Create or safely update one traceable epic per binding architecture module from current Approved GDDs, Accepted ADR lifecycle evidence, and TR coverage, with bounded manifests, dependency ordering, conflict-safe version and existence conflict check, and a recorded multi-file result."
---

# Create Epics

Treat revisions as supplied metadata; never calculate them from file content. Use stable business IDs, canonical paths, schema versions, explicit revisions, and UTC run IDs for identity and currentness.

Translate current approved design and accepted architecture evidence into epic
planning artifacts. Every selected in-scope canonical architecture module
produces exactly one epic, even when several systems map to it. This workflow never creates stories,
implementation tasks, code, assets, GDD/architecture/ADR/TR changes, readiness
transitions, or downstream approvals.

## Invocation and request contract

Invoke only as:

    $create-epics <request-manifest-path>

No argument prints that usage and stops before repository discovery, input reads,
delegation, authorization, or writes.

The manifest declares `contract: cgs.create-epics-request/v2` and:

- stable run/plan IDs and exact scope: `all`, one legal layer, ordered stable
  system IDs, or ordered stable module IDs;
- exact systems-index, architecture, control-manifest, TR-registry, engine-version,
  selected GDD, Accepted ADR, ADR lifecycle/review/authoring-receipt, and existing
  epic/index evidence paths with expected declared revision or `ABSENT`;
- exact output root, index path, create-only transaction-receipt path, expected
  target/index approved prior state revisions or `ABSENT`, and deterministic slug convention;
- context budget no larger than 32 files and 1048576 exact bytes; larger scopes
  must be split into another request rather than truncated;
- `review_mode: full | lean | solo`, producer task identity/limits at or below
  contract, and at most one targeted revision plus one re-review;
- product/planning owner, mutation authority, plan author, target recorder/writer,
  receipt recorder, and producer identities; and
- authorization manifest ID/revision/authority or instruction to collect one bounded
  authorization after candidate inventory, plus exact non-writes.

Reject unknown/duplicate fields, unsafe/aliased paths, invalid revisions/statuses/
layers/IDs, target/index/receipt aliasing, duplicate output paths, role identity
conflicts, missing expected preimages, or limits above contract.

Use runtime task identities when exposed. Otherwise generate one lowercase UUID
per task role and persist it. Never claim the user, source owner, producer,
architecture reviewer, ADR lifecycle recorder, or another writer identity.

## Roles, approval, and mutation boundary

- Systems index/GDD owners determine eligible systems and product requirements.
- Accepted ADR lifecycle records and current architecture determine binding module
  ownership/boundaries; this workflow cannot promote a proposal.
- The user or named planning owner chooses include/skip and approves exact epic
  plan content; it cannot waive stale/invalid source evidence or a conflict.
- Producer advice is bounded/read-only and never authorizes files or changes source
  truth.
- Mutation authority authorizes exact create/update targets, index patch, and
  create-only result receipt.
- The recorder/writer applies only the approved version and existence conflict check transaction and reports every
  applied/non-applied path.

Planning approval and write authorization are separate. After module mapping,
candidate bytes, target inventory, and optional producer gate are stable, present
one complete mutation manifest. Obtain one explicit authorization unless the
request already binds that exact manifest/current revisions. Never ask per file.
A new path, classification, candidate revision, source identifier, owner/writer, or larger
scope requires re-preview and new authorization.

## Authoritative source and status contract

The workflow consumes only current evidence declared by the request:

1. `design/gdd/systems-index.md` exact path/revision is the sole system enumeration
   source. Filesystem glob, filename, `Summary`, `Overview`, prose search, or
   discovery cannot add/remove systems.
2. A system is eligible only when its exact shared status is `Approved`. Legal but
   ineligible values are `Not Started`, `In Design`, `In Review`, and
   `Implemented`. `Designed` or any other token is malformed, never an alias.
3. Each eligible row must have stable system ID, exact GDD path, layer/order, and
   current row identifier. The full GDD must agree on ID/status and supply stable
   requirement/acceptance IDs plus declared revision.
4. `docs/architecture/architecture.md` must be a current derived view with stable
   module IDs/boundaries/owners/dependencies and exact system-to-module mappings.
   Every binding claim cites current Accepted ADR evidence.
5. An ADR is accepted only when its target revision, independent review record/revision,
   authoring receipt, and `cgs.adr-lifecycle-record/v1` current Accepted transition
   all match. Status prose alone, Proposed/Unknown/Superseded/Deprecated ADR, stale
   receipt, or non-binding architecture proposal cannot govern an epic.
6. `docs/architecture/tr-registry.yaml` supplies stable TR IDs, source GDD ID/path/
   locator/revision, module/system ownership, architecture-required classification,
   Accepted ADR coverage or auditable N/A disposition, and row identifier.
7. Control manifest and engine-version evidence must match the architecture/ADR
   source set. Mismatch is stale/blocked, never silently normalized.

Any missing, ambiguous, duplicate, stale, or contradictory required identity/
revision/status/owner stops the affected requested scope before candidate approval.
Never infer a GDD path, module, ADR acceptance, TR coverage, or status.

## Bounded source manifest

Select exact candidates in stable order:

1. applicable `AGENTS.md` root-to-output targets;
2. request, systems index, control manifest, architecture, TR registry, engine
   version;
3. selected Approved GDDs in systems-index order;
4. governing Accepted ADRs in canonical ADR ID order with lifecycle/review/
   authoring receipts adjacent;
5. exact existing epic targets/index/previous result receipt evidence.

Never scan all GDDs/ADRs/epics or follow undeclared links. Count every loaded file
against hard maxima 32 files and 1048576 exact bytes. Determine size before load;
never truncate. When the exact requested scope cannot fit, return
`BLOCKED — SOURCE_MANIFEST_BUDGET_EXCEEDED`, list a deterministic request split,
and write nothing.

Create canonical `cgs.epic-source-manifest/v2` with ordered path, role, stable
artifact/module/system/TR/ADR IDs, owner, locator/row identifier, bytes, declared revision,
version/status, dependency edge, loaded/omitted state, and reason. Canonicalize
UTF-8 LF, fixed field order, no trailing whitespace, one final newline; compute
manifest identifier. Source currency is content-bound: paths, labels, timestamps, and
semantically similar prose do not establish currency without matching declared revisions.

revalidate every source before producer review, plan approval, mutation preflight,
and receipt finalization. Before the first write, any mismatch makes dependent
candidates STALE, invalidates approval/authorization, returns PARTIAL/BLOCKED with
changed paths, and performs zero writes. A mismatch discovered only during
post-write receipt finalization returns PARTIAL with exact applied-state evidence,
permits only the already-authorized PARTIAL receipt attempt, and never claims
COMPLETE or performs further ordinary writes.

## Phase 0: Enumerate exact Approved systems

Validate systems-index identity/status/path/layer/order first. Apply request scope
only to that immutable index manifest. Full-read only selected exact GDD paths.

- `all`: every exact Approved row in declared layer/order;
- layer: Approved rows in that layer/order;
- system IDs: exact declared rows in request order after uniqueness/eligibility;
- module IDs: resolve selected modules only after Phase 1 mapping, but their source
  system set still comes solely from eligible index rows.

Report legal excluded rows. A requested ineligible/malformed/missing/ambiguous row
returns BLOCKED. No eligible systems returns
`BLOCKED — NO_ELIGIBLE_APPROVED_SYSTEMS`. Do not claim COMPLETE with omissions.

## Phase 1: Resolve one-epic-per-module identity

From current binding architecture evidence build:

    module_id -> {
      module_name,
      owner,
      architecture_path/locator/revision,
      accepted_adr_ids/revisions/lifecycle_receipts,
      system_ids[] in systems-index order,
      layer,
      dependency_module_ids[],
      order_key
    }

Rules:

- canonical epic ID is `EPIC-MODULE:<module_id>`; module ID, not name/slug/system,
  owns identity;
- exactly one candidate epic per unique module ID, aggregating every selected
  eligible mapped system ID and GDD; two systems in one module never create two
  epics;
- mixed system-per-epic and module-per-epic identity modes are prohibited;
- one system may contribute to multiple modules only when architecture explicitly
  declares distinct binding responsibility slices and TR rows map requirements to
  the correct module; otherwise BLOCKED;
- one module spanning system layers uses the architecture-declared module layer/
  order. Missing/conflicting layer/order is BLOCKED, never inferred from a system;
- module name/slug is display/routing metadata. A slug collision with a different
  module/epic ID is conflict, never solved by numeric suffix;
- every selected system/TR must map to at least one binding module; every candidate
  module must own at least one selected TR or explicit foundational responsibility
  with Accepted ADR evidence.

Render and ask planning owner to confirm/correct the read-only mapping table. A
correction requires current architecture/TR-owner evidence; user preference cannot
rewrite binding architecture. Include/skip decisions choose plan scope only.

## Phase 2: Validate TR/ADR coverage and downstream eligibility

For every selected TR row use exactly one disposition:

1. `ADR_ACCEPTED`: current Accepted ADR ID/path/revision plus lifecycle/review/
   authoring-receipt revisions covers the TR/module.
2. `ADR_NA`: architecture decision is truly not applicable and the registry row
   provides reason code `PRODUCT_ONLY`, `CONTENT_ONLY`, `PRESENTATION_ONLY`, or
   `NO_ARCHITECTURE_EFFECT`, exact owner, evidence path/locator/revision, and reviewed
   row identifier.
3. `ADR_REQUIRED_GAP`: registry says architecture required but no current Accepted
   coverage exists.
4. `UNKNOWN`: missing/ambiguous/stale classification or placeholder such as
   `TR-???`/ADR `N/A` without evidence.

Never convert UNKNOWN to ADR_NA. `ADR_REQUIRED_GAP` and UNKNOWN create stable
`cgs.epic-traceability-finding/v1` with epic/module/system/TR IDs, source revisions,
owner, destination `ARCHITECTURE_DECISION`, acceptance condition, status, and
stable finding key built from the rule ID and stable subject IDs.

Epic planning status and story routing are deterministic:

- all TRs ADR_ACCEPTED or valid ADR_NA, sources current: `Planning Status: READY`;
- any ADR_REQUIRED_GAP/UNKNOWN/stale/blocking dependency: `Planning Status:
  BLOCKED`, with exact affected TR IDs;
- create-stories may later emit a story for a blocked TR only as `Blocked` with the
  same finding ID/owner/acceptance condition; it may not use `TR-???`, unaudited
  ADR N/A, or Ready;
- ADR_NA TRs may produce Ready stories only when the exact reason/evidence row is
  current and no other readiness blocker applies.

Creating a BLOCKED epic preserves planning scope but does not claim architecture,
story, sprint, or implementation readiness.

## Phase 3: Build dependency graph and deterministic order

Combine architecture module dependencies with systems-index dependency evidence
and TR ownership. Every edge records upstream/downstream module IDs, source path/
locator/revision, kind, and blocking semantics.

Reject self-edge, duplicate contradictory edge, missing module, unknown owner,
cycle, cross-layer inversion, or source disagreement. No producer/user decision
may waive an invalid graph into readiness.

Topologically order unique module epics by explicit architecture layer/order then
stable module ID tie-breaker. Record:

- `planning_dependencies`: epic IDs that must exist/current before planning can be
  decomposed safely;
- `execution_dependencies`: upstream epics/modules whose accepted implementation
  evidence is required before dependent work executes; and
- missing/stale upstream epic evidence as stable BLOCKED findings without changing
  the authoritative module graph.

Dependency order controls candidate/index order and later story routing. It never
silently creates excluded upstream epics or marks them complete.

## Phase 4: Inventory outputs and classify candidates

Derive deterministic path
`production/epics/<module-slug>/EPIC.md` from stable module identity and declared
slug convention. Inventory every target, `production/epics/index.md`, and exact
result receipt path before producer review/authorization.

Record approved prior state revision/ABSENT, embedded epic/module/system IDs, source-manifest
identifier, generated schema, index ownership/collisions, and unknown/manual content.
Render exact candidate bytes and classify:

- `create`: target ABSENT, identity/path/index unique;
- `no-op`: existing bytes exactly equal candidate and current sources/index
  evidence match; do not refresh date/reformat;
- `update`: same canonical epic/module identity, recognized managed schema only,
  unique index mapping, no manual/unknown content, and exact diff approved later;
- `stale-update`: same safe managed identity but stored source revisions/identifier differ;
  show stale source diff and require current plan reapproval;
- `conflict`: identity/slug/module differs/ambiguous, duplicate index row, unknown/
  manual content, unsafe read, legacy per-system epic cannot map losslessly to the
  one-module aggregate, or another artifact owns the path.

Conflict blocks the whole transaction before producer/authorization. Never
overwrite/merge/delete/rename/relabel or write non-conflicting siblings. A legacy
system epic requiring aggregation needs a separately owned migration, not update.

If every target/index operation is no-op or planning-owner skipped, finish
`COMPLETE — NO_CHANGES_REQUIRED` only after current source/approved prior state verification;
write no receipt/timestamp solely to manufacture activity.

## Phase 5: Render managed epic schema v2

Every candidate uses `cgs.epic-plan/v2` and contains:

    Epic ID: EPIC-MODULE:<module_id>
    Module ID / name / owner / layer / order
    Planning Status: READY | BLOCKED
    Story Eligibility: READY | BLOCKED
    System IDs and exact GDD paths/revisions
    Source Manifest ID / revision
    Systems-index / architecture / control-manifest / TR-registry revisions
    Accepted ADR IDs, target revisions, review/authoring/lifecycle receipt revisions
    Engine/version evidence ID/revision
    Planning and execution dependency epic/module IDs
    Stable traceability finding IDs

Required sections:

1. Module Scope and Boundaries — architecture-owned responsibility, included
   systems/TR slices, explicit exclusions;
2. Source Evidence — exact version/revision table for every authority;
3. Governing Accepted ADRs — decision summary/engine risk/current receipt bindings;
4. GDD/TR Traceability — each stable TR ID, product requirement locator/revision,
   module responsibility, ADR_ACCEPTED/ADR_NA/gap disposition/finding;
5. Dependencies and Order — graph edges, planning/execution conditions;
6. Deliverables and Acceptance Mapping — observable module outcomes traced to TR/
   GDD acceptance IDs, not implementation tasks;
7. Definition of Done — all stories/acceptance/tests/manual evidence/dependencies
   expressed as referenced obligations, never invented completion;
8. Risks, Open Findings, and Owner Handoffs;
9. Story-Creation Contract — stable epic/module/source identifier, blocked routing,
   exact downstream preconditions;
10. Provenance — plan approval, producer result, recorder/result receipt IDs.

Do not prescribe story implementation steps or copy external product/architecture
truth as a second authority. Reference stable IDs/path/locator/revision.

## Required continuation

Read and follow `references/continued-workflow.md` in full after candidate render.
It defines the capped producer gate, plan approval, one changeset authorization,
source/target/authorization/writer version and existence conflict check, recorder transaction/partial result,
external receipt, final verdicts, and single next-step handoff.

In full mode the producer receives exactly one initial attempt. Concerns permit
at most one targeted revision and exactly one re-review; a second revision or
third review is prohibited.

## Non-write boundary

This workflow writes only selected managed EPIC.md targets, exact managed index
rows/header fields, and one create-only transaction receipt named by the request.
It never writes sources, stories, sprints, review/lifecycle records, registries,
readiness, implementation, code, tests, assets, or shared catalog.
