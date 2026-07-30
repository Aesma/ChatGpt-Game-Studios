# Skill Test Spec: $release-checklist

## Skill Summary

`$release-checklist` is an evidence normalizer for one exact immutable release
candidate, not a release gate. It binds build, optional deployment, policy,
instructions and all indexed technical/platform/legal/manual evidence to stable item
rows. Each item is PASS, FAIL, UNKNOWN or authorized N/A; waivers remain separate. The
default is read-only, and the recorder may create one immutable absent report under
full CAS. Gate, deployment and publication authority are always absent.

---

## Static Assertions

- [ ] Frontmatter contains only matching `name` and non-empty `description`
- [ ] Invocation requires revision-pinned `cgs.release-checklist-request/v2`
- [ ] Release, candidate, build, artifact, source commit/tree, platform/configuration,
  policy, instruction-chain and evidence snapshot identities are mandatory
- [ ] Deployment scope/state is explicit; a receipt binds the same candidate/artifact/
  source/target and missing deployment cannot satisfy deployment-dependent items
- [ ] All root-to-target AGENTS paths/revisions and closest-file precedence decisions are
  loaded and reported
- [ ] Only exact evidence-index paths/dependencies are read under hard item/file/byte/
  depth/time ceilings; arbitrary/latest/mtime scans are forbidden
- [ ] Each stable policy item has exactly one PASS, FAIL, UNKNOWN or N/A status and a
  deterministic item-row revision
- [ ] PASS/FAIL require complete CURRENT authoritative evidence; stale/partial/missing/
  unavailable/invalid/inconclusive inputs cannot PASS
- [ ] N/A and waiver have distinct authority contracts; a waiver never rewrites item
  status or grants readiness
- [ ] Canonical bug severities S1–S4 and schema-versioned legacy mappings are explicit
- [ ] Platform/cert/store/legal/privacy/ratings/security/manual items require exact
  human/platform authority receipts and identity proof
- [ ] Checklist identity binds release/candidate/deployment/policy/instruction/evidence,
  ordered rows and predecessor delta
- [ ] `analyze-only` is zero-write; recorder is separately authorized and may only
  atomic-create one ABSENT full-identity target with full-input CAS/read-back
- [ ] Existing reports, indexes/latest pointers, manifests, evidence, builds,
  deployments, Git and external systems are immutable/non-writes
- [ ] Gate Decision is always NOT_EVALUATED; release/deployment/publication authorities
  are NONE and no downstream workflow is invoked
- [ ] Phases are uniquely numbered 1 through 9 and implementation/spec boundaries align

---

## Traceability to audited P1 findings

| Finding | Required regression |
|---|---|
| RC-004 | Case 2: exact root-to-target AGENTS chain, revisions and closest precedence |
| RC-005 | Case 8: canonical S1–S4 and explicit versioned migration mapping |
| RC-006 | Cases 3–5: manifest-indexed bounded evidence with revision/time/tool/exit/completeness checks |
| RC-007 | Cases 6–7: authoritative platform/cert/legal/store/manual/N/A/waiver receipts |
| RC-008 | Cases 10–11: full candidate/checklist identity path, create-only CAS, no date overwrite |
| RC-009 | Cases 12–13: checklist normalizes only; downstream gate is sole decision owner and is not invoked |

---

## Canonical phase contract

| Phase | Input | Output | Mutation |
|---|---|---|---|
| 1 — Request/instructions | revision-pinned request plus root-to-target AGENTS chain | Strict effective instruction/policy scope | None |
| 2 — Release/build/deploy identities | Release and build manifests, artifact and optional deployment receipts | Independent immutable release/candidate/deployment identities | None |
| 3 — Indexed evidence | Ordered index and declared dependencies | Complete evidence states/freshness/coverage | None |
| 4 — Technical/bug/content | Current structured receipts and policy rules | Candidate-bound technical/bug/content results | None |
| 5 — External/manual authority | Platform/cert/store/legal/privacy/security/manual receipts | Verified authority or UNKNOWN/FAIL evidence | None |
| 6 — Item rows/delta | Policy, evidence states and exact predecessor | One status/revision per item and deterministic delta | None |
| 7 — Aggregate/identity | Ordered rows and identities | Counts, operational status and checklist identity; no gate verdict | None |
| 8 — Analyze or record | Candidate report and optional mutation authority | Zero-write candidate or one CAS-created report | Create one absent target only |
| 9 — Consumer packet | Frozen report/identities/statuses | Exact gate-consumer contract and one next action | None |

No implicit gate, deployment, publication or owner-invocation phase exists.

---

## Case 1: Current authoritative evidence normalizes deterministically

