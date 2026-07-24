# Skill Test Spec: $changelog

## Skill Summary

`$changelog` produces a deterministic local candidate from one explicit immutable Git
range. Every narrative claim is bound to surviving net-diff evidence; plans and design
documents remain explanatory context. Version, date, intended target, candidate,
deployment, local creation, and publication are distinct identities and states. The
default mode is read-only; persistence may only create one absent immutable artifact
through create-only CAS and never edits changelog history.

---

## Static Assertions

- [ ] Frontmatter has only matching `name` and non-empty `description`
- [ ] Invocation requires `--request` plus `--expect-request`; request schema is
  `cgs.changelog-request/v2`
- [ ] Request supplies exact from/to refs, expected commits/trees, repository identity,
  merge-base/ancestry policy, and no latest/recent/count-based discovery
- [ ] Release identity separately hashes version, source-backed date, intended target,
  and immutable Git range
- [ ] Every claim binds surviving path/patch/hunk hashes and supporting commits;
  non-Git sources are context only
- [ ] Merge, revert, partial-revert, fixup, net-zero and claim-dedup semantics use final
  surviving hunks
- [ ] Categories are a fixed enum with frozen policy predicates/precedence;
  no/multiple matches become `UNRESOLVED`
- [ ] Candidate and deployment receipts are distinct, exactly chained, and cannot
  substitute for source, target, release, or publication evidence
- [ ] Player projection is independently rendered, default-denies security/privacy
  ambiguity, and never stores removed secret/PII bytes in redaction receipts
- [ ] Internal category and claim ordering are deterministic and identical evidence
  yields identical hashed narrative bytes
- [ ] Analysis is read-only and persistence is only one ABSENT-target atomic
  create-new guarded by full-input CAS/read-back
- [ ] Append, insert, revise, upsert, overwrite, truncate, delete, historical rewrite,
  external messaging, and publication are forbidden
- [ ] Non-Git, parse, ref, ancestry, evidence, sanitization, target-exists, CAS, and
  read-back failures have truthful non-COMPLETE terminal states
- [ ] Phases are uniquely numbered 1 through 8 with explicit input/output boundaries

---

## Traceability to audited P1 findings

| Finding | Required regression |
|---|---|
| CL-003 | Cases 1 and 2: claims require commit/tree/net-hunk evidence; context cannot prove inclusion |
| CL-004 | Cases 3 and 4: fixed categories, frozen rules, deterministic precedence, UNRESOLVED |
| CL-005 | Cases 5 and 6: merge/revert/fixup/net-zero/dedup preserve only surviving semantics |
| CL-006 | Cases 7 and 8: secrets, PII, internal IDs, and security details are default-denied without echo |
| CL-007 | Cases 1 and 9: full refs/commits/trees/merge-base/repo state plus version/date/target identities |
| CL-008 | Cases 12 and 13: no-Git and failure paths are BLOCKED/PARTIAL with zero unsafe writes |
| CL-009 | Static phase assertion and Case 14: unique ordered phase contracts and terminal vocabulary |

---

## Canonical phase contract

| Phase | Input | Output | Mutation |
|---|---|---|---|
| 1 — Parse, resolve, and pin | Hash-pinned v2 request, repository objects, frozen policies | Validated request, full refs/commits/trees/merge-base and repository-state identity | None |
| 2 — Enumerate and compute | Verified range | Complete topology, commit-list hash, surviving net diff, revert/net-zero trace | None |
| 3 — Claim and classify | Surviving hunks, frozen classification policy, exact context | Source-bound deduplicated claims or UNRESOLVED records | None |
| 4 — Verify release evidence | Version/date/target declarations and optional candidate/deployment receipts | Independent identity hashes and evidence states | None |
| 5 — Render internal entry | Verified identities and claims | Deterministically ordered internal candidate bytes/hash | None |
| 6 — Sanitize player projection | Eligible claims and frozen redaction policy | Player candidate or SANITIZATION_BLOCKED, plus non-secret receipts | None |
| 7 — Create-only CAS | Explicit mutation authority, candidate hash, ABSENT target | One verified new file, BLOCKED, or RECOVERY_REQUIRED | Create one absent target only |
| 8 — Terminal result | All prior receipts/states | Final status, identities, non-writes, blockers, one legal next action | None |

No other phase number or implicit post-processing stage is allowed.

---

## Case 1: Exact range and provenance are reproducible

**Fixture:** The request pins from/to ref text, full expected commits and trees,
repository identity, and a range of 237 commits. HEAD contains newer work.

