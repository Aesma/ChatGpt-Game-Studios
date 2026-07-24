# Contract Specification: `reverse-document`

## Purpose

This specification validates `reverse-document` as a hard-bounded brownfield observation workflow. It may create one immutable, non-authoritative report from exact checked implementation evidence. It must keep observed facts, unverified inferences, explicit user-attested intent, unknowns, and unimplemented proposals machine-readably separate.

## Contract identity

- Request schema: `cgs.reverse-document-request/v2`
- Inline report/profile schema: `reverse-document-profile-v2`
- Provenance schema: `cgs.reverse-document-provenance/v2`
- Attestation schema: `cgs.reverse-document-attestation/v1`
- Authority: `NONAUTHORITATIVE_OBSERVATION`
- Skill source: `.agents/skills/reverse-document/SKILL.md`
- Metadata source: `.agents/skills/reverse-document/agents/openai.yaml`

## Invocation contract

Only this form is accepted:

```text
$reverse-document --manifest <request-path> --expect-manifest <sha256:...>
```

Both flags are required exactly once. The manifest must be a regular repository-local file with schema v2 and exact expected hash. No arguments prints usage and performs zero source reads, questions, writes, delegates, or verdicts. Unknown flags, moving aliases, directories, malformed hashes, traversal, symlink/reparse escapes, or schema mismatch return `ERROR`.

The request controls only proposed scope. It is not intent attestation, content approval, promotion approval, or write authorization.

## Required invariants

### A. P0 safety invariants retained

1. The three missing external template paths are never used; `reverse-document-profile-v2` is inline, versioned, structurally checked, and exact-byte hash-bound before source reads.
2. Missing, malformed, duplicated, unreadable, or hash-mismatched profile returns `ERROR — PROFILE_UNAVAILABLE`, with zero source analysis and writes.
3. Every row has exactly one class: `OBSERVED`, `USER_ATTESTED_INTENT`, `UNKNOWN`, or `PROPOSED_CHANGE_UNIMPLEMENTED`.
4. Bugs, workarounds, experiments, comments, tests, names, patterns, and commits cannot establish approved intent.
5. Missing/recommended behavior appears only under UNIMPLEMENTED/NOT ADR sections, never as current behavior, rules, architecture, acceptance criteria, or implementation.
6. At most one previously absent non-authoritative report may be created after exact authorization; authoritative artifacts and prior reports are read-only.

### B. Repository-local scope and target validation — RDOC-004

1. Request, every source, optional prior report, output target, and all existing output-parent segments normalize under the repository root.
2. Traversal, outside-root resolution, symlink, junction, reparse point, mount escape, special device, socket, pipe, duplicate, and case-collision inputs are rejected.
3. Source bodies must be individually declared regular files. Directories are descriptive labels only and never implicit/unbounded read scopes.
4. Declared and actual path, size, media/language type, generated state, and SHA-256 are compared before use.
5. Output must match the profile route, its parent chain must remain safe, and the final run-specific target must not exist.
6. Archives/binaries/executables/object files without an explicit safe read-only adapter are `UNSUPPORTED`; no parser is guessed.

### C. Inventory-first bounded sampling — RDOC-005

1. The canonical inventory is frozen and hashed before source-body reads.
2. Processing order is deterministic by priority, dependency depth, normalized path, and expected hash.
3. Dependencies affect ordering but cannot expand beyond exact declared inventory.
4. Request budgets may only lower fixed ceilings: manifest 256 KiB, 256 entries, 32 bodies, 256 KiB/file, 1 MiB aggregate body bytes, 512 KiB parsed text, depth 3, 128 edges, 8 generated bodies, 512 KiB prior report, 3 clarification rounds, and 512 KiB output.
5. The workflow stops before a read that would exceed a ceiling.
6. Every omitted entry retains path/hash/size/type/dependency and reason: `OMITTED_INVENTORY_BOUND`, `OMITTED_BUDGET`, `OMITTED_DEPENDENCY_BOUND`, `UNSUPPORTED`, `UNREADABLE`, or `CHANGED_DURING_RUN`; an unvalidated entry is never presented as checked.
7. Omission/unsupported coverage prevents COMPLETE and yields `PARTIAL` when at least one safe source was checked; no safely checkable essential source yields `ERROR` and zero writes.
8. The report never claims sampled evidence represents omitted code.

### D. Architecture report is not an ADR — RDOC-006

