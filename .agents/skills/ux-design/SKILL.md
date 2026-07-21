---
name: ux-design
description: "Author versioned screen, HUD, and interaction-pattern UX artifacts through bounded context, one mutation authorization, stable decisions, and hash-safe checkpoints."
---

# UX Design

Author one UX artifact without pretending that author approval is independent
review, that missing foundations are harmless, or that this workflow owns unrelated
accessibility and global-pattern prerequisites.

## Invocation contract

Invoke only as:

`$ux-design --manifest {ux-design-request-path} [--resume {checkpoint-path}]`

Validate arguments before reading the repository, delegating, requesting a decision,
or writing. With no manifest, print the usage line and stop with no side effects and
no verdict. Reject unknown/duplicate flags, missing values, directories, unsafe IDs,
path traversal, and unsupported schema versions.

The request manifest must declare:

- `Artifact Type: ux-design-request` and `Schema Version: 1`;
- stable artifact ID and run ID; screen/HUD work also requires a stable screen ID;
- profile: `ux-spec`, `hud-design`, or `interaction-pattern-library`;
- mode: `create`, `fill-gaps`, `revise-sections`, or `migrate-schema`;
- exact target path and expected SHA-256, or `ABSENT` for create;
- selected stable section IDs for revise mode and expected hashes for every other
  authorized artifact;
- exact context paths/hashes, GDD requirement IDs and owners, one-hop navigation
  neighbors, and file/byte/token budgets;
- exact platform/input profile path/hash or `MISSING`, including supported devices,
  resolutions/aspects, safe zones, and primary input;
- exact accessibility-foundation path/hash, committed tier, and external owner, or
  `MISSING`;
- global pattern-library path/hash and external UX-library owner, or `ABSENT`;
- player-journey and art-bible paths/hashes when applicable;
- product decision-maker, mutation authorizer, target writer task ID, checkpoint
  recorder task ID, maximum revision rounds, consultation timeout, and checkpoint
  root;
- explicit non-writes.

IDs are stable slugs or UUIDs, never dates alone. Resolve real paths and reject a
symlink or junction escaping the repository. `create` requires an absent target;
every other mode requires an existing target whose bytes match the expected hash.
The default target is profile-specific, but it must still be stated explicitly:

- `ux-spec`: `design/ux/{screen-id}.md`;
- `hud-design`: `design/ux/hud.md` with stable screen ID `hud`;
- `interaction-pattern-library`: `design/ux/interaction-patterns.md`.

One run authors exactly one target UX artifact plus its declared checkpoint records.
It does not create `design/accessibility-requirements.md` as a side effect and does
not create both a screen spec and the global pattern library.

## Author schema source of truth

The versioned profiles in this file and `references/continued-workflow.md` are the
single author/retrofit/review contract. Compute `author_schema_hash` as SHA-256 over
the exact bytes of this `SKILL.md`, one NUL byte, and the exact bytes of the required
continuation. Record:

- `Profile Version: ux-profile-schema-v1`;
- `Schema Version: ux-design-author-sha256:{author_schema_hash}`.

Every section has one stable ID and one exact H2 heading. Emit the stable ID as an
HTML comment immediately before the heading, for example
`<!-- ux-section: UXS-01 -->`. Headings are display labels; IDs govern migration,
selection, findings, decisions, and checkpoints.

### Profile: ux-spec

| Stable ID | Exact required H2 heading | Minimum contract |
|---|---|---|
| UXS-01 | Purpose & Player Need | Player-perspective goal, outcome, and linked requirement IDs |
| UXS-02 | Player Context on Arrival | Prior activity, state, pressure, and journey source |
| UXS-03 | Navigation Position | Root/parent/screen hierarchy and alternate access |
| UXS-04 | Entry & Exit Points | Entry/exit triggers, carried state, and irreversible effects |
| UXS-05 | Layout Specification | Information hierarchy, zones, component inventory, viewport assumptions, optional schematic evidence |
| UXS-06 | States & Variants | Default plus applicable loading, empty, populated, error, locked, and platform states |
| UXS-07 | Interaction Map | Every interactive component, supported input, focus order, feedback, and outcome |
| UXS-08 | Events Fired | Each action mapped to a stable event/payload or source-backed `none` |
| UXS-09 | Transitions & Animations | Enter/exit/state transitions and reduced-motion behavior |
| UXS-10 | Data Requirements | Data source/owner, read/write intent, update trigger, and null handling |
| UXS-11 | Accessibility | Conformance to the external committed tier; this section never chooses that tier |
| UXS-12 | Localization Considerations | Locale formatting, expansion/reflow, string ownership, and real layout constraints |
| UXS-13 | Acceptance Criteria | Requirement-linked, locally executable conditions without copied product rules |
| UXS-14 | Open Questions | Stable dependency/finding IDs, owners, state, and next resolution action |

