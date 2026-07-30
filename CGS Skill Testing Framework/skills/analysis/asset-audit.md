# Skill Test Spec: $asset-audit

## Skill Summary

`$asset-audit` is a strictly read-only, bounded analyzer for asset-rule
compliance, provenance, license-policy evidence, reference integrity, and
consumed production state. It uses one immutable manifest, deterministic rule
precedence, registered versioned adapters, stable asset/rule/finding IDs, and
exact declared revisions. It returns a `cgs.review-evidence/v1` envelope with a
`cgs.asset-audit-report/v1` extension under contract `cgs.asset-audit/v3`.

The analyzer owns asset compliance and reference integrity. It never claims that
a GDD content requirement shipped; that comparison belongs to content-audit.
Unsupported, stale, failed, unknown, or over-limit evidence cannot produce
`COMPLIANT`.

Every non-error result must state `allowed_project_write_set: []`,
`report_persisted: false`, `recorder_invoked: false`, and
`mutation_authorized: false`.

This specification is a repaired catalog candidate and is **NOT EXECUTED**.
Static inspection or contract editing must not populate catalog `last_*`, pass,
or tested fields without immutable runner receipts bound to the exact candidate
revisions.

## Contract Sources

- `.agents/skills/asset-audit/SKILL.md`
- `.agents/skills/asset-audit/references/evidence-contracts-v1.md`
- `.agents/skills/asset-audit/references/continued-workflow.md`
- `.agents/skills/asset-audit/agents/openai.yaml`

---

## P1 Remediation Trace

The root remediation task names these seven rows `AA-004..AA-010`; the repository
audit source names the same ordered P1 rows `ASA-002..ASA-008`.

| Task ID | Repository audit ID | Required behavior | Primary cases |
|---|---|---|---|
| AA-004 | ASA-002 | Root-to-target instructions and domain rule sources use explicit precedence | 5, 6 |
| AA-005 | ASA-003 | Orphan decisions use complete engine/build reference graphs, not string search | 10, 11, 12 |
| AA-006 | ASA-004 | Registered engine resolvers enumerate supported syntaxes and normalized IDs/locations | 11, 13 |
| AA-007 | ASA-005 | Stable rule severity and deterministic verdict aggregation | 3, 4, 18 |
| AA-008 | ASA-006 | Closed category grammar, project-root confinement, and no-follow symlink behavior | 1, 7 |
| AA-009 | ASA-007 | One-pass indexes, fixed budgets, bounded rows/revisions, and explicit failure coverage | 8, 9, 17 |
| AA-010 | ASA-008 | Static/behavioral spec matches v3; real binary/adapter/mutation fixtures are required | all |

---

## Static Assertions (Structural)

- [ ] Frontmatter contains only `name` and a non-empty `description`; name matches
      the skill directory.
- [ ] Both private reference links resolve and their invocation, bounds, resolver,
      verdict, read-only, and persistence contracts agree with the SKILL.
- [ ] Declares `cgs.asset-audit/v3`, `cgs.review-evidence/v1`,
      `cgs.asset-audit-report/v1`, and registered receipt/graph/provenance/license
      schemas.
- [ ] Invocation requires exactly one project-relative `--manifest`, accepts the
      closed category enum and optional presentation-only `--summary`, and rejects
      positional/duplicate/unknown arguments, URLs, globs, regexes, escapes,
      directories, symlinks, and junctions.
- [ ] Declares strict read-only behavior and forbids edits, imports, cache writes,
      fixes, report persistence, approval prompts, gates, delegation, and
      downstream skill invocation.
- [ ] Adapters require an OS-level project-read-only sandbox, argv arrays, exact
      executable revisions/versions, no shell string/network, bounded scratch,
      structured receipts, timeouts, and output caps.
- [ ] Reads all applicable root-to-target `AGENTS.md` files.
- [ ] Defines explicit rule precedence across instructions, technical preferences,
      art direction, provenance/license policy, and advisory manifest fallbacks.
- [ ] Cross-domain contradictions become `RULE_CONFLICT`/`UNVERIFIED` rather than
      a silent override.
- [ ] Rules have stable IDs, source artifact/path/revision/locator, domain, authority,
      typed applicability/operator, adapter requirement, severity, and owner.
- [ ] Defines fixed candidate, asset, byte, rule, receipt, reference-edge,
      provenance, license, output, and time limits that a manifest may only lower.
- [ ] Records the complete candidate business-key sequence and explicit inventory revision while retaining bounded
      detailed rows and exact overflow counts/boundary keys/revisions.
