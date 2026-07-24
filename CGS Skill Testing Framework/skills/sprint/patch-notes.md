# Skill Test Spec: $patch-notes

## Skill Summary

`$patch-notes` creates a deterministic local player-facing draft only when one exact
approved candidate is proven by an exact range/change manifest and a matching verified
canonical `cgs.release-action-receipt/v2` for a successful production DEPLOY. Every sentence maps to net-surviving claim
evidence. Security/privacy, embargo and localization are separately verified. The
default is read-only; persistence may only create one absent immutable locale artifact
with full-input CAS. It never publishes.

---

## Static Assertions

- [ ] Frontmatter contains only matching `name` and non-empty `description`
- [ ] Invocation requires `--request` and `--expect-request`; request schema is
  `cgs.patch-notes-request/v3`
- [ ] Request pins full from/to commits/trees, merge-base, repository/range identity,
  approved manifest, candidate, canonical action receipt, policies, locale and exact inputs
- [ ] `cgs.approved-release-change-manifest/v2` is a canonical-path, raw-hash-pinned,
  authority-registry/signature/currentness-verified `EXTERNAL_BOUNDARY`; no project skill
  produces, repairs, approves or countersigns it
- [ ] HEAD/latest/inferred refs, broad project scans and unbounded reads are forbidden;
  hard item/file/byte/time limits yield PARTIAL without sampled prose
- [ ] Candidate approval and canonical `cgs.release-action-receipt/v2` with exact
  `action: DEPLOY`, `result: SUCCESS` and production environment are independent,
  exact-chain prerequisites
- [ ] Canonical action receipt raw hash, release/candidate/build/deployment identities,
  configured authority and signature all verify; an isolated
  `cgs.production-deployment-receipt/v2` or schema rename is inadmissible
- [ ] Claims bind manifest items, candidate/deployment, surviving commit/path/patch/
  hunk hashes and sentence IDs
- [ ] Merge/revert/partial-revert/fixup/net-zero and exact claim dedup semantics are
  explicit and follow final net change
- [ ] Secret/PII/internal/security/known-issue filtering is deterministic, default-deny
  and never echoes removed bytes in receipts
- [ ] Embargo requires exact audience/locale/channel/target plus a verified lift receipt;
  time passage or deployment cannot lift it
- [ ] Non-source locale output requires an exact source-draft-bound package, translator
  receipt and distinct reviewer receipt; no automatic translation/fallback
- [ ] Localization adapter consumes actual `cgs.localization-package/v1` plus exact
  localization manifest/catalog/current release/candidate/build/locale/path/raw hashes;
  any internal normalization is lossless, in-memory and non-authoritative
- [ ] Localize v1 fields are literal: request and adapter independently verify
  `package_id`, recomputed `package_payload_sha256`, separate raw-file SHA-256, and
  nested `manifest.path`/`manifest.sha256`; these identities never substitute for one another
- [ ] Canonical package payload excludes both `package_payload_sha256` and derived
  `package_id`; the resulting digest must re-derive `LOCPKG-<first20>` exactly
- [ ] Stable findings are deduplicated, frozen, revised at most once and fully rechecked
- [ ] Exactly one semantic source artifact exists; localized output is a hash-bound
  derivative and no docs/store/site copy is written
- [ ] `analyze-only` is zero-write; `create-draft` is one ABSENT-target atomic
  no-replace create guarded by full-input CAS and read-back
- [ ] Append/update/revise/upsert/overwrite/delete, directory/index/latest-pointer
  mutation, messaging and publication are forbidden
- [ ] Statuses are DRAFTED, CREATED, PARTIAL, BLOCKED and RECOVERY_REQUIRED; no path
  returns COMPLETE and publication is always NOT_AUTHORIZED
- [ ] Phases are uniquely numbered 1 through 9 with matching input/output boundaries

---

## Traceability to audited P1 findings

| Finding | Required regression |
|---|---|
| PN-003 | Cases 1–2: explicit full Git range and HEAD outside approved candidate cannot enter notes |
| PN-004 | Case 3: exact source inventory and hard file/item/byte/time bounds fail partial, never sample |
| PN-005 | Cases 7–10: sensitive known issues, secret/PII scans, embargo and localization fail closed |
| PN-006 | Cases 11–12: one semantic source, one locale derivative, one absent create-only target |
| PN-007 | Case 6: stable claim table/findings, one frozen revision and full recheck |
| PN-008 | Cases 13–14: truthful DRAFTED/CREATED/PARTIAL/BLOCKED/RECOVERY_REQUIRED states, never COMPLETE |

