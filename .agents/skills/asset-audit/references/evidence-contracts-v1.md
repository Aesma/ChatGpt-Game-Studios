# Asset Audit Evidence Contracts v1

This private reference is normative for `$asset-audit`. It supplements the main
SKILL with the exact input, rule, adapter, resolver, finding, coverage, verdict,
and persistence boundaries used by static and behavioral verification.

## 1. Closed invocation contract

Accepted grammar is exactly:

```text
$asset-audit --manifest <project-relative-regular-file>
             [--category art|audio|model|animation|vfx|shader|data|provenance|license|reference|all]
             [--summary]
```

`--manifest` occurs exactly once. `--category` and `--summary` occur at most once;
category defaults to `all`. Options may be reordered. There are no positional
arguments or implicit latest/current inputs.

Reject unknown/repeated flags, missing values, invalid category, absolute/UNC/
drive/URI paths, traversal/dot segments, glob/regex metacharacters, directories,
non-regular files, unsupported encodings, case ambiguity, and any symlink,
junction, mount/reparse escape with `ERROR — INVALID INVOCATION`. Error is an
execution state and emits no audit verdict/evidence envelope.

Asset-family categories select that family plus all applicable compliance,
provenance, license, reference, and production channels. `provenance`, `license`,
and `reference` select that channel across the inventory plus its prerequisites.
`--summary` changes only human projection; machine identity and coverage are
identical to full output.

## 2. Immutable target and scope

Input manifest schema is `cgs.asset-audit-manifest/v1`. It binds exactly one
project, target, build/artifact, engine/version, platform, configuration, category,
inventory and completeness receipt, adapter/resolver registries, build/dependency
manifest when references apply, rule-source chain, instruction chain, technical/
art sources, provenance/license policy/records, production-state sources, and
effective limits.

Every declared input has stable artifact/asset ID, canonical project-relative
path, exact declared revision, schema/version, relationship, and expected status or
explicit absence. Resolve literal and real paths without following asset links.
Duplicate ID/path, path escape, unapproved alias, revision mismatch before lock,
duplicate mapping key, unsupported schema, ambiguous engine/target/build, or an
untrustworthy inventory identity makes the manifest invalid before adapters run.

The asset inventory is the only scope authority. It contains stable asset ID,
canonical path, exact declared revision/size, detected signature/container, declared type,
category, target, import metadata path/revision or `ABSENT`, materialization/LFS state,
and provenance/license IDs. A registered inventory-completeness receipt binds all
declared roots/exclusions, generator adapter/version/revision, ordered complete
candidate revision, and inventory output revision. Missing/stale/incomplete receipt
makes inventory coverage incomplete even when every listed item passes.

Never recursively discover undeclared roots. Re-enumerate only declared roots at
finalization to detect added/removed/renamed candidates. Never follow a link
outside the project or inspect external/aliased bytes.

## 3. Fixed hard limits

The manifest may lower but never raise:

