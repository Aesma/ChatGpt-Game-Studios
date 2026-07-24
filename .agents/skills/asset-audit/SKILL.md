---
name: asset-audit
description: "Read-only, bounded asset compliance, provenance, license, and reference-integrity audit using registered versioned adapters and hash-bound evidence."
---

# Asset Audit

Analyzer contract: `cgs.asset-audit/v3`.
Evidence envelope: `cgs.review-evidence/v1` with extension
`cgs.asset-audit-report/v1`.

Audit one immutable target snapshot for asset-rule compliance, asset provenance,
license-policy status, reference integrity, and consumed production-eligibility
state. Every conclusion must come from an explicit rule and a registered,
versioned evidence adapter. Filename, extension, modification time, source-code
string search, visual inspection, role opinion, and file presence are advisory
only.

## Invocation and immutable read-only boundary

Invoke exactly:

```text
$asset-audit --manifest <project-relative-manifest-path>
$asset-audit --manifest <project-relative-manifest-path> --category <category>
```

Either form may end with `--summary`. The closed category enum is:

```text
art | audio | model | animation | vfx | shader | data | provenance | license | reference | all
```

The default category is `all`. `art`, `audio`, `model`, `animation`, `vfx`,
`shader`, and `data` select that asset family and all applicable compliance,
provenance, license, reference, and production channels for those assets.
`provenance`, `license`, and `reference` select that one channel across all
inventory assets, plus its inventory/rule/adapter prerequisites. `all` selects
every asset and channel. Category changes scope, while `--summary` changes
presentation only. Reject positional categories, unknown or duplicate flags,
missing values, unsupported category values, absolute paths, URLs, globs, regular
expressions, dot segments, path escapes, directories, symlinks, junctions, and
non-regular manifest files with `ERROR — INVALID INVOCATION`. Return the accepted
grammar, emit no verdict or evidence record, and stop.

This workflow is a strictly read-only analyzer:

- It may enumerate, hash, parse, and read declared project-local regular files,
  inspect read-only Git state, and execute only registered adapters inside a
  project-read-only sandbox.
- It must not create, edit, append, import, reimport, rename, move, delete,
  regenerate, compress, reserialize, stage, commit, publish, approve, or hand off
  any asset, source, import metadata, cache, manifest, report, or project state.
- It must not request mutation approval, offer a fix/report-writing branch,
  invoke a director gate, invoke another skill, delegate remediation, or execute
  a recommendation.
- Adapter scratch output must be outside the project and is not project evidence
  until represented by a validated receipt. If an adapter cannot run with the
  project mounted read-only, do not run it.
- The only deliverable is one conversation packet. A separately invoked recorder
  may persist the exact returned bytes, but this analyzer never selects a path or
  performs that write.

Every non-error result states:

```text
allowed_project_write_set: []
report_persisted: false
recorder_invoked: false
mutation_authorized: false
```

Verdict is exactly
`COMPLIANT | WARNINGS | NON-COMPLIANT | PARTIAL`. `ERROR` is an execution result,
not a fifth verdict. Any execution error emits no verdict or review-evidence
record. A post-lock diagnostic may include the locked manifest and exact failure
as non-evidence context, then must stop.

---

## Load the private evidence contract

Read [evidence-contracts-v1.md](references/evidence-contracts-v1.md) completely.
It fixes the closed invocation/categories, immutable scope, hard limits, rule
precedence, adapter receipts, engine-specific reference syntax/normalization,
stable findings, deterministic aggregation, failure handling, and persistence
boundary.

Read [continued-workflow.md](references/continued-workflow.md) completely and
execute its phases in order. If either reference is missing, unreadable, or
internally inconsistent with this SKILL, return `ERROR — CONTRACT INVALID`, emit
no verdict/evidence envelope, perform no adapter execution, and stop.

---

## Phase 0 — Resolve instructions, project identity, and one target

Read every applicable `AGENTS.md` from repository root through the audit manifest
and each declared asset/rule directory, in root-to-target order. Record the exact
path and raw-byte SHA-256 of each instruction; the nearest applicable instruction
wins when instruction rules conflict.

