---
name: architecture-review
description: "Bounded, hash-bound, read-only architecture traceability gate over explicit approved requirements, ADR decisions, engine constraints, and current execution evidence; returns PASS, BLOCKED, or PARTIAL."
---

## Invocation and public contract

Invoke this workflow as `$architecture-review`.

Accepted grammar:

```text
$architecture-review [full | coverage | consistency | engine | rtm]
$architecture-review single-gdd [path:<canonical-project-relative-gdd> | id:<stable-system-id>]
```

No argument is `full`. A mode appears exactly once. `single-gdd` requires
exactly one `path:` or `id:` selector; other modes forbid selectors. Unknown,
duplicate, missing, fuzzy, title/name, or extra arguments return
`ERROR — INVALID INVOCATION`, emit no gate verdict, write nothing, and stop.

This skill is a formal, hash-bound gate. Its run verdict is exactly `PASS`,
`BLOCKED`, or `PARTIAL`. It does not grade `architecture.md` against an
eight-section template. It reviews explicit architecture requirements,
decisions, dependencies, compatibility, and traceability evidence.

The workflow is read-only by default. It may optionally create one new
immutable report at one exact user-authorized path after presenting the complete
report and changeset. It never modifies requirements, GDDs, ADRs,
`architecture.md`, registries, indexes, stories, tests, test results, logs,
systems status, sign-off, accepted-risk records, or session state. It never
uses or proposes `Needs Revision` as a systems-index lifecycle value.

Before analysis, read
[`references/review-rules-v1.md`](references/review-rules-v1.md) in full. Its
ruleset ID, authority model, mode matrix, limits, reviewer plan, evidence states,
finding schema, blocker matrix, and verdict precedence are normative.

## Frozen evidence contract

- **Explicit baseline only:** admit only stable requirement IDs backed by exact
  source text, current source hash/revision, lifecycle state, owner identity,
  approval status, and approval timestamp.
- **Exact trace links only:** prose similarity, implicit relationships, system
  names, filenames, or inferred intent are `UNVERIFIED_LINK`.
- **Execution truth only:** test-source discovery is not execution. Only a
  current authoritative `EXECUTED_PASS` record counts as passing evidence.
- **Bounded coverage:** every input, typed index record, comparison group,
  dependency edge, shard, check, and reviewer is planned and accounted. A limit
  overflow or unchecked required scope is `PARTIAL`, never hidden.
- **Single source ownership:** product rules, requirement lifecycle, decisions,
  derived views, implementation links, test runs, and engine references keep
  their separate owners. A derived artifact never overrules its source.
- **Machine identity:** every report binds a complete path/hash manifest,
  ruleset hash, skill-bundle hash, unique run ID, target manifest hash, stale
  key, coverage, stable findings, and reviewer results.
- **Risk separation:** `ACCEPTED_RISK` is a separate owner-signed record. It
  never changes an architecture-review verdict or finding disposition.

## Strict mode phase matrix

| Phase/input | `full` | `coverage` | `consistency` | `engine` | `single-gdd` | `rtm` |
|---|---|---|---|---|---|---|
| Approved requirement admission | REQUIRED | REQUIRED | FORBIDDEN | FORBIDDEN | REQUIRED for target | REQUIRED |
| Requirement → ADR coverage | REQUIRED | REQUIRED | FORBIDDEN | FORBIDDEN | REQUIRED for target | REQUIRED |
| Cross-ADR conflict/dependency checks | REQUIRED | FORBIDDEN | REQUIRED | FORBIDDEN | FORBIDDEN | FORBIDDEN |
| Pinned-engine compatibility | REQUIRED | FORBIDDEN | FORBIDDEN | REQUIRED | FORBIDDEN | FORBIDDEN |
| Story/test/test-run chain | REQUIRED when contract requires it | FORBIDDEN | FORBIDDEN | FORBIDDEN | FORBIDDEN | REQUIRED when contract requires it |
| Independent reviewers | TD + LP | NOT_APPLICABLE | TD | engine specialist | NOT_APPLICABLE | LP + QA |
| Optional immutable report | ALLOWED | ALLOWED | ALLOWED | ALLOWED | ALLOWED | ALLOWED |

`FORBIDDEN` means do not discover, read, delegate, compare, or emit
phase-specific findings. Record the phase as `NOT_APPLICABLE`; it is not a
coverage failure. A `single-gdd` run cannot expand to neighboring GDDs through
names or semantic similarity. A mode never silently promotes itself to `full`.

---

## Phase 0: Validate target, write boundary, and mutation guard

