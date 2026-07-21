# Skill Test Spec: $team-qa

## Skill Summary

Orchestrates an evidence-bound QA cycle for one exact build candidate. The skill
requires an exact current QA plan and canonical passing smoke handoff before any
execution artifacts are created, consumes structured automated/manual/playtest/
soak receipts, freezes an auditable evidence index, and derives signoff using
separate Workflow Status and QA Verdict axes. It never allocates bug numbers in
parallel.

---

## Static Assertions (Structural)

- [ ] TQA-S001: YAML frontmatter contains only `name` and a non-empty
  `description`; `name` is `team-qa`.
- [ ] TQA-S002: Invocation exposes explicit `start`, `ingest`, `status`, and
  `finalize` modes with exact paths.
- [ ] TQA-S003: The skill forbids "latest", "most recent", mtime selection, and
  session-state inference.
- [ ] TQA-S004: Missing, unknown, stale, quick, warning-bearing, or unpersisted
  smoke evidence maps to `BLOCKED_AT_ENTRY`, `INCOMPLETE`, and
  `SMOKE EVIDENCE REQUIRED`; no execution or signoff writes are allowed.
- [ ] TQA-S005: Candidate, QA-plan, smoke, automated, manual, playtest, soak,
  evidence-index, and review evidence all require exact build/hash binding.
- [ ] TQA-S006: Automated PASS requires command/argv, runner/version, exit code,
  per-test results/counts, logs/results hashes, stable IDs, and build provenance.
- [ ] TQA-S007: Automated `NOT_RUN`, `STALE`, `INVALID`, and `UNKNOWN` are
  explicitly nonconclusive and cannot become PASS.
- [ ] TQA-S008: Manual evidence requires tester, timestamps, platform/device,
  stable IDs, per-step actuals, attestation, and attachment/log hashes.
- [ ] TQA-S009: A user's chat choice and an agent summary are explicitly not
  execution evidence.
- [ ] TQA-S010: `Workflow Status` and `QA Verdict` are independent axes;
  `COMPLETE` never implies `APPROVED`.
- [ ] TQA-S011: Required `BLOCKED` or `NOT_RUN` rows force `INCOMPLETE` unless
  there is a hash-bound explicit exclusion approval.
- [ ] TQA-S012: Denominator arithmetic reports declared, excluded, required,
  pass, fail, blocked, not-run, stale, invalid, and unknown counts.
- [ ] TQA-S013: Valid current failure takes precedence over incomplete evidence
  as `NOT_APPROVED` while incomplete rows remain visible.
- [ ] TQA-S014: The skill forbids scanning, reserving, incrementing, or writing
  `BUG-NNN` and `production/qa/bugs/**`; it emits collision-resistant occurrence
  IDs for a serialized `bug-report` owner.
- [ ] TQA-S015: Finalize requires the exact staged `test-evidence-review` axes:
  COMPLETE, ADEQUATE, PASS, FULL, Closure Eligible YES.
- [ ] TQA-S016: Playtest `COMPLETED` and soak `COMPLETE` are not treated as PASS
  without their gate, identity, execution, readiness, dimension, and hash checks.
- [ ] TQA-S017: `Gate Eligible: YES` is possible only for persisted
  `QA Verdict: APPROVED`.
- [ ] TQA-S018: Metadata display name is `Team QA` and its prompt describes the
  exact-candidate evidence contract.

---

### Case 1: Missing or UNKNOWN smoke evidence blocks at entry

**Fixture:**

- Exact candidate manifest and current QA plan are valid.
- No canonical smoke report exists for the candidate, or the supplied report has
  `Verdict: INCOMPLETE` with an UNKNOWN row.
- No `production/qa/team-runs/tqa-run-001/` directory exists.

**Input:**

`$team-qa start sprint-12 --run-id tqa-run-001 --candidate production/builds/cand-12/manifest.md --qa-plan production/qa/qa-plan-sprint-12-2026-07-22.md --smoke-receipt production/qa/evidence/smoke/cand-12/smoke-001/report.md`

**Expected writes:**

- None.

**Expected non-writes:**

- No team-run directory, manifest, strategy, cases, evidence index, signoff, bug,
  session-state, or review-mode file.

**Expected behavior:**

