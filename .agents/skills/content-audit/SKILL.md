---
name: content-audit
description: "Read-only, bounded comparison of stable content requirement IDs with hash-bound target-build inclusion evidence, explicit coverage, and fail-closed verdicts."
---

# Content Audit

Analyzer contract: `cgs.content-audit/v3`.
Evidence envelope: `cgs.review-evidence/v1` with extension
`cgs.content-audit-report/v1`.

Determine whether the content required by authoritative design sources is
included in one exact target build. Identity comes from stable IDs, inclusion
comes from a versioned manifest or registered engine adapter, and every claim is
bound to exact source bytes. File presence and aggregate counts are never proof
that content ships.

## Invocation and read-only boundary

Invoke exactly one of:

```text
$content-audit
$content-audit system:<stable-system-id>
$content-audit target:<stable-target-id>
$content-audit system:<stable-system-id> target:<stable-target-id>
```

Any valid form may end with `--summary`. Argument order otherwise does not
matter. A no-argument run audits every system in the authoritative content
inventory and resolves one target from the authoritative build configuration.
`system:` and `target:` values are exact stable IDs, not display names, aliases,
paths, globs, regular expressions, or URLs. Reject missing values, duplicates,
unknown flags, extra text, ambiguous IDs, multiple default targets, absolute or
outside-project paths, and symlink-selected inputs with
`ERROR — INVALID INVOCATION`. Show the accepted grammar, emit no evidence record,
and stop.

This workflow is a strictly read-only analyzer:

- It may enumerate, hash, parse, and read project-local regular files and inspect
  read-only Git state.
- It must not create, edit, append, rename, delete, stage, commit, publish, or
  approve any file or project state.
- It must not request write approval, offer a report-writing branch, invoke a
  director gate, invoke another skill, delegate remediation, or execute a
  recommendation.
- It returns one conversation-only packet. A separately invoked recorder may
  persist the exact returned bytes, but the analyzer never selects a destination
  or performs that write.

Use one frozen target snapshot throughout the run. Never combine facts from
different file hashes, target IDs, manifests, adapter versions, or build IDs.

Verdict contract is exactly
`COMPLETE | GAPS FOUND | MISSING CRITICAL CONTENT | PARTIAL`. `ERROR` is an
execution result, not a fifth verdict. Any execution error emits no verdict or
evidence record. When failure occurs after manifest lock, return the locked
manifest plus the exact diagnostic as non-evidence context, then stop; never
turn an untrustworthy partial execution into a review-evidence claim.

---

## Phase 0 — Resolve instructions, project identity, and scope

Read every applicable `AGENTS.md` from repository root through each in-scope
artifact directory, in root-to-target order, and record path plus exact SHA-256.
The nearest applicable instruction wins.

Represent `project_id` as the exact string
`root=<forward-slash-canonical-root>;git-root=<root-commit-or-null>` and compute
`project_id_sha256` over its UTF-8 bytes. If Git is unavailable, use `null`, keep
working from exact current file hashes, record Git provenance as unavailable,
and force `PARTIAL`; never guess a commit.

Resolve scope from explicit structured sources, in this order:

1. a versioned system/content inventory that provides stable system and
   requirement IDs;
2. explicit structured Content Inventory sections or tables in every in-scope
   GDD; and
3. bounded full reads of every remaining in-scope GDD to identify explicit
   stable-ID declarations and unidentified normative content statements.

Never select or exclude a GDD through a keyword, filename fragment, summary
section, regular-expression pre-scan, asset-folder match, or prior report. Read
each selected GDD in full once within the Phase 1 limits. If no authoritative
scope declaration exists, enumerate all project-local regular Markdown GDD
candidates under the declared GDD roots, preserve the discovery limitation, and
force `PARTIAL`. If no authoritative content requirement exists after those full
reads, record `NO_AUTHORITATIVE_REQUIREMENTS`, return `PARTIAL`, and do not infer
planned content from the implementation tree.

