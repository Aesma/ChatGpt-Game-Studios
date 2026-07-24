# Team Level Contract v1

This private contract is normative for `team-level`. If it conflicts with
`SKILL.md`, stop with `run_status: ERROR` before reading project content or
dispatching agents. Never choose the more permissive rule.

## Canonical values, paths, and hashes

- Text artifacts use UTF-8 without BOM and LF.
- Raw artifact hashes are lowercase SHA-256 over exact bytes and are displayed as
  `sha256:<64-lowercase-hex>`.
- Canonical JSON objects use UTF-8/LF, keys sorted by Unicode code point, arrays
  in declared order unless a rule says sort, integers only, and no comments,
  duplicate keys, floats, NaN, or Infinity.
- Paths are project-root-relative, slash-separated, Unicode NFC, and confined
  after canonical resolution. Reject absolute/device paths, traversal, alternate
  data streams, and symlinks/reparse points escaping the project.
- Stable IDs compare byte-for-byte after schema validation. Do not infer, trim,
  case-fold, or repair them.
- Timestamps are ISO-8601 UTC instants. Deadlines are absolute, never relative
  prose.

Derived object hashes are SHA-256 over their exact canonical bytes. A hash does
not replace schema, owner, role-separation, dependency, or evidence validation.

## Fixed bounds

Apply before parsing or dispatch:

| Object | Maximum |
|---|---:|
| Context files | 20 |
| Aggregate raw context bytes | 250 KiB |
| One selected excerpt | 24 KiB |
| Aggregate prompt excerpt bytes per job | 96 KiB |
| First-level explicit dependencies | 64 |
| Adjacent interfaces | 128 |
| Adjacency traversal depth | 1 hop |
| Concurrent subagents | 3 |
| Jobs in one run | 16 |
| Narrowed follow-ups per job | 1 before original deadline |
| Default job duration | 10 minutes |
| One job result payload | 256 KiB |
| Proposals | 512 |
| Findings per profile | 256 |
| Product decisions | 128 |
| Review observations per original blocker | 2 |
| Checkpoint bytes | 2 MiB |
| Level source bytes | 2 MiB |
| QA planned cases | 512 |

Do not silently truncate a required input/output. An exceeded required bound is
BLOCKED or PARTIAL according to whether a safe core snapshot exists and always
prevents COMPLETE.

## Target and operation contract

The exact paths are:

```text
design/levels/<level-id>.md
production/session-state/team-level-<level-id>.yaml
```

`level-id` must already satisfy the invocation grammar. Operation is one of
`CREATE|REVISE|RESUME`:

- CREATE requires both paths absent and uses create-new/no-replace semantics.
- REVISE requires an existing regular level file, explicit user choice, and raw
  baseline hash; checkpoint may be absent or a matching prior record.
- RESUME requires a valid checkpoint whose exact current hash claims all verify.

A mismatch is not auto-repaired or converted to another operation. The user owns
the operation decision when existence makes intent ambiguous.

## Context manifest

Use `cgs.team-level-context-manifest/v1` with:

```text
schema_version
level_id
operation
root_instruction_refs[]
rows[]
omitted_candidates[]
limits
canonicalization_version
context_manifest_sha256
```

Each row contains `source_id`, canonical path, raw hash/bytes, artifact type,
required flag, exact selected sections, excerpt byte ranges/hashes, inclusion
reason, referring source ID, dependency depth, and state
`INCLUDED|MISSING|MALFORMED|OVER_LIMIT|OUT_OF_SCOPE|OMITTED_BY_USER`.

Order rows by artifact type, source ID, then path. Include only root/nearest
instructions, concept/pillars, current level in revise/resume, explicit first-hop
references, and one adjacency hop. A cycle is a recorded edge, not permission to
recurse. When required candidates exceed limits, user selection must bind the
full included/omitted list and its hash. Omitted required content prevents
COMPLETE unless the governing product decision formally makes it non-required.

