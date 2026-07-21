---
name: changelog
description: "Generate a reproducible local changelog entry from an explicit Git range, source-bound claims, optional candidate/deployment receipts, and a history-preserving keyed upsert."
---

# Changelog

Generate a local narrative about net committed changes. A version label is not a Git
range, a Git range is not a build candidate, a candidate is not deployed, and a
changelog write is not publication.

## Invocation contract

Invoke only as:

`$changelog --manifest {changelog-request-path}`

Validate the manifest before reading Git, context documents, or the changelog. With
no manifest, print the usage line and stop with no reads, writes, delegates, or
verdict. Reject unknown flags, missing values, directories, unsafe IDs, path
traversal, symlink/junction escapes, and unsupported schemas.

The manifest requires:

- `Artifact Type: changelog-request` and `Schema Version: 1`;
- stable `release_id`, `run_id`, and explicit `scope_kind`:
  `commit-range`, `release-candidate`, or `deployed-release`;
- optional human-facing `version_label`, separately from exact `from_ref` and
  `to_ref`; the manifest cannot use a sprint number in place of a Git ref;
- expected repository root/identity, hash algorithm, and exact ref-resolution policy;
- optional expected full `from_commit`, `to_commit`, tag-object hash, merge-base hash,
  and final tree hashes;
- exact candidate/build receipt path/hash for `release-candidate` or
  `deployed-release`;
- exact deployment receipt path/hash for `deployed-release`;
- exact sprint/GDD/issue/context paths and hashes used only as explanatory context;
- whether an internal entry, sanitized player draft, or both should be generated;
- exact public-redaction policy path/hash when a player draft is requested;
- operation `generate-only`, `insert-entry`, or `revise-entry`; exact changelog target,
  expected file hash or `ABSENT`, expected keyed-entry hash for revision, owner,
  recorder, size limit, mutation authority, and explicit non-writes.

Stable IDs are slugs or UUIDs, not dates alone. Normalize every path beneath the
repository. Do not search for the latest tag, newest report, recent sprint, or prior
release automatically.

## Evidence states that must not be conflated

Report these independently:

- `version_label_status`: `LABEL_ONLY`, `TAG_RESOLVED`, or `TAG_MISMATCH`;
- `commit_range_status`: `VERIFIED` only for immutable resolved full hashes with
  ancestry and final-tree evidence;
- `candidate_status`: `NOT_PROVIDED`, `VERIFIED_CANDIDATE`, or `MISMATCH`;
- `deployment_status`: `NOT_PROVIDED`, `VERIFIED_DEPLOYMENT`, or `MISMATCH`;
- `narrative_status`: `RESOLVED`, `HAS_UNRESOLVED`, or `SANITIZATION_BLOCKED`;
- `artifact_status`: `GENERATED`, `WRITTEN`, `PARTIAL`, or `BLOCKED`;
- `publication_status`: always `NOT_PUBLISHED` in this workflow.

A version label supplies presentation only. A lightweight/annotated tag supplies Git
identity only after resolving its tag object and commit. A commit proves inclusion in
the selected range, not build success or player availability. A candidate receipt
proves only the exact artifact/build/source/platform/configuration it binds. Only a
matching successful deployment receipt may support wording that the matching artifact
was deployed to its named environment/channel at its recorded time.

If candidate/deployment evidence is absent, the narrative must say `candidate not
proven` or `deployment not proven`; never say released, shipped, live, available,
published, or deployed. Even with a deployment receipt, this workflow only records
the evidence and remains `publication_status: NOT_PUBLISHED`.

## Phase 1: Resolve one exact Git range

Confirm the repository with a Git work-tree check. A non-Git directory, inaccessible
object database, shallow boundary that omits required ancestry, or missing ref returns
`Artifact Status: BLOCKED` and zero writes.

Resolve both refs with commit peeling to immutable full object IDs. Record original
ref text and resolved full commit/tree IDs. When a version tag is declared, record the
tag ref, tag-object ID/type, peeled commit, annotation/signature result when policy
requires it, and compare it with `to_commit`. A mismatch is blocking for tag/release
claims.

Require `from_commit` to be an ancestor of `to_commit`; record the full merge base and
ancestry result. The range is exactly `from_commit..to_commit`: the from commit is
excluded and the to commit is included. Reject unrelated histories unless the
manifest explicitly requests a non-release forensic report, which remains PARTIAL and
gate-ineligible.

`HEAD` or another moving ref is allowed only when explicitly supplied. Resolve it
once, label it as the exact commit, and re-resolve before output and before any write.
If it moves, invalidate the analysis and authorization. Never substitute current HEAD
for `to_ref`, and never infer that HEAD is released.