1. Parse the mode and selector using the strict grammar.
2. For `single-gdd path:`, require one normalized project-relative Markdown
   path resolving to a regular direct child of `design/gdd/`; reject absolute
   paths, traversal, external symlinks, directories, and non-GDD profiles.
3. For `single-gdd id:`, resolve the stable ID through the systems index. It
   must map to exactly one canonical GDD path. Zero, duplicate, collision, or
   path disagreement is `ERROR — AMBIGUOUS OR UNKNOWN GDD ID`, no verdict.
4. Establish the allowed write set before reading review inputs:
   - default: empty;
   - saved-report request: one exact new path after separate approval.
5. Build the mutation baseline as a streaming path/size/SHA-256 tree outside
   `.git` in ruleset-sized path batches. The snapshot is a guard, not review
   context; never paste the repository corpus into a prompt.

If the mutation baseline cannot cover the repository deterministically, record
`MUTATION_GUARD_INCOMPLETE` and the affected paths/batches. The run may continue
to preserve evidence but cannot `PASS`.

Immediately before the final response, repeat and compare the same streaming
snapshot. An actual unauthorized added, removed, or changed path is
`MUTATION_GUARD_FAILED`, a confirmed blocker. Name every path and do not revert
or normalize it. Failure to complete the final comparison without proof of a
mutation is incomplete evidence and produces `PARTIAL` when no blocker exists.

---

## Phase 1: Build a bounded target manifest and typed indexes

### 1a. Inventory only mode-permitted input classes

For every class in the mode matrix, create one ledger row:

```yaml
class: <GDD | systems-index | requirement-registry | ADR | architecture-derived | engine-reference | project-standard | story | test-source | test-run>
applicability: REQUIRED | OPTIONAL | NOT_APPLICABLE
presence: PRESENT | MISSING | NOT_APPLICABLE
currentness: CURRENT | STALE | UNREADABLE | UNKNOWN | NOT_APPLICABLE
paths: []
reason: <explicit contract evidence>
```

Absence never implies `NOT_APPLICABLE`. That state requires an explicit current
scope/requirement contract. Missing required input or unreadable intended input
prevents `PASS`. Record optional missing classes without expanding scope.

Mode inventories are exact:

- `coverage`: in-scope GDDs, explicit requirement lifecycle records, and ADRs
  that explicitly link admitted requirement IDs.
- `consistency`: current ADRs plus their explicit decision-domain, interface,
  resource-owner, and dependency records only.
- `engine`: current ADRs with explicit engine claims, pinned `VERSION.md`, and
  the directly applicable breaking-change, deprecated-API, and module-reference
  files.
- `single-gdd`: the exact selected GDD, the systems index when `id:` resolution
  is used, lifecycle records for IDs appearing verbatim in the GDD, and ADRs
  that explicitly name those IDs.
- `rtm`: coverage inputs plus stories, test sources, and test-run records linked
  by exact IDs where the approved requirement contract requires them.
- `full`: all classes required by coverage, consistency, and engine, plus the
  RTM classes explicitly required by admitted requirement contracts. A systems
  index may supply stable identity only when used and must then be hashed. A
  derived `architecture.md` or traceability index may be checked for drift when
  present but never becomes decision authority.

If a mode cannot establish any meaningful primary target—no reviewable GDD for
`coverage`/`single-gdd`/`rtm`, no current ADR for `consistency`/`engine`, or no
GDD and no ADR for `full`—return `ERROR — NO REVIEWABLE ARCHITECTURE SCOPE`, no
verdict, and stop. Other empty or missing classes follow the deterministic
input-state rules rather than fabricating a complete matrix.

### 1b. Build compact typed indexes before full reads

Hash each intended input's exact bytes, but first load only bounded declared
sections/fields needed to build indexes:

- requirement ID, source path/hash, lifecycle, owner, approval, criticality,
  layer, and required evidence kinds;
- ADR ID, lifecycle, explicitly addressed requirement IDs, decision domain,
  owned resource/interface keys, dependencies, engine claims, and supersession;
- story/test/run IDs and their explicit requirement/ADR/story links; and
- engine reference version/provenance and applicable API/module keys.

Do not infer Foundation/Core, criticality, a “required ADR,” ownership, or
applicability from prose. Unknown required metadata remains unknown and prevents
`PASS`.

Replace ADR all-pairs comparison with candidate groups. Normalize current ADRs
by explicit decision-domain, interface key, resource-owner key, dependency edge,
and engine API/module key. Compare only records sharing a key, and record the
group membership and checks. Run cycle detection over the explicit directed
dependency graph, not pairwise prose similarity.

### 1c. Plan bounded evidence shards

