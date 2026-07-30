---
name: brainstorm
description: "Collaboratively author or safely revise one game concept through bounded ideation, user-owned decisions, finite convergence, immutable checkpoints, section-scoped CAS, and a revision-bound independent concept-review handoff."
---

# Brainstorm

Facilitate product decisions; never make them for the user. Author exactly one
game concept, preserve decision/evidence provenance, and stop with authoring
evidence plus an optional independent read-only review handoff.

Do not implement a game, choose an engine, publish market claims, create a formal
schedule, invoke a system-GDD reviewer, approve the concept, or start downstream
workflows.

## Invocation and request contract

Invoke only as:

    $brainstorm <request-manifest-path>

No argument prints that usage and stops before repository discovery, target/
context reads, delegation, authorization, or writes.

The manifest declares `contract: cgs.brainstorm-request/v2` and:

- stable session, run, and concept artifact IDs;
- exact operation `new`, `resume`, or `revise`;
- exact target `design/gdd/game-concept.md`, checkpoint root, expected target
  revision or `ABSENT`, and expected checkpoint predecessor ID/revision or `ABSENT`;
- for `revise`, ordered selected stable section IDs; for `resume`, ordered IDs or
  an instruction to collect them once from OPEN/DRAFT inventory before mutation
  authorization;
- `review_mode: full | lean | solo`, separately from
  `research_mode: none | receipts-only | authorized-current`;
- exact source/reference, research, platform/technical-preference, estimate,
  gate, approval, workflow-catalog, and instruction evidence with stable ID/
  owner/path-or-URL/locator/raw revision and required/optional role;
- context budget no larger than 16 files and 524288 exact bytes;
- ideation count from two to four per round, no more than two concept rounds, no
  more than two revisions per decision family, and delegation limits at or below
  this contract;
- actual product-decision owner, mutation authority, author, target writer,
  checkpoint recorder, gate-node roles, and intended independent concept-reviewer
  role; and
- authorization manifest ID/revision/authority or instruction to collect one bounded
  mutation authorization after inventory, plus exact non-writes.

Reject unknown/duplicate fields, unsafe/aliased paths, duplicate IDs, invalid
operation/mode, malformed or missing declared revision, target/checkpoint aliasing, budgets above
the hard caps, review/gate identity equal to author/writer/recorder, or limits
above the finite-convergence contract.

`new` requires target `ABSENT`. Existing target `resume`/`revise` requires its
current raw revision. Checkpoint resume requires one exact v2 checkpoint chain;
never select newest/latest files or silently change operation.

Use runtime task identities when exposed. Otherwise generate one lowercase UUID
per task role and persist it. Never claim the user, a gate, research source, or
another agent identity.

## Roles, ownership, and one mutation boundary

- The user or named product owner owns concept selection, core fantasy/player
  promise, loop, pillars/anti-pillars, audience intent, visual anchor, platform
  intent, MVP/scope tradeoffs, risk acceptance, and explicit deferrals.
- The author asks, presents options, drafts, and performs semantic preflight.
- Gate nodes are bounded read-only advisers; they never choose product outcomes.
- The target writer performs concept skeleton/final section CAS writes only.
- The checkpoint recorder creates immutable checkpoints/authoring receipt only.
- A future fresh independent concept-review task is read-only and separate from
  every author/gate/writer/recorder identity.

After target/section inventory and selected-set confirmation, present one mutation
manifest covering:

- exact target operation (`new`: create skeleton then modify authorized sections;
  `resume/revise`: modify only selected stable-ID sections/header fields);
- expected target preimage/ABSENT and selected section preimage revisions;
- checkpoint root and deterministic create-only checkpoint/receipt names;
- author/profile/content schema, writer/recorder identities, limits, and non-writes.

Obtain one explicit authorization from the named mutation authority. It covers
that target boundary and create-only checkpoint/receipt sequence for this run.
Later product decisions and exact-draft approvals are content approval, not new
filesystem authority. A new path, operation, selected section, owner, writer, or
larger limit requires a revised manifest and new authorization.

## Versioned concept schema and content profile

The author contract version is:

    brainstorm-author-revision:<explicit skill release revision>

The target uses document schema `GC-1`, profile
`game-concept-profile-schema-v2`, and assertion contract
`cgs.game-concept-content-profile/v2`. Stable section IDs, never titles, govern
inventory, selection, decisions, assertions, CAS, revisions, and receipts.