Record repository identity, current HEAD, branch/detached state, object format,
worktree/index status hash, submodule/LFS pointer state when applicable, and generated-
at UTC. Dirty/untracked bytes are explicitly outside the commit range and never enter
claims.

## Phase 2: Enumerate the complete range and net change

Enumerate every reachable commit in the exact range with full IDs, parent IDs, tree
IDs, author/committer identities, timestamps, subject/body, decorations, and topology.
Do not apply a 30/100/N commit cap and do not select only the first tags. Record total
count and canonical ordered commit-list hash.

Calculate the final tree diff from `from_commit` to `to_commit`, with file statuses,
renames/copies, modes, submodule/LFS pointer changes, binary markers, line statistics,
and stable patch/hunk hashes. Record complete diff metadata and final net-diff hash.
Claims are based on this net result, not the sum of commit messages.

### Merge, revert, fixup, and net-zero semantics

- Merge commits remain in provenance but do not duplicate claims already represented
  by the final net diff.
- Detect explicit revert references and verify their patch relationship when possible;
  a message alone is not proof of a complete revert.
- Changes added and fully removed before `to_commit` are `EXCLUDED_NET_ZERO`; preserve
  their commit/revert trace internally but do not list them as released/current net
  changes.
- Partial reverts describe only the surviving hunks and link both original and revert
  commits.
- Fixup/squash/cleanup commits remain provenance; narrative claims consolidate only
  surviving behavior. Never hide a surviving fix or failure by “cleaning” prose.
- An empty range or empty final diff is reported explicitly; do not invent changes
  from sprint/GDD context.

Recompute commit-list and net-diff hashes immediately before final output/write.

## Phase 3: Build source-bound claims

Each internal claim has stable ID:

`CLM-{release-id}-{net-hunk-hash-prefix}`

and records:

- category `FEATURE`, `IMPROVEMENT`, `FIX`, `BALANCE`, `TECHNICAL`, `DOCS`,
  `SECURITY_INTERNAL`, `KNOWN_ISSUE`, or `UNRESOLVED`;
- exact surviving path/hunk/patch hashes and commit IDs;
- observed net change, affected surface, and evidence confidence;
- candidate/build/deployment receipt IDs when availability wording depends on them;
- linked sprint/story/GDD/issue IDs only as context, with their path/hash;
- authors from Git as `authors`; `owner` only from an explicit owner record or user
  attestation, otherwise `owner: UNRESOLVED`;
- classification source, unresolved questions, and public eligibility.

Sprint reports, story status, issue state, and completed design documents may explain
why a surviving commit exists, but cannot prove that work is in the range, built, or
deployed. A context item without matching net diff remains `CONTEXT_ONLY_NOT_RELEASE
EVIDENCE` and is not a changelog claim.

If commit messages and diff evidence do not justify a category or player-facing
statement, use `UNRESOLVED`. Present the evidence and request a human classification;
do not guess. Unresolved internal entries may be written under their explicit section,
but prevent `narrative_status: RESOLVED` and are excluded from public draft.

Balance/design-reason claims need exact surviving value diffs plus an attested or
approved design source. Without both, state only the observed value change internally
and mark rationale unresolved.

## Phase 4: Validate candidate and deployment receipts

A candidate receipt must use a supported immutable schema and include build ID,
artifact hash, source commit/tree hash, platform/configuration, build result, producer,
UTC time, and receipt hash. It is valid only when source commit/tree equal
`to_commit/to_tree` and the referenced artifact/result is current.

A deployment receipt must include deployment ID, exact build/artifact/receipt hashes,
source commit/tree, environment/channel, successful status, deployer/runner, deployed-
at UTC, logs/evidence hashes, and receipt hash. It must chain exactly to the verified
candidate and `to_commit`.

Missing or mismatched receipts do not invalidate a commit-range narrative, but they
forbid candidate/deployment/release assertions and make a requested
`release-candidate` or `deployed-release` scope PARTIAL/BLOCKED. Risk acceptance cannot
change these evidence states.

## Phase 5: Generate the internal entry

Use a structured keyed block:

```markdown
<!-- changelog-entry:start release_id={release-id} range={from-full}..{to-full} schema=changelog-entry-v1 -->
## {version-label or release-id}

> Commit Range: {from-full}..{to-full}
> Version Label Status: {status}
> Candidate Status: {status and receipt/hash}
> Deployment Status: {status and receipt/hash}
> Publication Status: NOT_PUBLISHED
> Provenance SHA-256: {canonical provenance hash}

### Features
### Improvements
### Fixes
### Balance
### Technical / Documentation
### Security — Internal
### Known Issues
### Unresolved
### Excluded Net-Zero / Revert Trace
### Provenance
<!-- changelog-entry:end release_id={release-id} -->
```

