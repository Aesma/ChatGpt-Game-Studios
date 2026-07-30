---
name: consistency-check
description: "Read-only, revision-bound cross-GDD consistency audit over typed claims, ownership, formulas, and dependencies that returns PASS, FINDINGS, PARTIAL, or ERROR."
---

# Consistency Check

Contract version: `cgs.consistency-check/v2`.
Claim ruleset: `cgs.consistency-claims/v1`.

Audit cross-document design consistency without changing the project. Build one
bounded, exact-revision manifest, compare typed claims from every in-scope system GDD,
and optionally treat `design/registry/entities.yaml` as another attributed claim
source. The registry and its `source` fields are never automatic product truth.

## Invocation and frozen contract

Invoke as:

```text
$consistency-check [full | entity:<id> | item:<id>]
$consistency-check since-last-review baseline:<project-relative-report-path>
```

No mode is equivalent to `full`. Accept exactly one mode. `entity:` and `item:`
IDs must be non-empty lowercase kebab-case and are matched as exact stable IDs,
not aliases or display names. `baseline:` is required exactly once for
`since-last-review` and forbidden in every other mode. Reject unknown arguments,
extra text, duplicate modes or baselines, URLs, globs, absolute/outside-project
paths, symlinks, and missing option values with `ERROR — INVALID INVOCATION`.
Show the exact grammar, emit no evidence record, and stop.

This workflow is strictly read-only:

- It may enumerate, revision, search, and read project files and inspect read-only
  Git state.
- It must not create, edit, append, rename, or delete any file.
- It must not update GDDs, the systems index, entity registry, consistency logs,
  saved reports, lifecycle state, approval state, or session state.
- It must not run another skill, spawn a director gate, or delegate remediation.
- Its only deliverable is one complete report returned to the caller. A separate
  recorder may later persist those exact report bytes, but this scanner never
  chooses a path or performs that write.

Verdict contract: exactly `PASS | FINDINGS | PARTIAL | ERROR`.

- `PASS`: required coverage is complete and there is no actionable finding.
- `FINDINGS`: required coverage is complete and at least one actionable finding
  is `OPEN` or `DECISION_REQUIRED`.
- `PARTIAL`: useful evidence exists, but any material input, claim, comparison,
  provenance channel, or required check is incomplete. It takes precedence over
  `FINDINGS` and preserves proven findings.
- `ERROR`: invocation/scope is invalid, fewer than two system GDDs are reviewable,
  no in-scope GDD can be semantically read, the input manifest changes during the
  scan, or a meaningful report cannot be constructed.

Dependency gaps are findings, not a verdict. Registry absence never means
“nothing to check”: perform the direct-GDD scan, disclose the missing coverage
channel, and return `PARTIAL`, never `PASS`.

---

## Phase 0: Resolve instructions, project identity, and scope

Read in full every applicable `AGENTS.md` from repository root through
`design/gdd/`, in root-to-target order, and list them in the report. The nearest
file wins when rules differ.

Represent project_id as the stable string root=<forward-slash-canonical-root>;git-root=<root-commit-or-null>. Use project_id directly with the UTC run ID for artifact identities; do not derive another ID from its bytes. Repository identity is the read-only Git root commit when available. If Git is unavailable,
use `null`, continue with exact current file revisions, record Git provenance as
unavailable, and force `PARTIAL`; never guess a commit or emit `PASS`.

Inventory direct children matching `design/gdd/*.md`. Exclude
`game-concept.md`, `game-pillars.md`, `systems-index.md`, templates, generated
cross-review or consistency reports, review logs, and non-system profiles.

Read `design/gdd/systems-index.md` when present and resolve exact stable
`System ID` and normalized `Design Doc` cells. Include every discovered system
GDD in the manifest:

- a unique index match supplies canonical system identity;
- an unindexed GDD remains `PROVISIONAL_DISCOVERY` and forces `PARTIAL`;
- duplicate IDs, normalization collisions, two IDs sharing a path, or one path
  mapping to multiple rows are coverage conflicts and force `PARTIAL`;