**Expected behavior:** Resolve and compare every object, verify ancestry and merge base,
enumerate all 237 commits, compute the complete from/to net diff, and exclude newer
HEAD plus dirty/untracked bytes.

**Assertions:**

- [ ] No 30/100/N commit or tag cap is used
- [ ] Range, commit-list, net-diff, repository-state and provenance hashes are recorded
- [ ] Original refs and resolved full commits/trees/merge-base are retained
- [ ] A budget stop is PARTIAL, never a truncated success

---

## Case 2: Sprint and GDD are context, not release proof

**Fixture:** A sprint report says Story-X is done and a GDD says Feature-Y is complete,
but neither maps to a surviving net hunk in the selected range.

**Expected behavior:** Record both as `CONTEXT_ONLY_NOT_RELEASE_EVIDENCE` with exact
path/hash and create no X/Y changelog claim.

**Assertions:**

- [ ] Context cannot prove commit inclusion, build, deployment, rationale, or ownership
- [ ] Every displayed claim has exact surviving hunk/patch and commit evidence
- [ ] Balance rationale without both value diff and attested design source is unresolved

---

## Case 3: Ambiguous classification remains unresolved

**Fixture:** A surviving diff has a `misc changes` message and file paths that might
suggest several categories, but no frozen rule or human attestation resolves it.

**Expected behavior:** Produce one internal `UNRESOLVED` claim, exclude it from the
player projection, and report `narrative_status: HAS_UNRESOLVED`.

**Assertions:**

- [ ] Message, path, author, and model judgment do not force a category
- [ ] Git authors are not treated as owners or approvers
- [ ] Exactly one unresolved question and safe next action are reported

---

## Case 4: Category policy is deterministic

**Fixture:** Frozen policy predicates match both security and fix rules for one hunk;
another hunk matches no rule. Evidence order is shuffled between two runs.

**Expected behavior:** Apply the declared precedence so security wins for the first;
classify the second UNRESOLVED; produce identical ordered claim bytes/hashes in both
runs.

**Assertions:**

- [ ] Exact policy schema/version/hash and rule IDs are recorded
- [ ] Fixed category order and claim-hash order are used
- [ ] Multiple/no match never triggers an improvised category

---

## Case 5: Full revert is net zero

**Fixture:** Commit A adds a feature and commit B fully reverts its exact patch before
to_commit.

**Expected behavior:** Preserve A/B and verified relationship in internal provenance,
mark `EXCLUDED_NET_ZERO`, and emit no current or player claim.

**Assertions:**

- [ ] Revert message alone is insufficient
- [ ] Final tree/hunk evidence controls survival
- [ ] Narrative cleanup cannot resurrect removed work

---

## Case 6: Merge, partial revert, fixup, and dedup

**Fixture:** A merge exposes the same surviving hunks through multiple parents, fixups
change the implementation, a partial revert removes half, and two commits support the
same remaining effect.

**Expected behavior:** Retain topology and all supporting IDs, describe only surviving
hunks, and generate one claim per exact claim identity without duplicate merge claims.

**Assertions:**

- [ ] Partial reverts link original/revert commits and omit removed hunks
- [ ] Claim identity uses sorted surviving hunk hashes and normalized observed effect
- [ ] Similar prose cannot merge distinct effects

---

## Case 7: Player draft removes secrets, PII, and internals

**Fixture:** Eligible internal records contain a token-like value, developer email,
private player identifier, issue ID, commit/path/host details, and deployment logs.

**Expected behavior:** Independently render and scan the player projection, remove or
block data per the frozen policy, and place only hashes/rule/reason codes in internal
redaction receipts.

**Assertions:**

- [ ] Removed bytes are absent from public artifact, logs, and redaction receipts
- [ ] Final public bytes receive a second deterministic scan
- [ ] Header says `PLAYER CHANGELOG DRAFT — NOT REVIEWED OR PUBLISHED`
- [ ] No message, upload, email, or publication occurs

---

## Case 8: Security ambiguity blocks the public artifact

**Fixture:** A surviving security fix could reveal an unreleased exploit and the policy
cannot safely generalize it.

**Expected behavior:** Keep a hashed `SECURITY_INTERNAL` claim, return
SANITIZATION_BLOCKED for the player projection, and emit no public bytes.

**Assertions:**

- [ ] Security is default-deny and wins category precedence
- [ ] The blocker does not quote exploit, secret, or unsafe workaround details
- [ ] Internal generation does not imply security/legal/publication approval

