# Skill Test Spec: $changelog

## Skill Summary

`$changelog` generates local, reproducible internal and optional sanitized player
narratives from an explicit immutable Git range. Claims require surviving net-diff
evidence; sprint/GDD context cannot prove inclusion. Version label, tag, commit range,
candidate build, deployment, local write, and publication are independent states.
Persistence is limited to a keyed insert/revise that preserves every historical byte;
whole-file overwrite is forbidden.

---

## Static Assertions (Structural)

- [ ] Frontmatter contains only matching `name` and non-empty `description`
- [ ] Invocation requires a manifest with explicit from_ref/to_ref and rejects
  version/sprint ambiguity
- [ ] Refs resolve to immutable full commits/trees with ancestry and merge-base checks
- [ ] Commit enumeration and final tree diff have no count/tag truncation
- [ ] Merge/revert/fixup/net-zero semantics are explicit and claim the surviving net
  result only
- [ ] Every claim has stable ID, commit/diff evidence and optional context links;
  ambiguous classification is UNRESOLVED rather than guessed
- [ ] Sprint/GDD/story/issue state is explanatory context, never release/build/deploy
  evidence
- [ ] Version label/tag, commit range, candidate, deployment, narrative, local artifact
  and publication states are machine-readably separate
- [ ] Candidate and deployment claims require exact chained receipts matching
  to_commit/to_tree/artifact hashes
- [ ] Player draft uses deterministic secret/PII/internal/security filtering and is
  explicitly unreviewed/unpublished
- [ ] Persistence permits only marker-keyed insert/revise with duplicate/range checks,
  preserved-history hashes, CAS and read-back
- [ ] Whole-file overwrite, deletion, truncate, historical rewrite and automatic
  publishing are prohibited
- [ ] No-Git, ref drift, ancestry, receipt, sanitization, duplicate, authorization and
  CAS failure statuses are defined; result is not always COMPLETE

---

## Case 1: Release range longer than 100 commits is complete

**Fixture:** Explicit from/to refs resolve to an ancestor range containing 237 commits.
The latest repository HEAD is newer than to_ref.

**Expected behavior:** Resolve immutable full commits, enumerate all 237 range commits,
compute the final from/to tree diff, and exclude newer HEAD commits.

**Assertions:**

- [ ] No 30/100/N commit cap is used
- [ ] No recent/latest tag selection occurs
- [ ] Commit-list count/hash and final net-diff hash are recorded
- [ ] HEAD bytes outside to_commit are not included

---

## Case 2: Explicit HEAD is a commit-range draft, not a release

**Fixture:** Manifest explicitly uses HEAD as to_ref with `scope_kind: commit-range`;
no tag, candidate or deployment receipt exists.

**Expected behavior:** Resolve and pin exact HEAD commit, recheck it before output, and
label the narrative as a commit-range draft with candidate/deployment not proven and
publication NOT_PUBLISHED.

**Assertions:**

- [ ] Version label, if supplied, remains LABEL_ONLY
- [ ] No released/shipped/live/available/deployed wording appears
- [ ] Moving HEAD invalidates analysis and write authorization

---

## Case 3: Full revert creates no published net-change claim

**Fixture:** Commit A adds a feature and later commit B fully reverts its exact patch;
the final from/to tree diff contains none of that feature.

**Expected behavior:** Preserve A/B in internal revert provenance, mark the change
EXCLUDED_NET_ZERO, and omit it from internal current-change and player claims.

**Assertions:**

- [ ] Revert message alone is not the only verification
- [ ] Net tree/hunk evidence determines survival
- [ ] Narrative cleanup cannot resurrect net-zero work

---

## Case 4: Merge, fixup and partial revert preserve surviving semantics

**Fixture:** A merge contains commits also reachable elsewhere, fixups alter a change,
and a later partial revert removes half the hunks.

**Expected behavior:** Record topology/provenance once, avoid duplicate merge claims,
and describe only surviving hunks while linking original/fixup/revert commits.

**Assertions:**

- [ ] Claim IDs bind final net hunk hashes
- [ ] Removed behavior is absent from current narrative
- [ ] Surviving fix/failure semantics are not hidden by prose cleanup

---

## Case 5: Ambiguous commit enters UNRESOLVED

**Fixture:** Commit message is `misc changes`; diff shows several technical edits but
does not establish player impact or feature category.

**Expected behavior:** Create an evidence-bound internal UNRESOLVED claim, ask for
human classification, and exclude it from player draft. Do not infer from filenames.

**Assertions:**

- [ ] No forced feature/fix/improvement category
- [ ] Git authors are not presented as owners
- [ ] Narrative status is HAS_UNRESOLVED

---

## Case 6: Sprint and GDD do not prove release inclusion

**Fixture:** A sprint says Story-X is done and a GDD marks Feature-Y complete, but the
selected range has no surviving diff linked to either.

