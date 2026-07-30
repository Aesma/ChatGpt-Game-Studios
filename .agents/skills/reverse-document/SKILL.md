---
name: reverse-document
description: Create a non-authoritative, provenance-bound observation report from bounded implementation evidence while separating observed facts, unverified inferences, user-attested intent, unknowns, and unimplemented proposals.
---

# Reverse Document

Create one immutable, non-authoritative observation report from an exact bounded brownfield source inventory. Code, configuration, tests, comments, prototypes, generated output, and defects can show what exists in the checked bytes; they do not establish approved product or architecture intent.

## Invocation

```text
$reverse-document --manifest <request-path>
```

Both flags are required and may occur once. Reject unknown/repeated flags, missing values, directories, moving aliases such as `latest`, malformed revision values, traversal, or a manifest outside the repository. With no arguments, show only the usage line and stop with zero source reads, questions, writes, delegates, or verdicts.

The request must conform to `cgs.reverse-document-request/v2` and contain:

- stable `artifact_id` and requested profile;
- exact normalized repository-relative output artifact identity;
- an exact source inventory of path, expected revision, expected size, media/language type, generated/handwritten state, inclusion reason, priority, and dependency depth/edges;
- optional exact build, source-tree, or commit identity as supporting context;
- requested file, byte, parser-output, dependency-depth, and clarification budgets;
- actual observer task ID, proposed recorder task ID, and output owner;
- explicit non-writes;
- optional prior immutable report path plus expected revision for lineage only;
- expected profile ID and optional expected profile-source revision.

The manifest path, schema, stable request ID, and explicit revision must match the invocation before any source or prior report is read. A manifest is a scope request, not content approval, intent attestation, promotion approval, or write authorization.

## Authority and mutation boundary

All sources, configuration, builds, tests, prototypes, indexes, prior reports, and authoritative design/architecture artifacts are read-only evidence.

The sole permitted mutation is creating one previously absent observation report after a complete byte-exact preview and explicit authorization. This workflow never:

- edits, merges, overwrites, appends to, renames, moves, or deletes an existing report;
- writes a GDD, concept, architecture specification, ADR, story, source file, test, prototype, registry, manifest, or status/configuration file;
- converts a bug, workaround, experiment, comment, naming pattern, or test expectation into approved intent;
- places unimplemented behavior into an as-is section;
- invokes another project workflow or implements a proposal;
- commits, pushes, publishes, or performs destructive cleanup.

Content approval, intent attestation, output-write authorization, and downstream promotion are four separate decisions. One never implies another.

## Versioned profile registry and unique routing

The canonical profile registry is `reverse-document-profile-v2` embedded in this `SKILL.md`. At startup, validate the registry ID, schema version, header fields, route table, profile section tables, and stable section IDs. When the request declares a profile-source revision, require that explicit revision.

If the source is missing, malformed, duplicated, unreadable, or revision-mismatched, return `ERROR — PROFILE_UNAVAILABLE`, read no implementation source, ask no intent question, and write nothing. Do not search for or invent a replacement template.

Each artifact type has exactly one profile and route pattern:

| Profile / artifact type | Only legal output route |
|---|---|
| `observed-design-report` | `docs/reverse-document/design/<artifact-id>/<run-id>.md` |
| `observed-architecture-report` | `docs/reverse-document/architecture/<artifact-id>/<run-id>.md` |
| `observed-concept-report` | `docs/reverse-document/concept/<artifact-id>/<run-id>.md` |

The route is create-only and run-specific. A prior run may be linked by exact path/revision but is never the output target. Reject an artifact type, profile, or route that does not match this table.

### Common report header

Every report begins with these machine-readable fields:

```yaml
artifact-type: observed-design-report | observed-architecture-report | observed-concept-report
schema-version: reverse-document-profile-v2
authority: NONAUTHORITATIVE_OBSERVATION
artifact-id: <stable ID>
run-id: <immutable run ID>
status: OBSERVATION_DRAFT | OBSERVATION_PARTIAL | OBSERVATION_COMPLETE
coverage-status: PARTIAL | COMPLETE
request-path: <normalized path>
request-revision: <exact revision>
source-inventory-revision: <canonical inventory revision>
observation-snapshot-revision: <canonical checked/omitted snapshot revision>
provenance-schema: cgs.reverse-document-provenance/v2
provenance-manifest-revision: <canonical embedded manifest revision>
profile-source-path: .agents/skills/reverse-document/SKILL.md
profile-source-revision: <exact revision>
attestation-status: NONE | UNVERIFIED_IDENTITY | USER_SUPPLIED_IDENTITY
attested-by: unverified | <verbatim identity explicitly supplied by user>
prior-report-path: NOT_SUPPLIED | <normalized immutable path>
prior-report-revision: NOT_SUPPLIED | <exact revision>
generated-at-utc: <ISO-8601 UTC>
```

