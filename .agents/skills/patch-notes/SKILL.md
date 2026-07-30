---
name: patch-notes
description: "Create one traceable local patch-note draft from an exact approved candidate and matching verified production deployment, with net-change provenance, privacy-safe localization, embargo controls, and optional create-only version and existence conflict check persistence."
---

# Patch Notes

Produce player-facing patch-note draft bytes only for the exact approved candidate that
has actually been deployed successfully to the declared production target. A Git
range is not a candidate, a candidate is not a deployment, a deployment is not public
availability, and a local draft is never publication.

## Invocation and strict request

Invoke only as:

`$patch-notes --request <path>`

Require both flags exactly once. With missing/invalid flags or unknown arguments, show
that usage and stop before project reads, Git access, output, delegation, or writes.
Reject directories, traversal, globs, moving request aliases, symlink/junction/reparse
escape, unsupported schemas, unknown/repeated fields, and expected/actual revision drift.

The request is strict `cgs.patch-notes-request/v3` and contains:

- stable `release_id`, `run_id`, source locale, exactly one output locale, and style
  `brief`, `detailed`, or `full` (presentation only);
- immutable repository identity; `from_ref`, `to_ref`; expected full `from_commit`,
  `to_commit`, `from_tree`, `to_tree`, merge-base, ancestry result, object format, and
  approved range identity;
- one versioned `EXTERNAL_BOUNDARY` `cgs.approved-release-change-manifest/v2` at its
  canonical path with explicit revision, `APPROVED` state, authority-registry/revision,
  signer/signature verification, currentness fields and exact approved item inventory;
- exact candidate ID, artifact identifier, source commit/tree, platform/configuration,
  build receipt path/revision, approval boundary and candidate identity revision;
- one canonical `cgs.release-action-receipt/v2` path/declared revision with exactly
  `action: DEPLOY`, `result: SUCCESS`, a production environment, configured-authority
  identity/signature verification, and intended production targets;
- exact classification, public-redaction, embargo, and locale policy paths, schema/
  version/revision, plus exact source/verification/quote/disclosure/locale evidence
  inventories;
- for non-source output, the canonical sanitized source-draft path/revision, exact
  `cgs.localization-manifest/v2` and catalog identities, one immutable
  `cgs.localization-package/v1` path plus literal `package_id`,
  `package_payload_revision`, separate `file_revision`, and literal
  `manifest.path`/`manifest.revision`, current target-locale revision bytes/revision,
  `cgs.translation-delivery/v1` and distinct `cgs.locale-review/v1` receipts;
- operation `analyze-only` or `create-draft`; and
- for `create-draft`, one normalized target path, `expected_target: ABSENT`, maximum
  bytes, creator, mutation authority/expiry, create-new capability, and non-writes.

Validate release/locale/target IDs as constrained slugs or canonical locale tags before
using them in a path. Do not search for latest/current manifests, tags, receipts,
deployments, translations, or policies. Do not infer HEAD, a release range, source or
target locale, version, date, link, platform, rollout state, owner, approval, or
publication authority.

## Authority and non-writes

Analysis is read-only. `create-draft` authorizes only the exact approved bytes at one
absent local target. It never authorizes append, update, revision, overwrite,
normalization, deletion, directory creation, a second copy, index mutation, build,
deploy, rollout, store/site/forum/email/chat/social activity, or publication.

The external release authority owns and signs the approved change-manifest boundary;
no project skill owns, produces, repairs or countersigns it. The build producer owns
candidate evidence. The configured deployment authority owns canonical release action receipts. Security,
privacy, legal, embargo, localization, community/content, and publication approvals
remain separate human/organizational authorities. The model may validate receipts but
cannot issue, repair, waive, or self-approve them.

Never invent facts, player impact, causality, quotes, developer voice, dates, links,
translations, mitigations, deployment coverage, sensitive-content decisions, or
approvals. Do not invoke another workflow.

## Hard bounds and partial results

The request may lower but never raise these per-invocation limits:

| Resource | Hard limit |
|---|---:|
| output locales | 1 |
| approved manifest items | 500 |
| linked source/verification records | 1,000 |
| linked files | 128 |
| linked file bytes total | 16 MiB |
| canonical net-diff bytes | 64 MiB |
| review findings | 500 |
| bounded prose revision rounds | 1 |
| total elapsed time | 15 minutes |

Read only the explicit inventory. If a limit, timeout, missing item, parser failure, or
unsupported binary prevents complete candidate-wide merge/revert/dedup validation,
return PARTIAL with completed/omitted counts, revisions, reason and an identity-bound
resume cursor. Produce no player prose or file from sampled/truncated evidence.

## Canonical identities and states

Use strict schema parsers. Canonical serialization is UTF-8/LF/NFC with stable
schema field order and sorted set arrays. Record each source path and declared revision.

```text
range_identity = {repository-ID}/{from-revision}/{to-revision}
manifest_identity = {approved-manifest-ID}/{manifest-revision}
candidate_identity = {candidate-ID}/{build-ID}/{artifact-ID}
deployment_identity = {deployment-action-receipt-ID}
claim_identity = {approved-stable-claim-ID}
source_draft_identity = {UTC-run-ID}/{source-locale}
locale_draft_identity = {UTC-run-ID}/{target-locale}
```

Use only these stable business IDs and explicit revisions. Never derive an identity from rendered or source bytes.

Report independently:

- `range_status`: `VERIFIED` or `MISMATCH`;
- `manifest_status`: `APPROVED_VERIFIED` or `MISMATCH`;
- `candidate_status`: `APPROVED_CANDIDATE_VERIFIED` or `MISMATCH`;
- `deployment_status`: `PRODUCTION_ACTION_VERIFIED` or `MISMATCH`;
- `embargo_status`: `NOT_EMBARGOED`, `ACTIVE`, `LIFT_VERIFIED`, or `MISMATCH`;
- `locale_status`: `SOURCE_VERIFIED`, `LOCALIZATION_REVIEWED`, `PARTIAL`, or
  `MISMATCH`;
- `review_status`: `CLEAN`, `BLOCKERS_REMAIN`, or `PARTIAL`;
- `artifact_status`: `DRAFTED`, `CREATED`, `PARTIAL`, `BLOCKED`, or
  `RECOVERY_REQUIRED`; and
- `publication_status`: always `NOT_AUTHORIZED`.

No path returns COMPLETE. Production deployment does not lift an embargo, approve a
translation, approve community wording, or publish patch notes.

## Phase 1 — Pin release, Git range, manifest, and candidate

Strictly parse the request, policies, manifest and receipts. Confirm the Git work tree
and object availability. Resolve/peel refs to full commits/trees and compare expected
IDs. Verify `from_commit` is an ancestor of `to_commit`, the exact merge base, and the
range `from_commit..to_commit` (from excluded, to included). Record repository object
format, current HEAD/branch, worktree/index revision and submodule/LFS state; these may
detect drift but never widen the range. Dirty/untracked bytes are outside evidence.

### Versioned approved-change EXTERNAL_BOUNDARY

No project skill in this repository produces `cgs.approved-release-change-manifest/v2`.
Treat it as a formally versioned external input, never as a missing workflow to invoke
or an artifact this skill may create, repair, approve or sign. Its only canonical path
is:

```text
production/releases/{release-id}/{candidate-identity-revision}/change-manifests/
  {manifest-identity-revision}.yaml
```

Require strict schema/version and the request-pinned exact path/declared revision;
release ID/identity, candidate ID/identity, build ID/identity, source/range and artifact
bindings; complete ordered `cgs.release-change-item/v2` rows and row revisions; approval
state; authority-registry path/revision/version; signer identity/key ID/scope; signature
algorithm/value and successful verification over the exact canonical signed payload;
issued/effective/expiry/revocation/currentness data and trusted-time evidence. revalidate
the manifest identity and require the identifier encoded in the path. Missing boundary,
unknown schema, noncanonical path, raw drift, incomplete rows, identity mismatch,
untrusted/expired/revoked authority, invalid signature or stale currentness is BLOCKED
before claims or player prose. A changelog, Git tag, release checklist, candidate,
deployment receipt, conversation approval or another project skill cannot substitute,
produce, endorse or countersign this boundary.

