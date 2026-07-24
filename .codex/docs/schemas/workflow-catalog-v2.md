# Workflow Catalog v2 Schema

Status: Proposed compatibility contract<br>
Schema ID: `cgs.workflow-catalog/v2`<br>
Canonical candidate: `.codex/docs/workflow-catalog.yaml`

## Purpose and authority

This schema makes routing and stage detection machine-checkable without turning the catalog into a workflow executor. Artifact presence is never completion. `gate-check` is read-only and emits a conversation-only assessment. No P1 project skill owns project-stage advancement.

The catalog may describe a separately configured external stage recorder only through the explicit external contract below. Missing or invalid external capability yields `UNKNOWN_ADVANCEMENT_UNSUPPORTED`; it never creates a project-skill command or authority.

## Serialization and identity

- The catalog MUST be valid YAML 1.2; JSON-compatible YAML is allowed.
- `schema` MUST equal `cgs.workflow-catalog/v2`; `schema_version` MUST equal `2`.
- `catalog_version`, `canonical_path`, `schema_reference`, and `canonicalization` are required.
- IDs are case-sensitive. Phase, step, transition, policy, verification, risk, and limit IDs MUST be unique in their namespaces.
- Consumers hash exact raw catalog bytes. They MUST NOT repair, merge, choose newest, or silently upgrade an unversioned catalog.

## Top-level keys

Required keys are `schema`, `schema_version`, `catalog_version`, `canonical_path`, `schema_reference`, `canonicalization`, `command_template_grammar`, `artifact_path_template_grammar`, `stage_contract`, `route_definitions`, `relations`, `phases`, and `transitions`.

Unknown required semantics return `UNKNOWN_NO_ROUTE`. Unknown optional metadata may be preserved but cannot authorize routing, completion, or advancement.

## Command template grammar

`command_template_grammar.schema` MUST equal `cgs.workflow-command-template/v1`.

- `<name>` is one required caller-supplied token. The referenced SKILL invocation clause owns its validation.
- `[tokens]` is one optional group only when the referenced SKILL declares it.
- `a|b` within a placeholder/group requires exactly one declared literal.
- An unresolved required placeholder or choice returns `INPUT_REQUIRED`.
- A router MUST NOT execute a template, invent a value, append an undeclared mode, or present unresolved text as an executable command.
- Each skill route declares `command_contract.source_path`, `source_clause`, template schema, and unresolved result. The source path is the project SKILL contract, not evidence that a command ran.
- Manual routes have `command: null`, a nonempty `manual_action`, and no project-skill implementation.

## Phase and step records

Each phase requires `phase_id`, `label`, `description`, positive contiguous `order`, `entry_policy`, and `steps`.

Each step requires:

- globally unique `id`, matching `phase_id`, contiguous phase-local `order`, `name`, and `description`;
- exactly one route: nonempty `command` or nonempty `manual_action`;
- `routable`, `owner`, `required`, and `repeatable`;
- `command_contract`;
- arrays `prerequisite_ids`, `accepted_artifact_types`, `produced_artifacts`, and `native_evidence_schemas`;
- `completion_evidence_contract`, `completion_policy_ref`, `verification_action_ref`, and `risk_policy_ref`;
- `evidence_scope.locations`, `presence_semantics`, `index_required`, and resolving `read_limits_ref`;
- `missing_prerequisite_consequence` and `unknown_evidence_consequence`.

Every prerequisite resolves to an earlier or same-phase step, contains no duplicate, and the complete graph is acyclic. Presence, filename, count, prose, and latest/newest selection never establish completion.

## Produced artifact record

Every produced-artifact entry has exactly these required semantic fields:

- `artifact_type`: producer-declared type/profile/schema identifier; it MUST NOT claim an undeclared schema. When a producer explicitly emits a document but declares no versioned artifact schema, this field MAY use the exact producer workflow ID only as an untyped producer-output class. That fallback is not a schema, cannot satisfy an accepted schema/profile, and cannot establish completion evidence;
- `path`: a canonical project-relative path or a registered path template;
- `path_kind`: `canonical` or `template`;
- `required`: boolean describing the selected route mode, not phase completion.

For `path_kind: canonical`, `path` contains no placeholder. For `path_kind: template`, every `<name>` value comes only from the exact producer request/result or stable identity declared by the source SKILL. An unresolved template is not a path and yields `PRESENT_UNVERIFIED`.

Extra legacy keys `type`, `path_pattern`, or `ownership` are invalid. Artifact records describe possible producer outputs only. They do not prove persistence, currentness, approval, or completion.

## Accepted artifact contracts