Represent `project_id` as the exact string
`root=<forward-slash-canonical-root>;git-root=<root-commit-or-null>` and compute
`project_id_sha256` over its UTF-8 bytes. If Git is unavailable, use `null`,
continue from exact current file hashes, mark project-revision provenance coverage
incomplete, and prevent `COMPLIANT`; never guess a commit.

The manifest must be a project-local regular file no larger than 1 MiB and use
schema `cgs.asset-audit-manifest/v1`. It must bind:

- one stable audit target ID, build ID, build-artifact hash, engine ID/version,
  platform, and configuration;
- one exact asset-inventory path/hash plus a versioned inventory-completeness
  receipt that names declared roots, exclusions, generator adapter/version,
  complete candidate identity digest, and output inventory digest;
- one exact adapter-registry path/hash and one exact engine resolver-registry
  path/hash;
- one exact build/dependency manifest path/hash when reference checks apply;
- the ordered applicable rule-source declarations, including technical
  preferences, art direction, and provenance/license policy when applicable;
- provenance and license record manifests with exact hashes when selected or
  implied by the category;
- asset-manifest/asset-spec production-state inputs when selected or implied and
  production eligibility is applicable;
- every applicable instruction path/hash, declared category, and generated-at
  timestamp; and
- optional lower execution limits. A manifest may lower but never raise the fixed
  Phase 1 limits.

Resolve literal and real paths without following symlinks. Reject a duplicate
normalized asset ID/path, real-path escape, unsupported manifest schema or
encoding, duplicate mapping key, mismatched declared hash, or ambiguous target as
`ERROR — INVALID AUDIT MANIFEST` before any adapter runs. Never infer the newest
inventory, current editor platform, current build, engine, rule set, adapter,
resolver, license policy, or report.

---

## Phase 1 — Lock a bounded exact-hash manifest and coverage plan

Build the complete candidate identity sequence from the explicit manifest,
inventory, rule sources, registries, declared asset roots, provenance/license
records, dependency graph, and production-state manifests. Do not recursively
discover undeclared roots. Hash exact raw bytes with SHA-256 before parsing;
normalized text, Git status, modification time, and import-cache time are never
hash inputs or currentness evidence.

Use these fixed upper bounds:

```yaml
max_manifest_candidates: 20000
max_selected_assets: 10000
max_total_selected_asset_bytes: 4294967296
max_rule_records: 8192
max_adapter_receipts: 100000
max_reference_edges: 200000
max_provenance_records: 20000
max_license_records: 20000
max_single_receipt_bytes: 1048576
max_output_findings: 10000
max_adapter_wall_ms: 30000
max_total_adapter_wall_ms: 600000
```

Sort candidate identities by channel, stable asset/artifact ID or null, then
canonical project-relative path. Stream the complete ordered identity sequence
into `inventory_sha256`, but retain at most `max_manifest_candidates` detailed
rows. On overflow, record exact total and omitted counts, the first and last
omitted sort keys, and `omitted_candidates_sha256` over the omitted canonical
identity sequence. Apply the same bounded-prefix plus count/digest rule to every
row limit. Do not read or judge an over-limit item. Add an aggregate `OVER_LIMIT`
coverage row naming every affected check and force `PARTIAL`. Never raise a cap,
silently omit input, or infer complete coverage from a sample.

Each detailed manifest row contains:

```yaml
channel: instruction | inventory | asset | import | rule | adapter | resolver | build | provenance | license | production
artifact_id: <stable ID or null>
asset_id: <stable asset ID or null>
path: <canonical project-relative path>
sha256: <locked 64-lowercase-hex or null>
revalidation_sha256: <final 64-lowercase-hex or null>
bytes: <non-negative integer or null>
status: LOCKED | EXCLUDED | MISSING | UNREADABLE | INVALID | UNSUPPORTED | LFS_POINTER | OVER_LIMIT | SYMLINK_REJECTED | OUTSIDE_PROJECT | STALE
reason: <bounded exact reason>
planned_checks: [<stable check IDs>]
```

