# Create Architecture — Evidence, Projection, and Transaction Contract

This contract is normative for `$create-architecture`. It defines source
authority, bounded manifests, current cross-GDD and ADR evidence, stable technical
requirement mappings, engine-knowledge states, derived-document provenance, and
the only permitted compare-and-set transaction.

## 1. Authority matrix

| Information | Authoritative owner | Architecture treatment |
|---|---|---|
| Player-facing/product requirement | Current approved GDD requirement and its lifecycle evidence | Derived source reference only |
| Cross-GDD consistency/review state | Current `review-all-gdds` evidence for the exact GDD manifest | Admission/readiness evidence, never product truth |
| Binding technical decision | Current Accepted ADR plus lifecycle evidence | Derived projection citing exact ADR/lifecycle revisions |
| Proposed/missing technical decision | ADR author/lifecycle owner | Non-binding `DECISION-*` gap only |
| Engine/API fact | Pinned engine reference with current provenance and applicable coverage | Verified observation or explicit UNVERIFIED marker |
| Architecture review verdict | Independent `architecture-review` evidence | External currentness reference only |
| Architecture READY status | Separate catalog-declared recorder | Never authored by `$create-architecture` |

`docs/architecture/architecture.md` is a derived view. It never overrides, edits,
accepts, rejects, supersedes, or repairs a GDD, review record, requirement lifecycle
record, ADR, ADR lifecycle record, engine reference, catalog, registry, or gate
record.

The only persistent output owned by this workflow is:

```text
docs/architecture/architecture.md
```

Atomic publication may use one same-directory temporary file after successful CAS;
the temporary file must be consumed or removed and is never an artifact. Session
state, skeleton checkpoints, review records, sign-off, and latest pointers are not
owned outputs.

## 2. Bounded source manifest

Freeze one repository-root identity and one UTC snapshot. Record exact raw bytes,
normalized project-relative path, real-path/root check, role, stable source ID,
selected scope, source state, revision when declared, and declared revision or an
explicit `ABSENT`/`UNREADABLE` marker.

Hard ceilings:

| Class | Allowed source | Count | Per file | Class bytes |
|---|---|---:|---:|---:|
| Workflow catalog | `.codex/docs/workflow-catalog.yaml` | 1 | 512 KiB | 512 KiB |
| Technical preferences | `.codex/docs/technical-preferences.md` | 1 | 256 KiB | 256 KiB |
| Target architecture | `docs/architecture/architecture.md` or ABSENT | 1 | 2 MiB | 2 MiB |
| Systems index | catalog-bound `design/gdd/systems-index.md` | 1 | 1 MiB | 1 MiB |
| Cross-GDD evidence | one explicit path/inline `cgs.review-evidence/v1` | 1 | 2 MiB | 2 MiB |
| System GDD | exact paths from the cross-GDD manifest or bounded systems-index rows | 64 | 512 KiB | 16 MiB |
| Per-GDD approval evidence | exact records named by cross-GDD evidence/explicit GDD links | 64 | 256 KiB | 8 MiB |
| ADR | catalog-declared direct-child ADR paths or exact architecture links | 64 | 512 KiB | 16 MiB |
| ADR lifecycle/review evidence | exact paths linked by ADR/registry entries | 64 | 256 KiB | 8 MiB |
| Architecture registry | `docs/registry/architecture.yaml` when present | 1 | 1 MiB | 1 MiB |
| Engine version/reference | pinned VERSION plus exact references linked by admitted ADRs | 32 | 512 KiB | 8 MiB |
| Project standards | exact catalog/ADR-linked standards | 16 | 256 KiB | 2 MiB |
| Prior independent architecture review | one explicit currentness candidate | 1 | 2 MiB | 2 MiB |

Total bytes read must not exceed 48 MiB. Enumerate only direct children when a
catalog artifact glob permits enumeration. Sort by normalized path, stop before a
count/byte limit, never recurse, never follow a symlink outside the root, and never
select newest/nearest evidence.

Use layered loading:

1. read catalog, target state, systems index, and supplied evidence envelopes;
2. parse their typed indexes/manifests without loading every referenced body;
3. construct the complete intended path/record manifest;
4. load only the exact source sections required by the selected profile; and
5. re-read all complete source files before candidate approval and CAS.

revision validation a source does not authorize full-context ingestion. When a required file,
record, typed index, or section exceeds a limit, is ambiguous/unreadable, changes
during the snapshot, or cannot fit the manifest, use `PARTIAL` with exact
`CONTEXT_BUDGET_EXCEEDED`, `SOURCE_UNREADABLE`, `SOURCE_CHANGED`, or schema reason.
Do not sample and call coverage complete.

