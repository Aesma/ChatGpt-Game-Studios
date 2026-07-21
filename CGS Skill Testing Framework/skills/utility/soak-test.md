# Skill Test Spec: $soak-test

## Skill Summary

`$soak-test` separates immutable test protocols, run manifests, raw evidence
receipts, sample ledgers, and canonical completed results. A saved protocol has
`Status: PLANNED`, `Gate Eligible: NO`, and never proves execution. Only
`production/qa/soak-tests/<run-id>/result.md` may have `Status: COMPLETED`, and only
after target/build/workload/environment identity, observer, termination, samples, and
all hashes validate.

Execution, stability, memory, performance, experience, readiness, artifact completion,
and gate eligibility are independent fields. No director gate applies.

---

## Static Assertions

- [ ] YAML frontmatter contains only `name` and a non-empty `description`; name matches the skill directory
- [ ] Has at least two phase headings
- [ ] Defines plan, start, ingest, finalize, and status modes with invalid-mode handling
- [ ] Uses distinct canonical paths and artifact types for protocol, manifest, receipts/raw/samples, and result
- [ ] A protocol returns PLANNED/PROTOCOL_PLANNED, NOT_STARTED, and Gate Eligible: NO
- [ ] Only a hash-verified canonical result can return Status: COMPLETED and Verdict: COMPLETE; incomplete/inconclusive results are not gate eligible
- [ ] Requires target, build/hash/commit, workload profile, environment profile, observer, duration/interval, and collection adapter identity
- [ ] Every metric threshold cites a project budget or approved matching baseline; missing thresholds force INCONCLUSIVE
- [ ] Contains no hard-coded or transplanted engine-, platform-, or tool-global pass threshold
- [ ] Expands stable checkpoint IDs and treats omitted samples as NOT_COLLECTED, never zero
- [ ] Preserves raw evidence and sample values separately from derived classifications
- [ ] Defines FAILED_EARLY and INCOMPLETE behavior with partial evidence preservation
- [ ] Separates Stability, Memory, Performance, and Experience results
- [ ] Consumes playtest context only from canonical completed, gate-eligible, hash-valid staged playtest-result contracts
- [ ] Uses bounded authorization and all-or-none publication for multi-file ingest
- [ ] Never overwrites a prior protocol, receipt, run, or result
- [ ] No director gates apply

---

## Case 1: Saving a protocol is PLANNED, not executed

**Fixture:**

- Every target/build/workload/environment and observer/adapter field is supplied
- Matching project budgets and threshold policies exist
- The requested bounded change authorizes the protocol path

**Input:** `$soak-test plan combat-loop --protocol-id SOAK-PROTO-combat-v1 --build 0.9.0 --build-hash abc123 --commit def456 --duration 2h --interval 30m --focus all --profile combat-standard --environment pc-minspec --save-protocol`

**Expected behavior:**

1. The skill expands CP-000 through the exact 2h endpoint.
2. It writes only `_protocols/SOAK-PROTO-combat-v1.md`.
3. It returns `Status: PLANNED`, `Execution Status: NOT_STARTED`,
   `Gate Eligible: NO`, and `Verdict: PROTOCOL_PLANNED`.

**Assertions:**

- [ ] No run directory, result, observed value, post-session analysis, completed sign-off, PASS/FAIL, EXECUTED, or COMPLETE is created
- [ ] Protocol identity includes exact build, workload, environment, adapter, target, duration, and thresholds
- [ ] Re-reading the protocol produces a SHA-256 receipt

---

## Case 2: Missing target identity blocks executable protocol

**Variants:**

- Missing build hash/source commit
- Missing system/scene target
- Missing workload steps/player count/seed policy
- Missing platform/device/configuration
- Missing observer or collection-tool identity

**Expected behavior:**

- Each variant returns `BLOCKED`, names all missing identity fields, and writes no
  protocol.
- It never emits an executable, completed, or gate-capable status.

**Assertions:**

- [ ] Placeholders cannot bypass validation
- [ ] No target is inferred from most-recent playtest or QA plan
- [ ] No file is written

---

## Case 3: Missing budget cannot produce a false PASS

**Fixture:**

- Target/build/workload/environment identity is complete
- A memory metric has no project budget and no approved matching baseline
- The full run later supplies every checkpoint sample

**Expected behavior:**

- Protocol records `THRESHOLD_UNAVAILABLE`, `Threshold Readiness: INCOMPLETE`, and
  `Gate Capable: NO`.
- Finalized `Memory Result: INCONCLUSIVE`, `Readiness Result: INCONCLUSIVE`, and `Gate Eligible: NO`.
- No engine-, platform-, series-shape, or device-class default is substituted.

**Assertions:**

- [ ] Missing threshold is never zero or a default
- [ ] Complete sampling alone cannot create Memory PASS
- [ ] Result explains the missing threshold source

---

## Case 4: Full hash-valid run becomes an EXECUTED completed result

**Fixture:**

- A valid PLANNED protocol and RUNNING manifest identify one build/profile/environment
- Every expected checkpoint and baseline is present in immutable receipt/sample files
- Observer, start/end, `SCHEDULE_COMPLETED`, adapter, thresholds, and confidence rules
  verify
- All required objective metric comparisons pass
- The exact result write is authorized

**Input:** `$soak-test finalize SOAK-RUN-combat-001 --ended-at 2026-07-22T12:00:00Z --termination SCHEDULE_COMPLETED`

**Expected behavior:**

