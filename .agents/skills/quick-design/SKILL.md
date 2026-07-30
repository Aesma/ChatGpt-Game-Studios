---
name: quick-design
description: "Create one immutable, evidence-gated low-risk design delta proposal against explicit target, section, owner, and base revisions; application, review, lifecycle recording, and implementation remain separate."
---

## Path-first integrity

Accept canonical project-relative paths directly; do not require a caller-supplied
content-derived token. Validate project-root containment, regular-file type, declared
schema/version, stable IDs, permissions, lifecycle state, and path or ID collisions.
Allocate collision-safe IDs independently of file bytes. Before any permitted write,
re-read referenced records and target state, preview the exact authorized changes,
then use same-directory staging plus atomic replacement and rollback on failure.


# Quick Design

quick-design is the lightweight proposal path for one structurally low-risk
change to an existing indexed system, or one explicitly isolated prototype
hypothesis. It creates one immutable proposal and never edits an authoritative
GDD, data file, registry, systems index, story, application receipt, review
evidence, lifecycle record, source file, or test.

A proposal records rationale and requested delta. It is not design truth.
Production work consumes only the updated authoritative GDD after separately
owned application, current-revision independent review, and lifecycle recording.

## Invocation and exact identity

Use exactly one form:

    $quick-design propose "<change>"
      --change-id <QD-stable-id>
      --version <vNNN>
      --target <design/gdd/system-slug.md>
      --target-id <SYS-stable-id>
      --section "<exact level-two heading>" [--section "<heading>" ...]

      [--supersedes <exact-proposal-path>]

    $quick-design propose "<hypothesis>"
      --change-id <QD-stable-id>
      --version <vNNN>
      --experiment-only <exact-prototypes-path-or-stable-id>
      [--supersedes <exact-proposal-path>]

    $quick-design status <exact-proposal-path>
      [--record <exact-lifecycle-record-path>]

propose is the only writing mode. status is read-only. Reject missing,
duplicated, incompatible, or ambiguous arguments. Never infer a target, target
ID, section, predecessor, proposal version, or record from relevance, fuzzy
names, modification time, or "latest".

change-id must match QD-[a-z0-9][a-z0-9-]{2,63}. version must match v[0-9]{3}.
Proposal ID is the exact pair <change-id>@<version>. The canonical path is:

    design/quick-specs/<change-id>/<version>/proposal.md

The path is collision-free by stable change/version identity, not by a
same-day filename. Created At UTC in the proposal is an RFC3339 UTC timestamp
with seconds and Z. The target base revision remains a separate identity binding.

A later revision is a fresh immutable version. It must use a new version, bind
the then-current target evidence, and name the exact predecessor path and
revision in Supersedes. Never update or overwrite an existing proposal.

## Roles, decisions, and authority boundary

Keep these owners separate:

1. Proposal author — this task gathers product decisions and may create only the
   one canonical proposal.
2. Product decision owner — user or named product owner selects product choices.
   The proposal author may not convert derived risk conclusions into user
   preferences.
3. Application author — a later authorized design-system task applies accepted
   delta IDs to exact GDD sections and produces external application evidence.
4. Independent reviewer — a fresh design-review task reviews the complete
   updated GDD and emits revision-bound review evidence.
5. Lifecycle recorder — a separate owner validates proposal, application,
   review, current GDD, and record pre-state before recording APPLIED or
   SUPERSEDED.

Reviewer task identity must differ from proposal and application author
identities. Recorder identity must differ from every author and reviewer. A
subagent in an authoring task, role-playing by one task, chat approval,
solo/advisory review, or an unavailable invented identity is not independent.
Use the runtime task identity when exposed. Otherwise generate one lowercase
UUID once and record codex-task:<uuid>; never claim a person or external task ID
that the runtime did not provide.

Use the same decision ownership classes as the staged design-system contract:

- product-choice — selected by user/named product owner;
- evidence-backed-hard-constraint — current owner source path, artifact ID,
  section/row, exact revision, and fact;
- derived-design-constraint — inputs, derivation, assumptions, and user
  acceptance when it affects the proposed product outcome; and
- technical-handoff — implementation/architecture question routed out.

Every material proposal statement references a stable QDD-<NNN> decision record.
A user may revise the proposed design so risk facts change, but cannot relabel a
current hard fact or derived gate result to enter the quick path.

An explicit bounded request authorizes only the canonical proposal CREATE after
content approval. It does not authorize GDD/data/index/story/receipt/review/
record/code/test edits. If application or implementation is requested in the
same invocation, preserve the proposal result and report:

    Downstream Action: BLOCKED — SEPARATE APPLICATION AND REVIEW REQUIRED

## Status axes and failure precedence

Always report independently:

- Workflow Status: COMPLETE, PARTIAL, BLOCKED, REDIRECTED, or ERROR
- Proposal Status: DRAFT, PROPOSED, APPLIED, SUPERSEDED, or NOT_CREATED
- Currentness: CURRENT, STALE, INVALID, or NOT_APPLICABLE
- Implementation Eligible: YES or NO
- Persistence: NOT_REQUESTED, DECLINED, VERIFIED, or FAILED
- Verdict: PROPOSAL_CREATED, DRAFT_ONLY, STATUS_REPORTED, REDIRECTED, BLOCKED,
  or ERROR

Apply the first matching result:

1. Invalid/unsupported arguments, path, artifact type, encoding, schema, stable
   identity, or contradictory supplied evidence:
   ERROR / NOT_CREATED / INVALID / NO / NOT_REQUESTED / ERROR.
2. Target, section, index, dependency, range, or ownership evidence required to
   resolve risk is missing or UNKNOWN:
   BLOCKED / NOT_CREATED / NOT_APPLICABLE / NO / NOT_REQUESTED / BLOCKED.
3. Any structural risk is YES:
   REDIRECTED / NOT_CREATED / NOT_APPLICABLE / NO / NOT_REQUESTED / REDIRECTED.
4. Discussion stops with unresolved product decisions before an approved full
   draft:
   PARTIAL / DRAFT / CURRENT when the base is still current, otherwise STALE /
   NO / NOT_REQUESTED / DRAFT_ONLY.
5. Approved draft persistence is declined:
   COMPLETE / DRAFT / CURRENT / NO / DECLINED / DRAFT_ONLY.
6. Atomic persistence or byte/schema verification fails:
   ERROR / NOT_CREATED / INVALID / NO / FAILED / ERROR.
7. Only verified atomic creation:
   COMPLETE / PROPOSED / CURRENT / NO / VERIFIED / PROPOSAL_CREATED.

COMPLETE means the requested operation completed. It never means approved or
implementation-ready. Propose is always Implementation Eligible NO.

status may report a recorded APPLIED/SUPERSEDED state with Currentness STALE or
INVALID. It returns ERROR instead of STATUS_REPORTED when the explicitly
requested proposal/record cannot be parsed or identity-bound at all. Never hide
failed, partial, or unsupported coverage behind COMPLETE.

## Phase 1: Resolve exact target, system owner, sections, and base

For a production proposal, canonicalize and require:

- one existing non-symlink Markdown file whose direct parent is design/gdd/;
- one supplied SYS-<canonical-kebab-slug> target ID;
- one or more unique supplied exact level-two headings in invocation order; and
- one required revision value.

Reject directories, globs, URLs, junction escapes, multiple paths, concept/index
documents, reviews, quick specs, stories, data, or unsupported document
profiles. Read applicable AGENTS.md files root-to-target, then exact raw target
bytes.