Every internal identifier in `accepted_artifact_types` MUST exactly match a literal
schema, profile, or untyped output class declared by the named upstream producer.
The catalog MUST NOT mint an alias for an internal producer. When a consumer
requires a generic envelope plus an embedded extension, list both exact
identifiers; the consumer's source contract owns their required co-occurrence and
same-record binding.

An input with no project-workflow producer is allowed only when either:

- a manual catalog producer declares the same exact untyped output class; or
- the consumer declares a versioned input schema and the catalog records the
  exact string `<schema> (EXTERNAL_BOUNDARY)`.

`EXTERNAL_BOUNDARY` means the project workflow set neither produces nor invokes
that input. The consumer must independently validate its producer identity,
authorization, canonical path, raw hash, currentness, and source binding. An
external-boundary input cannot prove completion of an upstream project step,
grant write authority, or be silently treated as an internally produced schema.

## Native completion evidence

There is no generic P1 producer for `cgs.workflow-step-completion-receipt/v2` or a set variant. The catalog MUST NOT advertise either schema.

`completion_evidence_contract.source_field` resolves to the step's
`native_evidence_schemas`. Persisted or gate-eligible completion is valid only
when the named producer contract itself declares an exact persisted current
artifact/receipt and the consumer verifies schema, producer identity, path, raw
hash, source hashes, coverage, currentness, supersession, and read-back.
Otherwise a persisted required step is `UNKNOWN_NO_ROUTE`; an optional step may
be `SKIPPED_BY_POLICY` only under its explicit policy.

A step that is required only for downstream workflow routing MAY use
`completion.required-candidate-conversation/v2` when its final producer contract
fixes the output to `NOT_PERSISTED` and gate-ineligible and no versioned durable
recorder is authorized. Such a step must declare
`candidate_only: true`, `candidate_output_persistence: NOT_PERSISTED`,
`candidate_gate_evidence_eligible: false`,
`durable_recorder_schema: null`, and
`gate_completion_state: BLOCKED_PENDING_VERSIONED_RECORDER`. Its exact,
current, complete conversation candidate may satisfy a declared non-gate
prerequisite, but it never establishes persisted completion, gate evidence, or
transition eligibility. Every affected transition must carry a matching
`transition_blockers` entry.

A required step whose producer needs a separately owned persistence or lifecycle
action MAY declare composite completion through `required_external_evidence`. Each entry
must name an exact versioned persisted artifact or receipt schema,
`boundary: EXTERNAL_BOUNDARY`, the independent external producer, the exact
contract sources that define the artifact or receipt,
candidate schemas it binds, `persisted_and_current_required: true`,
`gate_evidence_eligible_required: true`, `project_skill_invocation: null`, and
`missing_or_invalid_result: UNKNOWN_NO_ROUTE`. In that case:

- `producer` still names only the candidate producer;
- `candidate_output_persistence` is the producer-declared `PERSISTED` or
  `NOT_PERSISTED` state;
- `persisted_and_current_required: true` applies to the complete candidate plus
  external-receipt set, never to the candidate alone;
- the candidate producer MUST NOT create, invoke, simulate, or impersonate the
  external recorder; and
- completion remains `UNKNOWN_NO_ROUTE` until every candidate and external
  artifact/receipt identity, hash, currentness, persistence, eligibility, and binding
  check passes.

The catalog MUST NOT invent a generic review-recorder schema. An external
persistence boundary may name the exact producer envelope itself only when the
final consumer adapter explicitly accepts that persisted envelope and the
source contracts require byte-identical persistence and read-back. A wrapper
cannot rewrite immutable embedded persistence or gate-eligibility fields. The
final consumer adapter alone decides whether the unchanged candidate and an
exact companion artifact or receipt satisfy its gate-evidence contract.

The registered verification action is read-only. It emits no new schema, invokes no producer, and cannot persist or mutate. Completion-policy `accepted_receipt_schemas` therefore remains empty; exact native schemas live on each step.

Accepted risk never changes evidence or prerequisite state.

## Project-stage authority

`stage_contract.stage_enum` is the complete ordered vocabulary. The initial-stage rule is authoritative: without a valid authority record created through the configured external recorder contract, stage is `UNKNOWN`. Artifacts and legacy `production/stage.txt` never initialize or advance stage.

`authority_record` declares canonical path `production/stage/authority.json`, schema `cgs.project-stage-authority/v2`, and owner resolved from the external recorder contract. Each record binds catalog path/version/raw hash; project identity; current stage; transition ID/from/to; prior authority record path/raw hash; exact gate record ID/raw hash; external recorder owner/implementation/authorization; target commit/ref and dirty state; append-only history head; receipt ID/path/raw hash; UTC timestamp; and canonical record hash.