Job prompts contain the manifest hash plus bounded relevant excerpts and
structured predecessor records. They must not contain full directory dumps,
unrelated documents, or all prior transcripts.

## Adjacency interface contract

Use `cgs.level-adjacency-interface/v1`:

```text
interface_id
source_level_id
target_level_id
source_endpoint_id
target_endpoint_id
directionality
traversal_state_contract
source_revision_sha256
target_revision_sha256_or_null
reverse_interface_id_or_null
owner
state
finding_ids[]
```

Stable interface identity hashes level IDs, interface ID, endpoints, and
directionality; it excludes prose and observed hashes.

States derive as follows:

- `PLANNED`: a bounded current roadmap/manifest explicitly declares the target
  ID, interface, owner, and expected reverse contract; target level may be absent.
- `AUTHORED`: both current level sources exist and forward/reverse IDs, endpoints,
  directionality, traversal states, and revisions are compatible.
- `UNRESOLVED`: required declaration/decision is missing without a provably
  broken referenced artifact.
- `BROKEN_LINK`: a declared authored target/reverse reference or exact path is
  absent/invalid.
- `INTERFACE_CONFLICT`: two present authoritative claims disagree on any stable
  interface field or revision binding.

File/slug existence alone does not imply PLANNED or AUTHORED. Required
UNRESOLVED/BROKEN_LINK/INTERFACE_CONFLICT prevents COMPLETE. Never auto-run a
dependent workflow or expand beyond one hop.

## Role applicability and separation

Always-required jobs:

- one read-only level-designer author;
- one fresh read-only accessibility-specialist;
- one fresh independent read-only level reviewer after source write; and
- one read-only qa-tester after the final reviewed source hash.

Narrative-director, world-builder, art-director, and systems-designer are required
when the manifest or level brief contains their artifact types/interfaces. If the
applicability determination is unknown, the job is required until a user product
decision with source hashes narrows scope.

The accessibility reviewer and level reviewer must not be the author or
transaction writer. The level reviewer must not have produced an earlier
proposal for the same draft. No review mode or role substitution waives this.

## Agent job state machine

Each `cgs.team-level-job/v1` contains:

```text
job_id
role
phase_id
required
input_object_ids[]
input_sha256
output_schema
max_output_bytes
dispatched_at
deadline_at
attempt_number
followup_count
status
result_payload_or_null
result_sha256_or_null
failure_or_null
dependency_job_ids[]
```

Job ID is `TLJ-` plus the first 20 hex characters of SHA-256 over canonical
`{level_id,operation,phase_id,role,input_sha256,output_schema}`. It excludes time,
wording, agent instance, result, and status.

Transitions are:

```text
QUEUED -> RUNNING -> COMPLETE
                 -> BLOCKED
                 -> TIMED_OUT
                 -> INVALID
COMPLETE -> STALE only when an input hash changes
```

At most one narrowed follow-up reuses the job ID/input hash/deadline and increments
`followup_count`. It cannot expand scope or extend the deadline. A late result is
recorded but not treated COMPLETE for this run. Duplicate results with different
hashes are INVALID.

A required TIMED_OUT/BLOCKED/INVALID/STALE job prevents COMPLETE. If identity,
context, and a bounded level draft/current file remain coherent, return PARTIAL
with completed job payloads and resume phase. If no coherent core exists, return
BLOCKED. Never forge or silently replace a result.

## Proposal and destination routing

Use `cgs.team-level-proposal/v1` with:

```text
proposal_id
source_job_id
source_role
destination
source_refs[]
level_facing_constraint_or_NONE
payload
assumptions[]
dependency_ids[]
product_decision_ids[]
status
proposal_sha256
```