The approved manifest must bind release ID, exact range identity, candidate identity,
build identity, artifact identifier, external authority/signature/currentness, intended production targets,
and every ordered item. Each `cgs.release-change-item/v2` contains stable item ID,
INCLUDE/EXCLUDE disposition, player-visible flag, exact approved player fact, fixed
category, surviving commit/path/patch/hunk revisions, source/verification IDs and revisions,
platform/rollout qualifiers, sensitive class, embargo class, localization eligibility,
and item revision.

Candidate build receipt must report success and bind the same artifact,
`to_commit/to_tree`, platform/configuration and approval boundary. Any missing,
expired, unapproved, mismatched, or stale identity is BLOCKED before prose.

## Phase 2 — Verify exact production deployment

The immutable input must parse as canonical `cgs.release-action-receipt/v2`, its exact
schema, stable receipt ID, and explicit revision must match the request, and its canonical receipt identity and
signature must verify under the pinned authority registry. Require exactly
`action: DEPLOY`, `result: SUCCESS`, a production environment and completed observed
state. revalidate and require the same release ID/identity, manifest/range, approved
candidate ID/identity, build ID/identity, artifact identifier, source commit/tree,
deployment ID/identity, target set, rollout boundary, deployed-at time, request,
authorization path/revision/issuer/scope/expiry, checkpoint/predecessor chain, evidence and
raw payload revisions. Every availability/platform/region/channel claim must be a subset
of those verified deployed targets and rollout boundary.

An isolated `cgs.production-deployment-receipt/v2`, provider payload, tag, merge, Git
commit, build success, QA pass, release checklist, readiness record, hotfix branch/plan,
staging/canary deployment, schedule, schema rename or assertion is not the canonical
production action receipt and grants no authority. Such provider evidence is usable
only when version-bound inside the canonical receipt's verified chain. Missing, failed,
non-production, stale, mismatched, unsigned, unauthorized or non-canonical input returns
BLOCKED and no player narrative, including speculative prose.

## Phase 3 — Reconcile topology, reverts, and duplicate items

Enumerate the complete approved range without commit-count truncation and compute the
final from/to tree diff with stable patch/hunk identities. Claims follow surviving net
change, not commit messages or the sum of commits.

- Merge commits remain provenance but do not duplicate a surviving hunk or claim.
- Revert messages are hints until patch/hunk relationships verify them.
- Fully reverted changes are `EXCLUDED_NET_ZERO`; preserve internal original/revert
  trace and create no player claim.
- Partial reverts retain only surviving hunks and link original/revert commits.
- Fixup/squash commits remain provenance while final surviving semantics control.
- Deduplicate first by exact surviving hunk identity, then by
  `claim_identity`; combine supporting item/commit IDs, never distinct facts,
  platform qualifiers, rollout boundaries, or mitigations merely because prose matches.

An INCLUDE manifest item that has no matching surviving net evidence, or surviving
player-visible evidence absent from the approved manifest, is
`MANIFEST_NET_MISMATCH` and BLOCKED. Context documents cannot repair it. revalidate
range/net/item/claim revisions before output and before create.

## Phase 4 — Build the player-facing claim provenance table

Create deterministic `cgs.patch-notes-claim/v3` rows sorted by
`claim_identity`. Each row contains claim/item IDs and revisions, candidate and
deployment identities, exact approved fact revision, surviving commit/path/patch/hunk
revisions, source/verification record revisions, category, platforms/targets/rollout,
sensitive/embargo/locale states, exact draft sentence IDs, exclusions, and finding IDs.

Only INCLUDE + player-visible + net-surviving + deployed items are eligible. Preserve
meaning, causality, certainty, numbers, before/after values, platform/region/channel,
rollout state and known limitations. Clarity/style edits cannot strengthen evidence.
Every title, subtitle, date, link, highlight, bullet, limitation, known issue and
availability statement maps to claim/release/deployment evidence. Template and tone
guidance never introduce a fact, promise, date, link, quote, section, or scope.

