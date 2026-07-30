# Scope-check rules v1

Treat revisions as supplied metadata; never calculate them from file content. Use stable business IDs, canonical paths, schema versions, explicit revisions, and UTC run IDs.

This file is normative for `scope-check`.

## Contract identity

- Rules schema: `cgs.scope-check-rules/v1`
- Baseline schema: `cgs.scope-baseline/v1`
- Current manifest schema: `cgs.scope-current/v1`
- Evidence manifest schema: `cgs.scope-evidence-manifest/v1`
- Change decision schema: `cgs.scope-change-decision/v1`
- Risk acceptance schema: `cgs.scope-risk-acceptance/v1`
- Re-baseline decision schema: `cgs.scope-rebaseline/v1`
- Generic envelope: `cgs.review-evidence/v1`
- Scope-check extension: `cgs.scope-check/v2`

Record the explicit `skill_bundle_revision` supplied for the declared versions of `SKILL.md`, `continued-workflow.md`, and `scope-rules-v1.md`.

## Fixed limits

| Limit | Value |
|---|---:|
| Core comparison artifacts | 2 |
| Exact bytes per baseline/current artifact | 2097152 |
| Mandatory core identity records | 8 |
| Mandatory core identity record bytes total | 524288 |
| Stable Scope IDs per artifact | 4096 |
| Canonical semantic bytes across entries per artifact | 4194304 |
| Evidence-manifest supporting paths | 40 |
| Evidence supporting bytes | 2097152 |
| Exact Git commits in one declared range | 100 |
| Change-decision records | 256 |
| Risk-acceptance records | 256 |
| Estimate/capacity receipts | 256 |
| Dependency/interface edges | 4096 |
| Acceptance/test mapping rows | 4096 |
| Paths per input revalidate batch | 64 |

Bounds do not authorize silent truncation. Preserve every discoverable identity
as `UNCHECKED_LIMIT` and return `PARTIAL` after a meaningful core comparison. A
core artifact too large to establish identity/schema/completeness returns
`INSUFFICIENT EVIDENCE`.

## Exact identity reference

Every input artifact uses:

```text
<canonical-project-relative-path>
```

The path must resolve to one regular file inside repository root without an
escaping symlink/junction. Validate exact bytes before parsing and require equality.
The identity is path plus artifact revision plus internal schema/artifact ID/version;
neither path nor filename alone is immutable identity.

## Baseline artifact contract

```yaml
schema: cgs.scope-baseline/v1
baseline_id: <stable ID>
baseline_version: <immutable monotonic version>
parent_scope_id: <stable parent ID>
timebox_or_release_id: <stable ID>
source_revision: {commit_or_content_revision, recorded_at}
approval:
  state: APPROVED
  decision_id: <stable ID>
  record: <path@revision>
  approver_id: <identity>
  authority_ref: <path@revision plus role/scope>
  approved_at: <ISO-8601 UTC>
  signature_or_record_id: <immutable proof>
completeness:
  state: COMPLETE
  declared_entry_count: <integer>
normalization_schema: <stable schema ID/version>
entries:
  - scope_id: <stable unique ID>
    title: <display only>
    semantic_fields: <schema-declared payload>
    acceptance_boundary: <stable semantic payload>
    approved_state: <state>
exclusions: [{scope_id_or_non_goal_id, semantic_fields}]
```

The external explicit artifact revision is authoritative for version selection; the internal record must
bind that revision through its approval record. Missing/invalid approval, authority,
version, parent/timebox, stable IDs, completeness, or normalization schema is
`INSUFFICIENT EVIDENCE`. Do not infer approval from status prose or location.

## Current manifest contract

