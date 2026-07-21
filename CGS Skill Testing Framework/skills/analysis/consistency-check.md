# Skill Test Spec: $consistency-check

## Skill Summary

`$consistency-check` is a strictly read-only cross-GDD auditor. It reads the
complete in-scope GDD corpus, compares GDD claims directly, and may use
`design/registry/entities.yaml` as an additional neutral claim source. It checks
values, formulas, ownership, dependencies, and stale references. It returns its
complete report to the caller and never changes GDDs, the registry, logs, saved
reports, or session state.

The registry's `source` field is provenance, not product authority. When claims
compete, the skill reports both sides and requests an artifact-owner or user
decision; it does not select a winning number, formula, owner, or dependency.

The verdict contract is exactly `PASS | FINDINGS | PARTIAL | ERROR`.
`DEPENDENCY_GAP` is a finding category under `FINDINGS`, not a verdict.

---

## Static Assertions (Structural)

Verified automatically by `$skill-test static` — no fixture needed.

- [ ] YAML frontmatter contains only required `name` and non-empty
  `description`; `name` matches the skill directory
- [ ] Has at least two phase headings
- [ ] Contains all and only the verdict keywords `PASS`, `FINDINGS`, `PARTIAL`,
  and `ERROR` as the final verdict contract
- [ ] Defines verdict precedence: `ERROR`, then `PARTIAL`, then `FINDINGS`, then
  `PASS`
- [ ] States that the workflow is strictly read-only and its report is returned
  to the caller
- [ ] Contains no workflow step that creates, edits, appends, renames, or deletes
  a project file
- [ ] Does not describe the registry or its `source` field as authoritative
- [ ] Requires competing claims and their evidence to be shown without automatic
  resolution
- [ ] Has a verdict-appropriate next-step handoff and then stops

---

## Director Gate Checks

No director gates. The skill does not read
`production/session-state/review-mode.txt`, spawn an agent, or execute another
skill as part of the audit.

---

## Test Cases

### Case 1: Happy Path — direct scan succeeds without a registry

**Fixture:**

- `design/gdd/` contains exactly four system GDDs
- all overlapping values and formulas agree
- ownership claims do not compete
- all required dependencies resolve to existing system GDDs
- `design/registry/entities.yaml` does not exist

**Input:** `$consistency-check`

**Expected behavior:**

1. The skill inventories and reads all four GDDs in full.
2. It compares GDD claims directly instead of stopping because the registry is
   absent.
3. The coverage ledger reports registry coverage as missing and GDD coverage as
   complete.
4. It returns `No actionable consistency findings.`
5. Verdict: `PASS`.

**Assertions:**

- [ ] All four GDDs are read before the verdict
- [ ] Registry absence never produces “nothing to check”
- [ ] The report includes the coverage ledger and an empty findings section
- [ ] Verdict is `PASS`
- [ ] No file is changed
- [ ] A concise next-step handoff is present

---

### Case 2: Failure Path — competing damage formulas

**Fixture:**

- GDD-A defines `damage = attack * 1.5` for the same entity and conditions
- GDD-B defines `damage = attack * 2.0`
- all GDD inputs are readable and all other required checks complete

**Input:** `$consistency-check`

**Expected behavior:**

1. The skill reads the complete GDD corpus.
2. It reports `FORMULA_MISMATCH` with both filenames, both formulas, and precise
   evidence locations.
3. Status is `DECISION REQUIRED`; neither formula is selected automatically.
4. Verdict: `FINDINGS`.

**Assertions:**

- [ ] Verdict is `FINDINGS`, not `PASS`
- [ ] Category is `FORMULA_MISMATCH`
- [ ] Severity is `HIGH` for the direct normative contradiction
- [ ] Both claims and both evidence locations are shown
- [ ] The report identifies the decision owner or asks for a user decision
- [ ] The skill neither edits the documents nor proposes one formula as truth

---

### Case 3: Finding Path — unresolved dependency

**Fixture:**

- GDD-A declares system-B as a required dependency
- no system-B GDD or explicit planned-system record exists
- every input is readable and all other checks complete

**Input:** `$consistency-check`

**Expected behavior:**

1. The skill reports `DEPENDENCY_GAP` for GDD-A and missing system-B.
2. The finding cites GDD-A's declaration and the audited inventory.
3. Verdict: `FINDINGS`.

**Assertions:**

- [ ] `DEPENDENCY_GAP` is a category, not a verdict
- [ ] Verdict is `FINDINGS`
- [ ] The declaring document, missing target, evidence, and severity are shown
- [ ] The skill returns a handoff but does not invoke `$design-system`

---

### Case 4: Error Path — no GDDs found

**Fixture:** `design/gdd/` is empty or does not exist.

**Input:** `$consistency-check`

**Expected behavior:**

