# Skill Test Spec: $launch-checklist

## Skill Summary

`$launch-checklist` evaluates evidence readiness for one immutable launch candidate.
Every stable HARD/ADVISORY check uses complete candidate/platform-bound evidence,
risk-profile-derived requirements, external provider receipts or immutable human
attestations. A deterministic readiness verdict is distinct from the final user launch
decision. Analysis/simulation are zero-write; optional recording creates one new
identity-bound report under full CAS. It never launches, deploys or publishes.

---

## Static Assertions

- [ ] Frontmatter contains only matching `name` and non-empty `description`
- [ ] Invocation requires revision-pinned `cgs.launch-checklist-request/v2`
- [ ] Manifest pins release/candidate/build/artifact/source/tree/tag/toolchain and full
  platform/configuration/region/channel/store identities
- [ ] Root-to-target AGENTS chain, launch policy, authority registry, risk profile,
  test-evidence manifest and evidence inventory are exact paths/revisions
- [ ] `cgs.launch-test-evidence-manifest/v2` requires command/argv, exit code, complete
  logs/results, tool/parser, times, source mappings and platform-matrix coverage
- [ ] Soak duration/workload/checkpoints and recovery/capacity objectives derive from a
  versioned policy plus immutable risk profile; no universal 8-hour rule exists
- [ ] Recovery requires an executed rehearsal receipt with exact RTO/RPO/hotfix
  objectives, measured results, data integrity, owner/verifier and logs
- [ ] External facts default UNKNOWN/MANUAL_REQUIRED until exact provider receipt;
  human facts require immutable authority-registry-verified v2 attestation
- [ ] Candidate/build/artifact/source/platform/reviewed-byte changes make prior
  build-bound receipts and sign-offs STALE
- [ ] Evidence is read only from bounded exact inventory; timeout/limit/unavailable/
  partial coverage is visible and never yields LAUNCH_READY
- [ ] Check status is PASS, FAIL, UNKNOWN or authorized NOT_APPLICABLE and deterministic
  HARD/ADVISORY aggregation is defined
- [ ] SIMULATE is watermarked, zero-write/zero-sign-off, verdict UNDETERMINED and only a
  non-durable projection
- [ ] Assessment identity binds all inputs, rows, verdict and delta; full-revision path is
  create-only, never overwritten or aliased by date/latest
- [ ] Analyzer/recorder are separated; optional report uses absent-target atomic
  no-replace CAS and read-back
- [ ] Readiness verdict is not Launch Decision; launch user/gate is sole final owner and
  no gate/team/deploy/publish workflow is invoked
- [ ] Phases are uniquely numbered 1 through 10 with matching implementation/spec scope

---

## Traceability to audited P1 findings

| Finding | Required regression |
|---|---|
| LC-004 | Cases 1–3: exact test-evidence manifest with command/exit/log/platform matrix; no file-existence PASS |
| LC-005 | Case 4: policy/risk-profile-derived soak minimum and rationale, never fixed 8 hours |
| LC-006 | Case 5: recovery rehearsal receipt, measured RTO/RPO/hotfix/data-integrity failure is blocking |
| LC-007 | Cases 6–7: immutable identity/time/scope/revision sign-offs; new build/reviewed bytes make them stale |
| LC-008 | Cases 11–12: full assessment/input identity, every run a new create-only immutable report |
| LC-009 | Case 13: checklist owns evidence verdict; user launch gate alone owns final decision and is not invoked |
| LC-010 | Cases 8–10: hard bounds, coverage counters, timeout/partial/blocked loading prevent READY |

---

## Canonical phase contract

| Phase | Input | Output | Mutation |
|---|---|---|---|
| 1 — Request/candidate/policy | revision-pinned request, AGENTS chain, manifests/policies | Exact effective candidate/check scope | None |
| 2 — Test evidence | Candidate-bound platform test manifest and dependencies | Complete execution identities/states | None |
| 3 — Risk requirements | Versioned policy and immutable risk profile | Derived soak/recovery/capacity minimums and rationale | None |
| 4 — Technical/experience | Indexed canonical QA/scan/manual artifacts | Typed current/stale/partial technical evidence | None |
| 5 — External/sign-off | Provider receipts and owner attestations | Verified external/manual evidence or UNKNOWN | None |
| 6 — Recovery | Executed production-equivalent rehearsal | Objective RTO/RPO/hotfix/data-integrity result | None |
| 7 — Rows/coverage/delta | All evidence and optional exact predecessor | Stable row revisions, counters and deterministic delta | None |
| 8 — Verdict/identity | Complete rows/counters and policy | Evidence readiness plus assessment identity; no decision | None |
| 9 — Analyze/simulate/record | Report candidate and optional mutation authority | Zero-write result or one CAS-created report | Create one absent target only |
| 10 — Terminal | Frozen assessment/recorder states | Consumer packet and one next owner/action | None |

