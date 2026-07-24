---
name: team-narrative
description: "Coordinate canon-safe narrative artifacts through a bounded canon graph, explicit product decisions, hash-bound read-only proposals, single-owner writes, real localization constraints, resumable evidence, and independent final review."
---

# Team Narrative

Create or revise narrative artifacts without letting unresolved canon, overlapping
writers, stale reviews, incomplete localization evidence, or partial agent work
become delivery truth. This workflow creates narrative documents and contracts
only; it never implements engine triggers, assets, translations, or gameplay code.

## Invocation and request contract

Invoke only as:

    $team-narrative --manifest <request-path> [--resume <checkpoint-path>]

No manifest prints this usage and stops before repository discovery, source reads,
delegation, decisions, approval, authorization, or writes. Never infer a topic or
destination from repository state.

The manifest declares `contract: cgs.team-narrative-request/v2` and:

- stable `content_id`, unique `run_id`, and `operation: create | revise`;
- narrative goal, requested artifact IDs/types, exact normalized destination paths,
  intended audience, source locale, content-rating policy, and spoiler class;
- exact canon roots/registry, character/voice sources, narrative history, gameplay/
  level trigger contracts, UX surfaces, string-system/localization constraints, and
  localization-handoff interface evidence with expected raw SHA-256 or `ABSENT`;
- existing target preimage hashes or `ABSENT`, proposed unique owner for each
  destination/shared record, and explicit non-write paths;
- canon decision authority, canon-promotion authority, content-plan approver,
  mutation authority, operational recorder, artifact writers, localization
  reviewer, localization-handoff authority, and final reviewer identities;
- `review_mode: full | lean | solo`, limits no larger than this contract, exact
  attempt/phase deadlines, and one-retry policy; and
- operational root, initial checkpoint-chain state, expected record preimages, and
  existing authorization/receipt evidence when resuming.

Reject unknown/duplicate fields, unsafe/aliased paths, path traversal, symlink or
junction escape, duplicate IDs or normalized destinations, conflicting writer
sets, missing revise targets, occupied create targets, unsupported types, invalid
hashes/statuses, raised limits, target/source aliasing, and authorization that does
not bind exact candidate bytes.

## Non-negotiable invariants

1. Read-only canon validation, explicit product decisions, verified promotion when
   needed, and `CANON_FROZEN` finish before any canon-dependent brief, dialogue,
   art, or level proposal begins.
2. Parallel delegates are read-only proposal/review agents with disjoint context;
   they never write project or operational files and never delegate again.
3. Every normalized artifact path has exactly one writer. Every shared registry or
   manifest has one recorder and sequential hash-guarded updates.
4. No content write is proposed until an exact artifact plan lists every path,
   operation, artifact ID, owner, preimage, complete candidate hash, limit, and
   non-write. Concept approval is not mutation authorization.
5. Authors, editors, recorders, product approvers, and final reviewers are distinct
   evidence roles. A final reviewer is fresh/read-only and binds final hashes.
6. Blocking localization defects or unknown required constraints mean
   `NOT_LOCALIZATION_READY` and prohibit COMPLETE and downstream handoff.
7. Narrative artifacts use the narrative review profile; never invoke or recommend
   a system-GDD review workflow.
8. PARTIAL work remains PARTIAL. Timeout, omission, stale evidence, late output,
   checkpoint drift, missing role, or incomplete review cannot be accepted into
   COMPLETE.

## Operational records and stable identity

All optional persisted records live under:

    production/narrative/team-narrative/<content_id>/<run_id>/

The request must pre-authorize their exact paths/naming scheme and coordinator
recorder or they remain in conversation. Records are create-only event evidence:

- `context-manifest.yaml` — `cgs.narrative-context-manifest/v2`;
- `role-matrix.yaml` — `cgs.narrative-role-matrix/v2`;
- `manifests/string-constraints-<digest>.yaml` —
  `cgs.narrative-string-constraint-manifest/v2`;
- `manifests/final-artifacts-<digest>.yaml` —
  `cgs.narrative-final-artifact-manifest/v2`;
- `canon/<sequence>-decision-<digest>.yaml` and optional versioned promotion
  plan/receipt;
- `plans/<sequence>-artifact-<digest>.yaml` and
  `plans/<sequence>-ownership-<digest>.yaml`;