Destination is exactly one of `LEVEL_SOURCE|NARRATIVE_LORE|ART_BRIEF|SYSTEM_GDD|
QA_PLAN|BACKLOG|REVIEW_ONLY`. Proposal ID is role prefix plus the first 20 hex
characters of the canonical fingerprint `{schema_version,level_id,source_role,
destination,subject_ids}`. Exclude prose, observed hash, time, and job status.

The routing ledger lists every proposal/finding once with destination, inclusion
state, reducer field IDs, external owner/handoff, and reason. Cross-destination
duplicates are linked by ID/hash rather than copied. The workflow writes only the
level source and checkpoint.

## Level-source schema and reducer allowlist

Canonical level source schema is `cgs.level-spec/v1`. Allowed authoritative
sections are:

1. identity, purpose, boundaries, and source snapshot;
2. critical/optional spatial paths and topology;
3. pacing beats, pressure/rest transitions, and recovery routes;
4. navigation, landmarks, entry/exit and softlock constraints;
5. encounter/mechanic interface IDs and testable placement contracts without
   reusable formulas/tuning;
6. adjacency interface records;
7. level-facing visual/wayfinding and accessibility constraints;
8. resolved finding/decision IDs and open dependency records; and
9. external-destination reference ledger.

Forbidden bodies include lore/dialogue prose, production asset/VFX/palette lists,
system formulas/tuning/loot/enemy values, QA cases, backlog bodies, review
transcripts, prompts, or raw agent output. References to their stable proposal or
owning-artifact IDs are allowed.

The frozen level bytes contain schema/version, context hash, included proposal/
decision/resolved-finding IDs and adjacency/dependency states. Compute
`level_draft_sha256` from exact UTF-8/LF bytes.

## Accessibility and level-review findings

Both use `cgs.team-level-finding/v1`. Stable ID is the profile prefix (`AX-` or
`LR-`) plus level ID and first 16 hex characters of SHA-256 over canonical:

```text
{profile_version,level_id,finding_type,requirement_id,affected_entity_ids}
```

Exclude prose, severity, observed hash, line, reviewer, time, status, and round.
Each finding records profile/version, current draft/source hash, exact section and
requirement refs/hashes, severity `BLOCKING|RECOMMENDED|NICE_TO_HAVE`, testable
required outcome, owner, `OPEN|CLOSED`, observation count, and triggering diff/
finding IDs when a regression.

BLOCKING cannot be risk-accepted. One scoped author revision and one verification
re-review are the maximum. Verification checks existing OPEN IDs and regressions
whose evidence lies within/directly depends on the changed diff. Original IDs
retain identity. Original blocker open on observation two stops BLOCKED.

## Inline independent level-review profile

`cgs.level-review/v1` is read-only and bound to exact raw level hash,
context-manifest hash, reviewer identity, author/writer identities, start/end UTC,
and findings/result hash. It checks only:

- critical-path continuity/completion;
- sequence breaks, softlocks, and recovery routes;
- pacing and pressure/rest transitions;
- adjacency IDs, directionality, and forward/reverse compatibility;
- navigation/wayfinding including non-color-only cues;
- committed accessibility requirements/resolved IDs; and
- encounter interface/dependency/acceptance boundaries.

It never applies system-GDD section requirements, invokes `$design-review`,
writes source, or creates implementation/QA evidence. A reviewer identity
collision, timeout, malformed result, missing source refs, or hash mismatch yields
review PARTIAL/INVALID and prevents COMPLETE.

## QA proposal contract and ordering

`cgs.team-level-qa-proposal/v1` is generated only after final level integration,
source persistence/postverification, accessibility closure, and current-hash
level-review PASS. It binds exact current level hash, level-review result hash,
resolved finding IDs, context hash, and qa job result hash.

Cases have stable IDs, level section/entity refs, purpose, preconditions, steps,
expected observation, platform/assistive-mode scope, and state `PLANNED`. They
cover critical path, sequence break, softlock/recovery, boundary, navigation,
accessibility, encounter interfaces, adjacency, and playtest risks.

