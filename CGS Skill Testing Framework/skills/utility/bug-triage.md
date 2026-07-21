# Skill Test Spec: $bug-triage

## Skill Summary

`$bug-triage` reads unresolved canonical bug records from
`production/qa/bugs/*.md` and returns an evidence-backed conversational snapshot. It
uses `S1-Critical`, `S2-Major`, `S3-Minor`, and `S4-Trivial`, keeps observed severity
separate from priority and schedule recommendations, and performs no writes.

Assignments are always `PROPOSED` or `UNASSIGNED`. `DEFERRED`,
`WONT_FIX_CANDIDATE`, and `ACCEPTED_RISK` have different meanings, and accepted risk
requires a complete product-owner waiver plus a canonical recorder transaction.
There are no director gates.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only required `name` and non-empty `description`; name matches the skill directory
- [ ] Has at least two phase headings
- [ ] Contains `TRIAGED`, `PARTIAL_TRIAGE`, and `READ_ONLY_NO_CHANGES`
- [ ] Uses only `production/qa/bugs/*.md` as the canonical bug registry
- [ ] Uses canonical S1–S4 severity values and does not silently convert textual legacy severity
- [ ] Keeps severity evidence, priority recommendation, disposition, and scheduling proposal separate
- [ ] Every schedule result is explicitly `PROPOSED` or `UNASSIGNED`
- [ ] Defines an atomic recorder handoff that updates canonical bug and sprint/capacity records under one transaction ID
- [ ] Separates `DEFERRED`, `WONT_FIX_CANDIDATE`, and validated `ACCEPTED_RISK`
- [ ] Requires owner, scope, reason, timestamp, expiry/review date, and transaction ID for accepted risk
- [ ] Partial canonical reads force `PARTIAL_TRIAGE` and `backlog_health: UNKNOWN`
- [ ] Resolves active sprint only from stable explicit IDs, never mtime
- [ ] Flags missing reproduction evidence and possible duplicates without mutating records
- [ ] Remains read-only; no changeset authorization prompt or report write appears
- [ ] No director gates apply

---

## Case 1: Complete canonical backlog produces a read-only snapshot

**Fixture:**

- `production/qa/bugs/` contains five valid canonical records:
  - `BUG-0001`, `S1-Critical`, `Open`
  - `BUG-0002`, `S2-Major`, `Open`
  - `BUG-0003`, `S3-Minor`, `Reopened`
  - `BUG-0004`, `S4-Trivial`, `Open`
  - `BUG-0005`, `S2-Major`, `Closed`
- Each record has title, reported timestamp, system, build, platform, numbered repro
  steps, expected result, and actual result

**Input:** `$bug-triage full`

**Expected behavior:**

1. All five files are loaded and hashed; four unresolved bugs are analyzed.
2. The output sorts unresolved rows S1 through S4 and then by age/ID.
3. Observed severity/status and priority recommendation remain separate.
4. `operation_status: TRIAGED`, `mutation_status: READ_ONLY_NO_CHANGES`.
5. No report or registry file is written.

**Assertions:**

- [ ] Load counters show five loaded, four unresolved, one closed, and zero failed
- [ ] Snapshot SHA-256 and source hashes are present
- [ ] Triage table contains exactly four unresolved rows
- [ ] No language claims that any proposal was applied

---

## Case 2: Scheduling proposals do not create assignments

**Fixture:**

- `BUG-0010` is open with a verified two-point estimate
- Stable authority files agree on `active_sprint_id: sprint-06`
- Sprint plan and `production/sprint-status.yaml` hashes agree
- Capacity uses points and has four points remaining

**Input:** `$bug-triage sprint`

**Expected behavior:**

- The row may contain `assignment_proposal: PROPOSED:sprint-06`.
- The canonical bug record, sprint plan, sprint-status file, and filesystem are
  unchanged.
- Output includes a recorder transaction request only if the user asks to apply it.

**Assertions:**

- [ ] Output never uses a bare “Assigned to” or claims sprint-06 was updated
- [ ] `assignment_state: PROPOSALS_ONLY`
- [ ] Recorder request contains snapshot/preimage hashes, capacity delta, both registry sides, and all-or-nothing semantics
- [ ] No transaction ID is claimed committed before a recorder succeeds

---

## Case 3: One-sided prior assignment is not trusted

**Fixture:**

- A bug record claims `Sprint: sprint-06` with transaction `TX-10`
- The sprint plan and sprint-status capacity do not reference `TX-10`

**Expected behavior:**

- The skill flags `INCONSISTENT_TRANSACTION`.
- `operation_status: PARTIAL_TRIAGE`, `backlog_health: UNKNOWN`.
- The derived snapshot does not repair or ratify the assignment.

**Assertions:**

- [ ] Report text never treats the bug as canonically assigned
- [ ] Both canonical sides must share one transaction ID and capacity delta
- [ ] No files are modified

---

## Case 4: Deferred, Won't Fix candidate, and accepted risk cannot be conflated

**Variants:**

- A: A low-priority bug is proposed for a later sprint
- B: A product tradeoff suggests the bug may never be fixed, but no decision exists
- C: A record says `Accepted risk` but lacks owner, reason, expiry/review date, and
  transaction ID
- D: A canonical accepted-risk record contains every required waiver field and a
  matching recorder transaction

**Expected behavior:**

