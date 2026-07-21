# Skill Test Spec: $launch-checklist

## Skill Summary

`$launch-checklist` evaluates one explicit launch-candidate manifest. Every check has
a stable ID, HARD/ADVISORY class, applicability rule, evidence contract, owner, and
hash. Local/build evidence must bind the exact candidate; external facts require a
verifiable provider receipt; human facts require an authorized owner attestation.

The deterministic vocabulary is `LAUNCH_READY`, `LAUNCH_BLOCKED`, `CONCERNS`,
`UNDETERMINED`, and `ERROR`. The skill never records the final launch decision and
has no director gate.

---

## Static Assertions

- [ ] YAML frontmatter contains only `name` and a non-empty `description`; name matches the skill directory
- [ ] Has at least two phase headings
- [ ] Requires one explicit launch manifest and exact release/candidate/build/artifact/source/platform identity
- [ ] Never selects launch evidence, releases, milestones, or prior reports by modification time
- [ ] Defines stable check IDs, HARD/ADVISORY gate classes, evidence types, owners, applicability, hashes, and load counters
- [ ] External facts default to UNKNOWN/MANUAL_REQUIRED until a provider receipt verifies
- [ ] Human facts require a hash-bound authorized owner attestation and cannot be model-signed
- [ ] Missing, stale, unavailable, or manual-required HARD evidence deterministically yields LAUNCH_BLOCKED
- [ ] Any incomplete/advisory concern prevents LAUNCH_READY
- [ ] Dry-run is zero-write, zero-sign-off, watermarked SIMULATION, and returns UNDETERMINED plus a projection
- [ ] Consumes only canonical hash-valid staged smoke/regression/soak/playtest/test-evidence artifacts
- [ ] Requires a recovery rehearsal receipt with RTO/RPO or hotfix objective and measured outcome
- [ ] Uses an immutable assessment path and never overwrites history
- [ ] Keeps objective readiness separate from Launch Decision: NOT_RECORDED
- [ ] No director gate or downstream workflow is invoked

---

## Case 1: Missing launch manifest fails closed

**Fixture:**

- The supplied path is absent, a directory, malformed, or outside the project root

**Input:** `$launch-checklist assess --manifest production/releases/r1/launch-manifest.yaml --assessment-id launch-r1-a`

**Expected behavior:**

- `Workflow Status: ERROR`
- `Readiness Verdict: ERROR`
- `Launch Decision: NOT_RECORDED`
- No evidence scan, gate, or file write occurs

**Assertions:**

- [ ] No newest-release fallback occurs
- [ ] No LAUNCH_READY or CONCERNS verdict appears
- [ ] The failed path/check is named

---

## Case 2: Candidate identity mismatch cannot produce readiness

**Fixture:**

- Launch manifest declares candidate C-17/build B-17/hash H17
- Candidate manifest or a test receipt declares another build/hash/commit

**Expected behavior:**

- Mismatch is identified with declared and observed values.
- `Workflow Status: ERROR`, `Readiness Verdict: ERROR`.
- No report is persisted.

**Assertions:**

- [ ] Version/date similarity cannot replace exact hashes
- [ ] Every build-bound source must use the same candidate identity

---

## Case 3: Missing external and human evidence blocks HARD checks

**Fixture:**

- Platform certification, privacy publication, age rating, production server, and
  legal approval are applicable HARD checks
- Local files or prose claims exist, but no valid provider receipts or owner
  attestations do

**Expected behavior:**

- Each row is `Check Status: UNKNOWN`, `Evidence Status: MANUAL_REQUIRED`.
- `Readiness Verdict: LAUNCH_BLOCKED`.
- The skill names the required issuer/owner and receipt schema.

**Assertions:**

- [ ] Local policy/store/media files do not become proof of publication or approval
- [ ] The model never creates or signs an attestation
- [ ] Necessary UNKNOWN items cannot become CONCERNS or LAUNCH_READY

---

## Case 4: Advisory manual items produce CONCERNS, not READY

**Fixture:**

- Every HARD check has current verified PASS/N-A evidence
- Screenshot visual quality and community briefing are ADVISORY and lack attestations

**Expected behavior:**

- Advisory rows are UNKNOWN/MANUAL_REQUIRED.
- `Readiness Verdict: CONCERNS`.
- Launch decision remains NOT_RECORDED.

**Assertions:**

- [ ] Advisory unknown prevents LAUNCH_READY
- [ ] It does not become a HARD blocker unless manifest policy says HARD
- [ ] Exact owner/evidence next step is shown

---

## Case 5: Complete current staged QA evidence can contribute PASS

**Fixture:**

- Smoke report is persisted sprint mode, PASS, Handoff Eligible YES, and exact
  candidate/QA-plan/test-manifest/log/evidence hashes verify
- Regression selection is current VERIFIED COVERAGE with a matching build-bound pass
  receipt and current test-source/sensitivity hashes
- Soak result is canonical COMPLETED, Gate Eligible YES, EXECUTED, readiness PASS,
  and required objective dimensions PASS for the exact profile/build
- Playtest result is canonical COMPLETED/Gate Eligible YES with matching build and
  verified manifest/raw/ledger/report hashes
