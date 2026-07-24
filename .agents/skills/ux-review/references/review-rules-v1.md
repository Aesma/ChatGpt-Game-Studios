# UX review rules v1

This file is normative for `ux-review`. It is a reviewer contract, not an author
template. The current `ux-design` schema remains the authority for the artifacts
being reviewed.

## Contract identity

- Rules ID: `cgs.ux-review-rules/v1`
- Review extension: `cgs.ux-review/v2`
- Generic envelope: `cgs.review-evidence/v1`
- Author contract manifest: `cgs.ux-author-contract-manifest/v1`
- Supported author profile schema: `ux-profile-schema-v2`
- Supported author content profile: `cgs.ux-content-profile/v2`
- Batch schema: `cgs.ux-review-batch/v1`
- Worker schema: `cgs.ux-review-worker/v1`

## Author-contract compatibility gate

Read the exact current `ux-design` main and continuation sources specified by the
author itself. Compute their raw hashes and `author_schema_hash` as specified in
`SKILL.md`. Parse exactly one normative declaration for Profile Version, Content
Profile, Schema Version construction, artifact-type/profile routing, and each
stable section-ID set. Construct canonical
`cgs.ux-author-contract-manifest/v1` with:

```yaml
schema: cgs.ux-author-contract-manifest/v1
author_tool: ux-design
main: {path: <path>, sha256: <raw hash>}
continuation: {path: <path>, sha256: <raw hash>}
author_schema_hash: <NUL-delimited digest>
schema_version: ux-design-author-sha256:<same digest>
profile_version: <exact author declaration>
content_profile: <exact author declaration>
artifact_profiles:
  - {artifact_type, profile_id, stable_section_ids}
```

Sort artifact profiles by artifact type and keep stable section IDs in author
order, then compute `author_contract_manifest_sha256` over canonical JSON with
that hash field omitted. The author source declarations—not a reviewer filename
or legacy constant—supply the expected target values.

This reviewer version supports exactly the current author contract:

```text
profile_version: ux-profile-schema-v2
content_profile: cgs.ux-content-profile/v2
schema_version: ux-design-author-sha256:<computed current author_schema_hash>
```

Acceptance is strict, not open-ended. Continue to content review only when:

1. the author sources are readable and internally declare one coherent contract;
2. the declared profile/content pair is in the supported set above;
3. this rules file has a complete assertion matrix for every declared artifact
   profile and stable section ID; and
4. the target header's `Schema Version`, `Profile Version`, and `Content Profile`
   exactly equal the computed manifest values.

Missing/multiple/inconsistent author declarations, an unsupported author profile
or content version (including unsupported legacy `ux-profile-schema-v1`), assertion-matrix coverage
drift, or any target schema/profile/content/hash mismatch returns `MIGRATION
REQUIRED` with null verdict, expected/observed identities, author source hashes,
and the manifest hash when computable. Never fall back to v1, accept an arbitrary
manifest claim, substitute a remembered hash, or score content under mixed
contracts.

Compute `skill_bundle_sha256` from the exact UX-review `SKILL.md` bytes, one NUL
byte, exact `continued-workflow.md` bytes, one NUL byte, then exact
`review-rules-v1.md` bytes. Expose it as the generic producer version and in the
UX extension so consumers can detect reviewer-contract staleness.

## Fixed bounds

| Limit | Value |
|---|---:|
| Targets evaluated per batch | 8 |
| Context artifacts resolved per target | 16 |
| Exact context bytes loaded per target | 262144 |
| Requirement IDs in a denominator | 128 |
| Expert consultations per target | 1 |
| Paths per mutation-snapshot chunk | 256 |

Limits are certification limits, not permission to drop evidence. Overflow is
listed explicitly and makes the affected target or batch `PARTIAL`.

## Artifact profile matrix