- A is `PROPOSED: DEFERRED`, not Won't Fix and not accepted risk.
- B is `WONT_FIX_CANDIDATE`, never a closure or waiver.
- C is `INVALID_ACCEPTED_RISK_CLAIM` plus `NEEDS_PRODUCT_DECISION`.
- Only D is `ACCEPTED_RISK`.

**Assertions:**

- [ ] No user conversational answer alone creates accepted risk
- [ ] Accepted-risk validity requires product owner, scope/bug IDs, reason, timestamp, expiry/review date, and transaction ID
- [ ] No P4 mapping combines Won't Fix, deferred work, and accepted risk

---

## Case 5: Capacity overflow stays unassigned

**Fixture:**

- Stable active sprint has two points remaining
- Two proposed P1 bugs require two points each
- Existing sprint commitments may not be displaced automatically

**Input:** `$bug-triage sprint`

**Expected behavior:**

- At most one bug is `PROPOSED:sprint-06` under a deterministic order.
- The other is `UNASSIGNED_CAPACITY_OVERFLOW` with required and remaining units.
- Neither proposal changes sprint capacity.

**Assertions:**

- [ ] Overflow is never described as assigned
- [ ] Capacity units and arithmetic are shown
- [ ] The sprint owner must decide any scope swap through the recorder transaction

---

## Case 6: Newest sprint file does not override stable active ID

**Fixture:**

- `sprint-99.md` has the newest modification time
- Session state and sprint-status both declare `active_sprint_id: sprint-06`
- The sprint-06 plan exists and matches sprint-status

**Input:** `$bug-triage sprint`

**Expected behavior:**

- `active_sprint_id: sprint-06`
- `sprint-99.md` mtime is ignored

**Assertions:**

- [ ] No most-recent-file fallback occurs
- [ ] Stable authority sources and hashes are shown

---

## Case 7: Partial canonical load cannot yield a healthy conclusion

**Fixture:**

- Four canonical paths are discovered
- Two load successfully
- One is unreadable
- Two loaded records share the same `BUG-0042` ID
- The readable subset contains no S1/S2 bugs

**Expected behavior:**

- Exact discovered, loaded, failed, duplicate, omitted, and unresolved counts appear.
- `operation_status: PARTIAL_TRIAGE`
- `backlog_health: UNKNOWN`
- The skill does not say the build is healthy, ready for QA, or safe to ship.

**Assertions:**

- [ ] Failed and duplicate paths are listed
- [ ] Missing records are not counted as zero
- [ ] No healthy/release-readiness conclusion is emitted

---

## Case 8: Missing repro and duplicate candidates remain advisory

**Fixture:**

- `BUG-0100` lacks numbered steps and actual result
- `BUG-0101` and `BUG-0102` have the same system/severity and normalized title-token
  Jaccard similarity of `0.60`

**Expected behavior:**

- `BUG-0100` is retained and tagged `NEEDS_REPRO_INFO`.
- `BUG-0101` and `BUG-0102` are both retained, tagged `POSSIBLE_DUPLICATE`,
  cross-referenced, and show similarity `0.60`.
- No record is merged, closed, deleted, or rewritten.

**Assertions:**

- [ ] Repro validation checks steps, expected/actual results, build, and platform
- [ ] Duplicate threshold and score are deterministic
- [ ] `mutation_status: READ_ONLY_NO_CHANGES`

---

## Case 9: Snapshot rerun is idempotent and changed input is distinct

**Fixture:**

- Run A and Run B use identical canonical bytes, counters, and sprint context
- Before Run C, one canonical bug byte changes

**Expected behavior:**

- A and B have the same `snapshot_sha256`.
- C has a different hash.
- Any proposal for the old hash is stale and cannot be committed without regeneration.

**Assertions:**

- [ ] Snapshot canonicalization is documented
- [ ] Recorder preimage validation rejects changed inputs
- [ ] No derived snapshot is a source of truth

---

## Case 10: Empty versus missing canonical registry

**Variants:**

- A: `production/qa/bugs/` exists and is empty
- B: `production/qa/bugs/` does not exist

**Expected behavior:**

- A returns `TRIAGED`, `NO_OPEN_BUGS`, and `READ_ONLY_NO_CHANGES`.
- B returns `BLOCKED`, names the expected canonical path, and suggests `$bug-report`.
- Neither variant writes anything.

**Assertions:**

- [ ] Missing registry is not reported as zero bugs
- [ ] Empty verified registry does not produce a table
- [ ] No gate or authorization prompt appears

---

## Director Gate Checks

None. `$bug-triage` is a read-only advisory skill.

## Protocol Compliance

- [ ] Reads the full canonical registry before producing counts
- [ ] Filters by canonical unresolved status
- [ ] Emits exact load/failed/omitted counters and snapshot hash
- [ ] Separates evidence, recommendations, product decisions, and committed transactions
- [ ] Never persists a report or mutates bug/sprint/capacity records
- [ ] Uses `TRIAGED` only as operation completion, not as assignment or readiness proof

## Coverage Notes

The cases cover the three P0 failures: implementation/spec contract drift,
report-only assignments masquerading as canonical schedule, and conflated
deferral/Won't Fix/accepted-risk semantics. They also cover the minimum adjacent
integrity requirements needed for those fixes: full-snapshot partial handling, stable
active sprint selection, capacity units, deterministic duplicate/repro checks, and
transaction preimages.
