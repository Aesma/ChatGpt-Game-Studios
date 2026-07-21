---
name: asset-audit
description: "Read-only, hash-bound asset compliance and reference audit using versioned executable adapters; unsupported or incomplete coverage can never be COMPLIANT."
---

# Asset Audit

This workflow audits one immutable asset snapshot. It never edits, imports, renames,
deletes, moves, regenerates, compresses, reserializes, or stages assets or import
metadata. It never invokes another project workflow or runs an engine/editor action
that can mutate the project.

## Invocation

Use exactly:

~~~text
$asset-audit --manifest <asset-audit-manifest-path> --run-id <id> [--category art|audio|vfx|shader|data|all] [--summary]
~~~

The manifest and run ID are mandatory. Default category is `all`. Reject positional
categories, unknown or duplicate flags, missing values, unsupported category values,
unsafe paths, directories, dot segments, and run IDs containing separators. Never
infer the latest asset manifest, current build, engine, rule set, adapter, or report.

This workflow is conversation-only and performs no project write. `--summary` changes
presentation only and cannot weaken evidence or coverage requirements.

## Status vocabulary

| Field | Allowed values |
|---|---|
| `Workflow Status` | `COMPLETE`, `PARTIAL`, `BLOCKED`, `ERROR` |
| `Coverage` | `COMPLETE`, `INCOMPLETE`, `UNAVAILABLE` |
| `Adapter State` | `PASS`, `FAIL`, `NOT_RUN`, `UNSUPPORTED`, `PARSE_ERROR`, `TIMEOUT`, `INVALID_RECEIPT` |
| `Check Result` | `PASS`, `FAIL`, `UNVERIFIED`, `NOT_APPLICABLE` |
| `Reference State` | `REFERENCED`, `UNREFERENCED_CONFIRMED`, `POSSIBLY_ORPHANED`, `MISSING_CONFIRMED`, `UNKNOWN` |
| `Production Eligibility` | `READY_FOR_PRODUCTION`, `BLOCKED_NOT_FOR_PRODUCTION`, `DRAFT`, `UNKNOWN`, `NOT_APPLICABLE` |
| `Verdict` | `COMPLIANT`, `WARNINGS`, `NON-COMPLIANT`, `PARTIAL`, `ERROR` |
| `Persistence` | always `NOT_ATTEMPTED` |

`PASS` is permitted only from current, machine-verifiable evidence for the exact
asset bytes, rules, adapter version, target and platform. File existence, extension,
name, modification time, source-code string match, role prose, old import cache, or a
status label alone is never PASS.

## Phase 0: Validate one immutable audit manifest

Resolve literal and real paths without following asset symlinks. Reject paths outside
the project root, duplicate normalized paths, symlink escapes, unsupported encodings,
malformed/duplicate keys, and unsupported schemas. Read raw bytes once and compute
full lowercase SHA-256.

Require `Artifact Type: asset-audit-manifest`, schema version, stable audit target ID,
run scope, category, engine/platform/configuration identity, and:

- exact asset-inventory manifest path/hash with stable asset ID, normalized path,
  raw-byte hash, byte size, detected MIME/container, category, intended target,
  import-metadata path/hash or ABSENT, and LFS/materialization state;
- exact target build/dependency manifest path/hash and build ID/artifact hash when
  production/reference checks are requested;
- exact versioned adapter-registry path/hash;
- ordered rule-source chain with path/hash/locator/domain/authority;
- exact engine reference-resolver registry and dependency-graph receipts;
- exact technical-preferences and art-direction paths/hashes when applicable;
- exact asset-manifest and asset-spec paths/hashes/transaction IDs/statuses when
  production eligibility is in scope;
- file, byte, adapter-time, total-time, output-row and recursion budgets;
- applicable AGENTS.md path/hash chain, generated-at timestamp, owner and hash
  algorithm.

Re-hash every declared source before scanning. A changed inventory, asset byte,
import metadata, rule, adapter registry, dependency graph, asset specification, or
instruction makes the snapshot stale and returns PARTIAL/BLOCKED without mixing
versions.

Do not recursively discover undeclared asset roots. The inventory is the scope
authority. Reject an inventory entry whose real path escapes the project, resolves
through an unapproved symlink, duplicates another asset ID/path, or does not match its
recorded bytes.

