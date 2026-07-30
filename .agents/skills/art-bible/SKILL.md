---
name: art-bible
description: "Author or safely revise one versioned nine-section Art Bible through bounded evidence, explicit product decisions, content-profile assertions, transactional section writes, and a revision-bound independent-review handoff."
---

# Art Bible

Author exactly one `AB-1` Art Bible. The authoring task may write only the exact
Art Bible target and create-only checkpoint/authoring-receipt records named by
the request. It never creates art assets, implementation files, a review verdict,
or production approval.

## Invocation and request contract

Invoke only as:

    $art-bible <request-manifest-path>

No argument prints that usage and stops before repository discovery, context
reads, delegation, or writes. Reject positional flags and unknown fields.

The manifest declares `contract: cgs.art-bible-request/v2` and:

- stable artifact/run IDs and exact operation: `create`, `fill-gaps`,
  `revise-sections`, `migrate-schema`, or `resume`;
- exact scope alias (`full`, `core`, `asset-standards`, or `custom`) plus ordered
  stable section IDs; aliases never redefine whole-artifact completeness;
- exact target path, checkpoint root, expected target revision or `ABSENT`, and
  expected latest checkpoint ID/revision or `ABSENT`;
- declared legacy input path/revision and migration disposition when applicable;
- exact concept artifact/approval evidence, platform/engine profile evidence,
  accessibility/UX owners, technical constraints, workflow-catalog row, and
  reference-source evidence, each with path, stable ID/owner, locator, raw revision,
  and required/optional role;
- context budgets no larger than 16 files and 524288 exact bytes;
- `review_mode: full | lean | solo` and
  `consultation_mode: bounded | none`; `solo` forces `none` and zero subagents;
- product-decision owner, mutation authority, author task, checkpoint-recorder
  task, and intended future reviewer role; identities must be distinct where
  roles require separation;
- max revision rounds, consultation limits at or below this contract, and exact
  non-writes; and
- authorization manifest ID/revision/authority or an instruction to collect one
  explicit bounded authorization after inventory.

Reject ambiguous IDs, duplicate paths/section IDs, malformed or missing declared revision values,
target/checkpoint aliasing, target outside `design/art/`, checkpoint root outside
the declared session-state root, a writer equal to mutation authority when the
request separates them, a future reviewer equal to any author/consultant/recorder,
or budgets/limits above this contract.

Use runtime task identities when exposed. Otherwise generate one lowercase UUID
per role and persist it; never claim a user, director, or another task identity.

## Roles and authority boundary

- The product-decision owner selects visual product choices.
- The mutation authority authorizes exact target regions and create-only
  checkpoint/receipt names.
- The author asks questions, drafts, and performs semantic preflight.
- The target writer performs target CAS writes only.
- The checkpoint recorder creates checkpoint/authoring-receipt records only.
- Optional consultants provide read-only evidence proposals.
- A future independent `art-director` review task may run `AD-ART-BIBLE`; it is
  not invoked by this authoring workflow.

One mutation authorization covers the listed target operation/sections and
deterministically named checkpoint/receipt records for this run. Section-content
approval is not filesystem authorization. A new path, operation, section, owner,
writer, or larger limit requires a revised manifest and new authorization.

## Versioned schema and content profile

The author contract version is:

    art-bible-author-revision:<explicit skill release revision>

The document profile is `art-bible-profile-schema-v2`; the content assertion
contract is `cgs.art-bible-content-profile/v2`. Stable IDs, not display titles,
govern inventory, migration, decisions, assertions, writes, and receipts.

| Stable ID | Canonical display title | Coverage owner |
|---|---|---|
| `AB-01` | Visual Identity Statement | core visual rules and tests |
| `AB-02` | Mood, Lighting & Atmosphere | emotional states, lighting, atmosphere |
| `AB-03` | Shape, Composition & Silhouette | geometry, composition, readability |
| `AB-04` | Color System & Accessibility | roles, semantics, area, backup cues |
| `AB-05` | Typography & Iconography | hierarchy, personality, icons, legibility |
| `AB-06` | Character Art Direction | archetypes, silhouette, pose, camera/LOD |
| `AB-07` | Environment & Level Art Direction | architecture, materials, density, story |
| `AB-08` | UI/HUD & VFX Visual Language | presentation, motion, effects, readability |
| `AB-09` | Asset Standards, References & Prohibitions | budgets, formats, naming, rights, avoid rules |