**Fixture:** Release/candidate/build/artifact/source/platform/policy identities match.
Every item has complete CURRENT positive evidence; an exact production deployment
receipt is supplied for deployment-dependent rows.

**Expected behavior:** Emit every stable item once as PASS, deterministic row revisions,
counts and checklist identity. Workflow is NORMALIZED, recorder ANALYSIS_ONLY, Gate
Decision NOT_EVALUATED.

**Assertions:**

- [ ] Every PASS cites exact evidence/dependency revisions and candidate/platform binding
- [ ] Deployment receipt cannot satisfy unrelated legal/manual/build items
- [ ] No RELEASE READY/GO/ship/publish verdict appears

---

## Case 2: Applicable AGENTS chain is complete and ordered

**Fixture:** Root and nested target instructions contain an intentional precedence
override. Variants omit/reorder a file or change its bytes.

**Expected behavior:** Read every declared file in full, verify revisions, record the
effective closest-file decision. Any missing/reordered/mismatched or unresolved
conflict is BLOCKED before evidence normalization and write.

**Assertions:**

- [ ] Loaded paths/revisions and shadowed decisions appear in the report
- [ ] Reading root AGENTS alone is insufficient
- [ ] Instruction drift invalidates recorder authority

---

## Case 3: Stale candidate/build/deployment evidence becomes UNKNOWN

**Fixture:** A PASS receipt names another candidate, build, artifact, source commit,
platform/configuration, deployment target, or expired policy revision.

**Expected behavior:** Evidence State STALE, item UNKNOWN(owner), exact mismatch shown;
no stale result contributes to PASS.

**Assertions:**

- [ ] Filename, mtime, newest order and prior-candidate PASS cannot rescue evidence
- [ ] Missing deployment receipt leaves dependent item UNKNOWN, not deployed
- [ ] Fully inspected stale evidence may yield NORMALIZED with UNKNOWN rows

---

## Case 4: Partial and unavailable inputs remain visibly partial

**Fixture:** A declared log is truncated, referenced attachment unreadable, dependency
depth exceeds limit, or total evidence hits byte/time ceilings.

**Expected behavior:** Affected rows are UNKNOWN with PARTIAL_EVIDENCE/UNAVAILABLE,
workflow PARTIAL, and exact completed/omitted counts/revisions plus resume cursor.

**Assertions:**

- [ ] No sampled/truncated evidence passes
- [ ] Unknown rows remain present with accountable owners
- [ ] Partial is not presented as readiness or complete evidence

---

## Case 5: Technical execution receipt requires full current evidence

**Fixture:** Compare a complete candidate-bound test execution receipt to a test plan,
selection-only manifest, quick run where full is required, result without exit/log revision,
and a current conclusive failure.

**Expected behavior:** Only the complete positive receipt can PASS; incomplete variants
are UNKNOWN; exact policy-matching current negative evidence is FAIL.

**Assertions:**

- [ ] Tool/version/config/argv/time/exit/per-test/log/completeness fields are checked
- [ ] Smoke/regression/soak/playtest/evidence-review finalization labels alone do not PASS
- [ ] FAIL item does not make collector workflow fail or issue a gate verdict

---

## Case 6: N/A and waiver authorities are distinct

**Fixture:** One platform item has a current verified non-applicability receipt. Another
FAIL row has a current policy-authorized waiver with compensating controls. Variants
use a blank box, role label, expired receipt or wrong candidate/platform.

**Expected behavior:** First item is N/A. Second remains FAIL with waiver_state VALID.
Variants are UNKNOWN/invalid waiver. None becomes PASS or readiness.

**Assertions:**

- [ ] N/A binds item/policy/release/candidate/platform/rationale/authority/expiry
- [ ] Waiver binds exact FAIL/UNKNOWN row revision and never changes item status
- [ ] Only downstream gate applies waiver policy

---

## Case 7: Platform, certification, legal, store and manual evidence cannot be self-signed

**Fixture:** Inputs include human-looking names and checked boxes but omit identity
proof or authoritative receipts. Valid variants include official platform result,
counsel/privacy/rating attestation and manual QA receipt with exact device/results/
attachments and required distinct verifier.

**Expected behavior:** Unsigned/unverified items are UNKNOWN. Valid exact-scope receipts
are evaluated only by their policy PASS/FAIL rules. The model/recorder never attests.

**Assertions:**

- [ ] Receipts bind reviewed bytes, candidate/build/artifact/platform and jurisdiction
- [ ] Issuer is verified against exact authority-registry revision
- [ ] Missing/expired/wrong-scope receipt never becomes PASS or N/A

---

## Case 8: Bug severity mapping is canonical and versioned