Sort artifacts by source type, stable ID, then canonical path. Sort comparison
groups by key type/key and dependency edges by source/target ADR ID. Fill
evidence shards greedily under all ruleset artifact, record, edge, and byte
limits. Full-read exact files only within the shard that checks them and verify
their hashes before and after review.

Every intended artifact, admitted/indexed record, candidate comparison group,
dependency edge, and applicable check must belong to at least one planned shard.
No worker receives the complete project unless the complete permitted scope
fits one bounded shard. A single oversized file, index overflow, unreadable
artifact, or uncompleted shard is named as unchecked coverage and forces
`PARTIAL` unless an independent confirmed blocker produces `BLOCKED`.

### 1d. Bind target and producer identity

The ordered target manifest contains, for every actual review input:

- canonical project-relative path and complete-file SHA-256;
- source type, stable source ID when present, input-class row, and role;
- source revision: repository commit, otherwise `WORKTREE`; and
- currentness and exact scope consumed.

Record the requested mode, exact target selector/resolution, every inclusion and
exclusion, input-class ledger, ruleset ID/hash, effective limits, planned shards,
and skill-bundle SHA-256 over the ordered main file, continuation, and ruleset
bytes.

`target_manifest_hash` is SHA-256 of the canonical ordered target manifest.
`stale_key` is SHA-256 of canonical JSON containing project ID, mode, exact
target identity, ruleset ID/hash, and the sorted complete path/hash input set.
`run_id` is
`AR-<UTC timestamp with fractional seconds>-<manifest12>-<UUIDv4>`. Generate the
UUID once when the manifest is frozen and preserve it unchanged. Timestamps and
the nonce never substitute for content identity.

---

## Phase 2: Admit only explicit approved requirements

Run only where the mode matrix says `REQUIRED`.

A requirement is admitted only when all are present and current:

1. stable requirement ID appears verbatim in the source GDD;
2. lifecycle record preserves immutable exact source text;
3. record names the source GDD path and exact source hash/revision in the
   manifest;
4. owner identity, explicit approval status, and approval timestamp exist;
5. lifecycle is active for this revision; and
6. criticality/layer and required downstream evidence are explicit when the
   verdict depends on them.

Use exact ID matching only. Prose that implies a possible architecture need but
fails admission is excluded from the baseline and becomes a
`CANDIDATE_REQUIREMENT` with exact evidence, missing fields, and destination
owner. Never allocate, reuse, normalize, or edit a TR ID.

Unapproved, inferred, ambiguous, source-drifted, or metadata-incomplete
requirements are `UNVERIFIED` and prevent `PASS`. Registry/source disagreement
is `REGISTRY_DRIFT`; the product GDD remains product-rule authority and the
reviewer does not reconcile either artifact.

---

## Phase 3: Verify exact traceability permitted by the mode

For each admitted requirement, ADR coverage is `VERIFIED_COVERED` only when a
current usable ADR explicitly names the exact requirement ID, the ADR hash is in
the manifest, its lifecycle is eligible, and its decision addresses the
requirement without exceeding or contradicting the approved product boundary.

Use exactly:

- `VERIFIED_COVERED` — exact current link and valid decision evidence;
- `VERIFIED_GAP` — admitted requirement has no exact usable ADR link; and
- `UNVERIFIED_LINK` — only similarity, implicit prose, filename/system mention,
  stale revision, ambiguous ID, or derived-index assertion exists.

Implicit coverage never increments verified coverage. A derived architecture or
traceability index may reveal `DERIVED_DRIFT`, but it never supplies a missing
source link.

Where RTM is mode-permitted, extend only by exact IDs:

- story must name the exact requirement ID and governing ADR ID;
- test source must name the exact requirement, ADR, or story IDs required by
  the approved contract; and
- the test-run record must bind that exact test source and current target.

Do not discover stories/tests in modes where RTM is forbidden.

---

## Phase 4: Verify actual test-run evidence

Run only in `full` or `rtm`, and only for requirements whose approved current
contract explicitly requires test evidence. Classify each exact test target:

- `EXECUTED_PASS` — authoritative latest run for the exact test hash and current
  source revision/manifest passed;
- `EXECUTED_FAIL` — authoritative matching current run failed;
- `STALE_RUN` — run targets another test hash, revision, manifest, or link set;
- `DISCOVERED_NOT_EXECUTED` — test source exists without a current run;
- `MISSING_EVIDENCE` — required test source or run is absent; or
- `NOT_APPLICABLE` — explicit approved contract says this evidence is not
  required.