- [ ] Scope comes from a revision-bound inventory and registered completeness receipt,
      not undeclared recursive discovery or per-asset repository rescans.
- [ ] Every applicable type/rule uses a registered versioned adapter; metadata is
      verified from signature/container/structured output, never extension alone.
- [ ] JSON/YAML/binary validation requires exact parser and schema identity.
- [ ] `PASS` and conclusive `FAIL` require a valid current
      `cgs.asset-adapter-receipt/v1`; unsupported/parse/timeout/mutation-risk states
      are `UNVERIFIED` and incomplete.
- [ ] Provenance and license-policy records bind stable IDs, exact asset bytes,
      source receipts, policy/rule revisions, target scope, obligations, and
      derivation parent chains.
- [ ] Missing/unsupported/conflicting provenance or license evidence fails closed;
      prohibited/expired or conclusively unmet HARD obligations are HARD failures.
- [ ] License-policy output is evidence under the named policy and not legal advice.
- [ ] Engine references require a versioned resolver and
      `cgs.asset-reference-graph/v1` receipt covering declared static, dynamic,
      UID/addressable, packed, serialized, remap, and registry mechanisms.
- [ ] String absence cannot confirm orphan status; unsupported syntax cannot
      confirm a missing asset; unknown/incomplete graph coverage is `PARTIAL`.
- [ ] `UNREFERENCED_CONFIRMED` becomes a failure only under an exact applicable
      rule, and no automatic deletion is recommended.
- [ ] Asset-audit owns compliance/provenance/license/reference integrity while
      content-audit exclusively owns requirement-to-build inclusion.
- [ ] Asset PASS never emits `SHIPPED_VERIFIED` or proves content completeness.
- [ ] Stable `AAF-...` findings exclude paths, wording, revisions, values, severity,
      status, run identity, timestamps, and recommendation from identity.
- [ ] Coverage is recorded per candidate/channel/check with explicit
      `COMPLETE | PARTIAL | FAILED | NOT_APPLICABLE` states.
- [ ] Verdict precedence is deterministic: execution error, conclusive HARD
      failure, incomplete coverage, advisory failure, then fully proven compliance.
- [ ] Emits a version-bound envelope with explicit revisions; summary mode preserves all machine
      semantics and revisions.
- [ ] Returns at most one owner-routed recommendation and never executes it.
- [ ] Metadata describes adapter-backed, read-only, provenance/license/reference,
      fail-closed behavior and the content-audit ownership boundary.

---

## Director Gate Checks

None. Asset-audit is a read-only analyzer. It never invokes a director,
technical-artist consultation, remediation agent, recorder, or downstream
workflow in any category or verdict path.

---

## Required Fixture Contract

Behavioral fixtures provide exact bytes and required revision values for the audit
manifest, inventory and completeness receipt, assets/import metadata, adapter and
resolver registries, executable identities and receipts, build/dependency data,
rules/instructions/technical preferences/art direction, provenance/license
records and policy, production-state inputs, and expected canonical envelope.

Binary tests use real minimal PNG and audio/container bytes plus corrupt variants;
data tests use exact JSON/YAML bytes and schemas. Mutation tests snapshot every
project path and import/cache location before and after. Adapter, resolver, and
time behavior is injected deterministically; test harnesses do not infer results
from extensions or role prose.

The exact typed schemas under test are `cgs.asset-adapter-receipt/v1`,
`cgs.asset-reference-graph/v1`, `cgs.asset-provenance/v1`, and
`cgs.asset-license/v1`.

---

## Test Cases

### Case 1: Exact invocation and immutable target lock

Fixture:

- A valid project-relative manifest uses `cgs.asset-audit-manifest/v1` and binds
  one stable target/build/platform/configuration plus every declared input revision.
- Invalid variants use an absolute path, URL, glob, regex, dot segment, duplicate
  flag, positional category, directory, symlink, junction, or unknown category.

Inputs:

```text
$asset-audit --manifest audit/asset-audit.yaml
$asset-audit --manifest audit/asset-audit.yaml --category audio --summary
```

Expected behavior:

1. The first defaults to `all`; the second scopes to `audio` and compacts only
   the human projection.
2. Valid runs lock one exact target snapshot.
3. Every invalid variant returns `ERROR — INVALID INVOCATION` or
   `ERROR — INVALID AUDIT MANIFEST` before adapters run, with no verdict or
   evidence envelope.

Assertions:

- [ ] Closed categories include art, audio, model, animation, vfx, shader, data,
      provenance, license, reference, and all.
- [ ] Asset-family categories run all applicable channels for that family;
      provenance/license/reference categories run that channel across inventory
      assets with only its required prerequisites.
- [ ] No path is resolved outside the project or through a symlink/junction.
- [ ] Nothing is selected by “latest”, editor state, or modification time.

---

### Case 2: Complete binary image adapter PASS

Fixture:

- Real minimal PNG bytes have a valid signature and registered image-adapter
  receipt for exact dimensions, color, alpha, compression, mip, and import data.
- Every applicable HARD rule and rule source revision matches.
- All other required art-scope coverage channels are independently complete.

Input: `$asset-audit --manifest audit/asset-audit.yaml --category art`

Expected behavior:

1. The adapter validates the file signature rather than `.png`.
2. Per-rule rows bind asset, import, rule, executable, adapter, receipt, and target
   revisions.
3. Each applicable rule is `PASS` and `COMPLIANT` is eligible only because every
   required scoped coverage channel is complete.

Assertions:

- [ ] Extension and visual inspection are not evidence.
- [ ] Receipt schema, parser, argv revision, sandbox policy, and logs are validated.
- [ ] No import metadata or cache bytes change.

---

### Case 3: Missing or corrupt adapter fails closed

Fixture variants:

- An image has no compatible adapter.
- The adapter executable revision differs from the registry.
- A valid executable emits malformed/truncated output.
- A mutating adapter cannot run with a project-read-only mount.

Expected behavior:

1. States are respectively `UNSUPPORTED`, `INVALID_RECEIPT` or `NOT_RUN`, and
   `PARSE_ERROR`/`INVALID_RECEIPT` as contract evidence dictates.
2. Every affected check is `UNVERIFIED` and adapter coverage is incomplete.
3. Verdict is `PARTIAL`, not `FAIL`, `NON-COMPLIANT`, or `COMPLIANT` unless
   separate current evidence proves a HARD failure.

Assertions:

- [ ] Parse failure is not a conclusive format violation.
- [ ] No human guess or fallback parser is synthesized.
- [ ] Mutation-risk adapters are not executed.

---

### Case 4: Audio and data conclusive failures

Fixture:

- Real audio-container bytes produce a valid receipt with codec, sample rate,
  channels, bit depth, duration, streaming, and mix metadata.
- A HARD sample-rate rule fails.
- JSON and YAML fixtures bind exact parser and schema path/revision/version; one has a
  conclusive schema violation, while another lacks a supported YAML feature.

Expected behavior:

1. Current conclusive HARD violations are stable `RULE_FAIL` findings and verdict
   `NON-COMPLIANT`.
2. Unsupported YAML produces `UNVERIFIED` coverage rather than a fabricated fail.
3. If conclusive HARD failures and other coverage gaps coexist,
   `NON-COMPLIANT` takes precedence and all gaps remain visible.

Assertions:

- [ ] Findings include expected/actual/units, exact rule evidence, receipt revision,
      and owner.
- [ ] Extension alone is never evaluated.
- [ ] The deterministic first-match verdict order is used.

---

### Case 5: Root-to-target instruction precedence

Fixture:

- Root `AGENTS.md` declares naming rule `asset.naming.case`.
- A nested applicable `AGENTS.md` overrides that exact rule key.
- Technical preferences supplies texture budgets; art direction supplies palette
  constraints; the license policy supplies redistribution obligations.

Expected behavior:

1. Both instruction sources are loaded root-to-target and exact revisions reported.
2. The closest applicable instruction wins the same governance rule key.
3. Technical, art, and license rules coexist in their own domains.
4. Effective and overridden rules appear in `rule_precedence`.

Assertions:

- [ ] No built-in naming/format default overrides a project rule.
- [ ] Technical preferences and art direction are not interchangeable.
- [ ] Role memory or consultation is not a rule source.

---

### Case 6: Cross-domain contradiction remains unresolved

Fixture:

- Current technical and art sources make incompatible authoritative demands for
  the same material setting.
- No applicable instruction explicitly resolves the conflict.

Expected behavior:

1. Neither domain silently overrides the other.
2. A stable `RULE_CONFLICT` finding cites both exact sources.
3. The check is `UNVERIFIED`, rule coverage is incomplete, and verdict is
   `PARTIAL` absent a separate conclusive HARD failure.

Assertions:

- [ ] Art direction cannot relax technical safety or license obligations.
- [ ] A generic manifest fallback cannot resolve the conflict.
- [ ] The analyzer does not ask a specialist to decide product truth.