Every target begins with:

    # Art Bible

    > **Schema**: AB-1
    > **Profile Version**: art-bible-profile-schema-v2
    > **Content Profile**: cgs.art-bible-content-profile/v2
    > **Author Schema**: art-bible-author-<explicit revision>
    > **Artifact ID**: <stable ID>
    > **Artifact Status**: DRAFT | PARTIAL | COMPLETE
    > **Production Use**: BLOCKED — independent current-revision approval required
    > **Concept Evidence ID**: <stable approval ID | MISSING>
    > **Platform/Engine Profile IDs**: <stable IDs | MISSING>
    > **Context Manifest revision**: <revision>
    > **Authoring Receipt ID**: <stable ID | PENDING>

Do not write `APPROVED`, reviewer identity/signature/date, a review-record revision,
or authoring-receipt path/revision into the Art Bible. External records bind final
target bytes and avoid a target/receipt revision cycle.

## Independent state axes

For each `AB-01` through `AB-09`, checkpoint separately:

- `content_state`: `EMPTY`, `PLACEHOLDER`, `SUBSTANTIVE`, or `NOT_APPLICABLE`;
- `evidence_state`: `CURRENT`, `STALE`, `PROVISIONAL`, `MISSING`, or `CONFLICTING`;
- `workflow_state`: `PENDING`, `DRAFTING`, `APPROVED_NOT_WRITTEN`, `WRITTEN`,
  `BLOCKED`, or `OUT_OF_SCOPE`;
- `assertion_results`: stable assertion ID, `PASS/FAIL`, evidence, and owner; and
- `section_status`: `INCOMPLETE`, `COMPLETE`, `INVALID`, or `STALE`, derived from
  the other axes rather than placeholder detection.

`COMPLETE` section means substantive content, all applicable assertions passing,
current evidence, current exact-body product approval, and no blocking finding.
`SECTION_REVIEWED` is optional metadata and never whole-artifact approval.

Artifact status is content-derived:

- `DRAFT`: skeleton exists and no selected section has an approved write;
- `PARTIAL`: safe content exists but fewer than all nine sections are COMPLETE,
  or any required dependency is provisional/missing/conflicting/stale;
- `COMPLETE`: all nine unique sections are COMPLETE, the approved concept evidence
  is current, no provisional/unmapped/blocking item remains, and target bytes
  read back stably.

Selected-scope completion is reported separately and never upgrades the artifact.

## Production safety invariant

Production remains blocked unless a separate immutable
`cgs.art-bible-review/v1` record from a fresh independent `art-director`:

1. declares gate `AD-ART-BIBLE` and verdict `APPROVE`;
2. names `AB-1`, all nine section revisions, current dependencies, and author IDs;
3. proves reviewer separation;
4. binds the current complete target revision and verified authoring receipt; and
5. still matches current target/context bytes.

A user risk acceptance, section approval/review, scoped completion, authoring
receipt, `CONCERNS`, or status text inside the target cannot replace this gate.

## Phase 0: Parse request and resolve independent modes

Parse the invocation and request before any authoring context. Validate contract,
IDs, paths, revisions, roles, budgets, operation, scope, and non-writes.

Resolve modes independently:

- `review_mode: full` permits an independent review handoff only after a COMPLETE
  receipted artifact; it does not invoke a reviewer here.
- `lean` performs authoring/optional bounded consultation but emits no formal
  review handoff; COMPLETE remains UNREVIEWED and production-blocked.
- `solo` performs local authoring with the user, forces consultation `none`,
  spawns zero subagents/directors, and remains UNREVIEWED.
- `consultation_mode: bounded` permits only Phase 8 read-only consultations and
  never reserves or consumes the independent reviewer identity.

Invalid input returns `ERROR` with zero repository writes. Missing mandatory
identity/authorization evidence returns `BLOCKED` with zero target writes.

## Phase 1: Inventory target and authorize one mutation boundary

Read only applicable `AGENTS.md`, exact request, target if present, and profile
sources needed to identify the mutation. Inventory raw target bytes, header,
stable-ID anchors/ranges, duplicates, unknown content, per-section revisions, current
artifact/review status, and expected checkpoint head.

Operation rules:

- `create`: target must be `ABSENT`; selects exact skeleton plus requested bodies.
- `fill-gaps`: selects only EMPTY/PLACEHOLDER sections; never rewrites substantive
  content.
- `revise-sections`: selects explicit substantive sections and records why their
  accepted meaning may change.
- `migrate-schema`: maps every legacy byte range without new section content.
- `resume`: requires an exact valid v2 checkpoint chain and resumes only its next
  legal transition.

Present one mutation manifest before broader context loading:

    Operation / scope / stable section IDs
    Target / expected target revision or ABSENT
    Checkpoint root / expected predecessor ID and revision
    Deterministic checkpoint and authoring-receipt names
    Artifact/run/profile/content/author-schema IDs
    Writer/recorder identities and limits
    Exact non-writes

