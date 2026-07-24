---
name: changelog
description: "Generate one deterministic local changelog candidate from an explicit immutable Git range, source-bound net-change claims, sanitized public projection, and optional create-only CAS persistence."
---

# Changelog

Create a reproducible account of the surviving changes in one exact Git range. A
version label is not a Git object, a commit range is not a build, a build candidate is
not a deployment, a deployment is not publication, and generating a changelog is not
permission to write or publish it.

## Invocation and request

Invoke only as:

`$changelog --request <path> --expect-request <sha256>`

Both flags are required exactly once. With a missing/invalid flag or unknown argument,
show that usage and stop before project reads, Git enumeration, output, delegation, or
writes. Reject directories, moving aliases to request files, traversal, globbing,
symlink/junction/reparse escape, unsupported schema, and expected/actual request hash
mismatch.

The request is strict `cgs.changelog-request/v2` and declares:

- stable `release_id` and `run_id`, plus `scope_kind`: `commit-range`,
  `release-candidate`, or `deployed-release`;
- repository root and immutable repository identity; `from_ref`, `to_ref`, expected
  full `from_commit`, `to_commit`, `from_tree`, and `to_tree`; required ancestry and
  merge-base policy; optional exact tag ref/object/peeled-commit identity;
- presentation version as separate `version_scheme` and `version_label` fields;
- optional release date as `{ value, timezone, source_kind, source_path,
  source_sha256 }`, never an inferred clock/commit/tag date;
- intended distribution target as `{ target_id, audience, product, platforms,
  channels, regions, environments }`, separate from an actual deployment target;
- exact classification-policy and public-redaction-policy paths, schemas, versions,
  and SHA-256 hashes;
- exact explanatory context inventory with paths/hashes/types, never a directory or
  “latest” lookup;
- exact candidate receipt and deployment receipt paths/hashes when the requested scope
  needs them;
- output selection `internal` or `internal-and-player`; and
- operation `analyze-only` or `create-entry`. `create-entry` requires one normalized
  target path, `expected_target: ABSENT`, maximum bytes, creator identity, mutation
  authority/expiry, and explicit non-writes.

Unknown/repeated fields, aliases, unsupported algorithms, incomplete nested objects,
unsafe IDs, an absent required policy, or a hash mismatch are BLOCKED. Normalize
paths beneath the repository and locale-independent strings to Unicode NFC. Never
search for the latest tag/report/sprint, substitute HEAD, infer a date/target/owner,
or use a sprint/version label as a Git ref.

## Authority and non-writes

Analysis is read-only. `create-entry` authorizes only one absent target and only the
exact candidate hash presented for approval. It does not authorize appending to or
editing an existing changelog, changing Git refs/tags/commits, updating context or
receipts, building, deploying, publishing, messaging, or uploading.

Git authors are provenance, not product owners. Context authors are not release
approvers. Candidate producers cannot attest deployment. Deployment operators cannot
retroactively attest a different candidate. The model cannot supply missing human,
security, privacy, legal, release, or publication authority.

Never invent evidence, hashes, dates, targets, classifications, redactions, build
results, deployment results, or approvals. Use explicit UNKNOWN/MISMATCH/BLOCKED
states. Do not invoke another workflow.

## Canonical identities and states

Canonical serialization uses schema-declared field order, UTF-8, LF, NFC, lowercase
hex SHA-256, sorted set-valued arrays, and no timestamps except evidence timestamps.
Hash exact bytes before parsing and also record canonical record hashes.

```text
range_identity_sha256 = sha256(repository identity + from/to commit/tree IDs +
  merge-base + ancestry result + commit-list hash + net-diff hash)
version_identity_sha256 = sha256(version scheme + exact version label + tag identity)
date_identity_sha256 = sha256(date value/timezone + source kind/path/hash)
target_identity_sha256 = sha256(target ID + audience/product + sorted platforms/
  channels/regions/environments)
release_identity_sha256 = sha256(release ID + range/version/date/target identities)
claim_identity_sha256 = sha256(release identity + primary category + sorted surviving
  net-hunk hashes + normalized observed effect)
candidate_identity_sha256 = sha256(build ID + artifact/source/tree/platform/config +
  result + producer/time + receipt hash)
deployment_identity_sha256 = sha256(deployment ID + candidate/artifact/source/tree +
  environment/channel + result + deployer/time + evidence hashes + receipt hash)
```

Report these independently:

- `version_status`: `NOT_PROVIDED`, `LABEL_ONLY`, `TAG_VERIFIED`, or `MISMATCH`;
- `date_status`: `NOT_PROVIDED`, `SOURCE_VERIFIED`, or `MISMATCH`;
- `target_status`: `DECLARED`, `DEPLOYMENT_MATCHED`, or `MISMATCH`;
- `range_status`: `VERIFIED` or `MISMATCH`;
- `candidate_status`: `NOT_PROVIDED`, `VERIFIED_CANDIDATE`, or `MISMATCH`;
- `deployment_status`: `NOT_PROVIDED`, `VERIFIED_DEPLOYMENT`, or `MISMATCH`;
- `narrative_status`: `RESOLVED`, `HAS_UNRESOLVED`, or
  `SANITIZATION_BLOCKED`;