Git/changelog/sprint/GDD/retro/issue/bug/QA records outside the item inventory cannot
add claims. Linked records corroborate only their exact manifest fact. Never infer
implementation from design, player impact from technical change, or deployment from
readiness.

Do not invent first-person team voice, developer commentary, quotations, motives,
lessons or opinions. A quote may appear only verbatim from `cgs.approved-public-quote/v1`
binding speaker, exact bytes/revision, claim IDs, candidate/deployment, locale, audience,
public-use approval and expiry. Otherwise record `NO_APPROVED_QUOTE` and omit it.

## Phase 5 — Enforce security, privacy, known-issue, and embargo policy

Classify `SECURITY`, `ANTI_CHEAT`, `PRIVACY`, `EXPLOIT`, `LEGAL`, `EMBARGOED`, and
project restricted classes as default-deny. A sensitive claim needs a separate
verified `cgs.public-disclosure-approval/v2` bound to claim, exact approved text revision,
candidate/deployment, locale, audience/targets, policy, approver, time and expiry.
Known issues additionally need approved safe scope, non-exploitable mitigation wording,
verification, owner and disclosure boundary. Without all of them, omit or BLOCK as the
policy directs; never leak reproduction steps or unsafe workarounds.

Apply the frozen redaction policy and deterministic scans to claim fields and rendered
bytes for credentials/tokens/keys/secrets, high-entropy values, personal/player data,
developer identities, internal IDs/paths/hosts/IPs/domains/logs/infrastructure, build
and deployment internals, vulnerabilities/exploits, anti-cheat/abuse detection,
embargoed content, legal/privacy data and unsafe instructions. Ambiguity is deny, not
speculative generalization.

`cgs.patch-notes-redaction/v1` records only input/claim revisions, policy/rule/version,
action/reason, scanner result and output revision—never removed sensitive bytes. Re-scan
final bytes; any unresolved finding yields BLOCKED and no player artifact.

Embargo policy/receipt binds release/claim IDs, exact text/candidate/deployment revisions,
audience, locale, region/channel/target, starts/lifts, authority, status and receipt
revision. Wall-clock passage alone never lifts an embargo: require a verified lift receipt
and trusted time evidence named by policy. ACTIVE/MISMATCH embargo yields no player
bytes for that audience and target, even though production deployment succeeded.

## Phase 6 — Bind exactly one locale

Generate one locale per invocation. For the source locale, the sanitized claim table
and source rendering define `source_draft_identity`.

For a non-source locale, never translate or fall back automatically. The localization
adapter accepts the actual localize producer contract `cgs.localization-package/v1`,
not an isolated patch-notes locale schema. Strictly read the owner-assigned `package_id`, explicit `package_payload_revision`, and nested `manifest.schema`, `manifest.path`, and `manifest.revision`. Validate their schema, stable IDs, declared revisions, and request bindings without recalculating identity from bytes. None may be renamed, inferred, or substituted for another.
Then require exact `cgs.localization-manifest/v2`, catalog/source/keyset/per-key,
source-locale, target-locale/locale-identity, plural/placeholder, stable key-page and
owner bindings. Require matching current target translation-revision bytes/revision,
`cgs.translation-delivery/v1` from the translator/vendor and a distinct locale-qualified
`cgs.locale-review/v1` over that revision.

Bind that unchanged producer chain in memory to this exact current release, candidate,
build, sanitized source-draft revision and claim/sentence IDs. Preserve the complete parsed
package, source path/declared revision and field-source mapping in the internal localization view;
do not rewrite or persist a renamed package. This lossless normalization is data
compatibility only and grants no translation, review, mutation, release or publication
authority. Any manifest/catalog/release/candidate/build/locale/path/revision drift is
PARTIAL/BLOCKED. Validate structure, claim marker, numeric/unit, product-name, link,
placeholder, platform/rollout qualifier and omission parity. Translation cannot add
facts, promises, quotes, targets or dates; remove limitations; reintroduce redacted/
embargoed material; or weaken safety text.