`manifest_sha256` is SHA-256 over canonical JSON of project identity, invocation,
contract, target/build/platform, fixed and lowered limits, ordered retained rows,
complete inventory digest, and overflow counts/digests. Canonical JSON uses
UTF-8, lexicographically ordered object keys, displayed array order, no
insignificant whitespace, and exactly one final LF.

Re-enumerate declared roots and re-hash every locked project input immediately
before finalization. An added, removed, renamed, or byte-changed input is
`STALE`; discard conclusions derived from the stale bytes, keep unaffected
evidence, mark affected checks incomplete, and return `PARTIAL`. Never mix
snapshots or silently restart against another target.

---

## Phase 2 — Resolve rules with deterministic source precedence

Rules are data, not prose invented by this analyzer. Load and report the actual
effective chain in this order:

1. applicable root-to-target `AGENTS.md` instructions establish governance and
   explicit asset constraints; the closest applicable instruction wins the same
   rule key;
2. technical-preferences/pipeline sources provide format, import, platform,
   performance-budget, and schema rules not explicitly overridden by an
   applicable instruction;
3. art-bible/art-direction sources provide visual, material, palette, animation,
   and presentation rules not explicitly overridden by an applicable instruction;
4. approved provenance/license policy provides origin, permitted-use,
   attribution, redistribution, derivative, territory, platform, and expiration
   rules not explicitly overridden by an applicable instruction; and
5. manifest fallback rules are accepted only when explicitly marked advisory and
   never override an authoritative source.

Rules from different domains coexist. One domain cannot silently relax or
override another. If two current authoritative domains make incompatible demands
for the same asset/check and no applicable instruction resolves them, emit
`RULE_CONFLICT`, make that check `UNVERIFIED`, and force `PARTIAL`. Art direction
cannot relax technical safety or license obligations. Role consultation, memory,
prior reports, and default industry practice are not rule sources.

Normalize every rule to:

```yaml
rule_id: <stable globally unique ID>
domain: GOVERNANCE | TECHNICAL | ART | PROVENANCE | LICENSE | REFERENCE | PRODUCTION
source:
  artifact_id: <stable source ID>
  path: <canonical path>
  locator: <stable rule ID/anchor>
  sha256: <exact raw-byte hash>
  schema_version: <version or null>
authority: GOVERNING | AUTHORITATIVE | ADVISORY
applicable_asset_types: [<stable type IDs>]
target_platform_configuration: <exact scope>
expected_value_or_schema: <typed bounded value/reference>
operator: <registered exact operator ID>
adapter_requirement:
  adapter_class: <stable class ID>
  minimum_version: <exact version constraint>
severity: HARD | ADVISORY
not_applicable_condition: <typed predicate or null>
remediation_owner: <stable owner/role ID>
```

A duplicate rule ID with different meaning, missing stable ID, unknown operator,
unreadable/stale source, ambiguous precedence, missing required source, or
required rule without a compatible adapter makes rule coverage incomplete and
forces `PARTIAL`. Identical duplicate rules may be deduplicated only while
preserving all provenance.

---

## Phase 3 — Validate registered adapter and receipt contracts

The adapter registry is authoritative only about supported evidence extraction;
it cannot create rules or product approval. Each entry must bind:

- stable adapter class, adapter ID, semantic version, executable/tool identity,
  executable hash, and supported engine/platform/configuration range;
- supported MIME/container signatures, structured schemas, reference syntaxes,
  provenance/license record schemas, and rule operators;
- an argv array with typed placeholders, no shell command string, no network,
  project-read-only mount, separate bounded scratch root, timeout, and output cap;
- an explicit guarantee that it does not import, serialize, generate caches, or
  write project files;
- structured receipt schema/parser version, exit/result semantics, deterministic
  normalization, and cleanup contract.

Required adapter classes include, when their asset/rule channel is in scope:

- image/texture metadata: signature/container, dimensions, channels/alpha, color
  space, compression, mip and import metadata;