| Stable ID | Product owner | Required purpose |
|---|---|---|
| `CONCEPT-CORE-IDENTITY` | product owner | title, pitch, fantasy, hook |
| `CONCEPT-PLAYER-EXPERIENCE` | product owner | emotion, promise, motivation |
| `CONCEPT-CORE-LOOP` | product owner | moment, short, session, progression loops |
| `CONCEPT-PILLARS` | product owner | 3–5 definitions and decision tests |
| `CONCEPT-ANTI-PILLARS` | product owner | at least three explicit boundaries |
| `CONCEPT-AUDIENCE` | product owner | audience intent, exclusions, evidence labels |
| `CONCEPT-VISUAL-ANCHOR` | product owner | stable anchor ID, rule, principles |
| `CONCEPT-PLATFORM-CONSTRAINTS` | product owner | intent, observed constraints, deferred engine |
| `CONCEPT-MVP` | product owner | smallest core-uncertainty test |
| `CONCEPT-SCOPE-TIERS` | product owner | MVP, fallback, full-vision boundaries |
| `CONCEPT-RISKS` | product owner | design/technical/production/evidence risks |
| `CONCEPT-ASSUMPTIONS` | product owner | market/schedule/content/resource labels |
| `CONCEPT-OPEN-QUESTIONS` | product owner | explicit owner/impact/blocking/deferral |
| `CONCEPT-PROVENANCE` | authoring recorder | decisions, sources, gates, revisions only |

Unknown custom sections get stable preservation IDs and remain user-owned. They
are byte-preserved unless explicitly selected under a revised authorized set.

Every target begins with:

    # Game Concept

    > **Schema**: GC-1
    > **Profile Version**: game-concept-profile-schema-v2
    > **Content Profile**: cgs.game-concept-content-profile/v2
    > **Author Schema**: brainstorm-author-<explicit revision>
    > **Concept Artifact ID**: <stable ID>
    > **Content Status**: DRAFT | PARTIAL | CONTENT_COMPLETE
    > **Approval Status**: EXTERNAL EVIDENCE REQUIRED
    > **Context Manifest revision**: <revision>
    > **Authoring Receipt ID**: <stable ID | PENDING>

Never write `APPROVED`, reviewer identity/signature/date, approval-record path/
revision, or authoring-receipt path/revision into the concept. External evidence binds
already-final target bytes and avoids a target/receipt revision cycle.

## Independent state axes

For each canonical/custom section checkpoint:

- `content_state`: `EMPTY`, `PLACEHOLDER`, `SUBSTANTIVE`, or
  `EXPLICITLY_OPEN`;
- `evidence_state`: `CURRENT`, `USER_ASSUMPTION`, `MODEL_HYPOTHESIS`, `UNKNOWN`,
  `STALE`, or `CONFLICTING`;
- `workflow_state`: `PENDING`, `DRAFTING`, `APPROVED_NOT_WRITTEN`, `WRITTEN`,
  `PRESERVED`, `BLOCKED`, or `OUT_OF_SCOPE`;
- `assertion_results`: stable ID, `PASS/FAIL`, applicability, evidence, owner;
- `section_status`: `INCOMPLETE`, `COMPLETE`, `INVALID`, or `STALE`; and
- decision, exact-body approval, source, gate, and revision IDs.

Section COMPLETE requires substantive or profile-permitted explicitly-open
content, passing assertions, honest evidence labels, current exact-body user
approval, and no blocking conflict. Heading existence/non-placeholder length is
not completeness.

Target content status:

- DRAFT: authorized skeleton exists without a complete selected body;
- PARTIAL: safe selected work exists but any required section/assertion/evidence/
  gate/decision remains incomplete, invalid, stale, conflicting, or blocking;
- CONTENT_COMPLETE: all required sections pass the content profile, only permitted
  explicitly deferred nonblocking questions remain, and target/context bytes are
  current. A verified authoring receipt is still required before Workflow Verdict
  READY_FOR_REVIEW or a review handoff.

Selected-run completion and whole-concept readiness are separate.

## Concept approval and evidence boundary

User selection/section approval establishes product intent, not independent
concept approval. Only a separate immutable `cgs.concept-approval/v1` record from
a fresh independent concept-review task may support `APPROVED`, and only when it:

1. declares concept profile `GC-1/game-concept-profile-schema-v2` and verdict
   `APPROVE`;
2. binds current target, authoring receipt, section/assertion/context revisions;
3. names author/gate/reviewer identities and proves separation;
4. includes current findings/open-question disposition; and
5. still matches all current bytes.

CONCERNS, REJECT, self/wrong-profile review, stale target/context/receipt, user
risk acceptance, or conversation approval cannot establish approval. Authoring
only emits a review handoff; it never invokes/writes this evidence.

## Phase 0: Parse request and validate exact source identity

Parse request first. Validate contract, operation, modes, IDs, paths, revisions,
roles, budgets, limits, and non-writes before context or ideation.

Resolve review behavior:

- `full`: run the deterministic read-only advisory gate DAG in Phase 7; it is not
  the independent final concept review.
- `lean`: all advisory nodes are `NOT_RUN_BY_MODE`; no gate agents spawn.
- `solo`: all advisory nodes are `NOT_RUN_BY_MODE`; spawn zero subagents.