```yaml
max_manifest_bytes: 1048576
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

Sort complete identities by channel, stable asset/artifact ID or null, then
canonical path. Record an explicit revision for the complete identity sequence. Retain bounded detailed rows;
for omitted rows record exact total/omitted count, first/last omitted sort key, and
the stable first and last omitted business keys. Do not inspect or judge omitted rows.
Emit one `OVER_LIMIT` coverage finding and force `PARTIAL` absent a separately
conclusive current HARD failure.

Build inventory, rule, adapter, provenance, license, and reference indexes once.
Do not perform a repository/code search per asset. A bounded sample or prefix can
never establish complete coverage or `COMPLIANT`.

## 4. Deterministic rule precedence

Load actual sources and raw revisions in this order:

1. applicable `AGENTS.md` files root-to-target; the closest instruction wins the
   same explicit governance rule key;
2. technical-preferences/pipeline rules for format, import, platform, performance,
   schema, and engine safety not overridden by applicable instructions;
3. art-bible/art-direction rules for visual, palette, material, animation, and
   presentation constraints not overridden by applicable instructions;
4. approved provenance/license policies for origin, use, attribution,
   redistribution, derivative, territory/platform, and expiration obligations not
   overridden by applicable instructions; and
5. manifest fallback rules only when explicitly advisory.

Different domains coexist. They do not silently override one another. An
instruction may explicitly resolve a cross-domain rule key; otherwise incompatible
authoritative technical/art/license demands produce `RULE_CONFLICT`, an
`UNVERIFIED` check, incomplete rule coverage, and `PARTIAL`. Art direction cannot
relax technical safety or license obligations. Role opinion, model memory, prior
report, common practice, and specialist consultation are not rule sources.

Each normalized rule contains stable rule ID, domain, source artifact/path/raw
revision/stable locator/schema, authority, applicable asset types, target/platform/
configuration, typed expected value/schema, registered operator, adapter class and
minimum version, `HARD|ADVISORY` severity, explicit N/A predicate, and remediation
owner. Duplicate conflicting IDs, missing ID/source/revision/operator/owner, ambiguous
precedence, unreadable/stale required source, or missing compatible adapter makes
coverage incomplete. Identical duplicates may deduplicate only while preserving
all provenance.

## 5. Versioned adapter contract

The adapter registry declares stable class/ID/semantic version, executable/tool
identity and revision, supported engine/platform/configuration, signatures/containers/
schemas/operators, typed argv array, project-read-only mount, separate bounded
scratch root, no network, timeout/output cap, no project/import/cache mutation,
structured receipt/parser version, deterministic normalization, result semantics,
and cleanup.

Never use a shell command string, infer metadata from extension, synthesize a
parser, use visual/manual judgment, or let an adapter discover scope. If OS-level
project read-only isolation is unavailable or execution could import, serialize,
generate cache, contact network, or write project bytes, do not run and report
`NOT_RUN`.

`cgs.asset-adapter-receipt/v1` binds:

```text
receipt ID/schema
project/target/build/platform/configuration
asset/import/rule IDs and raw revisions
adapter class/ID/version/executable revision
argv-array revision, canonical cwd and sandbox-policy revision
started/ended/deadline, exit/timeout state
structured output/schema/parser version and revision
bounded stdout/stderr revisions and truncation state
before/after project/import/cache snapshot revisions
result: PASS | FAIL | NOT_RUN | UNSUPPORTED | PARSE_ERROR | TIMEOUT | INVALID_RECEIPT
limitations and receipt revision
```

`PASS` proves an applicable rule for exact current bytes/target. `FAIL` is
conclusive only when a valid execution proved the typed violation. Missing/
incompatible adapter or executable, signature mismatch, LFS pointer, permission,
timeout, malformed/truncated output, parse/schema error, invalid receipt, stale
identity, or mutation risk produces `UNVERIFIED`, incomplete adapter coverage,
and never an inferred PASS/FAIL.

Applicable adapters include image/texture, audio, model/animation, VFX/resource,
shader/material, JSON/YAML/binary data/schema, provenance, license-policy, engine
reference resolution, and every additional declared type. Extension never proves
type; a registered signature/container detector does.

## 6. Engine-specific reference resolver

Reference checks require one compatible registered resolver for the exact
engine/version/target/platform/configuration and one current build/dependency
manifest. The resolver registry enumerates each supported syntax as:

```yaml
syntax_id: <stable engine-specific syntax ID>
syntax_version: <exact version>
engine_range: <supported engine versions>
source_types: [<scene/prefab/resource/config/package types>]
parser_identity: <exact parser identity>
reference_token_kind: PATH | UID | GUID | ADDRESS | SERIALIZED_ID | REMAP | REGISTRY_KEY | PACKAGE_ID
normalizer_identity: <exact normalized-ID contract>
dynamic_coverage: STATIC_ONLY | DECLARED_ROOTS | EXHAUSTIVE_FOR_TARGET
```

`cgs.asset-reference-graph/v1` binds resolver ID/version/executable/parser/
normalizer revisions; engine/target/build/artifact/inventory/dependency-manifest
identities; supported/unsupported syntax set; declared dynamic roots/registries/
packages; exact parsed edges; complete edge count/revision; start/end/result/log
revision; and coverage/limitations.

Every edge contains stable edge ID, syntax ID/version, source artifact ID/path/revision,
stable structural locator, raw reference-token revision (not required to expose secret
or huge text), normalized ID kind/value, edge kind, resolved asset ID/path/revision or
explicit absent target, and target/build inclusion state. The normalized asset ID,
not display path or source string, is the graph join key.

Coverage must enumerate every applicable static and dynamic mechanism: scenes,
prefabs, resources, engine UID/GUID, addressables/bundles, import remaps, serialized
IDs, data/config references, runtime registries, declared dynamic-loading roots,
package/pak catalogs, and equivalent engine-native links. An unknown engine/
version/syntax/dynamic root/packed format is an explicit unsupported mechanism.

Classify exactly:

- `REFERENCED`: current graph proves a valid inbound or inclusion edge.
- `UNREFERENCED_CONFIRMED`: exhaustive current resolver/build coverage proves no
  inbound, allowed dynamic, or build edge.
- `POSSIBLY_ORPHANED`: no verified edge but any required coverage is incomplete.
- `MISSING_CONFIRMED`: supported syntax parsed at an exact location to a normalized
  ID and current inventory/build evidence proves the ID absent.
- `UNKNOWN`: unavailable/unsupported/stale/conflicting/invalid resolver evidence or
  unnormalizable identity.

String search is advisory only. String absence never proves orphaning; string
presence never proves engine/build inclusion. Unsupported syntax can never prove a
missing target. `POSSIBLY_ORPHANED`/`UNKNOWN` force incomplete reference coverage.
`MISSING_CONFIRMED` is HARD. `UNREFERENCED_CONFIRMED` has effect only from an exact
applicable HARD/ADVISORY policy rule. Never recommend automatic deletion.

## 7. Stable findings and severity

Each finding follows the main `AAF-...` schema and is assembled from declared stable business fields
of project ID, finding category, stable asset/rule/target IDs, stable provenance/
license/reference/production record IDs, and platform/configuration. Paths,
display names, wording, line, raw/content revisions, expected/actual values, severity,
confidence, status, run ID, timestamp, and recommendation are excluded from
identity. Preserve these values as evidence, not identity.

Severity comes only from the exact effective rule:

- `HARD`: a current conclusive FAIL blocks compliance;
- `ADVISORY`: a current conclusive FAIL may yield WARNINGS only with complete
  coverage; and
- `COVERAGE`: missing/unverified/unsupported evidence yields PARTIAL, not a
  fabricated violation.

Every finding contains complete evidence revisions/receipts, owner, open/current
status, objective closure condition, result, and limitation. Incompatible evidence
under one stable business key is a coverage conflict and forces PARTIAL absent a separate
current HARD failure.

## 8. Deterministic aggregation

Apply the first matching row:

| Priority | Exact condition | Result |
|---:|---|---|
| 1 | invalid invocation/manifest/target/snapshot, actual project mutation, no trustworthy inventory/packet | execution `ERROR`; no verdict/evidence envelope |
| 2 | any current conclusive HARD rule/reference/license/production failure | `NON-COMPLIANT` |
| 3 | otherwise any required incomplete/unavailable/UNVERIFIED/unsupported/stale/overflow/conflict state | `PARTIAL` |
| 4 | otherwise one or more conclusive ADVISORY failures | `WARNINGS` |
| 5 | otherwise all applicable required checks PASS/valid N/A and every required channel is complete | `COMPLIANT` |

Known HARD failures take precedence over gaps, but all gaps remain visible and the
report states it is not exhaustive. `COMPLIANT` is impossible from a subset,
empty search without a valid completeness receipt, missing adapter/schema/resolver,
unsupported syntax/type, stale input, unverified provenance/license, or unknown
production state. `NOT_APPLICABLE` requires an authoritative rule predicate and
current positive evidence; missing input is never N/A.

## 9. Failure, mutation, and persistence boundary

Snapshot every declared project input plus import/cache locations before adapter
execution and revalidate after each adapter/finalization. A stale input discards
only conclusions derived from old bytes, preserves independent current evidence,
marks affected coverage incomplete, and yields PARTIAL absent HARD failure. An
actual project mutation makes the run `ERROR` with no evidence envelope; do not
repair, revert, delete, or attribute the change.

The analyzer never writes a report or invokes a recorder. Its conversation
envelope is `NOT_PERSISTED`/not durable. A separate recorder would require fresh
authorization over exact canonical envelope bytes, independently re-read every artifact/manifest/payload/envelope and validate its declared revision and target/build identity, CAS an
owner-declared destination, write atomically, and emit a persistence receipt.
This workflow does not select that destination or simulate persistence.

Every non-error result preserves these machine assertions:

```text
allowed_project_write_set: []
report_persisted: false
recorder_invoked: false
mutation_authorized: false
```

Asset-audit owns compliance, metadata, provenance, approved license-policy
evidence, reference integrity, and consumed production eligibility. Content-audit
alone owns stable GDD requirement-to-build inclusion. Neither invokes the other;
asset compliance never proves `SHIPPED_VERIFIED`, and build inclusion never proves
asset compliance.