- `artifact_status`: `GENERATED`, `CREATED`, `PARTIAL`, `BLOCKED`, or
  `RECOVERY_REQUIRED`; and
- `publication_status`: always `NOT_PUBLISHED`.

Generated-at time is provenance only and cannot become the release date. A verified
tag proves version/tag identity only. A verified range proves source inclusion only.
A candidate receipt proves only its exact artifact. Only an exactly chained successful
deployment receipt can prove deployment to the matching target; it still does not
prove public availability or publication.

## Phase 1 — Parse, resolve, and pin the exact range

Strictly parse the request and policies. Confirm a Git work tree and required object
availability. A non-Git root, missing/shallow object, unsupported object format, parse
failure, or policy mismatch returns BLOCKED with zero writes.

Peel both refs to full immutable commits and trees and compare all expected IDs.
Require `from_commit` to be an ancestor of `to_commit`; record the full merge base and
ancestry result. The range is exactly `from_commit..to_commit`: from excluded, to
included. Resolve tag object/type/signature/peeled commit when declared. Unrelated
histories are not release evidence.

Record repository identity, object format, current HEAD and branch/detached state,
worktree/index status hash, submodule/LFS pointer state, and generated-at UTC. Dirty
or untracked bytes are outside the range. Re-resolve moving ref text before output and
again before create; any drift invalidates analysis/authority.

## Phase 2 — Enumerate topology and compute surviving net change

Enumerate every reachable commit in the range without a 30/100/N cap: full commit,
parent and tree IDs; author/committer identities and times; message bytes; decorations;
and topology. Record the count and canonical ordered commit-list hash.

Compute the complete final tree diff from `from_commit` to `to_commit`, including
add/delete/modify/type/mode, rename/copy identity, submodule/LFS pointer changes,
binary markers, line stats, patches, and stable hunk hashes. Record the canonical
net-diff hash. A budget may stop safely with PARTIAL, but must never truncate and call
the range complete.

Merge/revert/fixup rules are deterministic:

- merge commits stay in provenance; surviving net hunks are claimed once, never once
  per parent/path traversal;
- explicit revert messages are hints until patch/hunk relationships verify them;
- fully removed changes are `EXCLUDED_NET_ZERO`, retain original/revert trace, and
  produce no current or player claim;
- partial reverts claim only surviving hunks and link original/revert commits;
- fixup/squash/cleanup commits remain provenance while claims describe only the final
  surviving effect; and
- empty range/diff remains explicit and cannot be populated from plans or documents.

Deduplicate by exact surviving hunk identity first, then by
`claim_identity_sha256`. One claim may list multiple supporting commits/merge paths;
never merge distinct effects merely because prose is similar. Recompute topology,
commit-list, hunk, and net-diff hashes before final output/create.

## Phase 3 — Create source-bound claims and classify deterministically

Each `cgs.changelog-claim/v2` contains stable claim ID, release/range identity, exact
surviving path/patch/hunk hashes, supporting commit IDs, observed net effect, affected
surface, evidence confidence, primary category, classification rule/attestation,
context links, receipt links, unresolved questions, and public eligibility.

The primary category is exactly one of `SECURITY_INTERNAL`, `FIX`, `BALANCE`,
`FEATURE`, `IMPROVEMENT`, `TECHNICAL`, `DOCS`, `KNOWN_ISSUE`, or `UNRESOLVED`.
Apply only the frozen classification policy's exact evidence predicates, rule IDs,
and precedence. Security wins over all public categories; otherwise a multiple/no-rule
match is UNRESOLVED unless an exact human classification attestation resolves it.
Commit wording, file names, directories, authors, sprint state, and model judgment
alone never determine a category.

Sprint/GDD/story/issue materials are `CONTEXT_ONLY_NOT_RELEASE_EVIDENCE`. They may
explain an already surviving diff only when path/hash and claim mapping are explicit;
they never prove inclusion, build, deployment, rationale, or ownership. A balance or
design-rationale claim needs both surviving value evidence and an exact approved or
attested design source. Otherwise retain only the observed change and UNRESOLVED
rationale. Unresolved claims remain internal and prevent a resolved/player narrative.

## Phase 4 — Verify version, date, target, candidate, and deployment

Validate version syntax against its declared scheme. If a tag is evidence, its peeled
commit must equal `to_commit`; otherwise version/tag state is MISMATCH. Verify the date
only from the declared immutable source. Do not turn tag time, commit time, build time,
deploy time, or today's date into the release date without that exact source contract.