1. Reads only the exact candidate, plan, and supplied smoke path.
2. Does not search for another report or select by mtime.
3. Returns `Workflow Status: BLOCKED_AT_ENTRY`,
   `QA Verdict: INCOMPLETE`, `Gate Eligible: NO`, and
   `Reason: SMOKE EVIDENCE REQUIRED`.
4. May show a draft strategy only in conversation.
5. Does not delegate test execution or manual testing.

**Assertions:**

- [ ] TQA-C01-A: UNKNOWN is never accepted as pass-with-warnings.
- [ ] TQA-C01-B: No QA execution or signoff artifact is created.
- [ ] TQA-C01-C: The response names the exact missing/nonconclusive smoke row.

---

### Case 2: A newer wrong-build report cannot replace the supplied receipt

**Fixture:**

- Candidate `cand-a`, build hash `aaa...`, current QA plan, and canonical passing
  smoke report `smoke-a/report.md` are supplied.
- A later-mtime `smoke-b/report.md` exists for candidate `cand-b`, build hash
  `bbb...`.
- Variant A supplies `smoke-a/report.md` and all hashes match.
- Variant B supplies `smoke-b/report.md` while the candidate remains `cand-a`.

**Input:**

Run `start` for both variants with distinct run IDs.

**Expected writes:**

- Variant A may create its authorized team-run manifest, strategy, and cases.
- Variant B writes nothing.

**Expected non-writes:**

- Neither variant edits either smoke report or selects a third report.

**Expected behavior:**

1. Variant A consumes the exact supplied `smoke-a` report even if it is older.
2. Variant B detects candidate/build/artifact/source/platform/QA-plan mismatch and
   returns `BLOCKED_AT_ENTRY / INCOMPLETE / Gate Eligible: NO`.
3. No filename date or modification time participates in selection.

**Assertions:**

- [ ] TQA-C02-A: Exact path and hash win over mtime.
- [ ] TQA-C02-B: Wrong-build evidence is rejected as stale/mismatched.
- [ ] TQA-C02-C: A changed build requires a new QA run ID.

---

### Case 3: Automated tests not run or stale cannot pass

**Fixture:**

- A started QA run requires automated IDs `AT-001` and `AT-002`.
- Receipt R1 has a zero exit code but omits runner version, per-test results, and
  log/result hashes.
- Receipt R2 is structurally complete for `AT-002` but is bound to the previous
  build hash.
- The regression selection manifest path is present but its recorded hash differs
  from the current `tests/regression-suite.md`.

**Input:**

Ingest R1 and R2 with `--automated-receipt`.

**Expected writes:**

- At most immutable evidence records and a versioned evidence index describing the
  rejected/nonconclusive receipts, if those CREATE paths were authorized.

**Expected non-writes:**

- No PASS rewrite, fabricated runner receipt, source-receipt edit, or signoff.

**Expected behavior:**

1. R1 becomes `INVALID`, not PASS.
2. R2 becomes `STALE`, not PASS.
3. Uncovered required rows remain `NOT_RUN`.
4. Returns `Workflow Status: RUNNING`, `QA Verdict: INCOMPLETE`, and
   `Gate Eligible: NO`.
5. Names the missing receipt fields and changed selection-manifest hash.

**Assertions:**

- [ ] TQA-C03-A: Exit code alone is not execution evidence.
- [ ] TQA-C03-B: Old-build and changed-selection evidence cannot be current PASS.
- [ ] TQA-C03-C: All required automated IDs remain in denominator counts.

---

### Case 4: Chat PASS is not manual evidence

**Fixture:**

- Manual case `MC-017` requires three steps and a screenshot/log attachment.
- The user says "PASS" in chat and describes the feature as looking correct.
- No record contains tester ID, device/OS/input, timestamps, per-step actuals,
  attestation, attachment path, or hash.

**Input:**

`$team-qa ingest tqa-run-004 --manual-evidence conversation-summary.md`

**Expected writes:**

- None, or an authorized immutable rejection record that remains
  `Evidence Eligible: NO`.

**Expected non-writes:**

- No synthesized manual PASS receipt, no edited case status, no signoff, no bug.

**Expected behavior:**