Canonicalize the ordered manifest as JSON: lexicographic object keys; array order
by role, stable source ID, normalized path, then consumed scope; UTF-8/LF; no
insignificant whitespace. Its identity is:

```text
source_manifest_id: <stable manifest business ID plus UTC run ID>
```

Every candidate and final result binds this ID. A changed path, byte, state,
revision, approval/lifecycle record, selected scope, or directory membership makes
the manifest stale.

## 3. Current GDD and cross-GDD evidence

One cross-GDD evidence input may be supplied by exact path plus expected raw revision,
or as exactly one explicit inline record. Never discover a report by timestamp or
filename.

A usable cross-GDD record must be:

- envelope schema `cgs.review-evidence/v1`;
- producer `review-all-gdds` with extension schema
  `cgs.cross-gdd-review/v2`;
- internally valid `record_id bound to the stable artifact ID and UTC run ID;
- bound to the same project/root, ruleset, complete ordered GDD/supporting manifest,
  `manifest_revision`, and current exact source revisions;
- coverage `COMPLETE`; and
- verdict `PASS`, `CONCERNS`, `FAIL`, or `PARTIAL` preserved exactly.

For every GDD used, validate declared its exact revision and its per-GDD approval evidence:
envelope `cgs.review-evidence/v1`, producer `design-review`, exact artifact
path/revision, current record revision, and verdict `APPROVED`. Classify each source:

- `APPROVED_CURRENT` — exact current independent APPROVED evidence;
- `PROVISIONAL_EXPLICIT` — user explicitly admitted the exact path/revision for Draft
  work despite missing/non-current approval;
- `STALE` — approval/cross-GDD evidence targets different bytes/manifest;
- `UNBOUND` — record identity/path/project does not bind;
- `CONFLICT` — current records disagree; or
- `UNKNOWN` — missing, unreadable, malformed, or incomplete evidence.

Only `APPROVED_CURRENT` source requirements can populate the approved derived TR
map. `PROVISIONAL_EXPLICIT` content is allowed only in a separate non-binding
provisional section after the user sees the exact limitation and opts in. It cannot
support binding architecture text, ADR coverage, READY eligibility, or a claim of
complete requirements.

Cross-GDD verdict state is independent:

- current `PASS` with COMPLETE coverage can satisfy the cross-source readiness
  precondition;
- current `CONCERNS` keeps exact findings visible and blocks READY eligibility;
- `FAIL` blocks authoritative projection of affected claims;
- `PARTIAL`, missing, stale, unbound, conflict, or unknown forces a DRAFT/PARTIAL
  limitation and can never be described as cross-GDD complete.

Filename, `Status: Approved` text, directory membership, systems-index status,
conversation memory, or the architecture's prior manifest never establishes GDD
approval.

## 4. Stable derived TR mapping

The architecture contains a derived traceability map, not a requirement lifecycle
registry. Product requirement text and approval remain owned by source GDDs and
their lifecycle evidence.

Each row contains:

```text
tr_id
source_requirement_id | NONE
source_artifact_id
source_path
source_locator
exact_normative_text
source_revision
approval_record_id
approval_record_revision
class: EXPLICIT_REQUIREMENT | CONFIRMED_REQUIREMENT
currentness: CURRENT | CHANGED | STALE | UNBOUND
adr_ids_and_revisions
mapping_state: DERIVED_COVERED | DECISION_GAP | SOURCE_BLOCKED
```

ID construction:

1. When the approved source owns a stable requirement ID, use TR-<source-artifact-id>-<source-requirement-id>.
2. Without a source ID, allocate TR-<source-artifact-id>-<locator-business-id> once in the persisted mapping ledger from the approved locator business key; reuse it on later runs.
3. Preserve every persisted TR ID exactly on resume/focus. Never regenerate or
   renumber the full set because order or unrelated source content changed.

If a source-owned requirement ID remains the same but text/revision changes, preserve
the TR ID and mark `CHANGED` until current approval evidence covers the new bytes.
If a stable business key-based source changes identity/text/locator, propose a new TR ID
and an explicit `TR-MIGRATION-*` old→new/superseded record; never silently retarget.
Duplicate source identities, collisions, ambiguous locators, missing exact text,
or conflicting prior mappings block publication.

Inferred technical needs never enter this map. An inference appears only as
`INFERRED_CANDIDATE` with rationale/source provenance. Explicit user/technical-owner
confirmation may create `CONFIRMED_REQUIREMENT` only when the confirmation record
names the candidate, exact source context/revision, confirmer identity, decision ID,
timestamp, and bounded requirement text. Confirmation does not approve a GDD or an
ADR and cannot upgrade a provisional source.

## 5. ADR decision authority and derived ledger

For every in-scope ADR, record path, ADR ID/title, exact revision, declared status,
requirements addressed, decision domains, dependency/supersession IDs, and exact
lifecycle/review evidence paths/revisions.

An ADR is `ACCEPTED_CURRENT` only when all are true:

- one unique valid stable ADR ID and `Status: Accepted`;
- exact current bytes/revision in the source manifest;
- a current catalog-compatible lifecycle record binds ADR path/revision, transition to
  Accepted, recorder identity/time, and independent review evidence;
- any required supersession/dependency chain is complete and current; and
- no conflicting Accepted lifecycle record or registry projection exists.

Other states are `PROPOSED`, `SUPERSEDED`, `REJECTED`, `STALE`, `UNBOUND`,
`CONFLICT`, or `UNKNOWN`. Preserve the observed state; do not choose or repair it.

Only `ACCEPTED_CURRENT` ADR decisions may create a binding-looking derived
statement. Each such statement includes:

```text
DERIVED — <ADR-ID>@<ADR-revision>
lifecycle_record_id: <ID>
lifecycle_record_revision: <revision>
source_tr_ids: [<TR IDs>]
```

Every technical choice without one current Accepted owner is a non-binding gap:

```text
NON-BINDING — DECISION-<stable business key>
blocked_tr_ids: [<TR IDs>]
observed_adr_state: <state-or-NONE>
```

`DECISION-*` identity derives from decision domain, sorted TR IDs, and normalized
scope; preserve it across revisions while that gap is the same. Do not select an
engine API, module owner, public interface, data-flow mechanism, thread boundary,
storage format, network protocol, or other low-level choice in this workflow. An
open decision routes to the catalog's ADR authoring/lifecycle owner; options and
acceptance belong there.

Required Proposed/STALE/UNBOUND/CONFLICT/UNKNOWN ADRs, missing Accepted coverage,
and unresolved DECISION gaps block READY eligibility. They do not prevent a clearly
non-binding DRAFT unless a selected profile cannot render safely.

## 6. Engine knowledge state

The pinned engine/version and references are evidence, not capability truth.
For each consumed domain record engine, version, reference path/revision, publication
or snapshot date, applicable API/module scope, source revision, and coverage.

Classify:

- `CURRENT_COMPLETE` — pinned version matches and the exact needed domain is fully
  covered by a current authoritative reference;
- `CURRENT_PARTIAL` — current reference explicitly covers only part of the claim;
- `STALE` — version/date/revision does not match;
- `MISSING` — required reference is absent;
- `UNSUPPORTED` — the claimed domain/API is outside declared coverage;
- `UNREADABLE`; or
- `CONFLICT` — current references disagree.

Only `CURRENT_COMPLETE` may support a verified engine fact. All other states are
`UNVERIFIED` in the architecture, preserve the ADR decision separately, identify
the exact unsupported claim, and block READY when implementation depends on it.
Never search the entire engine source tree, browse the web, or claim every API was
verified.

## 7. Canonical derived document

The exact UTF-8/LF candidate follows `cgs.master-architecture/v3` and contains:

1. Document Status — schema, artifact revision, `DRAFT|PARTIAL`, manifest ID,
   prior artifact revision, and external review state/reference;
2. Authority Boundary;
3. Source Manifest projection;
4. Current GDD/Cross-GDD Evidence;
5. Stable Derived TR Map;
6. Provisional Inputs and Inferred Candidates;
7. ADR Decision Ledger;
8. System Layer Map;
9. Module Ownership;
10. Data Flow;
11. API Boundaries;
12. Engine Knowledge and Verification;
13. Required ADR/Decision Gaps;
14. Open Questions and READY Blockers; and
15. Immutable Revision/Provenance History.

Assign candidate_revision from the explicit base revision plus one, or 1 for create, before rendering. Store that revision and the source manifest business ID in the document and transaction result. Do not derive either value from candidate bytes.

Every content change authored here sets document status `DRAFT` or `PARTIAL`,
external review state `NOT_CURRENT`, and appends one immutable provenance event:
event ID, profile/focus scope, base revision/absence, candidate manifest ID, decision
IDs, changed sections, timestamp, and author-side task identity. Prior events are
never edited, deleted, reordered, or rewritten.

## 8. Profile mutation matrix

| Profile | Preconditions | Reads | Architecture mutation |
|---|---|---|---|
| `new` | target ABSENT | complete bounded manifest | create one complete v3 DRAFT/PARTIAL candidate |
| `resume` | valid v3 DRAFT/PARTIAL target | complete bounded manifest plus base | only explicitly selected incomplete/stale sections and mechanically affected manifest/TR/ledger/status/history fields |
| `focus requirements` | valid v3 target | sources needed for TR/provenance | TR map, provisional/candidate tables, affected decision-gap links, status/history |
| `focus decision-ledger` | valid v3 target | ADR/lifecycle sources | decision ledger, affected derived citations/gaps, status/history |
| `focus layers|ownership|data-flow|api-boundaries|engine` | valid v3 target | exact section dependency closure | selected section, directly affected citations/blockers, status/history |
| `audit` | existing target | bounded validation closure | NONE |

`new` first renders the complete skeleton in memory, then fills selected sections;
there is no early on-disk skeleton or session checkpoint. `resume` and `focus` use a
BASE→authorized INTENT→CANDIDATE three-way diff and preserve every out-of-scope byte
or canonical field. `audit` creates no temporary file, checkpoint, report, or
review request.

Unsupported/malformed legacy targets are `BLOCKED_UNSUPPORTED_BASE`; do not
silently retrofit, replace, or treat them as absent. Migration requires a separate
explicitly authorized profile/owner not defined by this skill.

## 9. Approval, CAS, and atomic publication

Show the complete candidate or lossless representation, structured three-way diff,
manifest entries/revision/limits, TR migrations, ADR/engine states, blockers, exact
candidate bytes/revision, and one-file changeset. Obtain one user approval bound to
candidate revision, manifest ID, profile/focus, decision IDs, and exact diff. Content
approval is neither ADR acceptance nor architecture review/READY approval.

The preview binds:

- root identity and destination parent state;
- catalog, technical preferences, systems index, and target base/absence;
- cross-GDD/per-GDD evidence and all GDD bytes/source states;
- ADR/registry/lifecycle/review evidence;
- engine references and project standards;
- every enumerated directory identity/membership used;
- source manifest ID, exact candidate bytes/revision, immutable history preimage, and
  ordered decision IDs.

Immediately before mutation, re-read the complete closure, rebuild the
canonical manifest, reapply BASE+INTENT, and require every bound state/revision plus
candidate revision to match the preview.

Any difference is `CONFLICT`: write nothing; report exact old/new revisions or states;
do not merge, refresh, retry, overwrite, update session state, or ask the user to
implicitly accept changed bytes.

After CAS succeeds:

1. write exact candidate bytes to one same-directory temporary file;
2. flush/close as supported;
3. atomically create/replace only `docs/architecture/architecture.md`;
4. re-read and verify exact candidate revision;
5. reparse and validate v3 schema, manifest ID, TR identities/migrations, ADR
   citations, profile mutation boundary, immutable provenance chain, DRAFT/PARTIAL
   status, and external review `NOT_CURRENT`; and
6. confirm no other persistent path changed because of this workflow.

Report `WRITTEN` only after all verification passes. Pre-publication failure is
`FAILED` with no success. Publication/read-back or resulting-state uncertainty is
`PARTIAL` and must name exact observed state; do not claim completion, repair an
external change, or promote status.

## 10. Independent review and READY separation

`$create-architecture` never dispatches or impersonates reviewers and never writes
a review record or READY transition. It may consume one explicitly identified
prior architecture-review record only to report currentness.

A usable independent review record is `cgs.review-evidence/v1` with producer
`architecture-review`, extension `cgs.architecture-review/v2`, current record
identity, complete coverage, and verdict `PASS|BLOCKED|PARTIAL`. Its manifest must
contain `docs/architecture/architecture.md` with role `architecture-derived` and
the exact candidate/current artifact revision, plus every source identity/revision needed
to reproduce or explicitly bind the document's `source_manifest_id`. Missing or
different architecture/source entries make the record stale or unbound. `PASS` is
necessary but not sufficient for READY and becomes stale after any artifact,
source-manifest, mode, target, scope, profile, or ruleset change. Only a current
`full` PASS can be READY-eligible; narrower modes remain bounded evidence for their
declared scope.

Only a separate catalog-declared recorder may set READY after independently
validating current PASS, exact candidate revision, approved/current GDD sources,
cross-GDD PASS, complete Accepted ADR coverage, no blocking DECISION/TR/engine gap,
and its own compare-and-set policy. This authoring workflow returns one
catalog-derived review/ADR/evidence action or `Stop` and never executes it.