| Artifact Type | Profile ID | Stable sections |
|---|---|---|
| `ux-spec` | `screen-spec` | `UXS-01` through `UXS-14` |
| `hud-design` | `hud` | `HUD-01` through `HUD-08` |
| `interaction-pattern-library` | `pattern-library` | `PAT-01` through `PAT-05` |

Every profile also requires all author-schema header fields applicable to that
type. A selector or filename does not select the profile.

## Common header assertions

Use these stable check keys for every target. “Present” always means substantive,
parseable content rather than a label alone.

| Check key | Assertion | Failure severity |
|---|---|---|
| `HDR-ARTIFACT-TYPE` | Artifact Type is present, recognized, and consistent with the routed profile. | `MAJOR` |
| `HDR-SCHEMA-VERSION` | Schema Version exactly matches the current author schema hash. | route error or migration |
| `HDR-PROFILE-VERSION` | Profile Version exactly matches the supported version declared by the current author-contract manifest. | route error or migration |
| `HDR-CONTENT-PROFILE` | Content Profile exactly matches the supported content contract declared by the current author-contract manifest. | route error or migration |
| `HDR-ARTIFACT-ID` | Artifact ID is a stable, non-placeholder ID. | `MAJOR` |
| `HDR-SCREEN-ID` | Screen ID is stable and non-placeholder when required by the author profile. | `MAJOR` |
| `HDR-STATUS` | Status is one of the author-schema states and is internally consistent. | `BLOCKING` |
| `HDR-AUTHOR-TASK` | Author Task ID is stable and non-placeholder. | `BLOCKING` |
| `HDR-LAST-UPDATED` | Last Updated UTC is parseable and not a template value. | `BLOCKING` |
| `HDR-PLATFORM-TARGET` | Platform Target is declared, but is treated only as a label. | `BLOCKING` |
| `HDR-PLATFORM-PROFILE` | Platform Profile contains an exact path and SHA-256 resolvable through the context manifest. | dependency gap |
| `HDR-ACCESSIBILITY` | Accessibility Foundation contains an exact path, SHA-256, and committed tier when applicable. | dependency gap |
| `HDR-REQUIREMENT-IDS` | Requirement IDs are stable IDs or an explicitly schema-permitted empty set with source-backed rationale. | denominator gap |
| `HDR-CONTEXT-MANIFEST` | Context Manifest SHA-256 resolves to the exact bounded manifest used by the author. | dependency gap |
| `HDR-AUTHORING-RECEIPT` | Authoring Receipt ID is stable and non-placeholder; READY_FOR_REVIEW must resolve its external current receipt path/hash from the supplied handoff/context evidence. | dependency gap |

`MISSING`, `EMPTY`, `PLACEHOLDER`, or `INVALID` never satisfies an assertion.
Foundation fields cannot use `NOT_APPLICABLE` unless the current author schema
explicitly permits it for that artifact profile and the rationale is supported
by a current stable source.

## Screen-spec assertions

| Check key | Required semantic content |
|---|---|
| `UXS-01-PURPOSE` | Player goal, intended outcome, and stable applicable requirement IDs. |
| `UXS-02-ARRIVAL` | Prior activity, carried state, pressure/context, and journey source. |
| `UXS-03-NAVIGATION` | Place in navigation hierarchy plus alternate/recovery access. |
| `UXS-04-ENTRY-EXIT` | Entry triggers, exits, carried state, cancellation, and irreversible effects. |
| `UXS-05-LAYOUT` | Required layout subheadings, information hierarchy, zones, component inventory, and current viewport/profile assumptions. |
| `UXS-06-STATES` | Default and every applicable loading, empty, populated, error, locked, and platform/input state; each omitted conditional state has source-backed N/A rationale. |
| `UXS-07-INTERACTION` | Stable component IDs, inputs, focus order, feedback, outcome, disabled behavior, and recovery. |
| `UXS-08-EVENTS` | Each applicable action maps to a stable event and payload, or cites current evidence that no event is required. |
| `UXS-09-TRANSITIONS` | Enter, exit, state transitions, interruption behavior, and reduced-motion behavior. |
| `UXS-10-DATA` | Data source, owner, read/write direction, update timing, null/late/error handling, and sensitivity where applicable. |
| `UXS-11-ACCESSIBILITY` | Requirements inherited from the exact committed accessibility tier, including non-color communication and focus/assistive behavior. |
| `UXS-12-LOCALIZATION` | String ownership, formatting, expansion/reflow, truncation/overflow policy, and locale-sensitive constraints. |
| `UXS-13-ACCEPTANCE` | Locally executable acceptance criteria, each mapped to stable requirement and component/state IDs. |
| `UXS-14-OPEN-QUESTIONS` | Stable question IDs, owner, state, next action, and blocking effect; an empty set must be explicit. |

