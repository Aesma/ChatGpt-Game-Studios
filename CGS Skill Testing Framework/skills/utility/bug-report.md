# Skill Test Spec: `$bug-report`

## Skill Summary

`$bug-report` creates and updates versioned canonical bug records under
`production/qa/bugs/<BUG-ID>.md`. Canonical severity is
`S1-Critical/S2-Major/S3-Minor/S4-Trivial`. The only legal forward lifecycle is
`Open → Fixed Pending Verification → Verified Fixed → Closed`, with an evidence
owner and immutable transition history for every status change.

Static source inspection is never runtime verification. `VERIFIED FIXED` requires a
target-build reproduction receipt plus a passing, failure-sensitive automated
regression-test receipt for the fix revision. `CLOSED` consumes that current
verification evidence; manual evidence cannot replace the regression gate.

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only `name` and non-empty `description`; name matches
      the skill directory
- [ ] Has at least two phase headings
- [ ] Uses only `production/qa/bugs/<BUG-ID>.md` as the canonical record path
- [ ] Never uses `production/bugs/` as a canonical or fallback registry
- [ ] Defines `Schema Version: 1` and stable IDs matching `BUG-[0-9]{4,}`
- [ ] Uses only `S1-Critical`, `S2-Major`, `S3-Minor`, and `S4-Trivial` for
      canonical severity; legacy text severity is not silently converted
- [ ] Keeps severity separate from priority and scheduling ownership
- [ ] Defines the states `Open`, `Fixed Pending Verification`,
      `Verified Fixed`, and `Closed`
- [ ] Defines owner, evidence preconditions, field patch, and history record for every
      legal transition
- [ ] Rejects direct `Open → Verified Fixed`, `Open → Closed`, and
      `Fixed Pending Verification → Closed`
- [ ] Static-only inspection returns `FIX PRESENT / RUNTIME UNVERIFIED` (or
      `FIX NOT FOUND / RUNTIME UNVERIFIED`) and cannot update status
- [ ] `VERIFIED FIXED` requires build ID, fix commit, platform, repro case ID,
      runner/manual observer, timestamp, observed result, evidence path, and SHA-256
- [ ] `VERIFIED FIXED` also requires an automated regression test ID/path and passing
      receipt bound to the fix commit
- [ ] Close rejects `Manual verification` as the regression test
- [ ] This workflow does not assign priority/schedule, accept risk, or edit triage,
      sprint, hotfix, release, or test-plan records

---

## Case 1: New crash report uses the canonical path and severity

**Fixture:**

- The project bug-ID allocator supplies `BUG-0042`.
- No canonical record with that ID exists.

**Input:** A complete description of a reproducible crash on build `build-77`.

**Expected behavior:**

1. The proposed record has `Schema Version: 1`, `ID: BUG-0042`,
   `Severity: S1-Critical`, and `Status: Open`.
2. The body and filename use the same stable ID.
3. The only destination is `production/qa/bugs/BUG-0042.md`.
4. The workflow previews the complete changeset and writes only after bounded
   authorization.

**Assertions:**

- [ ] No `production/bugs/` path is read or proposed
- [ ] No textual `CRITICAL` severity is written
- [ ] Priority is not automatically derived from S1 severity
- [ ] Initial transition history records creation at `Open`

---

## Case 2: Legacy location or severity is not silently canonicalized

**Fixture:**

- `production/bugs/bug-2026-03-20-audio-cut-out.md` exists with
  `Severity: MEDIUM`.
- No matching canonical file exists under `production/qa/bugs/`.

**Input:** `$bug-report verify BUG-0042`

**Expected behavior:**

- The workflow does not load the legacy file as the requested bug.
- It stops without a verification verdict or mutation, names the expected canonical
  path, and says a separately approved migration is required.
- It does not translate `MEDIUM` to an S-value.

**Assertions:**