Validate the intended target independently. A candidate receipt must use a supported
immutable schema and bind build ID, artifact hash, `to_commit/to_tree`, platform,
configuration, successful result, producer, time, and receipt hash. A deployment
receipt must bind deployment ID, that exact candidate/artifact/source/tree,
environment/channel/target, successful result, deployer, deployed-at time, logs and
receipt hashes. A target/candidate/deployment mismatch forbids deployed/released/live/
available wording. Missing or mismatched receipts leave a commit-range narrative
possible but make the requested candidate/deployed scope PARTIAL or BLOCKED.

## Phase 5 — Render a deterministic internal entry

Render `cgs.changelog-entry/v2` with fixed category order:

1. Security — Internal
2. Fixes
3. Balance
4. Features
5. Improvements
6. Technical
7. Documentation
8. Known Issues
9. Unresolved
10. Excluded Net-Zero / Revert Trace
11. Provenance

Within a category sort by `claim_identity_sha256`; sort evidence IDs/hashes
lexicographically. Omit no unresolved state, but use a fixed empty-section token.
Given identical request and evidence bytes, output bytes and candidate hash must be
identical; generated-at is taken only from a supplied generation receipt or excluded
from the hashed narrative body.

The header records release/version/date/target/range identities and independent
candidate/deployment/publication states. Each claim shows its ID and source evidence.
Provenance records original/resolved refs, commit/tree/tag/merge-base IDs, repository
state, commit-list/net-diff hashes and counts, policy/context/receipt hashes, schema and
tool version. A commit-range is labelled draft; a candidate is labelled candidate.

## Phase 6 — Build an optional sanitized player projection

Build the player draft independently from eligible claim records; never reformat the
internal prose. Apply the exact frozen redaction policy and deterministic scanners to
both source fields and final bytes for:

- credentials, tokens, keys, authorization headers, connection strings, secrets, and
  suspicious high-entropy values;
- personal data, names/emails/usernames, private player/customer data, and identifiers;
- internal issue/story IDs, commit hashes, paths, hosts/IPs/domains, logs,
  infrastructure, build/deploy internals, and security-control details; and
- unreleased vulnerabilities/exploits, anti-cheat or abuse detection, embargoed
  content, legal/privacy matters, and unsafe workaround instructions.

`SECURITY_INTERNAL` is default-deny. Ambiguous sensitive material is excluded, never
softened speculatively. Redaction receipt `cgs.changelog-redaction/v1` contains only
claim/input hashes, rule/version/hash, action, reason code, scanner result, and output
hash—never removed secret/PII bytes. Pseudonymize identities in internal summaries
where policy requires it.

Re-scan final public bytes. Any policy/scanner uncertainty or finding returns
SANITIZATION_BLOCKED and no player artifact. A successful draft begins
`PLAYER CHANGELOG DRAFT — NOT REVIEWED OR PUBLISHED`, includes exact
version/date/target/candidate/deployment statuses, and never claims more availability
than receipts prove. Never post, upload, email, message, or publish it.

## Phase 7 — Optional create-only CAS persistence

`analyze-only` writes nothing and returns exact candidate bytes/hash in the response.
`create-entry` may create one immutable new file only. The normalized target must be
inside the authorized root, its parent must already exist, and target state must be
ABSENT at request validation, preview, authorization, and commit. Existing files,
entries, indexes, manifests, and history are immutable; there is no append, insert,
revise, upsert, overwrite, truncate, normalize, delete, or rename-existing mode.

Preview one mutation manifest with request/range/release/policy/context/receipt hashes,
target path and expected ABSENT state, exact candidate hash/bytes, creator, create-only
primitive, maximum bytes, authority/expiry, and non-writes. Narrative approval is not
mutation approval.

Immediately before create, CAS the request, refs/objects/trees, repository state,
policies, context, receipts, candidate bytes, parent identity, and target ABSENT state.
Use an atomic no-replace/create-new primitive; if unavailable, write nothing. If the
target appears or any input drifts, write nothing and return BLOCKED. Flush, close,
read back, strictly parse, and hash the created file. A post-create mismatch is
RECOVERY_REQUIRED; report exact target/expected/actual hashes and do not overwrite or
silently delete evidence.

## Phase 8 — Terminal result

Return release/run/scope IDs; all canonical identities and source hashes; original and
resolved refs; ancestry/topology/counts; net/revert/dedup summary; claim/category/
evidence/unresolved records; privacy scan counts without sensitive bytes;
version/date/target/candidate/deployment/publication states; candidate/output/target
hashes; exact reads/non-writes; blockers; and exactly one legal next action.

Use only:

- `Artifact Status: GENERATED` — deterministic local candidate returned, zero writes;
- `Artifact Status: CREATED` — one absent target created by CAS and verified;
- `Artifact Status: PARTIAL` — bounded truthful analysis exists but required evidence
  or classification is incomplete;
- `Artifact Status: BLOCKED` — safe analysis/create cannot proceed; or
- `Artifact Status: RECOVERY_REQUIRED` — exclusive create occurred but verification
  failed and the exact new target needs owner-directed recovery.

Never return COMPLETE, imply publication, auto-fix evidence, or auto-run another mode.