This workflow writes no QA plan and reports no PASS/execution evidence. Any level
byte change makes review and QA evidence STALE and requires fresh review before
fresh QA. The reducer is frozen after QA starts.

## Checkpoint snapshots and resume

Use `cgs.team-level-checkpoint/v2`. After every phase construct an in-memory
snapshot containing:

```text
schema_version
level_id
run_id
operation
state_seq
last_verified_phase
safe_resume_phase_and_action
plan_hash_or_null
context_manifest_and_source_hashes
target_baseline_and_current_hashes
decisions[]
jobs[]                         # bounded payload plus result hash
routing_ledger_hash
finding_and_review_round_state
level_draft_or_current_hash
qa_proposal_hash_or_null
planned_and_actual_write_sets
write_receipts
approval_packet_hash_or_null
approval_status
checkpoint_sha256
```

`state_seq` starts at zero and increases by one per accepted transition. Before
the authorized transaction, snapshots stay in memory. The authorized checkpoint
path may be updated only by the single writer, only when its exact candidate
bytes/hash are in the currently authorized plan, and only with compare-and-set
baseline/current hash. An earlier plan cannot authorize later evidence-dependent
checkpoint bytes that did not yet exist.

Resume validates every field/payload/hash and current source/target bytes. Reuse
completed jobs only with exact input hash and intact stored result payload/hash;
reuse writes only with exact target bytes; reuse decisions/reviews/QA only with
their bound hashes. Start at the earliest stale/incomplete dependency. Never
duplicate a valid dispatch, write, decision, review observation, or QA proposal.

## Authorization and write transaction

`cgs.team-level-write-plan/v1` includes its exact one- or two-path write set,
operation and candidate bytes/hash for each path, single writer, raw baselines,
full source base set, context/routing/draft/finding/dependency hashes, open-blocker count,
success/partial/rollback protocol, and `plan_hash` over canonical plan bytes.

Preview all fields and ask once. Authorization binds plan hash. Material content,
path, operation, owner, baseline, or source-base change invalidates it. Immediately
before each write, compare-and-set all sources/targets. Use no-replace for CREATE
and expected-current-hash for MODIFY. Post-read exact bytes/hash and source
stability before success.

Rollback may be claimed only when all mutated target bytes equal verified
baselines. Otherwise persist/print honest recovery state. No external-destination
path is authorized.

## COMPLETE predicate matrix

`TL-COMPLETE/v1` is true only when every predicate is true and current:

1. valid one-target invocation and exact operation;
2. complete current bounded context manifest and source revalidation;
3. every required job COMPLETE before its deadline with valid input/result hash;
4. every proposal/finding routed once and reducer allowlist verified;
5. exact current level raw hash equals authorized/frozen bytes;
6. required adjacency/dependencies are PLANNED/AUTHORED as permitted by the
   level contract, with no UNRESOLVED/BROKEN_LINK/INTERFACE_CONFLICT;
7. zero OPEN BLOCKING accessibility findings on current hash;
8. independent level-review PASS on current hash with zero OPEN BLOCKING findings;
9. QA PLANNED proposal valid and bound to the same current hash/review result;
10. no accepted-risk branch, partial/unverified write, stale evidence, or role
    collision;
11. user final acceptance and write authorization bind the exact final packet,
    current level hash, and COMPLETE-checkpoint candidate/plan hash; and
12. same writer compare-and-set persists that exact COMPLETE checkpoint whose
    bytes/hash/sequence verify after write.

Record each predicate, evidence IDs/hashes, and true/false/unknown. Any false or
unknown value forbids `COMPLETE — DESIGN APPROVED`.

## Spec and catalog evidence boundary

The candidate test spec may state `NOT EXECUTED` and define cases. It must not
populate or imply shared catalog `last_*` results. Only an authorized test run
with immutable receipts may update those fields in a separate integration step.
Static package closure is not runtime approval evidence.
