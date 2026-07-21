# Skill Test Spec: $gate-check

## Skill Summary

`$gate-check` is a read-only assessment of one exact adjacent phase transition. It
validates the authoritative current stage, checks artifacts and quality, requires
hash-bound evidence for blocking prior-result checks, and emits a strict
PASS/CONCERNS/FAIL verdict plus an immutable gate record. It never writes
`production/stage.txt`. Accepted risk is a separate advance request and never changes
the gate verdict.

---

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only required `name` and non-empty `description`
- [ ] Declares all six exact transition IDs and rejects phase-name shorthand
- [ ] Reads and validates `production/stage.txt` before artifact checks
- [ ] Defines PASS, CONCERNS, FAIL, and the non-verdict invocation result ERROR
- [ ] Requires `cgs.review-evidence/v1` for every blocking check based on a prior result
- [ ] Classifies missing bindings as UNBOUND and hash mismatches as STALE; both force FAIL
- [ ] Emits `cgs.gate-record/v1` with `stage_mutated: false`
- [ ] Defines `PROCEED_WITH_ACCEPTED_RISK` only in a separate `cgs.advance-request/v1`
- [ ] Contains no instruction that writes, creates, or updates `production/stage.txt`
- [ ] Solo mode skips directors without skipping deterministic quality or evidence checks

---

## Case 1: Six Valid Adjacent Transitions

Run this case once for every row:

| Input | stage.txt | Candidate next stage |
|---|---|---|
| `$gate-check concept-to-systems-design` | `Concept` | `Systems Design` |
| `$gate-check systems-design-to-technical-setup` | `Systems Design` | `Technical Setup` |
| `$gate-check technical-setup-to-pre-production` | `Technical Setup` | `Pre-Production` |
| `$gate-check pre-production-to-production` | `Pre-Production` | `Production` |
| `$gate-check production-to-polish` | `Production` | `Polish` |
| `$gate-check polish-to-release` | `Polish` | `Release` |

**Fixture:** All blocking checks pass. Every blocking prior-result check has a complete
`cgs.review-evidence/v1` record whose artifact paths and SHA-256 values match current
bytes. Capture a repository snapshot and stage-file hash before invocation.

**Expected behavior:**

1. The exact ID maps to the listed current and candidate stages.
2. Current stage is verified before any artifact check.
3. Every evidence hash is recomputed and matches.
4. Verdict is PASS and gate record disposition is ELIGIBLE.
5. Gate record says `stage_mutated: false`.
6. Repository snapshot and `stage.txt` bytes are unchanged.

---

## Case 2: Transition and State Validation Errors

Test each input independently:

- `$gate-check production` (phase-name shorthand)
- `$gate-check concept-to-production` (non-adjacent/unknown ID)
- `$gate-check production-to-polish` with `stage.txt = Pre-Production`
- Any transition with missing, empty, or unknown `stage.txt`
- No transition argument with `stage.txt = Release`

**Assertions:**

- [ ] Result is ERROR, not PASS/CONCERNS/FAIL
- [ ] Artifact checks and director panel do not run
- [ ] No gate record or advance request is emitted
- [ ] No project file changes

---

## Case 3: Hash-Bound Evidence

### 3a — Current evidence

Provide all required fields, a complete artifact-set manifest, and matching SHA-256
values. The producer verdict satisfies the checklist threshold.

- [ ] Evidence may satisfy the blocking check
- [ ] Gate output cites evidence record ID and current artifact hashes

### 3b — Stale evidence

Modify one reviewed artifact after the evidence record is produced.

- [ ] Recomputed hash mismatch is STALE
- [ ] Blocking check fails and overall verdict is FAIL
- [ ] Skill does not fall back to another historical glob or structural completeness

### 3c — Unbound evidence

Provide a historical report/verdict but omit its evidence record or one required field.

- [ ] Result is UNBOUND
- [ ] Blocking check fails and overall verdict is FAIL
- [ ] Document-internal sign-off and user recollection are not substitutes

---

## Case 4: Accepted Risk Preserves the Strict Verdict

**Fixture:** At least one blocking finding makes the verdict FAIL. The user explicitly
requests continuation and accepts every named risk.

**Assertions:**

- [ ] Gate record remains immutable with verdict FAIL and disposition NOT_ELIGIBLE
- [ ] Skill emits a separate `cgs.advance-request/v1`
- [ ] Request contains transition ID, gate record ID, operator, timestamp, accepted
      finding IDs, and evidence record IDs