---

## Case 9: Version, date, and target identities do not collapse

**Fixture:** Version label is supplied, its tag points to another commit, a date lacks
its declared source, and intended target differs from deployment environment.

**Expected behavior:** Preserve separate version/date/target hashes and mark each exact
mismatch. Do not use generated-at, tag, commit, build, or deploy time as release date.

**Assertions:**

- [ ] Release identity binds range plus independent version/date/target identities
- [ ] Version label is presentation unless exact tag evidence matches to_commit
- [ ] Intended target is distinct from actual deployment target
- [ ] No released/live/available wording appears

---

## Case 10: Candidate is not deployment

**Fixture:** A valid candidate receipt binds to_commit/to_tree and artifact, but no
deployment receipt exists. A second fixture has a deployment receipt for another
artifact or target.

**Expected behavior:** First fixture is VERIFIED_CANDIDATE with deployment NOT_PROVIDED;
second is deployment MISMATCH. Neither supports deployment/public-availability claims.

**Assertions:**

- [ ] Tag/range/build success cannot substitute for deployment receipt
- [ ] Deployment must chain to the exact candidate/artifact/source/tree and target
- [ ] Publication status remains NOT_PUBLISHED even for verified deployment

---

## Case 11: Analyze-only is strictly read-only

**Fixture:** A valid request selects `analyze-only` and both internal and sanitized
player candidates.

**Expected behavior:** Return deterministic candidate bytes and hashes with
`Artifact Status: GENERATED` and an explicit zero-write/non-publication receipt.

**Assertions:**

- [ ] No changelog/index/manifest/Git/context/receipt file changes
- [ ] No temporary artifact escapes the response
- [ ] Content approval is not filesystem or publication authority

---

## Case 12: Create-only uses absent-target CAS

**Fixture:** A request authorizes one candidate hash and target expected ABSENT. Test
variants pre-create the target or drift a ref, policy, context, receipt, parent, or
candidate hash before commit.

**Expected behavior:** Any conflict returns BLOCKED with zero writes. With stable
inputs, an atomic no-replace primitive creates exactly one file, which is flushed,
strictly parsed, read back, and hash verified.

**Assertions:**

- [ ] CAS covers request, Git objects, repo state, policies, context, receipts,
  candidate, parent identity, and ABSENT target
- [ ] Append/insert/revise/upsert/overwrite/truncate/delete modes do not exist
- [ ] Existing changelog/history bytes cannot be touched or reordered
- [ ] Read-back mismatch is RECOVERY_REQUIRED, never silently overwritten/deleted

---

## Case 13: No Git or invalid evidence is fail-closed

**Fixture:** The root is not a Git work tree; separate variants have missing shallow
objects, malformed request/policy, unrelated ancestry, and mismatched expected hashes.

**Expected behavior:** Return BLOCKED, identify the exact failed identity/check, write
nothing, and provide exactly one safe corrective action.

**Assertions:**

- [ ] Empty/unavailable history is not a release narrative
- [ ] No GENERATED/CREATED success is emitted for invalid evidence
- [ ] Result is never unconditional COMPLETE

---

## Case 14: Phase and terminal contracts remain aligned

**Fixture:** Statically inspect implementation and spec; exercise generated, created,
partial, blocked, and post-create verification-failure paths.

**Expected behavior:** Both artifacts define the same unique Phases 1–8, request and
identity contracts, fixed category order, and terminal states.

**Assertions:**

- [ ] No duplicate/missing phase number exists
- [ ] `GENERATED`, `CREATED`, `PARTIAL`, `BLOCKED`, and `RECOVERY_REQUIRED` meanings match
- [ ] Terminal result includes all identities, hashes, statuses, non-writes, blockers,
  and exactly one legal next action

---

## Protocol Compliance

- [ ] Explicit immutable range and final net diff reproduce every source claim
- [ ] Merge/revert/fixup/dedup logic reports only surviving semantics
- [ ] Frozen deterministic categories never turn ambiguity into fact
- [ ] Security/privacy filtering is independent, hash-bound, and does not echo secrets
- [ ] Version/date/target/candidate/deployment/publication identities stay separate
- [ ] Default behavior is read-only; optional persistence is ABSENT create-only CAS
- [ ] Output is local and never auto-published

---

## Coverage Notes

Cases 1–14 cover CL-003 through CL-009 and retain the P0 protections for explicit,
untruncated ranges and non-destructive history. The specification is behavioral only;
unchecked boxes are required assertions, not claims of execution.
