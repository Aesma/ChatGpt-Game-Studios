---
name: create-architecture
description: "Author one bounded DRAFT master architecture as an immutable derived view of current approved GDD requirements and current Accepted ADRs, with stable TR mapping, profile-safe CAS, and external review/READY ownership."
---

# Create Architecture

## Invocation

```text
$create-architecture <new | resume | focus | audit> [<focus-area>]
  [--cross-gdd-evidence <path> --cross-gdd <revision:...>]
  [--prior-review <path> --prior-review <revision:...>]
```

Focus areas are exactly:

```text
requirements | decision-ledger | layers | ownership | data-flow | api-boundaries | engine
```

`focus` requires exactly one focus area; other profiles reject one. Each evidence
path requires its matching expected raw revision and vice versa. Reject duplicate/
unknown flags, positional extras, directories, globs, traversal, outside-root or
root-escaping symlink paths, malformed revisions, and both path plus inline forms of
the same evidence.

The user may explicitly supply one complete inline cross-GDD evidence record or
one prior-review record instead of the corresponding path pair. Never search for
the newest, nearest, highest-numbered, or most convenient evidence.

Read
[references/architecture-evidence-contract.md](references/architecture-evidence-contract.md)
in full before processing. It is normative.

## Ownership and hard stop

This workflow is an author only. It may create or update exactly:

```text
docs/architecture/architecture.md
```

It never writes session state, skeleton checkpoints, GDDs, ADRs, lifecycle
records, registries, engine references, reviews, sign-off, READY state, gate
records, catalogs, tests, or latest pointers. It never delegates to or impersonates
an architecture reviewer, technical director, lead programmer, recorder, gate, or
other workflow.

Accepted ADRs are the sole source of binding technical decisions; approved GDDs
are the sole source of admitted product requirements. The architecture is
`cgs.master-architecture/v3`, a derived view. New/changed bytes are always `DRAFT`
or `PARTIAL`, never `READY`.

Use these result fields:

| Field | Values |
|---|---|
| `Workflow Status` | `COMPLETE`, `PARTIAL`, `BLOCKED`, `STOPPED`, `ERROR` |
| `Architecture Operation` | `CREATE`, `UPDATE`, `UNCHANGED`, `NOT_REQUESTED`, `DECLINED`, `CONFLICT`, `FAILED` |
| `Profile` | `new`, `resume`, `focus`, `audit` |
| `Context State` | `COMPLETE`, `PARTIAL`, `INVALID` |
| `Cross-GDD State` | `CURRENT_PASS`, `CURRENT_CONCERNS`, `CURRENT_FAIL`, `CURRENT_PARTIAL`, `MISSING`, `STALE`, `UNBOUND`, `CONFLICT`, `UNKNOWN` |
| `Independent Review` | `NOT_SUPPLIED`, `CURRENT_PASS`, `CURRENT_BLOCKED`, `CURRENT_PARTIAL`, `STALE`, `INVALID` |
| `Route State` | `READY`, `BLOCKED`, `UNKNOWN`, `NO_ROUTE` |

`COMPLETE` means only that this authoring/audit interaction completed honestly.
It never means Architecture Complete, independently approved, READY, gate-ready,
or safe to implement unresolved choices.

---

## Phase 0: Freeze root and bind the catalog

Resolve exactly one repository root and one UTC snapshot. Read exact raw bytes and
read and validate explicit version/revision metadata.

Read `.codex/docs/workflow-catalog.yaml` first. Require unique phase/workflow IDs
and exactly one `create-architecture` entry with:

- exact command identity;
- one containing phase and required/optional semantics; and
- one non-wildcard artifact path equal to
  `docs/architecture/architecture.md`.

An unversioned catalog is `LEGACY_UNVERSIONED`; use only fields it declares and
never infer a transition, receipt, READY recorder, evidence producer, prerequisite,
or completion state from comments or artifact presence.

Catalog-only routing resolves:

- missing/current cross-GDD evidence through the unique declared cross-GDD review
  producer when available;
- a `DECISION-*`/non-Accepted ADR gap through the unique declared ADR authoring or
  lifecycle owner;
- independent review through the unique declared architecture-review entry;
- any READY recording, gate, or next-phase action only through an exact declared
  owner, command, transition, evidence, and receipt contract.