- a missing or malformed systems index does not stop direct discovery, but
  canonical scope is unavailable and the run is `PARTIAL`.

If fewer than two system GDDs are reviewable, return
`ERROR — CONSISTENCY CHECK REQUIRES TWO SYSTEM GDDS`, emit no evidence record,
and stop. Targeted `entity:` and `item:` modes still scan the complete system-GDD
corpus before filtering typed claims to the requested ID.

Read `design/registry/entities.yaml` when present:

- valid non-empty registry: parse attributed typed claims under its declared IDs;
- missing or empty registry: continue direct-GDD comparison, mark registry
  coverage as unavailable, and force `PARTIAL`;
- malformed or unreadable registry: preserve direct-GDD results, mark the exact
  failure, and force `PARTIAL`;
- a registry `source` field records provenance only, never authority, approval,
  ownership, or currentness.

For `since-last-review`, the baseline must be one explicitly supplied,
project-local, non-symlink regular file no larger than 1 MiB. Validate its
`cgs.review-evidence/v1` record ID, producer `consistency-check`, extension schema
`cgs.consistency-report/v1`, project ID, ruleset ID, complete path/revision manifest,
run ID, and exact prior findings. A missing, ambiguous, malformed, stale,
scope-incomplete, or revision-invalid baseline returns
`ERROR — INVALID CONSISTENCY BASELINE`; do not select a report by filename,
modification time, creation date, or “latest” Git history.

---

## Phase 1: Lock a bounded exact-revision manifest

Create and sort the complete candidate inventory by stable system ID, then
canonical path. revision exact raw bytes; never revision normalized or copied text. Lock
the manifest before semantic comparison and record:

- project ID, requested mode, contract/ruleset IDs;
- source revision commit or `null`, plus `clean`, `dirty`,
  `includes-untracked-inputs`, or `git-unavailable`;
- every included and excluded candidate path, reason, stable system ID or null,
  exact revision, exact byte count, and planned semantic status;
- systems-index, registry, applicable instruction, and baseline paths/revisions when
  present; and
- every required check: `VALUE`, `FORMULA`, `OWNERSHIP`, `DEPENDENCY`, and
  `REFERENCE`.

Use these fixed upper bounds:

```yaml
max_manifest_candidates: 256
max_semantically_analyzed_gdds: 32
max_single_gdd_bytes: 196608
max_total_semantic_input_bytes: 1048576
max_registry_entries: 2048
max_indexed_claims: 4096
```

Enumerating and streaming revisions does not consume the semantic byte budget, but
the manifest candidate cap still applies. If any cap is exceeded, retain the
complete deterministically enumerable inventory, select GDDs in manifest order
without exceeding a limit, mark all remaining paths/checks unchecked, and force
`PARTIAL`. Never raise a limit, silently omit a path, split one GDD into
independently judged fragments, or infer complete coverage from a sample.

manifest_revision is an explicit monotonic revision for the ordered manifest.
stale_key is a stable business scope key assembled from project ID, ruleset ID,
mode, and the sorted complete current system-GDD path/revision set. Timestamps,
filenames of reports, and Git modification times never participate.

re-read every in-scope input immediately before finalizing the report. Any added,
removed, renamed, or changed input after manifest lock returns
`ERROR — INPUT CHANGED DURING SCAN`; emit no consistency evidence from mixed
bytes.

---

## Phase 2: Build the typed claim, owner, and dependency indexes once

Read each selected GDD in full exactly once. A failed or partial read marks that
file and all five checks `FAILED`, preserves other completed work, and forces
`PARTIAL`. If no GDD can be read semantically, return `ERROR`.

### 2a. Typed claim schema

Index only a normative claim with identifiable evidence. Every claim uses:

