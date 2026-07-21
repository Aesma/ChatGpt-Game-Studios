# Skill Test Spec: $review-all-gdds

## Skill Summary

`$review-all-gdds` performs a report-only holistic review of the current,
hash-bound system-GDD set. It builds an input manifest, runs cross-GDD
consistency and game-design-holism phases in parallel when the selected mode
requires both, walks sampled cross-system scenarios, merges explicit coverage,
and returns exactly `PASS`, `CONCERNS`, `FAIL`, or `PARTIAL`.

Conversation output is the default. The only permitted mutation is one new,
explicitly authorized immutable report at the exact previewed path. The skill
never modifies GDDs, systems index, registry, session state, lifecycle status,
sign-off, or accepted-risk records.

The skill is itself the holistic review gate input. It does not spawn a director
gate agent. Design-theory observations are `HYPOTHESIS / ADVISORY` unless
they reproducibly violate an explicit anti-pillar, owner-approved invariant, or
owner-approved threshold in the hashed inputs.

---

## Static Assertions (Structural)

- [ ] YAML frontmatter contains only required `name` and non-empty
      `description`; name matches the skill directory
- [ ] Has at least five phase headings across the main file and required
      continuation
- [ ] Declares exactly the verdict vocabulary PASS / CONCERNS / FAIL / PARTIAL
- [ ] Declares conversation output as default and limits writes to one new,
      explicitly authorized immutable report
- [ ] Explicitly forbids mutations to GDDs, systems index, registry, session
      state, lifecycle status, sign-off, and accepted-risk records
- [ ] Builds an input manifest with project ID, run ID, source revision,
      canonical paths, SHA-256 hashes, mode, and coverage
- [ ] Defines changed input paths/hashes as stale and rejects stale PASS as gate
      evidence
- [ ] Requires incomplete coverage or worker failure to produce PARTIAL
- [ ] Treats unmeasured design theory as HYPOTHESIS / ADVISORY with assumptions,
      a counterexample, and a validation plan
- [ ] Documents parallel spawning of consistency and design-theory phases
- [ ] Includes the cross-system scenario walkthrough and a separate handoff

---

## Director Gate Checks

No director gates. This skill produces evidence for a later gate; delegating its
own verdict to a director gate would create a circular dependency.

---

## Test Cases

### Case 1: Clean, fully covered GDD set

**Fixture:** At least three current system GDDs with compatible rules, no stale
references, and explicit pillar alignment.

**Input:** `$review-all-gdds full`

**Expected behavior:**

1. Builds a complete canonical path/SHA-256 manifest and run ID.
2. Runs consistency and design-theory phases in parallel.
3. Completes the scenario walkthrough and coverage table.
4. Reports no blockers, warnings, or advisory hypotheses.
5. Returns `PASS`.
6. Does not write unless the exact immutable report path is authorized.

**Assertions:**

- [ ] Verdict is PASS
- [ ] Coverage status is COMPLETE with no unchecked scope
- [ ] Report contains project ID, run ID, source revision, mode, manifest digest,
      and per-input hashes
- [ ] No project file is mutated by default
- [ ] Handoff offers `$gate-check` or `$create-architecture`

---

### Case 2: Deterministic cross-GDD contradiction

**Fixture:** GDD-A defines an output floor; GDD-B explicitly allows the same
output below that floor, with no scoped exception.

**Input:** `$review-all-gdds consistency`

**Expected behavior:**

1. Quotes or precisely describes both current rules and their paths/sections.
2. Binds both findings to input hashes.
3. Classifies the reproducible contradiction as blocking.
4. Returns `FAIL`.
5. Does not choose which GDD is authoritative or modify either GDD.

**Assertions:**

- [ ] Verdict is FAIL
- [ ] Both filenames, sections, rules, and hashes are present
- [ ] Issue is deterministic and blocking
- [ ] No source, index, session, or lifecycle mutation occurs

---

### Case 3: Orphaned dependency without a contradictory rule

**Fixture:** GDD-A references system-B, but no system-B GDD exists; all checked
rules are otherwise compatible.

**Input:** `$review-all-gdds consistency`

**Expected behavior:** Reports the exact dependency gap as non-blocking and
returns `CONCERNS`.

**Assertions:**

- [ ] Verdict is CONCERNS
- [ ] GDD-A and system-B are named
- [ ] The gap is not silently ignored or upgraded to a blocker without an
      approved invariant
- [ ] Handoff recommends a separate owner-authorized remediation workflow

---

### Case 4: No reviewable GDDs

**Fixture:** No system GDDs exist.

**Input:** `$review-all-gdds`

**Expected behavior:** Stops with clear guidance and no review verdict or file
mutation.

**Assertions:**

- [ ] No PASS / CONCERNS / FAIL / PARTIAL verdict is emitted for a run that
      never acquired minimum inputs