Do not copy or hardcode downstream commands, phase shorthand, UX prerequisites,
gate profiles, transition IDs, minimum ADR counts, or file-presence completion
rules. Missing, duplicated, incompatible, or underspecified route policy produces
`UNKNOWN`/`BLOCKED` and `Stop`.

A catalog conflict affecting target identity/path blocks all processing. A
route-only gap does not invalidate an otherwise safe DRAFT/audit result but stays
visible.

---

## Phase 1: Enforce the selected profile

Read target source state and exact base revision before other authoring sources.

| Profile | Required target state | Mutation |
|---|---|---|
| `new` | exact target ABSENT | one complete v3 DRAFT/PARTIAL CREATE |
| `resume` | valid v3 DRAFT/PARTIAL target | selected incomplete/stale sections plus mechanically affected derived ledgers/status/history |
| `focus` | valid v3 target and one focus area | only the reference contract's exact focus mutation closure |
| `audit` | valid existing target | none |

Reject profile precondition mismatch. Do not silently switch profiles, overwrite an
existing target in `new`, treat a legacy/malformed file as absent, or retrofit an
unsupported schema. `BLOCKED_UNSUPPORTED_BASE` requires a separately authorized
migration owner not defined here.

For `resume`, show incomplete/stale sections and ask the user to select one bounded
batch of at most three sections. Dependencies mechanically required to keep the TR
map/decision ledger/provenance internally consistent are disclosed before selection.
Do not silently expand the batch.

For `focus`, freeze the exact target section and allowable collateral fields before
source loading. If a necessary change would affect another technical section, stop
and offer `resume` or a new focus run; never expand mutation scope implicitly.

For `audit`, declare `Architecture Operation: NOT_REQUESTED`, skip candidate,
approval, temporary-file and write phases, and return inline findings only.

---

## Phase 2: Build the bounded source manifest

Apply the reference contract's exact classes, count/per-file/class/48-MiB limits,
layered loading, direct-child boundaries, source states, ordering, and canonical
`source_manifest_id`.

Start from catalog, technical preferences, target/base, systems index, supplied
cross-GDD envelope, ADR registry/catalog artifact declarations, and supplied prior
review. Construct the complete intended manifest before reading full bodies.

Only read GDDs and per-GDD approval records named by the current cross-GDD manifest.
When cross-GDD evidence is absent, use only bounded systems-index exact GDD paths
and require the user to explicitly opt each exact path/revision into
`PROVISIONAL_EXPLICIT` Draft input. Never read every GDD merely because it exists.

Only read ADRs from an exact registry/architecture link or the catalog's bounded
direct-child ADR artifact declaration. Only read engine references pinned by
technical preferences/version and linked by an admitted ADR claim. Never scan an
engine library or browse for missing knowledge.

Any unreadable/ambiguous/oversize/changed/limit-exceeded required source is
`Context State: PARTIAL|INVALID`. Stop before writing, name exact unchecked scope,
and never sample it as complete.

For audit/resume/focus, validate the base document's prior manifest and immutable
provenance chain. A broken, reordered, removed, or rewritten event is
`BLOCKED_INVALID_PROVENANCE`.

---

## Phase 3: Admit current GDD evidence

Validate supplied cross-GDD evidence exactly as the reference contract requires:
`cgs.review-evidence/v1` produced by `review-all-gdds`, extension
`cgs.cross-gdd-review/v2`, complete manifest/coverage, internally valid record ID,
and current source revisions.

Recompute each GDD and per-GDD `design-review` approval record. Preserve exact
source and Cross-GDD states; do not upgrade them from filenames, status text,
systems-index rows, prose, or prior architecture claims.

Only `APPROVED_CURRENT` GDD requirements can enter the approved derived TR map.
`PROVISIONAL_EXPLICIT` input is isolated in the non-binding provisional section,
excluded from approved coverage and READY eligibility, and disclosed in every
result.

Cross-GDD current PASS is a readiness precondition, not a source of product truth.
CONCERNS keeps findings visible and blocks READY; FAIL blocks affected projection;
PARTIAL/missing/stale/unbound/conflict/unknown cannot be described as current
complete evidence.

If the user declines provisional use when current approval evidence is unavailable,
return `STOPPED`/`BLOCKED` with the unique catalog-derived evidence action or Stop.