1. Architecture output uses only `observed-architecture-report` and its non-authoritative route.
2. It cannot allocate an ADR number, write `adr-NNNN-slug.md`, assign ADR status, or claim an observed pattern is a decision.
3. Rationale is Unknown unless explicitly attested; alternatives remain `Decision Candidates — NOT ADRs` and `PROPOSED_ONLY`.
4. An architecture decision requires explicit user/decision-authority choice plus a separately authorized canonical ADR owner/schema/review.
5. Even attested rationale in this report is not an ADR decision receipt.

### E. Unique canonical routing — RDOC-007

Exactly one profile and one route pattern exist per artifact type:

| Artifact/profile | Route |
|---|---|
| observed design | `docs/reverse-document/design/<artifact-id>/<run-id>.md` |
| observed architecture | `docs/reverse-document/architecture/<artifact-id>/<run-id>.md` |
| observed concept | `docs/reverse-document/concept/<artifact-id>/<run-id>.md` |

Profile/type/route disagreement is `ERROR`. No second concept location, authoritative route, date-only path, or caller-selected alternate is legal.

### F. Immutable version/hash/tool provenance — RDOC-008

1. Every report embeds unchanged canonical `cgs.reverse-document-provenance/v2` bytes and their SHA-256.
2. Provenance contains request path/schema/expected/actual hash; project/artifact/run identity; profile path/version/hash; route/ABSENT baseline; inventory and observation-snapshot hashes; every included/omitted/unsupported/unreadable/changed file with path/hash/size/type/ranges/disposition; supporting build/tree/commit identity; dependency order; requested/effective/consumed budgets; parser/adapter/tool/skill versions; all claim/attestation/proposal IDs and evidence; attestation identity/status; prior lineage; coverage/status/authority/limitations.
3. Missing tool/adapter version is explicit `UNAVAILABLE` and caps dependent claims at Unknown/Partial.
4. VCS identity and timestamps are supporting context, never substitutes for source hashes.
5. The final observation snapshot is frozen after bounded reads and binds every checked/omitted/unsupported/unreadable/unvalidated/changed disposition. Only then is run ID `RDOC-RUN-<UTC-basic-milliseconds>-<snapshot8>-<profile8>` minted; the output route is create-only.
6. Existing/prior reports are immutable. A later run uses a new route and exact prior path/hash lineage; in-place merge, overwrite, or append is forbidden.
7. Final report SHA-256 is an external read-back receipt, avoiding a circular self-hash claim.

### G. Truthful attestation identity — RDOC-009

1. Every attested claim links an immutable `cgs.reverse-document-attestation/v1` record with exact question, options, answer, linked IDs, UTC timestamp, and record SHA-256.
2. Identity is copied verbatim only when explicitly supplied by the user for the attestation.
3. Explicit identity uses `USER_SUPPLIED_IDENTITY`; it is not called verified, signed, or approved.
4. Confirmed intent without identity uses `UNVERIFIED_IDENTITY` and `attested-by: unverified`; no confirmation uses `NONE`.
5. Identity must not be inferred from account metadata, repository authorship, filesystem user, email, OS login, task owner, or earlier context.
6. `verified-by`, `approved-by`, and `VERIFIED_IDENTITY` are prohibited.
7. Attestation does not prove implementation/correctness or authorize a write/change.

### H. Fact, inference, intent, and proposal separation — RDOC-010

1. `OBSERVED` requires exact source/build/test/config/runtime evidence with path/hash/range or serialized key.
2. An inference is never Observed; it is an `UNKNOWN` row with `statement-kind: INFERENCE_UNVERIFIED`, cited observed premises, and required resolution evidence.
3. `USER_ATTESTED_INTENT` requires the exact explicit attestation record; source structure, comments, tests, and model confidence cannot populate it.
4. `PROPOSED_CHANGE_UNIMPLEMENTED` records desired behavior only with `implementation-status: NOT_OBSERVED_OR_UNIMPLEMENTED` and `decision-status: PROPOSED_ONLY`.
5. No row combines classes, and confidence cannot promote inference to fact or intent.
6. Narrative material resolves to row/attestation IDs and preserves the same class label.
7. Static inspection does not prove runtime reachability, performance, fun, correctness, completeness, or production readiness.

## Profile requirements

The skill defines three inline profiles with stable headings:

- Design: RDD-01 through RDD-09, including Scope & Provenance, Observed sections, User-Attested Intent, Unknowns/Inferences/Contradictions, UNIMPLEMENTED proposals, and Promotion Requirements.
- Architecture: RDA-01 through RDA-08, including observed components/flows/constraints, attested intent, Unknowns, `Decision Candidates — NOT ADRs`, and Promotion Requirements.
- Concept: RDC-01 through RDC-08, including observed prototype behavior/mechanics/feasibility, attested intent/fantasy, Unknowns, UNIMPLEMENTED proposals, and Promotion Requirements.