---

### Case 7: Invalid inventory identity, revision, or materialization

Fixture variants:

- Duplicate asset ID or normalized path.
- Asset real path escapes the project through a symlink.
- Recorded bytes mismatch the current revision.
- Inventory row points to an LFS pointer instead of materialized content.
- A declared asset is unreadable.

Expected behavior:

1. Identity/path/revision violations that invalidate scope return
   `ERROR — INVALID AUDIT MANIFEST` before adapters run.
2. A valid manifest whose specific selected asset is an LFS pointer or becomes
   unreadable records `LFS_POINTER`/`UNREADABLE`, `UNVERIFIED`, incomplete
   coverage, and `PARTIAL`.
3. No aliased/external bytes are inspected.

Assertions:

- [ ] Exact declared revisions, not mtime/Git labels, determine currentness.
- [ ] No adapter PASS is synthesized for absent bytes.
- [ ] Every failure is represented in manifest and coverage rows.

---

### Case 8: Fixed budget and bounded overflow behavior

Fixture:

- The complete inventory identity stream has 1,000 items.
- The effective selected-asset limit is 200 and is no greater than the fixed cap.
- A manifest attempts to raise another fixed limit.

Expected behavior:

1. The manifest cannot raise the fixed limit.
2. The complete identity sequence is versioned; 200 deterministic detailed rows are
   retained; exact omitted count, first/last sort keys, and omitted revision are
   reported.
3. Omitted assets are not inspected or partially judged.
4. One aggregate `OVER_LIMIT` coverage row names all affected checks and verdict
   is `PARTIAL` absent a known HARD failure.

Assertions:

- [ ] No 800-row unbounded output is required.
- [ ] A sample or bounded prefix cannot yield `COMPLIANT`.
- [ ] Rule, receipt, edge, provenance, license, finding, byte, and time limits use
      the same fail-closed principle.

---

### Case 9: Inventory completeness receipt prevents false compliance

Fixture:

- Every listed asset passes its rules.
- The inventory-completeness receipt is missing, stale, has an unknown generator
  adapter, or does not bind declared roots/exclusions and output revision.

Expected behavior:

1. Listed asset PASS rows remain visible.
2. Inventory coverage is incomplete.
3. Verdict is `PARTIAL`, never `COMPLIANT`.

Assertions:

- [ ] A clean subset is not treated as the whole asset scope.
- [ ] The analyzer does not recursively discover undeclared roots as a fallback.
- [ ] A proven empty inventory may be complete only with a valid completeness
      receipt for the exact bounded scope.

---

### Case 10: Complete engine graph confirms an unreferenced asset

Fixture:

- A current `cgs.asset-reference-graph/v1` receipt covers every declared static,
  dynamic, UID/addressable, packed, remap, serialized, registry, and build
  mechanism.
- It proves asset `texture.unused-banner` has no inbound, dynamic, or build edge.
- Policy marks confirmed unused assets ADVISORY.

Expected behavior:

1. Reference state is `UNREFERENCED_CONFIRMED`.
2. One advisory rule failure may produce `WARNINGS` when all coverage is complete.
3. No deletion is performed or automatically recommended.

Assertions:

- [ ] Complete graph evidence, not string absence, supports the state.
- [ ] A HARD/non-HARD consequence comes only from the exact policy rule.
- [ ] Human/VCS/build review and separate authorization remain required for any
      later removal.

---

### Case 11: Dynamic UID/addressable edge defeats a false orphan

Fixture:

- No source file contains the asset's path string.
- A current engine receipt contains an exact normalized UID/addressable/runtime
  registry edge to the asset.

Expected behavior:

1. Reference state is `REFERENCED`.
2. The exact edge, source location, resolver version, target/build, and revisions are
   reported.
3. Text absence has no classification effect.

Assertions:

- [ ] Dynamic registries and engine-native IDs are first-class mechanisms.
- [ ] Display path and normalized asset ID are not conflated.
- [ ] Reference PASS does not imply GDD content inclusion.

---

### Case 12: Incomplete graph is only possibly orphaned

Fixture:

- No verified edge is found.
- One declared dynamic loading root and one packed-asset syntax were not covered
  by the resolver.

Expected behavior:

1. Reference state is `POSSIBLY_ORPHANED`, not
   `UNREFERENCED_CONFIRMED`.
2. Unsupported mechanisms are explicit resolver coverage gaps.
3. Verdict is `PARTIAL` absent a separate HARD failure.