All screen checks are required. Only individual conditional states or events may
be `NOT_APPLICABLE`, never an entire stable section.

## HUD assertions

| Check key | Required semantic content |
|---|---|
| `HUD-01-PHILOSOPHY` | Player need, information philosophy, attention budget, and governing requirement IDs. |
| `HUD-02-INFORMATION` | Requirement-linked information inventory with priority and always/contextual/hidden classification. |
| `HUD-03-ZONES` | Named layout zones with current platform, safe-zone, aspect, viewport, and attention assumptions. |
| `HUD-04-ELEMENTS` | Stable element IDs, data owner/source, visibility, update rule, interaction pattern, and complete applicable states. |
| `HUD-05-BEHAVIORS` | Context transitions, contention/priority rules, interruption, and reduced-motion behavior. |
| `HUD-06-VARIANTS` | Explicit behavior for every target and input modality declared by the current platform profile. |
| `HUD-07-ACCESSIBILITY` | Exact-tier requirements, non-color communication, focus/assistive behavior, and configurable assistance where required. |
| `HUD-08-OPEN-QUESTIONS` | Stable question IDs, owner, state, next action, and blocking effect; an empty set must be explicit. |

All HUD checks are required. A platform or input variant may be N/A only when the
resolved platform profile excludes it and that exact evidence is recorded.

## Pattern-library assertions

| Check key | Required semantic content |
|---|---|
| `PAT-01-OVERVIEW` | Scope, owner, consumers, current profile IDs/hashes, and governing requirements. |
| `PAT-02-CATALOG` | One canonical row per pattern with stable ID, name, category, version, status, and resolvable anchor. |
| `PAT-03-PATTERNS` | One owned definition per catalog row, including states, inputs, feedback, accessibility, use cases, and non-use cases. |
| `PAT-04-GAPS` | Stable proposed-gap IDs, source requirement IDs, owner, and disposition; an empty set must be explicit. |
| `PAT-05-OPEN-QUESTIONS` | Stable question IDs, owner, state, next action, and blocking effect; an empty set must be explicit. |

Catalog-to-definition coverage is bidirectional. An orphan row, missing row,
duplicate stable ID, unresolved anchor, or undocumented definition is `INVALID`.

## Content-state algorithm

For each header and profile check:

1. Locate the exact field/section by stable schema key, not fuzzy title matching.
2. If absent, emit `MISSING`.
3. If present but blank or structure-only, emit `EMPTY`.
4. If it contains template markers, `TODO`, `TBD`, sample/example-only data, or
   repeats the prompt without a concrete design decision, emit `PLACEHOLDER`.
5. If it is malformed, contradictory, uses unstable IDs, lacks required semantic
   elements, or cites unresolved/stale evidence, emit `INVALID`.
6. Emit `NOT_APPLICABLE` only for a conditional assertion with the exact source
   ID, path, hash, and rationale stored in `not_applicable_evidence`.
7. Emit `VALID` only after all required elements and evidence checks succeed.
8. Emit `UNEVALUATED` only when a declared bound or operational failure prevents
   completion; add the exact cause to `partial_reasons`.

A single section can yield multiple findings but has one aggregate assertion
state: `UNEVALUATED` first, then `MISSING`, `EMPTY`, `PLACEHOLDER`, `INVALID`,
`NOT_APPLICABLE`, and finally `VALID`.

