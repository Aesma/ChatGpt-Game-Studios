---
name: architecture-decision
description: "Author or safely retrofit one collision-safe Proposed Architecture Decision Record for one technical decision, with bounded source evidence, user-selected alternatives, dependency validation, transactional section writes, and independent review/lifecycle handoffs."
---

# Architecture Decision

Author exactly one ADR about one cohesive technical decision. This authoring task
may write only the exact ADR target and create-only checkpoint/authoring-receipt
records named by the request. It never edits GDDs, architecture/traceability
registries, other ADRs, stories/epics/readiness, review/lifecycle records, engine
configuration, code, or implementation files.

The ADR remains `Proposed` throughout new/revise authoring. A legacy retrofit may
remain `Unknown` only when lifecycle evidence is unavailable. No user answer,
advisory result, authoring receipt, or file-write authorization can make it
`Accepted`.

## Invocation and request contract

Invoke only as:

    $architecture-decision <request-manifest-path>

No argument prints that usage and stops before repository discovery, context
reads, ID allocation, delegation, authorization, or writes.

The manifest declares `contract: cgs.architecture-decision-request/v2` and:

- stable run and canonical ADR UUID, one normalized `decision_key`, one decision
  domain, one exact decision question, and in-scope/out-of-scope component IDs;
- exact operation `new`, `retrofit`, `revise-proposed`, or
  `supersede-proposal`;
- collision-safe `cgs.adr-id-allocation/v1` receipt with canonical UUID, optional
  display sequence, slug, exact target path, allocation nonce/allocator identity,
  reserved-at UTC, receipt path/hash, and expected target `ABSENT`; existing-target
  operations instead provide exact path/current raw SHA-256;
- exact checkpoint root and expected predecessor ID/hash or `ABSENT`;
- exact requirement, constraint, dependency/replacement ADR, accepted-registry
  projection, engine reference, code/interface evidence, review/lifecycle, and
  instruction sources with stable ID/owner/path-or-URL/locator/raw hash/date/
  required-or-optional role;
- a bounded ADR summary manifest sufficient for semantic duplicate detection;
- context budget no larger than 16 files and 524288 exact bytes;
- `consultation_mode: full | lean | solo`, consultation caps at or below this
  contract, and max two revision rounds per section decision;
- actual technical decision owner/user authority, mutation authority, author,
  target writer, checkpoint recorder, consultant roles, and intended independent
  architecture-review/lifecycle-recorder roles; and
- authorization manifest ID/hash/authority or instruction to collect one bounded
  authorization after inventory, plus exact non-writes.

Reject unknown/duplicate fields, unsafe/aliased paths, invalid UUID/slug/hash,
duplicate source/ADR IDs, target/checkpoint aliasing, allocation path mismatch,
target already existing for `new`, existing target mismatch, roles with forbidden
identity overlap, or budgets/limits above contract.

Never scan the ADR directory for “next number.” Display sequence is not identity.
The allocation receipt plus exact `ABSENT` Target CAS owns uniqueness. A path
collision invalidates the allocation and stops; never overwrite or silently pick
another number/path in this run.

Use runtime task identities when exposed. Otherwise generate one lowercase UUID
per task role and persist it. Never impersonate the user, source owner, reviewer,
recorder, or consultant.

## Single-decision scope

The request and ADR must answer one question whose alternatives can be selected
and whose consequences can be evaluated as one lifecycle unit.

Before context loading, write a read-only scope record:

    decision_key: <stable normalized key>
    decision_domain: <one domain>
    decision_question: <one interrogative statement>
    in_scope_component_ids: []
    out_of_scope_questions: [{question, owner, destination}]
    inseparability_claim: <evidence-backed reason or null>

Split compound choices when alternatives, owners, acceptance timing, rollback, or
replacement scope can differ. An “A and B” bundle is allowed only when current
evidence proves neither can be decided/rolled back independently; record the
inseparability source IDs/hashes. Route all other questions as separate ADR/TECH
handoffs. One target may not smuggle a second decision through interfaces,
migration, or validation sections.

## Roles and one mutation boundary

- The user or explicitly named technical decision authority owns the selected
  alternative, accepted tradeoffs, scoped exception, and supersession intent.