Assertions:

- [ ] Unknown engine/version/syntax/packed formats cannot be ignored.
- [ ] A code-string search cannot fill graph coverage.
- [ ] The packet explains that `PARTIAL` is non-exhaustive.

---

### Case 13: Confirmed missing and unsupported reference syntax

Fixture variants:

- A supported scene syntax parses an exact source location and normalized asset
  ID that current inventory/build evidence proves absent.
- Another data file uses a syntax absent from the resolver registry.

Expected behavior:

1. The supported broken edge is `MISSING_CONFIRMED`, a HARD
   `REFERENCE_FAIL`, and produces `NON-COMPLIANT`.
2. The unsupported syntax is `UNKNOWN`, a `REFERENCE_GAP`, and incomplete
   coverage; it cannot be called missing.
3. Both locations and evidence channels remain visible when the HARD failure takes
   verdict precedence.

Assertions:

- [ ] Resolver syntax support is exact and versioned.
- [ ] Reference locations and normalized IDs are revision-bound.
- [ ] New content requirements are not invented.

---

### Case 14: Provenance chain and generated/derived assets

Fixture:

- An internal original asset has a valid creation receipt.
- A commissioned asset has an exact provider/acquisition record.
- A generated asset records policy-required generator/model/tool identity and
  creation receipt.
- A derived asset has an exact acyclic parent chain to covered assets.
- Variants include a missing record, revision mismatch, unknown schema, cycle, and
  conflicting provider records.

Expected behavior:

1. Valid rows become provenance-verified only for exact asset bytes.
2. Invalid variants are `PROVENANCE_UNVERIFIED` or
   `PROVENANCE_CONFLICT`, make coverage incomplete, and yield `PARTIAL` absent a
   separate HARD failure.
3. No origin or rights are inferred from filenames, URLs, or project location.

Assertions:

- [ ] Every parent and record uses stable IDs and exact revisions.
- [ ] Derived cycles are detected deterministically.
- [ ] Generated provenance requirements come from policy, not model memory.

---

### Case 15: License-policy evidence and obligations

Fixture variants:

- An allowed license has exact policy and receipt revisions.
- An allowed-with-obligations license has current attribution evidence.
- Another lacks required attribution evidence.
- Other records are prohibited, expired, unknown, conflicting, or outside the
  permitted target/platform/territory.

Expected behavior:

1. `ALLOWED` and fully satisfied `ALLOWED_WITH_OBLIGATIONS` may pass.
2. `PROHIBITED`, `EXPIRED`, and conclusively unmet HARD obligations are HARD
   failures and produce `NON-COMPLIANT`.
3. Unknown/missing/unsupported/conflicting records produce `UNVERIFIED` or
   `LICENSE_CONFLICT`, incomplete coverage, and `PARTIAL` absent a separate HARD
   failure.
4. Results are explicitly evidence under the named policy, not legal advice.

Assertions:

- [ ] The analyzer never chooses the newest or most permissive record.
- [ ] `NOT_APPLICABLE` requires an exact policy rule.
- [ ] Scope, expiration, derivative/redistribution rights, and obligations are
      evaluated only by a registered policy adapter.

---

### Case 16: Content-audit has exclusive completeness ownership

Fixture:

- All asset checks, provenance, license, and references pass for the target.
- The target build-inclusion manifest omits one stable GDD requirement.
- A content-audit consumer receives the exact asset-audit envelope.

Expected behavior:

1. Asset-audit may be `COMPLIANT` for its exact asset scope but does not emit
   `SHIPPED_VERIFIED` or decide the missing GDD requirement.
2. Content-audit alone owns requirement-to-build comparison.
3. The consumer may display current asset evidence only after re-reading and validating the declared
   recognized envelope, producer/extension, target/build/manifest, artifact, and
   payload revisions.
4. Asset compliance does not substitute for build inclusion, and build inclusion
   does not substitute for compliance.

Assertions:

- [ ] There is no overlapping missing-content owner.
- [ ] Asset compliance PASS does not prove content inclusion or requirement
      coverage.
- [ ] File counts and paths remain advisory in both directions.
- [ ] Neither analyzer invokes the other.

---

### Case 17: Frozen snapshot mutation and strict read-only guard

Fixture:

- A rule source changes bytes after manifest lock.
- A new inventory candidate appears under a declared root.
- A malicious adapter attempts to write import metadata/cache data.
- A finding concerns a confirmed unused asset.

Expected behavior:

1. Final re-enumeration/re-reading records added and stale inputs and discards
   conclusions from old bytes.