- `checkpoints/<sequence>-<phase>-<digest>.yaml`;
- `reviews/localization-<sequence>.yaml` and `reviews/narrative-<sequence>.yaml`;
- `handoffs/localization-<digest>.yaml` —
  `cgs.narrative-localization-handoff/v2`; and
- `results/<sequence>-<verdict>-<digest>.yaml`.

Every record binds predecessor hash or `ROOT`, source/canon/artifact-set hashes,
active/revoked attempt tokens, identities, decisions, authorizations, findings,
and exact next safe phase. Do not overwrite a checkpoint or result to “resume.”

Use stable IDs derived from canonical evidence:

- `NCF-<fingerprint>` canon finding;
- `NCP-<artifact-id>-<fingerprint>` proposal;
- `LOC-<string-id>-<fingerprint>` localization finding;
- `NRF-<profile-check>-<artifact-id>-<fingerprint>` final-review finding; and
- `TNC-<sequence>-<phase>-<fingerprint>` checkpoint.

Finding rows contain ID, severity, status `OPEN | ROUTED | RESOLVED`, source path/
locator/hash, artifact/string/truth/trigger IDs, owner, destination, acceptance
condition, and resolution evidence. Approval or risk acceptance cannot close a
blocking finding without current verification.

## Phase 0: Freeze roles, mode, and bounded context

Before source loading, render `cgs.narrative-role-matrix/v2` from the request and
the exact mode contract in `references/execution-and-evidence.md`. The matrix lists
every phase, role, required/conditional/skipped state, identity, read/write scope,
deadline, retry cap, omission effect, and reviewer independence constraint.

Hard context limits are:

- 48 total source files and 2097152 exact bytes;
- 256 canon nodes, 512 dependency edges, and graph depth 8;
- 64 characters, 64 locations, 32 factions, 64 private truth entries, 500 string
  IDs, and 128 trigger-contract entries; and
- at most eight declared source groups.

The request may lower, never raise, a limit. Inventory/count before full-read;
never truncate a source. Build a directed graph only from declared roots and direct
stable-ID references. Record normalized path, role, selected locator, exact bytes/
hash, owner, node/edge IDs, cycles, omissions, and loaded state in the context
manifest.

Missing, ambiguous, contradictory, cyclic, or over-budget canon evidence blocks
canon freeze and all dependent proposals. Do not recursively load the repository.
An optional non-canon source group overflow yields PARTIAL and excludes dependent
artifacts from write authorization.

## Phase 1: Validate canon before dependent creation

The canon validator is read-only and receives only the frozen context-manifest
candidate. It reports existing claims, contradictions, missing references, proposed
diffs, affected artifact IDs, and stable NCF findings with source hashes. It cannot
promote or write canon.

Present source-backed options to the named canon authority. The authority must
choose explicitly or stop. Record `cgs.canon-product-decision/v2` with decision ID,
selected option, rationale, decision-maker, affected canon IDs/paths, source hashes,
and timestamp. The coordinator, world-builder, or narrative author cannot make the
product decision by convenience.

If no canon change is needed, rehash the declared canon manifest and freeze its
canonical sorted path/hash digest.

If canon must change, Phase 2 is mandatory. Writer, art-director, level-designer,
and canon-dependent narrative-director tasks remain unlaunched until a verified
`CANON_FROZEN` checkpoint exists.

## Phase 2: Separately approve and promote canon

Canon promotion is a distinct product-governance transaction, never a final-step
world-builder action. Render every final candidate byte first and create
`cgs.canon-promotion-plan/v2` containing:

- product decision ID/hash and affected canon IDs;
- every create/update path, artifact/registry ID, unique canon writer or registry
  recorder, expected preimage/ABSENT, candidate hash/bytes, and size;
- reference/registry changes, deterministic write order, validation rules, and
  explicit non-writes; and
- proposed promotion receipt path/hash and rollback limitation.

Obtain exact plan approval from the canon authority, then a separate mutation
authorization for that same path/hash set. Immediately before the first write,
rehash decision/source/target/registry/authorization/role evidence. Any drift means
zero promotion writes and a new preview.

One canon writer writes canon artifacts sequentially; one registry recorder writes
the shared canon registry after artifacts. Read back every byte, validate IDs,
references, registry projections, access class, and hashes, then persist a
`cgs.canon-promotion-receipt/v2`. Do not claim multi-file atomicity or destructive
rollback. A mid-transaction failure is PARTIAL/BLOCKED with exact applied/not-
applied evidence and prevents canon freeze.

