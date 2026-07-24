# Security-audit rules v1

This file is normative for `security-audit`.

## Contract identity

- Rules schema: `cgs.security-audit-rules/v1`
- Threat scope: `cgs.security-threat-scope/v1`
- Tool receipt: `cgs.security-tool-receipt/v1`
- Manual-flow receipt: `cgs.security-manual-flow/v1`
- Reviewer packet: `cgs.security-review-worker/v1`
- Generic envelope: `cgs.review-evidence/v1`
- Security extension: `cgs.security-audit/v2`
- Project severity model: `CGS-SEC-IEX/v1`

Compute `skill_bundle_sha256` over exact `SKILL.md` bytes, one NUL byte, exact
`continued-workflow.md` bytes, one NUL byte, then exact `audit-rules-v1.md` bytes.

## Fixed bounds

| Limit | Value |
|---|---:|
| Configured source roots | 16 |
| Manifest traversal depth per root | 16 |
| Eligible source/config files | 256 |
| Exact bytes per source/config file | 1048576 |
| Exact bytes across scanned source/config | 16777216 |
| Threat boundaries/assets/actors each | 64 |
| Threat entry points and data/authority flows each | 256 |
| Planned checks | 256 |
| Executed tool receipts | 64 |
| Component inventory entries | 1024 |
| Advisory matches | 1024 |
| Required reviewers | 2 |
| Attempts per reviewer | 1 |
| Tool/reviewer deadline | 120 seconds each |
| Paths per mutation-snapshot chunk | 256 |

Overflow is never silent sampling. Retain discoverable identities as
`UNCHECKED_LIMIT`, set affected coverage `UNVERIFIED`, and return `PARTIAL` when
at least one meaningful check ran. If no meaningful target/check exists, return
`ERROR`.

## Profile matrix

| Profile | Required categories |
|---|---|
| `full` | target/build identity; threat model; save/serialization; network/backend when configured; external input; secrets/exposure; cheat/authority; dependencies/supply chain; build/release; engine/platform-specific boundaries |
| `network` | target/build identity; threat model; network/backend authority, authentication, validation, abuse/rate limits; secrets/exposure; relevant dependencies; relevant build/export/platform configuration |
| `save` | target/build identity; threat model; serialization/parser bounds; path handling; integrity/authenticity; confidentiality only for classified sensitive data; rollback/authority/cheat exposure when applicable; local platform storage |
| `input` | target/build identity; threat model; untrusted player/file/IPC/network/platform inputs through validation/authority boundaries to file/log/network/backend/parser/dynamic-code sinks |
| `quick` | exact enumerated high-confidence checks only; no full-profile equivalence, release evidence, or full-finding closure |

Profile selection establishes the category denominator. Threat evidence decides
whether a conditional category is applicable. Do not drop a required category
because its files were not found.

## Target and scope states

Manifest entries use:

```text
IN_SCOPE | EXCLUDED | UNREADABLE | DENIED_CATEGORY_ONLY | OVERSIZE |
PARSER_UNSUPPORTED | ADAPTER_UNSUPPORTED | UNCHECKED_LIMIT | ERROR
```

Coverage categories use:

```text
CHECKED_WITH_FINDINGS | CHECKED_NO_FINDINGS | NOT_APPLICABLE |
UNVERIFIED | UNSUPPORTED
```

- `UNVERIFIED` means required evidence is missing, stale, failed, timed out,
  unauthorized, incomplete, changed, or ambiguous.
- `UNSUPPORTED` means the current engine/language/platform/ecosystem/file type has
  no compatible declared adapter/tool/manual evidence method.
- `NOT_APPLICABLE` requires positive current evidence proving the category absent
  from the threat scope.

Both `UNVERIFIED` and `UNSUPPORTED` fail closed to `PARTIAL`. Unsupported is not
evidence that a vulnerability exists and must not be presented as one.

## Threat-scope schema

Freeze before checks:

```yaml
schema: cgs.security-threat-scope/v1
scope_id: sha256:<canonical payload>
profile: full | network | save | input | quick
target:
  repository_id: <canonical identity>
  commit: <commit/ref or null>
  dirty_state: clean | dirty | includes-untracked | unknown
engine_platform:
  engine: <exact configured value or null>
  engine_version: <version plus source path/hash or null>
  language: <configured values>
  target_platforms: [<platform plus source path/hash>]
  build_export_profiles: [{id, path, sha256, status}]
  online_backend_features: [{id, evidence, status}]
  mods_plugins: [{id, trust, evidence}]
assets:
  - {asset_id, classification: public | local-sensitive | credential |
     player-pii | monetization | competitive-authority | release-signing,
     owner, evidence_path, evidence_sha256}
actors:
  - {actor_id, trust, capabilities, access_preconditions, evidence}
boundaries:
  - {boundary_id, from_zone, to_zone, authority_owner, validation_owner,
     transport_or_storage, evidence}
entry_points:
  - {entry_id, actor_id, boundary_id, source_symbol, target_path,
     target_sha256, data_classes}
flows:
  - {flow_id, source, validator_or_authority, sink, boundaries, data_classes,
     target_paths_and_hashes, state: CONFIRMED | ASSUMED | UNKNOWN}
abuse_goals: [{goal_id, actor_id, asset_id, effect, evidence}]
category_applicability:
  - {category, required_by_profile, state: APPLICABLE | NOT_APPLICABLE |
     UNKNOWN | UNSUPPORTED, evidence, rationale}
assumptions: [{id, statement, evidence, expiry_or_validation_trigger}]
unresolved: [{id, subject, evidence_gap, affected_categories}]
```

IDs are stable within project scope. Every evidence reference includes exact path
and hash; denied secret/environment scope is recorded only as a category-level
permission gap without a protected path or value.

Threat-scope completeness requires all profile categories, configured platforms,
authority owners, sensitive asset classes, and declared online/backend/build
features to have an explicit state. Missing engine/platform configuration is not
proof of a generic project; affected semantics are `UNKNOWN` or `UNSUPPORTED`.

## Bounded manifests

Each source/build/config row contains canonical allowed path, exact SHA-256, byte
size, language/type, owner-approved classification evidence, applicable threat
categories, and state. A `DENIED_CATEGORY_ONLY` row instead has `path: null`, no
path hash, and only a stable category-level gap ID. Do not read or name denied
paths. Do not follow links outside root.

Generated/vendor/binary/build exclusions require an exact current rule, committed
marker, or manifest record. A directory name alone does not prove exclusion.
Binary/build artifacts are evidence only when supplied and hashable; the audit
does not create them.

Hash canonical sorted rows to produce:

- `source_scope_manifest_hash`;
- `build_config_manifest_hash`;
- `component_inventory_hash`; and
- `check_plan_hash`.

The check plan maps every required category and in-scope manifest subset to a
compatible adapter/evidence method before execution. Any unchecked planned row is
a coverage gap.

## Engine/platform adapter routing

An adapter record is usable only with:

```yaml
adapter_id: <stable ID>
adapter_version: <version>
source_path: <current owner-approved registry path>
source_sha256: <hash>
engine_ranges: [<exact constraints>]
languages_or_types: [<types>]
platforms: [<platforms>]
categories: [<threat categories>]
capabilities: [SAST | DATAFLOW | SECRET_SAFE | DEPENDENCY_INVENTORY |
               ADVISORY_MATCH | BUILD_CONFIG | MANUAL_SEMANTICS]
tool_and_rule_requirements: [{tool, version_constraint, rulepack_id,
                              configuration_id}]
side_effect_contract: READ_ONLY | MUTATING | UNKNOWN
reviewer_role: <configured exact role or null>
```

Match all declared dimensions. `MUTATING`/`UNKNOWN` adapters are not executed.
An engine name alone does not make an adapter compatible. If no compatible
adapter exists for an applicable category/type/platform, mark it `UNSUPPORTED`.

Read configured Engine Specialists and exact routing notes. The globally defined
`security-engineer` supplies security-domain review. A configured Primary or
specialist supplies engine/platform semantics only when the adapter or project
routing assigns that exact role. Never derive a role from filename heuristics.

## Tool receipt schema

Every executed VCS/scanner/parser/SBOM/advisory/config check produces:

```yaml
schema: cgs.security-tool-receipt/v1
receipt_id: <stable run-local ID>
check_id: <planned stable check ID>
category: <category>
adapter: {id, version, source_path, source_sha256}
tool: {executable, version, binary_sha256_or_install_identity}
argv_redacted: [<arguments with no secret material>]
cwd: <canonical project-relative directory>
rulepack: {id, version, path, sha256}
configuration: {path, sha256}
target_subset: [{path, sha256}]
target_subset_hash: <hash>
started_at: <ISO-8601 UTC>
ended_at: <ISO-8601 UTC>
deadline_seconds: 120
exit_code: <integer or null>
timed_out: <boolean>
counts: {eligible_files, scanned_files, excluded_files, unsupported_files,
         failed_files, eligible_bytes, scanned_bytes, findings}
result_sha256: <hash of secret-safe normalized result or null>
redacted_log_sha256: <hash or null>
unsafe_raw_log_hmac: <truncated volatile-key HMAC only if quarantined, else null>
side_effects: {expected: none, observed: none | changed | unknown}
status: PASS | FINDINGS | PARTIAL | ERROR | UNSUPPORTED
```

Never expose a raw log that contains or may contain a secret. A tool configured
to emit raw matched values is ineligible. If unexpected raw secret material is
received, quarantine it in volatile memory, emit no raw content/plain digest,
optionally emit only the volatile-key HMAC, destroy the key, and mark the check
`PARTIAL` with unsafe-output coverage.

Receipt validity requires known compatible versions/rules/configuration, exact
input hashes, non-mutating execution, successful/defined exit semantics, complete
counts, and hashes. Discussion, planned commands, copied terminal prose, unknown
version, stale input, timeout, unexplained nonzero exit, zero scanned eligible
files, parser loss, or missing redacted log/result hash is not passing evidence.

## Manual-flow receipt schema

```yaml
schema: cgs.security-manual-flow/v1
receipt_id: <ID>
reviewer: <role/run identity>
profile: <profile>
threat_scope_hash: <hash>
check_id: <planned check>
target_artifacts: [{path, sha256}]
source: {symbol_or_structural_id, redacted_location, actor, data_class}
validation_or_authority:
  {symbol_or_structural_id, redacted_location, owner, rule, failure_behavior}
sink: {symbol_or_structural_id, redacted_location, effect, authority_zone}
boundaries: [<stable boundary IDs>]
reasoning: <secret-safe evidence reasoning>
evidence_class: CONFIRMED | SUPPORTED | CANDIDATE
confidence: HIGH | MEDIUM | LOW
reviewed_at: <ISO-8601 UTC>
```

`CANDIDATE` or a generic keyword cannot support a vulnerability or a
`CHECKED_NO_FINDINGS` conclusion. It may only identify follow-up scope. A manual
receipt never substitutes for a tool/data-flow capability when the check plan
requires that capability.

## Dependency and advisory evidence

Component rows require name, exact version or immutable digest, ecosystem,
source path/hash, derivation receipt, dependency relationship, and match
confidence. A package filename without parsed version evidence is incomplete.

Advisory matching requires:

```yaml
provider: <name>
scanner_version: <version>
snapshot_id: <immutable ID>
snapshot_sha256: <hash>
snapshot_timestamp: <ISO-8601 UTC>
freshness_policy: {source_path, source_sha256, maximum_age, satisfied}
query_receipt_id: <valid tool receipt>
matches:
  - {component_id, advisory_id, ecosystem, affected_range,
     installed_version_or_digest, range_reasoning,
     provider_cvss: {version, vector, score} | null}
```

No lockfile/SBOM, incomplete component inventory, unsupported ecosystem, absent/
stale/unhashable snapshot, denied network without local snapshot, missing
freshness policy, incomplete version-range match, timeout, or invalid receipt is
`UNVERIFIED` or `UNSUPPORTED`. It never supports “none” or “no known CVEs.”

A valid zero-match statement must name the exact inventory hash, snapshot ID/
hash/timestamp, freshness policy, scanner version, and receipt. It remains scoped
historical evidence.

## Secret-safe evidence contract

Secret detection output may contain only:

```yaml
secret_type: <classification>
path: <normalized allowed project path>
line: <integer>
column: <integer or null>
structural_anchor: <non-secret stable symbol/node ID>
rule_id: <scanner rule>
target_sha256: <source hash>
confidence: HIGH | MEDIUM | LOW
run_correlation_hmac: <truncated volatile-key HMAC or null>
```

Prohibited fields include value, source line/context, match length, entropy,
prefix/suffix, encoding, plaintext digest, reversible representation, volatile
key, raw command output, and protected denied path. Finding identity is derived
from rule, secret type, normalized allowed path, and structural anchor—not value,
HMAC, or line.

Containment text may recommend revoke/rotate, restrict distribution, and inspect
history/downstream logs through separately authorized operations. The audit
never performs or records completion of those actions.

