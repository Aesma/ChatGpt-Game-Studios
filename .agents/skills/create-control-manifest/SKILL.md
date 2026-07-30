---
name: create-control-manifest
description: "Author or update one bounded DRAFT control manifest as a source-faithful derived view of current Accepted ADR rules and stable TR scope, with deterministic conflicts, monotonic versions, immutable provenance, and atomic conflict check publication."
---

## Path-first integrity

Accept canonical project-relative paths directly; do not require a caller-supplied
content-derived token. Validate project-root containment, regular-file type, declared
schema/version, stable IDs, permissions, lifecycle state, and path or ID collisions.
Allocate collision-safe IDs independently of file bytes. Before any permitted write,
re-read referenced records and target state, preview the exact authorized changes,
then use same-directory staging plus atomic replacement and rollback on failure.


# Create Control Manifest

## Invocation

```text
$create-control-manifest <new | update | audit>
  [--architecture-review <path>]
  [--prior-manifest-review <path>]
```

Each evidence flag names one canonical path. The user may explicitly supply exactly one
complete inline record instead of the corresponding path form. Reject missing/duplicate/
unknown flags, positional extras, directories, globs, traversal, outside-root or
root-escaping symlink paths, malformed records, and both path/inline forms for the same record.

Never search for newest/nearest/highest-numbered evidence.

Read
[references/control-manifest-contract.md](references/control-manifest-contract.md)
in full before processing. It is normative.

## Author-only boundary and result vocabulary

This workflow deterministically extracts and renders one derived artifact:

```text
docs/architecture/control-manifest.md
```

It never delegates source parsing, rule normalization, conflict resolution,
drafting, review, or recording. It never spawns or impersonates a technical
director/reviewer/recorder, writes review evidence, or sets `ACTIVE`.

Accepted ADRs own binding technical rules. Current approved GDD requirements own
product scope; the architecture's current stable TR map links that scope. The
architecture and control manifest are derived views and cannot create or override
policy.

Use these fields:

| Field | Values |
|---|---|
| `Workflow Status` | `COMPLETE`, `PARTIAL`, `BLOCKED`, `STOPPED`, `ERROR` |
| `Manifest Operation` | `CREATE`, `UPDATE`, `UNCHANGED`, `NOT_REQUESTED`, `DECLINED`, `CONFLICT`, `FAILED` |
| `Profile` | `new`, `update`, `audit` |
| `Context State` | `COMPLETE`, `PARTIAL`, `INVALID` |
| `Architecture State` | `CURRENT_REVIEWED`, `CURRENT_UNREVIEWED`, `DRAFT`, `PARTIAL`, `STALE`, `INVALID` |
| `Rule State` | `DERIVED_CURRENT`, `RETIRED`, `BLOCKED`, `UNKNOWN` |
| `External Manifest Review` | `NOT_SUPPLIED`, `CURRENT_PASS`, `CURRENT_NONPASS`, `STALE`, `INVALID` |
| `Route State` | `READY`, `BLOCKED`, `UNKNOWN`, `NO_ROUTE` |

`COMPLETE` means only that this Draft extraction/update/audit interaction completed
honestly. It never means source truth changed, independent review passed, manifest
is Active, a story is current, or a gate is ready.

---

## Phase 0: Freeze root and bind catalog identity

Resolve exactly one repository root and UTC snapshot. Read exact raw bytes and
positive integer revision.

Read `.codex/docs/workflow-catalog.yaml` first. Require unique phase/workflow IDs
and exactly one `control-manifest` entry whose command identifies this workflow and
whose single non-wildcard artifact path equals:

```text
docs/architecture/control-manifest.md
```

Also bind the catalog's unique architecture artifact, ADR artifact declaration,
and any declared architecture-review/control-manifest-review/Active-recorder/
downstream consumer contracts.

An unversioned catalog is `LEGACY_UNVERSIONED`; use only declared fields. Never
infer reviewer/recorder identity, receipt schema, Active eligibility, minimum ADR
count, completion, or next action from comments, step order, filenames, dates, or
artifact presence.