Resolve exactly one stable `target_id`, `build_id`, and manifest or registered
adapter path. A target selected explicitly must match authoritative target
metadata. A missing or ambiguous target is `ERROR — TARGET NOT RESOLVABLE` before
manifest lock; do not choose the newest build, current editor platform, filename,
or modification time.

---

## Phase 1 — Lock a bounded exact-hash input manifest

Build a deterministic candidate inventory before interpreting content. Include
all discovered requirement sources, system index and inventory artifacts,
target/build declarations, content/build manifests, adapter registry and schema,
adapter inputs, applicable instructions, dependency graph, and any explicitly
supplied external asset-audit evidence. Record excluded candidates too.

Accept only canonical project-relative paths to regular files. Do not follow
symlinks, junctions, aliases, nested repositories, URLs, generated report
directories, or paths that normalize outside the project root. Hash exact raw
bytes with SHA-256 before parsing; normalized text is never the hash input.

Use these fixed upper bounds:

```yaml
max_manifest_candidates: 512
max_semantically_read_requirement_sources: 64
max_single_requirement_source_bytes: 262144
max_total_requirement_source_bytes: 2097152
max_requirement_ids: 8192
max_inclusion_records: 32768
max_dependency_edges: 16384
max_external_asset_findings: 4096
max_advisory_observations: 1024
```

Sort canonical candidates by channel, stable artifact ID or null, then path.
Enumeration and streaming hashes do not consume semantic-read bytes. A source is
read in full or not semantically judged at all; never split or sample one file.
Stream the complete candidate identity sequence into `inventory_sha256`, but
retain at most `max_manifest_candidates` detailed rows. On candidate overflow,
record the exact total and omitted counts, the first and last omitted sort keys,
and `omitted_candidates_sha256` over the omitted canonical identity sequence.
Select semantic inputs only from the retained prefix, add one `OVER_LIMIT`
coverage row for the aggregate omitted channel, identify every affected check,
and force `PARTIAL`. For every other limit, retain the bounded detailed prefix
plus exact overflow count and digest. Never silently omit input, raise a limit,
or interpret a bounded subset as complete coverage.

Each manifest row contains:

```yaml
channel: instruction | requirement | scope | target | inclusion | adapter | dependency | external
artifact_id: <stable ID or null>
path: <canonical project-relative path>
  sha256: <locked 64-lowercase-hex or null>
  revalidation_sha256: <final 64-lowercase-hex or null>
bytes: <non-negative integer or null>
status: LOCKED | EXCLUDED | MISSING | UNREADABLE | INVALID | UNSUPPORTED | OVER_LIMIT | SYMLINK_REJECTED | OUTSIDE_PROJECT | STALE
reason: <bounded exact reason>
planned_checks: [<stable check IDs>]
```

`manifest_sha256` is SHA-256 over canonical JSON of the ordered retained rows,
inventory and overflow digests/counts, plus project, invocation, contract,
target, build, adapter, and limit values. Canonical JSON uses UTF-8,
lexicographically ordered object keys, displayed array order, no insignificant
whitespace, and one final LF.

Re-enumerate the declared candidate roots and re-hash every locked input before
finalizing. An added, removed, renamed, or changed input is `STALE`; discard any
semantic conclusion derived from the changed bytes, record affected checks as
incomplete, preserve unrelated current evidence, and return `PARTIAL`. Never mix
the old and new snapshots or silently restart against a different target.

---

## Phase 2 — Normalize authoritative requirement IDs

Read every selected requirement source in full exactly once. For every source,
record `READ | MISSING | UNREADABLE | INVALID | OVER_LIMIT | STALE`, its hash,
bytes, parser/schema version, contributed IDs, and affected checks.

Normalize each explicit auditable requirement to:

```yaml
requirement_id: <globally unique stable content requirement ID>
logical_content_id: <stable logical item ID>
system_id: <stable system ID>
content_type: <stable type ID>
display_name: <label only; never identity>
criticality: CRITICAL | ORDINARY
required_variant_policy:
  policy_id: <stable policy ID>
  required_variant_ids: [<sorted stable IDs>]
source:
  artifact_id: <stable artifact ID>
  path: <canonical path>
  locator: <stable requirement ID/anchor; bounded line span only as fallback>
  sha256: <exact raw-byte hash>
  schema_version: <version or null>
```

Stable identity must be explicit in an authoritative inventory, structured GDD
record, or an exact cross-reference to one. Never derive identity from a display
name, folder, filename, alias, fuzzy match, ordinal position, or aggregate count.
A duplicate `requirement_id` with identical canonical meaning is deduplicated
with all source provenance retained. The same ID with different logical content,
system, type, criticality, or variant policy is `IDENTITY_CONFLICT`, makes
requirement coverage incomplete, and forces `PARTIAL`; never choose one side.

A normative statement that requires N items but supplies no stable IDs is an
`UNIDENTIFIED_REQUIREMENTS` coverage record. Preserve the exact quantity, unit,
source locator, and hash. Do not invent IDs or names, pair it with N files, use it
in set completeness, or calculate a completion percentage.

Localized, difficulty, platform, accessibility, and cosmetic variants remain
under one logical requirement unless the authoritative policy assigns separate
requirement IDs. A required variant missing from inclusion evidence prevents the
logical item from being `SHIPPED_VERIFIED`; extra variants never inflate totals.

Requirement coverage is `INCOMPLETE` for any missing, unreadable, invalid,
over-limit, stale, unidentified, ambiguous, or conflicting requirement source
or ID. Preserve successfully normalized IDs and known facts.

---

## Phase 3 — Load manifest or registered engine-adapter evidence

Inclusion is proven only by either:

1. a current versioned content/build manifest that already conforms to
   `cgs.content-inclusion/v1`; or
2. a registered engine adapter whose exact version deterministically converts
   authoritative engine data into `cgs.content-inclusion/v1` records.

The adapter registry must bind `engine_id`, engine version range, adapter ID,
adapter version, supported source schema/resource database, and output schema.
Adapters may cover engine-native scenes, prefabs, resource databases,
Addressables, packed assets, package/pak manifests, or equivalent build catalogs.
The analyzer never guesses support from extensions. An unknown engine, version,
schema, resource kind, packed format, or adapter output is `UNSUPPORTED_ADAPTER`
or `UNSUPPORTED_FORMAT`, makes implementation coverage incomplete, and forces
`PARTIAL`.

Every valid inclusion record contains:

```yaml
requirement_id: <exact stable requirement ID>
logical_content_id: <exact stable logical item ID>
target_id: <exact stable target ID>
build_id: <exact stable build ID>
manifest_id: <stable manifest ID>
included: true | false
included_variant_ids: [<sorted stable IDs>]
source:
  artifact_id: <stable manifest or adapter-input ID>
  path: <canonical path>
  locator: <stable record key>
  sha256: <exact raw-byte hash>
adapter:
  id: <registered adapter ID or direct-manifest>
  version: <exact version>
  output_schema: cgs.content-inclusion/v1
```

Reject a record that has no exact target/build match, unknown schema, missing
provenance, mismatched requirement/logical ID, invalid boolean, or incomplete
required variants. Different authoritative records for the same target and ID
that disagree are `EVIDENCE_CONFLICT`; never pick the newest or majority result.

Classify every normalized requirement exactly once:

- `SHIPPED_VERIFIED`: current, valid, conflict-free evidence proves
  `included: true` and every required variant for the exact target/build.
- `MISSING`: current, valid, conflict-free evidence explicitly states
  `included: false` or explicitly proves a required variant absent.
- `PRESENT_UNVERIFIED`: an advisory project-local observation matches the exact
  ID, but valid target-build inclusion is not proven.
