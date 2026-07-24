---
name: ux-design
description: "Author one versioned screen, HUD, or interaction-pattern UX artifact through explicit modes, content-profile validation, bounded evidence, decision provenance, CAS writes, and a hash-bound review receipt."
---

# UX Design

Author exactly one UX artifact. Do not treat author approval as independent
review, temporary platform answers as durable facts, missing foundations as
harmless, or this workflow as owner of accessibility/global-pattern artifacts.

The maximum write set is one target UX artifact plus immutable records under its
declared checkpoint root. Never write another UX artifact, a GDD, data, code,
visual asset, translation, ADR, accessibility foundation, global pattern
library outside the dedicated library profile, review record, or implementation.

## Invocation and request contract

Invoke only as:

    $ux-design --manifest <exact-request-path> [--resume <exact-checkpoint-path>]

With no manifest, print this usage and stop before repository reads,
delegation, decisions, authorization, or verdict. Reject unknown/duplicate
flags, missing values, directories, URLs, globs, unsafe IDs, traversal,
symlink/junction escapes, and unsupported schema.

The manifest contract is cgs.ux-design-request/v2 and must declare:

- stable artifact ID, run ID, profile, and screen ID where applicable;
- profile: ux-spec, hud-design, or interaction-pattern-library;
- mode: create, fill-gaps, revise-sections, or migrate-schema;
- exact target path and expected raw-byte SHA-256, or ABSENT for create;
- exact selected stable section IDs for revise-sections and expected baseline
  body hashes;
- exact context paths/hashes, requirement IDs/owners, and one-hop navigation
  neighbor IDs/paths/hashes;
- requested context budgets not exceeding 16 files and 524288 exact bytes;
- platform contract cgs.platform-input-profile/v1: stable profile ID, version,
  exact path/hash, supported platforms/devices/inputs, resolutions/aspects,
  safe zones, text scales, and primary input, or MISSING;
- accessibility foundation stable ID, version/tier, exact path/hash, external
  owner, or MISSING;
- pattern-library path/hash and external UX-library owner, or ABSENT;
- player-journey and art-bible exact paths/hashes when applicable;
- product decision owner, mutation authority, target writer task identity,
  checkpoint recorder task identity, maximum revision rounds at most 3,
  consultation limits at or below this contract, and checkpoint root;
- exact target/checkpoint mutation boundary and explicit non-writes.

IDs are stable slugs/UUIDs, never dates alone. create requires an absent target;
other modes require an existing target matching expected hash. The exact target
must be stated:

- ux-spec: design/ux/<screen-id>.md
- hud-design: design/ux/hud.md with screen ID hud
- interaction-pattern-library: design/ux/interaction-patterns.md

One run never creates both a screen/HUD artifact and the global library. It
never creates design/accessibility-requirements.md.

Use runtime task identities when exposed. Otherwise generate one lowercase UUID
once per role and record codex-task:<uuid>; never claim the user, consultant,
person, or unavailable external task as byte author/recorder.

## Versioned profile and content contracts

The exact bytes of this SKILL.md, one NUL byte, and the exact bytes of
references/continued-workflow.md define author_schema_hash. Record:

- Profile Version: ux-profile-schema-v2
- Content Profile: cgs.ux-content-profile/v2
- Schema Version: ux-design-author-sha256:<author_schema_hash>

Each section has one stable ID and exact H2 heading. Emit its ID immediately
before the heading:

    <!-- ux-section: UXS-01 -->
    ## Purpose & Player Need

IDs, not display labels, govern migration, selection, decisions, findings,
revision records, checkpoints, and review.

### Profile ux-spec

| ID | Exact required H2 heading | Content-profile contract |
|---|---|---|
| UXS-01 | Purpose & Player Need | Player goal/outcome and owned requirement IDs |
| UXS-02 | Player Context on Arrival | Prior activity/state/pressure and journey evidence |
| UXS-03 | Navigation Position | Stable root/parent/screen hierarchy and alternate access |
| UXS-04 | Entry & Exit Points | Trigger, source/destination IDs, carried state, irreversible effect |
| UXS-05 | Layout Specification | Hierarchy, zones, components, viewport/profile assumptions |
| UXS-06 | States & Variants | Default and applicable loading/empty/populated/error/locked/platform states |
| UXS-07 | Interaction Map | Component/input/focus/feedback/outcome/cancel/recovery |
| UXS-08 | Events Fired | Action to stable event/payload/owner or source-backed none |
| UXS-09 | Transitions & Animations | Enter/exit/state transitions, interrupt, reduced-motion equivalent |
| UXS-10 | Data Requirements | Source owner, read/write intent, update, null/stale/privacy behavior |
| UXS-11 | Accessibility | Trace to external tier/profile; no local tier selection |
| UXS-12 | Localization Considerations | Locale formatting, expansion/reflow, strings, bidirectionality targets |
| UXS-13 | Acceptance Criteria | Requirement/decision-linked executable local UX conditions |
| UXS-14 | Open Questions | Stable finding/dependency IDs, owner, state, destination, next action |