```yaml
schema: cgs.scope-current/v1
current_manifest_id: <stable ID>
current_version: <version/revision>
parent_scope_id: <same stable parent ID>
timebox_or_release_id: <same stable ID>
source_revision: {commit_or_content_revision, recorded_at}
baseline_ref:
  baseline_id: <exact ID>
  baseline_version: <exact version>
  path: <exact canonical path>
  revision: <explicit baseline revision>
completeness:
  state: COMPLETE
  declared_entry_count: <integer>
normalization_schema: <same compatible schema ID/version>
entries:
  - scope_id: <stable unique ID>
    title: <display only>
    semantic_fields: <schema-declared payload>
    acceptance_boundary: <semantic payload>
    current_state: <state>
    change_decision_refs: [<stable IDs or empty>]
explicit_removals:
  - {scope_id, change_decision_refs, successor_scope_ids}
```

The current manifest, not implementation evidence, defines current scope. Silent
deletion of baseline IDs without an explicit removal row is `CONFLICT`.

Story/epic/sprint/milestone/feature artifacts are eligible only when they directly
implement this schema or point through an exact `path@revision` to one unique
companion manifest. Fuzzy parent lookup is forbidden.

## Semantic normalization and stable Scope IDs

Use only the exact normalization adapter named by both artifacts. The adapter
lists semantic fields, Unicode/whitespace normalization, ordered versus set-valued
fields, stable reference encoding, null handling, and canonical serialization.

Title, heading level, row number, rendering order, Markdown formatting, comments,
and timestamps are presentation fields unless the schema explicitly declares one
semantic. Validate the canonical semantic payload plus acceptance boundary per Scope
ID. Never use an LLM summary, fuzzy similarity, or item count as semantic identity.

Duplicate/missing Scope IDs, incompatible adapters, schema disagreement, or
canonicalization failure is `UNMAPPED`/`CONFLICT` and blocks a complete result.

## Delta and stable identity

Delta type:

| Baseline | Current | Semantic revisions | Delta type |
|---|---|---|---|
| absent | present | n/a | `ADDED` |
| present | absent with explicit removal | n/a | `REMOVED` |
| present | present | different | `MODIFIED` |
| present | present | equal | `UNCHANGED` |
| missing/non-unique/uncanonicalizable ID | any | unknown | `UNMAPPED` |
| incompatible parent/link/record or silent deletion | any | conflicting | `CONFLICT` |

finding key material:

```text
baseline ID + baseline version + parent scope ID + stable Scope ID + delta type
```

Exclude artifact/entry revisions, current manifest ID/version, title, row/line,
timestamp, decision state, risk state, and impact. Delta ID is:

```text
SCP-DELTA-<scope-id>-<delta-type>-<stable-entry-id>-<sequence>
```

Each delta stores finding key, Scope ID, type, baseline/current artifact and entry
revisions, source locations, semantic field-level differences, authority state,
allowed-state classification, risk references, impact evidence, and notes.

## Change-decision authority

A final approved change record has:

```yaml
schema: cgs.scope-change-decision/v1
decision_id: <stable ID>
state: FINAL_APPROVED | PROPOSED | REJECTED | SUPERSEDED
operation: ADD | REMOVE | MODIFY
scope_ids: [<exact IDs>]
delta_ids: [<exact IDs>]
baseline: {id, version, path, revision}
current: {manifest_id, path, revision, entry_revision}
parent_scope_id: <ID>
timebox_or_release_id: <ID>
decision_owner: {identity, role}
authority_ref: {path, revision, permitted_parent_scope, permitted_operations}
rationale: <product decision rationale>
decided_at: <ISO-8601 UTC>
signature_or_record_id: <immutable proof>
supersedes: [<decision IDs>]
```

Admission requires exact operation/Scope/Delta/revision/parent/timebox match, current
owner authority for that scope/operation, final state, timestamp, immutable proof,
and no conflicting final record.

Authority state:

- valid admitted record -> `APPROVED_CHANGE`;
- structurally valid non-final proposal -> `PROPOSED_CHANGE`;
- no linked record -> `NO_RECORD`;
- linked external record unavailable to `compare`, or not included in a valid
  `inspect` allowlist -> `UNVERIFIED_RECORD`;
- owner lacks verified authority -> `UNAUTHORIZED_RECORD`;
- record superseded/outdated for the pair -> `STALE_RECORD`;
- any bound revision differs -> `REVISION_MISMATCH`;
- multiple contradictory final records -> `CONFLICTING_RECORD`;
- unchanged entry -> `NOT_APPLICABLE`.