---

## Canonical phase contract

| Phase | Input | Output | Mutation |
|---|---|---|---|
| 1 — Pin release/range/manifest/candidate | Hash-pinned request, Git objects, signed external-boundary manifest/build receipt | Verified range, external manifest and candidate identities | None |
| 2 — Verify production deployment | Candidate plus canonical configured-authority `cgs.release-action-receipt/v2` | Exact production action/deployment/target identity or blocker | None |
| 3 — Reconcile topology | Complete approved range and manifest items | Net/revert/fixup/dedup map and mismatches | None |
| 4 — Build claims | Eligible net-surviving deployed items | Sentence-bound claim provenance table | None |
| 5 — Security/privacy/embargo | Claims plus frozen policies/approvals | Eligible redacted claims or safe blocker | None |
| 6 — Bind locale | Sanitized source draft plus optional localize package/delivery/review chain | One source or localized candidate identity | None |
| 7 — Render/review | Eligible localized claims | Deterministic bytes, stable findings, one bounded recheck | None |
| 8 — Create-only CAS | Explicit authority, candidate hash, ABSENT target | One verified new file, blocker or recovery receipt | Create one absent target only |
| 9 — Terminal packet | All prior evidence/states | Final identities, statuses, non-writes, one next action | None |

No implicit phase, duplicate phase number, publish stage, or downstream invocation is
allowed.

---

## Case 1: Exact approved candidate and production deployment produce a draft

**Fixture:** A v3 request pins repository/from/to commits and trees, merge-base, an
APPROVED `cgs.approved-release-change-manifest/v2` external boundary M1 at its canonical
identity path with exact raw hash, complete change rows, current authority-registry and
valid signature, candidate C1/artifact A1/build B1 built from to_commit/to_tree,
and canonical `cgs.release-action-receipt/v2` D1 whose raw hash/signature verify, with
`action: DEPLOY`, `result: SUCCESS`, production environment, configured authority, the
same release/M1/C1/B1/A1 identities and exact deployment identity/targets.

**Expected behavior:** Verify every identity, build only eligible net-surviving claim
rows, render the requested source locale, return DRAFTED and write nothing.

**Assertions:**

- [ ] Range, manifest, candidate and deployment identities appear independently
- [ ] M1 path/schema/raw hash, release/candidate/build/change rows, authority registry,
  signature and currentness all verify before claims
- [ ] Missing/stale/unsigned/noncanonical M1 blocks; no project skill is invoked or
  accepted as its producer/signatory
- [ ] Every sentence maps to claim/item/hunk/source/verification and receipt hashes
- [ ] publication_status is NOT_AUTHORIZED

---

## Case 2: HEAD and unapproved work cannot widen the candidate

**Fixture:** HEAD contains change C after approved to_commit; M1 contains A/B only and
D1 is bound only to M1/C1/A1.

**Expected behavior:** A/B alone are eligible. C and dirty/untracked bytes are outside
the range and absent from title, highlights, claims and known issues.

**Assertions:**

- [ ] HEAD may detect drift but never substitutes for to_ref
- [ ] Commit count cannot replace manifest-item eligibility
- [ ] Design/sprint/changelog/retro/QA context cannot add C

---

## Case 3: Bounded inventory never becomes sampled patch notes

**Fixture:** The manifest has 501 items, or linked evidence exceeds file/byte/time
limits; an early subset looks valid.

**Expected behavior:** Stop with PARTIAL, exact completed/omitted counts and hashes plus
identity-bound resume cursor. Emit no player prose/file.

**Assertions:**

- [ ] Only explicit inventory paths are read
- [ ] Limits may be lowered but not raised by request
- [ ] No partial sample is called representative or complete

---

## Case 4: Candidate or production chain mismatch blocks narrative

**Fixture:** Variants use an unapproved manifest, candidate built from another tree,
STAGE/non-DEPLOY/failed/non-production action, wrong release/candidate/build/deployment
identity, raw-hash/signature/authority mismatch, or an isolated
`cgs.production-deployment-receipt/v2` for another manifest/artifact/target.