## Evidence confidence and finding admission

- `CONFIRMED`: complete compatible tool dataflow/reproduction evidence or exact
  manual authority/source→sink proof.
- `SUPPORTED`: multiple current compatible evidence elements establish the
  vulnerable path but no safe runtime reproduction is appropriate/available.
- `CANDIDATE`: heuristic/keyword/partial evidence identifies review scope only.

Only `CONFIRMED` and `SUPPORTED` create findings. `CANDIDATE` remains a coverage
item. Confidence (`HIGH|MEDIUM|LOW`) states evidence certainty and does not change
impact/exploitability/exposure or raise severity.

## Project severity: CGS-SEC-IEX/v1

This is a project triage model, not CVSS.

Choose exactly one evidence-backed value per dimension:

### Impact (I)

| Value | Meaning |
|---:|---|
| 0 | no demonstrated security impact |
| 1 | limited nuisance/non-sensitive local effect |
| 2 | bounded confidentiality, integrity, availability, or cheat impact |
| 3 | material player/PII/monetization/competitive or service impact |
| 4 | systemic authority compromise, credential/signing compromise, RCE, or catastrophic service/data impact |

### Exploitability (E)

| Value | Meaning |
|---:|---|
| 0 | no executable abuse path established |
| 1 | theoretical, fragile, or exceptional prerequisites |
| 2 | privileged/local access or complex chained conditions |
| 3 | repeatable with normal user/client access or limited interaction |
| 4 | repeatable low-complexity unauthenticated or broadly client-controlled path |

### Exposure (X)

| Value | Meaning |
|---:|---|
| 0 | test/development-only path excluded from shipped/runtime scope by current build evidence |
| 1 | local single-user or tightly restricted administrative scope |
| 2 | authenticated/limited online, shared-device, mod/plugin, or distributed client scope |
| 3 | internet/public/backend/platform boundary or untrusted client-to-authority scope |

Calculate `score = I × E × X` (range 0–48):

| Score | Project severity |
|---:|---|
| 36–48 | `CRITICAL` |
| 24–35 | `HIGH` |
| 10–23 | `MEDIUM` |
| 1–9 | `LOW` |
| 0 | `INFO` |

Record each factor and evidence. Multiplayer, monetization, PII, platform, or
public context influences only the chosen documented I/E/X value; there is no
post-calculation bump. If any required factor is unknown or unsupported, severity
is `UNRATED` and severity coverage is partial.

External advisory CVSS is separate metadata. Preserve only a provider-supplied
exact CVSS version/vector/score. Never call IEX “CVSS-like” in evidence, fabricate
missing CVSS, translate scores between CVSS versions, or use advisory CVSS alone
as project exploitability/severity.

## Stable findings

Fingerprint material is:

```text
stable rule/check ID + category + canonical allowed target path + stable source
and sink/authority/structural IDs + normalized defect class
```

Exclude title, prose, line/column, hashes, secret/HMAC, timestamp, profile,
reviewer, confidence, and severity. Finding ID is:

```text
SEC-<CATEGORY>-<first-12-of-SHA256(fingerprint)>
```

Finding shape:

```yaml
finding_id: <stable ID>
fingerprint: <full hash>
lifecycle_observation: OPEN | STILL_OPEN | CANDIDATE_RESOLVED | REGRESSED |
                       SUPERSEDED | UNVERIFIED
evidence_class: CONFIRMED | SUPPORTED
confidence: HIGH | MEDIUM | LOW
category: <category>
defect_class: <stable class>
threat_scope_hash: <hash>
targets: [{path, sha256, structural_id, redacted_location}]
trust_boundaries: [<IDs>]
source_validator_sink: <secret-safe IDs/evidence>
severity_model: CGS-SEC-IEX/v1
severity_factors: {impact, exploitability, exposure, evidence}
severity_score: <0..48 or null>
severity: CRITICAL | HIGH | MEDIUM | LOW | INFO | UNRATED
external_advisories: [{id, provider, provider_cvss_or_null}]
tool_or_manual_receipt_ids: [<IDs>]
owner: <security/remediation owner>
containment: <bounded recommendation>
remediation: <bounded requirement>
closure_condition: <testable current-evidence condition>
risk_acceptance_ref: <exact immutable record or null>
```

Discovery never emits `RESOLVED` or changes an external lifecycle record.

## Risk-acceptance admission

An existing risk record is referenceable only with:

- finding ID and fingerprint;
- exact target commit/build/source-scope/threat-scope hashes;
- approver identity and independently verifiable security/product authority;
- rationale, bounded affected scope, compensating controls;
- signed acceptance timestamp and immutable record hash;
- expiry timestamp or objective review trigger; and
- originating audit record ID.

Expired, scope/hash-mismatched, unsigned, self-authored, ordinary acknowledged,
or authority-unverifiable records are invalid. The audit cannot create/modify
acceptance. A valid reference does not erase the finding, change IEX severity,
make incomplete coverage complete, or change `FINDINGS` to no findings.

## Bounded reviewer policy

Reviewer candidates:

1. `security-engineer` — required for `full`, `network`, `save`, and `input`;
   not required for `quick`.
2. One exact configured engine/platform specialist — required only when an
   applicable planned manual-semantics check names that role and no compatible
   deterministic evidence covers it.

Total cap is two, one attempt each, 120 seconds each. Dispatch required candidates
in one parallel batch. The repository-authorized pre-dispatch unavailable-role
fallback may satisfy `security-engineer` only if the current agent produces all
assigned valid manual-flow receipts. A dispatched timeout/blocked/error does not
silently fall back. Engine/platform roles never fall back to an invented role.

Reviewer statuses:

```text
DONE | DONE_LOCAL_FALLBACK | NOT_REQUIRED | NOT_DISPATCHED_LIMIT |
UNAVAILABLE | DECLINED | BLOCKED | TIMEOUT | ERROR | INVALID_RESPONSE |
UNSAFE_OUTPUT
```

Reviewer packet/response:

```yaml
schema: cgs.security-review-worker/v1
run_id: <run ID>
role: <role>
profile: <profile>
target_manifest_hash: <hash>
threat_scope_hash: <hash>
assigned_checks: [<IDs>]
targets: [{path, sha256, structural IDs only}]
boundaries_and_flows: [<secret-safe IDs>]
constraints: {read_only: true, no_secret_values: true,
              may_decide_outcome: false, may_accept_risk: false}
status: <status>
manual_flow_receipts: [<cgs.security-manual-flow/v1>]
candidate_scope_gaps: [<redacted evidence>]
```

Malformed schema, manifest/scope mismatch, secret/raw-source leakage, unsupported
claim, or non-DONE required status makes reviewer coverage partial. Reviewer prose
without valid receipts is advisory only.

## Re-audit and convergence

Prior input must be one immutable persisted `cgs.review-evidence/v1` envelope with
a `cgs.security-audit/v2` extension, canonical record ID, exact prior target/source/
threat/build/tool/advisory identities, stable finding fingerprints, and a relation
to the same project. A conversation copy may guide diagnostics but cannot prove
lifecycle convergence.

Evaluation order:

1. validate prior identity and bytes;
2. reproduce exact prior→current source/build/config diff evidence;
3. evaluate every prior OPEN or accepted-risk-referenced finding against its exact
   closure condition;
4. inspect changed trust boundaries, authority, assets, entry points, flows,
   dependencies, and build/export/platform state;
5. run the current profile's complete check plan; and
6. reuse fingerprints/IDs and record dispositions.

Dispositions:

- `STILL_OPEN`: same defect remains;
- `CANDIDATE_RESOLVED`: current audit evidence meets closure condition, pending
  independent remediation/test/lifecycle authority;
- `REGRESSED`: a previously closed/superseded defect fingerprint recurs;
- `SUPERSEDED`: current authoritative rule/schema replaces it with exact successor;
- `UNVERIFIED`: closure/diff evidence is incomplete.

Quick profile may evaluate explicitly listed high-confidence checks and prior IDs,
but every result remains quick. It cannot claim the full finding set closed, turn
prior full coverage current, or satisfy release evidence. Full-profile convergence
requires a current complete full audit.

## Coverage ledger and outcome

Report these dimensions independently:

```yaml
target_identity: COMPLETE | PARTIAL | ERROR
threat_scope: COMPLETE | PARTIAL
source_build_manifest: COMPLETE | PARTIAL
engine_platform_routing: COMPLETE | PARTIAL | NOT_APPLICABLE
checks_tools: COMPLETE | PARTIAL
dependencies_advisories: COMPLETE | PARTIAL | NOT_APPLICABLE
reviewers: COMPLETE | PARTIAL | NOT_APPLICABLE
redaction: COMPLETE | PARTIAL | ERROR
re_audit: COMPLETE | PARTIAL | NOT_APPLICABLE
mutation_guard: COMPLETE | PARTIAL | ERROR
```

