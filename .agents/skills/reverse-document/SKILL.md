---
name: reverse-document
description: "Create a non-authoritative, provenance-bound observation report from bounded implementation evidence while separating observed behavior, attested intent, unknowns, and unimplemented proposals."
---

# Reverse Document

Reverse documentation records what selected implementation evidence demonstrates. It
does not treat code, comments, tests, prototypes, bugs, workarounds, or experiments as
approved product or architecture intent.

## Invocation contract

Invoke only as:

`$reverse-document --manifest {reverse-document-request-path}`

Validate arguments before reading sources, asking intent questions, delegating, or
writing. With no manifest, show the usage line and stop with no reads, writes,
delegates, or verdict. Reject unknown/duplicate flags, missing values, directories,
unsafe IDs, unsupported schemas, path traversal, and symlink/junction escapes.

The request manifest requires:

- `Artifact Type: reverse-document-request` and `Schema Version: 1`;
- stable artifact/run IDs and profile `observed-design-report`,
  `observed-architecture-report`, or `observed-concept-report`;
- mode `create` or `merge`, exact canonical output path, and expected target SHA-256
  or `ABSENT`;
- exact source-file inventory with normalized path, expected SHA-256, language/type,
  expected size, inclusion reason, and optional stable build/source-tree/commit hash;
- dependency edges and the maximum allowed dependency depth;
- maximum file count, bytes, tokens, generated-file count, and per-file size;
- actual observer task ID, recorder task ID, mutation authority, output owner,
  maximum clarification rounds, and explicit non-writes;
- expected inline profile ID and, when pinned, expected profile-source SHA-256.

Directories are not implicit read scopes. A directory target is accepted only when
the manifest already contains its exact deterministic file inventory and inventory
hash. Resolve every real path under the repository root and accept regular readable
files only. Do not follow undisclosed dependencies, glob the repository, or inspect
omitted files.

Canonical routing is unique:

| Profile | Exact route |
|---|---|
| `observed-design-report` | `docs/reverse-document/design/{artifact-id}.md` |
| `observed-architecture-report` | `docs/reverse-document/architecture/{artifact-id}.md` |
| `observed-concept-report` | `docs/reverse-document/concept/{artifact-id}.md` |

Reject an output path that does not match its profile. This workflow never writes
directly to authoritative GDD, ADR, architecture, concept, source, prototype, or
registry paths.

## Versioned inline profile source

The three schemas below are the canonical templates. Their profile ID is
`reverse-document-profile-v1`; their source is this exact `SKILL.md`. At startup:

1. read this file and compute its exact-byte SHA-256;
2. verify the frontmatter name, profile ID, common header fields, selected profile
   heading table, and stable section IDs are present exactly once;
3. compare the hash with a manifest-pinned profile hash when supplied;
4. record `profile_source_path` and `profile_source_sha256` in the report.

If the profile source is missing, unreadable, malformed, duplicated, or hash-mismatched,
return `Analysis Status: ERROR — TEMPLATE PROFILE UNAVAILABLE`, perform zero source
analysis and zero writes, and emit no document verdict. Do not fall back to a guessed
template or another artifact type.

### Common machine-readable header

Every report begins with:

```markdown
---
artifact-type: observed-design-report | observed-architecture-report | observed-concept-report
schema-version: reverse-document-profile-v1
authority: NON_AUTHORITATIVE_OBSERVATION
artifact-id: <stable ID>
run-id: <stable ID>
status: OBSERVATION_DRAFT | OBSERVATION_PARTIAL | OBSERVATION_COMPLETE
observer-task-id: <actual task that produced observations>
source-inventory-sha256: <canonical inventory hash>
provenance-manifest-sha256: <canonical embedded manifest hash>
profile-source-path: .agents/skills/reverse-document/SKILL.md
profile-source-sha256: <exact bytes hash>
attestation-status: NONE | UNVERIFIED_IDENTITY | VERIFIED_IDENTITY
attested-by: unverified | <identity supplied explicitly by the user>
generated-at-utc: <ISO-8601 UTC>
---
```