- The author gathers evidence, presents comparable alternatives, drafts, and
  performs semantic preflight; it never selects the decision.
- Consultants provide bounded read-only findings and never edit/approve the ADR.
- The target writer performs only target section CAS writes.
- The checkpoint recorder creates checkpoint/authoring-receipt records only.
- A future independent architecture reviewer and separate lifecycle recorder are
  both identity-separated from author/writer/consultants and from each other.

After target/scope/duplicate inventory, present one mutation manifest containing
exact target operation/path/preimage-or-ABSENT, canonical ADR ID/allocation receipt,
selected stable section IDs/preimages, checkpoint root/deterministic create-only
record names, writer/recorder identities, limits, and non-writes.

Obtain one explicit mutation authorization. It covers the target regions and
checkpoint/authoring-receipt sequence for this run. Later alternative selection
and exact-section approvals approve content, not filesystem scope. A new path,
operation, section, owner, writer, or larger limit requires a revised manifest;
otherwise never re-prompt for write permission per section/consultation/receipt.

## Versioned ADR schema and section profile

The author contract version is:

    architecture-decision-author-sha256:<sha256(SKILL.md exact bytes || 0x00 || references/continued-workflow.md exact bytes)>

The document profile is `architecture-decision-profile-schema-v2`; content
assertions use `cgs.adr-content-profile/v2`. Stable section IDs, not display
titles, govern inventory, retrofit, decisions, CAS, revisions, and receipts.

| Stable ID | Canonical section |
|---|---|
| `ADR-SEC-METADATA` | ADR ID, schema, completeness, receipt ID, date, decision makers |
| `ADR-SEC-STATUS` | lifecycle status (`Proposed` authoring; `Unknown` legacy only) |
| `ADR-SEC-SCOPE` | one decision question, in/out scope, problem/current state |
| `ADR-SEC-ENGINE` | engine/version/domain references and coverage state |
| `ADR-SEC-DEPENDENCIES` | Depends On/Enables/Blocks/order plus graph result |
| `ADR-SEC-CONSTRAINTS` | hard/derived/unknown constraints and requirements |
| `ADR-SEC-ALTERNATIVES` | comparable alternatives and evidence coverage |
| `ADR-SEC-DECISION` | user-selected proposed alternative and rationale |
| `ADR-SEC-CONSEQUENCES` | positive/negative/neutral consequences and risks |
| `ADR-SEC-TRACEABILITY` | stable product/technical requirement mappings |
| `ADR-SEC-PERFORMANCE` | evidence-bound impacts or hypotheses/validation plan |
| `ADR-SEC-MIGRATION` | migration, compatibility, rollback, ownership |
| `ADR-SEC-VALIDATION` | measurable validation and acceptance evidence needed |
| `ADR-SEC-REPLACEMENT` | related/supersedes/superseded-by/scoped-exception links |
| `ADR-SEC-PROVENANCE` | decisions, approvals, sources, consultations, revisions |

Every target includes:

    # ADR-<display-sequence-or-short-uuid>: <Title>

    > **ADR ID**: <canonical UUID>
    > **Schema**: architecture-decision-profile-schema-v2
    > **Content Profile**: cgs.adr-content-profile/v2
    > **Author Schema**: architecture-decision-author-sha256:<hash>
    > **Authoring Completeness**: DRAFT | PARTIAL | CONTENT_COMPLETE
    > **Authoring Receipt ID**: <stable ID | PENDING>

    ## Status
    Proposed | Unknown

Do not place `Accepted`, `Deprecated`, or `Superseded` into a new/revised target;
do not place reviewer/recorder signatures, review/lifecycle record path/hash, or
authoring-receipt path/hash in the ADR. External records bind already-final bytes
and avoid target/receipt cycles.

## Independent state axes

Checkpoint each section separately:

- `content_state`: `EMPTY`, `PLACEHOLDER`, `SUBSTANTIVE`, or `NOT_APPLICABLE`;
- `evidence_state`: `VERIFIED`, `PARTIAL`, `UNVERIFIED`, `STALE`, `UNKNOWN`, or
  `CONFLICTING`;