Every section appears exactly once. Claims about feel, fun, success, fantasy, or feasibility need direct runtime/playtest/telemetry evidence or explicit attestation; otherwise they remain Unknown/inference.

## Immutable write protocol

1. Freeze and hash request, profile, inventory, observation snapshot, included source bytes, attestations, provenance, candidate, and absent target.
2. Show the complete candidate and one mutation manifest: `CREATE`, exact target, `must_not_exist`, bytes/length/hash, evidence hashes, owner/recorder, create 1/modify 0/delete 0, and non-writes.
3. Obtain explicit authorization for that exact create. Content approval and attestation are insufficient.
4. Revalidate all hashes, path safety, target absence, candidate, and identities immediately before writing.
5. Drift/collision returns `BLOCKED`, writes nothing, and requires a new preview/authorization.
6. On success, atomically create where supported, read back, validate schema/class boundaries, record external SHA-256, and enumerate exactly one changed path.
7. No merge, overwrite, append, downstream invocation, commit, push, or publication occurs.

## Outcome contract

Exactly one outcome is returned:

- `COMPLETE`
- `PARTIAL`
- `DRAFT`
- `BLOCKED`
- `ERROR`

Every result includes artifact/run/profile/authority, request/profile/inventory/snapshot/provenance hashes, target/hash or `NOT_WRITTEN`, requested/effective/consumed budgets, included/omitted/unsupported scope, class counts/IDs, attestation status/record hashes, Unknowns/inferences, unimplemented proposals, prior lineage, authorization state, and `auto_executed: false`.

COMPLETE always means only complete within the exact bounded observation scope and remains non-authoritative.

## Static and behavioral cases

### Positive cases

- A valid exact v2 request with supported sources produces deterministic inventory/snapshot/provenance hashes and a source-cited fact table.
- A budget overflow after checked sources yields PARTIAL, lists every remaining manifest entry and reason, and makes no omitted-scope claim.
- A comment saying `intentional` is an observed comment while rationale remains an inference/Unknown.
- A user confirms intent without identity; the record is `UNVERIFIED_IDENTITY`, `attested-by: unverified`.
- An explicitly supplied identity is preserved verbatim as `USER_SUPPLIED_IDENTITY`, never verified/approved.
- Architecture patterns and alternatives remain observed structure/NOT ADR candidates pending explicit user decision and independent ADR ownership.
- A second run links the exact old report/hash but creates a new run-specific report.
- Exact write authorization creates and verifies one absent path.

### Negative cases

- No-argument invocation reads sources or guesses a target/profile.
- A caller raises a hard ceiling or uses a directory as an unlimited scope.
- A symlink/junction/reparse/outside-root/special/binary-without-adapter source is read.
- Unsupported or omitted files disappear from coverage or COMPLETE is returned.
- A recognized pattern, test, comment, bug, or workaround becomes approved intent.
- An inference is labeled Observed or model confidence promotes it.
- An unimplemented edge case enters current behavior/rules/architecture/acceptance criteria.
- An architecture report receives an ADR number/path/status.
- Concept output can choose between two locations.
- Provenance omits source hashes, scope, tool versions, budgets, omissions, or attestation records.
- Identity is inferred or emitted as `verified-by`/verified/approved.
- Existing report is merged, overwritten, appended, or used as the output target.
- Content approval or attestation is treated as write/promotion authorization.

Any negative case is a contract failure.

## Remediation traceability

| Finding | Closure evidence |
|---|---|
| RDOC-004 | Section B validates repository-local regular-file scope, parent/target safety, type/size/count/hash, and reparse/symlink rejection |
| RDOC-005 | Section C defines inventory-first dependency ordering, non-raiseable hard ceilings, explicit unsupported/omitted entries, and PARTIAL semantics |
| RDOC-006 | Section D makes architecture output non-ADR and preserves explicit user decision plus independent ADR ownership |
| RDOC-007 | Section E defines one profile and one immutable route per artifact type |
| RDOC-008 | Section F defines immutable v2 provenance with exact source/profile/tool/version/scope hashes and run lineage |
| RDOC-009 | Section G permits only explicit user-supplied identity and otherwise records `unverified` |
| RDOC-010 | Section H and all behavioral cases prohibit intent inference and separate facts, inferences, attestations, unknowns, and unimplemented proposals |

## Required disclaimer semantics

Every result states that the immutable report is a bounded, non-authoritative observation of exact checked evidence; observed facts, unverified inferences, user-attested intent, unknowns, and unimplemented proposals remain separate; omitted/unsupported scope is explicit; and the report is not an approved GDD, concept, architecture specification, ADR, implementation, or runtime-completeness claim.