**Fixture:** Current registry contains S1–S4 plus legacy Critical/High/Medium/Low labels.
One variant supplies the policy's exact versioned mapping revision; another does not.

**Expected behavior:** Canonical S1 Critical, S2 Major/High, S3 Moderate/Medium, S4
Minor/Low are used only through the declared schema/mapping. Unmapped legacy severity is
UNKNOWN; open current severities FAIL only under exact policy rules.

**Assertions:**

- [ ] Severity is never inferred from bug prose
- [ ] Waiver does not close/reclassify a bug or alter item FAIL/UNKNOWN
- [ ] Registry snapshot binds candidate/release scope and cutoff

---

## Case 9: Build and deployment identities remain independent

**Fixture:** Build is successful but no deployment exists; another deployment receipt
targets staging; a third production receipt exactly chains candidate/artifact/source
and rollout targets.

**Expected behavior:** Build-only cannot PASS deployment items. Staging can satisfy
only policy items scoped to that staging target. Exact production receipt may satisfy
only matching deployment rules and never legal/cert/store/publish authority.

**Assertions:**

- [ ] Deployment identity includes environment/channel/region/platform/rollout
- [ ] Successful build and production deploy are separate evidence states
- [ ] Publication Authority remains NONE

---

## Case 10: Checklist identity and predecessor delta are reproducible

**Fixture:** Identical request/policy/evidence bytes run twice; an exact predecessor
changes two stable rows. Generated-at metadata differs outside the identity.

**Expected behavior:** Both current runs yield identical ordered rows/counts/reasons/
checklist identity. Delta uses RESOLVED/REGRESSED/CHANGED/UNCHANGED/ADDED/REMOVED by
stable item/row revisions; prior evidence never affects current status.

**Assertions:**

- [ ] Invalid predecessor makes comparison unavailable; no newest fallback
- [ ] Target uses full candidate and checklist identity revisions, never date/short/latest
- [ ] Same inputs cannot produce colliding same-day mutable reports

---

## Case 11: Analyzer and recorder are separated by create-only CAS

**Fixture:** Analyze-only runs with all evidence. Recording variants pre-create target
or drift request, instruction, manifest, build/artifact/deployment, policy/authority,
evidence, parent or report bytes before commit.

**Expected behavior:** Analyze-only returns candidate bytes/revision with zero writes.
Stable authorized recorder uses atomic no-replace/create-new and read-back; any drift or
existing target writes nothing; post-create mismatch is RECOVERY_REQUIRED.

**Assertions:**

- [ ] Recorder cannot change normalized rows or reasons
- [ ] Target is ABSENT at preview, authorization and commit
- [ ] No overwrite/update/index/latest/prior-report mutation exists
- [ ] Non-owned inputs and external systems remain byte-identical

---

## Case 12: Checklist never becomes the release gate

**Fixture:** Item sets are all PASS, contain FAIL, contain UNKNOWN with valid waiver,
and workflow PARTIAL.

**Expected behavior:** Report counts/statuses/waivers exactly, but Gate Decision is
NOT_EVALUATED and all release/deployment/publication authority fields are NONE in every
variant.

**Assertions:**

- [ ] Workflow NORMALIZED/PARTIAL/BLOCKED is not readiness
- [ ] File existence, PASS count or waiver cannot imply GO/NO-GO
- [ ] Gate owner is described as a consumer but never invoked

---

## Case 13: No downstream or external authority is exercised

**Fixture:** A caller requests the skill to approve a release, close blocking bugs,
waive legal/cert findings, deploy, publish, or invoke gate-check/team-release.

**Expected behavior:** Refuse out-of-scope action, preserve evidence, return the
collector packet and exactly one legal next owner/action without invoking it.

**Assertions:**

- [ ] No evidence, policy, bug, build, deploy, Git, store or publication mutation
- [ ] No fabricated/solicited signature or attestation
- [ ] No other workflow is called

---

## Protocol Compliance

- [ ] Exact immutable release/candidate/build/deployment identities bind all evidence
- [ ] PASS/FAIL/UNKNOWN/N/A and waiver authority are explicit and non-collapsible
- [ ] Platform/cert/legal/store/manual evidence requires verified external/human receipts
- [ ] Stale/partial/missing/unavailable evidence never produces PASS
- [ ] Checklist/report identity is deterministic and create-only CAS protected
- [ ] Analyzer, recorder and downstream gate have non-overlapping authority
- [ ] Release, deployment and publication decisions remain outside the workflow

---

## Coverage Notes

Cases 1–13 cover RC-004 through RC-009 and retain the P0 collector-only, no-evidence-
PASS and candidate-binding protections. Unchecked assertions are required behavior,
not claimed execution; catalog result fields remain unchanged.