Parse systems-index.md by exact System ID and normalized Design Doc cell.
Exactly one current row must bind supplied target ID to supplied target path.
Zero/multiple rows, disagreement, or a production GDD without an indexed system
owner returns BLOCKED — TARGET SYSTEM REGISTRATION REQUIRED. Do not fuzzy-match
display names.

Compute and record:

- target declared revision;
- systems-index declared revision and exact owner row locator;
- each supplied section's exact raw heading-bound revision; and
- each required first-level dependency evidence path, artifact ID, locator, and
  declared revision.

The stable section ID is <SYS-id>#<lowercase-kebab canonical heading>. Record
both that ID and the exact heading. Reject two headings that normalize to the
same section ID.

Read the target directly and record its declared revision; no caller-supplied base token is accepted. Duplicate/missing/ambiguous
headings, a delta not assigned to a supplied section, unreadable bytes, missing
owner, or contradictory dependency evidence fails before risk classification.
Do not search for a "most relevant" target or section.

If --supersedes is supplied, validate exactly one predecessor: project-local
non-symlink proposal file, contract cgs.quick-design-proposal/v2, same change ID,
lower version, exact path/revision, same target system identity for production
changes, and lifecycle compatibility. An invalid predecessor returns
ERROR — INVALID PREDECESSOR. A new version always rebinds current base, sections,
index, dependencies, and decisions; it never reapplies stale bytes.

For --experiment-only, require one exact existing scope under prototypes/.
Production target/id/section/base arguments are forbidden in this form. Set
Target Use EXPERIMENT_ONLY. It never becomes APPLIED or production eligible.

## Phase 2: Build the versioned structural risk record

Do not use hours/days as a gate. Effort is non-gating planning context only.

Create one risk assessment contract cgs.quick-design-risk/v2. Every row has:

    id: QDR-<NNN>
    fact: <fixed question>
    result: YES | NO | UNKNOWN
    decision_kind: evidence-backed-hard-constraint | derived-design-constraint
    evidence:
      - path: <exact path>
        artifact_id: <SYS-id or stable artifact ID>
        locator: <section/row/field>
        revision: <non-empty stable value>
        quote_or_fact: <minimal fact>
    owner: <authoritative artifact/product owner>
    derivation: <why evidence produces result>
    assumptions: []

Evaluate every fixed row:

| ID | Risk fact | Gate |
|---|---|---|
| QDR-001 | Adds a production-visible system/subsystem, new stable owner, or systems-index row | YES redirects |
| QDR-002 | Adds state or changes state/lifecycle ownership | YES redirects |
| QDR-003 | Adds/changes cross-system input/output, timing, ordering, or ownership contract | YES redirects |
| QDR-004 | Adds/changes player-facing core rule, pillar, MDA, progression, or economy semantics | YES redirects |
| QDR-005 | Changes formula semantics rather than a documented in-range value | YES redirects |
| QDR-006 | Changes persistence/save compatibility/network/security/accessibility policy/platform contract | YES redirects |
| QDR-007 | Requires multiple authoritative owners or conflicts with another current GDD | YES redirects |
| QDR-008 | Places a tuning value outside its documented current allowed range | YES redirects |
| QDR-009 | Cannot prove the change stays inside supplied target sections and existing owner | YES redirects |

Each row must be YES, NO, or UNKNOWN. Missing evidence means UNKNOWN, not NO,
Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
no trailing whitespace, fixed field order, and one final newline.

For EXPERIMENT_ONLY, evaluate the same rows against exact prototype-scope
isolation evidence. A production-impact row must be NO because the hypothesis is
provably isolated; UNKNOWN blocks, and YES rejects experiment-only routing
instead of converting a production change into a prototype label.

The product owner may change the requested design, after which every row is
re-evaluated against the same still-current source revisions. User confirmation of
a label cannot alter a fact, evidence revision, owner, or derivation.