## Phase 1: Load rules with deterministic precedence

Rules are never hardcoded in this workflow. Load:

1. root AGENTS.md asset rules;
2. each nested AGENTS.md from root to the asset path, with the closest applicable
   rule overriding the same governance/naming key;
3. technical-preferences/pipeline rules for technical format, import, platform and
   budget keys;
4. art-bible/art-direction rules for visual/material/palette/presentation keys;
5. manifest fallback rules only when explicitly marked advisory.

Rules from different domains do not silently override each other. A naming conflict
between applicable AGENTS files follows closest-file precedence. A technical/art
cross-domain contradiction becomes `UNVERIFIED` with `RULE_CONFLICT` until the named
owners resolve it. Art direction cannot relax engine/platform safety constraints, and
a generic fallback cannot override an authoritative project rule.

Normalize every rule into:

~~~text
rule_id
domain
source_path
source_sha256
source_locator
authority
applicable_asset_types
platform/configuration
expected_value_or_schema
evaluation_operator
adapter_id_and_min_version
severity: HARD | ADVISORY
not_applicable_condition
~~~

A missing stable rule ID, unknown operator, unreadable source, stale hash, or required
rule without a compatible adapter makes rule coverage INCOMPLETE. Record the exact
loaded precedence chain and overridden rules in the result.

## Phase 2: Validate executable adapter contracts

The adapter registry must define, per adapter:

- stable adapter ID/version and supported extension/MIME/container signatures;
- trusted executable/tool identity and version;
- argv array with placeholders, project-contained read-only working scope, timeout
  and output-byte cap;
- explicit guarantee that it does not write project files/import caches;
- structured output schema and parser version;
- exit/result semantics, raw stdout/stderr receipt hash, and cleanup behavior;
- supported engine/platform/configuration versions.

Do not use a shell command string, synthesize a parser, infer metadata from extension,
or fall back to a human guess. Before and after each adapter, verify project asset and
import-metadata hashes are unchanged. If an adapter would trigger import, editor
serialization, cache generation, or another project mutation, do not run it and mark
`NOT_RUN`.

Required adapter classes include, when the inventory contains those types:

- image/texture: header/container, dimensions, channels/alpha, color space,
  compression/mip/import metadata;
- audio: container/codec, sample rate, channels, bit depth, duration and declared mix/
  streaming metadata;
- model/animation: parser for mesh/material/bone/animation counts, units and embedded
  dependencies;
- VFX/resource: engine-compatible structured resource parser, dependency/budget and
  scalability fields;
- shader/material: engine-compatible parser or compiler receipt for declared target
  variants without mutating caches;
- data: exact JSON/YAML/binary parser plus the rule-declared schema path/hash/version;
- any additional in-scope type: a manifest-declared compatible adapter.

An absent executable, missing adapter, unsupported type/version, LFS pointer instead
of content, permission failure, timeout, malformed output, truncated output,
signature mismatch, parse error, or missing schema yields `Adapter State` other than
PASS/FAIL and `Check Result: UNVERIFIED`. Adapter coverage becomes INCOMPLETE. It can
never yield COMPLIANT.

A conclusive adapter `FAIL` means the adapter executed and proved the exact rule was
violated. It is not the same as parse failure or unsupported evidence.

## Phase 3: Execute each rule once against indexed assets

Build the inventory and rule index once. Do not repeatedly scan source code per asset.
For each in-scope asset/rule pair:

1. verify asset/import/rule/adapter hashes;
2. validate the file signature rather than trusting extension;
3. run only the registered read-only argv;
4. validate the structured receipt and bind it to asset ID/path/hash, target,
   platform, rule ID/source hash, adapter ID/version and timestamps;
5. compare expected/actual with the rule's declared operator;
6. emit one stable finding ID derived from target ID, asset ID, rule ID and evidence
   snapshot hash.

Each finding contains:

- finding/rule/asset/target IDs;
- normalized asset and import-metadata paths/hashes;
- category/platform/configuration;
- rule source path/hash/locator and precedence;
- adapter ID/version/state, command receipt/log hashes and timestamp;
- expected value/schema, actual value, units and result;
- HARD/ADVISORY severity, confidence and exact remediation owner;
- evidence limitations and whether production use is blocked.