- [ ] No fallback registry is used
- [ ] No legacy file is rewritten
- [ ] No `VERIFIED FIXED` or `CLOSED` status is produced

---

## Case 3: Static fix inspection cannot verify a bug

**Fixture:**

- `BUG-0042` is `Fixed Pending Verification`.
- A source diff removes the suspected code pattern.
- No target-build reproduction receipt or regression receipt exists.

**Input:** `$bug-report verify BUG-0042`

**Expected behavior:**

- Static result is `FIX PRESENT / RUNTIME UNVERIFIED`.
- Operation verdict is `CANNOT VERIFY`.
- Status remains `Fixed Pending Verification` and no history event is appended.

**Assertions:**

- [ ] Source search is not described as re-running reproduction steps
- [ ] The missing runtime and regression receipts are listed
- [ ] No file mutation is proposed

---

## Case 4: Matching runtime and regression evidence verifies the fix

**Fixture:**

- `BUG-0042` is `Fixed Pending Verification` and references fix commit `abc123`,
  build `build-78`, platform `Windows-x64`, repro case `REPRO-0042`, and regression
  test `test_inventory_drop_preserves_item`.
- The reproduction receipt records those same values, QA runner identity, UTC
  timestamps, every step, the expected and observed result, `PASS`, an evidence
  path, and a matching raw-byte SHA-256.
- The automated regression receipt is from `abc123`, records the test ID/path,
  invocation, completion time, exit code 0, `PASS`, a failure-sensitive assertion,
  log path, and matching raw-byte SHA-256.

**Input:** `$bug-report verify BUG-0042`

**Expected behavior:**

1. Both receipts are validated against the canonical fix reference.
2. Verdict is `VERIFIED FIXED`.
3. One proposed edit changes the top-level status to `Verified Fixed`, stores the
   receipts, and appends the matching transition event.
4. The event identifies the QA verifier, UTC timestamp, reason, both receipt hashes,
   and bug-record preimage SHA-256.

**Assertions:**

- [ ] Status patch and history append are one proposed mutation
- [ ] Evidence is build-, platform-, repro-, and commit-bound
- [ ] The workflow does not claim any triage or sprint change

---

## Case 5: A failing target-build check returns the bug to Open

**Fixture:**

- `BUG-0042` is `Fixed Pending Verification`.
- Its matching target-build reproduction receipt is `FAIL` and captures the observed
  original defect.

**Input:** `$bug-report verify BUG-0042`

**Expected behavior:**

- Verdict is `STILL PRESENT`.
- The proposed atomic edit sets `Status: Open`, retains the failure receipt, and
  appends `Fixed Pending Verification → Open` with the QA verifier as owner.
- No verified or closed state is written.

**Assertions:**

- [ ] Failing evidence is preserved with its hash
- [ ] The record is never sent directly to `Closed`
- [ ] The workflow may suggest `$hotfix` but does not invoke it

---

## Case 6: Stale, mismatched, or runner-error evidence cannot verify

**Variants:**

- A: reproduction receipt is for an older build;
- B: receipt platform differs from the canonical fix reference;
- C: regression log is unreadable or its SHA-256 mismatches;
- D: runtime outcome is `RUNNER_ERROR`;
- E: regression receipt is for a different commit.

**Expected behavior:**

- Every variant returns `CANNOT VERIFY`.
- Status remains `Fixed Pending Verification`.
- The exact invalid or missing field is reported.

**Assertions:**

- [ ] No evidence is inferred from source state
- [ ] No partial evidence produces `VERIFIED FIXED`
- [ ] No file mutation is proposed

---

## Case 7: Manual verification cannot replace a regression test

**Fixture:**

- `BUG-0042` is `Verified Fixed`.
- A valid manual-observer target-build reproduction receipt exists.
- The closure proposal says `Regression test: Manual verification` and has no
  automated regression receipt.

**Input:** `$bug-report close BUG-0042`

**Expected behavior:**