Only a verified promotion receipt or a verified no-change decision may produce the
canonical sorted `canon_baseline_sha256` and `CANON_FROZEN` checkpoint.

## Phase 3: Create the brief and bounded read-only proposals

After CANON_FROZEN, the narrative-director author produces a read-only brief
proposal bound to the canon baseline. Canon-dependent unknowns remain findings.
Once the brief candidate is source-bound, launch only the mode-allowed conditional
proposal roles for requested artifact types:

- writer — dialogue/string-key/lore/voice proposals;
- art-director — visual narrative brief only, never asset production;
- level-designer — trigger/discovery/pacing/environmental-story contracts only,
  never engine implementation.

Each attempt receives the same canon-baseline hash, exact context slice/hash,
artifact schema, allowed proposal IDs, prohibited paths, deadline, and unique
attempt token. It returns proposal content, citations, assumptions, destination
suggestions, and candidate sizes/hashes; it has zero write authority.

Deadlines, cancellation, retry, late-result quarantine, mode degradation, and
checkpoint rules are normative in `references/execution-and-evidence.md`. Missing,
timed-out, canceled, invalid, or mode-omitted required proposals yield PARTIAL; no
dependent candidate may enter an authorized write set.

## Phase 4: Build the exact artifact and ownership plan

Reconcile proposals read-only. Before any narrative-content write, render complete
deterministic candidate bytes and create `cgs.narrative-artifact-plan/v2`. Each row
contains:

- stable artifact ID/type, operation, exact destination, schema/version, proposal
  IDs, canon/brief/context hashes, and dependency artifact IDs;
- unique writer identity, destination owner, reviewer identity, expected preimage
  hash or ABSENT, candidate byte count/SHA-256, and maximum size;
- localization/string/UX/trigger/spoiler/content-rating obligations; and
- explicit create/update/no-op/conflict classification and non-writes.

Create `cgs.narrative-ownership-manifest/v2` proving one writer per path, disjoint
writer path sets, and one sequential recorder for every shared record. A suggested
unknown destination is excluded; adding it requires a revised request, complete
re-render, plan approval, and authorization. Conflict is BLOCKED, never an implied
overwrite or merge.

Show the entire path/owner/preimage/candidate matrix. Obtain content-plan approval
only after the inventory is exact. Plan approval does not authorize writes.

## Phase 5: Validate real UX, string, and localization constraints

The localization reviewer is read-only and checks accepted candidates against
declared current UX/string sources. Build
`cgs.narrative-string-constraint-manifest/v2` with, per string ID:

- UI surface/control ID and source path/hash;
- actual lines, columns, pixels, bytes, markup, font/fallback, and truncation rules
  when the source defines them;
- placeholder/formatter contract, plurals, gender, grammar, concatenation, dates,
  numbers, and source-locale ownership;
- locale-specific expansion evidence and test profile from the authoritative UX/
  localization source; and
- content-rating, cultural-safety, and spoiler exposure.

Never invent a universal 120-character gate or generic expansion percentage. A
missing constraint may be recorded as an explicit test assumption with owner and
validation plan, but its status is `UNKNOWN`; it cannot become a shipping gate,
LOCALIZATION_READY, or COMPLETE until authoritative evidence replaces it.

Use `cgs.narrative-localization-review/v2`. Blocking/UNKNOWN required findings must
be fixed by the unique artifact owner inside the exact plan and re-reviewed, or the
run is PARTIAL with `NOT_LOCALIZATION_READY`. Business-risk acceptance records a
decision but never changes blocker severity/readiness or enables a downstream
handoff.

## Phase 6: Validate localization handoff interface

Do not guess or emit `$localize extract`. Read the exact declared current handoff
interface path/hash and require `cgs.localization-handoff-contract/v1` with:

- supported input artifact-manifest schema/version and exact manifest path/hash;
- content/run/source-locale IDs and ordered stable string IDs;
- LOCALIZATION_READY review/receipt schema and required zero-blocker fields;
- protected spoiler/private-truth exclusion rules;
- destination/output ownership, expected preimages, and caller authority; and
- availability/version evidence for the receiving workflow.

Create a read-only `cgs.narrative-localization-handoff/v2` candidate with exactly
this producer contract. Arrays retain the canonical order of their owning
manifests; hashes are over exact raw bytes unless the field explicitly names a
canonical digest:

```yaml
schema: cgs.narrative-localization-handoff/v2
adapter: cgs.narrative-localization-handoff-v2-adapter/v1
handoff_id: NLOC-<canonical-payload-digest-prefix>
content_id: <request content_id>
run_id: <request run_id>
source_locale: <request source locale>
producer:
  workflow: team-narrative
  request_path: <canonical request path>
  request_sha256: <exact raw request hash>
interface_contract:
  schema: cgs.localization-handoff-contract/v1
  path: <declared current contract path>
  sha256: <exact raw contract hash>
authority:
  request_authority_id: <localization-handoff authority from request>
  contract_caller_authority_id: <exact caller authority required by contract>
  recipient_id: <contract-declared receiving workflow identity>
canon:
  canon_baseline_sha256: <canonical sorted canon baseline digest>
  sources: [{path: <canonical path>, sha256: <exact raw hash>}]
narrative:
  final_artifact_manifest:
    schema: cgs.narrative-final-artifact-manifest/v2
    path: <canonical path>
    sha256: <exact raw hash>
    final_artifact_set_sha256: <canonical artifact-set digest>
  story_artifacts:
    - {artifact_id: <stable ID>, path: <canonical path>, schema: <version>, sha256: <exact raw hash>}
  context_manifest:
    schema: cgs.narrative-context-manifest/v2
    path: <canonical path>
    sha256: <exact raw hash>
  source_bindings:
    - {role: <declared role>, path: <canonical path>, sha256: <exact raw hash>}
strings:
  constraint_manifest:
    schema: cgs.narrative-string-constraint-manifest/v2
    path: <canonical path>
    sha256: <exact raw hash>
  ordered_string_ids: [<stable string IDs>]
  string_id_set_sha256: <canonical ordered-ID digest>
readiness:
  schema: cgs.narrative-localization-review/v2
  path: <canonical review record path>
  sha256: <exact raw review hash>
  verdict: LOCALIZATION_READY
  blocking_finding_ids: []
  unknown_required_finding_ids: []
exclusions:
  private_truth_excluded: true
  protected_spoiler_payload_excluded: true
destination:
  output_owner_id: <contract-declared owner>
  recorder_id: <contract-declared recorder>
  expected_preimages: [{path: <canonical path>, expected: <sha256 or ABSENT>}]
recipient:
  workflow: localize
  request_schema: cgs.localization-request/v2
  availability_path: <declared evidence path>
  availability_sha256: <exact raw hash>
payload_sha256: <sha256 of canonical payload excluding payload_sha256 and handoff_id>
```

Canonical handoff payload bytes are UTF-8 canonical JSON with object keys sorted
by Unicode code point, NFC strings, arrays preserved in their declared manifest
order, no insignificant whitespace, and no trailing newline; omit exactly
`payload_sha256` and the derived `handoff_id`. `handoff_id` is `NLOC-` plus the
first 20 lowercase hexadecimal characters of that digest. This two-field omission
prevents a circular self-hash; no placeholder value for `handoff_id` participates
in the payload. `string_id_set_sha256` hashes the ordered stable string
IDs joined by LF with no trailing LF. No other serialization or ID prefix is
accepted. A persisted handoff path is exactly
`production/narrative/team-narrative/<content_id>/<run_id>/handoffs/localization-<64-lowercase-payload-digest>.yaml`.

The two authority IDs must be equal. Every canon, story/artifact, context/source,
constraint, review, interface, and availability path is re-read and re-hashed
immediately before candidate finalization. `story_artifacts` must equal the final
artifact manifest rows exactly; `sources` and `source_bindings` must reproduce the
current canon/context digests. Any missing, extra, stale, incompatible, unavailable,
non-ready, non-empty blocker/unknown list, authority mismatch, or exclusion false
marks `LOCALIZATION_HANDOFF_UNVERIFIED`; do not recommend or invoke localization,
and return PARTIAL when localization delivery is required.

If persistence of the candidate was pre-authorized, only the operational recorder
may create its canonical handoff path and must read back/hash the exact candidate.
Otherwise it remains conversation-only and cannot be used as a path-bound input by
`localize` until a separately authorized recorder persists the identical bytes.

This skill never invokes the receiving workflow. A valid handoff is a possible
post-COMPLETE next action only.

## Phase 7: Authorize, CAS, write, and read back