- `workflow_state`: `PENDING`, `DRAFTING`, `APPROVED_NOT_WRITTEN`, `WRITTEN`,
  `PRESERVED`, `BLOCKED`, or `OUT_OF_SCOPE`;
- `assertion_results`: stable assertion ID, applicability, PASS/FAIL, evidence,
  owner; and
- `section_status`: `INCOMPLETE`, `COMPLETE`, `INVALID`, or `STALE`.

`CONTENT_COMPLETE` requires every mandatory section COMPLETE, selected alternative
and exact bodies approved by actual user/authority, all required sources verified,
no duplicate/unknown dependency/cycle/global conflict/blocking finding, stable
target/context, and stable read-back bytes. A verified authoring receipt is still
required before Workflow Verdict READY_FOR_REVIEW or a review handoff. Status
remains Proposed.

## Lifecycle state machine and replacement links

Authoring permissions:

- `new`, `revise-proposed`, `supersede-proposal`: target lifecycle status is
  Proposed only;
- `retrofit` with missing/ambiguous historical status may write Proposed or
  Unknown only after user confirms exact meaning;
- existing Accepted, Deprecated, or Superseded ADRs are immutable to this skill.

External lifecycle transitions are:

    Unknown --external evidence/recorder--> Proposed
    Proposed --current independent review + recorder CAS--> Accepted
    Accepted --recorder CAS--> Deprecated
    Accepted --accepted successor + recorder multi-target CAS--> Superseded by <ADR ID>

No reverse transition or author self-transition. A lifecycle recorder consumes a
current independent review plus authoring receipt, validates exact preimage/status,
and emits immutable `cgs.adr-lifecycle-record/v1` binding allowed status-only
pre/post hashes. Registry projection and story/readiness effects are separate
derived-owner actions.

A supersede proposal names one or more exact predecessor IDs/path/hashes/current
Accepted lifecycle receipts, replacement scope, retained obligations, migration,
and replacement completeness. The predecessors remain authoritative until the
successor is independently accepted and recorder atomically links both sides.
Proposed successor never writes predecessor `Superseded By`. Replacement links
must be acyclic and cannot leave two overlapping global stances active. A scoped
exception has objective boundary predicate, owner, reason, precedence, and exit
condition; otherwise align, supersede, or stop.

## Phase 0: Parse, inventory, and duplicate detection

Parse request before broader context. Validate exact operation/identity/allocation/
target/checkpoint/source manifests, modes, roles, budgets, and non-writes.

For existing targets, read all raw bytes, schema/status/section anchors, source/
decision/revision provenance, and current hash. Accepted/Deprecated/Superseded
status returns lifecycle-owner handoff with zero mutation.

For retrofit, inventory missing, malformed, stale, and conflicting sections;
never merely append over an incorrect section or treat legacy prose as current
evidence. Preserve all out-of-scope/custom bytes. Retrofit never validates
historical acceptance.

Compute semantic fingerprint over canonicalized decision domain, decision key,
question, and sorted in-scope component IDs. Compare only the exact bounded ADR
summary manifest (ID/status/title/domain/scope/question/fingerprint/path/hash).

When an exact/near semantic match exists, present factual evidence and user-owned
choices:

1. cancel new ADR and reference existing;
2. revise the existing Proposed ADR under a new exact request;
3. create a supersede proposal for current Accepted ADR;
4. prove an objectively disjoint scope predicate and proceed; or
5. stop for missing evidence.

Never create a duplicate by title variation. The author does not select a route.

After scope/duplicate/target inventory, establish the one mutation authorization.
Invalid/unsafe input returns ERROR/BLOCKED with zero writes.

## Phase 1: Load bounded hash-manifested decision context

After authorization, select candidates in stable order:

1. applicable `AGENTS.md` root-to-target/checkpoint;
2. exact target/checkpoint/allocation receipt;
3. exact stable requirement sources in request order;
4. exact Depends On/replacement/conflicting Accepted ADRs;
5. exact accepted-registry projection rows;
6. exact pinned engine/version/domain/breaking/deprecation references;
7. exact code/interface evidence named by the request; and
8. exact review/lifecycle evidence relevant to retrofit/replacement.

