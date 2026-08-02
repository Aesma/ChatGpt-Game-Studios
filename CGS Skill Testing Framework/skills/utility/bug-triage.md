# Skill Test Spec: $bug-triage

## Skill Summary

`$bug-triage` reads the canonical backlog under
`production/qa/bugs/`, produces a conversational triage report, and may persist
that same report to `production/qa/bug-triage-[date].md` after one complete
changeset authorization. It does not modify source bug files or sprint plans.

The workflow uses the same literals as `$bug-report`:
S1-Critical / S2-Major / S3-Minor / S4-Trivial and
P1-Immediate / P2-Next Sprint / P3-Backlog / P4-Wishlist.

---

## Static Assertions

- [ ] Reads `production/qa/bugs/`, not `production/bugs/`
- [ ] Uses the shared S1–S4 and P1–P4 literals
- [ ] Optional report persistence is documented and authorized
- [ ] No TRIAGED-only/read-only contract contradicts the implementation
- [ ] Full mode cannot bypass sprint capacity

---

## Case 1: Canonical backlog and report write

**Input:** `$bug-triage sprint`

**Assertions:**

- [ ] Bug reports are read from `production/qa/bugs/`
- [ ] The report is shown in conversation before any write
- [ ] The only possible target is
      `production/qa/bug-triage-[date].md`
- [ ] One authorization is required before persistence
- [ ] Declining leaves the file system unchanged

---

## Case 2: Enumerations match bug-report

**Assertions:**

- [ ] Severity is one of S1-Critical, S2-Major, S3-Minor, S4-Trivial
- [ ] Priority is one of P1-Immediate, P2-Next Sprint, P3-Backlog, P4-Wishlist
- [ ] Sorting and report labels do not introduce CRITICAL/HIGH/MEDIUM/LOW
      as a second enum
- [ ] Existing bug-report values are not silently renamed during triage

---

## Case 3: Full mode respects capacity

**Fixture:** Current sprint has capacity for one comparable bug effort and there
are three P1 bugs.

**Input:** `$bug-triage full`

**Assertions:**

- [ ] At most one P1 is proposed for the current sprint
- [ ] Remaining P1 items are shown as overflow/unassigned
- [ ] P2 next-sprint proposals require known comparable capacity
- [ ] Full mode never says all P1 items are assigned unconditionally
- [ ] Source bug and sprint-plan files remain unchanged

---

## Case 4: No capacity data

**Assertions:**

- [ ] No current- or next-sprint assignment is claimed
- [ ] The report clearly distinguishes a proposed assignment from persisted state
- [ ] Optional report persistence still uses the single approval boundary

---

## Protocol Compliance

- [ ] No director gate is introduced
- [ ] Triage output and optional report contain the same findings
- [ ] Capacity rules apply to sprint and full modes
- [ ] The workflow adds no new directory, status layer, or schema

## P1 Regression Assertions

- [ ] Report rows are proposed placements; source bugs and sprint plans remain unchanged
- [ ] Active sprint comes from an explicit status/marker, never file modification time
- [ ] Only Open bugs are processed; Closed/Verified Fixed are excluded and malformed status is flagged
- [ ] Capacity and effort must use comparable known units before any placement proposal
- [ ] P4 remains a candidate until the user chooses Deferred or Won't Fix
- [ ] Missing trend dates/links are Unknown and excluded from numeric claims
- [ ] Empty repro, possible duplicate, and unknown severity/status appear as data-quality flags
- [ ] Trend mode omits placement recommendations but may save its report