Any YES redirects before drafting/writing. For QDR-008, return a structured
range-change handoff in conversation: target path/ID/section/revision, exact current
range/unit/owner evidence, requested value, unresolved product-choice owner,
affected dependency owners, and next owner design-system revise-section. The
full authoring path decides a new range and later propagation/review. quick-design
does not choose or propagate it.

Any YES on QDR-001 returns the same no-write redirect. A "small system" is never
a quick profile.

## Phase 3: Derive one eligible profile

Only all-NO production risk records are eligible:

- QD-TUNING — one or more supplied sections change only documented
  designer-controlled defaults within current ranges; formula/rule/state/
  interface meaning is unchanged. Review depth lean or full.
- QD-COSMETIC — player-visible copy, presentation, or feedback mapping changes
  inside one existing indexed system without changing mechanics, state,
  accessibility policy, interface, or ownership. Review depth lean or full.
- QD-LOCAL — bounded clarification/adjustment within existing target sections
  and one indexed owner, with every risk row NO. Review depth full.
- EXPERIMENT_ONLY — isolated prototype hypothesis, no production application,
  formal approval, or APPLIED state.

A locally implemented UI/visual/audio component qualifies as QD-COSMETIC only
when it remains presentation content owned by the supplied existing system. If
it requires a new stable owner, state/lifecycle, interface, accessibility policy,
or systems-index row, QDR-001/002/003/006 is YES and redirects.

Show the complete risk record, evidence/record revisions, derived profile, and
required review depth. User may proceed, revise the product change, or redirect,
but may not select a profile inconsistent with facts.

## Phase 4: Record product decisions and draft delta

Follow Question -> Options -> Decision -> Draft -> Approval for each unresolved
product choice. Present two to four meaningful options. The user/named owner
selects the product rule/value and rationale.

Create QDD decision records:

    id: QDD-<NNN>
    class: product-choice | evidence-backed-hard-constraint |
      derived-design-constraint | technical-handoff
    authority: <user/owner artifact/derivation>
    source_path: <path or null>
    source_artifact_id: <ID or null>
    source_locator: <section/row/field or null>
    source_revision: <revision or null>
    inputs: []
    derivation: null
    assumptions: []
    outcome: <accepted statement or routed question>
    status: accepted | routed | blocked

Hard constraints remain owner-source facts. Derived constraints preserve inputs
and reasoning. Implementation choices, APIs, storage, code structure, test
procedure, and architecture become technical-handoff and stay out of the delta.

QD-TUNING requires exact knob, current default/range/unit, proposed in-range
value, observable behavior, rationale, and decision ID. QD-COSMETIC requires
exact existing presentation owner/section, before/after player-facing feedback,
unchanged mechanic/accessibility/interface invariants, and decision ID.
QD-LOCAL requires exact base rule locators, product-level before/after meaning,
unchanged invariants, outcomes, affected owner, and decision IDs.

Acceptance must be measurable. "Feels right" alone becomes a playtest hypothesis
with metric, observation method, sample/threshold, and decision owner.

## Phase 5: Draft one cgs.quick-design-proposal/v2 artifact

Use this exact header:

    # Quick Design Change Proposal: <title>

    Contract: cgs.quick-design-proposal/v2
    Artifact Type: quick-design-change-proposal
    Proposal ID: <change-id>@<version>
    Change ID: <QD-stable-id>
    Version: <vNNN>
    Status: PROPOSED
    Created At UTC: <RFC3339 seconds Z>
    Proposal Author Task ID: <stable available task identity>
    Target Use: PRODUCTION_CHANGE | EXPERIMENT_ONLY
    Prototype Scope: <exact prototype scope | NOT_APPLICABLE>
    Risk Profile: QD-TUNING | QD-COSMETIC | QD-LOCAL | EXPERIMENT_ONLY
    Required Review Depth: lean-or-full | full | NOT_APPLICABLE
    Target GDD Path: <exact path | NOT_APPLICABLE>
    Target System ID: <SYS-id | NOT_APPLICABLE>
    Base GDD revision: <positive integer | NOT_APPLICABLE>
    Systems Index Path: design/gdd/systems-index.md | NOT_APPLICABLE
    Systems Index revision: <positive integer | NOT_APPLICABLE>
    Risk Record Contract: cgs.quick-design-risk/v2
    Risk Record revision: <positive integer>
    Supersedes Path/revision: <exact path/revision | NONE>
    Currentness at Creation: CURRENT
    Implementation Eligible: NO

