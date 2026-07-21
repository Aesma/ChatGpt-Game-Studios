# Skill Test Spec: $milestone-review

## Skill Summary

`$milestone-review` resolves one stable milestone ID, verifies a hashed evidence
manifest, computes only source-backed metrics, optionally runs the read-only
PR-MILESTONE producer gate in full mode, and writes an immutable report after bounded
authorization. Objective readiness and the user's governance decision are always
separate.

The authoritative report statuses are `delivery_status`, `quality_status`,
`risk_status`, `evidence_status`, `evidence_verdict`, `user_decision`, and
`artifact_write_status`. Saving a report does not imply milestone readiness.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only required `name` and non-empty `description`; name matches the skill directory
- [ ] Has at least two phase headings
- [ ] Never resolves `current` by mtime, creation time, filename sort, or a guessed milestone
- [ ] Defines stable `current` resolution from explicit active-milestone fields and blocks missing, duplicate, or conflicting declarations
- [ ] Requires a milestone evidence manifest with tracker, exact sprint reports, bug registry, test results, performance reports, risk register, repository revision, revisions, build/scope, and SHA-256 values
- [ ] Missing, invalid, stale, or conflicting required evidence becomes `UNKNOWN`/`PARTIAL` and forbids `GO`
- [ ] Every numeric metric requires a source, formula, operands, unit, and confidence; `UNKNOWN` is never converted to zero
- [ ] Separates objective status fields from `user_decision` and explicitly forbids risk acceptance from rewriting them
- [ ] Scope recommendations remain undecided candidates with player/pillar and dependency impact
- [ ] Full-mode producer review is read-only and bound to `evidence_draft_sha256`; lean and solo modes skip it explicitly
- [ ] Uses an immutable run-ID report path, source snapshot hash, pre-write source revalidation, and no-overwrite rule
- [ ] Uses existing bounded task authorization or previews and confirms the complete changeset once before the first write
- [ ] Final response reports every independent status and does not equate write success with readiness

---

## Case 1: Complete, current evidence produces GO

**Fixture:**

- `production/session-state/active.md` declares exactly
  `Active Milestone ID: milestone-03`
- `production/milestones/index.md` declares the same active ID
- `production/milestones/milestone-03.md` exists and enumerates its required success
  criteria, scope, sprint IDs, target build, and quality thresholds
- `production/milestones/evidence/milestone-03.yaml` contains every required source
  with correct revisions and SHA-256 values
- Tracker mappings, all sprint reports, bug registry, test results, performance
  reports, risk register, build IDs, and repository revision verify
- Required scope and criteria are complete and every quality threshold passes
- Review mode is `full`; PR-MILESTONE returns `ON TRACK` bound to the draft hash
- The user records `PROCEED` and authorizes the exact report path

**Input:** `$milestone-review current --review full`

**Expected behavior:**

1. The skill resolves `milestone-03` from stable authority fields, never timestamps.
2. It builds a complete evidence ledger and deterministic metrics.
3. It shows the evidence-only draft and hash before the producer gate.
4. The producer is read-only and reviews the exact hashed draft.
5. Objective fields are `delivery_status: COMPLETE`, `quality_status: PASS`,
   `risk_status: ON_TRACK`, `evidence_status: COMPLETE`, and
   `evidence_verdict: GO`.
6. `user_decision: PROCEED` remains a separate record.
7. On authorization and unchanged-source verification, the skill writes
   `production/milestones/reviews/milestone-03/<run-id>.md`.

**Assertions:**

- [ ] Every metric shows source revision/hash, formula, operands, unit, and result
- [ ] Source snapshot and evidence-draft hashes appear in the report
- [ ] The report path contains UTC timestamp plus the source-snapshot hash prefix
- [ ] Saved report SHA-256 is displayed after the write
- [ ] `artifact_write_status: COMPLETE` is not described as milestone readiness

---

## Case 2: Missing bug, test, and performance evidence forbids GO

**Fixture:**

- The stable milestone resolves and tracker/sprint evidence is verified
- Bug registry is missing, test results are empty, and the performance report hash
  does not match the evidence manifest
- Other progress data suggests all features are complete
- The user says they accept the uncertainty

**Input:** `$milestone-review milestone-03`

**Expected behavior:**

1. Bug counts, test coverage, and performance results are `UNKNOWN`.
2. The ledger records `MISSING`, `EMPTY`, and `HASH_MISMATCH` with paths and reasons.
3. `evidence_status: PARTIAL`, `quality_status: UNKNOWN`, and
   `evidence_verdict: PARTIAL`.
4. If recorded, the user choice is `PROCEED_WITH_ACCEPTED_RISK`; it does not change
   any objective field.

**Assertions:**

- [ ] No missing value is inferred, copied from memory, or rendered as zero
- [ ] The output never contains `evidence_verdict: GO`
- [ ] Accepted risk lists stable gap IDs and explicitly says it is not readiness evidence
- [ ] A partial report may be written only after exact bounded authorization