1. The skill attempts to inventory `design/gdd/`.
2. It explains that no auditable system GDD exists.
3. Verdict: `ERROR`.
4. It performs no write.

**Assertions:**

- [ ] The error names the expected GDD location
- [ ] Verdict is exactly `ERROR`
- [ ] No empty success report or `PASS` is produced
- [ ] The next action is to correct the scope or create/identify auditable GDDs

---

### Case 5: Partial Path — one GDD is unreadable

**Fixture:**

- four system GDDs are discovered
- three can be read and contain one proven ownership conflict
- one GDD cannot be read

**Input:** `$consistency-check`

**Expected behavior:**

1. The skill preserves the proven conflict in the findings table.
2. The coverage ledger marks the unreadable GDD as failed.
3. It does not claim the scan is complete.
4. Verdict: `PARTIAL`, which takes precedence over `FINDINGS`.

**Assertions:**

- [ ] Proven findings are not discarded
- [ ] The coverage limitation and affected file are explicit
- [ ] Verdict is `PARTIAL`
- [ ] Verdict is not `PASS` or `FINDINGS`
- [ ] No file is changed

---

### Case 6: Product-truth boundary — registry source conflicts with GDDs

**Fixture:**

- registry claim: `sword.value_gold = 100`, with `source: economy-gdd.md`
- economy-gdd.md claims `sword.value_gold = 100`
- loot-gdd.md claims `sword.value_gold = 125` for the same scope
- no current approved decision artifact selects either value

**Input:** `$consistency-check item:sword`

**Expected behavior:**

1. The skill reports the registry, economy GDD, and loot GDD as attributed
   claims.
2. It reports a `VALUE_MISMATCH` with competing evidence.
3. It does not say the registry or economy GDD is correct merely because of the
   `source` field.
4. It requests an artifact-owner or user decision.
5. Verdict: `FINDINGS`.

**Assertions:**

- [ ] Registry `source` is presented only as provenance
- [ ] No claim is labeled canonical, correct, stale, or wrong without explicit
  decision evidence
- [ ] Status is `DECISION REQUIRED`
- [ ] No registry or GDD correction is performed

---

### Case 7: Registry parse failure does not erase direct findings

**Fixture:**

- all GDDs are readable
- two GDDs contain a proven value mismatch
- `design/registry/entities.yaml` exists but is malformed

**Input:** `$consistency-check`

**Expected behavior:**

1. The skill completes direct GDD comparison and retains the mismatch.
2. Registry coverage is marked invalid.
3. Verdict: `PARTIAL` because one material coverage channel failed.

**Assertions:**

- [ ] Direct findings remain visible
- [ ] Malformed registry never causes a crash or false `PASS`
- [ ] Verdict is `PARTIAL`
- [ ] The registry is not repaired or rewritten

---

### Case 8: Mutation guard and no hidden workflow effects

**Fixture:**

- at least two system GDDs and a valid registry exist
- `docs/consistency-failures.md` and
  `production/session-state/active.md` exist
- record pre-run hashes for the GDD tree, registry, failure log, session state,
  and all other repository files
- `production/session-state/review-mode.txt` contains `full`

**Input:** `$consistency-check`

**Expected behavior:**

1. The skill returns its report in the response.
2. It does not read review mode, spawn agents, execute another skill, or persist
   the report.
3. Every pre-run file hash and the repository path inventory are unchanged.

**Assertions:**

- [ ] GDD, registry, log, session-state, and repository hashes are unchanged
- [ ] No file or directory is created, removed, renamed, or appended
- [ ] No director gate or downstream skill runs
- [ ] Output contains no registry correction, report-save, log-append, or
  session-state-update step

---

## Protocol Compliance

- [ ] Reads every in-scope system GDD before a non-`ERROR` verdict
- [ ] Compares GDD claims directly; registry data is optional context
- [ ] Returns the complete coverage ledger and findings to the caller
- [ ] Uses exactly one final verdict from `PASS | FINDINGS | PARTIAL | ERROR`
- [ ] Treats dependency gaps as findings
- [ ] Gives `PARTIAL` precedence when useful evidence exists but material
  coverage is incomplete
- [ ] Never treats registry `source` as automatic product truth
- [ ] Never chooses a conflicting value, formula, owner, or dependency without
  explicit current decision evidence
- [ ] Performs zero project writes and has no director or skill chaining
- [ ] Ends with one verdict-appropriate handoff

---

## Coverage Notes

- This spec validates the P0 contract: read-only operation, neutral treatment of
  competing claims, direct all-GDD comparison, and one synchronized verdict
  model.
- More advanced claim schemas, immutable incremental baselines, bounded scan
  budgets, stable finding hashes, and semantic normalization require separate
  follow-up coverage.
- Deep design-theory analysis remains outside this skill's scope.