```yaml
claim_id: CLM-<stable-business-id>
source_system_id: <SYS-id or provisional path identity>
subject:
  kind: system | entity | item | resource | formula-output | requirement
  id: <explicit stable ID>
category: VALUE | FORMULA | OWNERSHIP | DEPENDENCY | REFERENCE
attribute: <normalized field, relationship, or formula output ID>
scope: <normalized applicability and conditions>
normative: true
value:
  type: integer | decimal | boolean | enum | string | expression | relationship
  raw: <bounded exact text>
  normalized: <typed normalized value or null>
  unit: <canonical unit or null>
formula:
  normalized_ast: <typed operator tree or null>
  symbols: <stable symbol-to-type/unit map or null>
owner:
  owner_id: <stable system/artifact/role ID or null>
  exclusive: true | false | null
evidence:
  path: <canonical path>
  revision: <exact current file revision>
  section: <canonical heading>
  line_or_anchor: <stable requirement/claim ID, otherwise bounded line location>
  excerpt: <short exact evidence>
```

Prefer an explicit claim/requirement ID. Otherwise derive `claim_id` from source
system ID, category, subject ID, attribute, normalized scope, evidence heading,
and occurrence ordinal. Exclude raw value, wording, file revision, line number,
severity, and run date so the same logical claim retains identity after a value
edit or line movement.

Subject identity must come from an exact stable ID in a GDD, systems index, or
registry. A display name, nearby noun, alias, case-insensitive guess, or fuzzy
filename cannot establish identity. If an alias resolves to zero or multiple
stable IDs, record `UNVERIFIABLE_IDENTITY`; do not merge claims.

Normative claims come from explicit rules, schema tables, formulas, ownership
declarations, dependency declarations, or acceptance criteria. Examples,
historical values, rejected alternatives, commentary, estimates, and prose
speculation are not normative claims. Do not extract a number merely because it
occurs near a familiar name.

### 2b. Semantic normalization

Normalize only when type, identity, scope, and unit are explicit. The closed
unit-conversion table is:

- time: `1000 ms = 1 s`;
- distance: `1000 mm = 100 cm = 1 m`;
- mass: `1000 g = 1 kg`;
- ratio: `100 percent = 1 ratio`.

Use exact rational conversion. Currency/resource units compare only when their
stable resource ID is identical. Never convert different dimensions or infer a
unit from convention. Non-listed, ambiguous, compound, or missing required units
are `UNVERIFIABLE_UNIT`.

Normalize formulas only when output ID, operator structure, every symbol, symbol
type/unit, applicability, clamp/rounding behavior, and input domain are explicit.
Store a typed operator tree rather than comparing display strings. An unparseable
rule-critical formula is a material coverage gap and forces `PARTIAL`; incidental
formula prose becomes an advisory unverifiable note.

### 2c. Owner map

Build one map from stable subject/attribute to every explicit owner claim. Only
`exclusive: true` can establish competing exclusive ownership. Missing or vague
owner metadata is `UNVERIFIABLE_OWNER`; it is not silently assigned to the source
GDD. Two non-exclusive collaborators are not a conflict.

### 2d. Directed dependency graph

The systems-index `Depends On IDs` cell is the authoritative declared edge:
`A depends on B` means `A -> B`. Compare each GDD's explicit outgoing dependency
claims to that row. Reverse dependents are derived by traversal; never require B
to restate `A -> B`.

Classify each declared dependency exactly once:

- `exists`: stable target row and current target GDD both resolve;
- `planned-not-authored`: target row is `Not Started` or `In Design` with no GDD;
  this is not a gap by itself;
- `missing-target`: no current or explicitly planned stable target exists;
- `broken-reference`: an explicit path is missing/outside the project, the index
  claims a missing Design Doc, or ID/path evidence disagrees;
- `declaration-mismatch`: GDD outgoing dependency and systems-index edge disagree.

Create actionable dependency findings for `missing-target`, `broken-reference`,
and `declaration-mismatch`. Preserve `planned-not-authored` in the dependency
ledger as non-actionable unless another current normative claim falsely requires
an already-authored interface.

Build the claim index in one pass and compare the completed typed index. Do not
run one repository search per registry entry or repeatedly reread a GDD.