An authoritative run contains immutable run ID, exact test path/hash, linked
IDs, result, execution timestamp, and reviewed revision or manifest hash. Only
`EXECUTED_PASS` is passing evidence. `EXECUTED_FAIL` is a confirmed blocker.
Stale, discovered-only, missing, ambiguous, or unreadable run evidence prevents
`PASS` and does not become execution proof through a file's existence.
“Latest authoritative” means the run selected by the evidence store's explicit
append-only sequence/index with a validated record hash. Never choose a test run
by filename date, directory order, or filesystem mtime.

---

## Phase 5: Run mode-specific decision checks and reviewers

### 5a. Deterministic checks

In `consistency` and `full`, evaluate only typed candidate groups and explicit
dependency edges for current ADR conflicts, competing resource/interface
ownership, incompatible budgets/contracts, missing or unusable dependencies,
cycles, and supersession errors.

In `engine` and `full`, validate explicit ADR engine claims only against the
pinned current VERSION and directly applicable reference hashes. Missing,
unreadable, stale, or out-of-scope engine references are unknown evidence and
prevent `PASS`; never substitute model memory or web recollection for the
pinned project evidence.

Apply the versioned blocker matrix. Imported severity, layer names guessed from
prose, or an unavailable source never establish a blocker. A confirmed current
conflict may produce `BLOCKED`; unknown identity, criticality, applicability, or
evidence produces `PARTIAL` when no blocker is independently proven.

### 5b. Profile-driven capped reviewers

Use exactly the reviewer plan in the mode matrix and ruleset, capped at two
reviewers for the run. Start required independent reviewers in parallel when
there are two. A reviewer receives only the relevant bounded shard(s), run ID,
target manifest hash, ruleset excerpt, check IDs, and exact input hashes. It is
read-only and cannot emit the gate verdict.

Every reviewer returns:

```yaml
schema: cgs.architecture-review-worker/v1
run_id: <run ID>
reviewer_role: <role>
status: DONE | DECLINED | TIMEOUT | ERROR
target_manifest_hash: <hash reviewed>
input_manifest: []
checks: []
unchecked_scope: []
findings: []
```

`DECLINED`, `TIMEOUT`, `ERROR`, wrong manifest/hash, missing required check, or
unchecked critical scope prevents `PASS` and produces `PARTIAL` when no
confirmed blocker exists. Normalize findings under the ruleset and deduplicate
identical fingerprints while retaining provenance. Incompatible facts,
severity, or evidence for the same fingerprint are `EVIDENCE_CONFLICT`, not a
majority vote, and produce `PARTIAL` unless a separate blocker is proven.

---

## Phase 6: Compute the deterministic verdict

Apply the ruleset precedence only after all applicable input classes, shards,
checks, links, runs, and reviewers have states:

1. `BLOCKED` when mutation guard actually fails or any confirmed current
   blocker satisfies every matrix precondition.
2. Otherwise `PARTIAL` when certification is incomplete: any missing/stale/
   unreadable required input, unverified/candidate requirement or link, unknown
   classification, budget overflow, unchecked shard, stale/missing run,
   required reviewer failure, or evidence conflict remains.
3. `PASS` only when the manifest is complete/current, every applicable check is
   done, exact traceability and required execution evidence pass, all reviewers
   are `DONE` on the same manifest, no blocker/incomplete evidence exists, and
   the final mutation guard passes.

Never infer a blocker merely to avoid `PARTIAL`. Never emit `PASS` with unknown,
implicit, missing, stale, over-budget, or unreviewed scope. Do not emit legacy
`APPROVED`, `NEEDS REVISION`, `MAJOR ISSUES`, `FAIL`, or advisory labels as the
gate verdict.

---

## Phase 7: Validate prior evidence and risk without rewriting it

A prior report is selected only by an exact project-relative path or exact
record ID. An ID may resolve through an explicit immutable review index only
when exactly one indexed path, record hash, project ID, mode, target identity,
and target manifest reproduce; otherwise return `ERROR — AMBIGUOUS REPORT
IDENTITY`. Never choose by filename date, directory order, mtime, or “latest.”

Rebuild the prior report's recorded scope and stale key. Any path, hash,
revision, required class, target selector, mode, ruleset hash, or scope change
makes it `STALE` and removes current gate value. Do not edit or relabel it.

A supplied `ACCEPTED_RISK` record is reported separately only when its record
hash, report/finding IDs, exact scope/manifest, owner/signature, timestamp, and
expiry validate. It never changes the review verdict, closes a finding, or
authorizes a write.

## Required continuation

Read [`references/continued-workflow.md`](references/continued-workflow.md) in
full. It defines the generic review-evidence envelope, architecture extension,
canonical record identity, optional immutable save, final mutation guard, and
single handoff. Follow it without expanding the write surface.