- [ ] Error explains the minimum input requirement
- [ ] No report, session state, or project file is created

---

### Case 5: No director gate in any mode

**Fixture:** At least two valid system GDDs; an unrelated
`production/session-state/review-mode.txt` exists.

**Input:** `$review-all-gdds full`

**Assertions:**

- [ ] No director gate agent is spawned
- [ ] `review-mode.txt` is not read or modified
- [ ] No gate-prefixed entry is fabricated
- [ ] The review's own evidence and verdict are produced normally

---

### Case 6: Unmeasured design-theory risk

**Fixture:** Six systems appear concurrently, and ranged attacks list 80% of
melee damage. No owner-approved attention budget, dominance threshold,
telemetry, simulation, or playtest result exists.

**Input:** `$review-all-gdds design-theory`

**Expected behavior:** Records advisory hypotheses rather than cognitive-load or
dominant-strategy blockers.

**Assertions:**

- [ ] Each theory item is labeled HYPOTHESIS / ADVISORY
- [ ] Each includes evidence, assumptions, a plausible counterexample, and a
      concrete validation plan
- [ ] Missing measurements are labeled NEEDS_MEASUREMENT
- [ ] These heuristics alone cannot produce FAIL
- [ ] Verdict is CONCERNS when coverage is otherwise complete

---

### Case 7: Incomplete worker or scenario coverage

**Fixture:** A required parallel worker errors, returns mismatched input hashes,
or cannot complete a required check.

**Input:** `$review-all-gdds full`

**Expected behavior:** Preserves completed evidence, names unchecked scope, and
returns `PARTIAL`.

**Assertions:**

- [ ] Verdict is PARTIAL
- [ ] Coverage identifies the failed worker/check and affected paths
- [ ] Output is never PASS
- [ ] Available evidence is not discarded
- [ ] No mutation occurs unless the user separately authorizes the exact report

---

### Case 8: Stale prior report

**Fixture:** A prior PASS exists, then one input GDD changes content, is renamed,
is removed, or a new review input is added.

**Input:** Validate the prior report for gate consumption or run
`$review-all-gdds since-last-review`.

**Expected behavior:** Recomputes exact hashes, marks the prior report STALE, and
does not use it as gate evidence. Incremental mode uses the embedded manifest,
never filesystem modification time; without a trustworthy baseline it falls
back to full mode.

**Assertions:**

- [ ] Any path/hash-set difference makes the prior report stale
- [ ] Stale PASS is rejected as gate evidence
- [ ] Baseline selection does not use report mtime
- [ ] Current report records project ID, mode, source revision, run ID, manifest,
      and coverage

---

### Case 9: Mutation guard and optional persistence

**Fixture:** A complete report is rendered. Test both decline and explicit
approval of a unique path.

**Expected behavior:**

- Decline: zero file mutations.
- Approve: creates only the exact new report path, verifies its manifest digest,
  and leaves all other files byte-identical.
- Existing target path: refuses to overwrite and selects no replacement without
  new approval.

**Assertions:**

- [ ] GDDs, systems index, registry, session state, lifecycle, sign-off, and
      accepted-risk records remain byte-identical
- [ ] At most one new immutable report is written
- [ ] No existing report is overwritten
- [ ] A corrected report uses a new run and `supersedes_run_id`

---

### Case 10: Accepted risk does not rewrite verdict

**Fixture:** A current FAIL report and a separate owner-signed accepted-risk
record naming its run ID and exact findings.

**Expected behavior:** The review remains FAIL. The record is reported separately
with scope and expiry; the reviewer neither creates nor signs it.

**Assertions:**

- [ ] FAIL is never changed to PASS or CONCERNS
- [ ] Accepted risk includes run ID, exact findings, scope, owner/signature, and
      expiry
- [ ] Missing or expired accepted risk provides no exception
- [ ] The consuming gate, not this reviewer, decides whether policy permits
      proceeding

---

## Protocol Compliance

- [ ] Full mode runs consistency and design-theory phases in parallel
- [ ] Scenario walkthrough and coverage are represented in the report
- [ ] Verdict is exactly one of PASS / CONCERNS / FAIL / PARTIAL
- [ ] Deterministic blockers and advisory hypotheses are separated
- [ ] Critical unknown or incomplete coverage cannot PASS
- [ ] Default execution is mutation-free
- [ ] Optional persistence writes only one authorized immutable report
- [ ] Report identity and staleness are hash-based, not timestamp-based
- [ ] FAIL remains FAIL even when a separate accepted risk exists
- [ ] Handoff invokes a separate workflow and does not edit reviewed sources

---

## Coverage Notes

Cases 1–5 preserve the baseline consistency, empty-input, and no-director-gate
behaviors. Cases 6–10 cover the P0 contract: theory evidence boundaries,
PARTIAL, input staleness, mutation guard, immutable report persistence, and
accepted-risk separation.