Never emit `verified-by`. Never invent a person's name, account, role, or signature.
An identity may be copied only from an explicit user-provided attestation field or
answer and must be stored verbatim with its record hash.

### Profile: observed-design-report

| Stable ID | Exact H2 heading | Required content |
|---|---|---|
| RDD-01 | Scope & Provenance | bounded scope, hashes, coverage, omissions, tools |
| RDD-02 | Observed Behavior | source-cited runtime/code behavior only |
| RDD-03 | Observed Rules, Values & Formulas | exact expressions/constants and execution conditions |
| RDD-04 | Observed State, Data & Events | implemented state transitions, ownership and events |
| RDD-05 | Observed Dependencies | evidenced calls/data/resource relationships |
| RDD-06 | User-Attested Intent | only exact attested claims and record IDs |
| RDD-07 | Unknowns & Contradictions | unresolved meaning, suspected defects/workarounds, conflicting evidence |
| RDD-08 | Gaps & Proposals — UNIMPLEMENTED | missing cases/improvements marked not observed/not implemented |
| RDD-09 | Promotion Requirements | decisions/evidence needed for an authoritative design owner |

### Profile: observed-architecture-report

| Stable ID | Exact H2 heading | Required content |
|---|---|---|
| RDA-01 | Scope & Provenance | bounded scope, hashes, coverage, omissions, tools |
| RDA-02 | Observed Components & Interfaces | implemented modules/types/contracts |
| RDA-03 | Observed Dependency, Data & Control Flow | source-cited relationships and lifecycle |
| RDA-04 | Observed Constraints & Trade-off Evidence | measured/encoded constraints, not assumed decisions |
| RDA-05 | User-Attested Intent | exact attested rationale and record IDs only |
| RDA-06 | Unknowns & Contradictions | ambiguous rationale, defects, legacy/workaround candidates |
| RDA-07 | Decision Candidates — NOT ADRs | proposed choices with no accepted status |
| RDA-08 | Promotion Requirements | user decision and ADR-owner requirements |

An observed pattern is not an architecture decision. This workflow never creates an
ADR or assigns Accepted/Proposed/Rejected ADR status. Even an attested rationale stays
in this non-authoritative report until the decision authority and ADR owner create a
properly numbered `adr-NNNN-slug.md` under their own authorization.

### Profile: observed-concept-report

| Stable ID | Exact H2 heading | Required content |
|---|---|---|
| RDC-01 | Scope & Provenance | prototype/build/source hashes, coverage, omissions, tools |
| RDC-02 | Observed Prototype Behavior | source/build/playtest-cited behavior only |
| RDC-03 | Observed Mechanics & Loop | implemented inputs, states, outcomes and reset loop |
| RDC-04 | Observed Feasibility Evidence | actual technical results/limits, not forecasts |
| RDC-05 | User-Attested Intent & Player Fantasy | exact attested intent/feel claims and record IDs |
| RDC-06 | Unknowns & Contradictions | unknown fun/feel, bugs, exploits, incomplete evidence |
| RDC-07 | Gaps & Proposals — UNIMPLEMENTED | experiments/features/edge cases not evidenced as present |
| RDC-08 | Promotion Requirements | evidence and decisions needed for concept ownership |

Claims that something worked, felt good, was fun, or represented a player fantasy
require playtest/telemetry evidence or explicit user attestation. Otherwise classify
them as Unknown.

## Classification contract

Every fact-table row has a stable ID and exactly one class:

- `OBSERVED`: directly supported by cited source bytes/ranges, tests, serialized
  configuration, build/prototype output, or declared runtime evidence;
- `USER_ATTESTED_INTENT`: exact intent statement explicitly confirmed by the user and
  bound to an attestation record;
- `UNKNOWN`: rationale, intended behavior, ownership, correctness, or completeness is
  not established;