---

## Phase 3: Compare only semantically comparable claims

Two claims are comparable only when stable subject ID, category/attribute,
normative status, overlapping applicability, and value type match, and their
units are identical or convertible by the closed table.

Create actionable findings only for these consumer-compatible categories:

- `VALUE_MISMATCH`: comparable typed values differ after exact conversion;
- `FORMULA_MISMATCH`: normalized formula trees for the same output/domain differ
  in operators, coefficients, symbols, caps, rounding, or allowed output;
- `COMPETING_OWNERSHIP`: two current explicit exclusive owner claims compete for
  the same stable subject/attribute;
- `DEPENDENCY_GAP`: subtype `MISSING_TARGET`, `BROKEN_REFERENCE`, or
  `DECLARATION_MISMATCH` from the directed dependency graph;
- `STALE_REFERENCE`: a current normative reference names a removed, renamed, or
  superseded stable target and no explicit current replacement resolves it;
- `MISSING_CLAIM`: a targeted exact entity/item ID has no supported normative
  claim after complete filtering.

Do not report a mismatch when values are equivalent after exact unit conversion,
conditions do not overlap, subject IDs differ, either passage is an example or
history, or semantic normalization is unverifiable. Material unverifiability is
a coverage gap and forces `PARTIAL`; non-material ambiguity is an advisory note.

Every competing-claim finding must show at least two complete claim sides. A
dependency or missing-claim finding instead shows the declaring claim plus the
complete manifest/graph lookup that failed to resolve it.

Severity is impact provenance, not product truth:

- `HIGH`: mutually exclusive normative formulas, typed values, or exclusive
  ownership can change core behavior or block downstream architecture;
- `MEDIUM`: a required dependency gap, stale reference, or bounded mismatch can
  invalidate a dependent system;
- `LOW`: a real, isolated actionable contradiction with limited downstream
  effect;
- `ADVISORY`: non-actionable observation with complete but non-normative evidence;
- `COVERAGE_GAP`: required semantic or input evidence is incomplete.

### Product-truth boundary

Never choose which current claim is correct because of registry provenance,
filename, lifecycle status, recency, source ordering, severity, or majority vote.
Never choose a new number, formula, owner, or dependency for the user. Competing
claims without current explicit decision evidence use status
`DECISION_REQUIRED` and name the artifact owner or user decision needed.

Only a current, exact-revision approved decision artifact that explicitly selects a
claim may support `RESOLVED_IN_CURRENT`. Cite it, revision it, and keep it in the
manifest. The scanner still never modifies any target.

---

## Phase 4: Assign stable finding identity and re-evaluate a baseline

Every finding uses:

```yaml
id: CSC-<category-slug>-<stable-business-id>
business_key: <explicit revision>
category: VALUE_MISMATCH | FORMULA_MISMATCH | COMPETING_OWNERSHIP | DEPENDENCY_GAP | STALE_REFERENCE | MISSING_CLAIM
subcategory: <bounded subtype or null>
severity: HIGH | MEDIUM | LOW | ADVISORY | COVERAGE_GAP
subject_id: <stable subject/system ID>
attribute_or_relationship: <normalized value>
claim_a: <complete typed claim side or declaring claim>
claim_b: <complete typed claim side, missing target, or manifest lookup>
owners: [<stable owner IDs or UNKNOWN>]
target_revisions:
  - path: <canonical path>
    revision: <exact current revision>
status: OPEN | DECISION_REQUIRED | RESOLVED_IN_CURRENT
acceptance: <objective current-input condition that closes the finding>
resolution_evidence: <current exact-revision evidence or null>
first_seen_run_id: <run ID>
last_evaluated_run_id: <run ID>
producer_claim_ids: [<sorted stable claim IDs>]
```

stable business key is assembled from declared category, subcategory, stable subject ID,
attribute/relationship, sorted source system IDs, and sorted stable claim IDs.
Exclude raw values, wording, paths, revisions, severity, status, reviewer, and time.
Thus value edits, path renames under a stable system ID, or rewording retain the
same finding ID; a different logical claim does not.