- audio metadata: container/codec, sample rate, channels, bit depth, duration,
  streaming and mix metadata;
- model/animation metadata: mesh, material, bone, animation, unit, scale, and
  embedded-dependency records;
- VFX/resource metadata: engine-native structured resources, budgets,
  dependencies, and scalability fields;
- shader/material evidence: engine-compatible parser or pre-existing compiler
  receipt for exact target variants without cache mutation;
- data validation: exact JSON/YAML/binary parser plus rule-declared schema
  path/hash/version;
- provenance validation: exact asset/origin/derivation/acquisition record parser;
- license-policy evaluation: recognized license expression/approved policy ID,
  license text/receipt hashes, obligation scope, and policy decision receipt;
- engine reference resolution: exact engine/version resolver for every declared
  resource and dynamic-reference mechanism; and
- any additional in-scope type: one manifest-declared compatible adapter.

Never infer metadata from extension, synthesize a parser, use a shell string,
fall back to visual/manual judgment, or let an adapter discover new scope. Verify
project inputs are unchanged before and after each run. If OS-level project
read-only isolation is unavailable or an adapter would trigger import,
serialization, cache generation, network access, or project writes, do not run it
and mark `NOT_RUN`.

A valid `cgs.asset-adapter-receipt/v1` binds exact asset/rule/target/build IDs,
asset/import/rule hashes, adapter ID/version/executable hash, argv digest,
sandbox policy, start/end timestamps, exit state, structured output digest,
bounded stdout/stderr digests, and parser version. States are:

```text
PASS | FAIL | NOT_RUN | UNSUPPORTED | PARSE_ERROR | TIMEOUT | INVALID_RECEIPT
```

`PASS` is permitted only when current machine-verifiable evidence proves the
exact rule for the exact bytes and target. `FAIL` is conclusive only when a valid
receipt executed and proved the rule violation. Missing executable/adapter/schema,
unsupported type/version/syntax, LFS pointer, permission failure, timeout,
malformed/truncated output, signature mismatch, parse error, invalid receipt, or
mutation risk yields `UNVERIFIED`, incomplete adapter coverage, and prevents
`COMPLIANT`; it is never silently converted to `FAIL` or `PASS`.

---

## Phase 4 — Index assets and evaluate each applicable rule once

Build the asset, import, rule, adapter, provenance, license, and reference indexes
once. Do not recursively rescan the repository or search source code separately
for each asset. Every inventory row must provide:

```yaml
asset_id: <globally unique stable ID>
path: <canonical project-relative path>
sha256: <exact raw-byte hash>
bytes: <integer>
detected_signature: <MIME/container ID from registered detector>
declared_type: <stable type ID>
category: <closed invocation category>
target_id: <exact stable target ID>
import_metadata: <path/hash or ABSENT>
lfs_state: MATERIALIZED | POINTER | NOT_APPLICABLE
provenance_record_id: <stable ID>
license_record_id: <stable ID or explicit policy-defined NOT_APPLICABLE>
```

An inventory completeness receipt must prove all declared roots/exclusions were
enumerated by a registered inventory adapter. Missing or invalid completeness
evidence makes inventory coverage incomplete even when every listed file passes.
An empty inventory can be complete only when that receipt proves the bounded
scope contains zero applicable assets.

For each selected asset/rule pair, verify hashes, signature, type, target,
applicability, adapter compatibility, and receipt; then compare typed expected and
actual values with the registered operator. The per-check result is exactly
`PASS | FAIL | UNVERIFIED | NOT_APPLICABLE`. `NOT_APPLICABLE` requires the
rule-declared predicate and current evidence, not absence of an adapter.

Modification time may be displayed as non-authoritative context only. Asset
hashes, stable IDs, rule hashes, target/build identity, adapter receipts, and
manifest revision determine reproducibility.

---

## Phase 5 — Verify provenance and license-policy evidence

Asset provenance and license-policy compliance belong to asset-audit. They do
not prove that a GDD requirement shipped and they are not legal advice. Use only
frozen project records and approved policy receipts; do not browse, infer rights
from a filename/source URL, or make a new legal determination.