Resolve research separately. `none` forbids research; `receipts-only` reads exact
declared receipts; `authorized-current` may collect only the bounded current
research evidence authorized by the request and records receipts. Research never
selects the concept.

For target `new`, prove absence. For `resume/revise`, read raw bytes, preserve
encoding/newlines, parse stable/custom sections and provenance, and verify current
revision. For checkpoint resume, validate exact session/run and v2 predecessor chain,
source ABSENT/revision, selected set, draft snapshot, and next transition.

Invalid input returns ERROR with zero writes. Missing/changed source,
instructions, authorization identity, or unsafe paths returns BLOCKED with zero
target writes.

## Phase 1: Inventory sections, choose resume scope, authorize once

Create the complete section/ownership table with headings, byte ranges, revisions,
content/evidence/workflow/assertion state, dependencies, decision/approval/
revision IDs, gate receipts, and custom preservation IDs.

Mode rules:

- `new`: all canonical sections selected for eventual target creation; concept
  ideation still begins from alternatives rather than a preselected answer.
- `resume`: show inventory and let the user select OPEN/DRAFT sections once;
  existing COMPLETE sections remain PRESERVED unless explicitly selected.
- `revise`: only request-declared IDs are selected; reject scope expansion.
- In existing targets, non-selected canonical/custom ranges remain byte-identical.
- Selecting a section never silently selects or writes its dependencies.

Linked `game-pillars.md`, art, architecture, or other project artifacts are
read-only evidence; disagreement creates an owned finding, never dual-write.

After selected-set confirmation, perform the one mutation authorization described
above. Do not ask for another write approval per checkpoint, decision, gate,
section, final exact body, or receipt while the boundary remains unchanged.

## Phase 2: Load bounded ideation context

After authorization select candidates in stable order:

1. applicable `AGENTS.md` root-to-target/checkpoint;
2. exact target and checkpoint chain;
3. exact request-declared concept/pillar/product references;
4. exact prior gate/approval evidence;
5. exact research receipts/snapshots;
6. exact platform/technical-preference evidence;
7. exact estimate evidence; and
8. exact workflow-catalog row evidence.

Never scan all GDDs/sessions, choose latest files, or follow undeclared links.
Count every loaded file against hard maxima 16 files and 524288 exact bytes.
Determine exact size before load; never truncate.

The ordered context manifest records path/URL snapshot, role, stable ID/owner,
locator, bytes, raw revision, observed date when temporal, dependency edge,
loaded/omitted state, and reason. Canonicalize UTF-8 LF, fixed fields, no trailing
whitespace, one final newline; persist its revision.

Mark an existing concept `mutable-target-baseline`: its baseline is provenance,
but target currentness is checked separately by Target/Section CAS after writes.
All external entries are re-read before dependent use/final handoff.

If mandatory evidence exceeds budget, is absent, or mismatches declared revision,
append at most one authorized PARTIAL checkpoint with
`CONTEXT_BUDGET_EXCEEDED` or `CONTEXT_EVIDENCE_INVALID`, leave target unchanged,
list loaded/omitted evidence, and stop. Required context is never silently omitted.

Only after context succeeds, summarize user decisions, current evidence,
hypotheses/assumptions/unknowns, derived concept constraints, and routed questions;
then ask the first product question.

## Phase 3: Skeleton and cgs.brainstorm-checkpoint/v2 chain

For `new`, the target writer first performs CAS on ABSENT and atomically creates
the complete GC-1 header plus every canonical stable-ID heading with neutral
placeholders. Read back exact bytes before drafting; do not fill a selected
concept silently. Existing targets remain unchanged during drafting.

Append create-only `cgs.brainstorm-checkpoint/v2` records after discovery brief,
every concept-selection/decision family, every gate node, content preflight,
final target attempt, and receipt attempt. Each contains request/authorization/
context/target/author-schema revisions, complete section axes, selected/preserved
IDs, decisions/approvals/revisions, draft snapshot, gate/research/estimate
evidence, convergence counters, findings/open questions, roles, operation ledger,
budgets, predecessor ID/revision, next legal transition, and UTC timestamp.

record_revision is an explicit monotonic revision assigned by the recorder. Append by deterministic
name through predecessor/create-if-absent CAS. Never overwrite or fork a chain.

Checkpoint state is continuity/provenance, not target content, review, approval,
market validation, engine recommendation, or estimate evidence.

## Required continuation

Read and follow `references/continued-workflow.md` in full after Phase 3. It
defines bounded ideation and convergence, decision/evidence provenance, gate DAG
failure results, content assertions, exact-body approval, five-part CAS, authoring
receipt, independent concept-review handoff, resume, and safe stop behavior.

## Non-implementation boundary

This workflow writes only its authorized concept target and create-only
checkpoint/authoring-receipt records. It never writes pillars, research source,
estimate, engine/platform setup, review/approval record, shared catalog, art,
architecture, backlog, code, assets, production state, or publication. It invokes
no downstream recommendation.