Never emit `verified-by`, `approved-by`, or `VERIFIED_IDENTITY`. An explicitly supplied identity is self-reported provenance, not a cryptographic signature.

### Observed design profile

| Stable ID | Exact H2 heading | Content boundary |
|---|---|---|
| RDD-01 | Scope & Provenance | exact snapshot, budgets, tools, included/omitted/unsupported scope |
| RDD-02 | Observed Behavior | source-cited behavior only |
| RDD-03 | Observed Rules, Values & Formulas | exact expressions/constants and conditions |
| RDD-04 | Observed State, Data & Events | evidenced states/transitions/ownership/events |
| RDD-05 | Observed Dependencies | evidenced calls/data/resources |
| RDD-06 | User-Attested Intent | exact attested claims and record revisions only |
| RDD-07 | Unknowns, Inferences & Contradictions | unverified interpretation and conflicting/insufficient evidence |
| RDD-08 | Gaps & Proposals — UNIMPLEMENTED | missing/recommended behavior, never as-is |
| RDD-09 | Promotion Requirements | user decisions and authoritative design-owner evidence needed |

### Observed architecture profile

| Stable ID | Exact H2 heading | Content boundary |
|---|---|---|
| RDA-01 | Scope & Provenance | exact snapshot, budgets, tools, included/omitted/unsupported scope |
| RDA-02 | Observed Components & Interfaces | implemented modules/types/contracts |
| RDA-03 | Observed Dependency, Data & Control Flow | evidenced relationships and lifecycle |
| RDA-04 | Observed Constraints & Trade-off Evidence | measured/encoded constraints, not inferred decisions |
| RDA-05 | User-Attested Intent | exact attested rationale and record revisions only |
| RDA-06 | Unknowns, Inferences & Contradictions | ambiguous rationale, legacy/defect/workaround candidates |
| RDA-07 | Decision Candidates — NOT ADRs | alternatives/proposals without ADR status |
| RDA-08 | Promotion Requirements | explicit user decision and ADR-owner requirements |

This profile is an observed architecture report, never an ADR. It cannot allocate an ADR number, write `adr-NNNN-slug.md`, or assign Proposed/Accepted/Rejected/Superseded status. A decision candidate remains non-authoritative until the user explicitly chooses a decision and an independently authorized ADR owner records it under the canonical ADR schema. Even user-attested rationale in this report is not an ADR decision receipt.

### Observed concept profile

| Stable ID | Exact H2 heading | Content boundary |
|---|---|---|
| RDC-01 | Scope & Provenance | exact prototype/build/source snapshot and coverage |
| RDC-02 | Observed Prototype Behavior | source/build/playtest-cited behavior only |
| RDC-03 | Observed Mechanics & Loop | evidenced inputs/states/outcomes/reset loop |
| RDC-04 | Observed Feasibility Evidence | actual technical results/limits, not forecasts |
| RDC-05 | User-Attested Intent & Player Fantasy | exact attested claims and record revisions only |
| RDC-06 | Unknowns, Inferences & Contradictions | unknown feel/fun, defects, exploits, incomplete evidence |
| RDC-07 | Gaps & Proposals — UNIMPLEMENTED | experiments/features/edge cases not evidenced as present |
| RDC-08 | Promotion Requirements | decisions/evidence needed for concept ownership |

Claims about feel, fun, success, player behavior, or fantasy require exact runtime/playtest/telemetry evidence or explicit user attestation. Otherwise they remain Unknown or an inference.

## Safe target and source validation

Normalize paths to repository-relative `/`, Unicode NFC, and case-preserving text. Resolve each path and every existing parent segment. Reject:

- paths outside the repository or containing traversal;
- symlinks, junctions, reparse points, mount escapes, special devices, sockets, pipes, or non-regular source files;
- output paths whose existing parent chain resolves outside the repository or whose final target already exists;
- duplicate or case-colliding paths;
- manifest-declared type/size/revision that differs from the actual file;
- archives, executables, object files, or binaries without an explicitly registered safe read-only adapter;
- a source inventory whose canonical identity is ambiguous.

Do not follow symlinks or dependencies not present in the exact manifest. Directories are never source bodies. A directory may only be a descriptive scope label; every readable source must be an individually declared regular file.

Validate the output route, target nonexistence, profile, request schema/revision, inventory structure, and hard budgets before reading any source body.

## Hard observation budgets

Request budgets may only lower, never raise, these per-invocation ceilings:

| Resource | Hard ceiling |
|---|---:|
| request manifest bytes | 256 KiB |
| declared inventory entries validated | 256 |
| source bodies read | 32 |
| individual source body | 256 KiB |
| total source bytes read | 1 MiB |
| parsed text retained | 512 KiB |
| dependency depth | 3 |
| dependency edges traversed | 128 |
| generated-file bodies read | 8 |
| prior report bytes | 512 KiB |
| clarification rounds | 3 |
| output report bytes | 512 KiB |

The effective budget is `min(requested, hard ceiling)` for each field. Missing or non-positive requested values use the hard ceiling; an unparseable value is `ERROR`.

Process the canonical inventory in `(priority, dependency_depth, normalized_path, expected_revision)` order. Dependency order selects which declared bodies are observed first; it never expands the inventory. Stop before the next read when any ceiling would be exceeded.

For every unprocessed entry, retain path, expected revision, size, type, dependency relation, and exact omission reason. Entries beyond the validation ceiling receive `OMITTED_INVENTORY_BOUND`; unsupported types/adapters receive `UNSUPPORTED`; safe but body-budget-excluded entries receive `OMITTED_BUDGET`; declared dependency depth/edge overflow receives `OMITTED_DEPENDENCY_BOUND`. Never silently sample or present an unvalidated manifest entry as a checked path.

If at least one safe supported source was checked, budget or unsupported omissions yield `coverage-status: PARTIAL`, `status: OBSERVATION_PARTIAL`, and primary verdict `PARTIAL`. If no essential source can be checked safely, return `ERROR` and write nothing. `OBSERVATION_COMPLETE` is forbidden whenever an entry is omitted, unsupported, unreadable, revision-mismatched, or changed during the run.

## Claim and inference classification

Build a fact table before narrative prose. Every row has a stable ID and exactly one class:

- `OBSERVED`: a bounded fact directly supported by exact checked source/build/test/configuration bytes or declared runtime evidence;
- `USER_ATTESTED_INTENT`: an exact intent statement explicitly confirmed by the user and linked to an immutable attestation record;
- `UNKNOWN`: rationale, correctness, completeness, ownership, reachability, intent, or an inference not established by available evidence;
- `PROPOSED_CHANGE_UNIMPLEMENTED`: a desired behavior, edge case, fix, refactor, alternative, consolidation, or experiment not evidenced as implemented.

No row combines classes. An inference is never an `OBSERVED` fact: record it as `UNKNOWN` with `statement-kind: INFERENCE_UNVERIFIED`, its cited observed premises, and the evidence required to resolve it. Narrative sentences that include interpretation must link the Unknown ID and carry the same label.

Use stable IDs:

- `OBS-<artifact-id>-<source-revision8>-<normalized-range>-<kind>`;
- `ATT-<artifact-id>-<UTC-run-id>-<attestation-ordinal>`;
- `UNK-<artifact-id>-<stable-check-or-inference-revision8>`;
- `PROP-<artifact-id>-<stable-proposal-revision8>`.

Every row records claim text, class, statement kind, source path/revision/range or attestation record, parser/adapter/tool identity and version, build/tree identity if applicable, confidence basis, and affected profile sections. Confidence never promotes an inference into fact or intent.

Code structure, names, constants, comments, tests, commit messages, and recognized patterns may establish only their observed content. Comments containing `intentional`, `temporary`, or `fix` remain observed comments. Bugs, exploits, inconsistent tests, legacy paths, and workarounds remain observations plus Unknown/Contradiction rows; do not normalize them into desired rules.

