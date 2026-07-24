# Start — Onboarding Preferences Contract

This contract is normative for the only file `$start` may create or update:
`production/onboarding/preferences.yaml`. It defines schema, validation,
initialization/update behavior, canonical identity, authorization preview,
compare-and-set, and read-back verification. Preferences are non-authoritative
user intent; they never establish stage, gate, completion, engine selection, or
workflow execution.

## 1. Owned path and operation vocabulary

The only owned file is:

```text
production/onboarding/preferences.yaml
```

The only preference operations are:

- `INITIALIZE` — target absent and schema-2 document proposed;
- `UPDATE` — valid schema-2 target exists and one append-only decision event plus
  selected mutable preference fields are proposed;
- `UNCHANGED` — proposed canonical bytes equal current bytes;
- `NOT_REQUESTED` — user did not request persistence;
- `DECLINED` — exact preview was declined;
- `CONFLICT` — a preimage, dependency, path, or directory state changed;
- `FAILED` — authorized atomic write/read-back failed; or
- `BLOCKED_INVALID_EXISTING` — existing target is unsupported or invalid.

Never treat an invalid existing file as absent, silently migrate schema 1, rewrite
history, or replace it with a fresh document. Migration is a separate owner task.

Creating `production/` or `production/onboarding/` is a mutation. Every missing
directory and the exact file operation must appear in the one changeset preview.

## 2. Schema `cgs.onboarding-preferences/v2`

Serialize one UTF-8 YAML document with LF line endings, no BOM, duplicate keys,
anchors, aliases, custom tags, merge keys, or implicit timestamps. Quote free-text
values. Use this field order:

```yaml
schema: cgs.onboarding-preferences/v2
schema_version: 2
preference_id: <stable UUID or sha256-based ID>
project:
  root_id: sha256:<canonical real-root identity>
created_at: <ISO-8601 with timezone>
updated_at: <ISO-8601 with timezone>
catalog:
  path: .codex/docs/workflow-catalog.yaml
  schema_version: <catalog schema version>
  catalog_version: <catalog version>
  raw_sha256: sha256:<64 lowercase hex>
stage_packet:
  state: CURRENT | MISSING | INVALID | STALE | PROJECT_MISMATCH | UNREADABLE
  source: INLINE | PATH | NONE
  source_path: <repository-relative path or null>
  raw_sha256: <sha256 or null for INLINE/NONE>
  packet_id: <sha256 or null>
  snapshot_manifest_sha256: <sha256 or null>
  result: DETECTED | CONFLICT | UNKNOWN | ERROR | UNAVAILABLE
  resolution_state: CLEAR | BLOCKED | UNAVAILABLE
  detected_stage: Concept | Systems Design | Technical Setup | Pre-Production | Production | Polish | Release | UNKNOWN
observed_configuration:
  legacy_stage:
    path: production/stage.txt
    source_state: PRESENT | ABSENT | UNREADABLE
    raw_sha256: <sha256 | ABSENT | UNVERIFIED>
    value: <bounded raw value | UNKNOWN>
    authority: LEGACY_DECLARATION_ONLY
  review_mode:
    path: production/review-mode.txt
    source_state: PRESENT | ABSENT | UNREADABLE
    raw_sha256: <sha256 | ABSENT | UNVERIFIED>
    value: full | lean | solo | INVALID | UNKNOWN
preferences:
  self_reported_start_state: NO_IDEA | VAGUE_IDEA | CLEAR_UNFORMALIZED_CONCEPT | EXISTING_WORK | OTHER
  intent_summary: <bounded user text>
  concept_formalization: PREFER_FIRST | ACCEPT_RISK_TO_DEFER | UNSPECIFIED
  review_mode: full | lean | solo | unspecified
route:
  catalog_step_id: <stable ID | NONE>
  command_or_manual_action: <catalog value | NONE>
  state: READY | AT_RISK | DIAGNOSTIC | UNKNOWN | BLOCKED | NO_ROUTE
  affected_prerequisite_id: <stable ID | NONE>
  reason_codes: [<stable codes>]
risk_records:
  - risk_id: <stable append-only ID>
    risk_type: accepted-risk/missing-concept
    state: ACCEPTED_BY_USER
    missing_prerequisite_ids: [<stable catalog IDs>]
    selected_catalog_step_id: <stable ID>
    consequence_codes: [<bounded catalog/policy codes>]
    decision_id: <decision ID>
    decision_owner: <explicit user identity>
    accepted_at: <ISO-8601 with timezone>
    expires_or_review_at: <timestamp or milestone ID>
    remediation_catalog_step_id: <first missing concept step ID>
    catalog_sha256: <sha256>
    stage_packet_id: <sha256 or null>
decision_history:
  - decision_id: <stable append-only ID>
    decision_owner: <explicit user identity>
    decided_at: <ISO-8601 with timezone>
    operation: INITIALIZE | UPDATE
    changed_fields: [<canonical field paths>]
    route_catalog_step_id: <stable ID | NONE>
    catalog_sha256: <sha256>
    stage_packet_id: <sha256 or null>
authority_boundary:
  stage_mutation: NONE
  review_mode_mutation: NONE
  workflow_auto_executed: false
```