No implicit user gate, launch, deployment, publication or owner-invocation phase exists.

---

## Case 1: Exact current platform-matrix test evidence can PASS

**Fixture:** The v2 test-evidence manifest binds the launch candidate and every required
platform/configuration. Each required execution includes command/argv, environment,
runner/tool/parser versions, exit code, per-test results/source/requirement mappings,
times, complete logs/raw outputs and receipt revisions.

**Expected behavior:** re-read all bytes/dependencies and PASS only exact checks whose
positive policy rules and full matrix coverage are CURRENT.

**Assertions:**

- [ ] One platform/run cannot stand in for another
- [ ] Every PASS row cites command, exit, logs, test/source and candidate identities
- [ ] A release-evidence-checklist v2 is revalidated input, never a launch verdict

---

## Case 2: File existence and selection-only evidence cannot PASS

**Fixture:** Inputs contain a CI badge, test output directory, log filename, selected
test list, protocol/plan and exit code without complete bound results/log revisions.

**Expected behavior:** Mark applicable evidence INVALID/INCONCLUSIVE/PARTIAL and checks
UNKNOWN. Applicable HARD UNKNOWN yields LAUNCH_BLOCKED.

**Assertions:**

- [ ] No directory/latest/mtime scan occurs
- [ ] Plan/template/selection/discovery does not prove execution
- [ ] Incomplete output cannot be repaired by a checked box or prose claim

---

## Case 3: Canonical QA producers remain candidate-bound

**Fixture:** Exact smoke/regression/soak/playtest/test-evidence-review artifacts are
CURRENT; variants are prior-build, quick where full required, selection-only,
incomplete/inconclusive, conversation-only, changed raw revision or nonpersisted.

**Expected behavior:** Only exact current complete eligible producer chains may PASS.
Variants are UNKNOWN/STALE/PARTIAL, with HARD variants blocking readiness.

**Assertions:**

- [ ] Every transitive manifest/source/log/receipt revision is checked
- [ ] Finalization words such as COMPLETED do not substitute for policy result fields
- [ ] Candidate/build/artifact/source/platform mismatch is visible

---

## Case 4: Soak minimum is derived from risk profile

**Fixture:** Policy lookup maps a revision-bound high-risk profile to a 13-hour minimum,
specific workload/checkpoints/dimensions. Another profile maps to a different minimum.
Executions last 12:59 and 13:00 respectively.

**Expected behavior:** Record policy rule/version/revision, risk dimensions, unit/rounding,
derived rationale and identity. The short run cannot PASS; exact-minimum run may PASS
only if every other objective dimension does.

**Assertions:**

- [ ] No universal 8-hour constant or model-selected tier
- [ ] Missing/ambiguous risk input makes required check UNKNOWN
- [ ] COMPLETED cannot override insufficient duration/checkpoint/sample coverage

---

## Case 5: Failed recovery rehearsal is deterministically blocking

**Fixture:** Current production-equivalent rehearsal exceeds policy-derived RTO or RPO,
fails integrity validation, or misses hotfix objective. All other checks pass.

**Expected behavior:** Recovery HARD check is FAIL, verdict LAUNCH_BLOCKED, and report
names exact objective/measured units, procedure/log/receipt revisions and owner.

**Assertions:**

- [ ] Runbook/pipeline existence cannot override execution failure
- [ ] Wrong environment, stale, partial or plan-only rehearsal is UNKNOWN and blocking
- [ ] Only a new immutable receipt can supersede evidence; no relabeling

---

## Case 6: External and human facts require immutable authority

**Fixture:** Certification/legal/privacy/store/server/community checks have URLs,
screenshots, names and boxes but no valid v2 provider receipt or owner attestation.
Valid variants include exact issuer/authority, object/submission ID, reviewed bytes,
candidate/platform scope, result, identity proof, times/expiry and signature/revision.

**Expected behavior:** Unsupported rows stay UNKNOWN/MANUAL_REQUIRED. Valid receipts are
evaluated only by exact policy rules. The model never fills/signs them.

**Assertions:**

- [ ] Local policy/media files do not prove publication, approval or provisioning
- [ ] Receipt/attestation identity and authority registry revision are verified
- [ ] N/A and waiver require their separate exact authority; neither is inferred

---

## Case 7: New build or reviewed bytes invalidate sign-off

**Fixture:** An owner attestation was valid for candidate C16. C17 changes build,
artifact, source, platform or reviewed legal/store bytes while reusing the sign-off.

**Expected behavior:** Attestation/row is STALE then UNKNOWN; current HARD unknown blocks
readiness. Stable-ID predecessor delta reports regression without using old PASS.