Static inspection does not prove runtime reachability, performance, player behavior, fun, correctness, completeness, or production readiness.

## Procedure

### 1. Freeze request, profile, inventory, and sampling plan

Record request path/expected/actual revision, request schema, project-root identity, selected profile, profile-source path/revision, exact canonical source inventory, effective budgets, tool/adapter availability, target path/ABSENT precondition, and optional prior-report identity.

revalidate every source ID/schema/version/revision that fits the inventory-validation ceiling and read the explicit inventory revision from the request before body reads. Entries beyond that ceiling remain explicitly unvalidated/omitted. A VCS commit or branch may be supporting context but is not a substitute for file revisions.

If a prior report is supplied, validate its exact revision, profile-v2 schema, authority, project/artifact identity, immutable run ID, provenance revision, and final report revision receipt when present. Use it only to show lineage/deltas. Never merge into it or inherit its facts/attestations without revalidating their exact current evidence.

### 2. Observe the bounded dependency sample

Read only supported inventory entries that fit the effective budgets, in deterministic dependency order. Revalidate each exact revision immediately before use. Record adapter/parser/tool name and version for each observation.

Extract profile-relevant implemented mechanics, values, formulas, conditions, state/data/events, interfaces, dependencies, configuration, and declared runtime evidence. Cite every material fact to exact path, revision, and normalized line/range or serialized key. Preserve contradictions as separate rows; do not choose a preferred source.

If bytes change, mark that entry `CHANGED_DURING_RUN`, invalidate dependent observations, and return at most `PARTIAL`. Retry no source automatically.

After the bounded reads finish, freeze the observation snapshot as the explicit revision for the canonical manifest containing every declared entry and its final checked, omitted, unsupported, unreadable, unvalidated, or changed disposition. Mint the run ID only now:

```text
RDOC-RUN-<UTC-basic-milliseconds>-<snapshot8>-<profile8>
```

Derive the exact canonical output route from the artifact ID and this run ID, revalidate its parent chain, and require the target to be absent. A collision is `BLOCKED`; mint and preview a new run rather than overwriting.

### 3. Ask for bounded intent attestations

Present the observation IDs and Unknowns before asking questions. Ask neutral, bounded questions only where the answer distinguishes approved intent from defect, workaround, legacy behavior, experiment, or unresolved choice. Stop at the clarification-round ceiling; unanswered items remain Unknown.

Each attestation record conforms to `cgs.reverse-document-attestation/v1` and includes exact question, displayed options, exact answer, linked observation/unknown IDs, UTC timestamp, and canonical record revision.

Copy an identity only when the user explicitly provides it for this attestation. Preserve it verbatim and set `attestation-status: USER_SUPPLIED_IDENTITY`. Do not infer identity from account metadata, repository authorship, filesystem user, email, OS login, task owner, or prior conversations. If intent is confirmed without an identity, use `UNVERIFIED_IDENTITY` and `attested-by: unverified`. If no intent is confirmed, use `NONE`.

Attestation establishes only what the user stated. It does not prove implementation, correctness, signature authenticity, organizational approval, or permission to change/write anything.

### 4. Isolate proposals and architecture decisions

Any behavior not evidenced in the checked implementation is `PROPOSED_CHANGE_UNIMPLEMENTED`. Put it only in `Gaps & Proposals — UNIMPLEMENTED` or `Decision Candidates — NOT ADRs`, with:

- linked observation/unknown IDs;
- `implementation-status: NOT_OBSERVED_OR_UNIMPLEMENTED`;
- `decision-status: PROPOSED_ONLY`;
- proposed owner and affected code/tests/docs;
- risks and validation evidence required.

Never place it in Observed Behavior, current rules/formulas, current architecture, acceptance criteria, or User-Attested Intent. A user may attest the desired outcome, but that changes only the attestation row; implementation status remains unimplemented.

For architecture, present decision candidates neutrally. Only the user or designated decision authority can choose one. A choice still requires a separate canonical ADR owner, numbered route, schema, review, and authorization. This workflow records the handoff requirement and stops.

### 5. Embed immutable provenance

Before rendering prose, create a canonical `cgs.reverse-document-provenance/v2` manifest containing:

- request path/schema/expected/actual revision;
- project root, artifact ID, run ID, selected profile, profile source path/revision;
- output route and `ABSENT` baseline;
- canonical inventory and observation snapshot revisions;
- every included, omitted, unsupported, unreadable, or changed source path/revision/size/type/generated state/ranges/disposition/reason;
- build/source-tree/commit identity when supplied, clearly marked supporting context;
- dependency edges/order/depth and requested/effective/consumed budgets;
- parser, adapter, observation tool, and skill/profile names and versions; unavailable version fields are explicit `UNAVAILABLE` and cap dependent claims at Unknown/Partial;
- every observation, attestation, Unknown/inference, contradiction, and proposal ID with evidence links/revisions;
- attestation status, verbatim supplied identity or `unverified`, and record revisions;
- prior-report path/revision and validated lineage/delta, or `NOT_SUPPLIED`;
- coverage/status, authority `NONAUTHORITATIVE_OBSERVATION`, and limitations.

canonicalize and validate the manifest, then embed it unchanged. The final report revision is an external write receipt and must not be placed inside bytes whose validate its declared revision would circularly change.

### 6. Render and authorize one immutable report

Render every stable profile section exactly once. A material statement must resolve to fact-table or attestation IDs. Show the complete candidate, fact-class summary, unsupported/omitted scope, provenance manifest/revision, target path, and limitations.

Completion semantics:

- `OBSERVATION_COMPLETE`: every declared entry is supported and checked, every material claim is classified/evidenced, every profile section is present, and no essential conflict/Unknown prevents the bounded observation from being complete;
- `OBSERVATION_PARTIAL`: a safe report exists but omissions, unsupported/unreadable/changed evidence, unavailable tool provenance, or essential Unknowns limit coverage;
- `OBSERVATION_DRAFT`: the complete read-only candidate exists but bounded user attestation/content questions remain.

Even COMPLETE is non-authoritative.

Writing is optional. Before a write, present one exact mutation manifest:

- operation `CREATE`;
- exact run-specific target and `must_not_exist` precondition;
- byte-for-byte candidate, byte length, and revision;
- request/profile/inventory/snapshot/provenance revisions;
- output owner and one recorder;
- `files_to_create: 1`, `files_to_modify: 0`, `files_to_delete: 0`;
- explicit non-writes.

Ask the user to authorize exactly this create. If content, revision, route, owner, recorder, or evidence snapshot changes, preview again. Content approval or attestation is not write authorization.

Immediately before writing, revalidate request, profile, all included source revisions, observation snapshot, attestation records, candidate revision, parent-path safety, and target absence. On any drift, return `BLOCKED` and write nothing. Otherwise create the exact bytes atomically where supported, read back, validate schema/class boundaries, record the final revision externally, and enumerate the one changed path.

## Outcomes and recovery

Return exactly one primary outcome:

- `COMPLETE`: complete bounded observation and, if authorized, exact verified report creation;
- `PARTIAL`: a safe observation exists but coverage/evidence/tool support is incomplete;
- `DRAFT`: read-only candidate exists and bounded questions remain;
- `BLOCKED`: authorization, route collision, target ownership, or compare-and-swap precondition failed;
- `ERROR`: request/profile/scope/path/adapter validation prevented trustworthy observation.

Every outcome includes run/artifact/profile identity, authority, request/profile/inventory/snapshot/provenance revisions, target path/revision or `NOT_WRITTEN`, exact budgets consumed, coverage and included/omitted/unsupported lists, class counts and IDs, attestation status/record revisions, Unknowns/inferences, unimplemented proposals, prior lineage, write authorization state, and `auto_executed: false`.

On interruption, resume only from the same exact request/profile/source/prior/candidate revisions. Drift invalidates dependent observations, attestations about displayed evidence, and authorization. Never reuse stale content or approval.

Return at most one next action: resolve one named evidence/attestation/coverage issue, or hand the immutable non-authoritative report to the appropriate design/concept/architecture decision owner for an independently authorized promotion decision. Do not invoke it.

End every result with this meaning:

> This immutable report is a bounded, non-authoritative observation of exact checked evidence. Observed facts, unverified inferences, user-attested intent, unknowns, and unimplemented proposals remain separate. Omitted and unsupported scope is explicit. It is not an approved GDD, concept, architecture specification, ADR, implementation, or runtime-completeness claim.