- Test-evidence review is persisted COMPLETE/ADEQUATE/PASS/FULL/Closure Eligible YES

**Expected behavior:**

- Applicable QA check rows are PASS.
- No protocol, plan, selection-only file, quick smoke, or conversation result is
  accepted as completed execution evidence.

**Assertions:**

- [ ] Exact staged producer paths/statuses and transitive hashes are revalidated
- [ ] Every artifact matches the launch candidate
- [ ] Soak duration follows risk-profile rationale, not a universal fixed duration

---

## Case 6: Stale or partial QA evidence blocks readiness

**Variants:**

- Smoke is from the prior build or quick mode
- Regression selection changed after its execution receipt
- Soak is INCOMPLETE/INCONCLUSIVE or Gate Eligible NO
- Playtest is IN_PROGRESS or its raw hash changed
- Test-evidence review is conversation-only, UNKNOWN, targeted-only, or nonpersisted

**Expected behavior:**

- Affected HARD rows are STALE, UNKNOWN, or UNAVAILABLE.
- `Evidence Coverage: PARTIAL` when applicable.
- `Readiness Verdict: LAUNCH_BLOCKED`.

**Assertions:**

- [ ] No old result is promoted by date or filename
- [ ] Selection/protocol existence alone cannot pass
- [ ] Partial evidence cannot yield LAUNCH_READY

---

## Case 7: Failed rollback rehearsal is deterministically blocking

**Fixture:**

- Current recovery rehearsal receipt binds the candidate and production-equivalent
  environment
- Measured recovery exceeds declared RTO or data loss exceeds RPO
- All other checks pass

**Expected behavior:**

- Recovery check is HARD FAIL.
- `Readiness Verdict: LAUNCH_BLOCKED`.
- Logs, measured target, owner, and receipt hash are shown.

**Assertions:**

- [ ] A runbook document cannot override the failed rehearsal
- [ ] User optimism cannot relabel the evidence
- [ ] Retest requires a new immutable receipt

---

## Case 8: New build invalidates old attestations and receipts

**Fixture:**

- A prior assessment and owner attestations were valid for candidate C-16
- Current manifest is C-17 with changed build/artifact hash
- Previous path/hash is explicitly supplied for delta comparison

**Expected behavior:**

- Old build-bound rows become STALE.
- Delta is shown by stable check ID.
- Current verdict ignores prior PASS labels and follows current evidence.

**Assertions:**

- [ ] Typed sign-off names cannot carry across build change
- [ ] Previous assessment is never selected by mtime
- [ ] Current unresolved HARD rows block launch

---

## Case 9: Dry-run creates no verdict artifact or signatures

**Fixture:**

- Valid launch manifest and mixed current evidence

**Input:** `$launch-checklist dry-run --manifest production/releases/r1/launch-manifest.yaml --assessment-id sim-r1`

**Expected behavior:**

- Output begins/ends with the SIMULATION watermark.
- `Readiness Verdict: UNDETERMINED` plus labeled `Simulation Projection`.
- `Persistence: SIMULATION`, null report path/hash.
- No writes, attestations, signatures, submissions, or external actions occur.

**Assertions:**

- [ ] Projection is not presented as actual LAUNCH_READY/BLOCKED/CONCERNS verdict
- [ ] Dry-run cannot be consumed as durable evidence
- [ ] Launch Decision remains NOT_RECORDED

---

## Case 10: Fully verified candidate may be LAUNCH_READY

**Fixture:**

- Launch/candidate/build identities and all required sources verify
- Every applicable HARD and ADVISORY check is PASS or valid N-A
- External receipts, owner attestations, QA producers, operational rehearsals, and
  freshness rules are all current
- No load failures, unknowns, stale data, unavailable sources, or unresolved warnings
- Exact immutable report write/read-back succeeds

**Expected behavior:**

- `Workflow Status: COMPLETE`
- `Evidence Coverage: COMPLETE`
- `Readiness Verdict: LAUNCH_READY`
- `Persistence: VERIFIED`
- `Launch Decision: NOT_RECORDED`

**Assertions:**

- [ ] Report contains evidence snapshot and every transitive hash
- [ ] LAUNCH_READY is described as evidence readiness, not launch authorization
- [ ] No downstream gate/team/release action is invoked

---

## Director Gate Checks

None. `$launch-checklist` is a read-only readiness evaluator with an optional
immutable report.

## Protocol Compliance

- [ ] Exact bounded authorization covers only the optional report
- [ ] Input hashes are revalidated immediately before persistence
- [ ] Persistence failure does not change observed readiness but prevents durable use
- [ ] External/manual facts never pass without verified evidence
- [ ] Verdict algorithm is applied after all stable rows and load counters exist
- [ ] Catalog and workflow guide are not modified by this workflow

## Coverage Notes

The cases close the three P0 failures: fabricated external/manual PASS, undefined
verdict aggregation, and missing release-candidate identity. They also encode current
staged smoke, regression, soak, playtest, and test-evidence producer contracts,
partial/stale handling, immutable sign-offs, recovery rehearsal, dry-run isolation,
and separation of readiness from the final launch decision.