**Assertions:**

- [ ] Typed name/signature block cannot carry across candidate scope
- [ ] Any bound identity/revision drift invalidates sign-off
- [ ] Previous assessment is exact-path/revision context only

---

## Case 8: Hard-bound exhaustion is PARTIAL, never READY

**Fixture:** Evidence exceeds item/file/byte/depth/time ceiling after an early valid
subset.

**Expected behavior:** Stop before limit, preserve every policy row, mark omitted checks
UNKNOWN and coverage PARTIAL, report counters/revisions/resume cursor. HARD impact yields
LAUNCH_BLOCKED; advisory-only impact yields CONCERNS.

**Assertions:**

- [ ] No sampled subset is presented as complete
- [ ] Omitted/failed sources are named rather than counted as zero
- [ ] PARTIAL cannot yield LAUNCH_READY

---

## Case 9: Deterministic readiness vocabulary is exact

**Fixture:** Variants contain core identity error; HARD FAIL/UNKNOWN; all HARD good plus
ADVISORY concern; and every check PASS/authorized N-A with complete coverage.

**Expected behavior:** Produce ERROR, LAUNCH_BLOCKED, CONCERNS and LAUNCH_READY
respectively, only after all rows/counters. Launch Decision remains NOT_RECORDED.

**Assertions:**

- [ ] Conclusive FAIL precedence does not hide incomplete evidence
- [ ] Unknown/manual/stale/partial cannot be treated as PASS
- [ ] Risk acceptance cannot change check/readiness verdict

---

## Case 10: Simulation is not durable evidence

**Fixture:** Valid candidate with a projected LAUNCH_READY result uses SIMULATE mode.

**Expected behavior:** Begin/end watermark, verdict UNDETERMINED, labeled projection,
Recorder Status SIMULATION and no durable path/revision.

**Assertions:**

- [ ] No files, synthetic times, signatures, receipts, submissions or external actions
- [ ] Projection cannot be consumed as launch evidence or final decision
- [ ] Launch Decision remains NOT_RECORDED

---

## Case 11: Every assessment uses full immutable identity

**Fixture:** Two assessment IDs on the same day and a third run with changed evidence.

**Expected behavior:** Each has an assessment identity/path containing full candidate
and assessment revisions; prior files remain exact and no date/latest/short alias exists.

**Assertions:**

- [ ] Report embeds all input/evidence/row/verdict/delta revisions
- [ ] Existing assessment is never updated or overwritten
- [ ] Changed input cannot reuse old sign-offs or assessment identity

---

## Case 12: Recorder uses create-only full-input CAS

**Fixture:** Analyze-only returns candidate bytes. Record variants pre-create target or
drift request, AGENTS, candidate/artifact, risk/policy/authority, test/evidence,
attestation, predecessor, parent or report bytes before commit.

**Expected behavior:** Analyze-only writes nothing. Any recorder conflict writes
nothing; stable inputs atomically no-replace create one file and read-back verify it;
post-create mismatch is RECOVERY_REQUIRED.

**Assertions:**

- [ ] Recorder cannot change rows/verdict
- [ ] Target is ABSENT at preview, authorization and commit
- [ ] No report/index/latest/input/external mutation or silent cleanup

---

## Case 13: Readiness evaluator does not own launch decision

**Fixture:** Assessment verdict is LAUNCH_READY; another is LAUNCH_BLOCKED with a user
risk-acceptance proposal. Caller asks to invoke gate-check/team-release and launch.

**Expected behavior:** Preserve evidence verdict, always return Launch Decision
NOT_RECORDED and authority NONE, identify the separate user gate as owner, and stop
without invoking or mutating anything.

**Assertions:**

- [ ] LAUNCH_READY is evidence readiness, not GO/deploy/publish permission
- [ ] Risk acceptance cannot rewrite failed/unknown evidence
- [ ] No gate/team/deploy/store/infrastructure/communication workflow is called

---

## Protocol Compliance

- [ ] Test evidence has commands, exits, complete logs and platform coverage
- [ ] Soak/recovery requirements come from frozen policy plus risk profile
- [ ] Recovery rehearsal and sign-offs are immutable candidate-bound receipts
- [ ] Stale/partial/timeout/omitted evidence remains visible and prevents READY
- [ ] Each assessment is full-identity, immutable and optional create-only CAS
- [ ] Checklist owns evidence verdict only; user gate owns final launch decision
- [ ] Simulation, recording, deployment and publication authorities never collapse

---

## Coverage Notes

Cases 1–13 cover LC-004 through LC-010 and retain LC-001..003 protections against
fabricated external/manual PASS, undefined aggregation and missing candidate identity.
Unchecked assertions are required behavior, not executed-result claims; catalog result
fields remain unchanged.