## Dependency rules

Every dependency-ledger row contains:

```yaml
kind: platform-profile | accessibility-foundation | context-manifest |
      requirement-source | pattern-library | data-contract |
      performance-source | other
declared_reference: <verbatim path@hash[/tier] or stable ID>
resolved_path: <normalized project-relative path or null>
expected_sha256: <lowercase hex or null>
actual_sha256: <lowercase hex or null>
stable_ids: [<ids actually consumed>]
status: CURRENT | MISSING | UNREADABLE | STALE | CONTRADICTORY | OVERFLOW
```

- `Platform Profile` must resolve and its actual hash must equal the declared
  hash. Never substitute `Platform Target`, a spec header, a remembered platform,
  or a similarly named file.
- `Accessibility Foundation` must resolve, match the declared hash, and define
  the declared committed tier. Missing/stale/unreadable/tierless authority is a
  dependency gap. The target cannot be certified compliant or approved.
- The context-manifest hash must be current before its records can establish
  scope. Do not discover authority through an unbounded repository scan.
- When a required dependency exceeds a fixed bound, record `OVERFLOW`, mark the
  affected assertions `UNEVALUATED`, and return `PARTIAL`.

## Requirement denominator and coverage

Construct the denominator from two exact sets:

1. every stable requirement ID declared by the target; and
2. every current owner-approved UI/UX requirement in the bounded context manifest
   whose scope names the same stable `Artifact ID`, `Screen ID`, HUD identity, or
   pattern-library identity.

Normalize and deduplicate IDs without dropping provenance. For each denominator
ID store source path/hash, owner/approval state, scope match, target locations,
and coverage state:

```text
COVERED | DECLARED_NOT_TRACED | IN_SCOPE_NOT_DECLARED |
SOURCE_MISSING | SOURCE_STALE | CONFLICTING | UNEVALUATED
```

An ID is `COVERED` only when current source semantics are implemented in a
specific compatible target section, state, interaction, or acceptance criterion.
The header list alone is not coverage. Product behavior with no current source ID
is an `UNSOURCED-BEHAVIOR` finding. If source discovery or scope membership is
incomplete, the denominator is incomplete and the run is `PARTIAL`.

Record:

```yaml
denominator_count: <integer>
covered_count: <integer>
coverage_ratio: <covered/denominator or null when incomplete>
denominator_complete: <boolean>
```

Zero divided by zero is not proof of full coverage. Use `coverage_ratio: null`
and require current source-backed evidence that the applicable set is empty.

## Perceived response versus runtime performance

UX assertions may require visible acknowledgement, progress/status feedback,
input-lock semantics, cancellation, recovery, optimistic-state correction, and
clear perceived-response behavior. They do not impose a generic `X ms` budget.

A numeric runtime budget is evaluable only when the target cites an exact current
technical/performance stable ID and source path/hash that defines platform,
hardware class, scenario, metric, and threshold. If such a requirement is needed
for an acceptance claim but its evidence is unavailable, add
`NEEDS-PERFORMANCE-EVIDENCE`, mark the assertion `UNEVALUATED`, and return
`PARTIAL`. Direct measurement belongs to the performance/technical owner; this
review only verifies the source-bound UX contract.

## Findings and stable identity

Finding severity is exactly `MAJOR`, `BLOCKING`, or `ADVISORY`. Finding state is
exactly `OPEN`, `ACCEPTED_RISK`, `RESOLVED`, `REGRESSED`, or `SUPERSEDED`.

Build a fingerprint from:

```text
artifact stable ID + profile ID + check key + stable subject ID + normalized
defect class
```

Do not include byte hashes, line numbers, prose wording, or timestamps in the
fingerprint. Set the finding ID to:

```text
UXF-<sanitized-artifact-id>-<check-key>-<first-8-of-sha256(fingerprint)>
```