Normalize every provenance record under `cgs.asset-provenance/v1`:

```yaml
provenance_record_id: <stable ID>
asset_id: <exact stable asset ID>
asset_sha256: <exact asset hash>
origin_kind: INTERNAL_ORIGINAL | COMMISSIONED | THIRD_PARTY | GENERATED | DERIVED
creator_or_provider_id: <stable party/provider ID>
acquisition_or_creation_receipt: <artifact ID/path/hash/locator>
source_locator: <bounded URI or source reference recorded as data>
parent_asset_ids: [<sorted stable IDs>]
generator_or_tool: <stable ID/version or null>
record_source: <artifact ID/path/hash/schema>
```

Derived assets require a cycle-free, exact parent chain to provenance-covered
assets. Generated assets require the policy-declared generator/model/tool and
creation receipt fields. A missing, stale, mismatched, cyclic, unsupported, or
conflicting record yields `PROVENANCE_UNVERIFIED` or `PROVENANCE_CONFLICT`, makes
provenance coverage incomplete, and forces `PARTIAL` unless separate current hard
evidence already proves `NON-COMPLIANT`.

Normalize every license record under `cgs.asset-license/v1`:

```yaml
license_record_id: <stable ID>
asset_id: <exact stable asset ID>
asset_sha256: <exact asset hash>
license_expression_or_policy_id: <recognized exact ID>
license_text_or_receipt: <artifact ID/path/hash/locator>
permitted_targets: [<stable target/platform IDs>]
territory: <policy-defined scope>
effective_and_expiration: <exact dates or policy-defined perpetual>
derivative_and_redistribution_rights: <typed policy values>
attribution_obligations: [<stable obligation IDs>]
obligation_evidence: [<artifact ID/path/hash/locator>]
policy_source: <artifact ID/path/hash/rule ID/schema>
```

The registered policy adapter may return exactly:

```text
ALLOWED | ALLOWED_WITH_OBLIGATIONS | PROHIBITED | EXPIRED | UNVERIFIED | NOT_APPLICABLE
```

`ALLOWED_WITH_OBLIGATIONS` passes only when every required obligation has current
exact-hash evidence for the audited target. `NOT_APPLICABLE` requires an explicit
policy rule. `PROHIBITED`, `EXPIRED`, or a conclusively unmet HARD obligation is a
HARD `FAIL`. Missing policy, record, recognized expression, scope, receipt,
attribution evidence, or adapter yields `UNVERIFIED` and `PARTIAL`, never an
assumed license. Conflicting current records are `LICENSE_CONFLICT`, remain
visible, and force `PARTIAL`; never choose the newest or most permissive record.

---

## Phase 6 — Build an engine-aware reference graph

Use only the exact registered engine resolver, its
`cgs.asset-reference-graph/v1` receipt, and current build/dependency manifests.
The receipt must bind engine/resolver versions, target/build/artifact IDs and
hashes, inventory and dependency-manifest hashes, supported reference syntaxes,
dynamic-registry coverage, normalized asset IDs, every parsed reference location,
complete edge digest/count, parser/tool versions, timestamp, result, and complete
log digest.

Resolver coverage must explicitly enumerate every applicable mechanism declared
for the target: scenes, prefabs, resources, engine UIDs, addressables, asset
bundles, import remaps, serialized IDs, data/config references, runtime registries,
declared dynamic-loading roots, package/pak catalogs, and equivalent engine-native
links. Unknown engines, versions, syntaxes, dynamic roots, or packed formats are
`UNSUPPORTED`, make reference coverage incomplete, and force `PARTIAL`.

Classify each selected asset/reference exactly once:

- `REFERENCED`: a current complete receipt proves at least one valid inbound or
  inclusion edge for the normalized asset ID.
- `UNREFERENCED_CONFIRMED`: complete current resolver/build coverage includes
  every declared mechanism and proves no inbound, allowed dynamic, or build edge.