Receipt, continuity, target, freshness, manifest, and read-limit policies are mandatory. Missing, stale, dirty-unknown, superseded, oversized, unreadable, or contradictory evidence returns `UNKNOWN` or the declared blocker.

## External stage-transition recorder contract

The only supported advancement boundary is `cgs.external-stage-transition-recorder-contract/v1` at the configured contract path. This is an external integration contract, not a P1 project skill and not a command.

A valid contract binds:

- stable contract/project/owner identity, verified owner authority/scope/expiry;
- external implementation name/version/digest;
- exact catalog path/schema/version/raw hash;
- authority-record path/schema and allowed adjacent transition IDs;
- accepted gate schema exactly `cgs.gate-record/v2`;
- receipt schema exactly `cgs.external-stage-transition-receipt/v1`;
- target commit/ref and dirty-state policy;
- compare-and-swap fields for authority preimage/history head;
- receipt create-only destination policy;
- atomic commit/full rollback, crash recovery, read-back, byte/time limits, and idempotency rules.

A transition request supplies the exact current conversation-produced `cgs.gate-record/v2` bytes and raw hash. The recorder independently validates record ID, transition/profile/catalog/authority identities, `PASS`, `COMPLETE` coverage, `ELIGIBLE`, current dependency hashes, source revision, dirty state, authorization, and authority preimage. It MUST NOT accept CONCERNS/FAIL/PARTIAL, accepted-risk requests, stale records, phase names, or conversation summaries.

A committed `cgs.external-stage-transition-receipt/v1` binds contract/owner/implementation/authorization; transition and gate record bytes/hash; authority pre/post bytes/hashes; prior/new history head; target revision/dirty state; exact owned field set; `COMMITTED`; rollback state `NOT_REQUIRED`; receipt path/hash; and independent read-back. Any partial, ambiguous, rejected, rolled-back, recovery-required, hash-mismatched, or unowned-field result does not advance stage.

No P1 skill creates, configures, invokes, simulates, or impersonates this recorder. Missing/invalid contract or receipt returns `UNKNOWN_ADVANCEMENT_UNSUPPORTED`.

## Transition records

Each transition requires `transition_id`, adjacent `from_stage`/`to_stage`, `authorized_owner`, `gate_profile_id`, `required_gate_record_schema`, `required_transition_receipt_schema`, `threshold`, `stage_owner_handoff`, `gate_assessment`, and `advancement_action`.

`transition_blockers`, when present, is a nonempty array of exact known
consumer-compatibility blockers. Each entry names a stable blocker ID, affected
adapter, exact candidate schemas and immutable candidate state, null unavailable
recorder schema, source contracts, null project invocation, and result
`BLOCKED_PENDING_VERSIONED_RECORDER`. While any entry remains, the transition is
not eligible even when the candidate workflow itself is conversation-complete.

- `gate_assessment.command` uses the exact transition ID and final `$gate-check [transition-id] [--review ...]` grammar.
- Its output is `cgs.gate-record/v2` with `persistence: CONVERSATION_ONLY`; `stage_mutated` is false.
- `advancement_action.kind` is `external-only`, with null project implementation and null command.
- No `advance.*` action ID exists.
- A transition is recorded only by the valid external contract/receipt described above.

## Relations

`relations` declares cross-workflow producer/consumer ownership. Every referenced workflow ID resolves. A relation cannot grant write authority, execute a handoff, or turn an external/manual contract into a project skill.

## Consumer algorithm

1. Read and hash the canonical catalog once within limits.
2. Validate schema/version, required fields, route exclusivity, command templates, artifact records, unique/contiguous IDs, references, dependency acyclicity, and transition adjacency.
3. Bind the exact source SKILL invocation clause before presenting a command. An unresolved placeholder returns `INPUT_REQUIRED`.
4. Read the exact authority and append-only receipt chain. Missing external recorder evidence means stage/advancement is unknown, not inferred.
5. Resolve only routes allowed by the current authoritative stage. Validate prerequisites using exact native evidence contracts.
6. Return one exact unresolved template plus required input names, or one manual action. Do not execute, persist, infer completion, or advance stage.

## Compatibility failures

Duplicate IDs, dangling references, cycles, invalid artifact keys, unresolved required command values presented as executable, route/source-contract mismatch, unknown schemas, stale hashes, ambiguous supersession, nonadjacent transitions, or a claimed project stage recorder invalidate the affected route or catalog. v1/unversioned records are not silently upgraded.