---

## Phase 4: Build the stable derived TR map

Extract exact normative requirements only from admitted source sections. Maintain
three separate collections:

1. `EXPLICIT_REQUIREMENT` — stable normative source requirement;
2. `CONFIRMED_REQUIREMENT` — a separately evidenced confirmation satisfying the
   reference contract; and
3. `INFERRED_CANDIDATE` — non-binding possibility that does not enter the TR map.

Apply the reference contract's deterministic TR ID construction, persisted-ID
preservation, source change state, and explicit `TR-MIGRATION-*` rules. Never use
sequential numbering, reorder-driven IDs, display order, filenames, or fuzzy text
matching.

Every approved TR row preserves exact source text/locator/revision, approval record
ID/revision, currentness, and ADR mapping. Duplicate source identities, revision collisions,
ambiguous locators, missing exact text, or conflicting persisted mappings block
publication.

An inferred candidate requiring confirmation is shown separately with provenance,
rationale, and consequences. Confirmation must be explicit and evidence-bound; it
does not approve the GDD/ADR and cannot promote a provisional source. Unconfirmed
candidates create neither TR coverage nor ADR obligations.

---

## Phase 5: Build the ADR-derived decision ledger

Validate every in-scope ADR and exact lifecycle/review/registry evidence. Classify
it as `ACCEPTED_CURRENT`, `PROPOSED`, `SUPERSEDED`, `REJECTED`, `STALE`, `UNBOUND`,
`CONFLICT`, or `UNKNOWN` using the reference contract.

Only `ACCEPTED_CURRENT` ADRs populate binding-looking derived text. Every derived
statement includes exact ADR ID/revision, lifecycle record ID/revision, and source TR IDs.
The architecture never settles disagreement between ADRs or lifecycle records.

For missing or non-current ownership, preserve one stable `DECISION-*` gap. Do not
select or ask the user to select APIs, modules, interfaces, data-flow mechanisms,
threading, persistence, networking, or other technical outcomes here. State the
decision scope and affected TR IDs, then resolve the next action from the catalog's
ADR owner.

Required Proposed/stale/unbound/conflicting/unknown ADRs and missing Accepted
coverage block READY eligibility. They may remain visibly non-binding in DRAFT.

---

## Phase 6: Validate engine knowledge without inventing capability

For every admitted ADR engine claim, bind pinned engine/version and only the exact
needed reference domain. Record provenance/date/revision/path/revision/coverage and
classify `CURRENT_COMPLETE`, `CURRENT_PARTIAL`, `STALE`, `MISSING`, `UNSUPPORTED`,
`UNREADABLE`, or `CONFLICT`.

Only CURRENT_COMPLETE supports a verified engine fact. Otherwise keep the ADR
decision citation but label the implementation/API assertion `UNVERIFIED`, name
the unsupported claim, and add a READY blocker when implementation depends on it.

Missing knowledge is not permission to rely on model memory. Return PARTIAL if the
selected profile cannot safely render its requested section.

---

## Phase 7: Render one canonical derived candidate

For `new`, render the full v3 skeleton in memory before inserting content. Do not
write an early skeleton or session checkpoint.

For `resume`/`focus`, construct:

```text
BASE + authorized profile INTENT -> CANDIDATE
```

Preserve every out-of-scope technical section and prior immutable provenance event.
Show a structured three-way diff separating unchanged, mechanically affected,
explicitly changed, blocked, and provenance-appended fields.

Populate the reference contract's fifteen sections. Every changed candidate uses:

```text
Schema: cgs.master-architecture/v3
Status: DRAFT | PARTIAL
External Review: NOT_CURRENT
Source Manifest ID: <stable manifest business ID plus UTC run ID>
Prior Artifact revision: <base-revision-or-ABSENT>
```

Do not embed the candidate's own revision in its bytes. Append exactly one immutable
author-side provenance event with profile/focus/base/manifest/decision/change/time/
task identity. Never edit prior events.

Assign candidate_revision from the explicit base revision plus one, then render exact UTF-8/LF bytes. Show and validate:

- approved/provisional/blocked GDD source counts;
- Cross-GDD record/state/findings;
- stable TR current/changed/gap/migration counts;
- Accepted/current and non-binding ADR states;
- verified/unverified engine claims;
- open DECISION IDs and READY blockers; and
- exact profile mutation boundary.