1. The skill re-hashes the protocol, manifest, receipts, raw files, and sample ledgers.
2. It writes only `production/qa/soak-tests/SOAK-RUN-combat-001/result.md`.
3. It re-reads the result before returning `Status: COMPLETED`,
   `Execution Status: EXECUTED`, `Readiness Result: PASS`, `Gate Eligible: YES`, and
   `Verdict: COMPLETE`.

**Assertions:**

- [ ] Completed header includes target/build/commit/workload/environment/observer/time/termination
- [ ] Completion receipt includes protocol, manifest, receipt, raw-set, sample-set, and result hashes
- [ ] COMPLETE is described as artifact finalization, not as an automatic release decision

---

## Case 5: Verified crash preserves samples and returns FAILED_EARLY

**Fixture:**

- A run records valid baseline and early checkpoints
- A raw crash receipt ties a crash event to observer, build, environment, timestamp,
  and source location
- Later scheduled checkpoints were not reached

**Expected behavior:**

- Existing samples remain immutable and referenced.
- Later checkpoints are `NOT_COLLECTED` with `Termination Reason: CRASH`.
- `Execution Status: FAILED_EARLY`, `Stability Result: FAIL`,
  `Readiness Result: FAIL`.
- A structurally complete result may be finalized; it never claims EXECUTED or PASS.

**Assertions:**

- [ ] Early evidence is not discarded
- [ ] Missing later samples are not zeros
- [ ] Bug candidate includes run/sample/receipt/build/environment IDs
- [ ] Smoke success cannot close this endurance failure

---

## Case 6: Missing checkpoints without a verified failure are INCOMPLETE

**Fixture:**

- The operator stops before the end
- No crash, hang, threshold, OOM, thermal, or data-corruption trigger verifies
- Some checkpoint IDs have no samples

**Expected behavior:**

- `Execution Status: INCOMPLETE` and `Gate Eligible: NO`
- Missing checkpoints are `NOT_COLLECTED`
- Required affected dimensions and readiness are `INCONCLUSIVE`
- The skill does not infer values or classify the run PASS

**Assertions:**

- [ ] Termination reason and observer remain required
- [ ] Every expected checkpoint has collected/not-collected status
- [ ] Partial evidence is preserved with hashes

---

## Case 7: Experience and technical results cannot overwrite each other

**Variants:**

- A: Stability/memory/performance pass, but experience fatigue evidence fails
- B: Experience passes, but memory threshold fails
- C: Experience is not in scope

**Expected behavior:**

- A preserves technical PASS values and `Experience Result: FAIL`.
- B preserves `Memory Result: FAIL` and does not promote readiness.
- C uses `Experience Result: NOT_IN_SCOPE`.
- Readiness follows only the named gate policy.

**Assertions:**

- [ ] No aggregate sentence rewrites a dimension
- [ ] Experience affects readiness only when explicitly required by policy
- [ ] Technical PASS is not evidence of enjoyable long-session experience

---

## Case 8: Historical extension creates a new immutable version

**Fixture:**

- SOAK-PROTO-combat-v1 already exists for the same target/profile
- The user requests a longer duration and names it with `--supersedes`

**Expected behavior:**

- The skill creates SOAK-PROTO-combat-v2 with predecessor path/hash.
- It never edits v1 or any result produced from v1.
- History is selected by exact target/profile/build IDs, not mtime.

**Assertions:**

- [ ] New protocol ID/path is required
- [ ] Old bytes/hash remain unchanged
- [ ] No date-only collision workaround is used

---

## Case 9: Only canonical completed playtest evidence is accepted

**Variants:**

- A: `production/playtests/PT-fatigue-001/report.md` is a hash-valid
  `playtest-session-result`, `Status: COMPLETED`, `Gate Eligible: YES`
- B: The candidate is a playtest protocol, IN_PROGRESS manifest, legacy report,
  missing-hash report, or director review

**Expected behavior:**

- A may be cited as derived experience context and keeps its report/evidence hashes.
- B is rejected and cannot supply completed experience evidence.
- Neither replaces the soak raw sample/receipt/observer requirements.

**Assertions:**

- [ ] Consumption matches the staged playtest-report completed-result contract
- [ ] Playtest observations and derived report remain distinct
- [ ] No “most recent playtest” fallback exists

---

## Case 10: Unverified engine adapter cannot create gate-capable metrics

**Fixture:**

- The target uses an unknown engine version or lacks a matching collection adapter

**Expected behavior:**

- Required metric guidance is `NEEDS_CONFIRMATION`.
- The skill does not insert Godot, Unity, or Unreal instructions from another version.
- No protocol is called executable or gate capable until adapter identity verifies.

**Assertions:**

- [ ] Only configured engine/version guidance is loaded
- [ ] Adapter path/hash/version is required
- [ ] No fixed engine heuristic appears

---

## Director Gate Checks

None. `$soak-test` is an evidence collection and finalization utility.

## Protocol Compliance

- [ ] Explicit bounded authorization covers all in-scope writes; otherwise one complete preview/approval precedes the first write
- [ ] Protocol, run, receipt/raw/sample, and result artifacts never overwrite each other
- [ ] Multi-file receipt ingest publishes all or none
- [ ] Finalization revalidates all hashes and writes only the canonical result
- [ ] Every mode returns exactly one mode-appropriate verdict
- [ ] Downstream actions are candidates only and are never invoked automatically

## Coverage Notes

These cases close the three P0 failures: protocol/result confusion, missing
system/build/workload/environment identity, and unsupported fixed thresholds. They
also cover required adjacent behavior: early termination, missing checkpoints,
dimension separation, immutable history, engine adapter routing, and exact
compatibility with the staged canonical playtest result/evidence layering.