UXS-05 requires exact H3 headings Information Hierarchy, Layout Zones, and
Component Inventory. A wireframe is optional schematic evidence and declares
viewport/scale assumptions; it is not pixel authority.

### Profile hud-design

| ID | Exact required H2 heading | Content-profile contract |
|---|---|---|
| HUD-01 | HUD Philosophy | Approved density principle and measurable implications |
| HUD-02 | Information Architecture | Requirement-linked inventory and visibility rationale |
| HUD-03 | Layout Zones | Platform/safe-zone/aspect/viewport/attention assumptions |
| HUD-04 | HUD Elements | Stable element IDs, owner, data/visibility/update/pattern/states |
| HUD-05 | Dynamic Behaviors | Context transitions, priority/contention, reduced motion |
| HUD-06 | Platform & Input Variants | Every declared platform/input/resolution/text-scale variant |
| HUD-07 | Accessibility | External-tier trace, non-color/focus/assistive/reflow behavior |
| HUD-08 | Open Questions | Stable finding/dependency IDs, owner, state, next action |

### Profile interaction-pattern-library

| ID | Exact required H2 heading | Content-profile contract |
|---|---|---|
| PAT-01 | Overview | Scope, external owner, consumers, profile/hash provenance |
| PAT-02 | Pattern Catalog | Canonical ID/name/category/version/status/entry anchor |
| PAT-03 | Patterns | Owner-approved states, inputs, feedback, accessibility, use/non-use |
| PAT-04 | Gaps & Patterns Needed | Local proposal IDs/source screen/owner/disposition |
| PAT-05 | Open Questions | Stable finding/dependency IDs, owner, state, next action |

Global IDs use UXP-GLOBAL-<slug>. Screen/HUD runs may record only
UXP-<screen-id>-<slug> local proposals inside their target. Only an independently
authorized interaction-pattern-library run owned by the external library owner
may merge canonical patterns.

## Required artifact header

Every target begins with:

    > **Artifact Type**: ux-spec | hud-design | interaction-pattern-library
    > **Schema Version**: ux-design-author-sha256:<author_schema_hash>
    > **Profile Version**: ux-profile-schema-v2
    > **Content Profile**: cgs.ux-content-profile/v2
    > **Artifact ID**: <stable-artifact-id>
    > **Screen ID**: <stable-screen-id | N/A-library>
    > **Status**: DRAFT | PARTIAL | READY_FOR_REVIEW
    > **Author Task ID**: <actual-writer-task-id>
    > **Last Updated UTC**: <RFC3339 seconds Z>
    > **Platform Target**: <declared targets | DEPENDENCY-GAP>
    > **Platform Profile ID**: <stable ID | MISSING>
    > **Platform Profile Version**: <version | MISSING>
    > **Platform Profile SHA-256**: <sha256 | MISSING>
    > **Input Profile IDs**: <stable IDs | MISSING>
    > **Accessibility Foundation**: <ID/version/path/hash/tier | MISSING>
    > **Requirement IDs**: <stable IDs and owners>
    > **Context Manifest SHA-256**: <hash>
    > **Authoring Receipt ID**: <stable receipt ID | PENDING>

Temporary user answers cannot replace a platform/input/accessibility source. If
needed to continue safe drafting, persist them as PROVISIONAL derived decision
records plus OPEN dependency findings; dependent sections cannot be VALID and
the artifact cannot be READY_FOR_REVIEW.

## Independent state axes

Section inventory keeps:

- content_state: MISSING, PLACEHOLDER, SUBSTANTIVE, or NOT_APPLICABLE;
- evidence_state: CURRENT, STALE, PROVISIONAL, MISSING, or CONFLICTING;
- workflow_state: PENDING, DRAFTING, APPROVED_NOT_WRITTEN, WRITTEN, BLOCKED, or
  OUT_OF_SCOPE; and
- assertion_results: stable assertion ID, PASS/FAIL, evidence, owner.

Artifact status:

- DRAFT — skeleton/some approved sections exist but required content/decisions
  remain;
- PARTIAL — safe work is preserved but dependency, evidence, timeout, drift,
  authorization, migration, or blocking finding remains;