- Close is blocked with the canonical message requiring a current target-build
  verification and passing automated regression-test receipt.
- Status remains `Verified Fixed`.
- No closure record or history event is appended.

**Assertions:**

- [ ] Manual runtime evidence may support reproduction only
- [ ] No waiver is invented; the repository test policy grants none
- [ ] No file mutation is proposed

---

## Case 8: Close consumes current verified evidence

**Fixture:**

- `BUG-0042` is `Verified Fixed`.
- Its verification history references readable, hash-matching passing reproduction
  and automated regression receipts for the current fix commit.
- An authorized QA closure owner and authority reference are provided.

**Input:** `$bug-report close BUG-0042`

**Expected behavior:**

1. Close revalidates both receipt hashes and their fix/build/test bindings.
2. One proposed edit changes the top-level status to `Closed`, appends the closure
   record, and appends `Verified Fixed → Closed`.
3. The closure record contains fix reference, build receipt, verifier, closure owner
   and authority, automated regression test ID/path, and regression receipt hash.

**Assertions:**

- [ ] No `Manual verification` regression value appears
- [ ] Closure owner is explicit and not granted by the workflow
- [ ] Triage output is not edited; a fresh `$bug-triage` run may only be suggested

---

## Case 9: Illegal transitions are rejected

**Variants:**

- A: Verify Mode is asked to verify an `Open` record.
- B: Close Mode is asked to close an `Open` record.
- C: Close Mode is asked to close `Fixed Pending Verification`.
- D: Any mode is asked to transition a `Closed` record.

**Expected behavior:**

- Each variant stops with the required current state and owner/evidence precondition.
- No top-level status or history is changed.

**Assertions:**

- [ ] Verify Mode never creates `Open → Fixed Pending Verification`
- [ ] `Open → Verified Fixed` and `Open → Closed` never occur
- [ ] `Fixed Pending Verification → Closed` never occurs
- [ ] Closed records remain immutable

---

## Case 10: Existing required-field follow-up behavior remains in force

**Fixture:**

- The description omits reproduction steps, actual result, and build/version.

**Input:** A short bug description.

**Expected behavior:**

- The workflow asks follow-up questions for the missing report information before
  finalizing the draft.
- No canonical report is written with unresolved required report fields.

**Assertions:**

- [ ] Reproduction steps, actual result, and build/version are requested
- [ ] A proposed path is not treated as a completed canonical record
- [ ] Changeset authorization still occurs only once before the first write

---

## Case 11: Existing duplicate-candidate choice remains advisory

**Fixture:**

- A similar canonical report already exists in `production/qa/bugs/`.

**Input:** A description that appears to describe the same defect.

**Expected behavior:**

- The existing canonical record is surfaced as a possible duplicate.
- The user chooses whether to link or create a separate record.
- No record is silently merged, closed, or overwritten.

**Assertions:**

- [ ] Duplicate detection reads only the canonical registry
- [ ] The stable existing bug ID and path are shown
- [ ] User choice precedes any proposed mutation

---

## Director Gate Checks

None. Bug-report mutations use the one complete changeset authorization and the
transition-owner evidence gates defined above; no director gate is introduced.

## Protocol Compliance

- [ ] Canonical path, schema, ID, severity, and status are consistent across every mode
- [ ] Static inspection is always distinguished from target-build reproduction
- [ ] Verify updates both status and immutable history only after both receipts pass
- [ ] Close requires current build verification and an automated regression receipt
- [ ] Manual evidence never substitutes for the repository regression-test policy
- [ ] Priority, scheduling, risk, sprint, triage, hotfix, release, and test-plan
      ownership stay outside this workflow

## Coverage Notes

Cases 1–9 are the P0 remediation gate for BR-001 through BR-004. Cases 10–11 retain
the pre-existing report-completeness and duplicate-choice contract; their broader
workflow redesign is outside this P0 remediation.