Respect manifest budgets. When file/byte/time/output caps are reached, stop cleanly,
list uninspected assets/rules, set coverage INCOMPLETE and verdict PARTIAL unless a
known hard FAIL already determines NON-COMPLIANT.

Modification time may be displayed as non-authoritative context only; content hashes
and manifest revision determine reproducibility.

## Phase 4: Build an engine-aware reference graph

Use only the exact versioned engine resolver and build/dependency manifests. A valid
resolver receipt binds engine/version, target build/artifact, source/dependency
manifest hashes, normalized asset IDs, supported reference syntaxes, dynamic registry
coverage, timestamps, tool/parser versions, result and complete log hash.

Resolver coverage must include every applicable mechanism declared by the target,
such as scenes/prefabs/resources, engine UIDs, addressables/asset bundles, import
remaps, serialized IDs, data/config references, runtime registries and declared
dynamic-loading roots.

Classify:

- `REFERENCED`: current graph proves at least one valid inbound/inclusion edge.
- `UNREFERENCED_CONFIRMED`: a complete current resolver/build graph covers every
  declared mechanism and proves the asset is excluded and has no allowed inbound
  edge.
- `POSSIBLY_ORPHANED`: no verified edge was found but resolver/dynamic/build coverage
  is not exhaustive.
- `MISSING_CONFIRMED`: a current parsed reference location and normalized asset ID are
  covered by the resolver, but the inventory/build manifest proves the target absent.
- `UNKNOWN`: resolver unavailable, unsupported, stale, conflicting or invalid.

A source-code text search may appear only as advisory observation. Absence of a string
can never produce `UNREFERENCED_CONFIRMED`; presence of a string can never prove build
inclusion. An unsupported reference syntax cannot produce `MISSING_CONFIRMED`.

Record every reference location, normalized ID, resolver evidence and confidence.
`POSSIBLY_ORPHANED` or `UNKNOWN` makes reference coverage INCOMPLETE. Never recommend
automatic deletion. A confirmed candidate still requires separate human review,
version-control/build-graph checks and separately authorized removal.

## Phase 5: Consume hash-bound asset-spec production state

When production eligibility is in scope, re-hash the exact
`design/assets/asset-manifest.md` and every indexed specification. Require each
manifest row/specification pair to bind the same asset ID/key, target, spec path,
transaction ID, raw hashes, dependency state and one exact status:

- `DRAFT`;
- `BLOCKED_NOT_FOR_PRODUCTION`;
- `READY_FOR_PRODUCTION`.

Treat the staged status contract exactly:

- `BLOCKED_NOT_FOR_PRODUCTION` is a conclusive HARD production blocker for that asset.
  Preserve its blocker list and validation evidence; it cannot be converted by user
  risk acceptance or local adapter PASS.
- `DRAFT` is not production eligible and is a HARD failure when the audited target is
  a production build.
- `READY_FOR_PRODUCTION` is acceptable only when manifest/spec statuses and
  transaction IDs match, committed hashes verify, `production_eligible: true`, all
  required validation rows are current PASS, all inferred requirements are confirmed,
  and no blocker remains.
- missing, mismatched, stale, malformed, uncommitted or unverifiable rows yield
  `Production Eligibility: UNKNOWN` and incomplete external-evidence coverage.

`READY_FOR_PRODUCTION` is external eligibility evidence, not automatic asset-audit
COMPLIANT. All applicable local rules, adapters, reference integrity and coverage
must still pass. Conversely, local technical PASS cannot upgrade DRAFT or
BLOCKED_NOT_FOR_PRODUCTION.

## Phase 6: Separate asset compliance from content completeness

Asset-audit owns:

- naming/format/size/import/pipeline rule compliance;
- binary/structured metadata validation;
- engine reference integrity and production-eligibility state consumption.

It does not decide whether every GDD content requirement shipped, create missing
requirements, or count files as implemented content. Those are content-coverage
questions.

Return external evidence in schema `asset_audit/v2`. A content-completeness consumer
may display a current hash-bound finding for the same target, but:

- asset compliance never proves `SHIPPED_VERIFIED`;
- content inclusion never proves asset compliance;
- `BLOCKED_NOT_FOR_PRODUCTION` remains a production blocker;
- file paths/counts/string matches remain advisory;
- target/build/inventory/rule/packet hashes must match.