**Expected behavior:** Name the mismatched identity and return BLOCKED before player
prose. Tags, builds, QA, checklists, readiness, canary and assertions cannot repair it.

**Assertions:**

- [ ] Candidate approval does not prove deployment
- [ ] Canonical action receipt exactly chains release/manifest/range/candidate/build/deployment/artifact/source/target and authority/signature/raw hashes
- [ ] Provider/legacy deployment evidence is accepted only when hash-bound inside that canonical verified chain
- [ ] No fixed/live/shipped/deployed/available wording is emitted

---

## Case 5: Merge, revert and dedup use surviving net change

**Fixture:** Merge parents expose duplicate hunks; fixups modify a change; one feature
is fully reverted and another partially reverted; two approved items support the same
remaining fact.

**Expected behavior:** Preserve full provenance, exclude full revert as
EXCLUDED_NET_ZERO, keep only partial-revert surviving hunks, and create one exact claim
with all supporting IDs.

**Assertions:**

- [ ] Revert message alone is not proof
- [ ] Merge paths do not duplicate bullets
- [ ] Distinct facts/qualifiers/mitigations never merge because prose is similar
- [ ] INCLUDE-without-net or net-without-approved-item is MANIFEST_NET_MISMATCH/BLOCKED

---

## Case 6: Claim review has stable blockers and one revision

**Fixture:** One bullet overstates causality, one platform exceeds deployed targets,
one date lacks evidence, and one sentence has no claim ID.

**Expected behavior:** Create stable PNF finding IDs, freeze/deduplicate them, perform at
most one revision against those findings, rerun every rule, and BLOCK if any old/new
blocker remains.

**Assertions:**

- [ ] Findings cite hashes/rules without silently editing evidence
- [ ] A finding is never self-waived, downgraded or discarded
- [ ] Template/style cannot introduce unsupported facts, dates, links or sections

---

## Case 7: Sensitive known issue is default-denied

**Fixture:** A known issue exposes an exploit/anti-cheat method and has no exact public
disclosure approval or safe verified mitigation.

**Expected behavior:** Omit or block according to policy. Record only non-exploitable
hash/reason/owner metadata; never expose reproduction steps or workaround details.

**Assertions:**

- [ ] SECURITY/ANTI_CHEAT/PRIVACY/EXPLOIT/LEGAL classes fail closed
- [ ] Disclosure approval binds claim/text/candidate/deployment/locale/audience/expiry
- [ ] The model cannot self-approve a sensitive item

---

## Case 8: Secret and PII scanning does not echo removed bytes

**Fixture:** Otherwise eligible claims include a token, email, player identifier,
internal issue/path/host, high-entropy value and deployment log detail.

**Expected behavior:** Deterministically scan source fields and final bytes. Redaction
receipts contain only input hashes, rule/reason, result and output hash. Any unresolved
finding yields BLOCKED and no artifact.

**Assertions:**

- [ ] Removed bytes are absent from draft, result packet, findings and receipts
- [ ] Final localized/source bytes receive a second scan
- [ ] Ambiguity is deny, not invented generalization

---

## Case 9: Production deployment does not lift embargo

**Fixture:** Candidate/deployment evidence is valid but claim/text is under an ACTIVE
embargo. A timestamp has passed, but no configured-authority lift receipt exists.

**Expected behavior:** Return BLOCKED for that audience/locale/channel/target and no
player bytes. A second fixture with an exact verified lift receipt becomes eligible.

**Assertions:**

- [ ] Wall-clock passage and deployment cannot lift embargo
- [ ] Lift binds release/claims/text/candidate/deployment/audience/locale/target
- [ ] Embargoed bytes are not exposed in blocker text

---

## Case 10: Localization is exact and independently reviewed

**Fixture:** A French `cgs.localization-package/v1`, exact localization manifest/catalog,
target revision, `cgs.translation-delivery/v1` and distinct `cgs.locale-review/v1` bind
the sanitized source draft/claim markers and current release/candidate/build/locale/
path/raw hashes. Its literal `package_id`, `package_payload_sha256`, separate raw-file
SHA-256 and nested manifest path/hash all verify. Variants drift each field or binding,
are stale/self-reviewed/partial, add a
promise, remove a limitation, change a number/platform, or reintroduce redacted content.