**Expected behavior:** Record context as CONTEXT_ONLY_NOT_RELEASE_EVIDENCE and produce
no changelog claim for X/Y.

**Assertions:**

- [ ] Completed documents cannot substitute for commit/diff/build evidence
- [ ] Design rationale appears only when linked to a surviving claim
- [ ] Balance rationale without approved/attested source remains unresolved

---

## Case 7: Keyed insert preserves all history

**Fixture:** Existing changelog contains release blocks v0.2 and v0.3 plus unmarked
header/history text. New unique release/range is authorized for insert.

**Expected behavior:** Parse markers, construct one keyed block, insert after the
stable header, and verify every prior entry and non-entry byte hash is unchanged.

**Assertions:**

- [ ] New entry has unique release ID/range and complete provenance
- [ ] Existing v0.2/v0.3 and unmarked history bytes remain exact
- [ ] Whole-file overwrite is never offered
- [ ] Read-back reparses all markers and hashes

---

## Case 8: Duplicate ID/range and overwrite requests are rejected

**Fixture:** Inputs separately reuse an existing release ID, reuse an existing exact
range under another ID, overlap without supersedes, and request whole-file overwrite.

**Expected behavior:** Return BLOCKED before mutation with exact conflicting marker,
ID/range/hash. Do not delete, truncate, normalize, reorder or overwrite history.

**Assertions:**

- [ ] Revision requires exact existing entry ID and expected entry hash
- [ ] Non-target entries remain immutable
- [ ] Risk acceptance does not bypass history protection

---

## Case 9: No Git repository is BLOCKED with zero writes

**Fixture:** Project root is not a work tree or required objects are unavailable due
to a shallow boundary.

**Expected behavior:** Return Artifact Status BLOCKED, name the Git/ancestry failure,
and write no changelog.

**Assertions:**

- [ ] Empty history is not treated as a valid release
- [ ] No COMPLETE/GENERATED/WRITTEN success is emitted
- [ ] Exactly one safe corrective action is provided

---

## Case 10: Player draft removes sensitive/internal material

**Fixture:** Internal claims contain a token-like value, developer email/name, private
host/IP, internal story/path/hash, and an unreleased security vulnerability.

**Expected behavior:** Apply the declared public policy, generate internal RED records
without copying removed secrets into public output, and default-deny ambiguous content.
If final scan fails, emit SANITIZATION_BLOCKED and no player draft.

**Assertions:**

- [ ] Public draft is independently built and says NOT REVIEWED OR PUBLISHED
- [ ] Secret/PII/security/internal details are absent
- [ ] Redaction reasons remain internal and do not expose removed bytes
- [ ] Nothing is posted or published

---

## Case 11: Candidate and deployment receipts cannot be substituted

**Fixture:** Version/tag/range are valid. Candidate receipt points to another tree, or
deployment receipt points to another artifact/environment.

**Expected behavior:** Mark exact receipt state MISMATCH, forbid candidate/deployed
wording and make requested candidate/deployed scope PARTIAL/BLOCKED. Commit-range
facts may remain valid.

**Assertions:**

- [ ] Tag is not a build/deployment receipt
- [ ] Build success is not deployment success
- [ ] Deployment receipt must chain to candidate artifact and to_commit/to_tree
- [ ] Local changelog write remains NOT_PUBLISHED

---

## Case 12: Authorization, ref drift and CAS failure

**Fixture:** Candidate entry is approved; before write, to_ref moves or target bytes
change. Another test proposes publishing the player draft.

**Expected behavior:** Re-resolve/re-hash all inputs. Drift invalidates mutation
authority and writes nothing. External publishing is outside scope and not performed.

**Assertions:**

- [ ] Narrative approval is not filesystem authorization
- [ ] Mutation manifest contains target/base/entry/file/history hashes and recorder
- [ ] Concurrent user edits are not overwritten or silently reverted
- [ ] Git refs/tags/commits, receipts and external systems are non-writes

---

## Protocol Compliance

- [ ] Exact from/to hashes reproduce the full untruncated range and net diff
- [ ] Surviving commit/diff evidence backs every claim
- [ ] Non-Git context only explains an already evidenced claim
- [ ] Version, candidate, deployment, local persistence and publication never collapse
  into one narrative state
- [ ] Sensitive player output is independently sanitized and never auto-published
- [ ] Keyed upsert preserves all history and has no overwrite escape hatch
- [ ] Output includes provenance/claim/receipt/redaction/target hashes, statuses,
  blockers and exactly one next action

---

## Coverage Notes

Cases 1–9 directly regress CL-001 and CL-002: count/tag-truncated Git ranges and
destructive changelog replacement. Cases 3–6 and 10–12 cover the adjacent net-change,
claim evidence, context, privacy, candidate/deployment, authorization and drift paths
that could otherwise produce false release history or unsafe public drafts.