Git author/committer, implementer, issue assignee, agent/reviewer, prose author,
chat acknowledgment, and file owner are not automatically product decision owners.

## Allowed-state classification

Combine delta type and authority deterministically:

| Delta | Authority | Classification |
|---|---|---|
| `UNCHANGED` | `NOT_APPLICABLE` | `ALLOWED_UNCHANGED` |
| `ADDED` | `APPROVED_CHANGE` | `ALLOWED_ADDITION` |
| `REMOVED` | `APPROVED_CHANGE` | `ALLOWED_REMOVAL` |
| `MODIFIED` | `APPROVED_CHANGE` | `ALLOWED_MODIFICATION` |
| `ADDED` | any other non-conflict state | `UNAPPROVED_ADDITION` |
| `REMOVED` | any other non-conflict state | `UNAPPROVED_REMOVAL` |
| `MODIFIED` | any other non-conflict state | `UNAPPROVED_MODIFICATION` |
| `UNMAPPED`/`CONFLICT` or conflicting authority | any | `CONFLICT` |

“Allowed” describes verified decision authority only. It does not mean low effort,
low risk, completed implementation, or a new baseline.

## Accepted-risk authority

Risk acceptance uses a separate immutable record:

```yaml
schema: cgs.scope-risk-acceptance/v1
risk_id: <stable ID>
state: ACTIVE | EXPIRED | REVOKED | SUPERSEDED
delta_ids: [<exact IDs>]
scope_ids: [<exact IDs>]
dimension: schedule | quality | integration | other
exposure_evidence: <exact impact receipts/state>
baseline_revision: <revision>
current_revision: <revision>
evidence_manifest_revision: <revision>
accepted_scope: <bounded statement>
owner: {identity, role}
authority_ref: {path, revision, permitted_dimensions/scopes}
rationale: <reason>
compensating_controls: [<controls/evidence>]
accepted_at: <ISO-8601 UTC>
expires_at_or_review_trigger: <timestamp/objective trigger>
signature_or_record_id: <immutable proof>
```

The audit may reference only a current ACTIVE, unexpired, authority-verified,
signature-valid, exact-revision/scope-matching record. It cannot create/renew/apply a
record. Risk acceptance never changes delta type/authority/classification,
evidence coverage, or baseline identity.

## Re-baseline authority

A new baseline is usable only as a new exact input after a separately created:

```yaml
schema: cgs.scope-rebaseline/v1
old_baseline: {id, version, revision}
new_baseline: {id, version, revision}
included_change_decision_ids: [<IDs>]
product_owner_and_authority: <verified evidence>
decided_at: <ISO-8601 UTC>
signature_or_record_id: <proof>
```

An edited file, a proposed record, “cuts completed,” a newer modification time, or
a prior scope-check result cannot re-baseline. Scope-check never creates/applies
this record.

## Evidence-manifest contract and bounds

```yaml
schema: cgs.scope-evidence-manifest/v1
manifest_id: <stable ID>
path: <canonical path>
revision: <exact revision>
baseline: {path, revision, id, version}
current: {path, revision, manifest_id}
allowlist:
  - {path, revision, purpose: implementation | change-decision | authority |
         estimate | capacity | dependency | test | risk-acceptance |
         rebaseline-reference, source_id}
git_evidence:
  repository_id: <ID>
  commits_or_range: [<exact immutable IDs>]
declared_budgets: {paths, bytes, commits}
completeness: COMPLETE
```

Effective budgets are the smaller of declared and fixed limits. No glob, directory
hint, fuzzy reference, missing revision, or repository search is allowed. Git evidence
is read only for the exact IDs/range and only as implementation activity; it never
creates scope, authorization, justification, estimate, or risk acceptance.

An invalid manifest identity/binding is `INSUFFICIENT EVIDENCE` for `inspect`.
Within a valid manifest, unavailable/revision mismatched/unsupported/over-limit paths
or receipts make inspect coverage `PARTIAL`; preserve core deltas.