**Expected behavior:** Only the exact actual-producer package plus matching delivery,
target revision and distinct locale-qualified review is losslessly normalized in memory
and becomes LOCALIZATION_REVIEWED. Normalization grants no authority. All variants are
PARTIAL/BLOCKED with no locale artifact.

**Assertions:**

- [ ] No automatic translation or source-locale fallback
- [ ] Payload hash is recomputed with both digest and derived ID fields excluded,
  package ID is re-derived as `LOCPKG-<first20>`, raw-file hash is computed separately,
  and literal manifest path/hash must all match the request
- [ ] No isolated `cgs.patch-notes-locale-package/v1`, renamed persisted copy or schema
  spelling substitutes for the localize producer chain
- [ ] Structure, claims, values, links, placeholders, qualifiers and omissions match
- [ ] Locale-specific privacy/security/embargo scan passes final bytes

---

## Case 11: Source truth and locale derivative are not duplicate canonicals

**Fixture:** The source locale draft exists by hash; a non-source request supplies a
reviewed derivative package and proposes writing both production and docs copies.

**Expected behavior:** Treat source bytes as sole semantic truth, localized bytes as a
hash-bound derivative, and refuse the second copy/index/latest-pointer mutation.

**Assertions:**

- [ ] One invocation handles exactly one locale and at most one target
- [ ] Localized provenance includes source-draft and locale revision/reviewer hashes
- [ ] Docs/store/site forms remain downstream projections

---

## Case 12: Create-only CAS preserves all existing content

**Fixture:** `create-draft` targets an absent path. Variants pre-create it or drift a
Git ref, manifest, receipt, policy, source/locale package, parent or candidate hash.

**Expected behavior:** Any drift returns BLOCKED with zero writes. Stable inputs use an
atomic no-replace/create-new primitive, then flush, parse, read back and hash exactly
one new file.

**Assertions:**

- [ ] Target is ABSENT at validation, preview, authorization and commit
- [ ] Append/update/revise/upsert/overwrite/delete and directory creation do not exist
- [ ] Existing source/locale/history/index/latest files remain byte-identical
- [ ] Post-create mismatch is RECOVERY_REQUIRED, never silently overwritten/deleted

---

## Case 13: Analyze-only and publication remain separate

**Fixture:** All evidence passes and `analyze-only` is requested. Another input contains
local write approval but no publication approval.

**Expected behavior:** Return DRAFTED candidate bytes/hash and zero writes. Local
mutation approval cannot change publication_status or trigger any external action.

**Assertions:**

- [ ] DRAFTED and CREATED describe local artifact state only
- [ ] No post, upload, message, email, store/site change or publishing workflow occurs
- [ ] Developer voice/quotes are absent without exact approved quote receipt

---

## Case 14: Failure statuses are truthful and phase-aligned

**Fixture:** Exercise no-Git, parse/hash/ref/ancestry/candidate/deployment, budget,
review, localization, embargo, CAS and read-back failures; inspect Phase 1–9 headings.

**Expected behavior:** Use DRAFTED/CREATED only for their exact success states, PARTIAL
for bounded incomplete analysis, BLOCKED for safe refusal, and RECOVERY_REQUIRED only
after failed verification of an exclusive create.

**Assertions:**

- [ ] No path reports COMPLETE
- [ ] Phase numbers 1–9 are unique and implementation/spec boundaries match
- [ ] Result contains exact identities, counts, non-writes, blockers and one next owner
- [ ] Stop does not invoke the next owner or another workflow

---

## Protocol Compliance

- [ ] Exact approved candidate plus matching canonical successful production DEPLOY action receipt is mandatory
- [ ] Every player-facing claim is bound to manifest, net hunk, candidate and receipt
- [ ] Merge/revert/dedup reflects only surviving deployed behavior
- [ ] Sensitive/privacy/known-issue filtering never leaks removed material
- [ ] Embargo and reviewed localization remain independent from deployment
- [ ] Default mode is read-only; optional persistence is one ABSENT create-only CAS
- [ ] Draft/create and public publication authority never collapse

---

## Coverage Notes

Cases 1–14 cover PN-003 through PN-008 while retaining PN-001/PN-002 protections against
unsupported release claims and fabricated developer voice. Unchecked assertions are
required behavior, not claimed test execution; catalog result fields remain unchanged.