Then include exactly seven level-two sections:

1. Product Decision — QDD records, selected outcome, rationale, authority,
   hard/derived provenance, non-goals, and routed technical questions.
2. Base Snapshot — ordered target path/ID/base revision, exact section headings/
   section IDs/revisions, index row/revision, dependency evidence, and minimal current
   statements.
3. Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
4. Proposed Delta — stable QDDELTA-<NNN> IDs; each maps to one supplied section,
   decision IDs, before/after product meaning, unchanged invariants, and owner.
   State: "This proposal does not replace the authoritative GDD."
5. Observable Acceptance Conditions — stable QDAC/HYP IDs, observable
   conditions, metrics/thresholds, validation and decision owners.
6. Apply, Review, and Record Handoff — ordered delta/section application plan,
   expected application evidence, review depth/evidence, lifecycle requirements,
   propagation owners, and explicit implementation block.
7. Boundaries — exact proposal write and every authoritative/implementation
   non-write.

Do not add a GDD Update Required No escape hatch or instruct implementation from
the proposal.

## Phase 6: Approve and compare-and-create only the proposal

Show the full draft. Ask approve exact content, revise, stop partial, or redirect.
Content approval is not formal review/implementation approval.

Before writing, present:

    CREATE_IF_ABSENT design/quick-specs/<change-id>/<version>/proposal.md
    NON-WRITES design/gdd/**, assets/data/**, design/registry/**,
               production/**, stories, src/**, tests/**, review evidence,
               application receipts, lifecycle records, session state

Use existing explicit authorization only when it covers this exact path and
CREATE_IF_ABSENT semantics. Otherwise obtain one authorization.

Immediately before create:

1. assert canonical proposal path does not exist;
2. re-read/re-read target, all supplied sections, systems index row/file,
   dependencies, owner evidence, and predecessor;
3. Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
4. confirm approved draft bytes still bind those exact revisions/decision IDs; and
5. confirm path, Proposal ID, change/version, and predecessor chain agree.

Any source mismatch returns ERROR — STALE BASE — REBASE REQUIRED with zero
writes. Existing path returns ERROR — PATH EXISTS; CHOOSE A NEW VERSION with zero
modification. The create operation is atomic create-if-absent; a concurrent
winner cannot be overwritten.

After atomic create, re-read bytes and verify contract, IDs, timestamp, source
revisions, risk reference ID, sections, status, and content. Report proposal raw-byte
revision. Declined/partial/failed results use the precedence matrix. Only verified
bytes return PROPOSAL_CREATED.

## Phase 7: Separate application, revision evidence, review, and record

After creation, stop with independent handoffs.

Application:

- A separate design author re-reads proposal and every bound source.
- Each accepted QDDELTA is applied through staged design-system
  revise-section for its exact canonical section with separate authorization.
- Product choices remain proposal decision-owner decisions; the application
  author may not silently select a different outcome.
- If any base/section/index/dependency/risk evidence changed, do not reapply.
  Create a new proposal version with --supersedes against the new base.
- The application owner produces immutable evidence contract
  cgs.design-application/v1 with receipt ID, proposal path/revision, target path/ID,
  pre/post raw GDD revisions, applied delta IDs, exact changed line ranges or patch
  content, application task ID, UTC timestamp, and payload revision.

Review:

- A fresh staged design-review task reviews the complete post-application GDD.
- QD-TUNING and QD-COSMETIC require formal lean or full; QD-LOCAL requires full.
- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
- Review evidence must use cgs.review-evidence/v1, formal APPROVED, independent,
  current target path/revision, required depth, and recomputable report/evidence
  revisions. solo/advisory/partial cannot approve.

Record:

- A separate recorder re-reads proposal, application receipt, current GDD,
  review evidence/report, and expected lifecycle predecessor before appending.
- APPLIED/SUPERSEDED records use contract cgs.quick-design-lifecycle/v2 and an
  explicit fresh path:

      design/quick-specs/<change-id>/<version>/records/<record-id>.md

- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
- SUPERSEDED binds the same identity graph plus successor proposal path/revision and
  Implementation Eligible NO.

Records are append-only. Never select by mtime. Conflicts, stale revisions, reused
roles, missing receipts, or unexpected pre-state authorize nothing. quick-design
never writes these artifacts.

## Phase 8: Read-only status and re-application safety

Allocate a collision-checked stable ID from declared domain identifiers plus a UUID or run-scoped sequence; never derive it from file bytes.

Without record: PROPOSED; CURRENT only if every production base/index/section/
dependency binding still matches; Implementation Eligible NO.

With APPLIED: YES requires simultaneously:

- proposal and lifecycle v2 identities/revisions match;
- application v1 receipt binds proposal, expected pre-base, applied delta IDs,
  and current post-GDD revision;
- current GDD equals post revision;
- independent review evidence v1 is APPROVED at required depth and targets that
  same current path/revision;
- record predecessor and recorder independence are valid;
- no valid SUPERSEDED record is supplied; and
- every explicit reference revalidates.

If any check fails, preserve reported record status for audit but Currentness is
STALE/INVALID and eligibility NO. Never repair it.

An APPLIED proposal is not reapplied to later GDD bytes. A desired follow-up uses
a new version, explicit predecessor, current base, new decisions/risk record,
fresh application receipt, review, and lifecycle record.

Valid SUPERSEDED always has eligibility NO and reports exact successor.
EXPERIMENT_ONLY never becomes APPLIED.

A production story may cite proposal as rationale only. Its authoritative source
must be the updated current GDD path/revision plus exact current APPLIED record
path/revision. Separate story-readiness remains required; this workflow never chains
to implementation.

## Final response contract

Report:

- exact inspected/created paths and raw-byte revisions;
- target system/section identities;
- Use the artifact declared schema, stable ID, and monotonic revision; do not compute a content-derived token.
- decision IDs/owners and unresolved routed questions;
- all six status axes;
- exact non-writes;
- application/review/record next owners; and
- structured error/partial/redirect reason when applicable.

Never end proposal creation with ready for implementation. Use:

    Proposal created; separate authoritative application, independent review,
    and lifecycle recording are required.

Recommend story-readiness only after exact status validation returns APPLIED,
CURRENT, and Implementation Eligible YES. Never chain into dev-story.

## Authoritative P1 traceability

This matrix links the audit rows to existing clauses; it grants no additional
write or lifecycle authority.

| Audit ID | Closing contract clause |
|---|---|
| QDS-005 | Phases 2–4 persist typed risk facts and user-owned decisions before any profile label. |
| QDS-006 | Phase 1 resolves one exact GDD, stable system owner, and explicit sections. |
| QDS-007 | Phase 6 uses compare-and-create identity/atomic conflict check and forbids same-day overwrite. |
| QDS-008 | Phases 2 and 3 redirect any tuning outside the approved range. |
| QDS-009 | Phase 3 routes production new-system work to the systems-index/design owner. |
| QDS-010 | Phases 7 and 8 bind base/predecessor/currentness and make re-application ineligible. |
| QDS-011 | Status axes and precedence distinguish invalid, partial, blocked, declined, and persistence failure. |
| QDS-012 | The final response contract exposes exact revisions while the formal spec keeps catalog evidence unexecuted until run. |