1. Treats the chat selection as non-evidence.
2. Classifies `MC-017` as `INVALID` or `UNKNOWN` and preserves it in the required
   denominator.
3. Returns `RUNNING / INCOMPLETE / Gate Eligible: NO`.
4. Requests a canonical record with tester, environment, every step's actual
   result, timestamps, attestation, and attachment hashes.

**Assertions:**

- [ ] TQA-C04-A: User self-report alone cannot establish PASS.
- [ ] TQA-C04-B: qa-tester transcription cannot invent missing provenance.
- [ ] TQA-C04-C: Manual evidence fields are checked individually.

---

### Case 5: BLOCKED and NOT_RUN rows prevent approval

**Fixture:**

- The plan declares ten required rows.
- One hash-bound approval receipt excludes one row, leaving required denominator
  nine.
- Seven rows PASS, one is BLOCKED, and one is NOT_RUN.
- The evidence-review report is COMPLETE but its execution status is UNKNOWN and
  closure eligibility is NO.

**Input:**

`$team-qa finalize tqa-run-005 --evidence-review production/qa/evidence/reviews/rev-005/report.md`

**Expected writes:**

- An authorized immutable `signoff.md` may be created with
  `QA Verdict: INCOMPLETE` and `Gate Eligible: NO`.

**Expected non-writes:**

- No change to plan, receipts, exclusion approval, evidence review, or bugs.

**Expected behavior:**

1. Shows declared 10, excluded 1, required 9, pass 7, blocked 1, not-run 1.
2. Does not omit the blocked/not-run rows or count the exclusion without verifying
   its scope/plan/candidate hashes.
3. Returns `Workflow Status: COMPLETE` and `QA Verdict: INCOMPLETE` as separate
   axes.
4. Does not recommend a downstream gate.

**Assertions:**

- [ ] TQA-C05-A: Required BLOCKED/NOT_RUN rows are never approval-neutral.
- [ ] TQA-C05-B: COMPLETE review/workflow text does not imply PASS.
- [ ] TQA-C05-C: Denominator arithmetic is explicit and consistent.

---

### Case 6: Parallel failure findings do not collide on bug IDs

**Fixture:**

- Two qa-tester tasks independently find failures for `MC-020` and `MC-021` at
  nearly the same time.
- The canonical bug directory's highest current numeric ID is `BUG-042`.
- Neither finding has an existing matching fingerprint.

**Input:**

Ingest both valid current failure receipts, then request finalize.

**Expected writes:**

- Distinct immutable evidence/finding records and evidence-index entries using
  occurrence IDs derived from run ID, test/case ID, and evidence hash.
- A `NOT_APPROVED` signoff may be written after evidence review.

**Expected non-writes:**

- No `BUG-043.md` or any other `production/qa/bugs/**` file.
- No bug-number reservation file and no scan/increment operation.

**Expected behavior:**

1. Produces two distinct `TQA-OCC-...` IDs and normalized fingerprints.
2. Sends both candidates to one serialized `bug-report` owner.
3. Keeps `Gate Eligible: NO` until canonical bug receipts or approved dispositions
   exist.
4. Never lets parallel qa-testers allocate canonical bug IDs.

**Assertions:**

- [ ] TQA-C06-A: Occurrence IDs are collision-resistant and distinct.
- [ ] TQA-C06-B: Team QA has no canonical bug-file write ownership.
- [ ] TQA-C06-C: The single-owner handoff eliminates the read-max/increment race.

---

### Case 7: Failure precedence preserves simultaneous evidence gaps

**Fixture:**

- One valid current automated receipt is FAIL.
- One required manual row is NOT_RUN.
- One required soak row is INCONCLUSIVE.
- The exact evidence-review report evaluates the whole declared scope but reports
  Overall Execution Status FAIL and Closure Eligible NO.

**Input:**

Finalize the run with the exact review report.

**Expected writes:**

- Authorized immutable signoff with `Workflow Status: COMPLETE`,
  `QA Verdict: NOT_APPROVED`, and `Gate Eligible: NO`.

**Expected non-writes:**

- No relabeling of NOT_RUN or INCONCLUSIVE; no downstream gate artifact.

**Expected behavior:**