`UXS-05` uses exact H3 headings `Information Hierarchy`, `Layout Zones`, and
`Component Inventory`. A wireframe is optional schematic evidence, not a pixel or
responsive-layout authority; when present it declares viewport and scale assumptions.

### Profile: hud-design

| Stable ID | Exact required H2 heading | Minimum contract |
|---|---|---|
| HUD-01 | HUD Philosophy | Approved information-density principle and conflicts |
| HUD-02 | Information Architecture | Requirement-linked inventory and Must Show/Contextual/On Demand/Hidden rationale |
| HUD-03 | Layout Zones | Platform, safe-zone, aspect, viewport, and attention assumptions |
| HUD-04 | HUD Elements | Stable element IDs, data owner, visibility/update rules, pattern refs, and states |
| HUD-05 | Dynamic Behaviors | Gameplay-context transitions, priority, contention, and reduced motion |
| HUD-06 | Platform & Input Variants | Every declared platform/input/resolution/text-scale variant |
| HUD-07 | Accessibility | External-tier conformance, non-color cues, focus/assistive behavior |
| HUD-08 | Open Questions | Stable dependency/finding IDs, owners, state, and next action |

### Profile: interaction-pattern-library

| Stable ID | Exact required H2 heading | Minimum contract |
|---|---|---|
| PAT-01 | Overview | Scope, library owner, consumers, profile/hash provenance |
| PAT-02 | Pattern Catalog | Canonical pattern ID, name, category, version, status, and entry anchor |
| PAT-03 | Patterns | One owner-approved definition per catalog entry, states, inputs, feedback, accessibility, use/non-use rules |
| PAT-04 | Gaps & Patterns Needed | Feature-local proposal IDs, source screen IDs, owner, and disposition |
| PAT-05 | Open Questions | Stable dependency/finding IDs, owners, state, and next action |

Global canonical pattern IDs use `UXP-GLOBAL-{slug}`. A screen/HUD run may only
record feature-local proposals `UXP-{screen-id}-{slug}` inside its own spec. Only the
external UX-library owner may approve the mapping and merge it into the global
library in an independently authorized `interaction-pattern-library` run.

## Required artifact header

Every authored target begins with exact machine-readable blockquote fields:

```markdown
> **Artifact Type**: ux-spec | hud-design | interaction-pattern-library
> **Schema Version**: ux-design-author-sha256:{author_schema_hash}
> **Profile Version**: ux-profile-schema-v1
> **Artifact ID**: {stable-artifact-id}
> **Screen ID**: {stable-screen-id | N/A-library}
> **Status**: DRAFT | PARTIAL | READY_FOR_REVIEW
> **Author Task ID**: {actual-writer-task-id}
> **Last Updated UTC**: {ISO-8601}
> **Platform Target**: {declared targets | DEPENDENCY-GAP}
> **Platform Profile**: {path}@{sha256 | MISSING}
> **Accessibility Foundation**: {path}@{sha256}/tier:{tier | MISSING}
> **Requirement IDs**: {stable IDs with owner}
> **Context Manifest SHA-256**: {hash}
```

Do not claim the user, a consultant, or a tool is an author unless that identity
actually wrote target bytes. Record product choices separately as decision IDs,
decision-maker identity, source options, chosen option, rationale, and timestamp.

## Status and dependency rules

Use artifact statuses, not an unconditional completion claim:

- `DRAFT`: a valid skeleton or some approved sections exist, but required sections
  or decisions remain;
- `PARTIAL`: all possible bounded work is preserved but a critical dependency,
  timeout, drift, authorization, migration, or cross-reference blocker remains;
- `READY_FOR_REVIEW`: every profile requirement and cross-reference check passes,
  the target was read back and hashed, and no critical dependency is missing.

The following are critical dependency gaps for screen/HUD work: missing concept
foundation where the player goal cannot be sourced, missing applicable GDD
requirement or requirement owner, missing committed accessibility tier/foundation,
missing platform/input profile, unresolved navigation contract, or an unowned
cross-screen/global pattern. A gap receives a stable `UXD-{artifact-id}-{check-id}`,
source evidence, owner, status `OPEN`, and resolution action. It prevents
`READY_FOR_REVIEW`; user acceptance may be recorded but cannot close the gap.

An accessibility specialist may assess conformance, but this workflow consumes the
external accessibility foundation and never defines or writes its tier. A missing
foundation requires its dedicated owner/workflow outside this run. Likewise, a
screen/HUD author cannot update the global pattern library.