Run locale-specific privacy/security/embargo scans on final localized bytes. Missing,
self-reviewed, stale, partial, source-mismatched or policy-mismatched localization is
PARTIAL/BLOCKED with no locale artifact. Source-locale bytes cannot silently substitute
for a requested locale.

The source-locale artifact is the sole semantic source of truth. A localized artifact
is a derivative with source-draft and locale revision identifiers, never a duplicate
canonical source. Documentation/store/site representations are downstream projections
outside this workflow.

## Phase 7 — Deterministic render and bounded review

Render fixed section/category order from eligible claims only; within each section sort
by claim identity and sentence ID. Omit empty optional sections with a fixed omission
token in provenance. Identical request/evidence bytes yield identical draft bytes and
revision; generated-at is supplied evidence metadata or excluded from the versioned body.

Create stable finding ID
`PNF-{release-id}-{locale}-{claim-or-document-id}-{rule-id}` for unsupported,
overstated, contradictory, sensitive, embargoed, unlocalized, untraceable or malformed
content. Deduplicate by finding ID. One bounded prose revision may address only those
frozen findings; then rerun every rule. Never silently discard, downgrade or self-waive
a finding. Any blocker or new blocker yields BLOCKED; limit/time gaps yield PARTIAL.

The draft header says `LOCAL PATCH-NOTE DRAFT — NOT PUBLISHED`, names exact release,
candidate, deployment target/canonical action receipt, source/output locale and embargo state, and
includes machine-readable range/manifest/candidate/deployment/claim/source-draft/
locale/policy revisions. `DRAFTED` means returned locally in conversation, not approved or
published.

## Phase 8 — Optional single-target create-only version and existence conflict check

`analyze-only` writes nothing. `create-draft` can create one absent immutable file only.
The authorized target must be inside the allowed release root, its parent must already
exist, and it must remain ABSENT during validation, preview, authorization and commit.
No second docs/production copy, alias, symlink, manifest, index, latest pointer, or
directory is created or updated.

Preview one mutation manifest containing request/range/manifest/candidate/deployment/
claim/redaction/embargo/source-draft/locale revisions, exact target and expected ABSENT,
candidate bytes/revision, parent identity, creator, create-new primitive, maximum bytes,
authority/expiry and non-writes. Content approval is not mutation authority.

Immediately before create, version and existence conflict check all input bytes and identities, Git refs/objects and
repository state, policies/receipts, source/locale package, candidate bytes, parent and
target ABSENT state. Use an atomic no-replace/create-new primitive; if unavailable or
anything drifts, write nothing and return BLOCKED. Flush, close, strictly parse, read
back and revision the created file. A post-create mismatch is RECOVERY_REQUIRED with exact
expected/actual revisions; never overwrite or silently delete evidence.

## Phase 9 — Terminal packet and stop

Return `cgs.patch-notes-result/v3` with release/run/style/source/output locale; exact
range/manifest/candidate/deployment/source-draft/locale/policy identities; complete
net/revert/dedup counts; claim provenance/exclusions; redaction, sensitive and embargo
results without protected bytes; frozen/rechecked findings; target/candidate/final
revisions or NOT_WRITTEN; all independent statuses; explicit non-writes; blockers; and
exactly one legal next action/owner.

Use only:

- `Artifact Status: DRAFTED` — verified local draft returned, zero writes;
- `Artifact Status: CREATED` — one absent local draft created and read-back verified;
- `Artifact Status: PARTIAL` — bounded evidence/localization analysis is incomplete
  and no player artifact is claimed complete;
- `Artifact Status: BLOCKED` — evidence, disclosure, embargo, review or version and existence conflict check prevents a
  safe draft/create; or
- `Artifact Status: RECOVERY_REQUIRED` — exclusive create happened but read-back
  verification failed and requires owner-directed recovery.

`publication_status` remains `NOT_AUTHORIZED`. Stop after the packet. Never publish,
send, upload, invoke a publishing workflow, or invoke the next owner.