1. Applies current failure precedence and returns NOT_APPROVED.
2. Separately lists the manual NOT_RUN and soak INCONCLUSIVE rows.
3. Creates a collision-resistant occurrence for the failure and requires its bug
   handoff/disposition.
4. Reports exact counts without erasing incomplete evidence.

**Assertions:**

- [ ] TQA-C07-A: Failure precedence is deterministic.
- [ ] TQA-C07-B: Incomplete rows remain visible under NOT_APPROVED.
- [ ] TQA-C07-C: Gate eligibility remains NO.

---

### Case 8: Canonical playtest and soak labels are interpreted semantically

**Fixture:**

- Playtest P1 is canonical and says `Status: COMPLETED` but
  `Gate Eligible: NO`.
- Soak S1 is canonical and says `Verdict: COMPLETE` but
  `Readiness Result: INCONCLUSIVE` and Memory dimension `INCOMPLETE`.
- Both otherwise match the candidate.

**Input:**

Ingest P1 and S1.

**Expected writes:**

- Optional authorized immutable evidence records reflecting their exact
  nonconclusive statuses.

**Expected non-writes:**

- No PASS normalization and no APPROVED signoff.

**Expected behavior:**

1. Rejects P1 for required-row closure because its gate flag is NO.
2. Rejects S1 for readiness because INCONCLUSIVE/INCOMPLETE is not PASS.
3. Returns `RUNNING / INCOMPLETE / Gate Eligible: NO`.
4. Explains that completion/finalization labels are independent of QA success.

**Assertions:**

- [ ] TQA-C08-A: Playtest COMPLETED alone is not PASS.
- [ ] TQA-C08-B: Soak COMPLETE alone is not readiness PASS.
- [ ] TQA-C08-C: Dimension and provenance hashes remain mandatory.

---

### Case 9: Fully verified exact-candidate run is approved

**Fixture:**

- Exact candidate manifest, current QA plan, and persisted sprint-mode smoke
  receipt all match and re-hash.
- Every required automated/manual/playtest/soak row has structurally valid,
  current, exact-candidate PASS evidence.
- No unapproved exclusion, warning, finding, condition, or gap exists.
- The frozen evidence index is current.
- The exact evidence-review report has artifact type/schema, candidate/index
  binding, `Workflow Status: COMPLETE`, `Overall Evidence Quality: ADEQUATE`,
  `Overall Execution Status: PASS`, `Execution Scope: FULL`, and
  `Closure Eligible: YES`.
- The authorized signoff path does not exist.

**Input:**

`$team-qa finalize tqa-run-009 --evidence-review production/qa/evidence/reviews/rev-009/report.md`

**Expected writes:**

- Exactly `production/qa/team-runs/tqa-run-009/signoff.md`, transactionally,
  followed by byte re-read and SHA-256 verification.

**Expected non-writes:**

- No source evidence edits, bugs, session state, review-mode, catalog, guide, or
  director-gate file.

**Expected behavior:**

1. Re-hashes the entire frozen evidence graph immediately before signoff.
2. Reports denominator totals with every required row PASS.
3. Writes a signoff with `Workflow Status: COMPLETE`,
   `QA Verdict: APPROVED`, `Gate Eligible: YES`, and
   `Persistence: VERIFIED`.
4. Reports the canonical signoff path and verified SHA-256.

**Assertions:**

- [ ] TQA-C09-A: APPROVED requires every closure condition simultaneously.
- [ ] TQA-C09-B: Gate Eligible becomes YES only after verified signoff persistence.
- [ ] TQA-C09-C: No unrelated or external-owner artifact is written.

---

## Cross-skill compatibility assertions

- [ ] TQA-X001: QA-plan currentness and stable ID rules match staged `qa-plan`.
- [ ] TQA-X002: Smoke path, receipt identity, sprint PASS, and handoff rules match
  staged `smoke-check`.
- [ ] TQA-X003: Regression selection manifest and runtime receipt distinction
  match staged `regression-suite`.
- [ ] TQA-X004: Evidence-review dual axes and closure rule match staged
  `test-evidence-review`.
- [ ] TQA-X005: Canonical playtest result path and required fields match staged
  `playtest-report`.
- [ ] TQA-X006: Canonical soak result path plus execution/readiness/dimension
  semantics match staged `soak-test`.