Each finding stores the fingerprint, target hash, exact evidence location,
evidence hash where applicable, expected assertion, observed state, consequence,
remediation, severity, state, and prior finding ID when converging. Findings may
share a check key only when their stable subject IDs differ.

Default severity:

- `MAJOR`: wrong artifact/profile identity, invalid stable foundation, missing
  player goal, missing owner-approved governing behavior, unresolved navigation,
  or an unowned cross-screen/global pattern.
- `BLOCKING`: any other failed required semantic assertion, incomplete state,
  untraced requirement with otherwise complete sources, or invalid N/A.
- `ADVISORY`: a non-required improvement with no failed requirement.

Dependency, denominator, reviewer, budget, mutation-guard, or evidence-conflict
gaps additionally force `PARTIAL`; retain the best-supported finding severity.

Accepted risk requires `risk_id`, owner, rationale, bounded scope, acceptance
authority, accepted-at timestamp, and expiry or review trigger. It remains open
for verdict purposes and cannot produce `APPROVED`.

## Convergence rules

The prior record must be a persistently readable `cgs.review-evidence/v1`
envelope with a `cgs.ux-review/v2` extension, a valid canonical record ID, the
same target path and stable artifact ID, an exact prior target hash, and the
author schema hash, author contract manifest hash, profile version, and content
profile used in that run. Reject malformed, unrelated, self-authored, or
hash-inconsistent evidence with `ERROR`. If the prior record used a different
otherwise valid author contract, do not compare findings across schemas: return
`MIGRATION REQUIRED` with null verdict until a separately evidenced artifact/
review migration supplies compatible current bytes.

Evaluate prior `OPEN` and `ACCEPTED_RISK` findings before new checks. Compare the
prior exact target bytes to current bytes through reproducible version-control or
archived-byte evidence. Then check changed stable sections and their current
cross-references for regressions. Record each prior finding as:

- `OPEN`: same fingerprint and defect remains;
- `RESOLVED`: assertion is now valid and no equivalent defect remains;
- `REGRESSED`: it was resolved but the same fingerprint recurred;
- `SUPERSEDED`: current schema intentionally replaces the assertion, with exact
  schema evidence and successor finding/check ID.

Do not close a finding merely because text moved, wording changed, or an owner
accepted the risk. If exact diff evidence is unavailable, convergence is
incomplete and the run is `PARTIAL`.

## Expert consultation

At `standard` depth, consultation status is `NOT_REQUESTED` and is complete. At
`expert` depth, dispatch exactly one bounded reviewer with:

```yaml
schema: cgs.ux-review-worker/v1
run_id: <run ID>
target_path: <normalized path>
target_sha256: <hash>
artifact_id: <stable ID>
profile_id: <profile>
author_schema_hash: <hash>
author_contract_manifest_sha256: <hash>
profile_version: ux-profile-schema-v2
content_profile: cgs.ux-content-profile/v2
assigned_check_keys: [<subjective quality checks>]
evidence_paths_and_hashes: [<bounded exact sources>]
constraints:
  may_write: false
  may_decide_verdict: false
```

Accept only:

```yaml
schema: cgs.ux-review-worker/v1
status: DONE | DECLINED | TIMEOUT | ERROR
target_sha256: <same hash>
evaluations: [{check_key, state, evidence, rationale}]
candidate_findings: [{check_key, stable_subject_id, defect_class, severity,
                      evidence, rationale}]
```

Any non-`DONE` status, malformed output, out-of-scope claim, target mismatch, or
unresolved evidence conflict makes the run `PARTIAL`. The lead independently
normalizes all candidate findings and owns the final verdict.

## Single-target output schema

Return this complete envelope in the conversation:

```yaml
schema: cgs.review-evidence/v1
record_id: sha256:<canonical SHA-256 over the normalized record with record_id omitted>
artifact_id: ux:<stable Artifact ID>
artifacts:
  - {role: target, path: <path>, sha256: <hash>, source_id: <Artifact ID>}
  - {role: author-schema-main, path: <path>, sha256: <hash>, source_id: null}
  - {role: author-schema-continuation, path: <path>, sha256: <hash>, source_id: null}
  - {role: dependency, path: <path>, sha256: <hash>, source_id: <stable ID or null>}
reviewer: ux-review:<run-id>
verdict: APPROVED | NEEDS REVISION | MAJOR REVISION NEEDED | PARTIAL
timestamp: <ISO-8601 UTC with fractional seconds>
finding_ids: [<all finding IDs>]
producer:
  tool: ux-review
  version: sha256:<ordered main/continuation/ruleset bundle digest>
extension:
  schema: cgs.ux-review/v2
  run_id: <stable run ID>
  target:
    path: <path>
    sha256: <hash>
    artifact_id: <ID>
    screen_id: <ID or null>
    artifact_type: <type>
  routing:
    selector: <exact selector>
    profile_id: screen-spec | hud | pattern-library
    profile_version: ux-profile-schema-v2
    content_profile: cgs.ux-content-profile/v2
    author_schema_hash: <hash>
    author_contract_manifest_sha256: <hash>
    author_contract_support_status: SUPPORTED
    skill_bundle_sha256: <hash>
    review_depth: standard | expert
  dependency_ledger: [<complete rows>]
  requirement_coverage:
    denominator_complete: <boolean>
    denominator_count: <integer>
    covered_count: <integer>
    coverage_ratio: <number or null>
    rows: [<complete coverage rows>]
  assertion_results:
    - {check_key: <key>, state: <state>, evidence: <locations/hashes>,
       not_applicable_evidence: <object or null>}
  consultation:
    status: NOT_REQUESTED | DONE | DECLINED | TIMEOUT | ERROR
    reviewer_count: <0 or 1>
    evidence_conflicts: [<conflicts>]
  convergence:
    requested: <boolean>
    prior_record_id: <ID or null>
    prior_target_sha256: <hash or null>
    diff_evidence: <exact source or null>
    prior_findings: [{finding_id, fingerprint, disposition, successor_id}]
    regression_checks: [<changed-section/cross-reference checks>]
  findings: [<complete finding objects>]
  accepted_risk_refs: [<complete risk objects>]
  partial_reasons: [<bounded exact causes>]
  mutation_guard:
    before_root: <streaming tree hash>
    after_root: <streaming tree hash>
    status: UNCHANGED | CHANGED | INCOMPLETE
  approval_status: APPROVED | NOT_APPROVED
  gate_evidence_status: NOT_PERSISTED
  gate_evidence_eligible: false
```

On routing/invocation/schema identity failure, return an error object with
`schema`, target/selector evidence, error code, and remediation; set `verdict:
null` and do not forge the complete review envelope.

## Batch output schema

```yaml
schema: cgs.ux-review-batch/v1
run_id: <run ID>
selector: all | hud | patterns
manifest_sha256: <hash of sorted manifest rows>
limits: {targets_per_batch: 8}
status: COMPLETE | PARTIAL | ERROR
targets:
  - {path, sha256, artifact_id, artifact_type,
     review_record_id, verdict, status: REVIEWED | ERROR}
unchecked:
  - {path, sha256, artifact_type_or_unknown, reason: LIMIT_REACHED | DEPENDENCY_OVERFLOW}
summary_counts: {reviewed, errors, unchecked}
gate_evidence_status: NOT_PERSISTED
gate_evidence_eligible: false
```

The batch schema has no `APPROVED` aggregate. Each reviewed target receives its
own complete generic envelope and verdict.

## Verdict and gate rules

Apply the deterministic precedence in `SKILL.md`. `PARTIAL` means review
certification is incomplete; it is not a weaker approval. A separate recorder
may persist a record only after recalculating its canonical ID and every artifact
hash. Until then, and for every output produced directly by this skill:

```text
gate_evidence_status = NOT_PERSISTED
gate_evidence_eligible = false
```