Obtain one explicit authorization from the named mutation authority if the
request does not already bind a current authorization revision. Do not ask again for
filesystem permission for later approved section bodies inside this boundary.

## Phase 2: Load bounded revision-manifested context

After authorization, select candidates in stable order:

1. applicable `AGENTS.md` root-to-target;
2. target and latest checkpoint chain;
3. exact concept artifact plus its approval evidence;
4. exact platform/engine and technical-budget profiles;
5. exact accessibility and UX owner artifacts;
6. exact owned product/pillar requirements;
7. exact workflow-catalog row evidence;
8. declared reference sources in manifest order.

Never glob all GDDs/art files or follow undeclared references. Count every loaded
file, including AGENTS, target, checkpoint, and evidence, against hard maxima 16
files and 524288 exact bytes. Determine size before load; never truncate.

The context manifest records ordered path, role, stable IDs/owners, locator,
bytes, raw revision, dependency edge, loaded/omitted state, and reason. Canonicalize
the manifest as UTF-8 LF, fixed field order, no trailing whitespace, one final
newline, then store its revision.

Mark an existing target `mutable-target-baseline`: its baseline remains
provenance, but target currentness is checked by Target/Section CAS rather than as
external context after an authorized write. re-read every external context entry
before each dependent write and final handoff.

If mandatory context exceeds budget, is absent, or mismatches its declared revision,
append at most one authorized PARTIAL checkpoint with reason
`CONTEXT_BUDGET_EXCEEDED` or `CONTEXT_EVIDENCE_INVALID`, leave target unchanged,
list loaded/omitted evidence, and stop. Required evidence is never silently
omitted.

Only after bounded context succeeds, summarize product decisions, hard evidence,
derived visual constraints, technical handoffs, provisional assumptions, and
dependency findings; then ask the first product question.

## Phase 3: Detect/migrate schema and plan exact sections

For AB-1, inventory all nine IDs using the v2 content assertions; non-placeholder
text alone never proves completeness. Reject duplicate/missing IDs and ambiguous
anchors before writes.

For legacy/unknown schema, create a read-only mapping proposal containing every
source byte range/revision, proposed AB-1 destinations, move/split/merge action,
ambiguity, preserved bytes, and `UNMAPPED` disposition. Show exact before/after
diff. Only `migrate-schema` plus accepted mapping and current CAS may rewrite.
Preserve unresolved content in an explicit appendix; unresolved mapping blocks
COMPLETE and review handoff. Migration alone grants no completeness or approval.

Build an ordered plan for selected sections with assertion results, source revisions,
decision dependencies, exact byte anchors/baselines, writer, and expected
operation. re-read target, authorization, and used context after plan approval;
mismatch returns `ERROR — TARGET/CONTEXT/AUTHORIZATION CHANGED`, zero write.

## Phase 4: Create/migrate skeleton and initialize checkpoint chain

After context and plan succeed, the target writer performs authorized CAS writes.
Fresh creation first writes the full header and all nine exact stable-ID headings
in one skeleton transaction; unselected bodies receive neutral placeholders.
Create no substantive body before the skeleton read-back succeeds.

Migration writes only the accepted lossless mapping, header, and nine-section
structure; do not mix migration with invented content.

Append a create-only `cgs.art-bible-checkpoint/v2` record containing request/
authorization/context/target/profile revisions, roles, modes, full section axes,
assertions, decisions/revisions, operation ledger, consultations/findings,
budgets, predecessor ID/revision, next legal transition, and UTC timestamp. Canonical
payload revision excludes its own `record_revision`; predecessor CAS prevents forks.

The final create-only `cgs.art-bible-authoring-receipt/v1` is written only after
final target content/header CAS and read-back revision. It binds pre/post target
revisions, context revision, author/profile/content schema, all section/revision/
decision IDs, authorization, writer/recorder identities, final checkpoint, and
target path. It is authoring evidence, never review approval.

If checkpoint/receipt persistence fails after a verified target write, leave the
content-derived artifact status intact, report Workflow Verdict PARTIAL with the
exact unreceipted target revision, emit no review handoff, and never replay the write.

## Required continuation

Read and follow `references/continued-workflow.md` in full after Phase 4. It
defines decision/revision provenance, section assertions and approvals,
transactional CAS, concept/platform/dependency rules, bounded consultation,
receipt finalization, independent-review handoff, resume, and catalog-driven
close behavior.

## Non-implementation and review boundary

This workflow stops after authoring evidence and, when eligible, a review handoff
for exact target/receipt/context revisions. It does not invoke `AD-ART-BIBLE`, create
or modify review records, mark itself approved, update shared catalogs, generate
assets, configure engines, or implement UI/art. Conversation memory, self-review,
the wrong role, stale revisions, or missing receipts cannot authorize production.