Because this workflow writes no project report, its conversation packet is not a
durable external artifact. A later consumer may use it only after an independent
evidence owner persists the exact canonical packet bytes and supplies a verification
receipt binding path, raw hash, target/build, producer identity and timestamp.
Without that receipt, external evidence is UNVERIFIED.

## Phase 7: Deterministic coverage and verdict

Calculate independently:

- inventory coverage;
- rule-source coverage;
- adapter coverage;
- reference-resolver coverage;
- asset-spec/external-evidence coverage;
- platform/configuration coverage.

Apply this exhaustive first-match order:

1. invalid manifest/target/snapshot/scope -> `Verdict: ERROR`;
2. any current conclusive HARD rule FAIL, `MISSING_CONFIRMED`, policy-hard
   `UNREFERENCED_CONFIRMED`, production-target DRAFT, or
   `BLOCKED_NOT_FOR_PRODUCTION` -> `NON-COMPLIANT`;
3. otherwise any coverage is INCOMPLETE/UNAVAILABLE, any required check is
   UNVERIFIED, any adapter is NOT_RUN/UNSUPPORTED/PARSE_ERROR/TIMEOUT/
   INVALID_RECEIPT, any reference is POSSIBLY_ORPHANED/UNKNOWN, or external state is
   UNKNOWN -> `PARTIAL`;
4. otherwise one or more ADVISORY rules conclusively FAIL -> `WARNINGS`;
5. otherwise every applicable required rule is current PASS or valid NOT_APPLICABLE,
   all coverage dimensions are COMPLETE, all production-target assets are verified
   READY_FOR_PRODUCTION, and no contradiction/blocker remains -> `COMPLIANT`.

Known hard failures take precedence over incomplete coverage, while all coverage gaps
remain visible. COMPLIANT is impossible when any required asset type lacks an adapter,
schema or resolver, any parse/execution failed, or any required evidence is partial/
stale/unknown.

Workflow Status is ERROR for verdict ERROR, PARTIAL for verdict PARTIAL, and COMPLETE
for the three conclusive verdicts. COMPLETE does not mean production handoff is
authorized.

## Phase 8: Return the hash-bound evidence packet

Return deterministic canonical JSON semantics for:

~~~text
schema_version: asset_audit/v2
packet_id: <run-id>
packet_sha256: sha256:<digest over canonical packet without this field>
target:
  target_id
  build_id
  build_artifact_sha256
  platform_configuration
  snapshot_at
inputs:
  audit_manifest_path_sha256
  inventory_path_sha256
  build_dependency_manifest_path_sha256
  adapter_registry_path_sha256
  rule_sources
  asset_manifest_path_sha256
coverage:
  inventory
  rules
  adapters
  references
  asset_spec_external
  platforms
counts:
  assets_total
  assets_inspected
  rules_total
  rules_evaluated
  pass
  fail
  unverified
  not_applicable
findings:
  <ordered stable finding rows>
references:
  referenced_ids
  unreferenced_confirmed_ids
  possibly_orphaned_ids
  missing_confirmed_ids
  unknown_ids
production_eligibility:
  ready_ids
  blocked_not_for_production_ids
  draft_ids
  unknown_ids
external_evidence_eligibility:
  conversation_packet: NOT_DURABLE
  durable_receipt_required: true
workflow_status
verdict
persistence: NOT_ATTEMPTED
limitations
recommendation
disclaimer
~~~

Canonicalize UTF-8 JSON with lexicographically sorted object keys and stable arrays
sorted by asset ID then rule ID/finding ID. Calculate the packet digest after every
row and coverage state is fixed. Summary mode retains target, all input hashes, every
coverage field, ID sets, verdict, limitations, packet hash and disclaimer.

The disclaimer states:

- PARTIAL/UNVERIFIED is not compliance;
- COMPLIANT is not proof of GDD content completeness or build inclusion beyond the
  exact manifest evidence;
- READY_FOR_PRODUCTION is consumed external state, not approval issued here;
- no deletion, import, production handoff or other mutation was authorized.

Return at most one owner-specific recommendation and stop. Do not invoke it.