An empty risk list is `risk_records: []`; never use `NONE` in place of a typed
list. The same applies to reason and history arrays. Free text is bounded to 1,000
UTF-8 bytes per field and must not contain secrets copied from unrelated files.

## 3. Validation

For an existing document, require:

- exact schema/version and allowed field types/enums;
- matching canonical current project root ID;
- unique preference, decision, and risk IDs;
- monotonic append-only decision/risk history;
- parseable timezone-bearing timestamps with `created_at <= updated_at`;
- valid lowercase SHA-256 values or exact allowed null/state marker;
- a catalog step/command pair that matches the recorded catalog bytes, unless
  route state is UNKNOWN/BLOCKED/NO_ROUTE and both are NONE;
- risk records whose decision/remediation/catalog/packet references resolve;
- authority boundary fixed to no stage/review mutation and no auto execution; and
- no unknown required field, duplicate key, placeholder, or self-approval claim.

An old catalog or packet hash in a structurally valid existing file is historical
provenance, not corruption. New route/preferences use the current catalog/packet
and append a decision event; never rewrite prior history to current hashes.

## 4. Initialize versus update

### INITIALIZE

Use only when the target was confirmed absent at snapshot time. Generate a new
preference ID and one decision event. Show complete proposed bytes and directory/
file operations. Immediately before writing, require target and every parent
directory existence state to equal the previewed preimage.

### UPDATE

Use only for a valid schema-2 target. Preserve:

- `preference_id` and `created_at`;
- every prior decision/risk record byte-for-byte in the same order; and
- unrelated extension-free schema fields not selected for change.

Update `updated_at`, current catalog/stage-packet/config observations, selected
mutable preference fields, current route, and append exactly one decision event.
Append a risk record only after explicit risk acceptance; never delete, edit, or
deduplicate historical records.

Show a field-level old/new diff and the full proposed output bytes. In particular,
show independently:

- observed review-mode value/hash;
- requested review-mode preference;
- whether they agree or differ; and
- `review_mode_mutation: NONE`.

`UNCHANGED` applies only when no decision, preference, route, risk, observation,
or provenance byte would change. Do not append a no-op event merely to claim an
update.

## 5. One authorization preview

Before any mutation, show:

- operation and exact target path;
- every directory to create;
- existing preference preimage hash or ABSENT;
- current catalog path/version/hash;
- stage-packet source/ID/snapshot hash/state;
- observed legacy-stage and review-mode path/hash/state;
- complete field diff for UPDATE;
- complete proposed file bytes and output hash;
- risk/decision IDs appended;
- stage/review-mode files explicitly unchanged; and
- no downstream workflow execution.

An explicit bounded `--persist` request may authorize this exact preview. Without
such authorization, ask once. Authorization is invalidated by any changed preview
input or output byte and never extends to another file/workflow.

## 6. Compare-and-set transaction

Immediately before mutation, re-read/re-hash:

1. workflow catalog;
2. path-supplied stage packet and every packet snapshot entry, or revalidate the
   complete inline packet against current project bytes;
3. observed legacy-stage and review-mode files/source states;
4. existing preference target or confirmed absence; and
5. every parent directory existence/type/real-path state.

Require equality with the preview snapshot. Any difference, including a changed
observed review mode, produces `CONFLICT`, writes nothing, and reports exact old/
new hashes or state markers. Do not merge, refresh the preview implicitly, retry,
or overwrite another actor's change.

After CAS succeeds:

1. create only previewed missing directories;
2. write proposed bytes to a same-directory temporary file;
3. flush/close as supported and atomically replace/create the exact target;
4. re-read exact target bytes;
5. require output hash and parsed schema/IDs/history/references to equal preview;
6. verify stage/review-mode bytes or source states remain unchanged by this
   workflow; and
7. report `WRITTEN` only after every verification succeeds.

If directory creation or file publication fails, report `FAILED`. Do not claim
preferences were applied, do not repair partial external state, and report any
previewed directory that now exists. The authoritative stage and review-mode
configuration remain outside this transaction.

## 7. Read-only and decline paths

Without persistence, emit the full proposed preference summary in conversation
with operation `NOT_REQUESTED`; do not create directories. A declined preview is
`DECLINED`, not success or failure. Invalid existing preferences are
`BLOCKED_INVALID_EXISTING`; guidance may continue with the limitation visible,
but the file is never replaced.

Every path reports:

- preference operation and persistence separately;
- exact path/preimage/output hash or absence marker;
- stage/review-mode mutation `NONE`;
- workflow auto-executed `false`; and
- conflicts, declines, failures, and unsupported schema without hiding them.