## Effort evidence

Every changed Scope ID must have baseline/current estimate receipts bound to exact
entry/artifact revisions, same calibrated method/unit, same confidence/uncertainty
policy, and compatible estimator provenance.

For intervals `[B_low,B_high]` and `[C_low,C_high]`, absolute effort delta is:

```text
[C_low - B_high, C_high - B_low]
```

Aggregate only compatible units/methods and report the summed interval. Do not
convert units, infer missing estimates, use item counts, or produce percentage
growth. Otherwise `Effort Delta: UNVERIFIED`.

## Deterministic impact dimensions

Allowed states:

```text
SUPPORTED_NO_EXPOSURE | SUPPORTED_EXPOSURE | INDETERMINATE |
UNVERIFIED | NOT_APPLICABLE
```

### Schedule

Requires complete changed-ID effort interval and current capacity/timebox interval
in the same calibrated unit/method, all bound to exact pair/evidence revisions.

- effort upper bound ≤ capacity lower bound -> `SUPPORTED_NO_EXPOSURE`;
- effort lower bound > capacity upper bound -> `SUPPORTED_EXPOSURE`;
- intervals overlap -> `INDETERMINATE`;
- missing/incompatible/stale receipt -> `UNVERIFIED`;
- zero changed IDs -> `NOT_APPLICABLE`.

### Quality

Denominator is every stable acceptance-boundary requirement added/removed/modified
by changed IDs. Require exact current regression/test-plan mappings and current
test-evidence state for each.

- every changed requirement has compatible current coverage and no invalidated
  requirement/test mapping -> `SUPPORTED_NO_EXPOSURE`;
- complete evidence proves at least one required mapping absent/invalidated ->
  `SUPPORTED_EXPOSURE`;
- complete mappings exist but their sufficiency conflicts/overlaps ->
  `INDETERMINATE`;
- denominator/mappings/evidence incomplete or stale -> `UNVERIFIED`;
- no acceptance-boundary change -> `NOT_APPLICABLE`.

### Integration

Compare exact baseline/current dependency/interface graph receipts bound to every
changed ID.

- no changed dependency/interface edge, or every changed edge has current owner,
  compatible contract, consumer mapping, and integration evidence ->
  `SUPPORTED_NO_EXPOSURE`;
- complete evidence proves an unowned/broken/incompatible changed edge ->
  `SUPPORTED_EXPOSURE`;
- complete graphs disagree about edge/ownership semantics -> `INDETERMINATE`;
- graph/owner/contract/evidence incomplete or stale -> `UNVERIFIED`;
- no dependency/interface-bearing change -> `NOT_APPLICABLE`.

Do not combine these dimensions into a score or Low/Medium/High label. An accepted
risk reference is displayed alongside but does not change the evidence state.

## Core and evidence coverage

Report independently:

```yaml
core_identity: COMPLETE | PARTIAL | INSUFFICIENT
scope_ids: {status, valid_unique, declared, unchecked}
semantic_diff: {status, compared, denominator, unmapped, conflicts}
change_authority: {status, approved, proposed, absent, invalid, unchecked}
evidence_allowlist: {status, read, declared, bytes_read, bytes_budget, unchecked}
effort: {status, covered_changed_ids, changed_ids}
schedule: <impact state>
quality: <impact state>
integration: <impact state>
risk_acceptance: {status, valid, invalid, unchecked}
input_mutation_guard: {status, before_revision, after_revision, changed}
```

Coverage ratios are evidence availability only, never scope-health/risk scores.
A zero denominator is `NOT_APPLICABLE`, not 100%.

## Canonical result table

Apply in precedence order:

| Condition | Result |
|---|---|
| invalid syntax/path/alias/type/schema or unreadable input | `ERROR` |
| discover/no arguments/missing required pair member | `INPUT REQUIRED` |
| baseline/current identity, approval, linkage, parent, completeness, stable IDs, normalization, or final core revalidate invalid/stale/conflicting | `INSUFFICIENT EVIDENCE` |
| core comparison is meaningful but core/evidence budget, declared allowlist, receipt, or evidence revalidate leaves requested scope unchecked | `PARTIAL` |
| complete core identity/diff, no ADDED/REMOVED/MODIFIED/UNMAPPED/CONFLICT | `NO SCOPE DELTA` |
| complete core identity/diff, at least one ADDED/REMOVED/MODIFIED, no UNMAPPED/CONFLICT | `SCOPE DELTA FOUND` |

Missing optional evidence under `compare` does not hide a core delta: authority is
`NO_RECORD` and impacts are `UNVERIFIED`. Under `inspect`, a declared evidence
manifest promises coverage, so a declared gap/overflow is `PARTIAL`.

Authorized deltas still yield `SCOPE DELTA FOUND`. Results never use `PASS`,
`FAIL`, bloat/creep percentages, or schedule/quality approval language.

## Review-evidence output

For a valid meaningful comparison return:

```yaml
schema: cgs.review-evidence/v1
record_id: <project-id>:<UTC-run-id>:<record-sequence>
artifact_id: scope-check:<baseline-id>:<baseline-version>:<current-manifest-id>
artifacts:
  - path: <canonical project-relative path>
    revision: <complete explicit revision>
    role: baseline | current | baseline-approval | normalization-schema |
          evidence-manifest | change-decision | authority | estimate | capacity |
          dependency | test | risk-acceptance | rebaseline-reference
    source_id: <stable ID or null>
reviewer: scope-check:<run-id>
verdict: INSUFFICIENT EVIDENCE | PARTIAL | NO SCOPE DELTA | SCOPE DELTA FOUND
timestamp: <ISO-8601 UTC with fractional seconds>
finding_ids: [<stable SCP-DELTA IDs for non-unchanged rows>]
producer:
  tool: scope-check
  version: <explicit-revision>
extension:
  schema: cgs.scope-check/v2
  run_id: SCP-<compact UTC>-<pair12>-<UUIDv4>
  project_id: <canonical repository identity>
  operation: compare | inspect
  baseline: {path, revision, byte_length, schema, id, version, source_revision,
             parent_scope_id, timebox_or_release_id, approval_record_id}
  current: {path, revision, byte_length, schema, id, version, source_revision,
            parent_scope_id, timebox_or_release_id, declared_baseline_ref}
  comparison_key: <identifier of project/baseline identity/current identity/normalizer>
  normalization: {schema_id, version, source_path, source_revision}
  limits: <all effective fixed limits>
  deltas: [<stable sorted complete delta rows including unchanged>]
  delta_summary: {added, removed, modified, unchanged, unmapped, conflict}
  allowed_classification_summary: <counts and IDs by exact class>
  evidence_manifest: <identity/coverage or null>
  change_decisions: [<validated state rows>]
  risk_acceptance_refs: [<validated state rows>]
  effort_delta: {state, unit, method, interval, receipts}
  impact: {schedule, quality, integration}
  coverage: <complete core/evidence ledger>
  unchecked: [<stable identities/reasons>]
  input_mutation_guard:
    before: [{path, revision}]
    after: [{path, revision}]
    status: UNCHANGED | CHANGED | INCOMPLETE
  result: <same as generic verdict>
  neutral_options: [<0 or 2-3 unranked options with Scope IDs/owner/action>]
  stale_key: <identifier of pair/approval/normalizer/evidence/decisions/receipts>
  gate_evidence_status: NOT_PERSISTED
  gate_evidence_eligible: false
  operation_boundary: READ_ONLY
```

`INPUT REQUIRED` and input `ERROR` return bounded non-review objects with null
verdict. Core `INSUFFICIENT EVIDENCE` may return a diagnostic generic envelope only
when both artifact identities were readable enough to bind the failure; otherwise
return the bounded error object.

Every consumed artifact is listed with exact revision and revalidated before output.
Direct output is non-persisted and grants no product, planning, gate, or mutation
authority.