Every dimension includes planned/covered/unsupported/unverified counts and exact
secret-safe gap IDs. Category coverage includes all profile categories and their
states.

Outcome precedence:

| Condition | Outcome |
|---|---|
| invalid target/scope identity, global evidence/redaction failure, or zero meaningful checks | `ERROR` |
| one or more meaningful checks plus any required partial dimension, `UNVERIFIED`, or `UNSUPPORTED` category | `PARTIAL` |
| complete required coverage and one or more findings | `FINDINGS` |
| complete required coverage and zero findings | `NO_FINDINGS_IN_SCANNED_SCOPE` |

`PARTIAL` preserves confirmed findings and severity. It never becomes a no-finding
or approval conclusion.

## Review-evidence output

For a valid meaningful scope return:

```yaml
schema: cgs.review-evidence/v1
record_id: sha256:<canonical normalized payload with record_id omitted>
artifact_id: security-audit:<first-16-of-source-scope-manifest-hash>
artifacts:
  - path: <canonical allowed path>
    sha256: <complete hash>
    role: source | build-config | build-artifact | threat-source |
          engine-platform-config | adapter | rulepack | tool-receipt |
          component-source | advisory-snapshot | prior-review
    source_id: <stable ID or null>
reviewer: security-audit:<run-id>
verdict: NO_FINDINGS_IN_SCANNED_SCOPE | FINDINGS | PARTIAL
timestamp: <ISO-8601 UTC with fractional seconds>
finding_ids: [<stable SEC IDs>]
producer:
  tool: security-audit
  version: sha256:<skill_bundle_sha256>
extension:
  schema: cgs.security-audit/v2
  run_id: SEA-<compact UTC>-<scope12>-<UUIDv4>
  project_id: <canonical repository identity>
  profile: full | network | save | input | quick
  source_revision: {commit: <commit or null>, dirty_state: <state>, vcs_receipt_id: <ID>}
  hashes:
    source_scope_manifest: <hash>
    build_config_manifest: <hash or null>
    component_inventory: <hash or null>
    threat_scope: <hash>
    check_plan: <hash>
    skill_bundle: <hash>
  stale_key: <digest of project/profile/revision/manifests/scope/adapters/tools/rules/advisory/reviewers>
  limits: <all effective fixed limits>
  threat_scope: <complete cgs.security-threat-scope/v1>
  manifests: {source_config: [<rows>], build: [<rows>], components: [<rows>]}
  routing: {engine_platform_sources: [<path/hash>], adapters: [<rows>], reviewers: [<rows>]}
  check_plan: [<planned check rows>]
  tool_receipts: [<cgs.security-tool-receipt/v1 rows>]
  manual_flow_receipts: [<cgs.security-manual-flow/v1 rows>]
  advisory_evidence: <complete record or gap>
  category_coverage: [{category, state, planned, covered, unsupported,
                       unverified, gap_ids}]
  coverage_dimensions: <complete ledger>
  findings: [<complete secret-safe findings>]
  risk_acceptance_refs: [<validated immutable references>]
  re_audit:
    requested: <boolean>
    prior_record_id: <ID or null>
    prior_profile: <profile or null>
    diff_evidence: <exact evidence or null>
    dispositions: [{finding_id, fingerprint, disposition, evidence}]
    current_attack_surface_checks: [<IDs>]
  mutation_guard:
    before_root: <hash>
    after_root: <hash>
    status: UNCHANGED | CHANGED | INCOMPLETE
    changed_paths_redacted: [<safe rows>]
  outcome: <same as generic verdict>
  confirmed_findings_present: <boolean>
  partial_reasons: [<secret-safe gap IDs/evidence>]
  gate_evidence_status: NOT_PERSISTED
  gate_evidence_eligible: false
  disclaimer: NOT A SHIP/RELEASE APPROVAL
```

Secret values, protected denied paths, raw source context, and unsafe logs never
appear in `artifacts` or the extension. The record becomes stale on any relevant
revision/manifest/threat/adapter/tool/rule/advisory/reviewer-contract change.

On input/global identity `ERROR`, return a bounded redacted error object with
schema, error/gap IDs, profile, safe root-containment evidence, and remediation.
Set `verdict: null`; do not forge a complete review envelope.