- READY_FOR_REVIEW — target content has all profile assertions passing, current
  evidence/critical dependencies, zero blocking findings, and stable read-back
  target bytes.

Authoring never emits COMPLETE, APPROVED, or IMPLEMENTATION READY.
Report Workflow Verdict separately. A review handoff is available only when a
READY_FOR_REVIEW artifact also has a verified external authoring receipt.

Critical gaps for screen/HUD include missing product requirement/owner,
platform/input profile, committed accessibility foundation/tier, navigation
contract, or owned cross-screen/global pattern. A user may accept risk but cannot
close or waive a blocking owner gap.

## Phase 0: Parse invocation and validate manifest identity

Parse flags first. Then read only the exact request manifest and validate its
contract, IDs, profile, mode, target/checkpoint roots, expected hashes, owners,
budgets, and non-writes. Do not read design context or ask design questions
before target/profile identity is known.

Invalid/unsupported input returns ERROR with no artifact status/verdict/write.
Missing mandatory identity/owner/hash evidence returns BLOCKED with no write.

## Phase 1: Inventory target and authorize one mutation boundary

Read applicable AGENTS.md root-to-target and the profile schema sources. For an
existing target, read raw bytes, compute target and section-body hashes, reject
duplicate IDs/headings, and inventory every required section against
cgs.ux-content-profile/v2.

- fill-gaps may select only MISSING/PLACEHOLDER content.
- revise-sections may select explicit SUBSTANTIVE sections whether evidence is
  CURRENT or STALE.
- migrate-schema maps legacy headings/content to stable IDs and preserves exact
  content hashes; ambiguous/unmappable fragments block until decided.
- create scopes all profile-required sections against ABSENT target.

Present one mutation manifest before broader context loading:

    Operation: <mode>
    Target: <exact path>
    Expected target: <hash | ABSENT>
    Checkpoint root: <exact path>
    Artifact/run/profile/schema IDs: <values>
    Authorized section IDs/body baselines: <ordered list>
    Writer/recorder task identities: <values>
    Limits: max bytes, revision rounds, consultation limits
    Non-writes: <complete list>

Obtain one explicit authorization from named mutation authority. It covers the
listed target regions and immutable checkpoint/receipt records for this task.
Per-section product approval is not filesystem authorization. New path/section,
operation, owner, writer, or larger limit requires a revised manifest and new
authorization.

## Phase 2: Load bounded hash-manifested context

After authorization, select candidates in stable order:

1. applicable AGENTS.md root-to-target;
2. exact target when existing;
3. exact platform/input profile;
4. exact accessibility foundation;
5. requirement-owner GDD sections in manifest requirement order;
6. direct navigation parent/entry/exit neighbors in manifest order;
7. declared pattern-library entries;
8. player journey; and
9. art-bible sections.

Never scan all GDDs/UX specs or follow second-hop navigation. Count every loaded
context file, including AGENTS and target, against hard maxima 16 files and
524288 exact bytes. Requested budgets may be smaller but never larger. Determine
size before load; never truncate or partially read.

The context manifest records ordered path, role, artifact/requirement IDs,
selected range, bytes, raw SHA-256, owner, dependency edge, loaded/omitted
state, and reason. Canonicalize UTF-8 LF, fixed field order, no trailing
whitespace, one final newline; record digest.

For an existing target, mark its manifest entry mutable-target-baseline. Its
baseline hash remains provenance but is not revalidated as external context
after authorized target writes. Target currentness is always checked separately
by target/section CAS. All other loaded entries are context evidence and must
continue to match their manifest hashes.

If any mandatory/selected candidate exceeds budget, is missing, or mismatches
declared hash, append at most an authorized PARTIAL checkpoint with reason
CONTEXT_BUDGET_EXCEEDED or CONTEXT_EVIDENCE_INVALID, leave target unchanged, and
stop. Required context is never silently omitted.

Only after bounded context succeeds, show sourced constraints, hard evidence,
derived constraints, provisional assumptions, and dependency findings; then ask
the first product question.

## Phase 3: Build create, fill, revision, or migration plan

For every authorized section, list baseline body hash/state, content assertion
results, source requirements/hashes, decision dependencies, exact byte
region/anchor, and planned operation.

For migration, produce deterministic old-heading to stable-ID mapping, proposed
moves, before hashes, and unresolved fragments. Never discard, duplicate, or
rewrite moved content silently.

Each selected content write uses compare-and-set:

1. re-read target and require current hash equals checkpoint current target hash;
2. require current section body equals stored baseline/current body hash;
3. re-hash context evidence used by the draft;
4. require authorization manifest hash and writer identity still match;
5. reject any out-of-scope byte change.

Target mismatch returns ERROR — CONCURRENT TARGET CHANGE. Evidence mismatch
returns ERROR — CONTEXT EVIDENCE CHANGED. No target/checkpoint write occurs for
that transaction.

## Phase 4: Create/migrate skeleton and initialize receipt chain

After context and plan succeed, the target writer performs only authorized
CAS writes. Create writes the exact profile skeleton with placeholders.
fill/revise preserves every unselected byte. Migration applies only approved
mappings.

The checkpoint recorder appends under:

    production/ux/ux-design/<artifact-id>/<run-id>/checkpoints/
      <sequence>-<phase>.yaml

Every record uses cgs.ux-design-checkpoint/v2 and includes previous checkpoint
path/hash, request/context/schema/authorization/target hashes, mode, full section
state/assertions, decision/revision IDs, writer identities, operation ledger,
consultation results, open findings, budgets, next legal step, UTC timestamp,
and canonical payload SHA-256. Sequence and previous hash use create-if-absent
compare-and-set; never rewrite a checkpoint.

After the final target content/header CAS and read-back hash, the final immutable
record additionally declares
cgs.ux-authoring-receipt/v1 and binds pre/post target hashes, context manifest,
content/profile/author schema, applied section/revision/decision IDs,
authorization hash, unresolved findings, author/recorder identities, and exact
target path. Its stable receipt ID may appear in the target header, but its path
or hash must not: the receipt binds the already-final target and therefore stays
external to avoid a target/receipt hash cycle. The receipt is authoring evidence,
not review approval.

Read back and hash every write. Drift, wrong writer, or path expansion halts
PARTIAL/BLOCKED without reverting user work. Receipt construction failure after
verified final target content leaves the content status unchanged but reports
Workflow Verdict PARTIAL, emits no review handoff, and names the exact
unreceipted target hash.

## Required continuation

Before section authoring, read references/continued-workflow.md in full. It
defines decision/revision provenance, deterministic content assertions,
cross-reference finding contract, acceptance references, bounded consultation,
recovery, final receipt, and independent-review handoff.

## Non-implementation and review boundary

After authoring, stop. A fresh independent reviewer reads the exact target,
content/profile/author schema, context digest, and authoring receipt path/hash.
Only a separate authorized recorder may persist review evidence after rechecking
all hashes.

READY_FOR_REVIEW is not approval or implementation readiness. A conversation
approval, author self-review, stale receipt, stale target, or advisory review
authorizes nothing.

## P1 audit traceability

Each authoritative P1 audit finding has one independent trace row. The row binds
the normative clause to a concrete dedicated-spec case/assertion; it does not
claim that the case was executed.

| Audit ID | Normative clause | Dedicated spec evidence |
|---|---|---|
| `UXD-005` | Phase 1 mode/content/evidence inventory and Phase 3 mutation planning | Case 4 — `UXD-C04-A`, `UXD-C04-B`, and `UXD-C04-C` |
| `UXD-006` | Phase 2 bounded hash-manifested context | Case 6 — `UXD-C06-A`, `UXD-C06-B`, and `UXD-C06-C` |
| `UXD-007` | Phase 0 request resolution before Phase 2 context/questions | Case 7 — `UXD-C07-A`, `UXD-C07-B`, and `UXD-C07-C` |
| `UXD-008` | `references/continued-workflow.md` Phase 5 decision and revision provenance | Case 8 — `UXD-C08-A`, `UXD-C08-B`, and `UXD-C08-C` |
| `UXD-009` | Required artifact header and independent state axes for platform/input evidence | Case 9 — `UXD-C09-A`, `UXD-C09-B`, and `UXD-C09-C` |
| `UXD-010` | `references/continued-workflow.md` Phase 8 dependency-finding gate | Case 10 — `UXD-C10-A`, `UXD-C10-B`, and `UXD-C10-C` |
| `UXD-011` | `references/continued-workflow.md` Phase 7 reference-first acceptance criteria | Case 11 — `UXD-C11-A`, `UXD-C11-B`, and `UXD-C11-C` |
| `UXD-012` | `references/continued-workflow.md` Phase 9 bounded consultation/failure results | Case 12 — `UXD-C12-A`, `UXD-C12-B`, and `UXD-C12-C` |
| `UXD-013` | Versioned profile/content contracts, required continuation, and this trace matrix | Case 18 — `UXD-C18-A`, `UXD-C18-B`, and `UXD-C18-C` |