- `PROPOSED_CHANGE_UNIMPLEMENTED`: an edge case, desired behavior, alternative,
  fix, consolidation, or future improvement not evidenced in current implementation.

No row may combine classes. Code structure, naming, constants, comments, tests, and
commit messages may prove what text or behavior exists, but not why it was chosen or
whether it remains desired. A comment that says `temporary`, `intentional`, or `fix`
is an observed comment, not user-attested intent. Bugs, exploits, inconsistent tests,
legacy paths, and workarounds remain Observed plus Unknown/Contradiction findings;
never normalize them into intended rules.

Use stable IDs:

- `OBS-{artifact-id}-{source-hash-prefix}-{range}-{kind}` for observations;
- `ATT-{artifact-id}-{sequence}` for attestations;
- `UNK-{artifact-id}-{stable-check}` for unknowns/contradictions;
- `PROP-{artifact-id}-{stable-slug}` for unimplemented proposals.

Each row records class, claim, source path/hash/range or attestation ID, parser/tool
version, build/source identity when applicable, confidence limited to evidence
quality, and affected sections. Never use confidence to promote an inference into
intent.

## Phase 1: Validate scope and build bounded inventory

Validate profile and output route before source reads. Recompute every source and
inventory hash; reject missing/unreadable files, file-type mismatch, changed bytes,
duplicates, outside-root paths, special devices, archives/binaries without a declared
safe adapter, and oversized individual files.

Order the exact inventory by manifest priority, then dependency depth and normalized
path. Process within file/byte/token/generated-file budgets. Record every omitted path,
hash, size, dependency reason, and omission reason. Budget exhaustion yields
`Coverage Status: PARTIAL` and prevents `OBSERVATION_COMPLETE`; do not claim the
omitted code agrees with sampled evidence.

Generated code is evidence only when explicitly included and marked generated with
generator path/hash/version. It cannot establish product intent. Unsupported formats
produce a stable Unknown or ERROR when essential.

## Phase 2: Produce source-bound observations

Read only the validated inventory. Extract exact implemented mechanics, formulas,
conditions, state/data/event flows, interfaces, calls, resources, configuration and
tests appropriate to the selected profile. Cite every material claim to exact path,
SHA-256 and line/range or serialized key.

Build the fact table before narrative prose. Separate contradictory sources rather
than choosing one. If a value is magic or a pattern resembles a known architecture,
record the value/structure as Observed and its rationale as Unknown.

Static inspection does not prove runtime reachability, performance, player behavior,
fun, correctness, completeness, or production readiness. State the evidence boundary.

## Phase 3: Collect explicit intent attestations

Present observations and Unknowns to the user without embedding a preferred answer.
Ask only bounded questions needed to distinguish current approved intent from defect,
legacy behavior, experiment, or unresolved choice.

For each confirmed claim, create an immutable attestation record containing the exact
question, displayed options if any, exact answer, linked observation/unknown IDs,
identity supplied explicitly by the user or `unverified`, UTC timestamp, and canonical
record hash. Do not infer identity from account, filesystem, repository, or context.

If the user confirms intent but supplies no identity, set
`attestation-status: UNVERIFIED_IDENTITY`, `attested-by: unverified`, and preserve the
claim in User-Attested Intent with its limitation. If the user does not answer or does
not explicitly confirm, leave it Unknown. Attestation never changes observed bytes or
authorizes a design/architecture change.

## Phase 4: Route unimplemented behavior safely

Any missing edge case, safer behavior, revised formula, desired balance, refactor,
new feature, architectural alternative, or prototype improvement is a
`PROPOSED_CHANGE_UNIMPLEMENTED`. Put it only in `Gaps & Proposals — UNIMPLEMENTED` or
`Decision Candidates — NOT ADRs`.