---

## Case 3: Newest mtime conflicts with stable active milestone

**Fixture:**

- `milestone-99.md` has the newest modification time
- `production/session-state/active.md` and `production/milestones/index.md` both
  declare `milestone-03`
- `milestone-03.md` exists

**Input:** `$milestone-review current`

**Expected behavior:**

- The skill reviews `milestone-03`.
- It ignores `milestone-99.md` timestamps completely.

**Assertions:**

- [ ] Resolved ID is `milestone-03`
- [ ] Resolution evidence names the stable authority files
- [ ] No mtime-based fallback occurs

---

## Case 4: Conflicting or missing active ID blocks before evidence loading

**Variants:**

- A: session state declares `milestone-03`, while milestone index declares
  `milestone-04`
- B: neither authority file declares an active milestone ID
- C: one authority file declares two active milestone IDs

**Input:** `$milestone-review current`

**Expected behavior:**

- Each variant returns `artifact_write_status: BLOCKED`.
- The skill lists the authority paths and the missing, duplicate, or conflicting
  values.
- It invokes no producer gate and writes no file.

**Assertions:**

- [ ] The skill never chooses an ID heuristically
- [ ] No evidence or objective GO verdict is emitted
- [ ] No source artifact changes

---

## Case 5: Producer AT_RISK cannot be promoted by user choice

**Fixture:**

- All required evidence is complete/current; delivery and quality pass
- Full-mode PR-MILESTONE returns `AT_RISK` with sourced mitigations and the exact
  evidence-draft hash
- The user chooses to proceed and accepts the listed risks

**Input:** `$milestone-review milestone-03 --review full`

**Expected behavior:**

- `risk_status: AT_RISK`
- `evidence_verdict: CONDITIONAL_GO`
- `user_decision: PROCEED_WITH_ACCEPTED_RISK`
- The report never relabels the result as `GO` or `ON_TRACK`

**Assertions:**

- [ ] Producer result remains verbatim and hash-bound
- [ ] User risk acceptance has decision maker, timestamp, rationale, risk IDs, owners, and deadlines
- [ ] No option offers “override to GO” or “frame as GO”
- [ ] Risk acceptance does not alter objective fields

---

## Case 6: Producer OFF_TRACK and report write success remain independent

**Fixture:**

- Evidence is complete/current, but PR-MILESTONE returns `OFF_TRACK`
- The user records `PROCEED_WITH_ACCEPTED_RISK`
- The user authorizes the exact immutable report path and the write succeeds

**Expected behavior:**

- `risk_status: OFF_TRACK`
- `evidence_verdict: NO_GO`
- `user_decision: PROCEED_WITH_ACCEPTED_RISK`
- `artifact_write_status: COMPLETE`

**Assertions:**

- [ ] `NO_GO` remains unchanged after the user decision
- [ ] Write success is not presented as milestone completion or readiness
- [ ] The immutable report contains the objective verdict and separate decision record

---

## Case 7: Producer failure produces PARTIAL, not GO

**Fixture:**

- Review mode is `full`
- Evidence-only draft and sources are otherwise complete
- Producer times out, returns malformed output, or returns a verdict for a different
  draft hash

**Expected behavior:**

- `risk_status: UNKNOWN`
- `evidence_verdict: PARTIAL`
- The exact draft, error evidence, and hash mismatch or timeout reason are preserved
- The skill does not silently rerun against changed inputs

**Assertions:**

- [ ] No `GO` is emitted
- [ ] Producer failure is visible in the report/final status
- [ ] No file is written without bounded authorization

---

## Case 8: Source changes between approval and write

**Fixture:**

- The user approves a report at a specific immutable path
- A required source hash changes before the first write

**Expected behavior:**

- The skill discards the stale candidate report and returns to evidence verification.
- It derives new hashes and a new run ID/path, then previews that new changeset before
  requesting authorization.
- It never writes the previously approved stale report.

**Assertions:**

- [ ] All sources are re-hashed immediately before write
- [ ] Approval for one path/content is not reused for changed bytes
- [ ] Existing reports are never overwritten

---

## Protocol Compliance

- [ ] Review mode is resolved exactly once
- [ ] Evidence-only draft is shown before PR-MILESTONE
- [ ] PR-MILESTONE runs only in full mode and cannot write
- [ ] Lean and solo output exact skip notes
- [ ] Scope candidates are not decisions
- [ ] Missing/partial evidence cannot result in GO
- [ ] User acceptance never changes objective readiness
- [ ] Final output includes report path/hash or `null` and every independent status

## Coverage Notes

These cases intentionally test the three P0 failure modes: unsupported quality
metrics, timestamp-based milestone selection, and risk acceptance masquerading as
objective readiness. They also cover the minimum adjacent contracts required to make
those fixes testable: deterministic formulas, immutable reports, draft/source hashes,
producer failure, and pre-write revalidation.