2. The malicious adapter is not run when sandbox policy is validated; any actual
   detected project mutation is an execution `ERROR` with no evidence envelope.
3. Other unaffected evidence may appear only in non-evidence diagnostics after an
   execution error.
4. No deletion, fix, reimport, report write, or mutation approval prompt occurs.

Assertions:

- [ ] Project and import/cache snapshots remain byte-identical in every valid run.
- [ ] Stale or mixed snapshots never yield `COMPLIANT`.
- [ ] The analyzer never attempts automatic cleanup.

---

### Case 18: Deterministic verdict and summary matrix

Evaluate these independent subfixtures:

| Current evidence | Expected result/verdict |
|---|---|
| invalid invocation/manifest, actual mutation, or untrustworthy packet | `ERROR`, no verdict/evidence |
| conclusive current HARD failure plus any coverage state | `NON-COMPLIANT` |
| no HARD failure, but any required coverage/check is incomplete or unverified | `PARTIAL` |
| complete coverage with advisory failures only | `WARNINGS` |
| complete coverage, all applicable checks PASS/valid N/A, no blocker | `COMPLIANT` |

Assertions:

- [ ] The first matching rule is applied mechanically.
- [ ] Known failures and every coverage gap remain visible regardless of
      precedence.
- [ ] `COMPLIANT` is impossible from a subset, empty search, unknown evidence,
      missing adapter/schema/resolver, stale record, or unsupported type/syntax.
- [ ] `--summary` retains identical machine target, manifest, rule precedence,
      coverage, state sets, finding IDs, verdict, limitations, and revisions.

---

### Case 19: Stable finding identity and evidence validation

Fixture:

- Run A has one HARD format finding for stable asset/rule/target IDs.
- Run B moves the asset path, changes wording, actual bytes, line location,
  severity display, and evidence timestamp without changing the logical issue.
- Run C changes the stable rule ID.

Expected behavior:

1. Runs A and B retain the same `AAF-...` finding ID while artifact/manifest/
   payload/record revisions change.
2. Run C gets a different stable business key and finding ID.
3. Incompatible evidence under one stable business key is a coverage conflict and forces
   `PARTIAL` absent a separate HARD finding.

Assertions:

- [ ] Finding identity uses stable project/asset/rule/target/record IDs and
      platform/configuration.
- [ ] Paths, names, wording, line numbers, revisions, values, severity, status, run
      ID, timestamp, and recommendation are excluded.
- [ ] Every artifact, manifest, extension payload, and envelope revision revalidates declared.

---

## Protocol Compliance

- [ ] Invocation, project identity, target/build/platform, applicable
      instructions, and every source are exact and revision-bound.
- [ ] Rule precedence is explicit, domain-aware, and reports winners, overrides,
      and conflicts.
- [ ] Scope uses a registered inventory completeness receipt and fixed bounded
      limits with complete candidate/overflow revisions.
- [ ] Registered adapters/resolvers are versioned, sandboxed read-only, typed,
      receipt-bound, and fail closed.
- [ ] Binary/container/schema checks use actual fixture bytes and registered
      parsers rather than extensions.
- [ ] Provenance and license-policy evidence is stable-ID/revision-bound and unknown
      states prevent compliance.
- [ ] Reference classifications use a complete engine/build graph and supported
      exact syntaxes; text search is advisory only.
- [ ] Content completeness remains exclusively owned by content-audit.
- [ ] Stable findings and coverage rows preserve exact evidence and limitations.
- [ ] Verdict aggregation is deterministic and incomplete coverage can never
      become `COMPLIANT`.
- [ ] Full and summary paths are project-read-only and invoke no gate, specialist,
      recorder, or downstream workflow.
- [ ] Output conforms to `cgs.review-evidence/v1` plus
      `cgs.asset-audit-report/v1` under `cgs.asset-audit/v3`.

---

## Coverage Notes

Fixtures must distinguish adapter `FAIL` from `PARSE_ERROR`, unsupported syntax
from a parsed missing reference, advisory string matches from engine graph edges,
policy prohibition from missing license evidence, and incomplete inventory from a
proven-empty scope. Exact revisions and stable IDs are mandatory for every expected
conclusion.

Report persistence belongs to a separate recorder contract and is outside this
analyzer specification. The catalog entry points to this file, and its `last_*`
fields remain blank until an authorized test workflow actually executes every
case. Editing the contract/spec or running structural probes alone is not a test
pass and must not create a catalog result claim.