Catalog-only routing resolves the first source/architecture/ADR evidence gap, an
independent control-manifest review, Active recording, or a downstream consumer
only from exact compatible entries. Missing, duplicated, ambiguous, or
underspecified policy yields UNKNOWN/BLOCKED and `Stop`. Do not hardcode reviewer,
recorder, story/epic, gate, command, profile, transition, or receipt policy.

Target-path/catalog identity conflict is ERROR before other reads. Route-only gaps
do not invalidate an otherwise safe Draft/audit but remain visible.

---

## Phase 1: Enforce profile and base state

Read exact target state before source extraction:

| Profile | Target precondition | Mutation |
|---|---|---|
| `new` | ABSENT | one v2 DRAFT/PARTIAL CREATE |
| `update` | valid `cgs.control-manifest/v2` base | one rule-level DRAFT/PARTIAL UPDATE or UNCHANGED |
| `audit` | valid existing v2 base | none |

Reject mismatches. Never overwrite in `new`, silently convert profiles, treat an
invalid/legacy file as absent, or retrofit unsupported schema. Return
`BLOCKED_INVALID_BASE` and require a separately authorized migration owner.

For update/audit, validate base version/payload/source identity, stable rule/
finding IDs, Local Extensions namespace, and immutable provenance chain. Any
removed/reordered/edited history, non-monotonic version, payload mismatch,
unsupported content outside `x-local-*`, or duplicate identity is blocking.

`audit` is strictly read-only: operation NOT_REQUESTED; no candidate, approval,
temporary file, review request, status change, or source mutation.

---

## Phase 2: Build one bounded input manifest

Apply the reference contract's exact classes, count/per-file/class/40-MiB limits,
layered loading, direct-child boundaries, deterministic order, and canonical
`source_manifest_id`.

Start by indexing catalog, target/base, current master architecture v3 header/
source manifest/TR map/ADR ledger/provenance, registry, and supplied review
envelopes. Construct the complete intended source set before loading ADR bodies.

Use architecture/registry exact paths and the catalog-bounded ADR declaration;
never read every ADR merely because it matches a broad convention. Validate exact
lifecycle/review evidence first and parse rule-bearing sections only for
ACCEPTED_CURRENT ADRs. Excluded ADR paths/statuses/revisions remain visible.

Read technical preferences and pinned engine references only for exact normative/
constraint sections. Never scan engine source or promote descriptive guidance.

Any unreadable/ambiguous/oversize/changed/limit-exceeded required source yields
PARTIAL/INVALID, exact unchecked scope, and zero writes. Do not sample and publish
apparently complete rules.

---

## Phase 3: Validate current architecture, review, TR, and ADR evidence

Require `docs/architecture/architecture.md` to parse as
`cgs.master-architecture/v3`. Validate its exact revision, source manifest,
append-only provenance, stable derived TR map, and ADR decision ledger. Text found
only in architecture never becomes a rule.

When architecture-review evidence is supplied, require generic
`cgs.review-evidence/v1`, producer `architecture-review`, extension
`cgs.architecture-review/v2`, full-mode PASS, COMPLETE coverage, internally valid
record identity, exact architecture-derived path/revision, and reproducible source
manifest/ADR/TR inputs.

Missing/stale/nonpass review keeps Architecture State DRAFT/PARTIAL/
CURRENT_UNREVIEWED as applicable and blocks Active eligibility. It may allow a
clearly PARTIAL diagnostic Draft only when all parsed source rules remain safe.

Admit scope from a TR only when `CURRENT` + `DERIVED_COVERED`, exact source
requirement/approval evidence and current ADR links reproduce. Changed/stale/
unbound/gap/source-blocked/provisional/ambiguous TRs are blocking/unknown, never
scope authority.

Classify each ADR exactly as ACCEPTED_CURRENT, PROPOSED, SUPERSEDED, REJECTED,
STALE, UNBOUND, CONFLICT, or UNKNOWN under lifecycle/review/registry evidence.
Only ACCEPTED_CURRENT ADRs contribute rules. A status line or architecture summary
cannot upgrade one.

Every ADR rule's TR IDs must be explicitly addressed by that ADR and current in the
architecture ledger. Missing/fuzzy scope linkage is UNKNOWN.