Never scan all ADRs, GDDs, code, registries, or “related” files. Count every
loaded file against hard maxima 16 files and 524288 exact bytes. Determine size
before load; never truncate or follow undeclared links.

The context manifest records ordered path/URL snapshot, role, source ID/owner,
locator, bytes, raw SHA-256, version/date/observed-at, coverage state, dependency
edge, loaded/omitted state, and reason. Canonicalize UTF-8 LF/fixed fields/no
trailing whitespace/one final newline and persist the digest.

Mark an existing target `mutable-target-baseline`; target currentness is checked
by Target/Section CAS, while every external source is re-hashed before dependent
writes/final handoff.

If mandatory context exceeds budget, is absent, or mismatches declared hash,
append at most one authorized PARTIAL checkpoint with
`CONTEXT_BUDGET_EXCEEDED` or `CONTEXT_EVIDENCE_INVALID`, leave target unchanged,
list loaded/omitted evidence, and stop. Never infer `None` from missing evidence.

Only after context succeeds, distinguish current hard constraints, user choices,
derived constraints, hypotheses, UNKNOWN dependencies, and routed handoffs.

## Phase 2: Validate engine/reference and dependency coverage

For every engine/API/technical reference record stable ID, owner/publisher,
path-or-URL/locator, raw/snapshot hash, engine/version/domain, published/updated
date when known, observed-at UTC, knowledge cutoff/risk, relevant claim, and
coverage state `VERIFIED`, `PARTIAL`, `UNVERIFIED`, or `STALE`.

Missing/old/ambiguous/post-cutoff evidence is never “verified.” Write `UNKNOWN`
for unclear API use, verification, dependency, migration, performance, or ordering
rather than `None`. Required UNVERIFIED/STALE/UNKNOWN evidence creates a blocking
finding and prevents READY_FOR_REVIEW; safe Proposed partial drafting may continue.
If no engine is configured, record exact setup-engine technical handoff rather
than inventing engine/version.

Build a graph from exact dependency/replacement IDs/statuses/hashes:

- every Depends On/replacement ID must resolve uniquely;
- implementation/acceptance eligibility requires each required prerequisite
  Accepted with current lifecycle evidence;
- Proposed/Unknown prerequisite is explicit BLOCKED, never None;
- detect self-edge, duplicate edge, dependency cycle, replacement cycle, and
  enable/block contradictions before target substantive writes;
- unknown ID, ambiguous projection, or cycle blocks section readiness/review
  handoff and is persisted as a finding.

The author may still preserve a safe Proposed/PARTIAL skeleton, but cannot claim
dependency-ready, acceptance-ready, registry-ready, or story-ready.

## Phase 3: Create skeleton and checkpoint chain

For collision-safe new target, Target CAS must prove allocation path still ABSENT.
Atomically create header, Status Proposed, and every stable section heading with
neutral placeholders. For retrofit/revise, preserve current bytes until an exact
approved section transaction.

Append create-only `cgs.architecture-decision-checkpoint/v2` after skeleton,
scope/duplicate route, constraint/alternative/decision approval, each section
transaction, consultation result, graph/preflight, target finalization, and receipt
attempt. It records request/allocation/authorization/context/target/author-schema
hashes, scope/fingerprint, full section axes/assertions, sources/coverage, graph/
findings, alternatives/decisions/approvals/revisions, consultations, lifecycle/
replacement links, operation ledger, limits, predecessor ID/hash, next transition,
and UTC timestamp.

Canonical payload excludes its `record_sha256`; append by deterministic name with
predecessor/create-if-absent CAS. Never overwrite/fork. Checkpoint is continuity
evidence, not acceptance/review/lifecycle/registry/readiness evidence.

## Required continuation

Read and follow `references/continued-workflow.md` in full after Phase 3. It
defines alternatives/constraint/source provenance, user decision authority,
section completeness/approval/CAS, bounded consultations/failure, authoring
receipt, independent architecture-review and lifecycle-recorder handoffs, resume,
and one-action stop behavior.

## Non-implementation and non-cross-write boundary

This skill never edits other ADRs, GDDs, registry/control manifests, stories,
readiness, review/lifecycle records, engine setup, source code, tests, assets, or
shared catalog. It may emit typed read-only handoffs/events, but it invokes none.