If candidate bytes equal valid base bytes, use `UNCHANGED`; do not rewrite or append
a no-op provenance event.

The user reviews only source mapping fidelity and derived projection accuracy here.
Any new low-level choice is sent to ADR authoring instead of being decided inside
this workflow.

---

## Phase 8: Approve one changeset and execute CAS

Preview exactly:

```text
docs/architecture/architecture.md: CREATE | REPLACE with candidate_revision
all other persistent writes: NONE
```

Show complete candidate/lossless representation, profile diff, manifest entries/
limits/revision, stable TR migrations, ADR/lifecycle/engine states, provenance append,
blockers, base/absence, destination parent, and exact candidate bytes/revision.

Obtain one approval bound to those exact values. Product/mapping approval and file
authorization are not ADR acceptance, independent review, READY recording, gate
approval, or permission to mutate another path. If declined, return STOPPED/
DECLINED with zero writes. Do not ask again per section or source.

Immediately before mutation, apply the complete reference-contract CAS: re-read every bound input/source state/directory membership, rebuild the manifest,
reapply BASE+INTENT, and require the same candidate revision/provenance chain.

Any mismatch returns BLOCKED/CONFLICT with exact old/new states and zero writes.
Do not merge, refresh, retry, overwrite, update session state, or implicitly accept
changed bytes.

After CAS, atomically publish only the exact architecture candidate, re-read it,
verify revision/v3 schema/profile boundary/manifest/TR/ADR/provenance/status/review
invariants, and confirm no other persistent path changed.

- exact verified publication -> CREATE/UPDATE and this authoring may be COMPLETE;
- pre-publication failure -> FAILED/BLOCKED;
- publication/read-back/result uncertainty -> PARTIAL, exact observed state, never
  COMPLETE or READY.

Never repair or revert external concurrent changes.

---

## Phase 9: Report external review currentness and route one action

When a prior independent review was explicitly supplied, validate it as
`cgs.review-evidence/v1` produced by `architecture-review`, extension
`cgs.architecture-review/v2`, exact architecture-derived path/revision, source-manifest
binding, target manifest/ruleset revisions, complete coverage, internal record
identity, and preserved PASS/BLOCKED/PARTIAL verdict. Only current full-mode PASS
is READY-eligible; narrower modes remain scoped evidence only.

It is current only for unchanged exact artifact and manifest bytes. Any authoring
change makes it STALE/NOT_CURRENT. Never retarget, copy, edit, save, or use it to
write READY.

Choose exactly one highest-priority next action from catalog-declared evidence:

1. obtain/refresh cross-GDD evidence when source admission is unsafe;
2. resolve the first stable DECISION/TR/ADR lifecycle blocker;
3. verify one blocking engine-reference gap;
4. run independent architecture review for the exact current artifact/manifest;
5. invoke a separate READY recorder/gate only when the catalog declares exact
   current evidence and ownership; or
6. `Stop` when no safe unique route exists.

Never claim an undeclared UX/accessibility artifact exists, skip a catalog-required
step because a file is present, infer gate readiness, print a copied roadmap, or
invoke the action.

Return:

- workflow/profile/operation/context states;
- catalog path/contract/revision and route ID/command or gap;
- architecture path/base/candidate/on-disk revisions;
- source manifest ID, limits/use, every source-class state;
- Cross-GDD and per-GDD evidence IDs/revisions/states;
- TR and migration IDs/states;
- ADR/lifecycle and engine-reference states;
- immutable provenance event ID and chain validation;
- external review state/record ID/revision;
- READY blockers and exact one next action;
- `Architecture READY Mutation: NONE`, `Review Record Mutation: NONE`,
  `Session-State Mutation: NONE`, `Auto Executed: false`.

Then stop.

## Status mapping

- invalid invocation/root/catalog target identity -> `ERROR`;
- profile/base/provenance/source-identity/TR/ADR conflict -> `BLOCKED`;
- context/source/evidence/engine coverage incomplete or resulting-state uncertainty
  -> `PARTIAL`;
- declined choice/changeset -> `STOPPED`;
- verified author Draft transaction, honest UNCHANGED, or complete read-only audit
  -> `COMPLETE` for this workflow only.