## Phase 1: Resolve target and load bounded context

Validate the manifest, target identity, mode, expected hash, author schema hash, and
applicable instruction chain. Load only declared paths and exact requirement IDs.
For navigation, load only declared direct parents, entries, and exits. For HUD, load
only declared UI requirement sections, not every GDD. For pattern work, load only
declared consumer specs and component/interaction sections, not all UX files.

Create an in-memory context manifest containing normalized path/hash, selected
section/range, requirement ID/owner, dependency edge, bytes/tokens consumed,
omissions, and author schema hash. Stop at the declared budget. Budget overflow or
hash drift produces `PARTIAL` with no target write.

Do not ask the user any design question until target/profile validation and bounded
context loading finish. Present the sourced constraints, explicit gaps, assumptions,
and the one next decision.

## Phase 2: Plan create, retrofit, revision, or migration

For `create`, produce candidate header and all required stable-ID section headings in
scratch. For an existing target, read exact bytes and classify every schema section:

- `VALID`: recognized ID/heading, substantive current content, sources current;
- `STALE`: substantive content whose source/profile hash changed;
- `PLACEHOLDER`: recognized but no substantive content;
- `MISSING`: required ID/heading absent;
- `UNMAPPABLE`: ambiguous duplicate or legacy content without a safe mapping.

`fill-gaps` selects only PLACEHOLDER/MISSING sections. `revise-sections` may select
VALID or STALE sections explicitly and must preserve all unselected bytes.
`migrate-schema` builds a deterministic old-heading-to-stable-ID mapping, proposed
moves, preserved content hashes, and unresolved fragments. Never silently discard,
rewrite, or duplicate legacy content. An UNMAPPABLE section requires a product
decision before mutation and remains `PARTIAL` if unresolved.

For every selected section, state source requirements, constraints, current hash,
decision dependencies, and the exact byte region/anchor to be replaced. Present the
plan before mutation authorization.

## Phase 3: One bounded mutation authorization

Read-only analysis, questions, options, decisions, and scratch drafts do not require
file authorization. Before the first write, present one task mutation manifest:

- operation, exact target and checkpoint paths;
- expected target base hash or `ABSENT`;
- stable artifact/screen/run/profile/schema IDs;
- authorized section IDs, anchors, writer and checkpoint recorder task IDs;
- maximum bytes and maximum revision rounds;
- explicit non-writes, including accessibility foundation, unrelated UX specs,
  implementation paths, and the global pattern library unless it is this run's
  sole authorized target owned by the external UX-library owner.

Obtain one explicit authorization from the named mutation authority. It authorizes
the listed path/section boundary for this task, including later user-approved section
writes and checkpoint updates. Do not ask again per section or per file. A new path,
new section ID, operation change, ownership change, or larger limit is scope expansion
and requires a revised manifest and new authorization.

Product decisions and section approvals are content choices, not filesystem
authorization. Never label a product approval as permission to mutate an unlisted
path.

## Phase 4: Create or migrate the skeleton

After authorization, the unique UX-author task verifies the current base hash and
writes the exact profile header/section structure. Create mode writes a complete
placeholder skeleton. Retrofit/revision preserves every unselected byte. Migration
applies only approved mappings and preserves hashes of content moved without edits.

The checkpoint recorder is the only writer of immutable records under:

`production/ux/ux-design/{artifact-id}/{run-id}/checkpoints/{sequence}-{phase}.yaml`

Each checkpoint records request/context/schema/target hashes, mode, section-state
matrix, decision IDs, authorization manifest/hash, writer identities, operation
ledger, open dependencies/findings, completed/pending sections, and next legal step.
Read back and hash every write. Drift, an outside-path mutation, or a writer mismatch
halts with `PARTIAL` or `BLOCKED`; do not revert user work silently.

## Required continuation

Before section authoring, read `references/continued-workflow.md` in full. It defines
the mandatory per-section cycle, profile evidence, cross-reference gate, recovery,
bounded consultation, and independent-review handoff. Its rules are part of the
versioned author schema and cannot be skipped.

## Non-implementation boundary

This workflow never writes implementation code, visual assets, production UI,
translations, ADRs, an accessibility foundation, or another artifact's global
patterns. `READY_FOR_REVIEW` means authoring is ready for an independent review; it
does not mean approved or implementation-ready.

After authoring, stop. A fresh reviewer task that is not the author must review the
exact target SHA-256 under the current `author_schema_hash`. Only a separately
authorized recorder may persist the returned review envelope after rechecking the
target hash. Even a conversation `APPROVED` result does not authorize implementation.
Production work must remain blocked until a consumer verifies current-hash persisted
approval and obtains its own precise implementation authorization.