---

## Phase 4: Extract source-faithful stable rules

Apply `cgs.control-rule/v2` exactly. For every item preserve stable rule ID, kind,
RFC level, complete scope/conditions, exact meaning, source ID/path/section/
locator/excerpt plus excerpt/source/lifecycle revisions, sorted current TR IDs,
derivation state, and supersedes IDs.

Preserve normative strength:

- mandatory positive -> MUST;
- mandatory negative -> MUST_NOT;
- recommendation -> SHOULD;
- negative recommendation -> SHOULD_NOT;
- permission/option -> MAY;
- no clear normative meaning -> no rule; stable UNKNOWN finding.

Never promote SHOULD/MAY, weaken MUST, convert SHOULD_NOT to prohibition, drop a
condition, or broaden scope. Split multi-level clauses without losing shared
conditions.

An alternative is PROHIBITION only when its authoritative source explicitly says
forbidden/prohibited for that scope. Rejected, deferred, not-selected, or lower-
ranked alternatives are CONTEXTUAL_REJECTION at level NONE with exact reason,
scope, and reconsideration condition. Never manufacture global `never`.

Use deterministic stable Rule IDs from source-owned IDs or the reference contract's
source/locator/clause/scope/level tuple. Preserve persisted IDs while identity and
meaning remain. Changed meaning/level/scope creates a new rule plus supersedes;
never number by extraction order/date/layer.

Technical preferences and engine references follow the same strength/provenance
rules. An engine constraint is emitted only for pinned current explicit coverage;
unsupported/ambiguous claims are UNKNOWN.

---

## Phase 5: Deduplicate and detect conflicts/unknown deterministically

Sort candidates deterministically. Deduplicate only exact same level/kind/meaning/
scope/conditions/TR/applicability; retain all equivalent sources and choose the
lexicographically smallest stable ID.

Only a current explicit lifecycle supersession/exception relation supplies
precedence. Newer date, higher ADR number, architecture order, source preference,
or scope width never silently wins.

For overlapping non-superseded incompatible rules, compute the stable
`CONFLICT-*` ID from sorted rule IDs plus overlap scope; retain every path/section/
revision and mark BLOCKED. Do not choose/merge/downgrade/waive inside this derived
workflow.

Ambiguous/malformed normative wording, missing source/scope/TR/lifecycle data, or
unverified engine coverage creates deterministic `UNKNOWN-*` and no executable
rule. A possibly mandatory UNKNOWN blocks Active eligibility.

Unresolved BLOCKED conflict or blocking UNKNOWN prevents a complete publish. A
PARTIAL diagnostic Draft is permitted only when excluded rules/limitations are
explicit and downstream use is forbidden.

---

## Phase 6: Render canonical candidate and rule-level diff

Render exact UTF-8/LF `cgs.control-manifest/v2` sections from the reference
contract. New/changed author output always uses:

```text
Status: DRAFT | PARTIAL
External Review: NOT_CURRENT
```

Version/payload rules:

- CREATE version = 1;
- content/provenance UPDATE version = base + 1;
- exact no-op preserves base version/generated time and writes nothing;
- Payload revision is canonical semantic payload identity, excluding volatile/
  status/review/self fields; and
- exact candidate artifact revision is external, never embedded as its own revision.

For update construct BASE + deterministic current SOURCES -> CANDIDATE and show
stable-ID diff sets: unchanged, provenance-only, added, retired/superseded,
level/scope/meaning replacement, conflict/unknown changes, ADR/TR/engine coverage,
preserved `x-local-*`, version/payload/artifact delta, and appended provenance.

Never delete a prior rule silently. A no-longer-current source retires the rule with
reason/evidence. Preserve Local Extensions unchanged and non-authoritative; they
cannot override/suppress/relevel derived rules.

Append exactly one immutable provenance event for an actual content update. Never
edit prior events. If semantic payload, source manifest, formatted bytes, and
provenance are identical, operation UNCHANGED and no event/version/time change.

Show complete candidate/lossless representation, source manifest/limits,
architecture/review/ADR/TR states, every rule/finding/source, complete diff,
version/payload/candidate revisions, local extensions, provenance event, conflicts,
unknowns, and Active blockers.