Sort findings by category, stable subject ID, attribute/relationship, then
stable business key. Deduplicate only identical stable business keys and retain all evidence
provenance. If identical stable business keys carry incompatible identity or evidence,
record the evidence conflict as a material coverage gap and return `PARTIAL`;
never choose one result.

For `since-last-review`, compare the validated baseline manifest with the current
manifest by stable system ID and classify added, removed, renamed, changed-revision,
or unchanged. Re-evaluate every prior actionable finding against current typed
claims, preserve its ID, and set `RESOLVED_IN_CURRENT` only when its acceptance is
demonstrably satisfied by current exact-revision evidence. Include newly proven
findings only when at least one claim side or dependency target changed; preserve
complete current-corpus coverage in the report.

Dirty and untracked current inputs participate through their exact bytes. The
baseline's commit is provenance, not a substitute for file revisions. Git rename
heuristics, modification time, report date, and filename recency never determine
identity or scope.

---

## Phase 5: Build the coverage ledger and choose the verdict

Record one row for every discovered system GDD, every required supporting input,
and every required check:

```yaml
path: <canonical path or channel ID>
system_id: <stable ID or null>
revision: <revision or null>
bytes: <integer or null>
status: IDENTIFIED_ONLY | INDEXED | PARTIAL | FAILED | EXCLUDED | MISSING
checks:
  VALUE: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  FORMULA: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  OWNERSHIP: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  DEPENDENCY: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  REFERENCE: DONE | PARTIAL | FAILED | NOT_APPLICABLE
limitation: <none or exact bounded reason>
```

Material coverage gaps include missing/empty/invalid registry, missing/malformed
systems index, Git provenance unavailable, unreadable GDD, invalid baseline,
manifest or semantic budget overflow, a material unnormalizable ID/unit/formula,
revision mismatch, evidence conflict, and any required unchecked comparison.

Apply exactly this precedence:

1. invalid invocation, fewer than two reviewable GDDs, no semantically readable
   GDD, changed locked input, or failed report construction: `ERROR`;
2. any material coverage gap: `PARTIAL`;
3. complete coverage with at least one actionable `OPEN` or
   `DECISION_REQUIRED` finding: `FINDINGS`;
4. complete coverage with no actionable finding: `PASS`.

Advisory notes do not cause `FINDINGS`. Never issue `PASS` from a registry-only
lookup, absent registry, absent systems index, subset/sample, empty text search,
or incomplete normalization.

---

## Phase 6: Return one revision-bound consistency report

When a manifest was locked and useful evidence exists, return one authoritative
machine block followed by a human projection. For invocation/scope errors before
manifest lock, return the error only and no evidence record. For an execution
`ERROR` after lock, return the partial manifest/coverage in a record whose verdict
is `ERROR`; downstream consumers must reject it.

Use this machine block:

```gate-evidence
schema: cgs.review-evidence/v1
record_id: <stable business record ID plus run_id>
artifact_id: consistency-scan:<project-id-prefix>:<manifest-prefix>
artifacts:
  - path: <canonical repository-relative path>
    revision: <declared revision for an existing exact-byte input>
    role: system-gdd | systems-index | entity-registry | decision-evidence | baseline
    system_id: <stable System ID or null>
reviewer: consistency-check:<run-id>
verdict: PASS | FINDINGS | PARTIAL | ERROR
timestamp: <ISO-8601 UTC>
finding_ids: [<sorted stable CSC IDs>]
producer:
  tool: consistency-check
  version: cgs.consistency-check/v2
extension:
  schema: cgs.consistency-report/v1
  ruleset_id: cgs.consistency-claims/v1
  run_id: <UTC timestamp>-<manifest prefix>
  project_id: <canonical root plus repository identity string>
  project_revision: <explicit project revision>
  requested_mode: full | since-last-review | entity | item
  targeted_id: <exact ID or null>
  source_revision:
    commit: <commit ID or null>
    input_state: clean | dirty | includes-untracked-inputs | git-unavailable
  manifest_revision: <ordered manifest revision>
  stale_key: <project/ruleset/mode/current-system-GDD-set revision>
  skill_revision: <exact current SKILL.md revision>
  coverage_status: COMPLETE | PARTIAL | ERROR
  limits:
    max_manifest_candidates: 256
    max_semantically_analyzed_gdds: 32
    max_single_gdd_bytes: 196608
    max_total_semantic_input_bytes: 1048576
    max_registry_entries: 2048
    max_indexed_claims: 4096
  baseline:
    path: <path or null>
    record_id: <record ID or null>
    manifest_revision: <revision or null>
    source_commit: <commit or null>
    deltas: []
  registry:
    status: AVAILABLE | MISSING | EMPTY | INVALID | UNREADABLE
    path: design/registry/entities.yaml
    revision: <revision or null>
    entries_indexed: <integer>
  claim_index_revision: <canonical typed claim index revision>
  owner_map_revision: <canonical owner map revision>
  dependency_graph_revision: <canonical directed graph revision>
  coverage: []
  findings: []
  advisory_notes: []
```

The `artifacts` array must include every existing current system GDD in the
complete review set, even when a semantic limit left it unchecked. Include
existing supporting inputs actually used. Missing required inputs appear only in
the coverage ledger with a null revision, never as a fake artifact. This lets
`$review-all-gdds` verify exact current path/revision coverage without rereading or
reinterpreting the registry.

Set record_id from the stable project/check scope plus the UTC run ID. Serialize the complete machine object as canonical JSON with record_id omitted, lexicographically sorted object keys, deterministic array ordering, UTF-8, JSON null for required absent values, and no insignificant whitespace. Assign the explicit report revision after the final verdict and coverage are known.

After the machine block, render from the same normalized data:

1. Run Identity and verdict;
2. Complete Input Manifest and Exclusions;
3. Registry and Baseline Status;
4. Coverage Ledger and exact limits/unchecked scope;
5. Typed Claim Summary;
6. Owner Map and Directed Dependency Ledger;
7. Actionable Findings with stable IDs and both evidence sides;
8. Advisory/Unverifiable Notes;
9. Decision Handoff naming the responsible owner without choosing truth; and
10. Staleness Contract stating that any changed path/revision invalidates the report.

The machine block and projection must agree. A mismatch before delivery is report
construction failure. Do not save the report, propose a report path, append a
failure log, update session state, or offer an in-workflow write.

Return one concise handoff and stop:

- `PASS`: provide `record_id`, manifest revision, and stale key for an already-planned
  downstream consumer.
- `FINDINGS`: route the highest-severity stable finding ID to its artifact owner
  or user for a separate decision/remediation task.
- `PARTIAL`: name the highest-priority coverage gap to restore before a fresh run.
- `ERROR`: correct the invocation/scope or restore the named failed input.

The handoff is not permission to edit, persist, advance stage, or invoke another
workflow automatically.

## Authoritative P1 traceability

This matrix records closure against the authoritative audit without changing the
scanner's report-only behavior.

| Audit ID | Closing contract clause |
|---|---|
| CSC-004 | Phase 0 treats missing or invalid registry authority as material uncertainty, never an empty success. |
| CSC-005 | Phases 2b and 3 compare only typed, stable-identity, unit-compatible semantic claims. |
| CSC-006 | Phases 2c and 2d build explicit owner and directed dependency indexes. |
| CSC-007 | Phase 4 accepts only an immutable exact-revision incremental baseline. |
| CSC-008 | Phases 1 and 2 freeze the manifest and enforce visible file, byte, claim, and comparison budgets. |
| CSC-009 | Phase 4 assigns stable finding identity, revisions, status, and resolution evidence. |
| CSC-010 | Phase 5 applies ERROR/PARTIAL precedence and reports every coverage gap. |
| CSC-011 | Phase 6 returns canonical report bytes in conversation and explicitly performs no save-path write. |