- `POSSIBLY_ORPHANED`: no verified edge was found but any resolver, dynamic, or
  build coverage is incomplete.
- `MISSING_CONFIRMED`: a supported syntax was parsed at an exact source location
  to a normalized asset ID and current inventory/build evidence proves that ID
  absent.
- `UNKNOWN`: the resolver/evidence is unavailable, unsupported, stale,
  conflicting, invalid, or cannot normalize identity.

A source-code text search may appear only as bounded advisory observation.
String absence never produces `UNREFERENCED_CONFIRMED`; string presence never
proves an engine edge or target inclusion. Unsupported syntax never produces
`MISSING_CONFIRMED`. `POSSIBLY_ORPHANED` or `UNKNOWN` makes reference coverage
incomplete and forces `PARTIAL`.

`MISSING_CONFIRMED` is a conclusive HARD reference-integrity failure.
`UNREFERENCED_CONFIRMED` becomes a failure only when an exact applicable policy
rule classifies it HARD or ADVISORY. Never recommend automatic deletion. Even a
confirmed unused candidate requires separate human review, version-control and
build-graph checks, and separately authorized removal.

---

## Phase 7 — Consume production state and enforce ownership boundaries

When production eligibility is in scope, consume exact hash-bound asset-manifest
and asset-spec state without changing it. Recognized states are:

```text
DRAFT | BLOCKED_NOT_FOR_PRODUCTION | READY_FOR_PRODUCTION
```

`READY_FOR_PRODUCTION` is accepted only when stable asset/spec IDs,
transactions, statuses, dependency state, committed raw hashes, and current
validation receipts agree; `production_eligible` is true; every inferred
requirement is confirmed; and no blocker remains. `DRAFT` is a HARD failure for
a production target. `BLOCKED_NOT_FOR_PRODUCTION` is a HARD failure and cannot be
upgraded by local adapter PASS, user risk acceptance, or this analyzer. Missing,
mismatched, stale, malformed, or unverifiable external state is `UNKNOWN`, makes
that coverage channel incomplete, and forces `PARTIAL` absent another conclusive
HARD failure.

Asset-audit owns:

- naming, format, size, import, platform, and pipeline-rule compliance;
- binary/structured metadata validation;
- provenance and approved license-policy evidence;
- engine reference integrity and confirmed broken/maybe-orphan classifications;
- consumed production-eligibility state.

Content-audit alone owns comparison of stable GDD requirement IDs with target
build-inclusion evidence. Asset-audit must not decide whether every required
piece of content shipped, invent missing requirements, interpret file counts as
implementation, or emit `SHIPPED_VERIFIED`. Content inclusion does not prove
asset compliance, and asset compliance/reference/provenance/license PASS does not
prove content inclusion or requirement coverage.

A content-audit consumer may accept a current asset-audit record only by
recomputing the `cgs.review-evidence/v1` envelope, recognized producer/extension,
target/build/manifest identity, and every artifact/payload hash. It may display
that evidence under the asset-audit owner, but it must not use it as inclusion
proof. This analyzer does not invoke content-audit.

---

## Phase 8 — Normalize stable findings and coverage

Every actionable or coverage finding uses:

```yaml
id: AAF-<category-slug>-<first-12-fingerprint-hex>
fingerprint_sha256: <64-lowercase-hex>
category: RULE_FAIL | RULE_CONFLICT | ADAPTER_GAP | INVENTORY_GAP | PROVENANCE_GAP | LICENSE_FAIL | LICENSE_CONFLICT | REFERENCE_FAIL | REFERENCE_GAP | PRODUCTION_BLOCKER | COVERAGE_GAP
asset_id: <stable asset ID or null>
rule_id: <stable rule ID or null>
target_id: <stable target ID>
severity: HARD | ADVISORY | COVERAGE
check_result: PASS | FAIL | UNVERIFIED | NOT_APPLICABLE
evidence: [<complete exact-hash references and receipt digests>]
owner: <stable remediation owner>
status: OPEN | RESOLVED_IN_CURRENT
acceptance: <objective current-snapshot closure condition>
```