- [ ] Requested disposition is `PROCEED_WITH_ACCEPTED_RISK`
- [ ] Neither output relabels the assessment as PASS
- [ ] `production/stage.txt` and transition history are not modified

---

## Case 5: Director Modes Do Not Bypass P0 Rules

### 5a — lean/full

- [ ] All four PHASE-GATE directors run in parallel
- [ ] NOT READY makes the strict verdict at least FAIL
- [ ] Explicit risk acceptance does not change that FAIL

### 5b — solo

- [ ] No director gates spawn
- [ ] Artifact, deterministic quality, evidence-binding, and stale checks still run
- [ ] Solo does not convert STALE or UNBOUND evidence into PASS

---

## Case 6: Mutation Guard

Run once with PASS and once with FAIL followed by accepted risk. Compare repository tree,
file hashes, and `stage.txt` metadata before and after.

- [ ] No file is created, edited, renamed, or deleted
- [ ] PASS produces only conversational output
- [ ] Accepted risk produces only conversational output
- [ ] Any attempted stage mutation fails the spec

---

## Case 7: Canonical Playtest-Session Counting

- [ ] Counts only distinct `production/playtests/<session-id>/report.md` results
- [ ] Requires COMPLETED, Gate Eligible YES, build/times/tester, and matching evidence hashes
- [ ] Templates, protocols, raw logs, reviews, ingest-only sessions, duplicates,
      legacy paths, and hash-mismatched reports count as zero
- [ ] A director review never increments the session count

## Case 8: Regression Selection Plus Build Receipt

- [ ] Selection manifest alone never passes the regression gate
- [ ] Revalidates QA/source/test/sensitivity hashes and active stable IDs
- [ ] Requires a runner receipt bound to the exact selection hash and target build
- [ ] Missing, stale, awaiting-run, indeterminate, quarantined-unverified, or any
      non-pass required test blocks the check

## Case 9: Release Collector Does Not Self-Approve

- [ ] Accepts only `Gate Decision: NOT EVALUATED` from release-checklist
- [ ] Re-hashes the exact release/policy/candidate/build/item evidence set
- [ ] Any unresolved hard item forces FAIL; advisory-only unresolved items force CONCERNS
- [ ] File existence, checkbox state, or merely running a checklist never passes
- [ ] Team-QA evidence passes only with current persisted COMPLETE + APPROVED +
      Gate Eligible YES for the exact candidate/build; conditions do not pass
- [ ] Localization requires current manifest/freeze/source/keyset/translation/
      font/UI/build receipts per locale; QA-plan-ready or MT drafts never pass

## Case 10: Runtime Performance Evidence Only

- [ ] Accepts only a persisted/read-back `performance-runtime-report-v1` bound to
      the exact versioned `performance-budget-v1`, source/build, platform/hardware,
      scenario, inputs, normalized data, and complete required matrix
- [ ] Requires `evidence_kind: RUNTIME_MEASUREMENT`, `gate_evidence_eligible: true`,
      `performance_targets_met: true`, and overall `WITHIN BUDGET`
- [ ] Recent files, prose budgets, static analysis, capture plans, conversation-only
      output, accepted risk, partial coverage, stale hashes, `CONCERNS`, and
      `OVER BUDGET` never pass

## Case 11: Current Persisted Vertical-Slice PROCEED

- [ ] Requires an explicitly supplied `vertical-slice-evaluation-report` schema 1
      and externally supplied report hash, then revalidates the complete referenced
      candidate/source/build/scope/evidence/playtest/velocity/decision graph
- [ ] PASS requires COMPLETE, evidence/product/final `PROCEED`, CURRENT,
      `Gate Eligible: YES`, `Persistence: VERIFIED`, and no later mutation
- [ ] A directory or report filename, skipped slice, PARTIAL, INCONCLUSIVE, PIVOT,
      KILL, BLOCKED, stale/unpersisted/advisory result, director concern, or hash
      mismatch never satisfies the transition

## Protocol Compliance

- [ ] Gate verdict is a strict calculation; user authority is represented separately
- [ ] Every accepted blocking prior-result conclusion is bound to exact current bytes
- [ ] Invalid or mismatched transitions cannot reach gate evaluation
- [ ] Only an independent, explicitly authorized stage-advancement workflow may mutate
      stage state; this skill stops after its records and next-step prompt

---

## Coverage Notes

This P0 specification covers transition identity, current-stage validation, stale and
unbound evidence, strict accepted-risk semantics, and read-only mutation guards. It does
not claim execution results; catalog result fields remain unchanged until tests run.