Each proposal records source observation/unknown IDs, `implementation-status:
NOT_OBSERVED_OR_UNIMPLEMENTED`, `decision-status: PROPOSED_ONLY`, proposed owner,
affected implementation/test/docs, risks, and the evidence needed to validate it.
Never place it in Observed Behavior, current rules/formulas, acceptance criteria,
current architecture, or attested intent. Never state that it exists.

This workflow does not implement proposals, create stories/ADRs, tune values, modify
source/tests, or promote them into authoritative design.

## Phase 5: Draft one non-authoritative report

Render the selected inline profile in scratch. Embed a canonical provenance manifest
covering:

- request/profile source path/hash, artifact/run/observer IDs and UTC time;
- every included/omitted source path/hash/size/type/range, build/tree/commit identity,
  inventory order, dependency edges and budgets consumed;
- parser/adapter/tool names and versions;
- every observation, attestation, unknown and proposal ID with evidence links;
- coverage and attestation status, target route/base hash, and explicit authority
  `NON_AUTHORITATIVE_OBSERVATION`.

Compute the canonical embedded provenance hash and put it in the header. Show the full
candidate, classification summary, coverage/omissions, attestations and target path to
the user. Content approval is not file authorization.

Completion semantics:

- `OBSERVATION_COMPLETE`: all declared sources and required profile sections are
  covered, every claim is classified/evidenced, and no essential parse conflict or
  identity gap remains;
- `OBSERVATION_PARTIAL`: budget omissions, unsupported essential evidence, unresolved
  merge conflict, or critical Unknown prevents full coverage;
- `OBSERVATION_DRAFT`: read-only candidate exists but content/attestation questions
  remain.

Even `OBSERVATION_COMPLETE` remains non-authoritative and is not an approved GDD,
concept, architecture specification, or ADR.

## Phase 6: Authorize and write exactly one artifact

Writing is optional. Before the first write, present one mutation manifest containing
operation `CREATE` or `MERGE`, exact target, expected base hash or `ABSENT`, complete
candidate hash, source/provenance/profile hashes, output owner, single recorder,
maximum bytes, and explicit non-writes. Obtain explicit mutation authorization.

For `create`, the target must remain absent. For `merge`, require a current compatible
reverse-document profile and base hash. Merge by stable observation/attestation/
unknown/proposal IDs; preserve unchanged sections and prior provenance. Surface
same-ID/different-evidence, classification, attestation, or schema conflicts for user
resolution. Never overwrite an existing target, replace unrelated bytes, or convert
an authoritative document into a reverse report.

Immediately before writing, re-hash source inventory, profile, attestations, candidate,
and target base. On drift, stop with `BLOCKED`; prior approval is stale. The one
recorder writes atomically where supported, enumerates changed paths, rejects any path
outside the manifest, reads the target back, validates schema/class boundaries, and
records final SHA-256. Scope expansion requires a new manifest and authorization.

## Output and recovery

Malformed request/profile/source/adapter returns `Analysis Status: ERROR` and zero
writes. Budget/coverage/merge limitations return `Verdict: PARTIAL`; authorization,
target collision, ownership, or CAS drift returns `Verdict: BLOCKED`. A fully covered,
authorized, read-back verified observation report may return `Verdict: COMPLETE`, but
must state `Authority: NON_AUTHORITATIVE_OBSERVATION` beside it.

Final output includes artifact/run/profile/status, target path/hash or `NOT WRITTEN`,
profile/inventory/provenance hashes, included/omitted coverage, fact-class counts,
attestation status/identity/record hashes, Unknowns, unimplemented proposals, mutation
authorization, and exactly one next action.

On interruption, resume only from a request-declared checkpoint/candidate. Re-hash
profile, sources, inventory, attestations, output base and candidate; invalidate all
dependent observations on drift. Do not reuse stale intent, approval, or provenance.

The sole next action resolves a named evidence/attestation/coverage conflict, or hands
the final non-authoritative report to the proper design/concept/architecture decision
owner for an independently authorized promotion decision. Do not invoke another
workflow or perform downstream implementation.