Fingerprint canonical JSON from `project_id_sha256`, category, stable
asset/rule/target IDs, stable provenance/license/reference/production record IDs,
and applicable platform/configuration. Exclude paths, display names, raw wording,
line numbers, content hashes, expected/actual values, severity, confidence,
status, run ID, timestamps, and recommendation so the same logical defect keeps
its ID after movement or byte changes. Deduplicate only the full fingerprint and
preserve all provenance. Incompatible evidence sharing a fingerprint is a
coverage conflict and forces `PARTIAL`.

Build one row for every candidate, selected asset/rule pair, provenance/license
record, reference mechanism, production-state input, and required check:

```yaml
channel_id: <stable channel/check ID>
artifact_or_asset_id: <stable ID or null>
path: <canonical path or null>
sha256: <hash or null>
bytes: <integer or null>
status: COMPLETE | PARTIAL | FAILED | NOT_APPLICABLE
checks:
  SNAPSHOT: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  INVENTORY: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  RULES: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  ADAPTERS: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  PROVENANCE: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  LICENSE: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  REFERENCES: DONE | PARTIAL | FAILED | NOT_APPLICABLE
  PRODUCTION: DONE | PARTIAL | FAILED | NOT_APPLICABLE
limitation: <none or exact bounded reason>
```

Required coverage dimensions are project snapshot, inventory, rules, adapters,
platform/configuration, and each channel selected directly or implied by `all`.
Reference, provenance, license, and production checks may be `NOT_APPLICABLE`
only from an explicit authoritative rule/manifest predicate. Missing inputs never
mean `NOT_APPLICABLE`.

---

## Phase 9 — Apply the deterministic verdict and return evidence

Apply this exhaustive first-match order:

1. Invalid invocation/manifest/target/snapshot, actual project mutation, no
   trustworthy inventory, failure before manifest lock, or inability to build a
   trustworthy packet: `result: ERROR`; emit no verdict or evidence record.
2. Any current conclusive HARD `FAIL`, `MISSING_CONFIRMED`, policy-HARD
   `UNREFERENCED_CONFIRMED`, `PROHIBITED`, `EXPIRED`, conclusively unmet HARD
   license obligation, production-target `DRAFT`, or
   `BLOCKED_NOT_FOR_PRODUCTION`: verdict `NON-COMPLIANT`.
3. Otherwise any incomplete/unavailable required coverage, `UNVERIFIED`,
   `NOT_RUN`, `UNSUPPORTED`, `PARSE_ERROR`, `TIMEOUT`, `INVALID_RECEIPT`,
   `POSSIBLY_ORPHANED`, `UNKNOWN`, stale input, overflow, unresolved rule/license
   conflict, or missing required adapter/schema/resolver/provenance/license state:
   verdict `PARTIAL`.
4. Otherwise one or more conclusive ADVISORY `FAIL` findings: verdict `WARNINGS`.
5. Otherwise every applicable required rule is current `PASS` or valid
   `NOT_APPLICABLE`, every required coverage dimension is complete, production
   eligibility is verified where applicable, and no contradiction/blocker
   remains: verdict `COMPLIANT`.

Known hard failures take precedence over incomplete coverage, but the report must
preserve every coverage gap and state that the audit is not exhaustive.
`COMPLIANT` is impossible from a partial inventory, scoped sample, empty search,
unsupported type/syntax, missing adapter/schema/resolver, stale receipt,
unverified provenance/license, or unknown production state.

Return one extension payload:

```yaml
schema: cgs.asset-audit-report/v1
contract: cgs.asset-audit/v3
result: OK
verdict: COMPLIANT | WARNINGS | NON-COMPLIANT | PARTIAL
project_id: <canonical project identity>
project_id_sha256: <hash>
run_id: <lowercase UUID>
observed_at: <UTC ISO-8601>
invocation:
  manifest_path: <canonical project-relative path>
  category: <closed enum value>
  summary: true | false
target: <stable target/build/platform/configuration IDs and artifact hash>
manifest:
  sha256: <manifest hash>
  inventory_sha256: <complete candidate identity-sequence hash>
  limits: <fixed and effective limits>
  overflow: <exact counts, boundary keys, and omitted-sequence digests>
  rows: [<ordered detailed rows>]
rule_precedence: <loaded, effective, overridden, and conflicting exact-hash rules>
coverage:
  dimensions: <status/reason per required dimension>
  ledger: [<ordered rows>]
checks: [<ordered per-asset/per-rule results>]
provenance: <ordered records/states/limitations>
licenses: <ordered records/policy states/obligations/limitations>
references:
  referenced_ids: []
  unreferenced_confirmed_ids: []
  possibly_orphaned_ids: []
  missing_confirmed_ids: []
  unknown_ids: []
production_eligibility: <ordered stable-ID state sets>
findings: [<ordered stable findings>]
advisory_observations: []
limitations: []
recommendation: <one owner-specific action or none>
disclaimer: <required boundary text>
```

Sort checks by asset ID then rule ID; sort provenance/license rows by asset ID
then record ID; sort reference ID sets lexicographically; sort findings by
category, asset/rule ID, then fingerprint. Bound excerpts and advisory text.
`--summary` may compact checks/findings in the human projection only; the machine
payload retains the same target, manifest, rule precedence, all coverage fields,
state sets, stable finding IDs, limitations, verdict, and hashes.

Hash canonical extension JSON using Phase 1 canonicalization, then wrap it in:

```yaml
schema: cgs.review-evidence/v1
record_id: sha256:<SHA-256 of canonical envelope payload excluding record_id>
artifact_id: asset-audit:<project_id_sha256>:<target_id>:<manifest_sha256>
artifacts: [<every retained locked input path and SHA-256, sorted as manifest>]
reviewer: <stable task identity or codex-task:<run_id>>
review_run_id: <run_id>
review_depth: bounded-full
independence: analyzer-read-only
verdict: <asset-audit verdict>
timestamp: <observed_at>
finding_ids: [<sorted stable finding IDs>]
unresolved_blocker_ids: [<sorted open HARD/coverage finding IDs>]
report_payload_sha256: <SHA-256 of canonical extension payload>
producer:
  tool: asset-audit
  version: cgs.asset-audit/v3
extension: <complete cgs.asset-audit-report/v1 payload>
```

Recompute every artifact, manifest, payload, and envelope hash once. Fail with
`ERROR — EVIDENCE CONSTRUCTION FAILED` and emit no evidence record rather than
returning inconsistent hashes. The record applies only to its exact target,
build, platform/configuration, rule chain, registries, inventory, asset bytes,
and manifest hashes. Conversation rendering does not persist it automatically;
later consumers must receive exact bytes and revalidate all hashes.

The disclaimer must state: `PARTIAL`/`UNVERIFIED` is not compliance;
`COMPLIANT` is not proof of GDD content completeness or build inclusion beyond
the exact reference evidence; license-policy results are evidence under the named
policy and not legal advice; no deletion, import, production handoff, or other
mutation was authorized.

---

## Phase 10 — Return one owner-routed recommendation and stop

Return at most one recommendation from the highest-impact open evidence:

- format/import/technical rule: named technical-art, audio, engine, or pipeline
  owner from the rule;
- art-direction rule: art owner from the rule;
- provenance/license gap or failure: named asset-rights/license-policy owner or
  user decision owner, without making a new legal conclusion;
- broken/unknown engine reference: resolver, integration, or owning asset-system
  owner;
- production-state blocker: asset-spec/production owner;
- missing GDD requirement or requirement-to-build inclusion question: identify
  content-audit as the separate owner, without invoking it;
- no finding with complete coverage: no follow-up required.

Never recommend deleting, renaming, moving, reimporting, relicensing, or replacing
an asset as an automatic action. State the evidence and owner only. Any mutation
requires a separate task, explicit target list, human/license review where
applicable, version-control/build-graph checks, and independent authorization.

Stop after returning the packet and recommendation. Never write a report, update
the catalog, call an owner, or change project state.