The user may correct extraction only by pointing to loaded source evidence. Do not
add an unsourced rule, remove a source mandate, change level/scope, or waive a
conflict because a different control policy is preferred; revise the authoritative
source separately.

---

## Phase 7: Approve one changeset and execute atomic conflict check

Preview exactly:

```text
docs/architecture/control-manifest.md: CREATE | REPLACE with candidate_revision
all other persistent writes: NONE
```

Obtain one approval bound to the complete preview/diff, source manifest, base,
ruleset, architecture/review/ADR/TR evidence, rules/findings, version/payload/
candidate revisions, provenance append, Local Extensions, and destination parent.
This is file authorization only—not source approval, independent review, Active
recording, story freshness, or gate permission.

If declined, return STOPPED/DECLINED and zero writes. Do not ask again per rule,
layer, source, or section.

Immediately before mutation, execute the reference-contract atomic conflict check over the complete
bound closure, directory membership, base/provenance, deterministic extraction,
diff, version, payload, and rerendered candidate.

Any mismatch is BLOCKED/CONFLICT with exact old/new evidence and zero writes. Do
not merge, refresh, retry, overwrite, request a new review, or implicitly accept
changed bytes.

After atomic conflict check, atomically publish only exact candidate bytes, re-read and verify
artifact revision/v2 schema/version/payload/source ledger/stable rules/conflicts/
unknowns/extensions/provenance/DRAFT-or-PARTIAL/NOT_CURRENT, and confirm no other
persistent path changed.

- verified publication -> CREATE/UPDATE and this authoring may be COMPLETE;
- pre-publication failure -> FAILED/BLOCKED;
- publication/read-back/result uncertainty -> PARTIAL with exact observed state,
  never COMPLETE or Active.

Never repair or revert external concurrent changes.

---

## Phase 8: Observe prior review and route one external action

When prior control-manifest review is explicitly supplied, validate it only under
the catalog-declared generic/extension/ruleset contract. Require exact current
artifact/payload/source-manifest revisions, complete rule/conflict/unknown coverage,
internal identity, reviewer/author separation when declared, and passing/nonpassing
verdict preserved exactly.

Any changed byte/source/ruleset/profile/scope makes it STALE. Never retarget/edit/
save the record or set Active. If catalog declares no compatible reviewer schema,
report UNKNOWN instead of inventing one.

Choose exactly one highest-priority catalog-derived action:

1. refresh/resolve current architecture, architecture review, TR, or ADR lifecycle
   evidence;
2. resolve first deterministic BLOCKED/UNKNOWN source conflict;
3. run independent control-manifest review for exact current revisions;
4. invoke a separate Active recorder when all exact conditions are declared/met;
5. route to the unique downstream consumer only for a current Active receipt; or
6. Stop.

Do not print a roadmap, infer downstream story freshness from date/version alone,
claim gate readiness from file presence, or invoke anything.

Return:

- workflow/profile/operation/context states;
- catalog identity/revision and route ID/command or gap;
- manifest path/base/candidate/on-disk artifact revisions;
- source manifest ID and budget use;
- architecture path/revision/review/currentness and stable TR states;
- ADR/lifecycle/engine source states;
- base/candidate monotonic versions and payload revisions;
- rule/retired/conflict/unknown IDs and rule-level diff;
- Local Extensions and provenance event/chain state;
- external manifest-review state/record/revision;
- Active blockers and exactly one next action;
- `Active Mutation: NONE`, `Review Record Mutation: NONE`,
  `Source Mutation: NONE`, `Session-State Mutation: NONE`,
  `Auto Executed: false`.

Then stop.

## Status mapping

- invalid invocation/root/catalog target identity -> ERROR;
- profile/base/provenance/architecture/TR/ADR/rule identity or conflict blocker ->
  BLOCKED;
- incomplete context/evidence/source parse or uncertain resulting state -> PARTIAL;
- declined changeset -> STOPPED;
- verified DRAFT transaction, honest UNCHANGED, or complete read-only audit ->
  COMPLETE for this workflow only.