Every displayed claim includes its stable ID and commit/diff evidence. Provenance
contains original/resolved refs, tag/merge-base/tree IDs, complete commit-list and
net-diff hashes/counts, repository/worktree status hash, context/receipt hashes,
generation tool/policy version, and UTC time.

Do not use a Released/Shipped/Live title unless `scope_kind: deployed-release` has a
verified matching deployment receipt. A commit-range or candidate entry is explicitly
labelled draft/candidate narrative.

## Phase 6: Generate an optional sanitized player draft

The player narrative is a separate draft, never a reformatted copy of internal text.
Only claims with surviving net diff, resolved classification, player-visible effect,
and any required candidate/deployment evidence are eligible.

Apply the exact public-redaction policy and deterministic scans for:

- credentials, API/token/key/private-key/auth-header patterns, connection strings,
  secrets and high-entropy suspicious values;
- PII, developer names/emails, internal usernames, private customer/player data;
- internal issue/story IDs, commit hashes, paths, hosts/domains/IPs, infrastructure,
  logs, build/deploy internals and security-control details;
- unreleased vulnerabilities, exploits, anti-cheat/abuse detection, embargoed content,
  legal/privacy matters, and unsafe workaround instructions.

Default-deny ambiguous sensitive text. Exclude or generalize only when policy allows;
never alter factual meaning. Record stable `RED-{release-id}-{claim-id}-{rule-id}`
internally with input hash, rule, action and reason. Redaction records never appear in
the public draft.

Recheck the final public bytes. A secret/PII/security policy failure sets
`narrative_status: SANITIZATION_BLOCKED` and produces no public draft. Header must say
`PLAYER CHANGELOG DRAFT — NOT REVIEWED OR PUBLISHED` and repeat candidate/deployment
status without overstating availability. This workflow never posts, publishes,
uploads, emails, or sends the draft.

## Phase 7: History-preserving keyed upsert

Generation is read-only unless `insert-entry` or `revise-entry` is explicitly
requested. Read the target's exact bytes and parse all start/end markers before
constructing candidate bytes.

Rules:

- `insert-entry`: release ID and exact range must not already exist; insert one keyed
  entry after the stable document header without reordering or editing old entries;
- `revise-entry`: release ID must occur exactly once, range identity must match unless
  the manifest explicitly supplies a superseding relation, and expected entry hash is
  required; replace only bytes between its exact markers;
- reject malformed/nested/unclosed markers, duplicate release IDs, duplicate exact
  ranges, and overlapping ranges without an explicit non-destructive supersedes link;
- compare every pre-existing keyed entry's exact hash before/after and require all
  non-target entries plus non-entry history bytes to remain identical;
- never offer or perform whole-file overwrite, historical entry deletion, truncate,
  rewrite, or normalization.

Before writing, present one mutation manifest containing operation, target/base hash,
release/range/entry IDs, candidate entry/file hashes, preserved-history hash map,
single recorder, maximum bytes, and explicit non-writes. Obtain explicit mutation
authorization. Narrative/content approval is not filesystem authorization.

Re-resolve refs and re-hash Git evidence, context/receipts, target, entry and candidate
immediately before write. Drift invalidates authorization. Write atomically where
supported, enumerate changed paths, read back the entire file, reparse markers, verify
the target entry and every preserved historical hash. On failure, return BLOCKED and
do not silently overwrite/revert concurrent user work.

This workflow never changes Git refs/tags/commits, build artifacts, sprint/GDD/issue
records, release/candidate/deployment receipts, deployment state, or external systems.

## Terminal output

Return:

- release/run/scope IDs and version label status;
- original refs, resolved full commits/trees/tag/merge-base and range provenance hash;
- complete commit/net-diff counts and hashes, net-zero/revert trace;
- claim IDs/categories/evidence and unresolved queue;
- candidate/deployment/publication states and receipt hashes;
- sanitized-draft status/redaction counts without exposing removed content;
- target operation/base/entry/final hashes or `NOT WRITTEN`;
- artifact/narrative status, blockers, and exactly one legal next action.

Use terminal results:

- `Artifact Status: GENERATED` — evidence-bound local drafts returned, no write;
- `Artifact Status: WRITTEN` — keyed entry atomically persisted and read back;
- `Artifact Status: PARTIAL` — safe narrative exists but requested classification,
  candidate/deployment evidence, sanitization, or scope remains incomplete;
- `Artifact Status: BLOCKED` — Git/ref/ancestry/duplicate/history/CAS/authorization
  failure prevents safe output/write.

Never return an unconditional COMPLETE. The next action resolves one named unresolved
claim/evidence conflict or hands a local player draft to an independently authorized
review/publishing owner. Do not invoke another workflow or publish anything.