After exact artifact/ownership plans and localization clearance, present one
mutation manifest containing only selected narrative artifact candidates plus
already-authorized operational evidence. It binds plan/approval IDs and hashes,
canon baseline, context/role/ownership/constraint/localization hashes, exact
targets/preimages/candidates/writers/order, result/checkpoint receipt targets, and
non-writes.

Obtain one explicit mutation authorization. Run source, canon, target-set,
ownership, approval/authorization, checkpoint/attempt-token, and role CAS in one
pre-write pass. Any mismatch means zero content writes and fresh planning.

Unique writers apply only authorized disjoint paths, sequentially per path, with
atomic single-file replacement where supported and immediate read-back/hash/schema/
reference verification. Shared manifests write once through the sole recorder after
artifact verification. Never claim whole-set atomicity. A mid-set failure stops
ordinary writes and yields PARTIAL with exact applied/not-applied evidence.

Build canonical `cgs.narrative-final-artifact-manifest/v2` from sorted artifact ID,
path, type, owner, schema, byte count, and observed hash. Its digest is
`final_artifact_set_sha256`.

When a downstream localization handoff is requested, the operational recorder
must create and read back the exact string-constraint and final-artifact manifests
at their pre-authorized canonical record paths before it may persist the handoff.
Without both durable raw-hash-bound manifests, the handoff remains unverified.

Private mystery truths may exist only in an explicitly access-controlled private
canon artifact. Public artifacts contain stable truth IDs, not protected answers.

## Phase 8: Independent final-hash narrative review

After all writes/read-back, run a fresh, read-only reviewer whose identity differs
from every author, editor, writer, recorder, decision-maker, and approver of the
reviewed set. The review binds the current canon baseline and final artifact-set
hash and loads only those exact bytes.

Use the narrative-specific profile in `references/narrative-review-profile.md`.
Persist `cgs.narrative-review-result/v2` with reviewer identity, input hashes,
coverage, stable NRF findings, omissions, disposition, and timestamp.

Any polish/fix makes the old review stale. Render the exact fix bytes through the
same unique artifact owner, create a new versioned artifact/ownership plan, and
obtain new content-plan approval and mutation authorization unless the exact fix
bytes were already bound by current authorization. Then rehash the complete
artifact set and run a fresh scoped independent review covering changed artifacts
and their declared dependents. Allow at most two fix/re-review rounds. Failure,
timeout, partial coverage, stale hash, identity overlap, or unresolved blocker
yields PARTIAL/BLOCKED, never COMPLETE.

## Checkpoint, recovery, and result protocol

Read and follow `references/execution-and-evidence.md` in full. It defines mode
semantics, exact deadlines/retry/cancel behavior, append-only checkpoints,
idempotent resume, late-write detection, CAS, partial receipts, and result schemas.

## Completion and next action

`Verdict: COMPLETE` requires all of:

- verified CANON_FROZEN checkpoint and current canon baseline hash;
- every authorized artifact at its exact path with final observed hash/owner and
  no unlisted or late write;
- LOCALIZATION_READY with zero blocking/UNKNOWN required findings;
- current independent narrative review over the final artifact-set hash with full
  canon/voice/arc/trigger/truth/localization/rating/reference coverage;
- valid checkpoint/result chains, authorizations, artifact manifest, and read-back;
- zero open blockers, stale evidence, revoked-token outputs, and required mode
  omissions; and
- when localization delivery is requested, a verified compatible localization
  handoff contract/candidate.

Otherwise return exactly:

- `Verdict: PARTIAL` when safe proposals/artifacts/evidence exist but required work,
  review, constraints, handoff, or verification is incomplete; include
  `NOT_LOCALIZATION_READY`, `NOT_INDEPENDENTLY_REVIEWED`, or
  `LOCALIZATION_HANDOFF_UNVERIFIED` as applicable; or
- `Verdict: BLOCKED` when no safe phase can continue without a product decision,
  missing authority/dependency, conflict, drift, invalid chain, or canon failure.

The result record includes content/run IDs, operation/mode, verdict/readiness,
canon-baseline and final-artifact-set hashes, artifact path/hash/owner table,
approval/authorization and checkpoint hashes, localization constraints/review/
handoff evidence, reviewer identity/result hash, open findings/blockers, partial or
late attempt evidence, and exactly one state-driven next action.

Never report COMPLETE merely because the process ran. Never invoke a downstream
workflow. COMPLETE may offer one exact handoff using the final manifest/readiness
hashes; PARTIAL/BLOCKED offers one action that resolves the highest-priority named
condition.