- `UNKNOWN_INCLUSION`: neither a current valid inclusion nor explicit exclusion
  record exists for the exact ID.
- `EVIDENCE_CONFLICT`: current authoritative records disagree or their identity,
  target, build, schema, adapter, provenance, or hashes cannot be reconciled.

Paths, filenames, source matches, directory or glob totals, editor objects,
test fixtures, import metadata, and file existence are advisory observations
only. They never establish `SHIPPED_VERIFIED`, reduce an unknown or missing set,
raise confidence, or permit `COMPLETE`. Editor-only and test-only content is
excluded unless the authoritative target manifest explicitly includes it.

Implementation coverage is `INCOMPLETE` when the manifest, adapter registry,
adapter input, or required record is missing, unreadable, invalid, stale,
unsupported, over limit, wrong-target, conflicting, or absent for any in-scope
requirement ID. Preserve verified and known-missing rows while failing closed.

---

## Phase 4 — Keep asset compliance under one owner

Format, naming, file-size, import settings, packaging policy, and pipeline
compliance belong exclusively to `asset-audit`. Content-audit must not read
technical preferences to recreate those checks, inspect raw assets for
compliance, or turn a format problem into build-inclusion evidence.

It may display a supplied asset-audit record only when all of these hold:

- the envelope is `cgs.review-evidence/v1` and its producer is `asset-audit`;
- the extension schema and producer version are recognized;
- every artifact and payload hash recomputes against the locked snapshot;
- its target/asset stable IDs resolve exactly; and
- the evidence is current for this target where target identity applies.

Classify accepted records as `EXTERNAL_ASSET_EVIDENCE` with owner and provenance.
Malformed, stale, wrong-target, or unverifiable external evidence is reported as
rejected external input and never changes content inclusion or core audit
coverage. No external asset-audit record is required to complete a content audit.
Point to the asset-audit owner when a supplied current finding needs follow-up;
never invoke it.

---

## Phase 5 — Compare stable sets and dependency impact

Compute set differences only by exact `requirement_id`:

```yaml
specified_ids: [<sorted IDs>]
shipped_verified_ids: [<sorted IDs>]
missing_ids: [<sorted IDs>]
present_unverified_ids: [<sorted IDs>]
unknown_inclusion_ids: [<sorted IDs>]
conflict_ids: [<sorted IDs>]
```

The sets are disjoint except that every implementation-state ID also appears in
`specified_ids`. Counts are projections of these explicit sets only. Never infer
a missing identity from a numeric delta, add unmatched assets to a verified set,
or calculate a completion percentage.

Priority and dependency impact may come only from authoritative stable data:

```yaml
dependency_id: <stable edge ID>
from_requirement_id: <exact stable dependent ID>
depends_on_requirement_id: <exact stable prerequisite ID>
kind: BUILD_BLOCKING | RUNTIME_BLOCKING | ORDERING | INFORMATIONAL
blocking: true | false
source:
  artifact_id: <stable graph artifact ID>
  path: <canonical path>
  locator: <stable edge key>
  sha256: <exact raw-byte hash>
  schema_version: <version>
```

Resolve both endpoints exactly against normalized requirement IDs. A duplicate,
unknown endpoint, cycle prohibited by the declared schema, malformed edge, or
unreadable/stale graph is a dependency-coverage gap and forces `PARTIAL` when
dependency impact is required. Preserve explicit criticality and blocking edges
as `priority_basis`; never infer urgency from systems-index prose, counts,
percentages, directory size, elapsed time, estimated effort, or reviewer opinion.
Dependency impact orders presentation only and cannot convert unverified content
into missing or shipped content.

Assign every finding a stable ID:

```yaml
id: CAU-<category-slug>-<first-12-fingerprint-hex>
fingerprint_sha256: <64-lowercase-hex>
category: MISSING_CONTENT | UNIDENTIFIED_REQUIREMENT | IDENTITY_CONFLICT | EVIDENCE_CONFLICT | COVERAGE_GAP | DEPENDENCY_GAP
requirement_id: <stable ID or null>
system_id: <stable ID or null>
target_id: <stable ID>
evidence: [<complete exact-hash references>]
status: OPEN | RESOLVED_IN_CURRENT
acceptance: <objective current-snapshot closure condition>
```

Fingerprint canonical JSON from `project_id_sha256`, category, stable
requirement/system/target IDs, stable source artifact IDs, and stable dependency
edge IDs. Exclude display labels, paths, raw wording, line numbers, source hashes,
severity/priority, status, timestamps, and run ID so the same logical issue keeps
its ID after movement or wording changes. Sort and deduplicate only by the full
fingerprint. Incompatible evidence under one fingerprint is an evidence conflict
and forces `PARTIAL`.

---

## Phase 6 — Build the coverage ledger and choose the verdict

Record one coverage row for every candidate, normalized requirement, inclusion
record, adapter channel, and required check:

```yaml
channel_id: <stable channel/check ID>
artifact_id: <stable ID or null>
path: <canonical path or null>
sha256: <hash or null>
bytes: <integer or null>
status: COMPLETE | PARTIAL | FAILED | NOT_APPLICABLE
checks:
  SCOPE: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  REQUIREMENT_IDENTITY: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  VARIANT_POLICY: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  TARGET_INCLUSION: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  DEPENDENCY_IMPACT: DONE | PARTIAL | FAILED | NOT_APPLICABLE
limitation: <none or exact bounded reason>
```

Required coverage dimensions are `scope`, `requirements`, `implementation`, and
`dependencies` when an authoritative graph declares dependency impact. External
asset compliance is a separate optional channel and never a required dimension.

Apply this precedence exactly:

1. Invalid invocation, unresolvable exact scope/target, no semantically readable
   requirement source, any execution failure, or inability to construct a
   trustworthy packet: `result: ERROR`; no completeness verdict or evidence
   record. A post-lock diagnostic may include the locked manifest only.
2. Any material coverage gap, stale source, overflow, symlink rejection,
   unsupported adapter/format, unidentified requirement, identity/evidence
   conflict, `PRESENT_UNVERIFIED`, or `UNKNOWN_INCLUSION`: verdict `PARTIAL`.
3. Complete coverage with one or more missing `CRITICAL` IDs: verdict
   `MISSING CRITICAL CONTENT`.
4. Complete coverage, no missing critical ID, and one or more missing `ORDINARY`
   IDs: verdict `GAPS FOUND`.
5. Complete coverage, every specified ID `SHIPPED_VERIFIED`, and no missing,
   unverified, unknown, conflict, unidentified, blocker, or unchecked item:
   verdict `COMPLETE`.

`PARTIAL` takes precedence over known gaps but must preserve `known_missing_ids`,
`known_missing_critical_ids`, and `known_gap_classification`. Explain that
`PARTIAL` means the audit is non-exhaustive, not that known gaps are harmless.
An empty requirement set never yields `COMPLETE`.

---

## Phase 7 — Return one hash-bound evidence packet

Return one machine-readable packet followed by a concise human projection.
`--summary` may compact rows in the human projection only; it must return the
same manifest, coverage dimensions, verdict, six ID sets, known gaps, finding
IDs, and hashes as the equivalent full run.

The extension payload uses this shape:

```yaml
schema: cgs.content-audit-report/v1
contract: cgs.content-audit/v3
result: OK
verdict: COMPLETE | GAPS FOUND | MISSING CRITICAL CONTENT | PARTIAL
project_id: <canonical project identity>
project_id_sha256: <hash>
run_id: <lowercase UUID>
observed_at: <UTC ISO-8601>
invocation:
  system_id: <stable ID or null>
  target_id: <stable ID>
  build_id: <stable ID>
  summary: true | false
manifest:
  sha256: <manifest hash>
  inventory_sha256: <complete candidate identity-sequence hash>
  limits: <all fixed limits>
  overflow: <exact counts, boundary sort keys, and omitted-sequence digests>
  rows: [<ordered manifest rows>]
coverage:
  dimensions: <status and reason per required dimension>
  ledger: [<ordered coverage rows>]
requirements: [<normalized exact-hash requirement records>]
implementation_rows: [<one classified row per requirement ID>]
sets:
  specified_ids: []
  shipped_verified_ids: []
  missing_ids: []
  present_unverified_ids: []
  unknown_inclusion_ids: []
  conflict_ids: []
known_missing_ids: []
known_missing_critical_ids: []
known_gap_classification: <MISSING CRITICAL CONTENT | GAPS FOUND | NONE>
dependency_ledger: []
findings: []
advisory_observations: []
external_asset_audit_evidence:
  accepted: []
  rejected: []
contradictions: []
recommendation: <one owned next action or none>
disclaimer: <required boundary text>
```

Sort requirements and implementation rows by `system_id`, `content_type`, then
`requirement_id`; sort every ID set lexicographically; sort findings by category,
stable system/requirement ID, then fingerprint. Bound excerpts and advisory text.

Hash the canonical extension payload exactly as displayed. The envelope fields
`record_id` and `report_payload_sha256` are outside that payload. Canonicalization
is UTF-8 canonical JSON as defined in Phase 1, with one final LF. Wrap it in:

```yaml
schema: cgs.review-evidence/v1
record_id: sha256:<SHA-256 of the canonical envelope payload excluding record_id>
artifact_id: content-audit:<project_id_sha256>:<target_id>:<manifest_sha256>
artifacts: [<every locked path and exact SHA-256, sorted as manifest>]
reviewer: <stable task identity or codex-task:<run_id>>
review_run_id: <run_id>
review_depth: bounded-full
independence: analyzer-read-only
verdict: <content-audit verdict>
timestamp: <observed_at>
finding_ids: [<sorted stable finding IDs>]
unresolved_blocker_ids: [<sorted open critical/coverage finding IDs>]
report_payload_sha256: <SHA-256 of canonical extension payload>
producer:
  tool: content-audit
  version: cgs.content-audit/v3
extension: <the complete cgs.content-audit-report/v1 payload>
```

Canonicalize the envelope without `record_id`, recompute all artifact,
manifest, report-payload, and record hashes once, and fail with
`ERROR — EVIDENCE CONSTRUCTION FAILED` rather than emitting inconsistent
evidence. The evidence is valid only for its exact target, build, adapter,
manifest, and artifact hashes.

The disclaimer must state: file presence is not proof of shipped content;
`PARTIAL` is not a completeness claim; format compliance remains owned by
asset-audit; and this analyzer changed no project state.

---

## Phase 8 — Return one owner-routed next action and stop

Return at most one recommendation selected mechanically from the highest-impact
open evidence, without invoking it:

- adequate specification plus verified missing implementation: production or
  backlog owner;
- missing, count-only, ambiguous, or conflicting specification: design owner;
- missing/unsupported manifest, build data, or engine adapter: manifest/build or
  engine-adapter owner;
- malformed stable dependency graph: graph-owning design/architecture owner;
- accepted current asset compliance finding: asset-audit owner;
- no gap with complete coverage: no follow-up required.

Missing implementation is not a design change. If specification repair may use
`quick-design`, recommend it only after a structural-risk screen proves the
change is local and does not alter shared contracts, schemas, save compatibility,
networking, economy, progression, cross-system dependencies, canonical
narrative, accessibility obligations, or release/platform commitments. Never use
gap count, percentage, size, or work-hour estimates. A quick-design output is a
proposal, not audit evidence, and closes nothing until a separate approved
application changes a canonical artifact and a new audit observes that exact new
hash.

Stop after returning the packet and recommendation. Never persist the packet,
modify a content or design artifact, update a catalog result, or invoke the next
owner.
